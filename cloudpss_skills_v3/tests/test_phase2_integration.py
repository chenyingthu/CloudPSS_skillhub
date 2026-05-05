"""
Phase 2 集成测试

测试异步任务管理和 Observation Portal 功能。
"""

import pytest
import asyncio
import tempfile
import shutil
from datetime import datetime, timedelta

from cloudpss_skills_v3.core.task_store import (
    TaskStore, TaskStatus, TaskInfo, get_task_store, reset_task_store
)
from cloudpss_skills_v3.mcp_server.handlers.powerflow import handle_powerflow_run
from cloudpss_skills_v3.mcp_server.handlers.result import handle_result_query
from cloudpss_skills_v3.portal.app import create_app


class TestPhase2Integration:
    """Phase 2 集成测试套件"""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """每个测试前重置状态"""
        reset_task_store()
        self.temp_dir = tempfile.mkdtemp()
        yield
        reset_task_store()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @pytest.mark.asyncio
    async def test_async_task_workflow(self):
        """测试完整的异步任务工作流"""
        # 1. 异步提交任务（不等待）
        result = await handle_powerflow_run({
            "case_name": "异步测试案例",
            "model_rid": "model/chenying/IEEE39",
            "wait": False
        })

        assert "任务已提交" in result[0].text

        # 提取任务ID
        import re
        match = re.search(r'任务 ID\*\*: (task-\S+)', result[0].text)
        assert match, "Should find task ID in response"
        task_id = match.group(1)

        # 2. 验证任务已存储
        task_store = get_task_store()
        task = task_store.get_task(task_id)
        assert task is not None
        assert task.status == TaskStatus.RUNNING
        assert task.case_name == "异步测试案例"

        # 3. 查询任务状态
        result = await handle_result_query({
            "task_id": task_id,
            "include_data": False
        })

        assert "任务状态查询" in result[0].text
        assert task_id in result[0].text

    @pytest.mark.asyncio
    async def test_sync_task_updates_status(self):
        """测试同步任务更新状态"""
        # 同步执行任务
        result = await handle_powerflow_run({
            "case_name": "同步测试案例",
            "model_rid": "model/chenying/IEEE39",
            "wait": True
        })

        assert "潮流计算完成" in result[0].text

        # 从响应中提取任务ID
        import re
        match = re.search(r'任务 ID\*\*: (task-\S+)', result[0].text)
        assert match, "Should find task ID in response"
        task_id = match.group(1)

        # 验证特定任务状态为已完成
        task_store = get_task_store()
        task = task_store.get_task(task_id)
        assert task is not None
        assert task.status == TaskStatus.COMPLETED
        assert task.progress == 100
        assert task.result_data is not None
        assert "bus_count" in task.result_data

    @pytest.mark.asyncio
    async def test_concurrent_tasks_status_tracking(self):
        """测试并发任务状态跟踪"""
        import re

        # 创建多个并发任务
        task_params = [
            {"case_name": f"并发任务-{i}", "model_rid": "model/chenying/IEEE39", "wait": False}
            for i in range(5)
        ]

        tasks = [handle_powerflow_run(params) for params in task_params]
        results = await asyncio.gather(*tasks)

        # 验证所有任务都提交成功并收集任务ID
        assert len(results) == 5
        task_ids = []
        for result in results:
            assert "任务已提交" in result[0].text
            match = re.search(r'任务 ID\*\*: (task-\S+)', result[0].text)
            assert match, "Should find task ID in response"
            task_ids.append(match.group(1))

        # 验证每个特定任务都在运行状态或已完成状态（快速任务可能已完成）
        task_store = get_task_store()
        for task_id in task_ids:
            task = task_store.get_task(task_id)
            assert task is not None
            assert task.case_name.startswith("并发任务-")
            assert task.status in [TaskStatus.RUNNING, TaskStatus.COMPLETED]

    def test_task_store_persistence(self):
        """测试任务存储持久化"""
        store1 = TaskStore(self.temp_dir)

        # 创建任务
        store1.create_task(
            task_id="persist-task",
            case_name="持久化测试",
            model_rid="model/test",
            task_type="powerflow"
        )
        store1.update_task_status(
            task_id="persist-task",
            status=TaskStatus.COMPLETED,
            progress=100,
            result_data={"voltage": 1.05}
        )

        # 重置单例并重新加载
        reset_task_store()
        store2 = TaskStore(self.temp_dir)
        store2.load_all_tasks()

        # 验证任务被正确加载
        task = store2.get_task("persist-task")
        assert task is not None
        assert task.case_name == "持久化测试"
        assert task.status == TaskStatus.COMPLETED
        assert task.result_data == {"voltage": 1.05}

    def test_task_store_status_filtering(self):
        """测试任务状态过滤"""
        store = TaskStore(self.temp_dir)

        # 创建不同状态的任务
        for i, status in enumerate([TaskStatus.PENDING, TaskStatus.RUNNING,
                                     TaskStatus.COMPLETED, TaskStatus.FAILED]):
            store.create_task(
                task_id=f"task-{status.value}",
                case_name=f"Case {i}",
                model_rid="model/test"
            )
            store.update_task_status(f"task-{status.value}", status)

        # 测试过滤
        completed = store.list_tasks(status=TaskStatus.COMPLETED)
        assert len(completed) == 1
        assert completed[0].status == TaskStatus.COMPLETED

        running = store.list_tasks(status=TaskStatus.RUNNING)
        assert len(running) == 1
        assert running[0].status == TaskStatus.RUNNING

    def test_portal_api_integration(self):
        """测试 Portal API 与任务存储集成"""
        # 创建一些测试任务
        store = TaskStore(self.temp_dir)
        for i in range(3):
            store.create_task(
                task_id=f"portal-task-{i}",
                case_name=f"Portal Test {i}",
                model_rid="model/chenying/IEEE39",
                task_type="powerflow"
            )
            if i < 2:
                store.update_task_status(
                    f"portal-task-{i}",
                    TaskStatus.COMPLETED,
                    progress=100
                )

        # 创建测试客户端
        app = create_app()
        app.config['TESTING'] = True
        client = app.test_client()

        # 测试仪表板统计 API
        response = client.get('/api/dashboard/stats')
        assert response.status_code == 200
        data = response.get_json()

        assert data['stats']['total_tasks'] == 3
        assert data['stats']['completed'] == 2
        assert data['stats']['running'] == 0

        # 测试任务列表 API
        response = client.get('/api/tasks')
        assert response.status_code == 200
        data = response.get_json()
        assert data['total'] == 3

    def test_portal_task_detail_api(self):
        """测试 Portal 任务详情 API"""
        # 创建带详细数据的任务
        store = TaskStore(self.temp_dir)
        store.create_task(
            task_id="detail-task",
            case_name="Detail Test",
            model_rid="model/chenying/IEEE39",
            task_type="emt"
        )
        store.update_task_status(
            task_id="detail-task",
            status=TaskStatus.COMPLETED,
            progress=100,
            message="暂态仿真完成",
            result_data={
                "bus_count": 39,
                "branch_count": 46,
                "voltage_min": 0.98,
                "voltage_max": 1.05
            }
        )

        # 创建测试客户端
        app = create_app()
        app.config['TESTING'] = True
        client = app.test_client()

        # 测试任务详情 API
        response = client.get('/api/tasks/detail-task')
        assert response.status_code == 200
        data = response.get_json()

        assert data['task_id'] == 'detail-task'
        assert data['case_name'] == 'Detail Test'
        assert data['task_type'] == 'emt'
        assert data['status'] == 'completed'
        assert data['result_data']['bus_count'] == 39
        assert data['result_data']['voltage_min'] == 0.98

    def test_task_status_timestamps(self):
        """测试任务状态时间戳"""
        store = TaskStore(self.temp_dir)

        # 创建任务
        task = store.create_task(
            task_id="timestamp-task",
            case_name="Timestamp Test",
            model_rid="model/test"
        )

        created_at = task.created_at
        assert isinstance(created_at, datetime)

        # 更新状态
        updated = store.update_task_status(
            task_id="timestamp-task",
            status=TaskStatus.COMPLETED
        )

        assert updated.completed_at is not None
        assert isinstance(updated.completed_at, datetime)
        assert updated.completed_at >= created_at

    def test_task_list_ordering(self):
        """测试任务列表排序"""
        store = TaskStore(self.temp_dir)

        # 创建多个任务（按时间顺序）
        for i in range(5):
            store.create_task(
                task_id=f"order-task-{i}",
                case_name=f"Order Test {i}",
                model_rid="model/test"
            )

        # 获取任务列表
        tasks = store.list_tasks(limit=10)

        # 验证按时间倒序排列（最新的在前）
        for i in range(len(tasks) - 1):
            assert tasks[i].created_at >= tasks[i + 1].created_at

    def test_task_limit(self):
        """测试任务列表限制"""
        store = TaskStore(self.temp_dir)

        # 创建20个任务
        for i in range(20):
            store.create_task(
                task_id=f"limit-task-{i}",
                case_name=f"Limit Test {i}",
                model_rid="model/test"
            )

        # 测试不同限制
        assert len(store.list_tasks(limit=5)) == 5
        assert len(store.list_tasks(limit=10)) == 10
        assert len(store.list_tasks(limit=100)) == 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
