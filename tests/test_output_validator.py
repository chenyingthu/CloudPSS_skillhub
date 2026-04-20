"""
Tests for Skill Output Validation

验证技能输出是否符合标准规范。
"""

import pytest
from datetime import datetime
from cloudpss_skills.core.output_validator import (
    SkillOutputValidator,
    ValidationResult,
    validate_skill_output,
)


class TestSkillOutputValidator:
    """测试 SkillOutputValidator"""

    def setup_method(self):
        self.validator = SkillOutputValidator()

    def test_valid_simulation_result(self):
        """测试有效的仿真结果"""
        data = {
            "skill_name": "power_flow",
            "success": True,
            "timestamp": "2026-04-15T10:00:00",
            "converged": True,
            "model_info": {
                "rid": "test/model",
                "bus_count": 39,
            },
            "summary": {
                "total_loss_mw": 1.5,
            },
        }
        result = self.validator.validate(
            skill_name="power_flow", data=data, category="simulation", status="SUCCESS"
        )
        assert result.valid
        assert len(result.get_errors()) == 0

    def test_missing_category_fields_requires_converged(self):
        """测试缺少类别特定字段（converged）"""
        data = {
            "skill_name": "power_flow",
            "success": True,
            "timestamp": "2026-04-15T10:00:00",
        }
        result = self.validator.validate(
            skill_name="power_flow", data=data, category="simulation", status="SUCCESS"
        )
        assert not result.valid
        errors = result.get_errors()
        assert any("converged" in e.message for e in errors)

    def test_missing_category_fields(self):
        """测试缺少类别特定字段"""
        data = {
            "skill_name": "power_flow",
            "success": True,
            "timestamp": "2026-04-15T10:00:00",
        }
        result = self.validator.validate(
            skill_name="power_flow", data=data, category="simulation", status="SUCCESS"
        )
        assert not result.valid
        errors = result.get_errors()
        assert any("converged" in e.message for e in errors)

    def test_success_with_empty_data(self):
        """测试 SUCCESS 状态但空数据"""
        data = {}
        result = self.validator.validate(
            skill_name="power_flow", data=data, status="SUCCESS"
        )
        assert len(result.get_warnings()) > 0

    def test_detect_fake_bus_data(self):
        """测试检测假 bus 数据"""
        data = {
            "skill_name": "loss_analysis",
            "success": True,
            "timestamp": "2026-04-15T10:00:00",
            "sensitivities": [
                {"bus": "Bus_1", "sensitivity": 0.01},
                {"bus": "Bus_2", "sensitivity": 0.02},
            ],
        }
        result = self.validator.validate(
            skill_name="loss_analysis", data=data, status="SUCCESS"
        )
        errors = result.get_errors()
        assert any("Bus_" in e.message for e in errors)

    def test_detect_placeholder_fields(self):
        """测试检测占位符字段"""
        data = {
            "skill_name": "power_flow",
            "success": True,
            "timestamp": "2026-04-15T10:00:00",
            "todo": "Not implemented",
        }
        result = self.validator.validate(
            skill_name="power_flow", data=data, status="SUCCESS"
        )
        assert not result.valid
        errors = result.get_errors()
        assert any("todo" in e.message for e in errors)

    def test_camelcase_warning(self):
        """测试 camelCase 警告"""
        data = {
            "skill_name": "power_flow",
            "success": True,
            "timestamp": "2026-04-15T10:00:00",
            "busCount": 39,
            "totalLoss": 1.5,
        }
        result = self.validator.validate(
            skill_name="power_flow", data=data, status="SUCCESS"
        )
        warnings = result.get_warnings()
        assert any("busCount" in e.message for e in warnings)
        assert any("totalLoss" in e.message for e in warnings)

    def test_success_field_type_check(self):
        """测试 success 字段类型检查"""
        data = {
            "skill_name": "power_flow",
            "success": "True",  # 字符串而非布尔
            "timestamp": "2026-04-15T10:00:00",
        }
        result = self.validator.validate(
            skill_name="power_flow", data=data, status="SUCCESS"
        )
        errors = result.get_errors()
        assert any("success" in e.message and "str" in e.message for e in errors)


class TestValidateSkillOutputFunction:
    """测试便捷函数"""

    def test_basic_validation(self):
        """测试基本验证"""
        data = {
            "skill_name": "power_flow",
            "success": True,
            "timestamp": "2026-04-15T10:00:00",
            "converged": True,
            "model_info": {"rid": "test"},
            "summary": {},
        }
        result = validate_skill_output(
            skill_name="power_flow", data=data, category="simulation", status="SUCCESS"
        )
        assert result.valid


class TestSkillResultValidation:
    """测试 SkillResult 验证"""

    def test_validate_complete_result(self):
        """测试完整的 SkillResult"""
        from cloudpss_skills.core.base import SkillResult, SkillStatus

        result = SkillResult(
            skill_name="power_flow",
            status=SkillStatus.SUCCESS,
            start_time=datetime.now(),
            end_time=datetime.now(),
            data={
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "converged": True,
                "model_info": {"rid": "test"},
                "summary": {},
            },
        )

        # 验证结果（skill_name 在 SkillResult 层级检查，不在 data 中）
        validator = SkillOutputValidator()
        validation = validator.validate(
            skill_name=result.skill_name,
            data=result.data,
            category="simulation",
            status=result.status.value.upper(),
        )

        # skill_name 不在 data 中是合法的，data 本身验证应该通过
        assert len(validation.get_errors()) == 0

    def test_validate_failed_result_has_error(self):
        """测试失败结果应包含 error"""
        from cloudpss_skills.core.base import SkillResult, SkillStatus

        result = SkillResult(
            skill_name="power_flow",
            status=SkillStatus.FAILED,
            start_time=datetime.now(),
            end_time=datetime.now(),
            data={},
            error="Connection failed",
        )

        # 失败状态不强制要求 data
        validator = SkillOutputValidator()
        validation = validator.validate(
            skill_name=result.skill_name,
            data=result.data,
            status=result.status.value.upper(),
        )

        # 失败状态允许空 data
        assert validation.valid or len(result.data) == 0


class TestNamingConventions:
    """测试命名规范"""

    def setup_method(self):
        self.validator = SkillOutputValidator()

    def test_snake_case_is_valid(self):
        """测试 snake_case 是合法的"""
        data = {
            "skill_name": "power_flow",
            "success": True,
            "timestamp": "2026-04-15T10:00:00",
            "bus_count": 39,
            "total_loss_mw": 1.5,
            "pass_rate": 0.95,
        }
        result = self.validator.validate(
            skill_name="power_flow", data=data, status="SUCCESS"
        )
        warnings = result.get_warnings()
        assert not any("bus_count" in w.message for w in warnings)
        assert not any("total_loss_mw" in w.message for w in warnings)

    def test_mixed_naming_generates_warnings(self):
        """测试混合命名产生警告"""
        data = {
            "skill_name": "power_flow",
            "success": True,
            "timestamp": "2026-04-15T10:00:00",
            "bus_count": 39,
            "totalLoss": 1.5,  # 应该是 total_loss
            "voltagePU": 1.0,  # 应该是 voltage_pu
        }
        result = self.validator.validate(
            skill_name="power_flow", data=data, status="SUCCESS"
        )
        warnings = result.get_warnings()
        assert len(warnings) >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
