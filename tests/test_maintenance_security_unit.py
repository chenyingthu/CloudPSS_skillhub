#!/usr/bin/env python3
"""
检修方式安全校核技能 - 单元测试
"""

from cloudpss_skills.builtin.maintenance_security import MaintenanceSecuritySkill


def make_table(rows):
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


class TestMaintenanceSecurityUnit:
    def test_table_to_rows_parses_cloudpss_table_list(self):
        skill = MaintenanceSecuritySkill()
        rows = skill._table_to_rows(
            [
                make_table(
                    [
                        {"Vm": 1.01, "loading": 0.72},
                        {"Vm": 0.97, "loading": 0.85},
                    ]
                )
            ]
        )

        assert rows == [
            {"Vm": 1.01, "loading": 0.72},
            {"Vm": 0.97, "loading": 0.85},
        ]

    def test_branch_loading_uses_real_power_and_rating(self):
        skill = MaintenanceSecuritySkill()
        model = type(
            "FakeModel",
            (),
            {
                "getComponentByKey": lambda self, _: type(
                    "FakeComponent",
                    (),
                    {
                        "definition": "model/CloudPSS/_newTransformer_3p2w",
                        "args": {"Tmva": {"source": "100", "ɵexp": ""}},
                    },
                )()
            },
        )()

        loading = skill._branch_loading(
            model,
            {"Branch": "xf_1", "Pij": 120.0, "Qij": 0.0, "Pji": -118.0, "Qji": 0.0},
        )

        assert loading > 1.0
