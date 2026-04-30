#!/usr/bin/env python3
"""Enhanced skill schema/default consistency fixer."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills_v2.registry import get_skill


def fix_skill(skill_name: str) -> tuple[bool, list[str]]:
    """Fix schema/default issues for a skill by analyzing both."""
    skill_class = get_skill(skill_name)
    if skill_class is None:
        return False, [f"Skill {skill_name} not found"]

    try:
        skill = skill_class()
        schema = skill.config_schema
        config = skill.get_default_config()
    except Exception as e:
        return False, [f"Cannot instantiate skill: {e}"]

    # Find the skill file
    module = skill_class.__module__
    module_file = sys.modules[module].__file__
    if not module_file:
        return False, ["Cannot find skill file"]

    filepath = Path(module_file)
    content = filepath.read_text()
    original = content
    fixes = []

    # Fix 1: Ensure skill has default matching config
    if 'skill' in config:
        skill_val = config['skill']
        # Add default to schema if missing
        if f'"skill": {{"type": "string", "const": "{skill_val}"}}' in content:
            content = content.replace(
                f'"skill": {{"type": "string", "const": "{skill_val}"}}',
                f'"skill": {{"type": "string", "const": "{skill_val}", "default": "{skill_val}"}}'
            )
            fixes.append(f"Added default to skill='{skill_val}'")

    # Fix 2: engine mismatch
    if 'engine' in config and 'engine' in str(schema):
        config_engine = config['engine']
        # Check if schema has different default
        if f'"default": "cloudpss"' in content and config_engine != 'cloudpss':
            content = content.replace(
                '"default": "cloudpss"',
                f'"default": "{config_engine}"',
                1  # Only first occurrence (usually the engine field)
            )
            fixes.append(f"Fixed engine default to '{config_engine}'")

    # Fix 3: model.rid default
    if 'model' in config and isinstance(config['model'], dict):
        model_config = config['model']
        if 'rid' in model_config:
            rid_val = model_config['rid']
            # Check if schema has rid without default
            if '"rid": {"type": "string"}' in content:
                content = content.replace(
                    '"rid": {"type": "string"}',
                    f'"rid": {{"type": "string", "default": "{rid_val}"}}'
                )
                fixes.append(f"Added default to model.rid='{rid_val}'")

    # Fix 4: models array default
    if 'models' in config and isinstance(config['models'], list):
        models_val = config['models']
        if '"models": {' in content and '"default":' not in content.split('"models":')[1].split('}')[0]:
            # Need to add default to models array - this is complex, skip for now
            pass

    # Fix 5: Add missing analysis defaults
    if 'analysis' in config and isinstance(config['analysis'], dict):
        analysis_config = config['analysis']
        for key, val in analysis_config.items():
            if isinstance(val, (list, bool, int, float, str)):
                # Check if this key exists in schema without default
                # This is a simplified check
                pass

    # Fix 6: Add missing output defaults
    if 'output' in config and isinstance(config['output'], dict):
        output_config = config['output']
        for key, val in output_config.items():
            if isinstance(val, (bool, int, float, str)):
                # Check if schema has this key without default
                pass

    # Write back if changes were made
    if content != original:
        filepath.write_text(content)
        return True, fixes

    return False, ["No changes needed"]


def main():
    skills_to_fix = [
        'contingency_analysis',
        'emt_simulation',
        'n1_security',
        'short_circuit',
        'transient_stability',
        'voltage_stability',
    ]

    for skill_name in skills_to_fix:
        print(f"Processing {skill_name}...")
        try:
            fixed, fixes = fix_skill(skill_name)
            if fixed:
                print(f"  ✅ Fixed: {', '.join(fixes)}")
            else:
                print(f"  ℹ️  {fixes[0]}")
        except Exception as e:
            print(f"  ❌ Error: {e}")


if __name__ == "__main__":
    main()
