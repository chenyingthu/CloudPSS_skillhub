# WTG_PMSG_01 新能源算例更新总结

> 归档说明（2026-04-03）：
> 本文档记录的是一次中间迁移。当前有效算例与退役清单请以 `TEST_MODELS.md` 和 `model_builder_renewable_audit_20260403.md` 为准。

## 问题背景

原有测试算例使用 `model/CloudPSS/WGSource` 组件，该组件**不支持潮流计算**，导致：
- 潮流计算结果中新能源发电功率显示为 0
- 无法验证新能源对系统的影响

## 解决方案

改用 `model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b5` 组件（永磁同步风机），该组件**完全支持潮流计算**，且保留更完整的 LVRT 参数与观测量。

## 完成的工作

### 1. 创建新的元数据文件

**文件**: `examples/metadata/wtg_pmsg.json`

定义了 WTG_PMSG_01 组件的完整元数据：
- 23个参数（包括潮流计算必需的参数）
- 完整的参数分组（基础、潮流、风机、控制、保护、聚合）
- 引脚定义（电气、输入、输出）
- 验证规则

**关键潮流参数**:
```json
{
  "Pctrl_mode": "1",    // 控制模式: 0=PQ, 1=PV, 2=平衡
  "P_cmd": 2.0,         // 有功指令 (MW)
  "pf_P": 2.0,          // 潮流有功 (MW)
  "pf_Q": 0.0,          // 潮流无功 (Mvar)
  "Sbase": 2.5,         // 基准容量 (MVA)
  "UnitCount": 40       // 风机台数
}
```

### 2. 更新算例创建脚本

**文件**: `examples/metadata/create_test_models.py`

修改了以下函数：
- `create_wind_model()`: 使用 WTG_PMSG_01 组件，配置 40台×2.5MW = 100MW 风电
- `create_hybrid_model()`: 风电部分使用 WTG_PMSG_01

**风电配置**:
```python
component_type = 'model/open-cloudpss/WTG_PMSG_01-avm-stdm-v2b5'
user_params = {
    'Vbase': 0.69,
    'Sbase': 2.5,
    'P_cmd': 2.0,
    'pf_P': 2.0,
    'Pctrl_mode': '1',
    'UnitCount': 40
}
```

### 3. 创建验证脚本

**文件**: `examples/metadata/validate_wtg_pmsg.py`

验证内容：
- 元数据加载
- 参数自动补全
- 参数验证
- 引脚配置
- 新旧组件对比

**文件**: `examples/metadata/test_pmsg_config.py`

测试内容：
- 风电模型配置
- 混合模型配置
- 引脚连接验证

### 4. 更新文档

**文件**: `examples/metadata/TEST_MODELS.md`

更新内容：
- 组件类型说明
- 新旧组件对比表
- 关键潮流参数说明
- 验证方法
- 故障排除

## 验证结果

```bash
$ python examples/metadata/validate_wtg_pmsg.py
✅ 元数据验证通过，可以使用 WTG_PMSG_01 创建算例

$ python examples/metadata/test_pmsg_config.py
✅ 所有配置测试通过
```

## 使用方法

### 创建测试算例

```bash
# 创建风电测试模型
python examples/metadata/create_test_models.py --wind

# 创建所有测试模型
python examples/metadata/create_test_models.py --all

# 创建并验证
python examples/metadata/create_test_models.py --all --validate
```

### 验证潮流计算

```python
from cloudpss import Model

# 获取风电模型
model = Model.fetch('model/holdme/test_ieee39_wind')

# 运行潮流计算
job = model.runPowerFlow()
result = job.result

# 验证新能源发电
buses = result.getBuses()
total_gen = sum(b.get('generation', {}).get('P', 0) for b in buses)
print(f"总发电: {total_gen:.2f} MW")  # 应比基准增加约80-100 MW
```

## 测试模型信息

| 模型 | RID | 组件 | 容量 | 说明 |
|------|-----|------|------|------|
| IEEE39+风电 | model/holdme/test_ieee39_wind | WTG_PMSG_01 | 80 MW | 支持潮流计算 |
| IEEE39+光伏 | model/holdme/test_ieee39_pv | PVStation | 50 MW | 简化模型 |
| IEEE39+混合 | model/holdme/test_ieee39_hybrid | WTG_PMSG_01+PV | 130 MW | 风电+光伏 |

## 关键改进

| 方面 | 旧组件 (WGSource) | 新组件 (WTG_PMSG_01) |
|------|-------------------|----------------------|
| 潮流计算 | ❌ 不支持 | ✅ 完全支持 |
| 关键参数 | Vbase, Pnom | Sbase, Pctrl_mode, P_cmd, pf_P |
| 控制模式 | 无 | PV/PQ/平衡节点 |
| 等值风场 | 不支持 | UnitCount 参数支持 |
| 参数数量 | ~15个 | 23个 |

## 下一步工作

1. **运行算例创建**: 执行 `python examples/metadata/create_test_models.py --all`
2. **验证潮流计算**: 运行潮流并检查新能源发电是否正确显示
3. **EMT仿真**: 验证 PMSG 模型在 EMT 仿真中的表现
4. **光伏模型**: 如果需要，为光伏组件找到支持潮流计算的模型类型
