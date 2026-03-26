# coding=UTF-8
"""
IEEE3 EMT 暂态仿真简化示例

本示例展示 IEEE3 模型的完整 EMT 仿真流程：
1. 从云端获取 IEEE3 模型
2. 运行 EMT 暂态仿真
3. 等待仿真完成
4. 提取波形数据（电压/电流）
5. 输出结果摘要

运行方式:
    python examples/simulation/ieee3_emt_simple.py

前置条件:
    - 有效的 .cloudpss_token 文件存在于项目根目录
    - 能够连接到 cloudpss.net
"""

import sys
import time
from pathlib import Path

from cloudpss import Model, setToken


DEFAULT_MODEL_RID = "model/holdme/IEEE3"


def load_token():
    """从项目根目录读取 CloudPSS API Token。"""
    token_path = Path(".cloudpss_token")
    if not token_path.exists():
        print("错误: 未找到 .cloudpss_token 文件")
        print("请先将 CloudPSS API token 写入项目根目录的 .cloudpss_token 文件")
        sys.exit(1)
    return token_path.read_text().strip()


def wait_for_completion(job, timeout=300, interval=3):
    """等待仿真任务完成。

    Args:
        job: Job 实例
        timeout: 超时时间（秒）
        interval: 状态检查间隔（秒）

    Returns:
        int: 最终状态码 (0: 运行中, 1: 已完成, 2: 失败, -1: 超时)
    """
    start_time = time.time()
    status_map = {0: "运行中", 1: "已完成", 2: "失败"}

    print("等待仿真完成...")
    while True:
        status = job.status()
        if status == 1:
            print("  状态: 已完成")
            return status
        if status == 2:
            print("  状态: 失败")
            return status

        elapsed = int(time.time() - start_time)
        print(f"  状态: {status_map.get(status, status)} ({elapsed}s)")
        if elapsed > timeout:
            print("  状态: 超时")
            return -1

        time.sleep(interval)


def describe_plot(plot, index):
    """获取波形分组的描述名称。"""
    return plot.get("key") or plot.get("name") or f"Plot {index}"


def run_ieee3_emt_simulation():
    """运行 IEEE3 EMT 暂态仿真并提取结果。"""
    print("=" * 60)
    print("IEEE3 EMT 暂态仿真示例")
    print("=" * 60)

    # 步骤 1: 认证
    print("\n步骤 1: 设置认证 Token")
    print("-" * 60)
    token = load_token()
    setToken(token)
    print("Token 已设置")

    # 步骤 2: 获取 IEEE3 模型
    print("\n步骤 2: 获取 IEEE3 模型")
    print("-" * 60)
    try:
        model = Model.fetch(DEFAULT_MODEL_RID)
        print(f"模型名称: {model.name}")
        print(f"模型 RID: {model.rid}")
        print(f"计算方案: {[job['rid'] for job in model.jobs]}")
    except Exception as e:
        print(f"获取模型失败: {e}")
        sys.exit(1)

    # 步骤 3: 检查 EMT 拓扑
    print("\n步骤 3: 检查 EMT 拓扑")
    print("-" * 60)
    try:
        topology = model.fetchTopology(implementType="emtp")
        topology_data = topology.toJSON()
        component_count = len(topology_data.get("components", {}))
        print(f"拓扑检查通过")
        print(f"  元件数量: {component_count}")
    except Exception as e:
        print(f"EMT 拓扑检查失败: {e}")
        print("请确认模型已正确配置 EMT 仿真参数")
        sys.exit(1)

    # 步骤 4: 运行 EMT 仿真
    print("\n步骤 4: 运行 EMT 仿真")
    print("-" * 60)
    try:
        job = model.runEMT()
        print(f"仿真任务已创建")
        print(f"  任务 ID: {job.id}")
    except Exception as e:
        print(f"创建仿真任务失败: {e}")
        print("可能原因:")
        print("  - 模型没有 EMT 计算方案")
        print("  - Token 权限不足")
        sys.exit(1)

    # 步骤 5: 等待仿真完成
    print("\n步骤 5: 等待仿真完成")
    print("-" * 60)
    final_status = wait_for_completion(job)
    if final_status != 1:
        print("仿真未成功完成，无法提取结果")
        sys.exit(1)

    # 步骤 6: 获取并输出结果摘要
    print("\n步骤 6: 提取仿真结果")
    print("-" * 60)
    try:
        result = job.result
        if result is None:
            print("结果为空")
            sys.exit(1)

        print(f"结果类型: {type(result).__name__}")

        # 获取波形分组
        plots = list(result.getPlots())
        print(f"\n波形分组数量: {len(plots)}")

        if not plots:
            print("未发现波形分组，请检查示波器和输出通道配置")
            sys.exit(1)

        # 显示每个波形分组的信息
        for i, plot in enumerate(plots):
            plot_name = describe_plot(plot, i)
            print(f"\n  波形分组 [{i}]: {plot_name}")

            # 获取该分组的通道名称
            channel_names = result.getPlotChannelNames(i)
            if channel_names:
                print(f"    通道数量: {len(channel_names)}")
                print(f"    通道列表: {', '.join(channel_names[:5])}")
                if len(channel_names) > 5:
                    print(f"      ... 等共 {len(channel_names)} 个通道")

                # 获取第一个通道的数据作为示例
                first_channel = channel_names[0]
                channel_data = result.getPlotChannelData(i, first_channel)
                if channel_data:
                    x_data = channel_data.get('x', [])
                    y_data = channel_data.get('y', [])
                    print(f"    首个通道 '{first_channel}' 数据点数: {len(x_data)}")
                    if x_data and y_data:
                        print(f"    时间范围: {x_data[0]:.6f}s ~ {x_data[-1]:.6f}s")
                        print(f"    数据范围: {min(y_data):.6f} ~ {max(y_data):.6f}")

        print("\n" + "=" * 60)
        print("仿真成功完成!")
        print("=" * 60)
        print(f"\n结果摘要:")
        print(f"  - 模型: {model.name}")
        print(f"  - 任务 ID: {job.id}")
        print(f"  - 波形分组数: {len(plots)}")
        print(f"  - 状态: 已完成")

        return result

    except Exception as e:
        print(f"提取结果失败: {e}")
        sys.exit(1)


def main():
    """主函数 - 运行 IEEE3 EMT 仿真流程。"""
    try:
        run_ieee3_emt_simulation()
    except KeyboardInterrupt:
        print("\n\n用户中断执行")
        sys.exit(0)


if __name__ == "__main__":
    main()
