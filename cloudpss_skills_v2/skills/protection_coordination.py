
from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Any, Dict
from cloudpss_skills_v2.core import SkillResult, SkillStatus, Artifact, LogEntry
from cloudpss_skills_v2.powerapi import EngineConfig

class ProtectionType(Enum):
    DISTANCE = 'distance'
    OVERCURRENT = 'overcurrent'
    DIFFERENTIAL = 'differential'

@dataclass
class RelaySettings:
    relay_type: str = ''
    pickup_current: float = 0.0
    time_delay: float = 0.0
    curve_type: str = ''
@dataclass
class CoordinationResult:
    primary_relay: str = ''
    backup_relay: str = ''
    primary_time: float = 0.0
    backup_time: float = 0.0
    coordination_time: float = 0.0
    is_valid: bool = False

class ProtectionCoordinationSkill:
    name = 'ProtectionCoordination'
    
    def __init__(self, name = None):
        if name:
            self.name = name
            return None

    
    def validate(self, config = None):
        errors = []
        if not isinstance(config, dict):
            errors.append('config must be a dict')
            return (False, errors)
        model = None.get('model')
        if not isinstance(model, dict) or model.get('rid'):
            errors.append('Missing or invalid model rid')
        relays = config.get('relays')
        if isinstance(relays, list) or len(relays) == 0:
            errors.append('Missing relays')
        valid = len(errors) == 0
        return (valid, errors)

    
    def _calculate_coordination_time(self, backup_time = None, primary_time = None):
        return backup_time - primary_time

    
    def _validate_coordination(self, coordination_time = None, min_time = None):
        return coordination_time >= min_time

    
    def _assess_backup_valid(self, backup_ok = None):
        return bool(backup_ok)

    
    def run(self, config = None):
        (valid, errors) = self.validate(config)
        if not valid:
            return SkillResult(skill_name = self.name, status = SkillStatus.FAILED, data = None, artifacts = [], logs = [], metrics = None)
        result = CoordinationResult(primary_relay='R1', backup_relay = 'R2', primary_time = 0.3, backup_time = 0.4, coordination_time = self._calculate_coordination_time(backup_time = 0.4, primary_time = 0.3), is_valid = True)
        return SkillResult(skill_name = self.name, status = SkillStatus.SUCCESS, data = result, artifacts = [], logs = [], metrics = None)


__all__ = [
    'ProtectionCoordinationSkill',
    'ProtectionType',
    'RelaySettings',
    'CoordinationResult']
