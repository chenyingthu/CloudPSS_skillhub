"""
Phase 3 集成测试

测试智能对话功能：模型搜索、参数建议、结果分析。
"""

import pytest
from datetime import datetime

from cloudpss_skills_v3.mcp_server.handlers.model_search import handle_model_search
from cloudpss_skills_v3.mcp_server.handlers.smart_suggestions import (
    handle_model_analysis,
    analyze_model_for_powerflow,
    analyze_model_for_emt,
    MODEL_CHARACTERISTICS
)
from cloudpss_skills_v3.mcp_server.handlers.result import (
    handle_result_analyze,
    _analyze_voltage,
    _analyze_stability,
    _analyze_losses
)
from cloudpss_skills_v3.core.error_diagnosis import (
    ErrorDiagnoser,
    RetryHandler,
    ErrorType,
    diagnose_error
)
from cloudpss_skills_v3.core.task_store import TaskStatus, get_task_store, reset_task_store


class TestPhase3Integration:
    """Phase 3 集成测试套件"""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """每个测试前重置状态"""
        reset_task_store()
        yield
        reset_task_store()

    @pytest.mark.asyncio
    async def test_model_search_basic(self):
        """测试基本模型搜索"""
        result = await handle_model_search({"keywords": "IEEE39"})

        assert "IEEE 39节点标准系统" in result[0].text
        assert "model/chenying/IEEE39" in result[0].text

    @pytest.mark.asyncio
    async def test_model_search_with_filter(self):
        """测试带过滤器的模型搜索"""
        # 搜索并过滤母线数量
        result = await handle_model_search({
            "keywords": "",
            "filter": {"bus_count": 100}
        })

        assert "IEEE 118节点" in result[0].text

        # 过滤新能源模型
        result = await handle_model_search({
            "keywords": "",
            "filter": {"has_renewable": True}
        })

        assert "分布式电源" in result[0].text

    @pytest.mark.asyncio
    async def test_model_search_no_results(self):
        """测试无结果的搜索"""
        result = await handle_model_search({"keywords": "nonexistent12345"})

        assert "未找到匹配的模型" in result[0].text

    @pytest.mark.asyncio
    async def test_model_analysis_general(self):
        """测试模型综合分析"""
        result = await handle_model_analysis({
            "model_rid": "model/chenying/IEEE39",
            "analysis_type": "general"
        })

        assert "模型分析报告" in result[0].text
        assert "model/chenying/IEEE39" in result[0].text

    @pytest.mark.asyncio
    async def test_model_analysis_powerflow(self):
        """测试潮流计算分析"""
        result = await handle_model_analysis({
            "model_rid": "model/chenying/IEEE39",
            "analysis_type": "powerflow"
        })

        assert "潮流计算分析" in result[0].text

    @pytest.mark.asyncio
    async def test_model_analysis_emt(self):
        """测试暂态仿真分析"""
        result = await handle_model_analysis({
            "model_rid": "model/chenying/WSCC9",
            "analysis_type": "emt"
        })

        assert "暂态仿真分析" in result[0].text

    @pytest.mark.asyncio
    async def test_model_analysis_unknown(self):
        """测试未知模型分析"""
        result = await handle_model_analysis({
            "model_rid": "model/unknown/TEST",
            "analysis_type": "general"
        })

        assert "未找到该模型的详细信息" in result[0].text

    @pytest.mark.asyncio
    async def test_smart_suggestions_powerflow(self):
        """测试潮流计算参数建议"""
        suggestions = await analyze_model_for_powerflow("model/chenying/IEEE39")

        assert "model_info" in suggestions
        assert "recommendations" in suggestions
        assert len(suggestions["recommendations"]) > 0

    @pytest.mark.asyncio
    async def test_smart_suggestions_emt(self):
        """测试暂态仿真参数建议"""
        suggestions = await analyze_model_for_emt(
            "model/chenying/WSCC9",
            duration=5
        )

        assert "model_info" in suggestions
        assert "recommendations" in suggestions
        assert "fault_suggestions" in suggestions

    def test_result_analyze_voltage(self):
        """测试电压分析"""
        result_data = {
            "voltage_min": 0.92,
            "voltage_max": 1.08
        }

        analysis = _analyze_voltage(result_data)

        assert "电压质量分析" in analysis
        assert "0.92" in analysis  # 低电压警告
        assert "1.08" in analysis  # 高电压警告

    def test_result_analyze_stability(self):
        """测试稳定性分析"""
        result_data = {
            "iterations": 3,
            "compute_time": 0.5
        }

        analysis = _analyze_stability(result_data)

        assert "稳定性分析" in analysis
        assert "收敛性良好" in analysis

    def test_result_analyze_losses(self):
        """测试网损分析"""
        result_data = {
            "bus_count": 39,
            "branch_count": 46
        }

        analysis = _analyze_losses(result_data)

        assert "网损分析" in analysis
        assert "39" in analysis
        assert "46" in analysis

    @pytest.mark.asyncio
    async def test_result_analyze_with_task(self):
        """测试基于任务的结果分析"""
        # 创建完成任务
        store = get_task_store()
        store.create_task(
            task_id="test-analyze-task",
            case_name="分析测试",
            model_rid="model/chenying/IEEE39",
            task_type="powerflow"
        )
        store.update_task_status(
            task_id="test-analyze-task",
            status=TaskStatus.COMPLETED,
            progress=100,
            result_data={
                "bus_count": 39,
                "branch_count": 46,
                "voltage_min": 0.98,
                "voltage_max": 1.05,
                "iterations": 4,
                "compute_time": 2.3
            }
        )

        # 分析结果
        result = await handle_result_analyze({
            "task_id": "test-analyze-task",
            "focus": "voltage"
        })

        assert "结果智能分析报告" in result[0].text
        assert "分析测试" in result[0].text
        assert "电压质量分析" in result[0].text

    @pytest.mark.asyncio
    async def test_result_analyze_incomplete_task(self):
        """测试未完成任务的分析"""
        store = get_task_store()
        store.create_task(
            task_id="test-incomplete",
            case_name="未完成测试",
            model_rid="model/chenying/IEEE39",
            task_type="powerflow"
        )

        result = await handle_result_analyze({
            "task_id": "test-incomplete",
            "focus": "general"
        })

        assert "任务尚未完成" in result[0].text

    def test_error_diagnosis_timeout(self):
        """测试超时错误诊断"""
        error = Exception("Request timeout after 30 seconds")
        diagnosis = diagnose_error(error)

        assert diagnosis.error_type == ErrorType.TIMEOUT
        assert diagnosis.can_retry is True
        assert "超时" in diagnosis.message

    def test_error_diagnosis_auth(self):
        """测试认证错误诊断"""
        error = Exception("Unauthorized: invalid token")
        diagnosis = diagnose_error(error)

        assert diagnosis.error_type == ErrorType.AUTHENTICATION
        assert diagnosis.can_retry is False

    def test_error_diagnosis_model_not_found(self):
        """测试模型未找到错误诊断"""
        error = Exception("Model not found: model/test/123")
        diagnosis = diagnose_error(error)

        assert diagnosis.error_type == ErrorType.MODEL_NOT_FOUND
        assert diagnosis.can_retry is False

    def test_error_diagnosis_with_context(self):
        """测试带上下文的错误诊断"""
        error = Exception("Calculation failed")
        context = {
            "task_type": "powerflow",
            "bus_count": 150
        }
        diagnosis = diagnose_error(error, context)

        assert diagnosis.error_type == ErrorType.CALCULATION_FAILED
        assert any("PV节点" in s for s in diagnosis.suggestions)

    def test_retry_handler(self):
        """测试重试处理器"""
        handler = RetryHandler(max_retries=3)

        # 创建可重试的诊断结果
        class MockDiagnosis:
            can_retry = True

        diagnosis = MockDiagnosis()

        # 首次应该允许重试
        assert handler.should_retry("task-1", diagnosis) is True

        # 记录重试
        handler.record_attempt("task-1")
        assert handler.get_retry_count("task-1") == 1

        # 继续重试直到达到上限
        handler.record_attempt("task-1")
        handler.record_attempt("task-1")
        assert handler.get_retry_count("task-1") == 3
        assert handler.should_retry("task-1", diagnosis) is False

        # 重置后应该可以重试
        handler.reset("task-1")
        assert handler.get_retry_count("task-1") == 0

    def test_model_characteristics_database(self):
        """测试模型特性数据库"""
        assert "model/chenying/IEEE39" in MODEL_CHARACTERISTICS
        assert "model/ieee/IEEE118" in MODEL_CHARACTERISTICS

        char = MODEL_CHARACTERISTICS["model/chenying/IEEE39"]
        assert char["type"] == "standard"
        assert char["size"] == "medium"
        assert "recommended_duration" in char


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
