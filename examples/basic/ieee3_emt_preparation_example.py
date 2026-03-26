"""
IEEE3 EMT preparation example

Run with: python examples/basic/ieee3_emt_preparation_example.py
Prerequisite: a valid CloudPSS token stored in .cloudpss_token

This example uses the verified readable model `model/holdme/IEEE3` and shows a
minimal, local-only EMT preparation workflow:
- fetch the IEEE3 template from CloudPSS
- create a local working copy
- inspect the fault -> meter -> output channel chain
- adjust fault timing on the local working copy
- adjust EMT output channel sampling on the local working copy
- save the modified working copy for later EMT runs
"""

from pathlib import Path
import sys

from cloudpss import Model, setToken


DEFAULT_MODEL_RID = "model/holdme/IEEE3"
DEFAULT_WORKING_COPY = "examples/basic/ieee3-emt-working-copy.yaml"
DEFAULT_PREPARED_COPY = "examples/basic/ieee3-emt-prepared.yaml"


def load_token():
    """Read the CloudPSS token from the project root."""
    token_path = Path(".cloudpss_token")
    if not token_path.exists():
        print("错误: 未找到 .cloudpss_token 文件")
        print("请先把 CloudPSS API token 写入项目根目录的 .cloudpss_token")
        sys.exit(1)
    return token_path.read_text().strip()


def fetch_source_model(model_rid=DEFAULT_MODEL_RID):
    """Fetch the verified IEEE3 template."""
    print("=" * 60)
    print("步骤 1: 获取 IEEE3 研究起点")
    print("=" * 60)

    model = Model.fetch(model_rid)
    print(f"模型名称: {model.name}")
    print(f"模型 RID: {model.rid}")
    print(f"计算方案: {[job['rid'] for job in model.jobs]}")
    return model


def create_local_working_copy(model, export_path=DEFAULT_WORKING_COPY):
    """Create a local-only working copy before any EMT preparation changes."""
    print("\n" + "=" * 60)
    print("步骤 2: 创建本地工作副本")
    print("=" * 60)

    Model.dump(model, export_path, compress=None)
    working_model = Model.load(export_path)
    print(f"已创建本地工作副本: {export_path}")
    return working_model


def find_components_for_emt_preparation(model):
    """Locate the fault, meter, and output channel chain on IEEE3."""
    print("\n" + "=" * 60)
    print("步骤 3: 识别故障、量测与输出链")
    print("=" * 60)

    components = model.getAllComponents()

    fault = next(
        component
        for component in components.values()
        if getattr(component, "definition", None) == "model/CloudPSS/_newFaultResistor_3p"
    )
    voltage_meter = next(
        component
        for component in components.values()
        if getattr(component, "definition", None) == "model/CloudPSS/_NewVoltageMeter"
    )

    voltage_signal = voltage_meter.args["V"]
    output_channel = next(
        component
        for component in components.values()
        if getattr(component, "definition", None) == "model/CloudPSS/_newChannel"
        and component.args.get("Name") == voltage_signal.lstrip("#")
    )

    emt_job = next(job for job in model.jobs if job["rid"] == "function/CloudPSS/emtps")
    output_group = next(
        group
        for group in emt_job["args"]["output_channels"]
        if output_channel.id in group["4"]
    )

    print(f"故障元件: {fault.label} ({fault.id})")
    print(f"  当前故障起始时间 fs: {fault.args['fs']['source']}")
    print(f"  当前故障结束时间 fe: {fault.args['fe']['source']}")
    print(f"电压量测元件: {voltage_meter.label} ({voltage_meter.id})")
    print(f"  量测信号: {voltage_signal}")
    print(f"输出通道元件: {output_channel.label} ({output_channel.id})")
    print(f"  通道名称: {output_channel.args['Name']}")
    print(f"  通道采样频率: {output_channel.args['Freq']['source']}")
    print(f"EMT 输出分组: {output_group['0']}")
    print(f"  分组采样频率: {output_group['1']}")
    print(f"  分组窗口类型: {output_group['2']}")

    return fault, voltage_meter, output_channel, emt_job, output_group


def update_fault_timing(model, fault_component):
    """Update fault start/end times on the local working copy."""
    print("\n" + "=" * 60)
    print("步骤 4: 微调故障时间")
    print("=" * 60)

    new_start = input("请输入新的故障起始时间 fs [2.5]: ").strip() or "2.5"
    new_end = input("请输入新的故障结束时间 fe [2.7]: ").strip() or "2.7"

    model.updateComponent(
        fault_component.id,
        args={
            "fs": {"source": new_start, "ɵexp": ""},
            "fe": {"source": new_end, "ɵexp": ""},
        },
    )

    updated_fault = model.getComponentByKey(fault_component.id)
    print(f"更新后 fs: {updated_fault.args['fs']['source']}")
    print(f"更新后 fe: {updated_fault.args['fe']['source']}")


def update_output_channel_sampling(model, output_channel, emt_output_group):
    """Align the signal channel and EMT output group sampling frequency."""
    print("\n" + "=" * 60)
    print("步骤 5: 微调输出通道采样")
    print("=" * 60)

    new_freq = input("请输入新的输出采样频率 [2000]: ").strip() or "2000"

    model.updateComponent(
        output_channel.id,
        args={"Freq": {"source": new_freq, "ɵexp": ""}},
    )
    emt_output_group["1"] = int(new_freq)

    updated_channel = model.getComponentByKey(output_channel.id)
    print(f"输出通道 Freq: {updated_channel.args['Freq']['source']}")
    print(f"EMT 输出分组采样频率: {emt_output_group['1']}")


def save_prepared_working_copy(model, export_path=DEFAULT_PREPARED_COPY):
    """Persist the prepared local copy for later EMT runs."""
    print("\n" + "=" * 60)
    print("步骤 6: 保存准备后的本地副本")
    print("=" * 60)

    Model.dump(model, export_path, compress=None)
    print(f"已保存本地 EMT 准备副本: {export_path}")
    print("下一步建议:")
    print(f"- 运行: python examples/simulation/run_emt_simulation.py {export_path}")
    print("- 或继续调整故障参数、量测信号和输出分组")


def main():
    """Run the local-only IEEE3 EMT preparation flow."""
    print("CloudPSS SDK - IEEE3 EMT 前置准备示例")
    print("=" * 60)

    setToken(load_token())
    print("Token 已设置")

    source_model = fetch_source_model()
    working_model = create_local_working_copy(source_model)
    fault, _meter, output_channel, emt_job, output_group = find_components_for_emt_preparation(
        working_model
    )
    update_fault_timing(working_model, fault)
    update_output_channel_sampling(working_model, output_channel, output_group)
    save_prepared_working_copy(working_model)

    print("\n提示:")
    print("- 这个示例只操作本地工作副本，不会创建新的云端算例")
    print("- 它演示的是最小 EMT 前置链，不是通用的任意模型故障脚本化配方")
    print(f"- 当前 EMT 方案 RID: {emt_job['rid']}")


if __name__ == "__main__":
    main()
