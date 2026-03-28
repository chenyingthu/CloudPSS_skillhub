# 扰动严重度分析技能 (Disturbance Severity Analysis)

基于PSA Skills S04实现，评估电力系统故障后的电压恢复特性。

## 功能特性

- **DV (Deviation from Voltage)**: 电压裕度分析，评估电压偏离稳态的程度
- **SI (Severity Index)**: 故障严重度指数，综合评估电压跌落深度和持续时间
- **薄弱点识别**: 自动识别电压恢复特性差的母线

## 快速开始

### 1. 基本使用

```python
from cloudpss_skills import SkillRegistry

# 获取技能
skill = SkillRegistry.get("disturbance_severity")

# 配置分析
config = {
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "simulation": {
        "fault_bus": "Bus_16",
        "fault_type": "three_phase",
        "fault_time": 4.0,
        "fault_duration": 0.1
    },
    "analysis": {
        "dv_enabled": True,
        "si_enabled": True,
        "voltage_measure_plot": 0
    }
}

# 运行分析
result = skill.run(config)
```

### 2. 使用配置文件

```bash
python -m cloudpss_skills run --config config/disturbance_severity.yaml
```

### 3. 验证测试

```bash
python tests/verify_disturbance_severity.py
```

## 核心指标说明

### DV (Voltage Deviation Margin)

电压裕度指标，表示电压相对于稳态值的偏离程度：

- **DV上限裕度** (`dv_up`): `V_max_limit - V_max_actual`
  - 正值：电压有裕度
  - 负值：电压越上限

- **DV下限裕度** (`dv_down`): `V_min_actual - V_min_limit`
  - 正值：电压有裕度
  - 负值：电压越下限

### SI (Severity Index)

故障严重度指数，综合评估电压跌落深度和持续时间：

- **SI = 0**: 无电压问题
- **0 < SI < 0.5**: 轻度严重
- **0.5 ≤ SI < 1.0**: 中度严重
- **SI ≥ 1.0**: 严重

计算公式基于两段式电压偏差积分：
- 第一段：故障清除后短时间（高阈值）
- 第二段：长期恢复过程（低阈值）

## 输出结果

### JSON结果 (`*_result.json`)

```json
{
  "model_rid": "model/holdme/IEEE39",
  "disturbance_time": 4.0,
  "channel_count": 39,
  "channel_results": [
    {
      "name": "Bus_16",
      "dv": {
        "dv_up": 0.05,
        "dv_down": -0.12,
        "v_steady": 1.02
      },
      "si": 0.65
    }
  ],
  "weak_points": [
    {
      "name": "Bus_16",
      "reason": "电压下限裕度不足 (-0.12); 严重度指数较高 (SI=0.65)",
      "dv_up": 0.05,
      "dv_down": -0.12,
      "si": 0.65
    }
  ],
  "summary": {
    "total_channels": 39,
    "dv_up": {"min": -0.15, "max": 0.25, "mean": 0.08, "negative_count": 5},
    "dv_down": {"min": -0.25, "max": 0.15, "mean": -0.05, "negative_count": 8},
    "si": {"min": 0.0, "max": 1.2, "mean": 0.35, "high_count": 6}
  }
}
```

### CSV汇总 (`*_result.csv`)

| 通道名称 | DV上限裕度 | DV下限裕度 | 稳态电压 | SI严重度 | 是否薄弱 |
|----------|------------|------------|----------|----------|----------|
| Bus_16   | 0.05       | -0.12      | 1.02     | 0.65     | 是       |

### Markdown报告 (`*_report.md`)

包含完整的分析摘要、薄弱点列表和详细结果表格。

## 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model.rid` | string | - | 模型RID（必需） |
| `simulation.fault_bus` | string | - | 故障母线label |
| `simulation.fault_type` | enum | three_phase | 故障类型 |
| `simulation.fault_time` | float | 4.0 | 故障发生时间(s) |
| `analysis.dv_enabled` | bool | true | 启用DV计算 |
| `analysis.si_enabled` | bool | true | 启用SI计算 |
| `analysis.judge_criteria` | array | 见配置 | DV判断条件 |
| `analysis.si_dv1` | float | 0.25 | SI第一阶段阈值 |
| `analysis.si_dv2` | float | 0.1 | SI第二阶段阈值 |

## 与已有技能的关联

- **emt_simulation**: 本技能需要基于带故障的EMT仿真结果
- **transient_stability**: DV/SI与暂态稳定裕度互补
- **contingency_analysis**: 可批量评估N-K故障的严重度

## 参考实现

基于 [PSA Skills S04](https://git.tsinghua.edu.cn/yuanxuefeng/psa-skills-0.2.3) 的 `disturbance-severity-analysis` 技能实现。
