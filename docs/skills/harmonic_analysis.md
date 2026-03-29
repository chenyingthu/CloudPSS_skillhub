# 谐波分析技能 (Harmonic Analysis)

## 概述

谐波分析技能用于评估电力系统的谐波分布，识别谐波源和谐波放大问题。

## 功能特性

- **谐波潮流**: 计算各次谐波的电压电流分布
- **谐波阻抗扫描**: 分析系统谐波阻抗频率特性
- **谐波畸变率**: 计算THD（总谐波畸变率）
- **谐波源建模**: 支持多种谐波源模型

## 快速开始

### 1. YAML配置

```yaml
skill: harmonic_analysis
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  harmonics: [3, 5, 7, 11, 13]  # 分析次数
  base_frequency: 50            # 基波频率(Hz)
  harmonic_sources:             # 谐波源
    - bus: Bus_16
      harmonics: {3: 0.1, 5: 0.05}

output:
  format: json
  path: ./results/
  prefix: harmonic
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("harmonic_analysis")

config = {
    "skill": "harmonic_analysis",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "harmonics": [3, 5, 7, 11, 13]
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "harmonic_analysis" |
| `model.rid` | string | 是 | - | 模型RID |
| `analysis.harmonics` | array | 是 | - | 谐波次数列表 |
| `analysis.base_frequency` | number | 否 | 50 | 基波频率(Hz) |
| `analysis.harmonic_sources` | array | 否 | [] | 谐波源配置 |
| `output.format` | enum | 否 | json | json / csv |

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
