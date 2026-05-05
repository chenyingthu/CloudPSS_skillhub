"""
暂态仿真 (EMT - Electromagnetic Transient) Handler

处理电力系统暂态仿真任务，用于故障分析、稳定性研究等。
"""

import logging
from typing import Any

from mcp.types import TextContent

from cloudpss_skills_v3.core.cloudpss_client import get_client

logger = logging.getLogger(__name__)


async def handle_emt_run(arguments: dict[str, Any]) -> list[TextContent]:
    """处理暂态仿真请求

    Args:
        arguments: 包含 case_name, model_rid, duration, fault_config, wait 等参数

    Returns:
        MCP TextContent 列表
    """
    logger.info(f"执行 emt_run: {arguments}")

    case_name = arguments.get("case_name")
    model_rid = arguments.get("model_rid")
    duration = arguments.get("duration", 10)
    fault_config = arguments.get("fault_config")
    wait = arguments.get("wait", True)

    if not case_name or not model_rid:
        return [TextContent(
            type="text",
            text="❌ 参数错误: 需要提供 case_name 和 model_rid"
        )]

    try:
        client = get_client()

        # 步骤 1: 创建案例
        logger.info(f"创建暂态仿真案例: {case_name}, 模型: {model_rid}")
        case_id = await client.create_case(name=case_name, model_rid=model_rid)

        # 步骤 2: 构建仿真配置
        emt_options = {
            "duration": duration,
            "fault_config": fault_config
        }

        # 步骤 3: 提交暂态仿真任务
        logger.info(f"提交暂态仿真: case={case_id}, duration={duration}s")
        task_id = await client.submit_emt(case_id=case_id, options=emt_options)

        if wait:
            # 同步模式：等待任务完成
            logger.info(f"等待暂态仿真完成: {task_id}")
            result = await client.wait_for_completion(task_id)

            return _format_emt_result(result, duration, fault_config)
        else:
            # 异步模式：只返回任务ID
            return [TextContent(
                type="text",
                text=f"""⏳ 暂态仿真任务已提交

**任务 ID**: {task_id}
**案例**: {case_name}
**模型**: {model_rid}
**仿真时长**: {duration} 秒

使用 `result_query` 查询任务状态和结果。"""
            )]

    except TimeoutError as e:
        logger.error(f"任务超时: {e}")
        return [TextContent(
            type="text",
            text=f"❌ 任务超时: {str(e)}"
        )]
    except RuntimeError as e:
        logger.error(f"任务失败: {e}")
        return [TextContent(
            type="text",
            text=f"❌ 任务执行失败: {str(e)}"
        )]
    except Exception as e:
        logger.error(f"执行 emt_run 时出错: {e}")
        return [TextContent(
            type="text",
            text=f"❌ 执行失败: {str(e)}"
        )]


def _format_emt_result(result, duration: float, fault_config: dict | None) -> list[TextContent]:
    """格式化暂态仿真结果"""

    # 故障信息描述
    fault_desc = "无故障（正常运行）"
    if fault_config:
        bus = fault_config.get("bus", "未知")
        fault_type = fault_config.get("type", "three_phase")
        start_time = fault_config.get("start_time", 0)
        clear_time = fault_config.get("clear_time", 0)

        type_map = {
            "three_phase": "三相短路",
            "single_phase": "单相接地"
        }
        type_cn = type_map.get(fault_type, fault_type)

        fault_desc = f"{bus} 母线{type_cn}故障，{start_time}s 发生，{clear_time}s 切除"

    return [TextContent(
        type="text",
        text=f"""✅ 暂态仿真完成！

**案例**: {result.case_name}
**模型**: {result.model_rid}
**任务 ID**: {result.task_id}

**仿真配置**:
- 仿真时长: {duration} 秒
- 故障设置: {fault_desc}

**系统规模**:
- 母线数量: {result.bus_count} 条
- 支路数量: {result.branch_count} 条

**计算结果**:
- 收敛迭代: {result.iterations} 次
- 计算用时: {result.compute_time:.1f} 秒

**状态**: 暂态仿真成功完成。

💡 使用 `result_analyze` 进行稳定性分析，或使用 `result_export` 导出波形数据。"""
    )]
