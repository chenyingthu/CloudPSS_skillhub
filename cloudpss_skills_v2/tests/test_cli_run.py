"""
Tests for CLI run command.

TDD approach: Write tests first, then implement the run command.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
from argparse import Namespace


class TestRunCommandImports:
    """Test that run command module can be imported."""

    def test_run_cmd_import(self):
        """Test that run_cmd module can be imported."""
        from cloudpss_skills_v2.cli.commands import run_cmd
        assert run_cmd is not None

    def test_execute_function_exists(self):
        """Test that execute function exists."""
        from cloudpss_skills_v2.cli.commands.run_cmd import execute
        assert callable(execute)


class TestRunCommandArguments:
    """Test run command argument parsing."""

    def test_execute_with_config_file(self, tmp_path):
        """Test running with config file path."""
        from cloudpss_skills_v2.cli.commands.run_cmd import execute

        # Create a real config file
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("""
skill: power_flow
model:
  rid: test/model
""")

        args = Namespace(
            config=str(config_file),
            model=None,
            engine=None,
            output=None,
            verbose=False,
            unified=False
        )

        # Mock the skill registry
        mock_skill_instance = Mock()
        mock_skill_instance.validate = Mock(return_value=(True, []))
        mock_skill_instance.run = Mock(return_value=Mock(
            is_success=True,
            to_dict=Mock(return_value={"status": "success"})
        ))
        mock_skill_class = Mock(return_value=mock_skill_instance)

        with patch('cloudpss_skills_v2.cli.commands.run_cmd.SKILL_REGISTRY') as mock_reg:
            mock_reg.get.return_value = mock_skill_class

            result = execute(args)
            assert result == 0

    def test_execute_with_missing_config_file(self):
        """Test error handling when config file does not exist."""
        from cloudpss_skills_v2.cli.commands.run_cmd import execute

        args = Namespace(
            config="nonexistent.yaml",
            model=None,
            engine=None,
            output=None,
            verbose=False,
            unified=False
        )

        result = execute(args)
        assert result == 1

    def test_execute_with_model_flag(self):
        """Test running with --model flag."""
        from cloudpss_skills_v2.cli.commands.run_cmd import execute

        args = Namespace(
            config=None,
            model="model/holdme/IEEE39",
            engine="power_flow",
            output=None,
            verbose=False,
            unified=False
        )

        mock_skill_instance = Mock()
        mock_skill_instance.validate = Mock(return_value=(True, []))
        mock_skill_instance.run = Mock(return_value=Mock(
            is_success=True,
            to_dict=Mock(return_value={"status": "success"})
        ))
        mock_skill_class = Mock(return_value=mock_skill_instance)

        with patch('cloudpss_skills_v2.cli.commands.run_cmd.SKILL_REGISTRY') as mock_reg:
            mock_reg.get.return_value = mock_skill_class

            result = execute(args)
            assert result == 0


class TestRunCommandOutput:
    """Test run command output handling."""

    def test_execute_outputs_json(self, tmp_path):
        """Test that results are output as JSON."""
        from cloudpss_skills_v2.cli.commands.run_cmd import execute

        # Create config file
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("skill: power_flow\nmodel:\n  rid: test")

        output_file = tmp_path / "result.json"
        args = Namespace(
            config=str(config_file),
            model=None,
            engine=None,
            output=str(output_file),
            verbose=False,
            unified=False
        )

        mock_skill_instance = Mock()
        mock_skill_instance.validate = Mock(return_value=(True, []))
        mock_skill_instance.run = Mock(return_value=Mock(
            is_success=True,
            to_dict=Mock(return_value={"status": "success", "data": {}})
        ))
        mock_skill_class = Mock(return_value=mock_skill_instance)

        with patch('cloudpss_skills_v2.cli.commands.run_cmd.SKILL_REGISTRY') as mock_reg:
            mock_reg.get.return_value = mock_skill_class

            result = execute(args)
            assert result == 0
            assert output_file.exists()


class TestRunCommandErrorHandling:
    """Test run command error handling."""

    def test_execute_returns_error_code_on_failure(self, tmp_path):
        """Test that execute returns 1 on failure."""
        from cloudpss_skills_v2.cli.commands.run_cmd import execute

        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("skill: power_flow\nmodel:\n  rid: test")

        args = Namespace(
            config=str(config_file),
            model=None,
            engine=None,
            output=None,
            verbose=False,
            unified=False
        )

        mock_skill_instance = Mock()
        mock_skill_instance.validate = Mock(return_value=(True, []))
        mock_skill_instance.run = Mock(return_value=Mock(
            is_success=False,
            to_dict=Mock(return_value={"status": "failed", "error": "test error"})
        ))
        mock_skill_class = Mock(return_value=mock_skill_instance)

        with patch('cloudpss_skills_v2.cli.commands.run_cmd.SKILL_REGISTRY') as mock_reg:
            mock_reg.get.return_value = mock_skill_class

            result = execute(args)
            assert result == 1

    def test_execute_handles_skill_not_found(self, tmp_path):
        """Test error when skill is not found."""
        from cloudpss_skills_v2.cli.commands.run_cmd import execute

        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("skill: nonexistent_skill\nmodel:\n  rid: test")

        args = Namespace(
            config=str(config_file),
            model=None,
            engine=None,
            output=None,
            verbose=False,
            unified=False
        )

        with patch('cloudpss_skills_v2.cli.commands.run_cmd.SKILL_REGISTRY') as mock_reg:
            mock_reg.get.return_value = None
            mock_reg.list_skills.return_value = ["power_flow", "n1_security"]

            result = execute(args)
            assert result == 1

    def test_execute_handles_exception(self, tmp_path):
        """Test that execute handles exceptions gracefully."""
        from cloudpss_skills_v2.cli.commands.run_cmd import execute

        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("skill: power_flow\nmodel:\n  rid: test")

        args = Namespace(
            config=str(config_file),
            model=None,
            engine=None,
            output=None,
            verbose=False,
            unified=False
        )

        with patch('cloudpss_skills_v2.cli.commands.run_cmd.SKILL_REGISTRY') as mock_reg:
            mock_reg.get.side_effect = Exception("Test exception")

            result = execute(args)
            assert result == 1


class TestRunCommandSKILLREGISTRY:
    """Test that SKILL_REGISTRY is used from list_cmd."""

    def test_skill_registry_import(self):
        """Test that SKILL_REGISTRY is imported from list_cmd."""
        from cloudpss_skills_v2.cli.commands.run_cmd import SKILL_REGISTRY
        from cloudpss_skills_v2.cli.commands.list_cmd import SKILL_REGISTRY as LIST_REGISTRY
        assert SKILL_REGISTRY is LIST_REGISTRY


class TestRunCommandConfigParsing:
    """Test configuration parsing."""

    def test_parse_config_from_json_string(self):
        """Test parsing config from JSON string."""
        from cloudpss_skills_v2.cli.commands.run_cmd import _parse_config

        json_str = '{"skill": "power_flow", "model": {"rid": "test"}}'
        result = _parse_config(json_str)

        assert result == {"skill": "power_flow", "model": {"rid": "test"}}

    def test_parse_config_from_yaml_file(self, tmp_path):
        """Test parsing config from YAML file."""
        from cloudpss_skills_v2.cli.commands.run_cmd import _parse_config

        config_file = tmp_path / "config.yaml"
        config_file.write_text("skill: power_flow\nmodel:\n  rid: test")

        result = _parse_config(str(config_file))
        assert result == {"skill": "power_flow", "model": {"rid": "test"}}

    def test_parse_config_invalid_json(self):
        """Test parsing invalid JSON."""
        from cloudpss_skills_v2.cli.commands.run_cmd import _parse_config

        with pytest.raises(ValueError):
            _parse_config("invalid json {{{")


class TestRunCommandEngineAndModel:
    """Test engine and model handling."""

    def test_create_engine_runs_power_flow(self, tmp_path):
        """Test that engine creation and power flow execution works."""
        from cloudpss_skills_v2.cli.commands.run_cmd import _run_analysis

        config = {
            "skill": "power_flow",
            "model": {"rid": "test/model"},
            "engine": {"type": "power_flow"}
        }

        mock_skill_instance = Mock()
        mock_skill_instance.validate = Mock(return_value=(True, []))
        mock_skill_instance.run = Mock(return_value=Mock(
            is_success=True,
            to_dict=Mock(return_value={"status": "success", "data": {}})
        ))
        mock_skill_class = Mock(return_value=mock_skill_instance)

        with patch('cloudpss_skills_v2.cli.commands.run_cmd.SKILL_REGISTRY') as mock_reg:
            mock_reg.get.return_value = mock_skill_class

            result = _run_analysis(config)
            assert result.is_success

    def test_unified_model_integration(self, tmp_path):
        """Test unified model integration."""
        from cloudpss_skills_v2.cli.commands.run_cmd import _run_analysis

        config = {
            "skill": "n1_security",
            "model": {"rid": "test/model"},
            "unified": True
        }

        mock_skill_instance = Mock()
        mock_skill_instance.validate = Mock(return_value=(True, []))
        mock_skill_instance.run = Mock(return_value=Mock(
            is_success=True,
            to_dict=Mock(return_value={"status": "success", "data": {}})
        ))
        mock_skill_class = Mock(return_value=mock_skill_instance)

        with patch('cloudpss_skills_v2.cli.commands.run_cmd.SKILL_REGISTRY') as mock_reg:
            mock_reg.get.return_value = mock_skill_class

            result = _run_analysis(config)
            assert result.is_success


class TestRunCommandMissingArgs:
    """Test error handling for missing arguments."""

    def test_execute_requires_config_or_model_engine(self):
        """Test that execute requires either config or both model and engine."""
        from cloudpss_skills_v2.cli.commands.run_cmd import execute

        args = Namespace(
            config=None,
            model=None,
            engine=None,
            output=None,
            verbose=False,
            unified=False
        )

        result = execute(args)
        assert result == 1

    def test_execute_requires_model_when_engine_given(self):
        """Test that execute requires model when engine is given."""
        from cloudpss_skills_v2.cli.commands.run_cmd import execute

        args = Namespace(
            config=None,
            model=None,
            engine="power_flow",
            output=None,
            verbose=False,
            unified=False
        )

        result = execute(args)
        assert result == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
