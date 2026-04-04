"""
Power Flow Skill

运行潮流计算。
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register

logger = logging.getLogger(__name__)


@register
class PowerFlowSkill(SkillBase):
    """潮流计算技能"""

    @property
    def name(self) -> str:
        return "power_flow"

    @property
    def description(self) -> str:
        return "运行潮流计算并输出结果"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "power_flow"},
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "token_file": {"type": "string", "default": ".cloudpss_token"},
                    },
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {
                        "rid": {"type": "string"},
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                    },
                },
                "algorithm": {
                    "type": "object",
                    "properties": {
                        "type": {"enum": ["newton_raphson", "fast_decoupled"], "default": "newton_raphson"},
                        "tolerance": {"type": "number", "default": 1e-6},
                        "max_iterations": {"type": "integer", "default": 100},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "yaml", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "power_flow"},
                        "timestamp": {"type": "boolean", "default": True},
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39", "source": "cloud"},
            "algorithm": {
                "type": "newton_raphson",
                "tolerance": 1e-6,
                "max_iterations": 100,
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "power_flow",
                "timestamp": True,
            },
        }

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行潮流计算"""
        from cloudpss import Model, setToken

        start_time = datetime.now()
        logs = []
        artifacts = []

        def log(level: str, message: str):
            logs.append(LogEntry(
                timestamp=datetime.now(),
                level=level,
                message=message
            ))
            getattr(logger, level.lower(), logger.info)(message)

        try:
            # 1. 认证
            log("INFO", "加载认证信息...")
            auth = config.get("auth", {})
            token = auth.get("token")

            if not token:
                token_file = auth.get("token_file", ".cloudpss_token")
                token_path = Path(token_file)
                if not token_path.exists():
                    raise FileNotFoundError(f"Token文件不存在: {token_file}")
                token = token_path.read_text().strip()

            setToken(token)
            log("INFO", "认证成功")

            # 2. 获取模型
            log("INFO", "获取模型...")
            model_config = config["model"]
            model_rid = model_config["rid"]

            if model_config.get("source") == "local":
                model = Model.load(model_rid)
            else:
                model = Model.fetch(model_rid)

            log("INFO", f"模型: {model.name} ({model.rid})")

            # 3. 运行潮流
            log("INFO", "运行潮流计算...")
            job = model.runPowerFlow()
            log("INFO", f"任务已创建: {job.id}")

            # 4. 等待完成
            import time
            max_wait = 120
            waited = 0
            status = 0
            while waited < max_wait:
                status = job.status()
                if status == 1:  # 完成
                    break
                elif status == 2:  # 失败
                    break
                time.sleep(2)
                waited += 2

            log("INFO", f"任务状态: {status} ({waited}s)")

            if status != 1:
                raise RuntimeError(f"潮流计算未成功完成，状态: {status}")

            # 5. 获取结果
            log("INFO", "提取结果...")
            result = job.result
            if result is None or not result.getBuses() or not result.getBranches():
                raise RuntimeError("潮流结果为空或缺少母线/支路表")

            # 6. 导出
            output_config = config.get("output", {})
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)

            prefix = output_config.get("prefix", "power_flow")
            use_timestamp = output_config.get("timestamp", True)

            filename = prefix
            if use_timestamp:
                filename += f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            filename += ".json"

            filepath = output_path / filename

            # 保存结果
            result_data = {
                "model": model.name,
                "model_rid": model.rid,
                "job_id": job.id,
                "converged": True,
                "timestamp": datetime.now().isoformat(),
            }

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)

            artifacts.append(Artifact(
                type="json",
                path=str(filepath),
                size=filepath.stat().st_size,
                description="潮流计算结果"
            ))

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
            )

        except (KeyError, AttributeError, ZeroDivisionError, RuntimeError, FileNotFoundError, ValueError, TypeError) as e:
            log("ERROR", str(e))
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
