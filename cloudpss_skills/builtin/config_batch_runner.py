"""
Config Batch Runner Skill

多配置场景批量运行器 - 对同一模型批量运行多个配置场景

核心功能:
1. 批量运行同一模型的多个配置(config)场景
2. 支持CloudPSS Config机制
3. 自动保存每个配置的仿真结果
4. 生成对比分析报告

适用于:
- 多运行方式对比分析
- 不同故障场景批量仿真
- 参数组合批量测试
- 配置敏感性分析

参考自: 潘春鹏工程脚本模式
"""

import csv
import json
import logging
import time
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field

from cloudpss_skills.core import (
    Artifact,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    register,
)
from cloudpss_skills.core.auth_utils import load_or_fetch_model, setup_auth

logger = logging.getLogger(__name__)


@dataclass
class ConfigRunResult:
    """单个配置运行结果"""

    config_index: int
    config_name: str
    status: str  # success, failed, timeout
    runner_id: Optional[int] = None
    timestamp: Optional[str] = None
    execution_time: float = 0.0
    error_message: Optional[str] = None
    result_summary: Dict[str, Any] = field(default_factory=dict)


@register
class ConfigBatchRunnerSkill(SkillBase):
    """多配置场景批量运行技能"""

    @property
    def name(self) -> str:
        return "config_batch_runner"

    @property
    def description(self) -> str:
        return "多配置场景批量运行器 - 对同一模型批量运行多个配置场景，支持Config机制"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "config_batch_runner"},
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "token_file": {"type": "string", "default": ".cloudpss_token"},
                    },
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {
                        "rid": {"type": "string", "description": "模型RID"},
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                        "job_name": {
                            "type": "string",
                            "description": "指定job名称，不指定则使用第一个EMT/PF job",
                        },
                    },
                },
                "configs": {
                    "type": "object",
                    "properties": {
                        "mode": {
                            "enum": ["all", "range", "list"],
                            "default": "all",
                            "description": "配置选择模式",
                        },
                        "indices": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "指定配置索引列表(list模式)",
                        },
                        "start": {
                            "type": "integer",
                            "default": 0,
                            "description": "起始索引(range模式)",
                        },
                        "end": {
                            "type": "integer",
                            "description": "结束索引(range模式)",
                        },
                        "custom_args": {
                            "type": "object",
                            "description": "覆盖参数，如{'end_time': 10, 'step_time': 0.0001}",
                        },
                    },
                },
                "execution": {
                    "type": "object",
                    "properties": {
                        "polling_interval": {
                            "type": "number",
                            "default": 5.0,
                            "description": "状态轮询间隔(s)",
                        },
                        "timeout": {
                            "type": "number",
                            "default": 3600.0,
                            "description": "单配置超时(s)",
                        },
                        "continue_on_error": {
                            "type": "boolean",
                            "default": True,
                            "description": "出错时继续下一个配置",
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "config_batch"},
                        "save_runner_ids": {
                            "type": "boolean",
                            "default": True,
                            "description": "保存runner ID列表到CSV",
                        },
                        "export_results": {
                            "type": "boolean",
                            "default": False,
                            "description": "是否导出详细仿真结果",
                        },
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "model": {
                "rid": "",
                "source": "cloud",
            },
            "configs": {
                "mode": "all",
                "custom_args": {},
            },
            "execution": {
                "polling_interval": 5.0,
                "timeout": 3600.0,
                "continue_on_error": True,
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "config_batch",
                "save_runner_ids": True,
                "export_results": False,
            },
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        """验证配置"""
        result = super().validate(config)

        model = config.get("model", {})
        rid = model.get("rid", "")

        if not rid:
            result.add_error("必须提供model.rid")
            result.add_error("  示例: 'model/holdme/IEEE39'")

        configs = config.get("configs", {})
        mode = configs.get("mode", "all")

        if mode == "list":
            indices = configs.get("indices", [])
            if not indices:
                result.add_error("list模式必须指定configs.indices")
        elif mode == "range":
            if "end" not in configs:
                result.add_error("range模式必须指定configs.end")
            if configs.get("start", 0) >= configs.get("end", 0):
                result.add_error("range模式的start必须小于end")

        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行多配置批量运行"""
        from cloudpss import Model, setToken

        start_time = datetime.now()
        logs = []
        artifacts = []
        results = []

        def log(level: str, message: str):
            logs.append(
                LogEntry(timestamp=datetime.now(), level=level, message=message)
            )
            getattr(logger, level.lower(), logger.info)(message)

        try:
            setup_auth(config)

            # 1. 认证
            log("INFO", "加载认证信息...")
            auth = config.get("auth", {})
            token = auth.get("token")

            if not token:
                token_file = auth.get("token_file", ".cloudpss_token")
                token_path = Path(token_file)
                if token_path.exists():
                    token = token_path.read_text().strip()

            if not token:
                raise ValueError(
                    "未找到CloudPSS token，请提供auth.token或创建.cloudpss_token文件"
                )

            setToken(token)
            log("INFO", "认证成功")

            # 2. 加载模型
            model_config = config.get("model", {})
            rid = model_config["rid"]
            source = model_config.get("source", "cloud")
            job_name = model_config.get("job_name")

            log("INFO", f"加载模型: {rid}")

            model = load_or_fetch_model(model_config, config)

            log("INFO", f"模型名称: {model.name}")
            log("INFO", f"可用配置数: {len(model.configs)}")

            if len(model.configs) == 0:
                raise ValueError("模型没有可用的配置(configs)")

            # 3. 获取执行配置
            configs_config = config.get("configs", {})
            mode = configs_config.get("mode", "all")
            custom_args = configs_config.get("custom_args", {})

            execution_config = config.get("execution", {})
            polling_interval = execution_config.get("polling_interval", 5.0)
            timeout = execution_config.get("timeout", 3600.0)
            continue_on_error = execution_config.get("continue_on_error", True)

            output_config = config.get("output", {})
            export_results = output_config.get("export_results", False)

            # 4. 确定要运行的配置索引
            if mode == "all":
                config_indices = list(range(len(model.configs)))
            elif mode == "range":
                start = configs_config.get("start", 0)
                end = configs_config.get("end", len(model.configs))
                config_indices = list(range(start, min(end, len(model.configs))))
            elif mode == "list":
                indices = configs_config.get("indices", [])
                config_indices = [i for i in indices if 0 <= i < len(model.configs)]
            else:
                config_indices = list(range(len(model.configs)))

            log("INFO", f"将运行 {len(config_indices)} 个配置场景")

            # 5. 选择job
            if job_name:
                job = model.getModelJob(job_name)
                if isinstance(job, list):
                    job = job[0]
                log("INFO", f"使用指定job: {job_name}")
            else:
                # 自动选择第一个EMT或PF job
                job = None
                for j in model.jobs:
                    if j.get("rid") in [
                        "function/CloudPSS/emtps",
                        "function/CloudPSS/powerflow",
                    ]:
                        job = j
                        break
                if not job and model.jobs:
                    job = model.jobs[0]
                log("INFO", f"使用默认job: {job.get('name', 'unnamed')}")

            # 6. 批量运行配置
            log("INFO", "开始批量运行配置...")
            runner_ids = []

            for idx, config_idx in enumerate(config_indices):
                cfg = model.configs[config_idx]
                cfg_name = (
                    cfg.get("name", f"Config_{config_idx}")
                    if isinstance(cfg, dict)
                    else f"Config_{config_idx}"
                )

                log(
                    "INFO",
                    f"[{idx + 1}/{len(config_indices)}] 运行配置: {cfg_name} (索引: {config_idx})",
                )

                cfg_start_time = time.time()

                try:
                    # 应用自定义参数覆盖
                    if custom_args:
                        for key, value in custom_args.items():
                            if isinstance(cfg, dict) and "args" in cfg:
                                cfg["args"][key] = value
                            elif hasattr(cfg, "args"):
                                cfg.args[key] = value
                            if "args" in job:
                                job["args"][key] = value

                    # 运行仿真
                    runner = model.run(job, cfg)
                    runner_id = runner.id
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    log("INFO", f"  -> Runner ID: {runner_id}")

                    # 等待完成
                    elapsed = 0
                    while not runner.status() and elapsed < timeout:
                        time.sleep(polling_interval)
                        elapsed += polling_interval
                        logs_buffer = []
                        try:
                            if hasattr(runner, "result") and hasattr(
                                runner.result, "getLogs"
                            ):
                                logs_buffer = runner.result.getLogs() or []
                        except (AttributeError, RuntimeError, TypeError):
                            logs_buffer = []
                        if logs_buffer and idx == 0:  # 只打印第一个配置的日志
                            for log_entry in logs_buffer[-3:]:  # 最近3条
                                if isinstance(log_entry, dict) and "data" in log_entry:
                                    content = log_entry["data"].get("content", "")
                                    if content:
                                        log("DEBUG", f"    {content[:80]}")

                    if elapsed >= timeout:
                        log("WARN", f"  -> 配置超时 (> {timeout}s)")
                        result = ConfigRunResult(
                            config_index=config_idx,
                            config_name=cfg_name,
                            status="timeout",
                            runner_id=runner_id,
                            timestamp=current_time,
                            execution_time=elapsed,
                            error_message="执行超时",
                        )
                    else:
                        # 获取结果摘要
                        result_summary = {}
                        try:
                            if hasattr(runner.result, "getPlots"):
                                plots = runner.result.getPlots()
                                result_summary["plots_count"] = len(plots)

                            # 获取潮流结果数据（如果存在）
                            if hasattr(runner.result, "getBuses"):
                                buses = runner.result.getBuses()
                                result_summary["buses_count"] = (
                                    len(buses) if buses else 0
                                )

                            if hasattr(runner.result, "getBranches"):
                                branches = runner.result.getBranches()
                                result_summary["branches_count"] = (
                                    len(branches) if branches else 0
                                )

                        except (KeyError, AttributeError) as e:
                            log("DEBUG", f"  -> 获取结果摘要失败: {e}")

                        execution_time = time.time() - cfg_start_time
                        log("INFO", f"  -> 完成，耗时: {execution_time:.1f}s")

                        result = ConfigRunResult(
                            config_index=config_idx,
                            config_name=cfg_name,
                            status="success",
                            runner_id=runner_id,
                            timestamp=current_time,
                            execution_time=execution_time,
                            result_summary=result_summary,
                        )

                    results.append(result)
                    runner_ids.append(
                        (runner_id, current_time, cfg_name, model.rid, model.name)
                    )

                except (
                    KeyError,
                    AttributeError,
                    ValueError,
                    RuntimeError,
                    TimeoutError,
                    TypeError,
                    FileNotFoundError,
                    ConnectionError,
                    Exception,
                ) as e:
                    error_msg = str(e)
                    log("ERROR", f"  -> 运行失败: {error_msg}")
                    result = ConfigRunResult(
                        config_index=config_idx,
                        config_name=cfg_name,
                        status="failed",
                        error_message=error_msg,
                    )
                    results.append(result)

                    if not continue_on_error:
                        log("INFO", "停止运行（continue_on_error=False）")
                        break

            # 7. 生成报告
            log("INFO", "生成批量运行报告...")
            report = self._generate_report(results, model, config)

            # 保存结果
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "config_batch")

            # 导出详细仿真结果（当 export_results=True 时）
            if export_results and success_results:
                log("INFO", "导出详细仿真结果...")
                try:
                    detailed_results = self._export_detailed_results(
                        results, model, output_path, prefix, log
                    )
                    if detailed_results:
                        artifacts.extend(detailed_results)
                        log("INFO", f"已导出 {len(detailed_results)} 个详细结果文件")
                except Exception as e:
                    log("WARN", f"导出详细结果失败: {e}")

            # 保存JSON报告
            report_file = output_path / f"{prefix}_report.json"
            report_file.write_text(
                json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            artifacts.append(
                Artifact(
                    type="json",
                    path=str(report_file),
                    size=report_file.stat().st_size,
                    description="批量运行报告",
                )
            )

            # 保存Runner ID列表（CSV格式）
            if output_config.get("save_runner_ids", True) and runner_ids:
                csv_file = output_path / f"{prefix}_runner_ids.csv"
                with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        [
                            "Runner ID",
                            "Timestamp",
                            "Config Name",
                            "Model RID",
                            "Model Name",
                        ]
                    )
                    for (
                        runner_id,
                        timestamp,
                        cfg_name,
                        model_rid,
                        model_name,
                    ) in runner_ids:
                        writer.writerow(
                            [runner_id, timestamp, cfg_name, model_rid, model_name]
                        )
                artifacts.append(
                    Artifact(
                        type="csv",
                        path=str(csv_file),
                        size=csv_file.stat().st_size,
                        description="Runner ID列表",
                    )
                )

            # 统计
            success_count = sum(1 for r in results if r.status == "success")
            failed_count = sum(1 for r in results if r.status == "failed")
            timeout_count = sum(1 for r in results if r.status == "timeout")

            log(
                "INFO",
                f"批量运行完成: 成功 {success_count}, 失败 {failed_count}, 超时 {timeout_count}",
            )

            # 根据结果确定状态
            has_failures = failed_count > 0 or timeout_count > 0

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS if not has_failures else SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "model_rid": rid,
                    "model_name": model.name,
                    "total_configs": len(config_indices),
                    "success_count": success_count,
                    "failed_count": failed_count,
                    "timeout_count": timeout_count,
                    "runner_count": len(runner_ids),
                    "results": [self._result_to_dict(r) for r in results],
                },
                artifacts=artifacts,
                logs=logs,
            )

        except (
            KeyError,
            AttributeError,
            ValueError,
            RuntimeError,
            TimeoutError,
            TypeError,
            FileNotFoundError,
            ConnectionError,
            Exception,
        ) as e:
            log("ERROR", f"执行失败: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "success": False,
                    "error": str(e),
                    "stage": "config_batch_runner",
                },
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )

    def _generate_report(
        self, results: List[ConfigRunResult], model: Any, config: Dict
    ) -> Dict:
        """生成报告"""
        success_results = [r for r in results if r.status == "success"]
        failed_results = [r for r in results if r.status == "failed"]
        timeout_results = [r for r in results if r.status == "timeout"]

        total_time = sum(r.execution_time for r in success_results)

        return {
            "summary": {
                "model_rid": model.rid,
                "model_name": model.name,
                "total_configs": len(results),
                "success_count": len(success_results),
                "failed_count": len(failed_results),
                "timeout_count": len(timeout_results),
                "total_execution_time": total_time,
                "average_execution_time": total_time / len(success_results)
                if success_results
                else 0,
            },
            "successful_runs": [self._result_to_dict(r) for r in success_results],
            "failed_runs": [self._result_to_dict(r) for r in failed_results],
            "timeout_runs": [self._result_to_dict(r) for r in timeout_results],
        }

    def _result_to_dict(self, result: ConfigRunResult) -> Dict:
        """转换结果为字典"""
        return {
            "config_index": result.config_index,
            "config_name": result.config_name,
            "status": result.status,
            "runner_id": result.runner_id,
            "timestamp": result.timestamp,
            "execution_time": result.execution_time,
            "error_message": result.error_message,
            "result_summary": result.result_summary,
        }

    def _export_detailed_results(
        self,
        results: List[ConfigRunResult],
        model: Any,
        output_path: Path,
        prefix: str,
        log_func,
    ) -> List[Artifact]:
        """导出每个成功运行的详细仿真结果"""
        from cloudpss_skills.core.utils import parse_cloudpss_table

        artifacts = []
        success_results = [r for r in results if r.status == "success"]

        for i, result in enumerate(success_results, 1):
            try:
                model_copy = model.clone()
                cfg = model_copy.configs[result.config_index]

                if hasattr(model_copy, "jobs") and model_copy.jobs:
                    job = model_copy.jobs[0]
                    runner = model_copy.run(job, cfg)

                    elapsed = 0
                    while not runner.status() and elapsed < 60:
                        import time

                        time.sleep(1)
                        elapsed += 1
                        if elapsed >= 60:
                            break

                    if runner.status() and hasattr(runner, "result"):
                        pf_result = runner.result
                        detailed_data = {
                            "config_index": result.config_index,
                            "config_name": result.config_name,
                            "model_rid": model.rid,
                            "model_name": model.name,
                        }

                        if hasattr(pf_result, "getBuses"):
                            buses = pf_result.getBuses()
                            if buses:
                                detailed_data["buses"] = parse_cloudpss_table(buses)

                        if hasattr(pf_result, "getBranches"):
                            branches = pf_result.getBranches()
                            if branches:
                                detailed_data["branches"] = parse_cloudpss_table(
                                    branches
                                )

                        if hasattr(pf_result, "getPlots"):
                            plots = pf_result.getPlots()
                            if plots:
                                detailed_data["plots"] = [
                                    {"name": p.get("name", f"plot_{j}")}
                                    for j, p in enumerate(plots)
                                ]

                        result_file = (
                            output_path
                            / f"{prefix}_config_{result.config_index}_result.json"
                        )
                        result_file.write_text(
                            json.dumps(detailed_data, indent=2, ensure_ascii=False),
                            encoding="utf-8",
                        )
                        artifacts.append(
                            Artifact(
                                type="json",
                                path=str(result_file),
                                size=result_file.stat().st_size,
                                description=f"配置 {result.config_index} ({result.config_name}) 详细结果",
                            )
                        )
                        log_func(
                            "DEBUG", f"  -> 已导出配置 {result.config_index} 详细结果"
                        )

            except Exception as e:
                log_func(
                    "WARN", f"  -> 导出配置 {result.config_index} 详细结果失败: {e}"
                )
                continue

        return artifacts
