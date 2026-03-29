# 批量潮流计算技能 (Batch Power Flow)

## 设计背景

### 研究对象
批量潮流计算技能用于对多个电力系统模型批量执行稳态潮流分析。在电力系统规划和运行分析中，经常需要对比不同系统配置、不同运行方式或不同时间断面的潮流分布情况。

### 实际需求
在以下场景中需要批量潮流计算能力：
1. **多场景对比分析**：对比不同规划方案的系统潮流特性
2. **年度运行方式分析**：批量计算8760小时的运行方式
3. **多区域协调分析**：对互联系统的多个区域分别计算
4. **模型版本对比**：对比同一系统的不同模型版本
5. **大规模系统评估**：对大量测试系统进行快速筛选

### 期望的输入和输出

**输入**：
- 多个电力系统模型（云端RID或本地YAML文件）
- 每个模型的名称标识
- 统一的潮流算法配置（算法类型、收敛精度、迭代次数）
- 输出格式和路径配置

**输出**：
- 每个模型的潮流计算结果（收敛状态、Job ID）
- 批量计算的汇总统计（成功率、收敛/失败数量）
- JSON或CSV格式的详细结果文件
- Markdown格式的汇总报告

### 计算结果的用途和价值
批量潮流计算结果可用于：
- 快速筛选收敛性良好的系统模型
- 对比分析不同系统的稳态特性
- 生成规划方案的初步评估报告
- 识别需要进一步详细分析的异常系统
- 支持大规模系统的自动化评估流程

## 功能特性

- **多模型批量计算**：支持对多个模型顺序执行潮流计算
- **灵活的模型来源**：支持CloudPSS云端模型和本地YAML文件混合
- **统一算法配置**：为所有模型应用相同的算法参数
- **完善的失败处理**：单个模型失败不影响其他模型计算
- **多格式结果输出**：支持JSON和CSV两种输出格式
- **自动汇总报告**：生成Markdown格式的汇总统计报告
- **详细的日志记录**：记录每个模型的计算过程和状态

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init batch_powerflow --output batch_pf.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config batch_pf.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("batch_powerflow")

# 配置
config = {
    "skill": "batch_powerflow",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "models": [
        {"rid": "model/holdme/IEEE39", "name": "IEEE39", "source": "cloud"},
        {"rid": "model/holdme/IEEE3", "name": "IEEE3", "source": "cloud"},
        {"rid": "./models/custom_system.yaml", "name": "Custom", "source": "local"}
    ],
    "algorithm": {
        "type": "newton_raphson",
        "tolerance": 1e-6,
        "max_iterations": 100
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "batch_pf",
        "timestamp": True,
        "aggregate": True
    }
}

# 验证配置
validation = skill.validate(config)
if not validation.valid:
    print("配置错误:", validation.errors)

# 运行
result = skill.run(config)
print(f"状态: {result.status}")
print(f"成功率: {result.metrics.get('success_rate', 0)*100:.1f}%")
```

### 3.3 YAML配置示例

```yaml
skill: batch_powerflow
auth:
  token_file: .cloudpss_token

models:
  - rid: model/holdme/IEEE39
    name: IEEE39
    source: cloud
  - rid: model/holdme/IEEE3
    name: IEEE3
    source: cloud
  - rid: ./models/my_system.yaml
    name: MySystem
    source: local

algorithm:
  type: newton_raphson
  tolerance: 1e-6
  max_iterations: 100

output:
  format: json
  path: ./results/
  prefix: batch_pf
  timestamp: true
  aggregate: true
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: batch_powerflow               # 必需: 技能名称
auth:                                # 认证配置
  token: string                      # 直接提供token（不推荐）
  token_file: string                 # token文件路径（默认: .cloudpss_token）

models:                              # 模型列表（必需）
  - rid: string                      # 模型RID或本地路径（必需）
    name: string                     # 模型名称（可选）
    source: enum                     # cloud | local（默认: cloud）

algorithm:                           # 算法配置
  type: enum                         # newton_raphson | fast_decoupled（默认: newton_raphson）
  tolerance: number                  # 收敛精度（默认: 1e-6）
  max_iterations: integer            # 最大迭代次数（默认: 100）

output:                              # 输出配置
  format: enum                       # json | csv（默认: json）
  path: string                       # 输出目录（默认: ./results/）
  prefix: string                     # 文件名前缀（默认: batch_powerflow）
  timestamp: boolean                 # 是否添加时间戳（默认: true）
  aggregate: boolean                 # 是否生成汇总报告（默认: true）
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"batch_powerflow" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `models` | array | 是 | - | 要计算的模型列表 |
| `models[].rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `models[].name` | string | 否 | rid值 | 模型显示名称 |
| `models[].source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `algorithm.type` | enum | 否 | newton_raphson | 算法类型 |
| `algorithm.tolerance` | number | 否 | 1e-6 | 收敛精度阈值 |
| `algorithm.max_iterations` | integer | 否 | 100 | 最大迭代次数 |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | batch_powerflow | 文件名前缀 |
| `output.timestamp` | boolean | 否 | true | 文件名是否包含时间戳 |
| `output.aggregate` | boolean | 否 | true | 是否生成Markdown汇总报告 |

## Agent使用指南

### 5.1 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("batch_powerflow")

# 最小化配置（使用默认值）
config = {
    "models": [
        {"rid": "model/holdme/IEEE39", "name": "IEEE39"},
        {"rid": "model/holdme/IEEE3", "name": "IEEE3"}
    ]
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status.value == "SUCCESS":
        print(f"批量计算完成: {result.data['summary']}")
    else:
        print(f"计算失败: {result.error}")
```

### 5.2 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data
    summary = data.get("summary", {})

    # 访问汇总统计
    print(f"总模型数: {summary['total']}")
    print(f"收敛: {summary['converged']}")
    print(f"失败: {summary['failed']}")
    print(f"成功率: {summary['success_rate']*100:.1f}%")

    # 访问详细结果
    for r in data.get("results", []):
        status = "✓" if r.get("converged") else "✗"
        print(f"{r['model_name']}: {status} {r['status']}")

    # 访问输出文件
    for artifact in result.artifacts:
        print(f"输出文件: {artifact.path} ({artifact.type})")

# 查看日志
for log in result.logs:
    print(f"[{log.level}] {log.message}")
```

### 5.3 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    error_msg = result.error

    # 常见错误处理
    if "Token文件不存在" in error_msg:
        print("错误: 请创建.cloudpss_token文件")
    elif "模型不存在" in error_msg:
        print("错误: 请检查模型RID是否正确")
    else:
        print(f"未知错误: {error_msg}")

# 处理部分失败情况（某些模型失败但批量任务完成）
if result.status.value == "SUCCESS":
    summary = result.data.get("summary", {})
    if summary.get("failed", 0) > 0:
        print(f"警告: {summary['failed']} 个模型计算失败")
        for r in result.data.get("results", []):
            if r.get("status") != "converged":
                print(f"  - {r['model_name']}: {r.get('error', 'Unknown error')}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "timestamp": "2024-03-24T14:32:01",
  "summary": {
    "total": 3,
    "converged": 3,
    "failed": 0,
    "success_rate": 1.0
  },
  "results": [
    {
      "model_rid": "model/holdme/IEEE39",
      "model_name": "IEEE39",
      "status": "converged",
      "job_id": "job_abc123",
      "converged": true
    },
    {
      "model_rid": "model/holdme/IEEE3",
      "model_name": "IEEE3",
      "status": "converged",
      "job_id": "job_def456",
      "converged": true
    },
    {
      "model_rid": "./models/my_system.yaml",
      "model_name": "MySystem",
      "status": "converged",
      "job_id": "job_ghi789",
      "converged": true
    }
  ]
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "batch_powerflow" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典，包含summary和results |
| `artifacts` | list | 输出文件列表（Artifact对象） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标（total, converged, failed） |

## 设计原理

### 工作流程

```
1. 配置加载与验证
   └── 验证models列表非空
   └── 验证每个模型的rid存在

2. 认证初始化
   └── 读取token文件或直接获取token
   └── 调用setToken完成认证

3. 批量计算循环
   对于每个模型:
   ├── 获取模型（fetch或load）
   ├── 运行潮流计算（runPowerFlow）
   ├── 轮询等待完成（status检查）
   ├── 记录结果（收敛/失败/错误）
   └── 继续下一个模型（失败不中断）

4. 结果汇总
   └── 统计收敛/失败数量
   └── 计算成功率

5. 文件导出
   └── 生成JSON或CSV结果文件
   └── 生成Markdown汇总报告（如启用）
```

### 失败处理策略

- **单模型失败不中断**：某个模型计算失败时，记录错误并继续处理后续模型
- **超时处理**：每个模型最大等待120秒，超时视为失败
- **异常捕获**：捕获所有异常，避免批量任务完全失败
- **详细日志**：记录每个模型的计算状态和错误信息

## 与其他技能的关联

```
power_flow (基础潮流计算)
    ↓ (扩展为批量)
batch_powerflow
    ↓ (批量结果分析)
n1_security, maintenance_security
    ↓ (进一步筛选)
param_scan, result_compare
```

**依赖关系**：
- **输入依赖**：无（直接使用模型列表）
- **输出被依赖**：
  - `result_compare`: 可对比批量计算的不同结果
  - `visualize`: 可视化批量计算结果

**使用场景组合**：
1. 批量潮流 + 结果对比：评估不同规划方案
2. 批量潮流 + 可视化：生成对比图表
3. 参数扫描 + 批量潮流：评估参数变化对系统收敛性的影响

## 性能特点

- **执行时间**：与模型数量和单模型计算时间成正比
  - IEEE39系统：约5-15秒/模型
  - IEEE3系统：约3-10秒/模型
- **顺序执行**：当前版本采用顺序执行，确保稳定性
- **内存占用**：同时只加载一个模型，内存占用稳定
- **失败隔离**：单模型失败不影响整体任务
- **适用规模**：建议单次批量计算控制在50个模型以内

## 常见问题

### 问题1: 部分模型计算失败

**原因**：
- 模型数据错误或不完整
- 系统潮流无解（负荷过重）
- 网络连接问题
- 模型访问权限不足

**解决**：
```python
# 检查失败详情
result = skill.run(config)
for r in result.data.get("results", []):
    if r.get("status") != "converged":
        print(f"{r['model_name']}: {r.get('error', 'Unknown')}")

# 重新运行失败的模型
failed_models = [
    r for r in result.data.get("results", [])
    if r.get("status") != "converged"
]
# 使用调整后的配置重新计算
```

### 问题2: 本地模型加载失败

**原因**：
- 文件路径错误
- YAML格式不正确
- 缺少必要的模型组件

**解决**：
```yaml
# 确认路径正确
models:
  - rid: ./models/my_system.yaml    # 相对路径
    source: local
  - rid: /absolute/path/model.yaml  # 绝对路径
    source: local
```

### 问题3: 汇总报告显示不正确

**原因**：
- aggregate设置为false
- 输出路径无写入权限

**解决**：
```yaml
output:
  aggregate: true      # 确保启用汇总报告
  path: ./results/     # 确保目录存在且有权限
```

### 问题4: 大批量任务执行时间过长

**原因**：
- 模型数量过多
- 单模型计算时间长
- 网络延迟

**解决**：
```python
# 分批执行
all_models = [...]  # 100+ 模型
batch_size = 20

for i in range(0, len(all_models), batch_size):
    batch = all_models[i:i+batch_size]
    config = {
        "models": batch,
        "output": {"prefix": f"batch_{i//batch_size}"}
    }
    result = skill.run(config)
    print(f"批次 {i//batch_size + 1} 完成")
```

## 完整示例

### 场景描述
某电力规划设计院需要评估10个不同规划方案的IEEE39系统变体，筛选出收敛性良好的方案进行进一步分析。

### 配置文件

```yaml
skill: batch_powerflow
auth:
  token_file: .cloudpss_token

models:
  - rid: model/holdme/IEEE39
    name: IEEE39_Base
    source: cloud
  - rid: model/holdme/IEEE39_Variant1
    name: IEEE39_V1
    source: cloud
  - rid: model/holdme/IEEE39_Variant2
    name: IEEE39_V2
    source: cloud
  - rid: ./scenarios/scenario_A.yaml
    name: Scenario_A
    source: local
  - rid: ./scenarios/scenario_B.yaml
    name: Scenario_B
    source: local

algorithm:
  type: newton_raphson
  tolerance: 1e-6
  max_iterations: 100

output:
  format: json
  path: ./batch_results/
  prefix: planning_evaluation
  timestamp: true
  aggregate: true
```

### 执行命令

```bash
# 创建输出目录
mkdir -p ./batch_results

# 执行批量潮流计算
python -m cloudpss_skills run --config batch_planning.yaml
```

### 预期输出

```
[INFO] 加载认证信息...
[INFO] 认证成功
[INFO] 开始批量潮流计算，共 5 个模型
[INFO] ==================================================
[INFO] [1/5] IEEE39_Base
[INFO]   -> 模型: IEEE39
[INFO]   -> Job ID: job_xxx
[INFO]   -> 潮流收敛 ✓ (8s)
[INFO] [2/5] IEEE39_V1
[INFO]   -> 模型: IEEE39_Variant1
[INFO]   -> Job ID: job_yyy
[INFO]   -> 潮流收敛 ✓ (7s)
[INFO] [3/5] IEEE39_V2
[INFO]   -> 模型: IEEE39_Variant2
[INFO]   -> Job ID: job_zzz
[INFO]   -> 潮流收敛 ✓ (9s)
[INFO] [4/5] Scenario_A
[INFO]   -> 模型: Scenario_A
[INFO]   -> Job ID: job_aaa
[INFO]   -> 潮流收敛 ✓ (6s)
[INFO] [5/5] Scenario_B
[INFO]   -> 模型: Scenario_B
[INFO]   -> Job ID: job_bbb
[INFO]   -> 潮流不收敛 ✗ (120s, status=2)
[INFO] ==================================================
[INFO] 批量计算完成:
[INFO]   收敛: 4
[INFO]   不收敛/失败: 1
[INFO]   成功率: 80.0%
[INFO] 结果已保存: ./batch_results/planning_evaluation_20240324_143245.json
[INFO] 汇总报告已保存: ./batch_results/planning_evaluation_summary_20240324_143245.md
```

### 结果文件

**JSON结果文件** (`planning_evaluation_20240324_143245.json`):
```json
{
  "timestamp": "2024-03-24T14:32:45",
  "summary": {
    "total": 5,
    "converged": 4,
    "failed": 1,
    "success_rate": 0.8
  },
  "results": [
    {
      "model_rid": "model/holdme/IEEE39",
      "model_name": "IEEE39_Base",
      "status": "converged",
      "job_id": "job_xxx",
      "converged": true
    },
    {
      "model_rid": "./scenarios/scenario_B.yaml",
      "model_name": "Scenario_B",
      "status": "diverged",
      "job_id": "job_bbb",
      "converged": false
    }
  ]
}
```

**Markdown汇总报告** (`planning_evaluation_summary_20240324_143245.md`):
```markdown
# 批量潮流计算报告

生成时间: 2024-03-24T14:32:45

## 汇总

- 总模型数: 5
- 收敛: 4
- 失败: 1
- 成功率: 80.0%

## 详细结果

| 模型 | 名称 | 状态 | Job ID |
|------|------|------|--------|
| model/holdme/IEEE39 | IEEE39_Base | ✓ converged | job_xxx |
| model/holdme/IEEE39_Variant1 | IEEE39_V1 | ✓ converged | job_yyy |
| model/holdme/IEEE39_Variant2 | IEEE39_V2 | ✓ converged | job_zzz |
| ./scenarios/scenario_A.yaml | Scenario_A | ✓ converged | job_aaa |
| ./scenarios/scenario_B.yaml | Scenario_B | ✗ diverged | job_bbb |
```

### 后续应用

基于批量潮流计算结果，可以：
1. 对收敛的方案使用 `n1_security` 进行N-1安全分析
2. 使用 `result_compare` 对比不同方案的潮流分布差异
3. 使用 `visualize` 生成各方案的关键指标对比图
4. 对不收敛的方案使用 `param_scan` 调整参数后重新计算

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
