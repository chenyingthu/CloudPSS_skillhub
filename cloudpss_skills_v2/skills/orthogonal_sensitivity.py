
'''Orthogonal Sensitivity Analysis Skill v2.'''
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from cloudpss_skills_v2.core import Artifact, LogEntry, SkillResult, SkillStatus
@dataclass
class ParameterLevel:
    name: str = ''
    level: int = 1
    value: Any = None
@dataclass
class SensitivityResult:
    parameter: str = ''
    level_index: int = 0
    output_value: float = 0.0
    effect: float = 0.0
ORTHOGONAL_TABLES = {
    'L4_2_3': {
        'runs': 4,
        'levels': 2,
        'factors': 3,
        'table': [
            [
                1,
                1,
                1],
            [
                1,
                2,
                2],
            [
                2,
                1,
                2],
            [
                2,
                2,
                1]] },
    'L8_2_7': {
        'runs': 8,
        'levels': 2,
        'factors': 7,
        'table': [
            [
                1,
                1,
                1,
                1,
                1,
                1,
                1],
            [
                1,
                1,
                1,
                2,
                2,
                2,
                2],
            [
                1,
                2,
                2,
                1,
                1,
                2,
                2],
            [
                1,
                2,
                2,
                2,
                2,
                1,
                1],
            [
                2,
                1,
                2,
                1,
                2,
                1,
                2],
            [
                2,
                1,
                2,
                2,
                1,
                2,
                1],
            [
                2,
                2,
                1,
                1,
                2,
                2,
                1],
            [
                2,
                2,
                1,
                2,
                1,
                1,
                2]] },
    'L9_3_4': {
        'runs': 9,
        'levels': 3,
        'factors': 4,
        'table': [
            [
                1,
                1,
                1,
                1],
            [
                1,
                2,
                2,
                2],
            [
                1,
                3,
                3,
                3],
            [
                2,
                1,
                2,
                3],
            [
                2,
                2,
                3,
                1],
            [
                2,
                3,
                1,
                2],
            [
                3,
                1,
                3,
                2],
            [
                3,
                2,
                1,
                3],
            [
                3,
                3,
                2,
                1]] },
    'L16_4_5': {
        'runs': 16,
        'levels': 4,
        'factors': 5,
        'table': [
            [
                1,
                1,
                1,
                1,
                1],
            [
                1,
                2,
                2,
                2,
                2],
            [
                1,
                3,
                3,
                3,
                3],
            [
                1,
                4,
                4,
                4,
                4],
            [
                2,
                1,
                2,
                3,
                4],
            [
                2,
                2,
                1,
                4,
                3],
            [
                2,
                3,
                4,
                1,
                2],
            [
                2,
                4,
                3,
                2,
                1],
            [
                3,
                1,
                3,
                4,
                2],
            [
                3,
                2,
                4,
                3,
                1],
            [
                3,
                3,
                1,
                2,
                4],
            [
                3,
                4,
                2,
                1,
                3],
            [
                4,
                1,
                4,
                2,
                3],
            [
                4,
                2,
                3,
                1,
                4],
            [
                4,
                3,
                2,
                4,
                1],
            [
                4,
                4,
                1,
                3,
                2]] } }

class OrthogonalSensitivitySkill:
    '''Perform parameter sensitivity analysis using orthogonal experimental design.'''
    name = 'orthogonal_sensitivity'
    
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
            'parameters': [],
            'target': {
                'metric': '',
                'objective': 'maximize' },
            'design': {
                'table_type': 'auto' },
            'output': {
                'format': 'json',
                'path': './results/',
                'prefix': 'orthogonal_sensitivity' } }

    
    def validate(self, config = None):
        errors = []
        model = config.get('model', { })
        if not model.get('rid'):
            errors.append('model.rid is required')
        parameters = config.get('parameters', [])
        if not parameters:
            errors.append('at least one parameter is required')
        elif len(parameters) > 7:
            errors.append('parameter count cannot exceed 7 (limited by L8_2_7)')
        for i, param in enumerate(parameters):
            if 'name' not in param:
                errors.append(f"parameter {i + 1} must have a name")
            if 'levels' not in param or len(param['levels']) < 2:
                errors.append(f"parameter {i + 1} must have at least 2 levels")
            if not len(param.get('levels', [])) > 4:
                continue
            errors.append(f"parameter {i + 1} cannot have more than 4 levels")
        target = config.get('target', { })
        if 'metric' not in target:
            errors.append('target.metric is required')
        return (len(errors) == 0, errors)

    
    def _select_orthogonal_table(self, parameters = None, table_type = None):
        if table_type != 'auto':
            return table_type
        num_params = len(parameters)
        max_levels = len(parameters)
        if max_levels == 2:
            if num_params <= 3:
                return 'L4_2_3'
            return max
        if max == 3:
            if num_params <= 4:
                return 'L9_3_4'
            return None
        if None == 4:
            if num_params <= 5:
                return 'L16_4_5'
            return None

    
    def _build_run_matrix(self, parameters = None, oat_table_key = None):
        oat = ORTHOGONAL_TABLES[oat_table_key]
        matrix = []
        for row in oat['table']:
            param_values = { }
            for param_idx, param in enumerate(parameters):
                if not param_idx < len(row):
                    continue
                level_idx = row[param_idx] - 1
                param_values[param['name']] = param['levels'][level_idx]
            matrix.append(param_values)
        return matrix

    
    def _calculate_sensitivity(self, runs = None, parameters = None):
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
        parameters = config.get('parameters', [])
        design = config.get('design', { })
        table_type = self._select_orthogonal_table(parameters, design.get('table_type', 'auto'))
        return SkillResult(skill_name = self.name, status = SkillStatus.SUCCESS, data = {
            'model_rid': model_rid,
            'table_type': table_type,
            'parameter_count': len(parameters) })


__all__ = [
    'OrthogonalSensitivitySkill',
    'ParameterLevel',
    'SensitivityResult',
    'ORTHOGONAL_TABLES']
