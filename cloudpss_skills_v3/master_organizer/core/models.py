"""
数据模型定义 - 收纳大师计划

定义 Server, Case, Task, Result, Variant 五大核心实体的数据模型。
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any


class EntityStatus(Enum):
    """实体状态枚举"""
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class TaskStatus(Enum):
    """任务状态枚举"""
    CREATED = "created"
    SUBMITTED = "submitted"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Server:
    """服务器实体"""
    id: str
    name: str
    url: str
    auth: Dict[str, str] = field(default_factory=dict)
    status: str = "active"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_used: Optional[str] = None
    is_default: bool = False
    capabilities: List[str] = field(default_factory=list)


@dataclass
class Case:
    """算例实体"""
    id: str
    name: str
    description: str = ""
    rid: str = ""  # CloudPSS 资源ID
    server_id: str = ""
    status: str = "draft"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: List[str] = field(default_factory=list)
    task_count: int = 0
    last_task_id: Optional[str] = None


@dataclass
class Variant:
    """变体实体"""
    id: str
    case_id: str
    name: str
    description: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    parent_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Task:
    """任务实体"""
    id: str
    name: str
    case_id: str
    variant_id: Optional[str] = None
    task_type: str = ""  # powerflow/emt/stability
    job_id: Optional[str] = None
    server_id: str = ""
    status: str = "created"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    submitted_at: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result_id: Optional[str] = None
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Result:
    """结果实体"""
    id: str
    name: str
    task_id: str
    case_id: str
    result_format: str = "json"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    size_bytes: int = 0
    files: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
