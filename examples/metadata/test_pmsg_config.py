"""
测试 WTG_PMSG_01 组件配置

验证算例创建脚本中的配置是否正确
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cloudpss_skills.metadata import get_registry
from cloudpss_skills.metadata.integration import get_metadata_integration

def test_wind_config():
    """测试风电模型配置"""
    print("=" * 60)
    print("测试风电模型配置 (WTG_PMSG_01)")
    print("=" * 60)

    # 初始化
    mi = get_metadata_integration()
    registry = get_registry()
    registry.clear()
    mi.initialize('examples/metadata')

    component_type = 'model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1'

    # 模拟 create_wind_model 中的配置
    user_params = {
        'Vbase': 0.69,
        'Sbase': 2.5,
        'P_cmd': 2.0,
        'pf_P': 2.0,
        'pf_Q': 0.0,       # 零无功
        'Pctrl_mode': '0', # PQ节点（符合实际新能源特性）
        'UnitCount': 40
    }

    print(f"\n组件类型: {component_type}")
    print(f"用户参数: {user_params}")
    print(f"\nℹ️  Pctrl_mode='0' 表示PQ节点，符合新能源实际运行特性")

    # 获取补全参数
    completed_params = mi.auto_complete_parameters(component_type, user_params)

    print(f"\n补全后参数数量: {len(completed_params)}")
    print(f"\n关键参数:")
    key_params = ['Sbase', 'Vbase', 'Pctrl_mode', 'P_cmd', 'pf_P', 'pf_Q', 'UnitCount']
    for param in key_params:
        value = completed_params.get(param, 'N/A')
        source = "用户提供" if param in user_params else "默认值"
        print(f"  {param}: {value} ({source})")

    # 验证参数
    result = mi.validate_parameters(component_type, completed_params)
    print(f"\n参数验证: {'✅ 通过' if result.valid else '❌ 失败'}")
    if not result.valid:
        print(f"  错误: {result.errors}")

    # 计算总容量
    total_capacity = completed_params.get('Sbase', 2.5) * completed_params.get('UnitCount', 1)
    print(f"\n总装机容量: {total_capacity:.1f} MVA")
    print(f"总有功出力: {completed_params.get('pf_P', 2.0) * completed_params.get('UnitCount', 1):.1f} MW")

    # 引脚验证
    pins_info = mi.get_pin_requirements(component_type)
    print(f"\n引脚配置:")
    print(f"  电气引脚: {pins_info.get('electrical_pins', [])}")
    print(f"  必需引脚: {pins_info.get('required_pins', [])}")

    # 验证引脚连接
    pin_connection = {'0': 'Bus10'}  # 模拟连接到Bus10
    pin_result = mi.validate_pin_connection(component_type, pin_connection)
    print(f"\n引脚连接验证: {'✅ 通过' if pin_result.valid else '❌ 失败'}")

    return result.valid and pin_result.valid

def test_hybrid_config():
    """测试混合模型配置"""
    print("\n" + "=" * 60)
    print("测试混合模型配置 (PMSG + PV)")
    print("=" * 60)

    mi = get_metadata_integration()
    registry = get_registry()
    registry.clear()
    mi.initialize('examples/metadata')

    # 风电参数
    wind_component_type = 'model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1'
    wind_params = mi.auto_complete_parameters(
        wind_component_type,
        {
            'Vbase': 0.69,
            'Sbase': 2.5,
            'P_cmd': 2.0,
            'pf_P': 2.0,
            'Pctrl_mode': '1',
            'UnitCount': 40
        }
    )

    wind_capacity = wind_params.get('pf_P', 2.0) * wind_params.get('UnitCount', 1)
    print(f"\n风电配置:")
    print(f"  组件: {wind_component_type}")
    print(f"  单台功率: {wind_params.get('pf_P', 2.0)} MW")
    print(f"  台数: {wind_params.get('UnitCount', 1)}")
    print(f"  总功率: {wind_capacity} MW")

    # 光伏参数（简化）
    pv_component_type = 'model/CloudPSS/PVStation'
    pv_params = mi.auto_complete_parameters(
        pv_component_type,
        {'Vpcc': 0.69, 'Pnom': 50.0, 'Irradiance': 1000.0}
    )

    print(f"\n光伏配置:")
    print(f"  组件: {pv_component_type}")
    print(f"  额定功率: {pv_params.get('Pnom', 50.0)} MW")

    total_new_energy = wind_capacity + pv_params.get('Pnom', 50.0)
    print(f"\n新能源总容量: {total_new_energy} MW")

    return True

if __name__ == '__main__':
    wind_ok = test_wind_config()
    hybrid_ok = test_hybrid_config()

    print("\n" + "=" * 60)
    if wind_ok and hybrid_ok:
        print("✅ 所有配置测试通过")
        print("\n可以运行: python examples/metadata/create_test_models.py --all")
    else:
        print("❌ 配置测试失败")
        sys.exit(1)
    print("=" * 60)
