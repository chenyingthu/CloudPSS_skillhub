"""Tests for cloudpss_skills_v2.poweranalysis.loss_analysis."""

from types import SimpleNamespace
from typing import Any, cast

from cloudpss_skills_v2.poweranalysis.loss_analysis import LossAnalysis


class TestLossAnalysis:
    def test_first_present_value_preserves_zero(self):
        skill = LossAnalysis()
        assert skill._first_present_value({"power_loss_mw": 0.0, "Ploss": 1.2}, "power_loss_mw", "Ploss") == 0.0

    def test_calculate_line_losses_keeps_zero_active_loss_when_reactive_loss_exists(self):
        skill = LossAnalysis()

        skill._calculate_line_losses(
            [
                {
                    "name": "Line 1",
                    "from_bus": "Bus1",
                    "to_bus": "Bus2",
                    "power_loss_mw": 0.0,
                    "Ploss": 2.5,
                    "reactive_loss_mvar": 3.2,
                    "current_ka": 0.0,
                }
            ]
        )

        assert len(skill.branch_losses) == 1
        branch_loss = skill.branch_losses[0]
        assert branch_loss.p_loss_mw == 0.0
        assert branch_loss.q_loss_mvar == 3.2
        assert branch_loss.current_ka == 0.0

    def test_calculate_transformer_losses_keeps_zero_active_loss(self):
        skill = LossAnalysis()
        fake_api = SimpleNamespace(
            get_model_handle=lambda model_rid: SimpleNamespace(
                get_components_by_type=lambda component_type: [SimpleNamespace(key="xf_1")]
            )
        )

        skill._calculate_transformer_losses(
            [
                {
                    "key": "xf_1",
                    "name": "Transformer 1",
                    "from_bus": "Bus3",
                    "to_bus": "Bus4",
                    "power_loss_mw": 0.0,
                    "Ploss": 4.0,
                    "reactive_loss_mvar": 1.5,
                }
            ],
            model_rid="model/test",
            api=cast(Any, fake_api),
        )

        assert len(skill.transformer_losses) == 1
        transformer = skill.transformer_losses[0]
        assert transformer.total_loss_mw == 0.0
        assert transformer.reactive_loss_mvar == 1.5

    def test_validate_requires_model_rid_and_auth(self):
        skill = LossAnalysis()
        valid, errors = skill.validate({})
        assert not valid
        assert "必须指定模型RID" in errors
        assert "必须提供 auth.token 或 auth.token_file" in errors
