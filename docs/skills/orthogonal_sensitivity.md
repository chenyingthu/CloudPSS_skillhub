# 正交敏感性分析技能 (Orthogonal Sensitivity Analysis)

## 设计背景

### 研究对象
正交敏感性分析技能基于正交实验设计（OAT, Orthogonal Array Testing）方法，用于高效识别电力系统模型中的关键参数。通过科学的实验设计，可以用较少的仿真次数评估多参数的敏感性。

### 实际需求
在电力系统分析中，经常需要：
1. **关键参数识别**：找出对系统影响最大的参数
2. **多因素分析**：同时分析多个参数的交互影响
3. **优化实验设计**：减少仿真次数，提高效率
4. **参数排序**：量化各参数对指标的影响程度
5. **敏感性量化**：计算各参数的效应值和贡献率

### 期望的输入和输出

**输入**：
- 模型配置（RID和来源）
- 要分析的参数列表（2-7个参数，2-4个水平）
- 评估指标（电压、功率、频率或自定义）
- 正交表类型（L4、L8、L9、L16）
- 仿真类型（潮流或EMT）

**输出**：
- 各参数的效应值和敏感性排序
- 贡献率分析
- 正交实验设计表
- 各次运行的结果
- JSON/CSV格式的分析报告

### 计算结果的用途和价值
正交敏感性分析结果可用于：
- 识别关键影响因素
- 参数优化设计
- 模型简化和降阶
- 不确定性量化
- 控制策略设计

## 功能特性

- **正交实验设计**：支持L4(2³)、L8(2⁷)、L9(3⁴)、L16(4⁵)正交表
- **多参数分析**：支持2-7个参数，2-4个水平
- **自动表选择**：可根据参数数量和水平自动选择合适正交表
- **效应值计算**：计算各参数对指标的影响程度
- **贡献率分析**：量化各参数的贡献比例
- **多指标支持**：支持电压、功率、频率和自定义指标
- **可视化准备**：生成可用于可视化的数据结构

## 快速开始

### CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init orthogonal_sensitivity --output oat_sensitivity.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config oat_sensitivity.yaml
```

### Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("orthogonal_sensitivity")

# 配置
config = {
    "skill": "orthogonal_sensitivity",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "parameters": [                   # 要分析的参数
        {"name": "Gen1.pf_P", "levels": [0.8, 1.0, 1.2]},
        {"name": "Gen2.pf_P", "levels": [0.8, 1.0, 1.2]},
        {"name": "Gen1.pf_V", "levels": [0.95, 1.0, 1.05]}
    ],
    "target": {                       # 评估指标
        "metric": "voltage",
        "bus_name": "Bus_1"
    },
    "design": {                       # 实验设计
        "table_type": "auto",         # auto | L4_2_3 | L8_2_7 | L9_3_4 | L16_4_5
        "simulation_type": "power_flow"
    },
    "execution": {
        "timeout": 300.0,
        "continue_on_error": True
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "oat_sensitivity"
    }
}

# 运行
result = skill.run(config)
print(f"状态: {result.status}")
print(f"正交运行次数: {result.data.get('runs_count')}")
```

### YAML配置示例

```yaml
skill: orthogonal_sensitivity
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

parameters:
  - name: Gen1.pf_P
    levels: [0.8, 1.0, 1.2]
  - name: Gen2.pf_P
    levels: [0.8, 1.0, 1.2]
  - name: Gen3.pf_P
    levels: [0.8, 1.0, 1.2]
  - name: Gen1.pf_V
    levels: [0.95, 1.0, 1.05]

target:
  metric: voltage
  bus_name: Bus_16

design:
  table_type: auto
  simulation_type: power_flow

execution:
  timeout: 300.0
  continue_on_error: true

output:
  format: json
  path: ./results/
  prefix: oat_sensitivity
```

## 配置Schema

### 完整配置结构

```yaml
skill: orthogonal_sensitivity         # 必需: 技能名称
auth:                              # 认证配置
  token: string                    # 直接提供token（不推荐）
  token_file: string               # token文件路径（默认: .cloudpss_token）

model:                             # 模型配置
  rid: string                      # 模型RID（必需）
  source: enum                     # cloud | local（默认: cloud）
  job_name: string                 # 指定job名称

parameters:                        # 参数列表（必需）
  - name: string                   # 参数名称（必需）
    levels: array                  # 水平值列表，2-4个（必需）
    component_rid: string          # 元件RID筛选（可选）

target:                            # 评估指标（必需）
  metric: enum                     # voltage | power | frequency | custom
  bus_name: string                 # 监测母线名称
  component_name: string           # 监测元件名称
  custom_expression: string        # 自定义指标表达式

design:                            # 实验设计配置
  table_type: enum                 # auto | L4_2_3 | L8_2_7 | L9_3_4 | L16_4_5
  simulation_type: enum            # power_flow | emt

execution:                         # 执行配置
  timeout: number                  # 单次仿真超时(s)（默认: 300.0）
  continue_on_error: boolean       # 出错继续（默认: true）

output:                            # 输出配置
  format: enum                     # json | csv（默认: json）
  path: string                     # 输出目录（默认: ./results/）
  prefix: string                   # 文件名前缀（默认: orthogonal_sensitivity）
```

### 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"orthogonal_sensitivity" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源 |
| `model.job_name` | string | 否 | - | 指定job名称 |
| `parameters` | array | 是 | - | 要分析的参数列表（最多7个） |
| `parameters[].name` | string | 是 | - | 参数名称（如Gen1.pf_P） |
| `parameters[].levels` | array | 是 | - | 水平值列表（2-4个） |
| `parameters[].component_rid` | string | 否 | - | 元件RID筛选 |
| `target.metric` | enum | 是 | - | 评估指标类型 |
| `target.bus_name` | string | 否 | - | 监测母线名称 |
| `target.component_name` | string | 否 | - | 监测元件名称 |
| `target.custom_expression` | string | 否 | - | 自定义指标表达式 |
| `design.table_type` | enum | 否 | auto | 正交表类型 |
| `design.simulation_type` | enum | 否 | power_flow | 仿真类型 |
| `execution.timeout` | number | 否 | 300.0 | 单次仿真超时(s) |
| `execution.continue_on_error` | boolean | 否 | true | 出错是否继续 |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | orthogonal_sensitivity | 文件名前缀 |

### 正交表类型说明

| 表类型 | 参数数 | 水平数 | 运行次数 | 适用场景 |
|--------|--------|--------|----------|----------|
| `L4_2_3` | 3 | 2 | 4 | 少量参数，2水平 |
| `L8_2_7` | 7 | 2 | 8 | 多参数，2水平 |
| `L9_3_4` | 4 | 3 | 9 | 中等参数，3水平 |
| `L16_4_5` | 5 | 4 | 16 | 多水平分析 |
| `auto` | - | - | - | 自动选择最优表 |

**auto选择逻辑**：
- 参数≤3且水平=2 → 选择L4_2_3
- 参数≤4且水平=3 → 选择L9_3_4
- 参数≤5且水平=4 → 选择L16_4_5
- 其他情况 → 选择L8_2_7（默认）

### 评估指标说明

| 指标类型 | 说明 | 需要指定 |
|----------|------|----------|
| `voltage` | 母线电压 | bus_name |
| `power` | 元件功率 | component_name |
| `frequency` | 系统频率 | - |
| `custom` | 自定义指标 | custom_expression |

## Agent使用指南

### 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("orthogonal_sensitivity")

# 配置
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "parameters": [
        {"name": "Gen1.pf_P", "levels": [0.8, 1.0, 1.2]},
        {"name": "Gen2.pf_P", "levels": [0.8, 1.0, 1.2]},
    ],
    "target": {
        "metric": "voltage",
        "bus_name": "Bus_16"
    },
    "design": {
        "table_type": "auto"
    }
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status.value == "SUCCESS":
        print(f"正交分析完成: {result.data['runs_count']} 次运行")
    else:
        print(f"正交分析失败: {result.error}")
```

### 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data

    # 访问汇总统计
    print(f"正交表: {data['orthogonal_table']}")
    print(f"运行次数: {data['runs_count']}")
    print(f"参数数量: {data['parameter_count']}")

    # 访问敏感性结果
    print("\n敏感性排序:")
    for sr in data.get('sensitivity_results', []):
        print(f"  {sr['parameter']}: 效应值={sr['effect_value']:.4f}, "
              f"贡献率={sr['contribution_ratio']*100:.2f}%")

    # 访问正交实验表
    print("\n正交实验表:")
    for run in data.get('runs', []):
        print(f"  运行{run['run_id']}: {run['parameter_values']} -> {run['result']}")

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
    elif "参数数量不能超过7个" in error_msg:
        print("错误: 正交分析最多支持7个参数")
    elif "水平数不能超过4个" in error_msg:
        print("错误: 每个参数最多4个水平")
    elif "必须指定target.metric" in error_msg:
        print("错误: 请指定评估指标")
    else:
        print(f"未知错误: {error_msg}")

# 处理部分失败情况
if result.status.value == "SUCCESS" and result.data.get("failed_runs", 0) > 0:
    print(f"警告: {result.data['failed_runs']} 次运行失败")
```

## 输出结果

### JSON输出格式

```json
{
  "orthogonal_table": "L9_3_4",
  "runs_count": 9,
  "parameter_count": 3,
  "target_metric": "voltage",
  "sensitivity_results": [
    {
      "parameter": "Gen1.pf_P",
      "effect_value": 0.0523,
      "sensitivity_rank": 1,
      "contribution_ratio": 0.45
    },
    {
      "parameter": "Gen2.pf_P",
      "effect_value": 0.0341,
      "sensitivity_rank": 2,
      "contribution_ratio": 0.32
    },
    {
      "parameter": "Gen1.pf_V",
      "effect_value": 0.0189,
      "sensitivity_rank": 3,
      "contribution_ratio": 0.23
    }
  ],
  "runs": [
    {
      "run_id": 1,
      "parameter_values": {
        "Gen1.pf_P": 0.8,
        "Gen2.pf_P": 0.8,
        "Gen1.pf_V": 0.95
      },
      "status": "completed",
      "result": 1.0234
    }
  ],
  "orthogonal_array": [
    [1, 1, 1, 1],
    [1, 2, 2, 2],
    [1, 3, 3, 3],
    [2, 1, 2, 3],
    [2, 2, 3, 1],
    [2, 3, 1, 2],
    [3, 1, 3, 2],
    [3, 2, 1, 3],
    [3, 3, 2, 1]
  ],
  "parameter_names": ["Gen1.pf_P", "Gen2.pf_P", "Gen1.pf_V"],
  "level_values": {
    "Gen1.pf_P": [0.8, 1.0, 1.2],
    "Gen2.pf_P": [0.8, 1.0, 1.2],
    "Gen1.pf_V": [0.95, 1.0, 1.05]
  }
}
```

### CSV报告格式

**敏感性分析结果**:
```csv
parameter,effect_value,sensitivity_rank,contribution_ratio
Gen1.pf_P,0.0523,1,0.45
Gen2.pf_P,0.0341,2,0.32
Gen1.pf_V,0.0189,3,0.23
```

**正交实验运行结果**:
```csv
run_id,Gen1.pf_P,Gen2.pf_P,Gen1.pf_V,result,status
1,0.8,0.8,0.95,1.0234,completed
2,0.8,1.0,1.00,1.0256,completed
3,0.8,1.2,1.05,1.0289,completed
...
```

### SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "orthogonal_sensitivity" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典，包含敏感性分析和运行结果 |
| `artifacts` | list | 输出文件列表（JSON、CSV） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |

## 设计原理

### 正交实验设计原理

正交表是一种科学的实验设计方法，具有**均衡分散**和**整齐可比**的特点：

1. **均衡分散**：实验点在实验范围内均匀分布
2. **整齐可比**：每个因素的各水平出现次数相同，各因素间搭配均匀

### 工作流程

```
1. 配置加载与验证
   └── 验证参数数量（2-7个）
   └── 验证水平数（2-4个）
   └── 验证目标指标

2. 选择正交表
   └── 根据参数数和水平数选择合适正交表
   └── 或使用auto模式自动选择

3. 生成实验方案
   └── 根据正交表生成参数组合
   └── 每个组合对应一次仿真运行

4. 批量仿真
   └── 按正交表顺序执行仿真
   └── 记录每次运行的指标值

5. 计算效应值
   └── 对每个参数，计算各水平的平均指标值
   └── 计算效应值（最大-最小）

6. 排序和贡献率
   └── 按效应值排序
   └── 计算贡献率

7. 生成报告
   └── 输出敏感性排序
   └── 输出正交实验表
```

### 效应值计算方法

对于每个参数，计算各水平下的平均指标值：

```
K_i = 第i水平下所有运行的指标平均值
Effect = max(K_i) - min(K_i)
```

效应值越大，说明该参数对指标的影响越大。

### 贡献率计算方法

```
Contribution = Effect / sum(所有参数的Effect)
```

贡献率表示该参数对总变异的贡献比例。

## 与其他技能的关联

```
model_parameter_extractor (模型参数提取)
    ↓ (获取模型参数)
orthogonal_sensitivity (正交敏感性分析)
    ↓ (识别关键参数)
param_scan (参数扫描) / config_batch_runner (批量运行)
    ↓ (针对关键参数深入分析)
result_compare (结果对比) / visualize (可视化)
```

**依赖关系**：
- **输入依赖**：
  - `model_parameter_extractor`: 获取参数列表和范围
- **输出被依赖**：
  - `param_scan`: 针对关键参数进行详细扫描
  - `config_batch_runner`: 基于关键参数设计批量运行
  - `visualize`: 可视化敏感性分析结果

**典型工作流**：
1. 使用 `model_parameter_extractor` 提取模型参数
2. 使用 `orthogonal_sensitivity` 识别关键参数
3. 针对关键参数使用 `param_scan` 进行详细分析
4. 使用 `visualize` 生成敏感性可视化报告

## 性能特点

- **执行方式**：批量串行仿真
- **仿真次数**：4-16次（取决于正交表）
- **时间开销**：仿真次数 × 单次仿真时间
- **计算效率**：比全因子实验大幅减少仿真次数
  - 3参数3水平：全因子需27次，正交仅需9次
  - 4参数3水平：全因子需81次，正交仅需9次
- **精度**：可识别主要影响因素，但无法分析交互作用

## 常见问题

### 问题1: 参数数量超过限制

**原因**：正交表最多支持7个参数（L8_2_7）

**解决**：
```python
# 选择最关键的7个参数进行分析
config["parameters"] = [
    {"name": "Gen1.pf_P", "levels": [0.8, 1.0, 1.2]},
    {"name": "Gen2.pf_P", "levels": [0.8, 1.0, 1.2]},
    # ... 最多7个
]

# 或使用两阶段分析
# 第一阶段：筛选最重要的7个
# 第二阶段：针对这7个进行详细分析
```

### 问题2: 参数水平数不一致

**原因**：不同参数的水平数不同

**解决**：
```python
# 正交表要求所有参数水平数相同
# 需要统一为2、3或4个水平

# 对于2水平参数
config["parameters"] = [
    {"name": "Gen1.pf_P", "levels": [0.8, 1.2]},  # 2水平
    {"name": "Gen2.pf_P", "levels": [0.8, 1.2]},  # 2水平
]
config["design"]["table_type"] = "L8_2_7"  # 选择2水平正交表
```

### 问题3: 某些运行失败

**原因**：
- 参数组合导致模型不收敛
- 仿真超时
- 网络问题

**解决**：
```yaml
execution:
  continue_on_error: true    # 继续执行其他运行
  timeout: 600.0            # 增加超时时间
```

### 问题4: 效应值差异不明显

**原因**：
- 参数范围设置不合理
- 参数对指标本身影响较小
- 水平数太少

**解决**：
```python
# 扩大参数变化范围
config["parameters"] = [
    {"name": "Gen1.pf_P", "levels": [0.5, 1.0, 1.5]},  # 更大范围
]

# 增加水平数
config["parameters"] = [
    {"name": "Gen1.pf_P", "levels": [0.8, 0.9, 1.0, 1.1, 1.2]},  # 5水平
]
```

## 完整示例

### 场景描述
某电力系统分析部门需要识别IEEE39模型中对Bus16母线电压影响最大的发电机参数，以便后续进行参数优化。

### 配置文件

```yaml
skill: orthogonal_sensitivity
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

parameters:
  - name: Gen1.pf_P
    levels: [0.8, 1.0, 1.2]
  - name: Gen2.pf_P
    levels: [0.8, 1.0, 1.2]
  - name: Gen3.pf_P
    levels: [0.8, 1.0, 1.2]
  - name: Gen1.pf_V
    levels: [0.95, 1.0, 1.05]

target:
  metric: voltage
  bus_name: Bus_16

design:
  table_type: auto
  simulation_type: power_flow

execution:
  timeout: 300.0
  continue_on_error: true

output:
  format: json
  path: ./results/
  prefix: gen_sensitivity
```

### 执行命令

```bash
# 创建输出目录
mkdir -p ./results

# 执行正交敏感性分析
python -m cloudpss_skills run --config oat_sensitivity.yaml
```

### 预期输出

```
[INFO] 正交敏感性分析开始
[INFO] 加载模型: model/holdme/IEEE39
[INFO] 自动选择正交表: L9_3_4 (4个参数, 3个水平, 9次运行)
[INFO] 开始正交实验运行...
[INFO] 运行 1/9: Gen1.pf_P=0.8, Gen2.pf_P=0.8, Gen3.pf_P=0.8, Gen1.pf_V=0.95
[INFO] 运行 2/9: Gen1.pf_P=0.8, Gen2.pf_P=1.0, Gen3.pf_P=1.0, Gen1.pf_V=1.00
...
[INFO] 运行 9/9: Gen1.pf_P=1.2, Gen2.pf_P=1.2, Gen3.pf_P=1.0, Gen1.pf_V=1.00
[INFO] 计算效应值...
[INFO] 敏感性排序:
  1. Gen1.pf_P: 效应值=0.0523, 贡献率=45.0%
  2. Gen2.pf_P: 效应值=0.0341, 贡献率=32.0%
  3. Gen3.pf_P: 效应值=0.0189, 贡献率=18.0%
  4. Gen1.pf_V: 效应值=0.0056, 贡献率=5.0%
[INFO] 正交敏感性分析完成，共9次运行
[INFO] 结果已保存: ./results/gen_sensitivity_result.json
```

### 结果文件

**JSON结果** (`gen_sensitivity_result.json`):
```json
{
  "orthogonal_table": "L9_3_4",
  "runs_count": 9,
  "parameter_count": 4,
  "target_metric": "voltage",
  "target_bus": "Bus_16",
  "sensitivity_results": [
    {
      "parameter": "Gen1.pf_P",
      "effect_value": 0.0523,
      "sensitivity_rank": 1,
      "contribution_ratio": 0.45
    },
    {
      "parameter": "Gen2.pf_P",
      "effect_value": 0.0341,
      "sensitivity_rank": 2,
      "contribution_ratio": 0.32
    },
    {
      "parameter": "Gen3.pf_P",
      "effect_value": 0.0189,
      "sensitivity_rank": 3,
      "contribution_ratio": 0.18
    },
    {
      "parameter": "Gen1.pf_V",
      "effect_value": 0.0056,
      "sensitivity_rank": 4,
      "contribution_ratio": 0.05
    }
  ],
  "runs": [...],
  "orthogonal_array": [...]
}
```

### 后续应用

基于敏感性分析结果，可以：
1. 重点优化Gen1.pf_P和Gen2.pf_P参数（贡献率77%）
2. 使用 `param_scan` 对这两个参数进行详细扫描
3. 使用 `config_batch_runner` 测试不同参数组合
4. 生成参数优化建议报告

**关键结论**：Gen1的有功功率设定值对Bus16母线电压影响最大（贡献率45%），其次是Gen2的有功功率（32%）。建议重点调整这两个参数来优化电压水平。

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
- **参考实现**: 谭镇东 OAT.py 正交表实现
