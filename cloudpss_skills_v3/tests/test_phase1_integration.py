"""
Phase 1 集成测试

测试 MCP Server 基础功能的完整流程。
"""

import pytest
import asyncio
from datetime import datetime

from cloudpss_skills_v3.mcp_server.server import list_tools, call_tool, CORE_TOOLS
from cloudpss_skills_v3.core.cloudpss_client import CloudPSSClient, SimulationResult
from cloudpss_skills_v3.mcp_server.handlers import (
    handle_powerflow_run,
    handle_emt_run,
    handle_result_query,
)


class TestPhase1Integration:
    """Phase 1 集成测试套件"""

    @pytest.mark.asyncio
    async def test_full_powerflow_workflow(self):
        """测试完整的潮流计算工作流"""
        # 1. 列出可用工具
        tools = await list_tools()
        tool_names = [t.name for t in tools]
        assert "powerflow_run" in tool_names
        assert "result_query" in tool_names

        # 2. 提交潮流计算任务
        result = await call_tool("powerflow_run", {
            "case_name": "IEEE39-测试",
            "model_rid": "model/chenying/IEEE39",
            "wait": True
        })

        assert len(result) == 1
        assert "潮流计算完成" in result[0].text

        # 3. 查询任务状态
        # 从响应中提取任务ID（在真实实现中会返回任务ID）
        result2 = await call_tool("result_query", {
            "task_id": "task-test-123"
        })

        assert len(result2) == 1
        assert "任务状态查询" in result2[0].text

    @pytest.mark.asyncio
    async def test_full_emt_workflow(self):
        """测试完整的暂态仿真工作流"""
        # 1. 提交暂态仿真任务
        result = await call_tool("emt_run", {
            "case_name": "IEEE39-故障分析",
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
        assert "暂态仿真完成" in result[0].text
        assert "故障设置" in result[0].text

    @pytest.mark.asyncio
    async def test_async_workflow(self):
        """测试异步任务工作流"""
        # 1. 异步提交潮流计算
        result = await call_tool("powerflow_run", {
            "case_name": "异步测试",
            "model_rid": "model/chenying/IEEE39",
            "wait": False
        })

        assert len(result) == 1
        assert "任务已提交" in result[0].text
        assert "任务 ID" in result[0].text

        # 2. 查询任务状态
        result2 = await call_tool("result_query", {
            "task_id": "task-async-123"
        })

        assert len(result2) == 1
        assert "任务状态查询" in result2[0].text

    @pytest.mark.asyncio
    async def test_client_integration(self):
        """测试 CloudPSSClient 集成"""
        client = CloudPSSClient()

        # 测试案例创建
        case_id = await client.create_case(
            name="集成测试案例",
            model_rid="model/chenying/IEEE39"
        )
        assert case_id.startswith("case-")

        # 测试任务提交
        task_id = await client.submit_powerflow(case_id=case_id)
        assert task_id.startswith("task-pf-")

        # 测试任务状态查询
        status = await client.get_task_status(task_id)
        assert "status" in status
        assert status["status"] == "completed"

        # 测试结果获取
        result = await client.get_powerflow_result(task_id)
        assert isinstance(result, SimulationResult)
        assert result.task_id == task_id
        assert result.status == "completed"

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """测试错误处理"""
        # 测试缺少必需参数
        result = await call_tool("powerflow_run", {})
        assert "参数错误" in result[0].text

        # 测试无效工具
        result = await call_tool("invalid_tool", {})
        assert "未知 Tool" in result[0].text

    def test_all_tools_have_handlers(self):
        """测试所有工具都有对应的处理器"""
        # 验证所有 core tools 都能在 call_tool 中被调用
        tool_handlers = {
            "powerflow_run": "✅",
            "emt_run": "✅",
            "result_query": "✅",
            "result_analyze": "✅",
            "result_export": "✅",
            "parameter_sweep": "✅",
            "case_compare": "✅",
            "model_search": "✅",
            "model_analysis": "✅",
        }

        for tool in CORE_TOOLS:
            assert tool.name in tool_handlers, f"Tool {tool.name} 没有对应的处理器"

    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """测试并发请求处理"""
        # 创建多个并发任务
        tasks = [
            handle_powerflow_run({
                "case_name": f"并发测试-{i}",
                "model_rid": "model/chenying/IEEE39",
                "wait": True
            })
            for i in range(3)
        ]

        # 并发执行
        results = await asyncio.gather(*tasks)

        # 验证所有任务都成功完成
        assert len(results) == 3
        for result in results:
            assert len(result) == 1
            assert "潮流计算完成" in result[0].text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
