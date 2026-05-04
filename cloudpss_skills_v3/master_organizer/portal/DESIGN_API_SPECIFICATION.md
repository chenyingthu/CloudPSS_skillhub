# Portal API 设计规范

**版本**: 1.0.0  
**日期**: 2026-05-03  
**状态**: 设计阶段

---

## 1. API 架构设计

### 1.1 RESTful 设计原则

- **资源导向**: URL 表示资源，而非操作
- **HTTP 方法语义化**: GET/POST/PUT/DELETE 表示 CRUD
- **状态码规范**: 使用标准 HTTP 状态码
- **版本控制**: URL 中包含版本号 `/api/v1/`
- **JSON 格式**: 请求/响应统一使用 JSON

### 1.2 基础 URL

```
http://{host}:{port}/api/v1/
```

### 1.3 认证方式

```http
GET /api/v1/cases HTTP/1.1
Host: localhost:8765
X-Portal-Token: {token}
Content-Type: application/json
```

---

## 2. 端点规范

### 2.1 Workspace 工作区

#### GET /workspace/snapshot
获取工作区完整快照

**响应**:
```json
{
  "workspace": {
    "root": "~/.cloudpss",
    "servers": 2,
    "cases": 5,
    "tasks": 12,
    "results": 10,
    "storage_mb": 150.5
  },
  "recent_tasks": [...],
  "recent_results": [...]
}
```

#### GET /workspace/health
健康检查

**响应**:
```json
{
  "status": "healthy",
  "checks": {
    "registry": "ok",
    "storage": "ok",
    "quotas": "ok"
  }
}
```

---

### 2.2 Cases 算例

#### GET /cases
获取 Case 列表

**查询参数**:
- `status`: 过滤状态 (draft/active/archived)
- `tag`: 标签过滤
- `limit`: 返回数量限制 (默认 50)
- `offset`: 分页偏移

**响应**:
```json
{
  "items": [
    {
      "id": "case_20260503_120000_a1b2c3d4",
      "name": "IEEE39",
      "rid": "model/chenying/IEEE39",
      "status": "active",
      "tags": ["ieee39", "powerflow"],
      "task_count": 5,
      "created_at": "2026-05-03T12:00:00Z"
    }
  ],
  "total": 10,
  "limit": 50,
  "offset": 0
}
```

#### POST /cases
创建新 Case

**请求体**:
```json
{
  "name": "IEEE39",
  "rid": "model/chenying/IEEE39",
  "model_source": "examples/basic/ieee39.yaml",
  "tags": ["ieee39", "powerflow"],
  "description": "IEEE 39节点系统"
}
```

**响应 (201)**:
```json
{
  "id": "case_20260503_120000_a1b2c3d4",
  "name": "IEEE39",
  "rid": "model/chenying/IEEE39",
  "status": "draft",
  "created_at": "2026-05-03T12:00:00Z"
}
```

#### GET /cases/{id}
获取 Case 详情

**响应**:
```json
{
  "id": "case_20260503_120000_a1b2c3d4",
  "name": "IEEE39",
  "rid": "model/chenying/IEEE39",
  "model_source": "examples/basic/ieee39.yaml",
  "status": "active",
  "tags": ["ieee39", "powerflow"],
  "description": "IEEE 39节点系统",
  "server_id": "server_abc123",
  "task_count": 5,
  "last_task_id": "task_20260503_130000_e5f6g7h8",
  "created_at": "2026-05-03T12:00:00Z",
  "updated_at": "2026-05-03T12:30:00Z"
}
```

#### PUT /cases/{id}
更新 Case

**请求体**:
```json
{
  "name": "IEEE39 Updated",
  "tags": ["ieee39", "powerflow", "emt"],
  "description": "Updated description"
}
```

#### DELETE /cases/{id}
删除 Case

**响应 (204)**: No Content

---

### 2.3 Tasks 任务

#### GET /tasks
获取 Task 列表

**查询参数**:
- `case_id`: 关联 Case
- `status`: 状态过滤
- `type`: 类型过滤 (powerflow/emt/stability)

**响应**:
```json
{
  "items": [
    {
      "id": "task_20260503_130000_e5f6g7h8",
      "name": "base-pf",
      "case_id": "case_20260503_120000_a1b2c3d4",
      "type": "powerflow",
      "status": "completed",
      "result_id": "result_20260503_130500_i9j0k1l2",
      "created_at": "2026-05-03T13:00:00Z"
    }
  ]
}
```

#### POST /tasks
创建 Task

**请求体**:
```json
{
  "name": "base-pf",
  "case_id": "case_20260503_120000_a1b2c3d4",
  "type": "powerflow",
  "config": {
    "max_iter": 20,
    "tolerance": 1e-6,
    "flat_start": true
  }
}
```

#### POST /tasks/{id}/run
运行 Task

**请求体**:
```json
{
  "timeout": 300
}
```

**响应**:
```json
{
  "task_id": "task_20260503_130000_e5f6g7h8",
  "job_id": "job_cloudpss_12345",
  "status": "running",
  "started_at": "2026-05-03T13:00:00Z"
}
```

#### GET /tasks/{id}/logs
获取 Task 日志

**响应**:
```json
{
  "task_id": "task_20260503_130000_e5f6g7h8",
  "logs": [
    {"timestamp": "2026-05-03T13:00:01Z", "level": "INFO", "message": "Task started"},
    {"timestamp": "2026-05-03T13:00:05Z", "level": "INFO", "message": "Job submitted"}
  ]
}
```

---

### 2.4 Results 结果

#### GET /results
获取 Result 列表

**查询参数**:
- `case_id`: 关联 Case
- `task_id`: 关联 Task

#### GET /results/{id}
获取 Result 详情

**响应**:
```json
{
  "id": "result_20260503_130500_i9j0k1l2",
  "task_id": "task_20260503_130000_e5f6g7h8",
  "case_id": "case_20260503_120000_a1b2c3d4",
  "format": "json",
  "created_at": "2026-05-03T13:05:00Z",
  "size_bytes": 1024000,
  "files": ["manifest.json", "buses.csv", "branches.csv"],
  "metadata": {
    "job_id": "job_cloudpss_12345",
    "duration_seconds": 45,
    "converged": true
  }
}
```

#### POST /results/{id}/report
生成报告

**响应**:
```json
{
  "report_url": "/api/v1/results/result_20260503_130500_i9j0k1l2/report.md",
  "format": "markdown"
}
```

#### POST /results/{id}/archive
归档结果

**响应**:
```json
{
  "archive_url": "/api/v1/results/result_20260503_130500_i9j0k1l2/archive.tar.gz",
  "size_bytes": 512000
}
```

---

### 2.5 Models 模型

#### GET /cases/{id}/model
获取 Case 模型编辑器数据

**响应**:
```json
{
  "case_id": "case_20260503_120000_a1b2c3d4",
  "components": {
    "buses": 39,
    "lines": 46,
    "generators": 10,
    "loads": 19
  },
  "parameters": [...]
}
```

#### POST /models/edits
保存模型编辑

**请求体**:
```json
{
  "case_id": "case_20260503_120000_a1b2c3d4",
  "edits": [
    {
      "component_id": "bus_1",
      "parameter": "voltage",
      "old_value": 1.0,
      "new_value": 1.05
    }
  ]
}
```

---

### 2.6 Servers 服务器

#### GET /servers
获取 Server 列表

**响应**:
```json
{
  "items": [
    {
      "id": "server_abc123",
      "name": "Internal",
      "url": "http://166.111.60.76:50001/",
      "owner": "chenying",
      "status": "active",
      "default": true
    }
  ]
}
```

---

### 2.7 Audit 审计

#### GET /audit
获取审计日志

**查询参数**:
- `limit`: 返回条数 (默认 80)

**响应**:
```json
{
  "entries": [
    {
      "timestamp": "2026-05-03T12:00:00Z",
      "action": "case.create",
      "entity_id": "case_20260503_120000_a1b2c3d4",
      "user": "chenying"
    }
  ]
}
```

---

## 3. 错误处理规范

### 3.1 错误响应格式

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Case not found",
    "details": {
      "case_id": "case_invalid"
    }
  }
}
```

### 3.2 HTTP 状态码

| 状态码 | 场景 |
|--------|------|
| 200 | 成功 GET/PUT |
| 201 | 成功 POST 创建 |
| 204 | 成功 DELETE |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 409 | 资源冲突 |
| 422 | 业务逻辑错误 |
| 500 | 服务器内部错误 |

### 3.3 错误代码表

| 代码 | 描述 |
|------|------|
| INVALID_REQUEST | 请求格式错误 |
| RESOURCE_NOT_FOUND | 资源不存在 |
| RESOURCE_CONFLICT | 资源冲突 |
| VALIDATION_ERROR | 数据验证失败 |
| AUTHENTICATION_ERROR | 认证失败 |
| AUTHORIZATION_ERROR | 授权失败 |
| RATE_LIMIT_EXCEEDED | 频率限制 |
| INTERNAL_ERROR | 内部错误 |

---

## 4. 数据模型

### 4.1 Case

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "rid": "string",
  "model_source": "string",
  "server_id": "string",
  "status": "draft|active|archived",
  "tags": ["string"],
  "task_count": 0,
  "last_task_id": "string",
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

### 4.2 Task

```json
{
  "id": "string",
  "name": "string",
  "case_id": "string",
  "variant_id": "string",
  "type": "powerflow|emt|stability",
  "job_id": "string",
  "server_id": "string",
  "status": "created|submitted|running|completed|failed",
  "result_id": "string",
  "config": {},
  "created_at": "ISO8601",
  "submitted_at": "ISO8601",
  "started_at": "ISO8601",
  "completed_at": "ISO8601"
}
```

### 4.3 Result

```json
{
  "id": "string",
  "name": "string",
  "task_id": "string",
  "case_id": "string",
  "format": "json|csv|hdf5",
  "created_at": "ISO8601",
  "size_bytes": 0,
  "files": ["string"],
  "metadata": {}
}
```

---

## 5. 分页规范

```json
{
  "items": [...],
  "pagination": {
    "total": 100,
    "limit": 20,
    "offset": 0,
    "has_more": true,
    "next_offset": 20
  }
}
```

---

## 6. 版本演进

### v1.0.0 (当前)
- 基础 CRUD 操作
- Task 执行
- Result 分析

### v1.1.0 (计划)
- WebSocket 实时更新
- 批量操作
- 高级查询

### v2.0.0 (未来)
- GraphQL 支持
- 插件系统
- 多租户
