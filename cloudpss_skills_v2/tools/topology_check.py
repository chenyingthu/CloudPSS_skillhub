"""Topology Check Tool - Validate network connectivity and integrity.

拓扑检查 - 验证网络连通性和完整性。
"""

from __future__ import annotations

import logging
from collections import deque
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.powerskill import Engine

logger = logging.getLogger(__name__)


class TopologyCheckTool:
    name = "topology_check"
    description = "拓扑检查 - 验证网络连通性和完整性"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "topology_check"},
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "pandapower",
                },
                "model": {"type": "object", "required": ["rid"]},
                "checks": {
                    "type": "object",
                    "properties": {
                        "islands": {"type": "boolean", "default": True},
                        "dangling": {"type": "boolean", "default": True},
                        "isolated": {"type": "boolean", "default": True},
                    },
                },
            },
        }

    def __init__(self):
        self.logs = []
        self.artifacts = []

    def _log(self, level: str, message: str) -> None:
        self.logs.append(
            {
                "timestamp": datetime.now().isoformat(),
                "level": level,
                "message": message,
            }
        )
        getattr(logger, level.lower(), logger.info)(message)

    def validate(self, config: dict | None) -> tuple[bool, list[str]]:
        errors = []
        if not config:
            errors.append("config is required")
            return (False, errors)
        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")
        return (len(errors) == 0, errors)

    def _build_adjacency(self, buses: list, branches: list) -> dict[str, list[str]]:
        adj = {b: [] for b in buses}
        for branch in branches:
            from_bus = branch.get("from_bus") or branch.get("from_bus_name")
            to_bus = branch.get("to_bus") or branch.get("to_bus_name")
            if from_bus in adj and to_bus in adj:
                adj[from_bus].append(to_bus)
                adj[to_bus].append(from_bus)
        return adj

    def _find_islands(self, adj: dict[str, list[str]]) -> list[list[str]]:
        visited = set()
        islands = []

        for start_node in adj:
            if start_node in visited:
                continue
            island = []
            queue = deque([start_node])
            visited.add(start_node)

            while queue:
                node = queue.popleft()
                island.append(node)
                for neighbor in adj.get(node, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            islands.append(island)

        return islands

    def _find_dangling_buses(self, buses: list, adj: dict[str, list[str]]) -> list[str]:
        dangling = []
        for bus in buses:
            if not adj.get(bus):
                dangling.append(bus)
        return dangling

    def _find_isolated_generators(
        self, buses: list, generators: list, adj: dict
    ) -> list[str]:
        isolated = []
        for gen in generators:
            bus = gen.get("bus")
            if bus and bus in adj:
                if not adj[bus]:
                    isolated.append(gen.get("name", bus))
            elif bus:
                isolated.append(gen.get("name", bus))
        return isolated

    def run(self, config: dict | None) -> SkillResult:
        start_time = datetime.now()
        if config is None:
            config = {}
        self.logs = []
        self.artifacts = []

        valid, errors = self.validate(config)
        if not valid:
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error="; ".join(errors),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )

        try:
            engine = config.get("engine", "pandapower")
            api = Engine.create_powerflow(engine=engine)
            self._log("INFO", f"Using engine: {api.adapter.engine_name}")

            model_rid = config["model"]["rid"]
            self._log("INFO", f"Model: {model_rid}")

            checks = config.get("checks", {})
            check_islands = checks.get("islands", True)
            check_dangling = checks.get("dangling", True)

            handle = api.get_model_handle(model_rid)
            result = api.run_power_flow(model_handle=handle)

            bus_results = result.data.get("bus_results", []) if result.data else []
            branch_results = (
                result.data.get("branch_results", []) if result.data else []
            )

            bus_names = [b.get("bus") or b.get("name") for b in bus_results]
            from_buses = [
                b.get("from_bus") or b.get("from_bus_name") for b in branch_results
            ]
            to_buses = [b.get("to_bus") or b.get("to_bus_name") for b in branch_results]
            all_buses = list(set(bus_names + from_buses + to_buses))

            adj = self._build_adjacency(all_buses, branch_results)

            issues = []
            total_issues = 0

            if check_islands:
                islands = self._find_islands(adj)
                if len(islands) > 1:
                    for i, island in enumerate(islands):
                        if len(island) > 1:
                            issues.append(
                                {
                                    "type": "island",
                                    "island_id": i + 1,
                                    "size": len(island),
                                    "buses": island,
                                }
                            )
                            self._log(
                                "WARNING",
                                f"Found island {i + 1} with {len(island)} buses",
                            )
                            total_issues += 1

            if check_dangling:
                dangling = self._find_dangling_buses(all_buses, adj)
                if dangling:
                    issues.append(
                        {
                            "type": "dangling",
                            "buses": dangling,
                        }
                    )
                    self._log("WARNING", f"Found {len(dangling)} dangling buses")
                    total_issues += 1

            result_data = {
                "total_buses": len(all_buses),
                "total_branches": len(branch_results),
                "islands_found": len(islands) if check_islands else 0,
                "dangling_buses": len(dangling) if check_dangling else 0,
                "total_issues": total_issues,
                "issues": issues,
                "status": "pass" if total_issues == 0 else "fail",
            }

            self._log("INFO", f"Topology check complete: {total_issues} issues found")

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.COMPLETED
                if total_issues == 0
                else SkillStatus.FAILED,
                data=result_data,
                logs=self.logs,
                artifacts=self.artifacts,
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            self._log("ERROR", f"Topology check failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["TopologyCheckTool"]
