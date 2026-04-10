#!/usr/bin/env python3
"""
完整真实测试剩余6个技能 (Integration Tests)
Requires valid CloudPSS token to run.
测试目标：n1_security, topology_check, batch_powerflow, ieee3_prep, result_compare, param_scan
"""

import pytest
import sys
import time
import os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss import Model, Job, setToken
from cloudpss_skills import builtin
from cloudpss_skills.core import get_skill

RESULTS_DIR = "/home/chenying/researches/cloudpss-api-enhanced/test_results/real_output"
os.makedirs(RESULTS_DIR, exist_ok=True)


def log_step(step_num, title):
    print("\n" + "=" * 70)
    print(f"步骤{step_num}: {title}")
    print("=" * 70)


@pytest.mark.integration
def test_n1_security_real():
    """真实测试N-1安全校核"""
    log_step(1, "N-1安全校核 (n1_security)")

    skill = get_skill("n1_security")
    config = skill.get_default_config()

    # 修改输出路径
    config["output"]["path"] = RESULTS_DIR

    print("配置:")
    print(f"  模型: {config['model']['rid']}")
    print(f"  检查项: 电压、热稳定")
    print(f"  输出: {config['output']['path']}")

    print("\n执行N-1校核...")
    start = time.time()
    result = skill.run(config)
    elapsed = time.time() - start

    print(f"\n执行时间: {elapsed:.1f}秒")
    print(f"状态: {result.status.value}")

    if result.status.value == "success":
        data = result.data
        print(f"\n结果:")
        print(f"  总支路: {data['summary']['total_branches']}")
        print(f"  通过: {data['summary']['passed']}")
        print(f"  失败: {data['summary']['failed']}")
        print(f"  通过率: {data['summary']['pass_rate'] * 100:.1f}%")

        if result.artifacts:
            for art in result.artifacts:
                print(f"\n  生成文件: {art.path}")
                print(f"    大小: {art.size} bytes")

        return True
    else:
        print(f"✗ 失败: {result.error}")
        return False


@pytest.mark.integration
def test_topology_check_real():
    """真实测试拓扑检查"""
    log_step(2, "拓扑检查 (topology_check)")

    skill = get_skill("topology_check")
    config = skill.get_default_config()
    config["output"]["path"] = RESULTS_DIR

    print("配置:")
    print(f"  模型: {config['model']['rid']}")
    print(f"  检查: 孤岛、悬空元件、参数完整性")

    print("\n执行拓扑检查...")
    result = skill.run(config)

    print(f"状态: {result.status.value}")

    if result.status.value == "success":
        data = result.data
        print(f"\n结果:")
        print(f"  总元件: {data['summary']['total_components']}")
        print(f"  通过: {data['summary']['passed']}")
        print(f"  警告: {data['summary']['warnings']}")
        print(f"  问题: {data['summary']['issues']}")

        # 显示详细检查结果
        for detail in data["details"]:
            print(f"\n  [{detail['check']}] {detail['status']}: {detail['message']}")

        if result.artifacts:
            for art in result.artifacts:
                print(f"\n  生成文件: {art.path}")

        return True
    else:
        print(f"✗ 失败: {result.error}")
        return False


@pytest.mark.integration
def test_batch_powerflow_real():
    """真实测试批量潮流计算"""
    log_step(3, "批量潮流计算 (batch_powerflow)")

    skill = get_skill("batch_powerflow")
    config = skill.get_default_config()
    config["output"]["path"] = RESULTS_DIR

    # 添加IEEE39模型进行批量测试
    config["models"] = [
        {"rid": "model/holdme/IEEE3", "name": "IEEE3", "source": "cloud"},
        {"rid": "model/holdme/IEEE39", "name": "IEEE39", "source": "cloud"},
    ]

    print("配置:")
    print(f"  模型数量: {len(config['models'])}")
    for m in config["models"]:
        print(f"    - {m['name']}: {m['rid']}")

    print("\n执行批量潮流...")
    start = time.time()
    result = skill.run(config)
    elapsed = time.time() - start

    print(f"\n执行时间: {elapsed:.1f}秒")
    print(f"状态: {result.status.value}")

    if result.status.value == "success":
        data = result.data
        print(f"\n结果:")
        print(f"  总模型: {data['summary']['total']}")
        print(f"  收敛: {data['summary']['converged']}")
        print(f"  失败: {data['summary']['failed']}")
        print(f"  成功率: {data['summary']['success_rate'] * 100:.1f}%")

        # 显示每个模型的结果
        print(f"\n  详细结果:")
        for r in data["results"]:
            status = "✓" if r.get("converged") else "✗"
            print(
                f"    {status} {r['model_name']}: {r['status']} (Job: {r.get('job_id', 'N/A')[:8]}...)"
            )

        if result.artifacts:
            for art in result.artifacts:
                print(f"\n  生成文件: {art.path}")

        return True
    else:
        print(f"✗ 失败: {result.error}")
        return False


@pytest.mark.integration
def test_ieee3_prep_real():
    """真实测试IEEE3模型准备"""
    log_step(4, "IEEE3模型准备 (ieee3_prep)")

    skill = get_skill("ieee3_prep")
    config = skill.get_default_config()
    config["output"]["path"] = RESULTS_DIR

    print("配置:")
    print(f"  模型: {config['model']['rid']}")
    print(
        f"  故障时间: {config['fault']['start_time']}s - {config['fault']['end_time']}s"
    )
    print(f"  采样频率: {config['output']['sampling_freq']}Hz")

    print("\n执行模型准备...")
    result = skill.run(config)

    print(f"状态: {result.status.value}")

    if result.status.value == "success":
        data = result.data
        print(f"\n结果:")
        print(f"  模型: {data['model_name']}")
        print(f"  RID: {data['model_rid']}")
        print(f"  输出: {data['output_path']}")

        if result.artifacts:
            for art in result.artifacts:
                print(f"\n  生成文件: {art.path}")
                print(f"    大小: {art.size} bytes")

        # 验证文件存在
        if os.path.exists(data["output_path"]):
            print(f"\n  ✓ 文件验证: 存在")
        else:
            print(f"\n  ✗ 文件验证: 不存在")

        return True
    else:
        print(f"✗ 失败: {result.error}")
        return False


@pytest.mark.integration
def test_result_compare_real(job_ids):
    """真实测试结果对比"""
    log_step(5, "结果对比 (result_compare)")

    skill = get_skill("result_compare")

    config = {
        "skill": "result_compare",
        "auth": {"token_file": ".cloudpss_token"},
        "sources": [
            {"job_id": job_ids[0], "label": "IEEE3_EMT"},
            {"job_id": job_ids[1], "label": "IEEE39_PF"},
        ],
        "compare": {
            "channels": [],  # 所有通道
            "metrics": ["max", "min", "mean"],
        },
        "output": {
            "format": "markdown",
            "path": RESULTS_DIR,
            "filename": "comparison_report",
            "timestamp": True,
        },
    }

    print("配置:")
    print(f"  对比任务: {len(config['sources'])}")
    for s in config["sources"]:
        print(f"    - {s['label']}: {s['job_id']}")

    print("\n执行结果对比...")
    result = skill.run(config)

    print(f"状态: {result.status.value}")

    if result.status.value == "success":
        data = result.data
        print(f"\n结果:")
        print(f"  对比通道数: {data['compared_channels']}")

        if result.artifacts:
            for art in result.artifacts:
                print(f"\n  生成文件: {art.path}")
                print(f"    大小: {art.size} bytes")
                # 显示报告内容预览
                if art.path.endswith(".md"):
                    with open(art.path, "r") as f:
                        content = f.read()
                        print(f"\n  报告预览 (前500字符):")
                        print(content[:500])

        return True
    else:
        print(f"✗ 失败: {result.error}")
        return False


@pytest.mark.integration
def test_param_scan_real():
    """真实测试参数扫描"""
    log_step(6, "参数扫描 (param_scan)")

    # 首先查询IEEE3模型的元件
    print("1. 查询模型元件...")
    token = (
        Path("/home/chenying/researches/cloudpss-api-enhanced/.cloudpss_token")
        .read_text()
        .strip()
    )
    setToken(token)

    model = Model.fetch("model/holdme/IEEE3")
    components = model.getAllComponents()

    print(f"  找到 {len(components)} 个元件")

    # 查找Load或Generator元件
    target_comp = None
    for comp_id, comp in components.items():
        definition = getattr(comp, "definition", "")
        name = getattr(comp, "name", comp_id)
        if "load" in definition.lower() or "load" in name.lower():
            target_comp = comp
            print(f"  ✓ 找到Load元件: {comp_id} ({name})")
            break
        elif "generator" in definition.lower() or "gen" in name.lower():
            target_comp = comp
            print(f"  ✓ 找到Generator元件: {comp_id} ({name})")
            break

    if not target_comp:
        # 使用第一个元件进行测试
        target_comp = list(components.values())[0]
        print(f"  ⚠ 使用第一个可用元件: {target_comp.id}")

    # 查看元件参数
    args = getattr(target_comp, "args", {})
    print(f"\n2. 元件参数:")
    for key in list(args.keys())[:5]:
        print(f"    - {key}: {args[key]}")

    # 使用第一个数值参数进行扫描
    param_name = None
    for key, val in args.items():
        try:
            float(val.get("source", 0))
            param_name = key
            base_value = float(val.get("source", 0))
            break
        except:
            continue

    if not param_name:
        param_name = "P"
        base_value = 100.0

    print(f"\n3. 扫描参数: {param_name}")
    print(f"   基准值: {base_value}")
    print(
        f"   扫描值: {[base_value * 0.8, base_value * 0.9, base_value, base_value * 1.1, base_value * 1.2]}"
    )

    # 执行参数扫描
    skill = get_skill("param_scan")
    config = {
        "skill": "param_scan",
        "auth": {"token_file": ".cloudpss_token"},
        "model": {"rid": "model/holdme/IEEE3", "source": "cloud"},
        "scan": {
            "component": target_comp.id,
            "parameter": param_name,
            "values": [
                base_value * 0.8,
                base_value * 0.9,
                base_value,
                base_value * 1.1,
                base_value * 1.2,
            ],
            "simulation_type": "power_flow",
        },
        "output": {
            "format": "json",
            "path": RESULTS_DIR,
            "prefix": "param_scan",
            "timestamp": True,
        },
    }

    print("\n4. 执行参数扫描...")
    start = time.time()
    result = skill.run(config)
    elapsed = time.time() - start

    print(f"\n执行时间: {elapsed:.1f}秒")
    print(f"状态: {result.status.value}")

    if result.status.value == "success":
        data = result.data
        print(f"\n结果:")
        print(f"  总扫描次数: {data['summary']['total']}")
        print(f"  成功: {data['summary']['success']}")
        print(f"  失败: {data['summary']['failed']}")

        # 显示每次扫描结果
        print(f"\n  扫描结果:")
        for r in data["results"]:
            status = "✓" if r["status"] == "success" else "✗"
            print(f"    {status} {param_name}={r['value']:.2f}: {r['status']}")

        if result.artifacts:
            for art in result.artifacts:
                print(f"\n  生成文件: {art.path}")

        return True
    else:
        print(f"✗ 失败: {result.error}")
        return False


def main():
    print("=" * 70)
    print("完整真实测试 - 剩余6个技能")
    print(f"开始时间: {datetime.now()}")
    print("=" * 70)

    results = {}
    job_ids = []

    # 测试1: N-1安全校核
    results["n1_security"] = test_n1_security_real()

    # 测试2: 拓扑检查
    results["topology_check"] = test_topology_check_real()

    # 测试3: 批量潮流计算
    results["batch_powerflow"] = test_batch_powerflow_real()

    # 获取一个Job ID用于后续测试
    print("\n" + "=" * 70)
    print("获取Job IDs用于result_compare测试...")
    print("=" * 70)

    token = (
        Path("/home/chenying/researches/cloudpss-api-enhanced/.cloudpss_token")
        .read_text()
        .strip()
    )
    setToken(token)

    # 运行IEEE3 EMT获取Job ID
    print("运行IEEE3 EMT...")
    model = Model.fetch("model/holdme/IEEE3")
    job = model.runEMT()
    time.sleep(10)  # 等待完成
    if job.status() == 1:
        job_ids.append(job.id)
        print(f"  ✓ EMT Job: {job.id}")

    # 运行IEEE39潮流获取Job ID
    print("运行IEEE39潮流...")
    model = Model.fetch("model/holdme/IEEE39")
    job = model.runPowerFlow()
    time.sleep(10)
    if job.status() == 1:
        job_ids.append(job.id)
        print(f"  ✓ PF Job: {job.id}")

    # 测试4: IEEE3模型准备
    results["ieee3_prep"] = test_ieee3_prep_real()

    # 测试5: 结果对比（如果有2个Job ID）
    if len(job_ids) >= 2:
        results["result_compare"] = test_result_compare_real(job_ids)
    else:
        print("\n  ⚠ Job ID不足，跳过result_compare测试")
        results["result_compare"] = False

    # 测试6: 参数扫描
    results["param_scan"] = test_param_scan_real()

    # 最终汇总
    print("\n" + "=" * 70)
    print("完整真实测试总结")
    print("=" * 70)

    for skill_name, ok in results.items():
        status = "✅ 通过" if ok else "❌ 失败"
        print(f"  {skill_name}: {status}")

    passed = sum(results.values())
    total = len(results)
    print(f"\n总计: {passed}/{total} 通过 ({passed / total * 100:.1f}%)")

    if passed == total:
        print("\n🎉 所有技能完全真实测试通过！")
    else:
        print(f"\n⚠️ {total - passed} 个技能测试失败")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
