# 波形导出技能 (Waveform Export)

## 概述

波形导出技能用于从已完成的仿真任务中导出波形数据，支持时间范围选择和通道筛选。

## 功能特性

- **任务ID导入**: 通过任务ID获取结果
- **时间切片**: 支持指定时间范围导出
- **通道选择**: 可选择特定通道导出
- **多格式支持**: CSV、JSON格式

## 快速开始

### 1. YAML配置

```yaml
skill: waveform_export
auth:
  token_file: .cloudpss_token

source:
  job_id: "your_job_id"

export:
  plots: []           # 分组索引，空表示全部
  channels: []        # 通道名称，空表示全部
  time_range:
    start: 0.0
    end: 10.0

output:
  format: csv
  path: ./results/
  prefix: waveform
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("waveform_export")

config = {
    "skill": "waveform_export",
    "auth": {"token_file": ".cloudpss_token"},
    "source": {"job_id": "job_abc123"},
    "export": {
        "time_range": {"start": 0.0, "end": 10.0}
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "waveform_export" |
| `source.job_id` | string | 是 | - | 仿真任务ID |
| `export.plots` | array | 否 | [] | 分组索引列表 |
| `export.channels` | array | 否 | [] | 通道名称列表 |
| `export.time_range.start` | number | 否 | 0.0 | 开始时间(s) |
| `export.time_range.end` | number | 否 | - | 结束时间(s) |
| `output.format` | enum | 否 | csv | csv / json |

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
