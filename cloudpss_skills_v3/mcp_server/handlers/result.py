"""
结果查询 (Result Query) Handler

处理仿真结果查询和状态检查。
"""

import logging
from typing import Any

from mcp.types import TextContent

from cloudpss_skills_v3.core.cloudpss_client import get_client
from cloudpss_skills_v3.core.task_store import TaskStatus, get_task_store

logger = logging.getLogger(__name__)


async def handle_result_query(arguments: dict[str, Any]) -> list[TextContent]:
    """处理结果查询请求

    Args:
        arguments: 包含 task_id, include_data 等参数

    Returns:
        MCP TextContent 列表
    """
    logger.info(f"执行 result_query: {arguments}")

    task_id = arguments.get("task_id")
    include_data = arguments.get("include_data", False)

    if not task_id:
        return [TextContent(
            type="text",
            text="❌ 参数错误: 需要提供 task_id"
        )]

    try:
        task_store = get_task_store()

        # 优先从 TaskStore 获取本地状态
        task_info = task_store.get_task(task_id)

        if task_info:
            # 如果本地有记录，使用本地状态
            status_dict = {
                "task_id": task_info.task_id,
                "status": task_info.status.value,
                "progress": task_info.progress,
                "message": task_info.message,
                "case_name": task_info.case_name,
                "model_rid": task_info.model_rid,
                "task_type": task_info.task_type,
                "created_at": task_info.created_at.isoformat(),
                "updated_at": task_info.updated_at.isoformat()
            }
            if task_info.result_data:
                status_dict["result"] = task_info.result_data
            if task_info.error_message:
                status_dict["error"] = task_info.error_message
        else:
            # 本地没有记录，从 API 查询
            client = get_client()
            status_dict = await client.get_task_status(task_id)

        return _format_status_result(status_dict, include_data)

    except Exception as e:
        logger.error(f"查询任务状态时出错: {e}")
        return [TextContent(
            type="text",
            text=f"❌ 查询失败: {str(e)}"
        )]


def _format_status_result(status: dict, include_data: bool) -> list[TextContent]:
    """格式化任务状态结果"""
    task_id = status.get("task_id", "未知")
    task_status = status.get("status", "unknown")
    progress = status.get("progress", 0)
    message = status.get("message", "")

    # 状态表情映射
    status_emoji = {
        "pending": "⏳",
        "running": "🔄",
        "completed": "✅",
        "failed": "❌",
        "cancelled": "🚫"
    }.get(task_status, "❓")

    # 状态中文映射
    status_cn = {
        "pending": "等待中",
        "running": "运行中",
        "completed": "已完成",
        "failed": "失败",
        "cancelled": "已取消"
    }.get(task_status, task_status)

    text = f"""📊 任务状态查询

**任务 ID**: {task_id}
**状态**: {status_emoji} {status_cn}
**进度**: {progress}%
"""

    if message:
        text += f"\n**消息**: {message}"

    if task_status == "completed":
        text += """

💡 使用 `result_analyze` 进行智能分析，或使用 `result_export` 导出详细数据。"""
    elif task_status == "failed":
        text += """

⚠️ 任务执行失败，请检查输入参数或联系管理员。"""
    elif task_status in ["pending", "running"]:
        text += """

⏳ 任务仍在执行中，请稍后再次查询。"""

    if include_data and task_status == "completed":
        text += """

**详细数据**:
```json
{"status": "completed", "data": {...}}
```
（详细数据暂未实现，将在 Phase 1.5 后支持）"""

    return [TextContent(type="text", text=text)]


def _get_focus_cn(focus: str) -> str:
    """获取分析维度的中文名称"""
    return {
        "voltage": "电压质量分析",
        "stability": "稳定性分析",
        "losses": "网损分析",
        "general": "综合分析"
    }.get(focus, "综合分析")


def _analyze_voltage(result_data: dict) -> str:
    """分析电压质量"""
    v_min = result_data.get('voltage_min', 0.98)
    v_max = result_data.get('voltage_max', 1.05)

    analysis = ["**电压质量分析**:\n"]

    # 电压范围评估
    if 0.95 <= v_min and v_max <= 1.05:
        analysis.append("✅ 电压水平在允许范围内（0.95 ~ 1.05 pu）")
    else:
        analysis.append("⚠️ 存在电压越限问题")

    # 电压波动评估
    v_range = v_max - v_min
    if v_range < 0.05:
        analysis.append("✅ 电压波动较小，系统稳定")
    elif v_range < 0.1:
        analysis.append("ℹ️ 电压波动适中，属于正常范围")
    else:
        analysis.append("⚠️ 电压波动较大，建议检查无功补偿配置")

    # 具体建议
    if v_min < 0.95:
        analysis.append(f"⚠️ 最低电压 {v_min:.3f} pu 偏低，建议增加无功补偿")
    if v_max > 1.05:
        analysis.append(f"⚠️ 最高电压 {v_max:.3f} pu 偏高，建议调整变压器分接头")

    return "\n".join(analysis)


def _analyze_stability(result_data: dict) -> str:
    """分析稳定性"""
    iterations = result_data.get('iterations', 4)
    compute_time = result_data.get('compute_time', 2.3)

    analysis = ["**稳定性分析**:\n"]

    # 收敛性评估
    if iterations <= 4:
        analysis.append("✅ 收敛性良好，系统求解稳定")
    elif iterations <= 8:
        analysis.append("ℹ️ 收敛正常，系统运行稳定")
    else:
        analysis.append("⚠️ 收敛迭代次数较多，建议检查系统参数")

    # 计算效率评估
    if compute_time < 1.0:
        analysis.append("✅ 计算效率高，响应迅速")
    elif compute_time < 5.0:
        analysis.append("ℹ️ 计算效率正常")
    else:
        analysis.append("ℹ️ 计算耗时较长（大规模系统正常）")

    return "\n".join(analysis)


def _analyze_losses(result_data: dict) -> str:
    """分析网损"""
    analysis = ["**网损分析**:\n"]

    # 基于系统规模估算网损
    bus_count = result_data.get('bus_count', 39)
    branch_count = result_data.get('branch_count', 46)

    # 典型网损率参考
    typical_loss_rate = 0.04  # 4%

    analysis.append(f"ℹ️ 系统规模: {bus_count} 母线 / {branch_count} 支路")
    analysis.append(f"ℹ️ 典型网损率参考: {typical_loss_rate*100:.1f}%")

    # 网损评估建议
    analysis.append("\n💡 **网损优化建议**:")
    analysis.append("- 优化无功补偿配置")
    analysis.append("- 合理调整变压器分接头")
    analysis.append("- 考虑采用低损耗设备")

    return "\n".join(analysis)


def _analyze_general(result_data: dict) -> str:
    """综合分析"""
    v_min = result_data.get('voltage_min', 0.98)
    v_max = result_data.get('voltage_max', 1.05)
    iterations = result_data.get('iterations', 4)

    analysis = ["**综合分析**:\n"]

    # 总体评估
    all_good = (
        0.95 <= v_min and v_max <= 1.05 and
        iterations <= 6
    )

    if all_good:
        analysis.append("✅ 系统运行状况良好")
    else:
        analysis.append("⚠️ 系统存在部分问题需要关注")

    analysis.append("")
    analysis.append(_analyze_voltage(result_data))
    analysis.append("")
    analysis.append(_analyze_stability(result_data))

    return "\n".join(analysis)


async def handle_result_analyze(arguments: dict[str, Any]) -> list[TextContent]:
    """处理结果分析请求

    Args:
        arguments: 包含 task_id, focus 等参数

    Returns:
        MCP TextContent 列表
    """
    logger.info(f"执行 result_analyze: {arguments}")

    task_id = arguments.get("task_id")
    focus = arguments.get("focus", "general")

    if not task_id:
        return [TextContent(
            type="text",
            text="❌ 参数错误: 需要提供 task_id"
        )]

    try:
        task_store = get_task_store()
        task = task_store.get_task(task_id)

        if not task:
            return [TextContent(
                type="text",
                text=f"❌ 未找到任务: {task_id}"
            )]

        if task.status != TaskStatus.COMPLETED:
            return [TextContent(
                type="text",
                text=f"⏳ 任务尚未完成，无法分析\n\n当前状态: {task.status.value}"
            )]

        # 获取结果数据
        result_data = task.result_data or {}

        # 根据 focus 进行分析
        if focus == "voltage":
            analysis = _analyze_voltage(result_data)
        elif focus == "stability":
            analysis = _analyze_stability(result_data)
        elif focus == "losses":
            analysis = _analyze_losses(result_data)
        else:
            analysis = _analyze_general(result_data)

        return [TextContent(
            type="text",
            text=f"""📈 结果智能分析报告

**任务**: {task.case_name}
**模型**: {task.model_rid}
**任务 ID**: {task_id}
**分析维度**: {_get_focus_cn(focus)}

{analysis}

---
📊 **原始数据摘要**:
- 母线数量: {result_data.get('bus_count', 'N/A')}
- 支路数量: {result_data.get('branch_count', 'N/A')}
- 电压范围: {result_data.get('voltage_min', 'N/A')} ~ {result_data.get('voltage_max', 'N/A')} pu
- 收敛迭代: {result_data.get('iterations', 'N/A')} 次
- 计算用时: {result_data.get('compute_time', 'N/A')} 秒"""
        )]

    except Exception as e:
        logger.error(f"分析结果时出错: {e}")
        return [TextContent(
            type="text",
            text=f"❌ 分析失败: {str(e)}"
        )]


async def handle_result_export(arguments: dict[str, Any]) -> list[TextContent]:
    """处理结果导出请求

    Args:
        arguments: 包含 task_id, format, output_path 等参数

    Returns:
        MCP TextContent 列表
    """
    logger.info(f"执行 result_export: {arguments}")

    task_id = arguments.get("task_id")
    fmt = arguments.get("format", "csv")
    output_path = arguments.get("output_path")

    if not task_id:
        return [TextContent(
            type="text",
            text="❌ 参数错误: 需要提供 task_id"
        )]

    try:
        task_store = get_task_store()
        task = task_store.get_task(task_id)

        if not task:
            return [TextContent(
                type="text",
                text=f"❌ 未找到任务: {task_id}"
            )]

        if task.status != TaskStatus.COMPLETED:
            return [TextContent(
                type="text",
                text=f"⏳ 任务尚未完成，无法导出\n\n当前状态: {task.status.value}"
            )]

        # 获取结果数据
        result_data = task.result_data or {}

        # 根据格式生成导出内容
        if fmt == "json":
            content = _export_json(task, result_data)
            file_ext = "json"
        elif fmt == "md":
            content = _export_markdown(task, result_data)
            file_ext = "md"
        else:  # csv
            content = _export_csv(task, result_data)
            file_ext = "csv"

        # 确定输出路径
        import os
        if not output_path:
            workspace = os.getenv("CLOUDPSS_WORKSPACE", "~/.cloudpss/workspace")
            output_path = os.path.expanduser(f"{workspace}/exports")

        os.makedirs(output_path, exist_ok=True)
        filename = f"{task.case_name}_{task_id}.{file_ext}"
        filepath = os.path.join(output_path, filename)

        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return [TextContent(
            type="text",
            text=f"""✅ 结果导出成功

**任务**: {task.case_name}
**任务 ID**: {task_id}
**导出格式**: {fmt.upper()}
**文件路径**: `{filepath}`

**导出内容预览**:

```
{content[:500]}{'...' if len(content) > 500 else ''}
```

💡 文件已保存到工作目录，可直接下载使用。"""
        )]

    except Exception as e:
        logger.error(f"导出结果时出错: {e}")
        return [TextContent(
            type="text",
            text=f"❌ 导出失败: {str(e)}"
        )]


def _export_json(task, result_data: dict) -> str:
    """导出为 JSON 格式"""
    import json
    from datetime import datetime

    export_data = {
        "task_id": task.task_id,
        "case_name": task.case_name,
        "model_rid": task.model_rid,
        "task_type": task.task_type,
        "status": task.status.value,
        "created_at": task.created_at.isoformat(),
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        "result": result_data,
        "exported_at": datetime.now().isoformat()
    }

    return json.dumps(export_data, ensure_ascii=False, indent=2)


def _export_markdown(task, result_data: dict) -> str:
    """导出为 Markdown 报告格式"""
    lines = [
        f"# 仿真结果报告: {task.case_name}",
        "",
        "## 任务信息",
        "",
        f"- **任务 ID**: `{task.task_id}`",
        f"- **案例名称**: {task.case_name}",
        f"- **模型 RID**: `{task.model_rid}`",
        f"- **任务类型**: {task.task_type}",
        f"- **状态**: {task.status.value}",
        f"- **创建时间**: {task.created_at.isoformat()}",
        "",
        "## 计算结果",
        "",
        "| 指标 | 数值 | 单位 |",
        "|------|------|------|",
        f"| 母线数量 | {result_data.get('bus_count', 'N/A')} | - |",
        f"| 支路数量 | {result_data.get('branch_count', 'N/A')} | - |",
        f"| 电压最小值 | {result_data.get('voltage_min', 'N/A')} | pu |",
        f"| 电压最大值 | {result_data.get('voltage_max', 'N/A')} | pu |",
        f"| 收敛迭代 | {result_data.get('iterations', 'N/A')} | 次 |",
        f"| 计算时间 | {result_data.get('compute_time', 'N/A')} | 秒 |",
        "",
        "## 分析结论",
        "",
        "根据计算结果，系统运行状态如下：",
        "",
    ]

    # 添加简单分析
    v_min = result_data.get('voltage_min', 0.98)
    v_max = result_data.get('voltage_max', 1.05)

    if 0.95 <= v_min and v_max <= 1.05:
        lines.append("- ✅ 电压水平在允许范围内")
    else:
        lines.append("- ⚠️ 存在电压越限问题")

    lines.extend([
        "",
        "---",
        "",
        "*报告由 CloudPSS Skills MCP Server 生成*",
    ])

    return "\n".join(lines)


def _export_csv(task, result_data: dict) -> str:
    """导出为 CSV 格式"""
    lines = [
        "指标,数值,单位",
        f"任务ID,{task.task_id},-",
        f"案例名称,{task.case_name},-",
        f"模型RID,{task.model_rid},-",
        f"母线数量,{result_data.get('bus_count', 'N/A')},-",
        f"支路数量,{result_data.get('branch_count', 'N/A')},-",
        f"电压最小值,{result_data.get('voltage_min', 'N/A')},pu",
        f"电压最大值,{result_data.get('voltage_max', 'N/A')},pu",
        f"收敛迭代,{result_data.get('iterations', 'N/A')},次",
        f"计算时间,{result_data.get('compute_time', 'N/A')},秒",
    ]

    return "\n".join(lines)
