# 当前主线用户故事

本文件只保留与当前仓库主线一致、且已经有代码与证据落地的用户故事。

## M-01: 从已知模型建立研究起点

- 用户角色：研究工程师
- 目标：从已验证可访问的 CloudPSS 模型或本地工作副本开始一轮研究
- 当前落地：
  `examples/basic/model_fetch_example.py`
  `examples/basic/model_save_dump_example.py`
- 当前证据：
  `tests/test_sdk_api.py`
- 可信边界：
  研究起点以 `model/holdme/IEEE39` 与 `model/holdme/IEEE3` 为主，不外推到任意默认模型

## M-02: 在本地工作副本上持续改模

- 用户角色：研究工程师
- 目标：在不污染原始算例的前提下创建、保存、恢复研究分支
- 当前落地：
  `examples/basic/model_save_dump_example.py`
  `examples/basic/component_example.py`
- 当前证据：
  `tests/test_sdk_api.py`
- 可信边界：
  `model.save()` live 写入是 opt-in；默认主线仍以本地工作副本为主

## M-03: 修改元件并做拓扑检查

- 用户角色：模型维护人员
- 目标：完成元件增删改查，并确认 revision 级拓扑可展开
- 当前落地：
  `examples/basic/component_example.py`
  `examples/basic/revision_example.py`
- 当前证据：
  `tests/test_sdk_api.py`
- 可信边界：
  `fetchTopology()` 只能证明 revision/config 级拓扑展开，不应单独拿来证明未保存本地改动已进入求解器

## P-01: 对 IEEE39 做工程化潮流研究

- 用户角色：方式或规划工程师
- 目标：在一个可信基线上比较负荷、线路、机组设定和无功压力工况
- 当前落地：
  `examples/analysis/powerflow_engineering_study_example.py`
  `examples/analysis/powerflow_batch_study_example.py`
- 当前证据：
  `tests/test_powerflow_result.py`
- 可信边界：
  结论只对当前已验证的 IEEE39 工况集合成立

## P-02: 对 IEEE39 做全网支路 N-1 潮流筛查

- 用户角色：安全分析工程师
- 目标：在潮流层面对基线在役线路和变压器支路形成统一严重性排序
- 当前落地：
  `examples/analysis/powerflow_n1_screening_example.py`
- 当前证据：
  `tests/test_powerflow_result.py`
- 可信边界：
  当前只对 IEEE39 基线在役支路集合宣称成立

## P-03: 对 IEEE39 做检修方式安全校核

- 用户角色：运行方式或检修校核工程师
- 目标：先建立一个计划停运工况，再在该检修态上继续做受限 N-1 复核
- 当前落地：
  `examples/analysis/powerflow_maintenance_security_example.py`
- 当前证据：
  `tests/test_examples.py`
  `tests/test_powerflow_result.py`
- 可信边界：
  当前只对 IEEE39、`line-26-28` 与变压器 `canvas_0_47` 计划停运样例、以及检修态下剩余已验证子集宣称成立，不等价于完整检修校核平台

## E-01: 运行 IEEE3 EMT 最小闭环

- 用户角色：EMT 研究人员
- 目标：从已准备好的 IEEE3 研究副本运行普通云 EMT 并提取波形
- 当前落地：
  `examples/basic/ieee3_emt_preparation_example.py`
  `examples/simulation/run_emt_simulation.py`
- 当前证据：
  `tests/test_sdk_api.py`
  `tests/test_emt_result.py`
- 可信边界：
  当前主线只覆盖普通云 EMT，不包含 SFEMT、实时控制或硬件联调

## E-02: 比较 IEEE3 代表性故障工况

- 用户角色：暂态稳定研究人员
- 目标：比较基线故障、延迟切除和较轻故障三工况，并形成定量结论
- 当前落地：
  `examples/analysis/emt_fault_study_example.py`
- 当前证据：
  `tests/test_emt_result.py`
- 可信边界：
  结论只对当前固定故障位置、固定量测链和固定时间窗成立

## E-03: 扫描故障清除时间

- 用户角色：暂态稳定研究人员
- 目标：比较 `fe` 延后时后故障恢复缺口如何单调恶化
- 当前落地：
  `examples/analysis/emt_fault_clearing_scan_example.py`
- 当前证据：
  `tests/test_emt_result.py`
- 可信边界：
  当前只对 IEEE3、固定故障深度与既定观察时刻成立

## E-04: 扫描故障严重度

- 用户角色：暂态稳定研究人员
- 目标：比较不同 `chg` 点下故障跌落和恢复缺口的排序
- 当前落地：
  `examples/analysis/emt_fault_severity_scan_example.py`
- 当前证据：
  `tests/test_emt_result.py`
- 可信边界：
  当前只对 IEEE3 与固定 `_newFaultResistor_3p` 研究路径成立

## E-05: 整理 EMT 量测可观测性

- 用户角色：EMT 研究人员
- 目标：复用已有测点、补挂 Bus2 测点、裁剪输出组，并形成联合结论
- 当前落地：
  `examples/basic/emt_voltage_meter_chain_example.py`
  `examples/analysis/emt_measurement_workflow_example.py`
- 当前证据：
  `tests/test_emt_result.py`
- 可信边界：
  当前只对 `_newBus_3p` 母线和仓库已验证样本宣称成立

## E-06: 输出 EMT 研究汇总报告

- 用户角色：研究工程师
- 目标：把故障研究、清除时间扫描、严重度扫描和量测工作流汇总成一份 Markdown 报告
- 当前落地：
  `examples/analysis/emt_research_report_example.py`
- 当前证据：
  `tests/test_examples.py`
  `tests/test_emt_result.py`
- 可信边界：
  这是对已验证研究路径的汇总包装，不应被表述成独立扩展出的新求解能力

## E-07: 对 IEEE3 做 EMT N-1 安全筛查

- 用户角色：安全分析工程师
- 目标：在固定故障下枚举单支路停运，并按多母线恢复缺口和 `#P1` 支撑读数形成排序
- 当前落地：
  `examples/analysis/emt_n1_security_screening_example.py`
- 当前证据：
  `tests/test_emt_result.py`
  手工 live 全扫描探针已记录在 `tests/README.md`
- 可信边界：
  当前只对 `model/holdme/IEEE3`、固定 `_newFaultResistor_3p`、`Bus7/Bus2/Bus8 + #P1` 监测链、以及默认 9 个候选工况成立

## E-08: 输出 EMT N-1 代表性报告与全扫描报告

- 用户角色：研究工程师或评审汇报人员
- 目标：把已验证的 EMT N-1 路径整理成专题报告和全扫描报告
- 当前落地：
  `examples/analysis/emt_n1_security_report_example.py`
  `examples/analysis/emt_n1_full_report_example.py`
- 当前证据：
  `tests/test_examples.py`
  `tests/test_emt_result.py`
- 可信边界：
  这是基于已验证筛查路径的报告包装，不应外推到其他模型、故障位置或更广泛安全判据体系

## 当前最值得继续增强的故事

如果后续继续扩主线，优先级最高的不是再发明新方向，而是：

1. 若再新增研究型 story，优先落到 `docs/guides/parameterized-study-matrix.md` 已有的相邻参数维度
2. 把案例库、验收清单和证据登记表继续保持同步，避免文档等级漂移
3. 在不扩大宣称边界的前提下，把现有 Markdown/CSV/digest 研究输出进一步统一成更稳定的摘要模板
