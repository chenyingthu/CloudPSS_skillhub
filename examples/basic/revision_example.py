"""
CloudPSS ModelRevision Version Management Example

运行方式: python examples/basic/revision_example.py
前置条件: 有效的CloudPSS token保存在 .cloudpss_token

本示例演示如何在研究流程中使用 ModelRevision 做辅助工作：
- 查看当前 revision 数据
- 拉取指定实现视角下的拓扑
- 显式使用 revision.run() 提交任务
"""

import os
from pathlib import Path
import sys

from cloudpss import Model, setToken


DEFAULT_READONLY_MODEL_RID = os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39")


def load_token():
    """从文件加载 API token"""
    try:
        with open('.cloudpss_token', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("错误: 未找到 .cloudpss_token 文件")
        print("请将 CloudPSS API token 保存到项目根目录的 .cloudpss_token 文件中")
        sys.exit(1)


def load_model_from_source(source):
    """从云端 RID 或本地 YAML/JSON 加载模型。"""
    candidate = Path(source).expanduser()
    file_like = candidate.suffix.lower() in {".yaml", ".yml", ".json"}

    if candidate.exists():
        model = Model.load(str(candidate))
        print(f"本地模型文件: {candidate}")
        print(f"模型名称: {model.name}")
        print(f"模型 RID: {model.rid}")
        return model

    if file_like:
        raise FileNotFoundError(f"未找到本地模型文件: {candidate}")

    model = Model.fetch(source)
    print(f"云端模型 RID: {source}")
    print(f"模型名称: {model.name}")
    print(f"模型 RID: {model.rid}")
    return model


def example_revision_info(model):
    """查看版本信息示例"""
    print("\n=== 版本信息示例 ===")

    revision = model.revision

    # 基本信息
    print(f"版本 Hash: {revision.hash}")

    # 获取实现数据
    implements = revision.getImplements()
    print(f"实现类型: {type(implements).__name__}")

    # 序列化为 JSON
    revision_dict = revision.toJSON()
    print(f"版本数据键: {list(revision_dict.keys())}")

    return revision


def example_fetch_topology(model):
    """获取拓扑数据示例"""
    print("\n=== 拓扑数据示例 ===")

    revision = model.revision

    if not model.configs:
        print("模型缺少 config，无法获取拓扑。")
        return

    config = model.configs[0]

    try:
        # 获取 EMT 拓扑数据
        topology = revision.fetchTopology(
            implementType='emtp',
            config=config,
            maximumDepth=1
        )
        print(f"EMT 拓扑: {type(topology).__name__}")
        topo_data = topology.toJSON()
        print(f"  元件数: {len(topo_data.get('components', {}))}")
        print(f"  映射键: {list(topo_data.get('mappings', {}).keys())[:5]}")

    except Exception as e:
        print(f"获取拓扑失败: {e}")

    try:
        # 获取潮流拓扑数据
        pf_topology = revision.fetchTopology(
            implementType='powerFlow',
            config=config,
            maximumDepth=1
        )
        print(f"潮流拓扑: {type(pf_topology).__name__}")
        pf_topo_data = pf_topology.toJSON()
        print(f"  元件数: {len(pf_topo_data.get('components', {}))}")

    except Exception as e:
        print(f"获取潮流拓扑失败: {e}")


def example_create_revision(model):
    """创建新版本示例"""
    print("\n=== 创建新版本示例 ===")

    try:
        # 注意: 这会创建一个新版本但不会自动保存
        from cloudpss.model import ModelRevision
        new_revision = ModelRevision.create(model.revision)
        print(f"新版本 Hash: {new_revision['hash']}")
        return new_revision['hash']
    except Exception as e:
        print(f"创建版本失败: {e}")
        return None


def example_run_revision(model):
    """运行版本仿真示例"""
    print("\n=== 运行版本仿真示例 ===")

    try:
        revision = model.revision

        if not model.jobs or not model.configs:
            print("模型缺少 job 或 config，无法调用 revision.run()")
            return None

        print("运行指定 job/config 仿真...")
        job = revision.run(
            job=model.jobs[0],
            config=model.configs[0],
            name="revision-example-run",
            rid=model.rid,
        )
        print(f"任务 ID: {job.id}")
        print(f"任务状态: {job.status()} (0=运行中, 1=完成, 2=失败)")
        if getattr(job, "context", None):
            print(f"任务上下文: {job.context[0]}")

        # 注意: 实际等待完成需要轮询
        return job

    except Exception as e:
        print(f"运行仿真失败: {e}")
        return None


def example_run_with_config(model):
    """使用指定配置运行仿真示例"""
    print("\n=== 使用指定配置运行仿真示例 ===")

    try:
        revision = model.revision
        print(f"当前 revision hash: {revision.hash}")

        print("模型中的计算方案:")
        for job in model.jobs:
            print(f"  - {job.get('name')}: {job.get('rid')}")

        print("模型中的参数方案:")
        for config in model.configs:
            print(f"  - {config.get('name')}")

        # 尝试使用特定 job 和 config 运行
        # 注意: 需要根据实际的 job 和 config 名称调整
        # job = revision.run(
        #     job={'name': 'EMT Simulation'},
        #     config={'name': 'Default'},
        #     name='My Custom Task'
        # )

    except Exception as e:
        print(f"获取配置失败: {e}")


def main():
    """主函数"""
    print("CloudPSS 版本管理示例")
    print("=" * 50)

    # 加载 token 并设置
    token = load_token()
    setToken(token)
    print("Token 已设置")

    print(f"- 可输入云端模型 RID，例如: {DEFAULT_READONLY_MODEL_RID}")
    print("- 也可输入本地 YAML，检查已保存研究副本的 revision 数据")

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

    print(f"获取模型: {model_source}")
    try:
        model = load_model_from_source(model_source)
    except Exception as e:
        print(f"获取模型失败: {e}")
        return

    # 示例执行
    example_revision_info(model)
    example_fetch_topology(model)
    example_run_with_config(model)

    # 运行仿真 (可选)
    confirm = input("\n是否运行仿真测试? (y/n): ").strip().lower()
    if confirm == 'y':
        job = example_run_revision(model)
        if job:
            print("仿真任务已创建")

    print("\n版本管理示例完成!")


if __name__ == "__main__":
    main()
