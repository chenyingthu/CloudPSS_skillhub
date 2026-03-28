"""
扰动严重度分析示例

演示如何使用 disturbance_severity 技能分析故障后的电压恢复特性

前提：
    - 已有带故障的EMT仿真结果
    - 或运行此脚本前先运行emt_fault_study技能

使用方法:
    python examples/analysis/disturbance_severity_example.py
"""

import logging
from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cloudpss import Model
from cloudpss_skills.core import get_skill, ConfigLoader

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_with_config_file():
    """使用配置文件运行扰动严重度分析"""
    logger.info("=" * 60)
    logger.info("示例1: 使用配置文件运行")
    logger.info("=" * 60)

    # 加载配置
    config_path = Path("config/disturbance_severity.yaml")
    if not config_path.exists():
        logger.error(f"配置文件不存在: {config_path}")
        return False

    config = ConfigLoader.load(config_path)
    logger.info(f"加载配置: {config_path}")

    # 获取技能
    skill = get_skill("disturbance_severity")
    logger.info(f"获取技能: {skill.name}")

    # 运行分析
    logger.info("开始扰动严重度分析...")
    result = skill.run(config)

    if result.status.value == "success":
        logger.info("✓ 分析成功")
        logger.info(f"结果数据键: {list(result.data.keys())}")

        # 输出摘要
        summary = result.data.get("summary", {})
        logger.info(f"总通道数: {summary.get('total_channels', 0)}")
        logger.info(f"薄弱点数: {len(result.data.get('weak_points', []))}")

        # 输出前5个薄弱点
        weak_points = result.data.get("weak_points", [])
        if weak_points:
            logger.info("\n薄弱点Top 5:")
            for i, wp in enumerate(weak_points[:5], 1):
                logger.info(f"  {i}. {wp['name']}: {wp['reason']}")

        # 输出生成的文件
        for artifact in result.artifacts:
            logger.info(f"生成文件: {artifact.path}")

        return True
    else:
        logger.error(f"✗ 分析失败: {result.logs}")
        return False


def example_direct_api():
    """直接使用API运行（简化版，需要已有EMT结果）"""
    logger.info("\n" + "=" * 60)
    logger.info("示例2: 直接使用API (需要已有EMT结果)")
    logger.info("=" * 60)

    # 获取技能
    skill = get_skill("disturbance_severity")

    # 配置（简化版，实际需要emt_result）
    config = {
        "auth": {
            "token_file": ".cloudpss_token"
        },
        "model": {
            "rid": "model/holdme/IEEE39",
            "source": "cloud"
        },
        "simulation": {
            # "emt_result": "job_id_here",  # 需要提供已有EMT结果
            "fault_bus": "Bus_16",
            "fault_type": "three_phase",
            "fault_time": 4.0,
            "fault_duration": 0.1,
            "simulation_time": 10.0
        },
        "analysis": {
            "dv_enabled": True,
            "si_enabled": True,
            "voltage_measure_plot": 0,
            "judge_criteria": [
                [0.1, 3.0, 0.75, 1.25],
                [3.0, 999.0, 0.95, 1.05]
            ]
        },
        "output": {
            "format": "json",
            "path": "./results/",
            "prefix": "disturbance_severity_demo"
        }
    }

    # 注意：由于没有提供emt_result，此示例会失败
    # 实际使用时需要提供已有EMT仿真结果
    logger.info("注意: 此示例需要已有EMT仿真结果")
    logger.info("请先运行emt_fault_study技能获取EMT结果")

    return True


def example_batch_analysis():
    """批量扰动严重度分析示例"""
    logger.info("\n" + "=" * 60)
    logger.info("示例3: 批量分析多个故障场景")
    logger.info("=" * 60)

    # 定义多个故障场景
    fault_scenarios = [
        {"bus": "Bus_16", "type": "three_phase", "name": "Bus16三相短路"},
        {"bus": "Bus_15", "type": "three_phase", "name": "Bus15三相短路"},
        {"bus": "Bus_26", "type": "single_phase", "name": "Bus26单相接地"},
    ]

    logger.info(f"计划分析 {len(fault_scenarios)} 个故障场景:")
    for i, scenario in enumerate(fault_scenarios, 1):
        logger.info(f"  {i}. {scenario['name']}")

    logger.info("\n批量分析流程:")
    logger.info("  1. 对每个故障场景运行EMT仿真")
    logger.info("  2. 使用disturbance_severity技能分析每个结果")
    logger.info("  3. 汇总所有场景的DV/SI指标")
    logger.info("  4. 生成综合评估报告")

    logger.info("\n实际代码实现:")
    logger.info("""
    results = []
    for scenario in fault_scenarios:
        # 运行EMT仿真
        emt_result = run_emt_simulation(scenario)

        # 扰动严重度分析
        config['simulation']['emt_result'] = emt_result.job_id
        severity_result = skill.run(config)

        results.append({
            'scenario': scenario['name'],
            'dv_data': severity_result.data['channel_results'],
            'weak_points': severity_result.data['weak_points']
        })

    # 生成综合报告
    generate_comprehensive_report(results)
    """)

    return True


def main():
    """主函数"""
    logger.info("扰动严重度分析技能示例")
    logger.info("=" * 60)

    examples = [
        ("配置文件方式", example_with_config_file),
        ("直接API调用", example_direct_api),
        ("批量分析", example_batch_analysis),
    ]

    passed = 0
    for name, example_func in examples:
        try:
            if example_func():
                passed += 1
                logger.info(f"✓ {name} 完成")
            else:
                logger.error(f"✗ {name} 失败")
        except Exception as e:
            logger.error(f"✗ {name} 异常: {e}")

    logger.info("\n" + "=" * 60)
    logger.info(f"示例完成: {passed}/{len(examples)}")
    logger.info("=" * 60)

    return passed == len(examples)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
