"""
Shared helpers for EMT fault-study style skills.
"""

from copy import deepcopy
from typing import Any, Dict, Optional, Tuple
from cloudpss_skills.core.auth_utils import get_cloudpss_kwargs


FAULT_DEFINITION = "model/CloudPSS/_newFaultResistor_3p"
CHANNEL_DEFINITION = "model/CloudPSS/_newChannel"
EMT_JOB_RID = "function/CloudPSS/emtps"


def clone_model(base_model):
    from cloudpss import Model

    return Model(deepcopy(base_model.toJSON()))


def find_fault_component(model):
    for comp in model.getAllComponents().values():
        if getattr(comp, "definition", None) == FAULT_DEFINITION:
            return comp
    raise ValueError("未找到故障元件")


def apply_fault_parameters(model, fs: Any, fe: Any, chg: Any):
    fault = find_fault_component(model)
    model.updateComponent(
        fault.id,
        args={
            "fs": {"source": str(fs), "ɵexp": ""},
            "fe": {"source": str(fe), "ɵexp": ""},
            "chg": {"source": str(chg), "ɵexp": ""},
        },
    )
    return fault


def find_named_channel_component(model, channel_name: str):
    for comp in model.getAllComponents().values():
        if getattr(comp, "definition", None) == CHANNEL_DEFINITION and comp.args.get("Name") == channel_name:
            return comp
    raise ValueError(f"未找到电压量测通道: {channel_name}")


def configure_channel_sampling(model, channel_name: str, sampling_freq: int):
    channel = find_named_channel_component(model, channel_name)
    emt_job = next((job for job in model.jobs if job["rid"] == EMT_JOB_RID), None)
    if not emt_job:
        raise ValueError("未找到EMT任务")

    output_group = None
    for group in emt_job["args"]["output_channels"]:
        if channel.id in group.get("4", []):
            output_group = group
            break
    if output_group is None:
        raise ValueError(f"未找到包含通道 {channel.id} 的EMT输出分组")

    model.updateComponent(
        channel.id,
        args={**channel.args, "Freq": {"source": str(sampling_freq), "ɵexp": ""}},
    )
    output_group["1"] = int(sampling_freq)
    return channel


def run_emt_and_wait(model, timeout: int = 300, poll_seconds: int = 3, log_func=None, config: Optional[Dict] = None):
    import time

    job = model.runEMT(**get_cloudpss_kwargs(config))
    start_time = time.time()
    while True:
        status = job.status()
        if status == 1:
            if log_func:
                log_func("INFO", "  仿真完成")
            return job
        if status == 2:
            raise RuntimeError("EMT仿真失败")
        if time.time() - start_time > timeout:
            raise TimeoutError("EMT仿真超时")
        time.sleep(poll_seconds)


def find_trace(result, trace_name: str) -> Tuple[int, Dict[str, Any]]:
    for plot_index, _ in enumerate(result.getPlots()):
        channel_names = result.getPlotChannelNames(plot_index)
        if trace_name in channel_names:
            trace = result.getPlotChannelData(plot_index, trace_name)
            return plot_index, trace
    raise KeyError(f"未找到目标通道 {trace_name}")


def trace_rms(trace: Dict[str, Any], start_time: float, end_time: float) -> float:
    import math

    samples = [
        value
        for time_value, value in zip(trace["x"], trace["y"])
        if start_time <= time_value <= end_time
    ]
    if not samples:
        raise ValueError(f"时间窗口 {start_time}..{end_time} 内无数据")
    return math.sqrt(sum(v * v for v in samples) / len(samples))


def trace_value_at_time(trace: Dict[str, Any], target_time: float, tolerance: float = 0.001) -> float:
    for time_value, value in zip(trace["x"], trace["y"]):
        if abs(time_value - target_time) < tolerance:
            return value
    raise ValueError(f"在 {target_time}s 附近未找到目标通道采样点")
