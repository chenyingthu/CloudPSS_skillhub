#!/usr/bin/env python3
"""
收纳大师 CLI - 主入口
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from cloudpss_skills_v3.master_organizer.core import (
    get_path_manager, get_config_manager,
    ServerRegistry, CaseRegistry, TaskRegistry, ResultRegistry
)


def cmd_init(args):
    """初始化工作区"""
    pm = get_path_manager(args.path)
    print(f"✅ 工作区初始化完成: {pm.root}")
    return 0


def cmd_status(args):
    """查看系统状态"""
    pm = get_path_manager()
    cm = get_config_manager()

    print("=" * 60)
    print("CloudPSS 收纳大师 - 系统状态")
    print("=" * 60)

    # 统计信息
    cases = CaseRegistry()
    tasks = TaskRegistry()
    results = ResultRegistry()

    print(f"\n📊 实体统计:")
    print(f"  算例数: {cases.count()}")
    print(f"  任务数: {tasks.count()}")
    print(f"  结果数: {results.count()}")

    # 存储使用
    usage = pm.get_storage_usage()
    total_mb = usage.get('total', 0) / (1024 * 1024)
    print(f"\n💾 存储使用: {total_mb:.2f} MB")

    print("\n" + "=" * 60)
    return 0


def cmd_case_list(args):
    """列出算例"""
    registry = CaseRegistry()
    cases = registry.list_all()

    print("=" * 60)
    print("算例列表")
    print("=" * 60)

    if not cases:
        print("  (无算例)")
    else:
        for case_id, case in cases:
            status_icon = "🟢" if case.status == "active" else "⚪"
            print(f"  {status_icon} {case_id}: {case.name} [{case.status}]")

    print("=" * 60)
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="cloudpss-master",
        description="CloudPSS SkillHub 收纳大师"
    )
    subparsers = parser.add_subparsers(dest="command")

    # init 命令
    init_parser = subparsers.add_parser("init", help="初始化工作区")
    init_parser.add_argument("--path", default=None, help="工作区路径")
    init_parser.set_defaults(func=cmd_init)

    # status 命令
    status_parser = subparsers.add_parser("status", help="查看系统状态")
    status_parser.set_defaults(func=cmd_status)

    # case 命令
    case_parser = subparsers.add_parser("case", help="算例管理")
    case_subparsers = case_parser.add_subparsers(dest="case_command")

    case_list_parser = case_subparsers.add_parser("list", help="列出算例")
    case_list_parser.set_defaults(func=cmd_case_list)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 1

    if hasattr(args, "func"):
        return args.func(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
