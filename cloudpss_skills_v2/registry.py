"""
Skill Registry - 统一技能注册与发现系统

提供全局技能注册表，支持：
- 技能注册与发现
- 按类别查询技能
- 动态技能加载
- 技能元数据管理

示例：
    >>> from cloudpss_skills_v2 import get_skill, list_skills
    >>> skill = get_skill("hdf5_export")
    >>> print(skill.name)
    >>> all_skills = list_skills()
    >>> tools = list_skills(category="tool")
"""

from __future__ import annotations

from typing import Any, Type, Callable
from functools import wraps
from cloudpss_skills_v2.core.skill_result import SkillResult


class SkillInfo:
    """技能信息容器"""
    
    def __init__(
        self,
        name: str,
        category: str,
        skill_class: Type,
        description: str = "",
        version: str = "2.0.0",
        author: str = "",
        tags: list[str] | None = None,
    ):
        self.name = name
        self.category = category
        self.skill_class = skill_class
        self.description = description
        self.version = version
        self.author = author
        self.tags = tags or []
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "tags": self.tags,
        }


class SkillRegistry:
    """全局技能注册表
    
    单例模式，管理所有技能的注册与发现。
    """
    
    _instance: SkillRegistry | None = None
    _skills: dict[str, SkillInfo]
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._skills = {}
        return cls._instance
    
    @classmethod
    def register(
        cls,
        name: str,
        category: str,
        skill_class: Type,
        description: str = "",
        version: str = "2.0.0",
        author: str = "",
        tags: list[str] | None = None,
    ) -> None:
        """注册技能
        
        Args:
            name: 技能名称（唯一标识）
            category: 类别（tool/poweranalysis）
            skill_class: 技能类
            description: 描述
            version: 版本
            author: 作者
            tags: 标签列表
        """
        instance = cls()
        instance._skills[name] = SkillInfo(
            name=name,
            category=category,
            skill_class=skill_class,
            description=description,
            version=version,
            author=author,
            tags=tags,
        )
    
    @classmethod
    def get(cls, name: str) -> Type | None:
        """获取技能类
        
        Args:
            name: 技能名称
            
        Returns:
            技能类，如果不存在返回 None
        """
        instance = cls()
        info = instance._skills.get(name)
        return info.skill_class if info else None
    
    @classmethod
    def get_info(cls, name: str) -> SkillInfo | None:
        """获取技能信息
        
        Args:
            name: 技能名称
            
        Returns:
            SkillInfo 对象，如果不存在返回 None
        """
        instance = cls()
        return instance._skills.get(name)
    
    @classmethod
    def list_skills(cls, category: str | None = None) -> list[str]:
        """列出所有技能名称
        
        Args:
            category: 可选，按类别过滤
            
        Returns:
            技能名称列表
        """
        instance = cls()
        if category:
            return [
                name for name, info in instance._skills.items()
                if info.category == category
            ]
        return list(instance._skills.keys())
    
    @classmethod
    def list_all(cls) -> dict[str, SkillInfo]:
        """获取所有技能信息"""
        instance = cls()
        return instance._skills.copy()
    
    @classmethod
    def create_skill(cls, name: str, *args, **kwargs) -> Any:
        """创建技能实例
        
        Args:
            name: 技能名称
            *args, **kwargs: 传递给技能构造函数的参数
            
        Returns:
            技能实例
            
        Raises:
            ValueError: 技能不存在
        """
        skill_class = cls.get(name)
        if skill_class is None:
            raise ValueError(f"技能不存在: {name}")
        return skill_class(*args, **kwargs)
    
    @classmethod
    def unregister(cls, name: str) -> bool:
        """注销技能
        
        Args:
            name: 技能名称
            
        Returns:
            是否成功注销
        """
        instance = cls()
        if name in instance._skills:
            del instance._skills[name]
            return True
        return False
    
    @classmethod
    def clear(cls) -> None:
        """清空所有注册的技能"""
        instance = cls()
        instance._skills.clear()
    
    @classmethod
    def count(cls) -> int:
        """获取已注册技能数量"""
        instance = cls()
        return len(instance._skills)


# 便捷函数

def get_skill(name: str) -> Type | None:
    """获取技能类（便捷函数）
    
    示例：
        >>> skill_class = get_skill("hdf5_export")
        >>> skill = skill_class()
        >>> result = skill.run(config)
    """
    return SkillRegistry.get(name)


def list_skills(category: str | None = None) -> list[str]:
    """列出所有技能（便捷函数）
    
    示例：
        >>> all_skills = list_skills()
        >>> tools = list_skills(category="tool")
        >>> analysis = list_skills(category="poweranalysis")
    """
    return SkillRegistry.list_skills(category)


def skill_exists(name: str) -> bool:
    """检查技能是否存在"""
    return SkillRegistry.get(name) is not None


# 装饰器版本

def register_skill(
    name: str,
    category: str,
    description: str = "",
    version: str = "2.0.0",
    author: str = "",
    tags: list[str] | None = None,
):
    """技能注册装饰器
    
    示例：
        @register_skill(
            name="hdf5_export",
            category="tool",
            description="导出HDF5格式数据",
        )
        class HDF5ExportTool(ToolBase):
            pass
    """
    def decorator(cls):
        SkillRegistry.register(
            name=name,
            category=category,
            skill_class=cls,
            description=description,
            version=version,
            author=author,
            tags=tags,
        )
        # 保留原类
        cls._skill_name = name
        cls._skill_category = category
        return cls
    return decorator


__all__ = [
    "SkillRegistry",
    "SkillInfo",
    "get_skill",
    "list_skills",
    "skill_exists",
    "register_skill",
]
