"""
元数据集成测试

测试 model_builder 和 model_validator 与元数据系统的集成
"""

import pytest
import json
import tempfile
from pathlib import Path

from cloudpss_skills.metadata.integration import get_metadata_integration, MetadataIntegration
from cloudpss_skills.metadata import get_registry


class TestMetadataIntegration:
    """元数据集成测试"""

    def setup_method(self):
        """每个测试方法前初始化"""
        self.mi = get_metadata_integration()
        self.mi.initialize()

    def test_auto_complete_parameters(self):
        """测试参数自动补全"""
        # 用户只提供部分参数
        user_params = {'Vpcc': 0.69}
        completed = self.mi.auto_complete_parameters('model/CloudPSS/WGSource', user_params)

        # 应该补全所有参数
        assert len(completed) > len(user_params)
        # 默认值应该被填充
        assert 'Vbase' in completed
        assert 'Fnom' in completed
        assert 'Pnom' in completed

    def test_validate_parameters_missing_required(self):
        """测试缺少必需参数的验证"""
        # 缺少必需参数
        invalid_params = {'WindSpeed': 12.0}
        result = self.mi.validate_parameters('model/CloudPSS/WGSource', invalid_params)

        assert result.valid is False
        assert len(result.errors) > 0
        # 应该报告缺少必需参数
        assert any('缺少必需参数' in e for e in result.errors)

    def test_validate_parameters_valid(self):
        """测试有效参数的验证"""
        # 完整参数
        valid_params = {
            'Vbase': 0.69,
            'Fnom': 50.0,
            'Pnom': 100.0,
            'Vpcc': 0.69
        }
        result = self.mi.validate_parameters('model/CloudPSS/WGSource', valid_params)

        assert result.valid is True

    def test_get_required_parameters(self):
        """测试获取必需参数"""
        required = self.mi.get_required_parameters('model/CloudPSS/WGSource')

        assert isinstance(required, list)
        # WGSource 应该有必需参数
        assert len(required) > 0

    def test_get_pin_requirements(self):
        """测试获取引脚要求"""
        pins = self.mi.get_pin_requirements('model/CloudPSS/WGSource')

        assert 'total_pins' in pins
        assert 'required_pins' in pins
        assert 'electrical_pins' in pins

        # WGSource 应该有电气引脚
        assert len(pins['electrical_pins']) > 0

    def test_validate_pin_connection(self):
        """测试引脚连接验证"""
        # 未连接必需引脚
        result = self.mi.validate_pin_connection('model/CloudPSS/WGSource', {})
        assert result.valid is False

        # 正确连接
        result = self.mi.validate_pin_connection('model/CloudPSS/WGSource', {'0': 'Bus1'})
        assert result.valid is True

    def test_get_component_summary(self):
        """测试获取组件摘要"""
        summary = self.mi.get_component_summary('model/CloudPSS/WGSource')

        assert 'Component:' in summary
        assert 'Parameters:' in summary
        assert 'Pins:' in summary

    def test_unknown_component(self):
        """测试未知组件"""
        # 未知组件应该返回原始参数
        user_params = {'param1': 1.0}
        completed = self.mi.auto_complete_parameters('unknown/component', user_params)
        assert completed == user_params

        # 验证应该通过（跳过）
        result = self.mi.validate_parameters('unknown/component', user_params)
        assert result.valid is True


class TestModelBuilderIntegration:
    """Model Builder 集成测试（模拟测试）"""

    def setup_method(self):
        """每个测试方法前初始化"""
        self.mi = get_metadata_integration()
        self.mi.initialize()

    def test_add_component_with_metadata_validation(self):
        """测试添加组件时的元数据验证"""
        # 模拟添加 WGSource 组件
        comp_type = 'model/CloudPSS/WGSource'
        user_params = {'Vpcc': 0.69}

        # 自动补全参数
        completed_params = self.mi.auto_complete_parameters(comp_type, user_params)
        assert len(completed_params) > len(user_params)

        # 验证参数
        result = self.mi.validate_parameters(comp_type, completed_params)
        assert result.valid is True

        # 检查必需参数
        required = self.mi.get_required_parameters(comp_type)
        for param in required:
            assert param in completed_params

    def test_add_component_missing_required(self):
        """测试添加组件时缺少必需参数"""
        comp_type = 'model/CloudPSS/WGSource'
        # 故意不完整的参数
        incomplete_params = {'WindSpeed': 12.0}

        # 验证应该失败
        result = self.mi.validate_parameters(comp_type, incomplete_params)
        assert result.valid is False
        assert len(result.errors) > 0


class TestModelValidatorIntegration:
    """Model Validator 集成测试（模拟测试）"""

    def setup_method(self):
        """每个测试方法前初始化"""
        self.mi = get_metadata_integration()
        self.mi.initialize()

    def test_validate_component_with_metadata(self):
        """测试使用元数据验证组件"""
        # 模拟 WGSource 组件参数
        comp_type = 'model/CloudPSS/WGSource'
        args = {
            'Vbase': 0.69,
            'Fnom': 50.0,
            'Pnom': 100.0,
            'Vpcc': 0.69,
            'WindSpeed': 12.0
        }

        # 元数据验证
        result = self.mi.validate_parameters(comp_type, args)
        assert result.valid is True

        # 检查必需参数
        required = self.mi.get_required_parameters(comp_type)
        for param in required:
            assert param in args

    def test_validate_component_incomplete(self):
        """测试验证不完整的组件"""
        comp_type = 'model/CloudPSS/WGSource'
        # 缺少必需参数
        args = {'WindSpeed': 12.0}

        result = self.mi.validate_parameters(comp_type, args)
        assert result.valid is False
        assert len(result.errors) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
