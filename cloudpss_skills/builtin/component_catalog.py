#!/usr/bin/env python3
"""
组件目录技能

功能：获取 CloudPSS 平台上所有可用的元件模型 RID 和描述，
      支持按标签过滤、名称搜索，导出为 JSON/CSV 格式。

适用：查找可用元件、获取组件 RID 参考、批量导出组件列表

作者: Claude Code
日期: 2026-04-01
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import re
import csv
import json

from cloudpss_skills.core.base import SkillBase, SkillResult, SkillStatus, ValidationResult

logger = logging.getLogger(__name__)


@dataclass
class ComponentInfo:
    """组件信息"""
    name: str
    rid: str
    description: str = ""
    tags: List[str] = field(default_factory=list)
    owner: str = ""
    updated_at: str = ""


class ComponentCatalogSkill(SkillBase):
    """
    组件目录技能

    功能特性:
    1. 获取 CloudPSS 平台上所有可用组件
    2. 按标签过滤（如 project-category:component）
    3. 按名称正则表达式搜索
    4. 导出为 JSON/CSV 格式
    5. 支持分页获取大量组件

    配置示例:
        skill: component_catalog

        auth:
          token_file: .cloudpss_token

        filters:
          tags:
            - project-category:component
          name_pattern: ".*PV.*"  # 可选，按名称过滤
          owner: "*"  # * 表示所有用户

        output:
          format: json  # 或 csv
          path: ./components.json
          include_details: true  # 是否包含详细信息

    """

    name = "component_catalog"
    description = "获取 CloudPSS 组件目录、RID查询、元件模型列表"
    version = "1.0.0"

    config_schema = {
        "type": "object",
        "properties": {
            "auth": {
                "type": "object",
                "properties": {
                    "token": {"type": "string"},
                    "token_file": {"type": "string"}
                }
            },
            "filters": {
                "type": "object",
                "properties": {
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "按标签过滤，如 project-category:component"
                    },
                    "name_pattern": {
                        "type": "string",
                        "description": "按名称正则表达式过滤"
                    },
                    "owner": {
                        "type": "string",
                        "default": "*",
                        "description": "按所有者过滤，* 表示所有"
                    }
                }
            },
            "options": {
                "type": "object",
                "properties": {
                    "page_size": {
                        "type": "integer",
                        "default": 1000,
                        "description": "每页获取数量"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "最大返回结果数，默认不限制"
                    },
                    "include_details": {
                        "type": "boolean",
                        "default": True,
                        "description": "是否获取组件详细信息"
                    }
                }
            },
            "output": {
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "enum": ["json", "csv", "console"],
                        "default": "console"
                    },
                    "path": {
                        "type": "string",
                        "description": "输出文件路径（format为json/csv时）"
                    },
                    "group_by_tag": {
                        "type": "boolean",
                        "default": False,
                        "description": "按标签分组输出"
                    }
                }
            }
        }
    }

    def __init__(self):
        super().__init__()
        self.components = []

    def validate(self, config: Dict) -> ValidationResult:
        """验证配置"""
        errors = []

        # 验证输出格式
        output = config.get("output", {})
        fmt = output.get("format", "console")
        if fmt in ["json", "csv"]:
            if not output.get("path"):
                errors.append("format为json/csv时必须指定path")

        # 验证正则表达式
        filters = config.get("filters", {})
        pattern = filters.get("name_pattern")
        if pattern:
            try:
                re.compile(pattern)
            except re.error as e:
                errors.append(f"name_pattern 正则表达式无效: {e}")

        return ValidationResult(valid=len(errors) == 0, errors=errors)

    def run(self, config: Dict) -> SkillResult:
        """执行组件目录获取"""
        start_time = datetime.now()
        try:
            self._setup_auth(config)

            # 获取组件列表
            logger.info("获取 CloudPSS 组件目录...")
            components = self._fetch_components(config)

            # 应用过滤器
            filtered = self._apply_filters(components, config.get("filters", {}))

            # 获取详细信息（可选）
            if config.get("options", {}).get("include_details", True):
                logger.info(f"获取 {len(filtered)} 个组件的详细信息...")
                filtered = self._enrich_components(filtered)

            # 限制结果数量
            max_results = config.get("options", {}).get("max_results")
            if max_results and len(filtered) > max_results:
                filtered = filtered[:max_results]
                logger.info(f"结果限制为 {max_results} 个")

            self.components = filtered

            # 输出结果
            output_config = config.get("output", {})
            output_path = self._output_results(filtered, output_config)

            # 构建结果
            result_data = {
                "total_fetched": len(components),
                "filtered_count": len(filtered),
                "output_path": output_path,
                "components": [
                    {
                        "name": c.name,
                        "rid": c.rid,
                        "description": c.description,
                        "tags": c.tags,
                        "owner": c.owner
                    }
                    for c in filtered
                ]
            }

            # 按标签分组统计
            tag_stats = self._get_tag_statistics(filtered)
            result_data["tag_statistics"] = tag_stats

            # 构建 artifacts
            artifacts = []
            if output_path:
                from cloudpss_skills.core import Artifact
                artifacts.append(Artifact(
                    type="file",
                    path=output_path,
                    size=0,
                    description="组件目录输出"
                ))

            logger.info(f"组件目录获取完成: {len(filtered)} 个组件")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                artifacts=artifacts
            )

        except (KeyError, AttributeError, ConnectionError, FileNotFoundError, ValueError, TypeError) as e:
            logger.error(f"组件目录获取失败: {e}", exc_info=True)
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                error=str(e)
            )

    def _fetch_components(self, config: Dict) -> List[ComponentInfo]:
        """从 CloudPSS 获取组件列表"""
        from cloudpss import Model

        options = config.get("options", {})
        page_size = options.get("page_size", 1000)
        owner = config.get("filters", {}).get("owner", "*")

        logger.info(f"获取模型列表 (owner={owner}, page_size={page_size})...")

        try:
            # 使用 fetchMany 获取所有模型
            models = Model.fetchMany(pageSize=page_size, owner=owner)
            logger.info(f"获取到 {len(models)} 个模型")
        except (KeyError, AttributeError) as e:
            logger.error(f"获取模型列表失败: {e}")
            raise

        # 转换为 ComponentInfo
        components = []
        for m in models:
            comp = ComponentInfo(
                name=m.get("name", ""),
                rid=m.get("rid", ""),
                description=m.get("description", ""),
                tags=m.get("tags", []),
                owner=m.get("owner", ""),
                updated_at=m.get("updatedAt", "")
            )
            components.append(comp)

        return components

    def _apply_filters(self, components: List[ComponentInfo], filters: Dict) -> List[ComponentInfo]:
        """应用过滤器"""
        result = components

        # 按标签过滤
        tags = filters.get("tags", [])
        if tags:
            logger.info(f"按标签过滤: {tags}")
            result = [
                c for c in result
                if any(tag in c.tags for tag in tags)
            ]
            logger.info(f"标签过滤后: {len(result)} 个")

        # 按名称正则表达式过滤
        pattern = filters.get("name_pattern")
        if pattern:
            logger.info(f"按名称过滤: {pattern}")
            regex = re.compile(pattern, re.IGNORECASE)
            result = [
                c for c in result
                if regex.search(c.name)
            ]
            logger.info(f"名称过滤后: {len(result)} 个")

        return result

    def _enrich_components(self, components: List[ComponentInfo]) -> List[ComponentInfo]:
        """获取组件详细信息"""
        from cloudpss import Model

        enriched = []
        for comp in components:
            try:
                # 尝试获取模型详细信息
                model = Model.fetch(comp.rid)
                # 获取拓扑信息
                topology = model.fetchTopology()
                if hasattr(topology, "components"):
                    comp_count = len(topology.components)
                    comp.description += f" (组件数: {comp_count})"
            except (KeyError, AttributeError) as e:
                logger.debug(f"获取 {comp.rid} 详细信息失败: {e}")

            enriched.append(comp)

        return enriched

    def _output_results(self, components: List[ComponentInfo], output_config: Dict) -> Optional[str]:
        """输出结果"""
        fmt = output_config.get("format", "console")
        path = output_config.get("path")
        group_by_tag = output_config.get("group_by_tag", False)

        if fmt == "console":
            self._output_console(components, group_by_tag)
            return None

        elif fmt == "json":
            return self._output_json(components, path, group_by_tag)

        elif fmt == "csv":
            return self._output_csv(components, path)

        return None

    def _output_console(self, components: List[ComponentInfo], group_by_tag: bool):
        """输出到控制台"""
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append(f"CloudPSS 组件目录 (共 {len(components)} 个)")
        lines.append("=" * 80)

        if group_by_tag:
            # 按标签分组
            tag_groups = {}
            for c in components:
                primary_tag = c.tags[0] if c.tags else "未分类"
                if primary_tag not in tag_groups:
                    tag_groups[primary_tag] = []
                tag_groups[primary_tag].append(c)

            for tag, comps in sorted(tag_groups.items()):
                lines.append(f"\n【{tag}】 ({len(comps)} 个)")
                lines.append("-" * 80)
                for c in comps:
                    lines.append(f"  {c.name:<40} {c.rid}")
        else:
            # 列表输出
            for i, c in enumerate(components, 1):
                lines.append(f"\n{i}. {c.name}")
                lines.append(f"   RID: {c.rid}")
                lines.append(f"   标签: {', '.join(c.tags)}")
                if c.description:
                    lines.append(f"   描述: {c.description}")

        lines.append("\n" + "=" * 80)

        for line in lines:
            logger.info(line)

    def _output_json(self, components: List[ComponentInfo], path: str, group_by_tag: bool) -> str:
        """输出为 JSON"""
        if group_by_tag:
            data = {}
            for c in components:
                primary_tag = c.tags[0] if c.tags else "未分类"
                if primary_tag not in data:
                    data[primary_tag] = []
                data[primary_tag].append({
                    "name": c.name,
                    "rid": c.rid,
                    "description": c.description,
                    "tags": c.tags,
                    "owner": c.owner
                })
        else:
            data = [
                {
                    "name": c.name,
                    "rid": c.rid,
                    "description": c.description,
                    "tags": c.tags,
                    "owner": c.owner
                }
                for c in components
            ]

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"JSON 已保存到: {path}")
        return path

    def _output_csv(self, components: List[ComponentInfo], path: str) -> str:
        """输出为 CSV"""
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["名称", "RID", "描述", "标签", "所有者"])
            for c in components:
                writer.writerow([
                    c.name,
                    c.rid,
                    c.description,
                    ", ".join(c.tags),
                    c.owner
                ])

        logger.info(f"CSV 已保存到: {path}")
        return path

    def _get_tag_statistics(self, components: List[ComponentInfo]) -> Dict[str, int]:
        """获取标签统计"""
        stats = {}
        for c in components:
            for tag in c.tags:
                stats[tag] = stats.get(tag, 0) + 1
        return dict(sorted(stats.items(), key=lambda x: x[1], reverse=True)[:20])

    def _setup_auth(self, config: Dict):
        """设置认证"""
        from cloudpss import setToken

        auth = config.get("auth", {})
        token = auth.get("token")

        if not token and auth.get("token_file"):
            try:
                with open(auth["token_file"], "r") as f:
                    token = f.read().strip()
            except FileNotFoundError:
                # 异常已捕获，无需额外处理
                logger.debug(f"忽略预期异常: {e}")

        if not token:
            try:
                with open(".cloudpss_token", "r") as f:
                    token = f.read().strip()
            except FileNotFoundError:
                raise ValueError("未找到 CloudPSS token")

        setToken(token)
