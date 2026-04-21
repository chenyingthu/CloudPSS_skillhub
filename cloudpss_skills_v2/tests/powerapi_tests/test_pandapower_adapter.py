# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/__pycache__/test_pandapower_adapter.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


def TestPandapowerAdapterLifecycle():
    """TestPandapowerAdapterLifecycle"""
pass  # TODO: restore


def TestPandapowerAdapterCase14():
    """TestPandapowerAdapterCase14"""
pass  # TODO: restore


def TestPandapowerAdapterCase39():
    """TestPandapowerAdapterCase39"""
pass  # TODO: restore


def TestPandapowerAdapterNetworkInput():
    """TestPandapowerAdapterNetworkInput"""
pass  # TODO: restore


def TestPandapowerAdapterValidation():
    """TestPandapowerAdapterValidation"""
pass  # TODO: restore


def TestPandapowerAdapterViaFactory():
    """TestPandapowerAdapterViaFactory"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('\nTests for PandapowerPowerFlowAdapter.\n\nREAL tests using actual pp.runpp() on pandapower built-in IEEE cases.\nNo mocks — every test exercises the full pandapower → DataLib pipeline.\n')
#               4 STORE_NAME               0 (__doc__)
# 
#   8           6 LOAD_CONST               1 (0)
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
#  10          40 LOAD_CONST               1 (0)
#              42 LOAD_CONST               3 (('SimulationStatus', 'SimulationType'))
#              44 IMPORT_NAME              8 (cloudpss_skills_v2.powerapi)
#              46 IMPORT_FROM              9 (SimulationStatus)
#              48 STORE_NAME               9 (SimulationStatus)
#              50 IMPORT_FROM             10 (SimulationType)
#              52 STORE_NAME              10 (SimulationType)
#              54 POP_TOP
# 
#  14          56 LOAD_CONST               1 (0)
#              58 LOAD_CONST               4 (('PandapowerPowerFlowAdapter',))
#              60 IMPORT_NAME             11 (cloudpss_skills_v2.powerapi.adapters.pandapower)
#              62 IMPORT_FROM             12 (PandapowerPowerFlowAdapter)
#              64 STORE_NAME              12 (PandapowerPowerFlowAdapter)
#              66 POP_TOP
# 
#  15          68 LOAD_CONST               1 (0)
#              70 LOAD_CONST               5 (('BusData', 'BranchData', 'BusType', 'BranchType', 'GeneratorData', 'NetworkSummary'))
#              72 IMPORT_NAME             13 (cloudpss_skills_v2.libs.data_lib)
#              74 IMPORT_FROM             14 (BusData)
#              76 STORE_NAME              14 (BusData)
#              78 IMPORT_FROM             15 (BranchData)
#              80 STORE_NAME              15 (BranchData)
#              82 IMPORT_FROM             16 (BusType)
#              84 STORE_NAME              16 (BusType)
#              86 IMPORT_FROM             17 (BranchType)
#              88 STORE_NAME              17 (BranchType)
#              90 IMPORT_FROM             18 (GeneratorData)
#              92 STORE_NAME              18 (GeneratorData)
#              94 IMPORT_FROM             19 (NetworkSummary)
#              96 STORE_NAME              19 (NetworkSummary)
#              98 POP_TOP
# 
#  25         100 PUSH_NULL
#             102 LOAD_BUILD_CLASS
#             104 LOAD_CONST               6 (<code object TestPandapowerAdapterLifecycle at 0x73cd93b066a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 25>)
#             106 MAKE_FUNCTION            0
#             108 LOAD_CONST               7 ('TestPandapowerAdapterLifecycle')
#             110 CALL                     2
#             118 STORE_NAME              20 (TestPandapowerAdapterLifecycle)
# 
#  51         120 PUSH_NULL
#             122 LOAD_BUILD_CLASS
#             124 LOAD_CONST               8 (<code object TestPandapowerAdapterCase14 at 0x73cd93b013e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 51>)
#             126 MAKE_FUNCTION            0
#             128 LOAD_CONST               9 ('TestPandapowerAdapterCase14')
#             130 CALL                     2
#             138 STORE_NAME              21 (TestPandapowerAdapterCase14)
# 
# 135         140 PUSH_NULL
#             142 LOAD_BUILD_CLASS
#             144 LOAD_CONST              10 (<code object TestPandapowerAdapterCase39 at 0x73cd93b44e70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 135>)
#             146 MAKE_FUNCTION            0
#             148 LOAD_CONST              11 ('TestPandapowerAdapterCase39')
#             150 CALL                     2
#             158 STORE_NAME              22 (TestPandapowerAdapterCase39)
# 
# 173         160 PUSH_NULL
#             162 LOAD_BUILD_CLASS
#             164 LOAD_CONST              12 (<code object TestPandapowerAdapterNetworkInput at 0x73cd93b065b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 173>)
#             166 MAKE_FUNCTION            0
#             168 LOAD_CONST              13 ('TestPandapowerAdapterNetworkInput')
#             170 CALL                     2
#             178 STORE_NAME              23 (TestPandapowerAdapterNetworkInput)
# 
# 205         180 PUSH_NULL
#             182 LOAD_BUILD_CLASS
#             184 LOAD_CONST              14 (<code object TestPandapowerAdapterValidation at 0x73cd93b06970, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 205>)
#             186 MAKE_FUNCTION            0
#             188 LOAD_CONST              15 ('TestPandapowerAdapterValidation')
#             190 CALL                     2
#             198 STORE_NAME              24 (TestPandapowerAdapterValidation)
# 
# 232         200 PUSH_NULL
#             202 LOAD_BUILD_CLASS
#             204 LOAD_CONST              16 (<code object TestPandapowerAdapterViaFactory at 0x73cd93b063d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 232>)
#             206 MAKE_FUNCTION            0
#             208 LOAD_CONST              17 ('TestPandapowerAdapterViaFactory')
#             210 CALL                     2
#             218 STORE_NAME              25 (TestPandapowerAdapterViaFactory)
#             220 RETURN_CONST             2 (None)
# 
# Disassembly of <code object TestPandapowerAdapterLifecycle at 0x73cd93b066a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 25>:
#  25           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestPandapowerAdapterLifecycle')
#               8 STORE_NAME               2 (__qualname__)
# 
#  26          10 LOAD_CONST               1 (<code object test_connect_succeeds at 0x3af95520, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 26>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_connect_succeeds)
# 
#  31          16 LOAD_CONST               2 (<code object test_disconnect_clears_state at 0x3af97180, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 31>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_disconnect_clears_state)
# 
#  37          22 LOAD_CONST               3 (<code object test_context_manager at 0x3af8f430, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 37>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_context_manager)
# 
#  42          28 LOAD_CONST               4 (<code object test_engine_name at 0x3af3fb70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 42>)
#              30 MAKE_FUNCTION            0
#              32 STORE_NAME               6 (test_engine_name)
# 
#  46          34 LOAD_CONST               5 (<code object test_supported_simulations at 0x3af96e20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 46>)
#              36 MAKE_FUNCTION            0
#              38 STORE_NAME               7 (test_supported_simulations)
#              40 RETURN_CONST             6 (None)
# 
# Disassembly of <code object test_connect_succeeds at 0x3af95520, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 26>:
#  26           0 RESUME                   0
# 
#  27           2 LOAD_GLOBAL              1 (NULL + PandapowerPowerFlowAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
#  28          22 LOAD_FAST                1 (adapter)
#              24 LOAD_ATTR                3 (NULL|self + connect)
#              44 CALL                     0
#              52 POP_TOP
# 
#  29          54 LOAD_FAST                1 (adapter)
#              56 LOAD_ATTR                4 (is_connected)
#              76 STORE_FAST               2 (@py_assert1)
#              78 PUSH_NULL
#              80 LOAD_FAST                2 (@py_assert1)
#              82 CALL                     0
#              90 STORE_FAST               3 (@py_assert3)
#              92 LOAD_FAST                3 (@py_assert3)
#              94 POP_JUMP_IF_TRUE       141 (to 378)
#              96 LOAD_CONST               1 ('assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_connected\n}()\n}')
#              98 LOAD_CONST               2 ('adapter')
#             100 LOAD_GLOBAL              7 (NULL + @py_builtins)
#             110 LOAD_ATTR                8 (locals)
#             130 CALL                     0
#             138 CONTAINS_OP              0
#             140 POP_JUMP_IF_TRUE        21 (to 184)
#             142 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             152 LOAD_ATTR               12 (_should_repr_global_name)
#             172 LOAD_FAST                1 (adapter)
#             174 CALL                     1
#             182 POP_JUMP_IF_FALSE       21 (to 226)
#         >>  184 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             194 LOAD_ATTR               14 (_saferepr)
#             214 LOAD_FAST                1 (adapter)
#             216 CALL                     1
#             224 JUMP_FORWARD             1 (to 228)
#         >>  226 LOAD_CONST               2 ('adapter')
#         >>  228 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             238 LOAD_ATTR               14 (_saferepr)
#             258 LOAD_FAST                2 (@py_assert1)
#             260 CALL                     1
#             268 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             278 LOAD_ATTR               14 (_saferepr)
#             298 LOAD_FAST                3 (@py_assert3)
#             300 CALL                     1
#             308 LOAD_CONST               3 (('py0', 'py2', 'py4'))
#             310 BUILD_CONST_KEY_MAP      3
#             312 BINARY_OP                6 (%)
#             316 STORE_FAST               4 (@py_format5)
#             318 LOAD_GLOBAL             17 (NULL + AssertionError)
#             328 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             338 LOAD_ATTR               18 (_format_explanation)
#             358 LOAD_FAST                4 (@py_format5)
#             360 CALL                     1
#             368 CALL                     1
#             376 RAISE_VARARGS            1
#         >>  378 LOAD_CONST               0 (None)
#             380 COPY                     1
#             382 STORE_FAST               2 (@py_assert1)
#             384 STORE_FAST               3 (@py_assert3)
#             386 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_disconnect_clears_state at 0x3af97180, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 31>:
#  31           0 RESUME                   0
# 
#  32           2 LOAD_GLOBAL              1 (NULL + PandapowerPowerFlowAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
#  33          22 LOAD_FAST                1 (adapter)
#              24 LOAD_ATTR                3 (NULL|self + connect)
#              44 CALL                     0
#              52 POP_TOP
# 
#  34          54 LOAD_FAST                1 (adapter)
#              56 LOAD_ATTR                5 (NULL|self + disconnect)
#              76 CALL                     0
#              84 POP_TOP
# 
#  35          86 LOAD_FAST                1 (adapter)
#              88 LOAD_ATTR                6 (is_connected)
#             108 STORE_FAST               2 (@py_assert1)
#             110 PUSH_NULL
#             112 LOAD_FAST                2 (@py_assert1)
#             114 CALL                     0
#             122 STORE_FAST               3 (@py_assert3)
#             124 LOAD_FAST                3 (@py_assert3)
#             126 UNARY_NOT
#             128 STORE_FAST               4 (@py_assert5)
#             130 LOAD_FAST                4 (@py_assert5)
#             132 POP_JUMP_IF_TRUE       141 (to 416)
#             134 LOAD_CONST               1 ('assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_connected\n}()\n}')
#             136 LOAD_CONST               2 ('adapter')
#             138 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             148 LOAD_ATTR               10 (locals)
#             168 CALL                     0
#             176 CONTAINS_OP              0
#             178 POP_JUMP_IF_TRUE        21 (to 222)
#             180 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             190 LOAD_ATTR               14 (_should_repr_global_name)
#             210 LOAD_FAST                1 (adapter)
#             212 CALL                     1
#             220 POP_JUMP_IF_FALSE       21 (to 264)
#         >>  222 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             232 LOAD_ATTR               16 (_saferepr)
#             252 LOAD_FAST                1 (adapter)
#             254 CALL                     1
#             262 JUMP_FORWARD             1 (to 266)
#         >>  264 LOAD_CONST               2 ('adapter')
#         >>  266 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             276 LOAD_ATTR               16 (_saferepr)
#             296 LOAD_FAST                2 (@py_assert1)
#             298 CALL                     1
#             306 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             316 LOAD_ATTR               16 (_saferepr)
#             336 LOAD_FAST                3 (@py_assert3)
#             338 CALL                     1
#             346 LOAD_CONST               3 (('py0', 'py2', 'py4'))
#             348 BUILD_CONST_KEY_MAP      3
#             350 BINARY_OP                6 (%)
#             354 STORE_FAST               5 (@py_format6)
#             356 LOAD_GLOBAL             19 (NULL + AssertionError)
#             366 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             376 LOAD_ATTR               20 (_format_explanation)
#             396 LOAD_FAST                5 (@py_format6)
#             398 CALL                     1
#             406 CALL                     1
#             414 RAISE_VARARGS            1
#         >>  416 LOAD_CONST               0 (None)
#             418 COPY                     1
#             420 STORE_FAST               2 (@py_assert1)
#             422 COPY                     1
#             424 STORE_FAST               3 (@py_assert3)
#             426 STORE_FAST               4 (@py_assert5)
#             428 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_context_manager at 0x3af8f430, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 37>:
#  37           0 RESUME                   0
# 
#  38           2 LOAD_GLOBAL              1 (NULL + PandapowerPowerFlowAdapter)
#              12 CALL                     0
#              20 BEFORE_WITH
#              22 STORE_FAST               1 (adapter)
# 
#  39          24 LOAD_FAST                1 (adapter)
#              26 LOAD_ATTR                2 (is_connected)
#              46 STORE_FAST               2 (@py_assert1)
#              48 PUSH_NULL
#              50 LOAD_FAST                2 (@py_assert1)
#              52 CALL                     0
#              60 STORE_FAST               3 (@py_assert3)
#              62 LOAD_FAST                3 (@py_assert3)
#              64 POP_JUMP_IF_TRUE       141 (to 348)
#              66 LOAD_CONST               1 ('assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_connected\n}()\n}')
#              68 LOAD_CONST               2 ('adapter')
#              70 LOAD_GLOBAL              5 (NULL + @py_builtins)
#              80 LOAD_ATTR                6 (locals)
#             100 CALL                     0
#             108 CONTAINS_OP              0
#             110 POP_JUMP_IF_TRUE        21 (to 154)
#             112 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             122 LOAD_ATTR               10 (_should_repr_global_name)
#             142 LOAD_FAST                1 (adapter)
#             144 CALL                     1
#             152 POP_JUMP_IF_FALSE       21 (to 196)
#         >>  154 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             164 LOAD_ATTR               12 (_saferepr)
#             184 LOAD_FAST                1 (adapter)
#             186 CALL                     1
#             194 JUMP_FORWARD             1 (to 198)
#         >>  196 LOAD_CONST               2 ('adapter')
#         >>  198 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             208 LOAD_ATTR               12 (_saferepr)
#             228 LOAD_FAST                2 (@py_assert1)
#             230 CALL                     1
#             238 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             248 LOAD_ATTR               12 (_saferepr)
#             268 LOAD_FAST                3 (@py_assert3)
#             270 CALL                     1
#             278 LOAD_CONST               3 (('py0', 'py2', 'py4'))
#             280 BUILD_CONST_KEY_MAP      3
#             282 BINARY_OP                6 (%)
#             286 STORE_FAST               4 (@py_format5)
#             288 LOAD_GLOBAL             15 (NULL + AssertionError)
#             298 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             308 LOAD_ATTR               16 (_format_explanation)
#             328 LOAD_FAST                4 (@py_format5)
#             330 CALL                     1
#             338 CALL                     1
#             346 RAISE_VARARGS            1
#         >>  348 LOAD_CONST               0 (None)
#             350 COPY                     1
#             352 STORE_FAST               2 (@py_assert1)
#             354 STORE_FAST               3 (@py_assert3)
# 
#  38         356 LOAD_CONST               0 (None)
#             358 LOAD_CONST               0 (None)
#             360 LOAD_CONST               0 (None)
#             362 CALL                     2
#             370 POP_TOP
# 
#  40     >>  372 LOAD_FAST_CHECK          1 (adapter)
#             374 LOAD_ATTR                2 (is_connected)
#             394 STORE_FAST               2 (@py_assert1)
#             396 PUSH_NULL
#             398 LOAD_FAST                2 (@py_assert1)
#             400 CALL                     0
#             408 STORE_FAST               3 (@py_assert3)
#             410 LOAD_FAST                3 (@py_assert3)
#             412 UNARY_NOT
#             414 STORE_FAST               5 (@py_assert5)
#             416 LOAD_FAST                5 (@py_assert5)
#             418 POP_JUMP_IF_TRUE       141 (to 702)
#             420 LOAD_CONST               4 ('assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_connected\n}()\n}')
#             422 LOAD_CONST               2 ('adapter')
#             424 LOAD_GLOBAL              5 (NULL + @py_builtins)
#             434 LOAD_ATTR                6 (locals)
#             454 CALL                     0
#             462 CONTAINS_OP              0
#             464 POP_JUMP_IF_TRUE        21 (to 508)
#             466 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             476 LOAD_ATTR               10 (_should_repr_global_name)
#             496 LOAD_FAST                1 (adapter)
#             498 CALL                     1
#             506 POP_JUMP_IF_FALSE       21 (to 550)
#         >>  508 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             518 LOAD_ATTR               12 (_saferepr)
#             538 LOAD_FAST                1 (adapter)
#             540 CALL                     1
#             548 JUMP_FORWARD             1 (to 552)
#         >>  550 LOAD_CONST               2 ('adapter')
#         >>  552 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             562 LOAD_ATTR               12 (_saferepr)
#             582 LOAD_FAST                2 (@py_assert1)
#             584 CALL                     1
#             592 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             602 LOAD_ATTR               12 (_saferepr)
#             622 LOAD_FAST                3 (@py_assert3)
#             624 CALL                     1
#             632 LOAD_CONST               3 (('py0', 'py2', 'py4'))
#             634 BUILD_CONST_KEY_MAP      3
#             636 BINARY_OP                6 (%)
#             640 STORE_FAST               6 (@py_format6)
#             642 LOAD_GLOBAL             15 (NULL + AssertionError)
#             652 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             662 LOAD_ATTR               16 (_format_explanation)
#             682 LOAD_FAST                6 (@py_format6)
#             684 CALL                     1
#             692 CALL                     1
#             700 RAISE_VARARGS            1
#         >>  702 LOAD_CONST               0 (None)
#             704 COPY                     1
#             706 STORE_FAST               2 (@py_assert1)
#             708 COPY                     1
#             710 STORE_FAST               3 (@py_assert3)
#             712 STORE_FAST               5 (@py_assert5)
#             714 RETURN_CONST             0 (None)
# 
#  38     >>  716 PUSH_EXC_INFO
#             718 WITH_EXCEPT_START
#             720 POP_JUMP_IF_TRUE         1 (to 724)
#             722 RERAISE                  2
#         >>  724 POP_TOP
#             726 POP_EXCEPT
#             728 POP_TOP
#             730 POP_TOP
#             732 JUMP_BACKWARD          181 (to 372)
#         >>  734 COPY                     3
#             736 POP_EXCEPT
#             738 RERAISE                  1
# ExceptionTable:
#   22 to 354 -> 716 [1] lasti
#   716 to 724 -> 734 [3] lasti
# 
# Disassembly of <code object test_engine_name at 0x3af3fb70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 42>:
#  42           0 RESUME                   0
# 
#  43           2 LOAD_GLOBAL              1 (NULL + PandapowerPowerFlowAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
#  44          22 LOAD_FAST                1 (adapter)
#              24 LOAD_ATTR                2 (engine_name)
#              44 STORE_FAST               2 (@py_assert1)
#              46 LOAD_CONST               1 ('pandapower')
#              48 STORE_FAST               3 (@py_assert4)
#              50 LOAD_FAST                2 (@py_assert1)
#              52 LOAD_FAST                3 (@py_assert4)
#              54 COMPARE_OP              40 (==)
#              58 STORE_FAST               4 (@py_assert3)
#              60 LOAD_FAST                4 (@py_assert3)
#              62 POP_JUMP_IF_TRUE       173 (to 410)
#              64 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              74 LOAD_ATTR                6 (_call_reprcompare)
#              94 LOAD_CONST               2 (('==',))
#              96 LOAD_FAST                4 (@py_assert3)
#              98 BUILD_TUPLE              1
#             100 LOAD_CONST               3 (('%(py2)s\n{%(py2)s = %(py0)s.engine_name\n} == %(py5)s',))
#             102 LOAD_FAST                2 (@py_assert1)
#             104 LOAD_FAST                3 (@py_assert4)
#             106 BUILD_TUPLE              2
#             108 CALL                     4
#             116 LOAD_CONST               4 ('adapter')
#             118 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             128 LOAD_ATTR               10 (locals)
#             148 CALL                     0
#             156 CONTAINS_OP              0
#             158 POP_JUMP_IF_TRUE        21 (to 202)
#             160 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             170 LOAD_ATTR               12 (_should_repr_global_name)
#             190 LOAD_FAST                1 (adapter)
#             192 CALL                     1
#             200 POP_JUMP_IF_FALSE       21 (to 244)
#         >>  202 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             212 LOAD_ATTR               14 (_saferepr)
#             232 LOAD_FAST                1 (adapter)
#             234 CALL                     1
#             242 JUMP_FORWARD             1 (to 246)
#         >>  244 LOAD_CONST               4 ('adapter')
#         >>  246 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             256 LOAD_ATTR               14 (_saferepr)
#             276 LOAD_FAST                2 (@py_assert1)
#             278 CALL                     1
#             286 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             296 LOAD_ATTR               14 (_saferepr)
#             316 LOAD_FAST                3 (@py_assert4)
#             318 CALL                     1
#             326 LOAD_CONST               5 (('py0', 'py2', 'py5'))
#             328 BUILD_CONST_KEY_MAP      3
#             330 BINARY_OP                6 (%)
#             334 STORE_FAST               5 (@py_format6)
#             336 LOAD_CONST               6 ('assert %(py7)s')
#             338 LOAD_CONST               7 ('py7')
#             340 LOAD_FAST                5 (@py_format6)
#             342 BUILD_MAP                1
#             344 BINARY_OP                6 (%)
#             348 STORE_FAST               6 (@py_format8)
#             350 LOAD_GLOBAL             17 (NULL + AssertionError)
#             360 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             370 LOAD_ATTR               18 (_format_explanation)
#             390 LOAD_FAST                6 (@py_format8)
#             392 CALL                     1
#             400 CALL                     1
#             408 RAISE_VARARGS            1
#         >>  410 LOAD_CONST               0 (None)
#             412 COPY                     1
#             414 STORE_FAST               2 (@py_assert1)
#             416 COPY                     1
#             418 STORE_FAST               4 (@py_assert3)
#             420 STORE_FAST               3 (@py_assert4)
#             422 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_supported_simulations at 0x3af96e20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 46>:
#  46           0 RESUME                   0
# 
#  47           2 LOAD_GLOBAL              1 (NULL + PandapowerPowerFlowAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
#  48          22 LOAD_GLOBAL              2 (SimulationType)
#              32 LOAD_ATTR                4 (POWER_FLOW)
#              52 STORE_FAST               2 (@py_assert1)
#              54 LOAD_FAST                1 (adapter)
#              56 LOAD_ATTR                6 (get_supported_simulations)
#              76 STORE_FAST               3 (@py_assert5)
#              78 PUSH_NULL
#              80 LOAD_FAST                3 (@py_assert5)
#              82 CALL                     0
#              90 STORE_FAST               4 (@py_assert7)
#              92 LOAD_FAST                2 (@py_assert1)
#              94 LOAD_FAST                4 (@py_assert7)
#              96 CONTAINS_OP              0
#              98 STORE_FAST               5 (@py_assert3)
#             100 LOAD_FAST                5 (@py_assert3)
#             102 EXTENDED_ARG             1
#             104 POP_JUMP_IF_TRUE       266 (to 638)
#             106 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             116 LOAD_ATTR               10 (_call_reprcompare)
#             136 LOAD_CONST               1 (('in',))
#             138 LOAD_FAST                5 (@py_assert3)
#             140 BUILD_TUPLE              1
#             142 LOAD_CONST               2 (('%(py2)s\n{%(py2)s = %(py0)s.POWER_FLOW\n} in %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.get_supported_simulations\n}()\n}',))
#             144 LOAD_FAST                2 (@py_assert1)
#             146 LOAD_FAST                4 (@py_assert7)
#             148 BUILD_TUPLE              2
#             150 CALL                     4
#             158 LOAD_CONST               3 ('SimulationType')
#             160 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             170 LOAD_ATTR               14 (locals)
#             190 CALL                     0
#             198 CONTAINS_OP              0
#             200 POP_JUMP_IF_TRUE        25 (to 252)
#             202 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             212 LOAD_ATTR               16 (_should_repr_global_name)
#             232 LOAD_GLOBAL              2 (SimulationType)
#             242 CALL                     1
#             250 POP_JUMP_IF_FALSE       25 (to 302)
#         >>  252 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             262 LOAD_ATTR               18 (_saferepr)
#             282 LOAD_GLOBAL              2 (SimulationType)
#             292 CALL                     1
#             300 JUMP_FORWARD             1 (to 304)
#         >>  302 LOAD_CONST               3 ('SimulationType')
#         >>  304 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             314 LOAD_ATTR               18 (_saferepr)
#             334 LOAD_FAST                2 (@py_assert1)
#             336 CALL                     1
#             344 LOAD_CONST               4 ('adapter')
#             346 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             356 LOAD_ATTR               14 (locals)
#             376 CALL                     0
#             384 CONTAINS_OP              0
#             386 POP_JUMP_IF_TRUE        21 (to 430)
#             388 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             398 LOAD_ATTR               16 (_should_repr_global_name)
#             418 LOAD_FAST                1 (adapter)
#             420 CALL                     1
#             428 POP_JUMP_IF_FALSE       21 (to 472)
#         >>  430 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             440 LOAD_ATTR               18 (_saferepr)
#             460 LOAD_FAST                1 (adapter)
#             462 CALL                     1
#             470 JUMP_FORWARD             1 (to 474)
#         >>  472 LOAD_CONST               4 ('adapter')
#         >>  474 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             484 LOAD_ATTR               18 (_saferepr)
#             504 LOAD_FAST                3 (@py_assert5)
#             506 CALL                     1
#             514 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             524 LOAD_ATTR               18 (_saferepr)
#             544 LOAD_FAST                4 (@py_assert7)
#             546 CALL                     1
#             554 LOAD_CONST               5 (('py0', 'py2', 'py4', 'py6', 'py8'))
#             556 BUILD_CONST_KEY_MAP      5
#             558 BINARY_OP                6 (%)
#             562 STORE_FAST               6 (@py_format9)
#             564 LOAD_CONST               6 ('assert %(py10)s')
#             566 LOAD_CONST               7 ('py10')
#             568 LOAD_FAST                6 (@py_format9)
#             570 BUILD_MAP                1
#             572 BINARY_OP                6 (%)
#             576 STORE_FAST               7 (@py_format11)
#             578 LOAD_GLOBAL             21 (NULL + AssertionError)
#             588 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             598 LOAD_ATTR               22 (_format_explanation)
#             618 LOAD_FAST                7 (@py_format11)
#             620 CALL                     1
#             628 CALL                     1
#             636 RAISE_VARARGS            1
#         >>  638 LOAD_CONST               0 (None)
#             640 COPY                     1
#             642 STORE_FAST               2 (@py_assert1)
#             644 COPY                     1
#             646 STORE_FAST               5 (@py_assert3)
#             648 COPY                     1
#             650 STORE_FAST               3 (@py_assert5)
#             652 STORE_FAST               4 (@py_assert7)
#             654 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestPandapowerAdapterCase14 at 0x73cd93b013e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 51>:
#  51           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestPandapowerAdapterCase14')
#               8 STORE_NAME               2 (__qualname__)
# 
#  52          10 LOAD_CONST               1 ('\n    IEEE 14-bus case — smallest standard test case.\n    Known results: 14 buses, 20 branches, 5 generators, converges.\n    ')
#              12 STORE_NAME               3 (__doc__)
# 
#  57          14 PUSH_NULL
#              16 LOAD_NAME                4 (pytest)
#              18 LOAD_ATTR               10 (fixture)
#              38 LOAD_CONST               2 (True)
#              40 KW_NAMES                 3 (('autouse',))
#              42 CALL                     1
# 
#  58          50 LOAD_CONST               4 (<code object setup at 0x73cd948d3730, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 57>)
#              52 MAKE_FUNCTION            0
# 
#  57          54 CALL                     0
# 
#  58          62 STORE_NAME               6 (setup)
# 
#  63          64 LOAD_CONST               5 (<code object test_converges at 0x3af9c250, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 63>)
#              66 MAKE_FUNCTION            0
#              68 STORE_NAME               7 (test_converges)
# 
#  68          70 LOAD_CONST               6 (<code object test_bus_count at 0x3aef8c90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 68>)
#              72 MAKE_FUNCTION            0
#              74 STORE_NAME               8 (test_bus_count)
# 
#  71          76 LOAD_CONST               7 (<code object test_branch_count at 0x3aef8860, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 71>)
#              78 MAKE_FUNCTION            0
#              80 STORE_NAME               9 (test_branch_count)
# 
#  74          82 LOAD_CONST               8 (<code object test_voltage_range_reasonable at 0x3af9d7e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 74>)
#              84 MAKE_FUNCTION            0
#              86 STORE_NAME              10 (test_voltage_range_reasonable)
# 
#  81          88 LOAD_CONST               9 (<code object test_slack_bus_identified at 0x3af981b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 81>)
#              90 MAKE_FUNCTION            0
#              92 STORE_NAME              11 (test_slack_bus_identified)
# 
#  86          94 LOAD_CONST              10 (<code object test_pv_buses_identified at 0x3af95b80, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 86>)
#              96 MAKE_FUNCTION            0
#              98 STORE_NAME              12 (test_pv_buses_identified)
# 
#  91         100 LOAD_CONST              11 (<code object test_losses_positive at 0x3aefd020, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 91>)
#             102 MAKE_FUNCTION            0
#             104 STORE_NAME              13 (test_losses_positive)
# 
#  96         106 LOAD_CONST              12 (<code object test_total_loss_matches_summary at 0x3af9bd40, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 96>)
#             108 MAKE_FUNCTION            0
#             110 STORE_NAME              14 (test_total_loss_matches_summary)
# 
# 102         112 LOAD_CONST              13 (<code object test_generation_exceeds_load at 0x73cd948baa30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 102>)
#             114 MAKE_FUNCTION            0
#             116 STORE_NAME              15 (test_generation_exceeds_load)
# 
# 106         118 LOAD_CONST              14 (<code object test_generator_count at 0x3aef4bd0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 106>)
#             120 MAKE_FUNCTION            0
#             122 STORE_NAME              16 (test_generator_count)
# 
# 109         124 LOAD_CONST              15 (<code object test_bus_data_roundtrip at 0x3af9f460, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 109>)
#             126 MAKE_FUNCTION            0
#             128 STORE_NAME              17 (test_bus_data_roundtrip)
# 
# 117         130 LOAD_CONST              16 (<code object test_branch_data_roundtrip at 0x3af9fb50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 117>)
#             132 MAKE_FUNCTION            0
#             134 STORE_NAME              18 (test_branch_data_roundtrip)
# 
# 125         136 LOAD_CONST              17 (<code object test_generator_data_roundtrip at 0x3afa4860, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 125>)
#             138 MAKE_FUNCTION            0
#             140 STORE_NAME              19 (test_generator_data_roundtrip)
#             142 RETURN_CONST            18 (None)
# 
# Disassembly of <code object setup at 0x73cd948d3730, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 57>:
#  57           0 RESUME                   0
# 
#  59           2 LOAD_GLOBAL              1 (NULL + PandapowerPowerFlowAdapter)
#              12 CALL                     0
#              20 LOAD_FAST                0 (self)
#              22 STORE_ATTR               1 (adapter)
# 
#  60          32 LOAD_FAST                0 (self)
#              34 LOAD_ATTR                2 (adapter)
#              54 LOAD_ATTR                5 (NULL|self + connect)
#              74 CALL                     0
#              82 POP_TOP
# 
#  61          84 LOAD_FAST                0 (self)
#              86 LOAD_ATTR                2 (adapter)
#             106 LOAD_ATTR                7 (NULL|self + run_simulation)
#             126 LOAD_CONST               1 ('case')
#             128 LOAD_CONST               2 ('case14')
#             130 BUILD_MAP                1
#             132 CALL                     1
#             140 LOAD_FAST                0 (self)
#             142 STORE_ATTR               4 (result)
#             152 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_converges at 0x3af9c250, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 63>:
#  63           0 RESUME                   0
# 
#  64           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 STORE_FAST               1 (@py_assert1)
#              26 LOAD_FAST                1 (@py_assert1)
#              28 LOAD_ATTR                2 (status)
#              48 STORE_FAST               2 (@py_assert3)
#              50 LOAD_GLOBAL              4 (SimulationStatus)
#              60 LOAD_ATTR                6 (COMPLETED)
#              80 STORE_FAST               3 (@py_assert7)
#              82 LOAD_FAST                2 (@py_assert3)
#              84 LOAD_FAST                3 (@py_assert7)
#              86 COMPARE_OP              40 (==)
#              90 STORE_FAST               4 (@py_assert5)
#              92 LOAD_FAST                4 (@py_assert5)
#              94 EXTENDED_ARG             1
#              96 POP_JUMP_IF_TRUE       266 (to 630)
#              98 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             108 LOAD_ATTR               10 (_call_reprcompare)
#             128 LOAD_CONST               1 (('==',))
#             130 LOAD_FAST                4 (@py_assert5)
#             132 BUILD_TUPLE              1
#             134 LOAD_CONST               2 (('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.result\n}.status\n} == %(py8)s\n{%(py8)s = %(py6)s.COMPLETED\n}',))
#             136 LOAD_FAST                2 (@py_assert3)
#             138 LOAD_FAST                3 (@py_assert7)
#             140 BUILD_TUPLE              2
#             142 CALL                     4
#             150 LOAD_CONST               3 ('self')
#             152 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             162 LOAD_ATTR               14 (locals)
#             182 CALL                     0
#             190 CONTAINS_OP              0
#             192 POP_JUMP_IF_TRUE        21 (to 236)
#             194 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             204 LOAD_ATTR               16 (_should_repr_global_name)
#             224 LOAD_FAST                0 (self)
#             226 CALL                     1
#             234 POP_JUMP_IF_FALSE       21 (to 278)
#         >>  236 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             246 LOAD_ATTR               18 (_saferepr)
#             266 LOAD_FAST                0 (self)
#             268 CALL                     1
#             276 JUMP_FORWARD             1 (to 280)
#         >>  278 LOAD_CONST               3 ('self')
#         >>  280 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             290 LOAD_ATTR               18 (_saferepr)
#             310 LOAD_FAST                1 (@py_assert1)
#             312 CALL                     1
#             320 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             330 LOAD_ATTR               18 (_saferepr)
#             350 LOAD_FAST                2 (@py_assert3)
#             352 CALL                     1
#             360 LOAD_CONST               4 ('SimulationStatus')
#             362 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             372 LOAD_ATTR               14 (locals)
#             392 CALL                     0
#             400 CONTAINS_OP              0
#             402 POP_JUMP_IF_TRUE        25 (to 454)
#             404 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             414 LOAD_ATTR               16 (_should_repr_global_name)
#             434 LOAD_GLOBAL              4 (SimulationStatus)
#             444 CALL                     1
#             452 POP_JUMP_IF_FALSE       25 (to 504)
#         >>  454 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             464 LOAD_ATTR               18 (_saferepr)
#             484 LOAD_GLOBAL              4 (SimulationStatus)
#             494 CALL                     1
#             502 JUMP_FORWARD             1 (to 506)
#         >>  504 LOAD_CONST               4 ('SimulationStatus')
#         >>  506 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             516 LOAD_ATTR               18 (_saferepr)
#             536 LOAD_FAST                3 (@py_assert7)
#             538 CALL                     1
#             546 LOAD_CONST               5 (('py0', 'py2', 'py4', 'py6', 'py8'))
#             548 BUILD_CONST_KEY_MAP      5
#             550 BINARY_OP                6 (%)
#             554 STORE_FAST               5 (@py_format9)
#             556 LOAD_CONST               6 ('assert %(py10)s')
#             558 LOAD_CONST               7 ('py10')
#             560 LOAD_FAST                5 (@py_format9)
#             562 BUILD_MAP                1
#             564 BINARY_OP                6 (%)
#             568 STORE_FAST               6 (@py_format11)
#             570 LOAD_GLOBAL             21 (NULL + AssertionError)
#             580 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             590 LOAD_ATTR               22 (_format_explanation)
#             610 LOAD_FAST                6 (@py_format11)
#             612 CALL                     1
#             620 CALL                     1
#             628 RAISE_VARARGS            1
#         >>  630 LOAD_CONST               0 (None)
#             632 COPY                     1
#             634 STORE_FAST               1 (@py_assert1)
#             636 COPY                     1
#             638 STORE_FAST               2 (@py_assert3)
#             640 COPY                     1
#             642 STORE_FAST               4 (@py_assert5)
#             644 STORE_FAST               3 (@py_assert7)
# 
#  65         646 LOAD_FAST                0 (self)
#             648 LOAD_ATTR                0 (result)
#             668 STORE_FAST               1 (@py_assert1)
#             670 LOAD_FAST                1 (@py_assert1)
#             672 LOAD_ATTR               24 (is_success)
#             692 STORE_FAST               2 (@py_assert3)
#             694 LOAD_FAST                2 (@py_assert3)
#             696 POP_JUMP_IF_TRUE       141 (to 980)
#             698 LOAD_CONST               8 ('assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.result\n}.is_success\n}')
#             700 LOAD_CONST               3 ('self')
#             702 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             712 LOAD_ATTR               14 (locals)
#             732 CALL                     0
#             740 CONTAINS_OP              0
#             742 POP_JUMP_IF_TRUE        21 (to 786)
#             744 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             754 LOAD_ATTR               16 (_should_repr_global_name)
#             774 LOAD_FAST                0 (self)
#             776 CALL                     1
#             784 POP_JUMP_IF_FALSE       21 (to 828)
#         >>  786 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             796 LOAD_ATTR               18 (_saferepr)
#             816 LOAD_FAST                0 (self)
#             818 CALL                     1
#             826 JUMP_FORWARD             1 (to 830)
#         >>  828 LOAD_CONST               3 ('self')
#         >>  830 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             840 LOAD_ATTR               18 (_saferepr)
#             860 LOAD_FAST                1 (@py_assert1)
#             862 CALL                     1
#             870 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             880 LOAD_ATTR               18 (_saferepr)
#             900 LOAD_FAST                2 (@py_assert3)
#             902 CALL                     1
#             910 LOAD_CONST               9 (('py0', 'py2', 'py4'))
#             912 BUILD_CONST_KEY_MAP      3
#             914 BINARY_OP                6 (%)
#             918 STORE_FAST               7 (@py_format5)
#             920 LOAD_GLOBAL             21 (NULL + AssertionError)
#             930 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             940 LOAD_ATTR               22 (_format_explanation)
#             960 LOAD_FAST                7 (@py_format5)
#             962 CALL                     1
#             970 CALL                     1
#             978 RAISE_VARARGS            1
#         >>  980 LOAD_CONST               0 (None)
#             982 COPY                     1
#             984 STORE_FAST               1 (@py_assert1)
#             986 STORE_FAST               2 (@py_assert3)
# 
#  66         988 LOAD_FAST                0 (self)
#             990 LOAD_ATTR                0 (result)
#            1010 LOAD_ATTR               26 (data)
#            1030 LOAD_CONST              10 ('converged')
#            1032 BINARY_SUBSCR
#            1036 STORE_FAST               8 (@py_assert0)
#            1038 LOAD_CONST              11 (True)
#            1040 STORE_FAST               2 (@py_assert3)
#            1042 LOAD_FAST                8 (@py_assert0)
#            1044 LOAD_FAST                2 (@py_assert3)
#            1046 IS_OP                    0
#            1048 STORE_FAST               9 (@py_assert2)
#            1050 LOAD_FAST                9 (@py_assert2)
#            1052 POP_JUMP_IF_TRUE       108 (to 1270)
#            1054 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1064 LOAD_ATTR               10 (_call_reprcompare)
#            1084 LOAD_CONST              12 (('is',))
#            1086 LOAD_FAST                9 (@py_assert2)
#            1088 BUILD_TUPLE              1
#            1090 LOAD_CONST              13 (('%(py1)s is %(py4)s',))
#            1092 LOAD_FAST                8 (@py_assert0)
#            1094 LOAD_FAST                2 (@py_assert3)
#            1096 BUILD_TUPLE              2
#            1098 CALL                     4
#            1106 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1116 LOAD_ATTR               18 (_saferepr)
#            1136 LOAD_FAST                8 (@py_assert0)
#            1138 CALL                     1
#            1146 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1156 LOAD_ATTR               18 (_saferepr)
#            1176 LOAD_FAST                2 (@py_assert3)
#            1178 CALL                     1
#            1186 LOAD_CONST              14 (('py1', 'py4'))
#            1188 BUILD_CONST_KEY_MAP      2
#            1190 BINARY_OP                6 (%)
#            1194 STORE_FAST               7 (@py_format5)
#            1196 LOAD_CONST              15 ('assert %(py6)s')
#            1198 LOAD_CONST              16 ('py6')
#            1200 LOAD_FAST                7 (@py_format5)
#            1202 BUILD_MAP                1
#            1204 BINARY_OP                6 (%)
#            1208 STORE_FAST              10 (@py_format7)
#            1210 LOAD_GLOBAL             21 (NULL + AssertionError)
#            1220 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1230 LOAD_ATTR               22 (_format_explanation)
#            1250 LOAD_FAST               10 (@py_format7)
#            1252 CALL                     1
#            1260 CALL                     1
#            1268 RAISE_VARARGS            1
#         >> 1270 LOAD_CONST               0 (None)
#            1272 COPY                     1
#            1274 STORE_FAST               8 (@py_assert0)
#            1276 COPY                     1
#            1278 STORE_FAST               9 (@py_assert2)
#            1280 STORE_FAST               2 (@py_assert3)
#            1282 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_bus_count at 0x3aef8c90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 68>:
#  68           0 RESUME                   0
# 
#  69           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('buses')
#              46 BINARY_SUBSCR
#              50 STORE_FAST               1 (@py_assert1)
#              52 LOAD_GLOBAL              5 (NULL + len)
#              62 LOAD_FAST                1 (@py_assert1)
#              64 CALL                     1
#              72 STORE_FAST               2 (@py_assert3)
#              74 LOAD_CONST               2 (14)
#              76 STORE_FAST               3 (@py_assert6)
#              78 LOAD_FAST                2 (@py_assert3)
#              80 LOAD_FAST                3 (@py_assert6)
#              82 COMPARE_OP              40 (==)
#              86 STORE_FAST               4 (@py_assert5)
#              88 LOAD_FAST                4 (@py_assert5)
#              90 POP_JUMP_IF_TRUE       201 (to 494)
#              92 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             102 LOAD_ATTR                8 (_call_reprcompare)
#             122 LOAD_CONST               3 (('==',))
#             124 LOAD_FAST                4 (@py_assert5)
#             126 BUILD_TUPLE              1
#             128 LOAD_CONST               4 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',))
#             130 LOAD_FAST                2 (@py_assert3)
#             132 LOAD_FAST                3 (@py_assert6)
#             134 BUILD_TUPLE              2
#             136 CALL                     4
#             144 LOAD_CONST               5 ('len')
#             146 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             156 LOAD_ATTR               12 (locals)
#             176 CALL                     0
#             184 CONTAINS_OP              0
#             186 POP_JUMP_IF_TRUE        25 (to 238)
#             188 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             198 LOAD_ATTR               14 (_should_repr_global_name)
#             218 LOAD_GLOBAL              4 (len)
#             228 CALL                     1
#             236 POP_JUMP_IF_FALSE       25 (to 288)
#         >>  238 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             248 LOAD_ATTR               16 (_saferepr)
#             268 LOAD_GLOBAL              4 (len)
#             278 CALL                     1
#             286 JUMP_FORWARD             1 (to 290)
#         >>  288 LOAD_CONST               5 ('len')
#         >>  290 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             300 LOAD_ATTR               16 (_saferepr)
#             320 LOAD_FAST                1 (@py_assert1)
#             322 CALL                     1
#             330 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             340 LOAD_ATTR               16 (_saferepr)
#             360 LOAD_FAST                2 (@py_assert3)
#             362 CALL                     1
#             370 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             380 LOAD_ATTR               16 (_saferepr)
#             400 LOAD_FAST                3 (@py_assert6)
#             402 CALL                     1
#             410 LOAD_CONST               6 (('py0', 'py2', 'py4', 'py7'))
#             412 BUILD_CONST_KEY_MAP      4
#             414 BINARY_OP                6 (%)
#             418 STORE_FAST               5 (@py_format8)
#             420 LOAD_CONST               7 ('assert %(py9)s')
#             422 LOAD_CONST               8 ('py9')
#             424 LOAD_FAST                5 (@py_format8)
#             426 BUILD_MAP                1
#             428 BINARY_OP                6 (%)
#             432 STORE_FAST               6 (@py_format10)
#             434 LOAD_GLOBAL             19 (NULL + AssertionError)
#             444 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             454 LOAD_ATTR               20 (_format_explanation)
#             474 LOAD_FAST                6 (@py_format10)
#             476 CALL                     1
#             484 CALL                     1
#             492 RAISE_VARARGS            1
#         >>  494 LOAD_CONST               0 (None)
#             496 COPY                     1
#             498 STORE_FAST               1 (@py_assert1)
#             500 COPY                     1
#             502 STORE_FAST               2 (@py_assert3)
#             504 COPY                     1
#             506 STORE_FAST               4 (@py_assert5)
#             508 STORE_FAST               3 (@py_assert6)
#             510 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_branch_count at 0x3aef8860, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 71>:
#  71           0 RESUME                   0
# 
#  72           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('branches')
#              46 BINARY_SUBSCR
#              50 STORE_FAST               1 (@py_assert1)
#              52 LOAD_GLOBAL              5 (NULL + len)
#              62 LOAD_FAST                1 (@py_assert1)
#              64 CALL                     1
#              72 STORE_FAST               2 (@py_assert3)
#              74 LOAD_CONST               2 (20)
#              76 STORE_FAST               3 (@py_assert6)
#              78 LOAD_FAST                2 (@py_assert3)
#              80 LOAD_FAST                3 (@py_assert6)
#              82 COMPARE_OP              40 (==)
#              86 STORE_FAST               4 (@py_assert5)
#              88 LOAD_FAST                4 (@py_assert5)
#              90 POP_JUMP_IF_TRUE       201 (to 494)
#              92 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             102 LOAD_ATTR                8 (_call_reprcompare)
#             122 LOAD_CONST               3 (('==',))
#             124 LOAD_FAST                4 (@py_assert5)
#             126 BUILD_TUPLE              1
#             128 LOAD_CONST               4 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',))
#             130 LOAD_FAST                2 (@py_assert3)
#             132 LOAD_FAST                3 (@py_assert6)
#             134 BUILD_TUPLE              2
#             136 CALL                     4
#             144 LOAD_CONST               5 ('len')
#             146 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             156 LOAD_ATTR               12 (locals)
#             176 CALL                     0
#             184 CONTAINS_OP              0
#             186 POP_JUMP_IF_TRUE        25 (to 238)
#             188 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             198 LOAD_ATTR               14 (_should_repr_global_name)
#             218 LOAD_GLOBAL              4 (len)
#             228 CALL                     1
#             236 POP_JUMP_IF_FALSE       25 (to 288)
#         >>  238 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             248 LOAD_ATTR               16 (_saferepr)
#             268 LOAD_GLOBAL              4 (len)
#             278 CALL                     1
#             286 JUMP_FORWARD             1 (to 290)
#         >>  288 LOAD_CONST               5 ('len')
#         >>  290 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             300 LOAD_ATTR               16 (_saferepr)
#             320 LOAD_FAST                1 (@py_assert1)
#             322 CALL                     1
#             330 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             340 LOAD_ATTR               16 (_saferepr)
#             360 LOAD_FAST                2 (@py_assert3)
#             362 CALL                     1
#             370 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             380 LOAD_ATTR               16 (_saferepr)
#             400 LOAD_FAST                3 (@py_assert6)
#             402 CALL                     1
#             410 LOAD_CONST               6 (('py0', 'py2', 'py4', 'py7'))
#             412 BUILD_CONST_KEY_MAP      4
#             414 BINARY_OP                6 (%)
#             418 STORE_FAST               5 (@py_format8)
#             420 LOAD_CONST               7 ('assert %(py9)s')
#             422 LOAD_CONST               8 ('py9')
#             424 LOAD_FAST                5 (@py_format8)
#             426 BUILD_MAP                1
#             428 BINARY_OP                6 (%)
#             432 STORE_FAST               6 (@py_format10)
#             434 LOAD_GLOBAL             19 (NULL + AssertionError)
#             444 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             454 LOAD_ATTR               20 (_format_explanation)
#             474 LOAD_FAST                6 (@py_format10)
#             476 CALL                     1
#             484 CALL                     1
#             492 RAISE_VARARGS            1
#         >>  494 LOAD_CONST               0 (None)
#             496 COPY                     1
#             498 STORE_FAST               1 (@py_assert1)
#             500 COPY                     1
#             502 STORE_FAST               2 (@py_assert3)
#             504 COPY                     1
#             506 STORE_FAST               4 (@py_assert5)
#             508 STORE_FAST               3 (@py_assert6)
#             510 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_voltage_range_reasonable at 0x3af9d7e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 74>:
#  74           0 RESUME                   0
# 
#  75           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('buses')
#              46 BINARY_SUBSCR
#              50 GET_ITER
#              52 LOAD_FAST_AND_CLEAR      1 (b)
#              54 SWAP                     2
#              56 BUILD_LIST               0
#              58 SWAP                     2
#         >>   60 FOR_ITER                23 (to 110)
#              64 STORE_FAST               1 (b)
#              66 LOAD_GLOBAL              5 (NULL + BusData)
#              76 LOAD_ATTR                6 (from_dict)
#              96 LOAD_FAST                1 (b)
#              98 CALL                     1
#             106 LIST_APPEND              2
#             108 JUMP_BACKWARD           25 (to 60)
#         >>  110 END_FOR
#             112 STORE_FAST               2 (buses)
#             114 STORE_FAST               1 (b)
# 
#  76         116 LOAD_FAST                2 (buses)
#             118 GET_ITER
#             120 LOAD_FAST_AND_CLEAR      1 (b)
#             122 SWAP                     2
#             124 BUILD_LIST               0
#             126 SWAP                     2
#         >>  128 FOR_ITER                27 (to 186)
#             132 STORE_FAST               1 (b)
#             134 LOAD_FAST                1 (b)
#             136 LOAD_ATTR                8 (voltage_pu)
#             156 POP_JUMP_IF_NOT_NONE     1 (to 160)
#             158 JUMP_BACKWARD           16 (to 128)
#         >>  160 LOAD_FAST                1 (b)
#             162 LOAD_ATTR                8 (voltage_pu)
#             182 LIST_APPEND              2
#             184 JUMP_BACKWARD           29 (to 128)
#         >>  186 END_FOR
#             188 STORE_FAST               3 (voltages)
#             190 STORE_FAST               1 (b)
# 
#  77         192 LOAD_GLOBAL             11 (NULL + len)
#             202 LOAD_FAST                3 (voltages)
#             204 CALL                     1
#             212 STORE_FAST               4 (@py_assert2)
#             214 LOAD_CONST               2 (14)
#             216 STORE_FAST               5 (@py_assert5)
#             218 LOAD_FAST                4 (@py_assert2)
#             220 LOAD_FAST                5 (@py_assert5)
#             222 COMPARE_OP              40 (==)
#             226 STORE_FAST               6 (@py_assert4)
#             228 LOAD_FAST                6 (@py_assert4)
#             230 POP_JUMP_IF_TRUE       246 (to 724)
#             232 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             242 LOAD_ATTR               14 (_call_reprcompare)
#             262 LOAD_CONST               3 (('==',))
#             264 LOAD_FAST                6 (@py_assert4)
#             266 BUILD_TUPLE              1
#             268 LOAD_CONST               4 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             270 LOAD_FAST                4 (@py_assert2)
#             272 LOAD_FAST                5 (@py_assert5)
#             274 BUILD_TUPLE              2
#             276 CALL                     4
#             284 LOAD_CONST               5 ('len')
#             286 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             296 LOAD_ATTR               18 (locals)
#             316 CALL                     0
#             324 CONTAINS_OP              0
#             326 POP_JUMP_IF_TRUE        25 (to 378)
#             328 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             338 LOAD_ATTR               20 (_should_repr_global_name)
#             358 LOAD_GLOBAL             10 (len)
#             368 CALL                     1
#             376 POP_JUMP_IF_FALSE       25 (to 428)
#         >>  378 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             388 LOAD_ATTR               22 (_saferepr)
#             408 LOAD_GLOBAL             10 (len)
#             418 CALL                     1
#             426 JUMP_FORWARD             1 (to 430)
#         >>  428 LOAD_CONST               5 ('len')
#         >>  430 LOAD_CONST               6 ('voltages')
#             432 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             442 LOAD_ATTR               18 (locals)
#             462 CALL                     0
#             470 CONTAINS_OP              0
#             472 POP_JUMP_IF_TRUE        21 (to 516)
#             474 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             484 LOAD_ATTR               20 (_should_repr_global_name)
#             504 LOAD_FAST                3 (voltages)
#             506 CALL                     1
#             514 POP_JUMP_IF_FALSE       21 (to 558)
#         >>  516 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             526 LOAD_ATTR               22 (_saferepr)
#             546 LOAD_FAST                3 (voltages)
#             548 CALL                     1
#             556 JUMP_FORWARD             1 (to 560)
#         >>  558 LOAD_CONST               6 ('voltages')
#         >>  560 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             570 LOAD_ATTR               22 (_saferepr)
#             590 LOAD_FAST                4 (@py_assert2)
#             592 CALL                     1
#             600 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             610 LOAD_ATTR               22 (_saferepr)
#             630 LOAD_FAST                5 (@py_assert5)
#             632 CALL                     1
#             640 LOAD_CONST               7 (('py0', 'py1', 'py3', 'py6'))
#             642 BUILD_CONST_KEY_MAP      4
#             644 BINARY_OP                6 (%)
#             648 STORE_FAST               7 (@py_format7)
#             650 LOAD_CONST               8 ('assert %(py8)s')
#             652 LOAD_CONST               9 ('py8')
#             654 LOAD_FAST                7 (@py_format7)
#             656 BUILD_MAP                1
#             658 BINARY_OP                6 (%)
#             662 STORE_FAST               8 (@py_format9)
#             664 LOAD_GLOBAL             25 (NULL + AssertionError)
#             674 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             684 LOAD_ATTR               26 (_format_explanation)
#             704 LOAD_FAST                8 (@py_format9)
#             706 CALL                     1
#             714 CALL                     1
#             722 RAISE_VARARGS            1
#         >>  724 LOAD_CONST               0 (None)
#             726 COPY                     1
#             728 STORE_FAST               4 (@py_assert2)
#             730 COPY                     1
#             732 STORE_FAST               6 (@py_assert4)
#             734 STORE_FAST               5 (@py_assert5)
# 
#  78         736 LOAD_CONST              10 (0.9)
#             738 STORE_FAST               9 (@py_assert0)
#             740 LOAD_GLOBAL             29 (NULL + min)
#             750 LOAD_FAST                3 (voltages)
#             752 CALL                     1
#             760 STORE_FAST              10 (@py_assert6)
#             762 LOAD_FAST                9 (@py_assert0)
#             764 LOAD_FAST               10 (@py_assert6)
#             766 COMPARE_OP               2 (<)
#             770 STORE_FAST               4 (@py_assert2)
#             772 LOAD_CONST              11 (1.2)
#             774 STORE_FAST              11 (@py_assert8)
#             776 LOAD_FAST               10 (@py_assert6)
#             778 LOAD_FAST               11 (@py_assert8)
#             780 COMPARE_OP               2 (<)
#             784 STORE_FAST              12 (@py_assert3)
#             786 LOAD_FAST                4 (@py_assert2)
#             788 POP_JUMP_IF_FALSE        3 (to 796)
#             790 LOAD_FAST               12 (@py_assert3)
#             792 EXTENDED_ARG             1
#             794 POP_JUMP_IF_TRUE       268 (to 1332)
#         >>  796 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             806 LOAD_ATTR               14 (_call_reprcompare)
#             826 LOAD_CONST              12 (('<', '<'))
#             828 LOAD_FAST                4 (@py_assert2)
#             830 LOAD_FAST               12 (@py_assert3)
#             832 BUILD_TUPLE              2
#             834 LOAD_CONST              13 (('%(py1)s < %(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n}', '%(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n} < %(py9)s'))
#             836 LOAD_FAST                9 (@py_assert0)
#             838 LOAD_FAST               10 (@py_assert6)
#             840 LOAD_FAST               11 (@py_assert8)
#             842 BUILD_TUPLE              3
#             844 CALL                     4
#             852 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             862 LOAD_ATTR               22 (_saferepr)
#             882 LOAD_FAST                9 (@py_assert0)
#             884 CALL                     1
#             892 LOAD_CONST              14 ('min')
#             894 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             904 LOAD_ATTR               18 (locals)
#             924 CALL                     0
#             932 CONTAINS_OP              0
#             934 POP_JUMP_IF_TRUE        25 (to 986)
#             936 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             946 LOAD_ATTR               20 (_should_repr_global_name)
#             966 LOAD_GLOBAL             28 (min)
#             976 CALL                     1
#             984 POP_JUMP_IF_FALSE       25 (to 1036)
#         >>  986 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             996 LOAD_ATTR               22 (_saferepr)
#            1016 LOAD_GLOBAL             28 (min)
#            1026 CALL                     1
#            1034 JUMP_FORWARD             1 (to 1038)
#         >> 1036 LOAD_CONST              14 ('min')
#         >> 1038 LOAD_CONST               6 ('voltages')
#            1040 LOAD_GLOBAL             17 (NULL + @py_builtins)
#            1050 LOAD_ATTR               18 (locals)
#            1070 CALL                     0
#            1078 CONTAINS_OP              0
#            1080 POP_JUMP_IF_TRUE        21 (to 1124)
#            1082 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1092 LOAD_ATTR               20 (_should_repr_global_name)
#            1112 LOAD_FAST                3 (voltages)
#            1114 CALL                     1
#            1122 POP_JUMP_IF_FALSE       21 (to 1166)
#         >> 1124 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1134 LOAD_ATTR               22 (_saferepr)
#            1154 LOAD_FAST                3 (voltages)
#            1156 CALL                     1
#            1164 JUMP_FORWARD             1 (to 1168)
#         >> 1166 LOAD_CONST               6 ('voltages')
#         >> 1168 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1178 LOAD_ATTR               22 (_saferepr)
#            1198 LOAD_FAST               10 (@py_assert6)
#            1200 CALL                     1
#            1208 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1218 LOAD_ATTR               22 (_saferepr)
#            1238 LOAD_FAST               11 (@py_assert8)
#            1240 CALL                     1
#            1248 LOAD_CONST              15 (('py1', 'py4', 'py5', 'py7', 'py9'))
#            1250 BUILD_CONST_KEY_MAP      5
#            1252 BINARY_OP                6 (%)
#            1256 STORE_FAST              13 (@py_format10)
#            1258 LOAD_CONST              16 ('assert %(py11)s')
#            1260 LOAD_CONST              17 ('py11')
#            1262 LOAD_FAST               13 (@py_format10)
#            1264 BUILD_MAP                1
#            1266 BINARY_OP                6 (%)
#            1270 STORE_FAST              14 (@py_format12)
#            1272 LOAD_GLOBAL             25 (NULL + AssertionError)
#            1282 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1292 LOAD_ATTR               26 (_format_explanation)
#            1312 LOAD_FAST               14 (@py_format12)
#            1314 CALL                     1
#            1322 CALL                     1
#            1330 RAISE_VARARGS            1
#         >> 1332 LOAD_CONST               0 (None)
#            1334 COPY                     1
#            1336 STORE_FAST               9 (@py_assert0)
#            1338 COPY                     1
#            1340 STORE_FAST               4 (@py_assert2)
#            1342 COPY                     1
#            1344 STORE_FAST              12 (@py_assert3)
#            1346 COPY                     1
#            1348 STORE_FAST              10 (@py_assert6)
#            1350 STORE_FAST              11 (@py_assert8)
# 
#  79        1352 LOAD_CONST              10 (0.9)
#            1354 STORE_FAST               9 (@py_assert0)
#            1356 LOAD_GLOBAL             31 (NULL + max)
#            1366 LOAD_FAST                3 (voltages)
#            1368 CALL                     1
#            1376 STORE_FAST              10 (@py_assert6)
#            1378 LOAD_FAST                9 (@py_assert0)
#            1380 LOAD_FAST               10 (@py_assert6)
#            1382 COMPARE_OP               2 (<)
#            1386 STORE_FAST               4 (@py_assert2)
#            1388 LOAD_CONST              11 (1.2)
#            1390 STORE_FAST              11 (@py_assert8)
#            1392 LOAD_FAST               10 (@py_assert6)
#            1394 LOAD_FAST               11 (@py_assert8)
#            1396 COMPARE_OP               2 (<)
#            1400 STORE_FAST              12 (@py_assert3)
#            1402 LOAD_FAST                4 (@py_assert2)
#            1404 POP_JUMP_IF_FALSE        3 (to 1412)
#            1406 LOAD_FAST               12 (@py_assert3)
#            1408 EXTENDED_ARG             1
#            1410 POP_JUMP_IF_TRUE       268 (to 1948)
#         >> 1412 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1422 LOAD_ATTR               14 (_call_reprcompare)
#            1442 LOAD_CONST              12 (('<', '<'))
#            1444 LOAD_FAST                4 (@py_assert2)
#            1446 LOAD_FAST               12 (@py_assert3)
#            1448 BUILD_TUPLE              2
#            1450 LOAD_CONST              13 (('%(py1)s < %(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n}', '%(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n} < %(py9)s'))
#            1452 LOAD_FAST                9 (@py_assert0)
#            1454 LOAD_FAST               10 (@py_assert6)
#            1456 LOAD_FAST               11 (@py_assert8)
#            1458 BUILD_TUPLE              3
#            1460 CALL                     4
#            1468 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1478 LOAD_ATTR               22 (_saferepr)
#            1498 LOAD_FAST                9 (@py_assert0)
#            1500 CALL                     1
#            1508 LOAD_CONST              18 ('max')
#            1510 LOAD_GLOBAL             17 (NULL + @py_builtins)
#            1520 LOAD_ATTR               18 (locals)
#            1540 CALL                     0
#            1548 CONTAINS_OP              0
#            1550 POP_JUMP_IF_TRUE        25 (to 1602)
#            1552 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1562 LOAD_ATTR               20 (_should_repr_global_name)
#            1582 LOAD_GLOBAL             30 (max)
#            1592 CALL                     1
#            1600 POP_JUMP_IF_FALSE       25 (to 1652)
#         >> 1602 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1612 LOAD_ATTR               22 (_saferepr)
#            1632 LOAD_GLOBAL             30 (max)
#            1642 CALL                     1
#            1650 JUMP_FORWARD             1 (to 1654)
#         >> 1652 LOAD_CONST              18 ('max')
#         >> 1654 LOAD_CONST               6 ('voltages')
#            1656 LOAD_GLOBAL             17 (NULL + @py_builtins)
#            1666 LOAD_ATTR               18 (locals)
#            1686 CALL                     0
#            1694 CONTAINS_OP              0
#            1696 POP_JUMP_IF_TRUE        21 (to 1740)
#            1698 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1708 LOAD_ATTR               20 (_should_repr_global_name)
#            1728 LOAD_FAST                3 (voltages)
#            1730 CALL                     1
#            1738 POP_JUMP_IF_FALSE       21 (to 1782)
#         >> 1740 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1750 LOAD_ATTR               22 (_saferepr)
#            1770 LOAD_FAST                3 (voltages)
#            1772 CALL                     1
#            1780 JUMP_FORWARD             1 (to 1784)
#         >> 1782 LOAD_CONST               6 ('voltages')
#         >> 1784 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1794 LOAD_ATTR               22 (_saferepr)
#            1814 LOAD_FAST               10 (@py_assert6)
#            1816 CALL                     1
#            1824 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1834 LOAD_ATTR               22 (_saferepr)
#            1854 LOAD_FAST               11 (@py_assert8)
#            1856 CALL                     1
#            1864 LOAD_CONST              15 (('py1', 'py4', 'py5', 'py7', 'py9'))
#            1866 BUILD_CONST_KEY_MAP      5
#            1868 BINARY_OP                6 (%)
#            1872 STORE_FAST              13 (@py_format10)
#            1874 LOAD_CONST              16 ('assert %(py11)s')
#            1876 LOAD_CONST              17 ('py11')
#            1878 LOAD_FAST               13 (@py_format10)
#            1880 BUILD_MAP                1
#            1882 BINARY_OP                6 (%)
#            1886 STORE_FAST              14 (@py_format12)
#            1888 LOAD_GLOBAL             25 (NULL + AssertionError)
#            1898 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1908 LOAD_ATTR               26 (_format_explanation)
#            1928 LOAD_FAST               14 (@py_format12)
#            1930 CALL                     1
#            1938 CALL                     1
#            1946 RAISE_VARARGS            1
#         >> 1948 LOAD_CONST               0 (None)
#            1950 COPY                     1
#            1952 STORE_FAST               9 (@py_assert0)
#            1954 COPY                     1
#            1956 STORE_FAST               4 (@py_assert2)
#            1958 COPY                     1
#            1960 STORE_FAST              12 (@py_assert3)
#            1962 COPY                     1
#            1964 STORE_FAST              10 (@py_assert6)
#            1966 STORE_FAST              11 (@py_assert8)
#            1968 RETURN_CONST             0 (None)
#         >> 1970 SWAP                     2
#            1972 POP_TOP
# 
#  75        1974 SWAP                     2
#            1976 STORE_FAST               1 (b)
#            1978 RERAISE                  0
#         >> 1980 SWAP                     2
#            1982 POP_TOP
# 
#  76        1984 SWAP                     2
#            1986 STORE_FAST               1 (b)
#            1988 RERAISE                  0
# ExceptionTable:
#   56 to 110 -> 1970 [2]
#   124 to 156 -> 1980 [2]
#   160 to 186 -> 1980 [2]
# 
# Disassembly of <code object test_slack_bus_identified at 0x3af981b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 81>:
#  81           0 RESUME                   0
# 
#  82           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('buses')
#              46 BINARY_SUBSCR
#              50 GET_ITER
#              52 LOAD_FAST_AND_CLEAR      1 (b)
#              54 SWAP                     2
#              56 BUILD_LIST               0
#              58 SWAP                     2
#         >>   60 FOR_ITER                23 (to 110)
#              64 STORE_FAST               1 (b)
#              66 LOAD_GLOBAL              5 (NULL + BusData)
#              76 LOAD_ATTR                6 (from_dict)
#              96 LOAD_FAST                1 (b)
#              98 CALL                     1
#             106 LIST_APPEND              2
#             108 JUMP_BACKWARD           25 (to 60)
#         >>  110 END_FOR
#             112 STORE_FAST               2 (buses)
#             114 STORE_FAST               1 (b)
# 
#  83         116 LOAD_FAST                2 (buses)
#             118 GET_ITER
#             120 LOAD_FAST_AND_CLEAR      1 (b)
#             122 SWAP                     2
#             124 BUILD_LIST               0
#             126 SWAP                     2
#         >>  128 FOR_ITER                34 (to 200)
#             132 STORE_FAST               1 (b)
#             134 LOAD_FAST                1 (b)
#             136 LOAD_ATTR                8 (bus_type)
#             156 LOAD_GLOBAL             10 (BusType)
#             166 LOAD_ATTR               12 (SLACK)
#             186 COMPARE_OP              40 (==)
#             190 POP_JUMP_IF_TRUE         1 (to 194)
#             192 JUMP_BACKWARD           33 (to 128)
#         >>  194 LOAD_FAST                1 (b)
#             196 LIST_APPEND              2
#             198 JUMP_BACKWARD           36 (to 128)
#         >>  200 END_FOR
#             202 STORE_FAST               3 (slack_buses)
#             204 STORE_FAST               1 (b)
# 
#  84         206 LOAD_GLOBAL             15 (NULL + len)
#             216 LOAD_FAST                3 (slack_buses)
#             218 CALL                     1
#             226 STORE_FAST               4 (@py_assert2)
#             228 LOAD_CONST               2 (1)
#             230 STORE_FAST               5 (@py_assert5)
#             232 LOAD_FAST                4 (@py_assert2)
#             234 LOAD_FAST                5 (@py_assert5)
#             236 COMPARE_OP              92 (>=)
#             240 STORE_FAST               6 (@py_assert4)
#             242 LOAD_FAST                6 (@py_assert4)
#             244 POP_JUMP_IF_TRUE       246 (to 738)
#             246 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             256 LOAD_ATTR               18 (_call_reprcompare)
#             276 LOAD_CONST               3 (('>=',))
#             278 LOAD_FAST                6 (@py_assert4)
#             280 BUILD_TUPLE              1
#             282 LOAD_CONST               4 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} >= %(py6)s',))
#             284 LOAD_FAST                4 (@py_assert2)
#             286 LOAD_FAST                5 (@py_assert5)
#             288 BUILD_TUPLE              2
#             290 CALL                     4
#             298 LOAD_CONST               5 ('len')
#             300 LOAD_GLOBAL             21 (NULL + @py_builtins)
#             310 LOAD_ATTR               22 (locals)
#             330 CALL                     0
#             338 CONTAINS_OP              0
#             340 POP_JUMP_IF_TRUE        25 (to 392)
#             342 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             352 LOAD_ATTR               24 (_should_repr_global_name)
#             372 LOAD_GLOBAL             14 (len)
#             382 CALL                     1
#             390 POP_JUMP_IF_FALSE       25 (to 442)
#         >>  392 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             402 LOAD_ATTR               26 (_saferepr)
#             422 LOAD_GLOBAL             14 (len)
#             432 CALL                     1
#             440 JUMP_FORWARD             1 (to 444)
#         >>  442 LOAD_CONST               5 ('len')
#         >>  444 LOAD_CONST               6 ('slack_buses')
#             446 LOAD_GLOBAL             21 (NULL + @py_builtins)
#             456 LOAD_ATTR               22 (locals)
#             476 CALL                     0
#             484 CONTAINS_OP              0
#             486 POP_JUMP_IF_TRUE        21 (to 530)
#             488 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             498 LOAD_ATTR               24 (_should_repr_global_name)
#             518 LOAD_FAST                3 (slack_buses)
#             520 CALL                     1
#             528 POP_JUMP_IF_FALSE       21 (to 572)
#         >>  530 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             540 LOAD_ATTR               26 (_saferepr)
#             560 LOAD_FAST                3 (slack_buses)
#             562 CALL                     1
#             570 JUMP_FORWARD             1 (to 574)
#         >>  572 LOAD_CONST               6 ('slack_buses')
#         >>  574 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             584 LOAD_ATTR               26 (_saferepr)
#             604 LOAD_FAST                4 (@py_assert2)
#             606 CALL                     1
#             614 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             624 LOAD_ATTR               26 (_saferepr)
#             644 LOAD_FAST                5 (@py_assert5)
#             646 CALL                     1
#             654 LOAD_CONST               7 (('py0', 'py1', 'py3', 'py6'))
#             656 BUILD_CONST_KEY_MAP      4
#             658 BINARY_OP                6 (%)
#             662 STORE_FAST               7 (@py_format7)
#             664 LOAD_CONST               8 ('assert %(py8)s')
#             666 LOAD_CONST               9 ('py8')
#             668 LOAD_FAST                7 (@py_format7)
#             670 BUILD_MAP                1
#             672 BINARY_OP                6 (%)
#             676 STORE_FAST               8 (@py_format9)
#             678 LOAD_GLOBAL             29 (NULL + AssertionError)
#             688 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             698 LOAD_ATTR               30 (_format_explanation)
#             718 LOAD_FAST                8 (@py_format9)
#             720 CALL                     1
#             728 CALL                     1
#             736 RAISE_VARARGS            1
#         >>  738 LOAD_CONST               0 (None)
#             740 COPY                     1
#             742 STORE_FAST               4 (@py_assert2)
#             744 COPY                     1
#             746 STORE_FAST               6 (@py_assert4)
#             748 STORE_FAST               5 (@py_assert5)
#             750 RETURN_CONST             0 (None)
#         >>  752 SWAP                     2
#             754 POP_TOP
# 
#  82         756 SWAP                     2
#             758 STORE_FAST               1 (b)
#             760 RERAISE                  0
#         >>  762 SWAP                     2
#             764 POP_TOP
# 
#  83         766 SWAP                     2
#             768 STORE_FAST               1 (b)
#             770 RERAISE                  0
# ExceptionTable:
#   56 to 110 -> 752 [2]
#   124 to 190 -> 762 [2]
#   194 to 200 -> 762 [2]
# 
# Disassembly of <code object test_pv_buses_identified at 0x3af95b80, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 86>:
#  86           0 RESUME                   0
# 
#  87           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('buses')
#              46 BINARY_SUBSCR
#              50 GET_ITER
#              52 LOAD_FAST_AND_CLEAR      1 (b)
#              54 SWAP                     2
#              56 BUILD_LIST               0
#              58 SWAP                     2
#         >>   60 FOR_ITER                23 (to 110)
#              64 STORE_FAST               1 (b)
#              66 LOAD_GLOBAL              5 (NULL + BusData)
#              76 LOAD_ATTR                6 (from_dict)
#              96 LOAD_FAST                1 (b)
#              98 CALL                     1
#             106 LIST_APPEND              2
#             108 JUMP_BACKWARD           25 (to 60)
#         >>  110 END_FOR
#             112 STORE_FAST               2 (buses)
#             114 STORE_FAST               1 (b)
# 
#  88         116 LOAD_FAST                2 (buses)
#             118 GET_ITER
#             120 LOAD_FAST_AND_CLEAR      1 (b)
#             122 SWAP                     2
#             124 BUILD_LIST               0
#             126 SWAP                     2
#         >>  128 FOR_ITER                34 (to 200)
#             132 STORE_FAST               1 (b)
#             134 LOAD_FAST                1 (b)
#             136 LOAD_ATTR                8 (bus_type)
#             156 LOAD_GLOBAL             10 (BusType)
#             166 LOAD_ATTR               12 (PV)
#             186 COMPARE_OP              40 (==)
#             190 POP_JUMP_IF_TRUE         1 (to 194)
#             192 JUMP_BACKWARD           33 (to 128)
#         >>  194 LOAD_FAST                1 (b)
#             196 LIST_APPEND              2
#             198 JUMP_BACKWARD           36 (to 128)
#         >>  200 END_FOR
#             202 STORE_FAST               3 (pv_buses)
#             204 STORE_FAST               1 (b)
# 
#  89         206 LOAD_GLOBAL             15 (NULL + len)
#             216 LOAD_FAST                3 (pv_buses)
#             218 CALL                     1
#             226 STORE_FAST               4 (@py_assert2)
#             228 LOAD_CONST               2 (2)
#             230 STORE_FAST               5 (@py_assert5)
#             232 LOAD_FAST                4 (@py_assert2)
#             234 LOAD_FAST                5 (@py_assert5)
#             236 COMPARE_OP              92 (>=)
#             240 STORE_FAST               6 (@py_assert4)
#             242 LOAD_FAST                6 (@py_assert4)
#             244 POP_JUMP_IF_TRUE       246 (to 738)
#             246 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             256 LOAD_ATTR               18 (_call_reprcompare)
#             276 LOAD_CONST               3 (('>=',))
#             278 LOAD_FAST                6 (@py_assert4)
#             280 BUILD_TUPLE              1
#             282 LOAD_CONST               4 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} >= %(py6)s',))
#             284 LOAD_FAST                4 (@py_assert2)
#             286 LOAD_FAST                5 (@py_assert5)
#             288 BUILD_TUPLE              2
#             290 CALL                     4
#             298 LOAD_CONST               5 ('len')
#             300 LOAD_GLOBAL             21 (NULL + @py_builtins)
#             310 LOAD_ATTR               22 (locals)
#             330 CALL                     0
#             338 CONTAINS_OP              0
#             340 POP_JUMP_IF_TRUE        25 (to 392)
#             342 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             352 LOAD_ATTR               24 (_should_repr_global_name)
#             372 LOAD_GLOBAL             14 (len)
#             382 CALL                     1
#             390 POP_JUMP_IF_FALSE       25 (to 442)
#         >>  392 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             402 LOAD_ATTR               26 (_saferepr)
#             422 LOAD_GLOBAL             14 (len)
#             432 CALL                     1
#             440 JUMP_FORWARD             1 (to 444)
#         >>  442 LOAD_CONST               5 ('len')
#         >>  444 LOAD_CONST               6 ('pv_buses')
#             446 LOAD_GLOBAL             21 (NULL + @py_builtins)
#             456 LOAD_ATTR               22 (locals)
#             476 CALL                     0
#             484 CONTAINS_OP              0
#             486 POP_JUMP_IF_TRUE        21 (to 530)
#             488 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             498 LOAD_ATTR               24 (_should_repr_global_name)
#             518 LOAD_FAST                3 (pv_buses)
#             520 CALL                     1
#             528 POP_JUMP_IF_FALSE       21 (to 572)
#         >>  530 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             540 LOAD_ATTR               26 (_saferepr)
#             560 LOAD_FAST                3 (pv_buses)
#             562 CALL                     1
#             570 JUMP_FORWARD             1 (to 574)
#         >>  572 LOAD_CONST               6 ('pv_buses')
#         >>  574 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             584 LOAD_ATTR               26 (_saferepr)
#             604 LOAD_FAST                4 (@py_assert2)
#             606 CALL                     1
#             614 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             624 LOAD_ATTR               26 (_saferepr)
#             644 LOAD_FAST                5 (@py_assert5)
#             646 CALL                     1
#             654 LOAD_CONST               7 (('py0', 'py1', 'py3', 'py6'))
#             656 BUILD_CONST_KEY_MAP      4
#             658 BINARY_OP                6 (%)
#             662 STORE_FAST               7 (@py_format7)
#             664 LOAD_CONST               8 ('assert %(py8)s')
#             666 LOAD_CONST               9 ('py8')
#             668 LOAD_FAST                7 (@py_format7)
#             670 BUILD_MAP                1
#             672 BINARY_OP                6 (%)
#             676 STORE_FAST               8 (@py_format9)
#             678 LOAD_GLOBAL             29 (NULL + AssertionError)
#             688 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             698 LOAD_ATTR               30 (_format_explanation)
#             718 LOAD_FAST                8 (@py_format9)
#             720 CALL                     1
#             728 CALL                     1
#             736 RAISE_VARARGS            1
#         >>  738 LOAD_CONST               0 (None)
#             740 COPY                     1
#             742 STORE_FAST               4 (@py_assert2)
#             744 COPY                     1
#             746 STORE_FAST               6 (@py_assert4)
#             748 STORE_FAST               5 (@py_assert5)
#             750 RETURN_CONST             0 (None)
#         >>  752 SWAP                     2
#             754 POP_TOP
# 
#  87         756 SWAP                     2
#             758 STORE_FAST               1 (b)
#             760 RERAISE                  0
#         >>  762 SWAP                     2
#             764 POP_TOP
# 
#  88         766 SWAP                     2
#             768 STORE_FAST               1 (b)
#             770 RERAISE                  0
# ExceptionTable:
#   56 to 110 -> 752 [2]
#   124 to 190 -> 762 [2]
#   194 to 200 -> 762 [2]
# 
# Disassembly of <code object test_losses_positive at 0x3aefd020, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 91>:
#  91           0 RESUME                   0
# 
#  92           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('branches')
#              46 BINARY_SUBSCR
#              50 GET_ITER
#              52 LOAD_FAST_AND_CLEAR      1 (br)
#              54 SWAP                     2
#              56 BUILD_LIST               0
#              58 SWAP                     2
#         >>   60 FOR_ITER                23 (to 110)
#              64 STORE_FAST               1 (br)
#              66 LOAD_GLOBAL              5 (NULL + BranchData)
#              76 LOAD_ATTR                6 (from_dict)
#              96 LOAD_FAST                1 (br)
#              98 CALL                     1
#             106 LIST_APPEND              2
#             108 JUMP_BACKWARD           25 (to 60)
#         >>  110 END_FOR
#             112 STORE_FAST               2 (branches)
#             114 STORE_FAST               1 (br)
# 
#  93         116 LOAD_GLOBAL              9 (NULL + sum)
#             126 LOAD_CONST               2 (<code object <genexpr> at 0x73cd93b31330, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 93>)
#             128 MAKE_FUNCTION            0
#             130 LOAD_FAST                2 (branches)
#             132 GET_ITER
#             134 CALL                     0
#             142 CALL                     1
#             150 STORE_FAST               3 (total_loss)
# 
#  94         152 LOAD_CONST               3 (0)
#             154 STORE_FAST               4 (@py_assert2)
#             156 LOAD_FAST                3 (total_loss)
#             158 LOAD_FAST                4 (@py_assert2)
#             160 COMPARE_OP              68 (>)
#             164 STORE_FAST               5 (@py_assert1)
#             166 LOAD_FAST                5 (@py_assert1)
#             168 POP_JUMP_IF_TRUE       153 (to 476)
#             170 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             180 LOAD_ATTR               12 (_call_reprcompare)
#             200 LOAD_CONST               4 (('>',))
#             202 LOAD_FAST                5 (@py_assert1)
#             204 BUILD_TUPLE              1
#             206 LOAD_CONST               5 (('%(py0)s > %(py3)s',))
#             208 LOAD_FAST                3 (total_loss)
#             210 LOAD_FAST                4 (@py_assert2)
#             212 BUILD_TUPLE              2
#             214 CALL                     4
#             222 LOAD_CONST               6 ('total_loss')
#             224 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             234 LOAD_ATTR               16 (locals)
#             254 CALL                     0
#             262 CONTAINS_OP              0
#             264 POP_JUMP_IF_TRUE        21 (to 308)
#             266 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             276 LOAD_ATTR               18 (_should_repr_global_name)
#             296 LOAD_FAST                3 (total_loss)
#             298 CALL                     1
#             306 POP_JUMP_IF_FALSE       21 (to 350)
#         >>  308 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             318 LOAD_ATTR               20 (_saferepr)
#             338 LOAD_FAST                3 (total_loss)
#             340 CALL                     1
#             348 JUMP_FORWARD             1 (to 352)
#         >>  350 LOAD_CONST               6 ('total_loss')
#         >>  352 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             362 LOAD_ATTR               20 (_saferepr)
#             382 LOAD_FAST                4 (@py_assert2)
#             384 CALL                     1
#             392 LOAD_CONST               7 (('py0', 'py3'))
#             394 BUILD_CONST_KEY_MAP      2
#             396 BINARY_OP                6 (%)
#             400 STORE_FAST               6 (@py_format4)
#             402 LOAD_CONST               8 ('assert %(py5)s')
#             404 LOAD_CONST               9 ('py5')
#             406 LOAD_FAST                6 (@py_format4)
#             408 BUILD_MAP                1
#             410 BINARY_OP                6 (%)
#             414 STORE_FAST               7 (@py_format6)
#             416 LOAD_GLOBAL             23 (NULL + AssertionError)
#             426 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             436 LOAD_ATTR               24 (_format_explanation)
#             456 LOAD_FAST                7 (@py_format6)
#             458 CALL                     1
#             466 CALL                     1
#             474 RAISE_VARARGS            1
#         >>  476 LOAD_CONST               0 (None)
#             478 COPY                     1
#             480 STORE_FAST               5 (@py_assert1)
#             482 STORE_FAST               4 (@py_assert2)
#             484 RETURN_CONST             0 (None)
#         >>  486 SWAP                     2
#             488 POP_TOP
# 
#  92         490 SWAP                     2
#             492 STORE_FAST               1 (br)
#             494 RERAISE                  0
# ExceptionTable:
#   56 to 110 -> 486 [2]
# 
# Disassembly of <code object <genexpr> at 0x73cd93b31330, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 93>:
#  93           0 RETURN_GENERATOR
#               2 POP_TOP
#               4 RESUME                   0
#               6 LOAD_FAST                0 (.0)
#         >>    8 FOR_ITER                20 (to 52)
#              12 STORE_FAST               1 (br)
#              14 LOAD_FAST                1 (br)
#              16 LOAD_ATTR                0 (power_loss_mw)
#              36 COPY                     1
#              38 POP_JUMP_IF_TRUE         2 (to 44)
#              40 POP_TOP
#              42 LOAD_CONST               0 (0)
#         >>   44 YIELD_VALUE              1
#              46 RESUME                   1
#              48 POP_TOP
#              50 JUMP_BACKWARD           22 (to 8)
#         >>   52 END_FOR
#              54 RETURN_CONST             1 (None)
#         >>   56 CALL_INTRINSIC_1         3 (INTRINSIC_STOPITERATION_ERROR)
#              58 RERAISE                  1
# ExceptionTable:
#   4 to 54 -> 56 [0] lasti
# 
# Disassembly of <code object test_total_loss_matches_summary at 0x3af9bd40, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 96>:
#  96           0 RESUME                   0
# 
#  97           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('branches')
#              46 BINARY_SUBSCR
#              50 GET_ITER
#              52 LOAD_FAST_AND_CLEAR      1 (br)
#              54 SWAP                     2
#              56 BUILD_LIST               0
#              58 SWAP                     2
#         >>   60 FOR_ITER                23 (to 110)
#              64 STORE_FAST               1 (br)
#              66 LOAD_GLOBAL              5 (NULL + BranchData)
#              76 LOAD_ATTR                6 (from_dict)
#              96 LOAD_FAST                1 (br)
#              98 CALL                     1
#             106 LIST_APPEND              2
#             108 JUMP_BACKWARD           25 (to 60)
#         >>  110 END_FOR
#             112 STORE_FAST               2 (branches)
#             114 STORE_FAST               1 (br)
# 
#  98         116 LOAD_GLOBAL              9 (NULL + sum)
#             126 LOAD_CONST               2 (<code object <genexpr> at 0x73cd93b31630, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 98>)
#             128 MAKE_FUNCTION            0
#             130 LOAD_FAST                2 (branches)
#             132 GET_ITER
#             134 CALL                     0
#             142 CALL                     1
#             150 STORE_FAST               3 (loss_from_branches)
# 
#  99         152 LOAD_FAST                0 (self)
#             154 LOAD_ATTR                0 (result)
#             174 LOAD_ATTR                2 (data)
#             194 LOAD_CONST               3 ('summary')
#             196 BINARY_SUBSCR
#             200 LOAD_CONST               4 ('total_loss_mw')
#             202 BINARY_SUBSCR
#             206 STORE_FAST               4 (loss_from_summary)
# 
# 100         208 LOAD_FAST                3 (loss_from_branches)
#             210 LOAD_FAST                4 (loss_from_summary)
#             212 BINARY_OP               10 (-)
#             216 STORE_FAST               5 (@py_assert3)
#             218 LOAD_GLOBAL             11 (NULL + abs)
#             228 LOAD_FAST                5 (@py_assert3)
#             230 CALL                     1
#             238 STORE_FAST               6 (@py_assert4)
#             240 LOAD_CONST               5 (0.01)
#             242 STORE_FAST               7 (@py_assert7)
#             244 LOAD_FAST                6 (@py_assert4)
#             246 LOAD_FAST                7 (@py_assert7)
#             248 COMPARE_OP               2 (<)
#             252 STORE_FAST               8 (@py_assert6)
#             254 LOAD_FAST                8 (@py_assert6)
#             256 EXTENDED_ARG             1
#             258 POP_JUMP_IF_TRUE       311 (to 882)
#             260 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             270 LOAD_ATTR               14 (_call_reprcompare)
#             290 LOAD_CONST               6 (('<',))
#             292 LOAD_FAST                8 (@py_assert6)
#             294 BUILD_TUPLE              1
#             296 LOAD_CONST               7 (('%(py5)s\n{%(py5)s = %(py0)s((%(py1)s - %(py2)s))\n} < %(py8)s',))
#             298 LOAD_FAST                6 (@py_assert4)
#             300 LOAD_FAST                7 (@py_assert7)
#             302 BUILD_TUPLE              2
#             304 CALL                     4
#             312 LOAD_CONST               8 ('abs')
#             314 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             324 LOAD_ATTR               18 (locals)
#             344 CALL                     0
#             352 CONTAINS_OP              0
#             354 POP_JUMP_IF_TRUE        25 (to 406)
#             356 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             366 LOAD_ATTR               20 (_should_repr_global_name)
#             386 LOAD_GLOBAL             10 (abs)
#             396 CALL                     1
#             404 POP_JUMP_IF_FALSE       25 (to 456)
#         >>  406 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             416 LOAD_ATTR               22 (_saferepr)
#             436 LOAD_GLOBAL             10 (abs)
#             446 CALL                     1
#             454 JUMP_FORWARD             1 (to 458)
#         >>  456 LOAD_CONST               8 ('abs')
#         >>  458 LOAD_CONST               9 ('loss_from_branches')
#             460 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             470 LOAD_ATTR               18 (locals)
#             490 CALL                     0
#             498 CONTAINS_OP              0
#             500 POP_JUMP_IF_TRUE        21 (to 544)
#             502 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             512 LOAD_ATTR               20 (_should_repr_global_name)
#             532 LOAD_FAST                3 (loss_from_branches)
#             534 CALL                     1
#             542 POP_JUMP_IF_FALSE       21 (to 586)
#         >>  544 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             554 LOAD_ATTR               22 (_saferepr)
#             574 LOAD_FAST                3 (loss_from_branches)
#             576 CALL                     1
#             584 JUMP_FORWARD             1 (to 588)
#         >>  586 LOAD_CONST               9 ('loss_from_branches')
#         >>  588 LOAD_CONST              10 ('loss_from_summary')
#             590 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             600 LOAD_ATTR               18 (locals)
#             620 CALL                     0
#             628 CONTAINS_OP              0
#             630 POP_JUMP_IF_TRUE        21 (to 674)
#             632 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             642 LOAD_ATTR               20 (_should_repr_global_name)
#             662 LOAD_FAST                4 (loss_from_summary)
#             664 CALL                     1
#             672 POP_JUMP_IF_FALSE       21 (to 716)
#         >>  674 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             684 LOAD_ATTR               22 (_saferepr)
#             704 LOAD_FAST                4 (loss_from_summary)
#             706 CALL                     1
#             714 JUMP_FORWARD             1 (to 718)
#         >>  716 LOAD_CONST              10 ('loss_from_summary')
#         >>  718 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             728 LOAD_ATTR               22 (_saferepr)
#             748 LOAD_FAST                6 (@py_assert4)
#             750 CALL                     1
#             758 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             768 LOAD_ATTR               22 (_saferepr)
#             788 LOAD_FAST                7 (@py_assert7)
#             790 CALL                     1
#             798 LOAD_CONST              11 (('py0', 'py1', 'py2', 'py5', 'py8'))
#             800 BUILD_CONST_KEY_MAP      5
#             802 BINARY_OP                6 (%)
#             806 STORE_FAST               9 (@py_format9)
#             808 LOAD_CONST              12 ('assert %(py10)s')
#             810 LOAD_CONST              13 ('py10')
#             812 LOAD_FAST                9 (@py_format9)
#             814 BUILD_MAP                1
#             816 BINARY_OP                6 (%)
#             820 STORE_FAST              10 (@py_format11)
#             822 LOAD_GLOBAL             25 (NULL + AssertionError)
#             832 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             842 LOAD_ATTR               26 (_format_explanation)
#             862 LOAD_FAST               10 (@py_format11)
#             864 CALL                     1
#             872 CALL                     1
#             880 RAISE_VARARGS            1
#         >>  882 LOAD_CONST               0 (None)
#             884 COPY                     1
#             886 STORE_FAST               5 (@py_assert3)
#             888 COPY                     1
#             890 STORE_FAST               6 (@py_assert4)
#             892 COPY                     1
#             894 STORE_FAST               8 (@py_assert6)
#             896 STORE_FAST               7 (@py_assert7)
#             898 RETURN_CONST             0 (None)
#         >>  900 SWAP                     2
#             902 POP_TOP
# 
#  97         904 SWAP                     2
#             906 STORE_FAST               1 (br)
#             908 RERAISE                  0
# ExceptionTable:
#   56 to 110 -> 900 [2]
# 
# Disassembly of <code object <genexpr> at 0x73cd93b31630, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 98>:
#  98           0 RETURN_GENERATOR
#               2 POP_TOP
#               4 RESUME                   0
#               6 LOAD_FAST                0 (.0)
#         >>    8 FOR_ITER                20 (to 52)
#              12 STORE_FAST               1 (br)
#              14 LOAD_FAST                1 (br)
#              16 LOAD_ATTR                0 (power_loss_mw)
#              36 COPY                     1
#              38 POP_JUMP_IF_TRUE         2 (to 44)
#              40 POP_TOP
#              42 LOAD_CONST               0 (0)
#         >>   44 YIELD_VALUE              1
#              46 RESUME                   1
#              48 POP_TOP
#              50 JUMP_BACKWARD           22 (to 8)
#         >>   52 END_FOR
#              54 RETURN_CONST             1 (None)
#         >>   56 CALL_INTRINSIC_1         3 (INTRINSIC_STOPITERATION_ERROR)
#              58 RERAISE                  1
# ExceptionTable:
#   4 to 54 -> 56 [0] lasti
# 
# Disassembly of <code object test_generation_exceeds_load at 0x73cd948baa30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 102>:
# 102           0 RESUME                   0
# 
# 103           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('summary')
#              46 BINARY_SUBSCR
#              50 STORE_FAST               1 (summary)
# 
# 104          52 LOAD_FAST                1 (summary)
#              54 LOAD_CONST               2 ('total_generation_mw')
#              56 BINARY_SUBSCR
#              60 STORE_FAST               2 (@py_assert0)
#              62 LOAD_FAST                1 (summary)
#              64 LOAD_CONST               3 ('total_load_mw')
#              66 BINARY_SUBSCR
#              70 STORE_FAST               3 (@py_assert3)
#              72 LOAD_FAST                2 (@py_assert0)
#              74 LOAD_FAST                3 (@py_assert3)
#              76 COMPARE_OP              68 (>)
#              80 STORE_FAST               4 (@py_assert2)
#              82 LOAD_FAST                4 (@py_assert2)
#              84 POP_JUMP_IF_TRUE       108 (to 302)
#              86 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              96 LOAD_ATTR                6 (_call_reprcompare)
#             116 LOAD_CONST               4 (('>',))
#             118 LOAD_FAST                4 (@py_assert2)
#             120 BUILD_TUPLE              1
#             122 LOAD_CONST               5 (('%(py1)s > %(py4)s',))
#             124 LOAD_FAST                2 (@py_assert0)
#             126 LOAD_FAST                3 (@py_assert3)
#             128 BUILD_TUPLE              2
#             130 CALL                     4
#             138 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             148 LOAD_ATTR                8 (_saferepr)
#             168 LOAD_FAST                2 (@py_assert0)
#             170 CALL                     1
#             178 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             188 LOAD_ATTR                8 (_saferepr)
#             208 LOAD_FAST                3 (@py_assert3)
#             210 CALL                     1
#             218 LOAD_CONST               6 (('py1', 'py4'))
#             220 BUILD_CONST_KEY_MAP      2
#             222 BINARY_OP                6 (%)
#             226 STORE_FAST               5 (@py_format5)
#             228 LOAD_CONST               7 ('assert %(py6)s')
#             230 LOAD_CONST               8 ('py6')
#             232 LOAD_FAST                5 (@py_format5)
#             234 BUILD_MAP                1
#             236 BINARY_OP                6 (%)
#             240 STORE_FAST               6 (@py_format7)
#             242 LOAD_GLOBAL             11 (NULL + AssertionError)
#             252 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             262 LOAD_ATTR               12 (_format_explanation)
#             282 LOAD_FAST                6 (@py_format7)
#             284 CALL                     1
#             292 CALL                     1
#             300 RAISE_VARARGS            1
#         >>  302 LOAD_CONST               0 (None)
#             304 COPY                     1
#             306 STORE_FAST               2 (@py_assert0)
#             308 COPY                     1
#             310 STORE_FAST               4 (@py_assert2)
#             312 STORE_FAST               3 (@py_assert3)
#             314 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_generator_count at 0x3aef4bd0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 106>:
# 106           0 RESUME                   0
# 
# 107           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('generators')
#              46 BINARY_SUBSCR
#              50 STORE_FAST               1 (@py_assert1)
#              52 LOAD_GLOBAL              5 (NULL + len)
#              62 LOAD_FAST                1 (@py_assert1)
#              64 CALL                     1
#              72 STORE_FAST               2 (@py_assert3)
#              74 LOAD_CONST               2 (1)
#              76 STORE_FAST               3 (@py_assert6)
#              78 LOAD_FAST                2 (@py_assert3)
#              80 LOAD_FAST                3 (@py_assert6)
#              82 COMPARE_OP              92 (>=)
#              86 STORE_FAST               4 (@py_assert5)
#              88 LOAD_FAST                4 (@py_assert5)
#              90 POP_JUMP_IF_TRUE       201 (to 494)
#              92 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             102 LOAD_ATTR                8 (_call_reprcompare)
#             122 LOAD_CONST               3 (('>=',))
#             124 LOAD_FAST                4 (@py_assert5)
#             126 BUILD_TUPLE              1
#             128 LOAD_CONST               4 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} >= %(py7)s',))
#             130 LOAD_FAST                2 (@py_assert3)
#             132 LOAD_FAST                3 (@py_assert6)
#             134 BUILD_TUPLE              2
#             136 CALL                     4
#             144 LOAD_CONST               5 ('len')
#             146 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             156 LOAD_ATTR               12 (locals)
#             176 CALL                     0
#             184 CONTAINS_OP              0
#             186 POP_JUMP_IF_TRUE        25 (to 238)
#             188 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             198 LOAD_ATTR               14 (_should_repr_global_name)
#             218 LOAD_GLOBAL              4 (len)
#             228 CALL                     1
#             236 POP_JUMP_IF_FALSE       25 (to 288)
#         >>  238 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             248 LOAD_ATTR               16 (_saferepr)
#             268 LOAD_GLOBAL              4 (len)
#             278 CALL                     1
#             286 JUMP_FORWARD             1 (to 290)
#         >>  288 LOAD_CONST               5 ('len')
#         >>  290 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             300 LOAD_ATTR               16 (_saferepr)
#             320 LOAD_FAST                1 (@py_assert1)
#             322 CALL                     1
#             330 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             340 LOAD_ATTR               16 (_saferepr)
#             360 LOAD_FAST                2 (@py_assert3)
#             362 CALL                     1
#             370 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             380 LOAD_ATTR               16 (_saferepr)
#             400 LOAD_FAST                3 (@py_assert6)
#             402 CALL                     1
#             410 LOAD_CONST               6 (('py0', 'py2', 'py4', 'py7'))
#             412 BUILD_CONST_KEY_MAP      4
#             414 BINARY_OP                6 (%)
#             418 STORE_FAST               5 (@py_format8)
#             420 LOAD_CONST               7 ('assert %(py9)s')
#             422 LOAD_CONST               8 ('py9')
#             424 LOAD_FAST                5 (@py_format8)
#             426 BUILD_MAP                1
#             428 BINARY_OP                6 (%)
#             432 STORE_FAST               6 (@py_format10)
#             434 LOAD_GLOBAL             19 (NULL + AssertionError)
#             444 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             454 LOAD_ATTR               20 (_format_explanation)
#             474 LOAD_FAST                6 (@py_format10)
#             476 CALL                     1
#             484 CALL                     1
#             492 RAISE_VARARGS            1
#         >>  494 LOAD_CONST               0 (None)
#             496 COPY                     1
#             498 STORE_FAST               1 (@py_assert1)
#             500 COPY                     1
#             502 STORE_FAST               2 (@py_assert3)
#             504 COPY                     1
#             506 STORE_FAST               4 (@py_assert5)
#             508 STORE_FAST               3 (@py_assert6)
#             510 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_bus_data_roundtrip at 0x3af9f460, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 109>:
# 109           0 RESUME                   0
# 
# 110           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('buses')
#              46 BINARY_SUBSCR
#              50 LOAD_CONST               2 (0)
#              52 BINARY_SUBSCR
#              56 STORE_FAST               1 (raw)
# 
# 111          58 LOAD_GLOBAL              5 (NULL + BusData)
#              68 LOAD_ATTR                6 (from_dict)
#              88 LOAD_FAST                1 (raw)
#              90 CALL                     1
#              98 STORE_FAST               2 (bus)
# 
# 112         100 LOAD_FAST                2 (bus)
#             102 LOAD_ATTR                8 (name)
#             122 STORE_FAST               3 (@py_assert1)
#             124 LOAD_FAST                3 (@py_assert1)
#             126 POP_JUMP_IF_TRUE       121 (to 370)
#             128 LOAD_CONST               3 ('assert %(py2)s\n{%(py2)s = %(py0)s.name\n}')
#             130 LOAD_CONST               4 ('bus')
#             132 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             142 LOAD_ATTR               12 (locals)
#             162 CALL                     0
#             170 CONTAINS_OP              0
#             172 POP_JUMP_IF_TRUE        21 (to 216)
#             174 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             184 LOAD_ATTR               16 (_should_repr_global_name)
#             204 LOAD_FAST                2 (bus)
#             206 CALL                     1
#             214 POP_JUMP_IF_FALSE       21 (to 258)
#         >>  216 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             226 LOAD_ATTR               18 (_saferepr)
#             246 LOAD_FAST                2 (bus)
#             248 CALL                     1
#             256 JUMP_FORWARD             1 (to 260)
#         >>  258 LOAD_CONST               4 ('bus')
#         >>  260 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             270 LOAD_ATTR               18 (_saferepr)
#             290 LOAD_FAST                3 (@py_assert1)
#             292 CALL                     1
#             300 LOAD_CONST               5 (('py0', 'py2'))
#             302 BUILD_CONST_KEY_MAP      2
#             304 BINARY_OP                6 (%)
#             308 STORE_FAST               4 (@py_format3)
#             310 LOAD_GLOBAL             21 (NULL + AssertionError)
#             320 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             330 LOAD_ATTR               22 (_format_explanation)
#             350 LOAD_FAST                4 (@py_format3)
#             352 CALL                     1
#             360 CALL                     1
#             368 RAISE_VARARGS            1
#         >>  370 LOAD_CONST               0 (None)
#             372 STORE_FAST               3 (@py_assert1)
# 
# 113         374 LOAD_FAST                2 (bus)
#             376 LOAD_ATTR               24 (voltage_kv)
#             396 STORE_FAST               3 (@py_assert1)
#             398 LOAD_CONST               2 (0)
#             400 STORE_FAST               5 (@py_assert4)
#             402 LOAD_FAST                3 (@py_assert1)
#             404 LOAD_FAST                5 (@py_assert4)
#             406 COMPARE_OP              68 (>)
#             410 STORE_FAST               6 (@py_assert3)
#             412 LOAD_FAST                6 (@py_assert3)
#             414 POP_JUMP_IF_TRUE       173 (to 762)
#             416 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             426 LOAD_ATTR               26 (_call_reprcompare)
#             446 LOAD_CONST               6 (('>',))
#             448 LOAD_FAST                6 (@py_assert3)
#             450 BUILD_TUPLE              1
#             452 LOAD_CONST               7 (('%(py2)s\n{%(py2)s = %(py0)s.voltage_kv\n} > %(py5)s',))
#             454 LOAD_FAST                3 (@py_assert1)
#             456 LOAD_FAST                5 (@py_assert4)
#             458 BUILD_TUPLE              2
#             460 CALL                     4
#             468 LOAD_CONST               4 ('bus')
#             470 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             480 LOAD_ATTR               12 (locals)
#             500 CALL                     0
#             508 CONTAINS_OP              0
#             510 POP_JUMP_IF_TRUE        21 (to 554)
#             512 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             522 LOAD_ATTR               16 (_should_repr_global_name)
#             542 LOAD_FAST                2 (bus)
#             544 CALL                     1
#             552 POP_JUMP_IF_FALSE       21 (to 596)
#         >>  554 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             564 LOAD_ATTR               18 (_saferepr)
#             584 LOAD_FAST                2 (bus)
#             586 CALL                     1
#             594 JUMP_FORWARD             1 (to 598)
#         >>  596 LOAD_CONST               4 ('bus')
#         >>  598 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             608 LOAD_ATTR               18 (_saferepr)
#             628 LOAD_FAST                3 (@py_assert1)
#             630 CALL                     1
#             638 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             648 LOAD_ATTR               18 (_saferepr)
#             668 LOAD_FAST                5 (@py_assert4)
#             670 CALL                     1
#             678 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#             680 BUILD_CONST_KEY_MAP      3
#             682 BINARY_OP                6 (%)
#             686 STORE_FAST               7 (@py_format6)
#             688 LOAD_CONST               9 ('assert %(py7)s')
#             690 LOAD_CONST              10 ('py7')
#             692 LOAD_FAST                7 (@py_format6)
#             694 BUILD_MAP                1
#             696 BINARY_OP                6 (%)
#             700 STORE_FAST               8 (@py_format8)
#             702 LOAD_GLOBAL             21 (NULL + AssertionError)
#             712 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             722 LOAD_ATTR               22 (_format_explanation)
#             742 LOAD_FAST                8 (@py_format8)
#             744 CALL                     1
#             752 CALL                     1
#             760 RAISE_VARARGS            1
#         >>  762 LOAD_CONST               0 (None)
#             764 COPY                     1
#             766 STORE_FAST               3 (@py_assert1)
#             768 COPY                     1
#             770 STORE_FAST               6 (@py_assert3)
#             772 STORE_FAST               5 (@py_assert4)
# 
# 114         774 LOAD_FAST                2 (bus)
#             776 LOAD_ATTR               28 (voltage_pu)
#             796 STORE_FAST               3 (@py_assert1)
#             798 LOAD_CONST               0 (None)
#             800 STORE_FAST               5 (@py_assert4)
#             802 LOAD_FAST                3 (@py_assert1)
#             804 LOAD_FAST                5 (@py_assert4)
#             806 IS_OP                    1
#             808 STORE_FAST               6 (@py_assert3)
#             810 LOAD_FAST                6 (@py_assert3)
#             812 POP_JUMP_IF_TRUE       173 (to 1160)
#             814 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             824 LOAD_ATTR               26 (_call_reprcompare)
#             844 LOAD_CONST              11 (('is not',))
#             846 LOAD_FAST                6 (@py_assert3)
#             848 BUILD_TUPLE              1
#             850 LOAD_CONST              12 (('%(py2)s\n{%(py2)s = %(py0)s.voltage_pu\n} is not %(py5)s',))
#             852 LOAD_FAST                3 (@py_assert1)
#             854 LOAD_FAST                5 (@py_assert4)
#             856 BUILD_TUPLE              2
#             858 CALL                     4
#             866 LOAD_CONST               4 ('bus')
#             868 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             878 LOAD_ATTR               12 (locals)
#             898 CALL                     0
#             906 CONTAINS_OP              0
#             908 POP_JUMP_IF_TRUE        21 (to 952)
#             910 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             920 LOAD_ATTR               16 (_should_repr_global_name)
#             940 LOAD_FAST                2 (bus)
#             942 CALL                     1
#             950 POP_JUMP_IF_FALSE       21 (to 994)
#         >>  952 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             962 LOAD_ATTR               18 (_saferepr)
#             982 LOAD_FAST                2 (bus)
#             984 CALL                     1
#             992 JUMP_FORWARD             1 (to 996)
#         >>  994 LOAD_CONST               4 ('bus')
#         >>  996 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1006 LOAD_ATTR               18 (_saferepr)
#            1026 LOAD_FAST                3 (@py_assert1)
#            1028 CALL                     1
#            1036 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1046 LOAD_ATTR               18 (_saferepr)
#            1066 LOAD_FAST                5 (@py_assert4)
#            1068 CALL                     1
#            1076 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#            1078 BUILD_CONST_KEY_MAP      3
#            1080 BINARY_OP                6 (%)
#            1084 STORE_FAST               7 (@py_format6)
#            1086 LOAD_CONST               9 ('assert %(py7)s')
#            1088 LOAD_CONST              10 ('py7')
#            1090 LOAD_FAST                7 (@py_format6)
#            1092 BUILD_MAP                1
#            1094 BINARY_OP                6 (%)
#            1098 STORE_FAST               8 (@py_format8)
#            1100 LOAD_GLOBAL             21 (NULL + AssertionError)
#            1110 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1120 LOAD_ATTR               22 (_format_explanation)
#            1140 LOAD_FAST                8 (@py_format8)
#            1142 CALL                     1
#            1150 CALL                     1
#            1158 RAISE_VARARGS            1
#         >> 1160 LOAD_CONST               0 (None)
#            1162 COPY                     1
#            1164 STORE_FAST               3 (@py_assert1)
#            1166 COPY                     1
#            1168 STORE_FAST               6 (@py_assert3)
#            1170 STORE_FAST               5 (@py_assert4)
# 
# 115        1172 LOAD_FAST                2 (bus)
#            1174 LOAD_ATTR               28 (voltage_pu)
#            1194 STORE_FAST               3 (@py_assert1)
#            1196 LOAD_CONST               2 (0)
#            1198 STORE_FAST               5 (@py_assert4)
#            1200 LOAD_FAST                3 (@py_assert1)
#            1202 LOAD_FAST                5 (@py_assert4)
#            1204 COMPARE_OP              68 (>)
#            1208 STORE_FAST               6 (@py_assert3)
#            1210 LOAD_FAST                6 (@py_assert3)
#            1212 POP_JUMP_IF_TRUE       173 (to 1560)
#            1214 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1224 LOAD_ATTR               26 (_call_reprcompare)
#            1244 LOAD_CONST               6 (('>',))
#            1246 LOAD_FAST                6 (@py_assert3)
#            1248 BUILD_TUPLE              1
#            1250 LOAD_CONST              13 (('%(py2)s\n{%(py2)s = %(py0)s.voltage_pu\n} > %(py5)s',))
#            1252 LOAD_FAST                3 (@py_assert1)
#            1254 LOAD_FAST                5 (@py_assert4)
#            1256 BUILD_TUPLE              2
#            1258 CALL                     4
#            1266 LOAD_CONST               4 ('bus')
#            1268 LOAD_GLOBAL             11 (NULL + @py_builtins)
#            1278 LOAD_ATTR               12 (locals)
#            1298 CALL                     0
#            1306 CONTAINS_OP              0
#            1308 POP_JUMP_IF_TRUE        21 (to 1352)
#            1310 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1320 LOAD_ATTR               16 (_should_repr_global_name)
#            1340 LOAD_FAST                2 (bus)
#            1342 CALL                     1
#            1350 POP_JUMP_IF_FALSE       21 (to 1394)
#         >> 1352 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1362 LOAD_ATTR               18 (_saferepr)
#            1382 LOAD_FAST                2 (bus)
#            1384 CALL                     1
#            1392 JUMP_FORWARD             1 (to 1396)
#         >> 1394 LOAD_CONST               4 ('bus')
#         >> 1396 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1406 LOAD_ATTR               18 (_saferepr)
#            1426 LOAD_FAST                3 (@py_assert1)
#            1428 CALL                     1
#            1436 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1446 LOAD_ATTR               18 (_saferepr)
#            1466 LOAD_FAST                5 (@py_assert4)
#            1468 CALL                     1
#            1476 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#            1478 BUILD_CONST_KEY_MAP      3
#            1480 BINARY_OP                6 (%)
#            1484 STORE_FAST               7 (@py_format6)
#            1486 LOAD_CONST               9 ('assert %(py7)s')
#            1488 LOAD_CONST              10 ('py7')
#            1490 LOAD_FAST                7 (@py_format6)
#            1492 BUILD_MAP                1
#            1494 BINARY_OP                6 (%)
#            1498 STORE_FAST               8 (@py_format8)
#            1500 LOAD_GLOBAL             21 (NULL + AssertionError)
#            1510 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1520 LOAD_ATTR               22 (_format_explanation)
#            1540 LOAD_FAST                8 (@py_format8)
#            1542 CALL                     1
#            1550 CALL                     1
#            1558 RAISE_VARARGS            1
#         >> 1560 LOAD_CONST               0 (None)
#            1562 COPY                     1
#            1564 STORE_FAST               3 (@py_assert1)
#            1566 COPY                     1
#            1568 STORE_FAST               6 (@py_assert3)
#            1570 STORE_FAST               5 (@py_assert4)
#            1572 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_branch_data_roundtrip at 0x3af9fb50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 117>:
# 117           0 RESUME                   0
# 
# 118           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('branches')
#              46 BINARY_SUBSCR
#              50 LOAD_CONST               2 (0)
#              52 BINARY_SUBSCR
#              56 STORE_FAST               1 (raw)
# 
# 119          58 LOAD_GLOBAL              5 (NULL + BranchData)
#              68 LOAD_ATTR                6 (from_dict)
#              88 LOAD_FAST                1 (raw)
#              90 CALL                     1
#              98 STORE_FAST               2 (branch)
# 
# 120         100 LOAD_FAST                2 (branch)
#             102 LOAD_ATTR                8 (name)
#             122 STORE_FAST               3 (@py_assert1)
#             124 LOAD_FAST                3 (@py_assert1)
#             126 POP_JUMP_IF_TRUE       121 (to 370)
#             128 LOAD_CONST               3 ('assert %(py2)s\n{%(py2)s = %(py0)s.name\n}')
#             130 LOAD_CONST               4 ('branch')
#             132 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             142 LOAD_ATTR               12 (locals)
#             162 CALL                     0
#             170 CONTAINS_OP              0
#             172 POP_JUMP_IF_TRUE        21 (to 216)
#             174 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             184 LOAD_ATTR               16 (_should_repr_global_name)
#             204 LOAD_FAST                2 (branch)
#             206 CALL                     1
#             214 POP_JUMP_IF_FALSE       21 (to 258)
#         >>  216 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             226 LOAD_ATTR               18 (_saferepr)
#             246 LOAD_FAST                2 (branch)
#             248 CALL                     1
#             256 JUMP_FORWARD             1 (to 260)
#         >>  258 LOAD_CONST               4 ('branch')
#         >>  260 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             270 LOAD_ATTR               18 (_saferepr)
#             290 LOAD_FAST                3 (@py_assert1)
#             292 CALL                     1
#             300 LOAD_CONST               5 (('py0', 'py2'))
#             302 BUILD_CONST_KEY_MAP      2
#             304 BINARY_OP                6 (%)
#             308 STORE_FAST               4 (@py_format3)
#             310 LOAD_GLOBAL             21 (NULL + AssertionError)
#             320 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             330 LOAD_ATTR               22 (_format_explanation)
#             350 LOAD_FAST                4 (@py_format3)
#             352 CALL                     1
#             360 CALL                     1
#             368 RAISE_VARARGS            1
#         >>  370 LOAD_CONST               0 (None)
#             372 STORE_FAST               3 (@py_assert1)
# 
# 121         374 LOAD_FAST                2 (branch)
#             376 LOAD_ATTR               24 (from_bus)
#             396 STORE_FAST               3 (@py_assert1)
#             398 LOAD_FAST                3 (@py_assert1)
#             400 POP_JUMP_IF_TRUE       121 (to 644)
#             402 LOAD_CONST               6 ('assert %(py2)s\n{%(py2)s = %(py0)s.from_bus\n}')
#             404 LOAD_CONST               4 ('branch')
#             406 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             416 LOAD_ATTR               12 (locals)
#             436 CALL                     0
#             444 CONTAINS_OP              0
#             446 POP_JUMP_IF_TRUE        21 (to 490)
#             448 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             458 LOAD_ATTR               16 (_should_repr_global_name)
#             478 LOAD_FAST                2 (branch)
#             480 CALL                     1
#             488 POP_JUMP_IF_FALSE       21 (to 532)
#         >>  490 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             500 LOAD_ATTR               18 (_saferepr)
#             520 LOAD_FAST                2 (branch)
#             522 CALL                     1
#             530 JUMP_FORWARD             1 (to 534)
#         >>  532 LOAD_CONST               4 ('branch')
#         >>  534 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             544 LOAD_ATTR               18 (_saferepr)
#             564 LOAD_FAST                3 (@py_assert1)
#             566 CALL                     1
#             574 LOAD_CONST               5 (('py0', 'py2'))
#             576 BUILD_CONST_KEY_MAP      2
#             578 BINARY_OP                6 (%)
#             582 STORE_FAST               4 (@py_format3)
#             584 LOAD_GLOBAL             21 (NULL + AssertionError)
#             594 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             604 LOAD_ATTR               22 (_format_explanation)
#             624 LOAD_FAST                4 (@py_format3)
#             626 CALL                     1
#             634 CALL                     1
#             642 RAISE_VARARGS            1
#         >>  644 LOAD_CONST               0 (None)
#             646 STORE_FAST               3 (@py_assert1)
# 
# 122         648 LOAD_FAST                2 (branch)
#             650 LOAD_ATTR               26 (to_bus)
#             670 STORE_FAST               3 (@py_assert1)
#             672 LOAD_FAST                3 (@py_assert1)
#             674 POP_JUMP_IF_TRUE       121 (to 918)
#             676 LOAD_CONST               7 ('assert %(py2)s\n{%(py2)s = %(py0)s.to_bus\n}')
#             678 LOAD_CONST               4 ('branch')
#             680 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             690 LOAD_ATTR               12 (locals)
#             710 CALL                     0
#             718 CONTAINS_OP              0
#             720 POP_JUMP_IF_TRUE        21 (to 764)
#             722 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             732 LOAD_ATTR               16 (_should_repr_global_name)
#             752 LOAD_FAST                2 (branch)
#             754 CALL                     1
#             762 POP_JUMP_IF_FALSE       21 (to 806)
#         >>  764 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             774 LOAD_ATTR               18 (_saferepr)
#             794 LOAD_FAST                2 (branch)
#             796 CALL                     1
#             804 JUMP_FORWARD             1 (to 808)
#         >>  806 LOAD_CONST               4 ('branch')
#         >>  808 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             818 LOAD_ATTR               18 (_saferepr)
#             838 LOAD_FAST                3 (@py_assert1)
#             840 CALL                     1
#             848 LOAD_CONST               5 (('py0', 'py2'))
#             850 BUILD_CONST_KEY_MAP      2
#             852 BINARY_OP                6 (%)
#             856 STORE_FAST               4 (@py_format3)
#             858 LOAD_GLOBAL             21 (NULL + AssertionError)
#             868 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             878 LOAD_ATTR               22 (_format_explanation)
#             898 LOAD_FAST                4 (@py_format3)
#             900 CALL                     1
#             908 CALL                     1
#             916 RAISE_VARARGS            1
#         >>  918 LOAD_CONST               0 (None)
#             920 STORE_FAST               3 (@py_assert1)
# 
# 123         922 LOAD_FAST                2 (branch)
#             924 LOAD_ATTR               28 (p_from_mw)
#             944 STORE_FAST               3 (@py_assert1)
#             946 LOAD_CONST               0 (None)
#             948 STORE_FAST               5 (@py_assert4)
#             950 LOAD_FAST                3 (@py_assert1)
#             952 LOAD_FAST                5 (@py_assert4)
#             954 IS_OP                    1
#             956 STORE_FAST               6 (@py_assert3)
#             958 LOAD_FAST                6 (@py_assert3)
#             960 POP_JUMP_IF_TRUE       173 (to 1308)
#             962 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             972 LOAD_ATTR               30 (_call_reprcompare)
#             992 LOAD_CONST               8 (('is not',))
#             994 LOAD_FAST                6 (@py_assert3)
#             996 BUILD_TUPLE              1
#             998 LOAD_CONST               9 (('%(py2)s\n{%(py2)s = %(py0)s.p_from_mw\n} is not %(py5)s',))
#            1000 LOAD_FAST                3 (@py_assert1)
#            1002 LOAD_FAST                5 (@py_assert4)
#            1004 BUILD_TUPLE              2
#            1006 CALL                     4
#            1014 LOAD_CONST               4 ('branch')
#            1016 LOAD_GLOBAL             11 (NULL + @py_builtins)
#            1026 LOAD_ATTR               12 (locals)
#            1046 CALL                     0
#            1054 CONTAINS_OP              0
#            1056 POP_JUMP_IF_TRUE        21 (to 1100)
#            1058 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1068 LOAD_ATTR               16 (_should_repr_global_name)
#            1088 LOAD_FAST                2 (branch)
#            1090 CALL                     1
#            1098 POP_JUMP_IF_FALSE       21 (to 1142)
#         >> 1100 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1110 LOAD_ATTR               18 (_saferepr)
#            1130 LOAD_FAST                2 (branch)
#            1132 CALL                     1
#            1140 JUMP_FORWARD             1 (to 1144)
#         >> 1142 LOAD_CONST               4 ('branch')
#         >> 1144 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1154 LOAD_ATTR               18 (_saferepr)
#            1174 LOAD_FAST                3 (@py_assert1)
#            1176 CALL                     1
#            1184 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1194 LOAD_ATTR               18 (_saferepr)
#            1214 LOAD_FAST                5 (@py_assert4)
#            1216 CALL                     1
#            1224 LOAD_CONST              10 (('py0', 'py2', 'py5'))
#            1226 BUILD_CONST_KEY_MAP      3
#            1228 BINARY_OP                6 (%)
#            1232 STORE_FAST               7 (@py_format6)
#            1234 LOAD_CONST              11 ('assert %(py7)s')
#            1236 LOAD_CONST              12 ('py7')
#            1238 LOAD_FAST                7 (@py_format6)
#            1240 BUILD_MAP                1
#            1242 BINARY_OP                6 (%)
#            1246 STORE_FAST               8 (@py_format8)
#            1248 LOAD_GLOBAL             21 (NULL + AssertionError)
#            1258 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1268 LOAD_ATTR               22 (_format_explanation)
#            1288 LOAD_FAST                8 (@py_format8)
#            1290 CALL                     1
#            1298 CALL                     1
#            1306 RAISE_VARARGS            1
#         >> 1308 LOAD_CONST               0 (None)
#            1310 COPY                     1
#            1312 STORE_FAST               3 (@py_assert1)
#            1314 COPY                     1
#            1316 STORE_FAST               6 (@py_assert3)
#            1318 STORE_FAST               5 (@py_assert4)
#            1320 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_generator_data_roundtrip at 0x3afa4860, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 125>:
# 125           0 RESUME                   0
# 
# 126           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('generators')
#              46 BINARY_SUBSCR
#              50 STORE_FAST               1 (gens)
# 
# 127          52 LOAD_FAST                1 (gens)
#              54 POP_JUMP_IF_TRUE        21 (to 98)
# 
# 128          56 LOAD_GLOBAL              5 (NULL + pytest)
#              66 LOAD_ATTR                6 (skip)
#              86 LOAD_CONST               2 ('No generators in case14 result')
#              88 CALL                     1
#              96 POP_TOP
# 
# 129     >>   98 LOAD_GLOBAL              9 (NULL + GeneratorData)
#             108 LOAD_ATTR               10 (from_dict)
#             128 LOAD_FAST                1 (gens)
#             130 LOAD_CONST               3 (0)
#             132 BINARY_SUBSCR
#             136 CALL                     1
#             144 STORE_FAST               2 (gen)
# 
# 130         146 LOAD_FAST                2 (gen)
#             148 LOAD_ATTR               12 (name)
#             168 STORE_FAST               3 (@py_assert1)
#             170 LOAD_FAST                3 (@py_assert1)
#             172 POP_JUMP_IF_TRUE       121 (to 416)
#             174 LOAD_CONST               4 ('assert %(py2)s\n{%(py2)s = %(py0)s.name\n}')
#             176 LOAD_CONST               5 ('gen')
#             178 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             188 LOAD_ATTR               16 (locals)
#             208 CALL                     0
#             216 CONTAINS_OP              0
#             218 POP_JUMP_IF_TRUE        21 (to 262)
#             220 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             230 LOAD_ATTR               20 (_should_repr_global_name)
#             250 LOAD_FAST                2 (gen)
#             252 CALL                     1
#             260 POP_JUMP_IF_FALSE       21 (to 304)
#         >>  262 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             272 LOAD_ATTR               22 (_saferepr)
#             292 LOAD_FAST                2 (gen)
#             294 CALL                     1
#             302 JUMP_FORWARD             1 (to 306)
#         >>  304 LOAD_CONST               5 ('gen')
#         >>  306 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             316 LOAD_ATTR               22 (_saferepr)
#             336 LOAD_FAST                3 (@py_assert1)
#             338 CALL                     1
#             346 LOAD_CONST               6 (('py0', 'py2'))
#             348 BUILD_CONST_KEY_MAP      2
#             350 BINARY_OP                6 (%)
#             354 STORE_FAST               4 (@py_format3)
#             356 LOAD_GLOBAL             25 (NULL + AssertionError)
#             366 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             376 LOAD_ATTR               26 (_format_explanation)
#             396 LOAD_FAST                4 (@py_format3)
#             398 CALL                     1
#             406 CALL                     1
#             414 RAISE_VARARGS            1
#         >>  416 LOAD_CONST               0 (None)
#             418 STORE_FAST               3 (@py_assert1)
# 
# 131         420 LOAD_FAST                2 (gen)
#             422 LOAD_ATTR               28 (bus)
#             442 STORE_FAST               3 (@py_assert1)
#             444 LOAD_FAST                3 (@py_assert1)
#             446 POP_JUMP_IF_TRUE       121 (to 690)
#             448 LOAD_CONST               7 ('assert %(py2)s\n{%(py2)s = %(py0)s.bus\n}')
#             450 LOAD_CONST               5 ('gen')
#             452 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             462 LOAD_ATTR               16 (locals)
#             482 CALL                     0
#             490 CONTAINS_OP              0
#             492 POP_JUMP_IF_TRUE        21 (to 536)
#             494 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             504 LOAD_ATTR               20 (_should_repr_global_name)
#             524 LOAD_FAST                2 (gen)
#             526 CALL                     1
#             534 POP_JUMP_IF_FALSE       21 (to 578)
#         >>  536 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             546 LOAD_ATTR               22 (_saferepr)
#             566 LOAD_FAST                2 (gen)
#             568 CALL                     1
#             576 JUMP_FORWARD             1 (to 580)
#         >>  578 LOAD_CONST               5 ('gen')
#         >>  580 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             590 LOAD_ATTR               22 (_saferepr)
#             610 LOAD_FAST                3 (@py_assert1)
#             612 CALL                     1
#             620 LOAD_CONST               6 (('py0', 'py2'))
#             622 BUILD_CONST_KEY_MAP      2
#             624 BINARY_OP                6 (%)
#             628 STORE_FAST               4 (@py_format3)
#             630 LOAD_GLOBAL             25 (NULL + AssertionError)
#             640 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             650 LOAD_ATTR               26 (_format_explanation)
#             670 LOAD_FAST                4 (@py_format3)
#             672 CALL                     1
#             680 CALL                     1
#             688 RAISE_VARARGS            1
#         >>  690 LOAD_CONST               0 (None)
#             692 STORE_FAST               3 (@py_assert1)
# 
# 132         694 LOAD_FAST                2 (gen)
#             696 LOAD_ATTR               30 (p_mw)
#             716 STORE_FAST               3 (@py_assert1)
#             718 LOAD_CONST               3 (0)
#             720 STORE_FAST               5 (@py_assert4)
#             722 LOAD_FAST                3 (@py_assert1)
#             724 LOAD_FAST                5 (@py_assert4)
#             726 COMPARE_OP              55 (!=)
#             730 STORE_FAST               6 (@py_assert3)
#             732 LOAD_FAST                6 (@py_assert3)
#             734 POP_JUMP_IF_TRUE       173 (to 1082)
#             736 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             746 LOAD_ATTR               32 (_call_reprcompare)
#             766 LOAD_CONST               8 (('!=',))
#             768 LOAD_FAST                6 (@py_assert3)
#             770 BUILD_TUPLE              1
#             772 LOAD_CONST               9 (('%(py2)s\n{%(py2)s = %(py0)s.p_mw\n} != %(py5)s',))
#             774 LOAD_FAST                3 (@py_assert1)
#             776 LOAD_FAST                5 (@py_assert4)
#             778 BUILD_TUPLE              2
#             780 CALL                     4
#             788 LOAD_CONST               5 ('gen')
#             790 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             800 LOAD_ATTR               16 (locals)
#             820 CALL                     0
#             828 CONTAINS_OP              0
#             830 POP_JUMP_IF_TRUE        21 (to 874)
#             832 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             842 LOAD_ATTR               20 (_should_repr_global_name)
#             862 LOAD_FAST                2 (gen)
#             864 CALL                     1
#             872 POP_JUMP_IF_FALSE       21 (to 916)
#         >>  874 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             884 LOAD_ATTR               22 (_saferepr)
#             904 LOAD_FAST                2 (gen)
#             906 CALL                     1
#             914 JUMP_FORWARD             1 (to 918)
#         >>  916 LOAD_CONST               5 ('gen')
#         >>  918 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             928 LOAD_ATTR               22 (_saferepr)
#             948 LOAD_FAST                3 (@py_assert1)
#             950 CALL                     1
#             958 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             968 LOAD_ATTR               22 (_saferepr)
#             988 LOAD_FAST                5 (@py_assert4)
#             990 CALL                     1
#             998 LOAD_CONST              10 (('py0', 'py2', 'py5'))
#            1000 BUILD_CONST_KEY_MAP      3
#            1002 BINARY_OP                6 (%)
#            1006 STORE_FAST               7 (@py_format6)
#            1008 LOAD_CONST              11 ('assert %(py7)s')
#            1010 LOAD_CONST              12 ('py7')
#            1012 LOAD_FAST                7 (@py_format6)
#            1014 BUILD_MAP                1
#            1016 BINARY_OP                6 (%)
#            1020 STORE_FAST               8 (@py_format8)
#            1022 LOAD_GLOBAL             25 (NULL + AssertionError)
#            1032 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1042 LOAD_ATTR               26 (_format_explanation)
#            1062 LOAD_FAST                8 (@py_format8)
#            1064 CALL                     1
#            1072 CALL                     1
#            1080 RAISE_VARARGS            1
#         >> 1082 LOAD_CONST               0 (None)
#            1084 COPY                     1
#            1086 STORE_FAST               3 (@py_assert1)
#            1088 COPY                     1
#            1090 STORE_FAST               6 (@py_assert3)
#            1092 STORE_FAST               5 (@py_assert4)
#            1094 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestPandapowerAdapterCase39 at 0x73cd93b44e70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 135>:
# 135           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestPandapowerAdapterCase39')
#               8 STORE_NAME               2 (__qualname__)
# 
# 136          10 LOAD_CONST               1 ('\n    IEEE 39-bus (10-machine New England) — used for CloudPSS cross-validation.\n    Known results: 39 buses, 46 branches, converges.\n    ')
#              12 STORE_NAME               3 (__doc__)
# 
# 141          14 PUSH_NULL
#              16 LOAD_NAME                4 (pytest)
#              18 LOAD_ATTR               10 (fixture)
#              38 LOAD_CONST               2 (True)
#              40 KW_NAMES                 3 (('autouse',))
#              42 CALL                     1
# 
# 142          50 LOAD_CONST               4 (<code object setup at 0x73cd948d3890, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 141>)
#              52 MAKE_FUNCTION            0
# 
# 141          54 CALL                     0
# 
# 142          62 STORE_NAME               6 (setup)
# 
# 147          64 LOAD_CONST               5 (<code object test_converges at 0x3afa4d70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 147>)
#              66 MAKE_FUNCTION            0
#              68 STORE_NAME               7 (test_converges)
# 
# 151          70 LOAD_CONST               6 (<code object test_bus_count at 0x3aef47a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 151>)
#              72 MAKE_FUNCTION            0
#              74 STORE_NAME               8 (test_bus_count)
# 
# 154          76 LOAD_CONST               7 (<code object test_branch_count at 0x3aefbf80, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 154>)
#              78 MAKE_FUNCTION            0
#              80 STORE_NAME               9 (test_branch_count)
# 
# 157          82 LOAD_CONST               8 (<code object test_voltage_range at 0x3af9ed10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 157>)
#              84 MAKE_FUNCTION            0
#              86 STORE_NAME              10 (test_voltage_range)
# 
# 163          88 LOAD_CONST               9 (<code object test_total_loss_reasonable at 0x3af40530, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 163>)
#              90 MAKE_FUNCTION            0
#              92 STORE_NAME              11 (test_total_loss_reasonable)
# 
# 167          94 LOAD_CONST              10 (<code object test_has_transformers at 0x3af90370, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 167>)
#              96 MAKE_FUNCTION            0
#              98 STORE_NAME              12 (test_has_transformers)
#             100 RETURN_CONST            11 (None)
# 
# Disassembly of <code object setup at 0x73cd948d3890, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 141>:
# 141           0 RESUME                   0
# 
# 143           2 LOAD_GLOBAL              1 (NULL + PandapowerPowerFlowAdapter)
#              12 CALL                     0
#              20 LOAD_FAST                0 (self)
#              22 STORE_ATTR               1 (adapter)
# 
# 144          32 LOAD_FAST                0 (self)
#              34 LOAD_ATTR                2 (adapter)
#              54 LOAD_ATTR                5 (NULL|self + connect)
#              74 CALL                     0
#              82 POP_TOP
# 
# 145          84 LOAD_FAST                0 (self)
#              86 LOAD_ATTR                2 (adapter)
#             106 LOAD_ATTR                7 (NULL|self + run_simulation)
#             126 LOAD_CONST               1 ('case')
#             128 LOAD_CONST               2 ('case39')
#             130 BUILD_MAP                1
#             132 CALL                     1
#             140 LOAD_FAST                0 (self)
#             142 STORE_ATTR               4 (result)
#             152 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_converges at 0x3afa4d70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 147>:
# 147           0 RESUME                   0
# 
# 148           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 STORE_FAST               1 (@py_assert1)
#              26 LOAD_FAST                1 (@py_assert1)
#              28 LOAD_ATTR                2 (status)
#              48 STORE_FAST               2 (@py_assert3)
#              50 LOAD_GLOBAL              4 (SimulationStatus)
#              60 LOAD_ATTR                6 (COMPLETED)
#              80 STORE_FAST               3 (@py_assert7)
#              82 LOAD_FAST                2 (@py_assert3)
#              84 LOAD_FAST                3 (@py_assert7)
#              86 COMPARE_OP              40 (==)
#              90 STORE_FAST               4 (@py_assert5)
#              92 LOAD_FAST                4 (@py_assert5)
#              94 EXTENDED_ARG             1
#              96 POP_JUMP_IF_TRUE       266 (to 630)
#              98 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             108 LOAD_ATTR               10 (_call_reprcompare)
#             128 LOAD_CONST               1 (('==',))
#             130 LOAD_FAST                4 (@py_assert5)
#             132 BUILD_TUPLE              1
#             134 LOAD_CONST               2 (('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.result\n}.status\n} == %(py8)s\n{%(py8)s = %(py6)s.COMPLETED\n}',))
#             136 LOAD_FAST                2 (@py_assert3)
#             138 LOAD_FAST                3 (@py_assert7)
#             140 BUILD_TUPLE              2
#             142 CALL                     4
#             150 LOAD_CONST               3 ('self')
#             152 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             162 LOAD_ATTR               14 (locals)
#             182 CALL                     0
#             190 CONTAINS_OP              0
#             192 POP_JUMP_IF_TRUE        21 (to 236)
#             194 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             204 LOAD_ATTR               16 (_should_repr_global_name)
#             224 LOAD_FAST                0 (self)
#             226 CALL                     1
#             234 POP_JUMP_IF_FALSE       21 (to 278)
#         >>  236 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             246 LOAD_ATTR               18 (_saferepr)
#             266 LOAD_FAST                0 (self)
#             268 CALL                     1
#             276 JUMP_FORWARD             1 (to 280)
#         >>  278 LOAD_CONST               3 ('self')
#         >>  280 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             290 LOAD_ATTR               18 (_saferepr)
#             310 LOAD_FAST                1 (@py_assert1)
#             312 CALL                     1
#             320 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             330 LOAD_ATTR               18 (_saferepr)
#             350 LOAD_FAST                2 (@py_assert3)
#             352 CALL                     1
#             360 LOAD_CONST               4 ('SimulationStatus')
#             362 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             372 LOAD_ATTR               14 (locals)
#             392 CALL                     0
#             400 CONTAINS_OP              0
#             402 POP_JUMP_IF_TRUE        25 (to 454)
#             404 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             414 LOAD_ATTR               16 (_should_repr_global_name)
#             434 LOAD_GLOBAL              4 (SimulationStatus)
#             444 CALL                     1
#             452 POP_JUMP_IF_FALSE       25 (to 504)
#         >>  454 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             464 LOAD_ATTR               18 (_saferepr)
#             484 LOAD_GLOBAL              4 (SimulationStatus)
#             494 CALL                     1
#             502 JUMP_FORWARD             1 (to 506)
#         >>  504 LOAD_CONST               4 ('SimulationStatus')
#         >>  506 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             516 LOAD_ATTR               18 (_saferepr)
#             536 LOAD_FAST                3 (@py_assert7)
#             538 CALL                     1
#             546 LOAD_CONST               5 (('py0', 'py2', 'py4', 'py6', 'py8'))
#             548 BUILD_CONST_KEY_MAP      5
#             550 BINARY_OP                6 (%)
#             554 STORE_FAST               5 (@py_format9)
#             556 LOAD_CONST               6 ('assert %(py10)s')
#             558 LOAD_CONST               7 ('py10')
#             560 LOAD_FAST                5 (@py_format9)
#             562 BUILD_MAP                1
#             564 BINARY_OP                6 (%)
#             568 STORE_FAST               6 (@py_format11)
#             570 LOAD_GLOBAL             21 (NULL + AssertionError)
#             580 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             590 LOAD_ATTR               22 (_format_explanation)
#             610 LOAD_FAST                6 (@py_format11)
#             612 CALL                     1
#             620 CALL                     1
#             628 RAISE_VARARGS            1
#         >>  630 LOAD_CONST               0 (None)
#             632 COPY                     1
#             634 STORE_FAST               1 (@py_assert1)
#             636 COPY                     1
#             638 STORE_FAST               2 (@py_assert3)
#             640 COPY                     1
#             642 STORE_FAST               4 (@py_assert5)
#             644 STORE_FAST               3 (@py_assert7)
# 
# 149         646 LOAD_FAST                0 (self)
#             648 LOAD_ATTR                0 (result)
#             668 LOAD_ATTR               24 (data)
#             688 LOAD_CONST               8 ('converged')
#             690 BINARY_SUBSCR
#             694 STORE_FAST               7 (@py_assert0)
#             696 LOAD_CONST               9 (True)
#             698 STORE_FAST               2 (@py_assert3)
#             700 LOAD_FAST                7 (@py_assert0)
#             702 LOAD_FAST                2 (@py_assert3)
#             704 IS_OP                    0
#             706 STORE_FAST               8 (@py_assert2)
#             708 LOAD_FAST                8 (@py_assert2)
#             710 POP_JUMP_IF_TRUE       108 (to 928)
#             712 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             722 LOAD_ATTR               10 (_call_reprcompare)
#             742 LOAD_CONST              10 (('is',))
#             744 LOAD_FAST                8 (@py_assert2)
#             746 BUILD_TUPLE              1
#             748 LOAD_CONST              11 (('%(py1)s is %(py4)s',))
#             750 LOAD_FAST                7 (@py_assert0)
#             752 LOAD_FAST                2 (@py_assert3)
#             754 BUILD_TUPLE              2
#             756 CALL                     4
#             764 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             774 LOAD_ATTR               18 (_saferepr)
#             794 LOAD_FAST                7 (@py_assert0)
#             796 CALL                     1
#             804 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             814 LOAD_ATTR               18 (_saferepr)
#             834 LOAD_FAST                2 (@py_assert3)
#             836 CALL                     1
#             844 LOAD_CONST              12 (('py1', 'py4'))
#             846 BUILD_CONST_KEY_MAP      2
#             848 BINARY_OP                6 (%)
#             852 STORE_FAST               9 (@py_format5)
#             854 LOAD_CONST              13 ('assert %(py6)s')
#             856 LOAD_CONST              14 ('py6')
#             858 LOAD_FAST                9 (@py_format5)
#             860 BUILD_MAP                1
#             862 BINARY_OP                6 (%)
#             866 STORE_FAST              10 (@py_format7)
#             868 LOAD_GLOBAL             21 (NULL + AssertionError)
#             878 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             888 LOAD_ATTR               22 (_format_explanation)
#             908 LOAD_FAST               10 (@py_format7)
#             910 CALL                     1
#             918 CALL                     1
#             926 RAISE_VARARGS            1
#         >>  928 LOAD_CONST               0 (None)
#             930 COPY                     1
#             932 STORE_FAST               7 (@py_assert0)
#             934 COPY                     1
#             936 STORE_FAST               8 (@py_assert2)
#             938 STORE_FAST               2 (@py_assert3)
#             940 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_bus_count at 0x3aef47a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 151>:
# 151           0 RESUME                   0
# 
# 152           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('buses')
#              46 BINARY_SUBSCR
#              50 STORE_FAST               1 (@py_assert1)
#              52 LOAD_GLOBAL              5 (NULL + len)
#              62 LOAD_FAST                1 (@py_assert1)
#              64 CALL                     1
#              72 STORE_FAST               2 (@py_assert3)
#              74 LOAD_CONST               2 (39)
#              76 STORE_FAST               3 (@py_assert6)
#              78 LOAD_FAST                2 (@py_assert3)
#              80 LOAD_FAST                3 (@py_assert6)
#              82 COMPARE_OP              40 (==)
#              86 STORE_FAST               4 (@py_assert5)
#              88 LOAD_FAST                4 (@py_assert5)
#              90 POP_JUMP_IF_TRUE       201 (to 494)
#              92 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             102 LOAD_ATTR                8 (_call_reprcompare)
#             122 LOAD_CONST               3 (('==',))
#             124 LOAD_FAST                4 (@py_assert5)
#             126 BUILD_TUPLE              1
#             128 LOAD_CONST               4 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',))
#             130 LOAD_FAST                2 (@py_assert3)
#             132 LOAD_FAST                3 (@py_assert6)
#             134 BUILD_TUPLE              2
#             136 CALL                     4
#             144 LOAD_CONST               5 ('len')
#             146 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             156 LOAD_ATTR               12 (locals)
#             176 CALL                     0
#             184 CONTAINS_OP              0
#             186 POP_JUMP_IF_TRUE        25 (to 238)
#             188 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             198 LOAD_ATTR               14 (_should_repr_global_name)
#             218 LOAD_GLOBAL              4 (len)
#             228 CALL                     1
#             236 POP_JUMP_IF_FALSE       25 (to 288)
#         >>  238 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             248 LOAD_ATTR               16 (_saferepr)
#             268 LOAD_GLOBAL              4 (len)
#             278 CALL                     1
#             286 JUMP_FORWARD             1 (to 290)
#         >>  288 LOAD_CONST               5 ('len')
#         >>  290 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             300 LOAD_ATTR               16 (_saferepr)
#             320 LOAD_FAST                1 (@py_assert1)
#             322 CALL                     1
#             330 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             340 LOAD_ATTR               16 (_saferepr)
#             360 LOAD_FAST                2 (@py_assert3)
#             362 CALL                     1
#             370 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             380 LOAD_ATTR               16 (_saferepr)
#             400 LOAD_FAST                3 (@py_assert6)
#             402 CALL                     1
#             410 LOAD_CONST               6 (('py0', 'py2', 'py4', 'py7'))
#             412 BUILD_CONST_KEY_MAP      4
#             414 BINARY_OP                6 (%)
#             418 STORE_FAST               5 (@py_format8)
#             420 LOAD_CONST               7 ('assert %(py9)s')
#             422 LOAD_CONST               8 ('py9')
#             424 LOAD_FAST                5 (@py_format8)
#             426 BUILD_MAP                1
#             428 BINARY_OP                6 (%)
#             432 STORE_FAST               6 (@py_format10)
#             434 LOAD_GLOBAL             19 (NULL + AssertionError)
#             444 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             454 LOAD_ATTR               20 (_format_explanation)
#             474 LOAD_FAST                6 (@py_format10)
#             476 CALL                     1
#             484 CALL                     1
#             492 RAISE_VARARGS            1
#         >>  494 LOAD_CONST               0 (None)
#             496 COPY                     1
#             498 STORE_FAST               1 (@py_assert1)
#             500 COPY                     1
#             502 STORE_FAST               2 (@py_assert3)
#             504 COPY                     1
#             506 STORE_FAST               4 (@py_assert5)
#             508 STORE_FAST               3 (@py_assert6)
#             510 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_branch_count at 0x3aefbf80, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 154>:
# 154           0 RESUME                   0
# 
# 155           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('branches')
#              46 BINARY_SUBSCR
#              50 STORE_FAST               1 (@py_assert1)
#              52 LOAD_GLOBAL              5 (NULL + len)
#              62 LOAD_FAST                1 (@py_assert1)
#              64 CALL                     1
#              72 STORE_FAST               2 (@py_assert3)
#              74 LOAD_CONST               2 (46)
#              76 STORE_FAST               3 (@py_assert6)
#              78 LOAD_FAST                2 (@py_assert3)
#              80 LOAD_FAST                3 (@py_assert6)
#              82 COMPARE_OP              40 (==)
#              86 STORE_FAST               4 (@py_assert5)
#              88 LOAD_FAST                4 (@py_assert5)
#              90 POP_JUMP_IF_TRUE       201 (to 494)
#              92 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             102 LOAD_ATTR                8 (_call_reprcompare)
#             122 LOAD_CONST               3 (('==',))
#             124 LOAD_FAST                4 (@py_assert5)
#             126 BUILD_TUPLE              1
#             128 LOAD_CONST               4 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',))
#             130 LOAD_FAST                2 (@py_assert3)
#             132 LOAD_FAST                3 (@py_assert6)
#             134 BUILD_TUPLE              2
#             136 CALL                     4
#             144 LOAD_CONST               5 ('len')
#             146 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             156 LOAD_ATTR               12 (locals)
#             176 CALL                     0
#             184 CONTAINS_OP              0
#             186 POP_JUMP_IF_TRUE        25 (to 238)
#             188 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             198 LOAD_ATTR               14 (_should_repr_global_name)
#             218 LOAD_GLOBAL              4 (len)
#             228 CALL                     1
#             236 POP_JUMP_IF_FALSE       25 (to 288)
#         >>  238 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             248 LOAD_ATTR               16 (_saferepr)
#             268 LOAD_GLOBAL              4 (len)
#             278 CALL                     1
#             286 JUMP_FORWARD             1 (to 290)
#         >>  288 LOAD_CONST               5 ('len')
#         >>  290 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             300 LOAD_ATTR               16 (_saferepr)
#             320 LOAD_FAST                1 (@py_assert1)
#             322 CALL                     1
#             330 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             340 LOAD_ATTR               16 (_saferepr)
#             360 LOAD_FAST                2 (@py_assert3)
#             362 CALL                     1
#             370 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             380 LOAD_ATTR               16 (_saferepr)
#             400 LOAD_FAST                3 (@py_assert6)
#             402 CALL                     1
#             410 LOAD_CONST               6 (('py0', 'py2', 'py4', 'py7'))
#             412 BUILD_CONST_KEY_MAP      4
#             414 BINARY_OP                6 (%)
#             418 STORE_FAST               5 (@py_format8)
#             420 LOAD_CONST               7 ('assert %(py9)s')
#             422 LOAD_CONST               8 ('py9')
#             424 LOAD_FAST                5 (@py_format8)
#             426 BUILD_MAP                1
#             428 BINARY_OP                6 (%)
#             432 STORE_FAST               6 (@py_format10)
#             434 LOAD_GLOBAL             19 (NULL + AssertionError)
#             444 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             454 LOAD_ATTR               20 (_format_explanation)
#             474 LOAD_FAST                6 (@py_format10)
#             476 CALL                     1
#             484 CALL                     1
#             492 RAISE_VARARGS            1
#         >>  494 LOAD_CONST               0 (None)
#             496 COPY                     1
#             498 STORE_FAST               1 (@py_assert1)
#             500 COPY                     1
#             502 STORE_FAST               2 (@py_assert3)
#             504 COPY                     1
#             506 STORE_FAST               4 (@py_assert5)
#             508 STORE_FAST               3 (@py_assert6)
#             510 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_voltage_range at 0x3af9ed10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 157>:
# 157           0 RESUME                   0
# 
# 158           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('buses')
#              46 BINARY_SUBSCR
#              50 GET_ITER
#              52 LOAD_FAST_AND_CLEAR      1 (b)
#              54 SWAP                     2
#              56 BUILD_LIST               0
#              58 SWAP                     2
#         >>   60 FOR_ITER                23 (to 110)
#              64 STORE_FAST               1 (b)
#              66 LOAD_GLOBAL              5 (NULL + BusData)
#              76 LOAD_ATTR                6 (from_dict)
#              96 LOAD_FAST                1 (b)
#              98 CALL                     1
#             106 LIST_APPEND              2
#             108 JUMP_BACKWARD           25 (to 60)
#         >>  110 END_FOR
#             112 STORE_FAST               2 (buses)
#             114 STORE_FAST               1 (b)
# 
# 159         116 LOAD_FAST                2 (buses)
#             118 GET_ITER
#             120 LOAD_FAST_AND_CLEAR      1 (b)
#             122 SWAP                     2
#             124 BUILD_LIST               0
#             126 SWAP                     2
#         >>  128 FOR_ITER                27 (to 186)
#             132 STORE_FAST               1 (b)
#             134 LOAD_FAST                1 (b)
#             136 LOAD_ATTR                8 (voltage_pu)
#             156 POP_JUMP_IF_NOT_NONE     1 (to 160)
#             158 JUMP_BACKWARD           16 (to 128)
#         >>  160 LOAD_FAST                1 (b)
#             162 LOAD_ATTR                8 (voltage_pu)
#             182 LIST_APPEND              2
#             184 JUMP_BACKWARD           29 (to 128)
#         >>  186 END_FOR
#             188 STORE_FAST               3 (voltages)
#             190 STORE_FAST               1 (b)
# 
# 160         192 LOAD_CONST               2 (0.9)
#             194 STORE_FAST               4 (@py_assert0)
#             196 LOAD_GLOBAL             11 (NULL + min)
#             206 LOAD_FAST                3 (voltages)
#             208 CALL                     1
#             216 STORE_FAST               5 (@py_assert6)
#             218 LOAD_FAST                4 (@py_assert0)
#             220 LOAD_FAST                5 (@py_assert6)
#             222 COMPARE_OP               2 (<)
#             226 STORE_FAST               6 (@py_assert2)
#             228 LOAD_CONST               3 (1.15)
#             230 STORE_FAST               7 (@py_assert8)
#             232 LOAD_FAST                5 (@py_assert6)
#             234 LOAD_FAST                7 (@py_assert8)
#             236 COMPARE_OP               2 (<)
#             240 STORE_FAST               8 (@py_assert3)
#             242 LOAD_FAST                6 (@py_assert2)
#             244 POP_JUMP_IF_FALSE        3 (to 252)
#             246 LOAD_FAST                8 (@py_assert3)
#             248 EXTENDED_ARG             1
#             250 POP_JUMP_IF_TRUE       268 (to 788)
#         >>  252 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             262 LOAD_ATTR               14 (_call_reprcompare)
#             282 LOAD_CONST               4 (('<', '<'))
#             284 LOAD_FAST                6 (@py_assert2)
#             286 LOAD_FAST                8 (@py_assert3)
#             288 BUILD_TUPLE              2
#             290 LOAD_CONST               5 (('%(py1)s < %(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n}', '%(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n} < %(py9)s'))
#             292 LOAD_FAST                4 (@py_assert0)
#             294 LOAD_FAST                5 (@py_assert6)
#             296 LOAD_FAST                7 (@py_assert8)
#             298 BUILD_TUPLE              3
#             300 CALL                     4
#             308 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             318 LOAD_ATTR               16 (_saferepr)
#             338 LOAD_FAST                4 (@py_assert0)
#             340 CALL                     1
#             348 LOAD_CONST               6 ('min')
#             350 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             360 LOAD_ATTR               20 (locals)
#             380 CALL                     0
#             388 CONTAINS_OP              0
#             390 POP_JUMP_IF_TRUE        25 (to 442)
#             392 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             402 LOAD_ATTR               22 (_should_repr_global_name)
#             422 LOAD_GLOBAL             10 (min)
#             432 CALL                     1
#             440 POP_JUMP_IF_FALSE       25 (to 492)
#         >>  442 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             452 LOAD_ATTR               16 (_saferepr)
#             472 LOAD_GLOBAL             10 (min)
#             482 CALL                     1
#             490 JUMP_FORWARD             1 (to 494)
#         >>  492 LOAD_CONST               6 ('min')
#         >>  494 LOAD_CONST               7 ('voltages')
#             496 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             506 LOAD_ATTR               20 (locals)
#             526 CALL                     0
#             534 CONTAINS_OP              0
#             536 POP_JUMP_IF_TRUE        21 (to 580)
#             538 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             548 LOAD_ATTR               22 (_should_repr_global_name)
#             568 LOAD_FAST                3 (voltages)
#             570 CALL                     1
#             578 POP_JUMP_IF_FALSE       21 (to 622)
#         >>  580 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             590 LOAD_ATTR               16 (_saferepr)
#             610 LOAD_FAST                3 (voltages)
#             612 CALL                     1
#             620 JUMP_FORWARD             1 (to 624)
#         >>  622 LOAD_CONST               7 ('voltages')
#         >>  624 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             634 LOAD_ATTR               16 (_saferepr)
#             654 LOAD_FAST                5 (@py_assert6)
#             656 CALL                     1
#             664 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             674 LOAD_ATTR               16 (_saferepr)
#             694 LOAD_FAST                7 (@py_assert8)
#             696 CALL                     1
#             704 LOAD_CONST               8 (('py1', 'py4', 'py5', 'py7', 'py9'))
#             706 BUILD_CONST_KEY_MAP      5
#             708 BINARY_OP                6 (%)
#             712 STORE_FAST               9 (@py_format10)
#             714 LOAD_CONST               9 ('assert %(py11)s')
#             716 LOAD_CONST              10 ('py11')
#             718 LOAD_FAST                9 (@py_format10)
#             720 BUILD_MAP                1
#             722 BINARY_OP                6 (%)
#             726 STORE_FAST              10 (@py_format12)
#             728 LOAD_GLOBAL             25 (NULL + AssertionError)
#             738 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             748 LOAD_ATTR               26 (_format_explanation)
#             768 LOAD_FAST               10 (@py_format12)
#             770 CALL                     1
#             778 CALL                     1
#             786 RAISE_VARARGS            1
#         >>  788 LOAD_CONST               0 (None)
#             790 COPY                     1
#             792 STORE_FAST               4 (@py_assert0)
#             794 COPY                     1
#             796 STORE_FAST               6 (@py_assert2)
#             798 COPY                     1
#             800 STORE_FAST               8 (@py_assert3)
#             802 COPY                     1
#             804 STORE_FAST               5 (@py_assert6)
#             806 STORE_FAST               7 (@py_assert8)
# 
# 161         808 LOAD_CONST              11 (0.95)
#             810 STORE_FAST               4 (@py_assert0)
#             812 LOAD_GLOBAL             29 (NULL + max)
#             822 LOAD_FAST                3 (voltages)
#             824 CALL                     1
#             832 STORE_FAST               5 (@py_assert6)
#             834 LOAD_FAST                4 (@py_assert0)
#             836 LOAD_FAST                5 (@py_assert6)
#             838 COMPARE_OP               2 (<)
#             842 STORE_FAST               6 (@py_assert2)
#             844 LOAD_CONST               3 (1.15)
#             846 STORE_FAST               7 (@py_assert8)
#             848 LOAD_FAST                5 (@py_assert6)
#             850 LOAD_FAST                7 (@py_assert8)
#             852 COMPARE_OP               2 (<)
#             856 STORE_FAST               8 (@py_assert3)
#             858 LOAD_FAST                6 (@py_assert2)
#             860 POP_JUMP_IF_FALSE        3 (to 868)
#             862 LOAD_FAST                8 (@py_assert3)
#             864 EXTENDED_ARG             1
#             866 POP_JUMP_IF_TRUE       268 (to 1404)
#         >>  868 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             878 LOAD_ATTR               14 (_call_reprcompare)
#             898 LOAD_CONST               4 (('<', '<'))
#             900 LOAD_FAST                6 (@py_assert2)
#             902 LOAD_FAST                8 (@py_assert3)
#             904 BUILD_TUPLE              2
#             906 LOAD_CONST               5 (('%(py1)s < %(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n}', '%(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n} < %(py9)s'))
#             908 LOAD_FAST                4 (@py_assert0)
#             910 LOAD_FAST                5 (@py_assert6)
#             912 LOAD_FAST                7 (@py_assert8)
#             914 BUILD_TUPLE              3
#             916 CALL                     4
#             924 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             934 LOAD_ATTR               16 (_saferepr)
#             954 LOAD_FAST                4 (@py_assert0)
#             956 CALL                     1
#             964 LOAD_CONST              12 ('max')
#             966 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             976 LOAD_ATTR               20 (locals)
#             996 CALL                     0
#            1004 CONTAINS_OP              0
#            1006 POP_JUMP_IF_TRUE        25 (to 1058)
#            1008 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1018 LOAD_ATTR               22 (_should_repr_global_name)
#            1038 LOAD_GLOBAL             28 (max)
#            1048 CALL                     1
#            1056 POP_JUMP_IF_FALSE       25 (to 1108)
#         >> 1058 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1068 LOAD_ATTR               16 (_saferepr)
#            1088 LOAD_GLOBAL             28 (max)
#            1098 CALL                     1
#            1106 JUMP_FORWARD             1 (to 1110)
#         >> 1108 LOAD_CONST              12 ('max')
#         >> 1110 LOAD_CONST               7 ('voltages')
#            1112 LOAD_GLOBAL             19 (NULL + @py_builtins)
#            1122 LOAD_ATTR               20 (locals)
#            1142 CALL                     0
#            1150 CONTAINS_OP              0
#            1152 POP_JUMP_IF_TRUE        21 (to 1196)
#            1154 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1164 LOAD_ATTR               22 (_should_repr_global_name)
#            1184 LOAD_FAST                3 (voltages)
#            1186 CALL                     1
#            1194 POP_JUMP_IF_FALSE       21 (to 1238)
#         >> 1196 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1206 LOAD_ATTR               16 (_saferepr)
#            1226 LOAD_FAST                3 (voltages)
#            1228 CALL                     1
#            1236 JUMP_FORWARD             1 (to 1240)
#         >> 1238 LOAD_CONST               7 ('voltages')
#         >> 1240 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1250 LOAD_ATTR               16 (_saferepr)
#            1270 LOAD_FAST                5 (@py_assert6)
#            1272 CALL                     1
#            1280 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1290 LOAD_ATTR               16 (_saferepr)
#            1310 LOAD_FAST                7 (@py_assert8)
#            1312 CALL                     1
#            1320 LOAD_CONST               8 (('py1', 'py4', 'py5', 'py7', 'py9'))
#            1322 BUILD_CONST_KEY_MAP      5
#            1324 BINARY_OP                6 (%)
#            1328 STORE_FAST               9 (@py_format10)
#            1330 LOAD_CONST               9 ('assert %(py11)s')
#            1332 LOAD_CONST              10 ('py11')
#            1334 LOAD_FAST                9 (@py_format10)
#            1336 BUILD_MAP                1
#            1338 BINARY_OP                6 (%)
#            1342 STORE_FAST              10 (@py_format12)
#            1344 LOAD_GLOBAL             25 (NULL + AssertionError)
#            1354 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1364 LOAD_ATTR               26 (_format_explanation)
#            1384 LOAD_FAST               10 (@py_format12)
#            1386 CALL                     1
#            1394 CALL                     1
#            1402 RAISE_VARARGS            1
#         >> 1404 LOAD_CONST               0 (None)
#            1406 COPY                     1
#            1408 STORE_FAST               4 (@py_assert0)
#            1410 COPY                     1
#            1412 STORE_FAST               6 (@py_assert2)
#            1414 COPY                     1
#            1416 STORE_FAST               8 (@py_assert3)
#            1418 COPY                     1
#            1420 STORE_FAST               5 (@py_assert6)
#            1422 STORE_FAST               7 (@py_assert8)
#            1424 RETURN_CONST             0 (None)
#         >> 1426 SWAP                     2
#            1428 POP_TOP
# 
# 158        1430 SWAP                     2
#            1432 STORE_FAST               1 (b)
#            1434 RERAISE                  0
#         >> 1436 SWAP                     2
#            1438 POP_TOP
# 
# 159        1440 SWAP                     2
#            1442 STORE_FAST               1 (b)
#            1444 RERAISE                  0
# ExceptionTable:
#   56 to 110 -> 1426 [2]
#   124 to 156 -> 1436 [2]
#   160 to 186 -> 1436 [2]
# 
# Disassembly of <code object test_total_loss_reasonable at 0x3af40530, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 163>:
# 163           0 RESUME                   0
# 
# 164           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('summary')
#              46 BINARY_SUBSCR
#              50 STORE_FAST               1 (summary)
# 
# 165          52 LOAD_CONST               2 (10)
#              54 STORE_FAST               2 (@py_assert0)
#              56 LOAD_FAST                1 (summary)
#              58 LOAD_CONST               3 ('total_loss_mw')
#              60 BINARY_SUBSCR
#              64 STORE_FAST               3 (@py_assert4)
#              66 LOAD_FAST                2 (@py_assert0)
#              68 LOAD_FAST                3 (@py_assert4)
#              70 COMPARE_OP               2 (<)
#              74 STORE_FAST               4 (@py_assert2)
#              76 LOAD_CONST               4 (200)
#              78 STORE_FAST               5 (@py_assert6)
#              80 LOAD_FAST                3 (@py_assert4)
#              82 LOAD_FAST                5 (@py_assert6)
#              84 COMPARE_OP               2 (<)
#              88 STORE_FAST               6 (@py_assert3)
#              90 LOAD_FAST                4 (@py_assert2)
#              92 POP_JUMP_IF_FALSE        2 (to 98)
#              94 LOAD_FAST                6 (@py_assert3)
#              96 POP_JUMP_IF_TRUE       130 (to 358)
#         >>   98 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             108 LOAD_ATTR                6 (_call_reprcompare)
#             128 LOAD_CONST               5 (('<', '<'))
#             130 LOAD_FAST                4 (@py_assert2)
#             132 LOAD_FAST                6 (@py_assert3)
#             134 BUILD_TUPLE              2
#             136 LOAD_CONST               6 (('%(py1)s < %(py5)s', '%(py5)s < %(py7)s'))
#             138 LOAD_FAST                2 (@py_assert0)
#             140 LOAD_FAST                3 (@py_assert4)
#             142 LOAD_FAST                5 (@py_assert6)
#             144 BUILD_TUPLE              3
#             146 CALL                     4
#             154 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             164 LOAD_ATTR                8 (_saferepr)
#             184 LOAD_FAST                2 (@py_assert0)
#             186 CALL                     1
#             194 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             204 LOAD_ATTR                8 (_saferepr)
#             224 LOAD_FAST                3 (@py_assert4)
#             226 CALL                     1
#             234 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             244 LOAD_ATTR                8 (_saferepr)
#             264 LOAD_FAST                5 (@py_assert6)
#             266 CALL                     1
#             274 LOAD_CONST               7 (('py1', 'py5', 'py7'))
#             276 BUILD_CONST_KEY_MAP      3
#             278 BINARY_OP                6 (%)
#             282 STORE_FAST               7 (@py_format8)
#             284 LOAD_CONST               8 ('assert %(py9)s')
#             286 LOAD_CONST               9 ('py9')
#             288 LOAD_FAST                7 (@py_format8)
#             290 BUILD_MAP                1
#             292 BINARY_OP                6 (%)
#             296 STORE_FAST               8 (@py_format10)
#             298 LOAD_GLOBAL             11 (NULL + AssertionError)
#             308 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             318 LOAD_ATTR               12 (_format_explanation)
#             338 LOAD_FAST                8 (@py_format10)
#             340 CALL                     1
#             348 CALL                     1
#             356 RAISE_VARARGS            1
#         >>  358 LOAD_CONST               0 (None)
#             360 COPY                     1
#             362 STORE_FAST               2 (@py_assert0)
#             364 COPY                     1
#             366 STORE_FAST               4 (@py_assert2)
#             368 COPY                     1
#             370 STORE_FAST               6 (@py_assert3)
#             372 COPY                     1
#             374 STORE_FAST               3 (@py_assert4)
#             376 STORE_FAST               5 (@py_assert6)
#             378 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_has_transformers at 0x3af90370, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 167>:
# 167           0 RESUME                   0
# 
# 168           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('branches')
#              46 BINARY_SUBSCR
#              50 GET_ITER
#              52 LOAD_FAST_AND_CLEAR      1 (br)
#              54 SWAP                     2
#              56 BUILD_LIST               0
#              58 SWAP                     2
#         >>   60 FOR_ITER                23 (to 110)
#              64 STORE_FAST               1 (br)
#              66 LOAD_GLOBAL              5 (NULL + BranchData)
#              76 LOAD_ATTR                6 (from_dict)
#              96 LOAD_FAST                1 (br)
#              98 CALL                     1
#             106 LIST_APPEND              2
#             108 JUMP_BACKWARD           25 (to 60)
#         >>  110 END_FOR
#             112 STORE_FAST               2 (branches)
#             114 STORE_FAST               1 (br)
# 
# 169         116 LOAD_FAST                2 (branches)
#             118 GET_ITER
#             120 LOAD_FAST_AND_CLEAR      1 (br)
#             122 SWAP                     2
#             124 BUILD_LIST               0
#             126 SWAP                     2
#         >>  128 FOR_ITER                34 (to 200)
#             132 STORE_FAST               1 (br)
#             134 LOAD_FAST                1 (br)
#             136 LOAD_ATTR                8 (branch_type)
#             156 LOAD_GLOBAL             10 (BranchType)
#             166 LOAD_ATTR               12 (TRANSFORMER)
#             186 COMPARE_OP              40 (==)
#             190 POP_JUMP_IF_TRUE         1 (to 194)
#             192 JUMP_BACKWARD           33 (to 128)
#         >>  194 LOAD_FAST                1 (br)
#             196 LIST_APPEND              2
#             198 JUMP_BACKWARD           36 (to 128)
#         >>  200 END_FOR
#             202 STORE_FAST               3 (trafos)
#             204 STORE_FAST               1 (br)
# 
# 170         206 LOAD_GLOBAL             15 (NULL + len)
#             216 LOAD_FAST                3 (trafos)
#             218 CALL                     1
#             226 STORE_FAST               4 (@py_assert2)
#             228 LOAD_CONST               2 (1)
#             230 STORE_FAST               5 (@py_assert5)
#             232 LOAD_FAST                4 (@py_assert2)
#             234 LOAD_FAST                5 (@py_assert5)
#             236 COMPARE_OP              92 (>=)
#             240 STORE_FAST               6 (@py_assert4)
#             242 LOAD_FAST                6 (@py_assert4)
#             244 POP_JUMP_IF_TRUE       246 (to 738)
#             246 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             256 LOAD_ATTR               18 (_call_reprcompare)
#             276 LOAD_CONST               3 (('>=',))
#             278 LOAD_FAST                6 (@py_assert4)
#             280 BUILD_TUPLE              1
#             282 LOAD_CONST               4 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} >= %(py6)s',))
#             284 LOAD_FAST                4 (@py_assert2)
#             286 LOAD_FAST                5 (@py_assert5)
#             288 BUILD_TUPLE              2
#             290 CALL                     4
#             298 LOAD_CONST               5 ('len')
#             300 LOAD_GLOBAL             21 (NULL + @py_builtins)
#             310 LOAD_ATTR               22 (locals)
#             330 CALL                     0
#             338 CONTAINS_OP              0
#             340 POP_JUMP_IF_TRUE        25 (to 392)
#             342 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             352 LOAD_ATTR               24 (_should_repr_global_name)
#             372 LOAD_GLOBAL             14 (len)
#             382 CALL                     1
#             390 POP_JUMP_IF_FALSE       25 (to 442)
#         >>  392 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             402 LOAD_ATTR               26 (_saferepr)
#             422 LOAD_GLOBAL             14 (len)
#             432 CALL                     1
#             440 JUMP_FORWARD             1 (to 444)
#         >>  442 LOAD_CONST               5 ('len')
#         >>  444 LOAD_CONST               6 ('trafos')
#             446 LOAD_GLOBAL             21 (NULL + @py_builtins)
#             456 LOAD_ATTR               22 (locals)
#             476 CALL                     0
#             484 CONTAINS_OP              0
#             486 POP_JUMP_IF_TRUE        21 (to 530)
#             488 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             498 LOAD_ATTR               24 (_should_repr_global_name)
#             518 LOAD_FAST                3 (trafos)
#             520 CALL                     1
#             528 POP_JUMP_IF_FALSE       21 (to 572)
#         >>  530 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             540 LOAD_ATTR               26 (_saferepr)
#             560 LOAD_FAST                3 (trafos)
#             562 CALL                     1
#             570 JUMP_FORWARD             1 (to 574)
#         >>  572 LOAD_CONST               6 ('trafos')
#         >>  574 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             584 LOAD_ATTR               26 (_saferepr)
#             604 LOAD_FAST                4 (@py_assert2)
#             606 CALL                     1
#             614 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             624 LOAD_ATTR               26 (_saferepr)
#             644 LOAD_FAST                5 (@py_assert5)
#             646 CALL                     1
#             654 LOAD_CONST               7 (('py0', 'py1', 'py3', 'py6'))
#             656 BUILD_CONST_KEY_MAP      4
#             658 BINARY_OP                6 (%)
#             662 STORE_FAST               7 (@py_format7)
#             664 LOAD_CONST               8 ('assert %(py8)s')
#             666 LOAD_CONST               9 ('py8')
#             668 LOAD_FAST                7 (@py_format7)
#             670 BUILD_MAP                1
#             672 BINARY_OP                6 (%)
#             676 STORE_FAST               8 (@py_format9)
#             678 LOAD_GLOBAL             29 (NULL + AssertionError)
#             688 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             698 LOAD_ATTR               30 (_format_explanation)
#             718 LOAD_FAST                8 (@py_format9)
#             720 CALL                     1
#             728 CALL                     1
#             736 RAISE_VARARGS            1
#         >>  738 LOAD_CONST               0 (None)
#             740 COPY                     1
#             742 STORE_FAST               4 (@py_assert2)
#             744 COPY                     1
#             746 STORE_FAST               6 (@py_assert4)
#             748 STORE_FAST               5 (@py_assert5)
#             750 RETURN_CONST             0 (None)
#         >>  752 SWAP                     2
#             754 POP_TOP
# 
# 168         756 SWAP                     2
#             758 STORE_FAST               1 (br)
#             760 RERAISE                  0
#         >>  762 SWAP                     2
#             764 POP_TOP
# 
# 169         766 SWAP                     2
#             768 STORE_FAST               1 (br)
#             770 RERAISE                  0
# ExceptionTable:
#   56 to 110 -> 752 [2]
#   124 to 190 -> 762 [2]
#   194 to 200 -> 762 [2]
# 
# Disassembly of <code object TestPandapowerAdapterNetworkInput at 0x73cd93b065b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 173>:
# 173           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestPandapowerAdapterNetworkInput')
#               8 STORE_NAME               2 (__qualname__)
# 
# 174          10 LOAD_CONST               1 ('Test with direct pandapowerNet input.')
#              12 STORE_NAME               3 (__doc__)
# 
# 176          14 LOAD_CONST               2 (<code object test_network_object_input at 0x3afa6510, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 176>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_network_object_input)
# 
# 186          20 LOAD_CONST               3 (<code object test_network_overrides_case at 0x3afa6f70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 186>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_network_overrides_case)
# 
# 196          26 LOAD_CONST               4 (<code object test_load_model_then_run at 0x3afa79c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 196>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_load_model_then_run)
#              32 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_network_object_input at 0x3afa6510, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 176>:
# 176           0 RESUME                   0
# 
# 177           2 LOAD_CONST               1 (0)
#               4 LOAD_CONST               0 (None)
#               6 IMPORT_NAME              0 (pandapower.networks)
#               8 IMPORT_FROM              1 (networks)
#              10 STORE_FAST               1 (nw)
#              12 POP_TOP
# 
# 179          14 LOAD_FAST                1 (nw)
#              16 LOAD_ATTR                5 (NULL|self + case9)
#              36 CALL                     0
#              44 STORE_FAST               2 (net)
# 
# 180          46 LOAD_GLOBAL              7 (NULL + PandapowerPowerFlowAdapter)
#              56 CALL                     0
#              64 STORE_FAST               3 (adapter)
# 
# 181          66 LOAD_FAST                3 (adapter)
#              68 LOAD_ATTR                9 (NULL|self + connect)
#              88 CALL                     0
#              96 POP_TOP
# 
# 182          98 LOAD_FAST                3 (adapter)
#             100 LOAD_ATTR               11 (NULL|self + run_simulation)
#             120 LOAD_CONST               2 ('network')
#             122 LOAD_FAST                2 (net)
#             124 BUILD_MAP                1
#             126 CALL                     1
#             134 STORE_FAST               4 (result)
# 
# 183         136 LOAD_FAST                4 (result)
#             138 LOAD_ATTR               12 (status)
#             158 STORE_FAST               5 (@py_assert1)
#             160 LOAD_GLOBAL             14 (SimulationStatus)
#             170 LOAD_ATTR               16 (COMPLETED)
#             190 STORE_FAST               6 (@py_assert5)
#             192 LOAD_FAST                5 (@py_assert1)
#             194 LOAD_FAST                6 (@py_assert5)
#             196 COMPARE_OP              40 (==)
#             200 STORE_FAST               7 (@py_assert3)
#             202 LOAD_FAST                7 (@py_assert3)
#             204 POP_JUMP_IF_TRUE       246 (to 698)
#             206 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             216 LOAD_ATTR               20 (_call_reprcompare)
#             236 LOAD_CONST               3 (('==',))
#             238 LOAD_FAST                7 (@py_assert3)
#             240 BUILD_TUPLE              1
#             242 LOAD_CONST               4 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.COMPLETED\n}',))
#             244 LOAD_FAST                5 (@py_assert1)
#             246 LOAD_FAST                6 (@py_assert5)
#             248 BUILD_TUPLE              2
#             250 CALL                     4
#             258 LOAD_CONST               5 ('result')
#             260 LOAD_GLOBAL             23 (NULL + @py_builtins)
#             270 LOAD_ATTR               24 (locals)
#             290 CALL                     0
#             298 CONTAINS_OP              0
#             300 POP_JUMP_IF_TRUE        21 (to 344)
#             302 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             312 LOAD_ATTR               26 (_should_repr_global_name)
#             332 LOAD_FAST                4 (result)
#             334 CALL                     1
#             342 POP_JUMP_IF_FALSE       21 (to 386)
#         >>  344 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             354 LOAD_ATTR               28 (_saferepr)
#             374 LOAD_FAST                4 (result)
#             376 CALL                     1
#             384 JUMP_FORWARD             1 (to 388)
#         >>  386 LOAD_CONST               5 ('result')
#         >>  388 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             398 LOAD_ATTR               28 (_saferepr)
#             418 LOAD_FAST                5 (@py_assert1)
#             420 CALL                     1
#             428 LOAD_CONST               6 ('SimulationStatus')
#             430 LOAD_GLOBAL             23 (NULL + @py_builtins)
#             440 LOAD_ATTR               24 (locals)
#             460 CALL                     0
#             468 CONTAINS_OP              0
#             470 POP_JUMP_IF_TRUE        25 (to 522)
#             472 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             482 LOAD_ATTR               26 (_should_repr_global_name)
#             502 LOAD_GLOBAL             14 (SimulationStatus)
#             512 CALL                     1
#             520 POP_JUMP_IF_FALSE       25 (to 572)
#         >>  522 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             532 LOAD_ATTR               28 (_saferepr)
#             552 LOAD_GLOBAL             14 (SimulationStatus)
#             562 CALL                     1
#             570 JUMP_FORWARD             1 (to 574)
#         >>  572 LOAD_CONST               6 ('SimulationStatus')
#         >>  574 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             584 LOAD_ATTR               28 (_saferepr)
#             604 LOAD_FAST                6 (@py_assert5)
#             606 CALL                     1
#             614 LOAD_CONST               7 (('py0', 'py2', 'py4', 'py6'))
#             616 BUILD_CONST_KEY_MAP      4
#             618 BINARY_OP                6 (%)
#             622 STORE_FAST               8 (@py_format7)
#             624 LOAD_CONST               8 ('assert %(py8)s')
#             626 LOAD_CONST               9 ('py8')
#             628 LOAD_FAST                8 (@py_format7)
#             630 BUILD_MAP                1
#             632 BINARY_OP                6 (%)
#             636 STORE_FAST               9 (@py_format9)
#             638 LOAD_GLOBAL             31 (NULL + AssertionError)
#             648 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             658 LOAD_ATTR               32 (_format_explanation)
#             678 LOAD_FAST                9 (@py_format9)
#             680 CALL                     1
#             688 CALL                     1
#             696 RAISE_VARARGS            1
#         >>  698 LOAD_CONST               0 (None)
#             700 COPY                     1
#             702 STORE_FAST               5 (@py_assert1)
#             704 COPY                     1
#             706 STORE_FAST               7 (@py_assert3)
#             708 STORE_FAST               6 (@py_assert5)
# 
# 184         710 LOAD_FAST                4 (result)
#             712 LOAD_ATTR               34 (data)
#             732 LOAD_CONST              10 ('buses')
#             734 BINARY_SUBSCR
#             738 STORE_FAST               5 (@py_assert1)
#             740 LOAD_GLOBAL             37 (NULL + len)
#             750 LOAD_FAST                5 (@py_assert1)
#             752 CALL                     1
#             760 STORE_FAST               7 (@py_assert3)
#             762 LOAD_CONST              11 (9)
#             764 STORE_FAST              10 (@py_assert6)
#             766 LOAD_FAST                7 (@py_assert3)
#             768 LOAD_FAST               10 (@py_assert6)
#             770 COMPARE_OP              40 (==)
#             774 STORE_FAST               6 (@py_assert5)
#             776 LOAD_FAST                6 (@py_assert5)
#             778 POP_JUMP_IF_TRUE       201 (to 1182)
#             780 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             790 LOAD_ATTR               20 (_call_reprcompare)
#             810 LOAD_CONST               3 (('==',))
#             812 LOAD_FAST                6 (@py_assert5)
#             814 BUILD_TUPLE              1
#             816 LOAD_CONST              12 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',))
#             818 LOAD_FAST                7 (@py_assert3)
#             820 LOAD_FAST               10 (@py_assert6)
#             822 BUILD_TUPLE              2
#             824 CALL                     4
#             832 LOAD_CONST              13 ('len')
#             834 LOAD_GLOBAL             23 (NULL + @py_builtins)
#             844 LOAD_ATTR               24 (locals)
#             864 CALL                     0
#             872 CONTAINS_OP              0
#             874 POP_JUMP_IF_TRUE        25 (to 926)
#             876 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             886 LOAD_ATTR               26 (_should_repr_global_name)
#             906 LOAD_GLOBAL             36 (len)
#             916 CALL                     1
#             924 POP_JUMP_IF_FALSE       25 (to 976)
#         >>  926 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             936 LOAD_ATTR               28 (_saferepr)
#             956 LOAD_GLOBAL             36 (len)
#             966 CALL                     1
#             974 JUMP_FORWARD             1 (to 978)
#         >>  976 LOAD_CONST              13 ('len')
#         >>  978 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             988 LOAD_ATTR               28 (_saferepr)
#            1008 LOAD_FAST                5 (@py_assert1)
#            1010 CALL                     1
#            1018 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1028 LOAD_ATTR               28 (_saferepr)
#            1048 LOAD_FAST                7 (@py_assert3)
#            1050 CALL                     1
#            1058 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1068 LOAD_ATTR               28 (_saferepr)
#            1088 LOAD_FAST               10 (@py_assert6)
#            1090 CALL                     1
#            1098 LOAD_CONST              14 (('py0', 'py2', 'py4', 'py7'))
#            1100 BUILD_CONST_KEY_MAP      4
#            1102 BINARY_OP                6 (%)
#            1106 STORE_FAST              11 (@py_format8)
#            1108 LOAD_CONST              15 ('assert %(py9)s')
#            1110 LOAD_CONST              16 ('py9')
#            1112 LOAD_FAST               11 (@py_format8)
#            1114 BUILD_MAP                1
#            1116 BINARY_OP                6 (%)
#            1120 STORE_FAST              12 (@py_format10)
#            1122 LOAD_GLOBAL             31 (NULL + AssertionError)
#            1132 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1142 LOAD_ATTR               32 (_format_explanation)
#            1162 LOAD_FAST               12 (@py_format10)
#            1164 CALL                     1
#            1172 CALL                     1
#            1180 RAISE_VARARGS            1
#         >> 1182 LOAD_CONST               0 (None)
#            1184 COPY                     1
#            1186 STORE_FAST               5 (@py_assert1)
#            1188 COPY                     1
#            1190 STORE_FAST               7 (@py_assert3)
#            1192 COPY                     1
#            1194 STORE_FAST               6 (@py_assert5)
#            1196 STORE_FAST              10 (@py_assert6)
#            1198 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_network_overrides_case at 0x3afa6f70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 186>:
# 186           0 RESUME                   0
# 
# 187           2 LOAD_CONST               1 (0)
#               4 LOAD_CONST               0 (None)
#               6 IMPORT_NAME              0 (pandapower.networks)
#               8 IMPORT_FROM              1 (networks)
#              10 STORE_FAST               1 (nw)
#              12 POP_TOP
# 
# 189          14 LOAD_FAST                1 (nw)
#              16 LOAD_ATTR                5 (NULL|self + case9)
#              36 CALL                     0
#              44 STORE_FAST               2 (net)
# 
# 190          46 LOAD_GLOBAL              7 (NULL + PandapowerPowerFlowAdapter)
#              56 CALL                     0
#              64 STORE_FAST               3 (adapter)
# 
# 191          66 LOAD_FAST                3 (adapter)
#              68 LOAD_ATTR                9 (NULL|self + connect)
#              88 CALL                     0
#              96 POP_TOP
# 
# 192          98 LOAD_FAST                3 (adapter)
#             100 LOAD_ATTR               11 (NULL|self + run_simulation)
#             120 LOAD_FAST                2 (net)
#             122 LOAD_CONST               2 ('case14')
#             124 LOAD_CONST               3 (('network', 'case'))
#             126 BUILD_CONST_KEY_MAP      2
#             128 CALL                     1
#             136 STORE_FAST               4 (result)
# 
# 193         138 LOAD_FAST                4 (result)
#             140 LOAD_ATTR               12 (status)
#             160 STORE_FAST               5 (@py_assert1)
#             162 LOAD_GLOBAL             14 (SimulationStatus)
#             172 LOAD_ATTR               16 (COMPLETED)
#             192 STORE_FAST               6 (@py_assert5)
#             194 LOAD_FAST                5 (@py_assert1)
#             196 LOAD_FAST                6 (@py_assert5)
#             198 COMPARE_OP              40 (==)
#             202 STORE_FAST               7 (@py_assert3)
#             204 LOAD_FAST                7 (@py_assert3)
#             206 POP_JUMP_IF_TRUE       246 (to 700)
#             208 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             218 LOAD_ATTR               20 (_call_reprcompare)
#             238 LOAD_CONST               4 (('==',))
#             240 LOAD_FAST                7 (@py_assert3)
#             242 BUILD_TUPLE              1
#             244 LOAD_CONST               5 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.COMPLETED\n}',))
#             246 LOAD_FAST                5 (@py_assert1)
#             248 LOAD_FAST                6 (@py_assert5)
#             250 BUILD_TUPLE              2
#             252 CALL                     4
#             260 LOAD_CONST               6 ('result')
#             262 LOAD_GLOBAL             23 (NULL + @py_builtins)
#             272 LOAD_ATTR               24 (locals)
#             292 CALL                     0
#             300 CONTAINS_OP              0
#             302 POP_JUMP_IF_TRUE        21 (to 346)
#             304 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             314 LOAD_ATTR               26 (_should_repr_global_name)
#             334 LOAD_FAST                4 (result)
#             336 CALL                     1
#             344 POP_JUMP_IF_FALSE       21 (to 388)
#         >>  346 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             356 LOAD_ATTR               28 (_saferepr)
#             376 LOAD_FAST                4 (result)
#             378 CALL                     1
#             386 JUMP_FORWARD             1 (to 390)
#         >>  388 LOAD_CONST               6 ('result')
#         >>  390 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             400 LOAD_ATTR               28 (_saferepr)
#             420 LOAD_FAST                5 (@py_assert1)
#             422 CALL                     1
#             430 LOAD_CONST               7 ('SimulationStatus')
#             432 LOAD_GLOBAL             23 (NULL + @py_builtins)
#             442 LOAD_ATTR               24 (locals)
#             462 CALL                     0
#             470 CONTAINS_OP              0
#             472 POP_JUMP_IF_TRUE        25 (to 524)
#             474 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             484 LOAD_ATTR               26 (_should_repr_global_name)
#             504 LOAD_GLOBAL             14 (SimulationStatus)
#             514 CALL                     1
#             522 POP_JUMP_IF_FALSE       25 (to 574)
#         >>  524 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             534 LOAD_ATTR               28 (_saferepr)
#             554 LOAD_GLOBAL             14 (SimulationStatus)
#             564 CALL                     1
#             572 JUMP_FORWARD             1 (to 576)
#         >>  574 LOAD_CONST               7 ('SimulationStatus')
#         >>  576 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             586 LOAD_ATTR               28 (_saferepr)
#             606 LOAD_FAST                6 (@py_assert5)
#             608 CALL                     1
#             616 LOAD_CONST               8 (('py0', 'py2', 'py4', 'py6'))
#             618 BUILD_CONST_KEY_MAP      4
#             620 BINARY_OP                6 (%)
#             624 STORE_FAST               8 (@py_format7)
#             626 LOAD_CONST               9 ('assert %(py8)s')
#             628 LOAD_CONST              10 ('py8')
#             630 LOAD_FAST                8 (@py_format7)
#             632 BUILD_MAP                1
#             634 BINARY_OP                6 (%)
#             638 STORE_FAST               9 (@py_format9)
#             640 LOAD_GLOBAL             31 (NULL + AssertionError)
#             650 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             660 LOAD_ATTR               32 (_format_explanation)
#             680 LOAD_FAST                9 (@py_format9)
#             682 CALL                     1
#             690 CALL                     1
#             698 RAISE_VARARGS            1
#         >>  700 LOAD_CONST               0 (None)
#             702 COPY                     1
#             704 STORE_FAST               5 (@py_assert1)
#             706 COPY                     1
#             708 STORE_FAST               7 (@py_assert3)
#             710 STORE_FAST               6 (@py_assert5)
# 
# 194         712 LOAD_FAST                4 (result)
#             714 LOAD_ATTR               34 (data)
#             734 LOAD_CONST              11 ('buses')
#             736 BINARY_SUBSCR
#             740 STORE_FAST               5 (@py_assert1)
#             742 LOAD_GLOBAL             37 (NULL + len)
#             752 LOAD_FAST                5 (@py_assert1)
#             754 CALL                     1
#             762 STORE_FAST               7 (@py_assert3)
#             764 LOAD_CONST              12 (9)
#             766 STORE_FAST              10 (@py_assert6)
#             768 LOAD_FAST                7 (@py_assert3)
#             770 LOAD_FAST               10 (@py_assert6)
#             772 COMPARE_OP              40 (==)
#             776 STORE_FAST               6 (@py_assert5)
#             778 LOAD_FAST                6 (@py_assert5)
#             780 POP_JUMP_IF_TRUE       201 (to 1184)
#             782 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             792 LOAD_ATTR               20 (_call_reprcompare)
#             812 LOAD_CONST               4 (('==',))
#             814 LOAD_FAST                6 (@py_assert5)
#             816 BUILD_TUPLE              1
#             818 LOAD_CONST              13 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',))
#             820 LOAD_FAST                7 (@py_assert3)
#             822 LOAD_FAST               10 (@py_assert6)
#             824 BUILD_TUPLE              2
#             826 CALL                     4
#             834 LOAD_CONST              14 ('len')
#             836 LOAD_GLOBAL             23 (NULL + @py_builtins)
#             846 LOAD_ATTR               24 (locals)
#             866 CALL                     0
#             874 CONTAINS_OP              0
#             876 POP_JUMP_IF_TRUE        25 (to 928)
#             878 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             888 LOAD_ATTR               26 (_should_repr_global_name)
#             908 LOAD_GLOBAL             36 (len)
#             918 CALL                     1
#             926 POP_JUMP_IF_FALSE       25 (to 978)
#         >>  928 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             938 LOAD_ATTR               28 (_saferepr)
#             958 LOAD_GLOBAL             36 (len)
#             968 CALL                     1
#             976 JUMP_FORWARD             1 (to 980)
#         >>  978 LOAD_CONST              14 ('len')
#         >>  980 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             990 LOAD_ATTR               28 (_saferepr)
#            1010 LOAD_FAST                5 (@py_assert1)
#            1012 CALL                     1
#            1020 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1030 LOAD_ATTR               28 (_saferepr)
#            1050 LOAD_FAST                7 (@py_assert3)
#            1052 CALL                     1
#            1060 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1070 LOAD_ATTR               28 (_saferepr)
#            1090 LOAD_FAST               10 (@py_assert6)
#            1092 CALL                     1
#            1100 LOAD_CONST              15 (('py0', 'py2', 'py4', 'py7'))
#            1102 BUILD_CONST_KEY_MAP      4
#            1104 BINARY_OP                6 (%)
#            1108 STORE_FAST              11 (@py_format8)
#            1110 LOAD_CONST              16 ('assert %(py9)s')
#            1112 LOAD_CONST              17 ('py9')
#            1114 LOAD_FAST               11 (@py_format8)
#            1116 BUILD_MAP                1
#            1118 BINARY_OP                6 (%)
#            1122 STORE_FAST              12 (@py_format10)
#            1124 LOAD_GLOBAL             31 (NULL + AssertionError)
#            1134 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1144 LOAD_ATTR               32 (_format_explanation)
#            1164 LOAD_FAST               12 (@py_format10)
#            1166 CALL                     1
#            1174 CALL                     1
#            1182 RAISE_VARARGS            1
#         >> 1184 LOAD_CONST               0 (None)
#            1186 COPY                     1
#            1188 STORE_FAST               5 (@py_assert1)
#            1190 COPY                     1
#            1192 STORE_FAST               7 (@py_assert3)
#            1194 COPY                     1
#            1196 STORE_FAST               6 (@py_assert5)
#            1198 STORE_FAST              10 (@py_assert6)
#            1200 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_load_model_then_run at 0x3afa79c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 196>:
# 196           0 RESUME                   0
# 
# 197           2 LOAD_GLOBAL              1 (NULL + PandapowerPowerFlowAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
# 198          22 LOAD_FAST                1 (adapter)
#              24 LOAD_ATTR                3 (NULL|self + connect)
#              44 CALL                     0
#              52 POP_TOP
# 
# 199          54 LOAD_FAST                1 (adapter)
#              56 LOAD_ATTR                5 (NULL|self + load_model)
#              76 LOAD_CONST               1 ('case14')
#              78 CALL                     1
#              86 POP_TOP
# 
# 200          88 LOAD_FAST                1 (adapter)
#              90 LOAD_ATTR                7 (NULL|self + run_simulation)
#             110 BUILD_MAP                0
#             112 CALL                     1
#             120 STORE_FAST               2 (result)
# 
# 201         122 LOAD_FAST                2 (result)
#             124 LOAD_ATTR                8 (status)
#             144 STORE_FAST               3 (@py_assert1)
#             146 LOAD_GLOBAL             10 (SimulationStatus)
#             156 LOAD_ATTR               12 (COMPLETED)
#             176 STORE_FAST               4 (@py_assert5)
#             178 LOAD_FAST                3 (@py_assert1)
#             180 LOAD_FAST                4 (@py_assert5)
#             182 COMPARE_OP              40 (==)
#             186 STORE_FAST               5 (@py_assert3)
#             188 LOAD_FAST                5 (@py_assert3)
#             190 POP_JUMP_IF_TRUE       246 (to 684)
#             192 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             202 LOAD_ATTR               16 (_call_reprcompare)
#             222 LOAD_CONST               2 (('==',))
#             224 LOAD_FAST                5 (@py_assert3)
#             226 BUILD_TUPLE              1
#             228 LOAD_CONST               3 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.COMPLETED\n}',))
#             230 LOAD_FAST                3 (@py_assert1)
#             232 LOAD_FAST                4 (@py_assert5)
#             234 BUILD_TUPLE              2
#             236 CALL                     4
#             244 LOAD_CONST               4 ('result')
#             246 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             256 LOAD_ATTR               20 (locals)
#             276 CALL                     0
#             284 CONTAINS_OP              0
#             286 POP_JUMP_IF_TRUE        21 (to 330)
#             288 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             298 LOAD_ATTR               22 (_should_repr_global_name)
#             318 LOAD_FAST                2 (result)
#             320 CALL                     1
#             328 POP_JUMP_IF_FALSE       21 (to 372)
#         >>  330 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             340 LOAD_ATTR               24 (_saferepr)
#             360 LOAD_FAST                2 (result)
#             362 CALL                     1
#             370 JUMP_FORWARD             1 (to 374)
#         >>  372 LOAD_CONST               4 ('result')
#         >>  374 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             384 LOAD_ATTR               24 (_saferepr)
#             404 LOAD_FAST                3 (@py_assert1)
#             406 CALL                     1
#             414 LOAD_CONST               5 ('SimulationStatus')
#             416 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             426 LOAD_ATTR               20 (locals)
#             446 CALL                     0
#             454 CONTAINS_OP              0
#             456 POP_JUMP_IF_TRUE        25 (to 508)
#             458 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             468 LOAD_ATTR               22 (_should_repr_global_name)
#             488 LOAD_GLOBAL             10 (SimulationStatus)
#             498 CALL                     1
#             506 POP_JUMP_IF_FALSE       25 (to 558)
#         >>  508 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             518 LOAD_ATTR               24 (_saferepr)
#             538 LOAD_GLOBAL             10 (SimulationStatus)
#             548 CALL                     1
#             556 JUMP_FORWARD             1 (to 560)
#         >>  558 LOAD_CONST               5 ('SimulationStatus')
#         >>  560 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             570 LOAD_ATTR               24 (_saferepr)
#             590 LOAD_FAST                4 (@py_assert5)
#             592 CALL                     1
#             600 LOAD_CONST               6 (('py0', 'py2', 'py4', 'py6'))
#             602 BUILD_CONST_KEY_MAP      4
#             604 BINARY_OP                6 (%)
#             608 STORE_FAST               6 (@py_format7)
#             610 LOAD_CONST               7 ('assert %(py8)s')
#             612 LOAD_CONST               8 ('py8')
#             614 LOAD_FAST                6 (@py_format7)
#             616 BUILD_MAP                1
#             618 BINARY_OP                6 (%)
#             622 STORE_FAST               7 (@py_format9)
#             624 LOAD_GLOBAL             27 (NULL + AssertionError)
#             634 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             644 LOAD_ATTR               28 (_format_explanation)
#             664 LOAD_FAST                7 (@py_format9)
#             666 CALL                     1
#             674 CALL                     1
#             682 RAISE_VARARGS            1
#         >>  684 LOAD_CONST               0 (None)
#             686 COPY                     1
#             688 STORE_FAST               3 (@py_assert1)
#             690 COPY                     1
#             692 STORE_FAST               5 (@py_assert3)
#             694 STORE_FAST               4 (@py_assert5)
# 
# 202         696 LOAD_FAST                2 (result)
#             698 LOAD_ATTR               30 (data)
#             718 LOAD_CONST               9 ('buses')
#             720 BINARY_SUBSCR
#             724 STORE_FAST               3 (@py_assert1)
#             726 LOAD_GLOBAL             33 (NULL + len)
#             736 LOAD_FAST                3 (@py_assert1)
#             738 CALL                     1
#             746 STORE_FAST               5 (@py_assert3)
#             748 LOAD_CONST              10 (14)
#             750 STORE_FAST               8 (@py_assert6)
#             752 LOAD_FAST                5 (@py_assert3)
#             754 LOAD_FAST                8 (@py_assert6)
#             756 COMPARE_OP              40 (==)
#             760 STORE_FAST               4 (@py_assert5)
#             762 LOAD_FAST                4 (@py_assert5)
#             764 POP_JUMP_IF_TRUE       201 (to 1168)
#             766 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             776 LOAD_ATTR               16 (_call_reprcompare)
#             796 LOAD_CONST               2 (('==',))
#             798 LOAD_FAST                4 (@py_assert5)
#             800 BUILD_TUPLE              1
#             802 LOAD_CONST              11 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',))
#             804 LOAD_FAST                5 (@py_assert3)
#             806 LOAD_FAST                8 (@py_assert6)
#             808 BUILD_TUPLE              2
#             810 CALL                     4
#             818 LOAD_CONST              12 ('len')
#             820 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             830 LOAD_ATTR               20 (locals)
#             850 CALL                     0
#             858 CONTAINS_OP              0
#             860 POP_JUMP_IF_TRUE        25 (to 912)
#             862 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             872 LOAD_ATTR               22 (_should_repr_global_name)
#             892 LOAD_GLOBAL             32 (len)
#             902 CALL                     1
#             910 POP_JUMP_IF_FALSE       25 (to 962)
#         >>  912 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             922 LOAD_ATTR               24 (_saferepr)
#             942 LOAD_GLOBAL             32 (len)
#             952 CALL                     1
#             960 JUMP_FORWARD             1 (to 964)
#         >>  962 LOAD_CONST              12 ('len')
#         >>  964 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             974 LOAD_ATTR               24 (_saferepr)
#             994 LOAD_FAST                3 (@py_assert1)
#             996 CALL                     1
#            1004 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1014 LOAD_ATTR               24 (_saferepr)
#            1034 LOAD_FAST                5 (@py_assert3)
#            1036 CALL                     1
#            1044 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1054 LOAD_ATTR               24 (_saferepr)
#            1074 LOAD_FAST                8 (@py_assert6)
#            1076 CALL                     1
#            1084 LOAD_CONST              13 (('py0', 'py2', 'py4', 'py7'))
#            1086 BUILD_CONST_KEY_MAP      4
#            1088 BINARY_OP                6 (%)
#            1092 STORE_FAST               9 (@py_format8)
#            1094 LOAD_CONST              14 ('assert %(py9)s')
#            1096 LOAD_CONST              15 ('py9')
#            1098 LOAD_FAST                9 (@py_format8)
#            1100 BUILD_MAP                1
#            1102 BINARY_OP                6 (%)
#            1106 STORE_FAST              10 (@py_format10)
#            1108 LOAD_GLOBAL             27 (NULL + AssertionError)
#            1118 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1128 LOAD_ATTR               28 (_format_explanation)
#            1148 LOAD_FAST               10 (@py_format10)
#            1150 CALL                     1
#            1158 CALL                     1
#            1166 RAISE_VARARGS            1
#         >> 1168 LOAD_CONST               0 (None)
#            1170 COPY                     1
#            1172 STORE_FAST               3 (@py_assert1)
#            1174 COPY                     1
#            1176 STORE_FAST               5 (@py_assert3)
#            1178 COPY                     1
#            1180 STORE_FAST               4 (@py_assert5)
#            1182 STORE_FAST               8 (@py_assert6)
#            1184 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestPandapowerAdapterValidation at 0x73cd93b06970, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 205>:
# 205           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestPandapowerAdapterValidation')
#               8 STORE_NAME               2 (__qualname__)
# 
# 206          10 LOAD_CONST               1 (<code object test_no_input_fails_validation at 0x3afa2060, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 206>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_no_input_fails_validation)
# 
# 212          16 LOAD_CONST               2 (<code object test_invalid_case_name at 0x3af91d70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 212>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_invalid_case_name)
# 
# 218          22 LOAD_CONST               3 (<code object test_invalid_algorithm at 0x3aef7030, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 218>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_invalid_algorithm)
# 
# 224          28 LOAD_CONST               4 (<code object test_fast_decoupled_algorithm at 0x3afa5a90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 224>)
#              30 MAKE_FUNCTION            0
#              32 STORE_NAME               6 (test_fast_decoupled_algorithm)
#              34 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_no_input_fails_validation at 0x3afa2060, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 206>:
# 206           0 RESUME                   0
# 
# 207           2 LOAD_GLOBAL              1 (NULL + PandapowerPowerFlowAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
# 208          22 LOAD_FAST                1 (adapter)
#              24 LOAD_ATTR                3 (NULL|self + connect)
#              44 CALL                     0
#              52 POP_TOP
# 
# 209          54 LOAD_FAST                1 (adapter)
#              56 LOAD_ATTR                5 (NULL|self + run_simulation)
#              76 BUILD_MAP                0
#              78 CALL                     1
#              86 STORE_FAST               2 (result)
# 
# 210          88 LOAD_FAST                2 (result)
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
#             662 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_invalid_case_name at 0x3af91d70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 212>:
# 212           0 RESUME                   0
# 
# 213           2 LOAD_GLOBAL              1 (NULL + PandapowerPowerFlowAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
# 214          22 LOAD_FAST                1 (adapter)
#              24 LOAD_ATTR                3 (NULL|self + connect)
#              44 CALL                     0
#              52 POP_TOP
# 
# 215          54 LOAD_FAST                1 (adapter)
#              56 LOAD_ATTR                5 (NULL|self + run_simulation)
#              76 LOAD_CONST               1 ('case')
#              78 LOAD_CONST               2 ('case999')
#              80 BUILD_MAP                1
#              82 CALL                     1
#              90 STORE_FAST               2 (result)
# 
# 216          92 LOAD_FAST                2 (result)
#              94 LOAD_ATTR                6 (status)
#             114 STORE_FAST               3 (@py_assert1)
#             116 LOAD_GLOBAL              8 (SimulationStatus)
#             126 LOAD_ATTR               10 (FAILED)
#             146 STORE_FAST               4 (@py_assert5)
#             148 LOAD_FAST                3 (@py_assert1)
#             150 LOAD_FAST                4 (@py_assert5)
#             152 COMPARE_OP              40 (==)
#             156 STORE_FAST               5 (@py_assert3)
#             158 LOAD_FAST                5 (@py_assert3)
#             160 POP_JUMP_IF_TRUE       246 (to 654)
#             162 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             172 LOAD_ATTR               14 (_call_reprcompare)
#             192 LOAD_CONST               3 (('==',))
#             194 LOAD_FAST                5 (@py_assert3)
#             196 BUILD_TUPLE              1
#             198 LOAD_CONST               4 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.FAILED\n}',))
#             200 LOAD_FAST                3 (@py_assert1)
#             202 LOAD_FAST                4 (@py_assert5)
#             204 BUILD_TUPLE              2
#             206 CALL                     4
#             214 LOAD_CONST               5 ('result')
#             216 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             226 LOAD_ATTR               18 (locals)
#             246 CALL                     0
#             254 CONTAINS_OP              0
#             256 POP_JUMP_IF_TRUE        21 (to 300)
#             258 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             268 LOAD_ATTR               20 (_should_repr_global_name)
#             288 LOAD_FAST                2 (result)
#             290 CALL                     1
#             298 POP_JUMP_IF_FALSE       21 (to 342)
#         >>  300 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             310 LOAD_ATTR               22 (_saferepr)
#             330 LOAD_FAST                2 (result)
#             332 CALL                     1
#             340 JUMP_FORWARD             1 (to 344)
#         >>  342 LOAD_CONST               5 ('result')
#         >>  344 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             354 LOAD_ATTR               22 (_saferepr)
#             374 LOAD_FAST                3 (@py_assert1)
#             376 CALL                     1
#             384 LOAD_CONST               6 ('SimulationStatus')
#             386 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             396 LOAD_ATTR               18 (locals)
#             416 CALL                     0
#             424 CONTAINS_OP              0
#             426 POP_JUMP_IF_TRUE        25 (to 478)
#             428 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             438 LOAD_ATTR               20 (_should_repr_global_name)
#             458 LOAD_GLOBAL              8 (SimulationStatus)
#             468 CALL                     1
#             476 POP_JUMP_IF_FALSE       25 (to 528)
#         >>  478 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             488 LOAD_ATTR               22 (_saferepr)
#             508 LOAD_GLOBAL              8 (SimulationStatus)
#             518 CALL                     1
#             526 JUMP_FORWARD             1 (to 530)
#         >>  528 LOAD_CONST               6 ('SimulationStatus')
#         >>  530 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             540 LOAD_ATTR               22 (_saferepr)
#             560 LOAD_FAST                4 (@py_assert5)
#             562 CALL                     1
#             570 LOAD_CONST               7 (('py0', 'py2', 'py4', 'py6'))
#             572 BUILD_CONST_KEY_MAP      4
#             574 BINARY_OP                6 (%)
#             578 STORE_FAST               6 (@py_format7)
#             580 LOAD_CONST               8 ('assert %(py8)s')
#             582 LOAD_CONST               9 ('py8')
#             584 LOAD_FAST                6 (@py_format7)
#             586 BUILD_MAP                1
#             588 BINARY_OP                6 (%)
#             592 STORE_FAST               7 (@py_format9)
#             594 LOAD_GLOBAL             25 (NULL + AssertionError)
#             604 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             614 LOAD_ATTR               26 (_format_explanation)
#             634 LOAD_FAST                7 (@py_format9)
#             636 CALL                     1
#             644 CALL                     1
#             652 RAISE_VARARGS            1
#         >>  654 LOAD_CONST               0 (None)
#             656 COPY                     1
#             658 STORE_FAST               3 (@py_assert1)
#             660 COPY                     1
#             662 STORE_FAST               5 (@py_assert3)
#             664 STORE_FAST               4 (@py_assert5)
#             666 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_invalid_algorithm at 0x3aef7030, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 218>:
# 218           0 RESUME                   0
# 
# 219           2 LOAD_GLOBAL              1 (NULL + PandapowerPowerFlowAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
# 220          22 LOAD_FAST                1 (adapter)
#              24 LOAD_ATTR                3 (NULL|self + connect)
#              44 CALL                     0
#              52 POP_TOP
# 
# 221          54 LOAD_FAST                1 (adapter)
#              56 LOAD_ATTR                5 (NULL|self + run_simulation)
#              76 LOAD_CONST               1 ('case14')
#              78 LOAD_CONST               2 ('invalid')
#              80 LOAD_CONST               3 (('case', 'algorithm'))
#              82 BUILD_CONST_KEY_MAP      2
#              84 CALL                     1
#              92 STORE_FAST               2 (result)
# 
# 222          94 LOAD_FAST                2 (result)
#              96 LOAD_ATTR                6 (status)
#             116 STORE_FAST               3 (@py_assert1)
#             118 LOAD_GLOBAL              8 (SimulationStatus)
#             128 LOAD_ATTR               10 (FAILED)
#             148 STORE_FAST               4 (@py_assert5)
#             150 LOAD_FAST                3 (@py_assert1)
#             152 LOAD_FAST                4 (@py_assert5)
#             154 COMPARE_OP              40 (==)
#             158 STORE_FAST               5 (@py_assert3)
#             160 LOAD_FAST                5 (@py_assert3)
#             162 POP_JUMP_IF_TRUE       246 (to 656)
#             164 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             174 LOAD_ATTR               14 (_call_reprcompare)
#             194 LOAD_CONST               4 (('==',))
#             196 LOAD_FAST                5 (@py_assert3)
#             198 BUILD_TUPLE              1
#             200 LOAD_CONST               5 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.FAILED\n}',))
#             202 LOAD_FAST                3 (@py_assert1)
#             204 LOAD_FAST                4 (@py_assert5)
#             206 BUILD_TUPLE              2
#             208 CALL                     4
#             216 LOAD_CONST               6 ('result')
#             218 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             228 LOAD_ATTR               18 (locals)
#             248 CALL                     0
#             256 CONTAINS_OP              0
#             258 POP_JUMP_IF_TRUE        21 (to 302)
#             260 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             270 LOAD_ATTR               20 (_should_repr_global_name)
#             290 LOAD_FAST                2 (result)
#             292 CALL                     1
#             300 POP_JUMP_IF_FALSE       21 (to 344)
#         >>  302 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             312 LOAD_ATTR               22 (_saferepr)
#             332 LOAD_FAST                2 (result)
#             334 CALL                     1
#             342 JUMP_FORWARD             1 (to 346)
#         >>  344 LOAD_CONST               6 ('result')
#         >>  346 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             356 LOAD_ATTR               22 (_saferepr)
#             376 LOAD_FAST                3 (@py_assert1)
#             378 CALL                     1
#             386 LOAD_CONST               7 ('SimulationStatus')
#             388 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             398 LOAD_ATTR               18 (locals)
#             418 CALL                     0
#             426 CONTAINS_OP              0
#             428 POP_JUMP_IF_TRUE        25 (to 480)
#             430 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             440 LOAD_ATTR               20 (_should_repr_global_name)
#             460 LOAD_GLOBAL              8 (SimulationStatus)
#             470 CALL                     1
#             478 POP_JUMP_IF_FALSE       25 (to 530)
#         >>  480 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             490 LOAD_ATTR               22 (_saferepr)
#             510 LOAD_GLOBAL              8 (SimulationStatus)
#             520 CALL                     1
#             528 JUMP_FORWARD             1 (to 532)
#         >>  530 LOAD_CONST               7 ('SimulationStatus')
#         >>  532 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             542 LOAD_ATTR               22 (_saferepr)
#             562 LOAD_FAST                4 (@py_assert5)
#             564 CALL                     1
#             572 LOAD_CONST               8 (('py0', 'py2', 'py4', 'py6'))
#             574 BUILD_CONST_KEY_MAP      4
#             576 BINARY_OP                6 (%)
#             580 STORE_FAST               6 (@py_format7)
#             582 LOAD_CONST               9 ('assert %(py8)s')
#             584 LOAD_CONST              10 ('py8')
#             586 LOAD_FAST                6 (@py_format7)
#             588 BUILD_MAP                1
#             590 BINARY_OP                6 (%)
#             594 STORE_FAST               7 (@py_format9)
#             596 LOAD_GLOBAL             25 (NULL + AssertionError)
#             606 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             616 LOAD_ATTR               26 (_format_explanation)
#             636 LOAD_FAST                7 (@py_format9)
#             638 CALL                     1
#             646 CALL                     1
#             654 RAISE_VARARGS            1
#         >>  656 LOAD_CONST               0 (None)
#             658 COPY                     1
#             660 STORE_FAST               3 (@py_assert1)
#             662 COPY                     1
#             664 STORE_FAST               5 (@py_assert3)
#             666 STORE_FAST               4 (@py_assert5)
#             668 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_fast_decoupled_algorithm at 0x3afa5a90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 224>:
# 224           0 RESUME                   0
# 
# 225           2 LOAD_GLOBAL              1 (NULL + PandapowerPowerFlowAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
# 226          22 LOAD_FAST                1 (adapter)
#              24 LOAD_ATTR                3 (NULL|self + connect)
#              44 CALL                     0
#              52 POP_TOP
# 
# 227          54 LOAD_FAST                1 (adapter)
#              56 LOAD_ATTR                5 (NULL|self + run_simulation)
#              76 LOAD_CONST               1 ('case14')
#              78 LOAD_CONST               2 ('fdbx')
#              80 LOAD_CONST               3 (('case', 'algorithm'))
#              82 BUILD_CONST_KEY_MAP      2
#              84 CALL                     1
#              92 STORE_FAST               2 (result)
# 
# 228          94 LOAD_FAST                2 (result)
#              96 LOAD_ATTR                6 (status)
#             116 STORE_FAST               3 (@py_assert1)
#             118 LOAD_GLOBAL              8 (SimulationStatus)
#             128 LOAD_ATTR               10 (COMPLETED)
#             148 STORE_FAST               4 (@py_assert5)
#             150 LOAD_FAST                3 (@py_assert1)
#             152 LOAD_FAST                4 (@py_assert5)
#             154 COMPARE_OP              40 (==)
#             158 STORE_FAST               5 (@py_assert3)
#             160 LOAD_FAST                5 (@py_assert3)
#             162 POP_JUMP_IF_TRUE       246 (to 656)
#             164 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             174 LOAD_ATTR               14 (_call_reprcompare)
#             194 LOAD_CONST               4 (('==',))
#             196 LOAD_FAST                5 (@py_assert3)
#             198 BUILD_TUPLE              1
#             200 LOAD_CONST               5 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.COMPLETED\n}',))
#             202 LOAD_FAST                3 (@py_assert1)
#             204 LOAD_FAST                4 (@py_assert5)
#             206 BUILD_TUPLE              2
#             208 CALL                     4
#             216 LOAD_CONST               6 ('result')
#             218 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             228 LOAD_ATTR               18 (locals)
#             248 CALL                     0
#             256 CONTAINS_OP              0
#             258 POP_JUMP_IF_TRUE        21 (to 302)
#             260 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             270 LOAD_ATTR               20 (_should_repr_global_name)
#             290 LOAD_FAST                2 (result)
#             292 CALL                     1
#             300 POP_JUMP_IF_FALSE       21 (to 344)
#         >>  302 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             312 LOAD_ATTR               22 (_saferepr)
#             332 LOAD_FAST                2 (result)
#             334 CALL                     1
#             342 JUMP_FORWARD             1 (to 346)
#         >>  344 LOAD_CONST               6 ('result')
#         >>  346 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             356 LOAD_ATTR               22 (_saferepr)
#             376 LOAD_FAST                3 (@py_assert1)
#             378 CALL                     1
#             386 LOAD_CONST               7 ('SimulationStatus')
#             388 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             398 LOAD_ATTR               18 (locals)
#             418 CALL                     0
#             426 CONTAINS_OP              0
#             428 POP_JUMP_IF_TRUE        25 (to 480)
#             430 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             440 LOAD_ATTR               20 (_should_repr_global_name)
#             460 LOAD_GLOBAL              8 (SimulationStatus)
#             470 CALL                     1
#             478 POP_JUMP_IF_FALSE       25 (to 530)
#         >>  480 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             490 LOAD_ATTR               22 (_saferepr)
#             510 LOAD_GLOBAL              8 (SimulationStatus)
#             520 CALL                     1
#             528 JUMP_FORWARD             1 (to 532)
#         >>  530 LOAD_CONST               7 ('SimulationStatus')
#         >>  532 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             542 LOAD_ATTR               22 (_saferepr)
#             562 LOAD_FAST                4 (@py_assert5)
#             564 CALL                     1
#             572 LOAD_CONST               8 (('py0', 'py2', 'py4', 'py6'))
#             574 BUILD_CONST_KEY_MAP      4
#             576 BINARY_OP                6 (%)
#             580 STORE_FAST               6 (@py_format7)
#             582 LOAD_CONST               9 ('assert %(py8)s')
#             584 LOAD_CONST              10 ('py8')
#             586 LOAD_FAST                6 (@py_format7)
#             588 BUILD_MAP                1
#             590 BINARY_OP                6 (%)
#             594 STORE_FAST               7 (@py_format9)
#             596 LOAD_GLOBAL             25 (NULL + AssertionError)
#             606 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             616 LOAD_ATTR               26 (_format_explanation)
#             636 LOAD_FAST                7 (@py_format9)
#             638 CALL                     1
#             646 CALL                     1
#             654 RAISE_VARARGS            1
#         >>  656 LOAD_CONST               0 (None)
#             658 COPY                     1
#             660 STORE_FAST               3 (@py_assert1)
#             662 COPY                     1
#             664 STORE_FAST               5 (@py_assert3)
#             666 STORE_FAST               4 (@py_assert5)
# 
# 229         668 LOAD_FAST                2 (result)
#             670 LOAD_ATTR               28 (data)
#             690 LOAD_CONST              11 ('solver')
#             692 BINARY_SUBSCR
#             696 STORE_FAST               8 (@py_assert0)
#             698 LOAD_CONST               2 ('fdbx')
#             700 STORE_FAST               5 (@py_assert3)
#             702 LOAD_FAST                8 (@py_assert0)
#             704 LOAD_FAST                5 (@py_assert3)
#             706 COMPARE_OP              40 (==)
#             710 STORE_FAST               9 (@py_assert2)
#             712 LOAD_FAST                9 (@py_assert2)
#             714 POP_JUMP_IF_TRUE       108 (to 932)
#             716 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             726 LOAD_ATTR               14 (_call_reprcompare)
#             746 LOAD_CONST               4 (('==',))
#             748 LOAD_FAST                9 (@py_assert2)
#             750 BUILD_TUPLE              1
#             752 LOAD_CONST              12 (('%(py1)s == %(py4)s',))
#             754 LOAD_FAST                8 (@py_assert0)
#             756 LOAD_FAST                5 (@py_assert3)
#             758 BUILD_TUPLE              2
#             760 CALL                     4
#             768 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             778 LOAD_ATTR               22 (_saferepr)
#             798 LOAD_FAST                8 (@py_assert0)
#             800 CALL                     1
#             808 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             818 LOAD_ATTR               22 (_saferepr)
#             838 LOAD_FAST                5 (@py_assert3)
#             840 CALL                     1
#             848 LOAD_CONST              13 (('py1', 'py4'))
#             850 BUILD_CONST_KEY_MAP      2
#             852 BINARY_OP                6 (%)
#             856 STORE_FAST              10 (@py_format5)
#             858 LOAD_CONST              14 ('assert %(py6)s')
#             860 LOAD_CONST              15 ('py6')
#             862 LOAD_FAST               10 (@py_format5)
#             864 BUILD_MAP                1
#             866 BINARY_OP                6 (%)
#             870 STORE_FAST               6 (@py_format7)
#             872 LOAD_GLOBAL             25 (NULL + AssertionError)
#             882 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             892 LOAD_ATTR               26 (_format_explanation)
#             912 LOAD_FAST                6 (@py_format7)
#             914 CALL                     1
#             922 CALL                     1
#             930 RAISE_VARARGS            1
#         >>  932 LOAD_CONST               0 (None)
#             934 COPY                     1
#             936 STORE_FAST               8 (@py_assert0)
#             938 COPY                     1
#             940 STORE_FAST               9 (@py_assert2)
#             942 STORE_FAST               5 (@py_assert3)
#             944 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestPandapowerAdapterViaFactory at 0x73cd93b063d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 232>:
# 232           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestPandapowerAdapterViaFactory')
#               8 STORE_NAME               2 (__qualname__)
# 
# 233          10 LOAD_CONST               1 ('Test the adapter through the Engine + PowerFlow pipeline.')
#              12 STORE_NAME               3 (__doc__)
# 
# 235          14 LOAD_CONST               2 (<code object test_factory_creates_pandapower_api at 0x3af12be0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 235>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_factory_creates_pandapower_api)
# 
# 241          20 LOAD_CONST               3 (<code object test_factory_lists_pandapower at 0x3ae730b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 241>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_factory_lists_pandapower)
# 
# 247          26 LOAD_CONST               4 (<code object test_full_pipeline_case14 at 0x3afa9f80, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 247>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_full_pipeline_case14)
#              32 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_factory_creates_pandapower_api at 0x3af12be0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 235>:
# 235           0 RESUME                   0
# 
# 236           2 LOAD_CONST               1 (0)
#               4 LOAD_CONST               2 (('Engine',))
#               6 IMPORT_NAME              0 (cloudpss_skills_v2.powerskill.engine)
#               8 IMPORT_FROM              1 (Engine)
#              10 STORE_FAST               1 (Engine)
#              12 POP_TOP
# 
# 238          14 LOAD_FAST                1 (Engine)
#              16 LOAD_ATTR                5 (NULL|self + create_powerflow_api)
#              36 LOAD_CONST               3 ('pandapower')
#              38 KW_NAMES                 4 (('engine',))
#              40 CALL                     1
#              48 STORE_FAST               2 (api)
# 
# 239          50 LOAD_CONST               0 (None)
#              52 STORE_FAST               3 (@py_assert2)
#              54 LOAD_FAST                2 (api)
#              56 LOAD_FAST                3 (@py_assert2)
#              58 IS_OP                    1
#              60 STORE_FAST               4 (@py_assert1)
#              62 LOAD_FAST                4 (@py_assert1)
#              64 POP_JUMP_IF_TRUE       153 (to 372)
#              66 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#              76 LOAD_ATTR                8 (_call_reprcompare)
#              96 LOAD_CONST               5 (('is not',))
#              98 LOAD_FAST                4 (@py_assert1)
#             100 BUILD_TUPLE              1
#             102 LOAD_CONST               6 (('%(py0)s is not %(py3)s',))
#             104 LOAD_FAST                2 (api)
#             106 LOAD_FAST                3 (@py_assert2)
#             108 BUILD_TUPLE              2
#             110 CALL                     4
#             118 LOAD_CONST               7 ('api')
#             120 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             130 LOAD_ATTR               12 (locals)
#             150 CALL                     0
#             158 CONTAINS_OP              0
#             160 POP_JUMP_IF_TRUE        21 (to 204)
#             162 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             172 LOAD_ATTR               14 (_should_repr_global_name)
#             192 LOAD_FAST                2 (api)
#             194 CALL                     1
#             202 POP_JUMP_IF_FALSE       21 (to 246)
#         >>  204 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             214 LOAD_ATTR               16 (_saferepr)
#             234 LOAD_FAST                2 (api)
#             236 CALL                     1
#             244 JUMP_FORWARD             1 (to 248)
#         >>  246 LOAD_CONST               7 ('api')
#         >>  248 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             258 LOAD_ATTR               16 (_saferepr)
#             278 LOAD_FAST                3 (@py_assert2)
#             280 CALL                     1
#             288 LOAD_CONST               8 (('py0', 'py3'))
#             290 BUILD_CONST_KEY_MAP      2
#             292 BINARY_OP                6 (%)
#             296 STORE_FAST               5 (@py_format4)
#             298 LOAD_CONST               9 ('assert %(py5)s')
#             300 LOAD_CONST              10 ('py5')
#             302 LOAD_FAST                5 (@py_format4)
#             304 BUILD_MAP                1
#             306 BINARY_OP                6 (%)
#             310 STORE_FAST               6 (@py_format6)
#             312 LOAD_GLOBAL             19 (NULL + AssertionError)
#             322 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             332 LOAD_ATTR               20 (_format_explanation)
#             352 LOAD_FAST                6 (@py_format6)
#             354 CALL                     1
#             362 CALL                     1
#             370 RAISE_VARARGS            1
#         >>  372 LOAD_CONST               0 (None)
#             374 COPY                     1
#             376 STORE_FAST               4 (@py_assert1)
#             378 STORE_FAST               3 (@py_assert2)
#             380 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_factory_lists_pandapower at 0x3ae730b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 241>:
# 241           0 RESUME                   0
# 
# 242           2 LOAD_CONST               1 (0)
#               4 LOAD_CONST               2 (('Engine',))
#               6 IMPORT_NAME              0 (cloudpss_skills_v2.powerskill.engine)
#               8 IMPORT_FROM              1 (Engine)
#              10 STORE_FAST               1 (Engine)
#              12 POP_TOP
# 
# 244          14 LOAD_FAST                1 (Engine)
#              16 LOAD_ATTR                5 (NULL|self + list_engines)
#              36 LOAD_CONST               3 ('power_flow')
#              38 CALL                     1
#              46 STORE_FAST               2 (engines)
# 
# 245          48 LOAD_CONST               4 ('pandapower')
#              50 STORE_FAST               3 (@py_assert0)
#              52 LOAD_FAST                3 (@py_assert0)
#              54 LOAD_FAST                2 (engines)
#              56 CONTAINS_OP              0
#              58 STORE_FAST               4 (@py_assert2)
#              60 LOAD_FAST                4 (@py_assert2)
#              62 POP_JUMP_IF_TRUE       153 (to 370)
#              64 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#              74 LOAD_ATTR                8 (_call_reprcompare)
#              94 LOAD_CONST               5 (('in',))
#              96 LOAD_FAST                4 (@py_assert2)
#              98 BUILD_TUPLE              1
#             100 LOAD_CONST               6 (('%(py1)s in %(py3)s',))
#             102 LOAD_FAST                3 (@py_assert0)
#             104 LOAD_FAST                2 (engines)
#             106 BUILD_TUPLE              2
#             108 CALL                     4
#             116 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             126 LOAD_ATTR               10 (_saferepr)
#             146 LOAD_FAST                3 (@py_assert0)
#             148 CALL                     1
#             156 LOAD_CONST               7 ('engines')
#             158 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             168 LOAD_ATTR               14 (locals)
#             188 CALL                     0
#             196 CONTAINS_OP              0
#             198 POP_JUMP_IF_TRUE        21 (to 242)
#             200 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             210 LOAD_ATTR               16 (_should_repr_global_name)
#             230 LOAD_FAST                2 (engines)
#             232 CALL                     1
#             240 POP_JUMP_IF_FALSE       21 (to 284)
#         >>  242 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             252 LOAD_ATTR               10 (_saferepr)
#             272 LOAD_FAST                2 (engines)
#             274 CALL                     1
#             282 JUMP_FORWARD             1 (to 286)
#         >>  284 LOAD_CONST               7 ('engines')
#         >>  286 LOAD_CONST               8 (('py1', 'py3'))
#             288 BUILD_CONST_KEY_MAP      2
#             290 BINARY_OP                6 (%)
#             294 STORE_FAST               5 (@py_format4)
#             296 LOAD_CONST               9 ('assert %(py5)s')
#             298 LOAD_CONST              10 ('py5')
#             300 LOAD_FAST                5 (@py_format4)
#             302 BUILD_MAP                1
#             304 BINARY_OP                6 (%)
#             308 STORE_FAST               6 (@py_format6)
#             310 LOAD_GLOBAL             19 (NULL + AssertionError)
#             320 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             330 LOAD_ATTR               20 (_format_explanation)
#             350 LOAD_FAST                6 (@py_format6)
#             352 CALL                     1
#             360 CALL                     1
#             368 RAISE_VARARGS            1
#         >>  370 LOAD_CONST               0 (None)
#             372 COPY                     1
#             374 STORE_FAST               3 (@py_assert0)
#             376 STORE_FAST               4 (@py_assert2)
#             378 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_full_pipeline_case14 at 0x3afa9f80, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py", line 247>:
# 247           0 RESUME                   0
# 
# 248           2 LOAD_CONST               1 (0)
#               4 LOAD_CONST               2 (('Engine',))
#               6 IMPORT_NAME              0 (cloudpss_skills_v2.powerskill.engine)
#               8 IMPORT_FROM              1 (Engine)
#              10 STORE_FAST               1 (Engine)
#              12 POP_TOP
# 
# 250          14 LOAD_FAST                1 (Engine)
#              16 LOAD_ATTR                5 (NULL|self + create_powerflow_api)
#              36 LOAD_CONST               3 ('pandapower')
#              38 KW_NAMES                 4 (('engine',))
#              40 CALL                     1
#              48 STORE_FAST               2 (api)
# 
# 251          50 LOAD_FAST                2 (api)
#              52 LOAD_ATTR                6 (_adapter)
#              72 STORE_FAST               3 (adapter)
# 
# 252          74 LOAD_FAST                3 (adapter)
#              76 LOAD_ATTR                9 (NULL|self + connect)
#              96 CALL                     0
#             104 POP_TOP
# 
# 253         106 LOAD_FAST                3 (adapter)
#             108 LOAD_ATTR               11 (NULL|self + run_simulation)
#             128 LOAD_CONST               5 ('case')
#             130 LOAD_CONST               6 ('case14')
#             132 BUILD_MAP                1
#             134 CALL                     1
#             142 STORE_FAST               4 (result)
# 
# 255         144 LOAD_FAST                2 (api)
#             146 LOAD_ATTR               13 (NULL|self + get_typed_buses)
#             166 LOAD_FAST                4 (result)
#             168 CALL                     1
#             176 STORE_FAST               5 (buses)
# 
# 256         178 LOAD_FAST                2 (api)
#             180 LOAD_ATTR               15 (NULL|self + get_typed_branches)
#             200 LOAD_FAST                4 (result)
#             202 CALL                     1
#             210 STORE_FAST               6 (branches)
# 
# 257         212 LOAD_FAST                2 (api)
#             214 LOAD_ATTR               17 (NULL|self + get_network_summary)
#             234 LOAD_FAST                4 (result)
#             236 CALL                     1
#             244 STORE_FAST               7 (summary)
# 
# 259         246 LOAD_GLOBAL             19 (NULL + len)
#             256 LOAD_FAST                5 (buses)
#             258 CALL                     1
#             266 STORE_FAST               8 (@py_assert2)
#             268 LOAD_CONST               7 (14)
#             270 STORE_FAST               9 (@py_assert5)
#             272 LOAD_FAST                8 (@py_assert2)
#             274 LOAD_FAST                9 (@py_assert5)
#             276 COMPARE_OP              40 (==)
#             280 STORE_FAST              10 (@py_assert4)
#             282 LOAD_FAST               10 (@py_assert4)
#             284 POP_JUMP_IF_TRUE       246 (to 778)
#             286 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             296 LOAD_ATTR               22 (_call_reprcompare)
#             316 LOAD_CONST               8 (('==',))
#             318 LOAD_FAST               10 (@py_assert4)
#             320 BUILD_TUPLE              1
#             322 LOAD_CONST               9 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             324 LOAD_FAST                8 (@py_assert2)
#             326 LOAD_FAST                9 (@py_assert5)
#             328 BUILD_TUPLE              2
#             330 CALL                     4
#             338 LOAD_CONST              10 ('len')
#             340 LOAD_GLOBAL             25 (NULL + @py_builtins)
#             350 LOAD_ATTR               26 (locals)
#             370 CALL                     0
#             378 CONTAINS_OP              0
#             380 POP_JUMP_IF_TRUE        25 (to 432)
#             382 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             392 LOAD_ATTR               28 (_should_repr_global_name)
#             412 LOAD_GLOBAL             18 (len)
#             422 CALL                     1
#             430 POP_JUMP_IF_FALSE       25 (to 482)
#         >>  432 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             442 LOAD_ATTR               30 (_saferepr)
#             462 LOAD_GLOBAL             18 (len)
#             472 CALL                     1
#             480 JUMP_FORWARD             1 (to 484)
#         >>  482 LOAD_CONST              10 ('len')
#         >>  484 LOAD_CONST              11 ('buses')
#             486 LOAD_GLOBAL             25 (NULL + @py_builtins)
#             496 LOAD_ATTR               26 (locals)
#             516 CALL                     0
#             524 CONTAINS_OP              0
#             526 POP_JUMP_IF_TRUE        21 (to 570)
#             528 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             538 LOAD_ATTR               28 (_should_repr_global_name)
#             558 LOAD_FAST                5 (buses)
#             560 CALL                     1
#             568 POP_JUMP_IF_FALSE       21 (to 612)
#         >>  570 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             580 LOAD_ATTR               30 (_saferepr)
#             600 LOAD_FAST                5 (buses)
#             602 CALL                     1
#             610 JUMP_FORWARD             1 (to 614)
#         >>  612 LOAD_CONST              11 ('buses')
#         >>  614 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             624 LOAD_ATTR               30 (_saferepr)
#             644 LOAD_FAST                8 (@py_assert2)
#             646 CALL                     1
#             654 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             664 LOAD_ATTR               30 (_saferepr)
#             684 LOAD_FAST                9 (@py_assert5)
#             686 CALL                     1
#             694 LOAD_CONST              12 (('py0', 'py1', 'py3', 'py6'))
#             696 BUILD_CONST_KEY_MAP      4
#             698 BINARY_OP                6 (%)
#             702 STORE_FAST              11 (@py_format7)
#             704 LOAD_CONST              13 ('assert %(py8)s')
#             706 LOAD_CONST              14 ('py8')
#             708 LOAD_FAST               11 (@py_format7)
#             710 BUILD_MAP                1
#             712 BINARY_OP                6 (%)
#             716 STORE_FAST              12 (@py_format9)
#             718 LOAD_GLOBAL             33 (NULL + AssertionError)
#             728 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             738 LOAD_ATTR               34 (_format_explanation)
#             758 LOAD_FAST               12 (@py_format9)
#             760 CALL                     1
#             768 CALL                     1
#             776 RAISE_VARARGS            1
#         >>  778 LOAD_CONST               0 (None)
#             780 COPY                     1
#             782 STORE_FAST               8 (@py_assert2)
#             784 COPY                     1
#             786 STORE_FAST              10 (@py_assert4)
#             788 STORE_FAST               9 (@py_assert5)
# 
# 260         790 LOAD_GLOBAL             19 (NULL + len)
#             800 LOAD_FAST                6 (branches)
#             802 CALL                     1
#             810 STORE_FAST               8 (@py_assert2)
#             812 LOAD_CONST              15 (20)
#             814 STORE_FAST               9 (@py_assert5)
#             816 LOAD_FAST                8 (@py_assert2)
#             818 LOAD_FAST                9 (@py_assert5)
#             820 COMPARE_OP              40 (==)
#             824 STORE_FAST              10 (@py_assert4)
#             826 LOAD_FAST               10 (@py_assert4)
#             828 POP_JUMP_IF_TRUE       246 (to 1322)
#             830 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             840 LOAD_ATTR               22 (_call_reprcompare)
#             860 LOAD_CONST               8 (('==',))
#             862 LOAD_FAST               10 (@py_assert4)
#             864 BUILD_TUPLE              1
#             866 LOAD_CONST               9 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             868 LOAD_FAST                8 (@py_assert2)
#             870 LOAD_FAST                9 (@py_assert5)
#             872 BUILD_TUPLE              2
#             874 CALL                     4
#             882 LOAD_CONST              10 ('len')
#             884 LOAD_GLOBAL             25 (NULL + @py_builtins)
#             894 LOAD_ATTR               26 (locals)
#             914 CALL                     0
#             922 CONTAINS_OP              0
#             924 POP_JUMP_IF_TRUE        25 (to 976)
#             926 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             936 LOAD_ATTR               28 (_should_repr_global_name)
#             956 LOAD_GLOBAL             18 (len)
#             966 CALL                     1
#             974 POP_JUMP_IF_FALSE       25 (to 1026)
#         >>  976 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             986 LOAD_ATTR               30 (_saferepr)
#            1006 LOAD_GLOBAL             18 (len)
#            1016 CALL                     1
#            1024 JUMP_FORWARD             1 (to 1028)
#         >> 1026 LOAD_CONST              10 ('len')
#         >> 1028 LOAD_CONST              16 ('branches')
#            1030 LOAD_GLOBAL             25 (NULL + @py_builtins)
#            1040 LOAD_ATTR               26 (locals)
#            1060 CALL                     0
#            1068 CONTAINS_OP              0
#            1070 POP_JUMP_IF_TRUE        21 (to 1114)
#            1072 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1082 LOAD_ATTR               28 (_should_repr_global_name)
#            1102 LOAD_FAST                6 (branches)
#            1104 CALL                     1
#            1112 POP_JUMP_IF_FALSE       21 (to 1156)
#         >> 1114 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1124 LOAD_ATTR               30 (_saferepr)
#            1144 LOAD_FAST                6 (branches)
#            1146 CALL                     1
#            1154 JUMP_FORWARD             1 (to 1158)
#         >> 1156 LOAD_CONST              16 ('branches')
#         >> 1158 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1168 LOAD_ATTR               30 (_saferepr)
#            1188 LOAD_FAST                8 (@py_assert2)
#            1190 CALL                     1
#            1198 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1208 LOAD_ATTR               30 (_saferepr)
#            1228 LOAD_FAST                9 (@py_assert5)
#            1230 CALL                     1
#            1238 LOAD_CONST              12 (('py0', 'py1', 'py3', 'py6'))
#            1240 BUILD_CONST_KEY_MAP      4
#            1242 BINARY_OP                6 (%)
#            1246 STORE_FAST              11 (@py_format7)
#            1248 LOAD_CONST              13 ('assert %(py8)s')
#            1250 LOAD_CONST              14 ('py8')
#            1252 LOAD_FAST               11 (@py_format7)
#            1254 BUILD_MAP                1
#            1256 BINARY_OP                6 (%)
#            1260 STORE_FAST              12 (@py_format9)
#            1262 LOAD_GLOBAL             33 (NULL + AssertionError)
#            1272 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1282 LOAD_ATTR               34 (_format_explanation)
#            1302 LOAD_FAST               12 (@py_format9)
#            1304 CALL                     1
#            1312 CALL                     1
#            1320 RAISE_VARARGS            1
#         >> 1322 LOAD_CONST               0 (None)
#            1324 COPY                     1
#            1326 STORE_FAST               8 (@py_assert2)
#            1328 COPY                     1
#            1330 STORE_FAST              10 (@py_assert4)
#            1332 STORE_FAST               9 (@py_assert5)
# 
# 261        1334 LOAD_CONST               0 (None)
#            1336 STORE_FAST               8 (@py_assert2)
#            1338 LOAD_FAST                7 (summary)
#            1340 LOAD_FAST                8 (@py_assert2)
#            1342 IS_OP                    1
#            1344 STORE_FAST              13 (@py_assert1)
#            1346 LOAD_FAST               13 (@py_assert1)
#            1348 POP_JUMP_IF_TRUE       153 (to 1656)
#            1350 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1360 LOAD_ATTR               22 (_call_reprcompare)
#            1380 LOAD_CONST              17 (('is not',))
#            1382 LOAD_FAST               13 (@py_assert1)
#            1384 BUILD_TUPLE              1
#            1386 LOAD_CONST              18 (('%(py0)s is not %(py3)s',))
#            1388 LOAD_FAST                7 (summary)
#            1390 LOAD_FAST                8 (@py_assert2)
#            1392 BUILD_TUPLE              2
#            1394 CALL                     4
#            1402 LOAD_CONST              19 ('summary')
#            1404 LOAD_GLOBAL             25 (NULL + @py_builtins)
#            1414 LOAD_ATTR               26 (locals)
#            1434 CALL                     0
#            1442 CONTAINS_OP              0
#            1444 POP_JUMP_IF_TRUE        21 (to 1488)
#            1446 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1456 LOAD_ATTR               28 (_should_repr_global_name)
#            1476 LOAD_FAST                7 (summary)
#            1478 CALL                     1
#            1486 POP_JUMP_IF_FALSE       21 (to 1530)
#         >> 1488 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1498 LOAD_ATTR               30 (_saferepr)
#            1518 LOAD_FAST                7 (summary)
#            1520 CALL                     1
#            1528 JUMP_FORWARD             1 (to 1532)
#         >> 1530 LOAD_CONST              19 ('summary')
#         >> 1532 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1542 LOAD_ATTR               30 (_saferepr)
#            1562 LOAD_FAST                8 (@py_assert2)
#            1564 CALL                     1
#            1572 LOAD_CONST              20 (('py0', 'py3'))
#            1574 BUILD_CONST_KEY_MAP      2
#            1576 BINARY_OP                6 (%)
#            1580 STORE_FAST              14 (@py_format4)
#            1582 LOAD_CONST              21 ('assert %(py5)s')
#            1584 LOAD_CONST              22 ('py5')
#            1586 LOAD_FAST               14 (@py_format4)
#            1588 BUILD_MAP                1
#            1590 BINARY_OP                6 (%)
#            1594 STORE_FAST              15 (@py_format6)
#            1596 LOAD_GLOBAL             33 (NULL + AssertionError)
#            1606 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1616 LOAD_ATTR               34 (_format_explanation)
#            1636 LOAD_FAST               15 (@py_format6)
#            1638 CALL                     1
#            1646 CALL                     1
#            1654 RAISE_VARARGS            1
#         >> 1656 LOAD_CONST               0 (None)
#            1658 COPY                     1
#            1660 STORE_FAST              13 (@py_assert1)
#            1662 STORE_FAST               8 (@py_assert2)
# 
# 262        1664 LOAD_FAST                7 (summary)
#            1666 LOAD_ATTR               36 (converged)
#            1686 STORE_FAST              13 (@py_assert1)
#            1688 LOAD_CONST              23 (True)
#            1690 STORE_FAST              10 (@py_assert4)
#            1692 LOAD_FAST               13 (@py_assert1)
#            1694 LOAD_FAST               10 (@py_assert4)
#            1696 IS_OP                    0
#            1698 STORE_FAST              16 (@py_assert3)
#            1700 LOAD_FAST               16 (@py_assert3)
#            1702 POP_JUMP_IF_TRUE       173 (to 2050)
#            1704 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1714 LOAD_ATTR               22 (_call_reprcompare)
#            1734 LOAD_CONST              24 (('is',))
#            1736 LOAD_FAST               16 (@py_assert3)
#            1738 BUILD_TUPLE              1
#            1740 LOAD_CONST              25 (('%(py2)s\n{%(py2)s = %(py0)s.converged\n} is %(py5)s',))
#            1742 LOAD_FAST               13 (@py_assert1)
#            1744 LOAD_FAST               10 (@py_assert4)
#            1746 BUILD_TUPLE              2
#            1748 CALL                     4
#            1756 LOAD_CONST              19 ('summary')
#            1758 LOAD_GLOBAL             25 (NULL + @py_builtins)
#            1768 LOAD_ATTR               26 (locals)
#            1788 CALL                     0
#            1796 CONTAINS_OP              0
#            1798 POP_JUMP_IF_TRUE        21 (to 1842)
#            1800 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1810 LOAD_ATTR               28 (_should_repr_global_name)
#            1830 LOAD_FAST                7 (summary)
#            1832 CALL                     1
#            1840 POP_JUMP_IF_FALSE       21 (to 1884)
#         >> 1842 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1852 LOAD_ATTR               30 (_saferepr)
#            1872 LOAD_FAST                7 (summary)
#            1874 CALL                     1
#            1882 JUMP_FORWARD             1 (to 1886)
#         >> 1884 LOAD_CONST              19 ('summary')
#         >> 1886 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1896 LOAD_ATTR               30 (_saferepr)
#            1916 LOAD_FAST               13 (@py_assert1)
#            1918 CALL                     1
#            1926 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1936 LOAD_ATTR               30 (_saferepr)
#            1956 LOAD_FAST               10 (@py_assert4)
#            1958 CALL                     1
#            1966 LOAD_CONST              26 (('py0', 'py2', 'py5'))
#            1968 BUILD_CONST_KEY_MAP      3
#            1970 BINARY_OP                6 (%)
#            1974 STORE_FAST              15 (@py_format6)
#            1976 LOAD_CONST              27 ('assert %(py7)s')
#            1978 LOAD_CONST              28 ('py7')
#            1980 LOAD_FAST               15 (@py_format6)
#            1982 BUILD_MAP                1
#            1984 BINARY_OP                6 (%)
#            1988 STORE_FAST              17 (@py_format8)
#            1990 LOAD_GLOBAL             33 (NULL + AssertionError)
#            2000 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            2010 LOAD_ATTR               34 (_format_explanation)
#            2030 LOAD_FAST               17 (@py_format8)
#            2032 CALL                     1
#            2040 CALL                     1
#            2048 RAISE_VARARGS            1
#         >> 2050 LOAD_CONST               0 (None)
#            2052 COPY                     1
#            2054 STORE_FAST              13 (@py_assert1)
#            2056 COPY                     1
#            2058 STORE_FAST              16 (@py_assert3)
#            2060 STORE_FAST              10 (@py_assert4)
# 
# 263        2062 LOAD_FAST                7 (summary)
#            2064 LOAD_ATTR               38 (bus_count)
#            2084 STORE_FAST              13 (@py_assert1)
#            2086 LOAD_CONST               7 (14)
#            2088 STORE_FAST              10 (@py_assert4)
#            2090 LOAD_FAST               13 (@py_assert1)
#            2092 LOAD_FAST               10 (@py_assert4)
#            2094 COMPARE_OP              40 (==)
#            2098 STORE_FAST              16 (@py_assert3)
#            2100 LOAD_FAST               16 (@py_assert3)
#            2102 POP_JUMP_IF_TRUE       173 (to 2450)
#            2104 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            2114 LOAD_ATTR               22 (_call_reprcompare)
#            2134 LOAD_CONST               8 (('==',))
#            2136 LOAD_FAST               16 (@py_assert3)
#            2138 BUILD_TUPLE              1
#            2140 LOAD_CONST              29 (('%(py2)s\n{%(py2)s = %(py0)s.bus_count\n} == %(py5)s',))
#            2142 LOAD_FAST               13 (@py_assert1)
#            2144 LOAD_FAST               10 (@py_assert4)
#            2146 BUILD_TUPLE              2
#            2148 CALL                     4
#            2156 LOAD_CONST              19 ('summary')
#            2158 LOAD_GLOBAL             25 (NULL + @py_builtins)
#            2168 LOAD_ATTR               26 (locals)
#            2188 CALL                     0
#            2196 CONTAINS_OP              0
#            2198 POP_JUMP_IF_TRUE        21 (to 2242)
#            2200 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            2210 LOAD_ATTR               28 (_should_repr_global_name)
#            2230 LOAD_FAST                7 (summary)
#            2232 CALL                     1
#            2240 POP_JUMP_IF_FALSE       21 (to 2284)
#         >> 2242 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            2252 LOAD_ATTR               30 (_saferepr)
#            2272 LOAD_FAST                7 (summary)
#            2274 CALL                     1
#            2282 JUMP_FORWARD             1 (to 2286)
#         >> 2284 LOAD_CONST              19 ('summary')
#         >> 2286 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            2296 LOAD_ATTR               30 (_saferepr)
#            2316 LOAD_FAST               13 (@py_assert1)
#            2318 CALL                     1
#            2326 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            2336 LOAD_ATTR               30 (_saferepr)
#            2356 LOAD_FAST               10 (@py_assert4)
#            2358 CALL                     1
#            2366 LOAD_CONST              26 (('py0', 'py2', 'py5'))
#            2368 BUILD_CONST_KEY_MAP      3
#            2370 BINARY_OP                6 (%)
#            2374 STORE_FAST              15 (@py_format6)
#            2376 LOAD_CONST              27 ('assert %(py7)s')
#            2378 LOAD_CONST              28 ('py7')
#            2380 LOAD_FAST               15 (@py_format6)
#            2382 BUILD_MAP                1
#            2384 BINARY_OP                6 (%)
#            2388 STORE_FAST              17 (@py_format8)
#            2390 LOAD_GLOBAL             33 (NULL + AssertionError)
#            2400 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            2410 LOAD_ATTR               34 (_format_explanation)
#            2430 LOAD_FAST               17 (@py_format8)
#            2432 CALL                     1
#            2440 CALL                     1
#            2448 RAISE_VARARGS            1
#         >> 2450 LOAD_CONST               0 (None)
#            2452 COPY                     1
#            2454 STORE_FAST              13 (@py_assert1)
#            2456 COPY                     1
#            2458 STORE_FAST              16 (@py_assert3)
#            2460 STORE_FAST              10 (@py_assert4)
# 
# 264        2462 LOAD_FAST                7 (summary)
#            2464 LOAD_ATTR               40 (total_loss_mw)
#            2484 STORE_FAST              13 (@py_assert1)
#            2486 LOAD_CONST               1 (0)
#            2488 STORE_FAST              10 (@py_assert4)
#            2490 LOAD_FAST               13 (@py_assert1)
#            2492 LOAD_FAST               10 (@py_assert4)
#            2494 COMPARE_OP              68 (>)
#            2498 STORE_FAST              16 (@py_assert3)
#            2500 LOAD_FAST               16 (@py_assert3)
#            2502 POP_JUMP_IF_TRUE       173 (to 2850)
#            2504 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            2514 LOAD_ATTR               22 (_call_reprcompare)
#            2534 LOAD_CONST              30 (('>',))
#            2536 LOAD_FAST               16 (@py_assert3)
#            2538 BUILD_TUPLE              1
#            2540 LOAD_CONST              31 (('%(py2)s\n{%(py2)s = %(py0)s.total_loss_mw\n} > %(py5)s',))
#            2542 LOAD_FAST               13 (@py_assert1)
#            2544 LOAD_FAST               10 (@py_assert4)
#            2546 BUILD_TUPLE              2
#            2548 CALL                     4
#            2556 LOAD_CONST              19 ('summary')
#            2558 LOAD_GLOBAL             25 (NULL + @py_builtins)
#            2568 LOAD_ATTR               26 (locals)
#            2588 CALL                     0
#            2596 CONTAINS_OP              0
#            2598 POP_JUMP_IF_TRUE        21 (to 2642)
#            2600 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            2610 LOAD_ATTR               28 (_should_repr_global_name)
#            2630 LOAD_FAST                7 (summary)
#            2632 CALL                     1
#            2640 POP_JUMP_IF_FALSE       21 (to 2684)
#         >> 2642 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            2652 LOAD_ATTR               30 (_saferepr)
#            2672 LOAD_FAST                7 (summary)
#            2674 CALL                     1
#            2682 JUMP_FORWARD             1 (to 2686)
#         >> 2684 LOAD_CONST              19 ('summary')
#         >> 2686 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            2696 LOAD_ATTR               30 (_saferepr)
#            2716 LOAD_FAST               13 (@py_assert1)
#            2718 CALL                     1
#            2726 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            2736 LOAD_ATTR               30 (_saferepr)
#            2756 LOAD_FAST               10 (@py_assert4)
#            2758 CALL                     1
#            2766 LOAD_CONST              26 (('py0', 'py2', 'py5'))
#            2768 BUILD_CONST_KEY_MAP      3
#            2770 BINARY_OP                6 (%)
#            2774 STORE_FAST              15 (@py_format6)
#            2776 LOAD_CONST              27 ('assert %(py7)s')
#            2778 LOAD_CONST              28 ('py7')
#            2780 LOAD_FAST               15 (@py_format6)
#            2782 BUILD_MAP                1
#            2784 BINARY_OP                6 (%)
#            2788 STORE_FAST              17 (@py_format8)
#            2790 LOAD_GLOBAL             33 (NULL + AssertionError)
#            2800 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            2810 LOAD_ATTR               34 (_format_explanation)
#            2830 LOAD_FAST               17 (@py_format8)
#            2832 CALL                     1
#            2840 CALL                     1
#            2848 RAISE_VARARGS            1
#         >> 2850 LOAD_CONST               0 (None)
#            2852 COPY                     1
#            2854 STORE_FAST              13 (@py_assert1)
#            2856 COPY                     1
#            2858 STORE_FAST              16 (@py_assert3)
#            2860 STORE_FAST              10 (@py_assert4)
#            2862 RETURN_CONST             0 (None)
# 