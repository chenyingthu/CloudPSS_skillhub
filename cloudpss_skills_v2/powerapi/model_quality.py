"""Unified model quality diagnostics for cross-engine reuse.

The checks here are intentionally engine-agnostic and serializable. They are a
quality gate for adapter output, not a replacement for an AC power-flow solve.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

import numpy as np

from cloudpss_skills_v2.core.system_model import PowerSystemModel


SEVERITY_ORDER = {"pass": 0, "warning": 1, "fail": 2}
DEFAULT_LINE_X_PU = 0.01
PLACEHOLDER_LIMIT = 999999.0


def diagnose_unified_model(
    model: PowerSystemModel,
    *,
    include_matpower: bool = False,
) -> dict[str, Any]:
    """Return a serializable quality report for a unified model.

    Args:
        model: Unified model to inspect.
        include_matpower: If True, include static MATPOWER case-readiness checks.

    Returns:
        Dict with status, summary, findings, parameter quality, and readiness.
    """
    findings: list[dict[str, str]] = []
    summary = _model_summary(model)
    parameter_quality = _parameter_quality(model, findings)
    structural_quality = _structural_quality(model, findings)
    engine_readiness = {
        "pandapower": _pandapower_readiness(model, findings),
    }
    if include_matpower:
        engine_readiness["matpower"] = _matpower_readiness(model, findings)

    return {
        "status": _status_from_findings(findings),
        "summary": summary,
        "findings": findings,
        "parameter_quality": parameter_quality,
        "structural_quality": structural_quality,
        "engine_readiness": engine_readiness,
        "assumptions": [
            "Checks inspect unified model structure and parameters before engine-specific solving",
            "Default-like branch reactance is treated as a data-quality warning unless every branch is affected",
        ],
        "limitations": [
            "Does not prove that a downstream nonlinear solver will converge",
            "Cannot infer missing static parameters that were not preserved by the source adapter",
        ],
    }


def evaluate_matpower_cpf_output(
    model_quality: dict[str, Any],
    cpf_result: dict[str, Any],
    pv_curve: list[dict[str, Any]],
) -> dict[str, Any]:
    """Evaluate whether MATPOWER CPF output is usable for reported results."""
    findings: list[dict[str, str]] = []
    max_lambda = cpf_result.get("max_lambda")
    solver_success = bool(cpf_result.get("success", True))
    cpf = cpf_result.get("cpf", {}) if isinstance(cpf_result, dict) else {}

    if model_quality.get("status") == "fail":
        _add_finding(findings, "fail", "model_quality_failed", "Unified model failed pre-CPF checks")
    elif model_quality.get("status") == "warning":
        _add_finding(findings, "warning", "model_quality_warning", "Unified model has pre-CPF warnings")

    if not solver_success:
        _add_finding(findings, "warning", "solver_partial", "MATPOWER runcpf did not report full success")
    if max_lambda is None or not _is_finite_number(max_lambda):
        _add_finding(findings, "fail", "missing_max_lambda", "CPF output has no finite max loadability")
    elif float(max_lambda) <= 0:
        _add_finding(findings, "fail", "non_positive_max_lambda", "CPF max loadability is not positive")
    if not pv_curve:
        _add_finding(findings, "warning", "empty_pv_curve", "CPF output did not yield monitored PV curve points")

    lambda_trace = _first_present(cpf, "lam_c", "lambda", "lam")
    voltage_trace = _first_present(cpf, "V_c", "V")
    if lambda_trace is None:
        _add_finding(findings, "warning", "missing_lambda_trace", "CPF output is missing lambda trace")
    elif not _all_finite(lambda_trace):
        _add_finding(findings, "fail", "nonfinite_lambda_trace", "CPF lambda trace contains non-finite values")
    if voltage_trace is None:
        _add_finding(findings, "warning", "missing_voltage_trace", "CPF output is missing voltage trace")
    elif not _all_finite_abs(voltage_trace):
        _add_finding(findings, "fail", "nonfinite_voltage_trace", "CPF voltage trace contains non-finite values")

    return {
        "status": _status_from_findings(findings),
        "solver_success": solver_success,
        "has_finite_max_loadability": max_lambda is not None and _is_finite_number(max_lambda),
        "pv_curve_points": len(pv_curve),
        "findings": findings,
    }


def _model_summary(model: PowerSystemModel) -> dict[str, Any]:
    active_branches = [branch for branch in model.branches if branch.in_service]
    return {
        "name": model.name,
        "source_engine": model.source_engine,
        "base_mva": model.base_mva,
        "frequency_hz": model.frequency_hz,
        "bus_count": len(model.buses),
        "branch_count": len(model.branches),
        "active_branch_count": len(active_branches),
        "generator_count": len(model.generators),
        "active_generator_count": sum(1 for gen in model.generators if gen.in_service),
        "load_count": len(model.loads),
        "active_load_count": sum(1 for load in model.loads if load.in_service),
        "total_load_mw": model.total_load_mw(),
        "total_generation_mw": model.total_generation_mw(),
        "branch_type_counts": dict(Counter(branch.branch_type for branch in model.branches)),
        "bus_type_counts": dict(Counter(bus.bus_type for bus in model.buses)),
        "bus_base_kv_counts": dict(Counter(str(bus.base_kv) for bus in model.buses)),
    }


def _parameter_quality(
    model: PowerSystemModel,
    findings: list[dict[str, str]],
) -> dict[str, Any]:
    active_branches = [branch for branch in model.branches if branch.in_service]
    zero_impedance = []
    zero_x = []
    default_like_x = []
    missing_rate = []
    tap_issues = []

    for branch in active_branches:
        if abs(branch.r_pu) < 1e-12 and abs(branch.x_pu) < 1e-12:
            zero_impedance.append(branch.name)
        if abs(branch.x_pu) < 1e-12:
            zero_x.append(branch.name)
        if abs(branch.x_pu - DEFAULT_LINE_X_PU) < 1e-12:
            default_like_x.append(branch.name)
        if branch.rate_a_mva is None or branch.rate_a_mva <= 0:
            missing_rate.append(branch.name)
        if branch.is_transformer() and branch.tap_ratio <= 0:
            tap_issues.append(branch.name)

    if zero_impedance:
        _add_finding(
            findings,
            "fail",
            "zero_branch_impedance",
            f"{len(zero_impedance)} active branches have zero impedance",
        )
    elif zero_x:
        _add_finding(
            findings,
            "warning",
            "zero_branch_reactance",
            f"{len(zero_x)} active branches have zero reactance",
        )

    if default_like_x:
        severity = "fail" if active_branches and len(default_like_x) == len(active_branches) else "warning"
        _add_finding(
            findings,
            severity,
            "default_like_branch_reactance",
            f"{len(default_like_x)} active branches use x_pu={DEFAULT_LINE_X_PU}",
        )
    if tap_issues:
        _add_finding(findings, "fail", "invalid_transformer_tap", f"{len(tap_issues)} transformers have invalid tap ratios")

    placeholder_q_limits = [
        gen.name
        for gen in model.generators
        if gen.in_service
        and (abs(gen.q_max_mvar) >= PLACEHOLDER_LIMIT or abs(gen.q_min_mvar) >= PLACEHOLDER_LIMIT)
    ]
    placeholder_p_limits = [
        gen.name
        for gen in model.generators
        if gen.in_service
        and (abs(gen.p_max_mw) >= PLACEHOLDER_LIMIT or abs(gen.p_min_mw) >= PLACEHOLDER_LIMIT)
    ]
    missing_v_set = [
        gen.name
        for gen in model.generators
        if gen.in_service and gen.v_set_pu is None
    ]

    if placeholder_q_limits:
        _add_finding(
            findings,
            "warning",
            "placeholder_generator_q_limits",
            f"{len(placeholder_q_limits)} active generators use placeholder Q limits",
        )
    if placeholder_p_limits:
        _add_finding(
            findings,
            "warning",
            "placeholder_generator_p_limits",
            f"{len(placeholder_p_limits)} active generators use placeholder P limits",
        )
    if missing_v_set:
        _add_finding(
            findings,
            "warning",
            "missing_generator_voltage_setpoint",
            f"{len(missing_v_set)} active generators are missing voltage setpoints",
        )

    return {
        "zero_impedance_branch_count": len(zero_impedance),
        "zero_reactance_branch_count": len(zero_x),
        "default_like_x_pu_branch_count": len(default_like_x),
        "missing_rate_branch_count": len(missing_rate),
        "invalid_transformer_tap_count": len(tap_issues),
        "placeholder_generator_q_limit_count": len(placeholder_q_limits),
        "placeholder_generator_p_limit_count": len(placeholder_p_limits),
        "missing_generator_voltage_setpoint_count": len(missing_v_set),
    }


def _structural_quality(
    model: PowerSystemModel,
    findings: list[dict[str, str]],
) -> dict[str, Any]:
    physical = model.validate_physical(raise_on_error=False)
    for violation in physical:
        severity = "fail" if violation.get("severity") == "CRITICAL" else "warning"
        _add_finding(
            findings,
            severity,
            f"physical_{violation.get('type', 'violation')}",
            str(violation.get("message", "Physical validation issue")),
        )

    if not model.buses:
        _add_finding(findings, "fail", "empty_model", "Model contains no buses")
    if not any(branch.in_service for branch in model.branches):
        _add_finding(findings, "fail", "no_active_branches", "Model contains no active branches")
    if model.get_slack_bus() is None:
        _add_finding(findings, "fail", "missing_slack_bus", "Model has no slack/reference bus")
    if not any(gen.in_service for gen in model.generators):
        _add_finding(findings, "warning", "no_active_generators", "Model contains no active generators")
    if not any(load.in_service and (load.p_mw or load.q_mvar) for load in model.loads):
        _add_finding(findings, "warning", "no_active_loads", "Model contains no active nonzero loads")

    active_bus_ids = {bus.bus_id for bus in model.buses}
    isolated_bus_count = sum(
        1
        for bus_id in active_bus_ids
        if not any(
            branch.in_service and (branch.from_bus == bus_id or branch.to_bus == bus_id)
            for branch in model.branches
        )
    )

    return {
        "physical_violation_count": len(physical),
        "critical_physical_violation_count": sum(
            1 for item in physical if item.get("severity") == "CRITICAL"
        ),
        "isolated_bus_count": isolated_bus_count,
        "has_slack_bus": model.get_slack_bus() is not None,
        "has_active_generation": any(gen.in_service for gen in model.generators),
        "has_active_load": any(load.in_service and (load.p_mw or load.q_mvar) for load in model.loads),
    }


def _pandapower_readiness(
    model: PowerSystemModel,
    findings: list[dict[str, str]],
) -> dict[str, Any]:
    missing_bus_voltage = sum(1 for bus in model.buses if bus.base_kv <= 0)
    transformer_count = sum(1 for branch in model.branches if branch.branch_type == "TRANSFORMER")
    line_count = sum(1 for branch in model.branches if branch.branch_type == "LINE")
    ready = bool(model.buses and any(branch.in_service for branch in model.branches) and missing_bus_voltage == 0)
    if not ready:
        _add_finding(findings, "fail", "pandapower_not_convertible", "Model lacks required pandapower conversion inputs")
    return {
        "convertible": ready,
        "line_count": line_count,
        "transformer_count": transformer_count,
        "frequency_hz": model.frequency_hz,
    }


def _matpower_readiness(
    model: PowerSystemModel,
    findings: list[dict[str, str]],
) -> dict[str, Any]:
    from cloudpss_skills_v2.powerapi.adapters.matpower_cpf import MatpowerCPFAdapter

    try:
        mpc = MatpowerCPFAdapter().to_mpc(model)
    except Exception as exc:
        _add_finding(findings, "fail", "matpower_conversion_error", f"MATPOWER conversion failed: {exc}")
        return {"convertible": False, "error": str(exc)}

    bus = np.asarray(mpc.get("bus", []))
    gen = np.asarray(mpc.get("gen", []))
    branch = np.asarray(mpc.get("branch", []))
    convertible = bool(bus.size and gen.size and branch.size)
    if not convertible:
        _add_finding(findings, "fail", "matpower_empty_case", "MATPOWER case is missing bus/gen/branch rows")
    if bus.size and not np.all(np.isfinite(bus)):
        _add_finding(findings, "fail", "matpower_nonfinite_bus", "MATPOWER bus matrix contains non-finite values")
    if gen.size and not np.all(np.isfinite(gen)):
        _add_finding(findings, "fail", "matpower_nonfinite_gen", "MATPOWER gen matrix contains non-finite values")
    if branch.size and not np.all(np.isfinite(branch)):
        _add_finding(findings, "fail", "matpower_nonfinite_branch", "MATPOWER branch matrix contains non-finite values")

    slack_count = int(np.sum(bus[:, 1] == 3)) if bus.size else 0
    if slack_count == 0:
        _add_finding(findings, "fail", "matpower_missing_slack", "MATPOWER case has no reference bus")

    return {
        "convertible": convertible,
        "bus_shape": list(bus.shape),
        "gen_shape": list(gen.shape),
        "branch_shape": list(branch.shape),
        "slack_bus_count": slack_count,
        "total_pd_mw": float(np.sum(bus[:, 2])) if bus.size else 0.0,
        "total_qd_mvar": float(np.sum(bus[:, 3])) if bus.size else 0.0,
    }


def _add_finding(
    findings: list[dict[str, str]],
    severity: str,
    code: str,
    message: str,
) -> None:
    findings.append({"severity": severity, "code": code, "message": message})


def _status_from_findings(findings: list[dict[str, str]]) -> str:
    status = "pass"
    for finding in findings:
        severity = finding.get("severity", "pass")
        if SEVERITY_ORDER.get(severity, 0) > SEVERITY_ORDER[status]:
            status = severity
    return status


def _first_present(mapping: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = mapping.get(key)
        if value is not None:
            return value
    return None


def _is_finite_number(value: Any) -> bool:
    try:
        return bool(np.isfinite(float(value)))
    except (TypeError, ValueError):
        return False


def _all_finite(value: Any) -> bool:
    array = np.asarray(value)
    return bool(array.size and np.all(np.isfinite(array)))


def _all_finite_abs(value: Any) -> bool:
    array = np.asarray(value)
    return bool(array.size and np.all(np.isfinite(np.abs(array))))


__all__ = ["diagnose_unified_model", "evaluate_matpower_cpf_output"]
