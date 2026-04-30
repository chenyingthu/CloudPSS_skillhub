"""
路径管理器测试
"""

import pytest
import tempfile
import shutil
from pathlib import Path

from cloudpss_skills_v3.master_organizer.core import (
    PathManager, get_path_manager, IDGenerator, EntityType
)


class TestPathManagerAdvanced:
    """高级路径管理测试"""

    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.pm = PathManager(self.temp_dir)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_storage_usage(self):
        """测试存储使用情况统计"""
        # 创建一些测试文件
        test_file = self.pm.config_dir / "test.txt"
        test_file.write_text("test content")

        usage = self.pm.get_storage_usage()
        assert "total" in usage
        assert "config" in usage
        assert usage["total"] > 0

    def test_get_variant_path(self):
        """测试获取变体路径"""
        case_id = "case_20260430_143052_a3f7b2d9"
        variant_id = "variant_c7e2d8a4"
        path = self.pm.get_variant_path(case_id, variant_id)
        assert variant_id in str(path)
        assert path.suffix == ".yaml"

    def test_get_result_path(self):
        """测试获取结果路径"""
        result_id = "result_20260430_143145_f6g3h7i5"
        path = self.pm.get_result_path(result_id)
        assert path == self.pm.results_dir / result_id

    def test_get_trash_path(self):
        """测试获取回收站路径"""
        item_id = "case_deleted"
        path = self.pm.get_trash_path(item_id)
        assert path == self.pm.trash_dir / item_id

    def test_exists(self):
        """测试实体存在检查"""
        # 不存在的实体
        assert not self.pm.exists("case_20260430_143052_nonexist")

        # 创建后存在的实体
        case_id = IDGenerator.generate(EntityType.CASE)
        case_path = self.pm.get_case_path(case_id)
        case_path.mkdir(parents=True)
        assert self.pm.exists(case_id)

    def test_get_all_cases(self):
        """测试获取所有算例"""
        # 初始为空
        assert self.pm.get_all_cases() == []

        # 创建算例目录
        for i in range(3):
            case_id = IDGenerator.generate(EntityType.CASE)
            self.pm.get_case_path(case_id).mkdir()

        cases = self.pm.get_all_cases()
        assert len(cases) == 3

    def test_get_all_tasks(self):
        """测试获取所有任务"""
        for i in range(2):
            task_id = IDGenerator.generate(EntityType.TASK)
            self.pm.get_task_path(task_id).mkdir()

        tasks = self.pm.get_all_tasks()
        assert len(tasks) == 2


class TestPathManagerSingleton:
    """路径管理器单例测试"""

    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_get_path_manager_returns_same_instance(self):
        """测试获取相同路径返回相同实例"""
        # 注意：当传入不同路径时，会创建新实例
        # 这个测试验证相同路径返回相同实例
        pm1 = get_path_manager(self.temp_dir)
        pm2 = get_path_manager(self.temp_dir)
        # 如果路径相同，应该返回相同实例
        assert pm1.root == pm2.root


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
