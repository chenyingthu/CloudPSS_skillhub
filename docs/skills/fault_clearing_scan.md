# 故障清除时间扫描技能 (Fault Clearing Scan)

## 概述

故障清除时间扫描技能用于扫描不同故障清除时间对系统稳定性的影响，确定临界清除时间。

## 功能特性

- **时间扫描**: 扫描不同故障清除时间
- **稳定性评估**: 评估每种时间下的稳定性
- **临界时间**: 确定临界清除时间
- **灵敏度分析**: 分析清除时间对稳定性的影响

## 快速开始

### 1. YAML配置

```yaml
skill: fault_clearing_scan
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

scan:
  fault_bus: Bus_1
  fault_type: three_phase
  clearing_times: [0.05, 0.1, 0.15, 0.2, 0.25]  # 扫描时间(s)

simulation:
  duration: 10.0

output:
  format: json
  path: ./results/
  prefix: clearing_scan
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("fault_clearing_scan")

config = {
    "skill": "fault_clearing_scan",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE3"},
    "scan": {
        "fault_bus": "Bus_1",
        "clearing_times": [0.05, 0.1, 0.15]
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "fault_clearing_scan" |
| `model.rid` | string | 是 | - | 模型RID |
| `scan.fault_bus` | string | 是 | - | 故障母线 |
| `scan.fault_type` | enum | 否 | three_phase | 故障类型 |
| `scan.clearing_times` | array | 是 | - | 清除时间列表(s) |
| `simulation.duration` | number | 否 | 10.0 | 仿真时长(s) |
| `output.format` | enum | 否 | json | json / csv |

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
