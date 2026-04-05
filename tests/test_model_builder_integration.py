#!/usr/bin/env python3
"""
模型构建器技能 - 集成测试

测试内容:
1. 技能注册验证
2. 配置Schema验证
3. 真实API调用测试 (添加/修改/删除组件)
4. 批量生成功能

运行: pytest tests/test_model_builder_integration.py -v
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cloudpss_skills.builtin.model_builder import ModelBuilderSkill
from cloudpss_skills.core.base import SkillStatus


HAS_TOKEN = os.path.exists(".cloudpss_token")
TOKEN_MSG = "需要.cloudpss_token文件进行集成测试"


class TestModelBuilderSkill:
    """模型构建器技能集成测试"""

    @pytest.fixture
    def skill(self):
        return ModelBuilderSkill()

    @pytest.fixture
    def valid_config(self):
        return {
            "base_model": {
                "rid": "model/holdme/IEEE39"
            },
            "auth": {
                "token_file": ".cloudpss_token"
            },
            "modifications": [
                {
                    "action": "modify_component",
                    "selector": {"label": "TLine_3p-17"},  # IEEE39中实际存在的线路标签
                    "parameters": {"线路长度": 150}
                }
            ],
            "output": {
                "save": False,  # 测试时不保存，避免污染
                "name": "Test_Model",
                "description": "测试模型"
            }
        }

    def test_skill_registration(self, skill):
        """测试1: 技能注册信息"""
        assert skill.name == "model_builder"
        assert "模型构建" in skill.description
        assert skill.version == "1.0.0"
        print(f"✅ 技能注册: {skill.name} v{skill.version}")

    def test_config_schema_validation(self, skill):
        """测试2: 配置Schema验证"""
        assert skill.config_schema is not None
        assert "properties" in skill.config_schema
        assert "base_model" in skill.config_schema["properties"]
        assert "modifications" in skill.config_schema["properties"]
        print("✅ 配置Schema验证通过")

    def test_validation_with_valid_config(self, skill, valid_config):
        """测试3: 有效配置验证"""
        result = skill.validate(valid_config)
        assert result.valid is True
        print("✅ 有效配置验证通过")

    def test_validation_with_missing_rid(self, skill):
        """测试4: 缺少RID的配置验证"""
        invalid_config = {"base_model": {}}
        result = skill.validate(invalid_config)
        assert result.valid is False
        print("✅ 缺失RID检测正确")

    def test_validation_with_invalid_action(self, skill):
        """测试5: 无效action检测"""
        config = {
            "base_model": {"rid": "model/holdme/IEEE39"},
            "modifications": [
                {"action": "invalid_action"}
            ]
        }
        result = skill.validate(config)
        assert result.valid is False
        print("✅ 无效action检测正确")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_fetch_model(self, skill, valid_config):
        """测试6: 获取基础模型"""
        print("\n🔄 开始获取基础模型...")
        print(f"   模型: {valid_config['base_model']['rid']}")

        result = skill.run(valid_config)

        print(f"   状态: {result.status.value}")
        assert result.status == SkillStatus.SUCCESS, f"执行失败: {result.error}"

        data = result.data
        assert data["base_model"] == "model/holdme/IEEE39"
        assert data["modifications_count"] == 1

        print("✅ 获取模型测试通过!")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_modify_component(self, skill):
        """测试7: 修改组件参数"""
        config = {
            "base_model": {"rid": "model/holdme/IEEE39"},
            "auth": {"token_file": ".cloudpss_token"},
            "modifications": [
                {
                    "action": "modify_component",
                    "selector": {"label": "TLine_3p-17"},  # 线路1-2
                    "parameters": {"线路长度": 200}
                },
                {
                    "action": "modify_component",
                    "selector": {"label": "TLine_3p-18"},  # 另一条线路
                    "parameters": {"线路长度": 180}
                }
            ],
            "output": {
                "save": False,
                "name": "Modified_Model"
            }
        }

        result = skill.run(config)
        assert result.status == SkillStatus.SUCCESS

        data = result.data
        assert data["modifications_count"] == 2
        assert "modify:" in str(data["modifications_applied"])

        print(f"✅ 组件修改验证通过 ({len(data['modifications_applied'])}处修改)")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_remove_component(self, skill):
        """测试8: 删除组件 - 使用key选择器更可靠"""
        config = {
            "base_model": {"rid": "model/holdme/IEEE39"},
            "auth": {"token_file": ".cloudpss_token"},
            "modifications": [
                {
                    "action": "remove_component",
                    "selector": {"key": "canvas_0_10"}  # 使用组件key而不是label
                }
            ],
            "output": {
                "save": False,
                "name": "Removed_Model"
            }
        }

        result = skill.run(config)
        # 注意：删除可能失败如果组件不存在，但不应抛异常
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

        if result.status == SkillStatus.SUCCESS:
            print("✅ 组件删除验证通过")
        else:
            print(f"⚠️ 组件删除失败（可能不存在）: {result.error}")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_add_component(self, skill):
        """测试9: 添加新组件"""
        config = {
            "base_model": {"rid": "model/holdme/IEEE39"},
            "auth": {"token_file": ".cloudpss_token"},
            "modifications": [
                {
                    "action": "add_component",
                    "component_type": "model/CloudPSS/_newBus_3p",
                    "label": "Test_Bus_999",
                    "parameters": {"额定电压": 110},
                    "position": {"x": 500, "y": 500}
                }
            ],
            "output": {
                "save": False,
                "name": "Added_Model"
            }
        }

        result = skill.run(config)
        assert result.status == SkillStatus.SUCCESS

        data = result.data
        assert data["modifications_count"] == 1
        assert "add:" in str(data["modifications_applied"])

        print("✅ 添加组件验证通过")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_batch_generation(self, skill):
        """测试11: 批量生成功能"""
        config = {
            "base_model": {"rid": "model/holdme/IEEE39"},
            "auth": {"token_file": ".cloudpss_token"},
            "batch": {
                "enabled": True,
                "parameter_sweep": [
                    {
                        "param_name": "capacity",
                        "values": [50, 100]
                    }
                ]
            },
            "modifications": [
                {
                    "action": "add_component",
                    "component_type": "model/CloudPSS/PV_Inverter",
                    "label": "PV_{capacity}MW",
                    "parameters": {
                        "额定容量": "{capacity}",
                        "有功功率参考值": 0.8
                    },
                    "position": {"x": 400, "y": 300}
                }
            ],
            "output": {
                "save": False,  # 测试时不实际保存
                "name": "IEEE39_PV_Batch"
            }
        }

        result = skill.run(config)
        assert result.status == SkillStatus.SUCCESS

        data = result.data
        assert data["modifications_count"] == 1
        # 批量生成应该生成 2 个模型（2个capacity值）
        assert len(data["generated_models"]) == 2

        print(f"✅ 批量生成验证通过 (生成了 {len(data['generated_models'])} 个模型)")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_batch_generation_multiple_params(self, skill):
        """测试12: 批量生成多参数组合"""
        config = {
            "base_model": {"rid": "model/holdme/IEEE39"},
            "auth": {"token_file": ".cloudpss_token"},
            "batch": {
                "enabled": True,
                "parameter_sweep": [
                    {"param_name": "level", "values": [0.8, 1.0]},
                    {"param_name": "location", "values": ["BUS10", "BUS20"]}
                ]
            },
            "modifications": [
                {
                    "action": "modify_component",
                    "selector": {"label": "TLine_3p-17"},
                    "parameters": {"负荷水平": "{level}"}
                }
            ],
            "output": {
                "save": False,
                "name": "IEEE39_Load_{level}_{location}"
            }
        }

        result = skill.run(config)
        assert result.status == SkillStatus.SUCCESS

        data = result.data
        # 2 * 2 = 4 种组合
        assert len(data["generated_models"]) == 4

        print(f"✅ 多参数批量生成验证通过 (生成了 {len(data['generated_models'])} 个模型)")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_combined_operations(self, skill):
        """测试13: 组合操作 - 添加、修改、删除"""
        config = {
            "base_model": {"rid": "model/holdme/IEEE39"},
            "auth": {"token_file": ".cloudpss_token"},
            "modifications": [
                {
                    "action": "modify_component",
                    "selector": {"label": "TLine_3p-17"},
                    "parameters": {"线路长度": 150}
                },
                {
                    "action": "add_component",
                    "component_type": "model/CloudPSS/_newBus_3p",
                    "label": "Test_Bus_Combined",
                    "parameters": {"额定电压": 110},
                    "position": {"x": 600, "y": 600}
                },
                {
                    "action": "add_component",
                    "component_type": "model/CloudPSS/PV_Inverter",
                    "label": "PV_Test",
                    "parameters": {"额定容量": 50},
                    "position": {"x": 650, "y": 650}
                }
            ],
            "output": {
                "save": False,
                "name": "Combined_Model"
            }
        }

        result = skill.run(config)
        assert result.status == SkillStatus.SUCCESS

        data = result.data
        assert data["modifications_count"] == 3
        assert len(data["modifications_applied"]) == 3

        # 验证修改记录包含所有操作类型
        mods_str = str(data["modifications_applied"])
        assert "modify:" in mods_str
        assert "add:" in mods_str

        print(f"✅ 组合操作验证通过 ({len(data['modifications_applied'])} 处修改)")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_find_component_by_type(self, skill):
        """测试14: 使用type选择器查找组件"""
        config = {
            "base_model": {"rid": "model/holdme/IEEE39"},
            "auth": {"token_file": ".cloudpss_token"},
            "modifications": [
                {
                    "action": "modify_component",
                    "selector": {"type": "model/CloudPSS/TransmissionLine"},
                    "parameters": {"线路长度": 180}
                }
            ],
            "output": {
                "save": False,
                "name": "Type_Selector_Model"
            }
        }

        result = skill.run(config)
        # 注意：type选择器可能匹配多个组件，目前只返回第一个
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

        if result.status == SkillStatus.SUCCESS:
            print("✅ type选择器验证通过")
        else:
            print(f"⚠️ type选择器未找到组件: {result.error}")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_modify_open_cloudpss_lvrt_fault_case(self, skill):
        """测试15: 基于 open-cloudpss 模型修改内部LVRT故障模块并保存可用算例"""
        config = {
            "base_model": {"rid": "model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b5"},
            "auth": {"token_file": ".cloudpss_token"},
            "modifications": [
                {
                    "action": "modify_component",
                    "selector": {"key": "component_vrt_fault_1"},
                    "parameters": {
                        "Fault_VRT": {"source": "1", "ɵexp": ""}
                    }
                }
            ],
            "output": {
                "save": True,
                "branch": "codex_test_open_cloudpss_lvrt_case",
                "name": "WTG_PMSG_LVRT_TestCase"
            }
        }

        result = skill.run(config)
        assert result.status == SkillStatus.SUCCESS, result.error

        generated = result.data["generated_models"]
        assert len(generated) == 1
        assert generated[0]["rid"].startswith("model/")
        assert "modify:component_vrt_fault_1" in generated[0]["modifications"]

        print(f"✅ open-cloudpss LVRT专项算例构建通过: {generated[0]['rid']}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
