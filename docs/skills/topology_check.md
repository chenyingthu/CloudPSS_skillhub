# 拓扑检查技能 (Topology Check)

## 概述

拓扑检查技能用于检查电力系统模型的拓扑完整性和连通性，识别孤岛、悬空元件、参数缺失等问题。

## 功能特性

- **孤岛检测**: 识别电气上不相连的子系统
- **悬空检查**: 发现未连接任何支路的元件
- **参数检查**: 检查元件参数完整性
- **EMT就绪检查**: 验证模型是否可进行EMT仿真

## 设计原理

### 检查流程

```
1. 加载模型
2. 获取拓扑信息
3. 执行各项检查:
   a. 孤岛检测（连通分量分析）
   b. 悬空元件检测
   c. 参数完整性检查
   d. EMT配置检查
4. 汇总问题
5. 生成报告
```

## 快速开始

### 1. YAML配置

```yaml
skill: topology_check
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

checks:
  islands: true       # 检查孤岛
  dangling: true      # 检查悬空元件
  parameter: true     # 检查参数
  emt_ready: false    # 检查EMT就绪

output:
  format: json
  path: ./results/
  prefix: topology_check
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("topology_check")

config = {
    "skill": "topology_check",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE39"},
    "checks": {
        "islands": True,
        "dangling": True,
        "parameter": True,
        "emt_ready": False
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "topology_check" |
| `model.rid` | string | 是 | - | 模型RID |
| `checks.islands` | boolean | 否 | true | 检查孤岛 |
| `checks.dangling` | boolean | 否 | true | 检查悬空元件 |
| `checks.parameter` | boolean | 否 | true | 检查参数 |
| `checks.emt_ready` | boolean | 否 | false | 检查EMT就绪 |
| `output.format` | enum | 否 | json | json / yaml |
| `output.path` | string | 否 | ./results/ | 输出目录 |

## 输出结果

### JSON结果

```json
{
  "model_rid": "model/holdme/IEEE39",
  "timestamp": "2024-03-24T14:32:01",
  "summary": {
    "islands_count": 1,
    "dangling_count": 0,
    "parameter_issues": 0,
    "emt_ready": true
  },
  "details": {
    "islands": [...],
    "dangling": [...],
    "parameters": [...]
  }
}
```

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
