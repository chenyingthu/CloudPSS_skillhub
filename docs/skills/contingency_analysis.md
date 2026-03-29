# 预想事故分析技能 (Contingency Analysis)

## 概述

预想事故分析技能用于批量分析多种预想事故场景，评估系统在各种故障条件下的安全性。

## 功能特性

- **批量场景**: 支持多种预想事故场景
- **安全评估**: 评估每种场景的系统安全性
- **风险排序**: 按风险程度排序事故场景
- **详细报告**: 生成分析报告和建议

## 快速开始

### 1. YAML配置

```yaml
skill: contingency_analysis
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  contingencies:              # 预想事故列表
    - type: line_outage
      elements: ["Line_1"]
    - type: generator_outage
      elements: ["Gen_1"]
  check_voltage: true
  check_thermal: true

output:
  format: json
  path: ./results/
  prefix: contingency
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("contingency_analysis")

config = {
    "skill": "contingency_analysis",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "contingencies": [
            {"type": "line_outage", "elements": ["Line_1"]}
        ]
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "contingency_analysis" |
| `model.rid` | string | 是 | - | 模型RID |
| `analysis.contingencies` | array | 是 | - | 预想事故列表 |
| `analysis.check_voltage` | boolean | 否 | true | 检查电压约束 |
| `analysis.check_thermal` | boolean | 否 | true | 检查热稳定约束 |
| `output.format` | enum | 否 | json | json / csv |

## 事故类型

| 类型 | 说明 |
|------|------|
| line_outage | 线路停运 |
| generator_outage | 发电机停运 |
| transformer_outage | 变压器停运 |
| bus_fault | 母线故障 |

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
