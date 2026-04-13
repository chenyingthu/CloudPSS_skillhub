# EMT暂态仿真技能 (EMT Simulation)

## 设计背景

### 研究对象

EMT（Electromagnetic Transient）暂态仿真是电力系统时域仿真技术，用于分析系统在故障、开关操作、负荷突变等扰动下的电磁暂态响应过程。与稳态潮流计算不同，EMT仿真捕捉的是微秒至秒级时间尺度内的电压、电流瞬态变化，是研究电力系统动态行为的重要工具。

### 实际需求

在电力系统规划和运行中，需要了解系统在扰动下的暂态行为：

1. **故障分析**：短路故障时的电流、电压暂态过程
2. **开关操作**：断路器开合引起的过电压和涌流
3. **设备测试**：保护装置的动作特性验证
4. **新能源接入**：逆变器、风电、光伏的暂态响应
5. **高压直流**：HVDC系统的启动、闭锁和故障恢复

### 期望的输入和输出

**输入**：

- 电力系统模型（IEEE标准模型或实际系统）
- 仿真时长（通常5-20秒）
- 仿真步长（通常0.0001秒，对应10kHz采样）
- 输出通道选择（电压、电流等测量信号）
- 超时时间设置

**输出**：

- 时域波形数据（CSV/JSON格式）
- 波形分组信息（Plot和Channel结构）
- 仿真任务状态
- 数据点数量和采样信息

### 计算结果的用途和价值

EMT仿真结果可用于：

- **保护整定**：获取短路电流的峰值和稳态值
- **设备选型**：根据暂态过电压选择设备绝缘水平
- **稳定性评估**：分析系统的暂态稳定裕度
- **控制策略优化**：验证控制器参数的有效性

## 功能特性

- **详细暂态分析**：基于EMTP算法，支持故障、开关、负荷变化等暂态过程
- **多格式导出**：支持CSV、JSON格式的波形数据导出
- **通道选择**：支持指定导出特定通道或全部通道
- **自动拓扑检查**：运行前自动检查EMT拓扑完整性
- **灵活时间配置**：可配置仿真时长、步长和超时时间
- **实时状态监控**：监控仿真进度和任务状态

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init emt_simulation --output emt_config.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config emt_config.yaml

# 或使用简化配置
python -m cloudpss_skills run --config <(echo '
skill: emt_simulation
model:
  rid: model/holdme/IEEE3
simulation:
  duration: 10.0
')
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("emt_simulation")

# 配置
config = {
    "skill": "emt_simulation",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE3",
        "source": "cloud"
    },
    "simulation": {
        "duration": 10.0,
        "step_size": 0.0001,
        "timeout": 300
    },
    "output": {
        "format": "csv",
        "path": "./results/",
        "prefix": "emt_ieee3",
        "channels": ["*"]  # 导出所有通道
    }
}

# 验证配置
validation = skill.validate(config)
if not validation.valid:
    print("配置错误:", validation.errors)

# 运行
result = skill.run(config)
print(f"状态: {result.status}")
print(f"波形分组数: {result.data.get('plot_count', 0)}")
```

### 3.3 YAML配置示例

```yaml
skill: emt_simulation
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud  # 或 local

simulation:
  duration: 10.0        # 仿真时长（秒）
  step_size: 0.0001     # 仿真步长（秒），50Hz系统建议0.0001
  timeout: 300          # 超时时间（秒）

output:
  format: csv           # csv | json | yaml
  path: ./results/
  prefix: emt_output
  timestamp: true       # 文件名添加时间戳
  channels: ["*"]       # ["*"]表示全部，或指定通道列表
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: emt_simulation                 # 必需: 技能名称
auth:                                  # 认证配置
  token: string                       # 直接提供token（不推荐）
  token_file: string                  # token文件路径（默认: .cloudpss_token）

model:                                 # 模型配置（必需）
  rid: string                         # 模型RID或本地路径（必需）
  source: enum                        # cloud | local（默认: cloud）

simulation:                            # 仿真配置
  duration: number                    # 仿真时长（秒）
  step_size: number                   # 仿真步长（秒）
  timeout: integer                    # 超时时间（秒，默认: 300）

output:                                # 输出配置
  format: enum                        # csv | json | yaml（默认: csv）
  path: string                        # 输出目录（默认: ./results/）
  prefix: string                      # 文件名前缀（默认: emt_output）
  timestamp: boolean                  # 是否添加时间戳（默认: true）
  channels: array                     # 导出通道列表，["*"]表示全部
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"emt_simulation" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID（如model/holdme/IEEE3）或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `simulation.duration` | number | 否 | - | 仿真时长（秒），需大于0 |
| `simulation.step_size` | number | 否 | - | 仿真步长（秒），建议0.0001（50Hz系统） |
| `simulation.timeout` | integer | 否 | 300 | 仿真超时时间（秒） |
| `output.format` | enum | 否 | csv | 输出格式：csv / json / yaml |
| `output.path` | string | 否 | ./results/ | 输出文件目录 |
| `output.prefix` | string | 否 | emt_output | 输出文件名前缀 |
| `output.timestamp` | boolean | 否 | true | 文件名是否包含时间戳 |
| `output.channels` | array | 否 | ["*"] | 导出通道列表，["*"]表示全部通道 |

## Agent使用指南

### 5.1 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("emt_simulation")

# 最小化配置（使用默认值）
config = {
    "model": {"rid": "model/holdme/IEEE3"},
    "simulation": {"duration": 10.0}
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status.value == "SUCCESS":
        print(f"仿真完成，波形分组数: {result.data['plot_count']}")
        for artifact in result.artifacts:
            print(f"输出文件: {artifact.path}")
    else:
        print(f"仿真失败: {result.error}")
```

### 5.2 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data

    # 访问仿真结果
    model_name = data.get("model_name")
    model_rid = data.get("model_rid")
    job_id = data.get("job_id")
    plot_count = data.get("plot_count")

    # 遍历波形分组
    for plot in data.get("plots", []):
        print(f"Plot {plot['index']}: {plot['name']} ({plot['channel_count']} channels)")
        print(f"  通道: {', '.join(plot['channels'][:5])}...")

    # 访问输出文件
    for artifact in result.artifacts:
        print(f"文件: {artifact.path} ({artifact.type}, {artifact.size} bytes)")

    # 查看性能指标
    metrics = result.metrics
    print(f"导出文件数: {metrics.get('exported_files', 0)}")

# 查看日志
for log in result.logs:
    print(f"[{log.timestamp}] [{log.level}] {log.message}")
```

### 5.3 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    error_msg = result.error

    # 常见错误处理
    if "Token文件不存在" in error_msg:
        print("错误: 请创建.cloudpss_token文件，内容为您的API token")
    elif "模型不存在" in error_msg:
        print("错误: 请检查模型RID是否正确，如model/holdme/IEEE3")
    elif "EMT拓扑检查失败" in error_msg:
        print("错误: 模型未配置EMT拓扑，请确认模型包含EMT仿真所需的元件和任务配置")
    elif "仿真超时" in error_msg:
        print("错误: 仿真超时，请增加timeout配置或减少duration")
    elif "仿真失败" in error_msg:
        print("错误: EMT仿真失败，请检查模型配置和参数")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "model_name": "IEEE3",
  "model_rid": "model/holdme/IEEE3",
  "job_id": "job_xxx",
  "plot_count": 2,
  "plots": [
    {
      "index": 0,
      "key": "voltage",
      "name": "母线电压",
      "channel_count": 3,
      "channels": ["Bus1_V", "Bus2_V", "Bus3_V"]
    },
    {
      "index": 1,
      "key": "current",
      "name": "支路电流",
      "channel_count": 3,
      "channels": ["Line1_I", "Line2_I", "Line3_I"]
    }
  ]
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "emt_simulation" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典，包含model_name、plot_count、plots等 |
| `artifacts` | list | 输出文件列表（Artifact对象） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标，包含plot_count、exported_files等 |

## 设计原理

### 工作流程

```
1. 加载认证信息 → 设置CloudPSS Token
2. 获取模型 → 从云端或本地加载模型
3. 检查EMT拓扑 → 验证模型EMT配置完整性
4. 运行EMT仿真 → 创建并执行EMT任务
5. 等待完成 → 监控任务状态直到完成或超时
6. 提取结果 → 获取仿真结果和波形数据
7. 导出数据 → 按指定格式导出波形到文件
```

### EMT仿真基础

EMT仿真基于时域微分方程求解：

```
dx/dt = f(x, t)
```

使用梯形积分法或后退欧拉法进行数值积分，时间步长通常设置为0.0001秒（对应10kHz采样率），可准确捕捉50Hz电力系统的暂态过程。

## 与其他技能的关联

```
emt_simulation (可通过 fault/sampling_freq 调整参数)
    ↓ (波形数据)
visualize → waveform_export → disturbance_severity
    ↓
emt_fault_study / fault_clearing_scan / fault_severity_scan
```

### 依赖关系

- **必需依赖**: CloudPSS SDK (`cloudpss`)
- **前置依赖**: 无（可直接运行）
- 可通过 `fault.start_time` / `fault.end_time` 调整故障参数
- 可通过 `simulation.sampling_freq` 调整采样频率
- **后续技能**:
  - `visualize`: 可视化波形
  - `waveform_export`: 导出特定格式波形
  - `disturbance_severity`: 扰动严重程度分析
  - `emt_fault_study`: EMT故障研究分析

## 性能特点

- **仿真时间**: IEEE3系统约30-60秒，IEEE39系统约5-15分钟
- **步长影响**: 步长越小精度越高但时间越长，50Hz系统建议0.0001s
- **内存占用**: 与系统规模和仿真时长成正比
- **输出大小**: CSV文件可能很大（IEEE3，10秒仿真约10-50MB）
- **建议步长**: 50Hz系统用0.0001s（10kHz采样），60Hz系统用8.33e-5s

## 常见问题

### 问题1: EMT拓扑检查失败

**原因**: 模型未配置EMT拓扑或缺少必要的EMT元件

**解决**:
```bash
# 通过配置直接调整故障参数
# 在config中添加 fault 段即可，无需单独准备模型
```

### 问题2: 仿真超时

**原因**: 仿真时间过长或系统复杂

**解决**:
```yaml
simulation:
  duration: 5.0       # 缩短仿真时长
  timeout: 600        # 增加超时时间到10分钟
```

### 问题3: 波形数据为空

**原因**: 未配置输出通道或模型无测量元件

**解决**: 确保模型包含测量元件（电压表、电流表），并正确配置EMT输出通道。检查模型的`output_channels`配置。

### 问题4: Token认证失败

**原因**: Token文件不存在或内容错误

**解决**:
```bash
# 创建token文件
echo "your_token_here" > .cloudpss_token
chmod 600 .cloudpss_token
```

## 完整示例

### 场景描述

某电力公司需要对IEEE3系统进行EMT暂态仿真，获取故障期间的电压和电流波形，用于保护装置整定分析。

### 配置文件

```yaml
skill: emt_simulation
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

simulation:
  duration: 10.0
  step_size: 0.0001
  timeout: 300

output:
  format: csv
  path: ./results/
  prefix: emt_ieee3
  timestamp: true
  channels: ["*"]
```

### 执行命令

```bash
python -m cloudpss_skills run --config emt_simulation.yaml
```

### 预期输出

```
[INFO] 加载认证信息...
[INFO] 认证成功
[INFO] 获取模型...
[INFO] 模型名称: IEEE3
[INFO] 模型RID: model/holdme/IEEE3
[INFO] 检查EMT拓扑...
[INFO] 拓扑检查通过，元件数: 156
[INFO] 启动EMT仿真...
[INFO] 任务已创建，ID: job_emt_xxx
[INFO] 仿真运行中... (0s)
[INFO] 仿真运行中... (10s)
...
[INFO] 仿真已完成
[INFO] 提取仿真结果...
[INFO] 波形分组数: 2
[INFO] 导出: results/emt_ieee3_20240324_143245_voltage.csv
[INFO] 导出: results/emt_ieee3_20240324_143245_current.csv
[INFO] EMT仿真完成，共导出 2 个文件
```

### 结果文件

CSV波形数据文件格式：

```csv
time,Bus1_V,Bus2_V,Bus3_V
0.000000,1.000000,0.982345,0.975421
0.000100,0.999876,0.982234,0.975312
...
```

### 后续应用

1. **可视化分析**: 使用`visualize`技能绘制波形图
2. **故障研究**: 使用`emt_fault_study`进行多工况对比分析
3. **波形导出**: 使用`waveform_export`导出特定格式
4. **扰动分析**: 使用`disturbance_severity`评估暂态严重程度

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
