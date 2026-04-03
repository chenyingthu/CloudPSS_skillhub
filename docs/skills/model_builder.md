# 模型构建器技能 (model_builder)

## 功能概述

基于现有模型创建新算例，支持组件的添加、修改和删除操作。用于批量生成测试算例、新能源接入模型、保护配置模型等。

## 核心特性

- ✅ **组件操作**: 支持添加(add)、修改(modify)、删除(remove)三种操作
- ✅ **批量生成**: 参数扫描批量生成模型变体，支持占位符替换
- ✅ **自动保存**: 直接保存到 CloudPSS 平台，生成可访问的 RID
- ✅ **Duck Typing**: 使用 `getattr()` 安全访问组件属性，兼容不同 SDK 版本
- ✅ **新能源兼容映射**: 旧配置中的 `WGSource` / `PVStation` / `PV_Inverter` 会自动映射到公开且支持潮流的组件

## 当前推荐的新能源接入路径

对于需要真实进入潮流计算的新能源算例，当前主线建议使用以下公开组件：

| 类别 | 推荐组件 | 说明 |
|-----|---------|-----|
| **风电** | `model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1` | 支持潮流，适合作为风电场等值接入 |
| **光伏** | `model/open-cloudpss/PVS_01-avm-stdm-v1b5` | 支持潮流，适合作为光伏电站接入 |

兼容说明：
- 旧配置中的 `model/CloudPSS/WGSource` 会自动映射到 `WTG_PMSG_01-avm-stdm-v2b1`
- 旧配置中的 `model/CloudPSS/DFIG_WindFarm_Equivalent_Model` 也会自动映射到 `WTG_PMSG_01-avm-stdm-v2b1`
- 旧配置中的 `model/CloudPSS/PVStation` 和 `model/CloudPSS/PV_Inverter` 会自动映射到 `PVS_01-avm-stdm-v1b5`
- `pin_connection.target_bus` 可以写成 `Bus14` / `bus14` / 母线组件 key，技能会自动解析到真实可连接信号
- `WGSource_Bus30` 这类旧设计已退役，不再作为推荐测试算例保留

## 配置说明

```yaml
skill: model_builder

base_model:
  rid: model/holdme/IEEE39

modifications:
  # 修改现有组件
  - action: modify_component
    selector:
      label: "TLine_3p-17"
    parameters:
      线路长度: 150

  # 添加新组件
  - action: add_component
    component_type: model/open-cloudpss/PVS_01-avm-stdm-v1b5
    label: "PV_Bus10"
    parameters:
      P_cmd: 50
      pf_P: 50
      pf_Q: 0
      Pctrl_mode: "0"
    pin_connection:
      target_bus: Bus14
      pin_name: "0"
    position:
      x: 400
      y: 300

  # 删除组件
  - action: remove_component
    selector:
      key: "canvas_0_10"

output:
  save: true
  branch: test_pv_integration
  name: "IEEE39_with_PV"
  description: "IEEE39系统母线10接入光伏电站"
```

## 操作类型

### 1. modify_component - 修改组件

**选择器选项:**
- `label`: 按组件标签匹配
- `type`: 按组件类型匹配
- `key`: 按组件key匹配

```yaml
- action: modify_component
  selector:
    label: "TLine_3p-17"
  parameters:
    线路长度: 150
```

### 2. add_component - 添加组件

**必需字段:**
- `component_type`: 组件类型RID
- `label`: 组件标签
- `parameters`: 组件参数

```yaml
- action: add_component
  component_type: model/open-cloudpss/PVS_01-avm-stdm-v1b5
  label: "PV_Bus10"
  parameters:
    P_cmd: 50
    pf_P: 50
    pf_Q: 0
    Pctrl_mode: "0"
  pin_connection:
    target_bus: Bus14
  position: {x: 400, y: 300}
```

### 3. remove_component - 删除组件

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

modifications:
  - action: add_component
    component_type: model/open-cloudpss/PVS_01-avm-stdm-v1b5
    label: "PV_{pv_capacity}MW"
    parameters:
      P_cmd: "{pv_capacity}"
      pf_P: "{pv_capacity}"
      pf_Q: 0
      Pctrl_mode: "0"
    pin_connection:
      target_bus: Bus14
```

**参数占位符**: 使用 `{param_name}` 格式，批量生成时自动替换。

## 常用组件类型

### 新能源组件
| 组件名称 | RID | 说明 |
|---------|-----|-----|
| 光伏电站（推荐） | `model/open-cloudpss/PVS_01-avm-stdm-v1b5` | 公开可访问，支持潮流的光伏封装模型 |
| 风电场（推荐） | `model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1` | 公开可访问，支持潮流的 PMSG 风机封装模型 |
| DFIG风电场 | `model/CloudPSS/DFIG_WindFarm_Equivalent_Model` | 旧写法，运行时会自动映射到公开 PMSG 风机模型 |

### 保护组件
| 组件名称 | RID | 说明 |
|---------|-----|-----|
| 纵联差动保护 | `model/CloudPSS/DifferentialProtection` | 线路差动保护 |
| 复压过流保护 | `model/CloudPSS/CompoundVoltageOverCurrentProtection` | 复压过流保护 |
| 零序电压保护 | `model/CloudPSS/ZeroSequenceOverVoltageProtection` | 零序过压保护 |

### 其他组件
| 组件名称 | RID | 说明 |
|---------|-----|-----|
| 三相母线 | `model/CloudPSS/_newBus_3p` | 新建母线 |
| 三相线路 | `model/CloudPSS/_newTLine_3p` | 输电线路 |
| 变压器 | `model/CloudPSS/_newTransformer_3p2w` | 三相双绕组变压器 |

## 使用示例

### 示例1: 创建新能源接入模型

```yaml
skill: model_builder
base_model:
  rid: model/holdme/IEEE39

modifications:
  - action: add_component
    component_type: model/open-cloudpss/PVS_01-avm-stdm-v1b5
    label: "PV_Bus10_50MW"
    parameters:
      P_cmd: 50
      pf_P: 50
      pf_Q: 0
      Pctrl_mode: "0"
    pin_connection:
      target_bus: Bus14
      pin_name: "0"
    position: {x: 400, y: 300}

output:
  save: true
  branch: test_IEEE39_with_PV_50MW
  name: "IEEE39_with_PV_50MW"
  description: "IEEE39系统母线10接入50MW光伏电站"
```

### 示例2: 批量生成光伏测试算例

```yaml
skill: model_builder
base_model:
  rid: model/holdme/IEEE39

batch:
  enabled: true
  parameter_sweep:
    - param_name: capacity
      values: [50, 100, 150]

modifications:
  - action: add_component
    component_type: model/open-cloudpss/PVS_01-avm-stdm-v1b5
    label: "PV_Bus10_{capacity}MW"
    parameters:
      P_cmd: "{capacity}"
      pf_P: "{capacity}"
      pf_Q: 0
      Pctrl_mode: "0"
    pin_connection:
      target_bus: Bus14
      pin_name: "0"

output:
  save: true
  branch: "test_IEEE39_with_PV_{capacity}MW"
  name: "IEEE39_with_PV_{capacity}MW"
```

### 示例3: 创建保护配置模型

```yaml
skill: model_builder
base_model:
  rid: model/holdme/IEEE39

modifications:
  - action: add_component
    component_type: model/CloudPSS/DifferentialProtection
    label: "DiffRelay_LINE_1_2"
    parameters: {}
    position: {x: 500, y: 350}

output:
  save: true
  branch: test_IEEE39_with_DifferentialProtection
  name: "IEEE39_with_DifferentialProtection"
```

## 输出结果

```json
{
  "base_model": "model/holdme/IEEE39",
  "modifications_count": 1,
  "modifications_applied": ["add:PV_Bus10_50MW"],
  "generated_models": [
    {
      "name": "IEEE39_with_PV_50MW",
      "rid": "model/holdme/test_IEEE39_with_PV_50MW",
      "description": "IEEE39系统母线10接入50MW光伏电站"
    }
  ]
}
```

## 技术实现

### 组件属性访问

使用 Duck Typing 模式安全访问组件属性:

```python
# 安全的属性访问方式
label = getattr(comp, 'label', None)
pins = getattr(comp, 'pins', {})
args = getattr(comp, 'args', {})
```

避免了 `comp.get()` 或 `comp['label']` 可能引发的 AttributeError。

### 批量参数替换

```python
def _get_modifications_with_params(
    self,
    modifications: List[Dict],
    params: Dict
) -> List[Dict]:
    """应用参数替换"""
    result = []
    for mod in modifications:
        new_mod = copy.deepcopy(mod)
        # 替换 label 中的占位符
        if 'label' in new_mod:
            new_mod['label'] = new_mod['label'].format(**params)
        # 替换 parameters 中的占位符
        if 'parameters' in new_mod:
            for k, v in new_mod['parameters'].items():
                if isinstance(v, str) and '{' in v:
                    new_mod['parameters'][k] = v.format(**params)
        result.append(new_mod)
    return result
```

## 注意事项

1. **组件类型**: 使用 `component_catalog` 技能查找有效的组件 RID
2. **标签格式**: IEEE39线路标签格式为 `TLine_3p-XX`
3. **保存权限**: 需要模型写权限才能保存
4. **分支命名**: 使用下划线 `_` 代替斜杠 `/`，如 `test_pv_50mw`

## 故障排查

| 问题 | 可能原因 | 解决方案 |
|-----|---------|---------|
| 找不到组件 | 标签名错误 | 使用 `model.getAllComponents()` 查看实际标签 |
| 保存失败 | 权限不足 | 确认 token 有写权限 |
| 参数无效 | 参数名错误 | 参考组件文档确认参数名 |
| 批量生成失败 | 占位符格式错误 | 使用 `{param_name}` 格式 |

## 配套技能

- **[component_catalog](component_catalog.md)**: 查找可用组件 RID
- **[model_validator](model_validator.md)**: 验证创建的模型有效性
