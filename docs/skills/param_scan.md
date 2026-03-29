# 参数扫描技能 (Parameter Scan)

## 设计背景

### 研究对象
参数扫描技能用于对电力系统中指定元件的参数进行批量变化，运行多次仿真，分析参数变化对系统稳态特性的影响。这是电力系统灵敏度分析和参数优化设计的基础工具。

### 实际需求
在电力系统分析和设计中，经常需要研究以下问题：
1. **负荷变化影响**：负荷功率变化对系统电压和潮流分布的影响
2. **发电机出力调整**：发电机有功/无功出力变化对系统稳定性的影响
3. **变压器分接头调节**：变压器变比变化对电压水平的影响
4. **线路参数灵敏度**：线路阻抗变化对网损和潮流的影响
5. **参数优化设计**：寻找最优的参数配置以满足特定约束

### 期望的输入和输出

**输入**：
- 电力系统模型（云端RID或本地YAML文件）
- 目标元件标识（元件ID或名称）
- 待扫描的参数名称
- 参数值列表（扫描范围）
- 仿真类型（潮流计算或EMT暂态仿真）

**输出**：
- 每个参数值对应的仿真结果
- 收敛状态统计
- JSON格式的扫描结果汇总
- 参数-响应关系数据

### 计算结果的用途和价值
参数扫描结果可用于：
- 识别系统对特定参数的灵敏度
- 确定参数的合理运行范围
- 验证系统的鲁棒性
- 指导运行方式调整
- 为参数优化提供数据基础

## 功能特性

- **灵活参数扫描**：支持对任意元件的任意可写参数进行扫描
- **双仿真模式**：支持潮流计算（稳态）和EMT暂态仿真两种模式
- **自动参数修改**：自动修改元件参数并运行仿真
- **收敛状态追踪**：记录每次仿真的收敛/完成状态
- **结果汇总统计**：自动统计成功/失败次数
- **智能元件匹配**：支持通过ID或名称匹配目标元件
- **模型隔离**：每次扫描重新加载模型，确保参数独立性

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init param_scan --output scan.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config scan.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("param_scan")

# 配置
config = {
    "skill": "param_scan",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE3",
        "source": "cloud"
    },
    "scan": {
        "component": "Bus1_Load",      # 元件ID或名称
        "parameter": "P",               # 参数名
        "values": [10, 20, 30, 40, 50], # 扫描值列表
        "simulation_type": "power_flow" # power_flow | emt
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "param_scan",
        "timestamp": True
    }
}

# 验证配置
validation = skill.validate(config)
if not validation.valid:
    print("配置错误:", validation.errors)

# 运行
result = skill.run(config)
print(f"状态: {result.status}")
print(f"扫描统计: {result.data.get('summary', {})}")
```

### 3.3 YAML配置示例

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

### 4.1 完整配置结构

```yaml
skill: param_scan                    # 必需: 技能名称
auth:                                # 认证配置
  token: string                      # 直接提供token（不推荐）
  token_file: string                 # token文件路径（默认: .cloudpss_token）

model:                               # 模型配置（必需）
  rid: string                        # 模型RID或本地路径（必需）
  source: enum                       # cloud | local（默认: cloud）

scan:                                # 扫描配置（必需）
  component: string                  # 元件ID或名称（必需）
  parameter: string                  # 参数名（必需）
  values: array                      # 参数值列表，number数组（必需）
  simulation_type: enum              # power_flow | emt（默认: power_flow）

output:                              # 输出配置
  format: enum                       # json | csv（默认: json）
  path: string                       # 输出目录（默认: ./results/）
  prefix: string                     # 文件名前缀（默认: param_scan）
  timestamp: boolean                 # 是否添加时间戳（默认: true）
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"param_scan" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `scan.component` | string | 是 | - | 元件ID或名称 |
| `scan.parameter` | string | 是 | - | 参数名（如P, Q, Vset等） |
| `scan.values` | array | 是 | - | 参数值列表（number数组） |
| `scan.simulation_type` | enum | 否 | power_flow | 仿真类型：power_flow(潮流) / emt(暂态) |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | param_scan | 文件名前缀 |
| `output.timestamp` | boolean | 否 | true | 文件名是否包含时间戳 |

## Agent使用指南

### 5.1 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("param_scan")

# 配置
config = {
    "model": {"rid": "model/holdme/IEEE3"},
    "scan": {
        "component": "Load_1",
        "parameter": "P",
        "values": [50, 60, 70, 80, 90, 100],
        "simulation_type": "power_flow"
    }
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status.value == "SUCCESS":
        summary = result.data.get("summary", {})
        print(f"扫描完成: {summary['success']}/{summary['total']} 成功")
    else:
        print(f"扫描失败: {result.error}")
```

### 5.2 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data

    # 访问扫描配置
    scan_config = data.get("scan", {})
    print(f"扫描参数: {scan_config['component']}.{scan_config['parameter']}")
    print(f"扫描值: {scan_config['values']}")

    # 访问汇总统计
    summary = data.get("summary", {})
    print(f"总扫描数: {summary['total']}")
    print(f"成功: {summary['success']}")
    print(f"失败: {summary['failed']}")

    # 访问详细结果
    for r in data.get("results", []):
        print(f"Value = {r['value']}: {r['status']}")
        if r['status'] == 'success':
            print(f"  Job ID: {r['job_id']}, 收敛: {r['converged']}")

    # 访问输出文件
    for artifact in result.artifacts:
        print(f"输出文件: {artifact.path}")

# 查看日志
for log in result.logs:
    print(f"[{log.level}] {log.message}")
```

### 5.3 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    error_msg = result.error

    # 常见错误处理
    if "component" in error_msg.lower():
        print("错误: 找不到指定的元件")
        print("  - 请确认元件ID或名称正确")
        print("  - 使用 model.getAllComponents() 查看可用元件")
    elif "parameter" in error_msg.lower():
        print("错误: 参数名错误或参数只读")
        print("  - 请确认参数名正确")
        print("  - 某些参数可能不允许修改")
    elif "Token文件不存在" in error_msg:
        print("错误: 请创建.cloudpss_token文件")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "model_rid": "model/holdme/IEEE3",
  "scan": {
    "component": "Bus1_Load",
    "parameter": "P",
    "values": [50, 60, 70, 80, 90, 100],
    "simulation_type": "power_flow"
  },
  "timestamp": "2024-03-24T14:32:01",
  "summary": {
    "total": 6,
    "success": 5,
    "failed": 1
  },
  "results": [
    {
      "value": 50,
      "status": "success",
      "job_id": "job_xxx",
      "converged": true
    },
    {
      "value": 60,
      "status": "success",
      "job_id": "job_yyy",
      "converged": true
    },
    {
      "value": 100,
      "status": "failed",
      "job_id": "job_zzz",
      "converged": false
    }
  ]
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "param_scan" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典，包含scan配置、summary和results |
| `artifacts` | list | 输出文件列表（Artifact对象） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标（total_scans, success, failed） |

## 设计原理

### 工作流程

```
1. 配置加载与验证
   └── 验证scan.component非空
   └── 验证scan.parameter非空
   └── 验证scan.values非空且为数组

2. 认证初始化
   └── 读取token文件或直接获取token
   └── 调用setToken完成认证

3. 参数扫描循环
   对于values中的每个值:
   ├── 重新加载模型（确保参数独立性）
   ├── 查找目标元件（先匹配ID，再匹配名称）
   ├── 修改元件参数（使用updateComponent API）
   ├── 运行仿真（power_flow或emt）
   ├── 轮询等待完成
   └── 记录结果（value, status, job_id, converged）

4. 结果汇总
   └── 统计成功/失败次数
   └── 计算成功率

5. 文件导出
   └── 生成JSON结果文件
```

### 参数修改机制

使用CloudPSS SDK的`updateComponent` API修改元件参数：

```python
model.updateComponent(
    target_comp.id,
    args={param_name: {"source": str(value), "ɵexp": ""}}
)
```

**注意**：每次扫描都重新加载模型，确保各扫描点之间的参数独立性。

## 与其他技能的关联

```
param_scan (参数扫描)
    ↓ (生成多组参数结果)
result_compare (结果对比)
    ↓ (对比不同参数下的结果)
visualize (可视化)
    ↓ (绘制参数-响应曲线)
reactive_compensation_design (补偿设计)
```

**依赖关系**：
- **输入依赖**：无（直接使用模型）
- **输出被依赖**：
  - `result_compare`: 对比不同参数设置的结果
  - `visualize`: 可视化参数扫描结果
  - `batch_powerflow`: 可作为批量分析的一部分

**常用参数组合**：

| 元件类型 | 参数名 | 说明 | 典型范围 |
|----------|--------|------|----------|
| 负荷 | P | 有功功率 (MW) | 50-150 |
| 负荷 | Q | 无功功率 (MVar) | 10-50 |
| 发电机 | Vset | 电压设定值 (pu) | 0.95-1.05 |
| 发电机 | P | 有功出力 (MW) | 根据容量 |
| 线路 | R | 电阻 (pu) | 根据线路 |
| 线路 | X | 电抗 (pu) | 根据线路 |
| 变压器 | ratio | 变比 | 0.9-1.1 |

## 性能特点

- **执行时间**：与扫描点数成正比
  - 潮流模式：每个点约5-15秒
  - EMT模式：每个点约30-120秒
- **扫描点数建议**：
  - 潮流扫描：建议控制在20个点以内
  - EMT扫描：建议控制在10个点以内
- **模型隔离**：每次扫描重新加载模型，保证结果独立性
- **内存占用**：同时只加载一个模型副本
- **失败处理**：单个扫描点失败不影响后续扫描

## 常见问题

### 问题1: 找不到元件

**原因**：
- component名称错误或不存在
- 元件ID格式不正确

**解决**：
```python
from cloudpss import Model

# 先获取模型元件列表
model = Model.fetch("model/holdme/IEEE3")
components = model.getAllComponents()
for comp_id, comp in components.items():
    comp_name = getattr(comp, 'name', 'N/A')
    print(f"ID: {comp_id}, Name: {comp_name}")

# 使用正确的ID或名称配置扫描
config = {
    "scan": {
        "component": "Bus1_Load",  # 使用ID或名称
        "parameter": "P",
        "values": [50, 60, 70]
    }
}
```

### 问题2: 参数修改失败

**原因**：
- 参数名错误
- 参数为只读参数
- 参数值超出有效范围

**解决**：
```python
# 确认参数名正确
# 检查元件的参数定义
component = model.getComponent("Bus1_Load")
args = getattr(component, 'args', {})
for param_name, param_config in args.items():
    print(f"参数: {param_name}, 配置: {param_config}")
```

### 问题3: 仿真不收敛

**原因**：
- 参数值超出合理范围
- 系统运行条件恶化

**解决**：
```yaml
# 调整扫描范围
scan:
  values: [10, 15, 20, 25, 30]  # 合理范围

# 或使用更小的步长
scan:
  values: [50, 55, 60, 65, 70]  # 小步长变化
```

### 问题4: EMT仿真扫描时间过长

**原因**：
- EMT仿真本身计算量大
- 扫描点数过多
- 仿真时长设置过长

**解决**：
```yaml
# 减少扫描点数
scan:
  values: [0.01, 0.1, 1.0]  # 关键点扫描
  simulation_type: emt

# 或者分批次执行
```

## 完整示例

### 场景描述
某电力系统运行部门需要分析IEEE3系统中Bus1负荷有功功率变化对系统电压的影响，确定系统的负荷承载能力。

### 配置文件

```yaml
skill: param_scan
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

scan:
  component: Bus1_Load    # 负荷元件名称
  parameter: P            # 有功功率参数
  values: [50, 60, 70, 80, 90, 100, 110, 120]  # 从50MW扫描到120MW
  simulation_type: power_flow

output:
  format: json
  path: ./results/
  prefix: load_sensitivity
  timestamp: true
```

### 执行命令

```bash
# 创建输出目录
mkdir -p ./results

# 执行参数扫描
python -m cloudpss_skills run --config load_scan.yaml
```

### 预期输出

```
[INFO] 加载认证信息...
[INFO] 认证成功
[INFO] 获取模型...
[INFO] 参数扫描: Bus1_Load.P
[INFO] 扫描值: [50, 60, 70, 80, 90, 100, 110, 120]
[INFO] 仿真类型: power_flow
[INFO] [1/8] P = 50
[INFO]   -> 已设置 P = 50
[INFO]   -> 仿真成功 (5s)
[INFO] [2/8] P = 60
[INFO]   -> 已设置 P = 60
[INFO]   -> 仿真成功 (5s)
...
[INFO] [7/8] P = 110
[INFO]   -> 已设置 P = 110
[INFO]   -> 仿真成功 (6s)
[INFO] [8/8] P = 120
[INFO]   -> 已设置 P = 120
[INFO]   -> 仿真未收敛 (120s, status=2)
[INFO] ==================================================
[INFO] 参数扫描完成: 8 次仿真
[INFO] 结果已保存: ./results/load_sensitivity_20240324_143245.json
```

### 结果文件

**JSON结果文件** (`load_sensitivity_20240324_143245.json`):
```json
{
  "model_rid": "model/holdme/IEEE3",
  "scan": {
    "component": "Bus1_Load",
    "parameter": "P",
    "values": [50, 60, 70, 80, 90, 100, 110, 120],
    "simulation_type": "power_flow"
  },
  "timestamp": "2024-03-24T14:32:45",
  "summary": {
    "total": 8,
    "success": 7,
    "failed": 1
  },
  "results": [
    {"value": 50, "status": "success", "job_id": "job_001", "converged": true},
    {"value": 60, "status": "success", "job_id": "job_002", "converged": true},
    {"value": 70, "status": "success", "job_id": "job_003", "converged": true},
    {"value": 80, "status": "success", "job_id": "job_004", "converged": true},
    {"value": 90, "status": "success", "job_id": "job_005", "converged": true},
    {"value": 100, "status": "success", "job_id": "job_006", "converged": true},
    {"value": 110, "status": "success", "job_id": "job_007", "converged": true},
    {"value": 120, "status": "failed", "job_id": "job_008", "converged": false}
  ]
}
```

### 后续应用

基于参数扫描结果，可以：
1. 使用 `result_compare` 对比不同负荷水平下的系统状态
2. 使用 `visualize` 绘制负荷-电压特性曲线
3. 结合 `voltage_stability` 进行更详细的电压稳定性分析
4. 使用 `reactive_compensation_design` 设计无功补偿方案以提高负荷承载能力

**分析结论**：从结果可以看出，当Bus1负荷有功功率增加到120MW时潮流不收敛，说明系统的负荷承载能力在110-120MW之间。

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
