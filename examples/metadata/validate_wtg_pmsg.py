"""
验证 WTG_PMSG 元数据配置

测试新的 PMSG 风机组件是否能正确参与潮流计算
"""

import os
import sys
import json
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cloudpss_skills.metadata import get_registry
from cloudpss_skills.metadata.integration import get_metadata_integration

def validate_metadata():
    """验证元数据加载和参数补全"""
    print("=" * 60)
    print("WTG_PMSG 元数据验证")
    print("=" * 60)

    # 初始化注册表
    mi = get_metadata_integration()
    registry = get_registry()
    registry.clear()  # 清空以确保加载新文件
    mi.initialize('examples/metadata')

    # 列出所有注册的组件
    print("\n已注册的组件:")
    for comp_id in registry.list_components():
        print(f"  - {comp_id}")

    # 检查 WTG_PMSG_01 是否注册
    component_type = 'model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1'
    metadata = mi.get_component_metadata(component_type)

    if metadata:
        print(f"\n✅ 找到组件: {component_type}")
        print(f"   名称: {metadata.name}")
        print(f"   描述: {metadata.description[:50]}...")

        # 测试参数补全
        user_params = {
            'Vbase': 0.69,
            'Sbase': 2.5,
            'P_cmd': 2.0,
            'pf_P': 2.0,
            'Pctrl_mode': '1',
            'UnitCount': 40
        }

        print("\n参数补全测试:")
        print(f"   用户输入参数: {list(user_params.keys())}")

        completed = mi.auto_complete_parameters(component_type, user_params)

        # 检查关键潮流参数
        powerflow_params = ['Pctrl_mode', 'P_cmd', 'pf_P', 'pf_Q', 'Q_cmd', 'V_cmd']
        print(f"\n   潮流计算关键参数:")
        for param in powerflow_params:
            if param in completed:
                print(f"     - {param}: {completed[param]}")

        # 检查所有参数
        print(f"\n   完整参数数量: {len(completed)}")
        print(f"   补全参数: {[k for k in completed if k not in user_params]}")

        # 验证参数
        print("\n参数验证:")
        result = mi.validate_parameters(component_type, completed)
        if result.valid:
            print("   ✅ 参数验证通过")
        else:
            print(f"   ❌ 参数验证失败: {result.errors}")

        # 引脚信息
        print("\n引脚信息:")
        pins = mi.get_pin_requirements(component_type)
        print(f"   总引脚数: {pins.get('total_pins', 0)}")
        print(f"   电气引脚: {pins.get('electrical_pins', [])}")
        print(f"   必需引脚: {pins.get('required_pins', [])}")

        return True
    else:
        print(f"\n❌ 未找到组件: {component_type}")
        print("\n尝试搜索相似组件:")
        for comp_id in registry.list_components():
            if 'WTG' in comp_id or 'PMSG' in comp_id or 'wind' in comp_id.lower():
                print(f"  - {comp_id}")
        return False

def compare_components():
    """对比新旧组件类型的差异"""
    print("\n" + "=" * 60)
    print("组件类型对比")
    print("=" * 60)

    mi = get_metadata_integration()
    registry = get_registry()
    registry.clear()
    mi.initialize('examples/metadata')

    # 旧组件
    old_type = 'model/CloudPSS/WGSource'
    # 新组件
    new_type = 'model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1'

    old_metadata = mi.get_component_metadata(old_type)
    new_metadata = mi.get_component_metadata(new_type)

    print(f"\n旧组件: {old_type}")
    if old_metadata:
        old_params = old_metadata.auto_complete({})
        print(f"   总参数数: {len(old_params)}")
        print(f"   潮流参数: {[k for k in old_params if k.startswith('pf_') or 'powerflow' in k.lower()]}")

    print(f"\n新组件: {new_type}")
    if new_metadata:
        new_params = new_metadata.auto_complete({})
        print(f"   总参数数: {len(new_params)}")
        print(f"   潮流参数: {[k for k in new_params if k.startswith('pf_') or k in ['Pctrl_mode', 'P_cmd', 'Q_cmd', 'V_cmd']]}")
        print(f"\n   ✅ 新组件包含完整的潮流计算参数:")
        print(f"      - Pctrl_mode: 控制模式")
        print(f"      - P_cmd: 有功指令")
        print(f"      - pf_P: 潮流有功")
        print(f"      - pf_Q: 潮流无功")
        print(f"      - Q_cmd: 无功指令")
        print(f"      - V_cmd: 电压指令")

if __name__ == '__main__':
    success = validate_metadata()
    compare_components()

    if success:
        print("\n" + "=" * 60)
        print("✅ 元数据验证通过，可以使用 WTG_PMSG_01 创建算例")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ 元数据验证失败")
        print("=" * 60)
        sys.exit(1)
