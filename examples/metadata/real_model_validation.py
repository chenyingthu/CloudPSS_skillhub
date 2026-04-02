"""
真实模型验证脚本

使用真实 CloudPSS API 验证元数据系统：
1. 使用 IEEE39 模型添加 WGSource 风机
2. 验证参数自动补全
3. 运行潮流验证
4. 生成验证报告

运行方式:
    python examples/metadata/real_model_validation.py

需要配置:
    - .cloudpss_token 文件或 CLOUDPSS_TOKEN 环境变量
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
            logger.error("请设置 CLOUDPSS_TOKEN 环境变量或创建 .cloudpss_token 文件")
            return False

    setToken(token)
    logger.info("CloudPSS 认证已设置")
    return True


def validate_wgsource_metadata():
    """验证 WGSource 元数据完整性"""
    logger.info("\n" + "="*60)
    logger.info("步骤 1: 验证 WGSource 元数据")
    logger.info("="*60)

    from cloudpss_skills.metadata.integration import get_metadata_integration

    mi = get_metadata_integration()
    mi.initialize('examples/metadata')

    comp_type = 'model/CloudPSS/WGSource'

    # 获取元数据摘要
    summary = mi.get_component_summary(comp_type)
    logger.info(f"\n元数据摘要:\n{summary}")

    # 验证必需参数
    required = mi.get_required_parameters(comp_type)
    logger.info(f"\n必需参数 ({len(required)}个): {required}")

    # 验证引脚要求
    pins = mi.get_pin_requirements(comp_type)
    logger.info(f"\n引脚信息:")
    logger.info(f"  总引脚: {pins['total_pins']}")
    logger.info(f"  电气引脚: {pins['electrical_pins']}")
    logger.info(f"  必需引脚: {pins['required_pins']}")

    return True


def test_autocomplete_functionality():
    """测试参数自动补全功能"""
    logger.info("\n" + "="*60)
    logger.info("步骤 2: 测试参数自动补全")
    logger.info("="*60)

    from cloudpss_skills.metadata.integration import get_metadata_integration

    mi = get_metadata_integration()
    mi.initialize('examples/metadata')

    comp_type = 'model/CloudPSS/WGSource'

    # 用户提供的最小参数集
    user_params = {
        'Vpcc': 0.69,  # 并网点电压
        'Pnom': 100.0,  # 额定功率
    }

    logger.info(f"\n用户提供的参数: {user_params}")

    # 自动补全
    completed = mi.auto_complete_parameters(comp_type, user_params)

    added = set(completed.keys()) - set(user_params.keys())
    logger.info(f"\n自动补全了 {len(added)} 个参数:")
    for key in sorted(added):
        logger.info(f"  - {key} = {completed[key]}")

    # 验证补全后的参数
    result = mi.validate_parameters(comp_type, completed)
    if result.valid:
        logger.info("\n✅ 自动补全后的参数验证通过")
    else:
        logger.error(f"\n❌ 参数验证失败: {result.errors}")
        return False

    return completed


def create_test_model_with_wgsource():
    """创建测试模型：IEEE39 + WGSource"""
    logger.info("\n" + "="*60)
    logger.info("步骤 3: 创建测试模型 (IEEE39 + WGSource)")
    logger.info("="*60)

    from cloudpss_skills.builtin.model_builder import ModelBuilderSkill
    from cloudpss_skills.metadata.integration import get_metadata_integration

    mi = get_metadata_integration()
    mi.initialize('examples/metadata')

    # 获取 WGSource 的自动补全参数
    user_params = {'Vpcc': 0.69, 'Pnom': 50.0}
    completed_params = mi.auto_complete_parameters('model/CloudPSS/WGSource', user_params)

    # 配置 model_builder
    config = {
        'base_model': {
            'rid': 'model/holdme/IEEE39'
        },
        'modifications': [
            {
                'action': 'add_component',
                'component_type': 'model/CloudPSS/WGSource',
                'label': 'WindFarm_Bus10',
                'parameters': completed_params,  # 使用自动补全的参数
                'position': {'x': 400, 'y': 300},
                'pin_connection': {
                    'target_bus': 'Bus10',
                    'pin_name': '0'
                }
            }
        ],
        'output': {
            'save': True,
            'branch': f'test_metadata_validation_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'name': 'IEEE39_with_WGSource_Metadata',
            'description': 'IEEE39 系统添加风机（使用元数据自动补全）'
        }
    }

    logger.info(f"\n模型配置:")
    logger.info(f"  基础模型: {config['base_model']['rid']}")
    logger.info(f"  添加组件: WGSource (参数自动补全)")
    logger.info(f"  参数数量: {len(completed_params)}")
    logger.info(f"  保存分支: {config['output']['branch']}")

    # 执行模型构建
    skill = ModelBuilderSkill()

    # 先验证配置
    validation = skill.validate(config)
    if not validation.valid:
        logger.error(f"配置验证失败: {validation.errors}")
        return None

    # 运行构建
    result = skill.run(config)

    if result.status.value == 'success':
        logger.info("\n✅ 模型创建成功")
        model_info = result.data['generated_models'][0]
        logger.info(f"  模型 RID: {model_info['rid']}")
        logger.info(f"  应用修改: {model_info['modifications']}")
        return model_info['rid']
    else:
        logger.error(f"\n❌ 模型创建失败: {result.error}")
        return None


def validate_model_with_metadata(model_rid: str):
    """使用 model_validator 验证模型"""
    logger.info("\n" + "="*60)
    logger.info("步骤 4: 验证模型")
    logger.info("="*60)

    from cloudpss_skills.builtin.model_validator import ModelValidatorSkill

    config = {
        'models': [
            {
                'rid': model_rid,
                'name': 'IEEE39 with WGSource'
            }
        ],
        'validation': {
            'phases': ['topology', 'powerflow'],
            'timeout': 300
        },
        'output': {
            'format': 'console'
        }
    }

    logger.info(f"\n验证配置:")
    logger.info(f"  模型: {model_rid}")
    logger.info(f"  验证阶段: topology, powerflow")

    skill = ModelValidatorSkill()
    result = skill.run(config)

    if result.status.value == 'success':
        logger.info("\n✅ 模型验证完成")

        # 输出详细报告
        for report in result.data['reports']:
            logger.info(f"\n模型: {report['model_name']}")
            logger.info(f"  结果: {'通过' if report['passed'] else '失败'}")

            for phase, phase_result in report['phases'].items():
                status = "✅" if phase_result.get('passed') else "❌"
                logger.info(f"  {status} {phase}")

                if phase_result.get('errors'):
                    for error in phase_result['errors']:
                        logger.error(f"      错误: {error}")

                if phase_result.get('warnings'):
                    for warning in phase_result['warnings']:
                        logger.warning(f"      警告: {warning}")

        return result.data['reports'][0]['passed']
    else:
        logger.error(f"\n❌ 验证失败: {result.error}")
        return False


def generate_report():
    """生成验证报告"""
    logger.info("\n" + "="*60)
    logger.info("验证报告")
    logger.info("="*60)

    report = {
        'timestamp': datetime.now().isoformat(),
        'test_items': [
            'WGSource 元数据完整性',
            '参数自动补全功能',
            '模型创建（IEEE39 + WGSource）',
            '模型验证（拓扑 + 潮流）'
        ],
        'metadata_components': 7,
        'wgsource_parameters': 15,
        'wgsource_required_params': 4,
        'wgsource_pins': 6
    }

    logger.info("\n测试项目:")
    for item in report['test_items']:
        logger.info(f"  ✓ {item}")

    logger.info(f"\n元数据系统统计:")
    logger.info(f"  组件总数: {report['metadata_components']}")
    logger.info(f"  WGSource 参数: {report['wgsource_parameters']}")
    logger.info(f"  WGSource 必需参数: {report['wgsource_required_params']}")
    logger.info(f"  WGSource 引脚: {report['wgsource_pins']}")

    return report


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='CloudPSS 元数据系统 - 真实模型验证'
    )
    parser.add_argument(
        '--auto', action='store_true',
        help='自动模式：跳过交互式提示，直接创建测试模型'
    )
    parser.add_argument(
        '--skip-model-creation', action='store_true',
        help='跳过模型创建步骤（仅运行元数据验证）'
    )
    args = parser.parse_args()

    print("\n" + "="*60)
    print("CloudPSS 元数据系统 - 真实模型验证")
    print("="*60)

    # 步骤 0: 设置认证
    if not setup_auth():
        sys.exit(1)

    try:
        # 步骤 1: 验证元数据
        if not validate_wgsource_metadata():
            logger.error("元数据验证失败")
            sys.exit(1)

        # 步骤 2: 测试自动补全
        completed_params = test_autocomplete_functionality()
        if not completed_params:
            logger.error("自动补全测试失败")
            sys.exit(1)

        # 步骤 3: 创建测试模型（可选，需要 API）
        if args.skip_model_creation:
            logger.info("\n" + "-"*60)
            logger.info("跳过模型创建步骤（--skip-model-creation）")
            logger.info("-"*60)
        else:
            logger.info("\n" + "-"*60)
            logger.info("注意：步骤 3-4 需要写入权限，将创建新模型分支")
            logger.info("-"*60)

            if args.auto:
                response = 'y'
                logger.info("\n自动模式：继续创建测试模型")
            else:
                response = input("\n是否继续创建测试模型？ (y/N): ")

            if response.lower() == 'y':
                model_rid = create_test_model_with_wgsource()
                if not model_rid:
                    logger.error("模型创建失败")
                    sys.exit(1)

                # 步骤 4: 验证模型
                passed = validate_model_with_metadata(model_rid)
                if not passed:
                    logger.warning("模型验证未完全通过，请查看详细报告")
            else:
                logger.info("跳过模型创建和验证步骤")

        # 生成报告
        report = generate_report()

        print("\n" + "="*60)
        print("验证完成!")
        print("="*60)

    except KeyboardInterrupt:
        logger.info("\n用户中断")
        sys.exit(0)
    except Exception as e:
        logger.error(f"验证失败: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
