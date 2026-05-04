# CloudPSS SkillHub 开发快速参考

## 常用场景速查

### 场景1: 开发新技能

```bash
# 1. 创建提案
/opsx:propose add-skill-[skill-name]

# 2. 使用模板
# 复制 .openspec/templates/new-skill-spec.md 到 .openspec/specs/

# 3. 头脑风暴
/sc:brainstorm

# 4. 生成计划
/sc:workflow

# 5. 实现
/sc:implement

# 6. 审查
/plan-eng-review
/review

# 7. 测试
pytest tests/test_[skill_name]_*.py -v

# 8. 部署
/ship

# 9. 复盘
/retro
```

### 场景2: 修复 Bug

```bash
# 简单 Bug (< 3 个文件)
直接修复 + 添加测试

# 复杂 Bug (≥ 3 个文件)
/opsx:propose fix-[bug-description]
/sc:brainstorm
/sc:implement
/review
/ship
```

### 场景3: 代码重构

```bash
/opsx:propose refactor-[target]
/sc:brainstorm
/sc:workflow
/sc:implement
/plan-eng-review
/review
pytest  # 确保所有测试通过
/ship
/retro
```

## 命令速查表

| 命令 | 用途 | 使用频率 |
|------|------|----------|
| `/opsx:propose` | 创建提案 | 每个新功能 |
| `/sc:brainstorm` | 需求探索 | 复杂功能 |
| `/sc:workflow` | 生成计划 | 复杂功能 |
| `/sc:implement` | 实现功能 | 经常 |
| `/sc:test` | 运行测试 | 经常 |
| `/plan-eng-review` | 工程审查 | 重要功能 |
| `/review` | 代码审查 | 每次提交 |
| `/ship` | 部署 | 完成功能 |
| `/retro` | 复盘 | 里程碑 |

## 质量检查清单

### 代码提交前
- [ ] 代码自测通过
- [ ] 单元测试通过
- [ ] ruff 检查通过
- [ ] pyright 类型检查通过

### 代码审查前
- [ ] 所有测试通过
- [ ] 覆盖率 ≥ 80%
- [ ] 文档已更新
- [ ] 配置示例已更新

### 部署前
- [ ] 代码审查通过
- [ ] CI 检查通过
- [ ] 变更日志已更新
