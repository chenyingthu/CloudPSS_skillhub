"""
Contingency Analysis Skill

预想事故分析 - 系统性评估电网在多种故障工况下的安全裕度
支持N-1、N-2、N-K故障，故障排序，薄弱环节识别
"""

import json
import logging
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register

logger = logging.getLogger(__name__)


@register
class ContingencyAnalysisSkill(SkillBase):
    """预想事故分析技能"""

    @property
    def name(self) -> str:
        return "contingency_analysis"

    @property
    def description(self) -> str:
        return "预想事故分析 - 评估N-K故障下的系统安全裕度，识别薄弱环节"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "contingency_analysis"},
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
                        "rid": {"type": "string"},
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                    },
                },
                "contingency": {
                    "type": "object",
                    "properties": {
                        "level": {
                            "enum": ["N-1", "N-2", "N-K"],
                            "default": "N-1",
                            "description": "故障级别"
                        },
                        "k": {"type": "integer", "default": 1, "description": "N-K中的K值"},
                        "components": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "待故障元件列表，空表示全部"
                        },
                        "component_types": {
                            "type": "array",
                            "items": {"enum": ["branch", "generator", "load", "transformer"]},
                            "default": ["branch"],
                            "description": "故障元件类型"
                        },
                        "max_combinations": {
                            "type": "integer",
                            "default": 100,
                            "description": "最大故障组合数"
                        },
                    },
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "check_voltage": {"type": "boolean", "default": True},
                        "check_thermal": {"type": "boolean", "default": True},
                        "check_transient": {"type": "boolean", "default": False},
                        "voltage_limit": {
                            "type": "object",
                            "properties": {
                                "min": {"type": "number", "default": 0.95},
                                "max": {"type": "number", "default": 1.05},
                            },
                        },
                        "thermal_limit": {"type": "number", "default": 1.0},
                        "severity_threshold": {
                            "type": "number",
                            "default": 0.8,
                            "description": "严重度阈值(0-1)"
                        },
                    },
                },
                "ranking": {
                    "type": "object",
                    "properties": {
                        "method": {
                            "enum": ["severity", "overload", "violation_count"],
                            "default": "severity"
                        },
                        "top_n": {"type": "integer", "default": 10},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "contingency"},
                        "generate_report": {"type": "boolean", "default": True},
                        "export_all_cases": {"type": "boolean", "default": False},
                    },
                },
            },
        }

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "model/holdme/IEEE39", "source": "cloud"},
            "contingency": {
                "level": "N-1",
                "k": 1,
                "components": [],
                "component_types": ["branch"],
                "max_combinations": 100,
            },
            "analysis": {
                "check_voltage": True,
                "check_thermal": True,
                "check_transient": False,
                "voltage_limit": {"min": 0.95, "max": 1.05},
                "thermal_limit": 1.0,
                "severity_threshold": 0.8,
            },
            "ranking": {
                "method": "severity",
                "top_n": 10,
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "prefix": "contingency",
                "generate_report": True,
                "export_all_cases": False,
            },
        }

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行预想事故分析"""
        from cloudpss import Model, setToken

        start_time = datetime.now()
        logs = []
        artifacts = []

        def log(level: str, message: str):
            logs.append(LogEntry(timestamp=datetime.now(), level=level, message=message))
            getattr(logger, level.lower(), logger.info)(message)

        try:
            log("INFO", "加载认证...")
            auth = config.get("auth", {})
            token = auth.get("token")
            if not token:
                token_file = auth.get("token_file", ".cloudpss_token")
                token_path = Path(token_file)
                if not token_path.exists():
                    raise FileNotFoundError(f"Token文件不存在: {token_file}")
                token = token_path.read_text().strip()
            setToken(token)
            log("INFO", "认证成功")

            model_config = config["model"]
            model_rid = model_config["rid"]
            model_source = model_config.get("source", "cloud")
            if model_source == "local":
                base_model = Model.load(model_rid)
            else:
                base_model = Model.fetch(model_rid)
            log("INFO", f"模型: {base_model.name}")

            # 获取配置参数
            contingency_config = config.get("contingency", {})
            analysis_config = config.get("analysis", {})
            ranking_config = config.get("ranking", {})
            output_config = config.get("output", {})

            level = contingency_config.get("level", "N-1")
            k = contingency_config.get("k", 1)
            component_types = contingency_config.get("component_types", ["branch"])
            max_combinations = contingency_config.get("max_combinations", 100)

            voltage_limit = analysis_config.get("voltage_limit", {"min": 0.95, "max": 1.05})
            thermal_limit = analysis_config.get("thermal_limit", 1.0)
            severity_threshold = analysis_config.get("severity_threshold", 0.8)

            ranking_method = ranking_config.get("method", "severity")
            top_n = ranking_config.get("top_n", 10)

            log("INFO", f"预想事故分析: {level}")
            log("INFO", f"故障元件类型: {', '.join(component_types)}")
            log("INFO", f"电压限值: {voltage_limit['min']:.3f} - {voltage_limit['max']:.3f} pu")
            log("INFO", f"热稳定限值: {thermal_limit:.3f} pu")

            # 获取基态潮流结果
            log("INFO", "计算基态潮流...")
            base_job = base_model.runPowerFlow()
            import time
            while True:
                status = base_job.status()
                if status == 1:
                    break
                if status == 2:
                    raise RuntimeError("基态潮流计算失败")
                time.sleep(1)

            base_result = base_job.result
            base_buses_raw = base_result.getBuses()
            base_branches_raw = base_result.getBranches()

            # Parse table format
            base_buses = self._parse_table(base_buses_raw)
            base_branches = self._parse_table(base_branches_raw)

            log("INFO", f"基态: {len(base_buses)} 节点, {len(base_branches)} 支路")

            # 生成故障组合
            log("INFO", "生成故障组合...")
            contingencies = self._generate_contingencies(
                base_model, component_types, level, k,
                contingency_config.get("components", []),
                max_combinations
            )
            log("INFO", f"共 {len(contingencies)} 个故障场景")

            if not contingencies:
                raise ValueError("未生成有效的故障场景")

            # 逐一评估故障场景
            log("INFO", "开始故障评估...")
            results = []
            passed = 0
            failed = 0

            for i, contingency in enumerate(contingencies, 1):
                try:
                    log("INFO", f"[{i}/{len(contingencies)}] {contingency['name']}")

                    result = self._evaluate_contingency(
                        model_rid, model_source, contingency,
                        voltage_limit, thermal_limit,
                        base_buses, base_branches,
                        log
                    )

                    results.append(result)

                    if result["status"] == "PASS":
                        passed += 1
                    else:
                        failed += 1

                except Exception as e:
                    log("WARNING", f"故障评估失败 {contingency['name']}: {e}")
                    results.append({
                        "name": contingency['name'],
                        "components": contingency['components'],
                        "status": "ERROR",
                        "error": str(e),
                    })

            # 计算严重度并排序
            log("INFO", "计算严重度并排序...")
            for result in results:
                if result.get("status") not in ["ERROR"]:
                    result["severity"] = self._calculate_severity(result, voltage_limit, thermal_limit)

            # 排序
            valid_results = [r for r in results if "severity" in r]
            valid_results.sort(key=lambda x: x["severity"], reverse=True)

            # 生成汇总
            summary = {
                "total_cases": len(contingencies),
                "passed": passed,
                "failed": failed,
                "errors": len(contingencies) - passed - failed,
                "pass_rate": round(passed / len(contingencies) * 100, 2) if contingencies else 0,
                "severe_cases": len([r for r in valid_results if r.get("severity", 0) >= severity_threshold]),
            }

            # 脆弱环节识别
            weak_points = self._identify_weak_points(valid_results, top_n)

            log("INFO", f"通过: {passed}/{len(contingencies)} ({summary['pass_rate']}%)")
            log("INFO", f"严重故障: {summary['severe_cases']} 个")

            # 准备输出数据
            result_data = {
                "model": base_model.name,
                "contingency_level": level,
                "summary": summary,
                "weak_points": weak_points,
                "top_severe_cases": valid_results[:top_n],
                "all_results": results if output_config.get("export_all_cases", False) else None,
            }

            # 导出结果
            output_path = Path(output_config.get("path", "./results/"))
            output_path.mkdir(parents=True, exist_ok=True)
            prefix = output_config.get("prefix", "contingency")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # JSON输出
            json_path = output_path / f"{prefix}_{timestamp}.json"
            with open(json_path, 'w') as f:
                json.dump(result_data, f, indent=2)
            artifacts.append(Artifact(type="json", path=str(json_path), size=json_path.stat().st_size, description="预想事故分析结果"))

            # CSV输出
            csv_path = output_path / f"{prefix}_{timestamp}.csv"
            self._export_csv(valid_results, csv_path)
            artifacts.append(Artifact(type="csv", path=str(csv_path), size=csv_path.stat().st_size, description="故障案例汇总"))

            # 生成报告
            if output_config.get("generate_report", True):
                report_path = output_path / f"{prefix}_report_{timestamp}.md"
                self._generate_report(result_data, report_path, voltage_limit, thermal_limit)
                artifacts.append(Artifact(type="markdown", path=str(report_path), size=report_path.stat().st_size, description="预想事故分析报告"))

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts,
                logs=logs,
            )

        except Exception as e:
            log("ERROR", f"执行失败: {e}")
            import traceback
            log("DEBUG", traceback.format_exc())
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

    def _generate_contingencies(self, model, component_types: List[str],
                                level: str, k: int,
                                specified_components: List[str],
                                max_combinations: int) -> List[Dict]:
        """生成故障组合"""
        from itertools import combinations

        contingencies = []

        # 从拓扑获取组件
        try:
            topology = model.fetchTopology(implementType="powerflow")
            topology_dict = topology.toJSON()
            components = topology_dict.get("components", [])
        except Exception:
            # 如果获取拓扑失败，尝试直接从模型获取
            model_dict = model.toJSON()
            components = model_dict.get("components", [])

        # 收集可用元件
        available = []
        for comp_key, comp in components.items() if isinstance(components, dict) else [(c.get('key', ''), c) for c in components]:
            if isinstance(comp, dict):
                comp_type = self._get_component_type(comp)
                if comp_type in component_types:
                    key = comp.get("key", comp_key if isinstance(comp_key, str) else "")
                    name = comp.get("name", comp.get("label", key))
                    if not specified_components or key in specified_components or name in specified_components:
                        available.append({
                            "key": key,
                            "name": name,
                            "type": comp_type,
                        })

        if not available:
            return []

        # 根据级别生成组合
        if level == "N-1":
            k = 1
        elif level == "N-2":
            k = 2
        # N-K 使用指定的k值

        k = min(k, len(available))

        for combo in combinations(available, k):
            keys = [c["key"] for c in combo]
            names = [c["name"] for c in combo]
            contingencies.append({
                "name": " + ".join(names),
                "components": keys,
            })

            if len(contingencies) >= max_combinations:
                break

        return contingencies

    def _get_component_type(self, component: Dict) -> str:
        """获取元件类型"""
        key = component.get("key", "")
        name = component.get("name", "").lower()
        label = component.get("label", "").lower()
        definition = component.get("definition", "").lower()

        # 根据definition判断（最可靠）
        if "line" in definition or "线路" in definition:
            return "branch"
        elif "generator" in definition or "gen" in definition or "发电机" in definition:
            return "generator"
        elif "load" in definition or "负荷" in definition:
            return "load"
        elif "transformer" in definition or "变压器" in definition:
            return "transformer"

        # 根据label判断
        if label.startswith("line") or label.startswith("线路"):
            return "branch"
        elif label.startswith("gen") or label.startswith("发电机"):
            return "generator"
        elif label.startswith("load") or label.startswith("负荷"):
            return "load"
        elif label.startswith("transformer") or label.startswith("变压器"):
            return "transformer"

        # 根据key判断
        if key.startswith("Line") or key.startswith("line") or key.startswith("/line"):
            return "branch"
        elif key.startswith("Gen") or key.startswith("gen") or key.startswith("/gen"):
            return "generator"
        elif key.startswith("Load") or key.startswith("load") or key.startswith("/load"):
            return "load"
        elif key.startswith("Transformer") or key.startswith("transformer") or key.startswith("/transformer"):
            return "transformer"

        # 默认为其他类型
        return "other"

    def _evaluate_contingency(self, model_rid: str, model_source: str, contingency: Dict,
                              voltage_limit: Dict, thermal_limit: float,
                              base_buses: List, base_branches: List,
                              log_func) -> Dict:
        """评估单个故障场景"""
        from cloudpss import Model

        result = {
            "name": contingency["name"],
            "components": contingency["components"],
            "status": "PASS",
            "violations": [],
        }

        # 重新加载原始模型（每次重新加载以确保干净状态）
        if model_source == "local":
            working_model = Model.load(model_rid)
        else:
            working_model = Model.fetch(model_rid)

        for comp_key in contingency["components"]:
            try:
                # Remove leading '/' if present (fetchTopology adds it, but removeComponent doesn't need it)
                clean_key = comp_key.lstrip('/')
                working_model.removeComponent(clean_key)
            except Exception as e:
                log_func("WARNING", f"无法移除元件 {comp_key}: {e}")

        # DEBUG: Check component count
        try:
            all_comps = working_model.getAllComponents()
            log_func("INFO", f"Model has {len(all_comps)} components after removal")
        except Exception as e:
            log_func("WARNING", f"Could not get component count: {e}")

        # 运行潮流计算
        job = working_model.runPowerFlow()

        import time
        max_wait = 30
        waited = 0
        while waited < max_wait:
            status = job.status()
            if status == 1:
                break
            if status == 2:
                result["status"] = "FAIL"
                result["violations"].append({
                    "type": "CONVERGENCE",
                    "description": "潮流计算不收敛",
                })
                return result
            time.sleep(1)
            waited += 1

        if waited >= max_wait:
            result["status"] = "TIMEOUT"
            return result

        # 获取结果
        pf_result = job.result
        buses_raw = pf_result.getBuses()
        branches_raw = pf_result.getBranches()

        # Parse table format
        buses = self._parse_table(buses_raw)
        branches = self._parse_table(branches_raw)

        # 电压检查
        voltage_violations = []
        min_voltage = float('inf')
        max_voltage = float('-inf')

        # Find voltage column name (handles HTML encoding)
        voltage_col = None
        if buses and len(buses) > 0:
            for key in buses[0].keys():
                if 'm' in key.lower() and 'pu' in key.lower():
                    voltage_col = key
                    break

        for bus in buses:
            # Get voltage magnitude from Vm / pu column (handles HTML encoding)
            if voltage_col:
                v = abs(bus.get(voltage_col, 1.0))
            else:
                v = 1.0
            bus_name = bus.get("Bus", bus.get("name", "Unknown"))
            min_voltage = min(min_voltage, v)
            max_voltage = max(max_voltage, v)

            if v < voltage_limit["min"]:
                voltage_violations.append({
                    "bus": bus_name,
                    "voltage": round(v, 4),
                    "limit": f"<{voltage_limit['min']}",
                })
            elif v > voltage_limit["max"]:
                voltage_violations.append({
                    "bus": bus_name,
                    "voltage": round(v, 4),
                    "limit": f">{voltage_limit['max']}",
                })

        result["min_voltage"] = round(min_voltage, 4) if min_voltage != float('inf') else 1.0
        result["max_voltage"] = round(max_voltage, 4) if max_voltage != float('-inf') else 1.0

        if voltage_violations:
            result["status"] = "VIOLATION"
            result["violations"].extend([
                {"type": "VOLTAGE", "details": v} for v in voltage_violations[:5]
            ])

        # 热稳定检查
        thermal_violations = []
        max_loading = 0.0

        # Find power column names (handles HTML encoding)
        p_col = None
        q_col = None
        rate_a_col = None
        if branches and len(branches) > 0:
            for key in branches[0].keys():
                if 'p' in key.lower() and 'mw' in key.lower():
                    p_col = key
                if 'q' in key.lower() and 'mvar' in key.lower():
                    q_col = key
                if 'rate' in key.lower() or 'rating' in key.lower():
                    rate_a_col = key

        for branch in branches:
            # Get loading - either from loading column or calculate from P/Q
            loading = branch.get("loading", 0.0)
            if loading == 0.0 and p_col and q_col:
                # Calculate from P and Q
                p = branch.get(p_col, 0.0)
                q = branch.get(q_col, 0.0)
                s = (p**2 + q**2)**0.5
                # Assume 100 MVA base if no rating available
                base_mva = 100.0
                loading = s / base_mva if base_mva > 0 else 0.0
            branch_name = branch.get("Branch", branch.get("name", "Unknown"))
            max_loading = max(max_loading, loading)

            if loading > thermal_limit:
                thermal_violations.append({
                    "branch": branch_name,
                    "loading": round(loading * 100, 2),
                    "limit": f"{thermal_limit * 100}%",
                })

        result["max_loading"] = round(max_loading * 100, 2)

        if thermal_violations:
            result["status"] = "VIOLATION"
            result["violations"].extend([
                {"type": "THERMAL", "details": t} for t in thermal_violations[:5]
            ])

        return result

    def _parse_table(self, table_data: List[Dict]) -> List[Dict]:
        """Parse CloudPSS table format to list of dicts

        CloudPSS returns table format:
        [{'type': 'table', 'data': {'columns': [
            {'name': 'Bus', 'data': ['Bus1', 'Bus2', ...]},
            {'name': 'Vm / pu', 'data': [1.027, 0.987, ...]},
            {'name': 'Va / deg', 'data': [...]}
        ]}}]

        Returns:
            List of dicts with column names as keys
        """
        if not table_data or len(table_data) == 0:
            return []

        table = table_data[0]
        if table.get('type') != 'table':
            # Already in expected format (list of dicts)
            return table_data

        columns = table['data']['columns']
        if not columns:
            return []

        # Convert column-oriented data to row-oriented dicts
        num_rows = len(columns[0]['data']) if columns else 0
        rows = []
        for i in range(num_rows):
            row = {}
            for col in columns:
                row[col['name']] = col['data'][i]
            rows.append(row)

        return rows

    def _calculate_severity(self, result: Dict, voltage_limit: Dict, thermal_limit: float) -> float:
        """计算故障严重度 (0-1)"""
        severity = 0.0

        if result.get("status") == "FAIL":
            return 1.0

        if result.get("status") == "TIMEOUT":
            return 0.9

        # 电压越界严重度
        min_v = result.get("min_voltage", 1.0)
        max_v = result.get("max_voltage", 1.0)

        if min_v < voltage_limit["min"]:
            severity = max(severity, (voltage_limit["min"] - min_v) / voltage_limit["min"])
        if max_v > voltage_limit["max"]:
            severity = max(severity, (max_v - voltage_limit["max"]) / (1.1 - voltage_limit["max"]))

        # 热稳定越界严重度
        max_loading = result.get("max_loading", 0.0) / 100.0
        if max_loading > thermal_limit:
            severity = max(severity, (max_loading - thermal_limit) / thermal_limit)

        return round(min(severity, 1.0), 4)

    def _identify_weak_points(self, results: List[Dict], top_n: int) -> List[Dict]:
        """识别系统薄弱环节"""
        # 统计元件出现在严重故障中的次数
        component_count = {}

        for result in results[:top_n]:
            for comp in result.get("components", []):
                component_count[comp] = component_count.get(comp, 0) + 1

        # 排序
        weak_points = [
            {"component": comp, "critical_cases": count}
            for comp, count in sorted(component_count.items(), key=lambda x: x[1], reverse=True)
        ]

        return weak_points[:top_n]

    def _export_csv(self, results: List[Dict], path: Path):
        """导出CSV"""
        import csv

        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "rank", "contingency", "status", "severity",
                "min_voltage_pu", "max_voltage_pu", "max_loading_pct",
                "violation_count"
            ])

            for i, result in enumerate(results, 1):
                writer.writerow([
                    i,
                    result.get("name", ""),
                    result.get("status", ""),
                    result.get("severity", 0),
                    result.get("min_voltage", ""),
                    result.get("max_voltage", ""),
                    result.get("max_loading", ""),
                    len(result.get("violations", [])),
                ])

    def _generate_report(self, data: Dict, path: Path, voltage_limit: Dict, thermal_limit: float):
        """生成Markdown报告"""
        summary = data.get("summary", {})
        weak_points = data.get("weak_points", [])
        top_cases = data.get("top_severe_cases", [])

        lines = [
            "# 预想事故分析报告",
            "",
            f"**模型**: {data.get('model', 'Unknown')}",
            f"**故障级别**: {data.get('contingency_level', 'N-1')}",
            f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 执行摘要",
            "",
            f"- **总故障场景**: {summary.get('total_cases', 0)}",
            f"- **通过**: {summary.get('passed', 0)} ({summary.get('pass_rate', 0)}%)",
            f"- **失败/越限**: {summary.get('failed', 0)}",
            f"- **严重故障**: {summary.get('severe_cases', 0)}",
            "",
            "### 安全裕度评估",
            "",
        ]

        if summary.get('pass_rate', 0) >= 95:
            lines.append("✅ **系统N-1安全裕度充足**")
        elif summary.get('pass_rate', 0) >= 80:
            lines.append("⚠️ **系统N-1安全裕度一般，存在局部风险**")
        else:
            lines.append("🚨 **系统N-1安全裕度不足，需加强网架结构**")

        lines.extend([
            "",
            "## 评判标准",
            "",
            f"- **电压限值**: {voltage_limit['min']:.3f} - {voltage_limit['max']:.3f} pu",
            f"- **热稳定限值**: {thermal_limit * 100:.1f}%",
            "- **严重度阈值**: ≥0.8",
            "",
            "## 系统薄弱环节",
            "",
            "| 排名 | 元件 | 关键故障次数 |",
            "|------|------|--------------|",
        ])

        for i, wp in enumerate(weak_points, 1):
            lines.append(f"| {i} | {wp.get('component', 'N/A')} | {wp.get('critical_cases', 0)} |")

        lines.extend([
            "",
            "## 最严重故障场景 (Top 10)",
            "",
            "| 排名 | 故障场景 | 严重度 | 状态 | 最低电压 | 最高负载率 |",
            "|------|----------|--------|------|----------|------------|",
        ])

        for i, case in enumerate(top_cases[:10], 1):
            lines.append(
                f"| {i} | {case.get('name', 'N/A')} | "
                f"{case.get('severity', 0):.4f} | {case.get('status', 'N/A')} | "
                f"{case.get('min_voltage', 'N/A')} | {case.get('max_loading', 'N/A')}% |"
            )

        lines.extend([
            "",
            "## 建议措施",
            "",
        ])

        if summary.get('severe_cases', 0) > 0:
            lines.append("### 针对严重故障场景")
            lines.append("1. **加强薄弱环节**: 对排名前列的元件进行加固或冗余设计")
            lines.append("2. **电压支撑**: 在电压薄弱节点配置无功补偿装置")
            lines.append("3. **负载均衡**: 优化运行方式，避免线路过载")
            lines.append("4. **保护配合**: 校核继电保护定值，确保故障快速隔离")
        elif summary.get('pass_rate', 0) == 100.0:
            lines.append("✅ **当前系统满足N-1安全准则，无需额外措施**")
        else:
            lines.append("🚨 **系统N-1安全裕度不足，需加强网架结构**")

        lines.extend([
            "",
            "## 附录: 故障状态说明",
            "",
            "- **PASS**: 故障后系统正常运行，无越限",
            "- **VIOLATION**: 故障后存在电压或热稳定越限",
            "- **FAIL**: 故障后潮流不收敛",
            "- **TIMEOUT**: 计算超时",
            "",
        ])

        path.write_text("\n".join(lines), encoding="utf-8")
