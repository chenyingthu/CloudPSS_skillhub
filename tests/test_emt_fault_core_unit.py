#!/usr/bin/env python3
"""
EMT故障扫描公共内核 - 单元测试
"""

from cloudpss_skills.core.emt_fault_core import trace_rms, trace_value_at_time


class TestEmtFaultCoreUnit:
    def test_trace_rms_requires_nonempty_window(self):
        trace = {"x": [0.0, 1.0], "y": [1.0, 1.0]}
        try:
            trace_rms(trace, 2.0, 3.0)
            assert False, "expected ValueError"
        except ValueError as e:
            assert "无数据" in str(e)

    def test_trace_value_at_time_requires_close_sample(self):
        trace = {"x": [0.0, 1.0], "y": [1.0, 2.0]}
        try:
            trace_value_at_time(trace, 0.5)
            assert False, "expected ValueError"
        except ValueError as e:
            assert "未找到目标通道采样点" in str(e)
