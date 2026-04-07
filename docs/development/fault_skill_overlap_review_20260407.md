# EMT故障类技能重叠性审查

日期: 2026-04-07

范围:
- `cloudpss_skills/builtin/emt_fault_study.py`
- `cloudpss_skills/builtin/fault_clearing_scan.py`
- `cloudpss_skills/builtin/fault_severity_scan.py`
- `cloudpss_skills/builtin/transient_stability_margin.py`

## 结论摘要

这四个技能里，前三个已经形成了明显的“同一条故障扫描内核，不同观察维度”的关系。

- `emt_fault_study`
  - 是一个“三工况固定专题研究器”
  - 固定比较 `baseline / delayed_clearing / mild_fault`
  - 输出 RMS 指标、波形对比、结论摘要
- `fault_clearing_scan`
  - 是“单参数扫描器”
  - 只扫描 `fe`（故障切除时间）
  - 在单一研究时刻取电压值，判断恢复趋势
- `fault_severity_scan`
  - 也是“单参数扫描器”
  - 只扫描 `chg`（故障电阻/故障严重度）
  - 用 prefault/fault/postfault RMS 评估跌落与恢复

这三个技能在本质上都属于：

`同一故障模型 + 单个或少量参数扫描 + EMT运行 + 对同一电压轨迹做窗口化后处理`

因此，**功能上高度重叠，代码上也明显雷同，完全值得归并到同一故障扫描框架下**。

相对地，`transient_stability_margin` 当前和前三者在“实现层”有重叠，但在“目标层”不应直接并成同一个技能。

- 它关注的是 `CCT / margin`
- 理论上是“稳定边界搜索器”
- 不是简单的故障专题对比或单参数扫描
- 但当前实现里，它仍然复用了“改故障参数 + 跑EMT + 读结果”的同一类执行框架

所以它**不适合直接和前三个技能完全合并**，但**非常适合共享同一套故障仿真执行内核**。

## 横向比较

### 1. 功能目标

| 技能 | 核心问题 | 参数维度 | 输出风格 |
|---|---|---|---|
| `emt_fault_study` | 三个代表性故障工况如何影响故障跌落和恢复 | 固定 3 工况 | 专题研究报告 |
| `fault_clearing_scan` | `fe` 增大时恢复是否单调恶化 | 单参数 `fe` | 扫描表 + 趋势结论 |
| `fault_severity_scan` | `chg` 增大时故障跌落/恢复是否单调改善 | 单参数 `chg` | 扫描表 + 趋势结论 |
| `transient_stability_margin` | 稳定边界在哪里，CCT是多少 | 二分搜索 `clearing_time` | 边界/裕度结论 |

### 2. 执行链重叠

前三个技能都重复了以下步骤：

1. 取模型
2. 找 `_newFaultResistor_3p`
3. 修改 `fs/fe/chg`
4. `runEMT()`
5. 等待完成
6. 找目标波形
7. 在固定时间窗内算 RMS / 某时刻值
8. 组装 CSV / JSON / Markdown

`transient_stability_margin` 虽然不做同样的输出，但也重复了：

1. 取模型
2. 改故障参数
3. `runEMT()`
4. 等待完成
5. 根据某种稳定判据给出 stable/unstable

## 代码重复点

### `emt_fault_study` 与 `fault_clearing_scan`

重复度非常高：

- 都扫描同一故障模型
- 都显式修改 `_newFaultResistor_3p`
- 都依赖 `trace_name`
- 都从 EMT 结果中抽同一条电压轨迹
- 都以时间窗/研究时刻为依据形成表格结论

区别只在：

- `emt_fault_study` 是固定三工况
- `fault_clearing_scan` 是 `fe` 参数数组

### `emt_fault_study` 与 `fault_severity_scan`

重复度同样很高：

- 故障模型相同
- EMT执行方式相同
- 波形抽取方式相同
- 后处理都是窗口化电压分析

区别只在：

- `fault_severity_scan` 扫 `chg`
- `emt_fault_study` 用预定义的三工况专题叙事

### `fault_clearing_scan` 与 `fault_severity_scan`

这两个几乎就是同一个扫描器的两个参数实例：

- 一个扫描 `fe`
- 一个扫描 `chg`
- 其余流程结构基本一致

## 归并建议

### 建议一: 先合并前三个为统一“EMT故障参数扫描内核”

建议抽出一个公共内核，例如：

- `cloudpss_skills/core/fault_scan.py`

核心职责：

1. 加载模型
2. 定位故障元件
3. 应用故障参数组合
4. 执行 EMT
5. 提取指定波形
6. 按时间窗或研究时刻提取指标
7. 返回结构化场景结果

在这个内核上保留三个薄封装：

- `emt_fault_study`
  - 只是预置三工况配置的专题包装器
- `fault_clearing_scan`
  - 只是 `scan_dimension = fe`
- `fault_severity_scan`
  - 只是 `scan_dimension = chg`

这样做的好处：

- 去掉重复的故障配置与 EMT 调度代码
- 去掉重复的 trace 提取与窗口 RMS 计算
- 三个技能的错误处理、结果契约、artifact 结构更容易统一
- 后续如果要加 `fs` 扫描、双参数扫描、故障位置扫描，也可直接复用

### 建议二: `transient_stability_margin` 不直接并技能，但共享执行内核

建议把它作为“边界搜索型上层技能”保留单独入口。

原因：

- 它的目标不是“做一张扫描表”
- 它是“搜索稳定边界”
- 未来如果要做真实 CCT，需要替换的是稳定判据，不是简单表格后处理

但它仍应共享：

- 故障参数应用器
- EMT 运行/等待器
- 波形抓取器
- 稳定性观测通道配置器

换句话说：

- 前三个技能可“功能归并”
- `transient_stability_margin` 更适合“内核归并，外壳保留”

## 当前质量判断

### `emt_fault_study`

定位最清晰，也最像用户真正会直接用的专题研究技能。

建议保留。

### `fault_clearing_scan`

适合保留为参数扫描技能，但应重建为统一故障扫描器的一个特例。

### `fault_severity_scan`

同上。

### `transient_stability_margin`

当前最大问题不是代码重复，而是**稳定判据仍是近似的**。

所以它当前的优先级不是“先并代码”，而是：

1. 先把“真实稳定判据”打通
2. 再考虑与故障扫描内核共享实现

## 推荐实施顺序

1. 抽公共 EMT 故障扫描内核
2. 让 `fault_clearing_scan` 和 `fault_severity_scan` 先迁过去
3. 再把 `emt_fault_study` 迁过去，保留专题化报告层
4. 最后再评估 `transient_stability_margin` 共享执行层，但不强行并掉技能入口

## 一句话判断

可以归并，但要分层归并：

- `emt_fault_study + fault_clearing_scan + fault_severity_scan`
  - **建议功能归并**
- `transient_stability_margin`
  - **建议仅共享执行内核，不直接功能归并**
