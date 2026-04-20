# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/__pycache__/test_skill_config_integrity.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


def TestSkillConfigIntegrity():
    """TestSkillConfigIntegrity"""
pass  # TODO: restore


def TestSkillRequiredFields():
    """TestSkillRequiredFields"""
pass  # TODO: restore


def TestSpecificSkillConfigs():
    """TestSpecificSkillConfigs"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('Tests for skill configuration integrity.\n\nThis module tests that all skills have proper get_default_config() methods\nand that default configurations pass validation.\n')
#               4 STORE_NAME               0 (__doc__)
# 
#   7           6 LOAD_CONST               1 (0)
#               8 LOAD_CONST               2 (None)
#              10 IMPORT_NAME              1 (builtins)
#              12 STORE_NAME               2 (@py_builtins)
#              14 LOAD_CONST               1 (0)
#              16 LOAD_CONST               2 (None)
#              18 IMPORT_NAME              3 (_pytest.assertion.rewrite)
#              20 IMPORT_FROM              4 (assertion)
#              22 SWAP                     2
#              24 POP_TOP
#              26 IMPORT_FROM              5 (rewrite)
#              28 STORE_NAME               6 (@pytest_ar)
#              30 POP_TOP
#              32 LOAD_CONST               1 (0)
#              34 LOAD_CONST               2 (None)
#              36 IMPORT_NAME              7 (pytest)
#              38 STORE_NAME               7 (pytest)
# 
#   8          40 LOAD_CONST               1 (0)
#              42 LOAD_CONST               3 (('Any', 'Dict', 'List', 'Tuple'))
#              44 IMPORT_NAME              8 (typing)
#              46 IMPORT_FROM              9 (Any)
#              48 STORE_NAME               9 (Any)
#              50 IMPORT_FROM             10 (Dict)
#              52 STORE_NAME              10 (Dict)
#              54 IMPORT_FROM             11 (List)
#              56 STORE_NAME              11 (List)
#              58 IMPORT_FROM             12 (Tuple)
#              60 STORE_NAME              12 (Tuple)
#              62 POP_TOP
# 
#  11          64 LOAD_CONST               1 (0)
#              66 LOAD_CONST               4 (('AutoChannelSetupSkill', 'AutoLoopBreakerSkill', 'BatchPowerFlowSkill', 'BatchTaskManagerSkill', 'CompareVisualizationSkill', 'ComponentCatalogSkill', 'ComtradeExportSkill', 'ConfigBatchRunnerSkill', 'ConfigRunResult', 'ContingencyAnalysisSkill', 'DUDVCurveSkill', 'DisturbanceSeveritySkill', 'EmtFaultStudySkill', 'EmtN1ScreeningSkill', 'EMTSimulationSkill', 'FaultClearingScanSkill', 'FaultSeverityScanSkill', 'FrequencyResponseSkill', 'HDF5ExportSkill', 'HarmonicAnalysisSkill', 'LossAnalysis', 'MaintenanceSecuritySkill', 'ModelBuilderSkill', 'ModelHubSkill', 'ModelParameterExtractorSkill', 'N1SecuritySkill', 'N2SecuritySkill', 'OrthogonalSensitivitySkill', 'ParamScanSkill', 'ParameterSensitivitySkill', 'PowerFlowSkill', 'PowerQualityAnalysisSkill', 'ProtectionCoordinationSkill', 'ReactiveCompensationDesignSkill', 'ReportGeneratorSkill', 'RenewableIntegrationSkill', 'ResultCompareSkill', 'ShortCircuitSkill', 'SmallSignalStabilitySkill', 'StudyPipelineSkill', 'TheveninEquivalentSkill', 'TopologyCheckSkill', 'TransientStabilityMarginSkill', 'TransientStabilitySkill', 'VisualizeSkill', 'VoltageStabilitySkill', 'VSIWeakBusSkill', 'WaveformExportSkill'))
#              68 IMPORT_NAME             13 (cloudpss_skills_v2.skills)
#              70 IMPORT_FROM             14 (AutoChannelSetupSkill)
#              72 STORE_NAME              14 (AutoChannelSetupSkill)
#              74 IMPORT_FROM             15 (AutoLoopBreakerSkill)
#              76 STORE_NAME              15 (AutoLoopBreakerSkill)
#              78 IMPORT_FROM             16 (BatchPowerFlowSkill)
#              80 STORE_NAME              16 (BatchPowerFlowSkill)
#              82 IMPORT_FROM             17 (BatchTaskManagerSkill)
#              84 STORE_NAME              17 (BatchTaskManagerSkill)
#              86 IMPORT_FROM             18 (CompareVisualizationSkill)
#              88 STORE_NAME              18 (CompareVisualizationSkill)
#              90 IMPORT_FROM             19 (ComponentCatalogSkill)
#              92 STORE_NAME              19 (ComponentCatalogSkill)
#              94 IMPORT_FROM             20 (ComtradeExportSkill)
#              96 STORE_NAME              20 (ComtradeExportSkill)
#              98 IMPORT_FROM             21 (ConfigBatchRunnerSkill)
#             100 STORE_NAME              21 (ConfigBatchRunnerSkill)
#             102 IMPORT_FROM             22 (ConfigRunResult)
#             104 STORE_NAME              22 (ConfigRunResult)
#             106 IMPORT_FROM             23 (ContingencyAnalysisSkill)
#             108 STORE_NAME              23 (ContingencyAnalysisSkill)
#             110 IMPORT_FROM             24 (DUDVCurveSkill)
#             112 STORE_NAME              24 (DUDVCurveSkill)
#             114 IMPORT_FROM             25 (DisturbanceSeveritySkill)
#             116 STORE_NAME              25 (DisturbanceSeveritySkill)
#             118 IMPORT_FROM             26 (EmtFaultStudySkill)
#             120 STORE_NAME              26 (EmtFaultStudySkill)
#             122 IMPORT_FROM             27 (EmtN1ScreeningSkill)
#             124 STORE_NAME              27 (EmtN1ScreeningSkill)
#             126 IMPORT_FROM             28 (EMTSimulationSkill)
#             128 STORE_NAME              28 (EMTSimulationSkill)
#             130 IMPORT_FROM             29 (FaultClearingScanSkill)
#             132 STORE_NAME              29 (FaultClearingScanSkill)
#             134 IMPORT_FROM             30 (FaultSeverityScanSkill)
#             136 STORE_NAME              30 (FaultSeverityScanSkill)
#             138 IMPORT_FROM             31 (FrequencyResponseSkill)
#             140 STORE_NAME              31 (FrequencyResponseSkill)
#             142 IMPORT_FROM             32 (HDF5ExportSkill)
#             144 STORE_NAME              32 (HDF5ExportSkill)
#             146 IMPORT_FROM             33 (HarmonicAnalysisSkill)
#             148 STORE_NAME              33 (HarmonicAnalysisSkill)
#             150 IMPORT_FROM             34 (LossAnalysis)
#             152 STORE_NAME              34 (LossAnalysis)
#             154 IMPORT_FROM             35 (MaintenanceSecuritySkill)
#             156 STORE_NAME              35 (MaintenanceSecuritySkill)
#             158 IMPORT_FROM             36 (ModelBuilderSkill)
#             160 STORE_NAME              36 (ModelBuilderSkill)
#             162 IMPORT_FROM             37 (ModelHubSkill)
#             164 STORE_NAME              37 (ModelHubSkill)
#             166 IMPORT_FROM             38 (ModelParameterExtractorSkill)
#             168 STORE_NAME              38 (ModelParameterExtractorSkill)
#             170 IMPORT_FROM             39 (N1SecuritySkill)
#             172 STORE_NAME              39 (N1SecuritySkill)
#             174 IMPORT_FROM             40 (N2SecuritySkill)
#             176 STORE_NAME              40 (N2SecuritySkill)
#             178 IMPORT_FROM             41 (OrthogonalSensitivitySkill)
#             180 STORE_NAME              41 (OrthogonalSensitivitySkill)
#             182 IMPORT_FROM             42 (ParamScanSkill)
#             184 STORE_NAME              42 (ParamScanSkill)
#             186 IMPORT_FROM             43 (ParameterSensitivitySkill)
#             188 STORE_NAME              43 (ParameterSensitivitySkill)
#             190 IMPORT_FROM             44 (PowerFlowSkill)
#             192 STORE_NAME              44 (PowerFlowSkill)
#             194 IMPORT_FROM             45 (PowerQualityAnalysisSkill)
#             196 STORE_NAME              45 (PowerQualityAnalysisSkill)
#             198 IMPORT_FROM             46 (ProtectionCoordinationSkill)
#             200 STORE_NAME              46 (ProtectionCoordinationSkill)
#             202 IMPORT_FROM             47 (ReactiveCompensationDesignSkill)
#             204 STORE_NAME              47 (ReactiveCompensationDesignSkill)
#             206 IMPORT_FROM             48 (ReportGeneratorSkill)
#             208 STORE_NAME              48 (ReportGeneratorSkill)
#             210 IMPORT_FROM             49 (RenewableIntegrationSkill)
#             212 STORE_NAME              49 (RenewableIntegrationSkill)
#             214 IMPORT_FROM             50 (ResultCompareSkill)
#             216 STORE_NAME              50 (ResultCompareSkill)
#             218 IMPORT_FROM             51 (ShortCircuitSkill)
#             220 STORE_NAME              51 (ShortCircuitSkill)
#             222 IMPORT_FROM             52 (SmallSignalStabilitySkill)
#             224 STORE_NAME              52 (SmallSignalStabilitySkill)
#             226 IMPORT_FROM             53 (StudyPipelineSkill)
#             228 STORE_NAME              53 (StudyPipelineSkill)
#             230 IMPORT_FROM             54 (TheveninEquivalentSkill)
#             232 STORE_NAME              54 (TheveninEquivalentSkill)
#             234 IMPORT_FROM             55 (TopologyCheckSkill)
#             236 STORE_NAME              55 (TopologyCheckSkill)
#             238 IMPORT_FROM             56 (TransientStabilityMarginSkill)
#             240 STORE_NAME              56 (TransientStabilityMarginSkill)
#             242 IMPORT_FROM             57 (TransientStabilitySkill)
#             244 STORE_NAME              57 (TransientStabilitySkill)
#             246 IMPORT_FROM             58 (VisualizeSkill)
#             248 STORE_NAME              58 (VisualizeSkill)
#             250 IMPORT_FROM             59 (VoltageStabilitySkill)
#             252 STORE_NAME              59 (VoltageStabilitySkill)
#             254 IMPORT_FROM             60 (VSIWeakBusSkill)
#             256 STORE_NAME              60 (VSIWeakBusSkill)
#             258 IMPORT_FROM             61 (WaveformExportSkill)
#             260 STORE_NAME              61 (WaveformExportSkill)
#             262 POP_TOP
# 
#  64         264 BUILD_LIST               0
# 
#  65         266 LOAD_NAME               14 (AutoChannelSetupSkill)
# 
#  64         268 LIST_APPEND              1
# 
#  66         270 LOAD_NAME               15 (AutoLoopBreakerSkill)
# 
#  64         272 LIST_APPEND              1
# 
#  67         274 LOAD_NAME               16 (BatchPowerFlowSkill)
# 
#  64         276 LIST_APPEND              1
# 
#  68         278 LOAD_NAME               17 (BatchTaskManagerSkill)
# 
#  64         280 LIST_APPEND              1
# 
#  69         282 LOAD_NAME               18 (CompareVisualizationSkill)
# 
#  64         284 LIST_APPEND              1
# 
#  70         286 LOAD_NAME               19 (ComponentCatalogSkill)
# 
#  64         288 LIST_APPEND              1
# 
#  71         290 LOAD_NAME               20 (ComtradeExportSkill)
# 
#  64         292 LIST_APPEND              1
# 
#  72         294 LOAD_NAME               21 (ConfigBatchRunnerSkill)
# 
#  64         296 LIST_APPEND              1
# 
#  73         298 LOAD_NAME               23 (ContingencyAnalysisSkill)
# 
#  64         300 LIST_APPEND              1
# 
#  74         302 LOAD_NAME               24 (DUDVCurveSkill)
# 
#  64         304 LIST_APPEND              1
# 
#  75         306 LOAD_NAME               25 (DisturbanceSeveritySkill)
# 
#  64         308 LIST_APPEND              1
# 
#  76         310 LOAD_NAME               26 (EmtFaultStudySkill)
# 
#  64         312 LIST_APPEND              1
# 
#  77         314 LOAD_NAME               27 (EmtN1ScreeningSkill)
# 
#  64         316 LIST_APPEND              1
# 
#  78         318 LOAD_NAME               28 (EMTSimulationSkill)
# 
#  64         320 LIST_APPEND              1
# 
#  79         322 LOAD_NAME               29 (FaultClearingScanSkill)
# 
#  64         324 LIST_APPEND              1
# 
#  80         326 LOAD_NAME               30 (FaultSeverityScanSkill)
# 
#  64         328 LIST_APPEND              1
# 
#  81         330 LOAD_NAME               31 (FrequencyResponseSkill)
# 
#  64         332 LIST_APPEND              1
# 
#  82         334 LOAD_NAME               32 (HDF5ExportSkill)
# 
#  64         336 LIST_APPEND              1
# 
#  83         338 LOAD_NAME               33 (HarmonicAnalysisSkill)
# 
#  64         340 LIST_APPEND              1
# 
#  84         342 LOAD_NAME               34 (LossAnalysis)
# 
#  64         344 LIST_APPEND              1
# 
#  85         346 LOAD_NAME               35 (MaintenanceSecuritySkill)
# 
#  64         348 LIST_APPEND              1
# 
#  86         350 LOAD_NAME               36 (ModelBuilderSkill)
# 
#  64         352 LIST_APPEND              1
# 
#  87         354 LOAD_NAME               37 (ModelHubSkill)
# 
#  64         356 LIST_APPEND              1
# 
#  88         358 LOAD_NAME               38 (ModelParameterExtractorSkill)
# 
#  64         360 LIST_APPEND              1
# 
#  89         362 LOAD_NAME               39 (N1SecuritySkill)
# 
#  64         364 LIST_APPEND              1
# 
#  90         366 LOAD_NAME               40 (N2SecuritySkill)
# 
#  64         368 LIST_APPEND              1
# 
#  91         370 LOAD_NAME               41 (OrthogonalSensitivitySkill)
# 
#  64         372 LIST_APPEND              1
# 
#  92         374 LOAD_NAME               42 (ParamScanSkill)
# 
#  64         376 LIST_APPEND              1
# 
#  93         378 LOAD_NAME               43 (ParameterSensitivitySkill)
# 
#  64         380 LIST_APPEND              1
# 
#  94         382 LOAD_NAME               44 (PowerFlowSkill)
# 
#  64         384 LIST_APPEND              1
# 
#  95         386 LOAD_NAME               45 (PowerQualityAnalysisSkill)
# 
#  64         388 LIST_APPEND              1
# 
#  96         390 LOAD_NAME               46 (ProtectionCoordinationSkill)
# 
#  64         392 LIST_APPEND              1
# 
#  97         394 LOAD_NAME               47 (ReactiveCompensationDesignSkill)
# 
#  64         396 LIST_APPEND              1
# 
#  98         398 LOAD_NAME               48 (ReportGeneratorSkill)
# 
#  64         400 LIST_APPEND              1
# 
#  99         402 LOAD_NAME               49 (RenewableIntegrationSkill)
# 
#  64         404 LIST_APPEND              1
# 
# 100         406 LOAD_NAME               50 (ResultCompareSkill)
# 
#  64         408 LIST_APPEND              1
# 
# 101         410 LOAD_NAME               51 (ShortCircuitSkill)
# 
#  64         412 LIST_APPEND              1
# 
# 102         414 LOAD_NAME               52 (SmallSignalStabilitySkill)
# 
#  64         416 LIST_APPEND              1
# 
# 103         418 LOAD_NAME               53 (StudyPipelineSkill)
# 
#  64         420 LIST_APPEND              1
# 
# 104         422 LOAD_NAME               54 (TheveninEquivalentSkill)
# 
#  64         424 LIST_APPEND              1
# 
# 105         426 LOAD_NAME               55 (TopologyCheckSkill)
# 
#  64         428 LIST_APPEND              1
# 
# 106         430 LOAD_NAME               56 (TransientStabilityMarginSkill)
# 
#  64         432 LIST_APPEND              1
# 
# 107         434 LOAD_NAME               57 (TransientStabilitySkill)
# 
#  64         436 LIST_APPEND              1
# 
# 108         438 LOAD_NAME               58 (VisualizeSkill)
# 
#  64         440 LIST_APPEND              1
# 
# 109         442 LOAD_NAME               59 (VoltageStabilitySkill)
# 
#  64         444 LIST_APPEND              1
# 
# 110         446 LOAD_NAME               60 (VSIWeakBusSkill)
# 
#  64         448 LIST_APPEND              1
# 
# 111         450 LOAD_NAME               61 (WaveformExportSkill)
# 
#  64         452 LIST_APPEND              1
#             454 STORE_NAME              62 (ALL_SKILL_CLASSES)
# 
# 115         456 PUSH_NULL
#             458 LOAD_BUILD_CLASS
#             460 LOAD_CONST               5 (<code object TestSkillConfigIntegrity at 0x73cd9491a010, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 115>)
#             462 MAKE_FUNCTION            0
#             464 LOAD_CONST               6 ('TestSkillConfigIntegrity')
#             466 CALL                     2
#             474 STORE_NAME              63 (TestSkillConfigIntegrity)
# 
# 183         476 PUSH_NULL
#             478 LOAD_BUILD_CLASS
#             480 LOAD_CONST               7 (<code object TestSkillRequiredFields at 0x73cd93b39a10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 183>)
#             482 MAKE_FUNCTION            0
#             484 LOAD_CONST               8 ('TestSkillRequiredFields')
#             486 CALL                     2
#             494 STORE_NAME              64 (TestSkillRequiredFields)
# 
# 217         496 PUSH_NULL
#             498 LOAD_BUILD_CLASS
#             500 LOAD_CONST               9 (<code object TestSpecificSkillConfigs at 0x73cd93b44d40, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 217>)
#             502 MAKE_FUNCTION            0
#             504 LOAD_CONST              10 ('TestSpecificSkillConfigs')
#             506 CALL                     2
#             514 STORE_NAME              65 (TestSpecificSkillConfigs)
# 
# 334         516 LOAD_NAME               66 (__name__)
#             518 LOAD_CONST              11 ('__main__')
#             520 COMPARE_OP              40 (==)
#             524 POP_JUMP_IF_FALSE       21 (to 568)
# 
# 335         526 PUSH_NULL
#             528 LOAD_NAME                7 (pytest)
#             530 LOAD_ATTR              134 (main)
#             550 LOAD_NAME               68 (__file__)
#             552 LOAD_CONST              12 ('-v')
#             554 BUILD_LIST               2
#             556 CALL                     1
#             564 POP_TOP
#             566 RETURN_CONST             2 (None)
# 
# 334     >>  568 RETURN_CONST             2 (None)
# 
# Disassembly of <code object TestSkillConfigIntegrity at 0x73cd9491a010, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 115>:
# 115           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestSkillConfigIntegrity')
#               8 STORE_NAME               2 (__qualname__)
# 
# 116          10 LOAD_CONST               1 ('Test that all skills have proper configuration methods.')
#              12 STORE_NAME               3 (__doc__)
# 
# 118          14 LOAD_NAME                4 (pytest)
#              16 LOAD_ATTR               10 (mark)
#              36 LOAD_ATTR               13 (NULL|self + parametrize)
#              56 LOAD_CONST               2 ('skill_class')
#              58 LOAD_NAME                7 (ALL_SKILL_CLASSES)
#              60 CALL                     2
# 
# 119          68 LOAD_CONST               3 (<code object test_skill_has_get_default_config at 0x3af9f150, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 118>)
#              70 MAKE_FUNCTION            0
# 
# 118          72 CALL                     0
# 
# 119          80 STORE_NAME               8 (test_skill_has_get_default_config)
# 
# 129          82 LOAD_NAME                4 (pytest)
#              84 LOAD_ATTR               10 (mark)
#             104 LOAD_ATTR               13 (NULL|self + parametrize)
#             124 LOAD_CONST               2 ('skill_class')
#             126 LOAD_NAME                7 (ALL_SKILL_CLASSES)
#             128 CALL                     2
# 
# 130         136 LOAD_CONST               4 (<code object test_default_config_returns_dict at 0x3af9bd40, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 129>)
#             138 MAKE_FUNCTION            0
# 
# 129         140 CALL                     0
# 
# 130         148 STORE_NAME               9 (test_default_config_returns_dict)
# 
# 139         150 LOAD_NAME                4 (pytest)
#             152 LOAD_ATTR               10 (mark)
#             172 LOAD_ATTR               13 (NULL|self + parametrize)
#             192 LOAD_CONST               2 ('skill_class')
#             194 LOAD_NAME                7 (ALL_SKILL_CLASSES)
#             196 CALL                     2
# 
# 140         204 LOAD_CONST               5 (<code object test_default_config_contains_skill_name at 0x3afa6250, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 139>)
#             206 MAKE_FUNCTION            0
# 
# 139         208 CALL                     0
# 
# 140         216 STORE_NAME              10 (test_default_config_contains_skill_name)
# 
# 152         218 LOAD_NAME                4 (pytest)
#             220 LOAD_ATTR               10 (mark)
#             240 LOAD_ATTR               13 (NULL|self + parametrize)
#             260 LOAD_CONST               2 ('skill_class')
#             262 LOAD_NAME                7 (ALL_SKILL_CLASSES)
#             264 CALL                     2
# 
# 153         272 LOAD_CONST               6 (<code object test_default_config_passes_validation at 0x3afaa120, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 152>)
#             274 MAKE_FUNCTION            0
# 
# 152         276 CALL                     0
# 
# 153         284 STORE_NAME              11 (test_default_config_passes_validation)
#             286 RETURN_CONST             7 (None)
# 
# Disassembly of <code object test_skill_has_get_default_config at 0x3af9f150, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 118>:
# 118           0 RESUME                   0
# 
# 121           2 PUSH_NULL
#               4 LOAD_FAST                1 (skill_class)
#               6 CALL                     0
#              14 STORE_FAST               2 (skill)
# 
# 122          16 LOAD_CONST               1 ('get_default_config')
#              18 STORE_FAST               3 (@py_assert2)
#              20 LOAD_GLOBAL              1 (NULL + hasattr)
#              30 LOAD_FAST                2 (skill)
#              32 LOAD_FAST                3 (@py_assert2)
#              34 CALL                     2
#              42 STORE_FAST               4 (@py_assert4)
#              44 LOAD_FAST                4 (@py_assert4)
#              46 POP_JUMP_IF_TRUE       249 (to 546)
#              48 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 124          58 LOAD_ATTR                4 (_format_assertmsg)
# 
# 123          78 LOAD_FAST                1 (skill_class)
#              80 LOAD_ATTR                6 (__name__)
#             100 FORMAT_VALUE             0
#             102 LOAD_CONST               2 (' must have get_default_config() method')
#             104 BUILD_STRING             2
# 
# 122         106 CALL                     1
#             114 LOAD_CONST               3 ('\n>assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}')
#             116 BINARY_OP                0 (+)
#             120 LOAD_CONST               4 ('hasattr')
#             122 LOAD_GLOBAL              9 (NULL + @py_builtins)
# 
# 124         132 LOAD_ATTR               10 (locals)
# 
# 122         152 CALL                     0
#             160 CONTAINS_OP              0
#             162 POP_JUMP_IF_TRUE        25 (to 214)
#             164 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 124         174 LOAD_ATTR               12 (_should_repr_global_name)
# 
# 122         194 LOAD_GLOBAL              0 (hasattr)
#             204 CALL                     1
#             212 POP_JUMP_IF_FALSE       25 (to 264)
#         >>  214 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 124         224 LOAD_ATTR               14 (_saferepr)
# 
# 122         244 LOAD_GLOBAL              0 (hasattr)
#             254 CALL                     1
#             262 JUMP_FORWARD             1 (to 266)
#         >>  264 LOAD_CONST               4 ('hasattr')
#         >>  266 LOAD_CONST               5 ('skill')
#             268 LOAD_GLOBAL              9 (NULL + @py_builtins)
# 
# 124         278 LOAD_ATTR               10 (locals)
# 
# 122         298 CALL                     0
#             306 CONTAINS_OP              0
#             308 POP_JUMP_IF_TRUE        21 (to 352)
#             310 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 124         320 LOAD_ATTR               12 (_should_repr_global_name)
# 
# 122         340 LOAD_FAST                2 (skill)
#             342 CALL                     1
#             350 POP_JUMP_IF_FALSE       21 (to 394)
#         >>  352 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 124         362 LOAD_ATTR               14 (_saferepr)
# 
# 122         382 LOAD_FAST                2 (skill)
#             384 CALL                     1
#             392 JUMP_FORWARD             1 (to 396)
#         >>  394 LOAD_CONST               5 ('skill')
#         >>  396 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 124         406 LOAD_ATTR               14 (_saferepr)
# 
# 122         426 LOAD_FAST                3 (@py_assert2)
#             428 CALL                     1
#             436 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 124         446 LOAD_ATTR               14 (_saferepr)
# 
# 122         466 LOAD_FAST                4 (@py_assert4)
#             468 CALL                     1
#             476 LOAD_CONST               6 (('py0', 'py1', 'py3', 'py5'))
#             478 BUILD_CONST_KEY_MAP      4
#             480 BINARY_OP                6 (%)
#             484 STORE_FAST               5 (@py_format6)
#             486 LOAD_GLOBAL             17 (NULL + AssertionError)
#             496 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 124         506 LOAD_ATTR               18 (_format_explanation)
# 
# 122         526 LOAD_FAST                5 (@py_format6)
#             528 CALL                     1
#             536 CALL                     1
#             544 RAISE_VARARGS            1
#         >>  546 LOAD_CONST               7 (None)
#             548 COPY                     1
#             550 STORE_FAST               3 (@py_assert2)
#             552 STORE_FAST               4 (@py_assert4)
# 
# 125         554 LOAD_CONST               1 ('get_default_config')
#             556 STORE_FAST               6 (@py_assert3)
#             558 LOAD_GLOBAL             21 (NULL + getattr)
#             568 LOAD_FAST                2 (skill)
#             570 LOAD_FAST                6 (@py_assert3)
#             572 CALL                     2
#             580 STORE_FAST               7 (@py_assert5)
#             582 LOAD_GLOBAL             23 (NULL + callable)
#             592 LOAD_FAST                7 (@py_assert5)
#             594 CALL                     1
#             602 STORE_FAST               8 (@py_assert7)
#             604 LOAD_FAST                8 (@py_assert7)
#             606 EXTENDED_ARG             1
#             608 POP_JUMP_IF_TRUE       342 (to 1294)
#             610 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 127         620 LOAD_ATTR                4 (_format_assertmsg)
# 
# 126         640 LOAD_FAST                1 (skill_class)
#             642 LOAD_ATTR                6 (__name__)
#             662 FORMAT_VALUE             0
#             664 LOAD_CONST               8 ('.get_default_config must be callable')
#             666 BUILD_STRING             2
# 
# 125         668 CALL                     1
#             676 LOAD_CONST               9 ('\n>assert %(py8)s\n{%(py8)s = %(py0)s(%(py6)s\n{%(py6)s = %(py1)s(%(py2)s, %(py4)s)\n})\n}')
#             678 BINARY_OP                0 (+)
#             682 LOAD_CONST              10 ('callable')
#             684 LOAD_GLOBAL              9 (NULL + @py_builtins)
# 
# 127         694 LOAD_ATTR               10 (locals)
# 
# 125         714 CALL                     0
#             722 CONTAINS_OP              0
#             724 POP_JUMP_IF_TRUE        25 (to 776)
#             726 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 127         736 LOAD_ATTR               12 (_should_repr_global_name)
# 
# 125         756 LOAD_GLOBAL             22 (callable)
#             766 CALL                     1
#             774 POP_JUMP_IF_FALSE       25 (to 826)
#         >>  776 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 127         786 LOAD_ATTR               14 (_saferepr)
# 
# 125         806 LOAD_GLOBAL             22 (callable)
#             816 CALL                     1
#             824 JUMP_FORWARD             1 (to 828)
#         >>  826 LOAD_CONST              10 ('callable')
#         >>  828 LOAD_CONST              11 ('getattr')
#             830 LOAD_GLOBAL              9 (NULL + @py_builtins)
# 
# 127         840 LOAD_ATTR               10 (locals)
# 
# 125         860 CALL                     0
#             868 CONTAINS_OP              0
#             870 POP_JUMP_IF_TRUE        25 (to 922)
#             872 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 127         882 LOAD_ATTR               12 (_should_repr_global_name)
# 
# 125         902 LOAD_GLOBAL             20 (getattr)
#             912 CALL                     1
#             920 POP_JUMP_IF_FALSE       25 (to 972)
#         >>  922 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 127         932 LOAD_ATTR               14 (_saferepr)
# 
# 125         952 LOAD_GLOBAL             20 (getattr)
#             962 CALL                     1
#             970 JUMP_FORWARD             1 (to 974)
#         >>  972 LOAD_CONST              11 ('getattr')
#         >>  974 LOAD_CONST               5 ('skill')
#             976 LOAD_GLOBAL              9 (NULL + @py_builtins)
# 
# 127         986 LOAD_ATTR               10 (locals)
# 
# 125        1006 CALL                     0
#            1014 CONTAINS_OP              0
#            1016 POP_JUMP_IF_TRUE        21 (to 1060)
#            1018 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 127        1028 LOAD_ATTR               12 (_should_repr_global_name)
# 
# 125        1048 LOAD_FAST                2 (skill)
#            1050 CALL                     1
#            1058 POP_JUMP_IF_FALSE       21 (to 1102)
#         >> 1060 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 127        1070 LOAD_ATTR               14 (_saferepr)
# 
# 125        1090 LOAD_FAST                2 (skill)
#            1092 CALL                     1
#            1100 JUMP_FORWARD             1 (to 1104)
#         >> 1102 LOAD_CONST               5 ('skill')
#         >> 1104 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 127        1114 LOAD_ATTR               14 (_saferepr)
# 
# 125        1134 LOAD_FAST                6 (@py_assert3)
#            1136 CALL                     1
#            1144 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 127        1154 LOAD_ATTR               14 (_saferepr)
# 
# 125        1174 LOAD_FAST                7 (@py_assert5)
#            1176 CALL                     1
#            1184 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 127        1194 LOAD_ATTR               14 (_saferepr)
# 
# 125        1214 LOAD_FAST                8 (@py_assert7)
#            1216 CALL                     1
#            1224 LOAD_CONST              12 (('py0', 'py1', 'py2', 'py4', 'py6', 'py8'))
#            1226 BUILD_CONST_KEY_MAP      6
#            1228 BINARY_OP                6 (%)
#            1232 STORE_FAST               9 (@py_format9)
#            1234 LOAD_GLOBAL             17 (NULL + AssertionError)
#            1244 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 127        1254 LOAD_ATTR               18 (_format_explanation)
# 
# 125        1274 LOAD_FAST                9 (@py_format9)
#            1276 CALL                     1
#            1284 CALL                     1
#            1292 RAISE_VARARGS            1
#         >> 1294 LOAD_CONST               7 (None)
#            1296 COPY                     1
#            1298 STORE_FAST               6 (@py_assert3)
#            1300 COPY                     1
#            1302 STORE_FAST               7 (@py_assert5)
#            1304 STORE_FAST               8 (@py_assert7)
#            1306 RETURN_CONST             7 (None)
# 
# Disassembly of <code object test_default_config_returns_dict at 0x3af9bd40, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 129>:
# 129           0 RESUME                   0
# 
# 132           2 PUSH_NULL
#               4 LOAD_FAST                1 (skill_class)
#               6 CALL                     0
#              14 STORE_FAST               2 (skill)
# 
# 133          16 LOAD_FAST                2 (skill)
#              18 LOAD_ATTR                1 (NULL|self + get_default_config)
#              38 CALL                     0
#              46 STORE_FAST               3 (default_config)
# 
# 134          48 LOAD_GLOBAL              3 (NULL + isinstance)
#              58 LOAD_FAST                3 (default_config)
#              60 LOAD_GLOBAL              4 (dict)
#              70 CALL                     2
#              78 STORE_FAST               4 (@py_assert3)
#              80 LOAD_FAST                4 (@py_assert3)
#              82 EXTENDED_ARG             1
#              84 POP_JUMP_IF_TRUE       323 (to 732)
#              86 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 137          96 LOAD_ATTR                8 (_format_assertmsg)
# 
# 135         116 LOAD_FAST                1 (skill_class)
#             118 LOAD_ATTR               10 (__name__)
#             138 FORMAT_VALUE             0
#             140 LOAD_CONST               1 ('.get_default_config() must return a dict, got ')
# 
# 136         142 LOAD_GLOBAL             13 (NULL + type)
#             152 LOAD_FAST                3 (default_config)
#             154 CALL                     1
#             162 LOAD_ATTR               10 (__name__)
#             182 FORMAT_VALUE             0
# 
# 135         184 BUILD_STRING             3
# 
# 134         186 CALL                     1
#             194 LOAD_CONST               2 ('\n>assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}')
#             196 BINARY_OP                0 (+)
#             200 LOAD_CONST               3 ('isinstance')
#             202 LOAD_GLOBAL             15 (NULL + @py_builtins)
# 
# 137         212 LOAD_ATTR               16 (locals)
# 
# 134         232 CALL                     0
#             240 CONTAINS_OP              0
#             242 POP_JUMP_IF_TRUE        25 (to 294)
#             244 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 137         254 LOAD_ATTR               18 (_should_repr_global_name)
# 
# 134         274 LOAD_GLOBAL              2 (isinstance)
#             284 CALL                     1
#             292 POP_JUMP_IF_FALSE       25 (to 344)
#         >>  294 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 137         304 LOAD_ATTR               20 (_saferepr)
# 
# 134         324 LOAD_GLOBAL              2 (isinstance)
#             334 CALL                     1
#             342 JUMP_FORWARD             1 (to 346)
#         >>  344 LOAD_CONST               3 ('isinstance')
#         >>  346 LOAD_CONST               4 ('default_config')
#             348 LOAD_GLOBAL             15 (NULL + @py_builtins)
# 
# 137         358 LOAD_ATTR               16 (locals)
# 
# 134         378 CALL                     0
#             386 CONTAINS_OP              0
#             388 POP_JUMP_IF_TRUE        21 (to 432)
#             390 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 137         400 LOAD_ATTR               18 (_should_repr_global_name)
# 
# 134         420 LOAD_FAST                3 (default_config)
#             422 CALL                     1
#             430 POP_JUMP_IF_FALSE       21 (to 474)
#         >>  432 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 137         442 LOAD_ATTR               20 (_saferepr)
# 
# 134         462 LOAD_FAST                3 (default_config)
#             464 CALL                     1
#             472 JUMP_FORWARD             1 (to 476)
#         >>  474 LOAD_CONST               4 ('default_config')
#         >>  476 LOAD_CONST               5 ('dict')
#             478 LOAD_GLOBAL             15 (NULL + @py_builtins)
# 
# 137         488 LOAD_ATTR               16 (locals)
# 
# 134         508 CALL                     0
#             516 CONTAINS_OP              0
#             518 POP_JUMP_IF_TRUE        25 (to 570)
#             520 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 137         530 LOAD_ATTR               18 (_should_repr_global_name)
# 
# 134         550 LOAD_GLOBAL              4 (dict)
#             560 CALL                     1
#             568 POP_JUMP_IF_FALSE       25 (to 620)
#         >>  570 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 137         580 LOAD_ATTR               20 (_saferepr)
# 
# 134         600 LOAD_GLOBAL              4 (dict)
#             610 CALL                     1
#             618 JUMP_FORWARD             1 (to 622)
#         >>  620 LOAD_CONST               5 ('dict')
#         >>  622 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 137         632 LOAD_ATTR               20 (_saferepr)
# 
# 134         652 LOAD_FAST                4 (@py_assert3)
#             654 CALL                     1
#             662 LOAD_CONST               6 (('py0', 'py1', 'py2', 'py4'))
#             664 BUILD_CONST_KEY_MAP      4
#             666 BINARY_OP                6 (%)
#             670 STORE_FAST               5 (@py_format5)
#             672 LOAD_GLOBAL             23 (NULL + AssertionError)
#             682 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 137         692 LOAD_ATTR               24 (_format_explanation)
# 
# 134         712 LOAD_FAST                5 (@py_format5)
#             714 CALL                     1
#             722 CALL                     1
#             730 RAISE_VARARGS            1
#         >>  732 LOAD_CONST               7 (None)
#             734 STORE_FAST               4 (@py_assert3)
#             736 RETURN_CONST             7 (None)
# 
# Disassembly of <code object test_default_config_contains_skill_name at 0x3afa6250, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 139>:
# 139           0 RESUME                   0
# 
# 142           2 PUSH_NULL
#               4 LOAD_FAST                1 (skill_class)
#               6 CALL                     0
#              14 STORE_FAST               2 (skill)
# 
# 143          16 LOAD_FAST                2 (skill)
#              18 LOAD_ATTR                1 (NULL|self + get_default_config)
#              38 CALL                     0
#              46 STORE_FAST               3 (default_config)
# 
# 144          48 LOAD_CONST               1 ('skill')
#              50 STORE_FAST               4 (@py_assert0)
#              52 LOAD_FAST                4 (@py_assert0)
#              54 LOAD_FAST                3 (default_config)
#              56 CONTAINS_OP              0
#              58 STORE_FAST               5 (@py_assert2)
#              60 LOAD_FAST                5 (@py_assert2)
#              62 POP_JUMP_IF_TRUE       188 (to 440)
#              64 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 146          74 LOAD_ATTR                4 (_call_reprcompare)
# 
# 144          94 LOAD_CONST               2 (('in',))
#              96 LOAD_FAST                5 (@py_assert2)
#              98 BUILD_TUPLE              1
#             100 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             102 LOAD_FAST                4 (@py_assert0)
#             104 LOAD_FAST                3 (default_config)
#             106 BUILD_TUPLE              2
#             108 CALL                     4
#             116 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 146         126 LOAD_ATTR                6 (_saferepr)
# 
# 144         146 LOAD_FAST                4 (@py_assert0)
#             148 CALL                     1
#             156 LOAD_CONST               4 ('default_config')
#             158 LOAD_GLOBAL              9 (NULL + @py_builtins)
# 
# 146         168 LOAD_ATTR               10 (locals)
# 
# 144         188 CALL                     0
#             196 CONTAINS_OP              0
#             198 POP_JUMP_IF_TRUE        21 (to 242)
#             200 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 146         210 LOAD_ATTR               12 (_should_repr_global_name)
# 
# 144         230 LOAD_FAST                3 (default_config)
#             232 CALL                     1
#             240 POP_JUMP_IF_FALSE       21 (to 284)
#         >>  242 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 146         252 LOAD_ATTR                6 (_saferepr)
# 
# 144         272 LOAD_FAST                3 (default_config)
#             274 CALL                     1
#             282 JUMP_FORWARD             1 (to 286)
#         >>  284 LOAD_CONST               4 ('default_config')
#         >>  286 LOAD_CONST               5 (('py1', 'py3'))
#             288 BUILD_CONST_KEY_MAP      2
#             290 BINARY_OP                6 (%)
#             294 STORE_FAST               6 (@py_format4)
#             296 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 146         306 LOAD_ATTR               14 (_format_assertmsg)
# 
# 145         326 LOAD_FAST                1 (skill_class)
#             328 LOAD_ATTR               16 (__name__)
#             348 FORMAT_VALUE             0
#             350 LOAD_CONST               6 (".get_default_config() must contain 'skill' field")
#             352 BUILD_STRING             2
# 
# 144         354 CALL                     1
#             362 LOAD_CONST               7 ('\n>assert %(py5)s')
#             364 BINARY_OP                0 (+)
#             368 LOAD_CONST               8 ('py5')
#             370 LOAD_FAST                6 (@py_format4)
#             372 BUILD_MAP                1
#             374 BINARY_OP                6 (%)
#             378 STORE_FAST               7 (@py_format6)
#             380 LOAD_GLOBAL             19 (NULL + AssertionError)
#             390 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 146         400 LOAD_ATTR               20 (_format_explanation)
# 
# 144         420 LOAD_FAST                7 (@py_format6)
#             422 CALL                     1
#             430 CALL                     1
#             438 RAISE_VARARGS            1
#         >>  440 LOAD_CONST               9 (None)
#             442 COPY                     1
#             444 STORE_FAST               4 (@py_assert0)
#             446 STORE_FAST               5 (@py_assert2)
# 
# 147         448 LOAD_GLOBAL             23 (NULL + getattr)
#             458 LOAD_FAST                2 (skill)
#             460 LOAD_CONST              10 ('name')
#             462 LOAD_FAST                1 (skill_class)
#             464 LOAD_ATTR               16 (__name__)
#             484 LOAD_ATTR               25 (NULL|self + lower)
#             504 CALL                     0
#             512 LOAD_ATTR               27 (NULL|self + replace)
#             532 LOAD_CONST               1 ('skill')
#             534 LOAD_CONST              11 ('')
#             536 CALL                     2
#             544 CALL                     3
#             552 STORE_FAST               8 (expected_name)
# 
# 148         554 LOAD_FAST                3 (default_config)
#             556 LOAD_CONST               1 ('skill')
#             558 BINARY_SUBSCR
#             562 STORE_FAST               4 (@py_assert0)
#             564 LOAD_FAST                4 (@py_assert0)
#             566 LOAD_FAST                8 (expected_name)
#             568 COMPARE_OP              40 (==)
#             572 STORE_FAST               5 (@py_assert2)
#             574 LOAD_FAST                5 (@py_assert2)
#             576 POP_JUMP_IF_TRUE       191 (to 960)
#             578 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 150         588 LOAD_ATTR                4 (_call_reprcompare)
# 
# 148         608 LOAD_CONST              12 (('==',))
#             610 LOAD_FAST                5 (@py_assert2)
#             612 BUILD_TUPLE              1
#             614 LOAD_CONST              13 (('%(py1)s == %(py3)s',))
#             616 LOAD_FAST                4 (@py_assert0)
#             618 LOAD_FAST                8 (expected_name)
#             620 BUILD_TUPLE              2
#             622 CALL                     4
#             630 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 150         640 LOAD_ATTR                6 (_saferepr)
# 
# 148         660 LOAD_FAST                4 (@py_assert0)
#             662 CALL                     1
#             670 LOAD_CONST              14 ('expected_name')
#             672 LOAD_GLOBAL              9 (NULL + @py_builtins)
# 
# 150         682 LOAD_ATTR               10 (locals)
# 
# 148         702 CALL                     0
#             710 CONTAINS_OP              0
#             712 POP_JUMP_IF_TRUE        21 (to 756)
#             714 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 150         724 LOAD_ATTR               12 (_should_repr_global_name)
# 
# 148         744 LOAD_FAST                8 (expected_name)
#             746 CALL                     1
#             754 POP_JUMP_IF_FALSE       21 (to 798)
#         >>  756 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 150         766 LOAD_ATTR                6 (_saferepr)
# 
# 148         786 LOAD_FAST                8 (expected_name)
#             788 CALL                     1
#             796 JUMP_FORWARD             1 (to 800)
#         >>  798 LOAD_CONST              14 ('expected_name')
#         >>  800 LOAD_CONST               5 (('py1', 'py3'))
#             802 BUILD_CONST_KEY_MAP      2
#             804 BINARY_OP                6 (%)
#             808 STORE_FAST               6 (@py_format4)
#             810 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 150         820 LOAD_ATTR               14 (_format_assertmsg)
# 
# 149         840 LOAD_FAST                1 (skill_class)
#             842 LOAD_ATTR               16 (__name__)
#             862 FORMAT_VALUE             0
#             864 LOAD_CONST              15 (".get_default_config()['skill'] must be '")
#             866 LOAD_FAST                8 (expected_name)
#             868 FORMAT_VALUE             0
#             870 LOAD_CONST              16 ("'")
#             872 BUILD_STRING             4
# 
# 148         874 CALL                     1
#             882 LOAD_CONST               7 ('\n>assert %(py5)s')
#             884 BINARY_OP                0 (+)
#             888 LOAD_CONST               8 ('py5')
#             890 LOAD_FAST                6 (@py_format4)
#             892 BUILD_MAP                1
#             894 BINARY_OP                6 (%)
#             898 STORE_FAST               7 (@py_format6)
#             900 LOAD_GLOBAL             19 (NULL + AssertionError)
#             910 LOAD_GLOBAL              3 (NULL + @pytest_ar)
# 
# 150         920 LOAD_ATTR               20 (_format_explanation)
# 
# 148         940 LOAD_FAST                7 (@py_format6)
#             942 CALL                     1
#             950 CALL                     1
#             958 RAISE_VARARGS            1
#         >>  960 LOAD_CONST               9 (None)
#             962 COPY                     1
#             964 STORE_FAST               4 (@py_assert0)
#             966 STORE_FAST               5 (@py_assert2)
#             968 RETURN_CONST             9 (None)
# 
# Disassembly of <code object test_default_config_passes_validation at 0x3afaa120, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 152>:
# 152           0 RESUME                   0
# 
# 160           2 PUSH_NULL
#               4 LOAD_FAST                1 (skill_class)
#               6 CALL                     0
#              14 STORE_FAST               2 (skill)
# 
# 161          16 LOAD_FAST                2 (skill)
#              18 LOAD_ATTR                1 (NULL|self + get_default_config)
#              38 CALL                     0
#              46 STORE_FAST               3 (default_config)
# 
# 164          48 LOAD_GLOBAL              3 (NULL + hasattr)
#              58 LOAD_FAST                2 (skill)
#              60 LOAD_CONST               1 ('validate')
#              62 CALL                     2
#              70 POP_JUMP_IF_TRUE        34 (to 140)
# 
# 165          72 LOAD_GLOBAL              5 (NULL + pytest)
#              82 LOAD_ATTR                6 (skip)
#             102 LOAD_FAST                1 (skill_class)
#             104 LOAD_ATTR                8 (__name__)
#             124 FORMAT_VALUE             0
#             126 LOAD_CONST               2 (' does not have validate() method')
#             128 BUILD_STRING             2
#             130 CALL                     1
#             138 POP_TOP
# 
# 167     >>  140 NOP
# 
# 168         142 LOAD_FAST                2 (skill)
#             144 LOAD_ATTR               11 (NULL|self + validate)
#             164 LOAD_FAST                3 (default_config)
#             166 CALL                     1
#             174 UNPACK_SEQUENCE          2
#             178 STORE_FAST               4 (valid)
#             180 STORE_FAST               5 (errors)
# 
# 171         182 LOAD_GLOBAL             13 (NULL + isinstance)
#             192 LOAD_FAST                4 (valid)
#             194 LOAD_GLOBAL             14 (bool)
#             204 CALL                     2
#             212 STORE_FAST               6 (@py_assert3)
#             214 LOAD_FAST                6 (@py_assert3)
#             216 EXTENDED_ARG             1
#             218 POP_JUMP_IF_TRUE       302 (to 824)
#             220 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 173         230 LOAD_ATTR               18 (_format_assertmsg)
# 
# 172         250 LOAD_FAST                1 (skill_class)
#             252 LOAD_ATTR                8 (__name__)
#             272 FORMAT_VALUE             0
#             274 LOAD_CONST               3 ('.validate() must return bool as first element')
#             276 BUILD_STRING             2
# 
# 171         278 CALL                     1
#             286 LOAD_CONST               4 ('\n>assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}')
#             288 BINARY_OP                0 (+)
#             292 LOAD_CONST               5 ('isinstance')
#             294 LOAD_GLOBAL             21 (NULL + @py_builtins)
# 
# 173         304 LOAD_ATTR               22 (locals)
# 
# 171         324 CALL                     0
#             332 CONTAINS_OP              0
#             334 POP_JUMP_IF_TRUE        25 (to 386)
#             336 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 173         346 LOAD_ATTR               24 (_should_repr_global_name)
# 
# 171         366 LOAD_GLOBAL             12 (isinstance)
#             376 CALL                     1
#             384 POP_JUMP_IF_FALSE       25 (to 436)
#         >>  386 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 173         396 LOAD_ATTR               26 (_saferepr)
# 
# 171         416 LOAD_GLOBAL             12 (isinstance)
#             426 CALL                     1
#             434 JUMP_FORWARD             1 (to 438)
#         >>  436 LOAD_CONST               5 ('isinstance')
#         >>  438 LOAD_CONST               6 ('valid')
#             440 LOAD_GLOBAL             21 (NULL + @py_builtins)
# 
# 173         450 LOAD_ATTR               22 (locals)
# 
# 171         470 CALL                     0
#             478 CONTAINS_OP              0
#             480 POP_JUMP_IF_TRUE        21 (to 524)
#             482 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 173         492 LOAD_ATTR               24 (_should_repr_global_name)
# 
# 171         512 LOAD_FAST                4 (valid)
#             514 CALL                     1
#             522 POP_JUMP_IF_FALSE       21 (to 566)
#         >>  524 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 173         534 LOAD_ATTR               26 (_saferepr)
# 
# 171         554 LOAD_FAST                4 (valid)
#             556 CALL                     1
#             564 JUMP_FORWARD             1 (to 568)
#         >>  566 LOAD_CONST               6 ('valid')
#         >>  568 LOAD_CONST               7 ('bool')
#             570 LOAD_GLOBAL             21 (NULL + @py_builtins)
# 
# 173         580 LOAD_ATTR               22 (locals)
# 
# 171         600 CALL                     0
#             608 CONTAINS_OP              0
#             610 POP_JUMP_IF_TRUE        25 (to 662)
#             612 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 173         622 LOAD_ATTR               24 (_should_repr_global_name)
# 
# 171         642 LOAD_GLOBAL             14 (bool)
#             652 CALL                     1
#             660 POP_JUMP_IF_FALSE       25 (to 712)
#         >>  662 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 173         672 LOAD_ATTR               26 (_saferepr)
# 
# 171         692 LOAD_GLOBAL             14 (bool)
#             702 CALL                     1
#             710 JUMP_FORWARD             1 (to 714)
#         >>  712 LOAD_CONST               7 ('bool')
#         >>  714 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 173         724 LOAD_ATTR               26 (_saferepr)
# 
# 171         744 LOAD_FAST                6 (@py_assert3)
#             746 CALL                     1
#             754 LOAD_CONST               8 (('py0', 'py1', 'py2', 'py4'))
#             756 BUILD_CONST_KEY_MAP      4
#             758 BINARY_OP                6 (%)
#             762 STORE_FAST               7 (@py_format5)
#             764 LOAD_GLOBAL             29 (NULL + AssertionError)
#             774 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 173         784 LOAD_ATTR               30 (_format_explanation)
# 
# 171         804 LOAD_FAST                7 (@py_format5)
#             806 CALL                     1
#             814 CALL                     1
#             822 RAISE_VARARGS            1
#         >>  824 LOAD_CONST               9 (None)
#             826 STORE_FAST               6 (@py_assert3)
# 
# 174         828 LOAD_GLOBAL             13 (NULL + isinstance)
#             838 LOAD_FAST                5 (errors)
#             840 LOAD_GLOBAL             32 (list)
#             850 CALL                     2
#             858 STORE_FAST               6 (@py_assert3)
#             860 LOAD_FAST                6 (@py_assert3)
#             862 EXTENDED_ARG             1
#             864 POP_JUMP_IF_TRUE       302 (to 1470)
#             866 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 176         876 LOAD_ATTR               18 (_format_assertmsg)
# 
# 175         896 LOAD_FAST                1 (skill_class)
#             898 LOAD_ATTR                8 (__name__)
#             918 FORMAT_VALUE             0
#             920 LOAD_CONST              10 ('.validate() must return list as second element')
#             922 BUILD_STRING             2
# 
# 174         924 CALL                     1
#             932 LOAD_CONST               4 ('\n>assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}')
#             934 BINARY_OP                0 (+)
#             938 LOAD_CONST               5 ('isinstance')
#             940 LOAD_GLOBAL             21 (NULL + @py_builtins)
# 
# 176         950 LOAD_ATTR               22 (locals)
# 
# 174         970 CALL                     0
#             978 CONTAINS_OP              0
#             980 POP_JUMP_IF_TRUE        25 (to 1032)
#             982 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 176         992 LOAD_ATTR               24 (_should_repr_global_name)
# 
# 174        1012 LOAD_GLOBAL             12 (isinstance)
#            1022 CALL                     1
#            1030 POP_JUMP_IF_FALSE       25 (to 1082)
#         >> 1032 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 176        1042 LOAD_ATTR               26 (_saferepr)
# 
# 174        1062 LOAD_GLOBAL             12 (isinstance)
#            1072 CALL                     1
#            1080 JUMP_FORWARD             1 (to 1084)
#         >> 1082 LOAD_CONST               5 ('isinstance')
#         >> 1084 LOAD_CONST              11 ('errors')
#            1086 LOAD_GLOBAL             21 (NULL + @py_builtins)
# 
# 176        1096 LOAD_ATTR               22 (locals)
# 
# 174        1116 CALL                     0
#            1124 CONTAINS_OP              0
#            1126 POP_JUMP_IF_TRUE        21 (to 1170)
#            1128 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 176        1138 LOAD_ATTR               24 (_should_repr_global_name)
# 
# 174        1158 LOAD_FAST                5 (errors)
#            1160 CALL                     1
#            1168 POP_JUMP_IF_FALSE       21 (to 1212)
#         >> 1170 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 176        1180 LOAD_ATTR               26 (_saferepr)
# 
# 174        1200 LOAD_FAST                5 (errors)
#            1202 CALL                     1
#            1210 JUMP_FORWARD             1 (to 1214)
#         >> 1212 LOAD_CONST              11 ('errors')
#         >> 1214 LOAD_CONST              12 ('list')
#            1216 LOAD_GLOBAL             21 (NULL + @py_builtins)
# 
# 176        1226 LOAD_ATTR               22 (locals)
# 
# 174        1246 CALL                     0
#            1254 CONTAINS_OP              0
#            1256 POP_JUMP_IF_TRUE        25 (to 1308)
#            1258 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 176        1268 LOAD_ATTR               24 (_should_repr_global_name)
# 
# 174        1288 LOAD_GLOBAL             32 (list)
#            1298 CALL                     1
#            1306 POP_JUMP_IF_FALSE       25 (to 1358)
#         >> 1308 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 176        1318 LOAD_ATTR               26 (_saferepr)
# 
# 174        1338 LOAD_GLOBAL             32 (list)
#            1348 CALL                     1
#            1356 JUMP_FORWARD             1 (to 1360)
#         >> 1358 LOAD_CONST              12 ('list')
#         >> 1360 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 176        1370 LOAD_ATTR               26 (_saferepr)
# 
# 174        1390 LOAD_FAST                6 (@py_assert3)
#            1392 CALL                     1
#            1400 LOAD_CONST               8 (('py0', 'py1', 'py2', 'py4'))
#            1402 BUILD_CONST_KEY_MAP      4
#            1404 BINARY_OP                6 (%)
#            1408 STORE_FAST               7 (@py_format5)
#            1410 LOAD_GLOBAL             29 (NULL + AssertionError)
#            1420 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 176        1430 LOAD_ATTR               30 (_format_explanation)
# 
# 174        1450 LOAD_FAST                7 (@py_format5)
#            1452 CALL                     1
#            1460 CALL                     1
#            1468 RAISE_VARARGS            1
#         >> 1470 LOAD_CONST               9 (None)
#            1472 STORE_FAST               6 (@py_assert3)
#            1474 RETURN_CONST             9 (None)
#         >> 1476 PUSH_EXC_INFO
# 
# 177        1478 LOAD_GLOBAL             34 (Exception)
#            1488 CHECK_EXC_MATCH
#            1490 POP_JUMP_IF_FALSE       46 (to 1584)
#            1492 STORE_FAST               8 (e)
# 
# 178        1494 LOAD_GLOBAL              5 (NULL + pytest)
#            1504 LOAD_ATTR               36 (fail)
# 
# 179        1524 LOAD_FAST                1 (skill_class)
#            1526 LOAD_ATTR                8 (__name__)
#            1546 FORMAT_VALUE             0
#            1548 LOAD_CONST              13 ('.validate() raised exception with default config: ')
#            1550 LOAD_FAST                8 (e)
#            1552 FORMAT_VALUE             0
#            1554 BUILD_STRING             3
# 
# 178        1556 CALL                     1
#            1564 POP_TOP
#            1566 POP_EXCEPT
#            1568 LOAD_CONST               9 (None)
#            1570 STORE_FAST               8 (e)
#            1572 DELETE_FAST              8 (e)
#            1574 RETURN_CONST             9 (None)
#         >> 1576 LOAD_CONST               9 (None)
#            1578 STORE_FAST               8 (e)
#            1580 DELETE_FAST              8 (e)
#            1582 RERAISE                  1
# 
# 177     >> 1584 RERAISE                  0
#         >> 1586 COPY                     3
#            1588 POP_EXCEPT
#            1590 RERAISE                  1
# ExceptionTable:
#   142 to 1472 -> 1476 [0]
#   1476 to 1492 -> 1586 [1] lasti
#   1494 to 1564 -> 1576 [1] lasti
#   1576 to 1584 -> 1586 [1] lasti
# 
# Disassembly of <code object TestSkillRequiredFields at 0x73cd93b39a10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 183>:
# 183           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestSkillRequiredFields')
#               8 STORE_NAME               2 (__qualname__)
# 
# 184          10 LOAD_CONST               1 ('Test that skills have required configuration fields.')
#              12 STORE_NAME               3 (__doc__)
# 
# 186          14 LOAD_NAME                4 (pytest)
#              16 LOAD_ATTR               10 (mark)
#              36 LOAD_ATTR               13 (NULL|self + parametrize)
#              56 LOAD_CONST               2 ('skill_class')
#              58 LOAD_NAME                7 (ALL_SKILL_CLASSES)
#              60 CALL                     2
# 
# 187          68 LOAD_CONST               3 (<code object test_default_config_has_required_structure at 0x3aeca6c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 186>)
#              70 MAKE_FUNCTION            0
# 
# 186          72 CALL                     0
# 
# 187          80 STORE_NAME               8 (test_default_config_has_required_structure)
#              82 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_default_config_has_required_structure at 0x3aeca6c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 186>:
# 186           0 RESUME                   0
# 
# 189           2 PUSH_NULL
#               4 LOAD_FAST                1 (skill_class)
#               6 CALL                     0
#              14 STORE_FAST               2 (skill)
# 
# 190          16 LOAD_FAST                2 (skill)
#              18 LOAD_ATTR                1 (NULL|self + get_default_config)
#              38 CALL                     0
#              46 STORE_FAST               3 (default_config)
# 
# 193          48 BUILD_LIST               0
#              50 LOAD_CONST               1 (('auth', 'model', 'output'))
#              52 LIST_EXTEND              1
#              54 STORE_FAST               4 (common_optional_fields)
# 
# 196          56 LOAD_CONST               2 ('auth')
#              58 LOAD_FAST                3 (default_config)
#              60 CONTAINS_OP              0
#              62 EXTENDED_ARG             1
#              64 POP_JUMP_IF_FALSE      285 (to 636)
# 
# 197          66 LOAD_FAST                3 (default_config)
#              68 LOAD_CONST               2 ('auth')
#              70 BINARY_SUBSCR
#              74 STORE_FAST               5 (@py_assert1)
#              76 LOAD_GLOBAL              3 (NULL + isinstance)
#              86 LOAD_FAST                5 (@py_assert1)
#              88 LOAD_GLOBAL              4 (dict)
#              98 CALL                     2
#             106 STORE_FAST               6 (@py_assert4)
#             108 LOAD_FAST                6 (@py_assert4)
#             110 EXTENDED_ARG             1
#             112 POP_JUMP_IF_TRUE       257 (to 628)
#             114 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 199         124 LOAD_ATTR                8 (_format_assertmsg)
# 
# 198         144 LOAD_FAST                1 (skill_class)
#             146 LOAD_ATTR               10 (__name__)
#             166 FORMAT_VALUE             0
#             168 LOAD_CONST               3 (": 'auth' must be a dict")
#             170 BUILD_STRING             2
# 
# 197         172 CALL                     1
#             180 LOAD_CONST               4 ('\n>assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}')
#             182 BINARY_OP                0 (+)
#             186 LOAD_CONST               5 ('isinstance')
#             188 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
# 199         198 LOAD_ATTR               14 (locals)
# 
# 197         218 CALL                     0
#             226 CONTAINS_OP              0
#             228 POP_JUMP_IF_TRUE        25 (to 280)
#             230 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 199         240 LOAD_ATTR               16 (_should_repr_global_name)
# 
# 197         260 LOAD_GLOBAL              2 (isinstance)
#             270 CALL                     1
#             278 POP_JUMP_IF_FALSE       25 (to 330)
#         >>  280 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 199         290 LOAD_ATTR               18 (_saferepr)
# 
# 197         310 LOAD_GLOBAL              2 (isinstance)
#             320 CALL                     1
#             328 JUMP_FORWARD             1 (to 332)
#         >>  330 LOAD_CONST               5 ('isinstance')
#         >>  332 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 199         342 LOAD_ATTR               18 (_saferepr)
# 
# 197         362 LOAD_FAST                5 (@py_assert1)
#             364 CALL                     1
#             372 LOAD_CONST               6 ('dict')
#             374 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
# 199         384 LOAD_ATTR               14 (locals)
# 
# 197         404 CALL                     0
#             412 CONTAINS_OP              0
#             414 POP_JUMP_IF_TRUE        25 (to 466)
#             416 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 199         426 LOAD_ATTR               16 (_should_repr_global_name)
# 
# 197         446 LOAD_GLOBAL              4 (dict)
#             456 CALL                     1
#             464 POP_JUMP_IF_FALSE       25 (to 516)
#         >>  466 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 199         476 LOAD_ATTR               18 (_saferepr)
# 
# 197         496 LOAD_GLOBAL              4 (dict)
#             506 CALL                     1
#             514 JUMP_FORWARD             1 (to 518)
#         >>  516 LOAD_CONST               6 ('dict')
#         >>  518 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 199         528 LOAD_ATTR               18 (_saferepr)
# 
# 197         548 LOAD_FAST                6 (@py_assert4)
#             550 CALL                     1
#             558 LOAD_CONST               7 (('py0', 'py2', 'py3', 'py5'))
#             560 BUILD_CONST_KEY_MAP      4
#             562 BINARY_OP                6 (%)
#             566 STORE_FAST               7 (@py_format6)
#             568 LOAD_GLOBAL             21 (NULL + AssertionError)
#             578 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 199         588 LOAD_ATTR               22 (_format_explanation)
# 
# 197         608 LOAD_FAST                7 (@py_format6)
#             610 CALL                     1
#             618 CALL                     1
#             626 RAISE_VARARGS            1
#         >>  628 LOAD_CONST               8 (None)
#             630 COPY                     1
#             632 STORE_FAST               5 (@py_assert1)
#             634 STORE_FAST               6 (@py_assert4)
# 
# 201     >>  636 LOAD_CONST               9 ('model')
#             638 LOAD_FAST                3 (default_config)
#             640 CONTAINS_OP              0
#             642 EXTENDED_ARG             2
#             644 POP_JUMP_IF_FALSE      581 (to 1808)
# 
# 202         646 LOAD_FAST                3 (default_config)
#             648 LOAD_CONST               9 ('model')
#             650 BINARY_SUBSCR
#             654 STORE_FAST               5 (@py_assert1)
#             656 LOAD_GLOBAL              3 (NULL + isinstance)
#             666 LOAD_FAST                5 (@py_assert1)
#             668 LOAD_GLOBAL              4 (dict)
#             678 CALL                     2
#             686 STORE_FAST               6 (@py_assert4)
#             688 LOAD_FAST                6 (@py_assert4)
#             690 EXTENDED_ARG             1
#             692 POP_JUMP_IF_TRUE       257 (to 1208)
#             694 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 204         704 LOAD_ATTR                8 (_format_assertmsg)
# 
# 203         724 LOAD_FAST                1 (skill_class)
#             726 LOAD_ATTR               10 (__name__)
#             746 FORMAT_VALUE             0
#             748 LOAD_CONST              10 (": 'model' must be a dict")
#             750 BUILD_STRING             2
# 
# 202         752 CALL                     1
#             760 LOAD_CONST               4 ('\n>assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}')
#             762 BINARY_OP                0 (+)
#             766 LOAD_CONST               5 ('isinstance')
#             768 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
# 204         778 LOAD_ATTR               14 (locals)
# 
# 202         798 CALL                     0
#             806 CONTAINS_OP              0
#             808 POP_JUMP_IF_TRUE        25 (to 860)
#             810 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 204         820 LOAD_ATTR               16 (_should_repr_global_name)
# 
# 202         840 LOAD_GLOBAL              2 (isinstance)
#             850 CALL                     1
#             858 POP_JUMP_IF_FALSE       25 (to 910)
#         >>  860 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 204         870 LOAD_ATTR               18 (_saferepr)
# 
# 202         890 LOAD_GLOBAL              2 (isinstance)
#             900 CALL                     1
#             908 JUMP_FORWARD             1 (to 912)
#         >>  910 LOAD_CONST               5 ('isinstance')
#         >>  912 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 204         922 LOAD_ATTR               18 (_saferepr)
# 
# 202         942 LOAD_FAST                5 (@py_assert1)
#             944 CALL                     1
#             952 LOAD_CONST               6 ('dict')
#             954 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
# 204         964 LOAD_ATTR               14 (locals)
# 
# 202         984 CALL                     0
#             992 CONTAINS_OP              0
#             994 POP_JUMP_IF_TRUE        25 (to 1046)
#             996 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 204        1006 LOAD_ATTR               16 (_should_repr_global_name)
# 
# 202        1026 LOAD_GLOBAL              4 (dict)
#            1036 CALL                     1
#            1044 POP_JUMP_IF_FALSE       25 (to 1096)
#         >> 1046 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 204        1056 LOAD_ATTR               18 (_saferepr)
# 
# 202        1076 LOAD_GLOBAL              4 (dict)
#            1086 CALL                     1
#            1094 JUMP_FORWARD             1 (to 1098)
#         >> 1096 LOAD_CONST               6 ('dict')
#         >> 1098 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 204        1108 LOAD_ATTR               18 (_saferepr)
# 
# 202        1128 LOAD_FAST                6 (@py_assert4)
#            1130 CALL                     1
#            1138 LOAD_CONST               7 (('py0', 'py2', 'py3', 'py5'))
#            1140 BUILD_CONST_KEY_MAP      4
#            1142 BINARY_OP                6 (%)
#            1146 STORE_FAST               7 (@py_format6)
#            1148 LOAD_GLOBAL             21 (NULL + AssertionError)
#            1158 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 204        1168 LOAD_ATTR               22 (_format_explanation)
# 
# 202        1188 LOAD_FAST                7 (@py_format6)
#            1190 CALL                     1
#            1198 CALL                     1
#            1206 RAISE_VARARGS            1
#         >> 1208 LOAD_CONST               8 (None)
#            1210 COPY                     1
#            1212 STORE_FAST               5 (@py_assert1)
#            1214 STORE_FAST               6 (@py_assert4)
# 
# 206        1216 LOAD_CONST              11 ('rid')
#            1218 LOAD_FAST                3 (default_config)
#            1220 LOAD_CONST               9 ('model')
#            1222 BINARY_SUBSCR
#            1226 CONTAINS_OP              0
#            1228 EXTENDED_ARG             1
#            1230 POP_JUMP_IF_FALSE      288 (to 1808)
# 
# 207        1232 LOAD_FAST                3 (default_config)
#            1234 LOAD_CONST               9 ('model')
#            1236 BINARY_SUBSCR
#            1240 LOAD_CONST              11 ('rid')
#            1242 BINARY_SUBSCR
#            1246 STORE_FAST               5 (@py_assert1)
#            1248 LOAD_GLOBAL              3 (NULL + isinstance)
#            1258 LOAD_FAST                5 (@py_assert1)
#            1260 LOAD_GLOBAL             24 (str)
#            1270 CALL                     2
#            1278 STORE_FAST               6 (@py_assert4)
#            1280 LOAD_FAST                6 (@py_assert4)
#            1282 EXTENDED_ARG             1
#            1284 POP_JUMP_IF_TRUE       257 (to 1800)
#            1286 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 209        1296 LOAD_ATTR                8 (_format_assertmsg)
# 
# 208        1316 LOAD_FAST                1 (skill_class)
#            1318 LOAD_ATTR               10 (__name__)
#            1338 FORMAT_VALUE             0
#            1340 LOAD_CONST              12 (": 'model.rid' must be a string")
#            1342 BUILD_STRING             2
# 
# 207        1344 CALL                     1
#            1352 LOAD_CONST               4 ('\n>assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}')
#            1354 BINARY_OP                0 (+)
#            1358 LOAD_CONST               5 ('isinstance')
#            1360 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
# 209        1370 LOAD_ATTR               14 (locals)
# 
# 207        1390 CALL                     0
#            1398 CONTAINS_OP              0
#            1400 POP_JUMP_IF_TRUE        25 (to 1452)
#            1402 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 209        1412 LOAD_ATTR               16 (_should_repr_global_name)
# 
# 207        1432 LOAD_GLOBAL              2 (isinstance)
#            1442 CALL                     1
#            1450 POP_JUMP_IF_FALSE       25 (to 1502)
#         >> 1452 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 209        1462 LOAD_ATTR               18 (_saferepr)
# 
# 207        1482 LOAD_GLOBAL              2 (isinstance)
#            1492 CALL                     1
#            1500 JUMP_FORWARD             1 (to 1504)
#         >> 1502 LOAD_CONST               5 ('isinstance')
#         >> 1504 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 209        1514 LOAD_ATTR               18 (_saferepr)
# 
# 207        1534 LOAD_FAST                5 (@py_assert1)
#            1536 CALL                     1
#            1544 LOAD_CONST              13 ('str')
#            1546 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
# 209        1556 LOAD_ATTR               14 (locals)
# 
# 207        1576 CALL                     0
#            1584 CONTAINS_OP              0
#            1586 POP_JUMP_IF_TRUE        25 (to 1638)
#            1588 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 209        1598 LOAD_ATTR               16 (_should_repr_global_name)
# 
# 207        1618 LOAD_GLOBAL             24 (str)
#            1628 CALL                     1
#            1636 POP_JUMP_IF_FALSE       25 (to 1688)
#         >> 1638 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 209        1648 LOAD_ATTR               18 (_saferepr)
# 
# 207        1668 LOAD_GLOBAL             24 (str)
#            1678 CALL                     1
#            1686 JUMP_FORWARD             1 (to 1690)
#         >> 1688 LOAD_CONST              13 ('str')
#         >> 1690 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 209        1700 LOAD_ATTR               18 (_saferepr)
# 
# 207        1720 LOAD_FAST                6 (@py_assert4)
#            1722 CALL                     1
#            1730 LOAD_CONST               7 (('py0', 'py2', 'py3', 'py5'))
#            1732 BUILD_CONST_KEY_MAP      4
#            1734 BINARY_OP                6 (%)
#            1738 STORE_FAST               7 (@py_format6)
#            1740 LOAD_GLOBAL             21 (NULL + AssertionError)
#            1750 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 209        1760 LOAD_ATTR               22 (_format_explanation)
# 
# 207        1780 LOAD_FAST                7 (@py_format6)
#            1782 CALL                     1
#            1790 CALL                     1
#            1798 RAISE_VARARGS            1
#         >> 1800 LOAD_CONST               8 (None)
#            1802 COPY                     1
#            1804 STORE_FAST               5 (@py_assert1)
#            1806 STORE_FAST               6 (@py_assert4)
# 
# 211     >> 1808 LOAD_CONST              14 ('output')
#            1810 LOAD_FAST                3 (default_config)
#            1812 CONTAINS_OP              0
#            1814 EXTENDED_ARG             1
#            1816 POP_JUMP_IF_FALSE      286 (to 2390)
# 
# 212        1818 LOAD_FAST                3 (default_config)
#            1820 LOAD_CONST              14 ('output')
#            1822 BINARY_SUBSCR
#            1826 STORE_FAST               5 (@py_assert1)
#            1828 LOAD_GLOBAL              3 (NULL + isinstance)
#            1838 LOAD_FAST                5 (@py_assert1)
#            1840 LOAD_GLOBAL              4 (dict)
#            1850 CALL                     2
#            1858 STORE_FAST               6 (@py_assert4)
#            1860 LOAD_FAST                6 (@py_assert4)
#            1862 EXTENDED_ARG             1
#            1864 POP_JUMP_IF_TRUE       257 (to 2380)
#            1866 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 214        1876 LOAD_ATTR                8 (_format_assertmsg)
# 
# 213        1896 LOAD_FAST                1 (skill_class)
#            1898 LOAD_ATTR               10 (__name__)
#            1918 FORMAT_VALUE             0
#            1920 LOAD_CONST              15 (": 'output' must be a dict")
#            1922 BUILD_STRING             2
# 
# 212        1924 CALL                     1
#            1932 LOAD_CONST               4 ('\n>assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}')
#            1934 BINARY_OP                0 (+)
#            1938 LOAD_CONST               5 ('isinstance')
#            1940 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
# 214        1950 LOAD_ATTR               14 (locals)
# 
# 212        1970 CALL                     0
#            1978 CONTAINS_OP              0
#            1980 POP_JUMP_IF_TRUE        25 (to 2032)
#            1982 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 214        1992 LOAD_ATTR               16 (_should_repr_global_name)
# 
# 212        2012 LOAD_GLOBAL              2 (isinstance)
#            2022 CALL                     1
#            2030 POP_JUMP_IF_FALSE       25 (to 2082)
#         >> 2032 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 214        2042 LOAD_ATTR               18 (_saferepr)
# 
# 212        2062 LOAD_GLOBAL              2 (isinstance)
#            2072 CALL                     1
#            2080 JUMP_FORWARD             1 (to 2084)
#         >> 2082 LOAD_CONST               5 ('isinstance')
#         >> 2084 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 214        2094 LOAD_ATTR               18 (_saferepr)
# 
# 212        2114 LOAD_FAST                5 (@py_assert1)
#            2116 CALL                     1
#            2124 LOAD_CONST               6 ('dict')
#            2126 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
# 214        2136 LOAD_ATTR               14 (locals)
# 
# 212        2156 CALL                     0
#            2164 CONTAINS_OP              0
#            2166 POP_JUMP_IF_TRUE        25 (to 2218)
#            2168 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 214        2178 LOAD_ATTR               16 (_should_repr_global_name)
# 
# 212        2198 LOAD_GLOBAL              4 (dict)
#            2208 CALL                     1
#            2216 POP_JUMP_IF_FALSE       25 (to 2268)
#         >> 2218 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 214        2228 LOAD_ATTR               18 (_saferepr)
# 
# 212        2248 LOAD_GLOBAL              4 (dict)
#            2258 CALL                     1
#            2266 JUMP_FORWARD             1 (to 2270)
#         >> 2268 LOAD_CONST               6 ('dict')
#         >> 2270 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 214        2280 LOAD_ATTR               18 (_saferepr)
# 
# 212        2300 LOAD_FAST                6 (@py_assert4)
#            2302 CALL                     1
#            2310 LOAD_CONST               7 (('py0', 'py2', 'py3', 'py5'))
#            2312 BUILD_CONST_KEY_MAP      4
#            2314 BINARY_OP                6 (%)
#            2318 STORE_FAST               7 (@py_format6)
#            2320 LOAD_GLOBAL             21 (NULL + AssertionError)
#            2330 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 214        2340 LOAD_ATTR               22 (_format_explanation)
# 
# 212        2360 LOAD_FAST                7 (@py_format6)
#            2362 CALL                     1
#            2370 CALL                     1
#            2378 RAISE_VARARGS            1
#         >> 2380 LOAD_CONST               8 (None)
#            2382 COPY                     1
#            2384 STORE_FAST               5 (@py_assert1)
#            2386 STORE_FAST               6 (@py_assert4)
#            2388 RETURN_CONST             8 (None)
# 
# 211     >> 2390 RETURN_CONST             8 (None)
# 
# Disassembly of <code object TestSpecificSkillConfigs at 0x73cd93b44d40, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 217>:
# 217           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestSpecificSkillConfigs')
#               8 STORE_NAME               2 (__qualname__)
# 
# 218          10 LOAD_CONST               1 ('Test specific skill configurations that were reported as buggy.')
#              12 STORE_NAME               3 (__doc__)
# 
# 220          14 LOAD_CONST               2 (<code object test_dudv_curve_has_buses at 0x3aecb0e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 220>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_dudv_curve_has_buses)
# 
# 228          20 LOAD_CONST               3 (<code object test_param_scan_has_required_fields at 0x3aecbe70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 228>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_param_scan_has_required_fields)
# 
# 237          26 LOAD_CONST               4 (<code object test_maintenance_security_has_maintenance at 0x3aecc5f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 237>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_maintenance_security_has_maintenance)
# 
# 244          32 LOAD_CONST               5 (<code object test_reactive_compensation_has_weak_buses_or_vsi at 0x3aee2dd0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 244>)
#              34 MAKE_FUNCTION            0
#              36 STORE_NAME               7 (test_reactive_compensation_has_weak_buses_or_vsi)
# 
# 252          38 LOAD_CONST               6 (<code object test_result_compare_has_sources at 0x3aecd0e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 252>)
#              40 MAKE_FUNCTION            0
#              42 STORE_NAME               8 (test_result_compare_has_sources)
# 
# 259          44 LOAD_CONST               7 (<code object test_visualize_has_source at 0x3aecd580, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 259>)
#              46 MAKE_FUNCTION            0
#              48 STORE_NAME               9 (test_visualize_has_source)
# 
# 266          50 LOAD_CONST               8 (<code object test_waveform_export_has_source_and_export at 0x3afa6d80, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 266>)
#              52 MAKE_FUNCTION            0
#              54 STORE_NAME              10 (test_waveform_export_has_source_and_export)
# 
# 273          56 LOAD_CONST               9 (<code object test_compare_visualization_has_sources at 0x3aecca90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 273>)
#              58 MAKE_FUNCTION            0
#              60 STORE_NAME              11 (test_compare_visualization_has_sources)
# 
# 280          62 LOAD_CONST              10 (<code object test_comtrade_export_has_source_and_export at 0x3aec4000, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 280>)
#              64 MAKE_FUNCTION            0
#              66 STORE_NAME              12 (test_comtrade_export_has_source_and_export)
# 
# 287          68 LOAD_CONST              11 (<code object test_auto_loop_breaker_has_algorithm at 0x3af937b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 287>)
#              70 MAKE_FUNCTION            0
#              72 STORE_NAME              13 (test_auto_loop_breaker_has_algorithm)
# 
# 293          74 LOAD_CONST              12 (<code object test_model_parameter_extractor_has_extraction at 0x3af97180, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 293>)
#              76 MAKE_FUNCTION            0
#              78 STORE_NAME              14 (test_model_parameter_extractor_has_extraction)
# 
# 299          80 LOAD_CONST              13 (<code object test_report_generator_has_report at 0x3ae76f20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 299>)
#              82 MAKE_FUNCTION            0
#              84 STORE_NAME              15 (test_report_generator_has_report)
# 
# 305          86 LOAD_CONST              14 (<code object test_renewable_integration_has_renewable at 0x3aeb9bc0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 305>)
#              88 MAKE_FUNCTION            0
#              90 STORE_NAME              16 (test_renewable_integration_has_renewable)
# 
# 311          92 LOAD_CONST              15 (<code object test_orthogonal_sensitivity_has_parameters_and_target at 0x3aec5210, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 311>)
#              94 MAKE_FUNCTION            0
#              96 STORE_NAME              17 (test_orthogonal_sensitivity_has_parameters_and_target)
# 
# 318          98 LOAD_CONST              16 (<code object test_component_catalog_has_filters_and_options at 0x3aea9820, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 318>)
#             100 MAKE_FUNCTION            0
#             102 STORE_NAME              18 (test_component_catalog_has_filters_and_options)
# 
# 325         104 LOAD_CONST              17 (<code object test_model_builder_has_workflow_and_base_model at 0x3aece640, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 325>)
#             106 MAKE_FUNCTION            0
#             108 STORE_NAME              19 (test_model_builder_has_workflow_and_base_model)
#             110 RETURN_CONST            18 (None)
# 
# Disassembly of <code object test_dudv_curve_has_buses at 0x3aecb0e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 220>:
# 220           0 RESUME                   0
# 
# 222           2 LOAD_GLOBAL              1 (NULL + DUDVCurveSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 223          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
# 224          54 LOAD_CONST               1 ('buses')
#              56 STORE_FAST               3 (@py_assert0)
#              58 LOAD_FAST                3 (@py_assert0)
#              60 LOAD_FAST                2 (config)
#              62 CONTAINS_OP              0
#              64 STORE_FAST               4 (@py_assert2)
#              66 LOAD_FAST                4 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       175 (to 420)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               2 (('in',))
#             102 LOAD_FAST                4 (@py_assert2)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             108 LOAD_FAST                3 (@py_assert0)
#             110 LOAD_FAST                2 (config)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_saferepr)
#             152 LOAD_FAST                3 (@py_assert0)
#             154 CALL                     1
#             162 LOAD_CONST               4 ('config')
#             164 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             174 LOAD_ATTR               12 (locals)
#             194 CALL                     0
#             202 CONTAINS_OP              0
#             204 POP_JUMP_IF_TRUE        21 (to 248)
#             206 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             216 LOAD_ATTR               14 (_should_repr_global_name)
#             236 LOAD_FAST                2 (config)
#             238 CALL                     1
#             246 POP_JUMP_IF_FALSE       21 (to 290)
#         >>  248 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             258 LOAD_ATTR                8 (_saferepr)
#             278 LOAD_FAST                2 (config)
#             280 CALL                     1
#             288 JUMP_FORWARD             1 (to 292)
#         >>  290 LOAD_CONST               4 ('config')
#         >>  292 LOAD_CONST               5 (('py1', 'py3'))
#             294 BUILD_CONST_KEY_MAP      2
#             296 BINARY_OP                6 (%)
#             300 STORE_FAST               5 (@py_format4)
#             302 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             312 LOAD_ATTR               16 (_format_assertmsg)
#             332 LOAD_CONST               6 ("dudv_curve must have 'buses' field")
#             334 CALL                     1
#             342 LOAD_CONST               7 ('\n>assert %(py5)s')
#             344 BINARY_OP                0 (+)
#             348 LOAD_CONST               8 ('py5')
#             350 LOAD_FAST                5 (@py_format4)
#             352 BUILD_MAP                1
#             354 BINARY_OP                6 (%)
#             358 STORE_FAST               6 (@py_format6)
#             360 LOAD_GLOBAL             19 (NULL + AssertionError)
#             370 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             380 LOAD_ATTR               20 (_format_explanation)
#             400 LOAD_FAST                6 (@py_format6)
#             402 CALL                     1
#             410 CALL                     1
#             418 RAISE_VARARGS            1
#         >>  420 LOAD_CONST               9 (None)
#             422 COPY                     1
#             424 STORE_FAST               3 (@py_assert0)
#             426 STORE_FAST               4 (@py_assert2)
# 
# 225         428 LOAD_FAST                2 (config)
#             430 LOAD_CONST               1 ('buses')
#             432 BINARY_SUBSCR
#             436 STORE_FAST               7 (@py_assert1)
#             438 LOAD_GLOBAL             23 (NULL + isinstance)
#             448 LOAD_FAST                7 (@py_assert1)
#             450 LOAD_GLOBAL             24 (list)
#             460 CALL                     2
#             468 STORE_FAST               8 (@py_assert4)
#             470 LOAD_FAST                8 (@py_assert4)
#             472 POP_JUMP_IF_TRUE       244 (to 962)
#             474 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             484 LOAD_ATTR               16 (_format_assertmsg)
#             504 LOAD_CONST              10 ('buses must be a list')
#             506 CALL                     1
#             514 LOAD_CONST              11 ('\n>assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}')
#             516 BINARY_OP                0 (+)
#             520 LOAD_CONST              12 ('isinstance')
#             522 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             532 LOAD_ATTR               12 (locals)
#             552 CALL                     0
#             560 CONTAINS_OP              0
#             562 POP_JUMP_IF_TRUE        25 (to 614)
#             564 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             574 LOAD_ATTR               14 (_should_repr_global_name)
#             594 LOAD_GLOBAL             22 (isinstance)
#             604 CALL                     1
#             612 POP_JUMP_IF_FALSE       25 (to 664)
#         >>  614 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             624 LOAD_ATTR                8 (_saferepr)
#             644 LOAD_GLOBAL             22 (isinstance)
#             654 CALL                     1
#             662 JUMP_FORWARD             1 (to 666)
#         >>  664 LOAD_CONST              12 ('isinstance')
#         >>  666 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             676 LOAD_ATTR                8 (_saferepr)
#             696 LOAD_FAST                7 (@py_assert1)
#             698 CALL                     1
#             706 LOAD_CONST              13 ('list')
#             708 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             718 LOAD_ATTR               12 (locals)
#             738 CALL                     0
#             746 CONTAINS_OP              0
#             748 POP_JUMP_IF_TRUE        25 (to 800)
#             750 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             760 LOAD_ATTR               14 (_should_repr_global_name)
#             780 LOAD_GLOBAL             24 (list)
#             790 CALL                     1
#             798 POP_JUMP_IF_FALSE       25 (to 850)
#         >>  800 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             810 LOAD_ATTR                8 (_saferepr)
#             830 LOAD_GLOBAL             24 (list)
#             840 CALL                     1
#             848 JUMP_FORWARD             1 (to 852)
#         >>  850 LOAD_CONST              13 ('list')
#         >>  852 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             862 LOAD_ATTR                8 (_saferepr)
#             882 LOAD_FAST                8 (@py_assert4)
#             884 CALL                     1
#             892 LOAD_CONST              14 (('py0', 'py2', 'py3', 'py5'))
#             894 BUILD_CONST_KEY_MAP      4
#             896 BINARY_OP                6 (%)
#             900 STORE_FAST               6 (@py_format6)
#             902 LOAD_GLOBAL             19 (NULL + AssertionError)
#             912 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             922 LOAD_ATTR               20 (_format_explanation)
#             942 LOAD_FAST                6 (@py_format6)
#             944 CALL                     1
#             952 CALL                     1
#             960 RAISE_VARARGS            1
#         >>  962 LOAD_CONST               9 (None)
#             964 COPY                     1
#             966 STORE_FAST               7 (@py_assert1)
#             968 STORE_FAST               8 (@py_assert4)
# 
# 226         970 LOAD_FAST                2 (config)
#             972 LOAD_CONST               1 ('buses')
#             974 BINARY_SUBSCR
#             978 STORE_FAST               7 (@py_assert1)
#             980 LOAD_GLOBAL             27 (NULL + len)
#             990 LOAD_FAST                7 (@py_assert1)
#             992 CALL                     1
#            1000 STORE_FAST               9 (@py_assert3)
#            1002 LOAD_CONST              15 (0)
#            1004 STORE_FAST              10 (@py_assert6)
#            1006 LOAD_FAST                9 (@py_assert3)
#            1008 LOAD_FAST               10 (@py_assert6)
#            1010 COMPARE_OP              68 (>)
#            1014 STORE_FAST              11 (@py_assert5)
#            1016 LOAD_FAST               11 (@py_assert5)
#            1018 POP_JUMP_IF_TRUE       223 (to 1466)
#            1020 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1030 LOAD_ATTR                6 (_call_reprcompare)
#            1050 LOAD_CONST              16 (('>',))
#            1052 LOAD_FAST               11 (@py_assert5)
#            1054 BUILD_TUPLE              1
#            1056 LOAD_CONST              17 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} > %(py7)s',))
#            1058 LOAD_FAST                9 (@py_assert3)
#            1060 LOAD_FAST               10 (@py_assert6)
#            1062 BUILD_TUPLE              2
#            1064 CALL                     4
#            1072 LOAD_CONST              18 ('len')
#            1074 LOAD_GLOBAL             11 (NULL + @py_builtins)
#            1084 LOAD_ATTR               12 (locals)
#            1104 CALL                     0
#            1112 CONTAINS_OP              0
#            1114 POP_JUMP_IF_TRUE        25 (to 1166)
#            1116 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1126 LOAD_ATTR               14 (_should_repr_global_name)
#            1146 LOAD_GLOBAL             26 (len)
#            1156 CALL                     1
#            1164 POP_JUMP_IF_FALSE       25 (to 1216)
#         >> 1166 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1176 LOAD_ATTR                8 (_saferepr)
#            1196 LOAD_GLOBAL             26 (len)
#            1206 CALL                     1
#            1214 JUMP_FORWARD             1 (to 1218)
#         >> 1216 LOAD_CONST              18 ('len')
#         >> 1218 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1228 LOAD_ATTR                8 (_saferepr)
#            1248 LOAD_FAST                7 (@py_assert1)
#            1250 CALL                     1
#            1258 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1268 LOAD_ATTR                8 (_saferepr)
#            1288 LOAD_FAST                9 (@py_assert3)
#            1290 CALL                     1
#            1298 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1308 LOAD_ATTR                8 (_saferepr)
#            1328 LOAD_FAST               10 (@py_assert6)
#            1330 CALL                     1
#            1338 LOAD_CONST              19 (('py0', 'py2', 'py4', 'py7'))
#            1340 BUILD_CONST_KEY_MAP      4
#            1342 BINARY_OP                6 (%)
#            1346 STORE_FAST              12 (@py_format8)
#            1348 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1358 LOAD_ATTR               16 (_format_assertmsg)
#            1378 LOAD_CONST              20 ('buses should have example values')
#            1380 CALL                     1
#            1388 LOAD_CONST              21 ('\n>assert %(py9)s')
#            1390 BINARY_OP                0 (+)
#            1394 LOAD_CONST              22 ('py9')
#            1396 LOAD_FAST               12 (@py_format8)
#            1398 BUILD_MAP                1
#            1400 BINARY_OP                6 (%)
#            1404 STORE_FAST              13 (@py_format10)
#            1406 LOAD_GLOBAL             19 (NULL + AssertionError)
#            1416 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1426 LOAD_ATTR               20 (_format_explanation)
#            1446 LOAD_FAST               13 (@py_format10)
#            1448 CALL                     1
#            1456 CALL                     1
#            1464 RAISE_VARARGS            1
#         >> 1466 LOAD_CONST               9 (None)
#            1468 COPY                     1
#            1470 STORE_FAST               7 (@py_assert1)
#            1472 COPY                     1
#            1474 STORE_FAST               9 (@py_assert3)
#            1476 COPY                     1
#            1478 STORE_FAST              11 (@py_assert5)
#            1480 STORE_FAST              10 (@py_assert6)
#            1482 RETURN_CONST             9 (None)
# 
# Disassembly of <code object test_param_scan_has_required_fields at 0x3aecbe70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 228>:
# 228           0 RESUME                   0
# 
# 230           2 LOAD_GLOBAL              1 (NULL + ParamScanSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 231          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
# 232          54 LOAD_CONST               1 ('component')
#              56 STORE_FAST               3 (@py_assert0)
#              58 LOAD_FAST                3 (@py_assert0)
#              60 LOAD_FAST                2 (config)
#              62 CONTAINS_OP              0
#              64 STORE_FAST               4 (@py_assert2)
#              66 LOAD_FAST                4 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       175 (to 420)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               2 (('in',))
#             102 LOAD_FAST                4 (@py_assert2)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             108 LOAD_FAST                3 (@py_assert0)
#             110 LOAD_FAST                2 (config)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_saferepr)
#             152 LOAD_FAST                3 (@py_assert0)
#             154 CALL                     1
#             162 LOAD_CONST               4 ('config')
#             164 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             174 LOAD_ATTR               12 (locals)
#             194 CALL                     0
#             202 CONTAINS_OP              0
#             204 POP_JUMP_IF_TRUE        21 (to 248)
#             206 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             216 LOAD_ATTR               14 (_should_repr_global_name)
#             236 LOAD_FAST                2 (config)
#             238 CALL                     1
#             246 POP_JUMP_IF_FALSE       21 (to 290)
#         >>  248 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             258 LOAD_ATTR                8 (_saferepr)
#             278 LOAD_FAST                2 (config)
#             280 CALL                     1
#             288 JUMP_FORWARD             1 (to 292)
#         >>  290 LOAD_CONST               4 ('config')
#         >>  292 LOAD_CONST               5 (('py1', 'py3'))
#             294 BUILD_CONST_KEY_MAP      2
#             296 BINARY_OP                6 (%)
#             300 STORE_FAST               5 (@py_format4)
#             302 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             312 LOAD_ATTR               16 (_format_assertmsg)
#             332 LOAD_CONST               6 ("param_scan must have 'component' field")
#             334 CALL                     1
#             342 LOAD_CONST               7 ('\n>assert %(py5)s')
#             344 BINARY_OP                0 (+)
#             348 LOAD_CONST               8 ('py5')
#             350 LOAD_FAST                5 (@py_format4)
#             352 BUILD_MAP                1
#             354 BINARY_OP                6 (%)
#             358 STORE_FAST               6 (@py_format6)
#             360 LOAD_GLOBAL             19 (NULL + AssertionError)
#             370 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             380 LOAD_ATTR               20 (_format_explanation)
#             400 LOAD_FAST                6 (@py_format6)
#             402 CALL                     1
#             410 CALL                     1
#             418 RAISE_VARARGS            1
#         >>  420 LOAD_CONST               9 (None)
#             422 COPY                     1
#             424 STORE_FAST               3 (@py_assert0)
#             426 STORE_FAST               4 (@py_assert2)
# 
# 233         428 LOAD_CONST              10 ('parameter')
#             430 STORE_FAST               3 (@py_assert0)
#             432 LOAD_FAST                3 (@py_assert0)
#             434 LOAD_FAST                2 (config)
#             436 CONTAINS_OP              0
#             438 STORE_FAST               4 (@py_assert2)
#             440 LOAD_FAST                4 (@py_assert2)
#             442 POP_JUMP_IF_TRUE       175 (to 794)
#             444 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             454 LOAD_ATTR                6 (_call_reprcompare)
#             474 LOAD_CONST               2 (('in',))
#             476 LOAD_FAST                4 (@py_assert2)
#             478 BUILD_TUPLE              1
#             480 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             482 LOAD_FAST                3 (@py_assert0)
#             484 LOAD_FAST                2 (config)
#             486 BUILD_TUPLE              2
#             488 CALL                     4
#             496 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             506 LOAD_ATTR                8 (_saferepr)
#             526 LOAD_FAST                3 (@py_assert0)
#             528 CALL                     1
#             536 LOAD_CONST               4 ('config')
#             538 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             548 LOAD_ATTR               12 (locals)
#             568 CALL                     0
#             576 CONTAINS_OP              0
#             578 POP_JUMP_IF_TRUE        21 (to 622)
#             580 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             590 LOAD_ATTR               14 (_should_repr_global_name)
#             610 LOAD_FAST                2 (config)
#             612 CALL                     1
#             620 POP_JUMP_IF_FALSE       21 (to 664)
#         >>  622 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             632 LOAD_ATTR                8 (_saferepr)
#             652 LOAD_FAST                2 (config)
#             654 CALL                     1
#             662 JUMP_FORWARD             1 (to 666)
#         >>  664 LOAD_CONST               4 ('config')
#         >>  666 LOAD_CONST               5 (('py1', 'py3'))
#             668 BUILD_CONST_KEY_MAP      2
#             670 BINARY_OP                6 (%)
#             674 STORE_FAST               5 (@py_format4)
#             676 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             686 LOAD_ATTR               16 (_format_assertmsg)
#             706 LOAD_CONST              11 ("param_scan must have 'parameter' field")
#             708 CALL                     1
#             716 LOAD_CONST               7 ('\n>assert %(py5)s')
#             718 BINARY_OP                0 (+)
#             722 LOAD_CONST               8 ('py5')
#             724 LOAD_FAST                5 (@py_format4)
#             726 BUILD_MAP                1
#             728 BINARY_OP                6 (%)
#             732 STORE_FAST               6 (@py_format6)
#             734 LOAD_GLOBAL             19 (NULL + AssertionError)
#             744 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             754 LOAD_ATTR               20 (_format_explanation)
#             774 LOAD_FAST                6 (@py_format6)
#             776 CALL                     1
#             784 CALL                     1
#             792 RAISE_VARARGS            1
#         >>  794 LOAD_CONST               9 (None)
#             796 COPY                     1
#             798 STORE_FAST               3 (@py_assert0)
#             800 STORE_FAST               4 (@py_assert2)
# 
# 234         802 LOAD_CONST              12 ('values')
#             804 STORE_FAST               3 (@py_assert0)
#             806 LOAD_FAST                3 (@py_assert0)
#             808 LOAD_FAST                2 (config)
#             810 CONTAINS_OP              0
#             812 STORE_FAST               4 (@py_assert2)
#             814 LOAD_FAST                4 (@py_assert2)
#             816 POP_JUMP_IF_TRUE       175 (to 1168)
#             818 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             828 LOAD_ATTR                6 (_call_reprcompare)
#             848 LOAD_CONST               2 (('in',))
#             850 LOAD_FAST                4 (@py_assert2)
#             852 BUILD_TUPLE              1
#             854 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             856 LOAD_FAST                3 (@py_assert0)
#             858 LOAD_FAST                2 (config)
#             860 BUILD_TUPLE              2
#             862 CALL                     4
#             870 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             880 LOAD_ATTR                8 (_saferepr)
#             900 LOAD_FAST                3 (@py_assert0)
#             902 CALL                     1
#             910 LOAD_CONST               4 ('config')
#             912 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             922 LOAD_ATTR               12 (locals)
#             942 CALL                     0
#             950 CONTAINS_OP              0
#             952 POP_JUMP_IF_TRUE        21 (to 996)
#             954 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             964 LOAD_ATTR               14 (_should_repr_global_name)
#             984 LOAD_FAST                2 (config)
#             986 CALL                     1
#             994 POP_JUMP_IF_FALSE       21 (to 1038)
#         >>  996 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1006 LOAD_ATTR                8 (_saferepr)
#            1026 LOAD_FAST                2 (config)
#            1028 CALL                     1
#            1036 JUMP_FORWARD             1 (to 1040)
#         >> 1038 LOAD_CONST               4 ('config')
#         >> 1040 LOAD_CONST               5 (('py1', 'py3'))
#            1042 BUILD_CONST_KEY_MAP      2
#            1044 BINARY_OP                6 (%)
#            1048 STORE_FAST               5 (@py_format4)
#            1050 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1060 LOAD_ATTR               16 (_format_assertmsg)
#            1080 LOAD_CONST              13 ("param_scan must have 'values' field")
#            1082 CALL                     1
#            1090 LOAD_CONST               7 ('\n>assert %(py5)s')
#            1092 BINARY_OP                0 (+)
#            1096 LOAD_CONST               8 ('py5')
#            1098 LOAD_FAST                5 (@py_format4)
#            1100 BUILD_MAP                1
#            1102 BINARY_OP                6 (%)
#            1106 STORE_FAST               6 (@py_format6)
#            1108 LOAD_GLOBAL             19 (NULL + AssertionError)
#            1118 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1128 LOAD_ATTR               20 (_format_explanation)
#            1148 LOAD_FAST                6 (@py_format6)
#            1150 CALL                     1
#            1158 CALL                     1
#            1166 RAISE_VARARGS            1
#         >> 1168 LOAD_CONST               9 (None)
#            1170 COPY                     1
#            1172 STORE_FAST               3 (@py_assert0)
#            1174 STORE_FAST               4 (@py_assert2)
# 
# 235        1176 LOAD_FAST                2 (config)
#            1178 LOAD_CONST              12 ('values')
#            1180 BINARY_SUBSCR
#            1184 STORE_FAST               7 (@py_assert1)
#            1186 LOAD_GLOBAL             23 (NULL + isinstance)
#            1196 LOAD_FAST                7 (@py_assert1)
#            1198 LOAD_GLOBAL             24 (list)
#            1208 CALL                     2
#            1216 STORE_FAST               8 (@py_assert4)
#            1218 LOAD_FAST                8 (@py_assert4)
#            1220 POP_JUMP_IF_TRUE       244 (to 1710)
#            1222 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1232 LOAD_ATTR               16 (_format_assertmsg)
#            1252 LOAD_CONST              14 ('values must be a list')
#            1254 CALL                     1
#            1262 LOAD_CONST              15 ('\n>assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}')
#            1264 BINARY_OP                0 (+)
#            1268 LOAD_CONST              16 ('isinstance')
#            1270 LOAD_GLOBAL             11 (NULL + @py_builtins)
#            1280 LOAD_ATTR               12 (locals)
#            1300 CALL                     0
#            1308 CONTAINS_OP              0
#            1310 POP_JUMP_IF_TRUE        25 (to 1362)
#            1312 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1322 LOAD_ATTR               14 (_should_repr_global_name)
#            1342 LOAD_GLOBAL             22 (isinstance)
#            1352 CALL                     1
#            1360 POP_JUMP_IF_FALSE       25 (to 1412)
#         >> 1362 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1372 LOAD_ATTR                8 (_saferepr)
#            1392 LOAD_GLOBAL             22 (isinstance)
#            1402 CALL                     1
#            1410 JUMP_FORWARD             1 (to 1414)
#         >> 1412 LOAD_CONST              16 ('isinstance')
#         >> 1414 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1424 LOAD_ATTR                8 (_saferepr)
#            1444 LOAD_FAST                7 (@py_assert1)
#            1446 CALL                     1
#            1454 LOAD_CONST              17 ('list')
#            1456 LOAD_GLOBAL             11 (NULL + @py_builtins)
#            1466 LOAD_ATTR               12 (locals)
#            1486 CALL                     0
#            1494 CONTAINS_OP              0
#            1496 POP_JUMP_IF_TRUE        25 (to 1548)
#            1498 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1508 LOAD_ATTR               14 (_should_repr_global_name)
#            1528 LOAD_GLOBAL             24 (list)
#            1538 CALL                     1
#            1546 POP_JUMP_IF_FALSE       25 (to 1598)
#         >> 1548 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1558 LOAD_ATTR                8 (_saferepr)
#            1578 LOAD_GLOBAL             24 (list)
#            1588 CALL                     1
#            1596 JUMP_FORWARD             1 (to 1600)
#         >> 1598 LOAD_CONST              17 ('list')
#         >> 1600 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1610 LOAD_ATTR                8 (_saferepr)
#            1630 LOAD_FAST                8 (@py_assert4)
#            1632 CALL                     1
#            1640 LOAD_CONST              18 (('py0', 'py2', 'py3', 'py5'))
#            1642 BUILD_CONST_KEY_MAP      4
#            1644 BINARY_OP                6 (%)
#            1648 STORE_FAST               6 (@py_format6)
#            1650 LOAD_GLOBAL             19 (NULL + AssertionError)
#            1660 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1670 LOAD_ATTR               20 (_format_explanation)
#            1690 LOAD_FAST                6 (@py_format6)
#            1692 CALL                     1
#            1700 CALL                     1
#            1708 RAISE_VARARGS            1
#         >> 1710 LOAD_CONST               9 (None)
#            1712 COPY                     1
#            1714 STORE_FAST               7 (@py_assert1)
#            1716 STORE_FAST               8 (@py_assert4)
#            1718 RETURN_CONST             9 (None)
# 
# Disassembly of <code object test_maintenance_security_has_maintenance at 0x3aecc5f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 237>:
# 237           0 RESUME                   0
# 
# 239           2 LOAD_GLOBAL              1 (NULL + MaintenanceSecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 240          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
# 241          54 LOAD_CONST               1 ('maintenance')
#              56 STORE_FAST               3 (@py_assert0)
#              58 LOAD_FAST                3 (@py_assert0)
#              60 LOAD_FAST                2 (config)
#              62 CONTAINS_OP              0
#              64 STORE_FAST               4 (@py_assert2)
#              66 LOAD_FAST                4 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       175 (to 420)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               2 (('in',))
#             102 LOAD_FAST                4 (@py_assert2)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             108 LOAD_FAST                3 (@py_assert0)
#             110 LOAD_FAST                2 (config)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_saferepr)
#             152 LOAD_FAST                3 (@py_assert0)
#             154 CALL                     1
#             162 LOAD_CONST               4 ('config')
#             164 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             174 LOAD_ATTR               12 (locals)
#             194 CALL                     0
#             202 CONTAINS_OP              0
#             204 POP_JUMP_IF_TRUE        21 (to 248)
#             206 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             216 LOAD_ATTR               14 (_should_repr_global_name)
#             236 LOAD_FAST                2 (config)
#             238 CALL                     1
#             246 POP_JUMP_IF_FALSE       21 (to 290)
#         >>  248 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             258 LOAD_ATTR                8 (_saferepr)
#             278 LOAD_FAST                2 (config)
#             280 CALL                     1
#             288 JUMP_FORWARD             1 (to 292)
#         >>  290 LOAD_CONST               4 ('config')
#         >>  292 LOAD_CONST               5 (('py1', 'py3'))
#             294 BUILD_CONST_KEY_MAP      2
#             296 BINARY_OP                6 (%)
#             300 STORE_FAST               5 (@py_format4)
#             302 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             312 LOAD_ATTR               16 (_format_assertmsg)
#             332 LOAD_CONST               6 ("maintenance_security must have 'maintenance' field")
#             334 CALL                     1
#             342 LOAD_CONST               7 ('\n>assert %(py5)s')
#             344 BINARY_OP                0 (+)
#             348 LOAD_CONST               8 ('py5')
#             350 LOAD_FAST                5 (@py_format4)
#             352 BUILD_MAP                1
#             354 BINARY_OP                6 (%)
#             358 STORE_FAST               6 (@py_format6)
#             360 LOAD_GLOBAL             19 (NULL + AssertionError)
#             370 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             380 LOAD_ATTR               20 (_format_explanation)
#             400 LOAD_FAST                6 (@py_format6)
#             402 CALL                     1
#             410 CALL                     1
#             418 RAISE_VARARGS            1
#         >>  420 LOAD_CONST               9 (None)
#             422 COPY                     1
#             424 STORE_FAST               3 (@py_assert0)
#             426 STORE_FAST               4 (@py_assert2)
# 
# 242         428 LOAD_FAST                2 (config)
#             430 LOAD_CONST               1 ('maintenance')
#             432 BINARY_SUBSCR
#             436 STORE_FAST               7 (@py_assert1)
#             438 LOAD_GLOBAL             23 (NULL + isinstance)
#             448 LOAD_FAST                7 (@py_assert1)
#             450 LOAD_GLOBAL             24 (dict)
#             460 CALL                     2
#             468 STORE_FAST               8 (@py_assert4)
#             470 LOAD_FAST                8 (@py_assert4)
#             472 POP_JUMP_IF_TRUE       244 (to 962)
#             474 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             484 LOAD_ATTR               16 (_format_assertmsg)
#             504 LOAD_CONST              10 ('maintenance must be a dict')
#             506 CALL                     1
#             514 LOAD_CONST              11 ('\n>assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}')
#             516 BINARY_OP                0 (+)
#             520 LOAD_CONST              12 ('isinstance')
#             522 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             532 LOAD_ATTR               12 (locals)
#             552 CALL                     0
#             560 CONTAINS_OP              0
#             562 POP_JUMP_IF_TRUE        25 (to 614)
#             564 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             574 LOAD_ATTR               14 (_should_repr_global_name)
#             594 LOAD_GLOBAL             22 (isinstance)
#             604 CALL                     1
#             612 POP_JUMP_IF_FALSE       25 (to 664)
#         >>  614 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             624 LOAD_ATTR                8 (_saferepr)
#             644 LOAD_GLOBAL             22 (isinstance)
#             654 CALL                     1
#             662 JUMP_FORWARD             1 (to 666)
#         >>  664 LOAD_CONST              12 ('isinstance')
#         >>  666 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             676 LOAD_ATTR                8 (_saferepr)
#             696 LOAD_FAST                7 (@py_assert1)
#             698 CALL                     1
#             706 LOAD_CONST              13 ('dict')
#             708 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             718 LOAD_ATTR               12 (locals)
#             738 CALL                     0
#             746 CONTAINS_OP              0
#             748 POP_JUMP_IF_TRUE        25 (to 800)
#             750 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             760 LOAD_ATTR               14 (_should_repr_global_name)
#             780 LOAD_GLOBAL             24 (dict)
#             790 CALL                     1
#             798 POP_JUMP_IF_FALSE       25 (to 850)
#         >>  800 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             810 LOAD_ATTR                8 (_saferepr)
#             830 LOAD_GLOBAL             24 (dict)
#             840 CALL                     1
#             848 JUMP_FORWARD             1 (to 852)
#         >>  850 LOAD_CONST              13 ('dict')
#         >>  852 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             862 LOAD_ATTR                8 (_saferepr)
#             882 LOAD_FAST                8 (@py_assert4)
#             884 CALL                     1
#             892 LOAD_CONST              14 (('py0', 'py2', 'py3', 'py5'))
#             894 BUILD_CONST_KEY_MAP      4
#             896 BINARY_OP                6 (%)
#             900 STORE_FAST               6 (@py_format6)
#             902 LOAD_GLOBAL             19 (NULL + AssertionError)
#             912 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             922 LOAD_ATTR               20 (_format_explanation)
#             942 LOAD_FAST                6 (@py_format6)
#             944 CALL                     1
#             952 CALL                     1
#             960 RAISE_VARARGS            1
#         >>  962 LOAD_CONST               9 (None)
#             964 COPY                     1
#             966 STORE_FAST               7 (@py_assert1)
#             968 STORE_FAST               8 (@py_assert4)
#             970 RETURN_CONST             9 (None)
# 
# Disassembly of <code object test_reactive_compensation_has_weak_buses_or_vsi at 0x3aee2dd0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 244>:
# 244           0 RESUME                   0
# 
# 246           2 LOAD_GLOBAL              1 (NULL + ReactiveCompensationDesignSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 247          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
# 248          54 BUILD_LIST               0
#              56 STORE_FAST               3 (@py_assert1)
#              58 LOAD_CONST               1 ('weak_buses')
#              60 STORE_FAST               4 (@py_assert2)
#              62 LOAD_FAST                4 (@py_assert2)
#              64 LOAD_FAST                2 (config)
#              66 CONTAINS_OP              0
#              68 STORE_FAST               5 (@py_assert4)
#              70 LOAD_FAST                5 (@py_assert4)
#              72 STORE_FAST               6 (@py_assert0)
#              74 LOAD_FAST                5 (@py_assert4)
#              76 POP_JUMP_IF_TRUE         8 (to 94)
#              78 LOAD_CONST               2 ('vsi_result')
#              80 STORE_FAST               7 (@py_assert9)
#              82 LOAD_FAST                7 (@py_assert9)
#              84 LOAD_FAST                2 (config)
#              86 CONTAINS_OP              0
#              88 STORE_FAST               8 (@py_assert11)
#              90 LOAD_FAST                8 (@py_assert11)
#              92 STORE_FAST               6 (@py_assert0)
#         >>   94 LOAD_FAST                6 (@py_assert0)
#              96 EXTENDED_ARG             1
#              98 POP_JUMP_IF_TRUE       366 (to 832)
#             100 LOAD_GLOBAL              5 (NULL + @pytest_ar)
# 
# 250         110 LOAD_ATTR                6 (_call_reprcompare)
# 
# 248         130 LOAD_CONST               3 (('in',))
#             132 LOAD_FAST                5 (@py_assert4)
#             134 BUILD_TUPLE              1
#             136 LOAD_CONST               4 (('%(py3)s in %(py5)s',))
#             138 LOAD_FAST                4 (@py_assert2)
#             140 LOAD_FAST                2 (config)
#             142 BUILD_TUPLE              2
#             144 CALL                     4
#             152 LOAD_GLOBAL              5 (NULL + @pytest_ar)
# 
# 250         162 LOAD_ATTR                8 (_saferepr)
# 
# 248         182 LOAD_FAST                4 (@py_assert2)
#             184 CALL                     1
#             192 LOAD_CONST               5 ('config')
#             194 LOAD_GLOBAL             11 (NULL + @py_builtins)
# 
# 250         204 LOAD_ATTR               12 (locals)
# 
# 248         224 CALL                     0
#             232 CONTAINS_OP              0
#             234 POP_JUMP_IF_TRUE        21 (to 278)
#             236 LOAD_GLOBAL              5 (NULL + @pytest_ar)
# 
# 250         246 LOAD_ATTR               14 (_should_repr_global_name)
# 
# 248         266 LOAD_FAST                2 (config)
#             268 CALL                     1
#             276 POP_JUMP_IF_FALSE       21 (to 320)
#         >>  278 LOAD_GLOBAL              5 (NULL + @pytest_ar)
# 
# 250         288 LOAD_ATTR                8 (_saferepr)
# 
# 248         308 LOAD_FAST                2 (config)
#             310 CALL                     1
#             318 JUMP_FORWARD             1 (to 322)
#         >>  320 LOAD_CONST               5 ('config')
#         >>  322 LOAD_CONST               6 (('py3', 'py5'))
#             324 BUILD_CONST_KEY_MAP      2
#             326 BINARY_OP                6 (%)
#             330 STORE_FAST               9 (@py_format6)
#             332 LOAD_CONST               7 ('%(py7)s')
#             334 LOAD_CONST               8 ('py7')
#             336 LOAD_FAST                9 (@py_format6)
#             338 BUILD_MAP                1
#             340 BINARY_OP                6 (%)
#             344 STORE_FAST              10 (@py_format8)
#             346 LOAD_FAST                3 (@py_assert1)
# 
# 250         348 LOAD_ATTR               17 (NULL|self + append)
# 
# 248         368 LOAD_FAST               10 (@py_format8)
# 
# 250         370 CALL                     1
#             378 POP_TOP
# 
# 248         380 LOAD_FAST                5 (@py_assert4)
#             382 POP_JUMP_IF_TRUE       140 (to 664)
#             384 LOAD_GLOBAL              5 (NULL + @pytest_ar)
# 
# 250         394 LOAD_ATTR                6 (_call_reprcompare)
# 
# 248         414 LOAD_CONST               3 (('in',))
#             416 LOAD_FAST_CHECK          8 (@py_assert11)
#             418 BUILD_TUPLE              1
#             420 LOAD_CONST               9 (('%(py10)s in %(py12)s',))
#             422 LOAD_FAST_CHECK          7 (@py_assert9)
#             424 LOAD_FAST                2 (config)
#             426 BUILD_TUPLE              2
#             428 CALL                     4
#             436 LOAD_GLOBAL              5 (NULL + @pytest_ar)
# 
# 250         446 LOAD_ATTR                8 (_saferepr)
# 
# 248         466 LOAD_FAST                7 (@py_assert9)
#             468 CALL                     1
#             476 LOAD_CONST               5 ('config')
#             478 LOAD_GLOBAL             11 (NULL + @py_builtins)
# 
# 250         488 LOAD_ATTR               12 (locals)
# 
# 248         508 CALL                     0
#             516 CONTAINS_OP              0
#             518 POP_JUMP_IF_TRUE        21 (to 562)
#             520 LOAD_GLOBAL              5 (NULL + @pytest_ar)
# 
# 250         530 LOAD_ATTR               14 (_should_repr_global_name)
# 
# 248         550 LOAD_FAST                2 (config)
#             552 CALL                     1
#             560 POP_JUMP_IF_FALSE       21 (to 604)
#         >>  562 LOAD_GLOBAL              5 (NULL + @pytest_ar)
# 
# 250         572 LOAD_ATTR                8 (_saferepr)
# 
# 248         592 LOAD_FAST                2 (config)
#             594 CALL                     1
#             602 JUMP_FORWARD             1 (to 606)
#         >>  604 LOAD_CONST               5 ('config')
#         >>  606 LOAD_CONST              10 (('py10', 'py12'))
#             608 BUILD_CONST_KEY_MAP      2
#             610 BINARY_OP                6 (%)
#             614 STORE_FAST              11 (@py_format13)
#             616 LOAD_CONST              11 ('%(py14)s')
#             618 LOAD_CONST              12 ('py14')
#             620 LOAD_FAST               11 (@py_format13)
#             622 BUILD_MAP                1
#             624 BINARY_OP                6 (%)
#             628 STORE_FAST              12 (@py_format15)
#             630 LOAD_FAST                3 (@py_assert1)
# 
# 250         632 LOAD_ATTR               17 (NULL|self + append)
# 
# 248         652 LOAD_FAST               12 (@py_format15)
# 
# 250         654 CALL                     1
#             662 POP_TOP
# 
# 248     >>  664 LOAD_GLOBAL              5 (NULL + @pytest_ar)
# 
# 250         674 LOAD_ATTR               18 (_format_boolop)
# 
# 248         694 LOAD_FAST                3 (@py_assert1)
#             696 LOAD_CONST              13 (1)
#             698 CALL                     2
#             706 BUILD_MAP                0
#             708 BINARY_OP                6 (%)
#             712 STORE_FAST              13 (@py_format16)
#             714 LOAD_GLOBAL              5 (NULL + @pytest_ar)
# 
# 250         724 LOAD_ATTR               20 (_format_assertmsg)
# 
# 249         744 LOAD_CONST              14 ("reactive_compensation_design must have 'weak_buses' or 'vsi_result' field")
# 
# 248         746 CALL                     1
#             754 LOAD_CONST              15 ('\n>assert %(py17)s')
#             756 BINARY_OP                0 (+)
#             760 LOAD_CONST              16 ('py17')
#             762 LOAD_FAST               13 (@py_format16)
#             764 BUILD_MAP                1
#             766 BINARY_OP                6 (%)
#             770 STORE_FAST              14 (@py_format18)
#             772 LOAD_GLOBAL             23 (NULL + AssertionError)
#             782 LOAD_GLOBAL              5 (NULL + @pytest_ar)
# 
# 250         792 LOAD_ATTR               24 (_format_explanation)
# 
# 248         812 LOAD_FAST               14 (@py_format18)
#             814 CALL                     1
#             822 CALL                     1
#             830 RAISE_VARARGS            1
#         >>  832 LOAD_CONST              17 (None)
#             834 COPY                     1
#             836 STORE_FAST               6 (@py_assert0)
#             838 COPY                     1
#             840 STORE_FAST               3 (@py_assert1)
#             842 COPY                     1
#             844 STORE_FAST               4 (@py_assert2)
#             846 COPY                     1
#             848 STORE_FAST               5 (@py_assert4)
#             850 COPY                     1
#             852 STORE_FAST               7 (@py_assert9)
#             854 STORE_FAST               8 (@py_assert11)
#             856 RETURN_CONST            17 (None)
# 
# Disassembly of <code object test_result_compare_has_sources at 0x3aecd0e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 252>:
# 252           0 RESUME                   0
# 
# 254           2 LOAD_GLOBAL              1 (NULL + ResultCompareSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 255          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
# 256          54 LOAD_CONST               1 ('sources')
#              56 STORE_FAST               3 (@py_assert0)
#              58 LOAD_FAST                3 (@py_assert0)
#              60 LOAD_FAST                2 (config)
#              62 CONTAINS_OP              0
#              64 STORE_FAST               4 (@py_assert2)
#              66 LOAD_FAST                4 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       175 (to 420)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               2 (('in',))
#             102 LOAD_FAST                4 (@py_assert2)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             108 LOAD_FAST                3 (@py_assert0)
#             110 LOAD_FAST                2 (config)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_saferepr)
#             152 LOAD_FAST                3 (@py_assert0)
#             154 CALL                     1
#             162 LOAD_CONST               4 ('config')
#             164 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             174 LOAD_ATTR               12 (locals)
#             194 CALL                     0
#             202 CONTAINS_OP              0
#             204 POP_JUMP_IF_TRUE        21 (to 248)
#             206 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             216 LOAD_ATTR               14 (_should_repr_global_name)
#             236 LOAD_FAST                2 (config)
#             238 CALL                     1
#             246 POP_JUMP_IF_FALSE       21 (to 290)
#         >>  248 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             258 LOAD_ATTR                8 (_saferepr)
#             278 LOAD_FAST                2 (config)
#             280 CALL                     1
#             288 JUMP_FORWARD             1 (to 292)
#         >>  290 LOAD_CONST               4 ('config')
#         >>  292 LOAD_CONST               5 (('py1', 'py3'))
#             294 BUILD_CONST_KEY_MAP      2
#             296 BINARY_OP                6 (%)
#             300 STORE_FAST               5 (@py_format4)
#             302 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             312 LOAD_ATTR               16 (_format_assertmsg)
#             332 LOAD_CONST               6 ("result_compare must have 'sources' field")
#             334 CALL                     1
#             342 LOAD_CONST               7 ('\n>assert %(py5)s')
#             344 BINARY_OP                0 (+)
#             348 LOAD_CONST               8 ('py5')
#             350 LOAD_FAST                5 (@py_format4)
#             352 BUILD_MAP                1
#             354 BINARY_OP                6 (%)
#             358 STORE_FAST               6 (@py_format6)
#             360 LOAD_GLOBAL             19 (NULL + AssertionError)
#             370 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             380 LOAD_ATTR               20 (_format_explanation)
#             400 LOAD_FAST                6 (@py_format6)
#             402 CALL                     1
#             410 CALL                     1
#             418 RAISE_VARARGS            1
#         >>  420 LOAD_CONST               9 (None)
#             422 COPY                     1
#             424 STORE_FAST               3 (@py_assert0)
#             426 STORE_FAST               4 (@py_assert2)
# 
# 257         428 LOAD_FAST                2 (config)
#             430 LOAD_CONST               1 ('sources')
#             432 BINARY_SUBSCR
#             436 STORE_FAST               7 (@py_assert1)
#             438 LOAD_GLOBAL             23 (NULL + isinstance)
#             448 LOAD_FAST                7 (@py_assert1)
#             450 LOAD_GLOBAL             24 (list)
#             460 CALL                     2
#             468 STORE_FAST               8 (@py_assert4)
#             470 LOAD_FAST                8 (@py_assert4)
#             472 POP_JUMP_IF_TRUE       244 (to 962)
#             474 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             484 LOAD_ATTR               16 (_format_assertmsg)
#             504 LOAD_CONST              10 ('sources must be a list')
#             506 CALL                     1
#             514 LOAD_CONST              11 ('\n>assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}')
#             516 BINARY_OP                0 (+)
#             520 LOAD_CONST              12 ('isinstance')
#             522 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             532 LOAD_ATTR               12 (locals)
#             552 CALL                     0
#             560 CONTAINS_OP              0
#             562 POP_JUMP_IF_TRUE        25 (to 614)
#             564 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             574 LOAD_ATTR               14 (_should_repr_global_name)
#             594 LOAD_GLOBAL             22 (isinstance)
#             604 CALL                     1
#             612 POP_JUMP_IF_FALSE       25 (to 664)
#         >>  614 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             624 LOAD_ATTR                8 (_saferepr)
#             644 LOAD_GLOBAL             22 (isinstance)
#             654 CALL                     1
#             662 JUMP_FORWARD             1 (to 666)
#         >>  664 LOAD_CONST              12 ('isinstance')
#         >>  666 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             676 LOAD_ATTR                8 (_saferepr)
#             696 LOAD_FAST                7 (@py_assert1)
#             698 CALL                     1
#             706 LOAD_CONST              13 ('list')
#             708 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             718 LOAD_ATTR               12 (locals)
#             738 CALL                     0
#             746 CONTAINS_OP              0
#             748 POP_JUMP_IF_TRUE        25 (to 800)
#             750 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             760 LOAD_ATTR               14 (_should_repr_global_name)
#             780 LOAD_GLOBAL             24 (list)
#             790 CALL                     1
#             798 POP_JUMP_IF_FALSE       25 (to 850)
#         >>  800 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             810 LOAD_ATTR                8 (_saferepr)
#             830 LOAD_GLOBAL             24 (list)
#             840 CALL                     1
#             848 JUMP_FORWARD             1 (to 852)
#         >>  850 LOAD_CONST              13 ('list')
#         >>  852 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             862 LOAD_ATTR                8 (_saferepr)
#             882 LOAD_FAST                8 (@py_assert4)
#             884 CALL                     1
#             892 LOAD_CONST              14 (('py0', 'py2', 'py3', 'py5'))
#             894 BUILD_CONST_KEY_MAP      4
#             896 BINARY_OP                6 (%)
#             900 STORE_FAST               6 (@py_format6)
#             902 LOAD_GLOBAL             19 (NULL + AssertionError)
#             912 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             922 LOAD_ATTR               20 (_format_explanation)
#             942 LOAD_FAST                6 (@py_format6)
#             944 CALL                     1
#             952 CALL                     1
#             960 RAISE_VARARGS            1
#         >>  962 LOAD_CONST               9 (None)
#             964 COPY                     1
#             966 STORE_FAST               7 (@py_assert1)
#             968 STORE_FAST               8 (@py_assert4)
#             970 RETURN_CONST             9 (None)
# 
# Disassembly of <code object test_visualize_has_source at 0x3aecd580, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 259>:
# 259           0 RESUME                   0
# 
# 261           2 LOAD_GLOBAL              1 (NULL + VisualizeSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 262          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
# 263          54 LOAD_CONST               1 ('source')
#              56 STORE_FAST               3 (@py_assert0)
#              58 LOAD_FAST                3 (@py_assert0)
#              60 LOAD_FAST                2 (config)
#              62 CONTAINS_OP              0
#              64 STORE_FAST               4 (@py_assert2)
#              66 LOAD_FAST                4 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       175 (to 420)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               2 (('in',))
#             102 LOAD_FAST                4 (@py_assert2)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             108 LOAD_FAST                3 (@py_assert0)
#             110 LOAD_FAST                2 (config)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_saferepr)
#             152 LOAD_FAST                3 (@py_assert0)
#             154 CALL                     1
#             162 LOAD_CONST               4 ('config')
#             164 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             174 LOAD_ATTR               12 (locals)
#             194 CALL                     0
#             202 CONTAINS_OP              0
#             204 POP_JUMP_IF_TRUE        21 (to 248)
#             206 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             216 LOAD_ATTR               14 (_should_repr_global_name)
#             236 LOAD_FAST                2 (config)
#             238 CALL                     1
#             246 POP_JUMP_IF_FALSE       21 (to 290)
#         >>  248 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             258 LOAD_ATTR                8 (_saferepr)
#             278 LOAD_FAST                2 (config)
#             280 CALL                     1
#             288 JUMP_FORWARD             1 (to 292)
#         >>  290 LOAD_CONST               4 ('config')
#         >>  292 LOAD_CONST               5 (('py1', 'py3'))
#             294 BUILD_CONST_KEY_MAP      2
#             296 BINARY_OP                6 (%)
#             300 STORE_FAST               5 (@py_format4)
#             302 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             312 LOAD_ATTR               16 (_format_assertmsg)
#             332 LOAD_CONST               6 ("visualize must have 'source' field")
#             334 CALL                     1
#             342 LOAD_CONST               7 ('\n>assert %(py5)s')
#             344 BINARY_OP                0 (+)
#             348 LOAD_CONST               8 ('py5')
#             350 LOAD_FAST                5 (@py_format4)
#             352 BUILD_MAP                1
#             354 BINARY_OP                6 (%)
#             358 STORE_FAST               6 (@py_format6)
#             360 LOAD_GLOBAL             19 (NULL + AssertionError)
#             370 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             380 LOAD_ATTR               20 (_format_explanation)
#             400 LOAD_FAST                6 (@py_format6)
#             402 CALL                     1
#             410 CALL                     1
#             418 RAISE_VARARGS            1
#         >>  420 LOAD_CONST               9 (None)
#             422 COPY                     1
#             424 STORE_FAST               3 (@py_assert0)
#             426 STORE_FAST               4 (@py_assert2)
# 
# 264         428 LOAD_FAST                2 (config)
#             430 LOAD_CONST               1 ('source')
#             432 BINARY_SUBSCR
#             436 STORE_FAST               7 (@py_assert1)
#             438 LOAD_GLOBAL             23 (NULL + isinstance)
#             448 LOAD_FAST                7 (@py_assert1)
#             450 LOAD_GLOBAL             24 (dict)
#             460 CALL                     2
#             468 STORE_FAST               8 (@py_assert4)
#             470 LOAD_FAST                8 (@py_assert4)
#             472 POP_JUMP_IF_TRUE       244 (to 962)
#             474 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             484 LOAD_ATTR               16 (_format_assertmsg)
#             504 LOAD_CONST              10 ('source must be a dict')
#             506 CALL                     1
#             514 LOAD_CONST              11 ('\n>assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}')
#             516 BINARY_OP                0 (+)
#             520 LOAD_CONST              12 ('isinstance')
#             522 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             532 LOAD_ATTR               12 (locals)
#             552 CALL                     0
#             560 CONTAINS_OP              0
#             562 POP_JUMP_IF_TRUE        25 (to 614)
#             564 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             574 LOAD_ATTR               14 (_should_repr_global_name)
#             594 LOAD_GLOBAL             22 (isinstance)
#             604 CALL                     1
#             612 POP_JUMP_IF_FALSE       25 (to 664)
#         >>  614 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             624 LOAD_ATTR                8 (_saferepr)
#             644 LOAD_GLOBAL             22 (isinstance)
#             654 CALL                     1
#             662 JUMP_FORWARD             1 (to 666)
#         >>  664 LOAD_CONST              12 ('isinstance')
#         >>  666 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             676 LOAD_ATTR                8 (_saferepr)
#             696 LOAD_FAST                7 (@py_assert1)
#             698 CALL                     1
#             706 LOAD_CONST              13 ('dict')
#             708 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             718 LOAD_ATTR               12 (locals)
#             738 CALL                     0
#             746 CONTAINS_OP              0
#             748 POP_JUMP_IF_TRUE        25 (to 800)
#             750 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             760 LOAD_ATTR               14 (_should_repr_global_name)
#             780 LOAD_GLOBAL             24 (dict)
#             790 CALL                     1
#             798 POP_JUMP_IF_FALSE       25 (to 850)
#         >>  800 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             810 LOAD_ATTR                8 (_saferepr)
#             830 LOAD_GLOBAL             24 (dict)
#             840 CALL                     1
#             848 JUMP_FORWARD             1 (to 852)
#         >>  850 LOAD_CONST              13 ('dict')
#         >>  852 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             862 LOAD_ATTR                8 (_saferepr)
#             882 LOAD_FAST                8 (@py_assert4)
#             884 CALL                     1
#             892 LOAD_CONST              14 (('py0', 'py2', 'py3', 'py5'))
#             894 BUILD_CONST_KEY_MAP      4
#             896 BINARY_OP                6 (%)
#             900 STORE_FAST               6 (@py_format6)
#             902 LOAD_GLOBAL             19 (NULL + AssertionError)
#             912 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             922 LOAD_ATTR               20 (_format_explanation)
#             942 LOAD_FAST                6 (@py_format6)
#             944 CALL                     1
#             952 CALL                     1
#             960 RAISE_VARARGS            1
#         >>  962 LOAD_CONST               9 (None)
#             964 COPY                     1
#             966 STORE_FAST               7 (@py_assert1)
#             968 STORE_FAST               8 (@py_assert4)
#             970 RETURN_CONST             9 (None)
# 
# Disassembly of <code object test_waveform_export_has_source_and_export at 0x3afa6d80, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 266>:
# 266           0 RESUME                   0
# 
# 268           2 LOAD_GLOBAL              1 (NULL + WaveformExportSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 269          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
# 270          54 LOAD_CONST               1 ('source')
#              56 STORE_FAST               3 (@py_assert0)
#              58 LOAD_FAST                3 (@py_assert0)
#              60 LOAD_FAST                2 (config)
#              62 CONTAINS_OP              0
#              64 STORE_FAST               4 (@py_assert2)
#              66 LOAD_FAST                4 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       175 (to 420)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               2 (('in',))
#             102 LOAD_FAST                4 (@py_assert2)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             108 LOAD_FAST                3 (@py_assert0)
#             110 LOAD_FAST                2 (config)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_saferepr)
#             152 LOAD_FAST                3 (@py_assert0)
#             154 CALL                     1
#             162 LOAD_CONST               4 ('config')
#             164 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             174 LOAD_ATTR               12 (locals)
#             194 CALL                     0
#             202 CONTAINS_OP              0
#             204 POP_JUMP_IF_TRUE        21 (to 248)
#             206 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             216 LOAD_ATTR               14 (_should_repr_global_name)
#             236 LOAD_FAST                2 (config)
#             238 CALL                     1
#             246 POP_JUMP_IF_FALSE       21 (to 290)
#         >>  248 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             258 LOAD_ATTR                8 (_saferepr)
#             278 LOAD_FAST                2 (config)
#             280 CALL                     1
#             288 JUMP_FORWARD             1 (to 292)
#         >>  290 LOAD_CONST               4 ('config')
#         >>  292 LOAD_CONST               5 (('py1', 'py3'))
#             294 BUILD_CONST_KEY_MAP      2
#             296 BINARY_OP                6 (%)
#             300 STORE_FAST               5 (@py_format4)
#             302 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             312 LOAD_ATTR               16 (_format_assertmsg)
#             332 LOAD_CONST               6 ("waveform_export must have 'source' field")
#             334 CALL                     1
#             342 LOAD_CONST               7 ('\n>assert %(py5)s')
#             344 BINARY_OP                0 (+)
#             348 LOAD_CONST               8 ('py5')
#             350 LOAD_FAST                5 (@py_format4)
#             352 BUILD_MAP                1
#             354 BINARY_OP                6 (%)
#             358 STORE_FAST               6 (@py_format6)
#             360 LOAD_GLOBAL             19 (NULL + AssertionError)
#             370 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             380 LOAD_ATTR               20 (_format_explanation)
#             400 LOAD_FAST                6 (@py_format6)
#             402 CALL                     1
#             410 CALL                     1
#             418 RAISE_VARARGS            1
#         >>  420 LOAD_CONST               9 (None)
#             422 COPY                     1
#             424 STORE_FAST               3 (@py_assert0)
#             426 STORE_FAST               4 (@py_assert2)
# 
# 271         428 LOAD_CONST              10 ('export')
#             430 STORE_FAST               3 (@py_assert0)
#             432 LOAD_FAST                3 (@py_assert0)
#             434 LOAD_FAST                2 (config)
#             436 CONTAINS_OP              0
#             438 STORE_FAST               4 (@py_assert2)
#             440 LOAD_FAST                4 (@py_assert2)
#             442 POP_JUMP_IF_TRUE       175 (to 794)
#             444 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             454 LOAD_ATTR                6 (_call_reprcompare)
#             474 LOAD_CONST               2 (('in',))
#             476 LOAD_FAST                4 (@py_assert2)
#             478 BUILD_TUPLE              1
#             480 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             482 LOAD_FAST                3 (@py_assert0)
#             484 LOAD_FAST                2 (config)
#             486 BUILD_TUPLE              2
#             488 CALL                     4
#             496 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             506 LOAD_ATTR                8 (_saferepr)
#             526 LOAD_FAST                3 (@py_assert0)
#             528 CALL                     1
#             536 LOAD_CONST               4 ('config')
#             538 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             548 LOAD_ATTR               12 (locals)
#             568 CALL                     0
#             576 CONTAINS_OP              0
#             578 POP_JUMP_IF_TRUE        21 (to 622)
#             580 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             590 LOAD_ATTR               14 (_should_repr_global_name)
#             610 LOAD_FAST                2 (config)
#             612 CALL                     1
#             620 POP_JUMP_IF_FALSE       21 (to 664)
#         >>  622 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             632 LOAD_ATTR                8 (_saferepr)
#             652 LOAD_FAST                2 (config)
#             654 CALL                     1
#             662 JUMP_FORWARD             1 (to 666)
#         >>  664 LOAD_CONST               4 ('config')
#         >>  666 LOAD_CONST               5 (('py1', 'py3'))
#             668 BUILD_CONST_KEY_MAP      2
#             670 BINARY_OP                6 (%)
#             674 STORE_FAST               5 (@py_format4)
#             676 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             686 LOAD_ATTR               16 (_format_assertmsg)
#             706 LOAD_CONST              11 ("waveform_export must have 'export' field")
#             708 CALL                     1
#             716 LOAD_CONST               7 ('\n>assert %(py5)s')
#             718 BINARY_OP                0 (+)
#             722 LOAD_CONST               8 ('py5')
#             724 LOAD_FAST                5 (@py_format4)
#             726 BUILD_MAP                1
#             728 BINARY_OP                6 (%)
#             732 STORE_FAST               6 (@py_format6)
#             734 LOAD_GLOBAL             19 (NULL + AssertionError)
#             744 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             754 LOAD_ATTR               20 (_format_explanation)
#             774 LOAD_FAST                6 (@py_format6)
#             776 CALL                     1
#             784 CALL                     1
#             792 RAISE_VARARGS            1
#         >>  794 LOAD_CONST               9 (None)
#             796 COPY                     1
#             798 STORE_FAST               3 (@py_assert0)
#             800 STORE_FAST               4 (@py_assert2)
#             802 RETURN_CONST             9 (None)
# 
# Disassembly of <code object test_compare_visualization_has_sources at 0x3aecca90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 273>:
# 273           0 RESUME                   0
# 
# 275           2 LOAD_GLOBAL              1 (NULL + CompareVisualizationSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 276          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
# 277          54 LOAD_CONST               1 ('sources')
#              56 STORE_FAST               3 (@py_assert0)
#              58 LOAD_FAST                3 (@py_assert0)
#              60 LOAD_FAST                2 (config)
#              62 CONTAINS_OP              0
#              64 STORE_FAST               4 (@py_assert2)
#              66 LOAD_FAST                4 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       175 (to 420)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               2 (('in',))
#             102 LOAD_FAST                4 (@py_assert2)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             108 LOAD_FAST                3 (@py_assert0)
#             110 LOAD_FAST                2 (config)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_saferepr)
#             152 LOAD_FAST                3 (@py_assert0)
#             154 CALL                     1
#             162 LOAD_CONST               4 ('config')
#             164 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             174 LOAD_ATTR               12 (locals)
#             194 CALL                     0
#             202 CONTAINS_OP              0
#             204 POP_JUMP_IF_TRUE        21 (to 248)
#             206 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             216 LOAD_ATTR               14 (_should_repr_global_name)
#             236 LOAD_FAST                2 (config)
#             238 CALL                     1
#             246 POP_JUMP_IF_FALSE       21 (to 290)
#         >>  248 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             258 LOAD_ATTR                8 (_saferepr)
#             278 LOAD_FAST                2 (config)
#             280 CALL                     1
#             288 JUMP_FORWARD             1 (to 292)
#         >>  290 LOAD_CONST               4 ('config')
#         >>  292 LOAD_CONST               5 (('py1', 'py3'))
#             294 BUILD_CONST_KEY_MAP      2
#             296 BINARY_OP                6 (%)
#             300 STORE_FAST               5 (@py_format4)
#             302 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             312 LOAD_ATTR               16 (_format_assertmsg)
#             332 LOAD_CONST               6 ("compare_visualization must have 'sources' field")
#             334 CALL                     1
#             342 LOAD_CONST               7 ('\n>assert %(py5)s')
#             344 BINARY_OP                0 (+)
#             348 LOAD_CONST               8 ('py5')
#             350 LOAD_FAST                5 (@py_format4)
#             352 BUILD_MAP                1
#             354 BINARY_OP                6 (%)
#             358 STORE_FAST               6 (@py_format6)
#             360 LOAD_GLOBAL             19 (NULL + AssertionError)
#             370 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             380 LOAD_ATTR               20 (_format_explanation)
#             400 LOAD_FAST                6 (@py_format6)
#             402 CALL                     1
#             410 CALL                     1
#             418 RAISE_VARARGS            1
#         >>  420 LOAD_CONST               9 (None)
#             422 COPY                     1
#             424 STORE_FAST               3 (@py_assert0)
#             426 STORE_FAST               4 (@py_assert2)
# 
# 278         428 LOAD_FAST                2 (config)
#             430 LOAD_CONST               1 ('sources')
#             432 BINARY_SUBSCR
#             436 STORE_FAST               7 (@py_assert1)
#             438 LOAD_GLOBAL             23 (NULL + isinstance)
#             448 LOAD_FAST                7 (@py_assert1)
#             450 LOAD_GLOBAL             24 (list)
#             460 CALL                     2
#             468 STORE_FAST               8 (@py_assert4)
#             470 LOAD_FAST                8 (@py_assert4)
#             472 POP_JUMP_IF_TRUE       244 (to 962)
#             474 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             484 LOAD_ATTR               16 (_format_assertmsg)
#             504 LOAD_CONST              10 ('sources must be a list')
#             506 CALL                     1
#             514 LOAD_CONST              11 ('\n>assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}')
#             516 BINARY_OP                0 (+)
#             520 LOAD_CONST              12 ('isinstance')
#             522 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             532 LOAD_ATTR               12 (locals)
#             552 CALL                     0
#             560 CONTAINS_OP              0
#             562 POP_JUMP_IF_TRUE        25 (to 614)
#             564 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             574 LOAD_ATTR               14 (_should_repr_global_name)
#             594 LOAD_GLOBAL             22 (isinstance)
#             604 CALL                     1
#             612 POP_JUMP_IF_FALSE       25 (to 664)
#         >>  614 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             624 LOAD_ATTR                8 (_saferepr)
#             644 LOAD_GLOBAL             22 (isinstance)
#             654 CALL                     1
#             662 JUMP_FORWARD             1 (to 666)
#         >>  664 LOAD_CONST              12 ('isinstance')
#         >>  666 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             676 LOAD_ATTR                8 (_saferepr)
#             696 LOAD_FAST                7 (@py_assert1)
#             698 CALL                     1
#             706 LOAD_CONST              13 ('list')
#             708 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             718 LOAD_ATTR               12 (locals)
#             738 CALL                     0
#             746 CONTAINS_OP              0
#             748 POP_JUMP_IF_TRUE        25 (to 800)
#             750 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             760 LOAD_ATTR               14 (_should_repr_global_name)
#             780 LOAD_GLOBAL             24 (list)
#             790 CALL                     1
#             798 POP_JUMP_IF_FALSE       25 (to 850)
#         >>  800 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             810 LOAD_ATTR                8 (_saferepr)
#             830 LOAD_GLOBAL             24 (list)
#             840 CALL                     1
#             848 JUMP_FORWARD             1 (to 852)
#         >>  850 LOAD_CONST              13 ('list')
#         >>  852 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             862 LOAD_ATTR                8 (_saferepr)
#             882 LOAD_FAST                8 (@py_assert4)
#             884 CALL                     1
#             892 LOAD_CONST              14 (('py0', 'py2', 'py3', 'py5'))
#             894 BUILD_CONST_KEY_MAP      4
#             896 BINARY_OP                6 (%)
#             900 STORE_FAST               6 (@py_format6)
#             902 LOAD_GLOBAL             19 (NULL + AssertionError)
#             912 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             922 LOAD_ATTR               20 (_format_explanation)
#             942 LOAD_FAST                6 (@py_format6)
#             944 CALL                     1
#             952 CALL                     1
#             960 RAISE_VARARGS            1
#         >>  962 LOAD_CONST               9 (None)
#             964 COPY                     1
#             966 STORE_FAST               7 (@py_assert1)
#             968 STORE_FAST               8 (@py_assert4)
#             970 RETURN_CONST             9 (None)
# 
# Disassembly of <code object test_comtrade_export_has_source_and_export at 0x3aec4000, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 280>:
# 280           0 RESUME                   0
# 
# 282           2 LOAD_GLOBAL              1 (NULL + ComtradeExportSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 283          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
# 284          54 LOAD_CONST               1 ('source')
#              56 STORE_FAST               3 (@py_assert0)
#              58 LOAD_FAST                3 (@py_assert0)
#              60 LOAD_FAST                2 (config)
#              62 CONTAINS_OP              0
#              64 STORE_FAST               4 (@py_assert2)
#              66 LOAD_FAST                4 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       175 (to 420)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               2 (('in',))
#             102 LOAD_FAST                4 (@py_assert2)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             108 LOAD_FAST                3 (@py_assert0)
#             110 LOAD_FAST                2 (config)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_saferepr)
#             152 LOAD_FAST                3 (@py_assert0)
#             154 CALL                     1
#             162 LOAD_CONST               4 ('config')
#             164 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             174 LOAD_ATTR               12 (locals)
#             194 CALL                     0
#             202 CONTAINS_OP              0
#             204 POP_JUMP_IF_TRUE        21 (to 248)
#             206 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             216 LOAD_ATTR               14 (_should_repr_global_name)
#             236 LOAD_FAST                2 (config)
#             238 CALL                     1
#             246 POP_JUMP_IF_FALSE       21 (to 290)
#         >>  248 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             258 LOAD_ATTR                8 (_saferepr)
#             278 LOAD_FAST                2 (config)
#             280 CALL                     1
#             288 JUMP_FORWARD             1 (to 292)
#         >>  290 LOAD_CONST               4 ('config')
#         >>  292 LOAD_CONST               5 (('py1', 'py3'))
#             294 BUILD_CONST_KEY_MAP      2
#             296 BINARY_OP                6 (%)
#             300 STORE_FAST               5 (@py_format4)
#             302 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             312 LOAD_ATTR               16 (_format_assertmsg)
#             332 LOAD_CONST               6 ("comtrade_export must have 'source' field")
#             334 CALL                     1
#             342 LOAD_CONST               7 ('\n>assert %(py5)s')
#             344 BINARY_OP                0 (+)
#             348 LOAD_CONST               8 ('py5')
#             350 LOAD_FAST                5 (@py_format4)
#             352 BUILD_MAP                1
#             354 BINARY_OP                6 (%)
#             358 STORE_FAST               6 (@py_format6)
#             360 LOAD_GLOBAL             19 (NULL + AssertionError)
#             370 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             380 LOAD_ATTR               20 (_format_explanation)
#             400 LOAD_FAST                6 (@py_format6)
#             402 CALL                     1
#             410 CALL                     1
#             418 RAISE_VARARGS            1
#         >>  420 LOAD_CONST               9 (None)
#             422 COPY                     1
#             424 STORE_FAST               3 (@py_assert0)
#             426 STORE_FAST               4 (@py_assert2)
# 
# 285         428 LOAD_CONST              10 ('export')
#             430 STORE_FAST               3 (@py_assert0)
#             432 LOAD_FAST                3 (@py_assert0)
#             434 LOAD_FAST                2 (config)
#             436 CONTAINS_OP              0
#             438 STORE_FAST               4 (@py_assert2)
#             440 LOAD_FAST                4 (@py_assert2)
#             442 POP_JUMP_IF_TRUE       175 (to 794)
#             444 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             454 LOAD_ATTR                6 (_call_reprcompare)
#             474 LOAD_CONST               2 (('in',))
#             476 LOAD_FAST                4 (@py_assert2)
#             478 BUILD_TUPLE              1
#             480 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             482 LOAD_FAST                3 (@py_assert0)
#             484 LOAD_FAST                2 (config)
#             486 BUILD_TUPLE              2
#             488 CALL                     4
#             496 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             506 LOAD_ATTR                8 (_saferepr)
#             526 LOAD_FAST                3 (@py_assert0)
#             528 CALL                     1
#             536 LOAD_CONST               4 ('config')
#             538 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             548 LOAD_ATTR               12 (locals)
#             568 CALL                     0
#             576 CONTAINS_OP              0
#             578 POP_JUMP_IF_TRUE        21 (to 622)
#             580 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             590 LOAD_ATTR               14 (_should_repr_global_name)
#             610 LOAD_FAST                2 (config)
#             612 CALL                     1
#             620 POP_JUMP_IF_FALSE       21 (to 664)
#         >>  622 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             632 LOAD_ATTR                8 (_saferepr)
#             652 LOAD_FAST                2 (config)
#             654 CALL                     1
#             662 JUMP_FORWARD             1 (to 666)
#         >>  664 LOAD_CONST               4 ('config')
#         >>  666 LOAD_CONST               5 (('py1', 'py3'))
#             668 BUILD_CONST_KEY_MAP      2
#             670 BINARY_OP                6 (%)
#             674 STORE_FAST               5 (@py_format4)
#             676 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             686 LOAD_ATTR               16 (_format_assertmsg)
#             706 LOAD_CONST              11 ("comtrade_export must have 'export' field")
#             708 CALL                     1
#             716 LOAD_CONST               7 ('\n>assert %(py5)s')
#             718 BINARY_OP                0 (+)
#             722 LOAD_CONST               8 ('py5')
#             724 LOAD_FAST                5 (@py_format4)
#             726 BUILD_MAP                1
#             728 BINARY_OP                6 (%)
#             732 STORE_FAST               6 (@py_format6)
#             734 LOAD_GLOBAL             19 (NULL + AssertionError)
#             744 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             754 LOAD_ATTR               20 (_format_explanation)
#             774 LOAD_FAST                6 (@py_format6)
#             776 CALL                     1
#             784 CALL                     1
#             792 RAISE_VARARGS            1
#         >>  794 LOAD_CONST               9 (None)
#             796 COPY                     1
#             798 STORE_FAST               3 (@py_assert0)
#             800 STORE_FAST               4 (@py_assert2)
#             802 RETURN_CONST             9 (None)
# 
# Disassembly of <code object test_auto_loop_breaker_has_algorithm at 0x3af937b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 287>:
# 287           0 RESUME                   0
# 
# 289           2 LOAD_GLOBAL              1 (NULL + AutoLoopBreakerSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 290          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
# 291          54 LOAD_CONST               1 ('algorithm')
#              56 STORE_FAST               3 (@py_assert0)
#              58 LOAD_FAST                3 (@py_assert0)
#              60 LOAD_FAST                2 (config)
#              62 CONTAINS_OP              0
#              64 STORE_FAST               4 (@py_assert2)
#              66 LOAD_FAST                4 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       175 (to 420)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               2 (('in',))
#             102 LOAD_FAST                4 (@py_assert2)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             108 LOAD_FAST                3 (@py_assert0)
#             110 LOAD_FAST                2 (config)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_saferepr)
#             152 LOAD_FAST                3 (@py_assert0)
#             154 CALL                     1
#             162 LOAD_CONST               4 ('config')
#             164 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             174 LOAD_ATTR               12 (locals)
#             194 CALL                     0
#             202 CONTAINS_OP              0
#             204 POP_JUMP_IF_TRUE        21 (to 248)
#             206 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             216 LOAD_ATTR               14 (_should_repr_global_name)
#             236 LOAD_FAST                2 (config)
#             238 CALL                     1
#             246 POP_JUMP_IF_FALSE       21 (to 290)
#         >>  248 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             258 LOAD_ATTR                8 (_saferepr)
#             278 LOAD_FAST                2 (config)
#             280 CALL                     1
#             288 JUMP_FORWARD             1 (to 292)
#         >>  290 LOAD_CONST               4 ('config')
#         >>  292 LOAD_CONST               5 (('py1', 'py3'))
#             294 BUILD_CONST_KEY_MAP      2
#             296 BINARY_OP                6 (%)
#             300 STORE_FAST               5 (@py_format4)
#             302 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             312 LOAD_ATTR               16 (_format_assertmsg)
#             332 LOAD_CONST               6 ("auto_loop_breaker must have 'algorithm' field")
#             334 CALL                     1
#             342 LOAD_CONST               7 ('\n>assert %(py5)s')
#             344 BINARY_OP                0 (+)
#             348 LOAD_CONST               8 ('py5')
#             350 LOAD_FAST                5 (@py_format4)
#             352 BUILD_MAP                1
#             354 BINARY_OP                6 (%)
#             358 STORE_FAST               6 (@py_format6)
#             360 LOAD_GLOBAL             19 (NULL + AssertionError)
#             370 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             380 LOAD_ATTR               20 (_format_explanation)
#             400 LOAD_FAST                6 (@py_format6)
#             402 CALL                     1
#             410 CALL                     1
#             418 RAISE_VARARGS            1
#         >>  420 LOAD_CONST               9 (None)
#             422 COPY                     1
#             424 STORE_FAST               3 (@py_assert0)
#             426 STORE_FAST               4 (@py_assert2)
#             428 RETURN_CONST             9 (None)
# 
# Disassembly of <code object test_model_parameter_extractor_has_extraction at 0x3af97180, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 293>:
# 293           0 RESUME                   0
# 
# 295           2 LOAD_GLOBAL              1 (NULL + ModelParameterExtractorSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 296          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
# 297          54 LOAD_CONST               1 ('extraction')
#              56 STORE_FAST               3 (@py_assert0)
#              58 LOAD_FAST                3 (@py_assert0)
#              60 LOAD_FAST                2 (config)
#              62 CONTAINS_OP              0
#              64 STORE_FAST               4 (@py_assert2)
#              66 LOAD_FAST                4 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       175 (to 420)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               2 (('in',))
#             102 LOAD_FAST                4 (@py_assert2)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             108 LOAD_FAST                3 (@py_assert0)
#             110 LOAD_FAST                2 (config)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_saferepr)
#             152 LOAD_FAST                3 (@py_assert0)
#             154 CALL                     1
#             162 LOAD_CONST               4 ('config')
#             164 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             174 LOAD_ATTR               12 (locals)
#             194 CALL                     0
#             202 CONTAINS_OP              0
#             204 POP_JUMP_IF_TRUE        21 (to 248)
#             206 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             216 LOAD_ATTR               14 (_should_repr_global_name)
#             236 LOAD_FAST                2 (config)
#             238 CALL                     1
#             246 POP_JUMP_IF_FALSE       21 (to 290)
#         >>  248 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             258 LOAD_ATTR                8 (_saferepr)
#             278 LOAD_FAST                2 (config)
#             280 CALL                     1
#             288 JUMP_FORWARD             1 (to 292)
#         >>  290 LOAD_CONST               4 ('config')
#         >>  292 LOAD_CONST               5 (('py1', 'py3'))
#             294 BUILD_CONST_KEY_MAP      2
#             296 BINARY_OP                6 (%)
#             300 STORE_FAST               5 (@py_format4)
#             302 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             312 LOAD_ATTR               16 (_format_assertmsg)
#             332 LOAD_CONST               6 ("model_parameter_extractor must have 'extraction' field")
#             334 CALL                     1
#             342 LOAD_CONST               7 ('\n>assert %(py5)s')
#             344 BINARY_OP                0 (+)
#             348 LOAD_CONST               8 ('py5')
#             350 LOAD_FAST                5 (@py_format4)
#             352 BUILD_MAP                1
#             354 BINARY_OP                6 (%)
#             358 STORE_FAST               6 (@py_format6)
#             360 LOAD_GLOBAL             19 (NULL + AssertionError)
#             370 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             380 LOAD_ATTR               20 (_format_explanation)
#             400 LOAD_FAST                6 (@py_format6)
#             402 CALL                     1
#             410 CALL                     1
#             418 RAISE_VARARGS            1
#         >>  420 LOAD_CONST               9 (None)
#             422 COPY                     1
#             424 STORE_FAST               3 (@py_assert0)
#             426 STORE_FAST               4 (@py_assert2)
#             428 RETURN_CONST             9 (None)
# 
# Disassembly of <code object test_report_generator_has_report at 0x3ae76f20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 299>:
# 299           0 RESUME                   0
# 
# 301           2 LOAD_GLOBAL              1 (NULL + ReportGeneratorSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 302          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
# 303          54 LOAD_CONST               1 ('report')
#              56 STORE_FAST               3 (@py_assert0)
#              58 LOAD_FAST                3 (@py_assert0)
#              60 LOAD_FAST                2 (config)
#              62 CONTAINS_OP              0
#              64 STORE_FAST               4 (@py_assert2)
#              66 LOAD_FAST                4 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       175 (to 420)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               2 (('in',))
#             102 LOAD_FAST                4 (@py_assert2)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             108 LOAD_FAST                3 (@py_assert0)
#             110 LOAD_FAST                2 (config)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_saferepr)
#             152 LOAD_FAST                3 (@py_assert0)
#             154 CALL                     1
#             162 LOAD_CONST               4 ('config')
#             164 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             174 LOAD_ATTR               12 (locals)
#             194 CALL                     0
#             202 CONTAINS_OP              0
#             204 POP_JUMP_IF_TRUE        21 (to 248)
#             206 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             216 LOAD_ATTR               14 (_should_repr_global_name)
#             236 LOAD_FAST                2 (config)
#             238 CALL                     1
#             246 POP_JUMP_IF_FALSE       21 (to 290)
#         >>  248 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             258 LOAD_ATTR                8 (_saferepr)
#             278 LOAD_FAST                2 (config)
#             280 CALL                     1
#             288 JUMP_FORWARD             1 (to 292)
#         >>  290 LOAD_CONST               4 ('config')
#         >>  292 LOAD_CONST               5 (('py1', 'py3'))
#             294 BUILD_CONST_KEY_MAP      2
#             296 BINARY_OP                6 (%)
#             300 STORE_FAST               5 (@py_format4)
#             302 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             312 LOAD_ATTR               16 (_format_assertmsg)
#             332 LOAD_CONST               6 ("report_generator must have 'report' field")
#             334 CALL                     1
#             342 LOAD_CONST               7 ('\n>assert %(py5)s')
#             344 BINARY_OP                0 (+)
#             348 LOAD_CONST               8 ('py5')
#             350 LOAD_FAST                5 (@py_format4)
#             352 BUILD_MAP                1
#             354 BINARY_OP                6 (%)
#             358 STORE_FAST               6 (@py_format6)
#             360 LOAD_GLOBAL             19 (NULL + AssertionError)
#             370 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             380 LOAD_ATTR               20 (_format_explanation)
#             400 LOAD_FAST                6 (@py_format6)
#             402 CALL                     1
#             410 CALL                     1
#             418 RAISE_VARARGS            1
#         >>  420 LOAD_CONST               9 (None)
#             422 COPY                     1
#             424 STORE_FAST               3 (@py_assert0)
#             426 STORE_FAST               4 (@py_assert2)
#             428 RETURN_CONST             9 (None)
# 
# Disassembly of <code object test_renewable_integration_has_renewable at 0x3aeb9bc0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 305>:
# 305           0 RESUME                   0
# 
# 307           2 LOAD_GLOBAL              1 (NULL + RenewableIntegrationSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 308          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
# 309          54 LOAD_CONST               1 ('renewable')
#              56 STORE_FAST               3 (@py_assert0)
#              58 LOAD_FAST                3 (@py_assert0)
#              60 LOAD_FAST                2 (config)
#              62 CONTAINS_OP              0
#              64 STORE_FAST               4 (@py_assert2)
#              66 LOAD_FAST                4 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       175 (to 420)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               2 (('in',))
#             102 LOAD_FAST                4 (@py_assert2)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             108 LOAD_FAST                3 (@py_assert0)
#             110 LOAD_FAST                2 (config)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_saferepr)
#             152 LOAD_FAST                3 (@py_assert0)
#             154 CALL                     1
#             162 LOAD_CONST               4 ('config')
#             164 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             174 LOAD_ATTR               12 (locals)
#             194 CALL                     0
#             202 CONTAINS_OP              0
#             204 POP_JUMP_IF_TRUE        21 (to 248)
#             206 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             216 LOAD_ATTR               14 (_should_repr_global_name)
#             236 LOAD_FAST                2 (config)
#             238 CALL                     1
#             246 POP_JUMP_IF_FALSE       21 (to 290)
#         >>  248 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             258 LOAD_ATTR                8 (_saferepr)
#             278 LOAD_FAST                2 (config)
#             280 CALL                     1
#             288 JUMP_FORWARD             1 (to 292)
#         >>  290 LOAD_CONST               4 ('config')
#         >>  292 LOAD_CONST               5 (('py1', 'py3'))
#             294 BUILD_CONST_KEY_MAP      2
#             296 BINARY_OP                6 (%)
#             300 STORE_FAST               5 (@py_format4)
#             302 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             312 LOAD_ATTR               16 (_format_assertmsg)
#             332 LOAD_CONST               6 ("renewable_integration must have 'renewable' field")
#             334 CALL                     1
#             342 LOAD_CONST               7 ('\n>assert %(py5)s')
#             344 BINARY_OP                0 (+)
#             348 LOAD_CONST               8 ('py5')
#             350 LOAD_FAST                5 (@py_format4)
#             352 BUILD_MAP                1
#             354 BINARY_OP                6 (%)
#             358 STORE_FAST               6 (@py_format6)
#             360 LOAD_GLOBAL             19 (NULL + AssertionError)
#             370 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             380 LOAD_ATTR               20 (_format_explanation)
#             400 LOAD_FAST                6 (@py_format6)
#             402 CALL                     1
#             410 CALL                     1
#             418 RAISE_VARARGS            1
#         >>  420 LOAD_CONST               9 (None)
#             422 COPY                     1
#             424 STORE_FAST               3 (@py_assert0)
#             426 STORE_FAST               4 (@py_assert2)
#             428 RETURN_CONST             9 (None)
# 
# Disassembly of <code object test_orthogonal_sensitivity_has_parameters_and_target at 0x3aec5210, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 311>:
# 311           0 RESUME                   0
# 
# 313           2 LOAD_GLOBAL              1 (NULL + OrthogonalSensitivitySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 314          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
# 315          54 LOAD_CONST               1 ('parameters')
#              56 STORE_FAST               3 (@py_assert0)
#              58 LOAD_FAST                3 (@py_assert0)
#              60 LOAD_FAST                2 (config)
#              62 CONTAINS_OP              0
#              64 STORE_FAST               4 (@py_assert2)
#              66 LOAD_FAST                4 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       175 (to 420)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               2 (('in',))
#             102 LOAD_FAST                4 (@py_assert2)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             108 LOAD_FAST                3 (@py_assert0)
#             110 LOAD_FAST                2 (config)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_saferepr)
#             152 LOAD_FAST                3 (@py_assert0)
#             154 CALL                     1
#             162 LOAD_CONST               4 ('config')
#             164 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             174 LOAD_ATTR               12 (locals)
#             194 CALL                     0
#             202 CONTAINS_OP              0
#             204 POP_JUMP_IF_TRUE        21 (to 248)
#             206 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             216 LOAD_ATTR               14 (_should_repr_global_name)
#             236 LOAD_FAST                2 (config)
#             238 CALL                     1
#             246 POP_JUMP_IF_FALSE       21 (to 290)
#         >>  248 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             258 LOAD_ATTR                8 (_saferepr)
#             278 LOAD_FAST                2 (config)
#             280 CALL                     1
#             288 JUMP_FORWARD             1 (to 292)
#         >>  290 LOAD_CONST               4 ('config')
#         >>  292 LOAD_CONST               5 (('py1', 'py3'))
#             294 BUILD_CONST_KEY_MAP      2
#             296 BINARY_OP                6 (%)
#             300 STORE_FAST               5 (@py_format4)
#             302 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             312 LOAD_ATTR               16 (_format_assertmsg)
#             332 LOAD_CONST               6 ("orthogonal_sensitivity must have 'parameters' field")
#             334 CALL                     1
#             342 LOAD_CONST               7 ('\n>assert %(py5)s')
#             344 BINARY_OP                0 (+)
#             348 LOAD_CONST               8 ('py5')
#             350 LOAD_FAST                5 (@py_format4)
#             352 BUILD_MAP                1
#             354 BINARY_OP                6 (%)
#             358 STORE_FAST               6 (@py_format6)
#             360 LOAD_GLOBAL             19 (NULL + AssertionError)
#             370 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             380 LOAD_ATTR               20 (_format_explanation)
#             400 LOAD_FAST                6 (@py_format6)
#             402 CALL                     1
#             410 CALL                     1
#             418 RAISE_VARARGS            1
#         >>  420 LOAD_CONST               9 (None)
#             422 COPY                     1
#             424 STORE_FAST               3 (@py_assert0)
#             426 STORE_FAST               4 (@py_assert2)
# 
# 316         428 LOAD_CONST              10 ('target')
#             430 STORE_FAST               3 (@py_assert0)
#             432 LOAD_FAST                3 (@py_assert0)
#             434 LOAD_FAST                2 (config)
#             436 CONTAINS_OP              0
#             438 STORE_FAST               4 (@py_assert2)
#             440 LOAD_FAST                4 (@py_assert2)
#             442 POP_JUMP_IF_TRUE       175 (to 794)
#             444 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             454 LOAD_ATTR                6 (_call_reprcompare)
#             474 LOAD_CONST               2 (('in',))
#             476 LOAD_FAST                4 (@py_assert2)
#             478 BUILD_TUPLE              1
#             480 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             482 LOAD_FAST                3 (@py_assert0)
#             484 LOAD_FAST                2 (config)
#             486 BUILD_TUPLE              2
#             488 CALL                     4
#             496 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             506 LOAD_ATTR                8 (_saferepr)
#             526 LOAD_FAST                3 (@py_assert0)
#             528 CALL                     1
#             536 LOAD_CONST               4 ('config')
#             538 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             548 LOAD_ATTR               12 (locals)
#             568 CALL                     0
#             576 CONTAINS_OP              0
#             578 POP_JUMP_IF_TRUE        21 (to 622)
#             580 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             590 LOAD_ATTR               14 (_should_repr_global_name)
#             610 LOAD_FAST                2 (config)
#             612 CALL                     1
#             620 POP_JUMP_IF_FALSE       21 (to 664)
#         >>  622 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             632 LOAD_ATTR                8 (_saferepr)
#             652 LOAD_FAST                2 (config)
#             654 CALL                     1
#             662 JUMP_FORWARD             1 (to 666)
#         >>  664 LOAD_CONST               4 ('config')
#         >>  666 LOAD_CONST               5 (('py1', 'py3'))
#             668 BUILD_CONST_KEY_MAP      2
#             670 BINARY_OP                6 (%)
#             674 STORE_FAST               5 (@py_format4)
#             676 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             686 LOAD_ATTR               16 (_format_assertmsg)
#             706 LOAD_CONST              11 ("orthogonal_sensitivity must have 'target' field")
#             708 CALL                     1
#             716 LOAD_CONST               7 ('\n>assert %(py5)s')
#             718 BINARY_OP                0 (+)
#             722 LOAD_CONST               8 ('py5')
#             724 LOAD_FAST                5 (@py_format4)
#             726 BUILD_MAP                1
#             728 BINARY_OP                6 (%)
#             732 STORE_FAST               6 (@py_format6)
#             734 LOAD_GLOBAL             19 (NULL + AssertionError)
#             744 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             754 LOAD_ATTR               20 (_format_explanation)
#             774 LOAD_FAST                6 (@py_format6)
#             776 CALL                     1
#             784 CALL                     1
#             792 RAISE_VARARGS            1
#         >>  794 LOAD_CONST               9 (None)
#             796 COPY                     1
#             798 STORE_FAST               3 (@py_assert0)
#             800 STORE_FAST               4 (@py_assert2)
#             802 RETURN_CONST             9 (None)
# 
# Disassembly of <code object test_component_catalog_has_filters_and_options at 0x3aea9820, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 318>:
# 318           0 RESUME                   0
# 
# 320           2 LOAD_GLOBAL              1 (NULL + ComponentCatalogSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 321          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
# 322          54 LOAD_CONST               1 ('filters')
#              56 STORE_FAST               3 (@py_assert0)
#              58 LOAD_FAST                3 (@py_assert0)
#              60 LOAD_FAST                2 (config)
#              62 CONTAINS_OP              0
#              64 STORE_FAST               4 (@py_assert2)
#              66 LOAD_FAST                4 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       175 (to 420)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               2 (('in',))
#             102 LOAD_FAST                4 (@py_assert2)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             108 LOAD_FAST                3 (@py_assert0)
#             110 LOAD_FAST                2 (config)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_saferepr)
#             152 LOAD_FAST                3 (@py_assert0)
#             154 CALL                     1
#             162 LOAD_CONST               4 ('config')
#             164 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             174 LOAD_ATTR               12 (locals)
#             194 CALL                     0
#             202 CONTAINS_OP              0
#             204 POP_JUMP_IF_TRUE        21 (to 248)
#             206 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             216 LOAD_ATTR               14 (_should_repr_global_name)
#             236 LOAD_FAST                2 (config)
#             238 CALL                     1
#             246 POP_JUMP_IF_FALSE       21 (to 290)
#         >>  248 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             258 LOAD_ATTR                8 (_saferepr)
#             278 LOAD_FAST                2 (config)
#             280 CALL                     1
#             288 JUMP_FORWARD             1 (to 292)
#         >>  290 LOAD_CONST               4 ('config')
#         >>  292 LOAD_CONST               5 (('py1', 'py3'))
#             294 BUILD_CONST_KEY_MAP      2
#             296 BINARY_OP                6 (%)
#             300 STORE_FAST               5 (@py_format4)
#             302 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             312 LOAD_ATTR               16 (_format_assertmsg)
#             332 LOAD_CONST               6 ("component_catalog must have 'filters' field")
#             334 CALL                     1
#             342 LOAD_CONST               7 ('\n>assert %(py5)s')
#             344 BINARY_OP                0 (+)
#             348 LOAD_CONST               8 ('py5')
#             350 LOAD_FAST                5 (@py_format4)
#             352 BUILD_MAP                1
#             354 BINARY_OP                6 (%)
#             358 STORE_FAST               6 (@py_format6)
#             360 LOAD_GLOBAL             19 (NULL + AssertionError)
#             370 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             380 LOAD_ATTR               20 (_format_explanation)
#             400 LOAD_FAST                6 (@py_format6)
#             402 CALL                     1
#             410 CALL                     1
#             418 RAISE_VARARGS            1
#         >>  420 LOAD_CONST               9 (None)
#             422 COPY                     1
#             424 STORE_FAST               3 (@py_assert0)
#             426 STORE_FAST               4 (@py_assert2)
# 
# 323         428 LOAD_CONST              10 ('options')
#             430 STORE_FAST               3 (@py_assert0)
#             432 LOAD_FAST                3 (@py_assert0)
#             434 LOAD_FAST                2 (config)
#             436 CONTAINS_OP              0
#             438 STORE_FAST               4 (@py_assert2)
#             440 LOAD_FAST                4 (@py_assert2)
#             442 POP_JUMP_IF_TRUE       175 (to 794)
#             444 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             454 LOAD_ATTR                6 (_call_reprcompare)
#             474 LOAD_CONST               2 (('in',))
#             476 LOAD_FAST                4 (@py_assert2)
#             478 BUILD_TUPLE              1
#             480 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             482 LOAD_FAST                3 (@py_assert0)
#             484 LOAD_FAST                2 (config)
#             486 BUILD_TUPLE              2
#             488 CALL                     4
#             496 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             506 LOAD_ATTR                8 (_saferepr)
#             526 LOAD_FAST                3 (@py_assert0)
#             528 CALL                     1
#             536 LOAD_CONST               4 ('config')
#             538 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             548 LOAD_ATTR               12 (locals)
#             568 CALL                     0
#             576 CONTAINS_OP              0
#             578 POP_JUMP_IF_TRUE        21 (to 622)
#             580 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             590 LOAD_ATTR               14 (_should_repr_global_name)
#             610 LOAD_FAST                2 (config)
#             612 CALL                     1
#             620 POP_JUMP_IF_FALSE       21 (to 664)
#         >>  622 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             632 LOAD_ATTR                8 (_saferepr)
#             652 LOAD_FAST                2 (config)
#             654 CALL                     1
#             662 JUMP_FORWARD             1 (to 666)
#         >>  664 LOAD_CONST               4 ('config')
#         >>  666 LOAD_CONST               5 (('py1', 'py3'))
#             668 BUILD_CONST_KEY_MAP      2
#             670 BINARY_OP                6 (%)
#             674 STORE_FAST               5 (@py_format4)
#             676 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             686 LOAD_ATTR               16 (_format_assertmsg)
#             706 LOAD_CONST              11 ("component_catalog must have 'options' field")
#             708 CALL                     1
#             716 LOAD_CONST               7 ('\n>assert %(py5)s')
#             718 BINARY_OP                0 (+)
#             722 LOAD_CONST               8 ('py5')
#             724 LOAD_FAST                5 (@py_format4)
#             726 BUILD_MAP                1
#             728 BINARY_OP                6 (%)
#             732 STORE_FAST               6 (@py_format6)
#             734 LOAD_GLOBAL             19 (NULL + AssertionError)
#             744 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             754 LOAD_ATTR               20 (_format_explanation)
#             774 LOAD_FAST                6 (@py_format6)
#             776 CALL                     1
#             784 CALL                     1
#             792 RAISE_VARARGS            1
#         >>  794 LOAD_CONST               9 (None)
#             796 COPY                     1
#             798 STORE_FAST               3 (@py_assert0)
#             800 STORE_FAST               4 (@py_assert2)
#             802 RETURN_CONST             9 (None)
# 
# Disassembly of <code object test_model_builder_has_workflow_and_base_model at 0x3aece640, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skill_config_integrity.py", line 325>:
# 325           0 RESUME                   0
# 
# 327           2 LOAD_GLOBAL              1 (NULL + ModelBuilderSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 328          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
# 329          54 LOAD_CONST               1 ('workflow')
#              56 STORE_FAST               3 (@py_assert0)
#              58 LOAD_FAST                3 (@py_assert0)
#              60 LOAD_FAST                2 (config)
#              62 CONTAINS_OP              0
#              64 STORE_FAST               4 (@py_assert2)
#              66 LOAD_FAST                4 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       175 (to 420)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               2 (('in',))
#             102 LOAD_FAST                4 (@py_assert2)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             108 LOAD_FAST                3 (@py_assert0)
#             110 LOAD_FAST                2 (config)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_saferepr)
#             152 LOAD_FAST                3 (@py_assert0)
#             154 CALL                     1
#             162 LOAD_CONST               4 ('config')
#             164 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             174 LOAD_ATTR               12 (locals)
#             194 CALL                     0
#             202 CONTAINS_OP              0
#             204 POP_JUMP_IF_TRUE        21 (to 248)
#             206 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             216 LOAD_ATTR               14 (_should_repr_global_name)
#             236 LOAD_FAST                2 (config)
#             238 CALL                     1
#             246 POP_JUMP_IF_FALSE       21 (to 290)
#         >>  248 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             258 LOAD_ATTR                8 (_saferepr)
#             278 LOAD_FAST                2 (config)
#             280 CALL                     1
#             288 JUMP_FORWARD             1 (to 292)
#         >>  290 LOAD_CONST               4 ('config')
#         >>  292 LOAD_CONST               5 (('py1', 'py3'))
#             294 BUILD_CONST_KEY_MAP      2
#             296 BINARY_OP                6 (%)
#             300 STORE_FAST               5 (@py_format4)
#             302 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             312 LOAD_ATTR               16 (_format_assertmsg)
#             332 LOAD_CONST               6 ("model_builder must have 'workflow' field")
#             334 CALL                     1
#             342 LOAD_CONST               7 ('\n>assert %(py5)s')
#             344 BINARY_OP                0 (+)
#             348 LOAD_CONST               8 ('py5')
#             350 LOAD_FAST                5 (@py_format4)
#             352 BUILD_MAP                1
#             354 BINARY_OP                6 (%)
#             358 STORE_FAST               6 (@py_format6)
#             360 LOAD_GLOBAL             19 (NULL + AssertionError)
#             370 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             380 LOAD_ATTR               20 (_format_explanation)
#             400 LOAD_FAST                6 (@py_format6)
#             402 CALL                     1
#             410 CALL                     1
#             418 RAISE_VARARGS            1
#         >>  420 LOAD_CONST               9 (None)
#             422 COPY                     1
#             424 STORE_FAST               3 (@py_assert0)
#             426 STORE_FAST               4 (@py_assert2)
# 
# 330         428 LOAD_CONST              10 ('base_model')
#             430 STORE_FAST               3 (@py_assert0)
#             432 LOAD_FAST                3 (@py_assert0)
#             434 LOAD_FAST                2 (config)
#             436 CONTAINS_OP              0
#             438 STORE_FAST               4 (@py_assert2)
#             440 LOAD_FAST                4 (@py_assert2)
#             442 POP_JUMP_IF_TRUE       175 (to 794)
#             444 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             454 LOAD_ATTR                6 (_call_reprcompare)
#             474 LOAD_CONST               2 (('in',))
#             476 LOAD_FAST                4 (@py_assert2)
#             478 BUILD_TUPLE              1
#             480 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             482 LOAD_FAST                3 (@py_assert0)
#             484 LOAD_FAST                2 (config)
#             486 BUILD_TUPLE              2
#             488 CALL                     4
#             496 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             506 LOAD_ATTR                8 (_saferepr)
#             526 LOAD_FAST                3 (@py_assert0)
#             528 CALL                     1
#             536 LOAD_CONST               4 ('config')
#             538 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             548 LOAD_ATTR               12 (locals)
#             568 CALL                     0
#             576 CONTAINS_OP              0
#             578 POP_JUMP_IF_TRUE        21 (to 622)
#             580 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             590 LOAD_ATTR               14 (_should_repr_global_name)
#             610 LOAD_FAST                2 (config)
#             612 CALL                     1
#             620 POP_JUMP_IF_FALSE       21 (to 664)
#         >>  622 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             632 LOAD_ATTR                8 (_saferepr)
#             652 LOAD_FAST                2 (config)
#             654 CALL                     1
#             662 JUMP_FORWARD             1 (to 666)
#         >>  664 LOAD_CONST               4 ('config')
#         >>  666 LOAD_CONST               5 (('py1', 'py3'))
#             668 BUILD_CONST_KEY_MAP      2
#             670 BINARY_OP                6 (%)
#             674 STORE_FAST               5 (@py_format4)
#             676 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             686 LOAD_ATTR               16 (_format_assertmsg)
#             706 LOAD_CONST              11 ("model_builder must have 'base_model' field")
#             708 CALL                     1
#             716 LOAD_CONST               7 ('\n>assert %(py5)s')
#             718 BINARY_OP                0 (+)
#             722 LOAD_CONST               8 ('py5')
#             724 LOAD_FAST                5 (@py_format4)
#             726 BUILD_MAP                1
#             728 BINARY_OP                6 (%)
#             732 STORE_FAST               6 (@py_format6)
#             734 LOAD_GLOBAL             19 (NULL + AssertionError)
#             744 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             754 LOAD_ATTR               20 (_format_explanation)
#             774 LOAD_FAST                6 (@py_format6)
#             776 CALL                     1
#             784 CALL                     1
#             792 RAISE_VARARGS            1
#         >>  794 LOAD_CONST               9 (None)
#             796 COPY                     1
#             798 STORE_FAST               3 (@py_assert0)
#             800 STORE_FAST               4 (@py_assert2)
# 
# 331         802 LOAD_CONST              12 ('modifications')
#             804 STORE_FAST               3 (@py_assert0)
#             806 LOAD_FAST                3 (@py_assert0)
#             808 LOAD_FAST                2 (config)
#             810 CONTAINS_OP              0
#             812 STORE_FAST               4 (@py_assert2)
#             814 LOAD_FAST                4 (@py_assert2)
#             816 POP_JUMP_IF_TRUE       175 (to 1168)
#             818 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             828 LOAD_ATTR                6 (_call_reprcompare)
#             848 LOAD_CONST               2 (('in',))
#             850 LOAD_FAST                4 (@py_assert2)
#             852 BUILD_TUPLE              1
#             854 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             856 LOAD_FAST                3 (@py_assert0)
#             858 LOAD_FAST                2 (config)
#             860 BUILD_TUPLE              2
#             862 CALL                     4
#             870 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             880 LOAD_ATTR                8 (_saferepr)
#             900 LOAD_FAST                3 (@py_assert0)
#             902 CALL                     1
#             910 LOAD_CONST               4 ('config')
#             912 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             922 LOAD_ATTR               12 (locals)
#             942 CALL                     0
#             950 CONTAINS_OP              0
#             952 POP_JUMP_IF_TRUE        21 (to 996)
#             954 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             964 LOAD_ATTR               14 (_should_repr_global_name)
#             984 LOAD_FAST                2 (config)
#             986 CALL                     1
#             994 POP_JUMP_IF_FALSE       21 (to 1038)
#         >>  996 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1006 LOAD_ATTR                8 (_saferepr)
#            1026 LOAD_FAST                2 (config)
#            1028 CALL                     1
#            1036 JUMP_FORWARD             1 (to 1040)
#         >> 1038 LOAD_CONST               4 ('config')
#         >> 1040 LOAD_CONST               5 (('py1', 'py3'))
#            1042 BUILD_CONST_KEY_MAP      2
#            1044 BINARY_OP                6 (%)
#            1048 STORE_FAST               5 (@py_format4)
#            1050 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1060 LOAD_ATTR               16 (_format_assertmsg)
#            1080 LOAD_CONST              13 ("model_builder must have 'modifications' field")
#            1082 CALL                     1
#            1090 LOAD_CONST               7 ('\n>assert %(py5)s')
#            1092 BINARY_OP                0 (+)
#            1096 LOAD_CONST               8 ('py5')
#            1098 LOAD_FAST                5 (@py_format4)
#            1100 BUILD_MAP                1
#            1102 BINARY_OP                6 (%)
#            1106 STORE_FAST               6 (@py_format6)
#            1108 LOAD_GLOBAL             19 (NULL + AssertionError)
#            1118 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1128 LOAD_ATTR               20 (_format_explanation)
#            1148 LOAD_FAST                6 (@py_format6)
#            1150 CALL                     1
#            1158 CALL                     1
#            1166 RAISE_VARARGS            1
#         >> 1168 LOAD_CONST               9 (None)
#            1170 COPY                     1
#            1172 STORE_FAST               3 (@py_assert0)
#            1174 STORE_FAST               4 (@py_assert2)
#            1176 RETURN_CONST             9 (None)
# 