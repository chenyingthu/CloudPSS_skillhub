#!/usr/bin/env python3
"""
EMT故障扫描公共内核 - 单元测试
"""

import pytest

from cloudpss_skills.core.emt_fault_core import trace_rms, trace_value_at_time


class TestEmtFaultCoreUnit:
    def test_trace_rms_requires_nonempty_window(self):
        trace = {"x": [0.0, 1.0], "y": [1.0, 1.0]}
        with pytest.raises(ValueError, match="无数据"):
            trace_rms(trace, 2.0, 3.0)

    def test_trace_value_at_time_requires_close_sample(self):
        trace = {"x": [0.0, 1.0], "y": [1.0, 2.0]}
        with pytest.raises(ValueError, match="未找到目标通道采样点"):
            trace_value_at_time(trace, 0.5)
