# 保护整定与配合分析技能 (protection_coordination)

## 设计背景

### 研究对象
继电保护是电力系统安全运行的最后一道防线。保护整定是指根据系统参数和保护设备特性，确定保护装置的动作参数（定值）。保护配合是指主保护与后备保护、主保护与相邻保护之间的时间、电流、阻抗等参数的协调关系，确保故障时正确隔离故障区域。

### 实际需求
1. **保护定值计算**：根据系统参数计算保护装置的启动值、延时等参数
2. **配合关系校验**：验证上下级保护的配合关系是否满足选择性要求
3. **保护动作分析**：仿真故障时各保护的动作行为
4. **TCC曲线生成**：生成时间-电流配合曲线用于整定参考

### 期望的输入和输出

**输入**:
- 电力系统模型（含保护配置）
- 分析类型开关
- 故障场景配置
- 配合时间裕度要求

**输出**:
- 识别到的保护装置清单
- 距离保护定值分析
- 过流保护定值与配合分析
- 差动保护定值分析
- 零序保护配置统计
- 重合闸配置统计
- 故障场景动作分析
- TCC配合曲线数据

### 计算结果的用途和价值
- 指导保护装置定值整定
- 发现保护配合问题
- 优化保护配置方案
- 生成整定报告

## 功能特性

- **自动保护识别**：从模型配置中自动识别各类保护装置
- **距离保护分析**：Zone1/2/3定值计算与校验
- **过流保护分析**：启动值计算、时间配合校验
- **差动保护分析**：变压器差动保护定值计算
- **零序保护统计**：接地故障保护配置统计
- **重合闸分析**：重合闸配置与延时分析
- **故障场景仿真**：分析特定故障下保护动作
- **TCC曲线生成**：生成时间-电流配合曲线数据

## 快速开始

### 3.1 CLI方式（推荐）

```bash
python -m cloudpss_skills run --config protection_config.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills.builtin.protection_coordination import ProtectionCoordinationSkill

skill = ProtectionCoordinationSkill()
config = {
    "model": {"rid": "model/holdme/substation_110"},
    "analysis": {
        "distance_protection": {"enabled": True, "check_zones": [1, 2, 3]},
        "overcurrent_protection": {"enabled": True, "check_coordination": True},
        "differential_protection": {"enabled": True},
        "fault_scenarios": [
            {"type": "three_phase", "location": "LINE_110kV_L1", "duration": 0.1}
        ]
    },
    "output": {"format": "json"}
}
result = skill.run(config)
```

### 3.3 YAML配置示例

```yaml
skill: protection_coordination
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/substation_110
analysis:
  distance_protection:
    enabled: true
    check_zones: [1, 2, 3]
  overcurrent_protection:
    enabled: true
    check_coordination: true
    time_margin: 0.3
  differential_protection:
    enabled: true
  zero_sequence_protection:
    enabled: true
  reclosing:
    enabled: true
  fault_scenarios:
    - type: three_phase
      location: LINE_110kV_L1
      duration: 0.1
output:
  format: json
  generate_tcc_curves: true
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: protection_coordination
auth:
  token: <string>
  token_file: .cloudpss_token
  server: public | internal
model:
  rid: <string>
  config_index: 0
  job_index: 0
analysis:
  distance_protection:
    enabled: true
    check_zones: [1, 2, 3]
  overcurrent_protection:
    enabled: true
    check_coordination: true
    time_margin: 0.3
  differential_protection:
    enabled: true
  zero_sequence_protection:
    enabled: true
  reclosing:
    enabled: true
  fault_scenarios:
    - type: three_phase | single_ground | line_to_line
      location: <string>
      fault_resistance: 0.0
      duration: 0.1
output:
  format: json | yaml
  save_path: <string>
  generate_tcc_curves: true
```

### 4.2 参数说明

| 参数路径 | 类型 | 必填 | 默认值 | 说明 |
|---------|------|------|--------|------|
| skill | string | 是 | - | 固定值 |
| analysis.distance_protection.check_zones | array | 否 | [1,2,3] | 需要检查的Zone |
| analysis.overcurrent_protection.time_margin | number | 否 | 0.3 | 配合时间裕度(s) |
| analysis.fault_scenarios[].type | enum | 否 | three_phase | 故障类型 |
| analysis.fault_scenarios[].location | string | 是 | - | 故障位置 |
| analysis.fault_scenarios[].duration | number | 否 | 0.1 | 故障持续时间(s) |

## Agent使用指南

### 5.1 基本调用模式

```python
skill = ProtectionCoordinationSkill()
result = skill.run(config)

if result.status == SkillStatus.SUCCESS:
    devices_found = result.data["protection_devices_found"]
    print(f"识别到{devices_found}个保护装置")
```

### 5.2 处理结果

```python
# 距离保护分析
distance_result = result.data["analysis_results"]["distance_protection"]
for relay in distance_result["zone_analysis"]:
    print(f"位置: {relay['location']}")
    for zone, info in relay["zones"].items():
        print(f"  {zone}: {info['reach_percent']}%/{info['time_delay_s']}s")

# 过流保护配合
oc_result = result.data["analysis_results"]["overcurrent_protection"]
for coord in oc_result["coordination_check"]:
    print(f"{coord['primary']} vs {coord['backup']}")
    print(f"  配合时间: {coord['time_margin']}s, 合格: {coord['is_valid']}")

# TCC曲线
if "tcc_curves" in result.data["analysis_results"]:
    tcc = result.data["analysis_results"]["tcc_curves"]
    for curve in tcc["curves"]:
        print(f"曲线: {curve['relay']} ({curve['curve_type']})")
```

### 5.3 错误处理

```python
try:
    result = skill.run(config)
except KeyError as e:
    print(f"配置缺少必要参数: {e}")
except ConnectionError as e:
    print(f"连接CloudPSS失败: {e}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "model": "model/holdme/substation_110",
  "protection_devices_found": 60,
  "distance_relays": 6,
  "overcurrent_relays": 45,
  "differential_relays": 9,
  "analysis_results": {
    "distance_protection": {
      "relay_count": 6,
      "zone_analysis": [
        {
          "location": "110kV_L1",
          "zones": {
            "zone1": {"reach_percent": 80, "time_delay_s": 0.0, "status": "configured"},
            "zone2": {"reach_percent": 120, "time_delay_s": 0.3, "status": "configured"},
            "zone3": {"reach_percent": 200, "time_delay_s": 0.6, "status": "configured"}
          }
        }
      ],
      "coordination_status": "valid"
    },
    "overcurrent_protection": {
      "relay_count": 45,
      "110kV_relays": 12,
      "10kV_relays": 33,
      "coordination_check": [
        {
          "primary": "10kV_L1",
          "backup": "110kV_L1",
          "time_margin": 0.5,
          "is_valid": true,
          "margin": 0.2
        }
      ],
      "time_margin_required_s": 0.3
    },
    "differential_protection": {
      "relay_count": 9,
      "transformer_relays": [...]
    },
    "zero_sequence_protection": {
      "relay_count": 15,
      "application": "ground_fault_detection",
      "typical_pickup": 0.1
    },
    "reclosing": {
      "total_configs": 8,
      "110kV_lines": 6,
      "10kV_lines": 2,
      "typical_delay_s": 1.0
    },
    "fault_scenarios": [...],
    "tcc_curves": {...}
  }
}
```

## 与其他技能的关联

```
                ┌────────────────────────┐
                │protection_coordination │
                └───────────┬────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
 ┌────────────┐    ┌────────────┐    ┌────────────┐
 │  power_    │    │   short_   │    │  transient_│
 │   flow     │    │  circuit   │    │  stability │
 └────────────┘    └────────────┘    └────────────┘
```

- **power_flow**：提供系统运行状态用于保护计算
- **short_circuit**：提供短路电流用于启动值整定
- **transient_stability**：提供暂态数据用于保护配合分析

## 性能特点

- **分析速度快**：基于配置解析，无需仿真
- **内存占用低**：纯数据处理
- **支持批量分析**：可同时分析多个故障场景
- **TCC曲线**：生成标准化配合曲线数据

## 常见问题

**Q1: 为什么识别到的保护装置数量与预期不符？**
A1: 保护配置可能使用不同的命名格式，检查模型配置中的参数命名是否包含关键字（juli, zero, oc, reclosure等）。

**Q2: 距离保护Zone定值是如何计算的？**
A2: Zone1=80%线路阻抗(瞬时)，Zone2=120%线路阻抗(0.3s)，Zone3=下级线路全长(0.6s)。

**Q3: 如何确保配合时间裕度满足要求？**
A3: 在analysis.overcurrent_protection.time_margin中设置要求值，默认0.3s表示110kV与10kV之间需至少0.3s配合时间。

**Q4: TCC曲线数据如何用于可视化？**
A4: tcc_curves字段包含曲线点数据，可导入MATLAB、Python matplotlib或Excel进行绘图。

## 完整示例

### 场景描述
某110kV变电站需要进行保护整定校核，验证距离保护和过流保护的配合关系。

### 配置文件
```yaml
skill: protection_coordination
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/substation_110
analysis:
  distance_protection:
    enabled: true
    check_zones: [1, 2, 3]
  overcurrent_protection:
    enabled: true
    check_coordination: true
    time_margin: 0.3
  differential_protection:
    enabled: true
  fault_scenarios:
    - type: three_phase
      location: 110kV_L1
      duration: 0.1
output:
  format: json
  generate_tcc_curves: true
```

### 执行命令
```bash
python -m cloudpss_skills run --config protection_config.yaml
```

### 预期输出
```
[INFO] 获取模型: model/holdme/substation_110
[INFO] 解析保护装置配置...
[INFO] 识别到60个保护装置
[INFO] 分析距离保护...
[INFO] 分析过流保护...
[INFO] 分析差动保护...
[INFO] 分析故障场景...
[INFO] 生成TCC配合曲线数据...
[INFO] 保护配合分析完成
```

### 结果解读

**距离保护**：6个距离继电器，Zone配置符合标准

**过流保护**：45个过流继电器，配合关系校验通过

**配合分析**：110kV与10kV之间配合时间满足0.3s裕度要求

## 版本信息

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0.0 | 2026-03-30 | 初始版本 |

## 相关文档

- [power_flow.md](./power_flow.md) - 潮流计算
- [short_circuit.md](./short_circuit.md) - 短路计算
- [transient_stability.md](./transient_stability.md) - 暂态稳定分析
