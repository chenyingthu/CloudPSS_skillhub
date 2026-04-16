#!/usr/bin/env python3
"""批量修复失败路径的 data 填充"""

import re
from pathlib import Path

BUILTIN_DIR = Path(__file__).parent.parent / "cloudpss_skills" / "builtin"

STAGE_MAP = {
    "power_flow": "power_flow",
    "emt_simulation": "emt_simulation",
    "n1_security": "n1_security",
    "n2_security": "n2_security",
    "voltage_stability": "voltage_stability",
    "transient_stability": "transient_stability",
    "batch_powerflow": "batch_powerflow",
    "loss_analysis": "loss_analysis",
    "harmonic_analysis": "harmonic_analysis",
    "short_circuit": "short_circuit",
    "param_scan": "param_scan",
    "parameter_sensitivity": "parameter_sensitivity",
    "orthogonal_sensitivity": "orthogonal_sensitivity",
    "model_hub": "model_hub",
    "model_builder": "model_builder",
    "model_validator": "model_validator",
    "model_parameter_extractor": "model_parameter_extractor",
    "component_catalog": "component_catalog",
    "topology_check": "topology_check",
    "thevenin_equivalent": "thevenin_equivalent",
    "auto_channel_setup": "auto_channel_setup",
    "auto_loop_breaker": "auto_loop_breaker",
    "batch_task_manager": "batch_task_manager",
    "config_batch_runner": "config_batch_runner",
    "comtrade_export": "comtrade_export",
    "hdf5_export": "hdf5_export",
    "waveform_export": "waveform_export",
    "visualize": "visualize",
    "compare_visualization": "compare_visualization",
    "result_compare": "result_compare",
    "report_generator": "report_generator",
    "emt_fault_study": "emt_fault_study",
    "fault_clearing_scan": "fault_clearing_scan",
    "fault_severity_scan": "fault_severity_scan",
    "protection_coordination": "protection_coordination",
    "reactive_compensation_design": "reactive_compensation_design",
    "renewable_integration": "renewable_integration",
    "power_quality_analysis": "power_quality_analysis",
    "study_pipeline": "study_pipeline",
    "contingency_analysis": "contingency_analysis",
    "maintenance_security": "maintenance_security",
    "emt_n1_screening": "emt_n1_screening",
    "dudv_curve": "dudv_curve",
    "small_signal_stability": "small_signal_stability",
    "transient_stability_margin": "transient_stability_margin",
    "vsi_weak_bus": "vsi_weak_bus",
    "frequency_response": "frequency_response",
    "disturbance_severity": "disturbance_severity",
}


def get_stage(filename):
    name = filename.replace(".py", "")
    return STAGE_MAP.get(name, name)


def fix_file(filepath):
    content = filepath.read_text()
    original = content
    stage = get_stage(filepath.name)

    pattern = r"(status=SkillStatus\.FAILED,[\s\S]*?)(data=\{\},)(\s*(?:artifacts|logs|error))"

    def replacer(m):
        prefix = m.group(1)
        suffix = m.group(3)
        new_data = (
            "data={\n"
            '            "success": False,\n'
            '            "error": str(e),\n'
            '            "stage": "' + stage + '",\n'
            "        }},\n"
        )
        return prefix + new_data + suffix

    content = re.sub(pattern, replacer, content)

    if content != original:
        filepath.write_text(content)
        return 1
    return 0


def main():
    count = 0
    for filepath in sorted(BUILTIN_DIR.glob("*.py")):
        if filepath.name == "__init__.py":
            continue
        try:
            if fix_file(filepath):
                print(f"Fixed: {filepath.name}")
                count += 1
        except Exception as e:
            print(f"Error in {filepath.name}: {e}")

    print(f"\nTotal files fixed: {count}")


if __name__ == "__main__":
    main()
