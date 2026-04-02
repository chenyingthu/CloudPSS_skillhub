# CloudPSS SDK 文档索引

本目录优先面向 CloudPSS 的离线研究工作流，而不是单纯按 SDK 对象结构罗列文档。

## 📚 推荐入口

建议先按工作流阅读，再进入按对象组织的 API 入口文档：

- [研究工作流核心 API](./guides/research-workflow-core-apis.md) - 以建模、潮流、EMT 离线研究闭环组织的核心范围说明
- [建模与改模工作流指南](./guides/model-building-workflow.md) - 面向模板选取、工作分支创建和元件修改的操作路线
- [潮流研究工作流指南](./guides/powerflow-study-workflow.md) - 面向模型校核、潮流试算和结果回写的操作路线
- [EMT 研究工作流指南](./guides/emt-study-workflow.md) - 面向 EMT 仿真、波形提取和结果排错的操作路线
- [元件元数据系统](./metadata/README.md) - 组件参数自动补全、验证和引脚检查框架
- [EMT 主线验收清单](./guides/emt-mainline-acceptance-checklist.md) - 将当前 EMT 主线压缩为固定模型、固定故障链、固定监测链和证据等级的可复核 checklist
- [EMT 母线电压量测链指南](./guides/emt-voltage-meter-chain-guide.md) - 面向 `_newBus_3p` 母线脚本化新增电压表、输出通道和 `diagram-edge` 的受限配方
- [主线研究场景矩阵](./guides/mainline-study-scenarios.md) - 以工程研究问题组织当前主线案例，而不是只按 API 枚举
- [参数化研究矩阵](./guides/parameterized-study-matrix.md) - 当前 `IEEE39/IEEE3` 已验证参数化案例库索引，包含脚本入口、本地/ live 验证、复核命令与结论边界
- [主线覆盖矩阵](./guides/mainline-coverage-matrix.md) - 当前主线 API 的文档、示例、测试对应关系
- [主线验收基线](./guides/mainline-acceptance-baseline.md) - 当前阶段主线完成判断、证据基线和延后范围
- [主线证据登记表](./guides/mainline-evidence-register.md) - 当前主线能力与本地测试、live 集成测试、手工 live 探针的对应清单
- [SDK Inventory](./api-inventory.md) - 基于已安装 SDK 自动生成的 API 清单与 gap report

## 📚 API 入口文档

### 主线优先

| 文档 | 说明 | 主要功能 |
|------|------|----------|
| [Model API](./api-reference/model-api.md) | 研究起点与分支管理入口 | 获取/保存模型，改模，发起仿真 |
| [Job API](./api-reference/job-api.md) | 任务轮询与结果承接入口 | 创建任务，查询状态，承接结果 |
| [PowerFlowResult API](./api-reference/powerflow-result-api.md) | 潮流结果处理入口 | 读取节点/支路结果，回写模型 |
| [EMTResult API](./api-reference/emtresult-api.md) | EMT 结果处理入口 | 提取波形，读取消息，定位异常 |
| [Component API](./api-reference/component-api.md) | 元件编辑入口 | 添加、删除、更新、查询元件 |

### 辅助类与次级入口

- [ModelRevision API](./api-reference/revision-api.md) - revision 级拓扑获取、显式 revision 提交和版本数据检查
- `ModelTopology` - 拓扑数据结构
- `IESResult` - 综合能源系统结果（当前未单列 API 文档，且不属于当前主线）

`ModelRevision` 很重要，但它更像“已经进入主线之后的高级接口”，不是推荐的第一个入口。

## 📝 示例程序

### 主线示例

| 示例 | 说明 | 文件路径 |
|------|------|----------|
| 模型获取与研究起点 | 演示 `Model.fetch()`、`Model.fetchMany()`、从本地 YAML 恢复以及本地工作副本创建 | [`examples/basic/model_fetch_example.py`](../examples/basic/model_fetch_example.py) |
| 研究分支管理 | 演示本地工作副本创建、本地快照保存、从本地副本继续，以及云端另存分支 | [`examples/basic/model_save_dump_example.py`](../examples/basic/model_save_dump_example.py) |
| IEEE3 EMT 前置准备 | 演示故障元件、量测信号、输出通道和 EMT 输出分组的本地工作副本微调 | [`examples/basic/ieee3_emt_preparation_example.py`](../examples/basic/ieee3_emt_preparation_example.py) |
| EMT 母线电压量测链准备 | 演示在本地工作副本上为 `_newBus_3p` 新增 `_NewVoltageMeter`、`_newChannel`、meter->bus `diagram-edge` 和 EMT 输出分组 | [`examples/basic/emt_voltage_meter_chain_example.py`](../examples/basic/emt_voltage_meter_chain_example.py) |
| EMT 量测可观测性工作流 | 演示 `IEEE3` 上如何在同一条 EMT 研究线里使用已有测点、增加 `Bus2` 测点、裁剪掉不需要的 `#Q*` 输出，并形成多测点联合结论 | [`examples/analysis/emt_measurement_workflow_example.py`](../examples/analysis/emt_measurement_workflow_example.py) |
| EMT N-1 安全筛查 | 演示 `IEEE3` 上如何枚举线路/变压器单停运工况，在固定故障下比较 `Bus7/Bus2/Bus8` 恢复缺口与 `#P1` 支撑读数，并形成排序与安全摘要 | [`examples/analysis/emt_n1_security_screening_example.py`](../examples/analysis/emt_n1_security_screening_example.py) |
| EMT N-1 专题报告 | 将 `Trans1 / tline4 / tline6` 代表性工况收敛成一份 Markdown 研究报告，突出最重、最轻与线路首位案例 | [`examples/analysis/emt_n1_security_report_example.py`](../examples/analysis/emt_n1_security_report_example.py) |
| EMT N-1 全扫描报告 | 将默认发现到的全部 `IEEE3` N-1 候选工况整理成一份 Markdown 报告，突出严重性分布、榜首工况和完整排序表 | [`examples/analysis/emt_n1_full_report_example.py`](../examples/analysis/emt_n1_full_report_example.py) |
| EMT 研究报告汇总 | 将已验证的 EMT 工况对比、清除时间扫描、严重度扫描和量测工作流汇总成一份 Markdown 研究报告 | [`examples/analysis/emt_research_report_example.py`](../examples/analysis/emt_research_report_example.py) |
| EMT 故障清除时间扫描 | 演示 `IEEE3` 上如何扫描多个 `fe` 点，并在固定研究审视时刻比较恢复缺口 | [`examples/analysis/emt_fault_clearing_scan_example.py`](../examples/analysis/emt_fault_clearing_scan_example.py) |
| EMT 故障严重度扫描 | 演示 `IEEE3` 上如何扫描多个 `chg` 点，并形成故障跌落/恢复缺口的排序与自动结论 | [`examples/analysis/emt_fault_severity_scan_example.py`](../examples/analysis/emt_fault_severity_scan_example.py) |
| 元件操作 | 演示添加、查询、更新、删除元件；支持云端只读模型或本地 YAML 起步 | [`examples/basic/component_example.py`](../examples/basic/component_example.py) |
| 潮流计算 | 运行潮流试算、读取结果并可选写回模型；支持云端 RID 或本地研究副本 | [`examples/simulation/run_powerflow.py`](../examples/simulation/run_powerflow.py) |
| 潮流工程研究场景 | 演示 `IEEE39` 上的线路切除、机组电压设定值调整、机组有功再调度、负荷中心转移和无功压力五类工程化潮流研究 | [`examples/analysis/powerflow_engineering_study_example.py`](../examples/analysis/powerflow_engineering_study_example.py) |
| 潮流多工况研究汇总 | 演示 `IEEE39` 上负荷、线路参数、线路切除、机组调压、机组再调度、负荷中心转移和无功压力等多工况批量试算与指标汇总 | [`examples/analysis/powerflow_batch_study_example.py`](../examples/analysis/powerflow_batch_study_example.py) |
| 全网支路 N-1 潮流筛查 | 演示 `IEEE39` 基线在役线路与变压器支路的停运严重性筛查、工程 digest、CSV 导出与候选支路自动发现入口 | [`examples/analysis/powerflow_n1_screening_example.py`](../examples/analysis/powerflow_n1_screening_example.py) |
| 检修方式安全校核 | 演示 `IEEE39` 上如何先建立计划停运工况，再对检修状态下的剩余支路做受限 N-1 复核，并导出摘要 CSV 与结论文本 | [`examples/analysis/powerflow_maintenance_security_example.py`](../examples/analysis/powerflow_maintenance_security_example.py) |
| EMT 故障研究摘要 | 演示 `IEEE3` 上如何比较基线故障、延迟切除和较轻故障三工况，并提取 RMS、相对故障前缺口、摘要 CSV、对比波形 CSV、时间窗裁剪导出和自动结论文本 | [`examples/analysis/emt_fault_study_example.py`](../examples/analysis/emt_fault_study_example.py) |
| EMT 仿真运行 | 运行 EMT 仿真、提取波形并查看消息；支持云端 RID 或本地准备 YAML | [`examples/simulation/run_emt_simulation.py`](../examples/simulation/run_emt_simulation.py) |

### 辅助示例与延后方向

| 示例 | 说明 | 文件路径 |
|------|------|----------|
| 版本管理 | 演示 revision 级拓扑获取和显式 `revision.run()`；支持云端 RID 或本地 YAML | [`examples/basic/revision_example.py`](../examples/basic/revision_example.py) |
| SFEMT 仿真 | 移频电磁暂态仿真，当前不是主攻范围 | [`examples/simulation/run_sfemt_simulation.py`](../examples/simulation/run_sfemt_simulation.py) |
| IES 仿真 | 综合能源系统仿真，当前不是主攻范围；示例仅保留 SDK 边界入口，不代表已完成 live 闭环验证 | [`examples/simulation/run_ies_simulation.py`](../examples/simulation/run_ies_simulation.py) |

### 当前重点

- 优先阅读和运行建模、潮流、EMT 三条主线的示例
- 实时仿真控制不是当前阶段的主攻范围

## 🧪 测试程序

| 测试 | 说明 | 文件路径 |
|------|------|----------|
| SDK API 测试 | 本地 SDK 边界测试，以及主线 live 集成入口 | [`tests/test_sdk_api.py`](../tests/test_sdk_api.py) |

运行测试：
```bash
pytest tests/ -q
pytest tests/ -q --run-integration -m "integration and not slow_emt"
pytest tests/test_emt_result.py -q --run-integration -m "integration and slow_emt"
TEST_SAVE_KEY_PREFIX=study_branch pytest tests/ -q --run-integration -m "integration and not slow_emt"
TEST_SAVE_KEY_PREFIX=study_branch pytest tests/ -q --run-integration -m integration
```

## 🔧 快速查找

### 按工作流查找

**建模与改模**
- Guide：[建模与改模工作流指南](./guides/model-building-workflow.md)
- API 文档：[Model API](./api-reference/model-api.md), [Component API](./api-reference/component-api.md)
- 示例：[`model_fetch_example.py`](../examples/basic/model_fetch_example.py), [`component_example.py`](../examples/basic/component_example.py), [`model_save_dump_example.py`](../examples/basic/model_save_dump_example.py)
- 已验证的主线：研究分支管理示例既可从云端算例起步，也可从已有本地 YAML 副本继续
- 已验证的主线：组件示例可在真实模型的本地工作副本上完成 add/update/remove，并继续拉取 `powerFlow` revision 拓扑
- 已验证的边界：对 fetched 工作副本，`fetchTopology()` 不应被解读为“未保存本地改动已进入拓扑/求解器”的证明；这类确认应依赖真实 `runPowerFlow()` / `runEMT()`
- 当输入已经是本地 YAML 时，示例默认会建议新的 `*-branch.yaml` 路径，避免覆盖源副本

**潮流试算**
- Guide：[潮流研究工作流指南](./guides/powerflow-study-workflow.md)
- API 文档：[Model API](./api-reference/model-api.md), [Job API](./api-reference/job-api.md), [PowerFlowResult API](./api-reference/powerflow-result-api.md)
- 示例：[`run_powerflow.py`](../examples/simulation/run_powerflow.py), [`powerflow_engineering_study_example.py`](../examples/analysis/powerflow_engineering_study_example.py), [`powerflow_batch_study_example.py`](../examples/analysis/powerflow_batch_study_example.py), [`powerflow_n1_screening_example.py`](../examples/analysis/powerflow_n1_screening_example.py)
- 示例：[`powerflow_maintenance_security_example.py`](../examples/analysis/powerflow_maintenance_security_example.py)
- 已验证的主线：本地 YAML 工作副本可以直接继续运行潮流试算
- 已验证的研究场景：`IEEE39` 上的线路切除、机组电压设定值调整、`Gen38` 有功再调度、`load-39 -> load-21` 负荷转移和 `load-21 q: 115 -> 215` 无功压力都已经有 live 集成验证
- 已验证的研究汇总：`IEEE39` 上 `baseline / load_up / line_x_up / line_outage / gen30_v_up / gen38_p_up / load_shift_39_to_21 / load21_q_up` 可以组成一轮多工况潮流研究摘要
- 已验证的全网 N-1 路径：`props.enabled=False` 可在 `IEEE39` 基线在役支路集合上表达停运，并支撑线路+变压器的严重性筛查、排序、工程 digest 和 CSV 导出；其中 `line-6-11` 因基线支路表缺席而不纳入主线候选集
- 已验证的检修校核路径：可先停运 `IEEE39 line-26-28` 或变压器 `canvas_0_47`，再在检修态上对剩余已验证子集继续做受限 N-1 复核，并输出排序与结论文本

**EMT 仿真**
- Guide：[EMT 研究工作流指南](./guides/emt-study-workflow.md)
- Guide：[EMT 母线电压量测链指南](./guides/emt-voltage-meter-chain-guide.md)
- API 文档：[Model API](./api-reference/model-api.md), [Job API](./api-reference/job-api.md), [EMTResult API](./api-reference/emtresult-api.md)
- 示例：[`ieee3_emt_preparation_example.py`](../examples/basic/ieee3_emt_preparation_example.py), [`emt_voltage_meter_chain_example.py`](../examples/basic/emt_voltage_meter_chain_example.py), [`emt_measurement_workflow_example.py`](../examples/analysis/emt_measurement_workflow_example.py), [`emt_fault_study_example.py`](../examples/analysis/emt_fault_study_example.py), [`emt_fault_clearing_scan_example.py`](../examples/analysis/emt_fault_clearing_scan_example.py), [`emt_fault_severity_scan_example.py`](../examples/analysis/emt_fault_severity_scan_example.py), [`run_emt_simulation.py`](../examples/simulation/run_emt_simulation.py)
- 已验证的最小闭环：先生成 `examples/basic/ieee3-emt-prepared.yaml`，再用 `run_emt_simulation.py` 直接加载该本地副本运行 EMT
- 已验证的量测工作流：`emt_measurement_workflow_example.py` 已在 `IEEE3` 上把“用已有 `vac`、增 `Bus2` 测点、删 `#Q*` 输出”收敛成一条 live 可复验的可观测性整理路径，并可输出 `Bus7/Bus2/#P1` 的联合结论
- 已验证的研究摘要：`emt_fault_study_example.py` 已在 `IEEE3` 上对 `baseline / delayed_clearing / mild_fault` 三工况做 live 对比，并固定写明只对这条量测链和时间窗口宣称成立
- 已验证的清除时间扫描能力：`emt_fault_clearing_scan_example.py` 已在 `IEEE3` 上对 `fe=2.70..2.90` 做 live 扫描，并给出固定研究时刻恢复缺口的单调恶化结论
- 已验证的扫描能力：`emt_fault_severity_scan_example.py` 已在 `IEEE3` 上对 `chg=1e-2 / 1e2 / 1e4` 做 live 扫描，并给出故障跌落/恢复缺口的排序结论
- 已验证的 EMT N-1 安全筛查能力：`emt_n1_security_screening_example.py` 已在 `IEEE3` 上验证“单支路停运 + 固定故障 + 多母线恢复缺口 + `#P1` 支撑读数”的组合路径，可形成排序与工程 digest
- 已验证的受限扩展：可在 `_newBus_3p` 母线上脚本化新增电压量测链，但当前只应按指南声明的已验证样本和边界使用

**辅助能力**
- API 文档：[ModelRevision API](./api-reference/revision-api.md)
- 示例：[`revision_example.py`](../examples/basic/revision_example.py)
- 说明：只在需要 revision 级拓扑和显式 revision 提交时进入

## 📖 使用指南

### 0. 推荐起点

- 先阅读 [研究工作流核心 API](./guides/research-workflow-core-apis.md)
- 进入建模工作时，优先阅读 [建模与改模工作流指南](./guides/model-building-workflow.md)
- 进入潮流工作时，优先阅读 [潮流研究工作流指南](./guides/powerflow-study-workflow.md)
- 进入 EMT 工作时，优先阅读 [EMT 研究工作流指南](./guides/emt-study-workflow.md)
- 需要为母线补挂研究量测链时，再阅读 [EMT 母线电压量测链指南](./guides/emt-voltage-meter-chain-guide.md)
- 再按建模、潮流、EMT 三条主线进入对象级 API 文档
- 当前仓库优先覆盖普通云仿真和离线研究场景，不以实时仿真为主

### 1. 入门流程

```bash
# 1. 阅读研究工作流说明
cat docs/guides/research-workflow-core-apis.md

# 2. 阅读建模工作流
cat docs/guides/model-building-workflow.md

# 3. 阅读潮流工作流
cat docs/guides/powerflow-study-workflow.md

# 4. 查看示例代码
cat examples/simulation/run_powerflow.py
```

### 2. 学习路径

1. **研究主线** → 阅读 [研究工作流核心 API](./guides/research-workflow-core-apis.md)
2. **建模与改模** → 阅读 [建模与改模工作流指南](./guides/model-building-workflow.md)、[Model API](./api-reference/model-api.md) 和 [Component API](./api-reference/component-api.md)
3. **潮流试算** → 阅读 [潮流研究工作流指南](./guides/powerflow-study-workflow.md) 和 [PowerFlowResult API](./api-reference/powerflow-result-api.md)
4. **EMT 仿真** → 阅读 [EMT 研究工作流指南](./guides/emt-study-workflow.md)、[Job API](./api-reference/job-api.md) 和 [EMTResult API](./api-reference/emtresult-api.md)
5. **EMT 量测链准备** → 在需要新增 `_newBus_3p` 母线电压量测链时，再阅读 [EMT 母线电压量测链指南](./guides/emt-voltage-meter-chain-guide.md)
6. **实践练习** → 运行 `run_powerflow.py`、`emt_fault_study_example.py` 与 `run_emt_simulation.py`
   EMT 最小闭环可直接串联 `ieee3_emt_preparation_example.py` -> `run_emt_simulation.py examples/basic/ieee3-emt-prepared.yaml`
   需要先看一份研究型 EMT 摘要时，可直接运行 `emt_fault_study_example.py`
   需要脚本化补挂母线电压量测时，可串联 `emt_voltage_meter_chain_example.py` -> `run_emt_simulation.py`
7. **测试验证** → 运行测试程序验证理解

### 3. 问题排查

**常见问题**

1. **无法获取项目**
   - 检查 API token 是否正确设置
   - 若只是试读示例，优先使用已验证可访问的 `model/holdme/IEEE39`
   - 确认项目 RID 格式正确（`model/owner/key`）
   - 验证项目是否存在且有访问权限

2. **仿真运行失败**
   - 确认项目有有效的计算方案
   - 检查参数方案是否完整
   - 查看错误信息中的详细描述

3. **结果数据为空**
   - 确认仿真已完成（`job.status() == 1`）
   - 检查项目是否有输出配置

## 📊 主线覆盖状态

| 主线能力 | 文档状态 | 示例状态 | 测试状态 |
|------|---------|---------|---------|
| 研究起点与分支管理 | ✅ 已覆盖 | ✅ 已覆盖 | ✅ 已覆盖，`model.save()` live 写入为 opt-in |
| 建模与改模 | ✅ 已覆盖 | ✅ 已覆盖 | ✅ 已覆盖 |
| 拓扑检查与 revision 控制 | ✅ 已覆盖 | ✅ 已覆盖 | ✅ 已覆盖，且已明确 `fetchTopology()` 的 revision 级边界 |
| 潮流试算与结果回写 | ✅ 已覆盖 | ✅ 已覆盖 | ✅ 已覆盖 |
| EMT 仿真与结果提取 | ✅ 已覆盖 | ✅ 已覆盖 | ✅ 已覆盖，含 `_newBus_3p` 电压量测链的受限 live 配方 |
| IES 与实时仿真扩展 | ⏳ 非当前主线 | ⏳ 非当前主线 | ⏳ 非当前主线 |

## 🔗 相关资源

- **官方文档**: `cloudpss_docs/` 目录
- **SDK 源码**: `/home/chenying/anaconda3/lib/python3.12/site-packages/cloudpss/`
- **官方网站**: https://www.cloudpss.net

## 📝 贡献指南

欢迎贡献文档和示例程序：

1. Fork 本仓库
2. 创建新分支
3. 添加文档或示例
4. 提交 Pull Request

---

**最后更新**: 2026-03-23
**SDK 版本**: 4.5.28
