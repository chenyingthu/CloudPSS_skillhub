from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ValidationIssue:
    severity: str = "warning"
    field: str = ""
    message: str = ""
    code: str | None = None


@dataclass
class ValidationResult:
    valid: bool = True
    issues: list[ValidationIssue] = field(default_factory=list)
    field: str = ""
    message: str = ""
    code: str | None = None

    def add_error(self, field: str, message: str, code: str | None = None):
        self.issues.append(
            ValidationIssue(severity="error", field=field, message=message, code=code)
        )
        self.valid = False

    def add_warning(self, field: str, message: str, code: str | None = None):
        self.issues.append(
            ValidationIssue(severity="warning", field=field, message=message, code=code)
        )

    @property
    def errors(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == "warning"]


class SkillOutputValidator:
    REQUIRED_BASE_FIELDS = ["skill_name", "success"]
    SKILL_TYPE_REQUIREMENTS = {
        "simulation": ["converged", "model_info", "summary"],
        "security": ["total_cases", "pass_rate"],
        "stability": ["stable", "stability_margin"],
        "parameter": ["scan_results", "optimal"],
        "processing": ["output_files", "processed_items"],
    }

    def __init__(self):
        self._category_map = self._build_category_map()

    def _build_category_map(self) -> dict[str, str]:
        return {
            "power_flow": "simulation",
            "emt_simulation": "simulation",
            "emt_fault_study": "simulation",
            "short_circuit": "simulation",
            "n1_security": "security",
            "n2_security": "security",
            "contingency_analysis": "security",
            "maintenance_security": "security",
            "voltage_stability": "stability",
            "transient_stability": "stability",
            "small_signal_stability": "stability",
            "frequency_response": "stability",
            "param_scan": "parameter",
            "orthogonal_sensitivity": "parameter",
            "result_compare": "processing",
            "visualize": "processing",
            "waveform_export": "processing",
            "loss_analysis": "processing",
        }

    def get_category(self, skill_name: str) -> str | None:
        return self._category_map.get(skill_name)

    def validate(self, result: Any) -> ValidationResult:
        validation = ValidationResult()
        if not hasattr(result, "to_dict"):
            validation.add_error(
                "result", "Result must have to_dict() method or be a dict"
            )
            return validation
        data = result.to_dict() if hasattr(result, "to_dict") else result
        for field_name in self.REQUIRED_BASE_FIELDS:
            if field_name not in data:
                validation.add_error(
                    field_name, f"Missing required field: {field_name}"
                )
        skill_name = data.get("skill_name")
        if skill_name:
            category = self.get_category(skill_name)
            if category and category in self.SKILL_TYPE_REQUIREMENTS:
                for req_field in self.SKILL_TYPE_REQUIREMENTS[category]:
                    if req_field not in data.get("data", {}):
                        validation.add_error(
                            f"data.{req_field}",
                            f"Missing {category} field: {req_field}",
                        )
        return validation

    def validate_failure_path(self, result: Any) -> ValidationResult:
        validation = ValidationResult()
        if not hasattr(result, "to_dict"):
            validation.add_error("result", "Result must have to_dict() method")
            return validation
        data = result.to_dict()
        if data.get("status") == "failed":
            if not data.get("error"):
                validation.add_error("error", "FAILED status must have error message")
            if data.get("success") is True:
                validation.add_error("success", "FAILED status must have success=False")
        if data.get("error") and data.get("status") != "failed":
            validation.add_warning("status", "Error present but status is not failed")
        return validation

    def validate_field_naming(self, data: dict[str, Any]) -> ValidationResult:
        validation = ValidationResult()
        camel_case_pattern = re.compile(r"[a-z][A-Z]")

        def check_dict(d: dict[str, Any], path: str = ""):
            for key, value in d.items():
                if camel_case_pattern.search(key):
                    validation.add_warning(
                        f"{path}.{key}" if path else key,
                        f"Field '{key}' appears to use camelCase. Use snake_case.",
                        code="NAMING001",
                    )
                if isinstance(value, dict):
                    check_dict(value, f"{path}.{key}" if path else key)
                elif isinstance(value, list):
                    for i, item in enumerate(value):
                        if isinstance(item, dict):
                            check_dict(
                                item, f"{path}.{key}[{i}]" if path else f"{key}[{i}]"
                            )

        check_dict(data)
        return validation
