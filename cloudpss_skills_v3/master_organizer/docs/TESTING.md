# Testing Guide

## Overview

The Master Organizer uses a multi-layer testing strategy:
- **Unit Tests**: Fast, isolated tests with mocked dependencies
- **Integration Tests**: HTTP layer tests with real file I/O
- **E2E Tests**: Browser automation with Playwright
- **Performance Tests**: Benchmarks for optimizations

## Test Organization

```
tests/
├── conftest.py              # Shared fixtures
├── test_*.py               # Unit/integration tests
├── test_performance.py     # Performance benchmarks
└── e2e/
    └── test_portal.py      # Playwright E2E tests
```

## Running Tests

### All Tests
```bash
pytest cloudpss_skills_v3/master_organizer/tests/ -v
```

### Unit Tests Only
```bash
pytest cloudpss_skills_v3/master_organizer/tests/ -v -m "not integration and not e2e and not benchmark"
```

### Integration Tests
```bash
pytest cloudpss_skills_v3/master_organizer/tests/ -v -m integration
```

### E2E Tests
```bash
pytest cloudpss_skills_v3/master_organizer/tests/e2e/ -v --browser chromium
```

### Performance Tests
```bash
pytest cloudpss_skills_v3/master_organizer/tests/test_performance.py -v
```

## Test Markers

| Marker | Description | Example |
|--------|-------------|---------|
| `integration` | Tests with file I/O | Registry tests |
| `e2e` | Browser automation | Portal UI tests |
| `benchmark` | Performance tests | CSV streaming |
| `slow` | Long-running tests | Large file processing |

## Writing Tests

### Unit Test Example
```python
def test_case_handler_create(tmp_path, monkeypatch):
    """Test case creation."""
    monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
    get_path_manager(str(tmp_path))

    # Setup default server
    server_id = IDGenerator.generate(EntityType.SERVER)
    ServerRegistry().create(server_id, Server(...))

    # Create case
    handler = CaseHandler()
    result, status = handler.create({
        "name": "Test Case",
        "rid": "model/test/case",
    })

    assert status == 201
    assert result["data"]["name"] == "Test Case"
```

### Integration Test Example
```python
@pytest.mark.integration
def test_api_case_lifecycle(tmp_path, monkeypatch, portal_server):
    """Test full case lifecycle via HTTP API."""
    base_url = portal_server

    # Create case
    resp = requests.post(f"{base_url}/api/cases", json={
        "name": "API Test",
        "rid": "model/test/api",
    })
    assert resp.status_code == 201
    case_id = resp.json()["data"]["id"]

    # Get case
    resp = requests.get(f"{base_url}/api/cases/{case_id}")
    assert resp.status_code == 200
```

### E2E Test Example
```python
@pytest.mark.e2e
def test_portal_create_case(page: Page, portal_url: str):
    """Test creating a case through UI."""
    page.goto(f"{portal_url}?token=test")

    # Click new case button
    page.click("[data-testid='new-case-btn']")

    # Fill form
    page.fill("[name='name']", "E2E Test Case")
    page.fill("[name='rid']", "model/test/e2e")

    # Submit
    page.click("[type='submit']")

    # Verify success
    expect(page.locator("[data-testid='success-toast']")).to_be_visible()
```

### Performance Test Example
```python
class TestCSVStreamingPerformance:
    """Benchmark CSV streaming performance."""

    def test_large_csv_preview_performance(self, tmp_path):
        """Test preview on large CSV files."""
        csv_path = tmp_path / "large.csv"

        # Create 10k row CSV
        with BufferedCSVWriter(csv_path) as writer:
            writer.write_row(["time", "value"])
            for i in range(10000):
                writer.write_row([str(i * 0.001), str(i)])

        # Benchmark
        start = time.perf_counter()
        reader = StreamingCSVReader(csv_path)
        preview = reader.preview(limit=12)
        elapsed = time.perf_counter() - start

        assert elapsed < 1.0  # Should complete in under 1 second
```

## Fixtures

### Common Fixtures
```python
# conftest.py

@pytest.fixture
def tmp_cloudpss_home(tmp_path, monkeypatch):
    """Create temporary CLOUDPSS_HOME."""
    monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
    return get_path_manager(str(tmp_path))

@pytest.fixture
def default_server(tmp_cloudpss_home):
    """Create default server for tests."""
    server_id = IDGenerator.generate(EntityType.SERVER)
    ServerRegistry().create(server_id, Server(
        id=server_id,
        name="test-server",
        url="http://test.com/",
        owner="tester",
        auth=build_auth_metadata("token", {"token_source": "test"}),
        default=True,
    ))
    return server_id

@pytest.fixture(scope="session")
def portal_server(tmp_path_factory):
    """Start portal server for integration tests."""
    tmp = tmp_path_factory.mktemp("portal")
    env = os.environ.copy()
    env["CLOUDPSS_HOME"] = str(tmp)
    env["CLOUDPSS_PORTAL_TOKEN"] = "test-token"

    proc = subprocess.Popen(
        [sys.executable, "-m", "cloudpss_skills_v3.master_organizer.portal",
         "--port", "0", "--token", "test-token"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # Wait for server to start...
    yield "http://localhost:PORT"
    proc.terminate()
```

## Coverage

### Run with Coverage
```bash
pytest cloudpss_skills_v3/master_organizer/tests/ \
  --cov=cloudpss_skills_v3.master_organizer \
  --cov-report=html \
  --cov-report=term-missing
```

### Coverage Configuration
```ini
# pyproject.toml
[tool.coverage.run]
source = ["cloudpss_skills_v3"]
omit = ["*/tests/*", "*/test_*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

## Debugging Tests

### Verbose Output
```bash
pytest -vvv --tb=long cloudpss_skills_v3/master_organizer/tests/test_specific.py
```

### Stop on First Failure
```bash
pytest -x cloudpss_skills_v3/master_organizer/tests/
```

### Run Specific Test
```bash
pytest cloudpss_skills_v3/master_organizer/tests/test_handlers.py::TestCaseHandler::test_create -v
```

### Debug with PDB
```bash
pytest --pdb cloudpss_skills_v3/master_organizer/tests/test_failing.py
```

## Best Practices

1. **Use tmp_path for file operations**: Ensures test isolation
2. **Mock external services**: Don't call CloudPSS API in unit tests
3. **Test edge cases**: Empty inputs, large inputs, invalid data
4. **Keep tests fast**: Unit tests should complete in milliseconds
5. **Name tests descriptively**: `test_case_creation_with_invalid_rid_raises_error`
6. **Use fixtures for common setup**: Reduces duplication
7. **Assert specific error messages**: Ensures correct error handling
