"""
验证无功补偿设计技能

使用方法:
    python verify_reactive_compensation_design.py
"""

import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills.builtin import ReactiveCompensationDesignSkill

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

    skill = ReactiveCompensationDesignSkill()

    logger.info(f"技能名称: {skill.name}")
    logger.info(f"技能描述: {skill.description}")

    # 测试配置验证
    valid_config = {
        "model": {"rid": "model/holdme/IEEE39", "source": "cloud"},
        "vsi_input": {"target_buses": ["Bus_16", "Bus_15"]}
    }

    result = skill.validate(valid_config)
    assert result.valid, f"有效配置应该通过验证: {result.errors}"
    logger.info("✓ 配置验证通过")

    # 测试无效配置
    invalid_config = {}
    result = skill.validate(invalid_config)
    assert not result.valid, "空配置应该验证失败"
    logger.info("✓ 无效配置正确识别")

    return True


def test_config_schema():
    """测试配置Schema"""
    logger.info("=" * 60)
    logger.info("测试配置Schema")
    logger.info("=" * 60)

    skill = ReactiveCompensationDesignSkill()
    schema = skill.config_schema

    logger.info(f"配置Schema属性数: {len(schema.get('properties', {}))}")

    # 检查必需的配置项
    assert "model" in schema["required"], "model应该是必需的"
    assert "vsi_input" in schema["properties"], "应该有vsi_input配置"
    assert "compensation" in schema["properties"], "应该有compensation配置"
    assert "iteration" in schema["properties"], "应该有iteration配置"

    logger.info("✓ Schema结构正确")
    return True


def test_iteration_logic():
    """测试迭代逻辑"""
    logger.info("=" * 60)
    logger.info("测试迭代容量调整逻辑")
    logger.info("=" * 60)

    skill = ReactiveCompensationDesignSkill()

    # 模拟数据
    capacities = [100.0, 100.0]
    dv_up = [0.05, -0.02]  # 第二个母线有上限违规
    dv_down = [0.03, -0.05]  # 第二个母线有下限违规

    # 计算调整
    adjustments = skill._calculate_adjustments(
        capacities,
        dv_up,
        dv_down,
        [{}, {}],
        speed_ratio=0.2,
        max_capacity=800,
        min_capacity=10
    )

    logger.info(f"初始容量: {capacities}")
    logger.info(f"DV上限: {dv_up}")
    logger.info(f"DV下限: {dv_down}")
    logger.info(f"调整量: {adjustments}")

    # 验证调整方向
    assert adjustments[1] > 0, "有下限违规的母线应该增加容量"

    logger.info("✓ 迭代逻辑测试通过")
    return True


def test_scheme_generation():
    """测试方案生成"""
    logger.info("=" * 60)
    logger.info("测试补偿方案生成")
    logger.info("=" * 60)

    skill = ReactiveCompensationDesignSkill()

    target_buses = [
        {"label": "Bus_16", "key": "bus_16", "voltage": 230, "vsi": 0.015},
        {"label": "Bus_15", "key": "bus_15", "voltage": 230, "vsi": 0.012}
    ]
    capacities = [150.0, 120.0]

    scheme = skill._generate_scheme(target_buses, capacities)

    logger.info(f"补偿方案:")
    for item in scheme:
        logger.info(f"  {item['bus_label']}: {item['capacity_mvar']:.1f} MVar, VSI={item['vsi']:.4f}")

    assert len(scheme) == 2, "应该有2个补偿方案"
    assert scheme[0]['capacity_mvar'] == 150.0, "容量应该匹配"

    logger.info("✓ 方案生成测试通过")
    return True


def main():
    """主测试函数"""
    logger.info("无功补偿设计技能验证")
    logger.info("=" * 60)

    tests = [
        ("技能初始化", test_skill_initialization),
        ("配置Schema", test_config_schema),
        ("迭代逻辑", test_iteration_logic),
        ("方案生成", test_scheme_generation),
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
