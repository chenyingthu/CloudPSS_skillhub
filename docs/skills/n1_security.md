# N-1安全校核技能 (N-1 Security)

## 概述

N-1安全校核是电力系统安全分析的核心方法，逐一断开系统中的每条支路（线路或变压器），检查系统是否仍能保持安全稳定运行。本技能自动执行N-1校核流程，生成详细的校核报告。

## 功能特性

- **自动支路识别**: 自动识别系统中的线路和变压器
- **批量校核**: 逐一停运支路并运行潮流计算
- **安全评估**: 检查电压越限和热稳定约束
- **详细报告**: JSON格式的校核结果和统计信息

## 设计原理

### N-1准则

N-1安全准则要求：系统在正常运行方式下，失去任一条支路后，其他支路不过载，母线电压不越限。

### 校核流程

```
1. 加载原始模型
2. 识别所有支路（线路+变压器）
3. 对于每条支路:
   a. 重新加载模型（确保干净状态）
   b. 移除该支路
   c. 运行潮流计算
   d. 检查收敛性和约束
   e. 记录结果
4. 汇总统计（通过/失败数量）
5. 生成报告
```

## 快速开始

### 1. CLI方式

```bash
# 初始化配置
python -m cloudpss_skills init n1_security --output n1.yaml

# 运行
python -m cloudpss_skills run --config n1.yaml
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("n1_security")

config = {
    "skill": "n1_security",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "branches": [],           # 空列表表示全部支路
        "check_voltage": True,    # 检查电压约束
        "check_thermal": True,    # 检查热稳定约束
        "voltage_threshold": 0.05,
        "thermal_threshold": 1.0
    }
}

result = skill.run(config)
```

### 3. YAML配置

```yaml
skill: n1_security
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  branches: []              # 指定支路列表，空表示全部
  check_voltage: true
  check_thermal: true
  voltage_threshold: 0.05   # 电压越限阈值(标幺值)
  thermal_threshold: 1.0    # 热稳定阈值(标幺值)

output:
  format: json
  path: ./results/
  prefix: n1_security
  timestamp: true
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "n1_security" |
| `model.rid` | string | 是 | - | 模型RID |
| `model.source` | enum | 否 | cloud | cloud / local |
| `analysis.branches` | array | 否 | [] | 指定支路列表（空=全部） |
| `analysis.check_voltage` | boolean | 否 | true | 检查电压约束 |
| `analysis.check_thermal` | boolean | 否 | true | 检查热稳定约束 |
| `analysis.voltage_threshold` | number | 否 | 0.05 | 电压越限阈值 |
| `analysis.thermal_threshold` | number | 否 | 1.0 | 热稳定阈值 |
| `output.format` | enum | 否 | json | json / yaml |
| `output.path` | string | 否 | ./results/ | 输出目录 |
| `output.prefix` | string | 否 | n1_security | 文件名前缀 |
| `output.timestamp` | boolean | 否 | true | 添加时间戳 |

## Agent使用指南

### 基础调用

```python
skill = get_skill("n1_security")

config = {
    "model": {"rid": "model/holdme/IEEE39"}
}

result = skill.run(config)

if result.status.value == "SUCCESS":
    data = result.data
    summary = data["summary"]
    print(f"总支路: {summary['total_branches']}")
    print(f"通过: {summary['passed']}")
    print(f"失败: {summary['failed']}")
    print(f"通过率: {summary['pass_rate']*100:.1f}%")
```

### 检查失败支路

```python
result = skill.run(config)
data = result.data

# 获取失败支路
failed_branches = data.get("failed_branches", [])
for branch in failed_branches:
    print(f"失败支路: {branch['branch_name']}")
    print(f"  原因: {branch.get('violation', '未知')}")
```

## 输出结果

### JSON结果

```json
{
  "model_name": "IEEE39",
  "model_rid": "model/holdme/IEEE39",
  "timestamp": "2024-03-24T14:32:01",
  "summary": {
    "total_branches": 46,
    "passed": 44,
    "failed": 2,
    "pass_rate": 0.9565
  },
  "results": [
    {
      "branch_id": "Branch_1",
      "branch_name": "Line_1",
      "status": "passed",
      "converged": true,
      "violation": null
    },
    {
      "branch_id": "Branch_2",
      "branch_name": "Line_2",
      "status": "failed",
      "converged": false,
      "violation": "潮流不收敛"
    }
  ],
  "failed_branches": [
    {
      "branch_id": "Branch_2",
      "branch_name": "Line_2",
      "status": "failed",
      "violation": "潮流不收敛"
    }
  ]
}
```

## 与其他技能的关联

```
power_flow
    ↓ (潮流计算)
n1_security
    ↓ (N-1结果)
contingency_analysis, maintenance_security
```

## 性能特点

- **执行时间**: IEEE39系统约5-10分钟（46条支路）
- **时间比例**: 与支路数量成正比
- **内存占用**: 较低，每次重新加载模型
- **适用规模**: 已测试至200条支路

## 支路类型

自动识别的支路类型：

| 类型 | CloudPSS元件 |
|------|--------------|
| 单相线路 | model/CloudPSS/line |
| 三相线路 | model/CloudPSS/3pline |
| 单相变压器 | model/CloudPSS/transformer |
| 三相变压器 | model/CloudPSS/3ptransformer |

## 常见问题

### 问题1: 校核时间过长

**原因**: 支路数量多或系统复杂

**解决**: 只检查关键支路
```yaml
analysis:
  branches:
    - "Line_1"
    - "Line_2"
    - "Transformer_1"
```

### 问题2: 潮流频繁不收敛

**原因**: 系统本身较脆弱

**解决**: 调整阈值或检查模型数据
```yaml
analysis:
  voltage_threshold: 0.1   # 放宽电压约束
```

## 配置示例

### 基础配置

```yaml
skill: n1_security
model:
  rid: model/holdme/IEEE39
```

### 只检查特定支路

```yaml
skill: n1_security
model:
  rid: model/holdme/IEEE39
analysis:
  branches:
    - "Line_1"
    - "Line_2"
    - "Transformer_Main"
```

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
