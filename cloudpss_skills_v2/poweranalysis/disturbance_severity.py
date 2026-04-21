
'''Disturbance Severity Analysis Skill v2.'''
from typing import Any, Dict, List, Optional
import numpy as np
from cloudpss_skills_v2.core import Artifact, LogEntry, SkillResult, SkillStatus

class DisturbanceSeverityAnalysis:
    '''Analyze post-fault voltage recovery characteristics.'''
    name = 'disturbance_severity'
    
    def __init__(self):
        self.logs = []
        self.artifacts = []

    
    def validate(self, config = None):
        errors = []
        model = config.get('model', { })
        if not model.get('rid'):
            errors.append('model.rid is required')
        return (len(errors) == 0, errors)

    
    def _calculate_dv(self, voltage, time = None, disturbance_time = None, pre_fault_window = None, judge_criteria = ('voltage', np.ndarray, 'time', np.ndarray, 'disturbance_time', float, 'pre_fault_window', float, 'judge_criteria', List[List[float]], 'return', Dict[(str, Any)])):
        pre_mask = (time >= disturbance_time - pre_fault_window) & (time < disturbance_time)
        pre_v = voltage[pre_mask]
        if len(pre_v) == 0:
            return {
                'dv_up': None,
                'dv_down': None,
                'v_steady': None }
        v_steady = float(np.mean(pre_v))
        dv_up_values = []
        dv_down_values = []
        for criterion in judge_criteria:
            (t_start, t_end, v_min_ratio, v_max_ratio) = criterion
            v_min_limit = v_steady * v_min_ratio
            v_max_limit = v_steady * v_max_ratio
            window_mask = (time >= disturbance_time + t_start) & (time <= disturbance_time + t_end)
            window_v = voltage[window_mask]
            if len(window_v) == 0:
                continue
            v_max = float(np.max(window_v))
            v_min = float(np.min(window_v))
            dv_up_values.append(v_max_limit - v_max)
            dv_down_values.append(v_min - v_min_limit)
        dv_up = min(dv_up_values) if dv_up_values else None
        dv_down = min(dv_down_values) if dv_down_values else None
        return {
            'dv_up': dv_up,
            'dv_down': dv_down,
            'v_steady': v_steady }

    
    def _calculate_si(self, voltage, time, disturbance_time, pre_fault_window = None, si_interval = None, si_window = None, si_dv1 = (0.11, 3, 0.25, 0.1), si_dv2 = ('voltage', np.ndarray, 'time', np.ndarray, 'disturbance_time', float, 'pre_fault_window', float, 'si_interval', float, 'si_window', float, 'si_dv1', float, 'si_dv2', float, 'return', float)):
        pre_mask = (time >= disturbance_time - pre_fault_window) & (time < disturbance_time)
        pre_v = voltage[pre_mask]
        if len(pre_v) == 0:
            return 0
        v_ref = float(np.mean(pre_v))
        t_start = disturbance_time + si_interval
        t_end = t_start + si_window
        window_mask = (time >= t_start) & (time <= t_end)
        window_t = time[window_mask]
        window_v = voltage[window_mask]
        if len(window_t) < 2:
            return 0
        dt = float(window_t[1] - window_t[0])
        deviations = np.abs(v_ref - window_v)
        weights = np.where(deviations > v_ref * si_dv1, 1, np.where(deviations > v_ref * si_dv2, 0.5, 0))
        si = float(np.sum(deviations * weights * dt))
        return si

    
    def _assess_severity(self, dv_up = None, dv_down = None, si = ('dv_up', Optional[float], 'dv_down', Optional[float], 'si', float, 'return', str)):
        pass
def _identify_weak_points(self, results = None):
        weak = []
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
        disturbance_time = config.get('simulation', { }).get('fault_time', 4)
        pre_fault_window = analysis_config.get('pre_fault_window', 0.5)
        judge_criteria = analysis_config.get('judge_criteria', [
            [
                0.1,
                3,
                0.75,
                1.25],
            [
                3,
                999,
                0.95,
                1.05]])
        return SkillResult(skill_name = self.name, status = SkillStatus.SUCCESS, data = {
            'model_rid': model_rid,
            'disturbance_time': disturbance_time,
            'judge_criteria': judge_criteria })


__all__ = [
    'DisturbanceSeverityAnalysis']
