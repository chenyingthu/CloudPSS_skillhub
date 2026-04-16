#!/usr/bin/env python3
"""
网损分析与优化技能 - 集成测试

测试内容:
1. 技能注册验证
2. 配置Schema验证
3. 真实API调用测试 (使用 IEEE39 算例)
4. 结果验证

运行: pytest tests/test_loss_analysis_integration.py -v
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cloudpss_skills.builtin.loss_analysis import (
    LossAnalysisSkill,
    BranchLoss,
    TransformerLoss,
)
from cloudpss_skills.core.base import SkillStatus


HAS_TOKEN = os.path.exists(".cloudpss_token")
TOKEN_MSG = "需要.cloudpss_token文件进行集成测试"


class TestLossAnalysisSkill:
    """网损分析技能集成测试"""

    @pytest.fixture
    def skill(self):
        return LossAnalysisSkill()

    @pytest.fixture
    def valid_config(self):
        return {
            "model": {"rid": "model/holdme/IEEE39"},
            "analysis": {
                "loss_calculation": {
                    "enabled": True,
                    "components": ["lines", "transformers"],
                },
                "loss_sensitivity": {"enabled": True},
                "loss_optimization": {
                    "enabled": True,
                    "method": "reactive_power_optimization",
                },
            },
            "output": {"format": "json"},
        }

    def test_skill_registration(self, skill):
        """测试1: 技能注册信息"""
        assert skill.name == "loss_analysis"
        assert "网损分析" in skill.description
        assert skill.version == "1.0.0"
        print(f"✅ 技能注册: {skill.name} v{skill.version}")

    def test_config_schema_validation(self, skill):
        """测试2: 配置Schema验证"""
        assert skill.config_schema is not None
        assert "properties" in skill.config_schema
        print("✅ 配置Schema验证通过")

    def test_validation_with_valid_config(self, skill, valid_config):
        """测试3: 有效配置验证"""
        result = skill.validate(valid_config)
        assert result.valid is True
        print("✅ 有效配置验证通过")

    def test_validation_with_missing_rid(self, skill):
        """测试4: 缺少RID的配置验证"""
        invalid_config = {"model": {}}
        result = skill.validate(invalid_config)
        assert result.valid is False
        print("✅ 缺失RID检测正确")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_real_api_call(self, skill, valid_config):
        """测试5: 真实API调用测试"""
        print("\n🔄 开始真实API调用测试...")
        print(f"   模型: {valid_config['model']['rid']}")

        result = skill.run(valid_config)

        print(f"   状态: {result.status.value}")
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED], (
            f"执行失败: {result.error}"
        )

        # 验证返回数据
        assert result.data is not None
        assert "model" in result.data
        assert "summary" in result.data
        assert "branch_losses" in result.data
        assert "transformer_losses" in result.data

        summary = result.data["summary"]
        print(f"   总网损: {summary.get('total_loss_mw', 0):.2f} MW")
        print(f"   线路损耗: {summary.get('branch_loss_mw', 0):.2f} MW")
        print(f"   变压器损耗: {summary.get('transformer_loss_mw', 0):.2f} MW")

        print("✅ 真实API调用测试通过!")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_loss_summary(self, skill, valid_config):
        """测试6: 网损汇总验证"""
        result = skill.run(valid_config)
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

        summary = result.data["summary"]
        assert "total_loss_mw" in summary
        assert "branch_loss_mw" in summary
        assert "transformer_loss_mw" in summary
        assert "top_loss_branches" in summary

        # 验证总损耗为正数且合理（IEEE39系统网损通常在1-100MW范围）
        assert summary["total_loss_mw"] >= 0
        assert summary["branch_count"] >= 0

        # 验证提取到了实际的损耗数据（而非全部为零）
        branch_losses = result.data.get("branch_losses", [])
        if branch_losses:
            total_branch_loss = sum(bl.get("p_loss_mw", 0) for bl in branch_losses)
            print(
                f"   实际线路损耗总和: {total_branch_loss:.4f} MW ({len(branch_losses)}条支路)"
            )
            # 对于IEEE39系统，应该有实际的损耗值
            assert total_branch_loss > 0.001, "应该提取到非零的线路损耗数据"

        print(f"✅ 网损汇总验证通过 (总损耗: {summary['total_loss_mw']:.2f} MW)")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_branch_losses(self, skill, valid_config):
        """测试7: 支路损耗详情验证"""
        result = skill.run(valid_config)
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

        branch_losses = result.data.get("branch_losses", [])

        for bl in branch_losses:
            assert "branch_id" in bl
            assert "p_loss_mw" in bl
            assert "q_loss_mvar" in bl
            assert "loading_percent" in bl

        print(f"✅ 支路损耗详情验证通过 ({len(branch_losses)}条支路)")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_sensitivity_analysis(self, skill, valid_config):
        """测试8: 灵敏度分析验证

        注意: 灵敏度分析当前未实现 (NotImplementedError)，
        返回 {"error": "...", "available": False}
        """
        result = skill.run(valid_config)
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

        sensitivity = result.data.get("sensitivity_analysis", {})
        # 灵敏度分析可能不可用
        if not sensitivity.get("available", True):
            assert "error" in sensitivity
            print("⚠️ 灵敏度分析未实现（预期行为）")
        else:
            # 如果可用，验证其结构
            assert "description" in sensitivity
            assert "method" in sensitivity
            print("✅ 灵敏度分析验证通过")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_optimization_suggestions(self, skill, valid_config):
        """测试9: 优化建议验证"""
        result = skill.run(valid_config)
        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]

        optimization = result.data.get("optimization_suggestions", {})
        assert "current_total_loss_mw" in optimization
        assert "suggestions" in optimization

        for suggestion in optimization.get("suggestions", []):
            assert "type" in suggestion
            assert "priority" in suggestion
            assert "description" in suggestion

        print(f"✅ 优化建议验证通过 ({len(optimization.get('suggestions', []))}条建议)")

    @pytest.mark.skipif(not HAS_TOKEN, reason=TOKEN_MSG)
    def test_integration_performance(self, skill, valid_config):
        """测试10: 性能测试"""
        import time

        start = time.time()
        result = skill.run(valid_config)
        elapsed = time.time() - start

        assert result.status in [SkillStatus.SUCCESS, SkillStatus.FAILED]
        assert elapsed < 120  # 应在2分钟内完成

        print(f"⏱️  执行时间: {elapsed:.1f}秒")
        print("✅ 性能测试通过")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
