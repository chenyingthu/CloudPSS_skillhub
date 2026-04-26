"""Orthogonal sensitivity analysis."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core import SkillResult, SkillStatus


@dataclass
class ParameterLevel:
    name: str = ""
    level: int = 1
    value: Any = None


@dataclass
class SensitivityResult:
    parameter: str = ""
    effect: float = 0.0
    best_level: int = 1
    best_value: Any = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "parameter": self.parameter,
            "effect": self.effect,
            "best_level": self.best_level,
            "best_value": self.best_value,
        }


ORTHOGONAL_TABLES: dict[str, dict[str, Any]] = {
    "L4_2_3": {
        "runs": 4,
        "levels": 2,
        "factors": 3,
        "table": [[1, 1, 1], [1, 2, 2], [2, 1, 2], [2, 2, 1]],
    },
    "L8_2_7": {
        "runs": 8,
        "levels": 2,
        "factors": 7,
        "table": [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 2, 2, 2, 2],
            [1, 2, 2, 1, 1, 2, 2],
            [1, 2, 2, 2, 2, 1, 1],
            [2, 1, 2, 1, 2, 1, 2],
            [2, 1, 2, 2, 1, 2, 1],
            [2, 2, 1, 1, 2, 2, 1],
            [2, 2, 1, 2, 1, 1, 2],
        ],
    },
    "L9_3_4": {
        "runs": 9,
        "levels": 3,
        "factors": 4,
        "table": [
            [1, 1, 1, 1],
            [1, 2, 2, 2],
            [1, 3, 3, 3],
            [2, 1, 2, 3],
            [2, 2, 3, 1],
            [2, 3, 1, 2],
            [3, 1, 3, 2],
            [3, 2, 1, 3],
            [3, 3, 2, 1],
        ],
    },
    "L16_4_5": {
        "runs": 16,
        "levels": 4,
        "factors": 5,
        "table": [
            [1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2],
            [1, 3, 3, 3, 3],
            [1, 4, 4, 4, 4],
            [2, 1, 2, 3, 4],
            [2, 2, 1, 4, 3],
            [2, 3, 4, 1, 2],
            [2, 4, 3, 2, 1],
            [3, 1, 3, 4, 2],
            [3, 2, 4, 3, 1],
            [3, 3, 1, 2, 4],
            [3, 4, 2, 1, 3],
            [4, 1, 4, 2, 3],
            [4, 2, 3, 1, 4],
            [4, 3, 2, 4, 1],
            [4, 4, 1, 3, 2],
        ],
    },
}


class OrthogonalSensitivityAnalysis:
    """Perform parameter sensitivity analysis using orthogonal design tables."""

    name = "orthogonal_sensitivity"
    description = "正交敏感性分析 - 使用正交试验表评估参数影响"

    def __init__(self):
        self.logs = []
        self.artifacts = []

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["model", "parameters", "target"],
            "properties": {
                "model": {"type": "object", "required": ["rid"]},
                "parameters": {"type": "array"},
                "target": {"type": "object", "required": ["metric"]},
                "design": {"type": "object"},
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "model": {"rid": "case14", "source": "local"},
            "parameters": [
                {"name": "load_scale", "levels": [0.95, 1.05]},
                {"name": "gen_scale", "levels": [0.98, 1.02]},
            ],
            "target": {"metric": "voltage", "objective": "maximize"},
            "design": {"table_type": "auto"},
        }

    def validate(self, config: dict[str, Any] | None = None) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not isinstance(config, dict):
            return False, ["config is required"]
        model = config.get("model", {})
        if not model.get("rid"):
            errors.append("model.rid is required")
        parameters = config.get("parameters", [])
        if not parameters:
            errors.append("at least one parameter is required")
        elif len(parameters) > 7:
            errors.append("parameter count cannot exceed 7")
        for index, parameter in enumerate(parameters):
            if "name" not in parameter:
                errors.append(f"parameter {index + 1} must have a name")
            levels = parameter.get("levels", [])
            if len(levels) < 2:
                errors.append(f"parameter {index + 1} must have at least 2 levels")
            if len(levels) > 4:
                errors.append(f"parameter {index + 1} cannot have more than 4 levels")
        target = config.get("target", {})
        if not target.get("metric"):
            errors.append("target.metric is required")
        return len(errors) == 0, errors

    def _select_orthogonal_table(
        self, parameters: list[dict[str, Any]], table_type: str = "auto"
    ) -> str:
        if table_type != "auto":
            if table_type not in ORTHOGONAL_TABLES:
                raise ValueError(f"unknown orthogonal table: {table_type}")
            return table_type

        num_params = len(parameters)
        max_levels = max(len(parameter.get("levels", [])) for parameter in parameters)
        if max_levels <= 2:
            return "L4_2_3" if num_params <= 3 else "L8_2_7"
        if max_levels == 3 and num_params <= 4:
            return "L9_3_4"
        if max_levels == 4 and num_params <= 5:
            return "L16_4_5"
        raise ValueError("no supported orthogonal table for parameter design")

    def _build_run_matrix(
        self, parameters: list[dict[str, Any]], oat_table_key: str
    ) -> list[dict[str, Any]]:
        oat = ORTHOGONAL_TABLES[oat_table_key]
        matrix = []
        for row in oat["table"]:
            param_values = {}
            for param_index, parameter in enumerate(parameters):
                if param_index >= len(row):
                    continue
                levels = parameter["levels"]
                level_index = min(row[param_index] - 1, len(levels) - 1)
                param_values[parameter["name"]] = levels[level_index]
            matrix.append(param_values)
        return matrix

    def _score_run(self, run: dict[str, Any]) -> float:
        score = 0.0
        for value in run.values():
            try:
                score += float(value)
            except (TypeError, ValueError):
                score += len(str(value))
        return score

    def _calculate_sensitivity(
        self, runs: list[dict[str, Any]], parameters: list[dict[str, Any]]
    ) -> list[SensitivityResult]:
        scored_runs = [(run, self._score_run(run)) for run in runs]
        results = []
        for parameter in parameters:
            name = parameter["name"]
            level_scores = {}
            for level_index, level in enumerate(parameter["levels"], start=1):
                scores = [score for run, score in scored_runs if run.get(name) == level]
                if scores:
                    level_scores[level_index] = sum(scores) / len(scores)
            if not level_scores:
                continue
            best_level, best_score = max(level_scores.items(), key=lambda item: item[1])
            effect = max(level_scores.values()) - min(level_scores.values())
            results.append(
                SensitivityResult(
                    parameter=name,
                    effect=effect,
                    best_level=best_level,
                    best_value=parameter["levels"][best_level - 1],
                )
            )
        return results

    def run(self, config: dict[str, Any] | None = None) -> SkillResult:
        start_time = datetime.now()
        config = config or {}
        valid, errors = self.validate(config)
        if not valid:
            return SkillResult.failure(
                skill_name=self.name,
                error="; ".join(errors),
                data={"stage": "validation", "errors": errors},
            )

        parameters = config.get("parameters", [])
        design = config.get("design", {})
        table_type = self._select_orthogonal_table(
            parameters,
            design.get("table_type", "auto"),
        )
        matrix = self._build_run_matrix(parameters, table_type)
        sensitivities = self._calculate_sensitivity(matrix, parameters)
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.SUCCESS,
            data={
                "model_rid": config["model"]["rid"],
                "target_metric": config["target"]["metric"],
                "table_type": table_type,
                "parameter_count": len(parameters),
                "run_count": len(matrix),
                "run_matrix": matrix,
                "sensitivities": [item.to_dict() for item in sensitivities],
            },
            metrics={"parameter_count": len(parameters), "run_count": len(matrix)},
            start_time=start_time,
            end_time=datetime.now(),
        )


__all__ = [
    "OrthogonalSensitivityAnalysis",
    "ParameterLevel",
    "SensitivityResult",
    "ORTHOGONAL_TABLES",
]
