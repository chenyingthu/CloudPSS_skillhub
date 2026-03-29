# 扰动严重度分析技能 (Disturbance Severity)

## 概述

扰动严重度分析技能用于评估电力系统故障后的电压恢复特性，基于DV（电压裕度）和SI（严重度指数）指标。

## 功能特性

- **DV分析**: 电压上下限裕度计算
- **SI计算**: 故障严重度指数
- **薄弱点识别**: 自动识别电压恢复差的母线
- **多格式报告**: JSON/CSV/Markdown报告

## 快速开始

### 1. YAML配置

```yaml
skill: disturbance_severity
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

simulation:
  fault_bus: Bus_16
  fault_type: three_phase
  fault_time: 4.0
  fault_duration: 0.1

analysis:
  dv_enabled: true
  si_enabled: true

output:
  format: json
  path: ./results/
  prefix: disturbance
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("disturbance_severity")

config = {
    "skill": "disturbance_severity",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE39"},
    "simulation": {
        "fault_bus": "Bus_16",
        "fault_type": "three_phase"
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "disturbance_severity" |
| `model.rid` | string | 是 | - | 模型RID |
| `simulation.fault_bus` | string | 是 | - | 故障母线 |
| `simulation.fault_type` | enum | 否 | three_phase | 故障类型 |
| `simulation.fault_time` | number | 否 | 4.0 | 故障时间(s) |
| `simulation.fault_duration` | number | 否 | 0.1 | 故障持续时间(s) |
| `analysis.dv_enabled` | boolean | 否 | true | 启用DV计算 |
| `analysis.si_enabled` | boolean | 否 | true | 启用SI计算 |
| `output.format` | enum | 否 | json | json / csv |

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
