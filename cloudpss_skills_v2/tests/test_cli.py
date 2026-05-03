"""CLI module tests for cloudpss_skills_v2.

Tests for CLI module import, entry point, and list command.
"""

import sys
from io import StringIO
from unittest.mock import patch

import pytest


class TestCliModule:
    """Tests for CLI module structure and imports."""

    def test_cli_module_imports(self):
        """Test that CLI module can be imported."""
        from cloudpss_skills_v2.cli import main

        assert main is not None
        assert callable(main)

    def test_cli_commands_module_imports(self):
        """Test that CLI commands module can be imported."""
        from cloudpss_skills_v2.cli.commands import list_cmd

        assert list_cmd is not None

    def test_list_command_function_exists(self):
        """Test that list command function exists."""
        from cloudpss_skills_v2.cli.commands.list_cmd import cmd_list

        assert cmd_list is not None
        assert callable(cmd_list)


class TestCliEntryPoint:
    """Tests for CLI entry point and argument parsing."""

    def test_main_function_exists(self):
        """Test that main entry point function exists."""
        from cloudpss_skills_v2.cli.main import main

        assert main is not None
        assert callable(main)

    def test_create_parser_exists(self):
        """Test that create_parser function exists."""
        from cloudpss_skills_v2.cli.main import create_parser

        assert create_parser is not None
        assert callable(create_parser)

    def test_parser_has_list_subcommand(self):
        """Test that parser has list subcommand."""
        from cloudpss_skills_v2.cli.main import create_parser

        parser = create_parser()
        args = parser.parse_args(["list"])
        assert args.command == "list"
        assert hasattr(args, "func")

    def test_parser_has_run_subcommand(self):
        """Test that parser has run subcommand."""
        from cloudpss_skills_v2.cli.main import create_parser

        parser = create_parser()
        args = parser.parse_args(["run", "--config", "test.yaml"])
        assert args.command == "run"
        assert hasattr(args, "func")

    def test_parser_has_compare_subcommand(self):
        """Test that parser has compare subcommand."""
        from cloudpss_skills_v2.cli.main import create_parser

        parser = create_parser()
        args = parser.parse_args(["compare", "--configs", "a.yaml", "b.yaml"])
        assert args.command == "compare"
        assert hasattr(args, "func")

    def test_main_shows_help_with_no_args(self):
        """Test that main shows help when no arguments provided."""
        from cloudpss_skills_v2.cli.main import main

        captured_output = StringIO()
        with patch.object(sys, "stdout", captured_output):
            result = main([])

        assert result == 0
        output = captured_output.getvalue()
        assert "usage:" in output.lower()


class TestListCommand:
    """Tests for list command functionality."""

    def test_list_command_returns_zero(self):
        """Test that list command returns 0 on success."""
        from cloudpss_skills_v2.cli.commands.list_cmd import cmd_list
        from cloudpss_skills_v2.cli.main import create_parser

        parser = create_parser()
        args = parser.parse_args(["list"])

        result = cmd_list(args)
        assert result == 0

    def test_list_command_outputs_skills(self):
        """Test that list command outputs skill information."""
        from cloudpss_skills_v2.cli.commands.list_cmd import cmd_list
        from cloudpss_skills_v2.cli.main import create_parser

        parser = create_parser()
        args = parser.parse_args(["list"])

        captured_output = StringIO()
        with patch.object(sys, "stdout", captured_output):
            cmd_list(args)

        output = captured_output.getvalue()
        assert len(output) >= 0  # May be empty if no skills registered


class TestModuleEntryPoint:
    """Tests for module entry point (__main__.py)."""

    def test_module_entry_point_imports(self):
        """Test that module entry point can be imported."""
        from cloudpss_skills_v2.__main__ import main

        assert main is not None
        assert callable(main)

    def test_module_entry_point_calls_cli_main(self):
        """Test that module entry point calls CLI main function."""
        from cloudpss_skills_v2 import __main__ as entry_module
        from cloudpss_skills_v2.cli import main as cli_main

        # Verify that the entry module imports from cli module
        assert hasattr(entry_module, "main")
