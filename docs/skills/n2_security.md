# N-2安全校核技能 (N-2 Security)

## 设计背景

### 研究对象

N-2安全校核是电力系统安全分析的极端场景评估方法，用于评估系统在同时失去两个元件（N-2故障）时的安全性。与N-1安全分析相比，N-2考虑的是更极端但概率较低的事件，如同一走廊的双回线同时故障、共因故障（地震、洪水等导致的多个设备同时退出）等。

### 实际需求

在电力系统规划和运行中，N-2安全校核用于：

1. **关键通道评估**：识别可能导致系统解列的关键输电通道
2. **极端工况分析**：评估系统在极端故障下的稳定性和安全性
3. **系统韧性评估**：量化系统在多重故障下的抗毁能力
4. **规划方案验证**：验证规划方案是否满足N-2安全准则
5. **运行方式调整**：识别需要特别关注的运行方式

### 期望的输入和输出

**输入**：

- 电力系统模型（需完成潮流收敛）
- 支路列表或支路对列表
- 电压安全限值（默认 0.95~1.05 pu）
- 设备热稳定限值（默认 1.0 pu）
- 最大检查组合数限制

**输出**：

- N-2故障场景列表及安全状态
- 电压越限信息
- 设备过载信息
- 关键故障对排序
- JSON格式的完整结果

### 计算结果的用途和价值

N-2校核结果可用于：

- **关键通道识别**：找出需要重点监控的输电通道
- **规划方案优化**：调整规划方案提高系统韧性
- **运行方式安排**：避免在关键通道重载时运行
- **应急响应准备**：制定N-2故障情况下的应急处置预案

## 功能特性

- **智能场景生成**：自动组合支路对或使用预定义的关键支路对
- **潮流收敛性校验**：验证N-2后系统是否能够保持潮流收敛
- **电压安全评估**：检查所有母线电压是否在允许范围内
- **设备过载检测**：检查支路和变压器负载是否超过限值
- **关键故障对排序**：按严重程度排序N-2故障场景
- **组合数量控制**：防止组合爆炸，控制计算规模
- **详细报告生成**：生成JSON格式的完整校核报告

## 快速开始

### 1. CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init n2_security --output n2_config.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config n2_config.yaml
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("n2_security")

config = {
    "skill": "n2_security",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "branches": ["LINE_1", "LINE_2"],  # 空列表表示全部支路
        "check_voltage": True,
        "check_thermal": True,
        "voltage_min": 0.95,
        "voltage_max": 1.05,
        "thermal_limit": 1.0,
        "max_combinations": 100,
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "n2_security",
    }
}

result = skill.run(config)
print(f"状态: {result.status}")
print(f"关键故障对: {result.data.get('critical_pairs', [])}")
```

### 3. YAML配置示例

```yaml
skill: n2_security
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  branches: []                    # 空表示全部支路
  branch_pairs: []                # 指定支路对（优先级高于branches）
  check_voltage: true             # 检查电压越限
  check_thermal: true             # 检查设备过载
  voltage_min: 0.95              # 电压下限(pu)
  voltage_max: 1.05              # 电压上限(pu)
  thermal_limit: 1.0             # 热稳定限值(pu)
  max_combinations: 100           # 最大检查组合数
  include_critical_pairs: true    # 包含关键支路对

output:
  format: json
  path: ./results/
  prefix: n2_security
```

## 配置Schema

### 完整配置结构

```yaml
skill: n2_security                   # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token
  token_file: string                  # token文件路径

model:                                # 模型配置（必需）
  rid: string                         # 模型RID或本地路径
  source: enum                        # cloud | local

analysis:                             # 分析配置
  branches: array                     # 要检查的支路列表
  branch_pairs: array                 # 指定支路对
  check_voltage: boolean             # 检查电压越限
  check_thermal: boolean             # 检查设备过载
  voltage_min: number                 # 电压下限(pu)
  voltage_max: number                 # 电压上限(pu)
  thermal_limit: number              # 热稳定限值(pu)
  max_combinations: integer           # 最大组合数
  include_critical_pairs: boolean     # 包含关键支路对

output:                              # 输出配置
  format: enum                        # json | console
  path: string                        # 输出目录
  prefix: string                      # 文件名前缀
```

### 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 必须为"n2_security" |
| `auth.token` | string | 否 | - | API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件 |
| `model.rid` | string | 是 | - | 模型RID |
| `model.source` | enum | 否 | cloud | 模型来源 |
| `analysis.branches` | array | 否 | [] | 支路列表 |
| `analysis.branch_pairs` | array | 否 | [] | 指定支路对 |
| `analysis.check_voltage` | boolean | 否 | true | 检查电压越限 |
| `analysis.check_thermal` | boolean | 否 | true | 检查设备过载 |
| `analysis.voltage_min` | number | 否 | 0.95 | 电压下限(pu) |
| `analysis.voltage_max` | number | 否 | 1.05 | 电压上限(pu) |
| `analysis.thermal_limit` | number | 否 | 1.0 | 热稳定限值(pu) |
| `analysis.max_combinations` | integer | 否 | 100 | 最大组合数 |
| `output.format` | enum | 否 | json | 输出格式 |

## Agent使用指南

### 基本调用模式

```python
from cloudpss_skills import get_skill

skill = get_skill("n2_security")

config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "max_combinations": 50,
    }
}

validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status.value == "SUCCESS":
        print(f"检查了 {result.data['total_scenarios']} 个场景")
```

### 处理结果

```python
result = skill.run(config)

if result.status.value == "SUCCESS":
    data = result.data
    
    # 摘要信息
    print(f"总场景数: {data['total_scenarios']}")
    print(f"通过: {data['passed_scenarios']}")
    print(f"失败: {data['failed_scenarios']}")
    
    # 关键故障对
    for pair in data.get("critical_pairs", []):
        print(f"  {pair['branch1']} + {pair['branch2']}: {pair['status']}")
        if pair.get('violations'):
            for v in pair['violations']:
                print(f"    - {v}")
    
    # 访问详细结果
    for artifact in result.artifacts:
        print(f"输出文件: {artifact.path}")
```

### 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    error_msg = result.error
    
    if "Token" in error_msg:
        print("错误: 请检查认证配置")
    elif "潮流" in error_msg.lower():
        print("错误: 基线潮流未收敛")
    elif "支路" in error_msg:
        print("错误: 未找到指定的支路")
    else:
        print(f"错误: {error_msg}")
```

## 输出结果

### JSON输出格式

```json
{
  "model_rid": "model/holdme/IEEE39",
  "total_scenarios": 50,
  "passed_scenarios": 45,
  "failed_scenarios": 5,
  "critical_pairs": [
    {
      "branch1": "LINE_1",
      "branch2": "LINE_2",
      "status": "failed",
      "converged": true,
      "violations": [
        {"type": "voltage", "bus": "Bus_5", "value": 0.92, "limit": 0.95},
        {"type": "thermal", "branch": "LINE_10", "value": 1.15, "limit": 1.0}
      ]
    }
  ],
  "summary": {
    "max_voltage_violation": 0.03,
    "max_thermal_violation": 0.15,
    "criticality_score": 8.5
  }
}
```

### SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | "n2_security" |
| `status` | SkillStatus | SUCCESS / FAILED |
| `data` | dict | 包含total_scenarios、critical_pairs等 |
| `artifacts` | list | JSON结果文件 |

## 与其他技能的关联

```
power_flow
    ↓ (基线潮流)
n1_security
    ↓ (N-1分析)
n2_security
    ↓ (N-2分析)
system_planning / operating_guide
```

### 依赖关系

- **前置依赖**: `power_flow`（基线潮流收敛）
- **相关技能**:
  - `n1_security`: N-1安全分析（基础）
  - `contingency_analysis`: 预想事故分析
  - `maintenance_security`: 检修安全分析

## 性能特点

- **计算时间**: 与支路组合数成正比
- **复杂度**: O(n²) 与支路数的平方成正比
- **建议**: 使用 `max_combinations` 控制规模
- **适用规模**: IEEE39系统约需检查1000+组合

## 常见问题

### 问题1: 组合数量过多

**原因**: 系统支路数较多时，N-2组合数量会爆炸式增长

**解决**:
```yaml
analysis:
  branches: [LINE_1, LINE_2, LINE_3]  # 只检查关键支路
  max_combinations: 50                  # 限制数量
```

### 问题2: 基线潮流不收敛

**原因**: 系统基础运行方式不合理

**解决**: 先运行 `power_flow` 确认潮流收敛

### 问题3: 所有场景都失败

**原因**: 电压限值或热稳定限值设置过严

**解决**:
```yaml
analysis:
  voltage_min: 0.90    # 放宽电压下限
  thermal_limit: 1.2     # 放宽热稳定限值
```

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2026-04-01
- **SDK要求**: cloudpss >= 4.5.28
