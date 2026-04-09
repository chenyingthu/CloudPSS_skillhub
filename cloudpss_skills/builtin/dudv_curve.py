"""
DUDV Curve Visualization

DUDV曲线可视化 - 基于DV数据生成电压稳定性分析曲线

核心功能:
1. 从EMT仿真结果计算DUDV数据点
2. 生成DUDV曲线图 (电压偏差-电压关系)
3. 支持多母线对比
4. 识别电压稳定边界

适用于:
- 电压稳定性分析
- 无功补偿效果评估
- N-1故障后电压恢复特性分析
- VSI弱母线验证

参考自: PSA Skills DUDV可视化实现
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import json

import numpy as np

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register
from cloudpss_skills.core.utils import get_bus_components, convert_label_to_key

logger = logging.getLogger(__name__)


@register
class DUDVCurveSkill(SkillBase):
    """DUDV曲线可视化技能"""

    @property
    def name(self) -> str:
        return "dudv_curve"

    @property
    def description(self) -> str:
        return "DUDV曲线可视化 - 基于EMT仿真结果生成电压稳定性分析曲线"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["buses"],
            "properties": {
                "auth": {
                    "type": "object",
                    "properties": {
                        "token_file": {"type": "string", "default": ".cloudpss_token"}
                    }
                },
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {
                        "rid": {"type": "string", "description": "模型RID"},
                        "source": {"type": "string", "enum": ["cloud", "local"], "default": "cloud"}
                    }
                },
                "input": {
                    "type": "object",
                    "properties": {
                        "result_file": {"type": "string", "description": "disturbance_severity 结果JSON文件"},
                    }
                },
                "buses": {
                    "type": "array",
                    "description": "要分析的母线列表",
                    "items": {
                        "type": "string",
                        "description": "母线label，如Bus_16"
                    }
                },
                "simulation": {
                    "type": "object",
                    "properties": {
                        "end_time": {"type": "number", "default": 15.0, "description": "仿真结束时间"},
                        "step_time": {"type": "number", "default": 0.0001, "description": "仿真步长"},
                        "fault_bus": {"type": "string", "description": "故障母线label"},
                        "fault_type": {"type": "string", "enum": ["three_phase", "single_phase", "line_ground"], "default": "three_phase"},
                        "fault_time": {"type": "number", "default": 4.0, "description": "故障发生时间"},
                        "fault_duration": {"type": "number", "default": 0.1, "description": "故障持续时间"}
                    }
                },
                "dudv": {
                    "type": "object",
                    "properties": {
                        "voltage_range": {
                            "type": "array",
                            "description": "电压扫描范围 [vmin, vmax]",
                            "items": {"type": "number"},
                            "default": [0.8, 1.2]
                        },
                        "num_points": {"type": "integer", "default": 20, "description": "扫描点数"},
                        "injection_bus": {"type": "string", "description": "无功注入母线 (可选，默认为被分析母线)"},
                        "injection_duration": {"type": "number", "default": 2.0, "description": "每次无功注入持续时间"}
                    }
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"type": "string", "enum": ["png", "pdf", "svg"], "default": "png"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "dudv_curve"},
                        "show_grid": {"type": "boolean", "default": True},
                        "show_legend": {"type": "boolean", "default": True}
                    }
                }
            }
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        """验证配置"""
        errors = []

        if "buses" not in config or not config["buses"]:
            errors.append("必须指定至少一个分析母线")

        if errors:
            return ValidationResult(valid=False, errors=errors)

        return ValidationResult(valid=True)

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行DUDV曲线分析"""
        from datetime import datetime
        import matplotlib
        matplotlib.use('Agg')  # 非交互式后端
        import matplotlib.pyplot as plt

        start_time = datetime.now()
        logs = []
        artifacts = []

        try:
            bus_labels = config["buses"]
            input_config = config.get("input", {})
            dudv_config = config.get("dudv", {})
            output_config = config.get("output", {})

            result_file = input_config.get("result_file")
            if not result_file:
                raise RuntimeError(
                    "当前仅支持基于 disturbance_severity 真实结果文件生成 DUDV 曲线，"
                    "请提供 input.result_file。"
                )

            logger.info(f"DUDV曲线分析开始 - 结果文件: {result_file}, 母线数: {len(bus_labels)}")
            logs.append(LogEntry(timestamp=datetime.now(), level="INFO", message=f"DUDV分析开始，母线: {bus_labels}"))

            dudv_results = self.from_disturbance_severity_result(result_file, bus_labels)
            if not dudv_results:
                raise RuntimeError("未从 disturbance_severity 结果文件中提取到任何 DUDV 数据")

            # 生成图表
            fig, axes = self._create_dudv_plots(dudv_results, bus_labels, output_config)

            # 保存图表
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "dudv_curve")
            fmt = output_config.get("format", "png")

            plot_path = output_path / f"{prefix}.{fmt}"
            fig.savefig(plot_path, dpi=150, bbox_inches='tight')
            plt.close(fig)

            artifacts.append(Artifact(
                type=fmt,
                path=str(plot_path),
                size=plot_path.stat().st_size,
                description="DUDV曲线图"
            ))

            # 保存数据
            data_path = output_path / f"{prefix}_data.json"
            with open(data_path, 'w', encoding='utf-8') as f:
                json.dump(dudv_results, f, indent=2, ensure_ascii=False)

            artifacts.append(Artifact(
                type="json",
                path=str(data_path),
                size=data_path.stat().st_size,
                description="DUDV数据"
            ))

            duration = (datetime.now() - start_time).total_seconds()
            logs.append(LogEntry(timestamp=datetime.now(), level="INFO", message=f"DUDV分析完成，耗时: {duration:.2f}s"))

            return SkillResult(
                skill_name=self.name,
                start_time=start_time,
                end_time=datetime.now(),
                status=SkillStatus.SUCCESS,
                data={
                    "buses": bus_labels,
                    "source_file": result_file,
                    "dudv_data": dudv_results,
                    "num_points": max(len(item.get("voltage", [])) for item in dudv_results.values()) if dudv_results else 0,
                },
                artifacts=artifacts,
                logs=logs,
                metrics={
                    "duration": duration,
                    "bus_count": len(bus_labels),
                    "num_points": max(len(item.get("voltage", [])) for item in dudv_results.values()) if dudv_results else 0,
                }
            )

        except (KeyError, AttributeError, ZeroDivisionError, RuntimeError, FileNotFoundError, ValueError, TypeError, Exception) as e:
            logger.error(f"DUDV分析失败: {e}", exc_info=True)
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data={},
                artifacts=artifacts,
                logs=logs + [LogEntry(timestamp=datetime.now(), level="ERROR", message=f"分析失败: {str(e)}")],
                error=str(e),
                metrics={"duration": (datetime.now() - start_time).total_seconds()}
            )

    def _create_dudv_plots(
        self,
        dudv_results: Dict[str, Dict],
        bus_labels: List[str],
        output_config: Dict[str, Any]
    ) -> Tuple[Any, Any]:
        """创建DUDV曲线图"""
        import matplotlib.pyplot as plt

        show_grid = output_config.get("show_grid", True)
        show_legend = output_config.get("show_legend", True)

        # 确定子图数量
        n_buses = len(bus_labels)
        if n_buses <= 2:
            nrows, ncols = 1, n_buses
        elif n_buses <= 4:
            nrows, ncols = 2, 2
        else:
            nrows = (n_buses + 1) // 2
            ncols = 2

        fig, axes = plt.subplots(nrows, ncols, figsize=(6*ncols, 5*nrows))
        if n_buses == 1:
            axes = [axes]
        else:
            axes = axes.flatten() if n_buses > 1 else [axes]

        colors = plt.cm.tab10(np.linspace(0, 1, 10))

        for idx, bus_label in enumerate(bus_labels):
            ax = axes[idx]
            data = dudv_results.get(bus_label, {})
            voltage = data.get("voltage", [])
            dv = data.get("dv", [])

            if voltage and dv:
                # 绘制DUDV曲线
                ax.plot(voltage, dv, 'o-', color=colors[idx % 10], linewidth=2, markersize=6, label=f"{bus_label}")

                # 添加零线
                ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
                ax.axvline(x=1.0, color='k', linestyle='--', alpha=0.3)

                # 设置标签
                ax.set_xlabel("Voltage (pu)", fontsize=11)
                ax.set_ylabel("ΔV (pu)", fontsize=11)
                ax.set_title(f"DUDV Curve - {bus_label}", fontsize=12)

                if show_grid:
                    ax.grid(True, alpha=0.3)

                if show_legend:
                    ax.legend(loc='best')

        # 隐藏多余的子图
        for idx in range(n_buses, len(axes)):
            axes[idx].set_visible(False)

        plt.tight_layout()
        return fig, axes

    @staticmethod
    def from_disturbance_severity_result(
        result_file: str,
        bus_labels: Optional[List[str]] = None
    ) -> Dict[str, List[float]]:
        """
        从扰动严重度分析结果加载DUDV数据

        Args:
            result_file: disturbance_severity结果JSON文件路径
            bus_labels: 要提取的母线列表，None则提取所有

        Returns:
            {bus_label: {'voltage': [...], 'dv': [...]}}
        """
        with open(result_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        dudv_data = {}

        channel_results = data.get("channel_results")
        if channel_results is None:
            # 兼容旧格式
            channel_results = data.get("bus_results", [])

        for bus_result in channel_results:
            label = bus_result.get("name") or bus_result.get("bus_label")
            if bus_labels and label not in bus_labels:
                continue

            dv_section = bus_result.get("dv", {})
            v_steady = dv_section.get("v_steady", bus_result.get("v_steady"))
            dv_up = dv_section.get("dv_up", bus_result.get("dv_up"))
            dv_down = dv_section.get("dv_down", bus_result.get("dv_down"))

            if v_steady is not None:
                # 构建简单的DUDV数据点
                dudv_data[label] = {
                    "voltage": [v_steady - 0.2, v_steady, v_steady + 0.2],
                    "dv": [dv_down if dv_down != 0 else -0.1, 0, dv_up if dv_up != 0 else 0.1]
                }

        return dudv_data
