"""
验证VSI弱母线分析技能

使用方法:
    python verify_vsi_weak_bus.py
"""

import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from cloudpss_skills.builtin import VSIWeakBusSkill
from cloudpss_skills.core.utils import calculate_voltage_average, get_time_index

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_vsi_calculation():
    """测试VSI计算逻辑"""
    logger.info("=" * 60)
    logger.info("测试VSI计算逻辑")
    logger.info("=" * 60)

    import numpy as np

    # 模拟电压和无功数据
    time_data = np.linspace(0, 15, 1500).tolist()

    # 模拟在t=8s时注入无功，电压下降
    voltage_data = []
    for t in time_data:
        if t < 7.5:
            v = 1.0 + np.random.normal(0, 0.005)
        elif t < 8.0:
            v = 1.0 + np.random.normal(0, 0.005)
        elif t < 8.5:
            v = 0.95 + np.random.normal(0, 0.005)  # 电压下降
        else:
            v = 0.98 + np.random.normal(0, 0.005)  # 部分恢复
        voltage_data.append(v)

    # 模拟无功数据（注入100MVar）
    q_data = []
    for t in time_data:
        if 8.0 <= t < 8.5:
            q_data.append(100.0)
        else:
            q_data.append(0.0)

    # 计算VSI
    ts_inject = 8.0
    te_inject = 8.5
    ts_before = 7.5

    # 注入前电压
    ms_before = get_time_index(time_data, ts_before)
    me_before = get_time_index(time_data, ts_inject)
    v_before = calculate_voltage_average(voltage_data, ms_before, me_before)

    # 注入时电压
    ms_inject = get_time_index(time_data, ts_inject)
    me_inject = get_time_index(time_data, te_inject)
    v_after = calculate_voltage_average(voltage_data, ms_inject, me_inject)

    # 注入无功
    q_injected = 100.0

    # 计算VSI
    delta_v = v_before - v_after
    vsi = delta_v / q_injected if q_injected != 0 else 0

    logger.info(f"VSI计算:")
    logger.info(f"  - 注入前电压: {v_before:.4f}")
    logger.info(f"  - 注入时电压: {v_after:.4f}")
    logger.info(f"  - 电压变化: {delta_v:.4f}")
    logger.info(f"  - 注入无功: {q_injected}")
    logger.info(f"  - VSI: {vsi:.6f}")

    # 验证
    assert v_before > v_after, "注入无功后电压应下降"
    assert vsi > 0, "VSI应为正值"

    logger.info("✓ VSI计算逻辑测试通过")
    return True


def test_skill_initialization():
    """测试技能初始化"""
    logger.info("=" * 60)
    logger.info("测试技能初始化")
    logger.info("=" * 60)

    skill = VSIWeakBusSkill()

    logger.info(f"技能名称: {skill.name}")
    logger.info(f"技能描述: {skill.description}")

    # 测试配置验证
    valid_config = {
        "model": {"rid": "model/holdme/IEEE39", "source": "cloud"}
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

    skill = VSIWeakBusSkill()
    schema = skill.config_schema

    logger.info(f"配置Schema属性数: {len(schema.get('properties', {}))}")

    # 检查必需的配置项
    assert "model" in schema["required"], "model应该是必需的"
    assert "vsi_setup" in schema["properties"], "应该有vsi_setup配置"
    assert "analysis" in schema["properties"], "应该有analysis配置"

    logger.info("✓ Schema结构正确")
    return True


def main():
    """主测试函数"""
    logger.info("VSI弱母线分析技能验证")
    logger.info("=" * 60)

    tests = [
        ("技能初始化", test_skill_initialization),
        ("配置Schema", test_config_schema),
        ("VSI计算逻辑", test_vsi_calculation),
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
