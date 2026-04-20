from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable
from cloudpss_skills_v2.core.skill_result import SkillResult, SkillStatus


class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class StepResult:
    step_name: str = ""
    status: StepStatus = StepStatus.PENDING
    output: Any = None
    error: str | None = None
    duration_seconds: float | None = None

    @property
    def is_success(self) -> bool:
        return self.status == StepStatus.SUCCESS

    def to_dict(self) -> dict[str, Any]:
        d = {
            "step_name": self.step_name,
            "status": self.status.value,
            "error": self.error,
            "duration_seconds": self.duration_seconds,
        }
        if isinstance(self.output, SkillResult):
            d["output"] = self.output.to_dict()
        elif isinstance(self.output, dict):
            d["output"] = self.output
        return d


@dataclass
class WorkflowStep:
    name: str = ""
    handler: Callable[..., Any] = None
    config: dict[str, Any] = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)
    optional: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            k: getattr(self, k) for k in ("name", "config", "depends_on", "optional")
        }


@dataclass
class ConditionalBranch:
    condition: Callable[[dict[str, Any]], bool] = None
    if_true_step: WorkflowStep = None
    if_false_step: WorkflowStep | None = None

    def evaluate(self, context: dict[str, Any]) -> WorkflowStep:
        if self.condition(context):
            return self.if_true_step
        return self.if_false_step or WorkflowStep(
            name="__noop__", handler=lambda _: None, optional=True
        )


@dataclass
class LoopConfig:
    max_iterations: int = 10
    convergence_check: Callable[[dict[str, Any]], bool] | None = None
    iteration_param: str = "iteration"
    value_param: str = "value"


@dataclass
class WorkflowResult:
    name: str = ""
    steps: list[StepResult] = field(default_factory=list)
    status: StepStatus = StepStatus.PENDING
    context: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    @property
    def is_success(self) -> bool:
        return self.status == StepStatus.SUCCESS

    @property
    def failed_steps(self) -> list[StepResult]:
        return [s for s in self.steps if s.status == StepStatus.FAILED]

    @property
    def successful_steps(self) -> list[StepResult]:
        return [s for s in self.steps if s.status == StepStatus.SUCCESS]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status.value,
            "steps": [s.to_dict() for s in self.steps],
            "failed_count": len(self.failed_steps),
            "success_count": len(self.successful_steps),
            "error": self.error,
        }


class Pipeline:
    def __init__(self, name: str = "pipeline"):
        self.name = name
        self._steps = []
        self._loop_config = None
        self._loop_body = []

    def add_step(
        self,
        name: str,
        handler: Callable[..., Any],
        config: dict[str, Any] | None = None,
        depends_on: list[str] | None = None,
        optional: bool = False,
    ) -> Pipeline:
        self._steps.append(
            WorkflowStep(
                name=name,
                handler=handler,
                config=config or {},
                depends_on=depends_on or [],
                optional=optional,
            )
        )
        return self

    def add_conditional(
        self,
        condition: Callable[[dict[str, Any]], bool],
        if_true_step: WorkflowStep,
        if_false_step: WorkflowStep | None = None,
    ) -> Pipeline:
        self._steps.append(
            ConditionalBranch(
                condition=condition,
                if_true_step=if_true_step,
                if_false_step=if_false_step,
            )
        )
        return self

    def add_loop(
        self, body_steps: list[WorkflowStep], config: LoopConfig | None = None
    ) -> Pipeline:
        self._loop_config = config or LoopConfig()
        self._loop_body = body_steps
        return self

    def run(self, initial_context: dict[str, Any] | None = None) -> WorkflowResult:
        import time

        context = dict(initial_context or {})
        results = []
        step_outputs = {}
        completed_step_names = set()

        for item in self._steps:
            if isinstance(item, ConditionalBranch):
                step = item.evaluate(context)
                if step.name == "__noop__":
                    results.append(
                        StepResult(step_name="__noop__", status=StepStatus.SKIPPED)
                    )
                    continue
            else:
                step = item

            for dep in step.depends_on:
                if dep not in completed_step_names:
                    if step.optional:
                        results.append(
                            StepResult(
                                step_name=step.name,
                                status=StepStatus.SKIPPED,
                                error=f"Dependency '{dep}' not completed",
                            )
                        )
                        break
                    else:
                        return WorkflowResult(
                            name=self.name,
                            steps=results,
                            status=StepStatus.FAILED,
                            error=f"Required dependency '{dep}' not completed before step '{step.name}'",
                        )
            else:
                start = time.monotonic()
                try:
                    merged_config = {**step.config, **context}
                    output = step.handler(merged_config)
                    elapsed = time.monotonic() - start

                    if isinstance(output, SkillResult):
                        context.update(
                            output.data if isinstance(output.data, dict) else {}
                        )
                    elif isinstance(output, dict):
                        context.update(output)

                    step_outputs[step.name] = output
                    completed_step_names.add(step.name)
                    results.append(
                        StepResult(
                            step_name=step.name,
                            status=StepStatus.SUCCESS,
                            output=output,
                            duration_seconds=elapsed,
                        )
                    )
                except Exception as e:
                    elapsed = time.monotonic() - start
                    results.append(
                        StepResult(
                            step_name=step.name,
                            status=StepStatus.FAILED,
                            error=str(e),
                            duration_seconds=elapsed,
                        )
                    )
                    if not step.optional:
                        return WorkflowResult(
                            name=self.name,
                            steps=results,
                            status=StepStatus.FAILED,
                            error=str(e),
                            context=context,
                        )

        if self._loop_config and self._loop_body:
            loop_result = self._run_loop(context, step_outputs, completed_step_names)
            results.extend(loop_result.steps)
            if loop_result.status == StepStatus.FAILED:
                return WorkflowResult(
                    name=self.name,
                    steps=results,
                    status=StepStatus.FAILED,
                    error=loop_result.error,
                    context=context,
                )

        return WorkflowResult(
            name=self.name, steps=results, status=StepStatus.SUCCESS, context=context
        )

    def _run_loop(
        self,
        context: dict[str, Any],
        step_outputs: dict[str, Any],
        completed_step_names: set[str],
    ) -> WorkflowResult:
        import time

        results = []
        cfg = self._loop_config

        for iteration in range(cfg.max_iterations):
            context[cfg.iteration_param] = iteration

            for step in self._loop_body:
                start = time.monotonic()
                try:
                    merged_config = {**step.config, **context}
                    output = step.handler(merged_config)
                    elapsed = time.monotonic() - start
                    step_outputs[step.name] = output

                    if isinstance(output, SkillResult):
                        context.update(
                            output.data if isinstance(output.data, dict) else {}
                        )
                    elif isinstance(output, dict):
                        context.update(output)

                    results.append(
                        StepResult(
                            step_name=f"_iter_{iteration}_{step.name}",
                            status=StepStatus.SUCCESS,
                            output=output,
                            duration_seconds=elapsed,
                        )
                    )
                except Exception as e:
                    elapsed = time.monotonic() - start
                    results.append(
                        StepResult(
                            step_name=f"_iter_{iteration}_{step.name}",
                            status=StepStatus.FAILED,
                            error=f"Loop iteration {iteration}, step '{step.name}' failed: {e}",
                            duration_seconds=elapsed,
                        )
                    )
                    return WorkflowResult(
                        name=f"{self.name}_loop_iter_{iteration}",
                        steps=results,
                        status=StepStatus.FAILED,
                        error=str(e),
                        context=context,
                    )

            if cfg.convergence_check and cfg.convergence_check(context):
                context["__convergence__"] = {"converged_at_iteration": iteration}
                results.append(
                    StepResult(
                        step_name=f"_loop_iter_{iteration}",
                        status=StepStatus.SUCCESS,
                        output={"converged": True, "iteration": iteration},
                    )
                )
                return WorkflowResult(
                    name=f"{self.name}_loop",
                    steps=results,
                    status=StepStatus.SUCCESS,
                    context=context,
                )

        results.append(
            StepResult(
                step_name="_loop",
                status=StepStatus.FAILED,
                error=f"Loop did not converge after {cfg.max_iterations} iterations",
            )
        )
        return WorkflowResult(
            name=f"{self.name}_loop",
            steps=results,
            status=StepStatus.FAILED,
            context=context,
        )


__all__ = [
    "StepStatus",
    "StepResult",
    "WorkflowStep",
    "ConditionalBranch",
    "LoopConfig",
    "WorkflowResult",
    "Pipeline",
]
