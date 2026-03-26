# 主线覆盖矩阵

本矩阵只关注当前仓库的主线目标：支持 CloudPSS 离线研究闭环，而不是平均覆盖全部 SDK 类。

主线闭环是：

1. 获取已有算例或本地工作文件
2. 创建研究分支并改模
3. 做拓扑检查
4. 运行潮流并读取结果
5. 把潮流结果写回模型
6. 运行 EMT 并提取波形与消息

## 使用方式

阅读本矩阵时，优先关注以下四列：

- 是否已有主线文档
- 是否已有主线示例
- 是否已有本地测试
- 是否已有真实集成测试

如果某个 API 只有文档、没有示例或真实验证，就不应该被视为“主线已完成”。

## 覆盖矩阵

| 主线阶段 | API | 文档 | 示例 | 本地测试 | 集成测试 | 当前判断 |
|----------|-----|------|------|----------|----------|----------|
| 获取模型 | `Model.fetch` | `docs/api-reference/model-api.md` | `examples/basic/model_fetch_example.py` | `tests/test_sdk_api.py` | `tests/test_sdk_api.py` | 主线已覆盖 |
| 搜索模型 | `Model.fetchMany` | `docs/api-reference/model-api.md` | `examples/basic/model_fetch_example.py` | `tests/test_sdk_api.py` | `tests/test_sdk_api.py` | 主线已覆盖 |
| 本地分支 | `Model.dump` | `docs/api-reference/model-api.md` | `examples/basic/model_save_dump_example.py` | `tests/test_sdk_api.py` | 无 | 主线已覆盖 |
| 恢复分支 | `Model.load` | `docs/api-reference/model-api.md` | `examples/basic/model_save_dump_example.py` | `tests/test_sdk_api.py` | 无 | 主线已覆盖 |
| 云端另存分支 | `model.save` | `docs/api-reference/model-api.md` | `examples/basic/model_save_dump_example.py` | `tests/test_sdk_api.py` | `tests/test_sdk_api.py`（opt-in） | 语义已清晰；live 写入测试需显式提供 disposable key 前缀 |
| 查询元件 | `model.getAllComponents` | `docs/api-reference/model-api.md`, `docs/api-reference/component-api.md` | `examples/basic/component_example.py` | `tests/test_sdk_api.py` | 无 | 主线已覆盖 |
| 按 key 查元件 | `model.getComponentByKey` | `docs/api-reference/model-api.md`, `docs/api-reference/component-api.md` | `examples/basic/component_example.py` | `tests/test_sdk_api.py` | 无 | 主线已覆盖 |
| 按类型查元件 | `model.getComponentsByRid` | `docs/api-reference/model-api.md`, `docs/api-reference/component-api.md` | `examples/basic/component_example.py` | `tests/test_sdk_api.py` | 无 | 主线已覆盖 |
| 添加元件 | `model.addComponent` | `docs/api-reference/model-api.md`, `docs/api-reference/component-api.md` | `examples/basic/component_example.py` | `tests/test_sdk_api.py` | 无 | 主线已覆盖 |
| 更新元件 | `model.updateComponent` | `docs/api-reference/model-api.md`, `docs/api-reference/component-api.md` | `examples/basic/component_example.py` | `tests/test_sdk_api.py` | 无 | 主线已覆盖 |
| 删除元件 | `model.removeComponent` | `docs/api-reference/model-api.md`, `docs/api-reference/component-api.md` | `examples/basic/component_example.py` | `tests/test_sdk_api.py` | 无 | 主线已覆盖 |
| 拓扑检查 | `model.fetchTopology` | `docs/api-reference/model-api.md`, `docs/api-reference/revision-api.md` | `examples/basic/component_example.py`, `examples/basic/revision_example.py`, `examples/simulation/run_powerflow.py`, `examples/simulation/run_emt_simulation.py` | `tests/test_sdk_api.py` | `tests/test_sdk_api.py` | 主线已覆盖 |
| revision 级拓扑 | `revision.fetchTopology` | `docs/api-reference/revision-api.md` | `examples/basic/revision_example.py` | 无 | `tests/test_sdk_api.py` | 辅助能力已覆盖 |
| 潮流运行 | `model.runPowerFlow` | `docs/api-reference/model-api.md`, `docs/api-reference/job-api.md` | `examples/simulation/run_powerflow.py` | 无 | `tests/test_powerflow_result.py` | 主线已覆盖 |
| 潮流消息 | `PowerFlowResult.getMessagesByKey` | `docs/api-reference/powerflow-result-api.md` | `examples/simulation/run_powerflow.py` | `tests/test_powerflow_result.py` | `tests/test_powerflow_result.py` | 主线已覆盖 |
| 潮流节点结果 | `PowerFlowResult.getBuses` | `docs/api-reference/powerflow-result-api.md` | `examples/simulation/run_powerflow.py` | `tests/test_powerflow_result.py` | `tests/test_powerflow_result.py` | 主线已覆盖 |
| 潮流支路结果 | `PowerFlowResult.getBranches` | `docs/api-reference/powerflow-result-api.md` | `examples/simulation/run_powerflow.py` | `tests/test_powerflow_result.py` | `tests/test_powerflow_result.py` | 主线已覆盖 |
| 潮流回写 | `PowerFlowResult.powerFlowModify` | `docs/api-reference/powerflow-result-api.md` | `examples/simulation/run_powerflow.py` | `tests/test_powerflow_result.py` | `tests/test_powerflow_result.py` | 主线已覆盖 |
| 潮流停运/N-1 支路筛查 | `model.updateComponent`, `model.removeComponent`, `model.runPowerFlow` | `docs/guides/powerflow-study-workflow.md` | `examples/analysis/powerflow_engineering_study_example.py`, `examples/analysis/powerflow_n1_screening_example.py` | `tests/test_examples.py` | `tests/test_powerflow_result.py` | IEEE39 基线在役支路主线已覆盖；其他模型仍需单独验证 |
| 潮流检修方式安全校核 | `model.updateComponent`, `model.runPowerFlow` | `docs/guides/powerflow-study-workflow.md`, `docs/guides/mainline-study-scenarios.md` | `examples/analysis/powerflow_maintenance_security_example.py` | `tests/test_examples.py` | `tests/test_powerflow_result.py` | IEEE39 线路/变压器计划停运 + 检修态残余 N-1 受限路径已覆盖；不等价于完整检修校核平台 |
| EMT 运行 | `model.runEMT` | `docs/api-reference/model-api.md`, `docs/api-reference/job-api.md` | `examples/simulation/run_emt_simulation.py` | 无 | `tests/test_emt_result.py`, `tests/test_sdk_api.py` | 主线已覆盖 |
| EMT 原始消息 | `EMTResult.getMessagesByKey` | `docs/api-reference/emtresult-api.md` | `examples/simulation/run_emt_simulation.py` | `tests/test_emt_result.py` | `tests/test_emt_result.py` | 主线已覆盖 |
| EMT 波形列表 | `EMTResult.getPlots` | `docs/api-reference/emtresult-api.md` | `examples/simulation/run_emt_simulation.py` | `tests/test_emt_result.py` | `tests/test_emt_result.py` | 主线已覆盖 |
| EMT 单个波形 | `EMTResult.getPlot` | `docs/api-reference/emtresult-api.md` | `examples/simulation/run_emt_simulation.py` | `tests/test_emt_result.py` | `tests/test_emt_result.py` | 主线已覆盖 |
| EMT 通道名 | `EMTResult.getPlotChannelNames` | `docs/api-reference/emtresult-api.md` | `examples/simulation/run_emt_simulation.py` | `tests/test_emt_result.py` | `tests/test_emt_result.py` | 主线已覆盖 |
| EMT 通道数据 | `EMTResult.getPlotChannelData` | `docs/api-reference/emtresult-api.md` | `examples/simulation/run_emt_simulation.py` | `tests/test_emt_result.py` | `tests/test_emt_result.py` | 主线已覆盖 |
| EMT 母线电压量测链新增 | `model.addComponent`, `Component`, `revision.getImplements().getDiagram().cells` | `docs/api-reference/component-api.md`, `docs/guides/emt-voltage-meter-chain-guide.md` | `examples/basic/emt_voltage_meter_chain_example.py` | `tests/test_examples.py` | `tests/test_emt_result.py` | 受限主线已覆盖，仅对 `_newBus_3p` 和当前已验证样本宣称成立 |
| EMT N-1 安全筛查 | `model.getComponentsByRid`, `model.updateComponent`, `model.addComponent`, `revision.getImplements().getDiagram().cells`, `model.runEMT`, `EMTResult.getPlotChannelData` | `docs/guides/emt-study-workflow.md`, `docs/guides/mainline-study-scenarios.md` | `examples/analysis/emt_n1_security_screening_example.py` | `tests/test_examples.py` | `tests/test_emt_result.py` | 受限主线已覆盖，仅对 IEEE3 固定故障和 `Bus7/Bus2/Bus8 + #P1` 监测链宣称成立 |

## 当前剩余 gap

以下项目仍可继续完善，但不妨碍主线框架成立：

- `model.save()` 的 live 写入链路已经有 opt-in 集成测试，但仍不适合作为默认 live 套件常规覆盖
- EMT 前置场景中的“故障事件元件搭建”仍然缺少可复用、可广泛迁移的 live SDK 脚本化样例
- EMT 输出链当前已经有 `_newBus_3p` 母线电压量测链的受限 live 配方，但还不能宣称适用于任意母线类型、任意 EMT 模型或大规模批量挂表
- EMT N-1 安全筛查当前已经有 IEEE3 固定故障上的受限路径，但还不能直接外推到其他模型、其他故障位置或更广泛的安全判据体系
- 潮流 N-1 当前已经完成 IEEE39 基线在役支路筛查，但还不能直接把这条结论外推到其他模型

## 不纳入当前主线完成度的能力

以下能力可以保留文档，但不应影响当前主线完成判断：

- `EMTResult.next/goto/send/writeShm/control/monitor/stopSimulation/saveSnapshot/loadSnapshot`
- `model.runSFEMT`
- `model.runThreePhasePowerFlow`
- IES 相关运行接口
- 硬件相关实时仿真联调能力
