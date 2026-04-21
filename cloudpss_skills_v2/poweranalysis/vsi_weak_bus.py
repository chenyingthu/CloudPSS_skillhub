
'''VSI Weak Bus Analysis Skill v2.'''
from typing import Any, Dict, List, Optional
import numpy as np
from cloudpss_skills_v2.core import Artifact, LogEntry, SkillResult, SkillStatus

class VSIWeakBusAnalysis:
    '''Identify weak buses via Voltage Stability Index analysis.'''
    name = 'vsi_weak_bus'
    
    def __init__(self):
        self.logs = []
        self.artifacts = []

    
    def validate(self, config = None):
        errors = []
        model = config.get('model', { })
        if not model.get('rid'):
            errors.append('model.rid is required')
        return (len(errors) == 0, errors)

    
    def _calculate_vsi(self, voltage_pre = None, voltage_post = None, q_injected = ('voltage_pre', float, 'voltage_post', float, 'q_injected', float, 'return', float)):
        if q_injected == 0:
            return 0
        delta_v = abs(voltage_post - voltage_pre)
        return delta_v / abs(q_injected)

    
    def _matches_bus_identifier(self, candidate = None, target = None):
        c = candidate.lower().replace('_', ' ').strip()
        t = target.lower().replace('_', ' ').strip()
        return c == t

    
    def _identify_weak_buses(self, vsi_results = None, threshold = None, top_n = (0.01, 10)):
        sorted_buses = sorted(vsi_results.items(), key = (lambda x: x[1]), reverse = True)
        weak = []
        for bus_label, vsi in sorted_buses[:top_n]:
            if not vsi >= threshold:
                continue
            weak.append({
                'label': bus_label,
                'vsi': vsi,
                'is_weak': True })
        return weak

    
    def _compute_vsi_statistics(self, vsi_values = None, threshold = None):
        pass
def run(self, config = None):
        if config is None:
            config = EngineConfig(engine_name=self.get_engine_name())
        config = { }
        (valid, errors) = self.validate(config)
        if not valid:
            return SkillResult.failure(skill_name = self.name, error = '; '.join(errors), data = {
                'stage': 'validation',
                'errors': errors })
        model_rid = config['model']['rid']
        analysis_config = config.get('analysis', { })
        threshold = analysis_config.get('vsi_threshold', 0.01)
        return SkillResult(skill_name = self.name, status = SkillStatus.SUCCESS, data = {
            'model_rid': model_rid,
            'vsi_threshold': threshold })


__all__ = [
    'VSIWeakBusAnalysis']
