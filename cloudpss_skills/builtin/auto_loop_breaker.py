"""
Auto Loop Breaker Skill

模型自动解环 - 检测并自动消除模型中的控制环路。
"""

import json
import logging
import re
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from cloudpss_skills.core import Artifact, LogEntry, SkillBase, SkillResult, SkillStatus, ValidationResult, register

logger = logging.getLogger(__name__)


@register
class AutoLoopBreakerSkill(SkillBase):
    """自动解环技能 - 检测并消除模型控制环路"""

    # CloudPSS标准元件RID
    COMPONENT_RIDS = {
        "loop_node": "model/CloudPSS/_newLoopNode",
        "loop_node_multi": "model/CloudPSS/_newLoopNodeMultiDim",
        "channel_demerge": "model/CloudPSS/_ChannelDeMerge",
        "channel_merge": "model/CloudPSS/_ChannelMerge",
        "electrical_label": "model/CloudPSS/ElectricalLable",
        "channel": "model/CloudPSS/_newChannel",
        "bus_connector": "model/CloudPSS/_BusConnector",
    }

    @property
    def name(self) -> str:
        return "auto_loop_breaker"

    @property
    def description(self) -> str:
        return "自动检测并消除模型中的控制环路，支持代数环和信号环的自动解环"

    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "auto_loop_breaker"},
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
                "algorithm": {
                    "type": "object",
                    "properties": {
                        "max_iterations": {"type": "integer", "default": 500, "description": "最大迭代次数"},
                        "strategy": {"enum": ["degree", "random", "hybrid"], "default": "degree", "description": "节点选择策略"},
                        "random_seed": {"type": "integer", "description": "随机种子（用于随机策略）"},
                    },
                },
                "loop_node": {
                    "type": "object",
                    "properties": {
                        "init_value": {"type": "string", "default": "0", "description": "解环点初始值"},
                        "name_prefix": {"type": "string", "default": "LoopBreaker", "description": "解环点名称前缀"},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "save_model": {"type": "boolean", "default": False, "description": "是否保存修改后的模型"},
                        "dry_run": {"type": "boolean", "default": False, "description": "仅预览不修改"},
                        "new_name_suffix": {"type": "string", "default": "_unloop", "description": "新模型名称后缀"},
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
            "algorithm": {
                "max_iterations": 500,
                "strategy": "degree",
                "random_seed": None,
            },
            "loop_node": {
                "init_value": "0",
                "name_prefix": "LoopBreaker",
            },
            "output": {
                "save_model": False,
                "dry_run": False,
                "new_name_suffix": "_unloop",
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

        return result

    def run(self, config: Dict[str, Any]) -> SkillResult:
        """执行自动解环"""
        from cloudpss import Model, setToken
        from cloudpss.model.implements.component import Component

        start_time = datetime.now()
        logs = []
        artifacts = []
        broken_loops = []

        def log(level: str, message: str):
            logs.append(LogEntry(
                timestamp=datetime.now(),
                level=level,
                message=message
            ))
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

            setToken(token)
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

            # 3. 获取配置
            algo_config = config.get("algorithm", {})
            loop_node_config = config.get("loop_node", {})
            output_config = config.get("output", {})

            dry_run = output_config.get("dry_run", False)
            save_model = output_config.get("save_model", False)
            new_name_suffix = output_config.get("new_name_suffix", "_unloop")

            max_iter = algo_config.get("max_iterations", 500)
            strategy = algo_config.get("strategy", "degree")
            random_seed = algo_config.get("random_seed")

            init_value = loop_node_config.get("init_value", "0")
            name_prefix = loop_node_config.get("name_prefix", "LoopBreaker")

            if dry_run:
                log("INFO", "【试运行模式】仅分析环路，不修改模型")

            # 4. 构建拓扑图
            log("INFO", "分析模型拓扑...")
            try:
                topo_graph, topo_pin_dict, comp_list = self._build_topology_graph(model)
                log("INFO", f"  -> 发现 {len(topo_graph.nodes)} 个信号节点，{len(topo_graph.edges)} 条连接")
            except (AttributeError) as e:
                log("ERROR", f"拓扑分析失败: {e}")
                raise

            # 5. 检测环路
            log("INFO", "检测控制环路...")
            try:
                import networkx as nx
                has_loops = not nx.is_directed_acyclic_graph(topo_graph)
            except ImportError as e:
                log("ERROR", f"环路检测失败: {e}")
                raise

            if not has_loops:
                log("INFO", "✓ 模型中未发现控制环路")
                return SkillResult(
                    skill_name=self.name,
                    status=SkillStatus.SUCCESS,
                    start_time=start_time,
                    end_time=datetime.now(),
                    data={
                        "model_rid": rid,
                        "model_name": model.name,
                        "loops_found": 0,
                        "loops_broken": 0,
                        "dry_run": dry_run,
                        "message": "模型中无控制环路",
                    },
                    artifacts=artifacts,
                    logs=logs,
                )

            log("INFO", "  -> 发现控制环路，开始计算解环方案...")

            # 6. 计算反馈顶点集
            try:
                fvs_nodes = self._compute_fvs(topo_graph, max_iter, strategy, random_seed)
                log("INFO", f"  -> 需要打破 {len(fvs_nodes)} 个环路节点")
            except (AttributeError) as e:
                log("ERROR", f"FVS计算失败: {e}")
                raise

            if dry_run:
                log("INFO", "【试运行模式】解环方案预览:")
                for node in fvs_nodes:
                    node_info = topo_pin_dict.get(node, [["unknown", "unknown"]])
                    log("INFO", f"  - 将在 {node_info[0][0]}.{node_info[0][1]} 插入解环点")

            # 7. 执行解环
            if not dry_run:
                log("INFO", "执行解环操作...")
                try:
                    broken_loops = self._break_loops(
                        model, fvs_nodes, topo_pin_dict, comp_list,
                        init_value, name_prefix
                    )
                    log("INFO", f"  -> 成功插入 {len(broken_loops)} 个解环点")
                except AttributeError as e:
                    log("ERROR", f"解环操作失败: {e}")
                    raise

            # 8. 保存模型（如果需要）
            if save_model and not dry_run:
                log("INFO", "保存修改后的模型...")
                try:
                    new_name = model.name + new_name_suffix
                    # 提取模型key
                    match = re.match(r'.*?/.*?/(.*)', model.rid)
                    if match:
                        new_key = match.group(1) + new_name_suffix
                        model.save(new_key)
                        log("INFO", f"  -> 模型已保存: {new_key}")
                    else:
                        log("WARN", "  -> 无法解析模型key，跳过保存")
                except (AttributeError, KeyError) as e:
                    log("ERROR", f"保存模型失败: {e}")
                    raise

            # 9. 生成报告
            log("INFO", "生成解环报告...")
            try:
                report = self._generate_report(fvs_nodes, topo_pin_dict, broken_loops, dry_run)
                report_path = Path("./results/auto_loop_breaker_report.json")
                report_path.parent.mkdir(parents=True, exist_ok=True)
                report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))

                artifacts.append(Artifact(
                    type="json",
                    path=str(report_path),
                    size=report_path.stat().st_size,
                    description="解环分析报告"
                ))
            except (AttributeError, ZeroDivisionError, json.JSONDecodeError, RuntimeError, ValueError, TypeError) as e:
                log("ERROR", f"生成报告失败: {e}")
                # 报告生成失败不中断整体流程
                pass  # 继续执行

            log("INFO", f"解环完成！共打破 {len(fvs_nodes)} 个环路")

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data={
                    "model_rid": rid,
                    "model_name": model.name,
                    "loops_found": len(fvs_nodes),
                    "loops_broken": len(broken_loops) if not dry_run else 0,
                    "nodes_analyzed": len(topo_graph.nodes),
                    "edges_analyzed": len(topo_graph.edges),
                    "strategy": strategy,
                    "dry_run": dry_run,
                    "saved": save_model and not dry_run,
                },
                artifacts=artifacts,
                logs=logs,
            )

        except (AttributeError, ZeroDivisionError, json.JSONDecodeError, RuntimeError, ValueError, TypeError) as e:
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

    def _build_topology_graph(self, model: Any) -> Tuple[Any, Dict, Dict]:
        """构建模型拓扑图"""
        import networkx as nx

        try:
            # 获取模型拓扑
            revision = model.revision
            topo = model.fetchTopology(implementType="emtp", maximumDepth=0).toJSON()
        except (KeyError, AttributeError) as e:
            logger.error(f"获取模型拓扑失败: {e}")
            raise RuntimeError(f"无法获取模型拓扑: {e}") from e

        try:
            # 获取元件定义信息
            dict_pin = {}
            for comp_key, comp in model.getAllComponents().items():
                if 'diagram-component' not in getattr(comp, 'shape', ''):
                    continue
                if comp.definition in dict_pin:
                    continue
                # 获取元件定义
                try:
                    defn = model.__class__.fetch(comp.definition)
                    r = defn.revision
                    dict_pin[comp.definition] = {r.pins[k]['key']: r.pins[k] for k in range(len(r.pins))}
                except (KeyError, AttributeError) as e:
                    logger.debug(f"获取元件定义失败 {comp.definition}: {e}")
                    continue

            # 构建图
            g = nx.DiGraph()
            topo_pin_dict = {}
            comp_list = {}

            for comp_key, comp_data in topo.get('components', {}).items():
                innodes = []
                outnodes = []
                definition = comp_data.get('definition', '')

                # 跳过特定元件
                if definition in [
                    self.COMPONENT_RIDS["electrical_label"],
                    self.COMPONENT_RIDS["channel"],
                    self.COMPONENT_RIDS["bus_connector"],
                ]:
                    continue

                pins = comp_data.get('pins', {})

                # 处理ChannelDeMerge
                if definition == self.COMPONENT_RIDS["channel_demerge"]:
                    for pin_name, pin_id in pins.items():
                        if not pin_id:
                            continue
                        pin_id_int = int(pin_id)
                        if pin_id_int not in topo_pin_dict:
                            topo_pin_dict[pin_id_int] = []
                        topo_pin_dict[pin_id_int].append([comp_key, pin_name, 0])
                        if pin_name == 'InName':
                            innodes.append(pin_id_int)
                        else:
                            outnodes.append(pin_id_int)

                # 处理ChannelMerge
                elif definition == self.COMPONENT_RIDS["channel_merge"]:
                    for pin_name, pin_id in pins.items():
                        if not pin_id:
                            continue
                        pin_id_int = int(pin_id)
                        if pin_id_int not in topo_pin_dict:
                            topo_pin_dict[pin_id_int] = []
                        topo_pin_dict[pin_id_int].append([comp_key, pin_name, 0])
                        if pin_name == 'OutName':
                            outnodes.append(pin_id_int)
                        else:
                            innodes.append(pin_id_int)

                # 处理其他元件
                else:
                    if definition not in dict_pin:
                        continue
                    for pin_name, pin_id in pins.items():
                        if not pin_id:
                            continue
                        pin_info = dict_pin[definition].get(pin_name, {})
                        if pin_info.get('connection') == 'electrical':
                            continue
                        pin_id_int = int(pin_id)
                        if pin_id_int not in topo_pin_dict:
                            topo_pin_dict[pin_id_int] = []
                        topo_pin_dict[pin_id_int].append([comp_key, pin_name, 0])
                        if pin_info.get('connection') == 'input':
                            innodes.append(pin_id_int)
                        elif pin_info.get('connection') == 'output':
                            outnodes.append(pin_id_int)

                innodes = list(set(innodes))
                outnodes = list(set(outnodes))
                if comp_key not in comp_list:
                    comp_list[comp_key] = {'in': innodes, 'out': outnodes}

            # 添加节点和边
            nodelist = list(topo_pin_dict.keys())
            g.add_nodes_from(nodelist)

            edgelist = []
            for comp_key, comp_info in comp_list.items():
                for ink in comp_info['in']:
                    for outk in comp_info['out']:
                        edgelist.append((ink, outk))
            g.add_edges_from(edgelist)

            return g, topo_pin_dict, comp_list

        except (KeyError, AttributeError, ConnectionError, RuntimeError, ValueError, TypeError) as e:
            logger.error(f"构建拓扑图失败: {e}")
            raise RuntimeError(f"构建模型拓扑图失败: {e}") from e

    def _compute_fvs(self, g: Any, max_iter: int, strategy: str, random_seed: Optional[int]) -> List[int]:
        """计算反馈顶点集"""
        import networkx as nx
        import random

        if random_seed is not None:
            random.seed(random_seed)

        fvs = set()
        g_copy = g.copy()

        iteration = 0
        while iteration < max_iter:
            if nx.is_directed_acyclic_graph(g_copy):
                break

            # 寻找强连通分量
            sccs = list(nx.strongly_connected_components(g_copy))
            non_trivial_sccs = [scc for scc in sccs if len(scc) > 1]

            if not non_trivial_sccs:
                break

            # 选择最大的SCC
            largest_scc = max(non_trivial_sccs, key=len)
            nodes_in_scc = list(largest_scc)

            # 根据策略选择节点
            if strategy == "degree":
                scores = {n: g_copy.in_degree(n) + g_copy.out_degree(n) for n in nodes_in_scc}
                top_node = max(nodes_in_scc, key=lambda x: scores[x])
            elif strategy == "random":
                top_node = random.choice(nodes_in_scc)
            elif strategy == "hybrid":
                if iteration % 5 == 0 and len(nodes_in_scc) >= 5:
                    top_node = random.choice(nodes_in_scc)
                else:
                    scores = {n: g_copy.in_degree(n) + g_copy.out_degree(n) for n in nodes_in_scc}
                    top_node = max(nodes_in_scc, key=lambda x: scores[x])
            else:
                scores = {n: g_copy.in_degree(n) + g_copy.out_degree(n) for n in nodes_in_scc}
                top_node = max(nodes_in_scc, key=lambda x: scores[x])

            fvs.add(top_node)
            g_copy.remove_node(top_node)
            iteration += 1

        return list(fvs)

    def _break_loops(
        self,
        model: Any,
        fvs_nodes: List[int],
        topo_pin_dict: Dict,
        comp_list: Dict,
        init_value: str,
        name_prefix: str
    ) -> List[Dict]:
        """执行解环操作"""
        from cloudpss.model.implements.component import Component

        broken_loops = []
        count = 1
        edge_id = f'edge_unloop_{time.strftime("%Y%m%d%H%M%S", time.localtime())}{random.randint(100,999)}'

        for node in fvs_nodes:
            node_info = topo_pin_dict.get(node, [])
            if not node_info:
                logger.warning(f"节点 {node} 无拓扑信息，跳过")
                continue

            comp_key = node_info[0][0]
            pin_name = node_info[0][1]

            try:
                comp = model.getComponentByKey(comp_key)
            except (AttributeError, KeyError) as e:
                logger.warning(f"获取元件 {comp_key} 失败: {e}")
                continue

            # 确定解环点类型
            try:
                if (comp.definition == self.COMPONENT_RIDS["channel_demerge"] and pin_name == 'InName'):
                    dim = comp.args.get('InDimX', '1')
                    loop_node = model.addComponent(
                        self.COMPONENT_RIDS["loop_node_multi"],
                        '多维解环点',
                        {'Name': f"{name_prefix}_{count}", 'Init': init_value, 'dim': str(dim)},
                        {'0': ''},
                        comp.canvas,
                        comp.position
                    )
                    target_port = 'Input'
                elif (comp.definition == self.COMPONENT_RIDS["channel_merge"] and pin_name == 'OutName'):
                    dim = comp.args.get('OutDimX', '1')
                    loop_node = model.addComponent(
                        self.COMPONENT_RIDS["loop_node_multi"],
                        '多维解环点',
                        {'Name': f"{name_prefix}_{count}", 'Init': init_value, 'dim': str(dim)},
                        {'0': ''},
                        comp.canvas,
                        comp.position
                    )
                    target_port = 'Input'
                else:
                    loop_node = model.addComponent(
                        self.COMPONENT_RIDS["loop_node"],
                        '解环点',
                        {'Name': f"{name_prefix}_{count}", 'Init': init_value},
                        {'0': ''},
                        comp.canvas,
                        comp.position
                    )
                    target_port = '0'
            except (AttributeError, TypeError) as e:
                logger.warning(f"创建解环点失败 ({comp_key}.{pin_name}): {e}")
                continue

            # 创建连接
            try:
                edge = Component({
                    'attrs': {
                        'root': {
                            'style': {
                                '--stroke': 'var(--edge-electrical-stroke,var(--edge-stroke))',
                                '--stroke-width': 'calc(2*var(--rpx,1))'
                            }
                        }
                    },
                    'canvas': comp.canvas,
                    'id': edge_id + str(count),
                    'shape': 'diagram-edge',
                    'source': {'cell': comp.id, 'port': pin_name},
                    'target': {'cell': loop_node.id, 'port': target_port}
                })

                model.revision.implements.diagram.cells[edge_id + str(count)] = edge
            except (KeyError, AttributeError, AttributeError) as e:
                logger.warning(f"创建连接失败 ({comp_key}.{pin_name}): {e}")
                continue

            broken_loops.append({
                'component': comp_key,
                'pin': pin_name,
                'loop_node_id': loop_node.id,
                'loop_node_name': f"{name_prefix}_{count}",
            })

            count += 1

        return broken_loops

    def _generate_report(
        self,
        fvs_nodes: List[int],
        topo_pin_dict: Dict,
        broken_loops: List[Dict],
        dry_run: bool
    ) -> Dict:
        """生成解环报告"""
        loop_details = []
        for node in fvs_nodes:
            node_info = topo_pin_dict.get(node, [["unknown", "unknown"]])
            loop_details.append({
                "node_id": node,
                "component": node_info[0][0],
                "pin": node_info[0][1],
            })

        return {
            "summary": {
                "loops_found": len(fvs_nodes),
                "loops_broken": len(broken_loops) if not dry_run else 0,
                "dry_run": dry_run,
            },
            "loops": loop_details,
            "break_points": broken_loops if not dry_run else [],
        }
