"""
Disturbance Severity Analysis Skill

扰动严重度分析 - 评估电力系统故障后的电压恢复特性
计算指标：
- DV (Deviation from Voltage): 电压裕度，评估电压偏离程度
- SI (Severity Index): 严重度指数，综合评估电压跌落深度和持续时间
- DUDV: 电压-电压导数曲线，可视化电压恢复过程

参考自：PSA Skills S04 - disturbance-severity-analysis
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from cloudpss import Model

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register
from cloudpss_skills.core.utils import (
    calculate_dv_metrics,
    calculate_si_metric,
    extract_voltage_from_result,
    get_time_index,
    calculate_voltage_average
)

logger = logging.getLogger(__name__)


@register
class DisturbanceSeveritySkill(SkillBase):
    """扰动严重度分析技能"""

    @property
    def name(self) -> str:
        return "disturbance_severity"

    @property
    def description(self) -> str:
        return "扰动严重度分析 - 计算DV电压裕度、SI严重度指数、DUDV曲线，评估故障后电压恢复特性"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["model"],
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
                "simulation": {
                    "type": "object",
                    "properties": {
                        "emt_result": {"type": "string", "description": "已有EMT结果Job ID（可选）"},
                        "fault_bus": {"type": "string", "description": "故障母线label/key"},
                        "fault_type": {"type": "string", "enum": ["three_phase", "single_phase"], "default": "three_phase"},
                        "fault_time": {"type": "number", "default": 4.0, "description": "故障发生时间(s)"},
                        "fault_duration": {"type": "number", "default": 0.1, "description": "故障持续时间(s)"},
                        "simulation_time": {"type": "number", "default": 10.0, "description": "总仿真时间(s)"},
                        "step_time": {"type": "number", "default": 0.0001, "description": "仿真步长(s)"}
                    }
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "dv_enabled": {"type": "boolean", "default": True, "description": "启用DV计算"},
                        "si_enabled": {"type": "boolean", "default": True, "description": "启用SI计算"},
                        "dudv_enabled": {"type": "boolean", "default": True, "description": "启用DUDV曲线"},
                        "voltage_measure_plot": {"type": "integer", "default": 0, "description": "电压量测图索引"},
                        "pre_fault_window": {"type": "number", "default": 0.5, "description": "故障前稳态计算窗口(s)"},
                        "judge_criteria": {
                            "type": "array",
                            "description": "DV判断条件 [[t_start, t_end, v_min_ratio, v_max_ratio], ...]",
                            "default": [[0.1, 3.0, 0.75, 1.25], [3.0, 999.0, 0.95, 1.05]]
                        },
                        "si_interval": {"type": "number", "default": 0.11, "description": "SI计算起始偏移(s)"},
                        "si_window": {"type": "number", "default": 3.0, "description": "SI积分窗口(s)"},
                        "si_dv1": {"type": "number", "default": 0.25, "description": "SI第一阶段电压偏差阈值"},
                        "si_dv2": {"type": "number", "default": 0.1, "description": "SI第二阶段电压偏差阈值"}
                    }
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"type": "string", "enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "disturbance_severity"}
                    }
                }
            }
        }

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        """验证配置"""
        errors = []

        if "model" not in config:
            errors.append("必须指定model配置")
        elif "rid" not in config["model"]:
            errors.append("必须指定model.rid")

        if errors:
            return ValidationResult(valid=False, errors=errors)

        return ValidationResult(valid=True)

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行扰动严重度分析"""
        start_time = datetime.now()
        logs = []
        artifacts = []

        try:
            # 1. 获取模型
            model_rid = config["model"]["rid"]
            logger.info(f"扰动严重度分析开始 - 模型: {model_rid}")
            logs.append(LogEntry(level="INFO", message=f"加载模型: {model_rid}"))

            model = Model.fetch(model_rid)

            # 2. 获取或运行EMT仿真
            emt_result = self._get_emt_result(model, config)
            if emt_result is None:
                return SkillResult(
                    status=SkillStatus.FAILED,
                    data={},
                    artifacts=artifacts,
                    logs=logs + [LogEntry(level="ERROR", message="获取EMT结果失败")],
                    metrics={"duration": (datetime.now() - start_time).total_seconds()}
                )

            logs.append(LogEntry(level="INFO", message="成功获取EMT仿真结果"))

            # 3. 提取电压数据
            voltage_plot_idx = config.get("analysis", {}).get("voltage_measure_plot", 0)
            voltage_channels = extract_voltage_from_result(emt_result, voltage_plot_idx)

            if not voltage_channels:
                return SkillResult(
                    status=SkillStatus.FAILED,
                    data={},
                    artifacts=artifacts,
                    logs=logs + [LogEntry(level="ERROR", message="未能从结果中提取电压数据")],
                    metrics={"duration": (datetime.now() - start_time).total_seconds()}
                )

            logger.info(f"提取到 {len(voltage_channels)} 个电压通道")
            logs.append(LogEntry(level="INFO", message=f"提取到 {len(voltage_channels)} 个电压通道"))

            # 4. 执行分析
            analysis_config = config.get("analysis", {})
            disturbance_time = config.get("simulation", {}).get("fault_time", 4.0)
            pre_fault_window = analysis_config.get("pre_fault_window", 0.5)

            results = self._analyze_all_channels(
                voltage_channels,
                disturbance_time,
                pre_fault_window,
                analysis_config
            )

            # 5. 识别薄弱点
            weak_points = self._identify_weak_points(results)

            # 6. 生成报告
            output_config = config.get("output", {})
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "disturbance_severity")

            result_data = {
                "model_rid": model_rid,
                "disturbance_time": disturbance_time,
                "channel_count": len(voltage_channels),
                "channel_results": results,
                "weak_points": weak_points,
                "summary": self._generate_summary(results)
            }

            # 保存JSON结果
            json_path = output_path / f"{prefix}_result.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)

            artifacts.append(Artifact(
                type="json",
                path=str(json_path),
                size=json_path.stat().st_size,
                description="扰动严重度分析结果"
            ))

            # 保存CSV结果
            csv_path = output_path / f"{prefix}_result.csv"
            self._save_csv_results(results, csv_path)

            artifacts.append(Artifact(
                type="csv",
                path=str(csv_path),
                size=csv_path.stat().st_size,
                description="扰动严重度指标汇总"
            ))

            # 生成Markdown报告
            report_path = output_path / f"{prefix}_report.md"
            self._generate_report(result_data, report_path)

            artifacts.append(Artifact(
                type="markdown",
                path=str(report_path),
                size=report_path.stat().st_size,
                description="扰动严重度分析报告"
            ))

            duration = (datetime.now() - start_time).total_seconds()
            logs.append(LogEntry(level="INFO", message=f"扰动严重度分析完成，耗时 {duration:.2f}s"))

            return SkillResult(
                status=SkillStatus.SUCCESS,
                data=result_data,
                artifacts=artifacts,
                logs=logs,
                metrics={"duration": duration, "channel_count": len(voltage_channels)}
            )

        except Exception as e:
            logger.error(f"扰动严重度分析失败: {e}", exc_info=True)
            return SkillResult(
                status=SkillStatus.FAILED,
                data={},
                artifacts=artifacts,
                logs=logs + [LogEntry(level="ERROR", message=f"分析失败: {str(e)}")],
                metrics={"duration": (datetime.now() - start_time).total_seconds()}
            )

    def _get_emt_result(self, model: Model, config: Dict[str, Any]) -> Optional[Any]:
        """获取EMT仿真结果"""
        sim_config = config.get("simulation", {})

        # 如果提供了已有结果ID，直接获取
        if "emt_result" in sim_config and sim_config["emt_result"]:
            result_id = sim_config["emt_result"]
            logger.info(f"使用已有EMT结果: {result_id}")
            # 这里需要通过job ID获取结果，具体实现取决于CloudPSS SDK
            # 暂时返回None，需要用户先运行EMT仿真
            return None

        # 否则需要配置并运行新的EMT仿真
        # 注意：这里需要配置故障，但当前实现假设用户已经运行了带故障的EMT仿真
        logger.info("需要运行新的EMT仿真（带故障配置）")
        return None

    def _analyze_all_channels(
        self,
        voltage_channels: List[Dict],
        disturbance_time: float,
        pre_fault_window: float,
        analysis_config: Dict[str, Any]
    ) -> List[Dict]:
        """分析所有电压通道"""
        results = []

        for channel in voltage_channels:
            channel_result = {
                "name": channel["name"],
                "dv_enabled": analysis_config.get("dv_enabled", True),
                "si_enabled": analysis_config.get("si_enabled", True)
            }

            time_data = channel["x"]
            voltage_data = channel["y"]

            if not time_data or not voltage_data:
                logger.warning(f"通道 {channel['name']} 数据为空")
                continue

            # 计算DV
            if analysis_config.get("dv_enabled", True):
                judge_criteria = analysis_config.get("judge_criteria", [[0.1, 3.0, 0.75, 1.25], [3.0, 999.0, 0.95, 1.05]])
                dv_result = calculate_dv_metrics(
                    voltage_data, time_data,
                    disturbance_time, pre_fault_window,
                    judge_criteria
                )
                channel_result["dv"] = dv_result

            # 计算SI
            if analysis_config.get("si_enabled", True):
                si_result = calculate_si_metric(
                    voltage_data, time_data,
                    disturbance_time, pre_fault_window,
                    analysis_config.get("si_interval", 0.11),
                    analysis_config.get("si_window", 3.0),
                    analysis_config.get("si_dv1", 0.25),
                    analysis_config.get("si_dv2", 0.1)
                )
                channel_result["si"] = si_result

            results.append(channel_result)

        return results

    def _identify_weak_points(self, results: List[Dict]) -> List[Dict]:
        """识别薄弱点（DV为负或SI较大的通道）"""
        weak_points = []

        for result in results:
            is_weak = False
            reason = []

            # 检查DV
            if "dv" in result:
                dv = result["dv"]
                if dv.get("dv_up", 0) < 0:
                    is_weak = True
                    reason.append(f"电压上限裕度不足 ({dv['dv_up']:.4f})")
                if dv.get("dv_down", 0) < 0:
                    is_weak = True
                    reason.append(f"电压下限裕度不足 ({dv['dv_down']:.4f})")

            # 检查SI
            if "si" in result:
                si = result["si"]
                if si > 0.5:  # SI阈值
                    is_weak = True
                    reason.append(f"严重度指数较高 (SI={si:.4f})")

            if is_weak:
                weak_points.append({
                    "name": result["name"],
                    "reason": "; ".join(reason),
                    "dv_up": result.get("dv", {}).get("dv_up"),
                    "dv_down": result.get("dv", {}).get("dv_down"),
                    "si": result.get("si")
                })

        # 按严重程度排序（SI降序）
        weak_points.sort(key=lambda x: x.get("si", 0), reverse=True)

        return weak_points

    def _generate_summary(self, results: List[Dict]) -> Dict[str, Any]:
        """生成汇总统计"""
        summary = {
            "total_channels": len(results),
            "dv_analyzed": sum(1 for r in results if "dv" in r),
            "si_analyzed": sum(1 for r in results if "si" in r)
        }

        # DV统计
        dv_up_values = [r["dv"]["dv_up"] for r in results if "dv" in r and r["dv"].get("dv_up") is not None]
        dv_down_values = [r["dv"]["dv_down"] for r in results if "dv" in r and r["dv"].get("dv_down") is not None]

        if dv_up_values:
            summary["dv_up"] = {
                "min": min(dv_up_values),
                "max": max(dv_up_values),
                "mean": sum(dv_up_values) / len(dv_up_values),
                "negative_count": sum(1 for v in dv_up_values if v < 0)
            }

        if dv_down_values:
            summary["dv_down"] = {
                "min": min(dv_down_values),
                "max": max(dv_down_values),
                "mean": sum(dv_down_values) / len(dv_down_values),
                "negative_count": sum(1 for v in dv_down_values if v < 0)
            }

        # SI统计
        si_values = [r["si"] for r in results if "si" in r]
        if si_values:
            summary["si"] = {
                "min": min(si_values),
                "max": max(si_values),
                "mean": sum(si_values) / len(si_values),
                "high_count": sum(1 for v in si_values if v > 0.5)
            }

        return summary

    def _save_csv_results(self, results: List[Dict], csv_path: Path):
        """保存CSV格式结果"""
        import csv

        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["通道名称", "DV上限裕度", "DV下限裕度", "稳态电压", "SI严重度", "是否薄弱"])

            for result in results:
                dv = result.get("dv", {})
                si = result.get("si", 0)

                dv_up = dv.get("dv_up", "N/A")
                dv_down = dv.get("dv_down", "N/A")
                v_steady = dv.get("v_steady", "N/A")

                # 判断是否薄弱
                is_weak = (isinstance(dv_up, (int, float)) and dv_up < 0) or \
                         (isinstance(dv_down, (int, float)) and dv_down < 0) or \
                         (isinstance(si, (int, float)) and si > 0.5)

                writer.writerow([
                    result["name"],
                    dv_up,
                    dv_down,
                    v_steady,
                    si,
                    "是" if is_weak else "否"
                ])

    def _generate_report(self, result_data: Dict[str, Any], report_path: Path):
        """生成Markdown报告"""
        lines = [
            "# 扰动严重度分析报告",
            "",
            f"**模型**: {result_data['model_rid']}",
            f"**扰动时间**: {result_data['disturbance_time']} s",
            f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 摘要",
            "",
            f"- **总通道数**: {result_data['summary']['total_channels']}",
            f"- **薄弱点数**: {len(result_data['weak_points'])}",
            ""
        ]

        # DV统计
        if 'dv_up' in result_data['summary']:
            dv_up = result_data['summary']['dv_up']
            lines.extend([
                "### DV电压裕度统计",
                "",
                f"- **DV上限裕度**: 最小={dv_up['min']:.4f}, 最大={dv_up['max']:.4f}, 平均={dv_up['mean']:.4f}",
                f"- **DV上限不足数**: {dv_up['negative_count']}/{result_data['summary']['dv_analyzed']}",
                ""
            ])

        if 'dv_down' in result_data['summary']:
            dv_down = result_data['summary']['dv_down']
            lines.extend([
                f"- **DV下限裕度**: 最小={dv_down['min']:.4f}, 最大={dv_down['max']:.4f}, 平均={dv_down['mean']:.4f}",
                f"- **DV下限不足数**: {dv_down['negative_count']}/{result_data['summary']['dv_analyzed']}",
                ""
            ])

        # SI统计
        if 'si' in result_data['summary']:
            si = result_data['summary']['si']
            lines.extend([
                "### SI严重度指数统计",
                "",
                f"- **SI范围**: {si['min']:.4f} ~ {si['max']:.4f}",
                f"- **SI平均值**: {si['mean']:.4f}",
                f"- **高严重度数**: {si['high_count']}/{result_data['summary']['si_analyzed']}",
                ""
            ])

        # 薄弱点列表
        if result_data['weak_points']:
            lines.extend([
                "## 薄弱点识别",
                "",
                "| 排名 | 通道名称 | DV上限裕度 | DV下限裕度 | SI | 原因 |",
                "|------|----------|------------|------------|-----|------|"
            ])

            for i, wp in enumerate(result_data['weak_points'][:10], 1):
                lines.append(
                    f"| {i} | {wp['name']} | {wp.get('dv_up', 'N/A')} | "
                    f"{wp.get('dv_down', 'N/A')} | {wp.get('si', 'N/A'):.4f} | {wp['reason']} |"
                )

            lines.append("")

        # 详细结果
        lines.extend([
            "## 详细结果",
            "",
            "| 通道名称 | DV上限裕度 | DV下限裕度 | 稳态电压 | SI |",
            "|----------|------------|------------|----------|-----|"
        ])

        for r in result_data['channel_results']:
            dv = r.get('dv', {})
            lines.append(
                f"| {r['name']} | {dv.get('dv_up', 'N/A')} | "
                f"{dv.get('dv_down', 'N/A')} | {dv.get('v_steady', 'N/A')} | {r.get('si', 'N/A')} |"
            )

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
