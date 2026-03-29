# 批量任务管理技能

异步批量运行 CloudPSS 仿真任务，支持并行/串行执行、状态轮询、失败重试和结果回收。

## 功能特性

- **批量任务提交**: 一次性提交多个仿真任务
- **异步状态轮询**: 自动监控任务执行状态
- **并行/串行执行**: 可配置的执行模式
- **失败任务重试**: 自动重试失败的仿真任务
- **结果自动回收**: 自动收集和整理仿真结果
- **进度实时报告**: 实时显示任务执行进度

## 适用场景

- N-1 安全分析 (批量故障场景)
- VSI 弱母线分析 (批量母线测试)
- 参数扫描 (批量参数组合)
- 故障扫描 (批量故障位置/类型)

## 快速开始

### 1. 基本使用

```python
from cloudpss_skills import get_skill

skill = get_skill("batch_task_manager")

config = {
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "tasks": [
        {"name": "PF_Base", "type": "power_flow", "max_retries": 2},
        {"name": "EMT_Fault", "type": "emt", "config": {"end_time": 10.0}}
    ],
    "execution": {
        "mode": "parallel",
        "max_concurrent": 3,
        "polling_interval": 2.0,
        "timeout": 600.0,
        "enable_retry": True
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "batch_tasks"
    }
}

result = skill.run(config)
```

### 2. 使用配置文件

```bash
python -m cloudpss_skills run --config config/batch_task_manager.yaml
```

### 3. 运行示例

```bash
python examples/analysis/batch_task_manager_example.py
```

## 工作流程

```
1. 配置加载
   └── 读取YAML配置或Python字典

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
   └── 生成JSON/CSV/Markdown报告

7. 输出报告
   └── *_result.json - 详细结果
   └── *_report.csv - 任务执行报告
   └── *_report.md - Markdown报告
```

## 核心类

### BatchTask

任务数据类，存储单个任务的完整信息。

```python
@dataclass
class BatchTask:
    task_id: str                    # 任务唯一ID
    name: str                       # 任务名称
    task_type: str                  # 任务类型 (emt, power_flow)
    config: Dict[str, Any]          # 任务配置
    status: TaskStatus              # 任务状态
    result: Any                     # 任务结果
    error: Optional[str]            # 错误信息
    submitted_at: datetime          # 提交时间
    started_at: datetime            # 开始时间
    completed_at: datetime          # 完成时间
    retry_count: int                # 重试次数
    max_retries: int                # 最大重试次数
```

### TaskStatus

任务状态枚举。

```python
class TaskStatus(Enum):
    PENDING = "pending"      # 等待提交
    SUBMITTED = "submitted"  # 已提交
    RUNNING = "running"      # 运行中
    COMPLETED = "completed"  # 完成
    FAILED = "failed"        # 失败
    CANCELLED = "cancelled"  # 取消
```

### BatchTaskResult

批量任务执行结果。

```python
@dataclass
class BatchTaskResult:
    total_tasks: int                # 总任务数
    completed_tasks: int            # 成功任务数
    failed_tasks: int               # 失败任务数
    cancelled_tasks: int            # 取消任务数
    running_tasks: int              # 运行中任务数
    pending_tasks: int              # 等待中任务数
    results: Dict[str, Any]         # 任务结果
    errors: Dict[str, str]          # 错误信息
    execution_time: float           # 执行时间
```

## 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model.rid` | string | - | 模型RID（必需） |
| `model.source` | enum | cloud | 模型来源 (cloud/local) |
| `tasks` | array | - | 任务列表（必需） |
| `tasks[].name` | string | - | 任务名称（必需） |
| `tasks[].type` | enum | - | 任务类型: emt, power_flow（必需） |
| `tasks[].config` | object | {} | 任务配置 |
| `tasks[].max_retries` | int | 3 | 最大重试次数 |
| `execution.mode` | enum | parallel | 执行模式: parallel, sequential |
| `execution.max_concurrent` | int | 5 | 最大并发数（仅parallel模式） |
| `execution.polling_interval` | float | 2.0 | 轮询间隔（秒） |
| `execution.timeout` | float | 600.0 | 单任务超时（秒） |
| `execution.enable_retry` | bool | True | 启用失败重试 |
| `output.format` | enum | json | 输出格式: json, csv |
| `output.path` | string | ./results/ | 输出路径 |
| `output.prefix` | string | batch_tasks | 文件名前缀 |
| `output.save_partial` | bool | True | 保存部分结果 |

## 辅助方法

### create_n1_tasks

创建N-1分析任务列表。

```python
n1_tasks = skill.create_n1_tasks(
    model_rid="model/holdme/IEEE39",
    bus_labels=["Bus_16", "Bus_15"],
    line_keys=["line_1", "line_2", "line_3"]
)
```

返回:
```python
[
    {"name": "N1_Line_1", "type": "power_flow", "config": {"line_outage": "line_1"}},
    {"name": "N1_Line_2", "type": "power_flow", "config": {"line_outage": "line_2"}},
    ...
]
```

### create_vsi_tasks

创建VSI测试任务列表。

```python
vsi_tasks = skill.create_vsi_tasks(
    model_rid="model/holdme/IEEE39",
    bus_labels=["Bus_16", "Bus_15", "Bus_26"]
)
```

返回:
```python
[
    {
        "name": "VSI_Bus_Bus_16",
        "type": "emt",
        "config": {
            "target_bus": "Bus_16",
            "injection_time": 8.0,
            "injection_duration": 0.5,
            "end_time": 15.0
        }
    },
    ...
]
```

## 执行模式对比

| 特性 | 并行模式 | 串行模式 |
|------|----------|----------|
| 资源占用 | 高 | 低 |
| 执行速度 | 快 | 慢 |
| 适用场景 | 大量独立任务 | 资源受限/依赖任务 |
| 失败影响 | 其他任务继续 | 可立即停止 |

## 输出文件

### JSON结果 (`*_result.json`)

```json
{
  "total_tasks": 5,
  "completed_tasks": 4,
  "failed_tasks": 1,
  "cancelled_tasks": 0,
  "execution_time": 120.5,
  "tasks_per_second": 0.04,
  "results": {
    "task_0000": {"job_id": "job_abc123", "status": "completed"},
    "task_0001": {"job_id": "job_def456", "status": "completed"}
  },
  "errors": {
    "task_0004": "仿真失败: job_xyz789"
  },
  "task_details": [
    {
      "task_id": "task_0000",
      "name": "N1_Line_1",
      "type": "power_flow",
      "status": "completed",
      "retry_count": 0
    }
  ]
}
```

### CSV报告 (`*_report.csv`)

| 任务ID | 任务名称 | 类型 | 状态 | 重试次数 | 错误信息 | 耗时(s) |
|--------|----------|------|------|----------|----------|---------|
| task_0000 | N1_Line_1 | power_flow | completed | 0 | | 45.23 |
| task_0001 | N1_Line_2 | power_flow | failed | 3 | 仿真超时 | 600.00 |

### Markdown报告 (`*_report.md`)

- 执行摘要
- 成功率统计
- 任务详情表格
- 错误详情

## 使用建议

### 1. 选择合适的执行模式

- **并行模式**: 大量独立的潮流计算任务
- **串行模式**: EMT仿真任务（资源密集型）

### 2. 配置合理的并发数

```yaml
# 对于power_flow任务，可增加并发
execution:
  max_concurrent: 10

# 对于emt任务，减少并发以避免资源竞争
execution:
  max_concurrent: 2
```

### 3. 设置适当的超时时间

```yaml
# 潮流计算通常较快
timeout: 300.0

# EMT仿真可能需要更长时间
timeout: 1800.0
```

### 4. 启用失败重试

```yaml
execution:
  enable_retry: true
# 为每个任务配置重试次数
tasks:
  - name: "Critical_Task"
    max_retries: 5
```

## 故障排查

### 问题1: 任务频繁失败

**原因**: 超时时间设置过短或模型问题
**解决**: 增加timeout值，检查模型配置

### 问题2: 并行执行时资源不足

**原因**: 并发数过高导致系统资源耗尽
**解决**: 降低max_concurrent值

### 问题3: 结果文件未生成

**原因**: 输出路径不存在或无写入权限
**解决**: 检查output.path是否存在且有写入权限

### 问题4: 认证失败

**原因**: Token无效或过期
**解决**: 检查.cloudpss_token文件或CLOUDPSS_TOKEN环境变量

## 与已有技能的关联

```
N-1安全分析 (n1_security)
    ↓ (生成线路列表)
batch_task_manager (create_n1_tasks)
    ↓ (批量执行power_flow)
结果分析和对比

VSI弱母线分析 (vsi_weak_bus)
    ↓ (生成母线列表)
batch_task_manager (create_vsi_tasks)
    ↓ (批量执行emt)
VSI计算和分析
```

## 性能注意事项

- **内存使用**: 并行模式会占用更多内存
- **API限流**: 注意CloudPSS API的调用频率限制
- **网络稳定性**: 长时间运行的批量任务需要稳定的网络连接
- **结果存储**: 大量任务的结果会占用较多磁盘空间

## 参考实现

基于 [PSA Skills](https://git.tsinghua.edu.cn/yuanxuefeng/psa-skills-0.2.3) 的批量任务管理功能实现。

## 版本历史

- **v1.0**: 基础批量任务管理功能
  - 并行/串行执行模式
  - 状态轮询和结果回收
  - 失败重试机制
  - N-1和VSI任务创建辅助方法
