# 波形导出技能 (Waveform Export)

## 设计背景

### 研究对象

电力系统电磁暂态（EMT）仿真产生大量时序波形数据，包括母线电压、支路电流、发电机功角、功率等。这些数据是分析系统动态行为、验证保护配置、评估设备性能的重要依据。

### 实际需求

工程师在以下场景需要导出波形数据：

1. **离线分析**：将数据导出到MATLAB、Python等工具进行深度分析
2. **报告制作**：提取特定时段数据制作报告
3. **数据存档**：长期保存仿真结果
4. **对比验证**：与其他软件或实测数据对比
5. **批量处理**：自动化处理大量仿真结果

### 期望的输入和输出

**输入**:
- 仿真任务Job ID
- 波形分组索引（可选）
- 通道筛选列表（可选）
- 时间范围切片（可选）

**输出**:
- CSV或JSON格式的波形数据文件
- 包含时间序列和各通道数值
- 执行日志和元数据

### 计算结果的用途和价值

导出数据可用于：
- 在MATLAB/Python中进行自定义分析
- 与其他仿真软件结果对比
- 制作Excel报告和图表
- 长期数据存档和版本管理
- 机器学习训练数据准备

## 功能特性

- **任务ID导入**：通过Job ID直接获取云端仿真结果
- **灵活筛选**：支持按分组、通道、时间范围筛选
- **双格式输出**：CSV适合表格分析，JSON适合程序处理
- **高效导出**：支持大容量数据导出（百万级数据点）
- **元数据完整**：保留Job ID、通道名、时间信息等

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化波形导出配置
python -m cloudpss_skills init waveform_export --output waveform.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config waveform.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("waveform_export")

# 配置
config = {
    "skill": "waveform_export",
    "source": {
        "job_id": "job_abc123",
        "auth": {
            "token_file": ".cloudpss_token"
        }
    },
    "export": {
        "plots": [],           # 空表示全部分组
        "channels": ["Bus_16_V", "Bus_15_V"],  # 空表示全部通道
        "time_range": {
            "start": 0,
            "end": 10
        }
    },
    "output": {
        "format": "csv",
        "path": "./results/",
        "filename": "waveforms.csv"
    }
}

# 运行
result = skill.run(config)
print(f"导出完成: {result.data}")
```

### 3.3 YAML配置示例

```yaml
skill: waveform_export
source:
  job_id: "job_abc123"
  auth:
    token_file: .cloudpss_token

export:
  plots: []              # 波形分组索引，空表示全部
  channels: []          # 通道名称，空表示全部
  time_range:
    start: 0.0          # 开始时间(s)
    end: 10.0           # 结束时间(s)

output:
  format: csv           # csv | json
  path: ./results/
  filename: waveforms.csv
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: waveform_export                 # 必需: 技能名称
source:                                 # 必需: 数据源配置
  job_id: string                       # 必需: 仿真任务ID
  auth:                                # 认证配置
    token: string                      # 直接提供token
    token_file: string                 # token文件路径

export:                                 # 导出配置
  plots:                               # 波形分组索引列表
    - integer                         # 空表示全部
  channels:                            # 通道名称列表
    - string                          # 空表示全部
  time_range:                          # 时间范围（可选）
    start: number                      # 开始时间(s)
    end: number                        # 结束时间(s)

output:                                 # 输出配置
  format: enum                         # csv | json（默认: csv）
  path: string                         # 输出目录（默认: ./results/）
  filename: string                     # 输出文件名（可选）
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"waveform_export" |
| `source.job_id` | string | 是 | - | 仿真任务ID |
| `source.auth.token` | string | 否 | - | 直接提供API token |
| `source.auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `export.plots` | array | 否 | [] | 波形分组索引，空表示全部 |
| `export.channels` | array | 否 | [] | 通道名称列表，空表示全部 |
| `export.time_range.start` | number | 否 | - | 开始时间(s) |
| `export.time_range.end` | number | 否 | - | 结束时间(s) |
| `output.format` | enum | 否 | csv | 输出格式: csv/json |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.filename` | string | 否 | 自动生成 | 输出文件名 |

## Agent使用指南

### 5.1 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("waveform_export")

# 最小配置（导出全部）
config = {
    "source": {
        "job_id": "job_abc123"
    }
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status == "SUCCESS":
        print(f"导出完成: {result.data}")
    else:
        print(f"导出失败: {result.error}")
```

### 5.2 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data
    # 访问结果数据
    job_id = data.get("job_id")
    plot_count = data.get("plot_count")
    exported_plots = data.get("exported_plots")

    print(f"任务 {job_id} 共 {plot_count} 个分组，导出 {exported_plots} 个")

# 访问输出文件
for artifact in result.artifacts:
    print(f"输出文件: {artifact.path} ({artifact.type}, {artifact.size} bytes)")
```

### 5.3 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    error_msg = result.error

    # 常见错误处理
    if "必须提供有效的 source.job_id" in error_msg:
        print("错误: 请提供有效的Job ID")
        print("示例: 'job-12345678-abcd-1234-efgh-123456789012'")
    elif "任务未完成或失败" in error_msg:
        print("错误: 任务尚未完成，请等待仿真结束")
    elif "认证失败" in error_msg:
        print("错误: 请检查token文件是否存在且有效")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### 6.1 CSV格式输出

```csv
time,Bus_16_V,Bus_15_V
0.0,1.0001,0.9998
0.0001,1.0002,0.9999
0.0002,1.0001,1.0000
...
```

### 6.2 JSON格式输出

```json
{
  "job_id": "job_abc123",
  "plots": [
    {
      "plot_index": 0,
      "plot_key": "Bus Voltages",
      "channels": {
        "Bus_16_V": {
          "x": [0.0, 0.0001, 0.0002, ...],
          "y": [1.0001, 1.0002, 1.0001, ...]
        },
        "Bus_15_V": {
          "x": [0.0, 0.0001, 0.0002, ...],
          "y": [0.9998, 0.9999, 1.0000, ...]
        }
      }
    }
  ]
}
```

### 6.3 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "waveform_export" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典（job_id, plot_count, exported_plots） |
| `artifacts` | list | 输出文件列表（Artifact对象） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |

## 设计原理

### 工作流程

```
1. 认证
   └── 加载CloudPSS token

2. 获取任务
   └── 通过Job ID获取仿真任务
   └── 检查任务状态（必须已完成）

3. 提取结果
   └── 获取结果对象
   └── 列出所有波形分组

4. 数据筛选
   └── 按plots参数筛选分组
   └── 按channels参数筛选通道
   └── 按time_range切片时间

5. 数据导出
   └── 按格式组织数据
   │   ├── CSV: 时间列 + 各通道列
   │   └── JSON: 嵌套结构
   └── 写入文件

6. 结果返回
   └── 返回导出信息和文件路径
```

## 与其他技能的关联

```
emt_simulation / power_flow
    ↓ (仿真执行，产生Job ID)
waveform_export
    ↓ (导出数据文件)
    ├── CSV → Excel / MATLAB / Python pandas
    └── JSON → Python / JavaScript
```

**输入依赖**: 需要仿真技能产生的Job ID
**输出被依赖**:
- `visualize`: 可用本地文件绘图
- `result_compare`: 导出多组数据后对比
- `hdf5_export`: 可进一步转换为HDF5格式

## 性能特点

- **执行时间**: 取决于数据量，通常5-20秒
- **内存占用**: 与通道数和数据点数成正比
- **导出速度**: 约100万数据点/秒
- **文件大小**: CSV约10MB/百万点，JSON约15MB/百万点
- **适用规模**: 已测试至导出1000万数据点

## 常见问题

### 问题1: Job ID无效

**原因**: Job ID格式错误或任务不存在

**解决**:
```python
# 确认Job ID格式正确
config["source"]["job_id"] = "job-12345678-abcd-1234-efgh-123456789012"

# 从CloudPSS平台复制正确的Job ID
```

### 问题2: 任务未完成

**原因**: 仿真仍在运行或已失败

**解决**:
```python
from cloudpss import Job

job = Job.fetch("job_abc123")
status = job.status()
if status == 0:
    print("任务仍在运行，请等待...")
elif status == 2:
    print("任务失败，请检查仿真配置")
```

### 问题3: 通道名不存在

**原因**: 指定的通道名与结果中的不匹配

**解决**:
```python
# 先查看可用通道
from cloudpss import Job

job = Job.fetch("job_abc123")
result = job.result
plots = list(result.getPlots())
for i, plot in enumerate(plots):
    channels = result.getPlotChannelNames(i)
    print(f"分组 {i}: {channels}")
```

### 问题4: 数据量过大

**原因**: 导出全部数据导致内存不足

**解决**:
```yaml
export:
  time_range:
    start: 0    # 只导出关键时段
    end: 10
  channels:     # 只导出关键通道
    - "Bus_16_V"
    - "Bus_15_V"
```

### 问题5: CSV格式问题

**原因**: 中文通道名或特殊字符

**解决**:
```python
# 使用JSON格式保留完整信息
output:
  format: json
```

## 完整示例

### 场景描述

某工程师需要导出IEEE39系统故障仿真的母线电压数据，用于MATLAB分析。

### 配置文件

```yaml
skill: waveform_export
source:
  job_id: "job_20240324_emt_001"
  auth:
    token_file: .cloudpss_token

export:
  plots: [0]             # 只导出第0个分组
  channels:              # 只导出母线电压
    - "Bus_16_V"
    - "Bus_15_V"
    - "Bus_14_V"
    - "Bus_13_V"
  time_range:
    start: 3.0          # 故障前1s到故障后5s
    end: 9.0

output:
  format: csv
  path: ./results/
  filename: ieee39_fault_voltage.csv
```

### 执行命令

```bash
python -m cloudpss_skills run --config waveform_config.yaml
```

### 预期输出

```
[INFO] 认证...
[INFO] 获取任务: job_20240324_emt_001
[INFO] 提取结果...
[INFO] 波形分组数: 3
[INFO] 导出完成: ./results/ieee39_fault_voltage.csv
```

### 结果文件

CSV文件 `./results/ieee39_fault_voltage.csv`:

```csv
time,Bus_16_V,Bus_15_V,Bus_14_V,Bus_13_V
3.0,1.0001,0.9998,1.0003,0.9997
3.0001,1.0002,0.9999,1.0002,0.9998
...
4.0,0.6523,0.5874,0.7231,0.6912  # 故障时刻
4.0001,0.6345,0.5721,0.6987,0.6754
...
9.0,1.0000,0.9999,1.0001,0.9998  # 故障切除后恢复
```

### 后续应用

1. **MATLAB分析**:
```matlab
data = readmatrix('ieee39_fault_voltage.csv');
t = data(:,1);
v16 = data(:,2);
plot(t, v16);
```

2. **Python分析**:
```python
import pandas as pd
df = pd.read_csv('ieee39_fault_voltage.csv')
df.plot(x='time', y='Bus_16_V')
```

3. **转换为HDF5**:
```python
from cloudpss_skills import get_skill
skill = get_skill("hdf5_export")
config = {
    "source": {"type": "file", "file_path": "./results/ieee39_fault_voltage.csv"},
    "output": {"path": "./results/", "filename": "voltage_data.h5"}
}
skill.run(config)
```

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
