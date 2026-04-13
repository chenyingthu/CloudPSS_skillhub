# 暂态稳定分析技能 (Transient Stability Analysis)

## 设计背景

### 研究对象

暂态稳定性是指电力系统在遭受大扰动（如短路故障、发电机跳闸、负荷突变等）后，各同步发电机保持同步运行的能力。暂态稳定分析通过时域仿真，模拟故障后发电机的动态响应，评估系统是否能在扰动后恢复到稳定运行状态。这是电力系统安全分析的核心内容之一。

### 实际需求

在电力系统规划和运行中，暂态稳定分析用于：

1. **故障场景评估**: 评估不同故障位置和类型对系统稳定性的影响
2. **保护整定配合**: 确定故障切除时间的临界值
3. **稳定控制策略**: 设计切机、切负荷等紧急控制措施
4. **运行方式校核**: 验证特定运行方式下的暂态稳定性
5. **规划方案比较**: 比较不同规划方案的暂态稳定性能

### 期望的输入和输出

**输入**:

- 电力系统模型（需配置EMT拓扑）
- 故障设置（位置、类型、起始时间、切除时间）
- 监测发电机列表（转速/功角信号通道）
- 稳定判据参数（最大转速偏差、阻尼比阈值等）

**输出**:

- 各故障切除时间下的稳定性评估
- 发电机转速/功角响应曲线数据
- 稳定指标（最大偏差、稳定时间、阻尼比等）
- 临界切除时间估计
- 暂态稳定性分析报告

### 计算结果的用途和价值

暂态稳定分析结果可用于：

- **保护整定**: 确定合理的故障切除时间
- **稳定控制**: 设计预防控制和紧急控制策略
- **运行限值**: 确定系统的暂态稳定传输极限
- **风险评估**: 量化系统的暂态稳定裕度

## 功能特性

- **故障切除时间扫描**: 自动扫描多个故障切除时间，评估稳定性趋势
- **多发电机监测**: 同时监测多台发电机的转速和功率响应
- **自动稳定判据**: 基于转速偏差和阻尼比自动判断稳定性
- **临界切除时间估计**: 通过插值估计临界切除时间
- **完整报告生成**: 生成JSON/CSV/Markdown多格式报告

## 快速开始

### 1. CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init transient_stability --output ts.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config ts.yaml
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("transient_stability")

# 配置
config = {
    "skill": "transient_stability",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE3",
        "source": "cloud"
    },
    "fault": {
        "location": "Bus7",
        "fs": 2.5,
        "fe_values": [2.7, 2.8, 2.9],
        "chg": 0.01
    },
    "generators": {
        "monitored": ["Gen1", "Gen2", "Gen3"],
        "speed_channels": ["#wr1:0", "#wr2:0", "#wr3:0"],
        "power_channels": ["#P1:0", "#P2:0", "#P3:0"]
    },
    "assessment": {
        "stable_criterion": "damped",
        "max_speed_deviation": 0.5,
        "analysis_window": [3.0, 8.0],
        "settling_time_threshold": 0.02
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "transient_stability",
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
skill: transient_stability
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

fault:
  location: "Bus7"                    # 故障位置
  fs: 2.5                             # 故障开始时间(s)
  fe_values: [2.7, 2.8, 2.9]          # 故障切除时间扫描值(s)
  chg: 0.01                           # 过渡电阻(pu)

generators:
  monitored: ["Gen1", "Gen2", "Gen3"]         # 监测发电机
  speed_channels: ["#wr1:0", "#wr2:0", "#wr3:0"]  # 转速信号通道
  power_channels: ["#P1:0", "#P2:0", "#P3:0"]      # 功率信号通道

assessment:
  stable_criterion: "damped"          # 稳定判据: damped | bounded
  max_speed_deviation: 0.5            # 最大允许转速偏差(pu)
  analysis_window: [3.0, 8.0]         # 分析时间窗口[s]
  settling_time_threshold: 0.02       # 稳定阈值(pu)

output:
  format: json
  path: ./results/
  prefix: transient_stability
  generate_report: true
```

## 配置Schema

### 完整配置结构

```yaml
skill: transient_stability           # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token（不推荐）
  token_file: string                  # token文件路径（默认: .cloudpss_token）
  server: enum                        # 服务器: public | internal（默认: public）

model:                                # 模型配置（必需）
  rid: string                         # 模型RID或本地路径（必需）
  source: enum                        # cloud | local（默认: cloud）

fault:                                # 故障配置（必需）
  location: string                    # 故障位置母线ID
  fs: number                          # 故障开始时间(s)（默认: 2.5）
  fe_values: array                    # 故障切除时间扫描值（默认: [2.7, 2.8, 2.9]）
  chg: number                         # 过渡电阻(pu)（默认: 0.01）

generators:                           # 发电机监测配置
  monitored: array                    # 监测发电机名称列表（默认: ["Gen1", "Gen2", "Gen3"]）
  speed_channels: array               # 转速信号通道（默认: ["#wr1:0", "#wr2:0", "#wr3:0"]）
  power_channels: array               # 功率信号通道（默认: ["#P1:0", "#P2:0", "#P3:0"]）

assessment:                           # 稳定评估配置
  stable_criterion: enum              # damped | bounded（默认: damped）
  max_speed_deviation: number         # 最大允许转速偏差(pu)（默认: 0.5）
  analysis_window: array              # 分析时间窗口[s]（默认: [3.0, 8.0]）
  settling_time_threshold: number     # 稳定阈值(pu)（默认: 0.02）

output:                               # 输出配置
  format: enum                        # json | csv（默认: json）
  path: string                        # 输出目录（默认: ./results/）
  prefix: string                      # 文件名前缀（默认: transient_stability）
  generate_report: boolean            # 是否生成报告（默认: true）
```

### 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"transient_stability" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `auth.server` | enum | 否 | public | 服务器：public(公共云) / internal(内部服务器) |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `fault.location` | string | 是 | - | 故障位置母线ID |
| `fault.fs` | number | 否 | 2.5 | 故障开始时间(s) |
| `fault.fe_values` | array | 否 | [2.7, 2.8, 2.9] | 故障切除时间扫描值列表 |
| `fault.chg` | number | 否 | 0.01 | 过渡电阻(pu) |
| `generators.monitored` | array | 否 | ["Gen1", "Gen2", "Gen3"] | 监测发电机名称列表 |
| `generators.speed_channels` | array | 否 | ["#wr1:0", ...] | 转速信号通道名 |
| `generators.power_channels` | array | 否 | ["#P1:0", ...] | 功率信号通道名 |
| `assessment.stable_criterion` | enum | 否 | damped | 稳定判据类型 |
| `assessment.max_speed_deviation` | number | 否 | 0.5 | 最大允许转速偏差(pu) |
| `assessment.analysis_window` | array | 否 | [3.0, 8.0] | 分析时间窗口[s] |
| `assessment.settling_time_threshold` | number | 否 | 0.02 | 稳定阈值(pu) |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | transient_stability | 文件名前缀 |
| `output.generate_report` | boolean | 否 | true | 是否生成Markdown报告 |

## Agent使用指南

### 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("transient_stability")

# 最小化配置（使用默认值）
config = {
    "model": {"rid": "model/holdme/IEEE3"},
    "fault": {"location": "Bus7"}
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

    # 获取稳定性趋势
    stability_trend = data.get("stability_trend")
    print(f"稳定性趋势: {stability_trend}")

    # 获取各工况结果
    for case in data.get("results", []):
        fe = case["fe"]
        stability = case["stability"]
        is_stable = stability.get("is_stable")
        max_dev = stability.get("max_speed_deviation")
        print(f"切除时间{fe}s: 稳定={is_stable}, 最大偏差={max_dev:.4f}")

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
  "model": "IEEE3",
  "fault_location": "Bus7",
  "stability_trend": "degrading_with_delay",
  "results": [
    {
      "fe": 2.7,
      "job_id": "job_xxx",
      "stability": {
        "is_stable": true,
        "max_speed_deviation": 0.0234,
        "settling_time": 5.2,
        "damping_ratio": 0.15,
        "oscillation_freq": 1.2
      }
    },
    {
      "fe": 2.8,
      "job_id": "job_xxx",
      "stability": {
        "is_stable": true,
        "max_speed_deviation": 0.0456,
        "settling_time": 6.5,
        "damping_ratio": 0.08,
        "oscillation_freq": 1.1
      }
    },
    {
      "fe": 2.9,
      "job_id": "job_xxx",
      "stability": {
        "is_stable": false,
        "max_speed_deviation": 0.5234,
        "settling_time": 8.0,
        "damping_ratio": -0.02,
        "oscillation_freq": 0.9
      }
    }
  ]
}
```

### SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "transient_stability" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典（包含stability_trend、results） |
| `artifacts` | list | 输出文件列表（Artifact对象） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标 |

## 设计原理

### 工作流程

```
1. 模型准备
   └── 获取基础模型

2. 故障配置
   └── 设置故障位置和切除时间

3. EMT仿真
   └── 对每个切除时间运行EMT仿真
       └── 等待仿真完成

4. 稳定性分析
   └── 提取发电机转速/功角响应
       └── 计算稳定性指标
           └── 最大转速偏差
           └── 稳定时间
           └── 阻尼比
           └── 振荡频率

5. 趋势分析
   └── 分析稳定性随切除时间的变化趋势
       └── 估计临界切除时间

6. 结果输出
   └── 保存JSON/CSV结果和Markdown报告
```

### 稳定性判据

**阻尼判据（damped）**:

- 转速偏差小于阈值（默认0.5 pu）
- 阻尼比大于0（振荡衰减）

**有界判据（bounded）**:

- 转速偏差小于阈值
- 不考虑阻尼特性

### 关键指标计算

- **最大转速偏差**: 故障后转速与基准的最大差值
- **稳定时间**: 转速进入稳态阈值的时间
- **阻尼比**: 通过对数递减法估算
- **振荡频率**: 通过峰值间隔计算

## 与其他技能的关联

```
power_flow
    ↓ (基础潮流)
emt_simulation (配置fault参数)
    ↓ (EMT仿真)
transient_stability
    ↓ (稳定性分析)
emt_n1_screening
    ↓ (N-1稳定筛查)
稳定控制策略设计
```

## 性能特点

- **仿真时间**: 每个工况约10-30秒
- **总时间**: 与扫描的切除时间数量成正比
- **内存占用**: 中等，与系统规模成正比
- **适用规模**: 已测试至39节点系统
- **建议**: 先用较大步长确定临界范围，再细化分析

## 常见问题

### 问题1: EMT仿真失败

**原因**: 模型未配置EMT拓扑

**解决**:
```bash
# 确保模型已配置EMT拓扑
# 可通过 emt_simulation 的 fault 配置调整故障参数
```

### 问题2: 转速信号提取失败

**原因**: 信号通道名称不匹配

**解决**:

```yaml
generators:
  speed_channels: ["#Gen31.wr:0", "#Gen32.wr:0", "#Gen33.wr:0"]  # IEEE39格式
  # 或自动检测
```

### 问题3: 仿真时间过长

**原因**: 切除时间范围过大或仿真时长过长

**解决**:

```yaml
fault:
  fs: 2.0                          # 提前故障开始时间
  fe_values: [2.1, 2.2, 2.3]       # 减少扫描点
assessment:
  analysis_window: [3.0, 6.0]      # 缩短分析窗口
```

### 问题4: 稳定性判断不准确

**原因**: 判据参数设置不当

**解决**:

```yaml
assessment:
  stable_criterion: "bounded"      # 对于强非线性系统使用有界判据
  max_speed_deviation: 0.3         # 降低允许偏差
  settling_time_threshold: 0.01    # 提高稳定阈值
```

## 完整示例

### 场景描述

某电力公司需要评估IEEE3系统在Bus7母线发生三相短路故障时的暂态稳定性，确定临界切除时间，为保护整定提供依据。

### 配置文件

创建文件 `ts_ieee3.yaml`:

```yaml
skill: transient_stability
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

fault:
  location: "Bus7"
  fs: 2.5
  fe_values: [2.7, 2.8, 2.9, 3.0, 3.1]
  chg: 0.01

generators:
  monitored: ["Gen1", "Gen2", "Gen3"]
  speed_channels: ["#wr1:0", "#wr2:0", "#wr3:0"]
  power_channels: ["#P1:0", "#P2:0", "#P3:0"]

assessment:
  stable_criterion: "damped"
  max_speed_deviation: 0.5
  analysis_window: [3.0, 8.0]
  settling_time_threshold: 0.02

output:
  format: json
  path: ./results/
  prefix: ts_ieee3
  generate_report: true
```

### 执行命令

```bash
python -m cloudpss_skills run --config ts_ieee3.yaml
```

### 预期输出

```
[14:32:01] [INFO] 加载认证...
[14:32:02] [INFO] 认证成功
[14:32:02] [INFO] 模型: IEEE3
[14:32:03] [INFO] 暂态稳定性分析: 5个故障切除时间
[14:32:03] [INFO] 监测发电机: ['Gen1', 'Gen2', 'Gen3']
[14:32:03] [INFO] 故障位置: Bus7
[14:32:04] [INFO] [1/5] 故障切除时间 fe=2.7s
[14:32:04] [INFO]   Job ID: job_xxx
[14:32:15] [INFO]   -> 稳定性: 稳定, 最大转速偏差: 0.0234
[14:32:15] [INFO] [2/5] 故障切除时间 fe=2.8s
...
[14:33:30] [INFO] 暂态稳定性分析完成
[14:33:30] [INFO] 稳定性趋势: partial_stable
[14:33:30] [INFO] 结果已保存: ./results/ts_ieee3_20240324_143330.json
[14:33:30] [INFO] 报告已保存: ./results/ts_ieee3_20240324_143330_report.md

[OK] 技能执行成功: transient_stability
耗时: 89.5s
```

### 结果文件

**JSON结果** (`ts_ieee3_20240324_143330.json`):

```json
{
  "model": "IEEE3",
  "fault_location": "Bus7",
  "stability_trend": "partial_stable",
  "results": [
    {
      "fe": 2.7,
      "job_id": "job_xxx",
      "stability": {
        "is_stable": true,
        "max_speed_deviation": 0.0234,
        "settling_time": 5.2,
        "damping_ratio": 0.15,
        "oscillation_freq": 1.2
      }
    },
    {
      "fe": 2.9,
      "job_id": "job_xxx",
      "stability": {
        "is_stable": false,
        "max_speed_deviation": 0.5234,
        "settling_time": 8.0,
        "damping_ratio": -0.02,
        "oscillation_freq": 0.9
      }
    }
  ]
}
```

**CSV结果** (`ts_ieee3_20240324_143330.csv`):

| fe | is_stable | max_speed_dev | settling_time | damping_ratio | oscillation_freq |
|----|-----------|---------------|---------------|---------------|------------------|
| 2.7 | true | 0.0234 | 5.20 | 0.1500 | 1.20 |
| 2.8 | true | 0.0456 | 6.50 | 0.0800 | 1.10 |
| 2.9 | false | 0.5234 | 8.00 | -0.0200 | 0.90 |
| 3.0 | false | 0.6234 | 8.00 | -0.0500 | 0.80 |
| 3.1 | false | 0.7234 | 8.00 | -0.0800 | 0.70 |

**Markdown报告** (`ts_ieee3_20240324_143330_report.md`):

- 摘要统计
- 各工况稳定性评估表格
- 结论（部分稳定，临界切除时间约在2.8-2.9s之间）
- 建议

### 后续应用

基于暂态稳定分析结果，可以：

1. **N-1稳定筛查**: 使用`emt_n1_screening`技能批量评估多种故障场景
2. **参数扫描**: 使用`fault_clearing_scan`技能更精确地确定临界切除时间
3. **稳定控制设计**: 根据薄弱场景设计切机、切负荷策略
4. **结果对比**: 使用`result_compare`技能对比不同方案的稳定性

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
