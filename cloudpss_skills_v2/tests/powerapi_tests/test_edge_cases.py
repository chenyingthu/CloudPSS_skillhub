# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/__pycache__/test_edge_cases.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


class TimeoutAdapter:
    """TimeoutAdapter"""
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


class ErrorAdapter:
    """ErrorAdapter"""
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


def TestTimeoutHandling():
    """TestTimeoutHandling"""
pass  # TODO: restore


def TestErrorHandling():
    """TestErrorHandling"""
pass  # TODO: restore


def TestValidationEdgeCases():
    """TestValidationEdgeCases"""
pass  # TODO: restore


def TestSimulationResultEdgeCases():
    """TestSimulationResultEdgeCases"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('Edge case tests for powerAPI/powerskill architecture.')
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
#              42 LOAD_CONST               3 (('SimulationStatus', 'SimulationResult', 'ValidationResult', 'ValidationError', 'EngineAdapter', 'EngineConfig'))
#              44 IMPORT_NAME              8 (cloudpss_skills_v2.powerapi)
#              46 IMPORT_FROM              9 (SimulationStatus)
#              48 STORE_NAME               9 (SimulationStatus)
#              50 IMPORT_FROM             10 (SimulationResult)
#              52 STORE_NAME              10 (SimulationResult)
#              54 IMPORT_FROM             11 (ValidationResult)
#              56 STORE_NAME              11 (ValidationResult)
#              58 IMPORT_FROM             12 (ValidationError)
#              60 STORE_NAME              12 (ValidationError)
#              62 IMPORT_FROM             13 (EngineAdapter)
#              64 STORE_NAME              13 (EngineAdapter)
#              66 IMPORT_FROM             14 (EngineConfig)
#              68 STORE_NAME              14 (EngineConfig)
#              70 POP_TOP
# 
#  12          72 LOAD_CONST               1 (0)
#              74 LOAD_CONST               4 (('APIFactory',))
#              76 IMPORT_NAME             15 (cloudpss_skills_v2.powerskill)
#              78 IMPORT_FROM             16 (APIFactory)
#              80 STORE_NAME              16 (APIFactory)
#              82 POP_TOP
# 
#  15          84 PUSH_NULL
#              86 LOAD_BUILD_CLASS
#              88 LOAD_CONST               5 (<code object TimeoutAdapter at 0x73cd93b39c50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 15>)
#              90 MAKE_FUNCTION            0
#              92 LOAD_CONST               6 ('TimeoutAdapter')
#              94 LOAD_NAME               13 (EngineAdapter)
#              96 CALL                     3
#             104 STORE_NAME              17 (TimeoutAdapter)
# 
#  48         106 PUSH_NULL
#             108 LOAD_BUILD_CLASS
#             110 LOAD_CONST               7 (<code object ErrorAdapter at 0x73cd93b398f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 48>)
#             112 MAKE_FUNCTION            0
#             114 LOAD_CONST               8 ('ErrorAdapter')
#             116 LOAD_NAME               13 (EngineAdapter)
#             118 CALL                     3
#             126 STORE_NAME              18 (ErrorAdapter)
# 
#  85         128 PUSH_NULL
#             130 LOAD_BUILD_CLASS
#             132 LOAD_CONST               9 (<code object TestTimeoutHandling at 0x73cd945fe250, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 85>)
#             134 MAKE_FUNCTION            0
#             136 LOAD_CONST              10 ('TestTimeoutHandling')
#             138 CALL                     2
#             146 STORE_NAME              19 (TestTimeoutHandling)
# 
# 104         148 PUSH_NULL
#             150 LOAD_BUILD_CLASS
#             152 LOAD_CONST              11 (<code object TestErrorHandling at 0x73cd93b066a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 104>)
#             154 MAKE_FUNCTION            0
#             156 LOAD_CONST              12 ('TestErrorHandling')
#             158 CALL                     2
#             166 STORE_NAME              20 (TestErrorHandling)
# 
# 130         168 PUSH_NULL
#             170 LOAD_BUILD_CLASS
#             172 LOAD_CONST              13 (<code object TestValidationEdgeCases at 0x73cd945fdfb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 130>)
#             174 MAKE_FUNCTION            0
#             176 LOAD_CONST              14 ('TestValidationEdgeCases')
#             178 CALL                     2
#             186 STORE_NAME              21 (TestValidationEdgeCases)
# 
# 153         188 PUSH_NULL
#             190 LOAD_BUILD_CLASS
#             192 LOAD_CONST              15 (<code object TestSimulationResultEdgeCases at 0x73cd93b065b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 153>)
#             194 MAKE_FUNCTION            0
#             196 LOAD_CONST              16 ('TestSimulationResultEdgeCases')
#             198 CALL                     2
#             206 STORE_NAME              22 (TestSimulationResultEdgeCases)
#             208 RETURN_CONST             2 (None)
# 
# Disassembly of <code object TimeoutAdapter at 0x73cd93b39c50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 15>:
#               0 MAKE_CELL                0 (__class__)
# 
#  15           2 RESUME                   0
#               4 LOAD_NAME                0 (__name__)
#               6 STORE_NAME               1 (__module__)
#               8 LOAD_CONST               0 ('TimeoutAdapter')
#              10 STORE_NAME               2 (__qualname__)
# 
#  16          12 LOAD_CONST               1 ('Adapter that simulates timeout.')
#              14 STORE_NAME               3 (__doc__)
# 
#  18          16 LOAD_CLOSURE             0 (__class__)
#              18 BUILD_TUPLE              1
#              20 LOAD_CONST               2 (<code object __init__ at 0x73cd93b31830, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 18>)
#              22 MAKE_FUNCTION            8 (closure)
#              24 STORE_NAME               4 (__init__)
# 
#  21          26 LOAD_NAME                5 (property)
# 
#  22          28 LOAD_CONST               3 (<code object engine_name at 0x73cd93b13290, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 21>)
#              30 MAKE_FUNCTION            0
# 
#  21          32 CALL                     0
# 
#  22          40 STORE_NAME               6 (engine_name)
# 
#  25          42 LOAD_CONST               4 (<code object _do_connect at 0x73cd93b13360, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 25>)
#              44 MAKE_FUNCTION            0
#              46 STORE_NAME               7 (_do_connect)
# 
#  28          48 LOAD_CONST               5 (<code object _do_disconnect at 0x73cd93b13500, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 28>)
#              50 MAKE_FUNCTION            0
#              52 STORE_NAME               8 (_do_disconnect)
# 
#  31          54 LOAD_CONST               6 (<code object _do_load_model at 0x73cd93b131c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 31>)
#              56 MAKE_FUNCTION            0
#              58 STORE_NAME               9 (_do_load_model)
# 
#  34          60 LOAD_CONST               7 (<code object _do_run_simulation at 0x73cd93b31330, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 34>)
#              62 MAKE_FUNCTION            0
#              64 STORE_NAME              10 (_do_run_simulation)
# 
#  41          66 LOAD_CONST               8 (<code object _do_get_result at 0x73cd93b31630, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 41>)
#              68 MAKE_FUNCTION            0
#              70 STORE_NAME              11 (_do_get_result)
# 
#  44          72 LOAD_CONST               9 (<code object _do_validate_config at 0x73cd945fc110, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 44>)
#              74 MAKE_FUNCTION            0
#              76 STORE_NAME              12 (_do_validate_config)
#              78 LOAD_CLOSURE             0 (__class__)
#              80 COPY                     1
#              82 STORE_NAME              13 (__classcell__)
#              84 RETURN_VALUE
# 
# Disassembly of <code object __init__ at 0x73cd93b31830, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 18>:
#               0 COPY_FREE_VARS           1
# 
#  18           2 RESUME                   0
# 
#  19           4 LOAD_GLOBAL              0 (super)
#              14 LOAD_DEREF               1 (__class__)
#              16 LOAD_FAST                0 (self)
#              18 LOAD_SUPER_ATTR          5 (NULL|self + __init__)
#              22 LOAD_GLOBAL              5 (NULL + EngineConfig)
#              32 LOAD_CONST               1 ('timeout')
#              34 KW_NAMES                 2 (('engine_name',))
#              36 CALL                     1
#              44 CALL                     1
#              52 POP_TOP
#              54 RETURN_CONST             0 (None)
# 
# Disassembly of <code object engine_name at 0x73cd93b13290, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 21>:
#  21           0 RESUME                   0
# 
#  23           2 RETURN_CONST             1 ('timeout')
# 
# Disassembly of <code object _do_connect at 0x73cd93b13360, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 25>:
#  25           0 RESUME                   0
# 
#  26           2 RETURN_CONST             0 (None)
# 
# Disassembly of <code object _do_disconnect at 0x73cd93b13500, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 28>:
#  28           0 RESUME                   0
# 
#  29           2 RETURN_CONST             0 (None)
# 
# Disassembly of <code object _do_load_model at 0x73cd93b131c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 31>:
#  31           0 RESUME                   0
# 
#  32           2 RETURN_CONST             1 (True)
# 
# Disassembly of <code object _do_run_simulation at 0x73cd93b31330, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 34>:
#  34           0 RESUME                   0
# 
#  35           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
#  36          12 LOAD_CONST               1 ('timeout-job')
# 
#  37          14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (TIMEOUT)
# 
#  38          44 LOAD_CONST               2 ('Simulation timed out after 300s')
#              46 BUILD_LIST               1
# 
#  35          48 KW_NAMES                 3 (('job_id', 'status', 'errors'))
#              50 CALL                     3
#              58 RETURN_VALUE
# 
# Disassembly of <code object _do_get_result at 0x73cd93b31630, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 41>:
#  41           0 RESUME                   0
# 
#  42           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
#              12 LOAD_FAST                1 (job_id)
#              14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (TIMEOUT)
#              44 KW_NAMES                 1 (('job_id', 'status'))
#              46 CALL                     2
#              54 RETURN_VALUE
# 
# Disassembly of <code object _do_validate_config at 0x73cd945fc110, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 44>:
#  44           0 RESUME                   0
# 
#  45           2 LOAD_GLOBAL              1 (NULL + ValidationResult)
#              12 LOAD_CONST               1 (True)
#              14 KW_NAMES                 2 (('valid',))
#              16 CALL                     1
#              24 RETURN_VALUE
# 
# Disassembly of <code object ErrorAdapter at 0x73cd93b398f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 48>:
#               0 MAKE_CELL                0 (__class__)
# 
#  48           2 RESUME                   0
#               4 LOAD_NAME                0 (__name__)
#               6 STORE_NAME               1 (__module__)
#               8 LOAD_CONST               0 ('ErrorAdapter')
#              10 STORE_NAME               2 (__qualname__)
# 
#  49          12 LOAD_CONST               1 ('Adapter that simulates errors.')
#              14 STORE_NAME               3 (__doc__)
# 
#  51          16 LOAD_CLOSURE             0 (__class__)
#              18 BUILD_TUPLE              1
#              20 LOAD_CONST               2 (<code object __init__ at 0x73cd93b31730, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 51>)
#              22 MAKE_FUNCTION            8 (closure)
#              24 STORE_NAME               4 (__init__)
# 
#  54          26 LOAD_NAME                5 (property)
# 
#  55          28 LOAD_CONST               3 (<code object engine_name at 0x73cd93b130f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 54>)
#              30 MAKE_FUNCTION            0
# 
#  54          32 CALL                     0
# 
#  55          40 STORE_NAME               6 (engine_name)
# 
#  58          42 LOAD_CONST               4 (<code object _do_connect at 0x73cd93b135d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 58>)
#              44 MAKE_FUNCTION            0
#              46 STORE_NAME               7 (_do_connect)
# 
#  61          48 LOAD_CONST               5 (<code object _do_disconnect at 0x73cd93b136a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 61>)
#              50 MAKE_FUNCTION            0
#              52 STORE_NAME               8 (_do_disconnect)
# 
#  64          54 LOAD_CONST               6 (<code object _do_load_model at 0x73cd93b13770, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 64>)
#              56 MAKE_FUNCTION            0
#              58 STORE_NAME               9 (_do_load_model)
# 
#  67          60 LOAD_CONST               7 (<code object _do_run_simulation at 0x73cd93b31230, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 67>)
#              62 MAKE_FUNCTION            0
#              64 STORE_NAME              10 (_do_run_simulation)
# 
#  74          66 LOAD_CONST               8 (<code object _do_get_result at 0x73cd93b31a30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 74>)
#              68 MAKE_FUNCTION            0
#              70 STORE_NAME              11 (_do_get_result)
# 
#  77          72 LOAD_CONST               9 (<code object _do_validate_config at 0x73cd945b92f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 77>)
#              74 MAKE_FUNCTION            0
#              76 STORE_NAME              12 (_do_validate_config)
#              78 LOAD_CLOSURE             0 (__class__)
#              80 COPY                     1
#              82 STORE_NAME              13 (__classcell__)
#              84 RETURN_VALUE
# 
# Disassembly of <code object __init__ at 0x73cd93b31730, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 51>:
#               0 COPY_FREE_VARS           1
# 
#  51           2 RESUME                   0
# 
#  52           4 LOAD_GLOBAL              0 (super)
#              14 LOAD_DEREF               1 (__class__)
#              16 LOAD_FAST                0 (self)
#              18 LOAD_SUPER_ATTR          5 (NULL|self + __init__)
#              22 LOAD_GLOBAL              5 (NULL + EngineConfig)
#              32 LOAD_CONST               1 ('error')
#              34 KW_NAMES                 2 (('engine_name',))
#              36 CALL                     1
#              44 CALL                     1
#              52 POP_TOP
#              54 RETURN_CONST             0 (None)
# 
# Disassembly of <code object engine_name at 0x73cd93b130f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 54>:
#  54           0 RESUME                   0
# 
#  56           2 RETURN_CONST             1 ('error')
# 
# Disassembly of <code object _do_connect at 0x73cd93b135d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 58>:
#  58           0 RESUME                   0
# 
#  59           2 RETURN_CONST             0 (None)
# 
# Disassembly of <code object _do_disconnect at 0x73cd93b136a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 61>:
#  61           0 RESUME                   0
# 
#  62           2 RETURN_CONST             0 (None)
# 
# Disassembly of <code object _do_load_model at 0x73cd93b13770, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 64>:
#  64           0 RESUME                   0
# 
#  65           2 RETURN_CONST             1 (True)
# 
# Disassembly of <code object _do_run_simulation at 0x73cd93b31230, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 67>:
#  67           0 RESUME                   0
# 
#  68           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
#  69          12 LOAD_CONST               1 ('error-job')
# 
#  70          14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (FAILED)
# 
#  71          44 LOAD_CONST               2 ('Invalid model configuration')
#              46 BUILD_LIST               1
# 
#  68          48 KW_NAMES                 3 (('job_id', 'status', 'errors'))
#              50 CALL                     3
#              58 RETURN_VALUE
# 
# Disassembly of <code object _do_get_result at 0x73cd93b31a30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 74>:
#  74           0 RESUME                   0
# 
#  75           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
#              12 LOAD_FAST                1 (job_id)
#              14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (FAILED)
#              44 KW_NAMES                 1 (('job_id', 'status'))
#              46 CALL                     2
#              54 RETURN_VALUE
# 
# Disassembly of <code object _do_validate_config at 0x73cd945b92f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 77>:
#  77           0 RESUME                   0
# 
#  78           2 LOAD_FAST                1 (config)
#               4 LOAD_ATTR                1 (NULL|self + get)
#              24 LOAD_CONST               1 ('invalid')
#              26 CALL                     1
#              34 POP_JUMP_IF_FALSE       33 (to 102)
# 
#  79          36 LOAD_GLOBAL              3 (NULL + ValidationResult)
#              46 LOAD_ATTR                4 (failure)
# 
#  80          66 LOAD_GLOBAL              7 (NULL + ValidationError)
#              76 LOAD_CONST               1 ('invalid')
#              78 LOAD_CONST               2 ('Config is invalid')
#              80 KW_NAMES                 3 (('field', 'message'))
#              82 CALL                     2
#              90 BUILD_LIST               1
# 
#  79          92 CALL                     1
#             100 RETURN_VALUE
# 
#  82     >>  102 LOAD_GLOBAL              3 (NULL + ValidationResult)
#             112 LOAD_CONST               4 (True)
#             114 KW_NAMES                 5 (('valid',))
#             116 CALL                     1
#             124 RETURN_VALUE
# 
# Disassembly of <code object TestTimeoutHandling at 0x73cd945fe250, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 85>:
#  85           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestTimeoutHandling')
#               8 STORE_NAME               2 (__qualname__)
# 
#  86          10 LOAD_CONST               1 ('Tests for timeout handling.')
#              12 STORE_NAME               3 (__doc__)
# 
#  88          14 LOAD_CONST               2 (<code object test_timeout_result at 0x3af9c1f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 88>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_timeout_result)
# 
#  96          20 LOAD_CONST               3 (<code object test_is_success_false_on_timeout at 0x3aeff050, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 96>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_is_success_false_on_timeout)
#              26 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_timeout_result at 0x3af9c1f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 88>:
#  88           0 RESUME                   0
# 
#  89           2 LOAD_GLOBAL              1 (NULL + TimeoutAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
#  90          22 LOAD_FAST                1 (adapter)
#              24 LOAD_ATTR                3 (NULL|self + connect)
#              44 CALL                     0
#              52 POP_TOP
# 
#  91          54 LOAD_FAST                1 (adapter)
#              56 LOAD_ATTR                5 (NULL|self + run_simulation)
#              76 BUILD_MAP                0
#              78 CALL                     1
#              86 STORE_FAST               2 (result)
# 
#  92          88 LOAD_FAST                2 (result)
#              90 LOAD_ATTR                6 (status)
#             110 STORE_FAST               3 (@py_assert1)
#             112 LOAD_GLOBAL              8 (SimulationStatus)
#             122 LOAD_ATTR               10 (TIMEOUT)
#             142 STORE_FAST               4 (@py_assert5)
#             144 LOAD_FAST                3 (@py_assert1)
#             146 LOAD_FAST                4 (@py_assert5)
#             148 COMPARE_OP              40 (==)
#             152 STORE_FAST               5 (@py_assert3)
#             154 LOAD_FAST                5 (@py_assert3)
#             156 POP_JUMP_IF_TRUE       246 (to 650)
#             158 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             168 LOAD_ATTR               14 (_call_reprcompare)
#             188 LOAD_CONST               1 (('==',))
#             190 LOAD_FAST                5 (@py_assert3)
#             192 BUILD_TUPLE              1
#             194 LOAD_CONST               2 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.TIMEOUT\n}',))
#             196 LOAD_FAST                3 (@py_assert1)
#             198 LOAD_FAST                4 (@py_assert5)
#             200 BUILD_TUPLE              2
#             202 CALL                     4
#             210 LOAD_CONST               3 ('result')
#             212 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             222 LOAD_ATTR               18 (locals)
#             242 CALL                     0
#             250 CONTAINS_OP              0
#             252 POP_JUMP_IF_TRUE        21 (to 296)
#             254 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             264 LOAD_ATTR               20 (_should_repr_global_name)
#             284 LOAD_FAST                2 (result)
#             286 CALL                     1
#             294 POP_JUMP_IF_FALSE       21 (to 338)
#         >>  296 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             306 LOAD_ATTR               22 (_saferepr)
#             326 LOAD_FAST                2 (result)
#             328 CALL                     1
#             336 JUMP_FORWARD             1 (to 340)
#         >>  338 LOAD_CONST               3 ('result')
#         >>  340 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             350 LOAD_ATTR               22 (_saferepr)
#             370 LOAD_FAST                3 (@py_assert1)
#             372 CALL                     1
#             380 LOAD_CONST               4 ('SimulationStatus')
#             382 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             392 LOAD_ATTR               18 (locals)
#             412 CALL                     0
#             420 CONTAINS_OP              0
#             422 POP_JUMP_IF_TRUE        25 (to 474)
#             424 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             434 LOAD_ATTR               20 (_should_repr_global_name)
#             454 LOAD_GLOBAL              8 (SimulationStatus)
#             464 CALL                     1
#             472 POP_JUMP_IF_FALSE       25 (to 524)
#         >>  474 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             484 LOAD_ATTR               22 (_saferepr)
#             504 LOAD_GLOBAL              8 (SimulationStatus)
#             514 CALL                     1
#             522 JUMP_FORWARD             1 (to 526)
#         >>  524 LOAD_CONST               4 ('SimulationStatus')
#         >>  526 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             536 LOAD_ATTR               22 (_saferepr)
#             556 LOAD_FAST                4 (@py_assert5)
#             558 CALL                     1
#             566 LOAD_CONST               5 (('py0', 'py2', 'py4', 'py6'))
#             568 BUILD_CONST_KEY_MAP      4
#             570 BINARY_OP                6 (%)
#             574 STORE_FAST               6 (@py_format7)
#             576 LOAD_CONST               6 ('assert %(py8)s')
#             578 LOAD_CONST               7 ('py8')
#             580 LOAD_FAST                6 (@py_format7)
#             582 BUILD_MAP                1
#             584 BINARY_OP                6 (%)
#             588 STORE_FAST               7 (@py_format9)
#             590 LOAD_GLOBAL             25 (NULL + AssertionError)
#             600 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             610 LOAD_ATTR               26 (_format_explanation)
#             630 LOAD_FAST                7 (@py_format9)
#             632 CALL                     1
#             640 CALL                     1
#             648 RAISE_VARARGS            1
#         >>  650 LOAD_CONST               0 (None)
#             652 COPY                     1
#             654 STORE_FAST               3 (@py_assert1)
#             656 COPY                     1
#             658 STORE_FAST               5 (@py_assert3)
#             660 STORE_FAST               4 (@py_assert5)
# 
#  93         662 LOAD_FAST                2 (result)
#             664 LOAD_ATTR               28 (errors)
#             684 STORE_FAST               8 (@py_assert2)
#             686 LOAD_GLOBAL             31 (NULL + len)
#             696 LOAD_FAST                8 (@py_assert2)
#             698 CALL                     1
#             706 STORE_FAST               9 (@py_assert4)
#             708 LOAD_CONST               8 (0)
#             710 STORE_FAST              10 (@py_assert7)
#             712 LOAD_FAST                9 (@py_assert4)
#             714 LOAD_FAST               10 (@py_assert7)
#             716 COMPARE_OP              68 (>)
#             720 STORE_FAST              11 (@py_assert6)
#             722 LOAD_FAST               11 (@py_assert6)
#             724 EXTENDED_ARG             1
#             726 POP_JUMP_IF_TRUE       266 (to 1260)
#             728 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             738 LOAD_ATTR               14 (_call_reprcompare)
#             758 LOAD_CONST               9 (('>',))
#             760 LOAD_FAST               11 (@py_assert6)
#             762 BUILD_TUPLE              1
#             764 LOAD_CONST              10 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.errors\n})\n} > %(py8)s',))
#             766 LOAD_FAST                9 (@py_assert4)
#             768 LOAD_FAST               10 (@py_assert7)
#             770 BUILD_TUPLE              2
#             772 CALL                     4
#             780 LOAD_CONST              11 ('len')
#             782 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             792 LOAD_ATTR               18 (locals)
#             812 CALL                     0
#             820 CONTAINS_OP              0
#             822 POP_JUMP_IF_TRUE        25 (to 874)
#             824 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             834 LOAD_ATTR               20 (_should_repr_global_name)
#             854 LOAD_GLOBAL             30 (len)
#             864 CALL                     1
#             872 POP_JUMP_IF_FALSE       25 (to 924)
#         >>  874 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             884 LOAD_ATTR               22 (_saferepr)
#             904 LOAD_GLOBAL             30 (len)
#             914 CALL                     1
#             922 JUMP_FORWARD             1 (to 926)
#         >>  924 LOAD_CONST              11 ('len')
#         >>  926 LOAD_CONST               3 ('result')
#             928 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             938 LOAD_ATTR               18 (locals)
#             958 CALL                     0
#             966 CONTAINS_OP              0
#             968 POP_JUMP_IF_TRUE        21 (to 1012)
#             970 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             980 LOAD_ATTR               20 (_should_repr_global_name)
#            1000 LOAD_FAST                2 (result)
#            1002 CALL                     1
#            1010 POP_JUMP_IF_FALSE       21 (to 1054)
#         >> 1012 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1022 LOAD_ATTR               22 (_saferepr)
#            1042 LOAD_FAST                2 (result)
#            1044 CALL                     1
#            1052 JUMP_FORWARD             1 (to 1056)
#         >> 1054 LOAD_CONST               3 ('result')
#         >> 1056 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1066 LOAD_ATTR               22 (_saferepr)
#            1086 LOAD_FAST                8 (@py_assert2)
#            1088 CALL                     1
#            1096 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1106 LOAD_ATTR               22 (_saferepr)
#            1126 LOAD_FAST                9 (@py_assert4)
#            1128 CALL                     1
#            1136 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1146 LOAD_ATTR               22 (_saferepr)
#            1166 LOAD_FAST               10 (@py_assert7)
#            1168 CALL                     1
#            1176 LOAD_CONST              12 (('py0', 'py1', 'py3', 'py5', 'py8'))
#            1178 BUILD_CONST_KEY_MAP      5
#            1180 BINARY_OP                6 (%)
#            1184 STORE_FAST               7 (@py_format9)
#            1186 LOAD_CONST              13 ('assert %(py10)s')
#            1188 LOAD_CONST              14 ('py10')
#            1190 LOAD_FAST                7 (@py_format9)
#            1192 BUILD_MAP                1
#            1194 BINARY_OP                6 (%)
#            1198 STORE_FAST              12 (@py_format11)
#            1200 LOAD_GLOBAL             25 (NULL + AssertionError)
#            1210 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1220 LOAD_ATTR               26 (_format_explanation)
#            1240 LOAD_FAST               12 (@py_format11)
#            1242 CALL                     1
#            1250 CALL                     1
#            1258 RAISE_VARARGS            1
#         >> 1260 LOAD_CONST               0 (None)
#            1262 COPY                     1
#            1264 STORE_FAST               8 (@py_assert2)
#            1266 COPY                     1
#            1268 STORE_FAST               9 (@py_assert4)
#            1270 COPY                     1
#            1272 STORE_FAST              11 (@py_assert6)
#            1274 STORE_FAST              10 (@py_assert7)
# 
#  94        1276 LOAD_FAST                1 (adapter)
#            1278 LOAD_ATTR               33 (NULL|self + disconnect)
#            1298 CALL                     0
#            1306 POP_TOP
#            1308 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_is_success_false_on_timeout at 0x3aeff050, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 96>:
#  96           0 RESUME                   0
# 
#  97           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
#  98          12 LOAD_CONST               1 ('test')
# 
#  99          14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (TIMEOUT)
# 
#  97          44 KW_NAMES                 2 (('job_id', 'status'))
#              46 CALL                     2
#              54 STORE_FAST               1 (result)
# 
# 101          56 LOAD_FAST                1 (result)
#              58 LOAD_ATTR                6 (is_success)
#              78 STORE_FAST               2 (@py_assert1)
#              80 LOAD_CONST               3 (False)
#              82 STORE_FAST               3 (@py_assert4)
#              84 LOAD_FAST                2 (@py_assert1)
#              86 LOAD_FAST                3 (@py_assert4)
#              88 IS_OP                    0
#              90 STORE_FAST               4 (@py_assert3)
#              92 LOAD_FAST                4 (@py_assert3)
#              94 POP_JUMP_IF_TRUE       173 (to 442)
#              96 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             106 LOAD_ATTR               10 (_call_reprcompare)
#             126 LOAD_CONST               4 (('is',))
#             128 LOAD_FAST                4 (@py_assert3)
#             130 BUILD_TUPLE              1
#             132 LOAD_CONST               5 (('%(py2)s\n{%(py2)s = %(py0)s.is_success\n} is %(py5)s',))
#             134 LOAD_FAST                2 (@py_assert1)
#             136 LOAD_FAST                3 (@py_assert4)
#             138 BUILD_TUPLE              2
#             140 CALL                     4
#             148 LOAD_CONST               6 ('result')
#             150 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             160 LOAD_ATTR               14 (locals)
#             180 CALL                     0
#             188 CONTAINS_OP              0
#             190 POP_JUMP_IF_TRUE        21 (to 234)
#             192 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             202 LOAD_ATTR               16 (_should_repr_global_name)
#             222 LOAD_FAST                1 (result)
#             224 CALL                     1
#             232 POP_JUMP_IF_FALSE       21 (to 276)
#         >>  234 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             244 LOAD_ATTR               18 (_saferepr)
#             264 LOAD_FAST                1 (result)
#             266 CALL                     1
#             274 JUMP_FORWARD             1 (to 278)
#         >>  276 LOAD_CONST               6 ('result')
#         >>  278 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             288 LOAD_ATTR               18 (_saferepr)
#             308 LOAD_FAST                2 (@py_assert1)
#             310 CALL                     1
#             318 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             328 LOAD_ATTR               18 (_saferepr)
#             348 LOAD_FAST                3 (@py_assert4)
#             350 CALL                     1
#             358 LOAD_CONST               7 (('py0', 'py2', 'py5'))
#             360 BUILD_CONST_KEY_MAP      3
#             362 BINARY_OP                6 (%)
#             366 STORE_FAST               5 (@py_format6)
#             368 LOAD_CONST               8 ('assert %(py7)s')
#             370 LOAD_CONST               9 ('py7')
#             372 LOAD_FAST                5 (@py_format6)
#             374 BUILD_MAP                1
#             376 BINARY_OP                6 (%)
#             380 STORE_FAST               6 (@py_format8)
#             382 LOAD_GLOBAL             21 (NULL + AssertionError)
#             392 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             402 LOAD_ATTR               22 (_format_explanation)
#             422 LOAD_FAST                6 (@py_format8)
#             424 CALL                     1
#             432 CALL                     1
#             440 RAISE_VARARGS            1
#         >>  442 LOAD_CONST               0 (None)
#             444 COPY                     1
#             446 STORE_FAST               2 (@py_assert1)
#             448 COPY                     1
#             450 STORE_FAST               4 (@py_assert3)
#             452 STORE_FAST               3 (@py_assert4)
#             454 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestErrorHandling at 0x73cd93b066a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 104>:
# 104           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestErrorHandling')
#               8 STORE_NAME               2 (__qualname__)
# 
# 105          10 LOAD_CONST               1 ('Tests for error handling.')
#              12 STORE_NAME               3 (__doc__)
# 
# 107          14 LOAD_CONST               2 (<code object test_failed_result at 0x3af9d2a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 107>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_failed_result)
# 
# 115          20 LOAD_CONST               3 (<code object test_validation_failure at 0x3af9d890, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 115>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_validation_failure)
# 
# 121          26 LOAD_CONST               4 (<code object test_is_success_false_on_error at 0x3afa0e10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 121>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_is_success_false_on_error)
#              32 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_failed_result at 0x3af9d2a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 107>:
# 107           0 RESUME                   0
# 
# 108           2 LOAD_GLOBAL              1 (NULL + ErrorAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
# 109          22 LOAD_FAST                1 (adapter)
#              24 LOAD_ATTR                3 (NULL|self + connect)
#              44 CALL                     0
#              52 POP_TOP
# 
# 110          54 LOAD_FAST                1 (adapter)
#              56 LOAD_ATTR                5 (NULL|self + run_simulation)
#              76 BUILD_MAP                0
#              78 CALL                     1
#              86 STORE_FAST               2 (result)
# 
# 111          88 LOAD_FAST                2 (result)
#              90 LOAD_ATTR                6 (status)
#             110 STORE_FAST               3 (@py_assert1)
#             112 LOAD_GLOBAL              8 (SimulationStatus)
#             122 LOAD_ATTR               10 (FAILED)
#             142 STORE_FAST               4 (@py_assert5)
#             144 LOAD_FAST                3 (@py_assert1)
#             146 LOAD_FAST                4 (@py_assert5)
#             148 COMPARE_OP              40 (==)
#             152 STORE_FAST               5 (@py_assert3)
#             154 LOAD_FAST                5 (@py_assert3)
#             156 POP_JUMP_IF_TRUE       246 (to 650)
#             158 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             168 LOAD_ATTR               14 (_call_reprcompare)
#             188 LOAD_CONST               1 (('==',))
#             190 LOAD_FAST                5 (@py_assert3)
#             192 BUILD_TUPLE              1
#             194 LOAD_CONST               2 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.FAILED\n}',))
#             196 LOAD_FAST                3 (@py_assert1)
#             198 LOAD_FAST                4 (@py_assert5)
#             200 BUILD_TUPLE              2
#             202 CALL                     4
#             210 LOAD_CONST               3 ('result')
#             212 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             222 LOAD_ATTR               18 (locals)
#             242 CALL                     0
#             250 CONTAINS_OP              0
#             252 POP_JUMP_IF_TRUE        21 (to 296)
#             254 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             264 LOAD_ATTR               20 (_should_repr_global_name)
#             284 LOAD_FAST                2 (result)
#             286 CALL                     1
#             294 POP_JUMP_IF_FALSE       21 (to 338)
#         >>  296 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             306 LOAD_ATTR               22 (_saferepr)
#             326 LOAD_FAST                2 (result)
#             328 CALL                     1
#             336 JUMP_FORWARD             1 (to 340)
#         >>  338 LOAD_CONST               3 ('result')
#         >>  340 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             350 LOAD_ATTR               22 (_saferepr)
#             370 LOAD_FAST                3 (@py_assert1)
#             372 CALL                     1
#             380 LOAD_CONST               4 ('SimulationStatus')
#             382 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             392 LOAD_ATTR               18 (locals)
#             412 CALL                     0
#             420 CONTAINS_OP              0
#             422 POP_JUMP_IF_TRUE        25 (to 474)
#             424 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             434 LOAD_ATTR               20 (_should_repr_global_name)
#             454 LOAD_GLOBAL              8 (SimulationStatus)
#             464 CALL                     1
#             472 POP_JUMP_IF_FALSE       25 (to 524)
#         >>  474 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             484 LOAD_ATTR               22 (_saferepr)
#             504 LOAD_GLOBAL              8 (SimulationStatus)
#             514 CALL                     1
#             522 JUMP_FORWARD             1 (to 526)
#         >>  524 LOAD_CONST               4 ('SimulationStatus')
#         >>  526 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             536 LOAD_ATTR               22 (_saferepr)
#             556 LOAD_FAST                4 (@py_assert5)
#             558 CALL                     1
#             566 LOAD_CONST               5 (('py0', 'py2', 'py4', 'py6'))
#             568 BUILD_CONST_KEY_MAP      4
#             570 BINARY_OP                6 (%)
#             574 STORE_FAST               6 (@py_format7)
#             576 LOAD_CONST               6 ('assert %(py8)s')
#             578 LOAD_CONST               7 ('py8')
#             580 LOAD_FAST                6 (@py_format7)
#             582 BUILD_MAP                1
#             584 BINARY_OP                6 (%)
#             588 STORE_FAST               7 (@py_format9)
#             590 LOAD_GLOBAL             25 (NULL + AssertionError)
#             600 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             610 LOAD_ATTR               26 (_format_explanation)
#             630 LOAD_FAST                7 (@py_format9)
#             632 CALL                     1
#             640 CALL                     1
#             648 RAISE_VARARGS            1
#         >>  650 LOAD_CONST               0 (None)
#             652 COPY                     1
#             654 STORE_FAST               3 (@py_assert1)
#             656 COPY                     1
#             658 STORE_FAST               5 (@py_assert3)
#             660 STORE_FAST               4 (@py_assert5)
# 
# 112         662 LOAD_FAST                2 (result)
#             664 LOAD_ATTR               28 (errors)
#             684 STORE_FAST               8 (@py_assert2)
#             686 LOAD_GLOBAL             31 (NULL + len)
#             696 LOAD_FAST                8 (@py_assert2)
#             698 CALL                     1
#             706 STORE_FAST               9 (@py_assert4)
#             708 LOAD_CONST               8 (0)
#             710 STORE_FAST              10 (@py_assert7)
#             712 LOAD_FAST                9 (@py_assert4)
#             714 LOAD_FAST               10 (@py_assert7)
#             716 COMPARE_OP              68 (>)
#             720 STORE_FAST              11 (@py_assert6)
#             722 LOAD_FAST               11 (@py_assert6)
#             724 EXTENDED_ARG             1
#             726 POP_JUMP_IF_TRUE       266 (to 1260)
#             728 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             738 LOAD_ATTR               14 (_call_reprcompare)
#             758 LOAD_CONST               9 (('>',))
#             760 LOAD_FAST               11 (@py_assert6)
#             762 BUILD_TUPLE              1
#             764 LOAD_CONST              10 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.errors\n})\n} > %(py8)s',))
#             766 LOAD_FAST                9 (@py_assert4)
#             768 LOAD_FAST               10 (@py_assert7)
#             770 BUILD_TUPLE              2
#             772 CALL                     4
#             780 LOAD_CONST              11 ('len')
#             782 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             792 LOAD_ATTR               18 (locals)
#             812 CALL                     0
#             820 CONTAINS_OP              0
#             822 POP_JUMP_IF_TRUE        25 (to 874)
#             824 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             834 LOAD_ATTR               20 (_should_repr_global_name)
#             854 LOAD_GLOBAL             30 (len)
#             864 CALL                     1
#             872 POP_JUMP_IF_FALSE       25 (to 924)
#         >>  874 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             884 LOAD_ATTR               22 (_saferepr)
#             904 LOAD_GLOBAL             30 (len)
#             914 CALL                     1
#             922 JUMP_FORWARD             1 (to 926)
#         >>  924 LOAD_CONST              11 ('len')
#         >>  926 LOAD_CONST               3 ('result')
#             928 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             938 LOAD_ATTR               18 (locals)
#             958 CALL                     0
#             966 CONTAINS_OP              0
#             968 POP_JUMP_IF_TRUE        21 (to 1012)
#             970 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             980 LOAD_ATTR               20 (_should_repr_global_name)
#            1000 LOAD_FAST                2 (result)
#            1002 CALL                     1
#            1010 POP_JUMP_IF_FALSE       21 (to 1054)
#         >> 1012 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1022 LOAD_ATTR               22 (_saferepr)
#            1042 LOAD_FAST                2 (result)
#            1044 CALL                     1
#            1052 JUMP_FORWARD             1 (to 1056)
#         >> 1054 LOAD_CONST               3 ('result')
#         >> 1056 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1066 LOAD_ATTR               22 (_saferepr)
#            1086 LOAD_FAST                8 (@py_assert2)
#            1088 CALL                     1
#            1096 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1106 LOAD_ATTR               22 (_saferepr)
#            1126 LOAD_FAST                9 (@py_assert4)
#            1128 CALL                     1
#            1136 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1146 LOAD_ATTR               22 (_saferepr)
#            1166 LOAD_FAST               10 (@py_assert7)
#            1168 CALL                     1
#            1176 LOAD_CONST              12 (('py0', 'py1', 'py3', 'py5', 'py8'))
#            1178 BUILD_CONST_KEY_MAP      5
#            1180 BINARY_OP                6 (%)
#            1184 STORE_FAST               7 (@py_format9)
#            1186 LOAD_CONST              13 ('assert %(py10)s')
#            1188 LOAD_CONST              14 ('py10')
#            1190 LOAD_FAST                7 (@py_format9)
#            1192 BUILD_MAP                1
#            1194 BINARY_OP                6 (%)
#            1198 STORE_FAST              12 (@py_format11)
#            1200 LOAD_GLOBAL             25 (NULL + AssertionError)
#            1210 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1220 LOAD_ATTR               26 (_format_explanation)
#            1240 LOAD_FAST               12 (@py_format11)
#            1242 CALL                     1
#            1250 CALL                     1
#            1258 RAISE_VARARGS            1
#         >> 1260 LOAD_CONST               0 (None)
#            1262 COPY                     1
#            1264 STORE_FAST               8 (@py_assert2)
#            1266 COPY                     1
#            1268 STORE_FAST               9 (@py_assert4)
#            1270 COPY                     1
#            1272 STORE_FAST              11 (@py_assert6)
#            1274 STORE_FAST              10 (@py_assert7)
# 
# 113        1276 LOAD_FAST                1 (adapter)
#            1278 LOAD_ATTR               33 (NULL|self + disconnect)
#            1298 CALL                     0
#            1306 POP_TOP
#            1308 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validation_failure at 0x3af9d890, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 115>:
# 115           0 RESUME                   0
# 
# 116           2 LOAD_GLOBAL              1 (NULL + ErrorAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
# 117          22 LOAD_FAST                1 (adapter)
#              24 LOAD_ATTR                3 (NULL|self + validate_config)
#              44 LOAD_CONST               1 ('invalid')
#              46 LOAD_CONST               2 (True)
#              48 BUILD_MAP                1
#              50 CALL                     1
#              58 STORE_FAST               2 (result)
# 
# 118          60 LOAD_FAST                2 (result)
#              62 LOAD_ATTR                4 (valid)
#              82 STORE_FAST               3 (@py_assert1)
#              84 LOAD_CONST               3 (False)
#              86 STORE_FAST               4 (@py_assert4)
#              88 LOAD_FAST                3 (@py_assert1)
#              90 LOAD_FAST                4 (@py_assert4)
#              92 IS_OP                    0
#              94 STORE_FAST               5 (@py_assert3)
#              96 LOAD_FAST                5 (@py_assert3)
#              98 POP_JUMP_IF_TRUE       173 (to 446)
#             100 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             110 LOAD_ATTR                8 (_call_reprcompare)
#             130 LOAD_CONST               4 (('is',))
#             132 LOAD_FAST                5 (@py_assert3)
#             134 BUILD_TUPLE              1
#             136 LOAD_CONST               5 (('%(py2)s\n{%(py2)s = %(py0)s.valid\n} is %(py5)s',))
#             138 LOAD_FAST                3 (@py_assert1)
#             140 LOAD_FAST                4 (@py_assert4)
#             142 BUILD_TUPLE              2
#             144 CALL                     4
#             152 LOAD_CONST               6 ('result')
#             154 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             164 LOAD_ATTR               12 (locals)
#             184 CALL                     0
#             192 CONTAINS_OP              0
#             194 POP_JUMP_IF_TRUE        21 (to 238)
#             196 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             206 LOAD_ATTR               14 (_should_repr_global_name)
#             226 LOAD_FAST                2 (result)
#             228 CALL                     1
#             236 POP_JUMP_IF_FALSE       21 (to 280)
#         >>  238 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             248 LOAD_ATTR               16 (_saferepr)
#             268 LOAD_FAST                2 (result)
#             270 CALL                     1
#             278 JUMP_FORWARD             1 (to 282)
#         >>  280 LOAD_CONST               6 ('result')
#         >>  282 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             292 LOAD_ATTR               16 (_saferepr)
#             312 LOAD_FAST                3 (@py_assert1)
#             314 CALL                     1
#             322 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             332 LOAD_ATTR               16 (_saferepr)
#             352 LOAD_FAST                4 (@py_assert4)
#             354 CALL                     1
#             362 LOAD_CONST               7 (('py0', 'py2', 'py5'))
#             364 BUILD_CONST_KEY_MAP      3
#             366 BINARY_OP                6 (%)
#             370 STORE_FAST               6 (@py_format6)
#             372 LOAD_CONST               8 ('assert %(py7)s')
#             374 LOAD_CONST               9 ('py7')
#             376 LOAD_FAST                6 (@py_format6)
#             378 BUILD_MAP                1
#             380 BINARY_OP                6 (%)
#             384 STORE_FAST               7 (@py_format8)
#             386 LOAD_GLOBAL             19 (NULL + AssertionError)
#             396 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             406 LOAD_ATTR               20 (_format_explanation)
#             426 LOAD_FAST                7 (@py_format8)
#             428 CALL                     1
#             436 CALL                     1
#             444 RAISE_VARARGS            1
#         >>  446 LOAD_CONST               0 (None)
#             448 COPY                     1
#             450 STORE_FAST               3 (@py_assert1)
#             452 COPY                     1
#             454 STORE_FAST               5 (@py_assert3)
#             456 STORE_FAST               4 (@py_assert4)
# 
# 119         458 LOAD_FAST                2 (result)
#             460 LOAD_ATTR               22 (errors)
#             480 STORE_FAST               8 (@py_assert2)
#             482 LOAD_GLOBAL             25 (NULL + len)
#             492 LOAD_FAST                8 (@py_assert2)
#             494 CALL                     1
#             502 STORE_FAST               4 (@py_assert4)
#             504 LOAD_CONST              10 (0)
#             506 STORE_FAST               9 (@py_assert7)
#             508 LOAD_FAST                4 (@py_assert4)
#             510 LOAD_FAST                9 (@py_assert7)
#             512 COMPARE_OP              68 (>)
#             516 STORE_FAST              10 (@py_assert6)
#             518 LOAD_FAST               10 (@py_assert6)
#             520 EXTENDED_ARG             1
#             522 POP_JUMP_IF_TRUE       266 (to 1056)
#             524 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             534 LOAD_ATTR                8 (_call_reprcompare)
#             554 LOAD_CONST              11 (('>',))
#             556 LOAD_FAST               10 (@py_assert6)
#             558 BUILD_TUPLE              1
#             560 LOAD_CONST              12 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.errors\n})\n} > %(py8)s',))
#             562 LOAD_FAST                4 (@py_assert4)
#             564 LOAD_FAST                9 (@py_assert7)
#             566 BUILD_TUPLE              2
#             568 CALL                     4
#             576 LOAD_CONST              13 ('len')
#             578 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             588 LOAD_ATTR               12 (locals)
#             608 CALL                     0
#             616 CONTAINS_OP              0
#             618 POP_JUMP_IF_TRUE        25 (to 670)
#             620 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             630 LOAD_ATTR               14 (_should_repr_global_name)
#             650 LOAD_GLOBAL             24 (len)
#             660 CALL                     1
#             668 POP_JUMP_IF_FALSE       25 (to 720)
#         >>  670 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             680 LOAD_ATTR               16 (_saferepr)
#             700 LOAD_GLOBAL             24 (len)
#             710 CALL                     1
#             718 JUMP_FORWARD             1 (to 722)
#         >>  720 LOAD_CONST              13 ('len')
#         >>  722 LOAD_CONST               6 ('result')
#             724 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             734 LOAD_ATTR               12 (locals)
#             754 CALL                     0
#             762 CONTAINS_OP              0
#             764 POP_JUMP_IF_TRUE        21 (to 808)
#             766 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             776 LOAD_ATTR               14 (_should_repr_global_name)
#             796 LOAD_FAST                2 (result)
#             798 CALL                     1
#             806 POP_JUMP_IF_FALSE       21 (to 850)
#         >>  808 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             818 LOAD_ATTR               16 (_saferepr)
#             838 LOAD_FAST                2 (result)
#             840 CALL                     1
#             848 JUMP_FORWARD             1 (to 852)
#         >>  850 LOAD_CONST               6 ('result')
#         >>  852 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             862 LOAD_ATTR               16 (_saferepr)
#             882 LOAD_FAST                8 (@py_assert2)
#             884 CALL                     1
#             892 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             902 LOAD_ATTR               16 (_saferepr)
#             922 LOAD_FAST                4 (@py_assert4)
#             924 CALL                     1
#             932 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             942 LOAD_ATTR               16 (_saferepr)
#             962 LOAD_FAST                9 (@py_assert7)
#             964 CALL                     1
#             972 LOAD_CONST              14 (('py0', 'py1', 'py3', 'py5', 'py8'))
#             974 BUILD_CONST_KEY_MAP      5
#             976 BINARY_OP                6 (%)
#             980 STORE_FAST              11 (@py_format9)
#             982 LOAD_CONST              15 ('assert %(py10)s')
#             984 LOAD_CONST              16 ('py10')
#             986 LOAD_FAST               11 (@py_format9)
#             988 BUILD_MAP                1
#             990 BINARY_OP                6 (%)
#             994 STORE_FAST              12 (@py_format11)
#             996 LOAD_GLOBAL             19 (NULL + AssertionError)
#            1006 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1016 LOAD_ATTR               20 (_format_explanation)
#            1036 LOAD_FAST               12 (@py_format11)
#            1038 CALL                     1
#            1046 CALL                     1
#            1054 RAISE_VARARGS            1
#         >> 1056 LOAD_CONST               0 (None)
#            1058 COPY                     1
#            1060 STORE_FAST               8 (@py_assert2)
#            1062 COPY                     1
#            1064 STORE_FAST               4 (@py_assert4)
#            1066 COPY                     1
#            1068 STORE_FAST              10 (@py_assert6)
#            1070 STORE_FAST               9 (@py_assert7)
#            1072 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_is_success_false_on_error at 0x3afa0e10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 121>:
# 121           0 RESUME                   0
# 
# 122           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
# 123          12 LOAD_CONST               1 ('test')
# 
# 124          14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
# 
# 125          44 LOAD_CONST               2 ('Some error occurred')
#              46 BUILD_LIST               1
# 
# 122          48 KW_NAMES                 3 (('job_id', 'status', 'errors'))
#              50 CALL                     3
#              58 STORE_FAST               1 (result)
# 
# 127          60 LOAD_FAST                1 (result)
#              62 LOAD_ATTR                6 (is_success)
#              82 STORE_FAST               2 (@py_assert1)
#              84 LOAD_CONST               4 (False)
#              86 STORE_FAST               3 (@py_assert4)
#              88 LOAD_FAST                2 (@py_assert1)
#              90 LOAD_FAST                3 (@py_assert4)
#              92 IS_OP                    0
#              94 STORE_FAST               4 (@py_assert3)
#              96 LOAD_FAST                4 (@py_assert3)
#              98 POP_JUMP_IF_TRUE       173 (to 446)
#             100 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             110 LOAD_ATTR               10 (_call_reprcompare)
#             130 LOAD_CONST               5 (('is',))
#             132 LOAD_FAST                4 (@py_assert3)
#             134 BUILD_TUPLE              1
#             136 LOAD_CONST               6 (('%(py2)s\n{%(py2)s = %(py0)s.is_success\n} is %(py5)s',))
#             138 LOAD_FAST                2 (@py_assert1)
#             140 LOAD_FAST                3 (@py_assert4)
#             142 BUILD_TUPLE              2
#             144 CALL                     4
#             152 LOAD_CONST               7 ('result')
#             154 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             164 LOAD_ATTR               14 (locals)
#             184 CALL                     0
#             192 CONTAINS_OP              0
#             194 POP_JUMP_IF_TRUE        21 (to 238)
#             196 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             206 LOAD_ATTR               16 (_should_repr_global_name)
#             226 LOAD_FAST                1 (result)
#             228 CALL                     1
#             236 POP_JUMP_IF_FALSE       21 (to 280)
#         >>  238 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             248 LOAD_ATTR               18 (_saferepr)
#             268 LOAD_FAST                1 (result)
#             270 CALL                     1
#             278 JUMP_FORWARD             1 (to 282)
#         >>  280 LOAD_CONST               7 ('result')
#         >>  282 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             292 LOAD_ATTR               18 (_saferepr)
#             312 LOAD_FAST                2 (@py_assert1)
#             314 CALL                     1
#             322 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             332 LOAD_ATTR               18 (_saferepr)
#             352 LOAD_FAST                3 (@py_assert4)
#             354 CALL                     1
#             362 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#             364 BUILD_CONST_KEY_MAP      3
#             366 BINARY_OP                6 (%)
#             370 STORE_FAST               5 (@py_format6)
#             372 LOAD_CONST               9 ('assert %(py7)s')
#             374 LOAD_CONST              10 ('py7')
#             376 LOAD_FAST                5 (@py_format6)
#             378 BUILD_MAP                1
#             380 BINARY_OP                6 (%)
#             384 STORE_FAST               6 (@py_format8)
#             386 LOAD_GLOBAL             21 (NULL + AssertionError)
#             396 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             406 LOAD_ATTR               22 (_format_explanation)
#             426 LOAD_FAST                6 (@py_format8)
#             428 CALL                     1
#             436 CALL                     1
#             444 RAISE_VARARGS            1
#         >>  446 LOAD_CONST               0 (None)
#             448 COPY                     1
#             450 STORE_FAST               2 (@py_assert1)
#             452 COPY                     1
#             454 STORE_FAST               4 (@py_assert3)
#             456 STORE_FAST               3 (@py_assert4)
#             458 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestValidationEdgeCases at 0x73cd945fdfb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 130>:
# 130           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestValidationEdgeCases')
#               8 STORE_NAME               2 (__qualname__)
# 
# 131          10 LOAD_CONST               1 ('Tests for validation edge cases.')
#              12 STORE_NAME               3 (__doc__)
# 
# 133          14 LOAD_CONST               2 (<code object test_validation_with_warnings at 0x3af9dd90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 133>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_validation_with_warnings)
# 
# 141          20 LOAD_CONST               3 (<code object test_validation_multiple_errors at 0x3af9e710, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 141>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_validation_multiple_errors)
#              26 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_validation_with_warnings at 0x3af9dd90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 133>:
# 133           0 RESUME                   0
# 
# 134           2 LOAD_GLOBAL              1 (NULL + ValidationResult)
# 
# 135          12 LOAD_CONST               1 (True)
# 
# 136          14 LOAD_CONST               2 ('Consider using a higher tolerance for better performance')
#              16 BUILD_LIST               1
# 
# 134          18 KW_NAMES                 3 (('valid', 'warnings'))
#              20 CALL                     2
#              28 STORE_FAST               1 (result)
# 
# 138          30 LOAD_FAST                1 (result)
#              32 LOAD_ATTR                2 (valid)
#              52 STORE_FAST               2 (@py_assert1)
#              54 LOAD_CONST               1 (True)
#              56 STORE_FAST               3 (@py_assert4)
#              58 LOAD_FAST                2 (@py_assert1)
#              60 LOAD_FAST                3 (@py_assert4)
#              62 IS_OP                    0
#              64 STORE_FAST               4 (@py_assert3)
#              66 LOAD_FAST                4 (@py_assert3)
#              68 POP_JUMP_IF_TRUE       173 (to 416)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               4 (('is',))
#             102 LOAD_FAST                4 (@py_assert3)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               5 (('%(py2)s\n{%(py2)s = %(py0)s.valid\n} is %(py5)s',))
#             108 LOAD_FAST                2 (@py_assert1)
#             110 LOAD_FAST                3 (@py_assert4)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_CONST               6 ('result')
#             124 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             134 LOAD_ATTR               10 (locals)
#             154 CALL                     0
#             162 CONTAINS_OP              0
#             164 POP_JUMP_IF_TRUE        21 (to 208)
#             166 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             176 LOAD_ATTR               12 (_should_repr_global_name)
#             196 LOAD_FAST                1 (result)
#             198 CALL                     1
#             206 POP_JUMP_IF_FALSE       21 (to 250)
#         >>  208 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             218 LOAD_ATTR               14 (_saferepr)
#             238 LOAD_FAST                1 (result)
#             240 CALL                     1
#             248 JUMP_FORWARD             1 (to 252)
#         >>  250 LOAD_CONST               6 ('result')
#         >>  252 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             262 LOAD_ATTR               14 (_saferepr)
#             282 LOAD_FAST                2 (@py_assert1)
#             284 CALL                     1
#             292 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             302 LOAD_ATTR               14 (_saferepr)
#             322 LOAD_FAST                3 (@py_assert4)
#             324 CALL                     1
#             332 LOAD_CONST               7 (('py0', 'py2', 'py5'))
#             334 BUILD_CONST_KEY_MAP      3
#             336 BINARY_OP                6 (%)
#             340 STORE_FAST               5 (@py_format6)
#             342 LOAD_CONST               8 ('assert %(py7)s')
#             344 LOAD_CONST               9 ('py7')
#             346 LOAD_FAST                5 (@py_format6)
#             348 BUILD_MAP                1
#             350 BINARY_OP                6 (%)
#             354 STORE_FAST               6 (@py_format8)
#             356 LOAD_GLOBAL             17 (NULL + AssertionError)
#             366 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             376 LOAD_ATTR               18 (_format_explanation)
#             396 LOAD_FAST                6 (@py_format8)
#             398 CALL                     1
#             406 CALL                     1
#             414 RAISE_VARARGS            1
#         >>  416 LOAD_CONST               0 (None)
#             418 COPY                     1
#             420 STORE_FAST               2 (@py_assert1)
#             422 COPY                     1
#             424 STORE_FAST               4 (@py_assert3)
#             426 STORE_FAST               3 (@py_assert4)
# 
# 139         428 LOAD_FAST                1 (result)
#             430 LOAD_ATTR               20 (warnings)
#             450 STORE_FAST               7 (@py_assert2)
#             452 LOAD_GLOBAL             23 (NULL + len)
#             462 LOAD_FAST                7 (@py_assert2)
#             464 CALL                     1
#             472 STORE_FAST               3 (@py_assert4)
#             474 LOAD_CONST              10 (1)
#             476 STORE_FAST               8 (@py_assert7)
#             478 LOAD_FAST                3 (@py_assert4)
#             480 LOAD_FAST                8 (@py_assert7)
#             482 COMPARE_OP              40 (==)
#             486 STORE_FAST               9 (@py_assert6)
#             488 LOAD_FAST                9 (@py_assert6)
#             490 EXTENDED_ARG             1
#             492 POP_JUMP_IF_TRUE       266 (to 1026)
#             494 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             504 LOAD_ATTR                6 (_call_reprcompare)
#             524 LOAD_CONST              11 (('==',))
#             526 LOAD_FAST                9 (@py_assert6)
#             528 BUILD_TUPLE              1
#             530 LOAD_CONST              12 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.warnings\n})\n} == %(py8)s',))
#             532 LOAD_FAST                3 (@py_assert4)
#             534 LOAD_FAST                8 (@py_assert7)
#             536 BUILD_TUPLE              2
#             538 CALL                     4
#             546 LOAD_CONST              13 ('len')
#             548 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             558 LOAD_ATTR               10 (locals)
#             578 CALL                     0
#             586 CONTAINS_OP              0
#             588 POP_JUMP_IF_TRUE        25 (to 640)
#             590 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             600 LOAD_ATTR               12 (_should_repr_global_name)
#             620 LOAD_GLOBAL             22 (len)
#             630 CALL                     1
#             638 POP_JUMP_IF_FALSE       25 (to 690)
#         >>  640 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             650 LOAD_ATTR               14 (_saferepr)
#             670 LOAD_GLOBAL             22 (len)
#             680 CALL                     1
#             688 JUMP_FORWARD             1 (to 692)
#         >>  690 LOAD_CONST              13 ('len')
#         >>  692 LOAD_CONST               6 ('result')
#             694 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             704 LOAD_ATTR               10 (locals)
#             724 CALL                     0
#             732 CONTAINS_OP              0
#             734 POP_JUMP_IF_TRUE        21 (to 778)
#             736 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             746 LOAD_ATTR               12 (_should_repr_global_name)
#             766 LOAD_FAST                1 (result)
#             768 CALL                     1
#             776 POP_JUMP_IF_FALSE       21 (to 820)
#         >>  778 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             788 LOAD_ATTR               14 (_saferepr)
#             808 LOAD_FAST                1 (result)
#             810 CALL                     1
#             818 JUMP_FORWARD             1 (to 822)
#         >>  820 LOAD_CONST               6 ('result')
#         >>  822 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             832 LOAD_ATTR               14 (_saferepr)
#             852 LOAD_FAST                7 (@py_assert2)
#             854 CALL                     1
#             862 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             872 LOAD_ATTR               14 (_saferepr)
#             892 LOAD_FAST                3 (@py_assert4)
#             894 CALL                     1
#             902 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             912 LOAD_ATTR               14 (_saferepr)
#             932 LOAD_FAST                8 (@py_assert7)
#             934 CALL                     1
#             942 LOAD_CONST              14 (('py0', 'py1', 'py3', 'py5', 'py8'))
#             944 BUILD_CONST_KEY_MAP      5
#             946 BINARY_OP                6 (%)
#             950 STORE_FAST              10 (@py_format9)
#             952 LOAD_CONST              15 ('assert %(py10)s')
#             954 LOAD_CONST              16 ('py10')
#             956 LOAD_FAST               10 (@py_format9)
#             958 BUILD_MAP                1
#             960 BINARY_OP                6 (%)
#             964 STORE_FAST              11 (@py_format11)
#             966 LOAD_GLOBAL             17 (NULL + AssertionError)
#             976 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             986 LOAD_ATTR               18 (_format_explanation)
#            1006 LOAD_FAST               11 (@py_format11)
#            1008 CALL                     1
#            1016 CALL                     1
#            1024 RAISE_VARARGS            1
#         >> 1026 LOAD_CONST               0 (None)
#            1028 COPY                     1
#            1030 STORE_FAST               7 (@py_assert2)
#            1032 COPY                     1
#            1034 STORE_FAST               3 (@py_assert4)
#            1036 COPY                     1
#            1038 STORE_FAST               9 (@py_assert6)
#            1040 STORE_FAST               8 (@py_assert7)
#            1042 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validation_multiple_errors at 0x3af9e710, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 141>:
# 141           0 RESUME                   0
# 
# 142           2 LOAD_GLOBAL              1 (NULL + ValidationResult)
#              12 LOAD_ATTR                2 (failure)
# 
# 144          32 LOAD_GLOBAL              5 (NULL + ValidationError)
#              42 LOAD_CONST               1 ('field1')
#              44 LOAD_CONST               2 ('Error 1')
#              46 KW_NAMES                 3 (('field', 'message'))
#              48 CALL                     2
# 
# 145          56 LOAD_GLOBAL              5 (NULL + ValidationError)
#              66 LOAD_CONST               4 ('field2')
#              68 LOAD_CONST               5 ('Error 2')
#              70 KW_NAMES                 3 (('field', 'message'))
#              72 CALL                     2
# 
# 146          80 LOAD_GLOBAL              5 (NULL + ValidationError)
#              90 LOAD_CONST               6 ('field3')
#              92 LOAD_CONST               7 ('Error 3')
#              94 KW_NAMES                 3 (('field', 'message'))
#              96 CALL                     2
# 
# 143         104 BUILD_LIST               3
# 
# 142         106 CALL                     1
#             114 STORE_FAST               1 (result)
# 
# 149         116 LOAD_FAST                1 (result)
#             118 LOAD_ATTR                6 (valid)
#             138 STORE_FAST               2 (@py_assert1)
#             140 LOAD_CONST               8 (False)
#             142 STORE_FAST               3 (@py_assert4)
#             144 LOAD_FAST                2 (@py_assert1)
#             146 LOAD_FAST                3 (@py_assert4)
#             148 IS_OP                    0
#             150 STORE_FAST               4 (@py_assert3)
#             152 LOAD_FAST                4 (@py_assert3)
#             154 POP_JUMP_IF_TRUE       173 (to 502)
#             156 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             166 LOAD_ATTR               10 (_call_reprcompare)
#             186 LOAD_CONST               9 (('is',))
#             188 LOAD_FAST                4 (@py_assert3)
#             190 BUILD_TUPLE              1
#             192 LOAD_CONST              10 (('%(py2)s\n{%(py2)s = %(py0)s.valid\n} is %(py5)s',))
#             194 LOAD_FAST                2 (@py_assert1)
#             196 LOAD_FAST                3 (@py_assert4)
#             198 BUILD_TUPLE              2
#             200 CALL                     4
#             208 LOAD_CONST              11 ('result')
#             210 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             220 LOAD_ATTR               14 (locals)
#             240 CALL                     0
#             248 CONTAINS_OP              0
#             250 POP_JUMP_IF_TRUE        21 (to 294)
#             252 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             262 LOAD_ATTR               16 (_should_repr_global_name)
#             282 LOAD_FAST                1 (result)
#             284 CALL                     1
#             292 POP_JUMP_IF_FALSE       21 (to 336)
#         >>  294 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             304 LOAD_ATTR               18 (_saferepr)
#             324 LOAD_FAST                1 (result)
#             326 CALL                     1
#             334 JUMP_FORWARD             1 (to 338)
#         >>  336 LOAD_CONST              11 ('result')
#         >>  338 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             348 LOAD_ATTR               18 (_saferepr)
#             368 LOAD_FAST                2 (@py_assert1)
#             370 CALL                     1
#             378 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             388 LOAD_ATTR               18 (_saferepr)
#             408 LOAD_FAST                3 (@py_assert4)
#             410 CALL                     1
#             418 LOAD_CONST              12 (('py0', 'py2', 'py5'))
#             420 BUILD_CONST_KEY_MAP      3
#             422 BINARY_OP                6 (%)
#             426 STORE_FAST               5 (@py_format6)
#             428 LOAD_CONST              13 ('assert %(py7)s')
#             430 LOAD_CONST              14 ('py7')
#             432 LOAD_FAST                5 (@py_format6)
#             434 BUILD_MAP                1
#             436 BINARY_OP                6 (%)
#             440 STORE_FAST               6 (@py_format8)
#             442 LOAD_GLOBAL             21 (NULL + AssertionError)
#             452 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             462 LOAD_ATTR               22 (_format_explanation)
#             482 LOAD_FAST                6 (@py_format8)
#             484 CALL                     1
#             492 CALL                     1
#             500 RAISE_VARARGS            1
#         >>  502 LOAD_CONST               0 (None)
#             504 COPY                     1
#             506 STORE_FAST               2 (@py_assert1)
#             508 COPY                     1
#             510 STORE_FAST               4 (@py_assert3)
#             512 STORE_FAST               3 (@py_assert4)
# 
# 150         514 LOAD_FAST                1 (result)
#             516 LOAD_ATTR               24 (errors)
#             536 STORE_FAST               7 (@py_assert2)
#             538 LOAD_GLOBAL             27 (NULL + len)
#             548 LOAD_FAST                7 (@py_assert2)
#             550 CALL                     1
#             558 STORE_FAST               3 (@py_assert4)
#             560 LOAD_CONST              15 (3)
#             562 STORE_FAST               8 (@py_assert7)
#             564 LOAD_FAST                3 (@py_assert4)
#             566 LOAD_FAST                8 (@py_assert7)
#             568 COMPARE_OP              40 (==)
#             572 STORE_FAST               9 (@py_assert6)
#             574 LOAD_FAST                9 (@py_assert6)
#             576 EXTENDED_ARG             1
#             578 POP_JUMP_IF_TRUE       266 (to 1112)
#             580 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             590 LOAD_ATTR               10 (_call_reprcompare)
#             610 LOAD_CONST              16 (('==',))
#             612 LOAD_FAST                9 (@py_assert6)
#             614 BUILD_TUPLE              1
#             616 LOAD_CONST              17 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.errors\n})\n} == %(py8)s',))
#             618 LOAD_FAST                3 (@py_assert4)
#             620 LOAD_FAST                8 (@py_assert7)
#             622 BUILD_TUPLE              2
#             624 CALL                     4
#             632 LOAD_CONST              18 ('len')
#             634 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             644 LOAD_ATTR               14 (locals)
#             664 CALL                     0
#             672 CONTAINS_OP              0
#             674 POP_JUMP_IF_TRUE        25 (to 726)
#             676 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             686 LOAD_ATTR               16 (_should_repr_global_name)
#             706 LOAD_GLOBAL             26 (len)
#             716 CALL                     1
#             724 POP_JUMP_IF_FALSE       25 (to 776)
#         >>  726 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             736 LOAD_ATTR               18 (_saferepr)
#             756 LOAD_GLOBAL             26 (len)
#             766 CALL                     1
#             774 JUMP_FORWARD             1 (to 778)
#         >>  776 LOAD_CONST              18 ('len')
#         >>  778 LOAD_CONST              11 ('result')
#             780 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             790 LOAD_ATTR               14 (locals)
#             810 CALL                     0
#             818 CONTAINS_OP              0
#             820 POP_JUMP_IF_TRUE        21 (to 864)
#             822 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             832 LOAD_ATTR               16 (_should_repr_global_name)
#             852 LOAD_FAST                1 (result)
#             854 CALL                     1
#             862 POP_JUMP_IF_FALSE       21 (to 906)
#         >>  864 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             874 LOAD_ATTR               18 (_saferepr)
#             894 LOAD_FAST                1 (result)
#             896 CALL                     1
#             904 JUMP_FORWARD             1 (to 908)
#         >>  906 LOAD_CONST              11 ('result')
#         >>  908 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             918 LOAD_ATTR               18 (_saferepr)
#             938 LOAD_FAST                7 (@py_assert2)
#             940 CALL                     1
#             948 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             958 LOAD_ATTR               18 (_saferepr)
#             978 LOAD_FAST                3 (@py_assert4)
#             980 CALL                     1
#             988 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             998 LOAD_ATTR               18 (_saferepr)
#            1018 LOAD_FAST                8 (@py_assert7)
#            1020 CALL                     1
#            1028 LOAD_CONST              19 (('py0', 'py1', 'py3', 'py5', 'py8'))
#            1030 BUILD_CONST_KEY_MAP      5
#            1032 BINARY_OP                6 (%)
#            1036 STORE_FAST              10 (@py_format9)
#            1038 LOAD_CONST              20 ('assert %(py10)s')
#            1040 LOAD_CONST              21 ('py10')
#            1042 LOAD_FAST               10 (@py_format9)
#            1044 BUILD_MAP                1
#            1046 BINARY_OP                6 (%)
#            1050 STORE_FAST              11 (@py_format11)
#            1052 LOAD_GLOBAL             21 (NULL + AssertionError)
#            1062 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1072 LOAD_ATTR               22 (_format_explanation)
#            1092 LOAD_FAST               11 (@py_format11)
#            1094 CALL                     1
#            1102 CALL                     1
#            1110 RAISE_VARARGS            1
#         >> 1112 LOAD_CONST               0 (None)
#            1114 COPY                     1
#            1116 STORE_FAST               7 (@py_assert2)
#            1118 COPY                     1
#            1120 STORE_FAST               3 (@py_assert4)
#            1122 COPY                     1
#            1124 STORE_FAST               9 (@py_assert6)
#            1126 STORE_FAST               8 (@py_assert7)
#            1128 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestSimulationResultEdgeCases at 0x73cd93b065b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 153>:
# 153           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestSimulationResultEdgeCases')
#               8 STORE_NAME               2 (__qualname__)
# 
# 154          10 LOAD_CONST               1 ('Tests for SimulationResult edge cases.')
#              12 STORE_NAME               3 (__doc__)
# 
# 156          14 LOAD_CONST               2 (<code object test_result_with_no_data at 0x3af9cd30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 156>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_result_with_no_data)
# 
# 164          20 LOAD_CONST               3 (<code object test_result_with_empty_errors at 0x3af98b30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 164>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_result_with_empty_errors)
# 
# 172          26 LOAD_CONST               4 (<code object test_to_dict_complete at 0x3af9f780, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 172>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_to_dict_complete)
#              32 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_result_with_no_data at 0x3af9cd30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 156>:
# 156           0 RESUME                   0
# 
# 157           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
# 158          12 LOAD_CONST               1 ('test')
# 
# 159          14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
# 
# 157          44 KW_NAMES                 2 (('job_id', 'status'))
#              46 CALL                     2
#              54 STORE_FAST               1 (result)
# 
# 161          56 LOAD_FAST                1 (result)
#              58 LOAD_ATTR                6 (data)
#              78 STORE_FAST               2 (@py_assert1)
#              80 LOAD_CONST               0 (None)
#              82 STORE_FAST               3 (@py_assert4)
#              84 LOAD_FAST                2 (@py_assert1)
#              86 LOAD_FAST                3 (@py_assert4)
#              88 IS_OP                    0
#              90 STORE_FAST               4 (@py_assert3)
#              92 LOAD_FAST                4 (@py_assert3)
#              94 POP_JUMP_IF_TRUE       173 (to 442)
#              96 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             106 LOAD_ATTR               10 (_call_reprcompare)
#             126 LOAD_CONST               3 (('is',))
#             128 LOAD_FAST                4 (@py_assert3)
#             130 BUILD_TUPLE              1
#             132 LOAD_CONST               4 (('%(py2)s\n{%(py2)s = %(py0)s.data\n} is %(py5)s',))
#             134 LOAD_FAST                2 (@py_assert1)
#             136 LOAD_FAST                3 (@py_assert4)
#             138 BUILD_TUPLE              2
#             140 CALL                     4
#             148 LOAD_CONST               5 ('result')
#             150 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             160 LOAD_ATTR               14 (locals)
#             180 CALL                     0
#             188 CONTAINS_OP              0
#             190 POP_JUMP_IF_TRUE        21 (to 234)
#             192 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             202 LOAD_ATTR               16 (_should_repr_global_name)
#             222 LOAD_FAST                1 (result)
#             224 CALL                     1
#             232 POP_JUMP_IF_FALSE       21 (to 276)
#         >>  234 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             244 LOAD_ATTR               18 (_saferepr)
#             264 LOAD_FAST                1 (result)
#             266 CALL                     1
#             274 JUMP_FORWARD             1 (to 278)
#         >>  276 LOAD_CONST               5 ('result')
#         >>  278 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             288 LOAD_ATTR               18 (_saferepr)
#             308 LOAD_FAST                2 (@py_assert1)
#             310 CALL                     1
#             318 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             328 LOAD_ATTR               18 (_saferepr)
#             348 LOAD_FAST                3 (@py_assert4)
#             350 CALL                     1
#             358 LOAD_CONST               6 (('py0', 'py2', 'py5'))
#             360 BUILD_CONST_KEY_MAP      3
#             362 BINARY_OP                6 (%)
#             366 STORE_FAST               5 (@py_format6)
#             368 LOAD_CONST               7 ('assert %(py7)s')
#             370 LOAD_CONST               8 ('py7')
#             372 LOAD_FAST                5 (@py_format6)
#             374 BUILD_MAP                1
#             376 BINARY_OP                6 (%)
#             380 STORE_FAST               6 (@py_format8)
#             382 LOAD_GLOBAL             21 (NULL + AssertionError)
#             392 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             402 LOAD_ATTR               22 (_format_explanation)
#             422 LOAD_FAST                6 (@py_format8)
#             424 CALL                     1
#             432 CALL                     1
#             440 RAISE_VARARGS            1
#         >>  442 LOAD_CONST               0 (None)
#             444 COPY                     1
#             446 STORE_FAST               2 (@py_assert1)
#             448 COPY                     1
#             450 STORE_FAST               4 (@py_assert3)
#             452 STORE_FAST               3 (@py_assert4)
# 
# 162         454 LOAD_FAST                1 (result)
#             456 LOAD_ATTR               24 (is_success)
#             476 STORE_FAST               2 (@py_assert1)
#             478 LOAD_CONST               9 (True)
#             480 STORE_FAST               3 (@py_assert4)
#             482 LOAD_FAST                2 (@py_assert1)
#             484 LOAD_FAST                3 (@py_assert4)
#             486 IS_OP                    0
#             488 STORE_FAST               4 (@py_assert3)
#             490 LOAD_FAST                4 (@py_assert3)
#             492 POP_JUMP_IF_TRUE       173 (to 840)
#             494 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             504 LOAD_ATTR               10 (_call_reprcompare)
#             524 LOAD_CONST               3 (('is',))
#             526 LOAD_FAST                4 (@py_assert3)
#             528 BUILD_TUPLE              1
#             530 LOAD_CONST              10 (('%(py2)s\n{%(py2)s = %(py0)s.is_success\n} is %(py5)s',))
#             532 LOAD_FAST                2 (@py_assert1)
#             534 LOAD_FAST                3 (@py_assert4)
#             536 BUILD_TUPLE              2
#             538 CALL                     4
#             546 LOAD_CONST               5 ('result')
#             548 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             558 LOAD_ATTR               14 (locals)
#             578 CALL                     0
#             586 CONTAINS_OP              0
#             588 POP_JUMP_IF_TRUE        21 (to 632)
#             590 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             600 LOAD_ATTR               16 (_should_repr_global_name)
#             620 LOAD_FAST                1 (result)
#             622 CALL                     1
#             630 POP_JUMP_IF_FALSE       21 (to 674)
#         >>  632 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             642 LOAD_ATTR               18 (_saferepr)
#             662 LOAD_FAST                1 (result)
#             664 CALL                     1
#             672 JUMP_FORWARD             1 (to 676)
#         >>  674 LOAD_CONST               5 ('result')
#         >>  676 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             686 LOAD_ATTR               18 (_saferepr)
#             706 LOAD_FAST                2 (@py_assert1)
#             708 CALL                     1
#             716 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             726 LOAD_ATTR               18 (_saferepr)
#             746 LOAD_FAST                3 (@py_assert4)
#             748 CALL                     1
#             756 LOAD_CONST               6 (('py0', 'py2', 'py5'))
#             758 BUILD_CONST_KEY_MAP      3
#             760 BINARY_OP                6 (%)
#             764 STORE_FAST               5 (@py_format6)
#             766 LOAD_CONST               7 ('assert %(py7)s')
#             768 LOAD_CONST               8 ('py7')
#             770 LOAD_FAST                5 (@py_format6)
#             772 BUILD_MAP                1
#             774 BINARY_OP                6 (%)
#             778 STORE_FAST               6 (@py_format8)
#             780 LOAD_GLOBAL             21 (NULL + AssertionError)
#             790 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             800 LOAD_ATTR               22 (_format_explanation)
#             820 LOAD_FAST                6 (@py_format8)
#             822 CALL                     1
#             830 CALL                     1
#             838 RAISE_VARARGS            1
#         >>  840 LOAD_CONST               0 (None)
#             842 COPY                     1
#             844 STORE_FAST               2 (@py_assert1)
#             846 COPY                     1
#             848 STORE_FAST               4 (@py_assert3)
#             850 STORE_FAST               3 (@py_assert4)
#             852 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_result_with_empty_errors at 0x3af98b30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 164>:
# 164           0 RESUME                   0
# 
# 165           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
# 166          12 LOAD_CONST               1 ('test')
# 
# 167          14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
# 
# 168          44 BUILD_LIST               0
# 
# 165          46 KW_NAMES                 2 (('job_id', 'status', 'errors'))
#              48 CALL                     3
#              56 STORE_FAST               1 (result)
# 
# 170          58 LOAD_FAST                1 (result)
#              60 LOAD_ATTR                6 (is_success)
#              80 STORE_FAST               2 (@py_assert1)
#              82 LOAD_CONST               3 (True)
#              84 STORE_FAST               3 (@py_assert4)
#              86 LOAD_FAST                2 (@py_assert1)
#              88 LOAD_FAST                3 (@py_assert4)
#              90 IS_OP                    0
#              92 STORE_FAST               4 (@py_assert3)
#              94 LOAD_FAST                4 (@py_assert3)
#              96 POP_JUMP_IF_TRUE       173 (to 444)
#              98 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             108 LOAD_ATTR               10 (_call_reprcompare)
#             128 LOAD_CONST               4 (('is',))
#             130 LOAD_FAST                4 (@py_assert3)
#             132 BUILD_TUPLE              1
#             134 LOAD_CONST               5 (('%(py2)s\n{%(py2)s = %(py0)s.is_success\n} is %(py5)s',))
#             136 LOAD_FAST                2 (@py_assert1)
#             138 LOAD_FAST                3 (@py_assert4)
#             140 BUILD_TUPLE              2
#             142 CALL                     4
#             150 LOAD_CONST               6 ('result')
#             152 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             162 LOAD_ATTR               14 (locals)
#             182 CALL                     0
#             190 CONTAINS_OP              0
#             192 POP_JUMP_IF_TRUE        21 (to 236)
#             194 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             204 LOAD_ATTR               16 (_should_repr_global_name)
#             224 LOAD_FAST                1 (result)
#             226 CALL                     1
#             234 POP_JUMP_IF_FALSE       21 (to 278)
#         >>  236 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             246 LOAD_ATTR               18 (_saferepr)
#             266 LOAD_FAST                1 (result)
#             268 CALL                     1
#             276 JUMP_FORWARD             1 (to 280)
#         >>  278 LOAD_CONST               6 ('result')
#         >>  280 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             290 LOAD_ATTR               18 (_saferepr)
#             310 LOAD_FAST                2 (@py_assert1)
#             312 CALL                     1
#             320 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             330 LOAD_ATTR               18 (_saferepr)
#             350 LOAD_FAST                3 (@py_assert4)
#             352 CALL                     1
#             360 LOAD_CONST               7 (('py0', 'py2', 'py5'))
#             362 BUILD_CONST_KEY_MAP      3
#             364 BINARY_OP                6 (%)
#             368 STORE_FAST               5 (@py_format6)
#             370 LOAD_CONST               8 ('assert %(py7)s')
#             372 LOAD_CONST               9 ('py7')
#             374 LOAD_FAST                5 (@py_format6)
#             376 BUILD_MAP                1
#             378 BINARY_OP                6 (%)
#             382 STORE_FAST               6 (@py_format8)
#             384 LOAD_GLOBAL             21 (NULL + AssertionError)
#             394 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             404 LOAD_ATTR               22 (_format_explanation)
#             424 LOAD_FAST                6 (@py_format8)
#             426 CALL                     1
#             434 CALL                     1
#             442 RAISE_VARARGS            1
#         >>  444 LOAD_CONST               0 (None)
#             446 COPY                     1
#             448 STORE_FAST               2 (@py_assert1)
#             450 COPY                     1
#             452 STORE_FAST               4 (@py_assert3)
#             454 STORE_FAST               3 (@py_assert4)
#             456 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_to_dict_complete at 0x3af9f780, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py", line 172>:
# 172           0 RESUME                   0
# 
# 173           2 LOAD_CONST               1 (0)
#               4 LOAD_CONST               2 (('datetime',))
#               6 IMPORT_NAME              0 (datetime)
#               8 IMPORT_FROM              0 (datetime)
#              10 STORE_FAST               1 (datetime)
#              12 POP_TOP
# 
# 175          14 LOAD_GLOBAL              3 (NULL + SimulationResult)
# 
# 176          24 LOAD_CONST               3 ('test')
# 
# 177          26 LOAD_GLOBAL              4 (SimulationStatus)
#              36 LOAD_ATTR                6 (COMPLETED)
# 
# 178          56 LOAD_CONST               4 ('key')
#              58 LOAD_CONST               5 ('value')
#              60 BUILD_MAP                1
# 
# 179          62 LOAD_CONST               6 ('meta')
#              64 LOAD_CONST               7 ('data')
#              66 BUILD_MAP                1
# 
# 180          68 LOAD_CONST               8 ('error1')
#              70 BUILD_LIST               1
# 
# 181          72 LOAD_CONST               9 ('warning1')
#              74 BUILD_LIST               1
# 
# 182          76 PUSH_NULL
#              78 LOAD_FAST                1 (datetime)
#              80 LOAD_CONST              10 (2024)
#              82 LOAD_CONST              11 (1)
#              84 LOAD_CONST              11 (1)
#              86 LOAD_CONST              12 (12)
#              88 LOAD_CONST               1 (0)
#              90 LOAD_CONST               1 (0)
#              92 CALL                     6
# 
# 183         100 PUSH_NULL
#             102 LOAD_FAST                1 (datetime)
#             104 LOAD_CONST              10 (2024)
#             106 LOAD_CONST              11 (1)
#             108 LOAD_CONST              11 (1)
#             110 LOAD_CONST              12 (12)
#             112 LOAD_CONST              11 (1)
#             114 LOAD_CONST               1 (0)
#             116 CALL                     6
# 
# 175         124 KW_NAMES                13 (('job_id', 'status', 'data', 'metadata', 'errors', 'warnings', 'started_at', 'completed_at'))
#             126 CALL                     8
#             134 STORE_FAST               2 (result)
# 
# 185         136 LOAD_FAST                2 (result)
#             138 LOAD_ATTR                9 (NULL|self + to_dict)
#             158 CALL                     0
#             166 STORE_FAST               3 (d)
# 
# 186         168 LOAD_FAST                3 (d)
#             170 LOAD_CONST              14 ('job_id')
#             172 BINARY_SUBSCR
#             176 STORE_FAST               4 (@py_assert0)
#             178 LOAD_CONST               3 ('test')
#             180 STORE_FAST               5 (@py_assert3)
#             182 LOAD_FAST                4 (@py_assert0)
#             184 LOAD_FAST                5 (@py_assert3)
#             186 COMPARE_OP              40 (==)
#             190 STORE_FAST               6 (@py_assert2)
#             192 LOAD_FAST                6 (@py_assert2)
#             194 POP_JUMP_IF_TRUE       108 (to 412)
#             196 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             206 LOAD_ATTR               12 (_call_reprcompare)
#             226 LOAD_CONST              15 (('==',))
#             228 LOAD_FAST                6 (@py_assert2)
#             230 BUILD_TUPLE              1
#             232 LOAD_CONST              16 (('%(py1)s == %(py4)s',))
#             234 LOAD_FAST                4 (@py_assert0)
#             236 LOAD_FAST                5 (@py_assert3)
#             238 BUILD_TUPLE              2
#             240 CALL                     4
#             248 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             258 LOAD_ATTR               14 (_saferepr)
#             278 LOAD_FAST                4 (@py_assert0)
#             280 CALL                     1
#             288 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             298 LOAD_ATTR               14 (_saferepr)
#             318 LOAD_FAST                5 (@py_assert3)
#             320 CALL                     1
#             328 LOAD_CONST              17 (('py1', 'py4'))
#             330 BUILD_CONST_KEY_MAP      2
#             332 BINARY_OP                6 (%)
#             336 STORE_FAST               7 (@py_format5)
#             338 LOAD_CONST              18 ('assert %(py6)s')
#             340 LOAD_CONST              19 ('py6')
#             342 LOAD_FAST                7 (@py_format5)
#             344 BUILD_MAP                1
#             346 BINARY_OP                6 (%)
#             350 STORE_FAST               8 (@py_format7)
#             352 LOAD_GLOBAL             17 (NULL + AssertionError)
#             362 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             372 LOAD_ATTR               18 (_format_explanation)
#             392 LOAD_FAST                8 (@py_format7)
#             394 CALL                     1
#             402 CALL                     1
#             410 RAISE_VARARGS            1
#         >>  412 LOAD_CONST               0 (None)
#             414 COPY                     1
#             416 STORE_FAST               4 (@py_assert0)
#             418 COPY                     1
#             420 STORE_FAST               6 (@py_assert2)
#             422 STORE_FAST               5 (@py_assert3)
# 
# 187         424 LOAD_FAST                3 (d)
#             426 LOAD_CONST              20 ('status')
#             428 BINARY_SUBSCR
#             432 STORE_FAST               4 (@py_assert0)
#             434 LOAD_CONST              21 ('completed')
#             436 STORE_FAST               5 (@py_assert3)
#             438 LOAD_FAST                4 (@py_assert0)
#             440 LOAD_FAST                5 (@py_assert3)
#             442 COMPARE_OP              40 (==)
#             446 STORE_FAST               6 (@py_assert2)
#             448 LOAD_FAST                6 (@py_assert2)
#             450 POP_JUMP_IF_TRUE       108 (to 668)
#             452 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             462 LOAD_ATTR               12 (_call_reprcompare)
#             482 LOAD_CONST              15 (('==',))
#             484 LOAD_FAST                6 (@py_assert2)
#             486 BUILD_TUPLE              1
#             488 LOAD_CONST              16 (('%(py1)s == %(py4)s',))
#             490 LOAD_FAST                4 (@py_assert0)
#             492 LOAD_FAST                5 (@py_assert3)
#             494 BUILD_TUPLE              2
#             496 CALL                     4
#             504 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             514 LOAD_ATTR               14 (_saferepr)
#             534 LOAD_FAST                4 (@py_assert0)
#             536 CALL                     1
#             544 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             554 LOAD_ATTR               14 (_saferepr)
#             574 LOAD_FAST                5 (@py_assert3)
#             576 CALL                     1
#             584 LOAD_CONST              17 (('py1', 'py4'))
#             586 BUILD_CONST_KEY_MAP      2
#             588 BINARY_OP                6 (%)
#             592 STORE_FAST               7 (@py_format5)
#             594 LOAD_CONST              18 ('assert %(py6)s')
#             596 LOAD_CONST              19 ('py6')
#             598 LOAD_FAST                7 (@py_format5)
#             600 BUILD_MAP                1
#             602 BINARY_OP                6 (%)
#             606 STORE_FAST               8 (@py_format7)
#             608 LOAD_GLOBAL             17 (NULL + AssertionError)
#             618 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             628 LOAD_ATTR               18 (_format_explanation)
#             648 LOAD_FAST                8 (@py_format7)
#             650 CALL                     1
#             658 CALL                     1
#             666 RAISE_VARARGS            1
#         >>  668 LOAD_CONST               0 (None)
#             670 COPY                     1
#             672 STORE_FAST               4 (@py_assert0)
#             674 COPY                     1
#             676 STORE_FAST               6 (@py_assert2)
#             678 STORE_FAST               5 (@py_assert3)
# 
# 188         680 LOAD_FAST                3 (d)
#             682 LOAD_CONST               7 ('data')
#             684 BINARY_SUBSCR
#             688 LOAD_CONST               4 ('key')
#             690 BINARY_SUBSCR
#             694 STORE_FAST               4 (@py_assert0)
#             696 LOAD_CONST               5 ('value')
#             698 STORE_FAST               5 (@py_assert3)
#             700 LOAD_FAST                4 (@py_assert0)
#             702 LOAD_FAST                5 (@py_assert3)
#             704 COMPARE_OP              40 (==)
#             708 STORE_FAST               6 (@py_assert2)
#             710 LOAD_FAST                6 (@py_assert2)
#             712 POP_JUMP_IF_TRUE       108 (to 930)
#             714 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             724 LOAD_ATTR               12 (_call_reprcompare)
#             744 LOAD_CONST              15 (('==',))
#             746 LOAD_FAST                6 (@py_assert2)
#             748 BUILD_TUPLE              1
#             750 LOAD_CONST              16 (('%(py1)s == %(py4)s',))
#             752 LOAD_FAST                4 (@py_assert0)
#             754 LOAD_FAST                5 (@py_assert3)
#             756 BUILD_TUPLE              2
#             758 CALL                     4
#             766 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             776 LOAD_ATTR               14 (_saferepr)
#             796 LOAD_FAST                4 (@py_assert0)
#             798 CALL                     1
#             806 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             816 LOAD_ATTR               14 (_saferepr)
#             836 LOAD_FAST                5 (@py_assert3)
#             838 CALL                     1
#             846 LOAD_CONST              17 (('py1', 'py4'))
#             848 BUILD_CONST_KEY_MAP      2
#             850 BINARY_OP                6 (%)
#             854 STORE_FAST               7 (@py_format5)
#             856 LOAD_CONST              18 ('assert %(py6)s')
#             858 LOAD_CONST              19 ('py6')
#             860 LOAD_FAST                7 (@py_format5)
#             862 BUILD_MAP                1
#             864 BINARY_OP                6 (%)
#             868 STORE_FAST               8 (@py_format7)
#             870 LOAD_GLOBAL             17 (NULL + AssertionError)
#             880 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             890 LOAD_ATTR               18 (_format_explanation)
#             910 LOAD_FAST                8 (@py_format7)
#             912 CALL                     1
#             920 CALL                     1
#             928 RAISE_VARARGS            1
#         >>  930 LOAD_CONST               0 (None)
#             932 COPY                     1
#             934 STORE_FAST               4 (@py_assert0)
#             936 COPY                     1
#             938 STORE_FAST               6 (@py_assert2)
#             940 STORE_FAST               5 (@py_assert3)
# 
# 189         942 LOAD_FAST                3 (d)
#             944 LOAD_CONST              22 ('duration_seconds')
#             946 BINARY_SUBSCR
#             950 STORE_FAST               4 (@py_assert0)
#             952 LOAD_CONST              23 (60.0)
#             954 STORE_FAST               5 (@py_assert3)
#             956 LOAD_FAST                4 (@py_assert0)
#             958 LOAD_FAST                5 (@py_assert3)
#             960 COMPARE_OP              40 (==)
#             964 STORE_FAST               6 (@py_assert2)
#             966 LOAD_FAST                6 (@py_assert2)
#             968 POP_JUMP_IF_TRUE       108 (to 1186)
#             970 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             980 LOAD_ATTR               12 (_call_reprcompare)
#            1000 LOAD_CONST              15 (('==',))
#            1002 LOAD_FAST                6 (@py_assert2)
#            1004 BUILD_TUPLE              1
#            1006 LOAD_CONST              16 (('%(py1)s == %(py4)s',))
#            1008 LOAD_FAST                4 (@py_assert0)
#            1010 LOAD_FAST                5 (@py_assert3)
#            1012 BUILD_TUPLE              2
#            1014 CALL                     4
#            1022 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1032 LOAD_ATTR               14 (_saferepr)
#            1052 LOAD_FAST                4 (@py_assert0)
#            1054 CALL                     1
#            1062 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1072 LOAD_ATTR               14 (_saferepr)
#            1092 LOAD_FAST                5 (@py_assert3)
#            1094 CALL                     1
#            1102 LOAD_CONST              17 (('py1', 'py4'))
#            1104 BUILD_CONST_KEY_MAP      2
#            1106 BINARY_OP                6 (%)
#            1110 STORE_FAST               7 (@py_format5)
#            1112 LOAD_CONST              18 ('assert %(py6)s')
#            1114 LOAD_CONST              19 ('py6')
#            1116 LOAD_FAST                7 (@py_format5)
#            1118 BUILD_MAP                1
#            1120 BINARY_OP                6 (%)
#            1124 STORE_FAST               8 (@py_format7)
#            1126 LOAD_GLOBAL             17 (NULL + AssertionError)
#            1136 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1146 LOAD_ATTR               18 (_format_explanation)
#            1166 LOAD_FAST                8 (@py_format7)
#            1168 CALL                     1
#            1176 CALL                     1
#            1184 RAISE_VARARGS            1
#         >> 1186 LOAD_CONST               0 (None)
#            1188 COPY                     1
#            1190 STORE_FAST               4 (@py_assert0)
#            1192 COPY                     1
#            1194 STORE_FAST               6 (@py_assert2)
#            1196 STORE_FAST               5 (@py_assert3)
#            1198 RETURN_CONST             0 (None)
# 