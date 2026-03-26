# EMT 研究工作流指南

本指南面向普通离线研究场景，描述如何使用 CloudPSS SDK 完成一轮 EMT 仿真闭环：

1. 基于已有算例或潮流校核后的模型准备研究场景
2. 运行 EMT 仿真
3. 等待任务完成并读取结果
4. 提取示波器或量测装置的波形
5. 读取原始消息辅助排错
6. 为后续稳定性分析导出数据

## 适用场景

这条工作流适用于以下常见任务：

- 在已有电网模型上施加故障或扰动
- 校核故障后系统暂态响应
- 提取关键节点、线路、机组的波形
- 为后续稳定性分析、控制策略评估或论文作图准备数据

## 前置建议

在正式开展 EMT 仿真前，建议先完成以下工作：

1. 模型结构已经稳定，主要拓扑问题已排除
2. 潮流计算已经通过，或已有可信初值
3. 量测装置、示波器或输出通道已经配置妥当

原因很简单：EMT 研究最常见的问题不是 `runEMT()` 调不起来，而是模型未准备好、输出通道不足，最终得不到有分析价值的波形。

## 当前可信边界

基于当前仓库已经核对过的 SDK 代码与官方文档，可以确认：

- SDK 的主入口仍然是 `Model` / `Component` 级改模能力，而不是某个专门的“故障场景 API”
- 离线 EMT 的量测与输出链条在产品文档中是明确存在的：量测信号 -> 输出通道 -> 计算方案中的示波器输出配置
- 仓库当前已经可信验证的是“在故障、量测和输出通道已经准备好的模型上，运行 EMT 并提取波形结果”

同时也要明确当前还**不能**宣称：

- 仓库已经沉淀出一条对任意模型都适用的“纯 SDK 脚本化故障事件搭建”通用配方
- 仓库已经沉淀出一条对任意模型都适用的“纯 SDK 脚本化示波器输出通道配置”通用配方

但这里有一个需要单独说明的例外：

- 对 `_newBus_3p` 母线补挂 `_NewVoltageMeter`、`_newChannel`、meter->bus `diagram-edge` 和 EMT 输出分组，当前仓库已经有受限、可复验的 live 配方
- 这条配方目前只对 `IEEE3 Bus7`、`IEEE3 Bus2` 和 `IEEE39 bus37` 这些已验证样本宣称成立
- 对应说明见 `docs/guides/emt-voltage-meter-chain-guide.md`

因此，本指南当前把“故障场景、量测装置、输出通道准备”视为 EMT 之前的研究分支准备工作；一旦这一步准备完成，`runEMT()`、`EMTResult` 和结果导出链路就是当前仓库的可信主线。

如果目标不是继续阅读长篇工作流，而是快速确认“当前 EMT 主线到底算不算通过验收”，应同时参考：

- `docs/guides/emt-mainline-acceptance-checklist.md`
- `docs/guides/mainline-evidence-register.md`
- `docs/guides/parameterized-study-matrix.md`

当前已核对过的可读样例里：

- `model/holdme/IEEE3` 更适合研究这条前置链，因为它同时包含三相故障电阻、母线电压量测和较小规模的输出通道配置
- `model/holdme/IEEE39` 也可读、也能跑通普通云仿真，但更偏向大系统结果读取，不适合作为第一眼理解元件关系的最小样例

当前仓库已经验证过一条最小闭环：

1. 用 `examples/basic/ieee3_emt_preparation_example.py` 获取并微调 `model/holdme/IEEE3`
2. 生成本地副本 `examples/basic/ieee3-emt-prepared.yaml`
3. 用 `examples/simulation/run_emt_simulation.py examples/basic/ieee3-emt-prepared.yaml` 直接加载本地副本
4. 由 `runEMT()` 把该本地 revision 提交到 CloudPSS 运行 EMT，并继续提取波形和原始 `plot-*` 消息

如果研究问题不是“直接运行已有准备副本”，而是“给某个 `_newBus_3p` 母线新增电压量测链”，应先参考：

- `docs/guides/emt-voltage-meter-chain-guide.md`
- `examples/basic/emt_voltage_meter_chain_example.py`

## 核心 API

### 模型准备

- `Model.fetch`
- `Model.load`
- `Model.dump`
- `Model.save`
- `model.getAllComponents`
- `model.updateComponent`
- `model.fetchTopology(implementType='emtp')`

### EMT 仿真

- `model.runEMT`
- `job.status`
- `job.result`

### 波形与消息读取

- `EMTResult.getPlots`
- `EMTResult.getPlot`
- `EMTResult.getPlotChannelNames`
- `EMTResult.getPlotChannelData`
- `EMTResult.getMessagesByKey`

## 推荐步骤

### 1. 获取研究模型

```python
import os

from cloudpss import Model

model = Model.fetch(os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39"))
```

如果是基于本地研究分支继续迭代：

```python
model = Model.load("study-case-after-powerflow.yaml")
```

对于当前仓库已验证过的最小 EMT 前置链，也可以直接加载 IEEE3 本地准备副本：

```python
model = Model.load("examples/basic/ieee3-emt-prepared.yaml")
```

### 2. 检查 EMT 拓扑

在改模后，建议先确认 `emtp` 视角下的 revision 拓扑可以正确展开：

```python
topology = model.fetchTopology(implementType="emtp")
topology_data = topology.toJSON()

print(len(topology_data["components"]))
print(topology_data["mappings"].keys())
```

这一步适合用于：

- 检查关键元件是否被正确展开
- 观察模型规模是否符合预期
- 在正式仿真前做结构级快速校核

但这里也要沿用同一条边界理解：

- 对 fetched 工作副本，`fetchTopology(implementType="emtp")` 更适合看成远端 saved revision 的展开结果
- 它不能单独证明尚未保存的本地改动已经进入 EMT 求解路径
- 若要验证这些改动是否真实生效，仍应以 `runEMT()` 的 live 结果为准

如果这一步失败，不建议继续强行运行 EMT；应先回到建模阶段确认故障场景、量测装置、示波器和参数方案是否准备妥当。

### 3. 运行 EMT 仿真

```python
job = model.runEMT()

while job.status() == 0:
    import time
    time.sleep(2)

if job.status() != 1:
    raise RuntimeError("EMT 仿真未成功完成")
```

### 4. 提取波形结果

`job.result` 返回 `EMTResult`，常用读取方式有三层：

#### 获取所有波形分组

```python
result = job.result
plots = list(result.getPlots())
```

这一步适合快速确认：

- 有多少个示波器或输出分组
- 当前算例是否真的产出了波形

如果 `plots` 为空，最常见原因不是结果接口失效，而是模型里没有配置好示波器、量测装置或输出通道。

#### 获取单个波形分组

```python
plot0 = result.getPlot(0)
channel_names = result.getPlotChannelNames(0)
```

这一步适合确定：

- 某个分组下有哪些通道
- 哪些通道是研究要重点关注的量

#### 获取指定通道数据

```python
data = result.getPlotChannelData(0, channel_names[0])

time_array = data["x"]
value_array = data["y"]
```

这一步适合直接进入后处理：

- 稳定性分析
- 波形导出
- 绘图或指标统计

注意：当前 SDK 在 `channelName` 不存在时不会抛错，而是会回落到最后一条 trace。更稳妥的做法是先用 `getPlotChannelNames()` 拿到合法名称，再传给 `getPlotChannelData()`。

### 5. 读取原始消息辅助排错

除了高层波形接口，`getMessagesByKey()` 还能帮助你保留原始消息结构。

普通云 EMT 仿真中，当前已验证常见消息形态包括：

- `type='plot'` 的波形消息
- `type='progress'` 的进度消息
- `type='log'` 的日志消息
- `type='terminate'` 的结束消息

其中最常用的是按 `plot-*` key 获取原始波形消息：

```python
raw_plot0 = result.getMessagesByKey("plot-0")
print(len(raw_plot0))
```

这一步适合用于：

- 保留原始消息分段形式
- 排查高层聚合结果与底层消息是否一致
- 分析单个输出分组的原始来源

### 6. 导出到后续分析流程

```python
plots = list(result.getPlots())
names = result.getPlotChannelNames(0)
data = result.getPlotChannelData(0, names[0])

with open("emt-output.csv", "w", encoding="utf-8") as f:
    f.write("time,value\n")
    for x, y in zip(data["x"], data["y"]):
        f.write(f"{x},{y}\n")
```

常见后续用途：

- 稳定性判断
- 绘制论文图表
- 计算超调、衰减、恢复时间等指标

## 典型研究案例：IEEE3 故障清除时间敏感性

在 EMT 研究里，光证明“有波形”仍然不够，更关键的是参数变化后波形是否出现符合研究预期的差异。

当前仓库已经用 live 集成测试固化了一个最小敏感性案例：

1. 基于 `model/holdme/IEEE3` 的本地工作副本准备故障场景
2. 将故障起始时间固定为 `fs=2.5`
3. 分别运行两组工况：
   - 基线工况：`fe=2.7`
   - 延长故障工况：`fe=2.9`
4. 保持输出通道采样频率一致为 `2000`
5. 读取第一组电压波形通道，在不同时间点对比数值

当前已验证的结果是：

- 在 `t=2.6s`，两种工况的波形几乎一致，因为故障都尚未切除
- 在 `t=2.95s`，延长故障工况的电压波形明显低于基线工况

这个案例的意义在于：

- 它体现了“故障持续时间变化 -> 后故障响应变化”的研究逻辑
- 它证明本地工作副本上的故障参数修改会真实进入 `runEMT()` 求解链
- 它为后续稳定边界、故障清除时间灵敏度研究提供了最小可信模板

## 典型研究案例：输出采样频率与波形分辨率

对 EMT 结果分析来说，输出通道配置不只是“有没有波形”，还决定了后处理时的时间分辨率。

当前仓库已经用 live 集成测试固化了一个最小采样分辨率案例：

1. 基于 `model/holdme/IEEE3` 的本地工作副本准备同一故障场景
2. 保持故障参数一致
3. 分别把输出采样频率设为 `1000` 和 `2000`
4. 运行两次普通云 EMT
5. 对比同一波形通道的点数与时间步长

当前已验证的结果是：

- `1000` 采样频率对应 `10001` 个点
- `2000` 采样频率对应 `20001` 个点
- 更高采样频率下，时间步长按预期减半，而总仿真窗口保持不变

这个案例的意义在于：

- 它证明输出通道采样配置会真实影响 `EMTResult` 的波形分辨率
- 它为后续“速度与精度权衡”“导出波形用于稳定性分析”等研究问题提供了最小可信模板

## 典型研究案例：IEEE3 故障参数 `chg` 灵敏度

在故障稳定性研究里，除了故障持续时间，还要验证故障元件参数本身是否真的进入求解链。

当前仓库已经用 live 集成测试固化了一个额外故障参数案例：

1. 基于 `model/holdme/IEEE3` 的本地工作副本准备同一故障场景
2. 将故障起止时间固定为 `fs=2.5`、`fe=2.7`
3. 保持输出通道采样频率为 `2000`
4. 仅修改 `_newFaultResistor_3p` 元件的 `chg` 参数：
   - 工况 A：`chg=1e-6`
   - 工况 B：`chg=1e4`
5. 读取同一电压波形通道，在故障前、故障中和故障后对比数值

当前已验证的结果是：

- 在 `t=2.45s` 的故障前时刻，两种工况波形一致
- 在 `t=2.6s` 的故障期间，较大 `chg` 工况的电压明显更高
- 在 `t=2.95s` 的故障后阶段，较大 `chg` 工况仍保持更高电压

这个案例的意义在于：

- 它证明故障元件参数 `chg` 会真实进入 `runEMT()` 求解链
- 它把 EMT 研究从“只比较故障切除时间”推进到“比较故障参数本身”
- 它为后续围绕故障严重度、稳定边界和参数灵敏度的研究提供了第二个可信模板

## 典型研究案例：故障严重度与切除时间对比

对工程研究来说，更常见的提问不是“某一个参数是否生效”，而是：

- 若故障本身更轻，故障中电压跌落会改善多少
- 若故障清除更晚，故障后恢复会恶化多少
- 这两类影响能否在同一套量测口径下被稳定区分

当前仓库已经把这个问题收敛成一个 live 可复验的三工况案例，配套示例为：

```bash
python examples/analysis/emt_fault_study_example.py
python examples/analysis/emt_fault_study_example.py --csv=emt-fault-study-summary.csv
python examples/analysis/emt_fault_study_example.py --waveform-csv=emt-fault-study-waveforms.csv
python examples/analysis/emt_fault_study_example.py --waveform-csv=emt-fault-study-waveforms.csv --waveform-window=2.4,3.0
python examples/analysis/emt_fault_study_example.py --conclusion-txt=emt-fault-study-conclusions.txt
```

研究设置如下：

1. 基于 `model/holdme/IEEE3` 的本地工作副本准备同一故障研究模型
2. 固定输出口径为 `plot-2 / vac:0`
3. 用相同的一组 RMS 观察窗口提取指标：
   - 故障前：`2.42s - 2.44s`
   - 故障中：`2.56s - 2.58s`
   - 故障后：`2.92s - 2.94s`
   - 晚恢复：`2.96s - 2.98s`
4. 比较三组工况：
   - `baseline`: `fe=2.7`, `chg=0.01`
   - `delayed_clearing`: `fe=2.9`, `chg=0.01`
   - `mild_fault`: `fe=2.7`, `chg=1e4`
5. 将结果整理成统一摘要字段：
   - 原始 RMS：`prefault_rms / fault_rms / postfault_rms / late_recovery_rms`
   - 相对故障前的缺口：`fault_drop_vs_prefault / postfault_gap_vs_prefault / late_recovery_gap_vs_prefault`
   - 相对基线的变化：`delta_fault_rms_vs_baseline / delta_postfault_rms_vs_baseline`

当前已验证的结果是：

- `baseline` 与 `delayed_clearing` 的故障前 RMS 一致，说明起始工作点相同
- `baseline` 与 `delayed_clearing` 在故障中窗口的 RMS 近似一致，说明比较重点不是故障深度，而是切除后恢复
- `delayed_clearing` 在故障后和晚恢复窗口上的 RMS 明显低于 `baseline`
- `mild_fault` 在故障中窗口上的 RMS 明显高于 `baseline`
- `mild_fault` 的故障后 RMS 也明显高于 `baseline`，并更接近故障前水平

最近一次 live probe 的代表性量级为：

- `baseline`: `fault_rms ≈ 62.93 V`, `postfault_rms ≈ 292.65 V`
- `delayed_clearing`: `fault_rms ≈ 62.93 V`, `postfault_rms ≈ 280.14 V`
- `mild_fault`: `fault_rms ≈ 294.72 V`, `postfault_rms ≈ 301.93 V`

这个案例的意义在于：

- 它把“故障参数生效”推进成“同一量测口径下的研究型对比摘要”
- 它能帮助工程人员区分“故障更重”与“故障更久”两种机制对波形的不同影响
- 它给后续稳定边界、故障穿越和保护整定类研究提供了一份更接近实际分析习惯的 EMT 模板
- 它还能直接导出 CSV 摘要，便于后续稳定性分析、报告整理或外部脚本继续加工
- 它还能把三工况波形按统一时间轴导出成对比 CSV，便于直接画图或做窗口后处理
- 若只关注研究窗口，还可以用 `--waveform-window=start,end` 导出裁剪后的对比波形 CSV，减少全时域数据量
- 摘要 CSV 和波形 CSV 默认共用同一研究前缀；若只显式指定其中一个路径，另一个也会按同一前缀自动派生
- 示例还会根据固定判据自动生成一份“研究结论”文本，而不是只停在数据导出

判读时可以优先看两类字段：

- `fault_drop_vs_prefault`
  - 用来看故障期间电压跌落有多深
  - `mild_fault` 应显著小于 `baseline`
- `postfault_gap_vs_prefault` / `late_recovery_gap_vs_prefault`
  - 用来看故障切除后离故障前工作点还差多少
  - `delayed_clearing` 应明显大于 `baseline`

需要强调的边界是：

- `--waveform-window` 只是对已经 live 验证过的同一批波形做时间窗裁剪导出
- 它本身不构成新的 EMT 物理结论，也不额外扩大模型适用范围
- 自动生成的研究结论同样只对当前三工况、当前量测链和当前判据成立

边界也要写清楚：

- 这个案例当前只对 `model/holdme/IEEE3` 和 `plot-2 / vac:0` 这条已验证输出链宣称成立
- 当前仓库并不因此宣称任意 EMT 模型都已有同样稳定的故障研究模板
- 若换模型、换量测链或换时间窗口，仍应重新做 live 复验

如果要把这些离散案例按“可继续扩哪些参数维度”重新组织，应参考：

- `docs/guides/parameterized-study-matrix.md`

## 典型研究案例：故障严重度扫描

如果目标不是只比较少数离散工况，而是做一轮小型 EMT 扰动扫描，当前仓库也已经有一条 live 可复验路径：

```bash
python examples/analysis/emt_fault_severity_scan_example.py
python examples/analysis/emt_fault_severity_scan_example.py --csv=emt-fault-severity-scan.csv
python examples/analysis/emt_fault_severity_scan_example.py --conclusion-txt=emt-fault-severity-scan.txt
```

这条扫描当前固定在一条已验证的最小研究链上：

1. 模型固定为 `model/holdme/IEEE3`
2. 故障清除时间固定为 `fe=2.7`
3. 量测链固定为 `plot-2 / vac:0`
4. 仅扫描 `_newFaultResistor_3p.chg` 的三个代表点：
   - `1e-2`
   - `1e2`
   - `1e4`

当前 live 探针观察到的代表性结果为：

- `chg=1e-2`
  - `fault_drop_vs_prefault ≈ 239.535 V`
  - `postfault_gap_vs_prefault ≈ 9.778 V`
- `chg=1e2`
  - `fault_drop_vs_prefault ≈ 210.131 V`
  - `postfault_gap_vs_prefault ≈ 9.451 V`
- `chg=1e4`
  - `fault_drop_vs_prefault ≈ 7.750 V`
  - `postfault_gap_vs_prefault ≈ 0.537 V`

这个案例的意义在于：

- 它展示了 CloudPSS 不只是“改单点参数再跑一次 EMT”，而是可以把一组扰动参数组织成一轮研究扫描
- 它把 EMT 结果从单条波形读取推进到“严重度排序”和“研究结论生成”
- 它更接近工程上做灵敏度分析、保护定值边界试探和暂态安全裕度摸底时的工作方式

边界同样要写清楚：

- 当前只对 `IEEE3 + fe=2.7 + plot-2/vac:0 + chg in {1e-2, 1e2, 1e4}` 这条扫描链宣称成立
- 它不意味着当前仓库已经提供任意扰动参数、任意模型、任意量测链的通用 EMT 扫描框架
- 如果未来要扩大扫描维度，仍应逐项做 live 复验

## 典型研究案例：故障清除时间扫描

除故障严重度外，清除时间本身也是 EMT 稳定性研究中的核心扫描维度。

当前仓库已经把这类问题收敛成一条 live 可复验的扫描路径：

```bash
python examples/analysis/emt_fault_clearing_scan_example.py
python examples/analysis/emt_fault_clearing_scan_example.py --csv=emt-fault-clearing-scan.csv
python examples/analysis/emt_fault_clearing_scan_example.py --conclusion-txt=emt-fault-clearing-scan.txt
```

这里的研究问题不是“清除后固定延时多久恢复到什么水平”，而是：

- 当工程人员在固定审视时刻回看仿真结果时
- 随着 `fe` 逐步延后
- 系统在这些固定时刻的恢复缺口是否会系统性恶化

当前扫描设置为：

1. 模型固定为 `model/holdme/IEEE3`
2. 故障严重度固定为 `chg=0.01`
3. 量测链固定为 `plot-2 / vac:0`
4. 扫描 `fe=2.70 / 2.75 / 2.80 / 2.85 / 2.90`
5. 用两个固定评估窗口构造恢复缺口：
   - `gap_295`: `2.94s - 2.96s` 的 RMS 相对故障前缺口
   - `gap_300`: `2.99s - 3.01s` 的 RMS 相对故障前缺口

最近一次 live probe 的代表性结果为：

- `gap_295`: `8.418 -> 12.770 -> 17.766 -> 22.674 -> 25.669 V`
- `gap_300`: `5.754 -> 8.890 -> 12.987 -> 17.833 -> 22.607 V`

这个案例的意义在于：

- 它更贴近工程上“在某个观察时刻检查系统是否恢复充分”的工作方式
- 它展示了 CloudPSS 可以把 EMT 从单点工况分析推进到清除时间扫描
- 它为后续保护时限试探、故障切除边界和暂态安全裕度研究提供了可信模板

边界同样明确：

- 这条扫描结论只对当前 `IEEE3 + chg=0.01 + plot-2/vac:0 + fe=2.70..2.90` 的设置宣称成立
- 它依赖的是固定绝对评估时刻，不应误读成“对齐清除后同一延时窗口”的普遍结论
- 若后续要换评估时刻、量测链或模型，仍需重新做 live 复验

## 典型研究案例：量测可观测性工作流

EMT 研究里，测点管理本身就是研究准备的一部分：

- 哪些已有测点可以直接用
- 哪些关键位置需要补挂新测点
- 哪些输出通道只是“占带宽、占注意力”，应在正式研究前删掉

当前仓库已经把这三类动作收敛成一条 live 可复验工作流：

```bash
python examples/analysis/emt_measurement_workflow_example.py
python examples/analysis/emt_measurement_workflow_example.py --csv=emt-measurement-workflow.csv
python examples/analysis/emt_measurement_workflow_example.py --conclusion-txt=emt-measurement-workflow.txt
```

这条工作流当前固定为：

1. 基于 `model/holdme/IEEE3`
2. 继续使用已有的 `Bus7` 电压测点 `vac`
3. 脚本化新增 `Bus2` 电压测点 `bus2_added`
4. 把 PQ 输出组裁剪为仅保留 `#P*` 通道
5. 在最终输出集上直接读取 `Bus7`、`Bus2` 和 `#P1`

当前这条工作流已经验证的关键结论是：

- 新增 `Bus2` 测点后，其稳态 RMS 与母线额定值计算结果吻合
- 删掉 `#Q*` 输出后，PQ 组只保留 `#P2/#P1/#P3`
- 删减后的输出集仍可直接支撑故障前功率读数和母线电压分析

这个案例的意义在于：

- 它展示了 CloudPSS 不只是“会加一个量测元件”，而是能做完整的 EMT 可观测性整理
- 它更贴近日常研究准备：增测点、删冗余、保留关键输出
- 它能帮助后续研究把输出配置从“能出图”推进到“能支撑结论”
- 它还能把 `Bus7`、`Bus2` 与 `#P1` 组合成一条联合结论链，区分局部冲击、远端支撑和功率响应

边界同样要写清楚：

- 当前只对 `IEEE3` 上这条已验证链成立：已有 `vac`、新增 `Bus2` 电压链、PQ 组裁剪到 `#P*`
- 它不意味着当前仓库已经提供任意模型、任意母线类型、任意测点组合的通用 EMT 量测编排框架
- 如果未来要扩到更多母线或更复杂输出集，仍应逐项做 live 复验

## 典型研究案例：EMT N-1 安全筛查

如果目标已经从“比较几个故障参数”推进到“在同一固定故障下扫描多条单支路停运工况”，当前仓库现在还提供了一条更像工程筛查的 EMT 研究路径：

```bash
python examples/analysis/emt_n1_security_screening_example.py
python examples/analysis/emt_n1_security_screening_example.py --validated-subset
python examples/analysis/emt_n1_security_screening_example.py --csv=emt-n1-security-screening.csv
python examples/analysis/emt_n1_security_screening_example.py --conclusion-txt=emt-n1-security-screening.txt
```

这条路径当前固定做的事情是：

1. 以 `model/holdme/IEEE3` 上已经验证过的 EMT 故障配置为基线
2. 自动发现当前模型里的 `TransmissionLine` 与 `_newTransformer_3p2w`
3. 逐条执行 `props.enabled=False`，形成单支路/单变压器 N-1 停运工况
4. 在每个工况里保留现有 `Bus7` 电压测点 `vac`
5. 再脚本化补挂 `Bus2` 和 `Bus8` 电压测点
6. 同时读取 `#P1` 有功通道，作为机组支撑诊断信号
7. 把各工况的 `Bus7/Bus2/Bus8` 恢复缺口与 `#P1` 读数组织成排序、CSV 和结论文本

当前已经有 live 证据支撑的工程结论是：

- `Trans1` 停运是当前扫描里最不安全的工况：`Bus7/Bus8` 的最差恢复缺口会超过无停运基线，且 `#P1` 在故障前/中/后都塌到接近零
- 在线路子集里，`tline4` 的恢复压力明显重于 `tline6`
- `tline6` 是当前扫描里最轻的工况，`Bus7/Bus8` 的后故障缺口都比无停运基线小很多
- `Bus2` 的后故障缺口在当前扫描里始终很小，说明这次冲击并不是在所有监测母线上均匀放大

这条路径的意义在于：

- 它把 EMT 研究从“只改故障参数”推进到“固定故障下的 N-1 安全筛查”
- 它展示了 CloudPSS 可以把停运表达、多测点量测链和 EMT 结果判据收敛到同一条工程工作流里
- 它比单条故障比较更接近日常暂态安全摸底和薄弱环节定位的使用方式

当前边界也必须写清楚：

- 它只对 `model/holdme/IEEE3`、固定 `_newFaultResistor_3p` 故障配置、`Bus7/Bus2/Bus8` 三个监测母线以及 `#P1` 读数宣称成立
- 它不是“任意模型、任意支路、任意故障组合”的通用 EMT 安全校核平台
- 当前仓库的 live 集成测试已覆盖代表性子集 `Trans1 / tline4 / tline6`，也覆盖了把默认 9 个候选工况整理成全扫描 Markdown 报告的 wrapper 路径；若要直接复核筛查表级输出，仍可运行示例或参考历史探针记录

如果想把这条路径直接整理成一份更适合阅读和归档的专题交付物，当前还提供了一个默认聚焦代表性工况的报告入口：

```bash
python examples/analysis/emt_n1_security_report_example.py
python examples/analysis/emt_n1_security_report_example.py --report=emt-n1-security-report.md
python examples/analysis/emt_n1_security_report_example.py --all-discovered
```

它默认围绕三类已经最有代表性的工况组织报告：

1. `Trans1`：当前最重的变压器停运工况
2. `tline4`：当前最重的线路停运工况
3. `tline6`：当前最轻的停运工况

它的意义不在于引入新的 EMT 物理判据，而在于：

- 把已经有 live 证据的 EMT N-1 安全筛查结果整理成 Markdown 专题报告
- 让后续使用者先看到“最重/最轻/代表性线路”三类结论，再决定是否去跑全扫描
- 给更完整的暂态安全专题报告自动化提供一个可信起点

如果目标已经不是“看代表工况”，而是想把默认全扫描结果也整理成一份可交付文档，当前还提供了一个单独的入口：

```bash
python examples/analysis/emt_n1_full_report_example.py
python examples/analysis/emt_n1_full_report_example.py --report=emt-n1-full-report.md
python examples/analysis/emt_n1_full_report_example.py --lines-only
```

它和前面的代表性报告入口差别只有一个：默认就跑完整的已发现 `IEEE3` N-1 候选集，并把结果按下面三个层次组织出来：

1. 严重性分布
2. 榜首/线路首位/变压器首位/最轻工况
3. 完整排序表

这条路径的意义在于：

- 它把 full scan 的输出从“只有 CSV 和终端表”推进到一份更适合归档的 Markdown 报告
- 它让后续使用者先看到严重性分布，再决定要不要深入具体工况
- 它仍然不引入新的物理判据，只是整理已经 live 验证过的 EMT N-1 结果

## 研究报告级输出

如果目标不是运行某一个 EMT 研究案例，而是想把几条已验证的 EMT 研究路径组织成一份交付物，当前仓库还提供了一个汇总入口：

```bash
python examples/analysis/emt_research_report_example.py
python examples/analysis/emt_research_report_example.py --report=emt-research-report.md
```

这份报告当前会汇总四条已经有 live 证据的 EMT 研究路径：

1. 工况对比研究
2. 故障清除时间扫描
3. 故障严重度扫描
4. 量测可观测性工作流

它的意义不在于新增新的 EMT 物理结论，而在于：

- 把已有可信案例组合成一份更像研究交付物的 Markdown 报告
- 让使用者直接看到 CloudPSS 在 EMT 研究中的能力带宽
- 给后续扩展到更完整的研究报告自动化打一个可信起点

## 典型研究案例：潮流回写后直接进入 EMT

在日常离线研究里，潮流计算往往不是终点，而是给后续暂态仿真准备稳态起点。

当前仓库已经用 live 集成测试固化了一条最小跨工作流案例：

1. 基于 `model/holdme/IEEE3` 建立本地工作副本
2. 将 7 号母线负荷从 `125/50` 提高到 `180/80`
3. 先运行潮流，并确认该母线电压明显下降
4. 用 `powerFlowModify()` 把潮流修正结果写回模型
5. 在写回后的模型上设置故障时间和输出采样频率
6. 直接运行 EMT，并读取“三台电机端口功率 PQ”通道

当前已验证的结果是：

- 潮流阶段，7 号母线电压幅值下降超过 `0.03 pu`
- 进入 EMT 后，在 `t=2.45s` 的故障前时刻，`#P1:0` 通道相对基线提高超过 `50 MW`
- 同一时刻，`#Q1:0` 通道相对基线提高超过 `20 MVar`

这个案例的意义在于：

- 它证明 `runPowerFlow()` -> `powerFlowModify()` -> `runEMT()` 这条主线在真实云端上可闭环
- 它证明潮流回写后的模型不只是“还能跑 EMT”，而是会把新的稳态工作点真实带进 EMT 初始状态
- 它比单独验证潮流或单独验证 EMT 更接近日常研究中的串联用法

## 典型研究案例：脚本化整理量测与输出通道

在实际研究里，EMT 前置准备不只是“有一个通道能出图”，还包括：

- 给量测信号换成研究可读的名字
- 只保留后处理真正需要的输出通道

当前仓库已经在 `model/holdme/IEEE3` 上用 live 集成测试验证了四类最小改配动作：

1. 量测信号与输出通道同步重命名
   - 将电压量测信号从 `#vac` 改为 `#bus7_voltage`
   - 将对应 `_newChannel` 的 `Name` 从 `vac` 改为 `bus7_voltage`
   - 同时把通道输入引脚改到 `#bus7_voltage`
   - 运行 EMT 后，`plot-2` 的通道名从 `vac:0/1/2` 变为 `bus7_voltage:0/1/2`
   - 同一波形在故障前和故障后的数值保持不变，说明只是改了链路命名，没有改坏信号本身

2. 输出分组裁剪
   - 在“三台电机端口功率 PQ”分组里，只保留名称以 `#P` 开头的通道
   - 运行 EMT 后，`plot-1` 的通道从 `#P2/#Q2/#P1/#Q1/#P3/#Q3` 收缩为 `#P2/#P1/#P3`
   - 保留下来的 `#P1:0` 波形在故障前和故障后的数值与基线一致，说明变化只发生在输出选择层

3. 新增输出通道
   - 保留已有 7 号母线电压量测信号 `#vac`
   - 通过 `addComponent()` 新增一个 `_newChannel`，把它也挂到 `#vac`
   - 将这个新通道追加到原有电压输出分组
   - 运行 EMT 后，`plot-2` 从 `vac:0/1/2` 扩展为 `vac:0/1/2 + vac_copy:0/1/2`
   - 新增 `vac_copy:*` 波形在故障前和故障后的数值与原始 `vac:*` 一致，说明新增通道真实进入了输出链

4. 新增量测元件并接入输出链
   - 通过 `addComponent()` 新增一个 `_NewVoltageMeter`，把量测信号设为 `#vac_added`
   - 再通过 `addComponent()` 新增一个 `_newChannel`，把它挂到 `#vac_added`
   - 仅新增元件本身还不够；还需要向 `revision.getImplements().getDiagram().cells` 手工注入一条 `diagram-edge`
   - 这条 `diagram-edge` 需要把新电压表的 `source` 连接到新表的 `0` 号端口，并把 `target` 连接到 `Bus7`
   - 将新通道追加到原有电压输出分组后，运行 EMT，`plot-2` 会从 `vac:0/1/2` 扩展为 `vac:0/1/2 + vac_added:0/1/2`
   - 新增 `vac_added:*` 波形在故障前和故障后的数值与原始 `vac:*` 一致，说明“新增表计 -> 新增通道 -> 示波器分组”这条链已经真实跑通
   - 这条路径目前已经额外做了两步可迁移性验证：
     - 在同一 `IEEE3` 模型里把目标母线从 `Bus7` 换到 `Bus2`，新通道 `bus2_added:*` 仍可稳定返回
     - 在没有现成电压表模板的 `IEEE39` 上，直接用 generic `diagram-edge` scaffold 接到 `bus37`，新通道 `bus37_added:*` 也可稳定返回

这个案例的意义在于：

- 它证明当前仓库已经能脚本化修改“已有量测信号 -> 输出通道 -> 输出分组”这条链
- 它覆盖了四个高频准备动作：研究命名整理、输出裁剪、基于已有信号新增输出通道、基于已有接线模板新增电压量测元件
- 它也明确暴露了 SDK 边界：当前公开 API 没有高层 `addEdge()`，新增量测元件之所以能跑通，是因为我们按真实模板克隆并注入了底层 `diagram-edge`
- 它还给出了一条更强的正确性判据：新增电压表通道的稳态 RMS 应满足 `V_rms ≈ V_pu * VBase / sqrt(3)`，这一点已在 `IEEE3 Bus2` 和 `IEEE39 bus37` 上与真实云端结果吻合

需要特别记录的调试结论是：

- 先前“只新增 `_NewVoltageMeter` 和 `_newChannel`”的最小克隆路径会在真实云端触发 `KLU Error: singular`
- 根因不是量测信号名或输出分组本身，而是**漏掉了电压表到母线的 `diagram-edge` 连接**
- 一旦把这条 meter->bus 的 `diagram-edge` 按现有工作模板补齐，`IEEE3` 上就能稳定返回新的 `vac_added:*` 波形
- 因而当前可谨慎宣称的能力边界是：**这条配方已经表现出跨母线、跨模型的可迁移性，但仍依赖底层 edge 注入，不应误写成 SDK 已提供公开的连线 API，更不能在没有进一步样本前直接宣称“任意模型通用”**

如果只是想基于当前仓库快速准备一个本地研究分支，可直接使用示例脚本：

```bash
python examples/basic/emt_voltage_meter_chain_example.py
```

这个脚本当前只支持 `_newBus_3p` 母线，并会明确区分两条路径：

- 模型里已有可工作的电压表时，优先克隆现成 meter->bus `diagram-edge`
- 模型里没有现成电压表模板时，回退到当前已在 `IEEE39 bus37` 上验证过的 generic scaffold

## 关于故障与扰动

研究工作流里，“添加故障”通常发生在模型准备阶段，而不是由 `EMTResult` 在结果阶段完成。

也就是说，仓库当前更关注：

1. 如何基于已有算例构造好故障研究场景
2. 如何运行 EMT
3. 如何读取波形和消息
4. 如何把首批波形导出到后续稳定性分析流程

而不是把实时交互控制当成主线。

### 关于 SDK 可编程性的谨慎说明

从 SDK 代码本身看，当前可确认的程序化抓手主要是：

- `model.getAllComponents()`
- `model.addComponent()`
- `model.updateComponent()`
- `model.removeComponent()`

也就是说，若未来要进一步沉淀“脚本化故障场景构造”或“脚本化量测/输出配置”，基础仍然会是元件定义 RID、参数字典和引脚连接的精细化操作。

但在仓库尚未给出 live 可复现样例之前，不应把这部分写成已完成主线。

## 当前阶段不作为重点的 API

以下 API 可以保留参考说明，但当前不作为近期端到端验证重点：

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

- 它们更依赖实时交互、流式控制条件或专门环境
- 当前仓库主攻普通云仿真和离线结果分析

## 对应示例与文档

- 示例：`examples/basic/ieee3_emt_preparation_example.py`
- 示例：`examples/simulation/run_emt_simulation.py`
- API：`docs/api-reference/model-api.md`
- API：`docs/api-reference/job-api.md`
- API：`docs/api-reference/emtresult-api.md`
- 主线说明：`docs/guides/research-workflow-core-apis.md`
