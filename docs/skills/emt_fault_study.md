# EMT故障研究技能 (EMT Fault Study)

## 设计背景

### 研究对象

EMT故障研究专注于分析电力系统在故障条件下的暂态响应特性，通过对比不同故障参数下的系统行为，评估故障对电压恢复、系统稳定性的影响。本技能基于三工况对比分析方法（基线故障、延迟切除、轻故障），系统性地研究故障特性与系统响应的关系。

### 实际需求

在电力系统保护设计和运行分析中，需要回答以下问题：

1. **故障切除时间影响**：延长故障切除时间如何影响系统恢复？
2. **故障严重程度影响**：降低故障严重程度能否改善系统响应？
3. **保护整定优化**：如何选择最优的保护动作时间？
4. **电压恢复特性**：故障后电压恢复的时间和质量如何？
5. **系统脆弱性评估**：识别对故障敏感的母线和设备

### 期望的输入和输出

**输入**：

- 电力系统模型（需配置EMT拓扑和故障元件）
- 故障工况配置（基线、延迟切除、轻故障）
- 时间窗口定义（故障前、故障中、故障后、恢复期）
- 电压通道名称和采样频率
- 分析参数（RMS计算窗口等）

**输出**：

- 各工况的RMS电压指标
- 故障跌落和恢复缺口量化
- 工况对比分析结果
- 波形对比数据
- 研究报告（Markdown格式）

### 计算结果的用途和价值

故障研究结果可用于：

- **保护整定**：确定最优故障切除时间
- **风险评估**：量化不同故障 severity 的影响
- **运行指导**：制定故障处理策略
- **规划设计**：评估系统对故障的承受能力

## 功能特性

- **三工况对比分析**：自动执行基线、延迟切除、轻故障三种工况
- **RMS指标计算**：故障前、故障中、故障后、恢复期的RMS电压
- **量化对比**：计算故障跌落、恢复缺口、相对基线变化
- **波形导出**：导出各工况的时域波形对比数据
- **研究报告生成**：自动生成Markdown格式的分析报告
- **灵活工况配置**：支持自定义故障时间和故障电阻
- **时间窗口自定义**：可配置分析的时间窗口

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init emt_fault_study --output fault_study.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config fault_study.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("emt_fault_study")

# 配置
config = {
    "skill": "emt_fault_study",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE3", "source": "cloud"},
    "scenarios": {
        "baseline": {
            "enabled": True,
            "fs": 2.5,
            "fe": 2.7,
            "chg": 0.01,
            "description": "基线故障"
        },
        "delayed_clearing": {
            "enabled": True,
            "fs": 2.5,
            "fe": 2.9,
            "chg": 0.01,
            "description": "延长故障切除"
        },
        "mild_fault": {
            "enabled": True,
            "fs": 2.5,
            "fe": 2.7,
            "chg": 1e4,
            "description": "较轻故障"
        }
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "fault_study",
        "export_waveforms": True,
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
print(f"工况数: {result.metrics.get('scenarios', 0)}")
```

### 3.3 YAML配置示例

```yaml
skill: emt_fault_study
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

scenarios:
  baseline:
    enabled: true
    fs: 2.5                 # 故障开始时间(s)
    fe: 2.7                 # 故障结束时间(s)
    chg: 0.01               # 故障电阻(Ω)
    description: "基线故障"
  delayed_clearing:
    enabled: true
    fs: 2.5
    fe: 2.9                 # 延长故障切除时间
    chg: 0.01
    description: "延长故障切除"
  mild_fault:
    enabled: true
    fs: 2.5
    fe: 2.7
    chg: 1e4                # 增大故障电阻，降低严重程度
    description: "较轻故障"

analysis:
  trace_name: "vac:0"       # 电压通道trace名称
  voltage_channel_name: "vac"  # 电压通道名称
  sampling_freq: 2000       # 采样频率(Hz)
  time_windows:
    prefault: [2.42, 2.44]      # 故障前窗口
    fault: [2.56, 2.58]         # 故障中窗口
    postfault: [2.92, 2.94]     # 故障后窗口
    late_recovery: [2.96, 2.98] # 恢复期窗口

output:
  format: json
  path: ./results/
  prefix: emt_fault_study
  export_waveforms: true    # 导出波形对比
  waveform_window: [2.0, 3.5]  # 波形导出时间范围
  generate_report: true     # 生成研究报告
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: emt_fault_study                 # 必需: 技能名称
auth:                                  # 认证配置
  token: string
  token_file: string                  # 默认: .cloudpss_token

model:                                 # 模型配置（必需）
  rid: string                         # 模型RID或本地路径
  source: enum                        # cloud | local

scenarios:                             # 工况配置
  baseline:                           # 基线工况
    enabled: boolean                  # 是否启用
    fs: number                        # 故障开始时间(s)
    fe: number                        # 故障结束时间(s)
    chg: number                       # 故障电阻(Ω)
    description: string               # 工况描述
  delayed_clearing:                   # 延迟切除工况
    enabled: boolean
    fs: number
    fe: number
    chg: number
    description: string
  mild_fault:                         # 轻故障工况
    enabled: boolean
    fs: number
    fe: number
    chg: number
    description: string

analysis:                              # 分析配置
  trace_name: string                  # trace名称
  voltage_channel_name: string        # 电压通道名称
  sampling_freq: integer              # 采样频率(Hz)
  time_windows:                       # 时间窗口
    prefault: array                   # 故障前窗口[s]
    fault: array                      # 故障中窗口[s]
    postfault: array                  # 故障后窗口[s]
    late_recovery: array              # 恢复期窗口[s]

output:                                # 输出配置
  format: enum                        # json | csv
  path: string
  prefix: string
  export_waveforms: boolean           # 是否导出波形
  waveform_window: array              # 波形时间范围
  generate_report: boolean            # 是否生成报告
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"emt_fault_study" |
| `auth.token` | string | 否 | - | API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地路径 |
| `model.source` | enum | 否 | cloud | cloud/local |
| `scenarios.baseline.enabled` | boolean | 否 | true | 启用基线工况 |
| `scenarios.baseline.fs` | number | 否 | 2.5 | 故障开始时间(s) |
| `scenarios.baseline.fe` | number | 否 | 2.7 | 故障结束时间(s) |
| `scenarios.baseline.chg` | number | 否 | 0.01 | 故障电阻(Ω) |
| `scenarios.baseline.description` | string | 否 | "基线故障" | 工况描述 |
| `scenarios.delayed_clearing.*` | - | - | - | 同上，fe默认2.9 |
| `scenarios.mild_fault.*` | - | - | - | 同上，chg默认1e4 |
| `analysis.trace_name` | string | 否 | "vac:0" | trace名称 |
| `analysis.sampling_freq` | integer | 否 | 2000 | 采样频率(Hz) |
| `analysis.time_windows.prefault` | array | 否 | [2.42, 2.44] | 故障前窗口 |
| `analysis.time_windows.fault` | array | 否 | [2.56, 2.58] | 故障中窗口 |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.export_waveforms` | boolean | 否 | true | 导出波形 |
| `output.generate_report` | boolean | 否 | true | 生成报告 |

## Agent使用指南

### 5.1 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("emt_fault_study")

# 配置（使用默认工况）
config = {
    "model": {"rid": "model/holdme/IEEE3"}
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status.value == "SUCCESS":
        data = result.data
        print(f"工况数: {len(data['scenarios'])}")
        for scenario in data['scenarios']:
            print(f"  {scenario['scenario']}: RMS={scenario['fault_rms']}")
    else:
        print(f"失败: {result.error}")
```

### 5.2 处理结果

```python
result = skill.run(config)

if result.status.value == "SUCCESS":
    data = result.data

    # 访问汇总数据
    print(f"模型: {data['model_name']}")
    print(f"时间: {data['timestamp']}")

    # 遍历各工况结果
    for scenario in data['scenarios']:
        print(f"\n工况: {scenario['scenario']}")
        print(f"  描述: {scenario['description']}")
        print(f"  故障前RMS: {scenario['prefault_rms']}")
        print(f"  故障RMS: {scenario['fault_rms']}")
        print(f"  故障后RMS: {scenario['postfault_rms']}")
        print(f"  故障跌落: {scenario['fault_drop_vs_prefault']}")
        print(f"  恢复缺口: {scenario['postfault_gap_vs_prefault']}")
        print(f"  观察结论: {scenario['observation']}")

    # 访问研究结论
    summary = data['summary']
    print(f"\n研究问题: {summary['research_question']}")
    for finding in summary['findings']:
        print(f"  发现: {finding['title']}")
        print(f"    支持: {'是' if finding['supported'] else '否'}")
        print(f"    证据: {finding['evidence']}")

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
    elif "未找到故障元件" in error_msg:
        print("错误: 模型未配置故障元件，请先运行ieee3_prep")
    elif "未找到电压量测通道" in error_msg:
        print("错误: 模型未配置电压量测通道")
    elif "未找到EMT任务" in error_msg:
        print("错误: 模型未配置EMT任务")
    elif "EMT仿真失败" in error_msg:
        print("错误: EMT仿真失败，请检查故障参数")
    elif "至少需要一个启用的工况" in error_msg:
        print("错误: 请至少启用一个工况")
    else:
        print(f"错误: {error_msg}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "model_name": "IEEE3",
  "model_rid": "model/holdme/IEEE3",
  "timestamp": "2024-03-24T14:32:01",
  "scenarios": [
    {
      "scenario": "baseline",
      "description": "基线故障",
      "fault_end_time": "2.7",
      "fault_chg": "0.01",
      "point_count": "50000",
      "prefault_rms": "0.999",
      "fault_rms": "0.234",
      "postfault_rms": "0.987",
      "late_recovery_rms": "0.998",
      "fault_drop_vs_prefault": "0.765",
      "postfault_gap_vs_prefault": "0.012",
      "delta_fault_rms_vs_baseline": "0.000",
      "observation": "reference"
    }
  ],
  "summary": {
    "research_question": "在同一故障模型上，延迟切除与降低故障严重度如何影响故障深度和恢复缺口？",
    "findings": [
      {
        "title": "延迟切除主要恶化故障后恢复，而不是改变故障深度",
        "supported": true,
        "evidence": "..."
      }
    ]
  }
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "emt_fault_study" |
| `status` | SkillStatus | SUCCESS / FAILED |
| `data` | dict | 包含model_name、scenarios、summary等 |
| `artifacts` | list | JSON汇总、CSV汇总、波形数据、报告 |
| `metrics` | dict | scenarios数、成功工况数 |

## 设计原理

### 工作流程

```
1. 加载认证 → 设置CloudPSS Token
2. 获取模型 → 加载IEEE3等EMT模型
3. 准备工况 → 配置三种故障工况参数
4. 循环执行 → 对每个工况：
   a. 准备模型（更新故障参数）
   b. 运行EMT仿真
   c. 等待完成
   d. 提取指标（RMS计算）
5. 汇总分析 → 计算对比指标和结论
6. 导出结果 → JSON、CSV、波形、报告
```

### 三工况对比逻辑

| 工况 | 故障电阻 | 故障切除时间 | 研究目的 |
|------|----------|--------------|----------|
| 基线 | 0.01Ω | 0.2s | 标准参考 |
| 延迟切除 | 0.01Ω | 0.4s | 评估切除时间影响 |
| 轻故障 | 1e4Ω | 0.2s | 评估故障severity影响 |

### RMS计算

在每个时间窗口内计算电压的RMS值：

```
RMS = sqrt(sum(v^2) / n)
```

窗口定义：
- **故障前(prefault)**: 故障前的稳态电压
- **故障中(fault)**: 故障期间的最低电压
- **故障后(postfault)**: 故障切除后的电压
- **恢复期(late_recovery)**: 系统恢复后的电压

## 与其他技能的关联

```
ieee3_prep
    ↓ (准备EMT模型)
emt_simulation
    ↓ (基础EMT仿真)
emt_fault_study
    ↓ (三工况对比)
visualize → waveform_export → disturbance_severity
    ↓
fault_clearing_scan / fault_severity_scan
```

### 依赖关系

- **前置依赖**: `ieee3_prep`（准备EMT模型）
- **相关技能**:
  - `emt_simulation`: 基础EMT仿真
  - `fault_clearing_scan`: 故障切除时间扫描
  - `fault_severity_scan`: 故障严重程度扫描
  - `visualize`: 波形可视化
  - `waveform_export`: 波形导出

## 性能特点

- **执行时间**: IEEE3系统约5-15分钟（3个工况）
- **内存占用**: 与模型规模和工况数成正比
- **输出大小**: 波形文件可能较大（每个工况10-50MB）
- **建议**: 首次运行先用单个工况测试

## 常见问题

### 问题1: 未找到故障元件

**原因**: 模型未配置故障电阻元件

**解决**:
```bash
# 运行ieee3_prep准备模型
python -m cloudpss_skills run --config config/ieee3_prep.yaml
```

### 问题2: 未找到电压量测通道

**原因**: 模型未配置电压测量通道

**解决**: 检查模型配置，确保包含`_newChannel`类型的电压通道组件

### 问题3: 仿真失败

**原因**: 故障参数不合理或模型配置错误

**解决**:
- 检查故障时间是否在仿真时长范围内
- 检查故障电阻值是否合理（chg: 0.01-1e4）
- 确认模型已正确配置EMT拓扑

### 问题4: 指标计算异常

**原因**: 时间窗口设置不当或数据缺失

**解决**: 调整`time_windows`配置，确保窗口在仿真时间范围内且有足够数据点

## 完整示例

### 场景描述

某电网公司需要评估IEEE3系统在故障条件下的电压恢复特性，对比标准故障、延迟切除、轻故障三种工况的系统响应。

### 配置文件

```yaml
skill: emt_fault_study
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

scenarios:
  baseline:
    enabled: true
    fs: 2.5
    fe: 2.7
    chg: 0.01
    description: "基线: fe=2.7, chg=0.01"
  delayed_clearing:
    enabled: true
    fs: 2.5
    fe: 2.9
    chg: 0.01
    description: "延迟切除: fe=2.9, chg=0.01"
  mild_fault:
    enabled: true
    fs: 2.5
    fe: 2.7
    chg: 1e4
    description: "轻故障: fe=2.7, chg=1e4"

analysis:
  trace_name: "vac:0"
  voltage_channel_name: "vac"
  sampling_freq: 2000
  time_windows:
    prefault: [2.42, 2.44]
    fault: [2.56, 2.58]
    postfault: [2.92, 2.94]
    late_recovery: [2.96, 2.98]

output:
  format: json
  path: ./results/
  prefix: emt_fault_study
  export_waveforms: true
  waveform_window: [2.0, 3.5]
  generate_report: true
```

### 执行命令

```bash
python -m cloudpss_skills run --config emt_fault_study.yaml
```

### 预期输出

```
[INFO] 加载认证信息...
[INFO] 认证成功
[INFO] 获取模型...
[INFO] 模型: IEEE3 (model/holdme/IEEE3)
[INFO] 将执行 3 个工况的仿真
[INFO] [1/3] 工况: baseline - 基线: fe=2.7, chg=0.01
[INFO]   故障参数: fs=2.5, fe=2.7, chg=0.01
[INFO]   Job ID: job_xxx
[INFO]   仿真完成
[INFO]   完成: 点数=50000, 故障前RMS=0.999, 故障RMS=0.234, 故障后RMS=0.987
[INFO] [2/3] 工况: delayed_clearing - 延迟切除: fe=2.9, chg=0.01
...
[INFO] [3/3] 工况: mild_fault - 轻故障: fe=2.7, chg=1e4
...
[INFO] 生成结果汇总...
[INFO] JSON结果: results/emt_fault_study_20240324_143245.json
[INFO] CSV结果: results/emt_fault_study_20240324_143245.csv
[INFO] 波形数据: results/emt_fault_study_waveforms_20240324_143245.csv
[INFO] 研究报告: results/emt_fault_study_report_20240324_143245.md
```

### 结果文件

CSV汇总文件格式：

```csv
scenario,description,fault_end_time,fault_chg,point_count,prefault_rms,fault_rms,postfault_rms,late_recovery_rms,fault_drop_vs_prefault,postfault_gap_vs_prefault,observation
baseline,基线: fe=2.7 chg=0.01,2.7,0.01,50000,0.999,0.234,0.987,0.998,0.765,0.012,reference
delayed_clearing,延迟切除: fe=2.9 chg=0.01,2.9,0.01,50000,0.999,0.235,0.950,0.995,0.764,0.049,same fault depth weaker post-fault recovery
mild_fault,轻故障: fe=2.7 chg=1e4,2.7,10000.0,50000,0.999,0.856,0.998,0.999,0.143,0.001,shallower sag stronger post-fault recovery
```

研究报告示例：

```markdown
# EMT 故障研究分析报告

## 研究概述

本研究对比分析三种故障工况对系统电压恢复的影响：
- **基线故障**: 标准故障参数
- **延迟切除**: 延长故障切除时间
- **轻故障**: 降低故障严重程度

## 关键发现

### 延迟切除主要恶化故障后恢复，而不是改变故障深度
**结论**: ✓ 支持
**证据**: delta_fault_rms=0.001, post_gap: 0.012 -> 0.049

### 较轻故障显著减小故障跌落，并把恢复缺口压回接近零
**结论**: ✓ 支持
**证据**: fault_drop: 0.765 -> 0.143, post_gap: 0.012 -> 0.001
```

### 后续应用

1. **可视化分析**: 使用波形对比数据绘制各工况电压曲线
2. **保护整定**: 根据故障研究结果优化保护动作时间
3. **风险评估**: 评估系统对不同故障 severity 的承受能力
4. **参数扫描**: 使用`fault_clearing_scan`进行更精细的参数扫描

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
