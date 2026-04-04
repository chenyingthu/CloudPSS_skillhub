"""
Frequency Response Analysis Skill

频率响应分析 - 基于EMT仿真分析系统频率动态响应
支持负荷扰动、发电机跳闸等场景，提取频率最低点、变化率、恢复时间等指标
"""

import csv
import json
import logging
import math
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register

logger = logging.getLogger(__name__)

# 扰动类型定义
STEP_LOAD_CHANGE = "step_load_change"  # 阶跃负荷变化
GENERATOR_TRIP = "generator_trip"       # 发电机跳闸
LOAD_SHEDDING = "load_shedding"         # 负荷切除


@register
class FrequencyResponseSkill(SkillBase):
    """频率响应分析技能"""

    @property
    def name(self) -> str:
        return "frequency_response"

    @property
    def description(self) -> str:
        return "频率响应分析 - 基于EMT仿真分析系统频率动态响应特性"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model", "disturbance"],
            "properties": {
                "skill": {"type": "string", "const": "frequency_response"},
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
                "disturbance": {
                    "type": "object",
                    "required": ["type"],
                    "properties": {
                        "type": {
                            "enum": ["step_load_change", "generator_trip", "load_shedding"],
                            "description": "扰动类型",
                        },
                        "time": {"type": "number", "default": 2.0, "description": "扰动发生时间(s)"},
                        # 阶跃负荷变化参数
                        "load_target": {"type": "string", "description": "目标负荷组件"},
                        "load_change_percent": {"type": "number", "description": "负荷变化百分比(%)"},
                        # 发电机跳闸参数
                        "generator_target": {"type": "string", "description": "目标发电机组件"},
                        # 负荷切除参数
                        "shed_load_target": {"type": "string", "description": "切除负荷目标"},
                        "shed_percent": {"type": "number", "description": "切除百分比(%)"},
                    },
                },
                "monitoring": {
                    "type": "object",
                    "properties": {
                        "frequency_channels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "频率/转速信号通道",
                        },
                        "power_channels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "功率信号通道",
                        },
                    },
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "base_frequency": {"type": "number", "default": 60.0, "description": "基准频率(Hz)"},
                        "analysis_window": {
                            "type": "array",
                            "items": {"type": "number"},
                            "default": [2.0, 10.0],
                            "description": "分析时间窗口[s]",
                        },
                        "frequency_deadband": {"type": "number", "default": 0.05, "description": "频率死区(Hz)"},
                        "settling_threshold": {"type": "number", "default": 0.1, "description": "稳定阈值(Hz)"},
                    },
                },
                "emt": {
                    "type": "object",
                    "properties": {
                        "duration": {"type": "number", "default": 10.0, "description": "仿真时长(s)"},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "frequency_response"},
                        "generate_report": {"type": "boolean", "default": True},
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39", "source": "cloud"},
            "disturbance": {
                "type": "step_load_change",
                "time": 2.0,
                "load_change_percent": 10.0,
            },
            "monitoring": {
                "frequency_channels": ["#Gen38.wr:0"],
                "power_channels": ["#Gen38.IT:0"],
            },
            "analysis": {
                "base_frequency": 60.0,
                "analysis_window": [2.0, 10.0],
                "frequency_deadband": 0.05,
                "settling_threshold": 0.1,
            },
            "emt": {
                "duration": 10.0,
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "frequency_response",
                "generate_report": True,
            },
        }

    def run(self, config: Dict[str, Any]) -> SkillResult:
        from cloudpss import Model, setToken
        import time

        start_time = datetime.now()
        logs = []
        artifacts = []

        def log(level: str, message: str):
            logs.append(LogEntry(timestamp=datetime.now(), level=level, message=message))
            getattr(logger, level.lower(), logger.info)(message)

        try:
            log("INFO", "加载认证...")
            auth = config.get("auth", {})
            token = auth.get("token")
            if not token:
                token_file = auth.get("token_file", ".cloudpss_token")
                token_path = Path(token_file)
                if not token_path.exists():
                    raise FileNotFoundError(f"Token文件不存在: {token_file}")
                token = token_path.read_text().strip()
            setToken(token)
            log("INFO", "认证成功")

            model_config = config["model"]
            if model_config.get("source") == "local":
                base_model = Model.load(model_config["rid"])
            else:
                base_model = Model.fetch(model_config["rid"])
            log("INFO", f"模型: {base_model.name}")

            disturbance_config = config["disturbance"]
            monitoring_config = config.get("monitoring", {})
            analysis_config = config.get("analysis", {})
            emt_config = config.get("emt", {})
            output_config = config.get("output", {})

            disturbance_type = disturbance_config["type"]
            disturbance_time = disturbance_config.get("time", 2.0)

            base_freq = analysis_config.get("base_frequency", 60.0)
            analysis_window = analysis_config.get("analysis_window", [2.0, 10.0])
            freq_deadband = analysis_config.get("frequency_deadband", 0.05)
            settling_threshold = analysis_config.get("settling_threshold", 0.1)

            freq_channels = monitoring_config.get("frequency_channels", [])
            power_channels = monitoring_config.get("power_channels", [])

            emt_duration = emt_config.get("duration", 10.0)

            log("INFO", f"频率响应分析: {base_model.name}")
            log("INFO", f"扰动类型: {disturbance_type}, 时间: {disturbance_time}s")

            # 准备模型
            working_model = Model(deepcopy(base_model.toJSON()))

            # 配置扰动
            self._configure_disturbance(
                working_model, disturbance_type, disturbance_time,
                disturbance_config, log
            )

            # 运行EMT
            log("INFO", f"运行EMT仿真 (时长: {emt_duration}s)...")
            job = working_model.runEMT()
            log("INFO", f"Job ID: {job.id}")

            # 等待完成
            while True:
                status = job.status()
                if status == 1:
                    break
                if status == 2:
                    raise RuntimeError("EMT仿真失败")
                time.sleep(2)

            result = job.result
            log("INFO", "EMT仿真完成")

            # 分析频率响应
            log("INFO", "分析频率响应...")
            frequency_metrics = self._analyze_frequency_response(
                result, freq_channels, base_freq, analysis_window,
                freq_deadband, settling_threshold, log
            )

            # 汇总结果
            result_data = {
                "model": base_model.name,
                "disturbance_type": disturbance_type,
                "disturbance_time": disturbance_time,
                "base_frequency": base_freq,
                "frequency_metrics": frequency_metrics,
            }

            # 导出结果
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "frequency_response")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # JSON输出
            json_path = output_path / f"{prefix}_{timestamp}.json"
            with open(json_path, 'w') as f:
                json.dump(result_data, f, indent=2)
            artifacts.append(Artifact(type="json", path=str(json_path), size=json_path.stat().st_size, description="频率响应分析结果"))

            # CSV输出
            csv_path = output_path / f"{prefix}_{timestamp}.csv"
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["channel", "nadir_freq", "nadir_time", "max_rocof", "steady_freq", "settling_time", "frequency_deviation"])
                for ch, metrics in frequency_metrics.items():
                    writer.writerow([
                        ch,
                        f"{metrics.get('nadir_frequency', 0):.4f}",
                        f"{metrics.get('nadir_time', 0):.4f}",
                        f"{metrics.get('max_rocof', 0):.4f}",
                        f"{metrics.get('steady_frequency', 0):.4f}",
                        f"{metrics.get('settling_time', 0):.4f}",
                        f"{metrics.get('frequency_deviation', 0):.4f}",
                    ])
            artifacts.append(Artifact(type="csv", path=str(csv_path), size=csv_path.stat().st_size, description="频率响应数据"))

            # 生成报告
            if output_config.get("generate_report", True):
                report_path = output_path / f"{prefix}_report_{timestamp}.md"
                self._generate_report(result_data, report_path)
                artifacts.append(Artifact(type="markdown", path=str(report_path), size=report_path.stat().st_size, description="频率响应分析报告"))

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
            )

        except (KeyError, AttributeError, ZeroDivisionError) as e:
            log("ERROR", f"执行失败: {e}")
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

    def _configure_disturbance(self, model, disturbance_type: str, disturbance_time: float,
                               config: Dict, log_func):
        """配置扰动"""
        from cloudpss import Model

        components = model.getAllComponents()

        if disturbance_type == "step_load_change":
            # 阶跃负荷变化
            load_target = config.get("load_target")
            change_percent = config.get("load_change_percent", 10)

            for key, comp in components.items():
                if not hasattr(comp, 'args'):
                    continue

                comp_def = getattr(comp, "definition", "")
                comp_label = getattr(comp, "label", "")

                # 匹配目标负荷
                if load_target and comp_label != load_target and load_target not in key:
                    continue

                # 检查负荷类型
                if "_newExpLoad" in comp_def:
                    # 指数负荷模型
                    p_val = comp.args.get("p", {}).get("source", "1")
                    try:
                        base_p = float(p_val)
                        new_p = base_p * (1 + change_percent / 100)
                        args = {
                            "stepTime": {"source": str(disturbance_time), "ɵexp": ""},
                            "stepValue": {"source": str(new_p), "ɵexp": ""},
                        }
                        model.updateComponent(key, args=args)
                        log_func("INFO", f"负荷阶跃: {comp_label}, {base_p}MW -> {new_p}MW @ {disturbance_time}s")
                    except (ValueError, TypeError) as e:
                        # 异常已捕获，无需额外处理
                        logger.debug(f"忽略预期异常: {e}")

                elif "_newLoad" in comp_def:
                    # 标准负荷模型
                    pf_P = comp.args.get("pf_P", {}).get("source", "1")
                    try:
                        base_p = float(pf_P)
                        new_p = base_p * (1 + change_percent / 100)
                        args = {
                            "stepTime": {"source": str(disturbance_time), "ɵexp": ""},
                            "stepValue": {"source": str(new_p), "ɵexp": ""},
                        }
                        model.updateComponent(key, args=args)
                        log_func("INFO", f"负荷阶跃: {comp_label}, {base_p}MW -> {new_p}MW @ {disturbance_time}s")
                    except (ValueError, TypeError) as e:
                        # 异常已捕获，无需额外处理
                        logger.debug(f"忽略预期异常: {e}")

        elif disturbance_type == "generator_trip":
            # 发电机跳闸
            gen_target = config.get("generator_target")

            for key, comp in components.items():
                if not hasattr(comp, 'args'):
                    continue

                comp_def = getattr(comp, "definition", "")
                comp_label = getattr(comp, "label", "")

                # 匹配目标发电机
                if gen_target and comp_label != gen_target and gen_target not in key:
                    continue

                if "Generator" in comp_def or "_newGenerator" in comp_def:
                    # 使用断路器跳闸
                    args = {
                        "tripTime": {"source": str(disturbance_time), "ɵexp": ""},
                    }
                    model.updateComponent(key, args=args)
                    log_func("INFO", f"发电机跳闸: {comp_label} @ {disturbance_time}s")
                    break

        elif disturbance_type == "load_shedding":
            # 负荷切除
            shed_target = config.get("shed_load_target")
            shed_percent = config.get("shed_percent", 50)

            for key, comp in components.items():
                if not hasattr(comp, 'args'):
                    continue

                comp_def = getattr(comp, "definition", "")
                comp_label = getattr(comp, "label", "")

                # 匹配目标负荷
                if shed_target and comp_label != shed_target and shed_target not in key:
                    continue

                if "_newExpLoad" in comp_def or "_newLoad" in comp_def:
                    args = {
                        "shedTime": {"source": str(disturbance_time), "ɵexp": ""},
                        "shedPercent": {"source": str(shed_percent), "ɵexp": ""},
                    }
                    model.updateComponent(key, args=args)
                    log_func("INFO", f"负荷切除: {comp_label}, {shed_percent}% @ {disturbance_time}s")
                    break

    def _analyze_frequency_response(self, result, freq_channels: List, base_freq: float,
                                    analysis_window: List, freq_deadband: float,
                                    settling_threshold: float, log_func) -> Dict:
        """分析频率响应"""
        metrics = {}

        for plot_idx in range(len(result.getPlots())):
            channel_names = result.getPlotChannelNames(plot_idx)

            for ch in freq_channels:
                if ch not in channel_names:
                    continue

                trace = result.getPlotChannelData(plot_idx, ch)
                if not trace or not trace.get("y"):
                    continue

                xs = trace.get("x", [])
                ys = trace.get("y", [])

                if not xs or not ys:
                    continue

                # 转速转换为频率（如果是转速信号）
                # wr是标幺值，额定转速=1.0 pu，对应base_freq
                frequencies = []
                for v in ys:
                    if isinstance(v, (int, float)):
                        freq = v * base_freq  # 标幺转速转换为Hz
                        frequencies.append(freq)
                    else:
                        frequencies.append(base_freq)

                # 提取分析窗口内的数据
                window_data = [(t, f) for t, f in zip(xs, frequencies)
                              if analysis_window[0] <= t <= analysis_window[1]]

                if not window_data:
                    continue

                times = [d[0] for d in window_data]
                freqs = [d[1] for d in window_data]

                # 基准频率（扰动前稳态）
                pre_disturbance = [f for t, f in zip(xs, frequencies)
                                  if analysis_window[0] - 0.5 <= t < analysis_window[0]]
                base_freq_val = sum(pre_disturbance) / len(pre_disturbance) if pre_disturbance else base_freq

                # 频率最低点
                nadir_freq = min(freqs) if freqs else base_freq_val
                nadir_idx = freqs.index(nadir_freq) if freqs else 0
                nadir_time = times[nadir_idx] if nadir_idx < len(times) else analysis_window[0]

                # 最大频率变化率 (Hz/s)
                max_rocof = 0
                for i in range(1, len(freqs)):
                    dt = times[i] - times[i-1]
                    if dt > 0:
                        df = abs(freqs[i] - freqs[i-1])
                        rocof = df / dt
                        max_rocof = max(max_rocof, rocof)

                # 稳态频率（分析窗口最后1秒的平均）
                steady_data = [f for t, f in window_data if t > analysis_window[1] - 1.0]
                steady_freq = sum(steady_data) / len(steady_data) if steady_data else base_freq_val

                # 稳定时间（进入稳态阈值的时间）
                settling_time = analysis_window[1]
                for i, (t, f) in enumerate(window_data):
                    if t > nadir_time:
                        if abs(f - steady_freq) < settling_threshold:
                            # 连续5个点在阈值内
                            if i + 5 < len(freqs):
                                if all(abs(freqs[j] - steady_freq) < settling_threshold
                                       for j in range(i, i+5)):
                                    settling_time = t
                                    break

                # 频率偏差
                freq_deviation = steady_freq - base_freq_val

                metrics[ch] = {
                    "base_frequency": base_freq_val,
                    "nadir_frequency": nadir_freq,
                    "nadir_time": nadir_time,
                    "max_rocof": max_rocof,
                    "steady_frequency": steady_freq,
                    "settling_time": settling_time,
                    "frequency_deviation": freq_deviation,
                }

                log_func("INFO", f"  {ch}:")
                log_func("INFO", f"    基准频率: {base_freq_val:.4f} Hz")
                log_func("INFO", f"    最低点: {nadir_freq:.4f} Hz @ {nadir_time:.3f}s")
                log_func("INFO", f"    最大变化率: {max_rocof:.2f} Hz/s")
                log_func("INFO", f"    稳态频率: {steady_freq:.4f} Hz")
                log_func("INFO", f"    稳定时间: {settling_time:.3f}s")

        return metrics

    def _generate_report(self, data: Dict, path: Path):
        """生成Markdown报告"""
        lines = [
            "# 频率响应分析报告",
            "",
            f"**模型**: {data['model']}",
            f"**扰动类型**: {data['disturbance_type']}",
            f"**扰动时间**: {data['disturbance_time']} s",
            f"**基准频率**: {data['base_frequency']} Hz",
            "",
            "## 频率响应指标",
            "",
            "| 通道 | 最低点(Hz) | 最低点时间(s) | 最大变化率(Hz/s) | 稳态频率(Hz) | 稳定时间(s) | 频率偏差(Hz) |",
            "|------|------------|---------------|------------------|--------------|-------------|--------------|",
        ]

        for ch, metrics in data.get("frequency_metrics", {}).items():
            lines.append(
                f"| {ch} | {metrics.get('nadir_frequency', 0):.4f} | "
                f"{metrics.get('nadir_time', 0):.4f} | "
                f"{metrics.get('max_rocof', 0):.2f} | "
                f"{metrics.get('steady_frequency', 0):.4f} | "
                f"{metrics.get('settling_time', 0):.4f} | "
                f"{metrics.get('frequency_deviation', 0):.4f} |"
            )

        lines.extend([
            "",
            "## 指标说明",
            "",
            "- **最低点**: 扰动后系统频率的最低值",
            "- **最大变化率**: 频率变化的最大速率 (RoCoF)",
            "- **稳态频率**: 扰动后系统达到的新稳态频率",
            "- **稳定时间**: 从扰动开始到频率进入稳态的时间",
            "- **频率偏差**: 稳态频率与基准频率的差值",
            "",
            "## 结论",
            "",
        ])

        # 汇总信息
        if data.get("frequency_metrics"):
            all_nadir = [m.get("nadir_frequency", data['base_frequency']) for m in data["frequency_metrics"].values()]
            min_nadir = min(all_nadir) if all_nadir else data['base_frequency']
            max_dev = max(abs(m.get("frequency_deviation", 0)) for m in data["frequency_metrics"].values())

            lines.append(f"系统频率最低点为 **{min_nadir:.4f} Hz**")
            lines.append(f"")
            lines.append(f"频率最大偏差为 **{max_dev:.4f} Hz**")

            # 评估
            if min_nadir < data['base_frequency'] - 0.5:
                lines.append(f"")
                lines.append("⚠️ 频率跌落较大，可能需要评估低频减载策略。")
            elif max_dev < 0.1:
                lines.append(f"")
                lines.append("✅ 系统频率响应良好，扰动后能快速恢复稳定。")

        path.write_text("\n".join(lines), encoding="utf-8")
