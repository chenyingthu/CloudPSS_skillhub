#!/usr/bin/env python3
"""Fix skill schema/default consistency issues."""

import re
import sys
from pathlib import Path


def fix_skill_file(filepath: Path) -> tuple[bool, list[str]]:
    """Fix common schema issues in a skill file."""
    content = filepath.read_text()
    original = content
    fixes = []

    # Fix 1: Add default to skill const
    skill_pattern = r'("skill"):\s*\{"type":\s*"string",\s*"const":\s*"([^"]+)"\s*\}'
    if re.search(skill_pattern, content):
        content = re.sub(
            skill_pattern,
            r'\1: {"type": "string", "const": "\2", "default": "\2"}',
            content
        )
        fixes.append("Added default to skill field")

    # Fix 2: Add default to model.rid if it's a string type without default
    rid_pattern = r'("rid"):\s*\{"type":\s*"string"\s*\}'
    if re.search(rid_pattern, content):
        content = re.sub(
            rid_pattern,
            r'\1: {"type": "string", "default": "model/holdme/IEEE39"}',
            content
        )
        fixes.append("Added default to model.rid field")

    # Fix 3: Fix analysis.branches missing default
    branches_pattern = r'("branches"):\s*\{\s*"type":\s*"array"[^}]*\}'
    if re.search(branches_pattern, content):
        content = re.sub(
            branches_pattern,
            r'\1: {"type": "array", "items": {"type": "string"}, "default": []}',
            content
        )
        fixes.append("Added default to analysis.branches")

    # Write back if changes were made
    if content != original:
        filepath.write_text(content)
        return True, fixes

    return False, fixes


def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_skill_schema.py <skill_file_or_directory>")
        sys.exit(1)

    path = Path(sys.argv[1])

    if path.is_file():
        files = [path]
    else:
        files = list(path.rglob("*.py"))

    total_fixed = 0
    for filepath in files:
        if "test" in filepath.name or "__" in filepath.name:
            continue

        try:
            fixed, fixes = fix_skill_file(filepath)
            if fixed:
                print(f"✅ Fixed {filepath}: {', '.join(fixes)}")
                total_fixed += 1
        except Exception as e:
            print(f"❌ Error processing {filepath}: {e}")

    print(f"\nTotal files fixed: {total_fixed}")


if __name__ == "__main__":
    main()
