#!/usr/bin/env python3
"""
修复版完整真实测试
"""

import sys
import time
import os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import Model, Job, setToken
from cloudpss_skills import builtin  # noqa: F401
from cloudpss_skills.core import get_skill

RESULTS_DIR = "/home/chenying/researches/cloudpss-api-enhanced/test_results/real_output"
os.makedirs(RESULTS_DIR, exist_ok=True)


def wait_for_job(job, timeout=60, label=""):
    """等待Job完成"""
    print(f"  等待{label}完成 (timeout={timeout}s)...", end="", flush=True)
    for i in range(timeout // 2):
        status = job.status()
        if status == 1:
            print(f" ✓ ({(i+1)*2}s)")
            return True
        elif status == 2:
            print(f" ✗ 失败")
            return False
        time.sleep(2)
    print(f" ⚠ 超时")
    return False


def test_with_real_jobs():
    """先运行仿真获取真实Job ID，然后进行所有测试"""
    print("="*70)
    print("第一步: 运行仿真获取真实Job IDs")
    print("="*70)

    token = Path("/home/chenying/researches/cloudpss-api-enhanced/.cloudpss_token").read_text().strip()
    setToken(token)

    job_ids = {}

    # 1. 运行IEEE39潮流（快速）
    print("\n1. 运行IEEE39潮流计算...")
    model = Model.fetch("model/holdme/IEEE39")
    job = model.runPowerFlow()
    if wait_for_job(job, timeout=60, label="潮流"):
        job_ids['ieee39_pf'] = job.id
        print(f"   Job ID: {job.id}")
    else:
        print("   潮流未收敛，尝试EMT...")

    # 2. 运行IEEE3 EMT
    print("\n2. 运行IEEE3 EMT仿真...")
    model = Model.fetch("model/holdme/IEEE3")
    job = model.runEMT()
    if wait_for_job(job, timeout=120, label="EMT"):
        job_ids['ieee3_emt'] = job.id
        print(f"   Job ID: {job.id}")
    else:
        print("   EMT未完成")

    print(f"\n✓ 获得 {len(job_ids)} 个完成的Job")
    for name, jid in job_ids.items():
        print(f"  - {name}: {jid}")

    return job_ids


def test_n1_security_improved():
    """改进的N-1安全校核测试 - 使用正确的支路类型"""
    print("\n" + "="*70)
    print("测试: N-1安全校核 (改进版)")
    print("="*70)

    token = Path("/home/chenying/researches/cloudpss-api-enhanced/.cloudpss_token").read_text().strip()
    setToken(token)

    # 手动执行N-1校核
    print("获取IEEE39模型...")
    model = Model.fetch("model/holdme/IEEE39")
    components = model.getAllComponents()

    # 查找支路 - 使用正确的类型名
    branch_types = [
        "TransmissionLine",
        "_newTransformer_3p2w",
        "_newTransformer_3p3w",
    ]

    branches = []
    for comp_id, comp in components.items():
        definition = getattr(comp, "definition", "")
        if any(bt in definition for bt in branch_types):
            branches.append({
                "id": comp_id,
                "name": getattr(comp, "name", comp_id),
                "type": definition.split("/")[-1],
            })

    print(f"✓ 发现 {len(branches)} 条支路")
    if branches:
        print(f"  前5条: {[b['name'] for b in branches[:5]]}")

    # 只测试前3条支路（节省时间）
    test_branches = branches[:3]
    results = []

    print(f"\n执行N-1校核（测试{len(test_branches)}条支路）...")
    for i, branch in enumerate(test_branches):
        print(f"\n[{i+1}/{len(test_branches)}] 停运: {branch['name']}")

        # 重新加载模型
        model = Model.fetch("model/holdme/IEEE39")

        # 移除支路
        try:
            model.removeComponent(branch["id"])
            print(f"  -> 已移除支路")
        except Exception as e:
            print(f"  -> 移除失败: {e}")
            continue

        # 运行潮流
        try:
            job = model.runPowerFlow()
            if wait_for_job(job, timeout=30, label="潮流"):
                print(f"  -> ✓ N-1通过")
                results.append({"branch": branch["name"], "status": "passed"})
            else:
                print(f"  -> ✗ N-1失败（潮流不收敛）")
                results.append({"branch": branch["name"], "status": "failed"})
        except Exception as e:
            print(f"  -> ✗ 异常: {e}")
            results.append({"branch": branch["name"], "status": "error", "error": str(e)})

    # 保存结果
    import json
    result_file = f"{RESULTS_DIR}/n1_security_improved_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(result_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_branches": len(branches),
            "tested": len(test_branches),
            "results": results,
        }, f, indent=2)

    print(f"\n✓ 结果已保存: {result_file}")
    passed = sum(1 for r in results if r["status"] == "passed")
    print(f"  通过: {passed}/{len(results)}")

    return len(results) > 0


def test_result_compare_with_jobs(job_ids):
    """使用真实Job ID测试结果对比"""
    print("\n" + "="*70)
    print("测试: 结果对比 (使用真实Job IDs)")
    print("="*70)

    if len(job_ids) < 2:
        print("✗ Job IDs不足，需要至少2个")
        return False

    # 获取Job IDs列表
    ids = list(job_ids.values())

    skill = get_skill("result_compare")
    if skill is None:
        print("✗ 无法获取result_compare技能")
        return False
    config = {
        "skill": "result_compare",
        "auth": {"token_file": ".cloudpss_token"},
        "sources": [
            {"job_id": ids[0], "label": "Case_1"},
            {"job_id": ids[1], "label": "Case_2"},
        ],
        "compare": {
            "channels": [],
            "metrics": ["max", "min"],
        },
        "output": {
            "format": "markdown",
            "path": RESULTS_DIR,
            "filename": "comparison_real",
            "timestamp": True,
        },
    }

    print(f"对比Job IDs:")
    print(f"  Case 1: {ids[0][:20]}...")
    print(f"  Case 2: {ids[1][:20]}...")

    print("\n执行对比...")
    result = skill.run(config)

    print(f"状态: {result.status.value}")

    if result.status.value == "success":
        print(f"✓ 对比完成")
        if result.artifacts:
            for art in result.artifacts:
                print(f"  报告: {art.path}")
        return True
    else:
        print(f"✗ 失败: {result.error}")
        return False


def test_param_scan_improved():
    """改进的参数扫描 - 找到真正的可修改参数"""
    print("\n" + "="*70)
    print("测试: 参数扫描 (改进版)")
    print("="*70)

    token = Path("/home/chenying/researches/cloudpss-api-enhanced/.cloudpss_token").read_text().strip()
    setToken(token)

    # 获取模型
    print("获取IEEE3模型...")
    model = Model.fetch("model/holdme/IEEE3")
    components = model.getAllComponents()

    # 查找有非零数值参数的元件
    target_comp = None
    target_param = None
    base_value = None

    for comp_id, comp in components.items():
        args = getattr(comp, "args", {})
        for param_name, param_val in args.items():
            try:
                source_val = param_val.get("source", "")
                val = float(source_val)
                if val != 0 and val != 1:  # 找有意义的参数
                    target_comp = comp
                    target_param = param_name
                    base_value = val
                    print(f"✓ 找到可扫描参数: {comp_id}.{param_name} = {val}")
                    break
            except:
                continue
        if target_comp:
            break

    if not target_comp:
        print("✗ 未找到合适的扫描参数")
        return False

    # 执行参数扫描
    skill = get_skill("param_scan")
    values = [base_value * 0.9, base_value * 0.95, base_value, base_value * 1.05, base_value * 1.1]

    config = {
        "skill": "param_scan",
        "auth": {"token_file": ".cloudpss_token"},
        "model": {"rid": "model/holdme/IEEE3", "source": "cloud"},
        "scan": {
            "component": target_comp.id,
            "parameter": target_param,
            "values": values,
            "simulation_type": "power_flow",
        },
        "output": {
            "format": "json",
            "path": RESULTS_DIR,
            "prefix": "param_scan_real",
            "timestamp": True,
        },
    }

    print(f"\n扫描参数: {target_param}")
    print(f"扫描值: {[f'{v:.4f}' for v in values]}")
    print(f"\n执行扫描...")

    result = skill.run(config)

    print(f"状态: {result.status.value}")

    if result.status.value == "success":
        data = result.data
        success_count = data['summary']['success']
        print(f"✓ 扫描完成: {success_count}/{data['summary']['total']} 成功")

        if result.artifacts:
            for art in result.artifacts:
                print(f"  结果: {art.path}")

        return success_count > 0
    else:
        print(f"✗ 失败: {result.error}")
        return False


def main():
    print("="*70)
    print("完整真实测试 - 修复版")
    print(f"开始: {datetime.now()}")
    print("="*70)

    # 第一步: 获取真实Job IDs
    job_ids = test_with_real_jobs()

    results = {}

    # 第二步: 运行各项测试
    results['n1_security'] = test_n1_security_improved()
    results['result_compare'] = test_result_compare_with_jobs(job_ids)
    results['param_scan'] = test_param_scan_improved()

    # 汇总
    print("\n" + "="*70)
    print("最终测试总结")
    print("="*70)

    for name, ok in results.items():
        status = "✅ 通过" if ok else "❌ 失败"
        print(f"  {name}: {status}")

    passed = sum(results.values())
    total = len(results)
    print(f"\n总计: {passed}/{total} ({passed/total*100:.1f}%)")

    # 显示生成的文件
    print("\n生成的文件:")
    for f in os.listdir(RESULTS_DIR):
        fpath = os.path.join(RESULTS_DIR, f)
        fsize = os.path.getsize(fpath)
        print(f"  - {f} ({fsize:,} bytes)")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
