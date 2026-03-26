# CloudPSS 研究工作流核心 API

本指南定义当前仓库的主攻范围：不按 SDK 类表面结构铺开，而按研究人员最常见的离线仿真工作流组织文档、示例和测试。

## 目标边界

当前优先覆盖的是以下工作：

1. 从已有算例、模板算例或本地文件出发，得到可研究的电力系统模型。
2. 修改拓扑、元件和参数，构建研究场景。
3. 进行潮流计算，验证模型可算性并获得初值。
4. 反复调整系统结构和参数，识别薄弱环节与安全边界。
5. 在可算模型上添加故障或扰动，运行 EMT 仿真。
6. 提取波形结果，支撑后续稳定性分析。

当前不优先覆盖的内容：

- 实时仿真控制和在线交互设备相关 API
- IES、三相不平衡等扩展方向
- 仅为类完整性存在、但不进入常见研究闭环的方法

## 工作流主线

### 1. 算例获取与保存

研究通常从现有模型出发，而不是从零写 GraphQL 请求。

核心 API：

- `Model.fetch`
- `Model.fetchMany`
- `Model.load`
- `Model.dump`
- `Model.save`

对应任务：

- 从平台获取模板或已有算例
- 从本地文件恢复模型
- 保存研究过程中的中间版本

### 2. 算例构建与修改

研究人员需要围绕元件、拓扑和参数反复改模。

核心 API：

- `model.getAllComponents`
- `model.getComponentByKey`
- `model.getComponentsByRid`
- `model.addComponent`
- `model.updateComponent`
- `model.removeComponent`

对应任务：

- 插入或替换元件
- 修改元件参数
- 调整连接关系前的结构检查

### 3. 拓扑与可算性检查

模型修改后，首先要确认当前拓扑是否与目标分析类型一致。

核心 API：

- `model.fetchTopology`
- `revision.fetchTopology`

对应任务：

- 获取 EMT 或潮流视角下的拓扑
- 检查 revision 级组件展开结果
- 为后续潮流和 EMT 仿真做准备

边界上要注意：

- `fetchTopology()` 很适合做 revision/config 级展开检查
- 但对 fetched 工作副本里的未保存本地改动，不能把它当作最终验证依据
- 这类改动是否真实进入求解流程，仍应以 `runPowerFlow()` / `runEMT()` 的 live 结果为准

### 4. 潮流分析与反复试算

潮流分析是离线研究的基础步骤，既用于模型校核，也用于动态仿真初值准备。

核心 API：

- `model.runPowerFlow`
- `job.status`
- `job.result`
- `PowerFlowResult.getBuses`
- `PowerFlowResult.getBranches`
- `PowerFlowResult.getMessagesByKey`
- `PowerFlowResult.powerFlowModify`

对应任务：

- 运行潮流计算
- 读取母线和支路结果
- 检查告警或错误消息
- 将潮流修正结果写回模型，进入下一轮试算

### 5. EMT 仿真与波形提取

在潮流校核通过后，研究人员通常会施加故障、扰动或参数变化，开展暂态稳定性研究。

核心 API：

- `model.runEMT`
- `job.status`
- `job.result`
- `EMTResult.getPlots`
- `EMTResult.getPlot`
- `EMTResult.getPlotChannelNames`
- `EMTResult.getPlotChannelData`
- `EMTResult.getMessagesByKey`

对应任务：

- 运行电磁暂态仿真
- 提取示波器或测量装置的波形
- 结合消息输出定位异常和数值问题

当前仓库在这一段的可信入口是：
- 已有一个准备好的研究模型，其中故障场景、量测信号和输出通道已经配置完成
- 然后用 `model.runEMT()` 与 `EMTResult` 完成普通云仿真和结果提取
- 并且已经在 `model/holdme/IEEE3` 上验证过：潮流回写后的模型可以直接承接后续 EMT
- 也已经验证过：可以脚本化修改已有量测信号名、输出通道名、输出分组成员，并为已有量测信号新增输出通道
- 还已经验证过：可在 `_newBus_3p` 母线上脚本化新增 `_NewVoltageMeter`、`_newChannel`、meter->bus `diagram-edge` 和输出分组引用，但当前只对已验证样本宣称成立

当前仓库尚未把下面两件事作为“已完成能力”对外宣称：

- 通用的脚本化故障元件创建
- 对任意 EMT 模型都通用的量测链/示波器输出自动配置

## 当前阶段的可信范围

当前仓库应优先做到下面三点：

1. 文档能解释研究流程中的 API 角色，而不是只列签名。
2. 示例能组成“获取模型 -> 改模 -> 潮流 -> EMT -> 结果分析”的闭环。
3. 测试能验证普通云仿真下可复现的行为，不使用 fake tests。

这意味着：

- `runPowerFlow` 和 `runEMT` 的普通云仿真链路要重点保证。
- `PowerFlowResult` 和 `EMTResult` 的离线结果提取接口要讲透。
- “潮流 -> 回写 -> EMT” 这类跨工作流串联场景要优先用真实云端证据固化。
- 文档中出现的默认 RID、返回结构、参数形态必须可验证。

## 延后处理的 API

以下 API 当前可以保留文档，但不作为近期端到端验证重点：

- `EMTResult.next`
- `EMTResult.goto`
- `EMTResult.send`
- `EMTResult.writeShm`
- `EMTResult.control`
- `EMTResult.monitor`
- `EMTResult.stopSimulation`
- `EMTResult.saveSnapshot`
- `EMTResult.loadSnapshot`

原因：

- 这些接口通常依赖实时仿真环境、流式交互条件或专门设备。
- 当前仓库的首要任务是服务普通离线研究工作流。

## 后续文档与样例优先级

建议后续工作按以下顺序推进：

1. 建模与算例修改文档
2. 潮流计算与结果回写文档
3. EMT 仿真与波形提取文档
4. 研究工作流串联示例
5. 仅在具备实际环境时再扩展实时控制与扩展模块

## 使用建议

阅读顺序建议如下：

1. 本文档
2. `docs/api-reference/model-api.md`
3. `docs/api-reference/powerflow-result-api.md`
4. `docs/api-reference/emtresult-api.md`
5. `examples/basic/component_example.py`
6. `examples/simulation/run_powerflow.py`
7. `examples/simulation/run_emt_simulation.py`
8. 若需要在 `_newBus_3p` 母线上补挂电压量测链，再阅读 `docs/guides/emt-voltage-meter-chain-guide.md`
