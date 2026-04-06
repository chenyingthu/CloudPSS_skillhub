#!/usr/bin/env python3
"""
预想事故分析技能 - 单元测试
"""

from types import SimpleNamespace

from cloudpss_skills.builtin.contingency_analysis import ContingencyAnalysisSkill


class TestContingencyAnalysisUnit:
    def test_parse_table_uses_cloudpss_row_conversion(self):
        skill = ContingencyAnalysisSkill()
        rows = skill._parse_table(
            [
                {
                    "type": "table",
                    "data": {
                        "columns": [
                            {"name": "Branch", "data": ["line-1"]},
                            {"name": "Pij", "data": [120.0]},
                            {"name": "Qij", "data": [0.0]},
                        ]
                    },
                }
            ]
        )

        assert rows == [{"Branch": "line-1", "Pij": 120.0, "Qij": 0.0}]

    def test_evaluate_thermal_loading_uses_real_ratings(self):
        skill = ContingencyAnalysisSkill()
        model = SimpleNamespace(
            getComponentByKey=lambda _: SimpleNamespace(
                definition="model/CloudPSS/_newTransformer_3p2w",
                label="XF-1",
                args={"Tmva": {"source": "100", "ɵexp": ""}},
            )
        )

        result = skill._evaluate_thermal_loading(
            model,
            [{"Branch": "xf_1", "Pij": 120.0, "Qij": 0.0, "Pji": -118.0, "Qji": 0.0}],
            thermal_limit=1.0,
        )

        assert result["supported"] is True
        assert result["max_loading_pu"] > 1.0
        assert result["violation"]["branch"] == "XF-1"
