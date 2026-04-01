#!/usr/bin/env python3
"""
模型构建器技能 - 单元测试

测试内容:
1. 参数占位符替换逻辑
2. 配置验证逻辑
3. 组件选择器匹配逻辑
4. 批量生成功能

运行: pytest tests/test_model_builder_unit.py -v
"""

import os
import sys
import pytest
from unittest.mock import Mock, MagicMock, patch
from copy import deepcopy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cloudpss_skills.builtin.model_builder import (
    ModelBuilderSkill,
    ComponentModification,
    GeneratedModel
)
from cloudpss_skills.core.base import SkillStatus


class TestModelBuilderUnit:
    """模型构建器技能单元测试"""

    @pytest.fixture
    def skill(self):
        """创建技能实例"""
        return ModelBuilderSkill()

    def test_default_component_types(self, skill):
        """测试默认组件类型列表"""
        assert len(skill.DEFAULT_COMPONENT_TYPES) == 9
        assert "model/CloudPSS/_newBus_3p" in skill.DEFAULT_COMPONENT_TYPES
        assert "model/CloudPSS/PV_Inverter" in skill.DEFAULT_COMPONENT_TYPES
        assert "model/CloudPSS/DistanceRelay" in skill.DEFAULT_COMPONENT_TYPES
        print("✅ 默认组件类型列表正确")

    def test_validate_valid_config(self, skill):
        """测试有效配置验证"""
        config = {
            "base_model": {"rid": "model/holdme/IEEE39"},
            "modifications": [
                {
                    "action": "add_component",
                    "component_type": "model/CloudPSS/_newBus_3p",
                    "label": "BUS_NEW"
                },
                {
                    "action": "modify_component",
                    "selector": {"label": "TLine_3p-17"},
                    "parameters": {"线路长度": 150}
                },
                {
                    "action": "remove_component",
                    "selector": {"key": "canvas_0_10"}
                }
            ]
        }
        result = skill.validate(config)
        assert result.valid is True
        assert len(result.errors) == 0
        print("✅ 有效配置验证通过")

    def test_validate_missing_rid(self, skill):
        """测试缺少RID的配置验证"""
        config = {"base_model": {}}
        result = skill.validate(config)
        assert result.valid is False
        assert "必须指定基础模型RID" in result.errors
        print("✅ 缺少RID检测正确")

    def test_validate_add_component_missing_fields(self, skill):
        """测试添加组件缺少必需字段"""
        config = {
            "base_model": {"rid": "model/holdme/IEEE39"},
            "modifications": [
                {"action": "add_component"}  # 缺少 component_type 和 label
            ]
        }
        result = skill.validate(config)
        assert result.valid is False
        assert any("component_type" in err for err in result.errors)
        assert any("label" in err for err in result.errors)
        print("✅ 添加组件缺少字段检测正确")

    def test_validate_modify_component_missing_selector(self, skill):
        """测试修改组件缺少选择器"""
        config = {
            "base_model": {"rid": "model/holdme/IEEE39"},
            "modifications": [
                {"action": "modify_component", "parameters": {"线路长度": 150}}
            ]
        }
        result = skill.validate(config)
        assert result.valid is False
        assert any("selector" in err for err in result.errors)
        print("✅ 修改组件缺少选择器检测正确")

    def test_validate_remove_component_missing_selector(self, skill):
        """测试删除组件缺少选择器"""
        config = {
            "base_model": {"rid": "model/holdme/IEEE39"},
            "modifications": [
                {"action": "remove_component"}
            ]
        }
        result = skill.validate(config)
        assert result.valid is False
        assert any("selector" in err for err in result.errors)
        print("✅ 删除组件缺少选择器检测正确")

    def test_validate_invalid_action(self, skill):
        """测试无效action检测"""
        config = {
            "base_model": {"rid": "model/holdme/IEEE39"},
            "modifications": [
                {"action": "invalid_action"}
            ]
        }
        result = skill.validate(config)
        assert result.valid is False
        assert any("invalid_action" in err for err in result.errors)
        print("✅ 无效action检测正确")

    def test_get_modifications_with_params_simple(self, skill):
        """测试简单参数占位符替换"""
        skill._original_modifications = [
            {
                "action": "add_component",
                "component_type": "model/CloudPSS/PV_Inverter",
                "label": "PV_{capacity}MW",
                "parameters": {
                    "额定容量": "{capacity}",
                    "固定参数": "不变"
                }
            }
        ]

        params = {"capacity": 100}
        result = skill._get_modifications_with_params(params)

        assert len(result) == 1
        assert result[0]["label"] == "PV_100MW"
        assert result[0]["parameters"]["额定容量"] == "100"
        assert result[0]["parameters"]["固定参数"] == "不变"
        print("✅ 简单参数占位符替换正确")

    def test_get_modifications_with_params_multiple(self, skill):
        """测试多个参数占位符替换"""
        skill._original_modifications = [
            {
                "action": "add_component",
                "component_type": "model/CloudPSS/PV_Inverter",
                "label": "PV_{location}_{capacity}MW",
                "parameters": {
                    "额定容量": "{capacity}",
                    "位置": "{location}"
                }
            }
        ]

        params = {"capacity": 150, "location": "BUS10"}
        result = skill._get_modifications_with_params(params)

        # 验证两个参数都被替换
        assert "BUS10" in result[0]["label"]
        assert "150" in result[0]["label"]
        assert result[0]["parameters"]["额定容量"] == "150"
        assert result[0]["parameters"]["位置"] == "BUS10"
        print("✅ 多个参数占位符替换正确")

    def test_get_modifications_with_params_no_placeholder(self, skill):
        """测试无占位符的配置"""
        skill._original_modifications = [
            {
                "action": "modify_component",
                "selector": {"label": "TLine_3p-17"},
                "parameters": {
                    "线路长度": 200
                }
            }
        ]

        params = {"unused": "value"}
        result = skill._get_modifications_with_params(params)

        assert len(result) == 1
        assert result[0]["selector"]["label"] == "TLine_3p-17"
        assert result[0]["parameters"]["线路长度"] == 200
        print("✅ 无占位符配置保持不变")

    def test_get_modifications_preserves_original(self, skill):
        """测试原始配置不被修改"""
        original = [
            {
                "action": "add_component",
                "label": "PV_{capacity}MW",
                "parameters": {"容量": "{capacity}"}
            }
        ]
        skill._original_modifications = deepcopy(original)

        params = {"capacity": 100}
        result = skill._get_modifications_with_params(params)

        # 验证原始配置未被修改
        assert skill._original_modifications[0]["label"] == "PV_{capacity}MW"
        assert skill._original_modifications[0]["parameters"]["容量"] == "{capacity}"
        # 验证新配置已替换
        assert result[0]["label"] == "PV_100MW"
        assert result[0]["parameters"]["容量"] == "100"
        print("✅ 原始配置未被修改")

    def test_get_modifications_multiple_mods(self, skill):
        """测试多个修改配置的参数替换"""
        skill._original_modifications = [
            {
                "action": "add_component",
                "label": "PV_{capacity}MW",
                "parameters": {"额定容量": "{capacity}"}
            },
            {
                "action": "modify_component",
                "selector": {"label": "Load_{load_id}"},
                "parameters": {"有功功率": "{power}"}
            }
        ]

        params = {"capacity": 200, "load_id": 5, "power": 50}
        result = skill._get_modifications_with_params(params)

        assert len(result) == 2
        assert result[0]["label"] == "PV_200MW"
        assert result[1]["selector"]["label"] == "Load_5"
        assert result[1]["parameters"]["有功功率"] == "50"
        print("✅ 多个修改配置参数替换正确")


class TestModelBuilderDataClasses:
    """测试数据类"""

    def test_component_modification_creation(self):
        """测试 ComponentModification 数据类"""
        mod = ComponentModification(
            action="add_component",
            component_type="model/CloudPSS/_newBus_3p",
            label="BUS_NEW",
            parameters={"额定电压": 110},
            position={"x": 100, "y": 200}
        )
        assert mod.action == "add_component"
        assert mod.label == "BUS_NEW"
        assert mod.parameters["额定电压"] == 110
        assert mod.position["x"] == 100
        print("✅ ComponentModification 创建正确")

    def test_component_modification_defaults(self):
        """测试 ComponentModification 默认值"""
        mod = ComponentModification(action="remove_component")
        assert mod.action == "remove_component"
        assert mod.component_type is None
        assert mod.label is None
        assert mod.parameters == {}
        assert mod.selector is None
        assert mod.position is None
        print("✅ ComponentModification 默认值正确")

    def test_generated_model_creation(self):
        """测试 GeneratedModel 数据类"""
        model = GeneratedModel(
            name="Test_Model",
            rid="model/holdme/test",
            description="测试模型",
            modifications_applied=["add:BUS1", "modify:LINE1"]
        )
        assert model.name == "Test_Model"
        assert model.rid == "model/holdme/test"
        assert len(model.modifications_applied) == 2
        print("✅ GeneratedModel 创建正确")


class TestModelBuilderMockIntegration:
    """使用 Mock 的集成测试"""

    @pytest.fixture
    def skill(self):
        return ModelBuilderSkill()

    @patch('cloudpss.setToken')
    @patch('cloudpss.Model')
    def test_run_with_mock_model(self, mock_model_class, mock_set_token, skill):
        """测试使用 Mock 模型的运行流程"""
        # 创建 Mock 模型
        mock_model = Mock()
        mock_model.name = "TestModel"
        mock_model.save.return_value = {"rid": "model/holdme/test_branch"}
        mock_model_class.fetch.return_value = mock_model

        config = {
            "base_model": {"rid": "model/holdme/IEEE39"},
            "auth": {"token": "test_token"},
            "modifications": [],
            "output": {
                "save": True,
                "branch": "test_branch",
                "name": "Test_Model"
            }
        }

        result = skill.run(config)

        assert result.status == SkillStatus.SUCCESS
        assert result.data["base_model"] == "model/holdme/IEEE39"
        assert result.data["modifications_count"] == 0
        assert len(result.data["generated_models"]) == 1
        mock_set_token.assert_called_once_with("test_token")
        mock_model_class.fetch.assert_called_once_with("model/holdme/IEEE39")
        mock_model.save.assert_called_once_with("test_branch")
        print("✅ Mock 模型运行流程测试通过")

    @patch('cloudpss.setToken')
    @patch('cloudpss.Model')
    def test_run_without_save(self, mock_model_class, mock_set_token, skill):
        """测试不保存的运行流程"""
        mock_model = Mock()
        mock_model.name = "TestModel"
        mock_model_class.fetch.return_value = mock_model

        config = {
            "base_model": {"rid": "model/holdme/IEEE39"},
            "auth": {"token": "test_token"},
            "modifications": [],
            "output": {"save": False}
        }

        result = skill.run(config)

        assert result.status == SkillStatus.SUCCESS
        assert len(result.data["generated_models"]) == 0
        mock_model.save.assert_not_called()
        print("✅ 不保存模式测试通过")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
