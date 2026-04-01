"""
认证工具模块

提供统一的 CloudPSS 认证功能。
"""

import logging
from pathlib import Path
from typing import Dict, Optional

from cloudpss import setToken

logger = logging.getLogger(__name__)

# 默认配置常量
DEFAULT_TOKEN_FILE = ".cloudpss_token"
DEFAULT_PAGE_SIZE = 1000
DEFAULT_TIMEOUT = 300
DEFAULT_POWERFLOW_TOLERANCE = 1e-6
DEFAULT_VOLTAGE_MIN = 0.5
DEFAULT_VOLTAGE_MAX = 1.5


def setup_auth(config: Dict) -> str:
    """
    设置 CloudPSS 认证

    Args:
        config: 配置字典，包含 auth 配置

    Returns:
        token: 认证令牌

    Raises:
        ValueError: 未找到 token
        FileNotFoundError: token 文件不存在
    """
    auth = config.get("auth", {})
    token = auth.get("token")

    # 从文件读取 token
    if not token and auth.get("token_file"):
        token_file = auth["token_file"]
        token_path = Path(token_file)
        if token_path.exists():
            token = token_path.read_text().strip()
            logger.debug(f"从 {token_file} 读取 token")

    # 尝试默认 token 文件
    if not token:
        token_path = Path(DEFAULT_TOKEN_FILE)
        if token_path.exists():
            token = token_path.read_text().strip()
            logger.debug(f"从 {DEFAULT_TOKEN_FILE} 读取 token")

    if not token:
        raise ValueError(
            "未找到 CloudPSS token。请提供 auth.token 或创建 .cloudpss_token 文件"
        )

    setToken(token)
    logger.debug("认证成功")
    return token


def get_token_from_config(config: Dict, token_file: Optional[str] = None) -> str:
    """
    从配置中获取 token

    Args:
        config: 配置字典
        token_file: 可选的 token 文件路径

    Returns:
        token: 认证令牌
    """
    auth = config.get("auth", {})
    token = auth.get("token")

    if not token:
        file_path = token_file or auth.get("token_file") or DEFAULT_TOKEN_FILE
        token_path = Path(file_path)
        if token_path.exists():
            token = token_path.read_text().strip()

    return token
