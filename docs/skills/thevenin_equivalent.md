# PCC戴维南等值技能 (thevenin_equivalent)

## 设计背景

### 研究对象
戴维南等值是电力系统分析中的基础方法，通过在指定母线（Point of Common Coupling, PCC）处构造一个等值电压源和串联阻抗来近似外部系统的行为。这对于分析新能源接入、弱电网特性、故障计算等场景至关重要。

### 实际需求
1. **新能源并网评估**：需要计算PCC点的短路比(SCR)来判断电网强度
2. **弱电网分析**：识别接入点是否为弱电网，决定是否需要额外电压支撑
3. **等值网络构建**：为后续小信号/暂态稳定性分析提供简化的系统模型

### 期望的输入和输出

**输入**:
- 电力系统模型（RID或本地文件）
- PCC母线名称（支持多种命名格式：bus8/Bus8/BUS_8）
- 系统基准容量（默认100MVA）

**输出**:
- PCC戴维南等值阻抗 Zth（标幺值）
- 短路容量 Ssc（MVA）
- 短路比 SCR（若提供新能源额定容量）

### 计算结果的用途和价值
- 直接用于新能源接入可行性评估
- 判断电网强弱（ SCR > 3 为强电网）
- 为其他分析技能提供等值参数

## 功能特性

- **精确阻抗计算**：基于拓扑正序网络构造PCC戴维南等值阻抗
- **多格式母线识别**：支持多种命名格式自动归一化
- **短路比计算**：可顺带计算SCR用于电网强度评估
- **多系统基准支持**：可配置系统基准容量
- **标准化输出**：JSON格式结果，便于后续处理

## 快速开始

### 3.1 CLI方式（推荐）

```bash
python -m cloudpss_skills run --config thevenin_config.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills.builtin.thevenin_equivalent import TheveninEquivalentSkill

skill = TheveninEquivalentSkill()
config = skill.get_default_config()
config["model"]["rid"] = "model/holdme/IEEE39"
config["pcc"]["bus"] = "bus8"
config["equivalent"]["system_base_mva"] = 100.0
config["equivalent"]["rating_mva"] = 100.0  # 计算SCR

result = skill.run(config)
print(f"Zth = {result.data['z_th_pu']}")
print(f"SCR = {result.data.get('scr')}")
```

### 3.3 YAML配置示例

```yaml
skill: thevenin_equivalent
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
  source: cloud
pcc:
  bus: bus8
equivalent:
  system_base_mva: 100.0
  rating_mva: 100.0  # 可选，提供则计算SCR
output:
  format: json
  path: ./results/
  prefix: thevenin_ieee39_bus8
  timestamp: true
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: thevenin_equivalent
auth:
  token: <string>           # 可选，直接提供token
  token_file: .cloudpss_token  # 默认token文件
model:
  rid: <string>             # 模型RID或本地路径
  source: cloud | local     # 默认cloud
pcc:
  bus: <string>             # PCC母线名称
equivalent:
  system_base_mva: 100.0    # 系统基准容量
  rating_mva: <number>       # 可选，新能源额定容量（用于SCR计算）
output:
  format: json              # 默认json
  path: ./results/          # 输出目录
  prefix: thevenin_equivalent  # 文件前缀
  timestamp: true           # 是否添加时间戳
```

### 4.2 参数说明

| 参数路径 | 类型 | 必填 | 默认值 | 说明 |
|---------|------|------|--------|------|
| skill | string | 是 | - | 固定值 `thevenin_equivalent` |
| auth.token | string | 否 | - | API token |
| auth.token_file | string | 否 | .cloudpss_token | token文件路径 |
| model.rid | string | 是 | - | 模型RID或本地路径 |
| model.source | enum | 否 | cloud | 模型来源 |
| pcc.bus | string | 是 | - | PCC母线名称 |
| equivalent.system_base_mva | number | 否 | 100.0 | 系统基准容量(MVA) |
| equivalent.rating_mva | number | 否 | - | 新能源额定容量(MVA)，提供则计算SCR |
| output.format | enum | 否 | json | 输出格式 |
| output.path | string | 否 | ./results/ | 输出目录 |
| output.prefix | string | 否 | thevenin_equivalent | 文件前缀 |
| output.timestamp | boolean | 否 | true | 是否添加时间戳 |

## Agent使用指南

### 5.1 基本调用模式

```python
from cloudpss_skills.builtin.thevenin_equivalent import TheveninEquivalentSkill

skill = TheveninEquivalentSkill()
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "pcc": {"bus": "bus8"},
    "equivalent": {"system_base_mva": 100.0, "rating_mva": 100.0}
}
result = skill.run(config)
```

### 5.2 处理结果

```python
# 检查执行状态
if result.status == SkillStatus.SUCCESS:
    # 读取结果数据
    z_th = result.data["z_th_pu"]
    s_sc = result.data["short_circuit_capacity_mva"]
    scr = result.data.get("scr")  # 可能不存在
    
    # 读取输出文件
    for artifact in result.artifacts:
        print(f"生成文件: {artifact.path}")
elif result.status == SkillStatus.FAILED:
    print(f"执行失败: {result.error}")
```

### 5.3 错误处理

```python
try:
    result = skill.run(config)
    if result.status == SkillStatus.FAILED:
        logger.error(f"计算失败: {result.error}")
except ValidationError as e:
    logger.error(f"配置验证失败: {e}")
except FileNotFoundError as e:
    logger.error(f"Token文件不存在: {e}")
except RuntimeError as e:
    logger.error(f"戴维南等值计算失败: {e}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "model_rid": "model/holdme/IEEE39",
  "model_name": "IEEE39",
  "pcc_bus": "bus8",
  "bus_node": "NODE_1010",
  "bus_nominal_voltage_kv": 345.0,
  "system_base_mva": 100.0,
  "z_th_pu": {
    "real": 0.012345,
    "imag": 0.045678,
    "magnitude": 0.047123
  },
  "short_circuit_capacity_mva": 2122.17,
  "rating_mva": 100.0,
  "scr": 21.22,
  "verified": true
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| skill_name | string | 技能名称 |
| status | SkillStatus | 执行状态 |
| data | dict | 结果数据 |
| artifacts | list | 输出文件列表 |
| logs | list | 执行日志 |
| error | string | 错误信息（失败时） |

## 与其他技能的关联

```
                    ┌─────────────────┐
                    │thevenin_equivalent│
                    └────────┬────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
    ┌────────────┐   ┌────────────┐   ┌────────────┐
    │  renewable │   │  voltage   │   │  short     │
    │ _integration│   │ _stability │   │ _circuit   │
    └────────────┘   └────────────┘   └────────────┘
```

- **renewable_integration**：使用SCR评估新能源接入可行性
- **voltage_stability**：基于戴维南阻抗分析电压稳定性
- **short_circuit**：与短路计算共享阻抗计算基础

## 性能特点

- **计算速度快**：仅需拓扑分析，无需仿真
- **内存占用低**：纯计算密集型
- **准确度高**：基于完整拓扑结构
- **适用性广**：支持任意母线位置的等值计算

## 常见问题

**Q1: 计算结果verified=false是什么原因？**
A1: 通常是PCC母线在拓扑中无法定位，可能是母线名称拼写错误或该母线不在正序网络中。

**Q2: 如何选择合适的PCC母线？**
A2: PCC通常选择新能源接入点或系统关注的关键母线。确保母线名称与模型中的label或pins匹配。

**Q3: system_base_mva对结果有什么影响？**
A3: system_base_mva影响阻抗的标幺值。确保与新能源容量基准一致，以便正确计算SCR。

**Q4: SCR的计算标准是什么？**
A4: SCR = Ssc / Pn，其中Ssc为短路容量，Pn为新能源额定功率。SCR > 3为强电网，SCR < 2为弱电网。

## 完整示例

### 场景描述
某风电场计划接入IEEE39系统的Bus8，需要评估该接入点的电网强度。

### 配置文件
```yaml
skill: thevenin_equivalent
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
  source: cloud
pcc:
  bus: bus8
equivalent:
  system_base_mva: 100.0
  rating_mva: 100.0
output:
  format: json
  path: ./results/
  prefix: wind_farm_pcc_analysis
  timestamp: true
```

### 执行命令
```bash
python -m cloudpss_skills run --config thevenin_config.yaml
```

### 预期输出
```
[INFO] 计算PCC戴维南等值: model=model/holdme/IEEE39, bus=bus8
[INFO] Zth={'real': 0.012345, 'imag': 0.045678, 'magnitude': 0.047123}, Ssc=2122.17 MVA
[INFO] 结果已保存: ./results/wind_farm_pcc_analysis_20260410_153000.json
```

### 结果文件
```json
{
  "model_rid": "model/holdme/IEEE39",
  "pcc_bus": "bus8",
  "bus_node": "NODE_1010",
  "bus_nominal_voltage_kv": 345.0,
  "system_base_mva": 100.0,
  "z_th_pu": {
    "real": 0.012345,
    "imag": 0.045678,
    "magnitude": 0.047123
  },
  "short_circuit_capacity_mva": 2122.17,
  "rating_mva": 100.0,
  "scr": 21.22,
  "verified": true
}
```

### 结论解读
SCR = 21.22 > 3，表明Bus8为强电网，风电场可以正常接入。

## 版本信息

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0.0 | 2026-04-01 | 初始版本 |

## 相关文档

- [renewable_integration.md](./renewable_integration.md) - 新能源接入评估
- [voltage_stability.md](./voltage_stability.md) - 电压稳定性分析
- [short_circuit.md](./short_circuit.md) - 短路计算
