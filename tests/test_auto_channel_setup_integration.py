#!/usr/bin/env python3
"""
Auto Channel Setup Skill - 集成测试

测试自动量测配置技能的基本功能。
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# 先导入builtin模块以注册技能
import cloudpss_skills.builtin
from cloudpss_skills import get_skill
from cloudpss_skills.core import ValidationResult


class TestAutoChannelSetupConfig:
    """测试配置生成和验证"""

    def test_skill_registration(self):
        """测试技能是否正确注册"""
        skill = get_skill("auto_channel_setup")
        assert skill is not None
        assert skill.name == "auto_channel_setup"
        assert "自动" in skill.description

    def test_default_config_generation(self):
        """测试默认配置生成"""
        skill = get_skill("auto_channel_setup")
        config = skill.get_default_config()

        assert config["skill"] == "auto_channel_setup"
        assert "model" in config
        assert "measurements" in config
        assert "output" in config

        # 验证电压量测默认配置
        assert config["measurements"]["voltage"]["enabled"] is True
        assert config["measurements"]["voltage"]["freq"] == 200

        # 验证电流量测默认配置
        assert config["measurements"]["current"]["enabled"] is False

    def test_config_schema_validation(self):
        """测试配置schema验证"""
        skill = get_skill("auto_channel_setup")
        schema = skill.config_schema

        assert schema["type"] == "object"
        assert "model" in schema["properties"]
        assert "measurements" in schema["properties"]
        assert "output" in schema["properties"]

    def test_empty_rid_validation(self):
        """测试空RID验证失败"""
        skill = get_skill("auto_channel_setup")
        config = skill.get_default_config()
        config["model"]["rid"] = ""

        result = skill.validate(config)
        assert not result.valid
        assert any("rid" in error.lower() for error in result.errors)

    def test_no_measurement_enabled_validation(self):
        """测试未启用任何量测时的验证"""
        skill = get_skill("auto_channel_setup")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/test/test"

        # 禁用所有量测
        for mtype in config["measurements"]:
            config["measurements"][mtype]["enabled"] = False

        result = skill.validate(config)
        assert not result.valid
        assert any("量测" in error or "measurement" in error.lower() for error in result.errors)

    def test_valid_config_validation(self):
        """测试有效配置验证通过"""
        skill = get_skill("auto_channel_setup")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"

        result = skill.validate(config)
        assert result.valid, f"验证失败: {result.errors}"


class TestAutoChannelSetupFeatures:
    """测试技能功能特性"""

    def test_voltage_levels_filter(self):
        """测试电压等级筛选配置"""
        skill = get_skill("auto_channel_setup")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["measurements"]["voltage"]["voltage_levels"] = [220, 500]

        result = skill.validate(config)
        assert result.valid

    def test_bus_names_filter(self):
        """测试母线名称筛选配置"""
        skill = get_skill("auto_channel_setup")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["measurements"]["voltage"]["bus_names"] = ["Bus30", "Bus38"]

        result = skill.validate(config)
        assert result.valid

    def test_dry_run_mode(self):
        """测试试运行模式配置"""
        skill = get_skill("auto_channel_setup")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["output"]["dry_run"] = True

        result = skill.validate(config)
        assert result.valid

    def test_save_model_config(self):
        """测试保存模型配置"""
        skill = get_skill("auto_channel_setup")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["output"]["save_model"] = True

        result = skill.validate(config)
        assert result.valid


@pytest.mark.integration
class TestAutoChannelSetupIntegration:
    """集成测试 - 需要CloudPSS API访问"""

    def test_skill_loads_correctly(self):
        """测试技能正确加载"""
        skill = get_skill("auto_channel_setup")
        assert skill is not None
        assert skill.name == "auto_channel_setup"
        assert "自动" in skill.description

    def test_model_fetch_and_analyze(self, live_auth, integration_model):
        """测试模型获取和分析（使用conftest fixtures）"""
        model = integration_model
        assert model is not None
        assert model.name is not None

        # 获取母线元件
        buses = model.getComponentsByRid("model/CloudPSS/_newBus_3p")
        assert len(buses) > 0, "模型应该包含母线"

        # 获取线路元件
        lines = model.getComponentsByRid("model/CloudPSS/TransmissionLine")
        assert len(lines) > 0, "模型应该包含线路"


if __name__ == "__main__":
    # 运行基本测试
    print("=" * 70)
    print("Auto Channel Setup Skill - 配置测试")
    print("=" * 70)

    skill = get_skill("auto_channel_setup")
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

    # 测试电压量测配置
    config["measurements"]["voltage"]["enabled"] = True
    config["measurements"]["voltage"]["voltage_levels"] = [220, 500]
    config["measurements"]["current"]["enabled"] = True
    config["measurements"]["power"]["enabled"] = True

    result = skill.validate(config)
    if result.valid:
        print("✓ 完整配置验证通过")
    else:
        print(f"✗ 配置验证失败: {result.errors}")

    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)
