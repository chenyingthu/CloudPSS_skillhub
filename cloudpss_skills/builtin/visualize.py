"""
Visualization Skill

可视化 - 生成波形图和结果图表。
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from cloudpss_skills.core import (
    Artifact,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    register,
)
from cloudpss_skills.core.auth_utils import setup_auth
from cloudpss_skills.core.utils import fetch_job_with_result

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
                        "data_file": {
                            "type": "string",
                            "description": "本地数据文件路径",
                        },
                        "data": {
                            "type": "object",
                            "description": "直接传入的数据（用于管道内传递）",
                        },
                        "format": {"enum": ["csv", "json"], "default": "csv"},
                    },
                },
                "plot": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "enum": ["time_series", "bar", "scatter", "comparison"],
                            "default": "time_series",
                        },
                        "channels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "要绘制的通道",
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
                        "include_raw_data": {
                            "type": "boolean",
                            "default": False,
                            "description": "是否在结果中包含原始波形数据",
                        },
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "source": {
                "job_id": "",
                "data": None,  # 用于 pipeline 直接传递数据
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
        has_direct_data = isinstance(source.get("data"), dict)

        if not has_job_id and not has_data_file and not has_direct_data:
            result.add_error(
                "必须提供 source.job_id、source.data_file 或 source.data 之一"
            )
            result.add_error("  job_id示例: 'job-12345678-abcd-1234-efgh-123456789012'")
            result.add_error("  data_file示例: './results/waveforms.csv'")
            result.add_error(
                "  data: 可在 pipeline 中直接传递上游 skill 的 result_data"
            )

        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行可视化"""
        import matplotlib

        matplotlib.use("Agg")  # 非交互式后端
        import matplotlib.font_manager as fm
        import matplotlib.pyplot as plt

        # Configure CJK font support
        cjk_fonts = [f.name for f in fm.fontManager.ttflist if "Noto Sans CJK" in f.name or "Noto Serif CJK" in f.name or "WenQuanYi" in f.name or "AR PL" in f.name]
        if cjk_fonts:
            plt.rcParams["font.sans-serif"] = cjk_fonts + plt.rcParams["font.sans-serif"]
            plt.rcParams["axes.unicode_minus"] = False

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
            log("INFO", "认证成功")

            source_config = config.get("source", {})
            plot_config = config.get("plot", {})
            output_config = config.get("output", {})

            # 获取数据
            data = None

            # 优先级 1: 直接数据（pipeline 传递）
            if source_config.get("data"):
                log("INFO", "使用直接传入的数据")
                pipeline_data = source_config["data"]

                if isinstance(pipeline_data, dict) and "buses" in pipeline_data:
                    buses = pipeline_data.get("buses", [])
                    if buses:
                        data = {"bus_names": [], "voltage_pu": []}
                        for bus in buses:
                            name = bus.get("Bus", bus.get("node_id", "Unknown"))
                            vm = bus.get("Vm", bus.get("voltage_mag", 0))
                            data["bus_names"].append(name)
                            data["voltage_pu"].append(float(vm) if vm else 0)
                        log("INFO", f"从 pipeline 数据提取 {len(buses)} 个母线电压")
                    else:
                        raise RuntimeError("pipeline 数据中没有母线数据")
                elif isinstance(pipeline_data, dict) and "time" in pipeline_data:
                    data = pipeline_data
                else:
                    raise RuntimeError(
                        f"不支持的 pipeline 数据格式: {list(pipeline_data.keys())}"
                    )

            # 优先级 2: 从 CloudPSS 获取
            elif source_config.get("job_id"):
                # 从CloudPSS获取
                log("INFO", "从CloudPSS获取数据...")

                job_id = source_config["job_id"]
                _job, result = fetch_job_with_result(job_id, config)

                if result is None:
                    raise RuntimeError("任务结果为空")

                # 提取数据 - 支持 EMT 波形和潮流计算结果
                data = None

                # 尝试 EMT 波形数据
                try:
                    plots = list(result.getPlots())
                    if plots:
                        # 从第一个 plot 提取
                        channel_names = result.getPlotChannelNames(0)
                        target_channels = plot_config.get("channels") or channel_names
                        missing_requested_channels = (
                            [
                                channel
                                for channel in target_channels
                                if channel not in channel_names
                            ]
                            if plot_config.get("channels")
                            else []
                        )

                        data = {"time": []}
                        for channel in target_channels:
                            if channel in channel_names:
                                channel_data = result.getPlotChannelData(0, channel)
                                if channel_data:
                                    if not data["time"]:
                                        data["time"] = channel_data.get("x", [])
                                    data[channel] = channel_data.get("y", [])

                        if plot_config.get("channels") and len(data) == 1:
                            raise RuntimeError(
                                "未找到任何可绘制的目标通道"
                                + (
                                    f": {', '.join(missing_requested_channels)}"
                                    if missing_requested_channels
                                    else ""
                                )
                            )
                except AttributeError:
                    # PowerFlowResult 没有 getPlots() 方法，尝试潮流计算结果
                    log("INFO", "检测到潮流计算结果，尝试提取母线数据...")
                    pass

                # 如果是潮流计算结果（没有 plots）
                if data is None:
                    # 1. SDK PowerFlowResult - 通过方法访问
                    if hasattr(result, "getBuses"):
                        from cloudpss_skills.core.utils import parse_cloudpss_table

                        buses_raw = result.getBuses()
                        if buses_raw:
                            bus_rows = parse_cloudpss_table(buses_raw)
                            if bus_rows:
                                data = {"bus_names": [], "voltage_pu": []}
                                for bus in bus_rows:
                                    name = bus.get("Bus", bus.get("node_id", "Unknown"))
                                    vm = bus.get("Vm", bus.get("voltage_mag", 0))
                                    data["bus_names"].append(name)
                                    data["voltage_pu"].append(float(vm) if vm else 0)
                                log(
                                    "INFO",
                                    f"从 SDK 结果提取 {len(bus_rows)} 个母线电压",
                                )
                            else:
                                raise RuntimeError("潮流计算结果中没有母线数据")
                        else:
                            raise RuntimeError("潮流计算结果 buses 表为空")
                    # 2. 已处理的数据 dict（向后兼容：skill 直接返回的 SkillResult.data）
                    elif isinstance(getattr(result, "data", None), dict):
                        result_data = result.data
                        if "buses" in result_data:
                            buses = result_data.get("buses", [])
                            if buses:
                                data = {"bus_names": [], "voltage_pu": []}
                                for bus in buses:
                                    name = bus.get("Bus", bus.get("node_id", "Unknown"))
                                    vm = bus.get("Vm", bus.get("voltage_mag", 0))
                                    data["bus_names"].append(name)
                                    data["voltage_pu"].append(float(vm) if vm else 0)
                                log("INFO", f"提取 {len(buses)} 个母线电压数据")
                            else:
                                raise RuntimeError("潮流计算结果中没有母线数据")
                        else:
                            raise RuntimeError("没有波形数据且非潮流计算结果")
                    else:
                        raise RuntimeError("没有波形数据且非潮流计算结果")

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
                with open(filepath, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        for key, value in row.items():
                            if key not in data:
                                data[key] = []
                            try:
                                data[key].append(float(value))
                            except ValueError:
                                data[key].append(value)

            if not data:
                raise RuntimeError("没有获取到有效数据")

            # 潮流计算结果没有 time 字段，但要确保有电压数据
            if "bus_names" in data and "voltage_pu" in data:
                log("INFO", f"潮流计算结果：{len(data['bus_names'])} 个母线")
            elif not data.get("time"):
                raise RuntimeError("没有获取到有效数据")

            log("INFO", f"获取到 {len(data)} 个通道")

            # Unified time_data definition (may be empty for power flow results)
            time_data = data.get("time", [])

            # 应用时间范围（仅适用于 EMT 波形数据）
            time_range = plot_config.get("time_range", {})
            if data.get("time") and (
                time_range.get("start") is not None or time_range.get("end") is not None
            ):
                start = time_range.get("start", float("-inf"))
                end = time_range.get("end", float("inf"))

                time_data = data.get("time", [])
                indices = [i for i, t in enumerate(time_data) if start <= t <= end]

                for key in data:
                    data[key] = [data[key][i] for i in indices]

                log("INFO", f"时间范围筛选后：{len(data['time'])} 个点")

            # 绘制图表
            log("INFO", "生成图表...")

            fig_width = output_config.get("width", 12)
            fig_height = output_config.get("height", 6)
            plot_type = plot_config.get("type", "time_series")

            # 检测是否为潮流计算结果（母线电压数据）
            is_power_flow = "bus_names" in data and "voltage_pu" in data

            if is_power_flow:
                # 潮流计算：绘制母线电压条形图
                fig, ax = plt.subplots(figsize=(fig_width, fig_height))

                bus_names = data["bus_names"]
                voltage_pu = data["voltage_pu"]

                # 条形图
                bars = ax.bar(
                    range(len(bus_names)), voltage_pu, color="steelblue", alpha=0.7
                )

                # 添加电压参考线
                ax.axhline(
                    y=1.0, color="green", linestyle="--", linewidth=1, label="1.0 pu"
                )
                ax.axhline(
                    y=0.95, color="orange", linestyle=":", linewidth=1, label="0.95 pu"
                )
                ax.axhline(
                    y=1.05, color="orange", linestyle=":", linewidth=1, label="1.05 pu"
                )

                # 设置标题和标签
                ax.set_title(plot_config.get("title", "Bus Voltage Profile"))
                ax.set_xlabel("Bus")
                ax.set_ylabel("Voltage (pu)")
                ax.set_xticks(range(len(bus_names)))
                ax.set_xticklabels(bus_names, rotation=90, fontsize=8)
                ax.legend(loc="upper right")
                ax.grid(True, alpha=0.3, axis="y")
                ax.set_ylim(0.8, 1.2)  # 电压范围

                plotted_channels = ["voltage_pu"]
                log("INFO", f"绘制 {len(bus_names)} 个母线电压条形图")
            else:
                # EMT 波形：绘制折线图
                fig, ax = plt.subplots(figsize=(fig_width, fig_height))

                time_data = data.get("time", range(len(data[list(data.keys())[0]])))

                channels_to_plot = plot_config.get("channels", [])
                if not channels_to_plot:
                    # 如果没有指定，绘制所有非 time 通道
                    channels_to_plot = [k for k in data.keys() if k != "time"]

                plotted_channels = []

                for channel in channels_to_plot:
                    if channel in data:
                        ax.plot(time_data, data[channel], label=channel, linewidth=1.5)
                        plotted_channels.append(channel)

                if not plotted_channels:
                    plt.close(fig)
                    raise RuntimeError("未找到任何可绘制的目标通道")

                ax.set_title(plot_config.get("title", "Waveform"))
                ax.set_xlabel(plot_config.get("xlabel", "Time (s)"))
                ax.set_ylabel(plot_config.get("ylabel", "Value"))
                ax.legend(loc="best")
                ax.grid(True, alpha=0.3)

            # 保存
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)

            filename = output_config.get(
                "filename", f"waveform_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            fmt = output_config.get("format", "png")
            # Pipeline may pass non-image formats (e.g. "json") from parent config.
            # Fall back to "png" for unsupported formats.
            supported_formats = {"png", "jpg", "jpeg", "svg", "pdf", "eps", "webp"}
            if fmt not in supported_formats:
                log("WARNING", f"输出格式 '{fmt}' 不支持图片，使用默认格式 png")
                fmt = "png"
            if Path(filename).suffix.lower() == f".{fmt}":
                filepath = output_path / filename
            else:
                filepath = output_path / f"{filename}.{fmt}"

            dpi = output_config.get("dpi", 150)
            plt.savefig(filepath, dpi=dpi, bbox_inches="tight")
            plt.close()

            artifacts.append(
                Artifact(
                    type=fmt,
                    path=str(filepath),
                    size=filepath.stat().st_size,
                    description="波形图表",
                )
            )

            log("INFO", f"图表已保存: {filepath}")

            result_data = {
                "channels": len(plotted_channels),
                "plotted_channels": plotted_channels,
                "data_points": len(time_data) if time_data else len(data.get("voltage_pu", [])),
                "output": str(filepath),
            }

            if output_config.get("include_raw_data", False):
                result_data["raw_data"] = data

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
                    "stage": "visualize",
                },
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )
