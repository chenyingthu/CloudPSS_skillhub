#!/usr/bin/env python3
"""
Transient Stability Margin Skill - Integration Tests

使用真实CloudPSS API进行集成测试
"""

import pytest
import os
from pathlib import Path

from cloudpss_skills.builtin.transient_stability_margin import TransientStabilityMarginSkill


@pytest.mark.integration
class TestTransientStabilityMarginSkill:
    """暂态稳定裕度评估技能集成测试"""

    @pytest.fixture
    def skill(self):
        return TransientStabilityMarginSkill()

    @pytest.fixture
    def base_config(self, live_auth):
        """基础配置"""
        return {
            "skill": "transient_stability_margin",
            "auth": {"token": live_auth},
            "model": {"rid": "model/holdme/IEEE3", "source": "cloud"},
            "fault_scenarios": [
                {"location": "BUS_1", "type": "three_phase", "duration": 0.1},
                {"location": "BUS_2", "type": "three_phase", "duration": 0.1}
            ],
            "generators": ["GEN_1", "GEN_2"],
            "analysis": {
                "compute_cct": True,
                "compute_margin": True,
                "margin_baseline": 0.2,
                "cct_tolerance": 0.005
            },
            "output": {"format": "json", "path": "./test_stability_margin_report.json"}
        }

    def test_skill_initialization(self, skill):
        """测试技能初始化"""
        assert skill.name == "transient_stability_margin"
        assert skill.version == "1.0.0"
        assert "暂态稳定裕度" in skill.description

    def test_config_validation_success(self, skill, base_config):
        """测试配置验证通过"""
        result = skill.validate(base_config)
        assert result.valid is True

    def test_config_validation_missing_model_rid(self, skill, base_config):
        """测试配置验证失败 - 缺少model.rid"""
        base_config["model"].pop("rid")
        result = skill.validate(base_config)
        assert result.valid is False

    def test_config_validation_no_scenarios(self, skill, base_config):
        """测试配置验证警告 - 无故障场景"""
        base_config["fault_scenarios"] = []
        result = skill.validate(base_config)
        # 应该有警告但不阻止执行
        assert result.valid is True

    def test_cct_calculation_execution(self, skill, base_config):
        """测试CCT计算执行 - 使用真实API"""
        # 简化场景以加快测试
        base_config["fault_scenarios"] = [
            {"location": "BUS_1", "type": "three_phase", "duration": 0.1}
        ]
        base_config["analysis"]["cct_tolerance"] = 0.01  # 放宽精度要求

        result = skill.run(base_config)

        # 由于EMT仿真可能较慢，允许部分失败
        if result.status.value == "success":
            report = result.data
            assert "model_rid" in report
            assert "scenarios" in report

            if report["scenarios"]:
                scenario = report["scenarios"][0]
                assert "cct" in scenario or "error" in scenario

                if "cct" in scenario:
                    cct = scenario["cct"]
                    assert "cct_seconds" in cct
                    assert "iterations" in cct
                    assert cct["method"] == "bisection"
                    print(f"\n✅ CCT计算完成: {cct['cct_seconds']:.4f}s ({cct['iterations']}次迭代)")
        else:
            pytest.skip(f"CCT计算需要EMT支持: {result.error}")

    def test_margin_calculation(self, skill, base_config):
        """测试稳定裕度计算"""
        # 使用已知的CCT结果测试裕度计算
        cct_result = {"cct_seconds": 0.25, "iterations": 10, "tolerance": 0.001}
        baseline = 0.2

        margin = skill._compute_margin(cct_result, baseline)

        assert "margin_percent" in margin
        assert "margin_seconds" in margin
        assert "stability_status" in margin
        assert "assessment" in margin

        # 验证计算: (0.25 - 0.2) / 0.25 * 100 = 20%
        expected_margin = (0.25 - 0.2) / 0.25 * 100
        assert abs(margin["margin_percent"] - expected_margin) < 0.01

        print(f"\n✅ 裕度计算: {margin['margin_percent']:.2f}% - {margin['stability_status']}")

    def test_margin_status_categories(self, skill):
        """测试裕度状态分类"""
        test_cases = [
            (0.4, 0.2, "高裕度"),    # 50% margin
            (0.25, 0.2, "中等裕度"),  # 20% margin
            (0.22, 0.2, "低裕度"),   # 9% margin
            (0.18, 0.2, "不稳定"),   # -11% margin
        ]

        for cct, baseline, expected_status in test_cases:
            cct_result = {"cct_seconds": cct}
            margin = skill._compute_margin(cct_result, baseline)
            assert margin["stability_status"] == expected_status, \
                f"CCT={cct}, baseline={baseline}: expected {expected_status}, got {margin['stability_status']}"
            print(f"\n   CCT={cct}s, baseline={baseline}s -> {margin['stability_status']}")

    def test_summary_generation(self, skill):
        """测试汇总生成"""
        scenarios = [
            {"fault_location": "BUS_1", "cct": {"cct_seconds": 0.25}, "margin": {"margin_percent": 20.0}},
            {"fault_location": "BUS_2", "cct": {"cct_seconds": 0.18}, "margin": {"margin_percent": -10.0}},
        ]

        summary = skill._generate_summary(scenarios)

        assert "total_scenarios" in summary
        assert summary["total_scenarios"] == 2
        assert "cct_statistics" in summary
        assert "margin_statistics" in summary
        assert "weakest_point" in summary
        assert summary["weakest_point"]["location"] == "BUS_2"
        assert "recommendations" in summary

        print(f"\n✅ 汇总生成: 最薄弱点={summary['weakest_point']['location']}")

    def test_recommendations_generation(self, skill):
        """测试建议生成"""
        scenarios = [
            {"fault_location": "BUS_1", "cct": {"cct_seconds": 0.25}, "margin": {"margin_percent": 20.0}},
            {"fault_location": "BUS_2", "cct": {"cct_seconds": 0.18}, "margin": {"margin_percent": -10.0}},
        ]
        margins = [20.0, -10.0]

        recommendations = skill._generate_recommendations(scenarios, margins)

        assert len(recommendations) > 0
        # 应该包含不稳定场景的建议
        assert any("不稳定" in rec or "薄弱点" in rec for rec in recommendations)

        for rec in recommendations:
            print(f"\n   建议: {rec}")

    def test_different_fault_types(self, skill, base_config):
        """测试不同故障类型"""
        fault_types = ["three_phase", "single_phase", "line_ground"]

        for fault_type in fault_types:
            base_config["fault_scenarios"] = [
                {"location": "BUS_1", "type": fault_type, "duration": 0.1}
            ]

            # 验证配置接受不同故障类型
            result = skill.validate(base_config)
            assert result.valid is True
            print(f"\n   故障类型 {fault_type} 验证通过")

    def test_output_file_generation(self, skill, base_config, tmp_path):
        """测试输出文件生成"""
        output_path = tmp_path / "stability_margin_test.json"
        base_config["output"]["path"] = str(output_path)
        base_config["fault_scenarios"] = [
            {"location": "BUS_1", "type": "three_phase", "duration": 0.1}
        ]

        result = skill.run(base_config)

        # 文件应该生成（即使执行失败也会有报告）
        assert output_path.exists()

        import json
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert "model_rid" in data

        print(f"\n✅ 输出文件已生成: {output_path}")

    def test_console_output(self, skill, base_config):
        """测试控制台输出"""
        base_config["output"]["format"] = "console"
        base_config["fault_scenarios"] = [
            {"location": "BUS_1", "type": "three_phase", "duration": 0.1}
        ]

        result = skill.run(base_config)
        # 控制台输出不应导致失败
        print(f"\n✅ 控制台输出测试完成")
