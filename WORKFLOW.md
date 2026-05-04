# CloudPSS SkillHub 开发工作流

> 基于 OpenSpec + Superpowers + gstack 的三件套最佳实践

---

## 核心理念

**各司其职、流水线作业**：
- **OpenSpec** — 想清楚再动手（需求先行）
- **Superpowers** — 拆清楚再执行（测试驱动 + 子代理驱动）
- **gstack** — 做清楚再交付（虚拟团队全流程审查）

---

## 工作流总览

```
想法 → /opsx:propose → /sc:brainstorm → /sc:workflow → /sc:implement
                              ↓                ↓              ↓
                       需求文档         执行计划       编码实现
                              ↓                ↓              ↓
                    ┌─────────┴────────┬─────────────────┴───────────┐
                    ↓                  ↓                             ↓
              /review → /qa → /ship  /retro  (gstack 虚拟团队流程)
              代码审查  测试   部署   复盘
```

---

## Phase 1: 想清楚 — OpenSpec

### 1.1 创建变更提案

```bash
# 提出一个功能变更（例如：新增一个仿真技能）
/opsx:propose add-new-skill
```

**OpenSpec 会生成：**

```
.openspec/
├── proposal.md          # 为什么要做这个功能
├── specs/
│   ├── spec-001.md      # 需求规格 1
│   └── spec-002.md      # 需求规格 2
├── design.md            # 技术方案
└── tasks.md             # 实施清单
```

### 1.2 提案模板

如果不使用 OpenSpec，按以下结构创建：

```markdown
# Proposal: [功能名称]

## Why
- 用户痛点描述
- 业务价值

## What Changes
- 功能清单
- 边界范围

## Acceptance Criteria
- [ ] 功能完成标准 1
- [ ] 功能完成标准 2
```

---

## Phase 2: 拆清楚 — Superpowers

### 2.1 头脑风暴

在正式编码前，使用 `/sc:brainstorm` 进行需求探索：

```bash
/sc:brainstorm
```

**提示词示例：**

```
基于以下规格，进行头脑风暴，发现潜在问题和边界情况：

[粘贴 proposal.md 和 specs/ 的内容]

请帮我：
1. 识别缺失的需求场景
2. 发现技术风险点
3. 提出实现方案建议
4. 列出验收检查清单
```

### 2.2 生成执行计划

```bash
/sc:workflow
```

**提示词示例：**

```
基于以下规格，生成详细的实施工作流：

## 规格文档
[粘贴 design.md 和 tasks.md 的内容]

## 要求
每个任务必须包含：
1. 具体文件路径
2. 完整代码实现
3. 明确的验收标准
4. 预计耗时
```

### 2.3 功能实现

```bash
/sc:implement
```

**提示词示例：**

```
请实现以下功能：
[粘贴工作流生成的任务计划]

要求：
1. 遵循项目代码规范
2. 编写单元测试
3. 更新相关文档
```

---

## Phase 3: 做清楚 — gstack

### 3.1 多级审查流程

#### CEO 视角审查

```bash
/plan-ceo-review
```

**目标：** 从战略角度审视需求对齐度

```
请审查以下实现：
1. 是否符合原始需求？
2. 用户体验是否达到标准？
3. 是否有更简单优雅的解决方案？
```

#### 工程经理审查

```bash
/plan-eng-review
```

**目标：** 技术架构和数据流审查

```
请审查以下实现：
1. 架构设计是否合理？
2. 数据流是否清晰？
3. 边界情况是否处理完整？
4. 测试覆盖是否充分？
```

### 3.2 代码审查

```bash
/review
```

**自动执行：**
- 静态代码分析
- 风格检查
- 潜在 Bug 检测
- 安全问题扫描

### 3.3 QA 测试

```bash
# 运行测试
pytest

# 使用 gstack QA（如有 Web UI）
/qa http://localhost:3000
```

### 3.4 部署上线

```bash
/ship
```

**自动执行：**
1. 运行测试套件
2. 创建 Pull Request
3. 等待 CI 通过
4. 合并到主分支

---

## Phase 4: 复盘归档

### 4.1 工程复盘

```bash
/retro
```

**回顾内容：**
- 哪些做得好？
- 哪些可以改进？
- 学到的经验教训
- 下次可以优化的地方

### 4.2 归档规格

```bash
/opsx:archive
```

规格会被归档到历史库，下次类似需求可以直接参考。

---

## 快速参考卡

### OpenSpec 命令

```bash
openspec init                    # 初始化项目
/opsx:propose <feature>          # 创建提案
/opsx:apply                      # 应用规格执行
/opsx:archive                    # 归档规格
```

### Superpowers 命令

```bash
/sc:brainstorm                   # 头脑风暴
/sc:workflow                     # 生成工作流
/sc:implement                    # 功能实现
/sc:analyze                      # 代码分析
/sc:design                       # 架构设计
/sc:test                         # 执行测试
/sc:review                       # 代码审查
```

### gstack 命令

```bash
/plan-ceo-review                 # CEO 审查
/plan-eng-review                 # 工程审查
/plan-design-review              # 设计审查
/review                          # 代码审查
/qa <url>                        # QA 测试
/ship                             # 部署上线
/retro                           # 复盘
```

---

## 最佳实践建议

### 工具选择原则

| 场景 | 推荐工具 | 原因 |
|------|----------|------|
| 需求模糊 | OpenSpec + /sc:brainstorm | 先对齐需求再动手 |
| 复杂功能 | Superpowers 全套 | 测试驱动 + 子代理 |
| 简单修改 | 直接使用 Claude | 避免过度流程 |
| 企业项目 | 三件套全套 | 全流程覆盖 |
| 个人项目 | OpenSpec + Superpowers | 轻量但规范 |

### 任务拆分原则

- **原子性**：每个任务只做一件事
- **独立性**：任务之间尽可能解耦
- **可验证**：每个任务有明确的验收标准
- **时效性**：单个任务控制在合理范围内

### 代码审查清单

使用 `/review` 前自检：

- [ ] 代码符合项目规范
- [ ] 测试覆盖率 > 80%
- [ ] 没有调试代码残留
- [ ] 错误处理完整
- [ ] 文档注释清晰

---

## 总结

这套三件套的核心价值：

1. **需求清晰** — OpenSpec 确保做对的事情
2. **执行可控** — Superpowers 确保事情做对
3. **质量可靠** — gstack 确保交付达标

**记住原则：**
> 简单变更直接用 AI，中大型功能走三件套。
