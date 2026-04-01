# 模型构建器技能 (model_builder)

## 功能概述

基于现有模型创建新算例，支持组件的添加、修改和删除操作。用于批量生成测试算例、新能源接入模型、保护配置模型等。

## 配置说明

```yaml
skill: model_builder

base_model:
  rid: model/holdme/IEEE39

modifications:
  # 修改现有组件 - 使用实际的组件标签
  - action: modify_component
    selector:
      label: "TLine_3p-17"  # IEEE39线路标签格式
    parameters:
      线路长度: 150

  # 添加新组件
  - action: add_component
    component_type: model/CloudPSS/_newBus_3p
    label: "BUS_NEW"
    parameters:
      额定电压: 110

  # 删除组件 - 使用key选择器更可靠
  - action: remove_component
    selector:
      key: "canvas_0_10"  # 组件的key标识

output:
  save: true
  branch: feature/modification
  name: "Modified_Model"
```

## 操作类型

### 1. modify_component - 修改组件

根据选择器定位组件并修改参数。

**选择器选项:**
- `label`: 按组件标签匹配
- `type`: 按组件类型匹配
- `key`: 按组件key匹配

**示例:**
```yaml
- action: modify_component
  selector:
    label: "TLine_3p-17"  # IEEE39线路标签
  parameters:
    线路长度: 150
    单位长度电阻: 0.02
```

### 2. add_component - 添加组件

在模型中添加新组件。

**必需字段:**
- `component_type`: 组件类型RID
- `label`: 组件标签
- `parameters`: 组件参数

**可选字段:**
- `position`: 位置坐标 `{x, y}`

**示例:**
```yaml
- action: add_component
  component_type: model/CloudPSS/_newBus_3p
  label: "BUS_NEW_1"
  parameters:
    额定电压: 110
  position:
    x: 400
    y: 300
```

### 3. remove_component - 删除组件

从模型中删除组件。

**示例:**
```yaml
- action: remove_component
  selector:
    label: "Load_39"
```

## 批量生成

支持参数扫描批量生成模型变体:

```yaml
batch:
  enabled: true
  parameter_sweep:
    - param_name: pv_capacity
      values: [50, 100, 150, 200]
    - param_name: location
      values: [BUS_10, BUS_20, BUS_30]

modifications:
  - action: add_component
    component_type: model/CloudPSS/PV_Inverter
    label: "PV_{location}"
    parameters:
      额定容量: "{pv_capacity}"
      有功功率参考值: 0.8
```

**参数占位符**: 在 `label` 和 `parameters` 值中使用 `{param_name}` 格式，
批量生成时会自动替换为对应参数值。

## 输出结果

```json
{
  "base_model": "model/holdme/IEEE39",
  "modifications_count": 3,
  "modifications_applied": [
    "modify:canvas_0_115",
    "add:BUS_NEW_1",
    "remove:Load_39"
  ],
  "generated_models": [
    {
      "name": "Modified_Model",
      "rid": "model/holdme/feature/modification",
      "description": "IEEE39系统修改版",
      "modifications": ["modify:canvas_0_115", "add:BUS_NEW_1"]
    }
  ]
}
```

## 使用示例

### 示例1: 创建新能源接入模型

```yaml
skill: model_builder
base_model:
  rid: model/holdme/IEEE39

modifications:
  - action: add_component
    component_type: model/CloudPSS/PV_Inverter
    label: "PV_Bus10"
    parameters:
      额定容量: 100
      有功功率参考值: 0.8
    position: {x: 400, y: 300}

output:
  save: true
  branch: feature/pv_integration
  name: "IEEE39_with_PV"
```

### 示例2: 创建保护配置模型

```yaml
skill: model_builder
base_model:
  rid: model/holdme/IEEE39

modifications:
  - action: add_component
    component_type: model/CloudPSS/DistanceRelay
    label: "Relay_LINE_1_2"
    parameters:
      Zone1: 0.8
      Zone2: 1.2
      Zone3: 2.0

output:
  save: true
  branch: feature/protection
  name: "IEEE39_with_Protection"
```

### 示例3: 批量生成测试算例

```yaml
skill: model_builder
base_model:
  rid: model/holdme/IEEE39

batch:
  enabled: true
  parameter_sweep:
    - param_name: load_level
      values: [0.8, 0.9, 1.0, 1.1, 1.2]

modifications:
  - action: modify_component
    selector: {label: "Load_Total"}
    parameters:
      负荷水平: "{load_level}"

output:
  save: true
  name: "IEEE39_Load_{load_level}"
```

## 注意事项

1. **保存权限**: 需要模型写权限才能保存
2. **组件引用**: 删除组件前确保没有其他组件引用它
3. **参数验证**: 修改参数时需确保数值在合理范围内
4. **批量生成**: 大量变体生成可能耗时较长

## 故障排查

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 找不到组件 | 标签名错误 | 检查模型中的实际标签名 |
| 保存失败 | 权限不足 | 确认token有写权限 |
| 参数无效 | 参数名错误 | 参考组件文档确认参数名 |
