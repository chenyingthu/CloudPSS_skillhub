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
                base_model = Model.fetch(model_config["rid"])
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
            job = working_model.runEMT()
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

        except Exception as e:
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

                thd = harmonic_data.get("thd", 0)
                harmonic_results["summary"]["max_thd_voltage"] = max(
                    harmonic_results["summary"]["max_thd_voltage"], thd
                )
                if thd > thd_limit:
                    harmonic_results["summary"]["thd_violations"] += 1

                log_func("INFO", f"  {ch}: THD={thd:.2f}%")

            except Exception as e:
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

                thd = harmonic_data.get("thd", 0)
                harmonic_results["summary"]["max_thd_current"] = max(
                    harmonic_results["summary"]["max_thd_current"], thd
                )
                if thd > thd_limit:
                    harmonic_results["summary"]["thd_violations"] += 1

                log_func("INFO", f"  {ch}: THD={thd:.2f}%")

            except Exception as e:
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

            # 谐波含量（相对于基波）
            h_content = (h_amp / fundamental_amp * 100) if fundamental_amp > 0 else 0

            harmonics[h] = {
                "frequency": round(h_freq, 2),
                "amplitude": round(h_amp, 6),
                "content_percent": round(h_content, 3),
            }

            # 累加谐波功率（用于THD计算）
            harmonic_power += (h_amp / 2) ** 2  # RMS的平方

        # 计算THD
        if fundamental_amp > 0:
            fundamental_rms = fundamental_amp / np.sqrt(2)
            thd = np.sqrt(harmonic_power) / fundamental_rms * 100
            # 总有效值
            total_rms = np.sqrt(fundamental_rms ** 2 + harmonic_power)
        else:
            fundamental_rms = 0.0
            thd = 0.0
            total_rms = np.sqrt(harmonic_power)

        return {
            "sampling_rate": round(fs, 0),
            "data_points": N,
            "fundamental": {
                "frequency": round(fundamental, 2),
                "amplitude": round(fundamental_amp, 6),
                "rms": round(fundamental_rms, 6),
            },
            "harmonics": harmonics,
            "thd": round(thd, 3),
            "total_rms": round(total_rms, 6),
            "dc_component": round(np.mean(y), 6),
        }

    def _export_csv(self, harmonic_results: Dict, path: Path,
                   voltage_channels: List, current_channels: List):
        """导出CSV"""
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["channel_type", "channel_name", "fundamental_freq_hz",
                           "fundamental_rms", "thd_percent", "dc_component"])

            for ch, data in harmonic_results.get("voltage", {}).items():
                writer.writerow([
                    "voltage",
                    ch,
                    data.get("fundamental", {}).get("frequency", 0),
                    data.get("fundamental", {}).get("rms", 0),
                    data.get("thd", 0),
                    data.get("dc_component", 0),
                ])

            for ch, data in harmonic_results.get("current", {}).items():
                writer.writerow([
                    "current",
                    ch,
                    data.get("fundamental", {}).get("frequency", 0),
                    data.get("fundamental", {}).get("rms", 0),
                    data.get("thd", 0),
                    data.get("dc_component", 0),
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
        lines = [
            "# 谐波分析报告",
            "",
            f"**模型**: {data['model']}",
            f"**基波频率**: {data['fundamental_freq']} Hz",
            f"**最高谐波次数**: {data['max_harmonic']}",
            f"**THD限值**: {data['thd_limit']}%",
            f"**分析窗口**: {data['analysis_window'][0]}-{data['analysis_window'][1]}s",
            "",
            "## 概述",
            "",
        ]

        summary = data.get("summary", {})

        lines.extend([
            f"- 最大电压THD: {summary.get('max_thd_voltage', 0):.2f}%",
            f"- 最大电流THD: {summary.get('max_thd_current', 0):.2f}%",
            f"- THD超标通道数: {summary.get('thd_violations', 0)}",
            "",
        ])

        if summary.get('thd_violations', 0) > 0:
            lines.append("⚠️ **存在THD超标通道**")
        else:
            lines.append("✅ **所有通道THD满足要求**")

        lines.extend([
            "",
            "## 电压谐波分析",
            "",
            "| 通道 | 基波有效值 | THD(%) | 3次 | 5次 | 7次 | 状态 |",
            "|------|------------|--------|-----|-----|-----|------|",
        ])

        voltage_data = data.get("voltage_analysis", {})
        for ch, ch_data in voltage_data.items():
            fundamental_rms = ch_data.get("fundamental", {}).get("rms", 0)
            thd = ch_data.get("thd", 0)
            harmonics = ch_data.get("harmonics", {})

            h3 = harmonics.get(3, {}).get("content_percent", 0)
            h5 = harmonics.get(5, {}).get("content_percent", 0)
            h7 = harmonics.get(7, {}).get("content_percent", 0)

            status = "✅" if thd < data['thd_limit'] else "⚠️"

            lines.append(f"| {ch} | {fundamental_rms:.4f} | {thd:.3f} | "
                        f"{h3:.3f} | {h5:.3f} | {h7:.3f} | {status} |")

        lines.extend([
            "",
            "## 电流谐波分析",
            "",
            "| 通道 | 基波有效值 | THD(%) | 3次 | 5次 | 7次 | 状态 |",
            "|------|------------|--------|-----|-----|-----|------|",
        ])

        current_data = data.get("current_analysis", {})
        for ch, ch_data in current_data.items():
            fundamental_rms = ch_data.get("fundamental", {}).get("rms", 0)
            thd = ch_data.get("thd", 0)
            harmonics = ch_data.get("harmonics", {})

            h3 = harmonics.get(3, {}).get("content_percent", 0)
            h5 = harmonics.get(5, {}).get("content_percent", 0)
            h7 = harmonics.get(7, {}).get("content_percent", 0)

            status = "✅" if thd < data['thd_limit'] else "⚠️"

            lines.append(f"| {ch} | {fundamental_rms:.4f} | {thd:.3f} | "
                        f"{h3:.3f} | {h5:.3f} | {h7:.3f} | {status} |")

        lines.extend([
            "",
            "## 指标说明",
            "",
            "- **THD**: 总谐波畸变率，各次谐波有效值与基波有效值之比",
            "- **3次/5次/7次**: 对应谐波含量百分比",
            "- IEEE 519标准**: 电压THD一般要求<5%",
            "",
            "## 建议",
            "",
        ])

        if summary.get('thd_violations', 0) > 0:
            lines.append("⚠️ THD超标，建议:")
            lines.append("- 检查非线性负荷")
            lines.append("- 考虑配置滤波器")
            lines.append("- 评估谐波抑制措施")
        else:
            lines.append("✅ 谐波水平满足要求，无需额外措施。")

        path.write_text("\n".join(lines), encoding="utf-8")
