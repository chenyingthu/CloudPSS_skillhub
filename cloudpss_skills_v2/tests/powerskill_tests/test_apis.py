# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/__pycache__/test_apis.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


class MockAWTAdapter:
    """MockAWTAdapter"""
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


def TestSimulationAPI():
    """TestSimulationAPI"""
pass  # TODO: restore


def TestPowerFlowAPI():
    """TestPowerFlowAPI"""
pass  # TODO: restore


def TestAPIFactory():
    """TestAPIFactory"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('Tests for PowerSkill layer.')
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
#              42 LOAD_CONST               3 (('Mock', 'MagicMock'))
#              44 IMPORT_NAME              8 (unittest.mock)
#              46 IMPORT_FROM              9 (Mock)
#              48 STORE_NAME               9 (Mock)
#              50 IMPORT_FROM             10 (MagicMock)
#              52 STORE_NAME              10 (MagicMock)
#              54 POP_TOP
# 
#   5          56 LOAD_CONST               1 (0)
#              58 LOAD_CONST               4 (('SimulationStatus', 'SimulationResult', 'ValidationResult', 'EngineAdapter', 'EngineConfig'))
#              60 IMPORT_NAME             11 (cloudpss_skills_v2.powerapi)
#              62 IMPORT_FROM             12 (SimulationStatus)
#              64 STORE_NAME              12 (SimulationStatus)
#              66 IMPORT_FROM             13 (SimulationResult)
#              68 STORE_NAME              13 (SimulationResult)
#              70 IMPORT_FROM             14 (ValidationResult)
#              72 STORE_NAME              14 (ValidationResult)
#              74 IMPORT_FROM             15 (EngineAdapter)
#              76 STORE_NAME              15 (EngineAdapter)
#              78 IMPORT_FROM             16 (EngineConfig)
#              80 STORE_NAME              16 (EngineConfig)
#              82 POP_TOP
# 
#  12          84 LOAD_CONST               1 (0)
#              86 LOAD_CONST               5 (('SimulationAPI',))
#              88 IMPORT_NAME             17 (cloudpss_skills_v2.powerskill)
#              90 IMPORT_FROM             18 (SimulationAPI)
#              92 STORE_NAME              18 (SimulationAPI)
#              94 POP_TOP
# 
#  13          96 LOAD_CONST               1 (0)
#              98 LOAD_CONST               6 (('PowerFlowAPI', 'APIFactory'))
#             100 IMPORT_NAME             19 (cloudpss_skills_v2.powerskill.apis)
#             102 IMPORT_FROM             20 (PowerFlowAPI)
#             104 STORE_NAME              20 (PowerFlowAPI)
#             106 IMPORT_FROM             21 (APIFactory)
#             108 STORE_NAME              21 (APIFactory)
#             110 POP_TOP
# 
#  16         112 PUSH_NULL
#             114 LOAD_BUILD_CLASS
#             116 LOAD_CONST               7 (<code object MockAWTAdapter at 0x73cd93b39c50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 16>)
#             118 MAKE_FUNCTION            0
#             120 LOAD_CONST               8 ('MockAWTAdapter')
#             122 LOAD_NAME               15 (EngineAdapter)
#             124 CALL                     3
#             132 STORE_NAME              22 (MockAWTAdapter)
# 
#  54         134 PUSH_NULL
#             136 LOAD_BUILD_CLASS
#             138 LOAD_CONST               9 (<code object TestSimulationAPI at 0x73cd945fc110, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 54>)
#             140 MAKE_FUNCTION            0
#             142 LOAD_CONST              10 ('TestSimulationAPI')
#             144 CALL                     2
#             152 STORE_NAME              23 (TestSimulationAPI)
# 
#  70         154 PUSH_NULL
#             156 LOAD_BUILD_CLASS
#             158 LOAD_CONST              11 (<code object TestPowerFlowAPI at 0x73cd945fe090, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 70>)
#             160 MAKE_FUNCTION            0
#             162 LOAD_CONST              12 ('TestPowerFlowAPI')
#             164 CALL                     2
#             172 STORE_NAME              24 (TestPowerFlowAPI)
# 
#  93         174 PUSH_NULL
#             176 LOAD_BUILD_CLASS
#             178 LOAD_CONST              13 (<code object TestAPIFactory at 0x73cd93b065b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 93>)
#             180 MAKE_FUNCTION            0
#             182 LOAD_CONST              14 ('TestAPIFactory')
#             184 CALL                     2
#             192 STORE_NAME              25 (TestAPIFactory)
#             194 RETURN_CONST             2 (None)
# 
# Disassembly of <code object MockAWTAdapter at 0x73cd93b39c50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 16>:
#               0 MAKE_CELL                0 (__class__)
# 
#  16           2 RESUME                   0
#               4 LOAD_NAME                0 (__name__)
#               6 STORE_NAME               1 (__module__)
#               8 LOAD_CONST               0 ('MockAWTAdapter')
#              10 STORE_NAME               2 (__qualname__)
# 
#  17          12 LOAD_CONST               1 ('Mock AWT adapter for testing PowerSkill layer.')
#              14 STORE_NAME               3 (__doc__)
# 
#  19          16 LOAD_CLOSURE             0 (__class__)
#              18 BUILD_TUPLE              1
#              20 LOAD_CONST               2 (<code object __init__ at 0x73cd93b1e340, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 19>)
#              22 MAKE_FUNCTION            8 (closure)
#              24 STORE_NAME               4 (__init__)
# 
#  23          26 LOAD_NAME                5 (property)
# 
#  24          28 LOAD_CONST               3 (<code object engine_name at 0x73cd93b13290, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 23>)
#              30 MAKE_FUNCTION            0
# 
#  23          32 CALL                     0
# 
#  24          40 STORE_NAME               6 (engine_name)
# 
#  27          42 LOAD_CONST               4 (<code object _do_connect at 0x73cd945fedb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 27>)
#              44 MAKE_FUNCTION            0
#              46 STORE_NAME               7 (_do_connect)
# 
#  30          48 LOAD_CONST               5 (<code object _do_disconnect at 0x73cd945feb10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 30>)
#              50 MAKE_FUNCTION            0
#              52 STORE_NAME               8 (_do_disconnect)
# 
#  33          54 LOAD_CONST               6 (<code object _do_load_model at 0x73cd93b139e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 33>)
#              56 MAKE_FUNCTION            0
#              58 STORE_NAME               9 (_do_load_model)
# 
#  36          60 LOAD_CONST               7 (<code object _do_run_simulation at 0x73cd93b31930, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 36>)
#              62 MAKE_FUNCTION            0
#              64 STORE_NAME              10 (_do_run_simulation)
# 
#  43          66 LOAD_CONST               8 (<code object _do_get_result at 0x73cd93b31730, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 43>)
#              68 MAKE_FUNCTION            0
#              70 STORE_NAME              11 (_do_get_result)
# 
#  50          72 LOAD_CONST               9 (<code object _do_validate_config at 0x73cd945fe330, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 50>)
#              74 MAKE_FUNCTION            0
#              76 STORE_NAME              12 (_do_validate_config)
#              78 LOAD_CLOSURE             0 (__class__)
#              80 COPY                     1
#              82 STORE_NAME              13 (__classcell__)
#              84 RETURN_VALUE
# 
# Disassembly of <code object __init__ at 0x73cd93b1e340, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 19>:
#               0 COPY_FREE_VARS           1
# 
#  19           2 RESUME                   0
# 
#  20           4 LOAD_GLOBAL              0 (super)
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
#  21          54 LOAD_CONST               3 (False)
#              56 LOAD_FAST                0 (self)
#              58 STORE_ATTR               3 (_connected)
#              68 RETURN_CONST             0 (None)
# 
# Disassembly of <code object engine_name at 0x73cd93b13290, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 23>:
#  23           0 RESUME                   0
# 
#  25           2 RETURN_CONST             1 ('mock')
# 
# Disassembly of <code object _do_connect at 0x73cd945fedb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 27>:
#  27           0 RESUME                   0
# 
#  28           2 LOAD_CONST               1 (True)
#               4 LOAD_FAST                0 (self)
#               6 STORE_ATTR               0 (_connected)
#              16 RETURN_CONST             0 (None)
# 
# Disassembly of <code object _do_disconnect at 0x73cd945feb10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 30>:
#  30           0 RESUME                   0
# 
#  31           2 LOAD_CONST               1 (False)
#               4 LOAD_FAST                0 (self)
#               6 STORE_ATTR               0 (_connected)
#              16 RETURN_CONST             0 (None)
# 
# Disassembly of <code object _do_load_model at 0x73cd93b139e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 33>:
#  33           0 RESUME                   0
# 
#  34           2 RETURN_CONST             1 (True)
# 
# Disassembly of <code object _do_run_simulation at 0x73cd93b31930, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 36>:
#  36           0 RESUME                   0
# 
#  37           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
#  38          12 LOAD_CONST               1 ('test-job')
# 
#  39          14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
# 
#  40          44 BUILD_LIST               0
#              46 BUILD_LIST               0
#              48 LOAD_CONST               2 (('buses', 'branches'))
#              50 BUILD_CONST_KEY_MAP      2
# 
#  37          52 KW_NAMES                 3 (('job_id', 'status', 'data'))
#              54 CALL                     3
#              62 RETURN_VALUE
# 
# Disassembly of <code object _do_get_result at 0x73cd93b31730, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 43>:
#  43           0 RESUME                   0
# 
#  44           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
#  45          12 LOAD_FAST                1 (job_id)
# 
#  46          14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
# 
#  47          44 BUILD_LIST               0
#              46 BUILD_LIST               0
#              48 LOAD_CONST               1 (('buses', 'branches'))
#              50 BUILD_CONST_KEY_MAP      2
# 
#  44          52 KW_NAMES                 2 (('job_id', 'status', 'data'))
#              54 CALL                     3
#              62 RETURN_VALUE
# 
# Disassembly of <code object _do_validate_config at 0x73cd945fe330, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 50>:
#  50           0 RESUME                   0
# 
#  51           2 LOAD_GLOBAL              1 (NULL + ValidationResult)
#              12 LOAD_CONST               1 (True)
#              14 KW_NAMES                 2 (('valid',))
#              16 CALL                     1
#              24 RETURN_VALUE
# 
# Disassembly of <code object TestSimulationAPI at 0x73cd945fc110, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 54>:
#  54           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestSimulationAPI')
#               8 STORE_NAME               2 (__qualname__)
# 
#  55          10 LOAD_CONST               1 ('Tests for SimulationAPI.')
#              12 STORE_NAME               3 (__doc__)
# 
#  57          14 LOAD_CONST               2 (<code object test_context_manager at 0x3af96e20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 57>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_context_manager)
# 
#  64          20 LOAD_CONST               3 (<code object test_engine_name at 0x3aeff050, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 64>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_engine_name)
#              26 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_context_manager at 0x3af96e20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 57>:
#  57           0 RESUME                   0
# 
#  58           2 LOAD_GLOBAL              1 (NULL + MockAWTAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
#  59          22 LOAD_GLOBAL              3 (NULL + SimulationAPI)
#              32 LOAD_FAST                1 (adapter)
#              34 CALL                     1
#              42 STORE_FAST               2 (api)
# 
#  60          44 LOAD_FAST                2 (api)
#              46 BEFORE_WITH
#              48 POP_TOP
# 
#  61          50 LOAD_FAST                2 (api)
#              52 LOAD_ATTR                4 (is_connected)
#              72 STORE_FAST               3 (@py_assert1)
#              74 LOAD_FAST                3 (@py_assert1)
#              76 POP_JUMP_IF_TRUE       121 (to 320)
#              78 LOAD_CONST               1 ('assert %(py2)s\n{%(py2)s = %(py0)s.is_connected\n}')
#              80 LOAD_CONST               2 ('api')
#              82 LOAD_GLOBAL              7 (NULL + @py_builtins)
#              92 LOAD_ATTR                8 (locals)
#             112 CALL                     0
#             120 CONTAINS_OP              0
#             122 POP_JUMP_IF_TRUE        21 (to 166)
#             124 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             134 LOAD_ATTR               12 (_should_repr_global_name)
#             154 LOAD_FAST                2 (api)
#             156 CALL                     1
#             164 POP_JUMP_IF_FALSE       21 (to 208)
#         >>  166 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             176 LOAD_ATTR               14 (_saferepr)
#             196 LOAD_FAST                2 (api)
#             198 CALL                     1
#             206 JUMP_FORWARD             1 (to 210)
#         >>  208 LOAD_CONST               2 ('api')
#         >>  210 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             220 LOAD_ATTR               14 (_saferepr)
#             240 LOAD_FAST                3 (@py_assert1)
#             242 CALL                     1
#             250 LOAD_CONST               3 (('py0', 'py2'))
#             252 BUILD_CONST_KEY_MAP      2
#             254 BINARY_OP                6 (%)
#             258 STORE_FAST               4 (@py_format3)
#             260 LOAD_GLOBAL             17 (NULL + AssertionError)
#             270 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             280 LOAD_ATTR               18 (_format_explanation)
#             300 LOAD_FAST                4 (@py_format3)
#             302 CALL                     1
#             310 CALL                     1
#             318 RAISE_VARARGS            1
#         >>  320 LOAD_CONST               0 (None)
#             322 STORE_FAST               3 (@py_assert1)
# 
#  60         324 LOAD_CONST               0 (None)
#             326 LOAD_CONST               0 (None)
#             328 LOAD_CONST               0 (None)
#             330 CALL                     2
#             338 POP_TOP
# 
#  62     >>  340 LOAD_FAST                2 (api)
#             342 LOAD_ATTR                4 (is_connected)
#             362 STORE_FAST               3 (@py_assert1)
#             364 LOAD_FAST                3 (@py_assert1)
#             366 UNARY_NOT
#             368 STORE_FAST               5 (@py_assert3)
#             370 LOAD_FAST                5 (@py_assert3)
#             372 POP_JUMP_IF_TRUE       121 (to 616)
#             374 LOAD_CONST               4 ('assert not %(py2)s\n{%(py2)s = %(py0)s.is_connected\n}')
#             376 LOAD_CONST               2 ('api')
#             378 LOAD_GLOBAL              7 (NULL + @py_builtins)
#             388 LOAD_ATTR                8 (locals)
#             408 CALL                     0
#             416 CONTAINS_OP              0
#             418 POP_JUMP_IF_TRUE        21 (to 462)
#             420 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             430 LOAD_ATTR               12 (_should_repr_global_name)
#             450 LOAD_FAST                2 (api)
#             452 CALL                     1
#             460 POP_JUMP_IF_FALSE       21 (to 504)
#         >>  462 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             472 LOAD_ATTR               14 (_saferepr)
#             492 LOAD_FAST                2 (api)
#             494 CALL                     1
#             502 JUMP_FORWARD             1 (to 506)
#         >>  504 LOAD_CONST               2 ('api')
#         >>  506 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             516 LOAD_ATTR               14 (_saferepr)
#             536 LOAD_FAST                3 (@py_assert1)
#             538 CALL                     1
#             546 LOAD_CONST               3 (('py0', 'py2'))
#             548 BUILD_CONST_KEY_MAP      2
#             550 BINARY_OP                6 (%)
#             554 STORE_FAST               6 (@py_format4)
#             556 LOAD_GLOBAL             17 (NULL + AssertionError)
#             566 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             576 LOAD_ATTR               18 (_format_explanation)
#             596 LOAD_FAST                6 (@py_format4)
#             598 CALL                     1
#             606 CALL                     1
#             614 RAISE_VARARGS            1
#         >>  616 LOAD_CONST               0 (None)
#             618 COPY                     1
#             620 STORE_FAST               3 (@py_assert1)
#             622 STORE_FAST               5 (@py_assert3)
#             624 RETURN_CONST             0 (None)
# 
#  60     >>  626 PUSH_EXC_INFO
#             628 WITH_EXCEPT_START
#             630 POP_JUMP_IF_TRUE         1 (to 634)
#             632 RERAISE                  2
#         >>  634 POP_TOP
#             636 POP_EXCEPT
#             638 POP_TOP
#             640 POP_TOP
#             642 JUMP_BACKWARD          152 (to 340)
#         >>  644 COPY                     3
#             646 POP_EXCEPT
#             648 RERAISE                  1
# ExceptionTable:
#   48 to 322 -> 626 [1] lasti
#   626 to 634 -> 644 [3] lasti
# 
# Disassembly of <code object test_engine_name at 0x3aeff050, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 64>:
#  64           0 RESUME                   0
# 
#  65           2 LOAD_GLOBAL              1 (NULL + MockAWTAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
#  66          22 LOAD_GLOBAL              3 (NULL + SimulationAPI)
#              32 LOAD_FAST                1 (adapter)
#              34 CALL                     1
#              42 STORE_FAST               2 (api)
# 
#  67          44 LOAD_FAST                2 (api)
#              46 LOAD_ATTR                4 (engine_name)
#              66 STORE_FAST               3 (@py_assert1)
#              68 LOAD_CONST               1 ('mock')
#              70 STORE_FAST               4 (@py_assert4)
#              72 LOAD_FAST                3 (@py_assert1)
#              74 LOAD_FAST                4 (@py_assert4)
#              76 COMPARE_OP              40 (==)
#              80 STORE_FAST               5 (@py_assert3)
#              82 LOAD_FAST                5 (@py_assert3)
#              84 POP_JUMP_IF_TRUE       173 (to 432)
#              86 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#              96 LOAD_ATTR                8 (_call_reprcompare)
#             116 LOAD_CONST               2 (('==',))
#             118 LOAD_FAST                5 (@py_assert3)
#             120 BUILD_TUPLE              1
#             122 LOAD_CONST               3 (('%(py2)s\n{%(py2)s = %(py0)s.engine_name\n} == %(py5)s',))
#             124 LOAD_FAST                3 (@py_assert1)
#             126 LOAD_FAST                4 (@py_assert4)
#             128 BUILD_TUPLE              2
#             130 CALL                     4
#             138 LOAD_CONST               4 ('api')
#             140 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             150 LOAD_ATTR               12 (locals)
#             170 CALL                     0
#             178 CONTAINS_OP              0
#             180 POP_JUMP_IF_TRUE        21 (to 224)
#             182 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             192 LOAD_ATTR               14 (_should_repr_global_name)
#             212 LOAD_FAST                2 (api)
#             214 CALL                     1
#             222 POP_JUMP_IF_FALSE       21 (to 266)
#         >>  224 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             234 LOAD_ATTR               16 (_saferepr)
#             254 LOAD_FAST                2 (api)
#             256 CALL                     1
#             264 JUMP_FORWARD             1 (to 268)
#         >>  266 LOAD_CONST               4 ('api')
#         >>  268 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             278 LOAD_ATTR               16 (_saferepr)
#             298 LOAD_FAST                3 (@py_assert1)
#             300 CALL                     1
#             308 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             318 LOAD_ATTR               16 (_saferepr)
#             338 LOAD_FAST                4 (@py_assert4)
#             340 CALL                     1
#             348 LOAD_CONST               5 (('py0', 'py2', 'py5'))
#             350 BUILD_CONST_KEY_MAP      3
#             352 BINARY_OP                6 (%)
#             356 STORE_FAST               6 (@py_format6)
#             358 LOAD_CONST               6 ('assert %(py7)s')
#             360 LOAD_CONST               7 ('py7')
#             362 LOAD_FAST                6 (@py_format6)
#             364 BUILD_MAP                1
#             366 BINARY_OP                6 (%)
#             370 STORE_FAST               7 (@py_format8)
#             372 LOAD_GLOBAL             19 (NULL + AssertionError)
#             382 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             392 LOAD_ATTR               20 (_format_explanation)
#             412 LOAD_FAST                7 (@py_format8)
#             414 CALL                     1
#             422 CALL                     1
#             430 RAISE_VARARGS            1
#         >>  432 LOAD_CONST               0 (None)
#             434 COPY                     1
#             436 STORE_FAST               3 (@py_assert1)
#             438 COPY                     1
#             440 STORE_FAST               5 (@py_assert3)
#             442 STORE_FAST               4 (@py_assert4)
#             444 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestPowerFlowAPI at 0x73cd945fe090, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 70>:
#  70           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestPowerFlowAPI')
#               8 STORE_NAME               2 (__qualname__)
# 
#  71          10 LOAD_CONST               1 ('Tests for PowerFlowAPI.')
#              12 STORE_NAME               3 (__doc__)
# 
#  73          14 LOAD_CONST               2 (<code object test_run_power_flow at 0x3af94600, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 73>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_run_power_flow)
# 
#  81          20 LOAD_CONST               3 (<code object test_get_bus_voltages at 0x3af977e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 81>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_get_bus_voltages)
#              26 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_run_power_flow at 0x3af94600, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 73>:
#  73           0 RESUME                   0
# 
#  74           2 LOAD_GLOBAL              1 (NULL + MockAWTAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
#  75          22 LOAD_GLOBAL              3 (NULL + PowerFlowAPI)
#              32 LOAD_FAST                1 (adapter)
#              34 CALL                     1
#              42 STORE_FAST               2 (api)
# 
#  76          44 LOAD_FAST                2 (api)
#              46 LOAD_ATTR                5 (NULL|self + connect)
#              66 CALL                     0
#              74 POP_TOP
# 
#  77          76 LOAD_FAST                2 (api)
#              78 LOAD_ATTR                7 (NULL|self + run_power_flow)
#              98 LOAD_CONST               1 ('test-model')
#             100 KW_NAMES                 2 (('model_id',))
#             102 CALL                     1
#             110 STORE_FAST               3 (result)
# 
#  78         112 LOAD_FAST                3 (result)
#             114 LOAD_ATTR                8 (status)
#             134 STORE_FAST               4 (@py_assert1)
#             136 LOAD_GLOBAL             10 (SimulationStatus)
#             146 LOAD_ATTR               12 (COMPLETED)
#             166 STORE_FAST               5 (@py_assert5)
#             168 LOAD_FAST                4 (@py_assert1)
#             170 LOAD_FAST                5 (@py_assert5)
#             172 COMPARE_OP              40 (==)
#             176 STORE_FAST               6 (@py_assert3)
#             178 LOAD_FAST                6 (@py_assert3)
#             180 POP_JUMP_IF_TRUE       246 (to 674)
#             182 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             192 LOAD_ATTR               16 (_call_reprcompare)
#             212 LOAD_CONST               3 (('==',))
#             214 LOAD_FAST                6 (@py_assert3)
#             216 BUILD_TUPLE              1
#             218 LOAD_CONST               4 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.COMPLETED\n}',))
#             220 LOAD_FAST                4 (@py_assert1)
#             222 LOAD_FAST                5 (@py_assert5)
#             224 BUILD_TUPLE              2
#             226 CALL                     4
#             234 LOAD_CONST               5 ('result')
#             236 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             246 LOAD_ATTR               20 (locals)
#             266 CALL                     0
#             274 CONTAINS_OP              0
#             276 POP_JUMP_IF_TRUE        21 (to 320)
#             278 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             288 LOAD_ATTR               22 (_should_repr_global_name)
#             308 LOAD_FAST                3 (result)
#             310 CALL                     1
#             318 POP_JUMP_IF_FALSE       21 (to 362)
#         >>  320 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             330 LOAD_ATTR               24 (_saferepr)
#             350 LOAD_FAST                3 (result)
#             352 CALL                     1
#             360 JUMP_FORWARD             1 (to 364)
#         >>  362 LOAD_CONST               5 ('result')
#         >>  364 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             374 LOAD_ATTR               24 (_saferepr)
#             394 LOAD_FAST                4 (@py_assert1)
#             396 CALL                     1
#             404 LOAD_CONST               6 ('SimulationStatus')
#             406 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             416 LOAD_ATTR               20 (locals)
#             436 CALL                     0
#             444 CONTAINS_OP              0
#             446 POP_JUMP_IF_TRUE        25 (to 498)
#             448 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             458 LOAD_ATTR               22 (_should_repr_global_name)
#             478 LOAD_GLOBAL             10 (SimulationStatus)
#             488 CALL                     1
#             496 POP_JUMP_IF_FALSE       25 (to 548)
#         >>  498 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             508 LOAD_ATTR               24 (_saferepr)
#             528 LOAD_GLOBAL             10 (SimulationStatus)
#             538 CALL                     1
#             546 JUMP_FORWARD             1 (to 550)
#         >>  548 LOAD_CONST               6 ('SimulationStatus')
#         >>  550 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             560 LOAD_ATTR               24 (_saferepr)
#             580 LOAD_FAST                5 (@py_assert5)
#             582 CALL                     1
#             590 LOAD_CONST               7 (('py0', 'py2', 'py4', 'py6'))
#             592 BUILD_CONST_KEY_MAP      4
#             594 BINARY_OP                6 (%)
#             598 STORE_FAST               7 (@py_format7)
#             600 LOAD_CONST               8 ('assert %(py8)s')
#             602 LOAD_CONST               9 ('py8')
#             604 LOAD_FAST                7 (@py_format7)
#             606 BUILD_MAP                1
#             608 BINARY_OP                6 (%)
#             612 STORE_FAST               8 (@py_format9)
#             614 LOAD_GLOBAL             27 (NULL + AssertionError)
#             624 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             634 LOAD_ATTR               28 (_format_explanation)
#             654 LOAD_FAST                8 (@py_format9)
#             656 CALL                     1
#             664 CALL                     1
#             672 RAISE_VARARGS            1
#         >>  674 LOAD_CONST               0 (None)
#             676 COPY                     1
#             678 STORE_FAST               4 (@py_assert1)
#             680 COPY                     1
#             682 STORE_FAST               6 (@py_assert3)
#             684 STORE_FAST               5 (@py_assert5)
# 
#  79         686 LOAD_FAST                2 (api)
#             688 LOAD_ATTR               31 (NULL|self + disconnect)
#             708 CALL                     0
#             716 POP_TOP
#             718 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_get_bus_voltages at 0x3af977e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 81>:
#  81           0 RESUME                   0
# 
#  82           2 LOAD_GLOBAL              1 (NULL + MockAWTAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
#  83          22 LOAD_GLOBAL              3 (NULL + PowerFlowAPI)
#              32 LOAD_FAST                1 (adapter)
#              34 CALL                     1
#              42 STORE_FAST               2 (api)
# 
#  84          44 LOAD_GLOBAL              5 (NULL + SimulationResult)
# 
#  85          54 LOAD_CONST               1 ('test')
# 
#  86          56 LOAD_GLOBAL              6 (SimulationStatus)
#              66 LOAD_ATTR                8 (COMPLETED)
# 
#  87          86 LOAD_CONST               2 ('buses')
#              88 LOAD_CONST               3 (1)
#              90 LOAD_CONST               4 (1.0)
#              92 LOAD_CONST               5 (('id', 'voltage'))
#              94 BUILD_CONST_KEY_MAP      2
#              96 BUILD_LIST               1
#              98 BUILD_MAP                1
# 
#  84         100 KW_NAMES                 6 (('job_id', 'status', 'data'))
#             102 CALL                     3
#             110 STORE_FAST               3 (result)
# 
#  89         112 LOAD_FAST                2 (api)
#             114 LOAD_ATTR               11 (NULL|self + get_bus_voltages)
#             134 LOAD_FAST                3 (result)
#             136 CALL                     1
#             144 STORE_FAST               4 (voltages)
# 
#  90         146 LOAD_GLOBAL             13 (NULL + len)
#             156 LOAD_FAST                4 (voltages)
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
#         >>  384 LOAD_CONST              10 ('voltages')
#             386 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             396 LOAD_ATTR               20 (locals)
#             416 CALL                     0
#             424 CONTAINS_OP              0
#             426 POP_JUMP_IF_TRUE        21 (to 470)
#             428 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             438 LOAD_ATTR               22 (_should_repr_global_name)
#             458 LOAD_FAST                4 (voltages)
#             460 CALL                     1
#             468 POP_JUMP_IF_FALSE       21 (to 512)
#         >>  470 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             480 LOAD_ATTR               24 (_saferepr)
#             500 LOAD_FAST                4 (voltages)
#             502 CALL                     1
#             510 JUMP_FORWARD             1 (to 514)
#         >>  512 LOAD_CONST              10 ('voltages')
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
#             690 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestAPIFactory at 0x73cd93b065b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 93>:
#  93           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestAPIFactory')
#               8 STORE_NAME               2 (__qualname__)
# 
#  94          10 LOAD_CONST               1 ('Tests for APIFactory.')
#              12 STORE_NAME               3 (__doc__)
# 
#  96          14 LOAD_CONST               2 (<code object test_create_powerflow_api at 0x3af9b9b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 96>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_create_powerflow_api)
# 
# 100          20 LOAD_CONST               3 (<code object test_list_engines at 0x3af23100, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 100>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_list_engines)
# 
# 104          26 LOAD_CONST               4 (<code object test_register_adapter at 0x3af3a060, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 104>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_register_adapter)
#              32 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_create_powerflow_api at 0x3af9b9b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 96>:
#  96           0 RESUME                   0
# 
#  97           2 LOAD_GLOBAL              1 (NULL + APIFactory)
#              12 LOAD_ATTR                2 (create_powerflow_api)
#              32 LOAD_CONST               1 ('cloudpss')
#              34 KW_NAMES                 2 (('engine',))
#              36 CALL                     1
#              44 STORE_FAST               1 (api)
# 
#  98          46 LOAD_GLOBAL              5 (NULL + isinstance)
#              56 LOAD_FAST                1 (api)
#              58 LOAD_GLOBAL              6 (PowerFlowAPI)
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
#         >>  362 LOAD_CONST               6 ('PowerFlowAPI')
#             364 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             374 LOAD_ATTR               10 (locals)
#             394 CALL                     0
#             402 CONTAINS_OP              0
#             404 POP_JUMP_IF_TRUE        25 (to 456)
#             406 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             416 LOAD_ATTR               14 (_should_repr_global_name)
#             436 LOAD_GLOBAL              6 (PowerFlowAPI)
#             446 CALL                     1
#             454 POP_JUMP_IF_FALSE       25 (to 506)
#         >>  456 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             466 LOAD_ATTR               16 (_saferepr)
#             486 LOAD_GLOBAL              6 (PowerFlowAPI)
#             496 CALL                     1
#             504 JUMP_FORWARD             1 (to 508)
#         >>  506 LOAD_CONST               6 ('PowerFlowAPI')
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
# Disassembly of <code object test_list_engines at 0x3af23100, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 100>:
# 100           0 RESUME                   0
# 
# 101           2 LOAD_GLOBAL              1 (NULL + APIFactory)
#              12 LOAD_ATTR                2 (list_engines)
#              32 LOAD_CONST               1 ('power_flow')
#              34 CALL                     1
#              42 STORE_FAST               1 (engines)
# 
# 102          44 LOAD_CONST               2 ('cloudpss')
#              46 STORE_FAST               2 (@py_assert0)
#              48 LOAD_FAST                2 (@py_assert0)
#              50 LOAD_FAST                1 (engines)
#              52 CONTAINS_OP              0
#              54 STORE_FAST               3 (@py_assert2)
#              56 LOAD_FAST                3 (@py_assert2)
#              58 POP_JUMP_IF_TRUE       153 (to 366)
#              60 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              70 LOAD_ATTR                6 (_call_reprcompare)
#              90 LOAD_CONST               3 (('in',))
#              92 LOAD_FAST                3 (@py_assert2)
#              94 BUILD_TUPLE              1
#              96 LOAD_CONST               4 (('%(py1)s in %(py3)s',))
#              98 LOAD_FAST                2 (@py_assert0)
#             100 LOAD_FAST                1 (engines)
#             102 BUILD_TUPLE              2
#             104 CALL                     4
#             112 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             122 LOAD_ATTR                8 (_saferepr)
#             142 LOAD_FAST                2 (@py_assert0)
#             144 CALL                     1
#             152 LOAD_CONST               5 ('engines')
#             154 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             164 LOAD_ATTR               12 (locals)
#             184 CALL                     0
#             192 CONTAINS_OP              0
#             194 POP_JUMP_IF_TRUE        21 (to 238)
#             196 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             206 LOAD_ATTR               14 (_should_repr_global_name)
#             226 LOAD_FAST                1 (engines)
#             228 CALL                     1
#             236 POP_JUMP_IF_FALSE       21 (to 280)
#         >>  238 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             248 LOAD_ATTR                8 (_saferepr)
#             268 LOAD_FAST                1 (engines)
#             270 CALL                     1
#             278 JUMP_FORWARD             1 (to 282)
#         >>  280 LOAD_CONST               5 ('engines')
#         >>  282 LOAD_CONST               6 (('py1', 'py3'))
#             284 BUILD_CONST_KEY_MAP      2
#             286 BINARY_OP                6 (%)
#             290 STORE_FAST               4 (@py_format4)
#             292 LOAD_CONST               7 ('assert %(py5)s')
#             294 LOAD_CONST               8 ('py5')
#             296 LOAD_FAST                4 (@py_format4)
#             298 BUILD_MAP                1
#             300 BINARY_OP                6 (%)
#             304 STORE_FAST               5 (@py_format6)
#             306 LOAD_GLOBAL             17 (NULL + AssertionError)
#             316 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             326 LOAD_ATTR               18 (_format_explanation)
#             346 LOAD_FAST                5 (@py_format6)
#             348 CALL                     1
#             356 CALL                     1
#             364 RAISE_VARARGS            1
#         >>  366 LOAD_CONST               0 (None)
#             368 COPY                     1
#             370 STORE_FAST               2 (@py_assert0)
#             372 STORE_FAST               3 (@py_assert2)
#             374 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_register_adapter at 0x3af3a060, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 104>:
# 104           0 RESUME                   0
# 
# 105           2 PUSH_NULL
#               4 LOAD_BUILD_CLASS
#               6 LOAD_CONST               1 (<code object CustomAdapter at 0x73cd93b31a30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 105>)
#               8 MAKE_FUNCTION            0
#              10 LOAD_CONST               2 ('CustomAdapter')
#              12 LOAD_GLOBAL              0 (EngineAdapter)
#              22 CALL                     3
#              30 STORE_FAST               1 (CustomAdapter)
# 
# 130          32 LOAD_GLOBAL              3 (NULL + APIFactory)
#              42 LOAD_ATTR                4 (register_adapter)
#              62 LOAD_CONST               3 ('power_flow')
#              64 LOAD_CONST               4 ('custom')
#              66 LOAD_FAST                1 (CustomAdapter)
#              68 CALL                     3
#              76 POP_TOP
# 
# 131          78 LOAD_GLOBAL              3 (NULL + APIFactory)
#              88 LOAD_ATTR                6 (list_engines)
#             108 LOAD_CONST               3 ('power_flow')
#             110 CALL                     1
#             118 STORE_FAST               2 (engines)
# 
# 132         120 LOAD_CONST               4 ('custom')
#             122 STORE_FAST               3 (@py_assert0)
#             124 LOAD_FAST                3 (@py_assert0)
#             126 LOAD_FAST                2 (engines)
#             128 CONTAINS_OP              0
#             130 STORE_FAST               4 (@py_assert2)
#             132 LOAD_FAST                4 (@py_assert2)
#             134 POP_JUMP_IF_TRUE       153 (to 442)
#             136 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             146 LOAD_ATTR               10 (_call_reprcompare)
#             166 LOAD_CONST               5 (('in',))
#             168 LOAD_FAST                4 (@py_assert2)
#             170 BUILD_TUPLE              1
#             172 LOAD_CONST               6 (('%(py1)s in %(py3)s',))
#             174 LOAD_FAST                3 (@py_assert0)
#             176 LOAD_FAST                2 (engines)
#             178 BUILD_TUPLE              2
#             180 CALL                     4
#             188 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             198 LOAD_ATTR               12 (_saferepr)
#             218 LOAD_FAST                3 (@py_assert0)
#             220 CALL                     1
#             228 LOAD_CONST               7 ('engines')
#             230 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             240 LOAD_ATTR               16 (locals)
#             260 CALL                     0
#             268 CONTAINS_OP              0
#             270 POP_JUMP_IF_TRUE        21 (to 314)
#             272 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             282 LOAD_ATTR               18 (_should_repr_global_name)
#             302 LOAD_FAST                2 (engines)
#             304 CALL                     1
#             312 POP_JUMP_IF_FALSE       21 (to 356)
#         >>  314 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             324 LOAD_ATTR               12 (_saferepr)
#             344 LOAD_FAST                2 (engines)
#             346 CALL                     1
#             354 JUMP_FORWARD             1 (to 358)
#         >>  356 LOAD_CONST               7 ('engines')
#         >>  358 LOAD_CONST               8 (('py1', 'py3'))
#             360 BUILD_CONST_KEY_MAP      2
#             362 BINARY_OP                6 (%)
#             366 STORE_FAST               5 (@py_format4)
#             368 LOAD_CONST               9 ('assert %(py5)s')
#             370 LOAD_CONST              10 ('py5')
#             372 LOAD_FAST                5 (@py_format4)
#             374 BUILD_MAP                1
#             376 BINARY_OP                6 (%)
#             380 STORE_FAST               6 (@py_format6)
#             382 LOAD_GLOBAL             21 (NULL + AssertionError)
#             392 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             402 LOAD_ATTR               22 (_format_explanation)
#             422 LOAD_FAST                6 (@py_format6)
#             424 CALL                     1
#             432 CALL                     1
#             440 RAISE_VARARGS            1
#         >>  442 LOAD_CONST               0 (None)
#             444 COPY                     1
#             446 STORE_FAST               3 (@py_assert0)
#             448 STORE_FAST               4 (@py_assert2)
#             450 RETURN_CONST             0 (None)
# 
# Disassembly of <code object CustomAdapter at 0x73cd93b31a30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 105>:
# 105           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestAPIFactory.test_register_adapter.<locals>.CustomAdapter')
#               8 STORE_NAME               2 (__qualname__)
# 
# 106          10 LOAD_NAME                3 (property)
# 
# 107          12 LOAD_CONST               1 (<code object engine_name at 0x73cd93b13840, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 106>)
#              14 MAKE_FUNCTION            0
# 
# 106          16 CALL                     0
# 
# 107          24 STORE_NAME               4 (engine_name)
# 
# 110          26 LOAD_CONST               2 (<code object _do_connect at 0x73cd93b13910, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 110>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               5 (_do_connect)
# 
# 113          32 LOAD_CONST               3 (<code object _do_disconnect at 0x73cd93b13360, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 113>)
#              34 MAKE_FUNCTION            0
#              36 STORE_NAME               6 (_do_disconnect)
# 
# 116          38 LOAD_CONST               4 (<code object _do_load_model at 0x73cd93b13500, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 116>)
#              40 MAKE_FUNCTION            0
#              42 STORE_NAME               7 (_do_load_model)
# 
# 119          44 LOAD_CONST               5 (<code object _do_run_simulation at 0x73cd93b31630, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 119>)
#              46 MAKE_FUNCTION            0
#              48 STORE_NAME               8 (_do_run_simulation)
# 
# 122          50 LOAD_CONST               6 (<code object _do_get_result at 0x73cd93b31230, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 122>)
#              52 MAKE_FUNCTION            0
#              54 STORE_NAME               9 (_do_get_result)
# 
# 127          56 LOAD_CONST               7 (<code object _do_validate_config at 0x73cd945fdfb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 127>)
#              58 MAKE_FUNCTION            0
#              60 STORE_NAME              10 (_do_validate_config)
#              62 RETURN_CONST             8 (None)
# 
# Disassembly of <code object engine_name at 0x73cd93b13840, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 106>:
# 106           0 RESUME                   0
# 
# 108           2 RETURN_CONST             1 ('custom')
# 
# Disassembly of <code object _do_connect at 0x73cd93b13910, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 110>:
# 110           0 RESUME                   0
# 
# 111           2 RETURN_CONST             0 (None)
# 
# Disassembly of <code object _do_disconnect at 0x73cd93b13360, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 113>:
# 113           0 RESUME                   0
# 
# 114           2 RETURN_CONST             0 (None)
# 
# Disassembly of <code object _do_load_model at 0x73cd93b13500, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 116>:
# 116           0 RESUME                   0
# 
# 117           2 RETURN_CONST             1 (True)
# 
# Disassembly of <code object _do_run_simulation at 0x73cd93b31630, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 119>:
# 119           0 RESUME                   0
# 
# 120           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
#              12 LOAD_CONST               1 ('x')
#              14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
#              44 KW_NAMES                 2 (('job_id', 'status'))
#              46 CALL                     2
#              54 RETURN_VALUE
# 
# Disassembly of <code object _do_get_result at 0x73cd93b31230, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 122>:
# 122           0 RESUME                   0
# 
# 123           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
# 124          12 LOAD_FAST                1 (job_id)
#              14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
# 
# 123          44 KW_NAMES                 1 (('job_id', 'status'))
#              46 CALL                     2
#              54 RETURN_VALUE
# 
# Disassembly of <code object _do_validate_config at 0x73cd945fdfb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerskill_tests/test_apis.py", line 127>:
# 127           0 RESUME                   0
# 
# 128           2 LOAD_GLOBAL              1 (NULL + ValidationResult)
#              12 LOAD_CONST               1 (True)
#              14 KW_NAMES                 2 (('valid',))
#              16 CALL                     1
#              24 RETURN_VALUE
# 