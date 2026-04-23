"""
认证工具模块

提供统一的 CloudPSS 认证功能与可选 baseUrl 路由支持。
"""

import logging
from pathlib import Path
from typing import Dict, Optional

from cloudpss import setToken

logger = logging.getLogger(__name__)

# 默认配置常量
DEFAULT_TOKEN_FILE = ".cloudpss_token"
DEFAULT_INTERNAL_TOKEN_FILE = ".cloudpss_token_internal"
DEFAULT_PAGE_SIZE = 1000
DEFAULT_TIMEOUT = 300
DEFAULT_POWERFLOW_TOLERANCE = 1e-6
DEFAULT_VOLTAGE_MIN = 0.5
DEFAULT_VOLTAGE_MAX = 1.5

# CloudPSS 服务器配置
SERVER_URLS = {
    "public": "https://cloudpss.net/",
    "internal": os.environ.get("CLOUDPSS_INTERNAL_URL", "https://internal.cloudpss.com"),
}


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
    import os

    auth = config.get("auth", {})
    token = auth.get("token")

    # 确定使用哪个服务器
    server = auth.get("server", "public")
    base_url = auth.get("base_url") or auth.get("baseUrl")

    # 如果指定了 baseUrl，优先使用
    if base_url:
        os.environ["CLOUDPSS_API_URL"] = base_url
        logger.debug(f"使用自定义 baseUrl: {base_url}")
    elif server == "internal":
        os.environ["CLOUDPSS_API_URL"] = SERVER_URLS["internal"]
        logger.debug(f"使用内部服务器: {SERVER_URLS['internal']}")
    else:
        os.environ["CLOUDPSS_API_URL"] = SERVER_URLS["public"]
        logger.debug(f"使用公共云服务器: {SERVER_URLS['public']}")

    # 选择对应的 token 文件
    if not token:
        if server == "internal":
            token_file = auth.get("token_file") or DEFAULT_INTERNAL_TOKEN_FILE
        else:
            token_file = auth.get("token_file") or DEFAULT_TOKEN_FILE

        token_path = Path(token_file)
        if token_path.exists():
            token = token_path.read_text().strip()
            logger.debug(f"从 {token_file} 读取 token")

    # 尝试默认 token 文件
    if not token:
        for default_file in [DEFAULT_TOKEN_FILE, DEFAULT_INTERNAL_TOKEN_FILE]:
            token_path = Path(default_file)
            if token_path.exists():
                token = token_path.read_text().strip()
                logger.debug(f"从 {default_file} 读取 token")
                break

    if not token:
        raise ValueError(
            "未找到 CloudPSS token。请提供 auth.token 或创建 .cloudpss_token 文件"
        )

    setToken(token)
    logger.debug("认证成功")
    return token


def get_base_url_from_config(config: Dict) -> Optional[str]:
    """
    从配置中获取备用 CloudPSS 服务地址。

    支持:
    - auth.base_url
    - auth.baseUrl
    """
    auth = config.get("auth", {})
    return auth.get("base_url") or auth.get("baseUrl")


def get_cloudpss_kwargs(config: Optional[Dict] = None) -> Dict[str, str]:
    """构造 CloudPSS SDK 调用参数。"""
    if not config:
        return {}

    base_url = get_base_url_from_config(config)
    if base_url:
        return {"baseUrl": base_url}
    return {}


def load_or_fetch_model(model_config: Dict, config: Optional[Dict] = None):
    """统一处理本地/云端模型获取，并透传可选 baseUrl。"""
    from cloudpss import Model

    if model_config.get("source") == "local":
        return Model.load(model_config["rid"])
    return Model.fetch(model_config["rid"], **get_cloudpss_kwargs(config))


def fetch_model_by_rid(rid: str, config: Optional[Dict] = None):
    """按 RID 获取云端模型，并透传可选 baseUrl。"""
    from cloudpss import Model

    return Model.fetch(rid, **get_cloudpss_kwargs(config))


def fetch_job_by_id(job_id: str, config: Optional[Dict] = None):
    """按 job id 获取任务，并透传可选 baseUrl。"""
    from cloudpss import Job

    return Job.fetch(job_id, **get_cloudpss_kwargs(config))


def run_powerflow(model, config: Optional[Dict] = None, **kwargs):
    """统一运行潮流，并透传可选 baseUrl。"""
    return model.runPowerFlow(**get_cloudpss_kwargs(config), **kwargs)


def run_emt(model, config: Optional[Dict] = None, **kwargs):
    """统一运行 EMT，并透传可选 baseUrl。"""
    return model.runEMT(**get_cloudpss_kwargs(config), **kwargs)


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
