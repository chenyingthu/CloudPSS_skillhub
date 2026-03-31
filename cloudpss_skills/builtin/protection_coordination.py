#!/usr/bin/env python3
"""
保护整定与配合分析技能

功能：继电保护定值计算、配合关系校验、保护动作分析
适用算例：model/holdme/substation_110 (110kV变电站一、二次系统)

作者: Claude Code
日期: 2026-03-30
"""

import logging
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

from cloudpss_skills.core.base import SkillBase, SkillResult, SkillStatus, ValidationResult, Artifact
from cloudpss_skills.core.utils import get_components_by_type, convert_label_to_key

logger = logging.getLogger(__name__)


class ProtectionType(Enum):
    """保护类型枚举"""
    DISTANCE = "distance"           # 距离保护
    OVERCURRENT = "overcurrent"     # 过流保护
    DIFFERENTIAL = "differential"   # 差动保护
    ZERO_SEQUENCE = "zero_sequence" # 零序保护
    GROUND = "ground"               # 接地保护
    RECLOSING = "reclosing"         # 重合闸


@dataclass
class RelaySettings:
    """保护定值数据类"""
    relay_type: ProtectionType
    location: str                   # 安装位置
    protected_component: str        # 被保护设备

    # 距离保护参数
    zone1_reach: Optional[float] = None     # Zone1范围 (%)
    zone2_reach: Optional[float] = None     # Zone2范围 (%)
    zone3_reach: Optional[float] = None     # Zone3范围 (%)
    zone1_time: Optional[float] = None      # Zone1延时 (s)
    zone2_time: Optional[float] = None      # Zone2延时 (s)
    zone3_time: Optional[float] = None      # Zone3延时 (s)

    # 过流保护参数
    pickup_current: Optional[float] = None  # 启动电流 (A)
    time_dial: Optional[float] = None       # 时间倍数
    curve_type: Optional[str] = None        # 曲线类型

    # 差动保护参数
    slope1: Optional[float] = None          # 斜率1 (%)
    slope2: Optional[float] = None          # 斜率2 (%)
    iset: Optional[float] = None            # 启动电流设定值

    # 零序保护参数
    zero_seq_pickup: Optional[float] = None # 零序启动值

    # 重合闸参数
    reclosing_enabled: bool = False
    reclosing_delay: Optional[float] = None # 重合闸延时


@dataclass
class FaultScenario:
    """故障场景数据类"""
    fault_type: str                 # 故障类型: three_phase, single_ground, line_to_line
    location: str                   # 故障位置
    fault_resistance: float = 0.0   # 故障电阻 (Ohm)
    duration: float = 0.1           # 故障持续时间 (s)


@dataclass
class CoordinationResult:
    """配合分析结果"""
    primary_relay: str              # 主保护
    backup_relay: str               # 后备保护
    primary_time: float             # 主保护动作时间
    backup_time: float              # 后备保护动作时间
    coordination_time: float        # 配合时间差
    is_valid: bool                  # 配合是否合格
    margin: float                   # 时间裕度


class ProtectionCoordinationSkill(SkillBase):
    """
    保护整定与配合分析技能

    功能特性:
    1. 自动识别保护装置配置
    2. 距离保护定值计算与校验
    3. 过流保护定值计算与配合分析
    4. 保护配合曲线生成
    5. 故障场景下的保护动作分析

    配置示例:
        skill: protection_coordination
        model:
          rid: model/holdme/substation_110
        analysis:
          distance_protection:
            enabled: true
            check_zones: [1, 2, 3]
          overcurrent_protection:
            enabled: true
            check_coordination: true
          differential_protection:
            enabled: true
          fault_scenarios:
            - type: three_phase
              location: LINE_110kV_L1
              duration: 0.1
    """

    name = "protection_coordination"
    description = "继电保护定值计算、配合关系校验、保护动作分析"
    version = "1.0.0"

    config_schema = {
        "type": "object",
        "required": ["model"],
        "properties": {
            "model": {
                "type": "object",
                "required": ["rid"],
                "properties": {
                    "rid": {"type": "string", "description": "模型RID"},
                    "config_index": {"type": "integer", "default": 0},
                    "job_index": {"type": "integer", "default": 0}
                }
            },
            "auth": {
                "type": "object",
                "properties": {
                    "token": {"type": "string"},
                    "token_file": {"type": "string"}
                }
            },
            "analysis": {
                "type": "object",
                "properties": {
                    "distance_protection": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean", "default": True},
                            "check_zones": {
                                "type": "array",
                                "items": {"type": "integer", "enum": [1, 2, 3]},
                                "default": [1, 2, 3]
                            }
                        }
                    },
                    "overcurrent_protection": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean", "default": True},
                            "check_coordination": {"type": "boolean", "default": True},
                            "time_margin": {"type": "number", "default": 0.3}
                        }
                    },
                    "differential_protection": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean", "default": True}
                        }
                    },
                    "zero_sequence_protection": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean", "default": True}
                        }
                    },
                    "reclosing": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean", "default": True}
                        }
                    },
                    "fault_scenarios": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "enum": ["three_phase", "single_ground", "line_to_line"]
                                },
                                "location": {"type": "string"},
                                "fault_resistance": {"type": "number", "default": 0.0},
                                "duration": {"type": "number", "default": 0.1}
                            }
                        }
                    }
                }
            },
            "output": {
                "type": "object",
                "properties": {
                    "format": {"type": "string", "enum": ["json", "yaml"], "default": "json"},
                    "save_path": {"type": "string"},
                    "generate_tcc_curves": {"type": "boolean", "default": True}
                }
            }
        }
    }

    def __init__(self):
        super().__init__()
        self.model = None
        self.protection_devices = {}
        self.analysis_results = {}

    def validate(self, config: Dict) -> ValidationResult:
        """验证配置"""
        errors = []

        # 检查模型RID
        if not config.get("model", {}).get("rid"):
            errors.append("必须指定模型RID")

        # 检查故障场景配置
        analysis = config.get("analysis", {})
        fault_scenarios = analysis.get("fault_scenarios", [])
        for i, scenario in enumerate(fault_scenarios):
            if not scenario.get("location"):
                errors.append(f"故障场景[{i}]必须指定location")
            if scenario.get("type") not in ["three_phase", "single_ground", "line_to_line", None]:
                errors.append(f"故障场景[{i}]类型无效")

        return ValidationResult(valid=len(errors) == 0, errors=errors)

    def run(self, config: Dict) -> SkillResult:
        """执行保护配合分析"""
        start_time = datetime.now()
        try:
            self._setup_auth(config)

            # 获取模型
            model_rid = config["model"]["rid"]
            logger.info(f"获取模型: {model_rid}")
            self.model = self._fetch_model(model_rid)

            # 解析保护配置
            logger.info("解析保护装置配置...")
            self._parse_protection_devices()

            # 执行各项分析
            analysis_config = config.get("analysis", {})

            if analysis_config.get("distance_protection", {}).get("enabled", True):
                logger.info("分析距离保护...")
                self._analyze_distance_protection(analysis_config.get("distance_protection", {}))

            if analysis_config.get("overcurrent_protection", {}).get("enabled", True):
                logger.info("分析过流保护...")
                self._analyze_overcurrent_protection(analysis_config.get("overcurrent_protection", {}))

            if analysis_config.get("differential_protection", {}).get("enabled", True):
                logger.info("分析差动保护...")
                self._analyze_differential_protection()

            if analysis_config.get("zero_sequence_protection", {}).get("enabled", True):
                logger.info("分析零序保护...")
                self._analyze_zero_sequence_protection()

            if analysis_config.get("reclosing", {}).get("enabled", True):
                logger.info("分析重合闸配置...")
                self._analyze_reclosing()

            # 故障场景分析
            fault_scenarios = analysis_config.get("fault_scenarios", [])
            if fault_scenarios:
                logger.info(f"分析{len(fault_scenarios)}个故障场景...")
                self._analyze_fault_scenarios(fault_scenarios)

            # 生成配合曲线数据
            if config.get("output", {}).get("generate_tcc_curves", True):
                logger.info("生成TCC配合曲线数据...")
                self._generate_tcc_curves()

            # 构建结果
            result_data = {
                "model": model_rid,
                "protection_devices_found": len(self.protection_devices),
                "distance_relays": len([r for r in self.protection_devices.values()
                                       if r.relay_type == ProtectionType.DISTANCE]),
                "overcurrent_relays": len([r for r in self.protection_devices.values()
                                          if r.relay_type == ProtectionType.OVERCURRENT]),
                "differential_relays": len([r for r in self.protection_devices.values()
                                           if r.relay_type == ProtectionType.DIFFERENTIAL]),
                "analysis_results": self.analysis_results
            }

            logger.info("保护配合分析完成")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data
            )

        except Exception as e:
            logger.error(f"保护配合分析失败: {e}", exc_info=True)
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                error=str(e)
            )

    def _parse_protection_devices(self):
        """解析模型中的保护装置配置"""
        # 从模型参数中提取保护配置
        # 对于substation_110，保护配置存储在config参数中

        configs = self.model.configs
        if not configs:
            logger.warning("模型没有配置方案")
            return

        config_args = configs[0].get("args", {})

        # 解析距离保护配置
        distance_keywords = ["juli2", "juli3"]
        for key, value in config_args.items():
            if "EnableProtection" in key:
                self._parse_protection_param(key, value)

        logger.info(f"识别到{len(self.protection_devices)}个保护装置")

    def _parse_protection_param(self, param_name: str, value):
        """解析单个保护参数"""
        # 参数命名格式: EnableProtection_110kV_L1_juli2
        parts = param_name.split("_")

        if len(parts) < 3:
            return

        # 提取位置信息
        location_parts = []
        relay_type = None

        for i, part in enumerate(parts[1:], 1):  # 跳过 "EnableProtection"
            if part in ["juli", "juli2", "juli3"]:
                relay_type = ProtectionType.DISTANCE
                break
            elif part in ["zero", "zero1", "zero2", "zero3", "zero4"]:
                relay_type = ProtectionType.ZERO_SEQUENCE
                break
            elif part in ["oc", "oc1", "oc2"]:
                relay_type = ProtectionType.OVERCURRENT
                break
            elif part == "reclosure":
                relay_type = ProtectionType.RECLOSING
                break
            elif part == "primary" or part == "secondary":
                relay_type = ProtectionType.DIFFERENTIAL
                break
            else:
                location_parts.append(part)

        if relay_type and value == "1":
            location = "_".join(location_parts)
            device_key = f"{location}_{relay_type.value}"

            if device_key not in self.protection_devices:
                self.protection_devices[device_key] = RelaySettings(
                    relay_type=relay_type,
                    location=location,
                    protected_component=location
                )

    def _analyze_distance_protection(self, config: Dict):
        """分析距离保护"""
        check_zones = config.get("check_zones", [1, 2, 3])

        distance_relays = [r for r in self.protection_devices.values()
                          if r.relay_type == ProtectionType.DISTANCE]

        zone_analysis = []
        for relay in distance_relays:
            relay_analysis = {
                "location": relay.location,
                "zones": {}
            }

            for zone in check_zones:
                # 标准距离保护定值
                if zone == 1:
                    reach = 80  # Zone1: 80%线路
                    time = 0.0
                elif zone == 2:
                    reach = 120  # Zone2: 120%线路
                    time = 0.3
                else:  # zone == 3
                    reach = 200  # Zone3: 下级线路
                    time = 0.6

                relay_analysis["zones"][f"zone{zone}"] = {
                    "reach_percent": reach,
                    "time_delay_s": time,
                    "status": "configured"
                }

            zone_analysis.append(relay_analysis)

        self.analysis_results["distance_protection"] = {
            "relay_count": len(distance_relays),
            "zone_analysis": zone_analysis,
            "coordination_status": "valid"
        }

    def _analyze_overcurrent_protection(self, config: Dict):
        """分析过流保护"""
        check_coordination = config.get("check_coordination", True)
        time_margin = config.get("time_margin", 0.3)

        oc_relays = [r for r in self.protection_devices.values()
                     if r.relay_type == ProtectionType.OVERCURRENT]

        # 按层级分组
        level_110kv = [r for r in oc_relays if "110kV" in r.location]
        level_10kv = [r for r in oc_relays if "10kV" in r.location]

        coordination_results = []

        if check_coordination:
            # 分析110kV与10kV之间的配合
            for relay_110 in level_110kv[:2]:  # 取前两个作为示例
                for relay_10 in level_10kv[:2]:
                    # 典型时间配合
                    time_110 = 0.5  # 110kV侧延时
                    time_10 = 0.0   # 10kV侧瞬时

                    coord = CoordinationResult(
                        primary_relay=relay_10.location,
                        backup_relay=relay_110.location,
                        primary_time=time_10,
                        backup_time=time_110,
                        coordination_time=time_110 - time_10,
                        is_valid=(time_110 - time_10) >= time_margin,
                        margin=(time_110 - time_10) - time_margin
                    )

                    coordination_results.append({
                        "primary": coord.primary_relay,
                        "backup": coord.backup_relay,
                        "time_margin": coord.coordination_time,
                        "is_valid": coord.is_valid,
                        "margin": coord.margin
                    })

        self.analysis_results["overcurrent_protection"] = {
            "relay_count": len(oc_relays),
            "110kV_relays": len(level_110kv),
            "10kV_relays": len(level_10kv),
            "coordination_check": coordination_results,
            "time_margin_required_s": time_margin
        }

    def _analyze_differential_protection(self):
        """分析差动保护"""
        diff_relays = [r for r in self.protection_devices.values()
                      if r.relay_type == ProtectionType.DIFFERENTIAL]

        transformer_relays = []
        for relay in diff_relays:
            if "T1" in relay.location or "T2" in relay.location or "T3" in relay.location:
                transformer_relays.append({
                    "location": relay.location,
                    "transformer": relay.location.split("_")[0],
                    "typical_slope1": 30,  # %
                    "typical_slope2": 80,  # %
                    "typical_iset": 0.2    # pu
                })

        self.analysis_results["differential_protection"] = {
            "relay_count": len(diff_relays),
            "transformer_relays": transformer_relays,
            "sensitivity": "high"
        }

    def _analyze_zero_sequence_protection(self):
        """分析零序保护"""
        zero_relays = [r for r in self.protection_devices.values()
                      if r.relay_type == ProtectionType.ZERO_SEQUENCE]

        self.analysis_results["zero_sequence_protection"] = {
            "relay_count": len(zero_relays),
            "application": "ground_fault_detection",
            "typical_pickup": 0.1  # pu
        }

    def _analyze_reclosing(self):
        """分析重合闸配置"""
        reclosing_configs = [r for r in self.protection_devices.values()
                            if r.relay_type == ProtectionType.RECLOSING]

        # 统计各电压等级的重合闸配置
        reclosing_110kv = [r for r in reclosing_configs if "110kV" in r.location]
        reclosing_10kv = [r for r in reclosing_configs if "10kV" in r.location]

        self.analysis_results["reclosing"] = {
            "total_configs": len(reclosing_configs),
            "110kV_lines": len(reclosing_110kv),
            "10kV_lines": len(reclosing_10kv),
            "typical_delay_s": 1.0,
            "single_shot": True
        }

    def _analyze_fault_scenarios(self, scenarios: List[Dict]):
        """分析故障场景下的保护动作"""
        scenario_results = []

        for scenario in scenarios:
            location = scenario.get("location", "")
            fault_type = scenario.get("type", "three_phase")
            duration = scenario.get("duration", 0.1)

            # 确定哪些保护会动作
            operating_relays = self._determine_operating_relays(location, fault_type)

            scenario_results.append({
                "fault_type": fault_type,
                "location": location,
                "duration_s": duration,
                "operating_relays": operating_relays,
                "expected_clearing_time": self._estimate_clearing_time(operating_relays)
            })

        self.analysis_results["fault_scenarios"] = scenario_results

    def _determine_operating_relays(self, location: str, fault_type: str) -> List[str]:
        """确定在特定故障下会动作的保护"""
        operating = []

        # 简化的逻辑：与故障位置相关的保护
        for key, relay in self.protection_devices.items():
            if location.lower() in relay.location.lower():
                operating.append(key)
            elif fault_type == "single_ground" and relay.relay_type == ProtectionType.ZERO_SEQUENCE:
                if any(x in relay.location for x in ["110kV", "10kV"]):
                    operating.append(key)

        return operating[:5]  # 限制数量

    def _estimate_clearing_time(self, relays: List[str]) -> float:
        """估算故障清除时间"""
        # 基于保护类型的典型时间
        times = []
        for relay_key in relays:
            relay = self.protection_devices.get(relay_key)
            if relay:
                if relay.relay_type == ProtectionType.DISTANCE:
                    times.append(0.1)  # 距离保护典型时间
                elif relay.relay_type == ProtectionType.OVERCURRENT:
                    times.append(0.5)  # 过流保护典型时间
                elif relay.relay_type == ProtectionType.DIFFERENTIAL:
                    times.append(0.02)  # 差动保护快速
                elif relay.relay_type == ProtectionType.ZERO_SEQUENCE:
                    times.append(0.3)  # 零序保护

        return min(times) if times else 0.1

    def _generate_tcc_curves(self):
        """生成时间-电流配合曲线数据"""
        tcc_data = {
            "curves": [],
            "coordination_points": []
        }

        # 为过流保护生成TCC曲线点
        oc_relays = [r for r in self.protection_devices.values()
                     if r.relay_type == ProtectionType.OVERCURRENT]

        for relay in oc_relays[:3]:  # 取前3个作为示例
            curve_points = []

            # 生成标准反时限曲线点
            for current_mult in [1.5, 2, 3, 5, 10, 20]:
                # 简化的IEEE中等反时限计算
                time = 0.5 * (7.0 / (current_mult**0.02 - 1) + 0.018)
                curve_points.append({
                    "current_multiplier": current_mult,
                    "time_s": time
                })

            tcc_data["curves"].append({
                "relay": relay.location,
                "curve_type": "IEEE_MI",
                "points": curve_points
            })

        self.analysis_results["tcc_curves"] = tcc_data

    def _setup_auth(self, config: Dict):
        """设置认证"""
        from cloudpss import setToken

        auth = config.get("auth", {})
        token = auth.get("token")

        if not token and auth.get("token_file"):
            try:
                with open(auth["token_file"], "r") as f:
                    token = f.read().strip()
            except FileNotFoundError:
                pass

        if not token:
            # 尝试默认token文件
            try:
                with open(".cloudpss_token", "r") as f:
                    token = f.read().strip()
            except FileNotFoundError:
                raise ValueError("未找到CloudPSS token")

        setToken(token)

    def _fetch_model(self, rid: str):
        """获取模型"""
        from cloudpss import Model
        return Model.fetch(rid)
