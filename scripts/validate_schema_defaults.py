#!/usr/bin/env python3
"""Schema/Default 一致性检查脚本

检查所有技能的 config_schema 和 get_default_config() 是否一致。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills_v2.registry import SkillRegistry, list_skills, get_skill


def get_schema_defaults(schema: dict, path: str = "") -> Dict[str, Any]:
    """从 JSON Schema 中提取所有 default 值。"""
    defaults = {}

    if not isinstance(schema, dict):
        return defaults

    # 当前路径的 default
    if "default" in schema:
        defaults[path] = schema["default"]

    # 递归处理 properties
    if "properties" in schema and isinstance(schema["properties"], dict):
        for key, value in schema["properties"].items():
            new_path = f"{path}.{key}" if path else key
            defaults.update(get_schema_defaults(value, new_path))

    # 处理 items (数组)
    if "items" in schema and isinstance(schema["items"], dict):
        defaults.update(get_schema_defaults(schema["items"], f"{path}[]"))

    return defaults


def get_config_defaults(config: dict, path: str = "") -> Dict[str, Any]:
    """从配置字典中提取所有值。"""
    defaults = {}

    if not isinstance(config, dict):
        return defaults

    for key, value in config.items():
        new_path = f"{path}.{key}" if path else key

        if isinstance(value, dict):
            defaults.update(get_config_defaults(value, new_path))
        else:
            defaults[new_path] = value

    return defaults


def compare_defaults(
    schema_defaults: Dict[str, Any], config_defaults: Dict[str, Any]
) -> List[Tuple[str, Any, Any]]:
    """比较两组默认值，返回不一致的字段。"""
    inconsistencies = []

    # 检查 schema 中有 default 但 config 中没有的字段
    for path, schema_value in schema_defaults.items():
        if path not in config_defaults:
            inconsistencies.append((path, schema_value, "MISSING_IN_CONFIG"))
        elif config_defaults[path] != schema_value:
            inconsistencies.append((path, schema_value, config_defaults[path]))

    # 检查 config 中有但 schema 中没有 default 的字段
    for path, config_value in config_defaults.items():
        if path not in schema_defaults:
            inconsistencies.append((path, "MISSING_IN_SCHEMA", config_value))

    return inconsistencies


def check_skill(skill_name: str) -> List[Tuple[str, Any, Any]]:
    """检查单个技能的 schema 和 default_config 一致性。"""
    skill_class = get_skill(skill_name)
    if skill_class is None:
        return []

    try:
        skill_instance = skill_class()
    except Exception as e:
        print(f"  ⚠️  无法实例化 {skill_name}: {e}")
        return []

    # 获取 schema
    try:
        schema = skill_instance.config_schema if hasattr(skill_instance, 'config_schema') else {}
    except Exception as e:
        print(f"  ⚠️  无法获取 {skill_name} 的 schema: {e}")
        schema = {}

    # 获取 default config
    try:
        default_config = skill_instance.get_default_config() if hasattr(skill_instance, 'get_default_config') else {}
    except Exception as e:
        print(f"  ⚠️  无法获取 {skill_name} 的 default_config: {e}")
        default_config = {}

    schema_defaults = get_schema_defaults(schema)
    config_defaults = get_config_defaults(default_config)

    return compare_defaults(schema_defaults, config_defaults)


def main():
    """主函数。"""
    print("=" * 80)
    print("Schema/Default 一致性检查")
    print("=" * 80)
    print()

    # 获取所有技能
    skill_names = list_skills()
    print(f"发现 {len(skill_names)} 个技能")
    print()

    all_issues = []
    consistent_count = 0
    inconsistent_count = 0

    for skill_name in sorted(skill_names):
        issues = check_skill(skill_name)

        if issues:
            inconsistent_count += 1
            all_issues.append((skill_name, issues))
            print(f"❌ {skill_name}: 发现 {len(issues)} 处不一致")
            for path, schema_val, config_val in issues:
                if config_val == "MISSING_IN_CONFIG":
                    print(f"     {path}: schema={schema_val!r}, config=MISSING")
                elif schema_val == "MISSING_IN_SCHEMA":
                    print(f"     {path}: schema=MISSING, config={config_val!r}")
                else:
                    print(f"     {path}: schema={schema_val!r}, config={config_val!r}")
        else:
            consistent_count += 1
            print(f"✅ {skill_name}: 一致")

    print()
    print("=" * 80)
    print("检查汇总")
    print("=" * 80)
    print(f"一致的技能: {consistent_count}")
    print(f"不一致的技能: {inconsistent_count}")
    print(f"总计: {len(skill_names)}")
    print()

    if all_issues:
        print("需要修复的技能列表:")
        for skill_name, issues in all_issues:
            print(f"  - {skill_name} ({len(issues)} 处)")
        return 1
    else:
        print("✅ 所有技能的 schema 和 default_config 完全一致！")
        return 0


if __name__ == "__main__":
    sys.exit(main())
