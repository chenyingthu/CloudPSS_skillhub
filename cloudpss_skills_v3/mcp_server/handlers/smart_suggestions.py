"""
智能建议 (Smart Suggestions) Handler

提供模型分析、参数建议和最佳实践指导。
"""

import logging
from typing import Any

from mcp.types import TextContent

logger = logging.getLogger(__name__)


# 模型特性数据库
MODEL_CHARACTERISTICS = {
    "model/chenying/IEEE39": {
        "type": "standard",
        "size": "medium",
        "typical_convergence": "4-6 iterations",
        "recommended_duration": 10,
        "typical_fault_location": "BUS16, BUS26, BUS29",
        "notes": "经典39节点系统，收敛性好"
    },
    "model/chenying/IEEE39-modified": {
        "type": "renewable",
        "size": "medium",
        "typical_convergence": "5-8 iterations",
        "recommended_duration": 15,
        "typical_fault_location": "BUS16, BUS33",
        "notes": "含分布式电源，注意电压波动"
    },
    "model/ieee/IEEE118": {
        "type": "standard",
        "size": "large",
        "typical_convergence": "6-10 iterations",
        "recommended_duration": 20,
        "typical_fault_location": "BUS49, BUS69, BUS75",
        "notes": "大规模系统，计算时间较长"
    },
    "model/chenying/IEEE14": {
        "type": "standard",
        "size": "small",
        "typical_convergence": "3-5 iterations",
        "recommended_duration": 5,
        "typical_fault_location": "BUS4, BUS9",
        "notes": "小型快速测试系统"
    },
    "model/chenying/WSCC9": {
        "type": "classic",
        "size": "small",
        "typical_convergence": "3-4 iterations",
        "recommended_duration": 5,
        "typical_fault_location": "BUS7, BUS8",
        "notes": "经典3机9节点，适合暂态稳定研究"
    }
}


async def analyze_model_for_powerflow(model_rid: str) -> dict:
    """分析模型并给出潮流计算建议"""
    char = MODEL_CHARACTERISTICS.get(model_rid, {})

    suggestions = {
        "model_info": char,
        "recommendations": []
    }

    if not char:
        suggestions["recommendations"].append({
            "type": "info",
            "message": "未知模型，使用默认参数"
        })
        return suggestions

    # 基于模型特性给出建议
    if char.get("size") == "large":
        suggestions["recommendations"].append({
            "type": "warning",
            "message": f"大规模系统（{char.get('typical_convergence')}），建议增加超时时间"
        })

    if char.get("type") == "renewable":
        suggestions["recommendations"].append({
            "type": "tip",
            "message": "含新能源接入，建议关注电压质量分析"
        })

    suggestions["recommendations"].append({
        "type": "info",
        "message": f"典型收敛迭代：{char.get('typical_convergence')}"
    })

    return suggestions


async def analyze_model_for_emt(model_rid: str, duration: float = 10,
                                fault_config: dict = None) -> dict:
    """分析模型并给出暂态仿真建议"""
    char = MODEL_CHARACTERISTICS.get(model_rid, {})

    suggestions = {
        "model_info": char,
        "recommendations": [],
        "fault_suggestions": []
    }

    if not char:
        suggestions["recommendations"].append({
            "type": "info",
            "message": "未知模型，使用默认参数"
        })
        return suggestions

    # 检查仿真时长
    recommended = char.get("recommended_duration", 10)
    if duration < recommended:
        suggestions["recommendations"].append({
            "type": "warning",
            "message": f"仿真时长较短（{duration}s），建议至少 {recommended}s 以观察完整暂态过程"
        })
    else:
        suggestions["recommendations"].append({
            "type": "success",
            "message": f"仿真时长合适（{duration}s）"
        })

    # 故障配置建议
    typical_faults = char.get("typical_fault_location", "").split(", ")
    if typical_faults and typical_faults[0]:
        suggestions["fault_suggestions"] = typical_faults

    # 模型特定建议
    if "WSCC" in model_rid:
        suggestions["recommendations"].append({
            "type": "tip",
            "message": "经典系统适合研究同步发电机暂态稳定性"
        })

    return suggestions


def format_suggestions(suggestions: dict, analysis_type: str) -> str:
    """格式化建议为文本"""
    lines = []

    # 模型信息
    char = suggestions.get("model_info", {})
    if char:
        lines.append(f"**模型类型**: {char.get('type', '未知')}")
        lines.append(f"**系统规模**: {char.get('size', '未知')}")
        if char.get("notes"):
            lines.append(f"**说明**: {char['notes']}")

    # 建议列表
    recs = suggestions.get("recommendations", [])
    if recs:
        lines.append("\n**建议**:")
        for rec in recs:
            emoji = {
                "info": "ℹ️",
                "warning": "⚠️",
                "tip": "💡",
                "success": "✅"
            }.get(rec["type"], "•")
            lines.append(f"{emoji} {rec['message']}")

    # 故障建议
    faults = suggestions.get("fault_suggestions", [])
    if faults:
        lines.append(f"\n**推荐故障位置**: {', '.join(faults)}")

    return "\n".join(lines)


async def handle_model_analysis(arguments: dict[str, Any]) -> list[TextContent]:
    """处理模型分析请求

    Args:
        arguments: 包含 model_rid, analysis_type 等参数

    Returns:
        MCP TextContent 列表
    """
    logger.info(f"执行 model_analysis: {arguments}")

    model_rid = arguments.get("model_rid")
    analysis_type = arguments.get("analysis_type", "general")

    if not model_rid:
        return [TextContent(
            type="text",
            text="❌ 参数错误: 需要提供 model_rid"
        )]

    try:
        char = MODEL_CHARACTERISTICS.get(model_rid, {})

        if not char:
            return [TextContent(
                type="text",
                text=f"""📊 模型分析

**模型 RID**: `{model_rid}`

⚠️ 未找到该模型的详细信息。

💡 建议：
- 检查模型 RID 是否正确
- 使用 `model_search` 查找可用模型
- 或使用标准参数进行尝试"""
            )]

        analysis = []

        if analysis_type in ["general", "powerflow"]:
            analysis.append(f"""**潮流计算分析**:
- 典型收敛迭代: {char.get('typical_convergence', 'N/A')}
- 系统规模: {char.get('size', '未知')}
- 预计计算时间: {'较长' if char.get('size') == 'large' else '适中'}
""")

        if analysis_type in ["general", "emt"]:
            analysis.append(f"""**暂态仿真分析**:
- 推荐仿真时长: {char.get('recommended_duration', 10)}s
- 典型故障位置: {char.get('typical_fault_location', 'N/A')}
- 特点: {char.get('notes', '')}
""")

        return [TextContent(
            type="text",
            text=f"""📊 模型分析报告

**模型**: {model_rid}

{''.join(analysis)}

💡 **使用建议**:
```python
# 潮流计算
powerflow_run(
    case_name="{char.get('type', 'test')}-分析",
    model_rid="{model_rid}"
)

# 暂态仿真
emt_run(
    case_name="{char.get('type', 'test')}-暂态",
    model_rid="{model_rid}",
    duration={char.get('recommended_duration', 10)},
    fault_config={{
        "bus": "{char.get('typical_fault_location', 'BUS1').split(',')[0]}",
        "type": "three_phase",
        "start_time": 1.0,
        "clear_time": 1.1
    }}
)
```"""
        )]

    except Exception as e:
        logger.error(f"分析模型时出错: {e}")
        return [TextContent(
            type="text",
            text=f"❌ 分析失败: {str(e)}"
        )]
