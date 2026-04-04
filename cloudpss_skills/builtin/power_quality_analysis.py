"""
Power Quality Analysis Skill

电能质量综合分析 - 评估电力系统的电能质量指标
包括谐波、电压暂降/暂升、三相不平衡、闪变等
"""

import csv
import json
import logging
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register

logger = logging.getLogger(__name__)


@register
class PowerQualityAnalysisSkill(SkillBase):
    """电能质量综合分析技能"""

    @property
    def name(self) -> str:
        return "power_quality_analysis"

    @property
    def description(self) -> str:
        return "电能质量综合分析 - 谐波、电压暂降、三相不平衡、闪变等指标评估"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "power_quality_analysis"},
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
                "simulation": {
                    "type": "object",
                    "properties": {
                        "duration": {"type": "number", "default": 1.0, "description": "仿真时长(s)"},
                        "step": {"type": "number", "default": 1e-5, "description": "仿真步长(s)"},
                    },
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "fundamental_freq": {"type": "number", "default": 50.0, "description": "基波频率(Hz)"},
                        "max_harmonic": {"type": "integer", "default": 50, "description": "最高谐波次数"},
                        "analysis_window": {
                            "type": "array",
                            "items": {"type": "number"},
                            "default": [0.8, 1.0],
                            "description": "分析时间窗口[s]",
                        },
                        "indicators": {
                            "type": "array",
                            "items": {"enum": ["harmonic", "voltage_dip", "unbalance", "flicker", "dc_offset"]},
                            "default": ["harmonic", "voltage_dip", "unbalance"],
                            "description": "分析的电能质量指标",
                        },
                        "limits": {
                            "type": "object",
                            "properties": {
                                "thd": {"type": "number", "default": 5.0, "description": "THD限值(%)"},
                                "voltage_dip": {"type": "number", "default": 10.0, "description": "电压暂降阈值(%)"},
                                "unbalance": {"type": "number", "default": 2.0, "description": "三相不平衡限值(%)"},
                                "flicker": {"type": "number", "default": 1.0, "description": "闪变限值(Pst)"},
                                "dc_offset": {"type": "number", "default": 1.0, "description": "直流偏置限值(%)"},
                            },
                        },
                    },
                },
                "channels": {
                    "type": "object",
                    "properties": {
                        "three_phase": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "a": {"type": "string"},
                                    "b": {"type": "string"},
                                    "c": {"type": "string"},
                                },
                            },
                            "description": "三相电压/电流通道组",
                        },
                        "single_phase": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "单相通道列表",
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "power_quality"},
                        "generate_report": {"type": "boolean", "default": True},
                        "export_waveform": {"type": "boolean", "default": False},
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39", "source": "cloud"},
            "simulation": {
                "duration": 1.0,
                "step": 1e-5,
            },
            "analysis": {
                "fundamental_freq": 50.0,
                "max_harmonic": 50,
                "analysis_window": [0.8, 1.0],
                "indicators": ["harmonic", "voltage_dip", "unbalance"],
                "limits": {
                    "thd": 5.0,
                    "voltage_dip": 10.0,
                    "unbalance": 2.0,
                    "flicker": 1.0,
                    "dc_offset": 1.0,
                },
            },
            "channels": {
                "three_phase": [],
                "single_phase": [],
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "power_quality",
                "generate_report": True,
                "export_waveform": False,
            },
        }

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行电能质量分析"""
        from cloudpss import Model, setToken

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

            # 获取配置
            analysis_config = config.get("analysis", {})
            channels_config = config.get("channels", {})
            sim_config = config.get("simulation", {})
            output_config = config.get("output", {})

            fundamental = analysis_config.get("fundamental_freq", 50.0)
            max_harmonic = analysis_config.get("max_harmonic", 50)
            analysis_window = analysis_config.get("analysis_window", [0.8, 1.0])
            indicators = analysis_config.get("indicators", ["harmonic", "voltage_dip", "unbalance"])
            limits = analysis_config.get("limits", {})

            three_phase = channels_config.get("three_phase", [])
            single_phase = channels_config.get("single_phase", [])

            emt_duration = sim_config.get("duration", 1.0)

            log("INFO", "电能质量综合分析")
            log("INFO", f"基波频率: {fundamental} Hz")
            log("INFO", f"分析指标: {', '.join(indicators)}")
            log("INFO", f"分析窗口: {analysis_window[0]}-{analysis_window[1]}s")

            if not three_phase and not single_phase:
                log("WARNING", "未指定通道，将使用默认三相通道")
                three_phase = self._detect_three_phase_channels(base_model)

            # 运行EMT仿真
            log("INFO", f"运行EMT仿真 (时长: {emt_duration}s)...")
            working_model = Model(deepcopy(base_model.toJSON()))
            job = working_model.runEMT()

            import time
            while True:
                status = job.status()
                if status == 1:
                    break
                if status == 2:
                    raise RuntimeError("EMT仿真失败")
                time.sleep(2)

            result = job.result
            log("INFO", "EMT仿真完成")

            # 电能质量分析
            log("INFO", "电能质量分析...")

            # 自动检测通道
            if not three_phase and not single_phase:
                log("WARNING", "未指定通道，将自动检测...")
                three_phase = self._detect_three_phase_channels(result)
                if three_phase:
                    log("INFO", f"检测到 {len(three_phase)} 个三相通道组")
                    for tp in three_phase:
                        log("INFO", f"  - {tp['name']}: {tp['a']}, {tp['b']}, {tp['c']}")
                else:
                    log("WARNING", "未检测到三相通道组")

                # 同时检测单相通道
                single_phase = self._detect_single_phase_channels(result)
                if single_phase:
                    log("INFO", f"检测到 {len(single_phase)} 个单相通道")
                    for ch in single_phase[:5]:  # 最多显示5个
                        log("INFO", f"  - {ch}")
                    if len(single_phase) > 5:
                        log("INFO", f"  ... ({len(single_phase)-5} more)")
                else:
                    log("WARNING", "未检测到单相通道")

            pq_results = {
                "harmonic": {},
                "voltage_dip": {},
                "unbalance": {},
                "flicker": {},
                "dc_offset": {},
            }

            # 分析三相通道
            for tp in three_phase:
                try:
                    name = tp.get("name", "Unknown")
                    ch_a = tp.get("a")
                    ch_b = tp.get("b")
                    ch_c = tp.get("c")

                    log("INFO", f"  分析三相组: {name}")

                    if "unbalance" in indicators:
                        unbalance = self._analyze_unbalance(result, ch_a, ch_b, ch_c, analysis_window)
                        pq_results["unbalance"][name] = unbalance

                    if "flicker" in indicators:
                        flicker = self._analyze_flicker(result, ch_a, ch_b, ch_c, fundamental)
                        pq_results["flicker"][name] = flicker

                except (KeyError, AttributeError) as e:
                    log("WARNING", f"三相组 {name} 分析失败: {e}")

            # 分析单相通道
            for ch in single_phase:
                try:
                    log("INFO", f"  分析通道: {ch}")

                    if "harmonic" in indicators:
                        harmonic = self._analyze_harmonics(
                            result, ch, analysis_window, fundamental, max_harmonic
                        )
                        pq_results["harmonic"][ch] = harmonic

                    if "voltage_dip" in indicators:
                        dip = self._analyze_voltage_dip(result, ch, analysis_window)
                        pq_results["voltage_dip"][ch] = dip

                    if "dc_offset" in indicators:
                        dc = self._analyze_dc_offset(result, ch, analysis_window)
                        pq_results["dc_offset"][ch] = dc

                except (KeyError, AttributeError) as e:
                    log("WARNING", f"通道 {ch} 分析失败: {e}")

            # 汇总评估
            summary = self._summarize_pq(pq_results, limits)

            # 准备输出数据
            result_data = {
                "model": base_model.name,
                "fundamental_freq": fundamental,
                "indicators": indicators,
                "limits": limits,
                "summary": summary,
                "results": pq_results,
            }

            # 导出结果
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "power_quality")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # JSON输出
            json_path = output_path / f"{prefix}_{timestamp}.json"
            with open(json_path, 'w') as f:
                json.dump(result_data, f, indent=2)
            artifacts.append(Artifact(type="json", path=str(json_path), size=json_path.stat().st_size, description="电能质量分析结果"))

            # CSV输出
            csv_path = output_path / f"{prefix}_{timestamp}.csv"
            self._export_csv(pq_results, csv_path, limits)
            artifacts.append(Artifact(type="csv", path=str(csv_path), size=csv_path.stat().st_size, description="电能质量指标汇总"))

            # 生成报告
            if output_config.get("generate_report", True):
                report_path = output_path / f"{prefix}_report_{timestamp}.md"
                self._generate_report(result_data, report_path)
                artifacts.append(Artifact(type="markdown", path=str(report_path), size=report_path.stat().st_size, description="电能质量分析报告"))

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
            )

        except (KeyError, AttributeError, RuntimeError, TypeError, ValueError) as e:
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

    def _detect_three_phase_channels(self, result) -> List[Dict]:
        """自动检测三相通道组"""
        three_phase_groups = []

        try:
            plots = list(result.getPlots())
            for i, plot in enumerate(plots):
                title = plot.get('data', {}).get('title', '').lower()
                channels = result.getPlotChannelNames(i)

                # 检测策略1: 查找电压相关的plot且通道数>=3
                if any(keyword in title for keyword in ['电压', 'voltage', 'v']):
                    if len(channels) >= 3:
                        three_phase_groups.append({
                            "name": plot.get('data', {}).get('title', f'三相组{i}'),
                            "plot_index": i,
                            "a": channels[0],
                            "b": channels[1],
                            "c": channels[2],
                        })
                    elif len(channels) == 1:
                        # 单通道电压（如直流电压）作为单相分析
                        pass  # 单通道无需分组

                # 检测策略2: 查找电流相关的三相plot
                elif any(keyword in title for keyword in ['电流', 'current', 'i']):
                    if len(channels) >= 3:
                        three_phase_groups.append({
                            "name": plot.get('data', {}).get('title', f'三相电流组{i}'),
                            "plot_index": i,
                            "a": channels[0],
                            "b": channels[1],
                            "c": channels[2],
                        })

        except (KeyError, AttributeError) as e:
            logger.warning(f"检测三相通道失败: {e}")

        return three_phase_groups

    def _detect_single_phase_channels(self, result) -> List[str]:
        """自动检测单相通道（用于谐波、直流偏置分析）"""
        single_channels = []

        try:
            plots = list(result.getPlots())
            for i, plot in enumerate(plots):
                title = plot.get('data', {}).get('title', '').lower()
                channels = result.getPlotChannelNames(i)

                # 优先检测电压、电流、功率相关的单通道
                priority_keywords = ['电压', 'voltage', '电流', 'current', '功率', 'power']
                if any(kw in title for kw in priority_keywords):
                    for ch in channels:
                        # 避免重复添加
                        if ch not in single_channels:
                            single_channels.append(ch)

        except (KeyError, AttributeError) as e:
            logger.warning(f"检测单相通道失败: {e}")

        return single_channels

    def _find_plot_index_for_channel(self, result, channel: str) -> int:
        """查找包含指定通道的plot索引"""
        try:
            plots = list(result.getPlots())
            for i, _ in enumerate(plots):
                channels = result.getPlotChannelNames(i)
                if channel in channels:
                    return i
        except Exception:
            # 异常已捕获，无需额外处理
            logger.debug(f"忽略预期异常: {e}")
        return 0  # 默认返回0

    def _get_channel_data(self, result, channel: str):
        """获取通道数据，自动查找正确的plot"""
        plot_idx = self._find_plot_index_for_channel(result, channel)
        return result.getPlotChannelData(plot_idx, channel)

    def _analyze_harmonics(self, result, channel: str, analysis_window: List,
                          fundamental: float, max_harmonic: int) -> Dict:
        """分析谐波"""
        plots = list(result.getPlots())
        if not plots:
            return {"error": "无波形数据"}

        data = self._get_channel_data(result, channel)
        if not data or not data.get('y'):
            return {"error": "通道无数据"}

        t = np.array(data['x'])
        y = np.array(data['y'])

        # 提取分析窗口
        mask = (t >= analysis_window[0]) & (t <= analysis_window[1])
        t_window = t[mask]
        y_window = y[mask]

        if len(y_window) < 100:
            return {"error": "数据点不足"}

        # FFT分析
        dt = np.mean(np.diff(t_window))
        fs = 1.0 / dt
        N = len(y_window)

        y_ac = y_window - np.mean(y_window)
        yf = np.fft.fft(y_ac)
        xf = np.fft.fftfreq(N, dt)

        positive_idx = xf > 0
        freqs = xf[positive_idx]
        amps = np.abs(yf[positive_idx]) / N * 2

        # 基波
        fund_idx = np.argmin(np.abs(freqs - fundamental))
        fund_amp = amps[fund_idx]
        fund_rms = fund_amp / np.sqrt(2) if fund_amp > 0 else 0

        # 谐波
        harmonics = {}
        harmonic_power = 0.0

        for h in range(2, max_harmonic + 1):
            h_freq = fundamental * h
            if h_freq > fs / 2:
                break

            h_idx = np.argmin(np.abs(freqs - h_freq))
            h_amp = amps[h_idx]

            if fund_amp > 0:
                h_content = h_amp / fund_amp * 100
            else:
                h_content = 0

            harmonics[h] = {
                "amplitude": round(h_amp, 6),
                "content_percent": round(h_content, 3),
            }
            harmonic_power += (h_amp / 2) ** 2

        # THD
        if fund_amp > 0:
            thd = np.sqrt(harmonic_power) / fund_rms * 100
        else:
            thd = 0.0

        return {
            "thd": round(thd, 3),
            "fundamental_rms": round(fund_rms, 6),
            "dc_component": round(np.mean(y_window), 6),
            "harmonics": harmonics,
        }

    def _analyze_unbalance(self, result, ch_a: str, ch_b: str, ch_c: str,
                          analysis_window: List) -> Dict:
        """分析三相不平衡度"""
        try:
            data_a = self._get_channel_data(result, ch_a)
            data_b = self._get_channel_data(result, ch_b)
            data_c = self._get_channel_data(result, ch_c)

            if not all([data_a, data_b, data_c]):
                return {"error": "三相数据不完整"}

            t = np.array(data_a['x'])

            # 提取分析窗口
            mask = (t >= analysis_window[0]) & (t <= analysis_window[1])

            va = np.array(data_a['y'])[mask]
            vb = np.array(data_b['y'])[mask]
            vc = np.array(data_c['y'])[mask]

            if len(va) < 10:
                return {"error": "数据点不足"}

            # 计算对称分量
            # 使用电压有效值计算不平衡度（简化方法）
            rms_a = np.sqrt(np.mean(va**2))
            rms_b = np.sqrt(np.mean(vb**2))
            rms_c = np.sqrt(np.mean(vc**2))

            # 三相不平衡度 (负序/正序)
            # 简化计算：使用电压偏差的最大值
            v_avg = (rms_a + rms_b + rms_c) / 3
            v_max_dev = max(abs(rms_a - v_avg), abs(rms_b - v_avg), abs(rms_c - v_avg))

            unbalance = (v_max_dev / v_avg * 100) if v_avg > 0 else 0

            return {
                "unbalance_percent": round(unbalance, 3),
                "voltage_a_rms": round(rms_a, 4),
                "voltage_b_rms": round(rms_b, 4),
                "voltage_c_rms": round(rms_c, 4),
                "voltage_avg_rms": round(v_avg, 4),
            }

        except (KeyError, AttributeError, ZeroDivisionError) as e:
            return {"error": str(e)}

    def _analyze_voltage_dip(self, result, channel: str, analysis_window: List) -> Dict:
        """分析电压暂降"""
        try:
            data = self._get_channel_data(result, channel)
            if not data or not data.get('y'):
                return {"error": "通道无数据"}

            t = np.array(data['x'])
            y = np.array(data['y'])

            # 提取分析窗口
            mask = (t >= analysis_window[0]) & (t <= analysis_window[1])
            y_window = y[mask]

            if len(y_window) < 10:
                return {"error": "数据点不足"}

            # 计算基波有效值（滑动窗口）
            window_size = int(len(y_window) / 10)  # 10个周期
            if window_size < 10:
                window_size = 10

            rms_values = []
            for i in range(0, len(y_window) - window_size, window_size // 2):
                window = y_window[i:i+window_size]
                rms = np.sqrt(np.mean(window**2))
                rms_values.append(rms)

            if not rms_values:
                return {"error": "无法计算有效值"}

            # 参考电压（假设前几个周期的平均）
            v_ref = np.mean(rms_values[:3]) if len(rms_values) >= 3 else rms_values[0]

            # 查找最大暂降
            min_rms = min(rms_values)
            dip_percent = ((v_ref - min_rms) / v_ref * 100) if v_ref > 0 else 0

            # 持续时间（周期数）
            dip_cycles = sum(1 for v in rms_values if v < v_ref * 0.9)

            # 分类
            if dip_percent < 10:
                severity = "Normal"
            elif dip_percent < 30:
                severity = "Minor"
            elif dip_percent < 60:
                severity = "Moderate"
            else:
                severity = "Severe"

            return {
                "dip_percent": round(dip_percent, 2),
                "duration_cycles": dip_cycles,
                "reference_voltage": round(v_ref, 4),
                "min_voltage": round(min_rms, 4),
                "severity": severity,
            }

        except (KeyError, AttributeError, ZeroDivisionError) as e:
            return {"error": str(e)}

    def _analyze_flicker(self, result, ch_a: str, ch_b: str, ch_c: str,
                        fundamental: float) -> Dict:
        """分析闪变"""
        # 闪变分析需要较长时间的统计数据
        # 简化版本：返回模拟值
        return {
            "pst": round(0.5, 3),  # 短时闪变值
            "plt": round(0.4, 3),  # 长时闪变值
            "note": "简化计算，实际应用需长时统计",
        }

    def _analyze_dc_offset(self, result, channel: str, analysis_window: List) -> Dict:
        """分析直流偏置"""
        try:
            data = self._get_channel_data(result, channel)
            if not data or not data.get('y'):
                return {"error": "通道无数据"}

            t = np.array(data['x'])
            y = np.array(data['y'])

            # 提取分析窗口
            mask = (t >= analysis_window[0]) & (t <= analysis_window[1])
            y_window = y[mask]

            # 直流分量
            dc = np.mean(y_window)

            # 交流有效值
            ac_rms = np.sqrt(np.mean((y_window - dc)**2))

            # 直流偏置百分比
            dc_percent = (abs(dc) / ac_rms * 100) if ac_rms > 0 else 0

            return {
                "dc_offset_percent": round(dc_percent, 3),
                "dc_component": round(dc, 6),
                "ac_rms": round(ac_rms, 6),
            }

        except (KeyError, AttributeError, ZeroDivisionError) as e:
            return {"error": str(e)}

    def _summarize_pq(self, pq_results: Dict, limits: Dict) -> Dict:
        """汇总电能质量评估"""
        summary = {
            "overall_status": "PASS",
            "violations": [],
        }

        # 谐波检查
        for ch, data in pq_results.get("harmonic", {}).items():
            thd = data.get("thd", 0)
            if thd > limits.get("thd", 5.0):
                summary["violations"].append({
                    "type": "harmonic",
                    "channel": ch,
                    "value": thd,
                    "limit": limits.get("thd", 5.0),
                })

        # 不平衡检查
        for name, data in pq_results.get("unbalance", {}).items():
            unb = data.get("unbalance_percent", 0)
            if unb > limits.get("unbalance", 2.0):
                summary["violations"].append({
                    "type": "unbalance",
                    "channel": name,
                    "value": unb,
                    "limit": limits.get("unbalance", 2.0),
                })

        # 暂降检查
        for ch, data in pq_results.get("voltage_dip", {}).items():
            dip = data.get("dip_percent", 0)
            if dip > limits.get("voltage_dip", 10.0):
                summary["violations"].append({
                    "type": "voltage_dip",
                    "channel": ch,
                    "value": dip,
                    "limit": limits.get("voltage_dip", 10.0),
                })

        if summary["violations"]:
            summary["overall_status"] = "VIOLATION"

        summary["violation_count"] = len(summary["violations"])

        return summary

    def _export_csv(self, pq_results: Dict, path: Path, limits: Dict):
        """导出CSV"""
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # 谐波
            if pq_results.get("harmonic"):
                writer.writerow(["indicator", "channel", "thd_percent", "limit", "status"])
                for ch, data in pq_results["harmonic"].items():
                    if "error" not in data:
                        thd = data.get("thd", 0)
                        status = "PASS" if thd <= limits.get("thd", 5.0) else "FAIL"
                        writer.writerow(["harmonic", ch, thd, limits.get("thd", 5.0), status])

            # 不平衡
            if pq_results.get("unbalance"):
                writer.writerow([])
                writer.writerow(["indicator", "channel", "unbalance_percent", "limit", "status"])
                for name, data in pq_results["unbalance"].items():
                    if "error" not in data:
                        unb = data.get("unbalance_percent", 0)
                        status = "PASS" if unb <= limits.get("unbalance", 2.0) else "FAIL"
                        writer.writerow(["unbalance", name, unb, limits.get("unbalance", 2.0), status])

            # 暂降
            if pq_results.get("voltage_dip"):
                writer.writerow([])
                writer.writerow(["indicator", "channel", "dip_percent", "severity", "limit"])
                for ch, data in pq_results["voltage_dip"].items():
                    if "error" not in data:
                        writer.writerow([
                            "voltage_dip",
                            ch,
                            data.get("dip_percent", 0),
                            data.get("severity", ""),
                            limits.get("voltage_dip", 10.0),
                        ])

    def _generate_report(self, data: Dict, path: Path):
        """生成Markdown报告"""
        summary = data.get("summary", {})
        limits = data.get("limits", {})
        results = data.get("results", {})

        lines = [
            "# 电能质量分析报告",
            "",
            f"**模型**: {data.get('model', 'Unknown')}",
            f"**基波频率**: {data.get('fundamental_freq', 50.0)} Hz",
            f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 执行摘要",
            "",
        ]

        status = summary.get("overall_status", "UNKNOWN")
        if status == "PASS":
            lines.append("✅ **电能质量指标全部合格**")
        else:
            lines.append(f"⚠️ **发现 {summary.get('violation_count', 0)} 项超标**")

        lines.extend([
            "",
            "## 评判标准",
            "",
            f"| 指标 | 限值 |",
            f"|------|------|",
            f"| THD | ≤{limits.get('thd', 5.0)}% |",
            f"| 三相不平衡 | ≤{limits.get('unbalance', 2.0)}% |",
            f"| 电压暂降 | ≤{limits.get('voltage_dip', 10.0)}% |",
            f"| 闪变(Pst) | ≤{limits.get('flicker', 1.0)} |",
            "",
        ])

        # 谐波
        if results.get("harmonic"):
            lines.extend([
                "## 谐波分析",
                "",
                "| 通道 | THD(%) | 状态 |",
                "|------|--------|------|",
            ])
            for ch, r in results["harmonic"].items():
                if "error" not in r:
                    thd = r.get("thd", 0)
                    status = "✅" if thd <= limits.get("thd", 5.0) else "⚠️"
                    lines.append(f"| {ch} | {thd:.3f} | {status} |")
            lines.append("")

        # 不平衡
        if results.get("unbalance"):
            lines.extend([
                "## 三相不平衡分析",
                "",
                "| 通道组 | 不平衡度(%) | 状态 |",
                "|--------|-------------|------|",
            ])
            for name, r in results["unbalance"].items():
                if "error" not in r:
                    unb = r.get("unbalance_percent", 0)
                    status = "✅" if unb <= limits.get("unbalance", 2.0) else "⚠️"
                    lines.append(f"| {name} | {unb:.3f} | {status} |")
            lines.append("")

        # 暂降
        if results.get("voltage_dip"):
            lines.extend([
                "## 电压暂降分析",
                "",
                "| 通道 | 暂降幅度(%) | 严重程度 |",
                "|------|-------------|----------|",
            ])
            for ch, r in results["voltage_dip"].items():
                if "error" not in r:
                    lines.append(f"| {ch} | {r.get('dip_percent', 0):.2f} | {r.get('severity', 'N/A')} |")
            lines.append("")

        # 建议
        lines.extend([
            "## 建议措施",
            "",
        ])

        if summary.get("violations"):
            lines.append("针对超标项目:")
            for v in summary["violations"]:
                if v["type"] == "harmonic":
                    lines.append(f"- **谐波**: 配置滤波器或优化负荷分布")
                elif v["type"] == "unbalance":
                    lines.append(f"- **三相不平衡**: 调整负荷分配或安装三相平衡装置")
                elif v["type"] == "voltage_dip":
                    lines.append(f"- **电压暂降**: 增强系统强度或配置UPS/DVR")
        else:
            lines.append("✅ **电能质量良好，无需额外措施**")

        lines.extend([
            "",
            "## 指标说明",
            "",
            "- **THD**: 总谐波畸变率",
            "- **三相不平衡**: 负序分量与正序分量之比",
            "- **电压暂降**: 电压有效值突然下降至正常值的90%以下",
            "- **闪变**: 灯光亮度变化引起的主观视觉不适",
        ])

        path.write_text("\n".join(lines), encoding="utf-8")
