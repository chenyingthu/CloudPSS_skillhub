#!/usr/bin/env python3
"""Generate get_default_config method from schema."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills_v2.registry import get_skill


def extract_defaults(schema: dict, path: str = "") -> dict:
    """Extract default values from schema."""
    result = {}

    if not isinstance(schema, dict):
        return result

    # Handle properties
    if "properties" in schema:
        for key, value in schema["properties"].items():
            if "default" in value:
                result[key] = value["default"]
            elif "properties" in value or "items" in value:
                nested = extract_defaults(value)
                if nested:
                    result[key] = nested

    # Handle items (arrays)
    if "items" in schema and isinstance(schema["items"], dict):
        # Return array with one item containing defaults
        item_defaults = extract_defaults(schema["items"])
        if item_defaults:
            return [item_defaults]
        return []

    return result


def generate_method(skill_name: str) -> str:
    """Generate get_default_config method for a skill."""
    skill_class = get_skill(skill_name)
    if not skill_class:
        return f"# Skill {skill_name} not found"

    try:
        skill = skill_class()
        schema = skill.config_schema
    except Exception as e:
        return f"# Error: {e}"

    # Extract defaults from schema
    defaults = extract_defaults(schema)

    # Add skill name if not present
    if "skill" not in defaults:
        defaults["skill"] = skill_name

    # Format as Python dict
    import json
    dict_str = json.dumps(defaults, indent=4, ensure_ascii=False)
    # Convert JSON to Python dict syntax
    dict_str = dict_str.replace('"', '"').replace("true", "True").replace("false", "False").replace("null", "None")

    return f'''    def get_default_config(self) -> dict[str, Any]:
        return {dict_str}

'''


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_default_config.py <skill_name>")
        sys.exit(1)

    skill_name = sys.argv[1]
    print(generate_method(skill_name))
