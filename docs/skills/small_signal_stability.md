# 小信号稳定分析技能 (Small Signal Stability)

## 概述

小信号稳定分析技能用于评估电力系统在受到小扰动后，恢复到稳态运行的能力。通过特征值分析判断系统振荡模式。

## 功能特性

- **特征值分析**: 计算系统状态矩阵特征值
- **振荡模式识别**: 识别机电振荡模式
- **阻尼比计算**: 评估各模式的阻尼水平
- **参与因子分析**: 识别影响振荡模式的关键元件

## 设计原理

### 小信号稳定性

系统在平衡点线性化后的动态特性：

```
Δx' = A * Δx
```

通过分析矩阵A的特征值判断稳定性。

## 快速开始

### 1. YAML配置

```yaml
skill: small_signal_stability
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  modes_count: 20         # 计算的特征值数量
  min_damping_ratio: 0.05 # 最小阻尼比阈值
  frequency_range: [0.1, 5.0]  # 频率范围(Hz)

output:
  format: json
  path: ./results/
  prefix: small_signal
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("small_signal_stability")

config = {
    "skill": "small_signal_stability",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "modes_count": 20,
        "min_damping_ratio": 0.05
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "small_signal_stability" |
| `model.rid` | string | 是 | - | 模型RID |
| `analysis.modes_count` | integer | 否 | 20 | 特征值数量 |
| `analysis.min_damping_ratio` | number | 否 | 0.05 | 最小阻尼比 |
| `analysis.frequency_range` | array | 否 | [0.1, 5.0] | 频率范围 |
| `output.format` | enum | 否 | json | json / csv |

## 输出结果

### JSON结果

```json
{
  "model_rid": "model/holdme/IEEE39",
  "eigenvalues": [
    {"real": -0.5, "imag": 6.28, "damping": 0.08, "frequency": 1.0}
  ],
  "unstable_modes": [],
  "weakly_damped_modes": [
    {"frequency": 0.5, "damping": 0.03, "gens": ["Gen_1", "Gen_2"]}
  ]
}
```

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
