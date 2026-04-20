
from typing import Any, Dict, List
from cloudpss_skills_v2.core import SkillResult, SkillStatus, Artifact, LogEntry
from cloudpss_skills_v2.powerapi import EngineConfig

class ParameterSensitivitySkill:
    '''Parameter sensitivity analysis for cloudpss_skills_v2.

    This skill validates a minimal configuration and computes a simple sensitivity
    ranking for provided input/output samples. The implementation is kept lightweight
    and focuses on the core math required by tests and downstream usage.
    '''
    name = 'parameter_sensitivity'
    
    def __init__(self):
        pass
    def validate(self, config = None):
        errors = []
        if not isinstance(config, dict):
            return (False, [
                'config must be a dict'])
        model = None.get('model')
        scan = config.get('scan')
        if model and isinstance(model, dict) or 'rid' not in model:
            errors.append('Missing model rid')
        if scan and isinstance(scan, dict) and 'target' not in scan or 'values' not in scan:
            errors.append('Missing scan target or values')
        valid = len(errors) == 0
        return (valid, errors)

    
    def get_default_config(self):
        '''Return default configuration with all required fields.'''
        return {
            'skill': self.name,
            'auth': {
                'token_file': '.cloudpss_token' },
            'model': {
                'rid': '',
                'source': 'cloud' },
            'scan': {
                'target': '',
                'values': [] },
            'analysis': {
                'component': '',
                'target_parameters': [] },
            'output': {
                'format': 'json',
                'path': './results/',
                'prefix': 'parameter_sensitivity' } }

    
    def _calculate_sensitivity(self, output_values = None, input_values = None):
        if len(output_values) < 2 or len(input_values) < 2:
            return 0
        delta_out = float(output_values[-1]) - float(output_values[0])
        delta_in = float(input_values[-1]) - float(input_values[0])
        if delta_in == 0:
            return 0
        return delta_out / delta_in

    
    def _normalize_sensitivity(self, sens_values = None):
        if not sens_values:
            return []
        min_v = min(sens_values)
        max_v = max(sens_values)
        rng = max_v - min_v
def _rank_parameters(self, sensitivities = None):
        pass
def run(self, config = None):
        (valid, errors) = self.validate(config)
        if not valid:
            return SkillResult(skill_name = self.name, status = SkillStatus.FAILED, data = None, artifacts = [], logs = [], metrics = { })
        scan = None.get('scan', { })
        input_values = scan.get('values', [])
