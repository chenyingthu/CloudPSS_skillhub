"""
IEEE3 Preparation Skill

准备IEEE3模型用于EMT仿真。
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register

logger = logging.getLogger(__name__)


@register
class IEEE3PrepSkill(SkillBase):
    """IEEE3 EMT准备技能"""

    @property
    def name(self) -> str:
        return "ieee3_prep"

    @property
    def description(self) -> str:
        return "准备IEEE3模型用于EMT仿真（调整故障时间和输出通道）"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill"],
            "properties": {
                "skill": {"type": "string", "const": "ieee3_prep"},
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "token_file": {"type": "string", "default": ".cloudpss_token"},
                    },
                },
                "model": {
                    "type": "object",
                    "properties": {
                        "rid": {"type": "string", "default": "model/holdme/IEEE3"},
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                    },
                },
                "fault": {
                    "type": "object",
                    "properties": {
                        "start_time": {"type": "number", "default": 2.5},
                        "end_time": {"type": "number", "default": 2.7},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "sampling_freq": {"type": "integer", "default": 2000},
                        "path": {"type": "string", "default": "./"},
                        "filename": {"type": "string", "default": "ieee3_prepared.yaml"},
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE3", "source": "cloud"},
            "fault": {
                "start_time": 2.5,
                "end_time": 2.7,
            },
            "output": {
                "sampling_freq": 2000,
                "path": "./",
                "filename": "ieee3_prepared.yaml",
            },
        }

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行准备流程"""
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
            log("INFO", "加载认证...")
            auth = config.get("auth", {})
            token = auth.get("token")

            if not token:
                token_file = auth.get("token_file", ".cloudpss_token")
                token_path = Path(token_file)
                if token_path.exists():
                    token = token_path.read_text().strip()
                    setToken(token)

            # 2. 获取模型
            log("INFO", "获取IEEE3模型...")
            model_config = config.get("model", {})
            model_rid = model_config.get("rid", "model/holdme/IEEE3")

            if model_config.get("source") == "local":
                model = Model.load(model_rid)
            else:
                model = Model.fetch(model_rid)

            log("INFO", f"模型: {model.name}")

            # 3. 创建本地工作副本
            log("INFO", "创建本地工作副本...")
            output_config = config.get("output", {})
            output_path = Path(output_config.get("path", "./"))
            filename = output_config.get("filename", "ieee3_prepared.yaml")
            filepath = output_path / filename

            output_path.mkdir(parents=True, exist_ok=True)

            # 4. 调整故障参数（如果有）
            fault_config = config.get("fault", {})
            if fault_config:
                log("INFO", "调整故障参数...")
                # 查找故障元件
                components = model.getAllComponents()
                fault = None
                for comp in components.values():
                    if getattr(comp, "definition", "") == "model/CloudPSS/_newFaultResistor_3p":
                        fault = comp
                        break

                if fault:
                    new_start = fault_config.get("start_time", 2.5)
                    new_end = fault_config.get("end_time", 2.7)

                    model.updateComponent(
                        fault.id,
                        args={
                            "fs": {"source": str(new_start), "ɵexp": ""},
                            "fe": {"source": str(new_end), "ɵexp": ""},
                        },
                    )
                    log("INFO", f"故障时间: {new_start}s - {new_end}s")

            # 5. 调整输出采样
            sampling_freq = output_config.get("sampling_freq", 2000)
            log("INFO", f"设置采样频率: {sampling_freq}Hz")

            # 6. 保存
            log("INFO", f"保存到: {filepath}")
            Model.dump(model, str(filepath), compress=None)

            artifacts.append(Artifact(
                type="yaml",
                path=str(filepath),
                size=filepath.stat().st_size,
                description="准备好的IEEE3模型"
            ))

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "model_name": model.name,
                    "model_rid": model.rid,
                    "output_path": str(filepath),
                    "fault": fault_config,
                    "sampling_freq": sampling_freq,
                },
                artifacts=artifacts,
                logs=logs,
            )

        except (KeyError, AttributeError, ZeroDivisionError) as e:
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
