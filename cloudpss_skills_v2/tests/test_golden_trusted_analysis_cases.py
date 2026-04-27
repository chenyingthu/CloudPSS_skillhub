"""Golden-case tests for trusted-analysis formula behavior."""

from __future__ import annotations

import pytest

from cloudpss_skills_v2.core import SkillStatus
from cloudpss_skills_v2.poweranalysis.power_quality_analysis import (
    PowerQualityAnalysisAnalysis,
)
from cloudpss_skills_v2.poweranalysis.protection_coordination import (
    ProtectionCoordinationAnalysis,
)
from cloudpss_skills_v2.poweranalysis.reactive_compensation_design import (
    ReactiveCompensationDesignAnalysis,
)
from cloudpss_skills_v2.poweranalysis.renewable_integration import (
    RenewableIntegrationAnalysis,
)
from cloudpss_skills_v2.poweranalysis.thevenin_equivalent import (
    TheveninEquivalentAnalysis,
)
from cloudpss_skills_v2.tests.golden_cases import (
    POWER_QUALITY_BORDERLINE_FAIR,
    POWER_QUALITY_BALANCED_HARMONIC,
    PROTECTION_IEC_VERY_INVERSE,
    PROTECTION_IEC_STANDARD_INVERSE,
    REACTIVE_COMPENSATION_WEAK_BUS,
    RENEWABLE_INTEGRATION_PASSING,
    THEVENIN_WEAK_GRID,
    TRUSTED_GOLDEN_CASES,
    TWO_BUS_PV_MODEL,
)
from cloudpss_skills_v2.tools.model_builder import ModelBuilderTool
from cloudpss_skills_v2.tools.model_validator import ModelValidatorTool
from cloudpss_skills_v2.powerapi.base import SimulationResult, SimulationStatus


class FakeAdapter:
    engine_name = "fake"


class FakeHandle:
    def __init__(self, components=None):
        self._components = components or []

    def get_components(self):
        return self._components

    def get_components_by_type(self, component_type):
        del component_type
        return []


class FakePowerFlow:
    adapter = FakeAdapter()

    def get_model_handle(self, model_rid):
        return FakeHandle()

    def run_power_flow(self, model_handle):
        return SimulationResult(status=SimulationStatus.COMPLETED, data={"bus_results": []})


def test_all_trusted_golden_cases_record_reference_basis():
    for case_name, case in TRUSTED_GOLDEN_CASES.items():
        reference = case.get("reference")
        assert isinstance(reference, dict), case_name
        assert reference.get("standard_basis"), case_name
        assert reference.get("formula"), case_name
        assert reference.get("limitations"), case_name
        assert isinstance(reference.get("sources"), list) and reference["sources"], case_name

        for source in reference["sources"]:
            assert source.get("title"), case_name
            has_public_url = bool(source.get("url"))
            has_explicit_derivation = source.get("source_kind") == "derivation" and bool(
                source.get("derivation")
            )
            assert has_public_url or has_explicit_derivation, case_name


def test_builder_validator_accepts_two_bus_pv_golden_case():
    builder = ModelBuilderTool()
    validator = ModelValidatorTool()
    base_components = TWO_BUS_PV_MODEL["components"][:-1]
    pv_component = TWO_BUS_PV_MODEL["components"][-1]

    built = builder.run(
        {
            "base_model": {
                "rid": TWO_BUS_PV_MODEL["rid"],
                "components": base_components,
            },
            "operations": [
                {
                    "action": "add",
                    "component": {
                        **pv_component,
                        "parameters": {"p_mw": str(pv_component["parameters"]["p_mw"])},
                    },
                    "schema": {"p_mw": "float"},
                }
            ],
        }
    )
    assert built.status == SkillStatus.SUCCESS

    validated = validator.run(
        {
            "model": built.data["model"],
            "validation": {"phases": ["structure", "topology", "parameters"]},
            "expectations": {
                "components_present": ["pv_pcc"],
                "component_count": len(TWO_BUS_PV_MODEL["components"]),
            },
            "component_requirements": {"pv_pcc": ["p_mw"]},
        }
    )

    assert validated.status == SkillStatus.SUCCESS
    assert validated.data["status"] == "pass"
    assert validated.data["issues"] == []


def test_thevenin_equivalent_matches_hand_calculated_short_circuit_capacity():
    case = THEVENIN_WEAK_GRID
    skill = TheveninEquivalentAnalysis()

    z_mag = skill._calculate_impedance_magnitude(case["z_th_pu"]["real"], case["z_th_pu"]["imag"])
    scc = skill._calculate_scc(110.0, z_mag, case["base_mva"])
    scr = skill._calculate_scr(scc, case["base_mva"])

    assert case["reference"]["formula"] == (
        "|Zth| = sqrt(R^2 + X^2); Ssc = Sbase / |Zth|; SCR = Ssc / Srated"
    )
    assert case["expected_scc_mva"] == pytest.approx(case["base_mva"] / z_mag)
    assert z_mag == pytest.approx(case["expected_z_mag"])
    assert scc == pytest.approx(case["expected_scc_mva"])
    assert scr == pytest.approx(case["expected_scr"])


def test_power_quality_matches_hand_calculated_thd_and_unbalance():
    case = POWER_QUALITY_BALANCED_HARMONIC
    skill = PowerQualityAnalysisAnalysis()

    harmonics = {int(order): value for order, value in case["harmonic_voltages"].items()}
    thd = skill._calculate_thd(harmonics)
    unbalance = skill._calculate_unbalance(*case["phase_voltages_pu"])
    expected_thd = sum(value**2 for value in harmonics.values()) ** 0.5

    assert case["reference"]["formula"] == (
        "THD = sqrt(sum(Vh^2)) / V1; unbalance = max(|Va,b,c - Vavg|) / Vavg"
    )
    assert expected_thd == pytest.approx(case["expected_thd"])
    assert thd == pytest.approx(case["expected_thd"])
    assert unbalance == pytest.approx(case["expected_unbalance"])
    assert skill._classify_power_quality(thd, unbalance) == "good"


def test_power_quality_borderline_fair_literature_case():
    case = POWER_QUALITY_BORDERLINE_FAIR
    skill = PowerQualityAnalysisAnalysis()

    harmonics = {int(order): value for order, value in case["harmonic_voltages"].items()}
    thd = skill._calculate_thd(harmonics)
    unbalance = skill._calculate_unbalance(*case["phase_voltages_pu"])

    assert case["reference"]["formula"] == (
        "THD = sqrt(sum(Vh^2)) / V1; unbalance = max(|Va,b,c - Vavg|) / Vavg"
    )
    assert thd == pytest.approx(case["expected_thd"])
    assert unbalance == pytest.approx(case["expected_unbalance"])
    assert skill._classify_power_quality(thd, unbalance) == "fair"


def test_protection_iec_standard_inverse_operating_time_golden_case():
    case = PROTECTION_IEC_STANDARD_INVERSE
    skill = ProtectionCoordinationAnalysis()

    setting = skill._calculate_relay_settings(case["relay"], case["analysis"])
    current_multiple = case["relay"]["fault_current"] / case["expected_pickup_current"]
    expected_time = 0.1 * 0.14 / (current_multiple**0.02 - 1.0)

    assert case["reference"]["formula"] == (
        "t = TMS * k / ((If / Ipickup)^alpha - 1), with SI k=0.14 and alpha=0.02"
    )
    assert setting.pickup_current == pytest.approx(case["expected_pickup_current"])
    assert expected_time == pytest.approx(case["expected_operating_time_s"], abs=1e-4)
    assert setting.time_delay == pytest.approx(case["expected_operating_time_s"], abs=1e-4)


def test_protection_iec_very_inverse_operating_time_literature_case():
    case = PROTECTION_IEC_VERY_INVERSE
    skill = ProtectionCoordinationAnalysis()

    setting = skill._calculate_relay_settings(case["relay"], case["analysis"])
    current_multiple = case["relay"]["fault_current"] / case["expected_pickup_current"]
    expected_time = 0.1 * 13.5 / (current_multiple - 1.0)

    assert case["reference"]["formula"] == (
        "t = TMS * k / ((If / Ipickup)^alpha - 1), with VI k=13.5 and alpha=1.0"
    )
    assert setting.pickup_current == pytest.approx(case["expected_pickup_current"])
    assert expected_time == pytest.approx(case["expected_operating_time_s"], abs=1e-4)
    assert setting.time_delay == pytest.approx(case["expected_operating_time_s"], abs=1e-4)


def test_reactive_compensation_uses_golden_delta_v_formula():
    case = REACTIVE_COMPENSATION_WEAK_BUS
    skill = ReactiveCompensationDesignAnalysis()
    bus = case["bus"]
    expected_q = bus["voltage_pu"] * (1.0 - bus["voltage_pu"]) / bus["x_pu"]

    result = skill.run(
        {
            "model": {"rid": TWO_BUS_PV_MODEL["rid"]},
            "weak_buses": [bus],
        }
    )

    assert result.status == SkillStatus.SUCCESS
    assert case["reference"]["formula"] == (
        "Qreq ~= Vpu * (Vtarget - Vpu) / Xth_pu, with Vtarget = 1.0 pu"
    )
    assert round(expected_q, 2) == pytest.approx(case["expected_required_q_mvar"])
    recommendation = result.data["compensation_recommendations"][0]
    assert recommendation["required_q_mvar"] == pytest.approx(case["expected_required_q_mvar"])
    assert result.data["data_source"] == "weak_buses"


def test_renewable_integration_golden_inputs_match_expected_metrics(
    monkeypatch: pytest.MonkeyPatch,
):
    case = RENEWABLE_INTEGRATION_PASSING
    skill = RenewableIntegrationAnalysis()
    monkeypatch.setattr(
        "cloudpss_skills_v2.poweranalysis.renewable_integration.Engine.create_powerflow",
        lambda engine: FakePowerFlow(),
    )

    result = skill.run(
        {
            "engine": "pandapower",
            "model": {"rid": TWO_BUS_PV_MODEL["rid"]},
            "renewable": case["renewable"],
            "harmonics": case["harmonics"],
            "lvrt": case["lvrt"],
            "analysis": case["analysis"],
        }
    )

    assert result.status == SkillStatus.SUCCESS
    assert case["reference"]["formula"] == (
        "SCR = Ssc / Prated; THD = sqrt(sum(Vh^2)) / V1; capacity_factor = average(P) / Prated"
    )
    assert result.data["results"]["scr"]["scr"] == pytest.approx(case["expected_scr"])
    assert result.data["results"]["harmonics"]["thd"] == pytest.approx(case["expected_thd"])
    assert result.data["results"]["capacity"]["capacity_factor"] == pytest.approx(
        case["expected_capacity_factor"]
    )
    assert result.data["summary"]["overall_passed"] is True
