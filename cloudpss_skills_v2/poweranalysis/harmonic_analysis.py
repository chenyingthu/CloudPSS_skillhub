from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

from cloudpss_skills_v2.core import Artifact, LogEntry, SkillResult, SkillStatus
from cloudpss_skills_v2.powerskill import Engine


class HarmonicAnalysisAnalysis:
    """Harmonic analysis using FFT on waveform data."""

    name = "harmonic_analysis"
    description = "Harmonic analysis using FFT on EMT waveform data"

    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []

    def get_default_config(self) -> dict[str, Any]:
        return {
            "skill": self.name,
            "waveform": {"values": [], "sample_rate": 1000},
            "output": {"format": "json", "path": "./results/", "prefix": self.name},
        }

    def validate(self, config=None):
        errors = []
        if not isinstance(config, dict):
            errors.append("config is required")
            return False, errors
        waveform = config.get("waveform", {})
        has_values = bool(waveform.get("values"))
        has_model = bool(config.get("model", {}).get("rid"))
        if not has_values and not has_model:
            errors.append("waveform.values or model.rid is required")
        sample_rate = waveform.get("sample_rate", config.get("sample_rate", 1000))
        try:
            if float(sample_rate) <= 0:
                errors.append("sample_rate must be positive")
        except (TypeError, ValueError):
            errors.append("sample_rate must be numeric")
        return len(errors) == 0, errors

    def _log(self, level: str, message: str) -> None:
        self.logs.append(LogEntry(timestamp=datetime.now(), level=level, message=message))

    def _fft_analysis(self, waveform=None, sample_rate=None):
        arr = np.asarray(waveform or [], dtype=float)
        if arr.size == 0:
            return {"fundamental_freq": None, "frequencies": [], "magnitudes": []}
        rate = float(sample_rate or 1000)
        arr = arr - float(np.mean(arr))
        n = arr.size
        freqs = np.fft.rfftfreq(n, d=1 / rate)
        spectrum = np.abs(np.fft.rfft(arr)) / n
        if spectrum.size > 1:
            max_idx = int(np.argmax(spectrum[1:]) + 1)
        else:
            max_idx = 0
        fundamental = float(freqs[max_idx]) if freqs.size > 0 else None
        return {
            "fundamental_freq": fundamental,
            "frequencies": freqs.tolist(),
            "magnitudes": spectrum.tolist(),
        }

    def _analyze_harmonics(self, waveform=None, sample_rate=None):
        fft_res = self._fft_analysis(waveform, sample_rate)
        fundamental = fft_res.get("fundamental_freq")
        freqs = np.asarray(fft_res.get("frequencies", []), dtype=float)
        mags = np.asarray(fft_res.get("magnitudes", []), dtype=float)
        harmonics = []
        if fundamental and fundamental > 0 and freqs.size and mags.size:
            fundamental_mag = float(mags[np.argmin(np.abs(freqs - fundamental))]) or 1.0
            for order in range(2, 11):
                target = fundamental * order
                idx = int(np.argmin(np.abs(freqs - target)))
                harmonics.append(
                    {
                        "harmonic": order,
                        "frequency": float(freqs[idx]),
                        "magnitude": float(mags[idx]),
                        "percent_of_fundamental": float(mags[idx] / fundamental_mag * 100),
                    }
                )
        return {"fundamental": fundamental, "harmonics": harmonics, "spectrum": fft_res}

    def _export_csv_spectrum(self, freqs=None, mags=None):
        lines = ["frequency,amplitude"]
        for freq, mag in zip(freqs or [], mags or []):
            lines.append(f"{float(freq):.6f},{float(mag):.6f}")
        return "\n".join(lines)

    def _waveform_from_emt(self, config: dict[str, Any]) -> tuple[list[float], float]:
        model = config.get("model", {})
        auth = config.get("auth", {})
        api = Engine.create_emt_for_skill(
            engine=config.get("engine", "cloudpss"),
            base_url=auth.get("base_url"),
            auth=auth,
        )
        sim = config.get("simulation", {})
        result = api.run_emt(
            model_id=model["rid"],
            duration=sim.get("duration"),
            step_size=sim.get("step_size"),
            timeout=sim.get("timeout", 300),
            sampling_freq=sim.get("sampling_freq", 1000),
            source=model.get("source", "cloud"),
            auth=auth,
        )
        if not result.is_success:
            raise RuntimeError(result.errors[0] if result.errors else "EMT simulation failed")
        plots = result.data.get("plots", [])
        for plot in plots:
            channel_data = plot.get("channel_data", {})
            for trace in channel_data.values():
                values = trace.get("y") if isinstance(trace, dict) else trace
                if values:
                    return list(values), float(sim.get("sampling_freq", 1000))
        raise RuntimeError("No waveform channel data found in EMT result")

    def run(self, config=None):
        start_time = datetime.now()
        self.logs = []
        self.artifacts = []
        config = config or {}
        valid, errors = self.validate(config)
        if not valid:
            return SkillResult.failure(self.name, "; ".join(errors), {"stage": "validation"})

        try:
            waveform_cfg = config.get("waveform", {})
            waveform = waveform_cfg.get("values")
            sample_rate = waveform_cfg.get("sample_rate", config.get("sample_rate", 1000))
            if not waveform:
                waveform, sample_rate = self._waveform_from_emt(config)

            analysis = self._analyze_harmonics(waveform, sample_rate)
            spectrum = analysis["spectrum"]
            result_data = {
                "sample_rate": sample_rate,
                "sample_count": len(waveform),
                "fundamental_freq": analysis["fundamental"],
                "harmonics": analysis["harmonics"],
                "spectrum": spectrum,
            }
            self._save_output(result_data, config.get("output", {}))
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data=result_data,
                artifacts=self.artifacts,
                logs=self.logs,
                metrics={"harmonic_count": len(analysis["harmonics"])},
                start_time=start_time,
                end_time=datetime.now(),
            )
        except Exception as exc:
            self._log("error", str(exc))
            return SkillResult.failure(self.name, str(exc), {"stage": "harmonic_analysis"})

    def _save_output(self, result_data: dict[str, Any], output_config: dict[str, Any]) -> None:
        if not output_config:
            return
        output_path = Path(output_config.get("path", "./results/"))
        output_path.mkdir(parents=True, exist_ok=True)
        prefix = output_config.get("prefix", self.name)
        output_format = output_config.get("format", "json")
        filepath = output_path / f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{output_format}"
        if output_format == "csv":
            with filepath.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["frequency", "amplitude"])
                for freq, mag in zip(
                    result_data["spectrum"]["frequencies"],
                    result_data["spectrum"]["magnitudes"],
                ):
                    writer.writerow([freq, mag])
        else:
            import json

            filepath.write_text(
                json.dumps(result_data, indent=2, ensure_ascii=False, default=str),
                encoding="utf-8",
            )
        self.artifacts.append(
            Artifact(
                name=filepath.name,
                path=str(filepath),
                type=output_format,
                size_bytes=filepath.stat().st_size,
                description="Harmonic analysis result",
            )
        )


__all__ = ["HarmonicAnalysisAnalysis"]
