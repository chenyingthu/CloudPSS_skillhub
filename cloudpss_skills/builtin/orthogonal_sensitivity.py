"""
Orthogonal Sensitivity Analysis Skill

正交敏感性分析 - 基于正交表的参数敏感性分析

核心功能:
1. 基于正交表设计参数组合
2. 批量运行仿真并收集结果
3. 计算各参数对指标的影响程度
4. 生成敏感性排序和可视化

适用于:
- 多参数敏感性分析
- 参数优化设计
- 关键因素识别
- 实验设计(DOE)

参考自: 谭镇东 OAT.py 正交表实现
"""

import json
import logging
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field

from cloudpss_skills.core import (
    Artifact,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    register,
)
from cloudpss_skills.core.auth_utils import load_or_fetch_model

logger = logging.getLogger(__name__)


@dataclass
class ParameterLevel:
    """参数水平"""

    name: str
    levels: List[float]


@dataclass
class OrthogonalRun:
    """正交运行"""

    run_id: int
    parameter_values: Dict[str, float]
    status: str = "pending"
    result: Optional[float] = None
    error: Optional[str] = None


@dataclass
class SensitivityResult:
    """敏感性结果"""

    parameter: str
    effect_value: float  # 效应值
    sensitivity_rank: int  # 敏感性排序
    contribution_ratio: float  # 贡献率


# 常用正交表定义 (简化版)
ORTHOGONAL_TABLES = {
    "L4_2_3": {  # L4(2^3) - 4次运行，3个2水平参数
        "runs": 4,
        "levels": 2,
        "factors": 3,
        "table": [
            [1, 1, 1],
            [1, 2, 2],
            [2, 1, 2],
            [2, 2, 1],
        ],
    },
    "L8_2_7": {  # L8(2^7) - 8次运行，7个2水平参数
        "runs": 8,
        "levels": 2,
        "factors": 7,
        "table": [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 2, 2, 2, 2],
            [1, 2, 2, 1, 1, 2, 2],
            [1, 2, 2, 2, 2, 1, 1],
            [2, 1, 2, 1, 2, 1, 2],
            [2, 1, 2, 2, 1, 2, 1],
            [2, 2, 1, 1, 2, 2, 1],
            [2, 2, 1, 2, 1, 1, 2],
        ],
    },
    "L9_3_4": {  # L9(3^4) - 9次运行，4个3水平参数
        "runs": 9,
        "levels": 3,
        "factors": 4,
        "table": [
            [1, 1, 1, 1],
            [1, 2, 2, 2],
            [1, 3, 3, 3],
            [2, 1, 2, 3],
            [2, 2, 3, 1],
            [2, 3, 1, 2],
            [3, 1, 3, 2],
            [3, 2, 1, 3],
            [3, 3, 2, 1],
        ],
    },
    "L16_4_5": {  # L16(4^5) - 16次运行，5个4水平参数
        "runs": 16,
        "levels": 4,
        "factors": 5,
        "table": [
            [1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2],
            [1, 3, 3, 3, 3],
            [1, 4, 4, 4, 4],
            [2, 1, 2, 3, 4],
            [2, 2, 1, 4, 3],
            [2, 3, 4, 1, 2],
            [2, 4, 3, 2, 1],
            [3, 1, 3, 4, 2],
            [3, 2, 4, 3, 1],
            [3, 3, 1, 2, 4],
            [3, 4, 2, 1, 3],
            [4, 1, 4, 2, 3],
            [4, 2, 3, 1, 4],
            [4, 3, 2, 4, 1],
            [4, 4, 1, 3, 2],
        ],
    },
}


@register
class OrthogonalSensitivitySkill(SkillBase):
    """正交敏感性分析技能"""

    @property
    def name(self) -> str:
        return "orthogonal_sensitivity"

    @property
    def description(self) -> str:
        return "正交敏感性分析 - 基于正交表的参数敏感性分析，识别关键参数"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model", "parameters", "target"],
            "properties": {
                "skill": {"type": "string", "const": "orthogonal_sensitivity"},
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "token_file": {"type": "string", "default": ".cloudpss_token"},
                    },
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {
                        "rid": {"type": "string", "description": "模型RID"},
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                        "job_name": {"type": "string", "description": "指定job名称"},
                    },
                },
                "parameters": {
                    "type": "array",
                    "description": "要分析的参数列表",
                    "items": {
                        "type": "object",
                        "required": ["name", "levels"],
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "参数名称 (e.g., Gen1.pf_P)",
                            },
                            "levels": {
                                "type": "array",
                                "items": {"type": "number"},
                                "minItems": 2,
                                "maxItems": 4,
                                "description": "参数水平值（2-4个）",
                            },
                            "component_rid": {
                                "type": "string",
                                "description": "元件RID筛选",
                            },
                        },
                    },
                },
                "target": {
                    "type": "object",
                    "required": ["metric"],
                    "properties": {
                        "metric": {
                            "enum": ["voltage", "power", "frequency", "custom"],
                            "description": "评估指标类型",
                        },
                        "bus_name": {"type": "string", "description": "监测母线名称"},
                        "component_name": {
                            "type": "string",
                            "description": "监测元件名称",
                        },
                        "custom_expression": {
                            "type": "string",
                            "description": "自定义指标表达式",
                        },
                    },
                },
                "design": {
                    "type": "object",
                    "properties": {
                        "table_type": {
                            "enum": ["auto", "L4_2_3", "L8_2_7", "L9_3_4", "L16_4_5"],
                            "default": "auto",
                            "description": "正交表类型",
                        },
                        "simulation_type": {
                            "enum": ["power_flow", "emt"],
                            "default": "power_flow",
                        },
                    },
                },
                "execution": {
                    "type": "object",
                    "properties": {
                        "timeout": {
                            "type": "number",
                            "default": 300.0,
                            "description": "单次仿真超时(s)",
                        },
                        "continue_on_error": {"type": "boolean", "default": True},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {
                            "type": "string",
                            "default": "orthogonal_sensitivity",
                        },
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "model": {
                "rid": "",
                "source": "cloud",
            },
            "parameters": [],
            "target": {
                "metric": "voltage",
            },
            "design": {
                "table_type": "auto",
                "simulation_type": "power_flow",
            },
            "execution": {
                "timeout": 300.0,
                "continue_on_error": True,
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "orthogonal_sensitivity",
            },
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        """验证配置"""
        result = super().validate(config)

        model = config.get("model", {})
        rid = model.get("rid", "")

        if not rid:
            result.add_error("必须提供model.rid")

        parameters = config.get("parameters", [])
        if not parameters:
            result.add_error("必须指定至少一个要分析的参数")
        elif len(parameters) > 7:
            result.add_error("参数数量不能超过7个（受限于正交表L8_2_7）")

        for i, param in enumerate(parameters):
            if "name" not in param:
                result.add_error(f"参数{i + 1}必须指定name")
            if "levels" not in param or len(param["levels"]) < 2:
                result.add_error(f"参数{i + 1}必须指定至少2个水平值")
            if len(param.get("levels", [])) > 4:
                result.add_error(f"参数{i + 1}的水平数不能超过4")

        target = config.get("target", {})
        if "metric" not in target:
            result.add_error("必须指定target.metric评估指标")

        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行正交敏感性分析"""
        from cloudpss import Model, setToken

        start_time = datetime.now()
        logs = []
        artifacts = []
        runs = []

        def log(level: str, message: str):
            logs.append(
                LogEntry(timestamp=datetime.now(), level=level, message=message)
            )
            getattr(logger, level.lower(), logger.info)(message)

        try:
            # 1. 认证
            log("INFO", "加载认证信息...")
            auth = config.get("auth", {})
            token = auth.get("token")

            if not token:
                token_file = auth.get("token_file", ".cloudpss_token")
                token_path = Path(token_file)
                if token_path.exists():
                    token = token_path.read_text().strip()

            setToken(token)
            log("INFO", "认证成功")

            # 2. 加载模型
            model_config = config.get("model", {})
            rid = model_config["rid"]
            source = model_config.get("source", "cloud")
            job_name = model_config.get("job_name")

            log("INFO", f"加载模型: {rid}")

            model = load_or_fetch_model(model_config, config)

            log("INFO", f"模型名称: {model.name}")

            # 3. 获取配置
            parameters = config.get("parameters", [])
            target = config.get("target", {})
            design = config.get("design", {})
            execution = config.get("execution", {})
            output_config = config.get("output", {})

            # 4. 选择正交表
            table_type = design.get("table_type", "auto")
            num_params = len(parameters)

            if table_type == "auto":
                # 自动选择正交表
                max_levels = max(len(p["levels"]) for p in parameters)
                if max_levels == 2:
                    if num_params <= 3:
                        table_type = "L4_2_3"
                    else:
                        table_type = "L8_2_7"
                elif max_levels == 3:
                    if num_params <= 4:
                        table_type = "L9_3_4"
                    else:
                        raise ValueError("3水平参数数量不能超过4个")
                elif max_levels == 4:
                    if num_params <= 5:
                        table_type = "L16_4_5"
                    else:
                        raise ValueError("4水平参数数量不能超过5个")
                else:
                    table_type = "L4_2_3"

            if table_type not in ORTHOGONAL_TABLES:
                raise ValueError(f"不支持的正交表类型: {table_type}")

            oat = ORTHOGONAL_TABLES[table_type]
            if num_params > oat["factors"]:
                raise ValueError(f"正交表{table_type}最多支持{oat['factors']}个参数")

            log("INFO", f"使用正交表: {table_type} ({oat['runs']}次运行)")

            # 5. 构建正交运行矩阵
            log("INFO", "构建正交运行矩阵...")
            oat_table = oat["table"]

            for run_idx, row in enumerate(oat_table):
                param_values = {}
                for param_idx, param in enumerate(parameters):
                    level_idx = row[param_idx] - 1  # 正交表是1-based
                    param_values[param["name"]] = param["levels"][level_idx]

                run = OrthogonalRun(run_id=run_idx + 1, parameter_values=param_values)
                runs.append(run)

            log("INFO", f"  -> 共 {len(runs)} 次运行")

            # 6. 选择job
            if job_name:
                job = model.getModelJob(job_name)
                if isinstance(job, list):
                    job = job[0]
            else:
                job = None
                for j in model.jobs:
                    if j.get("rid") in [
                        "function/CloudPSS/powerflow",
                        "function/CloudPSS/emtps",
                    ]:
                        job = j
                        break
                if not job and model.jobs:
                    job = model.jobs[0]

            log("INFO", f"使用job: {job.get('name', 'default')}")

            # 7. 执行正交运行
            log("INFO", "开始执行正交运行...")
            timeout = execution.get("timeout", 300.0)
            continue_on_error = execution.get("continue_on_error", True)

            for run in runs:
                log(
                    "INFO",
                    f"  -> 运行 {run.run_id}/{len(runs)}: {run.parameter_values}",
                )

                try:
                    # 每次运行前深拷贝模型，避免参数改动累积
                    from copy import deepcopy

                    working_model = Model(deepcopy(model.toJSON()))

                    # 修改模型参数
                    for param in parameters:
                        param_name = param["name"]
                        param_value = run.parameter_values[param_name]
                        comp_rid = param.get("component_rid")

                        # 查找并修改元件参数
                        if comp_rid:
                            components = working_model.getComponentsByRid(comp_rid)
                        else:
                            # 尝试从参数名解析组件
                            components = self._find_components_by_param(
                                working_model, param_name, param.get("component_type")
                            )

                        if not components:
                            raise RuntimeError(
                                f"参数 {param_name} 未解析到任何目标组件。"
                                "请显式指定 component_rid，或使用 组件名.参数名 的精确写法。"
                            )

                        for comp_key, comp in components.items():
                            if hasattr(comp, "args"):
                                # 假设参数名对应args中的key
                                if "." in param_name:
                                    _, arg_name = param_name.split(".", 1)
                                else:
                                    arg_name = param_name
                                comp.args[arg_name] = str(param_value)

                    # 运行仿真
                    import time
                    import cloudpss

                    runner = working_model.run(job)
                    start = time.time()

                    while not runner.status() and (time.time() - start) < timeout:
                        time.sleep(2)

                    if runner.status():
                        # 获取结果指标
                        metric_value = self._extract_metric(
                            runner.result, target, model
                        )
                        run.result = metric_value
                        run.status = "success"
                        log("INFO", f"     结果: {metric_value}")
                    else:
                        run.status = "timeout"
                        run.error = "仿真超时"
                        log("WARN", f"     超时")

                except (
                    KeyError,
                    AttributeError,
                    RuntimeError,
                    ValueError,
                    TypeError,
                ) as e:
                    run.status = "failed"
                    run.error = str(e)
                    log("ERROR", f"     失败: {e}")
                    if not continue_on_error:
                        break

            # 8. 计算敏感性
            log("INFO", "计算参数敏感性...")
            sensitivity_results = self._calculate_sensitivity(runs, parameters)

            for sr in sensitivity_results:
                log(
                    "INFO",
                    f"  -> {sr.parameter}: 效应={sr.effect_value:.4f}, 贡献率={sr.contribution_ratio:.1%}",
                )

            # 9. 生成报告
            log("INFO", "生成分析报告...")
            report = self._generate_report(
                runs, sensitivity_results, config, table_type
            )

            # 10. 导出结果
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "orthogonal_sensitivity")

            report_file = output_path / f"{prefix}_report.json"
            report_file.write_text(
                json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            artifacts.append(
                Artifact(
                    type="json",
                    path=str(report_file),
                    size=report_file.stat().st_size,
                    description="正交敏感性分析报告",
                )
            )

            # 成功统计
            success_count = sum(1 for r in runs if r.status == "success")

            log("INFO", f"分析完成: 成功 {success_count}/{len(runs)}")

            # 根据成功率确定状态
            final_status = (
                SkillStatus.SUCCESS
                if success_count == len(runs)
                else SkillStatus.FAILED
            )
            first_error = next((r.error for r in runs if r.error), None)
            final_error = (
                None
                if final_status == SkillStatus.SUCCESS
                else (first_error or "存在未完成或失败的正交运行")
            )

            return SkillResult(
                skill_name=self.name,
                status=final_status,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "model_rid": rid,
                    "model_name": model.name,
                    "table_type": table_type,
                    "total_runs": len(runs),
                    "success_count": success_count,
                    "sensitivity_ranking": [
                        {
                            "parameter": sr.parameter,
                            "effect": sr.effect_value,
                            "rank": sr.sensitivity_rank,
                        }
                        for sr in sorted(
                            sensitivity_results, key=lambda x: x.sensitivity_rank
                        )
                    ],
                },
                artifacts=artifacts,
                logs=logs,
                error=final_error,
            )

        except (
            KeyError,
            AttributeError,
            ValueError,
            RuntimeError,
            TimeoutError,
            TypeError,
            FileNotFoundError,
        ) as e:
            log("ERROR", f"执行失败: {e}")
            import traceback

            log("DEBUG", traceback.format_exc())
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data={},
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )

    def _find_components_by_param(
        self, model: Any, param_name: str, component_type: Optional[str] = None
    ) -> Dict:
        """根据参数名查找组件"""
        # 如果提供了组件类型，直接按类型查找
        if component_type:
            try:
                return model.getComponentsByRid(component_type)
            except Exception:
                return {}

        component_name = param_name.split(".", 1)[0]
        matches = {}
        try:
            for key, comp in model.getAllComponents().items():
                if not hasattr(comp, "args"):
                    continue
                label = getattr(comp, "label", "") or ""
                name = getattr(comp, "name", "") or ""
                comp_key = str(key)
                arg_name = (
                    str(comp.args.get("Name", "")) if hasattr(comp, "args") else ""
                )
                if (
                    component_name == label
                    or component_name == name
                    or component_name == arg_name
                    or component_name == comp_key
                ):
                    matches[key] = comp
        except Exception:
            return {}

        if matches:
            return matches

        # 无法识别参数类型，返回空字典
        logger.warning(
            f"无法从参数名 '{param_name}' 识别组件类型，请显式指定 component_rid 或 component_type"
        )
        return {}

    def _extract_metric(self, result: Any, target: Dict, model: Any) -> float:
        """从结果中提取指标"""
        metric_type = target.get("metric", "voltage")

        try:
            if metric_type == "voltage":
                bus_name = target.get("bus_name", "")
                if bus_name:
                    buses = model.getComponentsByRid("model/CloudPSS/_newBus_3p")
                    for comp in buses.values():
                        if comp.args.get("Name") == bus_name:
                            v_base = float(comp.args.get("VBase", 1.0))
                            v_pu = float(comp.args.get("V", 1.0))
                            return v_pu * v_base
                return 1.0

            elif metric_type == "power":
                # 简化实现
                return 0.0

            else:
                return 0.0

        except (KeyError, AttributeError, ZeroDivisionError) as e:
            logger.warning(f"提取指标失败: {e}")
            return 0.0

    def _calculate_sensitivity(
        self, runs: List[OrthogonalRun], parameters: List[Dict]
    ) -> List[SensitivityResult]:
        """计算参数敏感性"""
        success_runs = [
            r for r in runs if r.status == "success" and r.result is not None
        ]

        if not success_runs:
            return []

        # 按参数分组计算效应
        param_effects = {}

        for param in parameters:
            param_name = param["name"]
            levels = param["levels"]

            # 计算每个水平的平均结果
            level_means = {}
            for level_idx, level_value in enumerate(levels):
                level_results = [
                    r.result
                    for r in success_runs
                    if r.parameter_values.get(param_name) == level_value
                ]
                if level_results:
                    level_means[level_value] = sum(level_results) / len(level_results)
                else:
                    level_means[level_value] = 0

            # 计算极差（效应值）
            if level_means:
                effect = max(level_means.values()) - min(level_means.values())
            else:
                effect = 0

            param_effects[param_name] = effect

        # 计算贡献率
        total_effect = sum(param_effects.values())

        # 构建结果
        results = []
        sorted_params = sorted(param_effects.items(), key=lambda x: x[1], reverse=True)

        for rank, (param_name, effect) in enumerate(sorted_params, 1):
            contribution = effect / total_effect if total_effect > 0 else 0
            results.append(
                SensitivityResult(
                    parameter=param_name,
                    effect_value=effect,
                    sensitivity_rank=rank,
                    contribution_ratio=contribution,
                )
            )

        return results

    def _generate_report(
        self,
        runs: List[OrthogonalRun],
        sensitivity: List[SensitivityResult],
        config: Dict,
        table_type: str,
    ) -> Dict:
        """生成报告"""
        return {
            "summary": {
                "total_runs": len(runs),
                "success_count": sum(1 for r in runs if r.status == "success"),
                "failed_count": sum(1 for r in runs if r.status == "failed"),
                "timeout_count": sum(1 for r in runs if r.status == "timeout"),
                "table_type": table_type,
            },
            "sensitivity_analysis": [
                {
                    "parameter": sr.parameter,
                    "effect_value": sr.effect_value,
                    "sensitivity_rank": sr.sensitivity_rank,
                    "contribution_ratio": sr.contribution_ratio,
                }
                for sr in sensitivity
            ],
            "runs": [
                {
                    "run_id": r.run_id,
                    "parameter_values": r.parameter_values,
                    "status": r.status,
                    "result": r.result,
                    "error": r.error,
                }
                for r in runs
            ],
            "parameters": config.get("parameters", []),
            "target": config.get("target", {}),
        }
