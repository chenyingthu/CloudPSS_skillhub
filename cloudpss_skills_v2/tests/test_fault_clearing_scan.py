# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/__pycache__/test_fault_clearing_scan.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


def TestFaultClearingScanValidate():
    """TestFaultClearingScanValidate"""
pass  # TODO: restore


def TestFaultClearingScanMonotonic():
    """TestFaultClearingScanMonotonic"""
pass  # TODO: restore


def TestFaultClearingScanRun():
    """TestFaultClearingScanRun"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('Tests for fault_clearing_scan skill (v2 pattern).')
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
#              42 LOAD_CONST               3 (('SkillStatus',))
#              44 IMPORT_NAME              8 (cloudpss_skills_v2.core)
#              46 IMPORT_FROM              9 (SkillStatus)
#              48 STORE_NAME               9 (SkillStatus)
#              50 POP_TOP
# 
#   5          52 LOAD_CONST               1 (0)
#              54 LOAD_CONST               4 (('FaultClearingScanSkill',))
#              56 IMPORT_NAME             10 (cloudpss_skills_v2.skills.fault_clearing_scan)
#              58 IMPORT_FROM             11 (FaultClearingScanSkill)
#              60 STORE_NAME              11 (FaultClearingScanSkill)
#              62 POP_TOP
# 
#   8          64 PUSH_NULL
#              66 LOAD_BUILD_CLASS
#              68 LOAD_CONST               5 (<code object TestFaultClearingScanValidate at 0x73cd93b064c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 8>)
#              70 MAKE_FUNCTION            0
#              72 LOAD_CONST               6 ('TestFaultClearingScanValidate')
#              74 CALL                     2
#              82 STORE_NAME              12 (TestFaultClearingScanValidate)
# 
#  37          84 PUSH_NULL
#              86 LOAD_BUILD_CLASS
#              88 LOAD_CONST               7 (<code object TestFaultClearingScanMonotonic at 0x73cd945fea30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 37>)
#              90 MAKE_FUNCTION            0
#              92 LOAD_CONST               8 ('TestFaultClearingScanMonotonic')
#              94 CALL                     2
#             102 STORE_NAME              13 (TestFaultClearingScanMonotonic)
# 
#  62         104 PUSH_NULL
#             106 LOAD_BUILD_CLASS
#             108 LOAD_CONST               9 (<code object TestFaultClearingScanRun at 0x73cd945fe090, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 62>)
#             110 MAKE_FUNCTION            0
#             112 LOAD_CONST              10 ('TestFaultClearingScanRun')
#             114 CALL                     2
#             122 STORE_NAME              14 (TestFaultClearingScanRun)
#             124 RETURN_CONST             2 (None)
# 
# Disassembly of <code object TestFaultClearingScanValidate at 0x73cd93b064c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 8>:
#   8           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestFaultClearingScanValidate')
#               8 STORE_NAME               2 (__qualname__)
# 
#   9          10 LOAD_CONST               1 (<code object test_valid_config at 0x3af0c6d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 9>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_valid_config)
# 
#  17          16 LOAD_CONST               2 (<code object test_missing_model at 0x3af8e200, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 17>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_missing_model)
# 
#  23          22 LOAD_CONST               3 (<code object test_missing_fe_values at 0x3af9f150, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 23>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_missing_fe_values)
# 
#  30          28 LOAD_CONST               4 (<code object test_empty_fe_values at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 30>)
#              30 MAKE_FUNCTION            0
#              32 STORE_NAME               6 (test_empty_fe_values)
#              34 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_valid_config at 0x3af0c6d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 9>:
#   9           0 RESUME                   0
# 
#  10           2 LOAD_GLOBAL              1 (NULL + FaultClearingScanSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  12          22 LOAD_CONST               1 ('model')
#              24 LOAD_CONST               2 ('model/test/IEEE3')
#              26 BUILD_LIST               0
#              28 LOAD_CONST               3 ((2.7, 2.75, 2.8))
#              30 LIST_EXTEND              1
#              32 LOAD_CONST               4 (('rid', 'fe_values'))
#              34 BUILD_CONST_KEY_MAP      2
# 
#  11          36 BUILD_MAP                1
#              38 STORE_FAST               2 (config)
# 
#  14          40 LOAD_FAST                1 (skill)
#              42 LOAD_ATTR                3 (NULL|self + validate)
#              62 LOAD_FAST                2 (config)
#              64 CALL                     1
#              72 UNPACK_SEQUENCE          2
#              76 STORE_FAST               3 (valid)
#              78 STORE_FAST               4 (errors)
# 
#  15          80 LOAD_CONST               5 (True)
#              82 STORE_FAST               5 (@py_assert2)
#              84 LOAD_FAST                3 (valid)
#              86 LOAD_FAST                5 (@py_assert2)
#              88 IS_OP                    0
#              90 STORE_FAST               6 (@py_assert1)
#              92 LOAD_FAST                6 (@py_assert1)
#              94 POP_JUMP_IF_TRUE       153 (to 402)
#              96 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             106 LOAD_ATTR                6 (_call_reprcompare)
#             126 LOAD_CONST               6 (('is',))
#             128 LOAD_FAST                6 (@py_assert1)
#             130 BUILD_TUPLE              1
#             132 LOAD_CONST               7 (('%(py0)s is %(py3)s',))
#             134 LOAD_FAST                3 (valid)
#             136 LOAD_FAST                5 (@py_assert2)
#             138 BUILD_TUPLE              2
#             140 CALL                     4
#             148 LOAD_CONST               8 ('valid')
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
#         >>  276 LOAD_CONST               8 ('valid')
#         >>  278 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             288 LOAD_ATTR               14 (_saferepr)
#             308 LOAD_FAST                5 (@py_assert2)
#             310 CALL                     1
#             318 LOAD_CONST               9 (('py0', 'py3'))
#             320 BUILD_CONST_KEY_MAP      2
#             322 BINARY_OP                6 (%)
#             326 STORE_FAST               7 (@py_format4)
#             328 LOAD_CONST              10 ('assert %(py5)s')
#             330 LOAD_CONST              11 ('py5')
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
# Disassembly of <code object test_missing_model at 0x3af8e200, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 17>:
#  17           0 RESUME                   0
# 
#  18           2 LOAD_GLOBAL              1 (NULL + FaultClearingScanSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  19          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + validate)
#              44 BUILD_MAP                0
#              46 CALL                     1
#              54 UNPACK_SEQUENCE          2
#              58 STORE_FAST               2 (valid)
#              60 STORE_FAST               3 (errors)
# 
#  20          62 LOAD_CONST               1 (False)
#              64 STORE_FAST               4 (@py_assert2)
#              66 LOAD_FAST                2 (valid)
#              68 LOAD_FAST                4 (@py_assert2)
#              70 IS_OP                    0
#              72 STORE_FAST               5 (@py_assert1)
#              74 LOAD_FAST                5 (@py_assert1)
#              76 POP_JUMP_IF_TRUE       153 (to 384)
#              78 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              88 LOAD_ATTR                6 (_call_reprcompare)
#             108 LOAD_CONST               2 (('is',))
#             110 LOAD_FAST                5 (@py_assert1)
#             112 BUILD_TUPLE              1
#             114 LOAD_CONST               3 (('%(py0)s is %(py3)s',))
#             116 LOAD_FAST                2 (valid)
#             118 LOAD_FAST                4 (@py_assert2)
#             120 BUILD_TUPLE              2
#             122 CALL                     4
#             130 LOAD_CONST               4 ('valid')
#             132 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             142 LOAD_ATTR               10 (locals)
#             162 CALL                     0
#             170 CONTAINS_OP              0
#             172 POP_JUMP_IF_TRUE        21 (to 216)
#             174 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             184 LOAD_ATTR               12 (_should_repr_global_name)
#             204 LOAD_FAST                2 (valid)
#             206 CALL                     1
#             214 POP_JUMP_IF_FALSE       21 (to 258)
#         >>  216 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             226 LOAD_ATTR               14 (_saferepr)
#             246 LOAD_FAST                2 (valid)
#             248 CALL                     1
#             256 JUMP_FORWARD             1 (to 260)
#         >>  258 LOAD_CONST               4 ('valid')
#         >>  260 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             270 LOAD_ATTR               14 (_saferepr)
#             290 LOAD_FAST                4 (@py_assert2)
#             292 CALL                     1
#             300 LOAD_CONST               5 (('py0', 'py3'))
#             302 BUILD_CONST_KEY_MAP      2
#             304 BINARY_OP                6 (%)
#             308 STORE_FAST               6 (@py_format4)
#             310 LOAD_CONST               6 ('assert %(py5)s')
#             312 LOAD_CONST               7 ('py5')
#             314 LOAD_FAST                6 (@py_format4)
#             316 BUILD_MAP                1
#             318 BINARY_OP                6 (%)
#             322 STORE_FAST               7 (@py_format6)
#             324 LOAD_GLOBAL             17 (NULL + AssertionError)
#             334 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             344 LOAD_ATTR               18 (_format_explanation)
#             364 LOAD_FAST                7 (@py_format6)
#             366 CALL                     1
#             374 CALL                     1
#             382 RAISE_VARARGS            1
#         >>  384 LOAD_CONST               0 (None)
#             386 COPY                     1
#             388 STORE_FAST               5 (@py_assert1)
#             390 STORE_FAST               4 (@py_assert2)
# 
#  21         392 LOAD_CONST               8 (<code object <genexpr> at 0x73cd93b06970, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 21>)
#             394 MAKE_FUNCTION            0
#             396 LOAD_FAST                3 (errors)
#             398 GET_ITER
#             400 CALL                     0
#             408 STORE_FAST               5 (@py_assert1)
#             410 LOAD_GLOBAL             21 (NULL + any)
#             420 LOAD_FAST                5 (@py_assert1)
#             422 CALL                     1
#             430 STORE_FAST               8 (@py_assert3)
#             432 LOAD_FAST                8 (@py_assert3)
#             434 POP_JUMP_IF_TRUE       149 (to 734)
#             436 LOAD_CONST               9 ('assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}')
#             438 LOAD_CONST              10 ('any')
#             440 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             450 LOAD_ATTR               10 (locals)
#             470 CALL                     0
#             478 CONTAINS_OP              0
#             480 POP_JUMP_IF_TRUE        25 (to 532)
#             482 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             492 LOAD_ATTR               12 (_should_repr_global_name)
#             512 LOAD_GLOBAL             20 (any)
#             522 CALL                     1
#             530 POP_JUMP_IF_FALSE       25 (to 582)
#         >>  532 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             542 LOAD_ATTR               14 (_saferepr)
#             562 LOAD_GLOBAL             20 (any)
#             572 CALL                     1
#             580 JUMP_FORWARD             1 (to 584)
#         >>  582 LOAD_CONST              10 ('any')
#         >>  584 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             594 LOAD_ATTR               14 (_saferepr)
#             614 LOAD_FAST                5 (@py_assert1)
#             616 CALL                     1
#             624 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             634 LOAD_ATTR               14 (_saferepr)
#             654 LOAD_FAST                8 (@py_assert3)
#             656 CALL                     1
#             664 LOAD_CONST              11 (('py0', 'py2', 'py4'))
#             666 BUILD_CONST_KEY_MAP      3
#             668 BINARY_OP                6 (%)
#             672 STORE_FAST               9 (@py_format5)
#             674 LOAD_GLOBAL             17 (NULL + AssertionError)
#             684 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             694 LOAD_ATTR               18 (_format_explanation)
#             714 LOAD_FAST                9 (@py_format5)
#             716 CALL                     1
#             724 CALL                     1
#             732 RAISE_VARARGS            1
#         >>  734 LOAD_CONST               0 (None)
#             736 COPY                     1
#             738 STORE_FAST               5 (@py_assert1)
#             740 STORE_FAST               8 (@py_assert3)
#             742 RETURN_CONST             0 (None)
# 
# Disassembly of <code object <genexpr> at 0x73cd93b06970, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 21>:
#  21           0 RETURN_GENERATOR
#               2 POP_TOP
#               4 RESUME                   0
#               6 LOAD_FAST                0 (.0)
#         >>    8 FOR_ITER                 8 (to 28)
#              12 STORE_FAST               1 (e)
#              14 LOAD_CONST               0 ('model.rid')
#              16 LOAD_FAST                1 (e)
#              18 CONTAINS_OP              0
#              20 YIELD_VALUE              1
#              22 RESUME                   1
#              24 POP_TOP
#              26 JUMP_BACKWARD           10 (to 8)
#         >>   28 END_FOR
#              30 RETURN_CONST             1 (None)
#         >>   32 CALL_INTRINSIC_1         3 (INTRINSIC_STOPITERATION_ERROR)
#              34 RERAISE                  1
# ExceptionTable:
#   4 to 30 -> 32 [0] lasti
# 
# Disassembly of <code object test_missing_fe_values at 0x3af9f150, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 23>:
#  23           0 RESUME                   0
# 
#  24           2 LOAD_GLOBAL              1 (NULL + FaultClearingScanSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  25          22 LOAD_CONST               1 ('model')
#              24 LOAD_CONST               2 ('rid')
#              26 LOAD_CONST               3 ('test')
#              28 BUILD_MAP                1
#              30 BUILD_MAP                1
#              32 STORE_FAST               2 (config)
# 
#  26          34 LOAD_FAST                1 (skill)
#              36 LOAD_ATTR                3 (NULL|self + validate)
#              56 LOAD_FAST                2 (config)
#              58 CALL                     1
#              66 UNPACK_SEQUENCE          2
#              70 STORE_FAST               3 (valid)
#              72 STORE_FAST               4 (errors)
# 
#  27          74 LOAD_CONST               4 (False)
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
# 
#  28         404 LOAD_CONST              11 (<code object <genexpr> at 0x73cd93b06880, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 28>)
#             406 MAKE_FUNCTION            0
#             408 LOAD_FAST                4 (errors)
#             410 GET_ITER
#             412 CALL                     0
#             420 STORE_FAST               6 (@py_assert1)
#             422 LOAD_GLOBAL             21 (NULL + any)
#             432 LOAD_FAST                6 (@py_assert1)
#             434 CALL                     1
#             442 STORE_FAST               9 (@py_assert3)
#             444 LOAD_FAST                9 (@py_assert3)
#             446 POP_JUMP_IF_TRUE       149 (to 746)
#             448 LOAD_CONST              12 ('assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}')
#             450 LOAD_CONST              13 ('any')
#             452 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             462 LOAD_ATTR               10 (locals)
#             482 CALL                     0
#             490 CONTAINS_OP              0
#             492 POP_JUMP_IF_TRUE        25 (to 544)
#             494 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             504 LOAD_ATTR               12 (_should_repr_global_name)
#             524 LOAD_GLOBAL             20 (any)
#             534 CALL                     1
#             542 POP_JUMP_IF_FALSE       25 (to 594)
#         >>  544 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             554 LOAD_ATTR               14 (_saferepr)
#             574 LOAD_GLOBAL             20 (any)
#             584 CALL                     1
#             592 JUMP_FORWARD             1 (to 596)
#         >>  594 LOAD_CONST              13 ('any')
#         >>  596 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             606 LOAD_ATTR               14 (_saferepr)
#             626 LOAD_FAST                6 (@py_assert1)
#             628 CALL                     1
#             636 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             646 LOAD_ATTR               14 (_saferepr)
#             666 LOAD_FAST                9 (@py_assert3)
#             668 CALL                     1
#             676 LOAD_CONST              14 (('py0', 'py2', 'py4'))
#             678 BUILD_CONST_KEY_MAP      3
#             680 BINARY_OP                6 (%)
#             684 STORE_FAST              10 (@py_format5)
#             686 LOAD_GLOBAL             17 (NULL + AssertionError)
#             696 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             706 LOAD_ATTR               18 (_format_explanation)
#             726 LOAD_FAST               10 (@py_format5)
#             728 CALL                     1
#             736 CALL                     1
#             744 RAISE_VARARGS            1
#         >>  746 LOAD_CONST               0 (None)
#             748 COPY                     1
#             750 STORE_FAST               6 (@py_assert1)
#             752 STORE_FAST               9 (@py_assert3)
#             754 RETURN_CONST             0 (None)
# 
# Disassembly of <code object <genexpr> at 0x73cd93b06880, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 28>:
#  28           0 RETURN_GENERATOR
#               2 POP_TOP
#               4 RESUME                   0
#               6 LOAD_FAST                0 (.0)
#         >>    8 FOR_ITER                 8 (to 28)
#              12 STORE_FAST               1 (e)
#              14 LOAD_CONST               0 ('fe_values')
#              16 LOAD_FAST                1 (e)
#              18 CONTAINS_OP              0
#              20 YIELD_VALUE              1
#              22 RESUME                   1
#              24 POP_TOP
#              26 JUMP_BACKWARD           10 (to 8)
#         >>   28 END_FOR
#              30 RETURN_CONST             1 (None)
#         >>   32 CALL_INTRINSIC_1         3 (INTRINSIC_STOPITERATION_ERROR)
#              34 RERAISE                  1
# ExceptionTable:
#   4 to 30 -> 32 [0] lasti
# 
# Disassembly of <code object test_empty_fe_values at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 30>:
#  30           0 RESUME                   0
# 
#  31           2 LOAD_GLOBAL              1 (NULL + FaultClearingScanSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  32          22 LOAD_CONST               1 ('model')
#              24 LOAD_CONST               2 ('test')
#              26 BUILD_LIST               0
#              28 LOAD_CONST               3 (('rid', 'fe_values'))
#              30 BUILD_CONST_KEY_MAP      2
#              32 BUILD_MAP                1
#              34 STORE_FAST               2 (config)
# 
#  33          36 LOAD_FAST                1 (skill)
#              38 LOAD_ATTR                3 (NULL|self + validate)
#              58 LOAD_FAST                2 (config)
#              60 CALL                     1
#              68 UNPACK_SEQUENCE          2
#              72 STORE_FAST               3 (valid)
#              74 STORE_FAST               4 (errors)
# 
#  34          76 LOAD_CONST               4 (False)
#              78 STORE_FAST               5 (@py_assert2)
#              80 LOAD_FAST                3 (valid)
#              82 LOAD_FAST                5 (@py_assert2)
#              84 IS_OP                    0
#              86 STORE_FAST               6 (@py_assert1)
#              88 LOAD_FAST                6 (@py_assert1)
#              90 POP_JUMP_IF_TRUE       153 (to 398)
#              92 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             102 LOAD_ATTR                6 (_call_reprcompare)
#             122 LOAD_CONST               5 (('is',))
#             124 LOAD_FAST                6 (@py_assert1)
#             126 BUILD_TUPLE              1
#             128 LOAD_CONST               6 (('%(py0)s is %(py3)s',))
#             130 LOAD_FAST                3 (valid)
#             132 LOAD_FAST                5 (@py_assert2)
#             134 BUILD_TUPLE              2
#             136 CALL                     4
#             144 LOAD_CONST               7 ('valid')
#             146 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             156 LOAD_ATTR               10 (locals)
#             176 CALL                     0
#             184 CONTAINS_OP              0
#             186 POP_JUMP_IF_TRUE        21 (to 230)
#             188 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             198 LOAD_ATTR               12 (_should_repr_global_name)
#             218 LOAD_FAST                3 (valid)
#             220 CALL                     1
#             228 POP_JUMP_IF_FALSE       21 (to 272)
#         >>  230 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             240 LOAD_ATTR               14 (_saferepr)
#             260 LOAD_FAST                3 (valid)
#             262 CALL                     1
#             270 JUMP_FORWARD             1 (to 274)
#         >>  272 LOAD_CONST               7 ('valid')
#         >>  274 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             284 LOAD_ATTR               14 (_saferepr)
#             304 LOAD_FAST                5 (@py_assert2)
#             306 CALL                     1
#             314 LOAD_CONST               8 (('py0', 'py3'))
#             316 BUILD_CONST_KEY_MAP      2
#             318 BINARY_OP                6 (%)
#             322 STORE_FAST               7 (@py_format4)
#             324 LOAD_CONST               9 ('assert %(py5)s')
#             326 LOAD_CONST              10 ('py5')
#             328 LOAD_FAST                7 (@py_format4)
#             330 BUILD_MAP                1
#             332 BINARY_OP                6 (%)
#             336 STORE_FAST               8 (@py_format6)
#             338 LOAD_GLOBAL             17 (NULL + AssertionError)
#             348 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             358 LOAD_ATTR               18 (_format_explanation)
#             378 LOAD_FAST                8 (@py_format6)
#             380 CALL                     1
#             388 CALL                     1
#             396 RAISE_VARARGS            1
#         >>  398 LOAD_CONST               0 (None)
#             400 COPY                     1
#             402 STORE_FAST               6 (@py_assert1)
#             404 STORE_FAST               5 (@py_assert2)
#             406 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestFaultClearingScanMonotonic at 0x73cd945fea30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 37>:
#  37           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestFaultClearingScanMonotonic')
#               8 STORE_NAME               2 (__qualname__)
# 
#  38          10 LOAD_CONST               1 (<code object test_monotonic_degradation at 0x3afa23c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 38>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_monotonic_degradation)
# 
#  47          16 LOAD_CONST               2 (<code object test_non_monotonic at 0x3af95770, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 47>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_non_monotonic)
# 
#  56          22 LOAD_CONST               3 (<code object test_single_value at 0x3af9a2d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 56>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_single_value)
#              28 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_monotonic_degradation at 0x3afa23c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 38>:
#  38           0 RESUME                   0
# 
#  39           2 LOAD_GLOBAL              1 (NULL + FaultClearingScanSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  41          22 LOAD_CONST               1 (2.7)
#              24 LOAD_CONST               2 (1.0)
#              26 LOAD_CONST               3 (('fe', 'voltage_at_study'))
#              28 BUILD_CONST_KEY_MAP      2
# 
#  42          30 LOAD_CONST               4 (2.8)
#              32 LOAD_CONST               5 (0.9)
#              34 LOAD_CONST               3 (('fe', 'voltage_at_study'))
#              36 BUILD_CONST_KEY_MAP      2
# 
#  43          38 LOAD_CONST               6 (2.9)
#              40 LOAD_CONST               7 (0.8)
#              42 LOAD_CONST               3 (('fe', 'voltage_at_study'))
#              44 BUILD_CONST_KEY_MAP      2
# 
#  40          46 BUILD_LIST               3
#              48 STORE_FAST               2 (results)
# 
#  45          50 LOAD_FAST                1 (skill)
#              52 LOAD_ATTR                2 (_check_monotonic_degradation)
#              72 STORE_FAST               3 (@py_assert1)
#              74 PUSH_NULL
#              76 LOAD_FAST                3 (@py_assert1)
#              78 LOAD_FAST                2 (results)
#              80 CALL                     1
#              88 STORE_FAST               4 (@py_assert4)
#              90 LOAD_CONST               8 (True)
#              92 STORE_FAST               5 (@py_assert7)
#              94 LOAD_FAST                4 (@py_assert4)
#              96 LOAD_FAST                5 (@py_assert7)
#              98 IS_OP                    0
#             100 STORE_FAST               6 (@py_assert6)
#             102 LOAD_FAST                6 (@py_assert6)
#             104 EXTENDED_ARG             1
#             106 POP_JUMP_IF_TRUE       258 (to 624)
#             108 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             118 LOAD_ATTR                6 (_call_reprcompare)
#             138 LOAD_CONST               9 (('is',))
#             140 LOAD_FAST                6 (@py_assert6)
#             142 BUILD_TUPLE              1
#             144 LOAD_CONST              10 (('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s._check_monotonic_degradation\n}(%(py3)s)\n} is %(py8)s',))
#             146 LOAD_FAST                4 (@py_assert4)
#             148 LOAD_FAST                5 (@py_assert7)
#             150 BUILD_TUPLE              2
#             152 CALL                     4
#             160 LOAD_CONST              11 ('skill')
#             162 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             172 LOAD_ATTR               10 (locals)
#             192 CALL                     0
#             200 CONTAINS_OP              0
#             202 POP_JUMP_IF_TRUE        21 (to 246)
#             204 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             214 LOAD_ATTR               12 (_should_repr_global_name)
#             234 LOAD_FAST                1 (skill)
#             236 CALL                     1
#             244 POP_JUMP_IF_FALSE       21 (to 288)
#         >>  246 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             256 LOAD_ATTR               14 (_saferepr)
#             276 LOAD_FAST                1 (skill)
#             278 CALL                     1
#             286 JUMP_FORWARD             1 (to 290)
#         >>  288 LOAD_CONST              11 ('skill')
#         >>  290 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             300 LOAD_ATTR               14 (_saferepr)
#             320 LOAD_FAST                3 (@py_assert1)
#             322 CALL                     1
#             330 LOAD_CONST              12 ('results')
#             332 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             342 LOAD_ATTR               10 (locals)
#             362 CALL                     0
#             370 CONTAINS_OP              0
#             372 POP_JUMP_IF_TRUE        21 (to 416)
#             374 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             384 LOAD_ATTR               12 (_should_repr_global_name)
#             404 LOAD_FAST                2 (results)
#             406 CALL                     1
#             414 POP_JUMP_IF_FALSE       21 (to 458)
#         >>  416 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             426 LOAD_ATTR               14 (_saferepr)
#             446 LOAD_FAST                2 (results)
#             448 CALL                     1
#             456 JUMP_FORWARD             1 (to 460)
#         >>  458 LOAD_CONST              12 ('results')
#         >>  460 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             470 LOAD_ATTR               14 (_saferepr)
#             490 LOAD_FAST                4 (@py_assert4)
#             492 CALL                     1
#             500 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             510 LOAD_ATTR               14 (_saferepr)
#             530 LOAD_FAST                5 (@py_assert7)
#             532 CALL                     1
#             540 LOAD_CONST              13 (('py0', 'py2', 'py3', 'py5', 'py8'))
#             542 BUILD_CONST_KEY_MAP      5
#             544 BINARY_OP                6 (%)
#             548 STORE_FAST               7 (@py_format9)
#             550 LOAD_CONST              14 ('assert %(py10)s')
#             552 LOAD_CONST              15 ('py10')
#             554 LOAD_FAST                7 (@py_format9)
#             556 BUILD_MAP                1
#             558 BINARY_OP                6 (%)
#             562 STORE_FAST               8 (@py_format11)
#             564 LOAD_GLOBAL             17 (NULL + AssertionError)
#             574 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             584 LOAD_ATTR               18 (_format_explanation)
#             604 LOAD_FAST                8 (@py_format11)
#             606 CALL                     1
#             614 CALL                     1
#             622 RAISE_VARARGS            1
#         >>  624 LOAD_CONST               0 (None)
#             626 COPY                     1
#             628 STORE_FAST               3 (@py_assert1)
#             630 COPY                     1
#             632 STORE_FAST               4 (@py_assert4)
#             634 COPY                     1
#             636 STORE_FAST               6 (@py_assert6)
#             638 STORE_FAST               5 (@py_assert7)
#             640 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_non_monotonic at 0x3af95770, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 47>:
#  47           0 RESUME                   0
# 
#  48           2 LOAD_GLOBAL              1 (NULL + FaultClearingScanSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  50          22 LOAD_CONST               1 (2.7)
#              24 LOAD_CONST               2 (1.0)
#              26 LOAD_CONST               3 (('fe', 'voltage_at_study'))
#              28 BUILD_CONST_KEY_MAP      2
# 
#  51          30 LOAD_CONST               4 (2.8)
#              32 LOAD_CONST               5 (0.95)
#              34 LOAD_CONST               3 (('fe', 'voltage_at_study'))
#              36 BUILD_CONST_KEY_MAP      2
# 
#  52          38 LOAD_CONST               6 (2.9)
#              40 LOAD_CONST               7 (1.05)
#              42 LOAD_CONST               3 (('fe', 'voltage_at_study'))
#              44 BUILD_CONST_KEY_MAP      2
# 
#  49          46 BUILD_LIST               3
#              48 STORE_FAST               2 (results)
# 
#  54          50 LOAD_FAST                1 (skill)
#              52 LOAD_ATTR                2 (_check_monotonic_degradation)
#              72 STORE_FAST               3 (@py_assert1)
#              74 PUSH_NULL
#              76 LOAD_FAST                3 (@py_assert1)
#              78 LOAD_FAST                2 (results)
#              80 CALL                     1
#              88 STORE_FAST               4 (@py_assert4)
#              90 LOAD_CONST               8 (False)
#              92 STORE_FAST               5 (@py_assert7)
#              94 LOAD_FAST                4 (@py_assert4)
#              96 LOAD_FAST                5 (@py_assert7)
#              98 IS_OP                    0
#             100 STORE_FAST               6 (@py_assert6)
#             102 LOAD_FAST                6 (@py_assert6)
#             104 EXTENDED_ARG             1
#             106 POP_JUMP_IF_TRUE       258 (to 624)
#             108 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             118 LOAD_ATTR                6 (_call_reprcompare)
#             138 LOAD_CONST               9 (('is',))
#             140 LOAD_FAST                6 (@py_assert6)
#             142 BUILD_TUPLE              1
#             144 LOAD_CONST              10 (('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s._check_monotonic_degradation\n}(%(py3)s)\n} is %(py8)s',))
#             146 LOAD_FAST                4 (@py_assert4)
#             148 LOAD_FAST                5 (@py_assert7)
#             150 BUILD_TUPLE              2
#             152 CALL                     4
#             160 LOAD_CONST              11 ('skill')
#             162 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             172 LOAD_ATTR               10 (locals)
#             192 CALL                     0
#             200 CONTAINS_OP              0
#             202 POP_JUMP_IF_TRUE        21 (to 246)
#             204 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             214 LOAD_ATTR               12 (_should_repr_global_name)
#             234 LOAD_FAST                1 (skill)
#             236 CALL                     1
#             244 POP_JUMP_IF_FALSE       21 (to 288)
#         >>  246 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             256 LOAD_ATTR               14 (_saferepr)
#             276 LOAD_FAST                1 (skill)
#             278 CALL                     1
#             286 JUMP_FORWARD             1 (to 290)
#         >>  288 LOAD_CONST              11 ('skill')
#         >>  290 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             300 LOAD_ATTR               14 (_saferepr)
#             320 LOAD_FAST                3 (@py_assert1)
#             322 CALL                     1
#             330 LOAD_CONST              12 ('results')
#             332 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             342 LOAD_ATTR               10 (locals)
#             362 CALL                     0
#             370 CONTAINS_OP              0
#             372 POP_JUMP_IF_TRUE        21 (to 416)
#             374 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             384 LOAD_ATTR               12 (_should_repr_global_name)
#             404 LOAD_FAST                2 (results)
#             406 CALL                     1
#             414 POP_JUMP_IF_FALSE       21 (to 458)
#         >>  416 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             426 LOAD_ATTR               14 (_saferepr)
#             446 LOAD_FAST                2 (results)
#             448 CALL                     1
#             456 JUMP_FORWARD             1 (to 460)
#         >>  458 LOAD_CONST              12 ('results')
#         >>  460 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             470 LOAD_ATTR               14 (_saferepr)
#             490 LOAD_FAST                4 (@py_assert4)
#             492 CALL                     1
#             500 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             510 LOAD_ATTR               14 (_saferepr)
#             530 LOAD_FAST                5 (@py_assert7)
#             532 CALL                     1
#             540 LOAD_CONST              13 (('py0', 'py2', 'py3', 'py5', 'py8'))
#             542 BUILD_CONST_KEY_MAP      5
#             544 BINARY_OP                6 (%)
#             548 STORE_FAST               7 (@py_format9)
#             550 LOAD_CONST              14 ('assert %(py10)s')
#             552 LOAD_CONST              15 ('py10')
#             554 LOAD_FAST                7 (@py_format9)
#             556 BUILD_MAP                1
#             558 BINARY_OP                6 (%)
#             562 STORE_FAST               8 (@py_format11)
#             564 LOAD_GLOBAL             17 (NULL + AssertionError)
#             574 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             584 LOAD_ATTR               18 (_format_explanation)
#             604 LOAD_FAST                8 (@py_format11)
#             606 CALL                     1
#             614 CALL                     1
#             622 RAISE_VARARGS            1
#         >>  624 LOAD_CONST               0 (None)
#             626 COPY                     1
#             628 STORE_FAST               3 (@py_assert1)
#             630 COPY                     1
#             632 STORE_FAST               4 (@py_assert4)
#             634 COPY                     1
#             636 STORE_FAST               6 (@py_assert6)
#             638 STORE_FAST               5 (@py_assert7)
#             640 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_single_value at 0x3af9a2d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 56>:
#  56           0 RESUME                   0
# 
#  57           2 LOAD_GLOBAL              1 (NULL + FaultClearingScanSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  58          22 LOAD_CONST               1 (2.7)
#              24 LOAD_CONST               2 (1.0)
#              26 LOAD_CONST               3 (('fe', 'voltage_at_study'))
#              28 BUILD_CONST_KEY_MAP      2
#              30 BUILD_LIST               1
#              32 STORE_FAST               2 (results)
# 
#  59          34 LOAD_FAST                1 (skill)
#              36 LOAD_ATTR                2 (_check_monotonic_degradation)
#              56 STORE_FAST               3 (@py_assert1)
#              58 PUSH_NULL
#              60 LOAD_FAST                3 (@py_assert1)
#              62 LOAD_FAST                2 (results)
#              64 CALL                     1
#              72 STORE_FAST               4 (@py_assert4)
#              74 LOAD_CONST               4 (False)
#              76 STORE_FAST               5 (@py_assert7)
#              78 LOAD_FAST                4 (@py_assert4)
#              80 LOAD_FAST                5 (@py_assert7)
#              82 IS_OP                    0
#              84 STORE_FAST               6 (@py_assert6)
#              86 LOAD_FAST                6 (@py_assert6)
#              88 EXTENDED_ARG             1
#              90 POP_JUMP_IF_TRUE       258 (to 608)
#              92 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             102 LOAD_ATTR                6 (_call_reprcompare)
#             122 LOAD_CONST               5 (('is',))
#             124 LOAD_FAST                6 (@py_assert6)
#             126 BUILD_TUPLE              1
#             128 LOAD_CONST               6 (('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s._check_monotonic_degradation\n}(%(py3)s)\n} is %(py8)s',))
#             130 LOAD_FAST                4 (@py_assert4)
#             132 LOAD_FAST                5 (@py_assert7)
#             134 BUILD_TUPLE              2
#             136 CALL                     4
#             144 LOAD_CONST               7 ('skill')
#             146 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             156 LOAD_ATTR               10 (locals)
#             176 CALL                     0
#             184 CONTAINS_OP              0
#             186 POP_JUMP_IF_TRUE        21 (to 230)
#             188 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             198 LOAD_ATTR               12 (_should_repr_global_name)
#             218 LOAD_FAST                1 (skill)
#             220 CALL                     1
#             228 POP_JUMP_IF_FALSE       21 (to 272)
#         >>  230 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             240 LOAD_ATTR               14 (_saferepr)
#             260 LOAD_FAST                1 (skill)
#             262 CALL                     1
#             270 JUMP_FORWARD             1 (to 274)
#         >>  272 LOAD_CONST               7 ('skill')
#         >>  274 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             284 LOAD_ATTR               14 (_saferepr)
#             304 LOAD_FAST                3 (@py_assert1)
#             306 CALL                     1
#             314 LOAD_CONST               8 ('results')
#             316 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             326 LOAD_ATTR               10 (locals)
#             346 CALL                     0
#             354 CONTAINS_OP              0
#             356 POP_JUMP_IF_TRUE        21 (to 400)
#             358 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             368 LOAD_ATTR               12 (_should_repr_global_name)
#             388 LOAD_FAST                2 (results)
#             390 CALL                     1
#             398 POP_JUMP_IF_FALSE       21 (to 442)
#         >>  400 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             410 LOAD_ATTR               14 (_saferepr)
#             430 LOAD_FAST                2 (results)
#             432 CALL                     1
#             440 JUMP_FORWARD             1 (to 444)
#         >>  442 LOAD_CONST               8 ('results')
#         >>  444 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             454 LOAD_ATTR               14 (_saferepr)
#             474 LOAD_FAST                4 (@py_assert4)
#             476 CALL                     1
#             484 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             494 LOAD_ATTR               14 (_saferepr)
#             514 LOAD_FAST                5 (@py_assert7)
#             516 CALL                     1
#             524 LOAD_CONST               9 (('py0', 'py2', 'py3', 'py5', 'py8'))
#             526 BUILD_CONST_KEY_MAP      5
#             528 BINARY_OP                6 (%)
#             532 STORE_FAST               7 (@py_format9)
#             534 LOAD_CONST              10 ('assert %(py10)s')
#             536 LOAD_CONST              11 ('py10')
#             538 LOAD_FAST                7 (@py_format9)
#             540 BUILD_MAP                1
#             542 BINARY_OP                6 (%)
#             546 STORE_FAST               8 (@py_format11)
#             548 LOAD_GLOBAL             17 (NULL + AssertionError)
#             558 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             568 LOAD_ATTR               18 (_format_explanation)
#             588 LOAD_FAST                8 (@py_format11)
#             590 CALL                     1
#             598 CALL                     1
#             606 RAISE_VARARGS            1
#         >>  608 LOAD_CONST               0 (None)
#             610 COPY                     1
#             612 STORE_FAST               3 (@py_assert1)
#             614 COPY                     1
#             616 STORE_FAST               4 (@py_assert4)
#             618 COPY                     1
#             620 STORE_FAST               6 (@py_assert6)
#             622 STORE_FAST               5 (@py_assert7)
#             624 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestFaultClearingScanRun at 0x73cd945fe090, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 62>:
#  62           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestFaultClearingScanRun')
#               8 STORE_NAME               2 (__qualname__)
# 
#  63          10 LOAD_CONST               1 (<code object test_validation_failure at 0x3af9b9b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 63>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_validation_failure)
# 
#  68          16 LOAD_CONST               2 (<code object test_run_with_voltages at 0x3afa6250, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 68>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_run_with_voltages)
# 
#  84          22 LOAD_CONST               3 (<code object test_run_with_scan_results_provided at 0x3af9e7f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 84>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_run_with_scan_results_provided)
#              28 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_validation_failure at 0x3af9b9b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 63>:
#  63           0 RESUME                   0
# 
#  64           2 LOAD_GLOBAL              1 (NULL + FaultClearingScanSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  65          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + run)
#              44 BUILD_MAP                0
#              46 CALL                     1
#              54 STORE_FAST               2 (result)
# 
#  66          56 LOAD_FAST                2 (result)
#              58 LOAD_ATTR                4 (status)
#              78 STORE_FAST               3 (@py_assert1)
#              80 LOAD_GLOBAL              6 (SkillStatus)
#              90 LOAD_ATTR                8 (FAILED)
#             110 STORE_FAST               4 (@py_assert5)
#             112 LOAD_FAST                3 (@py_assert1)
#             114 LOAD_FAST                4 (@py_assert5)
#             116 COMPARE_OP              40 (==)
#             120 STORE_FAST               5 (@py_assert3)
#             122 LOAD_FAST                5 (@py_assert3)
#             124 POP_JUMP_IF_TRUE       246 (to 618)
#             126 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             136 LOAD_ATTR               12 (_call_reprcompare)
#             156 LOAD_CONST               1 (('==',))
#             158 LOAD_FAST                5 (@py_assert3)
#             160 BUILD_TUPLE              1
#             162 LOAD_CONST               2 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.FAILED\n}',))
#             164 LOAD_FAST                3 (@py_assert1)
#             166 LOAD_FAST                4 (@py_assert5)
#             168 BUILD_TUPLE              2
#             170 CALL                     4
#             178 LOAD_CONST               3 ('result')
#             180 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             190 LOAD_ATTR               16 (locals)
#             210 CALL                     0
#             218 CONTAINS_OP              0
#             220 POP_JUMP_IF_TRUE        21 (to 264)
#             222 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             232 LOAD_ATTR               18 (_should_repr_global_name)
#             252 LOAD_FAST                2 (result)
#             254 CALL                     1
#             262 POP_JUMP_IF_FALSE       21 (to 306)
#         >>  264 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             274 LOAD_ATTR               20 (_saferepr)
#             294 LOAD_FAST                2 (result)
#             296 CALL                     1
#             304 JUMP_FORWARD             1 (to 308)
#         >>  306 LOAD_CONST               3 ('result')
#         >>  308 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             318 LOAD_ATTR               20 (_saferepr)
#             338 LOAD_FAST                3 (@py_assert1)
#             340 CALL                     1
#             348 LOAD_CONST               4 ('SkillStatus')
#             350 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             360 LOAD_ATTR               16 (locals)
#             380 CALL                     0
#             388 CONTAINS_OP              0
#             390 POP_JUMP_IF_TRUE        25 (to 442)
#             392 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             402 LOAD_ATTR               18 (_should_repr_global_name)
#             422 LOAD_GLOBAL              6 (SkillStatus)
#             432 CALL                     1
#             440 POP_JUMP_IF_FALSE       25 (to 492)
#         >>  442 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             452 LOAD_ATTR               20 (_saferepr)
#             472 LOAD_GLOBAL              6 (SkillStatus)
#             482 CALL                     1
#             490 JUMP_FORWARD             1 (to 494)
#         >>  492 LOAD_CONST               4 ('SkillStatus')
#         >>  494 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             504 LOAD_ATTR               20 (_saferepr)
#             524 LOAD_FAST                4 (@py_assert5)
#             526 CALL                     1
#             534 LOAD_CONST               5 (('py0', 'py2', 'py4', 'py6'))
#             536 BUILD_CONST_KEY_MAP      4
#             538 BINARY_OP                6 (%)
#             542 STORE_FAST               6 (@py_format7)
#             544 LOAD_CONST               6 ('assert %(py8)s')
#             546 LOAD_CONST               7 ('py8')
#             548 LOAD_FAST                6 (@py_format7)
#             550 BUILD_MAP                1
#             552 BINARY_OP                6 (%)
#             556 STORE_FAST               7 (@py_format9)
#             558 LOAD_GLOBAL             23 (NULL + AssertionError)
#             568 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             578 LOAD_ATTR               24 (_format_explanation)
#             598 LOAD_FAST                7 (@py_format9)
#             600 CALL                     1
#             608 CALL                     1
#             616 RAISE_VARARGS            1
#         >>  618 LOAD_CONST               0 (None)
#             620 COPY                     1
#             622 STORE_FAST               3 (@py_assert1)
#             624 COPY                     1
#             626 STORE_FAST               5 (@py_assert3)
#             628 STORE_FAST               4 (@py_assert5)
#             630 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_run_with_voltages at 0x3afa6250, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 68>:
#  68           0 RESUME                   0
# 
#  69           2 LOAD_GLOBAL              1 (NULL + FaultClearingScanSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  72          22 LOAD_CONST               1 ('model/test/IEEE3')
# 
#  73          24 BUILD_LIST               0
#              26 LOAD_CONST               2 ((2.7, 2.8, 2.9))
#              28 LIST_EXTEND              1
# 
#  71          30 LOAD_CONST               3 (('rid', 'fe_values'))
#              32 BUILD_CONST_KEY_MAP      2
# 
#  75          34 BUILD_LIST               0
#              36 LOAD_CONST               4 ((1.0, 0.9, 0.8))
#              38 LIST_EXTEND              1
# 
#  76          40 LOAD_CONST               5 ('path')
#              42 LOAD_CONST               6 ('/tmp/fcs_test/')
#              44 BUILD_MAP                1
# 
#  70          46 LOAD_CONST               7 (('model', 'voltages_at_study', 'output'))
#              48 BUILD_CONST_KEY_MAP      3
#              50 STORE_FAST               2 (config)
# 
#  78          52 LOAD_FAST                1 (skill)
#              54 LOAD_ATTR                3 (NULL|self + run)
#              74 LOAD_FAST                2 (config)
#              76 CALL                     1
#              84 STORE_FAST               3 (result)
# 
#  79          86 LOAD_FAST                3 (result)
#              88 LOAD_ATTR                4 (status)
#             108 STORE_FAST               4 (@py_assert1)
#             110 LOAD_GLOBAL              6 (SkillStatus)
#             120 LOAD_ATTR                8 (SUCCESS)
#             140 STORE_FAST               5 (@py_assert5)
#             142 LOAD_FAST                4 (@py_assert1)
#             144 LOAD_FAST                5 (@py_assert5)
#             146 COMPARE_OP              40 (==)
#             150 STORE_FAST               6 (@py_assert3)
#             152 LOAD_FAST                6 (@py_assert3)
#             154 POP_JUMP_IF_TRUE       246 (to 648)
#             156 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             166 LOAD_ATTR               12 (_call_reprcompare)
#             186 LOAD_CONST               8 (('==',))
#             188 LOAD_FAST                6 (@py_assert3)
#             190 BUILD_TUPLE              1
#             192 LOAD_CONST               9 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.SUCCESS\n}',))
#             194 LOAD_FAST                4 (@py_assert1)
#             196 LOAD_FAST                5 (@py_assert5)
#             198 BUILD_TUPLE              2
#             200 CALL                     4
#             208 LOAD_CONST              10 ('result')
#             210 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             220 LOAD_ATTR               16 (locals)
#             240 CALL                     0
#             248 CONTAINS_OP              0
#             250 POP_JUMP_IF_TRUE        21 (to 294)
#             252 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             262 LOAD_ATTR               18 (_should_repr_global_name)
#             282 LOAD_FAST                3 (result)
#             284 CALL                     1
#             292 POP_JUMP_IF_FALSE       21 (to 336)
#         >>  294 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             304 LOAD_ATTR               20 (_saferepr)
#             324 LOAD_FAST                3 (result)
#             326 CALL                     1
#             334 JUMP_FORWARD             1 (to 338)
#         >>  336 LOAD_CONST              10 ('result')
#         >>  338 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             348 LOAD_ATTR               20 (_saferepr)
#             368 LOAD_FAST                4 (@py_assert1)
#             370 CALL                     1
#             378 LOAD_CONST              11 ('SkillStatus')
#             380 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             390 LOAD_ATTR               16 (locals)
#             410 CALL                     0
#             418 CONTAINS_OP              0
#             420 POP_JUMP_IF_TRUE        25 (to 472)
#             422 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             432 LOAD_ATTR               18 (_should_repr_global_name)
#             452 LOAD_GLOBAL              6 (SkillStatus)
#             462 CALL                     1
#             470 POP_JUMP_IF_FALSE       25 (to 522)
#         >>  472 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             482 LOAD_ATTR               20 (_saferepr)
#             502 LOAD_GLOBAL              6 (SkillStatus)
#             512 CALL                     1
#             520 JUMP_FORWARD             1 (to 524)
#         >>  522 LOAD_CONST              11 ('SkillStatus')
#         >>  524 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             534 LOAD_ATTR               20 (_saferepr)
#             554 LOAD_FAST                5 (@py_assert5)
#             556 CALL                     1
#             564 LOAD_CONST              12 (('py0', 'py2', 'py4', 'py6'))
#             566 BUILD_CONST_KEY_MAP      4
#             568 BINARY_OP                6 (%)
#             572 STORE_FAST               7 (@py_format7)
#             574 LOAD_CONST              13 ('assert %(py8)s')
#             576 LOAD_CONST              14 ('py8')
#             578 LOAD_FAST                7 (@py_format7)
#             580 BUILD_MAP                1
#             582 BINARY_OP                6 (%)
#             586 STORE_FAST               8 (@py_format9)
#             588 LOAD_GLOBAL             23 (NULL + AssertionError)
#             598 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             608 LOAD_ATTR               24 (_format_explanation)
#             628 LOAD_FAST                8 (@py_format9)
#             630 CALL                     1
#             638 CALL                     1
#             646 RAISE_VARARGS            1
#         >>  648 LOAD_CONST               0 (None)
#             650 COPY                     1
#             652 STORE_FAST               4 (@py_assert1)
#             654 COPY                     1
#             656 STORE_FAST               6 (@py_assert3)
#             658 STORE_FAST               5 (@py_assert5)
# 
#  80         660 LOAD_FAST                3 (result)
#             662 LOAD_ATTR               26 (data)
#             682 LOAD_CONST              15 ('monotonic_degradation')
#             684 BINARY_SUBSCR
#             688 STORE_FAST               9 (@py_assert0)
#             690 LOAD_CONST              16 (True)
#             692 STORE_FAST               6 (@py_assert3)
#             694 LOAD_FAST                9 (@py_assert0)
#             696 LOAD_FAST                6 (@py_assert3)
#             698 IS_OP                    0
#             700 STORE_FAST              10 (@py_assert2)
#             702 LOAD_FAST               10 (@py_assert2)
#             704 POP_JUMP_IF_TRUE       108 (to 922)
#             706 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             716 LOAD_ATTR               12 (_call_reprcompare)
#             736 LOAD_CONST              17 (('is',))
#             738 LOAD_FAST               10 (@py_assert2)
#             740 BUILD_TUPLE              1
#             742 LOAD_CONST              18 (('%(py1)s is %(py4)s',))
#             744 LOAD_FAST                9 (@py_assert0)
#             746 LOAD_FAST                6 (@py_assert3)
#             748 BUILD_TUPLE              2
#             750 CALL                     4
#             758 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             768 LOAD_ATTR               20 (_saferepr)
#             788 LOAD_FAST                9 (@py_assert0)
#             790 CALL                     1
#             798 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             808 LOAD_ATTR               20 (_saferepr)
#             828 LOAD_FAST                6 (@py_assert3)
#             830 CALL                     1
#             838 LOAD_CONST              19 (('py1', 'py4'))
#             840 BUILD_CONST_KEY_MAP      2
#             842 BINARY_OP                6 (%)
#             846 STORE_FAST              11 (@py_format5)
#             848 LOAD_CONST              20 ('assert %(py6)s')
#             850 LOAD_CONST              21 ('py6')
#             852 LOAD_FAST               11 (@py_format5)
#             854 BUILD_MAP                1
#             856 BINARY_OP                6 (%)
#             860 STORE_FAST               7 (@py_format7)
#             862 LOAD_GLOBAL             23 (NULL + AssertionError)
#             872 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             882 LOAD_ATTR               24 (_format_explanation)
#             902 LOAD_FAST                7 (@py_format7)
#             904 CALL                     1
#             912 CALL                     1
#             920 RAISE_VARARGS            1
#         >>  922 LOAD_CONST               0 (None)
#             924 COPY                     1
#             926 STORE_FAST               9 (@py_assert0)
#             928 COPY                     1
#             930 STORE_FAST              10 (@py_assert2)
#             932 STORE_FAST               6 (@py_assert3)
# 
#  81         934 LOAD_FAST                3 (result)
#             936 LOAD_ATTR               26 (data)
#             956 LOAD_CONST              22 ('study_time')
#             958 BINARY_SUBSCR
#             962 STORE_FAST               9 (@py_assert0)
#             964 LOAD_CONST               0 (None)
#             966 STORE_FAST               6 (@py_assert3)
#             968 LOAD_FAST                9 (@py_assert0)
#             970 LOAD_FAST                6 (@py_assert3)
#             972 IS_OP                    1
#             974 STORE_FAST              10 (@py_assert2)
#             976 LOAD_FAST               10 (@py_assert2)
#             978 POP_JUMP_IF_TRUE       108 (to 1196)
#             980 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             990 LOAD_ATTR               12 (_call_reprcompare)
#            1010 LOAD_CONST              23 (('is not',))
#            1012 LOAD_FAST               10 (@py_assert2)
#            1014 BUILD_TUPLE              1
#            1016 LOAD_CONST              24 (('%(py1)s is not %(py4)s',))
#            1018 LOAD_FAST                9 (@py_assert0)
#            1020 LOAD_FAST                6 (@py_assert3)
#            1022 BUILD_TUPLE              2
#            1024 CALL                     4
#            1032 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1042 LOAD_ATTR               20 (_saferepr)
#            1062 LOAD_FAST                9 (@py_assert0)
#            1064 CALL                     1
#            1072 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1082 LOAD_ATTR               20 (_saferepr)
#            1102 LOAD_FAST                6 (@py_assert3)
#            1104 CALL                     1
#            1112 LOAD_CONST              19 (('py1', 'py4'))
#            1114 BUILD_CONST_KEY_MAP      2
#            1116 BINARY_OP                6 (%)
#            1120 STORE_FAST              11 (@py_format5)
#            1122 LOAD_CONST              20 ('assert %(py6)s')
#            1124 LOAD_CONST              21 ('py6')
#            1126 LOAD_FAST               11 (@py_format5)
#            1128 BUILD_MAP                1
#            1130 BINARY_OP                6 (%)
#            1134 STORE_FAST               7 (@py_format7)
#            1136 LOAD_GLOBAL             23 (NULL + AssertionError)
#            1146 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1156 LOAD_ATTR               24 (_format_explanation)
#            1176 LOAD_FAST                7 (@py_format7)
#            1178 CALL                     1
#            1186 CALL                     1
#            1194 RAISE_VARARGS            1
#         >> 1196 LOAD_CONST               0 (None)
#            1198 COPY                     1
#            1200 STORE_FAST               9 (@py_assert0)
#            1202 COPY                     1
#            1204 STORE_FAST              10 (@py_assert2)
#            1206 STORE_FAST               6 (@py_assert3)
# 
#  82        1208 LOAD_FAST                3 (result)
#            1210 LOAD_ATTR               26 (data)
#            1230 LOAD_CONST              25 ('results')
#            1232 BINARY_SUBSCR
#            1236 STORE_FAST               4 (@py_assert1)
#            1238 LOAD_GLOBAL             29 (NULL + len)
#            1248 LOAD_FAST                4 (@py_assert1)
#            1250 CALL                     1
#            1258 STORE_FAST               6 (@py_assert3)
#            1260 LOAD_CONST              26 (3)
#            1262 STORE_FAST              12 (@py_assert6)
#            1264 LOAD_FAST                6 (@py_assert3)
#            1266 LOAD_FAST               12 (@py_assert6)
#            1268 COMPARE_OP              40 (==)
#            1272 STORE_FAST               5 (@py_assert5)
#            1274 LOAD_FAST                5 (@py_assert5)
#            1276 POP_JUMP_IF_TRUE       201 (to 1680)
#            1278 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1288 LOAD_ATTR               12 (_call_reprcompare)
#            1308 LOAD_CONST               8 (('==',))
#            1310 LOAD_FAST                5 (@py_assert5)
#            1312 BUILD_TUPLE              1
#            1314 LOAD_CONST              27 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',))
#            1316 LOAD_FAST                6 (@py_assert3)
#            1318 LOAD_FAST               12 (@py_assert6)
#            1320 BUILD_TUPLE              2
#            1322 CALL                     4
#            1330 LOAD_CONST              28 ('len')
#            1332 LOAD_GLOBAL             15 (NULL + @py_builtins)
#            1342 LOAD_ATTR               16 (locals)
#            1362 CALL                     0
#            1370 CONTAINS_OP              0
#            1372 POP_JUMP_IF_TRUE        25 (to 1424)
#            1374 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1384 LOAD_ATTR               18 (_should_repr_global_name)
#            1404 LOAD_GLOBAL             28 (len)
#            1414 CALL                     1
#            1422 POP_JUMP_IF_FALSE       25 (to 1474)
#         >> 1424 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1434 LOAD_ATTR               20 (_saferepr)
#            1454 LOAD_GLOBAL             28 (len)
#            1464 CALL                     1
#            1472 JUMP_FORWARD             1 (to 1476)
#         >> 1474 LOAD_CONST              28 ('len')
#         >> 1476 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1486 LOAD_ATTR               20 (_saferepr)
#            1506 LOAD_FAST                4 (@py_assert1)
#            1508 CALL                     1
#            1516 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1526 LOAD_ATTR               20 (_saferepr)
#            1546 LOAD_FAST                6 (@py_assert3)
#            1548 CALL                     1
#            1556 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1566 LOAD_ATTR               20 (_saferepr)
#            1586 LOAD_FAST               12 (@py_assert6)
#            1588 CALL                     1
#            1596 LOAD_CONST              29 (('py0', 'py2', 'py4', 'py7'))
#            1598 BUILD_CONST_KEY_MAP      4
#            1600 BINARY_OP                6 (%)
#            1604 STORE_FAST              13 (@py_format8)
#            1606 LOAD_CONST              30 ('assert %(py9)s')
#            1608 LOAD_CONST              31 ('py9')
#            1610 LOAD_FAST               13 (@py_format8)
#            1612 BUILD_MAP                1
#            1614 BINARY_OP                6 (%)
#            1618 STORE_FAST              14 (@py_format10)
#            1620 LOAD_GLOBAL             23 (NULL + AssertionError)
#            1630 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1640 LOAD_ATTR               24 (_format_explanation)
#            1660 LOAD_FAST               14 (@py_format10)
#            1662 CALL                     1
#            1670 CALL                     1
#            1678 RAISE_VARARGS            1
#         >> 1680 LOAD_CONST               0 (None)
#            1682 COPY                     1
#            1684 STORE_FAST               4 (@py_assert1)
#            1686 COPY                     1
#            1688 STORE_FAST               6 (@py_assert3)
#            1690 COPY                     1
#            1692 STORE_FAST               5 (@py_assert5)
#            1694 STORE_FAST              12 (@py_assert6)
#            1696 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_run_with_scan_results_provided at 0x3af9e7f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_fault_clearing_scan.py", line 84>:
#  84           0 RESUME                   0
# 
#  85           2 LOAD_GLOBAL              1 (NULL + FaultClearingScanSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  87          22 LOAD_CONST               1 ('test')
#              24 BUILD_LIST               0
#              26 LOAD_CONST               2 ((1.0, 2.0, 3.0))
#              28 LIST_EXTEND              1
#              30 LOAD_CONST               3 (('rid', 'fe_values'))
#              32 BUILD_CONST_KEY_MAP      2
# 
#  89          34 LOAD_CONST               4 (1.0)
#              36 LOAD_CONST               4 (1.0)
#              38 LOAD_CONST               5 (9.0)
#              40 LOAD_CONST               6 (('fe', 'clearing_time', 'voltage_at_study'))
#              42 BUILD_CONST_KEY_MAP      3
# 
#  90          44 LOAD_CONST               7 (2.0)
#              46 LOAD_CONST               7 (2.0)
#              48 LOAD_CONST               8 (8.0)
#              50 LOAD_CONST               6 (('fe', 'clearing_time', 'voltage_at_study'))
#              52 BUILD_CONST_KEY_MAP      3
# 
#  91          54 LOAD_CONST               9 (3.0)
#              56 LOAD_CONST               9 (3.0)
#              58 LOAD_CONST              10 (7.5)
#              60 LOAD_CONST               6 (('fe', 'clearing_time', 'voltage_at_study'))
#              62 BUILD_CONST_KEY_MAP      3
# 
#  88          64 BUILD_LIST               3
# 
#  93          66 LOAD_CONST              11 ('path')
#              68 LOAD_CONST              12 ('/tmp/fcs_test2/')
#              70 BUILD_MAP                1
# 
#  86          72 LOAD_CONST              13 (('model', 'scan_results', 'output'))
#              74 BUILD_CONST_KEY_MAP      3
#              76 STORE_FAST               2 (config)
# 
#  95          78 LOAD_FAST                1 (skill)
#              80 LOAD_ATTR                3 (NULL|self + run)
#             100 LOAD_FAST                2 (config)
#             102 CALL                     1
#             110 STORE_FAST               3 (result)
# 
#  96         112 LOAD_FAST                3 (result)
#             114 LOAD_ATTR                4 (status)
#             134 STORE_FAST               4 (@py_assert1)
#             136 LOAD_GLOBAL              6 (SkillStatus)
#             146 LOAD_ATTR                8 (SUCCESS)
#             166 STORE_FAST               5 (@py_assert5)
#             168 LOAD_FAST                4 (@py_assert1)
#             170 LOAD_FAST                5 (@py_assert5)
#             172 COMPARE_OP              40 (==)
#             176 STORE_FAST               6 (@py_assert3)
#             178 LOAD_FAST                6 (@py_assert3)
#             180 POP_JUMP_IF_TRUE       246 (to 674)
#             182 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             192 LOAD_ATTR               12 (_call_reprcompare)
#             212 LOAD_CONST              14 (('==',))
#             214 LOAD_FAST                6 (@py_assert3)
#             216 BUILD_TUPLE              1
#             218 LOAD_CONST              15 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.SUCCESS\n}',))
#             220 LOAD_FAST                4 (@py_assert1)
#             222 LOAD_FAST                5 (@py_assert5)
#             224 BUILD_TUPLE              2
#             226 CALL                     4
#             234 LOAD_CONST              16 ('result')
#             236 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             246 LOAD_ATTR               16 (locals)
#             266 CALL                     0
#             274 CONTAINS_OP              0
#             276 POP_JUMP_IF_TRUE        21 (to 320)
#             278 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             288 LOAD_ATTR               18 (_should_repr_global_name)
#             308 LOAD_FAST                3 (result)
#             310 CALL                     1
#             318 POP_JUMP_IF_FALSE       21 (to 362)
#         >>  320 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             330 LOAD_ATTR               20 (_saferepr)
#             350 LOAD_FAST                3 (result)
#             352 CALL                     1
#             360 JUMP_FORWARD             1 (to 364)
#         >>  362 LOAD_CONST              16 ('result')
#         >>  364 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             374 LOAD_ATTR               20 (_saferepr)
#             394 LOAD_FAST                4 (@py_assert1)
#             396 CALL                     1
#             404 LOAD_CONST              17 ('SkillStatus')
#             406 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             416 LOAD_ATTR               16 (locals)
#             436 CALL                     0
#             444 CONTAINS_OP              0
#             446 POP_JUMP_IF_TRUE        25 (to 498)
#             448 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             458 LOAD_ATTR               18 (_should_repr_global_name)
#             478 LOAD_GLOBAL              6 (SkillStatus)
#             488 CALL                     1
#             496 POP_JUMP_IF_FALSE       25 (to 548)
#         >>  498 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             508 LOAD_ATTR               20 (_saferepr)
#             528 LOAD_GLOBAL              6 (SkillStatus)
#             538 CALL                     1
#             546 JUMP_FORWARD             1 (to 550)
#         >>  548 LOAD_CONST              17 ('SkillStatus')
#         >>  550 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             560 LOAD_ATTR               20 (_saferepr)
#             580 LOAD_FAST                5 (@py_assert5)
#             582 CALL                     1
#             590 LOAD_CONST              18 (('py0', 'py2', 'py4', 'py6'))
#             592 BUILD_CONST_KEY_MAP      4
#             594 BINARY_OP                6 (%)
#             598 STORE_FAST               7 (@py_format7)
#             600 LOAD_CONST              19 ('assert %(py8)s')
#             602 LOAD_CONST              20 ('py8')
#             604 LOAD_FAST                7 (@py_format7)
#             606 BUILD_MAP                1
#             608 BINARY_OP                6 (%)
#             612 STORE_FAST               8 (@py_format9)
#             614 LOAD_GLOBAL             23 (NULL + AssertionError)
#             624 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             634 LOAD_ATTR               24 (_format_explanation)
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
#  97         686 LOAD_FAST                3 (result)
#             688 LOAD_ATTR               26 (metrics)
#             708 LOAD_CONST              21 ('scan_count')
#             710 BINARY_SUBSCR
#             714 STORE_FAST               9 (@py_assert0)
#             716 LOAD_CONST              22 (3)
#             718 STORE_FAST               6 (@py_assert3)
#             720 LOAD_FAST                9 (@py_assert0)
#             722 LOAD_FAST                6 (@py_assert3)
#             724 COMPARE_OP              40 (==)
#             728 STORE_FAST              10 (@py_assert2)
#             730 LOAD_FAST               10 (@py_assert2)
#             732 POP_JUMP_IF_TRUE       108 (to 950)
#             734 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             744 LOAD_ATTR               12 (_call_reprcompare)
#             764 LOAD_CONST              14 (('==',))
#             766 LOAD_FAST               10 (@py_assert2)
#             768 BUILD_TUPLE              1
#             770 LOAD_CONST              23 (('%(py1)s == %(py4)s',))
#             772 LOAD_FAST                9 (@py_assert0)
#             774 LOAD_FAST                6 (@py_assert3)
#             776 BUILD_TUPLE              2
#             778 CALL                     4
#             786 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             796 LOAD_ATTR               20 (_saferepr)
#             816 LOAD_FAST                9 (@py_assert0)
#             818 CALL                     1
#             826 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             836 LOAD_ATTR               20 (_saferepr)
#             856 LOAD_FAST                6 (@py_assert3)
#             858 CALL                     1
#             866 LOAD_CONST              24 (('py1', 'py4'))
#             868 BUILD_CONST_KEY_MAP      2
#             870 BINARY_OP                6 (%)
#             874 STORE_FAST              11 (@py_format5)
#             876 LOAD_CONST              25 ('assert %(py6)s')
#             878 LOAD_CONST              26 ('py6')
#             880 LOAD_FAST               11 (@py_format5)
#             882 BUILD_MAP                1
#             884 BINARY_OP                6 (%)
#             888 STORE_FAST               7 (@py_format7)
#             890 LOAD_GLOBAL             23 (NULL + AssertionError)
#             900 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             910 LOAD_ATTR               24 (_format_explanation)
#             930 LOAD_FAST                7 (@py_format7)
#             932 CALL                     1
#             940 CALL                     1
#             948 RAISE_VARARGS            1
#         >>  950 LOAD_CONST               0 (None)
#             952 COPY                     1
#             954 STORE_FAST               9 (@py_assert0)
#             956 COPY                     1
#             958 STORE_FAST              10 (@py_assert2)
#             960 STORE_FAST               6 (@py_assert3)
#             962 RETURN_CONST             0 (None)
# 