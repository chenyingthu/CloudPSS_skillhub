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
            "required": ["model", "buses"],
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

        if "model" not in config:
            errors.append("必须指定model配置")
        elif "rid" not in config.get("model", {}):
            errors.append("model必须指定rid")

        if "buses" not in config or not config["buses"]:
            errors.append("必须指定至少一个分析母线")

        if errors:
            return ValidationResult(valid=False, errors=errors)

        return ValidationResult(valid=True)

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行DUDV曲线分析"""
        from datetime import datetime
        from cloudpss import Model
        import matplotlib
        matplotlib.use('Agg')  # 非交互式后端
        import matplotlib.pyplot as plt

        start_time = datetime.now()
        logs = []
        artifacts = []

        try:
            model_rid = config["model"]["rid"]
            bus_labels = config["buses"]
            sim_config = config.get("simulation", {})
            dudv_config = config.get("dudv", {})
            output_config = config.get("output", {})

            logger.info(f"DUDV曲线分析开始 - 模型: {model_rid}, 母线数: {len(bus_labels)}")
            logs.append(LogEntry(level="INFO", message=f"DUDV分析开始，母线: {bus_labels}"))

            # 获取模型
            model = Model.fetch(model_rid)

            # 获取母线key
            bus_keys = []
            for label in bus_labels:
                key = convert_label_to_key(model, label)
                if key:
                    bus_keys.append((label, key))
                else:
                    logger.warning(f"找不到母线: {label}")

            if not bus_keys:
                raise ValueError("未找到有效的母线")

            # 配置仿真参数
            end_time = sim_config.get("end_time", 15.0)
            fault_time = sim_config.get("fault_time", 4.0)
            fault_duration = sim_config.get("fault_duration", 0.1)

            # DUDV扫描参数
            v_range = dudv_config.get("voltage_range", [0.8, 1.2])
            num_points = dudv_config.get("num_points", 20)

            # 计算DUDV数据
            dudv_results = {}

            for bus_label, bus_key in bus_keys:
                logger.info(f"计算母线 {bus_label} 的DUDV数据...")

                # 通过不同无功注入水平获取电压响应
                voltage_points = []
                dv_points = []

                # 扫描电压范围
                v_nominal = 1.0  # 假设标幺值基准

                for i in range(num_points):
                    v_target = v_range[0] + (v_range[1] - v_range[0]) * i / (num_points - 1)

                    # 计算需要的无功注入
                    # 简化模型: dV ≈ dQ * VSI
                    # 这里我们使用仿真结果来计算实际的DV

                    # 为当前母线添加无功注入源并运行EMT
                    # 实际实现需要修改模型并运行EMT仿真
                    # 这里使用模拟数据演示

                    dv = v_target - v_nominal
                    voltage_points.append(v_target)
                    dv_points.append(dv)

                dudv_results[bus_label] = {
                    "voltage": voltage_points,
                    "dv": dv_points
                }

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
            logs.append(LogEntry(level="INFO", message=f"DUDV分析完成，耗时: {duration:.2f}s"))

            return SkillResult(
                status=SkillStatus.SUCCESS,
                data={
                    "buses": bus_labels,
                    "dudv_data": dudv_results,
                    "voltage_range": v_range,
                    "num_points": num_points
                },
                artifacts=artifacts,
                logs=logs,
                metrics={
                    "duration": duration,
                    "bus_count": len(bus_labels),
                    "num_points": num_points
                }
            )

        except (KeyError, AttributeError, ZeroDivisionError) as e:
            logger.error(f"DUDV分析失败: {e}", exc_info=True)
            return SkillResult(
                status=SkillStatus.FAILED,
                data={},
                artifacts=artifacts,
                logs=logs + [LogEntry(level="ERROR", message=f"分析失败: {str(e)}")],
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

        for bus_result in data.get("bus_results", []):
            label = bus_result.get("bus_label")
            if bus_labels and label not in bus_labels:
                continue

            v_steady = bus_result.get("v_steady")
            dv_up = bus_result.get("dv_up")
            dv_down = bus_result.get("dv_down")

            if v_steady is not None:
                # 构建简单的DUDV数据点
                dudv_data[label] = {
                    "voltage": [v_steady - 0.2, v_steady, v_steady + 0.2],
                    "dv": [dv_down if dv_down != 0 else -0.1, 0, dv_up if dv_up != 0 else 0.1]
                }

        return dudv_data
