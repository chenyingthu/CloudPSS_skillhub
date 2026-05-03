"""Run Command - Execute analysis skills via CLI.

用法:
    cloudpss-skills run --config <config_file>
    cloudpss-skills run --model <model_id> --engine <engine_name>
"""

from __future__ import annotations

import json
import logging
import sys
from argparse import Namespace
from pathlib import Path
from typing import Any

import yaml

from cloudpss_skills_v2.cli.commands.list_cmd import SKILL_REGISTRY
from cloudpss_skills_v2.core.skill_result import SkillResult, SkillStatus

logger = logging.getLogger(__name__)


def print_error(message: str) -> None:
    """Print error message."""
    print(f"[ERROR] {message}", file=sys.stderr)


def print_success(message: str) -> None:
    """Print success message."""
    print(f"[OK] {message}")


def print_info(message: str) -> None:
    """Print info message."""
    print(f"[INFO] {message}")


def print_warning(message: str) -> None:
    """Print warning message."""
    print(f"[WARN] {message}")


def _parse_config(config_source: str) -> dict[str, Any]:
    """Parse configuration from file path or JSON string.

    Args:
        config_source: Path to config file (YAML/JSON) or JSON string

    Returns:
        Configuration dictionary

    Raises:
        ValueError: If config cannot be parsed
        FileNotFoundError: If config file does not exist
    """
    config_path = Path(config_source)

    # Check if it's a file path
    if config_path.exists():
        content = config_path.read_text(encoding="utf-8")

        # Try YAML first (also handles JSON)
        try:
            return yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse config file: {e}")
    else:
        # Try to parse as JSON string
        try:
            return json.loads(config_source)
        except json.JSONDecodeError as e:
            raise ValueError(f"Config is neither a valid file path nor valid JSON: {e}")


def _run_analysis(config: dict[str, Any]) -> SkillResult:
    """Run analysis with the given configuration.

    Args:
        config: Configuration dictionary containing skill, model, etc.

    Returns:
        SkillResult with analysis results
    """
    # Get skill name from config
    skill_name = config.get("skill")
    if not skill_name:
        return SkillResult.failure(
            skill_name="unknown",
            error="Configuration missing 'skill' field",
            stage="validation"
        )

    # Get skill class from registry
    skill_class = SKILL_REGISTRY.get(skill_name)
    if skill_class is None:
        available = SKILL_REGISTRY.list_skills()
        return SkillResult.failure(
            skill_name=skill_name,
            error=f"Skill '{skill_name}' not found. Available: {', '.join(available)}",
            stage="skill_lookup"
        )

    # Create skill instance
    try:
        skill = skill_class()
    except Exception as e:
        return SkillResult.failure(
            skill_name=skill_name,
            error=f"Failed to create skill instance: {e}",
            stage="instantiation"
        )

    # Validate configuration
    try:
        is_valid, errors = skill.validate(config)
        if not is_valid:
            return SkillResult.failure(
                skill_name=skill_name,
                error=f"Configuration validation failed: {'; '.join(errors)}",
                stage="validation"
            )
    except Exception as e:
        return SkillResult.failure(
            skill_name=skill_name,
            error=f"Validation error: {e}",
            stage="validation"
        )

    # Run the skill
    print_info(f"Executing skill: {skill_name}")
    try:
        result = skill.run(config)
        return result
    except Exception as e:
        return SkillResult.failure(
            skill_name=skill_name,
            error=f"Execution failed: {e}",
            stage="execution"
        )


def execute(args: Namespace) -> int:
    """Execute the run command.

    Args:
        args: Command line arguments with attributes:
            - config: Path to config file
            - model: Model ID (optional)
            - engine: Engine/skill name (optional)
            - output: Output file path (optional)
            - verbose: Enable verbose output (optional)

    Returns:
        Exit code: 0 for success, 1 for error
    """
    try:
        # Build configuration from args
        if args.config:
            # Load from config file
            print_info(f"Loading configuration from: {args.config}")
            config = _parse_config(args.config)
        elif args.model and args.engine:
            # Build config from command line args
            config = {
                "skill": args.engine,
                "model": {"rid": args.model}
            }
            if hasattr(args, 'unified') and args.unified:
                config["unified"] = True
        else:
            print_error("Either --config or both --model and --engine are required")
            return 1

        # Run the analysis
        result = _run_analysis(config)

        # Output results
        result_dict = result.to_dict()

        if args.output:
            # Write to output file
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result_dict, f, indent=2, ensure_ascii=False)
            print_success(f"Results written to: {args.output}")
        else:
            # Print to stdout
            print(json.dumps(result_dict, indent=2, ensure_ascii=False))

        # Return appropriate exit code
        return 0 if result.is_success else 1

    except FileNotFoundError as e:
        print_error(f"Configuration file not found: {e}")
        return 1
    except ValueError as e:
        print_error(f"Configuration error: {e}")
        return 1
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if hasattr(args, 'verbose') and args.verbose:
            import traceback
            traceback.print_exc()
        return 1


__all__ = ["execute", "_parse_config", "_run_analysis", "SKILL_REGISTRY"]
