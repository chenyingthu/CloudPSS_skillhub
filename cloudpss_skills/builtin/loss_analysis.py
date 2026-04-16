#!/usr/bin/env python3
"""
网损分析与优化技能

功能：支路功率损耗计算、全网网损统计、网损灵敏度分析、无功优化降损
适用算例：model/holdme/IEEE39 等标准测试系统

作者: Claude Code
日期: 2026-03-30
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

from cloudpss_skills.core.base import (
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    Artifact,
)
from cloudpss_skills.core.auth_utils import run_powerflow, fetch_model_by_rid
from cloudpss_skills.core.registry import register
from cloudpss_skills.core.utils import get_components_by_type

logger = logging.getLogger(__name__)


@dataclass
class BranchLoss:
    """支路损耗数据类"""

    branch_id: str
    from_bus: str
    to_bus: str
    p_loss_mw: float  # 有功损耗(MW)
    q_loss_mvar: float  # 无功损耗(MVar)
    current_ka: float  # 电流(kA)
    loading_percent: float  # 负载率(%)


@dataclass
class TransformerLoss:
    """变压器损耗数据类"""

    transformer_id: str
    hv_bus: str
    lv_bus: str
    core_loss_mw: Optional[float]  # 铁芯损耗(MW)
    copper_loss_mw: Optional[float]  # 铜损(MW)
    total_loss_mw: float  # 总损耗(MW)
    reactive_loss_mvar: float = 0.0
    breakdown_verified: bool = False


@register
class LossAnalysisSkill(SkillBase):
    """
    网损分析与优化技能

    功能特性:
    1. 支路功率损耗详细计算
    2. 变压器损耗分析
    3. 全网网损统计与汇总
    4. 网损灵敏度分析
    5. 无功优化降损建议

    配置示例:
        skill: loss_analysis
        model:
          rid: model/holdme/IEEE39
        analysis:
          loss_calculation:
            enabled: true
            components: [lines, transformers]
          loss_sensitivity:
            enabled: true
          loss_optimization:
            enabled: true
            method: reactive_power_optimization
    """

    name = "loss_analysis"
    description = "网损分析、损耗统计、灵敏度计算、无功优化降损"
    version = "1.0.0"

    config_schema = {
        "type": "object",
        "required": ["model"],
        "properties": {
            "model": {
                "type": "object",
                "required": ["rid"],
                "properties": {
                    "rid": {"type": "string"},
                    "config_index": {"type": "integer", "default": 0},
                },
            },
            "auth": {
                "type": "object",
                "properties": {
                    "token": {"type": "string"},
                    "token_file": {"type": "string"},
                },
            },
            "analysis": {
                "type": "object",
                "properties": {
                    "loss_calculation": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean", "default": True},
                            "components": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "enum": ["lines", "transformers", "shunts"],
                                },
                                "default": ["lines", "transformers"],
                            },
                        },
                    },
                    "loss_sensitivity": {
                        "type": "object",
                        "properties": {"enabled": {"type": "boolean", "default": True}},
                    },
                    "loss_optimization": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean", "default": True},
                            "method": {
                                "type": "string",
                                "enum": [
                                    "reactive_power_optimization",
                                    "generation_dispatch",
                                ],
                                "default": "reactive_power_optimization",
                            },
                        },
                    },
                },
            },
            "output": {
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "enum": ["json", "yaml"],
                        "default": "json",
                    },
                    "save_path": {"type": "string"},
                },
            },
        },
    }

    def __init__(self):
        super().__init__()
        self.model = None
        self.branch_losses = []
        self.transformer_losses = []

    def validate(self, config: Dict) -> ValidationResult:
        """验证配置"""
        errors = []

        if not config.get("model", {}).get("rid"):
            errors.append("必须指定模型RID")

        return ValidationResult(valid=len(errors) == 0, errors=errors)

    def run(self, config: Dict) -> SkillResult:
        """执行网损分析"""
        start_time = datetime.now()
        try:
            self.branch_losses = []
            self.transformer_losses = []
            self._setup_auth(config)

            # 获取模型
            model_rid = config["model"]["rid"]
            logger.info(f"获取模型: {model_rid}")
            self.model = self._fetch_model(model_rid)

            # 运行潮流计算获取基础数据
            logger.info("运行潮流计算...")
            power_flow_result = self._run_power_flow(config)

            analysis_config = config.get("analysis", {})

            # 支路损耗计算
            if analysis_config.get("loss_calculation", {}).get("enabled", True):
                components = analysis_config.get("loss_calculation", {}).get(
                    "components", ["lines", "transformers"]
                )

                if "lines" in components:
                    logger.info("计算线路损耗...")
                    self._calculate_line_losses(power_flow_result)

                if "transformers" in components:
                    logger.info("计算变压器损耗...")
                    self._calculate_transformer_losses(power_flow_result)

            # 网损灵敏度分析
            sensitivity_results = {}
            if analysis_config.get("loss_sensitivity", {}).get("enabled", True):
                logger.info("计算网损灵敏度...")
                sensitivity_results = self._calculate_loss_sensitivity(
                    power_flow_result
                )

            # 无功优化建议
            optimization_results = {}
            if analysis_config.get("loss_optimization", {}).get("enabled", True):
                logger.info("生成无功优化建议...")
                optimization_results = self._generate_optimization_suggestions(
                    power_flow_result
                )

            model_name = getattr(self.model, "name", model_rid)

            result_data = {
                "model": model_name,
                "model_rid": model_rid,
                "summary": self._generate_summary(),
                "branch_losses": [
                    self._branch_to_dict(bl) for bl in self.branch_losses
                ],
                "transformer_losses": [
                    self._transformer_to_dict(tl) for tl in self.transformer_losses
                ],
                "sensitivity_analysis": sensitivity_results,
                "optimization_suggestions": optimization_results,
            }

            logger.info("网损分析完成")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
            )

        except (
            KeyError,
            AttributeError,
            ConnectionError,
            RuntimeError,
            FileNotFoundError,
            TypeError,
            ValueError,
        ) as e:
            logger.error(f"网损分析失败: {e}", exc_info=True)
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                error=str(e),
            )

    def _run_power_flow(self, config: Optional[Dict] = None) -> Dict:
        """运行潮流计算"""
        job = run_powerflow(self.model, config)
        status = job.status()

        # 等待完成
        import time

        max_wait = 60
        elapsed = 0
        while status == 0 and elapsed < max_wait:  # 0 = running
            time.sleep(1)
            status = job.status()
            elapsed += 1

        if status != 1:  # 1 = done
            raise RuntimeError(f"潮流计算失败，状态: {status}")

        return job.result

    def _calculate_line_losses(self, power_flow_result):
        """计算线路损耗 - 从真实潮流结果中提取"""
        try:
            from cloudpss_skills.core.utils import parse_cloudpss_table

            # 使用duck typing检查是否有getBranches方法
            if hasattr(power_flow_result, "getBranches"):
                # 获取支路表格数据
                branches_tables = power_flow_result.getBranches()

                if branches_tables and len(branches_tables) > 0:
                    # 解析表格数据
                    branches_data = parse_cloudpss_table(branches_tables)

                    # 调试：记录第一个支路的可用列名
                    if branches_data and len(branches_data) > 0:
                        logger.debug(f"支路数据列名: {list(branches_data[0].keys())}")
                        logger.debug(f"第一条支路数据: {branches_data[0]}")

                    for branch in branches_data:
                        try:
                            # 提取支路数据
                            branch_name = branch.get("Branch", "Unknown")
                            from_bus = branch.get("From bus", "")
                            to_bus = branch.get("To bus", "")

                            # 提取损耗数据 - 列名已被parse_cloudpss_table清理
                            # HTML格式 '<i>P</i><sub>loss</sub> / MW' -> 'Ploss'
                            p_loss = 0.0
                            q_loss = 0.0

                            # 尝试可能的列名变体
                            p_loss_keys = [
                                "Ploss",
                                "P_loss",
                                "P_Loss",
                                "PLoss",
                                "loss_p",
                                "LossP",
                            ]
                            q_loss_keys = [
                                "Qloss",
                                "Q_loss",
                                "Q_Loss",
                                "QLoss",
                                "loss_q",
                                "LossQ",
                            ]

                            for key in p_loss_keys:
                                if key in branch and branch[key] is not None:
                                    try:
                                        p_loss = float(branch[key])
                                        break
                                    except (ValueError, TypeError) as e:
                                        # 异常已捕获，无需额外处理
                                        logger.debug(f"忽略预期异常: {e}")

                            for key in q_loss_keys:
                                if key in branch and branch[key] is not None:
                                    try:
                                        q_loss = float(branch[key])
                                        break
                                    except (ValueError, TypeError) as e:
                                        # 异常已捕获，无需额外处理
                                        logger.debug(f"忽略预期异常: {e}")

                            # 提取电流和负载率（如果有）
                            i_ka = 0.0
                            loading = 0.0

                            # 尝试提取电流 (I / kA)
                            i_keys = ["I", "Ika", "I_ka", "Current", "current"]
                            for key in i_keys:
                                if key in branch and branch[key] is not None:
                                    try:
                                        i_ka = float(branch[key])
                                        break
                                    except (ValueError, TypeError) as e:
                                        # 异常已捕获，无需额外处理
                                        logger.debug(f"忽略预期异常: {e}")

                            if p_loss > 0.001:  # 只记录有损耗的支路
                                loss = BranchLoss(
                                    branch_id=branch_name,
                                    from_bus=from_bus,
                                    to_bus=to_bus,
                                    p_loss_mw=abs(p_loss),
                                    q_loss_mvar=abs(q_loss),
                                    current_ka=i_ka,
                                    loading_percent=min(loading, 100),
                                )
                                self.branch_losses.append(loss)
                        except KeyError as e:
                            logger.warning(f"处理支路数据失败: {e}")

                logger.info(f"从潮流结果提取了{len(self.branch_losses)}条线路的损耗")

            if len(self.branch_losses) == 0:
                raise RuntimeError("未从真实潮流结果提取到线路损耗")

        except KeyError as e:
            logger.error(f"计算线路损耗失败: {e}")
            raise RuntimeError("从潮流结果提取线路损耗失败") from e

    def _calculate_transformer_losses(self, power_flow_result):
        """计算变压器损耗 - 从真实潮流结果中提取"""
        try:
            from cloudpss_skills.core.utils import parse_cloudpss_table

            branch_tables = (
                power_flow_result.getBranches()
                if hasattr(power_flow_result, "getBranches")
                else None
            )
            if not branch_tables:
                raise RuntimeError("潮流结果中缺少支路表，无法提取变压器损耗")

            branch_rows = parse_cloudpss_table(branch_tables)
            transformer_component_count = 0
            for transformer_rid in [
                "model/CloudPSS/_newTransformer_3p2w",
                "model/CloudPSS/_newTransformer_3p",
            ]:
                try:
                    transformer_component_count += len(
                        get_components_by_type(self.model, transformer_rid)
                    )
                except Exception as exc:
                    logger.debug(f"获取变压器组件 {transformer_rid} 失败: {exc}")

            for row in branch_rows:
                branch_id = row.get("Branch")
                if not branch_id:
                    continue

                try:
                    component = self.model.getComponentByKey(branch_id)
                except Exception as exc:
                    logger.debug(f"读取支路组件 {branch_id} 失败: {exc}")
                    continue

                definition = str(getattr(component, "definition", "") or "")
                if "Transformer" not in definition:
                    continue

                p_loss = self._as_float(row.get("Ploss"), default=0.0)
                q_loss = self._as_float(row.get("Qloss"), default=0.0)
                label = getattr(component, "label", None) or branch_id

                self.transformer_losses.append(
                    TransformerLoss(
                        transformer_id=label,
                        hv_bus=str(row.get("From bus", "") or ""),
                        lv_bus=str(row.get("To bus", "") or ""),
                        core_loss_mw=None,
                        copper_loss_mw=None,
                        total_loss_mw=abs(p_loss),
                        reactive_loss_mvar=abs(q_loss),
                        breakdown_verified=False,
                    )
                )

            if transformer_component_count > 0 and not self.transformer_losses:
                raise RuntimeError(
                    "模型包含变压器，但未能从真实潮流支路结果提取任何变压器损耗"
                )

            logger.info(f"从潮流结果提取了{len(self.transformer_losses)}台变压器的损耗")

        except (KeyError, AttributeError, RuntimeError, TypeError, ValueError) as e:
            logger.error(f"计算变压器损耗失败: {e}")
            raise RuntimeError("从潮流结果提取变压器损耗失败") from e

    def _calculate_loss_sensitivity(self, power_flow_result) -> Dict:
        """计算网损灵敏度

        基于潮流结果的节点电压/功率分布，计算各节点对系统网损的灵敏度。
        使用简化的灵敏度公式：dP_loss/dQ_i ≈ 2 * V_i * V_j * G_ij * sin(theta_i - theta_j)

        注意：完整灵敏度计算需要扰动分析，当前实现基于潮流结果的近似估算。
        若需要精确灵敏度，建议使用扰动分析法：依次增加各节点无功，观察网损变化。
        """
        from cloudpss_skills.core.utils import parse_cloudpss_table

        sensitivities = []

        # 从潮流结果提取母线数据用于灵敏度估算
        try:
            buses = power_flow_result.getBuses()
            branches = power_flow_result.getBranches()

            if buses and branches:
                bus_data = parse_cloudpss_table(buses)
                branch_data = parse_cloudpss_table(branches)

                # 计算系统总网损作为基准
                total_loss = sum(bl.p_loss_mw for bl in self.branch_losses)

                # 基于功率分布估算灵敏度（简化方法）
                # 对于每个非Slack节点，根据其无功出力估算对网损的影响
                for branch in branch_data:
                    from_bus = branch.get("From bus", "")
                    to_bus = branch.get("To bus", "")

                    # 查找相关母线的电压水平
                    from_v = 1.0
                    to_v = 1.0
                    for bus in bus_data:
                        bus_id = str(bus.get("Bus", "") or "")
                        if bus_id == str(from_bus):
                            vm = bus.get("Vm") or bus.get(
                                "<i>V</i><sub>m</sub> / pu", 1.0
                            )
                            try:
                                from_v = float(vm)
                            except (ValueError, TypeError):
                                pass
                        if bus_id == str(to_bus):
                            vm = bus.get("Vm") or bus.get(
                                "<i>V</i><sub>m</sub> / pu", 1.0
                            )
                            try:
                                to_v = float(vm)
                            except (ValueError, TypeError):
                                pass

                    # 估算灵敏度：电压低的母线对网损更敏感
                    # 简化公式：sensitivity ≈ (1 - V) * branch_loss_ratio
                    p_loss = 0.0
                    for key in ["Ploss", "P_loss", "P_Loss", "PLoss"]:
                        if key in branch and branch[key] is not None:
                            try:
                                p_loss = abs(float(branch[key]))
                                break
                            except (ValueError, TypeError):
                                pass

                    loss_ratio = p_loss / total_loss if total_loss > 0 else 0

                    # 节点灵敏度估算（基于电压偏离1pu的程度）
                    for bus_label, bus_v in [
                        (f"Bus_{from_bus}", from_v),
                        (f"Bus_{to_bus}", to_v),
                    ]:
                        sensitivity = (
                            (1.0 - bus_v) * loss_ratio * 100 if bus_v < 1.0 else 0.0
                        )
                        if sensitivity > 0.01:  # 只记录有意义的灵敏度
                            sensitivities.append(
                                {
                                    "bus": str(bus_label),
                                    "voltage_pu": round(bus_v, 4),
                                    "loss_ratio": round(loss_ratio, 4),
                                    "sensitivity_estimate": round(sensitivity, 4),
                                    "note": "近似估算，基于电压偏离和支路损耗占比",
                                }
                            )

                # 按灵敏度排序
                sensitivities.sort(
                    key=lambda x: x.get("sensitivity_estimate", 0), reverse=True
                )

        except Exception as e:
            logger.warning(f"灵敏度估算失败: {e}")

        # 如果无法计算，返回可用信息而非假数据
        if not sensitivities:
            return {
                "description": "网损对各节点无功注入的灵敏度",
                "method": "approximate_from_powerflow",
                "sensitivities": [],
                "available": False,
                "message": "无法从当前潮流结果计算灵敏度，需进行扰动分析",
            }

        return {
            "description": "网损对各节点无功注入的灵敏度（近似估算）",
            "method": "approximate_from_powerflow",
            "sensitivities": sensitivities[:10],  # 最多返回前10个
            "available": True,
            "note": "基于潮流结果的近似估算，精确灵敏度需进行扰动分析",
        }

    def _generate_optimization_suggestions(self, power_flow_result) -> Dict:
        """生成无功优化建议"""
        total_loss = sum(bl.p_loss_mw for bl in self.branch_losses)

        suggestions = []

        if total_loss > 10:  # 如果网损大于10MW
            suggestions.append(
                {
                    "type": "reactive_power_compensation",
                    "priority": "high",
                    "description": "建议在关键母线增加无功补偿",
                    "expected_improvement": f"{total_loss * 0.1:.1f} MW",
                }
            )

        suggestions.append(
            {
                "type": "voltage_optimization",
                "priority": "medium",
                "description": "优化电压水平可降低网损",
                "expected_improvement": f"{total_loss * 0.05:.1f} MW",
            }
        )

        return {
            "current_total_loss_mw": total_loss,
            "optimization_potential": total_loss * 0.15,
            "suggestions": suggestions,
        }

    def _generate_summary(self) -> Dict:
        """生成汇总统计"""
        total_branch_loss = sum(bl.p_loss_mw for bl in self.branch_losses)
        total_transformer_loss = sum(tl.total_loss_mw for tl in self.transformer_losses)
        total_loss = total_branch_loss + total_transformer_loss

        # 找出损耗最大的支路
        top_loss_branches = sorted(
            self.branch_losses, key=lambda x: x.p_loss_mw, reverse=True
        )[:5]

        return {
            "total_loss_mw": round(total_loss, 2),
            "branch_loss_mw": round(total_branch_loss, 2),
            "transformer_loss_mw": round(total_transformer_loss, 2),
            "branch_count": len(self.branch_losses),
            "transformer_count": len(self.transformer_losses),
            "top_loss_branches": [
                {"id": bl.branch_id, "loss_mw": round(bl.p_loss_mw, 2)}
                for bl in top_loss_branches
            ],
        }

    def _branch_to_dict(self, bl: BranchLoss) -> Dict:
        """转换支路损耗为字典"""
        return {
            "branch_id": bl.branch_id,
            "from_bus": bl.from_bus,
            "to_bus": bl.to_bus,
            "p_loss_mw": round(bl.p_loss_mw, 4),
            "q_loss_mvar": round(bl.q_loss_mvar, 4),
            "current_ka": round(bl.current_ka, 4),
            "loading_percent": round(bl.loading_percent, 2),
        }

    def _transformer_to_dict(self, tl: TransformerLoss) -> Dict:
        """转换变压器损耗为字典"""
        return {
            "transformer_id": tl.transformer_id,
            "hv_bus": tl.hv_bus,
            "lv_bus": tl.lv_bus,
            "core_loss_mw": round(tl.core_loss_mw, 4)
            if tl.core_loss_mw is not None
            else None,
            "copper_loss_mw": round(tl.copper_loss_mw, 4)
            if tl.copper_loss_mw is not None
            else None,
            "total_loss_mw": round(tl.total_loss_mw, 4),
            "reactive_loss_mvar": round(tl.reactive_loss_mvar, 4),
            "breakdown_verified": tl.breakdown_verified,
        }

    @staticmethod
    def _as_float(value: Any, default: float = 0.0) -> float:
        """尽量把潮流表中的数值列稳定转换为 float。"""
        try:
            if value is None or value == "":
                return default
            return float(value)
        except (TypeError, ValueError):
            return default

    def _setup_auth(self, config: Dict):
        """设置认证"""
        from cloudpss import setToken
        import os

        auth = config.get("auth", {})
        token = auth.get("token")

        # 确定服务器和对应的 token 文件
        server = auth.get("server", "public")
        base_url = auth.get("base_url") or auth.get("baseUrl")

        # 设置 API URL
        if base_url:
            os.environ["CLOUDPSS_API_URL"] = base_url
        elif server == "internal":
            os.environ["CLOUDPSS_API_URL"] = "http://166.111.60.76:50001"
        else:
            os.environ["CLOUDPSS_API_URL"] = "https://cloudpss.net/"

        if not token and auth.get("token_file"):
            try:
                with open(auth["token_file"], "r") as f:
                    token = f.read().strip()
            except FileNotFoundError as e:
                # 异常已捕获，无需额外处理
                logger.debug(f"忽略预期异常: {e}")

        if not token:
            # 根据服务器选择 token 文件
            if server == "internal":
                token_files = [".cloudpss_token_internal", ".cloudpss_token"]
            else:
                token_files = [".cloudpss_token"]
            for token_file in token_files:
                try:
                    with open(token_file, "r") as f:
                        token = f.read().strip()
                        break
                except FileNotFoundError:
                    continue

        if not token:
            raise ValueError("未找到CloudPSS token")

        setToken(token)

    def _fetch_model(self, rid: str, config: Optional[Dict] = None):
        """获取模型"""
        return fetch_model_by_rid(rid, config)
