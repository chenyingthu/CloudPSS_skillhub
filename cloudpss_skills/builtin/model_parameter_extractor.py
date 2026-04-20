"""
Model Parameter Extractor Skill

模型参数提取器 - 提取电力系统模型中的元件参数

核心功能:
1. 按元件类型批量提取参数
2. 支持拓扑分析提取连接关系
3. 生成参数报告和CSV导出
4. 支持参数对比和差异分析

适用于:
- 模型参数文档化
- 参数校核和验证
- 模型版本对比
- 数据驱动的分析准备

参考自: 丁嘉俊 Get_Param_0311.py 工程脚本
"""

import csv
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field

from cloudpss_skills.core import (
    Artifact,
    LogEntry,
    SkillBase,
    SkillResult,
    SkillStatus,
    ValidationResult,
    register,
)
from cloudpss_skills.core.auth_utils import setup_auth

logger = logging.getLogger(__name__)


# CloudPSS标准元件RID定义
COMPONENT_DEFINITIONS = {
    "bus_3p": "model/CloudPSS/_newBus_3p",
    "line_3p": "model/CloudPSS/TransmissionLine",
    "transformer_3p": "model/CloudPSS/_newTransformer_3p2w",  # IEEE39中使用3p2w
    "generator": "model/CloudPSS/SyncGeneratorRouter",  # IEEE39中使用SyncGeneratorRouter
    "load": "model/CloudPSS/_newExpLoad_3p",  # IEEE39中使用ExpLoad
    "shunt": "model/CloudPSS/_newShuntLC_3p",
    "ac_source": "model/CloudPSS/_newACVoltageSource_3p",
    "fault": "model/CloudPSS/_newFault_3p",
}


@dataclass
class ComponentParameter:
    """元件参数"""

    comp_key: str
    comp_type: str
    comp_rid: str
    label: str
    args: Dict[str, Any]
    pins: Dict[str, Any]


@dataclass
class ParameterGroup:
    """参数分组"""

    group_name: str
    component_type: str
    parameters: List[ComponentParameter]
    common_args: Set[str] = field(default_factory=set)


@register
class ModelParameterExtractorSkill(SkillBase):
    """模型参数提取技能"""

    @property
    def name(self) -> str:
        return "model_parameter_extractor"

    @property
    def description(self) -> str:
        return "模型参数提取器 - 提取电力系统模型中的元件参数，支持拓扑分析和参数导出"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "model_parameter_extractor"},
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
                "extraction": {
                    "type": "object",
                    "properties": {
                        "component_types": {
                            "type": "array",
                            "items": {"enum": list(COMPONENT_DEFINITIONS.keys())},
                            "description": "要提取的元件类型",
                        },
                        "include_topology": {
                            "type": "boolean",
                            "default": True,
                            "description": "提取拓扑连接关系",
                        },
                        "include_all_args": {
                            "type": "boolean",
                            "default": False,
                            "description": "提取所有参数（包括空值）",
                        },
                        "filter_empty": {
                            "type": "boolean",
                            "default": True,
                            "description": "过滤空值参数",
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv", "both"], "default": "both"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "model_params"},
                        "group_by_type": {
                            "type": "boolean",
                            "default": True,
                            "description": "按元件类型分组导出",
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
            "extraction": {
                "component_types": list(COMPONENT_DEFINITIONS.keys()),
                "include_topology": True,
                "include_all_args": False,
                "filter_empty": True,
            },
            "output": {
                "format": "both",
                "path": "./results/",
                "prefix": "model_params",
                "group_by_type": True,
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

        extraction = config.get("extraction", {})
        comp_types = extraction.get("component_types", [])

        if not comp_types:
            result.add_error("至少指定一种要提取的元件类型")

        invalid_types = set(comp_types) - set(COMPONENT_DEFINITIONS.keys())
        if invalid_types:
            result.add_error(f"无效的元件类型: {invalid_types}")
            result.add_error(f"  有效类型: {list(COMPONENT_DEFINITIONS.keys())}")

        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行参数提取"""
        from cloudpss import Model

        start_time = datetime.now()
        logs = []
        artifacts = []
        extracted_params = []

        def log(level: str, message: str):
            logs.append(
                LogEntry(timestamp=datetime.now(), level=level, message=message)
            )
            getattr(logger, level.lower(), logger.info)(message)

        try:
            # 1. 认证
            setup_auth(config)
            log("INFO", "认证成功")

            # 2. 加载模型
            model_config = config.get("model", {})
            rid = model_config["rid"]
            source = model_config.get("source", "cloud")

            log("INFO", f"加载模型: {rid}")

            if source == "cloud":
                model = Model.fetch(rid)
            else:
                model = Model.load(rid)

            log("INFO", f"模型名称: {model.name}")

            # 3. 获取提取配置
            extraction_config = config.get("extraction", {})
            component_types = extraction_config.get(
                "component_types", list(COMPONENT_DEFINITIONS.keys())
            )
            include_topology = extraction_config.get("include_topology", True)
            include_all_args = extraction_config.get("include_all_args", False)
            filter_empty = extraction_config.get("filter_empty", True)

            output_config = config.get("output", {})
            group_by_type = output_config.get("group_by_type", True)

            # 4. 提取拓扑（如果需要）
            topology_data = {}
            if include_topology:
                log("INFO", "提取模型拓扑...")
                try:
                    topo = model.fetchTopology(
                        implementType="emtp", maximumDepth=0
                    ).toJSON()
                    topology_data = topo
                    log("INFO", f"  -> 拓扑组件数: {len(topo.get('components', {}))}")
                except (KeyError, AttributeError) as e:
                    log("WARN", f"拓扑提取失败: {e}")

            # 5. 按类型提取元件参数
            log("INFO", "提取元件参数...")
            all_components = []
            component_groups = {}

            for comp_type in component_types:
                comp_rid = COMPONENT_DEFINITIONS.get(comp_type)
                if not comp_rid:
                    continue

                log("INFO", f"  -> 提取 {comp_type} ({comp_rid})...")

                try:
                    components = model.getComponentsByRid(comp_rid)
                    comp_list = []

                    for comp_key, comp in components.items():
                        # 获取参数
                        args = (
                            dict(comp.args)
                            if hasattr(comp, "args") and comp.args
                            else {}
                        )

                        # 处理pins - 可能是dict、list或其他类型
                        pins = {}
                        if hasattr(comp, "pins") and comp.pins:
                            try:
                                if isinstance(comp.pins, dict):
                                    pins = dict(comp.pins)
                                elif isinstance(comp.pins, (list, tuple)):
                                    pins = {
                                        f"pin_{i}": v for i, v in enumerate(comp.pins)
                                    }
                                else:
                                    pins = {"pins": str(comp.pins)}
                            except Exception as e:
                                # 异常已捕获，无需额外处理
                                logger.debug(f"忽略预期异常: {e}")
                                pins = {}

                        # 过滤空值
                        if filter_empty and not include_all_args:
                            args = {
                                k: v
                                for k, v in args.items()
                                if v not in [None, "", [], {}]
                            }

                        comp_param = ComponentParameter(
                            comp_key=comp_key,
                            comp_type=comp_type,
                            comp_rid=comp_rid,
                            label=getattr(comp, "label", comp_key),
                            args=args,
                            pins=pins,
                        )
                        comp_list.append(comp_param)
                        all_components.append(comp_param)

                    if comp_list:
                        component_groups[comp_type] = comp_list
                        log("INFO", f"     找到 {len(comp_list)} 个{comp_type}")

                except (
                    AttributeError,
                    KeyError,
                    RuntimeError,
                    ValueError,
                    TypeError,
                    ConnectionError,
                    Exception,
                ) as e:
                    log("WARN", f"     提取失败: {e}")

            # 6. 提取拓扑连接信息
            connections = []
            if include_topology and topology_data:
                log("INFO", "提取连接关系...")
                components_data = topology_data.get("components", {})
                for comp_key, comp_data in components_data.items():
                    pins = comp_data.get("pins", {})
                    for pin_name, pin_id in pins.items():
                        if pin_id:
                            connections.append(
                                {
                                    "source_component": comp_key,
                                    "source_pin": pin_name,
                                    "pin_id": pin_id,
                                }
                            )

            # 7. 生成报告
            log("INFO", "生成参数报告...")
            report = self._generate_report(
                all_components, component_groups, connections, model
            )

            # 8. 导出结果
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "model_params")
            output_format = output_config.get("format", "both")

            # 导出JSON
            if output_format in ["json", "both"]:
                json_file = output_path / f"{prefix}.json"
                json_file.write_text(
                    json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
                )
                artifacts.append(
                    Artifact(
                        type="json",
                        path=str(json_file),
                        size=json_file.stat().st_size,
                        description="完整参数报告(JSON)",
                    )
                )
                log("INFO", f"  -> JSON报告: {json_file}")

            # 导出CSV
            if output_format in ["csv", "both"]:
                if group_by_type:
                    # 按类型分组导出
                    for comp_type, comp_list in component_groups.items():
                        csv_file = output_path / f"{prefix}_{comp_type}.csv"
                        self._export_csv_grouped(comp_list, csv_file)
                        artifacts.append(
                            Artifact(
                                type="csv",
                                path=str(csv_file),
                                size=csv_file.stat().st_size,
                                description=f"{comp_type}参数(CSV)",
                            )
                        )
                        log("INFO", f"  -> {comp_type} CSV: {csv_file}")
                else:
                    # 统一导出
                    csv_file = output_path / f"{prefix}_all.csv"
                    self._export_csv_all(all_components, csv_file)
                    artifacts.append(
                        Artifact(
                            type="csv",
                            path=str(csv_file),
                            size=csv_file.stat().st_size,
                            description="参数汇总(CSV)",
                        )
                    )
                    log("INFO", f"  -> 汇总 CSV: {csv_file}")

            # 统计
            total_count = len(all_components)
            type_counts = {t: len(c) for t, c in component_groups.items()}

            log("INFO", f"参数提取完成: 总计 {total_count} 个元件")
            for t, c in type_counts.items():
                log("INFO", f"  -> {t}: {c} 个")

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "model_rid": rid,
                    "model_name": model.name,
                    "total_components": total_count,
                    "type_counts": type_counts,
                    "connections_count": len(connections),
                },
                artifacts=artifacts,
                logs=logs,
            )

        except (
            AttributeError,
            KeyError,
            RuntimeError,
            ValueError,
            TypeError,
            FileNotFoundError,
            ConnectionError,
            Exception,
        ) as e:
            log("ERROR", f"执行失败: {e}")
            import traceback

            log("DEBUG", traceback.format_exc())
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "success": False,
                    "error": str(e),
                    "stage": "model_parameter_extractor",
                },
                artifacts=artifacts,
                logs=logs,
                error=str(e),
            )

    def _generate_report(
        self,
        all_components: List[ComponentParameter],
        component_groups: Dict[str, List[ComponentParameter]],
        connections: List[Dict],
        model: Any,
    ) -> Dict:
        """生成完整报告"""
        # 统计各类型参数
        type_summaries = {}
        for comp_type, comp_list in component_groups.items():
            if comp_list:
                # 收集所有可能的参数名
                all_args = set()
                for comp in comp_list:
                    all_args.update(comp.args.keys())

                type_summaries[comp_type] = {
                    "count": len(comp_list),
                    "common_parameters": list(all_args),
                }

        # 构建详细参数列表
        components_detail = []
        for comp in all_components:
            components_detail.append(
                {
                    "key": comp.comp_key,
                    "type": comp.comp_type,
                    "label": comp.label,
                    "args": comp.args,
                    "pins": comp.pins,
                }
            )

        return {
            "summary": {
                "model_rid": model.rid,
                "model_name": model.name,
                "total_components": len(all_components),
                "component_types": list(component_groups.keys()),
                "type_summaries": type_summaries,
                "connections_count": len(connections),
            },
            "components": components_detail,
            "connections": connections,
        }

    def _export_csv_grouped(self, components: List[ComponentParameter], filepath: Path):
        """按组导出CSV"""
        if not components:
            return

        # 收集所有可能的参数名
        all_fields = set()
        for comp in components:
            all_fields.update(comp.args.keys())
        all_fields = sorted(all_fields)

        # 写入CSV
        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            # 表头
            header = ["component_key", "label"] + all_fields
            writer.writerow(header)

            # 数据行
            for comp in components:
                row = [comp.comp_key, comp.label]
                for field in all_fields:
                    row.append(comp.args.get(field, ""))
                writer.writerow(row)

    def _export_csv_all(self, components: List[ComponentParameter], filepath: Path):
        """统一导出CSV"""
        if not components:
            return

        # 按类型组织
        by_type = {}
        for comp in components:
            if comp.comp_type not in by_type:
                by_type[comp.comp_type] = []
            by_type[comp.comp_type].append(comp)

        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["component_type", "component_key", "label", "parameter", "value"]
            )

            for comp_type, comp_list in by_type.items():
                for comp in comp_list:
                    for key, value in comp.args.items():
                        writer.writerow(
                            [comp_type, comp.comp_key, comp.label, key, value]
                        )
