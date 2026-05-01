"""
路径管理器 - 收纳大师计划核心组件

管理 ~/.cloudpss/ 目录结构，确保所有文件存储在正确位置。
遵循"唯一定位"原则，每个实体都有且只有一个确定位置。
"""

import os
from pathlib import Path
from typing import Optional


class PathManager:
    """
    路径管理器

    负责管理 ~/.cloudpss/ 目录结构的所有路径。
    确保路径一致性、安全性和可预测性。

    支持从以下位置读取自定义路径（优先级从高到低）：
    1. 传入的 root_path 参数
    2. CLOUDPSS_HOME 环境变量
    3. ~/.cloudpss/config/user.yaml 中的 workspace.root
    4. 默认值 ~/.cloudpss
    """

    # 根目录名称
    ROOT_DIR_NAME = ".cloudpss"

    # 子目录定义
    DIRECTORIES = {
        "config": "config",
        "registry": "registry",
        "cases": "cases",
        "tasks": "tasks",
        "results": "results",
        "cache": "cache",
        "logs": "logs",
        "trash": "trash",
    }

    def __init__(self, root_path: Optional[Path] = None):
        """
        初始化路径管理器

        Args:
            root_path: 自定义根目录路径，默认为 ~/.cloudpss
        """
        self._root = self._resolve_root_path(root_path)
        self._ensure_structure()

    def _find_workspace_root(self, start_path: Optional[Path] = None) -> Optional[Path]:
        """
        在当前目录或其父目录中查找 CloudPSS 工作区根目录
        查找策略：
        1. 查找包含 config/user.yaml 且其中有 workspace.root 配置的目录
        2. 查找包含 config/ 和 registry/ 目录结构的目录（init --path 创建的工作区）
        """
        if start_path is None:
            start_path = Path.cwd()

        current = start_path.resolve()

        # 向上遍历目录树
        for path in [current] + list(current.parents):
            # 检查是否有 config/user.yaml 文件
            config_file = path / "config" / "user.yaml"
            if config_file.exists():
                try:
                    import yaml
                    with open(config_file, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        if data and "workspace" in data and "root" in data["workspace"]:
                            configured_root = Path(data["workspace"]["root"]).expanduser().resolve()
                            # 如果配置指向当前目录，这就是工作区
                            if configured_root == path.resolve():
                                return path
                except Exception:
                    pass

            # 检查是否有标准的 .cloudpss 子目录结构
            cloudpss_path = path / self.ROOT_DIR_NAME
            if cloudpss_path.is_dir():
                if (cloudpss_path / "config" / "user.yaml").exists():
                    try:
                        import yaml
                        with open(cloudpss_path / "config" / "user.yaml", 'r', encoding='utf-8') as f:
                            data = yaml.safe_load(f)
                            if data and "workspace" in data and "root" in data["workspace"]:
                                configured_root = Path(data["workspace"]["root"]).expanduser().resolve()
                                if configured_root == cloudpss_path.resolve():
                                    return cloudpss_path
                    except Exception:
                        pass
                # 有 registry 目录也认为是工作区
                if (cloudpss_path / "registry").exists():
                    return cloudpss_path

        return None

    def _resolve_root_path(self, root_path: Optional[Path] = None) -> Path:
        """
        解析根目录路径

        优先级:
        1. 传入的 root_path 参数
        2. CLOUDPSS_HOME 环境变量
        3. 当前目录或其父目录中的 .cloudpss (类似 git 查找 .git)
        4. ~/.cloudpss/config/user.yaml 中的 workspace.root
        5. 默认值 ~/.cloudpss
        """
        # 1. 传入的参数
        if root_path:
            return Path(root_path).expanduser().resolve()

        # 2. 环境变量
        env_path = os.environ.get("CLOUDPSS_HOME")
        if env_path:
            return Path(env_path).expanduser().resolve()

        # 3. 在当前目录或其父目录中查找 .cloudpss 工作区
        workspace_root = self._find_workspace_root()
        if workspace_root:
            return workspace_root

        # 4. 默认位置的配置文件
        default_path = Path.home() / self.ROOT_DIR_NAME
        config_file = default_path / "config" / "user.yaml"
        if config_file.exists():
            try:
                import yaml
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and "workspace" in data:
                        workspace_root = data["workspace"].get("root")
                        if workspace_root:
                            return Path(workspace_root).expanduser().resolve()
            except Exception:
                pass

        # 5. 默认值
        return default_path

    @property
    def root(self) -> Path:
        """根目录路径"""
        return self._root

    @property
    def config_dir(self) -> Path:
        """配置目录"""
        return self._root / self.DIRECTORIES["config"]

    @property
    def registry_dir(self) -> Path:
        """注册表目录"""
        return self._root / self.DIRECTORIES["registry"]

    @property
    def cases_dir(self) -> Path:
        """算例目录"""
        return self._root / self.DIRECTORIES["cases"]

    @property
    def tasks_dir(self) -> Path:
        """任务目录"""
        return self._root / self.DIRECTORIES["tasks"]

    @property
    def results_dir(self) -> Path:
        """结果目录"""
        return self._root / self.DIRECTORIES["results"]

    @property
    def cache_dir(self) -> Path:
        """缓存目录"""
        return self._root / self.DIRECTORIES["cache"]

    @property
    def logs_dir(self) -> Path:
        """日志目录"""
        return self._root / self.DIRECTORIES["logs"]

    @property
    def trash_dir(self) -> Path:
        """回收站目录"""
        return self._root / self.DIRECTORIES["trash"]

    def _ensure_structure(self):
        """确保目录结构存在"""
        # 创建所有必要的目录
        for dir_name in self.DIRECTORIES.values():
            (self._root / dir_name).mkdir(parents=True, exist_ok=True)

        # 设置适当的权限（仅限 Unix 系统）
        if os.name != 'nt':  # 非 Windows
            os.chmod(self._root, 0o700)
            os.chmod(self.config_dir, 0o700)
            os.chmod(self.registry_dir, 0o700)

    def get_case_path(self, case_id: str) -> Path:
        """
        获取算例目录路径

        Args:
            case_id: 算例ID

        Returns:
            算例目录完整路径
        """
        return self.cases_dir / case_id

    def get_task_path(self, task_id: str) -> Path:
        """
        获取任务目录路径

        Args:
            task_id: 任务ID

        Returns:
            任务目录完整路径
        """
        return self.tasks_dir / task_id

    def get_result_path(self, result_id: str) -> Path:
        """
        获取结果目录路径

        Args:
            result_id: 结果ID

        Returns:
            结果目录完整路径
        """
        return self.results_dir / result_id

    def get_variant_path(self, case_id: str, variant_id: str) -> Path:
        """
        获取变体文件路径

        Args:
            case_id: 算例ID
            variant_id: 变体ID

        Returns:
            变体文件完整路径
        """
        return self.get_case_path(case_id) / "variants" / f"{variant_id}.yaml"

    def get_registry_path(self, registry_name: str) -> Path:
        """
        获取注册表文件路径

        Args:
            registry_name: 注册表名称（不含扩展名）

        Returns:
            注册表文件完整路径
        """
        return self.registry_dir / f"{registry_name}.yaml"

    def get_config_path(self, config_name: str) -> Path:
        """
        获取配置文件路径

        Args:
            config_name: 配置文件名称（不含扩展名）

        Returns:
            配置文件完整路径
        """
        return self.config_dir / f"{config_name}.yaml"

    def get_trash_path(self, item_id: str) -> Path:
        """
        获取回收站项目路径

        Args:
            item_id: 项目ID

        Returns:
            回收站中项目的完整路径
        """
        return self.trash_dir / item_id

    def exists(self, entity_id: str) -> bool:
        """
        检查实体是否存在

        Args:
            entity_id: 实体ID

        Returns:
            实体是否存在
        """
        from .id_generator import IDGenerator, EntityType

        entity_type = IDGenerator.get_entity_type(entity_id)
        if not entity_type:
            return False

        if entity_type == EntityType.CASE:
            return self.get_case_path(entity_id).exists()
        elif entity_type == EntityType.TASK:
            return self.get_task_path(entity_id).exists()
        elif entity_type == EntityType.RESULT:
            return self.get_result_path(entity_id).exists()

        return False

    def get_all_cases(self) -> list[Path]:
        """获取所有算例目录"""
        if not self.cases_dir.exists():
            return []
        return [d for d in self.cases_dir.iterdir() if d.is_dir()]

    def get_all_tasks(self) -> list[Path]:
        """获取所有任务目录"""
        if not self.tasks_dir.exists():
            return []
        return [d for d in self.tasks_dir.iterdir() if d.is_dir()]

    def get_all_results(self) -> list[Path]:
        """获取所有结果目录"""
        if not self.results_dir.exists():
            return []
        return [d for d in self.results_dir.iterdir() if d.is_dir()]

    def get_storage_usage(self) -> dict:
        """
        获取存储使用情况

        Returns:
            包含各目录大小的字典
        """
        import shutil

        usage = {}
        total_size = 0

        for dir_name, dir_path in [
            ("config", self.config_dir),
            ("registry", self.registry_dir),
            ("cases", self.cases_dir),
            ("tasks", self.tasks_dir),
            ("results", self.results_dir),
            ("cache", self.cache_dir),
            ("logs", self.logs_dir),
            ("trash", self.trash_dir),
        ]:
            try:
                size = sum(
                    f.stat().st_size
                    for f in dir_path.rglob("*")
                    if f.is_file()
                )
                usage[dir_name] = size
                total_size += size
            except (OSError, IOError):
                usage[dir_name] = 0

        usage["total"] = total_size
        return usage


# 全局路径管理器实例
_path_manager: Optional[PathManager] = None


def get_path_manager(root_path: Optional[Path] = None) -> PathManager:
    """
    获取全局路径管理器实例

    Args:
        root_path: 可选的自定义根目录路径

    Returns:
        PathManager 实例
    """
    global _path_manager
    if _path_manager is None or root_path:
        _path_manager = PathManager(root_path)
    return _path_manager
