# CloudPSS Master Organizer

A local-first power system simulation management system with web-based Portal interface.

## Features

- **Case Management**: Organize power system models with metadata and tags
- **Task Execution**: Run power flow, EMT, and stability simulations
- **Result Visualization**: View and analyze simulation results with charts
- **Model Editing**: Built-in model editor with parameter modification
- **Zero Dependencies**: Pure Python with no external package dependencies

## Quick Start

### Start the Portal
```bash
python -m cloudpss_skills_v3.master_organizer.portal
```

Access at: http://127.0.0.1:8765

### With Authentication (for remote access)
```bash
python -m cloudpss_skills_v3.master_organizer.portal --token secret --host 0.0.0.0
```

Access at: http://localhost:8765/?token=secret

### Command Line
```bash
# List all cases
python -m cloudpss_skills_v3.master_organizer organizer list-cases

# Create a new case
python -m cloudpss_skills_v3.master_organizer organizer create-case \
  --name "IEEE 39 Bus" \
  --rid model/chenying/IEEE39

# Run power flow
python -m cloudpss_skills_v3.master_organizer organizer run-task \
  --case-id <case-id> \
  --type powerflow
```

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

```
master_organizer/
├── core/                   # Core business logic
│   ├── csv_streaming.py   # Memory-efficient CSV processing
│   ├── cache.py           # LRU cache with TTL
│   ├── path_manager.py    # Path management
│   └── *_registry.py      # Entity registries
├── portal/                # Web interface
│   ├── server.py          # HTTP server
│   ├── handlers/          # API handlers
│   ├── schemas/           # DTOs
│   └── static/            # Web UI assets
└── tests/                 # Test suite
```

## API Documentation

The Portal provides a RESTful API documented in [docs/openapi.yaml](docs/openapi.yaml).

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/cases` | GET/POST | List/create cases |
| `/api/cases/{id}` | GET/POST | Get/update case |
| `/api/tasks` | GET/POST | List/create tasks |
| `/api/tasks/{id}/run` | POST | Execute task |
| `/api/results` | GET | List results |
| `/api/results/{id}` | GET | Get result details |

## Testing

See [docs/TESTING.md](docs/TESTING.md) for detailed testing documentation.

```bash
# Run all tests
pytest cloudpss_skills_v3/master_organizer/tests/ -v

# Run with coverage
pytest --cov=cloudpss_skills_v3.master_organizer --cov-report=html

# Run performance benchmarks
pytest cloudpss_skills_v3/master_organizer/tests/test_performance.py -v
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CLOUDPSS_HOME` | Data directory | `~/.cloudpss` |
| `CLOUDPSS_PORTAL_TOKEN` | API auth token | None |
| `CLOUDPSS_PORTAL_QUIET` | Suppress logs | `0` |

### Data Directory Structure

```
$CLOUDPSS_HOME/
├── servers.json
├── cases/
│   ├── cases.json
│   └── {case_id}/
├── tasks/
│   ├── tasks.json
│   └── {task_id}/
└── results/
    ├── results.json
    └── {result_id}/
```

## Performance Optimizations

### CSV Streaming
Large simulation results are processed using memory-mapped files:
- Preview 10k rows in < 1 second
- Memory usage < 50MB regardless of file size
- Time series extraction with automatic sampling

### Caching
- Model data cached with 5-minute TTL
- Summary data cached with 1-minute TTL
- Cache hit rate tracking and statistics

### Pagination
All list endpoints support efficient pagination:
```python
# GET /api/cases?limit=50&offset=0
{
  "data": {
    "items": [...],
    "pagination": {
      "total": 200,
      "limit": 50,
      "offset": 0,
      "has_more": true
    }
  }
}
```

## Development

### Project Structure
```
cloudpss_skills_v3/master_organizer/
├── __init__.py
├── __main__.py           # CLI entry point
├── cli.py                # Command implementation
├── core/                 # Core modules
│   ├── __init__.py
│   ├── base.py          # Entity base classes
│   ├── case.py          # Case entity
│   ├── csv_streaming.py # CSV utilities
│   ├── cache.py         # Caching
│   └── ...
├── portal/              # Web interface
│   ├── __init__.py
│   ├── server.py        # HTTP server
│   ├── handlers/        # API handlers
│   └── static/          # Web assets
└── tests/               # Tests
    ├── conftest.py
    ├── test_*.py
    └── e2e/
```

### Adding a Feature
1. Define entity in `core/`
2. Create registry in `core/`
3. Add handler in `portal/handlers/`
4. Add routes in `portal/server.py`
5. Write tests

## License

MIT License - see LICENSE file for details.
