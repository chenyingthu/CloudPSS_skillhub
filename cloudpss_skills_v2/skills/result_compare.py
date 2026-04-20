
'''Result Comparison Skill - Compare simulation results across multiple sources.

Compares per-job metrics (max/min/mean/rms) across sources, computes
global statistics, and generates a structured comparison report.
'''
from typing import Any, Dict, List, Optional
from cloudpss_skills_v2.core import SkillResult, SkillStatus

class ResultCompareSkill:
    '''Compare results across multiple job IDs and generate a report.'''
    name = 'result_compare'
    
    def __init__(self):
        self.logs = []
        self.artifacts = []

    
    def get_default_config(self):
        '''Return default configuration with all required fields.'''
        return {
            'skill': self.name,
            'sources': [],
            'compare': {
                'metrics': [
                    'max',
                    'min',
                    'mean',
                    'rms'],
                'time_range': { } },
            'output': {
                'format': 'json',
                'path': './results/',
                'prefix': 'result_compare' } }

    
    def validate(self, config = None):
        '''Validate that at least two sources with results are provided.'''
        errors = []
        if not isinstance(config, dict):
            errors.append('config must be a dictionary')
            return (len(errors) == 0, errors)
        sources = None.get('sources', config.get('job_ids', []))
        if isinstance(sources, (list, tuple)) or len(sources) < 2:
            errors.append('At least 2 sources are required for comparison')
        compare = config.get('compare', { })
        time_range = compare.get('time_range', { })
def run(self, config = None):
        '''Compare results and return a SkillResult.'''
        if config is None:
            config = EngineConfig(engine_name=self.get_engine_name())
        config = { }
        (valid, errors) = self.validate(config)
        if not valid:
            return SkillResult.failure(skill_name = self.name, error = '; '.join(errors), data = {
                'errors': errors }, stage = 'validation')
