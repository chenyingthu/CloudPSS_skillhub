from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _load_artifact() -> dict[str, Any]:
    artifact_path = Path(__file__).resolve().with_name("test_system_1_network.json")
    return json.loads(artifact_path.read_text(encoding="utf-8"))


def _load_pandapower_reference():
    try:
        import pandapower.networks as networks
    except ImportError as exc:
        raise SystemExit(
            "pandapower is required for TS1 reconstruction audit; install it or run in the repo environment"
        ) from exc
    return networks.create_cigre_network_mv(with_der=False)


def _artifact_bus_id(bus_index: int) -> str:
    return f"bus{bus_index}"


def _line_signature(line: dict[str, Any]) -> dict[str, Any]:
    return {
        "from_bus": line["from_bus"],
        "to_bus": line["to_bus"],
        "length_km": round(float(line["length_km"]), 8),
        "r_ohm_per_km": round(float(line["r_ohm_per_km"]), 8),
        "x_ohm_per_km": round(float(line["x_ohm_per_km"]), 8),
        "c_nf_per_km": round(float(line["c_nf_per_km"]), 8),
        "max_i_ka": round(float(line["max_i_ka"]), 8),
    }


def _pandapower_line_signature(line: Any) -> dict[str, Any]:
    return {
        "from_bus": _artifact_bus_id(int(line.from_bus)),
        "to_bus": _artifact_bus_id(int(line.to_bus)),
        "length_km": round(float(line.length_km), 8),
        "r_ohm_per_km": round(float(line.r_ohm_per_km), 8),
        "x_ohm_per_km": round(float(line.x_ohm_per_km), 8),
        "c_nf_per_km": round(float(line.c_nf_per_km), 8),
        "max_i_ka": round(float(line.max_i_ka), 8),
    }


def audit_reconstruction() -> dict[str, Any]:
    artifact = _load_artifact()
    reference = _load_pandapower_reference()
    model = artifact["model"]

    artifact_lines = {line["name"]: _line_signature(line) for line in model["lines"]}
    reference_lines = {
        str(line.name): _pandapower_line_signature(line)
        for line in reference.line.itertuples()
    }
    line_mismatches = {}
    for line_name, artifact_line in sorted(artifact_lines.items()):
        reference_line = reference_lines.get(line_name)
        if reference_line is None:
            line_mismatches[line_name] = {"artifact": artifact_line, "reference": None}
        elif reference_line != artifact_line:
            line_mismatches[line_name] = {"artifact": artifact_line, "reference": reference_line}
    missing_artifact_lines = sorted(set(reference_lines) - set(artifact_lines))

    switch_line_names = {switch["line"] for switch in artifact.get("switches", [])}
    unknown_switch_lines = sorted(switch_line_names - set(artifact_lines))

    reference_line_switches = reference.switch[reference.switch.et == "l"]
    reference_trafo_switches = reference.switch[reference.switch.et == "t"]

    artifact_load_p = sum(float(load["p_mw"]) for load in model.get("loads", []))
    artifact_load_q = sum(float(load["q_mvar"]) for load in model.get("loads", []))
    reference_load_p = float(reference.load.p_mw.sum())
    reference_load_q = float(reference.load.q_mvar.sum())

    findings = []
    if float(model["sn_mva"]) != float(reference.sn_mva):
        findings.append(
            {
                "severity": "high",
                "id": "system_base_mismatch",
                "message": "artifact model.sn_mva differs from pandapower CIGRE MV reference net.sn_mva",
                "artifact_sn_mva": float(model["sn_mva"]),
                "reference_sn_mva": float(reference.sn_mva),
            }
        )
    if line_mismatches:
        findings.append(
            {
                "severity": "high",
                "id": "line_parameter_or_endpoint_mismatch",
                "message": "artifact line records differ from name-matched pandapower CIGRE MV lines",
                "count": len(line_mismatches),
            }
        )
    if missing_artifact_lines:
        findings.append(
            {
                "severity": "high",
                "id": "missing_reference_lines",
                "message": "reference line names are absent from the artifact",
                "line_names": missing_artifact_lines,
            }
        )
    if len(artifact.get("switches", [])) != len(reference.switch):
        findings.append(
            {
                "severity": "medium",
                "id": "switch_count_mismatch",
                "message": "artifact omits transformer switches present in the pandapower reference",
                "artifact_switch_count": len(artifact.get("switches", [])),
                "reference_switch_count": int(len(reference.switch)),
                "reference_line_switch_count": int(len(reference_line_switches)),
                "reference_trafo_switch_count": int(len(reference_trafo_switches)),
            }
        )
    if unknown_switch_lines:
        findings.append(
            {
                "severity": "high",
                "id": "unknown_switch_lines",
                "message": "artifact switch references line names missing from artifact line table",
                "line_names": unknown_switch_lines,
            }
        )
    if abs(artifact_load_p - reference_load_p) > 1e-9 or abs(artifact_load_q - reference_load_q) > 1e-9:
        findings.append(
            {
                "severity": "medium",
                "id": "load_total_mismatch",
                "message": "artifact load totals differ from pandapower CIGRE MV reference",
                "artifact_p_mw": artifact_load_p,
                "artifact_q_mvar": artifact_load_q,
                "reference_p_mw": reference_load_p,
                "reference_q_mvar": reference_load_q,
            }
        )

    return {
        "audit": "test_system_1_reconstruction_vs_pandapower_cigre_mv",
        "reference": {
            "source": "pandapower.networks.create_cigre_network_mv(with_der=False)",
            "upstream_source": "CIGRE TF C6.04.02 TB 575, Benchmark Systems for Network Integration of Renewable and Distributed Energy Resources",
            "sn_mva": float(reference.sn_mva),
            "bus_count": int(len(reference.bus)),
            "line_count": int(len(reference.line)),
            "trafo_count": int(len(reference.trafo)),
            "load_count": int(len(reference.load)),
            "switch_count": int(len(reference.switch)),
        },
        "artifact": {
            "path": str(Path(__file__).resolve().with_name("test_system_1_network.json")),
            "sn_mva": float(model["sn_mva"]),
            "bus_count": len(model["buses"]),
            "line_count": len(model["lines"]),
            "trafo_count": len(model.get("trafos", [])),
            "load_count": len(model.get("loads", [])),
            "switch_count": len(artifact.get("switches", [])),
        },
        "line_mismatches": line_mismatches,
        "findings": findings,
        "next_actions": [
            "Regenerate or patch test_system_1_network.json from name-matched pandapower CIGRE MV records instead of relying on list order.",
            "Resolve whether Test System 1 uses net.sn_mva=1.0, transformer 25 MVA ratings, or another paper-specific per-unit base.",
            "Add load impedance equivalents from paper Eq. (5) before expecting paper-table agreement.",
            "Confirm islanded transformer and switch semantics from paper Figure 1 before pruning lines or transformers.",
        ],
    }


def main() -> None:
    print(json.dumps(audit_reconstruction(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
