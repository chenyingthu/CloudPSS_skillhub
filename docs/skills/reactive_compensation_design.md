# 无功补偿设计技能

基于VSI弱母线分析结果，自动设计无功补偿方案，支持同步调相机、SVG（静止无功发生器）、SVC（静止无功补偿器）三种设备类型，迭代优化容量以满足电压裕度要求。

## 功能特性

- **VSI结果读取**: 自动识别需要补偿的弱母线
- **多种补偿设备**: 支持调相机、SVG、SVC、电容器组
- **故障场景仿真**: 配置N-1故障验证补偿效果
- **迭代容量优化**: 基于DV电压裕度自动调整容量（仅调相机）
- **完整方案输出**: 补偿容量、迭代历史、收敛状态

## 支持的补偿设备

| 设备类型 | 响应速度 | 特点 | 适用场景 |
|----------|----------|------|----------|
| **同步调相机** | 较慢（秒级） | 大容量、提供惯性支持、需AVR | 大容量补偿、系统稳定性要求高 |
| **SVG** | 快（毫秒级） | 响应极快、连续可调、无谐波 | 快速电压调节、精密控制 |
| **SVC** | 较快（几十毫秒） | 成本较低、技术成熟 | 中大容量补偿、经济型方案 |
| **电容器组** | 慢（分级投切） | 成本最低、阶梯调节、纯电容 | 功率因数校正、轻载补偿 |

## 快速开始

### 1. 基本使用（同步调相机）

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
        "device_type": "sync_compensator",  # 同步调相机
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

### 2. SVG配置示例

```python
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "vsi_input": {
        "vsi_result_file": "./results/vsi_weak_bus_result.json"
    },
    "compensation": {
        "device_type": "svg",           # SVG静止无功发生器
        "initial_capacity": 100,        # 容量(MVar)
        "response_time": 0.02,          # 响应时间(s)，毫秒级
        "control_mode": "voltage_control"  # 控制模式
    },
    "iteration": {
        "max_iterations": 0             # SVG不需要迭代优化
    }
}
```

### 3. SVC配置示例

```python
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "vsi_input": {
        "vsi_result_file": "./results/vsi_weak_bus_result.json"
    },
    "compensation": {
        "device_type": "svc",           # SVC静止无功补偿器
        "initial_capacity": 100,        # 容量(MVar)
        "response_time": 0.05,          # 响应时间(s)，几十毫秒
        "control_mode": "voltage_control"
    },
    "iteration": {
        "max_iterations": 0             # SVC不需要迭代优化
    }
}
```

### 4. 使用配置文件

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

3. 批量添加补偿设备
   根据device_type选择设备:
   ├── sync_compensator: 同步调相机+变压器+AVR
   ├── svg: SVG静止无功发生器
   └── svc: SVC静止无功补偿器

4. 配置故障场景
   └── 设置故障母线、类型、时间

5. 迭代优化（仅调相机）
   迭代k:
     ├── 更新调相机容量
     ├── 运行EMT仿真
     ├── 计算DV电压裕度
     ├── 检查收敛条件
     └── 调整容量（如有违规）
   直到收敛或达到最大迭代次数

   注意: SVG和SVC直接使用配置容量，不需要迭代优化

6. 输出方案
   └── 最终补偿容量
   └── 迭代历史（仅调相机）
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
| `compensation.device_type` | enum | sync_compensator | 设备类型: sync_compensator/svg/svc/capacitor |
| `compensation.initial_capacity` | float | 100 | 初始容量(MVar) |
| `compensation.max_capacity` | float | 800 | 最大容量(MVar) |
| `compensation.min_capacity` | float | 10 | 最小容量(MVar) |
| `compensation.avr_k` | float | 30 | AVR增益(仅调相机) |
| `compensation.avr_ka` | float | 14.2 | AVR放大倍数(仅调相机) |
| `compensation.response_time` | float | 0.02 | 响应时间(s)(SVG/SVC) |
| `compensation.control_mode` | enum | voltage_control | 控制模式: voltage_control/reactive_power_control |
| `simulation.fault_bus` | string | - | 故障母线 |
| `simulation.fault_type` | enum | three_phase | 故障类型 |
| `iteration.max_iterations` | int | 20 | 最大迭代次数(仅调相机) |
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

### SVG (静止无功发生器)

```python
{
    "Sn": "100",        # 额定容量(MVA)
    "Vn": "230",        # 额定电压(kV)
    "fn": "50",         # 额定频率(Hz)
    "Tresponse": "0.02", # 响应时间(s)
    "Vref": "1.0",      # 电压参考值(pu)
    "Qmin": "-100",     # 最小无功输出(MVar)
    "Qmax": "100",      # 最大无功输出(MVar)
    "mode": "1"         # 1-电压控制, 0-无功控制
}
```

### SVC (静止无功补偿器)

```python
{
    "Qmax": "100",      # 最大感性无功(MVar)
    "Qmin": "-100",     # 最大容性无功(MVar)
    "Vn": "230",        # 额定电压(kV)
    "fn": "50",         # 额定频率(Hz)
    "Tresponse": "0.05", # 响应时间(s)
    "Vref": "1.0",      # 电压参考值(pu)
    "slope": "0.05",    # 斜率(pu)
    "mode": "1"         # 1-电压控制, 0-无功控制
}
```

### 电容器组 (Capacitor Bank)

```python
{
    "Qn": "100",        # 总额定容量 (MVar)
    "Vn": "230",        # 额定电压 (kV)
    "fn": "50",         # 额定频率 (Hz)
    "steps": "5",       # 投切级数
    "Qstep": "20",      # 每级容量 (MVar) = Qn/steps
    "enabled": "1"      # 初始状态：1-投入，0-退出
}
```

电容器组特点:
- **成本最低**: 单位容量投资最小
- **分级投切**: 阶梯式调节，非连续
- **单向补偿**: 只能提供容性无功
- **无谐波**: 纯电容元件，不产生谐波
- **适用场景**: 功率因数校正、轻载电压支撑

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

### 1. 设备类型选择

| 场景 | 推荐设备 | 原因 |
|------|----------|------|
| 需要大容量补偿(>200MVar) | 同步调相机 | 大容量、提供惯性支持 |
| 需要快速电压调节 | SVG | 毫秒级响应、连续可调 |
| 成本敏感、中大容量 | SVC | 成本较低、技术成熟 |
| 成本敏感、小容量补偿 | 电容器组 | 成本最低、简单可靠 |
| 系统稳定性要求高 | 同步调相机 | 提供惯性支撑、短路容量 |

### 2. 设备特点对比

**同步调相机**
- ✅ 大容量、提供系统惯性
- ✅ 可双向调节（容性/感性）
- ✅ 提供短路容量支撑
- ❌ 响应较慢（秒级）
- ❌ 需要旋转部件维护

**SVG**
- ✅ 响应极快（毫秒级）
- ✅ 连续精确调节
- ✅ 无谐波污染
- ❌ 容量相对较小
- ❌ 成本较高

**SVC**
- ✅ 成本适中
- ✅ 响应较快（几十毫秒）
- ✅ 技术成熟可靠
- ❌ 产生谐波需滤波
- ❌ 容量分级调节

**电容器组**
- ✅ 成本最低
- ✅ 纯电容无谐波
- ✅ 结构简单、维护方便
- ❌ 分级投切（非连续调节）
- ❌ 只能提供容性无功（单向）
- ❌ 响应慢（秒级）

### 3. 先运行VSI分析

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

- **迭代时间**: 仅调相机需要迭代，每次迭代需运行EMT仿真，约需几分钟
- **总时间**:
  - 调相机: 10-20次迭代可能需要30-60分钟
  - SVG/SVC: 直接配置容量，无需迭代，几分钟完成
- **收敛性**: 仅调相机需要迭代收敛，大部分情况下5-10次即可收敛
- **建议**:
  - 调相机可先设置较小的max_iterations测试
  - SVG/SVC设置max_iterations=0，直接使用配置容量

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
