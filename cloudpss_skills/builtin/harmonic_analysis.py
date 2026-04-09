"""
Harmonic Analysis Skill

谐波分析 - 基于EMT仿真结果进行FFT分析
计算电压/电流波形的谐波含量、THD、识别谐波频谱
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
from cloudpss_skills.core.auth_utils import load_or_fetch_model, run_emt

logger = logging.getLogger(__name__)


@register
class HarmonicAnalysisSkill(SkillBase):
    """谐波分析技能"""

    @property
    def name(self) -> str:
        return "harmonic_analysis"

    @property
    def description(self) -> str:
        return "谐波分析 - 基于EMT仿真结果进行FFT分析，计算THD和谐波频谱"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "harmonic_analysis"},
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
                        "duration": {"type": "number", "default": 0.5, "description": "仿真时长(s)"},
                        "step": {"type": "number", "default": 1e-5, "description": "仿真步长(s)"},
                    },
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "fundamental_freq": {"type": "number", "default": 60.0, "description": "基波频率(Hz)"},
                        "max_harmonic": {"type": "integer", "default": 50, "description": "最高谐波次数"},
                        "thd_limit": {"type": "number", "default": 5.0, "description": "THD限值(%)"},
                        "analysis_window": {
                            "type": "array",
                            "items": {"type": "number"},
                            "default": [0.4, 0.5],
                            "description": "分析时间窗口[s]",
                        },
                    },
                },
                "channels": {
                    "type": "object",
                    "properties": {
                        "voltage": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "电压通道列表",
                        },
                        "current": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "电流通道列表",
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "harmonic"},
                        "generate_report": {"type": "boolean", "default": True},
                        "export_spectrum": {"type": "boolean", "default": True},
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
                "duration": 0.5,
                "step": 1e-5,
            },
            "analysis": {
                "fundamental_freq": 60.0,
                "max_harmonic": 50,
                "thd_limit": 5.0,
                "analysis_window": [0.4, 0.5],
            },
            "channels": {
                "voltage": ["#Gen39.VT:0"],
                "current": ["#Gen39.IT:0"],
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "harmonic",
                "generate_report": True,
                "export_spectrum": True,
            },
        }

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行谐波分析"""
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
                base_model = load_or_fetch_model(model_config, config)
            log("INFO", f"模型: {base_model.name}")

            analysis_config = config.get("analysis", {})
            channels_config = config.get("channels", {})
            sim_config = config.get("simulation", {})
            output_config = config.get("output", {})

            fundamental = analysis_config.get("fundamental_freq", 60.0)
            max_harmonic = analysis_config.get("max_harmonic", 50)
            thd_limit = analysis_config.get("thd_limit", 5.0)
            analysis_window = analysis_config.get("analysis_window", [0.4, 0.5])

            voltage_channels = channels_config.get("voltage", [])
            current_channels = channels_config.get("current", [])

            emt_duration = sim_config.get("duration", 0.5)

            log("INFO", "谐波分析")
            log("INFO", f"基波频率: {fundamental} Hz")
            log("INFO", f"最高谐波次数: {max_harmonic}")
            log("INFO", f"THD限值: {thd_limit}%")
            log("INFO", f"分析窗口: {analysis_window[0]}-{analysis_window[1]}s")

            # 准备模型
            working_model = Model(deepcopy(base_model.toJSON()))

            # 运行EMT仿真
            log("INFO", f"运行EMT仿真 (时长: {emt_duration}s)...")
            job = run_emt(working_model, config)
            log("INFO", f"Job ID: {job.id}")

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

            # 谐波分析
            log("INFO", "谐波分析...")
            harmonic_results = self._analyze_harmonics(
                result, voltage_channels, current_channels,
                analysis_window, fundamental, max_harmonic, thd_limit, log
            )

            analyzed_voltage = len(harmonic_results.get("voltage", {}))
            analyzed_current = len(harmonic_results.get("current", {}))
            if analyzed_voltage + analyzed_current == 0:
                raise RuntimeError("未从EMT结果中提取到任何有效的谐波分析通道")

            # 汇总结果
            result_data = {
                "model": base_model.name,
                "fundamental_freq": fundamental,
                "max_harmonic": max_harmonic,
                "thd_limit": thd_limit,
                "analysis_window": analysis_window,
                "voltage_analysis": harmonic_results.get("voltage", {}),
                "current_analysis": harmonic_results.get("current", {}),
                "summary": harmonic_results.get("summary", {}),
            }

            # 导出结果
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "harmonic")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # JSON输出
            json_path = output_path / f"{prefix}_{timestamp}.json"
            with open(json_path, 'w') as f:
                json.dump(result_data, f, indent=2)
            artifacts.append(Artifact(type="json", path=str(json_path), size=json_path.stat().st_size, description="谐波分析结果"))

            # CSV输出
            csv_path = output_path / f"{prefix}_{timestamp}.csv"
            self._export_csv(harmonic_results, csv_path, voltage_channels, current_channels)
            artifacts.append(Artifact(type="csv", path=str(csv_path), size=csv_path.stat().st_size, description="谐波数据"))

            # 导出频谱数据
            if output_config.get("export_spectrum", True):
                spectrum_path = output_path / f"{prefix}_spectrum_{timestamp}.csv"
                self._export_spectrum(harmonic_results, spectrum_path)
                artifacts.append(Artifact(type="csv", path=str(spectrum_path), size=spectrum_path.stat().st_size, description="频谱数据"))

            # 生成报告
            if output_config.get("generate_report", True):
                report_path = output_path / f"{prefix}_report_{timestamp}.md"
                self._generate_report(result_data, report_path)
                artifacts.append(Artifact(type="markdown", path=str(report_path), size=report_path.stat().st_size, description="谐波分析报告"))

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
            )

        except (KeyError, AttributeError, ZeroDivisionError, RuntimeError, FileNotFoundError, ValueError, TypeError, ConnectionError, Exception) as e:
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

    def _analyze_harmonics(self, result, voltage_channels: List, current_channels: List,
                          analysis_window: List, fundamental: float, max_harmonic: int,
                          thd_limit: float, log_func) -> Dict:
        """分析谐波"""

        harmonic_results = {
            "voltage": {},
            "current": {},
            "summary": {
                "max_thd_voltage": 0.0,
                "max_thd_current": 0.0,
                "thd_violations": 0,
                "max_ripple_voltage": 0.0,
                "max_ripple_current": 0.0,
                "ripple_violations": 0,
            }
        }

        # 获取所有波形
        plots = list(result.getPlots())
        if not plots:
            log_func("WARNING", "没有波形数据")
            return harmonic_results

        plot_idx = 0  # 使用第一个plot

        # 分析电压通道
        for ch in voltage_channels:
            try:
                data = result.getPlotChannelData(plot_idx, ch)
                if not data or not data.get('y'):
                    log_func("WARNING", f"通道 {ch} 无数据")
                    continue

                xs = np.array(data['x'])
                ys = np.array(data['y'])

                # 提取分析窗口内的数据
                mask = (xs >= analysis_window[0]) & (xs <= analysis_window[1])
                t_window = xs[mask]
                y_window = ys[mask]

                if len(y_window) < 100:
                    log_func("WARNING", f"通道 {ch} 数据点不足")
                    continue

                # FFT分析
                harmonic_data = self._fft_analysis(t_window, y_window, fundamental, max_harmonic)

                harmonic_results["voltage"][ch] = harmonic_data

                # 根据信号类型处理指标
                signal_type = harmonic_data.get("signal_type", "ac")
                if signal_type == "dc":
                    # 直流系统：使用纹波系数
                    ripple = harmonic_data.get("ripple_factor", 0) or 0
                    harmonic_results["summary"]["max_ripple_voltage"] = max(
                        harmonic_results["summary"]["max_ripple_voltage"], ripple
                    )
                    # 直流系统纹波限值通常<1%
                    if ripple > 1.0:
                        harmonic_results["summary"]["ripple_violations"] += 1
                    log_func("INFO", f"  {ch} [DC]: 纹波={ripple:.4f}%")
                else:
                    # 交流系统：使用THD
                    thd = harmonic_data.get("thd", 0) or 0
                    harmonic_results["summary"]["max_thd_voltage"] = max(
                        harmonic_results["summary"]["max_thd_voltage"], thd
                    )
                    if thd > thd_limit:
                        harmonic_results["summary"]["thd_violations"] += 1
                    log_func("INFO", f"  {ch} [AC]: THD={thd:.2f}%")

            except (KeyError, AttributeError) as e:
                log_func("WARNING", f"通道 {ch} 分析失败: {e}")

        # 分析电流通道
        for ch in current_channels:
            try:
                data = result.getPlotChannelData(plot_idx, ch)
                if not data or not data.get('y'):
                    log_func("WARNING", f"通道 {ch} 无数据")
                    continue

                xs = np.array(data['x'])
                ys = np.array(data['y'])

                mask = (xs >= analysis_window[0]) & (xs <= analysis_window[1])
                t_window = xs[mask]
                y_window = ys[mask]

                if len(y_window) < 100:
                    log_func("WARNING", f"通道 {ch} 数据点不足")
                    continue

                harmonic_data = self._fft_analysis(t_window, y_window, fundamental, max_harmonic)

                harmonic_results["current"][ch] = harmonic_data

                # 根据信号类型处理指标
                signal_type = harmonic_data.get("signal_type", "ac")
                if signal_type == "dc":
                    # 直流系统：使用纹波系数
                    ripple = harmonic_data.get("ripple_factor", 0) or 0
                    harmonic_results["summary"]["max_ripple_current"] = max(
                        harmonic_results["summary"]["max_ripple_current"], ripple
                    )
                    if ripple > 1.0:
                        harmonic_results["summary"]["ripple_violations"] += 1
                    log_func("INFO", f"  {ch} [DC]: 纹波={ripple:.4f}%")
                else:
                    # 交流系统：使用THD
                    thd = harmonic_data.get("thd", 0) or 0
                    harmonic_results["summary"]["max_thd_current"] = max(
                        harmonic_results["summary"]["max_thd_current"], thd
                    )
                    if thd > thd_limit:
                        harmonic_results["summary"]["thd_violations"] += 1
                    log_func("INFO", f"  {ch} [AC]: THD={thd:.2f}%")

            except (KeyError, AttributeError) as e:
                log_func("WARNING", f"通道 {ch} 分析失败: {e}")

        return harmonic_results

    def _fft_analysis(self, t: np.ndarray, y: np.ndarray, fundamental: float,
                     max_harmonic: int) -> Dict:
        """FFT谐波分析"""

        # 采样参数
        dt = np.mean(np.diff(t))  # 采样间隔
        fs = 1.0 / dt  # 采样频率
        N = len(y)  # 数据点数

        # 去直流分量
        y_ac = y - np.mean(y)

        # FFT
        yf = np.fft.fft(y_ac)
        xf = np.fft.fftfreq(N, dt)  # 频率轴

        # 只取正频率
        positive_freq_idx = xf > 0
        freqs = xf[positive_freq_idx]
        amps = np.abs(yf[positive_freq_idx]) / N * 2  # 幅度谱

        # 找到基波
        fundamental_idx = np.argmin(np.abs(freqs - fundamental))
        fundamental_amp = amps[fundamental_idx]

        # 计算各次谐波
        harmonics = {}
        harmonic_power = 0.0

        for h in range(2, max_harmonic + 1):
            harmonic_freq = fundamental * h
            if harmonic_freq > fs / 2:  # 超过奈奎斯特频率
                break

            # 找到最接近的频点
            h_idx = np.argmin(np.abs(freqs - harmonic_freq))
            h_freq = freqs[h_idx]
            h_amp = amps[h_idx]

            # 谐波含量（相对于基波）- 仅在基波明显时计算
            if fundamental_amp > 1e-9:
                h_content = (h_amp / fundamental_amp * 100)
            else:
                h_content = 0.0

            harmonics[h] = {
                "frequency": round(h_freq, 2),
                "amplitude": round(h_amp, 6),
                "content_percent": round(h_content, 3),
            }

            # 累加谐波功率（用于THD/纹波计算）
            harmonic_power += (h_amp / 2) ** 2  # RMS的平方

        # 直流分量
        dc_component = np.mean(y)
        dc_abs = abs(dc_component)

        # 判断是否为直流系统
        # 条件：直流分量显著 (>0.1V) 且基波极小 (<0.01V)
        is_dc_system = (dc_abs > 0.1) and (fundamental_amp < 0.01)

        if is_dc_system:
            # 直流系统：计算纹波系数而非THD
            fundamental_rms = fundamental_amp / np.sqrt(2) if fundamental_amp > 0 else 0.0
            ac_rms = np.sqrt(harmonic_power)  # 纹波有效值（所有交流分量）

            # 纹波系数 = V_rms_ac / V_dc * 100%
            ripple_factor = (ac_rms / dc_abs * 100) if dc_abs > 0 else 0.0

            # THD标记为不适用（直流系统无基波概念）
            thd = None

            # 总有效值
            total_rms = np.sqrt(dc_abs ** 2 + ac_rms ** 2)
        else:
            # 交流系统：计算THD
            if fundamental_amp > 0:
                fundamental_rms = fundamental_amp / np.sqrt(2)
                thd = np.sqrt(harmonic_power) / fundamental_rms * 100
                total_rms = np.sqrt(fundamental_rms ** 2 + harmonic_power)
            else:
                fundamental_rms = 0.0
                thd = 0.0
                total_rms = np.sqrt(harmonic_power)

            ripple_factor = None

        result = {
            "sampling_rate": round(fs, 0),
            "data_points": N,
            "signal_type": "dc" if is_dc_system else "ac",
            "fundamental": {
                "frequency": round(fundamental, 2),
                "amplitude": round(fundamental_amp, 6),
                "rms": round(fundamental_rms, 6),
            },
            "harmonics": harmonics,
            "dc_component": round(dc_component, 6),
        }

        # 根据信号类型添加相应指标
        if is_dc_system:
            result["ripple_factor"] = round(ripple_factor, 4) if ripple_factor is not None else None
            result["thd"] = None  # 直流系统THD不适用
            result["ac_rms"] = round(ac_rms, 6)
        else:
            result["thd"] = round(thd, 3) if thd is not None else None
            result["ripple_factor"] = None

        result["total_rms"] = round(total_rms, 6)

        return result

    def _export_csv(self, harmonic_results: Dict, path: Path,
                   voltage_channels: List, current_channels: List):
        """导出CSV"""
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["channel_type", "channel_name", "signal_type", "fundamental_freq_hz",
                           "fundamental_rms", "dc_component", "thd_percent", "ripple_factor_percent",
                           "total_rms"])

            for ch, data in harmonic_results.get("voltage", {}).items():
                signal_type = data.get("signal_type", "ac")
                writer.writerow([
                    "voltage",
                    ch,
                    signal_type,
                    data.get("fundamental", {}).get("frequency", 0),
                    data.get("fundamental", {}).get("rms", 0),
                    data.get("dc_component", 0),
                    data.get("thd", "") if data.get("thd") is not None else "",
                    data.get("ripple_factor", "") if data.get("ripple_factor") is not None else "",
                    data.get("total_rms", 0),
                ])

            for ch, data in harmonic_results.get("current", {}).items():
                signal_type = data.get("signal_type", "ac")
                writer.writerow([
                    "current",
                    ch,
                    signal_type,
                    data.get("fundamental", {}).get("frequency", 0),
                    data.get("fundamental", {}).get("rms", 0),
                    data.get("dc_component", 0),
                    data.get("thd", "") if data.get("thd") is not None else "",
                    data.get("ripple_factor", "") if data.get("ripple_factor") is not None else "",
                    data.get("total_rms", 0),
                ])

    def _export_spectrum(self, harmonic_results: Dict, path: Path):
        """导出频谱数据"""
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["channel", "harmonic_order", "frequency_hz",
                           "amplitude", "content_percent"])

            for ch, data in harmonic_results.get("voltage", {}).items():
                for h, h_data in data.get("harmonics", {}).items():
                    writer.writerow([
                        ch,
                        h,
                        h_data.get("frequency", 0),
                        h_data.get("amplitude", 0),
                        h_data.get("content_percent", 0),
                    ])

            for ch, data in harmonic_results.get("current", {}).items():
                for h, h_data in data.get("harmonics", {}).items():
                    writer.writerow([
                        ch,
                        h,
                        h_data.get("frequency", 0),
                        h_data.get("amplitude", 0),
                        h_data.get("content_percent", 0),
                    ])

    def _generate_report(self, data: Dict, path: Path):
        """生成Markdown报告"""

        # 分析通道类型（交流/直流）
        has_ac = False
        has_dc = False
        voltage_data = data.get("voltage_analysis", {})
        current_data = data.get("current_analysis", {})

        for ch_data in list(voltage_data.values()) + list(current_data.values()):
            signal_type = ch_data.get("signal_type", "ac")
            if signal_type == "dc":
                has_dc = True
            else:
                has_ac = True

        lines = [
            "# 谐波分析报告",
            "",
            f"**模型**: {data['model']}",
            f"**基波频率**: {data['fundamental_freq']} Hz",
            f"**最高谐波次数**: {data['max_harmonic']}",
            f"**分析窗口**: {data['analysis_window'][0]}-{data['analysis_window'][1]}s",
            "",
            "## 概述",
            "",
        ]

        summary = data.get("summary", {})

        # 根据通道类型显示不同指标
        if has_ac:
            lines.extend([
                f"- 最大电压THD: {summary.get('max_thd_voltage', 0):.2f}%",
                f"- 最大电流THD: {summary.get('max_thd_current', 0):.2f}%",
                f"- THD限值: {data['thd_limit']}%",
                "",
            ])

        if has_dc:
            lines.extend([
                f"- 最大电压纹波系数: {summary.get('max_ripple_voltage', 0):.4f}%",
                f"- 最大电流纹波系数: {summary.get('max_ripple_current', 0):.4f}%",
                "",
            ])

        if summary.get('thd_violations', 0) > 0 or summary.get('ripple_violations', 0) > 0:
            lines.append("⚠️ **存在超标通道**")
        else:
            lines.append("✅ **所有通道满足要求**")

        # 电压分析
        lines.extend([
            "",
            "## 电压分析",
            "",
        ])

        if voltage_data:
            # 检查是否有直流通道
            has_dc_voltage = any(
                ch_data.get("signal_type") == "dc"
                for ch_data in voltage_data.values()
            )

            if has_dc_voltage:
                # 直流电压通道显示
                lines.extend([
                    "### 直流电压通道",
                    "",
                    "| 通道 | 直流电压(V) | 纹波系数(%) | 2次谐波 | 3次谐波 | 总有效值 | 状态 |",
                    "|------|-------------|-------------|---------|---------|----------|------|",
                ])

                for ch, ch_data in voltage_data.items():
                    if ch_data.get("signal_type") == "dc":
                        dc_val = ch_data.get("dc_component", 0)
                        ripple = ch_data.get("ripple_factor", 0) or 0
                        harmonics = ch_data.get("harmonics", {})
                        h2 = harmonics.get(2, {}).get("amplitude", 0)
                        h3 = harmonics.get(3, {}).get("amplitude", 0)
                        total_rms = ch_data.get("total_rms", 0)

                        # 直流系统纹波限值通常<1%
                        status = "✅" if ripple < 1.0 else "⚠️"

                        lines.append(f"| {ch} | {dc_val:.4f} | {ripple:.4f} | "
                                    f"{h2:.6f} | {h3:.6f} | {total_rms:.6f} | {status} |")

            # 交流电压通道显示
            ac_voltage = {k: v for k, v in voltage_data.items() if v.get("signal_type") != "dc"}
            if ac_voltage:
                lines.extend([
                    "",
                    "### 交流电压通道",
                    "",
                    "| 通道 | 基波有效值 | THD(%) | 3次 | 5次 | 7次 | 状态 |",
                    "|------|------------|--------|-----|-----|-----|------|",
                ])

                for ch, ch_data in ac_voltage.items():
                    fundamental_rms = ch_data.get("fundamental", {}).get("rms", 0)
                    thd = ch_data.get("thd", 0) or 0
                    harmonics = ch_data.get("harmonics", {})

                    h3 = harmonics.get(3, {}).get("content_percent", 0)
                    h5 = harmonics.get(5, {}).get("content_percent", 0)
                    h7 = harmonics.get(7, {}).get("content_percent", 0)

                    status = "✅" if thd < data['thd_limit'] else "⚠️"

                    lines.append(f"| {ch} | {fundamental_rms:.4f} | {thd:.3f} | "
                                f"{h3:.3f} | {h5:.3f} | {h7:.3f} | {status} |")

        # 电流分析
        lines.extend([
            "",
            "## 电流分析",
            "",
        ])

        if current_data:
            # 检查是否有直流通道
            has_dc_current = any(
                ch_data.get("signal_type") == "dc"
                for ch_data in current_data.values()
            )

            if has_dc_current:
                # 直流电流通道显示
                lines.extend([
                    "### 直流电流通道",
                    "",
                    "| 通道 | 直流电流(A) | 纹波系数(%) | 2次谐波 | 3次谐波 | 总有效值 | 状态 |",
                    "|------|-------------|-------------|---------|---------|----------|------|",
                ])

                for ch, ch_data in current_data.items():
                    if ch_data.get("signal_type") == "dc":
                        dc_val = ch_data.get("dc_component", 0)
                        ripple = ch_data.get("ripple_factor", 0) or 0
                        harmonics = ch_data.get("harmonics", {})
                        h2 = harmonics.get(2, {}).get("amplitude", 0)
                        h3 = harmonics.get(3, {}).get("amplitude", 0)
                        total_rms = ch_data.get("total_rms", 0)

                        status = "✅" if ripple < 1.0 else "⚠️"

                        lines.append(f"| {ch} | {dc_val:.4f} | {ripple:.4f} | "
                                    f"{h2:.6f} | {h3:.6f} | {total_rms:.6f} | {status} |")

            # 交流电流通道显示
            ac_current = {k: v for k, v in current_data.items() if v.get("signal_type") != "dc"}
            if ac_current:
                lines.extend([
                    "",
                    "### 交流电流通道",
                    "",
                    "| 通道 | 基波有效值 | THD(%) | 3次 | 5次 | 7次 | 状态 |",
                    "|------|------------|--------|-----|-----|-----|------|",
                ])

                for ch, ch_data in ac_current.items():
                    fundamental_rms = ch_data.get("fundamental", {}).get("rms", 0)
                    thd = ch_data.get("thd", 0) or 0
                    harmonics = ch_data.get("harmonics", {})

                    h3 = harmonics.get(3, {}).get("content_percent", 0)
                    h5 = harmonics.get(5, {}).get("content_percent", 0)
                    h7 = harmonics.get(7, {}).get("content_percent", 0)

                    status = "✅" if thd < data['thd_limit'] else "⚠️"

                    lines.append(f"| {ch} | {fundamental_rms:.4f} | {thd:.3f} | "
                                f"{h3:.3f} | {h5:.3f} | {h7:.3f} | {status} |")

        # 指标说明
        lines.extend([
            "",
            "## 指标说明",
            "",
        ])

        if has_ac:
            lines.extend([
                "### 交流系统指标",
                "",
                "- **THD**: 总谐波畸变率，各次谐波有效值与基波有效值之比",
                "- **3次/5次/7次**: 对应谐波含量百分比（相对于基波）",
                "- **IEEE 519标准**: 电压THD一般要求<5%",
                "",
            ])

        if has_dc:
            lines.extend([
                "### 直流系统指标",
                "",
                "- **纹波系数(Ripple Factor)**: 交流纹波有效值与直流分量之比",
                "  - 公式: RF = V<sub>rms(ac)</sub> / V<sub>dc</sub> × 100%",
                "  - 典型要求: <1%（高品质直流电源）",
                "- **直流系统THD**: 不适用（无基波概念）",
                "- **2次谐波**: DC/AC变换器开关纹波的主要分量",
                "",
            ])

        # 建议
        lines.extend([
            "",
            "## 建议",
            "",
        ])

        if summary.get('thd_violations', 0) > 0:
            lines.append("⚠️ 交流通道THD超标，建议:")
            lines.append("- 检查非线性负荷")
            lines.append("- 考虑配置有源电力滤波器(APF)")
            lines.append("- 评估谐波抑制措施")
        elif summary.get('ripple_violations', 0) > 0:
            lines.append("⚠️ 直流通道纹波超标，建议:")
            lines.append("- 增大DC-Link电容")
            lines.append("- 优化变换器控制策略")
            lines.append("- 增加LC滤波器")
        else:
            lines.append("✅ 所有通道指标满足要求，无需额外措施。")

        path.write_text("\n".join(lines), encoding="utf-8")
