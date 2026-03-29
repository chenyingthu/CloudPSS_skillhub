"""
无功补偿设计示例

使用方法:
    python examples/analysis/reactive_compensation_design_example.py
"""

import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cloudpss_skills.core import get_skill, ConfigLoader

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_with_config_file():
    """使用配置文件运行"""
    logger.info("=" * 60)
    logger.info("示例: 使用配置文件运行无功补偿设计")
    logger.info("=" * 60)

    # 加载配置
    config_path = Path("config/reactive_compensation_design.yaml")
    if not config_path.exists():
        logger.error(f"配置文件不存在: {config_path}")
        return False

    config = ConfigLoader.load(config_path)
    logger.info(f"加载配置: {config_path}")

    # 获取技能
    skill = get_skill("reactive_compensation_design")
    logger.info(f"获取技能: {skill.name}")

    # 显示配置
    logger.info(f"VSI输入配置: {config.get('vsi_input', {})}")
    logger.info(f"补偿设备配置: {config.get('compensation', {})}")
    logger.info(f"迭代配置: {config.get('iteration', {})}")

    logger.info("\n注意: 此示例仅展示配置方式")
    logger.info("实际运行需要:")
    logger.info("  1. 有可用的CloudPSS API Token")
    logger.info("  2. 模型可访问且有写入权限")
    logger.info("  3. 有足够的仿真时间")

    return True


def example_workflow():
    """工作流程说明"""
    logger.info("\n" + "=" * 60)
    logger.info("无功补偿设计工作流程")
    logger.info("=" * 60)

    logger.info("""
完整工作流程:

步骤1: VSI弱母线分析
  └── 运行 vsi_weak_bus 技能
  └── 获取弱母线列表和VSI指标
  └── 保存结果到 vsi_weak_bus_result.json

步骤2: 无功补偿设计
  └── 读取VSI结果
  └── 识别需要补偿的母线
  └── 批量添加同步调相机
  └── 配置故障场景
  └── 迭代优化容量
  └── 输出最终方案

步骤3: 验证补偿效果
  └── 使用 disturbance_severity 技能
  └── 对比补偿前后的DV/SI指标

迭代优化流程:
  迭代1: 初始容量 → EMT仿真 → 计算DV → 调整容量
  迭代2: 新容量 → EMT仿真 → 计算DV → 调整容量
  ...
  直到: DV满足要求 或 达到最大迭代次数 或 容量收敛

容量调整策略:
  - 电压下限违规(DV_down < 0): 增加容量
  - 电压上限违规(DV_up < 0): 减少容量
  - 调整量 = DV * 当前容量 * 加速比
""")

    return True


def example_results_interpretation():
    """结果解读"""
    logger.info("\n" + "=" * 60)
    logger.info("无功补偿设计结果解读")
    logger.info("=" * 60)

    # 模拟结果
    example_result = {
        "target_buses": ["Bus_16", "Bus_15"],
        "final_capacities": [150.5, 120.3],
        "iterations": 5,
        "converged": True,
        "compensation_scheme": [
            {
                "bus_label": "Bus_16",
                "capacity_mvar": 150.5,
                "voltage_kv": 230,
                "vsi": 0.015
            },
            {
                "bus_label": "Bus_15",
                "capacity_mvar": 120.3,
                "voltage_kv": 230,
                "vsi": 0.012
            }
        ]
    }

    logger.info("示例补偿设计结果:")
    logger.info(f"  补偿母线: {example_result['target_buses']}")
    logger.info(f"  迭代次数: {example_result['iterations']}")
    logger.info(f"  是否收敛: {'是' if example_result['converged'] else '否'}")

    logger.info("\n补偿方案:")
    for i, item in enumerate(example_result['compensation_scheme'], 1):
        logger.info(f"  {i}. {item['bus_label']}:")
        logger.info(f"     - 补偿容量: {item['capacity_mvar']:.1f} MVar")
        logger.info(f"     - 母线电压: {item['voltage_kv']:.0f} kV")
        logger.info(f"     - VSI: {item['vsi']:.4f}")

    logger.info("""

结果解读:
    ✓ Bus_16需要150.5 MVar补偿（VSI最高，最薄弱）
    ✓ Bus_15需要120.3 MVar补偿
    ✓ 共需投资约270.8 MVar调相机容量

工程建议:
    1. 优先在Bus_16安装调相机（VSI=0.015，电压稳定性最差）
    2. 可选用300 MVar级调相机（留有裕度）
    3. 实际选型需考虑设备规格和经济效益
    4. 建议分阶段实施，先解决最严重的薄弱点
""")

    return True


def main():
    """主函数"""
    logger.info("无功补偿设计技能示例")
    logger.info("=" * 60)

    examples = [
        ("配置文件方式", example_with_config_file),
        ("工作流程", example_workflow),
        ("结果解读", example_results_interpretation),
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
