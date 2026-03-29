# 检修方式安全校核技能 (Maintenance Security)

## 概述

检修方式安全校核技能用于评估系统在检修方式下的安全性，检查检修期间系统是否满足N-1准则。

## 功能特性

- **检修场景**: 模拟设备检修停运
- **N-1校核**: 检修方式下的N-1安全校核
- **安全评估**: 评估检修期间系统安全性
- **操作建议**: 提供检修安排建议

## 快速开始

### 1. YAML配置

```yaml
skill: maintenance_security
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  maintenance_outages:        # 检修设备列表
    - type: line
      id: Line_1
    - type: generator
      id: Gen_1
  check_n1: true              # 检修方式下N-1校核

output:
  format: json
  path: ./results/
  prefix: maintenance
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("maintenance_security")

config = {
    "skill": "maintenance_security",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "maintenance_outages": [
            {"type": "line", "id": "Line_1"}
        ]
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "maintenance_security" |
| `model.rid` | string | 是 | - | 模型RID |
| `analysis.maintenance_outages` | array | 是 | - | 检修设备列表 |
| `analysis.check_n1` | boolean | 否 | true | 检修方式N-1校核 |
| `output.format` | enum | 否 | json | json / csv |

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
