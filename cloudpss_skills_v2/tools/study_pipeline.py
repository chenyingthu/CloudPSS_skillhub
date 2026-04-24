"""Study Pipeline Skill v2."""

from __future__ import annotations

import ast
import copy
import importlib
import re
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core import Artifact, LogEntry, SkillResult, SkillStatus


class StudyPipelineTool:
    name = "study_pipeline"

    _VAR_PATTERN = re.compile(r"\$\{([^}]+)\}")
    _SKILL_CLASS_PATHS = {
        "study_pipeline": "cloudpss_skills_v2.tools.study_pipeline.StudyPipelineTool",
        "waveform_export": "cloudpss_skills_v2.tools.waveform_export.WaveformExportTool",
        "comtrade_export": "cloudpss_skills_v2.tools.comtrade_export.ComtradeExportTool",
        "hdf5_export": "cloudpss_skills_v2.tools.hdf5_export.HDF5ExportTool",
        "visualize": "cloudpss_skills_v2.tools.visualize.VisualizeTool",
        "compare_visualization": "cloudpss_skills_v2.tools.compare_visualization.CompareVisualizationTool",
        "result_compare": "cloudpss_skills_v2.tools.result_compare.ResultCompareTool",
        "report_generator": "cloudpss_skills_v2.tools.report_generator.ReportGeneratorTool",
        "auto_channel_setup": "cloudpss_skills_v2.tools.auto_channel_setup.AutoChannelSetupTool",
        "auto_loop_breaker": "cloudpss_skills_v2.tools.auto_loop_breaker.AutoLoopBreakerTool",
        "topology_check": "cloudpss_skills_v2.tools.topology_check.TopologyCheckTool",
        "model_builder": "cloudpss_skills_v2.tools.model_builder.ModelBuilderTool",
        "model_hub": "cloudpss_skills_v2.tools.model_hub.ModelHubTool",
        "model_parameter_extractor": "cloudpss_skills_v2.tools.model_parameter_extractor.ModelParameterExtractorTool",
        "component_catalog": "cloudpss_skills_v2.tools.component_catalog.ComponentCatalogTool",
        "batch_task_manager": "cloudpss_skills_v2.tools.batch_task_manager.BatchTaskManagerTool",
        "config_batch_runner": "cloudpss_skills_v2.tools.config_batch_runner.ConfigBatchRunnerTool",
        "power_flow": "cloudpss_skills_v2.powerskill.presets.power_flow.PowerFlowPreset",
        "emt_simulation": "cloudpss_skills_v2.powerskill.presets.emt_simulation.EMTPreset",
        "n1_security": "cloudpss_skills_v2.poweranalysis.n1_security.N1SecurityAnalysis",
    }

    def __init__(self):
        self.logs = []
        self.artifacts = []

    def _log(self, level: str, message: str, context: dict[str, Any] | None = None) -> None:
        self.logs.append(
            LogEntry(
                timestamp=datetime.now(),
                level=level.lower(),
                message=message,
                context=context,
            )
        )

    def validate(self, config):
        errors = []
        if config is None:
            return True, []

        pipeline = config.get("pipeline", config.get("stages", []))
        if pipeline is None:
            pipeline = []

        if not isinstance(pipeline, list):
            errors.append("pipeline must be a list")
            return (False, errors)

        names = set()
        for index, step in enumerate(pipeline):
            if not isinstance(step, dict):
                errors.append(f"pipeline[{index}] must be an object")
                continue

            if "skill" not in step:
                errors.append(f"pipeline[{index}] must define skill")

            name = step.get("name")
            if name:
                if name in names:
                    errors.append(f"duplicate step name: {name}")
                names.add(name)

            if "for_each" in step:
                errors.append(f"pipeline[{index}] uses unsupported feature for_each")
            if "pipeline" in step:
                errors.append(f"pipeline[{index}] uses unsupported nested pipeline")

        return (len(errors) == 0, errors)

    def _expand_pipeline(self, pipeline, context):
        expanded = []
        for index, raw_step in enumerate(pipeline or []):
            if "for_each" in raw_step:
                raise ValueError("for_each loop is not supported in this phase")
            if "pipeline" in raw_step:
                raise ValueError("nested pipeline is not supported in this phase")

            step = copy.deepcopy(raw_step)
            step.setdefault("name", f"step_{index + 1}")
            step.setdefault("config", {})
            expanded.append(step)
        return expanded

    def _get_ready_steps(self, pipeline, executed, context, continue_on_failure):
        executed_names = set(executed)
        for step in pipeline:
            if step["name"] in executed_names:
                continue

            condition = step.get("if")
            if condition and not self._evaluate_condition(condition, context):
                continue

            return [step]
        return []

    def _evaluate_condition(self, condition, context):
        if condition is None:
            return True
        if isinstance(condition, bool):
            return condition

        if not isinstance(condition, str):
            return bool(condition)

        def replace_var(match: re.Match[str]) -> str:
            resolved = self._resolve_var_path(match.group(1).strip(), context)
            return repr(resolved)

        expression = self._VAR_PATTERN.sub(replace_var, condition).strip()
        if not expression:
            return False

        try:
            parsed = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise ValueError(f"invalid condition: {condition}") from exc

        return bool(self._eval_ast_node(parsed.body))

    def _eval_ast_node(self, node: ast.AST) -> Any:
        if isinstance(node, ast.Constant):
            return node.value

        if isinstance(node, ast.List):
            return [self._eval_ast_node(element) for element in node.elts]

        if isinstance(node, ast.Tuple):
            return tuple(self._eval_ast_node(element) for element in node.elts)

        if isinstance(node, ast.Dict):
            result = {}
            for key, value in zip(node.keys, node.values):
                if key is None:
                    raise ValueError("unsupported condition expression")
                result[self._eval_ast_node(key)] = self._eval_ast_node(value)
            return result

        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return not self._eval_ast_node(node.operand)

        if isinstance(node, ast.BoolOp):
            values = [self._eval_ast_node(value) for value in node.values]
            if isinstance(node.op, ast.And):
                return all(values)
            if isinstance(node.op, ast.Or):
                return any(values)

        if isinstance(node, ast.Compare):
            left = self._eval_ast_node(node.left)
            for operator, comparator_node in zip(node.ops, node.comparators):
                right = self._eval_ast_node(comparator_node)
                if isinstance(operator, ast.Eq):
                    ok = left == right
                elif isinstance(operator, ast.NotEq):
                    ok = left != right
                elif isinstance(operator, ast.Gt):
                    ok = left > right
                elif isinstance(operator, ast.GtE):
                    ok = left >= right
                elif isinstance(operator, ast.Lt):
                    ok = left < right
                elif isinstance(operator, ast.LtE):
                    ok = left <= right
                elif isinstance(operator, ast.In):
                    ok = left in right
                elif isinstance(operator, ast.NotIn):
                    ok = left not in right
                else:
                    raise ValueError("unsupported comparison operator")

                if not ok:
                    return False
                left = right

            return True

        raise ValueError("unsupported condition expression")

    def _resolve_var_path(self, var_path, context):
        if not var_path:
            return None

        current: Any = context
        for part in var_path.split("."):
            if isinstance(current, SkillResult):
                current = {
                    "skill_name": current.skill_name,
                    "status": current.status.value,
                    "result": current.data,
                    "error": current.error,
                    "metrics": current.metrics,
                }

            if isinstance(current, dict):
                if part not in current:
                    return None
                current = current[part]
            elif isinstance(current, list):
                try:
                    current = current[int(part)]
                except (ValueError, IndexError):
                    return None
            else:
                if not hasattr(current, part):
                    return None
                current = getattr(current, part)

        return current

    def _resolve_config(self, config, context):
        if isinstance(config, dict):
            return {
                key: self._resolve_config(value, context)
                for key, value in config.items()
            }
        if isinstance(config, list):
            return [self._resolve_config(item, context) for item in config]
        if isinstance(config, tuple):
            return tuple(self._resolve_config(item, context) for item in config)
        if isinstance(config, str):
            return self._resolve_string(config, context)
        return config

    def _resolve_string(self, value, context):
        if not isinstance(value, str):
            return value

        full_match = self._VAR_PATTERN.fullmatch(value)
        if full_match:
            return self._resolve_var_path(full_match.group(1).strip(), context)

        def replace_var(match: re.Match[str]) -> str:
            resolved = self._resolve_var_path(match.group(1).strip(), context)
            return "" if resolved is None else str(resolved)

        return self._VAR_PATTERN.sub(replace_var, value)

    def _load_skill(self, skill_name: str):
        class_path = self._SKILL_CLASS_PATHS.get(skill_name)
        if class_path:
            module_name, class_name = class_path.rsplit(".", 1)
            module = importlib.import_module(module_name)
            return getattr(module, class_name)()
        raise ValueError(f"unknown skill: {skill_name}")

    def _result_status(self, result: SkillResult) -> str:
        status = result.status
        if isinstance(status, SkillStatus):
            return status.value
        return str(status)

    def _store_step_context(self, step_name: str, skill_name: str, result: SkillResult, context: dict[str, Any]) -> dict[str, Any]:
        step_context = {
            "skill": skill_name,
            "status": self._result_status(result),
            "result": result.data,
            "error": result.error,
            "metrics": result.metrics,
        }
        context[step_name] = step_context
        return step_context

    def run(self, config):
        start_time = datetime.now()
        self.logs = []
        self.artifacts = []

        if config is None:
            config = {}

        valid, errors = self.validate(config)
        if not valid:
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error="; ".join(errors),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )

        try:
            pipeline = config.get("pipeline", config.get("stages", []))
            context = {
                "input": copy.deepcopy(config.get("input", {})),
                "context": copy.deepcopy(config.get("context", {})),
            }
            continue_on_failure = config.get("continue_on_failure", False)
            expanded_pipeline = self._expand_pipeline(pipeline, context)

            executed = []
            step_results = []
            failures = []
            skipped = []

            while len(executed) < len(expanded_pipeline):
                ready_steps = self._get_ready_steps(
                    expanded_pipeline,
                    executed,
                    context,
                    continue_on_failure,
                )

                if not ready_steps:
                    for step in expanded_pipeline:
                        if step["name"] in executed:
                            continue
                        if step.get("if") and not self._evaluate_condition(step["if"], context):
                            step_context = {
                                "skill": step.get("skill"),
                                "status": "skipped",
                                "result": None,
                                "error": None,
                                "metrics": {},
                            }
                            context[step["name"]] = step_context
                            step_results.append({"name": step["name"], **step_context})
                            skipped.append(step["name"])
                            executed.append(step["name"])
                            self._log("info", f"Skipped step: {step['name']}")
                            break
                    else:
                        break
                    continue

                step = ready_steps[0]
                step_name = step["name"]
                skill_name = step["skill"]
                resolved_config = self._resolve_config(step.get("config", {}), context)
                self._log("info", f"Executing step: {step_name}", {"skill": skill_name})

                try:
                    skill = self._load_skill(skill_name)
                    result = skill.run(resolved_config)
                except Exception as exc:
                    result = SkillResult(
                        skill_name=skill_name,
                        status=SkillStatus.FAILED,
                        error=str(exc),
                        data={"success": False, "error": str(exc)},
                        start_time=datetime.now(),
                        end_time=datetime.now(),
                    )

                step_context = self._store_step_context(step_name, skill_name, result, context)
                step_results.append({"name": step_name, **step_context})
                executed.append(step_name)
                self.logs.extend(result.logs)
                self.artifacts.extend(result.artifacts)

                if step_context["status"] != SkillStatus.SUCCESS.value:
                    failures.append({"step": step_name, "error": result.error})
                    self._log("error", f"Step failed: {step_name}", {"error": result.error})
                    if not continue_on_failure:
                        return SkillResult(
                            skill_name=self.name,
                            status=SkillStatus.FAILED,
                            data={
                                "steps": step_results,
                                "context": context,
                                "failed_step": step_name,
                            },
                            artifacts=self.artifacts,
                            logs=self.logs,
                            error=result.error or f"step {step_name} failed",
                            start_time=start_time,
                            end_time=datetime.now(),
                        )

            final_status = SkillStatus.SUCCESS if not failures else SkillStatus.FAILED
            final_error = None if not failures else "; ".join(
                f"{item['step']}: {item['error'] or 'failed'}" for item in failures
            )

            return SkillResult(
                skill_name=self.name,
                status=final_status,
                data={
                    "steps": step_results,
                    "context": context,
                    "executed_steps": executed,
                    "skipped_steps": skipped,
                },
                artifacts=self.artifacts,
                logs=self.logs,
                error=final_error,
                metrics={
                    "total_steps": len(expanded_pipeline),
                    "executed_steps": len(executed),
                    "failed_steps": len(failures),
                    "skipped_steps": len(skipped),
                },
                start_time=start_time,
                end_time=datetime.now(),
            )
        except Exception as exc:
            self._log("error", str(exc))
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(exc),
                logs=self.logs,
                artifacts=self.artifacts,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["StudyPipelineTool"]
