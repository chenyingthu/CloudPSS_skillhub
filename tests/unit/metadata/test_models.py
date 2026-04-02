"""
元数据模型单元测试
"""

import pytest
from cloudpss_skills.metadata.models import (
    Parameter,
    PinDefinition,
    ParameterGroup,
    ComponentMetadata
)


class TestParameter:
    """参数模型测试"""

    def test_parameter_creation(self):
        """测试参数创建"""
        param = Parameter(
            key='test_param',
            display_name='测试参数',
            type='real',
            unit='kV',
            description='这是一个测试参数',
            required=True,
            default=10.5,
            constraints={'min': 0.0, 'max': 100.0}
        )

        assert param.key == 'test_param'
        assert param.display_name == '测试参数'
        assert param.type == 'real'
        assert param.unit == 'kV'
        assert param.default == 10.5

    def test_validate_value_real(self):
        """测试实数类型验证"""
        param = Parameter(
            key='voltage',
            display_name='电压',
            type='real',
            constraints={'min': 0.0, 'max': 1000.0}
        )

        # 有效值
        valid, msg = param.validate_value(220.5)
        assert valid is True
        assert msg is None

        # 范围检查
        valid, msg = param.validate_value(-10.0)
        assert valid is False
        assert '必须 >= 0.0' in msg

        valid, msg = param.validate_value(1500.0)
        assert valid is False
        assert '必须 <= 1000.0' in msg

        # 类型检查
        valid, msg = param.validate_value('invalid')
        assert valid is False
        assert '必须是实数' in msg

    def test_validate_value_integer(self):
        """测试整数类型验证"""
        param = Parameter(
            key='count',
            display_name='数量',
            type='integer'
        )

        valid, msg = param.validate_value(10)
        assert valid is True

        valid, msg = param.validate_value(10.5)
        assert valid is False
        assert '必须是整数' in msg

    def test_validate_value_boolean(self):
        """测试布尔类型验证"""
        param = Parameter(
            key='enabled',
            display_name='启用',
            type='boolean'
        )

        valid, msg = param.validate_value(True)
        assert valid is True

        valid, msg = param.validate_value('true')
        assert valid is False
        assert '必须是布尔值' in msg

    def test_validate_value_text(self):
        """测试文本类型验证"""
        param = Parameter(
            key='name',
            display_name='名称',
            type='text',
            constraints={'regex': r'^[A-Z][a-z]+$'}
        )

        valid, msg = param.validate_value('Hello')
        assert valid is True

        valid, msg = param.validate_value('hello')
        assert valid is False
        assert '格式不匹配' in msg

    def test_validate_value_choice(self):
        """测试选择类型验证"""
        param = Parameter(
            key='mode',
            display_name='模式',
            type='choice',
            choices=['auto', 'manual', 'disabled']
        )

        valid, msg = param.validate_value('auto')
        assert valid is True

        valid, msg = param.validate_value('invalid')
        assert valid is False
        assert '必须是' in msg

    def test_get_default_value(self):
        """测试获取默认值"""
        # 有明确默认值
        param1 = Parameter(
            key='p1',
            display_name='参数1',
            type='real',
            default=5.0
        )
        assert param1.get_default_value() == 5.0

        # 无默认值时使用类型默认
        param2 = Parameter(
            key='p2',
            display_name='参数2',
            type='real'
        )
        assert param2.get_default_value() == 0.0

        param3 = Parameter(
            key='p3',
            display_name='参数3',
            type='boolean'
        )
        assert param3.get_default_value() is False

        param4 = Parameter(
            key='p4',
            display_name='参数4',
            type='text'
        )
        assert param4.get_default_value() == ''

        param5 = Parameter(
            key='p5',
            display_name='参数5',
            type='choice',
            choices=['a', 'b']
        )
        assert param5.get_default_value() == 'a'


class TestPinDefinition:
    """引脚定义测试"""

    def test_pin_creation(self):
        """测试引脚创建"""
        pin = PinDefinition(
            key='1',
            name='正极',
            type='electrical',
            dimension='3×1',
            description='电源正极引脚',
            required=True
        )

        assert pin.key == '1'
        assert pin.name == '正极'
        assert pin.type == 'electrical'
        assert pin.dimension == '3×1'
        assert pin.required is True


class TestParameterGroup:
    """参数组测试"""

    def test_group_creation(self):
        """测试参数组创建"""
        params = [
            Parameter(key='p1', display_name='参数1', type='real'),
            Parameter(key='p2', display_name='参数2', type='integer', required=True)
        ]

        group = ParameterGroup(
            group_id='basic',
            name='基础参数',
            description='基础配置参数',
            parameters=params
        )

        assert group.group_id == 'basic'
        assert group.name == '基础参数'
        assert len(group.parameters) == 2

    def test_get_required_params(self):
        """测试获取必需参数"""
        params = [
            Parameter(key='p1', display_name='参数1', type='real'),
            Parameter(key='p2', display_name='参数2', type='integer', required=True),
            Parameter(key='p3', display_name='参数3', type='boolean', required=True)
        ]

        group = ParameterGroup(
            group_id='test',
            name='测试组',
            parameters=params
        )

        required = group.get_required_params()
        assert len(required) == 2
        assert all(p.required for p in required)

    def test_get_param(self):
        """测试获取指定参数"""
        params = [
            Parameter(key='p1', display_name='参数1', type='real'),
            Parameter(key='p2', display_name='参数2', type='integer')
        ]

        group = ParameterGroup(
            group_id='test',
            name='测试组',
            parameters=params
        )

        param = group.get_param('p1')
        assert param is not None
        assert param.key == 'p1'

        param = group.get_param('nonexistent')
        assert param is None


class TestComponentMetadata:
    """组件元数据测试"""

    def test_component_creation(self):
        """测试组件元数据创建"""
        groups = [
            ParameterGroup(
                group_id='basic',
                name='基础参数',
                parameters=[
                    Parameter(key='Vpcc', display_name='并网点电压', type='real', default=0.69)
                ]
            )
        ]

        pins = {
            'electrical': [
                PinDefinition(key='0', name='N', type='electrical')
            ]
        }

        component = ComponentMetadata(
            component_id='model/CloudPSS/WGSource',
            name='风场等值模型',
            description='风场等值模型I：PMSG网侧变流器模型',
            category='renewable',
            parameter_groups=groups,
            pins=pins
        )

        assert component.component_id == 'model/CloudPSS/WGSource'
        assert component.name == '风场等值模型'
        assert component.category == 'renewable'

    def test_from_dict_to_dict(self):
        """测试序列化和反序列化"""
        original = ComponentMetadata(
            component_id='model/test',
            name='测试组件',
            description='用于测试的组件',
            parameter_groups=[
                ParameterGroup(
                    group_id='g1',
                    name='组1',
                    parameters=[
                        Parameter(
                            key='param1',
                            display_name='参数1',
                            type='real',
                            unit='kV',
                            default=10.5
                        )
                    ]
                )
            ],
            pins={
                'electrical': [
                    PinDefinition(key='1', name='引脚1', type='electrical')
                ]
            }
        )

        # 序列化
        data = original.to_dict()

        # 反序列化
        restored = ComponentMetadata.from_dict(data)

        assert restored.component_id == original.component_id
        assert restored.name == original.name
        assert len(restored.parameter_groups) == 1
        assert len(restored.pins['electrical']) == 1

    def test_get_all_parameters(self):
        """测试获取所有参数"""
        component = ComponentMetadata(
            component_id='model/test',
            name='测试组件',
            parameter_groups=[
                ParameterGroup(
                    group_id='g1',
                    name='组1',
                    parameters=[
                        Parameter(key='p1', display_name='参数1', type='real'),
                        Parameter(key='p2', display_name='参数2', type='integer')
                    ]
                ),
                ParameterGroup(
                    group_id='g2',
                    name='组2',
                    parameters=[
                        Parameter(key='p3', display_name='参数3', type='boolean')
                    ]
                )
            ]
        )

        all_params = component.get_all_parameters()
        assert len(all_params) == 3

    def test_get_required_parameters(self):
        """测试获取必需参数"""
        component = ComponentMetadata(
            component_id='model/test',
            name='测试组件',
            parameter_groups=[
                ParameterGroup(
                    group_id='g1',
                    name='组1',
                    parameters=[
                        Parameter(key='p1', display_name='参数1', type='real', required=True),
                        Parameter(key='p2', display_name='参数2', type='integer')
                    ]
                )
            ]
        )

        required = component.get_required_parameters()
        assert len(required) == 1
        assert required[0].key == 'p1'

    def test_validate_parameters(self):
        """测试参数验证"""
        component = ComponentMetadata(
            component_id='model/test',
            name='测试组件',
            parameter_groups=[
                ParameterGroup(
                    group_id='g1',
                    name='组1',
                    parameters=[
                        Parameter(key='required_param', display_name='必需参数', type='real', required=True),
                        Parameter(key='optional_param', display_name='可选参数', type='integer', constraints={'min': 0, 'max': 100})
                    ]
                )
            ]
        )

        # 缺少必需参数
        result = component.validate_parameters({'optional_param': 50})
        assert result.valid is False
        assert any('缺少必需参数' in e for e in result.errors)

        # 参数值超出范围
        result = component.validate_parameters({
            'required_param': 10.0,
            'optional_param': 200
        })
        assert result.valid is False
        assert any('必须 <=' in e for e in result.errors)

        # 有效参数
        result = component.validate_parameters({
            'required_param': 10.0,
            'optional_param': 50
        })
        assert result.valid is True

    def test_auto_complete(self):
        """测试参数自动补全"""
        component = ComponentMetadata(
            component_id='model/test',
            name='测试组件',
            parameter_groups=[
                ParameterGroup(
                    group_id='g1',
                    name='组1',
                    parameters=[
                        Parameter(key='p1', display_name='参数1', type='real', default=10.0),
                        Parameter(key='p2', display_name='参数2', type='integer', default=5),
                        Parameter(key='p3', display_name='参数3', type='text')  # 无默认值
                    ]
                )
            ]
        )

        user_params = {'p1': 20.0}
        completed = component.auto_complete(user_params)

        # 用户提供的值应保留
        assert completed['p1'] == 20.0
        # 默认值应填充
        assert completed['p2'] == 5

    def test_get_summary(self):
        """测试获取摘要"""
        component = ComponentMetadata(
            component_id='model/test',
            name='测试组件',
            category='test_category',
            parameter_groups=[
                ParameterGroup(
                    group_id='g1',
                    name='组1',
                    parameters=[
                        Parameter(key='p1', display_name='参数1', type='real', required=True),
                        Parameter(key='p2', display_name='参数2', type='integer')
                    ]
                )
            ],
            pins={
                'electrical': [
                    PinDefinition(key='1', name='引脚1', type='electrical', required=True)
                ]
            }
        )

        summary = component.get_summary()
        assert 'Component: 测试组件' in summary
        assert 'Parameters: 2 total, 1 required' in summary
        assert 'Pins: 1 total, 1 required' in summary
        assert 'Category: test_category' in summary


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
