#!/usr/bin/env python3
"""
正交敏感性分析技能 - 单元测试
"""

from types import SimpleNamespace
from unittest.mock import Mock, patch

from cloudpss_skills.builtin.orthogonal_sensitivity import OrthogonalSensitivitySkill
from cloudpss_skills.core.base import SkillStatus


class TestOrthogonalSensitivityUnit:
    def test_find_components_by_param_requires_exact_component_identity(self):
        skill = OrthogonalSensitivitySkill()
        model = SimpleNamespace(
            getAllComponents=lambda: {
                "canvas_gen1": SimpleNamespace(label="Gen1", name="", args={"Name": "GEN1"}),
                "canvas_gen10": SimpleNamespace(label="Gen10", name="", args={"Name": "GEN10"}),
            }
        )

        matches = skill._find_components_by_param(model, "Gen1.pf_P")

        assert list(matches.keys()) == ["canvas_gen1"]

    @patch("cloudpss.setToken")
    @patch("cloudpss.Model")
    def test_run_fails_when_parameter_targets_no_components(self, mock_model_class, mock_set_token):
        skill = OrthogonalSensitivitySkill()

        model = Mock()
        model.name = "TestModel"
        model.jobs = [{"rid": "function/CloudPSS/powerflow", "name": "pf"}]
        model.toJSON.return_value = {"dummy": True}
        model.getAllComponents.return_value = {}
        model.getComponentsByRid.return_value = {}
        mock_model_class.fetch.return_value = model
        mock_model_class.return_value = model

        config = {
            "skill": "orthogonal_sensitivity",
            "auth": {"token": "dummy"},
            "model": {"rid": "model/test"},
            "parameters": [{"name": "Gen1.pf_P", "levels": [0.9, 1.1]}],
            "target": {"metric": "voltage", "bus_name": "Bus_16"},
            "design": {"table_type": "L4_2_3", "simulation_type": "power_flow"},
        }

        result = skill.run(config)

        assert result.status == SkillStatus.FAILED
        assert "未解析到任何目标组件" in (result.error or "")
