"""Tests for cloudpss_skills_v2.libs.data_lib."""
import pytest
from cloudpss_skills_v2.libs.data_lib import BusData, BranchData, GeneratorData


class TestBusData:

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_import(self):
        """Smoke test: module and class can be imported."""
        assert BusData is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_instantiation(self):
        """Smoke test: class can be instantiated."""
        instance = BusData(name="Bus 1")
        assert instance is not None

    @pytest.mark.smoke
    @pytest.mark.needs_improvement(
        reason="仅验证导入，需添加业务逻辑验证",
        issue="https://github.com/org/repo/issues/456",
    )
    def test_has_name_attribute(self):
        """Smoke test: instance has expected attributes."""
        instance = BusData(name="Bus 1")
        assert hasattr(instance, 'name') or hasattr(instance, 'run')
