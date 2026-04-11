# 暂态稳定裕度评估技能 (transient_stability_margin)

## 设计背景

### 研究对象
暂态稳定裕度是衡量电力系统在遭受大扰动（如短路、线路故障）后能否恢复稳定运行的关键指标。临界清除时间(CCT)是暂态稳定分析的核心参数，表示系统在失去稳定之前能够承受的最长故障持续时间。

### 实际需求
1. **运行极限确定**：评估系统在当前运行方式下的稳定储备
2. **保护整定依据**：基于CCT确定最优保护切除时间
3. **风险评估**：量化系统的暂态稳定裕度，识别薄弱环节
4. **规划决策支持**：指导新建线路、发电机组的规划

### 期望的输入和输出

**输入**:
- 电力系统模型（含EMT仿真方案）
- 故障场景（位置、类型、切除时间）
- 需要监控的发电机列表
- 分析参数（二分法容差、最大迭代次数等）

**输出**:
- 各故障场景的临界清除时间(CCT)
- 稳定裕度百分比
- 最薄弱环节识别
- 系统总体评估结论

### 计算结果的用途和价值
- 为保护装置整定提供依据
- 评估系统抗扰动能力
- 指导运行方式安排
- 识别需要加固的薄弱环节

## 功能特性

- **CCT精确计算**：二分法搜索，收敛精度可配置
- **稳定裕度评估**：基于CCT与基准切除时间计算裕度百分比
- **多场景批量分析**：支持N-1场景下的裕度评估
- **电压波形分析**：基于真实EMT波形判断稳定性
- **自动电压量测**：无需手动配置电压通道
- **边界自适应**：自动扩展搜索上界

## 快速开始

### 3.1 CLI方式（推荐）

```bash
python -m cloudpss_skills run --config margin_config.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills.builtin.transient_stability_margin import TransientStabilityMarginSkill

skill = TransientStabilityMarginSkill()
config = skill.get_default_config()
config["model"]["rid"] = "model/holdme/IEEE39"
config["fault_scenarios"] = [
    {"location": "BUS_10", "type": "three_phase", "duration": 0.1}
]
config["generators"] = ["GEN_1", "GEN_2"]
config["analysis"]["compute_cct"] = True
config["analysis"]["compute_margin"] = True

result = skill.run(config)
print(f"CCT: {result.data['scenarios'][0]['cct']}")
```

### 3.3 YAML配置示例

```yaml
skill: transient_stability_margin
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
  source: cloud
fault_scenarios:
  - location: BUS_10
    type: three_phase
    duration: 0.1
generators:
  - GEN_1
  - GEN_2
analysis:
  compute_cct: true
  compute_margin: true
  margin_baseline: 0.5
  cct_tolerance: 0.001
  max_iterations: 20
  emt_timeout: 300
output:
  format: json
  path: ./results/
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: transient_stability_margin
auth:
  token: <string>
  token_file: .cloudpss_token
model:
  rid: <string>
  source: cloud | local
fault_scenarios:
  - location: <string>
    type: three_phase | single_phase | line_ground
    duration: <number>  # 切除时间(s)
generators:
  - <string>  # 发电机标签列表
analysis:
  compute_cct: true
  compute_margin: true
  margin_baseline: 0.5
  cct_initial_upper_bound: 1.0
  cct_search_upper_bound: 5.0
  cct_bound_expansion_factor: 2.0
  cct_tolerance: 0.001
  max_iterations: 20
  emt_timeout: 300.0
  stability_trace_name: "vac:0"
  postfault_min_ratio: 0.9
  late_recovery_min_ratio: 0.95
  prefault_window_offset: [-0.08, -0.06]
  postfault_window_offset: [0.22, 0.24]
  late_recovery_window_offset: [0.46, 0.48]
output:
  format: json | console
  path: <string>
```

### 4.2 参数说明

| 参数路径 | 类型 | 必填 | 默认值 | 说明 |
|---------|------|------|--------|------|
| skill | string | 是 | - | 固定值 |
| fault_scenarios[].location | string | 是 | - | 故障位置母线 |
| fault_scenarios[].type | enum | 否 | three_phase | 故障类型 |
| fault_scenarios[].duration | number | 否 | 0.1 | 基准切除时间 |
| analysis.margin_baseline | number | 否 | 0.5 | 裕度计算基准时间 |
| analysis.cct_tolerance | number | 否 | 0.001 | CCT收敛容差(s) |
| analysis.max_iterations | integer | 否 | 20 | 最大迭代次数 |
| analysis.emt_timeout | number | 否 | 300 | EMT仿真超时(s) |
| analysis.postfault_min_ratio | number | 否 | 0.9 | 故障后电压恢复阈值 |
| analysis.late_recovery_min_ratio | number | 否 | 0.95 | 晚恢复电压阈值 |

## Agent使用指南

### 5.1 基本调用模式

```python
from cloudpss_skills import SkillStatus

skill = TransientStabilityMarginSkill()
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "fault_scenarios": [
        {"location": "BUS_10", "type": "three_phase", "duration": 0.1}
    ],
    "analysis": {"compute_cct": True, "compute_margin": True}
}
result = skill.run(config)
```

### 5.2 处理结果

```python
if result.status == SkillStatus.SUCCESS:
    scenarios = result.data["scenarios"]
    for s in scenarios:
        cct = s["cct"]["cct_seconds"]
        margin = s["margin"]["margin_percent"]
        print(f"故障位置: {s['fault_location']}")
        print(f"CCT: {cct}s, 裕度: {margin}%")
    
    summary = result.data["summary"]
    print(f"最薄弱点: {summary.get('weakest_point')}")
elif result.status == SkillStatus.FAILED:
    print(f"分析失败: {result.error}")
```

### 5.3 错误处理

```python
try:
    result = skill.run(config)
except TimeoutError as e:
    print(f"仿真超时: {e}")
    print("建议: 增大 analysis.emt_timeout 或减少迭代次数")
except KeyError as e:
    print(f"配置错误: 缺少必要参数 {e}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "model_rid": "model/holdme/IEEE39",
  "timestamp": "2026-04-10T15:30:00",
  "scenarios": [
    {
      "fault_location": "BUS_10",
      "fault_type": "three_phase",
      "base_duration": 0.1,
      "cct": {
        "cct_seconds": 0.385,
        "cct_relation": "=",
        "iterations": 10,
        "tolerance": 0.001,
        "method": "bisection",
        "bounded": true,
        "verified": false
      },
      "margin": {
        "cct": 0.385,
        "baseline": 0.5,
        "margin_seconds": -0.115,
        "margin_percent": -29.87,
        "stability_status": "不稳定"
      }
    }
  ],
  "summary": {
    "total_scenarios": 1,
    "cct_statistics": {"min": 0.385, "max": 0.385, "avg": 0.385},
    "margin_statistics": {"min": -29.87, "max": -29.87, "avg": -29.87},
    "weakest_point": {"location": "BUS_10", "margin_percent": -29.87},
    "overall_assessment": "存在不稳定场景，需要改进",
    "verified": false
  }
}
```

### 6.2 稳定性判据说明

| 指标 | 稳定阈值 | 说明 |
|------|---------|------|
| postfault_min_ratio | ≥0.9 | 故障后0.22-0.24s窗口电压/故障前电压 |
| late_recovery_min_ratio | ≥0.95 | 故障后0.46-0.48s窗口电压/故障前电压 |

两者同时满足才判定为稳定。

## 与其他技能的关联

```
                    ┌────────────────────────┐
                    │transient_stability_margin│
                    └───────────┬────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
 ┌────────────┐          ┌────────────┐          ┌────────────┐
 │   emt_     │          │   emt_     │          │  fault_    │
 │simulation  │          │fault_study │          │clearing_scan│
 └────────────┘          └────────────┘          └────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │  transient_stability   │
                    └───────────────────────┘
```

- **emt_simulation**：提供EMT仿真基础能力
- **emt_fault_study**：故障分析基础
- **fault_clearing_scan**：故障清除扫描
- **transient_stability**：完整暂态稳定分析

## 性能特点

- **搜索效率高**：二分法收敛速度快（通常10-15次迭代）
- **多次EMT仿真**：每个场景需要多次EMT仿真（搜索+验证）
- **计算时间长**：完整CCT分析可能需要数分钟
- **资源占用高**：需要运行CloudPSS仿真服务

## 常见问题

**Q1: 为什么需要多次EMT仿真？**
A1: 二分法需要在每次迭代中运行EMT仿真来验证稳定性，直到收敛到指定容差。

**Q2: 如何加速CCT计算？**
A2: 1) 增大cct_tolerance（如0.005）；2) 减少max_iterations；3) 设置更小的cct_search_upper_bound。

**Q3: verified=false是什么意思？**
A3: 当前CCT基于电压恢复判据而非正式功角/转速判据，结果仅供初步评估参考。

**Q4: 为什么返回FAILED状态？**
A4: 当verified=false时技能返回FAILED，因为结果不能作为正式暂态稳定裕度结论。

**Q5: 如何识别最薄弱的故障位置？**
A5: 查看summary.weakest_point字段，margin_percent最低的场景即为最薄弱点。

## 完整示例

### 场景描述
评估IEEE39系统在Bus10发生三相短路时的暂态稳定裕度，确定系统能否承受0.5s的切除时间。

### 配置文件
```yaml
skill: transient_stability_margin
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
  source: cloud
fault_scenarios:
  - location: BUS_10
    type: three_phase
    duration: 0.5
analysis:
  compute_cct: true
  compute_margin: true
  margin_baseline: 0.5
  cct_tolerance: 0.001
  max_iterations: 15
  emt_timeout: 180
output:
  format: json
  path: ./results/
```

### 执行命令
```bash
python -m cloudpss_skills run --config margin_config.yaml
```

### 预期输出
```
[INFO] 开始暂态稳定裕度评估: model/holdme/IEEE39
[INFO] 故障场景数: 1
[INFO] 
[INFO] 分析场景 1/1: BUS_10
[INFO]   计算CCT...
[INFO]     二分法搜索CCT...
[INFO]   计算稳定裕度...
[INFO] 暂态稳定裕度评估完成
```

### 结果解读
- 若margin_percent > 0：当前切除时间下系统稳定
- 若margin_percent < 0：系统不稳定，需要调整保护整定
- 若margin_percent > 30：稳定裕度充足

## 版本信息

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0.0 | 2026-04-01 | 初始版本，支持CCT计算和裕度评估 |

## 相关文档

- [emt_simulation.md](./emt_simulation.md) - EMT仿真基础
- [emt_fault_study.md](./emt_fault_study.md) - EMT故障分析
- [transient_stability.md](./transient_stability.md) - 暂态稳定分析
- [fault_clearing_scan.md](./fault_clearing_scan.md) - 故障清除扫描
