# ModelRevision API

`ModelRevision` 表示某个模型当前版本的底层数据。对普通离线研究来说，它不是最先接触的入口，但在下面三类场景里很关键：

- 需要直接查看当前 revision 的实现数据、参数和 hash
- 需要基于指定 `implementType` 与 `config` 拉取拓扑
- 需要显式指定 `job + config + rid`，以当前 revision 直接提交任务

如果只是开展常规研究流程，通常先从 [Model API](./model-api.md) 入手；只有当你已经拿到 `model.revision`，并且要做更精细的拓扑或任务控制时，再进入 `ModelRevision`。

## 已验证约束

以下行为已经通过真实 CloudPSS API 或 SDK 本地边界测试验证：

- `revision.run()` 需要显式传入 `job` 和 `config`
- `revision.fetchTopology('emtp'|'powerFlow', config, maximumDepth)` 可正常返回 `ModelTopology`
- `ModelRevision.create()` 会剥离已有 `hash` 后再提交新 revision 创建请求

## 导入路径

```python
from cloudpss import ModelRevision
# 或
from cloudpss.model import ModelRevision
```

## 构造函数

```python
ModelRevision(revision: dict = {})
```

这个构造函数主要由 SDK 内部使用。研究脚本里更常见的获取方式是：

```python
from cloudpss import Model

model = Model.fetch("model/holdme/IEEE39")
revision = model.revision
```

## 实例属性

| 属性 | 类型 | 描述 |
|------|------|------|
| `implements` | `ModelImplement` | 当前版本的实现数据 |
| `parameters` | `dict | list` | 当前版本的参数数据 |
| `pins` | `dict` | 当前版本的引脚信息 |
| `documentation` | `dict` | 当前版本的文档信息 |
| `hash` | `str` | 当前版本唯一标识 |

## 方法

### `getImplements()`

获取当前 revision 对应的实现封装。

```python
def getImplements(self) -> ModelImplement
```

**返回**: `ModelImplement`

**适用场景**:

- 想查看 revision 是否包含 `diagram`
- 想把实现数据序列化后做本地检查

**示例**:

```python
from cloudpss import Model

model = Model.fetch("model/holdme/IEEE39")
implements = model.revision.getImplements()

print(type(implements).__name__)
print(implements.toJSON().keys())
```

---

### `run()`

以当前 revision 为基础提交仿真任务。

```python
def run(
    self,
    job: dict,
    config: dict,
    name: str = None,
    policy: dict = None,
    stop_on_entry: bool = None,
    rid: str = None,
    **kwargs
) -> Job
```

**参数**:

- `job`: 必需。计算方案字典
- `config`: 必需。参数方案字典
- `name`: 可选。提交任务时传给服务端的名称提示
- `policy`: 可选。调度策略
- `stop_on_entry`: 可选。是否在入口处停止
- `rid`: 可选。模型 RID
- `**kwargs`: 透传给底层请求

**返回**: `Job`

**研究工作流中的位置**:

- 当你已经明确选定某个 revision、job、config 组合时使用
- 比 `model.runEMT()` / `model.runPowerFlow()` 更底层
- 适合需要显式控制 revision 提交过程的脚本

**示例**:

```python
from cloudpss import Model

model = Model.fetch("model/holdme/IEEE39")

job = model.revision.run(
    job=model.jobs[0],
    config=model.configs[0],
    name="revision-run-example",
    rid=model.rid,
)

print(job.id)
print(job.status())
```

**注意**:

- 不要再写“省略 `job` / `config` 也能自动跑”的示例；当前 SDK 行为不是这样
- 如果你只是想运行默认方案，优先使用 `model.run()` / `model.runEMT()` / `model.runPowerFlow()`
- 当前 SDK 4.5.28 下，也不要把这里的 `name` 参数理解成“返回的 `Job` 上一定有 `job.name` 可读”；若要识别任务语义，优先读取 `job.id` 和 `job.context`

---

### `fetchTopology()`

按指定实现类型和参数方案拉取当前 revision 的拓扑。

```python
def fetchTopology(
    self,
    implementType: str,
    config: dict,
    maximumDepth: int,
    **kwargs
) -> ModelTopology
```

**参数**:

- `implementType`: 必需。常见值为 `'emtp'`、`'powerFlow'`、`'sfemt'`
- `config`: 必需。参数方案字典
- `maximumDepth`: 必需。diagram 元件展开最大递归深度
- `**kwargs`: 透传给底层请求

**返回**: `ModelTopology`

**研究工作流中的位置**:

- 对指定 revision 做结构级检查
- 为潮流或 EMT 仿真确认该 revision 的拓扑是否正确展开
- 在 `model.fetchTopology()` 不够明确时，直接指定 revision 版本来取拓扑

**边界说明**:

- `revision.fetchTopology()` 本质上就是 revision-hash 驱动的远端拓扑展开
- 因此它适合验证“某个已保存 revision/config 的结构长什么样”
- 它不应被用来证明 fetched 工作副本里尚未保存的本地改动已经进入拓扑

**示例**:

```python
from cloudpss import Model

model = Model.fetch("model/holdme/IEEE39")

emt_topology = model.revision.fetchTopology(
    implementType="emtp",
    config=model.configs[0],
    maximumDepth=1,
)
print(emt_topology.toJSON().keys())

powerflow_topology = model.revision.fetchTopology(
    implementType="powerFlow",
    config=model.configs[0],
    maximumDepth=1,
)
print(powerflow_topology.toJSON().keys())
```

---

### `toJSON()`

将 revision 序列化为字典。

```python
def toJSON(self) -> dict
```

**返回**: `dict`

**示例**:

```python
from cloudpss import Model

model = Model.fetch("model/holdme/IEEE39")
revision_dict = model.revision.toJSON()

print(revision_dict["hash"])
print(revision_dict["implements"].keys())
```

---

### `create()` [静态方法]

创建一个新的 revision 记录。

```python
@staticmethod
def create(revision, parentHash: str = None, **kwargs) -> dict
```

**参数**:

- `revision`: 必需。`ModelRevision` 对象
- `parentHash`: 可选。父 revision hash
- `**kwargs`: 透传给底层请求

**返回**: `dict`，形如 `{"hash": "..."}`

**研究工作流中的位置**:

- 通常由 `revision.run()` 间接触发
- 只有在你要显式管理 revision 生命周期时才直接调用

**示例**:

```python
from cloudpss import Model
from cloudpss.model import ModelRevision

model = Model.fetch("model/holdme/IEEE39")
created = ModelRevision.create(model.revision)

print(created["hash"])
```

## 相关文档

- [Model API](./model-api.md)
- [Job API](./job-api.md)
- [建模与改模工作流指南](../guides/model-building-workflow.md)

## 版本信息

- SDK 版本: 4.5.28+
- 最后更新: 2026-03-16
