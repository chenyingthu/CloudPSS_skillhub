"""HDF5 export tool for structured simulation results."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Protocol, cast

import h5py
import numpy as np

try:
    import pandas as pd
except ImportError:  # pragma: no cover - pandas is optional at runtime
    pd = None

from cloudpss_skills_v2.core import Artifact, LogEntry, SkillResult, SkillStatus

ALLOWED_OUTPUT_ROOTS = {
    Path("/tmp").resolve(),
    Path("/data").resolve(),
    Path("/results").resolve(),
    (Path.home() / "cloudpss_data").resolve(),
}
DEFAULT_VERSION = "2.0"


class _DataFrameLike(Protocol):
    def to_dict(self, *, orient: str) -> list[dict[str, object]]: ...


class HDF5ExportTool:
    name: str = "hdf5_export"

    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []

    def validate(self, config: object) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not isinstance(config, dict):
            return (False, ["config is required"])

        source = config.get("source")
        if not isinstance(source, dict):
            errors.append("source is required")
        elif "data" not in source:
            errors.append("source.data is required")
        elif not self._is_supported_data(source.get("data")):
            errors.append(
                "source.data must be a dict, list, numpy array, or pandas DataFrame"
            )

        output = config.get("output")
        if not isinstance(output, dict):
            errors.append("output is required")
        elif not output.get("path"):
            errors.append("output.path is required")
        else:
            try:
                self._validate_output_path(output["path"])
            except ValueError as exc:
                errors.append(str(exc))

        return (len(errors) == 0, errors)

    def _validate_output_path(self, output_path: str | Path) -> Path:
        path = Path(output_path).expanduser()
        if not path.is_absolute():
            path = (Path.cwd() / path).resolve(strict=False)
        else:
            path = path.resolve(strict=False)

        allowed_roots = sorted(ALLOWED_OUTPUT_ROOTS)
        if not any(path.is_relative_to(root) for root in allowed_roots):
            allowed_text = ", ".join(str(root) for root in allowed_roots)
            raise ValueError(
                f"output.path '{path}' is outside allowed directories: {allowed_text}"
            )

        if path.suffix.lower() not in {".h5", ".hdf5"}:
            raise ValueError("output.path must end with .h5 or .hdf5")

        return path

    def _is_supported_data(self, value: Any) -> bool:
        if isinstance(value, (dict, list, tuple, np.ndarray)):
            return True
        if pd is not None and isinstance(value, pd.DataFrame):
            return True
        return False

    def _to_python_scalar(self, value: object) -> object:
        if isinstance(value, (np.integer, np.floating, np.bool_)):
            return value.item()
        return value

    def _normalize_attr_value(self, value: object) -> object:
        if value is None:
            return ""
        if isinstance(value, (str, bytes, bool, int, float, np.integer, np.floating, np.bool_)):
            return self._to_python_scalar(value)
        if isinstance(value, (list, tuple, dict)):
            return json.dumps(value, ensure_ascii=False)
        return str(value)

    def _prepare_dataset_data(self, value: object) -> object:
        if pd is not None and isinstance(value, pd.DataFrame):
            return self._dataframe_to_structured_array(value)

        if isinstance(value, np.ndarray):
            return value

        if isinstance(value, tuple):
            value = list(value)

        if isinstance(value, list):
            if not value:
                return np.array([], dtype=float)
            if all(isinstance(item, dict) for item in value):
                return self._records_to_structured_array(value)
            return np.asarray(value)

        return value

    def _dataframe_to_structured_array(self, frame: object) -> np.ndarray:
        assert pd is not None
        typed_frame = cast(_DataFrameLike, frame)
        records = typed_frame.to_dict(orient="records")
        return self._records_to_structured_array(records)

    def _records_to_structured_array(self, records: list[dict[str, object]]) -> np.ndarray:
        if not records:
            return np.array([], dtype=float)

        keys = list(records[0].keys())
        rows: list[tuple[object, ...]] = []
        for record in records:
            rows.append(tuple(self._record_value(record.get(key)) for key in keys))

        dtype: list[tuple[str, object]] = []
        for index, key in enumerate(keys):
            sample = rows[0][index]
            if isinstance(sample, bool):
                dtype.append((key, np.bool_))
            elif isinstance(sample, int) and not isinstance(sample, bool):
                dtype.append((key, np.int64))
            elif isinstance(sample, float):
                dtype.append((key, np.float64))
            else:
                width = max(len(str(row[index])) for row in rows) if rows else 1
                dtype.append((key, f"S{max(1, width)}"))

        structured = np.array(rows, dtype=dtype)
        return structured

    def _record_value(self, value: object) -> object:
        if isinstance(value, (bool, int, float, np.integer, np.floating, np.bool_)):
            return self._to_python_scalar(value)
        if value is None:
            return ""
        return str(value)

    def _export_node(self, parent: h5py.Group, name: str, value: object) -> None:
        if isinstance(value, dict):
            mapping = cast(dict[str, object], value)
            attrs_object = mapping.get("attrs")
            attrs = cast(dict[str, object] | None, attrs_object) if isinstance(attrs_object, dict) else None
            payload = mapping.get("data") if set(mapping.keys()) <= {"data", "attrs"} else None

            if payload is not None:
                dataset = parent.create_dataset(name, data=self._prepare_dataset_data(payload))
                for attr_key, attr_value in (attrs or {}).items():
                    dataset.attrs[attr_key] = self._normalize_attr_value(attr_value)
                return

            group = parent.create_group(name)
            for attr_key, attr_value in (attrs or {}).items():
                group.attrs[attr_key] = self._normalize_attr_value(attr_value)

            for child_name, child_value in mapping.items():
                if child_name == "attrs":
                    continue
                self._export_node(group, child_name, child_value)
            return

        dataset_value = self._prepare_dataset_data(value)
        parent.create_dataset(name, data=dataset_value)

    def _export_to_hdf5(
        self,
        data: object,
        hdf5_path: str | Path,
        metadata: Mapping[str, object] | None,
        compression: object,
        compression_level: object,
    ) -> None:
        del compression
        del compression_level
        path = Path(hdf5_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        root_data = data if isinstance(data, dict) else {"data": data}
        metadata = dict(metadata or {})
        metadata.setdefault("skill_name", self.name)
        metadata.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
        metadata.setdefault("version", DEFAULT_VERSION)

        with h5py.File(path, "w") as handle:
            for key, value in metadata.items():
                handle.attrs[key] = self._normalize_attr_value(value)

            for name, value in root_data.items():
                self._export_node(handle, name, value)

    def _create_index(self, hdf5_path: str | Path) -> Path:
        datasets: list[dict[str, object]] = []
        path = Path(hdf5_path)
        index_path = path.with_suffix(".index.json")

        with h5py.File(path, "r") as handle:
            def collect(name: str, node: h5py.Dataset | h5py.Group) -> None:
                if isinstance(node, h5py.Dataset):
                    datasets.append(
                        {
                            "path": f"/{name}",
                            "shape": list(node.shape),
                            "dtype": str(node.dtype),
                        }
                    )

            handle.visititems(collect)
            index = {
                "file": str(path),
                "datasets": datasets,
                "attrs": {
                    key: self._normalize_attr_value(value)
                    for key, value in handle.attrs.items()
                },
            }

        index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
        return index_path

    @staticmethod
    def _decode_value(value: object) -> object:
        if isinstance(value, bytes):
            return value.decode("utf-8")
        if isinstance(value, np.ndarray):
            if value.dtype.names:
                rows = []
                for row in value:
                    rows.append(
                        {
                            name: HDF5ExportTool._decode_value(row[name])
                            for name in value.dtype.names
                        }
                    )
                return rows
            return value.tolist()
        if isinstance(value, np.generic):
            return value.item()
        return value

    @classmethod
    def _read_node(cls, node: h5py.Group | h5py.Dataset) -> object:
        if isinstance(node, h5py.Dataset):
            return cls._decode_value(node[()])

        result = {
            name: cls._read_node(child)
            for name, child in node.items()
        }
        if node.attrs:
            result["attrs"] = {
                key: cls._decode_value(value) for key, value in node.attrs.items()
            }
        return result

    @classmethod
    def read_hdf5(
        cls, hdf5_path: str | Path, dataset_path: str | None = None
    ) -> object:
        with h5py.File(hdf5_path, "r") as handle:
            if dataset_path:
                dataset = handle[dataset_path]
                if isinstance(dataset, h5py.Dataset):
                    return cls._decode_value(dataset[()])
                return cls._read_node(cast(h5py.Group, dataset))

            result = cast(dict[str, object], cls._read_node(handle))
            result["attrs"] = {
                key: cls._decode_value(value) for key, value in handle.attrs.items()
            }
            return result

    @staticmethod
    def list_datasets(hdf5_path: str | Path) -> list[str]:
        datasets: list[str] = []
        with h5py.File(hdf5_path, "r") as handle:
            def collect(name: str, node: h5py.Dataset | h5py.Group) -> None:
                if isinstance(node, h5py.Dataset):
                    datasets.append(f"/{name}")

            handle.visititems(collect)
        return datasets

    def run(self, config: object) -> SkillResult:
        self.logs = []
        self.artifacts = []
        if config is None:
            config = {}

        valid, errors = self.validate(config)
        if not valid:
            return SkillResult.failure(
                skill_name=self.name,
                error="; ".join(errors),
                data={"stage": "validation", "errors": errors},
            )

        typed_config = cast(dict[str, object], config)
        output = cast(dict[str, object], typed_config["output"])
        source = cast(dict[str, object], typed_config["source"])
        output_path = self._validate_output_path(cast(str | Path, output["path"]))
        metadata = dict(cast(Mapping[str, object] | None, typed_config.get("metadata")) or {})

        try:
            self._export_to_hdf5(
                data=source["data"],
                hdf5_path=output_path,
                metadata=metadata,
                compression=output.get("compression"),
                compression_level=output.get("compression_level"),
            )
            index_path = self._create_index(output_path)
        except Exception as exc:
            return SkillResult.failure(
                skill_name=self.name,
                error=str(exc),
                data={"stage": "export"},
            )

        self.logs.append(
            LogEntry(level="info", message=f"Exported HDF5 file to {output_path}")
        )
        self.artifacts.extend(
            [
                Artifact(
                    name=output_path.name,
                    path=str(output_path),
                    type="hdf5",
                    size_bytes=output_path.stat().st_size,
                    description="Exported HDF5 data file",
                ),
                Artifact(
                    name=index_path.name,
                    path=str(index_path),
                    type="json",
                    size_bytes=index_path.stat().st_size,
                    description="HDF5 dataset index",
                ),
            ]
        )

        return SkillResult.success(
            skill_name=self.name,
            data={
                "output_path": str(output_path),
                "index_path": str(index_path),
                "datasets": self.list_datasets(output_path),
                "metadata": metadata,
            },
            artifacts=self.artifacts,
            logs=self.logs,
            metrics={"file_size_bytes": output_path.stat().st_size},
        )


__all__ = ["HDF5ExportTool"]
