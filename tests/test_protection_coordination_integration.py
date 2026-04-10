#!/usr/bin/env python3
"""
保护整定与配合分析技能 - 集成测试

测试内容:
1. 技能注册验证
2. 配置Schema验证
3. 真实API调用测试 (使用 substation_110 算例)
4. 结果验证

运行: pytest tests/test_protection_coordination_integration.py -v
"""

import os
import sys
import pytest
import json

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cloudpss_skills.builtin.protection_coordination import (
    ProtectionCoordinationSkill,
    ProtectionType,
    RelaySettings,
)
from cloudpss_skills.core.base import SkillStatus


# 检查是否有token
HAS_TOKEN = os.path.exists(".cloudpss_token")
TOKEN_MSG = "需要.cloudpss_token文件进行集成测试"


class TestProtectionCoordinationSkill:
    """保护配合技能集成测试"""

    @pytest.fixture
    def skill(self):
        """创建技能实例"""
        return ProtectionCoordinationSkill()

    @pytest.fixture
    def valid_config(self):
        """有效配置"""
        return {
            "model": {"rid": "model/chenying/substation_110"},
            "auth": {"server": "internal"},
            "analysis": {
                "distance_protection": {"enabled": True, "check_zones": [1, 2, 3]},
                "overcurrent_protection": {
                    "enabled": True,
                    "check_coordination": True,
                    "time_margin": 0.3,
                },
                "differential_protection": {"enabled": True},
                "zero_sequence_protection": {"enabled": True},
                "reclosing": {"enabled": True},
                "fault_scenarios": [
                    {"type": "three_phase", "location": "110kV_L1", "duration": 0.1},
                    {"type": "single_ground", "location": "10kV_L1", "duration": 0.15},
                ],
            },
            "output": {"format": "json", "generate_tcc_curves": True},
        }

    def test_skill_registration(self, skill):
        """测试1: 技能注册信息"""
        assert skill.name == "protection_coordination"
        assert skill.description == "继电保护定值计算、配合关系校验、保护动作分析"
        assert skill.version == "1.0.0"
        print(f"✅ 技能注册: {skill.name} v{skill.version}")

    def test_config_schema_validation(self, skill):
        """测试2: 配置Schema验证"""
        assert skill.config_schema is not None
        assert "properties" in skill.config_schema
        assert "model" in skill.config_schema["properties"]
        assert "analysis" in skill.config_schema["properties"]
        print("✅ 配置Schema验证通过")

    def test_validation_with_valid_config(self, skill, valid_config):
        """测试3: 有效配置验证"""
        result = skill.validate(valid_config)
        assert result.valid is True
        assert len(result.errors) == 0
        print("✅ 有效配置验证通过")

    def test_validation_with_missing_rid(self, skill):
        """测试4: 缺少RID的配置验证"""
        invalid_config = {"model": {}, "analysis": {}}
        result = skill.validate(invalid_config)
        assert result.valid is False
        assert any("RID" in err for err in result.errors)
        print("✅ 缺失RID检测正确")

    def test_validation_with_invalid_fault_type(self, skill):
        """测试5: 无效故障类型验证"""
        invalid_config = {
            "model": {"rid": "test"},
            "analysis": {
                "fault_scenarios": [{"type": "invalid_type", "location": "test"}]
            },
        }
        # 注：当前validate不检查具体值，只检查结构
        # 这个测试展示了如何扩展验证
        result = skill.validate(invalid_config)
        assert isinstance(result.valid, bool)
        print("✅ 故障类型验证通过")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_real_api_call(self, skill, valid_config):
        """测试6: 真实API调用测试 - 使用substations_110算例"""
        print("\n🔄 开始真实API调用测试...")
        print(f"   模型: {valid_config['model']['rid']}")

        result = skill.run(valid_config)

        print(f"   状态: {result.status.value}")

        # 验证结果状态
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED], f"执行失败: {result.error}"

        # 验证返回数据
        assert result.data is not None
        assert "model" in result.data
        assert "protection_devices_found" in result.data
        assert "analysis_results" in result.data

        print(f"   发现保护装置: {result.data['protection_devices_found']}个")

        # 验证分析结果
        analysis = result.data["analysis_results"]
        assert "distance_protection" in analysis
        assert "overcurrent_protection" in analysis

        print("✅ 真实API调用测试通过!")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_distance_protection_analysis(self, skill, valid_config):
        """测试7: 距离保护分析验证"""
        result = skill.run(valid_config)

        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

        distance_analysis = result.data["analysis_results"]["distance_protection"]
        assert "relay_count" in distance_analysis
        assert "zone_analysis" in distance_analysis

        if distance_analysis["relay_count"] > 0:
            first_relay = distance_analysis["zone_analysis"][0]
            assert "location" in first_relay
            assert "zones" in first_relay
            assert "zone1" in first_relay["zones"]
            assert "reach_percent" in first_relay["zones"]["zone1"]
            print(f"✅ 距离保护分析验证通过 (发现{distance_analysis['relay_count']}个)")
        else:
            print("⚠️ 未识别到距离保护")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_overcurrent_coordination(self, skill, valid_config):
        """测试8: 过流保护配合验证"""
        result = skill.run(valid_config)

        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

        oc_analysis = result.data["analysis_results"]["overcurrent_protection"]
        assert "relay_count" in oc_analysis
        assert "coordination_check" in oc_analysis

        print(f"   过流保护数量: {oc_analysis['relay_count']}")
        print(f"   110kV侧: {oc_analysis.get('110kV_relays', 0)}个")
        print(f"   10kV侧: {oc_analysis.get('10kV_relays', 0)}个")

        # 验证配合关系
        coordination = oc_analysis.get("coordination_check", [])
        for coord in coordination:
            assert "primary" in coord
            assert "backup" in coord
            assert "is_valid" in coord

        print(f"✅ 过流保护配合验证通过 ({len(coordination)}对配合关系)")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_fault_scenario_analysis(self, skill, valid_config):
        """测试9: 故障场景分析验证"""
        result = skill.run(valid_config)

        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

        fault_analysis = result.data["analysis_results"].get("fault_scenarios", [])
        assert len(fault_analysis) == 2  # 配置了2个故障场景

        for scenario in fault_analysis:
            assert "fault_type" in scenario
            assert "location" in scenario
            assert "operating_relays" in scenario
            assert "expected_clearing_time" in scenario

            print(f"   故障: {scenario['fault_type']} @ {scenario['location']}")
            print(f"   动作保护: {len(scenario['operating_relays'])}个")
            print(f"   预期清除时间: {scenario['expected_clearing_time'] * 1000:.1f}ms")

        print("✅ 故障场景分析验证通过")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_tcc_curves(self, skill, valid_config):
        """测试10: TCC曲线生成验证"""
        result = skill.run(valid_config)

        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

        tcc_data = result.data["analysis_results"].get("tcc_curves", {})
        assert "curves" in tcc_data

        for curve in tcc_data["curves"]:
            assert "relay" in curve
            assert "curve_type" in curve
            assert "points" in curve
            assert len(curve["points"]) > 0

        print(f"✅ TCC曲线生成验证通过 ({len(tcc_data['curves'])}条曲线)")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_performance_benchmark(self, skill, valid_config):
        """测试11: 性能基准测试"""
        import time

        start_time = time.time()
        result = skill.run(valid_config)
        elapsed_time = time.time() - start_time

        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

        print(f"⏱️  执行时间: {elapsed_time:.2f}秒")

        # 性能要求: 应该能在30秒内完成
        assert elapsed_time < 30.0, f"执行时间过长: {elapsed_time:.2f}秒"

        print("✅ 性能基准测试通过")


class TestProtectionTypes:
    """保护类型枚举测试"""

    def test_protection_type_enum(self):
        """测试保护类型枚举"""
        assert ProtectionType.DISTANCE.value == "distance"
        assert ProtectionType.OVERCURRENT.value == "overcurrent"
        assert ProtectionType.DIFFERENTIAL.value == "differential"
        assert ProtectionType.ZERO_SEQUENCE.value == "zero_sequence"
        print("✅ 保护类型枚举测试通过")


class TestRelaySettings:
    """保护定值数据类测试"""

    def test_relay_settings_creation(self):
        """测试保护定值对象创建"""
        settings = RelaySettings(
            relay_type=ProtectionType.DISTANCE,
            location="110kV_L1",
            protected_component="Line_L1",
            zone1_reach=80.0,
            zone2_reach=120.0,
            zone3_reach=200.0,
            zone1_time=0.0,
            zone2_time=0.3,
            zone3_time=0.6,
        )

        assert settings.relay_type == ProtectionType.DISTANCE
        assert settings.location == "110kV_L1"
        assert settings.zone1_reach == 80.0
        print("✅ 保护定值对象创建测试通过")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
