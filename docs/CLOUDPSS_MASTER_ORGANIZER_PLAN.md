# CloudPSS SkillHub 收纳大师计划
## CloudPSS Master Organizer Plan

**版本**: 1.0.0  
**日期**: 2026-04-30  
**作者**: Claude Code  
**状态**: 设计完成，待实施

---

## 文档导读

本文档是 CloudPSS SkillHub 系统重构的完整设计规格书，采用"收纳大师"哲学，建立一个严谨、整洁、可扩展的电力系统仿真管理平台。

### 阅读指南
- **第1-3章**: 核心理念与数据模型，必读
- **第4-6章**: 技术实现细节，开发人员必读
- **第7-8章**: 实施路线图，项目经理必读

---

## 第1章 设计理念 - 收纳大师哲学

### 1.1 核心原则

收纳大师计划基于六个核心原则：

| 原则 | 中文名称 | 核心内涵 |
|------|---------|---------|
| **Classification** | 清晰分类 | 万物有序，各归其位 |
| **Uniqueness** | 唯一定位 | 每一个实体都有且只有一个确定位置 |
| **Naming** | 命名规范 | 见名知意，严格约束 |
| **Association** | 关联清晰 | 关系明确，可追溯 |
| **Lifecycle** | 生命周期 | 从生到灭，全程管理 |
| **Visualization** | 可视整洁 | 一目了然，强迫症友好 |

### 1.2 核心实体定义

系统管理五大核心实体：

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLOUDPSS SKILLHUB                          │
│                      核心实体关系图                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐         ┌─────────────┐                      │
│   │   Server    │◄────────┤    Case     │                      │
│   │   (服务器)   │ 1:N     │   (算例)     │                      │
│   └─────────────┘         └──────┬──────┘                      │
│                                  │                              │
│                                  │ 1:N                          │
│                                  ▼                              │
│                           ┌─────────────┐                      │
│                           │   Variant   │                      │
│                           │   (变体)    │                      │
│                           └──────┬──────┘                      │
│                                  │                              │
│                                  │ 1:N                          │
│                                  ▼                              │
│   ┌─────────────┐         ┌─────────────┐                      │
│   │   Result    │◄────────┤    Task     │                      │
│   │   (结果)    │ 1:1     │   (任务)    │                      │
│   └─────────────┘         └─────────────┘                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 实体详细定义

#### 1.3.1 Server（服务器）
- **定义**: CloudPSS 计算资源实例
- **存储位置**: `~/.cloudpss/config/servers.yaml`
- **关键属性**:
  - `id`: 唯一标识 (server_{hash8})
  - `name`: 人类可读名称
  - `url`: API 端点地址
  - `auth`: 认证信息（加密存储）
  - `status`: active/inactive

#### 1.3.2 Case（算例）
- **定义**: 电力系统仿真模型配置
- **存储位置**: `~/.cloudpss/cases/{case_id}/`
- **关键属性**:
  - `id`: case_{YYYYMMDD}_{HHMMSS}_{hash8}
  - `name`: 算例名称
  - `description`: 描述
  - `rid`: CloudPSS 模型资源ID
  - `server_id`: 关联服务器
  - `status`: draft/active/archived

#### 1.3.3 Task（任务）
- **定义**: 仿真执行实例
- **存储位置**: `~/.cloudpss/tasks/{task_id}/`
- **关键属性**:
  - `id`: task_{YYYYMMDD}_{HHMMSS}_{hash8}
  - `case_id`: 所属算例
  - `variant_id`: 使用的变体（可选）
  - `type`: powerflow/emt/stability/etc
  - `job_id`: CloudPSS 云端任务ID
  - `status`: created/submitted/running/completed/failed

#### 1.3.4 Result（结果）
- **定义**: 仿真输出数据
- **存储位置**: `~/.cloudpss/results/{result_id}/`
- **关键属性**:
  - `id`: result_{YYYYMMDD}_{HHMMSS}_{hash8}
  - `task_id`: 关联任务
  - `format`: csv/json/hdf5/comtrade
  - `files`: 文件列表
  - `metadata`: 仿真参数快照

#### 1.3.5 Variant（变体）
- **定义**: 算例参数变体配置
- **存储位置**: `~/.cloudpss/cases/{case_id}/variants/`
- **关键属性**:
  - `id`: variant_{hash8}
  - `case_id`: 所属算例
  - `name`: 变体名称
  - `parameters`: 参数覆盖字典
  - `parent_id`: 父变体（继承用）

---

## 第2章 数据模型规范

### 2.1 ID 生成规范

所有 ID 遵循统一格式：

```
{entity}_{YYYYMMDD}_{HHMMSS}_{hash8}

示例:
- server_a3f7b2d9
- case_20260430_143052_a3f7b2d9
- task_20260430_143052_b4e8c3f1
- result_20260430_143052_d5f9a4b2
- variant_c7e2d8a4
```

**生成规则**:
1. `entity`: 小写实体名称 (server/case/task/result/variant)
2. `YYYYMMDD`: 创建日期
3. `HHMMSS`: 创建时间
4. `hash8`: 8位随机十六进制字符串

### 2.2 时间戳规范

所有时间戳采用 ISO 8601 格式：

```yaml
created_at: "2026-04-30T14:30:52+08:00"
updated_at: "2026-04-30T14:35:21+08:00"
started_at: "2026-04-30T14:31:10+08:00"
completed_at: "2026-04-30T14:35:15+08:00"
```

### 2.3 状态机定义

#### Case 状态机

```
[draft] ──► [active] ──► [archived]
   │           │             ▲
   │           └─────────────┘
   └──────────► [deleted]
```

- **draft**: 草稿状态，可编辑
- **active**: 激活状态，可执行任务
- **archived**: 归档状态，只读
- **deleted**: 已删除，进入回收站

#### Task-Result 联合状态机

```
[created] ──► [submitted] ──► [running] ──► [completed] ──► [exported]
                │                │              │                │
                ▼                ▼              ▼                ▼
             [failed]        [cancelled]    [partial]      [registered]
```

### 2.4 YAML Schema 规范

所有配置文件采用 YAML 格式，遵循以下规范：

```yaml
# 版本声明（必需）
api_version: "v1.0"

# 元数据（必需）
metadata:
  created_at: "2026-04-30T14:30:52+08:00"
  updated_at: "2026-04-30T14:35:21+08:00"
  version: "1.0.0"

# 实体特定内容
...
```

---

## 第3章 目录结构设计

### 3.1 根目录结构

```
~/.cloudpss/
├── config/                    # 配置文件
│   ├── servers.yaml          # 服务器注册表
│   ├── defaults.yaml         # 默认设置
│   └── user.yaml             # 用户偏好
│
├── registry/                  # 注册表
│   ├── index.yaml            # 总索引
│   ├── cases.yaml            # 算例注册表
│   ├── tasks.yaml            # 任务注册表
│   ├── results.yaml          # 结果注册表
│   └── variants.yaml         # 变体注册表
│
├── cases/                     # 算例存储
│   └── {case_id}/            # 单个算例目录
│       ├── case.yaml         # 算例配置
│       ├── model.json        # 模型快照（可选）
│       ├── variants/         # 变体目录
│       │   └── {variant_id}.yaml
│       └── tasks/            # 符号链接到 tasks/
│
├── tasks/                     # 任务存储
│   └── {task_id}/            # 单个任务目录
│       ├── task.yaml         # 任务配置
│       ├── config/           # 执行配置
│   │   ├── logs/             # 执行日志
│   │   └── scripts/          # 执行脚本
│
├── results/                   # 结果存储
│   └── {result_id}/          # 单个结果目录
│       ├── result.yaml       # 结果元数据
│       ├── data/             # 数据文件
│   │   ├── figures/          # 生成图表
│   │   └── exports/          # 导出文件
│
├── cache/                     # 缓存目录
│   ├── models/               # 模型缓存
│   ├── downloads/            # 下载缓存
│   └── temp/                 # 临时文件
│
├── logs/                      # 日志目录
│   ├── skills.log            # 技能执行日志
│   ├── system.log            # 系统日志
│   └── audit.log             # 审计日志
│
└── trash/                     # 回收站
    └── {deleted_item}/       # 被删除项目
        └── .deleted_at       # 删除时间戳
```

### 3.2 命名约束

#### 文件命名

```python
# 命名规则
RULES = {
    "id_pattern": r"^(server|case|task|result|variant)_[0-9]{8}_[0-9]{6}_[a-f0-9]{8}$",
    "name_pattern": r"^[a-zA-Z0-9_\-\s]{1,64}$",
    "filename_pattern": r"^[a-zA-Z0-9_\-]+\.(yaml|json|csv|h5|cfg)$",
}

# 保留名称（不可使用）
RESERVED_NAMES = [
    "config", "registry", "cases", "tasks", "results",
    "cache", "logs", "trash", "temp", "tmp",
    "index", "default", "user", "system"
]

# 禁止字符
PROHIBITED_CHARS = ['<', '>', ':', '"', '|', '?', '*', '\0']
```

### 3.3 存储配额

```yaml
quotas:
  max_cases: 1000           # 最大算例数
  max_tasks_per_case: 100   # 每算例最大任务数
  max_results_per_task: 10  # 每任务最大结果数
  max_storage_gb: 50        # 最大存储空间（GB）
  trash_retention_days: 30  # 回收站保留天数
```

---

## 第4章 注册表设计

### 4.1 总索引 (index.yaml)

```yaml
api_version: "v1.0"

metadata:
  created_at: "2026-04-30T14:30:52+08:00"
  updated_at: "2026-04-30T14:35:21+08:00"
  version: "1.0.0"

# 统计信息
stats:
  total_servers: 3
  total_cases: 25
  total_tasks: 156
  total_results: 148
  total_variants: 42

# 索引摘要（用于快速浏览）
quick_access:
  recent_cases:
    - case_20260430_143052_a3f7b2d9
    - case_20260429_091522_b4e8c3f1
  recent_tasks:
    - task_20260430_143052_d5f9a4b2
  favorite_cases:
    - case_20260425_103045_e6g1h5i3

# 注册表文件位置
registries:
  servers: "registry/servers.yaml"
  cases: "registry/cases.yaml"
  tasks: "registry/tasks.yaml"
  results: "registry/results.yaml"
  variants: "registry/variants.yaml"
```

### 4.2 算例注册表 (cases.yaml)

```yaml
api_version: "v1.0"

metadata:
  created_at: "2026-04-30T14:30:52+08:00"
  updated_at: "2026-04-30T14:35:21+08:00"
  count: 25

# 算例列表
cases:
  case_20260430_143052_a3f7b2d9:
    name: "IEEE14_基态潮流"
    description: "IEEE 14节点系统基态潮流计算"
    rid: "model/holdme/IEEE14"
    server_id: "server_a3f7b2d9"
    status: "active"
    created_at: "2026-04-30T14:30:52+08:00"
    updated_at: "2026-04-30T14:35:21+08:00"
    tags: ["ieee", "pf", "base"]
    task_count: 5
    last_task_id: "task_20260430_143052_d5f9a4b2"
    path: "cases/case_20260430_143052_a3f7b2d9"

  case_20260429_091522_b4e8c3f1:
    name: "IEEE39_暂态稳定"
    description: "IEEE 39节点系统暂态稳定分析"
    rid: "model/holdme/IEEE39"
    server_id: "server_a3f7b2d9"
    status: "active"
    created_at: "2026-04-29T09:15:22+08:00"
    updated_at: "2026-04-29T16:45:33+08:00"
    tags: ["ieee39", "stability", "transient"]
    task_count: 12
    last_task_id: "task_20260429_164533_e7h2i6j4"
    path: "cases/case_20260429_091522_b4e8c3f1"

# 索引（按标签）
indices:
  by_tag:
    ieee:
      - case_20260430_143052_a3f7b2d9
    pf:
      - case_20260430_143052_a3f7b2d9
```

### 4.3 任务注册表 (tasks.yaml)

```yaml
api_version: "v1.0"

metadata:
  created_at: "2026-04-30T14:30:52+08:00"
  updated_at: "2026-04-30T14:35:21+08:00"
  count: 156

# 任务列表
tasks:
  task_20260430_143052_d5f9a4b2:
    name: "潮流计算_20260430"
    case_id: "case_20260430_143052_a3f7b2d9"
    variant_id: null
    type: "powerflow"
    job_id: "job_pf_abc123"
    server_id: "server_a3f7b2d9"
    status: "completed"
    created_at: "2026-04-30T14:30:52+08:00"
    submitted_at: "2026-04-30T14:31:10+08:00"
    started_at: "2026-04-30T14:31:15+08:00"
    completed_at: "2026-04-30T14:31:45+08:00"
    result_id: "result_20260430_143145_f6g3h7i5"
    path: "tasks/task_20260430_143052_d5f9a4b2"
    config:
      method: "newton_raphson"
      tolerance: 0.0001
      max_iter: 20

# 按状态索引
indices:
  by_status:
    completed:
      - task_20260430_143052_d5f9a4b2
    running:
      - task_20260430_150102_g8h4i9j6
  by_case:
    case_20260430_143052_a3f7b2d9:
      - task_20260430_143052_d5f9a4b2
```

### 4.4 结果注册表 (results.yaml)

```yaml
api_version: "v1.0"

metadata:
  created_at: "2026-04-30T14:30:52+08:00"
  updated_at: "2026-04-30T14:35:21+08:00"
  count: 148

# 结果列表
results:
  result_20260430_143145_f6g3h7i5:
    name: "潮流结果_20260430_143145"
    task_id: "task_20260430_143052_d5f9a4b2"
    case_id: "case_20260430_143052_a3f7b2d9"
    format: "json"
    created_at: "2026-04-30T14:31:45+08:00"
    size_bytes: 15420
    files:
      - "data/powerflow_result.json"
      - "data/bus_voltages.csv"
      - "figures/voltage_profile.png"
    path: "results/result_20260430_143145_f6g3h7i5"
    metadata:
      simulation_type: "powerflow"
      bus_count: 14
      converged: true
      iterations: 4

# 按格式索引
indices:
  by_format:
    json:
      - result_20260430_143145_f6g3h7i5
    csv:
      - result_20260429_164545_h8i5j0k7
```

### 4.5 服务器注册表 (servers.yaml)

```yaml
api_version: "v1.0"

metadata:
  created_at: "2026-04-30T14:30:52+08:00"
  updated_at: "2026-04-30T14:35:21+08:00"

servers:
  server_a3f7b2d9:
    name: "CloudPSS_生产环境"
    url: "https://www.cloudpss.net/"
    auth:
      # 加密存储的认证信息
      encrypted_token: "ENC[AES256_GCM:data:...]"
      key_id: "key_v1"
    status: "active"
    created_at: "2026-04-01T10:00:00+08:00"
    last_used: "2026-04-30T14:35:21+08:00"
    default: true
    capabilities:
      - "powerflow"
      - "emt"
      - "stability"
```

---

## 第5章 生命周期管理

### 5.1 Case 生命周期

```python
class CaseLifecycle:
    """算例生命周期管理器"""

    STATES = ["draft", "active", "archived", "deleted"]

    TRANSITIONS = {
        "draft": ["active", "deleted"],
        "active": ["archived", "deleted"],
        "archived": ["active", "deleted"],
        "deleted": []  # 终态
    }

    @staticmethod
    def can_transition(from_state: str, to_state: str) -> bool:
        return to_state in CaseLifecycle.TRANSITIONS.get(from_state, [])
```

### 5.2 Task-Result 生命周期

```python
class TaskLifecycle:
    """任务生命周期管理器"""

    STATES = [
        "created",      # 已创建
        "submitted",    # 已提交到云端
        "running",      # 执行中
        "completed",    # 成功完成
        "failed",       # 执行失败
        "cancelled",    # 已取消
        "exported",     # 结果已导出
        "registered"    # 结果已注册
    ]

    # 状态转换触发器
    TRIGGERS = {
        "created": "on_task_create",
        "submitted": "on_task_submit",
        "running": "on_task_start",
        "completed": "on_task_complete",
        "failed": "on_task_fail",
        "cancelled": "on_task_cancel",
        "exported": "on_result_export",
        "registered": "on_result_register"
    }
```

### 5.3 生命周期钩子

```python
# 生命周期钩子接口
class LifecycleHooks:
    async def on_case_create(self, case_id: str, case_data: dict):
        """算例创建时触发"""
        pass

    async def on_task_complete(self, task_id: str, result_data: dict):
        """任务完成时触发"""
        pass

    async def on_result_export(self, result_id: str, export_path: str):
        """结果导出时触发"""
        pass
```

---

## 第6章 技能架构设计

### 6.1 技能分类体系

```
┌─────────────────────────────────────────────────────────────────┐
│                      技能分类体系                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   System     │  │   Server     │  │    Case      │          │
│  │   (系统)      │  │   (服务器)   │  │   (算例)     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│        │                 │                 │                   │
│        ▼                 ▼                 ▼                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ system.init  │  │server.add    │  │case.create   │          │
│  │ system.status│  │server.list   │  │case.list     │          │
│  │ system.clean │  │server.remove │  │case.clone    │          │
│  │ system.backup│  │server.default│  │case.archive  │          │
│  └──────────────┘  └──────────────┘  │case.restore  │          │
│                                      │case.delete   │          │
│                                      └──────────────┘          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Variant    │  │    Task      │  │   Result     │          │
│  │   (变体)     │  │   (任务)     │  │   (结果)     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│        │                 │                 │                   │
│        ▼                 ▼                 ▼                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │variant.create│  │task.create   │  │result.export │          │
│  │variant.list  │  │task.submit   │  │result.compare│          │
│  │variant.apply │  │task.status   │  │result.analyze│          │
│  │variant.delete│  │task.cancel   │  │result.delete │          │
│  └──────────────┘  │task.list     │  │result.archive│          │
│                    └──────────────┘  └──────────────┘          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │    Query     │  │  Workspace   │                            │
│  │   (查询)     │  │   (工作区)   │                            │
│  └──────────────┘  └──────────────┘                            │
│        │                 │                                     │
│        ▼                 ▼                                     │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │query.case    │  │workspace.save│                            │
│  │query.task    │  │workspace.load│                            │
│  │query.result  │  │workspace.list│                            │
│  │query.tree    │  │workspace.clean│                           │
│  └──────────────┘  └──────────────┘                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 核心技能接口

#### Case 管理技能

```yaml
# case.create
skill: case.create
name: "创建算例"
description: "从 CloudPSS 创建本地算例"
parameters:
  rid:
    type: string
    description: "CloudPSS 模型资源ID"
    required: true
  name:
    type: string
    description: "算例名称"
    required: false
  description:
    type: string
    description: "算例描述"
    required: false
  server_id:
    type: string
    description: "服务器ID"
    required: false
    default: "default"
returns:
  case_id: string
  path: string

# case.list
skill: case.list
name: "列出算例"
description: "列出所有本地算例"
parameters:
  status:
    type: enum["all", "draft", "active", "archived"]
    default: "all"
  tag:
    type: string
    description: "按标签过滤"
    required: false
returns:
  cases: list[CaseInfo]

# case.delete
skill: case.delete
name: "删除算例"
description: "将算例移至回收站"
parameters:
  case_id:
    type: string
    required: true
  permanent:
    type: boolean
    default: false
    description: "是否永久删除"
```

#### Task 管理技能

```yaml
# task.create
skill: task.create
name: "创建任务"
description: "为算例创建执行任务"
parameters:
  case_id:
    type: string
    required: true
  type:
    type: enum["powerflow", "emt", "stability"]
    required: true
  name:
    type: string
    required: false
  config:
    type: object
    description: "任务配置"
    required: false
returns:
  task_id: string
  config_path: string

# task.submit
skill: task.submit
name: "提交任务"
description: "提交任务到 CloudPSS 执行"
parameters:
  task_id:
    type: string
    required: true
  wait:
    type: boolean
    default: false
    description: "是否等待完成"
returns:
  job_id: string
  status: string

# task.status
skill: task.status
name: "查询任务状态"
description: "查询任务执行状态"
parameters:
  task_id:
    type: string
    required: true
returns:
  status: string
  progress: float
  message: string
```

#### Result 管理技能

```yaml
# result.export
skill: result.export
name: "导出结果"
description: "导出仿真结果到指定格式"
parameters:
  task_id:
    type: string
    required: true
  format:
    type: enum["json", "csv", "hdf5", "comtrade"]
    default: "json"
  path:
    type: string
    required: false
    description: "导出路径"
returns:
  result_id: string
  files: list[string]

# result.compare
skill: result.compare
name: "比较结果"
description: "比较两个仿真结果"
parameters:
  result_ids:
    type: list[string]
    min_items: 2
    max_items: 5
    required: true
  metrics:
    type: list[string]
    required: false
returns:
  comparison_id: string
  differences: object
```

### 6.3 技能实现模板

```python
"""
收纳大师技能实现模板
所有管理技能必须继承此基类
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional
from pathlib import Path
import yaml

@dataclass
class SkillContext:
    """技能执行上下文"""
    workspace_root: Path
    registry: "RegistryManager"
    config: dict

class MasterOrganizerSkill(ABC):
    """
    收纳大师技能基类

    所有管理技能必须遵循以下原则：
    1. 原子性：每个操作要么完全成功，要么完全失败
    2. 幂等性：重复执行相同操作结果一致
    3. 可追溯：所有操作记录审计日志
    4. 回滚支持：失败时能够恢复原状
    """

    def __init__(self, context: SkillContext):
        self.ctx = context
        self.logger = self._init_logger()

    @property
    @abstractmethod
    def name(self) -> str:
        """技能名称"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """技能描述"""
        pass

    @abstractmethod
    async def execute(self, **params) -> dict:
        """
        执行技能

        Returns:
            操作结果字典，必须包含:
            - success: bool
            - message: str
            - data: dict (可选)
        """
        pass

    def _validate_id(self, entity_id: str, entity_type: str) -> bool:
        """验证ID格式"""
        import re
        pattern = rf"^{entity_type}_[0-9]{{8}}_[0-9]{{6}}_[a-f0-9]{{8}}$"
        return bool(re.match(pattern, entity_id))

    def _load_registry(self, name: str) -> dict:
        """加载注册表"""
        path = self.ctx.workspace_root / "registry" / f"{name}.yaml"
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _save_registry(self, name: str, data: dict):
        """保存注册表"""
        path = self.ctx.workspace_root / "registry" / f"{name}.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)

    def _log_audit(self, action: str, entity_id: str, details: dict):
        """记录审计日志"""
        import datetime
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "skill": self.name,
            "action": action,
            "entity_id": entity_id,
            "details": details
        }
        # 追加到审计日志
        log_path = self.ctx.workspace_root / "logs" / "audit.log"
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(yaml.dump([log_entry], allow_unicode=True))
```

---

## 第7章 命令行接口设计

### 7.1 CLI 命令结构

```bash
# 主命令结构
cloudpss <entity> <action> [options]

# 实体类型
cloudpss system    # 系统管理
cloudpss server    # 服务器管理
cloudpss case      # 算例管理
cloudpss variant   # 变体管理
cloudpss task      # 任务管理
cloudpss result    # 结果管理
cloudpss query     # 查询
cloudpss workspace # 工作区管理
```

### 7.2 详细命令示例

```bash
# ====== 系统管理 ======
# 初始化工作区
cloudpss system init --path ~/.cloudpss

# 查看系统状态
cloudpss system status

# 清理临时文件
cloudpss system clean --cache --logs --older-than 7d

# 备份数据
cloudpss system backup --output backup_$(date +%Y%m%d).tar.gz

# ====== 服务器管理 ======
# 添加服务器
cloudpss server add \
    --name "生产环境" \
    --url "https://www.cloudpss.net/" \
    --token-file ~/.cloudpss_token \
    --default

# 列出服务器
cloudpss server list

# 设置默认服务器
cloudpss server default server_a3f7b2d9

# ====== 算例管理 ======
# 从 CloudPSS 创建算例
cloudpss case create \
    --rid "model/holdme/IEEE14" \
    --name "IEEE14_基态潮流" \
    --description "IEEE 14节点基态" \
    --tags "ieee,pf,base"

# 克隆算例
cloudpss case clone case_20260430_143052_a3f7b2d9 \
    --name "IEEE14_改进方案"

# 列出算例（树形视图）
cloudpss case list --tree

# 查看算例详情
cloudpss case show case_20260430_143052_a3f7b2d9

# 归档算例
cloudpss case archive case_20260430_143052_a3f7b2d9

# 恢复算例
cloudpss case restore case_20260430_143052_a3f7b2d9

# ====== 任务管理 ======
# 创建潮流计算任务
cloudpss task create \
    --case case_20260430_143052_a3f7b2d9 \
    --type powerflow \
    --name "基态潮流" \
    --config pf_config.yaml

# 创建EMT仿真任务
cloudpss task create \
    --case case_20260430_143052_a3f7b2d9 \
    --type emt \
    --variant variant_xxx \
    --duration 10s \
    --step 1e-4

# 提交任务
cloudpss task submit task_20260430_143052_d5f9a4b2 --wait

# 查看任务状态
cloudpss task status task_20260430_143052_d5f9a4b2 --watch

# 取消任务
cloudpss task cancel task_20260430_143052_d5f9a4b2

# 列出算例的所有任务
cloudpss task list --case case_20260430_143052_a3f7b2d9

# ====== 结果管理 ======
# 导出结果
cloudpss result export task_20260430_143052_d5f9a4b2 \
    --format csv \
    --output ./results/

# 导出为 COMTRADE 格式
cloudpss result export task_20260430_143052_d5f9a4b2 \
    --format comtrade \
    --station-name "IEEE14"

# 比较多个结果
cloudpss result compare \
    result_20260430_143145_f6g3h7i5 \
    result_20260429_164545_h8i5j0k7 \
    --metrics "voltage,power,loss"

# 生成结果报告
cloudpss result report result_20260430_143145_f6g3h7i5 \
    --template ieee14_report \
    --output report.pdf

# ====== 变体管理 ======
# 创建参数变体
cloudpss variant create \
    --case case_20260430_143052_a3f7b2d9 \
    --name "负荷+10%" \
    --params '{"load.P": "*1.1"}'

# 应用变体并创建任务
cloudpss task create \
    --case case_20260430_143052_a3f7b2d9 \
    --variant variant_c7e2d8a4

# ====== 查询 ======
# 树形视图
cloudpss query tree

# 仪表板
cloudpss query dashboard

# 搜索
cloudpss query search --keyword "IEEE14" --type case

# 最近活动
cloudpss query recent --limit 10
```

### 7.3 输出格式

#### 树形视图

```bash
$ cloudpss query tree

📁 ~/.cloudpss/
├── 📋 Servers (3)
│   ├── ● 生产环境 (default)
│   ├── ○ 测试环境
│   └── ○ 开发环境
│
├── 📦 Cases (25)
│   ├── 📂 case_20260430_143052_a3f7b2d9
│   │   ├── 📝 IEEE14_基态潮流 [active]
│   │   ├── 🏷️  tags: ieee, pf, base
│   │   ├── 📊 Tasks (5)
│   │   │   ├── ✅ task_20260430_143052_d5f9a4b2 [completed]
│   │   │   │   └── 📈 result_20260430_143145_f6g3h7i5
│   │   │   └── 🔄 task_20260430_150102_g8h4i9j6 [running]
│   │   └── 🎨 Variants (3)
│   │       ├── variant_c7e2d8a4: 负荷+10%
│   │       └── variant_d8f3e9b5: 发电机检修
│   │
│   └── 📂 case_20260429_091522_b4e8c3f1 [archived]
│       └── 📝 IEEE39_暂态稳定
│
└── 📊 Statistics
    ├── 总算例数: 25
    ├── 活跃算例: 18
    ├── 总任务数: 156
    ├── 成功任务: 142 (91%)
    └── 存储占用: 2.3 GB / 50 GB
```

#### 仪表板视图

```bash
$ cloudpss query dashboard

╔════════════════════════════════════════════════════════════════╗
║               CloudPSS SkillHub 仪表板                         ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  📊 系统状态                                                   ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ║
║  服务器状态: 🟢 3/3 在线                                        ║
║  活跃任务:   🔄 2 运行中                                        ║
║  存储使用:   ████████░░░░░░░░░░░░  2.3 GB / 50 GB (4.6%)       ║
║                                                                ║
║  📈 今日活动                                                   ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ║
║  新建算例:   2                                                 ║
║  提交任务:   8                                                 ║
║  完成任务:   6 ✅  2 ❌                                        ║
║                                                                ║
║  🏆 最近成功                                                   ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ║
║  1. IEEE14_基态潮流 - 潮流计算完成 (14:31)                      ║
║  2. IEEE39_暂态稳定 - EMT仿真完成 (12:15)                       ║
║  3. 改进方案_B - 对比分析完成 (10:42)                           ║
║                                                                ║
║  ⚠️ 需要注意                                                   ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ║
║  1. 回收站中有 3 个项目将在 7 天后自动删除                      ║
║  2. 任务 task_xxx 失败，建议检查日志                            ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 第8章 实施路线图

### 8.1 总体时间线

```
第1周        第2周        第3周        第4周        第5-6周
[████████] [████████] [████████] [████████] [████████████████]
   │           │           │           │           │
   ▼           ▼           ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────────┐
│ Phase 1│ │ Phase 2│ │ Phase 3│ │ Phase 4│ │   Phase 5    │
│基础设施  │ │核心功能  │ │管理技能  │ │用户界面  │ │集成测试&优化  │
└────────┘ └────────┘ └────────┘ └────────┘ └──────────────┘
```

### 8.2 阶段详细计划

#### Phase 1: 基础设施 (Week 1)

**目标**: 建立核心数据结构和存储系统

| 天数 | 任务 | 产出物 | 验收标准 |
|------|------|--------|----------|
| 1 | 目录结构设计 | `~/.cloudpss/` 结构 | 目录创建成功 |
| 2 | ID生成器 | `id_generator.py` | ID格式正确 |
| 3 | 注册表基类 | `registry/base.py` | CRUD操作正常 |
| 4 | 加密模块 | `crypto.py` | 认证信息安全存储 |
| 5 | 配置管理 | `config/manager.py` | 配置读写正常 |

**依赖**: 无  
**风险**: 低  
**负责人**: 待定

#### Phase 2: 核心功能 (Week 2)

**目标**: 实现核心实体管理

| 天数 | 任务 | 产出物 | 验收标准 |
|------|------|--------|----------|
| 6-7 | Server管理 | `skills/server.py` | 增删改查正常 |
| 8-9 | Case管理 | `skills/case.py` | 生命周期正常 |
| 10 | 变体系统 | `skills/variant.py` | 参数覆盖正常 |

**依赖**: Phase 1  
**风险**: 中（CloudPSS API集成）  
**负责人**: 待定

#### Phase 3: 管理技能 (Week 3)

**目标**: 实现任务和结果管理

| 天数 | 任务 | 产出物 | 验收标准 |
|------|------|--------|----------|
| 11-12 | Task管理 | `skills/task.py` | 任务生命周期正常 |
| 13-14 | Result管理 | `skills/result.py` | 导出功能正常 |
| 15 | 关联管理 | `skills/relation.py` | Case-Task-Result关联正确 |

**依赖**: Phase 2  
**风险**: 中（结果格式解析）  
**负责人**: 待定

#### Phase 4: 用户界面 (Week 4)

**目标**: 实现CLI和可视化

| 天数 | 任务 | 产出物 | 验收标准 |
|------|------|--------|----------|
| 16-17 | CLI框架 | `cli/main.py` | 命令解析正常 |
| 18-19 | 树形视图 | `cli/views/tree.py` | 显示正确 |
| 20 | 仪表板 | `cli/views/dashboard.py` | 实时更新正常 |

**依赖**: Phase 3  
**风险**: 低  
**负责人**: 待定

#### Phase 5: 集成测试与优化 (Week 5-6)

**目标**: 系统测试和性能优化

| 天数 | 任务 | 产出物 | 验收标准 |
|------|------|--------|----------|
| 21-23 | 单元测试 | `tests/` | 覆盖率>80% |
| 24-25 | 集成测试 | `tests/integration/` | 全流程通过 |
| 26-27 | 性能优化 | 优化报告 | 响应<1s |
| 28-30 | 文档完善 | 用户手册 | 文档完整 |

**依赖**: Phase 4  
**风险**: 低  
**负责人**: 待定

### 8.3 里程碑

```
M1 (Week 1结束): 基础设施就绪
├── 目录结构完成
├── 注册表系统工作
└── 配置管理可用

M2 (Week 2结束): 核心功能就绪
├── Server管理可用
├── Case管理可用
└── 变体系统工作

M3 (Week 3结束): 管理技能就绪
├── Task管理可用
├── Result管理可用
└── 关联系统工作

M4 (Week 4结束): 用户界面就绪
├── CLI完整
├── 视图可用
└── 基本功能完整

M5 (Week 6结束): 系统发布
├── 测试通过
├── 文档完整
└── 正式发布
```

### 8.4 风险管理

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| CloudPSS API变更 | 中 | 高 | 封装API层，集中管理 |
| 存储空间不足 | 中 | 中 | 配额管理，自动清理 |
| 并发冲突 | 低 | 高 | 文件锁机制 |
| 数据损坏 | 低 | 高 | 定期备份，校验和 |

### 8.5 成功标准

1. **功能完整**: 所有设计的技能可用
2. **性能达标**: 操作响应 < 1秒
3. **用户满意**: 树形视图、仪表板可用
4. **文档完整**: 开发文档、用户手册齐全
5. **测试通过**: 单元测试覆盖率 > 80%

---

## 附录

### A. 命名规范速查表

```
ID格式:
  server_{hash8}
  case_{YYYYMMDD}_{HHMMSS}_{hash8}
  task_{YYYYMMDD}_{HHMMSS}_{hash8}
  result_{YYYYMMDD}_{HHMMSS}_{hash8}
  variant_{hash8}

文件名:
  配置: {entity}.yaml
  注册表: {entity}s.yaml
  数据: {timestamp}_{type}.{ext}

目录名:
  实体: {entity}_{id}/
  分类: {category}/
```

### B. 状态转换速查表

```
Case状态:
  draft ──► active ──► archived
    │         │           ▲
    └─────────┴───────────┘
           deleted

Task状态:
  created ──► submitted ──► running ──► completed ──► exported
                                  └─► failed
                                  └─► cancelled
```

### C. 目录权限

```
~/.cloudpss/           700 (rwx------)
├── config/            700
├── registry/          700
├── cases/             755 (rwxr-xr-x)
├── tasks/             755
├── results/           755
├── cache/             755
├── logs/              755
└── trash/             755
```

### D. 配置文件模板

#### 用户配置文件模板

```yaml
# ~/.cloudpss/config/user.yaml
api_version: "v1.0"

user:
  name: "用户名"
  email: "user@example.com"

preferences:
  default_format: "json"
  auto_export: true
  keep_history: true
  history_limit: 100

ui:
  theme: "default"
  language: "zh_CN"
  date_format: "YYYY-MM-DD"
  time_format: "24h"

quotas:
  max_storage_gb: 50
  trash_retention_days: 30
```

---

## 文档版本历史

| 版本 | 日期 | 作者 | 变更说明 |
|------|------|------|----------|
| 1.0.0 | 2026-04-30 | Claude Code | 初始版本，完整收纳大师计划 |

---

**本文档由 Claude Code 生成，遵循收纳大师哲学设计理念。**
