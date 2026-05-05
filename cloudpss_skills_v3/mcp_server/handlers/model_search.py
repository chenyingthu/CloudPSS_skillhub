"""
模型搜索 (Model Search) Handler

处理 CloudPSS 模型库搜索请求。
"""

import logging
from typing import Any

from mcp.types import TextContent

logger = logging.getLogger(__name__)


# 模拟模型数据库
MOCK_MODELS = [
    {
        "rid": "model/chenying/IEEE39",
        "name": "IEEE 39节点标准系统",
        "description": "IEEE 39节点标准测试系统，包含10台发电机、39条母线、46条支路",
        "bus_count": 39,
        "branch_count": 46,
        "has_renewable": False,
        "tags": ["标准系统", "潮流计算", "暂态仿真"]
    },
    {
        "rid": "model/chenying/IEEE39-modified",
        "name": "IEEE 39节点改进版（含分布式电源）",
        "description": "在IEEE 39节点基础上增加了风电和光伏接入",
        "bus_count": 39,
        "branch_count": 52,
        "has_renewable": True,
        "tags": ["分布式电源", "新能源", "暂态仿真"]
    },
    {
        "rid": "model/ieee/IEEE118",
        "name": "IEEE 118节点大规模系统",
        "description": "IEEE 118节点系统，用于大规模电网仿真研究",
        "bus_count": 118,
        "branch_count": 186,
        "has_renewable": False,
        "tags": ["大规模系统", "标准系统"]
    },
    {
        "rid": "model/chenying/IEEE14",
        "name": "IEEE 14节点系统",
        "description": "小型标准测试系统，适合快速验证",
        "bus_count": 14,
        "branch_count": 20,
        "has_renewable": False,
        "tags": ["小型系统", "快速测试"]
    },
    {
        "rid": "model/chenying/WSCC9",
        "name": "WSCC 9节点系统",
        "description": "经典的WSCC 3机9节点系统",
        "bus_count": 9,
        "branch_count": 9,
        "has_renewable": False,
        "tags": ["经典系统", "教学演示"]
    }
]


async def handle_model_search(arguments: dict[str, Any]) -> list[TextContent]:
    """处理模型搜索请求

    Args:
        arguments: 包含 keywords, filter 等参数

    Returns:
        MCP TextContent 列表
    """
    logger.info(f"执行 model_search: {arguments}")

    keywords = arguments.get("keywords", "").lower()
    filter_config = arguments.get("filter", {})

    try:
        # 过滤模型
        results = MOCK_MODELS

        # 关键词过滤
        if keywords:
            results = [
                m for m in results
                if keywords in m["name"].lower()
                or keywords in m["description"].lower()
                or keywords in m["rid"].lower()
                or any(keywords in tag.lower() for tag in m["tags"])
            ]

        # 应用过滤器
        if "bus_count" in filter_config:
            min_buses = filter_config["bus_count"]
            results = [m for m in results if m["bus_count"] >= min_buses]

        if "has_renewable" in filter_config:
            has_renewable = filter_config["has_renewable"]
            results = [m for m in results if m["has_renewable"] == has_renewable]

        # 格式化结果
        if not results:
            return [TextContent(
                type="text",
                text=f"""🔍 模型搜索结果

**搜索词**: {keywords or '（无）'}

未找到匹配的模型。请尝试其他关键词，如：
- IEEE39
- 分布式电源
- 暂态仿真
- 标准系统"""
            )]

        models_text = "\n\n".join([
            f"**{i+1}. {m['name']}**\n"
            f"- RID: `{m['rid']}`\n"
            f"- 描述: {m['description']}\n"
            f"- 规模: {m['bus_count']} 母线 / {m['branch_count']} 支路\n"
            f"- 标签: {', '.join(m['tags'])}"
            for i, m in enumerate(results)
        ])

        return [TextContent(
            type="text",
            text=f"""🔍 模型搜索结果

**搜索词**: {keywords or '（全部）'}
**找到**: {len(results)} 个模型

{models_text}

💡 使用找到的模型 RID 运行仿真：
```
powerflow_run(case_name="测试", model_rid="{results[0]['rid']}")
```"""
        )]

    except Exception as e:
        logger.error(f"搜索模型时出错: {e}")
        return [TextContent(
            type="text",
            text=f"❌ 搜索失败: {str(e)}"
        )]
