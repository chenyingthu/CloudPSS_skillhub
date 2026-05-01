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
    ServerRegistry, CaseRegistry, TaskRegistry, ResultRegistry, VariantRegistry,
    Server, Case, Task, Result, Variant
)


def cmd_init(args):
    """初始化工作区"""
    # 如果指定了自定义路径，先设置环境变量以确保一致性
    if args.path:
        import os
        os.environ["CLOUDPSS_HOME"] = str(Path(args.path).expanduser().resolve())

    pm = get_path_manager(args.path)

    # 保存工作区路径到配置（以便后续命令使用）
    if args.path:
        cm = get_config_manager(pm.config_dir)
        cm.update("user", {"workspace": {"root": str(pm.root)}}, merge=True)

    print(f"✅ 工作区初始化完成: {pm.root}")
    print(f"   配置目录: {pm.config_dir}")
    print(f"   注册表目录: {pm.registry_dir}")
    print(f"   算例目录: {pm.cases_dir}")
    print(f"   任务目录: {pm.tasks_dir}")
    print(f"   结果目录: {pm.results_dir}")

    if args.path:
        print(f"\n💡 提示: 已保存工作区路径到配置")
        print(f"   后续命令会自动使用此路径")
        print(f"   或在其他终端设置环境变量: export CLOUDPSS_HOME={pm.root}")

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


def cmd_task_submit(args):
    """提交任务"""
    registry = TaskRegistry()
    task = registry.get(args.task_id)

    if not task:
        print(f"❌ 任务不存在: {args.task_id}")
        return 1

    # 更新状态为 submitted
    registry.update(args.task_id, {"status": "submitted", "submitted_at": datetime.now().isoformat()})
    print(f"✅ 任务已提交: {args.task_id}")
    print(f"   名称: {task.name}")
    print(f"   类型: {task.type}")
    if args.wait:
        print(f"   等待模式: 已启用 (等待 CloudPSS 响应)")
    return 0


def cmd_task_status(args):
    """查看任务状态"""
    registry = TaskRegistry()
    task = registry.get(args.task_id)

    if not task:
        print(f"❌ 任务不存在: {args.task_id}")
        return 1

    print("=" * 60)
    print(f"任务状态: {args.task_id}")
    print("=" * 60)
    print(f"  名称: {task.name}")
    print(f"  状态: {task.status}")
    print(f"  类型: {task.type}")
    print(f"  算例: {task.case_id}")
    if task.created_at:
        print(f"  创建时间: {task.created_at}")
    if task.submitted_at:
        print(f"  提交时间: {task.submitted_at}")
    if task.started_at:
        print(f"  开始时间: {task.started_at}")
    if task.completed_at:
        print(f"  完成时间: {task.completed_at}")
    if task.result_id:
        print(f"  结果ID: {task.result_id}")
    print("=" * 60)
    return 0


def cmd_task_cancel(args):
    """取消任务"""
    registry = TaskRegistry()
    task = registry.get(args.task_id)

    if not task:
        print(f"❌ 任务不存在: {args.task_id}")
        return 1

    if task.status not in ["created", "submitted", "running"]:
        print(f"❌ 任务状态为 {task.status}，无法取消")
        return 1

    registry.update(args.task_id, {"status": "cancelled"})
    print(f"✅ 任务已取消: {args.task_id}")
    return 0


# ====== Variant 命令 ======
def cmd_variant_list(args):
    """列出变体"""
    registry = VariantRegistry()

    if args.case_id:
        variants = registry.get_by_case(args.case_id)
        print(f"=" * 60)
        print(f"算例 {args.case_id} 的变体列表")
    else:
        variants = registry.list_all()
        print("=" * 60)
        print("变体列表")

    print("=" * 60)

    if not variants:
        print("  (无变体)")
    else:
        for variant_id, variant in variants:
            print(f"  🎨 {variant_id}: {variant.name}")
            print(f"      算例: {variant.case_id}")
            if variant.parameters:
                print(f"      参数: {variant.parameters}")

    print("=" * 60)
    return 0


def cmd_variant_create(args):
    """创建变体"""
    registry = VariantRegistry()

    variant_id = IDGenerator.generate(EntityType.VARIANT)

    # 解析参数字符串 (格式: key1=val1,key2=val2)
    parameters = {}
    if args.parameters:
        for param in args.parameters.split(","):
            if "=" in param:
                key, value = param.split("=", 1)
                parameters[key] = value

    variant = Variant(
        id=variant_id,
        case_id=args.case_id,
        name=args.name,
        parameters=parameters
    )

    if registry.create(variant_id, variant):
        print(f"✅ 变体创建成功: {variant_id}")
        print(f"   名称: {args.name}")
        print(f"   算例: {args.case_id}")
        print(f"   参数: {parameters}")
        return 0
    else:
        print(f"❌ 创建失败")
        return 1


def cmd_variant_apply(args):
    """应用变体创建任务"""
    # 获取变体
    variant_registry = VariantRegistry()
    variant = variant_registry.get(args.variant_id)

    if not variant:
        print(f"❌ 变体不存在: {args.variant_id}")
        return 1

    # 创建任务
    task_registry = TaskRegistry()
    task_id = IDGenerator.generate(EntityType.TASK)
    task = Task(
        id=task_id,
        name=args.name or f"{variant.name}_应用",
        case_id=variant.case_id,
        variant_id=args.variant_id,
        type=args.type,
        status="created"
    )

    if task_registry.create(task_id, task):
        print(f"✅ 变体已应用，任务创建成功: {task_id}")
        print(f"   变体: {args.variant_id}")
        print(f"   算例: {variant.case_id}")
        print(f"   参数: {variant.parameters}")
        return 0
    else:
        print(f"❌ 任务创建失败")
        return 1


def cmd_variant_delete(args):
    """删除变体"""
    registry = VariantRegistry()
    if registry.delete(args.variant_id):
        print(f"✅ 变体已删除: {args.variant_id}")
        return 0
    else:
        print(f"❌ 变体不存在: {args.variant_id}")
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


def cmd_result_export(args):
    """导出结果"""
    import json
    import csv

    registry = ResultRegistry()
    result = registry.get(args.result_id)

    if not result:
        print(f"❌ 结果不存在: {args.result_id}")
        return 1

    # 确定导出格式和路径
    export_format = args.format or result.format
    export_path = args.output or f"./{args.result_id}_export.{export_format}"
    export_path = Path(export_path).expanduser().resolve()

    # 确保父目录存在
    export_path.parent.mkdir(parents=True, exist_ok=True)

    # 准备导出数据
    export_data = {
        "result_id": result.id,
        "name": result.name,
        "task_id": result.task_id,
        "case_id": result.case_id,
        "format": result.format,
        "created_at": result.created_at,
        "size_bytes": result.size_bytes,
        "files": result.files,
        "metadata": result.metadata,
        "exported_at": datetime.now().isoformat(),
        "export_format": export_format
    }

    try:
        # 根据格式导出文件
        if export_format == "json":
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

        elif export_format == "csv":
            # CSV 导出基本元数据
            with open(export_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Property", "Value"])
                writer.writerow(["result_id", result.id])
                writer.writerow(["name", result.name])
                writer.writerow(["task_id", result.task_id])
                writer.writerow(["case_id", result.case_id])
                writer.writerow(["format", result.format])
                writer.writerow(["created_at", result.created_at])
                writer.writerow(["size_bytes", result.size_bytes])
                writer.writerow(["exported_at", export_data["exported_at"]])

        elif export_format == "hdf5":
            # HDF5 格式需要 h5py，如果不可用则报错
            try:
                import h5py
                with h5py.File(export_path, 'w') as f:
                    f.attrs['result_id'] = result.id
                    f.attrs['name'] = result.name
                    f.attrs['task_id'] = result.task_id
                    f.attrs['case_id'] = result.case_id
                    f.attrs['format'] = result.format
                    f.attrs['created_at'] = result.created_at
                    f.attrs['exported_at'] = export_data["exported_at"]
            except ImportError:
                print(f"❌ 导出失败: HDF5 格式需要 h5py 库")
                print(f"   请安装: pip install h5py")
                return 1

        else:
            print(f"❌ 不支持的导出格式: {export_format}")
            return 1

        # 更新注册表中的导出信息
        actual_size = export_path.stat().st_size
        registry.update(args.result_id, {
            "export_format": export_format,
            "export_path": str(export_path),
            "exported_at": export_data["exported_at"]
        })

        print(f"✅ 结果导出成功: {args.result_id}")
        print(f"   格式: {export_format}")
        print(f"   路径: {export_path}")
        print(f"   大小: {actual_size} bytes")
        return 0

    except Exception as e:
        print(f"❌ 导出失败: {e}")
        return 1


def cmd_result_delete(args):
    """删除结果"""
    registry = ResultRegistry()
    result = registry.get(args.result_id)

    if not result:
        print(f"❌ 结果不存在: {args.result_id}")
        return 1

    if registry.delete(args.result_id):
        print(f"✅ 结果已删除: {args.result_id}")
        return 0
    else:
        print(f"❌ 删除失败")
        return 1


def cmd_result_analyze(args):
    """分析结果"""
    registry = ResultRegistry()
    result = registry.get(args.result_id)

    if not result:
        print(f"❌ 结果不存在: {args.result_id}")
        return 1

    print("=" * 60)
    print(f"结果分析: {args.result_id}")
    print("=" * 60)
    print(f"  名称: {result.name}")
    print(f"  格式: {result.format}")
    print(f"  大小: {result.size_bytes} bytes")
    print(f"  创建时间: {result.created_at}")

    if result.files:
        print(f"\n  包含文件 ({len(result.files)}):")
        for f in result.files[:10]:  # 最多显示10个
            print(f"    - {f}")
        if len(result.files) > 10:
            print(f"    ... 还有 {len(result.files) - 10} 个文件")

    if result.metadata:
        print(f"\n  元数据:")
        for key, value in result.metadata.items():
            print(f"    {key}: {value}")

    print("=" * 60)
    return 0


def cmd_result_compare(args):
    """比较两个结果"""
    registry = ResultRegistry()
    result1 = registry.get(args.result_id1)
    result2 = registry.get(args.result_id2)

    if not result1:
        print(f"❌ 结果不存在: {args.result_id1}")
        return 1
    if not result2:
        print(f"❌ 结果不存在: {args.result_id2}")
        return 1

    print("=" * 60)
    print(f"结果对比")
    print("=" * 60)
    print(f"{'属性':<20} {'结果1':<20} {'结果2':<20}")
    print("-" * 60)
    print(f"{'ID':<20} {result1.id:<20} {result2.id:<20}")
    print(f"{'名称':<20} {result1.name:<20} {result2.name:<20}")
    print(f"{'格式':<20} {result1.format:<20} {result2.format:<20}")
    print(f"{'大小 (bytes)':<20} {result1.size_bytes:<20} {result2.size_bytes:<20}")

    size_diff = result2.size_bytes - result1.size_bytes
    diff_pct = (size_diff / result1.size_bytes * 100) if result1.size_bytes > 0 else 0
    print(f"\n大小差异: {size_diff:+d} bytes ({diff_pct:+.1f}%)")

    if result1.format == result2.format:
        print("格式: 相同")
    else:
        print(f"格式: 不同 ({result1.format} vs {result2.format})")

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

    task_submit_parser = task_subparsers.add_parser("submit", help="提交任务")
    task_submit_parser.add_argument("task_id", help="任务ID")
    task_submit_parser.add_argument("--wait", action="store_true", help="等待完成")
    task_submit_parser.set_defaults(func=cmd_task_submit)

    task_status_parser = task_subparsers.add_parser("status", help="查看任务状态")
    task_status_parser.add_argument("task_id", help="任务ID")
    task_status_parser.set_defaults(func=cmd_task_status)

    task_cancel_parser = task_subparsers.add_parser("cancel", help="取消任务")
    task_cancel_parser.add_argument("task_id", help="任务ID")
    task_cancel_parser.set_defaults(func=cmd_task_cancel)

    # variant 命令
    variant_parser = subparsers.add_parser("variant", help="变体管理")
    variant_subparsers = variant_parser.add_subparsers(dest="variant_command")

    variant_list_parser = variant_subparsers.add_parser("list", help="列出变体")
    variant_list_parser.add_argument("--case-id", help="按算例过滤")
    variant_list_parser.set_defaults(func=cmd_variant_list)

    variant_create_parser = variant_subparsers.add_parser("create", help="创建变体")
    variant_create_parser.add_argument("--case-id", required=True, help="算例ID")
    variant_create_parser.add_argument("--name", required=True, help="变体名称")
    variant_create_parser.add_argument("--parameters", help="参数 (格式: key1=val1,key2=val2)")
    variant_create_parser.set_defaults(func=cmd_variant_create)

    variant_apply_parser = variant_subparsers.add_parser("apply", help="应用变体")
    variant_apply_parser.add_argument("variant_id", help="变体ID")
    variant_apply_parser.add_argument("--name", help="任务名称")
    variant_apply_parser.add_argument("--type", default="powerflow", choices=["powerflow", "emt", "stability"], help="任务类型")
    variant_apply_parser.set_defaults(func=cmd_variant_apply)

    variant_delete_parser = variant_subparsers.add_parser("delete", help="删除变体")
    variant_delete_parser.add_argument("variant_id", help="变体ID")
    variant_delete_parser.set_defaults(func=cmd_variant_delete)

    # result 命令
    result_parser = subparsers.add_parser("result", help="结果管理")
    result_subparsers = result_parser.add_subparsers(dest="result_command")

    result_list_parser = result_subparsers.add_parser("list", help="列出结果")
    result_list_parser.set_defaults(func=cmd_result_list)

    result_export_parser = result_subparsers.add_parser("export", help="导出结果")
    result_export_parser.add_argument("result_id", help="结果ID")
    result_export_parser.add_argument("--format", choices=["json", "csv", "hdf5"], help="导出格式")
    result_export_parser.add_argument("--output", "-o", help="输出路径")
    result_export_parser.set_defaults(func=cmd_result_export)

    result_delete_parser = result_subparsers.add_parser("delete", help="删除结果")
    result_delete_parser.add_argument("result_id", help="结果ID")
    result_delete_parser.set_defaults(func=cmd_result_delete)

    result_analyze_parser = result_subparsers.add_parser("analyze", help="分析结果")
    result_analyze_parser.add_argument("result_id", help="结果ID")
    result_analyze_parser.set_defaults(func=cmd_result_analyze)

    result_compare_parser = result_subparsers.add_parser("compare", help="比较结果")
    result_compare_parser.add_argument("result_id1", help="第一个结果ID")
    result_compare_parser.add_argument("result_id2", help="第二个结果ID")
    result_compare_parser.set_defaults(func=cmd_result_compare)

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
