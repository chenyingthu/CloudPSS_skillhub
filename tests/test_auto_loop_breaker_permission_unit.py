#!/usr/bin/env python3
"""
自动解环技能 - 权限提示单元测试
"""

from types import SimpleNamespace

import pytest

from cloudpss_skills.builtin.auto_loop_breaker import AutoLoopBreakerSkill


class TestAutoLoopBreakerPermissionUnit:
    def test_build_topology_graph_reports_definition_permission_issue_clearly(self):
        skill = AutoLoopBreakerSkill()

        class FakeModel:
            revision = object()

            def fetchTopology(self, implementType=None, maximumDepth=None):
                return SimpleNamespace(toJSON=lambda: {"components": {}})

            def getAllComponents(self):
                return {
                    "canvas_0_1": SimpleNamespace(
                        shape="diagram-component",
                        definition="model/CloudPSS/_newBus_3p",
                    )
                }

            @classmethod
            def fetch(cls, rid):
                raise Exception("权限不足")

        with pytest.raises(RuntimeError, match="需要访问组件 definition/revision"):
            skill._build_topology_graph(FakeModel())
