#!/usr/bin/env python3
"""
HDF5导出技能 - 单元测试
"""

import json

from cloudpss_skills.builtin.hdf5_export import HDF5ExportSkill
from cloudpss_skills.core.base import SkillStatus


class TestHDF5ExportUnit:
    def test_run_fails_for_placeholder_cloud_source_types(self, tmp_path):
        skill = HDF5ExportSkill()

        result = skill.run(
            {
                "source": {"type": "emt_result", "rid": "job-1"},
                "output": {"path": str(tmp_path)},
            }
        )

        assert result.status == SkillStatus.FAILED
        assert "当前未打通真实结果加载链路" in (result.error or "")

    def test_run_succeeds_for_real_file_source(self, tmp_path):
        skill = HDF5ExportSkill()

        source_file = tmp_path / "source.json"
        source_file.write_text(json.dumps({"type": "disturbance", "dv_results": [{"bus": "Bus1", "dv_up": 0.1, "dv_down": 0.2}]}), encoding="utf-8")

        result = skill.run(
            {
                "source": {"type": "file", "file_path": str(source_file)},
                "output": {"path": str(tmp_path), "filename": "exported.h5"},
            }
        )

        assert result.status == SkillStatus.SUCCESS
        assert result.data["hdf5_file"].endswith("exported.h5")
