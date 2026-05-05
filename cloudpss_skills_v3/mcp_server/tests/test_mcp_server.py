"""
MCP Server 单元测试
"""

import pytest
import asyncio
from mcp.types import TextContent

from cloudpss_skills_v3.mcp_server.server import (
    list_tools,
    call_tool,
    CORE_TOOLS,
)
from cloudpss_skills_v3.mcp_server.handlers import (
    handle_powerflow_run,
    handle_emt_run,
    handle_result_query,
)


@pytest.mark.asyncio
async def test_list_tools():
    """测试返回 Tools 列表"""
    tools = await list_tools()

    # 验证返回了正确的 Tools
    assert len(tools) == len(CORE_TOOLS)

    # 验证关键 Tool 存在
    tool_names = [t.name for t in tools]
    assert "powerflow_run" in tool_names
    assert "emt_run" in tool_names
    assert "result_query" in tool_names
    assert "result_analyze" in tool_names

    # 验证 powerflow_run 有正确的 schema
    powerflow_tool = next(t for t in tools if t.name == "powerflow_run")
    assert "case_name" in powerflow_tool.inputSchema["properties"]
    assert "model_rid" in powerflow_tool.inputSchema["properties"]


@pytest.mark.asyncio
async def test_call_tool_unknown():
    """测试调用未知 Tool"""
    result = await call_tool("unknown_tool", {})

    assert len(result) == 1
    assert result[0].type == "text"
    assert "未知 Tool" in result[0].text


@pytest.mark.asyncio
async def test_handle_powerflow_run_sync():
    """测试同步执行潮流计算"""
    result = await handle_powerflow_run({
        "case_name": "test-ieee39",
        "model_rid": "model/chenying/IEEE39",
        "wait": True
    })

    assert len(result) == 1
    assert result[0].type == "text"
    assert "潮流计算完成" in result[0].text
    assert "母线数量" in result[0].text
    assert "支路数量" in result[0].text


@pytest.mark.asyncio
async def test_handle_powerflow_run_async():
    """测试异步提交潮流计算"""
    result = await handle_powerflow_run({
        "case_name": "test-ieee39",
        "model_rid": "model/chenying/IEEE39",
        "wait": False
    })

    assert len(result) == 1
    assert result[0].type == "text"
    assert "任务已提交" in result[0].text
    assert "任务 ID" in result[0].text


@pytest.mark.asyncio
async def test_call_tool_powerflow_run():
    """测试通过 call_tool 调用 powerflow_run"""
    result = await call_tool("powerflow_run", {
        "case_name": "test-case",
        "model_rid": "model/test/123"
    })

    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "潮流计算完成" in result[0].text


@pytest.mark.asyncio
async def test_handle_emt_run_sync():
    """测试同步执行暂态仿真"""
    result = await handle_emt_run({
        "case_name": "test-emt",
        "model_rid": "model/chenying/IEEE39",
        "duration": 5,
        "wait": True
    })

    assert len(result) == 1
    assert result[0].type == "text"
    assert "暂态仿真完成" in result[0].text
    assert "仿真时长" in result[0].text


@pytest.mark.asyncio
async def test_handle_emt_run_with_fault():
    """测试带故障配置的暂态仿真"""
    result = await handle_emt_run({
        "case_name": "test-fault",
        "model_rid": "model/chenying/IEEE39",
        "duration": 10,
        "fault_config": {
            "bus": "BUS16",
            "type": "three_phase",
            "start_time": 1.0,
            "clear_time": 1.1
        },
        "wait": True
    })

    assert len(result) == 1
    assert result[0].type == "text"
    assert "暂态仿真完成" in result[0].text
    assert "故障设置" in result[0].text
    assert "三相短路" in result[0].text


@pytest.mark.asyncio
async def test_handle_result_query():
    """测试任务状态查询"""
    result = await handle_result_query({
        "task_id": "task-test-123",
        "include_data": False
    })

    assert len(result) == 1
    assert result[0].type == "text"
    assert "任务状态查询" in result[0].text
    assert "task-test-123" in result[0].text


@pytest.mark.asyncio
async def test_call_tool_emt_run():
    """测试通过 call_tool 调用 emt_run"""
    result = await call_tool("emt_run", {
        "case_name": "test-emt",
        "model_rid": "model/test/123",
        "duration": 5
    })

    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "暂态仿真完成" in result[0].text


@pytest.mark.asyncio
async def test_call_tool_result_query():
    """测试通过 call_tool 调用 result_query"""
    result = await call_tool("result_query", {
        "task_id": "task-test-456"
    })

    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "任务状态查询" in result[0].text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
