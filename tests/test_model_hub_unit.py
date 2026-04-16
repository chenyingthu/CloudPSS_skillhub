#!/usr/bin/env python3
"""
Model Hub Skill - Unit Tests

Tests for model_hub skill.
"""

import pytest
import sys
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills.builtin.model_hub import (
    ModelHubSkill,
    HubConfig,
    ModelRegistry,
)


class TestHubConfig:
    """Tests for HubConfig class"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.hub_dir = Path(self.temp_dir)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir)

    def test_init_default(self):
        config = HubConfig(self.hub_dir)
        config.init_default()
        assert config.config_file.exists()
        assert "servers" in config._config
        assert "current_server" in config._config

    def test_add_server(self):
        config = HubConfig(self.hub_dir)
        config.init_default()
        config.add_server("test", "https://test.com", "token123", None, 1)

        servers = config.list_servers()
        assert len(servers) == 1
        assert servers[0]["name"] == "test"
        assert servers[0]["url"] == "https://test.com"

    def test_remove_server(self):
        config = HubConfig(self.hub_dir)
        config.init_default()
        config.add_server("test", "https://test.com", "token123", None, 1)
        config.remove_server("test")

        servers = config.list_servers()
        assert len(servers) == 0

    def test_use_server(self):
        config = HubConfig(self.hub_dir)
        config.init_default()
        config.add_server("server1", "https://s1.com", "token1", None, 1)
        config.add_server("server2", "https://s2.com", "token2", None, 2)
        config.use_server("server2")

        assert config.get_current_server_name() == "server2"

    def test_get_current_server(self):
        config = HubConfig(self.hub_dir)
        config.init_default()
        config.add_server("test", "https://test.com", "token123", None, 1)

        current = config.get_current_server()
        assert current is not None
        assert current["name"] == "test"


class TestModelRegistry:
    """Tests for ModelRegistry class"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.hub_dir = Path(self.temp_dir)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir)

    def test_list_models_empty(self):
        registry = ModelRegistry(self.hub_dir)
        models = registry.list_models()
        assert models == []

    def test_register_model(self):
        registry = ModelRegistry(self.hub_dir)
        registry.register_model("IEEE39", "model/holdme/IEEE39", "public", {})

        models = registry.list_models()
        assert len(models) == 1
        assert models[0]["name"] == "IEEE39"
        assert registry.get_rid("IEEE39", "public") == "model/holdme/IEEE39"

    def test_unregister_model(self):
        registry = ModelRegistry(self.hub_dir)
        registry.register_model("IEEE39", "model/holdme/IEEE39", "public", {})
        registry.unregister_model("IEEE39")

        models = registry.list_models()
        assert len(models) == 0

    def test_update_rid(self):
        registry = ModelRegistry(self.hub_dir)
        registry.register_model("IEEE39", "model/holdme/IEEE39", "public", {})
        registry.update_rid("IEEE39", "internal", "model/chenying/IEEE39")

        assert registry.get_rid("IEEE39", "public") == "model/holdme/IEEE39"
        assert registry.get_rid("IEEE39", "internal") == "model/chenying/IEEE39"

    def test_get_local_path(self):
        registry = ModelRegistry(self.hub_dir)
        path = registry.get_local_path("IEEE39")
        assert path.name == "IEEE39"


class TestModelHubSkill:
    """Tests for ModelHubSkill class"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.skill = ModelHubSkill()

    def teardown_method(self):
        shutil.rmtree(self.temp_dir)

    def test_skill_properties(self):
        assert self.skill.name == "model_hub"
        assert self.skill.version == "1.0.0"
        assert "算例" in self.skill.description

    def test_config_schema(self):
        schema = self.skill.config_schema
        assert schema["type"] == "object"
        assert "action" in schema["properties"]

    def test_validate_valid_action(self):
        config = {"skill": "model_hub", "action": "status"}
        result = self.skill.validate(config)
        assert result.valid

    def test_validate_missing_action(self):
        config = {"skill": "model_hub"}
        result = self.skill.validate(config)
        assert result.valid

    def test_validate_add_server_without_name(self):
        config = {
            "skill": "model_hub",
            "action": "add_server",
            "server": {"url": "https://test.com"},
        }
        result = self.skill.validate(config)
        assert not result.valid
        assert any("name" in e.lower() for e in result.errors)

    def test_validate_add_server_without_url(self):
        config = {
            "skill": "model_hub",
            "action": "add_server",
            "server": {"name": "test"},
        }
        result = self.skill.validate(config)
        assert not result.valid
        assert any("url" in e.lower() for e in result.errors)

    def test_validate_pull_without_name_or_rid(self):
        config = {"skill": "model_hub", "action": "pull", "model": {}}
        result = self.skill.validate(config)
        assert not result.valid

    def test_validate_register_with_name(self):
        config = {
            "skill": "model_hub",
            "action": "register",
            "model": {"name": "IEEE39"},
        }
        result = self.skill.validate(config)
        assert result.valid

    def test_validate_register_with_rid(self):
        config = {
            "skill": "model_hub",
            "action": "register",
            "model": {"rid": "model/holdme/IEEE39"},
        }
        result = self.skill.validate(config)
        assert result.valid

    def test_run_init_action(self):
        config = {
            "skill": "model_hub",
            "action": "init",
            "hub_dir": self.temp_dir,
        }
        result = self.skill.run(config)
        assert result.success
        assert result.data["status"] == "initialized"

    def test_run_status_action(self):
        config = {
            "skill": "model_hub",
            "action": "status",
            "hub_dir": self.temp_dir,
        }
        result = self.skill.run(config)
        assert result.success
        assert "hub_dir" in result.data

    def test_run_add_server_action(self):
        config = {
            "skill": "model_hub",
            "action": "add_server",
            "hub_dir": self.temp_dir,
            "server": {
                "name": "test",
                "url": "https://test.com",
                "token": "test_token",
            },
        }
        result = self.skill.run(config)
        assert result.success
        assert result.data["status"] == "added"

    def test_run_list_servers_action(self):
        config = {
            "skill": "model_hub",
            "action": "list_servers",
            "hub_dir": self.temp_dir,
        }
        result = self.skill.run(config)
        assert result.success
        assert "servers" in result.data

    def test_run_remove_server_action(self):
        config_add = {
            "skill": "model_hub",
            "action": "add_server",
            "hub_dir": self.temp_dir,
            "server": {
                "name": "test",
                "url": "https://test.com",
                "token": "test_token",
            },
        }
        self.skill.run(config_add)

        config_remove = {
            "skill": "model_hub",
            "action": "remove_server",
            "hub_dir": self.temp_dir,
            "server": {"name": "test"},
        }
        result = self.skill.run(config_remove)
        assert result.success
        assert result.data["status"] == "removed"

    def test_run_use_server_action(self):
        config_add = {
            "skill": "model_hub",
            "action": "add_server",
            "hub_dir": self.temp_dir,
            "server": {"name": "test", "url": "https://test.com", "token": "test"},
        }
        self.skill.run(config_add)

        config_use = {
            "skill": "model_hub",
            "action": "use_server",
            "hub_dir": self.temp_dir,
            "server": {"name": "test"},
        }
        result = self.skill.run(config_use)
        assert result.success
        assert result.data["status"] == "switched"

    def test_run_register_model_action(self):
        config = {
            "skill": "model_hub",
            "action": "register",
            "hub_dir": self.temp_dir,
            "model": {
                "name": "IEEE39",
                "rid": "model/holdme/IEEE39",
                "source_server": "public",
                "description": "IEEE 39节点测试系统",
                "tags": ["ieee", "test"],
            },
        }
        result = self.skill.run(config)
        assert result.success
        assert result.data["status"] == "registered"

    def test_run_list_models_action(self):
        config_register = {
            "skill": "model_hub",
            "action": "register",
            "hub_dir": self.temp_dir,
            "model": {"name": "IEEE39", "rid": "model/holdme/IEEE39"},
        }
        self.skill.run(config_register)

        config_list = {
            "skill": "model_hub",
            "action": "list_models",
            "hub_dir": self.temp_dir,
        }
        result = self.skill.run(config_list)
        assert result.success
        assert result.data["count"] == 1
        assert result.data["models"][0]["name"] == "IEEE39"

    def test_run_unregister_model_action(self):
        config_register = {
            "skill": "model_hub",
            "action": "register",
            "hub_dir": self.temp_dir,
            "model": {"name": "IEEE39", "rid": "model/holdme/IEEE39"},
        }
        self.skill.run(config_register)

        config_unregister = {
            "skill": "model_hub",
            "action": "unregister",
            "hub_dir": self.temp_dir,
            "model": {"name": "IEEE39"},
        }
        result = self.skill.run(config_unregister)
        assert result.success
        assert result.data["status"] == "unregistered"

    def test_run_info_action(self):
        config_register = {
            "skill": "model_hub",
            "action": "register",
            "hub_dir": self.temp_dir,
            "model": {"name": "IEEE39", "rid": "model/holdme/IEEE39"},
        }
        self.skill.run(config_register)

        config_info = {
            "skill": "model_hub",
            "action": "info",
            "hub_dir": self.temp_dir,
            "model": {"name": "IEEE39"},
        }
        result = self.skill.run(config_info)
        assert result.success
        assert (
            result.data.get("name") == "IEEE39"
            or result.data.get("rids", {}).get("default") == "model/holdme/IEEE39"
        )

    def test_run_list_local_action(self):
        config_list = {
            "skill": "model_hub",
            "action": "list_local",
            "hub_dir": self.temp_dir,
        }
        result = self.skill.run(config_list)
        assert result.success
        assert "local_models" in result.data

    def test_run_unknown_action(self):
        config = {
            "skill": "model_hub",
            "action": "unknown_action",
            "hub_dir": self.temp_dir,
        }
        result = self.skill.run(config)
        assert result.status.value == "failed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
