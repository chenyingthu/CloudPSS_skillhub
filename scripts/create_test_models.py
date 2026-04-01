#!/usr/bin/env python3
"""
创建测试算例脚本

为后续技能测试和开发准备标准测试算例。

运行: python scripts/create_test_models.py
"""

import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cloudpss_skills.builtin.model_builder import ModelBuilderSkill
from cloudpss_skills.core.base import SkillStatus


def create_test_models():
    """创建测试算例"""

    skill = ModelBuilderSkill()

    # 定义要创建的测试算例
    test_cases = [
        # 1. 光伏接入模型 - 使用正确的RID
        {
            "name": "IEEE39_with_PV_50MW",
            "description": "IEEE39系统母线10接入50MW光伏电站",
            "modifications": [
                {
                    "action": "add_component",
                    "component_type": "model/CloudPSS/PVStation",  # 正确的RID
                    "label": "PV_Bus10_50MW",
                    "parameters": {
                        "额定容量": 50,
                        "有功功率参考值": 0.8,
                        "功率因数": 1.0
                    },
                    "position": {"x": 400, "y": 300}
                }
            ]
        },
        {
            "name": "IEEE39_with_PV_100MW",
            "description": "IEEE39系统母线10接入100MW光伏电站",
            "modifications": [
                {
                    "action": "add_component",
                    "component_type": "model/CloudPSS/PVStation",
                    "label": "PV_Bus10_100MW",
                    "parameters": {
                        "额定容量": 100,
                        "有功功率参考值": 0.8,
                        "功率因数": 1.0
                    },
                    "position": {"x": 400, "y": 300}
                }
            ]
        },
        {
            "name": "IEEE39_with_PV_150MW",
            "description": "IEEE39系统母线10接入150MW光伏电站",
            "modifications": [
                {
                    "action": "add_component",
                    "component_type": "model/CloudPSS/PVStation",
                    "label": "PV_Bus10_150MW",
                    "parameters": {
                        "额定容量": 150,
                        "有功功率参考值": 0.8,
                        "功率因数": 1.0
                    },
                    "position": {"x": 400, "y": 300}
                }
            ]
        },

        # 2. 风电接入模型 - 使用正确的RID
        {
            "name": "IEEE39_with_Wind_50MW",
            "description": "IEEE39系统母线20接入50MW风电场",
            "modifications": [
                {
                    "action": "add_component",
                    "component_type": "model/CloudPSS/DFIG_WindFarm_Equivalent_Model",  # DFIG风电场等值模型
                    "label": "Wind_Bus20_50MW",
                    "parameters": {
                        "额定容量": 50,
                        "有功功率参考值": 0.9,
                        "风速": 12
                    },
                    "position": {"x": 600, "y": 400}
                }
            ]
        },
        {
            "name": "IEEE39_with_Wind_100MW",
            "description": "IEEE39系统母线20接入100MW风电场",
            "modifications": [
                {
                    "action": "add_component",
                    "component_type": "model/CloudPSS/DFIG_WindFarm_Equivalent_Model",
                    "label": "Wind_Bus20_100MW",
                    "parameters": {
                        "额定容量": 100,
                        "有功功率参考值": 0.9,
                        "风速": 12
                    },
                    "position": {"x": 600, "y": 400}
                }
            ]
        },
        {
            "name": "IEEE39_with_Wind_WGSource",
            "description": "IEEE39系统母线30接入风电场(WGSource模型)",
            "modifications": [
                {
                    "action": "add_component",
                    "component_type": "model/CloudPSS/WGSource",  # 风电场电源模型
                    "label": "Wind_WGSource_Bus30",
                    "parameters": {
                        "额定容量": 80,
                        "有功功率参考值": 0.85
                    },
                    "position": {"x": 500, "y": 500}
                }
            ]
        },

        # 3. 保护配置模型 - 使用component_catalog发现的真实RID
        {
            "name": "IEEE39_with_DifferentialProtection",
            "description": "IEEE39系统配置纵联差动保护",
            "modifications": [
                {
                    "action": "add_component",
                    "component_type": "model/CloudPSS/DifferentialProtection",  # 纵联差动保护
                    "label": "DiffRelay_LINE_1_2",
                    "parameters": {},  # 使用默认参数
                    "position": {"x": 500, "y": 350}
                }
            ]
        },
        {
            "name": "IEEE39_with_OverCurrentProtection",
            "description": "IEEE39系统配置复压过流保护",
            "modifications": [
                {
                    "action": "add_component",
                    "component_type": "model/CloudPSS/CompoundVoltageOverCurrentProtection",  # 复压过流保护
                    "label": "OC_Relay_Bus10",
                    "parameters": {},  # 使用默认参数
                    "position": {"x": 450, "y": 320}
                }
            ]
        },
        {
            "name": "IEEE39_with_ZeroSeqProtection",
            "description": "IEEE39系统配置零序电压保护",
            "modifications": [
                {
                    "action": "add_component",
                    "component_type": "model/CloudPSS/ZeroSequenceOverVoltageProtection",  # 零序电压保护
                    "label": "ZSV_Relay_Bus30",
                    "parameters": {},  # 使用默认参数
                    "position": {"x": 550, "y": 400}
                }
            ]
        },

        # 4. 修改线路参数（更简单的版本）
        {
            "name": "IEEE39_Line_Length_150",
            "description": "IEEE39系统线路1-2长度修改为150km",
            "modifications": [
                {
                    "action": "modify_component",
                    "selector": {"label": "TLine_3p-17"},
                    "parameters": {
                        "线路长度": 150
                    }
                }
            ]
        },
        {
            "name": "IEEE39_Line_Length_200",
            "description": "IEEE39系统线路1-2长度修改为200km",
            "modifications": [
                {
                    "action": "modify_component",
                    "selector": {"label": "TLine_3p-17"},
                    "parameters": {
                        "线路长度": 200
                    }
                }
            ]
        },

        # 5. 添加新母线
        {
            "name": "IEEE39_New_Bus",
            "description": "IEEE39系统添加新母线",
            "modifications": [
                {
                    "action": "add_component",
                    "component_type": "model/CloudPSS/_newBus_3p",
                    "label": "Bus_New_Test",
                    "parameters": {
                        "额定电压": 110,
                        "电压初始值": 1.0
                    },
                    "position": {"x": 700, "y": 500}
                }
            ]
        },
    ]

    # 创建每个测试算例
    created_models = []
    failed_models = []

    print("=" * 60)
    print("开始创建测试算例")
    print("=" * 60)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}] 创建: {test_case['name']}")
        print(f"      描述: {test_case['description']}")

        config = {
            "base_model": {"rid": "model/holdme/IEEE39"},
            "auth": {"token_file": ".cloudpss_token"},
            "modifications": test_case["modifications"],
            "output": {
                "save": True,
                "branch": f"test_{test_case['name']}",
                "name": test_case["name"],
                "description": test_case["description"]
            }
        }

        result = skill.run(config)

        if result.status == SkillStatus.SUCCESS:
            print(f"      ✅ 成功")
            if result.data["generated_models"]:
                model_info = result.data["generated_models"][0]
                print(f"      RID: {model_info['rid']}")
                created_models.append({
                    "name": test_case["name"],
                    "rid": model_info["rid"],
                    "description": test_case["description"]
                })
        else:
            print(f"      ❌ 失败: {result.error}")
            failed_models.append({
                "name": test_case["name"],
                "error": result.error
            })

    # 汇总结果
    print("\n" + "=" * 60)
    print("创建完成")
    print("=" * 60)
    print(f"成功: {len(created_models)} 个")
    print(f"失败: {len(failed_models)} 个")

    if created_models:
        print("\n已创建的测试算例:")
        for model in created_models:
            print(f"  - {model['name']}")
            print(f"    RID: {model['rid']}")
            print(f"    描述: {model['description']}")

    if failed_models:
        print("\n失败的算例:")
        for model in failed_models:
            print(f"  - {model['name']}: {model['error']}")

    return created_models, failed_models


if __name__ == "__main__":
    if not os.path.exists(".cloudpss_token"):
        print("错误: 需要 .cloudpss_token 文件进行认证")
        sys.exit(1)

    created, failed = create_test_models()

    # 保存结果到文件
    import json
    with open("test_models_created.json", "w", encoding="utf-8") as f:
        json.dump({
            "created": created,
            "failed": failed
        }, f, indent=2, ensure_ascii=False)

    print(f"\n结果已保存到 test_models_created.json")
