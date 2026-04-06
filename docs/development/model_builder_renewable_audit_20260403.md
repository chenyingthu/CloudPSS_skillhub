# model_builder 新能源坏分支审计与重建记录

日期: 2026-04-03

## 结论

个人目录下旧的 IEEE39+新能源模型里，主要失败模式有三类：

1. 新能源元件被加入了模型，但 `pins` 为空，实际没有接入系统。
2. 新能源元件的引脚接成了 `Bus10` / `Bus14` 这类展示名，而不是 CloudPSS 实际可连接的 `bus10` / `bus14`。
3. 组件本身不适合当前潮流链路，或接入到特定母线后虽然 `runPowerFlow()` 返回完成，但结果表为空。

其中最典型的坏分支有：

- `model/holdme/test_IEEE39_with_PV_50MW`
- `model/holdme/test_IEEE39_with_PV_100MW`
- `model/holdme/test_IEEE39_with_PV_150MW`
- `model/holdme/test_IEEE39_with_Wind_50MW`
- `model/holdme/test_IEEE39_with_Wind_100MW`
- `model/holdme/test_IEEE39_with_Wind_WGSource`
- `model/holdme/test_ieee39_pv`
- `model/holdme/test_ieee39_wind`
- `model/holdme/test_ieee39_wind_csee`
- `model/holdme/test_ieee39_hybrid`

## 已确认失效的旧分支

| 旧分支 | 主要问题 | live 现象 |
|---|---|---|
| `model/holdme/test_IEEE39_with_PV_50MW` | `PVStation` 存在但 `pins: {}` | 潮流总发电增量 `0 MW` |
| `model/holdme/test_IEEE39_with_PV_100MW` | `PVStation` 存在但 `pins: {}` | 潮流总发电增量 `0 MW` |
| `model/holdme/test_IEEE39_with_PV_150MW` | `PVStation` 存在但 `pins: {}` | 潮流总发电增量 `0 MW` |
| `model/holdme/test_IEEE39_with_Wind_50MW` | `DFIG_WindFarm_Equivalent_Model` 存在但 `pins: {}` | 潮流总发电增量 `0 MW` |
| `model/holdme/test_IEEE39_with_Wind_100MW` | `DFIG_WindFarm_Equivalent_Model` 存在但 `pins: {}` | 潮流总发电增量 `0 MW` |
| `model/holdme/test_IEEE39_with_Wind_WGSource` | `WGSource` 存在但 `pins: {}` | 潮流总发电增量 `0 MW` |
| `model/holdme/test_ieee39_pv` | `PVStation` 接到 `Bus14` 而非 `bus14` | 潮流总发电增量 `0 MW` |
| `model/holdme/test_ieee39_wind` | `WTG_PMSG_01` 接到 `Bus10` 而非 `bus10` | 潮流总发电增量 `0 MW` |
| `model/holdme/test_ieee39_wind_csee` | `WTG_PMSG_01` 接到 `Bus10` 而非 `bus10` | 潮流总发电增量 `0 MW` |
| `model/holdme/test_ieee39_hybrid` | `WGSource/PVStation` 分别接到 `Bus10/Bus14` | 潮流总发电增量 `0 MW` |

## 重建结果

以下 `_fixed_20260403_104550` 分支为 2026-04-03 现场重建快照；同日多数原 branch 名也已被原位修复覆盖。

补充说明：
- 同日已将大部分可修复坏分支按原 branch key 原位覆盖修复，因此当前 CloudPSS 主线入口优先使用原 branch 名
- `_fixed_20260403_104550` 分支保留为这次清理动作的留痕快照

### 已重建并验证通过

| 旧分支 | 新分支 | 验证结果 |
|---|---|---|
| `model/holdme/test_IEEE39_with_PV_50MW` | `model/holdme/test_IEEE39_with_PV_50MW_fixed_20260403_104550` | `bus10` 接入点 `Pgen = 50 MW` |
| `model/holdme/test_IEEE39_with_PV_100MW` | `model/holdme/test_IEEE39_with_PV_100MW_fixed_20260403_104550` | `bus10` 接入点 `Pgen = 100 MW` |
| `model/holdme/test_IEEE39_with_PV_150MW` | `model/holdme/test_IEEE39_with_PV_150MW_fixed_20260403_104550` | `bus10` 接入点 `Pgen = 150 MW` |
| `model/holdme/test_IEEE39_with_Wind_50MW` | `model/holdme/test_IEEE39_with_Wind_50MW_fixed_20260403_104550` | `bus20` 接入点 `Pgen = 50 MW` |
| `model/holdme/test_IEEE39_with_Wind_100MW` | `model/holdme/test_IEEE39_with_Wind_100MW_fixed_20260403_104550` | `bus20` 接入点 `Pgen = 100 MW` |
| `model/holdme/test_ieee39_pv` | `model/holdme/test_ieee39_pv_fixed_20260403_104550` | `bus14` 接入点 `Pgen = 50 MW` |
| `model/holdme/test_ieee39_wind` | `model/holdme/test_ieee39_wind_fixed_20260403_104550` | `bus10` 接入点 `Pgen = 80 MW` |
| `model/holdme/test_ieee39_wind_csee` | `model/holdme/test_ieee39_wind_csee_fixed_20260403_104550` | `bus10` 接入点 `Pgen = 80 MW` |
| `model/holdme/test_ieee39_hybrid` | `model/holdme/test_ieee39_hybrid_fixed_20260403_104550` | `bus10` 接入点 `Pgen = 100 MW`，`bus14` 接入点 `Pgen = 50 MW` |

### 已重建但仍不建议使用

| 旧分支 | 尝试重建分支 | 当前状态 |
|---|---|---|
| `model/holdme/test_IEEE39_with_Wind_WGSource` | `model/holdme/test_IEEE39_with_Wind_WGSource_fixed_20260403_104550` | `runPowerFlow()` 返回完成，但 `getBuses()` / `getBranches()` 结果表为空，仍不应视为有效案例 |

## 额外说明

- 对 `WGSource`、`DFIG_WindFarm_Equivalent_Model`、`PVStation` 这类旧组件写法，`model_builder` 已经加入自动修复映射：
  - `WGSource` / `DFIG_WindFarm_Equivalent_Model` -> `model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b5`
  - `PVStation` / `PV_Inverter` -> `model/open-cloudpss/PVS_01-avm-stdm-v1b5`
- 对 `pin_connection.target_bus`，现在可自动把 `Bus10` / `Bus14` 映射到真实可连接的 `bus10` / `bus14`
- `WGSource_Bus30` 这条旧设计仍然不稳定。即便改成公开 PMSG 封装模型并修正为 `bus30`，当前 live 结果依然出现空结果表。该支路建议直接退役，不再作为正式测试算例沿用。

## 建议

后续技能验证优先使用以下新分支：

- `model/holdme/test_IEEE39_with_PV_50MW_fixed_20260403_104550`
- `model/holdme/test_IEEE39_with_PV_100MW_fixed_20260403_104550`
- `model/holdme/test_IEEE39_with_PV_150MW_fixed_20260403_104550`
- `model/holdme/test_IEEE39_with_Wind_50MW_fixed_20260403_104550`
- `model/holdme/test_IEEE39_with_Wind_100MW_fixed_20260403_104550`
- `model/holdme/test_ieee39_pv_fixed_20260403_104550`
- `model/holdme/test_ieee39_wind_fixed_20260403_104550`
- `model/holdme/test_ieee39_wind_csee_fixed_20260403_104550`
- `model/holdme/test_ieee39_hybrid_fixed_20260403_104550`
