"""
验证扰动严重度分析技能

使用方法:
    python verify_disturbance_severity.py

或者:
    python -m cloudpss_skills run --config config/disturbance_severity.yaml
"""

import logging
from pathlib import Path
import sys

# 确保cloudpss_skills在路径中
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from cloudpss_skills.builtin import DisturbanceSeveritySkill

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_with_mock_data():
    """使用模拟数据测试DV/SI计算逻辑"""
    import numpy as np
    from cloudpss_skills.core.utils import (
        calculate_dv_metrics,
        calculate_si_metric,
        calculate_voltage_average
    )

    logger.info("=" * 60)
    logger.info("测试DV/SI计算逻辑（使用模拟数据）")
    logger.info("=" * 60)

    # 生成模拟电压数据（故障后电压跌落然后恢复）
    time_data = np.linspace(0, 10, 1000).tolist()

    # 正常电压
    voltage_data = []
    for t in time_data:
        if t < 4.0:
            # 故障前：正常电压
            v = 1.0 + np.random.normal(0, 0.01)
        elif t < 4.1:
            # 故障期间：电压跌落
            progress = (t - 4.0) / 0.1
            v = 1.0 - progress * 0.3 + np.random.normal(0, 0.02)
        elif t < 5.0:
            # 故障切除后：逐渐恢复
            progress = (t - 4.1) / 0.9
            v = 0.7 + progress * 0.3 + np.random.normal(0, 0.02)
        else:
            # 恢复后：稳态
            v = 1.0 + np.random.normal(0, 0.01)
        voltage_data.append(v)

    disturbance_time = 4.0
    pre_fault_window = 0.5

    # 测试DV计算
    dv_result = calculate_dv_metrics(
        voltage_data, time_data,
        disturbance_time, pre_fault_window
    )

    logger.info(f"DV计算结果:")
    logger.info(f"  - DV上限裕度: {dv_result['dv_up']:.4f}")
    logger.info(f"  - DV下限裕度: {dv_result['dv_down']:.4f}")
    logger.info(f"  - 稳态电压: {dv_result['v_steady']:.4f}")

    # 测试SI计算
    si_result = calculate_si_metric(
        voltage_data, time_data,
        disturbance_time, pre_fault_window
    )

    logger.info(f"SI计算结果: {si_result:.4f}")

    # 验证
    assert dv_result['v_steady'] > 0.9, "稳态电压应该在0.9以上"
    assert dv_result['dv_down'] < 0, "应该有电压下限裕度不足（模拟故障）"
    assert si_result > 0, "SI应该大于0"

    logger.info("✓ 模拟数据测试通过")
    return True


def test_skill_initialization():
    """测试技能初始化和配置验证"""
    logger.info("=" * 60)
    logger.info("测试技能初始化")
    logger.info("=" * 60)

    skill = DisturbanceSeveritySkill()

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

    skill = DisturbanceSeveritySkill()
    schema = skill.config_schema

    logger.info(f"配置Schema属性数: {len(schema.get('properties', {}))}")

    # 检查必需的配置项
    assert "model" in schema["required"], "model应该是必需的"
    assert "auth" in schema["properties"], "应该有auth配置"
    assert "simulation" in schema["properties"], "应该有simulation配置"
    assert "analysis" in schema["properties"], "应该有analysis配置"

    logger.info("✓ Schema结构正确")
    return True


def main():
    """主测试函数"""
    logger.info("开始验证扰动严重度分析技能")
    logger.info("=" * 60)

    tests = [
        ("技能初始化", test_skill_initialization),
        ("配置Schema", test_config_schema),
        ("DV/SI计算逻辑", test_with_mock_data),
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
