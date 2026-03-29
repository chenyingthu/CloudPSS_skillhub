# 参数灵敏度分析技能 (Parameter Sensitivity)

## 概述

参数灵敏度分析技能用于分析系统响应随参数变化的灵敏度，识别关键参数。

## 功能特性

- **参数扰动**: 对指定参数进行扰动
- **灵敏度计算**: 计算输出对参数的灵敏度
- **关键参数识别**: 识别影响最大的参数
- **排序报告**: 按灵敏度排序参数

## 快速开始

### 1. YAML配置

```yaml
skill: parameter_sensitivity
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  target_parameters:          # 目标参数列表
    - component: Load_1
      parameter: P
      perturbation: 0.1      # 扰动幅度
  output_metrics:             # 输出指标
    - voltage_at: Bus_16
    - power_flow: Line_1

output:
  format: json
  path: ./results/
  prefix: sensitivity
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("parameter_sensitivity")

config = {
    "skill": "parameter_sensitivity",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "target_parameters": [
            {"component": "Load_1", "parameter": "P", "perturbation": 0.1}
        ]
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "parameter_sensitivity" |
| `model.rid` | string | 是 | - | 模型RID |
| `analysis.target_parameters` | array | 是 | - | 目标参数列表 |
| `analysis.output_metrics` | array | 否 | - | 输出指标列表 |
| `output.format` | enum | 否 | json | json / csv |

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
