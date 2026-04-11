"""
Waveform Export Skill

从已有仿真任务导出波形数据。
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

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
class WaveformExportSkill(SkillBase):
    """波形导出技能"""

    @property
    def name(self) -> str:
        return "waveform_export"

    @property
    def description(self) -> str:
        return "从仿真结果导出波形数据"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "source"],
            "properties": {
                "skill": {"type": "string", "const": "waveform_export"},
                "source": {
                    "type": "object",
                    "required": ["job_id"],
                    "properties": {
                        "job_id": {"type": "string", "description": "仿真任务ID"},
                        "auth": {
                            "type": "object",
                            "properties": {
                                "token": {"type": "string"},
                                "token_file": {"type": "string"},
                            },
                        },
                    },
                },
                "export": {
                    "type": "object",
                    "properties": {
                        "plots": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "要导出的波形分组索引，空表示全部",
                        },
                        "channels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "要导出的通道名称，空表示全部",
                        },
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
                        "format": {"enum": ["csv", "json"], "default": "csv"},
                        "path": {"type": "string", "default": "./results/"},
                        "filename": {"type": "string"},
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "source": {
                "job_id": "",
            },
            "export": {
                "plots": [],
                "channels": [],
            },
            "output": {
                "format": "csv",
                "path": "./results/",
            },
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        """验证配置 - 后处理技能不需要model.rid"""
        result = ValidationResult(valid=True)  # 不调用super()，避免model.rid检查

        source = config.get("source", {})
        job_id = source.get("job_id", "")

        if not job_id or job_id in ["", "your_job_id_here"]:
            result.add_error("必须提供有效的 source.job_id")
            result.add_error("  示例: 'job-12345678-abcd-1234-efgh-123456789012'")
            result.add_warning("提示: 从CloudPSS平台获取仿真任务的Job ID")

        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行导出"""

        start_time = datetime.now()
        logs = []
        artifacts = []

        def log(level: str, message: str):
            logs.append(
                LogEntry(timestamp=datetime.now(), level=level, message=message)
            )
            getattr(logger, level.lower(), logger.info)(message)

        try:
            # 1. 认证
            setup_auth(config)
            log("INFO", "认证成功")

            source_config = config.get("source", {})
            auth = source_config.get("auth", {})

            # 2. 获取任务
            job_id = source_config["job_id"]
            log("INFO", f"获取任务: {job_id}")
            job, result = fetch_job_with_result(job_id, {"auth": auth})

            # 3. 检查结果
            if job.status() != 1:
                raise RuntimeError(f"任务未完成或失败，状态: {job.status()}")

            # 4. 获取结果
            log("INFO", "提取结果...")
            plots = list(result.getPlots())
            log("INFO", f"波形分组数: {len(plots)}")

            # 5. 确定要导出的分组
            export_config = config.get("export", {})
            plot_indices = export_config.get("plots", [])
            if not plot_indices:
                plot_indices = list(range(len(plots)))

            # 6. 导出
            output_config = config.get("output", {})
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)

            output_format = output_config.get("format", "csv")
            filename = (
                output_config.get("filename") or f"waveforms_{job_id}.{output_format}"
            )
            filepath = output_path / filename

            # 导出数据
            exported_data = []
            exported_channel_count = 0
            for plot_idx in plot_indices:
                if plot_idx >= len(plots):
                    continue

                plot = plots[plot_idx]
                channel_names = result.getPlotChannelNames(plot_idx)

                # 过滤通道
                filter_channels = export_config.get("channels", [])
                if filter_channels:
                    channel_names = [c for c in channel_names if c in filter_channels]

                plot_data = {
                    "plot_index": plot_idx,
                    "plot_key": plot.get("key"),
                    "channels": {},
                }

                for channel in channel_names:
                    channel_data = result.getPlotChannelData(plot_idx, channel)
                    if channel_data:
                        x_data = channel_data.get("x", [])
                        y_data = channel_data.get("y", [])

                        # 时间范围切片
                        time_range = export_config.get("time_range", {})
                        start_t = time_range.get("start")
                        end_t = time_range.get("end")

                        if start_t is not None or end_t is not None:
                            filtered_x = []
                            filtered_y = []
                            for x, y in zip(x_data, y_data):
                                if start_t is not None and x < start_t:
                                    continue
                                if end_t is not None and x > end_t:
                                    continue
                                filtered_x.append(x)
                                filtered_y.append(y)
                            x_data = filtered_x
                            y_data = filtered_y

                        plot_data["channels"][channel] = {
                            "x": x_data,
                            "y": y_data,
                        }
                        exported_channel_count += 1

                if plot_data["channels"]:
                    exported_data.append(plot_data)

            if exported_channel_count == 0:
                raise RuntimeError("未找到任何可导出的目标波形通道")

            # 写入文件
            if output_format == "json":
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump({"job_id": job_id, "plots": exported_data}, f, indent=2)
            else:  # csv
                import csv

                with open(filepath, "w", newline="", encoding="utf-8") as f:
                    for plot_data in exported_data:
                        channels = plot_data["channels"]
                        if not channels:
                            continue

                        first_channel = list(channels.values())[0]
                        x_data = first_channel.get("x", [])

                        writer = csv.writer(f)
                        writer.writerow(["time"] + list(channels.keys()))

                        for i in range(len(x_data)):
                            row = [x_data[i]]
                            for ch_name in channels:
                                y_data = channels[ch_name].get("y", [])
                                row.append(y_data[i] if i < len(y_data) else "")
                            writer.writerow(row)

            artifacts.append(
                Artifact(
                    type=output_format,
                    path=str(filepath),
                    size=filepath.stat().st_size,
                    description=f"波形数据 ({len(exported_data)}个分组)",
                )
            )

            log("INFO", f"导出完成: {filepath}")

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "job_id": job_id,
                    "plot_count": len(plots),
                    "exported_plots": len(exported_data),
                    "exported_channels": exported_channel_count,
                },
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
            log("ERROR", str(e))
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
