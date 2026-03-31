# 保护整定与配合分析技能 (protection_coordination)

## 功能概述

本技能用于分析电力系统继电保护装置的定值配置、配合关系和动作特性。支持距离保护、过流保护、差动保护、零序保护和重合闸的完整分析流程。

## 适用算例

- **推荐算例**: `model/holdme/substation_110` (110kV变电站一、二次系统)
- **算例特点**: 包含完整的110kV/10kV两级保护配置

## 配置说明

```yaml
skill: protection_coordination
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/substation_110

analysis:
  distance_protection:
    enabled: true
    check_zones: [1, 2, 3]

  overcurrent_protection:
    enabled: true
    check_coordination: true
    time_margin: 0.3

  differential_protection:
    enabled: true

  zero_sequence_protection:
    enabled: true

  reclosing:
    enabled: true

  fault_scenarios:
    - type: three_phase
      location: 110kV_L1
      duration: 0.1

output:
  format: json
  generate_tcc_curves: true
```

## 分析功能

### 1. 距离保护分析
- **Zone1**: 80%线路阻抗，瞬时动作
- **Zone2**: 120%线路阻抗，延时0.3s
- **Zone3**: 下级线路，延时0.6s

### 2. 过流保护分析
- 启动电流计算
- 时间配合校验
- 上下级配合关系分析

### 3. 差动保护分析
- 变压器差动保护
- 斜率校验
- 启动电流设定

### 4. 零序保护分析
- 接地故障检测
- 零序电流保护

### 5. 重合闸分析
- 单相重合闸
- 三相重合闸
- 重合闸成功率统计

## 输出结果

```json
{
  "model": "model/holdme/substation_110",
  "protection_devices_found": 120,
  "distance_relays": 6,
  "overcurrent_relays": 45,
  "differential_relays": 9,
  "analysis_results": {
    "distance_protection": {...},
    "overcurrent_protection": {...},
    "fault_scenarios": [...],
    "tcc_curves": {...}
  }
}
```

## 使用示例

```python
from cloudpss_skills.builtin.protection_coordination import ProtectionCoordinationSkill

skill = ProtectionCoordinationSkill()
result = skill.run(config)

# 获取保护配合分析
oc_analysis = result.data["analysis_results"]["overcurrent_protection"]
for coord in oc_analysis["coordination_check"]:
    print(f"主保护: {coord['primary']}")
    print(f"后备保护: {coord['backup']}")
    print(f"时间裕度: {coord['time_margin']:.2f}s")
    print(f"配合合格: {coord['is_valid']}")
```

## 技术实现

### 保护定值计算方法

**距离保护定值:**
```
Zone1 = 0.8 × Z_line
Zone2 = Z_line + 0.5 × Z_next
Zone3 = Z_line + Z_next + 0.25 × Z_next2
```

**过流保护定值:**
```
Pickup = 1.5 × I_load_max
Time = TD × (A / (M^B - 1) + C)
```

### 配合时间要求

| 层级 | 时间配合要求 |
|-----|-------------|
| 110kV vs 10kV | ≥0.3s |
| 主变两侧 | ≥0.4s |
| 母线与出线 | ≥0.2s |

## 注意事项

1. 算例必须包含保护配置参数
2. 故障场景位置必须存在于模型中
3. TCC曲线数据可用于可视化配合关系
