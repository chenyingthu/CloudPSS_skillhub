"""
配置管理器测试
"""

import pytest
import tempfile
import shutil
from pathlib import Path

from cloudpss_skills_v3.master_organizer.core import (
    ConfigManager, get_config_manager,
    UserConfig, UserPreferences, StorageQuotas
)


class TestConfigManagerAdvanced:
    """配置管理器高级测试"""

    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.cm = ConfigManager(self.temp_dir)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_load_nonexistent_config(self):
        """测试加载不存在的配置"""
        result = self.cm.load("nonexistent")
        assert result is None

    def test_save_and_reload(self):
        """测试保存和重新加载"""
        data = {"test": "data", "nested": {"key": "value"}}
        self.cm.save("test", data)

        # 创建新实例重新加载
        cm2 = ConfigManager(self.temp_dir)
        loaded = cm2.load("test")
        assert loaded == data

    def test_delete_config(self):
        """测试删除配置"""
        self.cm.save("to_delete", {"data": "value"})
        assert self.cm.exists("to_delete")

        assert self.cm.delete("to_delete")
        assert not self.cm.exists("to_delete")
        assert not self.cm.delete("to_delete")  # 再次删除返回 False

    def test_list_configs(self):
        """测试列出配置"""
        self.cm.save("config1", {})
        self.cm.save("config2", {})
        self.cm.save("config3", {})

        configs = self.cm.list_configs()
        assert len(configs) == 3
        assert "config1" in configs
        assert "config2" in configs
        assert "config3" in configs

    def test_update_replace_mode(self):
        """测试替换模式更新"""
        self.cm.save("test", {"key1": "value1", "key2": "value2"})
        self.cm.update("test", {"key3": "value3"}, merge=False)

        loaded = self.cm.load("test")
        assert loaded == {"key3": "value3"}
        assert "key1" not in loaded

    def test_cache_invalidation(self):
        """测试缓存失效"""
        self.cm.save("cached", {"data": "original"})
        # 加载到缓存
        self.cm.load("cached")

        # 直接修改文件
        config_path = self.cm._get_config_path("cached")
        import yaml
        with open(config_path, 'w') as f:
            yaml.dump({"data": "modified"}, f)

        # 仍从缓存读取旧值
        cached = self.cm.load("cached")
        assert cached["data"] == "original"

        # 失效缓存后读取新值
        self.cm.invalidate_cache("cached")
        fresh = self.cm.load("cached")
        assert fresh["data"] == "modified"

    def test_user_config_save_load(self):
        """测试用户配置保存和加载"""
        config = UserConfig()
        config.user = {"name": "测试用户", "email": "test@example.com"}
        config.preferences.theme = "dark"
        config.quotas.max_storage_gb = 100

        self.cm.save_user_config(config)

        loaded = self.cm.get_user_config()
        assert loaded.user["name"] == "测试用户"
        assert loaded.preferences.theme == "dark"
        assert loaded.quotas.max_storage_gb == 100


class TestUserConfigDefaults:
    """用户配置默认值测试"""

    def test_default_values(self):
        """测试默认值"""
        config = UserConfig()

        # 检查默认值
        assert config.api_version == "v1.0"
        assert config.preferences.default_format == "json"
        assert config.preferences.auto_export is True
        assert config.preferences.keep_history is True
        assert config.preferences.history_limit == 100
        assert config.preferences.language == "zh_CN"
        assert config.quotas.max_storage_gb == 50
        assert config.quotas.max_cases == 1000

    def test_preferences_modification(self):
        """测试偏好修改"""
        prefs = UserPreferences()
        prefs.theme = "light"
        prefs.language = "en"

        assert prefs.theme == "light"
        assert prefs.language == "en"


class TestStorageQuotas:
    """存储配额测试"""

    def test_default_quotas(self):
        """测试默认配额"""
        quotas = StorageQuotas()
        assert quotas.max_storage_gb == 50
        assert quotas.max_cases == 1000
        assert quotas.max_tasks_per_case == 100
        assert quotas.max_results_per_task == 10
        assert quotas.trash_retention_days == 30


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
