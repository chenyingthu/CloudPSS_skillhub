"""
任务状态存储 (Task Store)

提供异步任务的状态管理和持久化存储。
支持内存存储和文件存储两种模式。
"""

import os
import json
import logging
from enum import Enum
from typing import Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from threading import Lock

logger = logging.getLogger(__name__)


class TaskStatus(str, Enum):
    """任务状态枚举"""
    PENDING = "pending"      # 等待执行
    RUNNING = "running"      # 执行中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"        # 失败
    CANCELLED = "cancelled"  # 已取消


@dataclass
class TaskInfo:
    """任务信息数据结构"""
    task_id: str
    case_name: str
    model_rid: str
    task_type: str  # powerflow, emt, etc.
    status: TaskStatus
    progress: int  # 0-100
    message: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    result_data: Optional[dict] = None
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        """转换为字典"""
        data = asdict(self)
        # 转换枚举和日期为字符串
        data['status'] = self.status.value
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        if self.completed_at:
            data['completed_at'] = self.completed_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "TaskInfo":
        """从字典创建"""
        data['status'] = TaskStatus(data['status'])
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        if data.get('completed_at'):
            data['completed_at'] = datetime.fromisoformat(data['completed_at'])
        return cls(**data)


class TaskStore:
    """任务存储管理器

    管理所有仿真任务的状态，支持内存和文件两种存储模式。
    使用单例模式确保全局只有一个存储实例。
    """

    _instance: Optional["TaskStore"] = None
    _lock: Lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, storage_path: Optional[str] = None):
        if self._initialized:
            return

        self._initialized = True
        self._memory_store: dict[str, TaskInfo] = {}
        self._store_lock = Lock()

        # 设置存储路径
        if storage_path:
            self._storage_path = Path(storage_path)
        else:
            workspace = os.getenv("CLOUDPSS_WORKSPACE", "~/.cloudpss/workspace")
            self._storage_path = Path(workspace).expanduser() / "tasks"

        self._storage_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"TaskStore 初始化完成，存储路径: {self._storage_path}")

    def create_task(self, task_id: str, case_name: str, model_rid: str,
                    task_type: str = "powerflow") -> TaskInfo:
        """创建新任务"""
        now = datetime.now()
        task_info = TaskInfo(
            task_id=task_id,
            case_name=case_name,
            model_rid=model_rid,
            task_type=task_type,
            status=TaskStatus.PENDING,
            progress=0,
            message="任务已创建，等待执行",
            created_at=now,
            updated_at=now
        )

        with self._store_lock:
            self._memory_store[task_id] = task_info

        self._persist_task(task_info)
        logger.info(f"任务创建: {task_id}, 案例: {case_name}")
        return task_info

    def update_task_status(self, task_id: str, status: TaskStatus,
                          progress: Optional[int] = None,
                          message: Optional[str] = None,
                          result_data: Optional[dict] = None,
                          error_message: Optional[str] = None) -> Optional[TaskInfo]:
        """更新任务状态"""
        with self._store_lock:
            task = self._memory_store.get(task_id)
            if not task:
                logger.warning(f"更新状态失败: 任务不存在 {task_id}")
                return None

            task.status = status
            task.updated_at = datetime.now()

            if progress is not None:
                task.progress = progress
            if message is not None:
                task.message = message
            if result_data is not None:
                task.result_data = result_data
            if error_message is not None:
                task.error_message = error_message

            if status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                task.completed_at = datetime.now()
                task.progress = 100 if status == TaskStatus.COMPLETED else task.progress

        self._persist_task(task)
        logger.debug(f"任务状态更新: {task_id} -> {status.value}")
        return task

    def get_task(self, task_id: str) -> Optional[TaskInfo]:
        """获取任务信息"""
        # 先检查内存
        with self._store_lock:
            if task_id in self._memory_store:
                return self._memory_store[task_id]

        # 从文件加载
        return self._load_task_from_file(task_id)

    def list_tasks(self, status: Optional[TaskStatus] = None,
                   limit: int = 100) -> list[TaskInfo]:
        """列出任务"""
        with self._store_lock:
            tasks = list(self._memory_store.values())

        # 按时间排序（最新的在前）
        tasks.sort(key=lambda t: t.created_at, reverse=True)

        if status:
            tasks = [t for t in tasks if t.status == status]

        return tasks[:limit]

    def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        with self._store_lock:
            if task_id in self._memory_store:
                del self._memory_store[task_id]

        # 删除文件
        file_path = self._get_task_file_path(task_id)
        if file_path.exists():
            file_path.unlink()
            logger.info(f"任务删除: {task_id}")
            return True
        return False

    def _get_task_file_path(self, task_id: str) -> Path:
        """获取任务文件路径"""
        return self._storage_path / f"{task_id}.json"

    def _persist_task(self, task: TaskInfo):
        """持久化任务到文件"""
        try:
            file_path = self._get_task_file_path(task.task_id)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(task.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"任务持久化失败 {task.task_id}: {e}")

    def _load_task_from_file(self, task_id: str) -> Optional[TaskInfo]:
        """从文件加载任务"""
        try:
            file_path = self._get_task_file_path(task_id)
            if not file_path.exists():
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            task = TaskInfo.from_dict(data)

            # 加载到内存
            with self._store_lock:
                self._memory_store[task_id] = task

            return task
        except Exception as e:
            logger.error(f"加载任务失败 {task_id}: {e}")
            return None

    def load_all_tasks(self):
        """加载所有持久化的任务"""
        try:
            for file_path in self._storage_path.glob("*.json"):
                task_id = file_path.stem
                self._load_task_from_file(task_id)
            logger.info(f"已加载 {len(self._memory_store)} 个历史任务")
        except Exception as e:
            logger.error(f"加载历史任务失败: {e}")


# 全局 TaskStore 实例
_task_store: Optional[TaskStore] = None


def get_task_store(storage_path: Optional[str] = None) -> TaskStore:
    """获取全局 TaskStore 实例"""
    global _task_store
    if _task_store is None:
        _task_store = TaskStore(storage_path)
        _task_store.load_all_tasks()
    return _task_store


def reset_task_store():
    """重置 TaskStore（主要用于测试）"""
    global _task_store
    TaskStore._instance = None
    _task_store = None
