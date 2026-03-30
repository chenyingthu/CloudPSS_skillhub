# 多配置批量运行技能 (Config Batch Runner)

## 设计背景

### 研究对象
多配置批量运行技能用于对同一模型批量运行多个配置场景，支持CloudPSS的Config机制。这是进行多场景对比分析和参数研究的基础工具。

### 实际需求
在电力系统分析中，经常需要在同一模型上使用不同的仿真配置：
1. **多方案对比**：不同运行方式、不同规划方案
2. **参数研究**：不同参数设置对系统的影响
3. **时序分析**：不同时间断面的系统状态
4. **敏感性分析**：批量测试不同边界条件

### 期望的输入和输出

**输入**：
- 模型配置（RID和来源）
- 配置选择模式（全部、范围、指定索引）
- 自定义参数覆盖
- 执行配置（超时、出错处理）
- 输出配置（格式、路径）

**输出**：
- 每个配置的运行结果和Job ID
- 成功/失败统计
- CSV格式的配置-Job映射表
- JSON格式的完整结果

### 计算结果的用途和价值
多配置批量运行结果可用于：
- 多方案对比评估
- 批量结果收集和管理
- 配置参数的敏感性分析
- 自动化测试和验证

## 功能特性

- **Config机制支持**：利用CloudPSS的Config功能管理多场景
- **多种选择模式**：支持all、range、list三种配置选择方式
- **自定义参数覆盖**：可为所有配置添加统一参数修改
- **批量结果追踪**：自动保存配置到Job ID的映射
- **出错继续执行**：可配置出错时是否继续执行剩余配置
- **多格式输出**：支持JSON和CSV格式结果

## 快速开始

### CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init config_batch_runner --output config_batch.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config config_batch.yaml
```

### Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("config_batch_runner")

# 配置
config = {
    "skill": "config_batch_runner",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "configs": {
        "mode": "all",              # all | range | list
        "start": 0,                 # range模式起始索引
        "end": 5,                   # range模式结束索引
        "indices": [0, 2, 4],       # list模式指定索引
        "custom_args": {            # 自定义参数覆盖
            "end_time": 10.0,
            "step_time": 0.0001
        }
    },
    "execution": {
        "polling_interval": 5.0,    # 轮询间隔(s)
        "timeout": 3600.0,          # 总超时(s)
        "continue_on_error": True   # 出错继续
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "config_batch"
    }
}

# 运行
result = skill.run(config)
print(f"状态: {result.status}")
print(f"成功: {result.data.get('completed')}/{result.data.get('total')}")
```

### YAML配置示例

```yaml
skill: config_batch_runner
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

configs:
  mode: all                    # 运行所有配置
  custom_args:                 # 为所有配置添加的参数
    end_time: 10.0
    step_time: 0.0001

execution:
  polling_interval: 5.0
  timeout: 3600.0
  continue_on_error: true

output:
  format: json
  path: ./results/
  prefix: config_batch
```

## 配置Schema

### 完整配置结构

```yaml
skill: config_batch_runner          # 必需: 技能名称
auth:                              # 认证配置
  token: string                    # 直接提供token（不推荐）
  token_file: string               # token文件路径（默认: .cloudpss_token）

model:                             # 模型配置
  rid: string                      # 模型RID（必需）
  source: enum                     # cloud | local（默认: cloud）

configs:                           # 配置选择（必需）
  mode: enum                       # all | range | list（默认: all）
  start: integer                   # range模式起始索引
  end: integer                     # range模式结束索引
  indices: array                   # list模式指定索引列表
  custom_args: object              # 自定义参数覆盖

execution:                         # 执行配置
  polling_interval: number         # 轮询间隔(s)（默认: 5.0）
  timeout: number                  # 总超时(s)（默认: 3600.0）
  continue_on_error: boolean       # 出错继续（默认: true）

output:                            # 输出配置
  format: enum                     # json | csv（默认: json）
  path: string                     # 输出目录（默认: ./results/）
  prefix: string                   # 文件名前缀（默认: config_batch）
```

### 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"config_batch_runner" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `configs.mode` | enum | 否 | all | 配置选择模式 |
| `configs.start` | integer | 否 | 0 | range模式起始索引（包含） |
| `configs.end` | integer | 否 | - | range模式结束索引（不包含） |
| `configs.indices` | array | 否 | [] | list模式指定的配置索引列表 |
| `configs.custom_args` | object | 否 | {} | 应用到所有配置的自定义参数 |
| `execution.polling_interval` | number | 否 | 5.0 | 状态轮询间隔(s) |
| `execution.timeout` | number | 否 | 3600.0 | 总超时时间(s) |
| `execution.continue_on_error` | boolean | 否 | true | 单个配置失败时是否继续 |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | config_batch | 文件名前缀 |

### 配置选择模式说明

**all模式**：运行模型的所有配置
```yaml
configs:
  mode: all
```

**range模式**：运行指定范围内的配置
```yaml
configs:
  mode: range
  start: 0    # 从第0个配置开始
  end: 5      # 到第4个配置结束（不包含5）
```

**list模式**：运行指定索引的配置
```yaml
configs:
  mode: list
  indices: [0, 2, 4, 6]  # 只运行第0、2、4、6个配置
```

## Agent使用指南

### 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("config_batch_runner")

# 配置 - 运行所有配置
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "configs": {"mode": "all"}
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status.value == "SUCCESS":
        print(f"批量运行完成: {result.data['completed']}/{result.data['total']}")
    else:
        print(f"批量运行失败: {result.error}")
```

### 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data

    # 访问汇总统计
    print(f"总配置数: {data['total']}")
    print(f"成功: {data['completed']}")
    print(f"失败: {data['failed']}")

    # 访问配置-Job映射
    for config_idx, job_info in data.get("results", {}).items():
        print(f"配置 {config_idx}: Job {job_info['job_id']} - {job_info['status']}")

    # 访问错误信息
    if data.get("errors"):
        print("错误详情:")
        for config_idx, error in data["errors"].items():
            print(f"  配置 {config_idx}: {error}")

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
    elif "配置索引超出范围" in error_msg:
        print("错误: 请检查configs.start和configs.end设置")
    else:
        print(f"未知错误: {error_msg}")

# 处理部分失败情况
if result.status.value == "SUCCESS" and result.data.get("failed", 0) > 0:
    print(f"警告: {result.data['failed']} 个配置运行失败")
    for config_idx, error in result.data.get("errors", {}).items():
        print(f"  配置 {config_idx}: {error}")
```

## 输出结果

### JSON输出格式

```json
{
  "total": 5,
  "completed": 5,
  "failed": 0,
  "model_rid": "model/holdme/IEEE39",
  "results": {
    "0": {"job_id": "job_abc123", "status": "completed"},
    "1": {"job_id": "job_def456", "status": "completed"},
    "2": {"job_id": "job_ghi789", "status": "completed"},
    "3": {"job_id": "job_jkl012", "status": "completed"},
    "4": {"job_id": "job_mno345", "status": "completed"}
  },
  "errors": {},
  "config_indices": [0, 1, 2, 3, 4],
  "execution_time": 245.5
}
```

### CSV报告格式

| 配置索引 | Job ID | 状态 | 错误信息 |
|----------|--------|------|----------|
| 0 | job_abc123 | completed | |
| 1 | job_def456 | completed | |
| 2 | job_ghi789 | completed | |
| 3 | job_jkl012 | completed | |
| 4 | job_mno345 | failed | 仿真超时 |

### SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "config_batch_runner" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典，包含配置运行统计和详情 |
| `artifacts` | list | 输出文件列表（JSON、CSV报告） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标（duration等） |

## 设计原理

### 工作流程

```
1. 配置加载与验证
   └── 验证model.rid非空
   └── 验证configs.mode有效
   └── 验证range模式start < end

2. 获取配置列表
   └── 从模型获取所有可用配置
   └── 根据mode筛选目标配置

3. 批量执行
   └── 遍历每个目标配置
   └── 应用custom_args覆盖
   └── 提交仿真任务
   └── 轮询等待完成
   └── 记录结果或错误

4. 结果汇总
   └── 统计成功/失败数量
   └── 生成配置-Job映射表

5. 报告生成
   └── 生成JSON结果文件
   └── 生成CSV报告
```

## 与其他技能的关联

```
model_parameter_extractor (模型参数提取)
    ↓ (获取模型信息)
config_batch_runner
    ↓ (批量运行多配置)
result_compare (结果对比)
    ↓ (对比不同配置结果)
可视化分析
```

**依赖关系**：
- **输入依赖**：无（可独立使用）
- **输出被依赖**：
  - `result_compare`: 对比不同配置的结果
  - `batch_task_manager`: 进一步批量处理

**典型工作流**：
1. 使用 `config_batch_runner` 批量运行多配置
2. 使用 `result_compare` 对比分析不同配置的结果差异
3. 使用 `visualize` 生成对比可视化报告

## 性能特点

- **执行方式**：串行执行（CloudPSS Config机制限制）
- **超时控制**：可配置总超时时间
- **错误处理**：可配置出错时是否继续执行
- **资源占用**：
  - 内存：较低（一次只运行一个配置）
  - 网络：与配置数成正比
- **适用规模**：适合运行10-100个配置的场景

## 常见问题

### 问题1: 配置索引超出范围

**原因**：
- start/end设置错误
- 模型配置数量少于预期

**解决**：
```yaml
# 先检查模型有多少配置
configs:
  mode: all    # 先运行all模式查看总配置数
```

### 问题2: 部分配置运行失败

**原因**：
- 某些配置本身有错误
- 仿真参数不兼容

**解决**：
```yaml
execution:
  continue_on_error: true    # 继续执行剩余配置
  timeout: 7200.0           # 增加超时时间
```

### 问题3: 需要统一修改所有配置的参数

**解决**：
```yaml
configs:
  mode: all
  custom_args:              # 应用到所有配置的参数
    end_time: 15.0
    step_time: 0.00005
```

## 完整示例

### 场景描述
某电力系统规划部门需要对IEEE39系统的5个规划方案进行EMT仿真分析，每个方案是一个配置，需要批量运行并收集结果。

### 配置文件

```yaml
skill: config_batch_runner
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

configs:
  mode: range
  start: 0
  end: 5
  custom_args:
    end_time: 10.0
    step_time: 0.0001

execution:
  polling_interval: 5.0
  timeout: 7200.0
  continue_on_error: true

output:
  format: json
  path: ./results/
  prefix: planning_scenarios
```

### 执行命令

```bash
# 创建输出目录
mkdir -p ./results

# 执行批量配置运行
python -m cloudpss_skills run --config config_batch.yaml
```

### 预期输出

```
[INFO] 多配置批量运行开始，共5个配置
[INFO] 模式: range (0-4)
[INFO] 配置 0 已提交: job_abc123
[INFO] 配置 0 完成
[INFO] 配置 1 已提交: job_def456
[INFO] 配置 1 完成
...
[INFO] 多配置批量运行完成 - 成功:5/5, 耗时:245.32s
[INFO] 结果已保存: ./results/planning_scenarios_result.json
[INFO] Job映射已保存: ./results/planning_scenarios_mapping.csv
```

### 结果文件

**JSON结果文件** (`planning_scenarios_result.json`):
```json
{
  "total": 5,
  "completed": 5,
  "failed": 0,
  "model_rid": "model/holdme/IEEE39",
  "results": {
    "0": {"job_id": "job_001", "status": "completed"},
    "1": {"job_id": "job_002", "status": "completed"},
    "2": {"job_id": "job_003", "status": "completed"},
    "3": {"job_id": "job_004", "status": "completed"},
    "4": {"job_id": "job_005", "status": "completed"}
  },
  "config_indices": [0, 1, 2, 3, 4],
  "execution_time": 245.5
}
```

**CSV映射文件** (`planning_scenarios_mapping.csv`):
```csv
config_index,job_id,status
0,job_001,completed
1,job_002,completed
2,job_003,completed
3,job_004,completed
4,job_005,completed
```

### 后续应用

基于批量运行结果，可以：
1. 使用 `result_compare` 对比不同规划方案的结果
2. 使用 `visualize` 生成多方案对比可视化
3. 进行方案优选和决策支持

**关键结论**：所有5个规划方案EMT仿真均成功完成，可以进一步分析各方案的暂态稳定性和电能质量指标。

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
