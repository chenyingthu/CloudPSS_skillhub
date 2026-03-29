# 谐波分析技能 (Harmonic Analysis)

## 设计背景

### 研究对象

谐波是电力系统中频率为基波频率整数倍的电压或电流分量。现代电力系统中，非线性负荷（如变频器、整流器、电弧炉等）和新能源设备的大量应用导致谐波污染日益严重。谐波分析技能用于评估电力系统的谐波分布特性，识别谐波源位置和谐波放大问题，为谐波治理提供数据支持。

### 实际需求

在电力系统规划、设计和运行中，谐波分析具有以下重要作用：

1. **谐波源识别**: 定位系统中主要的谐波注入点
2. **谐波潮流计算**: 评估各次谐波在系统中的分布和传播
3. **谐波放大分析**: 识别可能发生谐波谐振的频率点
4. **谐波限值校核**: 验证各节点谐波电压和电流是否满足国标要求
5. **滤波器设计**: 为无源或有源滤波器设计提供基础数据

### 期望的输入和输出

**输入**:
- 电力系统模型（IEEE标准系统或实际系统）
- 谐波源配置（位置、次数、幅值、相角）
- 分析谐波次数列表（3、5、7、11、13等典型次数）
- 基波频率（50Hz或60Hz）

**输出**:
- 各次谐波电压幅值和相角分布
- 各次谐波电流幅值和相角分布
- 各节点总谐波畸变率（THD）
- 谐波阻抗频率特性曲线
- 谐波功率流向分析

### 计算结果的用途和价值

谐波分析结果可直接用于：
- 评估系统谐波污染程度是否满足GB/T 14549标准要求
- 识别谐波电压/电流超标节点，确定治理优先级
- 分析谐波谐振风险，指导系统规划和运行方式调整
- 为无源滤波器（LC谐振型）的参数设计提供依据
- 评估新能源并网对系统谐波特性的影响

## 功能特性

- **多谐波次数分析**: 支持3、5、7、11、13等典型谐波次数的批量计算
- **谐波潮流计算**: 基于谐波网络模型计算各次谐波的电压电流分布
- **谐波阻抗扫描**: 分析系统谐波阻抗的频率特性，识别谐振点
- **THD自动计算**: 自动计算电压和电流的总谐波畸变率
- **谐波源建模**: 支持多种谐波源模型（电压源型、电流源型）
- **谐波功率分析**: 分析谐波功率流向，定位谐波源和吸收点
- **结果可视化**: 输出谐波频谱图、THD分布图等可视化结果

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init harmonic_analysis --output ha.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config ha.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("harmonic_analysis")

# 配置
config = {
    "skill": "harmonic_analysis",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "analysis": {
        "harmonics": [3, 5, 7, 11, 13],
        "base_frequency": 50,
        "harmonic_sources": [
            {
                "bus": "Bus_16",
                "harmonics": {"3": 0.1, "5": 0.05}
            }
        ]
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "harmonic",
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

```yaml
skill: harmonic_analysis
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  harmonics: [3, 5, 7, 11, 13]  # 分析谐波次数
  base_frequency: 50            # 基波频率(Hz)
  harmonic_sources:             # 谐波源配置
    - bus: Bus_16
      harmonics:
        "3": 0.1    # 3次谐波幅值(pu)
        "5": 0.05   # 5次谐波幅值(pu)
      phase:
        "3": 30     # 3次谐波相角(度)
        "5": -45    # 5次谐波相角(度)
    - bus: Bus_15
      harmonics:
        "3": 0.08
        "5": 0.04

output:
  format: json
  path: ./results/
  prefix: harmonic
  timestamp: true
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: harmonic_analysis              # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token（不推荐）
  token_file: string                  # token文件路径（默认: .cloudpss_token）

model:                                # 模型配置（必需）
  rid: string                         # 模型RID或本地路径（必需）
  source: enum                        # cloud | local（默认: cloud）

analysis:                             # 分析配置（必需）
  harmonics: array                    # 谐波次数列表（必需）
  base_frequency: number              # 基波频率（默认: 50）
  harmonic_sources: array             # 谐波源配置
    - bus: string                     # 谐波源所在母线
      harmonics: object               # 各次谐波幅值
        "h": number                  # h次谐波幅值(pu)
      phase: object                   # 各次谐波相角
        "h": number                  # h次谐波相角(度)
  impedance_scan:                     # 阻抗扫描配置
    enabled: boolean                  # 是否启用扫描（默认: true）
    frequency_range: array            # 频率范围[min, max]
    steps: integer                    # 扫描步数（默认: 100）

output:                               # 输出配置
  format: enum                        # json | csv（默认: json）
  path: string                        # 输出目录（默认: ./results/）
  prefix: string                      # 文件名前缀（默认: harmonic）
  timestamp: boolean                  # 是否添加时间戳（默认: true）
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"harmonic_analysis" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `analysis.harmonics` | array | 是 | - | 需要分析的谐波次数列表，如[3,5,7,11,13] |
| `analysis.base_frequency` | number | 否 | 50 | 基波频率(Hz)，50或60 |
| `analysis.harmonic_sources` | array | 否 | [] | 谐波源配置列表 |
| `analysis.harmonic_sources[].bus` | string | 是 | - | 谐波源所在母线标签 |
| `analysis.harmonic_sources[].harmonics` | object | 是 | - | 各次谐波幅值，键为次数，值为pu |
| `analysis.harmonic_sources[].phase` | object | 否 | - | 各次谐波相角，键为次数，值为角度 |
| `analysis.impedance_scan.enabled` | boolean | 否 | true | 是否执行谐波阻抗扫描 |
| `analysis.impedance_scan.frequency_range` | array | 否 | [50, 650] | 扫描频率范围(Hz) |
| `analysis.impedance_scan.steps` | integer | 否 | 100 | 扫描步数 |
| `output.format` | enum | 否 | json | 输出格式：json / csv |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | harmonic | 文件名前缀 |
| `output.timestamp` | boolean | 否 | true | 文件名是否包含时间戳 |

## Agent使用指南

### 5.1 基本调用模式

```python
# 获取技能实例
skill = get_skill("harmonic_analysis")

# 最小化配置（使用默认值）
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "harmonics": [3, 5, 7],
        "harmonic_sources": [
            {"bus": "Bus_16", "harmonics": {"3": 0.1, "5": 0.05}}
        ]
    }
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status == "SUCCESS":
        print(f"分析完成: {result.data}")
    else:
        print(f"分析失败: {result.error}")
```

### 5.2 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data

    # 访问各次谐波结果
    for h in [3, 5, 7, 11, 13]:
        harmonic_data = data.get(f"harmonic_{h}", {})
        bus_voltages = harmonic_data.get("bus_voltages", {})
        print(f"{h}次谐波电压分布: {bus_voltages}")

    # 访问THD结果
    thd_data = data.get("thd", {})
    voltage_thd = thd_data.get("voltage", {})
    print(f"电压THD: {voltage_thd}")

    # 访问输出文件
    for artifact in result.artifacts:
        print(f"输出文件: {artifact.path} ({artifact.type})")
        if artifact.type == "csv":
            print(f"  CSV文件包含谐波分布数据")

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
    if "Token文件不存在" in error_msg:
        print("错误: 请创建.cloudpss_token文件")
    elif "模型不存在" in error_msg:
        print("错误: 请检查模型RID是否正确")
    elif "谐波源母线不存在" in error_msg:
        print("错误: 请检查harmonic_sources中配置的母线标签")
    elif "谐波次数无效" in error_msg:
        print("错误: 谐波次数必须是正整数，且不超过系统支持的次数")
    elif "谐波源幅值过大" in error_msg:
        print("错误: 谐波源幅值应小于1.0 pu")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "model": "IEEE39",
  "model_rid": "model/holdme/IEEE39",
  "job_id": "job_xxx",
  "timestamp": "2024-03-24T14:32:01",
  "harmonics_analyzed": [3, 5, 7, 11, 13],
  "base_frequency": 50,
  "harmonic_3": {
    "bus_voltages": {
      "Bus_1": {"magnitude": 0.0152, "angle": 45.2},
      "Bus_16": {"magnitude": 0.0321, "angle": -12.5}
    },
    "branch_currents": {
      "Line_1": {"magnitude": 0.0085, "angle": 78.3}
    }
  },
  "harmonic_5": {
    "bus_voltages": {
      "Bus_1": {"magnitude": 0.0087, "angle": 32.1},
      "Bus_16": {"magnitude": 0.0213, "angle": -45.8}
    }
  },
  "thd": {
    "voltage": {
      "Bus_1": 0.0175,
      "Bus_16": 0.0389
    },
    "current": {
      "Line_1": 0.0085
    }
  },
  "impedance_scan": {
    "frequencies": [50, 56, 62, ...],
    "impedance_magnitude": [1.0, 1.2, 1.8, ...],
    "resonance_points": [
      {"frequency": 350, "impedance": 15.2}
    ]
  }
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "harmonic_analysis" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典，包含各次谐波结果、THD、阻抗扫描数据 |
| `artifacts` | list | 输出文件列表（Artifact对象），包含JSON和CSV结果文件 |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标，包括各次谐波计算耗时 |

## 设计原理

### 工作流程

```
1. 模型加载与初始化
   ├── 加载系统模型
   ├── 构建基波潮流计算结果
   └── 提取系统拓扑和参数

2. 谐波网络构建
   ├── 根据各次谐波频率计算元件谐波阻抗
   │   ├── 线路: Z_h = R + j*h*X (h为谐波次数)
   │   ├── 变压器: Z_h = R + j*h*X
   │   ├── 负荷: 根据负荷类型采用不同模型
   │   └── 电容器: X_c/h (容抗随频率降低)
   └── 构建各次谐波的节点导纳矩阵

3. 谐波源注入
   ├── 解析配置的谐波源参数
   ├── 在谐波网络中注入谐波电流源
   └── 支持多谐波源同时注入

4. 谐波潮流求解
   ├── 对每个谐波次数求解线性方程组
   ├── 计算各节点谐波电压
   └── 计算各支路谐波电流

5. THD计算
   ├── 收集各次谐波电压/电流结果
   ├── 计算电压THD: THD_v = sqrt(sum(V_h^2)) / V_1
   └── 计算电流THD: THD_i = sqrt(sum(I_h^2)) / I_1

6. 谐波阻抗扫描（可选）
   ├── 在指定频率范围内扫描
   ├── 计算各频率点的系统谐波阻抗
   ├── 识别阻抗极大值点（谐振点）
   └── 输出阻抗频率特性曲线

7. 结果输出
   ├── 生成JSON结果文件
   ├── 生成CSV数据文件
   └── 输出谐波分布可视化图表
```

### 数学基础

谐波网络采用线性频域分析方法，对于h次谐波：

```
I_h = Y_h × V_h
```

其中：
- `I_h`: h次谐波节点注入电流向量
- `Y_h`: h次谐波节点导纳矩阵
- `V_h`: h次谐波节点电压向量

各元件谐波阻抗：
- **线路**: Z_line,h = R + j*h*X
- **变压器**: Z_trans,h = R + j*h*X
- **电容器**: X_c,h = X_c,1 / h

THD计算：
```
THD_v = sqrt(sum_{h=2}^{H}(V_h^2)) / V_1 × 100%
THD_i = sqrt(sum_{h=2}^{H}(I_h^2)) / I_1 × 100%
```

## 与其他技能的关联

```
power_flow
    ↓ (潮流结果)
harmonic_analysis
    ↓ (谐波分析结果)
filter_design
    ↓ (滤波器参数)
emt_simulation
    ↓ (时域验证)
结果对比
```

### 依赖关系

- **必需依赖**: CloudPSS SDK (`cloudpss`)
- **输入依赖**:
  - `power_flow`: 提供基波潮流结果作为谐波分析基础
- **输出被依赖**:
  - `filter_design`: 根据谐波分析结果设计滤波器
  - `power_quality_analysis`: 综合电能质量评估

## 性能特点

- **执行时间**: IEEE39系统5次谐波分析约10-20秒
- **内存占用**: 与系统规模和谐波次数成正比
- **计算精度**: 基于线性频域分析，结果稳定可靠
- **适用规模**: 已测试至500节点系统
- **谐波次数**: 支持2-25次谐波分析

## 常见问题

### 问题1: THD计算结果异常偏高

**原因**:
- 谐波源幅值设置过大
- 系统存在谐波谐振点
- 电容器组与系统阻抗形成谐振

**解决**:
```yaml
analysis:
  harmonic_sources:
    - bus: Bus_16
      harmonics:
        "3": 0.05    # 降低谐波源幅值
        "5": 0.03
  impedance_scan:
    enabled: true    # 启用阻抗扫描识别谐振点
    frequency_range: [150, 350]  # 重点扫描3-7次谐波范围
```

### 问题2: 某些母线谐波电压不收敛

**原因**:
- 系统在该谐波频率下阻抗过大
- 谐波源配置错误导致数值问题
- 系统存在谐波孤岛

**解决**:
- 检查谐波源相角配置是否合理
- 减少同时分析的谐波次数，分批次计算
- 检查系统拓扑完整性

### 问题3: 谐波阻抗扫描结果不平滑

**原因**:
- 扫描步数过少
- 系统参数不连续
- 数值计算精度问题

**解决**:
```yaml
analysis:
  impedance_scan:
    steps: 200      # 增加扫描步数
    frequency_range: [50, 1000]  # 调整频率范围
```

### 问题4: 结果文件过大

**原因**:
- 系统规模过大
- 分析的谐波次数过多
- 同时输出了大量母线和支路数据

**解决**:
- 仅分析关键谐波次数（3、5、7、11、13）
- 关注特定母线和支路的结果
- 使用CSV格式代替JSON（通常更小）

## 完整示例

### 场景描述

某工业配电系统（IEEE39标准系统）中，Bus_16母线连接有变频器负荷，产生3次和5次谐波电流。需要评估谐波在系统中的分布情况，识别THD超标的母线，并分析是否存在谐波谐振风险。

### 配置文件

```yaml
skill: harmonic_analysis
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  harmonics: [3, 5, 7, 11, 13]
  base_frequency: 50
  harmonic_sources:
    - bus: Bus_16
      harmonics:
        "3": 0.1    # 3次谐波电流10%
        "5": 0.05   # 5次谐波电流5%
        "7": 0.03   # 7次谐波电流3%
      phase:
        "3": 0      # 相角0度
        "5": -30    # 相角-30度
        "7": -60    # 相角-60度
  impedance_scan:
    enabled: true
    frequency_range: [50, 650]
    steps: 100

output:
  format: json
  path: ./results/
  prefix: harmonic_ieee39
  timestamp: true
```

### 执行命令

```bash
python -m cloudpss_skills run --config harmonic_analysis.yaml
```

### 预期输出

```
[INFO] 加载认证信息...
[INFO] 认证成功
[INFO] 获取模型: IEEE39
[INFO] 基波潮流计算完成
[INFO] 开始谐波分析...
[INFO] 分析谐波次数: [3, 5, 7, 11, 13]
[INFO] [3次谐波] 计算中...
[INFO] [5次谐波] 计算中...
[INFO] [7次谐波] 计算中...
[INFO] [11次谐波] 计算中...
[INFO] [13次谐波] 计算中...
[INFO] THD计算完成
[INFO] 谐波阻抗扫描中...
[INFO] 发现1个谐振点: 350Hz
[INFO] 结果已保存: ./results/harmonic_ieee39_20240324_143245_result.json
[INFO] CSV数据已保存: ./results/harmonic_ieee39_20240324_143245_data.csv
```

### 结果文件

**JSON结果文件** (`harmonic_ieee39_20240324_143245_result.json`):

```json
{
  "model": "IEEE39",
  "model_rid": "model/holdme/IEEE39",
  "job_id": "job_ha_xxx",
  "timestamp": "2024-03-24T14:32:45",
  "harmonics_analyzed": [3, 5, 7, 11, 13],
  "base_frequency": 50,
  "harmonic_3": {
    "bus_voltages": {
      "Bus_16": {"magnitude": 0.0321, "angle": -12.5},
      "Bus_15": {"magnitude": 0.0289, "angle": -15.2},
      "Bus_1": {"magnitude": 0.0152, "angle": 45.2}
    }
  },
  "harmonic_5": {
    "bus_voltages": {
      "Bus_16": {"magnitude": 0.0213, "angle": -45.8},
      "Bus_15": {"magnitude": 0.0187, "angle": -52.1}
    }
  },
  "thd": {
    "voltage": {
      "Bus_16": 0.0389,
      "Bus_15": 0.0345,
      "Bus_1": 0.0152
    }
  },
  "impedance_scan": {
    "resonance_points": [
      {"frequency": 350, "impedance": 15.2, "order": 7}
    ]
  }
}
```

**CSV数据文件** (`harmonic_ieee39_20240324_143245_data.csv`):

```csv
Bus,THD_Voltage,H3_Mag,H3_Angle,H5_Mag,H5_Angle,H7_Mag,H7_Angle
Bus_16,3.89%,0.0321,-12.5,0.0213,-45.8,0.0156,-78.2
Bus_15,3.45%,0.0289,-15.2,0.0187,-52.1,0.0132,-85.3
Bus_1,1.52%,0.0152,45.2,0.0087,32.1,0.0054,18.7
...
```

### 后续应用

基于谐波分析结果，可以进行以下后续分析：

1. **滤波器设计**: 使用`filter_design`技能根据谐波分布设计无源滤波器
2. **电能质量综合评估**: 使用`power_quality_analysis`技能进行全面的电能质量分析
3. **谐波治理效果验证**: 在添加滤波器后重新运行谐波分析，对比THD改善效果
4. **谐振风险分析**: 根据阻抗扫描结果，评估系统在不同运行方式下的谐振风险

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
