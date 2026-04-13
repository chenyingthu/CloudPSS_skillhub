# 自动量测配置技能 (Auto Channel Setup)

## 设计背景

### 研究对象

在EMT（电磁暂态）仿真中，配置输出通道是一项繁琐但必要的工作。一个中等规模的电网模型可能包含数十条母线、多条线路和变压器，手动为每个元件添加电压、电流、功率等量测通道不仅耗时，还容易遗漏关键量测点。自动量测配置技能旨在解决这一问题，实现批量、智能化的量测通道配置。

### 实际需求

1. **批量配置**: 为所有母线自动添加电压量测，避免手动逐一配置
2. **电压等级筛选**: 根据研究需要，只关注特定电压等级（如220kV及以上）的母线
3. **多类型量测**: 支持电压、电流、功率、频率等多种量测类型的批量配置
4. **预览功能**: 在正式修改模型前预览将要添加的量测配置
5. **配置报告**: 生成详细的量测配置报告，便于后续分析

### 期望的输入和输出

**输入**:

- 模型RID（本地或云端）
- 量测类型配置（电压/电流/功率/频率的启用状态和参数）
- 筛选条件（电压等级、母线名称等）
- 采样频率设置
- 输出选项（是否保存模型、是否试运行）

**输出**:

- 量测配置报告（JSON格式）
- 各类型量测通道数量统计
- 建议的输出配置（按类型和频率分组）
- 修改后的模型（可选）

### 计算结果的用途和价值

自动量测配置结果可直接用于：

- **快速仿真准备**: 大幅缩短EMT仿真前的配置时间
- **标准化量测**: 确保关键量测点不被遗漏，提高仿真结果的完整性
- **批量研究**: 支持多场景、多模型的批量仿真准备工作
- **团队协作**: 通过配置报告共享量测配置方案

## 功能特性

- **批量配置**: 一键为所有符合条件的元件添加量测通道
- **灵活筛选**: 支持按电压等级、母线名称等条件筛选目标元件
- **多类型支持**: 电压、电流、功率（P/Q）、频率四种量测类型
- **试运行模式**: 预览配置效果而不实际修改模型
- **智能分组**: 自动生成按类型和采样频率分组的输出配置建议

## 快速开始

### CLI方式（推荐）

```bash
# 基础配置（为所有母线添加电压量测）
python -m cloudpss_skills run --config config_auto_channel.yaml
```

### 配置示例

```yaml
skill: auto_channel_setup
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
  source: cloud
measurements:
  voltage:
    enabled: true
    voltage_levels: [220, 500]  # 只配置220kV和500kV母线
    bus_names: []  # 空数组表示全部
    freq: 200
  current:
    enabled: true
    component_types: [line, transformer]
    freq: 200
  power:
    enabled: true
    component_types: [generator, load]
    freq: 200
output:
  save_model: false
  dry_run: false
```

## 配置参数详解

### model（模型配置）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `rid` | string | ✅ | - | 模型RID或本地路径 |
| `source` | string | ❌ | "cloud" | 模型来源：cloud/local |

### measurements.voltage（电压量测）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `enabled` | boolean | ❌ | true | 是否启用电压量测 |
| `voltage_levels` | array | ❌ | [] | 电压等级筛选(kV)，空数组表示全部 |
| `bus_names` | array | ❌ | [] | 母线名称筛选，空数组表示全部 |
| `freq` | integer | ❌ | 200 | 采样频率(Hz) |

### measurements.current（电流量测）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `enabled` | boolean | ❌ | false | 是否启用电流量测 |
| `component_types` | array | ❌ | ["line", "transformer"] | 元件类型：line/transformer |
| `freq` | integer | ❌ | 200 | 采样频率(Hz) |

### measurements.power（功率量测）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `enabled` | boolean | ❌ | false | 是否启用功率量测 |
| `component_types` | array | ❌ | ["generator", "load"] | 元件类型：generator/load/line |
| `freq` | integer | ❌ | 200 | 采样频率(Hz) |

### measurements.frequency（频率量测）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `enabled` | boolean | ❌ | false | 是否启用频率量测 |
| `freq` | integer | ❌ | 50 | 采样频率(Hz) |

### output（输出配置）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `save_model` | boolean | ❌ | false | 是否保存修改后的模型 |
| `dry_run` | boolean | ❌ | false | 仅预览不修改 |

## 配置示例

### 示例1：基础电压量测

```yaml
skill: auto_channel_setup
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
measurements:
  voltage:
    enabled: true
    freq: 200
output:
  save_model: false
```

### 示例2：指定电压等级

```yaml
skill: auto_channel_setup
model:
  rid: model/holdme/IEEE39
measurements:
  voltage:
    enabled: true
    voltage_levels: [500]  # 只配置500kV母线
    freq: 500
  current:
    enabled: true
    component_types: [line]
    freq: 500
output:
  dry_run: true  # 先预览
```

### 示例3：完整量测配置

```yaml
skill: auto_channel_setup
model:
  rid: model/holdme/IEEE39
measurements:
  voltage:
    enabled: true
    voltage_levels: [220, 500]
    freq: 200
  current:
    enabled: true
    component_types: [line, transformer]
    freq: 200
  power:
    enabled: true
    component_types: [generator, load]
    freq: 200
  frequency:
    enabled: true
    freq: 50
output:
  save_model: true
```

## 输出结果说明

### SkillResult结构

```json
{
  "skill_name": "auto_channel_setup",
  "status": "SUCCESS",
  "data": {
    "model_rid": "model/holdme/IEEE39",
    "model_name": "IEEE39",
    "total_channels": 156,
    "voltage_channels": 39,
    "current_channels": 46,
    "power_channels": 71,
    "frequency_channels": 5,
    "dry_run": false,
    "saved": true
  },
  "artifacts": [
    {
      "type": "json",
      "path": "./results/auto_channel_setup_report.json",
      "description": "量测配置报告"
    }
  ]
}
```

### 配置报告结构

```json
{
  "summary": {
    "total": 156,
    "by_type": {
      "voltage": 39,
      "current": 46,
      "power": 71,
      "frequency": 5
    }
  },
  "channels": [
    {
      "type": "voltage",
      "component": "Bus30",
      "pin": "#Bus30.Vrms",
      "v_base": 220,
      "freq": 200,
      "dim": 1
    }
  ],
  "suggested_output_config": [
    {
      "plot_name": "Voltage_200Hz",
      "freq": 200,
      "channels": ["#Bus30", "#Bus31", ...]
    }
  ]
}
```

## 设计原理

### 量测配置流程

```
1. 加载模型 → 从CloudPSS获取模型数据
2. 筛选元件 → 根据配置条件筛选目标母线/线路/变压器等
3. 配置量测 → 为每个元件添加对应的量测点
4. 生成报告 → 汇总所有配置信息
5. 保存模型（可选）→ 将修改后的模型保存回云端
```

### 量测点映射规则

- **电压量测**: 使用母线元件的 `Vrms` 量测点
- **电流量测**: 线路使用 `Is`（送端电流），变压器使用 `I1`（一次侧电流）
- **功率量测**: 有功功率 `P` 和无功功率 `Q` 分别配置
- **频率量测**: 使用母线的 `Freq` 量测点（通过PLL计算）

### 筛选逻辑

- **电压等级筛选**: `v_base` 必须在 `voltage_levels` 列表中（如果列表非空）
- **名称筛选**: `bus_name` 必须在 `bus_names` 列表中（如果列表非空）
- **逻辑关系**: 两个筛选条件为 AND 关系

## 使用场景

### 场景1：快速EMT仿真准备

为新模型快速配置基础量测，确保关键量测点不遗漏。

```yaml
measurements:
  voltage:
    enabled: true
    freq: 200
  current:
    enabled: true
    component_types: [line]
    freq: 200
output:
  save_model: true
```

### 场景2：高压侧重点监控

只关注高压侧（220kV及以上）母线和线路的量测。

```yaml
measurements:
  voltage:
    enabled: true
    voltage_levels: [220, 500]
    freq: 500
  current:
    enabled: true
    component_types: [line, transformer]
    freq: 500
```

### 场景3：故障分析专用配置

为故障分析配置详细的量测，包括功率和频率。

```yaml
measurements:
  voltage:
    enabled: true
    freq: 1000  # 高采样率
  current:
    enabled: true
    freq: 1000
  power:
    enabled: true
    component_types: [generator, load, line]
    freq: 1000
  frequency:
    enabled: true
    freq: 100
```

## 注意事项

1. **试运行模式**: 建议在首次配置时启用 `dry_run: true`，预览配置效果后再实际修改
2. **模型保存**: `save_model: true` 会修改云端模型，请谨慎使用
3. **采样频率**: 根据仿真需求选择合适的采样频率，过高会增加存储开销
4. **量测点冲突**: 如果模型中已存在同名量测点，技能会自动跳过

## 故障排除

### 问题1："没有找到符合条件的母线"

**原因**: 电压等级筛选条件过于严格
**解决**: 检查 `voltage_levels` 是否与实际模型的电压等级匹配

### 问题2："量测点添加失败"

**原因**: 模型元件缺少必要的参数
**解决**: 检查模型元件是否完整，特别是 `VBase` 和 `Name` 参数

### 问题3："保存模型失败"

**原因**: 权限不足或模型被锁定
**解决**: 确认Token有写权限，或尝试保存为新分支

## 相关技能

- **emt_simulation**: EMT仿真执行，支持故障参数和采样频率配置
- **waveform_export**: 波形导出，处理仿真后的量测数据
- **hdf5_export**: HDF5格式导出，适合大量测数据的存储

## 完整示例

### 场景描述

对IEEE39系统进行全面量测配置，为后续的暂态稳定分析做准备。

### 配置文件

```yaml
skill: auto_channel_setup
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
  source: cloud
measurements:
  voltage:
    enabled: true
    voltage_levels: [220, 500]
    bus_names: []
    freq: 200
  current:
    enabled: true
    component_types: [line, transformer]
    freq: 200
  power:
    enabled: true
    component_types: [generator, load]
    freq: 200
  frequency:
    enabled: true
    freq: 50
output:
  save_model: false
  dry_run: false
```

### 执行命令

```bash
python -m cloudpss_skills run --config config_auto_channel.yaml
```

### 预期输出

```
[INFO] 加载认证信息...
[INFO] 认证成功
[INFO] 加载模型: model/holdme/IEEE39
[INFO] 模型名称: IEEE39
[INFO] 配置电压量测...
[INFO]   -> 添加 39 个电压量测通道
[INFO] 配置电流量测...
[INFO]   -> 添加 46 个电流量测通道
[INFO] 配置功率量测...
[INFO]   -> 添加 71 个功率量测通道
[INFO] 配置频率量测...
[INFO]   -> 添加 5 个频率量测通道
[INFO] 生成配置报告...
[INFO] 配置完成！共添加 161 个量测通道
```

### 结果应用

1. **查看报告**: 打开 `results/auto_channel_setup_report.json` 查看详细配置
2. **EMT仿真**: 使用配置好的量测通道执行EMT仿真
3. **数据分析**: 根据建议的输出配置导出波形数据

---

*该技能基于CloudPSS SDK开发，遵循技能系统架构规范*
