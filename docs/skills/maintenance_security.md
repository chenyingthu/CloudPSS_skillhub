# 检修方式安全校核技能 (Maintenance Security)

## 设计背景

### 研究对象
检修方式安全校核是电力系统运行安全分析的重要方法，用于评估系统在计划检修停运条件下的安全性。当系统中某些设备进行计划检修停运时，系统的安全裕度会降低，需要进行检修方式下的N-1复核，确保检修期间系统仍能满足安全要求。

### 实际需求
在电力系统运行中，需要：
1. **检修计划评估**: 评估计划检修停运对系统安全的影响
2. **检修方式N-1复核**: 检修停运后，检查残余系统是否满足N-1准则
3. **安全裕度量化**: 量化检修方式下的安全裕度
4. **风险预警**: 识别检修期间的高风险工况
5. **检修安排优化**: 优化检修时间和范围，降低安全风险

### 期望的输入和输出

**输入**:
- 电力系统模型（IEEE39等标准系统或实际系统）
- 计划停运的支路ID
- 检修说明（可选）
- 残余N-1复核配置（支路列表、是否包含变压器）
- 安全约束阈值

**输出**:
- 基态潮流结果（检修前）
- 检修方式潮流结果
- 检修方式严重度评估
- 残余N-1复核结果
- JSON/CSV/Markdown格式的详细报告

### 计算结果的用途和价值
检修方式安全校核结果可直接用于：
- **检修计划审批**: 评估检修计划的安全性，决定是否批准
- **检修期间监控**: 对高风险检修方式加强监控
- **应急措施制定**: 针对高风险工况制定应急措施
- **检修方案优化**: 调整检修顺序或范围，降低风险

## 功能特性

- **检修场景模拟**: 模拟计划检修停运
- **检修方式评估**: 评估检修方式下的系统安全性
- **残余N-1复核**: 检修方式下的N-1安全校核
- **严重度分级**: 按电压和负载率分级（正常/警告/严重）
- **自动支路发现**: 自动发现残余系统中的可校核支路
- **多格式输出**: 支持JSON、CSV、Markdown报告

## 快速开始

### CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init maintenance_security --output maintenance.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config maintenance.yaml
```

### Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("maintenance_security")

# 配置
config = {
    "skill": "maintenance_security",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "maintenance": {
        "branch_id": "Line_1",    # 计划停运的支路ID
        "description": "Line_1计划检修停运"  # 检修说明
    },
    "residual_n1": {
        "branches": [],           # 残余N-1复核支路，空表示自动发现
        "include_transformers": True,  # 包含变压器
        "limit": 20               # 最大复核支路数
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "maintenance",
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
skill: maintenance_security
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

maintenance:
  branch_id: Line_1           # 计划停运的支路ID
  description: Line_1计划检修停运

residual_n1:
  branches: []                # 残余N-1复核支路，空表示自动发现
  include_transformers: true  # 包含变压器
  limit: 20                   # 最大复核支路数

output:
  format: json
  path: ./results/
  prefix: maintenance
  generate_report: true
```

## 配置Schema

### 完整配置结构

```yaml
skill: maintenance_security           # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token（不推荐）
  token_file: string                  # token文件路径（默认: .cloudpss_token）

model:                                # 模型配置（必需）
  rid: string                         # 模型RID或本地路径（必需）
  source: enum                        # cloud | local（默认: cloud）

maintenance:                          # 检修配置（必需）
  branch_id: string                   # 计划停运的支路ID（必需）
  description: string                 # 检修说明

residual_n1:                          # 残余N-1复核配置
  branches:                           # 复核支路列表
    - string                          # 支路ID
  include_transformers: boolean       # 是否包含变压器（默认: true）
  limit: integer                      # 最大复核支路数

output:                               # 输出配置
  format: enum                        # json | csv（默认: json）
  path: string                        # 输出目录（默认: ./results/）
  prefix: string                      # 文件名前缀（默认: maintenance_security）
  generate_report: boolean            # 是否生成Markdown报告（默认: true）
```

### 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"maintenance_security" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud / local |
| `maintenance.branch_id` | string | 是 | - | 计划停运的支路ID |
| `maintenance.description` | string | 否 | "计划检修停运" | 检修说明 |
| `residual_n1.branches` | array | 否 | [] | 残余N-1复核支路列表 |
| `residual_n1.include_transformers` | boolean | 否 | true | 是否包含变压器 |
| `residual_n1.limit` | integer | 否 | - | 最大复核支路数 |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | maintenance_security | 文件名前缀 |
| `output.generate_report` | boolean | 否 | true | 是否生成报告 |

## Agent使用指南

### 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("maintenance_security")

# 配置（必须指定branch_id）
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "maintenance": {
        "branch_id": "Line_1",
        "description": "Line_1检修"
    }
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

    # 获取检修方式评估
    maintenance = data.get("maintenance", {})
    print(f"检修支路: {maintenance['branch_id']}")
    print(f"严重度: {maintenance['severity']}")
    print(f"最低电压: {maintenance['min_vm']:.4f}")
    print(f"最大负载率: {maintenance['max_branch_loading']:.2f}")

    # 获取残余N-1复核结果
    print(f"\n残余N-1复核: {data['residual_n1_count']}条支路")
    print(f"严重: {data['critical_count']}")
    print(f"警告: {data['warning_count']}")

    # 遍历N-1结果
    for r in data.get("results", []):
        print(f"  {r['branch_id']}: {r['severity']} "
              f"(min_vm={r['min_vm']:.4f}, max_loading={r['max_loading']:.2f})")

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
    if "必须指定 maintenance.branch_id" in error_msg:
        print("错误: 请在配置中指定maintenance.branch_id")
    elif "Token文件不存在" in error_msg:
        print("错误: 请创建.cloudpss_token文件")
    elif "模型不存在" in error_msg:
        print("错误: 请检查模型RID是否正确")
    elif "支路不存在" in error_msg:
        print("错误: 指定的检修支路不存在")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### JSON输出格式

```json
{
  "model": "IEEE39",
  "maintenance": {
    "branch_id": "Line_1",
    "description": "Line_1计划检修停运",
    "min_vm": 0.9234,
    "max_branch_loading": 1.15,
    "severity": "warning"
  },
  "residual_n1_count": 20,
  "critical_count": 2,
  "warning_count": 5,
  "results": [
    {
      "branch_id": "Line_2",
      "severity": "normal",
      "min_vm": 0.9534,
      "max_loading": 0.95
    },
    {
      "branch_id": "Line_3",
      "severity": "warning",
      "min_vm": 0.8934,
      "max_loading": 1.08
    },
    {
      "branch_id": "Line_10",
      "severity": "critical",
      "min_vm": 0.8234,
      "max_loading": 1.25
    }
  ]
}
```

### SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "maintenance_security" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典 |
| `artifacts` | list | 输出文件列表（JSON/CSV/Markdown） |
| `logs` | list | 执行日志列表 |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标 |

## 设计原理

### 严重度分级标准

| 级别 | 条件 | 说明 |
|------|------|------|
| 严重(Critical) | min_vm < 0.85 或 max_loading > 1.2 | 检修方式下安全裕度严重不足 |
| 警告(Warning) | min_vm < 0.9 或 max_loading > 1.0 | 检修方式下安全裕度较低 |
| 正常(Normal) | min_vm >= 0.9 且 max_loading <= 1.0 | 检修方式下安全裕度充足 |

### 分析流程

```
1. 加载认证和模型
2. 计算基线潮流（检修前）
3. 执行计划停运
   a. 复制基线模型
   b. 禁用检修支路
   c. 运行检修方式潮流
   d. 评估检修方式严重度
4. 残余N-1复核
   a. 自动发现残余系统支路
   b. 对于每条残余支路:
      - 复制检修方式模型
      - 停用该支路
      - 运行潮流计算
      - 评估严重度
5. 汇总和生成报告
```

### 支路发现

自动发现残余系统中的可校核支路：
- 传输线路（model/CloudPSS/TransmissionLine）
- 变压器（model/CloudPSS/_newTransformer_3p2w，可选）

## 与其他技能的关联

```
power_flow
    ↓ (潮流计算)
n1_security
    ↓ (N-1分析)
maintenance_security
    ↓ (检修分析结果)
contingency_analysis
    ↓ (综合分析)
reactive_compensation_design
```

### 依赖关系

- **必需依赖**: CloudPSS SDK (`cloudpss`)
- **输入依赖**: 需要`power_flow`技能进行潮流计算
- **输出被依赖**:
  - `contingency_analysis`: 综合预想事故分析
  - 检修计划管理系统

## 性能特点

- **执行时间**: IEEE39系统约5-15分钟
- **时间构成**:
  - 基线潮流: ~30秒
  - 检修方式潮流: ~30秒
  - 残余N-1复核: 与支路数量成正比
- **内存占用**: 中等，需维护多个模型副本
- **适用规模**: 建议残余支路不超过50条

## 常见问题

### 问题1: 检修支路不存在

**原因**:
- 支路ID拼写错误
- 该支路已被删除

**解决**: 使用正确的支路ID
```python
# 先查看系统中的支路
from cloudpss import Model, setToken
setToken(token)
model = Model.fetch("model/holdme/IEEE39")
components = model.getAllComponents()
for comp_id, comp in components.items():
    if "line" in comp.definition.lower() or "transformer" in comp.definition.lower():
        print(f"{comp_id}: {comp.name}")
```

### 问题2: 残余N-1复核支路过多

**原因**:
- 系统规模较大
- 未设置limit参数

**解决**: 设置limit参数限制复核数量
```yaml
residual_n1:
  limit: 20          # 只检查前20条支路
  include_transformers: false  # 不包含变压器
```

### 问题3: 检修方式潮流不收敛

**原因**:
- 检修支路为关键支路，停运后系统无解
- 系统本身较脆弱

**解决**: 评估检修的必要性，或调整检修方案
```python
# 检查结果中的严重度
result = skill.run(config)
data = result.data
maintenance = data.get("maintenance", {})
if maintenance.get("severity") == "critical":
    print("警告: 检修方式下系统严重不安全，建议调整检修计划")
```

### 问题4: 残余N-1复核时间过长

**原因**:
- 残余支路数量多
- 每次复核都需重新加载模型

**解决**: 限制复核范围或并行执行
```yaml
residual_n1:
  branches:            # 只检查关键支路
    - "Line_2"
    - "Line_3"
    - "Transformer_Main"
  limit: 10
```

## 完整示例

### 场景描述

某电力公司计划对IEEE39系统中的Line_1进行检修停运，需要评估检修方式下的系统安全性，并进行残余N-1复核，确保检修期间系统仍能满足安全要求。

### 配置文件

```yaml
skill: maintenance_security
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

maintenance:
  branch_id: Line_1           # 计划停运的支路
  description: Line_1计划检修停运

residual_n1:
  branches: []                # 自动发现所有残余支路
  include_transformers: true
  limit: 20                   # 限制20条支路

output:
  format: json
  path: ./results/
  prefix: maintenance_line1
  generate_report: true
```

### 执行命令

```bash
python -m cloudpss_skills run --config maintenance_config.yaml
```

### 预期输出

```
[INFO] 加载认证...
[INFO] 认证成功
[INFO] 模型: IEEE39
[INFO] 计算基线潮流...
[INFO] 基线: 39母线, 46支路
[INFO] 执行计划停运: Line_1 (Line_1计划检修停运)
[INFO] 检修态: severity=warning
[INFO] 残余N-1复核...
[INFO]  [1/20] Line_2...
[INFO]  [2/20] Line_3...
...
[INFO]  [20/20] Transformer_3...
[INFO] 结果已导出
[INFO] JSON结果: ./results/maintenance_line1_20240324_143245.json
[INFO] CSV结果: ./results/maintenance_line1_20240324_143245.csv
[INFO] 检修安全报告: ./results/maintenance_line1_report_20240324_143245.md
```

### 结果文件

```json
{
  "model": "IEEE39",
  "maintenance": {
    "branch_id": "Line_1",
    "description": "Line_1计划检修停运",
    "min_vm": 0.9234,
    "max_branch_loading": 1.15,
    "severity": "warning"
  },
  "residual_n1_count": 20,
  "critical_count": 2,
  "warning_count": 5,
  "results": [
    {
      "branch_id": "Line_2",
      "severity": "normal",
      "min_vm": 0.9534,
      "max_loading": 0.95
    },
    {
      "branch_id": "Line_10",
      "severity": "critical",
      "min_vm": 0.8234,
      "max_loading": 1.25
    }
  ]
}
```

### CSV结果

```csv
type,branch_id,severity,min_vm,max_loading
maintenance,Line_1,warning,0.9234,1.15
residual_n1,Line_2,normal,0.9534,0.95
residual_n1,Line_3,warning,0.8934,1.08
residual_n1,Line_10,critical,0.8234,1.25
...
```

### Markdown报告

生成的报告包含：
- 检修方式评估
- 残余N-1复核结果统计
- 严重工况列表
- 建议措施

### 后续应用

基于检修方式安全校核结果，可以：
1. **检修计划调整**: 如存在严重工况，调整检修时间或范围
2. **运行监控加强**: 对警告及以上工况加强监控
3. **应急措施准备**: 针对严重工况准备应急措施
4. **网架评估**: 评估检修期间的网架薄弱环节

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
