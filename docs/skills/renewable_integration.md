# 新能源接入评估技能 (renewable_integration)

## 设计背景

### 研究对象
新能源（光伏、风电）接入电网时的系统影响评估。新能源大规模并网带来了一系列技术挑战，包括电网强度降低、电压波动、谐波注入、低电压穿越(LVRT)能力等问题。

### 实际需求
1. **接入可行性评估**：判断新能源能否安全接入指定电网点
2. **电网强度分析**：通过短路比(SCR)量化电网强弱
3. **电能质量评估**：分析电压波动和谐波注入影响
4. **并网合规性验证**：验证LVRT等并网标准要求
5. **稳定性影响评估**：评估对系统稳定性的影响

### 期望的输入和输出

**输入**:
- 含新能源的电力系统模型
- 新能源类型（pv/wind）、接入母线、额定容量
- 分析开关配置（各项分析可独立启用）
- 评估标准和阈值

**输出**:
- 短路比(SCR)及电网强度评估
- 电压波动分析结果
- 谐波注入评估
- LVRT合规性验证结果
- 稳定性影响评估
- 综合评估结论和建议

### 计算结果的用途和价值
- 指导新能源项目选址
- 确定并网条件和要求
- 为项目审批提供依据
- 指导无功补偿配置
- 为后续运行提供参考

## 功能特性

- **短路比(SCR)计算**：基于拓扑正序网络构造PCC戴维南等值阻抗，准确计算SCR
- **电压波动分析**：对比新能源接入前后电压变化，支持5%偏差容忍度配置
- **谐波注入评估**：基于典型值估算各次谐波含量和THD
- **LVRT合规性验证**：支持GB/T 19964-2012和IEEE 1547-2018标准
- **稳定性影响评估**：对比接入前后电压稳定性变化
- **自动新能源识别**：从模型拓扑自动识别新能源组件
- **综合评估报告**：生成包含结论、建议和限制的完整报告

## 快速开始

### 3.1 CLI方式（推荐）

```bash
python -m cloudpss_skills run --config renewable_config.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills.builtin.renewable_integration import RenewableIntegrationSkill
from cloudpss_skills import SkillStatus

skill = RenewableIntegrationSkill()
config = {
    "model": {"rid": "model/holdme/IEEE39_with_PV"},
    "renewable": {
        "type": "pv",
        "bus": "BUS_10",
        "capacity": 100
    },
    "analysis": {
        "scr": {"enabled": True, "threshold": 3.0},
        "voltage_variation": {"enabled": True},
        "harmonic_injection": {"enabled": True},
        "lvrt_compliance": {"enabled": True, "standard": "gb"},
        "stability_impact": {"enabled": True}
    },
    "output": {"format": "json", "path": "./results/"}
}
result = skill.run(config)
```

### 3.3 YAML配置示例

```yaml
skill: renewable_integration
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39_with_PV
  source: cloud
renewable:
  type: pv
  bus: BUS_10
  capacity: 100
analysis:
  scr:
    enabled: true
    threshold: 3.0
  voltage_variation:
    enabled: true
    tolerance: 0.05
  harmonic_injection:
    enabled: true
    limits:
      thd: 0.05
  lvrt_compliance:
    enabled: true
    standard: gb
  stability_impact:
    enabled: true
output:
  format: json
  path: ./renewable_report.json
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: renewable_integration
auth:
  token: <string>
  token_file: .cloudpss_token
model:
  rid: <string>
  source: cloud | local
renewable:
  type: pv | wind
  bus: <string>
  capacity: <number>  # MW
analysis:
  scr:
    enabled: true
    threshold: 3.0
  voltage_variation:
    enabled: true
    tolerance: 0.05
  harmonic_injection:
    enabled: true
    limits:
      thd: 0.05
  lvrt_compliance:
    enabled: true
    standard: gb | ieee | iec
  stability_impact:
    enabled: true
output:
  format: json | console
  path: <string>
```

### 4.2 参数说明

| 参数路径 | 类型 | 必填 | 默认值 | 说明 |
|---------|------|------|--------|------|
| skill | string | 是 | - | 固定值 |
| renewable.type | enum | 否 | pv | 新能源类型 |
| renewable.bus | string | 否 | - | 接入母线（可选） |
| renewable.capacity | number | 否 | - | 额定容量(MW)，未提供则自动识别 |
| analysis.scr.threshold | number | 否 | 3.0 | SCR判定阈值 |
| analysis.voltage_variation.tolerance | number | 否 | 0.05 | 电压偏差容忍度(pu) |
| analysis.harmonic_injection.limits.thd | number | 否 | 0.05 | THD限值 |
| analysis.lvrt_compliance.standard | enum | 否 | gb | LVRT标准 |

## Agent使用指南

### 5.1 基本调用模式

```python
skill = RenewableIntegrationSkill()
result = skill.run(config)

if result.status == SkillStatus.SUCCESS:
    report = result.data
    print(f"评估结论: {report['summary']['assessment']}")
```

### 5.2 处理结果

```python
# SCR分析
scr_result = result.data["analysis_results"]["scr"]
print(f"SCR: {scr_result['scr']}")
print(f"电网强度: {scr_result['grid_strength']}")

# 电压波动
voltage = result.data["analysis_results"]["voltage_variation"]
print(f"最大电压变化: {voltage['max_voltage_change_percent']}%")

# LVRT
lvrt = result.data["analysis_results"]["lvrt_compliance"]
print(f"LVRT合规: {lvrt['compliant']}")

# 综合结论
summary = result.data["summary"]
print(f"通过项: {summary['passed']}/{summary['total_analysis']}")
for rec in summary.get("recommendations", []):
    print(f"建议: {rec}")
```

### 5.3 错误处理

```python
try:
    result = skill.run(config)
except (KeyError, AttributeError) as e:
    print(f"配置错误: {e}")
except RuntimeError as e:
    print(f"仿真失败: {e}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "model_rid": "model/holdme/IEEE39_with_PV",
  "timestamp": "2026-04-10T15:30:00",
  "analysis_results": {
    "scr": {
      "scr": 4.52,
      "short_circuit_capacity_mva": 452.0,
      "renewable_capacity_mw": 100.0,
      "grid_strength": "强电网",
      "passed": true,
      "verified": true
    },
    "voltage_variation": {
      "max_voltage_change_pu": 0.012,
      "max_voltage_change_percent": 1.2,
      "passed": true,
      "verified": true
    },
    "harmonic_injection": {
      "thd_percent": 3.8,
      "thd_limit_percent": 5.0,
      "passed": true,
      "verified": false,
      "warning": "此结果是基于典型值的简化估算"
    },
    "lvrt_compliance": {
      "standard": "GB/T 19964-2012",
      "supported": true,
      "compliant": false,
      "verified": false,
      "warning": "当前仅确认模型具备LVRT能力"
    },
    "stability_impact": {
      "overall_stability": "good",
      "passed": true,
      "verified": true
    }
  },
  "summary": {
    "total_analysis": 5,
    "passed": 3,
    "overall_passed": false,
    "overall_verified": false,
    "certifiable": false,
    "assessment": "仅供初步评估",
    "recommendations": [
      "当前仍包含未完成真实仿真验证的分析项"
    ]
  }
}
```

### 6.2 评估结论说明

| 状态 | 说明 |
|------|------|
| certifiable=true | 所有分析均通过且verified=true，可作为正式评估结论 |
| certifiable=false | 包含估算或假设结果，仅供初步评估参考 |

## 与其他技能的关联

```
                         ┌──────────────────────┐
                         │renewable_integration │
                         └──────────┬───────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
 ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
 │  thevenin_      │      │   voltage_      │      │    short_       │
 │  equivalent     │      │   stability     │      │    circuit      │
 └─────────────────┘      └─────────────────┘      └─────────────────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │      power_flow              │
                    └─────────────────────────────┘
```

- **thevenin_equivalent**：SCR计算依赖戴维南等值阻抗
- **voltage_stability**：电压波动与稳定性分析相关
- **power_flow**：潮流计算是各项分析的基础
- **short_circuit**：短路计算支持SCR评估

## 性能特点

- **分析项目多**：包含5大分析模块
- **部分需仿真**：SCR、电压分析需要运行潮流
- **LVRT验证复杂**：需要EMT仿真和波形分析
- **运行时间长**：完整评估可能需要5-10分钟

## 常见问题

**Q1: verified=false的结果可靠吗？**
A1: verified=false表示结果基于估算或典型值，仅供初步评估参考，不能作为正式并网验证结论。

**Q2: 如何提高评估可信度？**
A2: 1) 确保模型包含完整的LVRT控制逻辑；2) 配置EMT仿真方案和输出通道；3) 使用真实故障场景进行验证。

**Q3: SCR计算需要什么前提条件？**
A3: 模型需要包含正序网络拓扑，且PCC母线能够正确定位。新能源组件应能被自动识别。

**Q4: harmonic_injection为什么总是verified=false？**
A4: 谐波分析需要EMT仿真获取波形后进行FFT分析，当前版本使用典型值估算，未来版本将支持真实仿真验证。

**Q5: 为什么LVRT返回supported=true但compliant=false？**
A5: 表示模型具备LVRT控制/保护逻辑，但尚未完成真实故障跌落与状态量测的闭环验证。

## 完整示例

### 场景描述
某100MW光伏电站计划接入IEEE39系统的Bus10，评估其并网可行性。

### 配置文件
```yaml
skill: renewable_integration
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39_with_PV
  source: cloud
renewable:
  type: pv
  bus: BUS_10
  capacity: 100
analysis:
  scr:
    enabled: true
    threshold: 3.0
  voltage_variation:
    enabled: true
    tolerance: 0.05
  harmonic_injection:
    enabled: true
    limits:
      thd: 0.05
  lvrt_compliance:
    enabled: true
    standard: gb
  stability_impact:
    enabled: true
output:
  format: json
  path: ./results/pv100_bus10_assessment.json
```

### 执行命令
```bash
python -m cloudpss_skills run --config renewable_config.yaml
```

### 预期输出
```
[INFO] 开始新能源接入评估: model/holdme/IEEE39_with_PV
[INFO] 计算短路比(SCR)...
[INFO] 分析电压波动...
[INFO] 评估谐波注入...
[INFO] 验证低电压穿越(LVRT)...
[INFO] 评估稳定性影响...
[INFO] 新能源接入评估完成
```

### 结果解读

**SCR分析**：SCR=4.52 > 3.0，强电网，可以接入

**电压波动**：最大变化1.2% < 5%，通过

**谐波（估算）**：THD=3.8% < 5%，通过（但需真实仿真验证）

**LVRT**：模型具备LVRT能力，建议后续进行专项验证

**综合结论**：除LVRT需专项验证外，各项指标满足并网要求

## 版本信息

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0.0 | 2026-04-01 | 初始版本，支持SCR、电压波动、谐波、LVRT、稳定性分析 |

## 相关文档

- [thevenin_equivalent.md](./thevenin_equivalent.md) - 戴维南等值计算
- [voltage_stability.md](./voltage_stability.md) - 电压稳定性分析
- [emt_fault_study.md](./emt_fault_study.md) - EMT故障分析（LVRT验证基础）
- [power_flow.md](./power_flow.md) - 潮流计算基础
