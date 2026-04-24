"""Tests for cloudpss_skills_v2.tools.model_hub."""

import base64
import json

from cloudpss_skills_v2.tools.model_hub import (
    ModelHubTool,
    normalize_model_name,
    parse_token_username,
)


def _jwt(payload):
    encoded = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8").rstrip("=")
    return f"header.{encoded}.sig"


class TestModelHubTool:
    def test_normalize_model_name(self):
        assert normalize_model_name("IEEE 39-Bus") == "ieee_39_bus"

    def test_parse_token_username(self):
        token = _jwt({"username": "alice"})
        assert parse_token_username(token) == "alice"

    def test_validate_private_server_requires_token(self):
        tool = ModelHubTool()
        valid, errors = tool.validate({"servers": [{"name": "s1", "url": "https://x"}]})
        assert valid is False
        assert "token is required" in errors[0]

    def test_run_search_merges_models_across_servers(self):
        tool = ModelHubTool()
        config = {
            "action": "search",
            "query": "ieee",
            "servers": [
                {
                    "name": "srv-a",
                    "url": "https://a",
                    "token": _jwt({"username": "alice"}),
                    "models": [{"name": "IEEE39", "rid": "model/a/IEEE39", "metadata": {"tag": "benchmark"}}],
                },
                {
                    "name": "srv-b",
                    "url": "https://b",
                    "is_public": True,
                    "models": [{"name": "IEEE39", "rid": "model/b/IEEE39"}, {"name": "WECC", "rid": "model/b/WECC"}],
                },
            ],
        }
        result = tool.run(config)

        assert result.status.value == "success"
        assert len(result.data["models"]) == 1
        assert sorted(result.data["models"][0]["rids"].keys()) == ["srv-a", "srv-b"]
        assert result.metrics["model_count"] == 2

    def test_run_get_and_cache_actions(self):
        tool = ModelHubTool()
        base_config = {
            "action": "list",
            "cache": {"enabled": True, "key": "hub-test"},
            "servers": [{"name": "srv", "url": "https://x", "is_public": True, "models": [{"name": "Demo", "rid": "model/demo"}]}],
        }
        list_result = tool.run(base_config)
        get_result = tool.run({**base_config, "action": "get", "query": "Demo"})
        cache_result = tool.run({"action": "cache_status"})
        clear_result = tool.run({"action": "clear_cache", "cache": {"key": "hub-test"}})

        assert list_result.data["models"][0]["name"] == "Demo"
        assert get_result.data["model"]["name"] == "Demo"
        assert "hub-test" in cache_result.data["keys"]
        assert clear_result.data["cleared"] is True
