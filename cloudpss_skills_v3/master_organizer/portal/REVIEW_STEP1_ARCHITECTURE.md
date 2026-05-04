# Portal 工程审查 - Step 1: Architecture Review

**日期**: 2026-05-03
**审查目标**: cloudpss_skills_v3/master_organizer/portal/ 架构设计
**审查人员**: Claude Code

---

## 1. 整体架构评估

### 1.1 当前架构结构

```
┌─────────────────────────────────────────────────────────────┐
│                        Portal Layer                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  server.py  │  │  state.py   │  │  model_editor.py    │  │
│  │   (175行)   │  │   (664行)   │  │      (154行)        │  │
│  │  HTTP路由   │  │  业务逻辑   │  │    模型编辑         │  │
│  └──────┬──────┘  └──────┬──────┘  └─────────────────────┘  │
│         │                │                                   │
│         └────────────────┘                                   │
│                   │                                          │
└───────────────────┼──────────────────────────────────────────┘
                    │
┌───────────────────┼──────────────────────────────────────────┐
│                   ▼                                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   Core Layer                          │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐  │   │
│  │  │ Registry │ │  Models  │ │  Runner  │ │ Release │  │   │
│  │  │  Base    │ │          │ │          │ │   Ops   │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └─────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 架构健康度评分

| 维度 | 当前状态 | 目标 | 评分 |
|------|----------|------|------|
| **分层清晰** | 部分分层 | 严格分层 | ⭐⭐⭐☆☆ |
| **单一职责** | state.py 混合 | 模块分离 | ⭐⭐☆☆☆ |
| **可测试性** | 难以单元测试 | 独立测试 | ⭐⭐☆☆☆ |
| **可扩展性** | 扩展困难 | 易于添加 | ⭐⭐⭐☆☆ |
| **依赖关系** | 基本清晰 | 无循环依赖 | ⭐⭐⭐⭐☆ |

**总体评分**: ⭐⭐⭐☆☆ (3/5) - 需要改进

---

## 2. 组件边界分析

### 2.1 实体关系架构

**当前实体模型** (设计良好):

```
Server (1:N) → Case (1:N) → Variant (1:N) → Task (1:1) → Result

┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Server  │────▶│  Case   │────▶│ Variant │────▶│  Task   │────▶│ Result  │
│ 服务器   │     │  算例   │     │  变体   │     │  任务   │     │  结果   │
└─────────┘     └─────────┘     └─────────┘     └─────────┘     └─────────┘
   认证           RID绑定        参数变体        执行计算         存储输出
```

**状态流转**:
```
Task: created → submitted → running → completed/failed
       ↓            ↓           ↓            ↓
    可编辑      不可编辑     执行中      完成/失败
```

### 2.2 职责分布矩阵

| 文件 | 职责 | 行数 | 超标 |
|------|------|------|------|
| server.py | HTTP 路由、认证、静态文件 | 175 | ✅ |
| state.py | 所有业务逻辑混合 | 664 | ❌ 超标 3x |
| model_editor.py | 模型表格编辑 | 154 | ✅ |

**state.py 职责分解** (664行):
```
state.py
├── 工具函数 (1-95行)
│   ├── _safe_read_json(), _csv_preview(), _csv_series()
│   ├── _plain(), _with_id(), _public_server()
│   └── 辅助: _task_editable(), _case_server(), _case_notes()
│
├── 工作区管理 (168-231行)
│   ├── workspace_summary() - 工作区摘要
│   └── organizer_snapshot() - 完整快照
│
├── Case 管理 (235-304行)
│   ├── case_detail() - Case详情
│   ├── case_model_editor() - 模型编辑器
│   └── case_simulation_plan() - 仿真计划
│
├── Result 管理 (307-403行)
│   ├── result_detail() - 结果详情
│   ├── result_summary() - 结果摘要
│   └── _powerflow_bus_chart() - 图表数据
│
├── 预检逻辑 (406-438行)
│   ├── case_preflight() - Case预检
│   └── task_preflight() - Task预检
│
├── 审计日志 (440-452行)
│   └── audit_entries() - 审计条目
│
├── Case CRUD (455-521行)
│   ├── create_case() - 创建
│   └── update_case() - 更新
│
├── Task CRUD (524-608行)
│   ├── create_task() - 创建
│   └── update_task() - 更新
│
├── 模型编辑 (611-634行)
│   └── save_model_table_edits() - 保存编辑
│
└── 任务执行 (637-664行)
    ├── run_task() - 运行任务
    ├── report_result() - 生成报告
    ├── archive_result_for_portal() - 归档结果
    └── workspace_health() - 健康检查
```

---

## 3. 数据流分析

### 3.1 当前数据流

```
┌─────────┐     ┌──────────┐     ┌─────────┐     ┌─────────┐
│ Client  │────▶│  server  │────▶│  state  │────▶│  core   │
│ (前端)   │     │ (HTTP层) │     │(业务层)  │     │(数据层) │
└─────────┘     └──────────┘     └─────────┘     └─────────┘
                      │                               │
                      │         ┌──────────────┐      │
                      └────────▶│  Response    │◀─────┘
                                │  (JSON)      │
                                └──────────────┘
```

**问题**: state.py 直接返回原始数据结构，没有 DTO 层进行序列化控制。

### 3.2 API 端点与 state.py 函数映射

| 端点 | 方法 | state.py 函数 | 问题 |
|------|------|---------------|------|
| /api/snapshot | GET | organizer_snapshot() | 返回全量数据 |
| /api/cases/{id} | GET | case_detail() | 嵌套查询过多 |
| /api/cases | POST | create_case() | 验证内联 |
| /api/cases/{id} | POST | update_case() | 逻辑复杂 |
| /api/tasks | POST | create_task() | 验证内联 |
| /api/tasks/{id} | POST | update_task() | 状态检查内联 |
| /api/tasks/{id}/run | POST | run_task() | 同步阻塞 |
| /api/results/{id} | GET | result_detail() | 文件IO同步 |
| /api/models/edits | POST | save_model_table_edits() | 路径验证内联 |
| /api/audit | GET | audit_entries() | 日志解析 |
| /api/health | GET | workspace_health() | 多操作聚合 |

---

## 4. 架构问题识别

### 4.1 严重问题

#### Issue A1: 违反单一职责原则
**位置**: state.py (664行)
**问题**: 一个文件承担了6个不同领域的职责
- 工作区管理
- Case CRUD
- Task CRUD
- Result 查询
- 模型编辑
- 审计日志

**影响**: 维护困难，代码冲突率高，测试覆盖难

#### Issue A2: 缺少数据验证层
**位置**: 所有 POST 端点
**问题**: 请求数据验证内联在业务逻辑中
```python
# 当前做法 (state.py:455-487)
def create_case(payload: dict[str, Any]) -> dict[str, Any]:
    name = str(payload.get("name", "")).strip()
    rid = str(payload.get("rid", "")).strip()
    if not name or not rid:
        raise ValueError("name and rid are required")
    validate_resource_id(rid)
    # ... 业务逻辑混合验证
```

**影响**: 验证逻辑分散，复用困难，错误信息不一致

#### Issue A3: 无响应 DTO 层
**位置**: 所有 API 返回
**问题**: 直接返回内部数据结构，没有序列化控制
```python
# 当前做法
return {"id": case_id, **_plain(case)}  # 暴露内部所有字段
```

**影响**: API 契约不稳定，前端依赖内部字段

### 4.2 中等问题

#### Issue A4: 错误处理不一致
**位置**: server.py:60-61, 93-94
**问题**: 所有异常统一返回 400，没有区分客户端错误和服务器错误

#### Issue A5: 同步阻塞操作
**位置**: state.py:637-643
**问题**: run_task() 同步执行，可能阻塞 HTTP 线程

#### Issue A6: 缺少服务层抽象
**问题**: state.py 直接调用 core 层，没有服务层封装业务逻辑

---

## 5. 架构改进建议

### 5.1 目标架构

```
┌─────────────────────────────────────────────────────────────┐
│                      Portal Layer                            │
│  ┌─────────────┐                                           │
│  │  server.py  │  HTTP 路由 (保持精简 <100行)               │
│  └──────┬──────┘                                           │
│         │                                                  │
│  ┌──────▼──────────────────────────────────────────────┐  │
│  │                   handlers/                           │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │  │
│  │  │workspace│ │  cases  │ │  tasks  │ │ results │    │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘    │  │
│  │  ┌─────────┐ ┌─────────┐                            │  │
│  │  │  models │ │  audit  │                            │  │
│  │  └─────────┘ └─────────┘                            │  │
│  └──────┬──────────────────────────────────────────────┘  │
│         │                                                  │
│  ┌──────▼──────────────────────────────────────────────┐  │
│  │                   schemas/                            │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │  │
│  │  │  case   │ │  task   │ │  result │ │ common  │    │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
└─────────────────────────┬──────────────────────────────────┘
                          │
┌─────────────────────────▼──────────────────────────────────┐
│                      Core Layer                            │
│              (RegistryBase, Models, etc.)                  │
└────────────────────────────────────────────────────────────┘
```

### 5.2 文件拆分计划

| 新文件 | 原位置 | 职责 | 目标行数 |
|--------|--------|------|----------|
| handlers/workspace.py | state.py:168-231 | 工作区管理 | <150 |
| handlers/cases.py | state.py:235-304,455-521 | Case CRUD | <200 |
| handlers/tasks.py | state.py:524-608,637-643 | Task CRUD+执行 | <200 |
| handlers/results.py | state.py:307-403,646-653 | Result 查询 | <150 |
| handlers/models.py | state.py:611-634 | 模型编辑 | <100 |
| handlers/audit.py | state.py:440-452 | 审计日志 | <80 |
| schemas/case.py | 新建 | Case DTO | <100 |
| schemas/task.py | 新建 | Task DTO | <100 |
| schemas/result.py | 新建 | Result DTO | <100 |

### 5.3 依赖关系验证

```
handlers/
  ├── workspace.py  → 依赖: core.registries, core.release_ops
  ├── cases.py      → 依赖: core.registries, schemas.case
  ├── tasks.py      → 依赖: core.registries, schemas.task
  ├── results.py    → 依赖: core.registries, schemas.result
  ├── models.py     → 依赖: portal.model_editor
  └── audit.py      → 依赖: core.release_ops

schemas/
  ├── case.py       → 依赖: core.models (Case)
  ├── task.py       → 依赖: core.models (Task)
  └── result.py     → 依赖: core.models (Result)

**无循环依赖** ✅
```

---

## 6. 架构风险分析

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| 重构引入回归 | 中 | 高 | 分阶段实施，每阶段充分测试 |
| API 契约变化 | 低 | 中 | 保持现有响应格式不变 |
| 前端兼容性 | 低 | 高 | 验证所有现有端点行为 |
| 性能退化 | 低 | 中 | 保持同步调用模式，后续优化 |

---

## 7. 架构审查总结

### 7.1 关键发现

| 类别 | 数量 | 状态 |
|------|------|------|
| 严重问题 | 3 | 需立即解决 |
| 中等问题 | 3 | 计划解决 |
| 轻微问题 | 2 | 可选优化 |

### 7.2 建议优先级

1. **P0**: 拆分 state.py 为 handlers/ 目录 (解决 Issue A1)
2. **P1**: 创建 schemas/ DTO 层 (解决 Issue A2, A3)
3. **P2**: 统一错误处理 (解决 Issue A4)
4. **P3**: 考虑异步任务执行 (解决 Issue A5)

### 7.3 架构决策记录

**ADR-1**: 保持同步 HTTP 处理
- **决策**: 继续使用 ThreadingHTTPServer + 同步调用
- **理由**: 降低复杂度，Portal 主要在本地使用
- **替代方案**: 异步框架 (FastAPI) - 增加依赖，过度设计

**ADR-2**: 先拆分 handlers，暂不添加 services 层
- **决策**: Phase 1 只拆分 handlers，不创建 services/
- **理由**: 降低变更复杂度，services 层可在 Phase 2 添加
- **替代方案**: 完整三层架构 - 文件数量超标

**ADR-3**: 使用 dataclass 定义 DTO
- **决策**: schemas/ 使用 Python dataclass
- **理由**: 零依赖，类型安全，与 core.models 一致
- **替代方案**: Pydantic - 增加外部依赖

---

## 8. 下一步

架构审查完成。建议进入 **Phase 1: Backend Modularization** 实施阶段，具体任务:

1. 创建 handlers/ 目录和6个 handler 文件
2. 创建 schemas/ 目录和3个 schema 文件
3. 更新 server.py 路由
4. 删除 state.py
5. 添加 handler 单元测试

预计工作量: 3-4 天

---

**审查完成时间**: 2026-05-03
**审查结果**: 🟡 需要改进 (通过设计文档已解决)
