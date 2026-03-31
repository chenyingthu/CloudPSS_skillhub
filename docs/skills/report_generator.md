# 智能报告生成器技能 (report_generator)

## 功能概述

自动整合多个技能的分析结果，生成专业的分析报告。支持Markdown、DOCX、HTML格式输出。

## 配置说明

```yaml
skill: report_generator
report:
  title: "电力系统分析报告"
  skills:
    - power_flow
    - n1_security
  skill_results:
    power_flow:
      status: success
      data: {...}
  template:
    type: comprehensive

output:
  format: docx
  path: ./reports/
```

## 输出结果

- 完整分析报告文档
- 包含执行摘要、详细分析、结论建议

## 使用示例

```python
from cloudpss_skills.builtin.report_generator import ReportGeneratorSkill

skill = ReportGeneratorSkill()
result = skill.run(config)

print(f"报告生成: {result.data['output_file']}")
```
