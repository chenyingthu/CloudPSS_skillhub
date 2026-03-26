# CloudPSS SDK 测试配置

本目录包含两类测试：
- 默认单元测试：不访问 CloudPSS 网络服务，验证本地可复现的 SDK 行为。
- 集成测试：真实调用 CloudPSS API，需要 token，并且要显式开启。

## 测试文件

| 文件 | 说明 |
|------|------|
| `test_examples.py` | 示例脚本的本地边界测试 |
| `test_sdk_api.py` | SDK 本地边界测试，以及模型/任务主线集成测试 |
| `test_emt_result.py` | EMT 仿真结果测试 |
| `test_powerflow_result.py` | 潮流计算结果测试 |

## 运行测试

### 使用 pytest (推荐)

```bash
# 运行默认测试（不联网）
pytest tests/ -q

# 运行标准 live 主线回归（排除高成本 slow_emt）
pytest tests/ -q --run-integration -m "integration and not slow_emt"

# 运行全部真实 CloudPSS 集成测试
pytest tests/ -q --run-integration -m integration

# 单独运行慢速 EMT 研究/报告回归
pytest tests/test_emt_result.py -q --run-integration -m "integration and slow_emt"

# 显式启用 model.save() live 写入测试
TEST_SAVE_KEY_PREFIX=study_branch pytest tests/ -q --run-integration -m "integration and not slow_emt"
TEST_SAVE_KEY_PREFIX=study_branch pytest tests/ -q --run-integration -m integration

# 本地单元测试覆盖率
pytest tests/ --cov=cloudpss --cov-report=term-missing -m "not integration"
```

### 按文件运行

```bash
pytest tests/test_sdk_api.py -q
pytest tests/test_emt_result.py -q
pytest tests/test_powerflow_result.py -q
```

## 配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `CLOUDPSS_TOKEN` | API Token | 从 `.cloudpss_token` 读取 |
| `TEST_MODEL_RID` | 集成测试模型 ID | `model/holdme/IEEE39` |
| `TEST_SAVE_KEY_PREFIX` | `model.save()` live 写入测试用的一次性 key 前缀 | 未设置时跳过该测试 |

### 配置文件

测试配置在 `tests/conftest.py` 顶部:

```python
DEFAULT_TEST_MODEL_RID = os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39")
```

## 证据边界

本目录里的测试结论必须按来源解释：

- `本地测试` 只能证明 SDK 本地包装、解析、序列化和脚本级防御逻辑
- `集成测试` 才能证明真实 CloudPSS API 和云端任务行为

禁止混淆的几种情况：

- 不能把 monkeypatch/本地 fixture 的结果描述成 live API 结构
- 不能把 SDK 源码签名直接当作服务端返回事实
- 不能把受限沙箱里 DNS 失败、连不上 `cloudpss.net` 的尝试记成“已完成云端验证”

### 默认单元测试
- 不需要真实 API token
- 使用真实 SDK 类，但只喂本地数据
- 不使用 `Mock(spec=...)` 做“方法存在即通过”的伪测试
- 不把 monkeypatch 边界测试描述成真实 CloudPSS 行为验证

### 集成测试
- 需要真实 API token
- 需要显式传 `--run-integration`
- 实际调用 CloudPSS 服务
- 当前已验证可访问的默认模型是 `model/holdme/IEEE39`
- `model.save()` 的 live 写入测试是显式 opt-in 的；只有设置 `TEST_SAVE_KEY_PREFIX` 才会创建一次性研究分支
- 只有真实连通 `cloudpss.net` 的执行结果才计入 live 验证
- 当前按成本分两层：
  - `integration and not slow_emt`：标准 live 主线回归，优先用于日常改动后快速确认主线没坏
  - `integration and slow_emt`：高成本 EMT 研究/报告回归，优先用于 EMT 研究脚本、N-1 路径和报告 wrapper 相关改动

### 仓库红线

- 不新增 fake tests
- 不新增 `model/CloudPSS/example-*` 之类不可验证的默认模型
- 只要结论依赖真实 CloudPSS 返回，就必须通过集成测试、真实探针或已记录的 live 验证支撑
- 本地测试可以验证 SDK 的包装、解析、序列化和参数拼装，但不能冒充 live coverage

### 跳过条件
- 未传 `--run-integration` 时跳过所有集成测试
- 未配置 API token 时跳过集成测试

## 覆盖率目标

使用 `pytest-cov`:

```bash
# 目标: 行覆盖率 > 70%
pytest tests/ --cov=cloudpss --cov-report=term-missing --cov-fail-under=70
```

## 测试类说明

### test_sdk_api.py
- 本地 Model 组件增删改查
- 本地 `Model.fetchMany()` 参数组装与错误透传
- 本地 dump/load 往返
- 本地 `ModelRevision.create()` / `ModelRevision.run()` 边界测试
- 本地 `Job.abort()` / `Job.dump()` / `Job.load()` 边界测试
- 真实 `Model.fetch()` / `Model.fetchMany()` / `ModelRevision.fetchTopology()` / `Job.fetch()` 集成测试
- 真实模型本地工作副本上的元件添加、更新、删除，以及 `powerFlow` 拓扑拉取边界测试
- 真实确认：fetched 工作副本上的未保存本地新增元件不会直接出现在 `fetchTopology()` 返回里
- 真实 `model/holdme/IEEE3` EMT 前置结构集成验证：故障元件、量测信号、输出通道和 EMT 方案输出分组链路
- 可选的 `model.save('new-key')` disposable branch 集成测试

### test_emt_result.py
- 本地 `EMTResult` 波形合并与通道访问
- 真实 EMT 仿真结果集成测试
- 真实 `IEEE3` 本地准备副本 `dump -> load -> runEMT -> result` 闭环验证
- 真实 `IEEE3` 故障清除时间敏感性验证：延长 `fe` 后，后故障电压波形出现可解释偏移
- 真实 `IEEE3` 输出采样频率验证：`1000` 与 `2000` 采样下的点数和时间分辨率按预期变化
- 真实 `IEEE3` 故障参数 `chg` 灵敏度验证：扩大参数范围后，故障中/故障后电压跌落深度按工况明显变化
- 真实 `IEEE3` 故障研究摘要验证：`baseline / delayed_clearing / mild_fault` 三工况可稳定区分“故障更久”和“故障更轻”对 `plot-2 / vac:0` RMS 恢复指标的不同影响
- 真实 `IEEE3` 跨工作流闭环验证：负荷扰动先经 `runPowerFlow()` + `powerFlowModify()` 回写，再进入 EMT，故障前机端功率通道落到新的稳态工作点
- 真实 `IEEE3` 量测与输出通道改配验证：量测信号/通道重命名会进入结果通道名，输出分组裁剪会真实减少返回通道
- 真实 `IEEE3` 新增输出通道验证：可对既有量测信号 `#vac` 新增 `vac_copy` 通道，并在真实 EMT 结果中返回复制波形
- 真实 `IEEE3` 新增量测元件验证：在新增 `_NewVoltageMeter` 的同时克隆 meter->bus 的 `diagram-edge`，可稳定返回 `vac_added:*` 波形
- 真实 `IEEE3 Bus2` 新增量测元件验证：换一条母线后，新增 `bus2_added:*` 通道的稳态 RMS 与 `V_pu * VBase / sqrt(3)` 一致
- 真实 `IEEE39 bus37` 新增量测元件验证：即使原模型没有现成电压表模板，直接构造 generic `diagram-edge` 也能稳定返回 `bus37_added:*` 波形，并满足同样的 RMS 判据
- 真实 `IEEE3` EMT N-1 安全筛查验证：在代表性 `Trans1 / tline4 / tline6` 单停运工况上，固定故障下的 `Bus7/Bus2/Bus8` 恢复缺口和 `#P1` 支撑读数可形成稳定排序与研究结论
- 真实 `IEEE3` EMT 研究报告 wrapper 验证：可把四条已验证 EMT 路径真实串联成 Markdown 报告并导出文件
- 真实 `IEEE3` EMT N-1 代表性报告 wrapper 验证：可把 `Trans1 / tline4 / tline6` 代表性工况整理成 Markdown 报告并导出文件
- 真实 `IEEE3` EMT N-1 全扫描报告 wrapper 验证：可把默认 `9` 个候选工况整理成全扫描 Markdown 报告并导出文件
- 其中高成本 EMT 研究摘要、扫描、量测工作流、N-1 排序和报告 wrapper 已统一打上 `slow_emt` marker，避免默认 live 主线每次都跑满整套慢测试

### test_examples.py
- `run_emt_simulation.py` 的本地 YAML 入口测试
- `Job` 缺少 `name` 属性时的脚本级防御性边界测试
- `run_powerflow.py` 的本地 YAML 入口和表头字段兼容测试
- `powerflow_engineering_study_example.py` 的本地 YAML 入口，以及线路切除/电压控制/有功再调度摘要函数测试
- `powerflow_batch_study_example.py` 的本地 YAML 入口，以及多工况指标提取/汇总格式化测试
- `powerflow_n1_screening_example.py` 的本地 YAML 入口，以及候选支路发现、基线缺席组件过滤、CSV 导出、全网支路 N-1 指标提取、严重性分类与筛查摘要格式化测试
- `powerflow_maintenance_security_example.py` 的本地 YAML 入口、检修态候选支路过滤、摘要 CSV、结论生成和参数解析测试
- `emt_fault_study_example.py` 的本地 YAML 入口，以及 EMT 故障研究摘要指标提取/格式化测试
- `emt_fault_study_example.py` 的 `--csv=` 参数和 CSV 导出测试
- `emt_fault_study_example.py` 的 `--waveform-csv=` 参数和对比波形 CSV 导出测试
- `emt_fault_study_example.py` 的 `--waveform-window=` 参数和时间窗裁剪导出测试
- `emt_fault_study_example.py` 的结论报告生成、结论路径派生和 `--conclusion-txt=` 参数测试
- `emt_measurement_workflow_example.py` 的本地 YAML 入口、量测工作流摘要导出、结论生成和参数解析测试
- `emt_fault_clearing_scan_example.py` 的本地 YAML 入口、扫描摘要导出、单调性结论和参数解析测试
- `emt_fault_severity_scan_example.py` 的本地 YAML 入口、扫描摘要导出、结论生成和参数解析测试
- `emt_n1_security_screening_example.py` 的本地 YAML 入口、候选支路选择、排序/摘要、结论生成和参数解析测试
- `emt_n1_security_report_example.py` 的参数解析、Markdown 报告拼装和导出测试
- `emt_n1_full_report_example.py` 的参数解析、全扫描 Markdown 报告拼装和导出测试
- `emt_research_report_example.py` 的参数解析、Markdown 表格拼装、四段报告汇总和报告文件导出测试
- `model_save_dump_example.py` 的本地 YAML 入口、导出路径传递和缺省 description 边界测试
- `model_save_dump_example.py` 对本地输入源生成安全默认 `*-branch.yaml` 路径的测试
- `component_example.py` 的本地 YAML 入口和安全输出路径测试
- `emt_voltage_meter_chain_example.py` 的本地 YAML 入口、工作副本路径保护，以及 template/generic `diagram-edge` 两条注入路径测试
- `model_fetch_example.py` 的本地 YAML 入口和安全工作副本路径测试
- `revision_example.py` 的本地 YAML 入口测试
- `run_sfemt_simulation.py` / `run_ies_simulation.py` 的 plot 标签优先级防御性测试
- `run_ies_simulation.py` 只把当前 SDK `runIES*()` 默认接受的 `job-definition/ies/*` RID 识别为可运行入口

### test_powerflow_result.py
- 本地 `PowerFlowResult` 表格解析与 `powerFlowModify`
- 真实潮流结果集成测试，包括 `powerFlowModify()` 对 live 结果的本地回写验证
- 真实本地 YAML 工作副本 `dump -> load -> runPowerFlow -> result` 闭环验证
- 真实 `IEEE39` 负荷扰动再平衡验证：提高 `load-39` 后，同母线平衡出力同步抬升
- 真实 `powerFlowModify()` 二次试算一致性验证：回写后的模型重跑潮流，关键母线结果保持稳定
- 真实 `IEEE39` 线路电抗扰动验证：提高 `line-26-28` 的 `X1pu` 后，目标支路传输和相邻母线状态出现可解释变化
- 真实 `IEEE39` 线路切除验证：移除 `line-26-28` 后，`line-26-29` 与 `line-28-29` 走廊出现明显潮流再分布，切除支路两端母线状态发生可解释偏移
- 真实 `IEEE39` 停运语义等价性验证：`line-26-28` 与变压器 `canvas_0_47` 上 `props.enabled=False` 与 `removeComponent()` 的潮流停运结果一致
- 真实 `IEEE39` 电压控制验证：提高 `Gen30` 的 `pf_V` 后，机端母线电压和机组无功支撑同步上升，邻近母线电压也出现可解释提升
- 真实 `IEEE39` 机组再调度验证：提高 `Gen38` 的 `pf_P` 后，平衡机组出力回落，关键送电走廊有功传输幅值明显抬升
- 真实 `IEEE39` 负荷中心转移验证：将 `load-39` 的 `200 MW / 60 MVar` 转到 `load-21` 后，`bus21` 电压下探，`line-21-22` 增载，`line-22-23/23-24` 走廊同步卸载
- 真实 `IEEE39` 无功压力验证：将 `load-21` 的无功从 `115` 提到 `215 MVar` 后，`bus21` 电压明显下探，平衡机组与远端发电机群无功支撑同步抬升，而关键有功走廊幅值只小幅变化
- 真实 `IEEE39` 多工况研究汇总验证：`baseline / load_up / line_x_up / line_outage / gen30_v_up / gen38_p_up / load_shift_39_to_21 / load21_q_up` 八个工况能够生成一份方向正确的潮流研究摘要
- 真实 `IEEE39` 全网支路 N-1 筛查验证：全部 `43` 条基线在役支路可依次通过 `props.enabled=False` 停运，并按相对基线新增越限、最低电压、缺失母线、最大电压/潮流偏移形成严重性排序与工程 digest
- 真实 `IEEE39` 检修方式安全校核验证：先停运 `line-26-28` 或变压器 `canvas_0_47`，再对检修态下剩余已验证子集继续停运，仍可形成稳定的残余 N-1 排序与结论

## 常见问题

### 1. 集成测试认证失败
```
错误: missing CloudPSS token for integration tests
```
- 检查 `.cloudpss_token` 文件是否存在
- 检查 `CLOUDPSS_TOKEN` 是否已设置
- 注意：`setToken()` 只负责写入环境变量，不会在调用时主动校验 token 有效性

### 2. 模型获取失败
```
错误: 获取模型失败: ...
```
- 检查 `TEST_MODEL_RID` 是否正确
- 确认模型存在且有访问权限
- 仓库里不再内置 `model/CloudPSS/example-*` 这类不可验证的默认值

### 3. 仿真超时
```
状态: 超时 (状态=0)
```
- 增加超时时间
- 检查网络连接

### 4. 结果为空
```
波形数量: 0
```
- 确认仿真已完成 (`job.status() == 1`)
- 检查项目是否有输出配置

## 更新日志

- 2026-03-16: 初始版本
  - 重构为默认单元测试 + 显式集成测试
  - 移除 fake tests
  - 使用 `--run-integration` 控制真实 CloudPSS 调用
- 2026-03-16: 主线覆盖增强
  - 新增 `Model.fetchMany()` 本地边界测试
  - 新增 `PowerFlowResult.powerFlowModify()` 真实集成验证
  - 明确 `model.save()` live 写入测试需通过 `TEST_SAVE_KEY_PREFIX` 显式 opt-in
- 2026-03-17: 证据边界收紧
  - 明确区分本地边界验证与真实云端验证
  - 记录完整 live 套件在真实联网环境下通过：`env TEST_SAVE_KEY_PREFIX=study_branch pytest tests/ -q --run-integration` -> `75 passed, 6 warnings`
- 2026-03-17: 第三批主线研究场景
  - 新增 `IEEE39` 线路电抗扰动导致潮流再分布的真实集成验证
  - 新增 `IEEE3` 故障参数 `chg` 灵敏度的真实集成验证
  - 更新完整 live 套件结果：`env TEST_SAVE_KEY_PREFIX=study_branch pytest tests/ -q --run-integration` -> `81 passed, 15 warnings`
- 2026-03-17: 跨工作流闭环补强
  - 新增 `IEEE3` 上 `runPowerFlow()` -> `powerFlowModify()` -> `runEMT()` 的真实集成验证
  - 更新完整 live 套件结果：`env TEST_SAVE_KEY_PREFIX=study_branch pytest tests/ -q --run-integration` -> `82 passed, 19 warnings`
- 2026-03-17: 量测与输出通道改配补强
  - 新增 `IEEE3` 量测信号/输出通道重命名的真实集成验证
  - 新增 `IEEE3` 输出分组裁剪到仅保留 `#P*` 通道的真实集成验证
  - 更新完整 live 套件结果：`env TEST_SAVE_KEY_PREFIX=study_branch pytest tests/ -q --run-integration` -> `84 passed, 23 warnings`
- 2026-03-17: 新增输出通道补强
  - 新增 `IEEE3` 上基于既有量测信号 `#vac` 创建 `vac_copy` 输出通道的真实集成验证
  - 更新完整 live 套件结果：`env TEST_SAVE_KEY_PREFIX=study_branch pytest tests/ -q --run-integration` -> `85 passed, 25 warnings`
- 2026-03-18: 新增量测元件补强
  - 新增 `IEEE3` 上 `_NewVoltageMeter` + `_newChannel` + meter->bus `diagram-edge` 的真实集成验证
  - 明确当前 SDK 公开 API 仍无高层 `addEdge()`，该能力依赖底层 `diagram.cells` 注入
- 2026-03-18: 新增量测元件可迁移性补强
  - 新增 `IEEE3 Bus2` 上换母线复验，确认该配方不只对 `Bus7` 偶然成立
  - 新增 `IEEE39 bus37` 上无现成电压表模板的复验，确认 generic `diagram-edge` scaffold 也可成立
- 2026-03-20: EMT 研究报告级输出补充
  - 新增 `emt_research_report_example.py` 的本地边界测试，覆盖参数解析、Markdown 汇总和导出逻辑
  - 当天手工 live 探针已验证 `python examples/analysis/emt_research_report_example.py model/holdme/IEEE3 --report=/tmp/emt-research-report.md` 可真实串联四条 EMT 研究路径并生成 Markdown 报告
  - 当时尚未为该脚本新增独立集成测试，以避免在标准 live 套件里重复触发四段高成本 EMT 研究任务
  - 相关定向回归：`pytest tests/test_emt_result.py -q --run-integration -k 'new_output_channel_for_existing_meter_signal or new_voltage_meter_when_meter_bus_edge_is_injected or bus2_and_match_bus_base_rms or without_existing_meter_template'` -> `4 passed, 22 deselected, 6 warnings`
- 2026-03-20: EMT N-1 安全筛查补充
  - 新增 `emt_n1_security_screening_example.py`，把 `IEEE3` 上的线路/变压器单停运扫描、`Bus7/Bus2/Bus8` 多测点恢复缺口和 `#P1` 支撑读数组合成一条 EMT 安全筛查路径
  - 新增对应本地边界测试，并新增代表性 live 集成测试覆盖 `Trans1 / tline4 / tline6`
  - 当天手工 live 探针已额外验证默认全扫描的 9 个 `IEEE3` 候选支路都能在固定故障下跑通 EMT，并返回可比较的排序指标
  - 相关定向回归：`pytest tests/test_emt_result.py -q --run-integration -k 'branch_n1_security_scan_ranks_representative_outages'` -> `1 passed, 30 deselected, 4 warnings in 37.82s`
  - 相关全扫描探针：`python examples/analysis/emt_n1_security_screening_example.py model/holdme/IEEE3 --csv=/tmp/emt-n1-security-screening.csv --conclusion-txt=/tmp/emt-n1-security-screening.txt`
- 2026-03-20: EMT N-1 专题报告入口补充
  - 新增 `emt_n1_security_report_example.py`，默认围绕 `Trans1 / tline4 / tline6` 代表性工况生成 Markdown 研究报告
  - 新增对应本地边界测试，覆盖参数解析、报告拼装和导出
  - 相关 live 探针：`python examples/analysis/emt_n1_security_report_example.py model/holdme/IEEE3 --report=/tmp/emt-n1-security-report.md`
- 2026-03-20: EMT N-1 全扫描报告入口补充
  - 新增 `emt_n1_full_report_example.py`，默认围绕全部已发现 `IEEE3` N-1 候选工况生成 Markdown 报告
  - 新增对应本地边界测试，覆盖参数解析、全扫描报告拼装和导出
  - 相关 live 探针：`python examples/analysis/emt_n1_full_report_example.py model/holdme/IEEE3 --report=/tmp/emt-n1-full-report.md`
- 2026-03-22: EMT 报告型 wrapper live 覆盖补齐
  - 新增 `emt_research_report_example.py` 的独立 live 集成测试，验证四段已验证 EMT 研究路径可真实串联成 Markdown 报告并导出文件
  - 新增 `emt_n1_security_report_example.py` 的独立 live 集成测试，验证代表性 `Trans1 / tline4 / tline6` 工况可真实整理成 Markdown 报告并导出文件
  - 新增 `emt_n1_full_report_example.py` 的独立 live 集成测试，验证默认 `9` 个候选工况可真实整理成全扫描 Markdown 报告并导出文件
  - 相关定向回归：`pytest tests/test_emt_result.py -q --run-integration -k 'research_report_wrapper or n1_security_report_wrapper or n1_full_report_wrapper'` -> `3 passed, 31 deselected, 26 warnings in 245.81s (0:04:05)`
- 2026-03-21: IEEE39 检修方式安全校核补充
  - 新增 `powerflow_maintenance_security_example.py`，把“计划停运 + 检修态残余 N-1 复核”收敛成一条受限潮流研究路径
  - 新增对应本地边界测试，覆盖参数解析、检修态候选支路过滤、摘要 CSV 和结论生成
  - 新增对应 live 集成测试，验证 `line-26-28` 与变压器 `canvas_0_47` 两个检修样例下，剩余已验证子集仍可形成稳定排序
  - 相关定向回归：`pytest tests/test_powerflow_result.py -q --run-integration -k 'line_maintenance_state_can_be_rechecked_with_residual_n1_subset'` -> `1 passed, 25 deselected, 5 warnings in 32.51s`
  - 相关定向回归：`pytest tests/test_powerflow_result.py -q --run-integration -k 'transformer_maintenance_state_can_be_rechecked_with_residual_n1_subset'` -> `1 passed, 26 deselected, 5 warnings in 32.48s`
- 2026-03-18: 潮流工程研究场景补强
  - 新增 `IEEE39` 上 `line-26-28` 切除后的潮流改道真实集成验证
  - 新增 `IEEE39` 上 `Gen30 pf_V` 调整后的局部电压/无功支撑真实集成验证
  - 相关定向回归：`pytest tests/test_powerflow_result.py -q --run-integration -k 'line_outage_redistributes_corridor_flow_and_shifts_local_bus_state or generator_voltage_setpoint_adjustment_changes_local_bus_voltage_and_q_support'` -> `2 passed, 13 deselected, 3 warnings`
- 2026-03-18: 潮流多工况研究摘要补强
  - 新增 `IEEE39` 上 `baseline / load_up / line_x_up / line_outage / gen30_v_up` 五工况汇总的真实集成验证
  - 新增对应本地示例 `powerflow_batch_study_example.py` 与摘要格式化测试
  - 相关定向回归：`pytest tests/test_powerflow_result.py -q --run-integration -k 'batch_powerflow_study_summaries_capture_expected_directional_changes'` -> `1 passed, 15 deselected, 5 warnings`
- 2026-03-18: 受限 N-1 潮流筛查补强
  - 新增 `IEEE39` 上 `props.enabled=False` 与 `removeComponent()` 的停运语义等价性真实集成验证
  - 新增基于 `line-26-28`、`line-26-29`、`line-28-29` 的受限 N-1 严重性筛查真实集成验证
  - 新增对应本地示例 `powerflow_n1_screening_example.py` 与筛查摘要格式化测试
  - 相关定向回归：`pytest tests/test_powerflow_result.py -q --run-integration -k 'line_disable_via_props_enabled_matches_component_removal_for_validated_outage or subset_n1_screening_can_disable_multiple_lines_and_report_nontrivial_shifts'` -> `2 passed, 16 deselected, 7 warnings`
- 2026-03-18: IEEE39 全网支路 N-1 补强
  - 识别并剔除基线潮流支路表缺席的 `line-6-11` 伪候选线路，避免把天然假阳性混入全网筛查
  - 新增 `IEEE39` 全部 `43` 条基线在役支路的真实集成筛查验证，覆盖 `32` 条线路和 `11` 台变压器
  - 默认示例升级为全量支路筛查，并保留 `--validated-subset` 与 `--lines-only` 作为快速复核入口
  - 相关定向回归：`pytest tests/test_powerflow_result.py -q --run-integration -k 'active_line_candidates_exclude_base_absent_line_component or transformer_disable_via_props_enabled_matches_component_removal_for_validated_outage'` -> `2 passed, 19 deselected, 3 warnings in 17.53s`
  - 相关定向回归：`pytest tests/test_powerflow_result.py -q --run-integration -k 'full_active_branch_n1_screening_covers_lines_and_transformers_and_stable_top_rankings'` -> `1 passed, 20 deselected, 44 warnings in 252.74s`
- 2026-03-19: 完整 live 套件复验
  - 在当前收紧后的主线文档、示例和集成测试基础上，重新执行完整真实云端套件
  - 完整结果：`env TEST_SAVE_KEY_PREFIX=study_branch pytest tests/ -q --run-integration` -> `115 passed, 89 warnings in 630.93s (0:10:30)`
- 2026-03-23: 完整 live 套件复验
  - 在补齐 EMT 报告型 wrapper 的独立 live 集成测试后，重新执行完整真实云端套件
  - 完整结果：`env TEST_SAVE_KEY_PREFIX=study_branch pytest tests/ -q --run-integration` -> `178 passed, 145 warnings in 1154.60s (0:19:14)`
  - 结论：当前主线与新增 wrapper live 覆盖没有引入完整套件回归，但整体时长已接近 20 分钟，后续新增高成本 EMT 路径应优先考虑是否保留为定向回归
- 2026-03-19: 机组有功再调度场景补强
  - 新增 `IEEE39` 上 `Gen38 pf_P: 830 -> 900` 的真实集成验证，确认平衡机组出力和关键送电走廊潮流会发生可解释重分布
  - 将 `gen38_p_up` 纳入多工况潮流研究摘要
  - 明确记录：当前 `IEEE39` 变压器 `Tap/InitTap` 的普通潮流探针没有观察到有效结果变化，因此不宣称为已验证主线
  - 相关定向回归：`pytest tests/test_powerflow_result.py -q --run-integration -k 'generator_active_power_redispatch_shifts_slack_and_key_transfer_corridors or batch_powerflow_study_summaries_capture_expected_directional_changes'` -> `2 passed, 20 deselected, 7 warnings in 43.54s`
- 2026-03-19: EMT 故障研究摘要补强
  - 新增 `emt_fault_study_example.py`，把 `IEEE3` 上的 `baseline / delayed_clearing / mild_fault` 三工况收敛成一份工程化 EMT 故障研究摘要
  - 新增对应本地示例测试，锁定 RMS 指标提取窗口和摘要格式化
  - 新增真实集成验证，确认延迟切除主要拉低故障后恢复，而较轻故障主要抬高故障中与故障后的电压 RMS
  - 相关定向回归：`pytest tests/test_emt_result.py -q --run-integration -k 'fault_study_summary_distinguishes_clearing_time_and_fault_severity'` -> `1 passed, 26 deselected, 3 warnings in 28.33s`
  - 新增 CSV 导出入口，默认输出 `emt-fault-study-summary.csv`，也可通过 `--csv=...` 指定路径
  - 摘要字段进一步收紧为“原始 RMS + 相对故障前缺口 + 相对基线变化”，便于工程判读故障深度和恢复缺口
  - 新增对比波形 CSV 导出入口，默认输出 `emt-fault-study-waveforms.csv`，便于直接画三工况对比图
  - 新增 `--waveform-window=start,end`，支持只导出研究关注时间段的对比波形
  - 默认摘要 CSV 与波形 CSV 会绑定到同一研究前缀；若只传一个路径，另一个会自动按同前缀派生
  - 新增自动结论文本导出，明确研究问题、判据、结论和边界，把“产生数据”推进为“产生结论”
- 2026-03-19: EMT 故障严重度扫描补强
  - 新增 `emt_fault_severity_scan_example.py`，在 `IEEE3` 上对 `chg=1e-2 / 1e2 / 1e4` 做小型 EMT 扰动扫描
  - 新增对应本地示例测试，锁定扫描摘要、单调性结论和导出参数
  - 新增真实集成验证，确认较大 `chg` 对应更小的故障跌落和更小的恢复缺口
- 2026-03-20: EMT 故障清除时间扫描补强
  - 新增 `emt_fault_clearing_scan_example.py`，在 `IEEE3` 上对 `fe=2.70 / 2.75 / 2.80 / 2.85 / 2.90` 做小型 EMT 清除时间扫描
  - 新增对应本地示例测试，锁定固定研究时刻 `gap_295 / gap_300` 的单调恶化结论
  - 新增真实集成验证，确认晚切除工况在固定研究审视时刻上的恢复缺口更大
- 2026-03-20: EMT 量测可观测性工作流补强
  - 新增 `emt_measurement_workflow_example.py`，在 `IEEE3` 上把“使用已有测点、增加 Bus2 测点、删除不需要的 #Q 输出”收敛为同一条 EMT 工作流
  - 新增对应本地示例测试，锁定量测工作流摘要、结论和导出参数
  - 新增真实集成验证，确认新增 `Bus2` 测点 RMS 成立、PQ 组成功裁剪为 `#P*`，且保留下来的 `#P1` 仍可直接用于研究读数
