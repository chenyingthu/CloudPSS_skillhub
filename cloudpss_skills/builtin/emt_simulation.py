"""
EMT Simulation Skill

运行EMT暂态仿真并导出波形数据。
"""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

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
    reload_model,
    run_emt_and_wait,
    OutputConfig,
    get_components_by_definition,
    update_component_args,
)

logger = logging.getLogger(__name__)


@register
class EmtSimulationSkill(SkillBase):
    """EMT暂态仿真技能"""

    @property
    def name(self) -> str:
        return "emt_simulation"

    @property
    def description(self) -> str:
        return "运行EMT暂态仿真并导出波形数据"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "emt_simulation"},
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
                "simulation": {
                    "type": "object",
                    "properties": {
                        "duration": {
                            "type": "number",
                            "minimum": 0,
                            "description": "仿真时长（秒）",
                        },
                        "step_size": {
                            "type": "number",
                            "minimum": 0,
                            "description": "仿真步长",
                        },
                        "timeout": {
                            "type": "integer",
                            "minimum": 0,
                            "default": 300,
                            "description": "超时时间（秒）",
                        },
                        "sampling_freq": {
                            "type": "integer",
                            "minimum": 1,
                            "default": 2000,
                            "description": "采样频率（Hz）",
                        },
                    },
                },
                "fault": {
                    "type": "object",
                    "properties": {
                        "start_time": {
                            "type": "number",
                            "description": "故障开始时间（秒），修改_newFaultResistor_3p元件的fs参数",
                        },
                        "end_time": {
                            "type": "number",
                            "description": "故障结束时间（秒），修改_newFaultResistor_3p元件的fe参数",
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["csv", "json", "yaml"], "default": "csv"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "emt_output"},
                        "timestamp": {"type": "boolean", "default": True},
                        "channels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "要导出的通道列表，*表示全部",
                        },
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE3", "source": "cloud"},
            "simulation": {"timeout": 300, "sampling_freq": 2000},
            "output": {
                "format": "csv",
                "path": "./results/",
                "prefix": "emt_output",
                "timestamp": True,
                "channels": ["*"],
            },
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        result = super().validate(config)

        # 检查model.rid
        model = config.get("model", {})
        if not model.get("rid"):
            result.add_error("必须提供 model.rid")

        # 检查token
        auth = config.get("auth", {})
        if not auth.get("token") and not auth.get("token_file"):
            result.add_error("必须提供auth.token或auth.token_file")

        # 检查仿真参数
        simulation = config.get("simulation", {})
        if simulation.get("duration", 0) < 0:
            result.add_warning("仿真时长应该大于0")

        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行EMT仿真"""
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
            model = reload_model(
                model_config["rid"],
                model_config.get("source", "cloud"),
                config,
            )
            log("INFO", f"模型: {model.name} ({model.rid})")

            # 可选：调整故障参数（ieee3_prep 功能合并）
            fault_config = config.get("fault", {})
            if fault_config:
                model = self._apply_fault_parameters(model, fault_config, log)

            # 可选：调整采样频率
            sampling_freq = config.get("simulation", {}).get("sampling_freq")
            if sampling_freq and sampling_freq != 2000:
                log("INFO", f"设置采样频率: {sampling_freq}Hz")
                model = self._set_sampling_freq(model, sampling_freq, log)

            log("INFO", "检查EMT拓扑...")
            try:
                topology = model.fetchTopology(implementType="emtp")
                topology_data = topology.toJSON()
                component_count = len(topology_data.get("components", {}))
                log("INFO", f"拓扑检查通过，元件数: {component_count}")
            except (KeyError, AttributeError) as e:
                log("ERROR", f"拓扑检查失败: {e}")
                raise RuntimeError(f"EMT拓扑检查失败: {e}")

            log("INFO", "启动EMT仿真...")
            timeout = config.get("simulation", {}).get("timeout", 300)
            job_result = run_emt_and_wait(model, config, timeout=timeout, log_func=log)

            if not job_result.success:
                raise RuntimeError(job_result.error or "EMT仿真失败")

            result = job_result.result
            if result is None:
                raise RuntimeError("结果为空")

            plots = list(result.getPlots())
            log("INFO", f"波形分组数: {len(plots)}")

            output_config = config.get("output", {})
            output = OutputConfig(
                path=output_config.get("path", "./results/"),
                prefix=output_config.get("prefix", "emt_output"),
                timestamp=output_config.get("timestamp", True),
            )
            output_format = output_config.get("format", "csv")

            exported_files = []
            for i, plot in enumerate(plots):
                plot_key = plot.get("key") or plot.get("name") or f"plot_{i}"
                channel_names = result.getPlotChannelNames(i)
                if not channel_names:
                    continue

                if output_format == "csv":
                    filepath = self._export_csv(
                        result,
                        i,
                        channel_names,
                        output.get_path(suffix=plot_key, extension="csv"),
                    )
                else:
                    filepath = self._export_json(
                        result,
                        i,
                        channel_names,
                        output.get_path(suffix=plot_key, extension="json"),
                    )
                if filepath:
                    exported_files.append(filepath)
                    artifacts.append(
                        Artifact(
                            type=output_format,
                            path=str(filepath),
                            size=filepath.stat().st_size,
                            description=f"波形数据 ({output_format.upper()})",
                        )
                    )
                    log("INFO", f"导出: {filepath}")

            job_id = getattr(getattr(job_result, "job", None), "id", None)
            result_data = {
                "model_name": model.name,
                "model_rid": model.rid,
                "job_id": job_id,
                "plot_count": len(plots),
                "plots": [],
            }

            for i, plot in enumerate(plots):
                channel_names = result.getPlotChannelNames(i)
                result_data["plots"].append(
                    {
                        "index": i,
                        "key": plot.get("key"),
                        "name": plot.get("name"),
                        "channel_count": len(channel_names),
                        "channels": channel_names[:10]
                        if len(channel_names) > 10
                        else channel_names,
                    }
                )

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
                metrics={
                    "plot_count": len(plots),
                    "exported_files": len(exported_files),
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
                    "stage": "emt_simulation",
                },
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )

    def _apply_fault_parameters(self, model, fault_config: Dict, log_func) -> Any:
        """调整故障元件参数（fs/fe）"""
        FAULT_DEFINITION = "model/CloudPSS/_newFaultResistor_3p"
        components = get_components_by_definition(model, FAULT_DEFINITION)
        if not components:
            log_func(
                "WARN",
                "未找到故障元件 model/CloudPSS/_newFaultResistor_3p，跳过故障参数调整",
            )
            return model

        fault = components[0]
        new_start = fault_config.get("start_time")
        new_end = fault_config.get("end_time")

        args = dict(fault.args) if hasattr(fault, "args") else {}
        if new_start is not None:
            args["fs"] = {"source": str(new_start), "ɵexp": ""}
            log_func("INFO", f"故障开始时间: {new_start}s")
        if new_end is not None:
            args["fe"] = {"source": str(new_end), "ɵexp": ""}
            log_func("INFO", f"故障结束时间: {new_end}s")

        update_component_args(model, fault.id, args)
        return model

    def _set_sampling_freq(self, model, sampling_freq: int, log_func) -> Any:
        """调整量测通道采样频率"""
        CHANNEL_DEFINITION = "model/CloudPSS/_newChannel"
        channels = get_components_by_definition(model, CHANNEL_DEFINITION)
        if not channels:
            log_func("WARN", "未找到量测通道，跳过采样频率调整")
            return model

        for channel in channels:
            args = dict(channel.args) if hasattr(channel, "args") else {}
            args["Freq"] = {"source": str(sampling_freq), "ɵexp": ""}
            update_component_args(model, channel.id, args)

        log_func("INFO", f"已设置 {len(channels)} 个通道的采样频率: {sampling_freq}Hz")
        return model

    def _export_csv(
        self, result, plot_index: int, channel_names: list, filepath: Path
    ) -> Path:
        """导出为CSV格式"""
        import csv

        # 获取所有通道的数据
        all_data = {}
        for channel in channel_names:
            channel_data = result.getPlotChannelData(plot_index, channel)
            if channel_data:
                all_data[channel] = channel_data

        if not all_data:
            return filepath

        # 写入CSV
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # 表头
            headers = ["time"] + list(all_data.keys())
            writer.writerow(headers)

            # 数据行
            first_channel = list(all_data.values())[0]
            x_data = first_channel.get("x", [])

            for i in range(len(x_data)):
                row = [x_data[i]]
                for channel in channel_names:
                    y_data = all_data.get(channel, {}).get("y", [])
                    row.append(y_data[i] if i < len(y_data) else "")
                writer.writerow(row)

        return filepath

    def _export_json(
        self, result, plot_index: int, channel_names: list, filepath: Path
    ) -> Path:
        """导出为JSON格式"""
        data = {"plot_index": plot_index, "channels": {}}

        for channel in channel_names:
            channel_data = result.getPlotChannelData(plot_index, channel)
            if channel_data:
                data["channels"][channel] = {
                    "x": channel_data.get("x", []),
                    "y": channel_data.get("y", []),
                }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return filepath
