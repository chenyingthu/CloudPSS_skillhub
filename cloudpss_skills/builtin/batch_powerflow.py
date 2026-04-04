"""
Batch Power Flow Skill

批量潮流计算 - 对多个模型批量运行潮流计算。
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register

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
                    "description": "要计算的模型列表"
                },
                "algorithm": {
                    "type": "object",
                    "properties": {
                        "type": {"enum": ["newton_raphson", "fast_decoupled"], "default": "newton_raphson"},
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
                        "aggregate": {"type": "boolean", "default": True, "description": "是否生成汇总报告"},
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
            result.add_error(f"技能名称不匹配: 期望 '{self.name}', 实际 '{config.get('skill')}'")
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
        from cloudpss import Model, setToken

        start_time = datetime.now()
        logs = []
        artifacts = []

        def log(level: str, message: str):
            logs.append(LogEntry(
                timestamp=datetime.now(),
                level=level,
                message=message
            ))
            getattr(logger, level.lower(), logger.info)(message)

        try:
            # 1. 认证
            log("INFO", "加载认证信息...")
            auth = config.get("auth", {})
            token = auth.get("token")

            if not token:
                token_file = auth.get("token_file", ".cloudpss_token")
                token_path = Path(token_file)
                if not token_path.exists():
                    raise FileNotFoundError(f"Token文件不存在: {token_file}")
                token = token_path.read_text().strip()

            setToken(token)
            log("INFO", "认证成功")

            # 2. 批量计算
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

                log("INFO", f"[{i+1}/{len(models_config)}] {model_name}")

                try:
                    # 获取模型
                    if model_source == "local":
                        model = Model.load(model_rid)
                    else:
                        model = Model.fetch(model_rid)

                    log("INFO", f"  -> 模型: {model.name}")

                    # 运行潮流
                    job = model.runPowerFlow()
                    log("INFO", f"  -> Job ID: {job.id}")

                    # 等待仿真完成
                    import time
                    max_wait = 120
                    waited = 0
                    status = 0
                    while waited < max_wait:
                        status = job.status()
                        if status == 1:  # 完成
                            break
                        elif status == 2:  # 失败
                            break
                        time.sleep(2)
                        waited += 2

                    if status == 1:
                        converged_count += 1
                        result_data = {
                            "model_rid": model_rid,
                            "model_name": model.name,
                            "status": "converged",
                            "job_id": job.id,
                            "converged": True,
                        }
                        log("INFO", f"  -> 潮流收敛 ✓ ({waited}s)")
                    else:
                        failed_count += 1
                        result_data = {
                            "model_rid": model_rid,
                            "model_name": model.name,
                            "status": "diverged" if status == 2 else "timeout",
                            "job_id": job.id,
                            "converged": False,
                        }
                        log("WARNING", f"  -> 潮流不收敛 ✗ ({waited}s, status={status})")

                    results.append(result_data)

                except (AttributeError, ConnectionError, RuntimeError) as e:
                    failed_count += 1
                    log("ERROR", f"  -> 计算异常: {e}")
                    results.append({
                        "model_rid": model_rid,
                        "model_name": model_name,
                        "status": "error",
                        "error": str(e),
                    })

            # 3. 生成汇总
            log("INFO", "=" * 50)
            log("INFO", "批量计算完成:")
            log("INFO", f"  收敛: {converged_count}")
            log("INFO", f"  不收敛/失败: {failed_count}")
            log("INFO", f"  成功率: {converged_count/len(models_config)*100:.1f}%")

            # 4. 导出结果
            output_config = config.get("output", {})
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)

            prefix = output_config.get("prefix", "batch_powerflow")
            use_timestamp = output_config.get("timestamp", True)
            output_format = output_config.get("format", "json")
            aggregate = output_config.get("aggregate", True)

            filename = prefix
            if use_timestamp:
                filename += f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            filename += ".json" if output_format == "json" else ".csv"

            filepath = output_path / filename

            batch_result = {
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total": len(models_config),
                    "converged": converged_count,
                    "failed": failed_count,
                    "success_rate": converged_count / len(models_config) if models_config else 0,
                },
                "results": results,
            }

            if output_format == "json":
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(batch_result, f, indent=2, ensure_ascii=False)
            else:
                # CSV格式
                import csv
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["model_rid", "model_name", "status", "job_id", "converged"])
                    for r in results:
                        writer.writerow([
                            r.get("model_rid", ""),
                            r.get("model_name", ""),
                            r.get("status", ""),
                            r.get("job_id", ""),
                            r.get("converged", ""),
                        ])

            artifacts.append(Artifact(
                type=output_format,
                path=str(filepath),
                size=filepath.stat().st_size,
                description="批量潮流计算结果"
            ))

            log("INFO", f"结果已保存: {filepath}")

            # 生成汇总报告
            if aggregate:
                summary_filename = f"{prefix}_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                summary_path = output_path / summary_filename

                summary_lines = [
                    "# 批量潮流计算报告",
                    "",
                    f"生成时间: {datetime.now().isoformat()}",
                    "",
                    "## 汇总",
                    "",
                    f"- 总模型数: {len(models_config)}",
                    f"- 收敛: {converged_count}",
                    f"- 失败: {failed_count}",
                    f"- 成功率: {converged_count/len(models_config)*100:.1f}%",
                    "",
                    "## 详细结果",
                    "",
                    "| 模型 | 名称 | 状态 | Job ID |",
                    "|------|------|------|--------|",
                ]

                for r in results:
                    status_emoji = "✓" if r.get("converged") else "✗"
                    summary_lines.append(
                        f"| {r.get('model_rid', '-')} | "
                        f"{r.get('model_name', '-')} | "
                        f"{status_emoji} {r.get('status', '-')} | "
                        f"{r.get('job_id', '-')} |"
                    )

                summary_path.write_text("\n".join(summary_lines), encoding='utf-8')

                artifacts.append(Artifact(
                    type="markdown",
                    path=str(summary_path),
                    size=summary_path.stat().st_size,
                    description="批量潮流计算汇总报告"
                ))

                log("INFO", f"汇总报告已保存: {summary_path}")

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

        except (AttributeError, ConnectionError, RuntimeError, FileNotFoundError, OSError) as e:
            log("ERROR", f"执行失败: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data={},
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )
