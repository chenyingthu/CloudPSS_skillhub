"""
收纳大师核心模块测试
"""

import pytest
from datetime import datetime
from pathlib import Path
import tempfile
import shutil

from cloudpss_skills_v3.master_organizer.core import (
    IDGenerator, EntityType, validate_id,
    PathManager, get_path_manager,
    ConfigManager, UserConfig,
    CryptoManager, MockCryptoManager
)


class TestIDGenerator:
    """测试 ID 生成器"""

    def test_generate_case_id(self):
        """测试生成算例ID"""
        case_id = IDGenerator.generate(EntityType.CASE)
        assert case_id.startswith("case_")
        assert len(case_id.split("_")) == 4  # case_YYYYMMDD_HHMMSS_hash8

    def test_generate_task_id(self):
        """测试生成任务ID"""
        task_id = IDGenerator.generate(EntityType.TASK)
        assert task_id.startswith("task_")
        assert len(task_id.split("_")) == 4

    def test_generate_server_id(self):
        """测试生成服务器ID"""
        server_id = IDGenerator.generate(EntityType.SERVER)
        assert server_id.startswith("server_")
        assert len(server_id.split("_")) == 2  # server_hash8

    def test_validate_valid_id(self):
        """测试验证有效ID"""
        case_id = IDGenerator.generate(EntityType.CASE)
        assert validate_id(case_id, EntityType.CASE)

    def test_validate_invalid_id(self):
        """测试验证无效ID"""
        assert not validate_id("invalid_id")
        assert not validate_id("")
        assert not validate_id(None)

    def test_parse_id(self):
        """测试解析ID"""
        case_id = IDGenerator.generate(EntityType.CASE)
        parsed = IDGenerator.parse(case_id)
        assert parsed is not None
        assert parsed["entity_type"] == EntityType.CASE
        assert "created_at" in parsed


class TestPathManager:
    """测试路径管理器"""

    def setup_method(self):
        """每个测试前创建临时目录"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.pm = PathManager(self.temp_dir)

    def teardown_method(self):
        """每个测试后清理"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_directory_structure(self):
        """测试目录结构创建"""
        assert self.pm.root == self.temp_dir
        assert self.pm.config_dir.exists()
        assert self.pm.registry_dir.exists()
        assert self.pm.cases_dir.exists()
        assert self.pm.tasks_dir.exists()
        assert self.pm.results_dir.exists()
        assert self.pm.cache_dir.exists()
        assert self.pm.logs_dir.exists()
        assert self.pm.trash_dir.exists()

    def test_get_case_path(self):
        """测试获取算例路径"""
        case_id = "case_20260430_143052_a3f7b2d9"
        case_path = self.pm.get_case_path(case_id)
        assert case_path == self.pm.cases_dir / case_id

    def test_get_task_path(self):
        """测试获取任务路径"""
        task_id = "task_20260430_143052_d5f9a4b2"
        task_path = self.pm.get_task_path(task_id)
        assert task_path == self.pm.tasks_dir / task_id

    def test_get_registry_path(self):
        """测试获取注册表路径"""
        registry_path = self.pm.get_registry_path("cases")
        assert registry_path == self.pm.registry_dir / "cases.yaml"


class TestConfigManager:
    """测试配置管理器"""

    def setup_method(self):
        """每个测试前创建临时目录"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.cm = ConfigManager(self.temp_dir)

    def teardown_method(self):
        """每个测试后清理"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_and_load_config(self):
        """测试保存和加载配置"""
        test_data = {"name": "test", "value": 123}
        self.cm.save("test_config", test_data)

        loaded = self.cm.load("test_config")
        assert loaded == test_data

    def test_user_config_defaults(self):
        """测试用户配置默认值"""
        config = self.cm.get_user_config()
        assert config.api_version == "v1.0"
        assert config.preferences.default_format == "json"
        assert config.quotas.max_storage_gb == 50

    def test_update_config(self):
        """测试更新配置"""
        self.cm.update("test", {"key1": "value1"})
        self.cm.update("test", {"key2": "value2"}, merge=True)

        loaded = self.cm.load("test")
        assert loaded["key1"] == "value1"
        assert loaded["key2"] == "value2"


class TestCryptoManager:
    """测试加密管理器"""

    def setup_method(self):
        """每个测试前创建临时目录"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.key_path = self.temp_dir / "test_key"
        self.cm = MockCryptoManager(self.key_path)

    def teardown_method(self):
        """每个测试后清理"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_encrypt_decrypt(self):
        """测试加密解密"""
        plaintext = "secret_token_123"
        ciphertext = self.cm.encrypt(plaintext)
        assert ciphertext != plaintext
        assert ciphertext.startswith("MOCK:")

        decrypted = self.cm.decrypt(ciphertext)
        assert decrypted == plaintext

    def test_encrypt_decrypt_dict(self):
        """测试字典加密解密"""
        data = {
            "username": "admin",
            "password": "secret123",
            "host": "example.com"
        }
        encrypted = self.cm.encrypt_dict(data)
        assert all(v.startswith("MOCK:") for v in encrypted.values() if isinstance(v, str))

        decrypted = self.cm.decrypt_dict(encrypted)
        assert decrypted == data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
