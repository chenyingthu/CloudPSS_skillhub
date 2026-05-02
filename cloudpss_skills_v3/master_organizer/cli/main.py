#!/usr/bin/env python3
"""
收纳大师 CLI - 主入口
完整实现计划中的所有命令
"""
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Iterable

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from cloudpss_skills_v3.master_organizer.core import (
    IDGenerator, EntityType,
    get_path_manager, get_config_manager,
    ServerRegistry, CaseRegistry, TaskRegistry, ResultRegistry, VariantRegistry,
    Server, Case, Task, Result, Variant
)
from cloudpss_skills_v3.master_organizer.core.server_auth import (
    TOKEN_SOURCE_ENV,
    TOKEN_SOURCE_INLINE,
    build_auth_metadata,
    ensure_internal_server,
    get_default_server,
    normalize_server_url,
    read_token_source,
    set_default_server,
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
        # 保存到自定义工作区的配置
        cm = get_config_manager(pm.config_dir)
        cm.update("user", {"workspace": {"root": str(pm.root)}}, merge=True)

        # 同时保存到默认位置的配置，以便从任意目录都能识别
        from cloudpss_skills_v3.master_organizer.core import PathManager
        default_config_dir = Path.home() / PathManager.ROOT_DIR_NAME / "config"
        default_config_dir.mkdir(parents=True, exist_ok=True)
        default_cm = get_config_manager(default_config_dir)
        default_cm.update("user", {"workspace": {"root": str(pm.root)}}, merge=True)

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


def _default_config_manager():
    from cloudpss_skills_v3.master_organizer.core import PathManager

    config_dir = Path.home() / PathManager.ROOT_DIR_NAME / "config"
    return get_config_manager(config_dir)


def _load_default_user_config() -> dict:
    return _default_config_manager().load("user") or {}


def _save_default_user_config(config: dict):
    _default_config_manager().save("user", config)


def _workspace_is_valid(path: Path) -> bool:
    return (path / "config").is_dir() and (path / "registry").is_dir()


def _parse_tags(values: Iterable[str] | None) -> list[str]:
    tags: list[str] = []
    for value in values or []:
        for tag in value.split(","):
            tag = tag.strip()
            if tag and tag not in tags:
                tags.append(tag)
    return tags


def _clean_directory(directory: Path) -> tuple[int, int]:
    import shutil

    removed = 0
    freed = 0
    if not directory.exists():
        return removed, freed

    for item in list(directory.iterdir()):
        try:
            if item.is_dir():
                size = sum(f.stat().st_size for f in item.rglob("*") if f.is_file())
                shutil.rmtree(item)
            else:
                size = item.stat().st_size
                item.unlink()
            removed += 1
            freed += size
        except OSError:
            continue
    return removed, freed


def _update_case_task_summary(case_id: str):
    cases = CaseRegistry()
    case = cases.get(case_id)
    if not case:
        return

    tasks = TaskRegistry().filter_by(case_id=case_id)
    last_task_id = None
    if tasks:
        last_task_id = sorted(tasks, key=lambda x: x[1].created_at, reverse=True)[0][0]

    cases.update(case_id, {
        "task_count": len(tasks),
        "last_task_id": last_task_id,
    })


def cmd_system_clean(args):
    """清理系统临时文件"""
    pm = get_path_manager()
    targets = []
    if args.cache or args.all:
        targets.append(("缓存", pm.cache_dir))
    if args.logs or args.all:
        targets.append(("日志", pm.logs_dir))
    if args.trash or args.all:
        targets.append(("回收站", pm.trash_dir))
    if not targets:
        targets = [("缓存", pm.cache_dir)]

    total_removed = 0
    total_freed = 0
    for label, path in targets:
        removed, freed = _clean_directory(path)
        total_removed += removed
        total_freed += freed
        print(f"🧹 已清理{label}: {removed} 个项目")

    print(f"✅ 共清理 {total_removed} 个项目，释放 {total_freed / (1024 * 1024):.2f} MB")
    return 0


def cmd_system_backup(args):
    """备份工作区数据"""
    import tarfile

    pm = get_path_manager()
    if args.output:
        backup_path = Path(args.output).expanduser().resolve()
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = Path.cwd() / f"cloudpss_backup_{timestamp}.tar.gz"

    backup_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tarfile.open(backup_path, "w:gz") as tar:
            for child in ["config", "registry", "cases", "tasks", "results"]:
                path = pm.root / child
                if path.exists():
                    tar.add(path, arcname=child)
        print(f"✅ 备份完成: {backup_path}")
        print(f"   大小: {backup_path.stat().st_size / (1024 * 1024):.2f} MB")
        return 0
    except Exception as e:
        print(f"❌ 备份失败: {e}")
        return 1


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
            if server.owner:
                print(f"      Owner: {server.owner}")
            token_source = server.auth.get("token_source") if server.auth else None
            if token_source:
                print(f"      Token: {token_source} (encrypted)")

    print("=" * 60)
    return 0


def cmd_server_add(args):
    """添加服务器"""
    registry = ServerRegistry()

    try:
        url = normalize_server_url(args.url)
    except ValueError as e:
        print(f"❌ {e}")
        return 1

    auth = {}
    if args.token:
        try:
            auth = build_auth_metadata(args.token, {"token_source": TOKEN_SOURCE_INLINE})
        except ValueError as e:
            print(f"❌ {e}")
            return 1
    elif args.token_file:
        try:
            token, metadata = read_token_source(args.token_file)
            auth = build_auth_metadata(token, metadata)
        except (OSError, ValueError) as e:
            print(f"❌ 读取 token 失败: {e}")
            return 1
    elif args.token_env:
        try:
            token, metadata = read_token_source(TOKEN_SOURCE_ENV)
            auth = build_auth_metadata(token, metadata)
        except ValueError as e:
            print(f"❌ 读取 token 失败: {e}")
            return 1

    server_id = IDGenerator.generate(EntityType.SERVER)
    server = Server(
        id=server_id,
        name=args.name,
        url=url,
        owner=args.owner or "",
        auth=auth,
        status="active"
    )

    if registry.create(server_id, server):
        if args.default:
            set_default_server(server_id, registry)
        print(f"✅ 服务器添加成功: {server_id}")
        print(f"   名称: {args.name}")
        print(f"   URL: {url}")
        if args.owner:
            print(f"   Owner: {args.owner}")
        if auth:
            print(f"   Token: 已加密保存 ({auth.get('token_source', 'unknown')})")
        if args.default:
            print("   已设为默认服务器")
        return 0
    else:
        print(f"❌ 添加失败")
        return 1


def cmd_server_default(args):
    """设置默认服务器"""
    if set_default_server(args.server_id):
        print(f"✅ 默认服务器已设置: {args.server_id}")
        return 0
    print(f"❌ 服务器不存在: {args.server_id}")
    return 1


def cmd_server_internal(args):
    """注册内网服务器"""
    try:
        server_id, server = ensure_internal_server()
    except (OSError, ValueError) as e:
        print(f"❌ 注册 internal 服务器失败: {e}")
        return 1

    print(f"✅ internal 服务器已注册: {server_id}")
    print(f"   名称: {server.name}")
    print(f"   URL: {server.url}")
    print(f"   Owner: {server.owner}")
    print("   Token: .cloudpss_token_internal (encrypted)")
    print("   已设为默认服务器")
    return 0


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

    if args.status != "all":
        cases = [(case_id, case) for case_id, case in cases if case.status == args.status]

    if args.tag:
        required_tags = set(_parse_tags(args.tag))
        cases = [
            (case_id, case)
            for case_id, case in cases
            if required_tags.issubset(set(case.tags))
        ]

    print("=" * 60)
    print("算例列表" + (" (树形)" if args.tree else ""))
    print("=" * 60)

    if not cases:
        print("  (无算例)")
    else:
        task_registry = TaskRegistry()
        variant_registry = VariantRegistry()
        for case_id, case in cases:
            status_icon = "🟢" if case.status == "active" else "⚪"
            if args.tree:
                print(f"  {status_icon} {case.name} [{case.status}]")
                print(f"      ID: {case_id}")
            else:
                print(f"  {status_icon} {case_id}: {case.name} [{case.status}]")
            if case.description:
                print(f"      描述: {case.description}")
            if case.tags:
                print(f"      标签: {', '.join(case.tags)}")
            if args.tree:
                tasks = task_registry.filter_by(case_id=case_id)
                variants = variant_registry.get_by_case(case_id)
                if variants:
                    print("      变体:")
                    for variant_id, variant in variants:
                        print(f"        - {variant_id}: {variant.name}")
                if tasks:
                    print("      任务:")
                    for task_id, task in tasks:
                        print(f"        - {task_id}: {task.name} [{task.status}]")

    print("=" * 60)
    return 0


def cmd_case_create(args):
    """创建算例"""
    registry = CaseRegistry()
    server_id = args.server_id or ""
    if not server_id:
        default_server = get_default_server()
        if default_server:
            server_id = default_server[0]

    case_id = IDGenerator.generate(EntityType.CASE)
    case = Case(
        id=case_id,
        name=args.name,
        description=args.description or "",
        rid=args.rid,
        server_id=server_id,
        status="draft",
        tags=_parse_tags(args.tag)
    )

    if registry.create(case_id, case):
        print(f"✅ 算例创建成功: {case_id}")
        print(f"   名称: {args.name}")
        print(f"   RID: {args.rid}")
        if server_id:
            print(f"   服务器: {server_id}")
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


def cmd_case_clone(args):
    """克隆算例"""
    registry = CaseRegistry()
    source_case = registry.get(args.case_id)

    if not source_case:
        print(f"❌ 源算例不存在: {args.case_id}")
        return 1

    new_case_id = IDGenerator.generate(EntityType.CASE)
    new_case = Case(
        id=new_case_id,
        name=args.name or f"{source_case.name}_副本",
        description=source_case.description,
        rid=source_case.rid,
        server_id=source_case.server_id,
        status="draft",
        tags=source_case.tags.copy() if hasattr(source_case, 'tags') else []
    )

    if registry.create(new_case_id, new_case):
        print(f"✅ 算例克隆成功")
        print(f"   原算例: {args.case_id}")
        print(f"   新算例: {new_case_id}")
        print(f"   名称: {new_case.name}")
        return 0
    else:
        print(f"❌ 克隆失败")
        return 1


def cmd_case_archive(args):
    """归档算例"""
    registry = CaseRegistry()
    case = registry.get(args.case_id)

    if not case:
        print(f"❌ 算例不存在: {args.case_id}")
        return 1

    if case.status == "archived":
        print(f"⚠️ 算例已是归档状态: {args.case_id}")
        return 0

    if registry.update(args.case_id, {"status": "archived"}):
        print(f"✅ 算例已归档: {args.case_id}")
        print(f"   名称: {case.name}")
        return 0
    else:
        print(f"❌ 归档失败")
        return 1


def cmd_case_restore(args):
    """恢复归档算例"""
    registry = CaseRegistry()
    case = registry.get(args.case_id)

    if not case:
        print(f"❌ 算例不存在: {args.case_id}")
        return 1

    if case.status != "archived":
        print(f"⚠️ 算例不是归档状态: {args.case_id}")
        return 0

    if registry.update(args.case_id, {"status": "active"}):
        print(f"✅ 算例已恢复: {args.case_id}")
        print(f"   名称: {case.name}")
        return 0
    else:
        print(f"❌ 恢复失败")
        return 1


def cmd_case_show(args):
    """查看算例详情"""
    registry = CaseRegistry()
    case = registry.get(args.case_id)

    if not case:
        print(f"❌ 算例不存在: {args.case_id}")
        return 1

    print("=" * 60)
    print(f"算例详情: {args.case_id}")
    print("=" * 60)
    print(f"  名称: {case.name}")
    print(f"  状态: {case.status}")
    print(f"  RID: {case.rid}")
    if case.description:
        print(f"  描述: {case.description}")
    if case.server_id:
        print(f"  服务器: {case.server_id}")
    if case.tags:
        print(f"  标签: {', '.join(case.tags)}")
    print(f"  创建时间: {case.created_at}")
    if hasattr(case, 'updated_at') and case.updated_at:
        print(f"  更新时间: {case.updated_at}")
    if hasattr(case, 'task_count') and case.task_count:
        print(f"  任务数: {case.task_count}")
    print("=" * 60)
    return 0


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
    case_registry = CaseRegistry()

    if not case_registry.exists(args.case_id):
        print(f"❌ 算例不存在: {args.case_id}")
        return 1
    case = case_registry.get(args.case_id)
    server_id = case.server_id if case else ""

    task_id = IDGenerator.generate(EntityType.TASK)
    task = Task(
        id=task_id,
        name=args.name,
        case_id=args.case_id,
        type=args.type,
        server_id=server_id,
        status="created"
    )

    if registry.create(task_id, task):
        _update_case_task_summary(args.case_id)
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
    task = registry.get(args.task_id)
    if registry.delete(args.task_id):
        if task:
            _update_case_task_summary(task.case_id)
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
        _update_case_task_summary(variant.case_id)
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
    referenced = TaskRegistry().filter_by(variant_id=args.variant_id)
    if referenced and not args.force:
        print(f"❌ 变体已被 {len(referenced)} 个任务引用，使用 --force 强制删除")
        return 1
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
    import shutil

    registry = ResultRegistry()
    result = registry.get(args.result_id)

    if not result:
        print(f"❌ 结果不存在: {args.result_id}")
        return 1

    # 确定导出格式和路径
    export_format = args.format or ("json" if result.format in {"powerflow", "emt"} else result.format)
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
    pm = get_path_manager()
    result_dir = pm.get_result_path(args.result_id)
    manifest_path = result_dir / "manifest.json"
    if manifest_path.exists():
        export_data["manifest"] = json.loads(manifest_path.read_text(encoding="utf-8"))

    try:
        # 根据格式导出文件
        if export_format == "json":
            artifacts = {}
            for relative_path in result.files:
                artifact_path = result_dir / relative_path
                if artifact_path.is_file() and artifact_path.suffix == ".json":
                    artifacts[relative_path] = json.loads(artifact_path.read_text(encoding="utf-8"))
            if artifacts:
                export_data["artifacts"] = artifacts
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

        elif export_format == "csv":
            if args.artifact:
                artifact_path = result_dir / args.artifact
            else:
                table_name = args.table or "buses"
                artifact_path = result_dir / "tables" / f"{table_name}.csv"
            if artifact_path.exists():
                shutil.copyfile(artifact_path, export_path)
            else:
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
    import shutil

    registry = ResultRegistry()
    result = registry.get(args.result_id)

    if not result:
        print(f"❌ 结果不存在: {args.result_id}")
        return 1

    if registry.delete(args.result_id):
        result_dir = get_path_manager().get_result_path(args.result_id)
        if result_dir.exists():
            shutil.rmtree(result_dir)
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

    result_dir = get_path_manager().get_result_path(args.result_id)
    if result_dir.exists():
        print(f"\n  存储目录: {result_dir}")
        manifest_path = result_dir / "manifest.json"
        if manifest_path.exists():
            print(f"  Manifest: {manifest_path}")

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


def cmd_query_search(args):
    """搜索功能"""
    keyword = args.keyword.lower()
    results = []

    # 搜索算例
    if args.type in ["all", "case"]:
        case_registry = CaseRegistry()
        for case_id, case in case_registry.list_all():
            if (keyword in case.name.lower() or
                keyword in case_id.lower() or
                (case.description and keyword in case.description.lower())):
                results.append(("case", case_id, case.name))

    # 搜索任务
    if args.type in ["all", "task"]:
        task_registry = TaskRegistry()
        for task_id, task in task_registry.list_all():
            if keyword in task.name.lower() or keyword in task_id.lower():
                results.append(("task", task_id, task.name))

    # 搜索服务器
    if args.type in ["all", "server"]:
        server_registry = ServerRegistry()
        for server_id, server in server_registry.list_all():
            if keyword in server.name.lower() or keyword in server_id.lower():
                results.append(("server", server_id, server.name))

    print("=" * 60)
    print(f"搜索结果: '{args.keyword}'")
    print("=" * 60)

    if not results:
        print("  (无匹配结果)")
    else:
        type_icons = {"case": "📦", "task": "📋", "server": "🖥️"}
        for entity_type, entity_id, name in results[:args.limit]:
            icon = type_icons.get(entity_type, "📄")
            print(f"  {icon} [{entity_type}] {name}")
            print(f"      ID: {entity_id}")

    print("=" * 60)
    print(f"共找到 {len(results)} 个结果")
    return 0


def cmd_query_recent(args):
    """最近活动"""
    print("=" * 60)
    print("最近活动")
    print("=" * 60)

    # 最近算例
    cases = CaseRegistry()
    recent_cases = sorted(cases.list_all(), key=lambda x: x[1].created_at, reverse=True)[:args.limit]
    if recent_cases:
        print("\n📦 最近算例:")
        for case_id, case in recent_cases:
            print(f"  • {case.name} [{case_id}]")

    # 最近任务
    tasks = TaskRegistry()
    recent_tasks = sorted(tasks.list_all(), key=lambda x: x[1].created_at, reverse=True)[:args.limit]
    if recent_tasks:
        print("\n📋 最近任务:")
        for task_id, task in recent_tasks:
            status_icon = {"completed": "✅", "running": "🔄", "failed": "❌"}.get(task.status, "⏳")
            print(f"  {status_icon} {task.name} [{task.status}]")

    print("\n" + "=" * 60)
    return 0


def cmd_workspace_list(args):
    """列出保存过的工作区"""
    config = _load_default_user_config()
    workspaces = config.get("workspaces", {})
    current_root = str(get_path_manager().root)

    print("=" * 60)
    print("已保存工作区")
    print("=" * 60)
    if not workspaces:
        print("  (无已保存工作区)")
    else:
        for name, info in sorted(workspaces.items()):
            root = info.get("root", "")
            mark = " (当前)" if root == current_root else ""
            status = "有效" if root and _workspace_is_valid(Path(root)) else "失效"
            print(f"  {name}: {root}{mark}")
            print(f"      状态: {status}")
    print("=" * 60)
    return 0


def cmd_workspace_save(args):
    """保存当前工作区别名"""
    pm = get_path_manager()
    config = _load_default_user_config()
    workspaces = config.setdefault("workspaces", {})
    workspaces[args.name] = {
        "root": str(pm.root),
        "saved_at": datetime.now().isoformat(),
    }
    config["workspace"] = {"root": str(pm.root)}
    _save_default_user_config(config)
    print(f"✅ 工作区已保存: {args.name}")
    print(f"   路径: {pm.root}")
    return 0


def cmd_workspace_load(args):
    """加载已保存工作区"""
    config = _load_default_user_config()
    workspaces = config.get("workspaces", {})
    workspace = workspaces.get(args.name)
    if not workspace:
        print(f"❌ 工作区不存在: {args.name}")
        return 1

    root = Path(workspace.get("root", "")).expanduser().resolve()
    if not _workspace_is_valid(root):
        print(f"❌ 工作区路径无效: {root}")
        return 1

    config["workspace"] = {"root": str(root)}
    _save_default_user_config(config)

    # Reset singleton so the current process sees the newly loaded workspace.
    import cloudpss_skills_v3.master_organizer.core.path_manager as pm_module
    pm_module._path_manager = None

    print(f"✅ 工作区已加载: {args.name}")
    print(f"   路径: {root}")
    return 0


def cmd_workspace_clean(args):
    """清理工作区缓存"""
    config = _load_default_user_config()
    root = get_path_manager().root
    if args.name:
        workspace = config.get("workspaces", {}).get(args.name)
        if not workspace:
            print(f"❌ 工作区不存在: {args.name}")
            return 1
        root = Path(workspace.get("root", "")).expanduser().resolve()
        if not _workspace_is_valid(root):
            print(f"❌ 工作区路径无效: {root}")
            return 1

    removed, freed = _clean_directory(root / "cache")
    print(f"✅ 已清理工作区缓存: {removed} 个项目，释放 {freed / (1024 * 1024):.2f} MB")
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

    # system 命令
    system_parser = subparsers.add_parser("system", help="系统管理")
    system_subparsers = system_parser.add_subparsers(dest="system_command", required=True, help="子命令")

    system_clean_parser = system_subparsers.add_parser("clean", help="清理临时文件")
    system_clean_parser.add_argument("--cache", action="store_true", help="清理缓存")
    system_clean_parser.add_argument("--logs", action="store_true", help="清理日志")
    system_clean_parser.add_argument("--trash", action="store_true", help="清理回收站")
    system_clean_parser.add_argument("--all", action="store_true", help="清理所有")
    system_clean_parser.add_argument("--older-than", type=int, metavar="DAYS", help="清理早于指定天数的文件")
    system_clean_parser.set_defaults(func=cmd_system_clean)

    system_backup_parser = system_subparsers.add_parser("backup", help="备份工作区")
    system_backup_parser.add_argument("--output", "-o", help="备份文件路径")
    system_backup_parser.set_defaults(func=cmd_system_backup)

    # server 命令
    server_parser = subparsers.add_parser("server", help="服务器管理")
    server_subparsers = server_parser.add_subparsers(dest="server_command", required=True, help="子命令")

    server_list_parser = server_subparsers.add_parser("list", help="列出服务器")
    server_list_parser.set_defaults(func=cmd_server_list)

    server_add_parser = server_subparsers.add_parser("add", help="添加服务器")
    server_add_parser.add_argument("--name", required=True, help="服务器名称")
    server_add_parser.add_argument("--url", required=True, help="服务器URL")
    server_add_parser.add_argument("--owner", help="服务器 token 所属用户")
    server_add_parser.add_argument("--token-file", help="从文件读取 token 并加密保存")
    server_add_parser.add_argument("--token-env", action="store_true", help="从 CLOUDPSS_TOKEN 读取 token 并加密保存")
    server_add_parser.add_argument("--token", help="直接传入 token 并加密保存")
    server_add_parser.add_argument("--default", action="store_true", help="设为默认")
    server_add_parser.set_defaults(func=cmd_server_add)

    server_default_parser = server_subparsers.add_parser("default", help="设置默认服务器")
    server_default_parser.add_argument("server_id", help="服务器ID")
    server_default_parser.set_defaults(func=cmd_server_default)

    server_internal_parser = server_subparsers.add_parser("internal", help="注册当前内网 CloudPSS 服务器")
    server_internal_parser.set_defaults(func=cmd_server_internal)

    server_remove_parser = server_subparsers.add_parser("remove", help="删除服务器")
    server_remove_parser.add_argument("server_id", help="服务器ID")
    server_remove_parser.set_defaults(func=cmd_server_remove)

    # case 命令
    case_parser = subparsers.add_parser("case", help="算例管理")
    case_subparsers = case_parser.add_subparsers(dest="case_command", required=True, help="子命令")

    case_list_parser = case_subparsers.add_parser("list", help="列出算例")
    case_list_parser.add_argument("--tree", action="store_true", help="树形显示算例、变体和任务")
    case_list_parser.add_argument("--tag", action="append", help="按标签过滤，可重复或逗号分隔")
    case_list_parser.add_argument("--status", choices=["all", "draft", "active", "archived", "deleted"], default="all", help="按状态过滤")
    case_list_parser.set_defaults(func=cmd_case_list)

    case_create_parser = case_subparsers.add_parser("create", help="创建算例")
    case_create_parser.add_argument("--name", required=True, help="算例名称")
    case_create_parser.add_argument("--rid", required=True, help="CloudPSS RID")
    case_create_parser.add_argument("--description", help="算例描述")
    case_create_parser.add_argument("--server-id", help="服务器ID")
    case_create_parser.add_argument("--tag", action="append", help="算例标签，可重复或逗号分隔")
    case_create_parser.set_defaults(func=cmd_case_create)

    case_delete_parser = case_subparsers.add_parser("delete", help="删除算例")
    case_delete_parser.add_argument("case_id", help="算例ID")
    case_delete_parser.set_defaults(func=cmd_case_delete)

    case_clone_parser = case_subparsers.add_parser("clone", help="克隆算例")
    case_clone_parser.add_argument("case_id", help="源算例ID")
    case_clone_parser.add_argument("--name", help="新算例名称")
    case_clone_parser.set_defaults(func=cmd_case_clone)

    case_archive_parser = case_subparsers.add_parser("archive", help="归档算例")
    case_archive_parser.add_argument("case_id", help="算例ID")
    case_archive_parser.set_defaults(func=cmd_case_archive)

    case_restore_parser = case_subparsers.add_parser("restore", help="恢复归档算例")
    case_restore_parser.add_argument("case_id", help="算例ID")
    case_restore_parser.set_defaults(func=cmd_case_restore)

    case_show_parser = case_subparsers.add_parser("show", help="查看算例详情")
    case_show_parser.add_argument("case_id", help="算例ID")
    case_show_parser.set_defaults(func=cmd_case_show)

    # task 命令
    task_parser = subparsers.add_parser("task", help="任务管理")
    task_subparsers = task_parser.add_subparsers(dest="task_command", required=True, help="子命令")

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
    variant_subparsers = variant_parser.add_subparsers(dest="variant_command", required=True, help="子命令")

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
    variant_delete_parser.add_argument("--force", action="store_true", help="即使已有任务引用也删除")
    variant_delete_parser.set_defaults(func=cmd_variant_delete)

    # result 命令
    result_parser = subparsers.add_parser("result", help="结果管理")
    result_subparsers = result_parser.add_subparsers(dest="result_command", required=True, help="子命令")

    result_list_parser = result_subparsers.add_parser("list", help="列出结果")
    result_list_parser.set_defaults(func=cmd_result_list)

    result_export_parser = result_subparsers.add_parser("export", help="导出结果")
    result_export_parser.add_argument("result_id", help="结果ID")
    result_export_parser.add_argument("--format", choices=["json", "csv", "hdf5"], help="导出格式")
    result_export_parser.add_argument("--output", "-o", help="输出路径")
    result_export_parser.add_argument("--table", choices=["buses", "branches"], help="CSV 导出的结果表")
    result_export_parser.add_argument("--artifact", help="导出指定结果文件，如 csv/plot_2_vac_0.csv")
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
    query_subparsers = query_parser.add_subparsers(dest="query_command", required=True, help="子命令")

    query_tree_parser = query_subparsers.add_parser("tree", help="树形视图")
    query_tree_parser.set_defaults(func=cmd_query_tree)

    query_dashboard_parser = query_subparsers.add_parser("dashboard", help="仪表板")
    query_dashboard_parser.set_defaults(func=cmd_query_dashboard)

    query_search_parser = query_subparsers.add_parser("search", help="搜索")
    query_search_parser.add_argument("keyword", help="搜索关键词")
    query_search_parser.add_argument("--type", choices=["all", "case", "task", "server"], default="all", help="搜索类型")
    query_search_parser.add_argument("--limit", type=int, default=20, help="结果数量限制")
    query_search_parser.set_defaults(func=cmd_query_search)

    query_recent_parser = query_subparsers.add_parser("recent", help="最近活动")
    query_recent_parser.add_argument("--limit", type=int, default=10, help="显示数量")
    query_recent_parser.set_defaults(func=cmd_query_recent)

    # workspace 命令
    workspace_parser = subparsers.add_parser("workspace", help="工作区管理")
    workspace_subparsers = workspace_parser.add_subparsers(dest="workspace_command", required=True, help="子命令")

    workspace_list_parser = workspace_subparsers.add_parser("list", help="列出已保存的工作区")
    workspace_list_parser.set_defaults(func=cmd_workspace_list)

    workspace_save_parser = workspace_subparsers.add_parser("save", help="保存当前工作区")
    workspace_save_parser.add_argument("--name", required=True, help="工作区名称")
    workspace_save_parser.set_defaults(func=cmd_workspace_save)

    workspace_load_parser = workspace_subparsers.add_parser("load", help="加载工作区")
    workspace_load_parser.add_argument("--name", required=True, help="工作区名称")
    workspace_load_parser.set_defaults(func=cmd_workspace_load)

    workspace_clean_parser = workspace_subparsers.add_parser("clean", help="清理工作区缓存")
    workspace_clean_parser.add_argument("--name", help="工作区名称（默认当前）")
    workspace_clean_parser.set_defaults(func=cmd_workspace_clean)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 1

    if hasattr(args, "func"):
        return args.func(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
