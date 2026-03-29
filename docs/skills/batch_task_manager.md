# 批量任务管理技能 (Batch Task Manager)

## 设计背景

### 研究对象
批量任务管理技能用于异步批量运行CloudPSS仿真任务，支持并行/串行执行、状态轮询、失败重试和结果回收。这是大规模电力系统分析的基础工具，特别适用于需要运行大量独立仿真任务的场景。

### 实际需求
在电力系统分析中，经常需要批量执行以下任务：
1. **N-1安全分析**：批量计算所有N-1故障场景
2. **VSI弱母线分析**：批量测试所有母线的电压稳定性
3. **参数扫描**：批量运行不同参数组合的仿真
4. **故障扫描**：批量分析不同故障位置和类型
5. **多场景评估**：评估大量规划或运行方案

### 期望的输入和输出

**输入**：
- 模型配置（RID和来源）
- 任务列表（名称、类型、配置、重试次数）
- 执行配置（并行/串行、并发数、超时、轮询间隔）
- 输出配置（格式、路径、前缀）

**输出**：
- 每个任务的执行状态和结果
- 成功/失败统计
- JSON、CSV和Markdown格式的详细报告
- 任务执行时间统计

### 计算结果的用途和价值
批量任务管理结果可用于：
- 大规模N-1安全分析
- 批量参数灵敏度分析
- 多方案对比评估
- 自动化测试和验证
- 系统鲁棒性评估

## 功能特性

- **批量任务提交**：一次性提交多个仿真任务
- **异步状态轮询**：自动监控任务执行状态
- **并行/串行执行**：可配置的执行模式
- **失败任务重试**：自动重试失败的仿真任务
- **结果自动回收**：自动收集和整理仿真结果
- **进度实时报告**：实时显示任务执行进度
- **多格式输出**：支持JSON、CSV和Markdown报告
- **辅助任务创建**：提供create_n1_tasks和create_vsi_tasks辅助方法

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init batch_task_manager --output batch.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config batch.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("batch_task_manager")

# 配置
config = {
    "skill": "batch_task_manager",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "tasks": [
        {"name": "PF_Base", "type": "power_flow", "max_retries": 2},
        {"name": "PF_Line_1_Out", "type": "power_flow", "config": {"line_outage": "line_1"}, "max_retries": 2},
        {"name": "EMT_Fault", "type": "emt", "config": {"end_time": 10.0}, "max_retries": 1}
    ],
    "execution": {
        "mode": "parallel",           # parallel | sequential
        "max_concurrent": 3,          # 最大并发数（仅parallel模式）
        "polling_interval": 2.0,      # 轮询间隔(s)
        "timeout": 600.0,             # 单任务超时(s)
        "enable_retry": True          # 启用失败重试
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "batch_tasks",
        "save_partial": True          # 保存部分结果
    }
}

# 运行
result = skill.run(config)
print(f"状态: {result.status}")
print(f"成功: {result.data.get('completed_tasks')}/{result.data.get('total_tasks')}")
```

### 3.3 YAML配置示例

```yaml
skill: batch_task_manager
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

tasks:
  - name: PF_Base
    type: power_flow
    max_retries: 2
  - name: PF_Line_1_Out
    type: power_flow
    config:
      line_outage: line_1
    max_retries: 2
  - name: EMT_Fault
    type: emt
    config:
      end_time: 10.0
    max_retries: 1

execution:
  mode: parallel
  max_concurrent: 3
  polling_interval: 2.0
  timeout: 600.0
  enable_retry: true

output:
  format: json
  path: ./results/
  prefix: batch_tasks
  save_partial: true
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: batch_task_manager             # 必需: 技能名称
auth:                              # 认证配置
  token: string                    # 直接提供token（不推荐）
  token_file: string               # token文件路径（默认: .cloudpss_token）

model:                             # 模型配置
  rid: string                      # 模型RID（必需）
  source: enum                     # cloud | local（默认: cloud）

tasks:                             # 任务列表（必需）
  - name: string                   # 任务名称（必需）
    type: enum                     # power_flow | emt（必需）
    config: object                 # 任务配置（可选）
    max_retries: integer           # 最大重试次数（默认: 3）

execution:                         # 执行配置
  mode: enum                       # parallel | sequential（默认: parallel）
  max_concurrent: integer          # 最大并发数（默认: 5，仅parallel模式）
  polling_interval: number         # 轮询间隔(s)（默认: 2.0）
  timeout: number                  # 单任务超时(s)（默认: 600.0）
  enable_retry: boolean            # 启用失败重试（默认: true）

output:                            # 输出配置
  format: enum                     # json | csv（默认: json）
  path: string                     # 输出目录（默认: ./results/）
  prefix: string                   # 文件名前缀（默认: batch_tasks）
  save_partial: boolean            # 保存部分结果（默认: true）
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"batch_task_manager" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `tasks` | array | 是 | - | 任务列表 |
| `tasks[].name` | string | 是 | - | 任务名称（唯一标识） |
| `tasks[].type` | enum | 是 | - | 任务类型：power_flow(潮流) / emt(暂态) |
| `tasks[].config` | object | 否 | {} | 任务配置（如line_outage等） |
| `tasks[].max_retries` | integer | 否 | 3 | 失败时的最大重试次数 |
| `execution.mode` | enum | 否 | parallel | 执行模式：parallel(并行) / sequential(串行) |
| `execution.max_concurrent` | integer | 否 | 5 | 最大并发任务数（仅parallel模式） |
| `execution.polling_interval` | number | 否 | 2.0 | 状态轮询间隔(s) |
| `execution.timeout` | number | 否 | 600.0 | 单任务超时时间(s) |
| `execution.enable_retry` | boolean | 否 | true | 是否启用失败重试 |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | batch_tasks | 文件名前缀 |
| `output.save_partial` | boolean | 否 | true | 是否保存部分成功结果 |

## Agent使用指南

### 5.1 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("batch_task_manager")

# 配置
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "tasks": [
        {"name": "Task_1", "type": "power_flow"},
        {"name": "Task_2", "type": "power_flow"},
        {"name": "Task_3", "type": "emt", "config": {"end_time": 5.0}}
    ],
    "execution": {
        "mode": "parallel",
        "max_concurrent": 3
    }
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status.value == "SUCCESS":
        print(f"批量任务完成: {result.data['completed_tasks']}/{result.data['total_tasks']}")
    else:
        print(f"批量任务失败: {result.error}")
```

### 5.2 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data

    # 访问汇总统计
    print(f"总任务数: {data['total_tasks']}")
    print(f"成功: {data['completed_tasks']}")
    print(f"失败: {data['failed_tasks']}")
    print(f"取消: {data['cancelled_tasks']}")
    print(f"执行时间: {data['execution_time']:.2f}s")
    print(f"平均速度: {data['tasks_per_second']:.2f} tasks/s")

    # 访问任务详情
    for task in data.get("task_details", []):
        print(f"{task['task_id']}: {task['name']} - {task['status']} (重试{task['retry_count']}次)")

    # 访问错误信息
    if data.get("errors"):
        print("错误详情:")
        for task_id, error in data["errors"].items():
            print(f"  {task_id}: {error}")

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
    elif "必须指定任务列表" in error_msg:
        print("错误: tasks数组不能为空")
    else:
        print(f"未知错误: {error_msg}")

# 处理部分失败情况
if result.status.value == "SUCCESS" and result.data.get("failed_tasks", 0) > 0:
    print(f"警告: {result.data['failed_tasks']} 个任务失败")
    for task_id, error in result.data.get("errors", {}).items():
        print(f"  {task_id}: {error}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "total_tasks": 5,
  "completed_tasks": 4,
  "failed_tasks": 1,
  "cancelled_tasks": 0,
  "running_tasks": 0,
  "pending_tasks": 0,
  "execution_time": 120.5,
  "tasks_per_second": 0.04,
  "results": {
    "task_0000": {"job_id": "job_abc123", "status": "completed"},
    "task_0001": {"job_id": "job_def456", "status": "completed"},
    "task_0002": {"job_id": "job_ghi789", "status": "completed"},
    "task_0003": {"job_id": "job_jkl012", "status": "completed"}
  },
  "errors": {
    "task_0004": "仿真失败: job_xyz789"
  },
  "task_details": [
    {
      "task_id": "task_0000",
      "name": "PF_Base",
      "type": "power_flow",
      "status": "completed",
      "retry_count": 0,
      "error": null
    },
    {
      "task_id": "task_0004",
      "name": "EMT_Fault_5",
      "type": "emt",
      "status": "failed",
      "retry_count": 3,
      "error": "仿真失败: job_xyz789"
    }
  ]
}
```

### 6.2 CSV报告格式

| 任务ID | 任务名称 | 类型 | 状态 | 重试次数 | 错误信息 | 耗时(s) |
|--------|----------|------|------|----------|----------|---------|
| task_0000 | PF_Base | power_flow | completed | 0 | | 45.23 |
| task_0001 | PF_Line_1 | power_flow | completed | 0 | | 42.15 |
| task_0002 | PF_Line_2 | power_flow | completed | 1 | | 88.56 |
| task_0003 | EMT_Fault_1 | emt | completed | 0 | | 234.12 |
| task_0004 | EMT_Fault_5 | emt | failed | 3 | 仿真超时 | 600.00 |

### 6.3 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "batch_task_manager" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典，包含任务统计和详情 |
| `artifacts` | list | 输出文件列表（JSON、CSV、Markdown报告） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标（duration, total_tasks等） |

## 设计原理

### 工作流程

```
1. 配置加载与验证
   └── 验证tasks列表非空
   └── 验证每个任务的name和type

2. 任务初始化
   └── 创建BatchTask对象列表
   └── 分配唯一task_id

3. 任务执行
   并行模式:
     └── 使用asyncio.Semaphore限制并发
     └── 同时运行多个任务
   串行模式:
     └── 按顺序逐个执行任务

4. 状态监控
   └── 定期轮询任务状态
   └── 检测完成/失败/超时

5. 失败重试
   └── 失败后自动重试
   └── 达到最大重试次数后标记失败

6. 结果回收
   └── 收集成功任务的job_id
   └── 汇总执行统计

7. 报告生成
   └── 生成JSON结果文件
   └── 生成CSV报告
   └── 生成Markdown报告
```

### 任务状态机

```
PENDING → SUBMITTED → RUNNING → COMPLETED
                              ↘ FAILED (可重试) → PENDING (重试)
                               ↘ FAILED (不可重试) → 终止
                               ↘ CANCELLED → 终止
```

### 核心类

**BatchTask**：任务数据类
- `task_id`: 任务唯一ID
- `name`: 任务名称
- `task_type`: 任务类型（emt/power_flow）
- `status`: 任务状态
- `result`: 任务结果
- `error`: 错误信息
- `retry_count`: 重试次数

**BatchTaskResult**：批量任务执行结果
- `total_tasks`: 总任务数
- `completed_tasks`: 成功任务数
- `failed_tasks`: 失败任务数
- `results`: 任务结果字典
- `errors`: 错误信息字典
- `execution_time`: 执行时间

## 与其他技能的关联

```
n1_security (N-1安全分析)
    ↓ (生成线路列表)
batch_task_manager (create_n1_tasks)
    ↓ (批量执行power_flow)
结果分析和对比

vsi_weak_bus (VSI弱母线分析)
    ↓ (生成母线列表)
batch_task_manager (create_vsi_tasks)
    ↓ (批量执行emt)
VSI计算和分析

param_scan (参数扫描)
    ↓ (生成参数组合)
batch_task_manager
    ↓ (批量执行)
结果汇总
```

**依赖关系**：
- **输入依赖**：无（可独立使用）
- **输出被依赖**：
  - `result_compare`: 对比不同任务的结果
  - `visualize`: 可视化批量任务执行状态

**辅助方法**：
- `create_n1_tasks(model_rid, bus_labels, line_keys)`: 创建N-1分析任务列表
- `create_vsi_tasks(model_rid, bus_labels)`: 创建VSI测试任务列表

## 性能特点

- **执行模式**：
  - 并行模式：资源占用高，执行速度快
  - 串行模式：资源占用低，执行速度慢
- **并发控制**：通过max_concurrent控制并发任务数
- **超时控制**：单任务超时后自动失败
- **重试机制**：失败任务自动重试，提高成功率
- **资源占用**：
  - 内存：与并发任务数成正比
  - 网络：与任务数成正比
- **适用规模**：建议单次批量任务控制在100个以内

## 常见问题

### 问题1: 任务频繁失败

**原因**：
- 超时时间设置过短
- 模型配置错误
- 网络不稳定
- 系统资源不足

**解决**：
```yaml
execution:
  timeout: 1800.0    # 增加超时时间（EMT可能需要更长时间）
  enable_retry: true
  polling_interval: 5.0    # 增加轮询间隔，减少API调用频率

tasks:
  - name: Long_Task
    type: emt
    max_retries: 5    # 增加重试次数
```

### 问题2: 并行执行时资源不足

**原因**：
- 并发数过高导致系统资源耗尽
- CloudPSS API限流

**解决**：
```yaml
execution:
  mode: parallel
  max_concurrent: 2    # 降低并发数

# 或者使用串行模式
execution:
  mode: sequential
```

### 问题3: 结果文件未生成

**原因**：
- 输出路径不存在
- 无写入权限
- 所有任务都失败

**解决**：
```bash
# 确保目录存在
mkdir -p ./results

# 检查权限
chmod 755 ./results
```

```yaml
output:
  path: ./results/
  save_partial: true    # 即使部分失败也保存结果
```

### 问题4: EMT任务和潮流任务混合执行

**原因**：
- EMT任务执行时间长，阻塞潮流任务
- 不同类型任务资源需求不同

**解决**：
```python
# 分开执行不同类型的任务
# 第一批：所有潮流任务
pf_config = {
    "tasks": [t for t in all_tasks if t["type"] == "power_flow"],
    "execution": {"max_concurrent": 10}  # 潮流任务可以多并发
}
pf_result = skill.run(pf_config)

# 第二批：所有EMT任务
emt_config = {
    "tasks": [t for t in all_tasks if t["type"] == "emt"],
    "execution": {"max_concurrent": 2}  # EMT任务少并发
}
emt_result = skill.run(emt_config)
```

## 完整示例

### 场景描述
某电力系统运行部门需要对IEEE39系统进行全面的N-1安全分析，包括所有线路的N-1开断仿真，使用批量任务管理技能高效完成这一任务。

### 配置文件

```yaml
skill: batch_task_manager
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

tasks:
  - name: N1_Base
    type: power_flow
    max_retries: 2
  - name: N1_Line_1
    type: power_flow
    config:
      line_outage: Line_1
    max_retries: 2
  - name: N1_Line_2
    type: power_flow
    config:
      line_outage: Line_2
    max_retries: 2
  - name: N1_Line_3
    type: power_flow
    config:
      line_outage: Line_3
    max_retries: 2
  - name: N1_Gen_1
    type: power_flow
    config:
      generator_outage: Gen_1
    max_retries: 2

execution:
  mode: parallel
  max_concurrent: 5
  polling_interval: 2.0
  timeout: 300.0
  enable_retry: true

output:
  format: json
  path: ./results/
  prefix: n1_analysis
  save_partial: true
```

### 使用辅助方法创建任务

```python
from cloudpss_skills import get_skill

skill = get_skill("batch_task_manager")

# 使用辅助方法创建N-1任务
tasks = skill.create_n1_tasks(
    model_rid="model/holdme/IEEE39",
    bus_labels=["Bus_16", "Bus_15", "Bus_26"],
    line_keys=["Line_1", "Line_2", "Line_3", "Line_4", "Line_5"]
)

config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "tasks": tasks,
    "execution": {
        "mode": "parallel",
        "max_concurrent": 5
    }
}

result = skill.run(config)
```

### 执行命令

```bash
# 创建输出目录
mkdir -p ./results

# 执行批量任务管理
python -m cloudpss_skills run --config n1_batch.yaml
```

### 预期输出

```
[INFO] 批量任务管理开始，共5个任务
[INFO] 并行执行模式，最大并发: 5
[INFO] 任务 task_0000 (N1_Base) 已提交
[INFO] 任务 task_0001 (N1_Line_1) 已提交
...
[INFO] 任务 task_0000 完成
[INFO] 任务 task_0001 完成
...
[INFO] 批量任务管理完成 - 成功:5/5, 耗时:245.32s
[INFO] 结果已保存: ./results/n1_analysis_result.json
```

### 结果文件

**JSON结果文件** (`n1_analysis_result.json`):
```json
{
  "total_tasks": 5,
  "completed_tasks": 5,
  "failed_tasks": 0,
  "cancelled_tasks": 0,
  "execution_time": 245.32,
  "tasks_per_second": 0.02,
  "results": {
    "task_0000": {"job_id": "job_001", "status": "completed"},
    "task_0001": {"job_id": "job_002", "status": "completed"},
    "task_0002": {"job_id": "job_003", "status": "completed"},
    "task_0003": {"job_id": "job_004", "status": "completed"},
    "task_0004": {"job_id": "job_005", "status": "completed"}
  },
  "task_details": [
    {
      "task_id": "task_0000",
      "name": "N1_Base",
      "type": "power_flow",
      "status": "completed",
      "retry_count": 0,
      "error": null
    },
    {
      "task_id": "task_0001",
      "name": "N1_Line_1",
      "type": "power_flow",
      "status": "completed",
      "retry_count": 0,
      "error": null
    }
  ]
}
```

**Markdown报告** (`n1_analysis_report.md`):
```markdown
# 批量任务执行报告

**执行时间**: 2024-03-24 14:32:45
**总任务数**: 5
**成功任务**: 5
**失败任务**: 0
**执行耗时**: 245.32s
**平均速度**: 0.02 tasks/s

## 执行摘要

- **成功率**: 5/5 (100.0%)
- **失败率**: 0/5 (0.0%)

## 任务详情

| 任务ID | 任务名称 | 类型 | 状态 | 重试 |
|--------|----------|------|------|------|
| task_0000 | N1_Base | power_flow | completed | 0 |
| task_0001 | N1_Line_1 | power_flow | completed | 0 |
| task_0002 | N1_Line_2 | power_flow | completed | 0 |
| task_0003 | N1_Line_3 | power_flow | completed | 0 |
| task_0004 | N1_Gen_1 | power_flow | completed | 0 |

## 错误详情

无错误
```

### 后续应用

基于批量任务管理结果，可以：
1. 使用 `result_compare` 对比不同N-1场景的结果
2. 使用 `n1_security` 进行N-1安全指标计算
3. 使用 `visualize` 生成N-1分析可视化报告
4. 使用 `batch_task_manager` 继续进行更深度的分析（如N-2分析）

**关键结论**：所有N-1场景均成功完成潮流计算，系统具有良好的N-1安全性。可以进一步分析各场景下的电压水平和线路负载率。

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
