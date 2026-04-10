"""
VSI Weak Bus Analysis Skill

VSI弱母线分析 - 基于动态无功注入的电压稳定敏感度分析

核心流程：
1. 为每个母线添加动态无功注入源（shuntLC + 断路器）
2. 配置时序信号，依次在各母线注入无功
3. 运行EMT仿真
4. 从结果计算VSI（Voltage Stability Index）
5. 识别弱母线（VSI高的母线电压稳定性差）

参考自：PSA Skills S05 - vsi-weak-bus-analysis
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from cloudpss import Model

from cloudpss_skills.core import (
    Artifact,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    register,
)
from cloudpss_skills.core.auth_utils import fetch_model_by_rid, run_emt
from cloudpss_skills.core.emt_measurement_core import (
    add_bus_voltage_measurements,
    compute_vsi_from_voltage_channels,
)
from cloudpss_skills.core import sync_support_core as sync_core
from cloudpss_skills.core.utils import (
    fetch_job_with_result,
    get_bus_components,
    clean_component_key,
)

logger = logging.getLogger(__name__)


def _matches_bus_identifier(candidate: str, target: str) -> bool:
    return sync_core.matches_bus_identifier(candidate, target)


def _as_numeric(value: Any, default: float = 0.0) -> float:
    return sync_core.as_numeric(value, default=default)


@register
class VSIWeakBusSkill(SkillBase):
    """VSI弱母线分析技能"""

    @property
    def name(self) -> str:
        return "vsi_weak_bus"

    @property
    def description(self) -> str:
        return "VSI弱母线分析 - 通过动态无功注入测试识别电压稳定性薄弱母线"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["model"],
            "properties": {
                "auth": {
                    "type": "object",
                    "properties": {
                        "token_file": {"type": "string", "default": ".cloudpss_token"}
                    },
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {
                        "rid": {"type": "string", "description": "模型RID"},
                        "source": {
                            "type": "string",
                            "enum": ["cloud", "local"],
                            "default": "cloud",
                        },
                    },
                },
                "vsi_setup": {
                    "type": "object",
                    "description": "VSI测试配置",
                    "properties": {
                        "bus_filter": {
                            "type": "object",
                            "properties": {
                                "v_min": {
                                    "type": "number",
                                    "default": 0.6,
                                    "description": "母线最小电压筛选(kV)",
                                },
                                "v_max": {
                                    "type": "number",
                                    "default": 300,
                                    "description": "母线最大电压筛选(kV)",
                                },
                                "name_keywords": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "母线名称关键字筛选",
                                },
                            },
                        },
                        "injection": {
                            "type": "object",
                            "properties": {
                                "v_base": {
                                    "type": "number",
                                    "default": 220,
                                    "description": "基准电压(kV)",
                                },
                                "q_base": {
                                    "type": "number",
                                    "default": 100,
                                    "description": "注入无功(MVar)",
                                },
                                "start_time": {
                                    "type": "number",
                                    "default": 8.0,
                                    "description": "开始时间(s)",
                                },
                                "interval": {
                                    "type": "number",
                                    "default": 1.5,
                                    "description": "每个母线测试时长(s)",
                                },
                                "duration": {
                                    "type": "number",
                                    "default": 0.5,
                                    "description": "无功注入持续时间(s)",
                                },
                            },
                        },
                        "simulation": {
                            "type": "object",
                            "properties": {
                                "step_time": {
                                    "type": "number",
                                    "default": 0.0001,
                                    "description": "仿真步长(s)",
                                },
                                "freq": {
                                    "type": "number",
                                    "default": 100,
                                    "description": "输出频率(Hz)",
                                },
                            },
                        },
                    },
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "vsi_threshold": {
                            "type": "number",
                            "default": 0.01,
                            "description": "弱母线VSI阈值",
                        },
                        "top_n": {
                            "type": "integer",
                            "default": 10,
                            "description": "输出前N个弱母线",
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {
                            "type": "string",
                            "enum": ["json", "csv"],
                            "default": "json",
                        },
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "vsi_weak_bus"},
                    },
                },
            },
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        """验证配置"""
        errors = []

        if "model" not in config:
            errors.append("必须指定model配置")
        elif "rid" not in config["model"]:
            errors.append("必须指定model.rid")

        if errors:
            return ValidationResult(valid=False, errors=errors)

        return ValidationResult(valid=True)

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行VSI弱母线分析"""
        import os
        from cloudpss import setToken

        start_time = datetime.now()
        logs = []
        artifacts = []

        try:
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

            if not token:
                # 根据服务器选择 token 文件
                if server == "internal":
                    token_files = [".cloudpss_token_internal", ".cloudpss_token"]
                else:
                    token_files = [".cloudpss_token"]
                for token_file in token_files:
                    token_path = Path(token_file)
                    if token_path.exists():
                        token = token_path.read_text().strip()
                        break

            if not token:
                raise FileNotFoundError("未找到CloudPSS token")
            setToken(token)

            # 1. 获取模型
            model_rid = config["model"]["rid"]
            logger.info(f"VSI弱母线分析开始 - 模型: {model_rid}")
            logs.append(
                LogEntry(
                    timestamp=datetime.now(),
                    level="INFO",
                    message=f"加载模型: {model_rid}",
                )
            )

            model = fetch_model_by_rid(model_rid, config)

            # 2. 筛选测试母线
            vsi_config = config.get("vsi_setup", {})
            bus_filter = vsi_config.get("bus_filter", {})

            test_buses = self._select_test_buses(
                model,
                v_min=bus_filter.get("v_min", 0.6),
                v_max=bus_filter.get("v_max", 300),
                name_keywords=bus_filter.get("name_keywords"),
            )

            if not test_buses:
                return SkillResult(
                    skill_name=self.name,
                    status=SkillStatus.FAILED,
                    start_time=start_time,
                    end_time=datetime.now(),
                    data={},
                    artifacts=artifacts,
                    logs=logs
                    + [
                        LogEntry(
                            timestamp=datetime.now(),
                            level="ERROR",
                            message="未找到符合条件的测试母线",
                        )
                    ],
                    metrics={"duration": (datetime.now() - start_time).total_seconds()},
                )

            logger.info(f"选定 {len(test_buses)} 个测试母线")
            logs.append(
                LogEntry(
                    timestamp=datetime.now(),
                    level="INFO",
                    message=f"选定 {len(test_buses)} 个测试母线",
                )
            )

            # 3. 添加VSI无功源
            injection_config = vsi_config.get("injection", {})
            vsi_q_keys = self._add_vsi_q_sources(
                model,
                test_buses,
                v_base=injection_config.get("v_base", 220),
                q_base=injection_config.get("q_base", 100),
                start_time=injection_config.get("start_time", 8.0),
                interval=injection_config.get("interval", 1.5),
                duration=injection_config.get("duration", 0.5),
            )

            logger.info(f"添加了 {len(vsi_q_keys)} 个VSI无功源")
            logs.append(
                LogEntry(
                    timestamp=datetime.now(),
                    level="INFO",
                    message=f"添加了 {len(vsi_q_keys)} 个VSI无功源",
                )
            )
            if not vsi_q_keys:
                raise RuntimeError("未成功添加任何VSI无功源，无法开展有效弱母线分析")

            # 4. 添加量测
            sim_config = vsi_config.get("simulation", {})
            measure_indices = self._add_vsi_measures(
                model, test_buses, freq=sim_config.get("freq", 100)
            )

            measurement_channels = measure_indices["voltage_channels"]

            logger.info(f"量测通道: 电压={len(measurement_channels)} 个")
            logs.append(
                LogEntry(
                    timestamp=datetime.now(),
                    level="INFO",
                    message=f"量测通道: 电压={len(measurement_channels)} 个",
                )
            )

            # 5. 设置仿真参数
            end_time = injection_config.get("start_time", 8.0) + len(
                test_buses
            ) * injection_config.get("interval", 1.5)

            logger.info(
                f"仿真参数: 步长={sim_config.get('step_time', 0.0001)}, 结束时间={end_time}"
            )

            # 6. 运行EMT仿真
            logger.info("开始EMT仿真...")
            logs.append(
                LogEntry(timestamp=datetime.now(), level="INFO", message="开始EMT仿真")
            )

            try:
                # 使用SDK支持的参数调用runEMT
                job = run_emt(model, config)

                # 等待完成
                import time

                max_wait = 300
                waited = 0
                while job.status() == 0 and waited < max_wait:
                    time.sleep(2)
                    waited += 2

                if job.status() != 1:
                    return SkillResult(
                        skill_name=self.name,
                        status=SkillStatus.FAILED,
                        start_time=start_time,
                        end_time=datetime.now(),
                        data={},
                        artifacts=artifacts,
                        logs=logs
                        + [
                            LogEntry(
                                timestamp=datetime.now(),
                                level="ERROR",
                                message="EMT仿真失败或未在时间内完成",
                            )
                        ],
                        metrics={
                            "duration": (datetime.now() - start_time).total_seconds()
                        },
                    )

                _job, emt_result = fetch_job_with_result(job.id, config)
                if emt_result is None:
                    raise RuntimeError("EMT结果为空")
                logger.info("EMT仿真完成")
                logs.append(
                    LogEntry(
                        timestamp=datetime.now(), level="INFO", message="EMT仿真完成"
                    )
                )

            except (KeyError, AttributeError, ConnectionError, TypeError) as e:
                logger.error(f"EMT仿真失败: {e}")
                return SkillResult(
                    skill_name=self.name,
                    status=SkillStatus.FAILED,
                    start_time=start_time,
                    end_time=datetime.now(),
                    data={},
                    artifacts=artifacts,
                    logs=logs
                    + [
                        LogEntry(
                            timestamp=datetime.now(),
                            level="ERROR",
                            message=f"EMT仿真失败: {str(e)}",
                        )
                    ],
                    metrics={"duration": (datetime.now() - start_time).total_seconds()},
                )

            # 7. 计算VSI
            logger.info("开始计算VSI...")
            logs.append(
                LogEntry(timestamp=datetime.now(), level="INFO", message="开始计算VSI")
            )

            vsi_results = self._calculate_vsi(
                emt_result,
                test_buses,
                measurement_channels,
                injection_config.get("q_base", 100),
                injection_config.get("start_time", 8.0),
                injection_config.get("interval", 1.5),
                injection_config.get("duration", 0.5),
            )

            logger.info(f"VSI计算完成 - 母线数: {len(vsi_results['vsi_i'])}")
            logs.append(
                LogEntry(
                    timestamp=datetime.now(),
                    level="INFO",
                    message=f"VSI计算完成 - 母线数: {len(vsi_results['vsi_i'])}",
                )
            )
            if not vsi_results.get("vsi_i"):
                unsupported = vsi_results.get("unsupported_buses", [])
                raise RuntimeError(
                    "未能形成任何有效VSI结果；当前模型缺少可验证的电压/无功量测链路。"
                    + (
                        f" 未支持母线: {', '.join(unsupported[:5])}"
                        if unsupported
                        else ""
                    )
                )

            # 8. 识别弱母线
            analysis_config = config.get("analysis", {})
            weak_buses = self._identify_weak_buses(
                vsi_results,
                threshold=analysis_config.get("vsi_threshold", 0.01),
                top_n=analysis_config.get("top_n", 10),
            )

            # 9. 生成输出
            output_config = config.get("output", {})
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "vsi_weak_bus")

            result_data = {
                "model_rid": model_rid,
                "test_bus_count": len(test_buses),
                "vsi_results": vsi_results,
                "weak_buses": weak_buses,
                "unsupported_buses": vsi_results.get("unsupported_buses", []),
                "summary": {
                    "total_buses": len(test_buses),
                    "weak_bus_count": len(weak_buses),
                    "max_vsi": max(vsi_results["vsi_i"].values())
                    if vsi_results["vsi_i"]
                    else 0,
                    "min_vsi": min(vsi_results["vsi_i"].values())
                    if vsi_results["vsi_i"]
                    else 0,
                    "avg_vsi": sum(vsi_results["vsi_i"].values())
                    / len(vsi_results["vsi_i"])
                    if vsi_results["vsi_i"]
                    else 0,
                },
            }

            # 保存JSON结果
            json_path = output_path / f"{prefix}_result.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)

            artifacts.append(
                Artifact(
                    type="json",
                    path=str(json_path),
                    size=json_path.stat().st_size,
                    description="VSI分析结果",
                )
            )

            # 保存CSV结果
            csv_path = output_path / f"{prefix}_result.csv"
            self._save_csv_results(vsi_results, weak_buses, csv_path)

            artifacts.append(
                Artifact(
                    type="csv",
                    path=str(csv_path),
                    size=csv_path.stat().st_size,
                    description="VSI指标汇总",
                )
            )

            # 生成Markdown报告
            report_path = output_path / f"{prefix}_report.md"
            self._generate_report(result_data, report_path)

            artifacts.append(
                Artifact(
                    type="markdown",
                    path=str(report_path),
                    size=report_path.stat().st_size,
                    description="VSI分析报告",
                )
            )

            duration = (datetime.now() - start_time).total_seconds()
            logs.append(
                LogEntry(
                    timestamp=datetime.now(),
                    level="INFO",
                    message=f"VSI弱母线分析完成，耗时 {duration:.2f}s",
                )
            )

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
                metrics={
                    "duration": duration,
                    "bus_count": len(test_buses),
                    "weak_count": len(weak_buses),
                },
            )

        except (
            KeyError,
            AttributeError,
            ConnectionError,
            FileNotFoundError,
            RuntimeError,
            ValueError,
            TypeError,
        ) as e:
            logger.error(f"VSI弱母线分析失败: {e}", exc_info=True)
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data={},
                artifacts=artifacts,
                logs=logs
                + [
                    LogEntry(
                        timestamp=datetime.now(),
                        level="ERROR",
                        message=f"分析失败: {str(e)}",
                    )
                ],
                error=str(e),
                metrics={"duration": (datetime.now() - start_time).total_seconds()},
            )

    def _select_test_buses(
        self,
        model: Model,
        v_min: float = 0.6,
        v_max: float = 300,
        name_keywords: Optional[List[str]] = None,
    ) -> List[Dict]:
        """筛选测试母线"""
        buses = get_bus_components(model)
        test_buses = []

        for key, data in buses.items():
            try:
                # 获取母线电压
                v_base = sync_core.resolve_model_numeric(
                    model, data.get("args", {}).get("V", 1.0), 1.0
                )
                v_base_kv = sync_core.resolve_model_numeric(
                    model, data.get("args", {}).get("VBase", 1.0), 1.0
                )
                bus_voltage = v_base * v_base_kv

                # 电压筛选
                if not (v_min <= bus_voltage <= v_max):
                    continue

                # 名称筛选
                label = data.get("label", "")
                bus_name = str(data.get("args", {}).get("Name", ""))
                if name_keywords:
                    if not any(
                        _matches_bus_identifier(label, kw)
                        or _matches_bus_identifier(bus_name, kw)
                        for kw in name_keywords
                    ):
                        continue

                test_buses.append(
                    {
                        "key": key,
                        "label": label,
                        "name": bus_name,
                        "voltage": bus_voltage,
                        "v_base": v_base,
                        "v_base_kv": v_base_kv,
                    }
                )

            except (KeyError, AttributeError) as e:
                logger.warning(f"处理母线 {key} 失败: {e}")
                continue

        # 按label排序
        test_buses.sort(key=lambda x: x["label"])

        return test_buses

    def _add_vsi_q_sources(
        self,
        model: Model,
        test_buses: List[Dict],
        v_base: float = 220,
        q_base: float = 100,
        start_time: float = 8.0,
        interval: float = 1.5,
        duration: float = 0.5,
    ) -> List[str]:
        """添加VSI动态无功源"""
        vsi_q_keys = []
        canvas_id = "canvas_VSI_Analysis"

        # 创建画布
        try:
            model.createCanvas(canvas_id, "VSI动态无功分析")
        except Exception as e:
            logger.warning(f"画布 {canvas_id} 可能已存在")

        for k, bus in enumerate(test_buses):
            bus_key = bus["key"]
            bus_voltage = bus["voltage"]

            # 添加shuntLC（无功注入源）
            shunt_id = f"VSI_ShuntLC_{k}"
            shunt_name = f"VSI_无功源_{k}"

            shunt_args = {
                "Name": shunt_name,
                "Dim": "3",
                "v": str(bus_voltage),
                "s": str(-q_base),  # 负号表示注入无功
                "Q": f"#VSI_DQ_{k}",  # 控制信号
            }

            shunt_pins = {"0": f"VSI_Bus_{k}"}

            try:
                component = model.addComponent(
                    "model/CloudPSS/_newShuntLC_3p", shunt_id, shunt_args, shunt_pins
                )
                vsi_q_keys.append(component.id)
            except (AttributeError, TypeError) as e:
                logger.warning(f"添加无功源 {shunt_id} 失败: {e}")
                continue

            # 添加断路器
            breaker_id = f"VSI_Breaker_{k}"
            breaker_name = f"VSI_断路器_{k}"
            ctrl_signal = f"@VSI_Breaker_Ctrl_{k}"

            breaker_args = {
                "Name": breaker_name,
                "ctrlsignal": ctrl_signal,
                "Init": "0",  # 初始断开
            }

            # 获取母线引脚
            try:
                bus_component = model.getComponentByKey(bus_key)
                bus_pin = bus_component.pins.get("0", bus_key)
            except Exception as e:
                bus_pin = bus_key

            breaker_pins = {"0": bus_pin, "1": f"VSI_Bus_{k}"}

            try:
                model.addComponent(
                    "model/CloudPSS/_newBreaker_3p",
                    breaker_id,
                    breaker_args,
                    breaker_pins,
                )
            except (AttributeError, TypeError) as e:
                logger.warning(f"添加断路器 {breaker_id} 失败: {e}")

            # 添加开关信号（步进信号）
            signal_name = f"VSI_Signal_{k}"
            t1 = start_time + k * interval
            t2 = t1 + duration

            signal_args = {
                "Name": signal_name,
                "INIT": "0",
                "Drop": "1",
                "T1": str(t1),
                "T2": str(t2),
            }

            signal_pins = {"0": ctrl_signal}

            try:
                model.addComponent(
                    "model/CloudPSS/_newStepGen",
                    f"VSI_Step_{k}",
                    signal_args,
                    signal_pins,
                )
            except (AttributeError, TypeError) as e:
                logger.warning(f"添加信号源 {signal_name} 失败: {e}")

        return vsi_q_keys

    def _add_vsi_measures(
        self, model: Model, test_buses: List[Dict[str, Any]], freq: float = 100
    ) -> Dict[str, Any]:
        """添加VSI量测"""
        measurement_channels = add_bus_voltage_measurements(
            model,
            buses=test_buses,
            sampling_freq=int(freq),
            signal_name_builder=lambda bus: f"#{bus['name'] or bus['label']}_vsi",
            channel_name_builder=lambda bus: f"vsi_v_{bus['name'] or bus['label']}",
            meter_label_builder=lambda bus: f"VSI_Meter_{bus['label']}",
            channel_label_builder=lambda bus: f"VSI_Channel_{bus['label']}",
        )
        return {"voltage_channels": measurement_channels}

    def _calculate_vsi(
        self,
        result: Any,
        test_buses: List[Dict],
        measurement_channels: List[Dict[str, Any]],
        q_base: float,
        start_time: float,
        interval: float,
        duration: float,
    ) -> Dict[str, Any]:
        """计算VSI指标"""
        try:
            return compute_vsi_from_voltage_channels(
                result,
                test_buses=test_buses,
                measurement_channels=measurement_channels,
                q_base=q_base,
                start_time=start_time,
                interval=interval,
                duration=duration,
            )

        except (KeyError, AttributeError, ZeroDivisionError) as e:
            logger.error(f"计算VSI失败: {e}")
            return {
                "vsi_i": {},
                "vsi_ij": {},
                "unsupported_buses": [b["label"] for b in test_buses],
            }

    def _identify_weak_buses(
        self, vsi_results: Dict[str, Any], threshold: float = 0.01, top_n: int = 10
    ) -> List[Dict]:
        """识别弱母线"""
        vsi_i = vsi_results.get("vsi_i", {})

        # 按VSI排序（VSI越高越弱）
        sorted_buses = sorted(vsi_i.items(), key=lambda x: x[1], reverse=True)

        weak_buses = []
        for bus_label, vsi in sorted_buses[:top_n]:
            if vsi >= threshold:
                weak_buses.append({"label": bus_label, "vsi": vsi, "is_weak": True})

        return weak_buses

    def _save_csv_results(
        self, vsi_results: Dict[str, Any], weak_buses: List[Dict], csv_path: Path
    ):
        """保存CSV结果"""
        import csv

        vsi_i = vsi_results.get("vsi_i", {})

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["母线名称", "VSI", "是否弱母线"])

            # 按VSI降序
            sorted_buses = sorted(vsi_i.items(), key=lambda x: x[1], reverse=True)
            weak_labels = {wb["label"] for wb in weak_buses}

            for label, vsi in sorted_buses:
                is_weak = "是" if label in weak_labels else "否"
                writer.writerow([label, f"{vsi:.6f}", is_weak])

    def _generate_report(self, result_data: Dict[str, Any], report_path: Path):
        """生成Markdown报告"""
        lines = [
            "# VSI弱母线分析报告",
            "",
            f"**模型**: {result_data['model_rid']}",
            f"**测试母线数**: {result_data['summary']['total_buses']}",
            f"**弱母线数**: {result_data['summary']['weak_bus_count']}",
            f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 摘要",
            "",
            f"- **总母线数**: {result_data['summary']['total_buses']}",
            f"- **弱母线数**: {result_data['summary']['weak_bus_count']}",
            f"- **VSI最大值**: {result_data['summary']['max_vsi']:.6f}",
            f"- **VSI最小值**: {result_data['summary']['min_vsi']:.6f}",
            f"- **VSI平均值**: {result_data['summary']['avg_vsi']:.6f}",
            "",
        ]

        # 弱母线列表
        weak_buses = result_data.get("weak_buses", [])
        if weak_buses:
            lines.extend(
                [
                    "## 弱母线列表 (Top {})".format(len(weak_buses)),
                    "",
                    "| 排名 | 母线名称 | VSI |",
                    "|------|----------|-----|",
                ]
            )

            for i, wb in enumerate(weak_buses, 1):
                lines.append(f"| {i} | {wb['label']} | {wb['vsi']:.6f} |")

            lines.append("")

        # VSI分布
        lines.extend(["## VSI指标分布", "", "| 母线名称 | VSI |", "|----------|-----|"])

        vsi_i = result_data.get("vsi_results", {}).get("vsi_i", {})
        for label, vsi in sorted(vsi_i.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"| {label} | {vsi:.6f} |")

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
