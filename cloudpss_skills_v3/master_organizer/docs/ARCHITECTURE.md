# Master Organizer Architecture

## Overview

The Master Organizer is a local-first power system simulation management system with a web-based Portal interface. It follows a layered architecture with clear separation of concerns.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                      Portal Layer                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Web UI    │  │  REST API   │  │   Model Editor      │  │
│  │  (static/)  │  │  (server)   │  │  (model_editor.py)  │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                    Handler Layer                             │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │  Case   │ │  Task   │ │ Result  │ │  Model  │ ...       │
│  │ Handler │ │ Handler │ │ Handler │ │ Handler │           │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘          │
├─────────────────────────────────────────────────────────────┤
│                   Service Layer                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Registry   │  │Task Runner  │  │   Export/Archive    │  │
│  │   (CRUD)    │  │  (async)    │  │    (release_ops)    │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                    Core Layer                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │CSV Streaming│  │    Cache    │  │  Path Management    │  │
│  │ (mmap-based)│  │   (LRU+TTL) │  │    (path_manager)   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                   Storage Layer                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   JSON      │  │    YAML     │  │    File System      │  │
│  │  Registry   │  │   Config    │  │    (CLOUDPSS_HOME)  │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Portal Layer (`portal/`)

#### HTTP Server (`server.py`)
- Built on Python's `http.server` (zero external dependencies)
- ThreadingHTTPServer for concurrent request handling
- Token-based authentication (optional)
- RESTful routing with versioned endpoints

#### Handlers (`portal/handlers/`)
- **CaseHandler**: Case lifecycle management
- **TaskHandler**: Task creation, updates, and execution
- **ResultHandler**: Result retrieval and visualization
- **ModelHandler**: Model editing operations
- **WorkspaceHandler**: Workspace state and health checks
- **AuditHandler**: Audit log access

#### Schemas (`portal/schemas/`)
- Pydantic-style dataclass-based DTOs
- Request/response validation
- Type-safe data transfer

### 2. Core Layer (`core/`)

#### CSV Streaming (`csv_streaming.py`)
Memory-efficient CSV processing using memory-mapped files:
```python
# Streaming read without loading entire file
reader = StreamingCSVReader(path)
preview = reader.preview(limit=12)  # First 12 rows only
data = reader.extract_time_series(x_column="time", y_column="value")
```

Features:
- Memory-mapped file access for large files
- Streaming preview without full load
- Time series extraction with sampling
- Buffered writing for exports

#### Caching (`cache.py`)
LRU cache with TTL support:
```python
# Function result caching
@cached(maxsize=100, ttl=300)
def expensive_operation(x):
    return compute(x)

# Manual cache management
cache = LRUCache(maxsize=1000, ttl=60)
cache.set("key", value)
value = cache.get("key")
```

Features:
- LRU eviction policy
- TTL-based expiration
- Hit rate statistics
- Thread-safe operations

#### Registries (`*_registry.py`)
JSON-based persistence with in-memory indexing:
- **CaseRegistry**: Case CRUD operations
- **TaskRegistry**: Task management
- **ResultRegistry**: Result metadata
- **ServerRegistry**: Server configuration
- **VariantRegistry**: Model variants

All registries inherit from `RegistryBase` with:
- `create()`, `get()`, `update()`, `delete()`
- `list_all()`, `list_paginated()`
- `filter_by()` with multiple criteria

### 3. Storage Layer

#### Directory Structure
```
$CLOUDPSS_HOME/
├── servers.json          # Server registry
├── cases/
│   ├── cases.json        # Case registry
│   └── {case_id}/
│       ├── case.yaml     # Case configuration
│       └── variants/
├── tasks/
│   ├── tasks.json        # Task registry
│   └── {task_id}/
│       ├── task.yaml
│       └── config.json
└── results/
    ├── results.json      # Result registry
    └── {result_id}/
        ├── result.yaml
        ├── tables/
        └── channels.json
```

## Data Flow

### Task Execution Flow
```
1. Client creates task via POST /api/tasks
   ↓
2. CaseHandler validates case exists
   ↓
3. TaskHandler creates task (status: created)
   ↓
4. Client runs task via POST /api/tasks/{id}/run
   ↓
5. TaskRunner executes task asynchronously
   ↓
6. Result is stored in results/{result_id}/
   ↓
7. Result registry is updated
   ↓
8. Client retrieves result via GET /api/results/{id}
```

### Result Visualization Flow
```
1. Client requests result via GET /api/results/{id}
   ↓
2. ResultHandler loads result metadata
   ↓
3. For EMT results:
   - Load channels.json
   - Stream CSV files on-demand
   - Generate preview data
   ↓
4. For PowerFlow results:
   - Load buses.json and branches.json
   - Generate chart data
   ↓
5. Return complete result with summary
```

## Design Patterns

### 1. Handler Pattern
All API endpoints are implemented using handlers:
```python
class CaseHandler(BaseHandler):
    def get(self, case_id: str) -> tuple[dict, int]:
        # Implementation
        return ResponseHelper.success(data), 200
```

### 2. Registry Pattern
CRUD operations abstracted through registries:
```python
registry = CaseRegistry()
registry.create(case_id, case)
registry.update(case_id, updates)
case = registry.get(case_id)
```

### 3. DTO Pattern
Type-safe data transfer with validation:
```python
@dataclass
class CaseCreate:
    name: str
    rid: str
    # Validation in __post_init__
```

### 4. Streaming Pattern
Memory-efficient processing of large files:
```python
with StreamingCSVReader(path) as reader:
    for row in reader.iter_rows():
        process(row)
```

## Performance Optimizations

### 1. Pagination
All list endpoints support pagination:
```python
items, total = registry.list_paginated(
    limit=50,
    offset=0,
    sort_by="created_at"
)
```

### 2. Caching
- Model data cached with 5-minute TTL
- Summary data cached with 1-minute TTL
- Cache hit rate tracked

### 3. Streaming
- CSV files read via memory-mapped I/O
- Preview data limited to 12 rows
- Time series sampled to 240 points

### 4. Lazy Loading
- Result artifacts loaded on-demand
- JSON files parsed only when accessed
- Report generated on first request

## Security Considerations

### 1. Token Authentication
Optional token-based auth for remote access:
```bash
# Set token via environment
export CLOUDPSS_PORTAL_TOKEN=secret

# Or pass to server
python -m cloudpss_skills_v3.master_organizer.portal --token secret
```

### 2. Path Security
All file paths are resolved and validated:
```python
path = (STATIC_DIR / relative).resolve()
if not str(path).startswith(str(STATIC_DIR.resolve())):
    raise SecurityError("Path traversal attempt")
```

### 3. Input Validation
All inputs validated via DTOs:
```python
try:
    data = CaseCreate(**payload)
except ValueError as exc:
    return ResponseHelper.validation_error(str(exc))
```

## Extension Points

### Adding a New Handler
1. Create handler class in `portal/handlers/`
2. Inherit from `BaseHandler`
3. Add routes in `server.py`
4. Register in `portal/handlers/__init__.py`

### Adding a New Registry
1. Create registry in `core/`
2. Inherit from `RegistryBase`
3. Define entity dataclass
4. Add to `core/__init__.py`

### Adding a New Schema
1. Create dataclass in `portal/schemas/`
2. Add validation logic
3. Export from `portal/schemas/__init__.py`

## Testing Strategy

### Unit Tests
- Handler logic isolated from HTTP layer
- Registry operations with temp directories
- Schema validation with edge cases

### Integration Tests
- Full HTTP request/response cycle
- Database (JSON file) persistence
- Authentication flow

### E2E Tests
- Browser automation with Playwright
- User workflow validation
- Cross-browser compatibility

### Performance Tests
- CSV streaming with large files (100k+ rows)
- Cache hit rate validation
- Pagination performance

## Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `CLOUDPSS_HOME` | Data directory | `~/.cloudpss` |
| `CLOUDPSS_PORTAL_TOKEN` | Auth token | None |
| `CLOUDPSS_PORTAL_QUIET` | Suppress logs | `0` |

### Server Options
```bash
python -m cloudpss_skills_v3.master_organizer.portal \
  --host 127.0.0.1 \
  --port 8765 \
  --token secret
```
