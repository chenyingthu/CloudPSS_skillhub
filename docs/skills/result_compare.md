# 结果对比技能 (Result Compare)

## 概述

结果对比技能用于对比多次仿真结果，生成差异分析报告，支持按通道对比指标（最大值、最小值、平均值等）。

## 功能特性

- **多结果对比**: 支持2个及以上结果对比
- **指标计算**: 自动计算max、min、mean等指标
- **差异分析**: 高亮显示差异较大的通道
- **多格式输出**: JSON、Markdown格式报告

## 设计原理

### 对比流程

```
1. 加载所有对比源（job_id列表）
2. 获取每个源的波形数据
3. 对于每个对比通道:
   a. 计算各源的指标
   b. 计算差异
   c. 判断是否超出阈值
4. 生成对比表格
5. 生成报告
```

## 快速开始

### 1. YAML配置

```yaml
skill: result_compare
auth:
  token_file: .cloudpss_token

source:
  - job_id: "job_abc123"
    label: "基准方案"
  - job_id: "job_def456"
    label: "对比方案"

compare:
  channels: ["Bus1_V", "Bus2_V", "Bus3_V"]
  metrics: [max, min, mean]
  threshold: 0.1  # 差异阈值

output:
  format: markdown
  path: ./results/
  prefix: compare
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("result_compare")

config = {
    "skill": "result_compare",
    "auth": {"token_file": ".cloudpss_token"},
    "source": [
        {"job_id": "job_abc123", "label": "Case A"},
        {"job_id": "job_def456", "label": "Case B"}
    ],
    "compare": {
        "channels": ["Bus1_V"],
        "metrics": ["max", "min", "mean"]
    }
}

result = skill.run(config)
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "result_compare" |
| `source` | array | 是 | - | 对比源列表 |
| `source[].job_id` | string | 是 | - | 任务ID |
| `source[].label` | string | 是 | - | 标签 |
| `compare.channels` | array | 是 | - | 对比通道列表 |
| `compare.metrics` | array | 否 | [max, min, mean] | 指标列表 |
| `compare.threshold` | number | 否 | 0.1 | 差异阈值 |
| `output.format` | enum | 否 | markdown | json / markdown |
| `output.path` | string | 否 | ./results/ | 输出目录 |
| `output.prefix` | string | 否 | compare | 文件名前缀 |

## Agent使用指南

### 基础调用

```python
skill = get_skill("result_compare")

config = {
    "source": [
        {"job_id": "job1", "label": "Before"},
        {"job_id": "job2", "label": "After"}
    ],
    "compare": {
        "channels": ["Bus1_V"],
        "metrics": ["max", "min"]
    }
}

result = skill.run(config)
```

## 输出结果

### Markdown报告

```markdown
# 结果对比报告

| 通道 | 指标 | Before | After | 差异 |
|------|------|--------|-------|------|
| Bus1_V | max | 1.05 | 1.02 | -0.03 |
| Bus1_V | min | 0.95 | 0.98 | +0.03 |
```

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
