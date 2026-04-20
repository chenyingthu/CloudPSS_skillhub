# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/__pycache__/test_base.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


class MockAdapter:
    """MockAdapter"""
    def __init__(self, config):
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


def TestValidationResult():
    """TestValidationResult"""
pass  # TODO: restore


def TestSimulationResult():
    """TestSimulationResult"""
pass  # TODO: restore


def TestEngineAdapter():
    """TestEngineAdapter"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('Tests for powerAPI Layer base classes.')
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
#              42 LOAD_CONST               3 (('SimulationStatus', 'SimulationType', 'ValidationError', 'ValidationResult', 'SimulationResult', 'EngineConfig', 'EngineAdapter'))
#              44 IMPORT_NAME              8 (cloudpss_skills_v2.powerapi)
#              46 IMPORT_FROM              9 (SimulationStatus)
#              48 STORE_NAME               9 (SimulationStatus)
#              50 IMPORT_FROM             10 (SimulationType)
#              52 STORE_NAME              10 (SimulationType)
#              54 IMPORT_FROM             11 (ValidationError)
#              56 STORE_NAME              11 (ValidationError)
#              58 IMPORT_FROM             12 (ValidationResult)
#              60 STORE_NAME              12 (ValidationResult)
#              62 IMPORT_FROM             13 (SimulationResult)
#              64 STORE_NAME              13 (SimulationResult)
#              66 IMPORT_FROM             14 (EngineConfig)
#              68 STORE_NAME              14 (EngineConfig)
#              70 IMPORT_FROM             15 (EngineAdapter)
#              72 STORE_NAME              15 (EngineAdapter)
#              74 POP_TOP
# 
#  15          76 PUSH_NULL
#              78 LOAD_BUILD_CLASS
#              80 LOAD_CONST               4 (<code object MockAdapter at 0x73cd93b398f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 15>)
#              82 MAKE_FUNCTION            0
#              84 LOAD_CONST               5 ('MockAdapter')
#              86 LOAD_NAME               15 (EngineAdapter)
#              88 CALL                     3
#              96 STORE_NAME              16 (MockAdapter)
# 
#  58          98 PUSH_NULL
#             100 LOAD_BUILD_CLASS
#             102 LOAD_CONST               6 (<code object TestValidationResult at 0x73cd93b064c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 58>)
#             104 MAKE_FUNCTION            0
#             106 LOAD_CONST               7 ('TestValidationResult')
#             108 CALL                     2
#             116 STORE_NAME              17 (TestValidationResult)
# 
#  80         118 PUSH_NULL
#             120 LOAD_BUILD_CLASS
#             122 LOAD_CONST               8 (<code object TestSimulationResult at 0x73cd93b065b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 80>)
#             124 MAKE_FUNCTION            0
#             126 LOAD_CONST               9 ('TestSimulationResult')
#             128 CALL                     2
#             136 STORE_NAME              18 (TestSimulationResult)
# 
# 105         138 PUSH_NULL
#             140 LOAD_BUILD_CLASS
#             142 LOAD_CONST              10 (<code object TestEngineAdapter at 0x73cd93b06880, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 105>)
#             144 MAKE_FUNCTION            0
#             146 LOAD_CONST              11 ('TestEngineAdapter')
#             148 CALL                     2
#             156 STORE_NAME              19 (TestEngineAdapter)
#             158 RETURN_CONST             2 (None)
# 
# Disassembly of <code object MockAdapter at 0x73cd93b398f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 15>:
#               0 MAKE_CELL                0 (__class__)
# 
#  15           2 RESUME                   0
#               4 LOAD_NAME                0 (__name__)
#               6 STORE_NAME               1 (__module__)
#               8 LOAD_CONST               0 ('MockAdapter')
#              10 STORE_NAME               2 (__qualname__)
# 
#  16          12 LOAD_CONST               1 ('Mock adapter for testing.')
#              14 STORE_NAME               3 (__doc__)
# 
#  18          16 LOAD_CONST              10 ((None,))
#              18 LOAD_CLOSURE             0 (__class__)
#              20 BUILD_TUPLE              1
#              22 LOAD_CONST               2 (<code object __init__ at 0x73cd93b39c50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 18>)
#              24 MAKE_FUNCTION            9 (defaults, closure)
#              26 STORE_NAME               4 (__init__)
# 
#  23          28 LOAD_NAME                5 (property)
# 
#  24          30 LOAD_CONST               3 (<code object engine_name at 0x73cd93b130f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 23>)
#              32 MAKE_FUNCTION            0
# 
#  23          34 CALL                     0
# 
#  24          42 STORE_NAME               6 (engine_name)
# 
#  27          44 LOAD_CONST               4 (<code object _do_connect at 0x73cd93b06790, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 27>)
#              46 MAKE_FUNCTION            0
#              48 STORE_NAME               7 (_do_connect)
# 
#  30          50 LOAD_CONST               5 (<code object _do_disconnect at 0x73cd93b066a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 30>)
#              52 MAKE_FUNCTION            0
#              54 STORE_NAME               8 (_do_disconnect)
# 
#  33          56 LOAD_CONST               6 (<code object _do_load_model at 0x73cd93b13290, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 33>)
#              58 MAKE_FUNCTION            0
#              60 STORE_NAME               9 (_do_load_model)
# 
#  36          62 LOAD_CONST               7 (<code object _do_run_simulation at 0x73cd93b31830, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 36>)
#              64 MAKE_FUNCTION            0
#              66 STORE_NAME              10 (_do_run_simulation)
# 
#  43          68 LOAD_CONST               8 (<code object _do_get_result at 0x73cd93b31930, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 43>)
#              70 MAKE_FUNCTION            0
#              72 STORE_NAME              11 (_do_get_result)
# 
#  50          74 LOAD_CONST               9 (<code object _do_validate_config at 0x73cd945b92f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 50>)
#              76 MAKE_FUNCTION            0
#              78 STORE_NAME              12 (_do_validate_config)
#              80 LOAD_CLOSURE             0 (__class__)
#              82 COPY                     1
#              84 STORE_NAME              13 (__classcell__)
#              86 RETURN_VALUE
# 
# Disassembly of <code object __init__ at 0x73cd93b39c50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 18>:
#               0 COPY_FREE_VARS           1
# 
#  18           2 RESUME                   0
# 
#  19           4 LOAD_GLOBAL              0 (super)
#              14 LOAD_DEREF               2 (__class__)
#              16 LOAD_FAST                0 (self)
#              18 LOAD_SUPER_ATTR          5 (NULL|self + __init__)
#              22 LOAD_FAST                1 (config)
#              24 COPY                     1
#              26 POP_JUMP_IF_TRUE        12 (to 52)
#              28 POP_TOP
#              30 LOAD_GLOBAL              5 (NULL + EngineConfig)
#              40 LOAD_CONST               1 ('mock')
#              42 KW_NAMES                 2 (('engine_name',))
#              44 CALL                     1
#         >>   52 CALL                     1
#              60 POP_TOP
# 
#  20          62 LOAD_CONST               3 (0)
#              64 LOAD_FAST                0 (self)
#              66 STORE_ATTR               3 (_connect_count)
# 
#  21          76 LOAD_CONST               3 (0)
#              78 LOAD_FAST                0 (self)
#              80 STORE_ATTR               4 (_disconnect_count)
#              90 RETURN_CONST             0 (None)
# 
# Disassembly of <code object engine_name at 0x73cd93b130f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 23>:
#  23           0 RESUME                   0
# 
#  25           2 RETURN_CONST             1 ('mock')
# 
# Disassembly of <code object _do_connect at 0x73cd93b06790, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 27>:
#  27           0 RESUME                   0
# 
#  28           2 LOAD_FAST                0 (self)
#               4 COPY                     1
#               6 LOAD_ATTR                0 (_connect_count)
#              26 LOAD_CONST               1 (1)
#              28 BINARY_OP               13 (+=)
#              32 SWAP                     2
#              34 STORE_ATTR               0 (_connect_count)
#              44 RETURN_CONST             0 (None)
# 
# Disassembly of <code object _do_disconnect at 0x73cd93b066a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 30>:
#  30           0 RESUME                   0
# 
#  31           2 LOAD_FAST                0 (self)
#               4 COPY                     1
#               6 LOAD_ATTR                0 (_disconnect_count)
#              26 LOAD_CONST               1 (1)
#              28 BINARY_OP               13 (+=)
#              32 SWAP                     2
#              34 STORE_ATTR               0 (_disconnect_count)
#              44 RETURN_CONST             0 (None)
# 
# Disassembly of <code object _do_load_model at 0x73cd93b13290, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 33>:
#  33           0 RESUME                   0
# 
#  34           2 RETURN_CONST             1 (True)
# 
# Disassembly of <code object _do_run_simulation at 0x73cd93b31830, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 36>:
#  36           0 RESUME                   0
# 
#  37           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
#  38          12 LOAD_CONST               1 ('test-job')
# 
#  39          14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
# 
#  40          44 LOAD_CONST               2 ('result')
#              46 LOAD_CONST               3 ('success')
#              48 BUILD_MAP                1
# 
#  37          50 KW_NAMES                 4 (('job_id', 'status', 'data'))
#              52 CALL                     3
#              60 RETURN_VALUE
# 
# Disassembly of <code object _do_get_result at 0x73cd93b31930, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 43>:
#  43           0 RESUME                   0
# 
#  44           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
#  45          12 LOAD_FAST                1 (job_id)
# 
#  46          14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
# 
#  47          44 LOAD_CONST               1 ('result')
#              46 LOAD_CONST               2 ('fetched')
#              48 BUILD_MAP                1
# 
#  44          50 KW_NAMES                 3 (('job_id', 'status', 'data'))
#              52 CALL                     3
#              60 RETURN_VALUE
# 
# Disassembly of <code object _do_validate_config at 0x73cd945b92f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 50>:
#  50           0 RESUME                   0
# 
#  51           2 LOAD_CONST               1 ('invalid')
#               4 LOAD_FAST                1 (config)
#               6 CONTAINS_OP              0
#               8 POP_JUMP_IF_FALSE       33 (to 76)
# 
#  52          10 LOAD_GLOBAL              1 (NULL + ValidationResult)
#              20 LOAD_ATTR                2 (failure)
# 
#  53          40 LOAD_GLOBAL              5 (NULL + ValidationError)
#              50 LOAD_CONST               1 ('invalid')
#              52 LOAD_CONST               2 ('invalid config')
#              54 KW_NAMES                 3 (('field', 'message'))
#              56 CALL                     2
#              64 BUILD_LIST               1
# 
#  52          66 CALL                     1
#              74 RETURN_VALUE
# 
#  55     >>   76 LOAD_GLOBAL              1 (NULL + ValidationResult)
#              86 LOAD_ATTR                6 (success)
#             106 CALL                     0
#             114 RETURN_VALUE
# 
# Disassembly of <code object TestValidationResult at 0x73cd93b064c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 58>:
#  58           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestValidationResult')
#               8 STORE_NAME               2 (__qualname__)
# 
#  59          10 LOAD_CONST               1 ('Tests for ValidationResult.')
#              12 STORE_NAME               3 (__doc__)
# 
#  61          14 LOAD_CONST               2 (<code object test_success at 0x3afa3150, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 61>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_success)
# 
#  66          20 LOAD_CONST               3 (<code object test_failure_with_tuple at 0x3af9bec0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 66>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_failure_with_tuple)
# 
#  72          26 LOAD_CONST               4 (<code object test_failure_with_validation_error at 0x3af9c980, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 72>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_failure_with_validation_error)
#              32 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_success at 0x3afa3150, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 61>:
#  61           0 RESUME                   0
# 
#  62           2 LOAD_GLOBAL              1 (NULL + ValidationResult)
#              12 LOAD_ATTR                2 (success)
#              32 CALL                     0
#              40 STORE_FAST               1 (result)
# 
#  63          42 LOAD_FAST                1 (result)
#              44 LOAD_ATTR                4 (valid)
#              64 STORE_FAST               2 (@py_assert1)
#              66 LOAD_CONST               1 (True)
#              68 STORE_FAST               3 (@py_assert4)
#              70 LOAD_FAST                2 (@py_assert1)
#              72 LOAD_FAST                3 (@py_assert4)
#              74 IS_OP                    0
#              76 STORE_FAST               4 (@py_assert3)
#              78 LOAD_FAST                4 (@py_assert3)
#              80 POP_JUMP_IF_TRUE       173 (to 428)
#              82 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#              92 LOAD_ATTR                8 (_call_reprcompare)
#             112 LOAD_CONST               2 (('is',))
#             114 LOAD_FAST                4 (@py_assert3)
#             116 BUILD_TUPLE              1
#             118 LOAD_CONST               3 (('%(py2)s\n{%(py2)s = %(py0)s.valid\n} is %(py5)s',))
#             120 LOAD_FAST                2 (@py_assert1)
#             122 LOAD_FAST                3 (@py_assert4)
#             124 BUILD_TUPLE              2
#             126 CALL                     4
#             134 LOAD_CONST               4 ('result')
#             136 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             146 LOAD_ATTR               12 (locals)
#             166 CALL                     0
#             174 CONTAINS_OP              0
#             176 POP_JUMP_IF_TRUE        21 (to 220)
#             178 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             188 LOAD_ATTR               14 (_should_repr_global_name)
#             208 LOAD_FAST                1 (result)
#             210 CALL                     1
#             218 POP_JUMP_IF_FALSE       21 (to 262)
#         >>  220 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             230 LOAD_ATTR               16 (_saferepr)
#             250 LOAD_FAST                1 (result)
#             252 CALL                     1
#             260 JUMP_FORWARD             1 (to 264)
#         >>  262 LOAD_CONST               4 ('result')
#         >>  264 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             274 LOAD_ATTR               16 (_saferepr)
#             294 LOAD_FAST                2 (@py_assert1)
#             296 CALL                     1
#             304 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             314 LOAD_ATTR               16 (_saferepr)
#             334 LOAD_FAST                3 (@py_assert4)
#             336 CALL                     1
#             344 LOAD_CONST               5 (('py0', 'py2', 'py5'))
#             346 BUILD_CONST_KEY_MAP      3
#             348 BINARY_OP                6 (%)
#             352 STORE_FAST               5 (@py_format6)
#             354 LOAD_CONST               6 ('assert %(py7)s')
#             356 LOAD_CONST               7 ('py7')
#             358 LOAD_FAST                5 (@py_format6)
#             360 BUILD_MAP                1
#             362 BINARY_OP                6 (%)
#             366 STORE_FAST               6 (@py_format8)
#             368 LOAD_GLOBAL             19 (NULL + AssertionError)
#             378 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             388 LOAD_ATTR               20 (_format_explanation)
#             408 LOAD_FAST                6 (@py_format8)
#             410 CALL                     1
#             418 CALL                     1
#             426 RAISE_VARARGS            1
#         >>  428 LOAD_CONST               0 (None)
#             430 COPY                     1
#             432 STORE_FAST               2 (@py_assert1)
#             434 COPY                     1
#             436 STORE_FAST               4 (@py_assert3)
#             438 STORE_FAST               3 (@py_assert4)
# 
#  64         440 LOAD_FAST                1 (result)
#             442 LOAD_ATTR               22 (errors)
#             462 STORE_FAST               7 (@py_assert2)
#             464 LOAD_GLOBAL             25 (NULL + len)
#             474 LOAD_FAST                7 (@py_assert2)
#             476 CALL                     1
#             484 STORE_FAST               3 (@py_assert4)
#             486 LOAD_CONST               8 (0)
#             488 STORE_FAST               8 (@py_assert7)
#             490 LOAD_FAST                3 (@py_assert4)
#             492 LOAD_FAST                8 (@py_assert7)
#             494 COMPARE_OP              40 (==)
#             498 STORE_FAST               9 (@py_assert6)
#             500 LOAD_FAST                9 (@py_assert6)
#             502 EXTENDED_ARG             1
#             504 POP_JUMP_IF_TRUE       266 (to 1038)
#             506 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             516 LOAD_ATTR                8 (_call_reprcompare)
#             536 LOAD_CONST               9 (('==',))
#             538 LOAD_FAST                9 (@py_assert6)
#             540 BUILD_TUPLE              1
#             542 LOAD_CONST              10 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.errors\n})\n} == %(py8)s',))
#             544 LOAD_FAST                3 (@py_assert4)
#             546 LOAD_FAST                8 (@py_assert7)
#             548 BUILD_TUPLE              2
#             550 CALL                     4
#             558 LOAD_CONST              11 ('len')
#             560 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             570 LOAD_ATTR               12 (locals)
#             590 CALL                     0
#             598 CONTAINS_OP              0
#             600 POP_JUMP_IF_TRUE        25 (to 652)
#             602 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             612 LOAD_ATTR               14 (_should_repr_global_name)
#             632 LOAD_GLOBAL             24 (len)
#             642 CALL                     1
#             650 POP_JUMP_IF_FALSE       25 (to 702)
#         >>  652 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             662 LOAD_ATTR               16 (_saferepr)
#             682 LOAD_GLOBAL             24 (len)
#             692 CALL                     1
#             700 JUMP_FORWARD             1 (to 704)
#         >>  702 LOAD_CONST              11 ('len')
#         >>  704 LOAD_CONST               4 ('result')
#             706 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             716 LOAD_ATTR               12 (locals)
#             736 CALL                     0
#             744 CONTAINS_OP              0
#             746 POP_JUMP_IF_TRUE        21 (to 790)
#             748 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             758 LOAD_ATTR               14 (_should_repr_global_name)
#             778 LOAD_FAST                1 (result)
#             780 CALL                     1
#             788 POP_JUMP_IF_FALSE       21 (to 832)
#         >>  790 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             800 LOAD_ATTR               16 (_saferepr)
#             820 LOAD_FAST                1 (result)
#             822 CALL                     1
#             830 JUMP_FORWARD             1 (to 834)
#         >>  832 LOAD_CONST               4 ('result')
#         >>  834 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             844 LOAD_ATTR               16 (_saferepr)
#             864 LOAD_FAST                7 (@py_assert2)
#             866 CALL                     1
#             874 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             884 LOAD_ATTR               16 (_saferepr)
#             904 LOAD_FAST                3 (@py_assert4)
#             906 CALL                     1
#             914 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             924 LOAD_ATTR               16 (_saferepr)
#             944 LOAD_FAST                8 (@py_assert7)
#             946 CALL                     1
#             954 LOAD_CONST              12 (('py0', 'py1', 'py3', 'py5', 'py8'))
#             956 BUILD_CONST_KEY_MAP      5
#             958 BINARY_OP                6 (%)
#             962 STORE_FAST              10 (@py_format9)
#             964 LOAD_CONST              13 ('assert %(py10)s')
#             966 LOAD_CONST              14 ('py10')
#             968 LOAD_FAST               10 (@py_format9)
#             970 BUILD_MAP                1
#             972 BINARY_OP                6 (%)
#             976 STORE_FAST              11 (@py_format11)
#             978 LOAD_GLOBAL             19 (NULL + AssertionError)
#             988 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             998 LOAD_ATTR               20 (_format_explanation)
#            1018 LOAD_FAST               11 (@py_format11)
#            1020 CALL                     1
#            1028 CALL                     1
#            1036 RAISE_VARARGS            1
#         >> 1038 LOAD_CONST               0 (None)
#            1040 COPY                     1
#            1042 STORE_FAST               7 (@py_assert2)
#            1044 COPY                     1
#            1046 STORE_FAST               3 (@py_assert4)
#            1048 COPY                     1
#            1050 STORE_FAST               9 (@py_assert6)
#            1052 STORE_FAST               8 (@py_assert7)
#            1054 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_failure_with_tuple at 0x3af9bec0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 66>:
#  66           0 RESUME                   0
# 
#  67           2 LOAD_GLOBAL              1 (NULL + ValidationResult)
#              12 LOAD_ATTR                2 (failure)
#              32 LOAD_CONST               1 (('field1', 'error message'))
#              34 BUILD_LIST               1
#              36 CALL                     1
#              44 STORE_FAST               1 (result)
# 
#  68          46 LOAD_FAST                1 (result)
#              48 LOAD_ATTR                4 (valid)
#              68 STORE_FAST               2 (@py_assert1)
#              70 LOAD_CONST               2 (False)
#              72 STORE_FAST               3 (@py_assert4)
#              74 LOAD_FAST                2 (@py_assert1)
#              76 LOAD_FAST                3 (@py_assert4)
#              78 IS_OP                    0
#              80 STORE_FAST               4 (@py_assert3)
#              82 LOAD_FAST                4 (@py_assert3)
#              84 POP_JUMP_IF_TRUE       173 (to 432)
#              86 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#              96 LOAD_ATTR                8 (_call_reprcompare)
#             116 LOAD_CONST               3 (('is',))
#             118 LOAD_FAST                4 (@py_assert3)
#             120 BUILD_TUPLE              1
#             122 LOAD_CONST               4 (('%(py2)s\n{%(py2)s = %(py0)s.valid\n} is %(py5)s',))
#             124 LOAD_FAST                2 (@py_assert1)
#             126 LOAD_FAST                3 (@py_assert4)
#             128 BUILD_TUPLE              2
#             130 CALL                     4
#             138 LOAD_CONST               5 ('result')
#             140 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             150 LOAD_ATTR               12 (locals)
#             170 CALL                     0
#             178 CONTAINS_OP              0
#             180 POP_JUMP_IF_TRUE        21 (to 224)
#             182 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             192 LOAD_ATTR               14 (_should_repr_global_name)
#             212 LOAD_FAST                1 (result)
#             214 CALL                     1
#             222 POP_JUMP_IF_FALSE       21 (to 266)
#         >>  224 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             234 LOAD_ATTR               16 (_saferepr)
#             254 LOAD_FAST                1 (result)
#             256 CALL                     1
#             264 JUMP_FORWARD             1 (to 268)
#         >>  266 LOAD_CONST               5 ('result')
#         >>  268 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             278 LOAD_ATTR               16 (_saferepr)
#             298 LOAD_FAST                2 (@py_assert1)
#             300 CALL                     1
#             308 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             318 LOAD_ATTR               16 (_saferepr)
#             338 LOAD_FAST                3 (@py_assert4)
#             340 CALL                     1
#             348 LOAD_CONST               6 (('py0', 'py2', 'py5'))
#             350 BUILD_CONST_KEY_MAP      3
#             352 BINARY_OP                6 (%)
#             356 STORE_FAST               5 (@py_format6)
#             358 LOAD_CONST               7 ('assert %(py7)s')
#             360 LOAD_CONST               8 ('py7')
#             362 LOAD_FAST                5 (@py_format6)
#             364 BUILD_MAP                1
#             366 BINARY_OP                6 (%)
#             370 STORE_FAST               6 (@py_format8)
#             372 LOAD_GLOBAL             19 (NULL + AssertionError)
#             382 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             392 LOAD_ATTR               20 (_format_explanation)
#             412 LOAD_FAST                6 (@py_format8)
#             414 CALL                     1
#             422 CALL                     1
#             430 RAISE_VARARGS            1
#         >>  432 LOAD_CONST               0 (None)
#             434 COPY                     1
#             436 STORE_FAST               2 (@py_assert1)
#             438 COPY                     1
#             440 STORE_FAST               4 (@py_assert3)
#             442 STORE_FAST               3 (@py_assert4)
# 
#  69         444 LOAD_FAST                1 (result)
#             446 LOAD_ATTR               22 (errors)
#             466 STORE_FAST               7 (@py_assert2)
#             468 LOAD_GLOBAL             25 (NULL + len)
#             478 LOAD_FAST                7 (@py_assert2)
#             480 CALL                     1
#             488 STORE_FAST               3 (@py_assert4)
#             490 LOAD_CONST               9 (1)
#             492 STORE_FAST               8 (@py_assert7)
#             494 LOAD_FAST                3 (@py_assert4)
#             496 LOAD_FAST                8 (@py_assert7)
#             498 COMPARE_OP              40 (==)
#             502 STORE_FAST               9 (@py_assert6)
#             504 LOAD_FAST                9 (@py_assert6)
#             506 EXTENDED_ARG             1
#             508 POP_JUMP_IF_TRUE       266 (to 1042)
#             510 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             520 LOAD_ATTR                8 (_call_reprcompare)
#             540 LOAD_CONST              10 (('==',))
#             542 LOAD_FAST                9 (@py_assert6)
#             544 BUILD_TUPLE              1
#             546 LOAD_CONST              11 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.errors\n})\n} == %(py8)s',))
#             548 LOAD_FAST                3 (@py_assert4)
#             550 LOAD_FAST                8 (@py_assert7)
#             552 BUILD_TUPLE              2
#             554 CALL                     4
#             562 LOAD_CONST              12 ('len')
#             564 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             574 LOAD_ATTR               12 (locals)
#             594 CALL                     0
#             602 CONTAINS_OP              0
#             604 POP_JUMP_IF_TRUE        25 (to 656)
#             606 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             616 LOAD_ATTR               14 (_should_repr_global_name)
#             636 LOAD_GLOBAL             24 (len)
#             646 CALL                     1
#             654 POP_JUMP_IF_FALSE       25 (to 706)
#         >>  656 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             666 LOAD_ATTR               16 (_saferepr)
#             686 LOAD_GLOBAL             24 (len)
#             696 CALL                     1
#             704 JUMP_FORWARD             1 (to 708)
#         >>  706 LOAD_CONST              12 ('len')
#         >>  708 LOAD_CONST               5 ('result')
#             710 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             720 LOAD_ATTR               12 (locals)
#             740 CALL                     0
#             748 CONTAINS_OP              0
#             750 POP_JUMP_IF_TRUE        21 (to 794)
#             752 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             762 LOAD_ATTR               14 (_should_repr_global_name)
#             782 LOAD_FAST                1 (result)
#             784 CALL                     1
#             792 POP_JUMP_IF_FALSE       21 (to 836)
#         >>  794 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             804 LOAD_ATTR               16 (_saferepr)
#             824 LOAD_FAST                1 (result)
#             826 CALL                     1
#             834 JUMP_FORWARD             1 (to 838)
#         >>  836 LOAD_CONST               5 ('result')
#         >>  838 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             848 LOAD_ATTR               16 (_saferepr)
#             868 LOAD_FAST                7 (@py_assert2)
#             870 CALL                     1
#             878 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             888 LOAD_ATTR               16 (_saferepr)
#             908 LOAD_FAST                3 (@py_assert4)
#             910 CALL                     1
#             918 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             928 LOAD_ATTR               16 (_saferepr)
#             948 LOAD_FAST                8 (@py_assert7)
#             950 CALL                     1
#             958 LOAD_CONST              13 (('py0', 'py1', 'py3', 'py5', 'py8'))
#             960 BUILD_CONST_KEY_MAP      5
#             962 BINARY_OP                6 (%)
#             966 STORE_FAST              10 (@py_format9)
#             968 LOAD_CONST              14 ('assert %(py10)s')
#             970 LOAD_CONST              15 ('py10')
#             972 LOAD_FAST               10 (@py_format9)
#             974 BUILD_MAP                1
#             976 BINARY_OP                6 (%)
#             980 STORE_FAST              11 (@py_format11)
#             982 LOAD_GLOBAL             19 (NULL + AssertionError)
#             992 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1002 LOAD_ATTR               20 (_format_explanation)
#            1022 LOAD_FAST               11 (@py_format11)
#            1024 CALL                     1
#            1032 CALL                     1
#            1040 RAISE_VARARGS            1
#         >> 1042 LOAD_CONST               0 (None)
#            1044 COPY                     1
#            1046 STORE_FAST               7 (@py_assert2)
#            1048 COPY                     1
#            1050 STORE_FAST               3 (@py_assert4)
#            1052 COPY                     1
#            1054 STORE_FAST               9 (@py_assert6)
#            1056 STORE_FAST               8 (@py_assert7)
# 
#  70        1058 LOAD_FAST                1 (result)
#            1060 LOAD_ATTR               22 (errors)
#            1080 LOAD_CONST              16 (0)
#            1082 BINARY_SUBSCR
#            1086 STORE_FAST              12 (@py_assert0)
#            1088 LOAD_FAST               12 (@py_assert0)
#            1090 LOAD_ATTR               26 (field)
#            1110 STORE_FAST               7 (@py_assert2)
#            1112 LOAD_CONST              17 ('field1')
#            1114 STORE_FAST              13 (@py_assert5)
#            1116 LOAD_FAST                7 (@py_assert2)
#            1118 LOAD_FAST               13 (@py_assert5)
#            1120 COMPARE_OP              40 (==)
#            1124 STORE_FAST               3 (@py_assert4)
#            1126 LOAD_FAST                3 (@py_assert4)
#            1128 POP_JUMP_IF_TRUE       128 (to 1386)
#            1130 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1140 LOAD_ATTR                8 (_call_reprcompare)
#            1160 LOAD_CONST              10 (('==',))
#            1162 LOAD_FAST                3 (@py_assert4)
#            1164 BUILD_TUPLE              1
#            1166 LOAD_CONST              18 (('%(py3)s\n{%(py3)s = %(py1)s.field\n} == %(py6)s',))
#            1168 LOAD_FAST                7 (@py_assert2)
#            1170 LOAD_FAST               13 (@py_assert5)
#            1172 BUILD_TUPLE              2
#            1174 CALL                     4
#            1182 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1192 LOAD_ATTR               16 (_saferepr)
#            1212 LOAD_FAST               12 (@py_assert0)
#            1214 CALL                     1
#            1222 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1232 LOAD_ATTR               16 (_saferepr)
#            1252 LOAD_FAST                7 (@py_assert2)
#            1254 CALL                     1
#            1262 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1272 LOAD_ATTR               16 (_saferepr)
#            1292 LOAD_FAST               13 (@py_assert5)
#            1294 CALL                     1
#            1302 LOAD_CONST              19 (('py1', 'py3', 'py6'))
#            1304 BUILD_CONST_KEY_MAP      3
#            1306 BINARY_OP                6 (%)
#            1310 STORE_FAST              14 (@py_format7)
#            1312 LOAD_CONST              20 ('assert %(py8)s')
#            1314 LOAD_CONST              21 ('py8')
#            1316 LOAD_FAST               14 (@py_format7)
#            1318 BUILD_MAP                1
#            1320 BINARY_OP                6 (%)
#            1324 STORE_FAST              10 (@py_format9)
#            1326 LOAD_GLOBAL             19 (NULL + AssertionError)
#            1336 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1346 LOAD_ATTR               20 (_format_explanation)
#            1366 LOAD_FAST               10 (@py_format9)
#            1368 CALL                     1
#            1376 CALL                     1
#            1384 RAISE_VARARGS            1
#         >> 1386 LOAD_CONST               0 (None)
#            1388 COPY                     1
#            1390 STORE_FAST              12 (@py_assert0)
#            1392 COPY                     1
#            1394 STORE_FAST               7 (@py_assert2)
#            1396 COPY                     1
#            1398 STORE_FAST               3 (@py_assert4)
#            1400 STORE_FAST              13 (@py_assert5)
#            1402 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_failure_with_validation_error at 0x3af9c980, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 72>:
#  72           0 RESUME                   0
# 
#  73           2 LOAD_GLOBAL              1 (NULL + ValidationResult)
#              12 LOAD_ATTR                2 (failure)
# 
#  74          32 LOAD_GLOBAL              5 (NULL + ValidationError)
#              42 LOAD_CONST               1 ('field2')
#              44 LOAD_CONST               2 ('error')
#              46 KW_NAMES                 3 (('field', 'message'))
#              48 CALL                     2
#              56 BUILD_LIST               1
# 
#  73          58 CALL                     1
#              66 STORE_FAST               1 (result)
# 
#  76          68 LOAD_FAST                1 (result)
#              70 LOAD_ATTR                6 (valid)
#              90 STORE_FAST               2 (@py_assert1)
#              92 LOAD_CONST               4 (False)
#              94 STORE_FAST               3 (@py_assert4)
#              96 LOAD_FAST                2 (@py_assert1)
#              98 LOAD_FAST                3 (@py_assert4)
#             100 IS_OP                    0
#             102 STORE_FAST               4 (@py_assert3)
#             104 LOAD_FAST                4 (@py_assert3)
#             106 POP_JUMP_IF_TRUE       173 (to 454)
#             108 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             118 LOAD_ATTR               10 (_call_reprcompare)
#             138 LOAD_CONST               5 (('is',))
#             140 LOAD_FAST                4 (@py_assert3)
#             142 BUILD_TUPLE              1
#             144 LOAD_CONST               6 (('%(py2)s\n{%(py2)s = %(py0)s.valid\n} is %(py5)s',))
#             146 LOAD_FAST                2 (@py_assert1)
#             148 LOAD_FAST                3 (@py_assert4)
#             150 BUILD_TUPLE              2
#             152 CALL                     4
#             160 LOAD_CONST               7 ('result')
#             162 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             172 LOAD_ATTR               14 (locals)
#             192 CALL                     0
#             200 CONTAINS_OP              0
#             202 POP_JUMP_IF_TRUE        21 (to 246)
#             204 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             214 LOAD_ATTR               16 (_should_repr_global_name)
#             234 LOAD_FAST                1 (result)
#             236 CALL                     1
#             244 POP_JUMP_IF_FALSE       21 (to 288)
#         >>  246 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             256 LOAD_ATTR               18 (_saferepr)
#             276 LOAD_FAST                1 (result)
#             278 CALL                     1
#             286 JUMP_FORWARD             1 (to 290)
#         >>  288 LOAD_CONST               7 ('result')
#         >>  290 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             300 LOAD_ATTR               18 (_saferepr)
#             320 LOAD_FAST                2 (@py_assert1)
#             322 CALL                     1
#             330 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             340 LOAD_ATTR               18 (_saferepr)
#             360 LOAD_FAST                3 (@py_assert4)
#             362 CALL                     1
#             370 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#             372 BUILD_CONST_KEY_MAP      3
#             374 BINARY_OP                6 (%)
#             378 STORE_FAST               5 (@py_format6)
#             380 LOAD_CONST               9 ('assert %(py7)s')
#             382 LOAD_CONST              10 ('py7')
#             384 LOAD_FAST                5 (@py_format6)
#             386 BUILD_MAP                1
#             388 BINARY_OP                6 (%)
#             392 STORE_FAST               6 (@py_format8)
#             394 LOAD_GLOBAL             21 (NULL + AssertionError)
#             404 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             414 LOAD_ATTR               22 (_format_explanation)
#             434 LOAD_FAST                6 (@py_format8)
#             436 CALL                     1
#             444 CALL                     1
#             452 RAISE_VARARGS            1
#         >>  454 LOAD_CONST               0 (None)
#             456 COPY                     1
#             458 STORE_FAST               2 (@py_assert1)
#             460 COPY                     1
#             462 STORE_FAST               4 (@py_assert3)
#             464 STORE_FAST               3 (@py_assert4)
# 
#  77         466 LOAD_FAST                1 (result)
#             468 LOAD_ATTR               24 (errors)
#             488 STORE_FAST               7 (@py_assert2)
#             490 LOAD_GLOBAL             27 (NULL + len)
#             500 LOAD_FAST                7 (@py_assert2)
#             502 CALL                     1
#             510 STORE_FAST               3 (@py_assert4)
#             512 LOAD_CONST              11 (1)
#             514 STORE_FAST               8 (@py_assert7)
#             516 LOAD_FAST                3 (@py_assert4)
#             518 LOAD_FAST                8 (@py_assert7)
#             520 COMPARE_OP              40 (==)
#             524 STORE_FAST               9 (@py_assert6)
#             526 LOAD_FAST                9 (@py_assert6)
#             528 EXTENDED_ARG             1
#             530 POP_JUMP_IF_TRUE       266 (to 1064)
#             532 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             542 LOAD_ATTR               10 (_call_reprcompare)
#             562 LOAD_CONST              12 (('==',))
#             564 LOAD_FAST                9 (@py_assert6)
#             566 BUILD_TUPLE              1
#             568 LOAD_CONST              13 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.errors\n})\n} == %(py8)s',))
#             570 LOAD_FAST                3 (@py_assert4)
#             572 LOAD_FAST                8 (@py_assert7)
#             574 BUILD_TUPLE              2
#             576 CALL                     4
#             584 LOAD_CONST              14 ('len')
#             586 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             596 LOAD_ATTR               14 (locals)
#             616 CALL                     0
#             624 CONTAINS_OP              0
#             626 POP_JUMP_IF_TRUE        25 (to 678)
#             628 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             638 LOAD_ATTR               16 (_should_repr_global_name)
#             658 LOAD_GLOBAL             26 (len)
#             668 CALL                     1
#             676 POP_JUMP_IF_FALSE       25 (to 728)
#         >>  678 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             688 LOAD_ATTR               18 (_saferepr)
#             708 LOAD_GLOBAL             26 (len)
#             718 CALL                     1
#             726 JUMP_FORWARD             1 (to 730)
#         >>  728 LOAD_CONST              14 ('len')
#         >>  730 LOAD_CONST               7 ('result')
#             732 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             742 LOAD_ATTR               14 (locals)
#             762 CALL                     0
#             770 CONTAINS_OP              0
#             772 POP_JUMP_IF_TRUE        21 (to 816)
#             774 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             784 LOAD_ATTR               16 (_should_repr_global_name)
#             804 LOAD_FAST                1 (result)
#             806 CALL                     1
#             814 POP_JUMP_IF_FALSE       21 (to 858)
#         >>  816 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             826 LOAD_ATTR               18 (_saferepr)
#             846 LOAD_FAST                1 (result)
#             848 CALL                     1
#             856 JUMP_FORWARD             1 (to 860)
#         >>  858 LOAD_CONST               7 ('result')
#         >>  860 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             870 LOAD_ATTR               18 (_saferepr)
#             890 LOAD_FAST                7 (@py_assert2)
#             892 CALL                     1
#             900 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             910 LOAD_ATTR               18 (_saferepr)
#             930 LOAD_FAST                3 (@py_assert4)
#             932 CALL                     1
#             940 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             950 LOAD_ATTR               18 (_saferepr)
#             970 LOAD_FAST                8 (@py_assert7)
#             972 CALL                     1
#             980 LOAD_CONST              15 (('py0', 'py1', 'py3', 'py5', 'py8'))
#             982 BUILD_CONST_KEY_MAP      5
#             984 BINARY_OP                6 (%)
#             988 STORE_FAST              10 (@py_format9)
#             990 LOAD_CONST              16 ('assert %(py10)s')
#             992 LOAD_CONST              17 ('py10')
#             994 LOAD_FAST               10 (@py_format9)
#             996 BUILD_MAP                1
#             998 BINARY_OP                6 (%)
#            1002 STORE_FAST              11 (@py_format11)
#            1004 LOAD_GLOBAL             21 (NULL + AssertionError)
#            1014 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1024 LOAD_ATTR               22 (_format_explanation)
#            1044 LOAD_FAST               11 (@py_format11)
#            1046 CALL                     1
#            1054 CALL                     1
#            1062 RAISE_VARARGS            1
#         >> 1064 LOAD_CONST               0 (None)
#            1066 COPY                     1
#            1068 STORE_FAST               7 (@py_assert2)
#            1070 COPY                     1
#            1072 STORE_FAST               3 (@py_assert4)
#            1074 COPY                     1
#            1076 STORE_FAST               9 (@py_assert6)
#            1078 STORE_FAST               8 (@py_assert7)
#            1080 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestSimulationResult at 0x73cd93b065b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 80>:
#  80           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestSimulationResult')
#               8 STORE_NAME               2 (__qualname__)
# 
#  81          10 LOAD_CONST               1 ('Tests for SimulationResult.')
#              12 STORE_NAME               3 (__doc__)
# 
#  83          14 LOAD_CONST               2 (<code object test_is_success at 0x3afa0e10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 83>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_is_success)
# 
#  89          20 LOAD_CONST               3 (<code object test_is_not_success_with_errors at 0x3af98b30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 89>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_is_not_success_with_errors)
# 
#  95          26 LOAD_CONST               4 (<code object test_to_dict at 0x3af9ce90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 95>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_to_dict)
#              32 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_is_success at 0x3afa0e10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 83>:
#  83           0 RESUME                   0
# 
#  84           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
#  85          12 LOAD_CONST               1 ('test')
#              14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
#              44 BUILD_LIST               0
# 
#  84          46 KW_NAMES                 2 (('job_id', 'status', 'errors'))
#              48 CALL                     3
#              56 STORE_FAST               1 (result)
# 
#  87          58 LOAD_FAST                1 (result)
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
# Disassembly of <code object test_is_not_success_with_errors at 0x3af98b30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 89>:
#  89           0 RESUME                   0
# 
#  90           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
#  91          12 LOAD_CONST               1 ('test')
#              14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
#              44 LOAD_CONST               2 ('some error')
#              46 BUILD_LIST               1
# 
#  90          48 KW_NAMES                 3 (('job_id', 'status', 'errors'))
#              50 CALL                     3
#              58 STORE_FAST               1 (result)
# 
#  93          60 LOAD_FAST                1 (result)
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
# Disassembly of <code object test_to_dict at 0x3af9ce90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 95>:
#  95           0 RESUME                   0
# 
#  96           2 LOAD_GLOBAL              1 (NULL + SimulationResult)
# 
#  97          12 LOAD_CONST               1 ('test')
#              14 LOAD_GLOBAL              2 (SimulationStatus)
#              24 LOAD_ATTR                4 (COMPLETED)
#              44 LOAD_CONST               2 ('key')
#              46 LOAD_CONST               3 ('value')
#              48 BUILD_MAP                1
# 
#  96          50 KW_NAMES                 4 (('job_id', 'status', 'data'))
#              52 CALL                     3
#              60 STORE_FAST               1 (result)
# 
#  99          62 LOAD_FAST                1 (result)
#              64 LOAD_ATTR                7 (NULL|self + to_dict)
#              84 CALL                     0
#              92 STORE_FAST               2 (d)
# 
# 100          94 LOAD_FAST                2 (d)
#              96 LOAD_CONST               5 ('job_id')
#              98 BINARY_SUBSCR
#             102 STORE_FAST               3 (@py_assert0)
#             104 LOAD_CONST               1 ('test')
#             106 STORE_FAST               4 (@py_assert3)
#             108 LOAD_FAST                3 (@py_assert0)
#             110 LOAD_FAST                4 (@py_assert3)
#             112 COMPARE_OP              40 (==)
#             116 STORE_FAST               5 (@py_assert2)
#             118 LOAD_FAST                5 (@py_assert2)
#             120 POP_JUMP_IF_TRUE       108 (to 338)
#             122 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             132 LOAD_ATTR               10 (_call_reprcompare)
#             152 LOAD_CONST               6 (('==',))
#             154 LOAD_FAST                5 (@py_assert2)
#             156 BUILD_TUPLE              1
#             158 LOAD_CONST               7 (('%(py1)s == %(py4)s',))
#             160 LOAD_FAST                3 (@py_assert0)
#             162 LOAD_FAST                4 (@py_assert3)
#             164 BUILD_TUPLE              2
#             166 CALL                     4
#             174 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             184 LOAD_ATTR               12 (_saferepr)
#             204 LOAD_FAST                3 (@py_assert0)
#             206 CALL                     1
#             214 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             224 LOAD_ATTR               12 (_saferepr)
#             244 LOAD_FAST                4 (@py_assert3)
#             246 CALL                     1
#             254 LOAD_CONST               8 (('py1', 'py4'))
#             256 BUILD_CONST_KEY_MAP      2
#             258 BINARY_OP                6 (%)
#             262 STORE_FAST               6 (@py_format5)
#             264 LOAD_CONST               9 ('assert %(py6)s')
#             266 LOAD_CONST              10 ('py6')
#             268 LOAD_FAST                6 (@py_format5)
#             270 BUILD_MAP                1
#             272 BINARY_OP                6 (%)
#             276 STORE_FAST               7 (@py_format7)
#             278 LOAD_GLOBAL             15 (NULL + AssertionError)
#             288 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             298 LOAD_ATTR               16 (_format_explanation)
#             318 LOAD_FAST                7 (@py_format7)
#             320 CALL                     1
#             328 CALL                     1
#             336 RAISE_VARARGS            1
#         >>  338 LOAD_CONST               0 (None)
#             340 COPY                     1
#             342 STORE_FAST               3 (@py_assert0)
#             344 COPY                     1
#             346 STORE_FAST               5 (@py_assert2)
#             348 STORE_FAST               4 (@py_assert3)
# 
# 101         350 LOAD_FAST                2 (d)
#             352 LOAD_CONST              11 ('status')
#             354 BINARY_SUBSCR
#             358 STORE_FAST               3 (@py_assert0)
#             360 LOAD_CONST              12 ('completed')
#             362 STORE_FAST               4 (@py_assert3)
#             364 LOAD_FAST                3 (@py_assert0)
#             366 LOAD_FAST                4 (@py_assert3)
#             368 COMPARE_OP              40 (==)
#             372 STORE_FAST               5 (@py_assert2)
#             374 LOAD_FAST                5 (@py_assert2)
#             376 POP_JUMP_IF_TRUE       108 (to 594)
#             378 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             388 LOAD_ATTR               10 (_call_reprcompare)
#             408 LOAD_CONST               6 (('==',))
#             410 LOAD_FAST                5 (@py_assert2)
#             412 BUILD_TUPLE              1
#             414 LOAD_CONST               7 (('%(py1)s == %(py4)s',))
#             416 LOAD_FAST                3 (@py_assert0)
#             418 LOAD_FAST                4 (@py_assert3)
#             420 BUILD_TUPLE              2
#             422 CALL                     4
#             430 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             440 LOAD_ATTR               12 (_saferepr)
#             460 LOAD_FAST                3 (@py_assert0)
#             462 CALL                     1
#             470 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             480 LOAD_ATTR               12 (_saferepr)
#             500 LOAD_FAST                4 (@py_assert3)
#             502 CALL                     1
#             510 LOAD_CONST               8 (('py1', 'py4'))
#             512 BUILD_CONST_KEY_MAP      2
#             514 BINARY_OP                6 (%)
#             518 STORE_FAST               6 (@py_format5)
#             520 LOAD_CONST               9 ('assert %(py6)s')
#             522 LOAD_CONST              10 ('py6')
#             524 LOAD_FAST                6 (@py_format5)
#             526 BUILD_MAP                1
#             528 BINARY_OP                6 (%)
#             532 STORE_FAST               7 (@py_format7)
#             534 LOAD_GLOBAL             15 (NULL + AssertionError)
#             544 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             554 LOAD_ATTR               16 (_format_explanation)
#             574 LOAD_FAST                7 (@py_format7)
#             576 CALL                     1
#             584 CALL                     1
#             592 RAISE_VARARGS            1
#         >>  594 LOAD_CONST               0 (None)
#             596 COPY                     1
#             598 STORE_FAST               3 (@py_assert0)
#             600 COPY                     1
#             602 STORE_FAST               5 (@py_assert2)
#             604 STORE_FAST               4 (@py_assert3)
# 
# 102         606 LOAD_FAST                2 (d)
#             608 LOAD_CONST              13 ('data')
#             610 BINARY_SUBSCR
#             614 LOAD_CONST               2 ('key')
#             616 BINARY_SUBSCR
#             620 STORE_FAST               3 (@py_assert0)
#             622 LOAD_CONST               3 ('value')
#             624 STORE_FAST               4 (@py_assert3)
#             626 LOAD_FAST                3 (@py_assert0)
#             628 LOAD_FAST                4 (@py_assert3)
#             630 COMPARE_OP              40 (==)
#             634 STORE_FAST               5 (@py_assert2)
#             636 LOAD_FAST                5 (@py_assert2)
#             638 POP_JUMP_IF_TRUE       108 (to 856)
#             640 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             650 LOAD_ATTR               10 (_call_reprcompare)
#             670 LOAD_CONST               6 (('==',))
#             672 LOAD_FAST                5 (@py_assert2)
#             674 BUILD_TUPLE              1
#             676 LOAD_CONST               7 (('%(py1)s == %(py4)s',))
#             678 LOAD_FAST                3 (@py_assert0)
#             680 LOAD_FAST                4 (@py_assert3)
#             682 BUILD_TUPLE              2
#             684 CALL                     4
#             692 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             702 LOAD_ATTR               12 (_saferepr)
#             722 LOAD_FAST                3 (@py_assert0)
#             724 CALL                     1
#             732 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             742 LOAD_ATTR               12 (_saferepr)
#             762 LOAD_FAST                4 (@py_assert3)
#             764 CALL                     1
#             772 LOAD_CONST               8 (('py1', 'py4'))
#             774 BUILD_CONST_KEY_MAP      2
#             776 BINARY_OP                6 (%)
#             780 STORE_FAST               6 (@py_format5)
#             782 LOAD_CONST               9 ('assert %(py6)s')
#             784 LOAD_CONST              10 ('py6')
#             786 LOAD_FAST                6 (@py_format5)
#             788 BUILD_MAP                1
#             790 BINARY_OP                6 (%)
#             794 STORE_FAST               7 (@py_format7)
#             796 LOAD_GLOBAL             15 (NULL + AssertionError)
#             806 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             816 LOAD_ATTR               16 (_format_explanation)
#             836 LOAD_FAST                7 (@py_format7)
#             838 CALL                     1
#             846 CALL                     1
#             854 RAISE_VARARGS            1
#         >>  856 LOAD_CONST               0 (None)
#             858 COPY                     1
#             860 STORE_FAST               3 (@py_assert0)
#             862 COPY                     1
#             864 STORE_FAST               5 (@py_assert2)
#             866 STORE_FAST               4 (@py_assert3)
#             868 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestEngineAdapter at 0x73cd93b06880, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 105>:
# 105           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestEngineAdapter')
#               8 STORE_NAME               2 (__qualname__)
# 
# 106          10 LOAD_CONST               1 ('Tests for EngineAdapter.')
#              12 STORE_NAME               3 (__doc__)
# 
# 108          14 LOAD_CONST               2 (<code object test_context_manager at 0x3af8f430, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 108>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_context_manager)
# 
# 114          20 LOAD_CONST               3 (<code object test_require_connected_raises at 0x73cd948d3890, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 114>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_require_connected_raises)
# 
# 119          26 LOAD_CONST               4 (<code object test_validate_config_success at 0x3aef1410, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 119>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_validate_config_success)
# 
# 124          32 LOAD_CONST               5 (<code object test_validate_config_failure at 0x3af9d830, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 124>)
#              34 MAKE_FUNCTION            0
#              36 STORE_NAME               7 (test_validate_config_failure)
# 
# 130          38 LOAD_CONST               6 (<code object test_get_supported_simulations at 0x3af9a2d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 130>)
#              40 MAKE_FUNCTION            0
#              42 STORE_NAME               8 (test_get_supported_simulations)
#              44 RETURN_CONST             7 (None)
# 
# Disassembly of <code object test_context_manager at 0x3af8f430, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 108>:
# 108           0 RESUME                   0
# 
# 109           2 LOAD_GLOBAL              1 (NULL + MockAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
# 110          22 LOAD_FAST                1 (adapter)
#              24 BEFORE_WITH
#              26 POP_TOP
# 
# 111          28 LOAD_FAST                1 (adapter)
#              30 LOAD_ATTR                2 (is_connected)
#              50 STORE_FAST               2 (@py_assert1)
#              52 PUSH_NULL
#              54 LOAD_FAST                2 (@py_assert1)
#              56 CALL                     0
#              64 STORE_FAST               3 (@py_assert3)
#              66 LOAD_FAST                3 (@py_assert3)
#              68 POP_JUMP_IF_TRUE       141 (to 352)
#              70 LOAD_CONST               1 ('assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_connected\n}()\n}')
#              72 LOAD_CONST               2 ('adapter')
#              74 LOAD_GLOBAL              5 (NULL + @py_builtins)
#              84 LOAD_ATTR                6 (locals)
#             104 CALL                     0
#             112 CONTAINS_OP              0
#             114 POP_JUMP_IF_TRUE        21 (to 158)
#             116 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             126 LOAD_ATTR               10 (_should_repr_global_name)
#             146 LOAD_FAST                1 (adapter)
#             148 CALL                     1
#             156 POP_JUMP_IF_FALSE       21 (to 200)
#         >>  158 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             168 LOAD_ATTR               12 (_saferepr)
#             188 LOAD_FAST                1 (adapter)
#             190 CALL                     1
#             198 JUMP_FORWARD             1 (to 202)
#         >>  200 LOAD_CONST               2 ('adapter')
#         >>  202 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             212 LOAD_ATTR               12 (_saferepr)
#             232 LOAD_FAST                2 (@py_assert1)
#             234 CALL                     1
#             242 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             252 LOAD_ATTR               12 (_saferepr)
#             272 LOAD_FAST                3 (@py_assert3)
#             274 CALL                     1
#             282 LOAD_CONST               3 (('py0', 'py2', 'py4'))
#             284 BUILD_CONST_KEY_MAP      3
#             286 BINARY_OP                6 (%)
#             290 STORE_FAST               4 (@py_format5)
#             292 LOAD_GLOBAL             15 (NULL + AssertionError)
#             302 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             312 LOAD_ATTR               16 (_format_explanation)
#             332 LOAD_FAST                4 (@py_format5)
#             334 CALL                     1
#             342 CALL                     1
#             350 RAISE_VARARGS            1
#         >>  352 LOAD_CONST               0 (None)
#             354 COPY                     1
#             356 STORE_FAST               2 (@py_assert1)
#             358 STORE_FAST               3 (@py_assert3)
# 
# 110         360 LOAD_CONST               0 (None)
#             362 LOAD_CONST               0 (None)
#             364 LOAD_CONST               0 (None)
#             366 CALL                     2
#             374 POP_TOP
# 
# 112     >>  376 LOAD_FAST                1 (adapter)
#             378 LOAD_ATTR                2 (is_connected)
#             398 STORE_FAST               2 (@py_assert1)
#             400 PUSH_NULL
#             402 LOAD_FAST                2 (@py_assert1)
#             404 CALL                     0
#             412 STORE_FAST               3 (@py_assert3)
#             414 LOAD_FAST                3 (@py_assert3)
#             416 UNARY_NOT
#             418 STORE_FAST               5 (@py_assert5)
#             420 LOAD_FAST                5 (@py_assert5)
#             422 POP_JUMP_IF_TRUE       141 (to 706)
#             424 LOAD_CONST               4 ('assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_connected\n}()\n}')
#             426 LOAD_CONST               2 ('adapter')
#             428 LOAD_GLOBAL              5 (NULL + @py_builtins)
#             438 LOAD_ATTR                6 (locals)
#             458 CALL                     0
#             466 CONTAINS_OP              0
#             468 POP_JUMP_IF_TRUE        21 (to 512)
#             470 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             480 LOAD_ATTR               10 (_should_repr_global_name)
#             500 LOAD_FAST                1 (adapter)
#             502 CALL                     1
#             510 POP_JUMP_IF_FALSE       21 (to 554)
#         >>  512 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             522 LOAD_ATTR               12 (_saferepr)
#             542 LOAD_FAST                1 (adapter)
#             544 CALL                     1
#             552 JUMP_FORWARD             1 (to 556)
#         >>  554 LOAD_CONST               2 ('adapter')
#         >>  556 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             566 LOAD_ATTR               12 (_saferepr)
#             586 LOAD_FAST                2 (@py_assert1)
#             588 CALL                     1
#             596 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             606 LOAD_ATTR               12 (_saferepr)
#             626 LOAD_FAST                3 (@py_assert3)
#             628 CALL                     1
#             636 LOAD_CONST               3 (('py0', 'py2', 'py4'))
#             638 BUILD_CONST_KEY_MAP      3
#             640 BINARY_OP                6 (%)
#             644 STORE_FAST               6 (@py_format6)
#             646 LOAD_GLOBAL             15 (NULL + AssertionError)
#             656 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             666 LOAD_ATTR               16 (_format_explanation)
#             686 LOAD_FAST                6 (@py_format6)
#             688 CALL                     1
#             696 CALL                     1
#             704 RAISE_VARARGS            1
#         >>  706 LOAD_CONST               0 (None)
#             708 COPY                     1
#             710 STORE_FAST               2 (@py_assert1)
#             712 COPY                     1
#             714 STORE_FAST               3 (@py_assert3)
#             716 STORE_FAST               5 (@py_assert5)
#             718 RETURN_CONST             0 (None)
# 
# 110     >>  720 PUSH_EXC_INFO
#             722 WITH_EXCEPT_START
#             724 POP_JUMP_IF_TRUE         1 (to 728)
#             726 RERAISE                  2
#         >>  728 POP_TOP
#             730 POP_EXCEPT
#             732 POP_TOP
#             734 POP_TOP
#             736 JUMP_BACKWARD          181 (to 376)
#         >>  738 COPY                     3
#             740 POP_EXCEPT
#             742 RERAISE                  1
# ExceptionTable:
#   26 to 358 -> 720 [1] lasti
#   720 to 728 -> 738 [3] lasti
# 
# Disassembly of <code object test_require_connected_raises at 0x73cd948d3890, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 114>:
# 114           0 RESUME                   0
# 
# 115           2 LOAD_GLOBAL              1 (NULL + MockAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
# 116          22 LOAD_GLOBAL              3 (NULL + pytest)
#              32 LOAD_ATTR                4 (raises)
#              52 LOAD_GLOBAL              6 (RuntimeError)
#              62 LOAD_CONST               1 ('Not connected')
#              64 KW_NAMES                 2 (('match',))
#              66 CALL                     2
#              74 BEFORE_WITH
#              76 POP_TOP
# 
# 117          78 LOAD_FAST                1 (adapter)
#              80 LOAD_ATTR                9 (NULL|self + run_simulation)
#             100 BUILD_MAP                0
#             102 CALL                     1
#             110 POP_TOP
# 
# 116         112 LOAD_CONST               0 (None)
#             114 LOAD_CONST               0 (None)
#             116 LOAD_CONST               0 (None)
#             118 CALL                     2
#             126 POP_TOP
#             128 RETURN_CONST             0 (None)
#         >>  130 PUSH_EXC_INFO
#             132 WITH_EXCEPT_START
#             134 POP_JUMP_IF_TRUE         1 (to 138)
#             136 RERAISE                  2
#         >>  138 POP_TOP
#             140 POP_EXCEPT
#             142 POP_TOP
#             144 POP_TOP
#             146 RETURN_CONST             0 (None)
#         >>  148 COPY                     3
#             150 POP_EXCEPT
#             152 RERAISE                  1
# ExceptionTable:
#   76 to 110 -> 130 [1] lasti
#   130 to 138 -> 148 [3] lasti
# 
# Disassembly of <code object test_validate_config_success at 0x3aef1410, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 119>:
# 119           0 RESUME                   0
# 
# 120           2 LOAD_GLOBAL              1 (NULL + MockAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
# 121          22 LOAD_FAST                1 (adapter)
#              24 LOAD_ATTR                3 (NULL|self + validate_config)
#              44 LOAD_CONST               1 ('valid')
#              46 LOAD_CONST               2 (True)
#              48 BUILD_MAP                1
#              50 CALL                     1
#              58 STORE_FAST               2 (result)
# 
# 122          60 LOAD_FAST                2 (result)
#              62 LOAD_ATTR                4 (valid)
#              82 STORE_FAST               3 (@py_assert1)
#              84 LOAD_CONST               2 (True)
#              86 STORE_FAST               4 (@py_assert4)
#              88 LOAD_FAST                3 (@py_assert1)
#              90 LOAD_FAST                4 (@py_assert4)
#              92 IS_OP                    0
#              94 STORE_FAST               5 (@py_assert3)
#              96 LOAD_FAST                5 (@py_assert3)
#              98 POP_JUMP_IF_TRUE       173 (to 446)
#             100 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             110 LOAD_ATTR                8 (_call_reprcompare)
#             130 LOAD_CONST               3 (('is',))
#             132 LOAD_FAST                5 (@py_assert3)
#             134 BUILD_TUPLE              1
#             136 LOAD_CONST               4 (('%(py2)s\n{%(py2)s = %(py0)s.valid\n} is %(py5)s',))
#             138 LOAD_FAST                3 (@py_assert1)
#             140 LOAD_FAST                4 (@py_assert4)
#             142 BUILD_TUPLE              2
#             144 CALL                     4
#             152 LOAD_CONST               5 ('result')
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
#         >>  280 LOAD_CONST               5 ('result')
#         >>  282 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             292 LOAD_ATTR               16 (_saferepr)
#             312 LOAD_FAST                3 (@py_assert1)
#             314 CALL                     1
#             322 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             332 LOAD_ATTR               16 (_saferepr)
#             352 LOAD_FAST                4 (@py_assert4)
#             354 CALL                     1
#             362 LOAD_CONST               6 (('py0', 'py2', 'py5'))
#             364 BUILD_CONST_KEY_MAP      3
#             366 BINARY_OP                6 (%)
#             370 STORE_FAST               6 (@py_format6)
#             372 LOAD_CONST               7 ('assert %(py7)s')
#             374 LOAD_CONST               8 ('py7')
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
#             458 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_config_failure at 0x3af9d830, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 124>:
# 124           0 RESUME                   0
# 
# 125           2 LOAD_GLOBAL              1 (NULL + MockAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
# 126          22 LOAD_FAST                1 (adapter)
#              24 LOAD_ATTR                3 (NULL|self + validate_config)
#              44 LOAD_CONST               1 ('invalid')
#              46 LOAD_CONST               2 (True)
#              48 BUILD_MAP                1
#              50 CALL                     1
#              58 STORE_FAST               2 (result)
# 
# 127          60 LOAD_FAST                2 (result)
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
# 128         458 LOAD_FAST                2 (result)
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
# Disassembly of <code object test_get_supported_simulations at 0x3af9a2d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_base.py", line 130>:
# 130           0 RESUME                   0
# 
# 131           2 LOAD_GLOBAL              1 (NULL + MockAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
# 132          22 LOAD_FAST                1 (adapter)
#              24 LOAD_ATTR                3 (NULL|self + get_supported_simulations)
#              44 CALL                     0
#              52 STORE_FAST               2 (sims)
# 
# 133          54 LOAD_GLOBAL              5 (NULL + isinstance)
#              64 LOAD_FAST                2 (sims)
#              66 LOAD_GLOBAL              6 (list)
#              76 CALL                     2
#              84 STORE_FAST               3 (@py_assert3)
#              86 LOAD_FAST                3 (@py_assert3)
#              88 EXTENDED_ARG             1
#              90 POP_JUMP_IF_TRUE       267 (to 626)
#              92 LOAD_CONST               1 ('assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}')
#              94 LOAD_CONST               2 ('isinstance')
#              96 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             106 LOAD_ATTR               10 (locals)
#             126 CALL                     0
#             134 CONTAINS_OP              0
#             136 POP_JUMP_IF_TRUE        25 (to 188)
#             138 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             148 LOAD_ATTR               14 (_should_repr_global_name)
#             168 LOAD_GLOBAL              4 (isinstance)
#             178 CALL                     1
#             186 POP_JUMP_IF_FALSE       25 (to 238)
#         >>  188 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             198 LOAD_ATTR               16 (_saferepr)
#             218 LOAD_GLOBAL              4 (isinstance)
#             228 CALL                     1
#             236 JUMP_FORWARD             1 (to 240)
#         >>  238 LOAD_CONST               2 ('isinstance')
#         >>  240 LOAD_CONST               3 ('sims')
#             242 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             252 LOAD_ATTR               10 (locals)
#             272 CALL                     0
#             280 CONTAINS_OP              0
#             282 POP_JUMP_IF_TRUE        21 (to 326)
#             284 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             294 LOAD_ATTR               14 (_should_repr_global_name)
#             314 LOAD_FAST                2 (sims)
#             316 CALL                     1
#             324 POP_JUMP_IF_FALSE       21 (to 368)
#         >>  326 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             336 LOAD_ATTR               16 (_saferepr)
#             356 LOAD_FAST                2 (sims)
#             358 CALL                     1
#             366 JUMP_FORWARD             1 (to 370)
#         >>  368 LOAD_CONST               3 ('sims')
#         >>  370 LOAD_CONST               4 ('list')
#             372 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             382 LOAD_ATTR               10 (locals)
#             402 CALL                     0
#             410 CONTAINS_OP              0
#             412 POP_JUMP_IF_TRUE        25 (to 464)
#             414 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             424 LOAD_ATTR               14 (_should_repr_global_name)
#             444 LOAD_GLOBAL              6 (list)
#             454 CALL                     1
#             462 POP_JUMP_IF_FALSE       25 (to 514)
#         >>  464 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             474 LOAD_ATTR               16 (_saferepr)
#             494 LOAD_GLOBAL              6 (list)
#             504 CALL                     1
#             512 JUMP_FORWARD             1 (to 516)
#         >>  514 LOAD_CONST               4 ('list')
#         >>  516 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             526 LOAD_ATTR               16 (_saferepr)
#             546 LOAD_FAST                3 (@py_assert3)
#             548 CALL                     1
#             556 LOAD_CONST               5 (('py0', 'py1', 'py2', 'py4'))
#             558 BUILD_CONST_KEY_MAP      4
#             560 BINARY_OP                6 (%)
#             564 STORE_FAST               4 (@py_format5)
#             566 LOAD_GLOBAL             19 (NULL + AssertionError)
#             576 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             586 LOAD_ATTR               20 (_format_explanation)
#             606 LOAD_FAST                4 (@py_format5)
#             608 CALL                     1
#             616 CALL                     1
#             624 RAISE_VARARGS            1
#         >>  626 LOAD_CONST               0 (None)
#             628 STORE_FAST               3 (@py_assert3)
#             630 RETURN_CONST             0 (None)
# 