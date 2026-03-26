# PowerFlowResult API

`PowerFlowResult` 类提供潮流计算结果的快速访问接口，用于获取节点（bus）和支路（branch）的数据。

**研究工作流定位**:
- 在离线研究中，`PowerFlowResult` 通常承担“读结果、看告警、回写模型”的角色
- `getBuses()` / `getBranches()` 适合直接做结果解读
- `getMessagesByKey()` 适合保留原始表结构或排查结果来源
- `powerFlowModify()` 适合把潮流修正结果写回模型，作为下一轮试算或 EMT 仿真的起点

**导入路径**:
```python
from cloudpss.job.result import PowerFlowResult
# 或
from cloudpss import Job

job = Job.fetch('job_id')
result = job.result  # 如果是潮流计算，返回 PowerFlowResult
```

## 基础信息

- 父类: `Result`
- 用途: 潮流计算结果视图
- 仿真类型: `powerFlow`, `three-phase-powerFlow`

## 方法

### getBuses()

获取所有节点（Bus）数据。

```python
def getBuses(self) -> list
```

**返回**:
- 节点数据列表，每个元素是一个包含列数据的字典
- 当前 SDK 会先对原始表格做一层解析，例如去掉 HTML 包装后的输入控件值
- 当前 live 结果里，列头字段常见为 `name`；本地边界测试里也可能出现 `title`

**示例**:
```python
import os

from cloudpss import Model, setToken

# 加载 token
with open('.cloudpss_token', 'r') as f:
    setToken(f.read().strip())

# 获取模型并运行潮流计算
model = Model.fetch(os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39"))
job = model.runPowerFlow()

# 等待仿真完成
while job.status() == 0:
    import time
    time.sleep(1)

# 获取结果
result = job.result  # PowerFlowResult 实例
buses = result.getBuses()

# 解析节点数据
if buses:
    bus_table = buses[0]
    columns = bus_table['data']['columns']
    print("节点列:")
    for col in columns:
        label = col.get('name') or col.get('title') or 'Unknown'
        print(f"  - {label}: {col['data']}")
```

---

### getBranches()

获取所有支路（Branch）数据。

```python
def getBranches(self) -> list
```

**返回**:
- 支路数据列表，每个元素是一个包含列数据的字典
- 当前 SDK 会对原始表格做一层解析，便于直接阅读支路结果
- 当前 live 结果里，列头字段常见为 `name`；本地边界测试里也可能出现 `title`

**示例**:
```python
import os

from cloudpss import Model, setToken

with open('.cloudpss_token', 'r') as f:
    setToken(f.read().strip())

model = Model.fetch(os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39"))
job = model.runPowerFlow()

# 等待完成
while job.status() == 0:
    import time
    time.sleep(1)

result = job.result
branches = result.getBranches()

# 解析支路数据
if branches:
    branch_table = branches[0]
    columns = branch_table['data']['columns']
    print("支路列:")
    for col in columns:
        label = col.get('name') or col.get('title') or 'Unknown'
        print(f"  - {label}: {col['data']}")
```

---

### powerFlowModify()

将潮流计算结果数据写入模型。

这是潮流研究工作流里的关键连接点：
- 先运行潮流并确认模型可算
- 再把稳态修正结果写回模型
- 然后继续调参、改拓扑或进入 EMT 仿真

```python
def powerFlowModify(self, model: dict) -> None
```

**参数**:
- `model` (dict): 可写入的模型字典。实践中应传 `model.toJSON()` 的结果。

**返回**:
- `None`。该方法会原地修改传入的 `model` 字典，不会返回新的模型对象。

**边界行为**:
- 如果结果消息中不存在 `power-flow-modify`，SDK 会抛出异常
- 更稳妥的研究流程是先把修改后的模型导出为本地研究副本，再决定是否云端另存

**示例**:
```python
import os

from cloudpss import Model, setToken

with open('.cloudpss_token', 'r') as f:
    setToken(f.read().strip())

# 方案1: 多次仿真迭代
# 第一次仿真
model1 = Model.fetch(os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39"))
job1 = model1.runPowerFlow()
while job1.status() == 0:
    import time
    time.sleep(1)

result1 = job1.result

# 将第一次结果写入模型字典
model_data = model1.toJSON()
result1.powerFlowModify(model_data)
modified_model = Model(model_data)

# 更稳妥的主线做法是：
# 1. 先导出本地研究分支
Model.dump(modified_model, 'study-case-after-powerflow.yaml', compress=None)

# 2. 在本地副本上继续调参、改拓扑或进入 EMT
# 3. 只有在确认有写权限且确实需要时，再调用:
# modified_model.save('modified-project')

print("潮流结果已写入模型，并已生成本地研究副本")
```

---

## 继承方法

### getMessagesByKey()

从结果消息中获取指定 key 的数据。

对潮流结果来说，这个方法最适合读取原始表格和回写消息。

```python
def getMessagesByKey(self, key: str) -> list
```

**参数**:
- `key` (str): 消息 key，如 `'buses-table'`, `'branches-table'`, `'power-flow-modify'`

**返回**: 消息数据列表

**示例**:
```python
result = job.result

# 直接获取原始消息
buses_raw = result.getMessagesByKey('buses-table')
branches_raw = result.getMessagesByKey('branches-table')

# 获取修改消息
modify_data = result.getMessagesByKey('power-flow-modify')

if modify_data:
    print("可以将潮流修正结果写回模型")
```

---

### getPlots()

获取所有绘图数据（继承自 Result）。

```python
def getPlots(self) -> list
```

**返回**: 绘图数据列表

---

### getPlot()

获取指定索引的绘图数据（继承自 Result）。

```python
def getPlot(self, index: int) -> dict
```

**参数**:
- `index` (int): 绘图索引

**返回**: 绘图数据字典

---

## 数据结构

### 节点数据 (Buses)

节点数据表格包含以下典型列：

注意：这些列名是研究视角下的典型语义归纳，不代表 live 返回一定逐字使用同样的标题文本。实际脚本里更稳妥的做法是同时兼容 `name` 与 `title` 字段。

| 列名 | 描述 |
|------|------|
| Bus | 节点编号 |
| Type | 节点类型 (PQ/PV/Slack) |
| V(pu) | 电压标幺值 |
| Angle(deg) | 电压相角 (度) |
| P(MW) | 有功功率 |
| Q(MVar) | 无功功率 |

### 支路数据 (Branches)

支路数据表格包含以下典型列：

注意：这些列名是研究视角下的典型语义归纳，不代表 live 返回一定逐字使用同样的标题文本。实际脚本里更稳妥的做法是同时兼容 `name` 与 `title` 字段。

| 列名 | 描述 |
|------|------|
| From | 起始节点 |
| To | 终止节点 |
| Circuit | 回路编号 |
| X(pu) | 电抗标幺值 |
| R(pu) | 电阻标幺值 |
| B(pu) | 电纳标幺值 |
| RateA | 额定功率 A |

## 工作流示例

```python
import os
import time

from cloudpss import Model, setToken, Job

# 加载 token
with open('.cloudpss_token', 'r') as f:
    setToken(f.read().strip())

# 获取模型
model = Model.fetch(os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39"))

# 运行潮流计算
print("开始潮流计算...")
job = model.runPowerFlow()

# 轮询等待完成
while job.status() == 0:
    print(f"  仿真状态: 运行中...")
    time.sleep(2)

# 检查结果
if job.status() == 1:  # 完成
    result = job.result
    print("\n=== 潮流计算结果 ===\n")

    # 获取节点数据
    buses = result.getBuses()
    if buses:
        print("节点数据:")
        for col in buses[0]['data']['columns']:
            label = col.get('name') or col.get('title')
            if label and col['data']:
                print(f"  {label}: {col['data'][:5]}...")  # 前5个
        print()

    # 获取支路数据
    branches = result.getBranches()
    if branches:
        print("支路数据:")
        for col in branches[0]['data']['columns']:
            label = col.get('name') or col.get('title')
            if label and col['data']:
                print(f"  {label}: {col['data'][:5]}...")
        print()

    # 获取原始消息（适合排查结果来源）
    raw_buses = result.getMessagesByKey('buses-table')
    raw_branches = result.getMessagesByKey('branches-table')
    print(f"原始节点消息数: {len(raw_buses)}")
    print(f"原始支路消息数: {len(raw_branches)}")

    # 将结果写入模型（可选）
    model_data = model.toJSON()
    result.powerFlowModify(model_data)

elif job.status() == 2:  # 失败
    print("潮流计算失败")
```

## 错误处理

```python
import os

from cloudpss import Model, setToken

with open('.cloudpss_token', 'r') as f:
    setToken(f.read().strip())

model = Model.fetch(os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39"))
job = model.runPowerFlow()

while job.status() == 0:
    import time
    time.sleep(1)

try:
    result = job.result

    # 获取节点数据
    buses = result.getBuses()
    if not buses:
        print("警告: 未获取到节点数据")

    # 获取支路数据
    branches = result.getBranches()
    if not branches:
        print("警告: 未获取到支路数据")

    # 获取原始消息
    raw_messages = result.getMessagesByKey('buses-table')
    if not raw_messages:
        print("警告: 未获取到原始 buses-table 消息")

except Exception as e:
    print(f"获取结果失败: {e}")
```

## 相关文档

- [Model API](./model-api.md)
- [Job API](./job-api.md)
- [EMTResult API](./emtresult-api.md)

## 版本信息

- SDK 版本: 4.5.28+
- 最后更新: 2026-03-16
