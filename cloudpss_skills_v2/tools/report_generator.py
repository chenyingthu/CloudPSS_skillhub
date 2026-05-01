"""Report Generator Tool - Generate analysis reports.

报告生成工具 - 生成分析报告。
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    SkillResult,
    SkillStatus,
)

logger = logging.getLogger(__name__)


class ReportGeneratorTool:
    name = "report_generator"
    description = "报告生成工具 - 生成分析报告"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill"],
            "properties": {
                "skill": {"type": "string", "const": "report_generator", "default": "report_generator"},
                "report": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "default": "CloudPSS Analysis Report",
                        },
                        "author": {"type": "string", "default": "CloudPSS Toolkit"},
                        "skills": {"type": "array", "items": {"type": "string"}, "default": []},
                        "skill_results": {"type": "array", "default": []},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {
                            "type": "string",
                            "enum": ["markdown", "html"],
                            "default": "markdown",
                        },
                        "path": {"type": "string", "default": "/tmp/cloudpss_reports"},
                        "filename": {"type": "string"},
                    },
                },
            },
        }

    def __init__(self):
        self.logs = []
        self.artifacts = []

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "report": {
                "title": "CloudPSS Analysis Report",
                "author": "CloudPSS Toolkit",
                "skills": [],
                "skill_results": [],
            },
            "output": {
                "format": "markdown",
                "path": "/tmp/cloudpss_reports",
            },
        }

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
        report = config.get("report")
        if not report:
            errors.append("report section is required")
        return (len(errors) == 0, errors)

    def _generate_sections(self, report_config: dict) -> dict:
        skills = report_config.get("skills", [])
        results = report_config.get("skill_results", [])
        cover_title = report_config.get("title", "Report")
        cover_author = report_config.get("author", "Unknown")

        return {
            "cover": {
                "title": cover_title,
                "author": cover_author,
            },
            "summary": {
                "skills_count": len(skills),
                "results_count": len(results),
            },
            "analysis_results": results,
            "conclusions": "This report was generated automatically by the report_generator tool.",
        }

    def _export_markdown(self, sections: dict) -> str:
        cover = sections.get("cover", {})
        summary = sections.get("summary", {})
        analysis = sections.get("analysis_results", [])
        conclusions = sections.get("conclusions", "")

        lines = []
        lines.append(f"# {cover.get('title', 'Report')}")
        lines.append("")
        lines.append(f"## Author: {cover.get('author', 'Unknown')}")
        lines.append("")
        lines.append("## Summary")
        lines.append(f"- Skills: {summary.get('skills_count', 0)}")
        lines.append(f"- Results: {summary.get('results_count', 0)}")
        lines.append("")
        lines.append("## Analysis Results")
        for item in analysis:
            if isinstance(item, dict):
                lines.append(
                    f"- {item.get('skill_name', 'Unknown')}: {item.get('status', 'N/A')}"
                )
            else:
                lines.append(f"- {item}")
        lines.append("")
        lines.append("## Conclusions")
        lines.append(conclusions)

        return "\n".join(lines)

    def _export_html(self, markdown: str) -> str:
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #666; border-bottom: 1px solid #ccc; padding-bottom: 10px; }}
        ul {{ list-style-type: none; padding-left: 20px; }}
        li {{ margin: 10px 0; }}
    </style>
</head>
<body>
<pre>{markdown}</pre>
</body>
</html>"""
        return html

    def _write_file(self, content: str, ext: str, base_name: str, out_dir: str) -> str:
        os.makedirs(out_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
        filename = f"{base_name}_{timestamp}.{ext}"
        path = os.path.join(out_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

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
            report_config = config.get("report", {})
            output_config = config.get("output", {})

            sections = self._generate_sections(report_config)
            markdown = self._export_markdown(sections)
            html = self._export_html(markdown)

            out_dir = output_config.get("path", "/tmp/cloudpss_reports")
            md_path = self._write_file(markdown, "md", "report_generator", out_dir)
            html_path = self._write_file(html, "html", "report_generator", out_dir)

            self.artifacts.append(
                Artifact(
                    name="report_generator_markdown",
                    path=md_path,
                    type="text/markdown",
                )
            )
            self.artifacts.append(
                Artifact(
                    name="report_generator_html",
                    path=html_path,
                    type="text/html",
                )
            )

            result_data = {
                "sections": sections,
                "markdown_path": md_path,
                "html_path": html_path,
            }

            self._log("INFO", f"Report generated: {md_path}, {html_path}")

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data=result_data,
                logs=self.logs,
                artifacts=self.artifacts,
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            self._log("ERROR", f"Report generation failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["ReportGeneratorTool"]
