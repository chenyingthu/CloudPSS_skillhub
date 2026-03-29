# 参数灵敏度分析技能 (Parameter Sensitivity)

## 设计背景

### 研究对象

电力系统的安全稳定运行依赖于各种元件参数的准确性。参数灵敏度分析技能用于分析系统关键输出指标（如母线电压、线路潮流等）对元件参数（如负荷有功/无功、线路阻抗、发电机出力等）变化的敏感程度，识别对系统性能影响最大的关键参数。

### 实际需求

在电力系统分析、规划和运行中，参数灵敏度分析具有以下重要作用：

1. **关键参数识别**: 确定对系统性能影响最大的参数
2. **参数优化指导**: 为参数调整和优化提供依据
3. **不确定性分析**: 评估参数不确定性对结果的影响
4. **风险评估**: 识别参数变化可能导致的安全隐患
5. **模型简化**: 识别可以忽略的次要参数，简化模型
6. **运行策略制定**: 指导运行参数的调整范围和优先级

### 期望的输入和输出

**输入**:
- 电力系统模型（标准系统或实际系统）
- 目标参数列表（需要分析的元件和参数）
- 扰动幅度（参数变化的百分比或绝对值）
- 输出指标（需要监测的系统响应）
- 基础运行点（潮流计算结果）

**输出**:
- 各参数的灵敏度系数
- 灵敏度排序结果
- 关键参数识别
- 灵敏度矩阵
- 可视化图表（灵敏度条形图、 tornado图等）

### 计算结果的用途和价值

参数灵敏度分析结果可直接用于：
- 识别需要精确测量或校准的关键参数
- 评估参数不确定性对分析结果的影响范围
- 指导运行人员关注对系统影响最大的可调参数
- 为参数优化和系统改造提供优先顺序
- 支持风险评估和决策制定
- 验证模型简化的合理性

## 功能特性

- **多参数分析**: 支持同时对多个元件参数进行灵敏度分析
- **多种扰动方式**: 支持相对扰动（百分比）和绝对扰动
- **多指标监测**: 可同时监测电压、功率、损耗等多种输出指标
- **灵敏度排序**: 自动按灵敏度大小排序，识别关键参数
- **可视化输出**: 生成灵敏度条形图、tornado图等可视化结果
- **批量分析**: 支持批量参数组合分析
- **结果对比**: 支持不同运行方式下的灵敏度对比

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init parameter_sensitivity --output ps.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config ps.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("parameter_sensitivity")

# 配置
config = {
    "skill": "parameter_sensitivity",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "analysis": {
        "target_parameters": [
            {
                "component": "Load_1",
                "parameter": "P",
                "perturbation": 0.1,  # 10%扰动
                "perturbation_type": "relative"
            },
            {
                "component": "Load_3",
                "parameter": "Q",
                "perturbation": 0.1
            },
            {
                "component": "Line_1",
                "parameter": "X",
                "perturbation": 0.05  # 5%扰动
            }
        ],
        "output_metrics": [
            {"type": "voltage", "bus": "Bus_16"},
            {"type": "power_flow", "branch": "Line_2"},
            {"type": "loss"}
        ]
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "sensitivity",
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
skill: parameter_sensitivity
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  target_parameters:          # 目标参数列表
    - component: Load_1       # 元件名称
      parameter: P            # 参数名称
      perturbation: 0.1       # 扰动幅度
      perturbation_type: relative  # 扰动类型: relative(相对) | absolute(绝对)
    - component: Load_3
      parameter: Q
      perturbation: 0.1
      perturbation_type: relative
    - component: Line_1
      parameter: X
      perturbation: 0.05
      perturbation_type: relative
    - component: Gen_1
      parameter: Vset
      perturbation: 0.02
      perturbation_type: relative

  output_metrics:             # 输出指标列表
    - type: voltage           # 电压
      bus: Bus_16             # 母线标签
    - type: voltage
      bus: Bus_15
    - type: power_flow        # 支路潮流
      branch: Line_2
    - type: loss              # 系统损耗

  method: central_diff        # 灵敏度计算方法: forward_diff | central_diff

calculation:
  base_power_flow: true       # 先计算基础潮流
  convergence_tolerance: 1e-6 # 潮流收敛精度

output:
  format: json
  path: ./results/
  prefix: sensitivity_ieee39
  timestamp: true
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: parameter_sensitivity            # 必需: 技能名称
auth:                                   # 认证配置
  token: string                         # 直接提供token（不推荐）
  token_file: string                    # token文件路径（默认: .cloudpss_token）

model:                                  # 模型配置（必需）
  rid: string                           # 模型RID或本地路径（必需）
  source: enum                          # cloud | local（默认: cloud）

analysis:                               # 分析配置（必需）
  target_parameters: array              # 目标参数列表（必需）
    - component: string                 # 元件名称
      parameter: string                 # 参数名称
      perturbation: number              # 扰动幅度
      perturbation_type: enum           # relative | absolute（默认: relative）
  output_metrics: array                 # 输出指标列表
    - type: enum                        # voltage | power_flow | loss | angle
      bus: string                       # 母线标签（voltage/angle类型）
      branch: string                    # 支路标签（power_flow类型）
  method: enum                          # forward_diff | central_diff（默认: central_diff）

calculation:                            # 计算配置
  base_power_flow: boolean              # 是否计算基础潮流（默认: true）
  convergence_tolerance: number         # 潮流收敛精度（默认: 1e-6）
  max_iterations: integer               # 最大迭代次数（默认: 100）

output:                                 # 输出配置
  format: enum                          # json | csv（默认: json）
  path: string                          # 输出目录（默认: ./results/）
  prefix: string                        # 文件名前缀（默认: sensitivity）
  timestamp: boolean                    # 是否添加时间戳（默认: true）
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"parameter_sensitivity" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `analysis.target_parameters` | array | 是 | - | 目标参数列表 |
| `analysis.target_parameters[].component` | string | 是 | - | 元件名称/标签 |
| `analysis.target_parameters[].parameter` | string | 是 | - | 参数名称（P, Q, X, R, Vset等） |
| `analysis.target_parameters[].perturbation` | number | 是 | - | 扰动幅度 |
| `analysis.target_parameters[].perturbation_type` | enum | 否 | relative | 扰动类型：relative(相对) / absolute(绝对) |
| `analysis.output_metrics` | array | 是 | - | 输出指标列表 |
| `analysis.output_metrics[].type` | enum | 是 | - | 指标类型：voltage / power_flow / loss / angle |
| `analysis.output_metrics[].bus` | string | 条件 | - | 母线标签（voltage/angle类型必需） |
| `analysis.output_metrics[].branch` | string | 条件 | - | 支路标签（power_flow类型必需） |
| `analysis.method` | enum | 否 | central_diff | 灵敏度计算方法 |
| `calculation.base_power_flow` | boolean | 否 | true | 是否先计算基础潮流 |
| `calculation.convergence_tolerance` | number | 否 | 1e-6 | 潮流收敛精度 |
| `calculation.max_iterations` | integer | 否 | 100 | 最大迭代次数 |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | sensitivity | 文件名前缀 |
| `output.timestamp` | boolean | 否 | true | 文件名是否包含时间戳 |

## Agent使用指南

### 5.1 基本调用模式

```python
# 获取技能实例
skill = get_skill("parameter_sensitivity")

# 最小化配置（使用默认值）
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "target_parameters": [
            {"component": "Load_1", "parameter": "P", "perturbation": 0.1}
        ],
        "output_metrics": [
            {"type": "voltage", "bus": "Bus_16"}
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

    # 访问灵敏度矩阵
    sensitivity_matrix = data.get("sensitivity_matrix", {})
    for param, sensitivities in sensitivity_matrix.items():
        print(f"参数 {param}:")
        for metric, value in sensitivities.items():
            print(f"  -> {metric}: {value:.6f}")

    # 访问灵敏度排序
    rankings = data.get("rankings", {})
    for metric, params in rankings.items():
        print(f"指标 {metric} 的关键参数:")
        for i, (param, sens) in enumerate(params[:5], 1):
            print(f"  {i}. {param}: {sens:.6f}")

    # 访问基础运行点
    base_case = data.get("base_case", {})
    print(f"基础运行点: {base_case}")

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
    if "Token文件不存在" in error_msg:
        print("错误: 请创建.cloudpss_token文件")
    elif "模型不存在" in error_msg:
        print("错误: 请检查模型RID是否正确")
    elif "参数不存在" in error_msg:
        print("错误: 请检查target_parameters中的元件和参数名称")
    elif "潮流不收敛" in error_msg:
        print("错误: 参数扰动后潮流不收敛，请减小perturbation")
    elif "元件不存在" in error_msg:
        print("错误: 请检查component名称是否正确")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "model": "IEEE39",
  "model_rid": "model/holdme/IEEE39",
  "timestamp": "2024-03-24T14:32:01",
  "base_case": {
    "voltage": {"Bus_16": 1.0234, "Bus_15": 1.0156},
    "power_flow": {"Line_2": 150.5},
    "loss": 45.3
  },
  "sensitivity_matrix": {
    "Load_1.P": {
      "Bus_16.voltage": -0.0152,
      "Bus_15.voltage": -0.0128,
      "Line_2.power_flow": 0.856,
      "loss": 0.234
    },
    "Load_3.Q": {
      "Bus_16.voltage": -0.0256,
      "Bus_15.voltage": -0.0213,
      "Line_2.power_flow": 0.234,
      "loss": 0.156
    },
    "Line_1.X": {
      "Bus_16.voltage": 0.0089,
      "Bus_15.voltage": 0.0076,
      "Line_2.power_flow": -0.456,
      "loss": 0.678
    }
  },
  "rankings": {
    "Bus_16.voltage": [
      ["Load_3.Q", -0.0256],
      ["Load_1.P", -0.0152],
      ["Line_1.X", 0.0089]
    ],
    "loss": [
      ["Line_1.X", 0.678],
      ["Load_1.P", 0.234],
      ["Load_3.Q", 0.156]
    ]
  },
  "summary": {
    "total_parameters": 3,
    "total_metrics": 4,
    "most_sensitive_param": "Load_3.Q",
    "most_sensitive_metric": "Bus_16.voltage"
  }
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "parameter_sensitivity" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典，包含灵敏度矩阵和排序 |
| `artifacts` | list | 输出文件列表（Artifact对象），包含JSON和CSV结果 |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标，包括参数分析耗时 |

## 设计原理

### 工作流程

```
1. 模型加载与基础潮流计算
   ├── 加载系统模型
   ├── 计算基础运行点潮流
   └── 记录基础输出指标

2. 参数扰动循环
   对于每个目标参数:
   ├── 应用正向扰动 (+ΔP)
   │   ├── 修改参数值
   │   ├── 计算扰动后潮流
   │   └── 记录输出指标
   ├── 应用负向扰动 (-ΔP, 中央差分法)
   │   ├── 修改参数值
   │   ├── 计算扰动后潮流
   │   └── 记录输出指标
   └── 恢复原始参数值

3. 灵敏度计算
   ├── 前向差分法:
   │   S = (Y(P+ΔP) - Y(P)) / ΔP
   ├── 中央差分法:
   │   S = (Y(P+ΔP) - Y(P-ΔP)) / (2×ΔP)
   └── 计算各参数对各指标的灵敏度

4. 结果排序与输出
   ├── 对每个指标，按灵敏度绝对值排序
   ├── 识别关键参数
   ├── 生成灵敏度矩阵
   └── 输出可视化图表
```

### 灵敏度计算方法

**前向差分法 (Forward Difference)**:
```
S = ∂Y/∂P ≈ (Y(P+ΔP) - Y(P)) / ΔP
```
- 计算量小（每参数2次潮流）
- 精度较低（一阶精度）

**中央差分法 (Central Difference)**:
```
S = ∂Y/∂P ≈ (Y(P+ΔP) - Y(P-ΔP)) / (2×ΔP)
```
- 计算量大（每参数3次潮流）
- 精度较高（二阶精度）

其中：
- `S`: 灵敏度系数
- `Y`: 输出指标（电压、功率等）
- `P`: 参数值
- `ΔP`: 扰动幅度

## 与其他技能的关联

```
parameter_sensitivity
    ↓ (灵敏度结果)
param_scan
    ↓ (参数扫描)
vsi_weak_bus / voltage_stability
    ↓ (稳定性分析)
reactive_compensation_design
    ↓ (补偿设计)
结果对比
```

### 依赖关系

- **必需依赖**: CloudPSS SDK (`cloudpss`)
- **输入依赖**: 无（直接使用模型）
- **输出被依赖**:
  - `param_scan`: 根据灵敏度确定扫描参数范围
  - `reactive_compensation_design`: 识别关键可调参数
  - `vsi_weak_bus`: 评估参数变化对电压稳定的影响

## 性能特点

- **执行时间**: IEEE39系统3参数×4指标约30-60秒
- **计算量**: 中央差分法约需 (2N+1) 次潮流计算，N为参数个数
- **精度**: 中央差分法二阶精度，前向差分法一阶精度
- **适用规模**: 已测试至100参数×50指标
- **内存占用**: 与参数和指标数量成正比

## 常见问题

### 问题1: 某些扰动后潮流不收敛

**原因**:
- 扰动幅度过大
- 参数变化导致系统无解
- 接近稳定边界

**解决**:
```yaml
analysis:
  target_parameters:
    - component: Load_1
      parameter: P
      perturbation: 0.05   # 减小到5%
  method: forward_diff     # 改用前向差分（只正向扰动）
```

### 问题2: 灵敏度结果不稳定

**原因**:
- 潮流收敛精度不够
- 参数在临界点附近
- 数值精度问题

**解决**:
```yaml
calculation:
  convergence_tolerance: 1e-8   # 提高收敛精度
  max_iterations: 200           # 增加最大迭代次数
```

### 问题3: 参数不存在或类型错误

**原因**:
- 元件名称错误
- 参数名称错误
- 参数不支持扰动

**解决**:
- 检查元件标签拼写
- 支持的参数：P, Q, R, X, B, Vset, Pset等
- 参考模型定义文件确认参数名称

### 问题4: 分析耗时过长

**原因**:
- 参数数量过多
- 使用中央差分法
- 系统规模大

**解决**:
- 优先分析关键参数
- 使用前向差分法
- 分批分析

```yaml
analysis:
  method: forward_diff   # 改用前向差分，速度提高约50%
```

### 问题5: 灵敏度结果与预期不符

**原因**:
- 基础运行点选择不当
- 非线性效应显著
- 多参数耦合影响

**解决**:
- 检查基础潮流结果
- 减小扰动幅度
- 考虑多参数联合分析

## 完整示例

### 场景描述

某电力公司需要分析IEEE39系统中各负荷变化对关键母线电压和系统损耗的影响，以确定需要重点监控和调节的关键负荷。分析3个关键负荷（Load_1、Load_3、Load_8）的有功和无功功率变化对Bus_16、Bus_15电压以及系统总损耗的灵敏度。

### 配置文件

```yaml
skill: parameter_sensitivity
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  target_parameters:
    # 负荷有功功率
    - component: Load_1
      parameter: P
      perturbation: 0.1
      perturbation_type: relative
    - component: Load_3
      parameter: P
      perturbation: 0.1
      perturbation_type: relative
    - component: Load_8
      parameter: P
      perturbation: 0.1
      perturbation_type: relative
    # 负荷无功功率
    - component: Load_1
      parameter: Q
      perturbation: 0.1
      perturbation_type: relative
    - component: Load_3
      parameter: Q
      perturbation: 0.1
      perturbation_type: relative
    - component: Load_8
      parameter: Q
      perturbation: 0.1
      perturbation_type: relative

  output_metrics:
    - type: voltage
      bus: Bus_16
    - type: voltage
      bus: Bus_15
    - type: loss

  method: central_diff
calculation:
  base_power_flow: true
  convergence_tolerance: 1e-6
  max_iterations: 100

output:
  format: json
  path: ./results/
  prefix: sensitivity_loads
  timestamp: true
```

### 执行命令

```bash
python -m cloudpss_skills run --config sensitivity_config.yaml
```

### 预期输出

```
[INFO] 加载认证信息...
[INFO] 认证成功
[INFO] 获取模型: IEEE39
[INFO] 计算基础潮流...
[INFO] 基础潮流收敛
[INFO] 开始参数灵敏度分析...
[INFO] 分析参数: 6个
[INFO] 监测指标: 3个
[INFO] [1/6] 分析 Load_1.P ...
[INFO] [2/6] 分析 Load_3.P ...
[INFO] [6/6] 分析 Load_8.Q ...
[INFO] 生成灵敏度矩阵...
[INFO] 灵敏度排序:
[INFO]   Bus_16.voltage 最敏感: Load_3.Q (-0.0256)
[INFO]   Bus_15.voltage 最敏感: Load_3.Q (-0.0213)
[INFO]   loss 最敏感: Load_1.P (0.456)
[INFO] 结果已保存: ./results/sensitivity_loads_20240324_143245_result.json
[INFO] CSV数据已保存: ./results/sensitivity_loads_20240324_143245_matrix.csv
```

### 结果文件

**JSON结果文件** (`sensitivity_loads_20240324_143245_result.json`):

```json
{
  "model": "IEEE39",
  "model_rid": "model/holdme/IEEE39",
  "timestamp": "2024-03-24T14:32:45",
  "base_case": {
    "voltage": {
      "Bus_16": 1.0234,
      "Bus_15": 1.0156
    },
    "loss": 45.3
  },
  "sensitivity_matrix": {
    "Load_1.P": {
      "Bus_16.voltage": -0.0152,
      "Bus_15.voltage": -0.0128,
      "loss": 0.456
    },
    "Load_3.P": {
      "Bus_16.voltage": -0.0189,
      "Bus_15.voltage": -0.0156,
      "loss": 0.523
    },
    "Load_3.Q": {
      "Bus_16.voltage": -0.0256,
      "Bus_15.voltage": -0.0213,
      "loss": 0.156
    },
    "Load_8.P": {
      "Bus_16.voltage": -0.0089,
      "Bus_15.voltage": -0.0076,
      "loss": 0.312
    }
  },
  "rankings": {
    "Bus_16.voltage": [
      ["Load_3.Q", -0.0256],
      ["Load_3.P", -0.0189],
      ["Load_1.P", -0.0152],
      ["Load_8.P", -0.0089]
    ],
    "loss": [
      ["Load_3.P", 0.523],
      ["Load_1.P", 0.456],
      ["Load_8.P", 0.312],
      ["Load_3.Q", 0.156]
    ]
  },
  "summary": {
    "total_parameters": 6,
    "total_metrics": 3,
    "most_sensitive_param": "Load_3.Q",
    "most_sensitive_metric": "Bus_16.voltage",
    "calculation_time": 45.2
  }
}
```

**CSV矩阵文件** (`sensitivity_loads_20240324_143245_matrix.csv`):

```csv
Parameter,Bus_16.voltage,Bus_15.voltage,loss
Load_1.P,-0.0152,-0.0128,0.456
Load_1.Q,-0.0213,-0.0189,0.123
Load_3.P,-0.0189,-0.0156,0.523
Load_3.Q,-0.0256,-0.0213,0.156
Load_8.P,-0.0089,-0.0076,0.312
Load_8.Q,-0.0123,-0.0105,0.089
```

### 后续应用

1. **关键负荷监控**: 根据灵敏度排序，重点监控Load_3的功率变化
2. **电压调节**: Load_3.Q对电压影响最大，优先调节该负荷的无功
3. **参数扫描**: 使用`param_scan`对关键参数进行更详细的扫描分析
4. **运行优化**: 制定负荷调度策略，降低关键参数变化对系统的影响

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
