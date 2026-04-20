#!/usr/bin/env python3
"""
DUDV曲线技能 - 单元测试
"""

import json

from cloudpss_skills.builtin.dudv_curve import DUDVCurveSkill
from cloudpss_skills.core.base import SkillStatus


class TestDUDVCurveUnit:
    def test_from_disturbance_result_reads_current_channel_results_format(self, tmp_path):
        skill = DUDVCurveSkill()
        result_file = tmp_path / "disturbance.json"
        result_file.write_text(
            json.dumps(
                {
                    "channel_results": [
                        {"name": "Bus_16", "dv": {"v_steady": 1.0, "dv_up": 0.05, "dv_down": -0.08}},
                    ]
                }
            ),
            encoding="utf-8",
        )

        data = skill.from_disturbance_severity_result(str(result_file), ["Bus_16"])

        assert "Bus_16" in data
        assert data["Bus_16"]["dv"][1] == 0

    def test_run_fails_without_real_result_file(self):
        skill = DUDVCurveSkill()

        result = skill.run({"buses": ["Bus_16"]})

        assert result.status == SkillStatus.FAILED
        assert "仅支持基于 disturbance_severity 真实结果文件" in (result.error or "")
