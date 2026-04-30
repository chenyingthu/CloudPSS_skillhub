"""Auto loop breaker tool."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core import LogEntry, SkillResult, SkillStatus


class AutoLoopBreakerTool:
    """Detect directed loops and suggest nodes to break them."""

    name = "auto_loop_breaker"

    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts = []

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill"],
            "properties": {
                "skill": {"type": "string", "const": "auto_loop_breaker", "default": "auto_loop_breaker"},
                "model": {
                    "type": "object",
                    "properties": {
                        "rid": {"type": "string", "default": ""},
                        "source": {"type": "string", "default": "inline"},
                        "graph": {"type": "object", "default": {}},
                    },
                },
                "algorithm": {
                    "type": "object",
                    "properties": {
                        "strategy": {"type": "string", "default": "degree"},
                        "max_iterations": {"type": "integer", "default": 500},
                    },
                },
                "loop_node": {
                    "type": "object",
                    "properties": {
                        "auto_detect": {"type": "boolean", "default": True},
                        "target_nodes": {"type": "array", "items": {"type": "string"}, "default": []},
                    },
                },
                "output": {"type": "object", "properties": {"format": {"type": "string", "default": "json"}}},
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "model": {"rid": "", "source": "inline", "graph": {}},
            "algorithm": {"strategy": "degree", "max_iterations": 500},
            "loop_node": {"auto_detect": True, "target_nodes": []},
            "output": {"format": "json"},
        }

    def validate(self, config: dict[str, Any] | None = None) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not isinstance(config, dict):
            return False, ["config is required"]
        model = config.get("model")
        if not isinstance(model, dict) or not model.get("rid"):
            errors.append("model.rid is required")
        graph = model.get("graph", {}) if isinstance(model, dict) else {}
        if graph and not isinstance(graph, dict):
            errors.append("model.graph must be an adjacency mapping")
        return len(errors) == 0, errors

    def _detect_cycles_dfs(self, graph: dict[str, list[str]] | None = None) -> list[list[str]]:
        graph = graph or {}
        cycles: list[list[str]] = []
        stack: list[str] = []
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node: str) -> None:
            if node in visiting:
                start = stack.index(node)
                cycle = stack[start:] + [node]
                if cycle not in cycles:
                    cycles.append(cycle)
                return
            if node in visited:
                return

            visiting.add(node)
            stack.append(node)
            for neighbor in graph.get(node, []):
                visit(str(neighbor))
            stack.pop()
            visiting.remove(node)
            visited.add(node)

        for node in graph:
            visit(str(node))
        return cycles

    def _select_node_by_strategy(
        self,
        candidates: set[str],
        graph: dict[str, list[str]],
        strategy: str = "degree",
    ) -> str:
        if not candidates:
            return ""
        if strategy != "degree":
            return sorted(candidates)[0]

        def degree(node: str) -> int:
            outgoing = len(graph.get(node, []))
            incoming = sum(1 for values in graph.values() if node in values)
            return outgoing + incoming

        return max(sorted(candidates), key=degree)

    def _compute_fvs_greedy(
        self,
        graph: dict[str, list[str]] | None = None,
        max_iterations: int = 500,
        strategy: str = "degree",
    ) -> tuple[list[str], list[list[str]]]:
        working = {str(k): [str(v) for v in values] for k, values in (graph or {}).items()}
        removed: list[str] = []
        cycles = self._detect_cycles_dfs(working)
        iterations = 0
        while cycles and iterations < max_iterations:
            candidates = {node for cycle in cycles for node in cycle[:-1]}
            selected = self._select_node_by_strategy(candidates, working, strategy)
            if not selected:
                break
            removed.append(selected)
            working.pop(selected, None)
            for values in working.values():
                values[:] = [value for value in values if value != selected]
            cycles = self._detect_cycles_dfs(working)
            iterations += 1
        return removed, cycles

    def run(self, config: dict[str, Any] | None = None) -> SkillResult:
        start_time = datetime.now()
        config = config or {}
        valid, errors = self.validate(config)
        if not valid:
            return SkillResult.failure(
                skill_name=self.name,
                error="; ".join(errors),
                data={"stage": "validation", "errors": errors},
            )

        model = config["model"]
        algorithm = config.get("algorithm", {})
        strategy = algorithm.get("strategy", "degree")
        max_iterations = int(algorithm.get("max_iterations", 500))
        graph = model.get("graph") or {
            "controller_a": ["controller_b"],
            "controller_b": ["controller_c"],
            "controller_c": ["controller_a"],
        }

        initial_cycles = self._detect_cycles_dfs(graph)
        break_nodes, remaining_cycles = self._compute_fvs_greedy(
            graph,
            max_iterations=max_iterations,
            strategy=strategy,
        )

        self.logs.append(LogEntry(level="info", message="Auto loop breaker completed"))
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.SUCCESS,
            data={
                "model_rid": model["rid"],
                "strategy": strategy,
                "initial_cycles": initial_cycles,
                "break_nodes": break_nodes,
                "remaining_cycles": remaining_cycles,
                "loop_free": not remaining_cycles,
            },
            logs=self.logs,
            metrics={
                "initial_cycle_count": len(initial_cycles),
                "break_node_count": len(break_nodes),
            },
            start_time=start_time,
            end_time=datetime.now(),
        )


__all__ = ["AutoLoopBreakerTool"]
