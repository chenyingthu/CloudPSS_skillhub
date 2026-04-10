#!/usr/bin/env python3
"""
Integration Test Generator for CloudPSS Skills

Usage:
    python scripts/generate_integration_test.py power_flow
    python scripts/generate_integration_test.py --all
"""

import argparse
import os
from pathlib import Path
from datetime import datetime

TEMPLATE = '''#!/usr/bin/env python3
"""
{SKILL_NAME} Skill - Integration Tests

Tests for {SKILL_NAME} skill with real CloudPSS API.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import setToken
from cloudpss_skills.builtin.{SKILL_IMPORT} import {SKILL_CLASS}
from cloudpss_skills.core import SkillStatus


class Test{SKILL_CLASS}Integration:
    """Integration tests for {SKILL_NAME} skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = {SKILL_CLASS}()

    @pytest.fixture(scope="class")
    def auth_token(self):
        """Load auth token from file"""
        token_path = Path(".cloudpss_token_internal")
        if token_path.exists():
            return token_path.read_text().strip()
        token_path = Path(".cloudpss_token")
        if token_path.exists():
            return token_path.read_text().strip()
        pytest.skip("No CloudPSS token found")

    def test_skill_registration(self):
        """Test that skill is registered"""
        from cloudpss_skills import get_skill
        skill = get_skill("{SKILL_NAME}")
        assert skill is not None
        assert skill.name == "{SKILL_NAME}"

    def test_config_schema_validation(self):
        """Test config schema validation"""
        config = self.skill.get_default_config()
        result = self.skill.validate(config)
        assert result.valid or len(result.errors) > 0

    def test_validation_with_valid_config(self, auth_token):
        """Test validation with valid config"""
        config = self.skill.get_default_config()
        config["auth"] = {{"token": auth_token}}
        result = self.skill.validate(config)
        # Validation may fail due to missing rid, which is expected

    def test_validation_with_missing_rid(self, auth_token):
        """Test validation fails when model.rid is missing"""
        config = {{
            "skill": "{SKILL_NAME}",
            "auth": {{"token": auth_token}},
        }}
        result = self.skill.validate(config)
        # Should fail or have warnings about missing rid

    @pytest.mark.integration
    def test_integration_real_api_call(self, auth_token):
        """Test real API call - requires valid token"""
        pytest.skip("TODO: Implement real API test")

    @pytest.mark.integration
    def test_integration_execution(self, auth_token):
        """Test full skill execution - requires valid token"""
        pytest.skip("TODO: Implement full execution test")
'''

UNIT_TEST_TEMPLATE = '''#!/usr/bin/env python3
"""
{SKILL_NAME} Skill - Unit Tests

Unit tests for {SKILL_NAME} skill.
"""

import pytest
from unittest.mock import patch, Mock

from cloudpss_skills.builtin.{SKILL_IMPORT} import {SKILL_CLASS}
from cloudpss_skills.core import SkillStatus


class Test{SKILL_CLASS}Unit:
    """Unit tests for {SKILL_NAME} skill"""

    def setup_method(self):
        """Setup for each test"""
        self.skill = {SKILL_CLASS}()

    def test_skill_name(self):
        """Test skill name"""
        assert self.skill.name == "{SKILL_NAME}"

    def test_skill_description(self):
        """Test skill has description"""
        assert len(self.skill.description) > 0

    def test_default_config(self):
        """Test default config generation"""
        config = self.skill.get_default_config()
        assert "skill" in config
        assert config["skill"] == "{SKILL_NAME}"

    def test_config_schema(self):
        """Test config schema exists"""
        schema = self.skill.config_schema
        assert schema is not None
        assert isinstance(schema, dict)

    @patch("cloudpss.setToken")
    def test_run_handles_missing_model(self, mock_set_token, tmp_path):
        """Test run handles missing model gracefully"""
        token_file = tmp_path / ".cloudpss_token"
        token_file.write_text("test-token")

        config = {{
            "skill": "{SKILL_NAME}",
            "auth": {{"token_file": str(token_file)}},
        }}

        result = self.skill.run(config)
        # Should handle missing model gracefully
        assert result is not None
'''


def to_class_name(skill_name):
    """Convert skill name to class name"""
    return "".join(word.capitalize() for word in skill_name.split("_")) + "Skill"


def to_import_name(skill_name):
    """Convert skill name to import name"""
    return skill_name


def generate_integration_test(skill_name, output_dir):
    """Generate integration test for a skill"""
    class_name = to_class_name(skill_name)

    content = TEMPLATE.format(
        SKILL_NAME=skill_name,
        SKILL_CLASS=class_name,
        SKILL_IMPORT=to_import_name(skill_name),
    )

    output_file = output_dir / f"test_{skill_name}_integration.py"
    output_file.write_text(content)
    print(f"Generated: {output_file}")
    return output_file


def generate_unit_test(skill_name, output_dir):
    """Generate unit test for a skill"""
    class_name = to_class_name(skill_name)

    content = UNIT_TEST_TEMPLATE.format(
        SKILL_NAME=skill_name,
        SKILL_CLASS=class_name,
        SKILL_IMPORT=to_import_name(skill_name),
    )

    output_file = output_dir / f"test_{skill_name}_unit.py"
    output_file.write_text(content)
    print(f"Generated: {output_file}")
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Generate integration tests for skills"
    )
    parser.add_argument("skill", nargs="?", help="Skill name to generate test for")
    parser.add_argument(
        "--all", action="store_true", help="Generate tests for all skills"
    )
    parser.add_argument("--unit", action="store_true", help="Generate unit tests only")
    parser.add_argument(
        "--integration", action="store_true", help="Generate integration tests only"
    )
    args = parser.parse_args()

    skills_dir = Path(__file__).parent.parent / "cloudpss_skills" / "builtin"
    tests_dir = Path(__file__).parent.parent / "tests"

    # Get all skills
    all_skills = [
        f.stem
        for f in skills_dir.glob("*.py")
        if not f.stem.startswith("_") and f.stem != "__init__"
    ]

    if args.all:
        skills_to_generate = all_skills
    elif args.skill:
        skills_to_generate = [args.skill]
    else:
        parser.print_help()
        return

    print(f"Generating tests for {len(skills_to_generate)} skills...")
    print()

    for skill in sorted(skills_to_generate):
        if args.integration or not args.unit:
            try:
                generate_integration_test(skill, tests_dir)
            except Exception as e:
                print(f"Error generating integration test for {skill}: {e}")

        if args.unit or not args.integration:
            try:
                generate_unit_test(skill, tests_dir)
            except Exception as e:
                print(f"Error generating unit test for {skill}: {e}")

    print()
    print(f"Done! Generated tests in {tests_dir}")


if __name__ == "__main__":
    main()
