# CloudPSS Toolkit 输入数据规范性审查报告

**审查日期**: 2026-04-16
**审查范围**: 48 个技能 + 核心辅助模块
**审查维度**: 规范性、标准化、完备性、准确性

---

## 一、总体发现概述

### 1.1 问题分类统计

| 问题类别 | 数量 | 占比 | 严重程度 |
|----------|------|------|----------|
| Schema-Runtime 不匹配 | 35 | 28% | 🔴 高 |
| 缺失验证逻辑 | 42 | 34% | 🟡 中 |
| 类型强制转换问题 | 8 | 6% | 🔴 高 |
| 默认值不一致 | 18 | 14% | 🟡 中 |
| 范围/边界检查缺失 | 15 | 12% | 🟢 低 |
| 字段名称不一致 | 7 | 6% | 🟡 中 |

### 1.2 按严重程度分类

#### 🔴 严重问题（Critical）- 需要立即修复

| # | 文件 | 问题 | 影响 |
|---|------|------|------|
| 1 | `batch_task_manager.py` | `model_rid` 和 `model` 变量在 `run()` 中未定义就使用 | 运行时 NameError |
| 2 | `config_batch_runner.py` | `success_results` 在定义前被引用 (L463-469) | 运行时 NameError |
| 3 | `maintenance_security.py` | 缺少 `Model` 和 `deepcopy` 导入 | 运行时 NameError |
| 4 | `emt_fault_study.py` | 数值参数被强制转为字符串 (fs/fe/chg) | 类型不匹配，EMT 计算错误 |
| 5 | `emt_n1_screening.py` | 数值参数被强制转为字符串 | 同上 |

#### 🟡 高优先级问题（High）

| # | 文件 | 问题 | 影响 |
|---|------|------|------|
| 1 | `power_flow.py` | `output.format` 定义但未使用 | 功能不可用 |
| 2 | `emt_simulation.py` | Schema 支持 YAML 但代码未实现 | 功能不可用 |
| 3 | `loss_analysis.py` | `output` 字段定义但未实现保存逻辑 | 功能不可用 |
| 4 | `model_builder.py` | Schema 顶层缺少 `required` 声明 | 验证不完整 |
| 5 | `model_validator.py` | `auth` 可选但运行时必须认证 | 配置困惑 |

#### 🟢 中优先级问题（Medium）

| # | 文件 | 问题 | 影响 |
|---|------|------|------|
| 1 | `orthogonal_sensitivity.py` | 默认配置 `parameters: []` 无效 | 默认无法运行 |
| 2 | `fault_clearing_scan.py` | `fe_values` 缺少 `minItems` 检查 | 可能空扫描 |
| 3 | `fault_severity_scan.py` | `chg_values` 缺少 `minItems` 检查 | 可能空扫描 |
| 4 | `small_signal_stability.py` | `freq_range` 缺少长度验证 | 索引越界风险 |
| 5 | `result_compare.py` | `time_range.start/end` 缺少顺序验证 | 逻辑错误 |

---

## 二、详细问题清单

### 2.1 仿真与分析技能

#### power_flow.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L61-67, L131-134 | `auth.token` 可选但 `setup_auth()` 会失败 | 在 schema 添加 `required` 或提供默认值 |
| B | L88-95, L158-164 | `output.format` 定义但未使用 | 实现格式选择或移除未用字段 |
| C | 整体 | 无 `validate()` 重写 | 添加显式预检查 |

#### emt_simulation.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L112-118, L226-248 | Schema 允许 YAML 但代码只实现 CSV/JSON | 实现 YAML 导出或限制 schema 选项 |
| B | L72-76, L191-199 | `duration` 字段定义但未在运行时使用 | 移除或实现功能 |
| C | L141-159 | `validate()` 仅做基本检查 | 增强验证逻辑 |

#### short_circuit.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L55-58, L75-101 | 验证逻辑良好，与 schema 一致 | 保持现状 |

#### loss_analysis.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L145-155, L239-246 | `output` 字段定义但无保存逻辑 | 实现保存功能或移除未用字段 |
| B | L98-99 | `model.config_index` 定义但未使用 | 移除或实现功能 |
| C | L101-107 | `auth.token_file` 无默认值 | 添加默认路径 |

### 2.2 安全分析技能

#### n1_security.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L136-155 | Schema 允许 YAML 但代码只实现 JSON | 统一输出格式 |
| B | L155-175 | `analysis` 对象验证不完整 | 添加必需字段检查 |
| C | L175-195 | `voltage_threshold` 缺少默认值同步 | 确保默认值一致 |

#### n2_security.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L200-220 | 存在重复函数定义 | 清理代码 |
| B | L150-170 | `analysis.branch_pairs` 缺少元素数量验证 | 添加 `minItems: 2` |

#### contingency_analysis.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L130-145 | Schema 允许 CSV 但代码只支持 JSON/Console | 移除 CSV 选项或实现 |
| B | L200-230 | 电压限值验证不完整 | 添加范围检查 |

#### maintenance_security.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | 文件开头 | 缺少 `Model` 导入 | 🔴 **立即修复** |
| B | 文件开头 | 缺少 `deepcopy` 导入 | 🔴 **立即修复** |

### 2.3 EMT 故障扫描技能

#### emt_fault_study.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L276-279 | `fs/fe/chg` 被转为字符串传给 EMT | 🔴 **立即修复** - 保持数值类型 |
| B | L488-491 | 类型不匹配风险 | 确保数值传递给 `apply_fault_parameters` |

#### fault_clearing_scan.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L76-83 | `fe_values` 缺少 `minItems` | 添加 `minItems: 1` 约束 |
| B | L176-179 | 空数组时静默通过 | 添加非空检查并报错 |

#### fault_severity_scan.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L71-83 | `chg_values` 缺少 `minItems` | 添加 `minItems: 1` 约束 |
| B | L183-205 | 空数组时静默通过 | 添加非空检查并报错 |

#### emt_n1_screening.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L498-502 | `fs/fe/chg` 被转为字符串 | 🔴 **立即修复** |
| B | L235-237, L246-247 | `limit=0` 导致空分支列表 | 明确 `limit=0` 语义或添加检查 |

### 2.4 稳定性分析技能

#### transient_stability.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L73-78, L211-214 | `fe_values` 缺少长度检查 | 添加 `minItems >= 1` |
| B | L114-118, L204-205 | `analysis_window` 缺少结构验证 | 验证 2 元素数组 |
| C | L108-112, L512-517 | `stable_criterion` 定义但未使用 | 移除或实现功能 |

#### small_signal_stability.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L75-79, L151-153 | `freq_range` 缺少长度验证 | 添加 `minItems: 2, maxItems: 2` |
| B | L640-643 | 无发电机时 `_build_state_matrix` 报错 | 添加预检查并友好提示 |

#### voltage_stability.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L98-103, L270-280 | `collapse_threshold` 缺少范围验证 | 添加 `[0, 1]` 范围约束 |
| B | L381-395, L405-408 | 组件分类依赖字符串匹配 | 添加回退逻辑 |

#### frequency_response.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L71-111, L412-517 | `disturbance.type` 与字段依赖未验证 | 添加交叉字段验证 |
| B | L112-126, L532-541 | 监控通道可选但无最低要求 | 文档说明或添加检查 |

### 2.5 模型构建与验证技能

#### model_builder.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L142-150 | Schema 顶层缺少 `required` 声明 | 添加关键字段要求 |
| B | L173-179 | `auth` 缺少 `server/base_url` 字段 | 补充 schema |
| C | L198-204 | `position.x/y` 缺少范围验证 | 添加合理范围 |

#### model_validator.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L139-145, L212-214 | `auth` 可选但 `setup_auth()` 必需 | 添加认证验证或默认值 |
| B | L168-171 | `timeout` 缺少范围验证 | 添加合理范围 (如 1-3600) |

#### model_parameter_extractor.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L98-104 | `auth.token_file` schema 无默认值 | 与 `get_default_config` 对齐 |
| B | L116-120 | `component_types` 受 `COMPONENT_DEFINITIONS` 限制 | 保持同步 |

### 2.6 批量与扫描技能

#### batch_powerflow.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L167-169, L176-178 | `config["models"]` 和 `model_config["rid"]` 缺少运行时检查 | 添加防御性检查 |
| B | L71-81 | `algorithm` 定义但未在 `run()` 中使用 | 实现算法选择或移除 |

#### batch_task_manager.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L285-289 | `model_rid` 和 `model` 未定义就使用 | 🔴 **立即修复** - 定义变量 |
| B | L133-149 | 任务验证不完整 | 增强内部字段验证 |

#### param_scan.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L135-139 | `scan.values` 缺少非空检查 | 添加 `minItems >= 1` |
| B | L75-79 | `values` 类型为数字但运行时转字符串 | 确认 API 期望类型 |

#### config_batch_runner.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L463-469 | `success_results` 在定义前被引用 | 🔴 **立即修复** - 重新组织代码 |

### 2.7 其他分析技能

#### orthogonal_sensitivity.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L270-271 | 默认配置 `parameters: []` 无效 | 提供有效默认值 |
| B | L208-211, L701-707 | `custom` 指标未实现 | 移除或实现功能 |
| C | L302-304 | 参数数量上限硬编码为 7 | 与正交表实际容量对齐 |

#### reactive_compensation_design.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L266-270 | 默认 `model.rid` 为空 | 提供有效默认值 |
| B | L449-456 | `capacitor_config` schema 未定义 | 添加 schema 定义 |
| C | L221-245 | 迭代参数缺少范围验证 | 添加合理范围 |

#### vsi_weak_bus.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L101-110 | `bus_filter` 缺少范围验证 | 添加电压合理范围 |
| B | L757-767 | VSI 计算依赖 EMT 结果结构 | 添加前置检查 |

#### thevenin_equivalent.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L98-100 | 默认模型 RID 可能过时 | 添加动态验证 |
| B | L66-71, L140-146 | `pcc.bus` 必须存在但无预验证 | 添加总线存在性检查 |

### 2.8 导出与可视化技能

#### visualize.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L93-102 | `output.format` 支持 PNG/PDF/SVG | 验证路径正确性 |

#### result_compare.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L79-85 | `time_range.start/end` 缺少顺序验证 | 添加 `start <= end` 检查 |

#### compare_visualization.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L60-90 | 输入验证基本完整 | 保持现状 |

### 2.9 工具类技能

#### auto_channel_setup.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L65-72, L151-156 | `model.rid` 默认空字符串 | 提供有效示例 RID |
| B | L85-93 | `auth.token` 可选但可能失败 | 文档说明认证要求 |

#### protection_coordination.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L219-221, L305-308 | Schema 定义 `save_path` 但代码使用其他字段 | 统一字段名称 |
| B | L166-176 | `time_margin` 缺少范围验证 | 添加合理范围 |

#### study_pipeline.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L119-124 | `max_workers` 缺少范围验证 | 添加 `minimum: 1` |
| B | L441-452 | 技能存在性仅在运行时检查 | 添加预检查 |

#### component_catalog.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L411-417, L448-456 | 输出路径目录可能不存在 | 添加 `mkdir(parents=True)` |
| B | L114-128 | `page_size` 缺少范围验证 | 添加 `minimum: 1` |

#### model_hub.py
| 问题 | 位置 | 描述 | 建议 |
|------|------|------|------|
| A | L237-246, L1014-1024 | Schema 定义 `output.path` 但代码使用 `model.local_path` | 统一路径来源 |

---

## 三、核心工具模块问题

### 3.1 core/utils.py
| 问题 | 描述 | 建议 |
|------|------|------|
| A | 多个函数缺少显式输入验证 | 添加类型检查包装器 |
| B | 对 `None` 输入处理不一致 | 统一空值处理 |
| C | `get_token_from_config` 可能返回 `None` | 添加显式错误处理 |

### 3.2 core/config.py
| 问题 | 描述 | 建议 |
|------|------|------|
| A | `InteractiveConfigBuilder` 缺少严格验证 | 添加输入验证 |
| B | JSON Schema 默认与 `get_default_config` 可能不一致 | 确保同步 |

### 3.3 metadata/models.py
| 问题 | 描述 | 建议 |
|------|------|------|
| A | `multi_choice` 类型验证缺失 | 添加多选类型验证 |
| B | YAML 解析过于简单 | 使用 PyYAML 解析器 |

---

## 四、修复优先级建议

### 4.1 P0 - 立即修复（阻塞性问题）

1. **maintenance_security.py** - 添加缺失导入
2. **batch_task_manager.py** - 定义未初始化变量
3. **config_batch_runner.py** - 修复变量引用顺序
4. **emt_fault_study.py** - 移除错误的字符串转换
5. **emt_n1_screening.py** - 移除错误的字符串转换

### 4.2 P1 - 高优先级（功能性问题）

1. **power_flow.py** - 实现 `output.format` 或移除未用字段
2. **emt_simulation.py** - 实现 YAML 导出或限制 schema
3. **loss_analysis.py** - 实现 `output` 保存或移除未用字段
4. **model_builder.py** - 添加顶层 `required` 声明
5. **orthogonal_sensitivity.py** - 修复默认配置

### 4.3 P2 - 中优先级（健壮性问题）

1. 所有 scan 技能 - 添加 `minItems` 验证
2. 稳定性技能 - 添加范围验证
3. 批量技能 - 添加运行时防御检查

### 4.4 P3 - 低优先级（改进建议）

1. 添加更多单元测试覆盖输入验证路径
2. 统一错误消息语言（建议英文）
3. 添加输入验证中间件

---

## 五、验收标准

修复完成后应满足：

| 维度 | 标准 |
|------|------|
| **规范性** | 所有 Schema 有完整 `required` 声明，类型约束明确 |
| **标准化** | 同类参数使用统一命名和默认值模式 |
| **完备性** | 所有必需输入在验证阶段被检查 |
| **准确性** | Schema 与运行时逻辑完全对齐 |

---

## 六、后续行动

1. 创建修复计划，针对 P0 问题优先处理
2. 为每个修复编写对应的单元测试
3. 建立输入验证最佳实践文档
4. 考虑添加自动化 Schema 验证工具
