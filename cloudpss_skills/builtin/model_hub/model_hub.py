"""
Model Hub Skill

算例中心 - 多服务器算例管理工具
支持：
- 多服务器/多Token管理
- 本地算例库存储
- RID映射表管理
- 跨服务器算例同步(push/pull/clone)
"""

import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from cloudpss_skills.core import (
    Artifact,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    register,
)

logger = logging.getLogger(__name__)


@register
class ModelHubSkill(SkillBase):
    """算例中心技能 - 多服务器算例统一管理"""

    DEFAULT_HUB_DIR = Path.home() / ".cloudpss-hub"
    DEFAULT_CONFIG_FILE = "config.yaml"
    DEFAULT_REGISTRY_FILE = "registry.yaml"
    DEFAULT_MODELS_DIR = "models"

    @property
    def name(self) -> str:
        return "model_hub"

    @property
    def description(self) -> str:
        return "算例中心 - 多服务器算例统一管理，支持本地存储、RID映射和跨服务器同步"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill"],
            "properties": {
                "skill": {"type": "string", "const": "model_hub"},
                "action": {
                    "type": "string",
                    "enum": [
                        "init",
                        "status",
                        "list_servers",
                        "add_server",
                        "remove_server",
                        "use_server",
                        "list_models",
                        "list_local",
                        "list_remote",
                        "push",
                        "pull",
                        "clone",
                        "sync",
                        "register",
                        "unregister",
                        "info",
                        "export",
                        "import",
                    ],
                    "description": "操作类型",
                },
                "server": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "服务器名称"},
                        "url": {"type": "string", "description": "服务器地址"},
                        "token_file": {
                            "type": "string",
                            "description": "Token文件路径",
                        },
                        "token": {"type": "string", "description": "Token值"},
                        "priority": {
                            "type": "integer",
                            "default": 10,
                            "description": "优先级",
                        },
                    },
                },
                "model": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "算例名称"},
                        "rid": {"type": "string", "description": "算例RID"},
                        "local_path": {"type": "string", "description": "本地路径"},
                        "source_server": {"type": "string", "description": "源服务器"},
                        "target_server": {
                            "type": "string",
                            "description": "目标服务器",
                        },
                        "description": {"type": "string", "description": "算例描述"},
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "标签",
                        },
                        "force": {
                            "type": "boolean",
                            "default": False,
                            "description": "强制覆盖",
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {
                            "type": "string",
                            "enum": ["json", "yaml"],
                            "default": "json",
                        },
                        "path": {"type": "string", "default": "./results/"},
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "action": "status",
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        result = super().validate(config)
        action = config.get("action")

        if action in ["add_server"]:
            server = config.get("server", {})
            if not server.get("name"):
                result.add_error("add_server 需要指定 server.name")
            if not server.get("url"):
                result.add_error("add_server 需要指定 server.url")

        if action in ["push", "pull", "clone", "register", "info"]:
            model = config.get("model", {})
            if not model.get("name") and not model.get("rid"):
                result.add_error(f"{action} 需要指定 model.name 或 model.rid")

        if action == "remove_server":
            server = config.get("server", {})
            if not server.get("name"):
                result.add_error("remove_server 需要指定 server.name")

        if action == "use_server":
            server = config.get("server", {})
            if not server.get("name"):
                result.add_error("use_server 需要指定 server.name")

        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
        start_time = datetime.now()
        logs = []
        artifacts = []

        def log(level: str, message: str):
            logs.append(
                LogEntry(timestamp=datetime.now(), level=level, message=message)
            )
            getattr(logger, level.lower(), logger.info)(message)

        try:
            action = config.get("action", "status")
            log("INFO", f"执行操作: {action}")

            hub_dir = self._get_hub_dir(config)
            self._ensure_hub_dir(hub_dir)

            hub_config = HubConfig(hub_dir)
            model_registry = ModelRegistry(hub_dir)

            result_data = {"action": action}

            if action == "init":
                result_data = self._init_hub(hub_config, model_registry, config, log)
            elif action == "status":
                result_data = self._show_status(hub_config, model_registry, log)
            elif action == "list_servers":
                result_data = self._list_servers(hub_config, log)
            elif action == "add_server":
                result_data = self._add_server(hub_config, config, log)
            elif action == "remove_server":
                result_data = self._remove_server(hub_config, config, log)
            elif action == "use_server":
                result_data = self._use_server(hub_config, config, log)
            elif action == "list_models":
                result_data = self._list_models(model_registry, config, log)
            elif action == "list_local":
                result_data = self._list_local(hub_dir, config, log)
            elif action == "list_remote":
                result_data = self._list_remote(model_registry, hub_config, config, log)
            elif action == "push":
                result_data = self._push_model(model_registry, hub_config, config, log)
            elif action == "pull":
                result_data = self._pull_model(model_registry, hub_config, config, log)
            elif action == "clone":
                result_data = self._clone_model(model_registry, hub_config, config, log)
            elif action == "register":
                result_data = self._register_model(model_registry, config, log)
            elif action == "unregister":
                result_data = self._unregister_model(model_registry, config, log)
            elif action == "info":
                result_data = self._model_info(model_registry, hub_config, config, log)
            elif action == "export":
                result_data = self._export_model(
                    model_registry, hub_config, config, log
                )
            elif action == "import":
                result_data = self._import_model(
                    model_registry, hub_config, config, log
                )
            elif action == "sync":
                result_data = self._sync_models(model_registry, hub_config, config, log)
            else:
                raise ValueError(f"未知操作: {action}")

            output_config = config.get("output", {})
            if output_config.get("format") == "yaml":
                import yaml

                export_path = Path(output_config.get("path", "./results/"))
                export_path.mkdir(parents=True, exist_ok=True)
                output_file = export_path / "model_hub_result.yaml"
                with open(output_file, "w", encoding="utf-8") as f:
                    yaml.dump(
                        result_data, f, allow_unicode=True, default_flow_style=False
                    )
                artifacts.append(
                    Artifact(
                        name="result",
                        path=str(output_file),
                        description="Model Hub 操作结果",
                    )
                )

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
            )

        except Exception as e:
            log("ERROR", f"操作失败: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data={},
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )

    def _get_hub_dir(self, config: Dict) -> Path:
        hub_dir = config.get("hub_dir")
        if hub_dir:
            return Path(hub_dir)
        return self.DEFAULT_HUB_DIR

    def _ensure_hub_dir(self, hub_dir: Path):
        hub_dir.mkdir(parents=True, exist_ok=True)
        models_dir = hub_dir / self.DEFAULT_MODELS_DIR
        models_dir.mkdir(parents=True, exist_ok=True)

    def _init_hub(
        self,
        hub_config: "HubConfig",
        model_registry: "ModelRegistry",
        config: Dict,
        log,
    ) -> Dict:
        hub_config.init_default()
        log("INFO", f"已初始化算例中心: {hub_config.hub_dir}")
        return {"status": "initialized", "hub_dir": str(hub_config.hub_dir)}

    def _show_status(
        self, hub_config: "HubConfig", model_registry: "ModelRegistry", log
    ) -> Dict:
        servers = hub_config.list_servers()
        current = hub_config.get_current_server()
        models = model_registry.list_models()

        log("INFO", f"当前服务器: {current.get('name') if current else '无'}")
        log("INFO", f"已配置服务器: {len(servers)}")
        log("INFO", f"已注册算例: {len(models)}")

        return {
            "hub_dir": str(hub_config.hub_dir),
            "current_server": current,
            "servers": servers,
            "model_count": len(models),
            "models": models[:10] if len(models) > 10 else models,
        }

    def _list_servers(self, hub_config: "HubConfig", log) -> Dict:
        servers = hub_config.list_servers()
        current = hub_config.get_current_server()

        log("INFO", f"已配置服务器 ({len(servers)}):")
        for server in servers:
            marker = " *" if server.get("name") == current.get("name") else ""
            log("INFO", f"  - {server['name']}: {server['url']}{marker}")

        return {"servers": servers, "current": current.get("name") if current else None}

    def _add_server(self, hub_config: "HubConfig", config: Dict, log) -> Dict:
        server = config.get("server", {})
        name = server["name"]
        url = server["url"]
        token_file = server.get("token_file")
        token = server.get("token")
        priority = server.get("priority", 10)

        if token_file:
            token_path = Path(token_file)
            if token_path.exists():
                token = token_path.read_text().strip()
        elif not token:
            default_token_file = Path(f".cloudpss_token")
            if default_token_file.exists():
                token = default_token_file.read_text().strip()

        hub_config.add_server(name, url, token, token_file, priority)
        log("INFO", f"已添加服务器: {name} -> {url}")

        return {
            "status": "added",
            "server": {"name": name, "url": url, "priority": priority},
        }

    def _remove_server(self, hub_config: "HubConfig", config: Dict, log) -> Dict:
        name = config.get("server", {}).get("name")
        hub_config.remove_server(name)
        log("INFO", f"已移除服务器: {name}")
        return {"status": "removed", "server": name}

    def _use_server(self, hub_config: "HubConfig", config: Dict, log) -> Dict:
        name = config.get("server", {}).get("name")
        hub_config.use_server(name)
        log("INFO", f"已切换到服务器: {name}")
        return {"status": "switched", "current_server": name}

    def _list_models(self, model_registry: "ModelRegistry", config: Dict, log) -> Dict:
        models = model_registry.list_models()
        log("INFO", f"已注册算例 ({len(models)}):")
        for model in models:
            log("INFO", f"  - {model['name']}: {model.get('rid', 'N/A')}")
        return {"models": models, "count": len(models)}

    def _list_local(self, hub_dir: Path, config: Dict, log) -> Dict:
        models_dir = hub_dir / self.DEFAULT_MODELS_DIR
        local_models = []

        for model_dir in models_dir.iterdir():
            if model_dir.is_dir():
                meta_file = model_dir / "meta.yaml"
                model_file = model_dir / "model.yaml"
                meta = {}
                if meta_file.exists():
                    import yaml

                    meta = yaml.safe_load(meta_file.read_text()) or {}

                local_models.append(
                    {
                        "name": model_dir.name,
                        "has_model": model_file.exists(),
                        "meta": meta,
                        "path": str(model_dir),
                    }
                )

        log("INFO", f"本地算例 ({len(local_models)}):")
        for model in local_models:
            log("INFO", f"  - {model['name']}")

        return {"local_models": local_models, "count": len(local_models)}

    def _list_remote(
        self,
        model_registry: "ModelRegistry",
        hub_config: "HubConfig",
        config: Dict,
        log,
    ) -> Dict:
        current = hub_config.get_current_server()
        if not current:
            return {"error": "未配置当前服务器"}

        log("INFO", f"查询服务器 {current['name']} 上的算例...")

        try:
            from cloudpss import Model
            from cloudpss_skills.core.auth_utils import setToken

            token = current.get("token")
            if not token:
                token_file = current.get("token_file")
                if token_file and Path(token_file).exists():
                    token = Path(token_file).read_text().strip()

            if token:
                setToken(token)

            models = []
            log("INFO", f"已获取服务器 {current['name']} 上的算例列表")
            return {
                "remote_models": models,
                "count": len(models),
                "server": current["name"],
            }
        except Exception as e:
            log("WARNING", f"获取远程算例失败: {e}")
            return {"error": str(e), "server": current.get("name")}

    def _push_model(
        self,
        model_registry: "ModelRegistry",
        hub_config: "HubConfig",
        config: Dict,
        log,
    ) -> Dict:
        model_config = config.get("model", {})
        name = model_config.get("name")
        target_server = (
            model_config.get("target_server") or hub_config.get_current_server_name()
        )
        force = model_config.get("force", False)

        if not name:
            raise ValueError("需要指定算例名称")

        model_info = model_registry.get_model(name)
        if not model_info:
            raise ValueError(f"算例 {name} 未注册")

        rid = model_info.get("rids", {}).get(target_server)
        if rid and not force:
            log("WARNING", f"算例 {name} 在 {target_server} 上已存在 RID: {rid}")
            return {"status": "skipped", "reason": "already_exists", "rid": rid}

        local_path = model_registry.get_local_path(name)
        if not local_path.exists():
            raise ValueError(f"本地算例文件不存在: {local_path}")

        log("INFO", f"上传算例 {name} 到 {target_server}...")
        try:
            from cloudpss import Model

            model = Model.load(str(local_path))
            saved_model = model.save()
            new_rid = saved_model.rid

            model_registry.update_rid(name, target_server, new_rid)
            log("INFO", f"上传成功! RID: {new_rid}")

            return {
                "status": "uploaded",
                "name": name,
                "rid": new_rid,
                "server": target_server,
            }
        except Exception as e:
            log("ERROR", f"上传失败: {e}")
            raise

    def _pull_model(
        self,
        model_registry: "ModelRegistry",
        hub_config: "HubConfig",
        config: Dict,
        log,
    ) -> Dict:
        model_config = config.get("model", {})
        name = model_config.get("name")
        rid = model_config.get("rid")
        source_server = (
            model_config.get("source_server") or hub_config.get_current_server_name()
        )

        if not name and not rid:
            raise ValueError("需要指定算例名称或RID")

        if rid and not name:
            name = rid.split("/")[-1]

        log("INFO", f"下载算例 {name or rid} 从 {source_server}...")

        try:
            from cloudpss import Model
            from cloudpss_skills.core.auth_utils import setToken

            server_info = hub_config.get_server(source_server)
            token = server_info.get("token")
            if not token:
                token_file = server_info.get("token_file")
                if token_file and Path(token_file).exists():
                    token = Path(token_file).read_text().strip()

            if token:
                setToken(token)

            if not rid:
                rid = model_registry.get_rid(name, source_server)
            if not rid:
                raise ValueError(f"未找到算例 {name} 在 {source_server} 上的 RID")

            model = Model.fetch(rid)
            local_path = model_registry.save_local(name, model)
            model_registry.register_model(
                name, rid, source_server, {"source": "pulled"}
            )

            log("INFO", f"下载成功! 保存到: {local_path}")

            return {
                "status": "downloaded",
                "name": name,
                "rid": rid,
                "local_path": str(local_path),
            }
        except Exception as e:
            log("ERROR", f"下载失败: {e}")
            raise

    def _clone_model(
        self,
        model_registry: "ModelRegistry",
        hub_config: "HubConfig",
        config: Dict,
        log,
    ) -> Dict:
        model_config = config.get("model", {})
        rid = model_config.get("rid")
        name = model_config.get("name")
        source_server = (
            model_config.get("source_server") or hub_config.get_current_server_name()
        )
        target_server = (
            model_config.get("target_server") or hub_config.get_current_server_name()
        )

        if not rid:
            raise ValueError("需要指定 RID")

        if not name:
            name = rid.split("/")[-1]

        log("INFO", f"克隆算例 {rid} 从 {source_server} 到 {target_server}...")

        try:
            from cloudpss import Model
            from cloudpss_skills.core.auth_utils import setToken

            server_info = hub_config.get_server(source_server)
            token = server_info.get("token")
            if not token:
                token_file = server_info.get("token_file")
                if token_file and Path(token_file).exists():
                    token = Path(token_file).read_text().strip()

            if token:
                setToken(token)

            model = Model.fetch(rid)
            local_path = model_registry.save_local(name, model)

            if source_server != target_server:
                setToken(hub_config.get_server(target_server).get("token", ""))
                saved_model = model.save()
                new_rid = saved_model.rid
                model_registry.register_model(
                    name, rid, source_server, {"source": "cloned"}
                )
                model_registry.update_rid(name, target_server, new_rid)
                log("INFO", f"克隆成功! 新 RID: {new_rid}")
                return {
                    "status": "cloned",
                    "name": name,
                    "source_rid": rid,
                    "target_rid": new_rid,
                }
            else:
                model_registry.register_model(
                    name, rid, source_server, {"source": "cloned"}
                )
                log("INFO", f"克隆成功! 本地保存: {local_path}")
                return {
                    "status": "cloned",
                    "name": name,
                    "rid": rid,
                    "local_path": str(local_path),
                }
        except Exception as e:
            log("ERROR", f"克隆失败: {e}")
            raise

    def _register_model(
        self, model_registry: "ModelRegistry", config: Dict, log
    ) -> Dict:
        model_config = config.get("model", {})
        name = model_config.get("name")
        rid = model_config.get("rid")
        server = model_config.get("source_server", "default")
        description = model_config.get("description", "")
        tags = model_config.get("tags", [])

        if not name:
            raise ValueError("需要指定算例名称")

        metadata = {"description": description, "tags": tags}
        model_registry.register_model(name, rid, server, metadata)

        log("INFO", f"已注册算例: {name} -> {rid}")

        return {"status": "registered", "name": name, "rid": rid, "server": server}

    def _unregister_model(
        self, model_registry: "ModelRegistry", config: Dict, log
    ) -> Dict:
        model_config = config.get("model", {})
        name = model_config.get("name")

        if not name:
            raise ValueError("需要指定算例名称")

        model_registry.unregister_model(name)
        log("INFO", f"已取消注册算例: {name}")

        return {"status": "unregistered", "name": name}

    def _model_info(
        self,
        model_registry: "ModelRegistry",
        hub_config: "HubConfig",
        config: Dict,
        log,
    ) -> Dict:
        model_config = config.get("model", {})
        name = model_config.get("name")
        rid = model_config.get("rid")

        if rid and not name:
            name = rid.split("/")[-1]

        if not name:
            raise ValueError("需要指定算例名称或RID")

        info = model_registry.get_model(name)
        if not info:
            return {"error": f"算例 {name} 未注册", "name": name}

        info["name"] = name
        local_path = model_registry.get_local_path(name)
        info["local_exists"] = local_path.exists()
        info["local_path"] = str(local_path)

        log("INFO", f"算例信息: {name}")
        for key, value in info.items():
            log("INFO", f"  {key}: {value}")

        return info

    def _export_model(
        self,
        model_registry: "ModelRegistry",
        hub_config: "HubConfig",
        config: Dict,
        log,
    ) -> Dict:
        model_config = config.get("model", {})
        name = model_config.get("name")
        output_path = model_config.get("local_path")

        if not name:
            raise ValueError("需要指定算例名称")

        local_path = model_registry.get_local_path(name)
        if not local_path.exists():
            raise ValueError(f"本地算例不存在: {local_path}")

        if output_path:
            export_path = Path(output_path)
            shutil.copytree(local_path, export_path, dirs_exist_ok=True)
            log("INFO", f"已导出到: {export_path}")
            return {"status": "exported", "path": str(export_path)}
        else:
            return {"status": "exported", "path": str(local_path), "local_only": True}

    def _import_model(
        self,
        model_registry: "ModelRegistry",
        hub_config: "HubConfig",
        config: Dict,
        log,
    ) -> Dict:
        model_config = config.get("model", {})
        local_path = model_config.get("local_path")
        name = model_config.get("name")
        rid = model_config.get("rid")
        server = (
            model_config.get("target_server") or hub_config.get_current_server_name()
        )

        if not local_path:
            raise ValueError("需要指定本地路径")

        source_path = Path(local_path)
        if not source_path.exists():
            raise ValueError(f"本地路径不存在: {local_path}")

        if not name:
            name = source_path.name

        saved_path = model_registry.save_local(name, source_path)
        model_registry.register_model(name, rid, server, {"source": "imported"})

        log("INFO", f"已导入算例: {name} -> {saved_path}")

        return {"status": "imported", "name": name, "path": str(saved_path)}

    def _sync_models(
        self,
        model_registry: "ModelRegistry",
        hub_config: "HubConfig",
        config: Dict,
        log,
    ) -> Dict:
        model_config = config.get("model", {})
        source_server = (
            model_config.get("source_server") or hub_config.get_current_server_name()
        )
        target_server = model_config.get("target_server")

        if not target_server:
            servers = hub_config.list_servers()
            if len(servers) >= 2:
                target_server = [
                    s["name"] for s in servers if s["name"] != source_server
                ][0]

        if not target_server:
            return {"error": "需要指定目标服务器"}

        log("INFO", f"同步算例从 {source_server} 到 {target_server}...")

        models = model_registry.list_models()
        synced = []
        failed = []

        for model in models:
            name = model["name"]
            rid = model.get("rids", {}).get(source_server)
            if rid:
                try:
                    config_copy = config.copy()
                    config_copy["model"] = {
                        "name": name,
                        "rid": rid,
                        "source_server": source_server,
                        "target_server": target_server,
                    }
                    result = self._clone_model(
                        model_registry, hub_config, config_copy, log
                    )
                    synced.append(name)
                except Exception as e:
                    log("WARNING", f"同步 {name} 失败: {e}")
                    failed.append({"name": name, "error": str(e)})

        log("INFO", f"同步完成: {len(synced)} 成功, {len(failed)} 失败")

        return {
            "synced": synced,
            "failed": failed,
            "source": source_server,
            "target": target_server,
        }


class HubConfig:
    """服务器配置管理"""

    def __init__(self, hub_dir: Path):
        self.hub_dir = hub_dir
        self.config_file = hub_dir / "config.yaml"
        self._config: Dict[str, Any] = {}
        self._load()

    def _load(self):
        import yaml

        if self.config_file.exists():
            self._config = yaml.safe_load(self.config_file.read_text()) or {}

    def _save(self):
        import yaml

        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w", encoding="utf-8") as f:
            yaml.dump(self._config, f, allow_unicode=True, default_flow_style=False)

    def init_default(self):
        if not self._config:
            self._config = {
                "servers": {},
                "current_server": None,
            }
            self._save()

    def list_servers(self) -> List[Dict]:
        servers = self._config.get("servers", {})
        return [
            {
                "name": name,
                "url": info.get("url"),
                "token": "***" if info.get("token") else None,
                "token_file": info.get("token_file"),
                "priority": info.get("priority", 10),
            }
            for name, info in servers.items()
        ]

    def get_server(self, name: str) -> Optional[Dict]:
        servers = self._config.get("servers", {})
        return servers.get(name)

    def add_server(
        self,
        name: str,
        url: str,
        token: Optional[str],
        token_file: Optional[str],
        priority: int = 10,
    ):
        servers = self._config.setdefault("servers", {})
        servers[name] = {
            "url": url,
            "token": token,
            "token_file": token_file,
            "priority": priority,
        }
        if not self._config.get("current_server"):
            self._config["current_server"] = name
        self._save()

    def remove_server(self, name: str):
        servers = self._config.get("servers", {})
        if name in servers:
            del servers[name]
        if self._config.get("current_server") == name:
            self._config["current_server"] = None
        self._save()

    def use_server(self, name: str):
        servers = self._config.get("servers", {})
        if name not in servers:
            raise ValueError(f"服务器 {name} 不存在")
        self._config["current_server"] = name
        self._save()

    def get_current_server(self) -> Optional[Dict]:
        current = self._config.get("current_server")
        if current:
            servers = self._config.get("servers", {})
            info = servers.get(current)
            if info:
                return {"name": current, **info}
        return None

    def get_current_server_name(self) -> Optional[str]:
        return self._config.get("current_server")


class ModelRegistry:
    """算例注册表管理"""

    def __init__(self, hub_dir: Path):
        self.hub_dir = hub_dir
        self.registry_file = hub_dir / "registry.yaml"
        self.models_dir = hub_dir / "models"
        self._registry: Dict[str, Any] = {}
        self._load()

    def _load(self):
        import yaml

        if self.registry_file.exists():
            self._registry = yaml.safe_load(self.registry_file.read_text()) or {}

    def _save(self):
        import yaml

        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.registry_file, "w", encoding="utf-8") as f:
            yaml.dump(self._registry, f, allow_unicode=True, default_flow_style=False)

    def list_models(self) -> List[Dict]:
        return [{"name": name, **info} for name, info in self._registry.items()]

    def get_model(self, name: str) -> Optional[Dict]:
        return self._registry.get(name)

    def get_rid(self, name: str, server: str) -> Optional[str]:
        model = self._registry.get(name)
        if model:
            return model.get("rids", {}).get(server)
        return None

    def register_model(
        self, name: str, rid: Optional[str], server: str, metadata: Dict
    ):
        if name not in self._registry:
            self._registry[name] = {"rids": {}, "metadata": {}}

        if rid:
            rids = self._registry[name].setdefault("rids", {})
            rids[server] = rid

        meta = self._registry[name].get("metadata", {})
        meta.update(metadata)
        self._registry[name]["metadata"] = meta
        self._save()

    def unregister_model(self, name: str):
        if name in self._registry:
            del self._registry[name]
            self._save()

    def update_rid(self, name: str, server: str, rid: str):
        if name not in self._registry:
            self._registry[name] = {"rids": {}, "metadata": {}}
        rids = self._registry[name].setdefault("rids", {})
        rids[server] = rid
        self._save()

    def get_local_path(self, name: str) -> Path:
        return self.models_dir / name

    def save_local(self, name: str, source: Path) -> Path:
        dest = self.models_dir / name
        if source.is_file():
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest / "model.yaml")
        elif source.is_dir():
            shutil.copytree(source, dest, dirs_exist_ok=True)
        else:
            raise ValueError(f"无效的源路径: {source}")

        meta = dest / "meta.yaml"
        if not meta.exists():
            import yaml

            with open(meta, "w", encoding="utf-8") as f:
                yaml.dump({"name": name, "created": datetime.now().isoformat()}, f)

        return dest
