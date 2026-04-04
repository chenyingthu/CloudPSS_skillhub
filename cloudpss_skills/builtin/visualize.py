"""
Visualization Skill

可视化 - 生成波形图和结果图表。
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register

logger = logging.getLogger(__name__)


@register
class VisualizeSkill(SkillBase):
    """可视化技能"""

    @property
    def name(self) -> str:
        return "visualize"

    @property
    def description(self) -> str:
        return "生成波形图和结果可视化图表"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill"],
            "anyOf": [
                {"required": ["source", "job_id"]},
                {"required": ["source", "data_file"]},
            ],
            "properties": {
                "skill": {"type": "string", "const": "visualize"},
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "token_file": {"type": "string", "default": ".cloudpss_token"},
                    },
                },
                "source": {
                    "type": "object",
                    "properties": {
                        "job_id": {"type": "string", "description": "仿真任务ID"},
                        "data_file": {"type": "string", "description": "本地数据文件路径"},
                        "format": {"enum": ["csv", "json"], "default": "csv"},
                    },
                },
                "plot": {
                    "type": "object",
                    "properties": {
                        "type": {"enum": ["time_series", "bar", "scatter", "comparison"], "default": "time_series"},
                        "channels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "要绘制的通道"
                        },
                        "title": {"type": "string"},
                        "xlabel": {"type": "string"},
                        "ylabel": {"type": "string"},
                        "time_range": {
                            "type": "object",
                            "properties": {
                                "start": {"type": "number"},
                                "end": {"type": "number"},
                            },
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["png", "pdf", "svg"], "default": "png"},
                        "path": {"type": "string", "default": "./results/"},
                        "filename": {"type": "string"},
                        "dpi": {"type": "integer", "default": 150},
                        "width": {"type": "number", "default": 12},
                        "height": {"type": "number", "default": 6},
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "source": {
                "job_id": "",  # 默认空，需要用户填写
                "format": "csv",
            },
            "plot": {
                "type": "time_series",
                "channels": [],
                "title": "Waveform",
                "xlabel": "Time (s)",
                "ylabel": "Value",
            },
            "output": {
                "format": "png",
                "path": "./results/",
                "dpi": 150,
                "width": 12,
                "height": 6,
            },
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        """验证配置 - 后处理技能不需要model.rid"""
        result = ValidationResult(valid=True)  # 不调用super()，避免model.rid检查

        source = config.get("source", {})

        has_job_id = source.get("job_id") and source.get("job_id") != ""
        has_data_file = source.get("data_file")

        if not has_job_id and not has_data_file:
            result.add_error("必须提供source.job_id或source.data_file")
            result.add_error("  job_id示例: 'job-12345678-abcd-1234-efgh-123456789012'")
            result.add_error("  data_file示例: './results/waveforms.csv'")

        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行可视化"""
        from cloudpss import Job, setToken
        import matplotlib
        matplotlib.use('Agg')  # 非交互式后端
        import matplotlib.pyplot as plt

        start_time = datetime.now()
        logs = []
        artifacts = []

        def log(level: str, message: str):
            logs.append(LogEntry(
                timestamp=datetime.now(),
                level=level,
                message=message
            ))
            getattr(logger, level.lower(), logger.info)(message)

        try:
            source_config = config.get("source", {})
            plot_config = config.get("plot", {})
            output_config = config.get("output", {})

            # 获取数据
            data = None

            if source_config.get("job_id"):
                # 从CloudPSS获取
                log("INFO", "从CloudPSS获取数据...")

                auth = config.get("auth", {})
                token = auth.get("token")
                if not token:
                    raise ValueError("未找到CloudPSS token，请提供auth.token或创建.cloudpss_token文件")

                setToken(token)

                job_id = source_config["job_id"]
                job = Job.fetch(job_id)
                result = job.result

                if result is None:
                    raise RuntimeError("任务结果为空")

                # 提取数据
                plots = list(result.getPlots())
                if not plots:
                    raise RuntimeError("没有波形数据")

                # 从第一个plot提取
                channel_names = result.getPlotChannelNames(0)
                target_channels = plot_config.get("channels", channel_names)

                data = {"time": []}
                for channel in target_channels:
                    if channel in channel_names:
                        channel_data = result.getPlotChannelData(0, channel)
                        if channel_data:
                            if not data["time"]:
                                data["time"] = channel_data.get("x", [])
                            data[channel] = channel_data.get("y", [])

            elif source_config.get("data_file"):
                # 从本地文件读取
                data_file = source_config["data_file"]
                log("INFO", f"从本地文件读取: {data_file}")

                filepath = Path(data_file)
                if not filepath.exists():
                    raise FileNotFoundError(f"数据文件不存在: {data_file}")

                # 读取CSV
                import csv
                data = {}
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        for key, value in row.items():
                            if key not in data:
                                data[key] = []
                            try:
                                data[key].append(float(value))
                            except ValueError:
                                data[key].append(value)

            if not data or not data.get("time"):
                raise RuntimeError("没有获取到有效数据")

            log("INFO", f"获取到 {len(data)} 个通道")

            # 应用时间范围
            time_range = plot_config.get("time_range", {})
            if time_range.get("start") is not None or time_range.get("end") is not None:
                start = time_range.get("start", float('-inf'))
                end = time_range.get("end", float('inf'))

                time_data = data.get("time", [])
                indices = [i for i, t in enumerate(time_data) if start <= t <= end]

                for key in data:
                    data[key] = [data[key][i] for i in indices]

                log("INFO", f"时间范围筛选后: {len(data['time'])} 个点")

            # 绘制图表
            log("INFO", "生成图表...")

            fig_width = output_config.get("width", 12)
            fig_height = output_config.get("height", 6)
            fig, ax = plt.subplots(figsize=(fig_width, fig_height))

            plot_type = plot_config.get("type", "time_series")
            time_data = data.get("time", range(len(data[list(data.keys())[0]])))

            channels_to_plot = plot_config.get("channels", [])
            if not channels_to_plot:
                # 如果没有指定，绘制所有非time通道
                channels_to_plot = [k for k in data.keys() if k != "time"]

            for channel in channels_to_plot:
                if channel in data:
                    ax.plot(time_data, data[channel], label=channel, linewidth=1.5)

            ax.set_title(plot_config.get("title", "Waveform"))
            ax.set_xlabel(plot_config.get("xlabel", "Time (s)"))
            ax.set_ylabel(plot_config.get("ylabel", "Value"))
            ax.legend(loc="best")
            ax.grid(True, alpha=0.3)

            # 保存
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)

            filename = output_config.get("filename", f"waveform_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            fmt = output_config.get("format", "png")
            filepath = output_path / f"{filename}.{fmt}"

            dpi = output_config.get("dpi", 150)
            plt.savefig(filepath, dpi=dpi, bbox_inches='tight')
            plt.close()

            artifacts.append(Artifact(
                type=fmt,
                path=str(filepath),
                size=filepath.stat().st_size,
                description="波形图表"
            ))

            log("INFO", f"图表已保存: {filepath}")

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "channels": len(channels_to_plot),
                    "data_points": len(time_data),
                    "output": str(filepath),
                },
                artifacts=artifacts,
                logs=logs,
            )

        except (KeyError, AttributeError) as e:
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
