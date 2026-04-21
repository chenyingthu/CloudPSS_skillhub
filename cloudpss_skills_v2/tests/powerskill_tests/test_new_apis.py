# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/__pycache__/test_new_apis.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


class MockSCAdapter:
    """MockSCAdapter"""
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


class MockEMTAdapter:
    """MockEMTAdapter"""
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


def TestShortCircuit():
    """TestShortCircuit"""
pass  # TODO: restore


def TestEMT():
    """TestEMT"""
pass  # TODO: restore


def TestEngineNewMethods():
    """TestEngineNewMethods"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('Tests for ShortCircuit and EMT.')
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
#              42 LOAD_CONST               3 (('SimulationStatus', 'SimulationResult', 'ValidationResult', 'EngineAdapter', 'EngineConfig'))
#              44 IMPORT_NAME              8 (cloudpss_skills_v2.powerapi)
#              46 IMPORT_FROM              9 (SimulationStatus)
#              48 STORE_NAME               9 (SimulationStatus)
#              50 IMPORT_FROM             10 (SimulationResult)
#              52 STORE_NAME              10 (SimulationResult)
#              54 IMPORT_FROM             11 (ValidationResult)
#              56 STORE_NAME              11 (ValidationResult)
#              58 IMPORT_FROM             12 (EngineAdapter)
#              60 STORE_NAME              12 (EngineAdapter)
#              62 IMPORT_FROM             13 (EngineConfig)
#              64 STORE_NAME              13 (EngineConfig)
#              66 POP_TOP
# 
#  11          68 LOAD_CONST               1 (0)
#              70 LOAD_CONST               4 (('ShortCircuit', 'EMT', 'Engine'))
#              72 IMPORT_NAME             14 (cloudpss_skills_v2.powerskill)
#              74 IMPORT_FROM             15 (ShortCircuit)
#              76 STORE_NAME              15 (ShortCircuit)
#              78 IMPORT_FROM             16 (EMT)
#              80 STORE_NAME              16 (EMT)
#              82 IMPORT_FROM             17 (Engine)
#              84 STORE_NAME              17 (Engine)
#              86 POP_TOP
# 
#  14          88 PUSH_NULL
#              90 LOAD_BUILD_CLASS
#              92 LOAD_CONST               5 (<code object MockSCAdapter at 0x73cd93b39c50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 14>)
#              94 MAKE_FUNCTION            0
#              96 LOAD_CONST               6 ('MockSCAdapter')
#              98 LOAD_NAME               12 (EngineAdapter)
#             100 CALL                     3
#             108 STORE_NAME              18 (MockSCAdapter)
# 
#  51         110 PUSH_NULL
#             112 LOAD_BUILD_CLASS
#             114 LOAD_CONST               7 (<code object MockEMTAdapter at 0x73cd93b39a10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 51>)
#             116 MAKE_FUNCTION            0
#             118 LOAD_CONST               8 ('MockEMTAdapter')
#             120 LOAD_NAME               12 (EngineAdapter)
#             122 CALL                     3
#             130 STORE_NAME              19 (MockEMTAdapter)
# 
#  89         132 PUSH_NULL
#             134 LOAD_BUILD_CLASS
#             136 LOAD_CONST               9 (<code object TestShortCircuit at 0x73cd945fedb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 89>)
#             138 MAKE_FUNCTION            0
#             140 LOAD_CONST              10 ('TestShortCircuit')
#             142 CALL                     2
#             150 STORE_NAME              20 (TestShortCircuit)
# 
# 113         152 PUSH_NULL
#             154 LOAD_BUILD_CLASS
#             156 LOAD_CONST              11 (<code object TestEMT at 0x73cd93b065b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 113>)
#             158 MAKE_FUNCTION            0
#             160 LOAD_CONST              12 ('TestEMT')
#             162 CALL                     2
#             170 STORE_NAME              21 (TestEMT)
# 
# 148         172 PUSH_NULL
#             174 LOAD_BUILD_CLASS
#             176 LOAD_CONST              13 (<code object TestEngineNewMethods at 0x73cd93b064c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 148>)
#             178 MAKE_FUNCTION            0
#             180 LOAD_CONST              14 ('TestEngineNewMethods')
#             182 CALL                     2
#             190 STORE_NAME              22 (TestEngineNewMethods)
#             192 RETURN_CONST             2 (None)
# 
# Disassembly of <code object MockSCAdapter at 0x73cd93b39c50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 14>:
#               0 MAKE_CELL                0 (__class__)
# 
#  14           2 RESUME                   0
#               4 LOAD_NAME                0 (__name__)
#               6 STORE_NAME               1 (__module__)
#               8 LOAD_CONST               0 ('MockSCAdapter')
#              10 STORE_NAME               2 (__qualname__)
# 
#  15          12 LOAD_CONST               1 ('Mock adapter for testing ShortCircuit.')
#              14 STORE_NAME               3 (__doc__)
# 
#  17          16 LOAD_CLOSURE             0 (__class__)
#              18 BUILD_TUPLE              1
#              20 LOAD_CONST               2 (<code object __init__ at 0x73cd93b31930, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 17>)
#              22 MAKE_FUNCTION            8 (closure)
#              24 STORE_NAME               4 (__init__)
# 
#  20          26 LOAD_NAME                5 (property)
# 
#  21          28 LOAD_CONST               3 (<code object engine_name at 0x73cd93b13290, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 20>)
#              30 MAKE_FUNCTION            0
# 
#  20          32 CALL                     0
# 
#  21          40 STORE_NAME               6 (engine_name)
# 
#  24          42 LOAD_CONST               4 (<code object _do_connect at 0x73cd93b139e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 24>)
#              44 MAKE_FUNCTION            0
#              46 STORE_NAME               7 (_do_connect)
# 
#  27          48 LOAD_CONST               5 (<code object _do_disconnect at 0x73cd93b13840, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 27>)
#              50 MAKE_FUNCTION            0
#              52 STORE_NAME               8 (_do_disconnect)
# 
#  30          54 LOAD_CONST               6 (<code object _do_load_model at 0x73cd93b13910, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 30>)
#              56 MAKE_FUNCTION            0
#              58 STORE_NAME               9 (_do_load_model)
# 
#  33          60 LOAD_CONST               7 (<code object _do_run_simulation at 0x73cd93b1e340, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 33>)
#              62 MAKE_FUNCTION            0
#              64 STORE_NAME              10 (_do_run_simulation)
# 
#  40          66 LOAD_CONST               8 (<code object _do_get_result at 0x73cd93b1e560, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 40>)
#              68 MAKE_FUNCTION            0
#              70 STORE_NAME              11 (_do_get_result)
# 
#  47          72 LOAD_CONST               9 (<code object _do_validate_config at 0x73cd945fe790, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 47>)
#              74 MAKE_FUNCTION            0
#              76 STORE_NAME              12 (_do_validate_config)
#              78 LOAD_CLOSURE             0 (__class__)
#              80 COPY                     1
#              82 STORE_NAME              13 (__classcell__)
#              84 RETURN_VALUE
# 
# Disassembly of <code object __init__ at 0x73cd93b31930, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 17>:
#               0 COPY_FREE_VARS           1
# 
#  17           2 RESUME                   0
# 
#  18           4 LOAD_GLOBAL              0 (super)
#              14 LOAD_DEREF               1 (__class__)
#              16 LOAD_FAST                0 (self)
#              18 LOAD_SUPER_ATTR          5 (NULL|self + __init__)
#              22 LOAD_GLOBAL              5 (NULL + EngineConfig)
#              32 LOAD_CONST               1 ('mock')
#              34 KW_NAMES                 2 (('engine_name',))
#              36 CALL                     1
#              44 CALL                     1
#              52 POP_TOP
#              54 RETURN_CONST             0 (None)
# 
# Disassembly of <code object engine_name at 0x73cd93b13290, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 20>:
#  20           0 RESUME                   0
# 
#  22           2 RETURN_CONST             1 ('mock')
# 
# Disassembly of <code object _do_connect at 0x73cd93b139e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 24>:
#  24           0 RESUME                   0
# 
#  25           2 RETURN_CONST             0 (None)
# 
# Disassembly of <code object _do_disconnect at 0x73cd93b13840, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 27>:
#  27           0 RESUME                   0
# 
#  28           2 RETURN_CONST             0 (None)
# 
# Disassembly of <code object _do_load_model at 0x73cd93b13910, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 30>:
#  30           0 RESUME                   0
# 
#  31           2 RETURN_CONST             1 (True)
# 
# Disassembly of <code object _do_run_simulation at 0x73cd93b1e340, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 33>:
#  33           0 RESUME                   0
# 
#  34           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
#  35          12 LOAD_CONST               1 ('sc-job')
# 
#  36          14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
# 
#  37          44 LOAD_CONST               2 ('fault_currents')
#              46 LOAD_CONST               3 (1)
#              48 LOAD_CONST               4 (10.5)
#              50 LOAD_CONST               5 (('bus', 'current'))
#              52 BUILD_CONST_KEY_MAP      2
#              54 BUILD_LIST               1
#              56 BUILD_MAP                1
# 
#  34          58 KW_NAMES                 6 (('job_id', 'status', 'data'))
#              60 CALL                     3
#              68 RETURN_VALUE
# 
# Disassembly of <code object _do_get_result at 0x73cd93b1e560, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 40>:
#  40           0 RESUME                   0
# 
#  41           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
#  42          12 LOAD_FAST                1 (job_id)
# 
#  43          14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
# 
#  44          44 LOAD_CONST               1 ('fault_currents')
#              46 LOAD_CONST               2 (1)
#              48 LOAD_CONST               3 (10.5)
#              50 LOAD_CONST               4 (('bus', 'current'))
#              52 BUILD_CONST_KEY_MAP      2
#              54 BUILD_LIST               1
#              56 BUILD_MAP                1
# 
#  41          58 KW_NAMES                 5 (('job_id', 'status', 'data'))
#              60 CALL                     3
#              68 RETURN_VALUE
# 
# Disassembly of <code object _do_validate_config at 0x73cd945fe790, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 47>:
#  47           0 RESUME                   0
# 
#  48           2 LOAD_GLOBAL              1 (NULL + ValidationResult)
#              12 LOAD_CONST               1 (True)
#              14 KW_NAMES                 2 (('valid',))
#              16 CALL                     1
#              24 RETURN_VALUE
# 
# Disassembly of <code object MockEMTAdapter at 0x73cd93b39a10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 51>:
#               0 MAKE_CELL                0 (__class__)
# 
#  51           2 RESUME                   0
#               4 LOAD_NAME                0 (__name__)
#               6 STORE_NAME               1 (__module__)
#               8 LOAD_CONST               0 ('MockEMTAdapter')
#              10 STORE_NAME               2 (__qualname__)
# 
#  52          12 LOAD_CONST               1 ('Mock adapter for testing EMT.')
#              14 STORE_NAME               3 (__doc__)
# 
#  54          16 LOAD_CLOSURE             0 (__class__)
#              18 BUILD_TUPLE              1
#              20 LOAD_CONST               2 (<code object __init__ at 0x73cd93b31430, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 54>)
#              22 MAKE_FUNCTION            8 (closure)
#              24 STORE_NAME               4 (__init__)
# 
#  57          26 LOAD_NAME                5 (property)
# 
#  58          28 LOAD_CONST               3 (<code object engine_name at 0x73cd93b13360, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 57>)
#              30 MAKE_FUNCTION            0
# 
#  57          32 CALL                     0
# 
#  58          40 STORE_NAME               6 (engine_name)
# 
#  61          42 LOAD_CONST               4 (<code object _do_connect at 0x73cd93b13500, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 61>)
#              44 MAKE_FUNCTION            0
#              46 STORE_NAME               7 (_do_connect)
# 
#  64          48 LOAD_CONST               5 (<code object _do_disconnect at 0x73cd93b130f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 64>)
#              50 MAKE_FUNCTION            0
#              52 STORE_NAME               8 (_do_disconnect)
# 
#  67          54 LOAD_CONST               6 (<code object _do_load_model at 0x73cd93b136a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 67>)
#              56 MAKE_FUNCTION            0
#              58 STORE_NAME               9 (_do_load_model)
# 
#  70          60 LOAD_CONST               7 (<code object _do_run_simulation at 0x73cd93b398f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 70>)
#              62 MAKE_FUNCTION            0
#              64 STORE_NAME              10 (_do_run_simulation)
# 
#  78          66 LOAD_CONST               8 (<code object _do_get_result at 0x73cd93b31730, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 78>)
#              68 MAKE_FUNCTION            0
#              70 STORE_NAME              11 (_do_get_result)
# 
#  85          72 LOAD_CONST               9 (<code object _do_validate_config at 0x73cd945fe870, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 85>)
#              74 MAKE_FUNCTION            0
#              76 STORE_NAME              12 (_do_validate_config)
#              78 LOAD_CLOSURE             0 (__class__)
#              80 COPY                     1
#              82 STORE_NAME              13 (__classcell__)
#              84 RETURN_VALUE
# 
# Disassembly of <code object __init__ at 0x73cd93b31430, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 54>:
#               0 COPY_FREE_VARS           1
# 
#  54           2 RESUME                   0
# 
#  55           4 LOAD_GLOBAL              0 (super)
#              14 LOAD_DEREF               1 (__class__)
#              16 LOAD_FAST                0 (self)
#              18 LOAD_SUPER_ATTR          5 (NULL|self + __init__)
#              22 LOAD_GLOBAL              5 (NULL + EngineConfig)
#              32 LOAD_CONST               1 ('mock')
#              34 KW_NAMES                 2 (('engine_name',))
#              36 CALL                     1
#              44 CALL                     1
#              52 POP_TOP
#              54 RETURN_CONST             0 (None)
# 
# Disassembly of <code object engine_name at 0x73cd93b13360, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 57>:
#  57           0 RESUME                   0
# 
#  59           2 RETURN_CONST             1 ('mock')
# 
# Disassembly of <code object _do_connect at 0x73cd93b13500, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 61>:
#  61           0 RESUME                   0
# 
#  62           2 RETURN_CONST             0 (None)
# 
# Disassembly of <code object _do_disconnect at 0x73cd93b130f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 64>:
#  64           0 RESUME                   0
# 
#  65           2 RETURN_CONST             0 (None)
# 
# Disassembly of <code object _do_load_model at 0x73cd93b136a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 67>:
#  67           0 RESUME                   0
# 
#  68           2 RETURN_CONST             1 (True)
# 
# Disassembly of <code object _do_run_simulation at 0x73cd93b398f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 70>:
#  70           0 RESUME                   0
# 
#  71           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
#  72          12 LOAD_CONST               1 ('emt-job')
# 
#  73          14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
# 
#  74          44 LOAD_CONST               2 ('waveforms')
#              46 BUILD_LIST               0
#              48 LOAD_CONST               3 ((0, 1, 2))
#              50 LIST_EXTEND              1
#              52 BUILD_LIST               0
#              54 LOAD_CONST               4 ((1.0, 0.9, 1.1))
#              56 LIST_EXTEND              1
#              58 LOAD_CONST               5 (('time', 'voltage'))
#              60 BUILD_CONST_KEY_MAP      2
#              62 BUILD_LIST               1
#              64 BUILD_MAP                1
# 
#  75          66 LOAD_CONST               6 (0.0001)
#              68 LOAD_CONST               7 (1.0)
#              70 LOAD_CONST               8 (('time_step', 'end_time'))
#              72 BUILD_CONST_KEY_MAP      2
# 
#  71          74 KW_NAMES                 9 (('job_id', 'status', 'data', 'metadata'))
#              76 CALL                     4
#              84 RETURN_VALUE
# 
# Disassembly of <code object _do_get_result at 0x73cd93b31730, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 78>:
#  78           0 RESUME                   0
# 
#  79           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
#  80          12 LOAD_FAST                1 (job_id)
# 
#  81          14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
# 
#  82          44 LOAD_CONST               1 ('waveforms')
#              46 BUILD_LIST               0
#              48 BUILD_MAP                1
# 
#  79          50 KW_NAMES                 2 (('job_id', 'status', 'data'))
#              52 CALL                     3
#              60 RETURN_VALUE
# 
# Disassembly of <code object _do_validate_config at 0x73cd945fe870, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 85>:
#  85           0 RESUME                   0
# 
#  86           2 LOAD_GLOBAL              1 (NULL + ValidationResult)
#              12 LOAD_CONST               1 (True)
#              14 KW_NAMES                 2 (('valid',))
#              16 CALL                     1
#              24 RETURN_VALUE
# 
# Disassembly of <code object TestShortCircuit at 0x73cd945fedb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 89>:
#  89           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestShortCircuit')
#               8 STORE_NAME               2 (__qualname__)
# 
#  90          10 LOAD_CONST               1 ('Tests for ShortCircuit.')
#              12 STORE_NAME               3 (__doc__)
# 
#  92          14 LOAD_CONST               2 (<code object test_run_short_circuit at 0x3af94600, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 92>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_run_short_circuit)
# 
# 100          20 LOAD_CONST               3 (<code object test_get_fault_currents at 0x3afa50b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 100>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_get_fault_currents)
#              26 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_run_short_circuit at 0x3af94600, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 92>:
#  92           0 RESUME                   0
# 
#  93           2 LOAD_GLOBAL              1 (NULL + MockSCAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
#  94          22 LOAD_GLOBAL              3 (NULL + ShortCircuit)
#              32 LOAD_FAST                1 (adapter)
#              34 CALL                     1
#              42 STORE_FAST               2 (api)
# 
#  95          44 LOAD_FAST                2 (api)
#              46 LOAD_ATTR                5 (NULL|self + connect)
#              66 CALL                     0
#              74 POP_TOP
# 
#  96          76 LOAD_FAST                2 (api)
#              78 LOAD_ATTR                7 (NULL|self + run_short_circuit)
#              98 LOAD_CONST               1 ('test-model')
#             100 LOAD_CONST               2 ('3phase')
#             102 KW_NAMES                 3 (('model_id', 'fault_type'))
#             104 CALL                     2
#             112 STORE_FAST               3 (result)
# 
#  97         114 LOAD_FAST                3 (result)
#             116 LOAD_ATTR                8 (status)
#             136 STORE_FAST               4 (@py_assert1)
#             138 LOAD_GLOBAL             10 (SimulationStatus)
#             148 LOAD_ATTR               12 (COMPLETED)
#             168 STORE_FAST               5 (@py_assert5)
#             170 LOAD_FAST                4 (@py_assert1)
#             172 LOAD_FAST                5 (@py_assert5)
#             174 COMPARE_OP              40 (==)
#             178 STORE_FAST               6 (@py_assert3)
#             180 LOAD_FAST                6 (@py_assert3)
#             182 POP_JUMP_IF_TRUE       246 (to 676)
#             184 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             194 LOAD_ATTR               16 (_call_reprcompare)
#             214 LOAD_CONST               4 (('==',))
#             216 LOAD_FAST                6 (@py_assert3)
#             218 BUILD_TUPLE              1
#             220 LOAD_CONST               5 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.COMPLETED\n}',))
#             222 LOAD_FAST                4 (@py_assert1)
#             224 LOAD_FAST                5 (@py_assert5)
#             226 BUILD_TUPLE              2
#             228 CALL                     4
#             236 LOAD_CONST               6 ('result')
#             238 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             248 LOAD_ATTR               20 (locals)
#             268 CALL                     0
#             276 CONTAINS_OP              0
#             278 POP_JUMP_IF_TRUE        21 (to 322)
#             280 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             290 LOAD_ATTR               22 (_should_repr_global_name)
#             310 LOAD_FAST                3 (result)
#             312 CALL                     1
#             320 POP_JUMP_IF_FALSE       21 (to 364)
#         >>  322 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             332 LOAD_ATTR               24 (_saferepr)
#             352 LOAD_FAST                3 (result)
#             354 CALL                     1
#             362 JUMP_FORWARD             1 (to 366)
#         >>  364 LOAD_CONST               6 ('result')
#         >>  366 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             376 LOAD_ATTR               24 (_saferepr)
#             396 LOAD_FAST                4 (@py_assert1)
#             398 CALL                     1
#             406 LOAD_CONST               7 ('SimulationStatus')
#             408 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             418 LOAD_ATTR               20 (locals)
#             438 CALL                     0
#             446 CONTAINS_OP              0
#             448 POP_JUMP_IF_TRUE        25 (to 500)
#             450 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             460 LOAD_ATTR               22 (_should_repr_global_name)
#             480 LOAD_GLOBAL             10 (SimulationStatus)
#             490 CALL                     1
#             498 POP_JUMP_IF_FALSE       25 (to 550)
#         >>  500 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             510 LOAD_ATTR               24 (_saferepr)
#             530 LOAD_GLOBAL             10 (SimulationStatus)
#             540 CALL                     1
#             548 JUMP_FORWARD             1 (to 552)
#         >>  550 LOAD_CONST               7 ('SimulationStatus')
#         >>  552 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             562 LOAD_ATTR               24 (_saferepr)
#             582 LOAD_FAST                5 (@py_assert5)
#             584 CALL                     1
#             592 LOAD_CONST               8 (('py0', 'py2', 'py4', 'py6'))
#             594 BUILD_CONST_KEY_MAP      4
#             596 BINARY_OP                6 (%)
#             600 STORE_FAST               7 (@py_format7)
#             602 LOAD_CONST               9 ('assert %(py8)s')
#             604 LOAD_CONST              10 ('py8')
#             606 LOAD_FAST                7 (@py_format7)
#             608 BUILD_MAP                1
#             610 BINARY_OP                6 (%)
#             614 STORE_FAST               8 (@py_format9)
#             616 LOAD_GLOBAL             27 (NULL + AssertionError)
#             626 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             636 LOAD_ATTR               28 (_format_explanation)
#             656 LOAD_FAST                8 (@py_format9)
#             658 CALL                     1
#             666 CALL                     1
#             674 RAISE_VARARGS            1
#         >>  676 LOAD_CONST               0 (None)
#             678 COPY                     1
#             680 STORE_FAST               4 (@py_assert1)
#             682 COPY                     1
#             684 STORE_FAST               6 (@py_assert3)
#             686 STORE_FAST               5 (@py_assert5)
# 
#  98         688 LOAD_FAST                2 (api)
#             690 LOAD_ATTR               31 (NULL|self + disconnect)
#             710 CALL                     0
#             718 POP_TOP
#             720 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_get_fault_currents at 0x3afa50b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 100>:
# 100           0 RESUME                   0
# 
# 101           2 LOAD_GLOBAL              1 (NULL + MockSCAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
# 102          22 LOAD_GLOBAL              3 (NULL + ShortCircuit)
#              32 LOAD_FAST                1 (adapter)
#              34 CALL                     1
#              42 STORE_FAST               2 (api)
# 
# 103          44 LOAD_GLOBAL              5 (NULL + SimulationResult)
# 
# 104          54 LOAD_CONST               1 ('test')
# 
# 105          56 LOAD_GLOBAL              6 (SimulationStatus)
#              66 LOAD_ATTR                8 (COMPLETED)
# 
# 106          86 LOAD_CONST               2 ('fault_currents')
#              88 LOAD_CONST               3 (1)
#              90 LOAD_CONST               4 (10.5)
#              92 LOAD_CONST               5 (('bus', 'current'))
#              94 BUILD_CONST_KEY_MAP      2
#              96 BUILD_LIST               1
#              98 BUILD_MAP                1
# 
# 103         100 KW_NAMES                 6 (('job_id', 'status', 'data'))
#             102 CALL                     3
#             110 STORE_FAST               3 (result)
# 
# 108         112 LOAD_FAST                2 (api)
#             114 LOAD_ATTR               11 (NULL|self + get_fault_currents)
#             134 LOAD_FAST                3 (result)
#             136 CALL                     1
#             144 STORE_FAST               4 (currents)
# 
# 109         146 LOAD_GLOBAL             13 (NULL + len)
#             156 LOAD_FAST                4 (currents)
#             158 CALL                     1
#             166 STORE_FAST               5 (@py_assert2)
#             168 LOAD_CONST               3 (1)
#             170 STORE_FAST               6 (@py_assert5)
#             172 LOAD_FAST                5 (@py_assert2)
#             174 LOAD_FAST                6 (@py_assert5)
#             176 COMPARE_OP              40 (==)
#             180 STORE_FAST               7 (@py_assert4)
#             182 LOAD_FAST                7 (@py_assert4)
#             184 POP_JUMP_IF_TRUE       246 (to 678)
#             186 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             196 LOAD_ATTR               16 (_call_reprcompare)
#             216 LOAD_CONST               7 (('==',))
#             218 LOAD_FAST                7 (@py_assert4)
#             220 BUILD_TUPLE              1
#             222 LOAD_CONST               8 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             224 LOAD_FAST                5 (@py_assert2)
#             226 LOAD_FAST                6 (@py_assert5)
#             228 BUILD_TUPLE              2
#             230 CALL                     4
#             238 LOAD_CONST               9 ('len')
#             240 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             250 LOAD_ATTR               20 (locals)
#             270 CALL                     0
#             278 CONTAINS_OP              0
#             280 POP_JUMP_IF_TRUE        25 (to 332)
#             282 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             292 LOAD_ATTR               22 (_should_repr_global_name)
#             312 LOAD_GLOBAL             12 (len)
#             322 CALL                     1
#             330 POP_JUMP_IF_FALSE       25 (to 382)
#         >>  332 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             342 LOAD_ATTR               24 (_saferepr)
#             362 LOAD_GLOBAL             12 (len)
#             372 CALL                     1
#             380 JUMP_FORWARD             1 (to 384)
#         >>  382 LOAD_CONST               9 ('len')
#         >>  384 LOAD_CONST              10 ('currents')
#             386 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             396 LOAD_ATTR               20 (locals)
#             416 CALL                     0
#             424 CONTAINS_OP              0
#             426 POP_JUMP_IF_TRUE        21 (to 470)
#             428 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             438 LOAD_ATTR               22 (_should_repr_global_name)
#             458 LOAD_FAST                4 (currents)
#             460 CALL                     1
#             468 POP_JUMP_IF_FALSE       21 (to 512)
#         >>  470 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             480 LOAD_ATTR               24 (_saferepr)
#             500 LOAD_FAST                4 (currents)
#             502 CALL                     1
#             510 JUMP_FORWARD             1 (to 514)
#         >>  512 LOAD_CONST              10 ('currents')
#         >>  514 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             524 LOAD_ATTR               24 (_saferepr)
#             544 LOAD_FAST                5 (@py_assert2)
#             546 CALL                     1
#             554 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             564 LOAD_ATTR               24 (_saferepr)
#             584 LOAD_FAST                6 (@py_assert5)
#             586 CALL                     1
#             594 LOAD_CONST              11 (('py0', 'py1', 'py3', 'py6'))
#             596 BUILD_CONST_KEY_MAP      4
#             598 BINARY_OP                6 (%)
#             602 STORE_FAST               8 (@py_format7)
#             604 LOAD_CONST              12 ('assert %(py8)s')
#             606 LOAD_CONST              13 ('py8')
#             608 LOAD_FAST                8 (@py_format7)
#             610 BUILD_MAP                1
#             612 BINARY_OP                6 (%)
#             616 STORE_FAST               9 (@py_format9)
#             618 LOAD_GLOBAL             27 (NULL + AssertionError)
#             628 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             638 LOAD_ATTR               28 (_format_explanation)
#             658 LOAD_FAST                9 (@py_format9)
#             660 CALL                     1
#             668 CALL                     1
#             676 RAISE_VARARGS            1
#         >>  678 LOAD_CONST               0 (None)
#             680 COPY                     1
#             682 STORE_FAST               5 (@py_assert2)
#             684 COPY                     1
#             686 STORE_FAST               7 (@py_assert4)
#             688 STORE_FAST               6 (@py_assert5)
# 
# 110         690 LOAD_FAST                4 (currents)
#             692 LOAD_CONST              14 (0)
#             694 BINARY_SUBSCR
#             698 LOAD_CONST              15 ('bus')
#             700 BINARY_SUBSCR
#             704 STORE_FAST              10 (@py_assert0)
#             706 LOAD_CONST               3 (1)
#             708 STORE_FAST              11 (@py_assert3)
#             710 LOAD_FAST               10 (@py_assert0)
#             712 LOAD_FAST               11 (@py_assert3)
#             714 COMPARE_OP              40 (==)
#             718 STORE_FAST               5 (@py_assert2)
#             720 LOAD_FAST                5 (@py_assert2)
#             722 POP_JUMP_IF_TRUE       108 (to 940)
#             724 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             734 LOAD_ATTR               16 (_call_reprcompare)
#             754 LOAD_CONST               7 (('==',))
#             756 LOAD_FAST                5 (@py_assert2)
#             758 BUILD_TUPLE              1
#             760 LOAD_CONST              16 (('%(py1)s == %(py4)s',))
#             762 LOAD_FAST               10 (@py_assert0)
#             764 LOAD_FAST               11 (@py_assert3)
#             766 BUILD_TUPLE              2
#             768 CALL                     4
#             776 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             786 LOAD_ATTR               24 (_saferepr)
#             806 LOAD_FAST               10 (@py_assert0)
#             808 CALL                     1
#             816 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             826 LOAD_ATTR               24 (_saferepr)
#             846 LOAD_FAST               11 (@py_assert3)
#             848 CALL                     1
#             856 LOAD_CONST              17 (('py1', 'py4'))
#             858 BUILD_CONST_KEY_MAP      2
#             860 BINARY_OP                6 (%)
#             864 STORE_FAST              12 (@py_format5)
#             866 LOAD_CONST              18 ('assert %(py6)s')
#             868 LOAD_CONST              19 ('py6')
#             870 LOAD_FAST               12 (@py_format5)
#             872 BUILD_MAP                1
#             874 BINARY_OP                6 (%)
#             878 STORE_FAST               8 (@py_format7)
#             880 LOAD_GLOBAL             27 (NULL + AssertionError)
#             890 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             900 LOAD_ATTR               28 (_format_explanation)
#             920 LOAD_FAST                8 (@py_format7)
#             922 CALL                     1
#             930 CALL                     1
#             938 RAISE_VARARGS            1
#         >>  940 LOAD_CONST               0 (None)
#             942 COPY                     1
#             944 STORE_FAST              10 (@py_assert0)
#             946 COPY                     1
#             948 STORE_FAST               5 (@py_assert2)
#             950 STORE_FAST              11 (@py_assert3)
#             952 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestEMT at 0x73cd93b065b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 113>:
# 113           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestEMT')
#               8 STORE_NAME               2 (__qualname__)
# 
# 114          10 LOAD_CONST               1 ('Tests for EMT.')
#              12 STORE_NAME               3 (__doc__)
# 
# 116          14 LOAD_CONST               2 (<code object test_run_emt at 0x3af9b610, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 116>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_run_emt)
# 
# 124          20 LOAD_CONST               3 (<code object test_get_waveforms at 0x3af994a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 124>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_get_waveforms)
# 
# 135          26 LOAD_CONST               4 (<code object test_get_metadata at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 135>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_get_metadata)
#              32 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_run_emt at 0x3af9b610, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 116>:
# 116           0 RESUME                   0
# 
# 117           2 LOAD_GLOBAL              1 (NULL + MockEMTAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
# 118          22 LOAD_GLOBAL              3 (NULL + EMT)
#              32 LOAD_FAST                1 (adapter)
#              34 CALL                     1
#              42 STORE_FAST               2 (api)
# 
# 119          44 LOAD_FAST                2 (api)
#              46 LOAD_ATTR                5 (NULL|self + connect)
#              66 CALL                     0
#              74 POP_TOP
# 
# 120          76 LOAD_FAST                2 (api)
#              78 LOAD_ATTR                7 (NULL|self + run_emt)
#              98 LOAD_CONST               1 ('test-model')
#             100 LOAD_CONST               2 (0.001)
#             102 KW_NAMES                 3 (('model_id', 'time_step'))
#             104 CALL                     2
#             112 STORE_FAST               3 (result)
# 
# 121         114 LOAD_FAST                3 (result)
#             116 LOAD_ATTR                8 (status)
#             136 STORE_FAST               4 (@py_assert1)
#             138 LOAD_GLOBAL             10 (SimulationStatus)
#             148 LOAD_ATTR               12 (COMPLETED)
#             168 STORE_FAST               5 (@py_assert5)
#             170 LOAD_FAST                4 (@py_assert1)
#             172 LOAD_FAST                5 (@py_assert5)
#             174 COMPARE_OP              40 (==)
#             178 STORE_FAST               6 (@py_assert3)
#             180 LOAD_FAST                6 (@py_assert3)
#             182 POP_JUMP_IF_TRUE       246 (to 676)
#             184 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             194 LOAD_ATTR               16 (_call_reprcompare)
#             214 LOAD_CONST               4 (('==',))
#             216 LOAD_FAST                6 (@py_assert3)
#             218 BUILD_TUPLE              1
#             220 LOAD_CONST               5 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.COMPLETED\n}',))
#             222 LOAD_FAST                4 (@py_assert1)
#             224 LOAD_FAST                5 (@py_assert5)
#             226 BUILD_TUPLE              2
#             228 CALL                     4
#             236 LOAD_CONST               6 ('result')
#             238 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             248 LOAD_ATTR               20 (locals)
#             268 CALL                     0
#             276 CONTAINS_OP              0
#             278 POP_JUMP_IF_TRUE        21 (to 322)
#             280 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             290 LOAD_ATTR               22 (_should_repr_global_name)
#             310 LOAD_FAST                3 (result)
#             312 CALL                     1
#             320 POP_JUMP_IF_FALSE       21 (to 364)
#         >>  322 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             332 LOAD_ATTR               24 (_saferepr)
#             352 LOAD_FAST                3 (result)
#             354 CALL                     1
#             362 JUMP_FORWARD             1 (to 366)
#         >>  364 LOAD_CONST               6 ('result')
#         >>  366 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             376 LOAD_ATTR               24 (_saferepr)
#             396 LOAD_FAST                4 (@py_assert1)
#             398 CALL                     1
#             406 LOAD_CONST               7 ('SimulationStatus')
#             408 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             418 LOAD_ATTR               20 (locals)
#             438 CALL                     0
#             446 CONTAINS_OP              0
#             448 POP_JUMP_IF_TRUE        25 (to 500)
#             450 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             460 LOAD_ATTR               22 (_should_repr_global_name)
#             480 LOAD_GLOBAL             10 (SimulationStatus)
#             490 CALL                     1
#             498 POP_JUMP_IF_FALSE       25 (to 550)
#         >>  500 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             510 LOAD_ATTR               24 (_saferepr)
#             530 LOAD_GLOBAL             10 (SimulationStatus)
#             540 CALL                     1
#             548 JUMP_FORWARD             1 (to 552)
#         >>  550 LOAD_CONST               7 ('SimulationStatus')
#         >>  552 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             562 LOAD_ATTR               24 (_saferepr)
#             582 LOAD_FAST                5 (@py_assert5)
#             584 CALL                     1
#             592 LOAD_CONST               8 (('py0', 'py2', 'py4', 'py6'))
#             594 BUILD_CONST_KEY_MAP      4
#             596 BINARY_OP                6 (%)
#             600 STORE_FAST               7 (@py_format7)
#             602 LOAD_CONST               9 ('assert %(py8)s')
#             604 LOAD_CONST              10 ('py8')
#             606 LOAD_FAST                7 (@py_format7)
#             608 BUILD_MAP                1
#             610 BINARY_OP                6 (%)
#             614 STORE_FAST               8 (@py_format9)
#             616 LOAD_GLOBAL             27 (NULL + AssertionError)
#             626 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             636 LOAD_ATTR               28 (_format_explanation)
#             656 LOAD_FAST                8 (@py_format9)
#             658 CALL                     1
#             666 CALL                     1
#             674 RAISE_VARARGS            1
#         >>  676 LOAD_CONST               0 (None)
#             678 COPY                     1
#             680 STORE_FAST               4 (@py_assert1)
#             682 COPY                     1
#             684 STORE_FAST               6 (@py_assert3)
#             686 STORE_FAST               5 (@py_assert5)
# 
# 122         688 LOAD_FAST                2 (api)
#             690 LOAD_ATTR               31 (NULL|self + disconnect)
#             710 CALL                     0
#             718 POP_TOP
#             720 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_get_waveforms at 0x3af994a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 124>:
# 124           0 RESUME                   0
# 
# 125           2 LOAD_GLOBAL              1 (NULL + MockEMTAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
# 126          22 LOAD_GLOBAL              3 (NULL + EMT)
#              32 LOAD_FAST                1 (adapter)
#              34 CALL                     1
#              42 STORE_FAST               2 (api)
# 
# 127          44 LOAD_GLOBAL              5 (NULL + SimulationResult)
# 
# 128          54 LOAD_CONST               1 ('test')
# 
# 129          56 LOAD_GLOBAL              6 (SimulationStatus)
#              66 LOAD_ATTR                8 (COMPLETED)
# 
# 130          86 LOAD_CONST               2 ('waveforms')
#              88 LOAD_CONST               3 (0)
#              90 LOAD_CONST               4 (1)
#              92 BUILD_LIST               2
#              94 LOAD_CONST               5 (1.0)
#              96 LOAD_CONST               6 (0.9)
#              98 BUILD_LIST               2
#             100 LOAD_CONST               7 (('time', 'voltage'))
#             102 BUILD_CONST_KEY_MAP      2
#             104 BUILD_LIST               1
#             106 BUILD_MAP                1
# 
# 127         108 KW_NAMES                 8 (('job_id', 'status', 'data'))
#             110 CALL                     3
#             118 STORE_FAST               3 (result)
# 
# 132         120 LOAD_FAST                2 (api)
#             122 LOAD_ATTR               11 (NULL|self + get_waveforms)
#             142 LOAD_FAST                3 (result)
#             144 CALL                     1
#             152 STORE_FAST               4 (waveforms)
# 
# 133         154 LOAD_GLOBAL             13 (NULL + len)
#             164 LOAD_FAST                4 (waveforms)
#             166 CALL                     1
#             174 STORE_FAST               5 (@py_assert2)
#             176 LOAD_CONST               4 (1)
#             178 STORE_FAST               6 (@py_assert5)
#             180 LOAD_FAST                5 (@py_assert2)
#             182 LOAD_FAST                6 (@py_assert5)
#             184 COMPARE_OP              40 (==)
#             188 STORE_FAST               7 (@py_assert4)
#             190 LOAD_FAST                7 (@py_assert4)
#             192 POP_JUMP_IF_TRUE       246 (to 686)
#             194 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             204 LOAD_ATTR               16 (_call_reprcompare)
#             224 LOAD_CONST               9 (('==',))
#             226 LOAD_FAST                7 (@py_assert4)
#             228 BUILD_TUPLE              1
#             230 LOAD_CONST              10 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             232 LOAD_FAST                5 (@py_assert2)
#             234 LOAD_FAST                6 (@py_assert5)
#             236 BUILD_TUPLE              2
#             238 CALL                     4
#             246 LOAD_CONST              11 ('len')
#             248 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             258 LOAD_ATTR               20 (locals)
#             278 CALL                     0
#             286 CONTAINS_OP              0
#             288 POP_JUMP_IF_TRUE        25 (to 340)
#             290 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             300 LOAD_ATTR               22 (_should_repr_global_name)
#             320 LOAD_GLOBAL             12 (len)
#             330 CALL                     1
#             338 POP_JUMP_IF_FALSE       25 (to 390)
#         >>  340 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             350 LOAD_ATTR               24 (_saferepr)
#             370 LOAD_GLOBAL             12 (len)
#             380 CALL                     1
#             388 JUMP_FORWARD             1 (to 392)
#         >>  390 LOAD_CONST              11 ('len')
#         >>  392 LOAD_CONST               2 ('waveforms')
#             394 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             404 LOAD_ATTR               20 (locals)
#             424 CALL                     0
#             432 CONTAINS_OP              0
#             434 POP_JUMP_IF_TRUE        21 (to 478)
#             436 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             446 LOAD_ATTR               22 (_should_repr_global_name)
#             466 LOAD_FAST                4 (waveforms)
#             468 CALL                     1
#             476 POP_JUMP_IF_FALSE       21 (to 520)
#         >>  478 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             488 LOAD_ATTR               24 (_saferepr)
#             508 LOAD_FAST                4 (waveforms)
#             510 CALL                     1
#             518 JUMP_FORWARD             1 (to 522)
#         >>  520 LOAD_CONST               2 ('waveforms')
#         >>  522 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             532 LOAD_ATTR               24 (_saferepr)
#             552 LOAD_FAST                5 (@py_assert2)
#             554 CALL                     1
#             562 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             572 LOAD_ATTR               24 (_saferepr)
#             592 LOAD_FAST                6 (@py_assert5)
#             594 CALL                     1
#             602 LOAD_CONST              12 (('py0', 'py1', 'py3', 'py6'))
#             604 BUILD_CONST_KEY_MAP      4
#             606 BINARY_OP                6 (%)
#             610 STORE_FAST               8 (@py_format7)
#             612 LOAD_CONST              13 ('assert %(py8)s')
#             614 LOAD_CONST              14 ('py8')
#             616 LOAD_FAST                8 (@py_format7)
#             618 BUILD_MAP                1
#             620 BINARY_OP                6 (%)
#             624 STORE_FAST               9 (@py_format9)
#             626 LOAD_GLOBAL             27 (NULL + AssertionError)
#             636 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             646 LOAD_ATTR               28 (_format_explanation)
#             666 LOAD_FAST                9 (@py_format9)
#             668 CALL                     1
#             676 CALL                     1
#             684 RAISE_VARARGS            1
#         >>  686 LOAD_CONST               0 (None)
#             688 COPY                     1
#             690 STORE_FAST               5 (@py_assert2)
#             692 COPY                     1
#             694 STORE_FAST               7 (@py_assert4)
#             696 STORE_FAST               6 (@py_assert5)
#             698 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_get_metadata at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 135>:
# 135           0 RESUME                   0
# 
# 136           2 LOAD_GLOBAL              1 (NULL + MockEMTAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
# 137          22 LOAD_GLOBAL              3 (NULL + EMT)
#              32 LOAD_FAST                1 (adapter)
#              34 CALL                     1
#              42 STORE_FAST               2 (api)
# 
# 138          44 LOAD_GLOBAL              5 (NULL + SimulationResult)
# 
# 139          54 LOAD_CONST               1 ('test')
# 
# 140          56 LOAD_GLOBAL              6 (SimulationStatus)
#              66 LOAD_ATTR                8 (COMPLETED)
# 
# 141          86 BUILD_MAP                0
# 
# 142          88 LOAD_CONST               2 (0.0001)
#              90 LOAD_CONST               3 (1.0)
#              92 LOAD_CONST               4 (('time_step', 'end_time'))
#              94 BUILD_CONST_KEY_MAP      2
# 
# 138          96 KW_NAMES                 5 (('job_id', 'status', 'data', 'metadata'))
#              98 CALL                     4
#             106 STORE_FAST               3 (result)
# 
# 144         108 LOAD_FAST                2 (api)
#             110 LOAD_ATTR               11 (NULL|self + get_metadata)
#             130 LOAD_FAST                3 (result)
#             132 CALL                     1
#             140 STORE_FAST               4 (meta)
# 
# 145         142 LOAD_FAST                4 (meta)
#             144 LOAD_CONST               6 ('time_step')
#             146 BINARY_SUBSCR
#             150 STORE_FAST               5 (@py_assert0)
#             152 LOAD_CONST               2 (0.0001)
#             154 STORE_FAST               6 (@py_assert3)
#             156 LOAD_FAST                5 (@py_assert0)
#             158 LOAD_FAST                6 (@py_assert3)
#             160 COMPARE_OP              40 (==)
#             164 STORE_FAST               7 (@py_assert2)
#             166 LOAD_FAST                7 (@py_assert2)
#             168 POP_JUMP_IF_TRUE       108 (to 386)
#             170 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             180 LOAD_ATTR               14 (_call_reprcompare)
#             200 LOAD_CONST               7 (('==',))
#             202 LOAD_FAST                7 (@py_assert2)
#             204 BUILD_TUPLE              1
#             206 LOAD_CONST               8 (('%(py1)s == %(py4)s',))
#             208 LOAD_FAST                5 (@py_assert0)
#             210 LOAD_FAST                6 (@py_assert3)
#             212 BUILD_TUPLE              2
#             214 CALL                     4
#             222 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             232 LOAD_ATTR               16 (_saferepr)
#             252 LOAD_FAST                5 (@py_assert0)
#             254 CALL                     1
#             262 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             272 LOAD_ATTR               16 (_saferepr)
#             292 LOAD_FAST                6 (@py_assert3)
#             294 CALL                     1
#             302 LOAD_CONST               9 (('py1', 'py4'))
#             304 BUILD_CONST_KEY_MAP      2
#             306 BINARY_OP                6 (%)
#             310 STORE_FAST               8 (@py_format5)
#             312 LOAD_CONST              10 ('assert %(py6)s')
#             314 LOAD_CONST              11 ('py6')
#             316 LOAD_FAST                8 (@py_format5)
#             318 BUILD_MAP                1
#             320 BINARY_OP                6 (%)
#             324 STORE_FAST               9 (@py_format7)
#             326 LOAD_GLOBAL             19 (NULL + AssertionError)
#             336 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             346 LOAD_ATTR               20 (_format_explanation)
#             366 LOAD_FAST                9 (@py_format7)
#             368 CALL                     1
#             376 CALL                     1
#             384 RAISE_VARARGS            1
#         >>  386 LOAD_CONST               0 (None)
#             388 COPY                     1
#             390 STORE_FAST               5 (@py_assert0)
#             392 COPY                     1
#             394 STORE_FAST               7 (@py_assert2)
#             396 STORE_FAST               6 (@py_assert3)
#             398 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestEngineNewMethods at 0x73cd93b064c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 148>:
# 148           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestEngineNewMethods')
#               8 STORE_NAME               2 (__qualname__)
# 
# 149          10 LOAD_CONST               1 ('Tests for new Engine methods.')
#              12 STORE_NAME               3 (__doc__)
# 
# 151          14 LOAD_CONST               2 (<code object test_create_short_circuit at 0x3af9a2d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 151>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_create_short_circuit)
# 
# 155          20 LOAD_CONST               3 (<code object test_create_emt at 0x3af9b9b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 155>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_create_emt)
# 
# 159          26 LOAD_CONST               4 (<code object test_list_engines_all_types at 0x3afa5a90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 159>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_list_engines_all_types)
#              32 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_create_short_circuit at 0x3af9a2d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 151>:
# 151           0 RESUME                   0
# 
# 152           2 LOAD_GLOBAL              1 (NULL + Engine)
#              12 LOAD_ATTR                2 (create_short_circuit)
#              32 LOAD_CONST               1 ('cloudpss')
#              34 KW_NAMES                 2 (('engine',))
#              36 CALL                     1
#              44 STORE_FAST               1 (api)
# 
# 153          46 LOAD_GLOBAL              5 (NULL + isinstance)
#              56 LOAD_FAST                1 (api)
#              58 LOAD_GLOBAL              6 (ShortCircuit)
#              68 CALL                     2
#              76 STORE_FAST               2 (@py_assert3)
#              78 LOAD_FAST                2 (@py_assert3)
#              80 EXTENDED_ARG             1
#              82 POP_JUMP_IF_TRUE       267 (to 618)
#              84 LOAD_CONST               3 ('assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}')
#              86 LOAD_CONST               4 ('isinstance')
#              88 LOAD_GLOBAL              9 (NULL + @py_builtins)
#              98 LOAD_ATTR               10 (locals)
#             118 CALL                     0
#             126 CONTAINS_OP              0
#             128 POP_JUMP_IF_TRUE        25 (to 180)
#             130 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             140 LOAD_ATTR               14 (_should_repr_global_name)
#             160 LOAD_GLOBAL              4 (isinstance)
#             170 CALL                     1
#             178 POP_JUMP_IF_FALSE       25 (to 230)
#         >>  180 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             190 LOAD_ATTR               16 (_saferepr)
#             210 LOAD_GLOBAL              4 (isinstance)
#             220 CALL                     1
#             228 JUMP_FORWARD             1 (to 232)
#         >>  230 LOAD_CONST               4 ('isinstance')
#         >>  232 LOAD_CONST               5 ('api')
#             234 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             244 LOAD_ATTR               10 (locals)
#             264 CALL                     0
#             272 CONTAINS_OP              0
#             274 POP_JUMP_IF_TRUE        21 (to 318)
#             276 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             286 LOAD_ATTR               14 (_should_repr_global_name)
#             306 LOAD_FAST                1 (api)
#             308 CALL                     1
#             316 POP_JUMP_IF_FALSE       21 (to 360)
#         >>  318 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             328 LOAD_ATTR               16 (_saferepr)
#             348 LOAD_FAST                1 (api)
#             350 CALL                     1
#             358 JUMP_FORWARD             1 (to 362)
#         >>  360 LOAD_CONST               5 ('api')
#         >>  362 LOAD_CONST               6 ('ShortCircuit')
#             364 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             374 LOAD_ATTR               10 (locals)
#             394 CALL                     0
#             402 CONTAINS_OP              0
#             404 POP_JUMP_IF_TRUE        25 (to 456)
#             406 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             416 LOAD_ATTR               14 (_should_repr_global_name)
#             436 LOAD_GLOBAL              6 (ShortCircuit)
#             446 CALL                     1
#             454 POP_JUMP_IF_FALSE       25 (to 506)
#         >>  456 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             466 LOAD_ATTR               16 (_saferepr)
#             486 LOAD_GLOBAL              6 (ShortCircuit)
#             496 CALL                     1
#             504 JUMP_FORWARD             1 (to 508)
#         >>  506 LOAD_CONST               6 ('ShortCircuit')
#         >>  508 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             518 LOAD_ATTR               16 (_saferepr)
#             538 LOAD_FAST                2 (@py_assert3)
#             540 CALL                     1
#             548 LOAD_CONST               7 (('py0', 'py1', 'py2', 'py4'))
#             550 BUILD_CONST_KEY_MAP      4
#             552 BINARY_OP                6 (%)
#             556 STORE_FAST               3 (@py_format5)
#             558 LOAD_GLOBAL             19 (NULL + AssertionError)
#             568 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             578 LOAD_ATTR               20 (_format_explanation)
#             598 LOAD_FAST                3 (@py_format5)
#             600 CALL                     1
#             608 CALL                     1
#             616 RAISE_VARARGS            1
#         >>  618 LOAD_CONST               0 (None)
#             620 STORE_FAST               2 (@py_assert3)
#             622 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_create_emt at 0x3af9b9b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 155>:
# 155           0 RESUME                   0
# 
# 156           2 LOAD_GLOBAL              1 (NULL + Engine)
#              12 LOAD_ATTR                2 (create_emt)
#              32 LOAD_CONST               1 ('cloudpss')
#              34 KW_NAMES                 2 (('engine',))
#              36 CALL                     1
#              44 STORE_FAST               1 (api)
# 
# 157          46 LOAD_GLOBAL              5 (NULL + isinstance)
#              56 LOAD_FAST                1 (api)
#              58 LOAD_GLOBAL              6 (EMT)
#              68 CALL                     2
#              76 STORE_FAST               2 (@py_assert3)
#              78 LOAD_FAST                2 (@py_assert3)
#              80 EXTENDED_ARG             1
#              82 POP_JUMP_IF_TRUE       267 (to 618)
#              84 LOAD_CONST               3 ('assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}')
#              86 LOAD_CONST               4 ('isinstance')
#              88 LOAD_GLOBAL              9 (NULL + @py_builtins)
#              98 LOAD_ATTR               10 (locals)
#             118 CALL                     0
#             126 CONTAINS_OP              0
#             128 POP_JUMP_IF_TRUE        25 (to 180)
#             130 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             140 LOAD_ATTR               14 (_should_repr_global_name)
#             160 LOAD_GLOBAL              4 (isinstance)
#             170 CALL                     1
#             178 POP_JUMP_IF_FALSE       25 (to 230)
#         >>  180 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             190 LOAD_ATTR               16 (_saferepr)
#             210 LOAD_GLOBAL              4 (isinstance)
#             220 CALL                     1
#             228 JUMP_FORWARD             1 (to 232)
#         >>  230 LOAD_CONST               4 ('isinstance')
#         >>  232 LOAD_CONST               5 ('api')
#             234 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             244 LOAD_ATTR               10 (locals)
#             264 CALL                     0
#             272 CONTAINS_OP              0
#             274 POP_JUMP_IF_TRUE        21 (to 318)
#             276 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             286 LOAD_ATTR               14 (_should_repr_global_name)
#             306 LOAD_FAST                1 (api)
#             308 CALL                     1
#             316 POP_JUMP_IF_FALSE       21 (to 360)
#         >>  318 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             328 LOAD_ATTR               16 (_saferepr)
#             348 LOAD_FAST                1 (api)
#             350 CALL                     1
#             358 JUMP_FORWARD             1 (to 362)
#         >>  360 LOAD_CONST               5 ('api')
#         >>  362 LOAD_CONST               6 ('EMT')
#             364 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             374 LOAD_ATTR               10 (locals)
#             394 CALL                     0
#             402 CONTAINS_OP              0
#             404 POP_JUMP_IF_TRUE        25 (to 456)
#             406 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             416 LOAD_ATTR               14 (_should_repr_global_name)
#             436 LOAD_GLOBAL              6 (EMT)
#             446 CALL                     1
#             454 POP_JUMP_IF_FALSE       25 (to 506)
#         >>  456 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             466 LOAD_ATTR               16 (_saferepr)
#             486 LOAD_GLOBAL              6 (EMT)
#             496 CALL                     1
#             504 JUMP_FORWARD             1 (to 508)
#         >>  506 LOAD_CONST               6 ('EMT')
#         >>  508 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             518 LOAD_ATTR               16 (_saferepr)
#             538 LOAD_FAST                2 (@py_assert3)
#             540 CALL                     1
#             548 LOAD_CONST               7 (('py0', 'py1', 'py2', 'py4'))
#             550 BUILD_CONST_KEY_MAP      4
#             552 BINARY_OP                6 (%)
#             556 STORE_FAST               3 (@py_format5)
#             558 LOAD_GLOBAL             19 (NULL + AssertionError)
#             568 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             578 LOAD_ATTR               20 (_format_explanation)
#             598 LOAD_FAST                3 (@py_format5)
#             600 CALL                     1
#             608 CALL                     1
#             616 RAISE_VARARGS            1
#         >>  618 LOAD_CONST               0 (None)
#             620 STORE_FAST               2 (@py_assert3)
#             622 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_list_engines_all_types at 0x3afa5a90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py", line 159>:
# 159           0 RESUME                   0
# 
# 160           2 LOAD_GLOBAL              1 (NULL + Engine)
#              12 LOAD_ATTR                2 (list_engines)
#              32 LOAD_CONST               1 ('power_flow')
#              34 CALL                     1
#              42 STORE_FAST               1 (pf_engines)
# 
# 161          44 LOAD_GLOBAL              1 (NULL + Engine)
#              54 LOAD_ATTR                2 (list_engines)
#              74 LOAD_CONST               2 ('short_circuit')
#              76 CALL                     1
#              84 STORE_FAST               2 (sc_engines)
# 
# 162          86 LOAD_GLOBAL              1 (NULL + Engine)
#              96 LOAD_ATTR                2 (list_engines)
#             116 LOAD_CONST               3 ('emt')
#             118 CALL                     1
#             126 STORE_FAST               3 (emt_engines)
# 
# 163         128 LOAD_CONST               4 ('cloudpss')
#             130 STORE_FAST               4 (@py_assert0)
#             132 LOAD_FAST                4 (@py_assert0)
#             134 LOAD_FAST                1 (pf_engines)
#             136 CONTAINS_OP              0
#             138 STORE_FAST               5 (@py_assert2)
#             140 LOAD_FAST                5 (@py_assert2)
#             142 POP_JUMP_IF_TRUE       153 (to 450)
#             144 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             154 LOAD_ATTR                6 (_call_reprcompare)
#             174 LOAD_CONST               5 (('in',))
#             176 LOAD_FAST                5 (@py_assert2)
#             178 BUILD_TUPLE              1
#             180 LOAD_CONST               6 (('%(py1)s in %(py3)s',))
#             182 LOAD_FAST                4 (@py_assert0)
#             184 LOAD_FAST                1 (pf_engines)
#             186 BUILD_TUPLE              2
#             188 CALL                     4
#             196 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             206 LOAD_ATTR                8 (_saferepr)
#             226 LOAD_FAST                4 (@py_assert0)
#             228 CALL                     1
#             236 LOAD_CONST               7 ('pf_engines')
#             238 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             248 LOAD_ATTR               12 (locals)
#             268 CALL                     0
#             276 CONTAINS_OP              0
#             278 POP_JUMP_IF_TRUE        21 (to 322)
#             280 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             290 LOAD_ATTR               14 (_should_repr_global_name)
#             310 LOAD_FAST                1 (pf_engines)
#             312 CALL                     1
#             320 POP_JUMP_IF_FALSE       21 (to 364)
#         >>  322 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             332 LOAD_ATTR                8 (_saferepr)
#             352 LOAD_FAST                1 (pf_engines)
#             354 CALL                     1
#             362 JUMP_FORWARD             1 (to 366)
#         >>  364 LOAD_CONST               7 ('pf_engines')
#         >>  366 LOAD_CONST               8 (('py1', 'py3'))
#             368 BUILD_CONST_KEY_MAP      2
#             370 BINARY_OP                6 (%)
#             374 STORE_FAST               6 (@py_format4)
#             376 LOAD_CONST               9 ('assert %(py5)s')
#             378 LOAD_CONST              10 ('py5')
#             380 LOAD_FAST                6 (@py_format4)
#             382 BUILD_MAP                1
#             384 BINARY_OP                6 (%)
#             388 STORE_FAST               7 (@py_format6)
#             390 LOAD_GLOBAL             17 (NULL + AssertionError)
#             400 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             410 LOAD_ATTR               18 (_format_explanation)
#             430 LOAD_FAST                7 (@py_format6)
#             432 CALL                     1
#             440 CALL                     1
#             448 RAISE_VARARGS            1
#         >>  450 LOAD_CONST               0 (None)
#             452 COPY                     1
#             454 STORE_FAST               4 (@py_assert0)
#             456 STORE_FAST               5 (@py_assert2)
# 
# 164         458 LOAD_CONST               4 ('cloudpss')
#             460 STORE_FAST               4 (@py_assert0)
#             462 LOAD_FAST                4 (@py_assert0)
#             464 LOAD_FAST                2 (sc_engines)
#             466 CONTAINS_OP              0
#             468 STORE_FAST               5 (@py_assert2)
#             470 LOAD_FAST                5 (@py_assert2)
#             472 POP_JUMP_IF_TRUE       153 (to 780)
#             474 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             484 LOAD_ATTR                6 (_call_reprcompare)
#             504 LOAD_CONST               5 (('in',))
#             506 LOAD_FAST                5 (@py_assert2)
#             508 BUILD_TUPLE              1
#             510 LOAD_CONST               6 (('%(py1)s in %(py3)s',))
#             512 LOAD_FAST                4 (@py_assert0)
#             514 LOAD_FAST                2 (sc_engines)
#             516 BUILD_TUPLE              2
#             518 CALL                     4
#             526 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             536 LOAD_ATTR                8 (_saferepr)
#             556 LOAD_FAST                4 (@py_assert0)
#             558 CALL                     1
#             566 LOAD_CONST              11 ('sc_engines')
#             568 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             578 LOAD_ATTR               12 (locals)
#             598 CALL                     0
#             606 CONTAINS_OP              0
#             608 POP_JUMP_IF_TRUE        21 (to 652)
#             610 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             620 LOAD_ATTR               14 (_should_repr_global_name)
#             640 LOAD_FAST                2 (sc_engines)
#             642 CALL                     1
#             650 POP_JUMP_IF_FALSE       21 (to 694)
#         >>  652 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             662 LOAD_ATTR                8 (_saferepr)
#             682 LOAD_FAST                2 (sc_engines)
#             684 CALL                     1
#             692 JUMP_FORWARD             1 (to 696)
#         >>  694 LOAD_CONST              11 ('sc_engines')
#         >>  696 LOAD_CONST               8 (('py1', 'py3'))
#             698 BUILD_CONST_KEY_MAP      2
#             700 BINARY_OP                6 (%)
#             704 STORE_FAST               6 (@py_format4)
#             706 LOAD_CONST               9 ('assert %(py5)s')
#             708 LOAD_CONST              10 ('py5')
#             710 LOAD_FAST                6 (@py_format4)
#             712 BUILD_MAP                1
#             714 BINARY_OP                6 (%)
#             718 STORE_FAST               7 (@py_format6)
#             720 LOAD_GLOBAL             17 (NULL + AssertionError)
#             730 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             740 LOAD_ATTR               18 (_format_explanation)
#             760 LOAD_FAST                7 (@py_format6)
#             762 CALL                     1
#             770 CALL                     1
#             778 RAISE_VARARGS            1
#         >>  780 LOAD_CONST               0 (None)
#             782 COPY                     1
#             784 STORE_FAST               4 (@py_assert0)
#             786 STORE_FAST               5 (@py_assert2)
# 
# 165         788 LOAD_CONST               4 ('cloudpss')
#             790 STORE_FAST               4 (@py_assert0)
#             792 LOAD_FAST                4 (@py_assert0)
#             794 LOAD_FAST                3 (emt_engines)
#             796 CONTAINS_OP              0
#             798 STORE_FAST               5 (@py_assert2)
#             800 LOAD_FAST                5 (@py_assert2)
#             802 POP_JUMP_IF_TRUE       153 (to 1110)
#             804 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             814 LOAD_ATTR                6 (_call_reprcompare)
#             834 LOAD_CONST               5 (('in',))
#             836 LOAD_FAST                5 (@py_assert2)
#             838 BUILD_TUPLE              1
#             840 LOAD_CONST               6 (('%(py1)s in %(py3)s',))
#             842 LOAD_FAST                4 (@py_assert0)
#             844 LOAD_FAST                3 (emt_engines)
#             846 BUILD_TUPLE              2
#             848 CALL                     4
#             856 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             866 LOAD_ATTR                8 (_saferepr)
#             886 LOAD_FAST                4 (@py_assert0)
#             888 CALL                     1
#             896 LOAD_CONST              12 ('emt_engines')
#             898 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             908 LOAD_ATTR               12 (locals)
#             928 CALL                     0
#             936 CONTAINS_OP              0
#             938 POP_JUMP_IF_TRUE        21 (to 982)
#             940 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             950 LOAD_ATTR               14 (_should_repr_global_name)
#             970 LOAD_FAST                3 (emt_engines)
#             972 CALL                     1
#             980 POP_JUMP_IF_FALSE       21 (to 1024)
#         >>  982 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             992 LOAD_ATTR                8 (_saferepr)
#            1012 LOAD_FAST                3 (emt_engines)
#            1014 CALL                     1
#            1022 JUMP_FORWARD             1 (to 1026)
#         >> 1024 LOAD_CONST              12 ('emt_engines')
#         >> 1026 LOAD_CONST               8 (('py1', 'py3'))
#            1028 BUILD_CONST_KEY_MAP      2
#            1030 BINARY_OP                6 (%)
#            1034 STORE_FAST               6 (@py_format4)
#            1036 LOAD_CONST               9 ('assert %(py5)s')
#            1038 LOAD_CONST              10 ('py5')
#            1040 LOAD_FAST                6 (@py_format4)
#            1042 BUILD_MAP                1
#            1044 BINARY_OP                6 (%)
#            1048 STORE_FAST               7 (@py_format6)
#            1050 LOAD_GLOBAL             17 (NULL + AssertionError)
#            1060 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1070 LOAD_ATTR               18 (_format_explanation)
#            1090 LOAD_FAST                7 (@py_format6)
#            1092 CALL                     1
#            1100 CALL                     1
#            1108 RAISE_VARARGS            1
#         >> 1110 LOAD_CONST               0 (None)
#            1112 COPY                     1
#            1114 STORE_FAST               4 (@py_assert0)
#            1116 STORE_FAST               5 (@py_assert2)
#            1118 RETURN_CONST             0 (None)
# 