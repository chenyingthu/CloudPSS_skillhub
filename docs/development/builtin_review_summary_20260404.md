# builtin 技能库代码审查总结

日期: 2026-04-04

范围:
- `cloudpss_skills/builtin/`

审查方法:
- 先对全目录做模式筛查，定位高风险点
- 再按文件逐个下钻 review
- 重点关注三类问题：
  1. 假成功：部分失败、零结果、空分析仍返回 `SUCCESS`
  2. 异常边界过窄：业务失败直接抛异常而不是返回 `FAILED`
  3. 结果语义失真：错误解析、占位结果、估算值/随机值冒充真实分析

---

## 总体判断

当前 builtin 技能库的主风险不在代码风格，而在**结果可信度**：

- 多个技能把“没拿到有效结果”当成“分析成功”
- 多个技能在清理异常捕获后失去 `SkillResult(FAILED)` 包装能力
- 少数技能会在真实结果不可用时继续生成估算/随机结果

这会直接破坏“已通过真实 CloudPSS API 验证”的结论质量。

---

## 高优先级问题

### 1. 假成功 / 状态错误

| 技能 | 文件位置 | 问题 |
|---|---|---|
| `n1_security` | `cloudpss_skills/builtin/n1_security.py` | 存在失败场景时仍可能返回 `SUCCESS` |
| `n2_security` | `cloudpss_skills/builtin/n2_security.py:214` | 顶层无条件 `SUCCESS`，忽略 N-2 失败场景 |
| `batch_powerflow` | `cloudpss_skills/builtin/batch_powerflow.py:342` | 部分模型失败/不收敛仍可能整体 `SUCCESS` |
| `config_batch_runner` | `cloudpss_skills/builtin/config_batch_runner.py:404` | 配置失败/超时不影响顶层 `SUCCESS` |
| `emt_n1_screening` | `cloudpss_skills/builtin/emt_n1_screening.py:338` | 筛查中有失败场景也无条件 `SUCCESS` |
| `param_scan` | `cloudpss_skills/builtin/param_scan.py:303` | 即使全部扫描点失败，仍返回 `SUCCESS` |
| `orthogonal_sensitivity` | `cloudpss_skills/builtin/orthogonal_sensitivity.py:487` | 即使运行失败较多，仍无条件 `SUCCESS` |
| `power_quality_analysis` | `cloudpss_skills/builtin/power_quality_analysis.py:316` | 空分析结果也被汇总成 `PASS` |
| `result_compare` | `cloudpss_skills/builtin/result_compare.py:294` | 零通道对比也会返回 `SUCCESS` |
| `report_generator` | `cloudpss_skills/builtin/report_generator.py:145` | 没有真实结果输入也能生成“正式报告” |

### 2. EMT 调用与当前 SDK 不兼容

| 技能 | 文件位置 | 问题 |
|---|---|---|
| `vsi_weak_bus` | `cloudpss_skills/builtin/vsi_weak_bus.py:208` | 使用 `runEMT(endTime=..., step=...)` |
| `reactive_compensation_design` | `cloudpss_skills/builtin/reactive_compensation_design.py:768` | 使用 `runEMT(endTime=..., step=...)` |
| `batch_task_manager` | `cloudpss_skills/builtin/batch_task_manager.py:440` | 使用 `runEMT(endTime=..., step=...)` |
| `transient_stability_margin` | `cloudpss_skills/builtin/transient_stability_margin.py:279` | 使用 `runEMT(simuTime=5.0)` |

### 3. 真实结果解析错误 / 逻辑错误

| 技能 | 文件位置 | 问题 |
|---|---|---|
| `compare_visualization` | `cloudpss_skills/builtin/compare_visualization.py:242` | 默认标签引用未定义变量 `i`，直接 `NameError` |
| `compare_visualization` | `cloudpss_skills/builtin/compare_visualization.py:507` | 热力图通道集合构造错误，得到空 `set()` 列表 |
| `maintenance_security` | `cloudpss_skills/builtin/maintenance_security.py:174` | 把 CloudPSS 表格对象当逐行 dict 读 `Vm/loading`，严重度结论不可信 |
| `loss_analysis` | `cloudpss_skills/builtin/loss_analysis.py:328` | 真实损耗提取失败时用随机数生成损耗结果 |
| `power_flow` | `cloudpss_skills/builtin/power_flow.py:155` | 只看 `job.status()==1` 就标记 `converged: true`，不验证结果表 |
| `power_quality_analysis` | `cloudpss_skills/builtin/power_quality_analysis.py:218` | 用 `Model` 调 EMTResult 风格的通道检测逻辑，检测路径错位 |
| `orthogonal_sensitivity` | `cloudpss_skills/builtin/orthogonal_sensitivity.py:522` | 未指定 `component_rid` 时，未知参数作用到全部发电机 |

### 4. 明确会导致运行时崩溃的代码错误

| 技能 | 文件位置 | 问题 |
|---|---|---|
| `loss_analysis` | `cloudpss_skills/builtin/loss_analysis.py:286` | `except` 里引用未定义变量 `e` |
| `loss_analysis` | `cloudpss_skills/builtin/loss_analysis.py:295` | `except` 里引用未定义变量 `e` |
| `loss_analysis` | `cloudpss_skills/builtin/loss_analysis.py:310` | `except` 里引用未定义变量 `e` |
| `loss_analysis` | `cloudpss_skills/builtin/loss_analysis.py:553` | `except FileNotFoundError` 里引用未定义变量 `e` |
| `power_quality_analysis` | `cloudpss_skills/builtin/power_quality_analysis.py:447` | `except Exception:` 后打印未定义变量 `e` |
| `emt_n1_screening` | `cloudpss_skills/builtin/emt_n1_screening.py:380` | `except Exception:` 后打印未定义变量 `e` |

---

## 中优先级问题

### 1. 异常边界过窄，业务失败直接逃逸

| 技能 | 文件位置 | 问题 |
|---|---|---|
| `batch_powerflow` | `cloudpss_skills/builtin/batch_powerflow.py:355` | `FileNotFoundError` 等常见输入错误不返回 `FAILED` |
| `config_batch_runner` | `cloudpss_skills/builtin/config_batch_runner.py:421` | `FileNotFoundError/RuntimeError/TimeoutError` 可能直接逃逸 |
| `batch_task_manager` | `cloudpss_skills/builtin/batch_task_manager.py:425` | `ValueError/RuntimeError/TimeoutError` 不在捕获范围 |
| `transient_stability` | `cloudpss_skills/builtin/transient_stability.py:311` | `RuntimeError("EMT仿真失败")` 可直接逃逸 |
| `short_circuit` | `cloudpss_skills/builtin/short_circuit.py:288` | `RuntimeError("EMT仿真失败")` 可直接逃逸 |
| `waveform_export` | `cloudpss_skills/builtin/waveform_export.py:246` | 业务 `RuntimeError` 不会转成 `FAILED` |
| `visualize` | `cloudpss_skills/builtin/visualize.py:292` | 业务 `RuntimeError` 不会转成 `FAILED` |
| `contingency_analysis` | `cloudpss_skills/builtin/contingency_analysis.py:351` | `FileNotFoundError/RuntimeError/ValueError` 可直接逃逸 |
| `renewable_integration` | `cloudpss_skills/builtin/renewable_integration.py:248` | 数值/业务异常可能直接逃逸 |
| `voltage_stability` | `cloudpss_skills/builtin/voltage_stability.py:319` | `FileNotFoundError/ValueError/TypeError` 可直接逃逸 |
| `auto_channel_setup` | `cloudpss_skills/builtin/auto_channel_setup.py:315` | 顶层仅捕获 `AttributeError` |
| `auto_loop_breaker` | `cloudpss_skills/builtin/auto_loop_breaker.py:287` | 内部 `RuntimeError` 不一定被顶层可靠接住 |
| `component_catalog` | `cloudpss_skills/builtin/component_catalog.py:229` | 虽已扩宽部分边界，但内部 fetch/enrich 仍有差异路径 |

### 2. 返回契约 / 结果对象问题

| 技能 | 文件位置 | 问题 |
|---|---|---|
| `component_catalog` | `cloudpss_skills/builtin/component_catalog.py:196` | `artifacts` 返回字符串路径而不是 `Artifact` |
| `component_catalog` | `cloudpss_skills/builtin/component_catalog.py:203` | 与其他技能的 artifact 契约不一致 |

### 3. 结果结论过于弱或基于占位逻辑

| 技能 | 文件位置 | 问题 |
|---|---|---|
| `model_validator` | `cloudpss_skills/builtin/model_validator.py:758` | EMT gate 仍然只是 smoke 级别，不足以证明结果物理正确 |
| `report_generator` | `cloudpss_skills/builtin/report_generator.py:200` | 无真实输入时仍构造 `pending` 占位结果并继续出报告 |
| `renewable_integration` | `cloudpss_skills/builtin/renewable_integration.py:420` | 多个子分析仍基于估算/假设，不宜直接视作真实验证结论 |

---

## 已复核后可以降级或移出问题清单的点

| 技能 | 说明 |
|---|---|
| `topology_check` | 当前工作树中 `issues > 0 -> FAILED`，不再算活跃问题 |
| `model_validator` | 守门逻辑明显改善，当前不是主风险源 |
| `comtrade_export` | token 检查与顶层异常边界已有改善，当前不列为最紧急问题 |

---

## 建议修复顺序

### 第一组：必须先修

1. `vsi_weak_bus`
2. `reactive_compensation_design`
3. `batch_task_manager`
4. `transient_stability_margin`
5. `n2_security`
6. `compare_visualization`
7. `loss_analysis`
8. `power_quality_analysis`

原因：
- 这几项不是简单警告，而是会直接崩、明显假成功、或输出错误结论

### 第二组：紧接着修

1. `config_batch_runner`
2. `param_scan`
3. `orthogonal_sensitivity`
4. `maintenance_security`
5. `emt_n1_screening`
6. `report_generator`

### 第三组：统一收口

1. `waveform_export`
2. `visualize`
3. `power_flow`
4. `auto_channel_setup`
5. `component_catalog`
6. `contingency_analysis`
7. `renewable_integration`
8. `voltage_stability`
9. `transient_stability`
10. `short_circuit`

---

## 回归验证建议

修复时不要只看“脚本能跑”：

1. 先做本地单元测试
2. 再做真实 CloudPSS API 集成测试
3. 对关键技能检查结果内容是否合理
4. 明确哪些技能只完成了 smoke-level 验证，哪些真的完成了结果正确性验证

建议每修完一组就跑对应集成测试，而不是最后一次性跑全套。

---

## 备注

本总结来自对 `cloudpss_skills/builtin/` 的分文件 review。
重点不是风格问题，而是：

- 失败是否会被正确上报
- 结果是否真的来自有效数据
- 结论是否具有工程可信度
