#!/usr/bin/env python3
"""
新能源接入评估技能 (renewable_integration)

功能：评估新能源（光伏/风电）接入电网的影响，包括短路比(SCR)计算、
      电压波动、谐波注入、低电压穿越(LVRT)合规性、稳定性影响等。

适用：新能源并网评估、弱电网分析、电能质量评估

作者: Claude Code
日期: 2026-04-01
"""

import logging
import math
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from copy import deepcopy

import numpy as np

from cloudpss_skills.core.base import SkillBase, SkillResult, SkillStatus, ValidationResult
from cloudpss_skills.core.auth_utils import setup_auth, DEFAULT_TIMEOUT
from cloudpss_skills.core.registry import register
from cloudpss_skills.core.network_equivalent import compute_positive_sequence_zth, normalize_bus_name
from cloudpss_skills.core.utils import parse_cloudpss_table

logger = logging.getLogger(__name__)


@dataclass
class RenewableIntegrationReport:
    """新能源接入评估报告"""
    model_rid: str
    renewable_type: str  # PV/Wind
    capacity_mw: float
    scr: float  # 短路比
    voltage_variation: Dict[str, float]
    harmonic_distortion: Dict[str, float]
    lvrt_compliant: bool
    stability_impact: Dict[str, Any]


@register
class RenewableIntegrationSkill(SkillBase):
    """
    新能源接入评估技能

    功能特性:
    1. 短路比(SCR)计算 - 评估电网强度
    2. 电压波动分析 - 评估电压变化范围
    3. 谐波注入评估 - 分析谐波影响
    4. 低电压穿越(LVRT)验证 - 检查并网合规性
    5. 稳定性影响评估 - 频率/电压/暂态稳定性

    配置示例:
        skill: renewable_integration

        model:
          rid: model/holdme/test_IEEE39_with_PV_100MW

        renewable:
          type: pv  # pv/wind
          bus: BUS_10
          capacity: 100  # MW

        analysis:
          scr:
            enabled: true
            threshold: 3.0  # SCR阈值
          voltage_variation:
            enabled: true
            tolerance: 0.05  # 5%电压偏差容忍度
          harmonic_injection:
            enabled: true
            limits:
              thd: 0.05  # 5% THD限值
          lvrt_compliance:
            enabled: true
            standard: gb  # gb/ieee/iec
          stability_impact:
            enabled: true

        output:
          format: json
          path: ./renewable_integration_report.json
    """

    name = "renewable_integration"
    description = "新能源接入评估(SCR/电压波动/谐波/LVRT/稳定性)"
    version = "1.0.0"

    config_schema = {
        "type": "object",
        "required": ["skill", "model"],
        "properties": {
            "skill": {"type": "string", "const": "renewable_integration"},
            "auth": {
                "type": "object",
                "properties": {
                    "token": {"type": "string"},
                    "token_file": {"type": "string", "default": ".cloudpss_token"}
                }
            },
            "model": {
                "type": "object",
                "required": ["rid"],
                "properties": {
                    "rid": {"type": "string"},
                    "source": {"enum": ["cloud", "local"], "default": "cloud"}
                }
            },
            "renewable": {
                "type": "object",
                "properties": {
                    "type": {"enum": ["pv", "wind"], "default": "pv"},
                    "bus": {"type": "string"},
                    "capacity": {"type": "number", "description": "额定容量(MW)"}
                }
            },
            "analysis": {
                "type": "object",
                "properties": {
                    "scr": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean", "default": True},
                            "threshold": {"type": "number", "default": 3.0}
                        }
                    },
                    "voltage_variation": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean", "default": True},
                            "tolerance": {"type": "number", "default": 0.05}
                        }
                    },
                    "harmonic_injection": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean", "default": True},
                            "limits": {
                                "type": "object",
                                "properties": {
                                    "thd": {"type": "number", "default": 0.05}
                                }
                            }
                        }
                    },
                    "lvrt_compliance": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean", "default": True},
                            "standard": {"enum": ["gb", "ieee", "iec"], "default": "gb"}
                        }
                    },
                    "stability_impact": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean", "default": True}
                        }
                    }
                }
            },
            "output": {
                "type": "object",
                "properties": {
                    "format": {"enum": ["json", "console"], "default": "json"},
                    "path": {"type": "string"}
                }
            }
        }
    }

    def validate(self, config: Dict) -> ValidationResult:
        """验证配置"""
        errors = []
        warnings = []

        model = config.get("model", {})
        if not model.get("rid"):
            errors.append("必须指定 model.rid")

        renewable = config.get("renewable", {})
        if not renewable.get("capacity"):
            warnings.append("建议指定 renewable.capacity (额定容量)；若模型内可识别新能源元件，将优先读取模型实际容量")

        return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)

    def run(self, config: Dict) -> SkillResult:
        """执行新能源接入评估"""
        start_time = datetime.now()

        try:
            setup_auth(config)

            model_config = config.get("model", {})
            model_rid = model_config["rid"]

            analysis_config = config.get("analysis", {})

            logger.info(f"开始新能源接入评估: {model_rid}")

            report = {
                "model_rid": model_rid,
                "timestamp": datetime.now().isoformat(),
                "analysis_results": {}
            }

            # 1. 短路比(SCR)计算
            if analysis_config.get("scr", {}).get("enabled", True):
                logger.info("计算短路比(SCR)...")
                scr_result = self._calculate_scr(model_rid, config)
                report["analysis_results"]["scr"] = scr_result

            # 2. 电压波动分析
            if analysis_config.get("voltage_variation", {}).get("enabled", True):
                logger.info("分析电压波动...")
                voltage_result = self._analyze_voltage_variation(model_rid, config)
                report["analysis_results"]["voltage_variation"] = voltage_result

            # 3. 谐波注入评估
            if analysis_config.get("harmonic_injection", {}).get("enabled", True):
                logger.info("评估谐波注入...")
                harmonic_result = self._assess_harmonic_injection(model_rid, config)
                report["analysis_results"]["harmonic_injection"] = harmonic_result

            # 4. LVRT合规性验证
            if analysis_config.get("lvrt_compliance", {}).get("enabled", True):
                logger.info("验证低电压穿越(LVRT)...")
                lvrt_result = self._verify_lvrt_compliance(model_rid, config)
                report["analysis_results"]["lvrt_compliance"] = lvrt_result

            # 5. 稳定性影响评估
            if analysis_config.get("stability_impact", {}).get("enabled", True):
                logger.info("评估稳定性影响...")
                stability_result = self._assess_stability_impact(model_rid, config)
                report["analysis_results"]["stability_impact"] = stability_result

            # 生成结论
            report["summary"] = self._generate_summary(report["analysis_results"])

            # 输出结果
            self._output_results(report, config.get("output", {}))

            logger.info("新能源接入评估完成")

            # 只有在结论通过且所有分析都基于真实可验证结果时才允许成功
            summary = report.get("summary", {})
            certifiable = summary.get("certifiable", False)
            overall_passed = summary.get("overall_passed", False)
            final_status = SkillStatus.SUCCESS if certifiable and overall_passed else SkillStatus.FAILED
            error = None
            if not certifiable:
                error = "分析包含估算或假设结果，当前不能作为已验证的新能源接入评估结论"

            return SkillResult(
                skill_name=self.name,
                status=final_status,
                start_time=start_time,
                end_time=datetime.now(),
                data=report,
                error=error,
            )

        except (KeyError, AttributeError, TypeError, ValueError, RuntimeError) as e:
            logger.error(f"新能源接入评估失败: {e}", exc_info=True)
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                error=str(e)
            )

    def _calculate_scr(self, model_rid: str, config: Dict) -> Dict:
        """
        计算短路比(Short Circuit Ratio)

        SCR = S_sc / P_n
        其中 S_sc 是接入点的短路容量，P_n 是新能源额定功率

        SCR > 3: 强电网
        2 < SCR < 3: 中等强度电网
        SCR < 2: 弱电网
        """
        from cloudpss import Model

        renewable_config = config.get("renewable", {})
        renewable_bus = renewable_config.get("bus", "")

        model = Model.fetch(model_rid)
        zth_result = compute_positive_sequence_zth(model, renewable_bus)
        if not zth_result.verified:
            return {
                "error": zth_result.error or "无法计算PCC等值阻抗",
                "passed": False,
                "verified": False,
            }

        renewable_components = self._find_renewable_components(model, config)
        inferred_capacity_mw = self._infer_renewable_capacity_mw(model, renewable_components)
        configured_capacity_mw = renewable_config.get("capacity")
        capacity_mw = inferred_capacity_mw if inferred_capacity_mw is not None else configured_capacity_mw
        if capacity_mw is None:
            return {
                "error": "未提供 renewable.capacity，且无法从模型中识别新能源额定容量",
                "passed": False,
                "verified": False,
            }

        zth_pu = zth_result.z_th_pu
        bus_nominal_voltage = float(zth_result.bus_nominal_voltage_kv)
        system_base_mva = float(zth_result.system_base_mva)
        zth_mag = float(abs(zth_pu))
        short_circuit_capacity_mva = system_base_mva / zth_mag if zth_mag > 0 else float("inf")
        scr = short_circuit_capacity_mva / float(capacity_mw) if capacity_mw > 0 else float("inf")

        # 判断电网强度
        if scr >= 3:
            strength = "强电网"
            recommendation = "正常运行"
        elif scr >= 2:
            strength = "中等强度电网"
            recommendation = "建议增加无功补偿"
        else:
            strength = "弱电网"
            recommendation = "需要额外的电压支撑设备"

        return {
            "scr": round(scr, 2),
            "short_circuit_capacity_mva": round(short_circuit_capacity_mva, 2),
            "renewable_capacity_mw": float(capacity_mw),
            "configured_capacity_mw": configured_capacity_mw,
            "inferred_capacity_mw": inferred_capacity_mw,
            "bus_nominal_voltage_kv": bus_nominal_voltage,
            "z_th_pu": {
                "real": round(zth_pu.real, 6),
                "imag": round(zth_pu.imag, 6),
                "magnitude": round(abs(zth_pu), 6),
            },
            "bus_node": zth_result.bus_node,
            "grid_strength": strength,
            "recommendation": recommendation,
            "threshold": config.get("analysis", {}).get("scr", {}).get("threshold", 3.0),
            "passed": bool(scr >= config.get("analysis", {}).get("scr", {}).get("threshold", 3.0)),
            "calculation_method": "基于拓扑正序网络构造PCC戴维南等值阻抗",
            "verified": True,
        }

    def _infer_renewable_capacity_mw(self, model, renewable_components: List[str]) -> Optional[float]:
        total_capacity = 0.0
        found = False
        for component_key in renewable_components:
            try:
                comp = model.getComponentByKey(component_key)
            except Exception:
                continue
            args = getattr(comp, "args", {}) or {}
            for key in ("pf_P", "P_cmd", "Pnom", "Sn", "Smva"):
                value = args.get(key)
                if value is None:
                    continue
                try:
                    total_capacity += float(value)
                    found = True
                    break
                except Exception:
                    continue
        return total_capacity if found else None

    def _analyze_voltage_variation(self, model_rid: str, config: Dict) -> Dict:
        """
        分析电压波动
        对比新能源接入前后的电压变化
        """
        from cloudpss import Model
        import time

        model_with_renewable = Model.fetch(model_rid)
        renewable_components = self._find_renewable_components(model_with_renewable, config)
        if not renewable_components:
            return {
                "error": "未在模型中识别到可用于对比的新能源组件",
                "passed": False,
                "verified": False,
            }

        # 运行带新能源的潮流
        voltages_with = self._run_powerflow_and_extract_voltages(model_with_renewable)
        if not voltages_with:
            return {"error": "无法获取含新能源的电压数据", "passed": False, "verified": False}

        model_without_renewable = Model(deepcopy(model_with_renewable.toJSON()))
        for component_key in renewable_components:
            try:
                model_without_renewable.removeComponent(component_key)
            except Exception:
                model_without_renewable.updateComponent(component_key, props={"enabled": False})

        voltages_without = self._run_powerflow_and_extract_voltages(model_without_renewable)
        if not voltages_without:
            return {"error": "无法获取去除新能源后的电压数据", "passed": False, "verified": False}

        # 计算含新能源时的电压统计
        v_max_with = max(voltages_with)
        v_min_with = min(voltages_with)
        v_avg_with = sum(voltages_with) / len(voltages_with)

        v_max_without = max(voltages_without)
        v_min_without = min(voltages_without)
        v_avg_without = sum(voltages_without) / len(voltages_without)

        # 计算电压变化
        max_change = max(abs(v_max_with - v_max_without), abs(v_min_with - v_min_without))
        max_change_percent = max_change * 100

        tolerance = config.get("analysis", {}).get("voltage_variation", {}).get("tolerance", 0.05)

        return {
            "voltage_max_with_renewable_pu": round(v_max_with, 4),
            "voltage_min_with_renewable_pu": round(v_min_with, 4),
            "voltage_avg_with_renewable_pu": round(v_avg_with, 4),
            "voltage_max_without_renewable_pu": round(v_max_without, 4),
            "voltage_min_without_renewable_pu": round(v_min_without, 4),
            "voltage_avg_without_renewable_pu": round(v_avg_without, 4),
            "max_voltage_change_pu": round(max_change, 4),
            "max_voltage_change_percent": round(max_change_percent, 2),
            "tolerance_percent": tolerance * 100,
            "passed": max_change <= tolerance,
            "renewable_components_removed": renewable_components,
            "verified": True,
        }

    def _find_renewable_components(self, model, config: Dict) -> List[str]:
        renewable_type = config.get("renewable", {}).get("type", "pv").lower()
        renewable_bus = str(config.get("renewable", {}).get("bus", "")).lower()
        matched = []

        for key, comp in model.getAllComponents().items():
            definition = str(getattr(comp, "definition", "") or "").lower()
            label = str(getattr(comp, "label", "") or "").lower()
            pins = getattr(comp, "pins", {}) or {}

            if renewable_type == "pv":
                if not any(token in definition for token in ["pv", "pvs"]):
                    continue
            elif renewable_type == "wind":
                if not any(token in definition for token in ["wind", "wg", "wtg", "dfig"]):
                    continue

            if renewable_bus:
                pin_values = " ".join(str(v).lower() for v in pins.values())
                if renewable_bus not in label and renewable_bus not in pin_values:
                    continue

            matched.append(key)

        return matched

    def _run_powerflow_and_extract_voltages(self, model) -> List[float]:
        import time

        job = model.runPowerFlow()
        start = time.time()
        while time.time() - start < 60:
            status = job.status()
            if status == 1:
                break
            if status == 2:
                raise RuntimeError("潮流计算失败")
            time.sleep(1)

        return self._extract_voltages_from_result(job.result)

    def _extract_voltages_from_result(self, pf_result) -> list:
        """从潮流结果中提取电压列表"""
        buses = parse_cloudpss_table(pf_result.getBuses())
        voltages = []

        for bus in buses:
            for key in ("Vm", "Vm / pu", "Vmpu"):
                if key in bus:
                    try:
                        vm = float(bus.get(key, 0))
                        if vm > 0:
                            voltages.append(vm)
                            break
                    except Exception as e:
                        logger.debug(f"忽略预期异常: {e}")

        return voltages

    def _assess_harmonic_injection(self, model_rid: str, config: Dict) -> Dict:
        """评估谐波注入"""
        # 简化实现，实际应通过EMT仿真获取波形后FFT分析

        renewable_config = config.get("renewable", {})
        renewable_type = renewable_config.get("type", "pv")

        # 模拟谐波含量（基于典型值）
        if renewable_type == "pv":
            harmonics = {
                "h5": 3.0,  # 5次谐波
                "h7": 2.0,  # 7次谐波
                "h11": 1.5,  # 11次谐波
                "h13": 1.0   # 13次谐波
            }
        else:  # wind
            harmonics = {
                "h5": 2.0,
                "h7": 1.5,
                "h11": 1.0,
                "h13": 0.8
            }

        # 计算THD
        thd = sum([h**2 for h in harmonics.values()]) ** 0.5

        limit = config.get("analysis", {}).get("harmonic_injection", {}).get("limits", {}).get("thd", 0.05)

        return {
            "harmonics": harmonics,
            "thd_percent": round(thd, 2),
            "thd_limit_percent": limit * 100,
            "passed": thd / 100 <= limit,
            "warning": "此结果是基于典型值的简化估算，未进行实际仿真验证，仅供初步评估参考",
            "verified": False,
        }

    def _verify_lvrt_compliance(self, model_rid: str, config: Dict) -> Dict:
        """
        验证低电压穿越(LVRT)合规性

        根据国标GB/T 19964-2012或IEEE 1547标准验证
        """
        from cloudpss import Model

        standard = config.get("analysis", {}).get("lvrt_compliance", {}).get("standard", "gb")

        model = Model.fetch(model_rid)
        capability = self._detect_lvrt_capability(model, config)

        # LVRT要求曲线（简化）
        # GB标准：电压跌至20%时，至少维持625ms不脱网
        # 电压跌至0时，至少维持200ms

        lvrt_requirements = {
            "gb": {
                "name": "GB/T 19964-2012",
                "curve": [
                    {"voltage_percent": 0, "duration_ms": 200},
                    {"voltage_percent": 20, "duration_ms": 625},
                    {"voltage_percent": 90, "duration_ms": 2000}
                ]
            },
            "ieee": {
                "name": "IEEE 1547-2018",
                "curve": [
                    {"voltage_percent": 0, "duration_ms": 1000},
                    {"voltage_percent": 50, "duration_ms": 3000}
                ]
            }
        }

        req = lvrt_requirements.get(standard, lvrt_requirements["gb"])
        if not capability["supported"]:
            return {
                "standard": req["name"],
                "lvrt_curve": req["curve"],
                "supported": False,
                "compliant": False,
                "passed": False,
                "reason": capability["reason"],
                "warning": "当前模型未识别到LVRT控制/保护逻辑，不能开展有效LVRT测试",
                "verified": False,
            }

        executable = self._detect_lvrt_execution_path(model)
        if executable["supported"]:
            return self._run_lvrt_verification(model, config, req, capability, executable)

        return {
            "standard": req["name"],
            "lvrt_curve": req["curve"],
            "supported": True,
            "supported_components": capability["components"],
            "compliant": False,
            "passed": False,
            "notes": "模型具备LVRT相关控制/保护逻辑，但当前自动化链路尚未完成故障跌落与状态量测的闭环验证",
            "warning": "当前仅确认模型具备LVRT能力，尚未完成真实故障过程验证，不能宣称已通过LVRT测试",
            "verified": False,
        }

    def _detect_lvrt_capability(self, model, config: Dict) -> Dict[str, Any]:
        renewable_type = config.get("renewable", {}).get("type", "pv").lower()
        renewable_bus = str(config.get("renewable", {}).get("bus", "")).lower()
        supported_components = []

        lvrt_keywords = {
            "pv": ["pvs_01-avm-std", "pvstation", "pvs_01"],
            "wind": ["wtg_pmsg_01-avm-std", "wgsource", "dfig", "vrt_sd"],
        }
        lvrt_param_keys = {
            "Enable_LV", "VLin_LV", "VLout_LV", "TdlyVLin_LV", "TdlyVLout_LV",
            "TL1_LV", "VL1_LV", "TL2_LV", "VL2_LV", "LVRT_IN_PFLAG", "LVRT_IN_QFLAG",
            "TLVRT_RECOVER0_LV", "LVRTEnable", "LVRT_Startup", "FRTMode",
        }

        for key, comp in model.getAllComponents().items():
            definition = str(getattr(comp, "definition", "") or "").lower()
            label = str(getattr(comp, "label", "") or "").lower()
            pins = getattr(comp, "pins", {}) or {}
            args = getattr(comp, "args", {}) or {}
            infra_component = "vrt_sd" in definition or "vrt_fault" in definition

            if renewable_bus and not infra_component:
                if isinstance(pins, dict):
                    pin_iter = pins.values()
                elif isinstance(pins, list):
                    pin_iter = pins
                else:
                    pin_iter = []
                pin_values = " ".join(str(v).lower() for v in pin_iter)
                if renewable_bus not in label and renewable_bus not in pin_values:
                    continue

            if not infra_component and not any(token in definition for token in lvrt_keywords.get(renewable_type, [])):
                if not (set(args.keys()) & lvrt_param_keys):
                    continue

            supported_components.append({
                "key": key,
                "label": getattr(comp, "label", ""),
                "definition": getattr(comp, "definition", ""),
                "lvrt_param_keys": sorted(set(args.keys()) & lvrt_param_keys),
            })

        if supported_components:
            return {
                "supported": True,
                "components": supported_components,
            }

        return {
            "supported": False,
            "reason": "模型中未识别到具备LVRT控制/保护参数的新能源或变流器组件",
            "components": [],
        }

    def _detect_lvrt_execution_path(self, model) -> Dict[str, Any]:
        emt_job = next((j for j in model.jobs if j.get("rid") == "function/CloudPSS/emtps"), None)
        if not emt_job:
            return {"supported": False, "reason": "模型没有EMT仿真方案"}

        output_groups = emt_job.get("args", {}).get("output_channels", [])
        has_state_group = False
        has_voltage_group = False
        for group in output_groups:
            name = str(group.get("0", ""))
            if "电压穿越状态" in name:
                has_state_group = True
            if "并网点电压" in name:
                has_voltage_group = True

        fault_component_key = None
        for key, comp in model.getAllComponents().items():
            definition = str(getattr(comp, "definition", "") or "")
            if "VRT_Fault" in definition:
                fault_component_key = key
                break

        if fault_component_key and has_state_group and has_voltage_group:
            return {
                "supported": True,
                "fault_component_key": fault_component_key,
            }

        return {
            "supported": False,
            "reason": "模型缺少可自动触发的VRT故障模块或缺少State/Vrms_HV默认输出组",
        }

    def _run_lvrt_verification(self, model, config: Dict, req: Dict[str, Any], capability: Dict[str, Any], execution: Dict[str, Any]) -> Dict[str, Any]:
        from cloudpss import Model
        import time

        working = Model(deepcopy(model.toJSON()))
        fault_mode = str(config.get("analysis", {}).get("lvrt_compliance", {}).get("fault_mode", "1"))
        working.updateComponent(
            execution["fault_component_key"],
            args={"Fault_VRT": {"source": fault_mode, "ɵexp": ""}}
        )

        job = working.runEMT()
        start = time.time()
        while time.time() - start < 90:
            status = job.status()
            if status == 1:
                break
            if status == 2:
                raise RuntimeError("LVRT专项EMT仿真失败")
            time.sleep(2)

        result = job.result
        plots = list(result.getPlots())
        state_data = None
        voltage_data = None
        curve_data = None
        for plot_idx in range(len(plots)):
            names = result.getPlotChannelNames(plot_idx) or []
            for channel_name in names:
                if channel_name == "State:0":
                    state_data = result.getPlotChannelData(plot_idx, channel_name)
                elif channel_name == "Vrms_HV [p.u.]:0":
                    voltage_data = result.getPlotChannelData(plot_idx, channel_name)
                elif channel_name == "LVRT_Curve:0":
                    curve_data = result.getPlotChannelData(plot_idx, channel_name)

        if not state_data or not voltage_data:
            return {
                "standard": req["name"],
                "lvrt_curve": req["curve"],
                "supported": True,
                "supported_components": capability["components"],
                "compliant": False,
                "passed": False,
                "notes": "模型具备LVRT能力，但未能提取State或并网点电压输出",
                "warning": "LVRT状态量测链仍不完整，无法给出正式结论",
                "verified": False,
            }

        state_values = [float(v) for v in state_data.get("y", [])]
        voltage_values = [float(v) for v in voltage_data.get("y", [])]
        curve_values = [float(v) for v in curve_data.get("y", [])] if curve_data else []
        entered_lvrt = any(v <= -1.0 for v in state_values)
        tripped = any(v <= -3.0 for v in state_values)
        recovered = abs(state_values[-1]) < 1e-6 if state_values else False
        min_voltage = min(voltage_values) if voltage_values else None
        max_lvrt_curve = max(curve_values) if curve_values else None
        compliant = entered_lvrt and not tripped and recovered

        return {
            "standard": req["name"],
            "lvrt_curve": req["curve"],
            "supported": True,
            "supported_components": capability["components"],
            "fault_mode": fault_mode,
            "job_id": job.id,
            "state_summary": {
                "entered_lvrt": entered_lvrt,
                "tripped": tripped,
                "recovered": recovered,
                "min_state": min(state_values) if state_values else None,
                "max_state": max(state_values) if state_values else None,
                "final_state": state_values[-1] if state_values else None,
            },
            "voltage_summary": {
                "min_voltage_pu": min_voltage,
                "max_voltage_pu": max(voltage_values) if voltage_values else None,
                "max_lvrt_curve_pu": max_lvrt_curve,
            },
            "compliant": compliant,
            "passed": compliant,
            "verified": True,
        }

    def _assess_stability_impact(self, model_rid: str, config: Dict) -> Dict:
        """评估稳定性影响"""
        from cloudpss import Model

        model_with = Model.fetch(model_rid)
        renewable_components = self._find_renewable_components(model_with, config)
        if not renewable_components:
            return {
                "error": "未识别到新能源组件，无法评估接入前后稳定性影响",
                "verified": False,
            }

        voltages_with = self._run_powerflow_and_extract_voltages(model_with)

        model_without = Model(deepcopy(model_with.toJSON()))
        for component_key in renewable_components:
            try:
                model_without.removeComponent(component_key)
            except Exception:
                model_without.updateComponent(component_key, props={"enabled": False})

        voltages_without = self._run_powerflow_and_extract_voltages(model_without)

        if not voltages_with or not voltages_without:
            return {
                "error": "缺少接入前后潮流结果，无法评估稳定性影响",
                "verified": False,
            }

        min_with = min(voltages_with)
        min_without = min(voltages_without)
        avg_with = sum(voltages_with) / len(voltages_with)
        avg_without = sum(voltages_without) / len(voltages_without)
        min_delta = min_with - min_without
        avg_delta = avg_with - avg_without

        voltage_status = "improved" if min_delta > 0.002 else "degraded" if min_delta < -0.002 else "neutral"
        voltage_risk = "low" if min_with >= 0.95 else "medium" if min_with >= 0.90 else "high"

        stability_assessment = {
            "frequency_stability": {
                "status": "not_assessed",
                "risk": "unknown",
                "notes": "未运行频率扰动专项仿真，本项未评估"
            },
            "voltage_stability": {
                "status": voltage_status,
                "risk": voltage_risk,
                "notes": f"接入后最低电压变化 {min_delta:.4f} pu，平均电压变化 {avg_delta:.4f} pu"
            },
            "transient_stability": {
                "status": "not_assessed",
                "risk": "unknown",
                "notes": "未运行暂态故障扰动专项仿真，本项未评估"
            }
        }

        if voltage_risk == "high":
            overall_stability = "weak"
        elif voltage_status == "degraded":
            overall_stability = "acceptable"
        else:
            overall_stability = "good"

        return {
            "overall_stability": overall_stability,
            "assessments": stability_assessment,
            "recommendations": [
                "建议基于真实故障场景补充暂态稳定与LVRT专项校核",
                "建议持续跟踪接入点及薄弱母线的电压裕度"
            ],
            "renewable_components_removed": renewable_components,
            "passed": overall_stability != "weak",
            "verified": True,
        }

    def _generate_summary(self, analysis_results: Dict) -> Dict:
        """生成评估总结"""
        passed_count = sum(1 for r in analysis_results.values()
                          if isinstance(r, dict) and r.get("passed", False))
        total_count = len(analysis_results)

        overall_passed = all(r.get("passed", True) for r in analysis_results.values()
                            if isinstance(r, dict))
        overall_verified = all(r.get("verified", True) for r in analysis_results.values()
                              if isinstance(r, dict))

        assessment = "通过" if overall_passed and overall_verified else "仅供初步评估"

        return {
            "total_analysis": total_count,
            "passed": passed_count,
            "overall_passed": overall_passed,
            "overall_verified": overall_verified,
            "certifiable": overall_passed and overall_verified,
            "assessment": assessment,
            "recommendations": self._generate_recommendations(analysis_results),
            "limitations": [] if overall_verified else ["当前评估包含估算/假设结果，不能作为已完成真实并网验证的结论"],
        }

    def _generate_recommendations(self, analysis_results: Dict) -> List[str]:
        """生成建议"""
        recommendations = []
        if any(isinstance(result, dict) and not result.get("verified", True) for result in analysis_results.values()):
            recommendations.append("当前仍包含未完成真实仿真验证的分析项，建议补充短路、谐波和LVRT专项校核")

        scr = analysis_results.get("scr", {})
        if not scr.get("passed", True):
            recommendations.append("短路比偏低，建议增加无功补偿或加强电网连接")

        voltage = analysis_results.get("voltage_variation", {})
        if not voltage.get("passed", True):
            recommendations.append("电压波动较大，建议配置电压调节设备")

        harmonic = analysis_results.get("harmonic_injection", {})
        if not harmonic.get("passed", True):
            recommendations.append("谐波含量超标，建议配置滤波器")

        if not recommendations:
            recommendations.append("各项指标正常，新能源可以安全接入")

        return recommendations

    def _output_results(self, report: Dict, output_config: Dict):
        """输出结果"""
        fmt = output_config.get("format", "json")

        if fmt == "console":
            self._output_console(report)
        elif fmt == "json":
            import json
            path = output_config.get("path", "./renewable_integration_report.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"报告已保存: {path}")

    def _output_console(self, report: Dict):
        """控制台输出"""
        lines = []
        lines.append("\n" + "=" * 70)
        lines.append("新能源接入评估报告")
        lines.append("=" * 70)
        lines.append(f"模型: {report['model_rid']}")
        lines.append(f"时间: {report['timestamp']}")
        lines.append("\n评估结果:")

        for name, result in report["analysis_results"].items():
            lines.append(f"\n{name}:")
            if isinstance(result, dict):
                for k, v in result.items():
                    if k != "passed":
                        lines.append(f"  {k}: {v}")

        summary = report.get("summary", {})
        lines.append(f"\n总体评估: {summary.get('assessment', '未知')}")
        lines.append(f"通过项: {summary.get('passed', 0)}/{summary.get('total_analysis', 0)}")

        lines.append("\n建议:")
        for rec in summary.get("recommendations", []):
            lines.append(f"  - {rec}")

        lines.append("=" * 70)

        for line in lines:
            logger.info(line)
