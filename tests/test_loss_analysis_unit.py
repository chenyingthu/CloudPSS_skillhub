#!/usr/bin/env python3
"""
网损分析技能 - 单元测试
"""

from types import SimpleNamespace

import pytest

from cloudpss_skills.builtin.loss_analysis import LossAnalysisSkill


class FakePowerFlowResult:
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
            "columns": [
                {"name": key, "data": values}
                for key, values in columns.items()
            ]
        }
    }


class TestLossAnalysisUnit:
    @pytest.fixture
    def skill(self):
        return LossAnalysisSkill()

    def test_transformer_losses_are_extracted_from_real_branch_rows(self, skill):
        branch_table = make_branch_table(
            [
                {"Branch": "line_1", "From bus": "Bus1", "To bus": "Bus2", "Ploss": 1.25, "Qloss": 3.5},
                {"Branch": "xf_1", "From bus": "Bus3", "To bus": "Bus4", "Ploss": 0.0, "Qloss": 12.0},
            ]
        )
        skill.model = SimpleNamespace(
            getComponentByKey=lambda key: SimpleNamespace(
                definition="model/CloudPSS/_newTransformer_3p2w" if key == "xf_1" else "model/CloudPSS/TransmissionLine",
                label="XF-1" if key == "xf_1" else "Line-1",
            )
        )

        skill._calculate_transformer_losses(FakePowerFlowResult(branch_table))

        assert len(skill.transformer_losses) == 1
        transformer = skill.transformer_losses[0]
        assert transformer.transformer_id == "XF-1"
        assert transformer.total_loss_mw == 0.0
        assert transformer.reactive_loss_mvar == 12.0
        assert transformer.core_loss_mw is None
        assert transformer.copper_loss_mw is None

    def test_transformer_loss_extraction_fails_when_model_has_transformers_but_rows_do_not_match(self, skill, monkeypatch):
        branch_table = make_branch_table(
            [
                {"Branch": "line_1", "From bus": "Bus1", "To bus": "Bus2", "Ploss": 1.25, "Qloss": 3.5},
            ]
        )
        skill.model = SimpleNamespace(
            getComponentByKey=lambda key: SimpleNamespace(
                definition="model/CloudPSS/TransmissionLine",
                label="Line-1",
            )
        )

        def fake_get_components_by_type(model, component_type):
            if component_type == "model/CloudPSS/_newTransformer_3p2w":
                return {"xf_missing": {"label": "XF-Missing"}}
            return {}

        monkeypatch.setattr("cloudpss_skills.builtin.loss_analysis.get_components_by_type", fake_get_components_by_type)

        with pytest.raises(RuntimeError, match="提取变压器损耗失败"):
            skill._calculate_transformer_losses(FakePowerFlowResult(branch_table))
