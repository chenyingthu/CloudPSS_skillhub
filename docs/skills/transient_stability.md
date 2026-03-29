# 暂态稳定分析技能 (Transient Stability)

## 概述

暂态稳定分析技能用于评估电力系统在遭受大扰动（如短路故障）后，同步发电机保持同步运行的能力。

## 功能特性

- **故障仿真**: 自动设置故障场景
- **摇摆曲线**: 生成发电机功角摇摆曲线
- **稳定判据**: 计算最大功角差判断稳定性
- **临界切除时间**: 估算故障临界切除时间

## 设计原理

### 暂态稳定性

系统受到大扰动后，各发电机维持同步运行的能力。

### 分析方法

```
1. 运行基础潮流
2. 设置故障场景
3. 运行EMT仿真
4. 提取发电机功角
5. 分析摇摆曲线
6. 判断稳定性
```

## 快速开始

### 1. YAML配置

```yaml
skill: transient_stability
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  fault_bus: Bus_16
  fault_type: three_phase
  fault_time: 1.0
  fault_duration: 0.1
  simulation_duration: 10.0

output:
  format: json
  path: ./results/
  prefix: transient_stability
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("transient_stability")

config = {
    "skill": "transient_stability",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "fault_bus": "Bus_16",
        "fault_type": "three_phase",
        "fault_time": 1.0
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "transient_stability" |
| `model.rid` | string | 是 | - | 模型RID |
| `analysis.fault_bus` | string | 是 | - | 故障母线 |
| `analysis.fault_type` | enum | 否 | three_phase | 故障类型 |
| `analysis.fault_time` | number | 否 | 1.0 | 故障时间(s) |
| `analysis.fault_duration` | number | 否 | 0.1 | 故障持续时间(s) |
| `analysis.simulation_duration` | number | 否 | 10.0 | 仿真时长(s) |
| `output.format` | enum | 否 | json | json / csv |

## 输出结果

### JSON结果

```json
{
  "model_rid": "model/holdme/IEEE39",
  "stable": true,
  "max_angle_diff": 120.5,
  "critical_gen": "Gen_1",
  "swing_curves": {
    "Gen_1": [[0.0, 30.0], [0.1, 35.0], ...]
  }
}
```

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
