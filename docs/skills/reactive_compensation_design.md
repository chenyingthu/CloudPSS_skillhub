# 无功补偿设计技能

基于VSI弱母线分析结果，自动设计调相机补偿方案，迭代优化容量以满足电压裕度要求。

## 功能特性

- **VSI结果读取**: 自动识别需要补偿的弱母线
- **批量添加调相机**: 同步调相机 + 变压器 + AVR
- **故障场景仿真**: 配置N-1故障验证补偿效果
- **迭代容量优化**: 基于DV电压裕度自动调整容量
- **完整方案输出**: 补偿容量、迭代历史、收敛状态

## 快速开始

### 1. 基本使用

```python
from cloudpss_skills import get_skill

skill = get_skill("reactive_compensation_design")

config = {
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "vsi_input": {
        "vsi_result_file": "./results/vsi_weak_bus_result.json",
        "vsi_threshold": 0.01,
        "max_buses": 5
    },
    "compensation": {
        "initial_capacity": 100,
        "max_capacity": 800,
        "avr_k": 30,
        "avr_ka": 14.2
    },
    "simulation": {
        "fault_bus": "Bus_16",
        "fault_type": "three_phase",
        "fault_time": 4.0
    },
    "iteration": {
        "max_iterations": 20,
        "convergence_threshold": 0.5,
        "speed_ratio": 0.2
    }
}

result = skill.run(config)
```

### 2. 使用配置文件

```bash
python -m cloudpss_skills run --config config/reactive_compensation_design.yaml
```

### 3. 运行示例

```bash
python examples/analysis/reactive_compensation_design_example.py
```

## 工作流程

```
1. 读取VSI结果
   └── 从JSON文件加载或指定目标母线

2. 识别补偿目标
   └── 筛选VSI超过阈值的母线
   └── 限制最大补偿数量

3. 批量添加调相机
   └── 同步调相机（SyncGeneratorRouter）
   └── 变压器（_newTransformer_3p2w）
   └── AVR调压器（_PSASP_AVR_11to12）

4. 配置故障场景
   └── 设置故障母线、类型、时间

5. 迭代优化
   迭代k:
     ├── 更新调相机容量
     ├── 运行EMT仿真
     ├── 计算DV电压裕度
     ├── 检查收敛条件
     └── 调整容量（如有违规）
   直到收敛或达到最大迭代次数

6. 输出方案
   └── 最终补偿容量
   └── 迭代历史
   └── 收敛状态
```

## 迭代优化算法

### 容量调整策略

```
if DV_down < 0 (电压下限违规):
    ΔQ = -DV_down × Q_current × speed_ratio
    Q_new = Q_current + ΔQ

if DV_up < 0 (电压上限违规):
    ΔQ = -DV_up × Q_current × speed_ratio
    Q_new = Q_current - ΔQ

约束: min_capacity ≤ Q_new ≤ max_capacity
```

### 收敛条件

1. **电压裕度满足**: 无DV上限/下限违规
2. **调整量收敛**: max(|ΔQ|) < convergence_threshold
3. **最大迭代**: 达到max_iterations

## 输入输出

### 输入（VSI结果JSON）

```json
{
  "weak_buses": [
    {"label": "Bus_16", "vsi": 0.0152, "is_weak": true},
    {"label": "Bus_15", "vsi": 0.0128, "is_weak": true}
  ],
  "summary": {
    "total_buses": 39,
    "weak_bus_count": 5
  }
}
```

### 输出结果 (`*_result.json`)

```json
{
  "model_rid": "model/holdme/IEEE39",
  "target_buses": ["Bus_16", "Bus_15"],
  "final_capacities": [150.5, 120.3],
  "iterations": 5,
  "converged": true,
  "compensation_scheme": [
    {
      "bus_label": "Bus_16",
      "capacity_mvar": 150.5,
      "voltage_kv": 230,
      "vsi": 0.015
    }
  ],
  "iteration_history": [
    {
      "iteration": 1,
      "capacities": [100.0, 100.0],
      "upper_violations": 0,
      "lower_violations": 2
    }
  ],
  "dv_results": [...]
}
```

### CSV方案 (`*_scheme.csv`)

| 母线名称 | 母线Key | 补偿容量(MVar) | 电压(kV) | VSI |
|----------|---------|----------------|----------|-----|
| Bus_16   | bus_16  | 150.50         | 230.00   | 0.015200 |
| Bus_15   | bus_15  | 120.30         | 230.00   | 0.012800 |

## 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model.rid` | string | - | 模型RID（必需） |
| `vsi_input.vsi_result_file` | string | - | VSI结果文件路径 |
| `vsi_input.vsi_threshold` | float | 0.01 | 弱母线VSI阈值 |
| `vsi_input.max_buses` | int | 5 | 最大补偿母线数 |
| `vsi_input.target_buses` | list | - | 直接指定补偿母线 |
| `compensation.initial_capacity` | float | 100 | 初始容量(MVar) |
| `compensation.max_capacity` | float | 800 | 最大容量(MVar) |
| `compensation.min_capacity` | float | 10 | 最小容量(MVar) |
| `compensation.avr_k` | float | 30 | AVR增益 |
| `simulation.fault_bus` | string | - | 故障母线 |
| `simulation.fault_type` | enum | three_phase | 故障类型 |
| `iteration.max_iterations` | int | 20 | 最大迭代次数 |
| `iteration.convergence_threshold` | float | 0.5 | 收敛阈值(MVar) |
| `iteration.speed_ratio` | float | 0.2 | 迭代加速比 |

## 设备参数

### 同步调相机 (SyncGeneratorRouter)

```python
{
    "Smva": "100",      # 容量(MVA)
    "Vn": "230",        # 额定电压(kV)
    "fn": "50",         # 额定频率(Hz)
    "H": "6",           # 惯性时间常数(s)
    "xq": "1.5",        # q轴同步电抗
    "xd": "1.8",        # d轴同步电抗
    "ra": "0.005"       # 电枢电阻
}
```

### 变压器 (_newTransformer_3p2w)

```python
{
    "Tmva": "100",      # 容量(MVA)
    "v": "230",         # 电压(kV)
    "R": "0.01",        # 电阻(pu)
    "X": "0.1"          # 电抗(pu)
}
```

### AVR调压器 (_PSASP_AVR_11to12)

```python
{
    "K": "30",          # 增益
    "KA": "14.2",       # 放大倍数
    "TA": "0.01"        # 时间常数
}
```

## 与已有技能的关联

```
vsi_weak_bus
    ↓ (VSI结果)
reactive_compensation_design
    ↓ (补偿方案)
emt_simulation / disturbance_severity
    ↓ (验证补偿效果)
结果对比
```

## 使用建议

### 1. 先运行VSI分析

```bash
python -m cloudpss_skills run --config config/vsi_weak_bus.yaml
```

### 2. 再运行补偿设计

```bash
python -m cloudpss_skills run --config config/reactive_compensation_design.yaml
```

### 3. 最后验证效果

修改 `config/disturbance_severity.yaml` 中的模型为添加调相机后的模型，运行：

```bash
python -m cloudpss_skills run --config config/disturbance_severity.yaml
```

对比补偿前后的DV/SI指标。

## 性能注意事项

- **迭代时间**: 每次迭代需运行EMT仿真，约需几分钟
- **总时间**: 10-20次迭代可能需要30-60分钟
- **收敛性**: 大部分情况下5-10次迭代即可收敛
- **建议**: 可先设置较小的max_iterations测试，再增加迭代次数

## 故障排查

### 问题1: 容量不收敛

**原因**: 系统电压问题严重，需要很大容量
**解决**: 增加max_capacity或增加补偿母线数量

### 问题2: 仿真失败

**原因**: 模型配置错误或不支持调相机
**解决**: 检查模型RID和组件类型

### 问题3: DV计算异常

**原因**: EMT结果中没有电压量测或数据异常
**解决**: 检查仿真配置和结果输出

## 参考实现

基于 [PSA Skills S06](https://git.tsinghua.edu.cn/yuanxuefeng/psa-skills-0.2.3) 的 `reactive-compensation-design` 技能实现。
