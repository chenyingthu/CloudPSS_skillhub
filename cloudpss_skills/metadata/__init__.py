"""
CloudPSS 元件库元数据管理系统

提供从 CloudPSS 文档自动提取元件参数定义，
并在 model_builder 和 model_validator 中使用元数据进行
参数验证、自动补全和引脚检查。

使用示例:
    >>> from cloudpss_skills.metadata import get_registry, ComponentMetadata
    >>> registry = get_registry()
    >>> metadata = registry.get_component("model/CloudPSS/WGSource")
    >>> print(metadata.name)
    '风场等值模型I：PMSG网侧变流器模型'
    >>> params = metadata.auto_complete({"Vpcc": 0.69})
    >>> result = metadata.validate_parameters(params)
"""

from .models import (
    Parameter,
    PinDefinition,
    ParameterGroup,
    ComponentMetadata,
)

from .registry import (
    ComponentMetadataRegistry,
    get_registry,
)

from .parser import (
    ComponentDocumentParser,
    BatchMetadataExtractor,
)

from .integration import (
    MetadataIntegration,
    get_metadata_integration,
)

__all__ = [
    # 数据模型
    'Parameter',
    'PinDefinition',
    'ParameterGroup',
    'ComponentMetadata',
    # 注册表
    'ComponentMetadataRegistry',
    'get_registry',
    # 解析器
    'ComponentDocumentParser',
    'BatchMetadataExtractor',
    # 集成
    'MetadataIntegration',
    'get_metadata_integration',
]

__version__ = '1.0.0'
