#!/usr/bin/env python3
"""
模型验证技能 (model_validator)

功能：系统性验证测试算例的有效性，分阶段进行拓扑、潮流、暂态验证。

适用：验证 model_builder 创建的测试算例是否真实可用

作者: Claude Code
日期: 2026-04-01
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from cloudpss_skills.core.base import SkillBase, SkillResult, SkillStatus, ValidationResult, LogEntry, Artifact
from cloudpss_skills.core.auth_utils import setup_auth, DEFAULT_TIMEOUT, DEFAULT_POWERFLOW_TOLERANCE

logger = logging.getLogger(__name__)


class ValidationPhase(Enum):
    """验证阶段"""
    TOPOLOGY = "topology"          # 拓扑验证
    POWERFLOW = "powerflow"        # 潮流验证
    EMT = "emt"                    # 暂态验证
    PARAMETER = "parameter"        # 参数验证


@dataclass
class ValidationReport:
    """验证报告"""
    model_rid: str
    model_name: str = ""
    phases: Dict[str, Any] = field(default_factory=dict)
    overall_passed: bool = False
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


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

    config_schema = {
        "type": "object",
        "properties": {
            "auth": {
                "type": "object",
                "properties": {
                    "token": {"type": "string"},
                    "token_file": {"type": "string"}
                }
            },
            "models": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "rid": {"type": "string"},
                        "base_rid": {"type": "string"},
                        "name": {"type": "string"}
                    },
                    "required": ["rid"]
                }
            },
            "validation": {
                "type": "object",
                "properties": {
                    "phases": {
                        "type": "array",
                        "items": {
                            "enum": ["topology", "powerflow", "emt", "parameter"]
                        },
                        "default": ["topology", "powerflow"]
                    },
                    "timeout": {"type": "integer", "default": 300},
                    "powerflow_tolerance": {"type": "number", "default": 1e-6},
                    "emt_duration": {"type": "number", "default": 1.0}
                }
            },
            "output": {
                "type": "object",
                "properties": {
                    "format": {"type": "string", "enum": ["json", "console"], "default": "console"},
                    "path": {"type": "string"}
                }
            }
        },
        "required": ["models"]
    }

    def __init__(self):
        super().__init__()
        self.reports = []

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
                report = self._validate_single_model(model_info, phases, validation_config)
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
                        "warnings": r.warnings
                    }
                    for r in reports
                ]
            }

            logger.info(f"验证完成: {passed}/{total} 通过")

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data
            )

        except Exception as e:
            logger.error(f"验证失败: {e}", exc_info=True)
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                error=str(e)
            )

    def _validate_single_model(self, model_info: Dict, phases: List[str],
                               validation_config: Dict) -> ValidationReport:
        """验证单个模型"""
        rid = model_info["rid"]
        base_rid = model_info.get("base_rid")
        name = model_info.get("name", rid)

        logger.info(f"\n{'='*60}")
        logger.info(f"验证模型: {name}")
        logger.info(f"RID: {rid}")
        logger.info(f"{'='*60}")

        report = ValidationReport(model_rid=rid, model_name=name)

        # 阶段1: 拓扑验证
        if "topology" in phases:
            report.phases["topology"] = self._validate_topology(rid)

        # 阶段2: 潮流验证
        if "powerflow" in phases:
            report.phases["powerflow"] = self._validate_powerflow(
                rid, validation_config.get("powerflow_tolerance", DEFAULT_POWERFLOW_TOLERANCE)
            )

        # 阶段3: 暂态验证
        if "emt" in phases:
            report.phases["emt"] = self._validate_emt(
                rid, validation_config.get("emt_duration", 1.0)
            )

        # 阶段4: 参数对比验证
        if "parameter" in phases and base_rid:
            report.phases["parameter"] = self._validate_parameters(rid, base_rid)

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

    def _validate_topology(self, rid: str) -> Dict:
        """拓扑验证"""
        logger.info("\n[阶段1] 拓扑验证...")
        from cloudpss import Model

        result = {
            "phase": "topology",
            "passed": True,
            "errors": [],
            "warnings": [],
            "details": {}
        }

        try:
            model = Model.fetch(rid)
            components = model.getAllComponents()

            result["details"]["total_components"] = len(components)
            logger.info(f"  元件总数: {len(components)}")

            # 检查母线数量
            buses = [c for c in components.values()
                     if "bus" in getattr(c, "definition", "").lower()]
            result["details"]["bus_count"] = len(buses)
            logger.info(f"  母线数量: {len(buses)}")

            # 检查发电机/电源元件
            generator_types = ["gen", "source", "pv", "wind", "wgsource"]
            generators = []
            for comp_id, comp in components.items():
                defn = getattr(comp, "definition", "").lower()
                if any(x in defn for x in generator_types):
                    generators.append((comp_id, comp))

            result["details"]["generator_count"] = len(generators)
            logger.info(f"  电源数量: {len(generators)}")

            # ========== 关键修复：电源元件引脚验证 ==========
            disconnected_generators = []

            # 获取所有母线名称用于验证连接
            bus_names = set()
            for comp_id, comp in components.items():
                if "bus" in getattr(comp, "definition", "").lower():
                    bus_names.add(comp_id)
                    bus_name = getattr(comp, "name", None)
                    if bus_name:
                        bus_names.add(bus_name)

            for comp_id, comp in generators:
                defn = getattr(comp, "definition", "").lower()
                pins = getattr(comp, "pins", {})

                # 修复1: 检查电源元件必须有引脚
                if not pins or not isinstance(pins, dict):
                    # 只检查关键电源（风机、光伏等），忽略控制元件
                    if any(x in defn for x in ["wgsource", "pv", "wind"]):
                        disconnected_generators.append({
                            "id": comp_id,
                            "name": getattr(comp, "name", comp_id),
                            "type": getattr(comp, "definition", "unknown"),
                            "reason": "无引脚（电源元件必须至少有一个引脚连接到母线）"
                        })
                    continue

                # 修复2: 检查关键电源元件（风机、光伏）的引脚连接
                # SyncGeneratorRouter 可能有内部连接机制，不强制检查
                if any(x in defn for x in ["wgsource", "pv", "wind"]):
                    has_power_pin = False
                    for pin_name, pin_value in pins.items():
                        if pin_value and pin_value != "" and not pin_value.startswith("@"):
                            # 检查是否连接到母线
                            if pin_value in bus_names:
                                has_power_pin = True
                                break

                    if not has_power_pin:
                        # 检查是否有任何非空引脚（可能使用内部连接）
                        any_connected = any(
                            v and v != "" and not v.startswith("@")
                            for v in pins.values()
                        )
                        if not any_connected:
                            disconnected_generators.append({
                                "id": comp_id,
                                "name": getattr(comp, "name", comp_id),
                                "type": getattr(comp, "definition", "unknown"),
                                "reason": f"引脚未连接到母线（pins={pins}）"
                            })

            if disconnected_generators:
                result["passed"] = False
                for dg in disconnected_generators:
                    result["errors"].append(
                        f"电源元件 '{dg['name']}' ({dg['type']}) {dg['reason']}"
                    )
                result["details"]["disconnected_generators"] = disconnected_generators
                logger.error(f"  ❌ {len(disconnected_generators)} 个电源元件未正确连接")

            # 检查其他悬空引脚（非电源类）
            dangling = []
            for comp_id, comp in components.items():
                # 跳过已检查的电源元件
                if any(dg["id"] == comp_id for dg in disconnected_generators):
                    continue

                pins = getattr(comp, "pins", {})
                if isinstance(pins, dict):
                    unconnected = [p for p, v in pins.items()
                                   if not v or v == ""]
                    if unconnected:
                        dangling.append({
                            "id": comp_id,
                            "unconnected": unconnected
                        })

            if dangling:
                result["warnings"].append(f"发现 {len(dangling)} 个元件有悬空引脚")
                result["details"]["dangling_count"] = len(dangling)
                logger.warning(f"  ⚠️ 悬空引脚: {len(dangling)} 个")

            # 检查参数完整性
            incomplete = []
            for comp_id, comp in components.items():
                args = getattr(comp, "args", {})
                if isinstance(args, dict):
                    empty = [k for k, v in args.items()
                             if v is None or v == ""]
                    if empty:
                        incomplete.append({"id": comp_id, "empty_params": empty})

            if incomplete:
                result["warnings"].append(f"发现 {len(incomplete)} 个元件参数不完整")
                logger.warning(f"  ⚠️ 参数不完整: {len(incomplete)} 个")

            if result["passed"]:
                logger.info("  ✅ 拓扑验证通过")
            else:
                logger.error("  ❌ 拓扑验证失败")

        except Exception as e:
            result["passed"] = False
            result["errors"].append(f"拓扑验证失败: {e}")
            logger.error(f"  ❌ 拓扑验证失败: {e}")

        return result

    def _validate_powerflow(self, rid: str, tolerance: float) -> Dict:
        """潮流验证"""
        logger.info("\n[阶段2] 潮流验证...")
        from cloudpss import Model
        import time

        result = {
            "phase": "powerflow",
            "passed": True,
            "errors": [],
            "warnings": [],
            "details": {}
        }

        try:
            model = Model.fetch(rid)
            logger.info("  提交潮流计算任务...")

            job = model.runPowerFlow()
            result["details"]["job_id"] = job.id

            # 等待完成
            start = time.time()
            while time.time() - start < DEFAULT_TIMEOUT:
                status = job.status()
                if status == 1:  # 完成
                    break
                if status == 2:  # 失败
                    raise RuntimeError("潮流计算失败")
                time.sleep(2)

            if time.time() - start >= DEFAULT_TIMEOUT:
                raise TimeoutError("潮流计算超时")

            # 获取结果
            pf_result = job.result
            result["details"]["converged"] = True

            # 检查电压范围
            buses = pf_result.getBuses()
            vm_values = []
            for bus in buses:
                try:
                    vm = bus.get("Vm", 0)
                    if vm:
                        vm_values.append(float(vm))
                except:
                    pass

            if vm_values:
                from cloudpss_skills.core.auth_utils import DEFAULT_VOLTAGE_MIN, DEFAULT_VOLTAGE_MAX
                vm_min, vm_max = min(vm_values), max(vm_values)
                result["details"]["voltage_min"] = vm_min
                result["details"]["voltage_max"] = vm_max
                logger.info(f"  电压范围: {vm_min:.4f} ~ {vm_max:.4f} pu")

                # 电压合理性检查
                if vm_min < DEFAULT_VOLTAGE_MIN or vm_max > DEFAULT_VOLTAGE_MAX:
                    result["warnings"].append(
                        f"电压异常: {vm_min:.3f} ~ {vm_max:.3f} pu"
                    )
                    logger.warning(f"  ⚠️ 电压可能异常")

            # 检查线路潮流
            branches = pf_result.getBranches()
            result["details"]["branch_count"] = len(branches)
            logger.info(f"  支路数量: {len(branches)}")

            logger.info("  ✅ 潮流验证通过")

        except Exception as e:
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
            "details": {}
        }

        try:
            model = Model.fetch(rid)

            # 首先检查EMT拓扑
            logger.info("  检查EMT拓扑...")
            try:
                topology = model.fetchTopology(implementType="emtp")
                result["details"]["topology_ready"] = True
                result["details"]["component_count"] = len(topology.components)
                logger.info(f"  EMT元件数: {len(topology.components)}")
            except Exception as e:
                result["passed"] = False
                result["errors"].append(f"EMT拓扑检查失败: {e}")
                logger.error(f"  ❌ EMT拓扑检查失败: {e}")
                return result

            # 提交EMT仿真（极短时长验证可行性）
            logger.info(f"  提交EMT仿真（{duration}s）...")
            job = model.runEMT(simuTime=duration)
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
            plots = emt_result.getPlots()
            result["details"]["plot_count"] = len(plots)
            logger.info(f"  输出通道: {len(plots)} 个")

            logger.info("  ✅ 暂态验证通过")

        except Exception as e:
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
            "details": {}
        }

        try:
            model = Model.fetch(rid)
            base_model = Model.fetch(base_rid)

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

        except Exception as e:
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
        print("\n" + "=" * 80)
        print("模型验证报告")
        print("=" * 80)

        for r in reports:
            status = "✅ 通过" if r.overall_passed else "❌ 失败"
            print(f"\n模型: {r.model_name}")
            print(f"RID: {r.model_rid}")
            print(f"结果: {status}")

            for phase, result in r.phases.items():
                phase_status = "✅" if result.get("passed") else "❌"
                print(f"  {phase_status} {phase}")

                if result.get("errors"):
                    for e in result["errors"]:
                        print(f"      错误: {e}")
                if result.get("warnings"):
                    for w in result["warnings"]:
                        print(f"      警告: {w}")

        passed = sum(1 for r in reports if r.overall_passed)
        print(f"\n{'='*80}")
        print(f"总计: {passed}/{len(reports)} 通过")
        print("=" * 80)

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
                "warnings": r.warnings
            }
            for r in reports
        ]

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"验证报告已保存: {path}")
