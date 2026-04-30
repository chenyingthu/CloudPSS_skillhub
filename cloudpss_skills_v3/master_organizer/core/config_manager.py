"""
配置管理器 - 收纳大师计划核心组件

管理 ~/.cloudpss/config/ 下的所有配置文件。
支持 YAML/JSON 格式，提供统一的读写接口。
"""

import json
import yaml
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Union


@dataclass
class UserPreferences:
    """用户偏好设置"""
    default_format: str = "json"
    auto_export: bool = True
    keep_history: bool = True
    history_limit: int = 100
    theme: str = "default"
    language: str = "zh_CN"
    date_format: str = "YYYY-MM-DD"
    time_format: str = "24h"


@dataclass
class StorageQuotas:
    """存储配额设置"""
    max_storage_gb: int = 50
    max_cases: int = 1000
    max_tasks_per_case: int = 100
    max_results_per_task: int = 10
    trash_retention_days: int = 30


@dataclass
class UserConfig:
    """用户配置"""
    api_version: str = "v1.0"
    user: dict = field(default_factory=lambda: {
        "name": "",
        "email": ""
    })
    preferences: UserPreferences = field(default_factory=UserPreferences)
    quotas: StorageQuotas = field(default_factory=StorageQuotas)
    metadata: dict = field(default_factory=lambda: {
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "version": "1.0.0"
    })


class ConfigManager:
    """
    配置管理器

    统一管理所有配置文件，确保配置的一致性、可验证性和可回滚。
    """

    # 配置文件名
    CONFIG_FILES = {
        "user": "user.yaml",
        "servers": "servers.yaml",
        "defaults": "defaults.yaml",
    }

    def __init__(self, config_dir: Optional[Path] = None):
        """
        初始化配置管理器

        Args:
            config_dir: 配置目录路径，默认从 PathManager 获取
        """
        if config_dir:
            self._config_dir = Path(config_dir)
        else:
            from .path_manager import get_path_manager
            self._config_dir = get_path_manager().config_dir

        self._ensure_config_dir()
        self._cache: dict[str, Any] = {}

    def _ensure_config_dir(self):
        """确保配置目录存在"""
        self._config_dir.mkdir(parents=True, exist_ok=True)

    def _get_config_path(self, name: str) -> Path:
        """获取配置文件路径"""
        filename = self.CONFIG_FILES.get(name, f"{name}.yaml")
        return self._config_dir / filename

    def _load_yaml(self, path: Path) -> Optional[dict]:
        """加载 YAML 文件"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return None
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML file {path}: {e}")

    def _save_yaml(self, path: Path, data: dict):
        """保存 YAML 文件"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    def load(self, name: str) -> Optional[dict]:
        """
        加载配置文件

        Args:
            name: 配置名称

        Returns:
            配置字典，如果不存在则返回 None
        """
        if name in self._cache:
            return self._cache[name]

        path = self._get_config_path(name)
        data = self._load_yaml(path)
        if data:
            self._cache[name] = data
        return data

    def save(self, name: str, data: dict):
        """
        保存配置文件

        Args:
            name: 配置名称
            data: 配置数据
        """
        path = self._get_config_path(name)
        self._save_yaml(path, data)
        self._cache[name] = data

    def get_user_config(self) -> UserConfig:
        """
        获取用户配置

        Returns:
            UserConfig 实例
        """
        data = self.load("user")
        if not data:
            config = UserConfig()
            self.save_user_config(config)
            return config

        # 从字典构建 UserConfig
        try:
            preferences = UserPreferences(**data.get("preferences", {}))
            quotas = StorageQuotas(**data.get("quotas", {}))
            return UserConfig(
                api_version=data.get("api_version", "v1.0"),
                user=data.get("user", {}),
                preferences=preferences,
                quotas=quotas,
                metadata=data.get("metadata", {})
            )
        except Exception as e:
            # 如果解析失败，返回默认配置
            return UserConfig()

    def save_user_config(self, config: UserConfig):
        """
        保存用户配置

        Args:
            config: UserConfig 实例
        """
        data = {
            "api_version": config.api_version,
            "user": config.user,
            "preferences": asdict(config.preferences),
            "quotas": asdict(config.quotas),
            "metadata": {
                "created_at": config.metadata.get("created_at", datetime.now().isoformat()),
                "updated_at": datetime.now().isoformat(),
                "version": config.metadata.get("version", "1.0.0")
            }
        }
        self.save("user", data)

    def get_default_config(self) -> dict:
        """获取默认配置"""
        return self.load("defaults") or {}

    def set_default_config(self, defaults: dict):
        """设置默认配置"""
        self.save("defaults", defaults)

    def update(self, name: str, updates: dict, merge: bool = True):
        """
        更新配置

        Args:
            name: 配置名称
            updates: 更新内容
            merge: 是否合并（True）还是替换（False）
        """
        if merge:
            current = self.load(name) or {}
            current.update(updates)
            self.save(name, current)
        else:
            self.save(name, updates)

    def invalidate_cache(self, name: Optional[str] = None):
        """
        使缓存失效

        Args:
            name: 特定配置名称，如果为 None 则清除所有缓存
        """
        if name:
            self._cache.pop(name, None)
        else:
            self._cache.clear()

    def exists(self, name: str) -> bool:
        """
        检查配置文件是否存在

        Args:
            name: 配置名称

        Returns:
            文件是否存在
        """
        path = self._get_config_path(name)
        return path.exists()

    def delete(self, name: str) -> bool:
        """
        删除配置文件

        Args:
            name: 配置名称

        Returns:
            是否成功删除
        """
        path = self._get_config_path(name)
        if path.exists():
            path.unlink()
            self._cache.pop(name, None)
            return True
        return False

    def list_configs(self) -> list[str]:
        """
        列出所有配置文件

        Returns:
            配置名称列表
        """
        configs = []
        for filename in self._config_dir.glob("*.yaml"):
            configs.append(filename.stem)
        return sorted(configs)


# 全局配置管理器实例
_config_manager: Optional[ConfigManager] = None


def get_config_manager(config_dir: Optional[Path] = None) -> ConfigManager:
    """
    获取全局配置管理器实例

    Args:
        config_dir: 可选的配置目录路径

    Returns:
        ConfigManager 实例
    """
    global _config_manager
    if _config_manager is None or config_dir:
        _config_manager = ConfigManager(config_dir)
    return _config_manager
