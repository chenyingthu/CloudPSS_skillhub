# Component API 参考

`Component` 类表示模型中的元件，包括电阻、电容、电感、电源等电气元件，以及连接线等。

**研究工作流定位**:
- `Component` 很少作为单独入口使用，研究人员通常通过 `Model` 来查询和修改元件
- 常见顺序是：先定位目标元件，再修改参数或连接关系，最后做拓扑和可算性检查
- 为避免误改原始算例，建议优先在本地工作副本上进行元件操作

**导入路径**:
```python
from cloudpss.model.implements.component import Component
```

## 属性

| 属性 | 类型 | 描述 |
|------|------|------|
| `id` | str | 元件唯一标识符 |
| `definition` | str | 元件定义，例如 `'model/CloudPSS/resistor'` |
| `label` | str | 元件标签/名称 |
| `args` | dict | 元件参数数据 |
| `pins` | dict | 元件引脚数据 |
| `shape` | str | 形状类型：`diagram-component`（元件）或 `diagram-edge`（连接线）|
| `props` | dict | 元件属性，如 `{enabled: true}` |
| `context` | dict | 元件上下文 |
| `canvas` | str | 所在图纸，如 `'canvas_0'` |
| `position` | dict | 位置，如 `{'x': 100, 'y': 200}` |
| `size` | dict | 尺寸，如 `{'width': 80, 'height': 40}` |
| `zIndex` | int | 渲染层级 |
| `style` | dict | 样式定义 |

## 通过 Model 类操作元件

元件操作主要通过 `Model` 类的方法进行。

推荐顺序：

1. `Model.fetch()` 或 `Model.load()` 获取算例
2. `Model.dump()` 创建本地工作副本
3. 用 `getComponentByKey()` / `getComponentsByRid()` 定位目标元件
4. 用 `addComponent()` / `updateComponent()` / `removeComponent()` 改模
5. 用 `fetchTopology()` 做 revision 级结构检查，再用真实求解验证未保存本地改动

### `diagram-edge` 的当前边界

当前 SDK 4.5.28 暴露了 `model.addComponent()`，但没有公开的高层 `addEdge()`。

这意味着：

- 普通元件可以直接通过 `addComponent()` 新增
- 如果研究动作涉及“复制现有接线关系”，有时需要直接操作 `revision.getImplements().getDiagram().cells`
- `cells` 中的值本质上就是 `Component` 对象，因此可以手工插入 `shape="diagram-edge"` 的连接线对象

当前仓库已经在真实 `model/holdme/IEEE3` 上验证过一条谨慎边界：

- 仅新增 `_NewVoltageMeter` 和 `_newChannel` 还不够
- 必须把新电压表通过一条 meter->bus 的 `diagram-edge` 接回电网拓扑
- 这样新增的 `vac_added:*` 通道才能稳定出现在 EMT 输出里
- 同类路径已进一步在 `IEEE3 Bus2` 和无现成电压表模板的 `IEEE39 bus37` 上复验通过

这说明 `diagram-edge` 不是纯显示元素，而是 EMT 可算性的一部分。这里应把它视为低层 escape hatch，而不是把它误写成 SDK 已有公开连线 API。

### addComponent()

在模型中添加新元件。

```python
def addComponent(
    self,
    definition: str,
    label: str,
    args: dict = {},
    pins: dict = {},
    canvas: str = None,
    position: dict = None,
    size: dict = None
) -> Component
```

**参数**:
- `definition` (str): 元件定义 RID，如 `'model/CloudPSS/resistor'`
- `label` (str): 元件标签
- `args` (dict, 可选): 元件参数，如 `{'resistance': 10}`
- `pins` (dict, 可选): 引脚定义
- `canvas` (str, 可选): 所在图纸，默认第一个图纸
- `position` (dict, 可选): 位置，如 `{'x': 100, 'y': 200}`
- `size` (dict, 可选): 尺寸，如 `{'width': 80, 'height': 40}`

**返回**: Component 实例

**示例**:
```python
import os

from cloudpss import Model, setToken

# 加载 token
with open('.cloudpss_token', 'r') as f:
    setToken(f.read().strip())

# 获取模型并创建本地工作副本
model = Model.fetch(os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39"))
Model.dump(model, 'component-working-copy.yaml', compress=None)
working_model = Model.load('component-working-copy.yaml')

# 添加电阻元件
resistor = working_model.addComponent(
    definition='model/CloudPSS/resistor',
    label='R1',
    args={'resistance': 10},  # 10 Ohm
    pins={'p': {'x': 0, 'y': 0}, 'n': {'x': 50, 'y': 0}},
    position={'x': 100, 'y': 200}
)

print(f"添加元件: {resistor.label}, ID: {resistor.id}")

```

当前仓库还额外验证过两个边界：

- 在真实 `model/holdme/IEEE39` 的 fetched 工作副本上，添加临时电阻、修改其参数后，`fetchTopology(implementType="powerFlow")` 仍可正常返回拓扑结果
- 但该返回结果不会直接反映尚未保存的本地 add/update/remove；这类改动是否真正进入求解流程，应继续用真实 `runPowerFlow()` / `runEMT()` 验证

如果要新增量测元件并接入已有母线，目前推荐的做法不是“凭空拼出一条 edge”，而是：

1. 先从现有可工作的量测元件上找到对应的 `diagram-edge`
2. 克隆这条 edge 的 `attrs/target/vertices` 结构
3. 只改新 edge 的 `id` 和 `source.cell`
4. 再把它注入 `diagram.cells`

这样做的原因是，不同元件类型的 edge 可能带有不同的 `anchor`、`selector` 或折线顶点信息，直接手写最小字典容易再次触发拓扑错误或 EMT 奇异矩阵。

如果目标模型里完全没有可克隆的电压表 edge，目前也存在一个更谨慎的 fallback：

1. 仍然新增 `_NewVoltageMeter` 与 `_newChannel`
2. 手工构造一个 `_newBus_3p` 常见连接形式的 `diagram-edge`
3. 再用 EMT 波形和 `V_rms ≈ V_pu * VBase / sqrt(3)` 做正确性校核

这条 fallback 已在真实 `model/holdme/IEEE39` 的 `bus37` 上通过，但当前证据还不足以把它提升为“任意模型通用模板”。

---

### removeComponent()

从模型中删除元件。

```python
def removeComponent(self, key: str) -> bool
```

**参数**:
- `key` (str): 元件的 key（从 `getAllComponents()` 或 `getComponentByKey()` 获取）

**返回**: bool - 删除成功返回 `True`，否则返回 `False`

**示例**:
```python
from cloudpss import Model

model = Model.load('component-working-copy.yaml')

# 获取所有元件
components = model.getAllComponents()

# 找到并删除特定元件
for key, component in components.items():
    if component.label == 'R1':
        success = model.removeComponent(key)
        print(f"删除 {'R1'}: {success}")
        break
```

---

### updateComponent()

更新元件属性。

```python
def updateComponent(self, key: str, **kwargs)
```

**参数**:
- `key` (str): 元件的 key
- `**kwargs`: 要更新的属性，支持：
  - `definition` (str): 元件定义
  - `label` (str): 元件标签
  - `args` (dict): 元件参数
  - `pins` (dict): 引脚数据
  - `position` (dict): 位置
  - `size` (dict): 尺寸
  - `style` (dict): 样式
  - `props` (dict): 属性
  - `zIndex` (int): 渲染层级

**返回**:
- 当前 SDK 4.5.28 中成功时返回 `None`
- 找不到组件时返回 `False`
- 参数非法时抛出异常

**示例**:
```python
from cloudpss import Model

model = Model.load('component-working-copy.yaml')

# 获取一个已有元件
first_key = next(iter(model.getAllComponents()))
component = model.getComponentByKey(first_key)

# 更新电阻值
model.updateComponent(
    first_key,
    args={'resistance': 50}  # 从 10 Ohm 改为 50 Ohm
)

# 更新元件位置
model.updateComponent(
    first_key,
    position={'x': 200, 'y': 300}
)

# 批量更新
model.updateComponent(
    first_key,
    label='R1_50ohm',
    args={'resistance': 50},
    position={'x': 200, 'y': 300}
)

component = model.getComponentByKey(first_key)
print(component.args['resistance'])

# 可先做一次 revision 级结构检查
topology = model.fetchTopology(implementType='powerFlow')
print(len(topology.toJSON()['components']))

# 若要确认未保存本地改动是否真正进入求解，再做真实仿真
result = model.runPowerFlow().result
```

---

### getComponentByKey()

通过 key 获取单个元件。

```python
def getComponentByKey(self, componentKey: str) -> Component
```

**参数**:
- `componentKey` (str): 元件的 key

**返回**: Component 实例

**示例**:
```python
from cloudpss import Model

model = Model.load('component-working-copy.yaml')

# 通过 key 获取元件
component = model.getComponentByKey('canvas_0_757')
print(f"元件: {component.label}, 定义: {component.definition}")
```

---

### getComponentsByRid()

通过元件类型 RID 获取元件。

```python
def getComponentsByRid(self, rid: str) -> dict
```

**参数**:
- `rid` (str): 元件定义 RID，如 `'model/CloudPSS/resistor'`

**返回**: dict - key 到 Component 实例的映射

**示例**:
```python
from cloudpss import Model

model = Model.load('component-working-copy.yaml')

# 获取所有电阻
resistors = model.getComponentsByRid('model/CloudPSS/resistor')
print(f"电阻数量: {len(resistors)}")

# 获取所有电感
inductors = model.getComponentsByRid('model/CloudPSS/inductor')

```

---

## Component 实例方法

### toJSON()

将元件序列化为字典。

```python
def toJSON(self) -> dict
```

**返回**: 包含元件数据的字典

**示例**:
```python
import os

from cloudpss import Model

model = Model.fetch(os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39"))
first_key = next(iter(model.getAllComponents()))
component = model.getComponentByKey(first_key)

# 序列化为 JSON
component_dict = component.toJSON()
print(component_dict)
```

## 常用元件定义 (RID)

以下是 CloudPSS 常用元件的 RID：

| 元件类型 | RID |
|----------|-----|
| 电阻 | `model/CloudPSS/resistor` |
| 电感 | `model/CloudPSS/inductor` |
| 电容 | `model/CloudPSS/capacitor` |
| 电压源 | `model/CloudPSS/acvoltageSource` |
| 二极管 | `model/CloudPSS/diode` |
| IGBT | `model/CloudPSS/IGBT` |
| MOSFET | `model/CloudPSS/MOSFET` |
| 变压器 | `model/CloudPSS/transformer` |

## 错误处理

```python
import os

from cloudpss import Model

model = Model.fetch(os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39"))

try:
    # 尝试更新不存在的元件
    success = model.updateComponent(
        'non_existent_key',
        args={'resistance': 10}
    )
except Exception as e:
    print(f"错误: {e}")
    # 可能的错误:
    # - "Component has no attribute xxx" (属性不存在)
    # - "Component args must be dict" (参数类型错误)
```

## 相关文档

- [Model API](./model-api.md)
- [ModelRevision API](./revision-api.md)

## 版本信息

- SDK 版本: 4.5.28+
- 最后更新: 2026-03-16
