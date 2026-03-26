"""
CloudPSS Skill System - Registry Module

技能注册表，管理所有可用的技能。
"""

import importlib
import inspect
import pkgutil
from typing import Dict, List, Optional, Type
import logging

from .base import SkillBase

logger = logging.getLogger(__name__)

# 全局技能注册表
_SKILL_REGISTRY: Dict[str, SkillBase] = {}


def register(skill_class: Type[SkillBase]) -> Type[SkillBase]:
    """
    装饰器：注册技能类

    用法:
        @register
        class MySkill(SkillBase):
            ...

    Args:
        skill_class: 技能类

    Returns:
        原始技能类（不改变）
    """
    try:
        skill_instance = skill_class()
        _SKILL_REGISTRY[skill_instance.name] = skill_instance
        logger.debug(f"Registered skill: {skill_instance.name}")
    except Exception as e:
        logger.error(f"Failed to register skill {skill_class.__name__}: {e}")
        raise

    return skill_class


def get_skill(name: str) -> Optional[SkillBase]:
    """
    获取技能实例

    Args:
        name: 技能名称

    Returns:
        SkillBase实例，如果不存在则返回None
    """
    return _SKILL_REGISTRY.get(name)


def list_skills() -> List[SkillBase]:
    """
    列出所有已注册的技能

    Returns:
        技能实例列表
    """
    return list(_SKILL_REGISTRY.values())


def get_skill_names() -> List[str]:
    """
    获取所有技能名称

    Returns:
        技能名称列表
    """
    return list(_SKILL_REGISTRY.keys())


def has_skill(name: str) -> bool:
    """
    检查技能是否存在

    Args:
        name: 技能名称

    Returns:
        是否存在
    """
    return name in _SKILL_REGISTRY


def unregister(name: str) -> bool:
    """
    注销技能（主要用于测试）

    Args:
        name: 技能名称

    Returns:
        是否成功注销
    """
    if name in _SKILL_REGISTRY:
        del _SKILL_REGISTRY[name]
        return True
    return False


def clear_registry():
    """清空注册表（主要用于测试）"""
    _SKILL_REGISTRY.clear()


def discover_skills(package_name: str = "cloudpss_skills.builtin"):
    """
    自动发现并加载指定包中的所有技能

    扫描指定包中的所有模块，自动导入并注册技能。

    Args:
        package_name: 要扫描的包名
    """
    try:
        package = importlib.import_module(package_name)
    except ImportError as e:
        logger.warning(f"Cannot import package {package_name}: {e}")
        return

    for _, name, is_pkg in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        if is_pkg:
            continue

        try:
            module = importlib.import_module(name)
            logger.debug(f"Imported module: {name}")

            # 扫描模块中的SkillBase子类
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    inspect.isclass(attr)
                    and issubclass(attr, SkillBase)
                    and attr is not SkillBase
                    and not inspect.isabstract(attr)
                ):
                    # 如果类有register装饰器，实例化时会自动注册
                    # 否则手动注册
                    if attr_name not in [s.__class__.__name__ for s in list_skills()]:
                        try:
                            instance = attr()
                            if instance.name not in _SKILL_REGISTRY:
                                _SKILL_REGISTRY[instance.name] = instance
                                logger.debug(f"Auto-discovered skill: {instance.name}")
                        except Exception as e:
                            logger.warning(f"Failed to instantiate {attr_name}: {e}")

        except Exception as e:
            logger.warning(f"Failed to import module {name}: {e}")


def auto_discover():
    """自动发现并加载所有内置技能"""
    discover_skills("cloudpss_skills.builtin")
