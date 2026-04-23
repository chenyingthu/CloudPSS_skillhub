#!/usr/bin/env python3
"""
完全真实的param_scan测试 (Integration Tests)
Requires valid CloudPSS token to run.
使用EMT仿真进行参数扫描
"""

import pytest
import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import Model, setToken
import json

RESULTS_DIR = "/home/chenying/researches/cloudpss-api-enhanced/test_results/real_output"


@pytest.mark.integration
def test_param_scan_emt():
    """使用EMT仿真进行参数扫描"""
    print("=" * 70)
    print("完全真实的param_scan测试（EMT模式）")
    print(f"时间: {datetime.now()}")
    print("=" * 70)

    # 加载token
    token = (
        Path(".cloudpss_token")
        .read_text()
        .strip()
    )
    setToken(token)

    # 获取IEEE3模型并查找可修改参数
    print("\n1. 查询模型元件...")
    model = Model.fetch("model/holdme/IEEE3")
    components = model.getAllComponents()

    # 查找Load元件
    target_comp = None
    target_param = None
    base_value = None

    for comp_id, comp in components.items():
        definition = getattr(comp, "definition", "")
        if "ExpLoad" in definition:
            args = getattr(comp, "args", {})
            if "p" in args:
                try:
                    base_value = float(args["p"].get("source", 0))
                    if base_value > 0:
                        target_comp = comp_id
                        target_param = "p"
                        print(f"✓ 找到Load元件: {comp_id}")
                        print(f"  参数: p = {base_value}")
                        break
                except:
                    pass

    assert target_comp, "未找到可用于 EMT 参数扫描的负荷元件"

    # 执行参数扫描
    print(f"\n2. 执行参数扫描...")
    print(f"   元件: {target_comp}")
    print(f"   参数: {target_param}")

    # 使用较小的变化范围
    values = [
        base_value * 0.95,
        base_value * 0.98,
        base_value,
        base_value * 1.02,
        base_value * 1.05,
    ]
    print(f"   扫描值: {[f'{v:.2f}' for v in values]}")
    print(f"   仿真类型: EMT")

    results = []

    for i, value in enumerate(values):
        print(f"\n   [{i + 1}/{len(values)}] {target_param} = {value:.2f}")

        # 重新加载模型
        model = Model.fetch("model/holdme/IEEE3")

        # 更新参数
        try:
            model.updateComponent(
                target_comp, args={target_param: {"source": str(value), "ɵexp": ""}}
            )
            print(f"      ✓ 已设置参数")
        except Exception as e:
            print(f"      ✗ 设置失败: {e}")
            results.append({"value": value, "status": "error", "error": str(e)})
            continue

        # 运行EMT仿真
        try:
            job = model.runEMT()
            print(f"      Job ID: {job.id}")
            print(f"      等待完成...", end="", flush=True)

            for j in range(60):
                status = job.status()
                if status == 1:
                    print(f" ✓ ({(j + 1) * 2}s)")
                    results.append(
                        {
                            "value": value,
                            "status": "success",
                            "job_id": job.id,
                            "converged": True,
                        }
                    )
                    break
                elif status == 2:
                    print(" ✗ 失败")
                    results.append(
                        {
                            "value": value,
                            "status": "failed",
                            "job_id": job.id,
                            "converged": False,
                        }
                    )
                    break
                time.sleep(2)
            else:
                print(" ⚠ 超时")
                results.append(
                    {
                        "value": value,
                        "status": "timeout",
                        "job_id": job.id,
                    }
                )

        except Exception as e:
            print(f"      ✗ 仿真异常: {e}")
            results.append({"value": value, "status": "error", "error": str(e)})

    # 汇总结果
    print("\n" + "=" * 70)
    print("参数扫描完成")
    print("=" * 70)

    success_count = sum(1 for r in results if r["status"] == "success")
    failed_count = sum(1 for r in results if r["status"] != "success")

    print(f"\n总扫描: {len(results)}")
    print(f"成功: {success_count}")
    print(f"失败: {failed_count}")

    print("\n详细结果:")
    for r in results:
        status = "✓" if r["status"] == "success" else "✗"
        job_info = f" (Job: {r.get('job_id', 'N/A')[:8]}...)" if r.get("job_id") else ""
        print(f"  {status} {target_param}={r['value']:.2f}: {r['status']}{job_info}")

    # 保存结果
    result_file = (
        f"{RESULTS_DIR}/param_scan_emt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(result_file, "w") as f:
        json.dump(
            {
                "timestamp": datetime.now().isoformat(),
                "component": target_comp,
                "parameter": target_param,
                "base_value": base_value,
                "values": values,
                "summary": {
                    "total": len(results),
                    "success": success_count,
                    "failed": failed_count,
                },
                "results": results,
            },
            f,
            indent=2,
        )

    print(f"\n✓ 结果已保存: {result_file}")

    assert success_count > 0, f"Expected at least 1 successful EMT scan, got {success_count}"


if __name__ == "__main__":
    success = test_param_scan_emt()
    sys.exit(0 if success else 1)
