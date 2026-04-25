"""Tests for cloudpss_skills_v2.poweranalysis.vsi_weak_bus."""

import pytest
from cloudpss_skills_v2.poweranalysis.vsi_weak_bus import VSIWeakBusAnalysis


class TestVSIWeakBusAnalysis:
    @pytest.fixture
    def instance(self):
        return VSIWeakBusAnalysis()

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_import(self):
        assert VSIWeakBusAnalysis is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_class_attributes(self, instance):
        assert hasattr(instance, "name") or hasattr(instance, "run")

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_config_schema(self, instance):
        schema = instance.config_schema
        assert isinstance(schema, dict)
        assert "properties" in schema

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_get_default_config(self, instance):
        if hasattr(instance, "get_default_config"):
            config = instance.get_default_config()
            assert isinstance(config, dict)
