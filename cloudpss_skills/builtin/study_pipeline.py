"""
Study Pipeline Skill

研究流水线 - 自动串联多个技能执行完整研究流程
支持并行执行、条件分支、循环遍历、数据传递和断点续跑
"""

import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

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
                            "name": {"type": "string", "description": "步骤名称"},
                            "skill": {"type": "string", "description": "技能名称"},
                            "config": {"type": "object", "description": "技能配置"},
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
                            "parallel": {
                                "type": "boolean",
                                "default": False,
                                "description": "是否与其他并行步骤一起执行",
                            },
                            "when": {
                                "type": "string",
                                "description": "执行条件（如 'steps.n1.success'）",
                            },
                            "foreach": {
                                "type": "object",
                                "properties": {
                                    "items": {
                                        "type": "string",
                                        "description": "迭代变量路径（如 'steps.scan.data.items'）",
                                    },
                                    "item_name": {
                                        "type": "string",
                                        "default": "item",
                                        "description": "循环中当前项的变量名",
                                    },
                                },
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
                "max_workers": {
                    "type": "integer",
                    "default": 4,
                    "description": "并行执行的最大线程数",
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
            "max_workers": 4,
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        result = super().validate(config)

        pipeline = config.get("pipeline", [])
        if not pipeline:
            result.add_error("pipeline不能为空")
            return result

        step_names: Set[str] = set()
        for i, step in enumerate(pipeline):
            step_name = step.get("name") or step.get("skill")
            if not step.get("skill"):
                result.add_error(f"pipeline[{i}]: 必须指定skill")

            if step_name in step_names:
                result.add_warning(f"pipeline[{i}]: 多个步骤使用相同名称 '{step_name}'")
            step_names.add(step_name)

            deps = step.get("depends_on", [])
            for dep in deps:
                if dep not in step_names and dep != step_name:
                    result.add_warning(f"pipeline[{i}]: 依赖的步骤 '{dep}' 尚未定义")

        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
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

            pipeline = self._expand_pipeline(config.get("pipeline", []), {})
            output_config = config.get("output", {})
            continue_on_failure = config.get("continue_on_failure", False)
            max_workers = config.get("max_workers", 4)

            log("INFO", f"=" * 50)
            log("INFO", f"开始执行研究流水线，共 {len(pipeline)} 个步骤")
            log("INFO", "=" * 50)

            context = {"steps": {}, "artifacts": [], "_pipeline": pipeline}
            step_results = []

            executed: Set[str] = set()
            total_iterations = 0

            while len(executed) < len(pipeline):
                ready_steps = self._get_ready_steps(
                    pipeline, executed, context, continue_on_failure
                )

                if not ready_steps:
                    if len(executed) < len(pipeline):
                        log("ERROR", "没有可执行的步骤，可能存在循环依赖")
                    break

                if len(ready_steps) > 1 and all(
                    s.get("parallel", False) for s in ready_steps
                ):
                    log("INFO", f"并行执行 {len(ready_steps)} 个步骤...")
                    batch_results = self._execute_parallel(
                        ready_steps, pipeline, context, max_workers, log, config
                    )
                    step_results.extend(batch_results)
                    for r in batch_results:
                        executed.add(r["name"])
                else:
                    for step_config in ready_steps:
                        if step_config.get("parallel", False):
                            continue
                        result = self._execute_step(step_config, pipeline, context, log, config)
                        step_results.append(result)
                        executed.add(step_config.get("name") or step_config["skill"])

                total_iterations += 1
                if total_iterations > 100:
                    log("WARNING", "达到最大迭代次数，停止执行")
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
                "executed_steps": len(step_results),
                "success_count": success_count,
                "failed_count": len(step_results) - success_count,
                "steps": step_results,
                "context": {
                    name: {
                        "status": data["status"].value,
                        "has_data": bool(data.get("data")),
                        "artifacts_count": len(data.get("artifacts", [])),
                        "data": data.get("data"),
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
                data={
                    "success": False,
                    "error": str(e),
                    "stage": "study_pipeline",
                },
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )

    def _expand_pipeline(self, pipeline: List[Dict], context: Dict) -> List[Dict]:
        """展开循环步骤"""
        expanded = []
        for step in pipeline:
            foreach = step.get("foreach")
            if foreach:
                items_path = foreach.get("items", "")
                items = self._resolve_var_path(items_path, context) or []
                item_name = foreach.get("item_name", "item")

                if isinstance(items, list):
                    for i, item in enumerate(items):
                        new_step = {
                            **step,
                            "name": f"{step.get('name', step['skill'])}_{i}",
                        }
                        new_config = {**step.get("config", {})}
                        new_config[item_name] = item
                        new_config[f"{item_name}_index"] = i
                        new_step["config"] = new_config
                        new_step.pop("foreach", None)
                        expanded.append(new_step)
                else:
                    step_copy = {**step}
                    step_copy.pop("foreach", None)
                    expanded.append(step_copy)
            else:
                expanded.append(step)
        return expanded

    def _get_ready_steps(
        self,
        pipeline: List[Dict],
        executed: Set[str],
        context: Dict,
        continue_on_failure: bool,
    ) -> List[Dict]:
        """获取当前可执行的步骤"""
        ready = []
        for step in pipeline:
            step_name = step.get("name") or step["skill"]
            if step_name in executed:
                continue

            deps = step.get("depends_on", [])
            deps_satisfied = all(d in executed for d in deps)

            if not deps_satisfied:
                continue

            when = step.get("when")
            if when and not self._evaluate_condition(when, context):
                executed.add(step_name)
                continue

            if continue_on_failure:
                ready.append(step)
            else:
                failed_deps = [
                    d
                    for d in deps
                    if d in context["steps"]
                    and context["steps"][d]["status"] != SkillStatus.SUCCESS
                ]
                if failed_deps:
                    executed.add(step_name)
                    continue
                ready.append(step)

        return ready

    def _evaluate_condition(self, condition: str, context: Dict) -> bool:
        """评估条件表达式"""
        condition = condition.strip()

        success_pattern = r"steps\.(\w+)\.success"
        match = re.search(success_pattern, condition)
        if match:
            step_name = match.group(1)
            if step_name in context["steps"]:
                return context["steps"][step_name]["status"] == SkillStatus.SUCCESS
            return False

        failed_pattern = r"steps\.(\w+)\.failed"
        match = re.search(failed_pattern, condition)
        if match:
            step_name = match.group(1)
            if step_name in context["steps"]:
                return context["steps"][step_name]["status"] != SkillStatus.SUCCESS
            return False

        data_pattern = r"steps\.(\w+)\.data\.(\S+)\s*([<>=!]+)\s*(\S+)"
        match = re.search(data_pattern, condition)
        if match:
            step_name, field, operator, value = match.groups()
            if step_name in context["steps"]:
                data = context["steps"][step_name].get("data", {})
                field_value = self._get_nested(data, field)
                if field_value is not None:
                    try:
                        return eval(f"{field_value} {operator} {value}")
                    except:
                        pass
            return False

        return True

    def _get_nested(self, data: Dict, path: str) -> Any:
        """获取嵌套字典的值"""
        parts = path.split(".")
        val = data
        for p in parts:
            if isinstance(val, dict):
                val = val.get(p)
            else:
                return None
        return val

    def _execute_step(
        self,
        step_config: Dict,
        pipeline: List[Dict],
        context: Dict,
        log,
        parent_config: Dict = None,
    ) -> Dict:
        """执行单个步骤"""
        step_name = step_config.get("name") or step_config["skill"]
        skill_name = step_config["skill"]

        try:
            skill = get_skill(skill_name)
            if skill is None:
                raise ValueError(f"技能 '{skill_name}' 不存在")

            # Merge parent config (model, auth, etc.) with step config
            step_config_base = step_config.get("config", {}).copy()
            if parent_config:
                # Merge parent-level config into step config
                # Parent config takes lower priority - step config overrides
                merged_config = {}
                for key, value in parent_config.items():
                    if key not in ["skill", "pipeline"]:  # Exclude parent skill name and pipeline
                        merged_config[key] = value
                # Step config overrides parent config
                for key, value in step_config_base.items():
                    merged_config[key] = value
                step_config_final = self._resolve_config(merged_config, context)
            else:
                step_config_final = self._resolve_config(step_config_base, context)

            result = skill.run(step_config_final)

            context["steps"][step_name] = {
                "result": result,
                "status": result.status,
                "data": result.data,
                "artifacts": result.artifacts,
            }
            context["artifacts"].extend(result.artifacts)

            if result.status == SkillStatus.SUCCESS:
                log("INFO", f"✓ {step_name}: 成功")
                return {
                    "name": step_name,
                    "skill": skill_name,
                    "status": "success",
                    "duration": (result.end_time - result.start_time).total_seconds()
                    if result.end_time and result.start_time
                    else 0,
                    "data": result.data,
                }
            else:
                log("WARNING", f"✗ {step_name}: 失败 - {result.error}")
                return {
                    "name": step_name,
                    "skill": skill_name,
                    "status": "failed",
                    "error": result.error,
                    "data": result.data,
                }

        except Exception as e:
            log("ERROR", f"✗ {step_name}: 异常 - {e}")
            return {
                "name": step_name,
                "skill": skill_name,
                "status": "error",
                "error": str(e),
            }

    def _execute_parallel(
        self,
        steps: List[Dict],
        pipeline: List[Dict],
        context: Dict,
        max_workers: int,
        log,
        parent_config: Dict = None,
    ) -> List[Dict]:
        """并行执行多个步骤"""
        results = []

        def run_step(step_config):
            return self._execute_step(step_config, pipeline, context, log, parent_config)

        with ThreadPoolExecutor(max_workers=min(max_workers, len(steps))) as executor:
            futures = {executor.submit(run_step, s): s for s in steps}
            for future in as_completed(futures):
                results.append(future.result())

        return results

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
            f"**执行步骤数**: {pipeline_result.get('executed_steps', len(pipeline_result.get('steps', [])))}",
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

        lines.extend(["## 上下文数据", ""])

        for name, data in pipeline_result.get("context", {}).items():
            lines.append(f"### {name}")
            lines.append(f"- 状态: {data['status']}")
            lines.append(f"- 数据: {'有' if data['has_data'] else '无'}")
            lines.append(f"- 产物数: {data['artifacts_count']}")
            lines.append("")

        lines.extend(["## 结论", ""])

        if pipeline_result["failed_count"] == 0:
            lines.append("✅ 所有步骤执行成功")
        elif pipeline_result["success_count"] == 0:
            lines.append("❌ 所有步骤执行失败")
        else:
            lines.append(f"⚠️ {pipeline_result['failed_count']} 个步骤执行失败")

        return "\n".join(lines)
