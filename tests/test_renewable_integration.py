#!/usr/bin/env python3
"""
Renewable Integration Skill - Integration Tests

使用真实CloudPSS API进行集成测试
"""

import pytest
import os
from pathlib import Path

from cloudpss_skills.builtin.renewable_integration import RenewableIntegrationSkill


@pytest.mark.integration
class TestRenewableIntegrationSkill:
    """新能源接入评估技能集成测试"""

    @pytest.fixture
    def skill(self):
        return RenewableIntegrationSkill()

    @pytest.fixture
    def base_config(self, live_auth):
        """基础配置"""
        return {
            "skill": "renewable_integration",
            "auth": {"token": live_auth},
            "model": {"rid": "model/holdme/IEEE39", "source": "cloud"},
            "renewable": {
                "type": "pv",
                "bus": "BUS_10",
                "capacity": 100
            },
            "analysis": {
                "scr": {"enabled": True, "threshold": 3.0},
                "voltage_variation": {"enabled": True, "tolerance": 0.05},
                "harmonic_injection": {"enabled": True, "limits": {"thd": 0.05}},
                "lvrt_compliance": {"enabled": True, "standard": "gb"},
                "stability_impact": {"enabled": True}
            },
            "output": {"format": "json", "path": "./test_renewable_report.json"}
        }

    def test_skill_initialization(self, skill):
        """测试技能初始化"""
        assert skill.name == "renewable_integration"
        assert skill.version == "1.0.0"
        assert "新能源接入评估" in skill.description

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
        assert any("rid" in err.lower() for err in result.errors)

    def test_full_analysis_execution(self, skill, base_config):
        """测试完整分析执行 - 使用真实API"""
        result = skill.run(base_config)

        # 验证执行结果
        assert result.status.value == "failed", "包含未真实验证分析项的全量评估不应返回success"
        assert "不能作为已验证的新能源接入评估结论" in (result.error or "")
        assert result.data is not None

        # 验证报告结构
        report = result.data
        assert "model_rid" in report
        assert "timestamp" in report
        assert "analysis_results" in report
        assert "summary" in report

        # 验证分析结果
        analysis = report["analysis_results"]
        assert "scr" in analysis
        assert "voltage_variation" in analysis
        assert "harmonic_injection" in analysis
        assert "lvrt_compliance" in analysis
        assert "stability_impact" in analysis

        # 验证SCR结果
        scr = analysis["scr"]
        assert "scr" in scr
        assert "grid_strength" in scr
        assert scr["grid_strength"] in ["强电网", "中等强度电网", "弱电网"]
        assert scr["verified"] is True

        # 验证电压波动结果
        voltage = analysis["voltage_variation"]
        assert "verified" in voltage
        assert voltage["verified"] is False

        # 验证汇总信息
        summary = report["summary"]
        assert "total_analysis" in summary
        assert "passed" in summary
        assert "assessment" in summary
        assert summary["assessment"] == "仅供初步评估"
        assert summary["certifiable"] is False

        print(f"\n✅ 新能源接入评估完成: {summary['passed']}/{summary['total_analysis']} 项满足当前规则")
        print(f"   SCR: {scr['scr']}, 电网强度: {scr['grid_strength']}")
        print(f"   总体评估: {summary['assessment']}")

    def test_pv_analysis(self, skill, base_config):
        """测试光伏接入分析"""
        base_config["renewable"] = {
            "type": "pv",
            "bus": "BUS_10",
            "capacity": 50
        }

        result = skill.run(base_config)
        assert result.status.value == "failed"

        # 验证光伏特性谐波
        harmonic = result.data["analysis_results"]["harmonic_injection"]
        assert "harmonics" in harmonic
        assert "h5" in harmonic["harmonics"]

        print(f"\n✅ 光伏接入分析完成: THD={harmonic['thd_percent']}%")

    def test_wind_analysis(self, skill, base_config):
        """测试风电接入分析"""
        base_config["renewable"] = {
            "type": "wind",
            "bus": "BUS_10",
            "capacity": 80
        }

        result = skill.run(base_config)
        assert result.status.value == "failed"

        # 验证风电特性
        scr = result.data["analysis_results"]["scr"]
        assert "scr" in scr
        assert scr["renewable_capacity_mw"] == 80

        print(f"\n✅ 风电接入分析完成: SCR={scr['scr']}")

    def test_scr_calculation_with_different_capacities(self, skill, base_config):
        """测试不同容量下的SCR计算"""
        capacities = [50, 100, 200]
        base_config["analysis"] = {
            "scr": {"enabled": True, "threshold": 3.0},
            "voltage_variation": {"enabled": False},
            "harmonic_injection": {"enabled": False},
            "lvrt_compliance": {"enabled": False},
            "stability_impact": {"enabled": False},
        }
        previous_scr = None

        for capacity in capacities:
            base_config["renewable"]["capacity"] = capacity
            result = skill.run(base_config)

            assert result.status.value == "success"
            scr = result.data["analysis_results"]["scr"]["scr"]
            if previous_scr is not None:
                assert scr < previous_scr
            previous_scr = scr

            # SCR应该随着容量增加而降低
            print(f"\n   容量 {capacity}MW -> SCR: {scr}")

    def test_lvrt_compliance_gb_standard(self, skill, base_config):
        """测试国标LVRT合规性验证"""
        base_config["analysis"]["lvrt_compliance"]["standard"] = "gb"

        result = skill.run(base_config)
        assert result.status.value == "failed"

        lvrt = result.data["analysis_results"]["lvrt_compliance"]
        assert lvrt["standard"] == "GB/T 19964-2012"
        assert "lvrt_curve" in lvrt
        assert len(lvrt["lvrt_curve"]) > 0
        assert lvrt["verified"] is False

        print(f"\n✅ GB标准LVRT验证完成")

    def test_lvrt_compliance_ieee_standard(self, skill, base_config):
        """测试IEEE LVRT合规性验证"""
        base_config["analysis"]["lvrt_compliance"]["standard"] = "ieee"

        result = skill.run(base_config)
        assert result.status.value == "failed"

        lvrt = result.data["analysis_results"]["lvrt_compliance"]
        assert lvrt["standard"] == "IEEE 1547-2018"
        assert lvrt["verified"] is False

        print(f"\n✅ IEEE标准LVRT验证完成")

    def test_output_file_generation(self, skill, base_config, tmp_path):
        """测试输出文件生成"""
        output_path = tmp_path / "renewable_test_output.json"
        base_config["output"]["path"] = str(output_path)

        result = skill.run(base_config)
        assert result.status.value == "failed"

        # 验证文件生成
        assert output_path.exists()
        assert output_path.stat().st_size > 0

        # 验证文件内容
        import json
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert "model_rid" in data
            assert "analysis_results" in data

        print(f"\n✅ 输出文件已生成: {output_path}")

    def test_console_output(self, skill, base_config):
        """测试控制台输出格式"""
        base_config["output"]["format"] = "console"

        result = skill.run(base_config)
        assert result.status.value == "failed"

        print(f"\n✅ 控制台输出测试完成")

    def test_stability_impact_assessment(self, skill, base_config):
        """测试稳定性影响评估"""
        result = skill.run(base_config)
        assert result.status.value == "failed"

        stability = result.data["analysis_results"]["stability_impact"]
        assert "verified" in stability
        assert stability["verified"] is False
        assert "error" in stability or "assessments" in stability

        print(f"\n✅ 稳定性评估检查完成: {stability}")

    def test_verified_lvrt_execution_on_wind_lvrt_case(self, skill, live_auth):
        """测试基于专用风机LVRT算例的真实低电压穿越验证"""
        config = {
            "skill": "renewable_integration",
            "auth": {"token": live_auth},
            "model": {"rid": "model/holdme/codex_lvrt_case_fix_20260405_114928", "source": "cloud"},
            "renewable": {"type": "wind", "bus": "PCC", "capacity": 50},
            "analysis": {
                "scr": {"enabled": False},
                "voltage_variation": {"enabled": False},
                "harmonic_injection": {"enabled": False},
                "lvrt_compliance": {"enabled": True, "standard": "gb", "fault_mode": "1"},
                "stability_impact": {"enabled": False},
            },
            "output": {"format": "json", "path": "./test_renewable_lvrt_verified.json"},
        }

        result = skill.run(config)
        assert result.status.value == "success", result.error

        lvrt = result.data["analysis_results"]["lvrt_compliance"]
        assert lvrt["supported"] is True
        assert lvrt["verified"] is True
        assert lvrt["passed"] is True
        assert lvrt["compliant"] is True
        assert lvrt["state_summary"]["entered_lvrt"] is True
        assert lvrt["state_summary"]["tripped"] is False
        assert lvrt["state_summary"]["recovered"] is True

        summary = result.data["summary"]
        assert summary["certifiable"] is True
        assert summary["overall_verified"] is True

        print(f"\n✅ LVRT真实验证完成: job={lvrt['job_id']} state={lvrt['state_summary']}")
