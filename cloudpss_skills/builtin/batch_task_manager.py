"""
Batch Task Manager

批量任务管理 - 异步批量运行CloudPSS仿真任务

核心功能:
1. 批量提交仿真任务
2. 异步状态轮询
3. 结果自动回收
4. 失败任务重试
5. 进度实时报告

适用于:
- N-1安全分析 (批量故障场景)
- VSI弱母线分析 (批量母线测试)
- 参数扫描 (批量参数组合)
- 故障扫描 (批量故障位置/类型)

参考自: PSA Skills 批量任务管理实现
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"      # 等待提交
    SUBMITTED = "submitted"  # 已提交
    RUNNING = "running"      # 运行中
    COMPLETED = "completed"  # 完成
    FAILED = "failed"        # 失败
    CANCELLED = "cancelled"  # 取消


@dataclass
class BatchTask:
    """批量任务定义"""
    task_id: str                    # 任务唯一ID
    name: str                       # 任务名称
    task_type: str                  # 任务类型 (emt, power_flow, etc.)
    config: Dict[str, Any]          # 任务配置
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None              # 任务结果
    error: Optional[str] = None     # 错误信息
    submitted_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    retry_count: int = 0            # 重试次数
    max_retries: int = 3            # 最大重试次数


@dataclass
class BatchTaskResult:
    """批量任务执行结果"""
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    cancelled_tasks: int = 0
    running_tasks: int = 0
    pending_tasks: int = 0
    results: Dict[str, Any] = field(default_factory=dict)
    errors: Dict[str, str] = field(default_factory=dict)
    execution_time: float = 0.0


@register
class BatchTaskManagerSkill(SkillBase):
    """批量任务管理技能"""

    @property
    def name(self) -> str:
        return "batch_task_manager"

    @property
    def description(self) -> str:
        return "批量任务管理 - 异步批量运行CloudPSS仿真任务，支持状态轮询和结果回收"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["tasks"],
            "properties": {
                "auth": {
                    "type": "object",
                    "properties": {
                        "token_file": {"type": "string", "default": ".cloudpss_token"}
                    }
                },
                "model": {
                    "type": "object",
                    "properties": {
                        "rid": {"type": "string", "description": "模型RID"},
                        "source": {"type": "string", "enum": ["cloud", "local"], "default": "cloud"}
                    }
                },
                "tasks": {
                    "type": "array",
                    "description": "任务列表",
                    "items": {
                        "type": "object",
                        "required": ["name", "type"],
                        "properties": {
                            "name": {"type": "string", "description": "任务名称"},
                            "type": {"type": "string", "enum": ["emt", "power_flow"], "description": "任务类型"},
                            "config": {"type": "object", "description": "任务配置"},
                            "max_retries": {"type": "integer", "default": 3, "description": "最大重试次数"}
                        }
                    }
                },
                "execution": {
                    "type": "object",
                    "properties": {
                        "mode": {"type": "string", "enum": ["sequential", "parallel"], "default": "parallel", "description": "执行模式"},
                        "max_concurrent": {"type": "integer", "default": 5, "description": "最大并发数"},
                        "polling_interval": {"type": "number", "default": 2.0, "description": "状态轮询间隔(s)"},
                        "timeout": {"type": "number", "default": 600.0, "description": "单任务超时(s)"},
                        "enable_retry": {"type": "boolean", "default": True, "description": "启用失败重试"}
                    }
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"type": "string", "enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "batch_tasks"},
                        "save_partial": {"type": "boolean", "default": True, "description": "保存部分结果"}
                    }
                }
            }
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        """验证配置"""
        errors = []

        if "tasks" not in config or not config["tasks"]:
            errors.append("必须指定任务列表")

        if config.get("tasks"):
            for i, task in enumerate(config["tasks"]):
                if "name" not in task:
                    errors.append(f"任务{i+1}必须指定name")
                if "type" not in task:
                    errors.append(f"任务{i+1}必须指定type")

        if errors:
            return ValidationResult(valid=False, errors=errors)

        return ValidationResult(valid=True)

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行批量任务管理"""
        start_time = datetime.now()
        logs = []
        artifacts = []

        try:
            tasks_config = config.get("tasks", [])
            execution_config = config.get("execution", {})

            logger.info(f"批量任务管理开始 - 任务数: {len(tasks_config)}")
            logs.append(LogEntry(level="INFO", message=f"批量任务管理开始，共{len(tasks_config)}个任务"))

            # 创建任务列表
            tasks = []
            for i, task_cfg in enumerate(tasks_config):
                task = BatchTask(
                    task_id=f"task_{i:04d}",
                    name=task_cfg["name"],
                    task_type=task_cfg["type"],
                    config=task_cfg.get("config", {}),
                    max_retries=task_cfg.get("max_retries", 3)
                )
                tasks.append(task)

            # 执行批量任务
            mode = execution_config.get("mode", "parallel")
            if mode == "parallel":
                result = asyncio.run(self._run_parallel(
                    tasks,
                    config,
                    max_concurrent=execution_config.get("max_concurrent", 5),
                    polling_interval=execution_config.get("polling_interval", 2.0),
                    timeout=execution_config.get("timeout", 600.0),
                    enable_retry=execution_config.get("enable_retry", True)
                ))
            else:
                result = asyncio.run(self._run_sequential(
                    tasks,
                    config,
                    polling_interval=execution_config.get("polling_interval", 2.0),
                    timeout=execution_config.get("timeout", 600.0),
                    enable_retry=execution_config.get("enable_retry", True)
                ))

            # 生成输出
            output_config = config.get("output", {})
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "batch_tasks")

            result_data = {
                "total_tasks": result.total_tasks,
                "completed_tasks": result.completed_tasks,
                "failed_tasks": result.failed_tasks,
                "cancelled_tasks": result.cancelled_tasks,
                "execution_time": result.execution_time,
                "tasks_per_second": result.total_tasks / result.execution_time if result.execution_time > 0 else 0,
                "results": result.results,
                "errors": result.errors,
                "task_details": [
                    {
                        "task_id": task.task_id,
                        "name": task.name,
                        "type": task.task_type,
                        "status": task.status.value,
                        "retry_count": task.retry_count,
                        "error": task.error
                    }
                    for task in tasks
                ]
            }

            # 保存JSON结果
            json_path = output_path / f"{prefix}_result.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)

            artifacts.append(Artifact(
                type="json",
                path=str(json_path),
                size=json_path.stat().st_size,
                description="批量任务执行结果"
            ))

            # 保存CSV结果
            csv_path = output_path / f"{prefix}_report.csv"
            self._save_csv_report(tasks, csv_path)

            artifacts.append(Artifact(
                type="csv",
                path=str(csv_path),
                size=csv_path.stat().st_size,
                description="任务执行报告"
            ))

            # 生成Markdown报告
            report_path = output_path / f"{prefix}_report.md"
            self._generate_report(result_data, report_path)

            artifacts.append(Artifact(
                type="markdown",
                path=str(report_path),
                size=report_path.stat().st_size,
                description="批量任务报告"
            ))

            duration = (datetime.now() - start_time).total_seconds()
            logs.append(LogEntry(
                level="INFO",
                message=f"批量任务管理完成 - 成功:{result.completed_tasks}/{result.total_tasks}, 耗时:{duration:.2f}s"
            ))

            return SkillResult(
                status=SkillStatus.SUCCESS if result.failed_tasks == 0 else SkillStatus.FAILED,
                data=result_data,
                artifacts=artifacts,
                logs=logs,
                metrics={
                    "duration": duration,
                    "total_tasks": result.total_tasks,
                    "completed_tasks": result.completed_tasks,
                    "failed_tasks": result.failed_tasks,
                    "tasks_per_second": result.total_tasks / duration if duration > 0 else 0
                }
            )

        except (KeyError, AttributeError, ZeroDivisionError) as e:
            logger.error(f"批量任务管理失败: {e}", exc_info=True)
            return SkillResult(
                status=SkillStatus.FAILED,
                data={},
                artifacts=artifacts,
                logs=logs + [LogEntry(level="ERROR", message=f"管理失败: {str(e)}")],
                metrics={"duration": (datetime.now() - start_time).total_seconds()}
            )

    async def _run_parallel(
        self,
        tasks: List[BatchTask],
        config: Dict[str, Any],
        max_concurrent: int = 5,
        polling_interval: float = 2.0,
        timeout: float = 600.0,
        enable_retry: bool = True
    ) -> BatchTaskResult:
        """并行执行批量任务"""
        result = BatchTaskResult(total_tasks=len(tasks))
        start_time = datetime.now()

        # 使用信号量限制并发
        semaphore = asyncio.Semaphore(max_concurrent)

        async def run_with_semaphore(task: BatchTask):
            async with semaphore:
                await self._execute_task(task, config, polling_interval, timeout, enable_retry)

        # 创建所有任务
        task_coroutines = [run_with_semaphore(task) for task in tasks]

        # 等待所有任务完成
        await asyncio.gather(*task_coroutines, return_exceptions=True)

        # 统计结果
        result.completed_tasks = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)
        result.failed_tasks = sum(1 for t in tasks if t.status == TaskStatus.FAILED)
        result.cancelled_tasks = sum(1 for t in tasks if t.status == TaskStatus.CANCELLED)
        result.running_tasks = sum(1 for t in tasks if t.status == TaskStatus.RUNNING)
        result.pending_tasks = sum(1 for t in tasks if t.status == TaskStatus.PENDING)

        for task in tasks:
            if task.result is not None:
                result.results[task.task_id] = task.result
            if task.error is not None:
                result.errors[task.task_id] = task.error

        result.execution_time = (datetime.now() - start_time).total_seconds()

        return result

    async def _run_sequential(
        self,
        tasks: List[BatchTask],
        config: Dict[str, Any],
        polling_interval: float = 2.0,
        timeout: float = 600.0,
        enable_retry: bool = True
    ) -> BatchTaskResult:
        """串行执行批量任务"""
        result = BatchTaskResult(total_tasks=len(tasks))
        start_time = datetime.now()

        for i, task in enumerate(tasks):
            logger.info(f"执行任务 {i+1}/{len(tasks)}: {task.name}")
            await self._execute_task(task, config, polling_interval, timeout, enable_retry)

        # 统计结果
        result.completed_tasks = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)
        result.failed_tasks = sum(1 for t in tasks if t.status == TaskStatus.FAILED)
        result.cancelled_tasks = sum(1 for t in tasks if t.status == TaskStatus.CANCELLED)

        for task in tasks:
            if task.result is not None:
                result.results[task.task_id] = task.result
            if task.error is not None:
                result.errors[task.task_id] = task.error

        result.execution_time = (datetime.now() - start_time).total_seconds()

        return result

    async def _execute_task(
        self,
        task: BatchTask,
        config: Dict[str, Any],
        polling_interval: float,
        timeout: float,
        enable_retry: bool
    ):
        """执行单个任务"""
        from cloudpss import Model

        while task.retry_count <= task.max_retries:
            try:
                task.status = TaskStatus.SUBMITTED
                task.submitted_at = datetime.now()

                # 获取模型
                model_rid = config.get("model", {}).get("rid")
                if not model_rid:
                    raise ValueError("未指定模型RID")

                model = Model.fetch(model_rid)

                # 根据任务类型执行
                if task.task_type == "emt":
                    job = await self._run_emt_task(model, task)
                elif task.task_type == "power_flow":
                    job = await self._run_power_flow_task(model, task)
                else:
                    raise ValueError(f"不支持的任务类型: {task.task_type}")

                # 等待完成
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.now()

                waited = 0
                while job.status() == 0 and waited < timeout:
                    await asyncio.sleep(polling_interval)
                    waited += polling_interval

                if job.status() == 1:  # 完成
                    task.status = TaskStatus.COMPLETED
                    task.result = {"job_id": job.id, "status": "completed"}
                    task.completed_at = datetime.now()
                    logger.info(f"任务 {task.name} 完成")
                    return
                elif job.status() == 2:  # 失败
                    raise RuntimeError(f"仿真失败: {job.id}")
                else:  # 超时
                    raise TimeoutError(f"任务超时: {timeout}s")

            except (KeyError, AttributeError, ConnectionError) as e:
                task.retry_count += 1
                if task.retry_count > task.max_retries or not enable_retry:
                    task.status = TaskStatus.FAILED
                    task.error = str(e)
                    task.completed_at = datetime.now()
                    logger.error(f"任务 {task.name} 失败: {e}")
                    return
                else:
                    logger.warning(f"任务 {task.name} 失败，第{task.retry_count}次重试: {e}")
                    await asyncio.sleep(5)  # 重试前等待

    async def _run_emt_task(self, model, task: BatchTask) -> Any:
        """运行EMT任务"""
        cfg = task.config
        job = model.runEMT(
            endTime=cfg.get("end_time", 10.0),
            step=cfg.get("step_time", 0.0001)
        )
        return job

    async def _run_power_flow_task(self, model, task: BatchTask) -> Any:
        """运行潮流任务"""
        job = model.runPowerFlow()
        return job

    def _save_csv_report(self, tasks: List[BatchTask], csv_path: Path):
        """保存CSV报告"""
        import csv

        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["任务ID", "任务名称", "类型", "状态", "重试次数", "错误信息", "耗时(s)"])

            for task in tasks:
                duration = 0
                if task.completed_at and task.started_at:
                    duration = (task.completed_at - task.started_at).total_seconds()

                writer.writerow([
                    task.task_id,
                    task.name,
                    task.task_type,
                    task.status.value,
                    task.retry_count,
                    task.error or "",
                    f"{duration:.2f}"
                ])

    def _generate_report(self, result_data: Dict[str, Any], report_path: Path):
        """生成Markdown报告"""
        lines = [
            "# 批量任务执行报告",
            "",
            f"**执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**总任务数**: {result_data['total_tasks']}",
            f"**成功任务**: {result_data['completed_tasks']}",
            f"**失败任务**: {result_data['failed_tasks']}",
            f"**执行耗时**: {result_data['execution_time']:.2f}s",
            f"**平均速度**: {result_data['tasks_per_second']:.2f} tasks/s",
            "",
            "## 执行摘要",
            "",
            f"- **成功率**: {result_data['completed_tasks']}/{result_data['total_tasks']} "
            f"({result_data['completed_tasks']/result_data['total_tasks']*100:.1f}%)",
            f"- **失败率**: {result_data['failed_tasks']}/{result_data['total_tasks']} "
            f"({result_data['failed_tasks']/result_data['total_tasks']*100:.1f}%)",
            "",
            "## 任务详情",
            "",
            "| 任务ID | 任务名称 | 类型 | 状态 | 重试 |",
            "|--------|----------|------|------|------|"
        ]

        for task in result_data.get("task_details", []):
            lines.append(
                f"| {task['task_id']} | {task['name']} | {task['type']} | "
                f"{task['status']} | {task['retry_count']} |"
            )

        if result_data.get("errors"):
            lines.extend([
                "",
                "## 错误详情",
                ""
            ])
            for task_id, error in result_data["errors"].items():
                lines.append(f"- **{task_id}**: {error}")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    @staticmethod
    def create_n1_tasks(model_rid: str, bus_labels: List[str], line_keys: List[str]) -> List[Dict]:
        """创建N-1分析任务列表"""
        tasks = []

        # 线路N-1
        for i, line_key in enumerate(line_keys):
            tasks.append({
                "name": f"N1_Line_{i+1}",
                "type": "power_flow",
                "config": {
                    "line_outage": line_key
                },
                "max_retries": 2
            })

        return tasks

    @staticmethod
    def create_vsi_tasks(model_rid: str, bus_labels: List[str]) -> List[Dict]:
        """创建VSI测试任务列表"""
        tasks = []

        for i, bus_label in enumerate(bus_labels):
            tasks.append({
                "name": f"VSI_Bus_{bus_label}",
                "type": "emt",
                "config": {
                    "target_bus": bus_label,
                    "injection_time": 8.0 + i * 1.5,
                    "injection_duration": 0.5,
                    "end_time": 15.0
                },
                "max_retries": 1
            })

        return tasks
