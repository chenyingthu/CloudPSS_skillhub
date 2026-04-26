"""Tests for cloudpss_skills_v2.libs.algo_lib."""

import pytest
from cloudpss_skills_v2.libs.algo_lib import (
    NewtonRaphsonSolver,
    FastDecoupledSolver,
    IEC60909Calculator,
)


class TestNewtonRaphsonSolver:
    def test_import(self):
        """Smoke test: module and class can be imported."""
        assert NewtonRaphsonSolver is not None

    def test_instantiation(self):
        """Smoke test: class can be instantiated."""
        instance = NewtonRaphsonSolver()
        assert instance is not None

    def test_has_name_attribute(self):
        """Smoke test: instance has expected attributes."""
        instance = NewtonRaphsonSolver()
        assert hasattr(instance, "name") or hasattr(instance, "solve")
