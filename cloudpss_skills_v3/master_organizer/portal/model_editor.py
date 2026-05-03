"""Table-oriented local CloudPSS model editor helpers."""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


MODEL_CELL_PATH = ("revision", "implements", "diagram", "cells")


def load_model_document(path: str | Path) -> tuple[Path, dict[str, Any]]:
    model_path = Path(path).expanduser().resolve()
    if not model_path.exists():
        raise ValueError(f"模型文件不存在: {model_path}")
    if model_path.suffix.lower() not in {".yaml", ".yml", ".json"}:
        raise ValueError("当前 Portal 仅支持 YAML/JSON 本地模型文件编辑")
    text = model_path.read_text(encoding="utf-8")
    data = json.loads(text) if model_path.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError("模型文件不是对象结构")
    return model_path, data


def _get_path(data: dict[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = data
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _cells(data: dict[str, Any]) -> dict[str, Any]:
    cells = _get_path(data, MODEL_CELL_PATH)
    return cells if isinstance(cells, dict) else {}


def _definition_group(definition: str) -> str:
    name = definition.rsplit("/", 1)[-1] if definition else "unknown"
    lowered = name.lower()
    if "bus" in lowered:
        return "Bus"
    if "transmissionline" in lowered or "line" in lowered:
        return "Line"
    if "transformer" in lowered:
        return "Transformer"
    if "load" in lowered:
        return "Load"
    if "generator" in lowered or "syncgen" in lowered:
        return "Generator"
    if "channel" in lowered or "meter" in lowered:
        return "Measurement"
    if "gov" in lowered or "tur" in lowered or "pss" in lowered or "exc" in lowered:
        return "Control"
    return name or "Other"


def _scalar(value: Any) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def _arg_columns(rows: list[dict[str, Any]], max_columns: int = 18) -> list[str]:
    counts: dict[str, int] = {}
    for row in rows:
        for key, value in row.get("args", {}).items():
            if _scalar(value):
                counts[key] = counts.get(key, 0) + 1
    return [key for key, _count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:max_columns]]


def model_summary(path: str | Path) -> dict[str, Any]:
    model_path, data = load_model_document(path)
    cells = _cells(data)
    components = []
    groups: dict[str, int] = {}
    for cell_id, cell in cells.items():
        if not isinstance(cell, dict) or not cell.get("definition"):
            continue
        definition = str(cell.get("definition", ""))
        group = _definition_group(definition)
        args = cell.get("args") if isinstance(cell.get("args"), dict) else {}
        row = {
            "id": str(cell.get("id") or cell_id),
            "cell_key": str(cell_id),
            "label": str(cell.get("label") or cell.get("name") or cell_id),
            "definition": definition,
            "group": group,
            "canvas": cell.get("canvas", ""),
            "args": args,
        }
        components.append(row)
        groups[group] = groups.get(group, 0) + 1

    grouped: dict[str, dict[str, Any]] = {}
    for group in sorted(groups):
        rows = [row for row in components if row["group"] == group]
        grouped[group] = {
            "name": group,
            "count": len(rows),
            "columns": _arg_columns(rows),
            "rows": rows,
        }

    return {
        "path": str(model_path),
        "name": data.get("name", model_path.stem),
        "description": data.get("description", ""),
        "component_count": len(components),
        "groups": grouped,
        "jobs": data.get("jobs", []),
        "configs": data.get("configs", []),
        "editable": True,
    }


def save_model_edits(path: str | Path, updates: list[dict[str, Any]]) -> dict[str, Any]:
    model_path, data = load_model_document(path)
    cells = _cells(data)
    if not cells:
        raise ValueError("模型文件中未找到 revision.implements.diagram.cells")

    backup_path = model_path.with_suffix(model_path.suffix + f".bak-{datetime.now().strftime('%Y%m%d%H%M%S%f')}")
    shutil.copy2(model_path, backup_path)

    changed = 0
    for update in updates:
        cell_id = str(update.get("cell_key") or update.get("id") or "").strip()
        arg_key = str(update.get("arg") or "").strip()
        if not cell_id or not arg_key:
            continue
        cell = cells.get(cell_id)
        if not isinstance(cell, dict):
            continue
        args = cell.setdefault("args", {})
        if not isinstance(args, dict):
            continue
        old_value = args.get(arg_key)
        new_value = update.get("value")
        if old_value != new_value:
            args[arg_key] = new_value
            changed += 1

    if model_path.suffix.lower() == ".json":
        model_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        model_path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")

    return {"path": str(model_path), "backup_path": str(backup_path), "changed": changed}
