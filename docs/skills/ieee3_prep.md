# IEEE3模型准备技能 (IEEE3 Prep)

## 概述

IEEE3模型准备技能用于准备IEEE3标准测试系统，配置EMT仿真所需的故障元件和测量通道。

## 功能特性

- **自动配置**: 自动添加故障元件
- **测量配置**: 配置电压电流测量
- **输出设置**: 配置EMT输出通道
- **一键准备**: 简化EMT仿真准备流程

## 快速开始

### 1. YAML配置

```yaml
skill: ieee3_prep
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

fault:
  start_time: 2.5
  end_time: 2.7

output:
  sampling_freq: 2000
  path: ./
  filename: ieee3_prepared.yaml
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("ieee3_prep")

config = {
    "skill": "ieee3_prep",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE3"},
    "fault": {
        "start_time": 2.5,
        "end_time": 2.7
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "ieee3_prep" |
| `model.rid` | string | 是 | - | 模型RID |
| `fault.start_time` | number | 否 | 2.5 | 故障开始时间(s) |
| `fault.end_time` | number | 否 | 2.7 | 故障结束时间(s) |
| `output.sampling_freq` | number | 否 | 2000 | 采样频率(Hz) |
| `output.path` | string | 否 | ./ | 输出路径 |
| `output.filename` | string | 否 | - | 输出文件名 |

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
