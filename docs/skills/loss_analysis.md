# 网损分析与优化技能 (Loss Analysis)

## 设计背景

### 研究对象

网损分析是电力系统经济运行研究的核心内容，用于计算电网在给定运行方式下的功率损耗分布。网损包括线路损耗和变压器损耗，反映了电网的输电效率和运行经济性。通过网损分析，可以识别高损耗设备，优化运行方式，降低供电成本。

### 实际需求

在电力系统规划和运行中，网损分析用于：

1. **经济运行评估**：评估当前运行方式的网损水平和经济性
2. **高损耗设备识别**：找出损耗最大的支路和变压器
3. **降损方案制定**：通过无功优化或机组组合降低网损
4. **规划方案比较**：比较不同规划方案的网损差异
5. **输电效率评估**：评估输电通道的传输效率

### 期望的输入和输出

**输入**：

- 电力系统模型（需完成潮流收敛）
- 网损计算组件（线路、变压器、静止无功补偿器）
- 灵敏度分析开关
- 优化方法选择

**输出**：

- 总网损（MW）
- 支路损耗明细
- 变压器损耗明细
- 网损灵敏度
- 无功优化降损建议
- 各设备损耗占比

### 计算结果的用途和价值

网损分析结果可用于：

- **运行方式优化**：调整发电机出力或变压器分接头降低网损
- **无功补偿规划**：确定无功补偿设备的安装位置和容量
- **设备改造决策**：优先改造高损耗设备
- **输电定价参考**：基于网损分摊输电成本

## 功能特性

- **支路损耗计算**：详细计算各输电线路的有功和无功损耗
- **变压器损耗分析**：区分铁芯损耗和铜损
- **全网损耗统计**：汇总各类设备的损耗，计算总网损
- **网损灵敏度分析**：计算各节点无功对网损的灵敏度
- **无功优化降损**：基于灵敏度分析提供降损建议
- **损耗排序输出**：按损耗大小排序，便于识别重点设备

## 快速开始

### 1. CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init loss_analysis --output loss_config.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config loss_config.yaml
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("loss_analysis")

config = {
    "skill": "loss_analysis",
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "loss_calculation": {
            "enabled": True,
            "components": ["lines", "transformers"]
        },
        "loss_sensitivity": {"enabled": True},
        "loss_optimization": {
            "enabled": True,
            "method": "reactive_power_optimization"
        }
    },
    "output": {"format": "json"}
}

result = skill.run(config)
summary = result.data["summary"]
print(f"总网损: {summary['total_loss_mw']:.2f} MW")
print(f"支路损耗: {summary['branch_loss_mw']:.2f} MW")
print(f"变压器损耗: {summary['transformer_loss_mw']:.2f} MW")
```

### 3. YAML配置示例

```yaml
skill: loss_analysis
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39

analysis:
  loss_calculation:
    enabled: true
    components: [lines, transformers]  # lines, transformers, shunts

  loss_sensitivity:
    enabled: true

  loss_optimization:
    enabled: true
    method: reactive_power_optimization  # 或 generation_dispatch

output:
  format: json
  path: ./results/
```

## 配置Schema

### 完整配置结构

```yaml
skill: loss_analysis                    # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token
  token_file: string                  # token文件路径

model:                                # 模型配置（必需）
  rid: string                         # 模型RID
  config_index: integer               # 配置索引

analysis:                             # 分析配置
  loss_calculation:                  # 损耗计算
    enabled: boolean                 # 是否启用
    components: [lines, transformers] # 计算组件
  loss_sensitivity:                  # 灵敏度分析
    enabled: boolean                 # 是否启用
  loss_optimization:                 # 优化建议
    enabled: boolean                 # 是否启用
    method: enum                      # reactive_power_optimization/generation_dispatch

output:                              # 输出配置
  format: enum                        # json/yaml
  path: string                        # 输出路径
```

### 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | "loss_analysis" |
| `auth.token` | string | 否 | - | API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件 |
| `model.rid` | string | 是 | - | 模型RID |
| `model.config_index` | integer | 否 | 0 | 配置索引 |
| `analysis.loss_calculation.enabled` | boolean | 否 | true | 启用损耗计算 |
| `analysis.loss_calculation.components` | array | 否 | [lines, transformers] | 计算组件 |
| `analysis.loss_sensitivity.enabled` | boolean | 否 | true | 启用灵敏度分析 |
| `analysis.loss_optimization.enabled` | boolean | 否 | true | 启用优化建议 |
| `analysis.loss_optimization.method` | enum | 否 | reactive_power_optimization | 优化方法 |

## Agent使用指南

### 基本调用模式

```python
from cloudpss_skills import get_skill

skill = get_skill("loss_analysis")

config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "loss_calculation": {"enabled": True},
        "loss_sensitivity": {"enabled": True},
    }
}

result = skill.run(config)

if result.status.value == "SUCCESS":
    data = result.data
    print(f"总网损: {data['summary']['total_loss_mw']:.2f} MW")
```

### 处理结果

```python
result = skill.run(config)

if result.status.value == "SUCCESS":
    data = result.data
    
    # 摘要
    summary = data["summary"]
    print(f"=== 网损摘要 ===")
    print(f"总有功损耗: {summary['total_loss_mw']:.2f} MW")
    print(f"支路损耗: {summary['branch_loss_mw']:.2f} MW ({summary['branch_loss_percent']:.1f}%)")
    print(f"变压器损耗: {summary['transformer_loss_mw']:.2f} MW ({summary['transformer_loss_percent']:.1f}%)")
    
    # 高损耗支路
    print(f"\n=== Top 5 高损耗支路 ===")
    for branch in data.get("top_loss_branches", [])[:5]:
        print(f"  {branch['label']}: {branch['p_loss_mw']:.2f} MW")
    
    # 优化建议
    print(f"\n=== 降损建议 ===")
    suggestions = data.get("optimization_suggestions", {})
    for bus, suggestion in suggestions.items():
        print(f"  {bus}: {suggestion['recommendation']}")
```

### 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    error_msg = result.error
    
    if "潮流" in error_msg:
        print("错误: 基线潮流未收敛")
    elif "Token" in error_msg:
        print("错误: 请检查认证配置")
    else:
        print(f"错误: {error_msg}")
```

## 输出结果

### JSON输出格式

```json
{
  "model": "model/holdme/IEEE39",
  "summary": {
    "total_loss_mw": 45.23,
    "branch_loss_mw": 38.12,
    "transformer_loss_mw": 7.11,
    "branch_loss_percent": 84.3,
    "transformer_loss_percent": 15.7,
    "loss_rate_percent": 3.2
  },
  "top_loss_branches": [
    {"label": "LINE_15", "p_loss_mw": 5.67, "loading_percent": 78.5},
    {"label": "LINE_23", "p_loss_mw": 4.32, "loading_percent": 65.2}
  ],
  "branch_losses": [...],
  "transformer_losses": [...],
  "optimization_suggestions": {
    "Bus_12": {
      "recommendation": "建议在Bus_12安装无功补偿装置",
      "estimated_loss_reduction_mw": 2.1,
      "sensitivity": 0.45
    }
  }
}
```

### SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | "loss_analysis" |
| `status` | SkillStatus | SUCCESS / FAILED |
| `data` | dict | summary、branch_losses、optimization_suggestions等 |
| `artifacts` | list | JSON结果文件 |

## 与其他技能的关联

```
power_flow
    ↓ (潮流收敛)
loss_analysis
    ↓ (网损统计)
    ├─ voltage_stability (电压分析)
    └─ reactive_compensation_design (无功补偿)
```

### 依赖关系

- **前置依赖**: `power_flow`（潮流收敛）
- **相关技能**:
  - `voltage_stability`: 电压稳定性分析
  - `reactive_compensation_design`: 无功补偿设计
  - `n1_security`: N-1安全分析

## 性能特点

- **计算时间**: 与系统规模成正比，通常秒级完成
- **精度**: 基于潮流计算结果，精度高
- **适用范围**: 适用于各种规模的电力系统

## 常见问题

### 问题1: 总网损为0

**原因**: 潮流计算未收敛或模型无损耗

**解决**: 检查潮流计算是否成功，确认模型包含阻抗参数

### 问题2: 支路损耗异常大

**原因**: 支路负载率过高或参数设置错误

**解决**: 检查支路负载率和阻抗参数

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2026-03-30
- **SDK要求**: cloudpss >= 4.5.28
