"""
创建正式的新能源测试算例

创建以下测试模型（固定分支名，可重复使用）：
1. model/holdme/test/ieee39_wind - IEEE39 + 风电场
2. model/holdme/test/ieee39_pv - IEEE39 + 光伏电站
3. model/holdme/test/ieee39_hybrid - IEEE39 + 风电 + 光伏 (混合新能源)

运行方式:
    python examples/metadata/create_test_models.py --all
    python examples/metadata/create_test_models.py --wind
    python examples/metadata/create_test_models.py --pv
    python examples/metadata/create_test_models.py --hybrid
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


def setup_auth():
    """设置 CloudPSS 认证"""
    from cloudpss import setToken

    token = os.environ.get('CLOUDPSS_TOKEN')
    if not token:
        token_file = Path('.cloudpss_token')
        if token_file.exists():
            token = token_file.read_text().strip()
            logger.info(f"已从 {token_file} 读取 token")
        else:
            logger.error("未找到 CloudPSS token!")
            return False

    setToken(token)
    logger.info("CloudPSS 认证已设置")
    return True


def create_wind_model():
    """创建 IEEE39 + 风电场 测试模型（使用WTG_PMSG_01，支持潮流计算）"""
    logger.info("\n" + "="*60)
    logger.info("创建测试模型: IEEE39 + 风电场 (Wind Farm - PMSG)")
    logger.info("="*60)

    from cloudpss_skills.builtin.model_builder import ModelBuilderSkill
    from cloudpss_skills.metadata.integration import get_metadata_integration

    mi = get_metadata_integration()
    mi.initialize('examples/metadata')

    # 使用 WTG_PMSG_01 组件（支持潮流计算的正确组件类型）
    component_type = 'model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1'

    # 获取 WTG_PMSG_01 的自动补全参数
    # 关键参数说明：
    #   Pctrl_mode='0' (PQ节点) - 新能源作为负荷型电源，给定P和Q
    #   Pctrl_mode='1' (PV节点) - 新能源控制电压（需要额外无功支撑设备）
    # 实际风电场通常作为PQ节点运行，因此使用'0'
    user_params = {
        'Vbase': 0.69,           # 基准电压 kV
        'Sbase': 2.5,            # 单台风机容量 MVA
        'P_cmd': 80.0,           # 总有功指令 MW (40台 × 2MW)
        'pf_P': 80.0,            # 潮流总有功 MW <-- 关键：设为总出力！
        'pf_Q': 0.0,             # 潮流总无功 MW
        'Pctrl_mode': '0',       # PQ节点控制
        # Note: UnitCount 不在组件参数中，通过等值方式实现
    }
    completed_params = mi.auto_complete_parameters(component_type, user_params)

    config = {
        'base_model': {'rid': 'model/holdme/IEEE39'},
        'modifications': [
            {
                'action': 'add_component',
                'component_type': component_type,
                'label': 'WindFarm_Bus10',
                'parameters': completed_params,
                'position': {'x': 400, 'y': 300},
                'pin_connection': {'target_bus': 'bus10', 'pin_name': '0'}
            }
        ],
        'output': {
            'save': True,
            'branch': 'test_ieee39_wind',
            'name': 'IEEE39_with_WindFarm_PMSG',
            'description': 'IEEE39 系统添加风电场（PMSG模型，支持潮流计算）'
        }
    }

    skill = ModelBuilderSkill()
    result = skill.run(config)

    if result.status.value == 'success':
        model_rid = result.data['generated_models'][0]['rid']
        logger.info(f"✅ 风电模型创建成功: {model_rid}")
        return model_rid
    else:
        logger.error(f"❌ 风电模型创建失败: {result.error}")
        return None


def create_pv_model():
    """创建 IEEE39 + 光伏电站 测试模型"""
    logger.info("\n" + "="*60)
    logger.info("创建测试模型: IEEE39 + 光伏电站 (PV Station)")
    logger.info("="*60)

    from cloudpss_skills.builtin.model_builder import ModelBuilderSkill
    from cloudpss_skills.metadata.integration import get_metadata_integration

    mi = get_metadata_integration()
    mi.initialize('examples/metadata')

    # 使用公开可访问且支持潮流的光伏封装模型
    component_type = 'model/open-cloudpss/PVS_01-avm-stdm-v1b5'
    completed_params = {
        'P_cmd': 50.0,
        'pf_P': 50.0,
        'pf_Q': 0.0,
        'Pctrl_mode': '0',
        'Q_cmd': 0.0,
        'Vbase': 0.69,
    }

    config = {
        'base_model': {'rid': 'model/holdme/IEEE39'},
        'modifications': [
            {
                'action': 'add_component',
                'component_type': component_type,
                'label': 'PVStation_Bus14',
                'parameters': completed_params,
                'position': {'x': 600, 'y': 200},
                'pin_connection': {'target_bus': 'bus14', 'pin_name': '0'}
            }
        ],
        'output': {
            'save': True,
            'branch': 'test_ieee39_pv',
            'name': 'IEEE39_with_PV_OpenModel',
            'description': 'IEEE39 系统添加公开光伏封装模型（支持潮流）'
        }
    }

    skill = ModelBuilderSkill()
    result = skill.run(config)

    if result.status.value == 'success':
        model_rid = result.data['generated_models'][0]['rid']
        logger.info(f"✅ 光伏模型创建成功: {model_rid}")
        return model_rid
    else:
        logger.error(f"❌ 光伏模型创建失败: {result.error}")
        return None


def create_hybrid_model():
    """创建 IEEE39 + 风电 + 光伏 混合新能源测试模型"""
    logger.info("\n" + "="*60)
    logger.info("创建测试模型: IEEE39 + 混合新能源 (Wind + PV)")
    logger.info("="*60)

    from cloudpss_skills.builtin.model_builder import ModelBuilderSkill
    from cloudpss_skills.metadata.integration import get_metadata_integration

    mi = get_metadata_integration()
    mi.initialize('examples/metadata')

    # 使用 WTG_PMSG_01 组件（支持潮流计算）
    wind_component_type = 'model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1'
    wind_params = mi.auto_complete_parameters(
        wind_component_type,
        {
            'Vbase': 0.69,
            'Sbase': 2.5,
            'P_cmd': 2.0,
            'pf_P': 2.0,
            'pf_Q': 0.0,      # 零无功输出
            'Pctrl_mode': '0', # PQ节点（符合实际新能源特性）
            'UnitCount': 40
        }
    )

    pv_component_type = 'model/open-cloudpss/PVS_01-avm-stdm-v1b5'
    pv_params = {
        'P_cmd': 50.0,
        'pf_P': 50.0,
        'pf_Q': 0.0,
        'Pctrl_mode': '0',
        'Q_cmd': 0.0,
        'Vbase': 0.69,
    }

    config = {
        'base_model': {'rid': 'model/holdme/IEEE39'},
        'modifications': [
            {
                'action': 'add_component',
                'component_type': wind_component_type,
                'label': 'WindFarm_Bus10',
                'parameters': wind_params,
                'position': {'x': 400, 'y': 300},
                'pin_connection': {'target_bus': 'bus10', 'pin_name': '0'}
            },
            {
                'action': 'add_component',
                'component_type': pv_component_type,
                'label': 'PVStation_Bus14',
                'parameters': pv_params,
                'position': {'x': 600, 'y': 200},
                'pin_connection': {'target_bus': 'bus14', 'pin_name': '0'}
            }
        ],
        'output': {
            'save': True,
            'branch': 'test_ieee39_hybrid',
            'name': 'IEEE39_with_Hybrid_Renewable',
            'description': 'IEEE39 系统添加风电场和光伏电站（混合新能源）'
        }
    }

    skill = ModelBuilderSkill()
    result = skill.run(config)

    if result.status.value == 'success':
        model_rid = result.data['generated_models'][0]['rid']
        logger.info(f"✅ 混合新能源模型创建成功: {model_rid}")
        return model_rid
    else:
        logger.error(f"❌ 混合新能源模型创建失败: {result.error}")
        return None


def validate_model(model_rid: str, name: str):
    """验证模型"""
    logger.info(f"\n验证模型: {name}")
    logger.info(f"RID: {model_rid}")

    from cloudpss_skills.builtin.model_validator import ModelValidatorSkill

    config = {
        'models': [{'rid': model_rid, 'name': name}],
        'validation': {'phases': ['topology', 'powerflow'], 'timeout': 300},
        'output': {'format': 'console'}
    }

    skill = ModelValidatorSkill()
    result = skill.run(config)

    if result.status.value == 'success':
        report = result.data['reports'][0]
        if report['passed']:
            logger.info(f"✅ {name} 验证通过")
        else:
            logger.warning(f"⚠️  {name} 验证未完全通过")
        return report['passed']
    else:
        logger.error(f"❌ {name} 验证失败: {result.error}")
        return False


def main():
    parser = argparse.ArgumentParser(description='创建新能源测试算例')
    parser.add_argument('--wind', action='store_true', help='创建风电测试模型')
    parser.add_argument('--pv', action='store_true', help='创建光伏测试模型')
    parser.add_argument('--hybrid', action='store_true', help='创建混合新能源测试模型')
    parser.add_argument('--all', action='store_true', help='创建所有测试模型')
    parser.add_argument('--validate', action='store_true', help='创建后验证模型')
    args = parser.parse_args()

    if not any([args.wind, args.pv, args.hybrid, args.all]):
        args.all = True  # 默认创建所有

    print("\n" + "="*60)
    print("CloudPSS 新能源测试算例创建工具")
    print("="*60)

    if not setup_auth():
        sys.exit(1)

    created_models = []

    try:
        # 创建风电模型
        if args.wind or args.all:
            wind_rid = create_wind_model()
            if wind_rid:
                created_models.append(('IEEE39 + Wind', wind_rid))

        # 创建光伏模型
        if args.pv or args.all:
            pv_rid = create_pv_model()
            if pv_rid:
                created_models.append(('IEEE39 + PV', pv_rid))

        # 创建混合模型
        if args.hybrid or args.all:
            hybrid_rid = create_hybrid_model()
            if hybrid_rid:
                created_models.append(('IEEE39 + Hybrid', hybrid_rid))

        # 验证模型
        if args.validate and created_models:
            logger.info("\n" + "="*60)
            logger.info("验证创建的模型")
            logger.info("="*60)
            for name, rid in created_models:
                validate_model(rid, name)

        # 生成报告
        print("\n" + "="*60)
        print("测试算例创建完成")
        print("="*60)
        print(f"\n共创建 {len(created_models)} 个测试模型:")
        for name, rid in created_models:
            print(f"  - {name}: {rid}")
        print("\n固定分支名:")
        if args.wind or args.all:
            print("  - test_ieee39_wind (风电)")
        if args.pv or args.all:
            print("  - test_ieee39_pv (光伏)")
        if args.hybrid or args.all:
            print("  - test_ieee39_hybrid (混合新能源)")
        print("\n这些模型可用于后续技能开发和测试。")

    except Exception as e:
        logger.error(f"创建失败: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
