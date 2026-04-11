"""
Thevenin Equivalent Skill

Compute a PCC Thevenin equivalent from CloudPSS topology data.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from cloudpss_skills.core import (
    Artifact,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    register,
)
from cloudpss_skills.core.auth_utils import setup_auth
from cloudpss_skills.core.network_equivalent import compute_positive_sequence_zth

logger = logging.getLogger(__name__)


@register
class TheveninEquivalentSkill(SkillBase):
    """PCC戴维南等值技能"""

    @property
    def name(self) -> str:
        return "thevenin_equivalent"

    @property
    def description(self) -> str:
        return "计算指定PCC的戴维南等值阻抗、短路容量和可选SCR"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model", "pcc"],
            "properties": {
                "skill": {"type": "string", "const": "thevenin_equivalent"},
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
                "pcc": {
                    "type": "object",
                    "required": ["bus"],
                    "properties": {
                        "bus": {
                            "type": "string",
                            "description": "PCC母线名，如 bus8 / Bus8 / BUS_8",
                        },
                    },
                },
                "equivalent": {
                    "type": "object",
                    "properties": {
                        "system_base_mva": {"type": "number", "default": 100.0},
                        "rating_mva": {
                            "type": "number",
                            "description": "可选。若提供则顺带计算SCR",
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "thevenin_equivalent"},
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
            "pcc": {"bus": "bus8"},
            "equivalent": {"system_base_mva": 100.0},
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "thevenin_equivalent",
                "timestamp": True,
            },
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        result = ValidationResult(valid=True)
        if not config.get("model", {}).get("rid"):
            result.add_error("必须提供 model.rid")
        if not config.get("pcc", {}).get("bus"):
            result.add_error("必须提供 pcc.bus")
        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
        from cloudpss import Model

        start_time = datetime.now()
        logs = []
        artifacts = []

        def log(level: str, message: str):
            logs.append(
                LogEntry(timestamp=datetime.now(), level=level, message=message)
            )
            getattr(logger, level.lower(), logger.info)(message)

        try:
            setup_auth(config)
            log("INFO", "认证成功")

            model_config = config["model"]
            if model_config.get("source") == "local":
                model = Model.load(model_config["rid"])
            else:
                model = Model.fetch(model_config["rid"])

            pcc_bus = config["pcc"]["bus"]
            system_base_mva = float(
                config.get("equivalent", {}).get("system_base_mva", 100.0)
            )
            rating_mva = config.get("equivalent", {}).get("rating_mva")

            log("INFO", f"计算PCC戴维南等值: model={model.rid}, bus={pcc_bus}")
            zth = compute_positive_sequence_zth(
                model, pcc_bus, system_base_mva=system_base_mva
            )
            if not zth.verified or zth.z_th_pu is None:
                raise RuntimeError(zth.error or "无法计算PCC戴维南等值")

            zth_mag = abs(zth.z_th_pu)
            short_circuit_capacity_mva = (
                system_base_mva / zth_mag if zth_mag > 0 else float("inf")
            )
            result_data = {
                "model_rid": model.rid,
                "model_name": getattr(model, "name", model.rid),
                "pcc_bus": pcc_bus,
                "bus_node": zth.bus_node,
                "bus_nominal_voltage_kv": zth.bus_nominal_voltage_kv,
                "system_base_mva": system_base_mva,
                "z_th_pu": {
                    "real": round(zth.z_th_pu.real, 6),
                    "imag": round(zth.z_th_pu.imag, 6),
                    "magnitude": round(zth_mag, 6),
                },
                "short_circuit_capacity_mva": round(short_circuit_capacity_mva, 2),
                "verified": True,
            }

            if rating_mva is not None:
                scr = (
                    short_circuit_capacity_mva / float(rating_mva)
                    if float(rating_mva) > 0
                    else float("inf")
                )
                result_data["rating_mva"] = float(rating_mva)
                result_data["scr"] = round(scr, 2)

            output_config = config.get("output", {})
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "thevenin_equivalent")
            filename = prefix
            if output_config.get("timestamp", True):
                filename += f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            filename += ".json"
            filepath = output_path / filename
            filepath.write_text(
                json.dumps(result_data, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            artifacts.append(
                Artifact(
                    type="json",
                    path=str(filepath),
                    size=filepath.stat().st_size,
                    description="PCC戴维南等值结果",
                )
            )

            log(
                "INFO",
                f"Zth={result_data['z_th_pu']}, Ssc={result_data['short_circuit_capacity_mva']} MVA",
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

        except (
            KeyError,
            AttributeError,
            RuntimeError,
            FileNotFoundError,
            ValueError,
            TypeError,
        ) as e:
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
