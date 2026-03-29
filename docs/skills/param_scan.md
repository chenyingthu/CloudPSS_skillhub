# 参数扫描技能 (Parameter Scan)

## 概述

参数扫描技能用于对指定元件参数进行批量变化，运行多次仿真，分析参数变化对系统的影响。支持潮流计算和EMT暂态仿真两种模式。

## 功能特性

- **批量参数变化**: 自动修改元件参数并运行仿真
- **支持多种仿真**: 潮流计算或EMT暂态仿真
- **结果汇总**: JSON格式的扫描结果汇总
- **收敛状态追踪**: 记录每次仿真的收敛状态

## 设计原理

### 扫描流程

```
1. 加载原始模型
2. 获取扫描配置（元件、参数、值列表）
3. 对于每个参数值:
   a. 重新加载模型
   b. 查找目标元件
   c. 修改参数值
   d. 运行仿真（潮流或EMT）
   e. 记录结果
4. 汇总扫描结果
5. 生成报告
```

### 参数修改机制

使用CloudPSS的`updateComponent` API修改元件参数：

```python
model.updateComponent(
    component_id,
    args={"P": {"source": str(value), "ɵexp": ""}}
)
```

## 快速开始

### 1. CLI方式

```bash
# 初始化配置
python -m cloudpss_skills init param_scan --output scan.yaml

# 运行
python -m cloudpss_skills run --config scan.yaml
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("param_scan")

config = {
    "skill": "param_scan",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE3"},
    "scan": {
        "component": "Bus1_Load",      # 元件ID或名称
        "parameter": "P",               # 参数名
        "values": [10, 20, 30, 40, 50], # 扫描值列表
        "simulation_type": "power_flow" # power_flow | emt
    }
}

result = skill.run(config)
```

### 3. YAML配置

```yaml
skill: param_scan
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

scan:
  component: Bus1_Load    # 元件ID或名称
  parameter: P            # 参数名
  values: [10, 20, 30, 40, 50]  # 参数值列表
  simulation_type: power_flow   # power_flow | emt

output:
  format: json
  path: ./results/
  prefix: param_scan
  timestamp: true
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "param_scan" |
| `model.rid` | string | 是 | - | 模型RID |
| `model.source` | enum | 否 | cloud | cloud / local |
| `scan.component` | string | 是 | - | 元件ID或名称 |
| `scan.parameter` | string | 是 | - | 参数名 |
| `scan.values` | array | 是 | - | 参数值列表（number数组） |
| `scan.simulation_type` | enum | 否 | power_flow | power_flow / emt |
| `output.format` | enum | 否 | json | json / csv |
| `output.path` | string | 否 | ./results/ | 输出目录 |
| `output.prefix` | string | 否 | param_scan | 文件名前缀 |
| `output.timestamp` | boolean | 否 | true | 添加时间戳 |

## Agent使用指南

### 基础调用

```python
skill = get_skill("param_scan")

config = {
    "model": {"rid": "model/holdme/IEEE3"},
    "scan": {
        "component": "Load_1",
        "parameter": "P",
        "values": [10, 20, 30]
    }
}

result = skill.run(config)

if result.status.value == "SUCCESS":
    data = result.data
    summary = data["summary"]
    print(f"扫描次数: {summary['total']}")
    print(f"成功: {summary['success']}")
    print(f"失败: {summary['failed']}")
```

### 检查详细结果

```python
result = skill.run(config)
data = result.data

for r in data["results"]:
    print(f"P = {r['value']}: {r['status']}")
    if r['status'] == 'success':
        print(f"  Job ID: {r['job_id']}")
```

### 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    if "component" in str(result.error):
        print("错误: 请检查component名称是否正确")
    elif "parameter" in str(result.error):
        print("错误: 请检查parameter名称是否正确")
```

## 输出结果

### JSON结果

```json
{
  "model_rid": "model/holdme/IEEE3",
  "scan": {
    "component": "Bus1_Load",
    "parameter": "P",
    "values": [10, 20, 30, 40, 50],
    "simulation_type": "power_flow"
  },
  "timestamp": "2024-03-24T14:32:01",
  "summary": {
    "total": 5,
    "success": 5,
    "failed": 0
  },
  "results": [
    {
      "value": 10,
      "status": "success",
      "job_id": "job_xxx",
      "converged": true
    },
    {
      "value": 20,
      "status": "success",
      "job_id": "job_yyy",
      "converged": true
    }
  ]
}
```

## 与其他技能的关联

```
param_scan
    ↓ (扫描结果)
result_compare, visualize
```

## 性能特点

- **执行时间**: 与扫描点数成正比
- **潮流模式**: 每个点约5-15秒
- **EMT模式**: 每个点约30-120秒
- **建议**: 扫描点数控制在20个以内

## 常用参数

### 负荷参数

| 元件类型 | 参数名 | 说明 |
|----------|--------|------|
| 负荷 | P | 有功功率 (MW) |
| 负荷 | Q | 无功功率 (MVar) |

### 发电机参数

| 元件类型 | 参数名 | 说明 |
|----------|--------|------|
| 发电机 | Vset | 电压设定值 (pu) |
| 发电机 | P | 有功出力 (MW) |

### 线路参数

| 元件类型 | 参数名 | 说明 |
|----------|--------|------|
| 线路 | R | 电阻 (pu) |
| 线路 | X | 电抗 (pu) |

## 常见问题

### 问题1: 找不到元件

**原因**: component名称错误或不存在

**解决**:
```python
# 先获取模型元件列表
model = Model.fetch("model/holdme/IEEE3")
components = model.getAllComponents()
for comp_id, comp in components.items():
    print(f"{comp_id}: {getattr(comp, 'name', 'N/A')}")
```

### 问题2: 参数修改失败

**原因**: 参数名错误或只读参数

**解决**: 确认参数名和可写性

### 问题3: 仿真不收敛

**原因**: 参数值超出合理范围

**解决**: 调整扫描范围
```yaml
scan:
  values: [10, 15, 20, 25, 30]  # 合理范围
```

## 配置示例

### 负荷扫描

```yaml
skill: param_scan
model:
  rid: model/holdme/IEEE3
scan:
  component: Bus1_Load
  parameter: P
  values: [50, 60, 70, 80, 90, 100]
  simulation_type: power_flow
```

### 电压设定扫描

```yaml
skill: param_scan
model:
  rid: model/holdme/IEEE39
scan:
  component: Generator_1
  parameter: Vset
  values: [0.95, 0.98, 1.0, 1.02, 1.05]
  simulation_type: power_flow
```

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
