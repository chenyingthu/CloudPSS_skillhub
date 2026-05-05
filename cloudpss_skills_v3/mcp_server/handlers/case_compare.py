"""
案例对比 (Case Compare) Handler

处理多个算例的结果对比分析。
"""

import logging
from typing import Any
from dataclasses import dataclass

from mcp.types import TextContent

from cloudpss_skills_v3.core.task_store import get_task_store, TaskStatus

logger = logging.getLogger(__name__)


@dataclass
class ComparisonMetric:
    """对比指标"""
    name: str
    unit: str
    baseline: float
    values: list[float]
    differences: list[float]
    percent_changes: list[float]


def calculate_comparison(baseline_data: dict, compare_data_list: list[dict],
                        metrics: list[str]) -> dict:
    """计算对比结果

    Args:
        baseline_data: 基准案例数据
        compare_data_list: 对比案例数据列表
        metrics: 对比指标列表

    Returns:
        对比结果字典
    """
    results = {}

    metric_mapping = {
        "voltage": ("voltage_min", "voltage_max", "pu"),
        "loading": ("branch_count", "loading", "%"),
        "losses": ("losses", "losses", "MW"),
        "iterations": ("iterations", "iterations", "次"),
        "compute_time": ("compute_time", "compute_time", "秒")
    }

    for metric in metrics:
        if metric in metric_mapping:
            key, display_name, unit = metric_mapping[metric]

            baseline_val = baseline_data.get(key, 0)
            values = [d.get(key, 0) for d in compare_data_list]

            diffs = [v - baseline_val for v in values]
            pct_changes = [
                ((v - baseline_val) / baseline_val * 100) if baseline_val != 0 else 0
                for v in values
            ]

            results[metric] = {
                "name": display_name,
                "unit": unit,
                "baseline": baseline_val,
                "values": values,
                "differences": diffs,
                "percent_changes": pct_changes
            }

    return results


def format_comparison_table(comparison: dict, case_names: list[str]) -> str:
    """格式化对比表格"""
    lines = ["| 指标 | 单位 | 基准 | " + " | ".join(case_names) + " |"]
    lines.append("|------|------|------|" + "|".join(["------"] * len(case_names)) + "|")

    for metric_key, metric_data in comparison.items():
        name = metric_data["name"]
        unit = metric_data["unit"]
        baseline = metric_data["baseline"]
        values = metric_data["values"]
        pct_changes = metric_data["percent_changes"]

        row = f"| {name} | {unit} | {baseline:.3f} |"
        for val, pct in zip(values, pct_changes):
            change_indicator = ""
            if pct > 0:
                change_indicator = f" ↗️ +{pct:.1f}%"
            elif pct < 0:
                change_indicator = f" ↘️ {pct:.1f}%"
            row += f" {val:.3f}{change_indicator} |"

        lines.append(row)

    return "\n".join(lines)


async def handle_case_compare(arguments: dict[str, Any]) -> list[TextContent]:
    """处理案例对比请求

    Args:
        arguments: 包含 case_ids, metrics 等参数

    Returns:
        MCP TextContent 列表
    """
    logger.info(f"执行 case_compare: {arguments}")

    case_ids = arguments.get("case_ids", [])
    metrics = arguments.get("metrics", ["voltage", "loading", "losses"])

    if len(case_ids) < 2:
        return [TextContent(
            type="text",
            text="❌ 参数错误: 至少需要提供 2 个案例 ID 进行对比"
        )]

    try:
        task_store = get_task_store()

        # 获取所有案例的任务信息
        tasks = []
        for case_id in case_ids:
            task = task_store.get_task(case_id)
            if not task:
                return [TextContent(
                    type="text",
                    text=f"❌ 未找到案例: {case_id}"
                )]

            if task.status != TaskStatus.COMPLETED:
                return [TextContent(
                    type="text",
                    text=f"⏳ 案例尚未完成: {case_id} (状态: {task.status.value})"
                )]

            tasks.append(task)

        # 第一个案例作为基准
        baseline = tasks[0]
        comparisons = tasks[1:]

        # 提取结果数据
        baseline_data = baseline.result_data or {}
        compare_data_list = [t.result_data or {} for t in comparisons]

        # 计算对比
        comparison = calculate_comparison(
            baseline_data,
            compare_data_list,
            metrics
        )

        # 生成对比表格
        case_names = [t.case_name for t in comparisons]
        comparison_table = format_comparison_table(comparison, case_names)

        # 生成差异总结
        summary_lines = []
        for metric_key, metric_data in comparison.items():
            max_change = max(abs(p) for p in metric_data["percent_changes"])
            if max_change > 10:
                summary_lines.append(f"⚠️ **{metric_data['name']}** 变化显著（最大 {max_change:.1f}%）")
            elif max_change > 5:
                summary_lines.append(f"ℹ️ **{metric_data['name']}** 有中等程度变化（最大 {max_change:.1f}%）")
            else:
                summary_lines.append(f"✅ **{metric_data['name']}** 基本稳定（最大变化 {max_change:.1f}%）")

        summary = "\n".join(summary_lines) if summary_lines else "✅ 各指标差异不大"

        return [TextContent(
            type="text",
            text=f"""📊 案例对比分析

**基准案例**: {baseline.case_name} (`{baseline.task_id}`)
**对比案例**: {len(comparisons)} 个

## 差异总结

{summary}

## 详细对比

{comparison_table}

## 各案例信息

| 案例 | 模型 | 状态 | 计算时间 |
|------|------|------|----------|
| **{baseline.case_name}** (基准) | `{baseline.model_rid}` | ✅ 完成 | {baseline_data.get('compute_time', 'N/A')}s |
{"\n".join([f"| {t.case_name} | `{t.model_rid}` | ✅ 完成 | {t.result_data.get('compute_time', 'N/A')}s |" for t in comparisons])}

💡 **提示**: 变化超过 10% 的指标需要重点关注。"""
        )]

    except Exception as e:
        logger.error(f"对比案例时出错: {e}")
        return [TextContent(
            type="text",
            text=f"❌ 对比失败: {str(e)}"
        )]
