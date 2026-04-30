"""
注册表测试
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from dataclasses import asdict

from cloudpss_skills_v3.master_organizer.core import (
    IDGenerator, EntityType, RegistryBase, RegistryEntry,
    ServerRegistry, CaseRegistry, TaskRegistry, ResultRegistry,
    Server, Case, Task, Result
)


class TestServerRegistry:
    """服务器注册表测试"""

    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.registry = ServerRegistry(self.temp_dir)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_server(self):
        """测试创建服务器"""
        server_id = IDGenerator.generate(EntityType.SERVER)
        server = Server(
            id=server_id,
            name="测试服务器",
            url="https://test.cloudpss.net"
        )

        assert self.registry.create(server_id, server)
        assert self.registry.exists(server_id)

        retrieved = self.registry.get(server_id)
        assert retrieved.name == "测试服务器"
        assert retrieved.url == "https://test.cloudpss.net"

    def test_update_server(self):
        """测试更新服务器"""
        server_id = IDGenerator.generate(EntityType.SERVER)
        server = Server(id=server_id, name="旧名称", url="https://old.url")
        self.registry.create(server_id, server)

        assert self.registry.update(server_id, {"name": "新名称"})

        updated = self.registry.get(server_id)
        assert updated.name == "新名称"

    def test_delete_server(self):
        """测试删除服务器"""
        server_id = IDGenerator.generate(EntityType.SERVER)
        server = Server(id=server_id, name="删除测试", url="https://test.url")
        self.registry.create(server_id, server)

        assert self.registry.delete(server_id)
        assert not self.registry.exists(server_id)

    def test_list_all_servers(self):
        """测试列出所有服务器"""
        for i in range(3):
            server_id = IDGenerator.generate(EntityType.SERVER)
            server = Server(id=server_id, name=f"服务器{i}", url="https://test.url")
            self.registry.create(server_id, server)

        servers = self.registry.list_all()
        assert len(servers) == 3

    def test_search_servers(self):
        """测试搜索服务器"""
        server_id = IDGenerator.generate(EntityType.SERVER)
        server = Server(id=server_id, name="生产环境", url="https://prod.url")
        self.registry.create(server_id, server)

        results = self.registry.search("生产")
        assert len(results) == 1
        assert results[0][1].name == "生产环境"


class TestCaseRegistry:
    """算例注册表测试"""

    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.registry = CaseRegistry(self.temp_dir)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_case(self):
        """测试创建算例"""
        case_id = IDGenerator.generate(EntityType.CASE)
        case = Case(
            id=case_id,
            name="IEEE14_基态潮流",
            rid="model/holdme/IEEE14",
            server_id="server_a3f7b2d9"
        )

        assert self.registry.create(case_id, case)
        assert self.registry.exists(case_id)

    def test_filter_by_status(self):
        """测试按状态过滤"""
        # 创建活跃算例
        active_id = IDGenerator.generate(EntityType.CASE)
        active_case = Case(id=active_id, name="活跃算例", status="active")
        self.registry.create(active_id, active_case)

        # 创建草稿算例
        draft_id = IDGenerator.generate(EntityType.CASE)
        draft_case = Case(id=draft_id, name="草稿算例", status="draft")
        self.registry.create(draft_id, draft_case)

        # 过滤
        active_cases = self.registry.filter_by(status="active")
        assert len(active_cases) == 1
        assert active_cases[0][1].name == "活跃算例"


class TestTaskRegistry:
    """任务注册表测试"""

    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.registry = TaskRegistry(self.temp_dir)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_task(self):
        """测试创建任务"""
        task_id = IDGenerator.generate(EntityType.TASK)
        task = Task(
            id=task_id,
            name="潮流计算",
            case_id="case_20260430_143052_a3f7b2d9",
            type="powerflow"
        )

        assert self.registry.create(task_id, task)
        assert self.registry.exists(task_id)

    def test_task_lifecycle(self):
        """测试任务生命周期"""
        task_id = IDGenerator.generate(EntityType.TASK)
        task = Task(
            id=task_id,
            name="EMT仿真",
            case_id="case_20260430_143052_a3f7b2d9",
            type="emt",
            status="created"
        )
        self.registry.create(task_id, task)

        # 更新状态
        assert self.registry.update(task_id, {"status": "running"})
        updated = self.registry.get(task_id)
        assert updated.status == "running"


class TestRegistryCRUD:
    """注册表 CRUD 测试"""

    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.registry = CaseRegistry(self.temp_dir)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_bulk_create(self):
        """测试批量创建"""
        entries = {}
        for i in range(5):
            case_id = IDGenerator.generate(EntityType.CASE)
            case = Case(id=case_id, name=f"算例{i}")
            entries[case_id] = case

        count = self.registry.bulk_create(entries)
        assert count == 5
        assert self.registry.count() == 5

    def test_bulk_delete(self):
        """测试批量删除"""
        case_ids = []
        for i in range(3):
            case_id = IDGenerator.generate(EntityType.CASE)
            case = Case(id=case_id, name=f"算例{i}")
            self.registry.create(case_id, case)
            case_ids.append(case_id)

        count = self.registry.bulk_delete(case_ids)
        assert count == 3
        assert self.registry.count() == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
