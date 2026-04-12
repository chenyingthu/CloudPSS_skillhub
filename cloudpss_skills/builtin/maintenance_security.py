"""
Maintenance Security Skill

检修方式安全校核 - 计划停运 + 残余N-1复核
"""

import csv
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

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
    OutputConfig,
    save_json,
)
from cloudpss_skills.core.utils import parse_cloudpss_table

logger = logging.getLogger(__name__)

TRANSMISSION_LINE_RID = "model/CloudPSS/TransmissionLine"
TRANSFORMER_RID = "model/CloudPSS/_newTransformer_3p2w"


@register
class MaintenanceSecuritySkill(SkillBase):
    """检修方式安全校核技能"""

    @property
    def name(self) -> str:
        return "maintenance_security"

    @property
    def description(self) -> str:
        return "检修方式安全校核 - 计划停运后残余N-1复核"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "maintenance_security"},
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
                "maintenance": {
                    "type": "object",
                    "required": ["branch_id"],
                    "properties": {
                        "branch_id": {
                            "type": "string",
                            "description": "计划停运的支路ID",
                        },
                        "description": {"type": "string", "description": "检修说明"},
                    },
                },
                "residual_n1": {
                    "type": "object",
                    "properties": {
                        "branches": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "残余N-1复核支路列表，空表示自动发现",
                        },
                        "include_transformers": {"type": "boolean", "default": True},
                        "limit": {"type": "integer"},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "maintenance_security"},
                        "generate_report": {"type": "boolean", "default": True},
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39", "source": "cloud"},
            "maintenance": {
                "branch_id": "",
                "description": "计划检修停运",
            },
            "residual_n1": {
                "branches": [],
                "include_transformers": True,
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "maintenance_security",
                "generate_report": True,
            },
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        result = super().validate(config)
        maintenance = config.get("maintenance", {})
        if not maintenance.get("branch_id"):
            result.add_error("必须指定 maintenance.branch_id（计划停运的支路ID）")
        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
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
            log("INFO", f"模型: {base_model.name}")

            # 获取配置
            maintenance_config = config["maintenance"]
            residual_config = config.get("residual_n1", {})
            output_config = config.get("output", {})

            maintenance_id = maintenance_config["branch_id"]
            maintenance_desc = maintenance_config.get("description", "计划检修")

            # 基线潮流
            log("INFO", "计算基线潮流...")
            base_buses, base_branches = self._run_powerflow(base_model, config)
            log("INFO", f"基线: {len(base_buses)}母线, {len(base_branches)}支路")

            # 计划停运
            log("INFO", f"执行计划停运: {maintenance_id} ({maintenance_desc})")
            working_model = clone_model(base_model)
            self._disable_branch(working_model, maintenance_id)
            maint_buses, maint_branches = self._run_powerflow(working_model, config)

            # 评估检修态
            maintenance_case = {
                "branch_id": maintenance_id,
                "description": maintenance_desc,
                "min_vm": min(b.get("Vm", 1.0) for b in maint_buses)
                if maint_buses
                else 1.0,
                "max_branch_loading": self._max_branch_loading(
                    working_model, maint_branches
                ),
            }
            maintenance_case["severity"] = self._classify_severity(maintenance_case)
            log("INFO", f"检修态: severity={maintenance_case['severity']}")

            # 残余N-1复核
            log("INFO", "残余N-1复核...")
            followup_ids = residual_config.get("branches", [])
            if not followup_ids:
                followup_ids = self._discover_branches(
                    working_model, residual_config.get("include_transformers", True)
                )
                followup_ids = [b for b in followup_ids if b != maintenance_id]

            if residual_config.get("limit"):
                followup_ids = followup_ids[: residual_config["limit"]]

            n1_results = []
            failed_cases = []
            for i, branch_id in enumerate(followup_ids):
                log("INFO", f"  [{i + 1}/{len(followup_ids)}] N-1: {branch_id}")
                try:
                    n1_model = Model(deepcopy(working_model.toJSON()))
                    self._disable_branch(n1_model, branch_id)
                    n1_buses, n1_branches = self._run_powerflow(n1_model, config)
                    n1_case = {
                        "branch_id": branch_id,
                        "min_vm": min(b.get("Vm", 1.0) for b in n1_buses)
                        if n1_buses
                        else 1.0,
                        "max_loading": self._max_branch_loading(n1_model, n1_branches),
                    }
                    n1_case["severity"] = self._classify_severity(n1_case)
                    n1_results.append(n1_case)
                except (
                    KeyError,
                    AttributeError,
                    RuntimeError,
                    ValueError,
                    TypeError,
                ) as e:
                    log("WARNING", f"    失败: {e}")
                    failed_cases.append({"branch_id": branch_id, "error": str(e)})

            # 导出
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "maintenance_security")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            critical_count = sum(1 for r in n1_results if r["severity"] == "critical")
            warning_count = sum(1 for r in n1_results if r["severity"] == "warning")
            overall_status = SkillStatus.SUCCESS
            if (
                maintenance_case["severity"] != "normal"
                or critical_count > 0
                or failed_cases
            ):
                overall_status = SkillStatus.FAILED

            result_data = {
                "model": base_model.name,
                "maintenance": maintenance_case,
                "residual_n1_count": len(n1_results),
                "critical_count": critical_count,
                "warning_count": warning_count,
                "failed_count": len(failed_cases),
                "results": n1_results,
                "failed_cases": failed_cases,
            }

            # JSON
            json_path = output_path / f"{prefix}_{timestamp}.json"
            with open(json_path, "w") as f:
                json.dump(result_data, f, indent=2)
            artifacts.append(
                Artifact(
                    type="json",
                    path=str(json_path),
                    size=json_path.stat().st_size,
                    description="检修安全结果",
                )
            )

            # CSV
            csv_path = output_path / f"{prefix}_{timestamp}.csv"
            self._export_csv(maintenance_case, n1_results, csv_path)
            artifacts.append(
                Artifact(
                    type="csv",
                    path=str(csv_path),
                    size=csv_path.stat().st_size,
                    description="检修安全CSV",
                )
            )

            # Report
            if output_config.get("generate_report", True):
                report_path = output_path / f"{prefix}_report_{timestamp}.md"
                self._generate_report(maintenance_case, n1_results, report_path)
                artifacts.append(
                    Artifact(
                        type="markdown",
                        path=str(report_path),
                        size=report_path.stat().st_size,
                        description="检修安全报告",
                    )
                )

            return SkillResult(
                skill_name=self.name,
                status=overall_status,
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

    def _run_powerflow(self, model, config: Optional[Dict] = None):
        job_result = run_powerflow_and_wait(model, config)
        if not job_result.success:
            raise RuntimeError(job_result.error or "潮流计算失败")
        result = job_result.result
        if result is None:
            raise RuntimeError("潮流结果为空")
        buses_table = result.getBuses()
        branches_table = result.getBranches()
        buses = self._table_to_rows(buses_table)
        branches = self._table_to_rows(branches_table)
        if not buses or not branches:
            raise RuntimeError("潮流结果缺少母线或支路表")
        return buses, branches

    def _table_to_rows(self, table):
        """将CloudPSS表结构转换为行字典列表"""
        if not table:
            return []
        # CloudPSS 常返回 [table_dict]，需要先做列转行
        if isinstance(table, list):
            return parse_cloudpss_table(table)
        # 如果是字典（列格式），转换为行
        if isinstance(table, dict):
            if table.get("type") == "table":
                return parse_cloudpss_table([table])
            rows = []
            columns = list(table.keys())
            if not columns:
                return []
            num_rows = len(table[columns[0]])
            for i in range(num_rows):
                row = {col: table[col][i] for col in columns}
                rows.append(row)
            return rows
        return []

    def _disable_branch(self, model, branch_id):
        model.updateComponent(branch_id, props={"enabled": False})

    def _discover_branches(self, model, include_transformers):
        rids = [TRANSMISSION_LINE_RID]
        if include_transformers:
            rids.append(TRANSFORMER_RID)
        branch_ids = []
        for rid in rids:
            try:
                components = model.getComponentsByRid(rid)
                for comp in components.values():
                    if comp.props.get("enabled", True):
                        branch_ids.append(comp.id)
            except Exception as e:
                # 异常已捕获，无需额外处理
                logger.debug(f"忽略预期异常: {e}")
        return sorted(branch_ids)

    def _classify_severity(self, case):
        min_vm = case.get("min_vm", 1.0)
        max_loading = case.get("max_loading", case.get("max_branch_loading", 0))
        if min_vm < 0.85 or max_loading > 1.2:
            return "critical"
        if min_vm < 0.9 or max_loading > 1.0:
            return "warning"
        return "normal"

    def _export_csv(self, maintenance, n1_results, path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["type", "branch_id", "severity", "min_vm", "max_loading"])
            writer.writerow(
                [
                    "maintenance",
                    maintenance["branch_id"],
                    maintenance["severity"],
                    f"{maintenance['min_vm']:.4f}",
                    f"{maintenance['max_branch_loading']:.4f}",
                ]
            )
            for r in n1_results:
                writer.writerow(
                    [
                        "residual_n1",
                        r["branch_id"],
                        r["severity"],
                        f"{r['min_vm']:.4f}",
                        f"{r['max_loading']:.4f}",
                    ]
                )

    def _generate_report(self, maintenance, n1_results, path):
        lines = [
            "# 检修方式安全校核报告",
            "",
            f"## 计划停运",
            f"- 支路: {maintenance['branch_id']}",
            f"- 严重度: {maintenance['severity']}",
            f"- 最低电压: {maintenance['min_vm']:.4f}",
            "",
            "## 残余N-1复核",
            "",
        ]
        critical = [r for r in n1_results if r["severity"] == "critical"]
        warning = [r for r in n1_results if r["severity"] == "warning"]
        lines.extend(
            [
                f"- 严重: {len(critical)}",
                f"- 警告: {len(warning)}",
                f"- 正常: {len(n1_results) - len(critical) - len(warning)}",
                "",
            ]
        )
        if critical:
            lines.append("### 严重工况")
            for r in critical:
                lines.append(f"- {r['branch_id']}: min_vm={r['min_vm']:.4f}")
            lines.append("")
        path.write_text("\n".join(lines), encoding="utf-8")

    @staticmethod
    def _read_numeric_arg(args: Dict[str, Any], key: str):
        value = args.get(key)
        if isinstance(value, dict):
            value = value.get("source")
        if value in (None, ""):
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _branch_loading(self, model, row: Dict[str, Any]) -> float:
        branch_id = row.get("Branch")
        if not branch_id:
            return 0.0

        component = model.getComponentByKey(branch_id)
        args = getattr(component, "args", {}) or {}
        definition = str(getattr(component, "definition", "") or "")

        p_ij = self._read_numeric_arg(row, "Pij") or 0.0
        q_ij = self._read_numeric_arg(row, "Qij") or 0.0
        p_ji = self._read_numeric_arg(row, "Pji") or 0.0
        q_ji = self._read_numeric_arg(row, "Qji") or 0.0
        apparent_mva = max((p_ij**2 + q_ij**2) ** 0.5, (p_ji**2 + q_ji**2) ** 0.5)

        rating_mva = None
        if "Transformer" in definition:
            rating_mva = self._read_numeric_arg(args, "Tmva")
        elif "TransmissionLine" in definition:
            i_rated = self._read_numeric_arg(args, "Irated")
            v_base = self._read_numeric_arg(args, "Vbase")
            if i_rated and i_rated > 0 and v_base and v_base > 0:
                rating_mva = 1.7320508075688772 * v_base * i_rated

        if not rating_mva or rating_mva <= 0:
            return 0.0
        return apparent_mva / rating_mva

    def _max_branch_loading(self, model, branch_rows: List[Dict[str, Any]]) -> float:
        max_loading = 0.0
        for row in branch_rows:
            try:
                max_loading = max(max_loading, self._branch_loading(model, row))
            except Exception as exc:
                logger.debug(f"计算支路负载率失败: {exc}")
        return max_loading
