"""Strict integration matrix for registered v2 skills.

These tests intentionally avoid mocks. Each registered skill is instantiated
from the registry and run with a bounded real local configuration. Pandapower
cases and inline data count as integration inputs; import-only checks do not.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import socket
from typing import Any
from urllib.parse import urlparse

import pytest

import cloudpss_skills_v2  # noqa: F401 - imports register all skills
from cloudpss_skills_v2 import SkillRegistry
from cloudpss_skills_v2.core import SkillResult, SkillStatus


TMP_ROOT = Path("/tmp/cloudpss_skill_matrix")
LOCAL_CLOUDPSS_BASE_URL = "http://166.111.60.76:50001"
LIVE_CLOUDPSS_SKILLS = {"emt_n1_screening", "emt_simulation"}


def _waveform_data() -> dict[str, Any]:
    return {
        "time": [0.0, 0.01, 0.02, 0.03],
        "channels": {
            "Va": [0.0, 0.5, 1.0, 0.5],
            "Ia": [0.0, 1.0, 0.0, -1.0],
        },
    }


def _inline_model() -> dict[str, Any]:
    return {
        "rid": "inline/demo",
        "source": "inline",
        "components": [
            {
                "key": "bus_1",
                "type": "bus_3p",
                "rid": "model/CloudPSS/_newBus_3p",
                "name": "Bus 1",
                "args": {"voltage": 110},
                "pins": {"p": "P1"},
            },
            {
                "key": "line_1",
                "type": "line_3p",
                "rid": "model/CloudPSS/_newLine_3p",
                "name": "Line 1",
                "args": {"rating": 100},
                "pins": {"p": "P1", "n": "P2"},
            },
        ],
    }


def _base_pf() -> dict[str, Any]:
    return {"engine": "pandapower", "model": {"rid": "case14", "source": "local"}}


def _local_auth() -> dict[str, str]:
    return {"token": "local-pandapower-token"}


def _live_auth() -> dict[str, str]:
    token_path = Path(".cloudpss_token_internal")
    return {
        "token": token_path.read_text().strip() if token_path.exists() else "",
        "base_url": LOCAL_CLOUDPSS_BASE_URL,
    }


@lru_cache(maxsize=1)
def _live_cloudpss_skip_reason() -> str | None:
    token_path = Path(".cloudpss_token_internal")
    if not token_path.exists() or not token_path.read_text().strip():
        return "local CloudPSS token .cloudpss_token_internal is unavailable"

    parsed = urlparse(LOCAL_CLOUDPSS_BASE_URL)
    host = parsed.hostname
    port = parsed.port
    if not host or not port:
        return f"invalid local CloudPSS base URL: {LOCAL_CLOUDPSS_BASE_URL}"

    try:
        with socket.create_connection((host, port), timeout=3):
            return None
    except OSError as exc:
        return f"local CloudPSS server {LOCAL_CLOUDPSS_BASE_URL} is unreachable: {exc}"


def _require_live_cloudpss(skill_name: str) -> None:
    if skill_name not in LIVE_CLOUDPSS_SKILLS:
        return
    reason = _live_cloudpss_skip_reason()
    if reason:
        pytest.skip(reason)


def _artifact_paths(result: SkillResult) -> list[Path]:
    paths = []
    for artifact in result.artifacts:
        if artifact.path:
            paths.append(Path(artifact.path))
    return paths


def _config_for(skill_name: str, tmp_path: Path) -> dict[str, Any]:
    out = tmp_path / skill_name
    out.mkdir(parents=True, exist_ok=True)

    pf = _base_pf()
    configs: dict[str, dict[str, Any]] = {
        "power_flow": {
            **pf,
            "auth": _local_auth(),
            "output": {"format": "json", "path": str(out), "timestamp": False},
        },
        "n1_security": {
            **pf,
            "auth": _local_auth(),
            "analysis": {"branches": ["line:0"], "voltage_threshold": 0.2},
            "output": {"format": "json", "path": str(out), "timestamp": False},
        },
        "contingency_analysis": {
            **pf,
            "auth": _local_auth(),
            "contingency": {
                "level": "N-1",
                "k": 1,
                "components": ["line:0"],
                "component_types": ["branch"],
                "max_combinations": 1,
            },
            "analysis": {
                "voltage_limit": {"min": 0.8, "max": 1.2},
                "thermal_limit": 200.0,
            },
            "ranking": {"top_n": 1},
            "output": {"format": "json", "path": str(out), "generate_report": False},
        },
        "voltage_stability": {
            **pf,
            "auth": _local_auth(),
            "scan": {"load_scaling": [1.0, 1.01], "scale_generation": False},
            "monitoring": {"buses": [], "collapse_threshold": 0.7},
            "output": {
                "format": "json",
                "path": str(out),
                "generate_report": False,
                "export_pv_curve": False,
            },
        },
        "loss_analysis": {
            **pf,
            "auth": _local_auth(),
            "analysis": {
                "loss_calculation": {"enabled": True, "components": ["lines"]},
                "loss_sensitivity": {"enabled": False},
                "loss_optimization": {"enabled": False},
            },
            "output": {"format": "json", "path": str(out), "timestamp": False},
        },
        "short_circuit": {
            "engine": "pandapower",
            "auth": _local_auth(),
            "model": {"rid": "case14", "source": "local"},
            "fault": {"location": "0", "type": "3ph"},
            "calculation": {"fault_impedance": 0.0},
        },
        "batch_powerflow": {
            "engine": "pandapower",
            "models": [{"rid": "case14", "source": "local"}],
            "output": {"format": "json", "path": str(out), "timestamp": False},
        },
        "param_scan": {
            **pf,
            "scan": {"parameter": "p_mw", "values": [1.0, 1.05]},
        },
        "parameter_sensitivity": {
            **pf,
            "analysis": {"target_parameter": "load.p_mw", "delta": 0.01},
        },
        "maintenance_security": {
            **pf,
            "auth": _local_auth(),
            "maintenance": {"branch_id": "line:0"},
        },
        "n2_security": {
            **pf,
            "auth": _local_auth(),
            "analysis": {"branches": ["line:0", "line:1"], "max_scenarios": 1},
        },
        "thevenin_equivalent": {**pf, "pcc": {"bus": "bus:0", "base_mva": 100}},
        "power_quality_analysis": {**pf, "analysis": {"harmonic_orders": [2, 3, 5]}},
        "protection_coordination": {
            **pf,
            "relays": [
                {
                    "id": "R1",
                    "protected_element": "line:0",
                    "load_current": 100,
                    "fault_current": 1000,
                },
                {
                    "id": "R2",
                    "protected_element": "line:1",
                    "load_current": 90,
                    "fault_current": 900,
                    "time_dial": 0.3,
                },
            ],
            "coordination_pairs": [{"primary": "R1", "backup": "R2"}],
        },
        "frequency_response": {
            **pf,
            "disturbance": {"type": "step_load_change", "magnitude": 0.05},
            "frequency_trace": {
                "time": [0.0, 1.0, 2.0, 3.0],
                "frequency_hz": [50.0, 49.92, 49.97, 50.0],
            },
        },
        "dudv_curve": {
            **pf,
            "bus": {"key": "bus:0"},
            "scan": {"voltage_range": [0.95, 1.05], "num_points": 5},
        },
        "disturbance_severity": {
            **pf,
            "voltage_trace": {
                "time": [0.0, 1.0, 2.0, 3.0],
                "voltage_pu": [1.0, 1.0, 0.72, 0.98],
            },
            "simulation": {"fault_time": 2.0},
        },
        "orthogonal_sensitivity": {
            "model": {"rid": "case14"},
            "parameters": [
                {"name": "load_scale", "levels": [0.95, 1.05]},
                {"name": "gen_scale", "levels": [0.98, 1.02]},
            ],
            "target": {"metric": "voltage", "objective": "maximize"},
        },
        "emt_n1_screening": {
            "engine": "cloudpss",
            "auth": _live_auth(),
            "model": {"rid": "model/chenying/IEEE3", "source": "cloud"},
            "contingencies": [{"branch": "canvas_0_105", "actual_trip": False}],
            "simulation": {"timeout": 60, "sampling_freq": 1000},
        },
        "emt_simulation": {
            "engine": "cloudpss",
            "auth": _live_auth(),
            "model": {"rid": "model/chenying/IEEE3", "source": "cloud"},
            "simulation": {"timeout": 60, "sampling_freq": 1000},
            "output": {"format": "json", "path": str(out), "timestamp": False},
        },
        "small_signal_stability": {
            **pf,
            "analysis": {"damping_threshold": 0.05},
            "state_matrix": [[-0.1, 0.05], [-0.05, -0.08]],
        },
        "transient_stability": {
            **pf,
            "auth": _local_auth(),
            "simulation": {"duration": 1.0, "time_step": 0.1},
            "rotor_angle_trace": {"angles_deg": [10.0, 45.0, 80.0, 95.0, 70.0]},
        },
        "fault_clearing_scan": {
            **pf,
            "auth": _local_auth(),
            "fault": {"bus": "bus:0", "type": "3ph"},
            "scan": {"clearing_times": [0.05, 0.1, 0.2]},
        },
        "renewable_integration": {
            **pf,
            "renewable": {
                "type": "pv",
                "capacity_mw": 100.0,
                "short_circuit_mva": 350.0,
                "point_of_interconnection": "bus:0",
            },
            "harmonics": {
                "fundamental_voltage": 1.0,
                "orders": {"5": 0.03, "7": 0.02},
                "limit_thd": 0.05,
            },
            "lvrt": {
                "profile": [
                    {"time_s": 0.0, "voltage_pu": 1.0},
                    {"time_s": 0.1, "voltage_pu": 0.2},
                    {"time_s": 0.8, "voltage_pu": 0.92},
                ]
            },
            "analysis": {"min_scr": 2.0, "target_capacity_factor": 0.25},
        },
        "vsi_weak_bus": {**pf, "analysis": {"threshold": 95.0, "top_n": 5}},
        "fault_severity_scan": {
            "model": {"rid": "case14"},
            "fault": {"location": "bus:0", "reference_voltage": 1.0},
            "scan": {"chg_values": [0.1, 0.25, 0.7]},
        },
        "transient_stability_margin": {
            "model": {"rid": "case14"},
            "fault_scenarios": [{"location": "bus:0", "clearing_time": 0.1}],
        },
        "emt_fault_study": {
            "model": {"rid": "case14"},
            "scenarios": {
                "baseline": {
                    "prefault_voltage_pu": 1.0,
                    "minimum_voltage_pu": 0.75,
                    "clearing_time": 0.1,
                }
            },
        },
        "harmonic_analysis": {
            "waveform": {
                "values": [0.0, 1.0, 0.0, -1.0] * 16,
                "sample_rate": 64,
            },
            "output": {"format": "json", "path": str(out), "prefix": "harmonic"},
        },
        "reactive_compensation_design": {
            "model": {"rid": "case14"},
            "weak_buses": [{"bus": "bus:3", "scr": 2.5, "voltage_pu": 0.92}],
        },
        "hdf5_export": {
            "source": {"data": {"time": [0.0, 0.1], "values": [1.0, 2.0]}},
            "output": {"path": str(out / "result.h5")},
        },
        "comtrade_export": {
            "source": {
                "data": {
                    "time": [0.0, 0.01],
                    "channels": [
                        {"name": "Va", "type": "voltage", "values": [0.0, 1.0]},
                    ],
                }
            },
            "output": {"path": str(out), "filename": "case"},
        },
        "waveform_export": {
            "data": _waveform_data(),
            "export": {"channels": ["Va"]},
            "output": {"format": "csv", "path": str(out), "filename": "wave.csv"},
        },
        "visualize": {
            "model": {"rid": "inline"},
            "data": {"time": [0, 1, 2], "values": [1.0, 1.1, 1.0]},
            "plot": {"type": ["time_series"]},
        },
        "compare_visualization": {
            "sources": [
                {"name": "base", "data": _waveform_data()},
                {"name": "study", "data": _waveform_data()},
            ],
            "compare": {"channels": ["Va"], "metrics": ["mean", "delta"]},
        },
        "result_compare": {
            "sources": [
                {"name": "base", "data": {"values": [1.0, 2.0]}},
                {"name": "study", "data": {"values": [1.2, 2.2]}},
            ],
            "compare": {"metrics": ["max", "mean"]},
        },
        "report_generator": {
            "report": {
                "title": "Integration Report",
                "skills": ["power_flow"],
                "skill_results": [{"skill_name": "power_flow", "status": "success"}],
            },
            "output": {"path": str(out)},
        },
        "auto_channel_setup": {
            "channels": {
                "voltage": {"buses": ["Bus1"]},
                "current": {"components": ["Line1"]},
            },
            "sampling": {"frequency": 1000},
        },
        "auto_loop_breaker": {
            "model": {
                "rid": "inline/loop",
                "graph": {"a": ["b"], "b": ["c"], "c": ["a"]},
            },
            "algorithm": {"strategy": "degree"},
        },
        "topology_check": {**pf, "checks": {"islands": True, "dangling": True}},
        "model_builder": {
            "base_model": {"components": []},
            "operations": [
                {
                    "action": "add",
                    "component": {
                        "id": "bus1",
                        "type": "bus",
                        "parameters": {"vn_kv": "110"},
                    },
                    "schema": {"vn_kv": "float"},
                }
            ],
        },
        "model_validator": {
            "base_model": {"components": []},
            "operations": [
                {
                    "action": "add",
                    "component": {"id": "bus1", "type": "bus"},
                }
            ],
        },
        "model_hub": {
            "action": "list",
            "servers": [
                {
                    "name": "local",
                    "url": "http://localhost",
                    "is_public": True,
                    "models": [{"name": "Demo", "rid": "model/demo"}],
                }
            ],
        },
        "model_parameter_extractor": {
            "model": _inline_model(),
            "component_types": ["bus_3p", "line_3p"],
        },
        "component_catalog": {
            "action": "search",
            "query": "bus",
            "servers": [
                {
                    "name": "local",
                    "components": [
                        {"name": "Bus", "rid": "comp/public/bus", "type": "bus"}
                    ],
                }
            ],
        },
        "batch_task_manager": {
            "tasks": [
                {"id": "load", "skill": "noop"},
                {"id": "process", "skill": "noop", "depends_on": ["load"]},
            ],
            "max_workers": 1,
        },
        "config_batch_runner": {
            "configs": [
                {"name": "case-a", "config": {"rid": "case14"}},
                {"name": "case-b", "config": {"rid": "case9"}},
            ]
        },
        "study_pipeline": {
            "pipeline": [
                {
                    "name": "channels",
                    "skill": "auto_channel_setup",
                    "config": {
                        "channels": {"voltage": {"buses": ["Bus1"]}},
                        "sampling": {"frequency": 1000},
                    },
                }
            ]
        },
    }

    return configs[skill_name]


EXPECTED_KEYS: dict[str, tuple[str, ...]] = {
    "power_flow": ("buses", "branches", "summary"),
    "batch_powerflow": ("summary", "results"),
    "hdf5_export": ("output_path",),
    "comtrade_export": ("cfg_file", "dat_file"),
    "waveform_export": ("output_file", "sample_count"),
    "visualize": ("plots",),
    "report_generator": ("markdown_path", "html_path"),
    "auto_loop_breaker": ("break_nodes", "loop_free"),
    "model_parameter_extractor": ("groups", "component_count"),
}


@pytest.mark.integration
@pytest.mark.parametrize("skill_name", sorted(SkillRegistry.list_all()))
def test_registered_skill_runs_real_minimal_integration(skill_name: str, tmp_path: Path):
    _require_live_cloudpss(skill_name)

    skill_class = SkillRegistry.get(skill_name)
    assert skill_class is not None, f"{skill_name} is registered without a class"

    skill = skill_class()
    config = _config_for(skill_name, tmp_path)

    valid, errors = skill.validate(config)
    assert valid, f"{skill_name} rejected matrix config: {errors}"

    result = skill.run(config)
    assert isinstance(result, SkillResult), f"{skill_name} did not return SkillResult"
    assert result.skill_name in {skill_name, getattr(skill, "name", skill_name)}
    assert result.status == SkillStatus.SUCCESS, (
        f"{skill_name} failed integration run: {result.error}; data={result.data}"
    )
    assert isinstance(result.data, dict), f"{skill_name} result.data must be a dict"
    assert result.to_dict()["success"] is True

    for key in EXPECTED_KEYS.get(skill_name, ()):
        assert key in result.data, f"{skill_name} missing data.{key}"

    for artifact_path in _artifact_paths(result):
        assert artifact_path.exists(), f"{skill_name} artifact missing: {artifact_path}"
        assert artifact_path.stat().st_size > 0, (
            f"{skill_name} artifact is empty: {artifact_path}"
        )
