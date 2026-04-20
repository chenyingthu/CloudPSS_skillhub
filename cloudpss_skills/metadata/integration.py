"""
元数据集成工具

为 model_builder 和 model_validator 提供元数据支持
"""

import logging
from typing import Dict, List, Any, Optional

from cloudpss_skills.metadata import get_registry, ComponentMetadata
from cloudpss_skills.core.base import ValidationResult

logger = logging.getLogger(__name__)


class MetadataIntegration:
    """
    元数据集成类

    提供组件参数自动补全、验证等功能
    """

    def __init__(self):
        self.registry = get_registry()
        self._initialized = False

    def initialize(self, metadata_dir: Optional[str] = None):
        """初始化，加载元数据"""
        if self._initialized:
            return

        # 尝试从示例目录加载
        if metadata_dir:
            self.registry.load_from_directory(metadata_dir)
        else:
            # 尝试加载内置示例
            import os
            builtin_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'examples', 'metadata')
            if os.path.exists(builtin_dir):
                self.registry.load_from_directory(builtin_dir)

        self._initialized = True
        logger.info(f"元数据集成已初始化，注册了 {len(self.registry)} 个组件")

    def get_component_metadata(self, component_type: str) -> Optional[ComponentMetadata]:
        """获取组件元数据"""
        if not self._initialized:
            self.initialize()

        # 尝试多种格式的组件ID
        metadata = self.registry.get_component(component_type)
        if metadata:
            return metadata

        # 尝试简化格式
        simple_id = component_type.split('/')[-1] if '/' in component_type else component_type
        for comp_id in self.registry.list_components():
            if comp_id.endswith(simple_id) or simple_id in comp_id:
                return self.registry.get_component(comp_id)

        return None

    def auto_complete_parameters(self, component_type: str, user_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        自动补全组件参数

        Args:
            component_type: 组件类型RID
            user_params: 用户提供的参数

        Returns:
            补全后的参数（包含默认值）
        """
        metadata = self.get_component_metadata(component_type)
        if not metadata:
            logger.warning(f"未找到组件 {component_type} 的元数据，返回原始参数")
            return user_params

        completed = metadata.auto_complete(user_params)

        # 记录补全的参数
        for key, value in completed.items():
            if key not in user_params:
                logger.debug(f"参数补全: {key} = {value}")

        return completed

    def validate_parameters(self, component_type: str, params: Dict[str, Any]) -> ValidationResult:
        """
        验证组件参数

        Args:
            component_type: 组件类型RID
            params: 参数字典

        Returns:
            验证结果
        """
        metadata = self.get_component_metadata(component_type)
        if not metadata:
            logger.warning(f"未找到组件 {component_type} 的元数据，跳过验证")
            return ValidationResult(valid=True)

        result = metadata.validate_parameters(params)

        if result.valid:
            logger.debug(f"组件 {component_type} 参数验证通过")
        else:
            logger.warning(f"组件 {component_type} 参数验证失败: {result.errors}")

        return result

    def get_required_parameters(self, component_type: str) -> List[str]:
        """
        获取组件的必需参数列表

        Args:
            component_type: 组件类型RID

        Returns:
            必需参数键名列表
        """
        metadata = self.get_component_metadata(component_type)
        if not metadata:
            return []

        return [p.key for p in metadata.get_required_parameters()]

    def get_pin_requirements(self, component_type: str) -> Dict[str, Any]:
        """
        获取组件引脚要求

        Args:
            component_type: 组件类型RID

        Returns:
            引脚要求信息
        """
        metadata = self.get_component_metadata(component_type)
        if not metadata:
            return {}

        pins = metadata.get_all_pins()
        required_pins = metadata.get_required_pins()

        return {
            'total_pins': len(pins),
            'required_pins': [p.key for p in required_pins],
            'electrical_pins': [p.key for p in pins if p.type == 'electrical'],
            'input_pins': [p.key for p in pins if p.type == 'input'],
            'output_pins': [p.key for p in pins if p.type == 'output'],
        }

    def validate_pin_connection(self, component_type: str, pins: Dict[str, str]) -> ValidationResult:
        """
        验证引脚连接

        Args:
            component_type: 组件类型RID
            pins: 引脚连接字典 {pin_name: target_bus}

        Returns:
            验证结果
        """
        metadata = self.get_component_metadata(component_type)
        if not metadata:
            return ValidationResult(valid=True)

        errors = []
        required_pins = metadata.get_required_pins()

        for pin in required_pins:
            if pin.key not in pins or not pins.get(pin.key):
                errors.append(f"必需引脚 '{pin.key}' ({pin.name}) 未连接")

        return ValidationResult(valid=len(errors) == 0, errors=errors)

    def get_component_summary(self, component_type: str) -> str:
        """获取组件摘要信息"""
        metadata = self.get_component_metadata(component_type)
        if not metadata:
            return f"组件 {component_type}: 无元数据"
        return metadata.get_summary()

    def list_available_components(self, category: Optional[str] = None) -> List[str]:
        """列出可用的组件类型"""
        if not self._initialized:
            self.initialize()
        return self.registry.list_components(category=category)


# 全局实例
_metadata_integration: Optional[MetadataIntegration] = None


def get_metadata_integration() -> MetadataIntegration:
    """获取全局元数据集成实例"""
    global _metadata_integration
    if _metadata_integration is None:
        _metadata_integration = MetadataIntegration()
    return _metadata_integration
