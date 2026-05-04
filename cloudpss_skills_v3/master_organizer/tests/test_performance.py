"""Performance benchmarks for Portal optimizations.

Usage:
    pytest tests/test_performance.py -v --benchmark-only
"""

import pytest
import time
from pathlib import Path
from unittest.mock import patch

from cloudpss_skills_v3.master_organizer.core import (
    CaseRegistry,
    ServerRegistry,
    Server,
    Case,
    IDGenerator,
    EntityType,
    get_path_manager,
)
from cloudpss_skills_v3.master_organizer.core.server_auth import build_auth_metadata
from cloudpss_skills_v3.master_organizer.core.csv_streaming import StreamingCSVReader, BufferedCSVWriter
from cloudpss_skills_v3.master_organizer.core.cache import LRUCache
from cloudpss_skills_v3.master_organizer.portal.handlers import CaseHandler, ResultHandler


class TestCSVStreamingPerformance:
    """Benchmark CSV streaming performance."""

    def test_large_csv_preview_performance(self, tmp_path):
        """Test preview performance on large CSV files."""
        # Create large CSV file
        csv_path = tmp_path / "large.csv"
        row_count = 10000

        with BufferedCSVWriter(csv_path) as writer:
            writer.write_row(["time", "value", "channel"])
            for i in range(row_count):
                writer.write_row([str(i * 0.001), str(i * 0.1), "bus1"])

        # Benchmark streaming reader
        reader = StreamingCSVReader(csv_path)

        start = time.perf_counter()
        preview = reader.preview(limit=12)
        elapsed = time.perf_counter() - start

        assert preview.total_lines == row_count + 1  # +1 for header
        assert len(preview.rows) == 12
        assert elapsed < 1.0  # Should complete in under 1 second

    def test_time_series_extraction_performance(self, tmp_path):
        """Benchmark time series extraction."""
        csv_path = tmp_path / "timeseries.csv"
        row_count = 50000

        with BufferedCSVWriter(csv_path) as writer:
            writer.write_row(["time", "value", "channel"])
            for i in range(row_count):
                writer.write_row([str(i * 0.001), str(i * 0.1), "bus1"])

        reader = StreamingCSVReader(csv_path)

        start = time.perf_counter()
        data = reader.extract_time_series(x_column="time", y_column="value", limit=240)
        elapsed = time.perf_counter() - start

        assert data.total_points == row_count
        assert len(data.points) == 240
        assert elapsed < 2.0  # Should complete in under 2 seconds


class TestCachePerformance:
    """Benchmark caching performance."""

    def test_cache_hit_performance(self):
        """Test cache hit is fast."""
        cache = LRUCache(maxsize=1000, ttl=60)

        # Populate cache
        for i in range(1000):
            cache.set(f"key_{i}", {"data": i})

        # Benchmark cache hits
        start = time.perf_counter()
        for i in range(1000):
            cache.get(f"key_{i}")
        elapsed = time.perf_counter() - start

        assert elapsed < 0.01  # 1000 hits should be under 10ms
        assert cache.info()["hits"] == 1000

    def test_cache_vs_direct_call(self):
        """Compare cached vs direct function call."""
        call_count = 0

        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            time.sleep(0.001)  # Simulate 1ms work
            return x * 2

        cache = LRUCache(maxsize=100)

        # First call (cache miss)
        start = time.perf_counter()
        result1 = expensive_function(5)
        elapsed1 = time.perf_counter() - start

        # Cache the result
        cache.set("key_5", result1)

        # Second call (cache hit)
        start = time.perf_counter()
        result2 = cache.get("key_5")
        elapsed2 = time.perf_counter() - start

        assert result1 == result2 == 10
        assert elapsed2 < elapsed1 / 10  # Cache hit should be 10x faster


class TestPaginationPerformance:
    """Benchmark pagination performance."""

    def test_large_dataset_pagination(self, tmp_path, monkeypatch):
        """Test pagination with large dataset."""
        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        # Setup server
        server_id = IDGenerator.generate(EntityType.SERVER)
        ServerRegistry().create(
            server_id,
            Server(
                id=server_id,
                name="test-server",
                url="http://test.com/",
                owner="tester",
                auth=build_auth_metadata("token", {"token_source": "test"}),
                default=True,
            ),
        )

        # Create many cases
        handler = CaseHandler()
        for i in range(500):
            handler.create({
                "name": f"Case {i}",
                "rid": f"model/test/case{i}",
            })

        # Benchmark pagination
        start = time.perf_counter()
        result, status = handler.list(limit=50, offset=0)
        elapsed = time.perf_counter() - start

        assert status == 200
        assert len(result["data"]["items"]) == 50
        assert result["data"]["pagination"]["total"] == 500
        assert elapsed < 0.5  # Should complete in under 500ms

    def test_pagination_offset_performance(self, tmp_path, monkeypatch):
        """Test pagination with large offset."""
        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        # Setup server
        server_id = IDGenerator.generate(EntityType.SERVER)
        ServerRegistry().create(
            server_id,
            Server(
                id=server_id,
                name="test-server",
                url="http://test.com/",
                owner="tester",
                auth=build_auth_metadata("token", {"token_source": "test"}),
                default=True,
            ),
        )

        # Create cases
        handler = CaseHandler()
        for i in range(200):
            handler.create({
                "name": f"Case {i}",
                "rid": f"model/test/case{i}",
            })

        # Benchmark pagination with large offset
        start = time.perf_counter()
        result, status = handler.list(limit=10, offset=150)
        elapsed = time.perf_counter() - start

        assert status == 200
        assert len(result["data"]["items"]) == 10
        assert elapsed < 0.3


class TestMemoryUsage:
    """Test memory efficiency."""

    def test_csv_streaming_memory_efficient(self, tmp_path):
        """Test CSV streaming doesn't load entire file into memory."""
        import psutil
        import os

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Create large CSV
        csv_path = tmp_path / "memory_test.csv"
        with BufferedCSVWriter(csv_path) as writer:
            writer.write_row(["col1", "col2", "col3"])
            for i in range(100000):
                writer.write_row([str(i), str(i * 2), str(i * 3)])

        # Stream read
        reader = StreamingCSVReader(csv_path)
        preview = reader.preview(limit=10)

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Memory increase should be minimal (< 50MB for preview)
        assert memory_increase < 50 * 1024 * 1024
        assert preview.total_lines == 100001


class TestCacheStats:
    """Test cache statistics."""

    def test_cache_hit_rate(self):
        """Test cache hit rate tracking."""
        cache = LRUCache(maxsize=100, ttl=60)

        # Populate cache
        for i in range(100):
            cache.set(f"key_{i}", i)

        # 50 hits, 50 misses
        for i in range(50):
            cache.get(f"key_{i}")  # hit
        for i in range(100, 150):
            cache.get(f"key_{i}")  # miss

        info = cache.info()
        assert info["hits"] == 50
        assert info["misses"] == 50
        assert info["hit_rate"] == 0.5

    def test_cache_cleanup(self):
        """Test cache cleanup of expired entries."""
        cache = LRUCache(maxsize=100, ttl=0.1)  # 100ms TTL

        # Add entries
        for i in range(50):
            cache.set(f"key_{i}", i)

        # Wait for expiration
        time.sleep(0.2)

        # Cleanup should remove expired entries
        removed = cache.cleanup_expired()
        assert removed == 50
        assert len(cache.keys()) == 0


@pytest.mark.benchmark
class TestBenchmarkSummary:
    """Summary benchmark of all optimizations."""

    def test_full_workflow_performance(self, tmp_path, monkeypatch):
        """Benchmark complete workflow performance."""
        monkeypatch.setenv("CLOUDPSS_HOME", str(tmp_path))
        get_path_manager(str(tmp_path))

        start = time.perf_counter()

        # Setup
        server_id = IDGenerator.generate(EntityType.SERVER)
        ServerRegistry().create(
            server_id,
            Server(
                id=server_id,
                name="test-server",
                url="http://test.com/",
                owner="tester",
                auth=build_auth_metadata("token", {"token_source": "test"}),
                default=True,
            ),
        )

        # Create case
        case_handler = CaseHandler()
        result, _ = case_handler.create({
            "name": "Performance Test Case",
            "rid": "model/test/case",
        })
        case_id = result["data"]["id"]

        # List cases (paginated)
        case_handler.list(limit=10)

        elapsed = time.perf_counter() - start

        # Full workflow should complete in under 1 second
        assert elapsed < 1.0
