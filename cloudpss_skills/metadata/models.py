"""
元数据模型定义

定义元件元数据的数据结构和验证逻辑
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
import logging

from cloudpss_skills.core.base import ValidationResult

logger = logging.getLogger(__name__)


@dataclass
class Parameter:
    """
    参数定义

    Attributes:
        key: 参数键名（英文）
        display_name: 显示名称（中文）
        type: 参数类型（real, integer, text, boolean, choice）
        unit: 单位（可选）
        description: 描述
        required: 是否必需
        default: 默认值
        choices: 选择项（仅用于 choice 类型）
        constraints: 约束条件（min, max, regex）
    """
    key: str
    display_name: str
    type: str  # 'real', 'integer', 'text', 'boolean', 'choice', 'virtual'
    unit: Optional[str] = None
    description: str = ""
    required: bool = False
    default: Any = None
    choices: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)

    def validate_value(self, value: Any) -> tuple[bool, Optional[str]]:
        """
        验证参数值

        Args:
            value: 待验证的值

        Returns:
            (是否有效, 错误信息)
        """
        # 类型验证
        if self.type == 'real':
            if not isinstance(value, (int, float)):
                return False, f"参数 {self.key} ({self.display_name}) 必须是实数，实际类型: {type(value).__name__}"
            value = float(value)

        elif self.type == 'integer':
            if not isinstance(value, int):
                return False, f"参数 {self.key} ({self.display_name}) 必须是整数，实际类型: {type(value).__name__}"

        elif self.type == 'boolean':
            if not isinstance(value, bool):
                return False, f"参数 {self.key} ({self.display_name}) 必须是布尔值，实际类型: {type(value).__name__}"

        elif self.type == 'text':
            if not isinstance(value, str):
                return False, f"参数 {self.key} ({self.display_name}) 必须是文本，实际类型: {type(value).__name__}"

        elif self.type == 'choice':
            if value not in self.choices:
                return False, f"参数 {self.key} ({self.display_name}) 必须是 {self.choices} 之一，实际值: {value}"

        elif self.type == 'virtual':
            # 虚拟引脚，通常用于输出
            pass

        # 范围验证（仅数值类型）
        if self.type in ('real', 'integer'):
            if 'min' in self.constraints:
                min_val = self.constraints['min']
                if value < min_val:
                    return False, f"参数 {self.key} ({self.display_name}) 必须 >= {min_val}，实际值: {value}"

            if 'max' in self.constraints:
                max_val = self.constraints['max']
                if value > max_val:
                    return False, f"参数 {self.key} ({self.display_name}) 必须 <= {max_val}，实际值: {value}"

        # 正则验证（仅文本类型）
        if self.type == 'text' and 'regex' in self.constraints:
            import re
            pattern = self.constraints['regex']
            if not re.match(pattern, str(value)):
                return False, f"参数 {self.key} ({self.display_name}) 格式不匹配正则: {pattern}"

        return True, None

    def get_default_value(self) -> Any:
        """获取默认值"""
        if self.default is not None:
            return self.default

        # 类型默认
        if self.type == 'real':
            return 0.0
        elif self.type == 'integer':
            return 0
        elif self.type == 'boolean':
            return False
        elif self.type == 'text':
            return ""
        elif self.type == 'choice' and self.choices:
            return self.choices[0]

        return None


@dataclass
class PinDefinition:
    """
    引脚定义

    Attributes:
        key: 引脚键名（通常是数字或标识符）
        name: 引脚显示名称
        type: 引脚类型（electrical, input, output）
        dimension: 维度（如 "3×1", "1×1"）
        description: 描述
        required: 是否必需连接
        valid_connections: 允许连接的目标类型
    """
    key: str
    name: str
    type: str  # 'electrical', 'input', 'output'
    dimension: str = "1×1"
    description: str = ""
    required: bool = False
    valid_connections: List[str] = field(default_factory=list)


@dataclass
class ParameterGroup:
    """
    参数组

    Attributes:
        group_id: 组标识符
        name: 组名称
        description: 组描述
        conditional: 条件显示规则
        parameters: 参数列表
    """
    group_id: str
    name: str
    description: str = ""
    conditional: Optional[Dict] = None
    parameters: List[Parameter] = field(default_factory=list)

    def get_required_params(self) -> List[Parameter]:
        """获取必需参数"""
        return [p for p in self.parameters if p.required]

    def get_param(self, key: str) -> Optional[Parameter]:
        """获取指定参数"""
        for p in self.parameters:
            if p.key == key:
                return p
        return None


@dataclass
class ComponentMetadata:
    """
    元件元数据

    Attributes:
        component_id: 元件唯一标识（如 model/CloudPSS/WGSource）
        name: 元件名称
        description: 元件描述
        version: 元数据版本
        category: 元件类别
        source: 来源信息（文档路径等）
        parameter_groups: 参数组列表
        pins: 引脚定义（按类型分组）
        validation_rules: 额外的验证规则
        simulation_support: 支持的仿真类型
    """
    component_id: str
    name: str
    description: str = ""
    version: str = "1.0.0"
    category: str = ""
    source: Dict = field(default_factory=dict)
    parameter_groups: List[ParameterGroup] = field(default_factory=list)
    pins: Dict[str, List[PinDefinition]] = field(default_factory=dict)
    validation_rules: Dict[str, Any] = field(default_factory=dict)
    simulation_support: Dict[str, bool] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict) -> 'ComponentMetadata':
        """从字典创建对象"""
        # 转换参数组
        groups = []
        for group_data in data.get('parameters', {}).get('groups', []):
            params = []
            for param_data in group_data.get('parameters', []):
                params.append(Parameter(
                    key=param_data['key'],
                    display_name=param_data.get('display_name', param_data['key']),
                    type=param_data.get('type', 'text'),
                    unit=param_data.get('unit'),
                    description=param_data.get('description', ''),
                    required=param_data.get('required', False),
                    default=param_data.get('default'),
                    choices=param_data.get('choices', []),
                    constraints=param_data.get('constraints', {})
                ))

            groups.append(ParameterGroup(
                group_id=group_data['group_id'],
                name=group_data['name'],
                description=group_data.get('description', ''),
                conditional=group_data.get('conditional'),
                parameters=params
            ))

        # 转换引脚
        pins_data = data.get('pins', {})
        pins = {'electrical': [], 'input': [], 'output': []}
        for pin_type in ['electrical', 'input', 'output']:
            for pin_data in pins_data.get(pin_type, []):
                pins[pin_type].append(PinDefinition(
                    key=pin_data['key'],
                    name=pin_data.get('name', pin_data['key']),
                    type=pin_data.get('type', pin_type),
                    dimension=pin_data.get('dimension', '1×1'),
                    description=pin_data.get('description', ''),
                    required=pin_data.get('required', False),
                    valid_connections=pin_data.get('valid_connections', [])
                ))

        return cls(
            component_id=data['component_id'],
            name=data['name'],
            description=data.get('description', ''),
            version=data.get('version', '1.0.0'),
            category=data.get('category', ''),
            source=data.get('source', {}),
            parameter_groups=groups,
            pins=pins,
            validation_rules=data.get('validation_rules', {}),
            simulation_support=data.get('simulation_support', {})
        )

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'component_id': self.component_id,
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'category': self.category,
            'source': self.source,
            'parameters': {
                'groups': [
                    {
                        'group_id': g.group_id,
                        'name': g.name,
                        'description': g.description,
                        'conditional': g.conditional,
                        'parameters': [
                            {
                                'key': p.key,
                                'display_name': p.display_name,
                                'type': p.type,
                                'unit': p.unit,
                                'description': p.description,
                                'required': p.required,
                                'default': p.default,
                                'choices': p.choices,
                                'constraints': p.constraints
                            }
                            for p in g.parameters
                        ]
                    }
                    for g in self.parameter_groups
                ]
            },
            'pins': {
                pin_type: [
                    {
                        'key': p.key,
                        'name': p.name,
                        'type': p.type,
                        'dimension': p.dimension,
                        'description': p.description,
                        'required': p.required,
                        'valid_connections': p.valid_connections
                    }
                    for p in pins
                ]
                for pin_type, pins in self.pins.items()
            },
            'validation_rules': self.validation_rules,
            'simulation_support': self.simulation_support
        }

    def get_all_parameters(self) -> List[Parameter]:
        """获取所有参数"""
        params = []
        for group in self.parameter_groups:
            params.extend(group.parameters)
        return params

    def get_parameter(self, key: str) -> Optional[Parameter]:
        """获取指定参数"""
        for group in self.parameter_groups:
            param = group.get_param(key)
            if param:
                return param
        return None

    def get_required_parameters(self) -> List[Parameter]:
        """获取所有必需参数"""
        return [p for p in self.get_all_parameters() if p.required]

    def get_all_pins(self) -> List[PinDefinition]:
        """获取所有引脚"""
        pins = []
        for pin_type in ['electrical', 'input', 'output']:
            pins.extend(self.pins.get(pin_type, []))
        return pins

    def get_required_pins(self) -> List[PinDefinition]:
        """获取所有必需引脚"""
        return [p for p in self.get_all_pins() if p.required]

    def validate_parameters(self, params: Dict[str, Any]) -> ValidationResult:
        """
        验证参数字典

        Args:
            params: 用户提供的参数

        Returns:
            ValidationResult: 验证结果
        """
        errors = []
        warnings = []

        # 获取所有参数定义
        all_params = {p.key: p for p in self.get_all_parameters()}

        # 检查必需参数
        for key, param in all_params.items():
            if param.required and key not in params:
                errors.append(f"缺少必需参数: {param.display_name} ({key})")

        # 验证每个参数值
        for key, value in params.items():
            if key not in all_params:
                warnings.append(f"未知参数: {key}")
                continue

            param = all_params[key]
            valid, message = param.validate_value(value)
            if not valid:
                errors.append(message)

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def auto_complete(self, user_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        自动补全参数

        使用用户提供的参数，补充默认值

        Args:
            user_params: 用户提供的参数

        Returns:
            完整的参数字典
        """
        complete = {}

        for group in self.parameter_groups:
            for param in group.parameters:
                if param.key in user_params:
                    complete[param.key] = user_params[param.key]
                elif param.default is not None:
                    complete[param.key] = param.default
                    logger.debug(f"使用默认值 {param.key}: {param.default}")
                elif param.required:
                    # 必需参数但没有提供也没有默认值
                    logger.warning(f"必需参数 {param.key} ({param.display_name}) 没有值")

        return complete

    def get_summary(self) -> str:
        """获取元数据摘要"""
        total_params = len(self.get_all_parameters())
        required_params = len(self.get_required_parameters())
        total_pins = len(self.get_all_pins())
        required_pins = len(self.get_required_pins())

        return (
            f"Component: {self.name} ({self.component_id})\n"
            f"  Parameters: {total_params} total, {required_params} required\n"
            f"  Pins: {total_pins} total, {required_pins} required\n"
            f"  Category: {self.category or 'Unknown'}\n"
            f"  Version: {self.version}"
        )
