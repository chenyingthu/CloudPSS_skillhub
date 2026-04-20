"""
CloudPSS Skills 工具函数模块

提供组件发现、数据解析、结果处理等通用工具函数
"""

import logging
import re
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from cloudpss_skills.core.auth_utils import get_cloudpss_kwargs

logger = logging.getLogger(__name__)


def fetch_job_with_result(job_id: str, config: Optional[Dict] = None):
    """
    获取任务及其结果。

    对 EMT 历史任务，CloudPSS SDK 的 ``Job.fetch(job_id).result`` 默认不会回放
    已结束任务的历史 plot 消息，导致 ``getPlots()`` 为空。这里在检测到空波形时，
    主动从输出流做一次历史回放。
    """
    from cloudpss import Job

    job = Job.fetch(job_id, **get_cloudpss_kwargs(config))
    result = job.result

    if result is None:
        return job, result

    if hasattr(result, "getPlots"):
        try:
            if len(list(result.getPlots())) == 0 and getattr(job, "output", None):
                replayed = replay_historical_emt_result(job)
                if replayed is not None:
                    job._result = replayed
                    result = replayed
        except Exception as e:
            logger.debug(f"历史 EMT 结果回放失败，回退到SDK默认结果: {e}")

    # PowerFlowResult 历史回放：已完成任务的 getBuses() 默认返回空
    if hasattr(result, "getBuses"):
        try:
            if len(result.getBuses()) == 0 and getattr(job, "output", None):
                replayed = replay_historical_emt_result(job)
                if replayed is not None:
                    job._result = replayed
                    result = replayed
        except Exception as e:
            logger.debug(f"历史潮流结果回放失败，回退到SDK默认结果: {e}")

    return job, result


def replay_historical_emt_result(job):
    """
    为已完成的 EMT 任务回放历史输出流，恢复 plot 数据。
    """
    import websocket
    from cloudpss.job.messageStreamReceiver import MessageStreamReceiver
    from cloudpss.job.result import getResultClass

    output_id = getattr(job, "output", None)
    if not output_id:
        return None

    receiver = MessageStreamReceiver(output_id, baseUrl=getattr(job, "baseUrl", None), job=job)
    path = receiver._MessageStreamReceiver__path("1970-01-01T00:00:00Z")
    ws = None

    try:
        ws = websocket.create_connection(
            path,
            header=["User-Agent: cloudpss-sdk-python/history-replay"],
            timeout=10,
        )
        setattr(ws, "url", path)
        receiver.ws = ws

        while True:
            try:
                message = ws.recv()
            except websocket.WebSocketConnectionClosedException:
                break

            if message is None:
                break

            if isinstance(message, str):
                continue

            receiver._MessageStreamReceiver__on_message(message)
    finally:
        if ws is not None:
            try:
                ws.close()
            except Exception:
                pass

    result_class = getResultClass(job.context[0])
    return result_class(job, receiver)


def get_components_by_type(model, comp_type: str) -> Dict[str, Dict]:
    """
    动态获取指定类型的组件列表

    Args:
        model: CloudPSS Model 对象
        comp_type: 组件类型，如 'model/CloudPSS/_newBus_3p', 'model/CloudPSS/TransmissionLine'

    Returns:
        组件字典，key为组件key，value为组件定义
    """
    try:
        if hasattr(model, "getRevision"):
            revision = model.getRevision()
            cells = revision.get("implements", {}).get("diagram", {}).get("cells", [])

            components = {}
            for cell in cells:
                if cell.get("type") == "standard.Image":
                    data = cell.get("data", {})
                    if data.get("rid") == comp_type:
                        components[cell.get("key")] = data

            logger.debug(f"通过revision获取到 {len(components)} 个类型为 {comp_type} 的组件")
            return components

        components = {}
        for key, comp in model.getAllComponents().items():
            if getattr(comp, "definition", None) != comp_type:
                continue
            components[key] = {
                "key": key,
                "label": getattr(comp, "label", ""),
                "name": getattr(comp, "name", ""),
                "args": getattr(comp, "args", {}) or {},
                "pins": getattr(comp, "pins", {}) or {},
                "definition": getattr(comp, "definition", ""),
            }

        logger.debug(f"通过getAllComponents获取到 {len(components)} 个类型为 {comp_type} 的组件")
        return components

    except Exception as e:
        logger.error(f"获取组件失败: {e}")
        return {}


def get_bus_components(model) -> Dict[str, Dict]:
    """获取所有母线组件"""
    return get_components_by_type(model, "model/CloudPSS/_newBus_3p")


def get_line_components(model) -> Dict[str, Dict]:
    """获取所有线路组件"""
    return get_components_by_type(model, "model/CloudPSS/TransmissionLine")


def get_generator_components(model) -> Dict[str, Dict]:
    """获取所有发电机组件"""
    return get_components_by_type(model, "model/CloudPSS/_newGenerator")


def convert_label_to_key(model, label: str) -> Optional[str]:
    """
    将组件label转换为component key

    Args:
        model: CloudPSS Model 对象
        label: 组件label（显示名称）

    Returns:
        组件key，如果找不到返回None
    """
    try:
        revision = model.getRevision()
        cells = revision.get("implements", {}).get("diagram", {}).get("cells", [])

        for cell in cells:
            if cell.get("type") == "standard.Image":
                if cell.get("data", {}).get("label") == label:
                    return cell.get("key")

        logger.warning(f"找不到label为 {label} 的组件")
        return None

    except Exception as e:
        logger.error(f"转换label到key失败: {e}")
        return None


def get_component_by_label(model, label: str) -> Optional[Dict]:
    """
    通过label获取组件定义

    Args:
        model: CloudPSS Model 对象
        label: 组件label

    Returns:
        组件定义字典，如果找不到返回None
    """
    try:
        revision = model.getRevision()
        cells = revision.get("implements", {}).get("diagram", {}).get("cells", [])

        for cell in cells:
            if cell.get("type") == "standard.Image":
                if cell.get("data", {}).get("label") == label:
                    return cell.get("data", {})

        logger.warning(f"找不到label为 {label} 的组件")
        return None

    except Exception as e:
        logger.error(f"获取组件失败: {e}")
        return None


def parse_html_column_name(html_name: str) -> str:
    """
    解析HTML编码的列名（如 '<i>V</i><sub>m</sub>' 转换为 'Vm'）

    Args:
        html_name: HTML格式的列名

    Returns:
        纯文本列名
    """
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', html_name)
    # 移除多余空格
    text = text.strip()
    # 移除单位部分（如 '/ pu', '/ kV'）
    text = re.sub(r'\s*/\s*\w+', '', text)
    return text


def parse_cloudpss_table(table_data: List[Dict]) -> List[Dict]:
    """
    解析CloudPSS表格格式数据

    CloudPSS的表格格式为:
    {
        'type': 'table',
        'data': {
            'columns': [
                {'name': '<i>V</i><sub>m</sub> / pu', 'data': [...]},
                {'name': '<i>P</i><sub>G</sub> / MW', 'data': [...]}
            ]
        }
    }

    Args:
        table_data: CloudPSS返回的表格数据

    Returns:
        行导向的字典列表
    """
    if not table_data or len(table_data) == 0:
        return []

    table = table_data[0]
    if table.get('type') != 'table':
        return table_data

    columns = table['data']['columns']
    if not columns:
        return []

    # 获取行数
    num_rows = len(columns[0]['data']) if columns else 0

    # 转换为行导向
    rows = []
    for i in range(num_rows):
        row = {}
        for col in columns:
            col_name = parse_html_column_name(col['name'])
            row[col_name] = col['data'][i]
        rows.append(row)

    return rows


def get_time_index(time_array: List[float], target_time: float) -> int:
    """
    获取目标时间点在时间数组中的索引

    Args:
        time_array: 时间数组
        target_time: 目标时间

    Returns:
        最接近目标时间的索引
    """
    if not time_array:
        return 0

    # 找到最接近的索引
    idx = np.argmin(np.abs(np.array(time_array) - target_time))
    return int(idx)


def calculate_voltage_average(voltage_data: List[float], start_idx: int, end_idx: int) -> float:
    """
    计算电压平均值

    Args:
        voltage_data: 电压数据数组
        start_idx: 起始索引
        end_idx: 结束索引

    Returns:
        平均电压值
    """
    if end_idx <= start_idx or not voltage_data:
        logger.warning(f"无效的索引范围: start={start_idx}, end={end_idx}")
        return 0.0

    segment = voltage_data[start_idx:end_idx]
    return sum(segment) / len(segment) if segment else 0.0


def calculate_dv_metrics(
    voltage_data: List[float],
    time_data: List[float],
    disturbance_time: float = 4.0,
    pre_fault_window: float = 0.5,
    judge_criteria: List[List[float]] = None
) -> Dict[str, float]:
    """
    计算电压裕度指标 (DV - Deviation from Voltage)

    Args:
        voltage_data: 电压时序数据
        time_data: 时间数组
        disturbance_time: 扰动发生时间
        pre_fault_window: 故障前计算平均值的时间窗口
        judge_criteria: 电压裕度判断条件，格式为[[t_start, t_end, v_min_ratio, v_max_ratio], ...]

    Returns:
        {
            'dv_up': 电压上限裕度,
            'dv_down': 电压下限裕度,
            'v_steady': 稳态电压
        }
    """
    if judge_criteria is None:
        # 默认判断条件：[开始时间, 结束时间, 最小电压比例, 最大电压比例]
        judge_criteria = [[0.1, 3.0, 0.75, 1.25], [3.0, 999.0, 0.95, 1.05]]

    # 计算初始平均电压（故障前）
    ts = disturbance_time - pre_fault_window
    te = disturbance_time
    ms_v = get_time_index(time_data, ts)
    me_v = get_time_index(time_data, te)
    v_steady = calculate_voltage_average(voltage_data, ms_v, me_v)

    if v_steady == 0:
        logger.warning("稳态电压为0，无法计算DV")
        return {'dv_up': 0.0, 'dv_down': 0.0, 'v_steady': 0.0}

    # 初始化裕度为极大值
    dv_up = float('inf')
    dv_down = float('inf')

    end_time = time_data[-1] if time_data else disturbance_time + 10

    # 遍历判断条件计算裕度
    for j in judge_criteria:
        ts = min(disturbance_time + j[0], end_time)
        te = min(disturbance_time + j[1], end_time)

        ms_v = get_time_index(time_data, ts)
        me_v = get_time_index(time_data, te)

        voltage_segment = voltage_data[ms_v:me_v]
        if voltage_segment:
            v_max = max(voltage_segment)
            v_min = min(voltage_segment)

            # 电压上限裕度：j[3]*V_steady - V_max
            dv_up = min(dv_up, j[3] * v_steady - v_max)
            # 电压下限裕度：V_min - j[2]*V_steady
            dv_down = min(dv_down, v_min - j[2] * v_steady)

    return {
        'dv_up': dv_up if dv_up != float('inf') else 0.0,
        'dv_down': dv_down if dv_down != float('inf') else 0.0,
        'v_steady': v_steady
    }


def calculate_si_metric(
    voltage_data: List[float],
    time_data: List[float],
    disturbance_time: float = 4.0,
    pre_fault_window: float = 0.5,
    t_interval: float = 0.11,
    t_window: float = 3.0,
    dv1: float = 0.25,
    dv2: float = 0.1
) -> float:
    """
    计算故障严重度指标 (SI - Severity Index)

    Args:
        voltage_data: 电压时序数据
        time_data: 时间数组
        disturbance_time: 扰动发生时间
        pre_fault_window: 故障前计算平均值的时间窗口
        t_interval: 故障清除后开始计算的时间偏移
        t_window: 积分时间窗长度
        dv1: 第一阶段电压偏差阈值
        dv2: 第二阶段电压偏差阈值

    Returns:
        SI指标值
    """
    # 计算初始平均电压
    ts = disturbance_time - pre_fault_window
    te = disturbance_time
    ms_v = get_time_index(time_data, ts)
    me_v = get_time_index(time_data, te)
    v_steady = calculate_voltage_average(voltage_data, ms_v, me_v)

    if v_steady == 0:
        logger.warning("稳态电压为0，无法计算SI")
        return 0.0

    # 第一阶段：故障清除后短时间内的电压偏差
    ts = disturbance_time + t_interval
    te = disturbance_time + t_interval + t_window
    end_time = time_data[-1] if time_data else te
    te = min(te, end_time)

    ms_v = get_time_index(time_data, ts)
    me_v = get_time_index(time_data, te)

    v_threshold_lower = (1 - dv1) * v_steady
    v_threshold_upper = (1 + dv1) * v_steady

    segment_1 = voltage_data[ms_v:me_v]
    violation_count_1 = sum(
        1 for v in segment_1
        if v < v_threshold_lower or v > v_threshold_upper
    )
    si_1 = violation_count_1 / len(segment_1) if segment_1 else 0

    # 第二阶段：长时间恢复过程的电压偏差
    v_threshold_lower_2 = (1 - dv2) * v_steady
    v_threshold_upper_2 = (1 + dv2) * v_steady

    segment_2 = voltage_data[me_v:]
    violation_count_2 = sum(
        1 for v in segment_2
        if v < v_threshold_lower_2 or v > v_threshold_upper_2
    )
    si_2 = violation_count_2 / len(segment_2) if segment_2 else 0

    return si_1 + si_2


def extract_voltage_from_result(result, plot_index: int = 0) -> List[Dict]:
    """
    从EMT结果中提取电压数据

    Args:
        result: EMTResult对象
        plot_index: 电压量测图索引

    Returns:
        电压通道列表，每个通道包含name, x(时间), y(电压值)
    """
    try:
        plots = list(result.getPlots())
        if plot_index >= len(plots):
            logger.warning(f"Plot索引 {plot_index} 超出范围")
            return []

        plot = plots[plot_index]
        traces = plot.get('data', {}).get('traces', [])

        channels = []
        for trace in traces:
            channels.append({
                'name': trace.get('name', 'Unknown'),
                'x': trace.get('x', []),
                'y': trace.get('y', [])
            })

        return channels

    except Exception as e:
        logger.error(f"提取电压数据失败: {e}")
        return []


def clean_component_key(key: str) -> str:
    """
    清理组件key（移除前导斜杠）

    fetchTopology返回的key有前导斜杠（如/canvas_0_115），
    但removeComponent需要不带斜杠的key（如canvas_0_115）

    Args:
        key: 原始组件key

    Returns:
        清理后的key
    """
    return key.lstrip('/') if key else key
