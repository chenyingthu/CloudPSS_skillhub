"""
Parameter Scan Skill

参数扫描 - 对指定参数进行批量扫描仿真。
"""

import json
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
    clone_model,
    reload_model,
    run_powerflow_and_wait,
    run_emt_and_wait,
    OutputConfig,
    save_json,
)
from cloudpss_skills.core.utils import parse_cloudpss_table

logger = logging.getLogger(__name__)


@register
class ParamScanSkill(SkillBase):
    """参数扫描技能"""

    @property
    def name(self) -> str:
        return "param_scan"

    @property
    def description(self) -> str:
        return "参数扫描 - 批量改变参数运行多次仿真"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model", "scan"],
            "properties": {
                "skill": {"type": "string", "const": "param_scan"},
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
                "scan": {
                    "type": "object",
                    "required": ["component", "parameter", "values"],
                    "properties": {
                        "component": {"type": "string", "description": "元件ID或名称"},
                        "parameter": {"type": "string", "description": "参数名"},
                        "values": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "参数值列表",
                        },
                        "simulation_type": {
                            "enum": ["emt", "power_flow"],
                            "default": "power_flow",
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "param_scan"},
                        "timestamp": {"type": "boolean", "default": True},
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE3", "source": "cloud"},
            "scan": {
                "component": "",
                "parameter": "",
                "values": [],
                "simulation_type": "power_flow",
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "param_scan",
                "timestamp": True,
            },
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        """验证配置"""
        result = super().validate(config)  # 仍然调用，检查model.rid等基础字段

        scan = config.get("scan", {})

        # 提供详细的错误信息和指导
        if not scan.get("component"):
            result.add_error("必须指定scan.component（元件ID或名称）")
            result.add_error("  示例: 'Load_1', 'Bus_7', 'Generator_1'")
            result.add_warning("提示: component不能为空，请参考模型中的元件列表")

        if not scan.get("parameter"):
            result.add_error("必须指定scan.parameter（参数名）")
            result.add_error(
                "  示例: 'P' (有功功率), 'Q' (无功功率), 'Vset' (电压设定值)"
            )

        if not scan.get("values"):
            result.add_error("必须指定scan.values（参数值列表）")
            result.add_error("  示例: [10, 20, 30, 40, 50]")
            result.add_warning("提示: values必须是非空数组")

        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行参数扫描"""
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
            base_model = reload_model(
                model_config["rid"],
                model_config.get("source", "cloud"),
                config,
            )

            scan_config = config["scan"]
            component_key = scan_config["component"]
            param_name = scan_config["parameter"]
            values = scan_config["values"]
            sim_type = scan_config.get("simulation_type", "power_flow")

            log("INFO", f"参数扫描: {component_key}.{param_name}")
            log("INFO", f"扫描值: {values}")
            log("INFO", f"仿真类型: {sim_type}")

            results = []
            for i, value in enumerate(values):
                log("INFO", f"[{i + 1}/{len(values)}] {param_name} = {value}")

                model = clone_model(base_model)

                try:
                    components = model.getAllComponents()
                    target_comp = None

                    if component_key in components:
                        target_comp = components[component_key]
                    else:
                        for comp_id, comp in components.items():
                            if getattr(comp, "name", "") == component_key:
                                target_comp = comp
                                break

                    if not target_comp:
                        raise ValueError(f"找不到元件: {component_key}")

                    model.updateComponent(
                        target_comp.id,
                        args={param_name: {"source": str(value), "ɵexp": ""}},
                    )
                    log("INFO", f"  -> 已设置 {param_name} = {value}")

                except (AttributeError, TypeError, ValueError) as e:
                    log("ERROR", f"  -> 参数设置失败: {e}")
                    results.append(
                        {
                            "value": value,
                            "status": "error",
                            "error": str(e),
                        }
                    )
                    continue

                try:
                    if sim_type == "emt":
                        job_result = run_emt_and_wait(model, config, log_func=log)
                    else:
                        job_result = run_powerflow_and_wait(model, config, log_func=log)

                    if job_result.success:
                        job_id = getattr(getattr(job_result, "job", None), "id", None)
                        scan_result = {
                            "value": value,
                            "status": "success",
                            "job_id": job_id,
                            "converged": True,
                        }

                        if sim_type != "emt" and hasattr(job_result, "result"):
                            pf_result = job_result.result
                            if pf_result:
                                bus_rows = (
                                    parse_cloudpss_table(pf_result.getBuses())
                                    if pf_result.getBuses
                                    else None
                                )
                                branch_rows = (
                                    parse_cloudpss_table(pf_result.getBranches())
                                    if pf_result.getBranches
                                    else None
                                )
                                scan_result["bus_count"] = (
                                    len(bus_rows) if bus_rows else 0
                                )
                                scan_result["branch_count"] = (
                                    len(branch_rows) if branch_rows else 0
                                )
                                scan_result["buses"] = bus_rows if bus_rows else []
                                scan_result["branches"] = (
                                    branch_rows if branch_rows else []
                                )

                        results.append(scan_result)
                        log("INFO", f"  -> 仿真成功 ({job_result.waited_seconds:.1f}s)")
                    else:
                        failed_job_id = getattr(
                            getattr(job_result, "job", None), "id", None
                        )
                        results.append(
                            {
                                "value": value,
                                "status": "failed",
                                "job_id": failed_job_id,
                                "converged": False,
                            }
                        )
                        log(
                            "WARNING",
                            f"  -> 仿真未收敛 ({job_result.waited_seconds:.1f}s)",
                        )

                except (
                    AttributeError,
                    ConnectionError,
                    RuntimeError,
                    FileNotFoundError,
                    ValueError,
                ) as e:
                    log("ERROR", f"  -> 仿真异常: {e}")
                    results.append(
                        {
                            "value": value,
                            "status": "error",
                            "error": str(e),
                        }
                    )

            # 5. 导出结果
            log("INFO", "=" * 50)
            log("INFO", f"参数扫描完成: {len(results)} 次仿真")

            output_config = config.get("output", {})
            output = OutputConfig(
                path=output_config.get("path", "./results/"),
                prefix=output_config.get("prefix", "param_scan"),
                timestamp=output_config.get("timestamp", True),
            )

            scan_result = {
                "model_rid": model_config["rid"],
                "scan": scan_config,
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total": len(values),
                    "success": sum(1 for r in results if r["status"] == "success"),
                    "failed": sum(1 for r in results if r["status"] != "success"),
                },
                "results": results,
            }

            export_result = save_json(scan_result, output, description="参数扫描结果")
            if export_result.artifact:
                artifacts.append(export_result.artifact)

            log("INFO", f"结果已保存: {export_result.filepath}")

            failed_count = sum(1 for r in results if r["status"] != "success")

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS if failed_count == 0 else SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data=scan_result,
                artifacts=artifacts,
                logs=logs,
                metrics={
                    "total_scans": len(values),
                    "success": scan_result["summary"]["success"],
                    "failed": scan_result["summary"]["failed"],
                },
            )

        except (
            AttributeError,
            ConnectionError,
            RuntimeError,
            FileNotFoundError,
            ValueError,
            TimeoutError,
            TypeError,
        ) as e:
            log("ERROR", f"执行失败: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "success": False,
                    "error": str(e),
                    "stage": "param_scan",
                },
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )
