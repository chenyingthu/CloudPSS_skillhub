"""
HDF5数据导出示例

演示如何使用 hdf5_export 技能将仿真结果导出为HDF5格式。
"""

import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cloudpss_skills import get_skill
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_basic_export():
    """基本导出示例"""
    logger.info("=" * 60)
    logger.info("示例: 基本HDF5导出")
    logger.info("=" * 60)

    # 创建一个模拟结果文件
    result_file = Path("./results/test_result.json")
    result_file.parent.mkdir(parents=True, exist_ok=True)

    test_data = {
        "type": "disturbance",
        "dv_results": [
            {"bus": "Bus_16", "dv_up": 0.05, "dv_down": 0.08, "v_steady": 1.02},
            {"bus": "Bus_15", "dv_up": 0.03, "dv_down": 0.06, "v_steady": 0.98}
        ],
        "si_results": [
            {"bus": "Bus_16", "si": 0.15},
            {"bus": "Bus_15", "si": 0.12}
        ]
    }

    with open(result_file, 'w') as f:
        json.dump(test_data, f)

    skill = get_skill("hdf5_export")

    config = {
        "source": {
            "type": "file",
            "file_path": str(result_file)
        },
        "output": {
            "path": "./results/",
            "filename": "test_export.h5",
            "compression": "gzip",
            "compression_level": 4
        },
        "metadata": {
            "title": "测试导出",
            "description": "HDF5导出功能测试",
            "tags": ["test", "demo"]
        },
        "options": {
            "include_metadata": True
        }
    }

    # 验证配置
    validation = skill.validate(config)
    if not validation.valid:
        logger.error(f"配置验证失败: {validation.errors}")
        return

    logger.info("✓ 配置验证通过")
    logger.info(f"源文件: {config['source']['file_path']}")
    logger.info(f"压缩: {config['output']['compression']}")

    # 执行导出
    result = skill.run(config)
    logger.info(f"导出结果: {result.status}")
    logger.info(f"输出文件: {result.data.get('hdf5_file')}")
    logger.info(f"文件大小: {result.data.get('file_size', 0) / 1024:.2f} KB")


def example_compression_comparison():
    """压缩算法对比"""
    logger.info("\n" + "=" * 60)
    logger.info("示例: 压缩算法对比")
    logger.info("=" * 60)

    compressions = [
        ("gzip", 4, "标准压缩，兼容性好"),
        ("gzip", 9, "最大压缩，速度较慢"),
        ("lzf", None, "快速压缩，压缩比较低"),
        ("none", None, "无压缩，速度最快")
    ]

    for algo, level, desc in compressions:
        level_str = f"(level={level})" if level else ""
        logger.info(f"  {algo} {level_str}: {desc}")


def example_read_hdf5():
    """读取HDF5文件示例"""
    logger.info("\n" + "=" * 60)
    logger.info("示例: 读取HDF5文件")
    logger.info("=" * 60)

    skill = get_skill("hdf5_export")
    hdf5_path = "./results/test_export.h5"

    try:
        # 列出所有数据集
        datasets = skill.list_datasets(hdf5_path)
        logger.info(f"✓ 找到 {len(datasets)} 个数据集")
        for ds in datasets[:5]:  # 只显示前5个
            logger.info(f"  - {ds}")

        # 读取特定数据集
        data = skill.read_hdf5(hdf5_path)
        logger.info(f"✓ 成功读取数据，包含 {len(data)} 个顶级组")

    except FileNotFoundError:
        logger.info(f"文件不存在: {hdf5_path}")
        logger.info("  请先运行基本导出示例")


def example_metadata_export():
    """元数据导出示例"""
    logger.info("\n" + "=" * 60)
    logger.info("示例: 完整元数据导出")
    logger.info("=" * 60)

    metadata = {
        "title": "IEEE39系统N-1分析",
        "description": "基于2026年夏季峰值负荷的N-1安全分析",
        "tags": [
            "IEEE39",
            "N-1",
            "voltage_stability",
            "summer_peak"
        ],
        "custom_attrs": {
            "project": "TSQH_2026",
            "scenario": "summer_peak",
            "engineer": "chenying",
            "approved": "true"
        }
    }

    logger.info("元数据配置:")
    logger.info(f"  标题: {metadata['title']}")
    logger.info(f"  标签: {', '.join(metadata['tags'])}")
    logger.info(f"  自定义属性: {len(metadata['custom_attrs'])} 个")


def main():
    """主函数"""
    logger.info("HDF5数据导出技能示例")
    logger.info("=" * 60)

    examples = [
        ("基本导出", example_basic_export),
        ("压缩对比", example_compression_comparison),
        ("读取HDF5", example_read_hdf5),
        ("元数据导出", example_metadata_export),
    ]

    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            logger.error(f"示例 '{name}' 失败: {e}")

    logger.info("\n" + "=" * 60)
    logger.info("示例运行完成")
    logger.info("=" * 60)
    logger.info("\nHDF5工具函数:")
    logger.info("  skill.read_hdf5(path) - 读取整个文件")
    logger.info("  skill.read_hdf5(path, dataset) - 读取特定数据集")
    logger.info("  skill.list_datasets(path) - 列出所有数据集")


if __name__ == "__main__":
    main()
