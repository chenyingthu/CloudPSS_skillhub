# 短路电流计算技能 (Short Circuit)

## 概述

短路电流计算技能用于计算电力系统在各种故障条件下的短路电流，为保护装置整定和设备选型提供依据。

## 功能特性

- **多种故障类型**: 三相短路、单相接地、两相短路等
- **全系统计算**: 计算所有母线的短路电流
- **阻抗矩阵**: 基于节点阻抗矩阵计算
- **结果导出**: JSON/CSV格式的短路电流报告

## 设计原理

### 短路计算

基于对称分量法和节点阻抗矩阵：

```
I_fault = V_prefault / Z_fault
```

## 快速开始

### 1. YAML配置

```yaml
skill: short_circuit
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  fault_type: three_phase    # 故障类型
  base_mva: 100.0           # 基准容量

output:
  format: json
  path: ./results/
  prefix: short_circuit
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("short_circuit")

config = {
    "skill": "short_circuit",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "fault_type": "three_phase"
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "short_circuit" |
| `model.rid` | string | 是 | - | 模型RID |
| `analysis.fault_type` | enum | 否 | three_phase | 故障类型 |
| `analysis.base_mva` | number | 否 | 100.0 | 基准容量(MVA) |
| `output.format` | enum | 否 | json | json / csv |

## 故障类型

| 类型 | 说明 |
|------|------|
| three_phase | 三相短路 |
| single_phase_ground | 单相接地 |
| two_phase | 两相短路 |
| two_phase_ground | 两相接地 |

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
