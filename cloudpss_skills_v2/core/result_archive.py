"""Result Archive - HDF5-based result storage and retrieval.

Provides high-performance storage for simulation results with:
- Time-series data storage
- Multi-dimensional indexing
- Efficient querying and comparison
- Long-term archival
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator

import h5py
import numpy as np
import pandas as pd

from .system_model import PowerSystemModel


# =============================================================================
# Archive Data Classes
# =============================================================================

@dataclass
class ArchiveMetadata:
    """Metadata for archived results."""

    archive_id: str
    study_id: str
    study_name: str
    project_id: str

    # Timing
    created_at: str
    execution_time_seconds: float | None = None

    # Model information
    model_id: str = ""
    model_fingerprint: str = ""  # For detecting same model

    # Engine information
    engine_type: str = ""
    engine_version: str = ""

    # Study configuration (snapshot)
    study_config: dict[str, Any] = field(default_factory=dict)

    # Tags for organization
    tags: list[str] = field(default_factory=list)

    # Result summary
    summary_metrics: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ArchiveMetadata":
        return cls(**data)


@dataclass
class ArchiveRecord:
    """Complete archive record including metadata and data references."""

    metadata: ArchiveMetadata
    data_paths: dict[str, str] = field(default_factory=dict)
    has_system_model: bool = False
    has_time_series: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "metadata": self.metadata.to_dict(),
            "data_paths": self.data_paths,
            "has_system_model": self.has_system_model,
            "has_time_series": self.has_time_series,
        }


@dataclass
class ComparisonResult:
    """Result of comparing multiple archived results."""

    base_archive_id: str
    compare_archive_ids: list[str]

    # Differences by metric
    metric_differences: dict[str, dict[str, float]] = field(default_factory=dict)

    # Changes detected
    added_buses: list[str] = field(default_factory=list)
    removed_buses: list[str] = field(default_factory=list)
    modified_branches: list[str] = field(default_factory=list)

    # Statistical summary
    voltage_differences: dict[str, Any] = field(default_factory=dict)
    loading_differences: dict[str, Any] = field(default_factory=dict)

    def has_significant_changes(self, threshold: float = 0.01) -> bool:
        """Check if there are significant changes."""
        for metric_diffs in self.metric_differences.values():
            for value in metric_diffs.values():
                if abs(value) > threshold:
                    return True
        return False


# =============================================================================
# Result Archive
# =============================================================================

class ResultArchive:
    """HDF5-based result archive for long-term storage.

    Archive structure:
        archive.h5
        ├── metadata/           # Study metadata
        │   ├── {archive_id}
        │   └── ...
        ├── system_models/      # PowerSystemModel snapshots
        │   ├── {archive_id}/buses
        │   ├── {archive_id}/branches
        │   └── ...
        ├── time_series/        # EMT/stability time series
        │   ├── {archive_id}/time
        │   ├── {archive_id}/bus_001_voltage
        │   └── ...
        └── index/              # Search indexes
            ├── by_date
            ├── by_model
            └── by_tag
    """

    def __init__(
        self,
        archive_path: str | Path = "./results/archive.h5",
        index_path: str | Path | None = None,
    ):
        self.archive_path = Path(archive_path)
        self.index_path = Path(index_path) if index_path else self.archive_path.with_suffix(".index.json")

        # Ensure directory exists
        self.archive_path.parent.mkdir(parents=True, exist_ok=True)

        # In-memory index cache
        self._index: dict[str, ArchiveMetadata] = {}
        self._load_index()

    def _load_index(self) -> None:
        """Load metadata index from disk."""
        if self.index_path.exists():
            with open(self.index_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._index = {
                    k: ArchiveMetadata.from_dict(v) for k, v in data.items()
                }

    def _save_index(self) -> None:
        """Save metadata index to disk."""
        data = {k: v.to_dict() for k, v in self._index.items()}
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

    def _generate_archive_id(
        self, study_id: str, timestamp: datetime | None = None
    ) -> str:
        """Generate unique archive ID."""
        ts = timestamp or datetime.now()
        hash_input = f"{study_id}_{ts.isoformat()}"
        hash_digest = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        return f"{study_id.replace('/', '_')}_{ts.strftime('%Y%m%d_%H%M%S')}_{hash_digest}"

    # -------------------------------------------------------------------------
    # Archive Operations
    # -------------------------------------------------------------------------

    def archive_result(
        self,
        study_id: str,
        study_name: str,
        project_id: str,
        system_model: PowerSystemModel | None,
        summary_metrics: dict[str, float],
        study_config: dict[str, Any],
        tags: list[str] | None = None,
        engine_type: str = "",
        engine_version: str = "",
        execution_time_seconds: float | None = None,
        time_series_data: dict[str, np.ndarray] | None = None,
        time_points: np.ndarray | None = None,
    ) -> str:
        """Archive a simulation result.

        Returns:
            archive_id: Unique identifier for the archived result
        """
        archive_id = self._generate_archive_id(study_id)

        # Create metadata
        metadata = ArchiveMetadata(
            archive_id=archive_id,
            study_id=study_id,
            study_name=study_name,
            project_id=project_id,
            created_at=datetime.now().isoformat(),
            execution_time_seconds=execution_time_seconds,
            model_id=study_config.get("model_id", ""),
            model_fingerprint=self._compute_model_fingerprint(system_model),
            engine_type=engine_type,
            engine_version=engine_version,
            study_config=study_config,
            tags=tags or [],
            summary_metrics=summary_metrics,
        )

        # Write to HDF5
        with h5py.File(self.archive_path, "a") as f:
            # Create archive group
            archive_group = f.create_group(f"archives/{archive_id}")

            # Store metadata as attributes
            meta_group = archive_group.create_group("metadata")
            self._store_dict_as_attrs(meta_group, metadata.to_dict())

            # Store system model
            data_paths = {}
            if system_model:
                model_group = archive_group.create_group("system_model")
                self._store_system_model(model_group, system_model)
                data_paths["system_model"] = f"archives/{archive_id}/system_model"

            # Store time series data
            if time_series_data and time_points is not None:
                ts_group = archive_group.create_group("time_series")
                ts_group.create_dataset("time", data=time_points)
                for name, data in time_series_data.items():
                    ts_group.create_dataset(name, data=data)
                data_paths["time_series"] = f"archives/{archive_id}/time_series"

            # Store summary metrics
            metrics_group = archive_group.create_group("metrics")
            for key, value in summary_metrics.items():
                metrics_group.attrs[key] = value

        # Update index
        self._index[archive_id] = metadata
        self._save_index()

        return archive_id

    def _compute_model_fingerprint(self, model: PowerSystemModel | None) -> str:
        """Compute fingerprint for model identification."""
        if model is None:
            return ""

        # Hash key characteristics
        key_data = f"{len(model.buses)}_{len(model.branches)}_{model.base_mva}"
        for bus in sorted(model.buses, key=lambda b: b.bus_id)[:5]:
            key_data += f"_{bus.bus_id}_{bus.base_kv}"

        return hashlib.md5(key_data.encode()).hexdigest()[:16]

    def _store_system_model(
        self, group: h5py.Group, model: PowerSystemModel
    ) -> None:
        """Store PowerSystemModel in HDF5."""
        # Store buses
        if model.buses:
            bus_data = []
            for bus in model.buses:
                bus_data.append(
                    [
                        bus.bus_id,
                        bus.base_kv,
                        bus.v_magnitude_pu if bus.v_magnitude_pu is not None else np.nan,
                        bus.v_angle_degree if bus.v_angle_degree is not None else np.nan,
                        bus.p_injected_mw if bus.p_injected_mw is not None else np.nan,
                        bus.q_injected_mvar if bus.q_injected_mvar is not None else np.nan,
                    ]
                )
            bus_array = np.array(bus_data)
            ds = group.create_dataset("buses", data=bus_array)
            ds.attrs["columns"] = json.dumps(
                ["bus_id", "base_kv", "v_magnitude_pu", "v_angle_degree", "p_injected_mw", "q_injected_mvar"]
            )
            ds.attrs["bus_names"] = json.dumps([b.name for b in model.buses])
            ds.attrs["bus_types"] = json.dumps([b.bus_type for b in model.buses])

        # Store branches
        if model.branches:
            branch_data = []
            for br in model.branches:
                branch_data.append(
                    [
                        br.from_bus,
                        br.to_bus,
                        br.r_pu,
                        br.x_pu,
                        br.loading_percent if br.loading_percent is not None else np.nan,
                    ]
                )
            branch_array = np.array(branch_data)
            ds = group.create_dataset("branches", data=branch_array)
            ds.attrs["columns"] = json.dumps(
                ["from_bus", "to_bus", "r_pu", "x_pu", "loading_percent"]
            )
            ds.attrs["branch_names"] = json.dumps([b.name for b in model.branches])

        # Store system parameters
        group.attrs["base_mva"] = model.base_mva
        group.attrs["frequency_hz"] = model.frequency_hz
        group.attrs["source_engine"] = model.source_engine

    def _store_dict_as_attrs(self, group: h5py.Group, data: dict) -> None:
        """Store dictionary as HDF5 attributes."""
        for key, value in data.items():
            if isinstance(value, (list, dict)):
                group.attrs[key] = json.dumps(value)
            else:
                try:
                    group.attrs[key] = value
                except (TypeError, ValueError):
                    group.attrs[key] = str(value)

    # -------------------------------------------------------------------------
    # Retrieval Operations
    # -------------------------------------------------------------------------

    def load_result(self, archive_id: str) -> ArchiveRecord:
        """Load an archived result."""
        if archive_id not in self._index:
            raise KeyError(f"Archive '{archive_id}' not found")

        metadata = self._index[archive_id]

        with h5py.File(self.archive_path, "r") as f:
            archive_path = f"archives/{archive_id}"
            if archive_path not in f:
                raise KeyError(f"Archive data '{archive_id}' not found in HDF5")

            archive_group = f[archive_path]

            # Check what data is available
            has_system_model = "system_model" in archive_group
            has_time_series = "time_series" in archive_group

            data_paths = {}
            if has_system_model:
                data_paths["system_model"] = f"{archive_path}/system_model"
            if has_time_series:
                data_paths["time_series"] = f"{archive_path}/time_series"

        return ArchiveRecord(
            metadata=metadata,
            data_paths=data_paths,
            has_system_model=has_system_model,
            has_time_series=has_time_series,
        )

    def load_system_model(self, archive_id: str) -> PowerSystemModel | None:
        """Load system model from archive."""
        with h5py.File(self.archive_path, "r") as f:
            model_path = f"archives/{archive_id}/system_model"
            if model_path not in f:
                return None

            model_group = f[model_path]

            # Load buses
            buses = []
            if "buses" in model_group:
                bus_data = model_group["buses"][:]
                bus_names = json.loads(model_group["buses"].attrs["bus_names"])
                bus_types = json.loads(model_group["buses"].attrs["bus_types"])

                from .system_model import Bus

                for i, row in enumerate(bus_data):
                    buses.append(
                        Bus(
                            bus_id=int(row[0]),
                            name=bus_names[i],
                            base_kv=float(row[1]),
                            bus_type=bus_types[i],
                            v_magnitude_pu=float(row[2]) if not np.isnan(row[2]) else None,
                            v_angle_degree=float(row[3]) if not np.isnan(row[3]) else None,
                            p_injected_mw=float(row[4]) if not np.isnan(row[4]) else None,
                            q_injected_mvar=float(row[5]) if not np.isnan(row[5]) else None,
                        )
                    )

            # Load branches
            branches = []
            if "branches" in model_group:
                branch_data = model_group["branches"][:]
                branch_names = json.loads(model_group["branches"].attrs["branch_names"])

                from .system_model import Branch

                for i, row in enumerate(branch_data):
                    branches.append(
                        Branch(
                            from_bus=int(row[0]),
                            to_bus=int(row[1]),
                            name=branch_names[i],
                            r_pu=float(row[2]),
                            x_pu=float(row[3]),
                            loading_percent=float(row[4]) if not np.isnan(row[4]) else None,
                        )
                    )

            return PowerSystemModel(
                buses=buses,
                branches=branches,
                base_mva=model_group.attrs["base_mva"],
                frequency_hz=model_group.attrs["frequency_hz"],
                source_engine=model_group.attrs.get("source_engine", ""),
            )

    # -------------------------------------------------------------------------
    # Query Operations
    # -------------------------------------------------------------------------

    def query(
        self,
        study_id: str | None = None,
        project_id: str | None = None,
        model_id: str | None = None,
        date_range: tuple[str, str] | None = None,
        tags: list[str] | None = None,
        engine_type: str | None = None,
    ) -> list[str]:
        """Query archives by multiple criteria.

        Returns:
            List of matching archive IDs
        """
        results = []

        for archive_id, metadata in self._index.items():
            # Filter by study
            if study_id and metadata.study_id != study_id:
                continue

            # Filter by project
            if project_id and metadata.project_id != project_id:
                continue

            # Filter by model
            if model_id and metadata.model_id != model_id:
                continue

            # Filter by date range
            if date_range:
                created = metadata.created_at
                if created < date_range[0] or created > date_range[1]:
                    continue

            # Filter by tags (must have all specified tags)
            if tags:
                if not all(tag in metadata.tags for tag in tags):
                    continue

            # Filter by engine
            if engine_type and metadata.engine_type != engine_type:
                continue

            results.append(archive_id)

        return sorted(results, key=lambda x: self._index[x].created_at, reverse=True)

    def get_recent_results(self, n: int = 10) -> list[ArchiveMetadata]:
        """Get n most recent results."""
        sorted_ids = sorted(
            self._index.keys(),
            key=lambda x: self._index[x].created_at,
            reverse=True,
        )
        return [self._index[aid] for aid in sorted_ids[:n]]

    def get_results_by_model(self, model_id: str) -> list[ArchiveMetadata]:
        """Get all results for a specific model."""
        return [
            metadata
            for metadata in self._index.values()
            if metadata.model_id == model_id
        ]

    # -------------------------------------------------------------------------
    # Comparison Operations
    # -------------------------------------------------------------------------

    def compare_results(
        self, base_archive_id: str, compare_archive_ids: list[str]
    ) -> ComparisonResult:
        """Compare multiple results against a base case."""
        base_model = self.load_system_model(base_archive_id)
        base_metadata = self._index[base_archive_id]

        comparison = ComparisonResult(
            base_archive_id=base_archive_id,
            compare_archive_ids=compare_archive_ids,
        )

        for compare_id in compare_archive_ids:
            compare_model = self.load_system_model(compare_id)
            compare_metadata = self._index[compare_id]

            if base_model is None or compare_model is None:
                continue

            # Compare metrics
            metric_diffs = {}
            for key in base_metadata.summary_metrics:
                if key in compare_metadata.summary_metrics:
                    base_val = base_metadata.summary_metrics[key]
                    compare_val = compare_metadata.summary_metrics[key]
                    metric_diffs[key] = compare_val - base_val

            comparison.metric_differences[compare_id] = metric_diffs

            # Compare buses
            base_bus_ids = {b.bus_id: b for b in base_model.buses}
            compare_bus_ids = {b.bus_id: b for b in compare_model.buses}

            comparison.added_buses.extend(
                str(bid) for bid in compare_bus_ids if bid not in base_bus_ids
            )
            comparison.removed_buses.extend(
                str(bid) for bid in base_bus_ids if bid not in compare_bus_ids
            )

            # Compare voltages
            voltage_diffs = []
            for bus_id in base_bus_ids:
                if bus_id in compare_bus_ids:
                    base_v = base_bus_ids[bus_id].v_magnitude_pu
                    compare_v = compare_bus_ids[bus_id].v_magnitude_pu
                    if base_v is not None and compare_v is not None:
                        voltage_diffs.append(compare_v - base_v)

            if voltage_diffs:
                comparison.voltage_differences[compare_id] = {
                    "max": max(voltage_diffs),
                    "min": min(voltage_diffs),
                    "mean": sum(voltage_diffs) / len(voltage_diffs),
                    "std": np.std(voltage_diffs),
                }

        return comparison

    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------

    def list_archives(self) -> list[str]:
        """List all archived result IDs."""
        return list(self._index.keys())

    def get_metadata(self, archive_id: str) -> ArchiveMetadata:
        """Get metadata for an archive."""
        if archive_id not in self._index:
            raise KeyError(f"Archive '{archive_id}' not found")
        return self._index[archive_id]

    def delete_archive(self, archive_id: str) -> bool:
        """Delete an archive."""
        if archive_id not in self._index:
            return False

        # Remove from HDF5
        with h5py.File(self.archive_path, "a") as f:
            archive_path = f"archives/{archive_id}"
            if archive_path in f:
                del f[archive_path]

        # Remove from index
        del self._index[archive_id]
        self._save_index()

        return True

    def export_to_dataframe(self, archive_ids: list[str] | None = None) -> pd.DataFrame:
        """Export archive metadata to DataFrame for analysis."""
        if archive_ids is None:
            archive_ids = list(self._index.keys())

        records = []
        for aid in archive_ids:
            meta = self._index[aid]
            records.append(
                {
                    "archive_id": aid,
                    "study_id": meta.study_id,
                    "study_name": meta.study_name,
                    "project_id": meta.project_id,
                    "created_at": meta.created_at,
                    "model_id": meta.model_id,
                    "engine_type": meta.engine_type,
                    "execution_time": meta.execution_time_seconds,
                    **meta.summary_metrics,
                }
            )

        return pd.DataFrame(records)


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "ArchiveMetadata",
    "ArchiveRecord",
    "ComparisonResult",
    "ResultArchive",
]
