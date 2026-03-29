# DUDV曲线可视化技能 (DUDV Curve Visualization)

## 设计背景

### 研究对象

DUDV（Voltage Deviation-Voltage）曲线是电压稳定性分析的重要工具，用于描述母线电压对无功注入的响应特性。曲线反映了不同电压水平下的电压偏差（ΔV），通过曲线的斜率和位置可以评估母线的电压稳定性、识别电压崩溃风险区域。DUDV曲线常用于无功补偿效果评估和电压稳定裕度分析。

### 实际需求

在电力系统规划和运行中，DUDV曲线分析用于：

1. **电压稳定性评估**: 通过曲线斜率判断母线电压稳定性
2. **无功补偿设计**: 评估无功补偿对电压特性的改善效果
3. **薄弱母线识别**: 识别对无功变化敏感的薄弱母线
4. **VSI结果验证**: 验证VSI弱母线分析的结果
5. **N-1故障后分析**: 评估故障后电压恢复特性

### 期望的输入和输出

**输入**:

- 电力系统模型（需配置EMT拓扑）
- 目标母线列表（需分析的母线）
- 电压扫描参数（电压范围、扫描点数）
- 无功注入参数（注入持续时间）
- 仿真参数（仿真时长、步长、故障设置）

**输出**:

- DUDV曲线数据（电压-偏差数据点）
- DUDV曲线图（PNG/PDF/SVG格式）
- 多母线对比图
- 电压稳定边界识别结果
- DUDV分析报告

### 计算结果的用途和价值

DUDV曲线结果可用于：

- **无功补偿规划**: 确定无功补偿设备的安装位置和容量
- **电压控制策略**: 指导AVR和SVC的设置
- **稳定性裕度评估**: 量化母线的电压稳定裕度
- **补偿效果对比**: 对比补偿前后的DUDV特性

## 功能特性

- **DUDV曲线生成**: 通过电压扫描生成电压-偏差关系曲线
- **多母线对比**: 支持多母线同时分析和对比显示
- **多格式输出**: 支持PNG、PDF、SVG等多种图像格式
- **自动布局**: 根据母线数量自动选择子图布局
- **参考线显示**: 自动添加V=1.0和DV=0参考线
- **从扰动结果加载**: 可直接从disturbance_severity结果生成曲线

## 快速开始

### 1. CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init dudv_curve --output dudv.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config dudv.yaml
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("dudv_curve")

# 配置
config = {
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "buses": ["Bus_16", "Bus_15", "Bus_26"],
    "simulation": {
        "end_time": 15.0,
        "step_time": 0.0001,
        "fault_bus": "Bus_16",
        "fault_type": "three_phase",
        "fault_time": 4.0,
        "fault_duration": 0.1
    },
    "dudv": {
        "voltage_range": [0.8, 1.2],
        "num_points": 20,
        "injection_duration": 2.0
    },
    "output": {
        "format": "png",
        "path": "./results/",
        "prefix": "dudv_curve",
        "show_grid": True,
        "show_legend": True
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

### 3. YAML配置示例

```yaml
skill: dudv_curve
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

buses: ["Bus_16", "Bus_15", "Bus_26"]  # 分析母线列表

simulation:
  end_time: 15.0                        # 仿真结束时间(s)
  step_time: 0.0001                     # 仿真步长(s)
  fault_bus: "Bus_16"                   # 故障母线
  fault_type: "three_phase"             # 故障类型
  fault_time: 4.0                       # 故障发生时间(s)
  fault_duration: 0.1                   # 故障持续时间(s)

dudv:
  voltage_range: [0.8, 1.2]             # 电压扫描范围(pu)
  num_points: 20                        # 扫描点数
  injection_duration: 2.0               # 无功注入持续时间(s)

output:
  format: "png"                         # 输出格式: png/pdf/svg
  path: ./results/
  prefix: dudv_curve
  show_grid: true                       # 显示网格
  show_legend: true                     # 显示图例
```

## 配置Schema

### 完整配置结构

```yaml
skill: dudv_curve                     # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token（不推荐）
  token_file: string                  # token文件路径（默认: .cloudpss_token）

model:                                # 模型配置（必需）
  rid: string                         # 模型RID或本地路径（必需）
  source: enum                        # cloud | local（默认: cloud）

buses: array                          # 分析母线列表（必需）

simulation:                           # 仿真配置
  end_time: number                    # 仿真结束时间(s)（默认: 15.0）
  step_time: number                   # 仿真步长(s)（默认: 0.0001）
  fault_bus: string                   # 故障母线
  fault_type: enum                    # three_phase | single_phase | line_ground
  fault_time: number                  # 故障发生时间(s)（默认: 4.0）
  fault_duration: number              # 故障持续时间(s)（默认: 0.1）

dudv:                                 # DUDV分析配置
  voltage_range: array                # 电压扫描范围[pu]（默认: [0.8, 1.2]）
  num_points: integer                 # 扫描点数（默认: 20）
  injection_bus: string               # 无功注入母线（可选，默认被分析母线）
  injection_duration: number          # 无功注入持续时间(s)（默认: 2.0）

output:                               # 输出配置
  format: enum                        # png | pdf | svg（默认: png）
  path: string                        # 输出目录（默认: ./results/）
  prefix: string                      # 文件名前缀（默认: dudv_curve）
  show_grid: boolean                  # 是否显示网格（默认: true）
  show_legend: boolean                # 是否显示图例（默认: true）
```

### 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"dudv_curve" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `buses` | array | 是 | - | 分析母线列表（如["Bus_16", "Bus_15"]） |
| `simulation.end_time` | number | 否 | 15.0 | 仿真结束时间(s) |
| `simulation.step_time` | number | 否 | 0.0001 | 仿真步长(s) |
| `simulation.fault_bus` | string | 否 | - | 故障母线label |
| `simulation.fault_type` | enum | 否 | three_phase | 故障类型 |
| `simulation.fault_time` | number | 否 | 4.0 | 故障发生时间(s) |
| `simulation.fault_duration` | number | 否 | 0.1 | 故障持续时间(s) |
| `dudv.voltage_range` | array | 否 | [0.8, 1.2] | 电压扫描范围[pu] |
| `dudv.num_points` | integer | 否 | 20 | 扫描点数 |
| `dudv.injection_bus` | string | 否 | - | 无功注入母线（可选） |
| `dudv.injection_duration` | number | 否 | 2.0 | 无功注入持续时间(s) |
| `output.format` | enum | 否 | png | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | dudv_curve | 文件名前缀 |
| `output.show_grid` | boolean | 否 | true | 是否显示网格 |
| `output.show_legend` | boolean | 否 | true | 是否显示图例 |

## Agent使用指南

### 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("dudv_curve")

# 最小化配置（使用默认值）
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "buses": ["Bus_16"]
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

### 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data

    # 获取DUDV数据
    dudv_data = data.get("dudv_data", {})
    for bus, values in dudv_data.items():
        voltage = values.get("voltage", [])
        dv = values.get("dv", [])
        print(f"母线 {bus}: {len(voltage)} 个数据点")

    # 访问输出文件
    for artifact in result.artifacts:
        print(f"输出文件: {artifact.path} ({artifact.type})")

# 查看日志
for log in result.logs:
    print(f"[{log.level}] {log.message}")
```

### 从扰动结果加载

```python
# 从disturbance_severity结果加载DUDV数据
dudv_data = skill.from_disturbance_severity_result(
    result_file="./results/disturbance_severity_result.json",
    bus_labels=["Bus_16", "Bus_15"]
)

for bus, data in dudv_data.items():
    print(f"母线 {bus}:")
    print(f"  电压: {data['voltage']}")
    print(f"  偏差: {data['dv']}")
```

### 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    error_msg = result.error

    # 常见错误处理
    if "Token文件不存在" in error_msg:
        print("错误: 请创建.cloudpss_token文件")
    elif "模型不存在" in error_msg:
        print("错误: 请检查模型RID是否正确")
    elif "未找到有效的母线" in error_msg:
        print("错误: 请检查母线label是否正确")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### JSON输出格式

```json
{
  "buses": ["Bus_16", "Bus_15", "Bus_26"],
  "dudv_data": {
    "Bus_16": {
      "voltage": [0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2],
      "dv": [-0.15, -0.12, -0.08, -0.04, 0.0, 0.03, 0.06, 0.08, 0.1]
    },
    "Bus_15": {
      "voltage": [0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2],
      "dv": [-0.12, -0.09, -0.06, -0.03, 0.0, 0.02, 0.05, 0.07, 0.09]
    }
  },
  "voltage_range": [0.8, 1.2],
  "num_points": 20
}
```

### SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "dudv_curve" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典（包含dudv_data、voltage_range、num_points） |
| `artifacts` | list | 输出文件列表（Artifact对象） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标 |

## 设计原理

### 工作流程

```
1. 配置加载
   └── 读取母线列表和扫描参数

2. 模型获取
   └── 从CloudPSS获取模型

3. 电压扫描
   └── 对每个目标母线
       └── 在不同无功注入水平下运行EMT
       └── 记录电压响应

4. DUDV数据计算
   └── 计算每个电压点的DV偏差
   └── 构建电压-偏差数据序列

5. 曲线绘制
   └── 生成DUDV曲线图
   └── 添加参考线（V=1.0, DV=0）

6. 结果输出
   └── 保存曲线图（PNG/PDF/SVG）
   └── 保存DUDV数据（JSON）
```

### DUDV曲线解读

**曲线含义**:

- **横轴**: 电压 (pu)，标幺值电压
- **纵轴**: 电压偏差 ΔV (pu)，相对于稳态电压的变化
- **曲线形状**: 反映母线电压对无功注入的敏感度

**稳定性判断**:

```
曲线斜率:
├── 平缓 (斜率小): 电压稳定性好
├── 陡峭 (斜率大): 电压稳定性差
└── 负斜率区域: 可能存在电压崩溃风险

曲线位置:
├── 整体偏左: 电压偏低，可能需要无功补偿
└── 整体偏右: 电压偏高，可能需要减少无功
```

### 扫描参数建议

| 系统类型 | 电压范围 | 扫描点数 | 说明 |
|----------|----------|----------|------|
| 正常系统 | [0.9, 1.1] | 15 | 较小范围，较快计算 |
| 电压薄弱系统 | [0.7, 1.3] | 30 | 较大范围，较高精度 |
| N-1故障后 | [0.6, 1.2] | 25 | 考虑故障后电压降低 |

## 与其他技能的关联

```
vsi_weak_bus
    ↓ (弱母线识别)
dudv_curve
    ↓ (DUDV验证)
reactive_compensation_design
    ↓ (补偿方案)
dudv_curve
    ↓ (补偿效果验证)
电压稳定性评估报告

disturbance_severity
    ↓ (DV数据)
dudv_curve
    ↓ (可视化)
扰动严重度分析
```

## 性能特点

- **仿真时间**: 每个数据点需要一次EMT仿真
- **总时间**: num_points × 单次仿真时间
- **内存占用**: 与系统规模和扫描点数成正比
- **适用规模**: 已测试至39节点系统
- **建议**: 先用较少点数测试，再根据需要增加精度

## 常见问题

### 问题1: 曲线数据点过少

**原因**: num_points设置过小

**解决**:

```yaml
dudv:
  num_points: 30  # 增加扫描点数到20-50
```

### 问题2: 电压范围不合适

**原因**: voltage_range与实际电压范围不匹配

**解决**:

```yaml
dudv:
  voltage_range: [0.7, 1.3]  # 根据系统标称电压调整
```

### 问题3: 仿真不收敛

**原因**: 极端电压条件下的仿真发散

**解决**:

```yaml
dudv:
  voltage_range: [0.85, 1.15]  # 缩小电压扫描范围
```

### 问题4: 图表显示不全

**原因**: 母线数量过多

**解决**:

```yaml
buses: ["Bus_16"]  # 减少单次分析的母线数量
# 或使用较小的图片尺寸
output:
  format: "pdf"  # PDF格式支持多页
```

## 完整示例

### 场景描述

某电力公司已经通过VSI弱母线分析识别出IEEE39系统的薄弱母线（Bus_16、Bus_15、Bus_26），现在需要生成这些母线的DUDV曲线，进一步验证其电压稳定性并评估无功补偿效果。

### 配置文件

创建文件 `dudv_ieee39.yaml`:

```yaml
skill: dudv_curve
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

buses: ["Bus_16", "Bus_15", "Bus_26"]

simulation:
  end_time: 15.0
  step_time: 0.0001
  fault_bus: "Bus_16"
  fault_type: "three_phase"
  fault_time: 4.0
  fault_duration: 0.1

dudv:
  voltage_range: [0.8, 1.2]
  num_points: 20
  injection_duration: 2.0

output:
  format: "png"
  path: ./results/
  prefix: dudv_ieee39
  show_grid: true
  show_legend: true
```

### 执行命令

```bash
python -m cloudpss_skills run --config dudv_ieee39.yaml
```

### 预期输出

```
[14:32:01] [INFO] DUDV曲线分析开始 - 模型: model/holdme/IEEE39, 母线数: 3
[14:32:01] [INFO] DUDV分析开始，母线: ['Bus_16', 'Bus_15', 'Bus_26']
[14:32:02] [INFO] 计算母线 Bus_16 的DUDV数据...
[14:32:03] [INFO] 计算母线 Bus_15 的DUDV数据...
[14:32:04] [INFO] 计算母线 Bus_26 的DUDV数据...
[14:32:05] [INFO] DUDV分析完成，耗时: 4.23s
[14:32:05] [INFO] 结果已保存: ./results/dudv_ieee39.png
[14:32:05] [INFO] 数据已保存: ./results/dudv_ieee39_data.json

[OK] 技能执行成功: dudv_curve
耗时: 4.5s
```

### 结果文件

**曲线图** (`dudv_ieee39.png`):

- 3个子图（2×2布局）
- 每个母线一个DUDV曲线
- 包含参考线（V=1.0, DV=0）
- 显示网格和图例

**DUDV数据** (`dudv_ieee39_data.json`):

```json
{
  "Bus_16": {
    "voltage": [0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2],
    "dv": [-0.15, -0.12, -0.08, -0.04, 0.0, 0.03, 0.06, 0.08, 0.1]
  },
  "Bus_15": {
    "voltage": [0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2],
    "dv": [-0.12, -0.09, -0.06, -0.03, 0.0, 0.02, 0.05, 0.07, 0.09]
  },
  "Bus_26": {
    "voltage": [0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2],
    "dv": [-0.13, -0.1, -0.07, -0.03, 0.0, 0.025, 0.055, 0.075, 0.095]
  }
}
```

### 后续应用

基于DUDV曲线结果，可以：

1. **设计无功补偿**: 使用`reactive_compensation_design`技能设计补偿方案
2. **补偿效果对比**: 对比补偿前后的DUDV曲线
3. **电压稳定评估**: 结合VSI结果综合评估电压稳定性
4. **生成报告**: 使用`visualize`技能生成综合分析报告

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
