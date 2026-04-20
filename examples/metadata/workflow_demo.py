"""
元数据集成工作流示例

演示如何使用元数据系统改进 model_builder 和 model_validator 的工作流
"""

import logging
from cloudpss_skills.metadata.integration import get_metadata_integration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def workflow_demo():
    """
    工作流演示：使用元数据系统

    场景：添加一个 WGSource 风机组件到模型
    """
    print("=" * 60)
    print("元数据集成工作流示例")
    print("=" * 60)

    # 1. 初始化元数据集成
    print("\n[步骤1] 初始化元数据集成...")
    mi = get_metadata_integration()
    mi.initialize()
    print(f"✅ 已加载 {len(mi.registry)} 个组件元数据")

    # 2. 查询组件元数据
    print("\n[步骤2] 查询 WGSource 组件元数据...")
    comp_type = "model/CloudPSS/WGSource"
    summary = mi.get_component_summary(comp_type)
    print(summary)

    # 3. 获取参数信息
    print("\n[步骤3] 获取参数要求...")
    required = mi.get_required_parameters(comp_type)
    print(f"必需参数 ({len(required)}个): {', '.join(required)}")

    # 4. 获取引脚要求
    print("\n[步骤4] 获取引脚要求...")
    pins = mi.get_pin_requirements(comp_type)
    print(f"总引脚: {pins['total_pins']}")
    print(f"电气引脚: {pins['electrical_pins']}")
    print(f"必需引脚: {pins['required_pins']}")

    # 5. 模拟用户提供的参数（不完整）
    print("\n[步骤5] 用户提供的参数（不完整）...")
    user_params = {
        "Vpcc": 0.69,  # 并网点电压
        "WindSpeed": 12.0,  # 风速
    }
    print(f"用户提供: {user_params}")

    # 6. 自动补全参数
    print("\n[步骤6] 自动补全参数...")
    completed = mi.auto_complete_parameters(comp_type, user_params)
    added = set(completed.keys()) - set(user_params.keys())
    print(f"✅ 已补全 {len(added)} 个参数:")
    for key in sorted(added):
        print(f"   - {key} = {completed[key]}")

    # 7. 验证参数
    print("\n[步骤7] 验证参数...")
    result = mi.validate_parameters(comp_type, completed)
    if result.valid:
        print("✅ 参数验证通过")
    else:
        print("❌ 参数验证失败:")
        for error in result.errors:
            print(f"   - {error}")

    # 8. 验证引脚连接
    print("\n[步骤8] 验证引脚连接...")
    pin_connection = {"0": "Bus10"}  # 连接到母线10
    pin_result = mi.validate_pin_connection(comp_type, pin_connection)
    if pin_result.valid:
        print("✅ 引脚连接验证通过")
    else:
        print("❌ 引脚连接验证失败:")
        for error in pin_result.errors:
            print(f"   - {error}")

    # 9. 总结
    print("\n" + "=" * 60)
    print("工作流完成总结")
    print("=" * 60)
    print(f"组件类型: {comp_type}")
    print(f"最终参数数: {len(completed)}")
    print(f"用户自定义: {len(user_params)}")
    print(f"自动补全: {len(added)}")
    print(f"参数验证: {'通过' if result.valid else '失败'}")
    print(f"引脚验证: {'通过' if pin_result.valid else '失败'}")
    print("\n✅ 元数据集成工作流演示完成!")


def validation_demo():
    """
    验证演示：检测不完整配置
    """
    print("\n" + "=" * 60)
    print("验证演示：检测不完整配置")
    print("=" * 60)

    mi = get_metadata_integration()
    mi.initialize()

    comp_type = "model/CloudPSS/WGSource"

    # 场景1：完全缺少必需参数
    print("\n[场景1] 完全缺少必需参数...")
    bad_params1 = {"WindSpeed": 12.0}
    result1 = mi.validate_parameters(comp_type, bad_params1)
    print(f"参数: {bad_params1}")
    print(f"结果: {'通过' if result1.valid else '失败'}")
    if not result1.valid:
        print(f"错误: {result1.errors}")

    # 场景2：部分参数缺失
    print("\n[场景2] 部分参数缺失...")
    bad_params2 = {
        "Vbase": 0.69,
        "Fnom": 50.0,
        # 缺少 Pnom, Vpcc
    }
    result2 = mi.validate_parameters(comp_type, bad_params2)
    print(f"参数: {bad_params2}")
    print(f"结果: {'通过' if result2.valid else '失败'}")
    if not result2.valid:
        print(f"错误: {result2.errors}")

    # 场景3：正确配置
    print("\n[场景3] 正确配置...")
    good_params = {
        "Vbase": 0.69,
        "Fnom": 50.0,
        "Pnom": 100.0,
        "Vpcc": 0.69,
    }
    result3 = mi.validate_parameters(comp_type, good_params)
    print(f"参数: {good_params}")
    print(f"结果: {'通过' if result3.valid else '失败'}")

    print("\n✅ 验证演示完成!")


if __name__ == "__main__":
    workflow_demo()
    validation_demo()
