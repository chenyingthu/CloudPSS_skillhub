
'''
powerAPI Layer - Engine Adapter Framework

This package provides the AWT (Abstract Window Toolkit) layer for cloudpss_skills_v2,
following the Java powerAPI pattern where adapters are heavyweight components that directly
interface with simulation engines.

Architecture:
    PowerSkill Layer (API facade) -> powerAPI Layer (Engine adapters) -> Simulation Engines

Usage:
    from cloudpss_skills_v2.powerapi import EngineAdapter, SimulationResult

    class MyEngineAdapter(EngineAdapter):
        ...
'''
from cloudpss_skills_v2.powerapi.base import SimulationStatus, SimulationType, ValidationError, ValidationResult, SimulationResult, EngineConfig, EngineAdapter, AsyncEngineAdapter
__all__ = [
    'SimulationStatus',
    'SimulationType',
    'ValidationError',
    'ValidationResult',
    'SimulationResult',
    'EngineConfig',
    'EngineAdapter',
    'AsyncEngineAdapter']
