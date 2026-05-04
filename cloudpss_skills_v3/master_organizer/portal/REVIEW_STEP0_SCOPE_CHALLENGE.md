# Portal 工程审查 - Step 0: Scope Challenge

**日期**: 2026-05-03  
**审查目标**: cloudpss_skills_v3/master_organizer/portal/ 质量提升  

---

## 1. 现有代码分析

### 1.1 当前文件结构

```
portal/
├── __init__.py              # 2 行
├── server.py                # 175 行 ✅ 合理
├── state.py                 # 664 行 ❌ 过大
├── model_editor.py          # 154 行 ✅ 合理
├── static/                  # 前端文件
│   ├── index.html           # 31KB
│   ├── app.js               # 85KB ❌ 过大
│   └── styles.css           # 58KB
└── tests/                   # 在 core/tests/ 中
```

### 1.2 现有部分解决方案

| 问题 | 现有方案 | 状态 |
|------|----------|------|
| API 端点 | server.py 中定义 | ✅ 基础存在 |
| 业务逻辑 | state.py 中混合 | ⚠️ 耦合严重 |
| 数据验证 | 内联验证 | ❌ 无统一方案 |
| 错误处理 | 基础 try/except | ⚠️ 不完整 |

**结论**: 现有代码有部分基础设施，但需要重构以提升质量。

---

## 2. 最小变更集分析

### 2.1 原始计划（完整重构）

```
创建:
- handlers/ (7 个文件)
- services/ (5 个文件)
- schemas/ (5 个文件)
- utils/ (4 个文件)
- tests/ (5 个文件)
修改:
- server.py (重构路由)
- state.py (删除)
总计: > 30 个文件变更
```

### 2.2 最小可行变更（MVP）

```
创建:
- handlers/ (6 个文件，从 state.py 拆分)
- schemas/ (3 个基础 DTO)
修改:
- server.py (更新导入)
- state.py (删除)
总计: ~10 个文件变更
```

**差异**: MVP 只拆分 state.py，暂时不创建 services/ 和完整 schemas/

---

## 3. 复杂性检查

### 3.1 原始计划复杂性 ❌

| 指标 | 数值 | 阈值 | 状态 |
|------|------|------|------|
| 文件数量 | > 30 | 8 | ❌ 超标 |
| 新服务类 | > 5 | 2 | ❌ 超标 |
| 架构层级 | 4 层 | - | ⚠️ 复杂 |

### 3.2 MVP 计划复杂性 ⚠️

| 指标 | 数值 | 阈值 | 状态 |
|------|------|------|------|
| 文件数量 | ~10 | 8 | ⚠️ 接近 |
| 新服务类 | 0 | 2 | ✅ 通过 |
| 架构层级 | 2 层 | - | ✅ 合理 |

---

## 4. 范围减少建议

### 建议: 分阶段实施

**理由**: 原始计划复杂度超标，一次性重构风险高。

**方案对比**:

| 方案 | 工作量 | 风险 | 收益 |
|------|--------|------|------|
| **A) 原始计划** (重构全部) | 2 周 | 高 | 完整 |
| **B) 分阶段** (推荐) | 1 周/阶段 | 低 | 渐进 |
| **C) 最小变更** | 3 天 | 最低 | 有限 |

**推荐**: **B) 分阶段实施**

### 阶段划分

```
Phase 1 (Week 1): 后端模块化
├── 拆分 state.py → handlers/
├── 创建基础 schemas/
├── 更新 server.py 路由
└── 验收: handlers 测试通过

Phase 2 (Week 2): 测试覆盖
├── Playwright E2E 测试
├── handlers 单元测试
├── 测试覆盖率报告
└── 验收: 覆盖率 > 80%

Phase 3 (Week 3): 前端优化
├── 拆分 app.js
├── 组件化
└── 验收: 前端模块化

Phase 4 (Week 4): 完善文档
├── OpenAPI 规范
├── 架构文档
└── 验收: 文档完整
```

---

## 5. 依赖检查

### 5.1 外部依赖

- Python 3.8+ (已满足)
- cloudpss SDK (已存在)
- Playwright (E2E 测试需要)

### 5.2 内部依赖

```
handlers/
  ├── workspace.py  → 依赖: core.registries
  ├── cases.py      → 依赖: core.registries, schemas.case
  ├── tasks.py      → 依赖: core.task_runner
  ├── results.py    → 依赖: core.release_ops
  ├── models.py     → 依赖: portal.model_editor
  └── audit.py      → 依赖: core.release_ops
```

**无循环依赖** ✅

---

## 6. 搜索检查 (Search Check)

### 6.1 架构模式检查

| 模式 | 检查 | 结果 |
|------|------|------|
| Python HTTP Server | 内置 http.server ✅ | Layer 1 |
| Dataclass DTO | Python 3.7+ ✅ | Layer 1 |
| Handler Pattern | 常用模式 ✅ | Layer 1 |
| CSV Streaming | pandas/read_csv ⚠️ | Layer 2 |

**结论**: 使用 Python 内置和标准模式，无创新令牌消耗。

---

## 7. TODOs 检查

### 7.1 项目 TODOs

检查 `TODOS.md`: 无相关 blocking TODOs

### 7.2 新增 TODOs

```markdown
## Portal Quality Improvement TODOs

### Phase 1: Backend Modularization
- [ ] 拆分 state.py 为 handlers/
- [ ] 创建基础 schemas/
- [ ] 更新 server.py 路由
- [ ] 添加 handlers 单元测试

### Phase 2: Test Coverage
- [ ] Playwright E2E 测试
- [ ] 测试覆盖率 > 80%
- [ ] CI 集成

### Phase 3: Frontend Optimization
- [ ] 拆分 app.js
- [ ] 组件化重构

### Phase 4: Documentation
- [ ] OpenAPI 规范
- [ ] 架构文档
- [ ] 用户指南
```

---

## 8. 完整性检查

### 8.1 当前计划完整性

| 维度 | 当前 | 目标 | 状态 |
|------|------|------|------|
| 代码重构 | 部分 | 完整 | 🟡 |
| 测试覆盖 | 缺失 | 80% | 🔴 |
| 文档 | 缺失 | 完整 | 🔴 |
| 类型注解 | 部分 | 100% | 🟡 |

### 8.2 Boil the Lake 评估

> "AI makes completeness cheap"

- 完整重构: 增加 ~2 小时 (AI 时间)
- 完整测试: 增加 ~3 小时 (AI 时间)
- 完整文档: 增加 ~1 小时 (AI 时间)

**结论**: 使用 AI 辅助，完整方案与最小方案成本差异不大。**推荐完整方案**。

---

## 9. 范围决策建议

### 9.1 决策问题

**D1 — 范围选择**: 一次性完整重构 vs 分阶段实施？

| 选项 | 描述 | 完整性 | 建议 |
|------|------|--------|------|
| A) 完整重构 | 一次性完成所有改进 | 10/10 | 风险高 |
| **B) 分阶段** | **4个 Phase，每阶段1周** | **9/10** | **推荐** |
| C) 最小变更 | 仅拆分 state.py | 5/10 | 收益低 |

**推荐**: **B) 分阶段实施**

**理由**:
- ✅ 降低风险（每阶段可独立验收）
- ✅ 渐进式改进（用户可提前使用）
- ✅ 便于回滚（阶段之间无强依赖）
- ⚠️ 总时间相同（4周 vs 4周）

### 9.2 第一阶段范围

**Phase 1: Backend Modularization (本周)**

**包含**:
- 拆分 state.py → 6 个 handler 文件
- 创建 3 个基础 schema 文件
- 更新 server.py 路由
- 添加 handler 单元测试

**不包含** (后续 Phase):
- Services 层（Phase 2）
- E2E 测试（Phase 2）
- 前端拆分（Phase 3）
- OpenAPI 文档（Phase 4）

---

## 10. 决策总结

| 决策 | 选择 | 理由 |
|------|------|------|
| 实施策略 | 分阶段 | 降低风险，渐进改进 |
| 第一阶段 | 后端模块化 | 核心问题，收益最大 |
| 工作量 | 1周 | 6个 handlers + 3个 schemas |
| 验收标准 | 测试通过 | handlers 单元测试覆盖 |

**下一步**: 进入 Section 1 - Architecture Review
