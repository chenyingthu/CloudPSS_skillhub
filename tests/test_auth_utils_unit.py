#!/usr/bin/env python3
"""
认证工具与 baseUrl 路由 - 单元测试
"""

from unittest.mock import Mock, patch

from cloudpss_skills.core.auth_utils import (
    get_base_url_from_config,
    get_cloudpss_kwargs,
    load_or_fetch_model,
    run_emt,
    run_powerflow,
    fetch_job_by_id,
)


class TestAuthUtilsUnit:
    def test_get_base_url_from_config_supports_two_spellings(self):
        assert get_base_url_from_config({"auth": {"base_url": "http://a"}}) == "http://a"
        assert get_base_url_from_config({"auth": {"baseUrl": "http://b"}}) == "http://b"

    def test_get_cloudpss_kwargs_empty_without_base_url(self):
        assert get_cloudpss_kwargs({}) == {}

    @patch("cloudpss.Model")
    def test_load_or_fetch_model_passes_base_url(self, mock_model_class):
        config = {"auth": {"base_url": "http://example.test"}}
        model_config = {"rid": "model/test", "source": "cloud"}
        load_or_fetch_model(model_config, config)
        mock_model_class.fetch.assert_called_once_with("model/test", baseUrl="http://example.test")

    def test_run_emt_passes_base_url(self):
        model = Mock()
        run_emt(model, {"auth": {"base_url": "http://example.test"}})
        model.runEMT.assert_called_once_with(baseUrl="http://example.test")

    def test_run_powerflow_passes_base_url(self):
        model = Mock()
        run_powerflow(model, {"auth": {"base_url": "http://example.test"}})
        model.runPowerFlow.assert_called_once_with(baseUrl="http://example.test")

    @patch("cloudpss.Job")
    def test_fetch_job_by_id_passes_base_url(self, mock_job_class):
        fetch_job_by_id("job-1", {"auth": {"base_url": "http://example.test"}})
        mock_job_class.fetch.assert_called_once_with("job-1", baseUrl="http://example.test")
