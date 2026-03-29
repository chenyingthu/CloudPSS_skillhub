# N-1安全校核技能 (N-1 Security)

## 设计背景

### 研究对象
N-1安全校核是电力系统安全分析的核心方法，用于评估系统在N-1故障条件下的安全性。N-1准则要求：系统在正常运行方式下，失去任一条支路（线路或变压器）后，其他支路不过载，母线电压不越限，系统仍能安全稳定运行。

### 实际需求
在电力系统规划和运行中，需要：
1. **规划设计阶段**：评估网架结构的N-1安全性，识别薄弱环节
2. **运行方式安排**：制定满足N-1准则的运行方案
3. **检修计划编制**：评估检修期间的系统安全裕度
4. **事故预案制定**：识别关键设备和关键故障场景

### 期望的输入和输出

**输入**:
- 电力系统模型（IEEE39等标准系统或实际系统）
- 支路筛选条件（指定检查特定支路或全部支路）
- 安全约束阈值（电压越限阈值、热稳定阈值）
- 校核类型（电压约束、热稳定约束）

**输出**:
- 各支路N-1校核结果（通过/失败）
- 失败支路的详细原因（潮流不收敛、电压越限、热稳定越限）
- 统计摘要（通过率、失败率）
- JSON/CSV格式的详细报告

### 计算结果的用途和价值
N-1校核结果可直接用于：
- **网架规划**：识别不满足N-1准则的支路，指导网架加强
- **运行控制**：制定关键设备的运行监视策略
- **保护配置**：针对N-1薄弱场景优化保护定值
- **事故预案**：预先制定N-1故障后的处置方案

## 功能特性

- **自动支路识别**: 自动识别系统中的线路和变压器
- **批量校核**: 逐一停运支路并运行潮流计算
- **安全评估**: 检查电压越限和热稳定约束
- **灵活配置**: 支持全部校核或指定支路校核
- **详细报告**: JSON格式的校核结果和统计信息
- **结果可视化**: 生成通过率统计和失败支路列表

## 快速开始

### CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init n1_security --output n1.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config n1.yaml
```

### Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("n1_security")

# 配置
config = {
    "skill": "n1_security",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "analysis": {
        "branches": [],           # 空列表表示全部支路
        "check_voltage": True,    # 检查电压约束
        "check_thermal": True,    # 检查热稳定约束
        "voltage_threshold": 0.05,  # 电压越限阈值(标幺值)
        "thermal_threshold": 1.0   # 热稳定阈值(标幺值)
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "n1_security",
        "timestamp": True
    }
}

# 验证配置
validation = skill.validate(config)
if not validation.valid:
    print("配置错误:", validation.errors)

# 运行
result = skill.run(config)
print(f"状态: {result.status}")
print(f"数据: {result.data}")
```

### YAML配置示例

```yaml
skill: n1_security
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud  # 或 local

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

### 完整配置结构

```yaml
skill: n1_security                    # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token（不推荐）
  token_file: string                  # token文件路径（默认: .cloudpss_token）

model:                                # 模型配置（必需）
  rid: string                         # 模型RID或本地路径（必需）
  source: enum                        # cloud | local（默认: cloud）

analysis:                             # 分析配置
  branches:                           # 要检查的支路列表
    - string                          # 支路名称或ID
  check_voltage: boolean              # 检查电压约束（默认: true）
  check_thermal: boolean              # 检查热稳定约束（默认: true）
  voltage_threshold: number           # 电压越限阈值（默认: 0.05）
  thermal_threshold: number           # 热稳定阈值（默认: 1.0）

output:                               # 输出配置
  format: enum                        # json | yaml（默认: json）
  path: string                        # 输出目录（默认: ./results/）
  prefix: string                      # 文件名前缀（默认: n1_security）
  timestamp: boolean                  # 是否添加时间戳（默认: true）
```

### 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"n1_security" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `analysis.branches` | array | 否 | [] | 指定支路列表，空表示全部 |
| `analysis.check_voltage` | boolean | 否 | true | 检查电压约束 |
| `analysis.check_thermal` | boolean | 否 | true | 检查热稳定约束 |
| `analysis.voltage_threshold` | number | 否 | 0.05 | 电压越限阈值(标幺值) |
| `analysis.thermal_threshold` | number | 否 | 1.0 | 热稳定阈值(标幺值) |
| `output.format` | enum | 否 | json | 输出格式：json / yaml |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | n1_security | 文件名前缀 |
| `output.timestamp` | boolean | 否 | true | 文件名是否包含时间戳 |

## Agent使用指南

### 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("n1_security")

# 最小化配置（使用默认值）
config = {
    "model": {"rid": "model/holdme/IEEE39"}
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status.value == "SUCCESS":
        print(f"校核完成: {result.data}")
    else:
        print(f"校核失败: {result.error}")
```

### 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data
    summary = data["summary"]
    print(f"总支路: {summary['total_branches']}")
    print(f"通过: {summary['passed']}")
    print(f"失败: {summary['failed']}")
    print(f"通过率: {summary['pass_rate']*100:.1f}%")

    # 访问失败支路
    failed_branches = data.get("failed_branches", [])
    for branch in failed_branches:
        print(f"失败支路: {branch['branch_name']}")
        print(f"  原因: {branch.get('violation', '未知')}")

# 查看日志
for log in result.logs:
    print(f"[{log.level}] {log.message}")

# 访问输出文件
for artifact in result.artifacts:
    print(f"输出文件: {artifact.path} ({artifact.type})")
```

### 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    error_msg = result.error

    # 常见错误处理
    if "Token文件不存在" in error_msg:
        print("错误: 请创建.cloudpss_token文件")
    elif "模型不存在" in error_msg:
        print("错误: 请检查模型RID是否正确")
    elif "支路" in error_msg:
        print("错误: 指定的支路不存在")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### JSON输出格式

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

### SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "n1_security" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典（包含summary, results, failed_branches） |
| `artifacts` | list | 输出文件列表（Artifact对象） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标（total_branches, passed, failed） |

## 设计原理

### N-1准则

N-1安全准则要求：系统在正常运行方式下，失去任一条支路后，其他支路不过载，母线电压不越限。

### 校核流程

```
1. 加载原始模型
2. 识别所有支路元件（线路+变压器）
3. 对于每条支路:
   a. 重新加载模型（确保干净状态）
   b. 移除该支路
   c. 运行潮流计算
   d. 检查收敛性和约束
   e. 记录结果
4. 汇总统计（通过/失败数量）
5. 生成报告
```

### 支路类型

自动识别的支路类型：

| 类型 | CloudPSS元件 |
|------|--------------|
| 单相线路 | model/CloudPSS/line |
| 三相线路 | model/CloudPSS/3pline |
| 单相变压器 | model/CloudPSS/transformer |
| 三相变压器 | model/CloudPSS/3ptransformer |

## 与其他技能的关联

```
power_flow
    ↓ (潮流计算)
n1_security
    ↓ (N-1结果)
contingency_analysis, maintenance_security
    ↓ (综合分析)
reactive_compensation_design
```

### 依赖关系

- **必需依赖**: CloudPSS SDK (`cloudpss`)
- **输入依赖**: 需要`power_flow`技能进行潮流计算
- **输出被依赖**:
  - `contingency_analysis`: 扩展N-1分析
  - `maintenance_security`: 检修方式安全校核

## 性能特点

- **执行时间**: IEEE39系统约5-10分钟（46条支路）
- **时间比例**: 与支路数量成正比
- **内存占用**: 较低，每次重新加载模型
- **适用规模**: 已测试至200条支路
- **并发能力**: 串行执行，每支路独立校核

## 常见问题

### 问题1: 校核时间过长

**原因**:
- 支路数量多
- 系统复杂，潮流计算收敛慢

**解决**: 只检查关键支路
```yaml
analysis:
  branches:
    - "Line_1"
    - "Line_2"
    - "Transformer_Main"
```

### 问题2: 潮流频繁不收敛

**原因**:
- 系统本身较脆弱
- 某些支路停运后系统无解

**解决**: 调整分析阈值或检查模型数据
```yaml
analysis:
  voltage_threshold: 0.1   # 放宽电压约束
  thermal_threshold: 1.2   # 放宽热稳定约束
```

### 问题3: 特定支路识别不到

**原因**:
- 支路名称拼写错误
- 该支路不是线路或变压器类型

**解决**: 先运行一次全支路校核，查看输出的支路名称列表
```python
result = skill.run(config)
data = result.data
for r in data["results"]:
    print(f"支路: {r['branch_name']} (ID: {r['branch_id']})")
```

### 问题4: 结果文件未生成

**原因**:
- 输出目录不存在
- 磁盘空间不足

**解决**: 确保输出目录存在且有写入权限
```bash
mkdir -p ./results/
chmod 755 ./results/
```

## 完整示例

### 场景描述

某电力公司需要对IEEE39系统进行N-1安全校核，评估系统在失去任一条支路后的安全性，识别不满足N-1准则的薄弱环节。

### 配置文件

```yaml
skill: n1_security
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  branches: []              # 空列表表示全部支路
  check_voltage: true
  check_thermal: true
  voltage_threshold: 0.05   # 电压越限阈值
  thermal_threshold: 1.0    # 热稳定阈值

output:
  format: json
  path: ./results/
  prefix: n1_ieee39
  timestamp: true
```

### 执行命令

```bash
python -m cloudpss_skills run --config n1_config.yaml
```

### 预期输出

```
[INFO] 加载认证信息...
[INFO] 认证成功
[INFO] 获取模型: IEEE39
[INFO] 发现46条支路
[INFO] 开始N-1校核...
[INFO] [1/46] 停运支路: Line_1...
[INFO]  -> N-1通过
[INFO] [2/46] 停运支路: Line_2...
[INFO]  -> N-1通过
...
[INFO] [45/46] 停运支路: Transformer_1...
[INFO]  -> N-1通过
[INFO] [46/46] 停运支路: Transformer_2...
[INFO]  -> N-1失败: 潮流不收敛
[INFO] ==================================================
[INFO] N-1校核完成: 通过 45, 失败 1
[INFO] 通过率: 97.8%
[INFO] 结果已保存: ./results/n1_ieee39_20240324_143245_result.json
```

### 结果文件

```json
{
  "model_name": "IEEE39",
  "model_rid": "model/holdme/IEEE39",
  "timestamp": "2024-03-24T14:32:45",
  "summary": {
    "total_branches": 46,
    "passed": 45,
    "failed": 1,
    "pass_rate": 0.9783
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
      "branch_id": "Branch_46",
      "branch_name": "Transformer_2",
      "status": "failed",
      "converged": false,
      "violation": "潮流不收敛"
    }
  ],
  "failed_branches": [
    {
      "branch_id": "Branch_46",
      "branch_name": "Transformer_2",
      "status": "failed",
      "violation": "潮流不收敛"
    }
  ]
}
```

### 后续应用

基于N-1校核结果，可以：
1. **网架加强**: 针对N-1失败的支路，评估加强方案
2. **运行方式优化**: 避免在N-1薄弱时段安排检修
3. **保护配置**: 针对N-1薄弱场景优化保护定值
4. **应急演练**: 基于N-1结果制定事故预案

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
