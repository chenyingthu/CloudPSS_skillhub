"""
Transient Stability Analysis Skill

暂态稳定性分析 - 基于EMT仿真的发电机稳定性评估
通过故障后转速/功角响应评估系统暂态稳定性
"""

import csv
import json
import logging
import math
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

from cloudpss_skills.core import (
    Artifact,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    register,
)
from cloudpss_skills.core.auth_utils import load_or_fetch_model, run_emt, setup_auth

logger = logging.getLogger(__name__)

FAULT_DEFINITION = "model/CloudPSS/_newFaultResistor_3p"


@register
class TransientStabilitySkill(SkillBase):
    """暂态稳定性分析技能"""

    @property
    def name(self) -> str:
        return "transient_stability"

    @property
    def description(self) -> str:
        return "暂态稳定性分析 - 基于EMT仿真的故障后发电机稳定性评估"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "transient_stability"},
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
                        "rid": {"type": "string"},
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                    },
                },
                "fault": {
                    "type": "object",
                    "required": ["location"],
                    "properties": {
                        "location": {"type": "string", "description": "故障位置母线ID"},
                        "fs": {"type": "number", "default": 2.5},
                        "fe_values": {
                            "type": "array",
                            "items": {"type": "number"},
                            "default": [2.7, 2.8, 2.9],
                            "description": "故障切除时间扫描值",
                        },
                        "chg": {"type": "number", "default": 0.01},
                    },
                },
                "generators": {
                    "type": "object",
                    "properties": {
                        "monitored": {
                            "type": "array",
                            "items": {"type": "string"},
                            "default": ["Gen1", "Gen2", "Gen3"],
                            "description": "监测的发电机名称列表",
                        },
                        "speed_channels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "default": ["#wr1", "#wr2", "#wr3"],
                            "description": "转速信号通道",
                        },
                        "power_channels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "default": ["#P1", "#P2", "#P3"],
                            "description": "有功功率信号通道",
                        },
                    },
                },
                "assessment": {
                    "type": "object",
                    "properties": {
                        "stable_criterion": {
                            "type": "string",
                            "enum": ["damped", "bounded"],
                            "default": "damped",
                        },
                        "max_speed_deviation": {"type": "number", "default": 0.5},
                        "analysis_window": {
                            "type": "array",
                            "items": {"type": "number"},
                            "default": [3.0, 8.0],
                        },
                        "settling_time_threshold": {"type": "number", "default": 0.02},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "transient_stability"},
                        "generate_report": {"type": "boolean", "default": True},
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE3", "source": "cloud"},
            "fault": {
                "location": "Bus7",
                "fs": 2.5,
                "fe_values": [2.7, 2.8, 2.9],
                "chg": 0.01,
            },
            "generators": {
                "monitored": ["Gen1", "Gen2", "Gen3"],
                "speed_channels": ["#wr1:0", "#wr2:0", "#wr3:0"],
                "power_channels": ["#P1:0", "#P2:0", "#P3:0"],
            },
            "assessment": {
                "stable_criterion": "damped",
                "max_speed_deviation": 0.5,
                "analysis_window": [3.0, 8.0],
                "settling_time_threshold": 0.02,
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "transient_stability",
                "generate_report": True,
            },
        }

    def run(self, config: Dict[str, Any]) -> SkillResult:
        from cloudpss import Model

        start_time = datetime.now()
        logs = []
        artifacts = []

        def log(level: str, message: str):
            logs.append(
                LogEntry(timestamp=datetime.now(), level=level, message=message)
            )
            getattr(logger, level.lower(), logger.info)(message)

        try:
            setup_auth(config)
            log("INFO", "加载模型...")

            model_config = config["model"]
            base_model = load_or_fetch_model(model_config, config)
            log("INFO", f"模型: {base_model.name}")

            fault_config = config["fault"]
            gen_config = config.get("generators", {})
            assessment_config = config.get("assessment", {})
            output_config = config.get("output", {})

            fe_values = fault_config["fe_values"]
            fs = fault_config.get("fs", 2.5)
            chg = fault_config.get("chg", 0.01)
            fault_location = fault_config["location"]

            monitored_gens = gen_config.get("monitored", ["Gen1", "Gen2", "Gen3"])
            speed_channels = gen_config.get(
                "speed_channels", ["#wr1:0", "#wr2:0", "#wr3:0"]
            )
            power_channels = gen_config.get(
                "power_channels", ["#P1:0", "#P2:0", "#P3:0"]
            )

            max_dev = assessment_config.get("max_speed_deviation", 0.5)
            analysis_window = assessment_config.get("analysis_window", [3.0, 8.0])
            settling_threshold = assessment_config.get("settling_time_threshold", 0.02)

            log("INFO", f"暂态稳定性分析: {len(fe_values)}个故障切除时间")
            log("INFO", f"监测发电机: {monitored_gens}")
            log("INFO", f"故障位置: {fault_location}")

            results = []
            for i, fe in enumerate(fe_values):
                log("INFO", f"[{i + 1}/{len(fe_values)}] 故障切除时间 fe={fe}s")
                working_model = Model(deepcopy(base_model.toJSON()))

                # 配置故障
                components = working_model.getAllComponents()
                fault = None
                for comp in components.values():
                    if getattr(comp, "definition", None) == FAULT_DEFINITION:
                        fault = comp
                        break

                if fault:
                    working_model.updateComponent(
                        fault.id,
                        args={
                            "fs": {"source": str(fs), "ɵexp": ""},
                            "fe": {"source": str(fe), "ɵexp": ""},
                            "chg": {"source": str(chg), "ɵexp": ""},
                        },
                    )
                    log("INFO", f"  故障配置: fs={fs}s, fe={fe}s, chg={chg}")

                # 运行EMT
                emt_result = run_emt(working_model, config)
                log("INFO", f"  Job ID: {emt_result.job.id}")

                result = emt_result.result

                # 提取稳定性指标
                stability_metrics = self._analyze_stability(
                    result,
                    speed_channels,
                    power_channels,
                    analysis_window,
                    settling_threshold,
                )

                case_result = {
                    "fe": fe,
                    "job_id": emt_result.job.id,
                    "stability": stability_metrics,
                }
                results.append(case_result)

                # 评估稳定性
                is_stable = self._assess_stability(stability_metrics, max_dev)
                status_str = "稳定" if is_stable else "不稳定/临界"
                log(
                    "INFO",
                    f"  -> 稳定性: {status_str}, 最大转速偏差: {stability_metrics.get('max_speed_deviation', 0):.4f}",
                )

            # 分析趋势
            stability_trend = self._analyze_stability_trend(results)

            # 导出结果
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "transient_stability")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            result_data = {
                "model": base_model.name,
                "model_rid": base_model.rid,
                "fault_location": fault_location,
                "stability_trend": stability_trend,
                "results": results,
            }

            # JSON输出
            json_path = output_path / f"{prefix}_{timestamp}.json"
            with open(json_path, "w") as f:
                json.dump(result_data, f, indent=2)
            artifacts.append(
                Artifact(
                    type="json",
                    path=str(json_path),
                    size=json_path.stat().st_size,
                    description="暂态稳定性分析结果",
                )
            )

            # CSV输出
            csv_path = output_path / f"{prefix}_{timestamp}.csv"
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "fe",
                        "is_stable",
                        "max_speed_dev",
                        "settling_time",
                        "damping_ratio",
                        "oscillation_freq",
                    ]
                )
                for r in results:
                    m = r["stability"]
                    writer.writerow(
                        [
                            r["fe"],
                            m.get("is_stable", False),
                            f"{m.get('max_speed_deviation', 0):.4f}",
                            f"{m.get('settling_time', 0):.2f}",
                            f"{m.get('damping_ratio', 0):.4f}",
                            f"{m.get('oscillation_freq', 0):.2f}",
                        ]
                    )
            artifacts.append(
                Artifact(
                    type="csv",
                    path=str(csv_path),
                    size=csv_path.stat().st_size,
                    description="暂态稳定性CSV",
                )
            )

            # 生成报告
            if output_config.get("generate_report", True):
                report_path = output_path / f"{prefix}_report_{timestamp}.md"
                self._generate_report(result_data, report_path)
                artifacts.append(
                    Artifact(
                        type="markdown",
                        path=str(report_path),
                        size=report_path.stat().st_size,
                        description="暂态稳定性分析报告",
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
            )

        except (
            KeyError,
            AttributeError,
            ZeroDivisionError,
            RuntimeError,
            FileNotFoundError,
            ValueError,
            TypeError,
        ) as e:
            log("ERROR", f"执行失败: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "success": False,
                    "error": str(e),
                    "stage": "transient_stability",
                },
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )

    def _analyze_stability(
        self,
        result,
        speed_channels,
        power_channels,
        analysis_window,
        settling_threshold,
    ):
        """分析稳定性指标"""
        metrics = {
            "max_speed_deviation": 0,
            "settling_time": 0,
            "damping_ratio": 0,
            "oscillation_freq": 0,
            "is_stable": True,
        }

        for plot_idx in range(len(result.getPlots())):
            channel_names = result.getPlotChannelNames(plot_idx)

            # 尝试两种方式获取速度数据：1) 直接通道名 2) 分组通道
            speed_data_list = []

            # 方式1: 直接通道名 (IEEE3格式: #wr1:0, #wr2:0...)
            for speed_ch in speed_channels:
                if speed_ch in channel_names:
                    trace = result.getPlotChannelData(plot_idx, speed_ch)
                    if trace and trace.get("y"):
                        speed_data_list.append(
                            (speed_ch, trace.get("x", []), trace.get("y", []))
                        )

            # 方式3: 自动检测发电机转速通道 (IEEE39格式: #Gen31.wr:0, #Gen32.wr:0...)
            if not speed_data_list:
                for ch in channel_names:
                    if (
                        ".wr:" in ch
                        or ch.endswith(".wr")
                        or ".omega:" in ch
                        or ".speed:" in ch
                    ):
                        trace = result.getPlotChannelData(plot_idx, ch)
                        if trace and trace.get("y"):
                            speed_data_list.append(
                                (ch, trace.get("x", []), trace.get("y", []))
                            )

            for speed_ch, xs, ys in speed_data_list:
                if not xs or not ys:
                    continue

                # 分析窗口内的数据
                window_data = [
                    (t, v)
                    for t, v in zip(xs, ys)
                    if analysis_window[0] <= t <= analysis_window[1]
                ]
                if not window_data:
                    continue

                times = [d[0] for d in window_data]
                values = [d[1] for d in window_data]

                # 计算基准转速（故障前稳态）
                pre_fault = [v for t, v in zip(xs, ys) if 2.0 <= t <= 2.4]
                base_speed = sum(pre_fault) / len(pre_fault) if pre_fault else 1.0

                # 最大转速偏差
                deviations = [abs(v - base_speed) for v in values]
                max_dev = max(deviations) if deviations else 0
                metrics["max_speed_deviation"] = max(
                    metrics["max_speed_deviation"], max_dev
                )

                # 估算稳定时间
                settling_time = analysis_window[1]
                for i, (t, v) in enumerate(window_data):
                    if abs(v - base_speed) < settling_threshold * base_speed:
                        settling_time = t
                        break
                if settling_time > metrics["settling_time"]:
                    metrics["settling_time"] = settling_time

                # 估算阻尼比和振荡频率
                damping, freq = self._estimate_damping(values, times)
                if damping > 0:
                    metrics["damping_ratio"] = damping
                if freq > 0:
                    metrics["oscillation_freq"] = freq

        # 稳定性判据
        metrics["is_stable"] = (
            metrics["max_speed_deviation"] < 0.5 and metrics["damping_ratio"] > 0.0
        )

        return metrics

    def _estimate_damping(self, values, times):
        """估算阻尼比和振荡频率"""
        if len(values) < 10:
            return 0, 0

        # 找峰值
        peaks = []
        for i in range(1, len(values) - 1):
            if values[i] > values[i - 1] and values[i] > values[i + 1]:
                peaks.append((times[i], values[i]))

        if len(peaks) < 2:
            return 0, 0

        # 估算振荡频率
        periods = [peaks[i + 1][0] - peaks[i][0] for i in range(len(peaks) - 1)]
        avg_period = sum(periods) / len(periods) if periods else 0
        freq = 1.0 / avg_period if avg_period > 0 else 0

        # 估算阻尼比（对数递减法）
        if len(peaks) >= 3:
            amplitudes = [p[1] for p in peaks]
            log_decrements = [
                math.log(amplitudes[i] / amplitudes[i + 1])
                for i in range(len(amplitudes) - 1)
                if amplitudes[i + 1] > 0
            ]
            avg_log_dec = (
                sum(log_decrements) / len(log_decrements) if log_decrements else 0
            )
            # 阻尼比 ≈ 对数递减 / (2π)
            damping = avg_log_dec / (2 * math.pi) if avg_log_dec > 0 else 0
        else:
            damping = 0

        return damping, freq

    def _assess_stability(self, metrics, max_dev_threshold):
        """评估稳定性"""
        return (
            metrics.get("max_speed_deviation", 999) < max_dev_threshold
            and metrics.get("damping_ratio", -1) > 0
        )

    def _analyze_stability_trend(self, results):
        """分析稳定性趋势"""
        if not results:
            return "unknown"

        stabilities = [r["stability"].get("is_stable", False) for r in results]
        deviations = [r["stability"].get("max_speed_deviation", 0) for r in results]
        fes = [r["fe"] for r in results]

        # 随着切除时间推迟，稳定性通常变差
        if all(stabilities):
            if all(
                deviations[i] <= deviations[i + 1] for i in range(len(deviations) - 1)
            ):
                return "degrading_with_delay"
            return "stable_all_cases"
        elif not any(stabilities):
            return "unstable_all_cases"
        else:
            # 部分稳定，找到临界切除时间
            return "partial_stable"

    def _generate_report(self, data, path):
        """生成Markdown报告"""
        lines = [
            "# 暂态稳定性分析报告",
            "",
            f"**模型**: {data['model']}",
            f"**故障位置**: {data['fault_location']}",
            f"**稳定性趋势**: {data['stability_trend']}",
            "",
            "## 各工况稳定性评估",
            "",
            "| 切除时间(s) | 稳定性 | 最大转速偏差 | 稳定时间(s) | 阻尼比 | 振荡频率(Hz) |",
            "|-------------|--------|--------------|-------------|--------|--------------|",
        ]

        for r in data["results"]:
            m = r["stability"]
            stable_str = "稳定" if m.get("is_stable") else "不稳定"
            lines.append(
                f"| {r['fe']:.2f} | {stable_str} | {m.get('max_speed_deviation', 0):.4f} | "
                f"{m.get('settling_time', 0):.2f} | {m.get('damping_ratio', 0):.4f} | {m.get('oscillation_freq', 0):.2f} |"
            )

        lines.extend(
            [
                "",
                "## 结论",
                "",
            ]
        )

        trend = data["stability_trend"]
        if trend == "stable_all_cases":
            lines.append("所有工况均保持暂态稳定。")
        elif trend == "degrading_with_delay":
            lines.append("随着故障切除时间推迟，系统稳定性逐渐恶化。建议尽快切除故障。")
        elif trend == "unstable_all_cases":
            lines.append("所有工况均失稳，需采取额外的稳定措施（如快关、切机等）。")
        else:
            lines.append("部分工况存在稳定性问题，需关注临界切除时间。")

        path.write_text("\n".join(lines), encoding="utf-8")
