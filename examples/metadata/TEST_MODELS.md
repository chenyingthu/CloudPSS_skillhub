# CloudPSS 新能源测试算例

## 概述

本目录包含用于技能开发和测试的正式新能源算例。这些算例使用固定的分支名，可重复使用。

**重要更新**:
- 风电模型主线使用 `model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1`
- 光伏模型主线使用 `model/open-cloudpss/PVS_01-avm-stdm-v1b5`
- `WGSource_Bus30` 旧案例已退役，不再作为正式测试算例

## 测试模型列表

### 1. IEEE39 + 风电场 (PMSG)
- **模型ID**: `model/holdme/test_ieee39_wind`
- **分支名**: `test_ieee39_wind`
- **新能源组件**: `model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1` (永磁同步风机)
- **连接母线**: Bus10
- **总容量**: 100 MW (40台 × 2.5 MW)
- **关键参数**:
  - `Sbase`: 2.5 MVA (单台容量)
  - `Pctrl_mode`: '1' (PV节点控制)
  - `P_cmd`: 2.0 MW (有功指令)
  - `pf_P`: 2.0 MW (潮流有功)
  - `UnitCount`: 40 (风机台数)
- **创建命令**:
  ```bash
  python examples/metadata/create_test_models.py --wind
  ```

### 2. IEEE39 + 光伏电站
- **模型ID**: `model/holdme/test_ieee39_pv`
- **分支名**: `test_ieee39_pv`
- **新能源组件**: `model/open-cloudpss/PVS_01-avm-stdm-v1b5`
- **连接母线**: Bus14
- **额定功率**: 50 MW
- **创建命令**:
  ```bash
  python examples/metadata/create_test_models.py --pv
  ```

### 3. IEEE39 + 混合新能源
- **模型ID**: `model/holdme/test_ieee39_hybrid`
- **分支名**: `test_ieee39_hybrid`
- **新能源组件**:
  - `WTG_PMSG_01` (PMSG风机) - Bus10, 100 MW
  - `PVS_01-avm-stdm-v1b5` (光伏封装模型) - Bus14, 50 MW
- **创建命令**:
  ```bash
  python examples/metadata/create_test_models.py --hybrid
  ```

## 组件类型说明

### 风电组件对比

| 特性 | WGSource (旧) | WTG_PMSG_01 (新) |
|------|---------------|------------------|
| **组件ID** | `model/CloudPSS/WGSource` | `model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b1` |
| **潮流计算** | ❌ 不支持 | ✅ 完全支持 |
| **关键参数** | Vbase, Pnom, WindSpeed | Sbase, Pctrl_mode, P_cmd, pf_P |
| **控制模式** | 无 | PV/PQ/平衡节点 |
| **EMT仿真** | ✅ 支持 | ✅ 支持 |

### 关键潮流参数说明

对于 WTG_PMSG_01 组件，以下参数决定潮流计算行为：

```python
{
    'Pctrl_mode': '0',    # 控制模式: 0=PQ节点(推荐), 1=PV节点, 2=平衡节点
    'P_cmd': 2.0,         # 有功指令 (MW)
    'pf_P': 2.0,          # 潮流有功 (MW)
    'Q_cmd': 0.0,         # 无功指令 (Mvar, Pctrl_mode=0时使用)
    'pf_Q': 0.0,          # 潮流无功 (Mvar)
    'Sbase': 2.5,         # 基准容量 (MVA)
}
```

**节点类型选择建议**:

| 模式 | 类型 | 适用场景 | 说明 |
|------|------|---------|------|
| **'0'** | **PQ节点** | **新能源场站（推荐）** | 给定有功P和无功Q，电压自由变化。符合风电/光伏实际运行方式 |
| '1' | PV节点 | 带电压支撑的新能源 | 给定有功P和电压V，需要无功调节能力（配合SVG/SVC） |
| '2' | 平衡节点 | 独立微网/特殊场景 | 给定电压V和相角，用于功率平衡 |

**为什么新能源应该用 PQ节点？**
1. **实际运行特性** - 风电/光伏通过变流器并网，按照调度指令输出有功功率，不主动控制并网点电压
2. **电压由电网调节** - 系统电压由传统同步发电机、无功补偿设备等负责支撑
3. **符合调度习惯** - 调度部门通常只给新能源场站下发有功功率指令，不指定电压目标
4. **计算结果更合理** - PQ节点下新能源表现为"负荷型电源"，电压随系统变化，更符合物理实际

## 快速开始

### 创建所有测试模型

```bash
python examples/metadata/create_test_models.py --all
```

### 创建并验证

```bash
python examples/metadata/create_test_models.py --all --validate
```

### 验证元数据配置

```bash
python examples/metadata/validate_wtg_pmsg.py
```

### 查看帮助

```bash
python examples/metadata/create_test_models.py --help
```

## 使用示例

### 在技能配置中使用

```yaml
skill: power_flow
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/test_ieee39_wind  # 使用PMSG风电测试模型
  source: cloud
algorithm:
  type: newton_raphson
  tolerance: 1e-6
output:
  format: json
  path: ./results/
```

### 在Python代码中使用

```python
from cloudpss import Model

# 获取风电测试模型
model = Model.fetch('model/holdme/test_ieee39_wind')

# 运行潮流计算
job = model.runPowerFlow()
result = job.result

# 获取节点结果
buses = result.getBuses()
for bus in buses:
    print(f"{bus['name']}: V={bus['voltage']:.4f} p.u.")

# 验证新能源发电
# 总发电应比基准IEEE39增加约100MW（风电容量）
```

## 模型特点

### 风电模型 (test_ieee39_wind) - PMSG
- **正确参与潮流计算**: 使用 WTG_PMSG_01 组件，支持完整的潮流计算
- **完整参数**: 23个参数（包括潮流计算必需的 Pctrl_mode, P_cmd, pf_P 等）
- **等值风场**: 40台 × 2.5 MW = 100 MW总容量
- **控制模式**: PV节点控制 (Pctrl_mode='1')，支持电压调节
- **电气引脚**: 正确连接到Bus10

### 光伏模型 (test_ieee39_pv)
- 使用公开可访问且支持潮流的光伏封装模型 `PVS_01-avm-stdm-v1b5`
- 通过 `P_cmd / pf_P / pf_Q / Pctrl_mode` 控制潮流注入
- 电气引脚正确连接到 Bus14

### 混合模型 (test_ieee39_hybrid)
- 风电使用 PMSG 模型（支持潮流计算）
- 光伏使用简化模型
- 分布在不同母线 (Bus10和Bus14)
- 可用于研究多类型新能源并网的影响

## 验证状态

所有测试模型均经过以下验证：
- ✅ 拓扑验证：元件和连接正确
- ✅ 参数验证：所有参数完整且类型正确
- ✅ 引脚验证：电气引脚正确连接
- ✅ 潮流验证：能够成功运行潮流计算并正确显示新能源发电

### 潮流计算验证方法

```python
from cloudpss import Model

# 获取基准模型
base_model = Model.fetch('model/holdme/IEEE39')
base_job = base_model.runPowerFlow()
base_result = base_job.result

# 获取风电模型
wind_model = Model.fetch('model/holdme/test_ieee39_wind')
wind_job = wind_model.runPowerFlow()
wind_result = wind_job.result

# 对比总发电
base_gen = sum(b.get('generation', {}).get('P', 0) for b in base_result.getBuses())
wind_gen = sum(b.get('generation', {}).get('P', 0) for b in wind_result.getBuses())

print(f"基准总发电: {base_gen:.2f} MW")
print(f"风电总发电: {wind_gen:.2f} MW")
print(f"增量: {wind_gen - base_gen:.2f} MW (应约为100 MW)")
```

## 注意事项

1. **组件类型选择**: 风电模型必须使用 `WTG_PMSG_01` 才能正确参与潮流计算
2. **关键参数**: 潮流计算需要正确设置 `Pctrl_mode`, `P_cmd`, `pf_P` 等参数
3. **固定分支名**: 使用固定的分支名，可被多次覆盖更新
4. **参数自动补全**: 所有新能源组件参数都通过元数据系统自动补全
5. **可扩展**: 可以基于此模板创建更多测试算例

## 更新模型

如果需要更新测试模型（例如修改参数或位置），直接重新运行创建命令即可：

```bash
# 更新风电模型
python examples/metadata/create_test_models.py --wind

# 更新所有模型
python examples/metadata/create_test_models.py --all
```

模型将被重新创建并覆盖原有分支。

## 故障排除

### 模型创建失败
- 检查 `.cloudpss_token` 文件是否存在且有效
- 检查网络连接
- 查看错误日志

### 潮流计算不显示新能源发电
- 确认使用的是 `WTG_PMSG_01` 而非 `WGSource`
- 检查参数中是否包含 `Pctrl_mode`, `P_cmd`, `pf_P`
- 验证电气引脚是否正确连接

### 模型验证失败
- 检查元数据文件是否完整
- 检查CloudPSS平台状态
- 查看详细错误信息

### 已退役算例
- `model/holdme/test_IEEE39_with_Wind_WGSource`
- `model/holdme/test_wind_with_pins`

这两条历史算例不再作为主线测试资产使用。

## 相关文档

- [WTG_PMSG 元数据](wtg_pmsg.json) - PMSG风机完整元数据定义
- [元数据系统文档](../docs/metadata/README.md)
- [模型构建工作流](../docs/guides/model-building-workflow.md)
- [潮流研究工作流](../docs/guides/powerflow-study-workflow.md)
