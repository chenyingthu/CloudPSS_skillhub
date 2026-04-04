"""
Result Comparison Skill

结果对比 - 对比多次仿真结果。
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register

logger = logging.getLogger(__name__)


@register
class ResultCompareSkill(SkillBase):
    """结果对比技能"""

    @property
    def name(self) -> str:
        return "result_compare"

    @property
    def description(self) -> str:
        return "对比多次仿真结果，生成差异分析报告"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "sources"],
            "properties": {
                "skill": {"type": "string", "const": "result_compare"},
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
                        },
                        "required": ["job_id"],
                    },
                    "description": "要对比的仿真任务列表"
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
                            "items": {"enum": ["max", "min", "mean", "rms"]},
                            "default": ["max", "min"],
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
                        "format": {"enum": ["json", "markdown"], "default": "markdown"},
                        "path": {"type": "string", "default": "./results/"},
                        "filename": {"type": "string", "default": "comparison_report"},
                        "timestamp": {"type": "boolean", "default": True},
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
                "metrics": ["max", "min"],
            },
            "output": {
                "format": "markdown",
                "path": "./results/",
                "filename": "comparison_report",
                "timestamp": True,
            },
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        """验证配置 - 后处理技能不需要model.rid"""
        result = ValidationResult(valid=True)  # 不调用super()，避免model.rid检查

        sources = config.get("sources", [])

        if len(sources) < 2:
            result.add_error("至少需要2个仿真任务进行对比")
            result.add_error("  示例: [{job_id: 'abc123', label: 'Case A'}, {job_id: 'def456', label: 'Case B'}]")

        for i, source in enumerate(sources):
            job_id = source.get("job_id", "")
            if not job_id or job_id in ["abc123", "def456", ""]:
                result.add_error(f"sources[{i}] 必须包含有效的job_id")
                result.add_error(f"  当前值: '{job_id}'")

        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行结果对比"""
        from cloudpss import Job, setToken

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
                if not token_path.exists():
                    raise FileNotFoundError(f"Token文件不存在: {token_file}")
                token = token_path.read_text().strip()

            setToken(token)
            log("INFO", "认证成功")

            # 2. 获取所有任务结果
            sources = config["sources"]
            compare_config = config.get("compare", {})
            target_channels = compare_config.get("channels", [])
            metrics = compare_config.get("metrics", ["max", "min"])

            log("INFO", f"对比 {len(sources)} 个仿真结果")

            all_results = []
            for source in sources:
                job_id = source["job_id"]
                label = source.get("label", job_id[:8])

                log("INFO", f"获取任务: {label} ({job_id})")

                try:
                    job = Job.fetch(job_id)
                    result = job.result

                    if result is None:
                        log("WARNING", f"  -> 任务 {label} 结果为空")
                        continue

                    # 检查结果类型并处理
                    result_type = type(result).__name__
                    log("INFO", f"  -> 结果类型: {result_type}")

                    channels_data = {}

                    # 对于EMT结果（有getPlots方法）
                    if hasattr(result, 'getPlots'):
                        plots = list(result.getPlots())
                        log("INFO", f"  -> 波形分组数: {len(plots)}")

                        for plot_idx in range(len(plots)):
                            channel_names = result.getPlotChannelNames(plot_idx)

                            for channel in channel_names:
                                # 如果指定了通道列表，只获取指定的
                                if target_channels and channel not in target_channels:
                                    continue

                                channel_data = result.getPlotChannelData(plot_idx, channel)
                                if channel_data:
                                    y_values = channel_data.get('y', [])

                                    # 计算指标
                                    import numpy as np
                                    channel_metrics = {}
                                    if y_values:
                                        arr = np.array(y_values)
                                        if "max" in metrics:
                                            channel_metrics["max"] = float(np.max(arr))
                                        if "min" in metrics:
                                            channel_metrics["min"] = float(np.min(arr))
                                        if "mean" in metrics:
                                            channel_metrics["mean"] = float(np.mean(arr))
                                        if "rms" in metrics:
                                            channel_metrics["rms"] = float(np.sqrt(np.mean(arr**2)))

                                    channels_data[channel] = channel_metrics
                    else:
                        # 对于潮流等其他结果类型，记录日志
                        log("WARNING", f"  -> 结果类型 {result_type} 暂不支持通道数据提取")
                        # 尝试获取基本数据
                        try:
                            data_attrs = [attr for attr in dir(result) if not attr.startswith('_') and not callable(getattr(result, attr))]
                            log("INFO", f"  -> 可用属性: {data_attrs[:5]}")
                        except Exception as e:
                            # 异常已捕获，无需额外处理
                            logger.debug(f"忽略预期异常: {e}")

                    all_results.append({
                        "label": label,
                        "job_id": job_id,
                        "channels": channels_data,
                    })

                    log("INFO", f"  -> 获取 {len(channels_data)} 个通道")

                except (KeyError, AttributeError) as e:
                    log("ERROR", f"  -> 获取失败: {e}")

            # 3. 生成对比分析
            log("INFO", "生成对比分析...")

            # 收集所有通道名
            all_channels = set()
            for r in all_results:
                all_channels.update(r["channels"].keys())

            # 对比每个通道
            comparison = {}
            for channel in sorted(all_channels):
                channel_comparison = {}

                for metric in metrics:
                    values = {}
                    for r in all_results:
                        val = r["channels"].get(channel, {}).get(metric)
                        if val is not None:
                            values[r["label"]] = val

                    if values:
                        channel_comparison[metric] = {
                            "values": values,
                            "max": max(values.values()),
                            "min": min(values.values()),
                            "diff": max(values.values()) - min(values.values()),
                        }

                comparison[channel] = channel_comparison

            # 4. 导出结果
            output_config = config.get("output", {})
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)

            filename = output_config.get("filename", "comparison_report")
            use_timestamp = output_config.get("timestamp", True)
            output_format = output_config.get("format", "markdown")

            if use_timestamp:
                filename += f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            filename += ".md" if output_format == "markdown" else ".json"

            filepath = output_path / filename

            if output_format == "markdown":
                self._export_markdown(filepath, all_results, comparison, metrics)
            else:
                self._export_json(filepath, all_results, comparison)

            artifacts.append(Artifact(
                type=output_format,
                path=str(filepath),
                size=filepath.stat().st_size,
                description="结果对比报告"
            ))

            log("INFO", f"对比报告已保存: {filepath}")

            # 检查是否有有效对比数据
            if len(all_channels) == 0:
                log("ERROR", "没有有效的通道数据进行对比")
                return SkillResult(
                    skill_name=self.name,
                    status=SkillStatus.FAILED,
                    start_time=start_time,
                    end_time=datetime.now(),
                    data={"error": "没有有效的通道数据进行对比"},
                    artifacts=artifacts,
                    logs=logs,
                )

            # 构建结果数据
            result_data = {
                "timestamp": datetime.now().isoformat(),
                "sources": sources,
                "compared_channels": len(all_channels),
                "comparison": comparison,
            }

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
                metrics={
                    "sources": len(sources),
                    "channels": len(all_channels),
                },
            )

        except (KeyError, AttributeError, RuntimeError, FileNotFoundError, ValueError) as e:
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

    def _export_markdown(self, filepath: Path, results: List[Dict], comparison: Dict, metrics: List[str]):
        """导出为Markdown格式"""
        lines = [
            "# 仿真结果对比报告",
            "",
            f"生成时间: {datetime.now().isoformat()}",
            "",
            "## 对比概览",
            "",
            f"- 对比任务数: {len(results)}",
            f"- 对比通道数: {len(comparison)}",
            "",
        ]

        # 任务列表
        lines.extend(["## 任务列表", ""])
        for r in results:
            lines.append(f"- **{r['label']}**: `{r['job_id']}`")
        lines.append("")

        # 通道对比表
        lines.extend(["## 通道对比", ""])

        for channel, channel_data in sorted(comparison.items()):
            lines.append(f"### {channel}")
            lines.append("")

            for metric, metric_data in channel_data.items():
                lines.append(f"**{metric.upper()}**:")
                lines.append("")
                lines.append("| 任务 | 值 |")
                lines.append("|------|-----|")

                for label, value in metric_data["values"].items():
                    lines.append(f"| {label} | {value:.6f} |")

                lines.append(f"")
                lines.append(f"- 范围: [{metric_data['min']:.6f}, {metric_data['max']:.6f}]")
                lines.append(f"- 差值: {metric_data['diff']:.6f}")
                lines.append("")

        filepath.write_text("\n".join(lines), encoding='utf-8')

    def _export_json(self, filepath: Path, results: List[Dict], comparison: Dict):
        """导出为JSON格式"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "comparison": comparison,
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
