"""
DUDV曲线可视化示例

演示如何使用 dudv_curve 技能生成电压稳定性分析曲线。
"""

import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cloudpss_skills import get_skill

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_basic_usage():
    """基本使用示例"""
    logger.info("=" * 60)
    logger.info("示例: 基本使用")
    logger.info("=" * 60)

    skill = get_skill("dudv_curve")

    config = {
        "model": {
            "rid": "model/holdme/IEEE39",
            "source": "cloud"
        },
        "buses": ["Bus_16", "Bus_15", "Bus_26"],
        "simulation": {
            "end_time": 15.0,
            "step_time": 0.0001,
            "fault_bus": "Bus_16",
            "fault_type": "three_phase",
            "fault_time": 4.0,
            "fault_duration": 0.1
        },
        "dudv": {
            "voltage_range": [0.8, 1.2],
            "num_points": 20,
            "injection_duration": 2.0
        },
        "output": {
            "format": "png",
            "path": "./results/",
            "prefix": "dudv_example",
            "show_grid": True,
            "show_legend": True
        }
    }

    # 验证配置
    validation = skill.validate(config)
    if not validation.valid:
        logger.error(f"配置验证失败: {validation.errors}")
        return

    logger.info("✓ 配置验证通过")
    logger.info(f"分析母线: {config['buses']}")
    logger.info(f"电压范围: {config['dudv']['voltage_range']}")
    logger.info(f"扫描点数: {config['dudv']['num_points']}")

    # 注意: 实际运行需要 CloudPSS token
    # result = skill.run(config)
    # logger.info(f"执行结果: {result.status}")


def example_from_disturbance_result():
    """从扰动严重度结果生成DUDV曲线"""
    logger.info("\n" + "=" * 60)
    logger.info("示例: 从扰动严重度结果生成DUDV曲线")
    logger.info("=" * 60)

    skill = get_skill("dudv_curve")

    # 从已有结果加载数据
    result_file = "./results/disturbance_severity_result.json"

    try:
        dudv_data = skill.from_disturbance_severity_result(
            result_file=result_file,
            bus_labels=["Bus_16", "Bus_15"]
        )

        logger.info(f"✓ 成功加载 {len(dudv_data)} 个母线的DUDV数据")
        for bus, data in dudv_data.items():
            logger.info(f"  - {bus}: {len(data['voltage'])} 个数据点")

    except FileNotFoundError:
        logger.info(f"结果文件不存在: {result_file}")
        logger.info("  请先运行扰动严重度分析技能")


def example_multiple_buses():
    """多母线对比分析"""
    logger.info("\n" + "=" * 60)
    logger.info("示例: 多母线对比分析")
    logger.info("=" * 60)

    buses_list = [
        ["Bus_16"],                           # 单母线
        ["Bus_16", "Bus_15"],                 # 2母线
        ["Bus_16", "Bus_15", "Bus_26"],       # 3母线
        ["Bus_16", "Bus_15", "Bus_26", "Bus_17", "Bus_18", "Bus_19"],  # 6母线
    ]

    for buses in buses_list:
        logger.info(f"母线数量: {len(buses)}")
        logger.info(f"  母线: {buses}")

        if len(buses) <= 2:
            layout = "1行"
        elif len(buses) <= 4:
            layout = "2x2"
        else:
            rows = (len(buses) + 1) // 2
            layout = f"{rows}x2"

        logger.info(f"  图表布局: {layout}")


def example_output_formats():
    """不同输出格式示例"""
    logger.info("\n" + "=" * 60)
    logger.info("示例: 输出格式选择")
    logger.info("=" * 60)

    formats = [
        ("png", "PNG图片，适合文档嵌入"),
        ("pdf", "PDF矢量图，适合论文发表"),
        ("svg", "SVG矢量图，适合网页展示"),
    ]

    for fmt, desc in formats:
        logger.info(f"  {fmt}: {desc}")


def main():
    """主函数"""
    logger.info("DUDV曲线可视化技能示例")
    logger.info("=" * 60)

    examples = [
        ("基本使用", example_basic_usage),
        ("从扰动结果加载", example_from_disturbance_result),
        ("多母线对比", example_multiple_buses),
        ("输出格式", example_output_formats),
    ]

    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            logger.error(f"示例 '{name}' 失败: {e}")

    logger.info("\n" + "=" * 60)
    logger.info("示例运行完成")
    logger.info("=" * 60)
    logger.info("\n提示: 实际运行需要有效的 CloudPSS token")
    logger.info("      配置 token 文件: .cloudpss_token")
    logger.info("\nDUDV曲线解读:")
    logger.info("  - 横轴: 电压 (pu)")
    logger.info("  - 纵轴: 电压偏差 ΔV (pu)")
    logger.info("  - 曲线形状反映电压稳定性")
    logger.info("  - 斜率越大，电压稳定性越差")


if __name__ == "__main__":
    main()
