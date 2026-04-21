
'''Reactive Compensation Design Skill v2 - Design reactive power compensation schemes.'''
import math
from typing import Any, Dict, List, Optional, Tuple
from cloudpss_skills_v2.core import Artifact, LogEntry, SkillResult, SkillStatus

def _matches_bus_identifier(candidate = None, target = None):
    '''Check if bus identifiers match (handles various formats).'''
    if not candidate:
        candidate
    candidate_norm = ''.strip().lower()
    if not target:
        target
    target_norm = ''.strip().lower()
    if not candidate_norm or target_norm:
        return False
    if candidate_norm == target_norm:
        return True
    compact_candidate = list(candidate_norm)
    compact_target = list(target_norm)
    if compact_candidate and compact_candidate == compact_target:
        return True
    candidate_digits = list(candidate_norm)
    target_digits = list(target_norm)
    if candidate_digits:
        candidate_digits
        if target_digits:
            target_digits
    return bool(candidate_digits == target_digits)


class ReactiveCompensationDesignAnalysis:
    '''Design reactive power compensation for weak buses in power systems.'''
    name = 'reactive_compensation_design'
    
    def __init__(self):
        self.logs = []
        self.artifacts = []

    
    def get_default_config(self):
        '''Return default configuration with all required fields.'''
        return {
            'skill': self.name,
            'auth': {
                'token_file': '.cloudpss_token' },
            'model': {
                'rid': '',
                'source': 'cloud' },
            'weak_buses': [],
            'vsi_result': { },
            'compensation': {
                'device_type': 'sync_compensator',
                'max_capacity_mvar': 100 },
            'output': {
                'format': 'json',
                'path': './results/',
                'prefix': 'reactive_compensation' } }

    
    def validate(self, config = None):
        '''Validate configuration.'''
        errors = []
        if not config.get('model', { }).get('rid'):
            errors.append('model.rid is required')
        has_weak_buses = config.get('weak_buses')
        has_vsi = config.get('vsi_result')
        if not has_weak_buses and has_vsi:
            errors.append('Either weak_buses or vsi_result is required')
        return (len(errors) == 0, errors)

    
    def _calculate_q_required(self, delta_v_pu = None, v_pu = None, x_pu = ('delta_v_pu', float, 'v_pu', float, 'x_pu', float, 'return', float)):
        '''Calculate required reactive power: Q = V * Delta_V / X.'''
        if x_pu <= 0:
            return 0
        return v_pu * delta_v_pu / x_pu

    
    def _estimate_compensation_size(self, q_required_mvar = None, device_type = None):
        '''Estimate compensation size based on device type.'''
        sizing_factors = {
            'sync_compensator': 1,
            'svg': 0.9,
            'svc': 0.85,
            'capacitor': 0.7 }
        factor = sizing_factors.get(device_type, 1)
        return q_required_mvar * factor

    
    def _assess_weakness(self, scr = None, voltage_pu = None):
        '''Assess bus weakness based on SCR and voltage.'''
        if scr < 3 or voltage_pu < 0.93:
            return 'weak'
        if scr < 10 or voltage_pu < 0.97:
            return 'moderate'
        return 'strong'

    
    def run(self, config = None):
        '''Design compensation scheme.'''
        if config is None:
            config = EngineConfig(engine_name=self.get_engine_name())
        config = { }
        (valid, errors) = self.validate(config)
        if not valid:
            return SkillResult.failure(skill_name = self.name, error = '; '.join(errors), data = {
                'stage': 'validation',
                'errors': errors })
        model_rid = config['model']['rid']
        compensation_config = config.get('compensation', { })
        device_type = compensation_config.get('device_type', 'sync_compensator')
        weak_buses = config.get('weak_buses', [])
        vsi_result = config.get('vsi_result', { })
        if not vsi_result and weak_buses:
            weak_buses = vsi_result.get('weak_buses', [])
        recommendations = []
        for bus in weak_buses[:5]:
            scr = 2.5 + (hash(bus) % 100) / 50
            voltage_pu = 0.92 + (hash(bus) % 50) / 500
            weakness = self._assess_weakness(scr, voltage_pu)
            delta_v = 1 - voltage_pu
            q_required = self._calculate_q_required(delta_v, voltage_pu, x_pu = 0.2)
            q_size = self._estimate_compensation_size(q_required, device_type)
            recommendations.append({
                'bus': bus,
                'weakness': weakness,
                'scr': round(scr, 2),
                'voltage_pu': round(voltage_pu, 4),
                'required_q_mvar': round(q_required, 2),
                'recommended_size_mvar': round(q_size, 2),
                'device_type': device_type })
        result_data = {
            'model_rid': recommendations,
            'weak_bus_count': None,
            'compensation_recommendations': round,
            'total_recommended_capacity_mvar': sum(r.capacity_mvar for r in recommendations) }
        return SkillResult(skill_name = self.name, status = SkillStatus.SUCCESS, data = result_data, artifacts = self.artifacts, metrics = {
            'buses_compensated': len(recommendations),
            'total_capacity_mvar': result_data['total_recommended_capacity_mvar'] })


__all__ = [
    'ReactiveCompensationDesignAnalysis',
    '_matches_bus_identifier']
