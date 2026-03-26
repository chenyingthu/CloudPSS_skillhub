"""
CloudPSS SFEMT (Shift-Frequency Electromagnetic Transient) Simulation Example

运行方式: python examples/simulation/run_sfemt_simulation.py
前置条件: 有效的CloudPSS token保存在 .cloudpss_token

本示例演示如何运行移频电磁暂态仿真。
"""

from cloudpss import Model, setToken, Job
import sys
import time


def load_token():
    """从文件加载 API token"""
    try:
        with open('.cloudpss_token', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("错误: 未找到 .cloudpss_token 文件")
        print("请将 CloudPSS API token 保存到项目根目录的 .cloudpss_token 文件中")
        sys.exit(1)


def describe_plot(plot, index):
    """优先使用更稳定的 key，再回退到可选的 name。"""
    return plot.get("key") or plot.get("name") or f"Plot {index}"


def wait_for_completion(job, timeout=300, interval=2):
    """等待任务完成

    Args:
        job: Job 实例
        timeout: 超时时间（秒）
        interval: 轮询间隔（秒）

    Returns:
        最终状态: 0=运行中, 1=完成, 2=失败
    """
    start_time = time.time()

    while True:
        status = job.status()

        if status == 1:  # 完成
            print("  状态: 完成")
            return status
        elif status == 2:  # 失败
            print("  状态: 失败")
            return status
        else:  # 运行中
            elapsed = int(time.time() - start_time)
            print(f"  状态: 运行中 ({elapsed}s)...")
            if elapsed > timeout:
                print("  状态: 超时")
                return -1

        time.sleep(interval)


def example_run_sfemt(model):
    """运行 SFEMT 仿真示例"""
    print("\n=== 运行 SFEMT 仿真 ===")

    try:
        # 运行移频电磁暂态仿真
        print("启动 SFEMT 仿真...")
        job = model.runSFEMT()

        print(f"任务 ID: {job.id}")

        # 等待完成
        status = wait_for_completion(job)

        if status == 1:
            print("\nSFEMT 仿真成功完成!")

            # 获取结果
            result = job.result

            # 获取绘图数据
            plots = list(result.getPlots())
            print(f"结果曲线数量: {len(plots)}")

            if plots:
                print("\n曲线列表:")
                for i, plot in enumerate(plots):
                    print(f"  [{i}] {describe_plot(plot, i)}")

            return result

        elif status == 2:
            print("\nSFEMT 仿真失败")

            # 尝试获取错误信息
            try:
                messages = job.result.getMessagesByKey('error') if hasattr(job, 'result') else []
                if messages:
                    print(f"错误信息: {messages}")
            except:
                pass

            return None

    except Exception as e:
        print(f"运行 SFEMT 失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def example_run_sfemt_with_config(model):
    """使用指定配置运行 SFEMT 仿真"""
    print("\n=== 使用指定配置运行 SFEMT ===")

    try:
        # 获取模型中的计算方案
        print("模型计算方案:")
        for job_def in model.jobs:
            print(f"  - {job_def.get('name')}: {job_def.get('rid')}")

        # 获取模型中的参数方案
        print("模型参数方案:")
        for config in model.configs:
            print(f"  - {config.get('name')}")

        # 使用指定配置运行 (需要根据实际方案名称调整)
        # job = model.runSFEMT(
        #     job={'name': 'SFEMT Simulation'},
        #     config={'name': 'Default Config'},
        #     name='My SFEMT Task'
        # )

        print("\n提示: 如需指定配置，请修改代码中的 job 和 config 参数")

    except Exception as e:
        print(f"获取配置失败: {e}")


def analyze_sfemt_result(result):
    """分析 SFEMT 结果"""
    print("\n=== 分析 SFEMT 结果 ===")

    if not result:
        return

    try:
        # 获取所有绘图
        plots = list(result.getPlots())
        print(f"绘图数量: {len(plots)}")

        # 分析每个绘图
        for i, plot in enumerate(plots):
            print(f"\n绘图 [{i}]: {describe_plot(plot, i)}")

            # 获取通道名称
            try:
                channel_names = result.getPlotChannelNames(i)
                print(f"  通道数: {len(channel_names)}")
                print(f"  通道名称: {channel_names[:5]}...")  # 显示前5个
            except Exception as e:
                print(f"  获取通道名称失败: {e}")

            # 获取通道数据 (示例: 第一个通道)
            if channel_names:
                try:
                    data = result.getPlotChannelData(i, channel_names[0])
                    if data:
                        print(f"  数据点数: {len(data.get('y', []))}")
                        print(
                            f"  数据范围: [{min(data.get('y', [0])):.4f}, {max(data.get('y', [0])):.4f}]"
                        )
                except Exception as e:
                    print(f"  获取通道数据失败: {e}")

    except Exception as e:
        print(f"分析结果失败: {e}")


def main():
    """主函数"""
    print("CloudPSS SFEMT 仿真示例")
    print("=" * 50)

    # 加载 token 并设置
    token = load_token()
    setToken(token)
    print("Token 已设置")

    # 获取模型
    model_id = input("请输入模型 ID: ").strip()
    if not model_id:
        print("未提供模型 ID，退出。此示例不会再使用不可验证的默认模型。")
        return

    print(f"获取模型: {model_id}")
    try:
        model = Model.fetch(model_id)
        print(f"模型名称: {model.name}")
    except Exception as e:
        print(f"获取模型失败: {e}")
        return

    # 检查模型是否支持 SFEMT
    has_sfemt = False
    if hasattr(model, 'jobs'):
        for job in model.jobs:
            if job.get('rid') == 'function/CloudPSS/sfemt':
                has_sfemt = True
                break

    if not has_sfemt:
        print("警告: 未在 model.jobs 中发现 function/CloudPSS/sfemt")
        print("按 SDK 4.5.28 源码，这通常意味着默认 model.runSFEMT() 会失败。")
        print("尝试运行...")

    # 运行 SFEMT 仿真
    result = example_run_sfemt(model)

    # 分析结果
    if result:
        analyze_sfemt_result(result)

    print("\nSFEMT 仿真示例完成!")


if __name__ == "__main__":
    main()
