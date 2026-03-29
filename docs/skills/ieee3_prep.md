# IEEE3模型准备技能 (IEEE3 Prep)

## 设计背景

### 研究对象
IEEE3模型准备技能用于获取IEEE3标准测试系统并进行EMT（电磁暂态）仿真所需的配置调整。IEEE3系统是电力系统暂态稳定性研究中最常用的标准测试系统之一，包含3台发电机、3条母线和3条传输线路。

### 实际需求
在进行EMT暂态仿真前，通常需要对标准模型进行以下准备工作：
1. **故障时间调整**：配置故障开始和结束时间以适应特定研究场景
2. **输出通道配置**：设置仿真输出通道和采样频率
3. **测量元件配置**：配置电压、电流等测量元件
4. **本地模型保存**：将云端模型保存为本地YAML文件以便后续修改
5. **仿真参数优化**：调整仿真步长、时长等参数

### 期望的输入和输出

**输入**：
- IEEE3模型来源（云端RID或本地路径）
- 故障时间参数（可选）
- 输出配置参数（采样频率、文件名等）

**输出**：
- 准备好的IEEE3模型YAML文件
- 模型配置信息
- 调整的参数摘要

### 计算结果的用途和价值
准备后的模型可用于：
- 作为EMT暂态仿真的基础模型
- 进行故障清除时间扫描
- 进行故障严重度扫描
- 进行暂态稳定分析
- 保存为本地副本进行离线修改

## 功能特性

- **自动模型获取**：从CloudPSS云端自动获取IEEE3标准模型
- **故障参数调整**：自动调整故障元件的开始和结束时间
- **采样频率配置**：配置EMT仿真输出采样频率
- **本地保存**：将准备好的模型保存为YAML文件
- **灵活配置**：支持自定义故障时间和输出参数
- **云端/本地兼容**：支持云端模型和本地模型作为输入

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init ieee3_prep --output prep.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config prep.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("ieee3_prep")

# 配置
config = {
    "skill": "ieee3_prep",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE3",
        "source": "cloud"
    },
    "fault": {
        "start_time": 2.5,    # 故障开始时间(s)
        "end_time": 2.7       # 故障结束时间(s)
    },
    "output": {
        "sampling_freq": 2000,              # 采样频率(Hz)
        "path": "./models/",                # 输出路径
        "filename": "ieee3_prepared.yaml"   # 输出文件名
    }
}

# 运行
result = skill.run(config)
print(f"状态: {result.status}")
print(f"输出文件: {result.data.get('output_path', 'N/A')}")
```

### 3.3 YAML配置示例

```yaml
skill: ieee3_prep
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

fault:
  start_time: 2.5    # 故障开始时间(s)
  end_time: 2.7      # 故障结束时间(s)

output:
  sampling_freq: 2000              # 采样频率(Hz)
  path: ./models/                  # 输出路径
  filename: ieee3_prepared.yaml    # 输出文件名
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: ieee3_prep                    # 必需: 技能名称
auth:                                 # 认证配置
  token: string                       # 直接提供token（不推荐）
  token_file: string                  # token文件路径（默认: .cloudpss_token）

model:                                # 模型配置
  rid: string                         # 模型RID或本地路径（默认: model/holdme/IEEE3）
  source: enum                        # cloud | local（默认: cloud）

fault:                                # 故障配置（可选）
  start_time: number                  # 故障开始时间(s)（默认: 2.5）
  end_time: number                    # 故障结束时间(s)（默认: 2.7）

output:                               # 输出配置
  sampling_freq: integer              # 采样频率(Hz)（默认: 2000）
  path: string                        # 输出目录（默认: ./）
  filename: string                    # 输出文件名（默认: ieee3_prepared.yaml）
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"ieee3_prep" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 否 | model/holdme/IEEE3 | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `fault.start_time` | number | 否 | 2.5 | 故障开始时间(s) |
| `fault.end_time` | number | 否 | 2.7 | 故障结束时间(s) |
| `output.sampling_freq` | integer | 否 | 2000 | EMT仿真采样频率(Hz) |
| `output.path` | string | 否 | ./ | 输出目录路径 |
| `output.filename` | string | 否 | ieee3_prepared.yaml | 输出文件名 |

## Agent使用指南

### 5.1 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("ieee3_prep")

# 最小化配置（使用所有默认值）
config = {}

# 或自定义故障时间
config = {
    "fault": {
        "start_time": 3.0,
        "end_time": 3.2
    },
    "output": {
        "filename": "my_ieee3.yaml"
    }
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status.value == "SUCCESS":
        print(f"模型准备完成: {result.data['output_path']}")
    else:
        print(f"准备失败: {result.error}")
```

### 5.2 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data

    # 访问模型信息
    print(f"模型名称: {data['model_name']}")
    print(f"模型RID: {data['model_rid']}")

    # 访问输出文件
    print(f"输出文件: {data['output_path']}")

    # 访问故障配置
    fault = data.get('fault', {})
    if fault:
        print(f"故障时间: {fault.get('start_time')}s - {fault.get('end_time')}s")

    # 访问采样频率
    print(f"采样频率: {data.get('sampling_freq', 'N/A')} Hz")

    # 访问输出文件
    for artifact in result.artifacts:
        print(f"输出文件: {artifact.path} ({artifact.size} bytes)")

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
    elif "权限" in error_msg:
        print("错误: 无权限访问模型，请检查token权限")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "model_name": "IEEE3",
  "model_rid": "model/holdme/IEEE3",
  "output_path": "./ieee3_prepared.yaml",
  "fault": {
    "start_time": 2.5,
    "end_time": 2.7
  },
  "sampling_freq": 2000
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "ieee3_prep" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典，包含model_name、model_rid、output_path等 |
| `artifacts` | list | 输出文件列表（Artifact对象） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标 |

## 设计原理

### 工作流程

```
1. 配置加载
   └── 使用默认值填充缺失配置
   └── 验证故障时间合理性（start_time < end_time）

2. 认证初始化
   └── 读取token文件或直接获取token
   └── 调用setToken完成认证

3. 获取模型
   └── 从云端fetch或本地load模型
   └── 记录模型信息

4. 调整故障参数（如果配置了fault）
   └── 查找故障元件（definition: model/CloudPSS/_newFaultResistor_3p）
   └── 使用updateComponent更新fs和fe参数
   └── 记录调整的故障时间

5. 配置采样频率
   └── 设置EMT仿真输出采样频率

6. 保存模型
   └── 创建输出目录
   └── 使用Model.dump保存为YAML文件
   └── 生成Artifact记录
```

### 故障元件识别

技能通过以下方式识别故障元件：

```python
for comp in components.values():
    if getattr(comp, "definition", "") == "model/CloudPSS/_newFaultResistor_3p":
        fault = comp
        break
```

**故障参数更新**：
- `fs` (fault start)：故障开始时间
- `fe` (fault end)：故障结束时间

## 与其他技能的关联

```
ieee3_prep (模型准备)
    ↓ (生成准备好的模型)
fault_clearing_scan (故障清除时间扫描)
    ↓ (调整清除时间)
fault_severity_scan (故障严重度扫描)
    ↓ (调整故障电阻)
emt_simulation (EMT暂态仿真)
    ↓ (运行仿真)
transient_stability (暂态稳定分析)
```

**依赖关系**：
- **输入依赖**：无（可直接使用）
- **输出被依赖**：
  - `fault_clearing_scan`: 需要准备后的模型作为输入
  - `fault_severity_scan`: 需要准备后的模型作为输入
  - `emt_simulation`: 可直接使用准备后的模型
  - `emt_n1_screening`: 批量EMT分析的基础

**使用流程**：
```
ieee3_prep → 保存本地模型 → fault_clearing_scan/fault_severity_scan → 分析结果
```

## 性能特点

- **执行时间**：约2-5秒（主要为模型获取和保存）
- **内存占用**：低（仅加载单个IEEE3模型）
- **网络依赖**：需要从云端获取模型（除非使用本地源）
- **输出大小**：IEEE3模型YAML文件约50-100KB
- **适用场景**：EMT仿真前的模型准备

## 常见问题

### 问题1: 找不到故障元件

**原因**：
- IEEE3模型中没有故障电阻元件
- 故障元件定义不匹配

**解决**：
```python
# 检查模型中是否有故障元件
from cloudpss import Model, setToken
setToken("your_token")
model = Model.fetch("model/holdme/IEEE3")
components = model.getAllComponents()
for comp_id, comp in components.items():
    print(f"ID: {comp_id}, Definition: {getattr(comp, 'definition', 'N/A')}")

# 如果没有故障元件，可能需要使用其他模型
# 或者手动添加故障元件
```

### 问题2: 输出目录不存在

**原因**：
- 指定的output.path目录不存在
- 无写入权限

**解决**：
```python
import os

# 确保目录存在
os.makedirs("./models", exist_ok=True)

config = {
    "output": {
        "path": "./models/",
        "filename": "ieee3_prepared.yaml"
    }
}
```

### 问题3: 故障时间不生效

**原因**：
- 配置中未指定fault部分
- 模型中无故障元件

**解决**：
```yaml
# 确保配置了fault参数
skill: ieee3_prep
fault:
  start_time: 2.5    # 必须同时指定start_time和end_time
  end_time: 2.7

output:
  filename: ieee3_with_fault.yaml
```

### 问题4: 使用本地模型作为输入

**原因**：
- 需要从本地加载已修改的模型
- 离线环境无法访问云端

**解决**：
```yaml
skill: ieee3_prep
model:
  rid: ./models/my_ieee3.yaml    # 本地模型路径
  source: local                   # 指定为本地来源

fault:
  start_time: 3.0
  end_time: 3.2

output:
  filename: ieee3_modified.yaml
```

## 完整示例

### 场景描述
某研究机构需要使用IEEE3系统进行故障清除时间扫描研究，需要先准备好带故障元件的模型，并调整故障时间为研究所需的值。

### 配置文件

```yaml
skill: ieee3_prep
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

fault:
  start_time: 3.0      # 故障在3.0s开始
  end_time: 3.2        # 故障在3.2s清除（持续0.2s）

output:
  sampling_freq: 2000               # 2kHz采样频率
  path: ./models/                   # 保存到models目录
  filename: ieee3_fault_study.yaml  # 输出文件名
```

### 执行命令

```bash
# 创建输出目录
mkdir -p ./models

# 执行模型准备
python -m cloudpss_skills run --config prep_fault_study.yaml
```

### 预期输出

```
[INFO] 加载认证...
[INFO] 认证成功
[INFO] 获取IEEE3模型...
[INFO] 模型: IEEE3
[INFO] 创建本地工作副本...
[INFO] 调整故障参数...
[INFO] 故障时间: 3.0s - 3.2s
[INFO] 设置采样频率: 2000Hz
[INFO] 保存到: ./models/ieee3_fault_study.yaml
[INFO] 模型准备完成
```

### 结果文件

**准备好的模型文件** (`./models/ieee3_fault_study.yaml`):
```yaml
# IEEE3模型YAML文件
# 已配置故障时间: 3.0s - 3.2s
# 采样频率: 2000Hz

name: IEEE3
rid: model/holdme/IEEE3
components:
  # ... 组件定义 ...
  FaultResistor:
    definition: model/CloudPSS/_newFaultResistor_3p
    args:
      fs: 3.0    # 故障开始时间已调整
      fe: 3.2    # 故障结束时间已调整
      chg: 0.01
  # ... 其他组件 ...
```

### 后续应用

基于准备好的IEEE3模型，可以：
1. 使用 `fault_clearing_scan` 进行故障清除时间扫描
2. 使用 `fault_severity_scan` 进行故障严重度扫描
3. 使用 `emt_simulation` 进行自定义EMT暂态仿真
4. 使用 `emt_n1_screening` 进行N-1安全分析

**使用示例**：
```python
from cloudpss_skills import get_skill

# 使用准备好的模型进行故障清除时间扫描
skill = get_skill("fault_clearing_scan")
config = {
    "model": {
        "rid": "./models/ieee3_fault_study.yaml",
        "source": "local"
    },
    "scan": {
        "fs": 3.0,  # 与准备时的start_time一致
        "fe_values": [3.05, 3.1, 3.15, 3.2, 3.25],
        "chg": 0.01
    }
}
result = skill.run(config)
```

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
