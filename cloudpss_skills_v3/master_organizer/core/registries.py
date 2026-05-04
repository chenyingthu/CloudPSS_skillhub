"""
具体注册表实现 - Phase 3

实现 ServerRegistry, CaseRegistry, TaskRegistry, ResultRegistry
"""

from dataclasses import asdict
from typing import Optional
from .registry_base import RegistryBase
from .models import Server, Case, Task, Result, Variant


class ServerRegistry(RegistryBase[Server]):
    @property
    def registry_name(self) -> str:
        return "servers"

    @property
    def entity_type(self) -> str:
        return "server"

    def _serialize_data(self) -> dict:
        return {k: asdict(v) for k, v in self._data.items()}

    def _deserialize_data(self, data: dict) -> dict:
        return {k: Server(**v) for k, v in data.get(self.registry_name, {}).items()}


class CaseRegistry(RegistryBase[Case]):
    @property
    def registry_name(self) -> str:
        return "cases"

    @property
    def entity_type(self) -> str:
        return "case"

    def _serialize_data(self) -> dict:
        return {k: asdict(v) for k, v in self._data.items()}

    def _deserialize_data(self, data: dict) -> dict:
        return {k: Case(**v) for k, v in data.get(self.registry_name, {}).items()}


class TaskRegistry(RegistryBase[Task]):
    @property
    def registry_name(self) -> str:
        return "tasks"

    @property
    def entity_type(self) -> str:
        return "task"

    def _serialize_data(self) -> dict:
        return {k: asdict(v) for k, v in self._data.items()}

    def _deserialize_data(self, data: dict) -> dict:
        return {k: Task(**v) for k, v in data.get(self.registry_name, {}).items()}

    def filter_by(self, **kwargs) -> list[tuple[str, Task]]:
        """Filter tasks by criteria (case_id, status, type)."""
        results = list(self._data.items())
        for key, value in kwargs.items():
            if value:
                results = [(k, v) for k, v in results if getattr(v, key, None) == value]
        return results


class ResultRegistry(RegistryBase[Result]):
    @property
    def registry_name(self) -> str:
        return "results"

    @property
    def entity_type(self) -> str:
        return "result"

    def _serialize_data(self) -> dict:
        return {k: asdict(v) for k, v in self._data.items()}

    def _deserialize_data(self, data: dict) -> dict:
        return {k: Result(**v) for k, v in data.get(self.registry_name, {}).items()}

    def filter_by(self, **kwargs) -> list[tuple[str, Result]]:
        """Filter results by criteria (task_id, case_id, status)."""
        results = list(self._data.items())
        for key, value in kwargs.items():
            if value:
                results = [(k, v) for k, v in results if getattr(v, key, None) == value]
        return results


class VariantRegistry(RegistryBase[Variant]):
    """变体注册表"""

    @property
    def registry_name(self) -> str:
        return "variants"

    @property
    def entity_type(self) -> str:
        return "variant"

    def _serialize_data(self) -> dict:
        return {k: asdict(v) for k, v in self._data.items()}

    def _deserialize_data(self, data: dict) -> dict:
        return {k: Variant(**v) for k, v in data.get(self.registry_name, {}).items()}

    def get_by_case(self, case_id: str) -> list[tuple[str, Variant]]:
        """获取指定算例的所有变体"""
        return [(k, v) for k, v in self._data.items() if v.case_id == case_id]


__all__ = ["ServerRegistry", "CaseRegistry", "TaskRegistry", "ResultRegistry", "VariantRegistry"]
