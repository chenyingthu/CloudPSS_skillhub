# 频率响应分析技能 (Frequency Response)

## 概述

频率响应分析技能用于评估电力系统在功率不平衡情况下的频率动态响应特性，分析系统的频率稳定性和控制性能。

## 功能特性

- **频率仿真**: 模拟功率扰动后的频率变化
- **频率指标**: 计算频率最低点、变化率等指标
- **惯量评估**: 评估系统等效惯量
- **一次调频分析**: 分析一次调频响应

## 设计原理

### 频率响应

系统频率由功率平衡决定：

```
2H * df/dt = Pm - Pe
```

其中H为惯性时间常数，Pm为机械功率，Pe为电磁功率。

## 快速开始

### 1. YAML配置

```yaml
skill: frequency_response
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  disturbance_bus: Bus_16
  disturbance_mw: 100.0       # 扰动功率(MW)
  disturbance_time: 1.0       # 扰动时间(s)
  simulation_duration: 30.0   # 仿真时长(s)

output:
  format: json
  path: ./results/
  prefix: frequency_response
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("frequency_response")

config = {
    "skill": "frequency_response",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "disturbance_mw": 100.0,
        "disturbance_time": 1.0
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "frequency_response" |
| `model.rid` | string | 是 | - | 模型RID |
| `analysis.disturbance_bus` | string | 是 | - | 扰动母线 |
| `analysis.disturbance_mw` | number | 是 | - | 扰动功率(MW) |
| `analysis.disturbance_time` | number | 否 | 1.0 | 扰动时间(s) |
| `analysis.simulation_duration` | number | 否 | 30.0 | 仿真时长(s) |
| `output.format` | enum | 否 | json | json / csv |

## 输出结果

### JSON结果

```json
{
  "model_rid": "model/holdme/IEEE39",
  "frequency_nadir": 49.2,
  "rocof": -0.5,
  "settling_time": 15.0,
  "steady_state_freq": 49.8,
  "equivalent_inertia": 5.2
}
```

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
