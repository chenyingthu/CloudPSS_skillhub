# 主线证据登记表

本文件把当前主线能力与其证据来源并排登记，目的是防止两个常见问题：

1. 把本地边界测试说成真实云端行为
2. 把手工 live 探针说成完整 live 集成覆盖

## 使用规则

阅读本表时，先区分三类证据：

- `本地测试`
  只能证明脚本逻辑、参数解析、格式化、序列化或 SDK 本地包装行为
- `live 集成测试`
  证明真实 CloudPSS API 与云端任务行为
- `手工 live 探针`
  证明某条高成本研究路径在真实云端可跑通，但通常不代表它已进入标准 live 套件的常规覆盖

一个能力若依赖真实云端结论，至少需要：

- `live 集成测试`
  或
- 已明确记录的 `手工 live 探针`

如果两者都没有，就不应把该能力描述成“已验证的 live 主线”。

## 证据等级

| 等级 | 含义 |
|------|------|
| A | 本地测试 + live 集成测试 |
| B | 本地测试 + 手工 live 探针 |
| C | live 集成测试为主，脚本本地边界覆盖不是主要证据 |
| L | 仅本地测试；不能宣称真实云端行为 |

## 主线登记

| 主线能力 | 主要脚本/入口 | 本地测试 | live 集成测试 | 手工 live 探针 | 等级 | 当前边界 |
|------|------|------|------|------|------|------|
| 研究起点与工作副本 | `examples/basic/model_fetch_example.py`, `examples/basic/model_save_dump_example.py` | `tests/test_sdk_api.py`, `tests/test_examples.py` | `tests/test_sdk_api.py` | 无需额外探针 | A | 以 `model/holdme/IEEE39` 与 `model/holdme/IEEE3` 为主要已验证起点 |
| 元件增删改查与拓扑检查 | `examples/basic/component_example.py`, `examples/basic/revision_example.py` | `tests/test_sdk_api.py`, `tests/test_examples.py` | `tests/test_sdk_api.py` | 无需额外探针 | A | `fetchTopology()` 只证明 revision/config 级展开，不单独证明未保存本地改动已进入求解器 |
| 潮流运行与结果回写 | `examples/simulation/run_powerflow.py` | `tests/test_examples.py`, `tests/test_powerflow_result.py` | `tests/test_powerflow_result.py` | 包含在完整 live 套件记录中 | A | 主线以 IEEE39 为主，不外推到任意模型 |
| IEEE39 工程化潮流研究 | `examples/analysis/powerflow_engineering_study_example.py`, `examples/analysis/powerflow_batch_study_example.py` | `tests/test_examples.py` | `tests/test_powerflow_result.py` | 相关定向回归记录在 `tests/README.md` | A | 只对当前已验证工况集合成立 |
| IEEE39 全网支路 N-1 潮流筛查 | `examples/analysis/powerflow_n1_screening_example.py` | `tests/test_examples.py` | `tests/test_powerflow_result.py` | 相关定向回归与全网筛查记录在 `tests/README.md` | A | 只对 IEEE39 基线在役 `43` 条支路集合成立 |
| IEEE39 检修方式安全校核 | `examples/analysis/powerflow_maintenance_security_example.py` | `tests/test_examples.py` | `tests/test_powerflow_result.py` | 当前定向集成测试记录在 `tests/README.md` | A | 只对 IEEE39、`line-26-28` 与变压器 `canvas_0_47` 计划停运样例、以及检修态下剩余已验证子集成立 |
| IEEE3 EMT 最小闭环 | `examples/basic/ieee3_emt_preparation_example.py`, `examples/simulation/run_emt_simulation.py` | `tests/test_examples.py`, `tests/test_emt_result.py` | `tests/test_sdk_api.py`, `tests/test_emt_result.py` | 包含在完整 live 套件记录中 | A | 只覆盖普通云 EMT，不含 SFEMT/实时控制/硬件联调 |
| IEEE3 EMT 故障研究摘要 | `examples/analysis/emt_fault_study_example.py` | `tests/test_examples.py` | `tests/test_emt_result.py` | 定向回归记录在 `tests/README.md` | A | 只对 `baseline / delayed_clearing / mild_fault`、固定量测链和时间窗成立 |
| IEEE3 EMT 故障清除时间扫描 | `examples/analysis/emt_fault_clearing_scan_example.py` | `tests/test_examples.py` | `tests/test_emt_result.py` | 定向回归记录在 `tests/README.md` | A | 只对 IEEE3、固定故障深度与既定观察时刻成立 |
| IEEE3 EMT 故障严重度扫描 | `examples/analysis/emt_fault_severity_scan_example.py` | `tests/test_examples.py` | `tests/test_emt_result.py` | 定向回归记录在 `tests/README.md` | A | 只对 IEEE3 与固定 `_newFaultResistor_3p` 路径成立 |
| EMT 量测可观测性工作流 | `examples/basic/emt_voltage_meter_chain_example.py`, `examples/analysis/emt_measurement_workflow_example.py` | `tests/test_examples.py` | `tests/test_emt_result.py` | 相关定向回归记录在 `tests/README.md` | A | 受限于 `_newBus_3p` 母线和当前已验证样本 |
| EMT 研究报告汇总 | `examples/analysis/emt_research_report_example.py` | `tests/test_examples.py` | `tests/test_emt_result.py::test_ieee3_research_report_wrapper_aggregates_live_sections_into_markdown` | 历史定向探针记录见 `tests/README.md` | A | 只证明四条已验证 EMT 路径可真实串联并输出 Markdown 报告，不代表新增求解能力 |
| IEEE3 EMT N-1 安全筛查 | `examples/analysis/emt_n1_security_screening_example.py` | `tests/test_examples.py` | `tests/test_emt_result.py` | `python examples/analysis/emt_n1_security_screening_example.py model/holdme/IEEE3 --csv=/tmp/emt-n1-security-screening.csv --conclusion-txt=/tmp/emt-n1-security-screening.txt` | A | 只对 `model/holdme/IEEE3`、固定 `_newFaultResistor_3p`、`Bus7/Bus2/Bus8 + #P1`、默认 9 个候选工况成立 |
| EMT N-1 代表性专题报告 | `examples/analysis/emt_n1_security_report_example.py` | `tests/test_examples.py` | `tests/test_emt_result.py::test_ieee3_n1_security_report_wrapper_exports_live_representative_markdown` | 历史定向探针记录见 `tests/README.md` | A | 只证明已验证筛查路径可整理成代表性报告，不外推到其他模型或判据 |
| EMT N-1 全扫描报告 | `examples/analysis/emt_n1_full_report_example.py` | `tests/test_examples.py` | `tests/test_emt_result.py::test_ieee3_n1_full_report_wrapper_exports_live_full_scan_markdown` | 历史定向探针记录见 `tests/README.md` | A | 只证明默认发现到的全部 IEEE3 候选工况可被真实串联并输出报告 |

## 当前基线记录

- 本地默认测试：
  `pytest tests/ -q`
- 最近一次完整 live 套件记录：
  `env TEST_SAVE_KEY_PREFIX=study_branch pytest tests/ -q --run-integration`
  -> `178 passed, 145 warnings in 1154.60s (0:19:14)`

## `cloudpss_skills_v2` 证据补充

这部分证据只针对 v2 skills，不替代上面的旧主线 CloudPSS SDK/workflow
基线。

| v2 能力 | 主要入口 | 本地/CI-safe 测试 | 私有 live 测试 | 等级 | 当前边界 |
|------|------|------|------|------|------|
| 注册技能可运行矩阵 | `cloudpss_skills_v2/tests/test_integration_registry_matrix.py` | 默认运行 46 个本地/pandapower/数据处理条目；live-only 条目无 token/网络时 skip | 有 `.cloudpss_token_internal` 和 `http://166.111.60.76:50001` 时 48 个注册 skill 全部通过 | A/L 混合 | 证明每个注册 skill 有最小真实路径；不等价于所有算法完成工程级正确性审查 |
| v2 live CloudPSS adapter 路径 | `test_integration_cloudpss.py`, `test_integration_local_server.py`, `test_integration_poweranalysis.py` | 不作为默认 CI 要求 | 本地服务器完整路径通过，最近记录为 v2 全量 `832 passed, 3 skipped` 的一部分 | A | 只针对 `166.111.60.76:50001`，不覆盖公网或 `internal.cloudpss.com` |
| fake/smoke 测试防回归 | `test_integration_quality_gate.py` | `rg` 检查与 pytest 质量门 | 不需要 live | L | 只防止弱标记回流；不能单独证明功能正确 |
| DataLib 转换 | `test_integration_datalib.py` | pandapower `case14` 真实结果转 `BusData`/`BranchData`/`NetworkSummary` | 不需要 live | L | 证明转换链路和字段映射，不证明 CloudPSS 数据全覆盖 |

最新 v2 验证命令：

```bash
python -m compileall -q cloudpss_skills_v2
rg -n "pytest\\.mark\\.(smoke|needs_improvement)|smoke:|needs_improvement:" cloudpss_skills_v2/tests pytest.ini
timeout 300s python -m pytest -q cloudpss_skills_v2/tests/test_integration_cloudpss.py cloudpss_skills_v2/tests/test_integration_quality_gate.py
timeout 600s python -m pytest -q cloudpss_skills_v2/tests
```

最新记录：

- `timeout 600s python -m pytest -q cloudpss_skills_v2/tests`
  -> `832 passed, 3 skipped, 210 warnings in 195.28s`

## 使用建议

后续如果新增一个主线能力，更新本表时至少要补齐这四项：

1. 入口脚本或主要代码路径
2. 本地测试是否覆盖
3. live 集成测试是否覆盖
4. 若只靠手工 live 探针成立，必须把命令和边界写明

如果第 3 项和第 4 项都为空，该能力不能被登记为 live 主线能力。

## 维护约束

- 不把 monkeypatch、本地 fixture、格式化测试写成 live 证据
- 不把手工 live 探针写成“标准 live 套件已覆盖”
- 不把 IEEE3 固定故障下的 EMT N-1 结论外推到其他模型、故障位置或更广泛安全判据
- 若后续完整 live 套件结果更新，应同步更新本文件和 `mainline-acceptance-baseline.md`

---

**最后更新**: 2026-03-23
