# EMT故障研究技能 (EMT Fault Study)

## 概述

EMT故障研究技能用于进行详细的EMT暂态仿真故障分析，支持多种故障类型和故障位置，分析系统故障响应。

## 功能特性

- **多种故障场景**: 三相、单相、两相故障
- **故障位置灵活**: 可设置任意母线故障
- **故障时序控制**: 精确控制故障开始和结束时间
- **波形记录**: 记录故障期间的详细波形

## 设计原理

### 故障仿真流程

```
1. 加载模型
2. 配置故障参数
3. 添加故障元件
4. 运行EMT仿真
5. 提取故障期间波形
6. 分析故障响应
```

## 快速开始

### 1. YAML配置

```yaml
skill: emt_fault_study
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

fault:
  bus: Bus_1
  type: three_phase
  start_time: 2.0
  duration: 0.1

simulation:
  duration: 10.0
  step_size: 0.0001

output:
  format: csv
  path: ./results/
  prefix: fault_study
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("emt_fault_study")

config = {
    "skill": "emt_fault_study",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE3"},
    "fault": {
        "bus": "Bus_1",
        "type": "three_phase",
        "start_time": 2.0,
        "duration": 0.1
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "emt_fault_study" |
| `model.rid` | string | 是 | - | 模型RID |
| `fault.bus` | string | 是 | - | 故障母线 |
| `fault.type` | enum | 否 | three_phase | 故障类型 |
| `fault.start_time` | number | 否 | 2.0 | 故障开始时间(s) |
| `fault.duration` | number | 否 | 0.1 | 故障持续时间(s) |
| `simulation.duration` | number | 否 | 10.0 | 仿真时长(s) |
| `simulation.step_size` | number | 否 | 0.0001 | 仿真步长(s) |
| `output.format` | enum | 否 | csv | csv / json |

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
