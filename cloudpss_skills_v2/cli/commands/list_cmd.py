"""CloudPSS Skills V2 CLI - List Command.

列出所有可用的技能。
"""

import argparse
import json
import sys
from typing import Dict, List

from cloudpss_skills_v2.registry import list_skills, SkillRegistry

# Global skill registry instance for use by other commands
SKILL_REGISTRY = SkillRegistry()


def cmd_list(args: argparse.Namespace) -> int:
    """列出可用技能

    Args:
        args: 命令行参数

    Returns:
        int: 退出码，0表示成功
    """
    # 获取所有技能
    all_skills = SkillRegistry.list_all()

    if not all_skills:
        print("暂无可用技能")
        return 0

    # 按类别分组
    categories: Dict[str, List[str]] = {}
    for name, info in all_skills.items():
        category = info.category
        if category not in categories:
            categories[category] = []
        categories[category].append(name)

    # 如果指定了类别过滤
    if hasattr(args, "category") and args.category:
        if args.category not in categories:
            print(f"未找到类别 '{args.category}' 的技能")
            print(f"可用类别: {', '.join(sorted(categories.keys()))}")
            return 1
        categories = {args.category: categories[args.category]}

    # 输出技能列表
    total_count = len(all_skills)
    print(f"\n可用技能 ({total_count}个):")
    print("-" * 60)

    for category in sorted(categories.keys()):
        skills = sorted(categories[category])
        print(f"\n[{category}] ({len(skills)}个)")
        for skill_name in skills:
            info = all_skills[skill_name]
            desc = info.description or "暂无描述"
            print(f"  {skill_name:<30} - {desc}")

    print()
    return 0
