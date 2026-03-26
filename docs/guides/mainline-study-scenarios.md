# 主线研究场景矩阵

本矩阵不按 SDK 类拆分，而按电气工程师常见的离线研究任务来组织主线 API。

目的只有一个：把“能调 API”收敛成“能做研究”。

## 使用原则

一个场景只有同时满足下面三点，才值得进入当前主线：

1. 能映射到真实研究动作，而不是孤立 API 演示
2. 能写出可复验的结果判据，而不是只看“任务成功”
3. 能由当前已验证主线 API 完成

## 已验证典型场景

| 场景 | 研究问题 | 模型 | 核心动作 | 核心 API | 当前证据 |
|------|----------|------|----------|-----------|----------|
| 潮流基线校核 | 现有算例是否可算，结果表是否可读 | `model/holdme/IEEE39` | `fetchTopology("powerFlow")` -> `runPowerFlow()` -> 读取节点/支路表 | `Model.fetch`, `model.fetchTopology`, `model.runPowerFlow`, `PowerFlowResult.getBuses/getBranches` | live 集成测试 |
| 潮流结果回写 | 稳态结果能否写回模型，作为下一轮试算或 EMT 初值 | `model/holdme/IEEE39` | `runPowerFlow()` -> `powerFlowModify()` -> `Model(model_data)` | `PowerFlowResult.powerFlowModify` | live 集成测试 |
| 负荷扰动再平衡 | 局部负荷增加后，系统平衡机组是否按预期增发 | `model/holdme/IEEE39` | 将 `load-39` 从 `1104/250` 提到 `1400/350`，再运行潮流并比较母线结果 | `model.getAllComponents`, `model.updateComponent`, `model.runPowerFlow`, `PowerFlowResult.getBuses` | live 集成测试 |
| 潮流回写后二次试算一致性 | 用潮流结果回写后的模型再次试算，关键母线结果是否基本保持一致 | `model/holdme/IEEE39` | `runPowerFlow()` -> `powerFlowModify()` -> 新模型再次 `runPowerFlow()`，对比关键母线电压与机组出力 | `PowerFlowResult.powerFlowModify`, `model.runPowerFlow`, `PowerFlowResult.getBuses` | live 集成测试 |
| 线路参数扰动后的潮流再分布 | 提高关键线路电抗后，支路传输与邻近母线状态是否按预期变化 | `model/holdme/IEEE39` | 将 `line-26-28` (`canvas_0_126`) 的 `X1pu` 从 `0.0474` 提到 `0.0600`，再比较支路潮流与邻近母线相角/电压 | `model.getComponentByKey`, `model.updateComponent`, `model.runPowerFlow`, `PowerFlowResult.getBranches/getBuses` | live 集成测试 |
| 线路切除后的潮流改道 | 切除关键线路后，潮流是否转移到替代走廊，局部母线状态是否明显变化 | `model/holdme/IEEE39` | 从本地工作副本移除 `line-26-28` (`canvas_0_126`)，再比较 `line-26-29`、`line-28-29` 和切除支路两端母线结果 | `model.removeComponent`, `model.runPowerFlow`, `PowerFlowResult.getBranches/getBuses` | live 集成测试 |
| 停运语义等价性校核 | `props.enabled=False` 能否作为“不物理删除元件”的可靠停运写法 | `model/holdme/IEEE39` | 对 `line-26-28` 和变压器 `canvas_0_47` 分别验证 `removeComponent()` 与 `props.enabled=False` 两种工况表达，并比较支路/母线结果是否一致 | `model.updateComponent`, `model.removeComponent`, `model.runPowerFlow`, `PowerFlowResult.getBranches/getBuses` | live 集成测试 |
| 机组电压设定值调整 | 提高 PV 机组电压设定值后，机端母线电压和无功支撑是否按预期抬升 | `model/holdme/IEEE39` | 将 `Gen30` (`canvas_2_303`) 的 `pf_V` 从 `1.047` 提到 `1.070`，再比较机端母线和邻近母线电压，以及机组无功出力 | `model.getComponentByKey`, `model.updateComponent`, `model.runPowerFlow`, `PowerFlowResult.getBuses` | live 集成测试 |
| 机组有功再调度 | 提高远端机组有功设定后，平衡机组出力和关键送电走廊潮流是否按预期重分布 | `model/holdme/IEEE39` | 将 `Gen38` (`canvas_9_384`) 的 `pf_P` 从 `830` 提到 `900`，再比较平衡机组出力、Gen38 无功支撑，以及 `line-26-27/26-28/26-29/28-29` 等关键走廊 | `model.getComponentByKey`, `model.updateComponent`, `model.runPowerFlow`, `PowerFlowResult.getBuses/getBranches` | live 集成测试 |
| 负荷中心转移 | 在总负荷近似守恒时，把需求从平衡母线转到远端负荷口袋后，局部电压和断面潮流会如何变化 | `model/holdme/IEEE39` | 将 `load-39` 降到 `904/190`，同时把 `load-21` 提到 `474/175`，再比较平衡机组、`bus21/bus22/bus23` 和 `line-21-22/22-23/23-24` 走廊 | `model.getComponentByKey`, `model.updateComponent`, `model.runPowerFlow`, `PowerFlowResult.getBuses/getBranches` | live 集成测试 |
| 无功压力与电压薄弱性 | 远端负荷口袋的无功需求上升后，局部电压是否明显下探，以及系统主要靠哪些机组提供无功支撑 | `model/holdme/IEEE39` | 将 `load-21` 的无功从 `115` 提到 `215 MVar`，再比较 `bus21/bus22/bus23/bus24` 电压、平衡机组无功以及主要无功支撑母线 | `model.getComponentByKey`, `model.updateComponent`, `model.runPowerFlow`, `PowerFlowResult.getBuses/getBranches` | live 集成测试 |
| 多工况批量潮流研究 | 一轮研究里连续比较负荷、线路参数、线路切除、机组调压、机组再调度、负荷中心转移和无功压力等工况时，关键指标是否能形成一份可读汇总表 | `model/holdme/IEEE39` | 在同一基线模型上依次运行 `baseline / load_up / line_x_up / line_outage / gen30_v_up / gen38_p_up / load_shift_39_to_21 / load21_q_up`，汇总平衡机组出力、Bus30/Bus21 电压、Gen38 出力和关键走廊潮流 | `model.updateComponent`, `model.removeComponent`, `model.runPowerFlow`, `PowerFlowResult.getBuses/getBranches` | live 集成测试 |
| 全网支路 N-1 筛查 | `IEEE39` 基线在役支路依次停运时，能否形成统一的潮流严重性筛查摘要，并定位最危险工况的主导问题 | `model/holdme/IEEE39` | 自动发现基线潮流结果里真实在役的 `TransmissionLine` 与 `_newTransformer_3p2w`，逐条执行 `props.enabled=False`，汇总目标支路是否消失、相对基线新增的电压越限、最低电压及其母线、缺失母线数、最大电压偏移和最大潮流偏移及其对应对象，并给出排序与工程 digest | `model.updateComponent`, `model.runPowerFlow`, `PowerFlowResult.getBuses/getBranches` | live 集成测试 |
| 检修方式安全校核 | 在一个计划停运工况已经成立后，系统是否仍可继续做残余 N-1 复核，并定位检修态下更敏感的支路 | `model/holdme/IEEE39` | 先对 `line-26-28` (`canvas_0_126`) 或变压器 `canvas_0_47` 执行 `props.enabled=False` 建立检修态，再把检修态作为新的比较基线，对剩余已验证子集继续停运并按受限判据形成排序与结论文本 | `model.updateComponent`, `model.runPowerFlow`, `PowerFlowResult.getBuses/getBranches` | live 集成测试 |
| EMT 最小闭环 | 已准备好的故障场景能否运行 EMT 并返回波形 | `model/holdme/IEEE3` + 本地准备副本 | 修改故障时间和输出频率后运行 `runEMT()` | `Model.load`, `model.updateComponent`, `model.runEMT`, `EMTResult.getPlots/getPlotChannelData` | live 集成测试 |
| 故障清除时间敏感性 | 延长故障切除时间后，后故障电压响应是否明显变化 | `model/holdme/IEEE3` | 将 `fe` 从 `2.7` 延长到 `2.9`，比较 `vac` 对应波形在 `t=2.95s` 的值 | `model.updateComponent`, `model.runEMT`, `EMTResult.getPlotChannelNames/getPlotChannelData` | live 集成测试 |
| EMT 采样分辨率对比 | 输出通道采样频率变化后，波形点数和时间分辨率是否按预期变化 | `model/holdme/IEEE3` | 将输出采样频率分别设为 `1000` 和 `2000`，比较同一波形的点数与时间步长 | `model.updateComponent`, `model.runEMT`, `EMTResult.getPlotChannelData` | live 集成测试 |
| 故障参数 `chg` 灵敏度 | 故障元件参数变化后，故障中和故障后的电压跌落是否按工况出现明显差异 | `model/holdme/IEEE3` | 固定 `fs=2.5`、`fe=2.7`，仅比较 `_newFaultResistor_3p.chg=1e-6` 与 `1e4` 的电压波形 | `model.updateComponent`, `model.runEMT`, `EMTResult.getPlotChannelData` | live 集成测试 |
| EMT 故障严重度与切除时间对比研究 | 同一故障深度下延迟切除，与同一切除时间下降低故障严重度，对故障中/故障后电压恢复的影响能否被稳定区分 | `model/holdme/IEEE3` | 固定 `plot-2 / vac:0`，比较 `baseline(fe=2.7, chg=0.01)`、`delayed_clearing(fe=2.9, chg=0.01)`、`mild_fault(fe=2.7, chg=1e4)` 三工况在故障前、故障中、故障后和晚恢复窗口上的 RMS 指标 | `model.updateComponent`, `model.runEMT`, `EMTResult.getPlotChannelNames/getPlotChannelData` | live 集成测试 |
| EMT 故障严重度扫描 | 在固定清除时间下，扫描多个 `chg` 点后，故障跌落和恢复缺口能否形成稳定的严重度排序 | `model/holdme/IEEE3` | 固定 `fe=2.7` 与 `plot-2 / vac:0`，比较 `chg=1e-2 / 1e2 / 1e4` 三点的 `fault_drop_vs_prefault` 与 `postfault_gap_vs_prefault` | `model.updateComponent`, `model.runEMT`, `EMTResult.getPlotChannelData` | live 集成测试 |
| EMT 故障清除时间扫描 | 在固定研究审视时刻上，随着 `fe` 延后，恢复缺口能否形成稳定的单调恶化排序 | `model/holdme/IEEE3` | 固定 `chg=0.01` 与 `plot-2 / vac:0`，扫描 `fe=2.70 / 2.75 / 2.80 / 2.85 / 2.90`，比较固定时刻 `2.95s` 与 `3.00s` 的 RMS 缺口 `gap_295 / gap_300` | `model.updateComponent`, `model.runEMT`, `EMTResult.getPlotChannelData` | live 集成测试 |
| EMT 量测可观测性工作流 | 能否在同一条 EMT 研究线上同时使用已有测点、增加关键测点并删除不需要的输出通道 | `model/holdme/IEEE3` | 使用已有 `vac`，新增 `Bus2` 电压测点 `bus2_added`，并把 PQ 组裁剪到仅保留 `#P*` 通道，再验证新增测点 RMS 与保留下来的 `#P1` 读数 | `model.addComponent`, `model.updateComponent`, `revision.getImplements().getDiagram().cells`, `model.runEMT`, `EMTResult.getPlotChannelNames/getPlotChannelData`, `model.fetchTopology` | live 集成测试 |
| EMT N-1 安全筛查 | 固定故障下枚举单支路/单变压器停运时，能否用多母线恢复缺口和 `#P1` 支撑读数形成一个暂态安全排序 | `model/holdme/IEEE3` | 自动发现 `TransmissionLine` 与 `_newTransformer_3p2w`，逐条执行 `props.enabled=False`，保留 `Bus7 vac`、新增 `Bus2/Bus8` 电压测点，并比较 `Bus7/Bus2/Bus8` 的后故障/晚恢复缺口以及 `#P1` 平均值 | `model.getComponentsByRid`, `model.updateComponent`, `model.addComponent`, `revision.getImplements().getDiagram().cells`, `model.runEMT`, `EMTResult.getPlotChannelData` | live 集成测试 + 手工 live 全扫描 |
| 潮流回写后进入 EMT | 更重负荷经潮流回写后，EMT 是否从新的稳态工作点起算 | `model/holdme/IEEE3` | 提高 7 号母线负荷，先 `runPowerFlow()` + `powerFlowModify()`，再运行 EMT 并比较机端功率通道 | `model.updateComponent`, `model.runPowerFlow`, `PowerFlowResult.powerFlowModify`, `model.runEMT`, `EMTResult.getPlotChannelData` | live 集成测试 |
| 量测与输出通道脚本化整理 | 研究专用命名、输出裁剪和已有信号的新增通道能否脚本化作用到真实 EMT 结果 | `model/holdme/IEEE3` | 将 `#vac/vac` 改为 `#bus7_voltage/bus7_voltage`，把 PQ 输出分组裁剪到仅保留 `#P*` 通道，并为 `#vac` 新增 `vac_copy` 输出通道 | `model.addComponent`, `model.updateComponent`, `model.runEMT`, `EMTResult.getPlotChannelNames/getPlotChannelData` | live 集成测试 |
| 新增量测元件接入 EMT 输出 | 基于现有模板或 generic edge scaffold 新增母线电压表后，新的量测链路能否稳定出图 | `model/holdme/IEEE3`, `model/holdme/IEEE39` | 在 `IEEE3` 上分别接入 `Bus7`、`Bus2`，在 `IEEE39` 上直接接入 `bus37`；新增 `_NewVoltageMeter`、`_newChannel`、meter->bus `diagram-edge` 后验证通道返回和稳态 RMS | `model.addComponent`, `Component`, `revision.getImplements().getDiagram().cells`, `model.runEMT`, `EMTResult.getPlotChannelNames/getPlotChannelData`, `model.fetchTopology` | live 集成测试 |

## 当前优先 backlog

下面这些方向值得继续做，但要等前面的场景完全沉淀后再扩：

| 候选场景 | 研究意义 | 当前状态 |
|----------|----------|----------|
| 批量化新增量测元件 | 更接近大规模 EMT 研究准备 | 单个 `_NewVoltageMeter` + `diagram-edge` + `_newChannel` 已在 `IEEE3 Bus7/Bus2` 与 `IEEE39 bus37` 上 live 验证；尚未沉淀成跨多母线/多模板的通用批量化脚本 |

## 当前不进入主线的方向

以下方向暂时不进入当前矩阵：

- IES 研究场景
- SFEMT 场景
- 三相不平衡潮流场景
- 实时交互控制场景
- 硬件联调场景

原因不是“不重要”，而是它们会显著稀释当前离线研究主线的文档和测试密度。
