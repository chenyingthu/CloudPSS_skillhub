# CloudPSS 技能系统文档

配置驱动的电力系统仿真工具包，包含47个专业仿真技能。

## 技能文档索引

### 模型管理类（新增）

| 技能 | 描述 | 文档 |
|------|------|------|
| `component_catalog` | 组件目录发现 | [查看文档](component_catalog.md) |
| `model_builder` | 模型构建器 | [查看文档](model_builder.md) |
| `model_validator` | 模型验证器 | [查看文档](model_validator.md) |

### 仿真执行类

| 技能 | 描述 | 文档 |
|------|------|------|
| `power_flow` | 牛顿-拉夫逊潮流计算 | [查看文档](power_flow.md) |
| `emt_simulation` | EMT暂态仿真 | [查看文档](emt_simulation.md) |
| `emt_fault_study` | EMT故障研究 | [查看文档](emt_fault_study.md) |
| `short_circuit` | 短路电流计算 | [查看文档](short_circuit.md) |

### N-1安全分析类

| 技能 | 描述 | 文档 |
|------|------|------|
| `n1_security` | N-1安全校核 | [查看文档](n1_security.md) |
| `n2_security` | N-2安全校核 | [查看文档](n2_security.md) |
| `emt_n1_screening` | EMT N-1安全筛查 | [查看文档](emt_n1_screening.md) |
| `contingency_analysis` | 预想事故分析 | [查看文档](contingency_analysis.md) |
| `maintenance_security` | 检修方式安全校核 | [查看文档](maintenance_security.md) |

### 安全与保护类

| 技能 | 描述 | 文档 |
|------|------|------|
| `protection_coordination` | 保护整定与配合分析 | [查看文档](protection_coordination.md) |

### 批量与扫描类

| 技能 | 描述 | 文档 |
|------|------|------|
| `batch_powerflow` | 批量潮流计算 | [查看文档](batch_powerflow.md) |
| `param_scan` | 参数扫描分析 | [查看文档](param_scan.md) |
| `fault_clearing_scan` | 故障清除时间扫描 | [查看文档](fault_clearing_scan.md) |
| `fault_severity_scan` | 故障严重度扫描 | [查看文档](fault_severity_scan.md) |
| `ieee3_prep` | IEEE3模型准备 | [查看文档](ieee3_prep.md) |
| `batch_task_manager` | 批处理任务管理 | [查看文档](batch_task_manager.md) |
| `config_batch_runner` | 多配置批量运行 | [查看文档](config_batch_runner.md) |

### 稳定性分析类

| 技能 | 描述 | 文档 |
|------|------|------|
| `voltage_stability` | 电压稳定分析 | [查看文档](voltage_stability.md) |
| `transient_stability` | 暂态稳定分析 | [查看文档](transient_stability.md) |
| `transient_stability_margin` | 暂态稳定裕度评估 | [查看文档](transient_stability_margin.md) |
| `small_signal_stability` | 小信号稳定分析 | [查看文档](small_signal_stability.md) |
| `frequency_response` | 频率响应分析 | [查看文档](frequency_response.md) |
| `vsi_weak_bus` | VSI弱母线分析 | [查看文档](vsi_weak_bus.md) |
| `dudv_curve` | DUDV曲线生成 | [查看文档](dudv_curve.md) |
| `orthogonal_sensitivity` | 正交敏感性分析 | [查看文档](orthogonal_sensitivity.md) |

### 结果处理类

| 技能 | 描述 | 文档 |
|------|------|------|
| `result_compare` | 结果对比分析 | [查看文档](result_compare.md) |
| `visualize` | 结果可视化 | [查看文档](visualize.md) |
| `waveform_export` | 波形数据导出 | [查看文档](waveform_export.md) |
| `hdf5_export` | HDF5数据导出 | [查看文档](hdf5_export.md) |
| `comtrade_export` | COMTRADE标准格式导出 | [查看文档](comtrade_export.md) |
| `compare_visualization` | 结果对比可视化 | [查看文档](compare_visualization.md) |
| `disturbance_severity` | 扰动严重度分析 | [查看文档](disturbance_severity.md) |
| `loss_analysis` | 网损分析 | [查看文档](loss_analysis.md) |
| `report_generator` | 智能报告生成 | [查看文档](report_generator.md) |

### 新能源接入类

| 技能 | 描述 | 文档 |
|------|------|------|
| `renewable_integration` | 新能源接入评估 | [查看文档](renewable_integration.md) |
| `thevenin_equivalent` | PCC戴维南等值 | [查看文档](thevenin_equivalent.md) |

### 电能质量类

| 技能 | 描述 | 文档 |
|------|------|------|
| `harmonic_analysis` | 谐波分析 | [查看文档](harmonic_analysis.md) |
| `power_quality_analysis` | 电能质量分析 | [查看文档](power_quality_analysis.md) |
| `reactive_compensation_design` | 无功补偿设计 | [查看文档](reactive_compensation_design.md) |

### 模型与拓扑类

| 技能 | 描述 | 文档 |
|------|------|------|
| `topology_check` | 拓扑检查 | [查看文档](topology_check.md) |
| `parameter_sensitivity` | 参数灵敏度分析 | [查看文档](parameter_sensitivity.md) |
| `auto_channel_setup` | 自动量测配置 | [查看文档](auto_channel_setup.md) |
| `auto_loop_breaker` | 自动解环 | [查看文档](auto_loop_breaker.md) |
| `model_parameter_extractor` | 模型参数提取 | [查看文档](model_parameter_extractor.md) |

## 快速开始

### 1. 安装

```bash
# 确保已安装CloudPSS SDK
pip install cloudpss

# 从源码安装
pip install -e .
```

### 2. 配置Token

```bash
echo "your_token_here" > .cloudpss_token
```

### 3. 列出可用技能

```bash
python -m cloudpss_skills list
```

### 4. 初始化并运行

```bash
# 创建配置
python -m cloudpss_skills init power_flow --output pf.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config pf.yaml
```

## 技能设计文档

- [用户手册](user_manual.md) - 完整的用户操作指南
- [配置参考](config_reference.md) - 配置参数详细说明

## 典型工作流

### 工作流1: 模型创建与验证（新增）

```
component_catalog → model_builder → model_validator
```

**用途**: 发现组件 → 创建测试算例 → 验证模型有效性

**实际成果**: 已使用此工作流创建并清洗一批 IEEE39 扩展算例：
- 光伏模型 3个 (50/100/150MW)
- 风电模型 2个 (50/100MW)
- 混合新能源模型 1个
- 保护模型 3个 (差动/过流/零序)
- 线路模型 2个 (150/200km)
- 母线模型 1个

**当前说明**:
- `WGSource_Bus30` 旧样例已退役，不再计入主线可验证算例
- 2026-04-03 起，新能源主线以修复后的 CloudPSS 分支为准

### 工作流2: 电压稳定分析与补偿设计

```
vsi_weak_bus → reactive_compensation_design → disturbance_severity
```

### 工作流3: N-1安全校核

```
n1_security → contingency_analysis → result_compare
```

### 工作流4: 故障分析

```
ieee3_prep → emt_fault_study → disturbance_severity → visualize
```

### 工作流5: 批量仿真

```
batch_task_manager → hdf5_export → result_compare
```

## Agent使用指南

每个技能文档包含:

1. **概述** - 技能功能和适用场景
2. **设计原理** - 算法和工作流程
3. **快速开始** - CLI和Python API示例
4. **配置Schema** - 完整的配置参数说明
5. **Agent使用指南** - 程序化调用方式
6. **输出结果** - 结果数据结构
7. **与其他技能的关联** - 技能组合建议

## 文档规范

所有技能文档遵循统一结构:

```markdown
# 技能名称

## 概述
## 功能特性
## 设计原理
## 快速开始
## 配置Schema
## Agent使用指南
## 输出结果
## 与其他技能的关联
## 性能特点
## 常见问题
## 版本信息
```

这样设计确保**人**可以通过示例快速上手，**Agent**可以通过Schema理解接口契约。

## 更多信息

- [项目总结](../../PROJECT_SUMMARY.md) - 完整项目成果
- [开发日志](../development/vsi_development_summary.md) - 开发过程记录
