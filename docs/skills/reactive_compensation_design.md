# 无功补偿设计技能 (Reactive Compensation Design)

## 设计背景

### 研究对象

无功功率是电力系统中与电压支撑和电能质量密切相关的重要物理量。系统无功功率不足或分布不合理会导致电压下降、电能质量恶化，严重时可能引发电压崩溃。无功补偿设计技能用于根据电压稳定性分析结果（如VSI弱母线分析），自动设计无功补偿方案，通过合理配置无功补偿设备（同步调相机、SVG、SVC、电容器组）来改善系统电压稳定性。

### 实际需求

在电力系统规划、设计和运行中，无功补偿设计具有以下重要作用：

1. **电压稳定提升**: 通过无功补偿提高系统电压稳定裕度
2. **弱母线治理**: 针对VSI分析识别的弱母线进行重点补偿
3. **设备选型优化**: 根据系统需求选择合适的补偿设备类型和容量
4. **投资效益分析**: 评估不同补偿方案的技术经济性能
5. **运行方式优化**: 确定补偿设备的运行策略和控制参数
6. **新能源接入支持**: 为大规模新能源并网提供电压支撑

### 期望的输入和输出

**输入**:
- VSI弱母线分析结果文件（JSON格式）
- 系统模型（IEEE标准系统或实际系统）
- 补偿设备类型选择（同步调相机/SVG/SVC/电容器组）
- 设备容量参数（初始/最大/最小容量）
- 迭代优化参数（仅调相机需要）
- 验证场景配置（N-1故障等）

**输出**:
- 补偿方案设计结果（各母线补偿容量）
- 设备详细参数配置
- 迭代优化历史（仅调相机）
- DV电压裕度验证结果
- 补偿前后对比分析
- 最终补偿方案CSV文件

### 计算结果的用途和价值

无功补偿设计结果可直接用于：
- 确定无功补偿设备的安装位置和容量配置
- 评估补偿方案对系统电压稳定性的改善效果
- 进行多方案技术经济比较，优化投资决策
- 指导补偿设备的控制参数整定
- 验证补偿方案在N-1故障等极端工况下的有效性
- 为工程设计和设备采购提供技术依据

## 功能特性

- **VSI结果读取**: 自动读取VSI弱母线分析结果，识别需要补偿的母线
- **多设备支持**: 支持同步调相机、SVG、SVC、电容器组四种补偿设备
- **自动容量优化**: 基于DV电压裕度指标自动迭代优化补偿容量（调相机）
- **N-1故障验证**: 配置故障场景验证补偿效果
- **完整方案输出**: 输出补偿容量、设备参数、迭代历史、收敛状态
- **设备参数模板**: 提供标准设备参数模板，支持自定义配置
- **方案对比分析**: 支持不同设备类型和容量的方案对比

## 当前实现说明

- 调相机路径已改为优先复用模型内已有同步机控制模板，而不是继续使用“同步机本体 + 单引脚 AVR”的错误简化接法。
- `simulation.fault_time` / `fault_duration` 当前会真正回写到模型故障元件，而不只是影响后处理。
- `iteration.dv_judge_criteria` 当前会真实参与分时间窗 DV 判定。

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init reactive_compensation_design --output rcd.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config rcd.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("reactive_compensation_design")

# 配置（同步调相机示例）
config = {
    "skill": "reactive_compensation_design",
    "auth": {
        "token_file": ".cloudpss_token"
    },
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
        "device_type": "sync_compensator",
        "initial_capacity": 100,
        "max_capacity": 800,
        "min_capacity": 10,
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
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "reactive_compensation",
        "timestamp": True
    }
}

# 验证配置
validation = skill.validate(config)
if not validation.valid:
    print("配置错误:", validation.errors)

# 运行
result = skill.run(config)
print(f"状态: {result.status}")
print(f"数据: {result.data}")
```

### 3.3 YAML配置示例

**同步调相机配置**:

```yaml
skill: reactive_compensation_design
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

vsi_input:
  vsi_result_file: ./results/vsi_weak_bus_result.json
  vsi_threshold: 0.01
  max_buses: 5
  # target_buses:  # 或指定具体母线
  #   - Bus_16
  #   - Bus_15

compensation:
  device_type: sync_compensator  # 同步调相机
  initial_capacity: 100          # 初始容量(MVar)
  max_capacity: 800              # 最大容量(MVar)
  min_capacity: 10               # 最小容量(MVar)
  avr_k: 30                      # AVR增益
  avr_ka: 14.2                   # AVR放大倍数

simulation:
  fault_bus: Bus_16              # 故障母线
  fault_type: three_phase        # 三相短路
  fault_time: 4.0                # 故障时刻(s)，应与模型内故障元件时序一致

iteration:
  max_iterations: 20             # 最大迭代次数
  convergence_threshold: 0.5     # 收敛阈值(MVar)
  speed_ratio: 0.2               # 迭代加速比

output:
  format: json
  path: ./results/
  prefix: reactive_compensation
  timestamp: true
```

**SVG配置**:

```yaml
skill: reactive_compensation_design
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

vsi_input:
  vsi_result_file: ./results/vsi_weak_bus_result.json
  vsi_threshold: 0.01
  max_buses: 5

compensation:
  device_type: svg               # SVG静止无功发生器
  initial_capacity: 100          # 配置容量(MVar)
  response_time: 0.02            # 响应时间(s)
  control_mode: voltage_control  # 电压控制模式

simulation:
  fault_bus: Bus_16
  fault_type: three_phase
  fault_time: 4.0

iteration:
  max_iterations: 0              # SVG不需要迭代

output:
  format: json
  path: ./results/
  prefix: svg_compensation
  timestamp: true
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: reactive_compensation_design   # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token（不推荐）
  token_file: string                  # token文件路径（默认: .cloudpss_token）

model:                                # 模型配置（必需）
  rid: string                         # 模型RID或本地路径（必需）
  source: enum                        # cloud | local（默认: cloud）

vsi_input:                            # VSI输入配置（必需）
  vsi_result_file: string             # VSI结果文件路径（必需）
  vsi_threshold: number               # 弱母线VSI阈值（默认: 0.01）
  max_buses: integer                  # 最大补偿母线数（默认: 5）
  target_buses: array                 # 直接指定补偿母线（可选）

compensation:                         # 补偿配置（必需）
  device_type: enum                   # sync_compensator | svg | svc | capacitor
  initial_capacity: number            # 初始/配置容量(MVar)（默认: 100）
  max_capacity: number                # 最大容量(MVar)（调相机默认: 800）
  min_capacity: number                # 最小容量(MVar)（调相机默认: 10）
  avr_k: number                       # AVR增益（调相机默认: 30）
  avr_ka: number                      # AVR放大倍数（调相机默认: 14.2）
  response_time: number               # 响应时间(s)（SVG/SVC默认: 0.02）
  control_mode: enum                  # voltage_control | reactive_power_control

simulation:                           # 仿真验证配置（可选）
  fault_bus: string                   # 故障母线
  fault_type: enum                    # three_phase | single_phase | line_ground
  fault_time: number                  # 故障时刻(s)
  duration: number                    # 故障持续时间(s)（默认: 0.1）

iteration:                            # 迭代优化配置（仅调相机）
  max_iterations: integer             # 最大迭代次数（默认: 20）
  convergence_threshold: number       # 收敛阈值(MVar)（默认: 0.5）
  speed_ratio: number                 # 迭代加速比（默认: 0.2）

output:                               # 输出配置
  format: enum                        # json | csv（默认: json）
  path: string                        # 输出目录（默认: ./results/）
  prefix: string                      # 文件名前缀（默认: reactive_compensation）
  timestamp: boolean                  # 是否添加时间戳（默认: true）
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"reactive_compensation_design" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `vsi_input.vsi_result_file` | string | 是 | - | VSI分析结果JSON文件路径 |
| `vsi_input.vsi_threshold` | number | 否 | 0.01 | 弱母线VSI阈值 |
| `vsi_input.max_buses` | integer | 否 | 5 | 最大补偿母线数 |
| `vsi_input.target_buses` | array | 否 | [] | 直接指定补偿母线标签列表 |
| `compensation.device_type` | enum | 否 | sync_compensator | 补偿设备类型 |
| `compensation.initial_capacity` | number | 否 | 100 | 初始/配置容量(MVar) |
| `compensation.max_capacity` | number | 否 | 800 | 最大容量(MVar，仅调相机) |
| `compensation.min_capacity` | number | 否 | 10 | 最小容量(MVar，仅调相机) |
| `compensation.avr_k` | number | 否 | 30 | AVR增益(仅调相机) |
| `compensation.avr_ka` | number | 否 | 14.2 | AVR放大倍数(仅调相机) |
| `compensation.response_time` | number | 否 | 0.02 | 响应时间(s，SVG/SVC) |
| `compensation.control_mode` | enum | 否 | voltage_control | 控制模式 |
| `simulation.fault_bus` | string | 否 | - | 故障母线标签 |
| `simulation.fault_type` | enum | 否 | three_phase | 故障类型 |
| `simulation.fault_time` | number | 否 | 4.0 | 故障时刻(s)。应与模型内故障元件时序一致 |
| `simulation.duration` | number | 否 | 0.1 | 故障持续时间(s) |
| `iteration.max_iterations` | integer | 否 | 20 | 最大迭代次数(仅调相机) |
| `iteration.convergence_threshold` | number | 否 | 0.5 | 收敛阈值(MVar) |
| `iteration.speed_ratio` | number | 否 | 0.2 | 迭代加速比 |

### DV判据说明

- `iteration.dv_judge_criteria` 采用 `[窗口起点, 窗口终点, 电压下限倍率, 电压上限倍率]` 格式。
- 当前实现会先从三相瞬时波形合成 RMS，再按各时间窗执行判据。
- 因此该参数会直接影响技能最终返回 `SUCCESS` 还是 `FAILED`。
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | reactive_compensation | 文件名前缀 |
| `output.timestamp` | boolean | 否 | true | 文件名是否包含时间戳 |

## Agent使用指南

### 5.1 基本调用模式

```python
# 获取技能实例
skill = get_skill("reactive_compensation_design")

# 最小化配置（使用默认值）
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "vsi_input": {
        "vsi_result_file": "./results/vsi_weak_bus_result.json"
    },
    "compensation": {
        "device_type": "sync_compensator"
    }
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status == "SUCCESS":
        print(f"设计完成: {result.data}")
    else:
        print(f"设计失败: {result.error}")
```

### 5.2 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data

    # 访问补偿方案
    target_buses = data.get("target_buses", [])
    final_capacities = data.get("final_capacities", [])
    print(f"补偿母线: {target_buses}")
    print(f"补偿容量: {final_capacities} MVar")

    # 访问迭代历史（仅调相机）
    iteration_history = data.get("iteration_history", [])
    print(f"迭代次数: {len(iteration_history)}")
    for hist in iteration_history:
        print(f"  迭代{hist['iteration']}: {hist['capacities']}")

    # 访问收敛状态
    converged = data.get("converged", False)
    print(f"是否收敛: {converged}")

    # 访问DV验证结果
    dv_results = data.get("dv_results", [])
    for dv in dv_results:
        print(f"母线{dv['bus']}: DV_down={dv['dv_down']:.4f}, DV_up={dv['dv_up']:.4f}")

    # 访问输出文件
    for artifact in result.artifacts:
        print(f"输出文件: {artifact.path} ({artifact.type})")

# 查看日志
for log in result.logs:
    print(f"[{log.level}] {log.message}")
```

### 5.3 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    error_msg = result.error

    # 常见错误处理
    if "VSI结果文件不存在" in error_msg:
        print("错误: 请检查vsi_result_file路径")
    elif "Token文件不存在" in error_msg:
        print("错误: 请创建.cloudpss_token文件")
    elif "模型不存在" in error_msg:
        print("错误: 请检查模型RID是否正确")
    elif "容量不收敛" in error_msg:
        print("错误: 增加max_capacity或减少补偿母线数量")
    elif "仿真失败" in error_msg:
        print("错误: 检查模型配置和故障参数")
    elif "设备类型不支持" in error_msg:
        print("错误: 支持的类型: sync_compensator, svg, svc, capacitor")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "model_rid": "model/holdme/IEEE39",
  "device_type": "sync_compensator",
  "target_buses": ["Bus_16", "Bus_15"],
  "final_capacities": [150.5, 120.3],
  "iterations": 8,
  "converged": true,
  "compensation_scheme": [
    {
      "bus_label": "Bus_16",
      "capacity_mvar": 150.5,
      "voltage_kv": 230,
      "vsi": 0.0152
    },
    {
      "bus_label": "Bus_15",
      "capacity_mvar": 120.3,
      "voltage_kv": 230,
      "vsi": 0.0128
    }
  ],
  "iteration_history": [
    {
      "iteration": 1,
      "capacities": [100.0, 100.0],
      "upper_violations": 0,
      "lower_violations": 2,
      "max_dv": 0.85
    },
    {
      "iteration": 8,
      "capacities": [150.5, 120.3],
      "upper_violations": 0,
      "lower_violations": 0,
      "max_dv": 0.92
    }
  ],
  "dv_results": [
    {
      "bus": "Bus_16",
      "dv_down": 0.15,
      "dv_up": 0.08,
      "status": "ok"
    }
  ],
  "simulation_config": {
    "fault_bus": "Bus_16",
    "fault_type": "three_phase",
    "fault_time": 4.0
  }
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "reactive_compensation_design" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典，包含补偿方案、迭代历史、DV结果 |
| `artifacts` | list | 输出文件列表（Artifact对象），包含JSON和CSV方案文件 |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标，包括迭代耗时 |

## 设计原理

### 工作流程

```
1. VSI结果读取
   ├── 读取VSI分析结果JSON文件
   ├── 解析弱母线列表
   ├── 根据vsi_threshold筛选
   └── 应用max_buses限制

2. 设备模型选择
   ├── sync_compensator: 同步调相机
   │   ├── 调相机本体参数
   │   ├── 升压变压器
   │   └── AVR调压器
   ├── svg: 静止无功发生器
   ├── svc: 静止无功补偿器
   └── capacitor: 电容器组

3. 补偿方案初始化
   ├── 在目标母线添加补偿设备
   ├── 设置初始容量
   └── 配置设备参数

4. 故障场景配置（如启用）
   ├── 设置故障母线
   ├── 设置故障类型
   └── 设置故障时刻和持续时间

5. 迭代优化（仅调相机）
   ├── 运行EMT仿真
   ├── 计算DV电压裕度
   │   ├── DV_up = V_max - V_peak
   │   └── DV_down = V_min - V_valley
   ├── 检查电压约束
   │   ├── DV_up < 0: 电压上限违规
   │   └── DV_down < 0: 电压下限违规
   ├── 调整容量
   │   ├── 违规时: Q_new = Q + ΔQ
   │   └── ΔQ = -DV × Q × speed_ratio
   └── 检查收敛条件
       ├── 无电压违规
       └── |ΔQ| < convergence_threshold

6. 结果输出
   ├── 生成补偿方案
   ├── 输出迭代历史
   └── 保存配置文件
```

### 设备参数

**同步调相机 (SyncGeneratorRouter)**:

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

**变压器 (_newTransformer_3p2w)**:

```python
{
    "Tmva": "100",      # 容量(MVA)
    "v": "230",         # 电压(kV)
    "R": "0.01",        # 电阻(pu)
    "X": "0.1"          # 电抗(pu)
}
```

**AVR调压器 (_PSASP_AVR_11to12)**:

```python
{
    "K": "30",          # 增益
    "KA": "14.2",       # 放大倍数
    "TA": "0.01"        # 时间常数
}
```

**SVG (静止无功发生器)**:

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

**SVC (静止无功补偿器)**:

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

## 与其他技能的关联

```
vsi_weak_bus
    ↓ (VSI结果)
reactive_compensation_design
    ↓ (补偿方案)
emt_simulation / disturbance_severity
    ↓ (验证补偿效果)
结果对比
```

### 依赖关系

- **必需依赖**: CloudPSS SDK (`cloudpss`)
- **输入依赖**:
  - `vsi_weak_bus`: 提供弱母线分析结果
  - `power_flow`: 提供基础潮流数据
- **输出被依赖**:
  - `emt_simulation`: 验证补偿方案效果
  - `disturbance_severity`: 评估补偿后系统稳定性
  - `result_compare`: 对比补偿前后效果

## 性能特点

- **迭代时间**: 仅调相机需要迭代，每次迭代运行EMT仿真约3-5分钟
- **总时间**:
  - 调相机: 10-20次迭代需30-60分钟
  - SVG/SVC: 无需迭代，几分钟完成
- **收敛性**: 大部分情况下5-10次迭代即可收敛
- **容量范围**: 支持10-800MVar容量配置
- **建议**: SVG/SVC设置max_iterations=0直接使用配置容量

## 常见问题

### 问题1: 容量不收敛

**原因**:
- 系统电压问题严重，需要很大容量
- max_capacity设置过小
- 补偿母线数量过多

**解决**:
```yaml
compensation:
  max_capacity: 1200    # 增加最大容量
iteration:
  max_iterations: 30   # 增加最大迭代次数
  speed_ratio: 0.3     # 增加加速比
```

### 问题2: 仿真失败

**原因**:
- 模型配置错误
- 不支持调相机设备
- 故障参数不合理

**解决**:
- 检查模型RID和组件类型
- 使用SVG/SVC替代调相机测试
- 调整fault_time避免与仿真起始冲突

### 问题3: DV计算异常

**原因**:
- EMT结果中没有电压量测
- 仿真时间过短
- 数据异常

**解决**:
- 检查仿真配置和输出通道
- 增加仿真时长
- 检查模型数据完整性

### 问题4: 迭代次数过多仍未收敛

**原因**:
- 系统不稳定
- 初始容量设置不当
- 收敛阈值过严

**解决**:
```yaml
compensation:
  initial_capacity: 200   # 增加初始容量
iteration:
  convergence_threshold: 1.0  # 放宽收敛条件
```

### 问题5: VSI结果文件格式错误

**原因**:
- 文件路径错误
- JSON格式损坏
- 缺少必要字段

**解决**:
- 确认vsi_result_file路径正确
- 检查JSON文件格式
- 确保包含weak_buses字段

## 完整示例

### 场景描述

某电力公司对IEEE39系统进行VSI弱母线分析后，发现Bus_16和Bus_15的VSI指标较高（分别为0.0152和0.0128），需要进行无功补偿。现设计同步调相机补偿方案，通过迭代优化确定最佳补偿容量，使系统满足电压稳定性要求。

### 配置文件

```yaml
skill: reactive_compensation_design
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

vsi_input:
  vsi_result_file: ./results/vsi_ieee39_result.json
  vsi_threshold: 0.01
  max_buses: 5

compensation:
  device_type: sync_compensator
  initial_capacity: 100
  max_capacity: 500
  min_capacity: 50
  avr_k: 30
  avr_ka: 14.2

simulation:
  fault_bus: Bus_16
  fault_type: three_phase
  fault_time: 4.0
  duration: 0.1

iteration:
  max_iterations: 20
  convergence_threshold: 0.5
  speed_ratio: 0.2

output:
  format: json
  path: ./results/
  prefix: rc_ieee39
  timestamp: true
```

### 执行命令

```bash
# 先运行VSI分析
python -m cloudpss_skills run --config vsi_config.yaml

# 再运行无功补偿设计
python -m cloudpss_skills run --config reactive_compensation.yaml
```

### 预期输出

```
[INFO] 加载认证信息...
[INFO] 认证成功
[INFO] 读取VSI结果: ./results/vsi_ieee39_result.json
[INFO] 识别到2个弱母线: Bus_16, Bus_15
[INFO] 设备类型: sync_compensator
[INFO] 开始迭代优化...
[INFO] [1/20] 容量: [100.0, 100.0], 违规: 2
[INFO] [2/20] 容量: [125.0, 115.0], 违规: 1
...
[INFO] [8/20] 容量: [150.5, 120.3], 违规: 0, 已收敛
[INFO] 迭代完成，共8次迭代
[INFO] 最终补偿容量: Bus_16=150.5MVar, Bus_15=120.3MVar
[INFO] 结果已保存: ./results/rc_ieee39_20240324_143245_result.json
[INFO] 方案已保存: ./results/rc_ieee39_20240324_143245_scheme.csv
```

### 结果文件

**JSON结果文件** (`rc_ieee39_20240324_143245_result.json`):

```json
{
  "model_rid": "model/holdme/IEEE39",
  "device_type": "sync_compensator",
  "target_buses": ["Bus_16", "Bus_15"],
  "final_capacities": [150.5, 120.3],
  "iterations": 8,
  "converged": true,
  "compensation_scheme": [
    {
      "bus_label": "Bus_16",
      "capacity_mvar": 150.5,
      "voltage_kv": 230,
      "vsi": 0.0152
    },
    {
      "bus_label": "Bus_15",
      "capacity_mvar": 120.3,
      "voltage_kv": 230,
      "vsi": 0.0128
    }
  ],
  "iteration_history": [
    {"iteration": 1, "capacities": [100.0, 100.0], "upper_violations": 0, "lower_violations": 2},
    {"iteration": 8, "capacities": [150.5, 120.3], "upper_violations": 0, "lower_violations": 0}
  ],
  "dv_results": [
    {"bus": "Bus_16", "dv_down": 0.15, "dv_up": 0.08, "status": "ok"},
    {"bus": "Bus_15", "dv_down": 0.12, "dv_up": 0.06, "status": "ok"}
  ]
}
```

**CSV方案文件** (`rc_ieee39_20240324_143245_scheme.csv`):

| 母线名称 | 母线Key | 补偿容量(MVar) | 电压(kV) | VSI |
|----------|---------|----------------|----------|-----|
| Bus_16   | bus_16  | 150.50         | 230.00   | 0.015200 |
| Bus_15   | bus_15  | 120.30         | 230.00   | 0.012800 |

### 后续应用

1. **效果验证**: 运行`emt_simulation`或`disturbance_severity`验证补偿效果
2. **方案对比**: 对比SVG/SVC方案的补偿效果和成本
3. **工程实施**: 根据CSV方案进行设备选型和工程设计
4. **运行优化**: 根据迭代历史优化控制参数

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
