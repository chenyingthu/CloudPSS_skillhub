# EMT暂态仿真技能 (EMT Simulation)

## 概述

EMT（Electromagnetic Transient）暂态仿真是电力系统时域仿真的一种，用于分析系统在故障、开关操作等扰动下的暂态响应。本技能基于CloudPSS的EMTP仿真引擎，支持详细的电磁暂态过程分析。

## 功能特性

- **详细暂态分析**: 支持故障、开关、负荷变化等暂态过程
- **多格式导出**: CSV、JSON格式的波形数据导出
- **通道选择**: 支持指定导出特定通道或全部通道
- **自动拓扑检查**: 运行前自动检查EMT拓扑完整性

## 设计原理

### EMT仿真基础

EMT仿真基于时域微分方程求解：

```
dx/dt = f(x, t)
```

使用梯形积分法或后退欧拉法进行数值积分。

### 仿真流程

```
1. 加载模型
2. 检查EMT拓扑
3. 配置仿真参数（时长、步长）
4. 运行EMT仿真
5. 等待任务完成
6. 提取波形数据
7. 导出指定格式
```

## 快速开始

### 1. CLI方式

```bash
# 初始化配置
python -m cloudpss_skills init emt_simulation --output emt.yaml

# 运行
python -m cloudpss_skills run --config emt.yaml
```

### 2. Python API方式

```python
from cloudpss_skills import get_skill

skill = get_skill("emt_simulation")

config = {
    "skill": "emt_simulation",
    "auth": {"token_file": ".cloudpss_token"},
    "model": {"rid": "model/holdme/IEEE3"},
    "simulation": {
        "duration": 10.0,
        "step_size": 0.0001,
        "timeout": 300
    },
    "output": {
        "format": "csv",
        "path": "./results/",
        "channels": ["*"]  # 导出所有通道
    }
}

result = skill.run(config)
```

### 3. YAML配置

```yaml
skill: emt_simulation
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

simulation:
  duration: 10.0          # 仿真时长（秒）
  step_size: 0.0001       # 仿真步长（秒）
  timeout: 300            # 超时时间（秒）

output:
  format: csv             # csv | json | yaml
  path: ./results/
  prefix: emt_output
  timestamp: true
  channels: ["*"]         # 通道列表，["*"]表示全部
```

## 配置Schema

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `skill` | string | 是 | - | "emt_simulation" |
| `model.rid` | string | 是 | - | 模型RID |
| `model.source` | enum | 否 | cloud | cloud / local |
| `simulation.duration` | number | 否 | - | 仿真时长（秒） |
| `simulation.step_size` | number | 否 | - | 仿真步长（秒） |
| `simulation.timeout` | integer | 否 | 300 | 超时时间（秒） |
| `output.format` | enum | 否 | csv | csv / json / yaml |
| `output.path` | string | 否 | ./results/ | 输出目录 |
| `output.prefix` | string | 否 | emt_output | 文件名前缀 |
| `output.timestamp` | boolean | 否 | true | 添加时间戳 |
| `output.channels` | array | 否 | ["*"] | 导出通道列表 |

## Agent使用指南

### 基础调用

```python
skill = get_skill("emt_simulation")

config = {
    "model": {"rid": "model/holdme/IEEE3"},
    "simulation": {"duration": 10.0}
}

result = skill.run(config)

if result.status.value == "SUCCESS":
    print(f"波形分组数: {result.data['plot_count']}")
    for artifact in result.artifacts:
        print(f"导出文件: {artifact.path}")
```

### 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    if "EMT拓扑检查失败" in result.error:
        print("错误: 模型未配置EMT参数，先运行ieee3_prep")
    elif "仿真超时" in result.error:
        print("错误: 增加timeout配置")
    else:
        print(f"错误: {result.error}")
```

## 输出结果

### JSON结果

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
    }
  ]
}
```

## 与其他技能的关联

```
ieee3_prep
    ↓ (准备EMT模型)
emt_simulation
    ↓ (波形数据)
visualize, waveform_export, disturbance_severity
```

## 性能特点

- **仿真时间**: IEEE3约30-60秒，IEEE39约5-15分钟
- **步长影响**: 步长越小精度越高但时间越长
- **内存占用**: 与系统规模和仿真时长成正比
- **建议步长**: 50Hz系统用0.0001s（10kHz采样）

## 常见问题

### 问题1: EMT拓扑检查失败

**原因**: 模型未配置EMT拓扑

**解决**:
```bash
# 先运行ieee3_prep准备模型
python -m cloudpss_skills run --config config/ieee3_prep.yaml
```

### 问题2: 仿真超时

**原因**: 仿真时间过长或系统复杂

**解决**:
```yaml
simulation:
  duration: 5.0       # 缩短时长
  timeout: 600        # 增加超时
```

### 问题3: 波形数据为空

**原因**: 未配置输出通道或模型无测量元件

**解决**: 确保模型包含测量元件（电压表、电流表）

## 配置示例

### 快速仿真

```yaml
skill: emt_simulation
model:
  rid: model/holdme/IEEE3
simulation:
  duration: 5.0
```

### 完整配置

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
  channels: ["Bus1_V", "Bus2_V", "Bus3_V"]
```

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
