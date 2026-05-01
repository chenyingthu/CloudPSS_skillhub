"""Server authentication helpers for the master organizer."""

from pathlib import Path
from typing import Optional

from .crypto import get_crypto_manager
from .models import Server
from .registries import ServerRegistry


TOKEN_SOURCE_INTERNAL = "internal"
TOKEN_SOURCE_ENV = "env"
TOKEN_SOURCE_FILE = "file"
TOKEN_SOURCE_INLINE = "inline"

INTERNAL_TOKEN_FILE = ".cloudpss_token_internal"
PUBLIC_TOKEN_FILE = ".cloudpss_token"
DEFAULT_INTERNAL_OWNER = "chenying"
DEFAULT_INTERNAL_URL = "http://166.111.60.76:50001/"


def normalize_server_url(url: str) -> str:
    """Normalize a server URL for stable registry storage and SDK env usage."""
    value = url.strip()
    if not value:
        raise ValueError("server URL cannot be empty")
    if not value.startswith(("http://", "https://")):
        value = f"http://{value}"
    if not value.endswith("/"):
        value = f"{value}/"
    return value


def read_token_source(source: str, *, repo_root: Optional[Path] = None) -> tuple[str, dict[str, str]]:
    """Read a token from a supported source and return token plus auth metadata."""
    import os

    root = repo_root or Path.cwd()
    if source == TOKEN_SOURCE_INTERNAL:
        token_file = root / INTERNAL_TOKEN_FILE
        token = token_file.read_text(encoding="utf-8").strip()
        return token, {"token_source": TOKEN_SOURCE_INTERNAL, "token_file": str(token_file)}

    if source == TOKEN_SOURCE_ENV:
        token = os.environ.get("CLOUDPSS_TOKEN", "").strip()
        return token, {"token_source": TOKEN_SOURCE_ENV, "env": "CLOUDPSS_TOKEN"}

    token_path = Path(source).expanduser()
    token = token_path.read_text(encoding="utf-8").strip()
    return token, {"token_source": TOKEN_SOURCE_FILE, "token_file": str(token_path)}


def build_auth_metadata(token: str, metadata: Optional[dict[str, str]] = None) -> dict[str, str]:
    """Encrypt token and attach non-secret metadata for server ownership tracking."""
    if not token:
        raise ValueError("token cannot be empty")
    auth = dict(metadata or {})
    auth["encrypted_token"] = f"ENC:{get_crypto_manager().encrypt(token)}"
    return auth


def decrypt_server_token(server: Server) -> str:
    encrypted = server.auth.get("encrypted_token", "")
    if not encrypted:
        raise ValueError(f"server {server.id} does not have an encrypted token")
    if not encrypted.startswith("ENC:"):
        raise ValueError(f"server {server.id} token is not encrypted")
    return get_crypto_manager().decrypt(encrypted[4:])


def get_default_server(registry: Optional[ServerRegistry] = None) -> tuple[str, Server] | None:
    registry = registry or ServerRegistry()
    servers = registry.list_all()
    for server_id, server in servers:
        if getattr(server, "default", False):
            return server_id, server
    return servers[0] if servers else None


def set_default_server(server_id: str, registry: Optional[ServerRegistry] = None) -> bool:
    registry = registry or ServerRegistry()
    if not registry.exists(server_id):
        return False
    for existing_id, _server in registry.list_all():
        registry.update(existing_id, {"default": existing_id == server_id})
    return True


def ensure_internal_server(registry: Optional[ServerRegistry] = None, *, repo_root: Optional[Path] = None) -> tuple[str, Server]:
    """Create or refresh the canonical internal server entry for the local token."""
    registry = registry or ServerRegistry()
    token, auth_meta = read_token_source(TOKEN_SOURCE_INTERNAL, repo_root=repo_root)
    auth = build_auth_metadata(token, auth_meta)

    for server_id, server in registry.list_all():
        if server.url == DEFAULT_INTERNAL_URL and server.owner == DEFAULT_INTERNAL_OWNER:
            registry.update(server_id, {"auth": auth, "default": True, "status": "active"})
            set_default_server(server_id, registry)
            refreshed = registry.get(server_id)
            assert refreshed is not None
            return server_id, refreshed

    from .id_generator import EntityType, IDGenerator

    server_id = IDGenerator.generate(EntityType.SERVER)
    server = Server(
        id=server_id,
        name="CloudPSS Internal",
        url=DEFAULT_INTERNAL_URL,
        owner=DEFAULT_INTERNAL_OWNER,
        auth=auth,
        status="active",
        default=True,
        capabilities=["powerflow", "emt", "stability"],
    )
    registry.create(server_id, server)
    set_default_server(server_id, registry)
    return server_id, server
