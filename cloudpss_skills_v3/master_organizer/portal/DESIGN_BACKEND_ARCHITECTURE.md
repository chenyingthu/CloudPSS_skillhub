# Portal 后端架构设计

**版本**: 1.0.0  
**日期**: 2026-05-03

---

## 1. 架构目标

### 1.1 设计原则

- **单一职责**: 每个模块只负责一个功能领域
- **高内聚低耦合**: 模块内部紧密相关，模块之间松散耦合
- **可测试性**: 每个模块可独立测试
- **可扩展性**: 易于添加新功能

### 1.2 当前问题

```
当前 state.py (664行):
├── 工作区管理 (workspace_summary, organizer_snapshot)
├── Case 管理 (case_detail, create_case, update_case)
├── Task 管理 (task_preflight, create_task, run_task)
├── Result 管理 (result_detail, result_summary)
├── 模型编辑 (save_model_table_edits)
└── 审计日志 (audit_entries)
```

**问题**:
- 单文件职责过多
- 代码行数超标（目标 < 200 行/文件）
- 难以维护和测试

---

## 2. 新架构设计

### 2.1 目录结构

```
portal/
├── __init__.py              # 导出
├── server.py                # HTTP 服务器 (保持精简)
├── middleware/
│   ├── __init__.py
│   ├── auth.py              # 认证中间件
│   ├── cors.py              # CORS 中间件
│   └── error.py             # 错误处理中间件
├── handlers/                # 业务处理器
│   ├── __init__.py
│   ├── base.py              # 基础处理器类
│   ├── workspace.py         # 工作区管理
│   ├── cases.py             # Case CRUD
│   ├── tasks.py             # Task CRUD + 执行
│   ├── results.py           # Result CRUD + 分析
│   ├── models.py            # 模型编辑
│   ├── servers.py           # 服务器管理
│   └── audit.py             # 审计日志
├── services/                # 业务服务层
│   ├── __init__.py
│   ├── case_service.py      # Case 业务逻辑
│   ├── task_service.py      # Task 业务逻辑
│   ├── result_service.py    # Result 业务逻辑
│   └── model_service.py     # 模型业务逻辑
├── schemas/                 # 数据验证
│   ├── __init__.py
│   ├── case.py              # Case DTO
│   ├── task.py              # Task DTO
│   ├── result.py            # Result DTO
│   └── common.py            # 通用 DTO
├── utils/                   # 工具函数
│   ├── __init__.py
│   ├── csv.py               # CSV 处理
│   ├── json.py              # JSON 处理
│   └── response.py          # 响应工具
├── static/                  # 前端静态文件
│   ├── index.html
│   ├── app.js
│   └── styles.css
└── tests/                   # 测试
    ├── __init__.py
    ├── conftest.py
    ├── test_handlers/
    ├── test_services/
    └── test_e2e/
```

### 2.2 模块职责

| 模块 | 职责 | 目标行数 |
|------|------|----------|
| server.py | HTTP 路由分发 | < 100 |
| handlers/* | 请求处理，参数验证 | < 150/文件 |
| services/* | 业务逻辑 | < 200/文件 |
| schemas/* | 数据验证和序列化 | < 100/文件 |
| utils/* | 工具函数 | < 100/文件 |

---

## 3. 核心模块设计

### 3.1 Base Handler

```python
# handlers/base.py
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from http.server import BaseHTTPRequestHandler

T = TypeVar('T')


class BaseHandler(ABC, Generic[T]):
    """基础处理器类"""
    
    def __init__(self, request: BaseHTTPRequestHandler):
        self.request = request
    
    @abstractmethod
    def get(self, entity_id: str) -> T:
        """获取单个资源"""
        pass
    
    @abstractmethod
    def list(self, **filters) -> list[T]:
        """获取资源列表"""
        pass
    
    @abstractmethod
    def create(self, data: dict) -> T:
        """创建资源"""
        pass
    
    @abstractmethod
    def update(self, entity_id: str, data: dict) -> T:
        """更新资源"""
        pass
    
    @abstractmethod
    def delete(self, entity_id: str) -> None:
        """删除资源"""
        pass


class ResponseHelper:
    """响应辅助类"""
    
    @staticmethod
    def success(data: dict, status: int = 200):
        return {"data": data, "error": None}, status
    
    @staticmethod
    def error(code: str, message: str, status: int = 400, details: dict = None):
        return {
            "error": {"code": code, "message": message, "details": details or {}}
        }, status
    
    @staticmethod
    def paginated(items: list, total: int, limit: int, offset: int):
        return {
            "data": items,
            "pagination": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "has_more": offset + len(items) < total
            }
        }
```

### 3.2 Case Handler

```python
# handlers/cases.py
from typing import List
from .base import BaseHandler, ResponseHelper
from ..services.case_service import CaseService
from ..schemas.case import CaseCreate, CaseUpdate, CaseResponse


class CaseHandler(BaseHandler[CaseResponse]):
    """Case 处理器"""
    
    def __init__(self, request):
        super().__init__(request)
        self.service = CaseService()
    
    def get(self, entity_id: str) -> CaseResponse:
        """GET /cases/{id}"""
        case = self.service.get(entity_id)
        if not case:
            return ResponseHelper.error(
                "RESOURCE_NOT_FOUND", 
                f"Case {entity_id} not found",
                404
            )
        return ResponseHelper.success(CaseResponse.from_model(case))
    
    def list(self, status: str = None, tag: str = None, 
             limit: int = 50, offset: int = 0) -> List[CaseResponse]:
        """GET /cases"""
        cases, total = self.service.list(
            status=status, tag=tag, limit=limit, offset=offset
        )
        return ResponseHelper.paginated(
            [CaseResponse.from_model(c) for c in cases],
            total, limit, offset
        )
    
    def create(self, data: dict) -> CaseResponse:
        """POST /cases"""
        try:
            validated = CaseCreate(**data)
            case = self.service.create(validated.dict())
            return ResponseHelper.success(
                CaseResponse.from_model(case), 
                201
            )
        except ValueError as e:
            return ResponseHelper.error(
                "VALIDATION_ERROR",
                str(e),
                422
            )
    
    def update(self, entity_id: str, data: dict) -> CaseResponse:
        """PUT /cases/{id}"""
        try:
            validated = CaseUpdate(**data)
            case = self.service.update(entity_id, validated.dict(exclude_unset=True))
            if not case:
                return ResponseHelper.error(
                    "RESOURCE_NOT_FOUND",
                    f"Case {entity_id} not found",
                    404
                )
            return ResponseHelper.success(CaseResponse.from_model(case))
        except ValueError as e:
            return ResponseHelper.error(
                "VALIDATION_ERROR",
                str(e),
                422
            )
    
    def delete(self, entity_id: str) -> None:
        """DELETE /cases/{id}"""
        success = self.service.delete(entity_id)
        if not success:
            return ResponseHelper.error(
                "RESOURCE_NOT_FOUND",
                f"Case {entity_id} not found",
                404
            )
        return ResponseHelper.success({}, 204)
```

### 3.3 Case Service

```python
# services/case_service.py
from typing import Optional, List, Tuple
from cloudpss_skills_v3.master_organizer.core import (
    Case, CaseRegistry, get_path_manager
)


class CaseService:
    """Case 业务服务"""
    
    def __init__(self):
        self.registry = CaseRegistry()
    
    def get(self, case_id: str) -> Optional[Case]:
        """获取单个 Case"""
        return self.registry.get(case_id)
    
    def list(self, status: str = None, tag: str = None,
             limit: int = 50, offset: int = 0) -> Tuple[List[Case], int]:
        """获取 Case 列表"""
        items = list(self.registry.list())
        
        # 过滤
        if status:
            items = [(k, v) for k, v in items if v.get('status') == status]
        if tag:
            items = [(k, v) for k, v in items if tag in v.get('tags', [])]
        
        total = len(items)
        
        # 分页
        paginated = items[offset:offset + limit]
        
        return [v for _, v in paginated], total
    
    def create(self, data: dict) -> Case:
        """创建 Case"""
        # 业务逻辑：验证 RID 格式
        rid = data.get('rid', '')
        if not rid.startswith('model/') or len(rid.split('/')) < 3:
            raise ValueError("CloudPSS RID 格式不正确，应类似 model/chenying/IEEE39")
        
        return self.registry.create(data)
    
    def update(self, case_id: str, data: dict) -> Optional[Case]:
        """更新 Case"""
        existing = self.registry.get(case_id)
        if not existing:
            return None
        
        return self.registry.update(case_id, data)
    
    def delete(self, case_id: str) -> bool:
        """删除 Case"""
        existing = self.registry.get(case_id)
        if not existing:
            return False
        
        self.registry.delete(case_id)
        return True
```

### 3.4 Case Schema

```python
# schemas/case.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class CaseCreate:
    """创建 Case 请求"""
    name: str
    rid: str
    model_source: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    description: str = ""
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("name is required")
        if not self.rid:
            raise ValueError("rid is required")


@dataclass
class CaseUpdate:
    """更新 Case 请求"""
    name: Optional[str] = None
    model_source: Optional[str] = None
    tags: Optional[List[str]] = None
    description: Optional[str] = None
    status: Optional[str] = None


@dataclass
class CaseResponse:
    """Case 响应"""
    id: str
    name: str
    rid: str
    model_source: Optional[str]
    description: str
    server_id: str
    status: str
    tags: List[str]
    task_count: int
    last_task_id: Optional[str]
    created_at: str
    updated_at: str
    
    @classmethod
    def from_model(cls, model: 'Case') -> 'CaseResponse':
        return cls(
            id=model.id,
            name=model.name,
            rid=model.rid,
            model_source=getattr(model, 'model_source', None),
            description=model.description,
            server_id=model.server_id,
            status=model.status,
            tags=model.tags,
            task_count=getattr(model, 'task_count', 0),
            last_task_id=getattr(model, 'last_task_id', None),
            created_at=model.created_at,
            updated_at=model.updated_at
        )
```

---

## 4. Server 重构

### 4.1 精简 server.py

```python
# server.py
"""Zero-dependency local web server for the master organizer portal."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import secrets
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from .handlers.workspace import WorkspaceHandler
from .handlers.cases import CaseHandler
from .handlers.tasks import TaskHandler
from .handlers.results import ResultHandler
from .handlers.servers import ServerHandler
from .handlers.audit import AuditHandler


STATIC_DIR = Path(__file__).resolve().parent / "static"
PORTAL_TOKEN_ENV = "CLOUDPSS_PORTAL_TOKEN"


class PortalHandler(BaseHTTPRequestHandler):
    """Portal HTTP 处理器"""
    
    server_version = "CloudPSSOrganizerPortal/1.0"
    
    # 路由表
    ROUTES = {
        # Workspace
        ("GET", "/api/v1/workspace/snapshot"): (WorkspaceHandler, "snapshot"),
        ("GET", "/api/v1/workspace/health"): (WorkspaceHandler, "health"),
        
        # Cases
        ("GET", "/api/v1/cases"): (CaseHandler, "list"),
        ("POST", "/api/v1/cases"): (CaseHandler, "create"),
        ("GET", "/api/v1/cases/{id}"): (CaseHandler, "get"),
        ("PUT", "/api/v1/cases/{id}"): (CaseHandler, "update"),
        ("DELETE", "/api/v1/cases/{id}"): (CaseHandler, "delete"),
        
        # Tasks
        ("GET", "/api/v1/tasks"): (TaskHandler, "list"),
        ("POST", "/api/v1/tasks"): (TaskHandler, "create"),
        ("GET", "/api/v1/tasks/{id}"): (TaskHandler, "get"),
        ("POST", "/api/v1/tasks/{id}/run"): (TaskHandler, "run"),
        ("GET", "/api/v1/tasks/{id}/logs"): (TaskHandler, "logs"),
        
        # Results
        ("GET", "/api/v1/results"): (ResultHandler, "list"),
        ("GET", "/api/v1/results/{id}"): (ResultHandler, "get"),
        ("POST", "/api/v1/results/{id}/report"): (ResultHandler, "report"),
        ("POST", "/api/v1/results/{id}/archive"): (ResultHandler, "archive"),
        
        # Servers
        ("GET", "/api/v1/servers"): (ServerHandler, "list"),
        
        # Audit
        ("GET", "/api/v1/audit"): (AuditHandler, "list"),
    }
    
    def do_GET(self):
        self._handle("GET")
    
    def do_POST(self):
        self._handle("POST")
    
    def do_PUT(self):
        self._handle("PUT")
    
    def do_DELETE(self):
        self._handle("DELETE")
    
    def _handle(self, method: str):
        """处理请求"""
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        
        # 认证检查
        if not self._authorized(query):
            self._json({"error": {"code": "AUTHENTICATION_ERROR", "message": "Unauthorized"}}, 401)
            return
        
        # 路由匹配
        handler_class, action = self._match_route(method, path)
        if not handler_class:
            self._static(path)
            return
        
        # 执行处理
        try:
            handler = handler_class(self)
            result, status = getattr(handler, action)(**query)
            self._json(result, status)
        except Exception as e:
            self._json({"error": {"code": "INTERNAL_ERROR", "message": str(e)}}, 500)
    
    def _match_route(self, method: str, path: str) -> tuple:
        """匹配路由"""
        # 精确匹配
        key = (method, path)
        if key in self.ROUTES:
            return self.ROUTES[key]
        
        # 参数匹配 (如 /cases/{id})
        for (m, pattern), handler in self.ROUTES.items():
            if m != method:
                continue
            if "{id}" in pattern:
                prefix = pattern.split("{id}")[0]
                if path.startswith(prefix):
                    return handler
        
        return None, None
    
    def _authorized(self, query: dict) -> bool:
        """认证检查"""
        token = os.environ.get(PORTAL_TOKEN_ENV, "")
        if not token:
            return True
        provided = self.headers.get("X-Portal-Token", "") or query.get("token", [""])[0]
        return secrets.compare_digest(provided, token)
    
    def _json(self, data: dict, status: int = 200):
        """发送 JSON 响应"""
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    
    def _static(self, path: str):
        """服务静态文件"""
        relative = "index.html" if path in ("", "/") else path.lstrip("/")
        file_path = (STATIC_DIR / relative).resolve()
        
        if not str(file_path).startswith(str(STATIC_DIR.resolve())) or not file_path.is_file():
            file_path = STATIC_DIR / "index.html"
        
        content = file_path.read_bytes()
        content_type = self._guess_type(file_path.suffix)
        
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)
    
    def _guess_type(self, suffix: str) -> str:
        """猜测 MIME 类型"""
        types = {
            ".html": "text/html",
            ".js": "application/javascript",
            ".css": "text/css",
            ".json": "application/json",
            ".png": "image/png",
        }
        return types.get(suffix, "application/octet-stream")
```

---

## 5. 迁移计划

### 5.1 Phase 1: 创建新结构 (Week 1)

```bash
# 1. 创建目录结构
mkdir -p handlers services schemas utils middleware tests/{handlers,services,e2e}

# 2. 实现基础类
# - handlers/base.py
# - schemas/common.py
# - utils/response.py

# 3. 迁移第一个模块: Workspace
# - services/workspace_service.py
# - handlers/workspace.py
# - 更新 server.py 路由
```

### 5.2 Phase 2: 迁移核心模块 (Week 2)

```bash
# 迁移顺序：
1. Cases (最完整，作为模板)
2. Results (相对独立)
3. Audit (简单)
4. Servers (简单)
5. Tasks (最复杂，依赖 execute_task)
6. Models (依赖 model_editor)
```

### 5.3 Phase 3: 清理旧代码 (Week 3)

```bash
# 1. 验证所有功能正常
pytest tests/ -v

# 2. 删除旧文件
# - state.py (迁移完成后删除)

# 3. 更新导入
# - __init__.py
# - 测试文件
```

---

## 6. 验收标准

| 指标 | 当前 | 目标 | 验证方式 |
|------|------|------|----------|
| state.py 行数 | 664 | 0 (删除) | wc -l |
| 最大单文件行数 | 664 | < 200 | wc -l |
| 模块数量 | 3 | > 10 | ls |
| 测试覆盖率 | 未知 | > 80% | pytest --cov |
| API 文档 | 缺失 | 完整 | OpenAPI |
