"""
Study Pipeline Skill

研究流水线 - 自动串联多个技能执行完整研究流程
支持步骤依赖、数据传递、结果聚合和断点续跑
"""

import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

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
    OutputConfig,
    save_json,
    generate_report,
)
from cloudpss_skills.core.registry import get_skill

logger = logging.getLogger(__name__)


@register
class StudyPipelineSkill(SkillBase):
    """研究流水线技能"""

    @property
    def name(self) -> str:
        return "study_pipeline"

    @property
    def description(self) -> str:
        return "研究流水线 - 自动串联多个技能执行完整研究流程"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "pipeline"],
            "properties": {
                "skill": {"type": "string", "const": "study_pipeline"},
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "token_file": {"type": "string", "default": ".cloudpss_token"},
                    },
                },
                "pipeline": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["skill"],
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "步骤名称（可选）",
                            },
                            "skill": {"type": "string", "description": "技能名称"},
                            "config": {
                                "type": "object",
                                "description": "技能配置（支持变量替换）",
                            },
                            "skip_on_failure": {
                                "type": "boolean",
                                "default": False,
                                "description": "前置步骤失败时是否跳过",
                            },
                            "depends_on": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "依赖的前置步骤名称",
                            },
                        },
                    },
                    "description": "流水线步骤列表",
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "pipeline"},
                        "generate_report": {"type": "boolean", "default": True},
                    },
                },
                "continue_on_failure": {
                    "type": "boolean",
                    "default": False,
                    "description": "步骤失败时是否继续执行后续步骤",
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "pipeline": [],
            "output": {
                "path": "./results/",
                "prefix": "pipeline",
                "generate_report": True,
            },
            "continue_on_failure": False,
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        result = super().validate(config)

        pipeline = config.get("pipeline", [])
        if not pipeline:
            result.add_error("pipeline不能为空")
            return result

        skill_names = set()
        for i, step in enumerate(pipeline):
            step_name = step.get("name") or step.get("skill")
            if not step.get("skill"):
                result.add_error(f"pipeline[{i}]: 必须指定skill")
            if step_name in skill_names and not step.get("name"):
                result.add_warning(f"pipeline[{i}]: 多个步骤使用相同名称 '{step_name}'")
            skill_names.add(step_name)

        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
        start_time = datetime.now()
        logs = []
        artifacts = []
        step_results = []

        def log(level: str, message: str):
            logs.append(
                LogEntry(timestamp=datetime.now(), level=level, message=message)
            )
            getattr(logger, level.lower(), logger.info)(message)

        try:
            setup_auth(config)
            log("INFO", "认证成功")

            pipeline = config.get("pipeline", [])
            output_config = config.get("output", {})
            continue_on_failure = config.get("continue_on_failure", False)

            log("INFO", f"=" * 50)
            log("INFO", f"开始执行研究流水线，共 {len(pipeline)} 个步骤")
            log("INFO", f"=" * 50)

            context = {"steps": {}, "artifacts": []}

            for i, step_config in enumerate(pipeline):
                step_name = step_config.get("name") or step_config.get("skill")
                skill_name = step_config["skill"]
                step_log_prefix = f"[{i + 1}/{len(pipeline)}] {step_name}"

                log("INFO", f"{step_log_prefix}: 开始执行...")

                try:
                    skill = get_skill(skill_name)
                    if skill is None:
                        raise ValueError(f"技能 '{skill_name}' 不存在")

                    step_config_final = self._resolve_config(
                        step_config.get("config", {}),
                        context,
                    )

                    result = skill.run(step_config_final)

                    context["steps"][step_name] = {
                        "result": result,
                        "status": result.status,
                        "data": result.data,
                        "artifacts": result.artifacts,
                    }
                    context["artifacts"].extend(result.artifacts)

                    if result.status == SkillStatus.SUCCESS:
                        log("INFO", f"{step_log_prefix}: ✓ 成功")
                        step_results.append(
                            {
                                "name": step_name,
                                "skill": skill_name,
                                "status": "success",
                                "duration": (
                                    result.end_time - result.start_time
                                ).total_seconds()
                                if result.end_time and result.start_time
                                else 0,
                            }
                        )
                    else:
                        log("WARNING", f"{step_log_prefix}: ✗ 失败 - {result.error}")
                        step_results.append(
                            {
                                "name": step_name,
                                "skill": skill_name,
                                "status": "failed",
                                "error": result.error,
                            }
                        )
                        if not continue_on_failure:
                            log("ERROR", "停止流水线执行")
                            break

                except Exception as e:
                    log("ERROR", f"{step_log_prefix}: ✗ 异常 - {e}")
                    step_results.append(
                        {
                            "name": step_name,
                            "skill": skill_name,
                            "status": "error",
                            "error": str(e),
                        }
                    )
                    if not continue_on_failure:
                        log("ERROR", "停止流水线执行")
                        break

            log("INFO", f"=" * 50)
            success_count = sum(1 for r in step_results if r["status"] == "success")
            log("INFO", f"流水线执行完成: {success_count}/{len(step_results)} 成功")

            output = OutputConfig(
                path=output_config.get("path", "./results/"),
                prefix=output_config.get("prefix", "pipeline"),
                timestamp=True,
            )

            pipeline_result = {
                "timestamp": datetime.now().isoformat(),
                "total_steps": len(pipeline),
                "success_count": success_count,
                "failed_count": len(step_results) - success_count,
                "steps": step_results,
                "context": {
                    name: {
                        "status": data["status"].value,
                        "has_data": bool(data.get("data")),
                        "artifacts_count": len(data.get("artifacts", [])),
                    }
                    for name, data in context["steps"].items()
                },
            }

            export_json = save_json(
                pipeline_result,
                output,
                description="流水线执行结果",
            )
            if export_json.artifact:
                artifacts.append(export_json.artifact)

            if output_config.get("generate_report", True):
                report_content = self._generate_report(pipeline_result)
                export_md = generate_report(
                    report_content,
                    output,
                    suffix="report",
                    description="流水线执行报告",
                )
                if export_md.artifact:
                    artifacts.append(export_md.artifact)

            overall_status = SkillStatus.SUCCESS
            if any(r["status"] in ("failed", "error") for r in step_results):
                overall_status = SkillStatus.FAILED

            return SkillResult(
                skill_name=self.name,
                status=overall_status,
                start_time=start_time,
                end_time=datetime.now(),
                data=pipeline_result,
                artifacts=artifacts,
                logs=logs,
                metrics={
                    "total_steps": len(pipeline),
                    "success_count": success_count,
                    "failed_count": len(step_results) - success_count,
                },
            )

        except Exception as e:
            log("ERROR", f"流水线执行失败: {e}")
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

    def _resolve_config(
        self,
        config: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Any:
        """递归解析配置中的变量占位符"""
        if isinstance(config, dict):
            return {k: self._resolve_config(v, context) for k, v in config.items()}
        elif isinstance(config, list):
            return [self._resolve_config(item, context) for item in config]
        elif isinstance(config, str):
            return self._resolve_string(config, context)
        else:
            return config

    def _resolve_string(self, value: str, context: Dict[str, Any]) -> Any:
        """解析字符串中的变量占位符"""
        pattern = r"\$\{([^}]+)\}"

        if "${" not in value:
            return value

        matches = list(re.finditer(pattern, value))

        if not matches:
            return value

        if len(matches) == 1:
            match = matches[0]
            var_path = match.group(1).strip()
            resolved = self._resolve_var_path(var_path, context)
            if resolved is not None:
                return resolved
            return value

        parts = []
        last_end = 0
        for match in matches:
            parts.append(value[last_end : match.start()])
            var_path = match.group(1).strip()
            resolved = self._resolve_var_path(var_path, context)
            if resolved is not None:
                if isinstance(resolved, list):
                    parts.append(str(resolved))
                elif isinstance(resolved, dict):
                    parts.append(str(resolved))
                else:
                    parts.append(str(resolved))
            else:
                parts.append(match.group(0))
            last_end = match.end()

        parts.append(value[last_end:])
        result = "".join(parts)

        if "${" in result:
            return value

        return result

    def _resolve_var_path(self, var_path: str, context: Dict[str, Any]) -> Any:
        """解析变量路径"""
        if var_path.startswith("steps."):
            parts = var_path.split(".")
            step_name = parts[1]
            attr_path = ".".join(parts[2:]) if len(parts) > 2 else None

            if step_name in context["steps"]:
                step_data = context["steps"][step_name]
                if attr_path:
                    path_parts = attr_path.split(".")
                    val = step_data
                    for p in path_parts:
                        if isinstance(val, dict):
                            val = val.get(p)
                        else:
                            return None
                    return val
                else:
                    return step_data.get("result")

        elif var_path.startswith("artifacts."):
            parts = var_path.split(".")
            step_name = parts[1]

            if step_name in context["steps"]:
                return context["steps"][step_name].get("artifacts", [])

        elif var_path == "output.path":
            return context.get("_output_path", "./results/")

        return None

    def _generate_report(self, pipeline_result: Dict) -> str:
        """生成流水线执行报告"""
        lines = [
            "# 研究流水线执行报告",
            "",
            f"**执行时间**: {pipeline_result['timestamp']}",
            f"**总步骤数**: {pipeline_result['total_steps']}",
            f"**成功**: {pipeline_result['success_count']}",
            f"**失败**: {pipeline_result['failed_count']}",
            "",
        ]

        lines.extend(["## 步骤执行详情", ""])

        for step in pipeline_result.get("steps", []):
            status_icon = "✓" if step["status"] == "success" else "✗"
            lines.append(f"### {status_icon} {step['name']}")

            if step["status"] == "success":
                lines.append(f"- **技能**: {step['skill']}")
                lines.append(f"- **耗时**: {step.get('duration', 0):.1f}s")
            else:
                lines.append(f"- **技能**: {step['skill']}")
                lines.append(f"- **错误**: {step.get('error', '未知错误')}")

            lines.append("")

        lines.extend(
            [
                "## 上下文数据",
                "",
            ]
        )

        for name, data in pipeline_result.get("context", {}).items():
            lines.append(f"### {name}")
            lines.append(f"- 状态: {data['status']}")
            lines.append(f"- 数据: {'有' if data['has_data'] else '无'}")
            lines.append(f"- 产物数: {data['artifacts_count']}")
            lines.append("")

        lines.extend(
            [
                "## 结论",
                "",
            ]
        )

        if pipeline_result["failed_count"] == 0:
            lines.append("✅ 所有步骤执行成功")
        elif pipeline_result["success_count"] == 0:
            lines.append("❌ 所有步骤执行失败")
        else:
            lines.append(f"⚠️ {pipeline_result['failed_count']} 个步骤执行失败")

        return "\n".join(lines)
