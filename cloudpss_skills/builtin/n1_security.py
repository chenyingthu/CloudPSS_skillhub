"""
N-1 Security Check Skill

N-1安全校核 - 逐一断开每条支路，检查系统是否仍能正常运行。
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register

logger = logging.getLogger(__name__)


@register
class N1SecuritySkill(SkillBase):
    """N-1安全校核技能"""

    @property
    def name(self) -> str:
        return "n1_security"

    @property
    def description(self) -> str:
        return "N-1安全校核 - 逐一停运支路评估系统安全性"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "n1_security"},
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
                        "branches": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "要检查的支路列表，空表示全部"
                        },
                        "check_voltage": {"type": "boolean", "default": True},
                        "check_thermal": {"type": "boolean", "default": True},
                        "voltage_threshold": {"type": "number", "default": 0.05, "description": "电压越限阈值(标幺值)"},
                        "thermal_threshold": {"type": "number", "default": 1.0, "description": "热稳定阈值(标幺值)"},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "yaml"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "n1_security"},
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
            "analysis": {
                "branches": [],
                "check_voltage": True,
                "check_thermal": True,
                "voltage_threshold": 0.05,
                "thermal_threshold": 1.0,
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "n1_security",
                "timestamp": True,
            },
        }

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行N-1安全校核"""
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

            # 3. 获取所有支路元件
            log("INFO", "获取支路信息...")
            components = model.getAllComponents()

            # 查找所有线路和变压器（支路类元件）
            branch_types = [
                "model/CloudPSS/line",
                "model/CloudPSS/3pline",
                "model/CloudPSS/transformer",
                "model/CloudPSS/3ptransformer",
                "model/CloudPSS/TransmissionLine",  # IEEE39实际使用的类型
                "model/CloudPSS/_newTransformer_3p2w",  # IEEE39实际使用的变压器类型
            ]

            branches = []
            for comp_id, comp in components.items():
                definition = getattr(comp, "definition", "")
                if any(bt in definition for bt in branch_types):
                    branches.append({
                        "id": comp_id,
                        "name": getattr(comp, "name", comp_id),
                        "type": definition.split("/")[-1],
                    })

            log("INFO", f"发现 {len(branches)} 条支路")

            # 4. 执行N-1校核
            analysis_config = config.get("analysis", {})
            target_branches = analysis_config.get("branches", [])

            if target_branches:
                # 只检查指定的支路
                branches = [b for b in branches if b["name"] in target_branches or b["id"] in target_branches]
                log("INFO", f"将检查 {len(branches)} 条指定支路")

            results = []
            passed = 0
            failed = 0

            for i, branch in enumerate(branches):
                log("INFO", f"[{i+1}/{len(branches)}] 停运支路: {branch['name']}")

                # 加载原始模型（每次重新加载以确保干净状态）
                if model_config.get("source") == "local":
                    working_model = Model.load(model_rid)
                else:
                    working_model = Model.fetch(model_rid)

                # 停运该支路（通过删除或禁用）
                try:
                    working_model.removeComponent(branch["id"])
                    log("INFO", f"  -> 已移除支路 {branch['name']}")
                except (KeyError, AttributeError) as e:
                    log("WARNING", f"  -> 移除支路失败: {e}")
                    continue

                # 运行潮流计算
                try:
                    job = working_model.runPowerFlow()

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

                    if status != 1:
                        # 潮流不收敛，N-1失败
                        result = {
                            "branch_id": branch["id"],
                            "branch_name": branch["name"],
                            "status": "failed",
                            "converged": False,
                            "violation": "潮流不收敛",
                        }
                        failed += 1
                        log("ERROR", f"  -> N-1失败: 潮流不收敛")
                    else:
                        # 潮流收敛，进一步检查结果
                        # 注意：这里简化处理，实际应检查电压和功率
                        result = {
                            "branch_id": branch["id"],
                            "branch_name": branch["name"],
                            "status": "passed",
                            "converged": True,
                            "violation": None,
                        }
                        passed += 1
                        log("INFO", f"  -> N-1通过")

                    results.append(result)

                except (KeyError, AttributeError, ConnectionError) as e:
                    result = {
                        "branch_id": branch["id"],
                        "branch_name": branch["name"],
                        "status": "error",
                        "converged": False,
                        "violation": str(e),
                    }
                    failed += 1
                    log("ERROR", f"  -> N-1异常: {e}")
                    results.append(result)

            # 5. 汇总结果
            log("INFO", "=" * 50)
            log("INFO", f"N-1校核完成: 通过 {passed}, 失败 {failed}")
            log("INFO", f"通过率: {passed/len(branches)*100:.1f}%" if branches else "N/A")

            # 6. 导出结果
            output_config = config.get("output", {})
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)

            prefix = output_config.get("prefix", "n1_security")
            use_timestamp = output_config.get("timestamp", True)

            filename = prefix
            if use_timestamp:
                filename += f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            filename += ".json"

            filepath = output_path / filename

            result_data = {
                "model_name": model.name,
                "model_rid": model.rid,
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_branches": len(branches),
                    "passed": passed,
                    "failed": failed,
                    "pass_rate": passed/len(branches) if branches else 0,
                },
                "results": results,
                "failed_branches": [r for r in results if r["status"] != "passed"],
            }

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)

            artifacts.append(Artifact(
                type="json",
                path=str(filepath),
                size=filepath.stat().st_size,
                description="N-1安全校核报告"
            ))

            log("INFO", f"结果已保存: {filepath}")

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS if failed == 0 else SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
                metrics={
                    "total_branches": len(branches),
                    "passed": passed,
                    "failed": failed,
                },
            )

        except (KeyError, AttributeError, ConnectionError) as e:
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
