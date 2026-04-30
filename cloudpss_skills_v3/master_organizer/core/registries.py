"""
具体注册表实现 - Phase 3

实现 ServerRegistry, CaseRegistry, TaskRegistry, ResultRegistry
"""

from dataclasses import asdict
from typing import Optional
from .registry_base import RegistryBase
from .models import Server, Case, Task, Result


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


__all__ = ["ServerRegistry", "CaseRegistry", "TaskRegistry", "ResultRegistry"]
