# CloudPSS Skills V3 API 参考文档

## 概述

CloudPSS Skills V3 提供两套 API 接口：

1. **MCP Server API** - 通过 Model Context Protocol 提供的 Tools 接口
2. **Portal REST API** - Observation Portal 提供的 HTTP REST 接口

---

## MCP Server API

### 工具列表 (Tools)

#### 1. powerflow_run - 运行潮流计算

运行电力系统潮流计算，分析稳态运行点。

**参数：**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| case_name | string | 是 | 案例名称，如 "IEEE39-基态工况" |
| model_rid | string | 是 | CloudPSS 模型 RID，如 "model/chenying/IEEE39" |
| wait | boolean | 否 | 是否等待计算完成（默认 true） |

**示例：**
```json
{
  "case_name": "IEEE39-测试",
  "model_rid": "model/chenying/IEEE39",
  "wait": true
}
```

**返回：**
```json
{
  "task_id": "task-pf-xxx",
  "status": "completed",
  "message": "潮流计算完成",
  "result": {
    "voltage_min": 0.98,
    "voltage_max": 1.05,
    "bus_count": 39,
    "branch_count": 46
  }
}
```

---

#### 2. emt_run - 运行暂态仿真

运行电磁暂态仿真（EMT），分析系统动态响应。

**参数：**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| case_name | string | 是 | 案例名称 |
| model_rid | string | 是 | 模型 RID |
| duration | number | 否 | 仿真时长（秒，默认 10） |
| fault_config | object | 否 | 故障配置 |
| wait | boolean | 否 | 是否等待完成（默认 true） |

**fault_config 结构：**
```json
{
  "bus": "BUS16",
  "type": "three_phase",
  "start_time": 1.0,
  "clear_time": 1.1
}
```

---

#### 3. result_query - 查询任务状态

查询仿真任务的状态和结果。

**参数：**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_id | string | 是 | 任务 ID |
| include_data | boolean | 否 | 是否包含完整结果数据 |

**返回状态：**
- `pending` - 等待中
- `running` - 运行中
- `completed` - 已完成
- `failed` - 失败
- `cancelled` - 已取消

---

#### 4. result_analyze - 智能分析结果

对仿真结果进行智能分析，生成专业解读报告。

**参数：**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_id | string | 是 | 任务 ID |
| focus | string | 否 | 分析维度：voltage/stability/losses/general |

**分析维度：**
- `voltage` - 电压质量分析
- `stability` - 稳定性分析
- `losses` - 网损分析
- `general` - 综合分析（默认）

---

#### 5. result_export - 导出结果

导出仿真结果为指定格式。

**参数：**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_id | string | 是 | 任务 ID |
| format | string | 否 | 格式：csv/json/md（默认 csv） |
| output_path | string | 否 | 输出路径 |

---

#### 6. case_compare - 案例对比

对比多个算例的结果差异。

**参数：**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| case_ids | array | 是 | 案例 ID 列表（至少 2 个） |
| metrics | array | 否 | 对比指标列表 |

---

#### 7. parameter_sweep - 参数扫描

批量运行多组参数，进行敏感性分析。

**参数：**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| base_case | string | 是 | 基准案例名称或 ID |
| parameter | string | 是 | 扫描参数名 |
| range | array | 是 | 参数值列表 |
| parallel | boolean | 否 | 是否并行执行（默认 true） |

---

#### 8. model_search - 模型搜索

在 CloudPSS 模型库中搜索模型。

**参数：**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| keywords | string | 是 | 搜索关键词 |
| filter | object | 否 | 过滤条件 |

---

#### 9. model_analysis - 模型分析

分析模型特性，提供参数建议。

**参数：**

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| model_rid | string | 是 | 模型 RID |
| analysis_type | string | 否 | 分析类型：general/powerflow/emt |

---

## Portal REST API

### 基础信息

- **Base URL:** `http://localhost:8765`
- **Content-Type:** `application/json`
- **认证:** Token (可选，通过 Header 或 Query 参数)

### 认证

**Header 方式：**
```
X-Portal-Token: your-token-here
```

**Query 参数方式：**
```
?token=your-token-here
```

---

### API 端点

#### GET /api/snapshot

获取工作区完整快照。

**返回：**
```json
{
  "workspace": {
    "root": "/path/to/workspace",
    "counts": {
      "servers": 2,
      "cases": 5,
      "tasks": 10,
      "results": 8
    },
    "storage": {
      "total_mb": 156
    }
  },
  "cases": [...],
  "tasks": [...],
  "results": [...],
  "servers": [...]
}
```

---

#### GET /api/health

检查服务健康状态。

**返回：**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "3.0.0"
}
```

---

#### GET /api/cases

列出所有 Case。

**Query 参数：**
- `status` - 按状态过滤
- `tag` - 按标签过滤
- `limit` - 返回数量限制（默认 50）
- `offset` - 分页偏移量

**返回：**
```json
{
  "data": [
    {
      "id": "case-001",
      "name": "IEEE 39 Bus",
      "status": "active",
      "rid": "model/demo/IEEE39",
      "tags": ["ieee39", "powerflow"]
    }
  ],
  "total": 10
}
```

---

#### POST /api/cases

创建新 Case。

**请求体：**
```json
{
  "name": "My Case",
  "rid": "model/chenying/IEEE39",
  "description": "案例描述",
  "tags": ["tag1", "tag2"]
}
```

---

#### GET /api/cases/{id}

获取 Case 详情。

---

#### POST /api/cases/{id}

更新 Case。

---

#### GET /api/tasks

列出所有任务。

**Query 参数：**
- `case_id` - 按 Case 过滤
- `status` - 按状态过滤
- `limit` - 返回数量限制
- `offset` - 分页偏移量

---

#### POST /api/tasks

创建新任务。

**请求体：**
```json
{
  "case_id": "case-001",
  "name": "潮流计算任务",
  "type": "powerflow",
  "config": {
    "channels": ["voltage", "power"]
  }
}
```

---

#### GET /api/tasks/{id}

获取任务详情。

---

#### POST /api/tasks/{id}

更新任务配置。

---

#### POST /api/tasks/{id}/run

运行任务。

---

#### GET /api/tasks/{id}/logs

获取任务日志。

---

#### GET /api/results

列出所有结果。

---

#### GET /api/results/{id}

获取结果详情。

---

#### POST /api/results/{id}/report

生成结果报告。

---

#### POST /api/results/{id}/archive

归档结果。

---

#### GET /api/audit

获取审计日志。

---

## 错误处理

### 错误响应格式

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "人类可读的错误描述"
  }
}
```

### 错误代码

| 代码 | 描述 | HTTP 状态码 |
|------|------|-------------|
| UNAUTHORIZED | 未授权 | 401 |
| NOT_FOUND | 资源不存在 | 404 |
| INVALID_REQUEST | 请求参数错误 | 400 |
| INTERNAL_ERROR | 内部服务器错误 | 500 |

---

## 状态码参考

### 任务状态

| 状态 | 描述 |
|------|------|
| created | 已创建 |
| submitted | 已提交 |
| running | 运行中 |
| completed | 已完成 |
| failed | 失败 |
| cancelled | 已取消 |

### 案例状态

| 状态 | 描述 |
|------|------|
| draft | 草稿 |
| active | 活跃 |
| archived | 已归档 |

---

## 使用示例

### Python 示例

```python
import requests

# 获取快照
response = requests.get("http://localhost:8765/api/snapshot")
snapshot = response.json()

# 创建任务
task = {
    "case_id": "case-001",
    "name": "潮流计算",
    "type": "powerflow"
}
response = requests.post("http://localhost:8765/api/tasks", json=task)
```

### curl 示例

```bash
# 获取快照
curl http://localhost:8765/api/snapshot

# 创建任务
curl -X POST http://localhost:8765/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"case_id":"case-001","name":"潮流计算","type":"powerflow"}'
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 3.0.0 | 2024-01 | 初始版本 |
