"""
CloudPSS IES (Integrated Energy System) Simulation Example

运行方式: python examples/simulation/run_ies_simulation.py
前置条件: 有效的CloudPSS token保存在 .cloudpss_token

本示例演示如何运行综合能源系统仿真。
"""

from cloudpss import Model, setToken
import sys
import time


SUPPORTED_IES_RUNNERS = (
    {
        "rid": "job-definition/ies/ies-power-flow",
        "label": "IES 时序潮流",
        "method": "runIESPowerFlow",
    },
    {
        "rid": "job-definition/ies/ies-load-prediction",
        "label": "IES 负荷预测",
        "method": "runIESLoadPrediction",
    },
    {
        "rid": "job-definition/ies/ies-energy-storage-plan",
        "label": "IES 储能规划",
        "method": "runIESEnergyStoragePlan",
    },
)

LEGACY_IES_JOB_RIDS = {
    "function/CloudPSS/ies-power-flow": "job-definition/ies/ies-power-flow",
    "function/CloudPSS/ies-load-prediction": "job-definition/ies/ies-load-prediction",
    "function/CloudPSS/ies-energy-storage-plan": "job-definition/ies/ies-energy-storage-plan",
}

SUPPORTED_IES_JOB_RIDS = {runner["rid"] for runner in SUPPORTED_IES_RUNNERS}


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


def wait_for_completion(job, timeout=600, interval=3):
    """等待任务完成"""
    start_time = time.time()

    while True:
        status = job.status()

        if status == 1:
            print("  状态: 完成")
            return status
        elif status == 2:
            print("  状态: 失败")
            return status
        else:
            elapsed = int(time.time() - start_time)
            print(f"  状态: 运行中 ({elapsed}s)...")
            if elapsed > timeout:
                print("  状态: 超时")
                return -1

        time.sleep(interval)


def example_get_ies_jobs(model):
    """查看当前模型里可被 SDK 4.5.28 `runIES*()` 默认识别的计算方案。"""
    print("\n=== 可用的 IES 计算方案 ===")

    if not hasattr(model, 'jobs'):
        print("模型无可用计算方案")
        return []

    ies_jobs = []
    legacy_jobs = []
    for job in model.jobs:
        rid = job.get('rid', '')
        if rid in SUPPORTED_IES_JOB_RIDS:
            ies_jobs.append(job)
            print(f"  - {job.get('name')}: {rid}")
        elif rid in LEGACY_IES_JOB_RIDS:
            legacy_jobs.append(job)

    if legacy_jobs:
        print("\n检测到旧样式 IES 条目:")
        for job in legacy_jobs:
            rid = job.get("rid", "")
            expected = LEGACY_IES_JOB_RIDS[rid]
            print(f"  - {job.get('name')}: {rid} -> SDK 默认入口期待 {expected}")
        print("这些条目不会被当作当前示例已验证可运行的默认入口。")

    return ies_jobs


def example_run_ies_simulation(model):
    """运行 IES 仿真示例"""
    print("\n=== 运行 IES 仿真 ===")

    # 首先查看可用的 IES 方案
    ies_jobs = example_get_ies_jobs(model)

    if not ies_jobs:
        print("未找到与 SDK 4.5.28 `runIES*()` 默认入口一致的 IES 计算方案")
        return None

    print(f"找到 {len(ies_jobs)} 个 IES 计算方案")

    try:
        job = None
        for runner in SUPPORTED_IES_RUNNERS:
            if any(job_def.get("rid") == runner["rid"] for job_def in ies_jobs):
                print(f"\n运行 {runner['label']}...")
                job = getattr(model, runner["method"])()
                break

        if job is None:
            print("未找到与 SDK 4.5.28 `runIES*()` 默认入口一致的 IES 计算方案")
            return None

        print(f"任务 ID: {job.id}")
        status = wait_for_completion(job)
        if status == 1:
            print("IES 仿真成功!")
            return job.result
        return None

    except Exception as e:
        print(f"运行 IES 仿真失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def analyze_ies_result(result):
    """分析 IES 结果"""
    print("\n=== 分析 IES 结果 ===")

    if not result:
        return

    try:
        # 获取结果类型
        result_type = type(result).__name__
        print(f"结果类型: {result_type}")

        # `IESResult` 内部按 plot key 聚合结果，这里同样优先展示 key。
        plots = list(result.getPlots()) if hasattr(result, 'getPlots') else []
        print(f"绘图数量: {len(plots)}")

        if plots:
            print("\n绘图列表:")
            for i, plot in enumerate(plots):
                print(f"  [{i}] {describe_plot(plot, i)}")

        # 获取其他消息
        try:
            messages = result.getMessagesByKey('summary') if hasattr(result, 'getMessagesByKey') else []
            if messages:
                print(f"\n摘要消息: {messages[:3]}...")
        except:
            pass

    except Exception as e:
        print(f"分析结果失败: {e}")


def example_ies_optimization(model):
    """运行 IES 优化示例"""
    print("\n=== 运行 IES 优化 ===")

    # 查找优化类 job
    optimization_job = None
    if hasattr(model, 'jobs'):
        for job_def in model.jobs:
            if 'optimization' in job_def.get('rid', '').lower():
                optimization_job = job_def
                break

    if optimization_job:
        print(f"找到优化方案: {optimization_job.get('name')}")

        # 注意: 实际运行需要根据具体参数调整
        # job = model.run(job=optimization_job)
        # status = wait_for_completion(job)

    else:
        print("未找到 IES 优化方案")


def main():
    """主函数"""
    print("CloudPSS IES 综合能源系统仿真示例")
    print("=" * 50)

    # 加载 token 并设置
    token = load_token()
    setToken(token)
    print("Token 已设置")

    # 获取模型
    model_id = input("请输入 IES 模型 ID: ").strip()
    if not model_id:
        print("未提供模型 ID，退出。此示例不会再使用不可验证的默认模型。")
        return

    print(f"获取模型: {model_id}")
    try:
        model = Model.fetch(model_id)
        print(f"模型名称: {model.name}")
    except Exception as e:
        print(f"获取模型失败: {e}")
        print("\n提示: 请使用包含 IES 计算方案的模型")
        return

    # 运行 IES 仿真
    result = example_run_ies_simulation(model)

    # 分析结果
    if result:
        analyze_ies_result(result)

    # 运行优化 (可选)
    # example_ies_optimization(model)

    print("\nIES 仿真示例完成!")


if __name__ == "__main__":
    main()
