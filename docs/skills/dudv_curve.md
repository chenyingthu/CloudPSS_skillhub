# DUDV曲线可视化技能

基于EMT仿真结果生成DUDV（电压偏差-电压）曲线，用于电压稳定性分析。

## 功能特性

- **DUDV曲线生成**: 通过无功注入扫描生成电压-偏差关系曲线
- **多母线对比**: 支持多母线同时分析和对比显示
- **从扰动结果加载**: 可直接从disturbance_severity结果生成曲线
- **多格式输出**: 支持PNG、PDF、SVG格式
- **电压稳定边界识别**: 辅助识别电压稳定极限

## 适用场景

- 电压稳定性分析
- 无功补偿效果评估
- N-1故障后电压恢复特性分析
- VSI弱母线验证

## 快速开始

### 1. 基本使用

```python
from cloudpss_skills import get_skill

skill = get_skill("dudv_curve")

config = {
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "buses": ["Bus_16", "Bus_15", "Bus_26"],
    "simulation": {
        "end_time": 15.0,
        "step_time": 0.0001,
        "fault_bus": "Bus_16",
        "fault_type": "three_phase",
        "fault_time": 4.0,
        "fault_duration": 0.1
    },
    "dudv": {
        "voltage_range": [0.8, 1.2],
        "num_points": 20,
        "injection_duration": 2.0
    },
    "output": {
        "format": "png",
        "path": "./results/",
        "prefix": "dudv_curve"
    }
}

result = skill.run(config)
```

### 2. 使用配置文件

```bash
python -m cloudpss_skills run --config config/dudv_curve.yaml
```

### 3. 运行示例

```bash
python examples/analysis/dudv_curve_example.py
```

## 工作流程

```
1. 配置加载
   └── 读取母线列表和扫描参数

2. 模型获取
   └── 从CloudPSS获取模型

3. 电压扫描
   └── 对每个目标母线
       └── 在不同无功注入水平下运行EMT
       └── 记录电压响应

4. DUDV数据计算
   └── 计算每个电压点的DV偏差
   └── 构建电压-偏差数据序列

5. 曲线绘制
   └── 生成DUDV曲线图
   └── 添加参考线（V=1.0, DV=0）

6. 结果输出
   └── 保存曲线图（PNG/PDF/SVG）
   └── 保存DUDV数据（JSON）
```

## DUDV曲线解读

### 曲线含义

- **横轴**: 电压 (pu)，标幺值电压
- **纵轴**: 电压偏差 ΔV (pu)，相对于稳态电压的变化
- **曲线形状**: 反映母线电压对无功注入的敏感度

### 稳定性判断

```
曲线斜率:
├── 平缓 (斜率小): 电压稳定性好
├── 陡峭 (斜率大): 电压稳定性差
└── 负斜率区域: 可能存在电压崩溃风险

曲线位置:
├── 整体偏左: 电压偏低，可能需要无功补偿
└── 整体偏右: 电压偏高，可能需要减少无功
```

## 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model.rid` | string | - | 模型RID（必需） |
| `buses` | array | - | 分析母线列表（必需） |
| `simulation.end_time` | float | 15.0 | 仿真结束时间 |
| `simulation.fault_bus` | string | - | 故障母线 |
| `simulation.fault_type` | enum | three_phase | 故障类型 |
| `dudv.voltage_range` | array | [0.8, 1.2] | 电压扫描范围 |
| `dudv.num_points` | int | 20 | 扫描点数 |
| `output.format` | enum | png | 输出格式 |
| `output.show_grid` | bool | True | 显示网格 |

## 辅助方法

### from_disturbance_severity_result

从扰动严重度分析结果加载DUDV数据。

```python
dudv_data = skill.from_disturbance_severity_result(
    result_file="./results/disturbance_severity_result.json",
    bus_labels=["Bus_16", "Bus_15"]
)
```

返回:
```python
{
    "Bus_16": {
        "voltage": [0.82, 1.02, 1.22],
        "dv": [-0.08, 0.0, 0.05]
    },
    ...
}
```

## 输出文件

### 曲线图 (`*_curve.{png|pdf|svg}`)

- 每个母线一个子图
- 自动布局（1行、2×2、多行等）
- 包含参考线（V=1.0, DV=0）
- 可选网格和图例

### DUDV数据 (`*_data.json`)

```json
{
  "Bus_16": {
    "voltage": [0.8, 0.85, 0.9, ..., 1.2],
    "dv": [-0.15, -0.1, -0.05, ..., 0.1]
  },
  "Bus_15": {
    "voltage": [...],
    "dv": [...]
  }
}
```

## 与已有技能的关联

```
disturbance_severity
    ↓ (DV数据)
dudv_curve
    ↓ (可视化)
DUDV曲线图

vsi_weak_bus
    ↓ (弱母线识别)
dudv_curve
    ↓ (验证分析)
电压稳定性验证报告
```

## 使用建议

### 1. 选择合适的扫描范围

```yaml
# 对于正常系统
dudv:
  voltage_range: [0.9, 1.1]
  num_points: 15

# 对于电压薄弱系统
dudv:
  voltage_range: [0.7, 1.3]
  num_points: 30
```

### 2. 结合VSI结果分析

```python
# 先运行VSI分析
vsi_result = vsi_skill.run(config_vsi)
weak_buses = [b["label"] for b in vsi_result.data["weak_buses"]]

# 再对弱母线进行DUDV分析
dudv_config["buses"] = weak_buses
dudv_result = dudv_skill.run(dudv_config)
```

### 3. 批量生成对比图

```python
# 补偿前
dudv_before = skill.run(config_before)

# 补偿后
dudv_after = skill.run(config_after)

# 对比分析
```

## 故障排查

### 问题1: 曲线数据点过少

**原因**: num_points设置过小
**解决**: 增加扫描点数到20-50

### 问题2: 电压范围不合适

**原因**: voltage_range与实际电压范围不匹配
**解决**: 根据系统标称电压调整范围

### 问题3: 仿真不收敛

**原因**: 极端电压条件下的仿真发散
**解决**: 缩小电压扫描范围

### 问题4: 图表显示不全

**原因**: 母线数量过多
**解决**: 减少单次分析的母线数量

## 性能注意事项

- **仿真时间**: 每个数据点需要一次EMT仿真
- **总时间**: num_points × 单仿真时间
- **建议**: 先用较少点数测试，再增加精度

## 参考实现

基于 [PSA Skills](https://git.tsinghua.edu.cn/yuanxuefeng/psa-skills-0.2.3) 的DUDV可视化功能实现。

## 版本历史

- **v1.0**: 基础DUDV曲线可视化功能
  - 电压扫描和DV计算
  - 多母线对比显示
  - 从扰动结果加载数据
