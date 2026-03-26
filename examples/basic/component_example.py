"""
CloudPSS Component Operations Example

运行方式: python examples/basic/component_example.py
前置条件: 有效的CloudPSS token保存在 .cloudpss_token

本示例演示如何基于已有算例或本地工作副本构建一个研究分支，并在其中添加、查询、更新和删除元件。
"""

import os
from pathlib import Path
import sys

from cloudpss import Model, setToken


DEFAULT_READONLY_MODEL_RID = os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39")
DEFAULT_WORKING_COPY = "examples/basic/component_working_copy.yaml"


def load_token():
    """从文件加载 API token"""
    try:
        with open('.cloudpss_token', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("错误: 未找到 .cloudpss_token 文件")
        print("请将 CloudPSS API token 保存到项目根目录的 .cloudpss_token 文件中")
        sys.exit(1)


def load_model_from_source(source):
    """从云端 RID 或本地 YAML/JSON 加载模型。"""
    candidate = Path(source).expanduser()
    file_like = candidate.suffix.lower() in {".yaml", ".yml", ".json"}

    if candidate.exists():
        model = Model.load(str(candidate))
        print(f"本地模型文件: {candidate}")
        print(f"模型名称: {model.name}")
        print(f"模型 RID: {model.rid}")
        return model

    if file_like:
        raise FileNotFoundError(f"未找到本地模型文件: {candidate}")

    model = Model.fetch(source)
    print(f"云端模型 RID: {source}")
    print(f"模型名称: {model.name}")
    print(f"模型 RID: {model.rid}")
    return model


def suggest_working_copy_path(source):
    """对本地输入源生成安全的默认工作副本路径。"""
    candidate = Path(source).expanduser()
    if candidate.exists() and candidate.suffix.lower() in {".yaml", ".yml", ".json"}:
        return str(candidate.with_name(f"{candidate.stem}-branch{candidate.suffix}"))
    return DEFAULT_WORKING_COPY


def suggest_modified_copy_path(working_copy_path):
    """为修改后的工作副本生成默认输出路径。"""
    candidate = Path(working_copy_path).expanduser()
    if candidate.suffix:
        return str(candidate.with_name(f"{candidate.stem}-modified{candidate.suffix}"))
    return f"{working_copy_path}-modified"


def example_add_component(model):
    """添加元件示例"""
    print("\n=== 添加元件示例 ===")

    # 添加电阻
    resistor = model.addComponent(
        definition='model/CloudPSS/resistor',
        label='R1',
        args={'resistance': 10},
        pins={'p': {'x': 0, 'y': 0}, 'n': {'x': 50, 'y': 0}},
        position={'x': 100, 'y': 200}
    )
    print(f"添加电阻: {resistor.label}, ID: {resistor.id}")
    print(f"  位置: {resistor.position}")
    print(f"  参数: {resistor.args}")

    return resistor.id


def create_local_working_copy(model, export_path=DEFAULT_WORKING_COPY):
    """先导出本地工作副本，再在副本上改模，避免直接污染原模型"""
    print("\n=== 创建本地工作副本 ===")

    Model.dump(model, export_path, compress=None)
    working_model = Model.load(export_path)
    print(f"已创建本地工作副本: {export_path}")
    print(f"工作副本模型: {working_model.name}")
    return working_model, export_path


def example_get_components(model):
    """获取元件示例"""
    print("\n=== 获取元件示例 ===")

    # 获取所有元件
    all_components = model.getAllComponents()
    print(f"模型中共有 {len(all_components)} 个元件")

    # 按类型获取元件
    resistors = model.getComponentsByRid('model/CloudPSS/resistor')
    print(f"电阻数量: {len(resistors)}")
    for key, comp in resistors.items():
        print(f"  {key}: {comp.label} - {comp.args}")

    voltage_sources = model.getComponentsByRid('model/CloudPSS/acvoltageSource')
    print(f"电压源数量: {len(voltage_sources)}")


def example_update_component(model, component_id):
    """更新元件示例"""
    print("\n=== 更新元件示例 ===")

    # 获取元件
    component = model.getComponentByKey(component_id)
    print(f"更新前: {component.label}, 阻值: {component.args}")

    # 更新电阻值
    model.updateComponent(
        component_id,
        args={'resistance': 50}
    )

    # 验证更新
    component = model.getComponentByKey(component_id)
    print(f"更新后: {component.label}, 阻值: {component.args}")


def example_remove_component(model, component_id):
    """删除元件示例"""
    print("\n=== 删除元件示例 ===")

    # 删除元件
    success = model.removeComponent(component_id)
    print(f"删除结果: {success}")

    # 验证删除
    try:
        component = model.getComponentByKey(component_id)
        print("警告: 元件仍然存在")
    except KeyError:
        print("确认: 元件已删除")


def example_check_topology(model):
    """改模后做 revision 级结构快速检查。"""
    print("\n=== 拓扑检查示例 ===")
    print("注意: fetched 工作副本上的 fetchTopology() 主要反映已保存 revision，")
    print("若要确认未保存本地改动是否真正进入求解，请继续运行潮流或 EMT。")

    try:
        topology = model.fetchTopology(implementType="powerFlow")
        topology_data = topology.toJSON()
        print(f"拓扑元件数: {len(topology_data.get('components', {}))}")
        print(f"映射键预览: {list(topology_data.get('mappings', {}).keys())[:5]}")
    except Exception as e:
        print(f"拓扑检查失败: {e}")


def main():
    """主函数"""
    print("CloudPSS 元件操作示例")
    print("=" * 50)

    # 加载 token 并设置
    token = load_token()
    setToken(token)
    print("Token 已设置")

    print(f"- 可输入云端模型 RID，例如: {DEFAULT_READONLY_MODEL_RID}")
    print("- 也可输入本地 YAML，继续已有研究分支上的改模")

    source_arg = sys.argv[1].strip() if len(sys.argv) > 1 else ""
    if source_arg:
        print(f"使用命令行输入源: {source_arg}")
        model_source = source_arg
    else:
        prompt = (
            "请输入模型 RID 或本地 YAML 路径，直接回车使用已验证的只读模型 "
            f"[{DEFAULT_READONLY_MODEL_RID}]: "
        )
        model_source = input(prompt).strip() or DEFAULT_READONLY_MODEL_RID

    print(f"获取模型: {model_source}")
    try:
        model = load_model_from_source(model_source)
    except Exception as e:
        print(f"获取模型失败: {e}")
        return

    # 先创建工作副本，再在副本上修改
    default_working_copy = suggest_working_copy_path(model_source)
    working_copy_path = (
        input(
            "请输入本地工作副本路径，直接回车使用 "
            f"[{default_working_copy}]: "
        ).strip()
        or default_working_copy
    )
    working_model, working_copy_path = create_local_working_copy(model, working_copy_path)

    # 执行操作示例
    component_id = example_add_component(working_model)

    # 查询元件
    example_get_components(working_model)

    # 更新元件
    if component_id:
        example_update_component(working_model, component_id)

        example_check_topology(working_model)

        # 询问是否删除
        confirm = input("\n是否删除测试元件? (y/n): ").strip().lower()
        if confirm == 'y':
            example_remove_component(working_model, component_id)

    # 保存修改后的本地工作副本
    default_modified_path = suggest_modified_copy_path(working_copy_path)
    modified_output_path = (
        input(
            "\n请输入修改后工作副本的保存路径，直接回车使用 "
            f"[{default_modified_path}]: "
        ).strip()
        or default_modified_path
    )
    Model.dump(working_model, modified_output_path, compress=None)
    print(f"\n已保存修改后的本地工作副本: {modified_output_path}")

    confirm = input("是否将工作副本另存为新的云端研究分支? (y/n): ").strip().lower()
    if confirm == 'y':
        new_key = input("请输入新的模型 key: ").strip()
        if new_key:
            try:
                working_model.save(new_key)
                print(f"模型已另存为新的云端研究分支: {working_model.rid}")
            except Exception as e:
                print(f"另存失败: {e}")

    print("\n示例完成!")


if __name__ == "__main__":
    main()
