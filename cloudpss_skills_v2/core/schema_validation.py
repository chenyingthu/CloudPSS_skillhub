"""Schema 验证工具模块

提供用于验证 config_schema 和 get_default_config 一致性的工具函数。
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


def get_schema_defaults(schema: dict, path: str = "") -> Dict[str, Any]:
    """从 JSON Schema 中提取所有 default 值。

    Args:
        schema: JSON Schema 字典
        path: 当前路径（用于递归）

    Returns:
        路径到 default 值的映射字典
    """
    defaults: Dict[str, Any] = {}

    if not isinstance(schema, dict):
        return defaults

    # 当前路径的 default
    if "default" in schema:
        defaults[path] = schema["default"]

    # 递归处理 properties
    if "properties" in schema and isinstance(schema["properties"], dict):
        for key, value in schema["properties"].items():
            new_path = f"{path}.{key}" if path else key
            defaults.update(get_schema_defaults(value, new_path))

    # 处理 items (数组)
    if "items" in schema and isinstance(schema["items"], dict):
        # 提取数组项的默认值（用于与config中的数组项对比）
        item_defaults = get_schema_defaults(schema["items"], f"{path}[]")
        defaults.update(item_defaults)
        # 也保留整个数组的默认值
        if "default" in schema["items"]:
            defaults[f"{path}[]"] = schema["items"]["default"]

    return defaults


def get_config_defaults(config: dict, path: str = "") -> Dict[str, Any]:
    """从配置字典中提取所有值。

    Args:
        config: 配置字典
        path: 当前路径（用于递归）

    Returns:
        路径到值的映射字典
    """
    defaults: Dict[str, Any] = {}

    if not isinstance(config, dict):
        return defaults

    for key, value in config.items():
        new_path = f"{path}.{key}" if path else key

        if isinstance(value, dict):
            # 如果字典为空，记录路径；否则递归处理子键
            if not value:
                defaults[new_path] = value
            defaults.update(get_config_defaults(value, new_path))
        else:
            defaults[new_path] = value

    return defaults


def compare_defaults(
    schema_defaults: Dict[str, Any], config_defaults: Dict[str, Any]
) -> List[Tuple[str, Any, Any]]:
    """比较两组默认值，返回不一致的字段。

    Args:
        schema_defaults: 从 schema 提取的默认值
        config_defaults: 从 config 提取的默认值

    Returns:
        不一致项列表，每项为 (path, schema_value, config_value)
        config_value 可能是 "MISSING_IN_CONFIG" 或实际值
        schema_value 可能是 "MISSING_IN_SCHEMA" 或实际值
    """
    inconsistencies: List[Tuple[str, Any, Any]] = []

    # 检查 schema 中有 default 但 config 中没有的字段
    for path, schema_value in schema_defaults.items():
        if path not in config_defaults:
            inconsistencies.append((path, schema_value, "MISSING_IN_CONFIG"))
        elif config_defaults[path] != schema_value:
            inconsistencies.append((path, schema_value, config_defaults[path]))

    # 检查 config 中有但 schema 中没有 default 的字段
    for path, config_value in config_defaults.items():
        if path not in schema_defaults:
            inconsistencies.append((path, "MISSING_IN_SCHEMA", config_value))

    return inconsistencies
