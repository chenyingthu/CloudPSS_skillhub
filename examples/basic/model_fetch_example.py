# coding=UTF-8
"""
Model 获取与研究起点示例

运行方式: python examples/basic/model_fetch_example.py
前置条件: 有效的 CloudPSS token 保存在 .cloudpss_token

本示例面向离线研究工作流的起点，演示：
- 使用 Model.fetch() 获取一个已有算例
- 使用 Model.fetchMany() 搜索可访问算例
- 使用 Model.dump() / Model.load() 创建本地工作副本
"""

import os
from pathlib import Path
import sys

from cloudpss import Model, setToken


DEFAULT_READONLY_MODEL_RID = os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39")
DEFAULT_WORKING_COPY = "examples/basic/model_fetch_working_copy.yaml"


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
    """从云端 RID 或本地 YAML/JSON 加载研究起点。"""
    candidate = Path(source).expanduser()
    file_like = candidate.suffix.lower() in {".yaml", ".yml", ".json"}

    if candidate.exists():
        model = Model.load(str(candidate))
        print(f"本地模型文件: {candidate}")
        print(f"模型名称: {model.name}")
        print(f"模型 RID: {model.rid}")
        print(f"参数方案数量: {len(model.configs)}")
        print(f"计算方案数量: {len(model.jobs)}")
        print(f"元件数量: {len(model.getAllComponents())}")
        return model

    if file_like:
        raise FileNotFoundError(f"未找到本地模型文件: {candidate}")

    return fetch_model(source)


def suggest_working_copy_path(source):
    """对本地输入源生成安全的默认工作副本路径。"""
    candidate = Path(source).expanduser()
    if candidate.exists() and candidate.suffix.lower() in {".yaml", ".yml", ".json"}:
        return str(candidate.with_name(f"{candidate.stem}-branch{candidate.suffix}"))
    return DEFAULT_WORKING_COPY


def fetch_model(rid):
    """获取单个模型并输出摘要。"""
    print("=" * 60)
    print("示例 1: 获取已有算例")
    print("=" * 60)

    model = Model.fetch(rid)
    print(f"模型名称: {model.name}")
    print(f"模型 RID: {model.rid}")
    print(f"参数方案数量: {len(model.configs)}")
    print(f"计算方案数量: {len(model.jobs)}")
    print(f"元件数量: {len(model.getAllComponents())}")

    current_job_idx = model.context.get("currentJob")
    current_config_idx = model.context.get("currentConfig")
    print(f"当前计算方案索引: {current_job_idx}")
    print(f"当前参数方案索引: {current_config_idx}")

    return model


def search_models(keyword="IEEE"):
    """搜索可访问模型，帮助选择研究起点。"""
    print("\n" + "=" * 60)
    print("示例 2: 搜索可访问算例")
    print("=" * 60)

    matches = Model.fetchMany(name=keyword, pageSize=5)
    print(f"关键词 '{keyword}' 命中 {len(matches)} 个模型")
    for index, item in enumerate(matches, start=1):
        print(f"[{index}] {item['name']} | {item['rid']}")

    return matches


def create_local_working_copy(model, export_path=DEFAULT_WORKING_COPY):
    """为后续改模创建本地工作副本。"""
    print("\n" + "=" * 60)
    print("示例 3: 创建本地工作副本")
    print("=" * 60)

    Model.dump(model, export_path, compress=None)
    working_model = Model.load(export_path)

    print(f"已导出到: {export_path}")
    print(f"本地工作副本名称: {working_model.name}")
    print("后续建议在该副本上改模，再进入潮流或 EMT 工作流。")

    return working_model, export_path


def main():
    """主函数。"""
    print("CloudPSS SDK - Model 获取与研究起点示例")
    print("=" * 60)

    token = load_token()
    setToken(token)
    print("Token 已设置")

    print(f"- 可输入云端模型 RID，例如: {DEFAULT_READONLY_MODEL_RID}")
    print("- 也可输入本地 YAML，继续已有研究起点副本")

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
        model = load_model_from_source(model_source)
    except Exception as exc:
        print(f"获取模型失败: {exc}")
        return

    search_keyword = input("\n请输入搜索关键词，直接回车使用 'IEEE': ").strip() or "IEEE"
    try:
        search_models(search_keyword)
    except Exception as exc:
        print(f"搜索模型失败: {exc}")

    try:
        default_working_copy = suggest_working_copy_path(model_source)
        working_copy_path = (
            input(
                "\n请输入本地工作副本路径，直接回车使用 "
                f"[{default_working_copy}]: "
            ).strip()
            or default_working_copy
        )
        create_local_working_copy(model, working_copy_path)
    except Exception as exc:
        print(f"创建本地工作副本失败: {exc}")

    print("\n提示:")
    print("- `model/holdme/IEEE39` 适合作为只读示例和真实 API 验证入口")
    print("- 如果你后续要调用 `save()`，请切换到你自己有写权限的模型")


if __name__ == "__main__":
    main()
