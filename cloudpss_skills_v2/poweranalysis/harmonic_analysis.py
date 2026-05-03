from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

from cloudpss_skills_v2.core import Artifact, LogEntry, SkillResult, SkillStatus
from cloudpss_skills_v2.powerskill import Engine


# =============================================================================
# Legacy Harmonic Analysis (kept for backward compatibility)
# =============================================================================

class HarmonicAnalysisAnalysis:
    """Harmonic analysis using FFT on waveform data."""

    name = "harmonic_analysis"
    description = "Harmonic analysis using FFT on EMT waveform data"

    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "skill": {"type": "string", "const": "harmonic_analysis", "default": "harmonic_analysis"},
                "waveform": {
                    "type": "object",
                    "properties": {
                        "values": {"type": "array", "items": {"type": "number"}, "default": []},
                        "sample_rate": {"type": "number", "default": 1000},
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "prefix": {"type": "string", "default": "harmonic_analysis"},
                    },
                },
            },
        }

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


# =============================================================================
# Unified Model Harmonic Analysis
# =============================================================================

from cloudpss_skills_v2.core.system_model import PowerSystemModel
from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis


class HarmonicAnalysis(PowerAnalysis):
    """Harmonic analysis using unified PowerSystemModel.

    This class performs harmonic power flow analysis on a power system model,
    calculating harmonic voltages at each bus and total harmonic distortion (THD).

    The analysis:
    1. Builds harmonic admittance (Ybus) matrix for each harmonic order
    2. Injects harmonic current sources at specified buses
    3. Solves for harmonic voltages: V_h = Ybus_h^-1 * I_h
    4. Calculates THD at each bus

    Example:
        model = PowerSystemModel(buses=[...], branches=[...])
        analysis = HarmonicAnalysis()
        result = analysis.run(model, {
            "harmonic_orders": [3, 5, 7],
            "sources": [{"bus": "Bus2", "order": 5, "magnitude": 0.05}]
        })
    """

    name = "harmonic_analysis_unified"
    description = "Harmonic analysis using unified PowerSystemModel"

    def __init__(self):
        self._harmonic_voltages: dict[int, dict[str, complex]] = {}
        self._thd: dict[str, float] = {}

    def run(self, model: PowerSystemModel, config: dict) -> dict:
        """Run harmonic analysis on unified model.

        Args:
            model: Unified PowerSystemModel containing buses, branches, etc.
            config: Analysis configuration with keys:
                - harmonic_orders: List of harmonic orders to analyze (e.g., [3, 5, 7])
                - sources: List of harmonic sources, each with:
                    - bus: Bus name where source is connected
                    - order: Harmonic order of the source
                    - magnitude: Current magnitude in per unit

        Returns:
            Dictionary containing:
                - status: "success" or "error"
                - harmonic_voltages: Dict mapping harmonic order to bus voltages
                - thd: Dict mapping bus name to THD percentage
                - harmonic_orders: List of analyzed harmonic orders
        """
        # Validate model
        errors = self.validate_model(model)
        if errors:
            return {
                "status": "error",
                "error": "; ".join(errors)
            }

        # Get configuration
        harmonic_orders = config.get("harmonic_orders", [3, 5, 7])
        sources = config.get("sources", [])

        # Initialize results
        self._harmonic_voltages = {}
        self._thd = {}

        # Calculate harmonic voltages for each order
        for h in harmonic_orders:
            voltages = self._calculate_harmonic_voltages(model, h, sources)
            self._harmonic_voltages[h] = voltages

        # Calculate THD for each bus
        self._thd = self._calculate_all_thd(model)

        return {
            "status": "success",
            "harmonic_voltages": self._harmonic_voltages,
            "thd": self._thd,
            "harmonic_orders": harmonic_orders,
        }

    def _calculate_harmonic_voltages(
        self,
        model: PowerSystemModel,
        harmonic_order: int,
        sources: list[dict],
    ) -> dict[str, complex]:
        """Calculate harmonic voltages for a specific harmonic order.

        Args:
            model: PowerSystemModel
            harmonic_order: Harmonic order h (e.g., 3 for 3rd harmonic)
            sources: List of harmonic sources

        Returns:
            Dictionary mapping bus name to complex harmonic voltage (p.u.)
        """
        n_buses = len(model.buses)
        if n_buses == 0:
            return {}

        # Build harmonic admittance matrix
        ybus = self._build_harmonic_ybus(model, harmonic_order)

        # Build current injection vector
        i_inj = self._build_current_injection(model, harmonic_order, sources)

        # Solve for harmonic voltages: V = Y^-1 * I
        try:
            # Handle slack bus - set voltage to 0 for harmonics at slack
            slack_bus = model.get_slack_bus()
            if slack_bus:
                slack_idx = self._get_bus_index(model, slack_bus.name)
                if slack_idx is not None:
                    # Modify Ybus to ground the slack bus for harmonics
                    ybus_modified = ybus.copy()
                    ybus_modified[slack_idx, :] = 0
                    ybus_modified[:, slack_idx] = 0
                    ybus_modified[slack_idx, slack_idx] = 1.0
                    i_inj[slack_idx] = 0.0

                    v_harmonic = np.linalg.solve(ybus_modified, i_inj)
                else:
                    v_harmonic = np.linalg.solve(ybus, i_inj)
            else:
                # Use pseudo-inverse if Ybus is singular
                try:
                    v_harmonic = np.linalg.solve(ybus, i_inj)
                except np.linalg.LinAlgError:
                    v_harmonic = np.linalg.lstsq(ybus, i_inj, rcond=None)[0]
        except np.linalg.LinAlgError:
            # Singular matrix - return zero voltages
            v_harmonic = np.zeros(n_buses, dtype=complex)

        # Map back to bus names
        bus_names = [bus.name for bus in model.buses]
        return {name: complex(v) for name, v in zip(bus_names, v_harmonic)}

    def _build_harmonic_ybus(
        self,
        model: PowerSystemModel,
        harmonic_order: int,
    ) -> np.ndarray:
        """Build harmonic admittance matrix (Ybus) for a given harmonic order.

        At harmonic order h:
        - Resistance R stays the same
        - Reactance X becomes h * X (inductive reactance increases with frequency)
        - Susceptance B becomes B / h (capacitive susceptance decreases with frequency)

        Args:
            model: PowerSystemModel
            harmonic_order: Harmonic order h

        Returns:
            Complex admittance matrix Ybus (n_buses x n_buses)
        """
        n_buses = len(model.buses)
        ybus = np.zeros((n_buses, n_buses), dtype=complex)

        # Build bus index mapping
        bus_idx = {bus.bus_id: i for i, bus in enumerate(model.buses)}

        for branch in model.branches:
            if not branch.in_service:
                continue

            from_idx = bus_idx.get(branch.from_bus)
            to_idx = bus_idx.get(branch.to_bus)

            if from_idx is None or to_idx is None:
                continue

            # Get branch parameters
            r = branch.r_pu
            x = branch.x_pu
            b = branch.b_pu

            # Scale for harmonic order
            # Z_h = R + j * h * X (inductive reactance increases with frequency)
            # B_h = B / h (capacitive susceptance decreases with frequency)
            x_h = harmonic_order * x
            b_h = b / harmonic_order if harmonic_order > 0 else 0

            # Series admittance
            if r != 0 or x_h != 0:
                y_series = 1.0 / complex(r, x_h)
            else:
                y_series = 0

            # Shunt admittance (half at each end for transmission lines)
            y_shunt = complex(0, b_h / 2) if b_h != 0 else 0

            # Add to Ybus
            ybus[from_idx, from_idx] += y_series + y_shunt
            ybus[to_idx, to_idx] += y_series + y_shunt
            ybus[from_idx, to_idx] -= y_series
            ybus[to_idx, from_idx] -= y_series

        return ybus

    def _build_current_injection(
        self,
        model: PowerSystemModel,
        harmonic_order: int,
        sources: list[dict],
    ) -> np.ndarray:
        """Build current injection vector for harmonic analysis.

        Args:
            model: PowerSystemModel
            harmonic_order: Harmonic order h
            sources: List of harmonic sources

        Returns:
            Current injection vector (n_buses,)
        """
        n_buses = len(model.buses)
        i_inj = np.zeros(n_buses, dtype=complex)

        # Map bus names to indices
        bus_name_to_idx = {bus.name: i for i, bus in enumerate(model.buses)}

        for source in sources:
            if source.get("order") != harmonic_order:
                continue

            bus_name = source.get("bus", "")
            magnitude = source.get("magnitude", 0.0)

            if bus_name in bus_name_to_idx:
                idx = bus_name_to_idx[bus_name]
                # Inject current (assume zero phase angle for simplicity)
                i_inj[idx] = magnitude * complex(1, 0)

        return i_inj

    def _get_bus_index(self, model: PowerSystemModel, bus_name: str) -> int | None:
        """Get array index for a bus by name."""
        for i, bus in enumerate(model.buses):
            if bus.name == bus_name:
                return i
        return None

    def _calculate_all_thd(self, model: PowerSystemModel) -> dict[str, float]:
        """Calculate THD for all buses.

        THD = sqrt(sum(V_h^2 for h > 1)) / V_1 * 100%

        Args:
            model: PowerSystemModel

        Returns:
            Dictionary mapping bus name to THD percentage
        """
        thd = {}

        for bus in model.buses:
            # Collect harmonic voltages for this bus
            bus_voltages = {}
            for h, voltages in self._harmonic_voltages.items():
                if bus.name in voltages:
                    bus_voltages[h] = abs(voltages[bus.name])

            # Calculate THD
            thd[bus.name] = self._calculate_thd(bus_voltages)

        return thd

    def _calculate_thd(self, harmonic_voltages: dict[int, float]) -> float:
        """Calculate Total Harmonic Distortion from harmonic voltages.

        THD = sqrt(sum(V_h^2 for h > 1)) / V_1 * 100%

        Args:
            harmonic_voltages: Dict mapping harmonic order to voltage magnitude (p.u.)

        Returns:
            THD as percentage
        """
        if not harmonic_voltages or 1 not in harmonic_voltages:
            # No fundamental - assume fundamental is 1.0 p.u.
            fundamental = 1.0
        else:
            fundamental = harmonic_voltages[1]

        if fundamental == 0:
            return 0.0

        # Sum of squares of harmonic voltages (excluding fundamental)
        harmonic_sum_sq = sum(
            v**2 for h, v in harmonic_voltages.items() if h != 1
        )

        thd = np.sqrt(harmonic_sum_sq) / fundamental * 100.0
        return float(thd)


__all__ = ["HarmonicAnalysisAnalysis", "HarmonicAnalysis"]
