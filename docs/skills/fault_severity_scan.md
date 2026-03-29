# 故障严重度扫描技能 (Fault Severity Scan)

## 概述

故障严重度扫描技能用于扫描不同位置和类型的故障，评估各故障场景的严重程度。

## 功能特性

- **位置扫描**: 扫描不同母线位置的故障
- **类型扫描**: 扫描不同故障类型
- **严重度评估**: 评估每种故障的严重程度
- **优先级排序**: 按严重度排序故障场景

## 快速开始

### 1. YAML配置

```yaml
skill: fault_severity_scan
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

scan:
  fault_buses: []              # 故障母线列表，空表示全部
  fault_types: [three_phase]   # 故障类型列表
  fault_duration: 0.1          # 故障持续时间(s)

simulation:
  duration: 10.0

output:
  format: json
  path: ./results/
  prefix: severity_scan
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("fault_severity_scan")

config = {
    "skill": "fault_severity_scan",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE3"},
    "scan": {
        "fault_buses": ["Bus_1", "Bus_2"],
        "fault_types": ["three_phase"]
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "fault_severity_scan" |
| `model.rid` | string | 是 | - | 模型RID |
| `scan.fault_buses` | array | 否 | [] | 故障母线列表 |
| `scan.fault_types` | array | 否 | [three_phase] | 故障类型列表 |
| `scan.fault_duration` | number | 否 | 0.1 | 故障持续时间(s) |
| `simulation.duration` | number | 否 | 10.0 | 仿真时长(s) |
| `output.format` | enum | 否 | json | json / csv |

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
