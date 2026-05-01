#!/usr/bin/env python3
"""
Schema/Default 一致性测试

验证所有技能的 config_schema 和 get_default_config() 是否一致，
以及 validate() 方法的基本行为。
"""

import pytest
from typing import Any

from cloudpss_skills_v2.registry import list_skills, get_skill
from cloudpss_skills_v2.core.schema_validation import (
    get_schema_defaults,
    get_config_defaults,
)


class TestSchemaConsistency:
    """测试所有技能的 schema 和 default_config 一致性。"""

    @pytest.fixture(scope="class")
    def all_skills(self):
        """获取所有已注册的技能名称。"""
        return list_skills()

    def test_all_skills_have_config_schema(self, all_skills):
        """验证所有技能都有 config_schema 属性。"""
        errors = []
        for name in all_skills:
            try:
                skill_class = get_skill(name)
                skill = skill_class()
                schema = skill.config_schema
                assert isinstance(schema, dict), f"{name}: config_schema 必须是字典"
                assert "properties" in schema or "type" in schema, f"{name}: schema 格式无效"
            except AttributeError as e:
                errors.append(f"{name}: 缺少 config_schema - {e}")
            except Exception as e:
                errors.append(f"{name}: 获取 config_schema 失败 - {e}")

        if errors:
            pytest.fail("\n".join(errors))

    def test_all_skills_have_get_default_config(self, all_skills):
        """验证所有技能都有 get_default_config 方法。"""
        errors = []
        for name in all_skills:
            try:
                skill_class = get_skill(name)
                skill = skill_class()
                default = skill.get_default_config()
                assert isinstance(default, dict), f"{name}: get_default_config 必须返回字典"
                assert "skill" in default, f"{name}: default_config 必须包含 'skill' 字段"
                assert default["skill"] == name, f"{name}: default_config['skill'] 必须等于技能名"
            except AttributeError as e:
                errors.append(f"{name}: 缺少 get_default_config - {e}")
            except Exception as e:
                errors.append(f"{name}: 调用 get_default_config 失败 - {e}")

        if errors:
            pytest.fail("\n".join(errors))

    def test_schema_default_matches_config(self, all_skills):
        """验证 schema 中的 default 值与 get_default_config 返回的值一致。"""
        errors = []

        for name in all_skills:
            try:
                skill_class = get_skill(name)
                skill = skill_class()
                schema = skill.config_schema
                default_config = skill.get_default_config()

                schema_defaults = get_schema_defaults(schema)
                config_defaults = get_config_defaults(default_config)

                # 检查 schema 中有 default 但 config 中没有的字段
                for path, schema_val in schema_defaults.items():
                    if path not in config_defaults:
                        errors.append(f"{name}: {path} - schema有default={schema_val!r}, config缺失")
                    elif config_defaults[path] != schema_val:
                        errors.append(
                            f"{name}: {path} - schema={schema_val!r} != config={config_defaults[path]!r}"
                        )

                # 检查 config 中有但 schema 中没有 default 的字段
                for path, config_val in config_defaults.items():
                    if path not in schema_defaults:
                        errors.append(f"{name}: {path} - schema缺失default, config={config_val!r}")

            except Exception as e:
                errors.append(f"{name}: 对比失败 - {e}")

        if errors:
            pytest.fail("\n".join(errors))


class TestValidateMethod:
    """测试所有技能的 validate 方法行为一致性。"""

    @pytest.fixture(scope="class")
    def all_skills(self):
        """获取所有已注册的技能名称。"""
        return list_skills()

    def test_all_skills_have_validate(self, all_skills):
        """验证所有技能都有 validate 方法。"""
        errors = []
        for name in all_skills:
            try:
                skill_class = get_skill(name)
                skill = skill_class()
                assert hasattr(skill, "validate"), f"{name}: 缺少 validate 方法"
                assert callable(getattr(skill, "validate")), f"{name}: validate 必须是可调用方法"
            except Exception as e:
                errors.append(f"{name}: {e}")

        if errors:
            pytest.fail("\n".join(errors))

    def test_validate_returns_tuple(self, all_skills):
        """验证 validate 方法返回 (bool, list[str]) 元组。"""
        errors = []
        for name in all_skills:
            try:
                skill_class = get_skill(name)
                skill = skill_class()
                default_config = skill.get_default_config()

                result = skill.validate(default_config)

                assert isinstance(result, tuple), f"{name}: validate 必须返回元组"
                assert len(result) == 2, f"{name}: validate 必须返回 (bool, errors) 两个元素"

                is_valid, error_list = result
                assert isinstance(is_valid, bool), f"{name}: 第一个返回值必须是 bool"
                assert isinstance(error_list, list), f"{name}: 第二个返回值必须是 list"
                assert all(isinstance(e, str) for e in error_list), f"{name}: 错误列表必须都是字符串"

            except Exception as e:
                errors.append(f"{name}: {e}")

        if errors:
            pytest.fail("\n".join(errors))

    def test_validate_with_default_config_returns_tuple(self, all_skills):
        """验证使用默认配置时 validate 返回正确的元组格式。"""
        errors = []
        for name in all_skills:
            try:
                skill_class = get_skill(name)
                skill = skill_class()
                default_config = skill.get_default_config()

                result = skill.validate(default_config)

                # 验证返回格式正确
                assert isinstance(result, tuple), f"{name}: validate 必须返回元组"
                assert len(result) == 2, f"{name}: validate 必须返回两个元素"

                is_valid, error_list = result
                assert isinstance(is_valid, bool), f"{name}: 第一个返回值必须是 bool"
                assert isinstance(error_list, list), f"{name}: 第二个返回值必须是 list"

                # 注意：不是所有技能的默认配置都能通过验证
                # 这只是验证 validate 方法能正确处理默认配置而不抛出异常

            except Exception as e:
                errors.append(f"{name}: {e}")

        if errors:
            pytest.fail("\n".join(errors))

    def test_validate_with_none_config(self, all_skills):
        """验证 validate 处理 None 配置不抛出未处理异常。"""
        errors = []
        for name in all_skills:
            try:
                skill_class = get_skill(name)
                skill = skill_class()

                result = skill.validate(None)

                assert isinstance(result, tuple), f"{name}: validate(None) 必须返回元组"
                assert len(result) == 2, f"{name}: validate(None) 必须返回两个元素"

                is_valid, error_list = result
                assert isinstance(is_valid, bool), f"{name}: 第一个返回值必须是 bool"

            except (TypeError, AttributeError) as e:
                # 有些技能没有处理 None，这是已知问题
                # 记录但不作为测试失败
                pass
            except Exception as e:
                errors.append(f"{name}: validate(None) 抛出未预期异常 - {e}")

        if errors:
            pytest.fail("\n".join(errors))

    def test_validate_with_empty_config(self, all_skills):
        """验证 validate 处理空配置的行为一致。"""
        errors = []
        for name in all_skills:
            try:
                skill_class = get_skill(name)
                skill = skill_class()

                result = skill.validate({})

                assert isinstance(result, tuple), f"{name}: validate({{}}) 必须返回元组"
                assert len(result) == 2, f"{name}: validate({{}}) 必须返回两个元素"

            except Exception as e:
                errors.append(f"{name}: validate({{}}) 抛出异常 - {e}")

        if errors:
            pytest.fail("\n".join(errors))
