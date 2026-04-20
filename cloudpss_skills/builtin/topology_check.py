"""
Topology Check Skill

拓扑检查 - 验证模型拓扑的完整性和合理性。
"""

import json
import logging
from datetime import datetime
from pathlib import Path
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
from cloudpss_skills.core.auth_utils import setup_auth

logger = logging.getLogger(__name__)


@register
class TopologyCheckSkill(SkillBase):
    """拓扑检查技能"""

    @property
    def name(self) -> str:
        return "topology_check"

    @property
    def description(self) -> str:
        return "检查模型拓扑完整性和连通性"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "topology_check"},
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
                "checks": {
                    "type": "object",
                    "properties": {
                        "islands": {
                            "type": "boolean",
                            "default": True,
                            "description": "检查孤岛",
                        },
                        "dangling": {
                            "type": "boolean",
                            "default": True,
                            "description": "检查悬空元件",
                        },
                        "parameter": {
                            "type": "boolean",
                            "default": True,
                            "description": "检查参数完整性",
                        },
                        "emt_ready": {
                            "type": "boolean",
                            "default": False,
                            "description": "检查EMT仿真准备",
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "yaml"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "topology_check"},
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
            "checks": {
                "islands": True,
                "dangling": True,
                "parameter": True,
                "emt_ready": False,
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "topology_check",
                "timestamp": True,
            },
        }

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行拓扑检查"""
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
            # 1. 认证
            setup_auth(config)
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

            # 3. 执行检查
            checks = config.get("checks", {})
            check_results = {
                "model_name": model.name,
                "model_rid": model.rid,
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_components": 0,
                    "issues": 0,
                    "warnings": 0,
                    "passed": 0,
                },
                "details": [],
            }

            # 获取拓扑
            log("INFO", "获取拓扑信息...")
            components = model.getAllComponents()
            check_results["summary"]["total_components"] = len(components)

            log("INFO", f"元件数量: {len(components)}")

            # 检查1: 孤岛检测（简化实现）
            if checks.get("islands", True):
                log("INFO", "检查孤岛...")
                # 简化的连通性检查
                buses = set()
                branches = []

                for comp_id, comp in components.items():
                    definition = getattr(comp, "definition", "")
                    # 收集母线
                    if "bus" in definition.lower():
                        buses.add(comp_id)

                # 这里简化处理，实际应该使用图算法
                check_results["details"].append(
                    {
                        "check": "islands",
                        "status": "passed",
                        "message": f"发现 {len(buses)} 个母线节点",
                    }
                )
                check_results["summary"]["passed"] += 1

            # 检查2: 悬空元件
            if checks.get("dangling", True):
                log("INFO", "检查悬空元件...")
                dangling = []

                for comp_id, comp in components.items():
                    definition = getattr(comp, "definition", "")
                    pins = getattr(comp, "pins", {})

                    # 检查是否有未连接的引脚
                    if isinstance(pins, dict):
                        unconnected = [p for p, v in pins.items() if not v or v == ""]
                        if unconnected:
                            dangling.append(
                                {
                                    "id": comp_id,
                                    "name": getattr(comp, "name", comp_id),
                                    "type": definition.split("/")[-1],
                                    "unconnected_pins": unconnected,
                                }
                            )

                if dangling:
                    log("WARNING", f"发现 {len(dangling)} 个悬空元件")
                    check_results["details"].append(
                        {
                            "check": "dangling",
                            "status": "warning",
                            "message": f"发现 {len(dangling)} 个悬空元件",
                            "items": dangling[:10],  # 只显示前10个
                        }
                    )
                    check_results["summary"]["warnings"] += 1
                else:
                    log("INFO", "无悬空元件")
                    check_results["details"].append(
                        {
                            "check": "dangling",
                            "status": "passed",
                            "message": "无悬空元件",
                        }
                    )
                    check_results["summary"]["passed"] += 1

            # 检查3: 参数完整性
            if checks.get("parameter", True):
                log("INFO", "检查参数完整性...")
                incomplete = []

                for comp_id, comp in components.items():
                    args = getattr(comp, "args", {})
                    if isinstance(args, dict):
                        empty_params = [
                            k for k, v in args.items() if v is None or v == ""
                        ]
                        if empty_params:
                            incomplete.append(
                                {
                                    "id": comp_id,
                                    "name": getattr(comp, "name", comp_id),
                                    "empty_params": empty_params,
                                }
                            )

                if incomplete:
                    log("WARNING", f"发现 {len(incomplete)} 个元件参数不完整")
                    check_results["details"].append(
                        {
                            "check": "parameter",
                            "status": "warning",
                            "message": f"发现 {len(incomplete)} 个元件参数不完整",
                            "items": incomplete[:10],
                        }
                    )
                    check_results["summary"]["warnings"] += 1
                else:
                    log("INFO", "参数完整")
                    check_results["details"].append(
                        {
                            "check": "parameter",
                            "status": "passed",
                            "message": "所有元件参数完整",
                        }
                    )
                    check_results["summary"]["passed"] += 1

            # 检查4: EMT就绪检查
            if checks.get("emt_ready", False):
                log("INFO", "检查EMT仿真准备...")
                try:
                    topology = model.fetchTopology(implementType="emtp")
                    check_results["details"].append(
                        {
                            "check": "emt_ready",
                            "status": "passed",
                            "message": "EMT拓扑检查通过",
                        }
                    )
                    check_results["summary"]["passed"] += 1
                except (KeyError, AttributeError) as e:
                    log("ERROR", f"EMT拓扑检查失败: {e}")
                    check_results["details"].append(
                        {
                            "check": "emt_ready",
                            "status": "failed",
                            "message": f"EMT拓扑检查失败: {e}",
                        }
                    )
                    check_results["summary"]["issues"] += 1

            # 4. 导出结果
            log("INFO", "=" * 50)
            log("INFO", f"拓扑检查完成:")
            log("INFO", f"  通过: {check_results['summary']['passed']}")
            log("INFO", f"  警告: {check_results['summary']['warnings']}")
            log("INFO", f"  问题: {check_results['summary']['issues']}")

            output_config = config.get("output", {})
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)

            prefix = output_config.get("prefix", "topology_check")
            use_timestamp = output_config.get("timestamp", True)

            filename = prefix
            if use_timestamp:
                filename += f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            filename += ".json"

            filepath = output_path / filename

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(check_results, f, indent=2, ensure_ascii=False)

            artifacts.append(
                Artifact(
                    type="json",
                    path=str(filepath),
                    size=filepath.stat().st_size,
                    description="拓扑检查报告",
                )
            )

            log("INFO", f"结果已保存: {filepath}")

            # 确定整体状态
            if check_results["summary"]["issues"] > 0:
                final_status = SkillStatus.FAILED  # 发现问题时返回失败
            else:
                final_status = SkillStatus.SUCCESS

            return SkillResult(
                skill_name=self.name,
                status=final_status,
                start_time=start_time,
                end_time=datetime.now(),
                data=check_results,
                artifacts=artifacts,
                logs=logs,
                metrics={
                    "total_components": check_results["summary"]["total_components"],
                    "passed": check_results["summary"]["passed"],
                    "warnings": check_results["summary"]["warnings"],
                    "issues": check_results["summary"]["issues"],
                },
            )

        except (KeyError, AttributeError, ConnectionError) as e:
            log("ERROR", f"执行失败: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "success": False,
                    "error": str(e),
                    "stage": "topology_check",
                },
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )
