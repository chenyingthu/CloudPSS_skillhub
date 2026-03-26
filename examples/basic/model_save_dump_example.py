# coding=UTF-8
"""
研究分支管理示例

运行方式: python examples/basic/model_save_dump_example.py
前置条件: 有效的 CloudPSS token 保存在 .cloudpss_token

本示例面向离线研究工作流中的“分支管理”阶段，演示：
- 从云端获取一个已有算例
- 用 Model.dump() 创建本地研究分支
- 用 Model.load() 恢复本地研究分支
- 在本地副本上记录研究说明
- 仅在确认有写权限时，另存为新的云端研究分支
"""

import os
from pathlib import Path
import sys

from cloudpss import Model, setToken


DEFAULT_READONLY_MODEL_RID = os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39")
DEFAULT_WORKING_COPY = "examples/basic/study-working-copy.yaml"
DEFAULT_SNAPSHOT = "examples/basic/study-working-snapshot.yaml"


def load_token():
    """从项目根目录读取 token。"""
    try:
        with open(".cloudpss_token", "r") as token_file:
            return token_file.read().strip()
    except FileNotFoundError:
        print("错误: 未找到 .cloudpss_token 文件")
        print("请先把 CloudPSS API token 写入项目根目录的 .cloudpss_token")
        sys.exit(1)


def load_model_from_source(source):
    """从云端 RID 或本地 YAML/JSON 继续研究分支管理。"""
    candidate = Path(source).expanduser()
    file_like = candidate.suffix.lower() in {".yaml", ".yml", ".json"}

    if candidate.exists():
        model = Model.load(str(candidate))
        print(f"本地模型文件: {candidate}")
        print(f"模型名称: {model.name}")
        print(f"模型 RID: {model.rid}")
        print(f"参数方案数量: {len(model.configs)}")
        print(f"计算方案数量: {len(model.jobs)}")
        return model

    if file_like:
        raise FileNotFoundError(f"未找到本地模型文件: {candidate}")

    model = Model.fetch(source)
    print(f"云端模型 RID: {source}")
    print(f"模型名称: {model.name}")
    print(f"模型 RID: {model.rid}")
    print(f"参数方案数量: {len(model.configs)}")
    print(f"计算方案数量: {len(model.jobs)}")
    return model


def suggest_working_copy_path(source):
    """为本地输入源生成更安全的默认工作副本路径，避免覆盖原文件。"""
    candidate = Path(source).expanduser()
    if candidate.exists() and candidate.suffix.lower() in {".yaml", ".yml", ".json"}:
        return str(candidate.with_name(f"{candidate.stem}-branch{candidate.suffix}"))
    return DEFAULT_WORKING_COPY


def fetch_source_model(model_source):
    """获取研究起点模型。"""
    print("=" * 60)
    print("步骤 1: 获取研究起点")
    print("=" * 60)

    return load_model_from_source(model_source)


def create_local_branch(model, export_path=DEFAULT_WORKING_COPY):
    """创建本地工作副本，作为研究分支。"""
    print("\n" + "=" * 60)
    print("步骤 2: 创建本地研究分支")
    print("=" * 60)

    Model.dump(model, export_path, compress=None)
    working_model = Model.load(export_path)

    print(f"本地工作副本: {export_path}")
    print("这样做的目的不是备份，而是避免直接污染原始算例。")

    return working_model, export_path


def review_local_branch(file_path):
    """重新加载本地副本，确认分支可恢复。"""
    print("\n" + "=" * 60)
    print("步骤 3: 恢复并检查本地分支")
    print("=" * 60)

    working_model = Model.load(file_path)
    print(f"恢复成功: {working_model.name}")
    print(f"元件数量: {len(working_model.getAllComponents())}")
    print(f"计算方案数量: {len(working_model.jobs)}")
    print(f"参数方案数量: {len(working_model.configs)}")

    return working_model


def annotate_local_branch(model):
    """在本地副本上写入研究说明，模拟一次非破坏性的研究分支更新。"""
    print("\n" + "=" * 60)
    print("步骤 4: 记录研究分支说明")
    print("=" * 60)

    branch_note = input("请输入本轮研究说明，直接回车使用默认说明: ").strip()
    branch_note = branch_note or "offline study branch for topology and parameter iteration"

    existing_description = getattr(model, "description", "") or ""
    if existing_description:
        model.description = f"{existing_description}\n[study-note] {branch_note}"
    else:
        model.description = f"[study-note] {branch_note}"

    print("已将研究说明写入本地副本 description。")
    print("建议后续在该副本上继续改模、做潮流校核和 EMT 仿真。")

    return model


def save_local_snapshot(model, snapshot_path=DEFAULT_SNAPSHOT):
    """保存本地研究中间快照。"""
    print("\n" + "=" * 60)
    print("步骤 5: 保存本地中间快照")
    print("=" * 60)

    Model.dump(model, snapshot_path, compress=None)
    print(f"已保存本地快照: {snapshot_path}")
    print("推荐在每个关键研究节点都保留一个本地快照。")


def optionally_save_cloud_branch(model):
    """在明确有写权限时，另存为新的云端研究分支。"""
    print("\n" + "=" * 60)
    print("步骤 6: 可选地另存为新的云端研究分支")
    print("=" * 60)

    print("只有当你确认自己对目标命名空间有写权限时，才应该执行这一步。")
    confirm = input("是否另存为新的云端研究分支? (y/n): ").strip().lower()
    if confirm != "y":
        print("跳过云端另存，继续使用本地研究分支。")
        return

    new_key = input("请输入新的模型 key: ").strip()
    if not new_key:
        print("未提供新 key，跳过云端另存。")
        return

    try:
        response = model.save(new_key)
        print(f"已另存为新的云端研究分支: {model.rid}")
        print("注意: SDK 不会返回一个新的 Model 对象，而是把当前 working_model 的 rid 改到新算例上。")
        print(f"保存响应键: {list(response.keys())}")
    except Exception as exc:
        print(f"另存失败: {exc}")
        print("常见原因:")
        print("  1. 当前用户没有写权限")
        print("  2. key 含非法字符")
        print("  3. 同名模型已存在")


def main():
    """主函数。"""
    print("CloudPSS SDK - 研究分支管理示例")
    print("=" * 60)

    token = load_token()
    setToken(token)
    print("Token 已设置")

    print(f"- 可输入云端模型 RID，例如: {DEFAULT_READONLY_MODEL_RID}")
    print("- 也可输入本地 YAML，继续已有研究分支管理")

    source_arg = sys.argv[1].strip() if len(sys.argv) > 1 else ""
    if source_arg:
        print(f"使用命令行输入源: {source_arg}")
        model_source = source_arg
    else:
        prompt = (
            "请输入模型 RID 或本地 YAML 路径，直接回车使用已验证的只读模型 "
            f"[{DEFAULT_READONLY_MODEL_RID}]: "
        )
        model_source = input(prompt).strip() or DEFAULT_READONLY_MODEL_RID

    try:
        source_model = fetch_source_model(model_source)
    except Exception as exc:
        print(f"获取模型失败: {exc}")
        return

    try:
        default_working_copy = suggest_working_copy_path(model_source)
        working_copy_path = (
            input(
                "请输入本地工作副本路径，直接回车使用 "
                f"[{default_working_copy}]: "
            ).strip()
            or default_working_copy
        )

        working_model, working_copy_path = create_local_branch(source_model, working_copy_path)
        working_model = review_local_branch(working_copy_path)
        working_model = annotate_local_branch(working_model)
        save_local_snapshot(working_model)
        optionally_save_cloud_branch(working_model)
    except Exception as exc:
        print(f"研究分支管理流程失败: {exc}")
        return

    print("\n提示:")
    print("- 先保留本地分支，再做结构修改和仿真，更符合研究工作流")
    print("- 如需继续操作元件，请转到 component_example.py")
    print("- 如需验证模型可算性，请转到 run_powerflow.py")


if __name__ == "__main__":
    main()
