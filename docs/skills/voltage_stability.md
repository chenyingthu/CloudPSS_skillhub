# 电压稳定分析技能 (Voltage Stability)

## 概述

电压稳定分析技能用于评估电力系统的电压稳定性，通过连续潮流或崩溃点分析，识别电压稳定极限和薄弱区域。

## 功能特性

- **连续潮流分析**: 逐步增加负荷直到电压崩溃
- **P-V曲线生成**: 绘制母线电压-负荷功率曲线
- **稳定裕度计算**: 计算电压稳定储备系数
- **薄弱点识别**: 识别电压稳定薄弱环节

## 设计原理

### 电压稳定性

电压稳定性是指系统在受到扰动后，能够维持所有母线电压在可接受范围内的能力。

### 分析方法

```
1. 基础潮流计算
2. 增加负荷（逐步增加负荷率）
3. 运行潮流计算
4. 记录母线电压
5. 检查收敛性
6. 重复直到不收敛（崩溃点）
7. 分析P-V曲线和稳定裕度
```

## 快速开始

### 1. YAML配置

```yaml
skill: voltage_stability
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  method: continuous_power_flow  # 分析方法
  load_increase_rate: 0.05      # 负荷增长率
  max_load_factor: 2.0          # 最大负荷倍数
  target_buses: []              # 目标母线，空表示全部

output:
  format: json
  path: ./results/
  prefix: voltage_stability
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("voltage_stability")

config = {
    "skill": "voltage_stability",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "load_increase_rate": 0.05,
        "max_load_factor": 2.0
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "voltage_stability" |
| `model.rid` | string | 是 | - | 模型RID |
| `analysis.method` | enum | 否 | continuous_power_flow | 分析方法 |
| `analysis.load_increase_rate` | number | 否 | 0.05 | 负荷增长率 |
| `analysis.max_load_factor` | number | 否 | 2.0 | 最大负荷倍数 |
| `analysis.target_buses` | array | 否 | [] | 目标母线列表 |
| `output.format` | enum | 否 | json | json / csv |
| `output.path` | string | 否 | ./results/ | 输出目录 |

## 输出结果

### JSON结果

```json
{
  "model_rid": "model/holdme/IEEE39",
  "stability_limit": 1.85,
  "weak_buses": ["Bus_16", "Bus_15"],
  "pv_curves": {
    "Bus_16": [
      {"load_factor": 1.0, "voltage": 1.02},
      {"load_factor": 1.5, "voltage": 0.95}
    ]
  }
}
```

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
