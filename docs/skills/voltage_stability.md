# 电压稳定分析技能 (Voltage Stability Analysis)

## 设计背景

### 研究对象

电压稳定是电力系统安全运行的重要指标，指系统在受到扰动后维持所有母线电压在可接受范围内的能力。电压失稳可能导致电压崩溃，造成大面积停电事故。电压稳定分析通过连续潮流计算，逐步增加负荷直至电压崩溃点，识别系统的电压稳定极限和薄弱区域。

### 实际需求

在电力系统规划和运行中，需要评估系统的电压稳定性，以便：

1. **确定电压稳定裕度**: 评估系统距离电压崩溃的距离
2. **识别薄弱母线**: 找出容易发生电压崩溃的关键节点
3. **指导无功规划**: 确定无功补偿设备的安装位置和容量
4. **运行方式优化**: 评估不同运行方式下的电压稳定性
5. **预防电压崩溃**: 提前预警，避免电压失稳事故

### 期望的输入和输出

**输入**:

- 电力系统模型（IEEE39等标准系统或实际系统）
- 负荷增长扫描参数（增长倍数列表）
- 监测母线列表（用于生成PV曲线）
- 电压崩溃阈值（判断崩溃的电压水平）
- 发电机出力调整策略（是否随负荷同步增长）

**输出**:

- 各负荷水平下的母线电压
- 电压崩溃点和最大负荷能力
- PV曲线数据（电压-功率曲线）
- 薄弱母线识别结果
- 电压稳定性评估报告

### 计算结果的用途和价值

电压稳定分析结果可直接用于：

- **无功补偿规划**: VSI高的母线优先安装补偿设备
- **运行限值设定**: 确定系统的最大负荷能力
- **N-1校核**: 评估故障后的电压稳定性
- **电压控制策略**: 指导AVR和OLTC的设置

## 功能特性

- **连续潮流分析**: 逐步增加负荷直到电压崩溃，记录全过程
- **PV曲线生成**: 自动生成母线电压-负荷功率（P-V）曲线
- **自动崩溃检测**: 基于电压阈值自动识别电压崩溃点
- **多母线监测**: 支持同时监测多个关键母线的电压变化
- **发电机协调调整**: 可配置发电机出力随负荷同步增长
- **完整报告输出**: 生成JSON/CSV/Markdown多格式报告

## 快速开始

### 1. CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init voltage_stability --output vs.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config vs.yaml
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("voltage_stability")

# 配置
config = {
    "skill": "voltage_stability",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "scan": {
        "load_scaling": [1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
        "scale_generation": True
    },
    "monitoring": {
        "buses": ["Bus30", "Bus38"],
        "collapse_threshold": 0.7
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "voltage_stability",
        "generate_report": True,
        "export_pv_curve": True
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
skill: voltage_stability
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

scan:
  load_scaling: [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]  # 负荷增长倍数
  scale_generation: true                          # 同步调整发电机出力

monitoring:
  buses: ["Bus30", "Bus38"]                       # 监测母线
  collapse_threshold: 0.7                         # 电压崩溃阈值(pu)

output:
  format: json
  path: ./results/
  prefix: voltage_stability
  generate_report: true
  export_pv_curve: true
```

## 配置Schema

### 完整配置结构

```yaml
skill: voltage_stability              # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token（不推荐）
  token_file: string                  # token文件路径（默认: .cloudpss_token）

model:                                # 模型配置（必需）
  rid: string                         # 模型RID或本地路径（必需）
  source: enum                        # cloud | local（默认: cloud）

scan:                                 # 负荷扫描配置
  load_scaling: array                 # 负荷增长倍数列表（默认: [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]）
  load_target: string                 # 目标负荷组件（可选）
  scale_generation: boolean           # 是否同步调整发电机出力（默认: true）

monitoring:                           # 监测配置
  buses: array                        # 监测母线列表（可选）
  collapse_threshold: number          # 电压崩溃阈值(pu)（默认: 0.7）

output:                               # 输出配置
  format: enum                        # json | csv（默认: json）
  path: string                        # 输出目录（默认: ./results/）
  prefix: string                      # 文件名前缀（默认: voltage_stability）
  generate_report: boolean            # 是否生成报告（默认: true）
  export_pv_curve: boolean            # 是否导出PV曲线数据（默认: true）
```

### 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"voltage_stability" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `scan.load_scaling` | array | 否 | [1.0, 1.2, ..., 2.0] | 负荷增长倍数列表 |
| `scan.load_target` | string | 否 | - | 指定要调整的目标负荷组件 |
| `scan.scale_generation` | boolean | 否 | true | 是否随负荷增长同步调整发电机出力 |
| `monitoring.buses` | array | 否 | [] | 监测电压的母线列表 |
| `monitoring.collapse_threshold` | number | 否 | 0.7 | 电压崩溃阈值(pu) |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | voltage_stability | 文件名前缀 |
| `output.generate_report` | boolean | 否 | true | 是否生成Markdown报告 |
| `output.export_pv_curve` | boolean | 否 | true | 是否导出PV曲线CSV数据 |

## Agent使用指南

### 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("voltage_stability")

# 最小化配置（使用默认值）
config = {
    "model": {"rid": "model/holdme/IEEE39"}
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

    # 获取电压稳定极限
    collapse_point = data.get("collapse_point")
    max_loadability = data.get("max_loadability")
    print(f"电压崩溃点: {collapse_point}x")
    print(f"最大负荷能力: {max_loadability}x")

    # 获取各工况结果
    for case in data.get("results", []):
        scale = case["scale"]
        min_v = case.get("min_voltage", 0)
        print(f"负荷{scale}x: 最小电压={min_v:.4f} pu")

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
    elif "潮流计算失败" in error_msg:
        print("错误: 系统可能无解，尝试降低负荷增长倍数")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### JSON输出格式

```json
{
  "model": "IEEE39",
  "collapse_threshold": 0.7,
  "collapse_point": 1.8,
  "max_loadability": 1.6,
  "total_cases": 6,
  "converged_cases": 5,
  "results": [
    {
      "scale": 1.0,
      "converged": true,
      "job_id": "job_xxx",
      "voltages": {"Bus30": 1.02, "Bus38": 0.98},
      "min_voltage": 0.98
    },
    {
      "scale": 1.2,
      "converged": true,
      "job_id": "job_xxx",
      "voltages": {"Bus30": 0.95, "Bus38": 0.92},
      "min_voltage": 0.92
    }
  ],
  "pv_curve": [
    {"bus": "Bus30", "scale": 1.0, "voltage": 1.02},
    {"bus": "Bus30", "scale": 1.2, "voltage": 0.95},
    {"bus": "Bus38", "scale": 1.0, "voltage": 0.98},
    {"bus": "Bus38", "scale": 1.2, "voltage": 0.92}
  ]
}
```

### SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "voltage_stability" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典（包含collapse_point、max_loadability、results、pv_curve） |
| `artifacts` | list | 输出文件列表（Artifact对象） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标 |

## 设计原理

### 工作流程

```
1. 基础潮流计算
   └── 获取初始运行状态

2. 负荷增长扫描
   └── 按load_scaling列表逐步增加负荷
       └── 可选：同步调整发电机出力

3. 连续潮流计算
   └── 每个负荷水平运行潮流计算
       └── 记录收敛状态和母线电压

4. 电压崩溃检测
   └── 检查最小电压是否低于collapse_threshold
       └── 识别第一个崩溃点

5. PV曲线生成
   └── 整理各工况的电压数据
       └── 生成P-V曲线数据点

6. 结果输出
   └── 保存JSON/CSV结果和Markdown报告
```

### 数学原理

连续潮流法（Continuation Power Flow）通过逐步增加负荷参数λ，求解以下方程：

```
f(x, λ) = 0
```

其中：
- x: 系统状态变量（电压幅值和相角）
- λ: 负荷增长参数
- f: 潮流方程

当Jacobian矩阵奇异时，系统到达电压稳定极限（崩溃点）。

## 与其他技能的关联

```
power_flow
    ↓ (基础潮流)
voltage_stability
    ↓ (电压稳定分析)
reactive_compensation_design
    ↓ (补偿方案设计)
dudv_curve
    ↓ (详细验证)
电压稳定性验证
```

## 性能特点

- **执行时间**: IEEE39系统约30-60秒（6个负荷水平）
- **内存占用**: 与系统规模成正比
- **收敛性**: 依赖系统强度和负荷增长步长
- **适用规模**: 已测试至500节点系统
- **建议**: 先用较大步长测试，再细化分析

## 常见问题

### 问题1: 潮流不收敛

**原因**:

- 负荷增长过快
- 系统强度不足
- 缺少无功支撑

**解决**:

```yaml
scan:
  load_scaling: [1.0, 1.1, 1.2, 1.3, 1.4]  # 减小步长
```

### 问题2: 电压崩溃点识别不准确

**原因**:

- collapse_threshold设置不当
- 监测母线选择不合适

**解决**:

```yaml
monitoring:
  buses: ["Bus30", "Bus38", "Bus15"]  # 选择负荷中心母线
  collapse_threshold: 0.75              # 根据实际情况调整
```

### 问题3: PV曲线数据不平滑

**原因**:

- 负荷增长步长过大
- 发电机出力未协调调整

**解决**:

```yaml
scan:
  load_scaling: [1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3]  # 更细的步长
  scale_generation: true  # 确保发电机协调调整
```

### 问题4: 结果文件过大

**原因**:

- 监测母线过多
- 负荷扫描点过密

**解决**:

```yaml
monitoring:
  buses: ["Bus30"]  # 只监测关键母线
scan:
  load_scaling: [1.0, 1.2, 1.4, 1.6, 1.8]  # 减少扫描点
```

## 完整示例

### 场景描述

某电力公司计划评估IEEE39系统的电压稳定裕度，确定系统的最大负荷能力和薄弱母线，为无功补偿规划提供依据。

### 配置文件

创建文件 `vs_ieee39.yaml`:

```yaml
skill: voltage_stability
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

scan:
  load_scaling: [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
  scale_generation: true

monitoring:
  buses: ["Bus30", "Bus38", "Bus15", "Bus16"]
  collapse_threshold: 0.7

output:
  format: json
  path: ./results/
  prefix: vs_ieee39
  generate_report: true
  export_pv_curve: true
```

### 执行命令

```bash
python -m cloudpss_skills run --config vs_ieee39.yaml
```

### 预期输出

```
[14:32:01] [INFO] 加载认证...
[14:32:02] [INFO] 认证成功
[14:32:02] [INFO] 模型: IEEE39
[14:32:03] [INFO] 电压稳定性分析: 6个负荷水平
[14:32:03] [INFO] 负荷增长范围: 1.0x ~ 2.0x
[14:32:03] [INFO] 监测母线: ['Bus30', 'Bus38', 'Bus15', 'Bus16']
[14:32:03] [INFO] 电压崩溃阈值: 0.7 pu
[14:32:03] [INFO] 基线负荷数: 19, 发电机数: 10
[14:32:04] [INFO] [1/6] 负荷水平=1.0x
[14:32:04] [INFO]   Job ID: job_xxx
[14:32:06] [INFO]   -> 最小电压: 0.9823 pu
[14:32:06] [INFO] [2/6] 负荷水平=1.2x
[14:32:09] [INFO]   -> 最小电压: 0.9456 pu
...
[14:33:15] [INFO] 电压稳定性分析完成
[14:33:15] [INFO] 电压崩溃点: 1.8x
[14:33:15] [INFO] 最大负荷能力: 1.6x
[14:33:15] [INFO] 结果已保存: ./results/vs_ieee39_20240324_143315.json
[14:33:15] [INFO] 报告已保存: ./results/vs_ieee39_20240324_143315_report.md

[OK] 技能执行成功: voltage_stability
耗时: 72.5s
```

### 结果文件

**JSON结果** (`vs_ieee39_20240324_143315.json`):

```json
{
  "model": "IEEE39",
  "collapse_threshold": 0.7,
  "collapse_point": 1.8,
  "max_loadability": 1.6,
  "total_cases": 6,
  "converged_cases": 5,
  "results": [
    {
      "scale": 1.0,
      "converged": true,
      "job_id": "job_xxx",
      "voltages": {"Bus30": 1.0234, "Bus38": 0.9823, "Bus15": 0.9456, "Bus16": 0.9123},
      "min_voltage": 0.9123
    },
    {
      "scale": 1.2,
      "converged": true,
      "job_id": "job_xxx",
      "voltages": {"Bus30": 0.9876, "Bus38": 0.9456, "Bus15": 0.9023, "Bus16": 0.8654},
      "min_voltage": 0.8654
    }
  ],
  "pv_curve": [
    {"bus": "Bus30", "scale": 1.0, "voltage": 1.0234},
    {"bus": "Bus30", "scale": 1.2, "voltage": 0.9876},
    {"bus": "Bus38", "scale": 1.0, "voltage": 0.9823},
    {"bus": "Bus38", "scale": 1.2, "voltage": 0.9456}
  ]
}
```

**CSV结果** (`vs_ieee39_20240324_143315.csv`):

| load_scale | converged | min_voltage | V_Bus30 | V_Bus38 | V_Bus15 | V_Bus16 |
|------------|-----------|-------------|---------|---------|---------|---------|
| 1.0 | true | 0.9123 | 1.0234 | 0.9823 | 0.9456 | 0.9123 |
| 1.2 | true | 0.8654 | 0.9876 | 0.9456 | 0.9023 | 0.8654 |
| 1.4 | true | 0.8123 | 0.9456 | 0.9023 | 0.8567 | 0.8123 |
| 1.6 | true | 0.7567 | 0.9023 | 0.8567 | 0.8023 | 0.7567 |
| 1.8 | false | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2.0 | false | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

**PV曲线数据** (`vs_ieee39_pv_curve_20240324_143315.csv`):

| bus | load_scale | voltage_pu |
|-----|------------|------------|
| Bus30 | 1.0 | 1.0234 |
| Bus30 | 1.2 | 0.9876 |
| ... | ... | ... |

**Markdown报告** (`vs_ieee39_20240324_143315_report.md`):

- 摘要统计
- 电压变化情况
- PV曲线数据
- 结论和建议

### 后续应用

基于电压稳定分析结果，可以：

1. **运行VSI弱母线分析**: 使用`vsi_weak_bus`技能识别薄弱母线
2. **设计无功补偿**: 使用`reactive_compensation_design`技能设计补偿方案
3. **生成DUDV曲线**: 使用`dudv_curve`技能验证补偿效果
4. **进行对比分析**: 使用`result_compare`技能对比补偿前后的稳定性

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
