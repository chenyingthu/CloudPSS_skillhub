"""
Skill Metadata - 技能元数据管理

提供技能元数据定义、验证和装饰器。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Type
from functools import wraps


@dataclass
class SkillMetadata:
    """技能元数据容器
    
    存储技能的描述性信息，支持文档生成和技能发现。
    
    属性:
        name: 技能名称（唯一标识）
        category: 类别（tool/poweranalysis）
        description: 简短描述
        long_description: 详细描述（支持Markdown）
        version: 版本号
        author: 作者
        email: 联系邮箱
        tags: 标签列表
        input_schema: 输入配置JSON Schema
        output_schema: 输出结果JSON Schema
        example_config: 示例配置
        example_output: 示例输出
        requirements: 依赖项列表
        min_python_version: 最低Python版本
        min_cloudpss_version: 最低CloudPSS SDK版本
        deprecated: 是否已弃用
        deprecation_message: 弃用说明
        experimental: 是否为实验性功能
    """
    name: str
    category: str
    description: str = ""
    long_description: str = ""
    version: str = "2.0.0"
    author: str = ""
    email: str = ""
    tags: list[str] = field(default_factory=list)
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    example_config: dict[str, Any] = field(default_factory=dict)
    example_output: dict[str, Any] = field(default_factory=dict)
    requirements: list[str] = field(default_factory=list)
    min_python_version: str = "3.8"
    min_cloudpss_version: str = ""
    deprecated: bool = False
    deprecation_message: str = ""
    experimental: bool = False
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "long_description": self.long_description,
            "version": self.version,
            "author": self.author,
            "email": self.email,
            "tags": self.tags,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "example_config": self.example_config,
            "example_output": self.example_output,
            "requirements": self.requirements,
            "min_python_version": self.min_python_version,
            "min_cloudpss_version": self.min_cloudpss_version,
            "deprecated": self.deprecated,
            "deprecation_message": self.deprecation_message,
            "experimental": self.experimental,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SkillMetadata:
        """从字典创建"""
        return cls(**data)


def skill_metadata(
    name: str,
    category: str,
    description: str = "",
    long_description: str = "",
    version: str = "2.0.0",
    author: str = "",
    email: str = "",
    tags: list[str] | None = None,
    input_schema: dict[str, Any] | None = None,
    output_schema: dict[str, Any] | None = None,
    example_config: dict[str, Any] | None = None,
    example_output: dict[str, Any] | None = None,
    requirements: list[str] | None = None,
    min_python_version: str = "3.8",
    min_cloudpss_version: str = "",
    deprecated: bool = False,
    deprecation_message: str = "",
    experimental: bool = False,
) -> Callable[[Type], Type]:
    """技能元数据装饰器
    
    为技能类添加元数据信息。
    
    示例：
        @skill_metadata(
            name="hdf5_export",
            category="tool",
            description="导出数据到HDF5格式",
            version="2.0.0",
            author="CloudPSS Team",
            tags=["export", "data"],
            input_schema={
                "type": "object",
                "properties": {
                    "source": {"type": "object"},
                    "output": {"type": "object"}
                }
            },
            example_config={
                "source": {"data": {...}},
                "output": {"path": "/data/output.h5"}
            }
        )
        class HDF5ExportTool(ToolBase):
            pass
    """
    def decorator(cls: Type) -> Type:
        metadata = SkillMetadata(
            name=name,
            category=category,
            description=description,
            long_description=long_description,
            version=version,
            author=author,
            email=email,
            tags=tags or [],
            input_schema=input_schema or {},
            output_schema=output_schema or {},
            example_config=example_config or {},
            example_output=example_output or {},
            requirements=requirements or [],
            min_python_version=min_python_version,
            min_cloudpss_version=min_cloudpss_version,
            deprecated=deprecated,
            deprecation_message=deprecation_message,
            experimental=experimental,
        )
        cls._metadata = metadata
        cls._skill_name = name
        cls._skill_category = category
        return cls
    return decorator


# 便捷函数

def get_skill_metadata(skill_class: Type) -> SkillMetadata | None:
    """获取技能元数据"""
    return getattr(skill_class, "_metadata", None)


def has_metadata(skill_class: Type) -> bool:
    """检查是否有元数据"""
    return hasattr(skill_class, "_metadata")


__all__ = [
    "SkillMetadata",
    "skill_metadata",
    "get_skill_metadata",
    "has_metadata",
]
