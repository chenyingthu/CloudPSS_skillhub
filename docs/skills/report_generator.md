# 智能报告生成器技能 (report_generator)

## 设计背景

### 研究对象
电力系统分析通常需要运行多个技能（如潮流、N-1安全、暂态稳定等），每个技能产生独立的结果。报告生成器将这些分散的结果整合成一份完整的分析报告，便于存档、分享和决策参考。

### 实际需求
1. **结果整合**：将多个技能的分析结果整合到单一报告中
2. **格式多样**：支持Markdown、DOCX、HTML等多种输出格式
3. **模板化**：支持综合报告、摘要报告、自定义报告等多种模板
4. **自动化**：可与工作流集成，自动生成定期分析报告

### 期望的输入和输出

**输入**:
- 技能名称列表（需要调用的技能）
- 技能结果数据（已执行技能的输出）
- 报告模板配置
- 输出格式配置

**输出**:
- 完整分析报告文件（Markdown/DOCX/HTML）
- 章节结构信息

### 计算结果的用途和价值
- 为决策者提供统一的分析结论
- 满足存档和审计要求
- 便于结果分享和讨论

## 功能特性

- **多技能结果整合**：支持整合任意数量技能的分析结果
- **多种输出格式**：Markdown（默认）、DOCX、HTML
- **模板化报告生成**：comprehensive、summary、custom三种模板
- **自定义章节配置**：可按需配置报告章节
- **图表自动插入**：支持在报告中嵌入图表引用
- **结构化数据输出**：提供章节结构信息便于后续处理

## 快速开始

### 3.1 CLI方式（推荐）

```bash
python -m cloudpss_skills run --config report_config.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills.builtin.report_generator import ReportGeneratorSkill

skill = ReportGeneratorSkill()
config = {
    "report": {
        "title": "电力系统分析报告",
        "skills": ["power_flow", "n1_security"],
        "skill_results": {
            "power_flow": {"status": "success", "data": {...}},
            "n1_security": {"status": "success", "data": {...}}
        }
    },
    "output": {"format": "markdown", "path": "./reports/"}
}
result = skill.run(config)
print(f"报告: {result.data['output_file']}")
```

### 3.3 YAML配置示例

```yaml
skill: report_generator
report:
  title: "IEEE39系统2026年安全分析报告"
  skills:
    - power_flow
    - n1_security
    - transient_stability
  skill_results:
    power_flow:
      status: success
      summary: "潮流计算收敛，所有节点电压正常"
      data: {...}
    n1_security:
      status: success
      summary: "N-1校验通过"
      data: {...}
  template:
    type: comprehensive
    sections:
      - executive_summary
      - system_overview
      - analysis_results
      - conclusions
output:
  format: docx
  path: ./reports/
  filename: security_report_2026.docx
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: report_generator
report:
  title: <string>                    # 报告标题
  skills:                             # 需要整合的技能名称列表
    - <string>
  skill_results:                      # 技能结果数据
    <skill_name>:
      status: success | failed
      summary: <string>
      data: {...}
  template:
    type: comprehensive | summary | custom
    sections:
      - executive_summary
      - system_overview
      - analysis_results
      - conclusions
output:
  format: markdown | docx | html | pdf
  path: <string>
  filename: <string>
```

### 4.2 参数说明

| 参数路径 | 类型 | 必填 | 默认值 | 说明 |
|---------|------|------|--------|------|
| skill | string | 是 | - | 固定值 `report_generator` |
| report.title | string | 否 | "电力系统分析报告" | 报告标题 |
| report.skills | array | 是* | - | 技能名称列表（*与skill_results二选一） |
| report.skill_results | object | 是* | - | 技能结果数据 |
| report.template.type | enum | 否 | comprehensive | 报告模板类型 |
| report.template.sections | array | 否 | - | 自定义章节列表 |
| output.format | enum | 否 | markdown | 输出格式 |
| output.path | string | 否 | ./reports/ | 输出目录 |
| output.filename | string | 否 | - | 输出文件名 |

## Agent使用指南

### 5.1 基本调用模式

```python
skill = ReportGeneratorSkill()
config = {
    "report": {
        "title": "月度分析报告",
        "skill_results": {
            "power_flow": pf_result.data,
            "n1_security": n1_result.data
        }
    },
    "output": {"format": "docx"}
}
result = skill.run(config)
```

### 5.2 处理结果

```python
if result.status == SkillStatus.SUCCESS:
    print(f"报告标题: {result.data['report_title']}")
    print(f"章节数: {result.data['sections_count']}")
    print(f"输出文件: {result.data['output_file']}")
    
    # 读取章节结构
    for section in result.data['sections']:
        print(f"  - {section['title']} (级别: {section['level']})")
    
    # 读取输出文件
    with open(result.data['output_file'], 'r') as f:
        content = f.read()
```

### 5.3 错误处理

```python
try:
    result = skill.run(config)
    if result.status == SkillStatus.FAILED:
        print(f"报告生成失败: {result.error}")
except ValidationError as e:
    print(f"配置验证失败: {e}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "report_title": "IEEE39系统安全分析报告",
  "sections_count": 6,
  "skills_included": ["power_flow", "n1_security", "transient_stability"],
  "output_format": "markdown",
  "output_file": "./reports/report_20260410_153000.md",
  "sections": [
    {"title": "封面", "level": 0},
    {"title": "目录", "level": 0},
    {"title": "执行摘要", "level": 1},
    {"title": "系统概述", "level": 1},
    {"title": "power_flow分析", "level": 1},
    {"title": "n1_security分析", "level": 1},
    {"title": "transient_stability分析", "level": 1},
    {"title": "结论与建议", "level": 1}
  ]
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| skill_name | string | 技能名称 |
| status | SkillStatus | 执行状态 |
| data.report_title | string | 报告标题 |
| data.sections_count | integer | 章节数量 |
| data.skills_included | array | 包含的技能列表 |
| data.output_format | string | 输出格式 |
| data.output_file | string | 输出文件路径 |
| data.sections | array | 章节结构列表 |
| artifacts | list | 输出文件工件 |
| error | string | 错误信息（失败时） |

## 与其他技能的关联

```
                    ┌────────────────────┐
                    │  report_generator   │
                    └─────────┬──────────┘
                              │
      ┌──────────────────────┼──────────────────────┐
      │                      │                      │
      ▼                      ▼                      ▼
┌──────────┐         ┌──────────┐          ┌──────────┐
│power_flow│         │n1_security│          │transient│
│          │         │          │          │_stability│
└──────────┘         └──────────┘          └──────────┘
```

报告生成器不执行具体分析，而是整合其他技能的输出结果。

## 性能特点

- **无需仿真**：纯数据处理，执行速度快
- **内存占用低**：不涉及大规模计算
- **格式转换快**：Markdown即时生成，DOCX需要python-docx库
- **可批量处理**：支持一次生成多份报告

## 常见问题

**Q1: 如何生成DOCX格式报告？**
A1: 安装python-docx库（`pip install python-docx`），配置`output.format: docx`。

**Q2: skill_results是什么格式？**
A2: 应传入各技能`SkillResult.data`的完整内容，包含status、summary、data等字段。

**Q3: 可以不提供skill_results吗？**
A3: 可以，但报告将显示"结果未提供"。建议传入真实结果以生成完整报告。

**Q4: 报告包含哪些章节？**
A4: 综合报告包含封面、目录、执行摘要、系统概述、各技能分析结果、结论与建议。

**Q5: 如何自定义章节顺序？**
A5: 在`report.template.sections`中指定章节顺序。

## 完整示例

### 场景描述
完成潮流计算和N-1安全分析后，生成综合分析报告。

### 配置文件
```yaml
skill: report_generator
report:
  title: "IEEE39系统安全评估报告"
  skills:
    - power_flow
    - n1_security
  skill_results:
    power_flow:
      status: success
      summary: "潮流计算收敛，所有节点电压在0.95-1.05pu范围内"
      data:
        converged: true
        max_voltage: 1.05
        min_voltage: 0.97
    n1_security:
      status: success
      summary: "N-1安全校验通过，所有支路断开后系统保持稳定"
      data:
        passed: true
        checked_branches: 64
        violations: 0
output:
  format: markdown
  path: ./reports/
  filename: security_report.md
```

### 执行命令
```bash
python -m cloudpss_skills run --config report_config.yaml
```

### 预期输出
```
[INFO] 开始生成报告: IEEE39系统安全评估报告
[INFO] 整合2个技能结果
[INFO] 报告生成完成: ./reports/security_report.md
```

### 结果文件
生成Markdown格式报告，包含：
- 封面信息
- 执行摘要
- 各技能分析详情
- 结论与建议

## 版本信息

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0.0 | 2026-03-30 | 初始版本 |

## 相关文档

- [power_flow.md](./power_flow.md) - 潮流计算
- [n1_security.md](./n1_security.md) - N-1安全分析
- [transient_stability.md](./transient_stability.md) - 暂态稳定分析
