"""
CloudPSS Skills MCP Server

为 Claude Code 和其他 MCP 客户端提供电力系统仿真技能。
"""

__version__ = "0.1.0"
__all__ = ["app", "create_server"]

from .server import app, create_server
