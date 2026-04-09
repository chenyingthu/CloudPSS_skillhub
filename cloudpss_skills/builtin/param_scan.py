"""
Parameter Scan Skill

参数扫描 - 对指定参数进行批量扫描仿真。
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Union

from cloudpss_skills.core import (
    Artifact,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    register,
)
from cloudpss_skills.core.auth_utils import load_or_fetch_model, run_emt, run_powerflow

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
        from cloudpss import Model, setToken

        start_time = datetime.now()
        logs = []
        artifacts = []

        def log(level: str, message: str):
            logs.append(
                LogEntry(timestamp=datetime.now(), level=level, message=message)
            )
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

            # 3. 获取扫描配置
            scan_config = config["scan"]
            component_key = scan_config["component"]
            param_name = scan_config["parameter"]
            values = scan_config["values"]
            sim_type = scan_config.get("simulation_type", "power_flow")

            log("INFO", f"参数扫描: {component_key}.{param_name}")
            log("INFO", f"扫描值: {values}")
            log("INFO", f"仿真类型: {sim_type}")

            # 4. 执行扫描
            results = []
            for i, value in enumerate(values):
                log("INFO", f"[{i + 1}/{len(values)}] {param_name} = {value}")

                # 重新加载模型
                model = load_or_fetch_model(model_config, config)

                # 查找并更新元件参数
                try:
                    components = model.getAllComponents()
                    target_comp = None

                    # 先尝试直接匹配ID
                    if component_key in components:
                        target_comp = components[component_key]
                    else:
                        # 尝试匹配名称
                        for comp_id, comp in components.items():
                            if getattr(comp, "name", "") == component_key:
                                target_comp = comp
                                break

                    if not target_comp:
                        raise ValueError(f"找不到元件: {component_key}")

                    # 更新参数
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

                # 运行仿真
                try:
                    if sim_type == "emt":
                        job = run_emt(model, config)
                    else:
                        job = run_powerflow(model, config)

                    # 等待仿真完成
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

                    if status == 1:
                        result_data = {
                            "value": value,
                            "status": "success",
                            "job_id": job.id,
                            "converged": True,
                        }
                        log("INFO", f"  -> 仿真成功 ({waited}s)")
                    else:
                        result_data = {
                            "value": value,
                            "status": "failed",
                            "job_id": job.id,
                            "converged": False,
                        }
                        log("WARNING", f"  -> 仿真未收敛 ({waited}s, status={status})")

                    results.append(result_data)

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
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)

            prefix = output_config.get("prefix", "param_scan")
            use_timestamp = output_config.get("timestamp", True)

            filename = prefix
            if use_timestamp:
                filename += f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            filename += ".json"

            filepath = output_path / filename

            scan_result = {
                "model_rid": model_rid,
                "scan": scan_config,
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total": len(values),
                    "success": sum(1 for r in results if r["status"] == "success"),
                    "failed": sum(1 for r in results if r["status"] != "success"),
                },
                "results": results,
            }

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(scan_result, f, indent=2, ensure_ascii=False)

            artifacts.append(
                Artifact(
                    type="json",
                    path=str(filepath),
                    size=filepath.stat().st_size,
                    description="参数扫描结果",
                )
            )

            log("INFO", f"结果已保存: {filepath}")

            # 根据结果确定状态
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
                data={},
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )
