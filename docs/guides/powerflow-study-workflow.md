# 潮流研究工作流指南

本指南面向普通离线研究场景，描述如何使用 CloudPSS SDK 完成一轮潮流试算闭环：

1. 获取或加载模型
2. 检查 revision 级潮流拓扑
3. 运行潮流计算
4. 读取节点、支路和消息结果
5. 将潮流修正结果写回模型
6. 继续修改参数或拓扑并再次试算

## 适用场景

这条工作流适用于以下常见任务：

- 校核已有算例是否可算
- 为 EMT 仿真准备动态初值
- 反复调整参数、负荷、发电机或网络结构
- 分析薄弱节点、重载支路和运行边界

## 核心 API

### 模型获取与保存

- `Model.fetch`
- `Model.fetchMany`
- `Model.load`
- `Model.dump`
- `Model.save`

### 模型检查与修改

- `model.getAllComponents`
- `model.getComponentByKey`
- `model.getComponentsByRid`
- `model.addComponent`
- `model.updateComponent`
- `model.removeComponent`
- `model.fetchTopology(implementType='powerFlow')`

### 潮流运行与结果处理

- `model.runPowerFlow`
- `job.status`
- `job.result`
- `PowerFlowResult.getBuses`
- `PowerFlowResult.getBranches`
- `PowerFlowResult.getMessagesByKey`
- `PowerFlowResult.powerFlowModify`

## 推荐步骤

### 1. 获取研究模型

优先从已有模板或成熟算例出发：

```python
import os

from cloudpss import Model

model = Model.fetch(os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39"))
```

如果是离线迭代，也可以从本地恢复：

```python
model = Model.load("study-case.yaml")
```

当前仓库也已经验证：本地 YAML 工作副本可以直接继续运行潮流试算，而不是必须先手工另存回云端再运行。

### 2. 检查潮流拓扑

在改模后，可以先确认 `powerFlow` 视角下的 revision 拓扑可以正常展开：

```python
topology = model.fetchTopology(implementType="powerFlow")
topology_data = topology.toJSON()

print(len(topology_data["components"]))
print(topology_data["mappings"].keys())
```

这一步适合用于：

- 观察模型展开后的组件规模
- 作为正式潮流计算前的快速结构检查

但当前仓库已经在真实云端上确认：

- 对 fetched 工作副本，`fetchTopology(implementType="powerFlow")` 仍跟随远端 saved revision
- 它不会直接反映尚未保存的本地 add/update/remove
- 所以它不能单独作为“本地改模已进入潮流求解器”的证据

如果你刚做了参数或拓扑改动，真正的验收动作仍应是后面的 `runPowerFlow()`。

如果这一步失败，不建议继续强行运行潮流；应先回到建模阶段修正拓扑、参数方案或元件连接，再重新试算。

### 3. 运行潮流计算

```python
job = model.runPowerFlow()

while job.status() == 0:
    import time
    time.sleep(2)

if job.status() != 1:
    raise RuntimeError("潮流计算未成功完成")
```

### 4. 读取潮流结果

`job.result` 返回 `PowerFlowResult`，常用入口有三类：

#### 节点结果

```python
result = job.result
buses = result.getBuses()
```

适合查看：

- 电压幅值
- 相角
- 节点注入功率

#### 支路结果

```python
branches = result.getBranches()
```

适合查看：

- 支路潮流方向
- 有功/无功传输
- 线路负载和瓶颈

#### 原始消息

```python
bus_messages = result.getMessagesByKey("buses-table")
branch_messages = result.getMessagesByKey("branches-table")
```

当需要排查数据来源、保留原始表结构、或查阅附加消息时，优先用 `getMessagesByKey()`。

### 5. 将潮流修正结果写回模型

潮流结果通常可以作为后续研究的起点，例如将稳态修正后的状态写回模型：

```python
model_data = model.toJSON()
result.powerFlowModify(model_data)  # 原地修改 model_data，返回值为 None

from cloudpss import Model
modified_model = Model(model_data)
```

这里有两个要点：

- `powerFlowModify()` 需要一个可变的模型字典，实践中应传 `model.toJSON()` 的结果
- 如果结果消息里不存在 `power-flow-modify`，SDK 会抛异常；这时应先把结果当作“只读分析结果”，检查原始消息和算例设置

更稳妥的主线做法是先保存为本地研究分支：

```python
from cloudpss import Model

Model.dump(modified_model, "study-case-after-powerflow.yaml", compress=None)
```

随后可以直接把这个本地副本作为下一轮潮流或 EMT 的输入：

```python
next_model = Model.load("study-case-after-powerflow.yaml")
next_job = next_model.runPowerFlow()
```

只有在确认拥有写权限、并且确实要在云端保留一个新的研究分支时，再显式另存：

```python
modified_model.save("study-case-after-powerflow")
```

### 6. 进入下一轮试算

典型循环如下：

1. 修改负荷、发电机、线路或补偿装置参数
2. 重新运行潮流
3. 对比关键节点和支路结果
4. 必要时把修正结果再次写回模型

## 典型研究案例：IEEE39 负荷扰动再平衡

对系统研究来说，只证明 `runPowerFlow()` 能成功还不够，更重要的是参数扰动后结果是否符合工程直觉。

当前仓库已经用 live 集成测试固化了一个可复验案例：

1. 以 `model/holdme/IEEE39` 为基线运行潮流
2. 在本地工作副本上找到 `load-39`
3. 将其有功/无功负荷从 `1104/250` 提高到 `1400/350`
4. 重新运行潮流
5. 对比同一母线的 `P_load/Q_load` 与平衡机组 `P_gen/Q_gen`

当前已验证的结果是：

- 该母线的 `P_load` 增加 `296 MW`
- 该母线的 `Q_load` 增加 `100 MVar`
- 同母线平衡机组的 `P_gen/Q_gen` 也同步增加相同量级，用来维持系统平衡

这个案例的意义在于：

- 它体现了“负荷增长 -> 平衡出力抬升”的研究逻辑
- 它证明 `model.updateComponent()` 的改模会真实进入后续 `runPowerFlow()` 求解链
- 它比单纯检查表格非空更接近真实系统研究

## 典型研究案例：潮流回写后二次试算一致性

对离线研究来说，`powerFlowModify()` 的价值不只是“能写进去”，而是写回后的模型能否继续作为下一轮稳定研究起点。

当前仓库已经用 live 集成测试固化了一个二次试算案例：

1. 先在 `model/holdme/IEEE39` 上运行一次潮流
2. 将结果通过 `powerFlowModify()` 写回模型字典
3. 用写回后的模型重建新的本地模型对象
4. 在这个新模型上再次运行潮流
5. 对比关键母线的电压和机组出力

当前已验证的结果是：

- 关键母线电压幅值保持一致
- 相角只有极小数值误差
- 平衡机组和典型发电机的有功/无功出力只出现很小的数值级差异

这个案例的意义在于：

- 它证明 `powerFlowModify()` 可以服务研究迭代，而不是一次性结果浏览
- 它把“潮流回写”从语义说明推进成了可复验的工作流能力

## 典型研究案例：IEEE39 线路电抗扰动与潮流再分布

对网架薄弱环节研究来说，除了改负荷，还要关心网络参数变化是否会真实改变潮流分布。

当前仓库已经用 live 集成测试固化了一个线路参数敏感性案例：

1. 以 `model/holdme/IEEE39` 为基线运行潮流
2. 选取线路 `canvas_0_126`，也就是 `line-26-28`
3. 将该线路的正序电抗 `X1pu` 从 `0.0474` 提高到 `0.0600`
4. 重新运行潮流
5. 对比该支路潮流以及相邻母线的电压/相角结果

当前已验证的结果是：

- 该支路双向有功传输幅值都明显下降，变化量约为 `13 MW`
- 线路一端母线电压幅值出现可观测下降
- 线路另一端母线相角出现约 `0.58 deg` 的明显偏移

这个案例的意义在于：

- 它体现了“网络参数变化 -> 潮流重分布”的研究逻辑
- 它证明线路参数改动会真实进入 `runPowerFlow()` 求解链
- 它比只看任务成功更接近实际的网架敏感性分析

## 典型研究案例：IEEE39 线路切除后的潮流改道

对工程研究来说，参数灵敏度只是第一步，更常见的动作是直接切除某条线路，看潮流如何在替代走廊上重分布。

当前仓库已经用 live 集成测试固化了一个受限但很实用的线路切除案例：

1. 以 `model/holdme/IEEE39` 为基线运行潮流
2. 在本地工作副本上移除 `line-26-28`，也就是 `canvas_0_126`
3. 重新运行潮流
4. 对比切除前后的三条相关走廊：
   - `line-26-27` (`canvas_0_123`)
   - `line-28-29` (`canvas_0_130`)
   - `line-26-29` (`canvas_0_134`)
5. 同时对比被切除支路两端母线的电压和相角

当前已验证的结果是：

- 被切除的 `line-26-28` 会从潮流支路结果表中消失
- `line-26-29` 的有功传输幅值显著上升，承担了主要改道任务
- `line-28-29` 的有功传输幅值显著下降，表明原有潮流分配关系已经改变
- 被切除支路一端母线电压明显下降，另一端母线相角出现超过 `5 deg` 的可观测偏移

这个案例的意义在于：

- 它体现了“线路切除 -> 替代走廊增载 -> 局部运行状态恶化”的研究逻辑
- 它证明 `removeComponent()` 的网络结构修改会真实进入 `runPowerFlow()` 求解链
- 它比单纯调参数更接近工程上的 N-1 / 断线类校核动作

补充说明：

- 当前仓库又额外验证了一个更贴近传统 N-1 习惯的停运表达方式：对 `TransmissionLine` 使用 `props.enabled=False`
- 在 `IEEE39 line-26-28` 这个已验证样本上，`props.enabled=False` 与 `removeComponent()` 的真实云端潮流结果一致
- 对 `IEEE39` 的变压器样本 `canvas_0_47`，`props.enabled=False` 与 `removeComponent()` 也得到完全一致的潮流结果
- 因此，当前可以把 `props.enabled=False` 视为 `IEEE39` 已验证支路样本上的“停运而不物理删除”的可靠写法

## 典型研究案例：IEEE39 机组电压设定值调整

工程人员做潮流研究时，另一个高频动作是调 PV 机组电压设定值，观察局部母线电压和无功支撑是否按预期变化。

当前仓库已经用 live 集成测试固化了一个简洁案例：

1. 以 `model/holdme/IEEE39` 为基线运行潮流
2. 在本地工作副本上找到 `Gen30`，也就是 `canvas_2_303`
3. 将它的潮流电压设定值 `pf_V` 从 `1.047` 提高到 `1.070`
4. 重新运行潮流
5. 对比机端母线、邻近母线和机组无功出力

当前已验证的结果是：

- `Gen30` 所在机端母线电压会基本跟随上调到 `1.070 pu`
- 该机组的无功出力显著增加，说明它真实承担了更多电压支撑任务
- 邻近母线电压也会同步上升，但幅度小于机端母线
- 该机组的有功出力基本保持不变，符合“调压主要影响无功支撑”的工程直觉

这个案例的意义在于：

- 它体现了“电压设定值调整 -> 局部电压抬升 -> 无功支撑重分配”的研究逻辑
- 它证明发电机 `pf_V` 修改会真实进入 `runPowerFlow()` 求解链
- 它为后续电压控制、无功优化和薄弱节点支撑研究提供了一个很好的最小模板

## 典型研究案例：IEEE39 机组有功再调度与功率转移

对工程研究来说，调压之外的另一类高频动作是调机组有功出力，看平衡机组和关键送电走廊如何重新分担功率转移。

当前仓库已经用 live 集成测试固化了一个很适合作为模板的再调度案例：

1. 以 `model/holdme/IEEE39` 为基线运行潮流
2. 在本地工作副本上找到 `Gen38`，也就是 `canvas_9_384`
3. 将它的潮流有功设定值 `pf_P` 从 `830` 提高到 `900`
4. 重新运行潮流
5. 对比 `Gen38`、平衡机组以及几条关键送电走廊的变化

当前已验证的结果是：

- `Gen38` 会真实增发到 `900 MW`
- 平衡机组出力会同步下降约 `68.8 MW`
- `Gen38` 的无功支撑会明显增加
- `newTransformer_3p2w-13`、`line-26-27`、`line-26-28`、`line-26-29`、`line-28-29` 等走廊的有功传输幅值都会明显抬升

这个案例的意义在于：

- 它体现了“机组再调度 -> 平衡机组回调 -> 关键断面功率转移重分布”的研究逻辑
- 它证明发电机 `pf_P` 修改会真实进入 `runPowerFlow()` 求解链
- 它比只盯着机端出力更贴近实际的断面转移和运行方式调整研究

## 典型研究案例：IEEE39 负荷中心转移

很多系统研究并不是简单“总负荷增加”，而是保持总量近似不变，只把负荷中心从一个区域移到另一个区域，然后观察远端负荷口袋和关键断面的承压变化。

当前仓库已经用 live 集成测试固化了一条可复验的负荷转移案例：

1. 以 `model/holdme/IEEE39` 为基线运行潮流
2. 在本地工作副本上把 `load-39` 从 `1104/250` 调到 `904/190`
3. 同时把 `load-21` 从 `274/115` 调到 `474/175`
4. 重新运行潮流
5. 对比平衡机组、`bus21/bus22/bus23` 和 `line-21-22/22-23/23-24` 走廊结果

当前已验证的结果是：

- 平衡机组有功出力只会因网损变化而小幅波动，幅度不到 `2 MW`
- `bus21` 电压会明显下探，当前样本中约下降 `0.0085 pu`
- `line-21-22` 的有功传输幅值会增加约 `34 MW`
- `line-22-23` 与 `line-23-24` 的有功传输幅值会同步回落约 `34 MW`

这个案例的意义在于：

- 它体现了“总负荷近似不变，但负荷中心转移”这类很常见的系统研究逻辑
- 它比单纯抬负荷更接近区域供电压力转移和断面承载能力分析
- 它证明负荷参数的成对联动修改会真实进入 `runPowerFlow()` 求解链

## 典型研究案例：IEEE39 无功压力与电压薄弱性

还有一类很常见的系统研究，不是看有功转移，而是给某个负荷口袋增加无功需求，观察局部电压是否明显变差，以及系统是靠哪些机组补上这部分无功支撑。

当前仓库已经用 live 集成测试固化了一条可复验的无功压力案例：

1. 以 `model/holdme/IEEE39` 为基线运行潮流
2. 在本地工作副本上找到 `load-21`
3. 只把它的无功需求从 `115` 提到 `215 MVar`
4. 重新运行潮流
5. 对比 `bus21/bus22/bus23/bus24`、平衡机组和主要无功支撑母线的结果

当前已验证的结果是：

- `bus21` 电压会明显下探，当前样本中约下降 `0.0134 pu`
- `bus22/bus23/bus24` 电压也会同步下降，但幅度更小
- 平衡机组无功出力会增加约 `4.8 MVar`
- 主要无功支撑会来自远端发电机群，当前样本里增幅最大的母线是 `canvas_0_152`
- 与负荷中心转移不同，这条路径对 `line-21-22/22-23/23-24` 的有功传输幅值只造成很小变化

这个案例的意义在于：

- 它把“无功压力导致的电压薄弱性”与“有功潮流重分布”清楚地区分开
- 它更贴近局部电压支撑能力、无功备用和薄弱区域识别这类研究动作
- 它证明仅修改负荷 `q` 也会真实进入 `runPowerFlow()` 求解链

## 典型研究案例：IEEE39 多工况批量试算与结果汇总

实际工程研究通常不会只跑一个扰动工况，而是会在同一基线模型上连续比较多种假设，最后把关键指标汇总成一张研究表。

当前仓库已经把这条工作流收敛成一个受限但可直接复用的批量案例：

1. 以 `model/holdme/IEEE39` 为同一基线
2. 依次运行以下工况：
   - `baseline`
   - `load_up`
   - `line_x_up`
   - `line_outage`
   - `gen30_v_up`
   - `gen38_p_up`
   - `load_shift_39_to_21`
   - `load21_q_up`
3. 每个工况都重新运行潮流
4. 统一提取同一组关键指标：
   - 平衡机组 `P_gen/Q_gen`
   - `Gen30` 机端母线电压和无功出力
   - `Gen38` 机组有功和无功出力
   - `bus21` 电压
   - `line-26-28`、`line-26-29`、`line-28-29`、`line-21-22`、`line-22-23`、`line-23-24` 六条走廊的有功传输幅值
5. 最后输出一张对比汇总表，而不是分别手工翻八次结果

当前已验证的结果方向包括：

- `load_up` 会抬升平衡机组出力
- `line_x_up` 会降低 `line-26-28` 的传输幅值
- `line_outage` 会让 `line-26-28` 从支路结果中消失，并把更多潮流推到 `line-26-29`
- `gen30_v_up` 会抬升 `Gen30` 机端母线电压和机组无功支撑
- `gen38_p_up` 会抬升 `Gen38` 出力，并降低平衡机组出力，同时推高关键走廊的送电幅值
- `load_shift_39_to_21` 会让 `bus21` 电压下探，并把更多功率推到 `line-21-22`，同时减轻 `line-22-23/23-24`
- `load21_q_up` 会进一步压低 `bus21` 电压，并抬升系统无功支撑，但关键有功走廊幅值只会小幅变化

这个案例的意义在于：

- 它更贴近日常的系统研究节奏，而不是单个 API 演示
- 它把“多工况比较”收敛成一份可复验、可自动生成的研究摘要
- 它为后续批量参数扫描、越限筛查和研究报告整理提供了主线模板

这里也要明确一个负结论：

- 当前对 `IEEE39` 变压器 `Tap` / `InitTap` 的普通潮流探针没有观察到任何可验证的结果变化
- 因此，仓库当前不会把“分接头调压”宣称成已经完成 live 验证的普通潮流主线能力

## 典型研究案例：IEEE39 受限 N-1 潮流筛查

如果研究目标已经从“分析单个工况”进入“快速扫一批支路停运工况”，更贴近工程做法的是把同一基线下的多条支路依次停运，并汇总每个工况对系统状态的影响。

当前仓库已经把这条路径收敛成一个受限版本：

1. 固定使用 `model/holdme/IEEE39` 作为已验证基线
2. 先运行一次基线潮流，只把支路结果表里真实在役的组件纳入候选集
3. 自动发现这些基线在役的 `TransmissionLine` 与 `_newTransformer_3p2w`
4. 对每条候选支路在本地工作副本上执行 `props.enabled=False`
5. 逐条运行潮流
6. 对每个停运工况统一汇总：
   - 目标支路是否从支路结果中消失
   - 相对基线新增的电压越限母线数
   - 最低母线电压及其对应母线
   - 缺失母线数与缺失母线 ID 预览
   - 最大母线电压偏移及其对应母线
   - 最大支路传输幅值偏移及其对应支路

当前已验证的结果是：

- `IEEE39` 基线潮流里的全部 `43` 条在役支路都可以通过 `props.enabled=False` 形成稳定的停运工况
- 这 `43` 条支路由 `32` 条线路和 `11` 台变压器组成
- 模型里还有一个 `TransmissionLine` 组件 `line-6-11`，但它本来就不在基线潮流支路表中，因此不会被纳入当前主线候选集
- 停运后目标支路都会从潮流支路结果表中消失
- 每个工况都会引起非平凡的母线电压变化和支路潮流再分布
- 按当前已验证的严重性排序，前几名包括：
  - `newTransformer_3p2w-13`
  - `line-21-22`
  - `line-15-16`
  - `line-2-3`
  - `newTransformer_3p2w-8`
  - `newTransformer_3p2w-19`

这里要明确一个边界：

- 当前 live 潮流结果表没有直接返回支路负载率或越限百分比列
- 因此当前仓库的严重性筛查采用的是**受限判据**：
  相对基线新增的电压越限母线数、最低电压、最大电压偏移、最大潮流偏移
- 某些变压器停运后，局部孤立母线会直接从停运工况的结果表中消失，因此当前脚本在计算 `max_vm_shift` 时只比较基线和停运结果里共同存在的母线
- 这足以支持当前主线里的工程筛查，但还不等价于完整的调度级 N-1 安全校核体系
- 这条“全网支路 N-1”结论当前只对 `IEEE39` 的基线在役支路范围完成了 live 验证；若换成其他模型，仍需单独验证

对应示例还补了两个更贴近工程整理的能力：

- 候选支路自动发现
  当前默认会使用基线潮流结果里自动发现的全部在役支路，包含线路和变压器
  若只想快速复核一小组已验证样例，可显式传 `--validated-subset`
  若只想聚焦线路，可显式传 `--lines-only`
- CSV 导出
  默认会把筛查摘要导出到 `powerflow-n1-screening-summary.csv`
  也可以显式传 `--csv=/path/to/result.csv`
- 工程 digest
  终端会先输出一段简短研究摘要，直接给出总榜首位、线路首位、变压器首位、最低电压工况、最大潮流改道工况和最大母线缺失工况
- 可选 DataFrame
  如果本地装有 `pandas`，可以调用脚本里的 `summary_rows_to_dataframe()` 把摘要行直接转成 DataFrame，用于后续报告或分析脚本

推荐用法：

```bash
python examples/analysis/powerflow_n1_screening_example.py
python examples/analysis/powerflow_n1_screening_example.py --limit=1 --csv=/tmp/n1.csv
python examples/analysis/powerflow_n1_screening_example.py --validated-subset
python examples/analysis/powerflow_n1_screening_example.py --lines-only --limit=10
```

这里同样要注意：

- 在 `IEEE39` 上，默认的全量支路筛查已经完成 live 主线验收
- 对其他模型来说，默认自动发现到的支路仍然只是扩展探索入口，不代表它们都已经完成主线验收

这个案例的意义在于：

- 它已经具备了 `N-1` 筛查的基本结构：枚举候选支路、逐条停运、逐条潮流计算、统一汇总指标
- 它比单个断线案例更贴近真实的运行校核和研究筛查动作
- 它现在还能把“最严重工况究竟是电压问题、潮流改道问题，还是伴随局部母线消失的问题”直接总结出来
- 它仍然保持当前仓库的边界克制：**这是受限子集上的 N-1 主线样例，不是“全网自动 N-1 平台”**

## 典型研究案例：IEEE39 检修方式安全校核

如果研究问题不是“直接扫全网 N-1”，而是“先进入一个计划检修方式，再看该方式下还剩哪些敏感支路”，当前仓库已经补了一条更贴近运行校核节奏的受限案例。

这条路径当前做法是：

1. 固定使用 `model/holdme/IEEE39` 作为已验证基线
2. 先对计划检修支路执行 `props.enabled=False`
3. 运行潮流，确认检修态结果仍可读
4. 把检修态作为新的比较基线
5. 再对检修态下剩余候选支路做受限 N-1 复核
6. 导出摘要 CSV 与结论文本

当前已验证的受限样例是：

- 计划停运 `line-26-28` (`canvas_0_126`)
- 计划停运变压器 `canvas_0_47`
- 再对检修态下剩余已验证子集继续复核
- 结果会形成一组非平凡的残余 N-1 排序，而不是“检修后所有后续工况都没有区别”

这里要明确边界：

- 当前只是一个 `IEEE39` 上的受限检修校核样例
- 计划停运仍然使用 `props.enabled=False` 这一条已验证表达方式
- 残余 N-1 的严重性解释仍沿用当前仓库的受限判据：
  新增电压越限、最低电压、最大电压偏移、最大潮流偏移
- 它不等价于完整的调度级检修校核平台，也不应直接外推到其他模型

推荐用法：

```bash
python examples/analysis/powerflow_maintenance_security_example.py
python examples/analysis/powerflow_maintenance_security_example.py --all-discovered
python examples/analysis/powerflow_maintenance_security_example.py --maintenance-branch=canvas_0_126 --csv=/tmp/maintenance.csv --conclusion-txt=/tmp/maintenance.txt
python examples/analysis/powerflow_maintenance_security_example.py --maintenance-branch=canvas_0_47 --lines-only --limit=3
```

## 结果解读建议

做潮流分析时，优先关注以下信息：

- 母线电压是否越限
- 平衡节点和 PV 节点是否异常
- 支路是否出现重载或潮流反转
- 原始消息中是否存在错误、告警或未收敛迹象

## 与 EMT 工作流的衔接

潮流计算通常不是终点，而是 EMT 研究的前置步骤。

推荐衔接方式：

1. 先完成潮流校核
2. 将潮流修正结果写回模型，并优先保存为本地研究分支
3. 在修正后模型上添加故障、扰动或参数变化
4. 运行 `model.runEMT()`
5. 用 `EMTResult` 提取波形

当前仓库已经在 `model/holdme/IEEE3` 上用 live 集成测试验证过一条最小跨工作流闭环：

- 先提高 7 号母线负荷并运行潮流
- 再用 `powerFlowModify()` 把新的稳态工作点写回模型
- 随后直接进入 EMT
- 最终在故障前时刻读到明显抬升的机端有功/无功功率通道

这说明当前主线里，“潮流回写”已经不是孤立功能，而是可以作为普通云 EMT 研究的前置步骤来使用。

## 对应示例与文档

- 示例：`examples/simulation/run_powerflow.py`
- 示例：`examples/analysis/powerflow_engineering_study_example.py`
- 示例：`examples/analysis/powerflow_batch_study_example.py`
- 示例：`examples/analysis/powerflow_n1_screening_example.py`
- 示例：`examples/analysis/powerflow_maintenance_security_example.py`
- API：`docs/api-reference/model-api.md`
- API：`docs/api-reference/powerflow-result-api.md`
- 主线说明：`docs/guides/research-workflow-core-apis.md`
