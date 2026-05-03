from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import numpy as np

from cloudpss_skills_v2.core.skill_result import (
    Artifact,
    SkillResult,
    SkillStatus,
)
from cloudpss_skills_v2.poweranalysis.base import PowerAnalysis
from cloudpss_skills_v2.core.system_model import PowerSystemModel

logger = logging.getLogger(__name__)


class SmallSignalStabilityAnalysis(PowerAnalysis):
    """小信号稳定分析 - 特征值分析评估系统小扰动稳定性.

    This analysis uses the unified PowerSystemModel and calculates:
    - Eigenvalues for electromechanical modes
    - Damping ratios
    - Participation factors (optional)
    - Overall stability assessment
    """

    name = "small_signal_stability"
    description = "小信号稳定分析 - 特征值分析评估系统小扰动稳定性"

    @property
    def config_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "analysis_modes": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["eigenvalues", "damping_ratios", "participation_factors"],
                    },
                    "default": ["eigenvalues", "damping_ratios"],
                },
                "num_modes": {
                    "type": "integer",
                    "description": "Number of modes to analyze",
                    "default": 10,
                },
                "damping_threshold": {
                    "type": "number",
                    "description": "Damping ratio threshold for critical mode identification",
                    "default": 0.05,
                },
                "frequency_range": {
                    "type": "object",
                    "properties": {
                        "min_freq": {"type": "number", "default": 0.1},
                        "max_freq": {"type": "number", "default": 5.0},
                    },
                },
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        return {
            "analysis_modes": ["eigenvalues", "damping_ratios"],
            "num_modes": 10,
            "damping_threshold": 0.05,
            "frequency_range": {"min_freq": 0.1, "max_freq": 5.0},
        }

    def __init__(self):
        self.logs = []
        self.artifacts = []

    def _log(self, level: str, message: str) -> None:
        self.logs.append(
            {
                "timestamp": datetime.now().isoformat(),
                "level": level,
                "message": message,
            }
        )
        getattr(logger, level.lower(), logger.info)(message)

    def validate(self, config: dict | None) -> tuple[bool, list[str]]:
        """Legacy validation method for backward compatibility.

        Args:
            config: Configuration dictionary (legacy format)

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        if not config:
            errors.append("config is required")
            return (False, errors)
        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")
        matrix = config.get("state_matrix")
        if matrix is None:
            errors.append("state_matrix is required for small signal eigenvalue analysis")
        else:
            try:
                arr = np.asarray(matrix, dtype=float)
                if arr.ndim != 2 or arr.shape[0] != arr.shape[1] or arr.shape[0] == 0:
                    errors.append("state_matrix must be a non-empty square matrix")
            except (TypeError, ValueError):
                errors.append("state_matrix must be numeric")
        return (len(errors) == 0, errors)

    def _build_state_matrix(self, model: PowerSystemModel) -> np.ndarray:
        """Build state matrix for small signal stability analysis.

        This is a simplified state matrix construction for electromechanical modes.
        In a full implementation, this would use detailed generator models.

        Args:
            model: PowerSystemModel with generators and buses

        Returns:
            State matrix A for eigenvalue analysis
        """
        n_gens = len(model.generators)
        if n_gens == 0:
            return np.array([])

        # Simplified 2nd order model for each generator (swing equation)
        # State variables: [delta_1, omega_1, delta_2, omega_2, ...]
        # This creates a state matrix for the electromechanical dynamics

        n_states = 2 * n_gens
        A = np.zeros((n_states, n_states))

        # Typical values for simplified analysis
        damping_coeff = 0.5  # D coefficient
        inertia_const = 5.0  # H (inertia constant)

        for i in range(n_gens):
            # delta_dot = omega
            A[2 * i, 2 * i + 1] = 1.0

            # omega_dot = -(D/2H) * omega - (1/2H) * P_e
            # Simplified: just damping term
            A[2 * i + 1, 2 * i + 1] = -damping_coeff / (2 * inertia_const)

        # Add coupling terms based on network connectivity
        if len(model.branches) > 0 and n_gens >= 2:
            # Simplified coupling between generators
            coupling = 0.1 / (2 * inertia_const)
            for i in range(n_gens):
                for j in range(i + 1, n_gens):
                    if 2 * i + 1 < n_states and 2 * j < n_states:
                        A[2 * i + 1, 2 * j] = coupling
                        A[2 * j + 1, 2 * i] = coupling

        return A

    def _eigenvalue_analysis(
        self,
        A: np.ndarray,
        damping_threshold: float = 0.05,
        freq_range: tuple | None = None,
    ) -> dict:
        """Perform eigenvalue analysis on state matrix.

        Args:
            A: State matrix
            damping_threshold: Threshold for identifying critical modes
            freq_range: Optional (min_freq, max_freq) tuple to filter modes

        Returns:
            Dictionary with eigenvalues, modes, and stability assessment
        """
        if A.size == 0:
            return {
                "stable": False,
                "eigenvalues": np.array([]),
                "damping_ratios": np.array([]),
                "modes": [],
                "critical_modes": [],
            }

        try:
            eigenvalues = np.linalg.eigvals(A)
        except np.linalg.LinAlgError:
            eigenvalues = np.array([])

        modes = []
        damping_ratios = []

        for i, e in enumerate(eigenvalues):
            # Calculate frequency in Hz
            freq = abs(e.imag) / (2 * np.pi)

            # Calculate damping ratio
            if abs(e) > 1e-10:
                damping = -e.real / abs(e)
            else:
                damping = 1.0

            damping_ratios.append(damping)

            mode_info = {
                "index": i,
                "eigenvalue": complex(e),
                "real_part": e.real,
                "imaginary_part": e.imag,
                "frequency_hz": freq,
                "damping_ratio": damping,
                "period_s": 1.0 / freq if freq > 1e-10 else None,
            }

            # Filter by frequency range if specified
            if freq_range is not None:
                min_freq, max_freq = freq_range
                if min_freq <= freq <= max_freq:
                    modes.append(mode_info)
            else:
                modes.append(mode_info)

        # Identify critical modes (low damping)
        critical_modes = [m for m in modes if m["damping_ratio"] < damping_threshold]

        # Determine stability: all eigenvalues must have negative real parts
        stable = all(e.real < 0 for e in eigenvalues if abs(e) > 1e-10)

        return {
            "stable": stable,
            "eigenvalues": eigenvalues,
            "damping_ratios": np.array(damping_ratios),
            "modes": modes,
            "critical_modes": critical_modes,
            "total_modes": len(modes),
            "critical_count": len(critical_modes),
        }

    def _calculate_participation_factors(
        self, A: np.ndarray, eigenvalues: np.ndarray, num_modes: int = 10
    ) -> dict:
        """Calculate participation factors for state variables.

        Participation factors indicate which states contribute most to each mode.

        Args:
            A: State matrix
            eigenvalues: Eigenvalues of A
            num_modes: Number of modes to analyze

        Returns:
            Dictionary with participation factor matrix
        """
        if A.size == 0 or len(eigenvalues) == 0:
            return {"participation_factors": None}

        try:
            # Compute eigenvectors
            eigenvalues_full, right_eigenvectors = np.linalg.eig(A)
            _, left_eigenvectors = np.linalg.eig(A.T)

            n_states = A.shape[0]
            n_modes = min(num_modes, len(eigenvalues_full))

            # Calculate participation factors
            # p_ki = |v_ki * u_ki| where v is right eigenvector, u is left eigenvector
            participation_matrix = np.zeros((n_states, n_modes))

            for i in range(n_modes):
                for k in range(n_states):
                    v_ki = right_eigenvectors[k, i]
                    u_ki = left_eigenvectors[k, i]
                    participation_matrix[k, i] = abs(v_ki * u_ki)

            # Normalize each column (mode) to sum to 1
            for i in range(n_modes):
                col_sum = np.sum(participation_matrix[:, i])
                if col_sum > 0:
                    participation_matrix[:, i] /= col_sum

            return {
                "participation_factors": participation_matrix,
                "dominant_states": np.argmax(participation_matrix, axis=0).tolist(),
            }
        except Exception as e:
            self._log("WARNING", f"Failed to calculate participation factors: {e}")
            return {"participation_factors": None}

    def run(self, model: PowerSystemModel | dict, config: dict | None = None) -> dict | SkillResult:
        """Run small signal stability analysis on unified model.

        This method supports both the new unified PowerSystemModel interface and
        the legacy config dict interface for backward compatibility.

        Args:
            model: Either a unified PowerSystemModel or a legacy config dict
            config: Analysis configuration dictionary (only used with PowerSystemModel)

        Returns:
            Dictionary with analysis results (for PowerSystemModel) or
            SkillResult (for legacy config dict)
        """
        # Detect input type and route appropriately
        if isinstance(model, dict):
            # Legacy config-based interface
            return self._run_legacy_config(model)

        # New unified PowerSystemModel interface
        return self._run_unified_model(model, config)

    def _run_unified_model(self, model: PowerSystemModel, config: dict | None = None) -> dict:
        """Run analysis on unified PowerSystemModel.

        Args:
            model: Unified PowerSystemModel containing buses, generators, etc.
            config: Analysis configuration dictionary with optional keys:
                - analysis_modes: List of analysis modes to perform
                - num_modes: Number of modes to analyze
                - damping_threshold: Damping ratio threshold for critical modes
                - frequency_range: Dict with min_freq and max_freq

        Returns:
            Dictionary with analysis results:
                - status: "success" or "error"
                - stable: Boolean indicating overall stability
                - eigenvalues: Array of eigenvalues
                - damping_ratios: Array of damping ratios
                - modes: List of mode information dictionaries
                - critical_modes: List of critical modes (low damping)
                - participation_factors: (optional) Participation factor matrix
        """
        if config is None:
            config = {}

        self.logs = []
        self.artifacts = []

        # Validate model
        errors = self.validate_model(model)
        if errors:
            error_msg = "; ".join(errors)
            self._log("ERROR", f"Model validation failed: {error_msg}")
            return {
                "status": "error",
                "message": f"Validation failed: {error_msg}",
                "logs": self.logs,
            }

        try:
            # Get configuration
            analysis_modes = config.get("analysis_modes", ["eigenvalues", "damping_ratios"])
            num_modes = config.get("num_modes", 10)
            damping_threshold = config.get("damping_threshold", 0.05)
            freq_range_config = config.get("frequency_range", {})
            min_freq = freq_range_config.get("min_freq", 0.1)
            max_freq = freq_range_config.get("max_freq", 5.0)

            self._log("INFO", f"Starting small signal stability analysis")
            self._log("INFO", f"Model: {len(model.buses)} buses, {len(model.generators)} generators")
            self._log("INFO", f"Analysis modes: {analysis_modes}")

            # Build state matrix
            state_matrix = self._build_state_matrix(model)

            if state_matrix.size == 0:
                self._log("WARNING", "No state matrix could be built (no generators)")
                return {
                    "status": "error",
                    "message": "No generators in model - cannot perform stability analysis",
                    "logs": self.logs,
                }

            self._log("INFO", f"State matrix shape: {state_matrix.shape}")

            # Perform eigenvalue analysis
            eigen_results = self._eigenvalue_analysis(
                state_matrix,
                damping_threshold=damping_threshold,
                freq_range=(min_freq, max_freq),
            )

            # Build result dictionary
            result = {
                "status": "success",
                "stable": eigen_results["stable"],
                "eigenvalues": eigen_results["eigenvalues"],
                "damping_ratios": eigen_results["damping_ratios"],
                "modes": eigen_results["modes"],
                "critical_modes": eigen_results["critical_modes"],
                "total_modes": eigen_results["total_modes"],
                "critical_count": eigen_results["critical_count"],
                "damping_threshold": damping_threshold,
                "logs": self.logs,
            }

            # Calculate participation factors if requested
            if "participation_factors" in analysis_modes:
                self._log("INFO", "Calculating participation factors")
                pf_results = self._calculate_participation_factors(
                    state_matrix, eigen_results["eigenvalues"], num_modes
                )
                result["participation_factors"] = pf_results.get("participation_factors")
                result["dominant_states"] = pf_results.get("dominant_states")

            status_str = "stable" if eigen_results["stable"] else "unstable"
            self._log(
                "INFO",
                f"Analysis complete: {status_str}, "
                f"{eigen_results['critical_count']} critical modes",
            )

            return result

        except Exception as e:
            self._log("ERROR", f"Small signal stability analysis failed: {e}")
            return {
                "status": "error",
                "message": str(e),
                "logs": self.logs,
            }

    def _run_legacy_config(self, config: dict | None) -> SkillResult:
        """Internal: Run analysis with legacy config-based interface.

        This method is used internally by run() when a dict is passed.
        It provides backward compatibility with existing code.

        Args:
            config: Configuration dictionary (legacy format)

        Returns:
            SkillResult object
        """
        from cloudpss_skills_v2.powerskill import Engine

        start_time = datetime.now()
        if config is None:
            config = {}
        self.logs = []
        self.artifacts = []

        # Validate config for legacy mode
        errors = []
        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")
        matrix = config.get("state_matrix")
        if matrix is None:
            errors.append("state_matrix is required for small signal eigenvalue analysis")
        else:
            try:
                arr = np.asarray(matrix, dtype=float)
                if arr.ndim != 2 or arr.shape[0] != arr.shape[1] or arr.shape[0] == 0:
                    errors.append("state_matrix must be a non-empty square matrix")
            except (TypeError, ValueError):
                errors.append("state_matrix must be numeric")

        if errors:
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error="; ".join(errors),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )

        try:
            engine = config.get("engine", "pandapower")
            api = Engine.create_powerflow(engine=engine)
            self._log("INFO", f"Using engine: {api.adapter.engine_name}")

            model_rid = config["model"]["rid"]
            self._log("INFO", f"Model: {model_rid}")

            analysis_config = config.get("analysis", {})
            damping_threshold = analysis_config.get("damping_threshold", 0.05)

            handle = api.get_model_handle(model_rid)
            result = api.run_power_flow(model_handle=handle)

            state_matrix = np.asarray(config["state_matrix"], dtype=float)
            eigen_results = self._eigenvalue_analysis(state_matrix, damping_threshold)

            result_data = {
                "converged": result.is_success,
                "stable": eigen_results.get("stable", False),
                "damping_threshold": damping_threshold,
                "total_modes": eigen_results.get("total_modes", 0),
                "critical_count": eigen_results.get("critical_count", 0),
                "modes": eigen_results.get("modes", []),
                "critical_modes": eigen_results.get("critical_modes", []),
                "data_source": "state_matrix",
            }

            status = "stable" if eigen_results.get("stable") else "unstable"
            self._log(
                "INFO",
                f"Small signal stability complete: {status}, {eigen_results.get('critical_count', 0)} critical modes",
            )

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                data=result_data,
                logs=self.logs,
                artifacts=self.artifacts,
                start_time=start_time,
                end_time=datetime.now(),
            )

        except Exception as e:
            self._log("ERROR", f"Small signal stability analysis failed: {e}")
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error=str(e),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now(),
            )


__all__ = ["SmallSignalStabilityAnalysis"]
