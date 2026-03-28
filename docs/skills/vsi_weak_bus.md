# VSI弱母线分析技能

基于动态无功注入的电压稳定敏感度分析，识别系统中电压稳定性薄弱的母线。

## 功能特性

- **动态无功注入**: 依次在各母线注入无功，测试电压响应
- **VSI指标计算**: 计算电压稳定指数（Voltage Stability Index）
- **弱母线识别**: 自动识别对无功变化敏感的薄弱母线
- **完整报告**: 生成JSON/CSV/Markdown多格式报告

## 快速开始

### 1. 基本使用

```python
from cloudpss_skills import get_skill

skill = get_skill("vsi_weak_bus")

config = {
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "vsi_setup": {
        "bus_filter": {
            "v_min": 0.6,
            "v_max": 300
        },
        "injection": {
            "v_base": 220,
            "q_base": 100,
            "start_time": 8.0,
            "interval": 1.5,
            "duration": 0.5
        }
    },
    "analysis": {
        "vsi_threshold": 0.01,
        "top_n": 10
    }
}

result = skill.run(config)
```

### 2. 使用配置文件

```bash
python -m cloudpss_skills run --config config/vsi_weak_bus.yaml
```

### 3. 运行示例

```bash
python examples/analysis/vsi_weak_bus_example.py
```

## VSI原理

### 计算公式

```
VSI_ij = (V_before - V_after) / Q_injected

VSI_i = mean(VSI_ij for all j)
```

其中：
- `V_before`: 注入无功前的电压
- `V_after`: 注入无功后的电压
- `Q_injected`: 注入的无功功率
- `i`: 注入无功的母线
- `j`: 观测电压变化的母线

### 物理意义

- **VSI越大**，表示母线对无功变化越敏感
- **VSI大的母线**电压稳定性差，容易发生电压崩溃
- **优先补偿**: VSI高的母线应优先安装无功补偿设备

## 工作流程

```
1. 筛选测试母线
   └── 按电压范围、名称关键字筛选

2. 添加VSI无功源
   └── 为每个母线添加shuntLC + 断路器 + 信号源

3. 配置时序
   └── 第k个母线在 T_start + k×interval 时刻注入无功

4. 运行EMT仿真
   └── 依次注入无功，记录电压变化

5. 计算VSI
   └── 提取电压变化，计算VSI指标

6. 识别弱母线
   └── 按VSI排序，输出薄弱母线列表
```

## 输出结果

### JSON结果 (`*_result.json`)

```json
{
  "model_rid": "model/holdme/IEEE39",
  "test_bus_count": 39,
  "vsi_results": {
    "vsi_i": {
      "Bus_16": 0.0152,
      "Bus_15": 0.0128,
      "Bus_26": 0.0115
    },
    "vsi_ij": {
      "Bus_16": {
        "Bus_16": 0.0152,
        "Bus_15": 0.0085,
        "Bus_26": 0.0072
      }
    }
  },
  "weak_buses": [
    {
      "label": "Bus_16",
      "vsi": 0.0152,
      "is_weak": true
    }
  ],
  "summary": {
    "total_buses": 39,
    "weak_bus_count": 1,
    "max_vsi": 0.0152,
    "min_vsi": 0.0021,
    "avg_vsi": 0.0065
  }
}
```

### CSV汇总 (`*_result.csv`)

| 母线名称 | VSI | 是否弱母线 |
|----------|-----|-----------|
| Bus_16   | 0.015234 | 是 |
| Bus_15   | 0.012856 | 是 |
| Bus_26   | 0.011523 | 否 |

### Markdown报告 (`*_report.md`)

- 摘要统计
- 弱母线列表
- VSI分布表

## 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model.rid` | string | - | 模型RID（必需） |
| `vsi_setup.bus_filter.v_min` | float | 0.6 | 母线最小电压筛选(kV) |
| `vsi_setup.bus_filter.v_max` | float | 300 | 母线最大电压筛选(kV) |
| `vsi_setup.injection.q_base` | float | 100 | 注入无功(MVar) |
| `vsi_setup.injection.start_time` | float | 8.0 | 开始时间(s) |
| `vsi_setup.injection.interval` | float | 1.5 | 每个母线测试时长(s) |
| `vsi_setup.injection.duration` | float | 0.5 | 无功注入持续时间(s) |
| `analysis.vsi_threshold` | float | 0.01 | 弱母线VSI阈值 |
| `analysis.top_n` | int | 10 | 输出前N个弱母线 |

## VSI阈值建议

| VSI范围 | 稳定性评估 | 建议措施 |
|---------|-----------|----------|
| VSI > 0.015 | 非常薄弱 | 立即安装补偿设备 |
| 0.01 < VSI ≤ 0.015 | 薄弱 | 优先补偿 |
| 0.005 < VSI ≤ 0.01 | 中等 | 经济分析后决定 |
| VSI ≤ 0.005 | 良好 | 无需补偿 |

## 与已有技能的关联

- **power_flow**: 用于获取母线电压和拓扑
- **emt_simulation**: VSI分析基于EMT仿真
- **disturbance_severity**: VSI结果可与DV/SI互补
- **reactive_compensation_design**: VSI结果指导补偿设计

## 性能注意事项

- **仿真时间**: 与母线数量成正比，每个母线约1.5s
- **39母线系统**: 约需60s仿真时间
- **建议**: 对大型系统可先筛选关键母线

## 参考实现

基于 [PSA Skills S05](https://git.tsinghua.edu.cn/yuanxuefeng/psa-skills-0.2.3) 的 `vsi-weak-bus-analysis` 技能实现。
