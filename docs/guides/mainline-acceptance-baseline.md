# 主线验收基线

本文件用于固定当前仓库的主线完成判断，防止后续工作偏离到“补全所有 SDK 方法”。

## 当前结论

截至 `2026-03-23`，仓库的核心目标可以视为已完成：

- 已围绕离线研究闭环组织文档
- 已提供可运行的主线示例
- 已清理主要 fake tests 风险
- 已用真实 CloudPSS API 跑通主线测试
- 已把 EMT 主线进一步收口成结论先行的研究输出与受限 N-1 报告输出

这里说的“核心目标”只指当前主线，不包含 IES、实时仿真、硬件联调等延后方向。

## 主线范围

当前主线闭环限定为：

1. 获取已有算例或本地工作副本
2. 创建研究分支并改模
3. 做拓扑检查
4. 运行潮流并读取结果
5. 把潮流结果写回模型
6. 运行普通云 EMT 并提取波形与消息

对应的可信能力是：

- `Model.fetch` / `Model.fetchMany` / `Model.load` / `Model.dump` / `model.save`
- 元件增删改查，以及 revision 级 `fetchTopology`
- `model.runPowerFlow` 与 `PowerFlowResult`
- `model.runEMT` 与 `EMTResult`

## 已完成内容

文档：

- 研究工作流核心说明
- 建模、潮流、EMT 三条 workflow guide
- `Model` / `Job` / `PowerFlowResult` / `EMTResult` / `Component` 主线 API 文档

示例：

- 研究起点获取与本地工作副本
- 研究分支管理
- 元件修改与拓扑检查
- 潮流试算与结果回写
- IEEE39 检修方式安全校核
- IEEE3 EMT 前置准备
- 普通云 EMT 仿真与波形提取
- IEEE3 EMT 故障研究摘要、故障严重度扫描、故障清除时间扫描
- IEEE3 EMT 量测可观测性工作流
- EMT 研究报告汇总
- IEEE3 EMT N-1 安全筛查
- EMT N-1 代表性专题报告
- EMT N-1 全扫描报告

测试：

- 本地边界测试覆盖主线包装、解析、序列化和脚本防御逻辑
- 真实云端集成测试覆盖 fetch、topology、潮流、普通云 EMT、`model.save()`
- 真实云端集成测试已覆盖 `runPowerFlow()` -> `powerFlowModify()` -> `runEMT()` 的跨工作流闭环
- 真实云端集成测试已覆盖 IEEE39 上“计划停运 + 检修态残余 N-1 复核”的受限校核路径
- 真实云端集成测试已覆盖 IEEE3 EMT 故障研究、量测链整理、代表性 EMT N-1 安全筛查，以及 EMT 研究/报告型 wrapper 的真实串联与 Markdown 导出

当前还应保持一个收紧后的理解：

- `fetchTopology()` 已验证可用于 revision/config 级拓扑展开
- 但不应把它表述成 fetched 工作副本未保存本地改动的最终验证手段

## 证据基线

当前主线完成判断依赖以下证据：

- 本地默认测试：`pytest tests/ -q`
- 标准 live 主线回归：
  `env TEST_SAVE_KEY_PREFIX=study_branch pytest tests/ -q --run-integration -m "integration and not slow_emt"`
- 真实云端完整测试：
  `env TEST_SAVE_KEY_PREFIX=study_branch pytest tests/ -q --run-integration`
- 真实云端定向验证：
  针对高成本 EMT 研究摘要、扫描、N-1 和报告 wrapper，保留 `slow_emt` 分层回归；手工 live 探针记录仅作为补充证据

最近一次已记录的完整结果：

- `178 passed, 145 warnings in 1154.60s (0:19:14)`

2026-03-20 新增的 EMT 研究输出能力，当前证据应这样理解：

- `emt_research_report_example.py`
  有本地边界测试与独立 live 集成测试；可真实串联四条 EMT 研究路径并生成 Markdown 报告
- `emt_n1_security_screening_example.py`
  有本地边界测试、代表性 live 集成测试，以及当天默认 9 个 IEEE3 候选支路的手工 live 全扫描探针
- `emt_n1_security_report_example.py`
  有本地边界测试与独立 live 集成测试；可基于已验证筛查路径输出代表性报告
- `emt_n1_full_report_example.py`
  有本地边界测试与独立 live 集成测试；可基于默认发现到的全部 IEEE3 候选工况输出全扫描报告

说明：

- warnings 来自 SDK 自身 `messageStreamReceiver.py` 的 `setDaemon()` 弃用提示
- 受限沙箱里若 DNS 解析不到 `cloudpss.net`，该次执行不计入 live 验证
- 报告型脚本即使已有独立 live 集成测试，也只能证明“已验证研究路径可以被真实串联并产出报告”，不能被表述成新的广义求解能力
- 完整 live 套件耗时已升到约 19 分钟；当前默认建议先跑 `integration and not slow_emt`，只在 EMT 研究相关改动或正式基线复验时再补跑 `slow_emt` 或完整套件

## 明确未纳入完成度的部分

以下内容可以保留文档或示例，但不影响主线是否完成：

- `model.runSFEMT`
- `model.runThreePhasePowerFlow`
- IES 相关接口
- 实时控制接口：
  `EMTResult.next/goto/send/writeShm/control/monitor/stopSimulation/saveSnapshot/loadSnapshot`
- 硬件联调和设备相关工作流
- 任意模型通用的脚本化故障/示波器配置配方

## 后续只建议做什么

后续工作应限制在以下三类：

- 维护：
  每次改动潮流、EMT、`model.save()`、结果解析后重跑真实云端测试
- 收尾：
  统一文档措辞，避免把本地验证说成 live 行为，并保持案例库、验收清单和证据登记表三份文档同步
- 小幅增强：
  只在现有主线内补充高价值样例、验收清单或证据登记

## 后续不要做什么

除非路线变更，否则不建议再把这些作为当前阶段目标：

- 为了“类完整性”继续铺开冷门 API
- 把 IES、SFEMT、实时仿真重新拉回主线
- 在没有 live 证据时扩大“已验证”表述
- 把 IEEE3 固定故障下的 EMT N-1 结论外推到其他模型、故障位置或更广泛安全判据体系

## 使用方式

以后如果要判断一个新增工作是否值得做，先问两件事：

1. 它是否直接加强“建模 -> 潮流 -> EMT -> 结果提取”主线？
2. 它是否能提供新的真实云端证据，而不是重复本地包装测试？

如果两个问题都不能明确回答“是”，就不应优先进入当前仓库路线。
