"""
元数据注册表

提供组件元数据的缓存、查询和管理功能
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field

from .models import ComponentMetadata

logger = logging.getLogger(__name__)


@dataclass
class RegistryStats:
    """注册表统计信息"""
    total_components: int = 0
    categories: List[str] = field(default_factory=list)
    source_files: List[str] = field(default_factory=list)
    last_updated: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'total_components': self.total_components,
            'categories': self.categories,
            'source_files': self.source_files,
            'last_updated': self.last_updated
        }


class ComponentMetadataRegistry:
    """
    组件元数据注册表

    提供组件元数据的集中管理和查询功能。
    支持从JSON文件加载和运行时注册。

    Attributes:
        _components: 组件ID到元数据的映射
        _categories: 类别到组件ID列表的映射
        _sources: 源文件路径列表
    """

    def __init__(self):
        self._components: Dict[str, ComponentMetadata] = {}
        self._categories: Dict[str, List[str]] = {}
        self._sources: List[str] = []
        self._initialized = False

    def register(self, metadata: ComponentMetadata) -> None:
        """
        注册组件元数据

        Args:
            metadata: 组件元数据对象
        """
        self._components[metadata.component_id] = metadata

        # 更新类别索引
        if metadata.category:
            if metadata.category not in self._categories:
                self._categories[metadata.category] = []
            if metadata.component_id not in self._categories[metadata.category]:
                self._categories[metadata.category].append(metadata.component_id)

        logger.debug(f"已注册组件: {metadata.component_id}")

    def unregister(self, component_id: str) -> bool:
        """
        注销组件元数据

        Args:
            component_id: 组件ID

        Returns:
            是否成功注销
        """
        if component_id not in self._components:
            return False

        metadata = self._components.pop(component_id)

        # 更新类别索引
        if metadata.category and metadata.category in self._categories:
            if component_id in self._categories[metadata.category]:
                self._categories[metadata.category].remove(component_id)

        logger.debug(f"已注销组件: {component_id}")
        return True

    def get_component(self, component_id: str) -> Optional[ComponentMetadata]:
        """
        获取组件元数据

        Args:
            component_id: 组件ID

        Returns:
            组件元数据，如果不存在则返回None
        """
        return self._components.get(component_id)

    def has_component(self, component_id: str) -> bool:
        """
        检查组件是否已注册

        Args:
            component_id: 组件ID

        Returns:
            是否已注册
        """
        return component_id in self._components

    def list_components(self, category: Optional[str] = None) -> List[str]:
        """
        列出所有组件ID

        Args:
            category: 可选的类别过滤

        Returns:
            组件ID列表
        """
        if category:
            return self._categories.get(category, [])
        return list(self._components.keys())

    def get_components_by_category(self, category: str) -> List[ComponentMetadata]:
        """
        获取指定类别的所有组件

        Args:
            category: 类别名称

        Returns:
            组件元数据列表
        """
        component_ids = self._categories.get(category, [])
        return [self._components[pid] for pid in component_ids if pid in self._components]

    def search(self, query: str) -> List[ComponentMetadata]:
        """
        搜索组件

        在组件ID、名称和描述中搜索匹配项

        Args:
            query: 搜索关键词

        Returns:
            匹配的组件元数据列表
        """
        query = query.lower()
        results = []

        for metadata in self._components.values():
            if (query in metadata.component_id.lower() or
                query in metadata.name.lower() or
                query in metadata.description.lower()):
                results.append(metadata)

        return results

    def load_from_file(self, filepath: Union[str, Path]) -> int:
        """
        从JSON文件加载元数据

        Args:
            filepath: JSON文件路径

        Returns:
            加载的组件数量

        Raises:
            FileNotFoundError: 文件不存在
            json.JSONDecodeError: JSON格式错误
        """
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"元数据文件不存在: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        count = 0

        # 支持单个组件或组件列表
        if isinstance(data, dict) and 'component_id' in data:
            # 单个组件
            metadata = ComponentMetadata.from_dict(data)
            self.register(metadata)
            count = 1
        elif isinstance(data, list):
            # 组件列表
            for item in data:
                metadata = ComponentMetadata.from_dict(item)
                self.register(metadata)
                count += 1
        elif isinstance(data, dict) and 'components' in data:
            # 包含components字段的对象
            for item in data['components']:
                metadata = ComponentMetadata.from_dict(item)
                self.register(metadata)
                count += 1

        self._sources.append(str(filepath))
        logger.info(f"从 {filepath} 加载了 {count} 个组件")
        return count

    def load_from_directory(self, directory: Union[str, Path]) -> int:
        """
        从目录加载所有JSON元数据文件

        Args:
            directory: 目录路径

        Returns:
            加载的组件总数
        """
        directory = Path(directory)

        if not directory.exists():
            logger.warning(f"目录不存在: {directory}")
            return 0

        count = 0
        for json_file in directory.glob('*.json'):
            try:
                count += self.load_from_file(json_file)
            except Exception as e:
                logger.error(f"加载 {json_file} 失败: {e}")

        logger.info(f"从目录 {directory} 共加载 {count} 个组件")
        return count

    def save_to_file(self, filepath: Union[str, Path]) -> None:
        """
        保存所有元数据到JSON文件

        Args:
            filepath: 输出文件路径
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        data = {
            'components': [m.to_dict() for m in self._components.values()]
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"已保存 {len(self._components)} 个组件到 {filepath}")

    def export_component(self, component_id: str, filepath: Union[str, Path]) -> bool:
        """
        导出单个组件到JSON文件

        Args:
            component_id: 组件ID
            filepath: 输出文件路径

        Returns:
            是否成功导出
        """
        metadata = self.get_component(component_id)
        if not metadata:
            return False

        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata.to_dict(), f, ensure_ascii=False, indent=2)

        return True

    def get_stats(self) -> RegistryStats:
        """
        获取注册表统计信息

        Returns:
            统计信息对象
        """
        from datetime import datetime
        return RegistryStats(
            total_components=len(self._components),
            categories=list(self._categories.keys()),
            source_files=self._sources.copy(),
            last_updated=datetime.now().isoformat()
        )

    def clear(self) -> None:
        """清空注册表"""
        self._components.clear()
        self._categories.clear()
        self._sources.clear()
        self._initialized = False
        logger.debug("注册表已清空")

    def __len__(self) -> int:
        """返回注册的组件数量"""
        return len(self._components)

    def __contains__(self, component_id: str) -> bool:
        """检查组件是否已注册"""
        return component_id in self._components


# 全局注册表实例
_registry: Optional[ComponentMetadataRegistry] = None


def get_registry() -> ComponentMetadataRegistry:
    """
    获取全局注册表实例

    Returns:
        全局注册表实例（单例模式）
    """
    global _registry
    if _registry is None:
        _registry = ComponentMetadataRegistry()
    return _registry


def reset_registry() -> None:
    """重置全局注册表（主要用于测试）"""
    global _registry
    _registry = None
    logger.debug("全局注册表已重置")
