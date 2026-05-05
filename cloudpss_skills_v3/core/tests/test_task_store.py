"""
TaskStore 单元测试

测试任务状态存储和管理功能。
"""

import pytest
import tempfile
import shutil
from datetime import datetime
from pathlib import Path

from cloudpss_skills_v3.core.task_store import (
    TaskStore,
    TaskInfo,
    TaskStatus,
    get_task_store,
    reset_task_store
)


class TestTaskStore:
    """TaskStore 测试套件"""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """每个测试前重置 TaskStore"""
        reset_task_store()
        self.temp_dir = tempfile.mkdtemp()
        yield
        # 清理
        reset_task_store()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_singleton_pattern(self):
        """测试单例模式"""
        store1 = TaskStore(self.temp_dir)
        store2 = TaskStore(self.temp_dir)
        assert store1 is store2

    def test_create_task(self):
        """测试创建任务"""
        store = TaskStore(self.temp_dir)

        task = store.create_task(
            task_id="task-001",
            case_name="IEEE39-测试",
            model_rid="model/chenying/IEEE39",
            task_type="powerflow"
        )

        assert task.task_id == "task-001"
        assert task.case_name == "IEEE39-测试"
        assert task.model_rid == "model/chenying/IEEE39"
        assert task.task_type == "powerflow"
        assert task.status == TaskStatus.PENDING
        assert task.progress == 0

    def test_get_task(self):
        """测试获取任务"""
        store = TaskStore(self.temp_dir)

        # 创建任务
        store.create_task(
            task_id="task-002",
            case_name="测试案例",
            model_rid="model/test/123"
        )

        # 获取任务
        task = store.get_task("task-002")
        assert task is not None
        assert task.case_name == "测试案例"

        # 获取不存在的任务
        task = store.get_task("task-nonexistent")
        assert task is None

    def test_update_task_status(self):
        """测试更新任务状态"""
        store = TaskStore(self.temp_dir)

        # 创建任务
        store.create_task(
            task_id="task-003",
            case_name="测试",
            model_rid="model/test"
        )

        # 更新状态为运行中
        updated = store.update_task_status(
            task_id="task-003",
            status=TaskStatus.RUNNING,
            progress=50,
            message="正在计算..."
        )

        assert updated is not None
        assert updated.status == TaskStatus.RUNNING
        assert updated.progress == 50
        assert updated.message == "正在计算..."

        # 更新状态为完成
        updated = store.update_task_status(
            task_id="task-003",
            status=TaskStatus.COMPLETED,
            progress=100,
            message="计算完成",
            result_data={"voltage": 1.0}
        )

        assert updated.status == TaskStatus.COMPLETED
        assert updated.completed_at is not None
        assert updated.result_data == {"voltage": 1.0}

    def test_list_tasks(self):
        """测试列出任务"""
        store = TaskStore(self.temp_dir)

        # 创建多个任务
        for i in range(5):
            store.create_task(
                task_id=f"task-{i:03d}",
                case_name=f"案例-{i}",
                model_rid="model/test"
            )

        # 列出所有任务
        tasks = store.list_tasks()
        assert len(tasks) == 5

        # 更新部分任务状态
        store.update_task_status("task-001", TaskStatus.COMPLETED)
        store.update_task_status("task-002", TaskStatus.RUNNING)

        # 按状态过滤
        completed = store.list_tasks(status=TaskStatus.COMPLETED)
        assert len(completed) == 1
        assert completed[0].task_id == "task-001"

        running = store.list_tasks(status=TaskStatus.RUNNING)
        assert len(running) == 1
        assert running[0].task_id == "task-002"

    def test_delete_task(self):
        """测试删除任务"""
        store = TaskStore(self.temp_dir)

        # 创建任务
        store.create_task(
            task_id="task-del",
            case_name="待删除",
            model_rid="model/test"
        )

        # 删除任务
        result = store.delete_task("task-del")
        assert result is True

        # 确认已删除
        task = store.get_task("task-del")
        assert task is None

        # 删除不存在的任务
        result = store.delete_task("task-nonexistent")
        assert result is False

    def test_persistence(self):
        """测试持久化功能"""
        store1 = TaskStore(self.temp_dir)

        # 创建并更新任务
        store1.create_task(
            task_id="task-persist",
            case_name="持久化测试",
            model_rid="model/test"
        )
        store1.update_task_status(
            task_id="task-persist",
            status=TaskStatus.COMPLETED,
            progress=100,
            result_data={"data": "test"}
        )

        # 重置单例并创建新实例
        reset_task_store()
        store2 = TaskStore(self.temp_dir)
        store2.load_all_tasks()

        # 验证数据已加载
        task = store2.get_task("task-persist")
        assert task is not None
        assert task.case_name == "持久化测试"
        assert task.status == TaskStatus.COMPLETED
        assert task.result_data == {"data": "test"}

    def test_task_info_to_dict(self):
        """测试 TaskInfo 序列化"""
        now = datetime.now()
        task = TaskInfo(
            task_id="task-001",
            case_name="测试",
            model_rid="model/test",
            task_type="powerflow",
            status=TaskStatus.RUNNING,
            progress=50,
            message="运行中",
            created_at=now,
            updated_at=now
        )

        data = task.to_dict()
        assert data["task_id"] == "task-001"
        assert data["status"] == "running"
        assert data["progress"] == 50

    def test_task_info_from_dict(self):
        """测试 TaskInfo 反序列化"""
        now = datetime.now().isoformat()
        data = {
            "task_id": "task-002",
            "case_name": "测试",
            "model_rid": "model/test",
            "task_type": "emt",
            "status": "completed",
            "progress": 100,
            "message": "完成",
            "created_at": now,
            "updated_at": now,
            "completed_at": now,
            "result_data": {"voltage": 1.0}
        }

        task = TaskInfo.from_dict(data)
        assert task.task_id == "task-002"
        assert task.status == TaskStatus.COMPLETED
        assert task.result_data == {"voltage": 1.0}

    def test_update_nonexistent_task(self):
        """测试更新不存在的任务"""
        store = TaskStore(self.temp_dir)

        result = store.update_task_status(
            task_id="task-nonexistent",
            status=TaskStatus.COMPLETED
        )
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
