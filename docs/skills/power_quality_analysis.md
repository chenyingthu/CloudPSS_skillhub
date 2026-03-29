# 电能质量分析技能 (Power Quality Analysis)

## 概述

电能质量分析技能用于综合评估电力系统的电能质量，包括电压质量、频率质量、波形质量等多维度分析。

## 功能特性

- **电压质量**: 电压偏差、波动、闪变分析
- **频率质量**: 频率偏差、变化率分析
- **谐波分析**: 谐波畸变率、间谐波分析
- **三相不平衡**: 三相电压电流不平衡度
- **综合评估**: 电能质量综合指标

## 快速开始

### 1. YAML配置

```yaml
skill: power_quality_analysis
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  voltage_limits:             # 电压限值
    min: 0.95
    max: 1.05
  frequency_limits:           # 频率限值
    min: 49.5
    max: 50.5
  thd_limits:                 # THD限值
    voltage: 0.05
    current: 0.08

output:
  format: json
  path: ./results/
  prefix: power_quality
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("power_quality_analysis")

config = {
    "skill": "power_quality_analysis",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "voltage_limits": {"min": 0.95, "max": 1.05}
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "power_quality_analysis" |
| `model.rid` | string | 是 | - | 模型RID |
| `analysis.voltage_limits` | object | 否 | - | 电压限值 |
| `analysis.frequency_limits` | object | 否 | - | 频率限值 |
| `analysis.thd_limits` | object | 否 | - | THD限值 |
| `output.format` | enum | 否 | json | json / csv |

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
