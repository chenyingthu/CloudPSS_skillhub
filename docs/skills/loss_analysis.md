# 网损分析与优化技能 (loss_analysis)

## 功能概述

本技能用于分析电力系统的网损分布，包括支路损耗、变压器损耗计算，网损灵敏度分析，以及无功优化降损建议。

## 适用算例

- **推荐算例**: `model/holdme/IEEE39` (标准39节点系统)
- **适用场景**: 任意潮流可算的电力系统模型

## 配置说明

```yaml
skill: loss_analysis
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39

analysis:
  loss_calculation:
    enabled: true
    components: [lines, transformers]

  loss_sensitivity:
    enabled: true

  loss_optimization:
    enabled: true
    method: reactive_power_optimization

output:
  format: json
```

## 输出结果

```json
{
  "model": "model/holdme/IEEE39",
  "summary": {
    "total_loss_mw": 45.23,
    "branch_loss_mw": 38.12,
    "transformer_loss_mw": 7.11,
    "top_loss_branches": [...]
  },
  "branch_losses": [...],
  "transformer_losses": [...],
  "optimization_suggestions": {...}
}
```

## 使用示例

```python
from cloudpss_skills.builtin.loss_analysis import LossAnalysisSkill

skill = LossAnalysisSkill()
result = skill.run(config)

summary = result.data["summary"]
print(f"总网损: {summary['total_loss_mw']:.2f} MW")
```
