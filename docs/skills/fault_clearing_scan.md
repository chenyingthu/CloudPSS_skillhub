# 故障清除时间扫描技能 (Fault Clearing Scan)

## 设计背景

### 研究对象
故障清除时间扫描技能用于分析不同故障清除时间对电力系统暂态稳定性的影响，确定系统的临界清除时间（Critical Clearing Time, CCT）。这是电力系统保护配合和稳定性评估的重要分析手段。

### 实际需求
在电力系统规划和运行中，需要解决以下问题：
1. **保护定值整定**：确定断路器的最大允许跳闸时间
2. **暂态稳定评估**：评估系统在不同故障清除时间下的稳定性
3. **临界时间确定**：找到系统能够保持稳定的极限清除时间
4. **保护配合验证**：验证各级保护的动作时间配合是否满足稳定要求
5. **系统强弱评估**：通过临界清除时间评估系统的稳定裕度

### 期望的输入和输出

**输入**：
- 电力系统EMT模型（云端RID或本地YAML文件）
- 故障开始时间（fs）
- 故障结束时间扫描值列表（fe_values）
- 故障电阻（chg）
- 电压评估参数（trace_name, study_time）

**输出**：
- 每个清除时间对应的研究时刻电压
- 电压恢复趋势分析
- 单调恶化判断
- JSON和CSV格式的详细结果
- Markdown格式的分析报告

### 计算结果的用途和价值
故障清除时间扫描结果可用于：
- 确定保护装置的最大允许动作时间
- 评估系统的暂态稳定裕度
- 指导保护定值的整定
- 验证系统的故障恢复能力
- 为系统规划和运行提供稳定性边界

## 功能特性

- **清除时间扫描**：扫描多个故障清除时间点
- **电压恢复评估**：在指定研究时刻提取电压值
- **趋势分析**：自动判断电压是否单调恶化
- **多格式输出**：支持JSON、CSV和Markdown报告
- **EMT暂态仿真**：基于详细的电磁暂态模型
- **灵活配置**：支持自定义故障时间和评估参数
- **自动报告生成**：生成详细的扫描分析报告

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init fault_clearing_scan --output clearing_scan.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config clearing_scan.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("fault_clearing_scan")

# 配置
config = {
    "skill": "fault_clearing_scan",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE3",
        "source": "cloud"
    },
    "scan": {
        "fs": 2.5,                           # 故障开始时间(s)
        "fe_values": [2.70, 2.75, 2.80, 2.85, 2.90],  # 清除时间扫描值
        "chg": 0.01                          # 故障电阻
    },
    "assessment": {
        "trace_name": "vac:0",               # 评估电压通道
        "study_time": 2.95                   # 研究时刻(s)
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "clearing_scan",
        "generate_report": True
    }
}

# 运行
result = skill.run(config)
print(f"状态: {result.status}")
print(f"单调恶化: {result.data.get('monotonic_degradation', False)}")
```

### 3.3 YAML配置示例

```yaml
skill: fault_clearing_scan
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

scan:
  fs: 2.5                              # 故障开始时间(s)
  fe_values: [2.70, 2.75, 2.80, 2.85, 2.90]  # 清除时间扫描值(s)
  chg: 0.01                            # 故障电阻

assessment:
  trace_name: "vac:0"                  # 评估电压通道名称
  study_time: 2.95                     # 研究时刻(s)

output:
  format: json
  path: ./results/
  prefix: clearing_scan
  generate_report: true
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: fault_clearing_scan            # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token（不推荐）
  token_file: string                  # token文件路径（默认: .cloudpss_token）

model:                                # 模型配置（必需）
  rid: string                         # 模型RID或本地路径（必需）
  source: enum                        # cloud | local（默认: cloud）

scan:                                 # 扫描配置（必需）
  fs: number                          # 故障开始时间(s)（默认: 2.5）
  fe_values: array                    # 故障结束时间扫描值列表，number数组（必需）
  chg: number                         # 故障电阻（默认: 0.01）

assessment:                           # 评估配置
  trace_name: string                  # 评估电压通道名称（默认: vac:0）
  study_time: number                  # 研究时刻(s)（默认: 2.95）

output:                               # 输出配置
  format: enum                        # json | csv（默认: json）
  path: string                        # 输出目录（默认: ./results/）
  prefix: string                      # 文件名前缀（默认: fault_clearing_scan）
  generate_report: boolean            # 是否生成报告（默认: true）
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"fault_clearing_scan" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `scan.fs` | number | 否 | 2.5 | 故障开始时间(s) |
| `scan.fe_values` | array | 是 | - | 故障结束时间扫描值列表(s) |
| `scan.chg` | number | 否 | 0.01 | 故障电阻(Ω) |
| `assessment.trace_name` | string | 否 | vac:0 | 评估电压通道名称 |
| `assessment.study_time` | number | 否 | 2.95 | 研究时刻(s) |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | fault_clearing_scan | 文件名前缀 |
| `output.generate_report` | boolean | 否 | true | 是否生成Markdown报告 |

## Agent使用指南

### 5.1 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("fault_clearing_scan")

# 配置
config = {
    "model": {"rid": "model/holdme/IEEE3"},
    "scan": {
        "fs": 2.5,
        "fe_values": [2.70, 2.75, 2.80, 2.85, 2.90],
        "chg": 0.01
    },
    "assessment": {
        "trace_name": "vac:0",
        "study_time": 2.95
    }
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status.value == "SUCCESS":
        print(f"扫描完成: {len(result.data['results'])} 个点")
    else:
        print(f"扫描失败: {result.error}")
```

### 5.2 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data

    # 访问模型信息
    print(f"模型: {data['model']}")
    print(f"研究时刻: {data['study_time']}s")

    # 访问趋势分析
    print(f"单调恶化: {data['monotonic_degradation']}")

    # 访问详细结果
    for r in data.get("results", []):
        print(f"清除时间 fe={r['fe']}s: 电压={r['voltage_at_study']:.4f} pu")

    # 查找临界清除时间
    results = data.get("results", [])
    for i in range(len(results) - 1):
        if results[i]["voltage_at_study"] > 0.8 and results[i+1]["voltage_at_study"] < 0.8:
            print(f"临界清除时间约在 {results[i]['fe']}s 到 {results[i+1]['fe']}s 之间")

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
    elif "EMT仿真失败" in error_msg:
        print("错误: EMT仿真失败，可能是系统不稳定或模型配置错误")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "model": "IEEE3",
  "study_time": 2.95,
  "monotonic_degradation": true,
  "results": [
    {
      "fe": 2.70,
      "voltage_at_study": 0.9823,
      "job_id": "job_xxx"
    },
    {
      "fe": 2.75,
      "voltage_at_study": 0.9541,
      "job_id": "job_yyy"
    },
    {
      "fe": 2.80,
      "voltage_at_study": 0.8912,
      "job_id": "job_zzz"
    },
    {
      "fe": 2.85,
      "voltage_at_study": 0.7234,
      "job_id": "job_aaa"
    },
    {
      "fe": 2.90,
      "voltage_at_study": 0.4521,
      "job_id": "job_bbb"
    }
  ]
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "fault_clearing_scan" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典，包含model、study_time、monotonic_degradation、results |
| `artifacts` | list | 输出文件列表（JSON、CSV、Markdown报告） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标 |

## 设计原理

### 工作流程

```
1. 配置加载与验证
   └── 验证model.rid存在
   └── 验证scan.fe_values非空且为数组

2. 认证初始化
   └── 读取token文件或直接获取token
   └── 调用setToken完成认证

3. 获取基础模型
   └── 获取模型副本（用于克隆）
   └── 查找故障元件

4. 清除时间扫描循环
   对于fe_values中的每个清除时间:
   ├── 克隆基础模型
   ├── 配置故障参数（fs, fe, chg）
   ├── 运行EMT仿真
   ├── 等待仿真完成
   ├── 提取研究时刻电压
   └── 记录结果（fe, voltage_at_study, job_id）

5. 趋势分析
   └── 判断电压是否单调下降

6. 文件导出
   └── 生成JSON结果文件
   └── 生成CSV结果文件
   └── 生成Markdown分析报告
```

### 关键概念

**故障时间参数**：
- `fs` (fault start)：故障开始时间，单位秒
- `fe` (fault end)：故障结束/清除时间，单位秒
- `chg` (change)：故障电阻，单位欧姆

**评估方法**：
- 在指定研究时刻（study_time）提取电压值
- 比较不同清除时间下的电压恢复水平
- 电压恢复越好，说明该清除时间越能满足稳定要求

## 与其他技能的关联

```
emt_simulation (基础EMT仿真)
    ↓ (扩展为扫描)
fault_clearing_scan
    ↓ (确定临界清除时间)
protection_coordination (保护配合)
    ↓ (整定保护定值)
transient_stability (暂态稳定分析)
```

**依赖关系**：
- **输入依赖**：`ieee3_prep` 或类似的模型准备技能（确保模型有故障元件）
- **输出被依赖**：
  - `visualize`: 绘制清除时间-电压恢复曲线
  - `result_compare`: 对比不同故障位置的扫描结果

## 性能特点

- **执行时间**：与扫描点数成正比，每个点约30-120秒
- **扫描点数建议**：建议控制在5-10个点以内
- **模型克隆**：每次扫描克隆基础模型，确保独立性
- **EMT计算量**：基于详细电磁暂态模型，计算量较大
- **适用规模**：适用于中小规模系统的保护配合分析

## 常见问题

### 问题1: EMT仿真失败

**原因**：
- 系统暂态不稳定
- 故障时间设置不合理
- 模型配置错误

**解决**：
```yaml
# 检查故障时间设置
scan:
  fs: 2.5           # 确保fs < fe
  fe_values: [2.6, 2.65, 2.7, 2.75, 2.8]  # 合理的清除时间范围
  chg: 0.01         # 合适的故障电阻
```

### 问题2: 找不到故障元件

**原因**：
- 模型中没有配置故障电阻元件
- 故障元件定义不匹配

**解决**：
```python
# 使用ieee3_prep技能准备模型
from cloudpss_skills import get_skill

prep_skill = get_skill("ieee3_prep")
prep_config = {
    "model": {"rid": "model/holdme/IEEE3"},
    "fault": {"start_time": 2.5, "end_time": 2.7},
    "output": {"filename": "ieee3_with_fault.yaml"}
}
result = prep_skill.run(prep_config)

# 然后使用准备好的模型进行扫描
scan_config = {
    "model": {"rid": "./ieee3_with_fault.yaml", "source": "local"},
    "scan": {"fe_values": [2.6, 2.65, 2.7]}
}
```

### 问题3: 电压趋势不单调

**原因**：
- 系统存在复杂的暂态过程
- 研究时刻选择不当
- 扫描点数量不足

**解决**：
```yaml
# 调整研究时刻
assessment:
  study_time: 3.0    # 选择更晚的研究时刻，等待暂态平息

# 增加扫描点密度
scan:
  fe_values: [2.60, 2.62, 2.64, 2.66, 2.68, 2.70, 2.72, 2.74, 2.76, 2.78, 2.80]
```

### 问题4: 扫描时间过长

**原因**：
- EMT仿真计算量大
- 扫描点数过多
- 仿真时长设置过长

**解决**：
```yaml
# 减少扫描点数，聚焦关键区域
scan:
  fe_values: [2.70, 2.75, 2.80, 2.85, 2.90]  # 5个关键点

# 先粗扫再细扫
# 第一轮：fe_values: [2.6, 2.7, 2.8, 2.9]
# 第二轮：在临界区域细扫 fe_values: [2.72, 2.74, 2.76, 2.78]
```

## 完整示例

### 场景描述
某电力系统保护部门需要确定IEEE3系统Bus_1处发生三相短路故障时的临界清除时间，为断路器保护定值整定提供依据。

### 配置文件

```yaml
skill: fault_clearing_scan
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

scan:
  fs: 2.5                              # 故障开始时间
  fe_values: [2.70, 2.72, 2.74, 2.76, 2.78, 2.80, 2.82, 2.84, 2.86, 2.88, 2.90]
  chg: 0.01                            # 故障电阻

assessment:
  trace_name: "vac:0"                  # Bus_1电压测量通道
  study_time: 3.0                      # 研究时刻（故障后稳定时间）

output:
  format: json
  path: ./results/
  prefix: clearing_time_study
  generate_report: true
```

### 执行命令

```bash
# 创建输出目录
mkdir -p ./results

# 执行故障清除时间扫描
python -m cloudpss_skills run --config clearing_study.yaml
```

### 预期输出

```
[INFO] 加载认证...
[INFO] 认证成功
[INFO] 模型: IEEE3
[INFO] 扫描 11 个清除时间点: [2.7, 2.72, 2.74, 2.76, 2.78, 2.8, 2.82, 2.84, 2.86, 2.88, 2.9]
[INFO] [1/11] fe=2.7
[INFO]   -> 研究时刻电压: 0.9823
[INFO] [2/11] fe=2.72
[INFO]   -> 研究时刻电压: 0.9756
...
[INFO] [8/11] fe=2.84
[INFO]   -> 研究时刻电压: 0.6123
[INFO] [9/11] fe=2.86
[INFO]   -> 研究时刻电压: 0.4231
...
[INFO] 单调恶化: True
[INFO] 结果已保存
```

### 结果文件

**JSON结果文件** (`clearing_time_study_20240324_143245.json`):
```json
{
  "model": "IEEE3",
  "study_time": 3.0,
  "monotonic_degradation": true,
  "results": [
    {"fe": 2.70, "voltage_at_study": 0.9823, "job_id": "job_001"},
    {"fe": 2.72, "voltage_at_study": 0.9756, "job_id": "job_002"},
    {"fe": 2.74, "voltage_at_study": 0.9689, "job_id": "job_003"},
    {"fe": 2.76, "voltage_at_study": 0.9541, "job_id": "job_004"},
    {"fe": 2.78, "voltage_at_study": 0.9324, "job_id": "job_005"},
    {"fe": 2.80, "voltage_at_study": 0.8912, "job_id": "job_006"},
    {"fe": 2.82, "voltage_at_study": 0.8123, "job_id": "job_007"},
    {"fe": 2.84, "voltage_at_study": 0.6123, "job_id": "job_008"},
    {"fe": 2.86, "voltage_at_study": 0.4231, "job_id": "job_009"},
    {"fe": 2.88, "voltage_at_study": 0.3456, "job_id": "job_010"},
    {"fe": 2.90, "voltage_at_study": 0.2987, "job_id": "job_011"}
  ]
}
```

**Markdown报告** (`clearing_time_study_report_20240324_143245.md`):
```markdown
# 故障清除时间扫描报告

研究时刻: 3.0s
单调恶化: 是

| fe (s) | 研究时刻电压 |
|--------|--------------|
| 2.7 | 0.9823 |
| 2.72 | 0.9756 |
| 2.74 | 0.9689 |
| 2.76 | 0.9541 |
| 2.78 | 0.9324 |
| 2.8 | 0.8912 |
| 2.82 | 0.8123 |
| 2.84 | 0.6123 |
| 2.86 | 0.4231 |
| 2.88 | 0.3456 |
| 2.9 | 0.2987 |

**结论**: 清除时间越晚，研究时刻电压越低，恢复越差。
**临界清除时间**: 约在2.82s到2.84s之间（电压从0.81pu骤降至0.61pu）
**保护建议**: 断路器动作时间应小于2.82s以确保系统稳定
```

### 后续应用

基于故障清除时间扫描结果，可以：
1. 使用 `visualize` 绘制清除时间-电压恢复曲线
2. 结合 `transient_stability` 进行更详细的暂态稳定分析
3. 使用 `fault_severity_scan` 分析不同故障严重度的影响
4. 为保护定值整定提供量化依据

**关键结论**：从结果可以看出，当清除时间超过2.82s时，系统电压恢复能力急剧下降，因此保护装置的动作时间应整定在2.82s以内。

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
