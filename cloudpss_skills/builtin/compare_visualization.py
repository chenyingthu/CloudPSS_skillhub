"""
Compare Visualization Skill

对比可视化 - 生成多场景仿真结果的对比图表。
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register

logger = logging.getLogger(__name__)


@register
class CompareVisualizationSkill(SkillBase):
    """对比可视化技能 - 生成多场景对比图表"""

    @property
    def name(self) -> str:
        return "compare_visualization"

    @property
    def description(self) -> str:
        return "生成多场景仿真结果的对比可视化图表，包括时序对比图、指标柱状图、热力图等"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "sources"],
            "properties": {
                "skill": {"type": "string", "const": "compare_visualization"},
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "token_file": {"type": "string", "default": ".cloudpss_token"},
                    },
                },
                "sources": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "job_id": {"type": "string"},
                            "label": {"type": "string"},
                            "color": {"type": "string"},
                        },
                        "required": ["job_id"],
                    },
                    "minItems": 2,
                    "description": "要对比的仿真任务列表，至少2个"
                },
                "compare": {
                    "type": "object",
                    "properties": {
                        "channels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "要对比的通道列表"
                        },
                        "metrics": {
                            "type": "array",
                            "items": {"enum": ["max", "min", "mean", "rms", "peak"]},
                            "default": ["max", "min", "mean"],
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
                "charts": {
                    "type": "object",
                    "properties": {
                        "time_series": {
                            "type": "object",
                            "properties": {
                                "enabled": {"type": "boolean", "default": True},
                                "per_channel": {"type": "boolean", "default": False},
                                "title": {"type": "string"},
                            },
                        },
                        "bar_chart": {
                            "type": "object",
                            "properties": {
                                "enabled": {"type": "boolean", "default": True},
                                "group_by": {"enum": ["metric", "source"], "default": "metric"},
                                "title": {"type": "string"},
                            },
                        },
                        "heatmap": {
                            "type": "object",
                            "properties": {
                                "enabled": {"type": "boolean", "default": False},
                                "metric": {"type": "string", "default": "max"},
                                "title": {"type": "string"},
                            },
                        },
                        "radar": {
                            "type": "object",
                            "properties": {
                                "enabled": {"type": "boolean", "default": False},
                                "title": {"type": "string"},
                            },
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["png", "pdf", "svg"], "default": "png"},
                        "path": {"type": "string", "default": "./results/"},
                        "filename_prefix": {"type": "string", "default": "compare"},
                        "dpi": {"type": "integer", "default": 150},
                        "width": {"type": "number", "default": 14},
                        "height": {"type": "number", "default": 8},
                        "combine": {"type": "boolean", "default": False},
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "sources": [],
            "compare": {
                "channels": [],
                "metrics": ["max", "min", "mean"],
            },
            "charts": {
                "time_series": {
                    "enabled": True,
                    "per_channel": False,
                    "title": "多场景时序对比",
                },
                "bar_chart": {
                    "enabled": True,
                    "group_by": "metric",
                    "title": "指标对比",
                },
                "heatmap": {
                    "enabled": False,
                    "metric": "max",
                    "title": "通道-场景热力图",
                },
                "radar": {
                    "enabled": False,
                    "title": "多维度雷达图",
                },
            },
            "output": {
                "format": "png",
                "path": "./results/",
                "filename_prefix": "compare",
                "dpi": 150,
                "width": 14,
                "height": 8,
                "combine": False,
            },
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        """验证配置"""
        result = ValidationResult(valid=True)

        sources = config.get("sources", [])

        if len(sources) < 2:
            result.add_error("至少需要2个仿真任务进行对比")
            result.add_error("  示例: [{job_id: 'abc123', label: '基态'}, {job_id: 'def456', label: '故障态'}]")

        for i, source in enumerate(sources):
            job_id = source.get("job_id", "")
            if not job_id:
                result.add_error(f"sources[{i}] 必须包含有效的job_id")

        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行对比可视化"""
        from cloudpss import Job, setToken
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.gridspec import GridSpec

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

            # 2. 获取配置
            sources = config["sources"]
            compare_config = config.get("compare", {})
            charts_config = config.get("charts", {})
            output_config = config.get("output", {})

            target_channels = compare_config.get("channels", [])
            metrics = compare_config.get("metrics", ["max", "min", "mean"])
            time_range = compare_config.get("time_range", {})

            log("INFO", f"对比 {len(sources)} 个仿真结果")

            # 3. 获取所有任务数据
            all_data = []
            for i, source in enumerate(sources):
                job_id = source["job_id"]
                label = source.get("label", f"场景{i+1}")
                color = source.get("color")

                log("INFO", f"获取任务: {label} ({job_id})")

                try:
                    job = Job.fetch(job_id)
                    result = job.result

                    if result is None:
                        log("WARNING", f"  -> 任务 {label} 结果为空，跳过")
                        continue

                    # 提取EMT波形数据
                    if hasattr(result, 'getPlots'):
                        plots = list(result.getPlots())
                        task_data = {
                            "label": label,
                            "job_id": job_id,
                            "color": color,
                            "channels": {},
                        }

                        for plot_idx in range(len(plots)):
                            channel_names = result.getPlotChannelNames(plot_idx)

                            for channel in channel_names:
                                if target_channels and channel not in target_channels:
                                    continue

                                channel_data = result.getPlotChannelData(plot_idx, channel)
                                if channel_data:
                                    x_data = channel_data.get('x', [])
                                    y_data = channel_data.get('y', [])

                                    # 应用时间范围筛选
                                    if time_range and (time_range.get("start") is not None or time_range.get("end") is not None):
                                        start_t = time_range.get("start", float('-inf'))
                                        end_t = time_range.get("end", float('inf'))
                                        indices = [i for i, t in enumerate(x_data) if start_t <= t <= end_t]
                                        x_data = [x_data[i] for i in indices]
                                        y_data = [y_data[i] for i in indices]

                                    # 计算指标
                                    if y_data:
                                        arr = np.array(y_data)
                                        channel_metrics = {}
                                        if "max" in metrics:
                                            channel_metrics["max"] = float(np.max(arr))
                                        if "min" in metrics:
                                            channel_metrics["min"] = float(np.min(arr))
                                        if "mean" in metrics:
                                            channel_metrics["mean"] = float(np.mean(arr))
                                        if "rms" in metrics:
                                            channel_metrics["rms"] = float(np.sqrt(np.mean(arr**2)))
                                        if "peak" in metrics:
                                            channel_metrics["peak"] = float(np.max(np.abs(arr)))

                                        task_data["channels"][channel] = {
                                            "time": x_data,
                                            "values": y_data,
                                            "metrics": channel_metrics,
                                        }

                        all_data.append(task_data)
                        log("INFO", f"  -> 获取 {len(task_data['channels'])} 个通道")

                    else:
                        log("WARNING", f"  -> 任务 {label} 不是EMT结果类型，跳过")

                except (KeyError, AttributeError, ConnectionError) as e:
                    log("ERROR", f"  -> 获取失败: {e}")

            if len(all_data) < 2:
                raise RuntimeError("成功获取的任务数不足2个，无法进行对比")

            # 4. 生成图表
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)

            filename_prefix = output_config.get("filename_prefix", "compare")
            fmt = output_config.get("format", "png")
            dpi = output_config.get("dpi", 150)
            fig_width = output_config.get("width", 14)
            fig_height = output_config.get("height", 8)
            combine = output_config.get("combine", False)

            generated_files = []

            # 图表1: 时序对比图
            ts_config = charts_config.get("time_series", {})
            if ts_config.get("enabled", True):
                log("INFO", "生成时序对比图...")

                per_channel = ts_config.get("per_channel", False)
                ts_title = ts_config.get("title", "多场景时序对比")

                if per_channel:
                    # 每个通道一张图
                    all_channel_names = set()
                    for task in all_data:
                        all_channel_names.update(task["channels"].keys())

                    for channel in sorted(all_channel_names):
                        fig, ax = plt.subplots(figsize=(fig_width, fig_height))

                        for task in all_data:
                            if channel in task["channels"]:
                                ch_data = task["channels"][channel]
                                color = task.get("color")
                                ax.plot(ch_data["time"], ch_data["values"],
                                       label=task["label"], linewidth=1.5, color=color)

                        ax.set_title(f"{ts_title} - {channel}")
                        ax.set_xlabel("时间 (s)")
                        ax.set_ylabel("幅值")
                        ax.legend(loc="best")
                        ax.grid(True, alpha=0.3)

                        filepath = output_path / f"{filename_prefix}_timeseries_{channel}.{fmt}"
                        plt.savefig(filepath, dpi=dpi, bbox_inches='tight')
                        plt.close()

                        generated_files.append(filepath)
                        log("INFO", f"  -> 已保存: {filepath.name}")
                else:
                    # 所有通道在一个图中（按通道分subplot）
                    all_channel_names = set()
                    for task in all_data:
                        all_channel_names.update(task["channels"].keys())

                    n_channels = len(all_channel_names)
                    if n_channels > 0:
                        n_cols = min(2, n_channels)
                        n_rows = (n_channels + n_cols - 1) // n_cols

                        fig = plt.figure(figsize=(fig_width * n_cols, fig_height * n_rows / 2))
                        gs = GridSpec(n_rows, n_cols, figure=fig)

                        for idx, channel in enumerate(sorted(all_channel_names)):
                            ax = fig.add_subplot(gs[idx // n_cols, idx % n_cols])

                            for task in all_data:
                                if channel in task["channels"]:
                                    ch_data = task["channels"][channel]
                                    color = task.get("color")
                                    ax.plot(ch_data["time"], ch_data["values"],
                                           label=task["label"], linewidth=1.2, color=color)

                            ax.set_title(channel)
                            ax.set_xlabel("时间 (s)")
                            ax.set_ylabel("幅值")
                            ax.legend(loc="best", fontsize=8)
                            ax.grid(True, alpha=0.3)

                        fig.suptitle(ts_title, fontsize=14, fontweight='bold')
                        plt.tight_layout()

                        filepath = output_path / f"{filename_prefix}_timeseries.{fmt}"
                        plt.savefig(filepath, dpi=dpi, bbox_inches='tight')
                        plt.close()

                        generated_files.append(filepath)
                        log("INFO", f"  -> 时序对比图已保存: {filepath.name}")

            # 图表2: 指标柱状图
            bar_config = charts_config.get("bar_chart", {})
            if bar_config.get("enabled", True):
                log("INFO", "生成指标对比柱状图...")

                group_by = bar_config.get("group_by", "metric")
                bar_title = bar_config.get("title", "指标对比")

                # 准备数据
                all_channel_names = set()
                for task in all_data:
                    all_channel_names.update(task["channels"].keys())

                if group_by == "metric":
                    # 每个指标一张图
                    for metric in metrics:
                        fig, ax = plt.subplots(figsize=(fig_width, fig_height))

                        # 准备数据
                        x_labels = []
                        data_by_task = {task["label"]: [] for task in all_data}

                        for channel in sorted(all_channel_names):
                            x_labels.append(channel)
                            for task in all_data:
                                val = task["channels"].get(channel, {}).get("metrics", {}).get(metric)
                                data_by_task[task["label"]].append(val if val is not None else 0)

                        # 绘制分组柱状图
                        x = np.arange(len(x_labels))
                        width = 0.8 / len(all_data)

                        for i, task in enumerate(all_data):
                            offset = (i - len(all_data) / 2 + 0.5) * width
                            color = task.get("color")
                            ax.bar(x + offset, data_by_task[task["label"]], width,
                                  label=task["label"], color=color)

                        ax.set_xlabel("通道")
                        ax.set_ylabel(metric.upper())
                        ax.set_title(f"{bar_title} - {metric.upper()}")
                        ax.set_xticks(x)
                        ax.set_xticklabels(x_labels, rotation=45, ha='right')
                        ax.legend(loc="best")
                        ax.grid(True, alpha=0.3, axis='y')

                        plt.tight_layout()
                        filepath = output_path / f"{filename_prefix}_bar_{metric}.{fmt}"
                        plt.savefig(filepath, dpi=dpi, bbox_inches='tight')
                        plt.close()

                        generated_files.append(filepath)
                        log("INFO", f"  -> {metric}指标柱状图已保存: {filepath.name}")

                else:  # group_by == "source"
                    # 每个场景一张图
                    for task in all_data:
                        fig, ax = plt.subplots(figsize=(fig_width, fig_height))

                        x_labels = []
                        data_by_metric = {m: [] for m in metrics}

                        for channel in sorted(all_channel_names):
                            x_labels.append(channel)
                            channel_metrics = task["channels"].get(channel, {}).get("metrics", {})
                            for metric in metrics:
                                val = channel_metrics.get(metric)
                                data_by_metric[metric].append(val if val is not None else 0)

                        x = np.arange(len(x_labels))
                        width = 0.8 / len(metrics)

                        for i, metric in enumerate(metrics):
                            offset = (i - len(metrics) / 2 + 0.5) * width
                            ax.bar(x + offset, data_by_metric[metric], width, label=metric.upper())

                        ax.set_xlabel("通道")
                        ax.set_ylabel("数值")
                        ax.set_title(f"{bar_title} - {task['label']}")
                        ax.set_xticks(x)
                        ax.set_xticklabels(x_labels, rotation=45, ha='right')
                        ax.legend(loc="best")
                        ax.grid(True, alpha=0.3, axis='y')

                        plt.tight_layout()
                        filepath = output_path / f"{filename_prefix}_bar_{task['label']}.{fmt}"
                        plt.savefig(filepath, dpi=dpi, bbox_inches='tight')
                        plt.close()

                        generated_files.append(filepath)
                        log("INFO", f"  -> {task['label']}柱状图已保存: {filepath.name}")

            # 图表3: 热力图
            heatmap_config = charts_config.get("heatmap", {})
            if heatmap_config.get("enabled", False):
                log("INFO", "生成热力图...")

                heatmap_metric = heatmap_config.get("metric", "max")
                heatmap_title = heatmap_config.get("title", "通道-场景热力图")

                all_channel_names = sorted(set(
                    ch for task in all_data
                    for ch in task["channels"].keys()
                ))
                all_channel_names = sorted(all_channel_names)

                # 构建数据矩阵
                heatmap_data = []
                task_labels = []

                for task in all_data:
                    row = []
                    for channel in all_channel_names:
                        val = task["channels"].get(channel, {}).get("metrics", {}).get(heatmap_metric)
                        row.append(val if val is not None else 0)
                    heatmap_data.append(row)
                    task_labels.append(task["label"])

                fig, ax = plt.subplots(figsize=(fig_width, fig_height))

                im = ax.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')

                # 设置刻度
                ax.set_xticks(np.arange(len(all_channel_names)))
                ax.set_yticks(np.arange(len(task_labels)))
                ax.set_xticklabels(all_channel_names, rotation=45, ha='right')
                ax.set_yticklabels(task_labels)

                # 添加数值标注
                for i in range(len(task_labels)):
                    for j in range(len(all_channel_names)):
                        text = ax.text(j, i, f'{heatmap_data[i][j]:.2f}',
                                      ha="center", va="center", color="black", fontsize=8)

                ax.set_title(f"{heatmap_title} ({heatmap_metric.upper()})")
                fig.colorbar(im, ax=ax, label=heatmap_metric.upper())

                plt.tight_layout()
                filepath = output_path / f"{filename_prefix}_heatmap.{fmt}"
                plt.savefig(filepath, dpi=dpi, bbox_inches='tight')
                plt.close()

                generated_files.append(filepath)
                log("INFO", f"  -> 热力图已保存: {filepath.name}")

            # 图表4: 雷达图
            radar_config = charts_config.get("radar", {})
            if radar_config.get("enabled", False):
                log("INFO", "生成雷达图...")

                radar_title = radar_config.get("title", "多维度雷达图")

                # 选择前6个通道作为维度
                all_channel_names = set()
                for task in all_data:
                    all_channel_names.update(task["channels"].keys())
                radar_channels = sorted(list(all_channel_names))[:6]

                if len(radar_channels) >= 3:
                    fig, ax = plt.subplots(figsize=(fig_height, fig_height), subplot_kw=dict(projection='polar'))

                    # 设置角度
                    angles = np.linspace(0, 2 * np.pi, len(radar_channels), endpoint=False).tolist()
                    angles += angles[:1]  # 闭合

                    for task in all_data:
                        values = []
                        for channel in radar_channels:
                            # 使用归一化后的峰值
                            val = task["channels"].get(channel, {}).get("metrics", {}).get("peak", 0)
                            values.append(val)

                        # 归一化
                        max_val = max(values) if max(values) > 0 else 1
                        values = [v / max_val for v in values]
                        values += values[:1]  # 闭合

                        color = task.get("color")
                        ax.plot(angles, values, 'o-', linewidth=2, label=task["label"], color=color)
                        ax.fill(angles, values, alpha=0.1, color=color)

                    ax.set_xticks(angles[:-1])
                    ax.set_xticklabels(radar_channels)
                    ax.set_ylim(0, 1)
                    ax.set_title(radar_title, y=1.08)
                    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

                    filepath = output_path / f"{filename_prefix}_radar.{fmt}"
                    plt.savefig(filepath, dpi=dpi, bbox_inches='tight')
                    plt.close()

                    generated_files.append(filepath)
                    log("INFO", f"  -> 雷达图已保存: {filepath.name}")

            # 5. 生成产物记录
            for filepath in generated_files:
                artifacts.append(Artifact(
                    type=fmt,
                    path=str(filepath),
                    size=filepath.stat().st_size,
                    description=f"对比图表: {filepath.name}"
                ))

            log("INFO", f"对比可视化完成，生成 {len(generated_files)} 张图表")

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "sources": len(all_data),
                    "channels": len(all_channel_names) if 'all_channel_names' in dir() else 0,
                    "charts_generated": len(generated_files),
                    "output_path": str(output_path),
                },
                artifacts=artifacts,
                logs=logs,
                metrics={
                    "sources": len(all_data),
                    "charts": len(generated_files),
                },
            )

        except (KeyError, AttributeError, ConnectionError) as e:
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
