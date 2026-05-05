"""
潮流计算 (Power Flow) Handler

处理电力系统潮流计算任务。
"""

import logging
from typing import Any

from mcp.types import TextContent

from cloudpss_skills_v3.core.cloudpss_client import get_client
from cloudpss_skills_v3.core.task_store import TaskStatus, get_task_store

logger = logging.getLogger(__name__)


async def handle_powerflow_run(arguments: dict[str, Any]) -> list[TextContent]:
    """处理潮流计算请求

    Args:
        arguments: 包含 case_name, model_rid, wait 等参数

    Returns:
        MCP TextContent 列表
    """
    logger.info(f"执行 powerflow_run: {arguments}")

    case_name = arguments.get("case_name")
    model_rid = arguments.get("model_rid")
    wait = arguments.get("wait", True)

    if not case_name or not model_rid:
        return [TextContent(
            type="text",
            text="❌ 参数错误: 需要提供 case_name 和 model_rid"
        )]

    task_store = get_task_store()
    client = get_client()
    task_id = None

    try:
        # 步骤 1: 创建案例
        logger.info(f"创建案例: {case_name}, 模型: {model_rid}")
        case_id = await client.create_case(name=case_name, model_rid=model_rid)

        # 步骤 2: 提交潮流计算任务
        logger.info(f"提交潮流计算: case={case_id}")
        task_id = await client.submit_powerflow(case_id=case_id)

        # 步骤 3: 在任务存储中创建记录
        task_store.create_task(
            task_id=task_id,
            case_name=case_name,
            model_rid=model_rid,
            task_type="powerflow"
        )

        if wait:
            # 同步模式：等待任务完成
            logger.info(f"等待任务完成: {task_id}")
            task_store.update_task_status(
                task_id=task_id,
                status=TaskStatus.RUNNING,
                progress=10,
                message="正在执行潮流计算..."
            )

            result = await client.wait_for_completion(task_id)

            # 更新任务状态为完成
            task_store.update_task_status(
                task_id=task_id,
                status=TaskStatus.COMPLETED,
                progress=100,
                message="潮流计算完成",
                result_data={
                    "bus_count": result.bus_count,
                    "branch_count": result.branch_count,
                    "voltage_min": result.voltage_min,
                    "voltage_max": result.voltage_max,
                    "iterations": result.iterations,
                    "compute_time": result.compute_time
                }
            )

            return _format_sync_result(result)
        else:
            # 异步模式：只返回任务ID
            task_store.update_task_status(
                task_id=task_id,
                status=TaskStatus.RUNNING,
                progress=5,
                message="任务已提交，正在执行..."
            )

            return [TextContent(
                type="text",
                text=f"""⏳ 潮流计算任务已提交

**任务 ID**: {task_id}
**案例**: {case_name}
**模型**: {model_rid}

使用 `result_query` 查询任务状态和结果。"""
            )]

    except TimeoutError as e:
        logger.error(f"任务超时: {e}")
        if task_id:
            task_store.update_task_status(
                task_id=task_id,
                status=TaskStatus.FAILED,
                error_message=str(e),
                message="任务执行超时"
            )
        return [TextContent(
            type="text",
            text=f"❌ 任务超时: {str(e)}"
        )]
    except RuntimeError as e:
        logger.error(f"任务失败: {e}")
        if task_id:
            task_store.update_task_status(
                task_id=task_id,
                status=TaskStatus.FAILED,
                error_message=str(e),
                message="任务执行失败"
            )
        return [TextContent(
            type="text",
            text=f"❌ 任务执行失败: {str(e)}"
        )]
    except Exception as e:
        logger.error(f"执行 powerflow_run 时出错: {e}")
        if task_id:
            task_store.update_task_status(
                task_id=task_id,
                status=TaskStatus.FAILED,
                error_message=str(e),
                message="执行过程中发生错误"
            )
        return [TextContent(
            type="text",
            text=f"❌ 执行失败: {str(e)}"
        )]


def _format_sync_result(result) -> list[TextContent]:
    """格式化同步执行结果"""
    voltage_status = "正常"
    if result.voltage_min < 0.95:
        voltage_status = f"⚠️ 偏低 (最低 {result.voltage_min:.3f} pu)"
    elif result.voltage_max > 1.05:
        voltage_status = f"⚠️ 偏高 (最高 {result.voltage_max:.3f} pu)"

    return [TextContent(
        type="text",
        text=f"""✅ 潮流计算完成！

**案例**: {result.case_name}
**模型**: {result.model_rid}
**任务 ID**: {result.task_id}

**系统规模**:
- 母线数量: {result.bus_count} 条
- 支路数量: {result.branch_count} 条

**计算结果**:
- 电压范围: {result.voltage_min:.3f} ~ {result.voltage_max:.3f} pu
- 电压状态: {voltage_status}
- 收敛迭代: {result.iterations} 次
- 计算用时: {result.compute_time:.1f} 秒

**状态**: 计算成功，系统运行正常。

💡 使用 `result_analyze` 进行智能分析，或使用 `result_export` 导出详细数据。"""
    )]
