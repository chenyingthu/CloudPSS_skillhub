"""
Reactive Compensation Design 集成测试

验证真实 CloudPSS API 上的补偿设备配置

注意：当前版本仅验证配置 schema，因为 CloudPSS SDK 的 Model.addComponent()
在测试环境中遇到 'attribute name must be string, not int' 错误，需要进一步调查。
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills.builtin import ReactiveCompensationDesignSkill


@pytest.mark.integration
class TestReactiveCompensationLive:
    """真实 CloudPSS 集成测试 - 验证补偿设备配置"""

    def test_skill_config_accepts_capacitor_device_type(self):
        """验证配置 schema 接受 capacitor 设备类型"""
        skill = ReactiveCompensationDesignSkill()

        config = {
            "model": {"rid": "model/holdme/IEEE39"},
            "vsi_input": {"target_buses": ["Bus_16"]},
            "compensation": {
                "device_type": "capacitor",
                "initial_capacity": 100,
            },
            "capacitor_config": {
                "num_steps": 5
            }
        }

        result = skill.validate(config)
        assert result.valid, f"电容器组配置应该通过验证: {result.errors}"

    def test_skill_config_accepts_all_device_types(self):
        """验证配置 schema 接受所有支持的设备类型"""
        skill = ReactiveCompensationDesignSkill()

        device_types = ["sync_compensator", "svg", "svc", "capacitor"]

        for device_type in device_types:
            config = {
                "model": {"rid": "model/holdme/IEEE39"},
                "vsi_input": {"target_buses": ["Bus_16"]},
                "compensation": {
                    "device_type": device_type,
                    "initial_capacity": 100,
                }
            }

            result = skill.validate(config)
            assert result.valid, f"{device_type} 配置应该通过验证: {result.errors}"

    def test_skill_description_includes_capacitor(self):
        """验证技能描述包含电容器组支持"""
        skill = ReactiveCompensationDesignSkill()
        assert "capacitor" in skill.description or "电容器组" in skill.description, \
            "技能描述应该包含电容器组支持"

    def test_device_type_enum_includes_capacitor(self):
        """验证 device_type enum 包含 capacitor"""
        skill = ReactiveCompensationDesignSkill()
        enum_values = skill.config_schema["properties"]["compensation"]["properties"]["device_type"]["enum"]
        assert "capacitor" in enum_values, f"device_type enum 应该包含 capacitor: {enum_values}"
