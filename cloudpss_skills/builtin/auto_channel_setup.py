"""
Auto Channel Setup Skill

自动量测配置 - 批量添加EMT仿真输出通道和量测配置。
"""

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from cloudpss_skills.core import (
    Artifact,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    register,
)
from cloudpss_skills.core.auth_utils import load_or_fetch_model

logger = logging.getLogger(__name__)


@register
class AutoChannelSetupSkill(SkillBase):
    """自动量测配置技能 - 批量添加EMT输出通道"""

    # CloudPSS标准元件RID
    COMPONENT_RIDS = {
        "bus_3p": "model/CloudPSS/_newBus_3p",
        "line_3p": "model/CloudPSS/TransmissionLine",
        "transformer_3p": "model/CloudPSS/_newTransformer_3p",
        "generator": "model/CloudPSS/_newGenerator",
        "shunt": "model/CloudPSS/_newShuntLC_3p",
        "load": "model/CloudPSS/_newLoad_3p",
        "channel": "model/CloudPSS/_newChannel",
    }

    @property
    def name(self) -> str:
        return "auto_channel_setup"

    @property
    def description(self) -> str:
        return "自动批量配置EMT仿真输出通道，支持电压、电流、功率等多种量测类型"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "auto_channel_setup"},
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
                        "rid": {"type": "string", "description": "模型RID"},
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                    },
                },
                "measurements": {
                    "type": "object",
                    "properties": {
                        "voltage": {
                            "type": "object",
                            "properties": {
                                "enabled": {"type": "boolean", "default": True},
                                "voltage_levels": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "电压等级筛选(kV)，如[220, 500]，空数组表示全部",
                                },
                                "bus_names": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "母线名称筛选，空数组表示全部",
                                },
                                "freq": {
                                    "type": "integer",
                                    "default": 200,
                                    "description": "采样频率(Hz)",
                                },
                            },
                        },
                        "current": {
                            "type": "object",
                            "properties": {
                                "enabled": {"type": "boolean", "default": False},
                                "component_types": {
                                    "type": "array",
                                    "items": {"enum": ["line", "transformer"]},
                                    "default": ["line", "transformer"],
                                },
                                "freq": {"type": "integer", "default": 200},
                            },
                        },
                        "power": {
                            "type": "object",
                            "properties": {
                                "enabled": {"type": "boolean", "default": False},
                                "component_types": {
                                    "type": "array",
                                    "items": {"enum": ["generator", "load", "line"]},
                                    "default": ["generator", "load"],
                                },
                                "freq": {"type": "integer", "default": 200},
                            },
                        },
                        "frequency": {
                            "type": "object",
                            "properties": {
                                "enabled": {"type": "boolean", "default": False},
                                "freq": {"type": "integer", "default": 50},
                            },
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "save_model": {
                            "type": "boolean",
                            "default": False,
                            "description": "是否保存修改后的模型",
                        },
                        "dry_run": {
                            "type": "boolean",
                            "default": False,
                            "description": "仅预览不修改",
                        },
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "model": {
                "rid": "",
                "source": "cloud",
            },
            "measurements": {
                "voltage": {
                    "enabled": True,
                    "voltage_levels": [],
                    "bus_names": [],
                    "freq": 200,
                },
                "current": {
                    "enabled": False,
                    "component_types": ["line", "transformer"],
                    "freq": 200,
                },
                "power": {
                    "enabled": False,
                    "component_types": ["generator", "load"],
                    "freq": 200,
                },
                "frequency": {
                    "enabled": False,
                    "freq": 50,
                },
            },
            "output": {
                "save_model": False,
                "dry_run": False,
            },
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        """验证配置"""
        result = super().validate(config)

        model = config.get("model", {})
        rid = model.get("rid", "")

        if not rid:
            result.add_error("必须提供model.rid")
            result.add_error("  示例: 'model/holdme/IEEE39'")

        # 检查至少启用了一种量测
        measurements = config.get("measurements", {})
        any_enabled = any(m.get("enabled", False) for m in measurements.values())
        if not any_enabled:
            result.add_error("至少启用一种量测类型(voltage/current/power/frequency)")

        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行自动量测配置"""
        from cloudpss import Model, setToken

        start_time = datetime.now()
        logs = []
        artifacts = []
        added_channels = []

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
                if token_path.exists():
                    token = token_path.read_text().strip()

            if not token:
                raise ValueError(
                    "未找到CloudPSS token，请提供auth.token或创建.cloudpss_token文件"
                )

            setToken(token)
            log("INFO", "认证成功")

            # 2. 加载模型
            model_config = config.get("model", {})
            rid = model_config["rid"]

            log("INFO", f"加载模型: {rid}")

            model = load_or_fetch_model(model_config, config)

            log("INFO", f"模型名称: {model.name}")

            # 3. 获取测量配置
            measurements = config.get("measurements", {})
            output_config = config.get("output", {})
            dry_run = output_config.get("dry_run", False)
            save_model = output_config.get("save_model", False)

            if dry_run:
                log("INFO", "【试运行模式】仅预览配置，不修改模型")

            # 4. 添加电压量测
            voltage_config = measurements.get("voltage", {})
            if voltage_config.get("enabled", True):
                try:
                    log("INFO", "配置电压量测...")
                    channels = self._add_voltage_measurements(
                        model, voltage_config, dry_run
                    )
                    added_channels.extend(channels)
                    log("INFO", f"  -> 添加 {len(channels)} 个电压量测通道")
                except (AttributeError, TypeError, ValueError, RuntimeError) as e:
                    log("ERROR", f"配置电压量测失败: {e}")
                    if not dry_run:
                        raise

            # 5. 添加电流量测
            current_config = measurements.get("current", {})
            if current_config.get("enabled", False):
                try:
                    log("INFO", "配置电流量测...")
                    channels = self._add_current_measurements(
                        model, current_config, dry_run
                    )
                    added_channels.extend(channels)
                    log("INFO", f"  -> 添加 {len(channels)} 个电流量测通道")
                except (AttributeError, TypeError, ValueError, RuntimeError) as e:
                    log("ERROR", f"配置电流量测失败: {e}")
                    if not dry_run:
                        raise

            # 6. 添加功率量测
            power_config = measurements.get("power", {})
            if power_config.get("enabled", False):
                try:
                    log("INFO", "配置功率量测...")
                    channels = self._add_power_measurements(
                        model, power_config, dry_run
                    )
                    added_channels.extend(channels)
                    log("INFO", f"  -> 添加 {len(channels)} 个功率量测通道")
                except (AttributeError, TypeError, ValueError, RuntimeError) as e:
                    log("ERROR", f"配置功率量测失败: {e}")
                    if not dry_run:
                        raise

            # 7. 添加频率量测
            freq_config = measurements.get("frequency", {})
            if freq_config.get("enabled", False):
                try:
                    log("INFO", "配置频率量测...")
                    channels = self._add_frequency_measurements(
                        model, freq_config, dry_run
                    )
                    added_channels.extend(channels)
                    log("INFO", f"  -> 添加 {len(channels)} 个频率量测通道")
                except (AttributeError, TypeError, ValueError, RuntimeError) as e:
                    log("ERROR", f"配置频率量测失败: {e}")
                    if not dry_run:
                        raise

            # 8. 保存模型（如果需要）
            if save_model and not dry_run:
                log("INFO", "保存修改后的模型...")
                model.save()
                log("INFO", "模型保存成功")

            # 9. 生成配置报告
            log("INFO", "生成配置报告...")
            report = self._generate_report(added_channels)
            report_path = Path("./results/auto_channel_setup_report.json")
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))

            artifacts.append(
                Artifact(
                    type="json",
                    path=str(report_path),
                    size=report_path.stat().st_size,
                    description="量测配置报告",
                )
            )

            log("INFO", f"配置完成！共添加 {len(added_channels)} 个量测通道")

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "model_rid": rid,
                    "model_name": model.name,
                    "total_channels": len(added_channels),
                    "voltage_channels": len(
                        [c for c in added_channels if c["type"] == "voltage"]
                    ),
                    "current_channels": len(
                        [c for c in added_channels if c["type"] == "current"]
                    ),
                    "power_channels": len(
                        [c for c in added_channels if c["type"] == "power"]
                    ),
                    "frequency_channels": len(
                        [c for c in added_channels if c["type"] == "frequency"]
                    ),
                    "dry_run": dry_run,
                    "saved": save_model and not dry_run,
                },
                artifacts=artifacts,
                logs=logs,
            )

        except (
            AttributeError,
            FileNotFoundError,
            TypeError,
            ValueError,
            RuntimeError,
            KeyError,
            ConnectionError,
            Exception,
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

    def _add_voltage_measurements(
        self, model: Any, config: Dict, dry_run: bool
    ) -> List[Dict]:
        """添加电压量测通道"""
        channels = []

        voltage_levels = config.get("voltage_levels", [])
        bus_names = config.get("bus_names", [])
        freq = config.get("freq", 200)

        # 获取所有母线
        buses = model.getComponentsByRid(self.COMPONENT_RIDS["bus_3p"])

        for bus_key, bus in buses.items():
            bus_name = bus.args.get("Name", bus.label)
            v_base = float(bus.args.get("VBase", 0))

            # 电压等级筛选
            if voltage_levels and v_base not in voltage_levels:
                continue

            # 母线名称筛选
            if bus_names and bus_name not in bus_names:
                continue

            # 获取Vrms量测点
            vrms_pin = bus.args.get("Vrms", "")
            if not vrms_pin:
                vrms_pin = f"#{bus_name}.Vrms"
                if not dry_run:
                    bus.args["Vrms"] = vrms_pin

            channel_info = {
                "type": "voltage",
                "component": bus_name,
                "pin": vrms_pin,
                "v_base": v_base,
                "freq": freq,
                "dim": 1,
            }
            channels.append(channel_info)

        return channels

    def _add_current_measurements(
        self, model: Any, config: Dict, dry_run: bool
    ) -> List[Dict]:
        """添加电流量测通道"""
        channels = []

        component_types = config.get("component_types", ["line", "transformer"])
        freq = config.get("freq", 200)

        for comp_type in component_types:
            if comp_type == "line":
                components = model.getComponentsByRid(self.COMPONENT_RIDS["line_3p"])
                pin_suffix = "Is"  # 送端电流
            elif comp_type == "transformer":
                components = model.getComponentsByRid(
                    self.COMPONENT_RIDS["transformer_3p"]
                )
                pin_suffix = "I1"  # 一次侧电流
            else:
                continue

            for comp_key, comp in components.items():
                comp_name = comp.args.get("Name", comp.label)

                # 获取电流量测点
                current_pin = comp.args.get(pin_suffix, "")
                if not current_pin:
                    current_pin = f"#{comp_name}.{pin_suffix}"
                    if not dry_run:
                        comp.args[pin_suffix] = current_pin

                channel_info = {
                    "type": "current",
                    "component": comp_name,
                    "pin": current_pin,
                    "freq": freq,
                    "dim": 3,  # 三相电流
                }
                channels.append(channel_info)

        return channels

    def _add_power_measurements(
        self, model: Any, config: Dict, dry_run: bool
    ) -> List[Dict]:
        """添加功率量测通道"""
        channels = []

        component_types = config.get("component_types", ["generator", "load"])
        freq = config.get("freq", 200)

        for comp_type in component_types:
            if comp_type == "generator":
                components = model.getComponentsByRid(self.COMPONENT_RIDS["generator"])
                p_pin_suffix = "P"
                q_pin_suffix = "Q"
            elif comp_type == "load":
                components = model.getComponentsByRid(self.COMPONENT_RIDS["load"])
                p_pin_suffix = "P"
                q_pin_suffix = "Q"
            elif comp_type == "line":
                components = model.getComponentsByRid(self.COMPONENT_RIDS["line_3p"])
                p_pin_suffix = "P"
                q_pin_suffix = "Q"
            else:
                continue

            for comp_key, comp in components.items():
                comp_name = comp.args.get("Name", comp.label)

                # 有功功率
                p_pin = comp.args.get(p_pin_suffix, "")
                if not p_pin:
                    p_pin = f"#{comp_name}.{p_pin_suffix}"
                    if not dry_run:
                        comp.args[p_pin_suffix] = p_pin

                channels.append(
                    {
                        "type": "power",
                        "component": comp_name,
                        "pin": p_pin,
                        "power_type": "P",
                        "freq": freq,
                        "dim": 1,
                    }
                )

                # 无功功率
                q_pin = comp.args.get(q_pin_suffix, "")
                if not q_pin:
                    q_pin = f"#{comp_name}.{q_pin_suffix}"
                    if not dry_run:
                        comp.args[q_pin_suffix] = q_pin

                channels.append(
                    {
                        "type": "power",
                        "component": comp_name,
                        "pin": q_pin,
                        "power_type": "Q",
                        "freq": freq,
                        "dim": 1,
                    }
                )

        return channels

    def _add_frequency_measurements(
        self, model: Any, config: Dict, dry_run: bool
    ) -> List[Dict]:
        """添加频率量测通道"""
        channels = []

        freq = config.get("freq", 50)

        # 获取所有母线（频率通常在母线上测量）
        buses = model.getComponentsByRid(self.COMPONENT_RIDS["bus_3p"])

        # 只选择前几个母线测量频率（避免过多）
        bus_list = list(buses.items())[:5]

        for bus_key, bus in bus_list:
            bus_name = bus.args.get("Name", bus.label)

            # 频率量测通常使用Vabc经过PLL
            freq_pin = f"#{bus_name}.Freq"

            channel_info = {
                "type": "frequency",
                "component": bus_name,
                "pin": freq_pin,
                "freq": freq,
                "dim": 1,
            }
            channels.append(channel_info)

        return channels

    def _generate_report(self, channels: List[Dict]) -> Dict:
        """生成配置报告"""
        by_type = {}
        for ch in channels:
            t = ch["type"]
            if t not in by_type:
                by_type[t] = []
            by_type[t].append(ch)

        return {
            "summary": {
                "total": len(channels),
                "by_type": {t: len(items) for t, items in by_type.items()},
            },
            "channels": channels,
            "suggested_output_config": self._generate_output_config(channels),
        }

    def _generate_output_config(self, channels: List[Dict]) -> Dict:
        """生成建议的输出配置"""
        # 按类型和采样频率分组
        groups = {}

        for ch in channels:
            key = (ch["type"], ch.get("freq", 200))
            if key not in groups:
                groups[key] = []
            groups[key].append(ch)

        output_channels = []
        for (mtype, freq), items in groups.items():
            channel_ids = [
                f"#{ch['component']}" for ch in items[:10]
            ]  # 限制每组最多10个
            output_channels.append(
                {
                    "plot_name": f"{mtype.capitalize()}_{freq}Hz",
                    "freq": freq,
                    "channels": channel_ids,
                }
            )

        return output_channels
