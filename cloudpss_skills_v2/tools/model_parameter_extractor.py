
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple
from cloudpss_skills_v2.core import SkillResult, SkillStatus, Artifact, LogEntry
from cloudpss_skills_v2.powerapi import EngineConfig
COMPONENT_DEFINITIONS: 'Dict[str, Dict[str, Any]]' = {
    'bus_3p': {
        'type': 'bus',
        'defaults': {
            'voltage': 110 } },
    'line_3p': {
        'type': 'line',
        'defaults': {
            'rating': 100 } },
    'transformer_3p': {
        'type': 'transformer',
        'defaults': { } },
    'generator_3p': {
        'type': 'generator',
        'defaults': { } },
    'load_3p': {
        'type': 'load',
        'defaults': { } } }
@dataclass
class ComponentParameter:
    name: str = ''
    value_type: str = ''
    default_value: Any = None
    description: str = ''
@dataclass
class ParameterGroup:
    group_name: str = ''
    component_type: str = ''
    parameters: List[ComponentParameter] = field(default_factory=list)

class ModelParameterExtractorTool:
    '''A simplified v2 skill that extracts component parameters from a given model.'''
    
    def __init__(self):
        self.name = 'model_parameter_extractor'

    
    def get_default_config(self):
        '''Return default configuration with all required fields.'''
        return {
            'skill': self.name,
            'auth': {
                'token_file': '.cloudpss_token' },
            'model': {
                'rid': '',
                'source': 'cloud' },
            'component_types': [],
            'extraction': {
                'include_args': True,
                'include_pins': True },
            'output': {
                'format': 'json',
                'path': './results/',
                'prefix': 'model_parameter_extractor' } }

    
    def validate(self, config = None):
        errors = []
        model = config.get('model')
        if not isinstance(model, dict) or model.get('rid'):
            errors.append("Missing or invalid 'model.rid'")
        component_types = config.get('component_types')
        if isinstance(component_types, list) or len(component_types) == 0:
            errors.append("Missing or empty 'component_types'")
def run(self, config = None):
        (valid, errors) = self.validate(config)
        if not valid:
            return SkillResult(skill_name = self.name, status = SkillStatus.FAILED, data = None, artifacts = [], logs = [], metrics = { })
        component_types = None.get('component_types', [])
        groups = []
        for ctype in component_types:
            definition = COMPONENT_DEFINITIONS.get(ctype, { })
            params = []
            for idx in range(2):
                comp_key = f"{ctype}_{idx + 1}"
                comp_rid = f"model/{ctype}/{idx + 1}"
                label = f"{ctype.upper()} {idx + 1}"
                args = {
                    'sample_arg': idx + 1,
                    'rid': comp_rid }
                pins = {
                    'pin': f"P{idx + 1}" }
                params.append(ComponentParameter(comp_key = comp_key, comp_type = ctype, comp_rid = comp_rid, label = label, args = args, pins = pins))
            group_name = f'''{ctype.replace('_3p', '').capitalize()}s'''
            groups.append(ParameterGroup(group_name = group_name, component_type = ctype, parameters = params))
        result_groups = []
