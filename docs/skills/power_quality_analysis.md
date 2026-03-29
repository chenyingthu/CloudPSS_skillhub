# 电能质量分析技能 (Power Quality Analysis)

## 设计背景

### 研究对象

电能质量是指电力系统中电能的品质特性，包括电压、频率、波形等参数与理想状态的偏离程度。电能质量问题主要包括电压偏差、频率偏差、电压波动与闪变、三相不平衡、谐波畸变、暂态扰动等。电能质量分析技能用于综合评估电力系统的电能质量水平，识别电能质量问题及其严重程度，为电能质量治理和系统优化提供依据。

### 实际需求

在电力系统规划、设计、运行和监管中，电能质量分析具有以下重要作用：

1. **电能质量评估**: 全面评估系统电能质量水平，识别存在的问题
2. **标准符合性校核**: 验证电能质量指标是否满足GB/T 12325、GB/T 12326、GB/T 14549等国家标准
3. **污染源识别**: 定位电能质量问题的来源，如非线性负荷、冲击性负荷等
4. **治理方案设计**: 为电能质量治理设备（如SVG、APF、DVR等）的配置和设计提供数据支持
5. **运行优化**: 指导系统运行方式调整，改善电能质量
6. **用户接入评估**: 评估新负荷或新能源接入对系统电能质量的影响

### 期望的输入和输出

**输入**:
- 电力系统模型（标准系统或实际系统）
- 电能质量限值标准（电压偏差、频率偏差、THD、三相不平衡度等）
- 分析场景配置（正常运行、故障工况、负荷变化等）
- 评估母线/区域范围

**输出**:
- 电压质量指标（偏差、波动、闪变）
- 频率质量指标（偏差、变化率）
- 谐波畸变指标（THD、各次谐波含有率）
- 三相不平衡度指标
- 综合电能质量指数（PQI）
- 超标节点清单及严重程度排序
- 电能质量改善建议

### 计算结果的用途和价值

电能质量分析结果可直接用于：
- 评估系统电能质量是否满足国家标准要求
- 识别电能质量问题的优先级，制定治理计划
- 为新负荷接入或新能源并网提供电能质量影响评估
- 指导电能质量监测点的优化配置
- 为电能质量治理设备的投资决策提供依据
- 支持电能质量经济责任分摊和纠纷处理

## 功能特性

- **多维度分析**: 同时评估电压质量、频率质量、谐波质量、三相不平衡等多维度指标
- **标准自动校核**: 自动对比GB/T系列电能质量标准，标识超标项
- **综合指数计算**: 计算电能质量综合指数（PQI），量化整体电能质量水平
- **场景对比分析**: 支持不同运行场景（正常/N-1/故障）的电能质量对比
- **污染源定位**: 识别主要电能质量问题来源和受影响节点
- **趋势分析**: 支持多时段数据对比，分析电能质量变化趋势
- **可视化报告**: 自动生成电能质量评估报告和可视化图表

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init power_quality_analysis --output pqa.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config pqa.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("power_quality_analysis")

# 配置
config = {
    "skill": "power_quality_analysis",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "analysis": {
        "voltage_limits": {
            "min": 0.95,
            "max": 1.05
        },
        "frequency_limits": {
            "min": 49.5,
            "max": 50.5
        },
        "thd_limits": {
            "voltage": 0.05,
            "current": 0.08
        },
        "unbalance_limit": 0.02,
        "flicker_limit": 1.0
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "power_quality",
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

### 3.3 YAML配置示例

```yaml
skill: power_quality_analysis
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  voltage_limits:             # 电压偏差限值(pu)
    min: 0.95                 # 最低电压
    max: 1.05                 # 最高电压
  frequency_limits:           # 频率偏差限值(Hz)
    min: 49.5                 # 最低频率
    max: 50.5                 # 最高频率
  thd_limits:                 # 总谐波畸变率限值
    voltage: 0.05             # 电压THD(5%)
    current: 0.08             # 电流THD(8%)
  unbalance_limit: 0.02       # 三相不平衡度限值(2%)
  flicker_limit: 1.0          # 闪变限值(Pst=1.0)
  assessment_buses:           # 指定评估母线（可选，默认全部）
    - Bus_1
    - Bus_16
    - Bus_15

output:
  format: json
  path: ./results/
  prefix: power_quality
  timestamp: true
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: power_quality_analysis         # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token（不推荐）
  token_file: string                  # token文件路径（默认: .cloudpss_token）

model:                                # 模型配置（必需）
  rid: string                         # 模型RID或本地路径（必需）
  source: enum                        # cloud | local（默认: cloud）

analysis:                             # 分析配置（必需）
  voltage_limits:                     # 电压偏差限值
    min: number                       # 最低电压(pu)，默认0.95
    max: number                       # 最高电压(pu)，默认1.05
  frequency_limits:                   # 频率偏差限值
    min: number                       # 最低频率(Hz)，默认49.5
    max: number                       # 最高频率(Hz)，默认50.5
  thd_limits:                         # THD限值
    voltage: number                   # 电压THD，默认0.05
    current: number                   # 电流THD，默认0.08
  unbalance_limit: number             # 不平衡度限值，默认0.02
  flicker_limit: number               # 闪变限值，默认1.0
  assessment_buses: array             # 评估母线列表（可选）
  include_scenarios: array            # 包含的分析场景
    - normal                          # 正常运行
    - n1_contingency                  # N-1故障
    - peak_load                       # 高峰负荷

output:                               # 输出配置
  format: enum                        # json | csv | yaml（默认: json）
  path: string                        # 输出目录（默认: ./results/）
  prefix: string                      # 文件名前缀（默认: power_quality）
  timestamp: boolean                  # 是否添加时间戳（默认: true）
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"power_quality_analysis" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `analysis.voltage_limits.min` | number | 否 | 0.95 | 最低电压限值(pu) |
| `analysis.voltage_limits.max` | number | 否 | 1.05 | 最高电压限值(pu) |
| `analysis.frequency_limits.min` | number | 否 | 49.5 | 最低频率限值(Hz) |
| `analysis.frequency_limits.max` | number | 否 | 50.5 | 最高频率限值(Hz) |
| `analysis.thd_limits.voltage` | number | 否 | 0.05 | 电压THD限值(5%) |
| `analysis.thd_limits.current` | number | 否 | 0.08 | 电流THD限值(8%) |
| `analysis.unbalance_limit` | number | 否 | 0.02 | 三相不平衡度限值(2%) |
| `analysis.flicker_limit` | number | 否 | 1.0 | 闪变限值Pst |
| `analysis.assessment_buses` | array | 否 | [] | 指定评估母线，空数组表示全部母线 |
| `analysis.include_scenarios` | array | 否 | ["normal"] | 分析场景列表 |
| `output.format` | enum | 否 | json | 输出格式：json / csv / yaml |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | power_quality | 文件名前缀 |
| `output.timestamp` | boolean | 否 | true | 文件名是否包含时间戳 |

## Agent使用指南

### 5.1 基本调用模式

```python
# 获取技能实例
skill = get_skill("power_quality_analysis")

# 最小化配置（使用默认值）
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "analysis": {
        "voltage_limits": {"min": 0.95, "max": 1.05},
        "thd_limits": {"voltage": 0.05, "current": 0.08}
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

    # 访问电压质量结果
    voltage_quality = data.get("voltage_quality", {})
    for bus, v_data in voltage_quality.items():
        print(f"母线 {bus}: 电压={v_data['magnitude']:.4f}, 偏差={v_data['deviation']:.2%}")

    # 访问超标节点
    violations = data.get("violations", [])
    print(f"发现 {len(violations)} 个电能质量问题:")
    for v in violations:
        print(f"  - {v['bus']}: {v['type']} = {v['value']:.4f} (限值: {v['limit']:.4f})")

    # 访问综合电能质量指数
    pqi = data.get("power_quality_index", {})
    print(f"综合电能质量指数: {pqi.get('overall', 0):.2f}")

    # 访问输出文件
    for artifact in result.artifacts:
        print(f"输出文件: {artifact.path} ({artifact.type})")

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
    if "Token文件不存在" in error_msg:
        print("错误: 请创建.cloudpss_token文件")
    elif "模型不存在" in error_msg:
        print("错误: 请检查模型RID是否正确")
    elif "潮流不收敛" in error_msg:
        print("错误: 基础潮流计算不收敛，请检查系统数据")
    elif "评估母线不存在" in error_msg:
        print("错误: 请检查assessment_buses中配置的母线标签")
    elif "限值配置错误" in error_msg:
        print("错误: 请检查限值配置，max应大于min")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "model": "IEEE39",
  "model_rid": "model/holdme/IEEE39",
  "job_id": "job_xxx",
  "timestamp": "2024-03-24T14:32:01",
  "power_quality_index": {
    "overall": 85.2,
    "voltage_quality": 88.5,
    "frequency_quality": 95.0,
    "harmonic_quality": 82.3,
    "unbalance_quality": 90.1
  },
  "voltage_quality": {
    "Bus_1": {
      "magnitude": 1.0234,
      "deviation": 0.0234,
      "status": "normal"
    },
    "Bus_16": {
      "magnitude": 0.9821,
      "deviation": -0.0179,
      "status": "normal"
    }
  },
  "frequency_quality": {
    "mean_frequency": 50.02,
    "max_deviation": 0.08,
    "status": "normal"
  },
  "harmonic_quality": {
    "Bus_16": {
      "thd_voltage": 0.0389,
      "thd_current": 0.0456,
      "status": "warning"
    }
  },
  "unbalance": {
    "max_unbalance": 0.012,
    "status": "normal"
  },
  "violations": [
    {
      "bus": "Bus_16",
      "type": "voltage_thd",
      "value": 0.0389,
      "limit": 0.05,
      "severity": "warning"
    }
  ],
  "summary": {
    "total_buses": 39,
    "violation_count": 1,
    "warning_count": 2,
    "normal_count": 36
  }
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "power_quality_analysis" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典，包含各维度电能质量指标和综合指数 |
| `artifacts` | list | 输出文件列表（Artifact对象），包含JSON/CSV报告 |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标 |

## 设计原理

### 工作流程

```
1. 模型加载与初始化
   ├── 加载系统模型
   ├── 执行基础潮流计算
   └── 提取系统拓扑和参数

2. 电能质量指标计算
   ├── 电压质量分析
   │   ├── 计算各节点电压幅值
   │   ├── 计算电压偏差：(V_actual - V_nominal) / V_nominal
   │   ├── 识别电压越限节点
   │   └── 计算电压合格率
   ├── 频率质量分析
   │   ├── 计算系统频率
   │   ├── 计算频率偏差
   │   └── 评估频率稳定性
   ├── 谐波质量分析
   │   ├── 计算各节点电压THD
   │   ├── 计算各支路电流THD
   │   ├── 识别谐波超标节点
   │   └── 分析谐波分布特性
   └── 三相不平衡分析
       ├── 计算负序不平衡度
       ├── 计算零序不平衡度
       └── 识别不平衡严重节点

3. 标准符合性校核
   ├── 对比GB/T 12325（电压偏差）
   ├── 对比GB/T 12326（电压波动与闪变）
   ├── 对比GB/T 14549（谐波）
   └── 对比GB/T 15543（三相不平衡）

4. 综合指数计算
   ├── 各维度分项指数计算
   ├── 加权计算综合PQI
   └── 等级评定（优秀/良好/合格/不合格）

5. 结果汇总与输出
   ├── 生成超标节点清单
   ├── 按严重程度排序
   ├── 生成改善建议
   └── 输出JSON/CSV报告
```

### 电能质量指标定义

**电压偏差**:
```
电压偏差(%) = (V_actual - V_nominal) / V_nominal × 100%
```

**电压THD**:
```
THD_v = sqrt(sum(V_h^2)) / V_1 × 100%
```

**三相不平衡度**:
```
不平衡度 = |V_negative| / |V_positive| × 100%
```

**综合电能质量指数(PQI)**:
```
PQI = w1×电压指数 + w2×频率指数 + w3×谐波指数 + w4×不平衡指数
```

## 与其他技能的关联

```
power_flow
    ↓ (潮流结果)
harmonic_analysis
    ↓ (谐波数据)
power_quality_analysis
    ↓ (电能质量评估结果)
reactive_compensation_design / filter_design
    ↓ (治理方案)
emt_simulation
    ↓ (效果验证)
```

### 依赖关系

- **必需依赖**: CloudPSS SDK (`cloudpss`)
- **输入依赖**:
  - `power_flow`: 提供基础潮流数据
  - `harmonic_analysis`: 提供谐波分析数据（如启用谐波评估）
- **输出被依赖**:
  - `reactive_compensation_design`: 根据电能质量结果设计补偿方案
  - `filter_design`: 根据谐波超标情况设计滤波器

## 性能特点

- **执行时间**: IEEE39系统完整分析约15-30秒
- **内存占用**: 与系统规模和评估维度成正比
- **适用标准**: 支持GB/T系列电能质量标准
- **适用规模**: 已测试至500节点系统
- **多场景支持**: 可同时分析多个运行场景

## 常见问题

### 问题1: PQI计算结果偏低但无明显超标项

**原因**:
- 各单项指标虽然都合格，但接近限值
- 权重配置不合理
- 某些隐性指标（如闪变）影响综合评分

**解决**:
```yaml
analysis:
  # 调整限值，使其更严格
  voltage_limits:
    min: 0.97    # 从0.95收紧
    max: 1.03    # 从1.05收紧
  # 关注各单项指数的详细值
```

### 问题2: 谐波分析结果与单独运行harmonic_analysis不一致

**原因**:
- power_quality_analysis使用的是简化谐波计算
- 谐波源配置不同
- 计算精度设置不同

**解决**:
- 如需精确谐波分析，请单独使用`harmonic_analysis`技能
- 确保谐波源配置一致
- 以`harmonic_analysis`结果为准

### 问题3: 某些母线缺少电能质量数据

**原因**:
- 该母线未配置量测
- 母线为平衡节点或PV节点，无负荷
- 数据提取失败

**解决**:
- 检查模型中各母线的类型和配置
- 使用`assessment_buses`指定需要评估的母线
- 检查模型数据完整性

### 问题4: N-1场景分析耗时过长

**原因**:
- N-1场景数量多（N条线路+N台发电机）
- 每个场景都需要完整计算
- 系统规模大

**解决**:
```yaml
analysis:
  include_scenarios:
    - normal          # 只分析正常场景
  # 或使用关键场景筛选
  critical_contingencies:  # 只分析关键N-1场景
    - Line_1
    - Line_2
```

## 完整示例

### 场景描述

某电力公司需要对IEEE39标准系统进行全面的电能质量评估，以确定是否满足国标要求。评估内容包括电压偏差、谐波畸变率、三相不平衡度等，同时需要分析系统在N-1故障条件下的电能质量表现。

### 配置文件

```yaml
skill: power_quality_analysis
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

analysis:
  voltage_limits:
    min: 0.95
    max: 1.05
  frequency_limits:
    min: 49.5
    max: 50.5
  thd_limits:
    voltage: 0.05
    current: 0.08
  unbalance_limit: 0.02
  flicker_limit: 1.0
  assessment_buses:  # 重点评估母线
    - Bus_1
    - Bus_16
    - Bus_15
    - Bus_21
    - Bus_39
  include_scenarios:
    - normal
    - n1_contingency

output:
  format: json
  path: ./results/
  prefix: pq_assessment_ieee39
  timestamp: true
```

### 执行命令

```bash
python -m cloudpss_skills run --config power_quality_analysis.yaml
```

### 预期输出

```
[INFO] 加载认证信息...
[INFO] 认证成功
[INFO] 获取模型: IEEE39
[INFO] 开始电能质量分析...
[INFO] 分析场景: normal
[INFO] 计算电压质量指标...
[INFO] 计算谐波质量指标...
[INFO] 计算三相不平衡度...
[INFO] 分析场景: n1_contingency
[INFO] 完成N-1场景分析(46个场景)
[INFO] 计算综合电能质量指数...
[INFO] 发现1个电能质量问题
[INFO] 结果已保存: ./results/pq_assessment_ieee39_20240324_143245_result.json
[INFO] 报告已保存: ./results/pq_assessment_ieee39_20240324_143245_report.csv
```

### 结果文件

**JSON结果文件** (`pq_assessment_ieee39_20240324_143245_result.json`):

```json
{
  "model": "IEEE39",
  "model_rid": "model/holdme/IEEE39",
  "job_id": "job_pqa_xxx",
  "timestamp": "2024-03-24T14:32:45",
  "power_quality_index": {
    "overall": 85.2,
    "voltage_quality": 88.5,
    "frequency_quality": 95.0,
    "harmonic_quality": 82.3,
    "unbalance_quality": 90.1,
    "grade": "良好"
  },
  "voltage_quality": {
    "Bus_16": {
      "magnitude": 0.9821,
      "deviation": -0.0179,
      "status": "normal",
      "nominal": 1.0
    }
  },
  "violations": [
    {
      "bus": "Bus_16",
      "type": "voltage_thd",
      "value": 0.0389,
      "limit": 0.05,
      "severity": "warning",
      "scenario": "normal"
    }
  ],
  "summary": {
    "total_buses": 39,
    "assessed_buses": 5,
    "violation_count": 1,
    "warning_count": 2,
    "normal_count": 36,
    "scenarios_analyzed": 2
  }
}
```

**CSV报告文件** (`pq_assessment_ieee39_20240324_143245_report.csv`):

```csv
Bus,Voltage_Mag,Voltage_Deviation,Voltage_Status,THD_Voltage,THD_Status,Unbalance,Overall_Status
Bus_1,1.0234,2.34%,normal,0.0152,normal,0.008,normal
Bus_16,0.9821,-1.79%,normal,0.0389,warning,0.012,warning
Bus_15,0.9912,-0.88%,normal,0.0345,normal,0.010,normal
...
```

### 后续应用

基于电能质量分析结果，可以进行以下后续分析：

1. **谐波治理**: 如存在谐波超标，使用`filter_design`技能设计无源滤波器
2. **无功补偿**: 如存在电压偏差问题，使用`reactive_compensation_design`技能设计补偿方案
3. **效果验证**: 在实施治理措施后，重新运行电能质量分析验证效果
4. **趋势分析**: 定期运行分析，建立电能质量档案，分析变化趋势

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
