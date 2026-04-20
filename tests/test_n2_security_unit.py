#!/usr/bin/env python3
"""
N-2安全校核技能 - 单元测试
"""

from types import SimpleNamespace

import pytest

from cloudpss_skills.builtin.n2_security import N2SecuritySkill


class FakePFResult:
    def __init__(self, branch_table):
        self._branch_table = branch_table

    def getBranches(self):
        return [self._branch_table]


def make_branch_table(rows):
    columns = {}
    for row in rows:
        for key, value in row.items():
            columns.setdefault(key, []).append(value)
    return {
        "type": "table",
        "data": {
            "columns": [{"name": key, "data": values} for key, values in columns.items()]
        },
    }


class TestN2SecurityUnit:
    @pytest.fixture
    def skill(self):
        return N2SecuritySkill()

    def test_get_branches_prefers_label_over_internal_key(self, skill):
        model = SimpleNamespace(
            getAllComponents=lambda: {
                "canvas_0_115": SimpleNamespace(
                    definition="model/CloudPSS/TransmissionLine",
                    label="TLine_3p-17",
                    args={"Name": "line-3-18"},
                )
            }
        )

        branches = skill._get_branches(model, {})

        assert branches[0]["name"] == "TLine_3p-17"

    def test_evaluate_thermal_loading_flags_overload_when_rating_is_available(self, skill):
        table = make_branch_table(
            [{"Branch": "xf_1", "Pij": 120.0, "Qij": 0.0, "Pji": -118.0, "Qji": 0.0}]
        )
        model = SimpleNamespace(
            getComponentByKey=lambda _: SimpleNamespace(
                definition="model/CloudPSS/_newTransformer_3p2w",
                args={"Tmva": {"source": "100", "ɵexp": ""}},
            )
        )

        result = skill._evaluate_thermal_loading(model, FakePFResult(table), thermal_limit=1.0)

        assert result["supported"] is True
        assert result["max_loading_pu"] > 1.0
        assert "热稳定越限" in result["violation"]

    def test_evaluate_thermal_loading_reports_unsupported_when_no_rating_exists(self, skill):
        table = make_branch_table(
            [{"Branch": "line_1", "Pij": 50.0, "Qij": 0.0, "Pji": -49.0, "Qji": 0.0}]
        )
        model = SimpleNamespace(
            getComponentByKey=lambda _: SimpleNamespace(
                definition="model/CloudPSS/TransmissionLine",
                args={"Irated": 0, "Vbase": {"source": "500", "ɵexp": ""}},
            )
        )

        result = skill._evaluate_thermal_loading(model, FakePFResult(table), thermal_limit=1.0)

        assert result["supported"] is False
        assert result["max_loading_pu"] is None
