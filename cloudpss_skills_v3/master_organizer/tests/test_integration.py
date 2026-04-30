"""
集成测试 - 验证各组件协同工作
"""

import pytest
import tempfile
import shutil
from pathlib import Path

from cloudpss_skills_v3.master_organizer.core import (
    IDGenerator, EntityType,
    PathManager, ConfigManager,
    ServerRegistry, CaseRegistry, TaskRegistry,
    Server, Case, Task
)


class TestFullWorkflow:
    """完整工作流测试"""

    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.pm = PathManager(self.temp_dir)
        self.cm = ConfigManager(self.temp_dir / "config")

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_server_and_case(self):
        """测试创建服务器和算例的完整流程"""
        # 1. 创建服务器
        server_id = IDGenerator.generate(EntityType.SERVER)
        server = Server(
            id=server_id,
            name="测试服务器",
            url="https://test.cloudpss.net"
        )

        server_registry = ServerRegistry(self.pm.registry_dir)
        assert server_registry.create(server_id, server)

        # 2. 创建算例
        case_id = IDGenerator.generate(EntityType.CASE)
        case = Case(
            id=case_id,
            name="IEEE14_测试",
            rid="model/holdme/IEEE14",
            server_id=server_id
        )

        case_registry = CaseRegistry(self.pm.registry_dir)
        assert case_registry.create(case_id, case)

        # 3. 验证关联
        retrieved_case = case_registry.get(case_id)
        assert retrieved_case.server_id == server_id

        # 4. 验证路径正确（目录在需要时创建，注册表不负责创建目录）
        case_path = self.pm.get_case_path(case_id)
        assert str(case_path).endswith(case_id)

    def test_case_task_result_workflow(self):
        """测试算例-任务-结果工作流"""
        # 创建算例
        case_id = IDGenerator.generate(EntityType.CASE)
        case = Case(id=case_id, name="测试算例")
        case_registry = CaseRegistry(self.pm.registry_dir)
        case_registry.create(case_id, case)

        # 创建任务
        task_id = IDGenerator.generate(EntityType.TASK)
        task = Task(
            id=task_id,
            name="潮流计算",
            case_id=case_id,
            type="powerflow"
        )
        task_registry = TaskRegistry(self.pm.registry_dir)
        task_registry.create(task_id, task)

        # 更新任务状态
        task_registry.update(task_id, {"status": "completed"})

        # 验证状态更新
        updated_task = task_registry.get(task_id)
        assert updated_task.status == "completed"
        assert updated_task.case_id == case_id

    def test_persistence_across_instances(self):
        """测试跨实例持久化"""
        # 第一个实例创建数据
        case_id = IDGenerator.generate(EntityType.CASE)
        case = Case(id=case_id, name="持久化测试")

        registry1 = CaseRegistry(self.pm.registry_dir)
        registry1.create(case_id, case)

        # 第二个实例读取数据
        registry2 = CaseRegistry(self.pm.registry_dir)
        retrieved = registry2.get(case_id)

        assert retrieved is not None
        assert retrieved.name == "持久化测试"


class TestConfigAndPathIntegration:
    """配置和路径集成测试"""

    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_config_saved_to_correct_location(self):
        """测试配置保存到正确位置"""
        pm = PathManager(self.temp_dir)
        cm = ConfigManager(pm.config_dir)

        # 保存配置
        cm.save("test", {"key": "value"})

        # 验证文件位置
        config_file = pm.config_dir / "test.yaml"
        assert config_file.exists()

    def test_registry_saved_to_correct_location(self):
        """测试注册表保存到正确位置"""
        pm = PathManager(self.temp_dir)
        registry = CaseRegistry(pm.registry_dir)

        # 创建条目
        case_id = IDGenerator.generate(EntityType.CASE)
        case = Case(id=case_id, name="位置测试")
        registry.create(case_id, case)

        # 验证文件位置
        registry_file = pm.registry_dir / "cases.yaml"
        assert registry_file.exists()


class TestErrorHandling:
    """错误处理测试"""

    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_duplicate_case(self):
        """测试创建重复算例"""
        registry = CaseRegistry(self.temp_dir)
        case_id = IDGenerator.generate(EntityType.CASE)
        case = Case(id=case_id, name="测试")

        assert registry.create(case_id, case)
        assert not registry.create(case_id, case)  # 重复创建应失败

    def test_update_nonexistent_case(self):
        """测试更新不存在的算例"""
        registry = CaseRegistry(self.temp_dir)
        case_id = IDGenerator.generate(EntityType.CASE)

        assert not registry.update(case_id, {"name": "新名称"})

    def test_delete_nonexistent_case(self):
        """测试删除不存在的算例"""
        registry = CaseRegistry(self.temp_dir)
        case_id = IDGenerator.generate(EntityType.CASE)

        assert not registry.delete(case_id)

    def test_get_nonexistent_case(self):
        """测试获取不存在的算例"""
        registry = CaseRegistry(self.temp_dir)
        case_id = IDGenerator.generate(EntityType.CASE)

        assert registry.get(case_id) is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
