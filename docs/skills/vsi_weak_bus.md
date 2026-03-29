# VSI弱母线分析技能 (VSI Weak Bus Analysis)

## 设计背景

### 研究对象
电压稳定是电力系统安全运行的重要指标。弱母线是指对无功变化敏感、容易发生电压崩溃的母线。VSI（Voltage Stability Index）通过测量母线对无功注入的响应来量化电压稳定性。

### 实际需求
在规划和运行中，需要识别系统中电压稳定性薄弱的母线，以便：
1. 确定无功补偿设备的安装位置
2. 评估系统电压稳定裕度
3. 指导运行方式调整
4. 预防电压崩溃事故

### 期望的输入和输出

**输入**:
- 电力系统模型（IEEE39等标准系统或实际系统）
- 测试母线筛选条件（电压范围、名称关键字等）
- 无功注入参数（注入量、开始时间、持续时间等）
- VSI判定阈值

**输出**:
- 各母线的VSI指标值
- 弱母线识别结果
- VSI分布统计
- 补偿建议

### 计算结果的用途和价值
VSI结果可直接指导无功补偿设计：
- VSI高的母线优先安装补偿设备
- 量化比较不同母线的稳定性
- 评估补偿前后的稳定性改善程度
- 为运行人员提供电压稳定预警

## 功能特性

- **动态无功注入**: 依次在各母线注入无功，测试电压响应
- **VSI指标计算**: 计算电压稳定指数（Voltage Stability Index）
- **弱母线识别**: 自动识别对无功变化敏感的薄弱母线
- **完整报告**: 生成JSON/CSV/Markdown多格式报告
- **批量测试**: 支持同时测试多条母线

## 快速开始

### 1. CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init vsi_weak_bus --output vsi.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config vsi.yaml
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("vsi_weak_bus")

# 配置
config = {
    "skill": "vsi_weak_bus",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "vsi_setup": {
        "bus_filter": {
            "v_min": 0.6,
            "v_max": 300
        },
        "injection": {
            "q_base": 100,
            "start_time": 8.0,
            "interval": 1.5,
            "duration": 0.5
        }
    },
    "analysis": {
        "vsi_threshold": 0.01,
        "top_n": 10
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "vsi_weak_bus",
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
print(f"数据: {result.data}")
```

### 3. YAML配置示例

```yaml
skill: vsi_weak_bus
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

vsi_setup:
  bus_filter:
    v_min: 0.6          # 最小电压筛选(kV)
    v_max: 300          # 最大电压筛选(kV)
  injection:
    q_base: 100         # 注入无功(MVar)
    start_time: 8.0     # 开始时间(s)
    interval: 1.5       # 每个母线测试时长(s)
    duration: 0.5       # 无功注入持续时间(s)

analysis:
  vsi_threshold: 0.01   # 弱母线VSI阈值
  top_n: 10             # 输出前N个弱母线

output:
  format: json
  path: ./results/
  prefix: vsi_weak_bus
  timestamp: true
```

## 配置Schema

### 完整配置结构

```yaml
skill: vsi_weak_bus                   # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token（不推荐）
  token_file: string                  # token文件路径（默认: .cloudpss_token）

model:                                # 模型配置（必需）
  rid: string                         # 模型RID或本地路径（必需）
  source: enum                        # cloud | local（默认: cloud）

vsi_setup:                            # VSI设置
  bus_filter:                         # 母线筛选
    v_min: number                     # 最小电压(kV)（默认: 0.6）
    v_max: number                     # 最大电压(kV)（默认: 300）
  injection:                          # 无功注入设置
    q_base: number                    # 注入无功(MVar)（默认: 100）
    start_time: number                # 开始时间(s)（默认: 8.0）
    interval: number                  # 测试间隔(s)（默认: 1.5）
    duration: number                  # 注入持续时间(s)（默认: 0.5）

analysis:                             # 分析配置
  vsi_threshold: number               # 弱母线阈值（默认: 0.01）
  top_n: integer                      # 输出前N个（默认: 10）

output:                               # 输出配置
  format: enum                        # json | csv（默认: json）
  path: string                        # 输出目录（默认: ./results/）
  prefix: string                      # 文件名前缀（默认: vsi_weak_bus）
  timestamp: boolean                  # 是否添加时间戳（默认: true）
```

### 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"vsi_weak_bus" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `vsi_setup.bus_filter.v_min` | number | 否 | 0.6 | 母线最小电压筛选(kV) |
| `vsi_setup.bus_filter.v_max` | number | 否 | 300 | 母线最大电压筛选(kV) |
| `vsi_setup.injection.q_base` | number | 否 | 100 | 注入无功功率(MVar) |
| `vsi_setup.injection.start_time` | number | 否 | 8.0 | 无功注入开始时间(s) |
| `vsi_setup.injection.interval` | number | 否 | 1.5 | 每个母线测试时长(s) |
| `vsi_setup.injection.duration` | number | 否 | 0.5 | 无功注入持续时间(s) |
| `analysis.vsi_threshold` | number | 否 | 0.01 | 弱母线VSI阈值 |
| `analysis.top_n` | integer | 否 | 10 | 输出前N个弱母线 |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | vsi_weak_bus | 文件名前缀 |
| `output.timestamp` | boolean | 否 | true | 文件名是否包含时间戳 |

## Agent使用指南

### 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("vsi_weak_bus")

# 最小化配置（使用默认值）
config = {
    "model": {"rid": "model/holdme/IEEE39"}
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status == "SUCCESS":
        print(f"分析完成: {result.data}")
    else:
        print(f"分析失败: {result.error}")
```

### 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data

    # 获取弱母线列表
    weak_buses = data.get("weak_buses", [])
    for bus in weak_buses:
        print(f"弱母线: {bus['label']}, VSI: {bus['vsi']}")

    # 获取统计信息
    summary = data.get("summary", {})
    print(f"总支线数: {summary.get('total_buses')}")
    print(f"弱母线数: {summary.get('weak_bus_count')}")

    # 访问输出文件
    for artifact in result.artifacts:
        print(f"输出文件: {artifact.path} ({artifact.type})")

# 查看日志
for log in result.logs:
    print(f"[{log.level}] {log.message}")
```

### 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    error_msg = result.error

    # 常见错误处理
    if "Token文件不存在" in error_msg:
        print("错误: 请创建.cloudpss_token文件")
    elif "模型不存在" in error_msg:
        print("错误: 请检查模型RID是否正确")
    elif "EMT拓扑检查失败" in error_msg:
        print("错误: 模型未配置EMT参数，先运行ieee3_prep")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### JSON输出格式

```json
{
  "model_rid": "model/holdme/IEEE39",
  "test_bus_count": 39,
  "vsi_results": {
    "vsi_i": {
      "Bus_16": 0.0152,
      "Bus_15": 0.0128,
      "Bus_26": 0.0115
    },
    "vsi_ij": {
      "Bus_16": {
        "Bus_16": 0.0152,
        "Bus_15": 0.0085,
        "Bus_26": 0.0072
      }
    }
  },
  "weak_buses": [
    {
      "label": "Bus_16",
      "vsi": 0.0152,
      "is_weak": true
    },
    {
      "label": "Bus_15",
      "vsi": 0.0128,
      "is_weak": true
    }
  ],
  "summary": {
    "total_buses": 39,
    "weak_bus_count": 5,
    "max_vsi": 0.0152,
    "min_vsi": 0.0021,
    "avg_vsi": 0.0065
  }
}
```

### SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "vsi_weak_bus" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典（包含vsi_results、weak_buses、summary） |
| `artifacts` | list | 输出文件列表（Artifact对象） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标 |

## 设计原理

### VSI计算公式

```
VSI_ij = (V_before - V_after) / Q_injected

VSI_i = mean(VSI_ij for all j)
```

其中：
- `V_before`: 注入无功前的电压
- `V_after`: 注入无功后的电压
- `Q_injected`: 注入的无功功率
- `i`: 注入无功的母线
- `j`: 观测电压变化的母线

### 物理意义

- **VSI越大**，表示母线对无功变化越敏感
- **VSI大的母线**电压稳定性差，容易发生电压崩溃
- **优先补偿**: VSI高的母线应优先安装无功补偿设备

### 工作流程

```
1. 筛选测试母线
   └── 按电压范围、名称关键字筛选

2. 添加VSI无功源
   └── 为每个母线添加shuntLC + 断路器 + 信号源

3. 配置时序
   └── 第k个母线在 T_start + k×interval 时刻注入无功

4. 运行EMT仿真
   └── 依次注入无功，记录电压变化

5. 计算VSI
   └── 提取电压变化，计算VSI指标

6. 识别弱母线
   └── 按VSI排序，输出薄弱母线列表
```

## 与其他技能的关联

```
power_flow
    ↓ (潮流结果)
vsi_weak_bus
    ↓ (VSI结果)
reactive_compensation_design
    ↓ (补偿方案)
disturbance_severity
    ↓ (验证效果)
结果对比
```

## 性能特点

- **仿真时间**: 与母线数量成正比，每个母线约1.5s
- **39母线系统**: 约需60s仿真时间
- **内存占用**: 中等，与系统规模成正比
- **适用规模**: 已测试至100母线系统
- **建议**: 对大型系统可先筛选关键母线

## VSI阈值建议

| VSI范围 | 稳定性评估 | 建议措施 |
|---------|-----------|----------|
| VSI > 0.015 | 非常薄弱 | 立即安装补偿设备 |
| 0.01 < VSI ≤ 0.015 | 薄弱 | 优先补偿 |
| 0.005 < VSI ≤ 0.01 | 中等 | 经济分析后决定 |
| VSI ≤ 0.005 | 良好 | 无需补偿 |

## 常见问题

### 问题1: EMT拓扑检查失败

**原因**: 模型未配置EMT拓扑

**解决**:
```bash
# 先运行ieee3_prep准备模型
python -m cloudpss_skills run --config config/ieee3_prep.yaml
```

### 问题2: 仿真时间过长

**原因**: 母线数量多或系统复杂

**解决**:
```yaml
vsi_setup:
  bus_filter:
    v_min: 200       # 只测试高压母线
    v_max: 300
analysis:
  top_n: 5           # 只输出最薄弱的5个
```

### 问题3: VSI计算异常

**原因**: 电压量测数据异常

**解决**: 检查仿真配置和结果输出，确保模型包含电压测量元件

## 完整示例

### 场景描述
某电力公司计划对IEEE39系统进行电压稳定性评估，识别需要安装无功补偿设备的母线。

### 配置文件

创建文件 `vsi_ieee39.yaml`:

```yaml
skill: vsi_weak_bus
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

vsi_setup:
  bus_filter:
    v_min: 0.6
    v_max: 300
  injection:
    q_base: 100
    start_time: 8.0
    interval: 1.5
    duration: 0.5

analysis:
  vsi_threshold: 0.01
  top_n: 10

output:
  format: json
  path: ./results/
  prefix: vsi_ieee39
  timestamp: true
```

### 执行命令

```bash
python -m cloudpss_skills run --config vsi_ieee39.yaml
```

### 预期输出

```
[14:32:01] [INFO] 加载认证信息...
[14:32:02] [INFO] 认证成功
[14:32:02] [INFO] 获取模型: IEEE39
[14:32:03] [INFO] 发现39条母线
[14:32:03] [INFO] 开始VSI分析...
[14:32:05] [INFO] [1/39] 测试母线 Bus_1...
[14:32:07] [INFO] [2/39] 测试母线 Bus_2...
...
[14:33:15] [INFO] [39/39] 测试母线 Bus_39...
[14:33:15] [INFO] VSI分析完成
[14:33:15] [INFO] 识别到5个弱母线
[14:33:15] [INFO] 结果已保存: ./results/vsi_ieee39_20240324_143315_result.json
[14:33:15] [INFO] 报告已保存: ./results/vsi_ieee39_20240324_143315_report.md

[OK] 技能执行成功: vsi_weak_bus
耗时: 72.5s
```

### 结果文件

**JSON结果** (`vsi_ieee39_20240324_143315_result.json`):

```json
{
  "model_rid": "model/holdme/IEEE39",
  "test_bus_count": 39,
  "vsi_results": {
    "vsi_i": {
      "Bus_16": 0.0152,
      "Bus_15": 0.0128,
      "Bus_26": 0.0115,
      "Bus_4": 0.0098,
      "Bus_12": 0.0085
    }
  },
  "weak_buses": [
    {
      "label": "Bus_16",
      "vsi": 0.0152,
      "is_weak": true
    },
    {
      "label": "Bus_15",
      "vsi": 0.0128,
      "is_weak": true
    },
    {
      "label": "Bus_26",
      "vsi": 0.0115,
      "is_weak": true
    }
  ],
  "summary": {
    "total_buses": 39,
    "weak_bus_count": 3,
    "max_vsi": 0.0152,
    "min_vsi": 0.0021,
    "avg_vsi": 0.0065
  }
}
```

**CSV汇总** (`vsi_ieee39_20240324_143315_result.csv`):

| 母线名称 | VSI | 是否弱母线 |
|----------|-----|-----------|
| Bus_16 | 0.015234 | 是 |
| Bus_15 | 0.012856 | 是 |
| Bus_26 | 0.011523 | 是 |
| Bus_4 | 0.009812 | 否 |
| Bus_12 | 0.008456 | 否 |

**Markdown报告** (`vsi_ieee39_20240324_143315_report.md`):
- 摘要统计
- 弱母线列表
- VSI分布表
- 补偿建议

### 后续应用

基于VSI结果，使用`reactive_compensation_design`技能设计无功补偿方案:

```bash
# 使用VSI结果设计补偿
python -m cloudpss_skills run --config reactive_compensation.yaml
```

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
