"""CSV streaming utilities for large file handling."""

from __future__ import annotations

import csv
import mmap
from pathlib import Path
from typing import Any, Iterator, Optional
from dataclasses import dataclass


@dataclass
class CSVPreview:
    """CSV preview result."""

    headers: list[str]
    rows: list[list[str]]
    total_lines: int
    path: str
    error: Optional[str] = None


@dataclass
class TimeSeriesPoint:
    """Single time series data point."""

    x: float
    y: float


@dataclass
class TimeSeriesData:
    """Time series extraction result."""

    points: list[TimeSeriesPoint]
    path: str
    total_points: int
    error: Optional[str] = None


class StreamingCSVReader:
    """Memory-efficient CSV reader using streaming and mmap."""

    def __init__(self, path: Path, chunk_size: int = 8192):
        """Initialize streaming reader.

        Args:
            path: Path to CSV file
            chunk_size: Size of chunks to read
        """
        self.path = path
        self.chunk_size = chunk_size

    def preview(self, limit: int = 12) -> CSVPreview:
        """Get CSV preview without loading entire file.

        Args:
            limit: Number of rows to preview

        Returns:
            CSVPreview with headers and sample rows
        """
        if not self.path.exists():
            return CSVPreview(
                headers=[], rows=[], total_lines=0, path=str(self.path), error="File not found"
            )

        try:
            headers: list[str] = []
            rows: list[list[str]] = []
            total_lines = 0

            with open(self.path, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)

                # Read headers
                try:
                    headers = next(reader)
                    total_lines = 1
                except StopIteration:
                    return CSVPreview(
                        headers=[], rows=[], total_lines=0, path=str(self.path)
                    )

                # Read preview rows
                for row in reader:
                    total_lines += 1
                    if len(rows) < limit:
                        rows.append(row)

            return CSVPreview(
                headers=headers,
                rows=rows,
                total_lines=total_lines,
                path=str(self.path),
            )

        except Exception as e:
            return CSVPreview(
                headers=[], rows=[], total_lines=0, path=str(self.path), error=str(e)
            )

    def iter_rows(self) -> Iterator[list[str]]:
        """Iterate over CSV rows without loading entire file.

        Yields:
            List of strings for each row
        """
        if not self.path.exists():
            return

        with open(self.path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            yield from reader

    def extract_time_series(
        self,
        x_column: str = "time",
        y_column: str = "value",
        limit: int = 240,
        offset: int = 0,
    ) -> TimeSeriesData:
        """Extract time series data efficiently.

        Args:
            x_column: Name of x-axis column (usually "time")
            y_column: Name of y-axis column
            limit: Maximum number of points to extract
            offset: Number of points to skip

        Returns:
            TimeSeriesData with points
        """
        if not self.path.exists():
            return TimeSeriesData(
                points=[], path=str(self.path), total_points=0, error="File not found"
            )

        points: list[TimeSeriesPoint] = []
        total_points = 0
        x_idx: Optional[int] = None
        y_idx: Optional[int] = None

        try:
            with open(self.path, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)

                # Read header to find column indices
                try:
                    headers = next(reader)
                    headers_lower = [h.lower().strip() for h in headers]

                    # Find column indices (case-insensitive)
                    x_idx = headers_lower.index(x_column.lower()) if x_column.lower() in headers_lower else None
                    y_idx = headers_lower.index(y_column.lower()) if y_column.lower() in headers_lower else None

                    if x_idx is None or y_idx is None:
                        # Try numeric column names if headers not found
                        if headers[0].replace(".", "").replace("-", "").isdigit():
                            # No header, assume first column is time
                            x_idx = 0
                            y_idx = 1 if len(headers) > 1 else 0
                        else:
                            return TimeSeriesData(
                                points=[],
                                path=str(self.path),
                                total_points=0,
                                error=f"Columns not found: {x_column}, {y_column}",
                            )
                except StopIteration:
                    return TimeSeriesData(points=[], path=str(self.path), total_points=0)

                # Read data rows
                for row in reader:
                    total_points += 1

                    if total_points <= offset:
                        continue

                    if len(points) >= limit:
                        # Continue counting but don't store
                        continue

                    try:
                        if x_idx < len(row) and y_idx < len(row):
                            x_val = float(row[x_idx])
                            y_val = float(row[y_idx])
                            points.append(TimeSeriesPoint(x=x_val, y=y_val))
                    except (ValueError, IndexError):
                        continue

            return TimeSeriesData(
                points=points,
                path=str(self.path),
                total_points=total_points,
            )

        except Exception as e:
            return TimeSeriesData(
                points=[], path=str(self.path), total_points=0, error=str(e)
            )

    def count_lines(self) -> int:
        """Count total lines in CSV without loading it.

        Returns:
            Number of lines in file
        """
        if not self.path.exists():
            return 0

        try:
            # Use mmap for fast line counting
            with open(self.path, "rb") as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    return mm.read().count(b"\n")
        except Exception:
            # Fallback to regular reading
            count = 0
            with open(self.path, "r", encoding="utf-8", errors="ignore") as f:
                for _ in f:
                    count += 1
            return count


class BufferedCSVWriter:
    """Buffered CSV writer for efficient large file output."""

    def __init__(self, path: Path, buffer_size: int = 1000):
        """Initialize buffered writer.

        Args:
            path: Output file path
            buffer_size: Number of rows to buffer before writing
        """
        self.path = path
        self.buffer_size = buffer_size
        self._buffer: list[list[str]] = []
        self._writer: Optional[csv.writer] = None
        self._file: Optional[Any] = None
        self._total_written = 0

    def __enter__(self) -> BufferedCSVWriter:
        """Context manager entry."""
        self._file = open(self.path, "w", newline="", encoding="utf-8")
        self._writer = csv.writer(self._file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.flush()
        if self._file:
            self._file.close()

    def write_row(self, row: list[str]) -> None:
        """Write a single row (buffered).

        Args:
            row: Row data to write
        """
        self._buffer.append(row)

        if len(self._buffer) >= self.buffer_size:
            self.flush()

    def write_rows(self, rows: list[list[str]]) -> None:
        """Write multiple rows.

        Args:
            rows: List of rows to write
        """
        for row in rows:
            self.write_row(row)

    def flush(self) -> None:
        """Flush buffered rows to disk."""
        if self._buffer and self._writer:
            self._writer.writerows(self._buffer)
            self._total_written += len(self._buffer)
            self._buffer.clear()

    @property
    def total_written(self) -> int:
        """Get total rows written."""
        return self._total_written + len(self._buffer)


def stream_csv_transform(
    input_path: Path,
    output_path: Path,
    transform_func: callable,
    chunk_size: int = 1000,
) -> dict[str, Any]:
    """Transform CSV file using streaming.

    Args:
        input_path: Input CSV path
        output_path: Output CSV path
        transform_func: Function to transform each row (receives dict, returns dict or None)
        chunk_size: Rows to process before writing

    Returns:
        Statistics about the transformation
    """
    processed = 0
    skipped = 0

    with BufferedCSVWriter(output_path, buffer_size=chunk_size) as writer:
        reader = StreamingCSVReader(input_path)

        # Read headers
        row_iter = reader.iter_rows()
        try:
            headers = next(row_iter)
            writer.write_row(headers)
        except StopIteration:
            return {"processed": 0, "skipped": 0, "output": str(output_path)}

        headers_lower = [h.lower().strip() for h in headers]

        # Process rows
        for row in row_iter:
            row_dict = dict(zip(headers_lower, row))
            result = transform_func(row_dict)

            if result is None:
                skipped += 1
                continue

            # Convert dict back to row
            output_row = [str(result.get(h, "")) for h in headers]
            writer.write_row(output_row)
            processed += 1

    return {
        "processed": processed,
        "skipped": skipped,
        "output": str(output_path),
    }
