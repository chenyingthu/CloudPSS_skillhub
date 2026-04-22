import os
import pytest
import tempfile
from cloudpss_skills_v2.tools.report_generator import ReportGeneratorTool


class TestReportGeneratorTool:
    def test_import(self):
        assert ReportGeneratorTool is not None

    def test_instantiation(self):
        instance = ReportGeneratorTool()
        assert instance is not None

    def test_has_name_attribute(self):
        instance = ReportGeneratorTool()
        assert instance.name == "report_generator"

    def test_has_description(self):
        instance = ReportGeneratorTool()
        assert hasattr(instance, "description")

    def test_has_config_schema(self):
        instance = ReportGeneratorTool()
        schema = instance.config_schema
        assert schema is not None
        assert schema["type"] == "object"

    def test_validate_empty_config(self):
        instance = ReportGeneratorTool()
        valid, errors = instance.validate({})
        assert valid is False

    def test_validate_missing_report(self):
        instance = ReportGeneratorTool()
        config = {"model": {"rid": "test"}}
        valid, errors = instance.validate(config)
        assert valid is False

    def test_validate_valid_config(self):
        instance = ReportGeneratorTool()
        config = {"report": {"title": "Test"}}
        valid, errors = instance.validate(config)
        assert valid is True

    def test_run_returns_skill_result(self):
        instance = ReportGeneratorTool()
        result = instance.run({"report": {}})
        assert result is not None
        assert hasattr(result, "skill_name")
        assert hasattr(result, "status")

    def test_has_log_method(self):
        instance = ReportGeneratorTool()
        assert hasattr(instance, "_log")
        assert callable(instance._log)
