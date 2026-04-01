#!/usr/bin/env python3
"""
批量验证测试算例

验证所有 model_builder 创建的测试模型
"""

from cloudpss_skills.builtin.model_validator import ModelValidatorSkill
from cloudpss_skills.core.base import SkillStatus
import json


def validate_all_test_models():
    """验证所有测试算例"""

    # 所有测试模型
    test_models = [
        # 光伏模型
        {"rid": "model/holdme/test_IEEE39_with_PV_50MW", "base_rid": "model/holdme/IEEE39", "name": "光伏50MW"},
        {"rid": "model/holdme/test_IEEE39_with_PV_100MW", "base_rid": "model/holdme/IEEE39", "name": "光伏100MW"},
        {"rid": "model/holdme/test_IEEE39_with_PV_150MW", "base_rid": "model/holdme/IEEE39", "name": "光伏150MW"},

        # 风电模型
        {"rid": "model/holdme/test_IEEE39_with_Wind_50MW", "base_rid": "model/holdme/IEEE39", "name": "风电50MW"},
        {"rid": "model/holdme/test_IEEE39_with_Wind_100MW", "base_rid": "model/holdme/IEEE39", "name": "风电100MW"},
        {"rid": "model/holdme/test_IEEE39_with_Wind_WGSource", "base_rid": "model/holdme/IEEE39", "name": "WGSource风电"},

        # 保护模型
        {"rid": "model/holdme/test_IEEE39_with_DifferentialProtection", "base_rid": "model/holdme/IEEE39", "name": "差动保护"},
        {"rid": "model/holdme/test_IEEE39_with_OverCurrentProtection", "base_rid": "model/holdme/IEEE39", "name": "过流保护"},
        {"rid": "model/holdme/test_IEEE39_with_ZeroSeqProtection", "base_rid": "model/holdme/IEEE39", "name": "零序保护"},

        # 线路修改
        {"rid": "model/holdme/test_IEEE39_Line_Length_150", "base_rid": "model/holdme/IEEE39", "name": "线路150km"},
        {"rid": "model/holdme/test_IEEE39_Line_Length_200", "base_rid": "model/holdme/IEEE39", "name": "线路200km"},

        # 新母线
        {"rid": "model/holdme/test_IEEE39_New_Bus", "base_rid": "model/holdme/IEEE39", "name": "新增母线"},
    ]

    skill = ModelValidatorSkill()

    config = {
        'auth': {'token_file': '.cloudpss_token'},
        'models': test_models,
        'validation': {
            'phases': ['topology', 'powerflow', 'parameter'],
            'timeout': 300,
            'powerflow_tolerance': 1e-6
        },
        'output': {
            'format': 'console'
        }
    }

    print("=" * 70)
    print("批量验证所有测试算例")
    print("=" * 70)
    print(f"待验证模型: {len(test_models)} 个")
    print()

    result = skill.run(config)

    if result.status == SkillStatus.SUCCESS:
        print("\n" + "=" * 70)
        print("验证汇总")
        print("=" * 70)
        print(f"总计: {result.data['total_models']} 个")
        print(f"通过: {result.data['passed']} 个 ✅")
        print(f"失败: {result.data['failed']} 个 ❌")

        # 分类统计
        categories = {
            "光伏": ["光伏50MW", "光伏100MW", "光伏150MW"],
            "风电": ["风电50MW", "风电100MW", "WGSource风电"],
            "保护": ["差动保护", "过流保护", "零序保护"],
            "线路": ["线路150km", "线路200km"],
            "其他": ["新增母线"]
        }

        print("\n分类统计:")
        for cat, names in categories.items():
            cat_passed = sum(1 for r in result.data['reports']
                           if r['model_name'] in names and r['passed'])
            cat_total = len(names)
            print(f"  {cat}: {cat_passed}/{cat_total} 通过")

        # 保存详细报告
        with open("validation_results.json", "w", encoding="utf-8") as f:
            json.dump(result.data, f, indent=2, ensure_ascii=False)
        print("\n详细报告已保存: validation_results.json")

        return result.data['passed'] == result.data['total_models']
    else:
        print(f"验证失败: {result.error}")
        return False


if __name__ == "__main__":
    success = validate_all_test_models()
    exit(0 if success else 1)
