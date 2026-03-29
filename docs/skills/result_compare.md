# 结果对比技能 (Result Compare)

## 设计背景

### 研究对象

在电力系统分析中，经常需要对比不同场景、不同参数配置或不同时间点的仿真结果。结果对比是评估系统变化、验证改进效果、进行灵敏度分析的核心手段。

### 实际需求

工程师在以下场景需要进行结果对比：

1. **方案评估**：对比不同运行方案下的系统性能
2. **改进验证**：验证参数调整或设备改造后的效果
3. **N-1分析**：对比故障前后的系统状态变化
4. **时序分析**：对比不同时段的系统运行特征
5. **基准测试**：将当前结果与历史基准进行对比

### 期望的输入和输出

**输入**:
- 多个仿真任务的Job ID（至少2个）
- 对比通道列表（可选，默认全部）
- 对比指标（max/min/mean/rms）
- 时间范围切片（可选）

**输出**:
- 对比报告（Markdown/JSON格式）
- 各通道的指标统计表
- 差异分析结果
- 可视化对比图表（如启用）

### 计算结果的用途和价值

结果对比数据可用于：
- 量化评估方案改进效果
- 识别系统薄弱环节
- 支持运行决策制定
- 生成技术报告
- 建立系统性能基准库

## 功能特性

- **多任务对比**：支持2个及以上仿真任务同时对比
- **智能指标计算**：自动计算最大值、最小值、平均值、有效值
- **通道级分析**：支持按通道维度进行差异对比
- **灵活输出**：Markdown报告便于阅读，JSON便于程序处理
- **时间切片**：支持指定时间范围进行局部对比

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化对比配置
python -m cloudpss_skills init result_compare --output compare.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config compare.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("result_compare")

# 配置
config = {
    "skill": "result_compare",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "sources": [
        {"job_id": "job_abc123", "label": "基准方案"},
        {"job_id": "job_def456", "label": "优化方案"}
    ],
    "compare": {
        "channels": ["Bus_16_V", "Bus_15_V", "Bus_14_V"],
        "metrics": ["max", "min", "mean"],
        "time_range": {"start": 0, "end": 10}
    },
    "output": {
        "format": "markdown",
        "path": "./results/",
        "filename": "comparison_report"
    }
}

# 运行
result = skill.run(config)
print(f"对比完成，识别到 {len(result.data.get('compared_channels', []))} 个通道差异")
```

### 3.3 YAML配置示例

```yaml
skill: result_compare
auth:
  token_file: .cloudpss_token

sources:
  - job_id: "job_abc123"
    label: "基准方案"
  - job_id: "job_def456"
    label: "优化方案"

compare:
  channels: ["Bus_16_V", "Bus_15_V", "Bus_14_V"]
  metrics: [max, min, mean, rms]
  time_range:
    start: 0
    end: 10

output:
  format: markdown
  path: ./results/
  filename: comparison_report
  timestamp: true
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: result_compare                  # 必需: 技能名称
auth:                                   # 认证配置
  token: string                        # 直接提供token（不推荐）
  token_file: string                   # token文件路径（默认: .cloudpss_token）

sources:                                # 必需: 对比源列表（至少2个）
  - job_id: string                     # 必需: 仿真任务ID
    label: string                      # 可选: 任务标签

compare:                                # 对比配置
  channels:                            # 可选: 要对比的通道列表
    - string
  metrics:                             # 可选: 指标列表
    - enum: [max, min, mean, rms]    # 默认: [max, min]
  time_range:                          # 可选: 时间范围
    start: number                      # 开始时间(s)
    end: number                      # 结束时间(s)

output:                                 # 输出配置
  format: enum                         # json | markdown（默认: markdown）
  path: string                         # 输出目录（默认: ./results/）
  filename: string                     # 文件名前缀（默认: comparison_report）
  timestamp: boolean                   # 是否添加时间戳（默认: true）
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"result_compare" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `sources` | array | 是 | - | 对比源列表，至少2个 |
| `sources[].job_id` | string | 是 | - | 仿真任务ID |
| `sources[].label` | string | 否 | job_id前8位 | 任务标签 |
| `compare.channels` | array | 否 | [] | 通道列表，空表示全部 |
| `compare.metrics` | array | 否 | [max, min] | 指标列表 |
| `compare.time_range.start` | number | 否 | - | 开始时间(s) |
| `compare.time_range.end` | number | 否 | - | 结束时间(s) |
| `output.format` | enum | 否 | markdown | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.filename` | string | 否 | comparison_report | 文件名前缀 |
| `output.timestamp` | boolean | 否 | true | 是否添加时间戳 |

## Agent使用指南

### 5.1 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("result_compare")

# 最小配置（使用默认值）
config = {
    "sources": [
        {"job_id": "job_abc123", "label": "Before"},
        {"job_id": "job_def456", "label": "After"}
    ]
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status == "SUCCESS":
        print(f"对比完成: {result.data}")
    else:
        print(f"对比失败: {result.error}")
```

### 5.2 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data
    # 访问对比结果
    compared_channels = data.get("compared_channels", 0)
    comparison = data.get("comparison", {})

    # 分析差异
    for channel, metrics in comparison.items():
        print(f"通道: {channel}")
        for metric_name, metric_data in metrics.items():
            diff = metric_data.get("diff", 0)
            if abs(diff) > 0.1:  # 显著差异阈值
                print(f"  {metric_name}: 差异显著 ({diff:.4f})")

# 访问输出文件
for artifact in result.artifacts:
    print(f"报告文件: {artifact.path}")
```

### 5.3 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    error_msg = result.error

    # 常见错误处理
    if "至少需要2个仿真任务" in error_msg:
        print("错误: 请提供至少2个Job ID进行对比")
    elif "认证失败" in error_msg:
        print("错误: 请检查token文件或token是否有效")
    elif "任务未完成" in error_msg:
        print("错误: 任务尚未完成，请等待仿真结束后再对比")
    elif "任务不存在" in error_msg:
        print("错误: 请检查Job ID是否正确")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "timestamp": "2024-03-24T14:32:01",
  "sources": [
    {"job_id": "job_abc123", "label": "基准方案"},
    {"job_id": "job_def456", "label": "优化方案"}
  ],
  "compared_channels": 3,
  "comparison": {
    "Bus_16_V": {
      "max": {
        "values": {"基准方案": 1.0523, "优化方案": 1.0489},
        "max": 1.0523,
        "min": 1.0489,
        "diff": 0.0034
      },
      "min": {
        "values": {"基准方案": 0.9477, "优化方案": 0.9512},
        "max": 0.9512,
        "min": 0.9477,
        "diff": 0.0035
      }
    }
  }
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "result_compare" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 对比结果数据字典 |
| `artifacts` | list | 输出文件列表（Artifact对象） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标（sources, channels数量） |

## 设计原理

### 工作流程

```
1. 认证与初始化
   └── 加载CloudPSS token

2. 数据获取
   └── 遍历sources列表
       └── 获取每个Job的结果
           └── 提取指定通道的波形数据

3. 指标计算
   └── 对每个通道计算指标
       ├── max: 最大值
       ├── min: 最小值
       ├── mean: 平均值
       └── rms: 有效值

4. 差异分析
   └── 对比各方案的指标值
       └── 计算差值、范围、统计

5. 报告生成
   └── 生成Markdown或JSON报告
       └── 包含对比表格和统计信息
```

## 与其他技能的关联

```
emt_simulation / power_flow / 其他仿真技能
    ↓ (仿真结果Job ID)
result_compare
    ↓ (对比报告)
visualize (可视化对比结果)
    ↓
决策支持 / 技术报告
```

**输入依赖**: 需要其他仿真技能产生的Job ID
**输出被依赖**:
- `visualize`: 可视化对比数据
- `report_generation`: 生成技术报告

## 性能特点

- **执行时间**: 取决于数据量和通道数，通常10-30秒
- **内存占用**: 与对比任务数和通道数成正比
- **并发处理**: 支持多任务并行数据获取
- **适用规模**: 已测试至10个任务、100个通道的对比

## 常见问题

### 问题1: 对比任务数不足

**原因**: 只提供了1个Job ID

**解决**:
```yaml
sources:
  - job_id: "job_abc123"
    label: "Case A"
  - job_id: "job_def456"  # 添加第二个任务
    label: "Case B"
```

### 问题2: 任务结果为空

**原因**:
- 任务尚未完成
- 任务失败
- 任务无波形数据

**解决**:
- 确认任务状态: `job.status()`
- 等待任务完成后再对比
- 检查原始仿真配置

### 问题3: 通道名不匹配

**原因**: 不同任务的通道命名不一致

**解决**:
```python
# 手动指定要对比的通道
config["compare"]["channels"] = ["Bus_16_V", "Bus_15_V"]
```

### 问题4: 内存不足

**原因**: 对比大量长时程波形数据

**解决**:
```yaml
compare:
  time_range:
    start: 0    # 只对比关键时段
    end: 10
```

### 问题5: Token认证失败

**原因**: Token文件不存在或内容错误

**解决**:
```bash
echo "your_token" > .cloudpss_token
chmod 600 .cloudpss_token
```

## 完整示例

### 场景描述

某电力公司需要对比两种运行方案下的母线电压特性，评估优化方案的效果。

### 配置文件

```yaml
skill: result_compare
auth:
  token_file: .cloudpss_token

sources:
  - job_id: "job_20240324_001"
    label: "基准运行方案"
  - job_id: "job_20240324_002"
    label: "优化运行方案"

compare:
  channels: ["Bus_16_V", "Bus_15_V", "Bus_14_V", "Bus_13_V", "Bus_12_V"]
  metrics: [max, min, mean, rms]
  time_range:
    start: 0
    end: 10

output:
  format: markdown
  path: ./results/
  filename: voltage_comparison
  timestamp: true
```

### 执行命令

```bash
python -m cloudpss_skills run --config compare_config.yaml
```

### 预期输出

```
[INFO] 加载认证信息...
[INFO] 认证成功
[INFO] 对比 2 个仿真结果
[INFO] 获取任务: 基准运行方案 (job_20240324_001)
[INFO]   -> 结果类型: EMTResult
[INFO]   -> 波形分组数: 3
[INFO]   -> 获取 5 个通道
[INFO] 获取任务: 优化运行方案 (job_20240324_002)
[INFO]   -> 结果类型: EMTResult
[INFO]   -> 波形分组数: 3
[INFO]   -> 获取 5 个通道
[INFO] 生成对比分析...
[INFO] 对比报告已保存: ./results/voltage_comparison_20240324_143245.md
```

### 结果文件

```markdown
# 仿真结果对比报告

生成时间: 2024-03-24T14:32:45

## 对比概览

- 对比任务数: 2
- 对比通道数: 5

## 任务列表

- **基准运行方案**: `job_20240324_001`
- **优化运行方案**: `job_20240324_002`

## 通道对比

### Bus_16_V

**MAX**:

| 任务 | 值 |
|------|-----|
| 基准运行方案 | 1.052300 |
| 优化运行方案 | 1.048900 |

- 范围: [1.048900, 1.052300]
- 差值: 0.003400

**MIN**:

| 任务 | 值 |
|------|-----|
| 基准运行方案 | 0.947700 |
| 优化运行方案 | 0.951200 |

- 范围: [0.947700, 0.951200]
- 差值: 0.003500
...
```

### 后续应用

1. **可视化分析**: 使用`visualize`技能生成对比图表
2. **报告生成**: 将Markdown报告转换为PDF或Word
3. **趋势追踪**: 保存对比结果，建立历史基准库
4. **决策支持**: 基于对比数据评估方案优劣

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
