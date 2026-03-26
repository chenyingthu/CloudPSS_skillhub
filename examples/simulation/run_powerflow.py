"""
CloudPSS Power Flow Simulation Example

运行方式: python examples/simulation/run_powerflow.py
前置条件: 有效的 CloudPSS token 保存在 .cloudpss_token

本示例面向离线研究工作流中的潮流试算阶段，演示：
- 获取一个研究模型
- 检查 powerFlow 视角下的拓扑
- 运行潮流计算
- 读取节点、支路和原始消息
- 将结果写回模型数据，并优先保存为本地研究副本
"""

import os
from pathlib import Path
import sys
import time

from cloudpss import Model, setToken


DEFAULT_READONLY_MODEL_RID = os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39")
DEFAULT_LOCAL_SNAPSHOT = "study-case-after-powerflow.yaml"


def load_token():
    """从文件加载 API token。"""
    try:
        with open(".cloudpss_token", "r") as token_file:
            return token_file.read().strip()
    except FileNotFoundError:
        print("错误: 未找到 .cloudpss_token 文件")
        print("请将 CloudPSS API token 保存到项目根目录的 .cloudpss_token 文件中")
        sys.exit(1)


def load_model_from_source(source):
    """从云端 RID 或本地 YAML/JSON 研究副本加载模型。"""
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


def describe_table_column(column):
    """优先使用 live 结果里的 `name`，并兼容旧写法。"""
    return column.get("name") or column.get("title") or "Unknown"


def wait_for_completion(job, timeout=300, interval=2):
    """等待任务完成。"""
    start_time = time.time()

    while True:
        status = job.status()

        if status == 1:
            print("  状态: 完成")
            return status
        if status == 2:
            print("  状态: 失败")
            return status

        elapsed = int(time.time() - start_time)
        print(f"  状态: 运行中 ({elapsed}s)...")
        if elapsed > timeout:
            print("  状态: 超时")
            return -1

        time.sleep(interval)


def inspect_powerflow_topology(model):
    """在正式潮流计算前检查 powerFlow 视角下的 revision 拓扑。"""
    print("\n=== 检查潮流拓扑 ===")
    print("注意: 这一步适合做 revision/config 展开检查，不单独证明未保存本地改动已进入求解器。")

    try:
        topology = model.fetchTopology(implementType="powerFlow")
        topology_data = topology.toJSON()
        component_count = len(topology_data.get("components", {}))
        mapping_keys = list(topology_data.get("mappings", {}).keys())

        print(f"拓扑元件数: {component_count}")
        print(f"映射键预览: {mapping_keys[:5]}")
        return topology_data
    except Exception as exc:
        print(f"获取潮流拓扑失败: {exc}")
        print("请先返回建模阶段修正拓扑或参数，再重新进行潮流试算。")
        return None


def run_powerflow(model):
    """运行潮流计算。"""
    print("\n=== 运行潮流计算 ===")

    try:
        print("启动潮流计算...")
        job = model.runPowerFlow()
        print(f"任务 ID: {job.id}")

        status = wait_for_completion(job)
        if status == 1:
            print("\n潮流计算成功完成!")
            return job.result
        if status == 2:
            print("\n潮流计算失败")
            return None
        return None
    except Exception as exc:
        print(f"运行潮流计算失败: {exc}")
        return None


def analyze_powerflow_result(result):
    """分析潮流结果。"""
    print("\n=== 分析潮流结果 ===")

    if not result:
        return

    try:
        print("\n--- 原始消息 ---")
        bus_messages = result.getMessagesByKey("buses-table")
        branch_messages = result.getMessagesByKey("branches-table")
        modify_messages = result.getMessagesByKey("power-flow-modify")
        print(f"buses-table 消息数: {len(bus_messages)}")
        print(f"branches-table 消息数: {len(branch_messages)}")
        print(f"power-flow-modify 消息数: {len(modify_messages)}")

        print("\n--- 节点数据 ---")
        buses = result.getBuses()
        print(f"节点数据块数: {len(buses)}")
        if buses:
            for col in buses[0]["data"]["columns"]:
                print(f"  {describe_table_column(col)}: {col.get('data', [])[:5]}...")

        print("\n--- 支路数据 ---")
        branches = result.getBranches()
        print(f"支路数据块数: {len(branches)}")
        if branches:
            for col in branches[0]["data"]["columns"]:
                print(f"  {describe_table_column(col)}: {col.get('data', [])[:5]}...")
    except Exception as exc:
        print(f"分析结果失败: {exc}")


def build_modified_model_from_result(model, result):
    """将潮流结果回写到可变模型字典，并重建为新的本地研究副本对象。"""
    model_data = model.toJSON()
    result.powerFlowModify(model_data)
    return Model(model_data)


def save_modified_model_locally(model, result):
    """将潮流结果写回模型，并优先保存本地研究副本。"""
    print("\n=== 将潮流结果写入模型 ===")

    try:
        modified_model = build_modified_model_from_result(model, result)

        print("潮流结果已写入模型数据")
        print(f"写回后的模型名称: {modified_model.name}")
        print("建议先把它作为下一轮试算或 EMT 仿真的本地研究副本。")

        local_path = input(
            "请输入本地副本路径，直接回车使用 "
            f"[{DEFAULT_LOCAL_SNAPSHOT}]: "
        ).strip() or DEFAULT_LOCAL_SNAPSHOT
        Model.dump(modified_model, local_path, compress=None)
        print(f"已保存本地研究副本: {local_path}")

        confirm = input(
            "是否在确认写权限后另存为新的云端研究分支? (y/n): "
        ).strip().lower()
        if confirm == "y":
            new_key = input("请输入新的模型 key: ").strip()
            if new_key:
                response = modified_model.save(new_key)
                print(f"模型已另存为新的云端研究分支: {modified_model.rid}")
                print(f"返回字段: {list(response.get('data', {}).keys())}")
            else:
                print("未提供新 key，跳过云端另存。")

    except Exception as exc:
        print(f"写入模型失败: {exc}")
        print("若失败发生在 powerFlowModify()，请先检查结果消息中是否存在 power-flow-modify。")


def main():
    """主函数。"""
    print("CloudPSS 潮流计算仿真示例")
    print("=" * 50)

    token = load_token()
    setToken(token)
    print("Token 已设置")

    print(f"- 可输入云端模型 RID，例如: {DEFAULT_READONLY_MODEL_RID}")
    print("- 也可输入本地 YAML，例如: study-case-after-powerflow.yaml")

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
    except Exception as exc:
        print(f"获取模型失败: {exc}")
        return

    topology_data = inspect_powerflow_topology(model)
    if topology_data is None:
        print("\n拓扑检查未通过，已停止后续潮流试算。")
        return

    result = run_powerflow(model)

    if result:
        analyze_powerflow_result(result)

        confirm = input("\n是否将潮流结果写回模型数据? (y/n): ").strip().lower()
        if confirm == "y":
            save_modified_model_locally(model, result)

    print("\n潮流计算示例完成!")


if __name__ == "__main__":
    main()
