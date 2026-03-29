# 短路电流计算技能 (Short Circuit)

## 设计背景

### 研究对象

短路电流计算是电力系统分析的基础工作，用于计算系统在故障条件下的短路电流水平。本技能基于EMT暂态仿真，通过在实际系统模型中设置故障点，运行暂态仿真，提取故障电流的峰值、稳态值和直流分量，为保护装置整定、设备选型和系统安全评估提供依据。

### 实际需求

在电力系统设计和运行中，短路电流计算用于：

1. **保护整定**：确定断路器、继电保护的动作电流阈值
2. **设备选型**：根据短路电流水平选择断路器、互感器等设备的额定参数
3. **母线强度评估**：评估母线结构的机械强度是否满足短路电动力要求
4. **接地设计**：确定接地装置的容量和接地电阻要求
5. **系统规划**：评估新增电源或线路对短路电流水平的影响
6. **安全分析**：评估系统短路容量是否超过设备额定值

### 期望的输入和输出

**输入**：

- 电力系统模型（需配置EMT拓扑和故障元件）
- 短路故障位置和类型（三相、单相接地、两相短路）
- 故障电阻和故障时间
- 监测电流和电压通道
- 基准值（基准电压、基准容量）
- 采样时间窗口

**输出**：

- 短路电流峰值（kA）
- 稳态短路电流（kA）
- 直流分量（kA）
- 时间常数（ms）
- 短路容量（MVA）
- 最低电压（标幺值）
- JSON/CSV/报告格式的完整结果

### 计算结果的用途和价值

短路电流结果可直接用于：

- **断路器选型**：选择额定开断电流大于短路电流峰值的断路器
- **保护整定**：设置过电流保护的动作值和时间特性
- **设备校验**：验证变压器、母线等设备的动热稳定性
- **短路容量评估**：计算系统的短路容量，评估系统强度
- **保护协调**：分析上下游保护的动作配合

## 功能特性

- **多种故障类型支持**：三相短路、单相接地短路、两相短路
- **精确故障建模**：支持故障电阻和故障时间配置
- **多通道监测**：同时监测多个电流和电压通道
- **完整电流分析**：提取峰值电流、稳态电流、直流分量
- **短路容量计算**：自动计算短路容量（MVA）
- **时间常数估算**：估算短路电流的衰减时间常数
- **电压跌落分析**：记录故障期间的最低电压
- **自动生成报告**：生成Markdown格式的分析报告
- **多格式输出**：支持JSON、CSV格式输出

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init short_circuit --output sc_config.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config sc_config.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("short_circuit")

# 配置
config = {
    "skill": "short_circuit",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "fault": {
        "location": "Bus7",
        "type": "three_phase",
        "resistance": 0.0001,
        "fs": 2.0,
        "fe": 2.1
    },
    "monitoring": {
        "current_channels": ["#Gen38.IT:0"],
        "voltage_channels": ["#Gen38.VT:0"]
    },
    "calculation": {
        "base_voltage": 500,
        "base_capacity": 100,
        "sample_window": [2.0, 2.05]
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "short_circuit",
        "generate_report": True
    }
}

# 验证配置
validation = skill.validate(config)
if not validation.valid:
    print("配置错误:", validation.errors)

# 运行
result = skill.run(config)
print(f"状态: {result.status}")
print(f"短路容量: {result.data.get('short_circuit_mva', {})}")
```

### 3.3 YAML配置示例

```yaml
skill: short_circuit
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

fault:
  location: Bus7              # 短路位置母线
  type: three_phase           # 故障类型：three_phase/line_to_ground/line_to_line
  resistance: 0.0001          # 故障电阻(Ω)
  fs: 2.0                     # 故障开始时间(s)
  fe: 2.1                     # 故障结束时间(s)

monitoring:
  current_channels:           # 监测电流通道
    - "#Gen38.IT:0"
    - "#Gen39.IT:0"
  voltage_channels:           # 监测电压通道
    - "#Gen38.VT:0"

calculation:
  base_voltage: 500           # 基准电压(kV)
  base_capacity: 100          # 基准容量(MVA)
  sample_window: [2.0, 2.05]  # 采样时间窗口[s]

output:
  format: json                # json | csv
  path: ./results/
  prefix: short_circuit
  generate_report: true       # 生成分析报告
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: short_circuit                   # 必需: 技能名称
auth:                                  # 认证配置
  token: string
  token_file: string                  # 默认: .cloudpss_token

model:                                 # 模型配置（必需）
  rid: string                         # 模型RID或本地路径
  source: enum                        # cloud | local

fault:                                 # 故障配置（必需）
  location: string                    # 短路位置母线ID
  type: enum                          # three_phase | line_to_ground | line_to_line
  resistance: number                  # 故障电阻(Ω)
  fs: number                          # 故障开始时间(s)
  fe: number                          # 故障结束时间(s)

monitoring:                            # 监测配置
  current_channels: array             # 电流通道列表
  voltage_channels: array             # 电压通道列表

calculation:                           # 计算配置
  base_voltage: number                # 基准电压(kV)
  base_capacity: number               # 基准容量(MVA)
  sample_window: array                # 采样时间窗口[s]

output:                                # 输出配置
  format: enum                        # json | csv
  path: string
  prefix: string
  generate_report: boolean            # 是否生成报告
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"short_circuit" |
| `auth.token` | string | 否 | - | API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地路径 |
| `model.source` | enum | 否 | cloud | cloud/local |
| `fault.location` | string | 是 | - | 短路位置母线ID |
| `fault.type` | enum | 否 | three_phase | 故障类型 |
| `fault.resistance` | number | 否 | 0.0001 | 故障电阻(Ω) |
| `fault.fs` | number | 否 | 2.0 | 故障开始时间(s) |
| `fault.fe` | number | 否 | 2.1 | 故障结束时间(s) |
| `monitoring.current_channels` | array | 否 | [] | 监测电流通道列表 |
| `monitoring.voltage_channels` | array | 否 | [] | 监测电压通道列表 |
| `calculation.base_voltage` | number | 否 | 500 | 基准电压(kV) |
| `calculation.base_capacity` | number | 否 | 100 | 基准容量(MVA) |
| `calculation.sample_window` | array | 否 | [2.0, 2.05] | 采样时间窗口[s] |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.generate_report` | boolean | 否 | true | 生成报告 |

### 故障类型说明

| 故障类型 | 说明 | 适用场景 |
|----------|------|----------|
| `three_phase` | 三相短路 | 最严重故障，用于设备极限校验 |
| `line_to_ground` | 单相接地短路 | 最常见故障，用于接地保护整定 |
| `line_to_line` | 两相短路 | 不对称故障分析 |

## Agent使用指南

### 5.1 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("short_circuit")

# 最小化配置
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "fault": {
        "location": "Bus7",
        "type": "three_phase"
    }
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status.value == "SUCCESS":
        data = result.data
        print(f"短路位置: {data['fault_location']}")
        print(f"短路类型: {data['fault_type']}")
        for ch, analysis in data['analysis'].items():
            if 'peak_current' in analysis:
                print(f"  {ch}: 峰值={analysis['peak_current']:.2f}kA")
    else:
        print(f"失败: {result.error}")
```

### 5.2 处理结果

```python
result = skill.run(config)

if result.status.value == "SUCCESS":
    data = result.data

    # 基本信息
    print(f"模型: {data['model']}")
    print(f"短路位置: {data['fault_location']}")
    print(f"短路类型: {data['fault_type']}")
    print(f"故障电阻: {data['fault_resistance']} Ω")

    # 短路电流分析
    print("\n短路电流分析:")
    for ch, analysis in data['analysis'].items():
        if 'peak_current' in analysis:
            print(f"  通道 {ch}:")
            print(f"    峰值电流: {analysis['peak_current']:.4f} kA")
            print(f"    稳态电流: {analysis['steady_current']:.4f} kA")
            print(f"    直流分量: {analysis['dc_component']:.4f} kA")
            print(f"    时间常数: {analysis['time_constant']:.2f} ms")
        elif 'min_voltage' in analysis:
            print(f"  通道 {ch}: 最低电压={analysis['min_voltage']:.4f} pu")

    # 短路容量
    print("\n短路容量:")
    for ch, scc in data['short_circuit_mva'].items():
        print(f"  {ch}: {scc['short_circuit_mva']:.2f} MVA "
              f"(稳态电流: {scc['steady_current_ka']:.4f} kA)")

    # 访问输出文件
    for artifact in result.artifacts:
        print(f"文件: {artifact.path} ({artifact.type})")
```

### 5.3 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    error_msg = result.error

    if "Token文件不存在" in error_msg:
        print("错误: 请创建.cloudpss_token文件")
    elif "模型不存在" in error_msg:
        print("错误: 请检查模型RID是否正确")
    elif "EMT仿真失败" in error_msg:
        print("错误: EMT仿真失败，请检查模型是否已准备EMT拓扑")
    elif "未找到故障元件" in error_msg:
        print("错误: 模型未配置故障元件")
    elif "时间窗口" in error_msg:
        print("错误: 采样时间窗口设置不当，请调整sample_window")
    else:
        print(f"错误: {error_msg}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "model": "IEEE39",
  "fault_location": "Bus7",
  "fault_type": "three_phase",
  "fault_resistance": 0.0001,
  "base_voltage": 500,
  "base_capacity": 100,
  "analysis": {
    "#Gen38.IT:0": {
      "peak_current": 12.3456,
      "steady_current": 8.9012,
      "dc_component": 3.4444,
      "time_constant": 45.23
    },
    "#Gen38.VT:0": {
      "min_voltage": 0.2345
    }
  },
  "short_circuit_mva": {
    "#Gen38.IT:0": {
      "steady_current_ka": 8.9012,
      "short_circuit_mva": 7712.34
    }
  }
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "short_circuit" |
| `status` | SkillStatus | SUCCESS / FAILED |
| `data` | dict | 包含model、fault_location、analysis、short_circuit_mva等 |
| `artifacts` | list | JSON结果、CSV数据、Markdown报告 |
| `metrics` | dict | 执行指标 |

### CSV输出格式

```csv
channel,peak_current_ka,steady_current_ka,dc_component_ka,time_constant_ms
#Gen38.IT:0,12.3456,8.9012,3.4444,45.23
#Gen39.IT:0,11.2345,8.1234,3.1111,42.15
```

## 设计原理

### 工作流程

```
1. 加载认证 → 设置CloudPSS Token
2. 获取模型 → 加载系统模型
3. 配置故障 → 设置故障类型、位置、时间
4. 运行EMT → 执行暂态仿真
5. 等待完成 → 监控任务状态
6. 分析结果 → 提取电流指标
7. 计算容量 → 计算短路容量
8. 导出结果 → JSON/CSV/报告
```

### 短路电流分析

**峰值电流**：故障期间电流的最大绝对值

```
I_peak = max(|i(t)|), t ∈ [fs, fe]
```

**稳态电流**：故障后电流的稳定值（取最后10个点的平均值）

```
I_steady = mean(i(t)), t ∈ [fe - Δt, fe]
```

**直流分量**：峰值与稳态峰值的差值

```
I_dc = I_peak - |I_steady|
```

**时间常数**：电流衰减到初始直流分量37%的时间

```
τ = t_decay - t_fault_start
```

**短路容量**：

```
S_sc = √3 × V_base × I_steady
```

## 与其他技能的关联

```
ieee3_prep
    ↓ (准备EMT模型)
short_circuit
    ↓ (短路电流结果)
n1_security / contingency_analysis
    ↓ (N-1分析)
protection_coordination
```

### 依赖关系

- **前置依赖**: `ieee3_prep`（准备EMT拓扑）
- **相关技能**:
  - `emt_simulation`: 基础EMT仿真
  - `emt_fault_study`: 故障研究分析
  - `n1_security`: N-1安全分析
  - `contingency_analysis`: 预想事故分析

## 性能特点

- **执行时间**: IEEE39系统约2-5分钟
- **精度**: 基于EMT仿真，精度高，可捕获暂态过程
- **适用范围**: 适用于各种规模的电力系统
- **计算复杂度**: O(n) 与监测通道数成正比
- **内存占用**: 与仿真时长和采样率相关

## 常见问题

### 问题1: EMT仿真失败

**原因**: 模型未配置EMT拓扑或故障元件

**解决**:
```bash
# 先准备模型
python -m cloudpss_skills run --config config/ieee3_prep.yaml
```

### 问题2: 电流通道无数据

**原因**: 通道名称错误或模型未配置该通道

**解决**: 检查模型中的量测通道名称，使用正确的trace名称格式，如`#ComponentName.SignalName:Index`

### 问题3: 短路电流异常小

**原因**: 故障电阻设置过大或故障时间不当

**解决**:
```yaml
fault:
  resistance: 0.0001    # 使用较小的故障电阻
  fs: 2.0               # 确保故障时间在仿真时间范围内
  fe: 2.1
```

### 问题4: 采样窗口无数据

**原因**: 采样时间窗口设置不当

**解决**: 调整`sample_window`使其在仿真时间范围内，并包含足够的故障数据：
```yaml
calculation:
  sample_window: [2.0, 2.05]  # 确保fs ≤ start < end ≤ simulation_duration
```

## 完整示例

### 场景描述

某电力公司需要对IEEE39系统进行短路电流计算，评估Bus7母线三相短路时的短路电流水平，为保护整定和设备选型提供依据。

### 配置文件

```yaml
skill: short_circuit
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

fault:
  location: Bus7
  type: three_phase
  resistance: 0.0001
  fs: 2.0
  fe: 2.1

monitoring:
  current_channels:
    - "#Gen38.IT:0"
    - "#Gen39.IT:0"
  voltage_channels:
    - "#Gen38.VT:0"
    - "#Gen39.VT:0"

calculation:
  base_voltage: 500
  base_capacity: 100
  sample_window: [2.0, 2.05]

output:
  format: json
  path: ./results/
  prefix: sc_ieee39_bus7
  generate_report: true
```

### 执行命令

```bash
python -m cloudpss_skills run --config short_circuit.yaml
```

### 预期输出

```
[INFO] 加载认证...
[INFO] 认证成功
[INFO] 模型: IEEE39
[INFO] 短路电流计算: Bus7
[INFO] 短路类型: three_phase
[INFO] 短路电阻: 0.0001 Ω
[INFO] 故障时间: 2.0s ~ 2.1s
[INFO] 运行EMT仿真...
[INFO] Job ID: job_xxx
[INFO] EMT仿真完成
[INFO] 分析短路电流...
[INFO]   #Gen38.IT:0: 峰值=12.3456kA, 稳态=8.9012kA
[INFO]   #Gen39.IT:0: 峰值=11.2345kA, 稳态=8.1234kA
[INFO] 结果已保存
```

### 结果文件

JSON结果：

```json
{
  "model": "IEEE39",
  "fault_location": "Bus7",
  "fault_type": "three_phase",
  "fault_resistance": 0.0001,
  "base_voltage": 500,
  "base_capacity": 100,
  "analysis": {
    "#Gen38.IT:0": {
      "peak_current": 12.3456,
      "steady_current": 8.9012,
      "dc_component": 3.4444,
      "time_constant": 45.23
    },
    "#Gen39.IT:0": {
      "peak_current": 11.2345,
      "steady_current": 8.1234,
      "dc_component": 3.1111,
      "time_constant": 42.15
    },
    "#Gen38.VT:0": {
      "min_voltage": 0.2345
    },
    "#Gen39.VT:0": {
      "min_voltage": 0.2567
    }
  },
  "short_circuit_mva": {
    "#Gen38.IT:0": {
      "steady_current_ka": 8.9012,
      "short_circuit_mva": 7712.34
    },
    "#Gen39.IT:0": {
      "steady_current_ka": 8.1234,
      "short_circuit_mva": 7037.89
    }
  }
}
```

Markdown报告示例：

```markdown
# 短路电流计算报告

**模型**: IEEE39
**短路位置**: Bus7
**短路类型**: three_phase
**短路电阻**: 0.0001 Ω

## 基准值

- 基准电压: 500 kV
- 基准容量: 100 MVA

## 短路电流分析

| 通道 | 峰值电流(kA) | 稳态电流(kA) | 直流分量(kA) | 时间常数(ms) |
|------|--------------|--------------|--------------|--------------|
| #Gen38.IT:0 | 12.3456 | 8.9012 | 3.4444 | 45.23 |
| #Gen39.IT:0 | 11.2345 | 8.1234 | 3.1111 | 42.15 |

## 短路容量

| 通道 | 稳态电流(kA) | 短路容量(MVA) |
|------|--------------|---------------|
| #Gen38.IT:0 | 8.9012 | 7712.34 |
| #Gen39.IT:0 | 8.1234 | 7037.89 |

## 结论

最大短路容量约为 **7712.34 MVA**
```

### 后续应用

1. **保护整定**: 根据峰值电流和稳态电流设置过电流保护动作值
2. **断路器选型**: 选择额定开断电流大于12.35kA的断路器
3. **设备校验**: 验证变压器、母线等设备的动热稳定性
4. **系统评估**: 评估系统短路容量是否超过设备额定值
5. **N-1分析**: 使用`n1_security`技能进行N-1安全分析

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
