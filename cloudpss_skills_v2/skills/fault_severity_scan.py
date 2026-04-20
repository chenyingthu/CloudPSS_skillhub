
import numpy as np
from cloudpss_skills_v2.core import SkillResult, SkillStatus, Artifact, LogEntry
from cloudpss_skills_v2.powerapi import EngineConfig

class FaultSeverityScanSkill:
    
    def __init__(self):
        self.name = 'fault_severity_scan'

    
    def validate(self, config = None):
        errors = []
        if not isinstance(config, dict):
            errors.append('Config must be a dictionary.')
            return (False, errors)
        model = None.get('model')
        if isinstance(model, dict) or 'rid' not in model:
            errors.append("Missing or invalid 'model.rid'.")
        scan = config.get('scan')
        if isinstance(scan, dict) or 'chg_values' not in scan:
            errors.append("Missing or invalid 'scan.chg_values'.")
        valid = len(errors) == 0
        return (valid, errors)

    
    def _calculate_severity(self, voltage_drop = None, reference_voltage = None):
        if reference_voltage == 0:
            return 0
        return float(voltage_drop) / float(reference_voltage)

    
    def _assess_severity_level(self, severity_fraction = None):
        if severity_fraction < 0.2:
            return 'low'
        if severity_fraction < 0.6:
            return 'moderate'
        return 'critical'

    
    def _calculate_recovery_time(self, voltage = None, time = None, threshold = ('voltage', np.ndarray, 'time', np.ndarray, 'threshold', float, 'return', float)):
        v = np.asarray(voltage)
        t = np.asarray(time)
        if v.size == 0:
            return 0
        below = np.where(v < threshold)[0]
        if below.size == 0:
            if t.size > 0:
                return float(t[0])
            return None
        last_below = float(below[-1])
        return float(t[last_below])

    
    def run(self, config = None):
        (valid, errors) = self.validate(config)
        if not valid:
            return SkillResult(skill_name = self.name, status = SkillStatus.FAILED, data = None, artifacts = [], logs = [], metrics = { })
        model_rid = None
