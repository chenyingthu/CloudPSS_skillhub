# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/__pycache__/test_pandapower_sc_adapter.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


def TestPandapowerSCAdapterLifecycle():
    """TestPandapowerSCAdapterLifecycle"""
pass  # TODO: restore


def TestPandapowerSCAdapterCase9():
    """TestPandapowerSCAdapterCase9"""
pass  # TODO: restore


def TestPandapowerSCAdapterCase14():
    """TestPandapowerSCAdapterCase14"""
pass  # TODO: restore


def TestPandapowerSCAdapterNetworkInput():
    """TestPandapowerSCAdapterNetworkInput"""
pass  # TODO: restore


def TestPandapowerSCAdapterValidation():
    """TestPandapowerSCAdapterValidation"""
pass  # TODO: restore


def TestPandapowerSCAdapterViaFactory():
    """TestPandapowerSCAdapterViaFactory"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('\nTests for PandapowerShortCircuitAdapter.\n\nREAL tests using actual pp.shortcircuit.calc_sc() on pandapower IEEE cases.\nNo mocks — every test exercises the full pandapower → DataLib pipeline.\n')
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
#  11          56 LOAD_CONST               1 (0)
#              58 LOAD_CONST               4 (('PandapowerShortCircuitAdapter',))
#              60 IMPORT_NAME             11 (cloudpss_skills_v2.powerapi.adapters.pandapower)
#              62 IMPORT_FROM             12 (PandapowerShortCircuitAdapter)
#              64 STORE_NAME              12 (PandapowerShortCircuitAdapter)
#              66 POP_TOP
# 
#  14          68 LOAD_CONST               1 (0)
#              70 LOAD_CONST               5 (('FaultData',))
#              72 IMPORT_NAME             13 (cloudpss_skills_v2.libs.data_lib)
#              74 IMPORT_FROM             14 (FaultData)
#              76 STORE_NAME              14 (FaultData)
#              78 POP_TOP
# 
#  17          80 PUSH_NULL
#              82 LOAD_BUILD_CLASS
#              84 LOAD_CONST               6 (<code object TestPandapowerSCAdapterLifecycle at 0x73cd945fe6b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 17>)
#              86 MAKE_FUNCTION            0
#              88 LOAD_CONST               7 ('TestPandapowerSCAdapterLifecycle')
#              90 CALL                     2
#              98 STORE_NAME              15 (TestPandapowerSCAdapterLifecycle)
# 
#  32         100 PUSH_NULL
#             102 LOAD_BUILD_CLASS
#             104 LOAD_CONST               8 (<code object TestPandapowerSCAdapterCase9 at 0x73cd9495ba60, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 32>)
#             106 MAKE_FUNCTION            0
#             108 LOAD_CONST               9 ('TestPandapowerSCAdapterCase9')
#             110 CALL                     2
#             118 STORE_NAME              16 (TestPandapowerSCAdapterCase9)
# 
#  69         120 PUSH_NULL
#             122 LOAD_BUILD_CLASS
#             124 LOAD_CONST              10 (<code object TestPandapowerSCAdapterCase14 at 0x73cd93b1e340, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 69>)
#             126 MAKE_FUNCTION            0
#             128 LOAD_CONST              11 ('TestPandapowerSCAdapterCase14')
#             130 CALL                     2
#             138 STORE_NAME              17 (TestPandapowerSCAdapterCase14)
# 
#  83         140 PUSH_NULL
#             142 LOAD_BUILD_CLASS
#             144 LOAD_CONST              12 (<code object TestPandapowerSCAdapterNetworkInput at 0x73cd945fe870, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 83>)
#             146 MAKE_FUNCTION            0
#             148 LOAD_CONST              13 ('TestPandapowerSCAdapterNetworkInput')
#             150 CALL                     2
#             158 STORE_NAME              18 (TestPandapowerSCAdapterNetworkInput)
# 
#  95         160 PUSH_NULL
#             162 LOAD_BUILD_CLASS
#             164 LOAD_CONST              14 (<code object TestPandapowerSCAdapterValidation at 0x73cd945fe4f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 95>)
#             166 MAKE_FUNCTION            0
#             168 LOAD_CONST              15 ('TestPandapowerSCAdapterValidation')
#             170 CALL                     2
#             178 STORE_NAME              19 (TestPandapowerSCAdapterValidation)
# 
# 109         180 PUSH_NULL
#             182 LOAD_BUILD_CLASS
#             184 LOAD_CONST              16 (<code object TestPandapowerSCAdapterViaFactory at 0x73cd945fe950, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 109>)
#             186 MAKE_FUNCTION            0
#             188 LOAD_CONST              17 ('TestPandapowerSCAdapterViaFactory')
#             190 CALL                     2
#             198 STORE_NAME              20 (TestPandapowerSCAdapterViaFactory)
#             200 RETURN_CONST             2 (None)
# 
# Disassembly of <code object TestPandapowerSCAdapterLifecycle at 0x73cd945fe6b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 17>:
#  17           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestPandapowerSCAdapterLifecycle')
#               8 STORE_NAME               2 (__qualname__)
# 
#  18          10 LOAD_CONST               1 (<code object test_connect_succeeds at 0x3af95520, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 18>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_connect_succeeds)
# 
#  23          16 LOAD_CONST               2 (<code object test_engine_name at 0x3af3fb70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 23>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_engine_name)
# 
#  27          22 LOAD_CONST               3 (<code object test_supported_simulations at 0x3af96e20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 27>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_supported_simulations)
#              28 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_connect_succeeds at 0x3af95520, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 18>:
#  18           0 RESUME                   0
# 
#  19           2 LOAD_GLOBAL              1 (NULL + PandapowerShortCircuitAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
#  20          22 LOAD_FAST                1 (adapter)
#              24 LOAD_ATTR                3 (NULL|self + connect)
#              44 CALL                     0
#              52 POP_TOP
# 
#  21          54 LOAD_FAST                1 (adapter)
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
# Disassembly of <code object test_engine_name at 0x3af3fb70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 23>:
#  23           0 RESUME                   0
# 
#  24           2 LOAD_GLOBAL              1 (NULL + PandapowerShortCircuitAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
#  25          22 LOAD_FAST                1 (adapter)
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
# Disassembly of <code object test_supported_simulations at 0x3af96e20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 27>:
#  27           0 RESUME                   0
# 
#  28           2 LOAD_GLOBAL              1 (NULL + PandapowerShortCircuitAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
#  29          22 LOAD_GLOBAL              2 (SimulationType)
#              32 LOAD_ATTR                4 (SHORT_CIRCUIT)
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
#             142 LOAD_CONST               2 (('%(py2)s\n{%(py2)s = %(py0)s.SHORT_CIRCUIT\n} in %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.get_supported_simulations\n}()\n}',))
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
# Disassembly of <code object TestPandapowerSCAdapterCase9 at 0x73cd9495ba60, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 32>:
#  32           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestPandapowerSCAdapterCase9')
#               8 STORE_NAME               2 (__qualname__)
# 
#  33          10 PUSH_NULL
#              12 LOAD_NAME                3 (pytest)
#              14 LOAD_ATTR                8 (fixture)
#              34 LOAD_CONST               1 (True)
#              36 KW_NAMES                 2 (('autouse',))
#              38 CALL                     1
# 
#  34          46 LOAD_CONST               3 (<code object setup at 0x73cd948d3730, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 33>)
#              48 MAKE_FUNCTION            0
# 
#  33          50 CALL                     0
# 
#  34          58 STORE_NAME               5 (setup)
# 
#  39          60 LOAD_CONST               4 (<code object test_completes at 0x3afa23c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 39>)
#              62 MAKE_FUNCTION            0
#              64 STORE_NAME               6 (test_completes)
# 
#  42          66 LOAD_CONST               5 (<code object test_fault_currents_populated at 0x3aef4bd0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 42>)
#              68 MAKE_FUNCTION            0
#              70 STORE_NAME               7 (test_fault_currents_populated)
# 
#  45          72 LOAD_CONST               6 (<code object test_ikss_positive at 0x73cd948baa30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 45>)
#              74 MAKE_FUNCTION            0
#              76 STORE_NAME               8 (test_ikss_positive)
# 
#  49          78 LOAD_CONST               7 (<code object test_ikss_max_reasonable at 0x3af23100, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 49>)
#              80 MAKE_FUNCTION            0
#              82 STORE_NAME               9 (test_ikss_max_reasonable)
# 
#  52          84 LOAD_CONST               8 (<code object test_skss_total_reasonable at 0x73cd949426f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 52>)
#              86 MAKE_FUNCTION            0
#              88 STORE_NAME              10 (test_skss_total_reasonable)
# 
#  55          90 LOAD_CONST               9 (<code object test_standard_is_iec at 0x73cd94942ad0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 55>)
#              92 MAKE_FUNCTION            0
#              94 STORE_NAME              11 (test_standard_is_iec)
# 
#  58          96 LOAD_CONST              10 (<code object test_fault_data_roundtrip at 0x3aef47a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 58>)
#              98 MAKE_FUNCTION            0
#             100 STORE_NAME              12 (test_fault_data_roundtrip)
#             102 RETURN_CONST            11 (None)
# 
# Disassembly of <code object setup at 0x73cd948d3730, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 33>:
#  33           0 RESUME                   0
# 
#  35           2 LOAD_GLOBAL              1 (NULL + PandapowerShortCircuitAdapter)
#              12 CALL                     0
#              20 LOAD_FAST                0 (self)
#              22 STORE_ATTR               1 (adapter)
# 
#  36          32 LOAD_FAST                0 (self)
#              34 LOAD_ATTR                2 (adapter)
#              54 LOAD_ATTR                5 (NULL|self + connect)
#              74 CALL                     0
#              82 POP_TOP
# 
#  37          84 LOAD_FAST                0 (self)
#              86 LOAD_ATTR                2 (adapter)
#             106 LOAD_ATTR                7 (NULL|self + run_simulation)
#             126 LOAD_CONST               1 ('case')
#             128 LOAD_CONST               2 ('case9')
#             130 BUILD_MAP                1
#             132 CALL                     1
#             140 LOAD_FAST                0 (self)
#             142 STORE_ATTR               4 (result)
#             152 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_completes at 0x3afa23c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 39>:
#  39           0 RESUME                   0
# 
#  40           2 LOAD_FAST                0 (self)
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
#             646 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_fault_currents_populated at 0x3aef4bd0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 42>:
#  42           0 RESUME                   0
# 
#  43           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('fault_currents')
#              46 BINARY_SUBSCR
#              50 STORE_FAST               1 (@py_assert1)
#              52 LOAD_GLOBAL              5 (NULL + len)
#              62 LOAD_FAST                1 (@py_assert1)
#              64 CALL                     1
#              72 STORE_FAST               2 (@py_assert3)
#              74 LOAD_CONST               2 (9)
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
# Disassembly of <code object test_ikss_positive at 0x73cd948baa30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 45>:
#  45           0 RESUME                   0
# 
#  46           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('fault_currents')
#              46 BINARY_SUBSCR
#              50 GET_ITER
#         >>   52 FOR_ITER               130 (to 316)
#              56 STORE_FAST               1 (fc)
# 
#  47          58 LOAD_FAST                1 (fc)
#              60 LOAD_CONST               2 ('ikss_ka')
#              62 BINARY_SUBSCR
#              66 STORE_FAST               2 (@py_assert0)
#              68 LOAD_CONST               3 (0)
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
#             314 JUMP_BACKWARD          132 (to 52)
# 
#  46     >>  316 END_FOR
#             318 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_ikss_max_reasonable at 0x3af23100, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 49>:
#  49           0 RESUME                   0
# 
#  50           2 LOAD_CONST               1 (0)
#               4 STORE_FAST               1 (@py_assert0)
#               6 LOAD_FAST                0 (self)
#               8 LOAD_ATTR                0 (result)
#              28 LOAD_ATTR                2 (data)
#              48 LOAD_CONST               2 ('ikss_max_ka')
#              50 BINARY_SUBSCR
#              54 STORE_FAST               2 (@py_assert4)
#              56 LOAD_FAST                1 (@py_assert0)
#              58 LOAD_FAST                2 (@py_assert4)
#              60 COMPARE_OP               2 (<)
#              64 STORE_FAST               3 (@py_assert2)
#              66 LOAD_CONST               3 (100)
#              68 STORE_FAST               4 (@py_assert6)
#              70 LOAD_FAST                2 (@py_assert4)
#              72 LOAD_FAST                4 (@py_assert6)
#              74 COMPARE_OP               2 (<)
#              78 STORE_FAST               5 (@py_assert3)
#              80 LOAD_FAST                3 (@py_assert2)
#              82 POP_JUMP_IF_FALSE        2 (to 88)
#              84 LOAD_FAST                5 (@py_assert3)
#              86 POP_JUMP_IF_TRUE       130 (to 348)
#         >>   88 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              98 LOAD_ATTR                6 (_call_reprcompare)
#             118 LOAD_CONST               4 (('<', '<'))
#             120 LOAD_FAST                3 (@py_assert2)
#             122 LOAD_FAST                5 (@py_assert3)
#             124 BUILD_TUPLE              2
#             126 LOAD_CONST               5 (('%(py1)s < %(py5)s', '%(py5)s < %(py7)s'))
#             128 LOAD_FAST                1 (@py_assert0)
#             130 LOAD_FAST                2 (@py_assert4)
#             132 LOAD_FAST                4 (@py_assert6)
#             134 BUILD_TUPLE              3
#             136 CALL                     4
#             144 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             154 LOAD_ATTR                8 (_saferepr)
#             174 LOAD_FAST                1 (@py_assert0)
#             176 CALL                     1
#             184 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             194 LOAD_ATTR                8 (_saferepr)
#             214 LOAD_FAST                2 (@py_assert4)
#             216 CALL                     1
#             224 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             234 LOAD_ATTR                8 (_saferepr)
#             254 LOAD_FAST                4 (@py_assert6)
#             256 CALL                     1
#             264 LOAD_CONST               6 (('py1', 'py5', 'py7'))
#             266 BUILD_CONST_KEY_MAP      3
#             268 BINARY_OP                6 (%)
#             272 STORE_FAST               6 (@py_format8)
#             274 LOAD_CONST               7 ('assert %(py9)s')
#             276 LOAD_CONST               8 ('py9')
#             278 LOAD_FAST                6 (@py_format8)
#             280 BUILD_MAP                1
#             282 BINARY_OP                6 (%)
#             286 STORE_FAST               7 (@py_format10)
#             288 LOAD_GLOBAL             11 (NULL + AssertionError)
#             298 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             308 LOAD_ATTR               12 (_format_explanation)
#             328 LOAD_FAST                7 (@py_format10)
#             330 CALL                     1
#             338 CALL                     1
#             346 RAISE_VARARGS            1
#         >>  348 LOAD_CONST               0 (None)
#             350 COPY                     1
#             352 STORE_FAST               1 (@py_assert0)
#             354 COPY                     1
#             356 STORE_FAST               3 (@py_assert2)
#             358 COPY                     1
#             360 STORE_FAST               5 (@py_assert3)
#             362 COPY                     1
#             364 STORE_FAST               2 (@py_assert4)
#             366 STORE_FAST               4 (@py_assert6)
#             368 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_skss_total_reasonable at 0x73cd949426f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 52>:
#  52           0 RESUME                   0
# 
#  53           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('skss_total_mw')
#              46 BINARY_SUBSCR
#              50 STORE_FAST               1 (@py_assert0)
#              52 LOAD_CONST               2 (0)
#              54 STORE_FAST               2 (@py_assert3)
#              56 LOAD_FAST                1 (@py_assert0)
#              58 LOAD_FAST                2 (@py_assert3)
#              60 COMPARE_OP              68 (>)
#              64 STORE_FAST               3 (@py_assert2)
#              66 LOAD_FAST                3 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       108 (to 286)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               3 (('>',))
#             102 LOAD_FAST                3 (@py_assert2)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               4 (('%(py1)s > %(py4)s',))
#             108 LOAD_FAST                1 (@py_assert0)
#             110 LOAD_FAST                2 (@py_assert3)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_saferepr)
#             152 LOAD_FAST                1 (@py_assert0)
#             154 CALL                     1
#             162 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             172 LOAD_ATTR                8 (_saferepr)
#             192 LOAD_FAST                2 (@py_assert3)
#             194 CALL                     1
#             202 LOAD_CONST               5 (('py1', 'py4'))
#             204 BUILD_CONST_KEY_MAP      2
#             206 BINARY_OP                6 (%)
#             210 STORE_FAST               4 (@py_format5)
#             212 LOAD_CONST               6 ('assert %(py6)s')
#             214 LOAD_CONST               7 ('py6')
#             216 LOAD_FAST                4 (@py_format5)
#             218 BUILD_MAP                1
#             220 BINARY_OP                6 (%)
#             224 STORE_FAST               5 (@py_format7)
#             226 LOAD_GLOBAL             11 (NULL + AssertionError)
#             236 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             246 LOAD_ATTR               12 (_format_explanation)
#             266 LOAD_FAST                5 (@py_format7)
#             268 CALL                     1
#             276 CALL                     1
#             284 RAISE_VARARGS            1
#         >>  286 LOAD_CONST               0 (None)
#             288 COPY                     1
#             290 STORE_FAST               1 (@py_assert0)
#             292 COPY                     1
#             294 STORE_FAST               3 (@py_assert2)
#             296 STORE_FAST               2 (@py_assert3)
#             298 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_standard_is_iec at 0x73cd94942ad0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 55>:
#  55           0 RESUME                   0
# 
#  56           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('standard')
#              46 BINARY_SUBSCR
#              50 STORE_FAST               1 (@py_assert0)
#              52 LOAD_CONST               2 ('IEC 60909')
#              54 STORE_FAST               2 (@py_assert3)
#              56 LOAD_FAST                1 (@py_assert0)
#              58 LOAD_FAST                2 (@py_assert3)
#              60 COMPARE_OP              40 (==)
#              64 STORE_FAST               3 (@py_assert2)
#              66 LOAD_FAST                3 (@py_assert2)
#              68 POP_JUMP_IF_TRUE       108 (to 286)
#              70 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              80 LOAD_ATTR                6 (_call_reprcompare)
#             100 LOAD_CONST               3 (('==',))
#             102 LOAD_FAST                3 (@py_assert2)
#             104 BUILD_TUPLE              1
#             106 LOAD_CONST               4 (('%(py1)s == %(py4)s',))
#             108 LOAD_FAST                1 (@py_assert0)
#             110 LOAD_FAST                2 (@py_assert3)
#             112 BUILD_TUPLE              2
#             114 CALL                     4
#             122 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_saferepr)
#             152 LOAD_FAST                1 (@py_assert0)
#             154 CALL                     1
#             162 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             172 LOAD_ATTR                8 (_saferepr)
#             192 LOAD_FAST                2 (@py_assert3)
#             194 CALL                     1
#             202 LOAD_CONST               5 (('py1', 'py4'))
#             204 BUILD_CONST_KEY_MAP      2
#             206 BINARY_OP                6 (%)
#             210 STORE_FAST               4 (@py_format5)
#             212 LOAD_CONST               6 ('assert %(py6)s')
#             214 LOAD_CONST               7 ('py6')
#             216 LOAD_FAST                4 (@py_format5)
#             218 BUILD_MAP                1
#             220 BINARY_OP                6 (%)
#             224 STORE_FAST               5 (@py_format7)
#             226 LOAD_GLOBAL             11 (NULL + AssertionError)
#             236 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             246 LOAD_ATTR               12 (_format_explanation)
#             266 LOAD_FAST                5 (@py_format7)
#             268 CALL                     1
#             276 CALL                     1
#             284 RAISE_VARARGS            1
#         >>  286 LOAD_CONST               0 (None)
#             288 COPY                     1
#             290 STORE_FAST               1 (@py_assert0)
#             292 COPY                     1
#             294 STORE_FAST               3 (@py_assert2)
#             296 STORE_FAST               2 (@py_assert3)
#             298 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_fault_data_roundtrip at 0x3aef47a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 58>:
#  58           0 RESUME                   0
# 
#  59           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('fault_currents')
#              46 BINARY_SUBSCR
#              50 LOAD_CONST               2 (0)
#              52 BINARY_SUBSCR
#              56 STORE_FAST               1 (fc)
# 
#  60          58 LOAD_GLOBAL              5 (NULL + FaultData)
# 
#  61          68 LOAD_FAST                1 (fc)
#              70 LOAD_CONST               3 ('fault_bus')
#              72 BINARY_SUBSCR
# 
#  62          76 LOAD_FAST                1 (fc)
#              78 LOAD_CONST               4 ('fault_type')
#              80 BINARY_SUBSCR
# 
#  63          84 LOAD_FAST                1 (fc)
#              86 LOAD_CONST               5 ('ikss_ka')
#              88 BINARY_SUBSCR
# 
#  64          92 LOAD_FAST                1 (fc)
#              94 LOAD_CONST               6 ('skss_mw')
#              96 BINARY_SUBSCR
#             100 LOAD_CONST               7 (1.0)
#             102 BINARY_OP               11 (/)
# 
#  60         106 KW_NAMES                 8 (('bus', 'fault_type', 'ikss_ka', 'skss_mva'))
#             108 CALL                     4
#             116 STORE_FAST               2 (fault)
# 
#  66         118 LOAD_FAST                2 (fault)
#             120 LOAD_ATTR                6 (ikss_ka)
#             140 STORE_FAST               3 (@py_assert1)
#             142 LOAD_CONST               2 (0)
#             144 STORE_FAST               4 (@py_assert4)
#             146 LOAD_FAST                3 (@py_assert1)
#             148 LOAD_FAST                4 (@py_assert4)
#             150 COMPARE_OP              68 (>)
#             154 STORE_FAST               5 (@py_assert3)
#             156 LOAD_FAST                5 (@py_assert3)
#             158 POP_JUMP_IF_TRUE       173 (to 506)
#             160 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             170 LOAD_ATTR               10 (_call_reprcompare)
#             190 LOAD_CONST               9 (('>',))
#             192 LOAD_FAST                5 (@py_assert3)
#             194 BUILD_TUPLE              1
#             196 LOAD_CONST              10 (('%(py2)s\n{%(py2)s = %(py0)s.ikss_ka\n} > %(py5)s',))
#             198 LOAD_FAST                3 (@py_assert1)
#             200 LOAD_FAST                4 (@py_assert4)
#             202 BUILD_TUPLE              2
#             204 CALL                     4
#             212 LOAD_CONST              11 ('fault')
#             214 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             224 LOAD_ATTR               14 (locals)
#             244 CALL                     0
#             252 CONTAINS_OP              0
#             254 POP_JUMP_IF_TRUE        21 (to 298)
#             256 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             266 LOAD_ATTR               16 (_should_repr_global_name)
#             286 LOAD_FAST                2 (fault)
#             288 CALL                     1
#             296 POP_JUMP_IF_FALSE       21 (to 340)
#         >>  298 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             308 LOAD_ATTR               18 (_saferepr)
#             328 LOAD_FAST                2 (fault)
#             330 CALL                     1
#             338 JUMP_FORWARD             1 (to 342)
#         >>  340 LOAD_CONST              11 ('fault')
#         >>  342 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             352 LOAD_ATTR               18 (_saferepr)
#             372 LOAD_FAST                3 (@py_assert1)
#             374 CALL                     1
#             382 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             392 LOAD_ATTR               18 (_saferepr)
#             412 LOAD_FAST                4 (@py_assert4)
#             414 CALL                     1
#             422 LOAD_CONST              12 (('py0', 'py2', 'py5'))
#             424 BUILD_CONST_KEY_MAP      3
#             426 BINARY_OP                6 (%)
#             430 STORE_FAST               6 (@py_format6)
#             432 LOAD_CONST              13 ('assert %(py7)s')
#             434 LOAD_CONST              14 ('py7')
#             436 LOAD_FAST                6 (@py_format6)
#             438 BUILD_MAP                1
#             440 BINARY_OP                6 (%)
#             444 STORE_FAST               7 (@py_format8)
#             446 LOAD_GLOBAL             21 (NULL + AssertionError)
#             456 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             466 LOAD_ATTR               22 (_format_explanation)
#             486 LOAD_FAST                7 (@py_format8)
#             488 CALL                     1
#             496 CALL                     1
#             504 RAISE_VARARGS            1
#         >>  506 LOAD_CONST               0 (None)
#             508 COPY                     1
#             510 STORE_FAST               3 (@py_assert1)
#             512 COPY                     1
#             514 STORE_FAST               5 (@py_assert3)
#             516 STORE_FAST               4 (@py_assert4)
#             518 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestPandapowerSCAdapterCase14 at 0x73cd93b1e340, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 69>:
#  69           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestPandapowerSCAdapterCase14')
#               8 STORE_NAME               2 (__qualname__)
# 
#  70          10 PUSH_NULL
#              12 LOAD_NAME                3 (pytest)
#              14 LOAD_ATTR                8 (fixture)
#              34 LOAD_CONST               1 (True)
#              36 KW_NAMES                 2 (('autouse',))
#              38 CALL                     1
# 
#  71          46 LOAD_CONST               3 (<code object setup at 0x73cd948d35d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 70>)
#              48 MAKE_FUNCTION            0
# 
#  70          50 CALL                     0
# 
#  71          58 STORE_NAME               5 (setup)
# 
#  76          60 LOAD_CONST               4 (<code object test_completes at 0x3af95770, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 76>)
#              62 MAKE_FUNCTION            0
#              64 STORE_NAME               6 (test_completes)
# 
#  79          66 LOAD_CONST               5 (<code object test_fault_currents_count at 0x3aefbf80, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 79>)
#              68 MAKE_FUNCTION            0
#              70 STORE_NAME               7 (test_fault_currents_count)
#              72 RETURN_CONST             6 (None)
# 
# Disassembly of <code object setup at 0x73cd948d35d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 70>:
#  70           0 RESUME                   0
# 
#  72           2 LOAD_GLOBAL              1 (NULL + PandapowerShortCircuitAdapter)
#              12 CALL                     0
#              20 LOAD_FAST                0 (self)
#              22 STORE_ATTR               1 (adapter)
# 
#  73          32 LOAD_FAST                0 (self)
#              34 LOAD_ATTR                2 (adapter)
#              54 LOAD_ATTR                5 (NULL|self + connect)
#              74 CALL                     0
#              82 POP_TOP
# 
#  74          84 LOAD_FAST                0 (self)
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
# Disassembly of <code object test_completes at 0x3af95770, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 76>:
#  76           0 RESUME                   0
# 
#  77           2 LOAD_FAST                0 (self)
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
#             646 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_fault_currents_count at 0x3aefbf80, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 79>:
#  79           0 RESUME                   0
# 
#  80           2 LOAD_FAST                0 (self)
#               4 LOAD_ATTR                0 (result)
#              24 LOAD_ATTR                2 (data)
#              44 LOAD_CONST               1 ('fault_currents')
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
# Disassembly of <code object TestPandapowerSCAdapterNetworkInput at 0x73cd945fe870, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 83>:
#  83           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestPandapowerSCAdapterNetworkInput')
#               8 STORE_NAME               2 (__qualname__)
# 
#  84          10 LOAD_CONST               1 (<code object test_network_object_input at 0x3af9c2b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 84>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_network_object_input)
#              16 RETURN_CONST             2 (None)
# 
# Disassembly of <code object test_network_object_input at 0x3af9c2b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 84>:
#  84           0 RESUME                   0
# 
#  85           2 LOAD_CONST               1 (0)
#               4 LOAD_CONST               0 (None)
#               6 IMPORT_NAME              0 (pandapower.networks)
#               8 IMPORT_FROM              1 (networks)
#              10 STORE_FAST               1 (nw)
#              12 POP_TOP
# 
#  87          14 LOAD_FAST                1 (nw)
#              16 LOAD_ATTR                5 (NULL|self + case9)
#              36 CALL                     0
#              44 STORE_FAST               2 (net)
# 
#  88          46 LOAD_GLOBAL              7 (NULL + PandapowerShortCircuitAdapter)
#              56 CALL                     0
#              64 STORE_FAST               3 (adapter)
# 
#  89          66 LOAD_FAST                3 (adapter)
#              68 LOAD_ATTR                9 (NULL|self + connect)
#              88 CALL                     0
#              96 POP_TOP
# 
#  90          98 LOAD_FAST                3 (adapter)
#             100 LOAD_ATTR               11 (NULL|self + run_simulation)
#             120 LOAD_CONST               2 ('network')
#             122 LOAD_FAST                2 (net)
#             124 BUILD_MAP                1
#             126 CALL                     1
#             134 STORE_FAST               4 (result)
# 
#  91         136 LOAD_FAST                4 (result)
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
#  92         710 LOAD_FAST                4 (result)
#             712 LOAD_ATTR               34 (data)
#             732 LOAD_CONST              10 ('fault_currents')
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
# Disassembly of <code object TestPandapowerSCAdapterValidation at 0x73cd945fe4f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 95>:
#  95           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestPandapowerSCAdapterValidation')
#               8 STORE_NAME               2 (__qualname__)
# 
#  96          10 LOAD_CONST               1 (<code object test_no_input_fails at 0x3afa2060, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 96>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_no_input_fails)
# 
# 102          16 LOAD_CONST               2 (<code object test_invalid_fault_type at 0x3af91d70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 102>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_invalid_fault_type)
#              22 RETURN_CONST             3 (None)
# 
# Disassembly of <code object test_no_input_fails at 0x3afa2060, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 96>:
#  96           0 RESUME                   0
# 
#  97           2 LOAD_GLOBAL              1 (NULL + PandapowerShortCircuitAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
#  98          22 LOAD_FAST                1 (adapter)
#              24 LOAD_ATTR                3 (NULL|self + connect)
#              44 CALL                     0
#              52 POP_TOP
# 
#  99          54 LOAD_FAST                1 (adapter)
#              56 LOAD_ATTR                5 (NULL|self + run_simulation)
#              76 BUILD_MAP                0
#              78 CALL                     1
#              86 STORE_FAST               2 (result)
# 
# 100          88 LOAD_FAST                2 (result)
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
# Disassembly of <code object test_invalid_fault_type at 0x3af91d70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 102>:
# 102           0 RESUME                   0
# 
# 103           2 LOAD_GLOBAL              1 (NULL + PandapowerShortCircuitAdapter)
#              12 CALL                     0
#              20 STORE_FAST               1 (adapter)
# 
# 104          22 LOAD_FAST                1 (adapter)
#              24 LOAD_ATTR                3 (NULL|self + connect)
#              44 CALL                     0
#              52 POP_TOP
# 
# 105          54 LOAD_FAST                1 (adapter)
#              56 LOAD_ATTR                5 (NULL|self + run_simulation)
#              76 LOAD_CONST               1 ('case9')
#              78 LOAD_CONST               2 ('invalid')
#              80 LOAD_CONST               3 (('case', 'fault_type'))
#              82 BUILD_CONST_KEY_MAP      2
#              84 CALL                     1
#              92 STORE_FAST               2 (result)
# 
# 106          94 LOAD_FAST                2 (result)
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
# Disassembly of <code object TestPandapowerSCAdapterViaFactory at 0x73cd945fe950, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 109>:
# 109           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestPandapowerSCAdapterViaFactory')
#               8 STORE_NAME               2 (__qualname__)
# 
# 110          10 LOAD_CONST               1 (<code object test_factory_creates_sc_api at 0x3af40530, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 110>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_factory_creates_sc_api)
# 
# 116          16 LOAD_CONST               2 (<code object test_factory_lists_pandapower_sc at 0x3af12be0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 116>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_factory_lists_pandapower_sc)
#              22 RETURN_CONST             3 (None)
# 
# Disassembly of <code object test_factory_creates_sc_api at 0x3af40530, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 110>:
# 110           0 RESUME                   0
# 
# 111           2 LOAD_CONST               1 (0)
#               4 LOAD_CONST               2 (('Engine',))
#               6 IMPORT_NAME              0 (cloudpss_skills_v2.powerskill.engine)
#               8 IMPORT_FROM              1 (Engine)
#              10 STORE_FAST               1 (Engine)
#              12 POP_TOP
# 
# 113          14 LOAD_FAST                1 (Engine)
#              16 LOAD_ATTR                5 (NULL|self + create_short_circuit_api)
#              36 LOAD_CONST               3 ('pandapower')
#              38 KW_NAMES                 4 (('engine',))
#              40 CALL                     1
#              48 STORE_FAST               2 (api)
# 
# 114          50 LOAD_CONST               0 (None)
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
# Disassembly of <code object test_factory_lists_pandapower_sc at 0x3af12be0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py", line 116>:
# 116           0 RESUME                   0
# 
# 117           2 LOAD_CONST               1 (0)
#               4 LOAD_CONST               2 (('Engine',))
#               6 IMPORT_NAME              0 (cloudpss_skills_v2.powerskill.engine)
#               8 IMPORT_FROM              1 (Engine)
#              10 STORE_FAST               1 (Engine)
#              12 POP_TOP
# 
# 119          14 LOAD_FAST                1 (Engine)
#              16 LOAD_ATTR                5 (NULL|self + list_engines)
#              36 LOAD_CONST               3 ('short_circuit')
#              38 CALL                     1
#              46 STORE_FAST               2 (engines)
# 
# 120          48 LOAD_CONST               4 ('pandapower')
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