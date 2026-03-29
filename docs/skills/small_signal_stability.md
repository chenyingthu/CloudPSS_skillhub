# 小信号稳定分析技能 (Small Signal Stability Analysis)

## 设计背景

### 研究对象

小信号稳定性是指电力系统在受到小扰动（如负荷的随机波动）后，恢复到原稳态运行点的能力。这种稳定性问题主要表现为机电振荡，即发电机转子之间的相对摇摆。小信号稳定分析通过特征值分析方法，识别系统的机电振荡模式、阻尼特性和主导参与机组。

### 实际需求

在电力系统规划和运行中，小信号稳定分析用于：

1. **振荡风险评估**: 识别系统中存在的弱阻尼或负阻尼振荡模式
2. **PSS参数整定**: 为电力系统稳定器（PSS）提供整定依据
3. **运行方式优化**: 评估不同运行方式下的小信号稳定性
4. **控制策略验证**: 验证励磁系统、调速器等控制策略的稳定性影响
5. **规划方案比较**: 比较不同网架结构对小信号稳定性的影响

### 期望的输入和输出

**输入**:

- 电力系统模型（含详细的发电机和控制系统参数）
- 阻尼比阈值（判断弱阻尼的临界值）
- 机电振荡频率范围（通常0.1-2.0 Hz）
- 基准容量（用于归一化计算）

**输出**:

- 系统特征值及其阻尼特性
- 机电振荡模式列表（频率、阻尼比、稳定性状态）
- 参与因子分析结果（各发电机对各模式的参与程度）
- 弱阻尼模式识别结果
- 小信号稳定性评估报告

### 计算结果的用途和价值

小信号稳定分析结果可用于：

- **PSS整定**: 针对弱阻尼模式设计PSS参数
- **运行限值**: 确定系统的稳定传输极限
- **控制优化**: 调整励磁系统和调速器参数
- **风险评估**: 量化系统的小信号稳定裕度

## 功能特性

- **特征值分析**: 基于潮流结果构建状态矩阵，计算系统特征值
- **机电振荡模式识别**: 自动识别0.1-2.0 Hz范围内的机电振荡模式
- **阻尼比评估**: 评估各模式的阻尼水平，识别弱阻尼和负阻尼模式
- **参与因子分析**: 计算各发电机对各振荡模式的参与程度
- **稳定性综合评估**: 提供系统整体小信号稳定性评估结论
- **完整报告输出**: 生成JSON/CSV/Markdown多格式报告

## 快速开始

### 1. CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init small_signal_stability --output sss.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config sss.yaml
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("small_signal_stability")

# 配置
config = {
    "skill": "small_signal_stability",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "analysis": {
        "damping_threshold": 0.05,
        "freq_range": [0.1, 2.0],
        "base_power": 100.0
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "small_signal",
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
skill: small_signal_stability
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  damping_threshold: 0.05           # 弱阻尼阈值(阻尼比)
  freq_range: [0.1, 2.0]            # 机电振荡频率范围[Hz]
  base_power: 100.0                 # 基准容量[MVA]

output:
  format: json
  path: ./results/
  prefix: small_signal
  generate_report: true
```

## 配置Schema

### 完整配置结构

```yaml
skill: small_signal_stability       # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token（不推荐）
token_file: string                  # token文件路径（默认: cloudpss_token）

model:                                # 模型配置（必需rid: string）                         # 模型RID或本地路径（必需）
  source: enum                        # cloud | local（默认: cloud）

analysis:                             # 分析配置
  damping_threshold: number           # 弱阻尼阈值(阻尼比)（默认: 0.05）
  freq_range: array                   # 机电振荡频率范围[Hz]（默认: [0.1, 2.0]）
  base_power: number                  # 基准容量[MVA]（默认: 100.0）

output:                               # 输出配置
  format: enum                        # json | csv（默认: json）
  path: string                        # 输出目录（默认: ./results/）
  prefix: string                      # 文件名前缀（默认: small_signal）
  generate_report: boolean            # 是否生成报告（默认: true）
```

### 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"small_signal_stability" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `analysis.damping_threshold` | number | 否 | 0.05 | 弱阻尼阈值(阻尼比) |
| `analysis.freq_range` | array | 否 | [0.1, 2.0] | 机电振荡频率范围[Hz] |
| `analysis.base_power` | number | 否 | 100.0 | 基准容量[MVA] |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | small_signal | 文件名前缀 |
| `output.generate_report` | boolean | 否 | true | 是否生成Markdown报告 |

## Agent使用指南

### 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("small_signal_stability")

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

    # 获取稳定性评估
    assessment = data.get("stability_assessment", {})
    print(f"系统稳定: {assessment.get('is_stable')}")
    print(f"总模式数: {assessment.get('n_modes')}")
    print(f"弱阻尼模式: {assessment.get('n_weakly_damped')}")

    # 获取机电振荡模式
    for mode in data.get("oscillation_modes", []):
        if mode.get("is_electromechanical"):
            freq = mode["frequency"]
            damping = mode["damping_ratio"]
            status = mode["damping_status"]
            dominant = mode.get("dominant_gens", [])
            print(f"模式{mode['index']}: f={freq:.3f}Hz, ζ={damping:.3f}, {status}, 主导机={dominant}")

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
        print("错误: 基础潮流不收敛，检查模型数据")
    elif "系统中没有发电机" in error_msg:
        print("错误: 模型中未识别出发电机")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### JSON输出格式

```json
{
  "model": "IEEE39",
  "base_power": 100.0,
  "n_generators": 10,
  "n_buses": 39,
  "damping_threshold": 0.05,
  "freq_range": [0.1, 2.0],
  "eigenvalues": [
    {"real": -0.5234, "imag": 6.2832},
    {"real": -0.3125, "imag": 4.7124}
  ],
  "oscillation_modes": [
    {
      "index": 0,
      "eigenvalue": {"real": -0.5234, "imag": 6.2832},
      "frequency": 1.0,
      "damping_ratio": 0.083,
      "time_constant": 1.91,
      "status": "stable",
      "is_electromechanical": true,
      "damping_status": "良好阻尼",
      "dominant_gens": ["Gen30", "Gen38"]
    },
    {
      "index": 1,
      "eigenvalue": {"real": -0.1562, "imag": 3.1416},
      "frequency": 0.5,
      "damping_ratio": 0.049,
      "time_constant": 6.4,
      "status": "stable",
      "is_electromechanical": true,
      "damping_status": "弱阻尼",
      "dominant_gens": ["Gen31", "Gen32"]
    }
  ],
  "participation_factors": {
    "mode_0": {
      "frequency": 1.0,
      "dominant_generators": [
        {"gen": "Gen30", "total_p": 0.85, "delta_p": 0.9, "omega_p": 0.8},
        {"gen": "Gen38", "total_p": 0.72, "delta_p": 0.75, "omega_p": 0.68}
      ]
    }
  },
  "stability_assessment": {
    "n_modes": 20,
    "n_electromechanical": 9,
    "n_weakly_damped": 2,
    "n_unstable": 0,
    "is_stable": true
  }
}
```

### SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "small_signal_stability" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典（包含eigenvalues、oscillation_modes、participation_factors、stability_assessment） |
| `artifacts` | list | 输出文件列表（Artifact对象） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标 |

## 设计原理

### 工作流程

```
1. 潮流计算
   └── 获取系统稳态运行点

2. 系统数据提取
   └── 提取母线、发电机、支路参数
       └── 提取励磁系统、PSS、调速器参数

3. 状态矩阵构建
   └── 基于经典发电机模型(δ, ω)
       └── 计算同步功率系数
       └── 考虑多机耦合效应

4. 特征值分析
   └── 计算状态矩阵特征值
       └── 识别机电振荡模式(0.1-2.0 Hz)
       └── 计算阻尼比和频率

5. 参与因子计算
   └── 计算各发电机对各模式的参与程度
       └── 识别主导发电机

6. 结果输出
   └── 保存JSON/CSV结果和Markdown报告
```

### 数学模型

**状态方程**:

```
Δδ' = ω_s * Δω
Δω' = (-D * Δω - ΔPe) / (2H)
```

其中：
- δ: 转子角(rad)
- ω: 转速偏差(pu)
- ω_s: 同步角速度(rad/s)
- D: 阻尼系数
- H: 惯性时间常数(s)
- Pe: 电磁功率

**状态矩阵**:

```
A = [0, ω_s; -K/(2H), -D/(2H)]
```

其中K为同步功率系数。

**特征值与阻尼特性**:

- 特征值: λ = σ ± jω
- 振荡频率: f = ω / (2π) [Hz]
- 阻尼比: ζ = -σ / √(σ² + ω²)

### 判据标准

| 阻尼比 | 稳定性评估 | 建议措施 |
|--------|-----------|----------|
| ζ > 0.05 | 良好阻尼 | 无需调整 |
| 0.03 ≤ ζ ≤ 0.05 | 弱阻尼 | 考虑PSS整定 |
| 0 ≤ ζ < 0.03 | 很弱阻尼 | 必须配置PSS |
| ζ < 0 | 负阻尼(不稳定) | 紧急控制措施 |

## 与其他技能的关联

```
power_flow
    ↓ (基础潮流)
small_signal_stability
    ↓ (小信号稳定分析)
vsi_weak_bus
    ↓ (弱母线识别)
reactive_compensation_design
    ↓ (补偿方案)
参数优化
```

## 性能特点

- **计算时间**: IEEE39系统约5-10秒
- **内存占用**: 与系统规模和发电机数量成正比
- **特征值数量**: 2×发电机数量
- **适用规模**: 已测试至50台发电机系统
- **精度**: 基于线性化模型，适用于小扰动分析

## 常见问题

### 问题1: 潮流计算失败

**原因**: 模型数据错误或系统无解

**解决**:

```bash
# 先运行power_flow验证模型
python -m cloudpss_skills run --config power_flow.yaml
```

### 问题2: 特征值计算失败

**原因**: 状态矩阵奇异或数值问题

**解决**:

```yaml
analysis:
  base_power: 1000.0  # 调整基准容量改善数值稳定性
```

### 问题3: 机电模式识别不准确

**原因**: 频率范围设置不当

**解决**:

```yaml
analysis:
  freq_range: [0.05, 3.0]  # 扩大频率范围
```

### 问题4: 参与因子计算失败

**原因**: 特征向量计算数值问题

**解决**: 检查发电机数量是否匹配，尝试调整基准容量

## 完整示例

### 场景描述

某电力公司需要评估IEEE39系统的小信号稳定性，识别存在的机电振荡模式和弱阻尼模式，为PSS整定提供依据。

### 配置文件

创建文件 `sss_ieee39.yaml`:

```yaml
skill: small_signal_stability
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  damping_threshold: 0.05
  freq_range: [0.1, 2.0]
  base_power: 100.0

output:
  format: json
  path: ./results/
  prefix: sss_ieee39
  generate_report: true
```

### 执行命令

```bash
python -m cloudpss_skills run --config sss_ieee39.yaml
```

### 预期输出

```
[14:32:01] [INFO] 加载认证...
[14:32:02] [INFO] 认证成功
[14:32:02] [INFO] 模型: IEEE39
[14:32:03] [INFO] 小信号稳定性分析
[14:32:03] [INFO] 阻尼阈值: 0.05, 频率范围: 0.1-2.0 Hz
[14:32:04] [INFO] 运行潮流计算...
[14:32:04] [INFO] Job ID: job_xxx
[14:32:06] [INFO] 潮流计算完成
[14:32:06] [INFO] 提取系统数据...
[14:32:07] [INFO] 提取到 39 个母线, 10 台发电机
[14:32:07] [INFO] 构建状态矩阵...
[14:32:08] [INFO] 改进状态矩阵维度: 20x20 (每台机2状态，含详细参数)
[14:32:08] [INFO] 特征值分析...
[14:32:09] [INFO] 特征值分析完成:
[14:32:09] [INFO]   总模式数: 20
[14:32:09] [INFO]   机电振荡模式: 9
[14:32:09] [INFO]   弱阻尼模式: 2
[14:32:09] [INFO]   不稳定模式: 0
[14:32:09] [INFO] 计算参与因子...
[14:32:10] [INFO] 参与因子计算完成，分析了 9 个机电模式
[14:32:10] [INFO] 结果已保存: ./results/sss_ieee39_20240324_143210.json
[14:32:10] [INFO] 报告已保存: ./results/sss_ieee39_20240324_143210_report.md

[OK] 技能执行成功: small_signal_stability
耗时: 9.5s
```

### 结果文件

**JSON结果** (`sss_ieee39_20240324_143210.json`):

```json
{
  "model": "IEEE39",
  "base_power": 100.0,
  "n_generators": 10,
  "n_buses": 39,
  "stability_assessment": {
    "n_modes": 20,
    "n_electromechanical": 9,
    "n_weakly_damped": 2,
    "n_unstable": 0,
    "is_stable": true
  },
  "oscillation_modes": [
    {
      "index": 0,
      "frequency": 1.234,
      "damping_ratio": 0.083,
      "damping_status": "良好阻尼",
      "dominant_gens": ["Gen30", "Gen38"]
    },
    {
      "index": 3,
      "frequency": 0.567,
      "damping_ratio": 0.042,
      "damping_status": "弱阻尼",
      "dominant_gens": ["Gen31", "Gen32"]
    }
  ]
}
```

**CSV结果** (`sss_ieee39_20240324_143210.csv`):

| mode_id | eigenvalue_real | eigenvalue_imag | frequency_hz | damping_ratio | damping_status | dominant_gens |
|---------|-----------------|-----------------|--------------|---------------|----------------|---------------|
| 1 | -0.523456 | 6.283185 | 1.0000 | 0.0830 | 良好阻尼 | Gen30, Gen38 |
| 2 | -0.312500 | 4.712389 | 0.7500 | 0.0660 | 良好阻尼 | Gen33, Gen34 |
| 4 | -0.156250 | 3.141593 | 0.5000 | 0.0496 | 弱阻尼 | Gen31, Gen32 |
| 7 | -0.098765 | 1.884956 | 0.3000 | 0.0520 | 弱阻尼 | Gen35, Gen36 |

**Markdown报告** (`sss_ieee39_20240324_143210_report.md`):

包含：
- 系统概况
- 稳定性评估结论
- 机电振荡模式表格
- 弱阻尼模式分析
- PSS整定建议
- 模型说明

### 后续应用

基于小信号稳定分析结果，可以：

1. **PSS整定**: 针对弱阻尼模式调整PSS参数
2. **励磁优化**: 优化励磁系统增益和时间常数
3. **运行方式调整**: 避免弱阻尼运行方式
4. **对比分析**: 使用`result_compare`技能对比不同方案的稳定性

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
