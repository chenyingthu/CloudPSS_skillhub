# 可视化技能 (Visualize)

## 设计背景

### 研究对象

电力系统仿真产生大量时序数据，如母线电压、支路潮流、发电机功角等。将这些数据以图形化方式呈现，可以直观理解系统动态行为、识别异常模式、支持工程决策。

### 实际需求

工程师需要可视化工具来：

1. **快速查看波形**：检查仿真结果是否符合预期
2. **多通道对比**：对比不同母线或设备的响应
3. **报告生成**：为技术报告生成高质量的图表
4. **异常识别**：通过视觉发现电压跌落、振荡等异常
5. **时序分析**：观察系统在故障前后的动态响应

### 期望的输入和输出

**输入**:
- 仿真任务Job ID 或本地数据文件
- 要绘制的通道列表
- 图表类型配置（时序图、柱状图、散点图）
- 图表样式（标题、坐标轴标签、分辨率）
- 时间范围切片（可选）

**输出**:
- 图表文件（PNG/PDF/SVG格式）
- 图表元数据（通道数、数据点数）
- 执行日志

### 计算结果的用途和价值

可视化结果可用于：
- 快速验证仿真结果的正确性
- 识别系统的动态特性和问题
- 生成技术报告和演示文稿
- 与团队成员分享分析结果
- 存档记录系统运行特征

## 功能特性

- **多种图表类型**：时序图、柱状图、散点图、对比图
- **多数据源支持**：支持CloudPSS Job ID或本地CSV文件
- **灵活样式配置**：自定义标题、坐标轴、图例、分辨率
- **时间切片**：支持指定时间范围进行局部绘图
- **高质量输出**：支持PNG、PDF、SVG多种格式

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化可视化配置
python -m cloudpss_skills init visualize --output visualize.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config visualize.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("visualize")

# 配置
config = {
    "skill": "visualize",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "source": {
        "job_id": "job_abc123"
    },
    "plot": {
        "type": "time_series",
        "channels": ["Bus_16_V", "Bus_15_V"],
        "title": "母线电压波形",
        "xlabel": "时间 (s)",
        "ylabel": "电压 (pu)",
        "time_range": {
            "start": 0,
            "end": 10
        }
    },
    "output": {
        "format": "png",
        "path": "./results/",
        "filename": "voltage_waveform",
        "dpi": 150,
        "width": 12,
        "height": 6
    }
}

# 运行
result = skill.run(config)
print(f"图表已保存: {result.data.get('output')}")
```

### 3.3 YAML配置示例

```yaml
skill: visualize
auth:
  token_file: .cloudpss_token

source:
  job_id: "job_abc123"  # 或 data_file: "./results/waveforms.csv"

plot:
  type: time_series     # time_series | bar | scatter | comparison
  channels: ["Bus_16_V", "Bus_15_V", "Bus_14_V"]
  title: "母线电压波形"
  xlabel: "时间 (s)"
  ylabel: "电压 (pu)"
  time_range:
    start: 0
    end: 10

output:
  format: png           # png | pdf | svg
  path: ./results/
  filename: voltage_waveform
  dpi: 150
  width: 12
  height: 6
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: visualize                       # 必需: 技能名称
auth:                                   # 认证配置
  token: string                        # 直接提供token（不推荐）
  token_file: string                   # token文件路径（默认: .cloudpss_token）

source:                                 # 数据源配置（二选一）
  job_id: string                       # CloudPSS任务ID
  data_file: string                    # 本地数据文件路径（CSV格式）

plot:                                   # 绘图配置
  type: enum                           # time_series | bar | scatter | comparison（默认: time_series）
  channels:                            # 要绘制的通道列表
    - string
  title: string                        # 图表标题
  xlabel: string                       # X轴标签
  ylabel: string                       # Y轴标签
  time_range:                          # 时间范围（可选）
    start: number                      # 开始时间(s)
    end: number                        # 结束时间(s)

output:                                 # 输出配置
  format: enum                         # png | pdf | svg（默认: png）
  path: string                         # 输出目录（默认: ./results/）
  filename: string                     # 输出文件名（可选）
  dpi: integer                         # 分辨率DPI（默认: 150）
  width: number                        # 图表宽度（英寸，默认: 12）
  height: number                       # 图表高度（英寸，默认: 6）
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"visualize" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `source.job_id` | string | 否 | - | CloudPSS任务ID（与data_file二选一） |
| `source.data_file` | string | 否 | - | 本地CSV文件路径 |
| `plot.type` | enum | 否 | time_series | 图表类型 |
| `plot.channels` | array | 否 | [] | 通道列表，空表示全部 |
| `plot.title` | string | 否 | "Waveform" | 图表标题 |
| `plot.xlabel` | string | 否 | "Time (s)" | X轴标签 |
| `plot.ylabel` | string | 否 | "Value" | Y轴标签 |
| `plot.time_range.start` | number | 否 | - | 开始时间(s) |
| `plot.time_range.end` | number | 否 | - | 结束时间(s) |
| `output.format` | enum | 否 | png | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.filename` | string | 否 | 自动生成 | 输出文件名 |
| `output.dpi` | integer | 否 | 150 | 分辨率DPI |
| `output.width` | number | 否 | 12 | 图表宽度(英寸) |
| `output.height` | number | 否 | 6 | 图表高度(英寸) |

## Agent使用指南

### 5.1 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("visualize")

# 从Job ID绘图
config = {
    "source": {"job_id": "job_abc123"},
    "plot": {
        "type": "time_series",
        "channels": ["Bus_16_V"]
    }
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status == "SUCCESS":
        print(f"图表生成完成: {result.data}")
```

### 5.2 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data
    # 访问结果数据
    channels_count = data.get("channels")
    data_points = data.get("data_points")
    output_path = data.get("output")

    print(f"绘制了 {channels_count} 个通道，共 {data_points} 个数据点")
    print(f"图表保存至: {output_path}")

# 访问输出文件
for artifact in result.artifacts:
    print(f"输出文件: {artifact.path} ({artifact.type})")
```

### 5.3 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    error_msg = result.error

    # 常见错误处理
    if "必须提供source.job_id或source.data_file" in error_msg:
        print("错误: 请提供Job ID或本地数据文件路径")
    elif "任务结果为空" in error_msg:
        print("错误: 任务尚未完成或结果为空")
    elif "没有波形数据" in error_msg:
        print("错误: 该任务没有波形数据输出")
    elif "数据文件不存在" in error_msg:
        print("错误: 请检查本地数据文件路径")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### 6.1 执行结果数据

```json
{
  "channels": 3,
  "data_points": 10000,
  "output": "./results/waveform_20240324_143245.png"
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "visualize" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典（channels, data_points, output） |
| `artifacts` | list | 输出文件列表（Artifact对象） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标 |

## 设计原理

### 工作流程

```
1. 数据获取
   ├── 从CloudPSS获取Job结果
   │   └── 提取波形数据
   └── 或从本地CSV读取数据
       └── 解析通道和时间列

2. 数据处理
   ├── 筛选指定通道
   ├── 应用时间范围切片
   └── 数据格式转换

3. 图表生成
   ├── 创建Matplotlib图形
   ├── 根据类型配置绘图参数
   │   ├── time_series: 时序曲线
   │   ├── bar: 柱状图
   │   └── scatter: 散点图
   └── 添加标题、标签、图例

4. 文件输出
   └── 保存为指定格式
       ├── PNG: 位图，适合屏幕显示
       ├── PDF: 矢量图，适合打印
       └── SVG: 矢量图，适合网页
```

## 与其他技能的关联

```
emt_simulation / power_flow / 其他仿真技能
    ↓ (仿真结果Job ID)
visualize
    ↓ (图表文件)
技术报告 / 演示文稿 / Web展示
```

**输入依赖**: 需要仿真技能产生的Job ID，或本地数据文件
**输出被依赖**: 图表可直接用于报告、演示、网页展示

**配合使用**:
- `waveform_export`: 先导出波形数据，再用本地文件绘图
- `result_compare`: 可视化对比多个任务的结果

## 性能特点

- **执行时间**: 取决于数据量，通常5-15秒
- **内存占用**: 与通道数和数据点数成正比
- **图表质量**: 支持高DPI输出（最高300 DPI）
- **适用规模**: 已测试至同时绘制20个通道、10万数据点

## 常见问题

### 问题1: 数据源未指定

**原因**: 未提供Job ID或本地数据文件

**解决**:
```yaml
source:
  job_id: "job_abc123"  # 提供有效的Job ID
  # 或
  # data_file: "./results/data.csv"
```

### 问题2: 任务无波形数据

**原因**: 潮流计算等无波形输出的任务

**解决**: 该技能主要用于EMT仿真结果可视化。对于潮流结果，建议直接查看数据表格。

### 问题3: 通道名不匹配

**原因**: 指定的通道名不存在于结果中

**解决**:
```python
# 查看可用通道
from cloudpss import Job
job = Job.fetch("job_abc123")
result = job.result
channels = result.getPlotChannelNames(0)
print(f"可用通道: {channels}")
```

### 问题4: 中文显示乱码

**原因**: 系统缺少中文字体

**解决**:
```bash
# Linux系统安装中文字体
sudo apt-get install fonts-wqy-microhei

# 或在配置中使用英文标签
plot:
  title: "Voltage Waveform"
  xlabel: "Time (s)"
  ylabel: "Voltage (pu)"
```

### 问题5: 图表分辨率低

**原因**: DPI设置过低

**解决**:
```yaml
output:
  dpi: 300  # 提高分辨率
  format: pdf  # 或矢量格式
```

## 完整示例

### 场景描述

某工程师需要生成IEEE39系统故障后母线电压的波形图，用于技术报告。

### 配置文件

```yaml
skill: visualize
auth:
  token_file: .cloudpss_token

source:
  job_id: "job_20240324_emt_001"

plot:
  type: time_series
  channels: ["Bus_16_V", "Bus_15_V", "Bus_14_V"]
  title: "故障后母线电压恢复过程"
  xlabel: "时间 (s)"
  ylabel: "电压 (pu)"
  time_range:
    start: 3
    end: 8

output:
  format: png
  path: ./results/
  filename: voltage_recovery
  dpi: 200
  width: 14
  height: 8
```

### 执行命令

```bash
python -m cloudpss_skills run --config visualize_config.yaml
```

### 预期输出

```
[INFO] 从CloudPSS获取数据...
[INFO] 获取到 4 个通道
[INFO] 时间范围筛选后: 50000 个点
[INFO] 生成图表...
[INFO] 图表已保存: ./results/voltage_recovery.png
```

### 结果文件

生成文件 `./results/voltage_recovery.png`，包含三条电压曲线：
- Bus_16_V（红色）
- Bus_15_V（蓝色）
- Bus_14_V（绿色）

图表显示故障发生后（4s）各母线电压的跌落和恢复过程。

### 后续应用

1. **报告插入**: 将PNG图表插入Word/PPT报告
2. **矢量输出**: 使用PDF格式进行高质量打印
3. **批量生成**: 配合脚本批量生成多场景图表
4. **Web展示**: 使用SVG格式在网页中展示

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28, matplotlib >= 3.5.0
