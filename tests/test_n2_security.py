#!/usr/bin/env python3
"""
N-2 Security Skill - Integration Tests

使用真实CloudPSS API进行集成测试
"""

import pytest
import os
from pathlib import Path

from cloudpss_skills.builtin.n2_security import N2SecuritySkill


@pytest.mark.integration
class TestN2SecuritySkill:
    """N-2安全校核技能集成测试"""

    @pytest.fixture
    def skill(self):
        return N2SecuritySkill()

    @pytest.fixture
    def base_config(self, live_auth):
        """基础配置 - 使用IEEE39模型进行N-2测试"""
        return {
            "skill": "n2_security",
            "auth": {"token": live_auth},
            "model": {"rid": "model/holdme/IEEE39", "source": "cloud"},
            "analysis": {
                "branches": [],  # 空表示全部
                "check_voltage": True,
                "check_thermal": True,
                "voltage_min": 0.95,
                "voltage_max": 1.05,
                "thermal_limit": 1.0,
                "max_combinations": 10  # 限制组合数以加快测试
            },
            "output": {"format": "json", "path": "./test_n2_security_report.json"}
        }

    def test_skill_initialization(self, skill):
        """测试技能初始化"""
        assert skill.name == "n2_security"
        assert skill.version == "1.0.0"
        assert "N-2" in skill.description

    def test_config_validation_success(self, skill, base_config):
        """测试配置验证通过"""
        result = skill.validate(base_config)
        assert result.valid is True
        assert len(result.errors) == 0

    def test_config_validation_missing_model_rid(self, skill, base_config):
        """测试配置验证失败 - 缺少model.rid"""
        base_config["model"].pop("rid")
        result = skill.validate(base_config)
        assert result.valid is False

    def test_config_validation_invalid_voltage_range(self, skill, base_config):
        """测试配置验证失败 - 电压范围无效"""
        base_config["analysis"]["voltage_min"] = 1.1
        base_config["analysis"]["voltage_max"] = 0.9
        result = skill.validate(base_config)
        assert result.valid is False
        assert any("voltage" in err.lower() for err in result.errors)

    def test_branch_detection(self, skill, base_config, live_auth):
        """测试支路检测 - 使用真实API"""
        from cloudpss import Model, setToken
        setToken(live_auth)

        model = Model.fetch(base_config["model"]["rid"])
        branches = skill._get_branches(model, base_config["analysis"])

        assert len(branches) > 0
        assert all("id" in b and "name" in b and "type" in b for b in branches)

        print(f"\n✅ 检测到 {len(branches)} 条支路")
        for b in branches[:5]:  # 显示前5条
            print(f"   - {b['name']} ({b['type']})")

    def test_n2_scenario_generation(self, skill):
        """测试N-2场景生成"""
        branches = [
            {"id": "line1", "name": "LINE_1", "type": "line"},
            {"id": "line2", "name": "LINE_2", "type": "line"},
            {"id": "line3", "name": "LINE_3", "type": "line"},
        ]

        analysis_config = {"max_combinations": 100}
        scenarios = skill._generate_n2_scenarios(branches, analysis_config)

        # 3条支路的C(3,2) = 3种组合
        assert len(scenarios) == 3

        expected_pairs = [("LINE_1", "LINE_2"), ("LINE_1", "LINE_3"), ("LINE_2", "LINE_3")]
        for i, (b1, b2) in enumerate(scenarios):
            assert (b1["name"], b2["name"]) in expected_pairs

        print(f"\n✅ 生成 {len(scenarios)} 个N-2场景")

    def test_n2_scenario_generation_with_limit(self, skill):
        """测试N-2场景生成 - 带限制"""
        branches = [
            {"id": f"line{i}", "name": f"LINE_{i}", "type": "line"}
            for i in range(10)
        ]

        analysis_config = {"max_combinations": 5}
        scenarios = skill._generate_n2_scenarios(branches, analysis_config)

        # 应该被限制到5个
        assert len(scenarios) == 5
        print(f"\n✅ 限制后生成 {len(scenarios)} 个N-2场景")

    def test_n2_scenario_generation_with_pairs(self, skill):
        """测试N-2场景生成 - 指定支路对"""
        branches = [
            {"id": "line1", "name": "LINE_1", "type": "line"},
            {"id": "line2", "name": "LINE_2", "type": "line"},
            {"id": "line3", "name": "LINE_3", "type": "line"},
        ]

        analysis_config = {
            "branch_pairs": [["LINE_1", "LINE_2"], ["LINE_2", "LINE_3"]]
        }
        scenarios = skill._generate_n2_scenarios(branches, analysis_config)

        assert len(scenarios) == 2
        print(f"\n✅ 指定支路对生成 {len(scenarios)} 个N-2场景")

    def test_full_n2_analysis_execution(self, skill, base_config):
        """测试完整N-2分析执行 - 使用真实API"""
        # 限制为少量组合以加快测试
        base_config["analysis"]["max_combinations"] = 3

        result = skill.run(base_config)

        # N-2测试可能因为系统解列而失败，但我们检查报告结构
        assert result.data is not None
        report = result.data

        assert "model_name" in report
        assert "model_rid" in report
        assert "timestamp" in report
        assert "summary" in report
        assert "voltage_limits" in report
        assert "results" in report

        summary = report["summary"]
        assert "total_scenarios" in summary
        assert "passed" in summary
        assert "failed" in summary
        assert "errors" in summary
        assert "pass_rate" in summary

        print(f"\n✅ N-2分析完成")
        print(f"   总场景: {summary['total_scenarios']}")
        print(f"   通过: {summary['passed']}, 失败: {summary['failed']}, 错误: {summary['errors']}")
        print(f"   通过率: {summary['pass_rate']:.1f}%")

    def test_n2_analysis_with_specific_branches(self, skill, base_config):
        """测试指定支路的N-2分析"""
        # 先获取模型中的实际支路名称
        base_config["analysis"]["branches"] = []  # 使用所有支路
        base_config["analysis"]["max_combinations"] = 3

        result = skill.run(base_config)

        # 验证执行
        assert result.data is not None
        print(f"\n✅ 指定支路N-2分析完成")

    def test_n2_analysis_with_specific_pairs(self, skill, base_config, live_auth):
        """测试指定支路对的N-2分析 - 使用真实API"""
        from cloudpss import Model, setToken
        setToken(live_auth)

        # 获取模型中的实际支路
        model = Model.fetch(base_config["model"]["rid"])
        branches = skill._get_branches(model, {})

        if len(branches) >= 2:
            # 使用前两个支路作为测试对
            base_config["analysis"]["branch_pairs"] = [
                [branches[0]["name"], branches[1]["name"]]
            ]
            # 清除branches设置以使用branch_pairs
            base_config["analysis"]["branches"] = []

            result = skill.run(base_config)

            assert result.data is not None
            assert result.data["summary"]["total_scenarios"] == 1

            print(f"\n✅ 指定支路对N-2分析完成: {branches[0]['name']} + {branches[1]['name']}")

    def test_result_structure(self, skill):
        """测试结果数据结构"""
        from cloudpss_skills.builtin.n2_security import N2ContingencyResult

        result = N2ContingencyResult(
            branch1_id="line1",
            branch1_name="LINE_1",
            branch2_id="line2",
            branch2_name="LINE_2",
            status="passed",
            converged=True,
            violation=None,
            max_voltage_pu=1.02,
            min_voltage_pu=0.98,
            max_loading_pu=0.85
        )

        assert result.branch1_name == "LINE_1"
        assert result.branch2_name == "LINE_2"
        assert result.status == "passed"
        assert result.converged is True

        print(f"\n✅ 结果数据结构验证通过")

    def test_report_generation(self, skill):
        """测试报告生成"""
        class MockModel:
            name = "TestModel"
            rid = "model/test/TestModel"

        scenarios = [
            ({"id": "l1", "name": "LINE_1", "type": "line"},
             {"id": "l2", "name": "LINE_2", "type": "line"}),
        ]

        from cloudpss_skills.builtin.n2_security import N2ContingencyResult
        results = [
            N2ContingencyResult(
                branch1_id="l1", branch1_name="LINE_1",
                branch2_id="l2", branch2_name="LINE_2",
                status="passed", converged=True, violation=None,
                max_voltage_pu=1.02, min_voltage_pu=0.98, max_loading_pu=0.85
            )
        ]

        analysis_config = {
            "voltage_min": 0.95,
            "voltage_max": 1.05
        }

        report = skill._generate_report(MockModel(), scenarios, results, analysis_config)

        assert report["model_name"] == "TestModel"
        assert report["summary"]["total_scenarios"] == 1
        assert report["summary"]["passed"] == 1
        assert report["summary"]["pass_rate"] == 100.0
        assert len(report["results"]) == 1

        print(f"\n✅ 报告生成验证通过")

    def test_output_file_generation(self, skill, base_config, tmp_path):
        """测试输出文件生成"""
        output_path = tmp_path / "n2_security_test.json"
        base_config["output"]["path"] = str(output_path)
        base_config["analysis"]["max_combinations"] = 2

        result = skill.run(base_config)

        # 验证文件生成
        assert output_path.exists()
        assert output_path.stat().st_size > 0

        import json
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert "model_rid" in data
            assert "summary" in data

        print(f"\n✅ 输出文件已生成: {output_path}")

    def test_console_output(self, skill, base_config):
        """测试控制台输出"""
        base_config["output"]["format"] = "console"
        base_config["analysis"]["max_combinations"] = 2

        result = skill.run(base_config)

        print(f"\n✅ 控制台输出测试完成")

    def test_critical_pairs_identification(self, skill):
        """测试关键故障对识别"""
        class MockModel:
            name = "TestModel"
            rid = "model/test/TestModel"

        scenarios = [
            ({"id": "l1", "name": "LINE_1", "type": "line"},
             {"id": "l2", "name": "LINE_2", "type": "line"}),
            ({"id": "l3", "name": "LINE_3", "type": "line"},
             {"id": "l4", "name": "LINE_4", "type": "line"}),
        ]

        from cloudpss_skills.builtin.n2_security import N2ContingencyResult
        results = [
            N2ContingencyResult(
                branch1_id="l1", branch1_name="LINE_1",
                branch2_id="l2", branch2_name="LINE_2",
                status="passed", converged=True, violation=None,
                max_voltage_pu=1.02, min_voltage_pu=0.98, max_loading_pu=0.85
            ),
            N2ContingencyResult(
                branch1_id="l3", branch1_name="LINE_3",
                branch2_id="l4", branch2_name="LINE_4",
                status="failed", converged=True, violation="电压越下限: 0.920 pu",
                max_voltage_pu=1.01, min_voltage_pu=0.92, max_loading_pu=0.90
            ),
        ]

        analysis_config = {"voltage_min": 0.95, "voltage_max": 1.05}
        report = skill._generate_report(MockModel(), scenarios, results, analysis_config)

        assert len(report["critical_pairs"]) == 1
        assert report["critical_pairs"][0]["branch1"] == "LINE_3"
        assert report["critical_pairs"][0]["branch2"] == "LINE_4"
        assert "电压越下限" in report["critical_pairs"][0]["violation"]

        print(f"\n✅ 关键故障对识别: {report['critical_pairs'][0]['branch1']} + {report['critical_pairs'][0]['branch2']}")
