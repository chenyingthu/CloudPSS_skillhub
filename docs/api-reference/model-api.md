# Model API 参考

**文件位置**: `cloudpss/model/model.py`

**继承关系**: `Model` 是 CloudPSS SDK 的核心类，用于项目和模型的管理。

**研究工作流定位**:
- 研究人员通常先通过 `Model.fetch()` / `Model.load()` 获取已有算例
- 然后围绕 `getAllComponents()`、`addComponent()`、`updateComponent()`、`removeComponent()` 改模
- 再通过 `fetchTopology()` 做 revision 级结构检查
- 最后进入 `runPowerFlow()` 或 `runEMT()` 的分析流程

如果当前目标是离线研究而不是直接覆盖线上模型，建议先用 `Model.dump()` 导出本地工作副本，再继续修改。

## 构造函数

### `__init__(model: dict = {})`

初始化 Model 实例。

**参数**:
- `model`: dict, 可选。项目数据字典，包含 rid、name、description、revision 等字段。

**示例**:
```python
import os

# 从云端获取（推荐）
model = Model.fetch(os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39"))

# 从本地文件加载
model = Model.load('project.yaml')
```

---

## 静态方法

### `Model.fetch(rid, **kwargs)`

通过项目 rid 从云端获取单个项目。

**参数**:
- `rid`: str, 必需。项目资源 ID，格式为 `model/owner/key`。

**返回**:
- `Model` 实例

**异常**:
- `Exception`: 当项目不存在或无权访问时抛出。

**示例**:
```python
import os

# 获取项目
model = Model.fetch(os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39"))
print(f"项目名称：{model.name}")
print(f"元件数量：{len(model.getAllComponents())}")
```

**相关方法**:
- `Model.fetchMany()` - 获取多个项目
- `Model.load()` - 从本地文件加载

---

### `Model.fetchMany(name=None, cursor=[], pageSize=10, owner=None, **kwargs)`

获取用户可访问的项目列表，支持搜索和分页。

**参数**:
- `name`: str, 可选。搜索关键词，模糊匹配项目名称。
- `cursor`: list, 可选。分页游标，用于获取下一页数据。
- `pageSize`: int, 可选。每页返回的项目数量，默认 10。
- `owner`: str, 可选。
  - `None`: 获取当前用户的项目（默认）
  - `'*'`: 获取所有用户的项目
  - 指定用户名：获取该用户的项目

**返回**:
- list[dict]: 项目信息列表，每个 dict 包含：
  - `rid`: 项目 RID
  - `name`: 项目名称
  - `description`: 项目描述
  - `owner`: 所有者
  - `tags`: 标签
  - `updatedAt`: 更新时间

**当前 SDK 4.5.28 的实际边界**:
- 方法签名里虽然有 `cursor` 参数
- 但当前返回值只有 `items` 列表，不会把分页 cursor 一并返回给调用者
- 因此仓库当前只把它当作“搜索和列出可访问模型”的入口，而不把完整翻页链路写成已沉淀能力

**示例**:
```python
# 获取当前用户的前 10 个项目
models = Model.fetchMany(pageSize=10)

# 搜索名称包含 'IEEE' 的项目
models = Model.fetchMany(name='IEEE')

# 只看指定 owner 的项目
owner_models = Model.fetchMany(owner='holdme', pageSize=10)

# 获取所有用户的项目
all_models = Model.fetchMany(owner='*')

# 搜索当前可访问的 IEEE 类模型
matches = Model.fetchMany(name='IEEE', owner='*', pageSize=5)
for item in matches:
    print(item['rid'], item['name'])
```

**相关方法**:
- `Model.fetch()` - 获取单个项目

---

### `Model.load(filePath, format="yaml")`

从本地文件加载项目。

这个方法非常适合研究过程中的“本地工作分支”：
- 先从云端获取成熟算例
- 用 `Model.dump()` 导出到本地
- 再用 `Model.load()` 恢复并继续改模

**参数**:
- `filePath`: str, 必需。文件路径。
- `format`: str, 可选。文件格式，默认 `'yaml'`。

**返回**:
- `Model` 实例

**异常**:
- `FileNotFoundError`: 文件不存在时抛出。

**示例**:
```python
# 从 YAML 文件加载工作副本
model = Model.load('working-copy.yaml')

# 从压缩文件加载
model = Model.load('project.yaml.gz')
```

**相关方法**:
- `Model.dump()` - 导出项目到文件
- `Model.fetch()` - 从云端获取

---

### `Model.dump(model, file, format="yaml", compress="gzip")`

将项目导出到本地文件。

在研究工作流里，`Model.dump()` 的主要价值不是“备份一下”，而是显式创建本地研究分支，避免直接污染原始算例。

**参数**:
- `model`: Model, 必需。Model 实例。
- `file`: str, 必需。输出文件路径。
- `format`: str, 可选。文件格式，默认 `'yaml'`。
- `compress`: str, 可选。压缩格式，`'gzip'` 或 `None`。

**示例**:
```python
# 导出为 YAML 工作副本
Model.dump(model, 'working-copy.yaml', compress=None)

# 导出为压缩 YAML
Model.dump(model, 'project.yaml.gz', compress='gzip')

# 导出为 JSON（如果支持）
Model.dump(model, 'project.json', format='json')
```

**相关方法**:
- `Model.load()` - 从文件加载
- `model.save()` - 保存到云端

---

### `Model.create(model, **kwargs)`

创建新项目。

这属于较底层的 SDK 接口。对当前仓库的研究工作流来说，一般不应直接调用，而应优先使用 `model.save('new-key')` 创建新的云端研究分支。

**参数**:
- `model`: Model, 必需。Model 实例。

**返回**:
- GraphQL 响应

**当前语义说明**:
- `model.save('new-key')` 会在云端创建或指向一个新的算例 RID
- 但它不会返回一个新的 `Model` 实例
- 当前这个 `model` 对象本身会被重定向到新的 `rid`
- 如果你既要保留旧算例的本地对象，又要创建新的云端研究分支，应该先做本地副本，再在副本对象上调用 `save('new-key')`

**示例**:
```python
# 更推荐的研究工作流写法
model.save('new-project')
```

---

### `Model.update(model, **kwargs)`

更新现有项目。

这同样属于较底层的 SDK 接口。对研究流程来说，更推荐直接使用 `model.save()`，并且只在明确要覆盖当前模型时这样做。

**参数**:
- `model`: Model, 必需。Model 实例。

**返回**:
- GraphQL 响应

**示例**:
```python
# 推荐方式
model.save()  # 不指定 key 时更新现有项目
```

---

## 实例方法 - 项目操作

### `model.save(key=None)`

保存项目到云端。

对研究流程来说，更推荐的用法是：
- `model.save()` 只用于更新你自己拥有、并且明确准备覆盖的模型
- `model.save('new-key')` 用于将当前研究状态另存为新的云端分支

**参数**:
- `key`: str, 可选。项目唯一标识符。
  - `None`: 更新现有项目（根据 rid）
  - 指定 key: 创建新项目或覆盖同名项目

**返回**:
- GraphQL 响应

**异常**:
- `Exception`: 保存失败时抛出。

**示例**:
```python
# 更新现有项目（仅在确认要覆盖当前模型时使用）
model.save()

# 更常见的研究用法：另存为新的云端分支
model.save('study-case-v2')
print(model.rid)  # model/当前用户/study-case-v2

# 如果只想保留本地分支，优先使用 dump()
Model.dump(model, 'study-case-v2.yaml', compress=None)
```

**注意事项**:
- key 只能包含字母、数字和下划线
- 创建新项目时必须指定唯一的 key
- 保存时当前用户必须是项目所有者
- 对研究流程而言，优先保留本地工作副本；云端保存更适合在关键节点创建研究分支
- `save('new-key')` 的“新算例”发生在云端资源层，不是“返回一个新的本地 Model 对象”

**相关方法**:
- `Model.dump()` - 导出到本地

---

### `model.toJSON()`

将 Model 实例序列化为 dict。

**返回**:
- dict: 包含所有项目数据的字典。

**示例**:
```python
model_dict = model.toJSON()
print(model_dict.keys())
# dict_keys(['rid', 'name', 'description', 'revision', 'configs', 'jobs', 'context'])
```

---

## 实例方法 - 元件操作

### `model.getAllComponents()`

获取项目中的所有元件。

**返回**:
- dict[str, Component]: 元件字典，key 为元件标识符，value 为 Component 实例。

**异常**:
- `ValueError`: 当项目没有拓扑实现时抛出。

**示例**:
```python
components = model.getAllComponents()
print(f"元件总数：{len(components)}")

for key, comp in components.items():
    print(f"  {key}: {comp.definition}")
```

**相关方法**:
- `model.getComponentByKey()` - 通过 key 获取元件
- `model.getComponentsByRid()` - 通过类型获取元件

---

### `model.getComponentByKey(componentKey: str)`

通过元件的 key 获取元件。

**参数**:
- `componentKey`: str, 必需。元件标识符。

**返回**:
- Component: 元件实例。

**示例**:
```python
component = model.getComponentByKey('canvas_0_1')
print(f"元件类型：{component.definition}")
print(f"元件参数：{component.args}")
```

---

### `model.getComponentsByRid(rid: str)`

通过元件类型 rid 获取元件。

**参数**:
- `rid`: str, 必需。元件类型 rid，如 `'model/CloudPSS/resistor'`。

**返回**:
- dict[str, Component]: 匹配的元件字典。

**示例**:
```python
# 获取所有电阻
resistors = model.getComponentsByRid('model/CloudPSS/resistor')
print(f"电阻数量：{len(resistors)}")

# 获取所有电容
capacitors = model.getComponentsByRid('model/CloudPSS/capacitor')
```

---

### `model.addComponent(definition, label, args, pins, canvas=None, position=None, size=None)`

添加新元件到项目。

**参数**:
- `definition`: str, 必需。元件类型 rid。
- `label`: str, 必需。元件标签。
- `args`: dict, 必需。元件参数。
- `pins`: dict, 必需。元件引脚连接信息。
- `canvas`: str, 可选。画布 ID。
- `position`: dict, 可选。元件位置，如 `{'x': 100, 'y': 200}`。
- `size`: dict, 可选。元件尺寸，如 `{'width': 80, 'height': 40}`。

**返回**:
- Component: 创建的元件实例。

**示例**:
```python
# 添加电阻
resistor = model.addComponent(
    definition='model/CloudPSS/resistor',
    label='R1',
    args={'resistance': 100},
    pins={'p': {}, 'n': {}}
)
```

---

### `model.updateComponent(key, **kwargs)`

更新元件参数。

**参数**:
- `key`: str, 必需。元件标识符。
- `**kwargs`: 可选。要更新的参数字段。

**返回**:
- 当前 SDK 4.5.28 中，成功时返回 `None`
- 找不到组件时返回 `False`
- 参数非法时抛出异常

**示例**:
```python
# 更新电阻值
model.updateComponent('canvas_0_1', args={'resistance': 200})

# 更新多个参数
model.updateComponent('canvas_0_1',
    args={'resistance': 200},
    label='R_new'
)
```

---

### `model.removeComponent(key)`

删除元件。

**参数**:
- `key`: str, 必需。元件标识符。

**返回**:
- bool: 是否成功。

**示例**:
```python
model.removeComponent('canvas_0_1')
```

---

## 实例方法 - 计算方案操作

### `model.createJob(jobType: str, name: str)`

创建新的计算方案。

**参数**:
- `jobType`: str, 必需。方案类型：
  - `'emtp'`: 电磁暂态仿真
  - `'sfemt'`: 移频电磁暂态仿真
  - `'powerFlow'`: 潮流计算
- `name`: str, 必需。方案名称。

**返回**:
- dict: 计算方案字典。

**注意**:
- 创建后需要调用 `model.addJob()` 添加到项目中。
- 如果 `jobType` 不在 SDK 内置定义中，当前实现会抛出 `KeyError`。

**示例**:
```python
# 创建 EMT 仿真方案
job = model.createJob('emtp', '我的 EMT 仿真')
model.addJob(job)

# 创建潮流计算方案
job = model.createJob('powerFlow', '潮流计算')
model.addJob(job)
```

**相关方法**:
- `model.addJob()` - 添加到项目
- `model.getModelJob()` - 获取方案

---

### `model.addJob(job: dict)`

将计算方案添加到项目。

**参数**:
- `job`: dict, 必需。计算方案字典。

**示例**:
```python
job = model.createJob('emtp', 'EMT 仿真')
model.addJob(job)
```

---

### `model.getModelJob(name)`

获取指定名称的计算方案。

**参数**:
- `name`: str, 必需。方案名称。

**返回**:
- list[dict]: 同名方案列表。

**示例**:
```python
jobs = model.getModelJob('EMT 仿真')
if jobs:
    job = jobs[0]
    print(f"方案 RID: {job['rid']}")
```

---

## 实例方法 - 参数方案操作

### `model.createConfig(name: str)`

创建新的参数方案。

**参数**:
- `name`: str, 必需。方案名称。

**返回**:
- dict: 参数方案字典。

**注意**:
- 基于当前模型的第一个参数方案创建，创建后需要调用 `model.addConfig()` 添加。
- 如果模型当前没有任何参数方案，当前实现无法直接创建新的 config。

**示例**:
```python
config = model.createConfig('我的参数方案')
model.addConfig(config)
```

---

### `model.addConfig(config: dict)`

将参数方案添加到项目。

**参数**:
- `config`: dict, 必需。参数方案字典。

**返回**:
- dict: 添加后的方案。

---

### `model.getModelConfig(name)`

获取指定名称的参数方案。

**参数**:
- `name`: str, 必需。方案名称。

**返回**:
- list[dict]: 同名方案列表。

---

## 实例方法 - 仿真运行

### `model.runEMT(job=None, config=None, **kwargs)`

运行电磁暂态（EMT）仿真。

通常建议在以下前提下调用：
- 模型结构已经稳定
- 潮流初值已经准备好，或已有可信初始状态
- 示波器和量测通道已经配置完成

**参数**:
- `job`: str|dict, 可选。计算方案名称或字典，默认使用当前选中的 EMT 方案。
- `config`: str|dict, 可选。参数方案名称或字典，默认使用当前选中的参数方案。

**返回**:
- `Job[EMTResult]`: 仿真任务实例。

**异常**:
- `Exception`: 当没有 EMT 计算方案时抛出。

**示例**:
```python
# 使用默认方案
job = model.runEMT()

# 指定方案名称
job = model.runEMT(job='EMT 仿真 1')

# 指定方案和参数
job = model.runEMT(job='EMT 仿真 1', config='参数方案 1')

# 等待完成并获取结果
result = job.result
plots = result.getPlots()
```

**相关方法**:
- `model.runSFEMT()` - 移频 EMT 仿真
- `model.runPowerFlow()` - 潮流计算
- `Job.fetch()` - 获取任务状态

---

### `model.runSFEMT(job=None, config=None, **kwargs)`

运行移频电磁暂态（SFEMT）仿真。

**说明**:
- SDK 提供该能力
- 但当前仓库不把它作为离线研究主线的端到端覆盖重点

**参数**: 同 `runEMT()`。

**返回**:
- `Job[EMTResult]`: 仿真任务实例。

---

### `model.runPowerFlow(job=None, config=None, **kwargs)`

运行潮流计算。

这是离线研究中最常用的校核入口之一：
- 检查模型是否可算
- 获取稳态运行点
- 为后续 EMT 仿真准备初值

**参数**: 同 `runEMT()`。

**返回**:
- `Job[PowerFlowResult]`: 仿真任务实例。

---

### `model.runThreePhasePowerFlow(job=None, config=None, **kwargs)`

运行三相不平衡潮流计算。

**说明**:
- 该能力当前不属于仓库主线覆盖重点
- 当前主线仍以普通潮流和 EMT 的离线研究闭环为主

**参数**: 同 `runEMT()`。

**返回**:
- `Job[PowerFlowResult]`: 仿真任务实例。

---

### `model.run(job=None, config=None, name=None, **kwargs)`

通用仿真运行方法（底层方法）。

**参数**:
- `job`: dict, 可选。计算方案。
- `config`: dict, 可选。参数方案。
- `name`: str, 可选。提交任务时传给服务端的名称提示。

**返回**:
- `Job`: 仿真任务实例。

**说明**:
- 此方法是 `runEMT()`、`runPowerFlow()` 等的底层实现，通常不直接调用。
- 当前 SDK 4.5.28 下，不应因为传了 `name` 就假设返回的 `Job` 实例上稳定存在 `job.name` 属性；研究脚本更稳妥的读取入口仍然是 `job.id`、`job.context` 和 `job.status()`。

---

## 实例方法 - 拓扑操作

### `model.fetchTopology(implementType=None, config=None, maximumDepth=None, **kwargs)`

获取项目的拓扑数据。

在研究工作流里，`fetchTopology()` 更适合被理解为“revision 级结构检查”：
- 检查当前 revision 在指定实现类型下能否正确展开
- 读取展开后的组件与映射结构
- 再决定是否进入潮流或 EMT 仿真

当前仓库在真实云端上额外确认了一个重要边界：
- 对 `Model.fetch()` 得到、且仍携带 `revision.hash` 的工作副本，`fetchTopology()` 仍按远端 saved revision 拉取拓扑
- 它不会把本地尚未保存的 `addComponent()` / `updateComponent()` / `removeComponent()` 直接投影进返回结果
- 因此，未保存本地改动是否真的进入求解路径，不应仅靠 `fetchTopology()` 判断，而应以真实 `runPowerFlow()` / `runEMT()` 结果为准

**参数**:
- `implementType`: str, 可选。实现类型：
  - `'emtp'`: 电磁暂态（默认）
  - `'powerFlow'`: 潮流计算
  - `'sfemt'`: 移频 EMT
- `config`: dict, 可选。参数方案，默认使用当前选中的方案。
- `maximumDepth`: int, 可选。最大递归深度，用于元件展开。

**返回**:
- `ModelTopology`: 拓扑实例。

**示例**:
```python
# 获取 EMT 拓扑
topology = model.fetchTopology()
topology_data = topology.toJSON()
print(len(topology_data['components']))

# 获取潮流拓扑
topology = model.fetchTopology(implementType='powerFlow')

# 限制展开深度
topology = model.fetchTopology(maximumDepth=2)
```

**使用建议**:
- 把 `fetchTopology()` 当作 revision/config 级的拓扑展开入口，而不是“未保存本地改动已生效”的直接证据
- 如果脚本刚在 fetched 工作副本上新增、删除或更新了元件，想确认求解器是否真正接受这些改动，应继续做真实 `runPowerFlow()` 或 `runEMT()` 验证

---

## 属性

### `model.rid`

项目资源 ID，格式为 `model/owner/key`。

### `model.name`

项目名称。

### `model.description`

项目描述。

### `model.revision`

项目版本信息（`ModelRevision` 实例）。

### `model.configs`

所有参数方案列表。

### `model.jobs`

所有计算方案列表。

### `model.context`

项目上下文信息，包含：
- `currentJob`: 当前选中的计算方案索引
- `currentConfig`: 当前选中的参数方案索引

---

## 废弃提示

以下接口在当前 SDK 生态里不建议作为新脚本入口：

| 废弃 | 替代 |
|------|------|
| `Project` 类 | `Model` 类 |
| `Runner` 类 | `Job` 类 |
| `model.run()` | `model.runEMT()` / `model.runPowerFlow()` 等 |

---

## 版本信息

**SDK 版本**: 4.5.28+

**相关文档**:
- [Job API 参考](./job-api.md)
- [ModelRevision API 参考](./revision-api.md)
- [EMTResult API 参考](./emtresult-api.md)
