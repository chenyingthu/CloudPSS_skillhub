"""
注册表基类 - 收纳大师计划核心组件

提供统一的注册表管理接口，支持 CRUD 操作、索引管理和数据验证。
所有具体注册表（CaseRegistry, TaskRegistry 等）继承此类。
"""

import re
import os
import tempfile
from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Generic, Optional, TypeVar

import yaml

T = TypeVar('T')


@dataclass
class RegistryEntry:
    """注册表条目基类"""
    id: str
    name: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


class RegistryBase(ABC, Generic[T]):
    """
    注册表基类

    所有实体注册表的抽象基类，提供：
    - 统一的 CRUD 接口
    - 索引管理
    - 数据验证
    - 缓存机制

    Attributes:
        registry_name: 注册表名称（用于文件名）
        entity_type: 实体类型标识
    """

    def __init__(
        self,
        registry_dir: Optional[Path] = None,
        auto_save: bool = True
    ):
        """
        初始化注册表

        Args:
            registry_dir: 注册表目录路径，默认从 PathManager 获取
            auto_save: 是否自动保存更改
        """
        if registry_dir:
            self._registry_dir = Path(registry_dir)
        else:
            from .path_manager import get_path_manager
            self._registry_dir = get_path_manager().registry_dir

        self._auto_save = auto_save
        self._data: dict[str, T] = {}
        self._indices: dict[str, dict[str, list[str]]] = {}

        self._load()

    @contextmanager
    def _file_lock(self):
        """Best-effort local lock around registry writes."""
        lock_path = self._registry_dir / f"{self.registry_name}.lock"
        self._registry_dir.mkdir(parents=True, exist_ok=True)
        with open(lock_path, "w", encoding="utf-8") as lock_file:
            try:
                import fcntl

                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            except (ImportError, OSError):
                pass
            try:
                yield
            finally:
                try:
                    import fcntl

                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
                except (ImportError, OSError):
                    pass

    @property
    @abstractmethod
    def registry_name(self) -> str:
        """注册表名称（文件名，不含扩展名）"""
        pass

    @property
    @abstractmethod
    def entity_type(self) -> str:
        """实体类型标识"""
        pass

    @property
    def _registry_path(self) -> Path:
        """注册表文件路径"""
        return self._registry_dir / f"{self.registry_name}.yaml"

    def _load(self):
        """从文件加载注册表数据"""
        if self._registry_path.exists():
            try:
                with open(self._registry_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data:
                        self._data = self._deserialize_data(data)
                        self._indices = data.get('indices', {})
            except Exception as e:
                raise ValueError(f"Failed to load registry {self.registry_name}: {e}")

    def _save(self):
        """保存注册表数据到文件"""
        data = {
            'api_version': 'v1.0',
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'count': len(self._data)
            },
            self.registry_name: self._serialize_data(),
            'indices': self._indices
        }

        self._registry_dir.mkdir(parents=True, exist_ok=True)
        with self._file_lock():
            fd, temp_name = tempfile.mkstemp(
                prefix=f".{self.registry_name}.",
                suffix=".tmp",
                dir=self._registry_dir,
                text=True,
            )
            temp_path = Path(temp_name)
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    yaml.dump(data, f, allow_unicode=True, sort_keys=False)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(temp_path, self._registry_path)
            finally:
                if temp_path.exists():
                    temp_path.unlink()

    @abstractmethod
    def _serialize_data(self) -> dict:
        """序列化数据为字典"""
        pass

    @abstractmethod
    def _deserialize_data(self, data: dict) -> dict[str, T]:
        """反序列化字典为数据"""
        pass

    def _validate_id(self, entity_id: str) -> bool:
        """验证ID格式"""
        from .id_generator import validate_id
        return validate_id(entity_id)

    def _update_indices(self, entity_id: str, entry: T, remove: bool = False):
        """更新索引"""
        pass  # 子类可重写

    def _touch(self):
        """标记更改，自动保存"""
        if self._auto_save:
            self._save()

    # CRUD 操作

    def create(self, entity_id: str, entry: T) -> bool:
        """
        创建条目

        Args:
            entity_id: 实体ID
            entry: 条目数据

        Returns:
            是否成功创建（False 表示ID已存在）
        """
        if entity_id in self._data:
            return False

        if not self._validate_id(entity_id):
            raise ValueError(f"Invalid entity ID: {entity_id}")

        self._data[entity_id] = entry
        self._update_indices(entity_id, entry)
        self._touch()
        return True

    def get(self, entity_id: str) -> Optional[T]:
        """
        获取条目

        Args:
            entity_id: 实体ID

        Returns:
            条目数据，如果不存在则返回 None
        """
        return self._data.get(entity_id)

    def update(self, entity_id: str, updates: dict) -> bool:
        """
        更新条目

        Args:
            entity_id: 实体ID
            updates: 更新字段

        Returns:
            是否成功更新
        """
        if entity_id not in self._data:
            return False

        entry = self._data[entity_id]
        # 更新字段
        for key, value in updates.items():
            if hasattr(entry, key):
                setattr(entry, key, value)

        # 更新时间戳
        if hasattr(entry, 'updated_at'):
            entry.updated_at = datetime.now().isoformat()

        self._update_indices(entity_id, entry)
        self._touch()
        return True

    def delete(self, entity_id: str) -> bool:
        """
        删除条目

        Args:
            entity_id: 实体ID

        Returns:
            是否成功删除
        """
        if entity_id not in self._data:
            return False

        entry = self._data.pop(entity_id)
        self._update_indices(entity_id, entry, remove=True)
        self._touch()
        return True

    def exists(self, entity_id: str) -> bool:
        """
        检查条目是否存在

        Args:
            entity_id: 实体ID

        Returns:
            是否存在
        """
        return entity_id in self._data

    def list_all(self) -> list[tuple[str, T]]:
        """
        列出所有条目

        Returns:
            (entity_id, entry) 列表
        """
        return list(self._data.items())

    def list_paginated(
        self,
        limit: int = 50,
        offset: int = 0,
        sort_by: str | None = None,
        sort_desc: bool = True,
    ) -> tuple[list[tuple[str, T]], int]:
        """列出条目（分页优化版本）

        Args:
            limit: 每页数量
            offset: 偏移量
            sort_by: 排序字段（None表示按ID）
            sort_desc: 是否降序

        Returns:
            (条目列表, 总数)
        """
        items = list(self._data.items())
        total = len(items)

        # 排序
        if sort_by:
            items.sort(
                key=lambda x: getattr(x[1], sort_by, x[0]),
                reverse=sort_desc,
            )
        elif sort_desc:
            # 默认按ID降序（最新的在前）
            items.sort(key=lambda x: x[0], reverse=True)

        # 分页
        paginated = items[offset:offset + limit]

        return paginated, total

    def count(self) -> int:
        """
        获取条目数量

        Returns:
            条目总数
        """
        return len(self._data)

    # 索引查询

    def query_by_index(self, index_name: str, key: str) -> list[str]:
        """
        通过索引查询

        Args:
            index_name: 索引名称
            key: 索引键

        Returns:
            匹配的实体ID列表
        """
        return self._indices.get(index_name, {}).get(key, [])

    # 批量操作

    def bulk_create(self, entries: dict[str, T]) -> int:
        """
        批量创建条目

        Args:
            entries: {entity_id: entry} 字典

        Returns:
            成功创建的数量
        """
        count = 0
        for entity_id, entry in entries.items():
            if self.create(entity_id, entry):
                count += 1
        return count

    def bulk_delete(self, entity_ids: list[str]) -> int:
        """
        批量删除条目

        Args:
            entity_ids: 实体ID列表

        Returns:
            成功删除的数量
        """
        count = 0
        for entity_id in entity_ids:
            if self.delete(entity_id):
                count += 1
        return count

    # 工具方法

    def search(self, pattern: str, field: Optional[str] = None) -> list[tuple[str, T]]:
        """
        搜索条目

        Args:
            pattern: 搜索模式（正则表达式）
            field: 指定字段，None 则搜索所有字段

        Returns:
            匹配的 (entity_id, entry) 列表
        """
        regex = re.compile(pattern, re.IGNORECASE)
        results = []

        for entity_id, entry in self._data.items():
            if field:
                value = getattr(entry, field, None)
                if value and regex.search(str(value)):
                    results.append((entity_id, entry))
            else:
                # 搜索所有字段
                entry_dict = entry.__dict__ if hasattr(entry, '__dict__') else {}
                for value in entry_dict.values():
                    if regex.search(str(value)):
                        results.append((entity_id, entry))
                        break

        return results

    def filter_by(self, **kwargs) -> list[tuple[str, T]]:
        """
        按条件过滤

        Args:
            **kwargs: 字段-值匹配条件

        Returns:
            匹配的 (entity_id, entry) 列表
        """
        results = []
        for entity_id, entry in self._data.items():
            match = True
            for key, value in kwargs.items():
                if getattr(entry, key, None) != value:
                    match = False
                    break
            if match:
                results.append((entity_id, entry))
        return results

    def save(self):
        """手动保存注册表"""
        self._save()

    def reload(self):
        """重新加载注册表"""
        self._load()
