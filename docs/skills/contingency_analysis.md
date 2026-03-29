# 预想事故分析技能 (Contingency Analysis)

## 设计背景

### 研究对象
预想事故分析（Contingency Analysis）是电力系统安全评估的核心方法，用于评估系统在N-K故障（失去K个元件）条件下的安全性。与简单的N-1校核不同，预想事故分析支持多种故障组合（N-1、N-2、N-K），能够全面评估系统在多重故障情况下的安全裕度。

### 实际需求
在电力系统规划和运行中，需要：
1. **多重故障评估**: 评估系统在失去多个元件时的安全性
2. **薄弱环节识别**: 发现对系统安全影响最大的关键元件
3. **风险排序**: 按严重程度对故障场景进行排序
4. **安全裕度量化**: 量化系统在各种故障下的安全裕度
5. **网架评估**: 评估网架结构对多重故障的抵御能力

### 期望的输入和输出

**输入**:
- 电力系统模型（IEEE39等标准系统或实际系统）
- 故障级别（N-1、N-2、N-K）
- 故障元件类型（线路、发电机、变压器、负荷）
- 安全约束阈值（电压限值、热稳定限值）
- 严重度阈值
- 最大故障组合数

**输出**:
- 基态潮流结果
- 各故障场景的评估结果（通过/越限/失败）
- 严重程度排序
- 系统薄弱环节识别
- JSON/CSV/Markdown格式的详细报告

### 计算结果的用途和价值
预想事故分析结果可直接用于：
- **网架规划**: 识别网架薄弱环节，指导网架加强
- **运行方式优化**: 避免在薄弱环节叠加多重故障
- **保护配置**: 针对严重故障场景优化保护定值
- **应急预案**: 制定多重故障的应急处置方案

## 功能特性

- **多级故障支持**: 支持N-1、N-2、N-K故障级别
- **多类型元件**: 支持线路、发电机、变压器、负荷故障
- **自动组合生成**: 自动生成分布式故障组合
- **严重度评估**: 量化故障严重度（0-1）
- **薄弱环节识别**: 自动识别系统薄弱环节
- **风险排序**: 按严重度排序故障场景
- **详细报告**: 生成Markdown格式的分析报告

## 快速开始

### CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init contingency_analysis --output contingency.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config contingency.yaml
```

### Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("contingency_analysis")

# 配置
config = {
    "skill": "contingency_analysis",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "contingency": {
        "level": "N-1",           # 故障级别: N-1 / N-2 / N-K
        "k": 1,                   # N-K中的K值
        "components": [],         # 指定元件列表，空表示全部
        "component_types": ["branch"],  # 元件类型
        "max_combinations": 100   # 最大故障组合数
    },
    "analysis": {
        "check_voltage": True,    # 检查电压约束
        "check_thermal": True,    # 检查热稳定约束
        "check_transient": False, # 检查暂态约束
        "voltage_limit": {
            "min": 0.95,          # 电压下限
            "max": 1.05           # 电压上限
        },
        "thermal_limit": 1.0,     # 热稳定限值
        "severity_threshold": 0.8 # 严重度阈值
    },
    "ranking": {
        "method": "severity",     # 排序方法
        "top_n": 10              # 显示前N个
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "contingency",
        "generate_report": True,
        "export_all_cases": False
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
skill: contingency_analysis
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

contingency:
  level: N-1                  # N-1 / N-2 / N-K
  k: 1
  components: []              # 指定元件，空表示全部
  component_types:
    - branch                  # 线路
    - generator               # 发电机
    - transformer             # 变压器
  max_combinations: 100

analysis:
  check_voltage: true
  check_thermal: true
  voltage_limit:
    min: 0.95
    max: 1.05
  thermal_limit: 1.0
  severity_threshold: 0.8

ranking:
  method: severity            # severity / overload / violation_count
  top_n: 10

output:
  format: json
  path: ./results/
  prefix: contingency
  generate_report: true
  export_all_cases: false
```

## 配置Schema

### 完整配置结构

```yaml
skill: contingency_analysis           # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token（不推荐）
  token_file: string                  # token文件路径（默认: .cloudpss_token）

model:                                # 模型配置（必需）
  rid: string                         # 模型RID或本地路径（必需）
  source: enum                        # cloud | local（默认: cloud）

contingency:                          # 故障配置
  level: enum                         # N-1 | N-2 | N-K（默认: N-1）
  k: integer                          # N-K中的K值（默认: 1）
  components:                         # 指定故障元件列表
    - string                          # 元件ID
  component_types:                    # 故障元件类型
    - enum                            # branch | generator | load | transformer
  max_combinations: integer           # 最大故障组合数（默认: 100）

analysis:                             # 分析配置
  check_voltage: boolean              # 检查电压约束（默认: true）
  check_thermal: boolean              # 检查热稳定约束（默认: true）
  check_transient: boolean            # 检查暂态约束（默认: false）
  voltage_limit:                      # 电压限值
    min: number                       # 电压下限（默认: 0.95）
    max: number                       # 电压上限（默认: 1.05）
  thermal_limit: number               # 热稳定限值（默认: 1.0）
  severity_threshold: number          # 严重度阈值（默认: 0.8）

ranking:                              # 排序配置
  method: enum                        # severity | overload | violation_count（默认: severity）
  top_n: integer                      # 显示前N个（默认: 10）

output:                               # 输出配置
  format: enum                        # json | csv（默认: json）
  path: string                        # 输出目录（默认: ./results/）
  prefix: string                      # 文件名前缀（默认: contingency）
  generate_report: boolean            # 是否生成Markdown报告（默认: true）
  export_all_cases: boolean           # 是否导出所有案例（默认: false）
```

### 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"contingency_analysis" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud / local |
| `contingency.level` | enum | 否 | N-1 | 故障级别：N-1 / N-2 / N-K |
| `contingency.k` | integer | 否 | 1 | N-K中的K值 |
| `contingency.components` | array | 否 | [] | 指定故障元件列表 |
| `contingency.component_types` | array | 否 | ["branch"] | 故障元件类型 |
| `contingency.max_combinations` | integer | 否 | 100 | 最大故障组合数 |
| `analysis.check_voltage` | boolean | 否 | true | 检查电压约束 |
| `analysis.check_thermal` | boolean | 否 | true | 检查热稳定约束 |
| `analysis.voltage_limit.min` | number | 否 | 0.95 | 电压下限 |
| `analysis.voltage_limit.max` | number | 否 | 1.05 | 电压上限 |
| `analysis.thermal_limit` | number | 否 | 1.0 | 热稳定限值 |
| `analysis.severity_threshold` | number | 否 | 0.8 | 严重度阈值 |
| `ranking.method` | enum | 否 | severity | 排序方法 |
| `ranking.top_n` | integer | 否 | 10 | 显示前N个 |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | contingency | 文件名前缀 |
| `output.generate_report` | boolean | 否 | true | 是否生成报告 |
| `output.export_all_cases` | boolean | 否 | false | 是否导出所有案例 |

## Agent使用指南

### 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("contingency_analysis")

# 最小化配置（使用默认值）
config = {
    "model": {"rid": "model/holdme/IEEE39"}
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status.value == "SUCCESS":
        print(f"分析完成: {result.data}")
    else:
        print(f"分析失败: {result.error}")
```

### 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data

    # 获取摘要信息
    summary = data.get("summary", {})
    print(f"总场景: {summary['total_cases']}")
    print(f"通过: {summary['passed']} ({summary['pass_rate']}%)")
    print(f"失败: {summary['failed']}")
    print(f"严重故障: {summary['severe_cases']}")

    # 获取薄弱环节
    weak_points = data.get("weak_points", [])
    print("\n系统薄弱环节:")
    for wp in weak_points[:5]:
        print(f"  {wp['component']}: {wp['critical_cases']}次关键故障")

    # 获取最严重故障
    top_cases = data.get("top_severe_cases", [])
    print("\n最严重故障场景:")
    for case in top_cases[:5]:
        print(f"  {case['name']}: 严重度={case['severity']:.4f}")

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
    elif "未生成有效的故障场景" in error_msg:
        print("错误: 未找到符合条件的故障元件")
    elif "基态潮流计算失败" in error_msg:
        print("错误: 基态潮流不收敛，请检查模型数据")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### JSON输出格式

```json
{
  "model": "IEEE39",
  "contingency_level": "N-1",
  "summary": {
    "total_cases": 46,
    "passed": 44,
    "failed": 2,
    "errors": 0,
    "pass_rate": 95.65,
    "severe_cases": 3
  },
  "weak_points": [
    {
      "component": "Line_10",
      "critical_cases": 5
    },
    {
      "component": "Transformer_2",
      "critical_cases": 3
    }
  ],
  "top_severe_cases": [
    {
      "name": "Line_10",
      "components": ["Line_10"],
      "status": "VIOLATION",
      "severity": 0.8234,
      "min_voltage": 0.9123,
      "max_voltage": 1.0234,
      "max_loading": 108.5,
      "violations": [
        {
          "type": "VOLTAGE",
          "details": {"bus": "Bus_10", "voltage": 0.9123, "limit": "<0.95"}
        }
      ]
    }
  ],
  "all_results": null
}
```

### SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "contingency_analysis" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典 |
| `artifacts` | list | 输出文件列表（JSON/CSV/Markdown） |
| `logs` | list | 执行日志列表 |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标 |

## 设计原理

### 分析流程

```
1. 加载认证和模型
2. 计算基态潮流
3. 生成故障组合
   - 根据component_types从拓扑获取元件
   - 根据level和k生成组合
   - 应用max_combinations限制
4. 逐一评估故障场景
   a. 重新加载模型
   b. 移除故障元件
   c. 运行潮流计算
   d. 检查电压/热稳定约束
   e. 记录结果和越限信息
5. 计算严重度并排序
6. 识别薄弱环节
7. 生成报告
```

### 严重度计算

严重度计算公式（0-1）：

```
严重度 = max(电压越界严重度, 热稳定越界严重度, 不收敛严重度)

电压越界严重度 = max(
    (V_min_limit - V_min) / V_min_limit,  # 电压过低
    (V_max - V_max_limit) / (1.1 - V_max_limit)  # 电压过高
)

热稳定越界严重度 = (Loading_max - Loading_limit) / Loading_limit

不收敛严重度 = 1.0
超时严重度 = 0.9
```

### 薄弱环节识别

薄弱环节通过统计元件在严重故障（top_n）中出现的次数来识别：

```
薄弱环节 = 按critical_cases排序的元件列表
```

## 与其他技能的关联

```
power_flow
    ↓ (潮流计算)
n1_security
    ↓ (N-1分析)
contingency_analysis
    ↓ (多重故障分析)
maintenance_security, emt_n1_screening
    ↓ (综合分析)
reactive_compensation_design
```

### 依赖关系

- **必需依赖**: CloudPSS SDK (`cloudpss`)
- **输入依赖**: 需要`power_flow`技能进行潮流计算
- **输出被依赖**:
  - `maintenance_security`: 检修方式安全校核
  - `emt_n1_screening`: EMT N-1安全筛查

## 性能特点

- **执行时间**: IEEE39系统N-1分析约10-20分钟（46个场景）
- **时间比例**: 与故障场景数量成正比
- **内存占用**: 较低，每次重新加载模型
- **适用规模**: 建议max_combinations不超过500
- **N-2注意**: N-2故障组合数可能很大，需谨慎设置max_combinations

## 常见问题

### 问题1: 故障场景数量过大

**原因**:
- N-2及以上级别故障组合数呈组合爆炸
- 系统中元件数量多

**解决**: 限制故障组合数或指定特定元件
```yaml
contingency:
  level: N-2
  max_combinations: 50           # 限制最大组合数
  components:                      # 或只检查关键元件
    - "Line_1"
    - "Line_2"
    - "Transformer_1"
```

### 问题2: 某些元件识别为"other"类型

**原因**:
- 元件定义或命名不规范
- 使用了非标准元件类型

**解决**: 检查元件定义或手动指定元件列表
```yaml
contingency:
  components:
    - "/Line_1"          # 使用完整key
    - "/Transformer_Main"
```

### 问题3: 严重度计算不合理

**原因**:
- 阈值设置与系统特性不匹配
- 系统正常运行电压范围较宽

**解决**: 根据系统特性调整阈值
```yaml
analysis:
  voltage_limit:
    min: 0.90        # 放宽电压下限
    max: 1.10        # 放宽电压上限
  thermal_limit: 1.2  # 放宽热稳定限值
```

### 问题4: 基态潮流不收敛

**原因**:
- 系统数据错误
- 负荷过重
- 缺少无功支撑

**解决**: 检查模型数据，或先使用power_flow技能单独验证
```python
from cloudpss_skills import get_skill

# 先用power_flow验证基态
pf_skill = get_skill("power_flow")
pf_config = {"model": {"rid": "model/holdme/IEEE39"}}
pf_result = pf_skill.run(pf_config)
if pf_result.status.value != "SUCCESS":
    print("基态潮流不收敛，请先检查模型")
```

## 完整示例

### 场景描述

某电力公司需要对IEEE39系统进行N-2预想事故分析，评估系统在失去两条支路时的安全性，识别需要加强的关键设备和运行方式。

### 配置文件

```yaml
skill: contingency_analysis
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

contingency:
  level: N-2                  # N-2故障
  k: 2
  components: []              # 全部支路
  component_types:
    - branch                  # 只检查线路
  max_combinations: 50       # 限制50个组合

analysis:
  check_voltage: true
  check_thermal: true
  voltage_limit:
    min: 0.95
    max: 1.05
  thermal_limit: 1.0
  severity_threshold: 0.8

ranking:
  method: severity
  top_n: 10

output:
  format: json
  path: ./results/
  prefix: contingency_n2
  generate_report: true
  export_all_cases: false
```

### 执行命令

```bash
python -m cloudpss_skills run --config contingency_n2.yaml
```

### 预期输出

```
[INFO] 加载认证...
[INFO] 认证成功
[INFO] 模型: IEEE39
[INFO] 预想事故分析: N-2
[INFO] 故障元件类型: branch
[INFO] 电压限值: 0.950 - 1.050 pu
[INFO] 热稳定限值: 1.000 pu
[INFO] 计算基态潮流...
[INFO] 基态: 39 节点, 46 支路
[INFO] 生成故障组合...
[INFO] 共 50 个故障场景
[INFO] 开始故障评估...
[INFO] [1/50] Line_1 + Line_2...
[INFO] [2/50] Line_1 + Line_3...
...
[INFO] [50/50] Line_45 + Line_46...
[INFO] 计算严重度并排序...
[INFO] 通过: 35/50 (70.0%)
[INFO] 严重故障: 8 个
[INFO] 结果已保存
```

### 结果文件

```json
{
  "model": "IEEE39",
  "contingency_level": "N-2",
  "summary": {
    "total_cases": 50,
    "passed": 35,
    "failed": 15,
    "errors": 0,
    "pass_rate": 70.0,
    "severe_cases": 8
  },
  "weak_points": [
    {
      "component": "Line_10",
      "critical_cases": 6
    },
    {
      "component": "Line_15",
      "critical_cases": 4
    }
  ],
  "top_severe_cases": [
    {
      "name": "Line_10 + Line_15",
      "components": ["Line_10", "Line_15"],
      "status": "VIOLATION",
      "severity": 0.9234,
      "min_voltage": 0.8234,
      "max_loading": 125.6
    }
  ]
}
```

### Markdown报告

生成的报告包含：
- 执行摘要（通过/失败率）
- 安全裕度评估
- 评判标准
- 系统薄弱环节排名
- 最严重故障场景Top 10
- 建议措施

### 后续应用

基于预想事故分析结果，可以：
1. **网架加强**: 针对薄弱环节进行网架改造
2. **运行控制**: 避免关键设备同时检修
3. **保护优化**: 针对严重故障场景优化保护配置
4. **应急演练**: 模拟严重故障场景进行演练

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
