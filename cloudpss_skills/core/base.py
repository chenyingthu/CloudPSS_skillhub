"""
CloudPSS Skill System - Core Module

基础模块，定义技能系统的核心类和接口。
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional, List, Dict
from datetime import datetime
import enum


class SkillStatus(enum.Enum):
    """技能执行状态"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Artifact:
    """输出产物"""
    type: str  # csv, json, yaml, png, log, etc.
    path: str
    size: int = 0
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LogEntry:
    """日志条目"""
    timestamp: datetime
    level: str
    message: str
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SkillResult:
    """技能执行结果"""
    skill_name: str
    status: SkillStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    data: Dict[str, Any] = field(default_factory=dict)
    artifacts: List[Artifact] = field(default_factory=list)
    logs: List[LogEntry] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        """是否成功"""
        return self.status == SkillStatus.SUCCESS

    @property
    def duration(self) -> float:
        """执行时长（秒）"""
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "skill_name": self.skill_name,
            "status": self.status.value,
            "success": self.success,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "data": self.data,
            "artifacts": [
                {
                    "type": a.type,
                    "path": a.path,
                    "size": a.size,
                    "description": a.description,
                }
                for a in self.artifacts
            ],
            "metrics": self.metrics,
            "error": self.error,
        }


@dataclass
class ValidationResult:
    """配置验证结果"""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_error(self, message: str):
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str):
        self.warnings.append(message)


class SkillBase(ABC):
    """
    技能基类

    所有技能必须继承此类并实现抽象方法。
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """技能唯一标识名"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """技能描述"""
        pass

    @property
    def version(self) -> str:
        """技能版本"""
        return "1.0.0"

    @property
    def author(self) -> str:
        """作者"""
        return "CloudPSS"

    @property
    def config_schema(self) -> Dict[str, Any]:
        """
        配置JSON Schema

        返回JSON Schema字典，用于验证配置。
        子类可覆盖以提供更严格的验证。
        """
        return {
            "type": "object",
            "required": ["skill"],
            "properties": {
                "skill": {"type": "string"},
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "token_file": {"type": "string"},
                    },
                },
                "model": {
                    "type": "object",
                    "properties": {
                        "rid": {"type": "string"},
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"type": "string"},
                        "path": {"type": "string"},
                        "prefix": {"type": "string"},
                    },
                },
            },
        }

    @abstractmethod
    def run(self, config: Dict[str, Any]) -> SkillResult:
        """
        执行技能

        Args:
            config: 配置字典

        Returns:
            SkillResult: 执行结果
        """
        pass

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        """
        验证配置

        Args:
            config: 配置字典

        Returns:
            ValidationResult: 验证结果
        """
        result = ValidationResult(valid=True)

        # 基础验证
        if not isinstance(config, dict):
            result.add_error("配置必须是字典类型")
            return result

        if "skill" not in config:
            result.add_error("配置必须包含 'skill' 字段")
            return result

        if config.get("skill") != self.name:
            result.add_error(f"技能名称不匹配: 期望 '{self.name}', 实际 '{config.get('skill')}'")
            return result

        # 注意: 不再强制检查model.rid，由子类自行决定
        # 子类可以覆盖validate()添加特定的验证逻辑

        return result

    def get_default_config(self) -> Dict[str, Any]:
        """
        获取默认配置

        Returns:
            Dict: 默认配置字典
        """
        return {
            "skill": self.name,
            "auth": {
                "token_file": ".cloudpss_token",
            },
            "model": {
                "source": "cloud",
            },
            "output": {
                "format": "csv",
                "path": "./results/",
                "prefix": "output",
            },
        }

    def describe(self) -> Dict[str, Any]:
        """
        获取技能描述信息

        Returns:
            Dict: 技能描述字典
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "schema": self.config_schema,
            "defaults": self.get_default_config(),
        }

    def __str__(self) -> str:
        return f"{self.name} (v{self.version}): {self.description}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"
