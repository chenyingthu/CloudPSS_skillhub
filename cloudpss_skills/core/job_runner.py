"""
Job Runner Module - Unified job execution and polling utilities.

Provides standardized interfaces for:
- Power flow job execution and waiting
- EMT simulation job execution and waiting
- Batch simulation with progress tracking
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

from cloudpss_skills.core.auth_utils import get_cloudpss_kwargs

logger = logging.getLogger(__name__)


class JobStatus(Enum):
    """Job status enumeration matching CloudPSS SDK."""

    PENDING = 0
    DONE = 1
    FAILED = 2


@dataclass
class JobResult:
    """Standardized job result container."""

    job: Any
    status: JobStatus
    result: Any = None
    error: Optional[str] = None
    duration: float = 0.0
    waited_seconds: float = 0.0
    converged: bool = False

    @property
    def success(self) -> bool:
        return self.status == JobStatus.DONE and self.result is not None


@dataclass
class BatchJobResult:
    """Result container for batch job execution."""

    total: int
    succeeded: int = 0
    failed: int = 0
    results: List[JobResult] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None

    @property
    def duration(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0

    @property
    def success_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return self.succeeded / self.total


@dataclass
class PollConfig:
    """Configuration for job polling."""

    max_wait: int = 120
    poll_seconds: int = 2
    timeout_enabled: bool = True


def get_default_poll_config() -> PollConfig:
    return PollConfig()


def run_powerflow_and_wait(
    model,
    config: Optional[Dict] = None,
    poll_config: Optional[PollConfig] = None,
    log_func: Optional[Callable[[str, str], None]] = None,
) -> JobResult:
    """
    Run power flow and wait for completion.

    Args:
        model: CloudPSS Model object
        config: Optional configuration dict (for auth kwargs)
        poll_config: Polling configuration
        log_func: Optional logging function (level, message)

    Returns:
        JobResult with status, result, and timing info
    """
    if poll_config is None:
        poll_config = get_default_poll_config()

    def log(level: str, msg: str):
        if log_func:
            log_func(level, msg)
        else:
            getattr(logger, level.lower(), logger.info)(msg)

    start_time = time.time()
    kwargs = get_cloudpss_kwargs(config) if config else {}

    log("DEBUG", "启动潮流计算...")
    job = model.runPowerFlow(**kwargs)

    waited = 0
    status = JobStatus.PENDING

    while waited < poll_config.max_wait:
        status = JobStatus(job.status())
        if status == JobStatus.DONE:
            log("DEBUG", f"潮流计算完成 ({waited}s)")
            break
        if status == JobStatus.FAILED:
            log("ERROR", "潮流计算失败")
            break
        time.sleep(poll_config.poll_seconds)
        waited += poll_config.poll_seconds

    duration = time.time() - start_time

    if status == JobStatus.DONE:
        result = job.result
        converged = result is not None
        return JobResult(
            job=job,
            status=status,
            result=result,
            duration=duration,
            waited_seconds=waited,
            converged=converged,
        )

    return JobResult(
        job=job,
        status=status,
        error=f"Job failed or timed out after {waited}s",
        duration=duration,
        waited_seconds=waited,
        converged=False,
    )


def run_emt_and_wait(
    model,
    config: Optional[Dict] = None,
    poll_config: Optional[PollConfig] = None,
    log_func: Optional[Callable[[str, str], None]] = None,
    timeout: int = 300,
) -> JobResult:
    """
    Run EMT simulation and wait for completion.

    Args:
        model: CloudPSS Model object
        config: Optional configuration dict (for auth kwargs)
        poll_config: Polling configuration
        log_func: Optional logging function (level, message)
        timeout: Maximum wait time in seconds (default 300)

    Returns:
        JobResult with status, result, and timing info
    """
    if poll_config is None:
        poll_config = PollConfig(max_wait=timeout)

    def log(level: str, msg: str):
        if log_func:
            log_func(level, msg)
        else:
            getattr(logger, level.lower(), logger.info)(msg)

    start_time = time.time()
    kwargs = get_cloudpss_kwargs(config) if config else {}

    log("DEBUG", "启动EMT仿真...")
    job = model.runEMT(**kwargs)

    waited = 0
    status = JobStatus.PENDING

    while waited < poll_config.max_wait:
        status = JobStatus(job.status())
        if status == JobStatus.DONE:
            log("DEBUG", f"EMT仿真完成 ({waited}s)")
            break
        if status == JobStatus.FAILED:
            log("ERROR", "EMT仿真失败")
            break
        time.sleep(poll_config.poll_seconds)
        waited += poll_config.poll_seconds

    duration = time.time() - start_time

    if status == JobStatus.DONE:
        result = job.result
        return JobResult(
            job=job,
            status=status,
            result=result,
            duration=duration,
            waited_seconds=waited,
            converged=True,
        )

    error_msg = (
        "EMT仿真失败" if status == JobStatus.FAILED else f"EMT仿真超时 ({waited}s)"
    )
    return JobResult(
        job=job,
        status=status,
        error=error_msg,
        duration=duration,
        waited_seconds=waited,
        converged=False,
    )


def batch_simulation(
    simulation_func: Callable,
    params_list: List[Dict[str, Any]],
    model_factory: Optional[Callable[[], Any]] = None,
    poll_config: Optional[PollConfig] = None,
    stop_on_first_failure: bool = False,
    log_func: Optional[Callable[[str, str], None]] = None,
) -> BatchJobResult:
    """
    Run batch simulations with standardized progress tracking.

    Args:
        simulation_func: Function that takes (model, params) and returns JobResult
        params_list: List of parameter dicts for each simulation
        model_factory: Optional function to create fresh model for each run
        poll_config: Polling configuration
        stop_on_first_failure: Stop batch on first failure
        log_func: Optional logging function (level, message)

    Returns:
        BatchJobResult with all job results and statistics
    """
    if poll_config is None:
        poll_config = get_default_poll_config()

    def log(level: str, msg: str):
        if log_func:
            log_func(level, msg)
        else:
            getattr(logger, level.lower(), logger.info)(msg)

    batch_result = BatchJobResult(total=len(params_list))
    batch_result.start_time = datetime.now()

    for i, params in enumerate(params_list):
        log("INFO", f"[{i + 1}/{len(params_list)}] 执行仿真...")

        try:
            if model_factory is not None:
                model = model_factory()
            else:
                model = None

            job_result = simulation_func(model, params)

            if job_result.success:
                batch_result.succeeded += 1
                log("INFO", f"  -> 成功 ({job_result.waited_seconds:.1f}s)")
            else:
                batch_result.failed += 1
                log("ERROR", f"  -> 失败: {job_result.error}")
                if stop_on_first_failure:
                    log("WARNING", "停止批量执行（遇到失败）")
                    break

            batch_result.results.append(job_result)

        except Exception as e:
            batch_result.failed += 1
            log("ERROR", f"  -> 异常: {e}")
            batch_result.results.append(
                JobResult(
                    job=None,
                    status=JobStatus.FAILED,
                    error=str(e),
                )
            )
            if stop_on_first_failure:
                break

    batch_result.end_time = datetime.now()
    log(
        "INFO",
        f"批量执行完成: 成功 {batch_result.succeeded}/{batch_result.total}, "
        f"耗时 {batch_result.duration:.1f}s",
    )

    return batch_result


def wait_for_job(
    job,
    poll_config: Optional[PollConfig] = None,
    log_func: Optional[Callable[[str, str], None]] = None,
) -> Tuple[JobStatus, float]:
    """
    Wait for any job to complete.

    Args:
        job: CloudPSS Job object
        poll_config: Polling configuration
        log_func: Optional logging function

    Returns:
        Tuple of (JobStatus, waited_seconds)
    """
    if poll_config is None:
        poll_config = get_default_poll_config()

    waited = 0
    status = JobStatus.PENDING

    while waited < poll_config.max_wait:
        status = JobStatus(job.status())
        if status != JobStatus.PENDING:
            break
        time.sleep(poll_config.poll_seconds)
        waited += poll_config.poll_seconds

    return status, waited


def check_job_status(job, raise_on_failure: bool = True) -> JobStatus:
    """
    Quick status check for a job.

    Args:
        job: CloudPSS Job object
        raise_on_failure: Raise exception if job failed

    Returns:
        JobStatus

    Raises:
        RuntimeError: If job status is FAILED and raise_on_failure is True
    """
    status = JobStatus(job.status())

    if raise_on_failure and status == JobStatus.FAILED:
        raise RuntimeError(f"Job {job.id} failed")

    return status
