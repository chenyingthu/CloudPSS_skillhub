#!/usr/bin/env python3
"""
小信号稳定性技能 - 单元测试
"""

from unittest.mock import Mock, patch

from cloudpss_skills.builtin.small_signal_stability import SmallSignalStabilitySkill
from cloudpss_skills.core.base import SkillStatus


class TestSmallSignalStabilityUnit:
    @patch("cloudpss.setToken")
    @patch("cloudpss.Model")
    def test_run_returns_failed_for_approximate_small_signal_result(self, mock_model_class, mock_set_token, tmp_path):
        skill = SmallSignalStabilitySkill()

        model = Mock()
        model.name = "IEEE3"
        job = Mock()
        job.id = "job-1"
        job.status.return_value = 1
        job.result.getBuses.return_value = [{"data": {"columns": []}}]
        job.result.getBranches.return_value = [{"data": {"columns": []}}]
        model.runPowerFlow.return_value = job
        mock_model_class.fetch.return_value = model

        # 让内部分析链跑到返回结果阶段，不在前置提取阶段失败
        skill._extract_system_data = Mock(return_value={"generators": [{"label": "G1", "H": 3.0, "Xdp": 0.3, "P": 100.0, "V": 1.0}], "buses": [{}], "base_power": 100.0})
        skill._build_state_matrix = Mock(return_value=__import__("numpy").array([[0.0, 1.0], [-0.1, -0.2]]))
        skill._eigenvalue_analysis = Mock(return_value={"eigenvalues": [{"real": -0.1, "imag": 1.0}], "modes": [], "assessment": {"is_stable": True}})
        skill._calculate_participation_factors = Mock(return_value={})

        token_file = tmp_path / ".cloudpss_token"
        token_file.write_text("dummy", encoding="utf-8")

        result = skill.run(
            {
                "skill": "small_signal_stability",
                "auth": {"token_file": str(token_file)},
                "model": {"rid": "model/test", "source": "cloud"},
                "output": {"path": str(tmp_path), "generate_report": False},
            }
        )

        assert result.status == SkillStatus.FAILED
        assert result.data["verified"] is False
        assert "近似状态矩阵" in (result.error or "")
