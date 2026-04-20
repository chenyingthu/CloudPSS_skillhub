
from __future__ import annotations
import math
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
from cloudpss_skills_v2.core import SkillResult, SkillStatus, Artifact, LogEntry
from cloudpss_skills_v2.powerskill import APIFactory

class HarmonicAnalysisSkill:
    '''Harmonic analysis using FFT on EMT waveform data.

    This v2 skill focuses on performing FFT analysis on waveform data
    returned by a short EMT simulation and extracting fundamental and
    harmonic components. The EMT API integration is simplified to use a
    factory to obtain an EMT API instance and run a short, representative
    simulation.
    '''
    
    def __init__(self, config = None):
        self.name = 'harmonic_analysis'
        if config is None:
            config = EngineConfig(engine_name=self.get_engine_name())
        self.config = { }

    
    def validate(self, config = None):
        errors = []
        if not isinstance(config, dict) or config:
            errors.append('Missing or invalid configuration for HarmonicAnalysisSkill')
        return (len(errors) == 0, errors)

    
    def _fft_analysis(self, waveform = None, sample_rate = None):
        arr = np.asarray(waveform, dtype = float)
        if arr.size == 0:
            return {
                'fundamental_freq': None,
                'frequencies': [],
                'magnitudes': [] }
        n = None.size
        freqs = np.fft.rfftfreq(n, d = 1 / float(sample_rate))
        spectrum = np.abs(np.fft.rfft(arr))
        max_idx = int(np.argmax(spectrum))
        fundamental = float(freqs[max_idx]) if freqs.size > 0 else None
        return {
            'fundamental_freq': fundamental,
            'frequencies': freqs.tolist(),
            'magnitudes': spectrum.tolist() }

    
    def _analyze_harmonics(self, waveform = None, sample_rate = None):
        fft_res = self._fft_analysis(waveform, sample_rate)
        fundamental = fft_res.get('fundamental_freq')
        harmonics = []
        if fundamental and fundamental > 0:
            for k in range(2, 11):
                freq = fundamental * k
                harmonics.append({
                    'harmonic': k,
                    'frequency': freq })
        return {
            'fundamental': fundamental,
            'harmonics': harmonics }

    
    def _export_csv_spectrum(self, freqs = None, mags = None):
        lines = [
            'frequency,amplitude']
        for f, m in zip(freqs, mags):
            lines.append(f"{f:.6f},{m:.6f}")
        return '\n'.join(lines)

    
    def run(self, config = None):
        if config is None:
            config = EngineConfig(engine_name=self.get_engine_name())
        (valid, errors) = self.validate(self.config)
        if not valid:
            return SkillResult.failure(skill_name = self.name, error = '; '.join(errors), data = {
                'stage': 'validation' })
        emt_api = None.create_emt_api(self.config.get('emt_config', { }))
        waveform = None
        sample_rate = 1000
        if hasattr(emt_api, 'run_short_simulation'):
            (waveform, sample_rate) = emt_api.run_short_simulation()
        elif hasattr(emt_api, 'run_simulation'):
            (waveform, sample_rate) = emt_api.run_simulation(short = True)
__all__ = [
    'HarmonicAnalysisSkill']
