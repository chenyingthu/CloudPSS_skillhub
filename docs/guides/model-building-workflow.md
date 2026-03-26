# 建模与改模工作流指南

本指南面向普通离线研究场景，描述如何基于已有算例、模板算例或本地文件构建研究用电力系统模型。

## 适用场景

这条工作流适用于以下常见任务：

- 从模板算例出发搭建研究对象
- 基于已有工程做参数变型或拓扑变型
- 添加、替换或删除元件
- 为潮流试算和 EMT 仿真准备研究分支

## 核心 API

### 模型获取与保存

- `Model.fetch`
- `Model.fetchMany`
- `Model.load`
- `Model.dump`
- `Model.save`

### 元件与拓扑操作

- `model.getAllComponents`
- `model.getComponentByKey`
- `model.getComponentsByRid`
- `model.addComponent`
- `model.updateComponent`
- `model.removeComponent`
- `model.fetchTopology`

## 推荐步骤

### 1. 选择研究起点

优先顺序通常如下：

1. 已验证可算的已有算例
2. 官方或团队内部模板算例
3. 本地保存的研究中间版本

常见入口：

```python
import os

from cloudpss import Model

# 从云端获取已有算例
model = Model.fetch(os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39"))

# 或从本地加载中间版本
model = Model.load("study-case.yaml")
```

当前仓库的研究起点示例也已经支持这两种入口，并会在输入本地 YAML 时默认建议新的 `*-branch.yaml` 工作副本路径，避免覆盖原文件。

### 2. 先做工作分支，而不是直接改原模型

研究中最常见的失误之一，是直接在唯一模型上反复修改。

更稳妥的做法是：

```python
Model.dump(model, "working-copy.yaml", compress=None)
working_model = Model.load("working-copy.yaml")
```

当前仓库也已经把“从已有本地研究副本继续管理分支”收敛为主线的一部分；不需要每次都重新从云端取起点。

同时，分支管理示例会在“输入本地 YAML”时默认建议新的 `*-branch.yaml` 输出路径，避免把输入副本直接覆盖掉。

组件改模示例也已经按同样原则收紧：既可从 `model/holdme/IEEE39` 这类已验证只读模型起步，也可从已有本地 YAML 起步；在真实模型的本地工作副本上，`addComponent()`、`updateComponent()`、`removeComponent()` 本身已有 live 支撑，而 `fetchTopology(implementType="powerFlow")` 目前只应理解为 revision 级拓扑拉取仍然可用。

这样做的好处：

- 不会立即污染原始算例
- 可以保留每轮试算的中间状态
- 后续更方便比较不同参数和拓扑方案

如果后续研究需要给某个 `_newBus_3p` 母线补挂新的 EMT 电压量测链，也应先在这一步导出本地工作副本，再继续修改。当前仓库已经 live 验证过一条受限配方，但它依赖底层 `diagram-edge` 注入，不应直接当作通用高层 SDK 建模能力使用。对应说明见：

- `docs/guides/emt-voltage-meter-chain-guide.md`

### 3. 识别关键元件

在开始修改前，先用查询接口定位研究对象：

```python
components = working_model.getAllComponents()
transformers = working_model.getComponentsByRid("model/CloudPSS/transformer")
target = working_model.getComponentByKey("canvas_0_123")
```

这一步适合用于：

- 统计模型规模
- 找到目标元件
- 确认要修改的是正确对象，而不是误改别的同类元件

### 4. 执行改模操作

#### 添加元件

```python
new_component = working_model.addComponent(
    definition="model/CloudPSS/resistor",
    label="R_test",
    args={"resistance": 10},
    pins={"p": {}, "n": {}},
    position={"x": 100, "y": 200},
)
```

#### 更新元件

```python
working_model.updateComponent(
    new_component.id,
    args={"resistance": 20},
)
```

#### 删除元件

```python
working_model.removeComponent(new_component.id)
```

### 5. 做结构级检查

改模完成后，可以先确认指定实现类型下的 revision 拓扑可以正确展开：

```python
topology = working_model.fetchTopology(implementType="powerFlow")
topology_data = topology.toJSON()

print(len(topology_data["components"]))
print(topology_data["mappings"].keys())
```

如果后续目标是 EMT 仿真，也可以检查：

```python
emt_topology = working_model.fetchTopology(implementType="emtp")
```

这里要特别注意一个真实云端已经验证过的边界：

- 对 `Model.fetch()` 得到、且保留 `revision.hash` 的工作副本，`fetchTopology()` 仍按远端 saved revision 拉取拓扑
- 它不会直接证明本地尚未保存的 add/update/remove 已经反映到返回结果中
- 因此这一步更适合作为“当前 revision/config 能否展开”的检查，而不是未保存改模的最终验收

如果你要确认本地改动已经真正进入求解路径，应继续做真实的潮流或 EMT 试算。

### 6. 保存研究中间版本

研究过程中建议同时保留：

- 本地快照
- 必要时的云端研究分支

本地快照：

```python
Model.dump(working_model, "study-case-v2.yaml", compress=None)
```

云端研究分支：

```python
working_model.save("study-case-v2")
```

推荐做法：

- 不轻易覆盖原始模型
- 用新 key 保存研究分支
- 在关键节点保留本地文件版本

## 进入下一条工作流

改模完成后，下一步一般有两种：

1. 进入潮流工作流，检查模型是否可算并获得稳态初值
2. 在已有可信初值基础上，进入 EMT 工作流
3. 如果目标是补挂 `_newBus_3p` 母线电压量测链，则进入受限的 EMT 前置准备指南

对应指南：

- `docs/guides/powerflow-study-workflow.md`
- `docs/guides/emt-study-workflow.md`
- `docs/guides/emt-voltage-meter-chain-guide.md`

## 对应示例与文档

- 示例：`examples/basic/component_example.py`
- 示例：`examples/basic/model_save_dump_example.py`
- 示例：`examples/basic/emt_voltage_meter_chain_example.py`
- API：`docs/api-reference/model-api.md`
- API：`docs/api-reference/component-api.md`
- 主线说明：`docs/guides/research-workflow-core-apis.md`
