# Study Pipeline Skill

研究流水线技能 - 自动串联多个技能执行完整研究流程。

## 概述

`study_pipeline` 是一个工作流编排技能，可以自动串联多个技能按依赖顺序执行，支持步骤间数据传递、结果聚合和断点续跑。

## 功能特性

### 1. 自动串联执行
- 按配置顺序自动执行多个技能
- 支持步骤依赖声明（`depends_on`）
- 支持前置失败时跳过（`skip_on_failure`）

### 2. 数据传递
- 使用 `${steps.xxx.data}` 占位符引用前置步骤的数据
- 使用 `${steps.xxx.artifacts}` 获取产物列表
- 自动解析嵌套配置

### 3. 统一输出管理
- 所有步骤共享输出目录
- 自动聚合产物列表
- 生成综合执行报告

### 4. 错误处理
- 支持 `continue_on_failure` 模式
- 记录每步执行状态和耗时
- 失败后仍可查看已生成结果

## 快速开始

### YAML 配置

```yaml
skill: study_pipeline
auth:
  token_file: .cloudpss_token

pipeline:
  - name: baseline_powerflow
    skill: power_flow
    config:
      model:
        rid: model/holdme/IEEE39
        source: cloud
      output:
        path: ./results/baseline

  - name: n1_security
    skill: n1_security
    config:
      model:
        rid: model/holdme/IEEE39
        source: cloud
      output:
        path: ./results/baseline
    depends_on:
      - baseline_powerflow

  - name: voltage_stability
    skill: voltage_stability
    config:
      model:
        rid: model/holdme/IEEE39
        source: cloud
      monitoring:
        buses:
          - ${steps.n1_security.data.critical_buses}

output:
  path: ./results/
  prefix: full_study
  generate_report: true

continue_on_failure: false
```

### Python API

```python
from cloudpss_skills.builtin.study_pipeline import StudyPipelineSkill

pipeline = StudyPipelineSkill()

config = {
    "skill": "study_pipeline",
    "auth": {"token_file": ".cloudpss_token"},
    "pipeline": [
        {
            "name": "baseline",
            "skill": "power_flow",
            "config": {"model": {"rid": "model/holdme/IEEE39"}},
        },
        {
            "name": "n1",
            "skill": "n1_security",
            "config": {"model": {"rid": "model/holdme/IEEE39"}},
        },
    ],
}

result = pipeline.run(config)

print(f"成功: {result.data['success_count']}/{result.data['total_steps']}")
```

## 配置 Schema

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `skill` | string | ✓ | 固定值 `study_pipeline` |
| `auth` | object | ✓ | 认证配置 |
| `pipeline` | array | ✓ | 步骤列表 |
| `output` | object | | 输出配置 |
| `continue_on_failure` | boolean | | 失败时是否继续 |

### Pipeline 步骤配置

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | 步骤名称（用于引用） |
| `skill` | string | 技能名称 |
| `config` | object | 技能配置 |
| `skip_on_failure` | boolean | 前置失败时跳过 |
| `depends_on` | array | 依赖的前置步骤 |

## 变量占位符

### 引用前置数据

```yaml
# 引用前置步骤的数据
monitoring:
  buses: ${steps.n1_security.data.critical_buses}

# 引用前置步骤的产物
sources:
  - ${steps.baseline.artifacts}
```

### 支持的变量格式

| 格式 | 说明 | 示例 |
|------|------|------|
| `${steps.<name>.data}` | 步骤结果数据 | `${steps.n1.data}` |
| `${steps.<name>.data.field}` | 数据字段 | `${steps.n1.data.critical_buses}` |
| `${steps.<name>.artifacts}` | 产物列表 | `${steps.pf.artifacts}` |
| `${steps.<name>.status}` | 执行状态 | `${steps.pf.status}` |

## Agent 使用指南

### 1. 创建标准研究流程

```python
# 完整安全评估流程
config = {
    "skill": "study_pipeline",
    "pipeline": [
        {
            "name": "powerflow",
            "skill": "power_flow",
            "config": {"model": {"rid": "model/holdme/IEEE39"}},
        },
        {
            "name": "n1",
            "skill": "n1_security",
            "config": {"model": {"rid": "model/holdme/IEEE39"}},
        },
        {
            "name": "contingency",
            "skill": "contingency_analysis",
            "config": {
                "model": {"rid": "model/holdme/IEEE39"},
                "contingency": {"level": "N-1"},
            },
        },
    ],
}
```

### 2. 使用数据传递

```python
# 假设 n1_security 输出了 critical_buses
# 传递给 voltage_stability 进行针对性分析

config = {
    "pipeline": [
        {"name": "n1", "skill": "n1_security", "config": {...}},
        {
            "name": "voltage",
            "skill": "voltage_stability",
            "config": {
                "monitoring": {
                    "buses": "${steps.n1.data.critical_buses}"
                }
            },
        },
    ]
}
```

### 3. 批量模型研究

```python
# 对多个模型执行相同研究流程
models = ["model/holdme/IEEE3", "model/holdme/IEEE39"]

config = {
    "pipeline": [
        {
            "skill": "batch_powerflow",
            "config": {
                "models": [{"rid": rid} for rid in models]
            },
        },
        {
            "skill": "report_generator",
            "config": {
                "sources": "${steps.batch_powerflow.artifacts}"
            },
        },
    ]
}
```

## 输出结果

### 数据结构

```python
{
    "timestamp": "2026-04-12T14:30:00",
    "total_steps": 3,
    "success_count": 3,
    "failed_count": 0,
    "steps": [
        {
            "name": "powerflow",
            "skill": "power_flow",
            "status": "success",
            "duration": 12.5
        },
        {
            "name": "n1",
            "skill": "n1_security",
            "status": "success",
            "duration": 45.2
        }
    ],
    "context": {
        "powerflow": {
            "status": "SUCCESS",
            "has_data": True,
            "artifacts_count": 1
        }
    }
}
```

### 生成的文件

| 文件 | 说明 |
|------|------|
| `pipeline_<timestamp>.json` | 流水线执行结果 |
| `pipeline_<timestamp>_report.md` | 执行报告（可选） |

## 与其他技能的关联

| 上游技能 | 组合方式 |
|----------|----------|
| `power_flow` | 作为基线，为后续分析提供初始状态 |
| `n1_security` | 结合做完整安全评估 |
| `voltage_stability` | 结合做电压稳定研究 |

| 下游技能 | 组合方式 |
|----------|----------|
| `report_generator` | 汇总所有结果生成报告 |
| `visualize` | 可视化流水线产物 |

### 典型工作流

```
study_pipeline
├── power_flow (基线潮流)
├── n1_security (N-1校核)
├── voltage_stability (电压分析)
└── report_generator (生成报告)
```

## 性能特点

| 指标 | 说明 |
|------|------|
| 并行支持 | 当前版本顺序执行，可配置依赖优化 |
| 断点续跑 | 失败后可直接重跑，跳过成功步骤 |
| 日志追踪 | 每步完整日志，便于调试 |

## 常见问题

### Q: 如何跳过失败的步骤继续执行？

```yaml
continue_on_failure: true  # 允许继续执行
```

### Q: 如何引用前置步骤的数据？

使用 `${steps.<name>.data.field}` 格式：

```yaml
buses: ${steps.n1.data.critical_buses}
```

### Q: 如何让步骤依赖多个前置步骤？

```yaml
- name: final
  skill: report_generator
  depends_on:
    - baseline
    - n1
    - voltage
```

## 完整示例

### IEEE39 完整安全评估

```yaml
skill: study_pipeline
auth:
  token_file: .cloudpss_token

pipeline:
  - name: baseline
    skill: power_flow
    config:
      model: {rid: model/holdme/IEEE39}
      output: {path: ./results/ieee39}

  - name: n1
    skill: n1_security
    config:
      model: {rid: model/holdme/IEEE39}
      output: {path: ./results/ieee39}
    depends_on: [baseline]

  - name: n2
    skill: n2_security
    config:
      model: {rid: model/holdme/IEEE39}
      output: {path: ./results/ieee39}
    depends_on: [baseline]

  - name: voltage
    skill: voltage_stability
    config:
      model: {rid: model/holdme/IEEE39}
      monitoring:
        buses: ${steps.n1.data.critical_buses}
    depends_on: [n1]

  - name: report
    skill: report_generator
    config:
      sources:
        - ${steps.baseline.artifacts}
        - ${steps.n1.artifacts}
        - ${steps.n2.artifacts}
        - ${steps.voltage.artifacts}
    depends_on: [n1, n2, voltage]

output:
  path: ./results/ieee39_full
  prefix: security_assessment
  generate_report: true

continue_on_failure: false
```

## 版本信息

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-04-12 | 初始版本 |
