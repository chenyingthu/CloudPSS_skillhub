# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/__pycache__/test_power_flow.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


class MockPowerFlowAdapter:
    """MockPowerFlowAdapter"""
    def __init__(self):
        pass
    def engine_name(self):
        pass  # TODO: restore

    def _do_connect(self):
        pass  # TODO: restore

    def _do_disconnect(self):
        pass  # TODO: restore

    def _do_load_model(self, model_id):
        pass  # TODO: restore

    def _do_run_simulation(self, config):
        pass  # TODO: restore

    def _do_get_result(self, job_id):
        pass  # TODO: restore

    def _do_validate_config(self, config):
        pass  # TODO: restore


def TestPowerFlowPreset():
    """TestPowerFlowPreset"""
pass  # TODO: restore


def TestPowerFlowPresetRun():
    """TestPowerFlowPresetRun"""
pass  # TODO: restore


def TestGenerateSummary():
    """TestGenerateSummary"""
pass  # TODO: restore


def TestPowerFlowPresetIntegration():
    """TestPowerFlowPresetIntegration"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('Tests for migrated PowerFlowPreset v2.')
#               4 STORE_NAME               0 (__doc__)
# 
#   3           6 LOAD_CONST               1 (0)
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
#   4          40 LOAD_CONST               1 (0)
#              42 LOAD_CONST               3 (('Mock', 'patch', 'MagicMock'))
#              44 IMPORT_NAME              8 (unittest.mock)
#              46 IMPORT_FROM              9 (Mock)
#              48 STORE_NAME               9 (Mock)
#              50 IMPORT_FROM             10 (patch)
#              52 STORE_NAME              10 (patch)
#              54 IMPORT_FROM             11 (MagicMock)
#              56 STORE_NAME              11 (MagicMock)
#              58 POP_TOP
# 
#   5          60 LOAD_CONST               1 (0)
#              62 LOAD_CONST               4 (('SimulationStatus', 'SimulationResult', 'ValidationResult', 'EngineAdapter', 'EngineConfig'))
#              64 IMPORT_NAME             12 (cloudpss_skills_v2.powerapi)
#              66 IMPORT_FROM             13 (SimulationStatus)
#              68 STORE_NAME              13 (SimulationStatus)
#              70 IMPORT_FROM             14 (SimulationResult)
#              72 STORE_NAME              14 (SimulationResult)
#              74 IMPORT_FROM             15 (ValidationResult)
#              76 STORE_NAME              15 (ValidationResult)
#              78 IMPORT_FROM             16 (EngineAdapter)
#              80 STORE_NAME              16 (EngineAdapter)
#              82 IMPORT_FROM             17 (EngineConfig)
#              84 STORE_NAME              17 (EngineConfig)
#              86 POP_TOP
# 
#  12          88 LOAD_CONST               1 (0)
#              90 LOAD_CONST               5 (('PowerFlowPreset', 'create_skill'))
#              92 IMPORT_NAME             18 (cloudpss_skills_v2.presets.power_flow)
#              94 IMPORT_FROM             19 (PowerFlowPreset)
#              96 STORE_NAME              19 (PowerFlowPreset)
#              98 IMPORT_FROM             20 (create_skill)
#             100 STORE_NAME              20 (create_skill)
#             102 POP_TOP
# 
#  15         104 PUSH_NULL
#             106 LOAD_BUILD_CLASS
#             108 LOAD_CONST               6 (<code object MockPowerFlowAdapter at 0x73cd93b39c50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 15>)
#             110 MAKE_FUNCTION            0
#             112 LOAD_CONST               7 ('MockPowerFlowAdapter')
#             114 LOAD_NAME               16 (EngineAdapter)
#             116 CALL                     3
#             124 STORE_NAME              21 (MockPowerFlowAdapter)
# 
#  64         126 PUSH_NULL
#             128 LOAD_BUILD_CLASS
#             130 LOAD_CONST               8 (<code object TestPowerFlowPreset at 0x73cd93b31730, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 64>)
#             132 MAKE_FUNCTION            0
#             134 LOAD_CONST               9 ('TestPowerFlowPreset')
#             136 CALL                     2
#             144 STORE_NAME              22 (TestPowerFlowPreset)
# 
# 117         146 PUSH_NULL
#             148 LOAD_BUILD_CLASS
#             150 LOAD_CONST              10 (<code object TestPowerFlowPresetRun at 0x73cd93b44fa0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 117>)
#             152 MAKE_FUNCTION            0
#             154 LOAD_CONST              11 ('TestPowerFlowPresetRun')
#             156 CALL                     2
#             164 STORE_NAME              23 (TestPowerFlowPresetRun)
# 
# 164         166 PUSH_NULL
#             168 LOAD_BUILD_CLASS
#             170 LOAD_CONST              12 (<code object TestGenerateSummary at 0x73cd93b064c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 164>)
#             172 MAKE_FUNCTION            0
#             174 LOAD_CONST              13 ('TestGenerateSummary')
#             176 CALL                     2
#             184 STORE_NAME              24 (TestGenerateSummary)
# 
# 203         186 PUSH_NULL
#             188 LOAD_BUILD_CLASS
#             190 LOAD_CONST              14 (<code object TestPowerFlowPresetIntegration at 0x73cd945fedb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 203>)
#             192 MAKE_FUNCTION            0
#             194 LOAD_CONST              15 ('TestPowerFlowPresetIntegration')
#             196 CALL                     2
#             204 STORE_NAME              25 (TestPowerFlowPresetIntegration)
#             206 RETURN_CONST             2 (None)
# 
# Disassembly of <code object MockPowerFlowAdapter at 0x73cd93b39c50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 15>:
#               0 MAKE_CELL                0 (__class__)
# 
#  15           2 RESUME                   0
#               4 LOAD_NAME                0 (__name__)
#               6 STORE_NAME               1 (__module__)
#               8 LOAD_CONST               0 ('MockPowerFlowAdapter')
#              10 STORE_NAME               2 (__qualname__)
# 
#  16          12 LOAD_CONST               1 ('Mock adapter for testing PowerFlowPreset.')
#              14 STORE_NAME               3 (__doc__)
# 
#  18          16 LOAD_CLOSURE             0 (__class__)
#              18 BUILD_TUPLE              1
#              20 LOAD_CONST               2 (<code object __init__ at 0x73cd93b1e340, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 18>)
#              22 MAKE_FUNCTION            8 (closure)
#              24 STORE_NAME               4 (__init__)
# 
#  22          26 LOAD_NAME                5 (property)
# 
#  23          28 LOAD_CONST               3 (<code object engine_name at 0x73cd93b131c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 22>)
#              30 MAKE_FUNCTION            0
# 
#  22          32 CALL                     0
# 
#  23          40 STORE_NAME               6 (engine_name)
# 
#  26          42 LOAD_CONST               4 (<code object _do_connect at 0x73cd945fe090, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 26>)
#              44 MAKE_FUNCTION            0
#              46 STORE_NAME               7 (_do_connect)
# 
#  29          48 LOAD_CONST               5 (<code object _do_disconnect at 0x73cd945fe330, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 29>)
#              50 MAKE_FUNCTION            0
#              52 STORE_NAME               8 (_do_disconnect)
# 
#  32          54 LOAD_CONST               6 (<code object _do_load_model at 0x73cd93b13290, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 32>)
#              56 MAKE_FUNCTION            0
#              58 STORE_NAME               9 (_do_load_model)
# 
#  35          60 LOAD_CONST               7 (<code object _do_run_simulation at 0x73cd945b92f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 35>)
#              62 MAKE_FUNCTION            0
#              64 STORE_NAME              10 (_do_run_simulation)
# 
#  53          66 LOAD_CONST               8 (<code object _do_get_result at 0x73cd93b31430, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 53>)
#              68 MAKE_FUNCTION            0
#              70 STORE_NAME              11 (_do_get_result)
# 
#  60          72 LOAD_CONST               9 (<code object _do_validate_config at 0x73cd945fe790, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 60>)
#              74 MAKE_FUNCTION            0
#              76 STORE_NAME              12 (_do_validate_config)
#              78 LOAD_CLOSURE             0 (__class__)
#              80 COPY                     1
#              82 STORE_NAME              13 (__classcell__)
#              84 RETURN_VALUE
# 
# Disassembly of <code object __init__ at 0x73cd93b1e340, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 18>:
#               0 COPY_FREE_VARS           1
# 
#  18           2 RESUME                   0
# 
#  19           4 LOAD_GLOBAL              0 (super)
#              14 LOAD_DEREF               1 (__class__)
#              16 LOAD_FAST                0 (self)
#              18 LOAD_SUPER_ATTR          5 (NULL|self + __init__)
#              22 LOAD_GLOBAL              5 (NULL + EngineConfig)
#              32 LOAD_CONST               1 ('mock')
#              34 KW_NAMES                 2 (('engine_name',))
#              36 CALL                     1
#              44 CALL                     1
#              52 POP_TOP
# 
#  20          54 LOAD_CONST               3 (False)
#              56 LOAD_FAST                0 (self)
#              58 STORE_ATTR               3 (_connected)
#              68 RETURN_CONST             0 (None)
# 
# Disassembly of <code object engine_name at 0x73cd93b131c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 22>:
#  22           0 RESUME                   0
# 
#  24           2 RETURN_CONST             1 ('mock')
# 
# Disassembly of <code object _do_connect at 0x73cd945fe090, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 26>:
#  26           0 RESUME                   0
# 
#  27           2 LOAD_CONST               1 (True)
#               4 LOAD_FAST                0 (self)
#               6 STORE_ATTR               0 (_connected)
#              16 RETURN_CONST             0 (None)
# 
# Disassembly of <code object _do_disconnect at 0x73cd945fe330, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 29>:
#  29           0 RESUME                   0
# 
#  30           2 LOAD_CONST               1 (False)
#               4 LOAD_FAST                0 (self)
#               6 STORE_ATTR               0 (_connected)
#              16 RETURN_CONST             0 (None)
# 
# Disassembly of <code object _do_load_model at 0x73cd93b13290, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 32>:
#  32           0 RESUME                   0
# 
#  33           2 RETURN_CONST             1 (True)
# 
# Disassembly of <code object _do_run_simulation at 0x73cd945b92f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 35>:
#  35           0 RESUME                   0
# 
#  36           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
#  37          12 LOAD_CONST               1 ('mock-job-123')
# 
#  38          14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
# 
#  41          44 LOAD_CONST               2 (1)
#              46 LOAD_CONST               3 ('Bus1')
#              48 LOAD_CONST               4 (1.05)
#              50 LOAD_CONST               5 (100.0)
#              52 LOAD_CONST               6 (50.0)
#              54 LOAD_CONST               7 (('id', 'name', 'Vm', 'Pg', 'Pl'))
#              56 BUILD_CONST_KEY_MAP      5
# 
#  42          58 LOAD_CONST               8 (2)
#              60 LOAD_CONST               9 ('Bus2')
#              62 LOAD_CONST              10 (1.02)
#              64 LOAD_CONST               6 (50.0)
#              66 LOAD_CONST              11 (30.0)
#              68 LOAD_CONST               7 (('id', 'name', 'Vm', 'Pg', 'Pl'))
#              70 BUILD_CONST_KEY_MAP      5
# 
#  43          72 LOAD_CONST              12 (3)
#              74 LOAD_CONST              13 ('Bus3')
#              76 LOAD_CONST              14 (0.98)
#              78 LOAD_CONST              15 (0.0)
#              80 LOAD_CONST              16 (40.0)
#              82 LOAD_CONST               7 (('id', 'name', 'Vm', 'Pg', 'Pl'))
#              84 BUILD_CONST_KEY_MAP      5
# 
#  40          86 BUILD_LIST               3
# 
#  46          88 LOAD_CONST               2 (1)
#              90 LOAD_CONST               8 (2)
#              92 LOAD_CONST              17 (2.5)
#              94 LOAD_CONST              18 (('from', 'to', 'Ploss'))
#              96 BUILD_CONST_KEY_MAP      3
# 
#  47          98 LOAD_CONST               8 (2)
#             100 LOAD_CONST              12 (3)
#             102 LOAD_CONST              19 (1.5)
#             104 LOAD_CONST              18 (('from', 'to', 'Ploss'))
#             106 BUILD_CONST_KEY_MAP      3
# 
#  45         108 BUILD_LIST               2
# 
#  49         110 BUILD_MAP                0
# 
#  39         112 LOAD_CONST              20 (('buses', 'branches', 'summary'))
#             114 BUILD_CONST_KEY_MAP      3
# 
#  36         116 KW_NAMES                21 (('job_id', 'status', 'data'))
#             118 CALL                     3
#             126 RETURN_VALUE
# 
# Disassembly of <code object _do_get_result at 0x73cd93b31430, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 53>:
#  53           0 RESUME                   0
# 
#  54           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
#  55          12 LOAD_FAST                1 (job_id)
# 
#  56          14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
# 
#  57          44 BUILD_LIST               0
#              46 BUILD_LIST               0
#              48 LOAD_CONST               1 (('buses', 'branches'))
#              50 BUILD_CONST_KEY_MAP      2
# 
#  54          52 KW_NAMES                 2 (('job_id', 'status', 'data'))
#              54 CALL                     3
#              62 RETURN_VALUE
# 
# Disassembly of <code object _do_validate_config at 0x73cd945fe790, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 60>:
#  60           0 RESUME                   0
# 
#  61           2 LOAD_GLOBAL              1 (NULL + ValidationResult)
#              12 LOAD_CONST               1 (True)
#              14 KW_NAMES                 2 (('valid',))
#              16 CALL                     1
#              24 RETURN_VALUE
# 
# Disassembly of <code object TestPowerFlowPreset at 0x73cd93b31730, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 64>:
#  64           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestPowerFlowPreset')
#               8 STORE_NAME               2 (__qualname__)
# 
#  65          10 LOAD_CONST               1 ('Tests for PowerFlowPreset.')
#              12 STORE_NAME               3 (__doc__)
# 
#  67          14 LOAD_CONST               2 (<code object test_create_skill at 0x3af3a3e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 67>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_create_skill)
# 
#  72          20 LOAD_CONST               3 (<code object test_create_skill_factory at 0x3afa2710, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 72>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_create_skill_factory)
# 
#  76          26 LOAD_CONST               4 (<code object test_default_config at 0x3afa5a90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 76>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_default_config)
# 
#  84          32 LOAD_CONST               5 (<code object test_config_schema at 0x3afa0150, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 84>)
#              34 MAKE_FUNCTION            0
#              36 STORE_NAME               7 (test_config_schema)
# 
#  91          38 LOAD_CONST               6 (<code object test_validate_valid_config at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 91>)
#              40 MAKE_FUNCTION            0
#              42 STORE_NAME               8 (test_validate_valid_config)
# 
#  97          44 LOAD_CONST               7 (<code object test_validate_missing_model at 0x3afa6030, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 97>)
#              46 MAKE_FUNCTION            0
#              48 STORE_NAME               9 (test_validate_missing_model)
# 
# 104          50 LOAD_CONST               8 (<code object test_validate_missing_rid at 0x3af90d20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 104>)
#              52 MAKE_FUNCTION            0
#              54 STORE_NAME              10 (test_validate_missing_rid)
# 
# 110          56 LOAD_CONST               9 (<code object test_validate_invalid_tolerance at 0x3af3fb70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 110>)
#              58 MAKE_FUNCTION            0
#              60 STORE_NAME              11 (test_validate_invalid_tolerance)
#              62 RETURN_CONST            10 (None)
# 
# Disassembly of <code object test_create_skill at 0x3af3a3e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 67>:
#  67           0 RESUME                   0
# 
#  68           2 LOAD_GLOBAL              1 (NULL + PowerFlowPreset)
#              12 LOAD_CONST               1 ('cloudpss')
#              14 KW_NAMES                 2 (('engine',))
#              16 CALL                     1
#              24 STORE_FAST               1 (skill)
# 
#  69          26 LOAD_FAST                1 (skill)
#              28 LOAD_ATTR                2 (name)
#              48 STORE_FAST               2 (@py_assert1)
#              50 LOAD_CONST               3 ('power_flow')
#              52 STORE_FAST               3 (@py_assert4)
#              54 LOAD_FAST                2 (@py_assert1)
#              56 LOAD_FAST                3 (@py_assert4)
#              58 COMPARE_OP              40 (==)
#              62 STORE_FAST               4 (@py_assert3)
#              64 LOAD_FAST                4 (@py_assert3)
#              66 POP_JUMP_IF_TRUE       173 (to 414)
#              68 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              78 LOAD_ATTR                6 (_call_reprcompare)
#              98 LOAD_CONST               4 (('==',))
#             100 LOAD_FAST                4 (@py_assert3)
#             102 BUILD_TUPLE              1
#             104 LOAD_CONST               5 (('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s',))
#             106 LOAD_FAST                2 (@py_assert1)
#             108 LOAD_FAST                3 (@py_assert4)
#             110 BUILD_TUPLE              2
#             112 CALL                     4
#             120 LOAD_CONST               6 ('skill')
#             122 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             132 LOAD_ATTR               10 (locals)
#             152 CALL                     0
#             160 CONTAINS_OP              0
#             162 POP_JUMP_IF_TRUE        21 (to 206)
#             164 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             174 LOAD_ATTR               12 (_should_repr_global_name)
#             194 LOAD_FAST                1 (skill)
#             196 CALL                     1
#             204 POP_JUMP_IF_FALSE       21 (to 248)
#         >>  206 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             216 LOAD_ATTR               14 (_saferepr)
#             236 LOAD_FAST                1 (skill)
#             238 CALL                     1
#             246 JUMP_FORWARD             1 (to 250)
#         >>  248 LOAD_CONST               6 ('skill')
#         >>  250 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             260 LOAD_ATTR               14 (_saferepr)
#             280 LOAD_FAST                2 (@py_assert1)
#             282 CALL                     1
#             290 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             300 LOAD_ATTR               14 (_saferepr)
#             320 LOAD_FAST                3 (@py_assert4)
#             322 CALL                     1
#             330 LOAD_CONST               7 (('py0', 'py2', 'py5'))
#             332 BUILD_CONST_KEY_MAP      3
#             334 BINARY_OP                6 (%)
#             338 STORE_FAST               5 (@py_format6)
#             340 LOAD_CONST               8 ('assert %(py7)s')
#             342 LOAD_CONST               9 ('py7')
#             344 LOAD_FAST                5 (@py_format6)
#             346 BUILD_MAP                1
#             348 BINARY_OP                6 (%)
#             352 STORE_FAST               6 (@py_format8)
#             354 LOAD_GLOBAL             17 (NULL + AssertionError)
#             364 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             374 LOAD_ATTR               18 (_format_explanation)
#             394 LOAD_FAST                6 (@py_format8)
#             396 CALL                     1
#             404 CALL                     1
#             412 RAISE_VARARGS            1
#         >>  414 LOAD_CONST               0 (None)
#             416 COPY                     1
#             418 STORE_FAST               2 (@py_assert1)
#             420 COPY                     1
#             422 STORE_FAST               4 (@py_assert3)
#             424 STORE_FAST               3 (@py_assert4)
# 
#  70         426 LOAD_FAST                1 (skill)
#             428 LOAD_ATTR               20 (_engine)
#             448 STORE_FAST               2 (@py_assert1)
#             450 LOAD_CONST               1 ('cloudpss')
#             452 STORE_FAST               3 (@py_assert4)
#             454 LOAD_FAST                2 (@py_assert1)
#             456 LOAD_FAST                3 (@py_assert4)
#             458 COMPARE_OP              40 (==)
#             462 STORE_FAST               4 (@py_assert3)
#             464 LOAD_FAST                4 (@py_assert3)
#             466 POP_JUMP_IF_TRUE       173 (to 814)
#             468 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             478 LOAD_ATTR                6 (_call_reprcompare)
#             498 LOAD_CONST               4 (('==',))
#             500 LOAD_FAST                4 (@py_assert3)
#             502 BUILD_TUPLE              1
#             504 LOAD_CONST              10 (('%(py2)s\n{%(py2)s = %(py0)s._engine\n} == %(py5)s',))
#             506 LOAD_FAST                2 (@py_assert1)
#             508 LOAD_FAST                3 (@py_assert4)
#             510 BUILD_TUPLE              2
#             512 CALL                     4
#             520 LOAD_CONST               6 ('skill')
#             522 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             532 LOAD_ATTR               10 (locals)
#             552 CALL                     0
#             560 CONTAINS_OP              0
#             562 POP_JUMP_IF_TRUE        21 (to 606)
#             564 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             574 LOAD_ATTR               12 (_should_repr_global_name)
#             594 LOAD_FAST                1 (skill)
#             596 CALL                     1
#             604 POP_JUMP_IF_FALSE       21 (to 648)
#         >>  606 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             616 LOAD_ATTR               14 (_saferepr)
#             636 LOAD_FAST                1 (skill)
#             638 CALL                     1
#             646 JUMP_FORWARD             1 (to 650)
#         >>  648 LOAD_CONST               6 ('skill')
#         >>  650 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             660 LOAD_ATTR               14 (_saferepr)
#             680 LOAD_FAST                2 (@py_assert1)
#             682 CALL                     1
#             690 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             700 LOAD_ATTR               14 (_saferepr)
#             720 LOAD_FAST                3 (@py_assert4)
#             722 CALL                     1
#             730 LOAD_CONST               7 (('py0', 'py2', 'py5'))
#             732 BUILD_CONST_KEY_MAP      3
#             734 BINARY_OP                6 (%)
#             738 STORE_FAST               5 (@py_format6)
#             740 LOAD_CONST               8 ('assert %(py7)s')
#             742 LOAD_CONST               9 ('py7')
#             744 LOAD_FAST                5 (@py_format6)
#             746 BUILD_MAP                1
#             748 BINARY_OP                6 (%)
#             752 STORE_FAST               6 (@py_format8)
#             754 LOAD_GLOBAL             17 (NULL + AssertionError)
#             764 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             774 LOAD_ATTR               18 (_format_explanation)
#             794 LOAD_FAST                6 (@py_format8)
#             796 CALL                     1
#             804 CALL                     1
#             812 RAISE_VARARGS            1
#         >>  814 LOAD_CONST               0 (None)
#             816 COPY                     1
#             818 STORE_FAST               2 (@py_assert1)
#             820 COPY                     1
#             822 STORE_FAST               4 (@py_assert3)
#             824 STORE_FAST               3 (@py_assert4)
#             826 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_create_skill_factory at 0x3afa2710, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 72>:
#  72           0 RESUME                   0
# 
#  73           2 LOAD_GLOBAL              1 (NULL + create_skill)
#              12 LOAD_CONST               1 ('mock')
#              14 KW_NAMES                 2 (('engine',))
#              16 CALL                     1
#              24 STORE_FAST               1 (skill)
# 
#  74          26 LOAD_GLOBAL              3 (NULL + isinstance)
#              36 LOAD_FAST                1 (skill)
#              38 LOAD_GLOBAL              4 (PowerFlowPreset)
#              48 CALL                     2
#              56 STORE_FAST               2 (@py_assert3)
#              58 LOAD_FAST                2 (@py_assert3)
#              60 EXTENDED_ARG             1
#              62 POP_JUMP_IF_TRUE       267 (to 598)
#              64 LOAD_CONST               3 ('assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}')
#              66 LOAD_CONST               4 ('isinstance')
#              68 LOAD_GLOBAL              7 (NULL + @py_builtins)
#              78 LOAD_ATTR                8 (locals)
#              98 CALL                     0
#             106 CONTAINS_OP              0
#             108 POP_JUMP_IF_TRUE        25 (to 160)
#             110 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             120 LOAD_ATTR               12 (_should_repr_global_name)
#             140 LOAD_GLOBAL              2 (isinstance)
#             150 CALL                     1
#             158 POP_JUMP_IF_FALSE       25 (to 210)
#         >>  160 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             170 LOAD_ATTR               14 (_saferepr)
#             190 LOAD_GLOBAL              2 (isinstance)
#             200 CALL                     1
#             208 JUMP_FORWARD             1 (to 212)
#         >>  210 LOAD_CONST               4 ('isinstance')
#         >>  212 LOAD_CONST               5 ('skill')
#             214 LOAD_GLOBAL              7 (NULL + @py_builtins)
#             224 LOAD_ATTR                8 (locals)
#             244 CALL                     0
#             252 CONTAINS_OP              0
#             254 POP_JUMP_IF_TRUE        21 (to 298)
#             256 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             266 LOAD_ATTR               12 (_should_repr_global_name)
#             286 LOAD_FAST                1 (skill)
#             288 CALL                     1
#             296 POP_JUMP_IF_FALSE       21 (to 340)
#         >>  298 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             308 LOAD_ATTR               14 (_saferepr)
#             328 LOAD_FAST                1 (skill)
#             330 CALL                     1
#             338 JUMP_FORWARD             1 (to 342)
#         >>  340 LOAD_CONST               5 ('skill')
#         >>  342 LOAD_CONST               6 ('PowerFlowPreset')
#             344 LOAD_GLOBAL              7 (NULL + @py_builtins)
#             354 LOAD_ATTR                8 (locals)
#             374 CALL                     0
#             382 CONTAINS_OP              0
#             384 POP_JUMP_IF_TRUE        25 (to 436)
#             386 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             396 LOAD_ATTR               12 (_should_repr_global_name)
#             416 LOAD_GLOBAL              4 (PowerFlowPreset)
#             426 CALL                     1
#             434 POP_JUMP_IF_FALSE       25 (to 486)
#         >>  436 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             446 LOAD_ATTR               14 (_saferepr)
#             466 LOAD_GLOBAL              4 (PowerFlowPreset)
#             476 CALL                     1
#             484 JUMP_FORWARD             1 (to 488)
#         >>  486 LOAD_CONST               6 ('PowerFlowPreset')
#         >>  488 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             498 LOAD_ATTR               14 (_saferepr)
#             518 LOAD_FAST                2 (@py_assert3)
#             520 CALL                     1
#             528 LOAD_CONST               7 (('py0', 'py1', 'py2', 'py4'))
#             530 BUILD_CONST_KEY_MAP      4
#             532 BINARY_OP                6 (%)
#             536 STORE_FAST               3 (@py_format5)
#             538 LOAD_GLOBAL             17 (NULL + AssertionError)
#             548 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             558 LOAD_ATTR               18 (_format_explanation)
#             578 LOAD_FAST                3 (@py_format5)
#             580 CALL                     1
#             588 CALL                     1
#             596 RAISE_VARARGS            1
#         >>  598 LOAD_CONST               0 (None)
#             600 STORE_FAST               2 (@py_assert3)
#             602 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_default_config at 0x3afa5a90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 76>:
#  76           0 RESUME                   0
# 
#  77           2 LOAD_GLOBAL              1 (NULL + PowerFlowPreset)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  78          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
#  79          54 LOAD_FAST                2 (config)
#              56 LOAD_CONST               1 ('skill')
#              58 BINARY_SUBSCR
#              62 STORE_FAST               3 (@py_assert0)
#              64 LOAD_CONST               2 ('power_flow')
#              66 STORE_FAST               4 (@py_assert3)
#              68 LOAD_FAST                3 (@py_assert0)
#              70 LOAD_FAST                4 (@py_assert3)
#              72 COMPARE_OP              40 (==)
#              76 STORE_FAST               5 (@py_assert2)
#              78 LOAD_FAST                5 (@py_assert2)
#              80 POP_JUMP_IF_TRUE       108 (to 298)
#              82 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              92 LOAD_ATTR                6 (_call_reprcompare)
#             112 LOAD_CONST               3 (('==',))
#             114 LOAD_FAST                5 (@py_assert2)
#             116 BUILD_TUPLE              1
#             118 LOAD_CONST               4 (('%(py1)s == %(py4)s',))
#             120 LOAD_FAST                3 (@py_assert0)
#             122 LOAD_FAST                4 (@py_assert3)
#             124 BUILD_TUPLE              2
#             126 CALL                     4
#             134 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             144 LOAD_ATTR                8 (_saferepr)
#             164 LOAD_FAST                3 (@py_assert0)
#             166 CALL                     1
#             174 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             184 LOAD_ATTR                8 (_saferepr)
#             204 LOAD_FAST                4 (@py_assert3)
#             206 CALL                     1
#             214 LOAD_CONST               5 (('py1', 'py4'))
#             216 BUILD_CONST_KEY_MAP      2
#             218 BINARY_OP                6 (%)
#             222 STORE_FAST               6 (@py_format5)
#             224 LOAD_CONST               6 ('assert %(py6)s')
#             226 LOAD_CONST               7 ('py6')
#             228 LOAD_FAST                6 (@py_format5)
#             230 BUILD_MAP                1
#             232 BINARY_OP                6 (%)
#             236 STORE_FAST               7 (@py_format7)
#             238 LOAD_GLOBAL             11 (NULL + AssertionError)
#             248 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             258 LOAD_ATTR               12 (_format_explanation)
#             278 LOAD_FAST                7 (@py_format7)
#             280 CALL                     1
#             288 CALL                     1
#             296 RAISE_VARARGS            1
#         >>  298 LOAD_CONST               0 (None)
#             300 COPY                     1
#             302 STORE_FAST               3 (@py_assert0)
#             304 COPY                     1
#             306 STORE_FAST               5 (@py_assert2)
#             308 STORE_FAST               4 (@py_assert3)
# 
#  80         310 LOAD_FAST                2 (config)
#             312 LOAD_CONST               8 ('engine')
#             314 BINARY_SUBSCR
#             318 STORE_FAST               3 (@py_assert0)
#             320 LOAD_CONST               9 ('cloudpss')
#             322 STORE_FAST               4 (@py_assert3)
#             324 LOAD_FAST                3 (@py_assert0)
#             326 LOAD_FAST                4 (@py_assert3)
#             328 COMPARE_OP              40 (==)
#             332 STORE_FAST               5 (@py_assert2)
#             334 LOAD_FAST                5 (@py_assert2)
#             336 POP_JUMP_IF_TRUE       108 (to 554)
#             338 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             348 LOAD_ATTR                6 (_call_reprcompare)
#             368 LOAD_CONST               3 (('==',))
#             370 LOAD_FAST                5 (@py_assert2)
#             372 BUILD_TUPLE              1
#             374 LOAD_CONST               4 (('%(py1)s == %(py4)s',))
#             376 LOAD_FAST                3 (@py_assert0)
#             378 LOAD_FAST                4 (@py_assert3)
#             380 BUILD_TUPLE              2
#             382 CALL                     4
#             390 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             400 LOAD_ATTR                8 (_saferepr)
#             420 LOAD_FAST                3 (@py_assert0)
#             422 CALL                     1
#             430 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             440 LOAD_ATTR                8 (_saferepr)
#             460 LOAD_FAST                4 (@py_assert3)
#             462 CALL                     1
#             470 LOAD_CONST               5 (('py1', 'py4'))
#             472 BUILD_CONST_KEY_MAP      2
#             474 BINARY_OP                6 (%)
#             478 STORE_FAST               6 (@py_format5)
#             480 LOAD_CONST               6 ('assert %(py6)s')
#             482 LOAD_CONST               7 ('py6')
#             484 LOAD_FAST                6 (@py_format5)
#             486 BUILD_MAP                1
#             488 BINARY_OP                6 (%)
#             492 STORE_FAST               7 (@py_format7)
#             494 LOAD_GLOBAL             11 (NULL + AssertionError)
#             504 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             514 LOAD_ATTR               12 (_format_explanation)
#             534 LOAD_FAST                7 (@py_format7)
#             536 CALL                     1
#             544 CALL                     1
#             552 RAISE_VARARGS            1
#         >>  554 LOAD_CONST               0 (None)
#             556 COPY                     1
#             558 STORE_FAST               3 (@py_assert0)
#             560 COPY                     1
#             562 STORE_FAST               5 (@py_assert2)
#             564 STORE_FAST               4 (@py_assert3)
# 
#  81         566 LOAD_CONST              10 ('model')
#             568 STORE_FAST               3 (@py_assert0)
#             570 LOAD_FAST                3 (@py_assert0)
#             572 LOAD_FAST                2 (config)
#             574 CONTAINS_OP              0
#             576 STORE_FAST               5 (@py_assert2)
#             578 LOAD_FAST                5 (@py_assert2)
#             580 POP_JUMP_IF_TRUE       153 (to 888)
#             582 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             592 LOAD_ATTR                6 (_call_reprcompare)
#             612 LOAD_CONST              11 (('in',))
#             614 LOAD_FAST                5 (@py_assert2)
#             616 BUILD_TUPLE              1
#             618 LOAD_CONST              12 (('%(py1)s in %(py3)s',))
#             620 LOAD_FAST                3 (@py_assert0)
#             622 LOAD_FAST                2 (config)
#             624 BUILD_TUPLE              2
#             626 CALL                     4
#             634 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             644 LOAD_ATTR                8 (_saferepr)
#             664 LOAD_FAST                3 (@py_assert0)
#             666 CALL                     1
#             674 LOAD_CONST              13 ('config')
#             676 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             686 LOAD_ATTR               16 (locals)
#             706 CALL                     0
#             714 CONTAINS_OP              0
#             716 POP_JUMP_IF_TRUE        21 (to 760)
#             718 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             728 LOAD_ATTR               18 (_should_repr_global_name)
#             748 LOAD_FAST                2 (config)
#             750 CALL                     1
#             758 POP_JUMP_IF_FALSE       21 (to 802)
#         >>  760 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             770 LOAD_ATTR                8 (_saferepr)
#             790 LOAD_FAST                2 (config)
#             792 CALL                     1
#             800 JUMP_FORWARD             1 (to 804)
#         >>  802 LOAD_CONST              13 ('config')
#         >>  804 LOAD_CONST              14 (('py1', 'py3'))
#             806 BUILD_CONST_KEY_MAP      2
#             808 BINARY_OP                6 (%)
#             812 STORE_FAST               8 (@py_format4)
#             814 LOAD_CONST              15 ('assert %(py5)s')
#             816 LOAD_CONST              16 ('py5')
#             818 LOAD_FAST                8 (@py_format4)
#             820 BUILD_MAP                1
#             822 BINARY_OP                6 (%)
#             826 STORE_FAST               9 (@py_format6)
#             828 LOAD_GLOBAL             11 (NULL + AssertionError)
#             838 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             848 LOAD_ATTR               12 (_format_explanation)
#             868 LOAD_FAST                9 (@py_format6)
#             870 CALL                     1
#             878 CALL                     1
#             886 RAISE_VARARGS            1
#         >>  888 LOAD_CONST               0 (None)
#             890 COPY                     1
#             892 STORE_FAST               3 (@py_assert0)
#             894 STORE_FAST               5 (@py_assert2)
# 
#  82         896 LOAD_CONST              17 ('algorithm')
#             898 STORE_FAST               3 (@py_assert0)
#             900 LOAD_FAST                3 (@py_assert0)
#             902 LOAD_FAST                2 (config)
#             904 CONTAINS_OP              0
#             906 STORE_FAST               5 (@py_assert2)
#             908 LOAD_FAST                5 (@py_assert2)
#             910 POP_JUMP_IF_TRUE       153 (to 1218)
#             912 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             922 LOAD_ATTR                6 (_call_reprcompare)
#             942 LOAD_CONST              11 (('in',))
#             944 LOAD_FAST                5 (@py_assert2)
#             946 BUILD_TUPLE              1
#             948 LOAD_CONST              12 (('%(py1)s in %(py3)s',))
#             950 LOAD_FAST                3 (@py_assert0)
#             952 LOAD_FAST                2 (config)
#             954 BUILD_TUPLE              2
#             956 CALL                     4
#             964 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             974 LOAD_ATTR                8 (_saferepr)
#             994 LOAD_FAST                3 (@py_assert0)
#             996 CALL                     1
#            1004 LOAD_CONST              13 ('config')
#            1006 LOAD_GLOBAL             15 (NULL + @py_builtins)
#            1016 LOAD_ATTR               16 (locals)
#            1036 CALL                     0
#            1044 CONTAINS_OP              0
#            1046 POP_JUMP_IF_TRUE        21 (to 1090)
#            1048 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1058 LOAD_ATTR               18 (_should_repr_global_name)
#            1078 LOAD_FAST                2 (config)
#            1080 CALL                     1
#            1088 POP_JUMP_IF_FALSE       21 (to 1132)
#         >> 1090 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1100 LOAD_ATTR                8 (_saferepr)
#            1120 LOAD_FAST                2 (config)
#            1122 CALL                     1
#            1130 JUMP_FORWARD             1 (to 1134)
#         >> 1132 LOAD_CONST              13 ('config')
#         >> 1134 LOAD_CONST              14 (('py1', 'py3'))
#            1136 BUILD_CONST_KEY_MAP      2
#            1138 BINARY_OP                6 (%)
#            1142 STORE_FAST               8 (@py_format4)
#            1144 LOAD_CONST              15 ('assert %(py5)s')
#            1146 LOAD_CONST              16 ('py5')
#            1148 LOAD_FAST                8 (@py_format4)
#            1150 BUILD_MAP                1
#            1152 BINARY_OP                6 (%)
#            1156 STORE_FAST               9 (@py_format6)
#            1158 LOAD_GLOBAL             11 (NULL + AssertionError)
#            1168 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1178 LOAD_ATTR               12 (_format_explanation)
#            1198 LOAD_FAST                9 (@py_format6)
#            1200 CALL                     1
#            1208 CALL                     1
#            1216 RAISE_VARARGS            1
#         >> 1218 LOAD_CONST               0 (None)
#            1220 COPY                     1
#            1222 STORE_FAST               3 (@py_assert0)
#            1224 STORE_FAST               5 (@py_assert2)
#            1226 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_config_schema at 0x3afa0150, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 84>:
#  84           0 RESUME                   0
# 
#  85           2 LOAD_GLOBAL              1 (NULL + PowerFlowPreset)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  86          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                2 (config_schema)
#              44 STORE_FAST               2 (schema)
# 
#  87          46 LOAD_FAST                2 (schema)
#              48 LOAD_CONST               1 ('type')
#              50 BINARY_SUBSCR
#              54 STORE_FAST               3 (@py_assert0)
#              56 LOAD_CONST               2 ('object')
#              58 STORE_FAST               4 (@py_assert3)
#              60 LOAD_FAST                3 (@py_assert0)
#              62 LOAD_FAST                4 (@py_assert3)
#              64 COMPARE_OP              40 (==)
#              68 STORE_FAST               5 (@py_assert2)
#              70 LOAD_FAST                5 (@py_assert2)
#              72 POP_JUMP_IF_TRUE       108 (to 290)
#              74 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              84 LOAD_ATTR                6 (_call_reprcompare)
#             104 LOAD_CONST               3 (('==',))
#             106 LOAD_FAST                5 (@py_assert2)
#             108 BUILD_TUPLE              1
#             110 LOAD_CONST               4 (('%(py1)s == %(py4)s',))
#             112 LOAD_FAST                3 (@py_assert0)
#             114 LOAD_FAST                4 (@py_assert3)
#             116 BUILD_TUPLE              2
#             118 CALL                     4
#             126 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             136 LOAD_ATTR                8 (_saferepr)
#             156 LOAD_FAST                3 (@py_assert0)
#             158 CALL                     1
#             166 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             176 LOAD_ATTR                8 (_saferepr)
#             196 LOAD_FAST                4 (@py_assert3)
#             198 CALL                     1
#             206 LOAD_CONST               5 (('py1', 'py4'))
#             208 BUILD_CONST_KEY_MAP      2
#             210 BINARY_OP                6 (%)
#             214 STORE_FAST               6 (@py_format5)
#             216 LOAD_CONST               6 ('assert %(py6)s')
#             218 LOAD_CONST               7 ('py6')
#             220 LOAD_FAST                6 (@py_format5)
#             222 BUILD_MAP                1
#             224 BINARY_OP                6 (%)
#             228 STORE_FAST               7 (@py_format7)
#             230 LOAD_GLOBAL             11 (NULL + AssertionError)
#             240 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             250 LOAD_ATTR               12 (_format_explanation)
#             270 LOAD_FAST                7 (@py_format7)
#             272 CALL                     1
#             280 CALL                     1
#             288 RAISE_VARARGS            1
#         >>  290 LOAD_CONST               0 (None)
#             292 COPY                     1
#             294 STORE_FAST               3 (@py_assert0)
#             296 COPY                     1
#             298 STORE_FAST               5 (@py_assert2)
#             300 STORE_FAST               4 (@py_assert3)
# 
#  88         302 LOAD_CONST               8 ('skill')
#             304 STORE_FAST               3 (@py_assert0)
#             306 LOAD_FAST                2 (schema)
#             308 LOAD_CONST               9 ('required')
#             310 BINARY_SUBSCR
#             314 STORE_FAST               4 (@py_assert3)
#             316 LOAD_FAST                3 (@py_assert0)
#             318 LOAD_FAST                4 (@py_assert3)
#             320 CONTAINS_OP              0
#             322 STORE_FAST               5 (@py_assert2)
#             324 LOAD_FAST                5 (@py_assert2)
#             326 POP_JUMP_IF_TRUE       108 (to 544)
#             328 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             338 LOAD_ATTR                6 (_call_reprcompare)
#             358 LOAD_CONST              10 (('in',))
#             360 LOAD_FAST                5 (@py_assert2)
#             362 BUILD_TUPLE              1
#             364 LOAD_CONST              11 (('%(py1)s in %(py4)s',))
#             366 LOAD_FAST                3 (@py_assert0)
#             368 LOAD_FAST                4 (@py_assert3)
#             370 BUILD_TUPLE              2
#             372 CALL                     4
#             380 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             390 LOAD_ATTR                8 (_saferepr)
#             410 LOAD_FAST                3 (@py_assert0)
#             412 CALL                     1
#             420 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             430 LOAD_ATTR                8 (_saferepr)
#             450 LOAD_FAST                4 (@py_assert3)
#             452 CALL                     1
#             460 LOAD_CONST               5 (('py1', 'py4'))
#             462 BUILD_CONST_KEY_MAP      2
#             464 BINARY_OP                6 (%)
#             468 STORE_FAST               6 (@py_format5)
#             470 LOAD_CONST               6 ('assert %(py6)s')
#             472 LOAD_CONST               7 ('py6')
#             474 LOAD_FAST                6 (@py_format5)
#             476 BUILD_MAP                1
#             478 BINARY_OP                6 (%)
#             482 STORE_FAST               7 (@py_format7)
#             484 LOAD_GLOBAL             11 (NULL + AssertionError)
#             494 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             504 LOAD_ATTR               12 (_format_explanation)
#             524 LOAD_FAST                7 (@py_format7)
#             526 CALL                     1
#             534 CALL                     1
#             542 RAISE_VARARGS            1
#         >>  544 LOAD_CONST               0 (None)
#             546 COPY                     1
#             548 STORE_FAST               3 (@py_assert0)
#             550 COPY                     1
#             552 STORE_FAST               5 (@py_assert2)
#             554 STORE_FAST               4 (@py_assert3)
# 
#  89         556 LOAD_CONST              12 ('model')
#             558 STORE_FAST               3 (@py_assert0)
#             560 LOAD_FAST                2 (schema)
#             562 LOAD_CONST               9 ('required')
#             564 BINARY_SUBSCR
#             568 STORE_FAST               4 (@py_assert3)
#             570 LOAD_FAST                3 (@py_assert0)
#             572 LOAD_FAST                4 (@py_assert3)
#             574 CONTAINS_OP              0
#             576 STORE_FAST               5 (@py_assert2)
#             578 LOAD_FAST                5 (@py_assert2)
#             580 POP_JUMP_IF_TRUE       108 (to 798)
#             582 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             592 LOAD_ATTR                6 (_call_reprcompare)
#             612 LOAD_CONST              10 (('in',))
#             614 LOAD_FAST                5 (@py_assert2)
#             616 BUILD_TUPLE              1
#             618 LOAD_CONST              11 (('%(py1)s in %(py4)s',))
#             620 LOAD_FAST                3 (@py_assert0)
#             622 LOAD_FAST                4 (@py_assert3)
#             624 BUILD_TUPLE              2
#             626 CALL                     4
#             634 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             644 LOAD_ATTR                8 (_saferepr)
#             664 LOAD_FAST                3 (@py_assert0)
#             666 CALL                     1
#             674 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             684 LOAD_ATTR                8 (_saferepr)
#             704 LOAD_FAST                4 (@py_assert3)
#             706 CALL                     1
#             714 LOAD_CONST               5 (('py1', 'py4'))
#             716 BUILD_CONST_KEY_MAP      2
#             718 BINARY_OP                6 (%)
#             722 STORE_FAST               6 (@py_format5)
#             724 LOAD_CONST               6 ('assert %(py6)s')
#             726 LOAD_CONST               7 ('py6')
#             728 LOAD_FAST                6 (@py_format5)
#             730 BUILD_MAP                1
#             732 BINARY_OP                6 (%)
#             736 STORE_FAST               7 (@py_format7)
#             738 LOAD_GLOBAL             11 (NULL + AssertionError)
#             748 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             758 LOAD_ATTR               12 (_format_explanation)
#             778 LOAD_FAST                7 (@py_format7)
#             780 CALL                     1
#             788 CALL                     1
#             796 RAISE_VARARGS            1
#         >>  798 LOAD_CONST               0 (None)
#             800 COPY                     1
#             802 STORE_FAST               3 (@py_assert0)
#             804 COPY                     1
#             806 STORE_FAST               5 (@py_assert2)
#             808 STORE_FAST               4 (@py_assert3)
#             810 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_valid_config at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 91>:
#  91           0 RESUME                   0
# 
#  92           2 LOAD_GLOBAL              1 (NULL + PowerFlowPreset)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  93          22 LOAD_CONST               1 ('model')
#              24 LOAD_CONST               2 ('rid')
#              26 LOAD_CONST               3 ('model/test/123')
#              28 BUILD_MAP                1
#              30 BUILD_MAP                1
#              32 STORE_FAST               2 (config)
# 
#  94          34 LOAD_FAST                1 (skill)
#              36 LOAD_ATTR                3 (NULL|self + validate)
#              56 LOAD_FAST                2 (config)
#              58 CALL                     1
#              66 UNPACK_SEQUENCE          2
#              70 STORE_FAST               3 (valid)
#              72 STORE_FAST               4 (errors)
# 
#  95          74 LOAD_CONST               4 (True)
#              76 STORE_FAST               5 (@py_assert2)
#              78 LOAD_FAST                3 (valid)
#              80 LOAD_FAST                5 (@py_assert2)
#              82 IS_OP                    0
#              84 STORE_FAST               6 (@py_assert1)
#              86 LOAD_FAST                6 (@py_assert1)
#              88 POP_JUMP_IF_TRUE       153 (to 396)
#              90 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             100 LOAD_ATTR                6 (_call_reprcompare)
#             120 LOAD_CONST               5 (('is',))
#             122 LOAD_FAST                6 (@py_assert1)
#             124 BUILD_TUPLE              1
#             126 LOAD_CONST               6 (('%(py0)s is %(py3)s',))
#             128 LOAD_FAST                3 (valid)
#             130 LOAD_FAST                5 (@py_assert2)
#             132 BUILD_TUPLE              2
#             134 CALL                     4
#             142 LOAD_CONST               7 ('valid')
#             144 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             154 LOAD_ATTR               10 (locals)
#             174 CALL                     0
#             182 CONTAINS_OP              0
#             184 POP_JUMP_IF_TRUE        21 (to 228)
#             186 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             196 LOAD_ATTR               12 (_should_repr_global_name)
#             216 LOAD_FAST                3 (valid)
#             218 CALL                     1
#             226 POP_JUMP_IF_FALSE       21 (to 270)
#         >>  228 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             238 LOAD_ATTR               14 (_saferepr)
#             258 LOAD_FAST                3 (valid)
#             260 CALL                     1
#             268 JUMP_FORWARD             1 (to 272)
#         >>  270 LOAD_CONST               7 ('valid')
#         >>  272 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             282 LOAD_ATTR               14 (_saferepr)
#             302 LOAD_FAST                5 (@py_assert2)
#             304 CALL                     1
#             312 LOAD_CONST               8 (('py0', 'py3'))
#             314 BUILD_CONST_KEY_MAP      2
#             316 BINARY_OP                6 (%)
#             320 STORE_FAST               7 (@py_format4)
#             322 LOAD_CONST               9 ('assert %(py5)s')
#             324 LOAD_CONST              10 ('py5')
#             326 LOAD_FAST                7 (@py_format4)
#             328 BUILD_MAP                1
#             330 BINARY_OP                6 (%)
#             334 STORE_FAST               8 (@py_format6)
#             336 LOAD_GLOBAL             17 (NULL + AssertionError)
#             346 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             356 LOAD_ATTR               18 (_format_explanation)
#             376 LOAD_FAST                8 (@py_format6)
#             378 CALL                     1
#             386 CALL                     1
#             394 RAISE_VARARGS            1
#         >>  396 LOAD_CONST               0 (None)
#             398 COPY                     1
#             400 STORE_FAST               6 (@py_assert1)
#             402 STORE_FAST               5 (@py_assert2)
#             404 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_missing_model at 0x3afa6030, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 97>:
#  97           0 RESUME                   0
# 
#  98           2 LOAD_GLOBAL              1 (NULL + PowerFlowPreset)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  99          22 BUILD_MAP                0
#              24 STORE_FAST               2 (config)
# 
# 100          26 LOAD_FAST                1 (skill)
#              28 LOAD_ATTR                3 (NULL|self + validate)
#              48 LOAD_FAST                2 (config)
#              50 CALL                     1
#              58 UNPACK_SEQUENCE          2
#              62 STORE_FAST               3 (valid)
#              64 STORE_FAST               4 (errors)
# 
# 101          66 LOAD_CONST               1 (False)
#              68 STORE_FAST               5 (@py_assert2)
#              70 LOAD_FAST                3 (valid)
#              72 LOAD_FAST                5 (@py_assert2)
#              74 IS_OP                    0
#              76 STORE_FAST               6 (@py_assert1)
#              78 LOAD_FAST                6 (@py_assert1)
#              80 POP_JUMP_IF_TRUE       153 (to 388)
#              82 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              92 LOAD_ATTR                6 (_call_reprcompare)
#             112 LOAD_CONST               2 (('is',))
#             114 LOAD_FAST                6 (@py_assert1)
#             116 BUILD_TUPLE              1
#             118 LOAD_CONST               3 (('%(py0)s is %(py3)s',))
#             120 LOAD_FAST                3 (valid)
#             122 LOAD_FAST                5 (@py_assert2)
#             124 BUILD_TUPLE              2
#             126 CALL                     4
#             134 LOAD_CONST               4 ('valid')
#             136 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             146 LOAD_ATTR               10 (locals)
#             166 CALL                     0
#             174 CONTAINS_OP              0
#             176 POP_JUMP_IF_TRUE        21 (to 220)
#             178 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             188 LOAD_ATTR               12 (_should_repr_global_name)
#             208 LOAD_FAST                3 (valid)
#             210 CALL                     1
#             218 POP_JUMP_IF_FALSE       21 (to 262)
#         >>  220 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             230 LOAD_ATTR               14 (_saferepr)
#             250 LOAD_FAST                3 (valid)
#             252 CALL                     1
#             260 JUMP_FORWARD             1 (to 264)
#         >>  262 LOAD_CONST               4 ('valid')
#         >>  264 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             274 LOAD_ATTR               14 (_saferepr)
#             294 LOAD_FAST                5 (@py_assert2)
#             296 CALL                     1
#             304 LOAD_CONST               5 (('py0', 'py3'))
#             306 BUILD_CONST_KEY_MAP      2
#             308 BINARY_OP                6 (%)
#             312 STORE_FAST               7 (@py_format4)
#             314 LOAD_CONST               6 ('assert %(py5)s')
#             316 LOAD_CONST               7 ('py5')
#             318 LOAD_FAST                7 (@py_format4)
#             320 BUILD_MAP                1
#             322 BINARY_OP                6 (%)
#             326 STORE_FAST               8 (@py_format6)
#             328 LOAD_GLOBAL             17 (NULL + AssertionError)
#             338 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             348 LOAD_ATTR               18 (_format_explanation)
#             368 LOAD_FAST                8 (@py_format6)
#             370 CALL                     1
#             378 CALL                     1
#             386 RAISE_VARARGS            1
#         >>  388 LOAD_CONST               0 (None)
#             390 COPY                     1
#             392 STORE_FAST               6 (@py_assert1)
#             394 STORE_FAST               5 (@py_assert2)
# 
# 102         396 LOAD_GLOBAL             21 (NULL + len)
#             406 LOAD_FAST                4 (errors)
#             408 CALL                     1
#             416 STORE_FAST               5 (@py_assert2)
#             418 LOAD_CONST               8 (0)
#             420 STORE_FAST               9 (@py_assert5)
#             422 LOAD_FAST                5 (@py_assert2)
#             424 LOAD_FAST                9 (@py_assert5)
#             426 COMPARE_OP              68 (>)
#             430 STORE_FAST              10 (@py_assert4)
#             432 LOAD_FAST               10 (@py_assert4)
#             434 POP_JUMP_IF_TRUE       246 (to 928)
#             436 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             446 LOAD_ATTR                6 (_call_reprcompare)
#             466 LOAD_CONST               9 (('>',))
#             468 LOAD_FAST               10 (@py_assert4)
#             470 BUILD_TUPLE              1
#             472 LOAD_CONST              10 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} > %(py6)s',))
#             474 LOAD_FAST                5 (@py_assert2)
#             476 LOAD_FAST                9 (@py_assert5)
#             478 BUILD_TUPLE              2
#             480 CALL                     4
#             488 LOAD_CONST              11 ('len')
#             490 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             500 LOAD_ATTR               10 (locals)
#             520 CALL                     0
#             528 CONTAINS_OP              0
#             530 POP_JUMP_IF_TRUE        25 (to 582)
#             532 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             542 LOAD_ATTR               12 (_should_repr_global_name)
#             562 LOAD_GLOBAL             20 (len)
#             572 CALL                     1
#             580 POP_JUMP_IF_FALSE       25 (to 632)
#         >>  582 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             592 LOAD_ATTR               14 (_saferepr)
#             612 LOAD_GLOBAL             20 (len)
#             622 CALL                     1
#             630 JUMP_FORWARD             1 (to 634)
#         >>  632 LOAD_CONST              11 ('len')
#         >>  634 LOAD_CONST              12 ('errors')
#             636 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             646 LOAD_ATTR               10 (locals)
#             666 CALL                     0
#             674 CONTAINS_OP              0
#             676 POP_JUMP_IF_TRUE        21 (to 720)
#             678 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             688 LOAD_ATTR               12 (_should_repr_global_name)
#             708 LOAD_FAST                4 (errors)
#             710 CALL                     1
#             718 POP_JUMP_IF_FALSE       21 (to 762)
#         >>  720 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             730 LOAD_ATTR               14 (_saferepr)
#             750 LOAD_FAST                4 (errors)
#             752 CALL                     1
#             760 JUMP_FORWARD             1 (to 764)
#         >>  762 LOAD_CONST              12 ('errors')
#         >>  764 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             774 LOAD_ATTR               14 (_saferepr)
#             794 LOAD_FAST                5 (@py_assert2)
#             796 CALL                     1
#             804 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             814 LOAD_ATTR               14 (_saferepr)
#             834 LOAD_FAST                9 (@py_assert5)
#             836 CALL                     1
#             844 LOAD_CONST              13 (('py0', 'py1', 'py3', 'py6'))
#             846 BUILD_CONST_KEY_MAP      4
#             848 BINARY_OP                6 (%)
#             852 STORE_FAST              11 (@py_format7)
#             854 LOAD_CONST              14 ('assert %(py8)s')
#             856 LOAD_CONST              15 ('py8')
#             858 LOAD_FAST               11 (@py_format7)
#             860 BUILD_MAP                1
#             862 BINARY_OP                6 (%)
#             866 STORE_FAST              12 (@py_format9)
#             868 LOAD_GLOBAL             17 (NULL + AssertionError)
#             878 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             888 LOAD_ATTR               18 (_format_explanation)
#             908 LOAD_FAST               12 (@py_format9)
#             910 CALL                     1
#             918 CALL                     1
#             926 RAISE_VARARGS            1
#         >>  928 LOAD_CONST               0 (None)
#             930 COPY                     1
#             932 STORE_FAST               5 (@py_assert2)
#             934 COPY                     1
#             936 STORE_FAST              10 (@py_assert4)
#             938 STORE_FAST               9 (@py_assert5)
#             940 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_missing_rid at 0x3af90d20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 104>:
# 104           0 RESUME                   0
# 
# 105           2 LOAD_GLOBAL              1 (NULL + PowerFlowPreset)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 106          22 LOAD_CONST               1 ('model')
#              24 BUILD_MAP                0
#              26 BUILD_MAP                1
#              28 STORE_FAST               2 (config)
# 
# 107          30 LOAD_FAST                1 (skill)
#              32 LOAD_ATTR                3 (NULL|self + validate)
#              52 LOAD_FAST                2 (config)
#              54 CALL                     1
#              62 UNPACK_SEQUENCE          2
#              66 STORE_FAST               3 (valid)
#              68 STORE_FAST               4 (errors)
# 
# 108          70 LOAD_CONST               2 (False)
#              72 STORE_FAST               5 (@py_assert2)
#              74 LOAD_FAST                3 (valid)
#              76 LOAD_FAST                5 (@py_assert2)
#              78 IS_OP                    0
#              80 STORE_FAST               6 (@py_assert1)
#              82 LOAD_FAST                6 (@py_assert1)
#              84 POP_JUMP_IF_TRUE       153 (to 392)
#              86 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              96 LOAD_ATTR                6 (_call_reprcompare)
#             116 LOAD_CONST               3 (('is',))
#             118 LOAD_FAST                6 (@py_assert1)
#             120 BUILD_TUPLE              1
#             122 LOAD_CONST               4 (('%(py0)s is %(py3)s',))
#             124 LOAD_FAST                3 (valid)
#             126 LOAD_FAST                5 (@py_assert2)
#             128 BUILD_TUPLE              2
#             130 CALL                     4
#             138 LOAD_CONST               5 ('valid')
#             140 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             150 LOAD_ATTR               10 (locals)
#             170 CALL                     0
#             178 CONTAINS_OP              0
#             180 POP_JUMP_IF_TRUE        21 (to 224)
#             182 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             192 LOAD_ATTR               12 (_should_repr_global_name)
#             212 LOAD_FAST                3 (valid)
#             214 CALL                     1
#             222 POP_JUMP_IF_FALSE       21 (to 266)
#         >>  224 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             234 LOAD_ATTR               14 (_saferepr)
#             254 LOAD_FAST                3 (valid)
#             256 CALL                     1
#             264 JUMP_FORWARD             1 (to 268)
#         >>  266 LOAD_CONST               5 ('valid')
#         >>  268 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             278 LOAD_ATTR               14 (_saferepr)
#             298 LOAD_FAST                5 (@py_assert2)
#             300 CALL                     1
#             308 LOAD_CONST               6 (('py0', 'py3'))
#             310 BUILD_CONST_KEY_MAP      2
#             312 BINARY_OP                6 (%)
#             316 STORE_FAST               7 (@py_format4)
#             318 LOAD_CONST               7 ('assert %(py5)s')
#             320 LOAD_CONST               8 ('py5')
#             322 LOAD_FAST                7 (@py_format4)
#             324 BUILD_MAP                1
#             326 BINARY_OP                6 (%)
#             330 STORE_FAST               8 (@py_format6)
#             332 LOAD_GLOBAL             17 (NULL + AssertionError)
#             342 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             352 LOAD_ATTR               18 (_format_explanation)
#             372 LOAD_FAST                8 (@py_format6)
#             374 CALL                     1
#             382 CALL                     1
#             390 RAISE_VARARGS            1
#         >>  392 LOAD_CONST               0 (None)
#             394 COPY                     1
#             396 STORE_FAST               6 (@py_assert1)
#             398 STORE_FAST               5 (@py_assert2)
#             400 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_invalid_tolerance at 0x3af3fb70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 110>:
# 110           0 RESUME                   0
# 
# 111           2 LOAD_GLOBAL              1 (NULL + PowerFlowPreset)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 112          22 LOAD_CONST               1 ('rid')
#              24 LOAD_CONST               2 ('test')
#              26 BUILD_MAP                1
#              28 LOAD_CONST               3 ('tolerance')
#              30 LOAD_CONST               4 (-1)
#              32 BUILD_MAP                1
#              34 LOAD_CONST               5 (('model', 'algorithm'))
#              36 BUILD_CONST_KEY_MAP      2
#              38 STORE_FAST               2 (config)
# 
# 113          40 LOAD_FAST                1 (skill)
#              42 LOAD_ATTR                3 (NULL|self + validate)
#              62 LOAD_FAST                2 (config)
#              64 CALL                     1
#              72 UNPACK_SEQUENCE          2
#              76 STORE_FAST               3 (valid)
#              78 STORE_FAST               4 (errors)
# 
# 114          80 LOAD_CONST               6 (False)
#              82 STORE_FAST               5 (@py_assert2)
#              84 LOAD_FAST                3 (valid)
#              86 LOAD_FAST                5 (@py_assert2)
#              88 IS_OP                    0
#              90 STORE_FAST               6 (@py_assert1)
#              92 LOAD_FAST                6 (@py_assert1)
#              94 POP_JUMP_IF_TRUE       153 (to 402)
#              96 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             106 LOAD_ATTR                6 (_call_reprcompare)
#             126 LOAD_CONST               7 (('is',))
#             128 LOAD_FAST                6 (@py_assert1)
#             130 BUILD_TUPLE              1
#             132 LOAD_CONST               8 (('%(py0)s is %(py3)s',))
#             134 LOAD_FAST                3 (valid)
#             136 LOAD_FAST                5 (@py_assert2)
#             138 BUILD_TUPLE              2
#             140 CALL                     4
#             148 LOAD_CONST               9 ('valid')
#             150 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             160 LOAD_ATTR               10 (locals)
#             180 CALL                     0
#             188 CONTAINS_OP              0
#             190 POP_JUMP_IF_TRUE        21 (to 234)
#             192 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             202 LOAD_ATTR               12 (_should_repr_global_name)
#             222 LOAD_FAST                3 (valid)
#             224 CALL                     1
#             232 POP_JUMP_IF_FALSE       21 (to 276)
#         >>  234 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             244 LOAD_ATTR               14 (_saferepr)
#             264 LOAD_FAST                3 (valid)
#             266 CALL                     1
#             274 JUMP_FORWARD             1 (to 278)
#         >>  276 LOAD_CONST               9 ('valid')
#         >>  278 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             288 LOAD_ATTR               14 (_saferepr)
#             308 LOAD_FAST                5 (@py_assert2)
#             310 CALL                     1
#             318 LOAD_CONST              10 (('py0', 'py3'))
#             320 BUILD_CONST_KEY_MAP      2
#             322 BINARY_OP                6 (%)
#             326 STORE_FAST               7 (@py_format4)
#             328 LOAD_CONST              11 ('assert %(py5)s')
#             330 LOAD_CONST              12 ('py5')
#             332 LOAD_FAST                7 (@py_format4)
#             334 BUILD_MAP                1
#             336 BINARY_OP                6 (%)
#             340 STORE_FAST               8 (@py_format6)
#             342 LOAD_GLOBAL             17 (NULL + AssertionError)
#             352 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             362 LOAD_ATTR               18 (_format_explanation)
#             382 LOAD_FAST                8 (@py_format6)
#             384 CALL                     1
#             392 CALL                     1
#             400 RAISE_VARARGS            1
#         >>  402 LOAD_CONST               0 (None)
#             404 COPY                     1
#             406 STORE_FAST               6 (@py_assert1)
#             408 STORE_FAST               5 (@py_assert2)
#             410 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestPowerFlowPresetRun at 0x73cd93b44fa0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 117>:
# 117           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestPowerFlowPresetRun')
#               8 STORE_NAME               2 (__qualname__)
# 
# 118          10 LOAD_CONST               1 ('Tests for PowerFlowPreset.run() with mocked adapter.')
#              12 STORE_NAME               3 (__doc__)
# 
# 120          14 LOAD_NAME                4 (pytest)
#              16 LOAD_ATTR               10 (fixture)
# 
# 121          36 LOAD_CONST               2 (<code object skill_with_mock at 0x73cd945fe870, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 120>)
#              38 MAKE_FUNCTION            0
# 
# 120          40 CALL                     0
# 
# 121          48 STORE_NAME               6 (skill_with_mock)
# 
# 126          50 PUSH_NULL
#              52 LOAD_NAME                7 (patch)
#              54 LOAD_CONST               3 ('cloudpss_skills_v2.powerskill.presets.power_flow.Engine')
#              56 CALL                     1
# 
# 127          64 LOAD_CONST               4 (<code object test_run_success at 0x3af9df30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 126>)
#              66 MAKE_FUNCTION            0
# 
# 126          68 CALL                     0
# 
# 127          76 STORE_NAME               8 (test_run_success)
# 
# 154          78 PUSH_NULL
#              80 LOAD_NAME                7 (patch)
#              82 LOAD_CONST               3 ('cloudpss_skills_v2.powerskill.presets.power_flow.Engine')
#              84 CALL                     1
# 
# 155          92 LOAD_CONST               5 (<code object test_run_validation_failure at 0x3af9e5f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 154>)
#              94 MAKE_FUNCTION            0
# 
# 154          96 CALL                     0
# 
# 155         104 STORE_NAME               9 (test_run_validation_failure)
#             106 RETURN_CONST             6 (None)
# 
# Disassembly of <code object skill_with_mock at 0x73cd945fe870, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 120>:
# 120           0 RESUME                   0
# 
# 123           2 LOAD_GLOBAL              1 (NULL + PowerFlowPreset)
#              12 LOAD_CONST               1 ('mock')
#              14 KW_NAMES                 2 (('engine',))
#              16 CALL                     1
#              24 STORE_FAST               1 (skill)
# 
# 124          26 LOAD_FAST                1 (skill)
#              28 RETURN_VALUE
# 
# Disassembly of <code object test_run_success at 0x3af9df30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 126>:
# 126           0 RESUME                   0
# 
# 128           2 LOAD_GLOBAL              1 (NULL + MockPowerFlowAdapter)
#              12 CALL                     0
#              20 STORE_FAST               3 (mock_adapter)
# 
# 129          22 LOAD_GLOBAL              3 (NULL + Mock)
#              32 CALL                     0
#              40 STORE_FAST               4 (mock_api)
# 
# 130          42 LOAD_FAST                3 (mock_adapter)
#              44 LOAD_ATTR                5 (NULL|self + _do_run_simulation)
#              64 BUILD_MAP                0
#              66 CALL                     1
#              74 LOAD_FAST                4 (mock_api)
#              76 LOAD_ATTR                6 (run_power_flow)
#              96 STORE_ATTR               4 (return_value)
# 
# 132         106 LOAD_CONST               1 (1)
#             108 LOAD_CONST               2 (1.05)
#             110 LOAD_CONST               3 (('id', 'Vm'))
#             112 BUILD_CONST_KEY_MAP      2
# 
# 133         114 LOAD_CONST               4 (2)
#             116 LOAD_CONST               5 (1.02)
#             118 LOAD_CONST               3 (('id', 'Vm'))
#             120 BUILD_CONST_KEY_MAP      2
# 
# 131         122 BUILD_LIST               2
#             124 LOAD_FAST                4 (mock_api)
#             126 LOAD_ATTR               10 (get_bus_voltages)
#             146 STORE_ATTR               4 (return_value)
# 
# 135         156 LOAD_CONST               1 (1)
#             158 LOAD_CONST               4 (2)
#             160 LOAD_CONST               6 (2.5)
#             162 LOAD_CONST               7 (('from', 'to', 'Ploss'))
#             164 BUILD_CONST_KEY_MAP      3
#             166 BUILD_LIST               1
#             168 LOAD_FAST                4 (mock_api)
#             170 LOAD_ATTR               12 (get_branch_flows)
#             190 STORE_ATTR               4 (return_value)
# 
# 136         200 BUILD_MAP                0
#             202 LOAD_FAST                4 (mock_api)
#             204 LOAD_ATTR               14 (get_summary)
#             224 STORE_ATTR               4 (return_value)
# 
# 137         234 LOAD_CONST               8 (True)
#             236 LOAD_FAST                4 (mock_api)
#             238 STORE_ATTR               8 (is_connected)
# 
# 139         248 LOAD_FAST                4 (mock_api)
#             250 LOAD_FAST                1 (mock_factory)
#             252 LOAD_ATTR               18 (create_powerflow_api)
#             272 STORE_ATTR               4 (return_value)
# 
# 142         282 LOAD_CONST               9 ('rid')
#             284 LOAD_CONST              10 ('model/test/123')
#             286 BUILD_MAP                1
# 
# 143         288 LOAD_CONST              11 ('acpf')
#             290 LOAD_CONST              12 (1e-06)
#             292 LOAD_CONST              13 (('type', 'tolerance'))
#             294 BUILD_CONST_KEY_MAP      2
# 
# 141         296 LOAD_CONST              14 (('model', 'algorithm'))
#             298 BUILD_CONST_KEY_MAP      2
#             300 STORE_FAST               5 (config)
# 
# 146         302 LOAD_FAST                2 (skill_with_mock)
#             304 LOAD_ATTR               21 (NULL|self + run)
#             324 LOAD_FAST                5 (config)
#             326 CALL                     1
#             334 STORE_FAST               6 (result)
# 
# 148         336 LOAD_FAST                6 (result)
#             338 LOAD_ATTR               22 (is_success)
#             358 STORE_FAST               7 (@py_assert1)
#             360 LOAD_CONST               8 (True)
#             362 STORE_FAST               8 (@py_assert4)
#             364 LOAD_FAST                7 (@py_assert1)
#             366 LOAD_FAST                8 (@py_assert4)
#             368 IS_OP                    0
#             370 STORE_FAST               9 (@py_assert3)
#             372 LOAD_FAST                9 (@py_assert3)
#             374 POP_JUMP_IF_TRUE       173 (to 722)
#             376 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             386 LOAD_ATTR               26 (_call_reprcompare)
#             406 LOAD_CONST              15 (('is',))
#             408 LOAD_FAST                9 (@py_assert3)
#             410 BUILD_TUPLE              1
#             412 LOAD_CONST              16 (('%(py2)s\n{%(py2)s = %(py0)s.is_success\n} is %(py5)s',))
#             414 LOAD_FAST                7 (@py_assert1)
#             416 LOAD_FAST                8 (@py_assert4)
#             418 BUILD_TUPLE              2
#             420 CALL                     4
#             428 LOAD_CONST              17 ('result')
#             430 LOAD_GLOBAL             29 (NULL + @py_builtins)
#             440 LOAD_ATTR               30 (locals)
#             460 CALL                     0
#             468 CONTAINS_OP              0
#             470 POP_JUMP_IF_TRUE        21 (to 514)
#             472 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             482 LOAD_ATTR               32 (_should_repr_global_name)
#             502 LOAD_FAST                6 (result)
#             504 CALL                     1
#             512 POP_JUMP_IF_FALSE       21 (to 556)
#         >>  514 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             524 LOAD_ATTR               34 (_saferepr)
#             544 LOAD_FAST                6 (result)
#             546 CALL                     1
#             554 JUMP_FORWARD             1 (to 558)
#         >>  556 LOAD_CONST              17 ('result')
#         >>  558 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             568 LOAD_ATTR               34 (_saferepr)
#             588 LOAD_FAST                7 (@py_assert1)
#             590 CALL                     1
#             598 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             608 LOAD_ATTR               34 (_saferepr)
#             628 LOAD_FAST                8 (@py_assert4)
#             630 CALL                     1
#             638 LOAD_CONST              18 (('py0', 'py2', 'py5'))
#             640 BUILD_CONST_KEY_MAP      3
#             642 BINARY_OP                6 (%)
#             646 STORE_FAST              10 (@py_format6)
#             648 LOAD_CONST              19 ('assert %(py7)s')
#             650 LOAD_CONST              20 ('py7')
#             652 LOAD_FAST               10 (@py_format6)
#             654 BUILD_MAP                1
#             656 BINARY_OP                6 (%)
#             660 STORE_FAST              11 (@py_format8)
#             662 LOAD_GLOBAL             37 (NULL + AssertionError)
#             672 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             682 LOAD_ATTR               38 (_format_explanation)
#             702 LOAD_FAST               11 (@py_format8)
#             704 CALL                     1
#             712 CALL                     1
#             720 RAISE_VARARGS            1
#         >>  722 LOAD_CONST               0 (None)
#             724 COPY                     1
#             726 STORE_FAST               7 (@py_assert1)
#             728 COPY                     1
#             730 STORE_FAST               9 (@py_assert3)
#             732 STORE_FAST               8 (@py_assert4)
# 
# 149         734 LOAD_CONST              21 ('bus_count')
#             736 STORE_FAST              12 (@py_assert0)
#             738 LOAD_FAST                6 (result)
#             740 LOAD_ATTR               40 (data)
#             760 STORE_FAST               8 (@py_assert4)
#             762 LOAD_FAST               12 (@py_assert0)
#             764 LOAD_FAST                8 (@py_assert4)
#             766 CONTAINS_OP              0
#             768 STORE_FAST              13 (@py_assert2)
#             770 LOAD_FAST               13 (@py_assert2)
#             772 POP_JUMP_IF_TRUE       173 (to 1120)
#             774 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             784 LOAD_ATTR               26 (_call_reprcompare)
#             804 LOAD_CONST              22 (('in',))
#             806 LOAD_FAST               13 (@py_assert2)
#             808 BUILD_TUPLE              1
#             810 LOAD_CONST              23 (('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.data\n}',))
#             812 LOAD_FAST               12 (@py_assert0)
#             814 LOAD_FAST                8 (@py_assert4)
#             816 BUILD_TUPLE              2
#             818 CALL                     4
#             826 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             836 LOAD_ATTR               34 (_saferepr)
#             856 LOAD_FAST               12 (@py_assert0)
#             858 CALL                     1
#             866 LOAD_CONST              17 ('result')
#             868 LOAD_GLOBAL             29 (NULL + @py_builtins)
#             878 LOAD_ATTR               30 (locals)
#             898 CALL                     0
#             906 CONTAINS_OP              0
#             908 POP_JUMP_IF_TRUE        21 (to 952)
#             910 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             920 LOAD_ATTR               32 (_should_repr_global_name)
#             940 LOAD_FAST                6 (result)
#             942 CALL                     1
#             950 POP_JUMP_IF_FALSE       21 (to 994)
#         >>  952 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             962 LOAD_ATTR               34 (_saferepr)
#             982 LOAD_FAST                6 (result)
#             984 CALL                     1
#             992 JUMP_FORWARD             1 (to 996)
#         >>  994 LOAD_CONST              17 ('result')
#         >>  996 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1006 LOAD_ATTR               34 (_saferepr)
#            1026 LOAD_FAST                8 (@py_assert4)
#            1028 CALL                     1
#            1036 LOAD_CONST              24 (('py1', 'py3', 'py5'))
#            1038 BUILD_CONST_KEY_MAP      3
#            1040 BINARY_OP                6 (%)
#            1044 STORE_FAST              10 (@py_format6)
#            1046 LOAD_CONST              19 ('assert %(py7)s')
#            1048 LOAD_CONST              20 ('py7')
#            1050 LOAD_FAST               10 (@py_format6)
#            1052 BUILD_MAP                1
#            1054 BINARY_OP                6 (%)
#            1058 STORE_FAST              11 (@py_format8)
#            1060 LOAD_GLOBAL             37 (NULL + AssertionError)
#            1070 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1080 LOAD_ATTR               38 (_format_explanation)
#            1100 LOAD_FAST               11 (@py_format8)
#            1102 CALL                     1
#            1110 CALL                     1
#            1118 RAISE_VARARGS            1
#         >> 1120 LOAD_CONST               0 (None)
#            1122 COPY                     1
#            1124 STORE_FAST              12 (@py_assert0)
#            1126 COPY                     1
#            1128 STORE_FAST              13 (@py_assert2)
#            1130 STORE_FAST               8 (@py_assert4)
# 
# 150        1132 LOAD_FAST                6 (result)
#            1134 LOAD_ATTR               40 (data)
#            1154 LOAD_CONST              21 ('bus_count')
#            1156 BINARY_SUBSCR
#            1160 STORE_FAST              12 (@py_assert0)
#            1162 LOAD_CONST               4 (2)
#            1164 STORE_FAST               9 (@py_assert3)
#            1166 LOAD_FAST               12 (@py_assert0)
#            1168 LOAD_FAST                9 (@py_assert3)
#            1170 COMPARE_OP              40 (==)
#            1174 STORE_FAST              13 (@py_assert2)
#            1176 LOAD_FAST               13 (@py_assert2)
#            1178 POP_JUMP_IF_TRUE       108 (to 1396)
#            1180 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1190 LOAD_ATTR               26 (_call_reprcompare)
#            1210 LOAD_CONST              25 (('==',))
#            1212 LOAD_FAST               13 (@py_assert2)
#            1214 BUILD_TUPLE              1
#            1216 LOAD_CONST              26 (('%(py1)s == %(py4)s',))
#            1218 LOAD_FAST               12 (@py_assert0)
#            1220 LOAD_FAST                9 (@py_assert3)
#            1222 BUILD_TUPLE              2
#            1224 CALL                     4
#            1232 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1242 LOAD_ATTR               34 (_saferepr)
#            1262 LOAD_FAST               12 (@py_assert0)
#            1264 CALL                     1
#            1272 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1282 LOAD_ATTR               34 (_saferepr)
#            1302 LOAD_FAST                9 (@py_assert3)
#            1304 CALL                     1
#            1312 LOAD_CONST              27 (('py1', 'py4'))
#            1314 BUILD_CONST_KEY_MAP      2
#            1316 BINARY_OP                6 (%)
#            1320 STORE_FAST              14 (@py_format5)
#            1322 LOAD_CONST              28 ('assert %(py6)s')
#            1324 LOAD_CONST              29 ('py6')
#            1326 LOAD_FAST               14 (@py_format5)
#            1328 BUILD_MAP                1
#            1330 BINARY_OP                6 (%)
#            1334 STORE_FAST              15 (@py_format7)
#            1336 LOAD_GLOBAL             37 (NULL + AssertionError)
#            1346 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1356 LOAD_ATTR               38 (_format_explanation)
#            1376 LOAD_FAST               15 (@py_format7)
#            1378 CALL                     1
#            1386 CALL                     1
#            1394 RAISE_VARARGS            1
#         >> 1396 LOAD_CONST               0 (None)
#            1398 COPY                     1
#            1400 STORE_FAST              12 (@py_assert0)
#            1402 COPY                     1
#            1404 STORE_FAST              13 (@py_assert2)
#            1406 STORE_FAST               9 (@py_assert3)
# 
# 151        1408 LOAD_FAST                4 (mock_api)
#            1410 LOAD_ATTR               42 (connect)
#            1430 LOAD_ATTR               45 (NULL|self + assert_called_once)
#            1450 CALL                     0
#            1458 POP_TOP
# 
# 152        1460 LOAD_FAST                4 (mock_api)
#            1462 LOAD_ATTR               46 (disconnect)
#            1482 LOAD_ATTR               45 (NULL|self + assert_called_once)
#            1502 CALL                     0
#            1510 POP_TOP
#            1512 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_run_validation_failure at 0x3af9e5f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 154>:
# 154           0 RESUME                   0
# 
# 156           2 LOAD_CONST               1 ('model')
#               4 BUILD_MAP                0
#               6 BUILD_MAP                1
#               8 STORE_FAST               3 (config)
# 
# 157          10 LOAD_FAST                2 (skill_with_mock)
#              12 LOAD_ATTR                1 (NULL|self + run)
#              32 LOAD_FAST                3 (config)
#              34 CALL                     1
#              42 STORE_FAST               4 (result)
# 
# 159          44 LOAD_FAST                4 (result)
#              46 LOAD_ATTR                2 (is_success)
#              66 STORE_FAST               5 (@py_assert1)
#              68 LOAD_CONST               2 (False)
#              70 STORE_FAST               6 (@py_assert4)
#              72 LOAD_FAST                5 (@py_assert1)
#              74 LOAD_FAST                6 (@py_assert4)
#              76 IS_OP                    0
#              78 STORE_FAST               7 (@py_assert3)
#              80 LOAD_FAST                7 (@py_assert3)
#              82 POP_JUMP_IF_TRUE       173 (to 430)
#              84 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              94 LOAD_ATTR                6 (_call_reprcompare)
#             114 LOAD_CONST               3 (('is',))
#             116 LOAD_FAST                7 (@py_assert3)
#             118 BUILD_TUPLE              1
#             120 LOAD_CONST               4 (('%(py2)s\n{%(py2)s = %(py0)s.is_success\n} is %(py5)s',))
#             122 LOAD_FAST                5 (@py_assert1)
#             124 LOAD_FAST                6 (@py_assert4)
#             126 BUILD_TUPLE              2
#             128 CALL                     4
#             136 LOAD_CONST               5 ('result')
#             138 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             148 LOAD_ATTR               10 (locals)
#             168 CALL                     0
#             176 CONTAINS_OP              0
#             178 POP_JUMP_IF_TRUE        21 (to 222)
#             180 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             190 LOAD_ATTR               12 (_should_repr_global_name)
#             210 LOAD_FAST                4 (result)
#             212 CALL                     1
#             220 POP_JUMP_IF_FALSE       21 (to 264)
#         >>  222 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             232 LOAD_ATTR               14 (_saferepr)
#             252 LOAD_FAST                4 (result)
#             254 CALL                     1
#             262 JUMP_FORWARD             1 (to 266)
#         >>  264 LOAD_CONST               5 ('result')
#         >>  266 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             276 LOAD_ATTR               14 (_saferepr)
#             296 LOAD_FAST                5 (@py_assert1)
#             298 CALL                     1
#             306 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             316 LOAD_ATTR               14 (_saferepr)
#             336 LOAD_FAST                6 (@py_assert4)
#             338 CALL                     1
#             346 LOAD_CONST               6 (('py0', 'py2', 'py5'))
#             348 BUILD_CONST_KEY_MAP      3
#             350 BINARY_OP                6 (%)
#             354 STORE_FAST               8 (@py_format6)
#             356 LOAD_CONST               7 ('assert %(py7)s')
#             358 LOAD_CONST               8 ('py7')
#             360 LOAD_FAST                8 (@py_format6)
#             362 BUILD_MAP                1
#             364 BINARY_OP                6 (%)
#             368 STORE_FAST               9 (@py_format8)
#             370 LOAD_GLOBAL             17 (NULL + AssertionError)
#             380 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             390 LOAD_ATTR               18 (_format_explanation)
#             410 LOAD_FAST                9 (@py_format8)
#             412 CALL                     1
#             420 CALL                     1
#             428 RAISE_VARARGS            1
#         >>  430 LOAD_CONST               0 (None)
#             432 COPY                     1
#             434 STORE_FAST               5 (@py_assert1)
#             436 COPY                     1
#             438 STORE_FAST               7 (@py_assert3)
#             440 STORE_FAST               6 (@py_assert4)
# 
# 160         442 LOAD_CONST               9 ('validation')
#             444 STORE_FAST              10 (@py_assert0)
#             446 LOAD_FAST                4 (result)
#             448 LOAD_ATTR               20 (data)
#             468 STORE_FAST               6 (@py_assert4)
#             470 LOAD_FAST                6 (@py_assert4)
#             472 LOAD_ATTR               22 (get)
#             492 STORE_FAST              11 (@py_assert6)
#             494 LOAD_CONST              10 ('stage')
#             496 STORE_FAST              12 (@py_assert8)
#             498 LOAD_CONST              11 ('')
#             500 STORE_FAST              13 (@py_assert10)
#             502 PUSH_NULL
#             504 LOAD_FAST               11 (@py_assert6)
#             506 LOAD_FAST               12 (@py_assert8)
#             508 LOAD_FAST               13 (@py_assert10)
#             510 CALL                     2
#             518 STORE_FAST              14 (@py_assert12)
#             520 LOAD_FAST               10 (@py_assert0)
#             522 LOAD_FAST               14 (@py_assert12)
#             524 CONTAINS_OP              0
#             526 STORE_FAST              15 (@py_assert2)
#             528 LOAD_FAST               15 (@py_assert2)
#             530 POP_JUMP_IF_TRUE       253 (to 1038)
#             532 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             542 LOAD_ATTR                6 (_call_reprcompare)
#             562 LOAD_CONST              12 (('in',))
#             564 LOAD_FAST               15 (@py_assert2)
#             566 BUILD_TUPLE              1
#             568 LOAD_CONST              13 (('%(py1)s in %(py13)s\n{%(py13)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.data\n}.get\n}(%(py9)s, %(py11)s)\n}',))
#             570 LOAD_FAST               10 (@py_assert0)
#             572 LOAD_FAST               14 (@py_assert12)
#             574 BUILD_TUPLE              2
#             576 CALL                     4
#             584 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             594 LOAD_ATTR               14 (_saferepr)
#             614 LOAD_FAST               10 (@py_assert0)
#             616 CALL                     1
#             624 LOAD_CONST               5 ('result')
#             626 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             636 LOAD_ATTR               10 (locals)
#             656 CALL                     0
#             664 CONTAINS_OP              0
#             666 POP_JUMP_IF_TRUE        21 (to 710)
#             668 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             678 LOAD_ATTR               12 (_should_repr_global_name)
#             698 LOAD_FAST                4 (result)
#             700 CALL                     1
#             708 POP_JUMP_IF_FALSE       21 (to 752)
#         >>  710 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             720 LOAD_ATTR               14 (_saferepr)
#             740 LOAD_FAST                4 (result)
#             742 CALL                     1
#             750 JUMP_FORWARD             1 (to 754)
#         >>  752 LOAD_CONST               5 ('result')
#         >>  754 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             764 LOAD_ATTR               14 (_saferepr)
#             784 LOAD_FAST                6 (@py_assert4)
#             786 CALL                     1
#             794 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             804 LOAD_ATTR               14 (_saferepr)
#             824 LOAD_FAST               11 (@py_assert6)
#             826 CALL                     1
#             834 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             844 LOAD_ATTR               14 (_saferepr)
#             864 LOAD_FAST               12 (@py_assert8)
#             866 CALL                     1
#             874 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             884 LOAD_ATTR               14 (_saferepr)
#             904 LOAD_FAST               13 (@py_assert10)
#             906 CALL                     1
#             914 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             924 LOAD_ATTR               14 (_saferepr)
#             944 LOAD_FAST               14 (@py_assert12)
#             946 CALL                     1
#             954 LOAD_CONST              14 (('py1', 'py3', 'py5', 'py7', 'py9', 'py11', 'py13'))
#             956 BUILD_CONST_KEY_MAP      7
#             958 BINARY_OP                6 (%)
#             962 STORE_FAST              16 (@py_format14)
#             964 LOAD_CONST              15 ('assert %(py15)s')
#             966 LOAD_CONST              16 ('py15')
#             968 LOAD_FAST               16 (@py_format14)
#             970 BUILD_MAP                1
#             972 BINARY_OP                6 (%)
#             976 STORE_FAST              17 (@py_format16)
#             978 LOAD_GLOBAL             17 (NULL + AssertionError)
#             988 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             998 LOAD_ATTR               18 (_format_explanation)
#            1018 LOAD_FAST               17 (@py_format16)
#            1020 CALL                     1
#            1028 CALL                     1
#            1036 RAISE_VARARGS            1
#         >> 1038 LOAD_CONST               0 (None)
#            1040 COPY                     1
#            1042 STORE_FAST              10 (@py_assert0)
#            1044 COPY                     1
#            1046 STORE_FAST              15 (@py_assert2)
#            1048 COPY                     1
#            1050 STORE_FAST               6 (@py_assert4)
#            1052 COPY                     1
#            1054 STORE_FAST              11 (@py_assert6)
#            1056 COPY                     1
#            1058 STORE_FAST              12 (@py_assert8)
#            1060 COPY                     1
#            1062 STORE_FAST              13 (@py_assert10)
#            1064 STORE_FAST              14 (@py_assert12)
# 
# 161        1066 LOAD_FAST                1 (mock_factory)
#            1068 LOAD_ATTR               24 (create_powerflow_api)
#            1088 LOAD_ATTR               27 (NULL|self + assert_not_called)
#            1108 CALL                     0
#            1116 POP_TOP
#            1118 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestGenerateSummary at 0x73cd93b064c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 164>:
# 164           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestGenerateSummary')
#               8 STORE_NAME               2 (__qualname__)
# 
# 165          10 LOAD_CONST               1 ('Tests for _generate_summary method.')
#              12 STORE_NAME               3 (__doc__)
# 
# 167          14 LOAD_CONST               2 (<code object test_generate_summary_basic at 0x3afa7720, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 167>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_generate_summary_basic)
# 
# 187          20 LOAD_CONST               3 (<code object test_generate_summary_empty at 0x3af9ce50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 187>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_generate_summary_empty)
# 
# 193          26 LOAD_CONST               4 (<code object test_generate_summary_null_values at 0x3af96120, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 193>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_generate_summary_null_values)
#              32 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_generate_summary_basic at 0x3afa7720, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 167>:
# 167           0 RESUME                   0
# 
# 168           2 LOAD_GLOBAL              1 (NULL + PowerFlowPreset)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 170          22 LOAD_CONST               1 (100.0)
#              24 LOAD_CONST               2 (50.0)
#              26 LOAD_CONST               3 (80.0)
#              28 LOAD_CONST               4 (40.0)
#              30 LOAD_CONST               5 (1.05)
#              32 LOAD_CONST               6 (('Pg', 'Qg', 'Pl', 'Ql', 'Vm'))
#              34 BUILD_CONST_KEY_MAP      5
# 
# 171          36 LOAD_CONST               2 (50.0)
#              38 LOAD_CONST               7 (25.0)
#              40 LOAD_CONST               8 (60.0)
#              42 LOAD_CONST               9 (30.0)
#              44 LOAD_CONST              10 (0.98)
#              46 LOAD_CONST               6 (('Pg', 'Qg', 'Pl', 'Ql', 'Vm'))
#              48 BUILD_CONST_KEY_MAP      5
# 
# 169          50 BUILD_LIST               2
#              52 STORE_FAST               2 (buses)
# 
# 174          54 LOAD_CONST              11 ('Ploss')
#              56 LOAD_CONST              12 (2.5)
#              58 BUILD_MAP                1
# 
# 175          60 LOAD_CONST              11 ('Ploss')
#              62 LOAD_CONST              13 (1.5)
#              64 BUILD_MAP                1
# 
# 173          66 BUILD_LIST               2
#              68 STORE_FAST               3 (branches)
# 
# 178          70 LOAD_FAST                1 (skill)
#              72 LOAD_ATTR                3 (NULL|self + _generate_summary)
#              92 LOAD_FAST                2 (buses)
#              94 LOAD_FAST                3 (branches)
#              96 CALL                     2
#             104 STORE_FAST               4 (summary)
# 
# 180         106 LOAD_FAST                4 (summary)
#             108 LOAD_CONST              14 ('total_generation')
#             110 BINARY_SUBSCR
#             114 LOAD_CONST              15 ('p_mw')
#             116 BINARY_SUBSCR
#             120 STORE_FAST               5 (@py_assert0)
#             122 LOAD_CONST              16 (150.0)
#             124 STORE_FAST               6 (@py_assert3)
#             126 LOAD_FAST                5 (@py_assert0)
#             128 LOAD_FAST                6 (@py_assert3)
#             130 COMPARE_OP              40 (==)
#             134 STORE_FAST               7 (@py_assert2)
#             136 LOAD_FAST                7 (@py_assert2)
#             138 POP_JUMP_IF_TRUE       108 (to 356)
#             140 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             150 LOAD_ATTR                6 (_call_reprcompare)
#             170 LOAD_CONST              17 (('==',))
#             172 LOAD_FAST                7 (@py_assert2)
#             174 BUILD_TUPLE              1
#             176 LOAD_CONST              18 (('%(py1)s == %(py4)s',))
#             178 LOAD_FAST                5 (@py_assert0)
#             180 LOAD_FAST                6 (@py_assert3)
#             182 BUILD_TUPLE              2
#             184 CALL                     4
#             192 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             202 LOAD_ATTR                8 (_saferepr)
#             222 LOAD_FAST                5 (@py_assert0)
#             224 CALL                     1
#             232 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             242 LOAD_ATTR                8 (_saferepr)
#             262 LOAD_FAST                6 (@py_assert3)
#             264 CALL                     1
#             272 LOAD_CONST              19 (('py1', 'py4'))
#             274 BUILD_CONST_KEY_MAP      2
#             276 BINARY_OP                6 (%)
#             280 STORE_FAST               8 (@py_format5)
#             282 LOAD_CONST              20 ('assert %(py6)s')
#             284 LOAD_CONST              21 ('py6')
#             286 LOAD_FAST                8 (@py_format5)
#             288 BUILD_MAP                1
#             290 BINARY_OP                6 (%)
#             294 STORE_FAST               9 (@py_format7)
#             296 LOAD_GLOBAL             11 (NULL + AssertionError)
#             306 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             316 LOAD_ATTR               12 (_format_explanation)
#             336 LOAD_FAST                9 (@py_format7)
#             338 CALL                     1
#             346 CALL                     1
#             354 RAISE_VARARGS            1
#         >>  356 LOAD_CONST               0 (None)
#             358 COPY                     1
#             360 STORE_FAST               5 (@py_assert0)
#             362 COPY                     1
#             364 STORE_FAST               7 (@py_assert2)
#             366 STORE_FAST               6 (@py_assert3)
# 
# 181         368 LOAD_FAST                4 (summary)
#             370 LOAD_CONST              14 ('total_generation')
#             372 BINARY_SUBSCR
#             376 LOAD_CONST              22 ('q_mvar')
#             378 BINARY_SUBSCR
#             382 STORE_FAST               5 (@py_assert0)
#             384 LOAD_CONST              23 (75.0)
#             386 STORE_FAST               6 (@py_assert3)
#             388 LOAD_FAST                5 (@py_assert0)
#             390 LOAD_FAST                6 (@py_assert3)
#             392 COMPARE_OP              40 (==)
#             396 STORE_FAST               7 (@py_assert2)
#             398 LOAD_FAST                7 (@py_assert2)
#             400 POP_JUMP_IF_TRUE       108 (to 618)
#             402 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             412 LOAD_ATTR                6 (_call_reprcompare)
#             432 LOAD_CONST              17 (('==',))
#             434 LOAD_FAST                7 (@py_assert2)
#             436 BUILD_TUPLE              1
#             438 LOAD_CONST              18 (('%(py1)s == %(py4)s',))
#             440 LOAD_FAST                5 (@py_assert0)
#             442 LOAD_FAST                6 (@py_assert3)
#             444 BUILD_TUPLE              2
#             446 CALL                     4
#             454 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             464 LOAD_ATTR                8 (_saferepr)
#             484 LOAD_FAST                5 (@py_assert0)
#             486 CALL                     1
#             494 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             504 LOAD_ATTR                8 (_saferepr)
#             524 LOAD_FAST                6 (@py_assert3)
#             526 CALL                     1
#             534 LOAD_CONST              19 (('py1', 'py4'))
#             536 BUILD_CONST_KEY_MAP      2
#             538 BINARY_OP                6 (%)
#             542 STORE_FAST               8 (@py_format5)
#             544 LOAD_CONST              20 ('assert %(py6)s')
#             546 LOAD_CONST              21 ('py6')
#             548 LOAD_FAST                8 (@py_format5)
#             550 BUILD_MAP                1
#             552 BINARY_OP                6 (%)
#             556 STORE_FAST               9 (@py_format7)
#             558 LOAD_GLOBAL             11 (NULL + AssertionError)
#             568 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             578 LOAD_ATTR               12 (_format_explanation)
#             598 LOAD_FAST                9 (@py_format7)
#             600 CALL                     1
#             608 CALL                     1
#             616 RAISE_VARARGS            1
#         >>  618 LOAD_CONST               0 (None)
#             620 COPY                     1
#             622 STORE_FAST               5 (@py_assert0)
#             624 COPY                     1
#             626 STORE_FAST               7 (@py_assert2)
#             628 STORE_FAST               6 (@py_assert3)
# 
# 182         630 LOAD_FAST                4 (summary)
#             632 LOAD_CONST              24 ('total_load')
#             634 BINARY_SUBSCR
#             638 LOAD_CONST              15 ('p_mw')
#             640 BINARY_SUBSCR
#             644 STORE_FAST               5 (@py_assert0)
#             646 LOAD_CONST              25 (140.0)
#             648 STORE_FAST               6 (@py_assert3)
#             650 LOAD_FAST                5 (@py_assert0)
#             652 LOAD_FAST                6 (@py_assert3)
#             654 COMPARE_OP              40 (==)
#             658 STORE_FAST               7 (@py_assert2)
#             660 LOAD_FAST                7 (@py_assert2)
#             662 POP_JUMP_IF_TRUE       108 (to 880)
#             664 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             674 LOAD_ATTR                6 (_call_reprcompare)
#             694 LOAD_CONST              17 (('==',))
#             696 LOAD_FAST                7 (@py_assert2)
#             698 BUILD_TUPLE              1
#             700 LOAD_CONST              18 (('%(py1)s == %(py4)s',))
#             702 LOAD_FAST                5 (@py_assert0)
#             704 LOAD_FAST                6 (@py_assert3)
#             706 BUILD_TUPLE              2
#             708 CALL                     4
#             716 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             726 LOAD_ATTR                8 (_saferepr)
#             746 LOAD_FAST                5 (@py_assert0)
#             748 CALL                     1
#             756 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             766 LOAD_ATTR                8 (_saferepr)
#             786 LOAD_FAST                6 (@py_assert3)
#             788 CALL                     1
#             796 LOAD_CONST              19 (('py1', 'py4'))
#             798 BUILD_CONST_KEY_MAP      2
#             800 BINARY_OP                6 (%)
#             804 STORE_FAST               8 (@py_format5)
#             806 LOAD_CONST              20 ('assert %(py6)s')
#             808 LOAD_CONST              21 ('py6')
#             810 LOAD_FAST                8 (@py_format5)
#             812 BUILD_MAP                1
#             814 BINARY_OP                6 (%)
#             818 STORE_FAST               9 (@py_format7)
#             820 LOAD_GLOBAL             11 (NULL + AssertionError)
#             830 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             840 LOAD_ATTR               12 (_format_explanation)
#             860 LOAD_FAST                9 (@py_format7)
#             862 CALL                     1
#             870 CALL                     1
#             878 RAISE_VARARGS            1
#         >>  880 LOAD_CONST               0 (None)
#             882 COPY                     1
#             884 STORE_FAST               5 (@py_assert0)
#             886 COPY                     1
#             888 STORE_FAST               7 (@py_assert2)
#             890 STORE_FAST               6 (@py_assert3)
# 
# 183         892 LOAD_FAST                4 (summary)
#             894 LOAD_CONST              26 ('total_loss_mw')
#             896 BINARY_SUBSCR
#             900 STORE_FAST               5 (@py_assert0)
#             902 LOAD_CONST              27 (4.0)
#             904 STORE_FAST               6 (@py_assert3)
#             906 LOAD_FAST                5 (@py_assert0)
#             908 LOAD_FAST                6 (@py_assert3)
#             910 COMPARE_OP              40 (==)
#             914 STORE_FAST               7 (@py_assert2)
#             916 LOAD_FAST                7 (@py_assert2)
#             918 POP_JUMP_IF_TRUE       108 (to 1136)
#             920 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             930 LOAD_ATTR                6 (_call_reprcompare)
#             950 LOAD_CONST              17 (('==',))
#             952 LOAD_FAST                7 (@py_assert2)
#             954 BUILD_TUPLE              1
#             956 LOAD_CONST              18 (('%(py1)s == %(py4)s',))
#             958 LOAD_FAST                5 (@py_assert0)
#             960 LOAD_FAST                6 (@py_assert3)
#             962 BUILD_TUPLE              2
#             964 CALL                     4
#             972 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             982 LOAD_ATTR                8 (_saferepr)
#            1002 LOAD_FAST                5 (@py_assert0)
#            1004 CALL                     1
#            1012 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1022 LOAD_ATTR                8 (_saferepr)
#            1042 LOAD_FAST                6 (@py_assert3)
#            1044 CALL                     1
#            1052 LOAD_CONST              19 (('py1', 'py4'))
#            1054 BUILD_CONST_KEY_MAP      2
#            1056 BINARY_OP                6 (%)
#            1060 STORE_FAST               8 (@py_format5)
#            1062 LOAD_CONST              20 ('assert %(py6)s')
#            1064 LOAD_CONST              21 ('py6')
#            1066 LOAD_FAST                8 (@py_format5)
#            1068 BUILD_MAP                1
#            1070 BINARY_OP                6 (%)
#            1074 STORE_FAST               9 (@py_format7)
#            1076 LOAD_GLOBAL             11 (NULL + AssertionError)
#            1086 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1096 LOAD_ATTR               12 (_format_explanation)
#            1116 LOAD_FAST                9 (@py_format7)
#            1118 CALL                     1
#            1126 CALL                     1
#            1134 RAISE_VARARGS            1
#         >> 1136 LOAD_CONST               0 (None)
#            1138 COPY                     1
#            1140 STORE_FAST               5 (@py_assert0)
#            1142 COPY                     1
#            1144 STORE_FAST               7 (@py_assert2)
#            1146 STORE_FAST               6 (@py_assert3)
# 
# 184        1148 LOAD_FAST                4 (summary)
#            1150 LOAD_CONST              28 ('voltage_range')
#            1152 BINARY_SUBSCR
#            1156 LOAD_CONST              29 ('min_pu')
#            1158 BINARY_SUBSCR
#            1162 STORE_FAST               5 (@py_assert0)
#            1164 LOAD_CONST              10 (0.98)
#            1166 STORE_FAST               6 (@py_assert3)
#            1168 LOAD_FAST                5 (@py_assert0)
#            1170 LOAD_FAST                6 (@py_assert3)
#            1172 COMPARE_OP              40 (==)
#            1176 STORE_FAST               7 (@py_assert2)
#            1178 LOAD_FAST                7 (@py_assert2)
#            1180 POP_JUMP_IF_TRUE       108 (to 1398)
#            1182 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1192 LOAD_ATTR                6 (_call_reprcompare)
#            1212 LOAD_CONST              17 (('==',))
#            1214 LOAD_FAST                7 (@py_assert2)
#            1216 BUILD_TUPLE              1
#            1218 LOAD_CONST              18 (('%(py1)s == %(py4)s',))
#            1220 LOAD_FAST                5 (@py_assert0)
#            1222 LOAD_FAST                6 (@py_assert3)
#            1224 BUILD_TUPLE              2
#            1226 CALL                     4
#            1234 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1244 LOAD_ATTR                8 (_saferepr)
#            1264 LOAD_FAST                5 (@py_assert0)
#            1266 CALL                     1
#            1274 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1284 LOAD_ATTR                8 (_saferepr)
#            1304 LOAD_FAST                6 (@py_assert3)
#            1306 CALL                     1
#            1314 LOAD_CONST              19 (('py1', 'py4'))
#            1316 BUILD_CONST_KEY_MAP      2
#            1318 BINARY_OP                6 (%)
#            1322 STORE_FAST               8 (@py_format5)
#            1324 LOAD_CONST              20 ('assert %(py6)s')
#            1326 LOAD_CONST              21 ('py6')
#            1328 LOAD_FAST                8 (@py_format5)
#            1330 BUILD_MAP                1
#            1332 BINARY_OP                6 (%)
#            1336 STORE_FAST               9 (@py_format7)
#            1338 LOAD_GLOBAL             11 (NULL + AssertionError)
#            1348 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1358 LOAD_ATTR               12 (_format_explanation)
#            1378 LOAD_FAST                9 (@py_format7)
#            1380 CALL                     1
#            1388 CALL                     1
#            1396 RAISE_VARARGS            1
#         >> 1398 LOAD_CONST               0 (None)
#            1400 COPY                     1
#            1402 STORE_FAST               5 (@py_assert0)
#            1404 COPY                     1
#            1406 STORE_FAST               7 (@py_assert2)
#            1408 STORE_FAST               6 (@py_assert3)
# 
# 185        1410 LOAD_FAST                4 (summary)
#            1412 LOAD_CONST              28 ('voltage_range')
#            1414 BINARY_SUBSCR
#            1418 LOAD_CONST              30 ('max_pu')
#            1420 BINARY_SUBSCR
#            1424 STORE_FAST               5 (@py_assert0)
#            1426 LOAD_CONST               5 (1.05)
#            1428 STORE_FAST               6 (@py_assert3)
#            1430 LOAD_FAST                5 (@py_assert0)
#            1432 LOAD_FAST                6 (@py_assert3)
#            1434 COMPARE_OP              40 (==)
#            1438 STORE_FAST               7 (@py_assert2)
#            1440 LOAD_FAST                7 (@py_assert2)
#            1442 POP_JUMP_IF_TRUE       108 (to 1660)
#            1444 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1454 LOAD_ATTR                6 (_call_reprcompare)
#            1474 LOAD_CONST              17 (('==',))
#            1476 LOAD_FAST                7 (@py_assert2)
#            1478 BUILD_TUPLE              1
#            1480 LOAD_CONST              18 (('%(py1)s == %(py4)s',))
#            1482 LOAD_FAST                5 (@py_assert0)
#            1484 LOAD_FAST                6 (@py_assert3)
#            1486 BUILD_TUPLE              2
#            1488 CALL                     4
#            1496 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1506 LOAD_ATTR                8 (_saferepr)
#            1526 LOAD_FAST                5 (@py_assert0)
#            1528 CALL                     1
#            1536 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1546 LOAD_ATTR                8 (_saferepr)
#            1566 LOAD_FAST                6 (@py_assert3)
#            1568 CALL                     1
#            1576 LOAD_CONST              19 (('py1', 'py4'))
#            1578 BUILD_CONST_KEY_MAP      2
#            1580 BINARY_OP                6 (%)
#            1584 STORE_FAST               8 (@py_format5)
#            1586 LOAD_CONST              20 ('assert %(py6)s')
#            1588 LOAD_CONST              21 ('py6')
#            1590 LOAD_FAST                8 (@py_format5)
#            1592 BUILD_MAP                1
#            1594 BINARY_OP                6 (%)
#            1598 STORE_FAST               9 (@py_format7)
#            1600 LOAD_GLOBAL             11 (NULL + AssertionError)
#            1610 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1620 LOAD_ATTR               12 (_format_explanation)
#            1640 LOAD_FAST                9 (@py_format7)
#            1642 CALL                     1
#            1650 CALL                     1
#            1658 RAISE_VARARGS            1
#         >> 1660 LOAD_CONST               0 (None)
#            1662 COPY                     1
#            1664 STORE_FAST               5 (@py_assert0)
#            1666 COPY                     1
#            1668 STORE_FAST               7 (@py_assert2)
#            1670 STORE_FAST               6 (@py_assert3)
#            1672 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_generate_summary_empty at 0x3af9ce50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 187>:
# 187           0 RESUME                   0
# 
# 188           2 LOAD_GLOBAL              1 (NULL + PowerFlowPreset)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 189          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _generate_summary)
#              44 BUILD_LIST               0
#              46 BUILD_LIST               0
#              48 CALL                     2
#              56 STORE_FAST               2 (summary)
# 
# 190          58 LOAD_FAST                2 (summary)
#              60 LOAD_CONST               1 ('total_generation')
#              62 BINARY_SUBSCR
#              66 LOAD_CONST               2 ('p_mw')
#              68 BINARY_SUBSCR
#              72 STORE_FAST               3 (@py_assert0)
#              74 LOAD_CONST               3 (0.0)
#              76 STORE_FAST               4 (@py_assert3)
#              78 LOAD_FAST                3 (@py_assert0)
#              80 LOAD_FAST                4 (@py_assert3)
#              82 COMPARE_OP              40 (==)
#              86 STORE_FAST               5 (@py_assert2)
#              88 LOAD_FAST                5 (@py_assert2)
#              90 POP_JUMP_IF_TRUE       108 (to 308)
#              92 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             102 LOAD_ATTR                6 (_call_reprcompare)
#             122 LOAD_CONST               4 (('==',))
#             124 LOAD_FAST                5 (@py_assert2)
#             126 BUILD_TUPLE              1
#             128 LOAD_CONST               5 (('%(py1)s == %(py4)s',))
#             130 LOAD_FAST                3 (@py_assert0)
#             132 LOAD_FAST                4 (@py_assert3)
#             134 BUILD_TUPLE              2
#             136 CALL                     4
#             144 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             154 LOAD_ATTR                8 (_saferepr)
#             174 LOAD_FAST                3 (@py_assert0)
#             176 CALL                     1
#             184 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             194 LOAD_ATTR                8 (_saferepr)
#             214 LOAD_FAST                4 (@py_assert3)
#             216 CALL                     1
#             224 LOAD_CONST               6 (('py1', 'py4'))
#             226 BUILD_CONST_KEY_MAP      2
#             228 BINARY_OP                6 (%)
#             232 STORE_FAST               6 (@py_format5)
#             234 LOAD_CONST               7 ('assert %(py6)s')
#             236 LOAD_CONST               8 ('py6')
#             238 LOAD_FAST                6 (@py_format5)
#             240 BUILD_MAP                1
#             242 BINARY_OP                6 (%)
#             246 STORE_FAST               7 (@py_format7)
#             248 LOAD_GLOBAL             11 (NULL + AssertionError)
#             258 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             268 LOAD_ATTR               12 (_format_explanation)
#             288 LOAD_FAST                7 (@py_format7)
#             290 CALL                     1
#             298 CALL                     1
#             306 RAISE_VARARGS            1
#         >>  308 LOAD_CONST               0 (None)
#             310 COPY                     1
#             312 STORE_FAST               3 (@py_assert0)
#             314 COPY                     1
#             316 STORE_FAST               5 (@py_assert2)
#             318 STORE_FAST               4 (@py_assert3)
# 
# 191         320 LOAD_FAST                2 (summary)
#             322 LOAD_CONST               9 ('voltage_range')
#             324 BINARY_SUBSCR
#             328 LOAD_CONST              10 ('min_pu')
#             330 BINARY_SUBSCR
#             334 STORE_FAST               3 (@py_assert0)
#             336 LOAD_CONST              11 (999.0)
#             338 STORE_FAST               4 (@py_assert3)
#             340 LOAD_FAST                3 (@py_assert0)
#             342 LOAD_FAST                4 (@py_assert3)
#             344 COMPARE_OP              40 (==)
#             348 STORE_FAST               5 (@py_assert2)
#             350 LOAD_FAST                5 (@py_assert2)
#             352 POP_JUMP_IF_TRUE       108 (to 570)
#             354 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             364 LOAD_ATTR                6 (_call_reprcompare)
#             384 LOAD_CONST               4 (('==',))
#             386 LOAD_FAST                5 (@py_assert2)
#             388 BUILD_TUPLE              1
#             390 LOAD_CONST               5 (('%(py1)s == %(py4)s',))
#             392 LOAD_FAST                3 (@py_assert0)
#             394 LOAD_FAST                4 (@py_assert3)
#             396 BUILD_TUPLE              2
#             398 CALL                     4
#             406 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             416 LOAD_ATTR                8 (_saferepr)
#             436 LOAD_FAST                3 (@py_assert0)
#             438 CALL                     1
#             446 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             456 LOAD_ATTR                8 (_saferepr)
#             476 LOAD_FAST                4 (@py_assert3)
#             478 CALL                     1
#             486 LOAD_CONST               6 (('py1', 'py4'))
#             488 BUILD_CONST_KEY_MAP      2
#             490 BINARY_OP                6 (%)
#             494 STORE_FAST               6 (@py_format5)
#             496 LOAD_CONST               7 ('assert %(py6)s')
#             498 LOAD_CONST               8 ('py6')
#             500 LOAD_FAST                6 (@py_format5)
#             502 BUILD_MAP                1
#             504 BINARY_OP                6 (%)
#             508 STORE_FAST               7 (@py_format7)
#             510 LOAD_GLOBAL             11 (NULL + AssertionError)
#             520 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             530 LOAD_ATTR               12 (_format_explanation)
#             550 LOAD_FAST                7 (@py_format7)
#             552 CALL                     1
#             560 CALL                     1
#             568 RAISE_VARARGS            1
#         >>  570 LOAD_CONST               0 (None)
#             572 COPY                     1
#             574 STORE_FAST               3 (@py_assert0)
#             576 COPY                     1
#             578 STORE_FAST               5 (@py_assert2)
#             580 STORE_FAST               4 (@py_assert3)
#             582 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_generate_summary_null_values at 0x3af96120, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 193>:
# 193           0 RESUME                   0
# 
# 194           2 LOAD_GLOBAL              1 (NULL + PowerFlowPreset)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 196          22 LOAD_CONST               0 (None)
#              24 LOAD_CONST               1 ('')
#              26 LOAD_CONST               0 (None)
#              28 LOAD_CONST               2 (('Pg', 'Pl', 'Vm'))
#              30 BUILD_CONST_KEY_MAP      3
# 
# 195          32 BUILD_LIST               1
#              34 STORE_FAST               2 (buses)
# 
# 198          36 LOAD_FAST                1 (skill)
#              38 LOAD_ATTR                3 (NULL|self + _generate_summary)
#              58 LOAD_FAST                2 (buses)
#              60 BUILD_LIST               0
#              62 CALL                     2
#              70 STORE_FAST               3 (summary)
# 
# 199          72 LOAD_FAST                3 (summary)
#              74 LOAD_CONST               3 ('total_generation')
#              76 BINARY_SUBSCR
#              80 LOAD_CONST               4 ('p_mw')
#              82 BINARY_SUBSCR
#              86 STORE_FAST               4 (@py_assert0)
#              88 LOAD_CONST               5 (0.0)
#              90 STORE_FAST               5 (@py_assert3)
#              92 LOAD_FAST                4 (@py_assert0)
#              94 LOAD_FAST                5 (@py_assert3)
#              96 COMPARE_OP              40 (==)
#             100 STORE_FAST               6 (@py_assert2)
#             102 LOAD_FAST                6 (@py_assert2)
#             104 POP_JUMP_IF_TRUE       108 (to 322)
#             106 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             116 LOAD_ATTR                6 (_call_reprcompare)
#             136 LOAD_CONST               6 (('==',))
#             138 LOAD_FAST                6 (@py_assert2)
#             140 BUILD_TUPLE              1
#             142 LOAD_CONST               7 (('%(py1)s == %(py4)s',))
#             144 LOAD_FAST                4 (@py_assert0)
#             146 LOAD_FAST                5 (@py_assert3)
#             148 BUILD_TUPLE              2
#             150 CALL                     4
#             158 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             168 LOAD_ATTR                8 (_saferepr)
#             188 LOAD_FAST                4 (@py_assert0)
#             190 CALL                     1
#             198 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             208 LOAD_ATTR                8 (_saferepr)
#             228 LOAD_FAST                5 (@py_assert3)
#             230 CALL                     1
#             238 LOAD_CONST               8 (('py1', 'py4'))
#             240 BUILD_CONST_KEY_MAP      2
#             242 BINARY_OP                6 (%)
#             246 STORE_FAST               7 (@py_format5)
#             248 LOAD_CONST               9 ('assert %(py6)s')
#             250 LOAD_CONST              10 ('py6')
#             252 LOAD_FAST                7 (@py_format5)
#             254 BUILD_MAP                1
#             256 BINARY_OP                6 (%)
#             260 STORE_FAST               8 (@py_format7)
#             262 LOAD_GLOBAL             11 (NULL + AssertionError)
#             272 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             282 LOAD_ATTR               12 (_format_explanation)
#             302 LOAD_FAST                8 (@py_format7)
#             304 CALL                     1
#             312 CALL                     1
#             320 RAISE_VARARGS            1
#         >>  322 LOAD_CONST               0 (None)
#             324 COPY                     1
#             326 STORE_FAST               4 (@py_assert0)
#             328 COPY                     1
#             330 STORE_FAST               6 (@py_assert2)
#             332 STORE_FAST               5 (@py_assert3)
# 
# 200         334 LOAD_FAST                3 (summary)
#             336 LOAD_CONST              11 ('voltage_range')
#             338 BINARY_SUBSCR
#             342 LOAD_CONST              12 ('min_pu')
#             344 BINARY_SUBSCR
#             348 STORE_FAST               4 (@py_assert0)
#             350 LOAD_CONST              13 (1.0)
#             352 STORE_FAST               5 (@py_assert3)
#             354 LOAD_FAST                4 (@py_assert0)
#             356 LOAD_FAST                5 (@py_assert3)
#             358 COMPARE_OP              40 (==)
#             362 STORE_FAST               6 (@py_assert2)
#             364 LOAD_FAST                6 (@py_assert2)
#             366 POP_JUMP_IF_TRUE       108 (to 584)
#             368 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             378 LOAD_ATTR                6 (_call_reprcompare)
#             398 LOAD_CONST               6 (('==',))
#             400 LOAD_FAST                6 (@py_assert2)
#             402 BUILD_TUPLE              1
#             404 LOAD_CONST               7 (('%(py1)s == %(py4)s',))
#             406 LOAD_FAST                4 (@py_assert0)
#             408 LOAD_FAST                5 (@py_assert3)
#             410 BUILD_TUPLE              2
#             412 CALL                     4
#             420 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             430 LOAD_ATTR                8 (_saferepr)
#             450 LOAD_FAST                4 (@py_assert0)
#             452 CALL                     1
#             460 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             470 LOAD_ATTR                8 (_saferepr)
#             490 LOAD_FAST                5 (@py_assert3)
#             492 CALL                     1
#             500 LOAD_CONST               8 (('py1', 'py4'))
#             502 BUILD_CONST_KEY_MAP      2
#             504 BINARY_OP                6 (%)
#             508 STORE_FAST               7 (@py_format5)
#             510 LOAD_CONST               9 ('assert %(py6)s')
#             512 LOAD_CONST              10 ('py6')
#             514 LOAD_FAST                7 (@py_format5)
#             516 BUILD_MAP                1
#             518 BINARY_OP                6 (%)
#             522 STORE_FAST               8 (@py_format7)
#             524 LOAD_GLOBAL             11 (NULL + AssertionError)
#             534 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             544 LOAD_ATTR               12 (_format_explanation)
#             564 LOAD_FAST                8 (@py_format7)
#             566 CALL                     1
#             574 CALL                     1
#             582 RAISE_VARARGS            1
#         >>  584 LOAD_CONST               0 (None)
#             586 COPY                     1
#             588 STORE_FAST               4 (@py_assert0)
#             590 COPY                     1
#             592 STORE_FAST               6 (@py_assert2)
#             594 STORE_FAST               5 (@py_assert3)
#             596 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestPowerFlowPresetIntegration at 0x73cd945fedb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 203>:
# 203           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestPowerFlowPresetIntegration')
#               8 STORE_NAME               2 (__qualname__)
# 
# 204          10 LOAD_CONST               1 ('Integration-style tests (no real API calls).')
#              12 STORE_NAME               3 (__doc__)
# 
# 206          14 LOAD_CONST               2 (<code object test_skill_interface_complete at 0x3afa9880, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 206>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_skill_interface_complete)
# 
# 218          20 LOAD_CONST               3 (<code object test_skill_config_backward_compatible at 0x3af9d7e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 218>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_skill_config_backward_compatible)
#              26 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_skill_interface_complete at 0x3afa9880, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 206>:
# 206           0 RESUME                   0
# 
# 208           2 LOAD_GLOBAL              1 (NULL + PowerFlowPreset)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 210          22 LOAD_CONST               1 ('name')
#              24 STORE_FAST               2 (@py_assert2)
#              26 LOAD_GLOBAL              3 (NULL + hasattr)
#              36 LOAD_FAST                1 (skill)
#              38 LOAD_FAST                2 (@py_assert2)
#              40 CALL                     2
#              48 STORE_FAST               3 (@py_assert4)
#              50 LOAD_FAST                3 (@py_assert4)
#              52 POP_JUMP_IF_TRUE       214 (to 482)
#              54 LOAD_CONST               2 ('assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}')
#              56 LOAD_CONST               3 ('hasattr')
#              58 LOAD_GLOBAL              5 (NULL + @py_builtins)
#              68 LOAD_ATTR                6 (locals)
#              88 CALL                     0
#              96 CONTAINS_OP              0
#              98 POP_JUMP_IF_TRUE        25 (to 150)
#             100 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             110 LOAD_ATTR               10 (_should_repr_global_name)
#             130 LOAD_GLOBAL              2 (hasattr)
#             140 CALL                     1
#             148 POP_JUMP_IF_FALSE       25 (to 200)
#         >>  150 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             160 LOAD_ATTR               12 (_saferepr)
#             180 LOAD_GLOBAL              2 (hasattr)
#             190 CALL                     1
#             198 JUMP_FORWARD             1 (to 202)
#         >>  200 LOAD_CONST               3 ('hasattr')
#         >>  202 LOAD_CONST               4 ('skill')
#             204 LOAD_GLOBAL              5 (NULL + @py_builtins)
#             214 LOAD_ATTR                6 (locals)
#             234 CALL                     0
#             242 CONTAINS_OP              0
#             244 POP_JUMP_IF_TRUE        21 (to 288)
#             246 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             256 LOAD_ATTR               10 (_should_repr_global_name)
#             276 LOAD_FAST                1 (skill)
#             278 CALL                     1
#             286 POP_JUMP_IF_FALSE       21 (to 330)
#         >>  288 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             298 LOAD_ATTR               12 (_saferepr)
#             318 LOAD_FAST                1 (skill)
#             320 CALL                     1
#             328 JUMP_FORWARD             1 (to 332)
#         >>  330 LOAD_CONST               4 ('skill')
#         >>  332 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             342 LOAD_ATTR               12 (_saferepr)
#             362 LOAD_FAST                2 (@py_assert2)
#             364 CALL                     1
#             372 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             382 LOAD_ATTR               12 (_saferepr)
#             402 LOAD_FAST                3 (@py_assert4)
#             404 CALL                     1
#             412 LOAD_CONST               5 (('py0', 'py1', 'py3', 'py5'))
#             414 BUILD_CONST_KEY_MAP      4
#             416 BINARY_OP                6 (%)
#             420 STORE_FAST               4 (@py_format6)
#             422 LOAD_GLOBAL             15 (NULL + AssertionError)
#             432 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             442 LOAD_ATTR               16 (_format_explanation)
#             462 LOAD_FAST                4 (@py_format6)
#             464 CALL                     1
#             472 CALL                     1
#             480 RAISE_VARARGS            1
#         >>  482 LOAD_CONST               6 (None)
#             484 COPY                     1
#             486 STORE_FAST               2 (@py_assert2)
#             488 STORE_FAST               3 (@py_assert4)
# 
# 211         490 LOAD_CONST               7 ('description')
#             492 STORE_FAST               2 (@py_assert2)
#             494 LOAD_GLOBAL              3 (NULL + hasattr)
#             504 LOAD_FAST                1 (skill)
#             506 LOAD_FAST                2 (@py_assert2)
#             508 CALL                     2
#             516 STORE_FAST               3 (@py_assert4)
#             518 LOAD_FAST                3 (@py_assert4)
#             520 POP_JUMP_IF_TRUE       214 (to 950)
#             522 LOAD_CONST               2 ('assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}')
#             524 LOAD_CONST               3 ('hasattr')
#             526 LOAD_GLOBAL              5 (NULL + @py_builtins)
#             536 LOAD_ATTR                6 (locals)
#             556 CALL                     0
#             564 CONTAINS_OP              0
#             566 POP_JUMP_IF_TRUE        25 (to 618)
#             568 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             578 LOAD_ATTR               10 (_should_repr_global_name)
#             598 LOAD_GLOBAL              2 (hasattr)
#             608 CALL                     1
#             616 POP_JUMP_IF_FALSE       25 (to 668)
#         >>  618 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             628 LOAD_ATTR               12 (_saferepr)
#             648 LOAD_GLOBAL              2 (hasattr)
#             658 CALL                     1
#             666 JUMP_FORWARD             1 (to 670)
#         >>  668 LOAD_CONST               3 ('hasattr')
#         >>  670 LOAD_CONST               4 ('skill')
#             672 LOAD_GLOBAL              5 (NULL + @py_builtins)
#             682 LOAD_ATTR                6 (locals)
#             702 CALL                     0
#             710 CONTAINS_OP              0
#             712 POP_JUMP_IF_TRUE        21 (to 756)
#             714 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             724 LOAD_ATTR               10 (_should_repr_global_name)
#             744 LOAD_FAST                1 (skill)
#             746 CALL                     1
#             754 POP_JUMP_IF_FALSE       21 (to 798)
#         >>  756 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             766 LOAD_ATTR               12 (_saferepr)
#             786 LOAD_FAST                1 (skill)
#             788 CALL                     1
#             796 JUMP_FORWARD             1 (to 800)
#         >>  798 LOAD_CONST               4 ('skill')
#         >>  800 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             810 LOAD_ATTR               12 (_saferepr)
#             830 LOAD_FAST                2 (@py_assert2)
#             832 CALL                     1
#             840 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             850 LOAD_ATTR               12 (_saferepr)
#             870 LOAD_FAST                3 (@py_assert4)
#             872 CALL                     1
#             880 LOAD_CONST               5 (('py0', 'py1', 'py3', 'py5'))
#             882 BUILD_CONST_KEY_MAP      4
#             884 BINARY_OP                6 (%)
#             888 STORE_FAST               4 (@py_format6)
#             890 LOAD_GLOBAL             15 (NULL + AssertionError)
#             900 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             910 LOAD_ATTR               16 (_format_explanation)
#             930 LOAD_FAST                4 (@py_format6)
#             932 CALL                     1
#             940 CALL                     1
#             948 RAISE_VARARGS            1
#         >>  950 LOAD_CONST               6 (None)
#             952 COPY                     1
#             954 STORE_FAST               2 (@py_assert2)
#             956 STORE_FAST               3 (@py_assert4)
# 
# 212         958 LOAD_CONST               8 ('config_schema')
#             960 STORE_FAST               2 (@py_assert2)
#             962 LOAD_GLOBAL              3 (NULL + hasattr)
#             972 LOAD_FAST                1 (skill)
#             974 LOAD_FAST                2 (@py_assert2)
#             976 CALL                     2
#             984 STORE_FAST               3 (@py_assert4)
#             986 LOAD_FAST                3 (@py_assert4)
#             988 POP_JUMP_IF_TRUE       214 (to 1418)
#             990 LOAD_CONST               2 ('assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}')
#             992 LOAD_CONST               3 ('hasattr')
#             994 LOAD_GLOBAL              5 (NULL + @py_builtins)
#            1004 LOAD_ATTR                6 (locals)
#            1024 CALL                     0
#            1032 CONTAINS_OP              0
#            1034 POP_JUMP_IF_TRUE        25 (to 1086)
#            1036 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1046 LOAD_ATTR               10 (_should_repr_global_name)
#            1066 LOAD_GLOBAL              2 (hasattr)
#            1076 CALL                     1
#            1084 POP_JUMP_IF_FALSE       25 (to 1136)
#         >> 1086 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1096 LOAD_ATTR               12 (_saferepr)
#            1116 LOAD_GLOBAL              2 (hasattr)
#            1126 CALL                     1
#            1134 JUMP_FORWARD             1 (to 1138)
#         >> 1136 LOAD_CONST               3 ('hasattr')
#         >> 1138 LOAD_CONST               4 ('skill')
#            1140 LOAD_GLOBAL              5 (NULL + @py_builtins)
#            1150 LOAD_ATTR                6 (locals)
#            1170 CALL                     0
#            1178 CONTAINS_OP              0
#            1180 POP_JUMP_IF_TRUE        21 (to 1224)
#            1182 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1192 LOAD_ATTR               10 (_should_repr_global_name)
#            1212 LOAD_FAST                1 (skill)
#            1214 CALL                     1
#            1222 POP_JUMP_IF_FALSE       21 (to 1266)
#         >> 1224 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1234 LOAD_ATTR               12 (_saferepr)
#            1254 LOAD_FAST                1 (skill)
#            1256 CALL                     1
#            1264 JUMP_FORWARD             1 (to 1268)
#         >> 1266 LOAD_CONST               4 ('skill')
#         >> 1268 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1278 LOAD_ATTR               12 (_saferepr)
#            1298 LOAD_FAST                2 (@py_assert2)
#            1300 CALL                     1
#            1308 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1318 LOAD_ATTR               12 (_saferepr)
#            1338 LOAD_FAST                3 (@py_assert4)
#            1340 CALL                     1
#            1348 LOAD_CONST               5 (('py0', 'py1', 'py3', 'py5'))
#            1350 BUILD_CONST_KEY_MAP      4
#            1352 BINARY_OP                6 (%)
#            1356 STORE_FAST               4 (@py_format6)
#            1358 LOAD_GLOBAL             15 (NULL + AssertionError)
#            1368 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1378 LOAD_ATTR               16 (_format_explanation)
#            1398 LOAD_FAST                4 (@py_format6)
#            1400 CALL                     1
#            1408 CALL                     1
#            1416 RAISE_VARARGS            1
#         >> 1418 LOAD_CONST               6 (None)
#            1420 COPY                     1
#            1422 STORE_FAST               2 (@py_assert2)
#            1424 STORE_FAST               3 (@py_assert4)
# 
# 213        1426 LOAD_CONST               9 ('get_default_config')
#            1428 STORE_FAST               2 (@py_assert2)
#            1430 LOAD_GLOBAL              3 (NULL + hasattr)
#            1440 LOAD_FAST                1 (skill)
#            1442 LOAD_FAST                2 (@py_assert2)
#            1444 CALL                     2
#            1452 STORE_FAST               3 (@py_assert4)
#            1454 LOAD_FAST                3 (@py_assert4)
#            1456 POP_JUMP_IF_TRUE       214 (to 1886)
#            1458 LOAD_CONST               2 ('assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}')
#            1460 LOAD_CONST               3 ('hasattr')
#            1462 LOAD_GLOBAL              5 (NULL + @py_builtins)
#            1472 LOAD_ATTR                6 (locals)
#            1492 CALL                     0
#            1500 CONTAINS_OP              0
#            1502 POP_JUMP_IF_TRUE        25 (to 1554)
#            1504 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1514 LOAD_ATTR               10 (_should_repr_global_name)
#            1534 LOAD_GLOBAL              2 (hasattr)
#            1544 CALL                     1
#            1552 POP_JUMP_IF_FALSE       25 (to 1604)
#         >> 1554 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1564 LOAD_ATTR               12 (_saferepr)
#            1584 LOAD_GLOBAL              2 (hasattr)
#            1594 CALL                     1
#            1602 JUMP_FORWARD             1 (to 1606)
#         >> 1604 LOAD_CONST               3 ('hasattr')
#         >> 1606 LOAD_CONST               4 ('skill')
#            1608 LOAD_GLOBAL              5 (NULL + @py_builtins)
#            1618 LOAD_ATTR                6 (locals)
#            1638 CALL                     0
#            1646 CONTAINS_OP              0
#            1648 POP_JUMP_IF_TRUE        21 (to 1692)
#            1650 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1660 LOAD_ATTR               10 (_should_repr_global_name)
#            1680 LOAD_FAST                1 (skill)
#            1682 CALL                     1
#            1690 POP_JUMP_IF_FALSE       21 (to 1734)
#         >> 1692 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1702 LOAD_ATTR               12 (_saferepr)
#            1722 LOAD_FAST                1 (skill)
#            1724 CALL                     1
#            1732 JUMP_FORWARD             1 (to 1736)
#         >> 1734 LOAD_CONST               4 ('skill')
#         >> 1736 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1746 LOAD_ATTR               12 (_saferepr)
#            1766 LOAD_FAST                2 (@py_assert2)
#            1768 CALL                     1
#            1776 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1786 LOAD_ATTR               12 (_saferepr)
#            1806 LOAD_FAST                3 (@py_assert4)
#            1808 CALL                     1
#            1816 LOAD_CONST               5 (('py0', 'py1', 'py3', 'py5'))
#            1818 BUILD_CONST_KEY_MAP      4
#            1820 BINARY_OP                6 (%)
#            1824 STORE_FAST               4 (@py_format6)
#            1826 LOAD_GLOBAL             15 (NULL + AssertionError)
#            1836 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1846 LOAD_ATTR               16 (_format_explanation)
#            1866 LOAD_FAST                4 (@py_format6)
#            1868 CALL                     1
#            1876 CALL                     1
#            1884 RAISE_VARARGS            1
#         >> 1886 LOAD_CONST               6 (None)
#            1888 COPY                     1
#            1890 STORE_FAST               2 (@py_assert2)
#            1892 STORE_FAST               3 (@py_assert4)
# 
# 214        1894 LOAD_CONST              10 ('validate')
#            1896 STORE_FAST               2 (@py_assert2)
#            1898 LOAD_GLOBAL              3 (NULL + hasattr)
#            1908 LOAD_FAST                1 (skill)
#            1910 LOAD_FAST                2 (@py_assert2)
#            1912 CALL                     2
#            1920 STORE_FAST               3 (@py_assert4)
#            1922 LOAD_FAST                3 (@py_assert4)
#            1924 POP_JUMP_IF_TRUE       214 (to 2354)
#            1926 LOAD_CONST               2 ('assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}')
#            1928 LOAD_CONST               3 ('hasattr')
#            1930 LOAD_GLOBAL              5 (NULL + @py_builtins)
#            1940 LOAD_ATTR                6 (locals)
#            1960 CALL                     0
#            1968 CONTAINS_OP              0
#            1970 POP_JUMP_IF_TRUE        25 (to 2022)
#            1972 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1982 LOAD_ATTR               10 (_should_repr_global_name)
#            2002 LOAD_GLOBAL              2 (hasattr)
#            2012 CALL                     1
#            2020 POP_JUMP_IF_FALSE       25 (to 2072)
#         >> 2022 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            2032 LOAD_ATTR               12 (_saferepr)
#            2052 LOAD_GLOBAL              2 (hasattr)
#            2062 CALL                     1
#            2070 JUMP_FORWARD             1 (to 2074)
#         >> 2072 LOAD_CONST               3 ('hasattr')
#         >> 2074 LOAD_CONST               4 ('skill')
#            2076 LOAD_GLOBAL              5 (NULL + @py_builtins)
#            2086 LOAD_ATTR                6 (locals)
#            2106 CALL                     0
#            2114 CONTAINS_OP              0
#            2116 POP_JUMP_IF_TRUE        21 (to 2160)
#            2118 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            2128 LOAD_ATTR               10 (_should_repr_global_name)
#            2148 LOAD_FAST                1 (skill)
#            2150 CALL                     1
#            2158 POP_JUMP_IF_FALSE       21 (to 2202)
#         >> 2160 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            2170 LOAD_ATTR               12 (_saferepr)
#            2190 LOAD_FAST                1 (skill)
#            2192 CALL                     1
#            2200 JUMP_FORWARD             1 (to 2204)
#         >> 2202 LOAD_CONST               4 ('skill')
#         >> 2204 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            2214 LOAD_ATTR               12 (_saferepr)
#            2234 LOAD_FAST                2 (@py_assert2)
#            2236 CALL                     1
#            2244 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            2254 LOAD_ATTR               12 (_saferepr)
#            2274 LOAD_FAST                3 (@py_assert4)
#            2276 CALL                     1
#            2284 LOAD_CONST               5 (('py0', 'py1', 'py3', 'py5'))
#            2286 BUILD_CONST_KEY_MAP      4
#            2288 BINARY_OP                6 (%)
#            2292 STORE_FAST               4 (@py_format6)
#            2294 LOAD_GLOBAL             15 (NULL + AssertionError)
#            2304 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            2314 LOAD_ATTR               16 (_format_explanation)
#            2334 LOAD_FAST                4 (@py_format6)
#            2336 CALL                     1
#            2344 CALL                     1
#            2352 RAISE_VARARGS            1
#         >> 2354 LOAD_CONST               6 (None)
#            2356 COPY                     1
#            2358 STORE_FAST               2 (@py_assert2)
#            2360 STORE_FAST               3 (@py_assert4)
# 
# 215        2362 LOAD_CONST              11 ('run')
#            2364 STORE_FAST               2 (@py_assert2)
#            2366 LOAD_GLOBAL              3 (NULL + hasattr)
#            2376 LOAD_FAST                1 (skill)
#            2378 LOAD_FAST                2 (@py_assert2)
#            2380 CALL                     2
#            2388 STORE_FAST               3 (@py_assert4)
#            2390 LOAD_FAST                3 (@py_assert4)
#            2392 POP_JUMP_IF_TRUE       214 (to 2822)
#            2394 LOAD_CONST               2 ('assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}')
#            2396 LOAD_CONST               3 ('hasattr')
#            2398 LOAD_GLOBAL              5 (NULL + @py_builtins)
#            2408 LOAD_ATTR                6 (locals)
#            2428 CALL                     0
#            2436 CONTAINS_OP              0
#            2438 POP_JUMP_IF_TRUE        25 (to 2490)
#            2440 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            2450 LOAD_ATTR               10 (_should_repr_global_name)
#            2470 LOAD_GLOBAL              2 (hasattr)
#            2480 CALL                     1
#            2488 POP_JUMP_IF_FALSE       25 (to 2540)
#         >> 2490 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            2500 LOAD_ATTR               12 (_saferepr)
#            2520 LOAD_GLOBAL              2 (hasattr)
#            2530 CALL                     1
#            2538 JUMP_FORWARD             1 (to 2542)
#         >> 2540 LOAD_CONST               3 ('hasattr')
#         >> 2542 LOAD_CONST               4 ('skill')
#            2544 LOAD_GLOBAL              5 (NULL + @py_builtins)
#            2554 LOAD_ATTR                6 (locals)
#            2574 CALL                     0
#            2582 CONTAINS_OP              0
#            2584 POP_JUMP_IF_TRUE        21 (to 2628)
#            2586 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            2596 LOAD_ATTR               10 (_should_repr_global_name)
#            2616 LOAD_FAST                1 (skill)
#            2618 CALL                     1
#            2626 POP_JUMP_IF_FALSE       21 (to 2670)
#         >> 2628 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            2638 LOAD_ATTR               12 (_saferepr)
#            2658 LOAD_FAST                1 (skill)
#            2660 CALL                     1
#            2668 JUMP_FORWARD             1 (to 2672)
#         >> 2670 LOAD_CONST               4 ('skill')
#         >> 2672 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            2682 LOAD_ATTR               12 (_saferepr)
#            2702 LOAD_FAST                2 (@py_assert2)
#            2704 CALL                     1
#            2712 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            2722 LOAD_ATTR               12 (_saferepr)
#            2742 LOAD_FAST                3 (@py_assert4)
#            2744 CALL                     1
#            2752 LOAD_CONST               5 (('py0', 'py1', 'py3', 'py5'))
#            2754 BUILD_CONST_KEY_MAP      4
#            2756 BINARY_OP                6 (%)
#            2760 STORE_FAST               4 (@py_format6)
#            2762 LOAD_GLOBAL             15 (NULL + AssertionError)
#            2772 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            2782 LOAD_ATTR               16 (_format_explanation)
#            2802 LOAD_FAST                4 (@py_format6)
#            2804 CALL                     1
#            2812 CALL                     1
#            2820 RAISE_VARARGS            1
#         >> 2822 LOAD_CONST               6 (None)
#            2824 COPY                     1
#            2826 STORE_FAST               2 (@py_assert2)
#            2828 STORE_FAST               3 (@py_assert4)
# 
# 216        2830 LOAD_CONST              12 ('_generate_summary')
#            2832 STORE_FAST               2 (@py_assert2)
#            2834 LOAD_GLOBAL              3 (NULL + hasattr)
#            2844 LOAD_FAST                1 (skill)
#            2846 LOAD_FAST                2 (@py_assert2)
#            2848 CALL                     2
#            2856 STORE_FAST               3 (@py_assert4)
#            2858 LOAD_FAST                3 (@py_assert4)
#            2860 POP_JUMP_IF_TRUE       214 (to 3290)
#            2862 LOAD_CONST               2 ('assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}')
#            2864 LOAD_CONST               3 ('hasattr')
#            2866 LOAD_GLOBAL              5 (NULL + @py_builtins)
#            2876 LOAD_ATTR                6 (locals)
#            2896 CALL                     0
#            2904 CONTAINS_OP              0
#            2906 POP_JUMP_IF_TRUE        25 (to 2958)
#            2908 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            2918 LOAD_ATTR               10 (_should_repr_global_name)
#            2938 LOAD_GLOBAL              2 (hasattr)
#            2948 CALL                     1
#            2956 POP_JUMP_IF_FALSE       25 (to 3008)
#         >> 2958 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            2968 LOAD_ATTR               12 (_saferepr)
#            2988 LOAD_GLOBAL              2 (hasattr)
#            2998 CALL                     1
#            3006 JUMP_FORWARD             1 (to 3010)
#         >> 3008 LOAD_CONST               3 ('hasattr')
#         >> 3010 LOAD_CONST               4 ('skill')
#            3012 LOAD_GLOBAL              5 (NULL + @py_builtins)
#            3022 LOAD_ATTR                6 (locals)
#            3042 CALL                     0
#            3050 CONTAINS_OP              0
#            3052 POP_JUMP_IF_TRUE        21 (to 3096)
#            3054 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            3064 LOAD_ATTR               10 (_should_repr_global_name)
#            3084 LOAD_FAST                1 (skill)
#            3086 CALL                     1
#            3094 POP_JUMP_IF_FALSE       21 (to 3138)
#         >> 3096 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            3106 LOAD_ATTR               12 (_saferepr)
#            3126 LOAD_FAST                1 (skill)
#            3128 CALL                     1
#            3136 JUMP_FORWARD             1 (to 3140)
#         >> 3138 LOAD_CONST               4 ('skill')
#         >> 3140 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            3150 LOAD_ATTR               12 (_saferepr)
#            3170 LOAD_FAST                2 (@py_assert2)
#            3172 CALL                     1
#            3180 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            3190 LOAD_ATTR               12 (_saferepr)
#            3210 LOAD_FAST                3 (@py_assert4)
#            3212 CALL                     1
#            3220 LOAD_CONST               5 (('py0', 'py1', 'py3', 'py5'))
#            3222 BUILD_CONST_KEY_MAP      4
#            3224 BINARY_OP                6 (%)
#            3228 STORE_FAST               4 (@py_format6)
#            3230 LOAD_GLOBAL             15 (NULL + AssertionError)
#            3240 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            3250 LOAD_ATTR               16 (_format_explanation)
#            3270 LOAD_FAST                4 (@py_format6)
#            3272 CALL                     1
#            3280 CALL                     1
#            3288 RAISE_VARARGS            1
#         >> 3290 LOAD_CONST               6 (None)
#            3292 COPY                     1
#            3294 STORE_FAST               2 (@py_assert2)
#            3296 STORE_FAST               3 (@py_assert4)
#            3298 RETURN_CONST             6 (None)
# 
# Disassembly of <code object test_skill_config_backward_compatible at 0x3af9d7e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/skills/test_power_flow.py", line 218>:
# 218           0 RESUME                   0
# 
# 220           2 LOAD_GLOBAL              1 (NULL + PowerFlowPreset)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 221          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + get_default_config)
#              44 CALL                     0
#              52 STORE_FAST               2 (config)
# 
# 223          54 LOAD_CONST               1 ('skill')
#              56 STORE_FAST               3 (@py_assert0)
#              58 LOAD_FAST                3 (@py_assert0)
#              60 LOAD_FAST                2 (config)
#              62 CONTAINS_OP              0
#              64 STORE_FAST               4 (@py_assert2)
#              66 LOAD_FAST                4 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       153 (to 376)
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
#             302 LOAD_CONST               6 ('assert %(py5)s')
#             304 LOAD_CONST               7 ('py5')
#             306 LOAD_FAST                5 (@py_format4)
#             308 BUILD_MAP                1
#             310 BINARY_OP                6 (%)
#             314 STORE_FAST               6 (@py_format6)
#             316 LOAD_GLOBAL             17 (NULL + AssertionError)
#             326 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             336 LOAD_ATTR               18 (_format_explanation)
#             356 LOAD_FAST                6 (@py_format6)
#             358 CALL                     1
#             366 CALL                     1
#             374 RAISE_VARARGS            1
#         >>  376 LOAD_CONST               8 (None)
#             378 COPY                     1
#             380 STORE_FAST               3 (@py_assert0)
#             382 STORE_FAST               4 (@py_assert2)
# 
# 224         384 LOAD_CONST               9 ('model')
#             386 STORE_FAST               3 (@py_assert0)
#             388 LOAD_FAST                3 (@py_assert0)
#             390 LOAD_FAST                2 (config)
#             392 CONTAINS_OP              0
#             394 STORE_FAST               4 (@py_assert2)
#             396 LOAD_FAST                4 (@py_assert2)
#             398 POP_JUMP_IF_TRUE       153 (to 706)
#             400 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             410 LOAD_ATTR                6 (_call_reprcompare)
#             430 LOAD_CONST               2 (('in',))
#             432 LOAD_FAST                4 (@py_assert2)
#             434 BUILD_TUPLE              1
#             436 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             438 LOAD_FAST                3 (@py_assert0)
#             440 LOAD_FAST                2 (config)
#             442 BUILD_TUPLE              2
#             444 CALL                     4
#             452 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             462 LOAD_ATTR                8 (_saferepr)
#             482 LOAD_FAST                3 (@py_assert0)
#             484 CALL                     1
#             492 LOAD_CONST               4 ('config')
#             494 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             504 LOAD_ATTR               12 (locals)
#             524 CALL                     0
#             532 CONTAINS_OP              0
#             534 POP_JUMP_IF_TRUE        21 (to 578)
#             536 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             546 LOAD_ATTR               14 (_should_repr_global_name)
#             566 LOAD_FAST                2 (config)
#             568 CALL                     1
#             576 POP_JUMP_IF_FALSE       21 (to 620)
#         >>  578 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             588 LOAD_ATTR                8 (_saferepr)
#             608 LOAD_FAST                2 (config)
#             610 CALL                     1
#             618 JUMP_FORWARD             1 (to 622)
#         >>  620 LOAD_CONST               4 ('config')
#         >>  622 LOAD_CONST               5 (('py1', 'py3'))
#             624 BUILD_CONST_KEY_MAP      2
#             626 BINARY_OP                6 (%)
#             630 STORE_FAST               5 (@py_format4)
#             632 LOAD_CONST               6 ('assert %(py5)s')
#             634 LOAD_CONST               7 ('py5')
#             636 LOAD_FAST                5 (@py_format4)
#             638 BUILD_MAP                1
#             640 BINARY_OP                6 (%)
#             644 STORE_FAST               6 (@py_format6)
#             646 LOAD_GLOBAL             17 (NULL + AssertionError)
#             656 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             666 LOAD_ATTR               18 (_format_explanation)
#             686 LOAD_FAST                6 (@py_format6)
#             688 CALL                     1
#             696 CALL                     1
#             704 RAISE_VARARGS            1
#         >>  706 LOAD_CONST               8 (None)
#             708 COPY                     1
#             710 STORE_FAST               3 (@py_assert0)
#             712 STORE_FAST               4 (@py_assert2)
# 
# 225         714 LOAD_CONST              10 ('algorithm')
#             716 STORE_FAST               3 (@py_assert0)
#             718 LOAD_FAST                3 (@py_assert0)
#             720 LOAD_FAST                2 (config)
#             722 CONTAINS_OP              0
#             724 STORE_FAST               4 (@py_assert2)
#             726 LOAD_FAST                4 (@py_assert2)
#             728 POP_JUMP_IF_TRUE       153 (to 1036)
#             730 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             740 LOAD_ATTR                6 (_call_reprcompare)
#             760 LOAD_CONST               2 (('in',))
#             762 LOAD_FAST                4 (@py_assert2)
#             764 BUILD_TUPLE              1
#             766 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             768 LOAD_FAST                3 (@py_assert0)
#             770 LOAD_FAST                2 (config)
#             772 BUILD_TUPLE              2
#             774 CALL                     4
#             782 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             792 LOAD_ATTR                8 (_saferepr)
#             812 LOAD_FAST                3 (@py_assert0)
#             814 CALL                     1
#             822 LOAD_CONST               4 ('config')
#             824 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             834 LOAD_ATTR               12 (locals)
#             854 CALL                     0
#             862 CONTAINS_OP              0
#             864 POP_JUMP_IF_TRUE        21 (to 908)
#             866 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             876 LOAD_ATTR               14 (_should_repr_global_name)
#             896 LOAD_FAST                2 (config)
#             898 CALL                     1
#             906 POP_JUMP_IF_FALSE       21 (to 950)
#         >>  908 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             918 LOAD_ATTR                8 (_saferepr)
#             938 LOAD_FAST                2 (config)
#             940 CALL                     1
#             948 JUMP_FORWARD             1 (to 952)
#         >>  950 LOAD_CONST               4 ('config')
#         >>  952 LOAD_CONST               5 (('py1', 'py3'))
#             954 BUILD_CONST_KEY_MAP      2
#             956 BINARY_OP                6 (%)
#             960 STORE_FAST               5 (@py_format4)
#             962 LOAD_CONST               6 ('assert %(py5)s')
#             964 LOAD_CONST               7 ('py5')
#             966 LOAD_FAST                5 (@py_format4)
#             968 BUILD_MAP                1
#             970 BINARY_OP                6 (%)
#             974 STORE_FAST               6 (@py_format6)
#             976 LOAD_GLOBAL             17 (NULL + AssertionError)
#             986 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             996 LOAD_ATTR               18 (_format_explanation)
#            1016 LOAD_FAST                6 (@py_format6)
#            1018 CALL                     1
#            1026 CALL                     1
#            1034 RAISE_VARARGS            1
#         >> 1036 LOAD_CONST               8 (None)
#            1038 COPY                     1
#            1040 STORE_FAST               3 (@py_assert0)
#            1042 STORE_FAST               4 (@py_assert2)
# 
# 226        1044 LOAD_CONST              11 ('output')
#            1046 STORE_FAST               3 (@py_assert0)
#            1048 LOAD_FAST                3 (@py_assert0)
#            1050 LOAD_FAST                2 (config)
#            1052 CONTAINS_OP              0
#            1054 STORE_FAST               4 (@py_assert2)
#            1056 LOAD_FAST                4 (@py_assert2)
#            1058 POP_JUMP_IF_TRUE       153 (to 1366)
#            1060 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1070 LOAD_ATTR                6 (_call_reprcompare)
#            1090 LOAD_CONST               2 (('in',))
#            1092 LOAD_FAST                4 (@py_assert2)
#            1094 BUILD_TUPLE              1
#            1096 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#            1098 LOAD_FAST                3 (@py_assert0)
#            1100 LOAD_FAST                2 (config)
#            1102 BUILD_TUPLE              2
#            1104 CALL                     4
#            1112 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1122 LOAD_ATTR                8 (_saferepr)
#            1142 LOAD_FAST                3 (@py_assert0)
#            1144 CALL                     1
#            1152 LOAD_CONST               4 ('config')
#            1154 LOAD_GLOBAL             11 (NULL + @py_builtins)
#            1164 LOAD_ATTR               12 (locals)
#            1184 CALL                     0
#            1192 CONTAINS_OP              0
#            1194 POP_JUMP_IF_TRUE        21 (to 1238)
#            1196 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1206 LOAD_ATTR               14 (_should_repr_global_name)
#            1226 LOAD_FAST                2 (config)
#            1228 CALL                     1
#            1236 POP_JUMP_IF_FALSE       21 (to 1280)
#         >> 1238 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1248 LOAD_ATTR                8 (_saferepr)
#            1268 LOAD_FAST                2 (config)
#            1270 CALL                     1
#            1278 JUMP_FORWARD             1 (to 1282)
#         >> 1280 LOAD_CONST               4 ('config')
#         >> 1282 LOAD_CONST               5 (('py1', 'py3'))
#            1284 BUILD_CONST_KEY_MAP      2
#            1286 BINARY_OP                6 (%)
#            1290 STORE_FAST               5 (@py_format4)
#            1292 LOAD_CONST               6 ('assert %(py5)s')
#            1294 LOAD_CONST               7 ('py5')
#            1296 LOAD_FAST                5 (@py_format4)
#            1298 BUILD_MAP                1
#            1300 BINARY_OP                6 (%)
#            1304 STORE_FAST               6 (@py_format6)
#            1306 LOAD_GLOBAL             17 (NULL + AssertionError)
#            1316 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1326 LOAD_ATTR               18 (_format_explanation)
#            1346 LOAD_FAST                6 (@py_format6)
#            1348 CALL                     1
#            1356 CALL                     1
#            1364 RAISE_VARARGS            1
#         >> 1366 LOAD_CONST               8 (None)
#            1368 COPY                     1
#            1370 STORE_FAST               3 (@py_assert0)
#            1372 STORE_FAST               4 (@py_assert2)
# 
# 227        1374 LOAD_FAST                2 (config)
#            1376 LOAD_CONST              10 ('algorithm')
#            1378 BINARY_SUBSCR
#            1382 LOAD_CONST              12 ('tolerance')
#            1384 BINARY_SUBSCR
#            1388 STORE_FAST               3 (@py_assert0)
#            1390 LOAD_CONST              13 (1e-06)
#            1392 STORE_FAST               7 (@py_assert3)
#            1394 LOAD_FAST                3 (@py_assert0)
#            1396 LOAD_FAST                7 (@py_assert3)
#            1398 COMPARE_OP              40 (==)
#            1402 STORE_FAST               4 (@py_assert2)
#            1404 LOAD_FAST                4 (@py_assert2)
#            1406 POP_JUMP_IF_TRUE       108 (to 1624)
#            1408 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1418 LOAD_ATTR                6 (_call_reprcompare)
#            1438 LOAD_CONST              14 (('==',))
#            1440 LOAD_FAST                4 (@py_assert2)
#            1442 BUILD_TUPLE              1
#            1444 LOAD_CONST              15 (('%(py1)s == %(py4)s',))
#            1446 LOAD_FAST                3 (@py_assert0)
#            1448 LOAD_FAST                7 (@py_assert3)
#            1450 BUILD_TUPLE              2
#            1452 CALL                     4
#            1460 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1470 LOAD_ATTR                8 (_saferepr)
#            1490 LOAD_FAST                3 (@py_assert0)
#            1492 CALL                     1
#            1500 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1510 LOAD_ATTR                8 (_saferepr)
#            1530 LOAD_FAST                7 (@py_assert3)
#            1532 CALL                     1
#            1540 LOAD_CONST              16 (('py1', 'py4'))
#            1542 BUILD_CONST_KEY_MAP      2
#            1544 BINARY_OP                6 (%)
#            1548 STORE_FAST               8 (@py_format5)
#            1550 LOAD_CONST              17 ('assert %(py6)s')
#            1552 LOAD_CONST              18 ('py6')
#            1554 LOAD_FAST                8 (@py_format5)
#            1556 BUILD_MAP                1
#            1558 BINARY_OP                6 (%)
#            1562 STORE_FAST               9 (@py_format7)
#            1564 LOAD_GLOBAL             17 (NULL + AssertionError)
#            1574 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1584 LOAD_ATTR               18 (_format_explanation)
#            1604 LOAD_FAST                9 (@py_format7)
#            1606 CALL                     1
#            1614 CALL                     1
#            1622 RAISE_VARARGS            1
#         >> 1624 LOAD_CONST               8 (None)
#            1626 COPY                     1
#            1628 STORE_FAST               3 (@py_assert0)
#            1630 COPY                     1
#            1632 STORE_FAST               4 (@py_assert2)
#            1634 STORE_FAST               7 (@py_assert3)
#            1636 RETURN_CONST             8 (None)
# 