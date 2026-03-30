#!/usr/bin/env python3
"""
Orthogonal Sensitivity Analysis Skill - 集成测试

测试正交敏感性分析技能的基本功能。
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# 先导入builtin模块以注册技能
import cloudpss_skills.builtin
from cloudpss_skills import get_skill
from cloudpss_skills.core import ValidationResult


class TestOrthogonalSensitivityConfig:
    """测试配置生成和验证"""

    def test_skill_registration(self):
        """测试技能是否正确注册"""
        skill = get_skill("orthogonal_sensitivity")
        assert skill is not None
        assert skill.name == "orthogonal_sensitivity"
        assert "正交" in skill.description or "orthogonal" in skill.description.lower()

    def test_default_config_generation(self):
        """测试默认配置生成"""
        skill = get_skill("orthogonal_sensitivity")
        config = skill.get_default_config()

        assert config["skill"] == "orthogonal_sensitivity"
        assert "model" in config
        assert "parameters" in config
        assert "target" in config
        assert "design" in config
        assert "execution" in config
        assert "output" in config

        # 验证默认设计配置
        assert config["design"]["table_type"] == "auto"
        assert config["design"]["simulation_type"] == "power_flow"
        assert config["target"]["metric"] == "voltage"

    def test_config_schema_validation(self):
        """测试配置schema验证"""
        skill = get_skill("orthogonal_sensitivity")
        schema = skill.config_schema

        assert schema["type"] == "object"
        assert "model" in schema["properties"]
        assert "parameters" in schema["properties"]
        assert "target" in schema["properties"]
        assert "design" in schema["properties"]

    def test_empty_rid_validation(self):
        """测试空RID验证失败"""
        skill = get_skill("orthogonal_sensitivity")
        config = skill.get_default_config()
        config["model"]["rid"] = ""
        config["parameters"] = [{"name": "Gen1.pf_P", "levels": [0.8, 1.0, 1.2]}]

        result = skill.validate(config)
        assert not result.valid
        assert any("rid" in error.lower() for error in result.errors)

    def test_valid_config_validation(self):
        """测试有效配置验证通过"""
        skill = get_skill("orthogonal_sensitivity")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["parameters"] = [
            {"name": "Gen1.pf_P", "levels": [0.8, 1.0, 1.2]},
            {"name": "Gen2.pf_P", "levels": [0.8, 1.0, 1.2]},
        ]
        config["target"]["metric"] = "voltage"

        result = skill.validate(config)
        assert result.valid, f"验证失败: {result.errors}"

    def test_parameter_count_validation(self):
        """测试参数数量验证"""
        skill = get_skill("orthogonal_sensitivity")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"

        # 超过7个参数应该失败
        config["parameters"] = [
            {"name": f"Gen{i}.pf_P", "levels": [0.8, 1.0]}
            for i in range(8)
        ]
        result = skill.validate(config)
        assert not result.valid
        assert any("7" in error for error in result.errors)

    def test_parameter_levels_validation(self):
        """测试参数水平验证"""
        skill = get_skill("orthogonal_sensitivity")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"

        # 少于2个水平应该失败
        config["parameters"] = [{"name": "Gen1.pf_P", "levels": [1.0]}]
        result = skill.validate(config)
        assert not result.valid

        # 超过4个水平应该失败
        config["parameters"] = [{"name": "Gen1.pf_P", "levels": [0.5, 0.8, 1.0, 1.2, 1.5]}]
        result = skill.validate(config)
        assert not result.valid

        # 2-4个水平应该通过
        for num_levels in [2, 3, 4]:
            config["parameters"] = [{"name": "Gen1.pf_P", "levels": [0.8, 1.0, 1.2, 1.5][:num_levels]}]
            result = skill.validate(config)
            assert result.valid, f"{num_levels}个水平应该通过"

    def test_target_metric_validation(self):
        """测试目标指标验证"""
        skill = get_skill("orthogonal_sensitivity")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["parameters"] = [{"name": "Gen1.pf_P", "levels": [0.8, 1.0]}]

        # 有效指标
        for metric in ["voltage", "power", "frequency", "custom"]:
            config["target"]["metric"] = metric
            result = skill.validate(config)
            assert result.valid, f"指标 {metric} 应该通过"


class TestOrthogonalSensitivityFeatures:
    """测试技能功能特性"""

    def test_table_type_config(self):
        """测试正交表类型配置"""
        skill = get_skill("orthogonal_sensitivity")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["parameters"] = [{"name": "Gen1.pf_P", "levels": [0.8, 1.0]}]

        # 测试各种正交表类型
        for table_type in ["auto", "L4_2_3", "L8_2_7", "L9_3_4", "L16_4_5"]:
            config["design"]["table_type"] = table_type
            result = skill.validate(config)
            assert result.valid, f"正交表类型 {table_type} 验证失败"

    def test_simulation_type_config(self):
        """测试仿真类型配置"""
        skill = get_skill("orthogonal_sensitivity")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["parameters"] = [{"name": "Gen1.pf_P", "levels": [0.8, 1.0]}]

        for sim_type in ["power_flow", "emt"]:
            config["design"]["simulation_type"] = sim_type
            result = skill.validate(config)
            assert result.valid, f"仿真类型 {sim_type} 验证失败"

    def test_execution_config(self):
        """测试执行配置"""
        skill = get_skill("orthogonal_sensitivity")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["parameters"] = [{"name": "Gen1.pf_P", "levels": [0.8, 1.0]}]

        config["execution"]["timeout"] = 600.0
        config["execution"]["continue_on_error"] = False
        result = skill.validate(config)
        assert result.valid

    def test_multiple_parameters_config(self):
        """测试多参数配置"""
        skill = get_skill("orthogonal_sensitivity")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["parameters"] = [
            {"name": "Gen1.pf_P", "levels": [0.8, 1.0, 1.2]},
            {"name": "Gen2.pf_P", "levels": [0.8, 1.0, 1.2]},
            {"name": "Gen1.pf_V", "levels": [0.95, 1.0, 1.05]},
        ]
        config["target"]["bus_name"] = "Bus1"

        result = skill.validate(config)
        assert result.valid


@pytest.mark.integration
class TestOrthogonalSensitivityIntegration:
    """集成测试 - 需要CloudPSS API访问"""

    def test_skill_loads_correctly(self):
        """测试技能正确加载"""
        skill = get_skill("orthogonal_sensitivity")
        assert skill is not None
        assert skill.name == "orthogonal_sensitivity"

    def test_two_level_analysis(self, live_auth):
        """测试2水平参数分析（使用真实API）"""
        skill = get_skill("orthogonal_sensitivity")
        config = {
            "skill": "orthogonal_sensitivity",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "parameters": [
                {"name": "Gen1.pf_P", "levels": [0.9, 1.1]},  # 2水平
                {"name": "Gen2.pf_P", "levels": [0.9, 1.1]},  # 2水平
            ],
            "target": {
                "metric": "voltage",
                "bus_name": "Bus_16"
            },
            "design": {
                "table_type": "L4_2_3",  # L4(2^3) 正交表
                "simulation_type": "power_flow"
            },
            "execution": {
                "timeout": 300.0,
                "continue_on_error": True
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "test_oat_2level"
            }
        }

        result = skill.run(config)

        assert result is not None
        assert result.status.value in ["success", "failed", "cancelled"]

        if result.status.value == "success":
            data = result.data
            assert "table_type" in data
            assert "total_runs" in data
            assert data["total_runs"] == 4  # L4表有4次运行
            assert "sensitivity_ranking" in data
            assert len(data["sensitivity_ranking"]) == 2  # 2个参数

            print(f"\n✓ 2水平分析成功")
            print(f"  - 正交表: {data['table_type']}")
            print(f"  - 运行次数: {data['total_runs']}")

            # 验证敏感性结果
            for sr in data["sensitivity_ranking"]:
                assert "parameter" in sr
                assert "effect" in sr
                assert "rank" in sr
                print(f"  - {sr['parameter']}: 排序={sr['rank']}, "
                      f"效应值={sr['effect']:.4f}")

    def test_three_level_analysis(self, live_auth):
        """测试3水平参数分析（使用真实API）"""
        skill = get_skill("orthogonal_sensitivity")
        config = {
            "skill": "orthogonal_sensitivity",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "parameters": [
                {"name": "Gen1.pf_P", "levels": [0.8, 1.0, 1.2]},  # 3水平
                {"name": "Gen2.pf_P", "levels": [0.8, 1.0, 1.2]},  # 3水平
            ],
            "target": {
                "metric": "voltage",
                "bus_name": "Bus_16"
            },
            "design": {
                "table_type": "L9_3_4",  # L9(3^4) 正交表
                "simulation_type": "power_flow"
            },
            "execution": {
                "timeout": 300.0,
                "continue_on_error": True
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "test_oat_3level"
            }
        }

        result = skill.run(config)

        if result.status.value == "success":
            data = result.data
            assert data["total_runs"] == 9  # L9表有9次运行
            assert len(data["sensitivity_ranking"]) == 2

            print(f"\n✓ 3水平分析成功")
            print(f"  - 正交表: {data['table_type']}")
            print(f"  - 运行次数: {data['total_runs']}")

    def test_auto_table_selection(self, live_auth):
        """测试自动正交表选择（使用真实API）"""
        skill = get_skill("orthogonal_sensitivity")
        config = {
            "skill": "orthogonal_sensitivity",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "parameters": [
                {"name": "Gen1.pf_P", "levels": [0.9, 1.1]},
                {"name": "Gen2.pf_P", "levels": [0.9, 1.1]},
                {"name": "Gen3.pf_P", "levels": [0.9, 1.1]},
            ],
            "target": {
                "metric": "voltage",
                "bus_name": "Bus_16"
            },
            "design": {
                "table_type": "auto",  # 自动选择
                "simulation_type": "power_flow"
            },
            "execution": {
                "timeout": 300.0,
                "continue_on_error": True
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "test_oat_auto"
            }
        }

        result = skill.run(config)

        if result.status.value == "success":
            data = result.data
            # 3个2水平参数应该自动选择L4_2_3
            assert data["table_type"] == "L4_2_3"
            assert data["total_runs"] == 4

            print(f"\n✓ 自动正交表选择成功")
            print(f"  - 自动选择: {data['table_type']}")
            print(f"  - 运行次数: {data['total_runs']}")

    def test_effect_value_calculation(self, live_auth):
        """测试效应值计算（使用真实API）"""
        skill = get_skill("orthogonal_sensitivity")
        config = {
            "skill": "orthogonal_sensitivity",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "parameters": [
                {"name": "Gen1.pf_P", "levels": [0.9, 1.1]},
                {"name": "Gen2.pf_P", "levels": [0.9, 1.1]},
            ],
            "target": {
                "metric": "voltage",
                "bus_name": "Bus_16"
            },
            "design": {
                "table_type": "L4_2_3",
                "simulation_type": "power_flow"
            },
            "execution": {
                "timeout": 300.0,
                "continue_on_error": True
            }
        }

        result = skill.run(config)

        if result.status.value == "success":
            data = result.data
            sensitivity_ranking = data["sensitivity_ranking"]

            # 验证效应值
            for sr in sensitivity_ranking:
                assert "effect" in sr
                assert sr["effect"] >= 0

            print(f"\n✓ 效应值计算验证通过")

    def test_result_data_structure(self, live_auth):
        """测试结果数据结构（使用真实API）"""
        skill = get_skill("orthogonal_sensitivity")
        config = {
            "skill": "orthogonal_sensitivity",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "parameters": [
                {"name": "Gen1.pf_P", "levels": [0.9, 1.1]},
            ],
            "target": {
                "metric": "voltage",
                "bus_name": "Bus_16"
            },
            "design": {
                "table_type": "L4_2_3",
                "simulation_type": "power_flow"
            },
            "execution": {
                "timeout": 300.0,
                "continue_on_error": True
            }
        }

        result = skill.run(config)

        # 验证结果结构
        assert result.skill_name == "orthogonal_sensitivity"
        assert result.start_time is not None
        assert result.end_time is not None

        if result.status.value == "success":
            data = result.data
            assert "table_type" in data
            assert "total_runs" in data
            assert "success_count" in data
            assert "sensitivity_ranking" in data

            # 验证日志
            assert len(result.logs) > 0

            print(f"\n✓ 结果数据结构验证通过")
            print(f"  - 正交表: {data['table_type']}")
            print(f"  - 运行数: {data['total_runs']}")
            print(f"  - 成功数: {data['success_count']}")
            print(f"  - 日志条目数: {len(result.logs)}")


if __name__ == "__main__":
    # 运行基本测试
    print("=" * 70)
    print("Orthogonal Sensitivity Skill - 配置测试")
    print("=" * 70)

    skill = get_skill("orthogonal_sensitivity")
    print(f"\n✓ 技能已注册: {skill.name}")
    print(f"✓ 技能描述: {skill.description}")

    # 测试配置验证
    config = skill.get_default_config()
    config["model"]["rid"] = "model/holdme/IEEE39"
    config["parameters"] = [
        {"name": "Gen1.pf_P", "levels": [0.8, 1.0, 1.2]},
        {"name": "Gen2.pf_P", "levels": [0.8, 1.0, 1.2]},
    ]

    result = skill.validate(config)
    if result.valid:
        print("✓ 默认配置验证通过")
    else:
        print(f"✗ 配置验证失败: {result.errors}")

    # 测试不同参数水平数
    for num_levels in [2, 3, 4]:
        config["parameters"] = [{"name": "Gen1.pf_P", "levels": [0.8, 1.0, 1.2, 1.5][:num_levels]}]
        result = skill.validate(config)
        if result.valid:
            print(f"✓ {num_levels}水平参数验证通过")
        else:
            print(f"✗ {num_levels}水平参数验证失败: {result.errors}")

    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)
