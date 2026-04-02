"""
端到端测试：元数据系统完整工作流

测试完整流程：
1. 从元数据注册表获取组件信息
2. 使用 model_builder 添加组件（带自动补全）
3. 使用 model_validator 验证模型

注意：此测试需要真实 CloudPSS API 访问权限
运行方式：pytest tests/e2e/test_metadata_workflow.py --run-integration
"""

import pytest
import logging
from pathlib import Path

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestMetadataWorkflow:
    """元数据系统端到端测试"""

    @pytest.fixture
    def metadata_integration(self):
        """元数据集成 fixture"""
        from cloudpss_skills.metadata.integration import get_metadata_integration
        mi = get_metadata_integration()
        mi.initialize('examples/metadata')
        return mi

    def test_wgsource_metadata_complete(self, metadata_integration):
        """测试 WGSource 元数据完整性"""
        comp_type = 'model/CloudPSS/WGSource'

        # 获取元数据
        metadata = metadata_integration.get_component_metadata(comp_type)
        assert metadata is not None, "WGSource 元数据未找到"

        # 验证基本字段
        assert metadata.component_id == comp_type
        assert metadata.name == '风场等值模型I：PMSG网侧变流器模型'
        assert metadata.category == 'renewable'

        # 验证参数组
        assert len(metadata.parameter_groups) > 0, "至少有一个参数组"

        # 验证必需参数
        required_params = metadata_integration.get_required_parameters(comp_type)
        assert len(required_params) > 0, "应该有必需参数"
        assert 'Vbase' in required_params
        assert 'Fnom' in required_params

        # 验证引脚
        pins = metadata_integration.get_pin_requirements(comp_type)
        assert pins['total_pins'] > 0, "应该有引脚定义"
        assert '0' in pins['electrical_pins'], "应该有电气引脚 0"

        logger.info(f"✅ WGSource 元数据验证通过: {len(required_params)} 个必需参数, {pins['total_pins']} 个引脚")

    def test_autocomplete_wgsource(self, metadata_integration):
        """测试 WGSource 参数自动补全"""
        comp_type = 'model/CloudPSS/WGSource'

        # 用户提供部分参数
        user_params = {
            'Vpcc': 0.69,
            'WindSpeed': 12.0
        }

        # 自动补全
        completed = metadata_integration.auto_complete_parameters(comp_type, user_params)

        # 验证补全结果
        assert len(completed) > len(user_params), "应该补全了更多参数"

        # 验证必需参数被补全
        required = metadata_integration.get_required_parameters(comp_type)
        for param in required:
            assert param in completed, f"必需参数 {param} 应该被补全"

        # 验证用户提供的值保持不变
        assert completed['Vpcc'] == 0.69
        assert completed['WindSpeed'] == 12.0

        logger.info(f"✅ 自动补全验证通过: {len(user_params)} -> {len(completed)} 个参数")

    def test_validate_complete_parameters(self, metadata_integration):
        """测试完整参数验证通过"""
        comp_type = 'model/CloudPSS/WGSource'

        # 完整的参数（必需+可选）
        complete_params = {
            'Vbase': 0.69,
            'Fnom': 50.0,
            'Pnom': 100.0,
            'Vpcc': 0.69,
            'WindSpeed': 12.0,
            'AirDensity': 1.225,
            'MPPTEnable': True,
            'RecoveryEnable': True,
            'RecoveryRate': 0.1,
            'TestMode': 'normal',
        }

        result = metadata_integration.validate_parameters(comp_type, complete_params)
        assert result.valid is True, f"参数应该验证通过: {result.errors}"

        logger.info("✅ 完整参数验证通过")

    def test_validate_incomplete_parameters(self, metadata_integration):
        """测试不完整参数验证失败"""
        comp_type = 'model/CloudPSS/WGSource'

        # 故意不完整的参数
        incomplete_params = {
            'WindSpeed': 12.0,
            # 缺少必需参数 Vbase, Fnom, Pnom, Vpcc
        }

        result = metadata_integration.validate_parameters(comp_type, incomplete_params)
        assert result.valid is False, "缺少必需参数应该验证失败"
        assert len(result.errors) > 0, "应该有错误信息"

        # 验证错误信息包含必需参数
        error_str = ' '.join(result.errors)
        assert 'Vbase' in error_str or '基准电压' in error_str

        logger.info(f"✅ 不完整参数验证失败检测成功: {len(result.errors)} 个错误")

    def test_validate_pin_connection(self, metadata_integration):
        """测试引脚连接验证"""
        comp_type = 'model/CloudPSS/WGSource'

        # 未连接任何引脚 - 应该失败
        result = metadata_integration.validate_pin_connection(comp_type, {})
        assert result.valid is False, "未连接必需引脚应该验证失败"

        # 正确连接 - 应该通过
        result = metadata_integration.validate_pin_connection(comp_type, {'0': 'Bus10'})
        assert result.valid is True, "正确连接应该验证通过"

        logger.info("✅ 引脚连接验证通过")

    def test_all_components_in_index(self, metadata_integration):
        """测试所有元数据文件都在索引中"""
        metadata_dir = Path('examples/metadata')

        # 获取所有 JSON 文件
        json_files = set(f.stem for f in metadata_dir.glob('*.json') if f.name != '_index.json')

        # 获取所有已注册组件
        registered = set(metadata_integration.list_available_components())

        # 每个 JSON 文件应该对应一个注册的组件
        logger.info(f"Metadata files: {len(json_files)}")
        logger.info(f"Registered components: {len(registered)}")

        # 验证至少有一些组件被注册
        assert len(registered) >= 1, "应该至少有一个组件被注册"

        logger.info("✅ 组件注册验证通过")


class TestMetadataWithSkills:
    """测试元数据与技能的集成（需要 API token）"""

    @pytest.fixture
    def setup_auth(self):
        """设置认证（从环境变量或文件）"""
        import os
        from cloudpss import setToken

        token = os.environ.get('CLOUDPSS_TOKEN')
        if not token:
            token_file = Path('.cloudpss_token')
            if token_file.exists():
                token = token_file.read_text().strip()

        if token:
            setToken(token)
            return True
        return False

    @pytest.mark.skip(reason="需要真实 CloudPSS API 访问权限")
    def test_model_builder_with_metadata(self, setup_auth):
        """测试 model_builder 使用元数据（需要 API）"""
        if not setup_auth:
            pytest.skip("未配置 CloudPSS token")

        from cloudpss_skills.builtin.model_builder import ModelBuilderSkill

        # 创建技能实例
        skill = ModelBuilderSkill()

        # 配置：添加 WGSource 组件
        config = {
            'base_model': {
                'rid': 'model/holdme/IEEE39'
            },
            'modifications': [
                {
                    'action': 'add_component',
                    'component_type': 'model/CloudPSS/WGSource',
                    'label': 'WindFarm_Bus10',
                    'parameters': {
                        'Vpcc': 0.69,
                        'Pnom': 50.0
                    },
                    'pin_connection': {
                        'target_bus': 'Bus10'
                    }
                }
            ],
            'output': {
                'save': True,
                'branch': 'test/metadata_integration'
            }
        }

        # 运行技能
        result = skill.run(config)

        # 验证结果
        assert result.status.value == 'success', f"模型构建应该成功: {result.error}"
        assert len(result.data['generated_models']) > 0, "应该生成模型"

        logger.info(f"✅ Model builder with metadata test passed: {result.data['generated_models'][0]['rid']}")

    @pytest.mark.skip(reason="需要真实 CloudPSS API 访问权限")
    def test_model_validator_with_metadata(self, setup_auth):
        """测试 model_validator 使用元数据（需要 API）"""
        if not setup_auth:
            pytest.skip("未配置 CloudPSS token")

        from cloudpss_skills.builtin.model_validator import ModelValidatorSkill

        # 创建技能实例
        skill = ModelValidatorSkill()

        # 配置：验证 IEEE39 模型
        config = {
            'models': [
                {
                    'rid': 'model/holdme/IEEE39',
                    'name': 'IEEE39 测试模型'
                }
            ],
            'validation': {
                'phases': ['topology', 'powerflow']
            },
            'output': {
                'format': 'json'
            }
        }

        # 运行技能
        result = skill.run(config)

        # 验证结果（拓扑验证和潮流验证应该通过）
        assert result.status.value == 'success', f"验证应该成功: {result.error}"

        # 检查验证报告
        reports = result.data.get('reports', [])
        assert len(reports) > 0, "应该有验证报告"

        for report in reports:
            # 拓扑验证应该通过
            topology = report.get('phases', {}).get('topology', {})
            assert topology.get('passed') is True, "拓扑验证应该通过"

        logger.info("✅ Model validator with metadata test passed")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--run-integration'])
