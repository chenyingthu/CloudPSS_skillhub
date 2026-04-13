# 频率响应分析技能 (Frequency Response Analysis)

## 设计背景

### 研究对象

频率响应分析用于评估电力系统在功率不平衡情况下的频率动态特性。当系统发生大功率缺失（如发电机跳闸）或负荷突增时，系统频率会经历一个动态变化过程。频率响应分析通过时域仿真，提取频率最低点（频率跌落）、变化率（RoCoF）、稳定时间等关键指标，评估系统的频率稳定性和控制性能。

### 实际需求

在电力系统规划和运行中，频率响应分析用于：

1. **频率稳定评估**: 评估系统在功率扰动下的频率稳定性
2. **惯量评估**: 评估系统的等效惯量水平
3. **一次调频验证**: 验证一次调频响应性能
4. **低频减载整定**: 为低频减载保护提供整定依据
5. **新能源接入评估**: 评估高比例新能源接入对频率响应的影响

### 期望的输入和输出

**输入**:

- 电力系统模型（需配置EMT拓扑）
- 扰动设置（类型、幅值、发生时间）
- 监测信号通道（频率/转速、功率等）
- 分析参数（基准频率、分析窗口、稳定阈值等）
- 仿真时长

**输出**:

- 频率响应曲线数据
- 频率最低点（频率跌落深度）
- 最大频率变化率（RoCoF）
- 稳态频率和频率偏差
- 稳定时间
- 等效惯量估计
- 频率响应分析报告

### 计算结果的用途和价值

频率响应分析结果可用于：

- **保护整定**: 确定低频减载的启动频率和延时
- **惯量规划**: 评估系统需要的最低惯量水平
- **调频控制**: 优化一次调频和二次调频参数
- **运行限值**: 确定最大可承受功率缺额

## 功能特性

- **多种扰动类型**: 支持阶跃负荷变化、发电机跳闸、负荷切除等
- **多通道监测**: 可同时监测多个频率/转速信号通道
- **自动指标提取**: 自动提取频率最低点、RoCoF、稳定时间等指标
- **等效惯量估计**: 基于频率响应估计系统等效惯量
- **完整报告输出**: 生成JSON/CSV/Markdown多格式报告

## 快速开始

### 1. CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init frequency_response --output fr.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config fr.yaml
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("frequency_response")

# 配置
config = {
    "skill": "frequency_response",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "disturbance": {
        "type": "step_load_change",
        "time": 2.0,
        "load_change_percent": 10.0
    },
    "monitoring": {
        "frequency_channels": ["#Gen38.wr:0"],
        "power_channels": ["#Gen38.IT:0"]
    },
    "analysis": {
        "base_frequency": 60.0,
        "analysis_window": [2.0, 10.0],
        "frequency_deadband": 0.05,
        "settling_threshold": 0.1
    },
    "emt": {
        "duration": 10.0
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "frequency_response",
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
print(f"数据: {result.data}")
```

### 3. YAML配置示例

```yaml
skill: frequency_response
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

disturbance:
  type: "step_load_change"            # 扰动类型
  time: 2.0                           # 扰动发生时间(s)
  load_change_percent: 10.0           # 负荷变化百分比(%)
  # generator_target: "Gen38"         # 发电机跳闸目标（如type=generator_trip）

monitoring:
  frequency_channels: ["#Gen38.wr:0"] # 频率/转速信号通道
  power_channels: ["#Gen38.IT:0"]     # 功率信号通道

analysis:
  base_frequency: 60.0                # 基准频率(Hz)
  analysis_window: [2.0, 10.0]        # 分析时间窗口[s]
  frequency_deadband: 0.05            # 频率死区(Hz)
  settling_threshold: 0.1             # 稳定阈值(Hz)

emt:
  duration: 10.0                      # 仿真时长(s)

output:
  format: json
  path: ./results/
  prefix: frequency_response
  generate_report: true
```

## 配置Schema

### 完整配置结构

```yaml
skill: frequency_response             # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token（不推荐）
  token_file: string                  # token文件路径（默认: .cloudpss_token）

model:                                # 模型配置（必需）
  rid: string                         # 模型RID或本地路径（必需）
  source: enum                        # cloud | local（默认: cloud）

disturbance:                          # 扰动配置（必需）
  type: enum                          # step_load_change | generator_trip | load_shedding
  time: number                        # 扰动发生时间(s)（默认: 2.0）
  load_change_percent: number         # 负荷变化百分比(%)
  generator_target: string            # 发电机跳闸目标
  shed_load_target: string            # 切除负荷目标
  shed_percent: number                # 切除百分比(%)

monitoring:                           # 监测配置
  frequency_channels: array           # 频率/转速信号通道
  power_channels: array               # 功率信号通道

analysis:                             # 分析配置
  base_frequency: number              # 基准频率(Hz)（默认: 60.0）
  analysis_window: array              # 分析时间窗口[s]（默认: [2.0, 10.0]）
  frequency_deadband: number          # 频率死区(Hz)（默认: 0.05）
  settling_threshold: number          # 稳定阈值(Hz)（默认: 0.1）

emt:                                  # EMT仿真配置
  duration: number                    # 仿真时长(s)（默认: 10.0）

output:                               # 输出配置
  format: enum                        # json | csv（默认: json）
  path: string                        # 输出目录（默认: ./results/）
  prefix: string                      # 文件名前缀（默认: frequency_response）
  generate_report: boolean            # 是否生成报告（默认: true）
```

### 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"frequency_response" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `disturbance.type` | enum | 是 | - | 扰动类型：step_load_change/generator_trip/load_shedding |
| `disturbance.time` | number | 否 | 2.0 | 扰动发生时间(s) |
| `disturbance.load_change_percent` | number | 否 | - | 负荷变化百分比(%) |
| `disturbance.generator_target` | string | 否 | - | 发电机跳闸目标 |
| `disturbance.shed_load_target` | string | 否 | - | 切除负荷目标 |
| `disturbance.shed_percent` | number | 否 | - | 切除百分比(%) |
| `monitoring.frequency_channels` | array | 否 | [] | 频率/转速信号通道列表 |
| `monitoring.power_channels` | array | 否 | [] | 功率信号通道列表 |
| `analysis.base_frequency` | number | 否 | 60.0 | 基准频率(Hz) |
| `analysis.analysis_window` | array | 否 | [2.0, 10.0] | 分析时间窗口[s] |
| `analysis.frequency_deadband` | number | 否 | 0.05 | 频率死区(Hz) |
| `analysis.settling_threshold` | number | 否 | 0.1 | 稳定阈值(Hz) |
| `emt.duration` | number | 否 | 10.0 | 仿真时长(s) |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | frequency_response | 文件名前缀 |
| `output.generate_report` | boolean | 否 | true | 是否生成Markdown报告 |

## Agent使用指南

### 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("frequency_response")

# 最小化配置（使用默认值）
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "disturbance": {
        "type": "step_load_change",
        "load_change_percent": 10.0
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

### 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data

    # 获取频率响应指标
    freq_metrics = data.get("frequency_metrics", {})
    for ch, metrics in freq_metrics.items():
        print(f"通道 {ch}:")
        print(f"  最低点: {metrics['nadir_frequency']:.4f} Hz")
        print(f"  最大RoCoF: {metrics['max_rocof']:.2f} Hz/s")
        print(f"  稳态频率: {metrics['steady_frequency']:.4f} Hz")
        print(f"  稳定时间: {metrics['settling_time']:.2f} s")

    # 访问输出文件
    for artifact in result.artifacts:
        print(f"输出文件: {artifact.path} ({artifact.type})")

# 查看日志
for log in result.logs:
    print(f"[{log.level}] {log.message}")
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
    elif "EMT仿真失败" in error_msg:
        print("错误: 模型未配置EMT参数，请确保模型包含EMT拓扑和故障元件")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### JSON输出格式

```json
{
  "model": "IEEE39",
  "disturbance_type": "step_load_change",
  "disturbance_time": 2.0,
  "base_frequency": 60.0,
  "frequency_metrics": {
    "#Gen38.wr:0": {
      "base_frequency": 60.0,
      "nadir_frequency": 59.6234,
      "nadir_time": 2.45,
      "max_rocof": -1.52,
      "steady_frequency": 59.85,
      "settling_time": 8.2,
      "frequency_deviation": -0.15
    }
  }
}
```

### SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "frequency_response" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典（包含frequency_metrics等） |
| `artifacts` | list | 输出文件列表（Artifact对象） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标 |

## 设计原理

### 工作流程

```
1. 模型准备
   └── 获取基础模型

2. 扰动配置
   └── 根据扰动类型配置模型
       └── 阶跃负荷变化/发电机跳闸/负荷切除

3. EMT仿真
   └── 运行指定时长的EMT仿真
       └── 等待仿真完成

4. 频率响应分析
   └── 提取频率/转速信号
       └── 计算频率响应指标
           └── 频率最低点
           └── 最大变化率(RoCoF)
           └── 稳态频率
           └── 稳定时间
           └── 频率偏差

5. 结果输出
   └── 保存JSON/CSV结果和Markdown报告
```

### 关键指标计算

**频率最低点（Frequency Nadir）**:

```
f_nadir = min(f(t)) for t in [t_disturbance, t_end]
```

**最大频率变化率（RoCoF）**:

```
RoCoF_max = max(|df/dt|)
```

**稳态频率**:

```
f_steady = mean(f(t)) for t in [t_end - 1s, t_end]
```

**稳定时间**:

```
t_settling = min(t) where |f(t) - f_steady| < threshold for 5 consecutive points
```

**等效惯量估计**:

```
H_eq = (ΔP * f_base) / (2 * RoCoF_max * S_base)
```

其中：
- ΔP: 功率缺额
- f_base: 基准频率
- S_base: 基准容量

### 频率响应评价标准

| 指标 | 良好 | 一般 | 较差 |
|------|------|------|------|
| 频率跌落 | < 0.5 Hz | 0.5-1.0 Hz | > 1.0 Hz |
| RoCoF | < 1 Hz/s | 1-2 Hz/s | > 2 Hz/s |
| 稳定时间 | < 10 s | 10-20 s | > 20 s |

## 与其他技能的关联

```
power_flow
    ↓ (基础潮流)
emt_simulation (配置fault参数)
    ↓ (EMT仿真)
frequency_response
    ↓ (频率响应分析)
transient_stability
    ↓ (综合稳定性评估)
控制策略设计
```

## 性能特点

- **仿真时间**: 约10-30秒（取决于仿真时长）
- **内存占用**: 中等，与系统规模成正比
- **适用规模**: 已测试至39节点系统
- **精度**: 取决于EMT仿真精度和采样率
- **建议**: 使用较小的仿真步长（0.0001s）以获得精确的RoCoF

## 常见问题

### 问题1: 频率信号提取失败

**原因**: 信号通道名称不匹配

**解决**:

```yaml
monitoring:
  frequency_channels: ["#Gen38.wr:0"]  # 使用实际存在的通道名
```

### 问题2: RoCoF计算不准确

**原因**: 仿真步长过大或信号噪声

**解决**:

```yaml
emt:
  duration: 10.0
# 在模型中设置较小的仿真步长（如0.0001s）
```

### 问题3: 稳态频率估计偏差

**原因**: 分析窗口内频率未完全稳定

**解决**:

```yaml
emt:
  duration: 15.0  # 延长仿真时间
analysis:
  analysis_window: [2.0, 15.0]  # 扩大分析窗口
```

### 问题4: 扰动未正确设置

**原因**: 扰动目标组件不存在

**解决**:

```yaml
disturbance:
  type: "step_load_change"
  load_change_percent: 10.0
  # 不指定load_target则作用于所有负荷
```

## 完整示例

### 场景描述

某电力公司需要评估IEEE39系统在10%负荷突增情况下的频率响应特性，确定频率跌落深度和RoCoF，为低频减载整定提供依据。

### 配置文件

创建文件 `fr_ieee39.yaml`:

```yaml
skill: frequency_response
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

disturbance:
  type: "step_load_change"
  time: 2.0
  load_change_percent: 10.0

monitoring:
  frequency_channels: ["#Gen38.wr:0"]
  power_channels: ["#Gen38.IT:0"]

analysis:
  base_frequency: 60.0
  analysis_window: [2.0, 10.0]
  frequency_deadband: 0.05
  settling_threshold: 0.1

emt:
  duration: 10.0

output:
  format: json
  path: ./results/
  prefix: fr_ieee39
  generate_report: true
```

### 执行命令

```bash
python -m cloudpss_skills run --config fr_ieee39.yaml
```

### 预期输出

```
[14:32:01] [INFO] 加载认证...
[14:32:02] [INFO] 认证成功
[14:32:02] [INFO] 模型: IEEE39
[14:32:03] [INFO] 频率响应分析: IEEE39
[14:32:03] [INFO] 扰动类型: step_load_change, 时间: 2.0s
[14:32:04] [INFO] 负荷阶跃: Load_16, 150MW -> 165MW @ 2.0s
[14:32:05] [INFO] 运行EMT仿真 (时长: 10.0s)...
[14:32:05] [INFO] Job ID: job_xxx
[14:32:25] [INFO] EMT仿真完成
[14:32:25] [INFO] 分析频率响应...
[14:32:26] [INFO]   #Gen38.wr:0:
[14:32:26] [INFO]     基准频率: 60.0000 Hz
[14:32:26] [INFO]     最低点: 59.6234 Hz @ 2.450s
[14:32:26] [INFO]     最大变化率: 1.52 Hz/s
[14:32:26] [INFO]     稳态频率: 59.8500 Hz
[14:32:26] [INFO]     稳定时间: 8.200s
[14:32:27] [INFO] 结果已保存: ./results/fr_ieee39_20240324_143227.json
[14:32:27] [INFO] 报告已保存: ./results/fr_ieee39_20240324_143227_report.md

[OK] 技能执行成功: frequency_response
耗时: 26.5s
```

### 结果文件

**JSON结果** (`fr_ieee39_20240324_143227.json`):

```json
{
  "model": "IEEE39",
  "disturbance_type": "step_load_change",
  "disturbance_time": 2.0,
  "base_frequency": 60.0,
  "frequency_metrics": {
    "#Gen38.wr:0": {
      "base_frequency": 60.0,
      "nadir_frequency": 59.6234,
      "nadir_time": 2.45,
      "max_rocof": 1.52,
      "steady_frequency": 59.85,
      "settling_time": 8.2,
      "frequency_deviation": -0.15
    }
  }
}
```

**CSV结果** (`fr_ieee39_20240324_143227.csv`):

| channel | nadir_freq | nadir_time | max_rocof | steady_freq | settling_time | frequency_deviation |
|---------|------------|------------|-----------|-------------|---------------|---------------------|
| #Gen38.wr:0 | 59.6234 | 2.4500 | 1.52 | 59.8500 | 8.20 | -0.15 |

**Markdown报告** (`fr_ieee39_20240324_143227_report.md`):

包含：
- 系统概况
- 频率响应指标表格
- 指标说明
- 结论（频率跌落较大，可能需要评估低频减载策略）

### 后续应用

基于频率响应分析结果，可以：

1. **低频减载整定**: 根据频率最低点设置减载启动频率
2. **惯量评估**: 评估系统是否需要增加同步调相机或储能
3. **一次调频优化**: 调整发电机调差系数
4. **新能源接入分析**: 评估新能源渗透率对频率响应的影响

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
