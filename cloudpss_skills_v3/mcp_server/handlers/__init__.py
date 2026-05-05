"""
MCP Server Handlers

提供各个 Tool 的处理函数。
"""

from .powerflow import handle_powerflow_run
from .emt import handle_emt_run
from .result import handle_result_query, handle_result_analyze, handle_result_export
from .model_search import handle_model_search
from .smart_suggestions import (
    analyze_model_for_powerflow,
    analyze_model_for_emt,
    handle_model_analysis
)
from .case_compare import handle_case_compare
from .parameter_sweep import handle_parameter_sweep

__all__ = [
    "handle_powerflow_run",
    "handle_emt_run",
    "handle_result_query",
    "handle_result_analyze",
    "handle_result_export",
    "handle_model_search",
    "handle_model_analysis",
    "handle_case_compare",
    "handle_parameter_sweep",
]
