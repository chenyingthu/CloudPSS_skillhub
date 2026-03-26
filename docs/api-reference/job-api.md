# Job API 参考

**文件位置**: `cloudpss/job/job.py`

**继承关系**: `Job` 是 CloudPSS SDK 中用于管理仿真任务执行的核心类。

**研究工作流定位**:
- `Job` 是 `Model.runPowerFlow()` / `Model.runEMT()` 之后的桥梁对象
- 它负责承接“任务创建 -> 状态轮询 -> 结果获取”这段流程
- 在普通离线研究里，最常用的是 `status()`、`result` 和 `fetch()`
- `read()` / `write()` 更偏向流式交互能力，当前不属于普通云仿真的主线

---

## 构造函数

### `__init__(...)`

`Job` 的构造函数属于 SDK 内部入口，实际参数是一组展开后的任务字段，而不是一个单独的 `job: dict`。

对研究脚本来说，通常不应直接构造 `Job`，而应通过以下方式获取：

```python
# 1. 通过仿真运行获取
job = model.runEMT()

# 2. 通过 ID 获取
job = Job.fetch(job_id)

# 3. 通过 Job.create 创建
job = Job.create(revisionHash, job_dict, config_dict, rid='model/holdme/IEEE39')
```

当前仓库不会把 `Job.__init__` 作为主线 API 使用。

---

## 静态方法

### `Job.fetch(job_id)`

通过任务 ID 获取仿真任务。

这在研究流程里通常用于：
- 重新连接已经提交的任务
- 在另一个脚本或会话里继续查询状态
- 复查任务 ID 对应的真实结果

**参数**:
- `job_id`: str, 必需。任务 ID。

**返回**:
- `Job` 实例

**示例**:
```python
# 获取任务
job = Job.fetch(existing_job_id)

# 检查状态
status = job.status()
print(f"任务状态：{status}")

# 获取结果（如果已完成）
if status == 1:
    result = job.result
```

**相关方法**:
- `model.runEMT()` - 运行仿真获取 Job
- `Job.create()` - 创建新任务

---

### `Job.create(revisionHash, job, config, name=None, rid=None, policy=None, **kwargs)`

创建新的仿真任务。

对大多数研究脚本来说，优先使用 `model.runEMT()` 或 `model.runPowerFlow()` 更直接；`Job.create()` 更适合需要显式控制 revision/job/config 三元组的场景。

**参数**:
- `revisionHash`: str, 必需。项目版本 hash。
- `job`: dict, 必需。计算方案字典。
- `config`: dict, 必需。参数方案字典。
- `name`: str, 可选。提交任务时传给服务端的名称提示。
- `rid`: str, 可选。项目 RID。
- `policy`: dict, 可选。调度策略。
- `**kwargs`: 透传给底层请求。

**返回**:
- `Job` 实例

**示例**:
```python
import os
import time

from cloudpss import Job, Model

# 获取项目
model = Model.fetch(os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39"))

# 创建任务
job = Job.create(
    revisionHash=model.revision.hash,
    job=model.jobs[0],
    config=model.configs[0],
    rid=model.rid
)

# 等待完成
while job.status() == 0:
    time.sleep(3)

# 获取结果
result = job.result
```

**相关方法**:
- `model.runEMT()` - 直接运行仿真（推荐）
- `Job.fetch()` - 获取已有任务

**注意**:
- 当前 SDK 4.5.28 下，`name` 参数不应被理解为“返回的 `Job` 一定带有稳定可读的 `job.name` 属性”。
- 任务提交后，更稳妥的读取入口仍然是 `job.id`、`job.context`、`job.input`、`job.output` 和 `job.status()`。

---

### `Job.load(file, format="yaml")`

从本地文件加载任务。

这类用法在当前仓库不是主线，因为研究人员通常更关心模型和结果，而不是单独持久化 `Job` 对象。

**参数**:
- `file`: str, 必需。文件路径。
- `format`: str, 可选。文件格式，默认 `'yaml'`。

**返回**:
- 当前 SDK 4.5.28 下返回的是反序列化后的原始数据对象
- 它不会像 `Model.load()` 那样自动包装成 `Job` 实例

**示例**:
```python
job_data = Job.load('saved_job.yaml')
print(type(job_data).__name__)
```

**注意**:
- 如果你需要重新连接真实任务，优先使用 `Job.fetch(job_id)`。
- 当前仓库不把 `Job.load()` 作为研究主线入口。

---

### `Job.dump(job, file, format="yaml", compress="gzip")`

将任务导出到本地文件。

这类用法同样不是当前研究闭环的主线，更常见的是导出模型或结果数据，而不是导出 `Job` 本身。

**参数**:
- `job`: 必需。要写出的任务对象或任务数据。
- `file`: str, 必需。输出文件路径。
- `format`: str, 可选。文件格式，默认 `'yaml'`。
- `compress`: str, 可选。压缩格式，`'gzip'` 或 `None`。

**示例**:
```python
# 导出任务
Job.dump(job, 'job_backup.yaml')

# 导出并压缩
Job.dump(job, 'job_backup.yaml.gz', compress='gzip')
```

**注意**:
- 当前 SDK 4.5.28 下，`Job.dump()` 只是直接调用底层 `IO.dump()` 写出传入对象。
- 它和 `Job.load()` 组合起来更像“原始数据持久化”，不是仓库当前主线里的常用研究能力。

---

## 实例方法

### `job.read(receiver=None, **kwargs)`

创建或复用任务输出接收器，用于读取流式消息。

**参数**:
- `receiver`: 可选。自定义接收器；传入后会直接使用该对象。
- `**kwargs`: 透传给接收器的 `connect()`，例如超时参数。

**返回**:
- `MessageStreamReceiver`: 已连接的消息接收器。

**示例**:
```python
receiver = job.read(timeout=5)

for message in receiver.messages:
    print(message.get('key'))
```

**说明**:
- 首次调用会基于 `job.output` 创建接收器并建立连接。
- 再次调用会复用已创建的接收器。
- 当前仓库已验证其本地包装行为，但普通云仿真研究流程通常不需要直接操作这一层。

---

### `job.write(sender=None, **kwargs)`

创建或复用任务输入发送器，用于向实时仿真写入控制消息。

**参数**:
- `sender`: 可选。自定义发送器；传入后会直接使用该对象。
- `**kwargs`: 透传给发送器的 `connect_legacy()`。

**返回**:
- `MessageStreamSender`: 已连接的消息发送器。

**示例**:
```python
sender = job.write(timeout=5)

# EMTResult.next()/goto()/control() 最终也会复用这条输入流
```

**说明**:
- 首次调用会基于 `job.input` 创建发送器并建立连接。
- `EMTResult` 的实时控制方法通常不需要手动直接写入消息。
- 当前仓库已验证其本地包装行为，但普通云仿真和离线研究通常不把它作为主线 API。

---

### `job.status()`

获取任务状态。

这是 `Job` 在研究流程里最核心的方法之一。典型用法就是轮询等待任务结束，然后再判断是否进入结果分析。

**返回**:
- int: 状态码
  - `0`: 运行中
  - `1`: 已完成
  - `2`: 失败

**示例**:
```python
# 运行仿真
job = model.runEMT()

# 等待完成
while job.status() == 0:
    print("仿真运行中...")
    time.sleep(3)

# 检查结果
if job.status() == 1:
    print("仿真完成")
    result = job.result
elif job.status() == 2:
    print("仿真失败")
```

---

### `job.result`

获取任务结果（只读属性）。

这是 `Job` 在研究流程里最关键的出口：
- 潮流任务会进入 `PowerFlowResult`
- EMT 任务会进入 `EMTResult`
- 后续所有结果读取都从这里展开

**返回**:
- `EMTResult` | `PowerFlowResult` | `IESResult`: 结果实例，取决于仿真类型。
- `None`: 仿真未完成时返回 None。

**示例**:
```python
# 等待完成
while job.status() != 1:
    time.sleep(3)

# 获取 EMT 结果
result = job.result

# 处理 EMT 波形数据
plots = list(result.getPlots())
for i, plot in enumerate(plots):
    print(f"波形分组：{plot['key']}")
    channels = result.getPlotChannelNames(i)
    for ch in channels:
        data = result.getPlotChannelData(i, ch)
        print(f"  通道：{ch}, 数据点：{len(data['x'])}")
```

**相关类**:
- `EMTResult` - EMT 仿真结果
- `PowerFlowResult` - 潮流计算结果
- `IESResult` - 综合能源系统结果；当前仓库未单列该类 API 文档，且没有把 IES 作为主线 live 闭环覆盖

---

### `job.abort(timeout=3)`

中止正在运行的仿真任务。

这个方法已经做了本地边界验证，但在当前仓库的主线研究流程里不是高频入口。更常见的做法是先通过模型和参数校核，减少提交后再中止的需要。

**参数**:
- `timeout`: int, 可选。等待响应的超时时间（秒），默认 3。

**异常**:
- `Exception`: 中止失败时抛出。

**示例**:
```python
# 运行仿真
job = model.runEMT()

# 运行中检查
if job.status() == 0:
    # 中止仿真
    job.abort(timeout=3)
    print("仿真已中止")
```

**注意事项**:
- 只能在仿真运行时调用
- 中止后无法恢复
- 可能需要几秒才能生效
- 当前 SDK 4.5.28 下，该方法本身不返回新的 `Job` 对象或状态字典；如需确认结果，仍应继续调用 `job.status()`

---

---

## 任务类型

Job 可以与以下仿真类型关联：

对当前仓库主线最相关的是：
- EMT
- Power Flow

### 电磁暂态仿真 (EMT)

```python
job = model.runEMT()
# job.result 返回 EMTResult
```

### 移频电磁暂态仿真 (SFEMT)

```python
job = model.runSFEMT()
# job.result 返回 EMTResult
```

当前不作为主线覆盖重点。

### 潮流计算 (Power Flow)

```python
job = model.runPowerFlow()
# job.result 返回 PowerFlowResult
```

### 三相不平衡潮流

```python
job = model.runThreePhasePowerFlow()
# job.result 返回 PowerFlowResult
```

当前不作为主线覆盖重点。

### 综合能源系统仿真 (IES)

```python
job = model.runIESPowerFlow()
job = model.runIESLoadPrediction()
job = model.runIESEnergyStoragePlan()
# job.result 返回 IESResult
```

当前不作为主线覆盖重点。当前仓库只确认 SDK 4.5.28 暴露了这些入口及其预期返回类型，
并未把它们视为已完成的 live 端到端验证链路。

---

## 完整工作流示例

### 示例 1: 基本 EMT 仿真

```python
import os

from cloudpss import Model, setToken

# 设置 token
with open('.cloudpss_token', 'r') as f:
    setToken(f.read().strip())

# 获取项目
model = Model.fetch(os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39"))

# 运行仿真
job = model.runEMT()
print(f"任务 ID: {job.id}")

# 等待完成
import time
while job.status() == 0:
    time.sleep(5)

# 获取结果
result = job.result
plots = list(result.getPlots())
print(f"获取到 {len(plots)} 个波形分组")

# 导出数据
for i, plot in enumerate(plots):
    names = result.getPlotChannelNames(i)
    for name in names:
        data = result.getPlotChannelData(i, name)
        # 处理 data['x'] 和 data['y']
```

### 示例 2: 基本潮流仿真

```python
job = model.runPowerFlow()

while job.status() == 0:
    time.sleep(3)

if job.status() == 1:
    result = job.result
    buses = result.getBuses()
    branches = result.getBranches()
    print(len(buses), len(branches))
```

### 示例 3: 带错误处理

```python
try:
    job = model.runEMT()

    # 监控状态
    while True:
        status = job.status()
        if status == 1:
            print("仿真完成")
            break
        elif status == 2:
            print("仿真失败")
            break
        time.sleep(3)

    # 获取结果
    if job.status() == 1:
        result = job.result
        # 处理结果...

except Exception as e:
    print(f"仿真出错：{e}")
    # 尝试中止
    if 'job' in locals():
        try:
            job.abort(timeout=3)
        except:
            pass
```

### 示例 4: 批量仿真

```python
# 多个参数方案批量仿真
# 这类参数扫描常见于离线研究，但仍建议从已校核的主线模型出发
configs = model.configs
results = []

for i, config in enumerate(configs):
    print(f"运行方案 {i+1}/{len(configs)}")
    job = model.runEMT(config=config)

    # 等待
    while job.status() == 0:
        time.sleep(3)

    if job.status() == 1:
        results.append(job.result)
        print(f"  完成")
    else:
        print(f"  失败")

# 汇总结果
print(f"成功 {len(results)}/{len(configs)}")
```

---

## 属性

### `job.id`

任务唯一标识符。

### `job.context`

任务上下文列表。

在 SDK 4.5.28 的 live `Job` 对象里，`context` 是当前最稳妥的任务语义入口之一。当前已验证常见形态类似：

```python
[
    "function/CloudPSS/power-flow",
    "model/@sdk/1481065046",
    "model/holdme/IEEE39",
]
```

它通常可帮助你识别：

- 任务对应的算法类型
- SDK 为本次运行提交的临时 revision 资源
- 原始模型 RID

### `job.input`

任务输入流地址。

通常只在实时交互或 `job.write()` / `EMTResult.control()` 这类场景下才需要直接关注。

### `job.output`

任务输出流地址。

通常在 `job.read()`、`EMTResult` 流式消息接收或原始消息排查时使用。

### `job.createTime` / `job.startTime` / `job.endTime`

任务创建、开始和结束时间。

### `job.status`

任务状态（通过 `job.status()` 方法获取，不是直接读取属性）。

### 关于 `job.name` 和 `job.rid` 的谨慎说明

当前 SDK 4.5.28 的 `Job` 类构造和 live 返回都**不能**稳定保证 `job.name`、`job.rid` 这两个属性存在。

当前仓库已通过 SDK 源码和 live 探针确认：

- `job.id`、`job.context`、`job.input`、`job.output` 是更可靠的读取入口
- 不应在示例或主线文档里把 `job.name` / `job.rid` 当成稳定字段直接依赖

如果你需要在脚本里打印任务语义，优先打印 `job.id` 和 `job.context`。

---

## 废弃提示

| 废弃 | 替代 |
|------|------|
| `Runner` 类 | `Job` 类 |
| `runner.status` | `job.status()` |
| `runner.result` | `job.result` |

---

## 版本信息

**SDK 版本**: 4.5.28+

**相关文档**:
- [Model API 参考](./model-api.md)
- [EMTResult API 参考](./emtresult-api.md)
- [PowerFlowResult API 参考](./powerflow-result-api.md)
