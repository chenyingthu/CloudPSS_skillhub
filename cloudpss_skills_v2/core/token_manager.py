from __future__ import annotations

import json
import os
import warnings
from pathlib import Path
from typing import Any


class TokenManager:
    """
    Token 管理器 - 安全的 token 获取策略

    优先级：
    1. 显式配置 (最安全)
    2. 环境变量
    3. 用户本地配置文件
    4. 当前工作目录 .cloudpss_token (仅开发)
    """

    _MIN_TOKEN_LENGTH: int = 10

    @staticmethod
    def get_token(config: dict[str, Any] | None = None) -> str:
        """获取 token，按优先级尝试。"""
        auth_config = config or {}

        explicit_token = auth_config.get("token")
        if explicit_token:
            token = str(explicit_token).strip()
            if TokenManager.validate_token(token):
                return token
            raise ValueError("Invalid CloudPSS token format in auth.token")

        env_token = os.environ.get("CLOUDPSS_TOKEN")
        if env_token:
            token = env_token.strip()
            if TokenManager.validate_token(token):
                return token
            raise ValueError("Invalid CloudPSS token format in CLOUDPSS_TOKEN")

        user_config = Path.home() / ".cloudpss" / "config"
        if user_config.exists():
            try:
                config_data = json.loads(user_config.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise ValueError(
                    f"Failed to read CloudPSS config from {user_config}: {exc}"
                ) from exc

            if not isinstance(config_data, dict):
                raise ValueError(
                    f"Invalid CloudPSS config format in {user_config}: expected object"
                )

            token = str(config_data.get("token", "")).strip()
            if token:
                if TokenManager.validate_token(token):
                    return token
                raise ValueError(
                    f"Invalid CloudPSS token format in user config: {user_config}"
                )

        dev_token_path = Path.cwd() / ".cloudpss_token"
        if dev_token_path.exists():
            try:
                token = dev_token_path.read_text(encoding="utf-8").strip()
            except OSError as exc:
                raise ValueError(
                    f"Failed to read development token from {dev_token_path}: {exc}"
                ) from exc

            warnings.warn(
                "Using CloudPSS token from current working directory; "
                "avoid this in production environments.",
                stacklevel=2,
            )
            if TokenManager.validate_token(token):
                return token
            raise ValueError(
                f"Invalid CloudPSS token format in development token file: {dev_token_path}"
            )

        raise ValueError(
            "No CloudPSS token found. Provide auth.token, set CLOUDPSS_TOKEN, "
            "store token in ~/.cloudpss/config, or create .cloudpss_token for local development."
        )

    @staticmethod
    def validate_token(token: object) -> bool:
        """验证 token 格式。"""
        if not isinstance(token, str):
            return False

        normalized = token.strip()
        if len(normalized) < TokenManager._MIN_TOKEN_LENGTH:
            return False
        if any(ch.isspace() for ch in normalized):
            return False

        return True


class CloudPSSAdapter:
    """CloudPSS SDK wrapper that stores auth state on the instance."""

    DEFAULT_API_URL: str = "https://www.cloudpss.net/"
    INTERNAL_API_URL: str = "https://internal.cloudpss.com"

    def __init__(self, token: str | None = None, api_url: str | None = None):
        self.token: str | None = token
        self.api_url: str = api_url or self.DEFAULT_API_URL

    @classmethod
    def from_config(cls, config: dict[str, object]) -> "CloudPSSAdapter":
        """Create an adapter from a simulation or engine config dict."""

        nested_auth = config.get("auth")
        if isinstance(nested_auth, dict):
            auth = nested_auth
        else:
            auth = config

        token = TokenManager.get_token(auth)
        return cls(token=token, api_url=cls.resolve_api_url(auth))

    @classmethod
    def resolve_api_url(cls, auth: dict[str, object]) -> str:
        """Resolve CloudPSS API URL without modifying ``os.environ``."""

        base_url = auth.get("base_url") or auth.get("baseUrl")
        if isinstance(base_url, str) and base_url:
            return base_url
        if auth.get("server") == "internal":
            return cls.INTERNAL_API_URL
        return cls.DEFAULT_API_URL

    def connect(self) -> bool:
        """Authenticate the CloudPSS SDK using this instance's token."""

        if not self.token:
            return False

        try:
            from cloudpss import setToken
        except ImportError:
            return False

        setToken(self.token)
        return True

    def sdk_kwargs(self) -> dict[str, str]:
        """Return explicit SDK keyword arguments for endpoint selection."""

        if self.api_url == self.DEFAULT_API_URL:
            return {}
        return {"baseUrl": self.api_url}


def build_cloudpss_adapter(config: dict[str, object]) -> CloudPSSAdapter:
    """Resolve auth for a config dict and return a connected SDK wrapper."""

    adapter = CloudPSSAdapter.from_config(config)
    _ = adapter.connect()
    return adapter
