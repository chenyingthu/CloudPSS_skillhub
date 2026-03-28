"""
VSI弱母线分析示例

使用方法:
    python examples/analysis/vsi_weak_bus_example.py
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
    logger.info("示例: 使用配置文件运行VSI弱母线分析")
    logger.info("=" * 60)

    # 加载配置
    config_path = Path("config/vsi_weak_bus.yaml")
    if not config_path.exists():
        logger.error(f"配置文件不存在: {config_path}")
        return False

    config = ConfigLoader.load(config_path)
    logger.info(f"加载配置: {config_path}")

    # 获取技能
    skill = get_skill("vsi_weak_bus")
    logger.info(f"获取技能: {skill.name}")

    # 显示配置
    logger.info(f"测试母线筛选: {config.get('vsi_setup', {}).get('bus_filter', {})}")
    logger.info(f"无功注入配置: {config.get('vsi_setup', {}).get('injection', {})}")

    logger.info("\n注意: VSI分析需要运行EMT仿真，此示例仅展示配置方式")
    logger.info("实际运行请确保:")
    logger.info("  1. 有可用的CloudPSS API Token")
    logger.info("  2. IEEE39模型可访问")
    logger.info("  3. 有足够的仿真时间（可能较长）")

    return True


def example_vsi_explanation():
    """VSI原理说明"""
    logger.info("\n" + "=" * 60)
    logger.info("VSI (Voltage Stability Index) 原理说明")
    logger.info("=" * 60)

    logger.info("""
VSI是电压稳定指数，用于识别电压稳定性薄弱的母线。

计算原理:
    VSI_ij = (V_before - V_after) / Q_injected

其中:
    - V_before: 注入无功前的电压
    - V_after: 注入无功后的电压
    - Q_injected: 注入的无功功率
    - i: 注入无功的母线
    - j: 观测电压变化的母线

对于母线i的VSIi（平均敏感度）:
    VSI_i = mean(VSI_ij for all j)

物理意义:
    - VSI越大，表示该母线对无功变化越敏感
    - VSI大的母线电压稳定性差，是无功补偿的优先位置

测试流程:
    1. 为每个母线添加动态无功注入源（shuntLC + 断路器）
    2. 依次在各母线注入无功（时间错开）
    3. 记录所有母线的电压变化
    4. 计算VSI指标
    5. 排序识别弱母线

与其他指标的关系:
    - 与PV曲线：VSI高的母线在PV曲线上更接近崩溃点
    - 与无功储备：VSI高的母线无功储备通常较低
    - 与短路容量：VSI与短路容量呈负相关
    """)

    return True


def example_results_interpretation():
    """结果解读示例"""
    logger.info("\n" + "=" * 60)
    logger.info("VSI结果解读")
    logger.info("=" * 60)

    # 模拟VSI结果
    example_results = {
        "weak_buses": [
            {"label": "Bus_16", "vsi": 0.0152},
            {"label": "Bus_15", "vsi": 0.0128},
            {"label": "Bus_26", "vsi": 0.0115},
        ],
        "summary": {
            "total_buses": 39,
            "weak_bus_count": 3,
            "max_vsi": 0.0152,
            "min_vsi": 0.0021,
            "avg_vsi": 0.0065
        }
    }

    logger.info("示例VSI分析结果:")
    logger.info(f"  总母线数: {example_results['summary']['total_buses']}")
    logger.info(f"  弱母线数: {example_results['summary']['weak_bus_count']}")
    logger.info(f"  VSI范围: {example_results['summary']['min_vsi']:.4f} ~ {example_results['summary']['max_vsi']:.4f}")

    logger.info("\n弱母线列表:")
    for i, bus in enumerate(example_results['weak_buses'], 1):
        logger.info(f"  {i}. {bus['label']}: VSI={bus['vsi']:.4f}")

    logger.info("""

结果解读:
    ✓ Bus_16的VSI最高(0.0152)，是系统中最薄弱的母线
    ✓ 这些母线应优先考虑无功补偿设备安装
    ✓ 可通过reactive_compensation_design技能进行补偿设计

工程建议:
    1. VSI > 0.01: 高优先级，建议安装调相机或SVG
    2. VSI 0.005-0.01: 中优先级，根据经济分析决定
    3. VSI < 0.005: 电压稳定性良好
    """)

    return True


def main():
    """主函数"""
    logger.info("VSI弱母线分析技能示例")
    logger.info("=" * 60)

    examples = [
        ("配置文件方式", example_with_config_file),
        ("VSI原理说明", example_vsi_explanation),
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
