import pytest
from cloudpss_skills_v2.poweranalysis.contingency_analysis import ContingencyAnalysis


class TestContingencyAnalysis:
    @pytest.fixture
    def instance(self):
        return ContingencyAnalysis()

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_import(self):
        assert ContingencyAnalysis is not None

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
        config = instance.get_default_config()
        assert isinstance(config, dict)
