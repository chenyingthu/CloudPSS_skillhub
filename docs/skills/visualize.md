# 可视化技能 (Visualize)

## 概述

可视化技能用于生成波形图和结果可视化图表，支持时序图、柱状图、散点图等多种图表类型。

## 功能特性

- **多种图表类型**: 时序图、柱状图、散点图
- **多格式输出**: PNG、PDF、SVG
- **自定义样式**: 标题、标签、颜色等
- **多通道对比**: 支持同时绘制多个通道

## 设计原理

### 绘图流程

```
1. 加载数据源（job_id或数据文件）
2. 解析通道数据
3. 根据图表类型配置绘图参数
4. 生成图表
5. 保存到文件
```

## 快速开始

### 1. YAML配置

```yaml
skill: visualize
auth:
  token_file: .cloudpss_token

source:
  job_id: "job_abc123"  # 或 data_file: "./data.csv"

plot:
  type: time_series     # time_series | bar | scatter
  channels: ["Bus1_V", "Bus2_V"]
  title: "母线电压波形"
  xlabel: "时间 (s)"
  ylabel: "电压 (pu)"

output:
  format: png           # png | pdf | svg
  path: ./results/
  filename: voltage_plot.png
  dpi: 150
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("visualize")

config = {
    "skill": "visualize",
    "source": {"job_id": "job_abc123"},
    "plot": {
        "type": "time_series",
        "channels": ["Bus1_V"],
        "title": "Voltage Waveform"
    },
    "output": {
        "format": "png",
        "path": "./results/",
        "dpi": 150
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "visualize" |
| `source.job_id` | string | 否 | - | 任务ID |
| `source.data_file` | string | 否 | - | 数据文件路径 |
| `plot.type` | enum | 否 | time_series | time_series / bar / scatter |
| `plot.channels` | array | 是 | - | 通道列表 |
| `plot.title` | string | 否 | - | 图表标题 |
| `plot.xlabel` | string | 否 | - | X轴标签 |
| `plot.ylabel` | string | 否 | - | Y轴标签 |
| `output.format` | enum | 否 | png | png / pdf / svg |
| `output.path` | string | 否 | ./results/ | 输出目录 |
| `output.dpi` | integer | 否 | 150 | 分辨率 |

## 图表类型

### 时序图 (time_series)

适合显示波形随时间变化

### 柱状图 (bar)

适合对比不同通道的指标

### 散点图 (scatter)

适合显示通道间关系

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
