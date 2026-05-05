"""
MCP Server 主入口

提供电力系统仿真相关的 Tools，支持：
- 潮流计算 (powerflow_run)
- 暂态仿真 (emt_run)
- 结果查询 (result_query)
- 结果分析 (result_analyze)
- 结果导出 (result_export)
- 参数扫描 (parameter_sweep)
- 算例对比 (case_compare)
- 模型搜索 (model_search)
"""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.types import TextContent, Tool

# 导入 handlers
from cloudpss_skills_v3.mcp_server.handlers import (
    handle_powerflow_run,
    handle_emt_run,
    handle_result_query,
    handle_result_analyze,
    handle_result_export,
    handle_model_search,
    handle_model_analysis,
    handle_case_compare,
    handle_parameter_sweep,
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建 MCP Server 实例
app = Server("cloudpss-skills")


# =============================================================================
# Tool 定义
# =============================================================================

CORE_TOOLS: list[Tool] = [
    Tool(
        name="powerflow_run",
        description="""运行潮流计算，分析电力系统稳态运行点。

返回母线电压、支路功率、网损等关键指标。适用于：
- 基础潮流分析
- 电压质量评估
- 线路负载检查

示例: 运行 IEEE39 系统的潮流计算""",
        inputSchema={
            "type": "object",
            "properties": {
                "case_name": {
                    "type": "string",
                    "description": "案例名称，如 'IEEE39-基态工况'"
                },
                "model_rid": {
                    "type": "string",
                    "description": "CloudPSS 模型 RID，如 'model/chenying/IEEE39'"
                },
                "wait": {
                    "type": "boolean",
                    "description": "是否等待计算完成（默认 true）",
                    "default": True
                }
            },
            "required": ["case_name", "model_rid"]
        }
    ),
    Tool(
        name="emt_run",
        description="""运行暂态仿真（EMT），分析系统动态响应。

适用于故障分析、稳定性研究等场景。可以设置：
- 仿真时长
- 故障类型和位置
- 切除时间

示例: 分析母线三相短路故障后的系统恢复过程""",
        inputSchema={
            "type": "object",
            "properties": {
                "case_name": {
                    "type": "string",
                    "description": "案例名称"
                },
                "model_rid": {
                    "type": "string",
                    "description": "模型 RID"
                },
                "duration": {
                    "type": "number",
                    "description": "仿真时长（秒，默认 10）",
                    "default": 10
                },
                "fault_config": {
                    "type": "object",
                    "description": "故障配置（可选）",
                    "properties": {
                        "bus": {"type": "string", "description": "故障母线"},
                        "type": {"type": "string", "enum": ["three_phase", "single_phase"]},
                        "start_time": {"type": "number"},
                        "clear_time": {"type": "number"}
                    }
                },
                "wait": {
                    "type": "boolean",
                    "default": True
                }
            },
            "required": ["case_name", "model_rid"]
        }
    ),
    Tool(
        name="result_query",
        description="""查询仿真任务的状态和结果。

可以获取：
- 任务执行状态（pending/running/completed/failed）
- 当前进度百分比
- 计算结果（如果已完成）
- 错误信息（如果失败）

适用于异步任务的状态检查""",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "任务 ID"
                },
                "include_data": {
                    "type": "boolean",
                    "description": "是否包含完整结果数据",
                    "default": False
                }
            },
            "required": ["task_id"]
        }
    ),
    Tool(
        name="result_analyze",
        description="""智能分析仿真结果，生成专业解读。

分析维度：
- voltage: 电压质量分析
- stability: 稳定性分析
- losses: 网损分析
- general: 综合分析

返回自然语言格式的分析报告，适合直接用于论文或报告。""",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "已完成任务的 ID"
                },
                "focus": {
                    "type": "string",
                    "enum": ["voltage", "stability", "losses", "general"],
                    "description": "分析重点",
                    "default": "general"
                }
            },
            "required": ["task_id"]
        }
    ),
    Tool(
        name="result_export",
        description="""导出仿真结果为指定格式。

支持格式：
- csv: CSV 表格（适合 Excel 分析）
- json: JSON 数据（适合程序处理）
- md: Markdown 报告（适合论文附录）

可指定输出路径，默认保存到工作空间。""",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "任务 ID"
                },
                "format": {
                    "type": "string",
                    "enum": ["csv", "json", "md"],
                    "description": "导出格式",
                    "default": "csv"
                },
                "output_path": {
                    "type": "string",
                    "description": "输出文件路径（可选）"
                }
            },
            "required": ["task_id"]
        }
    ),
    Tool(
        name="parameter_sweep",
        description="""参数扫描分析，批量运行多组参数。

适用于：
- 敏感性分析
- 参数优化
- 工况对比

系统会自动创建多个变体案例，并行执行，最后汇总对比结果。""",
        inputSchema={
            "type": "object",
            "properties": {
                "base_case": {
                    "type": "string",
                    "description": "基准案例名称或 ID"
                },
                "parameter": {
                    "type": "string",
                    "description": "扫描参数名，如 'load_p', 'generation'"
                },
                "range": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "参数值列表，如 [0.8, 0.9, 1.0, 1.1, 1.2]"
                },
                "parallel": {
                    "type": "boolean",
                    "description": "是否并行执行",
                    "default": True
                }
            },
            "required": ["base_case", "parameter", "range"]
        }
    ),
    Tool(
        name="case_compare",
        description="""对比多个算例的结果差异。

生成对比表格和差异分析，帮助评估：
- 不同控制策略的效果
- 不同参数配置的影响
- 改进前后的变化

支持对比母线电压、支路功率、网损等指标。""",
        inputSchema={
            "type": "object",
            "properties": {
                "case_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "案例 ID 列表"
                },
                "metrics": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "对比指标",
                    "default": ["voltage", "loading", "losses"]
                }
            },
            "required": ["case_ids"]
        }
    ),
    Tool(
        name="model_search",
        description="""在 CloudPSS 模型库中搜索模型。

帮助用户：
- 发现可用模型
- 对比模型差异
- 选择合适的模型进行仿真

返回模型列表，包含名称、描述、关键参数等信息。""",
        inputSchema={
            "type": "object",
            "properties": {
                "keywords": {
                    "type": "string",
                    "description": "搜索关键词，如 'IEEE39', '暂态', '分布式电源'"
                },
                "filter": {
                    "type": "object",
                    "description": "过滤条件（可选）",
                    "properties": {
                        "bus_count": {"type": "integer"},
                        "has_renewable": {"type": "boolean"}
                    }
                }
            },
            "required": ["keywords"]
        }
    ),
    Tool(
        name="model_analysis",
        description="""分析模型特性，提供参数建议和最佳实践。

分析维度：
- general: 综合分析
- powerflow: 潮流计算分析
- emt: 暂态仿真分析

返回模型特性、推荐参数、使用建议。""",
        inputSchema={
            "type": "object",
            "properties": {
                "model_rid": {
                    "type": "string",
                    "description": "模型 RID，如 'model/chenying/IEEE39'"
                },
                "analysis_type": {
                    "type": "string",
                    "enum": ["general", "powerflow", "emt"],
                    "description": "分析类型",
                    "default": "general"
                }
            },
            "required": ["model_rid"]
        }
    )
]


# =============================================================================
# Tool 处理函数
# =============================================================================













# =============================================================================
# MCP 路由
# =============================================================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """返回所有可用的 Tools"""
    logger.info("返回 Tools 列表")
    return CORE_TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """处理 Tool 调用"""
    logger.info(f"调用 Tool: {name}, 参数: {arguments}")

    handlers = {
        "powerflow_run": handle_powerflow_run,
        "emt_run": handle_emt_run,
        "result_query": handle_result_query,
        "result_analyze": handle_result_analyze,
        "result_export": handle_result_export,
        "model_search": handle_model_search,
        "model_analysis": handle_model_analysis,
        "case_compare": handle_case_compare,
        "parameter_sweep": handle_parameter_sweep,
    }

    handler = handlers.get(name)
    if handler:
        try:
            return await handler(arguments)
        except Exception as e:
            logger.error(f"处理 {name} 时出错: {e}")
            return [TextContent(
                type="text",
                text=f"❌ 执行失败: {str(e)}"
            )]
    else:
        return [TextContent(
            type="text",
            text=f"❌ 未知 Tool: {name}"
        )]


# =============================================================================
# 启动入口
# =============================================================================

def create_server() -> Server:
    """创建并返回 MCP Server 实例"""
    return app


async def main():
    """主入口函数"""
    logger.info("启动 CloudPSS Skills MCP Server...")
    logger.info(f"已注册 {len(CORE_TOOLS)} 个 Tools")

    # 使用 stdio 传输
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
