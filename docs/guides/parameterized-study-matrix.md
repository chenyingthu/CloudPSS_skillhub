# 参数化研究矩阵

本矩阵不是“可扫一切参数”的目录，而是当前仓库已经沉淀出的参数化研究案例库索引。

只有同时满足下面五件事的条目，才允许进入这里：

1. 有固定模型和固定研究条件
2. 有明确入口脚本
3. 有本地测试，证明脚本和摘要逻辑可复验
4. 有 live 集成测试或已记录的手工 live 探针
5. 有清楚写出的结论边界

如果缺少第 3 项或第 4 项，这个条目就不是当前主线案例库的一部分。

## 如何使用

把本页当成“研究起点导航”，而不是结论汇总页。

每次复用一个案例，至少先确认四件事：

1. 固定基线是否完全一致
2. 你引用的是脚本、测试还是手工 live 探针
3. 你要复核的命令是什么
4. 你准备复述的结论有没有超出当前边界

证据等级沿用 `mainline-evidence-register.md`：

- `A`: 本地测试 + live 集成测试
- `B`: 本地测试 + 手工 live 探针

## IEEE39 潮流案例库

| 案例 | 参数/扰动维度 | 固定基线 | 入口脚本 | 本地验证 | live 验证 | 推荐复核入口 | 证据 | 当前可宣称结论 | 边界 |
|------|------|------|------|------|------|------|------|------|------|
| 负荷扰动再平衡 | `load-39: 1104/250 -> 1400/350` | `model/holdme/IEEE39` | `examples/analysis/powerflow_engineering_study_example.py` | `tests/test_examples.py::TestPowerFlowEngineeringStudyExample` | `tests/test_powerflow_result.py::test_ieee39_load_perturbation_rebalances_local_slack_bus_generation` | `python examples/analysis/powerflow_engineering_study_example.py model/holdme/IEEE39` | A | 平衡机组出力同步抬升 | 只对当前 IEEE39 工况成立 |
| 线路参数扰动 | `line-26-28 X1pu: 0.0474 -> 0.0600` | `model/holdme/IEEE39` | `examples/analysis/powerflow_engineering_study_example.py` | `tests/test_examples.py::TestPowerFlowEngineeringStudyExample` | `tests/test_powerflow_result.py::test_ieee39_line_reactance_perturbation_redistributes_branch_flow_and_bus_angle` | 同上 | A | 目标支路传输下降，邻近母线状态出现可解释变化 | 不外推到任意线路参数 |
| 线路切除 | 移除 `line-26-28` | `model/holdme/IEEE39` | `examples/analysis/powerflow_engineering_study_example.py` | `tests/test_examples.py::TestPowerFlowEngineeringStudyExample` | `tests/test_powerflow_result.py::test_ieee39_line_outage_redistributes_corridor_flow_and_shifts_local_bus_state` | 同上 | A | `line-26-29` 承担主要改道任务，局部母线状态恶化 | 只对当前已验证走廊成立 |
| 机组调压 | `Gen30 pf_V: 1.047 -> 1.070` | `model/holdme/IEEE39` | `examples/analysis/powerflow_engineering_study_example.py` | `tests/test_examples.py::TestPowerFlowEngineeringStudyExample` | `tests/test_powerflow_result.py::test_ieee39_generator_voltage_setpoint_adjustment_changes_local_bus_voltage_and_q_support` | 同上 | A | 机端母线电压与无功支撑同步上升 | 当前不包含 Tap/InitTap 通用调压结论 |
| 机组再调度 | `Gen38 pf_P: 830 -> 900` | `model/holdme/IEEE39` | `examples/analysis/powerflow_engineering_study_example.py` | `tests/test_examples.py::TestPowerFlowEngineeringStudyExample` | `tests/test_powerflow_result.py::test_ieee39_generator_active_power_redispatch_shifts_slack_and_key_transfer_corridors` | 同上 | A | 平衡机组回调，关键走廊传输抬升 | 只对当前 IEEE39 送电走廊成立 |
| 负荷中心转移 | `load-39 -> load-21` | `model/holdme/IEEE39` | `examples/analysis/powerflow_engineering_study_example.py` | `tests/test_examples.py::TestPowerFlowEngineeringStudyExample` | `tests/test_powerflow_result.py::test_ieee39_load_transfer_from_bus39_to_bus21_shifts_remote_corridor_with_nearly_constant_total_demand` | 同上 | A | `bus21` 电压下探，`line-21-22` 增载，远端走廊卸载 | 只对当前目标负荷口袋成立 |
| 无功压力 | `load-21 q: 115 -> 215` | `model/holdme/IEEE39` | `examples/analysis/powerflow_engineering_study_example.py` | `tests/test_examples.py::TestPowerFlowEngineeringStudyExample` | `tests/test_powerflow_result.py::test_ieee39_reactive_stress_on_load21_depresses_local_voltage_and_raises_system_q_support` | 同上 | A | `bus21` 电压明显下探，远端无功支撑上升 | 只对当前无功压力样例成立 |
| 多工况批量汇总 | `baseline / load_up / line_x_up / line_outage / gen30_v_up / gen38_p_up / load_shift_39_to_21 / load21_q_up` | `model/holdme/IEEE39` | `examples/analysis/powerflow_batch_study_example.py` | `tests/test_examples.py::TestPowerFlowBatchStudyExample` | `tests/test_powerflow_result.py::test_ieee39_batch_powerflow_study_summaries_capture_expected_directional_changes` | `python examples/analysis/powerflow_batch_study_example.py model/holdme/IEEE39` | A | 可生成方向正确的多工况研究摘要 | 不等价于通用批量优化框架 |
| 停运语义等价性 | `removeComponent()` vs `props.enabled=False` | `model/holdme/IEEE39` | `examples/analysis/powerflow_n1_screening_example.py` | `tests/test_examples.py::TestPowerFlowN1ScreeningExample` | `tests/test_powerflow_result.py::test_ieee39_line_disable_via_props_enabled_matches_component_removal_for_validated_outage`; `tests/test_powerflow_result.py::test_ieee39_transformer_disable_via_props_enabled_matches_component_removal_for_validated_outage` | `python examples/analysis/powerflow_n1_screening_example.py model/holdme/IEEE39` | A | 在线路 `canvas_0_126` 与变压器 `canvas_0_47` 上，两种停运表达结果一致 | 不外推到其他模型或未验证样本 |
| 全网支路 N-1 | 基线在役 `43` 条支路逐条停运 | `model/holdme/IEEE39` | `examples/analysis/powerflow_n1_screening_example.py` | `tests/test_examples.py::TestPowerFlowN1ScreeningExample` | `tests/test_powerflow_result.py::test_ieee39_full_active_branch_n1_screening_covers_lines_and_transformers_and_stable_top_rankings`; `tests/test_powerflow_result.py::test_ieee39_full_active_branch_n1_screening_digest_identifies_top_line_transformer_and_islanding_cases` | 同上；并参考 `tests/README.md` 的完整 live 套件记录 | A | 可形成统一严重性排序与工程 digest | 只对 IEEE39 基线在役支路集合成立 |
| 检修态残余 N-1 | 计划停运 `canvas_0_126` 或 `canvas_0_47` 后继续复核 | `model/holdme/IEEE39` | `examples/analysis/powerflow_maintenance_security_example.py` | `tests/test_examples.py::TestPowerFlowMaintenanceSecurityExample` | `tests/test_powerflow_result.py::test_ieee39_line_maintenance_state_can_be_rechecked_with_residual_n1_subset`; `tests/test_powerflow_result.py::test_ieee39_transformer_maintenance_state_can_be_rechecked_with_residual_n1_subset` | `python examples/analysis/powerflow_maintenance_security_example.py model/holdme/IEEE39 --maintenance-branch=canvas_0_126` | A | 可在检修态上形成受限残余 N-1 排序 | 不等价于完整检修校核平台 |

## IEEE3 EMT 案例库

| 案例 | 参数/扰动维度 | 固定基线 | 入口脚本 | 本地验证 | live 验证 | 推荐复核入口 | 证据 | 当前可宣称结论 | 边界 |
|------|------|------|------|------|------|------|------|------|------|
| EMT 最小闭环 | `runEMT()` + 波形提取 | `model/holdme/IEEE3` 或 `examples/basic/ieee3-emt-prepared.yaml` | `examples/basic/ieee3_emt_preparation_example.py`; `examples/simulation/run_emt_simulation.py` | `tests/test_examples.py` 中 EMT 相关示例的本地 YAML 入口测试；`tests/test_sdk_api.py` EMT 前置链本地边界 | `tests/test_sdk_api.py` EMT 前置结构集成验证；`tests/test_emt_result.py::test_ieee3_output_sampling_frequency_changes_trace_resolution` | `python examples/basic/ieee3_emt_preparation_example.py`; `python examples/simulation/run_emt_simulation.py examples/basic/ieee3-emt-prepared.yaml` | A | 可真实返回 plots、channel names 和 channel data | 只覆盖普通云 EMT |
| 输出采样分辨率 | `Freq: 1000 -> 2000` | 固定 `model/holdme/IEEE3` 故障链 | `examples/simulation/run_emt_simulation.py` | `tests/test_examples.py::TestEMTFaultStudyExample` 的本地入口覆盖 | `tests/test_emt_result.py::test_ieee3_output_sampling_frequency_changes_trace_resolution` | 参考上条最小闭环命令 | A | 更高采样频率对应更细时间分辨率 | 当前只是输出配置验证，不扩成通用精度指南 |
| 故障清除时间敏感性 | `fe: 2.7 -> 2.9` | 固定 `chg=0.01`，固定 `plot-2 / vac:0` | `examples/analysis/emt_fault_clearing_scan_example.py` | `tests/test_examples.py::TestEMTFaultClearingScanExample` | `tests/test_emt_result.py::test_ieee3_fault_clearing_time_change_affects_post_fault_voltage_trace`; `tests/test_emt_result.py::test_ieee3_fault_clearing_scan_orders_fixed_deadline_recovery_gaps_by_fe` | `python examples/analysis/emt_fault_clearing_scan_example.py model/holdme/IEEE3 --csv=/tmp/emt-clearing.csv --conclusion-txt=/tmp/emt-clearing.txt` | A | 更晚切除会拉低固定研究时刻的后故障恢复 | 只对当前量测链和固定观察时刻成立 |
| 故障严重度灵敏度 | `chg: 1e-6 -> 1e4` | 固定 `fs=2.5`, `fe=2.7` | `examples/analysis/emt_fault_severity_scan_example.py` | `tests/test_examples.py::TestEMTFaultSeverityScanExample` | `tests/test_emt_result.py::test_ieee3_fault_chg_parameter_changes_fault_depth_and_post_fault_recovery`; `tests/test_emt_result.py::test_ieee3_fault_severity_scan_orders_fault_drop_and_recovery_gap_by_chg` | `python examples/analysis/emt_fault_severity_scan_example.py model/holdme/IEEE3 --csv=/tmp/emt-severity.csv --conclusion-txt=/tmp/emt-severity.txt` | A | 更大 `chg` 对应更小故障跌落和恢复缺口 | 只对 `_newFaultResistor_3p` 当前路径成立 |
| 三工况故障研究 | `baseline / delayed_clearing / mild_fault` | 固定 `plot-2 / vac:0` 与 RMS 时间窗 | `examples/analysis/emt_fault_study_example.py` | `tests/test_examples.py::TestEMTFaultStudyExample` | `tests/test_emt_result.py::test_ieee3_fault_study_summary_distinguishes_clearing_time_and_fault_severity` | `python examples/analysis/emt_fault_study_example.py model/holdme/IEEE3 --csv=/tmp/emt-fault-study.csv --conclusion-txt=/tmp/emt-fault-study.txt` | A | 可稳定区分“故障更久”和“故障更轻”两类机制 | 只对当前三工况和当前时间窗成立 |
| 量测可观测性整理 | `Bus7 vac + Bus2 added + 裁剪 #Q*` | 固定 `IEEE3`、`_newBus_3p` 配方 | `examples/basic/emt_voltage_meter_chain_example.py`; `examples/analysis/emt_measurement_workflow_example.py` | `tests/test_examples.py::TestEMTMeasurementWorkflowExample` | `tests/test_emt_result.py::test_ieee3_measurement_workflow_can_add_prune_and_use_channels_together`; `tests/test_emt_result.py::test_ieee3_can_add_new_voltage_meter_to_bus2_and_match_bus_base_rms` | `python examples/analysis/emt_measurement_workflow_example.py model/holdme/IEEE3 --csv=/tmp/emt-measurement.csv --conclusion-txt=/tmp/emt-measurement.txt` | A | 可形成可复验的多测点联合结论 | 只对 `_newBus_3p` 受限配方和当前样本成立 |
| EMT 研究报告汇总 | 整合四条已验证研究路径 | 固定 `IEEE3` 已验证工作线 | `examples/analysis/emt_research_report_example.py` | `tests/test_examples.py::TestEMTResearchReportExample` | `tests/test_emt_result.py::test_ieee3_research_report_wrapper_aggregates_live_sections_into_markdown` | `python examples/analysis/emt_research_report_example.py model/holdme/IEEE3 --report=/tmp/emt-research-report.md` | A | 可把四段研究真实串联成 Markdown 报告 | 只是 wrapper，不是新求解能力 |
| EMT N-1 安全筛查 | 默认发现 `9` 个候选工况 | 固定 `model/holdme/IEEE3`、`_newFaultResistor_3p`、`Bus7/Bus2/Bus8 + #P1` | `examples/analysis/emt_n1_security_screening_example.py` | `tests/test_examples.py::TestEMTN1SecurityScreeningExample` | `tests/test_emt_result.py::test_ieee3_branch_n1_security_scan_ranks_representative_outages`; 手工 full scan 探针记录见 `tests/README.md` | `python examples/analysis/emt_n1_security_screening_example.py model/holdme/IEEE3 --csv=/tmp/emt-n1.csv --conclusion-txt=/tmp/emt-n1.txt` | A | 可形成排序、工程 digest 和受限结论 | 不外推到其他模型、故障位置或安全判据 |
| EMT N-1 报告输出 | 代表性报告 / 全扫描报告 | 固定已验证 EMT N-1 路径 | `examples/analysis/emt_n1_security_report_example.py`; `examples/analysis/emt_n1_full_report_example.py` | `tests/test_examples.py::TestEMTN1SecurityReportExample`; `tests/test_examples.py::TestEMTN1FullReportExample` | `tests/test_emt_result.py::test_ieee3_n1_security_report_wrapper_exports_live_representative_markdown`; `tests/test_emt_result.py::test_ieee3_n1_full_report_wrapper_exports_live_full_scan_markdown` | `python examples/analysis/emt_n1_security_report_example.py model/holdme/IEEE3 --report=/tmp/emt-n1-security-report.md`; `python examples/analysis/emt_n1_full_report_example.py model/holdme/IEEE3 --report=/tmp/emt-n1-full-report.md` | A | 可把已验证筛查路径整理成专题报告和全扫描报告 | 只是 wrapper，不是新求解能力 |

## 作为后续开发清单时，优先怎么看

如果后续要继续做“参数化研究矩阵”，最值得推进的不是再发明新方向，而是沿现有案例库补强这三类东西：

1. 先补 `A` 级案例周围的标准复核命令和输出模板，让后续复核更低成本
2. 把参数化案例库与 `mainline-evidence-register.md`、EMT 验收清单保持同步，避免文档之间再次出现等级漂移
3. 若要新增参数维度，只允许从当前已有案例的相邻维度外扩，且新增条目必须同步补脚本、本地测试、live 证据和边界说明

## 当前不纳入矩阵的方向

以下内容当前不进入参数化研究矩阵：

- IES、SFEMT、实时控制
- 任意模型通用的参数扫描框架
- 发电机 N-1、N-2 或更广义安全平台
- 市场、碳排放、微电网、HVDC、配网重构

## 关联文档

- `docs/guides/emt-mainline-acceptance-checklist.md`
- `docs/guides/mainline-evidence-register.md`
- `docs/guides/mainline-study-scenarios.md`

---

**最后更新**: 2026-03-22
