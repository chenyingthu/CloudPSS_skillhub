#!/usr/bin/env python3
"""
收纳大师 CLI - 主入口
完整实现计划中的所有命令
"""
import argparse
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from cloudpss_skills_v3.master_organizer.core import (
    IDGenerator, EntityType,
    get_path_manager, get_config_manager,
    ServerRegistry, CaseRegistry, TaskRegistry, ResultRegistry,
    Server, Case, Task, Result
)


def cmd_init(args):
    """初始化工作区"""
    pm = get_path_manager(args.path)
    print(f"✅ 工作区初始化完成: {pm.root}")
    print(f"   配置目录: {pm.config_dir}")
    print(f"   注册表目录: {pm.registry_dir}")
    print(f"   算例目录: {pm.cases_dir}")
    print(f"   任务目录: {pm.tasks_dir}")
    print(f"   结果目录: {pm.results_dir}")
    return 0


def cmd_status(args):
    """查看系统状态"""
    pm = get_path_manager()

    print("=" * 60)
    print("CloudPSS 收纳大师 - 系统状态")
    print("=" * 60)

    # 统计信息
    cases = CaseRegistry()
    tasks = TaskRegistry()
    results = ResultRegistry()
    servers = ServerRegistry()

    print(f"\n📊 实体统计:")
    print(f"  服务器数: {servers.count()}")
    print(f"  算例数: {cases.count()}")
    print(f"  任务数: {tasks.count()}")
    print(f"  结果数: {results.count()}")

    # 存储使用
    usage = pm.get_storage_usage()
    total_mb = usage.get('total', 0) / (1024 * 1024)
    print(f"\n💾 存储使用: {total_mb:.2f} MB")

    print("\n" + "=" * 60)
    return 0


# ====== Server 命令 ======
def cmd_server_list(args):
    """列出服务器"""
    registry = ServerRegistry()
    servers = registry.list_all()

    print("=" * 60)
    print("服务器列表")
    print("=" * 60)

    if not servers:
        print("  (无服务器)")
    else:
        for server_id, server in servers:
            status_icon = "🟢" if server.status == "active" else "⚪"
            default_mark = " (默认)" if getattr(server, 'default', False) else ""
            print(f"  {status_icon} {server_id}: {server.name}{default_mark}")
            print(f"      URL: {server.url}")

    print("=" * 60)
    return 0


def cmd_server_add(args):
    """添加服务器"""
    registry = ServerRegistry()

    server_id = IDGenerator.generate(EntityType.SERVER)
    server = Server(
        id=server_id,
        name=args.name,
        url=args.url,
        status="active"
    )

    if registry.create(server_id, server):
        print(f"✅ 服务器添加成功: {server_id}")
        print(f"   名称: {args.name}")
        print(f"   URL: {args.url}")
        if args.default:
            registry.update(server_id, {"default": True})
            print("   已设为默认服务器")
        return 0
    else:
        print(f"❌ 添加失败")
        return 1


def cmd_server_remove(args):
    """删除服务器"""
    registry = ServerRegistry()
    if registry.delete(args.server_id):
        print(f"✅ 服务器已删除: {args.server_id}")
        return 0
    else:
        print(f"❌ 服务器不存在: {args.server_id}")
        return 1


# ====== Case 命令 ======
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
            if case.description:
                print(f"      描述: {case.description}")

    print("=" * 60)
    return 0


def cmd_case_create(args):
    """创建算例"""
    registry = CaseRegistry()

    case_id = IDGenerator.generate(EntityType.CASE)
    case = Case(
        id=case_id,
        name=args.name,
        description=args.description or "",
        rid=args.rid,
        server_id=args.server_id or "",
        status="draft"
    )

    if registry.create(case_id, case):
        print(f"✅ 算例创建成功: {case_id}")
        print(f"   名称: {args.name}")
        print(f"   RID: {args.rid}")
        return 0
    else:
        print(f"❌ 创建失败")
        return 1


def cmd_case_delete(args):
    """删除算例"""
    registry = CaseRegistry()
    if registry.delete(args.case_id):
        print(f"✅ 算例已删除: {args.case_id}")
        return 0
    else:
        print(f"❌ 算例不存在: {args.case_id}")
        return 1


# ====== Task 命令 ======
def cmd_task_list(args):
    """列出任务"""
    registry = TaskRegistry()

    if args.case_id:
        tasks = registry.filter_by(case_id=args.case_id)
        print(f"=" * 60)
        print(f"算例 {args.case_id} 的任务列表")
    else:
        tasks = registry.list_all()
        print("=" * 60)
        print("任务列表")

    print("=" * 60)

    if not tasks:
        print("  (无任务)")
    else:
        for task_id, task in tasks:
            status_icon = {
                "completed": "✅",
                "running": "🔄",
                "failed": "❌",
                "created": "⏳"
            }.get(task.status, "⚪")
            print(f"  {status_icon} {task_id}: {task.name} [{task.status}]")
            print(f"      类型: {task.type}")

    print("=" * 60)
    return 0


def cmd_task_create(args):
    """创建任务"""
    registry = TaskRegistry()

    task_id = IDGenerator.generate(EntityType.TASK)
    task = Task(
        id=task_id,
        name=args.name,
        case_id=args.case_id,
        type=args.type,
        status="created"
    )

    if registry.create(task_id, task):
        print(f"✅ 任务创建成功: {task_id}")
        print(f"   名称: {args.name}")
        print(f"   算例: {args.case_id}")
        print(f"   类型: {args.type}")
        return 0
    else:
        print(f"❌ 创建失败")
        return 1


def cmd_task_delete(args):
    """删除任务"""
    registry = TaskRegistry()
    if registry.delete(args.task_id):
        print(f"✅ 任务已删除: {args.task_id}")
        return 0
    else:
        print(f"❌ 任务不存在: {args.task_id}")
        return 1


# ====== Result 命令 ======
def cmd_result_list(args):
    """列出结果"""
    registry = ResultRegistry()
    results = registry.list_all()

    print("=" * 60)
    print("结果列表")
    print("=" * 60)

    if not results:
        print("  (无结果)")
    else:
        for result_id, result in results:
            print(f"  📊 {result_id}: {result.name}")
            print(f"      格式: {result.format}")
            print(f"      大小: {result.size_bytes} bytes")

    print("=" * 60)
    return 0


# ====== Query 命令 ======
def cmd_query_tree(args):
    """树形视图"""
    pm = get_path_manager()
    cases = CaseRegistry()
    tasks = TaskRegistry()

    print("📁 收纳大师工作区")
    print(f"   根目录: {pm.root}")
    print()

    # 服务器
    servers = ServerRegistry()
    print(f"🖥️  服务器 ({servers.count()}):")
    for server_id, server in servers.list_all():
        print(f"   • {server.name} ({server_id})")
    print()

    # 算例和任务
    print(f"📦 算例 ({cases.count()}):")
    for case_id, case in cases.list_all():
        status_icon = "🟢" if case.status == "active" else "⚪"
        print(f"   {status_icon} {case.name}")
        print(f"      ID: {case_id}")

        # 该算例的任务
        case_tasks = tasks.filter_by(case_id=case_id)
        if case_tasks:
            print(f"      任务:")
            for task_id, task in case_tasks:
                icon = {"completed": "✅", "running": "🔄"}.get(task.status, "⏳")
                print(f"        {icon} {task.name} [{task.status}]")
    print()

    # 统计
    print("📊 统计:")
    print(f"   总任务数: {tasks.count()}")
    print(f"   总结果数: {ResultRegistry().count()}")

    return 0


def cmd_query_dashboard(args):
    """仪表板视图"""
    pm = get_path_manager()
    cases = CaseRegistry()
    tasks = TaskRegistry()
    results = ResultRegistry()

    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "CloudPSS 收纳大师 仪表板" + " " * 18 + "║")
    print("╠" + "═" * 58 + "╣")
    print("║" + " " * 58 + "║")
    print("║  📊 系统状态" + " " * 45 + "║")
    print("║  " + "─" * 54 + " " * 1 + "║")

    # 统计
    completed_tasks = len([t for _, t in tasks.list_all() if t.status == "completed"])
    failed_tasks = len([t for _, t in tasks.list_all() if t.status == "failed"])

    print(f"║  算例数: {cases.count():<5}  任务数: {tasks.count():<5}  结果数: {results.count():<5}" + " " * 12 + "║")
    print(f"║  成功任务: {completed_tasks:<3}  失败任务: {failed_tasks:<3}" + " " * 26 + "║")

    # 存储
    usage = pm.get_storage_usage()
    total_mb = usage.get('total', 0) / (1024 * 1024)
    print(f"║  存储使用: {total_mb:.2f} MB" + " " * 36 + "║")

    print("║" + " " * 58 + "║")
    print("║  📈 最近活动" + " " * 45 + "║")
    print("║  " + "─" * 54 + " " * 1 + "║")

    # 最近任务
    recent_tasks = sorted(tasks.list_all(), key=lambda x: x[1].created_at, reverse=True)[:3]
    if recent_tasks:
        for task_id, task in recent_tasks:
            name = task.name[:20] + "..." if len(task.name) > 20 else task.name
            print(f"║  • {name:<24} [{task.status:<10}]" + " " * 13 + "║")
    else:
        print("║  (无近期活动)" + " " * 44 + "║")

    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")

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

    # server 命令
    server_parser = subparsers.add_parser("server", help="服务器管理")
    server_subparsers = server_parser.add_subparsers(dest="server_command")

    server_list_parser = server_subparsers.add_parser("list", help="列出服务器")
    server_list_parser.set_defaults(func=cmd_server_list)

    server_add_parser = server_subparsers.add_parser("add", help="添加服务器")
    server_add_parser.add_argument("--name", required=True, help="服务器名称")
    server_add_parser.add_argument("--url", required=True, help="服务器URL")
    server_add_parser.add_argument("--default", action="store_true", help="设为默认")
    server_add_parser.set_defaults(func=cmd_server_add)

    server_remove_parser = server_subparsers.add_parser("remove", help="删除服务器")
    server_remove_parser.add_argument("server_id", help="服务器ID")
    server_remove_parser.set_defaults(func=cmd_server_remove)

    # case 命令
    case_parser = subparsers.add_parser("case", help="算例管理")
    case_subparsers = case_parser.add_subparsers(dest="case_command")

    case_list_parser = case_subparsers.add_parser("list", help="列出算例")
    case_list_parser.set_defaults(func=cmd_case_list)

    case_create_parser = case_subparsers.add_parser("create", help="创建算例")
    case_create_parser.add_argument("--name", required=True, help="算例名称")
    case_create_parser.add_argument("--rid", required=True, help="CloudPSS RID")
    case_create_parser.add_argument("--description", help="算例描述")
    case_create_parser.add_argument("--server-id", help="服务器ID")
    case_create_parser.set_defaults(func=cmd_case_create)

    case_delete_parser = case_subparsers.add_parser("delete", help="删除算例")
    case_delete_parser.add_argument("case_id", help="算例ID")
    case_delete_parser.set_defaults(func=cmd_case_delete)

    # task 命令
    task_parser = subparsers.add_parser("task", help="任务管理")
    task_subparsers = task_parser.add_subparsers(dest="task_command")

    task_list_parser = task_subparsers.add_parser("list", help="列出任务")
    task_list_parser.add_argument("--case-id", help="按算例过滤")
    task_list_parser.set_defaults(func=cmd_task_list)

    task_create_parser = task_subparsers.add_parser("create", help="创建任务")
    task_create_parser.add_argument("--name", required=True, help="任务名称")
    task_create_parser.add_argument("--case-id", required=True, help="算例ID")
    task_create_parser.add_argument("--type", required=True, choices=["powerflow", "emt", "stability"], help="任务类型")
    task_create_parser.set_defaults(func=cmd_task_create)

    task_delete_parser = task_subparsers.add_parser("delete", help="删除任务")
    task_delete_parser.add_argument("task_id", help="任务ID")
    task_delete_parser.set_defaults(func=cmd_task_delete)

    # result 命令
    result_parser = subparsers.add_parser("result", help="结果管理")
    result_subparsers = result_parser.add_subparsers(dest="result_command")

    result_list_parser = result_subparsers.add_parser("list", help="列出结果")
    result_list_parser.set_defaults(func=cmd_result_list)

    # query 命令
    query_parser = subparsers.add_parser("query", help="查询")
    query_subparsers = query_parser.add_subparsers(dest="query_command")

    query_tree_parser = query_subparsers.add_parser("tree", help="树形视图")
    query_tree_parser.set_defaults(func=cmd_query_tree)

    query_dashboard_parser = query_subparsers.add_parser("dashboard", help="仪表板")
    query_dashboard_parser.set_defaults(func=cmd_query_dashboard)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 1

    if hasattr(args, "func"):
        return args.func(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
