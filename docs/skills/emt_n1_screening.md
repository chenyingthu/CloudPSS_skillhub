# EMT N-1安全筛查技能 (EMT N-1 Screening)

## 设计背景

### 研究对象
EMT（Electromagnetic Transient）N-1安全筛查是电力系统暂态安全分析的重要方法。与稳态N-1校核不同，EMT N-1筛查通过电磁暂态仿真评估系统在支路停运并伴随故障时的暂态稳定性，能够捕捉到稳态分析无法发现的暂态电压崩溃、功角失稳等问题。

### 实际需求
在电力系统规划和运行中，需要：
1. **暂态安全评估**: 评估系统在N-1故障下的暂态稳定性
2. **薄弱环节识别**: 发现暂态稳定性薄弱的设备和运行方式
3. **故障严重程度排序**: 按暂态后果严重程度排序故障场景
4. **保护定值校核**: 验证保护配置在N-1故障下的适应性
5. **运行方式优化**: 识别需要特殊运行控制的场景

### 期望的输入和输出

**输入**:
- 电力系统模型（支持EMT仿真的模型）
- 筛查支路列表（可自动发现）
- 故障配置（故障开始时间、持续时间、阻抗）
- 监测母线（用于评估暂态响应）
- 时间窗口配置（故障前、故障中、故障后）
- 严重程度阈值（警告和临界阈值）

**输出**:
- 基线工况（无支路停运）的暂态响应
- 各支路N-1工况的暂态响应对比
- 严重程度分级（观察/警告/严重）
- 恢复缺口指标（量化暂态电压恢复能力）
- JSON/CSV/Markdown格式的详细报告

### 计算结果的用途和价值
EMT N-1筛查结果可直接用于：
- **保护配置优化**: 针对严重场景调整保护定值和动作逻辑
- **运行控制策略**: 制定N-1故障后的紧急控制措施
- **网架加强规划**: 识别需要加强的薄弱环节
- **事故预案制定**: 预先制定严重故障的处置方案

## 功能特性

- **自动支路发现**: 自动识别系统中的线路和变压器
- **基线对比分析**: 与无故障基线工况对比，量化N-1影响
- **暂态响应评估**: 监测故障前后母线电压的暂态变化
- **严重程度分级**: 自动分级（观察/警告/严重）
- **恢复缺口指标**: 量化故障后电压恢复能力
- **多格式输出**: 支持JSON、CSV、Markdown报告

## 快速开始

### CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init emt_n1_screening --output emt_n1.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config emt_n1.yaml
```

### Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("emt_n1_screening")

# 配置
config = {
    "skill": "emt_n1_screening",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE3",
        "source": "cloud"
    },
    "scan": {
        "branches": [],              # 空列表自动发现
        "include_transformers": True,  # 包含变压器
        "limit": 10                  # 限制检查支路数
    },
    "fault": {
        "fs": 2.5,      # 故障开始时间(s)
        "fe": 2.7,      # 故障结束时间(s)
        "chg": 0.01     # 故障电阻(标幺值)
    },
    "assessment": {
        "monitored_buses": ["Bus7"],  # 监测母线
        "power_trace": "#P1:0",       # 功率跟踪通道
        "time_windows": {
            "prefault": [2.42, 2.44],      # 故障前窗口
            "fault": [2.56, 2.58],          # 故障中窗口
            "postfault": [2.92, 2.94],      # 故障后窗口
            "late_recovery": [2.96, 2.98]   # 恢复后期窗口
        },
        "severity_thresholds": {
            "warning": 10.0,   # 警告阈值
            "critical": 15.0   # 严重阈值
        }
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "emt_n1",
        "generate_report": True
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
skill: emt_n1_screening
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

scan:
  branches: []              # 筛查支路，空表示自动发现
  include_transformers: true
  limit: 10                 # 限制检查支路数

fault:
  fs: 2.5                   # 故障开始时间(s)
  fe: 2.7                   # 故障结束时间(s)
  chg: 0.01                 # 故障电阻(标幺值)

assessment:
  monitored_buses:
    - Bus7                   # 监测母线
  power_trace: "#P1:0"
  time_windows:
    prefault: [2.42, 2.44]
    fault: [2.56, 2.58]
    postfault: [2.92, 2.94]
    late_recovery: [2.96, 2.98]
  severity_thresholds:
    warning: 10.0
    critical: 15.0

output:
  format: json
  path: ./results/
  prefix: emt_n1
  generate_report: true
```

## 配置Schema

### 完整配置结构

```yaml
skill: emt_n1_screening              # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token（不推荐）
  token_file: string                  # token文件路径（默认: .cloudpss_token）

model:                                # 模型配置（必需）
  rid: string                         # 模型RID或本地路径（必需）
  source: enum                        # cloud | local（默认: cloud）

scan:                                 # 筛查配置
  branches:                           # 要检查的支路列表
    - string                          # 支路ID
  include_transformers: boolean       # 是否包含变压器（默认: true）
  limit: integer                      # 最大检查支路数

fault:                                # 故障配置
  fs: number                          # 故障开始时间(s)（默认: 2.5）
  fe: number                          # 故障结束时间(s)（默认: 2.7）
  chg: number                         # 故障电阻(标幺值)（默认: 0.01）

assessment:                           # 评估配置
  monitored_buses:                    # 监测母线列表
    - string                          # 母线名称
  power_trace: string                 # 功率跟踪通道（默认: #P1:0）
  time_windows:                       # 时间窗口配置
    prefault: [number, number]        # 故障前窗口[s]（默认: [2.42, 2.44]）
    fault: [number, number]           # 故障中窗口[s]（默认: [2.56, 2.58]）
    postfault: [number, number]       # 故障后窗口[s]（默认: [2.92, 2.94]）
    late_recovery: [number, number]   # 恢复后期窗口[s]（默认: [2.96, 2.98]）
  severity_thresholds:                # 严重程度阈值
    warning: number                   # 警告阈值（默认: 10.0）
    critical: number                  # 严重阈值（默认: 15.0）

output:                               # 输出配置
  format: enum                        # json | csv（默认: json）
  path: string                        # 输出目录（默认: ./results/）
  prefix: string                      # 文件名前缀（默认: emt_n1_screening）
  generate_report: boolean            # 是否生成Markdown报告（默认: true）
```

### 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"emt_n1_screening" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud / local |
| `scan.branches` | array | 否 | [] | 指定支路列表，空表示自动发现 |
| `scan.include_transformers` | boolean | 否 | true | 是否包含变压器 |
| `scan.limit` | integer | 否 | - | 最大检查支路数 |
| `fault.fs` | number | 否 | 2.5 | 故障开始时间(s) |
| `fault.fe` | number | 否 | 2.7 | 故障结束时间(s) |
| `fault.chg` | number | 否 | 0.01 | 故障电阻(标幺值) |
| `assessment.monitored_buses` | array | 否 | ["Bus7"] | 监测母线列表 |
| `assessment.power_trace` | string | 否 | "#P1:0" | 功率跟踪通道 |
| `assessment.severity_thresholds.warning` | number | 否 | 10.0 | 警告阈值 |
| `assessment.severity_thresholds.critical` | number | 否 | 15.0 | 严重阈值 |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | emt_n1_screening | 文件名前缀 |
| `output.generate_report` | boolean | 否 | true | 是否生成报告 |

## Agent使用指南

### 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("emt_n1_screening")

# 最小化配置（使用默认值）
config = {
    "model": {"rid": "model/holdme/IEEE3"}
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status.value == "SUCCESS":
        print(f"筛查完成: {result.data}")
    else:
        print(f"筛查失败: {result.error}")
```

### 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data

    # 获取严重程度分布
    severity_dist = data.get("severity_distribution", {})
    print(f"严重: {severity_dist.get('critical', 0)}")
    print(f"警告: {severity_dist.get('warning', 0)}")
    print(f"观察: {severity_dist.get('observe', 0)}")

    # 获取基线结果
    baseline = data.get("baseline", {})
    print(f"基线恢复缺口: {baseline.get('worst_postfault_gap', 0):.2f}")

    # 遍历各支路结果
    for r in data.get("results", []):
        print(f"{r['rank']}. {r['branch_name']}: {r['severity']}")
        print(f"   恢复缺口: {r['worst_postfault_gap']:.2f}")

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
    elif "EMT仿真失败" in error_msg:
        print("错误: EMT仿真失败，请检查模型是否支持EMT仿真")
    elif "没有要检查的支路" in error_msg:
        print("错误: 系统中未找到可检查的支路")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### JSON输出格式

```json
{
  "model_name": "IEEE3",
  "model_rid": "model/holdme/IEEE3",
  "timestamp": "2024-03-24T14:32:01",
  "baseline": {
    "branch_id": "baseline",
    "branch_name": "baseline",
    "branch_kind": "reference",
    "severity": "observe",
    "worst_postfault_gap": 2.34,
    "worst_late_gap": 2.34
  },
  "total_branches": 5,
  "severity_distribution": {
    "critical": 1,
    "warning": 2,
    "observe": 2
  },
  "results": [
    {
      "rank": 1,
      "branch_id": "Branch_1",
      "branch_name": "Line_1",
      "branch_kind": "line",
      "severity": "critical",
      "worst_postfault_gap": 18.56,
      "worst_late_gap": 15.23,
      "delta_vs_baseline": 16.22
    },
    {
      "rank": 2,
      "branch_name": "Line_2",
      "severity": "warning",
      "worst_postfault_gap": 12.45
    }
  ]
}
```

### SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "emt_n1_screening" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典 |
| `artifacts` | list | 输出文件列表（JSON/CSV/Markdown） |
| `logs` | list | 执行日志列表 |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标（total_branches, completed, critical, warning） |

## 设计原理

### 筛查流程

```
1. 加载认证和模型
2. 发现候选支路（线路+变压器）
3. 执行基线仿真（无支路停运）
4. 对于每条支路:
   a. 复制基线模型
   b. 停运该支路
   c. 配置故障参数
   d. 运行EMT仿真
   e. 提取监测母线波形
   f. 计算恢复缺口
   g. 严重程度分级
5. 排序和汇总结果
6. 生成报告
```

### 恢复缺口指标

恢复缺口（Postfault Gap）定义为故障前电压有效值与故障后电压有效值的差值，用于量化暂态电压恢复能力：

```
Gap = V_prefault - V_postfault
```

- Gap越大，表示故障后电压恢复越差
- 用于严重程度分级和排序

### 严重程度分级

| 级别 | 条件 | 说明 |
|------|------|------|
| 严重(Critical) | Gap >= critical_threshold | 暂态电压恢复严重不足 |
| 警告(Warning) | Gap >= warning_threshold | 暂态电压恢复较差 |
| 观察(Observe) | Gap < warning_threshold | 暂态电压恢复正常 |

## 与其他技能的关联

```
emt_simulation
    ↓ (EMT仿真基础)
emt_n1_screening
    ↓ (N-1筛查结果)
contingency_analysis, emt_fault_study
    ↓ (综合分析)
reactive_compensation_design
```

### 依赖关系

- **必需依赖**: CloudPSS SDK (`cloudpss`)
- **输入依赖**: 需要`emt_simulation`技能进行EMT仿真
- **输出被依赖**:
  - `contingency_analysis`: 综合预想事故分析
  - `emt_fault_study`: 故障研究

## 性能特点

- **执行时间**: 每条支路约3-5分钟（EMT仿真耗时）
- **总时间**: 与支路数量成正比，IEEE3系统约15-30分钟
- **内存占用**: 中等，需存储多个模型副本
- **适用规模**: 建议单次不超过20条支路
- **并行能力**: 目前串行执行

## 常见问题

### 问题1: EMT仿真超时

**原因**:
- 仿真步长过小
- 仿真时长过长
- 系统暂态过程复杂

**解决**: 调整故障参数或限制仿真时长
```yaml
fault:
  fs: 2.0      # 提前开始故障
  fe: 2.1      # 缩短故障持续时间
```

### 问题2: 监测母线数据提取失败

**原因**:
- 母线名称拼写错误
- 该母线没有电压测量通道

**解决**: 确认母线名称存在于EMT输出中
```python
# 先检查EMT结果中的可用通道
from cloudpss import Model, setToken
setToken(token)
model = Model.fetch("model/holdme/IEEE3")
job = model.runEMT()
# 等待完成后
result = job.result
for i in range(len(result.getPlots())):
    channels = result.getPlotChannelNames(i)
    print(f"Plot {i}: {channels}")
```

### 问题3: 基线工况恢复缺口异常

**原因**:
- 时间窗口配置不当
- 故障参数与系统不匹配

**解决**: 调整时间窗口配置
```yaml
assessment:
  time_windows:
    prefault: [2.0, 2.2]      # 确保故障前稳定
    fault: [2.5, 2.7]
    postfault: [3.0, 3.2]     # 确保有足够恢复时间
```

### 问题4: 严重程度分级不合理

**原因**:
- 阈值设置与系统特性不匹配
- 系统本身暂态特性差异大

**解决**: 根据基线结果调整阈值
```python
# 先运行基线，观察基线恢复缺口
result = skill.run(config)
baseline_gap = result.data["baseline"]["worst_postfault_gap"]
print(f"基线恢复缺口: {baseline_gap}")
# 然后根据基线值设置阈值
```

## 完整示例

### 场景描述

某电力公司需要对IEEE3系统进行EMT N-1安全筛查，评估各支路停运并伴随三相短路故障时的暂态电压恢复能力，识别暂态稳定性薄弱的支路。

### 配置文件

```yaml
skill: emt_n1_screening
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

scan:
  branches: []              # 自动发现所有支路
  include_transformers: true
  limit: 5                  # 限制检查前5条支路

fault:
  fs: 2.5                   # 故障开始时间(s)
  fe: 2.7                   # 故障持续时间0.2s
  chg: 0.01                 # 故障电阻

assessment:
  monitored_buses:
    - Bus7                   # 监测Bus7电压
  power_trace: "#P1:0"
  time_windows:
    prefault: [2.42, 2.44]
    fault: [2.56, 2.58]
    postfault: [2.92, 2.94]
    late_recovery: [2.96, 2.98]
  severity_thresholds:
    warning: 10.0
    critical: 15.0

output:
  format: json
  path: ./results/
  prefix: emt_n1_ieee3
  generate_report: true
```

### 执行命令

```bash
python -m cloudpss_skills run --config emt_n1_config.yaml
```

### 预期输出

```
[INFO] 加载认证信息...
[INFO] 认证成功
[INFO] 获取模型: IEEE3
[INFO] 自动发现候选支路...
[INFO] 发现 8 条候选支路
[INFO] 限制为前 5 条支路
[INFO] 执行基线仿真...
[INFO] 基线完成: worst_post_gap=2.34
[INFO] [1/5] 支路: Line_1...
[INFO]  -> 完成: severity=critical
[INFO] [2/5] 支路: Line_2...
[INFO]  -> 完成: severity=warning
...
[INFO] 排序和分级...
[INFO] JSON结果: ./results/emt_n1_ieee3_20240324_143245.json
[INFO] CSV结果: ./results/emt_n1_ieee3_20240324_143245.csv
[INFO] 研究报告: ./results/emt_n1_ieee3_report_20240324_143245.md
```

### 结果文件

```json
{
  "model_name": "IEEE3",
  "model_rid": "model/holdme/IEEE3",
  "timestamp": "2024-03-24T14:32:45",
  "baseline": {
    "branch_id": "baseline",
    "branch_name": "baseline",
    "severity": "observe",
    "worst_postfault_gap": 2.34
  },
  "total_branches": 5,
  "severity_distribution": {
    "critical": 1,
    "warning": 2,
    "observe": 2
  },
  "results": [
    {
      "rank": 1,
      "branch_id": "Branch_1",
      "branch_name": "Line_1",
      "branch_kind": "line",
      "severity": "critical",
      "worst_postfault_gap": 18.56,
      "worst_late_gap": 15.23,
      "delta_vs_baseline": 16.22
    },
    {
      "rank": 2,
      "branch_id": "Branch_2",
      "branch_name": "Line_2",
      "branch_kind": "line",
      "severity": "warning",
      "worst_postfault_gap": 12.45,
      "worst_late_gap": 10.12,
      "delta_vs_baseline": 10.11
    }
  ]
}
```

### Markdown报告

生成的报告包含：
- 执行摘要（严重/警告/观察数量）
- 基线工况对比
- N-1筛查结果排名表
- 最严重工况详细分析

### 后续应用

基于EMT N-1筛查结果，可以：
1. **保护优化**: 针对严重工况调整保护定值
2. **运行控制**: 制定严重故障的紧急控制策略
3. **网架加强**: 对薄弱环节进行加强改造
4. **事故预案**: 预先制定严重场景的处置方案

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
