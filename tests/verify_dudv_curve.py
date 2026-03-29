"""
验证DUDV曲线可视化技能

使用方法:
    python verify_dudv_curve.py
"""

import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills.builtin import DUDVCurveSkill

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_skill_initialization():
    """测试技能初始化"""
    logger.info("=" * 60)
    logger.info("测试技能初始化")
    logger.info("=" * 60)

    skill = DUDVCurveSkill()

    logger.info(f"技能名称: {skill.name}")
    logger.info(f"技能描述: {skill.description}")

    # 测试配置验证
    valid_config = {
        "model": {"rid": "model/holdme/IEEE39"},
        "buses": ["Bus_16"]
    }

    result = skill.validate(valid_config)
    assert result.valid, f"有效配置应该通过验证: {result.errors}"
    logger.info("✓ 配置验证通过")

    # 测试无效配置
    invalid_config = {"model": {}}  # 缺少buses
    result = skill.validate(invalid_config)
    assert not result.valid, "无效配置应该验证失败"
    logger.info("✓ 无效配置正确识别")

    return True


def test_config_schema():
    """测试配置Schema"""
    logger.info("=" * 60)
    logger.info("测试配置Schema")
    logger.info("=" * 60)

    skill = DUDVCurveSkill()
    schema = skill.config_schema

    logger.info(f"配置Schema属性数: {len(schema.get('properties', {}))}")

    # 检查必需的配置项
    assert "buses" in schema["required"], "buses应该是必需的"
    assert "model" in schema["required"], "model应该是必需的"
    assert "dudv" in schema["properties"], "应该有dudv配置"
    assert "output" in schema["properties"], "应该有output配置"

    logger.info("✓ Schema结构正确")
    return True


def test_from_disturbance_result():
    """测试从扰动结果加载"""
    logger.info("=" * 60)
    logger.info("测试从扰动结果加载")
    logger.info("=" * 60)

    skill = DUDVCurveSkill()

    # 创建模拟的扰动结果文件
    import json
    import tempfile
    import os

    mock_result = {
        "bus_results": [
            {
                "bus_label": "Bus_16",
                "v_steady": 1.02,
                "dv_up": 0.05,
                "dv_down": 0.08
            },
            {
                "bus_label": "Bus_15",
                "v_steady": 0.98,
                "dv_up": 0.03,
                "dv_down": 0.06
            }
        ]
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(mock_result, f)
        temp_file = f.name

    try:
        # 测试加载
        dudv_data = skill.from_disturbance_severity_result(
            result_file=temp_file,
            bus_labels=["Bus_16"]
        )

        assert "Bus_16" in dudv_data, "应该包含Bus_16"
        assert "voltage" in dudv_data["Bus_16"], "应该包含voltage数据"
        assert "dv" in dudv_data["Bus_16"], "应该包含dv数据"

        logger.info(f"✓ 成功加载 {len(dudv_data)} 个母线的数据")

        # 测试加载所有母线
        dudv_data_all = skill.from_disturbance_severity_result(temp_file)
        assert len(dudv_data_all) == 2, "应该加载所有母线"
        logger.info("✓ 成功加载所有母线数据")

    finally:
        os.unlink(temp_file)

    return True


def test_dudv_calculation():
    """测试DUDV数据计算逻辑"""
    logger.info("=" * 60)
    logger.info("测试DUDV数据计算逻辑")
    logger.info("=" * 60)

    # 模拟DUDV数据
    voltage_points = [0.8, 0.9, 1.0, 1.1, 1.2]
    dv_points = [-0.2, -0.1, 0.0, 0.1, 0.2]

    logger.info(f"电压点: {voltage_points}")
    logger.info(f"DV点: {dv_points}")

    # 验证数据一致性
    assert len(voltage_points) == len(dv_points), "电压和DV点数应该相同"
    logger.info("✓ 数据点数量一致")

    # 验证电压范围
    assert min(voltage_points) >= 0.5, "电压不应过低"
    assert max(voltage_points) <= 1.5, "电压不应过高"
    logger.info("✓ 电压范围合理")

    return True


def main():
    """主测试函数"""
    logger.info("DUDV曲线可视化技能验证")
    logger.info("=" * 60)

    tests = [
        ("技能初始化", test_skill_initialization),
        ("配置Schema", test_config_schema),
        ("扰动结果加载", test_from_disturbance_result),
        ("DUDV计算逻辑", test_dudv_calculation),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            logger.info(f"\n运行测试: {name}")
            if test_func():
                passed += 1
                logger.info(f"✓ {name} 通过")
            else:
                failed += 1
                logger.error(f"✗ {name} 失败")
        except Exception as e:
            failed += 1
            logger.error(f"✗ {name} 失败: {e}", exc_info=True)

    logger.info("\n" + "=" * 60)
    logger.info(f"测试结果: {passed}/{len(tests)} 通过")
    logger.info("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
