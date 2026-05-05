"""
Phase 4 集成测试

测试高级功能：案例对比、参数扫描、结果导出。
"""

import pytest
import os
import tempfile
import shutil
from datetime import datetime

from cloudpss_skills_v3.mcp_server.handlers.case_compare import (
    handle_case_compare,
    calculate_comparison,
    format_comparison_table
)
from cloudpss_skills_v3.mcp_server.handlers.parameter_sweep import handle_parameter_sweep
from cloudpss_skills_v3.mcp_server.handlers.result import (
    handle_result_export,
    _export_json,
    _export_markdown,
    _export_csv
)
from cloudpss_skills_v3.core.task_store import TaskStatus, get_task_store, reset_task_store


class TestPhase4Integration:
    """Phase 4 集成测试套件"""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """每个测试前重置状态"""
        reset_task_store()
        self.temp_dir = tempfile.mkdtemp()
        yield
        reset_task_store()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @pytest.mark.asyncio
    async def test_case_compare_basic(self):
        """测试基本案例对比"""
        # 创建测试任务
        store = get_task_store()

        # 基准案例
        store.create_task("case-base", "Base Case", "model/test", "powerflow")
        store.update_task_status(
            "case-base",
            TaskStatus.COMPLETED,
            result_data={
                "voltage_min": 0.98,
                "voltage_max": 1.05,
                "bus_count": 39,
                "branch_count": 46,
                "iterations": 4,
                "compute_time": 2.0
            }
        )

        # 对比案例 1
        store.create_task("case-compare-1", "Compare 1", "model/test", "powerflow")
        store.update_task_status(
            "case-compare-1",
            TaskStatus.COMPLETED,
            result_data={
                "voltage_min": 0.96,
                "voltage_max": 1.08,
                "bus_count": 39,
                "branch_count": 46,
                "iterations": 5,
                "compute_time": 2.5
            }
        )

        # 执行对比
        result = await handle_case_compare({
            "case_ids": ["case-base", "case-compare-1"],
            "metrics": ["voltage", "iterations"]
        })

        assert "案例对比分析" in result[0].text
        assert "Base Case" in result[0].text
        assert "Compare 1" in result[0].text

    @pytest.mark.asyncio
    async def test_case_compare_multiple(self):
        """测试多案例对比"""
        store = get_task_store()

        # 创建3个案例
        for i in range(3):
            store.create_task(f"case-{i}", f"Case {i}", "model/test", "powerflow")
            store.update_task_status(
                f"case-{i}",
                TaskStatus.COMPLETED,
                result_data={
                    "voltage_min": 0.95 + i * 0.01,
                    "voltage_max": 1.05 + i * 0.01,
                    "iterations": 4 + i,
                    "compute_time": 2.0 + i * 0.5
                }
            )

        result = await handle_case_compare({
            "case_ids": ["case-0", "case-1", "case-2"],
            "metrics": ["voltage", "iterations", "compute_time"]
        })

        assert "对比案例**: 2 个" in result[0].text
        assert "Case 0" in result[0].text
        assert "Case 1" in result[0].text
        assert "Case 2" in result[0].text

    @pytest.mark.asyncio
    async def test_case_compare_insufficient_cases(self):
        """测试案例数量不足的情况"""
        result = await handle_case_compare({
            "case_ids": ["case-1"],
            "metrics": ["voltage"]
        })

        assert "至少需要提供 2 个案例" in result[0].text

    @pytest.mark.asyncio
    async def test_case_compare_incomplete_case(self):
        """测试未完成案例的对比"""
        store = get_task_store()
        store.create_task("case-incomplete", "Incomplete", "model/test", "powerflow")
        # 不更新状态，保持 pending

        store.create_task("case-complete", "Complete", "model/test", "powerflow")
        store.update_task_status("case-complete", TaskStatus.COMPLETED)

        result = await handle_case_compare({
            "case_ids": ["case-incomplete", "case-complete"],
            "metrics": ["voltage"]
        })

        assert "案例尚未完成" in result[0].text

    def test_calculate_comparison(self):
        """测试对比计算逻辑"""
        baseline = {
            "voltage_min": 0.98,
            "voltage_max": 1.05,
            "iterations": 4,
            "compute_time": 2.0
        }

        compare_list = [
            {
                "voltage_min": 0.96,
                "voltage_max": 1.08,
                "iterations": 5,
                "compute_time": 2.5
            }
        ]

        metrics = ["voltage", "iterations"]
        result = calculate_comparison(baseline, compare_list, metrics)

        assert "voltage" in result
        assert result["voltage"]["baseline"] == 0.98
        assert len(result["voltage"]["values"]) == 1

    def test_format_comparison_table(self):
        """测试对比表格格式化"""
        comparison = {
            "voltage": {
                "name": "voltage_min",
                "unit": "pu",
                "baseline": 0.98,
                "values": [0.96],
                "differences": [-0.02],
                "percent_changes": [-2.04]
            }
        }

        table = format_comparison_table(comparison, ["Case 1"])

        assert "指标" in table
        assert "0.980" in table or "0.98" in table
        assert "0.960" in table or "0.96" in table

    @pytest.mark.asyncio
    async def test_parameter_sweep_basic(self):
        """测试基本参数扫描"""
        # 创建基准案例
        store = get_task_store()
        store.create_task(
            "sweep-base",
            "Sweep Base",
            "model/chenying/IEEE39",
            "powerflow"
        )
        store.update_task_status(
            "sweep-base",
            TaskStatus.COMPLETED,
            result_data={
                "voltage_min": 0.98,
                "voltage_max": 1.05,
                "bus_count": 39,
                "branch_count": 46,
                "iterations": 4,
                "compute_time": 2.3
            }
        )

        # 执行参数扫描
        result = await handle_parameter_sweep({
            "base_case": "sweep-base",
            "parameter": "load_p",
            "range": [0.8, 0.9, 1.0, 1.1, 1.2],
            "parallel": False  # 串行以避免测试复杂度
        })

        assert "参数扫描完成" in result[0].text
        assert "load_p" in result[0].text
        assert "参数范围" in result[0].text

    @pytest.mark.asyncio
    async def test_parameter_sweep_invalid_base(self):
        """测试无效基准案例"""
        result = await handle_parameter_sweep({
            "base_case": "nonexistent",
            "parameter": "test",
            "range": [1, 2, 3]
        })

        assert "未找到基准案例" in result[0].text

    @pytest.mark.asyncio
    async def test_parameter_sweep_missing_params(self):
        """测试缺少参数"""
        result = await handle_parameter_sweep({
            "base_case": "test"
        })

        assert "参数错误" in result[0].text

    def test_export_json(self):
        """测试 JSON 导出"""
        from cloudpss_skills_v3.core.task_store import TaskInfo, TaskStatus

        task = TaskInfo(
            task_id="test-task",
            case_name="Test Export",
            model_rid="model/test",
            task_type="powerflow",
            status=TaskStatus.COMPLETED,
            progress=100,
            message="Done",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            completed_at=datetime.now()
        )

        result_data = {
            "voltage_min": 0.98,
            "voltage_max": 1.05,
            "bus_count": 39
        }

        content = _export_json(task, result_data)

        assert "test-task" in content
        assert "Test Export" in content
        assert '"voltage_min": 0.98' in content

    def test_export_markdown(self):
        """测试 Markdown 导出"""
        from cloudpss_skills_v3.core.task_store import TaskInfo, TaskStatus

        task = TaskInfo(
            task_id="test-task",
            case_name="Test Export",
            model_rid="model/test",
            task_type="powerflow",
            status=TaskStatus.COMPLETED,
            progress=100,
            message="Done",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            completed_at=datetime.now()
        )

        result_data = {
            "voltage_min": 0.98,
            "voltage_max": 1.05,
            "bus_count": 39
        }

        content = _export_markdown(task, result_data)

        assert "# 仿真结果报告" in content
        assert "Test Export" in content
        assert "电压最小值" in content

    def test_export_csv(self):
        """测试 CSV 导出"""
        from cloudpss_skills_v3.core.task_store import TaskInfo, TaskStatus

        task = TaskInfo(
            task_id="test-task",
            case_name="Test Export",
            model_rid="model/test",
            task_type="powerflow",
            status=TaskStatus.COMPLETED,
            progress=100,
            message="Done",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        result_data = {
            "voltage_min": 0.98,
            "voltage_max": 1.05,
            "bus_count": 39
        }

        content = _export_csv(task, result_data)

        assert "指标,数值,单位" in content
        assert "test-task" in content
        assert "0.98" in content

    @pytest.mark.asyncio
    async def test_result_export_json(self):
        """测试 JSON 格式导出"""
        store = get_task_store()
        store.create_task("export-task", "Export Test", "model/test", "powerflow")
        store.update_task_status(
            "export-task",
            TaskStatus.COMPLETED,
            result_data={
                "voltage_min": 0.98,
                "voltage_max": 1.05,
                "bus_count": 39,
                "branch_count": 46,
                "iterations": 4,
                "compute_time": 2.3
            }
        )

        result = await handle_result_export({
            "task_id": "export-task",
            "format": "json",
            "output_path": self.temp_dir
        })

        assert "导出成功" in result[0].text
        assert ".json" in result[0].text

    @pytest.mark.asyncio
    async def test_result_export_csv(self):
        """测试 CSV 格式导出"""
        store = get_task_store()
        store.create_task("export-csv", "Export CSV", "model/test", "powerflow")
        store.update_task_status(
            "export-csv",
            TaskStatus.COMPLETED,
            result_data={
                "voltage_min": 0.98,
                "voltage_max": 1.05,
                "bus_count": 39,
                "branch_count": 46,
                "iterations": 4,
                "compute_time": 2.3
            }
        )

        result = await handle_result_export({
            "task_id": "export-csv",
            "format": "csv",
            "output_path": self.temp_dir
        })

        assert "导出成功" in result[0].text
        assert ".csv" in result[0].text

    @pytest.mark.asyncio
    async def test_result_export_markdown(self):
        """测试 Markdown 格式导出"""
        store = get_task_store()
        store.create_task("export-md", "Export MD", "model/test", "powerflow")
        store.update_task_status(
            "export-md",
            TaskStatus.COMPLETED,
            result_data={
                "voltage_min": 0.98,
                "voltage_max": 1.05,
                "bus_count": 39,
                "branch_count": 46,
                "iterations": 4,
                "compute_time": 2.3
            }
        )

        result = await handle_result_export({
            "task_id": "export-md",
            "format": "md",
            "output_path": self.temp_dir
        })

        assert "导出成功" in result[0].text
        assert ".md" in result[0].text

    @pytest.mark.asyncio
    async def test_result_export_incomplete_task(self):
        """测试未完成任务的导出"""
        store = get_task_store()
        store.create_task("export-incomplete", "Incomplete", "model/test", "powerflow")

        result = await handle_result_export({
            "task_id": "export-incomplete",
            "format": "csv"
        })

        assert "任务尚未完成" in result[0].text

    @pytest.mark.asyncio
    async def test_result_export_nonexistent(self):
        """测试不存在的任务导出"""
        result = await handle_result_export({
            "task_id": "nonexistent",
            "format": "json"
        })

        assert "未找到任务" in result[0].text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
