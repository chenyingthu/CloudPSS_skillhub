"""CloudPSS SkillHub V2 - 电力系统仿真技能框架

提供48个专业仿真技能，包括：
- 潮流计算、暂态仿真、安全分析
- 稳定性评估、保护配合、新能源接入
- 数据导出、可视化、批量处理
"""

from cloudpss_skills_v2.core import (
    SkillResult,
    SkillStatus,
    Artifact,
    LogEntry,
    TokenManager,
    SkillOutputValidator,
    ValidationResult,
)
from cloudpss_skills_v2.registry import (
    SkillRegistry,
    SkillInfo,
    get_skill,
    list_skills,
    skill_exists,
    register_skill,
)
from cloudpss_skills_v2.base import SkillBase, ToolBase, AnalysisBase
from cloudpss_skills_v2.metadata import (
    SkillMetadata,
    skill_metadata,
    get_skill_metadata,
    has_metadata,
)

# PowerSkill - Simulation layer
from cloudpss_skills_v2.powerskill import (
    PowerFlow,
    EMT,
    ShortCircuit,
    TransientStability,
    HarmonicAnalysis,
    SmallSignalStability,
)

from cloudpss_skills_v2.metadata import SkillMetadata

# PowerAnalysis - all analysis skills
from cloudpss_skills_v2.poweranalysis import (
    N1SecurityAnalysis,
    ContingencyAnalysis,
    VoltageStabilityAnalysis,
    LossAnalysis,
    ShortCircuitAnalysis,
    BatchPowerFlowAnalysis,
    ParamScanAnalysis,
    ParameterSensitivityAnalysis,
    MaintenanceSecurityAnalysis,
    N2SecurityAnalysis,
    TheveninEquivalentAnalysis,
    PowerQualityAnalysisAnalysis,
    FaultSeverityScanAnalysis,
    ProtectionCoordinationAnalysis,
    FrequencyResponseAnalysis,
    DUDVCurveAnalysis,
    DisturbanceSeverityAnalysis,
    OrthogonalSensitivityAnalysis,
    EmtFaultStudyAnalysis,
    EmtN1ScreeningAnalysis,
    HarmonicAnalysisAnalysis,
    SmallSignalStabilityAnalysis,
    TransientStabilityAnalysis,
    TransientStabilityMarginAnalysis,
    FaultClearingScanAnalysis,
    ReactiveCompensationDesignAnalysis,
    RenewableIntegrationAnalysis,
    VSIWeakBusAnalysis,
)

SkillRegistry.register("n1_security", "poweranalysis", N1SecurityAnalysis, "N-1安全校核")
SkillRegistry.register("contingency_analysis", "poweranalysis", ContingencyAnalysis, "预想事故分析")
SkillRegistry.register("voltage_stability", "poweranalysis", VoltageStabilityAnalysis, "电压稳定分析")
SkillRegistry.register("loss_analysis", "poweranalysis", LossAnalysis, "网损分析")
SkillRegistry.register("short_circuit", "poweranalysis", ShortCircuitAnalysis, "短路电流计算")
SkillRegistry.register("batch_powerflow", "poweranalysis", BatchPowerFlowAnalysis, "批量潮流计算")
SkillRegistry.register("param_scan", "poweranalysis", ParamScanAnalysis, "参数扫描分析")
SkillRegistry.register("parameter_sensitivity", "poweranalysis", ParameterSensitivityAnalysis, "参数灵敏度分析")
SkillRegistry.register("maintenance_security", "poweranalysis", MaintenanceSecurityAnalysis, "检修安全校核")
SkillRegistry.register("n2_security", "poweranalysis", N2SecurityAnalysis, "N-2安全校核")
SkillRegistry.register("thevenin_equivalent", "poweranalysis", TheveninEquivalentAnalysis, "戴维南等值")
SkillRegistry.register("power_quality_analysis", "poweranalysis", PowerQualityAnalysisAnalysis, "电能质量分析")
SkillRegistry.register("fault_severity_scan", "poweranalysis", FaultSeverityScanAnalysis, "故障严重度扫描")
SkillRegistry.register("protection_coordination", "poweranalysis", ProtectionCoordinationAnalysis, "保护配合")
SkillRegistry.register("frequency_response", "poweranalysis", FrequencyResponseAnalysis, "频率响应分析")
SkillRegistry.register("dudv_curve", "poweranalysis", DUDVCurveAnalysis, "DUDV曲线")
SkillRegistry.register("disturbance_severity", "poweranalysis", DisturbanceSeverityAnalysis, "扰动严重度")
SkillRegistry.register("orthogonal_sensitivity", "poweranalysis", OrthogonalSensitivityAnalysis, "正交敏感性")
SkillRegistry.register("emt_fault_study", "poweranalysis", EmtFaultStudyAnalysis, "EMT故障研究")
SkillRegistry.register("emt_n1_screening", "poweranalysis", EmtN1ScreeningAnalysis, "EMT N-1筛查")
SkillRegistry.register("harmonic_analysis", "poweranalysis", HarmonicAnalysisAnalysis, "谐波分析")
SkillRegistry.register("small_signal_stability", "poweranalysis", SmallSignalStabilityAnalysis, "小信号稳定")
SkillRegistry.register("transient_stability", "poweranalysis", TransientStabilityAnalysis, "暂态稳定")
SkillRegistry.register("transient_stability_margin", "poweranalysis", TransientStabilityMarginAnalysis, "暂态稳定裕度")
SkillRegistry.register("fault_clearing_scan", "poweranalysis", FaultClearingScanAnalysis, "故障清除扫描")
SkillRegistry.register("reactive_compensation_design", "poweranalysis", ReactiveCompensationDesignAnalysis, "无功补偿设计")
SkillRegistry.register("renewable_integration", "poweranalysis", RenewableIntegrationAnalysis, "新能源接入")
SkillRegistry.register("vsi_weak_bus", "poweranalysis", VSIWeakBusAnalysis, "VSI弱母线")

__version__ = "2.0.0"
__author__ = "CloudPSS Team"

__all__ = [
    "SkillResult", "SkillStatus", "Artifact", "LogEntry",
    "TokenManager", "SkillOutputValidator", "ValidationResult",
    "SkillRegistry", "SkillInfo", "get_skill", "list_skills",
    "skill_exists", "register_skill", "SkillBase", "ToolBase",
    "AnalysisBase", "SkillMetadata", "skill_metadata",
    "get_skill_metadata", "has_metadata",
]

# Tools
from cloudpss_skills_v2.tools import (
    HDF5ExportTool, ComtradeExportTool, WaveformExportTool,
    VisualizeTool, CompareVisualizationTool, ResultCompareTool,
    ReportGeneratorTool, AutoChannelSetupTool, AutoLoopBreakerTool,
    TopologyCheckTool, ModelBuilderTool, ModelHubTool,
    ModelParameterExtractorTool, ComponentCatalogTool,
    BatchTaskManagerTool, ConfigBatchRunnerTool, StudyPipelineTool,
)

# Register tools
SkillRegistry.register("hdf5_export", "tool", HDF5ExportTool, "HDF5数据导出")
SkillRegistry.register("comtrade_export", "tool", ComtradeExportTool, "COMTRADE格式导出")
SkillRegistry.register("waveform_export", "tool", WaveformExportTool, "波形数据导出")
SkillRegistry.register("visualize", "tool", VisualizeTool, "结果可视化")
SkillRegistry.register("compare_visualization", "tool", CompareVisualizationTool, "多场景对比可视化")
SkillRegistry.register("result_compare", "tool", ResultCompareTool, "结果对比分析")
SkillRegistry.register("report_generator", "tool", ReportGeneratorTool, "智能报告生成")
SkillRegistry.register("auto_channel_setup", "tool", AutoChannelSetupTool, "自动量测配置")
SkillRegistry.register("auto_loop_breaker", "tool", AutoLoopBreakerTool, "自动解环")
SkillRegistry.register("topology_check", "tool", TopologyCheckTool, "拓扑检查")
SkillRegistry.register("model_builder", "tool", ModelBuilderTool, "模型构建")
SkillRegistry.register("model_hub", "tool", ModelHubTool, "算例中心")
SkillRegistry.register("model_parameter_extractor", "tool", ModelParameterExtractorTool, "参数提取")
SkillRegistry.register("component_catalog", "tool", ComponentCatalogTool, "组件目录")
SkillRegistry.register("batch_task_manager", "tool", BatchTaskManagerTool, "批处理任务管理")
SkillRegistry.register("config_batch_runner", "tool", ConfigBatchRunnerTool, "配置批量运行")
SkillRegistry.register("study_pipeline", "tool", StudyPipelineTool, "研究流水线")
SkillRegistry.register("model_validator", "tool", ModelBuilderTool, "模型验证")

# Register Simulation skills (PowerSkill layer)
SkillRegistry.register("power_flow", "simulation", PowerFlow, "潮流计算")
SkillRegistry.register("emt_simulation", "simulation", EMT, "EMT暂态仿真")
SkillRegistry.register("short_circuit", "simulation", ShortCircuit, "短路电流计算")
SkillRegistry.register("transient_stability", "simulation", TransientStability, "暂态稳定分析")
SkillRegistry.register("harmonic_analysis", "simulation", HarmonicAnalysis, "谐波分析")
SkillRegistry.register("small_signal_stability", "simulation", SmallSignalStability, "小信号稳定分析")

__all__.extend([
    "HDF5ExportTool", "ComtradeExportTool", "WaveformExportTool",
    "VisualizeTool", "CompareVisualizationTool", "ResultCompareTool",
    "ReportGeneratorTool", "AutoChannelSetupTool", "AutoLoopBreakerTool",
    "TopologyCheckTool", "ModelBuilderTool", "ModelHubTool",
    "ModelParameterExtractorTool", "ComponentCatalogTool",
    "BatchTaskManagerTool", "ConfigBatchRunnerTool", "StudyPipelineTool",
])
