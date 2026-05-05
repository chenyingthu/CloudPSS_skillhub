"""
参数扫描 (Parameter Sweep) Handler

处理批量参数扫描分析。
"""

import logging
import asyncio
from typing import Any

from mcp.types import TextContent

from cloudpss_skills_v3.core.cloudpss_client import get_client
from cloudpss_skills_v3.core.task_store import TaskStatus, get_task_store
from cloudpss_skills_v3.mcp_server.handlers.powerflow import handle_powerflow_run

logger = logging.getLogger(__name__)


async def handle_parameter_sweep(arguments: dict[str, Any]) -> list[TextContent]:
    """处理参数扫描请求

    Args:
        arguments: 包含 base_case, parameter, range, parallel 等参数

    Returns:
        MCP TextContent 列表
    """
    logger.info(f"执行 parameter_sweep: {arguments}")

    base_case = arguments.get("base_case")
    parameter = arguments.get("parameter")
    param_range = arguments.get("range", [])
    parallel = arguments.get("parallel", True)

    if not base_case or not parameter or not param_range:
        return [TextContent(
            type="text",
            text="❌ 参数错误: 需要提供 base_case, parameter 和 range"
        )]

    try:
        task_store = get_task_store()

        # 获取基准案例信息
        base_task = task_store.get_task(base_case)
        if not base_task:
            return [TextContent(
                type="text",
                text=f"❌ 未找到基准案例: {base_case}"
            )]

        # 创建扫描任务列表
        sweep_tasks = []
        for value in param_range:
            case_name = f"{base_task.case_name}-{parameter}={value}"
            sweep_tasks.append({
                "case_name": case_name,
                "model_rid": base_task.model_rid,
                "parameter_value": value,
                "wait": False  # 异步提交
            })

        # 执行扫描
        if parallel:
            # 并行执行
            logger.info(f"并行执行 {len(sweep_tasks)} 个扫描任务")
            results = await asyncio.gather(*[
                handle_powerflow_run(task)
                for task in sweep_tasks
            ])
        else:
            # 串行执行
            logger.info(f"串行执行 {len(sweep_tasks)} 个扫描任务")
            results = []
            for task in sweep_tasks:
                result = await handle_powerflow_run(task)
                results.append(result)

        # 收集任务ID
        task_ids = []
        import re
        for result in results:
            text = result[0].text
            match = re.search(r'任务 ID\*\*: (task-\S+)', text)
            if match:
                task_ids.append(match.group(1))

        # 等待所有任务完成
        logger.info(f"等待 {len(task_ids)} 个扫描任务完成")
        completed_tasks = []

        for task_id in task_ids:
            # 轮询等待任务完成
            max_attempts = 60  # 最多等待60秒
            for _ in range(max_attempts):
                task = task_store.get_task(task_id)
                if task and task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                    completed_tasks.append(task)
                    break
                await asyncio.sleep(1)

        # 分析结果
        successful = [t for t in completed_tasks if t.status == TaskStatus.COMPLETED]
        failed = [t for t in completed_tasks if t.status == TaskStatus.FAILED]

        # 提取关键结果数据
        sweep_results = []
        for task in successful:
            result_data = task.result_data or {}
            sweep_results.append({
                "case_name": task.case_name,
                "voltage_min": result_data.get("voltage_min", 0),
                "voltage_max": result_data.get("voltage_max", 0),
                "iterations": result_data.get("iterations", 0),
                "compute_time": result_data.get("compute_time", 0)
            })

        # 生成结果表格
        table_lines = [
            "| 参数值 | 电压最小 | 电压最大 | 迭代次数 | 计算时间 |",
            "|--------|----------|----------|----------|----------|"
        ]

        for i, result in enumerate(sweep_results):
            param_value = param_range[i] if i < len(param_range) else "N/A"
            table_lines.append(
                f"| {param_value} | {result['voltage_min']:.3f} | "
                f"{result['voltage_max']:.3f} | {result['iterations']} | "
                f"{result['compute_time']:.1f}s |"
            )

        # 分析趋势
        if len(sweep_results) >= 2:
            voltage_mins = [r["voltage_min"] for r in sweep_results]
            voltage_maxs = [r["voltage_max"] for r in sweep_results]

            v_min_trend = "下降" if voltage_mins[-1] < voltage_mins[0] else "上升"
            v_max_trend = "下降" if voltage_maxs[-1] < voltage_maxs[0] else "上升"

            trend_analysis = f"""\n## 趋势分析

- **电压最小值**: 随 {parameter} 增加呈 **{v_min_trend}** 趋势
- **电压最大值**: 随 {parameter} 增加呈 **{v_max_trend}** 趋势

💡 **建议**: 根据趋势选择合适的参数值，确保电压在允许范围内（0.95 ~ 1.05 pu）。"""
        else:
            trend_analysis = ""

        return [TextContent(
            type="text",
            text=f"""📊 参数扫描完成

**基准案例**: {base_task.case_name}
**扫描参数**: {parameter}
**参数范围**: {param_range}
**执行模式**: {'并行' if parallel else '串行'}

## 执行统计

- ✅ 成功: {len(successful)} 个
- ❌ 失败: {len(failed)} 个
- ⏱️ 总耗时: {sum(r['compute_time'] for r in sweep_results):.1f} 秒

## 扫描结果

{chr(10).join(table_lines)}
{trend_analysis}

## 任务ID列表

{'\n'.join([f'- `{tid}`' for tid in task_ids])}

💡 使用 `case_compare` 对比特定案例，或使用 `result_analyze` 分析单个案例。"""
        )]

    except Exception as e:
        logger.error(f"参数扫描时出错: {e}")
        return [TextContent(
            type="text",
            text=f"❌ 扫描失败: {str(e)}"
        )]
