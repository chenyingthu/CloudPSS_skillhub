# 潮流计算技能 (Power Flow)

## 概述

潮流计算是电力系统分析的基础，用于计算系统在给定运行条件下的稳态电压、功率分布和损耗。本技能基于牛顿-拉夫逊法或快速解耦法，求解非线性潮流方程。

## 功能特性

- **多种算法支持**: 牛顿-拉夫逊法、快速解耦法
- **自动收敛控制**: 自适应迭代次数和收敛精度
- **完整结果输出**: 母线电压、支路潮流、网损等
- **云模型支持**: 支持CloudPSS云端模型和本地YAML模型

## 设计原理

### 数学基础

潮流计算求解以下非线性方程组：

```
Pi = Vi × Σ(Vj × (Gij×cosθij + Bij×sinθij))
Qi = Vi × Σ(Vj × (Gij×sinθij - Bij×cosθij))
```

其中：
- `Pi`, `Qi`: 节点i的有功和无功注入
- `Vi`, `Vj`: 节点电压幅值
- `θij`: 节点相角差
- `Gij`, `Bij`: 导纳矩阵元素

### 算法选择

| 算法 | 适用场景 | 收敛特性 |
|------|----------|----------|
| 牛顿-拉夫逊 | 通用场景 | 二次收敛，快速 |
| 快速解耦 | 高压系统 | 线性收敛，内存小 |

## 快速开始

### 1. CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init power_flow --output pf.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config pf.yaml
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("power_flow")

# 配置
config = {
    "skill": "power_flow",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "algorithm": {
        "type": "newton_raphson",
        "tolerance": 1e-6,
        "max_iterations": 100
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "power_flow",
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

### 3. YAML配置示例

```yaml
skill: power_flow
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud  # 或 local

algorithm:
  type: newton_raphson  # 或 fast_decoupled
  tolerance: 1.0e-6
  max_iterations: 100

output:
  format: json
  path: ./results/
  prefix: power_flow
  timestamp: true
```

## 配置Schema

### 完整配置结构

```yaml
skill: power_flow                    # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token（不推荐）
  token_file: string                  # token文件路径（默认: .cloudpss_token）

model:                                # 模型配置（必需）
  rid: string                         # 模型RID或本地路径（必需）
  source: enum                        # cloud | local（默认: cloud）

algorithm:                            # 算法配置
  type: enum                          # newton_raphson | fast_decoupled（默认: newton_raphson）
  tolerance: number                   # 收敛精度（默认: 1e-6）
  max_iterations: integer             # 最大迭代次数（默认: 100）

output:                               # 输出配置
  format: enum                        # json | yaml | csv（默认: json）
  path: string                        # 输出目录（默认: ./results/）
  prefix: string                      # 文件名前缀（默认: power_flow）
  timestamp: boolean                  # 是否添加时间戳（默认: true）
```

### 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"power_flow" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `algorithm.type` | enum | 否 | newton_raphson | 算法类型 |
| `algorithm.tolerance` | number | 否 | 1e-6 | 收敛精度阈值 |
| `algorithm.max_iterations` | integer | 否 | 100 | 最大迭代次数 |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | power_flow | 文件名前缀 |
| `output.timestamp` | boolean | 否 | true | 文件名是否包含时间戳 |

## Agent使用指南

### 基本调用模式

```python
# 获取技能实例
skill = get_skill("power_flow")

# 最小化配置（使用默认值）
config = {
    "model": {"rid": "model/holdme/IEEE39"}
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status == "SUCCESS":
        print(f"计算完成: {result.data}")
    else:
        print(f"计算失败: {result.error}")
```

### 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data
    # 访问结果数据
    model_name = data.get("model")
    converged = data.get("converged")
    job_id = data.get("job_id")

    # 访问输出文件
    for artifact in result.artifacts:
        print(f"输出文件: {artifact.path} ({artifact.type})")

# 查看日志
for log in result.logs:
    print(f"[{log.level}] {log.message}")
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
    elif "潮流不收敛" in error_msg:
        print("错误: 系统可能无解，尝试调整算法参数")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### JSON输出格式

```json
{
  "model": "IEEE39",
  "model_rid": "model/holdme/IEEE39",
  "job_id": "job_xxx",
  "converged": true,
  "timestamp": "2024-03-24T14:32:01"
}
```

### SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "power_flow" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典 |
| `artifacts` | list | 输出文件列表（Artifact对象） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标 |

## 与其他技能的关联

```
power_flow
    ↓ (潮流结果)
n1_security, maintenance_security
    ↓ (N-1分析结果)
param_scan
    ↓ (参数扫描)
voltage_stability
    ↓ (电压稳定分析)
reactive_compensation_design
```

## 依赖关系

- **必需依赖**: CloudPSS SDK (`cloudpss`)
- **输入依赖**: 无（直接使用模型）
- **输出被依赖**:
  - `n1_security`: 需要潮流计算结果
  - `voltage_stability`: 电压稳定分析基础
  - `contingency_analysis`: 预想事故分析

## 性能特点

- **执行时间**: IEEE39系统约5-15秒
- **内存占用**: 与系统规模成正比
- **收敛率**: 正常系统>99%
- **适用规模**: 已测试至500节点系统

## 常见问题

### 问题1: 潮流不收敛

**原因**:
- 系统数据错误
- 负荷过重
- 缺少无功支撑

**解决**:
```yaml
algorithm:
  type: newton_raphson
  tolerance: 1e-4    # 放宽收敛条件
  max_iterations: 200  # 增加迭代次数
```

### 问题2: Token认证失败

**原因**: Token文件不存在或内容错误

**解决**:
```bash
echo "your_token" > .cloudpss_token
chmod 600 .cloudpss_token
```

### 问题3: 模型无法加载

**原因**:
- RID错误
- 网络问题
- 无访问权限

**解决**:
- 确认模型RID格式: `model/holdme/IEEE39`
- 使用本地模型: `source: local`

## 配置示例

### 基础配置

```yaml
skill: power_flow
model:
  rid: model/holdme/IEEE39
```

### 完整配置

```yaml
skill: power_flow
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
  source: cloud
algorithm:
  type: newton_raphson
  tolerance: 1.0e-6
  max_iterations: 100
output:
  format: json
  path: ./results/
  prefix: pf_ieee39
  timestamp: true
```

### 使用本地模型

```yaml
skill: power_flow
model:
  rid: ./models/my_model.yaml
  source: local
```

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
