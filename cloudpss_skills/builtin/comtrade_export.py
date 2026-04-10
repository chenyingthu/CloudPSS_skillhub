"""
COMTRADE Export Skill

COMTRADE导出 - 将EMT仿真结果导出为COMTRADE标准格式。

COMTRADE（Common Format for Transient Data Exchange）是IEEE Std C37.111
标准定义的电力系统暂态数据交换格式，包含.cfg配置文件和.dat数据文件。
"""

import json
import logging
import struct
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from cloudpss_skills.core import (
    Artifact,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    register,
)
from cloudpss_skills.core.utils import fetch_job_with_result

logger = logging.getLogger(__name__)


@register
class ComtradeExportSkill(SkillBase):
    """COMTRADE导出技能 - 将EMT仿真结果导出为标准格式"""

    @property
    def name(self) -> str:
        return "comtrade_export"

    @property
    def description(self) -> str:
        return "将EMT仿真结果导出为COMTRADE标准格式(.cfg+.dat)，支持BINARY格式"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "source"],
            "properties": {
                "skill": {"type": "string", "const": "comtrade_export"},
                "auth": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"},
                        "token_file": {"type": "string", "default": ".cloudpss_token"},
                    },
                },
                "source": {
                    "type": "object",
                    "required": ["job_id"],
                    "properties": {
                        "job_id": {"type": "string", "description": "EMT仿真任务ID"},
                        "plot_index": {
                            "type": "integer",
                            "default": 0,
                            "description": "要导出的波形分组索引",
                        },
                    },
                },
                "comtrade": {
                    "type": "object",
                    "properties": {
                        "station_name": {
                            "type": "string",
                            "default": "CloudPSS",
                            "description": "厂站名称",
                        },
                        "rec_dev_id": {
                            "type": "string",
                            "default": "EMT",
                            "description": "记录装置标识",
                        },
                        "rev_year": {
                            "type": "integer",
                            "default": 1999,
                            "description": "COMTRADE版本年号(1991/1999/2013)",
                        },
                        "frequency": {
                            "type": "number",
                            "default": 50.0,
                            "description": "系统频率(Hz)",
                        },
                        "time_mult": {
                            "type": "number",
                            "default": 1.0,
                            "description": "时间戳倍率因子",
                        },
                    },
                },
                "channels": {
                    "type": "object",
                    "properties": {
                        "selected": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "要导出的通道列表，空数组表示全部",
                        },
                        "uu_map": {
                            "type": "object",
                            "description": "通道名称到单位的映射，如{'Bus1_V': 'kV'}",
                        },
                        "ph_map": {
                            "type": "object",
                            "description": "通道名称到相别的映射，如{'Bus1_V': 'A'}",
                        },
                        "ratio_map": {
                            "type": "object",
                            "description": "通道名称到变比的映射，如{'Bus1_V': [220.0, 1.0]}",
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "default": "./results/",
                            "description": "输出目录",
                        },
                        "filename": {
                            "type": "string",
                            "description": "文件名前缀（默认使用job_id）",
                        },
                        "file_type": {
                            "enum": ["BINARY", "ASCII"],
                            "default": "BINARY",
                            "description": "数据文件格式",
                        },
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "source": {
                "job_id": "",
                "plot_index": 0,
            },
            "comtrade": {
                "station_name": "CloudPSS",
                "rec_dev_id": "EMT",
                "rev_year": 1999,
                "frequency": 50.0,
                "time_mult": 1.0,
            },
            "channels": {
                "selected": [],
                "uu_map": {},
                "ph_map": {},
                "ratio_map": {},
            },
            "output": {
                "path": "./results/",
                "filename": "",
                "file_type": "BINARY",
            },
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        """验证配置"""
        result = ValidationResult(valid=True)

        source = config.get("source", {})
        job_id = source.get("job_id", "")

        if not job_id:
            result.add_error("必须提供source.job_id")
            result.add_error("  示例: 'job-12345678-abcd-1234-efgh-123456789012'")

        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行COMTRADE导出"""
        from cloudpss import setToken

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
            import os

            log("INFO", "加载认证信息...")
            auth = config.get("auth", {})
            token = auth.get("token")

            # 确定服务器和对应的 token 文件
            server = auth.get("server", "public")
            base_url = auth.get("base_url") or auth.get("baseUrl")

            # 设置 API URL
            if base_url:
                os.environ["CLOUDPSS_API_URL"] = base_url
            elif server == "internal":
                os.environ["CLOUDPSS_API_URL"] = "http://166.111.60.76:50001"
            else:
                os.environ["CLOUDPSS_API_URL"] = "https://cloudpss.net/"

            if not token:
                # 根据服务器选择 token 文件
                if server == "internal":
                    token_files = [".cloudpss_token_internal", ".cloudpss_token"]
                else:
                    token_files = [".cloudpss_token"]
                for token_file in token_files:
                    token_path = Path(token_file)
                    if token_path.exists():
                        token = token_path.read_text().strip()
                        break

            if not token:
                raise ValueError(
                    "未找到CloudPSS token，请提供auth.token或创建.cloudpss_token文件"
                )

            setToken(token)
            log("INFO", "认证成功")

            # 2. 获取任务结果
            source_config = config.get("source", {})
            job_id = source_config["job_id"]
            plot_index = source_config.get("plot_index", 0)

            log("INFO", f"获取任务结果: {job_id}")

            job, result = fetch_job_with_result(job_id)

            if result is None:
                raise RuntimeError("任务结果为空")

            # 获取波形数据
            plots = list(result.getPlots())
            if not plots:
                raise RuntimeError("没有波形数据")

            if plot_index >= len(plots):
                raise RuntimeError(
                    f"plot_index {plot_index} 超出范围，共有 {len(plots)} 个波形分组"
                )

            channel_names = result.getPlotChannelNames(plot_index)
            if not channel_names:
                raise RuntimeError("没有通道数据")

            log("INFO", f"找到 {len(channel_names)} 个通道")

            # 3. 获取配置参数
            comtrade_config = config.get("comtrade", {})
            channels_config = config.get("channels", {})
            output_config = config.get("output", {})

            station_name = comtrade_config.get("station_name", "CloudPSS")
            rec_dev_id = comtrade_config.get("rec_dev_id", "EMT")
            rev_year = comtrade_config.get("rev_year", 1999)
            frequency = comtrade_config.get("frequency", 50.0)
            time_mult = comtrade_config.get("time_mult", 1.0)

            # 4. 筛选通道
            selected_channels = channels_config.get("selected", [])
            if selected_channels:
                channels_to_export = [
                    ch for ch in channel_names if ch in selected_channels
                ]
                if not channels_to_export:
                    raise RuntimeError(f"指定的通道 {selected_channels} 未在结果中找到")
            else:
                channels_to_export = channel_names

            log("INFO", f"将导出 {len(channels_to_export)} 个通道")

            # 5. 收集数据
            log("INFO", "收集波形数据...")

            data_dict = {}  # channel_name -> {time: [], values: []}
            sampling_rate = None

            for channel in channels_to_export:
                channel_data = result.getPlotChannelData(plot_index, channel)
                if channel_data:
                    time_data = channel_data.get("x", [])
                    value_data = channel_data.get("y", [])

                    if time_data and value_data:
                        data_dict[channel] = {
                            "time": np.array(time_data),
                            "values": np.array(value_data),
                        }

                        # 计算采样率（假设均匀采样）
                        if len(time_data) > 1 and sampling_rate is None:
                            sampling_rate = 1.0 / (time_data[1] - time_data[0])

            if not data_dict:
                raise RuntimeError("没有获取到有效的波形数据")

            # 统一时间戳（取所有通道时间的并集）
            all_times = set()
            for ch_data in data_dict.values():
                all_times.update(ch_data["time"])
            sorted_times = sorted(all_times)

            log(
                "INFO",
                f"数据点数: {len(sorted_times)}, 采样率: {(sampling_rate or 1000.0):.2f} Hz",
            )

            # 6. 准备输出路径
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)

            filename = output_config.get("filename", "")
            if not filename:
                filename = f"comtrade_{job_id[:8]}"

            file_type = output_config.get("file_type", "BINARY")

            # 7. 构建通道信息
            uu_map = channels_config.get("uu_map", {})
            ph_map = channels_config.get("ph_map", {})
            ratio_map = channels_config.get("ratio_map", {})

            channel_info_list = []
            min_max_values = {}

            for idx, channel in enumerate(channels_to_export, start=1):
                # 确定单位
                uu = uu_map.get(channel, self._guess_unit(channel))

                # 确定相别
                ph = ph_map.get(channel, self._guess_phase(channel))

                # 获取变比
                ratio = ratio_map.get(channel, [1.0, 1.0])
                if isinstance(ratio, (int, float)):
                    ratio = [float(ratio), 1.0]

                # 计算最大最小值
                if channel in data_dict:
                    values = data_dict[channel]["values"]
                    min_val = float(np.min(values))
                    max_val = float(np.max(values))
                    min_max_values[channel] = (min_val, max_val)

                    # 计算转换因子A和B
                    # A = (max - min) / 8192, B = (max + min) / 2
                    a_factor = (
                        (max_val - min_val) / 8192.0 if max_val != min_val else 1.0
                    )
                    b_factor = (max_val + min_val) / 2.0
                else:
                    min_val, max_val = -32767, 32767
                    a_factor, b_factor = 1.0, 0.0

                channel_info = {
                    "An": idx,
                    "ch_id": channel[-64:] if len(channel) > 64 else channel,
                    "ph": ph,
                    "ccbm": channel[-64:] if len(channel) > 3 else channel,
                    "uu": uu,
                    "a": a_factor,
                    "b": b_factor,
                    "skew": 0.0,
                    "min": -32767,
                    "max": 32767,
                    "primary": ratio[0],
                    "secondary": ratio[1] if len(ratio) > 1 else 1.0,
                    "PS": "p",
                }
                channel_info_list.append(channel_info)

            # 8. 生成时间信息
            start_time_obj = datetime.now()
            start_time_str = start_time_obj.strftime("%d/%m/%Y,%H:%M:%S.%f")[:-3]
            end_time_obj = start_time_obj + timedelta(
                seconds=sorted_times[-1] if sorted_times else 0
            )
            end_time_str = end_time_obj.strftime("%d/%m/%Y,%H:%M:%S.%f")[:-3]

            # 9. 生成CFG文件
            log("INFO", "生成CFG配置文件...")

            cfg_content = self._generate_cfg(
                station_name=station_name,
                rec_dev_id=rec_dev_id,
                rev_year=rev_year,
                channel_info_list=channel_info_list,
                frequency=frequency,
                sampling_rate=sampling_rate if sampling_rate else 1000.0,
                num_samples=len(sorted_times),
                start_time=start_time_str,
                end_time=end_time_str,
                file_type=file_type,
                time_mult=time_mult,
            )

            cfg_path = output_path / f"{filename}.cfg"
            cfg_path.write_text(cfg_content, encoding="gb2312")

            artifacts.append(
                Artifact(
                    type="cfg",
                    path=str(cfg_path),
                    size=cfg_path.stat().st_size,
                    description="COMTRADE配置文件",
                )
            )

            log("INFO", f"CFG文件已保存: {cfg_path.name}")

            # 10. 生成DAT文件
            log("INFO", f"生成DAT数据文件 ({file_type})...")

            dat_path = output_path / f"{filename}.dat"

            if file_type == "BINARY":
                self._generate_dat_binary(
                    dat_path=dat_path,
                    sorted_times=sorted_times,
                    channels_to_export=channels_to_export,
                    data_dict=data_dict,
                    channel_info_list=channel_info_list,
                    time_mult=time_mult,
                )
            else:
                self._generate_dat_ascii(
                    dat_path=dat_path,
                    sorted_times=sorted_times,
                    channels_to_export=channels_to_export,
                    data_dict=data_dict,
                    channel_info_list=channel_info_list,
                    time_mult=time_mult,
                )

            artifacts.append(
                Artifact(
                    type="dat",
                    path=str(dat_path),
                    size=dat_path.stat().st_size,
                    description=f"COMTRADE数据文件({file_type})",
                )
            )

            log("INFO", f"DAT文件已保存: {dat_path.name}")

            # 11. 返回结果
            log("INFO", "COMTRADE导出完成")

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "job_id": job_id,
                    "channels_exported": len(channels_to_export),
                    "samples": len(sorted_times),
                    "sampling_rate_hz": sampling_rate or 1000.0,
                    "file_type": file_type,
                    "cfg_file": str(cfg_path),
                    "dat_file": str(dat_path),
                },
                artifacts=artifacts,
                logs=logs,
                metrics={
                    "channels": len(channels_to_export),
                    "samples": len(sorted_times),
                },
            )

        except (
            KeyError,
            AttributeError,
            ZeroDivisionError,
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

    def _guess_unit(self, channel_name: str) -> str:
        """根据通道名称猜测单位"""
        name_lower = channel_name.lower()
        if "_v" in name_lower or "voltage" in name_lower or "volt" in name_lower:
            return "kV"
        elif "_i" in name_lower or "current" in name_lower or "curr" in name_lower:
            return "kA"
        elif "_p" in name_lower or "power" in name_lower or "pow" in name_lower:
            return "MW"
        elif "_q" in name_lower or "var" in name_lower:
            return "Mvar"
        elif "freq" in name_lower or "f_" in name_lower:
            return "Hz"
        elif "angle" in name_lower or "delta" in name_lower:
            return "deg"
        else:
            return "pu"

    def _guess_phase(self, channel_name: str) -> str:
        """根据通道名称猜测相别"""
        name_lower = channel_name.lower()
        if "_a" in name_lower or "_0" in name_lower or "phase_a" in name_lower:
            return "A"
        elif "_b" in name_lower or "_1" in name_lower or "phase_b" in name_lower:
            return "B"
        elif "_c" in name_lower or "_2" in name_lower or "phase_c" in name_lower:
            return "C"
        elif "3p" in name_lower or "3phase" in name_lower:
            return "A"  # 三相量默认标记为A相
        else:
            return "A"

    def _generate_cfg(
        self,
        station_name: str,
        rec_dev_id: str,
        rev_year: int,
        channel_info_list: List[Dict],
        frequency: float,
        sampling_rate: float,
        num_samples: int,
        start_time: str,
        end_time: str,
        file_type: str,
        time_mult: float,
    ) -> str:
        """生成CFG文件内容"""
        lines = []

        # 第一行：厂站名称,记录装置标识,版本年号
        lines.append(f"{station_name},{rec_dev_id},{rev_year}")

        # 第二行：通道总数,模拟通道数A,状态通道数D
        total_channels = len(channel_info_list)
        analog_channels = total_channels
        digital_channels = 0
        lines.append(f"{total_channels},{analog_channels}A,{digital_channels}D")

        # 模拟通道信息行
        for ch in channel_info_list:
            line = (
                f"{ch['An']},{ch['ch_id']},{ch['ph']},{ch['ccbm']},{ch['uu']},"
                f"{ch['a']:.6f},{ch['b']:.6f},{ch['skew']:.6f},"
                f"{ch['min']},{ch['max']},{ch['primary']},{ch['secondary']},{ch['PS']}"
            )
            lines.append(line)

        # 频率行
        lines.append(f"{frequency:.6f}")

        # 采样率信息
        lines.append("1")  # 采样率个数
        lines.append(f"{sampling_rate:.6f},{num_samples}")

        # 开始时间和结束时间
        lines.append(start_time)
        lines.append(end_time)

        # 文件类型和时间倍率
        lines.append(file_type)
        lines.append(f"{time_mult:.6f}")

        return "\n".join(lines)

    def _generate_dat_binary(
        self,
        dat_path: Path,
        sorted_times: List[float],
        channels_to_export: List[str],
        data_dict: Dict[str, Dict],
        channel_info_list: List[Dict],
        time_mult: float,
    ):
        """生成二进制DAT文件"""
        with open(dat_path, "wb") as f:
            sample_num = 1
            for t in sorted_times:
                # 时间戳（微秒）
                timestamp = int(t * 1000000 / time_mult)

                # 写入采样序号和时间戳（32位整数）
                f.write(struct.pack("<I", sample_num))  # 小端序无符号32位
                f.write(struct.pack("<i", timestamp))  # 小端序有符号32位

                # 写入各通道数据（16位整数）
                for ch_info in channel_info_list:
                    channel = ch_info["ch_id"]
                    a_factor = ch_info["a"]
                    b_factor = ch_info["b"]

                    if channel in data_dict:
                        # 找到最接近当前时间的值
                        time_arr = data_dict[channel]["time"]
                        value_arr = data_dict[channel]["values"]

                        # 插值或找到最近的点
                        idx = np.argmin(np.abs(time_arr - t))
                        raw_value = value_arr[idx]

                        # 转换为整数值: (value - B) / A
                        if a_factor != 0:
                            int_value = int((raw_value - b_factor) / a_factor)
                        else:
                            int_value = 0

                        # 限制在16位范围内
                        int_value = max(-32767, min(32767, int_value))
                    else:
                        int_value = 0

                    f.write(struct.pack("<h", int_value))  # 小端序有符号16位

                sample_num += 1

    def _generate_dat_ascii(
        self,
        dat_path: Path,
        sorted_times: List[float],
        channels_to_export: List[str],
        data_dict: Dict[str, Dict],
        channel_info_list: List[Dict],
        time_mult: float,
    ):
        """生成ASCII DAT文件"""
        lines = []
        sample_num = 1

        for t in sorted_times:
            timestamp = int(t * 1000000 / time_mult)

            values = []
            for ch_info in channel_info_list:
                channel = ch_info["ch_id"]
                a_factor = ch_info["a"]
                b_factor = ch_info["b"]

                if channel in data_dict:
                    time_arr = data_dict[channel]["time"]
                    value_arr = data_dict[channel]["values"]
                    idx = np.argmin(np.abs(time_arr - t))
                    raw_value = value_arr[idx]

                    if a_factor != 0:
                        int_value = int((raw_value - b_factor) / a_factor)
                    else:
                        int_value = 0

                    int_value = max(-32767, min(32767, int_value))
                else:
                    int_value = 0

                values.append(int_value)

            line = f"{sample_num},{timestamp}," + ",".join(map(str, values))
            lines.append(line)
            sample_num += 1

        dat_path.write_text("\n".join(lines), encoding="utf-8")
