# coding=UTF-8
"""
EMT 仿真运行示例

本示例面向普通云仿真和离线研究工作流，默认走完以下主线：
- 获取一个已完成潮流校核或已准备好扰动场景的模型
- 检查 emtp 视角下的拓扑
- 运行 EMT 仿真并等待完成
- 提取波形分组、通道名称和通道数据
- 读取原始 plot 消息，辅助排查结果来源
- 按需导出 CSV 供后续稳定性分析

实时控制接口会在示例里保留说明，但不作为默认执行路径。
"""

import os
from pathlib import Path
import sys
import time

from cloudpss import Model, Job, setToken


DEFAULT_READONLY_MODEL_RID = os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39")
DEFAULT_PREPARED_MODEL_PATH = "examples/basic/ieee3-emt-prepared.yaml"


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
    """
    从云端 RID 或本地 YAML/JSON 文件加载模型。

    `Model.load()` 得到的是本地工作副本，但后续 `runEMT()` 仍会把当前
    revision 提交到 CloudPSS 创建真实仿真任务。
    """
    candidate = Path(source).expanduser()
    file_like = candidate.suffix.lower() in {".yaml", ".yml", ".json"}

    if candidate.exists():
        model = Model.load(str(candidate))
        print(f"本地模型文件: {candidate}")
        print(f"模型：{model.name}")
        print(f"模型 RID: {model.rid}")
        return model

    if file_like:
        raise FileNotFoundError(f"未找到本地模型文件: {candidate}")

    model = Model.fetch(source)
    print(f"云端模型 RID: {source}")
    print(f"模型：{model.name}")
    print(f"模型 RID: {model.rid}")
    return model


def describe_job(job):
    """提取 live `Job` 实例上稳定可读的字段，避免假设 `job.name` 必然存在。"""
    context = getattr(job, "context", None) or []
    label = getattr(job, "name", None) or (context[0] if context else "N/A")

    return {
        "id": getattr(job, "id", "N/A"),
        "label": label,
        "context": context,
    }


def describe_plot(plot, index):
    """优先使用 live 结果里更稳定的 key，再回退到可选的 name。"""
    return plot.get("key") or plot.get("name") or f"Plot {index}"


def example_run_emt_simulation(model, job_name=None, config_name=None):
    """
    示例 1: 运行 EMT 仿真

    使用 model.runEMT() 运行电磁暂态仿真

    :param model: Model 实例
    :param job_name: 计算方案名称（可选，默认使用当前选中的方案）
    :param config_name: 参数方案名称（可选，默认使用当前选中的方案）
    :return: Job 实例
    """
    print("=" * 50)
    print("示例 1: 运行 EMT 仿真")
    print("=" * 50)

    try:
        if job_name or config_name:
            print("运行指定 EMT 方案...")
            job = model.runEMT(job=job_name, config=config_name)
        else:
            print("运行默认 EMT 仿真...")
            job = model.runEMT()

        job_info = describe_job(job)
        print(f"仿真任务已创建:")
        print(f"  任务 ID: {job_info['id']}")
        print(f"  任务标签: {job_info['label']}")
        if job_info["context"]:
            print(f"  任务上下文: {job_info['context']}")

        return job

    except Exception as e:
        print(f"运行仿真失败：{e}")
        print("\n可能的原因:")
        print("  1. 项目没有 EMT 计算方案")
        print("  2. 指定的计算方案不存在")
        print("  3. 参数方案不完整")
        return None


def inspect_emt_topology(model):
    """
    示例 1.5: 检查 EMT 拓扑

    在正式仿真前，先确认 emtp 视角下的 revision 拓扑可以正确展开。
    """
    print("\n" + "=" * 50)
    print("示例 1.5: 检查 EMT 拓扑")
    print("=" * 50)
    print("注意: 这一步适合做 revision/config 展开检查，不单独证明未保存本地改动已进入 EMT 求解器。")

    try:
        topology = model.fetchTopology(implementType="emtp")
        topology_data = topology.toJSON()
        component_count = len(topology_data.get("components", {}))
        mapping_keys = list(topology_data.get("mappings", {}).keys())

        print(f"拓扑元件数: {component_count}")
        print(f"映射键预览: {mapping_keys[:5]}")
        return topology_data
    except Exception as e:
        print(f"获取 EMT 拓扑失败：{e}")
        print("请先回到建模阶段确认故障场景、量测装置和 EMT 拓扑配置。")
        return None


def wait_for_completion(job, timeout=300, interval=3):
    """等待 EMT 任务完成。"""
    start_time = time.time()
    status_map = {0: "运行中", 1: "已完成", 2: "失败"}

    while True:
        status = job.status()
        if status == 1:
            print("  状态：已完成")
            return status
        if status == 2:
            print("  状态：失败")
            return status

        elapsed = int(time.time() - start_time)
        print(f"  状态：{status_map.get(status, status)} ({elapsed}s)")
        if elapsed > timeout:
            print("  状态：超时")
            return -1

        time.sleep(interval)


def example_check_job_status(job):
    """
    示例 2: 检查任务状态

    使用 job.status() 检查仿真任务状态

    :param job: Job 实例
    """
    if job is None:
        return

    print("\n" + "=" * 50)
    print("示例 2: 检查任务状态")
    print("=" * 50)

    try:
        status = job.status()

        # 状态码说明
        status_map = {
            0: "运行中",
            1: "已完成",
            2: "失败"
        }

        print(f"当前状态：{status_map.get(status, f'未知 ({status})')}")
        print(f"状态码：{status}")

        # 等待仿真完成
        if status == 0:
            print("\n仿真仍在运行，等待完成...")
            wait_for_completion(job)
            final_status = job.status()
            print(f"仿真完成，最终状态：{status_map.get(final_status)}")

        return job.status()

    except Exception as e:
        print(f"检查状态失败：{e}")
        return None


def example_abort_job(job):
    """
    示例 3: 中止仿真任务

    使用 job.abort() 中止正在运行的仿真

    :param job: Job 实例
    """
    if job is None:
        return

    print("\n" + "=" * 50)
    print("示例 3: 中止仿真任务")
    print("=" * 50)

    try:
        current_status = job.status()
        if current_status != 0:
            print("任务未运行，无需中止")
            return

        print("正在中止仿真...")
        job.abort(timeout=3)
        print("仿真已中止")

    except Exception as e:
        print(f"中止失败：{e}")


def example_get_emt_result(job):
    """
    示例 4: 获取 EMT 仿真结果

    使用 job.result 获取 EMTResult 实例并处理结果

    :param job: Job 实例
    """
    if job is None:
        return

    print("\n" + "=" * 50)
    print("示例 4: 获取 EMT 仿真结果")
    print("=" * 50)

    try:
        # 检查仿真是否完成
        if job.status() != 1:
            print("仿真未完成，无法获取结果")
            return

        # 获取结果对象
        result = job.result

        if result is None:
            print("结果为空")
            return

        print(f"结果类型：{type(result).__name__}")
        plots = list(result.getPlots())
        print(f"波形分组数量：{len(plots)}")
        if plots:
            print(f"首个波形分组：{describe_plot(plots[0], 0)}")

        return result

    except Exception as e:
        print(f"获取结果失败：{e}")
        return None


def example_job_stream_endpoints(job):
    """
    示例 4.5: 查看任务流式输入输出接口

    使用 job.read() / job.write() 连接消息流。
    默认不主动执行，避免在普通示例运行时建立额外连接。
    """
    if job is None:
        return

    print("\n" + "=" * 50)
    print("示例 4.5: 任务流式接口")
    print("=" * 50)

    print(f"输出流地址: {job.output}")
    print(f"输入流地址: {job.input}")
    print("如需读取流式消息，可调用: receiver = job.read(timeout=5)")
    print("如需写入实时控制，可调用: sender = job.write(timeout=5)")


def example_realtime_controls(result):
    """
    示例 4.6: EMT 实时控制接口

    这些接口依赖流式 sender，通常在可暂停/可交互仿真中使用。
    默认不主动执行，只展示调用方式。
    """
    if result is None:
        return

    print("\n" + "=" * 50)
    print("示例 4.6: EMT 实时控制接口")
    print("=" * 50)

    print("单步推进: result.next()")
    print("跳转到指定步: result.goto(100)")
    print("发送虚拟输入: result.send({'breaker': 'open'})")
    print("写共享内存: result.writeShm('/tmp/buffer', b'data', 0)")
    print("修改参数: result.control({'key': 'R1', 'value': 200})")
    print(
        "添加监视器: result.monitor({'key': 'Ia', 'function': 'abs', 'period': 1, 'value': 2.0, 'freq': 50, 'condition': '>', 'cycle': 1, 'nCount': 1})"
    )
    print("保存断面: result.saveSnapshot(1)")
    print("加载断面: result.loadSnapshot(1)")
    print("停止仿真: result.stopSimulation()")


def example_process_plot_data(result):
    """
    示例 5: 处理波形数据

    使用 EMTResult 的方法处理仿真波形数据

    :param result: EMTResult 实例
    """
    if result is None:
        return

    print("\n" + "=" * 50)
    print("示例 5: 处理波形数据")
    print("=" * 50)

    try:
        # 1. 获取所有波形
        print("1. 获取所有波形分组:")
        plots = list(result.getPlots())
        print(f"   波形分组数量：{len(plots)}")
        if not plots:
            print("   未发现波形分组；请先检查示波器、量测装置或输出通道配置。")
            return None

        for i, plot in enumerate(plots):
            print(f"   [{i}] {describe_plot(plot, i)}")

        # 2. 获取指定波形
        print("\n2. 获取第一个波形分组:")
        first_plot = result.getPlot(0)
        if first_plot:
            print(f"   分组标识：{describe_plot(first_plot, 0)}")
            print(f"   曲线数量：{len(first_plot.get('data', {}).get('traces', []))}")

        # 3. 获取通道名称
        print("\n3. 获取第一个波形的所有通道:")
        channel_names = result.getPlotChannelNames(0)
        if channel_names:
            for i, name in enumerate(channel_names):
                print(f"   [{i}] {name}")

        # 4. 获取通道数据
        print("\n4. 获取第一个通道的数据:")
        if channel_names:
            first_channel = channel_names[0]
            channel_data = result.getPlotChannelData(0, first_channel)
            if channel_data:
                print(f"   通道名称：{channel_data.get('name')}")
                print(f"   X 数据点数：{len(channel_data.get('x', []))}")
                print(f"   Y 数据点数：{len(channel_data.get('y', []))}")
                # 显示前 5 个数据点
                if channel_data.get('x') and channel_data.get('y'):
                    print(f"   前 5 个点：")
                    for i in range(min(5, len(channel_data['x']))):
                        print(f"     [{i}] t={channel_data['x'][i]:.6f}, y={channel_data['y'][i]:.6f}")

        return {
            "plots": plots,
            "channel_names": channel_names,
            "channel_data": channel_data if channel_names else None,
        }

        # 5. 导出数据到 CSV（示例）
        # import csv
        # with open('output.csv', 'w', newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(['time', first_channel])
        #     for i, t in enumerate(channel_data['x']):
        #         writer.writerow([t, channel_data['y'][i]])
        # print("\n数据已导出到 output.csv")

    except Exception as e:
        print(f"处理数据失败：{e}")
        return None


def export_first_channel_csv(channel_data, output_path="emt-output.csv"):
    """导出首个通道数据到 CSV。"""
    if not channel_data:
        print("没有可导出的通道数据")
        return

    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write("time,value\n")
        for x, y in zip(channel_data["x"], channel_data["y"]):
            output_file.write(f"{x},{y}\n")

    print(f"首个通道已导出到: {output_path}")


def example_inspect_raw_messages(result):
    """
    示例 5.5: 检查 EMT 原始消息

    使用 getMessagesByKey() 保留原始 plot 分段消息。
    """
    if result is None:
        return

    print("\n" + "=" * 50)
    print("示例 5.5: 检查 EMT 原始消息")
    print("=" * 50)

    try:
        plots = list(result.getPlots())
        if not plots:
            print("未找到波形分组")
            return

        first_plot_key = plots[0].get("key", "plot-0")
        raw_messages = result.getMessagesByKey(first_plot_key)

        print(f"原始消息 key: {first_plot_key}")
        print(f"原始消息数量: {len(raw_messages)}")
        if raw_messages:
            print(f"首条消息 type: {raw_messages[0].get('type')}")
            trace_count = len(raw_messages[0].get("data", {}).get("traces", []))
            print(f"首条消息 trace 数量: {trace_count}")

    except Exception as e:
        print(f"检查原始消息失败：{e}")


def example_fetch_job_by_id(job_id):
    """
    示例 6: 通过 ID 获取任务

    使用 Job.fetch() 通过任务 ID 获取已有的仿真任务

    :param job_id: 任务 ID
    """
    print("\n" + "=" * 50)
    print("示例 6: 通过 ID 获取任务")
    print("=" * 50)

    try:
        job = Job.fetch(job_id)
        job_info = describe_job(job)
        print(f"任务标签: {job_info['label']}")
        if job_info["context"]:
            print(f"任务上下文: {job_info['context']}")
        print(f"任务状态：{job.status()}")

        return job

    except Exception as e:
        print(f"获取任务失败：{e}")
        return None


def example_emt_workflow(model):
    """
    示例 7: 完整 EMT 仿真工作流

    演示从创建任务到获取结果的完整流程

    :param model: Model 实例
    """
    if model is None:
        return

    print("\n" + "=" * 50)
    print("示例 7: 完整 EMT 仿真工作流")
    print("=" * 50)

    try:
        # 步骤 1: 检查 EMT 拓扑
        print("步骤 1: 检查 EMT 拓扑")
        topology_data = inspect_emt_topology(model)
        if topology_data is None:
            print("  EMT 拓扑检查失败，停止工作流")
            return

        # 步骤 2: 运行仿真
        print("\n步骤 2: 运行 EMT 仿真")
        job = model.runEMT()
        print(f"  任务已创建：{job.id}")

        # 步骤 3: 等待完成
        print("\n步骤 3: 等待仿真完成")
        wait_for_completion(job)

        # 步骤 4: 检查结果
        print("\n步骤 4: 检查结果")
        final_status = job.status()
        if final_status == 1:
            print("  仿真成功完成")

            # 步骤 5: 获取结果
            result = job.result
            if result:
                plot_info = example_process_plot_data(result)
                example_inspect_raw_messages(result)
                if plot_info and plot_info.get("channel_data"):
                    print("  可按需将首个通道导出到 CSV，供后续稳定性分析使用")
        elif final_status == 2:
            print("  仿真失败")
        else:
            print(f"  仿真未完成（超时或中止）")

    except Exception as e:
        print(f"工作流执行失败：{e}")


def main():
    """主函数 - 运行普通云 EMT 主线示例"""
    print("CloudPSS SDK - EMT 仿真运行示例")
    print("=" * 50)

    token = load_token()
    setToken(token)
    print("Token 已设置")

    print("\n步骤 1: 获取项目")
    print("-" * 50)
    print(f"- 可输入云端模型 RID，例如: {DEFAULT_READONLY_MODEL_RID}")
    print(f"- 也可输入本地 YAML，例如: {DEFAULT_PREPARED_MODEL_PATH}")

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
    except Exception as e:
        print(f"无法获取项目：{e}")
        print("请确认 token 正确，并使用有访问权限的模型 RID 或有效的本地 YAML 路径")
        return

    topology_data = inspect_emt_topology(model)
    if topology_data is None:
        print("\nEMT 拓扑检查未通过，已停止后续仿真。")
        return

    job = example_run_emt_simulation(model)
    if job is None:
        return

    final_status = example_check_job_status(job)
    if final_status != 1:
        print("EMT 仿真未成功完成，无法继续提取波形。")
        return

    result = example_get_emt_result(job)
    if result is None:
        return

    plot_info = example_process_plot_data(result)
    example_inspect_raw_messages(result)

    if plot_info and plot_info.get("channel_data"):
        confirm = input("\n是否将首个通道导出为 CSV? (y/n): ").strip().lower()
        if confirm == "y":
            output_path = input("请输入输出路径 [emt-output.csv]: ").strip() or "emt-output.csv"
            export_first_channel_csv(plot_info["channel_data"], output_path)

    print("\n补充说明:")
    print("- 本地 YAML 入口适合承接 IEEE3 这类研究分支准备副本，再直接提交 EMT 仿真")
    print("- 若需要持续迭代故障或扰动场景，建议先回到本地研究分支继续改模")
    print("- 实时控制接口属于延后能力，不是普通云仿真的默认主线")

    print("\n" + "=" * 50)
    print("示例运行完成")
    print("=" * 50)


if __name__ == '__main__':
    main()
