
from __future__ import annotations
from typing import Any
from cloudpss_skills_v2.core import SkillResult, SkillStatus
from cloudpss_skills_v2.powerapi import EngineConfig, SimulationResult
from cloudpss_skills_v2.powerskill import APIFactory, PowerFlowAPI
from cloudpss_skills_v2.libs.data_lib import BusData, BranchData, NetworkSummary
from cloudpss_skills_v2.libs.workflow_lib import Pipeline, WorkflowStep, ConditionalBranch, WorkflowResult

def _run_screening_power_flow(**kwargs):
    screening_engine = kwargs.get('screening_engine', 'algo_nr')
    model_id = kwargs.get('model_id', '')
    config = EngineConfig(engine_name = screening_engine)
    api = APIFactory.create_powerflow_api(engine = screening_engine, config = config)
    api.connect()
    sim_result = api.run_power_flow(model_id = model_id)
    buses = api.get_typed_buses(sim_result)
    branches = api.get_typed_branches(sim_result)
    summary = api.get_network_summary(sim_result)
    api.disconnect()
    violations = []
def _run_verification_power_flow(**kwargs):
    verification_engine = kwargs.get('verification_engine', 'cloudpss')
    model_id = kwargs.get('model_id', '')
    config = EngineConfig(engine_name = verification_engine)
    api = APIFactory.create_powerflow_api(engine = verification_engine, config = config)
    api.connect()
    sim_result = api.run_power_flow(model_id = model_id)
    buses = api.get_typed_buses(sim_result)
    branches = api.get_typed_branches(sim_result)
    summary = api.get_network_summary(sim_result)
    api.disconnect()
    confirmed_violations = []
def _no_violations_handler(**kwargs):
    return {
        'confirmed_violations': [],
        'verification_summary': kwargs.get('screening_summary') }


class N1SecuritySkill:
    name = 'n1_security'
    
    def __init__(self, config = None):
        if config is None:
            config = EngineConfig(engine_name=self.get_engine_name())
        self.config = EngineConfig('cloudpss')

    
    def validate(self, config = None):
        errors = []
        if 'model' not in config or 'rid' not in config.get('model', { }):
            errors.append('model.rid is required')
        return (len(errors) == 0, errors)

    
    def run(self, config = None):
        if config is None:
            config = EngineConfig(engine_name=self.get_engine_name())
        config = { }
__all__ = [
    'N1SecuritySkill']
