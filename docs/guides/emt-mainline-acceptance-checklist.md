# EMT 主线验收清单

本清单用于回答一个更具体的问题：

在当前仓库里，什么情况下才能把一条 EMT 工作线视为“已经进入主线并可对外稳定表述”？

它不是通用 EMT 平台的验收标准，而是当前受限主线的验收标准。

## 适用范围

当前清单只覆盖：

- 普通云 EMT
- `model/holdme/IEEE3`
- 当前仓库已经有 live 证据的故障研究、量测工作流和 EMT N-1 路径

当前不覆盖：

- SFEMT
- 实时控制接口
- 硬件联调
- 任意模型通用的脚本化故障搭建
- 任意模型通用的脚本化量测/输出配置

## 固定边界

在当前 EMT 主线里，以下边界必须被明确写出，不能省略：

### 固定模型

- 主模型：`model/holdme/IEEE3`

### 固定故障链

- 当前已验证故障元件：`_newFaultResistor_3p`
- 当前已验证研究主要围绕同一固定故障路径展开

### 固定监测链

- 已验证的基础监测通道：`Bus7 vac`
- 已验证的补充监测通道：`Bus2`, `Bus8`
- 已验证的支撑诊断通道：`#P1`

### 固定可宣称结论边界

- EMT 故障研究结论只对当前时间窗、当前通道和当前工况集合成立
- EMT N-1 结论只对 `Bus7/Bus2/Bus8 + #P1` 监测链和默认发现到的 `9` 个候选工况成立
- 不把这些结论外推到其他模型、其他故障位置或更广泛安全判据体系

## 验收等级

本清单沿用当前仓库的证据分层：

- `A`
  本地测试 + live 集成测试
- `B`
  本地测试 + 手工 live 探针

对依赖真实云端结论的 EMT 能力，最低要求是：

- `A`
  或
- `B`

如果只有本地测试，不能算通过主线验收。

## 证据填写规则

每个 EMT 主线验收项至少要补齐四类信息：

1. 主入口脚本
2. 本地验证入口
3. live 验证入口
4. 快速复核命令

如果一个条目只能写到第 1 项和第 2 项，它最多只是“脚本已成形”，不是“EMT 主线已验收”。

## 核心验收项

### EMT-01: 最小闭环可运行

必须满足：

- 可从 `examples/basic/ieee3_emt_preparation_example.py` 生成或继承可运行副本
- 可通过 `examples/simulation/run_emt_simulation.py` 真实运行 EMT
- 可在 `EMTResult` 中读到 plots、channel names 和 channel data

当前证据：

- 脚本：`examples/basic/ieee3_emt_preparation_example.py`
- 脚本：`examples/simulation/run_emt_simulation.py`
- 本地验证：`tests/test_examples.py` 中 EMT 示例本地 YAML 入口测试
- live 验证：`tests/test_sdk_api.py` 中 `model/holdme/IEEE3` EMT 前置结构集成验证
- live 验证：`tests/test_emt_result.py::test_ieee3_output_sampling_frequency_changes_trace_resolution`

快速复核：

- `python examples/basic/ieee3_emt_preparation_example.py`
- `python examples/simulation/run_emt_simulation.py examples/basic/ieee3-emt-prepared.yaml`

验收结果：

- 当前已通过

### EMT-02: 故障参数真实进入求解链

必须满足至少一项：

- 固定 `chg` 时，延后 `fe` 会真实改变后故障恢复
- 固定 `fe` 时，改变 `chg` 会真实改变故障中/故障后电压跌落

当前证据：

- 脚本：`examples/analysis/emt_fault_clearing_scan_example.py`
- 脚本：`examples/analysis/emt_fault_severity_scan_example.py`
- 本地验证：`tests/test_examples.py::TestEMTFaultClearingScanExample`
- 本地验证：`tests/test_examples.py::TestEMTFaultSeverityScanExample`
- live 验证：`tests/test_emt_result.py::test_ieee3_fault_clearing_time_change_affects_post_fault_voltage_trace`
- live 验证：`tests/test_emt_result.py::test_ieee3_fault_chg_parameter_changes_fault_depth_and_post_fault_recovery`

快速复核：

- `python examples/analysis/emt_fault_clearing_scan_example.py model/holdme/IEEE3 --csv=/tmp/emt-clearing.csv --conclusion-txt=/tmp/emt-clearing.txt`
- `python examples/analysis/emt_fault_severity_scan_example.py model/holdme/IEEE3 --csv=/tmp/emt-severity.csv --conclusion-txt=/tmp/emt-severity.txt`

验收结果：

- 当前已通过

### EMT-03: 研究型三工况对比可稳定区分

必须满足：

- `baseline / delayed_clearing / mild_fault` 三工况可稳定区分
- 比较口径固定在已验证量测链与固定 RMS 时间窗上
- 结论文本中明确区分“故障更久”和“故障更轻”两类机制

当前证据：

- 脚本：`examples/analysis/emt_fault_study_example.py`
- 本地验证：`tests/test_examples.py::TestEMTFaultStudyExample`
- live 验证：`tests/test_emt_result.py::test_ieee3_fault_study_summary_distinguishes_clearing_time_and_fault_severity`

快速复核：

- `python examples/analysis/emt_fault_study_example.py model/holdme/IEEE3 --csv=/tmp/emt-fault-study.csv --conclusion-txt=/tmp/emt-fault-study.txt`

验收结果：

- 当前已通过

### EMT-04: 量测可观测性工作流成立

必须满足：

- 可复用已有 `Bus7 vac`
- 可新增 `Bus2` 测点并在真实结果中返回波形
- 可裁剪掉 `#Q*` 输出而保留 `#P1`
- 结论文本明确说明当前只对已验证样本和 `_newBus_3p` 配方成立

当前证据：

- 脚本：`examples/basic/emt_voltage_meter_chain_example.py`
- 脚本：`examples/analysis/emt_measurement_workflow_example.py`
- 本地验证：`tests/test_examples.py::TestEMTMeasurementWorkflowExample`
- live 验证：`tests/test_emt_result.py::test_ieee3_measurement_workflow_can_add_prune_and_use_channels_together`
- live 验证：`tests/test_emt_result.py::test_ieee3_can_add_new_voltage_meter_to_bus2_and_match_bus_base_rms`

快速复核：

- `python examples/analysis/emt_measurement_workflow_example.py model/holdme/IEEE3 --csv=/tmp/emt-measurement.csv --conclusion-txt=/tmp/emt-measurement.txt`

验收结果：

- 当前已通过

### EMT-05: EMT N-1 安全筛查成立

必须满足：

- 单支路/单变压器停运通过 `props.enabled=False` 表达
- 固定故障下可形成 `Bus7/Bus2/Bus8 + #P1` 的统一排序口径
- 默认发现到的候选工况总数为 `9`
- 结果中能稳定识别当前最重、最重线路和最轻工况

当前证据：

- 脚本：`examples/analysis/emt_n1_security_screening_example.py`
- 本地验证：`tests/test_examples.py::TestEMTN1SecurityScreeningExample`
- live 验证：`tests/test_emt_result.py::test_ieee3_branch_n1_security_scan_ranks_representative_outages`
- 手工 live 全扫描探针记录：`tests/README.md`

快速复核：

- `python examples/analysis/emt_n1_security_screening_example.py model/holdme/IEEE3 --csv=/tmp/emt-n1.csv --conclusion-txt=/tmp/emt-n1.txt`

验收结果：

- 当前已通过

### EMT-06: 报告型 wrapper 只按包装能力验收

必须满足：

- 研究报告和 N-1 报告只被表述成“已验证路径的汇总包装”
- 文档里不把 wrapper 写成新的求解能力
- 若独立 live 集成测试缺失，必须明确降级为手工 live 探针支撑

当前证据：

- 脚本：`examples/analysis/emt_research_report_example.py`
- 脚本：`examples/analysis/emt_n1_security_report_example.py`
- 脚本：`examples/analysis/emt_n1_full_report_example.py`
- 本地验证：`tests/test_examples.py::TestEMTResearchReportExample`
- 本地验证：`tests/test_examples.py::TestEMTN1SecurityReportExample`
- 本地验证：`tests/test_examples.py::TestEMTN1FullReportExample`
- live 验证：`tests/test_emt_result.py::test_ieee3_research_report_wrapper_aggregates_live_sections_into_markdown`
- live 验证：`tests/test_emt_result.py::test_ieee3_n1_security_report_wrapper_exports_live_representative_markdown`
- live 验证：`tests/test_emt_result.py::test_ieee3_n1_full_report_wrapper_exports_live_full_scan_markdown`
- 历史手工 live 探针记录：`tests/README.md`

快速复核：

- `python examples/analysis/emt_research_report_example.py model/holdme/IEEE3 --report=/tmp/emt-research-report.md`
- `python examples/analysis/emt_n1_security_report_example.py model/holdme/IEEE3 --report=/tmp/emt-n1-security-report.md`
- `python examples/analysis/emt_n1_full_report_example.py model/holdme/IEEE3 --report=/tmp/emt-n1-full-report.md`

验收结果：

- 当前已通过，证据等级是 `A`

## 快速复核顺序

若后续有人要快速确认当前 EMT 主线没有被破坏，建议按这个顺序看：

1. `examples/simulation/run_emt_simulation.py`
   确认最小闭环仍在
2. `examples/analysis/emt_fault_study_example.py`
   确认三工况研究摘要仍成立
3. `examples/analysis/emt_measurement_workflow_example.py`
   确认量测链整理仍成立
4. `examples/analysis/emt_n1_security_screening_example.py`
   确认固定故障下的受限 N-1 排序仍成立
5. `docs/guides/mainline-evidence-register.md`
   确认证据等级和边界没有被写松
6. `docs/guides/parameterized-study-matrix.md`
   确认案例库里的脚本、测试和复核命令仍然对得上

## 失败信号

出现以下任一情况时，不应再把对应能力视为“通过主线验收”：

- 只能跑本地格式化测试，缺少 live 证据
- 换了模型、故障位置或监测链，却继续沿用旧结论
- 把 wrapper 输出说成新的 EMT 求解能力
- 把 `_newBus_3p` 已验证配方外推成任意母线通用配方
- 把 `Bus7/Bus2/Bus8 + #P1` 的 EMT N-1 结论外推成通用安全判据

## 与参数化研究矩阵的关系

本清单回答的是“什么算通过验收”。

如果问题是“当前已经有哪些已验证参数维度可以继续做研究扩展”，应看：

- `docs/guides/parameterized-study-matrix.md`

---

**最后更新**: 2026-03-22
