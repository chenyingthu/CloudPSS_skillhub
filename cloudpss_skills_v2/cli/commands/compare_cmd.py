"""Compare Command - Cross-engine comparison CLI command.

跨引擎比较命令 - 用于比较不同仿真引擎的分析结果。
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime
from typing import Any

from cloudpss_skills_v2.powerapi.base import SimulationResult, SimulationStatus
from cloudpss_skills_v2.powerapi.registry import registry

logger = logging.getLogger(__name__)


def print_error(message: str) -> None:
    """Print error message."""
    print(f"[ERROR] {message}", file=sys.stderr)


def print_success(message: str) -> None:
    """Print success message."""
    print(f"[OK] {message}")


def print_info(message: str) -> None:
    """Print info message."""
    print(f"[INFO] {message}")


def print_warning(message: str) -> None:
    """Print warning message."""
    print(f"[WARN] {message}")


def print_header(title: str) -> None:
    """Print section header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def print_subheader(title: str) -> None:
    """Print subsection header."""
    print(f"\n{'-' * 60}")
    print(f"  {title}")
    print(f"{'-' * 60}")


class EngineComparator:
    """Compare analysis results across multiple engines."""

    def __init__(self, engines: list[str], model_id: str, analysis_type: str):
        self.engines = engines
        self.model_id = model_id
        self.analysis_type = analysis_type
        self.results: dict[str, SimulationResult] = {}
        self.errors: dict[str, str] = {}

    def run_comparison(self) -> dict[str, Any]:
        """Run analysis on all engines and collect results."""
        print_header(f"Cross-Engine Comparison: {self.analysis_type}")
        print_info(f"Model: {self.model_id}")
        print_info(f"Engines: {', '.join(self.engines)}")

        for engine in self.engines:
            print_subheader(f"Running on {engine}")
            result = self._run_single_engine(engine)
            if result:
                self.results[engine] = result
            print()

        return self._generate_comparison_report()

    def _run_single_engine(self, engine_name: str) -> SimulationResult | None:
        """Run analysis on a single engine."""
        adapter_cls = registry.get(engine_name, self.analysis_type)

        if not adapter_cls:
            error_msg = f"Engine '{engine_name}' does not support '{self.analysis_type}'"
            print_error(error_msg)
            self.errors[engine_name] = error_msg
            return None

        try:
            adapter = adapter_cls()
            print_info(f"Connecting to {engine_name}...")
            adapter.connect()

            print_info(f"Loading model: {self.model_id}...")
            if not adapter.load_model(self.model_id):
                error_msg = f"Failed to load model on {engine_name}"
                print_error(error_msg)
                self.errors[engine_name] = error_msg
                adapter.disconnect()
                return None

            config = {"analysis_type": self.analysis_type, "model_id": self.model_id}
            print_info(f"Running {self.analysis_type} analysis...")
            result = adapter.run_simulation(config)

            adapter.disconnect()

            if result.status == SimulationStatus.COMPLETED:
                print_success(f"Analysis completed on {engine_name}")
                print_info(f"  Duration: {result.duration_seconds:.2f}s" if result.duration_seconds else "  Duration: N/A")
                return result
            else:
                error_msg = f"Analysis failed on {engine_name}: {', '.join(result.errors)}"
                print_error(error_msg)
                self.errors[engine_name] = error_msg
                return result

        except Exception as e:
            error_msg = f"Exception on {engine_name}: {e}"
            print_error(error_msg)
            self.errors[engine_name] = str(e)
            return None

    def _generate_comparison_report(self) -> dict[str, Any]:
        """Generate comparison report from results."""
        print_header("Comparison Summary")

        report = {
            "model_id": self.model_id,
            "analysis_type": self.analysis_type,
            "engines": self.engines,
            "timestamp": datetime.now().isoformat(),
            "engine_results": {},
            "comparison": {},
            "status_summary": {},
        }

        # Status summary
        success_count = sum(
            1 for r in self.results.values()
            if r and r.status == SimulationStatus.COMPLETED
        )
        failed_count = len(self.engines) - success_count

        print_info(f"Total engines: {len(self.engines)}")
        print_success(f"Successful: {success_count}")
        if failed_count > 0:
            print_error(f"Failed: {failed_count}")

        report["status_summary"] = {
            "total": len(self.engines),
            "success": success_count,
            "failed": failed_count,
        }

        # Per-engine results
        print_subheader("Engine Status")
        for engine in self.engines:
            result = self.results.get(engine)
            if result:
                status_str = "✓ SUCCESS" if result.status == SimulationStatus.COMPLETED else "✗ FAILED"
                print(f"  {engine:15} {status_str}")
                if result.duration_seconds:
                    print(f"    Duration: {result.duration_seconds:.2f}s")

                report["engine_results"][engine] = {
                    "status": result.status.value if result.status else "unknown",
                    "duration_seconds": result.duration_seconds,
                    "errors": result.errors,
                    "warnings": result.warnings,
                }
            else:
                print(f"  {engine:15} ✗ ERROR: {self.errors.get(engine, 'Unknown error')}")
                report["engine_results"][engine] = {
                    "status": "error",
                    "error": self.errors.get(engine, "Unknown error"),
                }

        # Data comparison (if multiple successful results)
        successful_results = {
            name: result for name, result in self.results.items()
            if result and result.status == SimulationStatus.COMPLETED
        }

        if len(successful_results) >= 2:
            print_subheader("Data Comparison")
            comparison = self._compare_data(successful_results)
            report["comparison"] = comparison

            if comparison.get("differences"):
                print_warning(f"Found {len(comparison['differences'])} differences:")
                for diff in comparison["differences"]:
                    print(f"  - {diff}")
            else:
                print_success("No significant differences found")
        elif len(successful_results) == 1:
            print_info("Only one engine succeeded - comparison not possible")
        else:
            print_error("No engines succeeded - comparison not possible")

        return report

    def _compare_data(self, results: dict[str, SimulationResult]) -> dict[str, Any]:
        """Compare data across successful results."""
        comparison = {
            "engines_compared": list(results.keys()),
            "differences": [],
            "common_keys": [],
            "engine_specific_keys": {},
        }

        # Collect all data keys
        all_keys: set[str] = set()
        engine_keys: dict[str, set[str]] = {}

        for engine, result in results.items():
            keys = set(result.data.keys()) if result.data else set()
            engine_keys[engine] = keys
            all_keys.update(keys)

        # Find common and specific keys
        if all_keys:
            common = all_keys.copy()
            for keys in engine_keys.values():
                common &= keys

            comparison["common_keys"] = sorted(common)

            for engine, keys in engine_keys.items():
                specific = keys - common
                if specific:
                    comparison["engine_specific_keys"][engine] = sorted(specific)

        # Compare common values (simple comparison)
        for key in comparison["common_keys"]:
            values = {}
            for engine, result in results.items():
                values[engine] = result.data.get(key)

            # Check if all values are equal
            unique_values = set(str(v) for v in values.values())
            if len(unique_values) > 1:
                comparison["differences"].append({
                    "key": key,
                    "values": values,
                    "type": "value_mismatch",
                })

        return comparison


def execute(args: argparse.Namespace) -> int:
    """Execute the compare command.

    Args:
        args: Command line arguments

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    # Parse engines from comma-separated list
    engines = [e.strip() for e in args.engines.split(",")]

    if len(engines) < 2:
        print_error("At least 2 engines required for comparison")
        return 1

    model_id = args.model
    analysis_type = args.analysis

    # Validate analysis type
    valid_analysis_types = ["power_flow", "emt", "short_circuit", "harmonic", "dynamic"]
    if analysis_type not in valid_analysis_types:
        print_error(f"Invalid analysis type: {analysis_type}")
        print_info(f"Valid types: {', '.join(valid_analysis_types)}")
        return 1

    # Run comparison
    comparator = EngineComparator(engines, model_id, analysis_type)
    report = comparator.run_comparison()

    # Output to file if specified
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print_success(f"Report saved to: {args.output}")
        except Exception as e:
            print_error(f"Failed to save report: {e}")

    # Return exit code based on success
    success_count = report["status_summary"].get("success", 0)
    if success_count == 0:
        return 2  # All failed
    elif success_count < len(engines):
        return 1  # Partial success
    return 0  # All succeeded


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add the compare command parser to subparsers."""
    compare_parser = subparsers.add_parser(
        "compare",
        help="Compare analysis results across multiple engines",
        description="Run the same analysis on multiple engines and compare results.",
    )

    compare_parser.add_argument(
        "--engines", "-e",
        required=True,
        help="Comma-separated list of engines to compare (e.g., 'cloudpss,pandapower')",
    )

    compare_parser.add_argument(
        "--model", "-m",
        required=True,
        help="Model ID to analyze",
    )

    compare_parser.add_argument(
        "--analysis", "-a",
        required=True,
        choices=["power_flow", "emt", "short_circuit", "harmonic", "dynamic"],
        help="Type of analysis to run",
    )

    compare_parser.add_argument(
        "--output", "-o",
        help="Output file path for JSON report",
    )

    compare_parser.set_defaults(func=execute)


__all__ = ["execute", "add_parser", "EngineComparator"]
