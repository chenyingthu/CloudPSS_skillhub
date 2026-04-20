"""
Power Flow Skill

运行潮流计算。
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

from cloudpss_skills.core import (
    Artifact,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    register,
)
from cloudpss_skills.core import (
    setup_auth,
    reload_model,
    run_powerflow_and_wait,
    OutputConfig,
    save_json,
    build_artifact,
)
from cloudpss_skills.core.utils import parse_cloudpss_table

logger = logging.getLogger(__name__)


def _as_float(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


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
            model = reload_model(
                model_config["rid"],
                model_config.get("source", "cloud"),
                config,
            )
            log("INFO", f"模型: {model.name} ({model.rid})")

            log("INFO", "运行潮流计算...")
            job_result = run_powerflow_and_wait(model, config, log_func=log)

            if not job_result.success:
                raise RuntimeError(job_result.error or "潮流计算失败")

            result = job_result.result
            if result is None or not result.getBuses() or not result.getBranches():
                raise RuntimeError("潮流结果为空或缺少母线/支路表")

            bus_rows = parse_cloudpss_table(result.getBuses())
            branch_rows = parse_cloudpss_table(result.getBranches())
            if not bus_rows or not branch_rows:
                raise RuntimeError("潮流结果表为空，不能判定为有效收敛")

            output_config = config.get("output", {})
            output = OutputConfig(
                path=output_config.get("path", "./results/"),
                prefix=output_config.get("prefix", "power_flow"),
                timestamp=output_config.get("timestamp", True),
            )

            # Safe access to job.id (job may be None even if success is True)
            job_id = getattr(getattr(job_result, "job", None), "id", None)

            result_data = {
                "model": model.name,
                "model_rid": model.rid,
                "job_id": job_id,
                "converged": True,
                "bus_count": len(bus_rows),
                "branch_count": len(branch_rows),
                "timestamp": datetime.now().isoformat(),
                # Complete power flow results
                "buses": bus_rows,
                "branches": branch_rows,
                # Summary statistics
                "summary": self._generate_summary(bus_rows, branch_rows),
            }

            export_result = save_json(
                result_data,
                output,
                description="潮流计算结果",
            )

            if export_result.artifact:
                artifacts.append(export_result.artifact)

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
            FileNotFoundError,
            ValueError,
            TypeError,
            Exception,
        ) as e:
            log("ERROR", str(e))
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "success": False,
                    "error": str(e),
                    "stage": "power_flow",
                },
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )

    def _generate_summary(self, bus_rows: List[Dict], branch_rows: List[Dict]) -> Dict:
        total_p_gen = 0.0
        total_q_gen = 0.0
        total_p_load = 0.0
        total_q_load = 0.0
        total_loss = 0.0
        min_voltage = 999.0
        max_voltage = 0.0

        for bus in bus_rows:
            p_gen = _as_float(bus.get("Pg") or bus.get("<i>P</i><sub>g</sub> / MW"))
            q_gen = _as_float(bus.get("Qg") or bus.get("<i>Q</i><sub>g</sub> / Mvar"))
            p_load = _as_float(bus.get("Pl") or bus.get("<i>P</i><sub>l</sub> / MW"))
            q_load = _as_float(bus.get("Ql") or bus.get("<i>Q</i><sub>l</sub> / Mvar"))
            vm = _as_float(bus.get("Vm") or bus.get("<i>V</i><sub>m</sub> / pu"), 1.0)

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
                branch.get("Ploss") or branch.get("P_loss") or branch.get("P_Loss")
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
