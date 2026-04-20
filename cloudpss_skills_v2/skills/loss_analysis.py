"""Loss Analysis Skill v2 - Engine-agnostic network loss analysis.

网损分析、损耗统计、灵敏度计算、无功优化降损
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    LogEntry,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.powerskill import APIFactory, PowerFlowAPI

logger = logging.getLogger(__name__)


@dataclass
class BranchLoss:
    branch_id: str
    from_bus: str
    to_bus: str
    p_loss_mw: float
    q_loss_mvar: float
    current_ka: float
    loading_percent: float


@dataclass
class TransformerLoss:
    transformer_id: str
    hv_bus: str
    lv_bus: str
    core_loss_mw: Optional[float]
    copper_loss_mw: Optional[float]
    total_loss_mw: float
    reactive_loss_mvar: float = 0.0
    breakdown_verified: bool = False


def _as_float(value, default=0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


class LossAnalysisSkill:
    """网损分析与优化技能 - v2 engine-agnostic implementation."""

    name = "loss_analysis"
    description = "网损分析、损耗统计、灵敏度计算、无功优化降损"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "loss_analysis"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower", "algolib"],
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
                        "rid": {"type": "string"},
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                    },
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "loss_calculation": {
                            "type": "object",
                            "properties": {
                                "enabled": {"type": "boolean", "default": True},
                                "components": {
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "enum": ["lines", "transformers", "shunts"],
                                    },
                                    "default": ["lines", "transformers"],
                                },
                            },
                        },
                        "loss_sensitivity": {
                            "type": "object",
                            "properties": {
                                "enabled": {"type": "boolean", "default": True}
                            },
                        },
                        "loss_optimization": {
                            "type": "object",
                            "properties": {
                                "enabled": {"type": "boolean", "default": True},
                                "method": {
                                    "type": "string",
                                    "enum": [
                                        "reactive_power_optimization",
                                        "generation_dispatch",
                                    ],
                                    "default": "reactive_power_optimization",
                                },
                            },
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "yaml"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "loss_analysis"},
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
            "analysis": {
                "loss_calculation": {
                    "enabled": True,
                    "components": ["lines", "transformers"],
                },
                "loss_sensitivity": {"enabled": True},
                "loss_optimization": {
                    "enabled": True,
                    "method": "reactive_power_optimization",
                },
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "loss_analysis",
                "timestamp": True,
            },
        }

    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []
        self.branch_losses: list[BranchLoss] = []
        self.transformer_losses: list[TransformerLoss] = []

    def _log(self, level: str, message: str) -> None:
        self.logs.append(
            LogEntry(timestamp=datetime.now(), level=level, message=message)
        )
        getattr(logger, level.lower(), logger.info)(message)

    def _get_api(self, config: dict[str, Any]) -> PowerFlowAPI:
        engine = config.get("engine", "cloudpss")
        return APIFactory.create_powerflow_api(engine=engine)

    def validate(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
        errors = []
        if not config.get("model", {}).get("rid"):
            errors.append("必须指定模型RID")
        auth = config.get("auth", {})
        if not auth.get("token") and not auth.get("token_file"):
            errors.append("必须提供 auth.token 或 auth.token_file")
        return len(errors) == 0, errors

    def run(self, config: dict[str, Any]) -> SkillResult:
        start_time = datetime.now()
        self.logs = []
        self.artifacts = []
        self.branch_losses = []
        self.transformer_losses = []

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
            source = model_config.get("source", "cloud")
            auth = config.get("auth", {})

            self._log("INFO", "运行潮流计算...")
            sim_result = api.run_power_flow(
                model_id=model_rid, source=source, auth=auth
            )

            if not sim_result.is_success:
                raise RuntimeError(
                    f"潮流计算失败: {sim_result.errors[0] if sim_result.errors else 'unknown'}"
                )

            result_data = sim_result.data
            branches = result_data.get("branches", [])
            buses = result_data.get("buses", [])

            analysis_config = config.get("analysis", {})

            if analysis_config.get("loss_calculation", {}).get("enabled", True):
                components = analysis_config.get("loss_calculation", {}).get(
                    "components", ["lines", "transformers"]
                )
                if "lines" in components:
                    self._log("INFO", "计算线路损耗...")
                    self._calculate_line_losses(branches)

                if "transformers" in components:
                    self._log("INFO", "计算变压器损耗...")
                    self._calculate_transformer_losses(
                        branches, model_rid, source, auth
                    )

            sensitivity_results = {}
            if analysis_config.get("loss_sensitivity", {}).get("enabled", True):
                self._log("INFO", "计算网损灵敏度...")
                sensitivity_results = self._calculate_loss_sensitivity(buses, branches)

            optimization_results = {}
            if analysis_config.get("loss_optimization", {}).get("enabled", True):
                self._log("INFO", "生成无功优化建议...")
                optimization_results = self._generate_optimization_suggestions()

            result_data = {
                "model_rid": model_rid,
                "summary": self._generate_summary(),
                "branch_losses": [
                    self._branch_to_dict(bl) for bl in self.branch_losses
                ],
                "transformer_losses": [
                    self._transformer_to_dict(tl) for tl in self.transformer_losses
                ],
                "sensitivity_analysis": sensitivity_results,
                "optimization_suggestions": optimization_results,
                "timestamp": datetime.now().isoformat(),
            }

            output_config = config.get("output", {})
            self._save_output(result_data, output_config)

            self._log("INFO", "网损分析完成")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data=result_data,
                artifacts=self.artifacts,
                logs=self.logs,
                metrics={
                    "total_loss_mw": result_data["summary"]["total_loss_mw"],
                    "branch_count": len(self.branch_losses),
                    "transformer_count": len(self.transformer_losses),
                },
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            self._log("ERROR", f"网损分析失败: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                data={
                    "success": False,
                    "error": str(e),
                    "stage": "loss_analysis",
                },
                artifacts=self.artifacts,
                logs=self.logs,
                error=str(e),
                start_time=start_time,
                end_time=datetime.now(),
            )

    def _calculate_line_losses(self, branches: list[dict]) -> None:
        for branch in branches:
            p_loss = _as_float(
                branch.get("power_loss_mw")
                or branch.get("Ploss")
                or branch.get("P_loss")
            )
            q_loss = _as_float(
                branch.get("reactive_loss_mvar")
                or branch.get("Qloss")
                or branch.get("Q_loss")
            )

            if p_loss < 0.001 and q_loss < 0.001:
                continue

            branch_name = branch.get("name", "Unknown")
            from_bus = branch.get("from_bus", branch.get("From bus", ""))
            to_bus = branch.get("to_bus", branch.get("To bus", ""))
            i_ka = _as_float(branch.get("current_ka") or branch.get("I"), 0)
            loading_pct = _as_float(branch.get("loading_pct"), 0)

            self.branch_losses.append(
                BranchLoss(
                    branch_id=branch_name,
                    from_bus=from_bus,
                    to_bus=to_bus,
                    p_loss_mw=abs(p_loss),
                    q_loss_mvar=abs(q_loss),
                    current_ka=i_ka,
                    loading_percent=min(loading_pct, 100),
                )
            )

        self._log(
            "INFO",
            f"从潮流结果提取了 {len(self.branch_losses)} 条线路的损耗",
        )

    def _calculate_transformer_losses(
        self,
        branches: list[dict],
        model_rid: str,
        source: str,
        auth: dict,
    ) -> None:
        transformer_rids = [
            "model/CloudPSS/_newTransformer_3p2w",
            "model/CloudPSS/_newTransformer_3p",
        ]
        transformer_keys = set()

        try:
            from cloudpss import Model
            from cloudpss_skills_v2.powerapi.adapters.cloudpss._component_utils import (
                get_components_by_definition,
            )

            kwargs = {}
            base_url = auth.get("base_url") or auth.get("baseUrl")
            if base_url:
                kwargs["baseUrl"] = base_url

            if source == "local":
                model = Model.load(model_rid)
            else:
                model = Model.fetch(model_rid, **kwargs)

            for trid in transformer_rids:
                try:
                    comps = get_components_by_definition(model, trid)
                    for comp in comps:
                        comp_id = getattr(comp, "id", "")
                        if comp_id:
                            transformer_keys.add(comp_id)
                except Exception:
                    pass

            for branch in branches:
                branch_id = branch.get("key", branch.get("name", ""))
                if not branch_id:
                    continue

                if branch_id not in transformer_keys:
                    definition = str(branch.get("definition", "")).lower()
                    if "transformer" not in definition:
                        continue

                p_loss = _as_float(
                    branch.get("power_loss_mw")
                    or branch.get("Ploss")
                    or branch.get("P_loss")
                )
                q_loss = _as_float(
                    branch.get("reactive_loss_mvar")
                    or branch.get("Qloss")
                    or branch.get("Q_loss")
                )
                label = branch.get("name", branch_id)
                from_bus = branch.get("from_bus", branch.get("From bus", ""))
                to_bus = branch.get("to_bus", branch.get("To bus", ""))

                self.transformer_losses.append(
                    TransformerLoss(
                        transformer_id=label,
                        hv_bus=str(from_bus),
                        lv_bus=str(to_bus),
                        core_loss_mw=None,
                        copper_loss_mw=None,
                        total_loss_mw=abs(p_loss),
                        reactive_loss_mvar=abs(q_loss),
                        breakdown_verified=False,
                    )
                )

        except Exception as e:
            self._log("WARNING", f"变压器损耗计算回退到简化模式: {e}")
            for branch in branches:
                definition = str(branch.get("definition", "")).lower()
                if "transformer" not in definition:
                    continue
                p_loss = _as_float(branch.get("power_loss_mw") or branch.get("Ploss"))
                q_loss = _as_float(
                    branch.get("reactive_loss_mvar") or branch.get("Qloss")
                )
                label = branch.get("name", "Unknown")
                self.transformer_losses.append(
                    TransformerLoss(
                        transformer_id=label,
                        hv_bus="",
                        lv_bus="",
                        core_loss_mw=None,
                        copper_loss_mw=None,
                        total_loss_mw=abs(p_loss),
                        reactive_loss_mvar=abs(q_loss),
                    )
                )

        self._log(
            "INFO",
            f"从潮流结果提取了 {len(self.transformer_losses)} 台变压器的损耗",
        )

    def _calculate_loss_sensitivity(
        self, buses: list[dict], branches: list[dict]
    ) -> dict:
        sensitivities = []
        total_loss = sum(bl.p_loss_mw for bl in self.branch_losses)

        if total_loss <= 0 or not buses or not branches:
            return {
                "description": "网损对各节点无功注入的灵敏度",
                "method": "approximate_from_powerflow",
                "sensitivities": [],
                "available": False,
                "message": "无法从当前潮流结果计算灵敏度，需进行扰动分析",
            }

        for branch in branches:
            p_loss = _as_float(
                branch.get("power_loss_mw")
                or branch.get("Ploss")
                or branch.get("P_loss")
            )
            if p_loss <= 0:
                continue

            from_bus = branch.get("from_bus", branch.get("From bus", ""))
            to_bus = branch.get("to_bus", branch.get("To bus", ""))

            from_v = 1.0
            to_v = 1.0
            for bus in buses:
                bus_name = bus.get("name", bus.get("Bus", ""))
                if str(bus_name) == str(from_bus):
                    from_v = _as_float(bus.get("voltage_pu"), 1.0)
                if str(bus_name) == str(to_bus):
                    to_v = _as_float(bus.get("voltage_pu"), 1.0)

            loss_ratio = p_loss / total_loss

            for bus_label, bus_v in [
                (f"Bus_{from_bus}", from_v),
                (f"Bus_{to_bus}", to_v),
            ]:
                sensitivity = (1.0 - bus_v) * loss_ratio * 100 if bus_v < 1.0 else 0.0
                if sensitivity > 0.01:
                    sensitivities.append(
                        {
                            "bus": str(bus_label),
                            "voltage_pu": round(bus_v, 4),
                            "loss_ratio": round(loss_ratio, 4),
                            "sensitivity_estimate": round(sensitivity, 4),
                        }
                    )

        sensitivities.sort(key=lambda x: x.get("sensitivity_estimate", 0), reverse=True)

        return {
            "description": "网损对各节点无功注入的灵敏度（近似估算）",
            "method": "approximate_from_powerflow",
            "sensitivities": sensitivities[:10],
            "available": True,
            "note": "基于潮流结果的近似估算，精确灵敏度需进行扰动分析",
        }

    def _generate_optimization_suggestions(self) -> dict:
        total_loss = sum(bl.p_loss_mw for bl in self.branch_losses) + sum(
            tl.total_loss_mw for tl in self.transformer_losses
        )
        suggestions = []

        if total_loss > 10:
            suggestions.append(
                {
                    "type": "reactive_power_compensation",
                    "priority": "high",
                    "description": "建议在关键母线增加无功补偿",
                    "expected_improvement": f"{total_loss * 0.1:.1f} MW",
                }
            )

        suggestions.append(
            {
                "type": "voltage_optimization",
                "priority": "medium",
                "description": "优化电压水平可降低网损",
                "expected_improvement": f"{total_loss * 0.05:.1f} MW",
            }
        )

        return {
            "current_total_loss_mw": round(total_loss, 2),
            "optimization_potential": round(total_loss * 0.15, 2),
            "suggestions": suggestions,
        }

    def _generate_summary(self) -> dict:
        total_branch_loss = sum(bl.p_loss_mw for bl in self.branch_losses)
        total_transformer_loss = sum(tl.total_loss_mw for tl in self.transformer_losses)
        total_loss = total_branch_loss + total_transformer_loss

        top_loss_branches = sorted(
            self.branch_losses, key=lambda x: x.p_loss_mw, reverse=True
        )[:5]

        return {
            "total_loss_mw": round(total_loss, 2),
            "branch_loss_mw": round(total_branch_loss, 2),
            "transformer_loss_mw": round(total_transformer_loss, 2),
            "branch_count": len(self.branch_losses),
            "transformer_count": len(self.transformer_losses),
            "top_loss_branches": [
                {"id": bl.branch_id, "loss_mw": round(bl.p_loss_mw, 2)}
                for bl in top_loss_branches
            ],
        }

    def _branch_to_dict(self, bl: BranchLoss) -> dict:
        return {
            "branch_id": bl.branch_id,
            "from_bus": bl.from_bus,
            "to_bus": bl.to_bus,
            "p_loss_mw": round(bl.p_loss_mw, 4),
            "q_loss_mvar": round(bl.q_loss_mvar, 4),
            "current_ka": round(bl.current_ka, 4),
            "loading_percent": round(bl.loading_percent, 2),
        }

    def _transformer_to_dict(self, tl: TransformerLoss) -> dict:
        return {
            "transformer_id": tl.transformer_id,
            "hv_bus": tl.hv_bus,
            "lv_bus": tl.lv_bus,
            "core_loss_mw": round(tl.core_loss_mw, 4)
            if tl.core_loss_mw is not None
            else None,
            "copper_loss_mw": round(tl.copper_loss_mw, 4)
            if tl.copper_loss_mw is not None
            else None,
            "total_loss_mw": round(tl.total_loss_mw, 4),
            "reactive_loss_mvar": round(tl.reactive_loss_mvar, 4),
            "breakdown_verified": tl.breakdown_verified,
        }

    def _save_output(self, result_data: dict, output_config: dict) -> None:
        output_format = output_config.get("format", "json")
        output_path = Path(output_config.get("path", "./results/"))
        prefix = output_config.get("prefix", "loss_analysis")
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
            import yaml

            with open(filepath, "w", encoding="utf-8") as f:
                yaml.dump(result_data, f, allow_unicode=True, default_flow_style=False)

        self.artifacts.append(
            Artifact(
                name=filename,
                path=str(filepath),
                type=output_format,
                size_bytes=filepath.stat().st_size,
                description="网损分析结果",
            )
        )
        self._log("INFO", f"导出: {filepath}")


__all__ = ["LossAnalysisSkill"]
