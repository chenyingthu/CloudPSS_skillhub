# 故障严重度扫描技能 (Fault Severity Scan)

## 设计背景

### 研究对象
故障严重度扫描技能用于分析不同故障电阻（代表故障严重程度）对电力系统电压跌落和恢复的影响。故障电阻越小代表故障越严重（金属性短路），故障电阻越大代表故障越轻（经过渡电阻短路）。

### 实际需求
在电力系统保护和稳定性分析中，需要解决以下问题：
1. **故障严重程度评估**：量化不同严重程度故障对系统的影响
2. **电压跌落分析**：分析故障期间母线电压跌落幅度
3. **恢复能力评估**：评估系统在不同故障严重程度下的恢复能力
4. **保护灵敏度分析**：分析保护装置对不同故障的响应
5. **系统鲁棒性评估**：评估系统承受不同程度故障的能力

### 期望的输入和输出

**输入**：
- 电力系统EMT模型（云端RID或本地YAML文件）
- 故障开始时间和结束时间（fs, fe）
- 故障电阻扫描值列表（chg_values）
- 评估电压通道和时间段（trace_name, time_windows）

**输出**：
- 每个故障电阻对应的电压RMS值（故障前、故障中、故障后）
- 电压跌落幅度（fault_drop）
- 恢复缺口（postfault_gap）
- 趋势分析结果
- JSON、CSV和Markdown格式的详细结果

### 计算结果的用途和价值
故障严重度扫描结果可用于：
- 评估系统对不同严重度故障的承受能力
- 确定保护的灵敏度要求
- 分析电压跌落对敏感负荷的影响
- 为故障类型识别提供特征数据
- 验证系统的故障恢复能力

## 功能特性

- **故障电阻扫描**：扫描多个故障电阻值（从金属性短路到高阻故障）
- **三时段RMS计算**：分别计算故障前、故障中、故障后的电压RMS值
- **跌落与恢复分析**：自动计算电压跌落幅度和恢复缺口
- **趋势自动判断**：自动判断故障跌落和恢复的趋势
- **多格式输出**：支持JSON、CSV和Markdown报告
- **EMT暂态仿真**：基于详细的电磁暂态模型
- **灵活时间段配置**：支持自定义三个评估时间段

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init fault_severity_scan --output severity_scan.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config severity_scan.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("fault_severity_scan")

# 配置
config = {
    "skill": "fault_severity_scan",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE3",
        "source": "cloud"
    },
    "scan": {
        "fs": 2.5,                           # 故障开始时间(s)
        "fe": 2.7,                           # 故障结束时间(s)
        "chg_values": [0.01, 0.1, 1.0, 10.0, 100.0]  # 故障电阻扫描值(Ω)
    },
    "assessment": {
        "trace_name": "vac:0",               # 评估电压通道
        "time_windows": {
            "prefault": [2.42, 2.44],        # 故障前时间段
            "fault": [2.56, 2.58],           # 故障中时间段
            "postfault": [2.92, 2.94]        # 故障后时间段
        }
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "severity_scan",
        "generate_report": True
    }
}

# 运行
result = skill.run(config)
print(f"状态: {result.status}")
print(f"故障趋势: {result.data.get('fault_trend', 'unknown')}")
print(f"恢复趋势: {result.data.get('gap_trend', 'unknown')}")
```

### 3.3 YAML配置示例

```yaml
skill: fault_severity_scan
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

scan:
  fs: 2.5                              # 故障开始时间(s)
  fe: 2.7                              # 故障结束时间(s)
  chg_values: [0.01, 0.1, 1.0, 10.0, 100.0]  # 故障电阻扫描值(Ω)

assessment:
  trace_name: "vac:0"                  # 评估电压通道名称
  time_windows:
    prefault: [2.42, 2.44]             # 故障前时间段(s)
    fault: [2.56, 2.58]                # 故障中时间段(s)
    postfault: [2.92, 2.94]            # 故障后时间段(s)

output:
  format: json
  path: ./results/
  prefix: severity_scan
  generate_report: true
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: fault_severity_scan            # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token（不推荐）
  token_file: string                  # token文件路径（默认: .cloudpss_token）

model:                                # 模型配置（必需）
  rid: string                         # 模型RID或本地路径（必需）
  source: enum                        # cloud | local（默认: cloud）

scan:                                 # 扫描配置（必需）
  fs: number                          # 故障开始时间(s)（默认: 2.5）
  fe: number                          # 故障结束时间(s)（默认: 2.7）
  chg_values: array                   # 故障电阻扫描值列表，number数组（必需）

assessment:                           # 评估配置
  trace_name: string                  # 评估电压通道名称（默认: vac:0）
  time_windows:                       # 评估时间段配置
    prefault: array                   # 故障前时间段[s_start, s_end]（默认: [2.42, 2.44]）
    fault: array                      # 故障中时间段[s_start, s_end]（默认: [2.56, 2.58]）
    postfault: array                  # 故障后时间段[s_start, s_end]（默认: [2.92, 2.94]）

output:                               # 输出配置
  format: enum                        # json | csv（默认: json）
  path: string                        # 输出目录（默认: ./results/）
  prefix: string                      # 文件名前缀（默认: fault_severity_scan）
  generate_report: boolean            # 是否生成报告（默认: true）
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"fault_severity_scan" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `scan.fs` | number | 否 | 2.5 | 故障开始时间(s) |
| `scan.fe` | number | 否 | 2.7 | 故障结束时间(s) |
| `scan.chg_values` | array | 是 | - | 故障电阻扫描值列表(Ω) |
| `assessment.trace_name` | string | 否 | vac:0 | 评估电压通道名称 |
| `assessment.time_windows.prefault` | array | 否 | [2.42, 2.44] | 故障前评估时间段(s) |
| `assessment.time_windows.fault` | array | 否 | [2.56, 2.58] | 故障中评估时间段(s) |
| `assessment.time_windows.postfault` | array | 否 | [2.92, 2.94] | 故障后评估时间段(s) |
| `output.format` | enum | 否 | json | 输出格式 |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | fault_severity_scan | 文件名前缀 |
| `output.generate_report` | boolean | 否 | true | 是否生成Markdown报告 |

## Agent使用指南

### 5.1 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("fault_severity_scan")

# 配置
config = {
    "model": {"rid": "model/holdme/IEEE3"},
    "scan": {
        "fs": 2.5,
        "fe": 2.7,
        "chg_values": [0.01, 0.1, 1.0, 10.0, 100.0]
    },
    "assessment": {
        "trace_name": "vac:0",
        "time_windows": {
            "prefault": [2.42, 2.44],
            "fault": [2.56, 2.58],
            "postfault": [2.92, 2.94]
        }
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

    # 访问趋势分析
    print(f"故障趋势: {data['fault_trend']}")
    print(f"恢复趋势: {data['gap_trend']}")

    # 访问详细结果
    for r in data.get("results", []):
        print(f"chg={r['chg']}Ω:")
        print(f"  故障前电压: {r['prefault_rms']:.4f} pu")
        print(f"  故障中电压: {r['fault_rms']:.4f} pu")
        print(f"  故障后电压: {r['postfault_rms']:.4f} pu")
        print(f"  电压跌落: {r['fault_drop']:.4f} pu")
        print(f"  恢复缺口: {r['postfault_gap']:.4f} pu")

    # 查找最严重的故障情况
    results = data.get("results", [])
    min_chg = min(results, key=lambda r: r['fault_rms'])
    print(f"最严重故障: chg={min_chg['chg']}Ω, 故障电压={min_chg['fault_rms']:.4f} pu")

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
        print("错误: EMT仿真失败，可能是系统不稳定")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "model": "IEEE3",
  "fault_trend": "decreasing",
  "gap_trend": "decreasing",
  "results": [
    {
      "chg": 0.01,
      "prefault_rms": 1.0012,
      "fault_rms": 0.2345,
      "postfault_rms": 0.9876,
      "fault_drop": 0.7667,
      "postfault_gap": 0.0136,
      "job_id": "job_xxx"
    },
    {
      "chg": 0.1,
      "prefault_rms": 1.0012,
      "fault_rms": 0.4567,
      "postfault_rms": 0.9923,
      "fault_drop": 0.5445,
      "postfault_gap": 0.0089,
      "job_id": "job_yyy"
    },
    {
      "chg": 100.0,
      "prefault_rms": 1.0012,
      "fault_rms": 0.9234,
      "postfault_rms": 0.9987,
      "fault_drop": 0.0778,
      "postfault_gap": 0.0025,
      "job_id": "job_zzz"
    }
  ]
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "fault_severity_scan" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典，包含model、fault_trend、gap_trend、results |
| `artifacts` | list | 输出文件列表（JSON、CSV、Markdown报告） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标 |

## 设计原理

### 工作流程

```
1. 配置加载与验证
   └── 验证model.rid存在
   └── 验证scan.chg_values非空且为数组

2. 认证初始化
   └── 读取token文件或直接获取token
   └── 调用setToken完成认证

3. 获取基础模型
   └── 获取模型副本（用于克隆）
   └── 查找故障元件

4. 故障电阻扫描循环
   对于chg_values中的每个故障电阻:
   ├── 克隆基础模型
   ├── 配置故障参数（fs, fe, chg）
   ├── 运行EMT仿真
   ├── 等待仿真完成
   ├── 提取三个时段的电压RMS值
   │   ├── 故障前RMS（prefault时间段）
   │   ├── 故障中RMS（fault时间段）
   │   └── 故障后RMS（postfault时间段）
   ├── 计算电压跌落（prefault - fault）
   ├── 计算恢复缺口（prefault - postfault）
   └── 记录结果

5. 趋势分析
   └── 判断故障跌落趋势
   └── 判断恢复缺口趋势

6. 文件导出
   └── 生成JSON结果文件
   └── 生成CSV结果文件
   └── 生成Markdown分析报告
```

### RMS计算方法

电压RMS值通过以下公式计算：

```
RMS = sqrt(Σ(v_i^2) / N)
```

其中v_i是指定时间段内的电压采样值，N是采样点数。

**指标定义**：
- **电压跌落（fault_drop）** = 故障前RMS - 故障中RMS
- **恢复缺口（postfault_gap）** = 故障前RMS - 故障后RMS

## 与其他技能的关联

```
emt_simulation (基础EMT仿真)
    ↓ (配置故障)
fault_severity_scan
    ↓ (评估故障严重度)
fault_clearing_scan (清除时间扫描)
    ↓ (综合评估)
transient_stability (暂态稳定分析)
```

**依赖关系**：
- **输入依赖**：`ieee3_prep` 或类似的模型准备技能（确保模型有故障元件）
- **输出被依赖**：
  - `visualize`: 绘制故障电阻-电压特性曲线
  - `result_compare`: 对比不同故障位置的扫描结果
  - `fault_clearing_scan`: 可与清除时间扫描结合进行综合评估

**故障严重程度分级**：

| 故障电阻 | 严重程度 | 典型场景 |
|----------|----------|----------|
| 0.01-0.1 Ω | 极严重 | 金属性三相短路 |
| 0.1-1 Ω | 严重 | 低阻接地故障 |
| 1-10 Ω | 中等 | 高阻接地故障 |
| 10-100 Ω | 轻微 | 电弧故障、树木接触 |
| >100 Ω | 极轻微 | 绝缘老化、轻微漏电 |

## 性能特点

- **执行时间**：与扫描点数成正比，每个点约30-120秒
- **扫描点数建议**：建议控制在3-10个点以内
- **模型克隆**：每次扫描克隆基础模型，确保独立性
- **EMT计算量**：基于详细电磁暂态模型，计算量较大
- **适用场景**：适用于保护灵敏度分析和系统鲁棒性评估

## 常见问题

### 问题1: 故障时间段设置不合理

**原因**：
- prefault、fualt、postfault时间段与故障时间不匹配
- 时间段太短，采样点不足

**解决**：
```yaml
# 确保时间段在仿真范围内且合理
scan:
  fs: 2.5
  fe: 2.7

assessment:
  time_windows:
    prefault: [2.0, 2.4]      # 故障前，在fs之前
    fault: [2.55, 2.65]       # 故障中，在fs和fe之间
    postfault: [3.0, 3.5]     # 故障后，在fe之后且系统已稳定
```

### 问题2: chg_values设置不合理

**原因**：
- 故障电阻值跨度太大，导致仿真不稳定
- 故障电阻为0或负数

**解决**：
```yaml
# 合理的故障电阻范围
scan:
  chg_values: [0.01, 0.1, 1.0, 10.0, 100.0]  # 从金属性到高阻故障

# 或者针对特定场景
scan:
  chg_values: [0.01, 0.05, 0.1, 0.5, 1.0]    # 聚焦低阻故障
```

### 问题3: RMS计算异常

**原因**：
- 指定时间段内无数据点
- 时间段设置错误
- trace_name不存在

**解决**：
```python
# 先验证通道存在
result = job.result
plots = result.getPlots()
for i, _ in enumerate(plots):
    channels = result.getPlotChannelNames(i)
    print(f"Plot {i}: {channels}")

# 确认trace_name正确
# 常用通道名：vac:0 (Bus_1电压), vbc:0 (Bus_2电压)等
```

### 问题4: 趋势判断不符合预期

**原因**：
- 扫描点数量不足
- 存在异常数据点
- 系统非线性特性

**解决**：
```yaml
# 增加扫描点密度
scan:
  chg_values: [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]

# 或者手动分析结果
decreasing = all(results[i]["fault_drop"] >= results[i+1]["fault_drop"]
                 for i in range(len(results)-1))
```

## 完整示例

### 场景描述
某电力系统运行部门需要评估IEEE3系统在不同故障严重程度下的电压跌落情况，为保护定值整定和电压暂降评估提供数据支持。

### 配置文件

```yaml
skill: fault_severity_scan
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

scan:
  fs: 2.5                              # 故障开始时间
  fe: 2.7                              # 故障结束时间
  chg_values: [0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0, 50.0, 100.0]  # 9个严重度等级

assessment:
  trace_name: "vac:0"                  # Bus_1电压测量通道
  time_windows:
    prefault: [2.42, 2.44]             # 故障前0.06-0.08s
    fault: [2.56, 2.58]                # 故障中0.06-0.08s
    postfault: [2.92, 2.94]            # 故障后0.22-0.24s

output:
  format: json
  path: ./results/
  prefix: severity_study
  generate_report: true
```

### 执行命令

```bash
# 创建输出目录
mkdir -p ./results

# 执行故障严重度扫描
python -m cloudpss_skills run --config severity_study.yaml
```

### 预期输出

```
[INFO] 加载认证...
[INFO] 认证成功
[INFO] 模型: IEEE3
[INFO] 扫描 9 个故障电阻值: [0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0, 50.0, 100.0]
[INFO] [1/9] chg=0.01
[INFO]   -> 故障跌落: 0.768, 恢复缺口: 0.014
[INFO] [2/9] chg=0.05
[INFO]   -> 故障跌落: 0.721, 恢复缺口: 0.013
...
[INFO] [8/9] chg=50.0
[INFO]   -> 故障跌落: 0.156, 恢复缺口: 0.004
[INFO] [9/9] chg=100.0
[INFO]   -> 故障跌落: 0.089, 恢复缺口: 0.003
[INFO] 故障电阻趋势: decreasing
[INFO] 恢复缺口趋势: decreasing
[INFO] 结果已保存
```

### 结果文件

**JSON结果文件** (`severity_study_20240324_143245.json`):
```json
{
  "model": "IEEE3",
  "fault_trend": "decreasing",
  "gap_trend": "decreasing",
  "results": [
    {
      "chg": 0.01,
      "prefault_rms": 1.0012,
      "fault_rms": 0.2334,
      "postfault_rms": 0.9872,
      "fault_drop": 0.7678,
      "postfault_gap": 0.0140,
      "job_id": "job_001"
    },
    {
      "chg": 0.05,
      "prefault_rms": 1.0012,
      "fault_rms": 0.2801,
      "postfault_rms": 0.9889,
      "fault_drop": 0.7211,
      "postfault_gap": 0.0123,
      "job_id": "job_002"
    },
    {
      "chg": 100.0,
      "prefault_rms": 1.0012,
      "fault_rms": 0.9123,
      "postfault_rms": 0.9989,
      "fault_drop": 0.0889,
      "postfault_gap": 0.0023,
      "job_id": "job_009"
    }
  ]
}
```

**Markdown报告** (`severity_study_report_20240324_143245.md`):
```markdown
# 故障严重度扫描报告

故障电阻趋势: decreasing
恢复缺口趋势: decreasing

| chg | 故障前RMS | 故障RMS | 故障后RMS | 跌落 | 缺口 |
|-----|-----------|---------|-----------|------|------|
| 0.01 | 1.001 | 0.233 | 0.987 | 0.768 | 0.014 |
| 0.05 | 1.001 | 0.280 | 0.989 | 0.721 | 0.012 |
| 0.1 | 1.001 | 0.345 | 0.991 | 0.656 | 0.010 |
| 0.5 | 1.001 | 0.512 | 0.994 | 0.489 | 0.007 |
| 1.0 | 1.001 | 0.623 | 0.996 | 0.378 | 0.005 |
| 5.0 | 1.001 | 0.789 | 0.998 | 0.212 | 0.003 |
| 10.0 | 1.001 | 0.856 | 0.998 | 0.145 | 0.003 |
| 50.0 | 1.001 | 0.902 | 0.999 | 0.099 | 0.002 |
| 100.0 | 1.001 | 0.912 | 0.999 | 0.089 | 0.002 |

**结论**: 故障电阻越大（故障越轻），故障跌落越小，恢复越好。
**关键发现**:
- 金属性短路(chg=0.01Ω)时电压跌落达76.8%，严重影响敏感负荷
- 高阻故障(chg>50Ω)时电压跌落<10%，对系统影响较小
- 系统在所有故障情况下均能恢复稳定
```

### 后续应用

基于故障严重度扫描结果，可以：
1. 使用 `visualize` 绘制故障电阻-电压跌落曲线
2. 结合 `fault_clearing_scan` 进行综合的故障分析
3. 使用 `transient_stability` 评估最严重的故障情况
4. 为保护定值整定和电压暂降评估提供量化依据

**关键结论**：从结果可以看出，金属性短路（chg=0.01Ω）时电压跌落最严重（76.8%），可能对敏感负荷造成严重影响，需要在保护整定时考虑快速切除。

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
