"""Power Flow Skill v2 - Engine-agnostic power flow simulation.

Runs power flow simulation using the PowerSkill API layer,
which delegates to the configured engine adapter (CloudPSS, pandapower, etc.).
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    LogEntry,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.powerapi import EngineConfig
from cloudpss_skills_v2.powerskill import Engine, PowerFlow

logger = logging.getLogger(__name__)


class PowerFlowPreset:
    """潮流计算预设入口 - v2 engine-agnostic implementation."""

    name = "power_flow"
    description = "运行潮流计算并输出结果"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "power_flow", "default": "power_flow"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "cloudpss",
                },
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
                        "rid": {"type": "string", "default": "model/holdme/IEEE39"},
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                    },
                },
                "algorithm": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "enum": ["newton_raphson", "fast_decoupled"],
                            "default": "newton_raphson",
                        },
                        "tolerance": {"type": "number", "default": 1e-6},
                        "max_iterations": {"type": "integer", "default": 100},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "power_flow"},
                        "timestamp": {"type": "boolean", "default": True},
                    },
                },
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "engine": "cloudpss",
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

    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []

    def _log(self, level: str, message: str) -> None:
        self.logs.append(
            LogEntry(timestamp=datetime.now(), level=level, message=message)
        )
        getattr(logger, level.lower(), logger.info)(message)

    def _get_api(self, config: dict[str, Any]) -> PowerFlow:
        engine = config.get("engine", "cloudpss")
        auth = config.get("auth", {})
        engine_config = EngineConfig(
            engine_name=engine,
            base_url=auth.get("base_url", ""),
            extra={"auth": auth},
        )
        return Engine.create_powerflow(engine=engine, config=engine_config)

    def validate(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
        errors = []
        if not config.get("model", {}).get("rid"):
            errors.append("必须提供 model.rid")
        auth = config.get("auth", {})
        if not auth.get("token") and not auth.get("token_file"):
            errors.append("必须提供 auth.token 或 auth.token_file")
        return len(errors) == 0, errors

    def run(self, config: dict[str, Any]) -> SkillResult:
        start_time = datetime.now()
        self.logs = []
        self.artifacts = []

        valid, errors = self.validate(config)
        if not valid:
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error="; ".join(errors),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )

        try:
            api = self._get_api(config)
            self._log("INFO", f"使用引擎: {api.adapter.engine_name}")

            model_config = config["model"]
            model_rid = model_config["rid"]
            algorithm_config = config.get("algorithm", {})

            self._log("INFO", f"运行潮流计算: {model_rid}")

            sim_result = api.run_power_flow(
                model_id=model_rid,
                algorithm=algorithm_config.get("type", "newton_raphson"),
                tolerance=algorithm_config.get("tolerance", 1e-6),
                max_iterations=algorithm_config.get("max_iterations", 100),
                source=model_config.get("source", "cloud"),
                auth=config.get("auth", {}),
            )

            if not sim_result.is_success:
                raise RuntimeError(
                    sim_result.errors[0] if sim_result.errors else "潮流计算失败"
                )

            result_data = sim_result.data
            if not result_data.get("buses") or not result_data.get("branches"):
                raise RuntimeError("潮流结果为空或缺少母线/支路表")

            output_config = config.get("output", {})
            self._save_output(result_data, output_config)

            self._log(
                "INFO",
                f"潮流计算完成: {result_data.get('bus_count', 0)} 条母线, "
                f"{result_data.get('branch_count', 0)} 条支路",
            )

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data=result_data,
                artifacts=self.artifacts,
                logs=self.logs,
                metrics={
                    "bus_count": result_data.get("bus_count", 0),
                    "branch_count": result_data.get("branch_count", 0),
                    "converged": result_data.get("converged", False),
                },
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            self._log("ERROR", str(e))
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                data={"success": False, "error": str(e), "stage": "power_flow"},
                artifacts=self.artifacts,
                logs=self.logs,
                error=str(e),
                start_time=start_time,
                end_time=datetime.now(),
            )

    def _save_output(self, result_data: dict, output_config: dict) -> None:
        output_format = output_config.get("format", "json")
        output_path = Path(output_config.get("path", "./results/"))
        prefix = output_config.get("prefix", "power_flow")
        use_timestamp = output_config.get("timestamp", True)

        output_path.mkdir(parents=True, exist_ok=True)

        ts_suffix = (
            f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}" if use_timestamp else ""
        )
        filename = f"{prefix}{ts_suffix}.{output_format}"
        filepath = output_path / filename

        if output_format == "json":
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False, default=str)
        else:
            self._save_csv(result_data, filepath)

        self.artifacts.append(
            Artifact(
                name=filename,
                path=str(filepath),
                type=output_format,
                size_bytes=filepath.stat().st_size,
                description="潮流计算结果",
            )
        )
        self._log("INFO", f"导出: {filepath}")

    def _save_csv(self, result_data: dict, filepath: Path) -> None:
        import csv

        buses = result_data.get("buses", [])
        if not buses:
            return

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=buses[0].keys())
            writer.writeheader()
            writer.writerows(buses)

    def _generate_summary(self, bus_rows: list[dict], branch_rows: list[dict]) -> dict:
        """Generate summary statistics from normalized bus/branch rows."""
        total_p_gen = total_q_gen = total_p_load = total_q_load = total_loss = 0.0
        min_voltage = 999.0
        max_voltage = 0.0

        for bus in bus_rows:
            p_gen = _as_float(bus.get("generation_mw") or bus.get("Pg"))
            q_gen = _as_float(bus.get("generation_mvar") or bus.get("Qg"))
            p_load = _as_float(bus.get("load_mw") or bus.get("Pl"))
            q_load = _as_float(bus.get("load_mvar") or bus.get("Ql"))
            vm = _as_float(bus.get("voltage_pu") or bus.get("Vm"), 1.0)
            total_p_gen += p_gen
            total_q_gen += q_gen
            total_p_load += p_load
            total_q_load += q_load
            if 0 < vm < min_voltage:
                min_voltage = vm
            if vm > max_voltage:
                max_voltage = vm

        for branch in branch_rows:
            p_loss = _as_float(
                branch.get("power_loss_mw")
                or branch.get("Ploss")
                or branch.get("P_loss")
            )
            total_loss += p_loss

        return {
            "total_generation": {
                "p_mw": round(total_p_gen, 2),
                "q_mvar": round(total_q_gen, 2),
            },
            "total_load": {
                "p_mw": round(total_p_load, 2),
                "q_mvar": round(total_q_load, 2),
            },
            "total_loss_mw": round(total_loss, 4),
            "voltage_range": {
                "min_pu": round(min_voltage, 4),
                "max_pu": round(max_voltage, 4),
            },
        }


def _as_float(value, default=0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


__all__ = ["PowerFlowPreset"]
