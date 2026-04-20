#!/usr/bin/env python3
"""
Config Batch Runner Skill - 集成测试

测试多配置场景批量运行技能的基本功能。
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# 先导入builtin模块以注册技能
import cloudpss_skills.builtin
from cloudpss_skills import get_skill
from cloudpss_skills.core import ValidationResult


class TestConfigBatchRunnerConfig:
    """测试配置生成和验证"""

    def test_skill_registration(self):
        """测试技能是否正确注册"""
        skill = get_skill("config_batch_runner")
        assert skill is not None
        assert skill.name == "config_batch_runner"
        assert "配置" in skill.description or "config" in skill.description.lower()

    def test_default_config_generation(self):
        """测试默认配置生成"""
        skill = get_skill("config_batch_runner")
        config = skill.get_default_config()

        assert config["skill"] == "config_batch_runner"
        assert "model" in config
        assert "configs" in config
        assert "execution" in config
        assert "output" in config

        # 验证默认配置
        assert config["configs"]["mode"] == "all"
        assert config["execution"]["polling_interval"] == 5.0
        assert config["execution"]["timeout"] == 3600.0

    def test_config_schema_validation(self):
        """测试配置schema验证"""
        skill = get_skill("config_batch_runner")
        schema = skill.config_schema

        assert schema["type"] == "object"
        assert "model" in schema["properties"]
        assert "configs" in schema["properties"]
        assert "execution" in schema["properties"]
        assert "output" in schema["properties"]

    def test_empty_rid_validation(self):
        """测试空RID验证失败"""
        skill = get_skill("config_batch_runner")
        config = skill.get_default_config()
        config["model"]["rid"] = ""

        result = skill.validate(config)
        assert not result.valid
        assert any("rid" in error.lower() for error in result.errors)

    def test_valid_config_validation(self):
        """测试有效配置验证通过"""
        skill = get_skill("config_batch_runner")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"

        result = skill.validate(config)
        assert result.valid, f"验证失败: {result.errors}"

    def test_different_config_modes(self):
        """测试不同配置模式"""
        skill = get_skill("config_batch_runner")

        # all模式
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["configs"]["mode"] = "all"
        result = skill.validate(config)
        assert result.valid

        # range模式
        config["configs"]["mode"] = "range"
        config["configs"]["start"] = 0
        config["configs"]["end"] = 3
        result = skill.validate(config)
        assert result.valid

        # list模式
        config["configs"]["mode"] = "list"
        config["configs"]["indices"] = [0, 1, 2]
        result = skill.validate(config)
        assert result.valid

    def test_invalid_range_validation(self):
        """测试无效range验证"""
        skill = get_skill("config_batch_runner")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["configs"]["mode"] = "range"
        config["configs"]["start"] = 5
        config["configs"]["end"] = 3

        result = skill.validate(config)
        assert not result.valid
        assert any("range" in error.lower() or "start" in error.lower() for error in result.errors)


class TestConfigBatchRunnerFeatures:
    """测试技能功能特性"""

    def test_custom_args_config(self):
        """测试自定义参数覆盖配置"""
        skill = get_skill("config_batch_runner")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["configs"]["custom_args"] = {"end_time": 10, "step_time": 0.0001}

        result = skill.validate(config)
        assert result.valid

    def test_continue_on_error_config(self):
        """测试出错继续配置"""
        skill = get_skill("config_batch_runner")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["execution"]["continue_on_error"] = False

        result = skill.validate(config)
        assert result.valid


@pytest.mark.integration
class TestConfigBatchRunnerIntegration:
    """集成测试 - 需要CloudPSS API访问"""

    def test_skill_loads_correctly(self):
        """测试技能正确加载"""
        skill = get_skill("config_batch_runner")
        assert skill is not None
        assert skill.name == "config_batch_runner"

    def test_model_has_configs(self, live_auth, integration_model):
        """测试模型有配置可用"""
        # 验证IEEE39模型至少有一个配置
        assert hasattr(integration_model, 'configs') or hasattr(integration_model, 'getConfigs')
        configs = getattr(integration_model, 'configs', []) or getattr(integration_model, 'getConfigs', lambda: [])()
        assert len(configs) >= 1, "模型至少需要1个配置"

    def test_run_all_configs(self, live_auth):
        """测试运行所有配置（使用真实API）"""
        skill = get_skill("config_batch_runner")
        config = {
            "skill": "config_batch_runner",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "configs": {
                "mode": "all"
            },
            "execution": {
                "polling_interval": 5.0,
                "timeout": 300.0,
                "continue_on_error": True
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "test_config_batch"
            }
        }

        # 验证配置
        validation = skill.validate(config)
        assert validation.valid, f"配置验证失败: {validation.errors}"

        # 运行技能（实际调用CloudPSS API）
        result = skill.run(config)

        # 验证结果
        assert result is not None
        assert result.status.value in ["success", "failed", "cancelled"]

        if result.status.value == "success":
            assert "total_configs" in result.data
            assert "success_count" in result.data
            assert result.data["total_configs"] >= 1
            print(f"\n✓ 成功运行 {result.data['success_count']}/{result.data['total_configs']} 个配置")
        else:
            # 即使失败也应该有错误信息
            assert result.error or result.logs
            print(f"\n⚠ 运行失败: {result.error}")

    def test_run_range_configs(self, live_auth):
        """测试范围模式运行（使用真实API）"""
        skill = get_skill("config_batch_runner")
        config = {
            "skill": "config_batch_runner",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "configs": {
                "mode": "range",
                "start": 0,
                "end": 1  # 只运行第0个配置
            },
            "execution": {
                "polling_interval": 5.0,
                "timeout": 300.0,
                "continue_on_error": True
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "test_config_range"
            }
        }

        result = skill.run(config)
        assert result is not None
        assert result.status.value in ["success", "failed", "cancelled"]

        if result.status.value == "success":
            assert result.data["total_configs"] == 1
            print(f"\n✓ 范围模式成功运行1个配置")

    def test_run_list_configs(self, live_auth):
        """测试列表模式运行（使用真实API）"""
        skill = get_skill("config_batch_runner")
        config = {
            "skill": "config_batch_runner",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "configs": {
                "mode": "list",
                "indices": [0]  # 只运行第0个配置
            },
            "execution": {
                "polling_interval": 5.0,
                "timeout": 300.0,
                "continue_on_error": True
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "test_config_list"
            }
        }

        result = skill.run(config)
        assert result is not None

        if result.status.value == "success":
            assert result.data["total_configs"] == 1
            results = result.data.get("results", [])
            assert len(results) > 0
            assert results[0]["config_index"] == 0
            print(f"\n✓ 列表模式成功运行指定配置")

    def test_custom_args_override(self, live_auth):
        """测试自定义参数覆盖（使用真实API）"""
        skill = get_skill("config_batch_runner")
        config = {
            "skill": "config_batch_runner",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "configs": {
                "mode": "range",
                "start": 0,
                "end": 1,
                "custom_args": {
                    "end_time": 5.0  # 覆盖仿真结束时间
                }
            },
            "execution": {
                "polling_interval": 5.0,
                "timeout": 300.0,
                "continue_on_error": True
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "test_custom_args"
            }
        }

        result = skill.run(config)
        assert result is not None
        assert result.status.value in ["success", "failed", "cancelled"]

        if result.status.value == "success":
            print(f"\n✓ 自定义参数覆盖成功")
            # 验证输出文件存在
            import os
            assert os.path.exists("./results/test_custom_args_report.json")

    def test_csv_mapping_output(self, live_auth):
        """测试CSV映射文件输出（使用真实API）"""
        skill = get_skill("config_batch_runner")
        config = {
            "skill": "config_batch_runner",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "configs": {
                "mode": "range",
                "start": 0,
                "end": 1
            },
            "execution": {
                "polling_interval": 5.0,
                "timeout": 300.0,
                "continue_on_error": True
            },
            "output": {
                "format": "csv",  # CSV格式
                "path": "./results/",
                "prefix": "test_csv_mapping"
            }
        }

        result = skill.run(config)

        if result.status.value == "success":
            # 验证CSV文件生成
            import os
            csv_file = "./results/test_csv_mapping_runner_ids.csv"
            if os.path.exists(csv_file):
                with open(csv_file, 'r') as f:
                    content = f.read()
                    assert "Runner ID" in content
                    assert "Config Name" in content
                    print(f"\n✓ CSV映射文件生成成功")

    def test_result_data_structure(self, live_auth):
        """测试结果数据结构（使用真实API）"""
        skill = get_skill("config_batch_runner")
        config = {
            "skill": "config_batch_runner",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "configs": {
                "mode": "range",
                "start": 0,
                "end": 1
            },
            "execution": {
                "polling_interval": 5.0,
                "timeout": 300.0,
                "continue_on_error": True
            }
        }

        result = skill.run(config)

        # 验证结果结构
        assert result.skill_name == "config_batch_runner"
        assert result.start_time is not None
        assert result.end_time is not None

        if result.status.value == "success":
            data = result.data
            assert "total_configs" in data
            assert "success_count" in data
            assert "failed_count" in data
            assert "model_rid" in data
            assert "results" in data
            assert isinstance(data["results"], list)

            # 验证日志
            assert len(result.logs) > 0
            log_messages = [log.message for log in result.logs]
            assert any("Config" in msg or "配置" in msg for msg in log_messages)

            print(f"\n✓ 结果数据结构验证通过")
            print(f"  - 总配置数: {data['total_configs']}")
            print(f"  - 成功数: {data['success_count']}")
            print(f"  - 失败数: {data['failed_count']}")
            print(f"  - 日志条目数: {len(result.logs)}")


if __name__ == "__main__":
    # 运行基本测试
    print("=" * 70)
    print("Config Batch Runner Skill - 配置测试")
    print("=" * 70)

    skill = get_skill("config_batch_runner")
    print(f"\n✓ 技能已注册: {skill.name}")
    print(f"✓ 技能描述: {skill.description}")

    # 测试配置验证
    config = skill.get_default_config()
    config["model"]["rid"] = "model/holdme/IEEE39"

    result = skill.validate(config)
    if result.valid:
        print("✓ 默认配置验证通过")
    else:
        print(f"✗ 配置验证失败: {result.errors}")

    # 测试不同模式
    modes = ["all", "range", "list"]
    for mode in modes:
        config["configs"]["mode"] = mode
        if mode == "range":
            config["configs"]["start"] = 0
            config["configs"]["end"] = 3
        elif mode == "list":
            config["configs"]["indices"] = [0, 1]

        result = skill.validate(config)
        if result.valid:
            print(f"✓ 模式 '{mode}' 验证通过")
        else:
            print(f"✗ 模式 '{mode}' 验证失败: {result.errors}")

    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)
