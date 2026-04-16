"""
Batch Power Flow Skill

批量潮流计算 - 对多个模型批量运行潮流计算。
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

from cloudpss_skills.core import (
    Artifact,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    register,
)
from cloudpss_skills.core import (
    setup_auth,
    reload_model,
    run_powerflow_and_wait,
    OutputConfig,
    save_json,
)
from cloudpss_skills.core.utils import parse_cloudpss_table

logger = logging.getLogger(__name__)


@register
class BatchPowerFlowSkill(SkillBase):
    """批量潮流计算技能"""

    @property
    def name(self) -> str:
        return "batch_powerflow"

    @property
    def description(self) -> str:
        return "批量对多个模型运行潮流计算"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "models"],
            "properties": {
                "skill": {"type": "string", "const": "batch_powerflow"},
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "token_file": {"type": "string", "default": ".cloudpss_token"},
                    },
                },
                "models": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "rid": {"type": "string"},
                            "name": {"type": "string"},
                            "source": {"enum": ["cloud", "local"], "default": "cloud"},
                        },
                        "required": ["rid"],
                    },
                    "description": "要计算的模型列表",
                },
                "algorithm": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "enum": ["newton_raphson", "fast_decoupled"],
                            "default": "newton_raphson",
                        },
                        "tolerance": {"type": "number", "default": 1e-6},
                        "max_iterations": {"type": "integer", "default": 100},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "batch_powerflow"},
                        "timestamp": {"type": "boolean", "default": True},
                        "aggregate": {
                            "type": "boolean",
                            "default": True,
                            "description": "是否生成汇总报告",
                        },
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "models": [
                {"rid": "model/holdme/IEEE3", "name": "IEEE3", "source": "cloud"}
            ],
            "algorithm": {
                "type": "newton_raphson",
                "tolerance": 1e-6,
                "max_iterations": 100,
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "batch_powerflow",
                "timestamp": True,
                "aggregate": True,
            },
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        from cloudpss_skills.core import ValidationResult

        result = ValidationResult(valid=True)

        # 基础验证（不调用父类，因为batch_powerflow使用models而非model）
        if not isinstance(config, dict):
            result.add_error("配置必须是字典类型")
            return result

        if "skill" not in config:
            result.add_error("配置必须包含 'skill' 字段")
            return result

        if config.get("skill") != self.name:
            result.add_error(
                f"技能名称不匹配: 期望 '{self.name}', 实际 '{config.get('skill')}'"
            )
            return result

        # batch_powerflow特定验证
        models = config.get("models", [])
        if not models:
            result.add_warning("建议至少指定一个模型，当前models为空")

        for i, model in enumerate(models):
            if not model.get("rid"):
                result.add_error(f"models[{i}] 必须包含rid")

        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行批量潮流计算"""
        start_time = datetime.now()
        logs = []
        artifacts = []

        def log(level: str, message: str):
            logs.append(
                LogEntry(timestamp=datetime.now(), level=level, message=message)
            )
            getattr(logger, level.lower(), logger.info)(message)

        try:
            setup_auth(config)
            log("INFO", "认证成功")

            models_config = config["models"]
            results = []
            converged_count = 0
            failed_count = 0

            log("INFO", f"开始批量潮流计算，共 {len(models_config)} 个模型")
            log("INFO", "=" * 50)

            for i, model_config in enumerate(models_config):
                model_rid = model_config["rid"]
                model_name = model_config.get("name", model_rid)
                model_source = model_config.get("source", "cloud")

                log("INFO", f"[{i + 1}/{len(models_config)}] {model_name}")

                try:
                    model = reload_model(model_rid, model_source, config)
                    log("INFO", f"  -> 模型: {model.name}")

                    job_result = run_powerflow_and_wait(model, config, log_func=log)

                    if job_result.success:
                        result = job_result.result
                        if not result.getBuses() or not result.getBranches():
                            raise RuntimeError("潮流结果为空或缺少母线/支路表")
                        converged_count += 1
                        job_id = getattr(getattr(job_result, "job", None), "id", None)

                        # Extract complete power flow results
                        bus_rows = parse_cloudpss_table(result.getBuses())
                        branch_rows = parse_cloudpss_table(result.getBranches())

                        result_data = {
                            "model_rid": model_rid,
                            "model_name": model.name,
                            "status": "converged",
                            "job_id": job_id,
                            "converged": True,
                            "bus_count": len(bus_rows) if bus_rows else 0,
                            "branch_count": len(branch_rows) if branch_rows else 0,
                            # Complete power flow results
                            "buses": bus_rows if bus_rows else [],
                            "branches": branch_rows if branch_rows else [],
                        }
                        log(
                            "INFO",
                            f"  -> 潮流收敛 ✓ ({job_result.waited_seconds:.1f}s, {len(bus_rows)} buses, {len(branch_rows)} branches)",
                        )
                    else:
                        failed_count += 1
                        result_data = {
                            "model_rid": model_rid,
                            "model_name": model.name,
                            "status": "diverged",
                            "job_id": job_result.job.id if job_result.job else "",
                            "converged": False,
                        }
                        log(
                            "WARNING",
                            f"  -> 潮流不收敛 ✗ ({job_result.waited_seconds:.1f}s)",
                        )

                    results.append(result_data)

                except (
                    AttributeError,
                    ConnectionError,
                    RuntimeError,
                    FileNotFoundError,
                    ValueError,
                    TypeError,
                    Exception,
                ) as e:
                    failed_count += 1
                    log("ERROR", f"  -> 计算异常: {e}")
                    results.append(
                        {
                            "model_rid": model_rid,
                            "model_name": model_name,
                            "status": "error",
                            "error": str(e),
                        }
                    )

            log("INFO", "=" * 50)
            log("INFO", f"批量计算完成: 收敛 {converged_count}, 失败 {failed_count}")
            log("INFO", f"  成功率: {converged_count / len(models_config) * 100:.1f}%")

            output_config = config.get("output", {})
            output = OutputConfig(
                path=output_config.get("path", "./results/"),
                prefix=output_config.get("prefix", "batch_powerflow"),
                timestamp=output_config.get("timestamp", True),
            )
            output_format = output_config.get("format", "json")
            aggregate = output_config.get("aggregate", True)

            batch_result = {
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total": len(models_config),
                    "converged": converged_count,
                    "failed": failed_count,
                    "success_rate": converged_count / len(models_config)
                    if models_config
                    else 0,
                },
                "results": results,
            }

            if output_format == "json":
                export_result = save_json(
                    batch_result, output, description="批量潮流计算结果"
                )
                if export_result.artifact:
                    artifacts.append(export_result.artifact)
            else:
                export_result = save_json(
                    batch_result, output, description="批量潮流计算结果"
                )
                if export_result.artifact:
                    artifacts.append(export_result.artifact)

            if aggregate:
                summary_content = [
                    "# 批量潮流计算报告",
                    "",
                    f"生成时间: {datetime.now().isoformat()}",
                    "",
                    "## 汇总",
                    "",
                    f"- 总模型数: {len(models_config)}",
                    f"- 收敛: {converged_count}",
                    f"- 失败: {failed_count}",
                    f"- 成功率: {converged_count / len(models_config) * 100:.1f}%",
                    "",
                    "## 详细结果",
                    "",
                    "| 模型 | 名称 | 状态 | Job ID |",
                    "|------|------|------|--------|",
                ]
                for r in results:
                    status_emoji = "✓" if r.get("converged") else "✗"
                    summary_content.append(
                        f"| {r.get('model_rid', '-')} | "
                        f"{r.get('model_name', '-')} | "
                        f"{status_emoji} {r.get('status', '-')} | "
                        f"{r.get('job_id', '-')} |"
                    )
                summary_content_str = "\n".join(summary_content)
                export_md = save_json(
                    {"report": summary_content_str},
                    output,
                    suffix="summary_report",
                    description="批量潮流计算汇总报告",
                )
                if export_md.artifact:
                    export_md.artifact.type = "markdown"
                    artifacts.append(export_md.artifact)

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS if failed_count == 0 else SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data=batch_result,
                artifacts=artifacts,
                logs=logs,
                metrics={
                    "total": len(models_config),
                    "converged": converged_count,
                    "failed": failed_count,
                },
            )

        except (
            AttributeError,
            ConnectionError,
            RuntimeError,
            FileNotFoundError,
            OSError,
            ValueError,
            TypeError,
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
                    "stage": "batch_powerflow",
                },
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )
