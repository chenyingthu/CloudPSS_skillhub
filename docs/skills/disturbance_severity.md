# 扰动严重度分析技能 (Disturbance Severity)

## 设计背景

### 研究对象

电力系统故障后的电压恢复特性是评估系统暂态电压稳定性的关键。扰动严重度分析通过计算DV（电压裕度）和SI（严重度指数）指标，量化评估故障对系统电压的影响程度和恢复特性。

### 实际需求

在电力系统规划和运行中，需要：

1. **电压恢复评估**：评估故障后电压能否恢复到允许范围
2. **薄弱点识别**：识别电压恢复能力差的母线或区域
3. **保护配置优化**：为低压保护、切负荷保护提供整定依据
4. **稳定性裕度评估**：量化系统的暂态电压稳定裕度
5. **改进措施评估**：评估无功补偿、控制策略改进的效果

### 期望的输入和输出

**输入**:
- 电力系统模型（IEEE39等）
- EMT仿真结果或仿真配置（故障位置、类型、时间）
- 分析参数（DV/SI使能、计算窗口、阈值）
- 输出配置（格式、路径、前缀）

**输出**:
- DV指标（电压上下限裕度）
- SI指标（严重度指数）
- 薄弱点识别结果
- 汇总统计信息
- 多格式报告（JSON/CSV/Markdown）

### 计算结果的用途和价值

分析结果可用于：
- 识别电压稳定薄弱环节
- 指导无功补偿设备配置
- 优化保护装置整定值
- 评估运行方式的安全性
- 支持系统规划决策

## 功能特性

- **DV分析**：计算电压上下限裕度，评估电压恢复能力
- **SI计算**：综合评估电压跌落深度和持续时间
- **薄弱点识别**：自动识别DV为负或SI较高的母线
- **多格式报告**：JSON/CSV/Markdown格式，便于后续处理
- **灵活配置**：支持自定义计算参数和判断阈值

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化扰动严重度分析配置
python -m cloudpss_skills init disturbance_severity --output disturbance.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config disturbance.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("disturbance_severity")

# 配置
config = {
    "skill": "disturbance_severity",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "simulation": {
        "fault_bus": "Bus_16",
        "fault_type": "three_phase",
        "fault_time": 4.0,
        "fault_duration": 0.1,
        "simulation_time": 10.0,
        "step_time": 0.0001
    },
    "analysis": {
        "dv_enabled": True,
        "si_enabled": True,
        "dudv_enabled": True,
        "voltage_measure_plot": 0,
        "pre_fault_window": 0.5,
        "judge_criteria": [
            [0.1, 3.0, 0.75, 1.25],
            [3.0, 999.0, 0.95, 1.05]
        ]
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "disturbance_severity"
    }
}

# 运行
result = skill.run(config)
print(f"分析完成: {result.data}")
```

### 3.3 YAML配置示例

```yaml
skill: disturbance_severity
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

simulation:
  fault_bus: Bus_16
  fault_type: three_phase
  fault_time: 4.0
  fault_duration: 0.1
  simulation_time: 10.0
  step_time: 0.0001

analysis:
  dv_enabled: true
  si_enabled: true
  dudv_enabled: true
  voltage_measure_plot: 0
  pre_fault_window: 0.5
  judge_criteria:
    - [0.1, 3.0, 0.75, 1.25]
    - [3.0, 999.0, 0.95, 1.05]

output:
  format: json
  path: ./results/
  prefix: disturbance_severity
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: disturbance_severity             # 必需: 技能名称
auth:                                   # 认证配置
  token_file: string                   # token文件路径

model:                                  # 模型配置（必需）
  rid: string                          # 模型RID或本地路径
  source: enum                         # cloud | local

simulation:                             # 仿真配置
  emt_result: string                   # 已有EMT结果Job ID（可选）
  fault_bus: string                    # 故障母线label
  fault_type: enum                     # three_phase | single_phase
  fault_time: number                   # 故障发生时间(s)
  fault_duration: number               # 故障持续时间(s)
  simulation_time: number              # 总仿真时间(s)
  step_time: number                    # 仿真步长(s)

analysis:                               # 分析配置
  dv_enabled: boolean                  # 启用DV计算
  si_enabled: boolean                  # 启用SI计算
  dudv_enabled: boolean                # 启用DUDV曲线
  voltage_measure_plot: integer        # 电压量测图索引
  pre_fault_window: number             # 故障前稳态窗口(s)
  judge_criteria:                      # DV判断条件
    - [t_start, t_end, v_min_ratio, v_max_ratio]
  si_interval: number                  # SI计算起始偏移(s)
  si_window: number                    # SI积分窗口(s)
  si_dv1: number                       # SI第一阶段电压偏差阈值
  si_dv2: number                       # SI第二阶段电压偏差阈值

output:                                 # 输出配置
  format: enum                         # json | csv
  path: string                         # 输出目录
  prefix: string                       # 文件名前缀
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"disturbance_severity" |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地路径 |
| `model.source` | enum | 否 | cloud | 模型来源: cloud/local |
| `simulation.emt_result` | string | 否 | - | 已有EMT结果Job ID |
| `simulation.fault_bus` | string | 条件 | - | 故障母线（运行新仿真时必需） |
| `simulation.fault_type` | enum | 否 | three_phase | 故障类型 |
| `simulation.fault_time` | number | 否 | 4.0 | 故障发生时间(s) |
| `simulation.fault_duration` | number | 否 | 0.1 | 故障持续时间(s) |
| `simulation.simulation_time` | number | 否 | 10.0 | 总仿真时间(s) |
| `analysis.dv_enabled` | boolean | 否 | true | 启用DV计算 |
| `analysis.si_enabled` | boolean | 否 | true | 启用SI计算 |
| `analysis.voltage_measure_plot` | integer | 否 | 0 | 电压量测图索引 |
| `analysis.pre_fault_window` | number | 否 | 0.5 | 故障前稳态窗口(s) |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录 |
| `output.prefix` | string | 否 | disturbance_severity | 文件名前缀 |

## Agent使用指南

### 5.1 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("disturbance_severity")

# 最小配置
config = {
    "model": {
        "rid": "model/holdme/IEEE39"
    },
    "simulation": {
        "fault_bus": "Bus_16",
        "fault_type": "three_phase"
    }
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

### 5.2 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data

    # 访问汇总统计
    summary = data.get("summary", {})
    print(f"总通道数: {summary.get('total_channels')}")
    print(f"薄弱点数: {len(data.get('weak_points', []))}")

    # 访问DV统计
    if 'dv_up' in summary:
        dv_up = summary['dv_up']
        print(f"DV上限裕度范围: [{dv_up['min']:.4f}, {dv_up['max']:.4f}]")
        print(f"DV上限不足数: {dv_up['negative_count']}")

    # 访问SI统计
    if 'si' in summary:
        si = summary['si']
        print(f"SI范围: [{si['min']:.4f}, {si['max']:.4f}]")

    # 访问薄弱点
    weak_points = data.get("weak_points", [])
    for wp in weak_points[:5]:  # 前5个薄弱点
        print(f"薄弱点: {wp['name']}, SI: {wp.get('si', 'N/A')}, 原因: {wp['reason']}")

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
    if "必须指定model配置" in error_msg:
        print("错误: 请配置model参数")
    elif "必须指定model.rid" in error_msg:
        print("错误: 请提供模型RID")
    elif "获取EMT结果失败" in error_msg:
        print("错误: 无法获取仿真结果，请检查模型和故障配置")
    elif "未能从结果中提取电压数据" in error_msg:
        print("错误: 仿真结果中没有电压数据")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "model_rid": "model/holdme/IEEE39",
  "disturbance_time": 4.0,
  "channel_count": 39,
  "channel_results": [
    {
      "name": "Bus_16_V",
      "dv_enabled": true,
      "si_enabled": true,
      "dv": {
        "dv_up": 0.0523,
        "dv_down": 0.1477,
        "v_steady": 1.0000
      },
      "si": 0.1523
    }
  ],
  "weak_points": [
    {
      "name": "Bus_16_V",
      "reason": "电压下限裕度不足 (-0.0234); 严重度指数较高 (SI=0.4521)",
      "dv_up": 0.0523,
      "dv_down": -0.0234,
      "si": 0.4521
    }
  ],
  "summary": {
    "total_channels": 39,
    "dv_analyzed": 39,
    "si_analyzed": 39,
    "dv_up": {
      "min": -0.0345,
      "max": 0.1523,
      "mean": 0.0789,
      "negative_count": 2
    },
    "dv_down": {
      "min": -0.0891,
      "max": 0.2345,
      "mean": 0.1234,
      "negative_count": 5
    },
    "si": {
      "min": 0.0123,
      "max": 0.4521,
      "mean": 0.1567,
      "high_count": 3
    }
  }
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "disturbance_severity" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 分析结果数据字典 |
| `artifacts` | list | 输出文件列表（JSON/CSV/Markdown） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标（duration, channel_count） |

## 设计原理

### 工作流程

```
1. 模型加载
   └── 获取CloudPSS模型

2. EMT仿真执行或获取
   ├── 如果提供emt_result: 直接获取结果
   └── 否则: 配置并运行新的EMT仿真
       └── 配置故障参数
       └── 执行仿真

3. 电压数据提取
   └── 从EMT结果中提取电压波形
   └── 识别所有母线电压通道

4. 分析计算
   ├── DV计算（如果启用）
   │   ├── 计算故障前稳态电压
   │   ├── 计算电压上下限裕度
   │   └── 判断是否满足判据
   └── SI计算（如果启用）
       ├── 计算电压偏差
       ├── 分段积分
       └── 得到严重度指数

5. 薄弱点识别
   └── 筛选DV为负或SI>0.5的母线
   └── 按SI排序

6. 报告生成
   ├── 生成JSON结果文件
   ├── 生成CSV汇总文件
   └── 生成Markdown报告
```

### 指标说明

**DV（电压裕度）**: 评估电压偏离稳态值的程度
- DV_up > 0: 电压未超过上限
- DV_down > 0: 电压未低于下限
- DV < 0: 电压越限，存在稳定风险

**SI（严重度指数）**: 综合评估电压跌落深度和持续时间
- SI < 0.1: 轻微扰动
- 0.1 <= SI < 0.5: 中等扰动
- SI >= 0.5: 严重扰动

## 与其他技能的关联

```
emt_simulation
    ↓ (EMT仿真结果)
disturbance_severity
    ↓ (分析结果)
    ├── reactive_compensation_design (无功补偿设计)
    ├── hdf5_export (HDF5格式导出)
    └── visualize (结果可视化)
```

**输入依赖**: 需要EMT仿真结果（通过emt_simulation技能或已有Job ID）
**输出被依赖**:
- `reactive_compensation_design`: 基于薄弱点设计无功补偿
- `hdf5_export`: 导出为标准HDF5格式
- `visualize`: 可视化DV/SI分布

## 性能特点

- **执行时间**: 包含EMT仿真时约1-3分钟，仅分析时约10-30秒
- **内存占用**: 与母线数量和数据点数成正比
- **计算精度**: DV精度0.0001，SI精度0.0001
- **适用规模**: 已测试至500母线系统

## 常见问题

### 问题1: EMT结果获取失败

**原因**:
- 仿真尚未完成
- 模型配置错误
- 故障参数不正确

**解决**:
```python
# 先确保EMT仿真成功完成
from cloudpss_skills import get_skill

emt_skill = get_skill("emt_simulation")
emt_result = emt_skill.run(emt_config)

# 然后使用已有结果进行分析
disturbance_config["simulation"]["emt_result"] = emt_result.data.get("job_id")
```

### 问题2: 无电压数据

**原因**: EMT结果中没有电压量测通道

**解决**:
```yaml
analysis:
  voltage_measure_plot: 0  # 检查波形分组索引是否正确
```

### 问题3: 薄弱点过多

**原因**: 判断阈值设置过严

**解决**:
```yaml
analysis:
  judge_criteria:
    - [0.1, 3.0, 0.70, 1.30]   # 放宽第一阶段判据
    - [3.0, 999.0, 0.90, 1.10]  # 放宽第二阶段判据
```

### 问题4: SI计算异常

**原因**: 仿真时间不足或故障时间设置不当

**解决**:
```yaml
simulation:
  fault_time: 4.0         # 确保故障前有足够稳态时间
  fault_duration: 0.1     # 合理的故障持续时间
  simulation_time: 10.0   # 确保故障后有足够恢复时间
```

### 问题5: 模型加载失败

**原因**: 模型RID错误或无权访问

**解决**:
```python
# 确认模型RID格式正确
config["model"]["rid"] = "model/holdme/IEEE39"

# 或使用本地模型
config["model"]["source"] = "local"
config["model"]["rid"] = "./models/ieee39.yaml"
```

## 完整示例

### 场景描述

某电力公司需要评估IEEE39系统在Bus_16母线发生三相短路故障后的电压恢复特性，识别电压稳定薄弱环节。

### 配置文件

```yaml
skill: disturbance_severity
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

simulation:
  fault_bus: Bus_16
  fault_type: three_phase
  fault_time: 4.0
  fault_duration: 0.1
  simulation_time: 10.0
  step_time: 0.0001

analysis:
  dv_enabled: true
  si_enabled: true
  dudv_enabled: true
  voltage_measure_plot: 0
  pre_fault_window: 0.5
  judge_criteria:
    - [0.1, 3.0, 0.75, 1.25]
    - [3.0, 999.0, 0.95, 1.05]
  si_interval: 0.11
  si_window: 3.0
  si_dv1: 0.25
  si_dv2: 0.1

output:
  format: json
  path: ./results/
  prefix: disturbance_ieee39_bus16
```

### 执行命令

```bash
python -m cloudpss_skills run --config disturbance_config.yaml
```

### 预期输出

```
[INFO] 扰动严重度分析开始 - 模型: model/holdme/IEEE39
[INFO] 成功获取EMT仿真结果
[INFO] 提取到 39 个电压通道
[INFO] 扰动严重度分析完成，耗时 25.34s
[INFO] 结果已保存: ./results/disturbance_ieee39_bus16_result.json
[INFO] 识别到 5 个薄弱点
```

### 结果文件

**JSON结果**: `./results/disturbance_ieee39_bus16_result.json`

```json
{
  "model_rid": "model/holdme/IEEE39",
  "disturbance_time": 4.0,
  "channel_count": 39,
  "weak_points": [
    {
      "name": "Bus_16_V",
      "reason": "电压下限裕度不足 (-0.0234); 严重度指数较高 (SI=0.4521)",
      "dv_up": 0.0523,
      "dv_down": -0.0234,
      "si": 0.4521
    },
    {
      "name": "Bus_15_V",
      "reason": "电压下限裕度不足 (-0.0156); 严重度指数较高 (SI=0.3891)",
      "dv_up": 0.0689,
      "dv_down": -0.0156,
      "si": 0.3891
    }
  ],
  "summary": {
    "total_channels": 39,
    "weak_bus_count": 5,
    "dv_up": {
      "min": -0.0345,
      "max": 0.1523,
      "mean": 0.0789,
      "negative_count": 2
    },
    "si": {
      "min": 0.0123,
      "max": 0.4521,
      "mean": 0.1567,
      "high_count": 3
    }
  }
}
```

**CSV汇总**: `./results/disturbance_ieee39_bus16_result.csv`

```csv
通道名称,DV上限裕度,DV下限裕度,稳态电压,SI严重度,是否薄弱
Bus_16_V,0.0523,-0.0234,1.0000,0.4521,是
Bus_15_V,0.0689,-0.0156,0.9987,0.3891,是
Bus_14_V,0.1234,0.0876,0.9956,0.1256,否
...
```

**Markdown报告**: `./results/disturbance_ieee39_bus16_report.md`

### 后续应用

1. **无功补偿设计**:
```python
from cloudpss_skills import get_skill

# 基于薄弱点进行无功补偿设计
compensation_skill = get_skill("reactive_compensation_design")
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "target_buses": ["Bus_16", "Bus_15"],  # 薄弱点母线
    "compensation_type": "svc"
}
compensation_skill.run(config)
```

2. **HDF5导出**:
```python
hdf5_skill = get_skill("hdf5_export")
config = {
    "source": {
        "type": "file",
        "file_path": "./results/disturbance_ieee39_bus16_result.json"
    },
    "output": {"filename": "disturbance_analysis.h5"}
}
hdf5_skill.run(config)
```

3. **可视化**:
```python
visualize_skill = get_skill("visualize")
# 绘制DV/SI分布图
```

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28, numpy >= 1.20.0
