"""
收纳大师核心模块 - CloudPSS SkillHub Master Organizer

提供基础数据管理功能：
- ID 生成与管理
- 路径管理
- 配置管理
- 加密服务
- 注册表基类

使用示例：
    >>> from cloudpss_skills_v3.master_organizer.core import (
    ...     IDGenerator, EntityType,
    ...     PathManager, get_path_manager,
    ...     ConfigManager, get_config_manager,
    ...     CryptoManager, get_crypto_manager,
    ...     RegistryBase, RegistryEntry
    ... )
    >>>
    >>> # 生成ID
    >>> case_id = IDGenerator.generate(EntityType.CASE)
    >>>
    >>> # 获取路径
    >>> pm = get_path_manager()
    >>> case_path = pm.get_case_path(case_id)
    >>>
    >>> # 管理配置
    >>> cm = get_config_manager()
    >>> config = cm.get_user_config()
"""

from .id_generator import IDGenerator, EntityType, generate_id, validate_id, parse_id
from .path_manager import PathManager, get_path_manager
from .config_manager import ConfigManager, get_config_manager, UserConfig, UserPreferences, StorageQuotas
from .crypto import CryptoManager, MockCryptoManager, get_crypto_manager
from .registry_base import RegistryBase, RegistryEntry

__all__ = [
    # ID 生成器
    'IDGenerator',
    'EntityType',
    'generate_id',
    'validate_id',
    'parse_id',

    # 路径管理
    'PathManager',
    'get_path_manager',

    # 配置管理
    'ConfigManager',
    'get_config_manager',
    'UserConfig',
    'UserPreferences',
    'StorageQuotas',

    # 加密
    'CryptoManager',
    'MockCryptoManager',
    'get_crypto_manager',

    # 注册表
    'RegistryBase',
    'RegistryEntry',
]

__version__ = '1.0.0'
