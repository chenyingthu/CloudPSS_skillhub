
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
from cloudpss_skills_v2.core import SkillResult, SkillStatus
from cloudpss_skills_v2.powerapi import EngineConfig
@dataclass
class StabilityMargin:
    metric_name: str = ''
    value: float = 0.0
    limit: float = 0.0
    margin_pct: float = 0.0
    is_secure: bool = True

class TransientStabilityMarginAnalysis:
    '''Lightweight implementation of the transient stability margin analysis.

    This is a simplified port focused on the testable math and data flow
    patterns used in CloudPSS v2 skills.
    '''
    
    def __init__(self):
        self.name = 'TransientStabilityMargin'

    
    def validate(self, config = None):
        errors = []
        model = config.get('model')
        if not isinstance(model, dict) or model.get('rid'):
            errors.append('Missing model.rid')
        if not config.get('fault_scenarios') and config.get('generators'):
            errors.append('Missing fault_scenarios or generators')
        return (len(errors) == 0, errors)

    
    def _calculate_margin_percent(self, cct = None, actual_time = None):
        if cct <= 0:
            return 0
        return ((cct - actual_time) / cct) * 100

    
    def _assess_stability(self, margin_percent = None):
        threshold = 10
        if margin_percent > threshold:
            return 'stable'
        if margin_percent < 0:
            return 'unstable'
        return 'marginal'

    
    def _binary_search_cct(self, fault_location = None, actual_time = None, target_margin = (0.3, 10)):
        ratio = 1 - target_margin / 100
        if ratio <= 0:
            return max(actual_time, 0.5)
        cct = None / ratio
        if cct <= 0:
            cct = 0.5
        return cct

    
    def run(self, config = None):
        (valid, errors) = self.validate(config)
        if not valid:
            return SkillResult(skill_name = self.name, status = SkillStatus.FAILED, data = None, artifacts = [], logs = [], metrics = { })
        fault_scenarios = None.get('fault_scenarios', [])
        results = []
        for fs in fault_scenarios:
            location = fs.get('location', 'UNKNOWN')
            cct = self._binary_search_cct(location, actual_time = 0.3, target_margin = 10)
            margin = self._calculate_margin_percent(cct, 0.3)
            status = self._assess_stability(margin)
            results.append(StabilityMargin(fault_location = location, cct = cct, margin_percent = margin, stability_status = status))
__all__ = [
    'TransientStabilityMarginAnalysis',
    'StabilityMargin']
