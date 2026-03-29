# EMT N-1安全筛查技能 (EMT N-1 Screening)

## 概述

EMT N-1安全筛查技能用于通过EMT暂态仿真进行N-1安全分析，评估系统在N-1故障后的暂态稳定性。

## 功能特性

- **批量EMT仿真**: 对N-1场景批量运行EMT
- **稳定性评估**: 评估故障后系统暂态稳定性
- **故障分类**: 按严重程度分类故障场景
- **详细报告**: 生成筛查报告

## 快速开始

### 1. YAML配置

```yaml
skill: emt_n1_screening
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

analysis:
  branches: []              # 筛查支路，空表示全部
  fault_duration: 0.1       # 故障持续时间(s)
  simulation_duration: 10.0 # 仿真时长(s)

output:
  format: json
  path: ./results/
  prefix: emt_n1
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("emt_n1_screening")

config = {
    "skill": "emt_n1_screening",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE3"}
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "emt_n1_screening" |
| `model.rid` | string | 是 | - | 模型RID |
| `analysis.branches` | array | 否 | [] | 筛查支路列表 |
| `analysis.fault_duration` | number | 否 | 0.1 | 故障持续时间(s) |
| `analysis.simulation_duration` | number | 否 | 10.0 | 仿真时长(s) |
| `output.format` | enum | 否 | json | json / csv |

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
