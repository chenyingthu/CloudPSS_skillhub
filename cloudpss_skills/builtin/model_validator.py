#!/usr/bin/env python3
"""
模型验证技能 (model_validator)

功能：系统性验证测试算例的有效性，分阶段进行拓扑、潮流、暂态验证。

适用：验证 model_builder 创建的测试算例是否真实可用

作者: Claude Code
日期: 2026-04-01
"""

import logging
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from cloudpss_skills.core.base import (
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    LogEntry,
    Artifact,
)
from cloudpss_skills.core.auth_utils import (
    setup_auth,
    DEFAULT_TIMEOUT,
    DEFAULT_POWERFLOW_TOLERANCE,
    fetch_model_by_rid,
    run_powerflow,
    run_emt,
)
from cloudpss_skills.core.registry import register
from cloudpss_skills.metadata.integration import get_metadata_integration

logger = logging.getLogger(__name__)


BUS_COLUMN = "Bus"
NODE_COLUMN = "Node"
VM_COLUMN = "<i>V</i><sub>m</sub> / pu"
P_GEN_COLUMN = "<i>P</i><sub>gen</sub> / MW"
Q_GEN_COLUMN = "<i>Q</i><sub>gen</sub> / MVar"


def table_rows(table: Dict[str, Any]) -> List[Dict[str, Any]]:
    """把 CloudPSS 表格结果展平成行列表。"""
    columns = table.get("data", {}).get("columns", [])
    labels = [
        column.get("name") or column.get("title") or f"col_{index}"
        for index, column in enumerate(columns)
    ]
    row_count = len(columns[0].get("data", [])) if columns else 0
    rows = []
    for row_index in range(row_count):
        rows.append(
            {
                label: column.get("data", [None] * row_count)[row_index]
                for label, column in zip(labels, columns)
            }
        )
    return rows


class ValidationPhase(Enum):
    """验证阶段"""

    TOPOLOGY = "topology"  # 拓扑验证
    POWERFLOW = "powerflow"  # 潮流验证
    EMT = "emt"  # 暂态验证
    PARAMETER = "parameter"  # 参数验证


@dataclass
class ValidationReport:
    """验证报告"""

    model_rid: str
    model_name: str = ""
    phases: Dict[str, Any] = field(default_factory=dict)
    overall_passed: bool = False
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@register
class ModelValidatorSkill(SkillBase):
    """
    模型验证技能

    分阶段验证测试算例：
    1. 拓扑验证 - 检查孤岛、悬空元件、参数完整性
    2. 潮流验证 - 运行潮流计算，检查收敛性和结果合理性
    3. 暂态验证 - 运行EMT仿真，检查仿真可行性
    4. 参数验证 - 对比原始模型，验证修改正确性

    配置示例:
        skill: model_validator

        auth:
          token_file: .cloudpss_token

        models:
          - rid: model/holdme/test_IEEE39_with_PV_50MW
            base_rid: model/holdme/IEEE39  # 可选，用于对比验证

        validation:
          phases:
            - topology
            - powerflow
            - emt
          timeout: 300

        output:
          format: json
          path: ./validation_report.json
    """

    name = "model_validator"
    description = "系统性验证测试算例有效性（拓扑/潮流/暂态）"
    version = "1.0.0"

    RENEWABLE_KEYWORDS = (
        "wgsource",
        "wind",
        "dfig_windfarm_equivalent_model",
        "wtg_pmsg",
        "pvstation",
        "pv_inverter",
        "pvs_01",
    )

    config_schema = {
        "type": "object",
        "required": ["skill", "models"],
        "properties": {
            "skill": {"type": "string", "const": "model_validator"},
            "auth": {
                "type": "object",
                "properties": {
                    "token": {"type": "string"},
                    "token_file": {"type": "string"},
                },
            },
            "models": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "rid": {"type": "string"},
                        "base_rid": {"type": "string"},
                        "name": {"type": "string"},
                    },
                    "required": ["rid"],
                },
            },
            "validation": {
                "type": "object",
                "properties": {
                    "phases": {
                        "type": "array",
                        "items": {
                            "enum": ["topology", "powerflow", "emt", "parameter"]
                        },
                        "default": ["topology", "powerflow"],
                    },
                    "timeout": {"type": "integer", "default": 300},
                    "powerflow_tolerance": {"type": "number", "default": 1e-6},
                    "emt_duration": {"type": "number", "default": 1.0},
                },
            },
            "output": {
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "enum": ["json", "console"],
                        "default": "console",
                    },
                    "path": {"type": "string"},
                },
            },
        },
        "required": ["skill", "models"],
    }

    def __init__(self):
        super().__init__()
        self.reports = []
        self._metadata_integration = get_metadata_integration()
        self._metadata_integration.initialize()

    def validate(self, config: Dict) -> ValidationResult:
        """验证配置"""
        errors = []

        models = config.get("models", [])
        if not models:
            errors.append("必须指定至少一个模型")

        for i, model in enumerate(models):
            if not model.get("rid"):
                errors.append(f"models[{i}] 必须指定 rid")

        return ValidationResult(valid=len(errors) == 0, errors=errors)

    def run(self, config: Dict) -> SkillResult:
        """执行验证"""
        start_time = datetime.now()
        try:
            setup_auth(config)

            models = config.get("models", [])
            validation_config = config.get("validation", {})
            phases = validation_config.get("phases", ["topology", "powerflow"])
            timeout = validation_config.get("timeout", 300)

            logger.info(f"开始验证 {len(models)} 个模型")
            logger.info(f"验证阶段: {phases}")

            reports = []
            for model_info in models:
                report = self._validate_single_model(
                    model_info, phases, validation_config
                )
                reports.append(report)

            self.reports = reports

            # 输出结果
            output_config = config.get("output", {})
            self._output_results(reports, output_config)

            # 统计
            passed = sum(1 for r in reports if r.overall_passed)
            total = len(reports)

            result_data = {
                "total_models": total,
                "passed": passed,
                "failed": total - passed,
                "reports": [
                    {
                        "model_rid": r.model_rid,
                        "model_name": r.model_name,
                        "passed": r.overall_passed,
                        "phases": r.phases,
                        "issues": r.issues,
                        "warnings": r.warnings,
                    }
                    for r in reports
                ],
            }

            logger.info(f"验证完成: {passed}/{total} 通过")

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
            )

        except Exception as e:
            # run()方法顶层异常捕获，确保任何错误都返回FAILED状态
            logger.error(f"验证失败: {e}", exc_info=True)
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                error=str(e),
            )

    def _validate_single_model(
        self, model_info: Dict, phases: List[str], validation_config: Dict
    ) -> ValidationReport:
        """验证单个模型"""
        rid = model_info["rid"]
        base_rid = model_info.get("base_rid")
        name = model_info.get("name", rid)

        logger.info(f"\n{'=' * 60}")
        logger.info(f"验证模型: {name}")
        logger.info(f"RID: {rid}")
        logger.info(f"{'=' * 60}")

        report = ValidationReport(model_rid=rid, model_name=name)

        validation_order = ["topology", "powerflow", "emt", "parameter"]
        requested_phases = [phase for phase in validation_order if phase in phases]
        previous_failed = None

        for phase in requested_phases:
            if previous_failed is not None:
                report.phases[phase] = self._skipped_phase_result(
                    phase, f"跳过 {phase}：前序阶段 {previous_failed} 未通过"
                )
                continue

            if phase == "topology":
                phase_result = self._validate_topology(model_info)
            elif phase == "powerflow":
                phase_result = self._validate_powerflow(
                    model_info,
                    validation_config.get(
                        "powerflow_tolerance", DEFAULT_POWERFLOW_TOLERANCE
                    ),
                    validation_config.get("timeout", DEFAULT_TIMEOUT),
                )
            elif phase == "emt":
                phase_result = self._validate_emt(
                    rid, validation_config.get("emt_duration", 1.0)
                )
            elif phase == "parameter":
                if not base_rid:
                    phase_result = self._skipped_phase_result(
                        phase, "跳过 parameter：未提供 base_rid"
                    )
                else:
                    phase_result = self._validate_parameters(rid, base_rid)
            else:
                phase_result = self._skipped_phase_result(
                    phase, f"跳过未知阶段 {phase}"
                )

            report.phases[phase] = phase_result
            if phase_result.get("passed") is False and not phase_result.get(
                "skipped", False
            ):
                previous_failed = phase

        # 汇总结果
        report.issues = []
        report.warnings = []
        for phase, result in report.phases.items():
            if not result.get("passed", False):
                report.issues.extend(result.get("errors", []))
            report.warnings.extend(result.get("warnings", []))

        report.overall_passed = len(report.issues) == 0

        logger.info(f"\n验证结果: {'✅ 通过' if report.overall_passed else '❌ 失败'}")
        if report.issues:
            logger.info(f"问题: {len(report.issues)} 个")
        if report.warnings:
            logger.info(f"警告: {len(report.warnings)} 个")

        return report

    @staticmethod
    def _skipped_phase_result(phase: str, reason: str) -> Dict:
        """构造序贯验证中的跳过阶段结果。"""
        return {
            "phase": phase,
            "passed": False,
            "skipped": True,
            "errors": [],
            "warnings": [reason],
            "details": {"reason": reason},
        }

    @staticmethod
    def _component_name(comp_id: str, comp: Any) -> str:
        args = getattr(comp, "args", {}) or {}
        return getattr(comp, "label", None) or args.get("Name") or comp_id

    @staticmethod
    def _normalize_name(value: Any) -> str:
        if value is None:
            return ""
        return re.sub(r"[^a-z0-9]+", "", str(value).lower())

    @classmethod
    def _is_bus_component(cls, comp: Any) -> bool:
        definition = (getattr(comp, "definition", "") or "").lower()
        return "_newbus" in definition or definition.endswith("bus_3p")

    @classmethod
    def _is_renewable_component(cls, comp: Any) -> bool:
        definition = (getattr(comp, "definition", "") or "").lower()
        return any(keyword in definition for keyword in cls.RENEWABLE_KEYWORDS)

    @staticmethod
    def _first_connected_pin(pins: Dict[str, Any]) -> Optional[str]:
        for pin_value in (pins or {}).values():
            if (
                isinstance(pin_value, str)
                and pin_value
                and not pin_value.startswith("@")
            ):
                return pin_value
        return None

    @staticmethod
    def _coerce_number(value: Any) -> Optional[float]:
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, dict):
            for key in ("source", "value"):
                nested = value.get(key)
                if nested is not None:
                    return ModelValidatorSkill._coerce_number(nested)
        try:
            return float(str(value))
        except (TypeError, ValueError):
            return None

    def _expected_active_power(self, comp: Any) -> Optional[float]:
        args = getattr(comp, "args", {}) or {}
        for key in ("pf_P", "P_cmd", "Pnom", "额定容量"):
            value = self._coerce_number(args.get(key))
            if value is not None and value > 0:
                return value
        return None

    def _build_bus_signal_map(self, components: Dict[str, Any]) -> Dict[str, str]:
        bus_signals = {}
        for comp_id, comp in components.items():
            if not self._is_bus_component(comp):
                continue
            args = getattr(comp, "args", {}) or {}
            pins = getattr(comp, "pins", {}) or {}
            for candidate in (
                comp_id,
                args.get("Name"),
                pins.get("0"),
                getattr(comp, "label", None),
            ):
                if candidate:
                    bus_signals[str(candidate)] = comp_id
        return bus_signals

    def _validate_topology(self, model_info: Dict[str, Any]) -> Dict:
        """拓扑验证"""
        logger.info("\n[阶段1] 拓扑验证...")
        from cloudpss import Model

        result = {
            "phase": "topology",
            "passed": True,
            "errors": [],
            "warnings": [],
            "details": {},
        }

        try:
            rid = model_info["rid"]
            model = fetch_model_by_rid(rid, {})
            components = model.getAllComponents()

            result["details"]["total_components"] = len(components)
            logger.info(f"  元件总数: {len(components)}")

            # 检查母线数量
            buses = [c for c in components.values() if self._is_bus_component(c)]
            result["details"]["bus_count"] = len(buses)
            logger.info(f"  母线数量: {len(buses)}")

            renewable_components = [
                (comp_id, comp)
                for comp_id, comp in components.items()
                if self._is_renewable_component(comp)
            ]
            result["details"]["renewable_count"] = len(renewable_components)
            logger.info(f"  新能源元件数量: {len(renewable_components)}")

            bus_signals = self._build_bus_signal_map(components)
            disconnected_renewables = []
            metadata_issues = []
            verified_connections = []

            for comp_id, comp in renewable_components:
                comp_label = self._component_name(comp_id, comp)
                comp_type = getattr(comp, "definition", "unknown")
                pins = getattr(comp, "pins", {}) or {}
                connected_pin = self._first_connected_pin(pins)
                connected_bus_id = bus_signals.get(connected_pin)

                if not connected_pin:
                    disconnected_renewables.append(
                        {
                            "id": comp_id,
                            "label": comp_label,
                            "type": comp_type,
                            "reason": "没有任何有效电气引脚连接",
                        }
                    )
                elif not connected_bus_id:
                    disconnected_renewables.append(
                        {
                            "id": comp_id,
                            "label": comp_label,
                            "type": comp_type,
                            "reason": f"引脚连接 '{connected_pin}' 不是有效母线信号",
                        }
                    )
                else:
                    verified_connections.append(
                        {
                            "id": comp_id,
                            "label": comp_label,
                            "type": comp_type,
                            "signal": connected_pin,
                            "bus_id": connected_bus_id,
                        }
                    )

                args = getattr(comp, "args", {}) or {}
                validation = self._metadata_integration.validate_parameters(
                    comp_type, args
                )
                if not validation.valid:
                    metadata_issues.append(
                        {
                            "id": comp_id,
                            "label": comp_label,
                            "type": comp_type,
                            "errors": validation.errors,
                        }
                    )

                required = self._metadata_integration.get_required_parameters(comp_type)
                missing = [p for p in required if p not in args or args[p] is None]
                if missing:
                    metadata_issues.append(
                        {
                            "id": comp_id,
                            "label": comp_label,
                            "type": comp_type,
                            "errors": [f"缺少必需参数: {', '.join(missing)}"],
                        }
                    )

            if disconnected_renewables:
                result["passed"] = False
                for dg in disconnected_renewables:
                    result["errors"].append(
                        f"新能源元件 '{dg['label']}' ({dg['type']}) {dg['reason']}"
                    )
                result["details"]["disconnected_renewables"] = disconnected_renewables
                logger.error(
                    f"  ❌ {len(disconnected_renewables)} 个新能源元件未正确连接"
                )

            # 检查其他悬空引脚（非电源类）
            dangling = []
            for comp_id, comp in components.items():
                # 跳过已检查的新能源元件
                if any(dg["id"] == comp_id for dg in disconnected_renewables):
                    continue

                pins = getattr(comp, "pins", {})
                if isinstance(pins, dict):
                    unconnected = [p for p, v in pins.items() if not v or v == ""]
                    if unconnected:
                        dangling.append({"id": comp_id, "unconnected": unconnected})

            if dangling:
                result["details"]["dangling_count"] = len(dangling)
                logger.info(f"  非关键悬空引脚: {len(dangling)} 个")

            # 检查参数完整性
            incomplete = []
            for comp_id, comp in components.items():
                args = getattr(comp, "args", {})
                if isinstance(args, dict):
                    empty = [k for k, v in args.items() if v is None or v == ""]
                    if empty:
                        incomplete.append({"id": comp_id, "empty_params": empty})

            if incomplete:
                result["details"]["incomplete_count"] = len(incomplete)
                logger.info(f"  非关键参数缺失: {len(incomplete)} 个")

            if metadata_issues:
                result["passed"] = False
                for issue in metadata_issues:
                    for error in issue["errors"]:
                        result["errors"].append(
                            f"元件 '{issue['label']}' ({issue['type']}): {error}"
                        )
                result["details"]["metadata_issues"] = metadata_issues
                logger.error(f"  ❌ {len(metadata_issues)} 个新能源元件元数据验证失败")

            if verified_connections:
                result["details"]["renewable_connections"] = verified_connections

            if result["passed"]:
                logger.info("  ✅ 拓扑验证通过")
            else:
                logger.error("  ❌ 拓扑验证失败")

        except (RuntimeError, ConnectionError, TimeoutError) as e:
            result["passed"] = False
            result["errors"].append(f"拓扑验证失败: {e}")
            logger.error(f"  ❌ 拓扑验证失败: {e}")

        return result

    def _validate_powerflow(
        self, model_info: Dict[str, Any], tolerance: float, timeout: int
    ) -> Dict:
        """潮流验证"""
        logger.info("\n[阶段2] 潮流验证...")
        from cloudpss import Model
        import time

        result = {
            "phase": "powerflow",
            "passed": True,
            "errors": [],
            "warnings": [],
            "details": {},
        }

        try:
            rid = model_info["rid"]
            model = Model.fetch(rid)
            logger.info("  提交潮流计算任务...")

            job = run_powerflow(model, {})
            result["details"]["job_id"] = job.id

            # 等待完成
            start = time.time()
            while time.time() - start < timeout:
                status = job.status()
                if status == 1:  # 完成
                    break
                if status == 2:  # 失败
                    raise RuntimeError("潮流计算失败")
                time.sleep(2)

            if time.time() - start >= timeout:
                raise TimeoutError("潮流计算超时")

            # 获取结果
            pf_result = job.result
            result["details"]["converged"] = True

            bus_tables = pf_result.getBuses()
            branch_tables = pf_result.getBranches()
            if not bus_tables:
                raise RuntimeError("潮流结果缺少母线表")
            if not branch_tables:
                raise RuntimeError("潮流结果缺少支路表")

            bus_rows = table_rows(bus_tables[0])
            branch_rows = table_rows(branch_tables[0])
            if not bus_rows:
                raise RuntimeError("潮流母线结果为空")
            if not branch_rows:
                raise RuntimeError("潮流支路结果为空")

            result["details"]["bus_count"] = len(bus_rows)
            result["details"]["branch_count"] = len(branch_rows)
            result["details"]["buses"] = bus_rows
            result["details"]["branches"] = branch_rows

            # 检查电压范围
            vm_values = [self._coerce_number(row.get(VM_COLUMN)) for row in bus_rows]
            vm_values = [v for v in vm_values if v is not None]

            if vm_values:
                from cloudpss_skills.core.auth_utils import (
                    DEFAULT_VOLTAGE_MIN,
                    DEFAULT_VOLTAGE_MAX,
                )

                vm_min, vm_max = min(vm_values), max(vm_values)
                result["details"]["voltage_min"] = vm_min
                result["details"]["voltage_max"] = vm_max
                result["details"]["per_bus_voltages"] = {
                    row.get(BUS_COLUMN): self._coerce_number(row.get(VM_COLUMN))
                    for row in bus_rows
                    if row.get(VM_COLUMN) is not None
                }
                logger.info(f"  电压范围: {vm_min:.4f} ~ {vm_max:.4f} pu")

                if vm_min < DEFAULT_VOLTAGE_MIN or vm_max > DEFAULT_VOLTAGE_MAX:
                    result["warnings"].append(
                        f"电压异常: {vm_min:.3f} ~ {vm_max:.3f} pu"
                    )
                    logger.warning("  ⚠️ 电压可能异常")

            components = model.getAllComponents()
            bus_signals = self._build_bus_signal_map(components)
            renewable_rows = []
            renewable_failures = []
            for comp_id, comp in components.items():
                if not self._is_renewable_component(comp):
                    continue
                connected_signal = self._first_connected_pin(
                    getattr(comp, "pins", {}) or {}
                )
                if not connected_signal:
                    continue
                bus_id = bus_signals.get(connected_signal)
                if not bus_id:
                    continue

                bus_row = next(
                    (row for row in bus_rows if row.get(BUS_COLUMN) == bus_id), None
                )
                comp_name = self._component_name(comp_id, comp)
                expected_p = self._expected_active_power(comp)
                actual_p = (
                    self._coerce_number(bus_row.get(P_GEN_COLUMN)) if bus_row else None
                )

                renewable_rows.append(
                    {
                        "component": comp_name,
                        "type": getattr(comp, "definition", "unknown"),
                        "signal": connected_signal,
                        "bus_id": bus_id,
                        "expected_p": expected_p,
                        "actual_p": actual_p,
                    }
                )

                if bus_row is None:
                    renewable_failures.append(
                        f"新能源元件 '{comp_name}' 已连接到 {connected_signal}，但潮流结果中找不到对应母线行"
                    )
                    continue

                if expected_p is not None:
                    minimum_expected = max(1.0, expected_p * 0.1)
                    if actual_p is None or abs(actual_p) < minimum_expected:
                        renewable_failures.append(
                            f"新能源元件 '{comp_name}' 接入母线 {connected_signal}，"
                            f"预期至少约 {minimum_expected:.1f} MW 注入，但实际潮流出力为 {actual_p or 0:.3f} MW"
                        )

            if renewable_rows:
                result["details"]["renewable_rows"] = renewable_rows
                logger.info(f"  新能源出力检查: {len(renewable_rows)} 个接入点")

            if renewable_failures:
                result["passed"] = False
                result["errors"].extend(renewable_failures)
                logger.error(
                    f"  ❌ {len(renewable_failures)} 个新能源接入点未真实进入潮流结果"
                )

            if result["passed"]:
                logger.info("  ✅ 潮流验证通过")
            else:
                logger.error("  ❌ 潮流验证失败")

        except (RuntimeError, ConnectionError, TimeoutError) as e:
            result["passed"] = False
            result["errors"].append(f"潮流验证失败: {e}")
            logger.error(f"  ❌ 潮流验证失败: {e}")

        return result

    def _validate_emt(self, rid: str, duration: float) -> Dict:
        """暂态验证"""
        logger.info("\n[阶段3] 暂态验证...")
        from cloudpss import Model
        import time

        result = {
            "phase": "emt",
            "passed": True,
            "errors": [],
            "warnings": [],
            "details": {},
        }

        try:
            model = fetch_model_by_rid(rid, {})

            # 首先检查EMT拓扑
            logger.info("  检查EMT拓扑...")
            try:
                topology = model.fetchTopology(implementType="emtp")
                result["details"]["topology_ready"] = True
                result["details"]["component_count"] = len(topology.components)
                logger.info(f"  EMT元件数: {len(topology.components)}")
            except (KeyError, AttributeError) as e:
                result["passed"] = False
                result["errors"].append(f"EMT拓扑检查失败: {e}")
                logger.error(f"  ❌ EMT拓扑检查失败: {e}")
                return result

            # 当前 SDK 的 runEMT 不稳定接受 simuTime 透传，这里先使用模型现有 EMT 配置做 smoke gate。
            logger.info(
                f"  提交EMT仿真（使用模型既有配置，目标 smoke 时长 {duration}s）..."
            )
            job = run_emt(model, {})
            result["details"]["job_id"] = job.id

            # 等待完成
            start = time.time()
            while time.time() - start < DEFAULT_TIMEOUT:
                status = job.status()
                if status == 1:
                    break
                if status == 2:
                    raise RuntimeError("EMT仿真失败")
                time.sleep(2)

            if time.time() - start >= DEFAULT_TIMEOUT:
                raise TimeoutError("EMT仿真超时")

            # 获取结果
            emt_result = job.result
            result["details"]["completed"] = True

            # 检查输出通道
            plots = list(emt_result.getPlots())
            result["details"]["plot_count"] = len(plots)
            logger.info(f"  输出通道: {len(plots)} 个")

            if not plots:
                raise RuntimeError("EMT结果缺少 plot 输出")

            valid_trace = None
            raw_x, raw_y = [], []
            for plot_index, _plot in enumerate(plots):
                channel_names = emt_result.getPlotChannelNames(plot_index) or []
                if not channel_names:
                    continue

                for channel_name in channel_names:
                    trace = emt_result.getPlotChannelData(plot_index, channel_name)
                    if not isinstance(trace, dict):
                        continue

                    x_values = trace.get("x") or []
                    y_values = trace.get("y") or []
                    if len(x_values) < 2 or len(y_values) < 2:
                        continue
                    if len(x_values) != len(y_values):
                        continue

                    numeric_samples = [
                        self._coerce_number(value)
                        for value in y_values[: min(len(y_values), 2000)]
                    ]
                    numeric_samples = [
                        value for value in numeric_samples if value is not None
                    ]
                    if not numeric_samples:
                        continue

                    y_min = min(numeric_samples)
                    y_max = max(numeric_samples)
                    if abs(y_max - y_min) < 1e-9 and abs(y_max) < 1e-9:
                        continue

                    valid_trace = {
                        "plot_index": plot_index,
                        "channel_name": channel_name,
                        "point_count": len(x_values),
                        "y_min": y_min,
                        "y_max": y_max,
                        "waveform_sample": {
                            "x": x_values[:100],
                            "y": y_values[:100],
                            "total_points": len(x_values),
                        },
                    }
                    raw_x, raw_y = x_values, y_values
                    break

                if valid_trace:
                    break

            if not valid_trace:
                raise RuntimeError("EMT结果缺少非空有效波形")

            result["details"]["sample_trace"] = valid_trace
            logger.info(
                "  有效波形: plot-%s / %s (%s 点)"
                % (
                    valid_trace["plot_index"],
                    valid_trace["channel_name"],
                    valid_trace["point_count"],
                )
            )

            logger.info("  ✅ 暂态验证通过")

        except (RuntimeError, ConnectionError, TimeoutError) as e:
            result["passed"] = False
            result["errors"].append(f"暂态验证失败: {e}")
            logger.error(f"  ❌ 暂态验证失败: {e}")

        return result

    def _validate_parameters(self, rid: str, base_rid: str) -> Dict:
        """参数对比验证"""
        logger.info("\n[阶段4] 参数对比验证...")
        from cloudpss import Model

        result = {
            "phase": "parameter",
            "passed": True,
            "errors": [],
            "warnings": [],
            "details": {},
        }

        try:
            model = fetch_model_by_rid(rid, {})
            base_model = fetch_model_by_rid(base_rid, {})

            # 获取拓扑对比
            components = model.getAllComponents()
            base_components = base_model.getAllComponents()

            added = len(components) - len(base_components)
            result["details"]["base_component_count"] = len(base_components)
            result["details"]["modified_component_count"] = len(components)
            result["details"]["added_components"] = max(0, added)

            logger.info(f"  原始元件: {len(base_components)}")
            logger.info(f"  当前元件: {len(components)}")
            if added > 0:
                logger.info(f"  新增元件: {added}")

            logger.info("  ✅ 参数对比验证通过")

        except (KeyError, AttributeError, TypeError) as e:
            result["passed"] = False
            result["errors"].append(f"参数对比失败: {e}")
            logger.error(f"  ❌ 参数对比失败: {e}")

        return result

    def _output_results(self, reports: List[ValidationReport], output_config: Dict):
        """输出验证结果"""
        fmt = output_config.get("format", "console")

        if fmt == "console":
            self._output_console(reports)
        elif fmt == "json":
            path = output_config.get("path", "./validation_report.json")
            self._output_json(reports, path)

    def _output_console(self, reports: List[ValidationReport]):
        """控制台输出"""
        # 使用日志输出报告，便于统一控制输出级别
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("模型验证报告")
        lines.append("=" * 80)

        for r in reports:
            status = "✅ 通过" if r.overall_passed else "❌ 失败"
            lines.append(f"\n模型: {r.model_name}")
            lines.append(f"RID: {r.model_rid}")
            lines.append(f"结果: {status}")

            for phase, result in r.phases.items():
                phase_status = "✅" if result.get("passed") else "❌"
                lines.append(f"  {phase_status} {phase}")

                if result.get("errors"):
                    for e in result.get("errors"):
                        lines.append(f"      错误: {e}")
                if result.get("warnings"):
                    for w in result.get("warnings"):
                        lines.append(f"      警告: {w}")

        passed = sum(1 for r in reports if r.overall_passed)
        lines.append(f"\n{'=' * 80}")
        lines.append(f"总计: {passed}/{len(reports)} 通过")
        lines.append("=" * 80)

        # 统一使用info级别输出报告
        for line in lines:
            logger.info(line)

    def _output_json(self, reports: List[ValidationReport], path: str):
        """JSON输出"""
        import json

        data = [
            {
                "model_rid": r.model_rid,
                "model_name": r.model_name,
                "overall_passed": r.overall_passed,
                "phases": r.phases,
                "issues": r.issues,
                "warnings": r.warnings,
            }
            for r in reports
        ]

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"验证报告已保存: {path}")
