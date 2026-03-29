# 批量潮流计算技能 (Batch Power Flow)

## 概述

批量潮流计算技能用于对多个模型批量运行潮流计算，适合多场景对比分析或大规模系统评估。

## 功能特性

- **多模型批量**: 支持多个模型顺序计算
- **汇总报告**: 生成批量计算的汇总统计
- **失败处理**: 单个模型失败不影响其他模型
- **算法配置**: 可配置潮流算法参数

## 快速开始

### 1. YAML配置

```yaml
skill: batch_powerflow
auth:
  token_file: .cloudpss_token

models:
  - rid: model/holdme/IEEE39
    name: IEEE39
  - rid: model/holdme/IEEE3
    name: IEEE3

algorithm:
  type: newton_raphson
  tolerance: 1e-6

output:
  format: json
  path: ./results/
  prefix: batch_pf
  aggregate: true    # 生成汇总报告
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("batch_powerflow")

config = {
    "skill": "batch_powerflow",
    "auth": {"token_file": ".cloudpss_token"},
    "models": [
        {"rid": "model/holdme/IEEE39", "name": "IEEE39"},
        {"rid": "model/holdme/IEEE3", "name": "IEEE3"}
    ]
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "batch_powerflow" |
| `models` | array | 是 | - | 模型列表 |
| `models[].rid` | string | 是 | - | 模型RID |
| `models[].name` | string | 否 | - | 模型名称 |
| `algorithm.type` | enum | 否 | newton_raphson | 算法类型 |
| `algorithm.tolerance` | number | 否 | 1e-6 | 收敛精度 |
| `output.format` | enum | 否 | json | json / csv |
| `output.aggregate` | boolean | 否 | true | 生成汇总报告 |

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
