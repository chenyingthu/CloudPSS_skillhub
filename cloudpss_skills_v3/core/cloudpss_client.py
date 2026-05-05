"""
CloudPSS SDK 客户端封装

提供简化的接口与 CloudPSS 平台交互。
"""

import os
import logging
from typing import Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime

from cloudpss_skills_v3.core.task_store import TaskStatus, get_task_store

logger = logging.getLogger(__name__)


@dataclass
class SimulationResult:
    """仿真结果数据结构"""
    task_id: str
    status: str  # completed, failed, running
    case_name: str
    model_rid: str
    bus_count: int
    branch_count: int
    voltage_min: float
    voltage_max: float
    iterations: int
    compute_time: float  # 秒
    created_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    raw_data: Optional[dict] = None


class CloudPSSClient:
    """CloudPSS 客户端

    封装 CloudPSS SDK，提供简化接口。
    当前为占位符实现，后续接入真实 SDK。
    """

    def __init__(self, token: Optional[str] = None):
        """初始化客户端

        Args:
            token: CloudPSS API Token，默认从环境变量读取
        """
        self.token = token or os.getenv("CLOUDPSS_TOKEN") or self._load_token_from_file()
        self.base_url = "https://cloudpss.net/api"
        logger.info("CloudPSSClient 初始化完成")

    def _load_token_from_file(self) -> Optional[str]:
        """从文件加载 Token"""
        token_file = os.path.expanduser("~/.cloudpss/token")
        try:
            with open(token_file, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            logger.warning(f"Token 文件不存在: {token_file}")
            return None

    async def create_case(self, name: str, model_rid: str) -> str:
        """创建仿真案例

        Args:
            name: 案例名称
            model_rid: 模型 RID

        Returns:
            case_id: 创建的案例 ID
        """
        logger.info(f"创建案例: {name}, 模型: {model_rid}")

        # TODO: 接入真实的 CloudPSS SDK
        # 目前返回模拟数据
        import asyncio
        await asyncio.sleep(0.1)  # 模拟网络延迟

        case_id = f"case-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        logger.info(f"案例创建成功: {case_id}")
        return case_id

    async def submit_powerflow(self, case_id: str, options: Optional[dict] = None) -> str:
        """提交潮流计算任务

        Args:
            case_id: 案例 ID
            options: 计算选项

        Returns:
            task_id: 任务 ID
        """
        logger.info(f"提交潮流计算: case={case_id}")

        # TODO: 接入真实的 CloudPSS SDK
        import asyncio
        await asyncio.sleep(0.1)

        task_id = f"task-pf-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        logger.info(f"任务提交成功: {task_id}")
        return task_id

    async def submit_emt(self, case_id: str, options: Optional[dict] = None) -> str:
        """提交暂态仿真任务

        Args:
            case_id: 案例 ID
            options: 仿真选项，包含 duration, fault_config 等

        Returns:
            task_id: 任务 ID
        """
        logger.info(f"提交暂态仿真: case={case_id}, options={options}")

        # TODO: 接入真实的 CloudPSS SDK
        import asyncio
        await asyncio.sleep(0.1)

        task_id = f"task-emt-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        logger.info(f"暂态仿真任务提交成功: {task_id}")
        return task_id

    async def get_task_status(self, task_id: str) -> dict:
        """获取任务状态

        Args:
            task_id: 任务 ID

        Returns:
            任务状态信息
        """
        # TODO: 接入真实的 CloudPSS SDK
        return {
            "task_id": task_id,
            "status": "completed",
            "progress": 100,
            "message": "计算完成"
        }

    async def get_powerflow_result(self, task_id: str) -> SimulationResult:
        """获取潮流计算结果

        Args:
            task_id: 任务 ID

        Returns:
            SimulationResult: 仿真结果
        """
        logger.info(f"获取结果: {task_id}")

        # TODO: 接入真实的 CloudPSS SDK
        # 目前返回模拟的 IEEE39 结果
        import asyncio
        await asyncio.sleep(0.2)  # 模拟网络延迟

        return SimulationResult(
            task_id=task_id,
            status="completed",
            case_name="IEEE39",
            model_rid="model/chenying/IEEE39",
            bus_count=39,
            branch_count=46,
            voltage_min=0.98,
            voltage_max=1.05,
            iterations=4,
            compute_time=2.3,
            created_at=datetime.now(),
            completed_at=datetime.now(),
            raw_data={
                "buses": [{"id": i, "v": 1.0 + (i % 5) * 0.01} for i in range(39)],
                "branches": [{"from": 0, "to": 1, "p": 100.5} for _ in range(46)]
            }
        )

    async def wait_for_completion(self, task_id: str, timeout: float = 300.0) -> SimulationResult:
        """等待任务完成

        Args:
            task_id: 任务 ID
            timeout: 超时时间（秒）

        Returns:
            SimulationResult: 仿真结果

        Raises:
            TimeoutError: 超时
            RuntimeError: 任务失败
        """
        logger.info(f"等待任务完成: {task_id}, timeout={timeout}s")

        import asyncio
        start_time = asyncio.get_event_loop().time()

        while True:
            status = await self.get_task_status(task_id)

            if status["status"] == "completed":
                return await self.get_powerflow_result(task_id)

            if status["status"] == "failed":
                raise RuntimeError(f"任务失败: {status.get('message', 'Unknown error')}")

            if asyncio.get_event_loop().time() - start_time > timeout:
                raise TimeoutError(f"任务超时: {task_id}")

            await asyncio.sleep(1.0)  # 每秒轮询一次


# 全局客户端实例
_client: Optional[CloudPSSClient] = None


def get_client() -> CloudPSSClient:
    """获取全局客户端实例"""
    global _client
    if _client is None:
        _client = CloudPSSClient()
    return _client
