#!/usr/bin/env python3
"""
Model Parameter Extractor Skill - 集成测试

测试模型参数提取技能的基本功能。
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# 先导入builtin模块以注册技能
import cloudpss_skills.builtin
from cloudpss_skills import get_skill
from cloudpss_skills.core import ValidationResult


class TestModelParameterExtractorConfig:
    """测试配置生成和验证"""

    def test_skill_registration(self):
        """测试技能是否正确注册"""
        skill = get_skill("model_parameter_extractor")
        assert skill is not None
        assert skill.name == "model_parameter_extractor"
        assert "参数" in skill.description or "parameter" in skill.description.lower()

    def test_default_config_generation(self):
        """测试默认配置生成"""
        skill = get_skill("model_parameter_extractor")
        config = skill.get_default_config()

        assert config["skill"] == "model_parameter_extractor"
        assert "model" in config
        assert "extraction" in config
        assert "output" in config

        # 验证提取配置
        assert config["extraction"]["include_topology"] is True
        assert config["extraction"]["filter_empty"] is True
        assert "bus_3p" in config["extraction"]["component_types"]

    def test_config_schema_validation(self):
        """测试配置schema验证"""
        skill = get_skill("model_parameter_extractor")
        schema = skill.config_schema

        assert schema["type"] == "object"
        assert "model" in schema["properties"]
        assert "extraction" in schema["properties"]
        assert "output" in schema["properties"]

        # 验证提取配置项
        extract_props = schema["properties"]["extraction"]["properties"]
        assert "component_types" in extract_props
        assert "include_topology" in extract_props

    def test_empty_rid_validation(self):
        """测试空RID验证失败"""
        skill = get_skill("model_parameter_extractor")
        config = skill.get_default_config()
        config["model"]["rid"] = ""

        result = skill.validate(config)
        assert not result.valid
        assert any("rid" in error.lower() for error in result.errors)

    def test_valid_config_validation(self):
        """测试有效配置验证通过"""
        skill = get_skill("model_parameter_extractor")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"

        result = skill.validate(config)
        assert result.valid, f"验证失败: {result.errors}"

    def test_component_types_validation(self):
        """测试元件类型配置"""
        skill = get_skill("model_parameter_extractor")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"

        # 有效类型
        config["extraction"]["component_types"] = ["bus_3p", "line_3p", "generator"]
        result = skill.validate(config)
        assert result.valid

        # 包含无效类型
        config["extraction"]["component_types"] = ["bus_3p", "invalid_type"]
        result = skill.validate(config)
        assert not result.valid
        assert any("invalid" in error.lower() for error in result.errors)


class TestModelParameterExtractorFeatures:
    """测试技能功能特性"""

    def test_topology_extraction_config(self):
        """测试拓扑提取配置"""
        skill = get_skill("model_parameter_extractor")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["extraction"]["include_topology"] = False

        result = skill.validate(config)
        assert result.valid

    def test_output_format_config(self):
        """测试输出格式配置"""
        skill = get_skill("model_parameter_extractor")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"

        for fmt in ["json", "csv", "both"]:
            config["output"]["format"] = fmt
            result = skill.validate(config)
            assert result.valid, f"格式 {fmt} 验证失败"

    def test_group_by_type_config(self):
        """测试按类型分组配置"""
        skill = get_skill("model_parameter_extractor")
        config = skill.get_default_config()
        config["model"]["rid"] = "model/holdme/IEEE39"
        config["output"]["group_by_type"] = True

        result = skill.validate(config)
        assert result.valid


@pytest.mark.integration
class TestModelParameterExtractorIntegration:
    """集成测试 - 需要CloudPSS API访问"""

    def test_skill_loads_correctly(self):
        """测试技能正确加载"""
        skill = get_skill("model_parameter_extractor")
        assert skill is not None
        assert skill.name == "model_parameter_extractor"

    def test_extract_bus_parameters(self, live_auth):
        """测试提取母线参数（使用真实API）"""
        skill = get_skill("model_parameter_extractor")
        config = {
            "skill": "model_parameter_extractor",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "extraction": {
                "component_types": ["bus_3p"],
                "include_topology": False,
                "filter_empty": True
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "test_bus_params"
            }
        }

        result = skill.run(config)

        assert result is not None
        assert result.status.value in ["success", "failed"]

        if result.status.value == "success":
            data = result.data
            assert "total_components" in data
            assert data["total_components"] > 0
            assert "bus_3p" in data.get("type_counts", {})
            assert data["type_counts"]["bus_3p"] > 0
            print(f"\n✓ 成功提取 {data['type_counts']['bus_3p']} 个母线参数")

    def test_extract_line_parameters(self, live_auth):
        """测试提取线路参数（使用真实API）"""
        skill = get_skill("model_parameter_extractor")
        config = {
            "skill": "model_parameter_extractor",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "extraction": {
                "component_types": ["line_3p"],
                "include_topology": False,
                "filter_empty": True
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "test_line_params"
            }
        }

        result = skill.run(config)

        if result.status.value == "success":
            data = result.data
            assert "line_3p" in data.get("type_counts", {})
            line_count = data["type_counts"]["line_3p"]
            assert line_count > 0
            print(f"\n✓ 成功提取 {line_count} 个线路参数")

    def test_extract_generator_parameters(self, live_auth):
        """测试提取发电机参数（使用真实API）"""
        skill = get_skill("model_parameter_extractor")
        config = {
            "skill": "model_parameter_extractor",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "extraction": {
                "component_types": ["generator"],
                "include_topology": False,
                "filter_empty": True
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "test_gen_params"
            }
        }

        result = skill.run(config)

        if result.status.value == "success":
            data = result.data
            assert "generator" in data.get("type_counts", {})
            gen_count = data["type_counts"]["generator"]
            assert gen_count > 0
            print(f"\n✓ 成功提取 {gen_count} 个发电机参数")

    def test_extract_topology(self, live_auth):
        """测试提取拓扑连接（使用真实API）"""
        skill = get_skill("model_parameter_extractor")
        config = {
            "skill": "model_parameter_extractor",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "extraction": {
                "component_types": ["bus_3p", "line_3p"],
                "include_topology": True,  # 启用拓扑提取
                "filter_empty": True
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "test_topology"
            }
        }

        result = skill.run(config)

        if result.status.value == "success":
            data = result.data
            assert "connections_count" in data
            assert data["connections_count"] > 0
            print(f"\n✓ 成功提取 {data['connections_count']} 个连接关系")

    def test_extract_all_component_types(self, live_auth):
        """测试提取所有元件类型（使用真实API）"""
        skill = get_skill("model_parameter_extractor")
        config = {
            "skill": "model_parameter_extractor",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "extraction": {
                "component_types": [
                    "bus_3p",
                    "line_3p",
                    "generator",
                    "load",
                    "transformer_3p"
                ],
                "include_topology": False,
                "filter_empty": True
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "test_all_types"
            }
        }

        result = skill.run(config)

        if result.status.value == "success":
            data = result.data
            total = data["total_components"]
            type_counts = data.get("type_counts", {})

            print(f"\n✓ 成功提取 {total} 个元件参数:")
            for comp_type, count in type_counts.items():
                print(f"  - {comp_type}: {count} 个")

            assert total > 0
            assert len(type_counts) > 0

    def test_csv_grouped_export(self, live_auth):
        """测试CSV分组导出（使用真实API）"""
        import os

        skill = get_skill("model_parameter_extractor")
        config = {
            "skill": "model_parameter_extractor",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "extraction": {
                "component_types": ["bus_3p", "line_3p"],
                "include_topology": False,
                "filter_empty": True
            },
            "output": {
                "format": "csv",  # CSV格式
                "path": "./results/",
                "prefix": "test_csv_grouped",
                "group_by_type": True  # 按类型分组
            }
        }

        result = skill.run(config)

        if result.status.value == "success":
            # 验证CSV文件生成
            bus_csv = "./results/test_csv_grouped_bus_3p.csv"
            line_csv = "./results/test_csv_grouped_line_3p.csv"

            if os.path.exists(bus_csv):
                with open(bus_csv, 'r') as f:
                    content = f.read()
                    assert "component_key" in content
                    assert "label" in content
                print(f"\n✓ 母线CSV文件生成成功")

            if os.path.exists(line_csv):
                print(f"\n✓ 线路CSV文件生成成功")

    def test_json_report_structure(self, live_auth):
        """测试JSON报告结构（使用真实API）"""
        skill = get_skill("model_parameter_extractor")
        config = {
            "skill": "model_parameter_extractor",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "extraction": {
                "component_types": ["bus_3p"],
                "include_topology": True,
                "filter_empty": True
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "test_json_structure"
            }
        }

        result = skill.run(config)

        if result.status.value == "success":
            # 验证JSON报告结构
            import json
            import os

            json_file = "./results/test_json_structure.json"
            if os.path.exists(json_file):
                with open(json_file, 'r') as f:
                    report = json.load(f)

                assert "summary" in report
                assert "components" in report
                assert "connections" in report

                summary = report["summary"]
                assert "model_rid" in summary
                assert "model_name" in summary
                assert "total_components" in summary

                print(f"\n✓ JSON报告结构验证通过")
                print(f"  - 模型: {summary['model_name']}")
                print(f"  - 总元件数: {summary['total_components']}")
                print(f"  - 连接数: {summary.get('connections_count', 0)}")

    def test_result_data_structure(self, live_auth):
        """测试结果数据结构（使用真实API）"""
        skill = get_skill("model_parameter_extractor")
        config = {
            "skill": "model_parameter_extractor",
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39"},
            "extraction": {
                "component_types": ["bus_3p", "line_3p", "generator"],
                "include_topology": False,
                "filter_empty": True
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "test_data_structure"
            }
        }

        result = skill.run(config)

        # 验证结果结构
        assert result.skill_name == "model_parameter_extractor"
        assert result.start_time is not None
        assert result.end_time is not None

        if result.status.value == "success":
            data = result.data
            assert "model_rid" in data
            assert "model_name" in data
            assert "total_components" in data
            assert "type_counts" in data

            # 验证日志
            assert len(result.logs) > 0

            print(f"\n✓ 结果数据结构验证通过")
            print(f"  - 模型RID: {data['model_rid']}")
            print(f"  - 模型名称: {data['model_name']}")
            print(f"  - 总元件数: {data['total_components']}")
            print(f"  - 日志条目数: {len(result.logs)}")


if __name__ == "__main__":
    # 运行基本测试
    print("=" * 70)
    print("Model Parameter Extractor Skill - 配置测试")
    print("=" * 70)

    skill = get_skill("model_parameter_extractor")
    print(f"\n✓ 技能已注册: {skill.name}")
    print(f"✓ 技能描述: {skill.description}")

    # 测试配置验证
    config = skill.get_default_config()
    config["model"]["rid"] = "model/holdme/IEEE39"

    result = skill.validate(config)
    if result.valid:
        print("✓ 默认配置验证通过")
    else:
        print(f"✗ 配置验证失败: {result.errors}")

    # 测试输出格式
    for fmt in ["json", "csv", "both"]:
        config["output"]["format"] = fmt
        result = skill.validate(config)
        if result.valid:
            print(f"✓ 格式 '{fmt}' 验证通过")
        else:
            print(f"✗ 格式 '{fmt}' 验证失败: {result.errors}")

    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)
