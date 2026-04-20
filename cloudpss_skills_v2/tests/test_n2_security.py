# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/__pycache__/test_n2_security.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


def TestN2Validation():
    """TestN2Validation"""
pass  # TODO: restore


def TestN2Scenarios():
    """TestN2Scenarios"""
pass  # TODO: restore


def TestN2Assessment():
    """TestN2Assessment"""
pass  # TODO: restore


def TestN2ContingencyResult():
    """TestN2ContingencyResult"""
pass  # TODO: restore


def TestN2Run():
    """TestN2Run"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('Tests for N2SecuritySkill v2.')
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
#              42 LOAD_CONST               3 (('N2SecuritySkill', 'N2ContingencyResult'))
#              44 IMPORT_NAME              8 (cloudpss_skills_v2.skills.n2_security)
#              46 IMPORT_FROM              9 (N2SecuritySkill)
#              48 STORE_NAME               9 (N2SecuritySkill)
#              50 IMPORT_FROM             10 (N2ContingencyResult)
#              52 STORE_NAME              10 (N2ContingencyResult)
#              54 POP_TOP
# 
#   7          56 PUSH_NULL
#              58 LOAD_BUILD_CLASS
#              60 LOAD_CONST               4 (<code object TestN2Validation at 0x73cd945fedb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 7>)
#              62 MAKE_FUNCTION            0
#              64 LOAD_CONST               5 ('TestN2Validation')
#              66 CALL                     2
#              74 STORE_NAME              11 (TestN2Validation)
# 
#  33          76 PUSH_NULL
#              78 LOAD_BUILD_CLASS
#              80 LOAD_CONST               6 (<code object TestN2Scenarios at 0x73cd945ff050, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 33>)
#              82 MAKE_FUNCTION            0
#              84 LOAD_CONST               7 ('TestN2Scenarios')
#              86 CALL                     2
#              94 STORE_NAME              12 (TestN2Scenarios)
# 
#  60          96 PUSH_NULL
#              98 LOAD_BUILD_CLASS
#             100 LOAD_CONST               8 (<code object TestN2Assessment at 0x73cd945fe250, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 60>)
#             102 MAKE_FUNCTION            0
#             104 LOAD_CONST               9 ('TestN2Assessment')
#             106 CALL                     2
#             114 STORE_NAME              13 (TestN2Assessment)
# 
#  84         116 PUSH_NULL
#             118 LOAD_BUILD_CLASS
#             120 LOAD_CONST              10 (<code object TestN2ContingencyResult at 0x73cd945febf0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 84>)
#             122 MAKE_FUNCTION            0
#             124 LOAD_CONST              11 ('TestN2ContingencyResult')
#             126 CALL                     2
#             134 STORE_NAME              14 (TestN2ContingencyResult)
# 
#  99         136 PUSH_NULL
#             138 LOAD_BUILD_CLASS
#             140 LOAD_CONST              12 (<code object TestN2Run at 0x73cd945fecd0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 99>)
#             142 MAKE_FUNCTION            0
#             144 LOAD_CONST              13 ('TestN2Run')
#             146 CALL                     2
#             154 STORE_NAME              15 (TestN2Run)
#             156 RETURN_CONST             2 (None)
# 
# Disassembly of <code object TestN2Validation at 0x73cd945fedb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 7>:
#   7           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestN2Validation')
#               8 STORE_NAME               2 (__qualname__)
# 
#   8          10 LOAD_CONST               1 (<code object test_validate_missing_model at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 8>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_validate_missing_model)
# 
#  13          16 LOAD_CONST               2 (<code object test_validate_voltage_range_invalid at 0x3afa5260, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 13>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_validate_voltage_range_invalid)
# 
#  23          22 LOAD_CONST               3 (<code object test_validate_valid_config at 0x3af0c6d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 23>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_validate_valid_config)
#              28 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_validate_missing_model at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 8>:
#   8           0 RESUME                   0
# 
#   9           2 LOAD_GLOBAL              1 (NULL + N2SecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  10          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + validate)
#              44 BUILD_MAP                0
#              46 CALL                     1
#              54 UNPACK_SEQUENCE          2
#              58 STORE_FAST               2 (valid)
#              60 STORE_FAST               3 (errors)
# 
#  11          62 LOAD_CONST               1 (False)
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
#             392 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_voltage_range_invalid at 0x3afa5260, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 13>:
#  13           0 RESUME                   0
# 
#  14           2 LOAD_GLOBAL              1 (NULL + N2SecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  16          22 LOAD_CONST               1 ('rid')
#              24 LOAD_CONST               2 ('test')
#              26 BUILD_MAP                1
# 
#  17          28 LOAD_CONST               3 (1.05)
#              30 LOAD_CONST               4 (0.95)
#              32 LOAD_CONST               5 (('voltage_min', 'voltage_max'))
#              34 BUILD_CONST_KEY_MAP      2
# 
#  15          36 LOAD_CONST               6 (('model', 'analysis'))
#              38 BUILD_CONST_KEY_MAP      2
#              40 STORE_FAST               2 (config)
# 
#  19          42 LOAD_FAST                1 (skill)
#              44 LOAD_ATTR                3 (NULL|self + validate)
#              64 LOAD_FAST                2 (config)
#              66 CALL                     1
#              74 UNPACK_SEQUENCE          2
#              78 STORE_FAST               3 (valid)
#              80 STORE_FAST               4 (errors)
# 
#  20          82 LOAD_CONST               7 (False)
#              84 STORE_FAST               5 (@py_assert2)
#              86 LOAD_FAST                3 (valid)
#              88 LOAD_FAST                5 (@py_assert2)
#              90 IS_OP                    0
#              92 STORE_FAST               6 (@py_assert1)
#              94 LOAD_FAST                6 (@py_assert1)
#              96 POP_JUMP_IF_TRUE       153 (to 404)
#              98 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             108 LOAD_ATTR                6 (_call_reprcompare)
#             128 LOAD_CONST               8 (('is',))
#             130 LOAD_FAST                6 (@py_assert1)
#             132 BUILD_TUPLE              1
#             134 LOAD_CONST               9 (('%(py0)s is %(py3)s',))
#             136 LOAD_FAST                3 (valid)
#             138 LOAD_FAST                5 (@py_assert2)
#             140 BUILD_TUPLE              2
#             142 CALL                     4
#             150 LOAD_CONST              10 ('valid')
#             152 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             162 LOAD_ATTR               10 (locals)
#             182 CALL                     0
#             190 CONTAINS_OP              0
#             192 POP_JUMP_IF_TRUE        21 (to 236)
#             194 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             204 LOAD_ATTR               12 (_should_repr_global_name)
#             224 LOAD_FAST                3 (valid)
#             226 CALL                     1
#             234 POP_JUMP_IF_FALSE       21 (to 278)
#         >>  236 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             246 LOAD_ATTR               14 (_saferepr)
#             266 LOAD_FAST                3 (valid)
#             268 CALL                     1
#             276 JUMP_FORWARD             1 (to 280)
#         >>  278 LOAD_CONST              10 ('valid')
#         >>  280 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             290 LOAD_ATTR               14 (_saferepr)
#             310 LOAD_FAST                5 (@py_assert2)
#             312 CALL                     1
#             320 LOAD_CONST              11 (('py0', 'py3'))
#             322 BUILD_CONST_KEY_MAP      2
#             324 BINARY_OP                6 (%)
#             328 STORE_FAST               7 (@py_format4)
#             330 LOAD_CONST              12 ('assert %(py5)s')
#             332 LOAD_CONST              13 ('py5')
#             334 LOAD_FAST                7 (@py_format4)
#             336 BUILD_MAP                1
#             338 BINARY_OP                6 (%)
#             342 STORE_FAST               8 (@py_format6)
#             344 LOAD_GLOBAL             17 (NULL + AssertionError)
#             354 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             364 LOAD_ATTR               18 (_format_explanation)
#             384 LOAD_FAST                8 (@py_format6)
#             386 CALL                     1
#             394 CALL                     1
#             402 RAISE_VARARGS            1
#         >>  404 LOAD_CONST               0 (None)
#             406 COPY                     1
#             408 STORE_FAST               6 (@py_assert1)
#             410 STORE_FAST               5 (@py_assert2)
# 
#  21         412 LOAD_CONST              14 (<code object <genexpr> at 0x73cd93b06790, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 21>)
#             414 MAKE_FUNCTION            0
#             416 LOAD_FAST                4 (errors)
#             418 GET_ITER
#             420 CALL                     0
#             428 STORE_FAST               6 (@py_assert1)
#             430 LOAD_GLOBAL             21 (NULL + any)
#             440 LOAD_FAST                6 (@py_assert1)
#             442 CALL                     1
#             450 STORE_FAST               9 (@py_assert3)
#             452 LOAD_FAST                9 (@py_assert3)
#             454 POP_JUMP_IF_TRUE       149 (to 754)
#             456 LOAD_CONST              15 ('assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}')
#             458 LOAD_CONST              16 ('any')
#             460 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             470 LOAD_ATTR               10 (locals)
#             490 CALL                     0
#             498 CONTAINS_OP              0
#             500 POP_JUMP_IF_TRUE        25 (to 552)
#             502 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             512 LOAD_ATTR               12 (_should_repr_global_name)
#             532 LOAD_GLOBAL             20 (any)
#             542 CALL                     1
#             550 POP_JUMP_IF_FALSE       25 (to 602)
#         >>  552 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             562 LOAD_ATTR               14 (_saferepr)
#             582 LOAD_GLOBAL             20 (any)
#             592 CALL                     1
#             600 JUMP_FORWARD             1 (to 604)
#         >>  602 LOAD_CONST              16 ('any')
#         >>  604 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             614 LOAD_ATTR               14 (_saferepr)
#             634 LOAD_FAST                6 (@py_assert1)
#             636 CALL                     1
#             644 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             654 LOAD_ATTR               14 (_saferepr)
#             674 LOAD_FAST                9 (@py_assert3)
#             676 CALL                     1
#             684 LOAD_CONST              17 (('py0', 'py2', 'py4'))
#             686 BUILD_CONST_KEY_MAP      3
#             688 BINARY_OP                6 (%)
#             692 STORE_FAST              10 (@py_format5)
#             694 LOAD_GLOBAL             17 (NULL + AssertionError)
#             704 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             714 LOAD_ATTR               18 (_format_explanation)
#             734 LOAD_FAST               10 (@py_format5)
#             736 CALL                     1
#             744 CALL                     1
#             752 RAISE_VARARGS            1
#         >>  754 LOAD_CONST               0 (None)
#             756 COPY                     1
#             758 STORE_FAST               6 (@py_assert1)
#             760 STORE_FAST               9 (@py_assert3)
#             762 RETURN_CONST             0 (None)
# 
# Disassembly of <code object <genexpr> at 0x73cd93b06790, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 21>:
#  21           0 RETURN_GENERATOR
#               2 POP_TOP
#               4 RESUME                   0
#               6 LOAD_FAST                0 (.0)
#         >>    8 FOR_ITER                 8 (to 28)
#              12 STORE_FAST               1 (e)
#              14 LOAD_CONST               0 ('voltage_min')
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
# Disassembly of <code object test_validate_valid_config at 0x3af0c6d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 23>:
#  23           0 RESUME                   0
# 
#  24           2 LOAD_GLOBAL              1 (NULL + N2SecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  26          22 LOAD_CONST               1 ('rid')
#              24 LOAD_CONST               2 ('test')
#              26 BUILD_MAP                1
# 
#  27          28 LOAD_CONST               3 (0.95)
#              30 LOAD_CONST               4 (1.05)
#              32 LOAD_CONST               5 (('voltage_min', 'voltage_max'))
#              34 BUILD_CONST_KEY_MAP      2
# 
#  25          36 LOAD_CONST               6 (('model', 'analysis'))
#              38 BUILD_CONST_KEY_MAP      2
#              40 STORE_FAST               2 (config)
# 
#  29          42 LOAD_FAST                1 (skill)
#              44 LOAD_ATTR                3 (NULL|self + validate)
#              64 LOAD_FAST                2 (config)
#              66 CALL                     1
#              74 UNPACK_SEQUENCE          2
#              78 STORE_FAST               3 (valid)
#              80 STORE_FAST               4 (errors)
# 
#  30          82 LOAD_CONST               7 (True)
#              84 STORE_FAST               5 (@py_assert2)
#              86 LOAD_FAST                3 (valid)
#              88 LOAD_FAST                5 (@py_assert2)
#              90 IS_OP                    0
#              92 STORE_FAST               6 (@py_assert1)
#              94 LOAD_FAST                6 (@py_assert1)
#              96 POP_JUMP_IF_TRUE       153 (to 404)
#              98 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             108 LOAD_ATTR                6 (_call_reprcompare)
#             128 LOAD_CONST               8 (('is',))
#             130 LOAD_FAST                6 (@py_assert1)
#             132 BUILD_TUPLE              1
#             134 LOAD_CONST               9 (('%(py0)s is %(py3)s',))
#             136 LOAD_FAST                3 (valid)
#             138 LOAD_FAST                5 (@py_assert2)
#             140 BUILD_TUPLE              2
#             142 CALL                     4
#             150 LOAD_CONST              10 ('valid')
#             152 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             162 LOAD_ATTR               10 (locals)
#             182 CALL                     0
#             190 CONTAINS_OP              0
#             192 POP_JUMP_IF_TRUE        21 (to 236)
#             194 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             204 LOAD_ATTR               12 (_should_repr_global_name)
#             224 LOAD_FAST                3 (valid)
#             226 CALL                     1
#             234 POP_JUMP_IF_FALSE       21 (to 278)
#         >>  236 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             246 LOAD_ATTR               14 (_saferepr)
#             266 LOAD_FAST                3 (valid)
#             268 CALL                     1
#             276 JUMP_FORWARD             1 (to 280)
#         >>  278 LOAD_CONST              10 ('valid')
#         >>  280 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             290 LOAD_ATTR               14 (_saferepr)
#             310 LOAD_FAST                5 (@py_assert2)
#             312 CALL                     1
#             320 LOAD_CONST              11 (('py0', 'py3'))
#             322 BUILD_CONST_KEY_MAP      2
#             324 BINARY_OP                6 (%)
#             328 STORE_FAST               7 (@py_format4)
#             330 LOAD_CONST              12 ('assert %(py5)s')
#             332 LOAD_CONST              13 ('py5')
#             334 LOAD_FAST                7 (@py_format4)
#             336 BUILD_MAP                1
#             338 BINARY_OP                6 (%)
#             342 STORE_FAST               8 (@py_format6)
#             344 LOAD_GLOBAL             17 (NULL + AssertionError)
#             354 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             364 LOAD_ATTR               18 (_format_explanation)
#             384 LOAD_FAST                8 (@py_format6)
#             386 CALL                     1
#             394 CALL                     1
#             402 RAISE_VARARGS            1
#         >>  404 LOAD_CONST               0 (None)
#             406 COPY                     1
#             408 STORE_FAST               6 (@py_assert1)
#             410 STORE_FAST               5 (@py_assert2)
#             412 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestN2Scenarios at 0x73cd945ff050, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 33>:
#  33           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestN2Scenarios')
#               8 STORE_NAME               2 (__qualname__)
# 
#  34          10 LOAD_CONST               1 (<code object test_generate_n2_scenarios_from_branches at 0x3afa0aa0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 34>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_generate_n2_scenarios_from_branches)
# 
#  45          16 LOAD_CONST               2 (<code object test_generate_n2_scenarios_with_limit at 0x3af3a2f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 45>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_generate_n2_scenarios_with_limit)
# 
#  51          22 LOAD_CONST               3 (<code object test_generate_n2_scenarios_with_pairs at 0x3afa23c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 51>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_generate_n2_scenarios_with_pairs)
#              28 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_generate_n2_scenarios_from_branches at 0x3afa0aa0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 34>:
#  34           0 RESUME                   0
# 
#  35           2 LOAD_GLOBAL              1 (NULL + N2SecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  37          22 LOAD_CONST               1 ('L1')
#              24 LOAD_CONST               2 ('Line1')
#              26 LOAD_CONST               3 (('id', 'name'))
#              28 BUILD_CONST_KEY_MAP      2
# 
#  38          30 LOAD_CONST               4 ('L2')
#              32 LOAD_CONST               5 ('Line2')
#              34 LOAD_CONST               3 (('id', 'name'))
#              36 BUILD_CONST_KEY_MAP      2
# 
#  39          38 LOAD_CONST               6 ('L3')
#              40 LOAD_CONST               7 ('Line3')
#              42 LOAD_CONST               3 (('id', 'name'))
#              44 BUILD_CONST_KEY_MAP      2
# 
#  40          46 LOAD_CONST               8 ('L4')
#              48 LOAD_CONST               9 ('Line4')
#              50 LOAD_CONST               3 (('id', 'name'))
#              52 BUILD_CONST_KEY_MAP      2
# 
#  36          54 BUILD_LIST               4
#              56 STORE_FAST               2 (branches)
# 
#  42          58 LOAD_FAST                1 (skill)
#              60 LOAD_ATTR                3 (NULL|self + _generate_n2_scenarios)
#              80 LOAD_FAST                2 (branches)
#              82 BUILD_MAP                0
#              84 CALL                     2
#              92 STORE_FAST               3 (scenarios)
# 
#  43          94 LOAD_GLOBAL              5 (NULL + len)
#             104 LOAD_FAST                3 (scenarios)
#             106 CALL                     1
#             114 STORE_FAST               4 (@py_assert2)
#             116 LOAD_CONST              10 (6)
#             118 STORE_FAST               5 (@py_assert5)
#             120 LOAD_FAST                4 (@py_assert2)
#             122 LOAD_FAST                5 (@py_assert5)
#             124 COMPARE_OP              40 (==)
#             128 STORE_FAST               6 (@py_assert4)
#             130 LOAD_FAST                6 (@py_assert4)
#             132 POP_JUMP_IF_TRUE       246 (to 626)
#             134 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             144 LOAD_ATTR                8 (_call_reprcompare)
#             164 LOAD_CONST              11 (('==',))
#             166 LOAD_FAST                6 (@py_assert4)
#             168 BUILD_TUPLE              1
#             170 LOAD_CONST              12 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             172 LOAD_FAST                4 (@py_assert2)
#             174 LOAD_FAST                5 (@py_assert5)
#             176 BUILD_TUPLE              2
#             178 CALL                     4
#             186 LOAD_CONST              13 ('len')
#             188 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             198 LOAD_ATTR               12 (locals)
#             218 CALL                     0
#             226 CONTAINS_OP              0
#             228 POP_JUMP_IF_TRUE        25 (to 280)
#             230 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             240 LOAD_ATTR               14 (_should_repr_global_name)
#             260 LOAD_GLOBAL              4 (len)
#             270 CALL                     1
#             278 POP_JUMP_IF_FALSE       25 (to 330)
#         >>  280 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             290 LOAD_ATTR               16 (_saferepr)
#             310 LOAD_GLOBAL              4 (len)
#             320 CALL                     1
#             328 JUMP_FORWARD             1 (to 332)
#         >>  330 LOAD_CONST              13 ('len')
#         >>  332 LOAD_CONST              14 ('scenarios')
#             334 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             344 LOAD_ATTR               12 (locals)
#             364 CALL                     0
#             372 CONTAINS_OP              0
#             374 POP_JUMP_IF_TRUE        21 (to 418)
#             376 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             386 LOAD_ATTR               14 (_should_repr_global_name)
#             406 LOAD_FAST                3 (scenarios)
#             408 CALL                     1
#             416 POP_JUMP_IF_FALSE       21 (to 460)
#         >>  418 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             428 LOAD_ATTR               16 (_saferepr)
#             448 LOAD_FAST                3 (scenarios)
#             450 CALL                     1
#             458 JUMP_FORWARD             1 (to 462)
#         >>  460 LOAD_CONST              14 ('scenarios')
#         >>  462 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             472 LOAD_ATTR               16 (_saferepr)
#             492 LOAD_FAST                4 (@py_assert2)
#             494 CALL                     1
#             502 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             512 LOAD_ATTR               16 (_saferepr)
#             532 LOAD_FAST                5 (@py_assert5)
#             534 CALL                     1
#             542 LOAD_CONST              15 (('py0', 'py1', 'py3', 'py6'))
#             544 BUILD_CONST_KEY_MAP      4
#             546 BINARY_OP                6 (%)
#             550 STORE_FAST               7 (@py_format7)
#             552 LOAD_CONST              16 ('assert %(py8)s')
#             554 LOAD_CONST              17 ('py8')
#             556 LOAD_FAST                7 (@py_format7)
#             558 BUILD_MAP                1
#             560 BINARY_OP                6 (%)
#             564 STORE_FAST               8 (@py_format9)
#             566 LOAD_GLOBAL             19 (NULL + AssertionError)
#             576 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             586 LOAD_ATTR               20 (_format_explanation)
#             606 LOAD_FAST                8 (@py_format9)
#             608 CALL                     1
#             616 CALL                     1
#             624 RAISE_VARARGS            1
#         >>  626 LOAD_CONST               0 (None)
#             628 COPY                     1
#             630 STORE_FAST               4 (@py_assert2)
#             632 COPY                     1
#             634 STORE_FAST               6 (@py_assert4)
#             636 STORE_FAST               5 (@py_assert5)
#             638 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_generate_n2_scenarios_with_limit at 0x3af3a2f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 45>:
#  45           0 RESUME                   0
# 
#  46           2 LOAD_GLOBAL              1 (NULL + N2SecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  47          22 LOAD_GLOBAL              3 (NULL + range)
#              32 LOAD_CONST               1 (6)
#              34 CALL                     1
#              42 GET_ITER
#              44 LOAD_FAST_AND_CLEAR      2 (i)
#              46 SWAP                     2
#              48 BUILD_LIST               0
#              50 SWAP                     2
#         >>   52 FOR_ITER                13 (to 82)
#              56 STORE_FAST               2 (i)
#              58 LOAD_CONST               2 ('L')
#              60 LOAD_FAST                2 (i)
#              62 FORMAT_VALUE             0
#              64 BUILD_STRING             2
#              66 LOAD_CONST               3 ('Line')
#              68 LOAD_FAST                2 (i)
#              70 FORMAT_VALUE             0
#              72 BUILD_STRING             2
#              74 LOAD_CONST               4 (('id', 'name'))
#              76 BUILD_CONST_KEY_MAP      2
#              78 LIST_APPEND              2
#              80 JUMP_BACKWARD           15 (to 52)
#         >>   82 END_FOR
#              84 STORE_FAST               3 (branches)
#              86 STORE_FAST               2 (i)
# 
#  48          88 LOAD_FAST                1 (skill)
#              90 LOAD_ATTR                5 (NULL|self + _generate_n2_scenarios)
#             110 LOAD_FAST                3 (branches)
#             112 LOAD_CONST               5 ('max_combinations')
#             114 LOAD_CONST               6 (3)
#             116 BUILD_MAP                1
#             118 CALL                     2
#             126 STORE_FAST               4 (scenarios)
# 
#  49         128 LOAD_GLOBAL              7 (NULL + len)
#             138 LOAD_FAST                4 (scenarios)
#             140 CALL                     1
#             148 STORE_FAST               5 (@py_assert2)
#             150 LOAD_CONST               6 (3)
#             152 STORE_FAST               6 (@py_assert5)
#             154 LOAD_FAST                5 (@py_assert2)
#             156 LOAD_FAST                6 (@py_assert5)
#             158 COMPARE_OP              40 (==)
#             162 STORE_FAST               7 (@py_assert4)
#             164 LOAD_FAST                7 (@py_assert4)
#             166 POP_JUMP_IF_TRUE       246 (to 660)
#             168 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             178 LOAD_ATTR               10 (_call_reprcompare)
#             198 LOAD_CONST               7 (('==',))
#             200 LOAD_FAST                7 (@py_assert4)
#             202 BUILD_TUPLE              1
#             204 LOAD_CONST               8 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             206 LOAD_FAST                5 (@py_assert2)
#             208 LOAD_FAST                6 (@py_assert5)
#             210 BUILD_TUPLE              2
#             212 CALL                     4
#             220 LOAD_CONST               9 ('len')
#             222 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             232 LOAD_ATTR               14 (locals)
#             252 CALL                     0
#             260 CONTAINS_OP              0
#             262 POP_JUMP_IF_TRUE        25 (to 314)
#             264 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             274 LOAD_ATTR               16 (_should_repr_global_name)
#             294 LOAD_GLOBAL              6 (len)
#             304 CALL                     1
#             312 POP_JUMP_IF_FALSE       25 (to 364)
#         >>  314 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             324 LOAD_ATTR               18 (_saferepr)
#             344 LOAD_GLOBAL              6 (len)
#             354 CALL                     1
#             362 JUMP_FORWARD             1 (to 366)
#         >>  364 LOAD_CONST               9 ('len')
#         >>  366 LOAD_CONST              10 ('scenarios')
#             368 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             378 LOAD_ATTR               14 (locals)
#             398 CALL                     0
#             406 CONTAINS_OP              0
#             408 POP_JUMP_IF_TRUE        21 (to 452)
#             410 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             420 LOAD_ATTR               16 (_should_repr_global_name)
#             440 LOAD_FAST                4 (scenarios)
#             442 CALL                     1
#             450 POP_JUMP_IF_FALSE       21 (to 494)
#         >>  452 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             462 LOAD_ATTR               18 (_saferepr)
#             482 LOAD_FAST                4 (scenarios)
#             484 CALL                     1
#             492 JUMP_FORWARD             1 (to 496)
#         >>  494 LOAD_CONST              10 ('scenarios')
#         >>  496 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             506 LOAD_ATTR               18 (_saferepr)
#             526 LOAD_FAST                5 (@py_assert2)
#             528 CALL                     1
#             536 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             546 LOAD_ATTR               18 (_saferepr)
#             566 LOAD_FAST                6 (@py_assert5)
#             568 CALL                     1
#             576 LOAD_CONST              11 (('py0', 'py1', 'py3', 'py6'))
#             578 BUILD_CONST_KEY_MAP      4
#             580 BINARY_OP                6 (%)
#             584 STORE_FAST               8 (@py_format7)
#             586 LOAD_CONST              12 ('assert %(py8)s')
#             588 LOAD_CONST              13 ('py8')
#             590 LOAD_FAST                8 (@py_format7)
#             592 BUILD_MAP                1
#             594 BINARY_OP                6 (%)
#             598 STORE_FAST               9 (@py_format9)
#             600 LOAD_GLOBAL             21 (NULL + AssertionError)
#             610 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             620 LOAD_ATTR               22 (_format_explanation)
#             640 LOAD_FAST                9 (@py_format9)
#             642 CALL                     1
#             650 CALL                     1
#             658 RAISE_VARARGS            1
#         >>  660 LOAD_CONST               0 (None)
#             662 COPY                     1
#             664 STORE_FAST               5 (@py_assert2)
#             666 COPY                     1
#             668 STORE_FAST               7 (@py_assert4)
#             670 STORE_FAST               6 (@py_assert5)
#             672 RETURN_CONST             0 (None)
#         >>  674 SWAP                     2
#             676 POP_TOP
# 
#  47         678 SWAP                     2
#             680 STORE_FAST               2 (i)
#             682 RERAISE                  0
# ExceptionTable:
#   48 to 82 -> 674 [2]
# 
# Disassembly of <code object test_generate_n2_scenarios_with_pairs at 0x3afa23c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 51>:
#  51           0 RESUME                   0
# 
#  52           2 LOAD_GLOBAL              1 (NULL + N2SecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  53          22 LOAD_CONST               1 ('L1')
#              24 LOAD_CONST               2 ('Line1')
#              26 LOAD_CONST               3 (('id', 'name'))
#              28 BUILD_CONST_KEY_MAP      2
#              30 LOAD_CONST               4 ('L2')
#              32 LOAD_CONST               5 ('Line2')
#              34 LOAD_CONST               3 (('id', 'name'))
#              36 BUILD_CONST_KEY_MAP      2
#              38 BUILD_LIST               2
#              40 STORE_FAST               2 (branches)
# 
#  54          42 LOAD_FAST                1 (skill)
#              44 LOAD_ATTR                3 (NULL|self + _generate_n2_scenarios)
# 
#  55          64 LOAD_FAST                2 (branches)
#              66 LOAD_CONST               6 ('branch_pairs')
#              68 LOAD_CONST               2 ('Line1')
#              70 LOAD_CONST               5 ('Line2')
#              72 BUILD_LIST               2
#              74 BUILD_LIST               1
#              76 BUILD_MAP                1
# 
#  54          78 CALL                     2
#              86 STORE_FAST               3 (scenarios)
# 
#  57          88 LOAD_GLOBAL              5 (NULL + len)
#              98 LOAD_FAST                3 (scenarios)
#             100 CALL                     1
#             108 STORE_FAST               4 (@py_assert2)
#             110 LOAD_CONST               7 (1)
#             112 STORE_FAST               5 (@py_assert5)
#             114 LOAD_FAST                4 (@py_assert2)
#             116 LOAD_FAST                5 (@py_assert5)
#             118 COMPARE_OP              40 (==)
#             122 STORE_FAST               6 (@py_assert4)
#             124 LOAD_FAST                6 (@py_assert4)
#             126 POP_JUMP_IF_TRUE       246 (to 620)
#             128 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             138 LOAD_ATTR                8 (_call_reprcompare)
#             158 LOAD_CONST               8 (('==',))
#             160 LOAD_FAST                6 (@py_assert4)
#             162 BUILD_TUPLE              1
#             164 LOAD_CONST               9 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             166 LOAD_FAST                4 (@py_assert2)
#             168 LOAD_FAST                5 (@py_assert5)
#             170 BUILD_TUPLE              2
#             172 CALL                     4
#             180 LOAD_CONST              10 ('len')
#             182 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             192 LOAD_ATTR               12 (locals)
#             212 CALL                     0
#             220 CONTAINS_OP              0
#             222 POP_JUMP_IF_TRUE        25 (to 274)
#             224 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             234 LOAD_ATTR               14 (_should_repr_global_name)
#             254 LOAD_GLOBAL              4 (len)
#             264 CALL                     1
#             272 POP_JUMP_IF_FALSE       25 (to 324)
#         >>  274 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             284 LOAD_ATTR               16 (_saferepr)
#             304 LOAD_GLOBAL              4 (len)
#             314 CALL                     1
#             322 JUMP_FORWARD             1 (to 326)
#         >>  324 LOAD_CONST              10 ('len')
#         >>  326 LOAD_CONST              11 ('scenarios')
#             328 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             338 LOAD_ATTR               12 (locals)
#             358 CALL                     0
#             366 CONTAINS_OP              0
#             368 POP_JUMP_IF_TRUE        21 (to 412)
#             370 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             380 LOAD_ATTR               14 (_should_repr_global_name)
#             400 LOAD_FAST                3 (scenarios)
#             402 CALL                     1
#             410 POP_JUMP_IF_FALSE       21 (to 454)
#         >>  412 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             422 LOAD_ATTR               16 (_saferepr)
#             442 LOAD_FAST                3 (scenarios)
#             444 CALL                     1
#             452 JUMP_FORWARD             1 (to 456)
#         >>  454 LOAD_CONST              11 ('scenarios')
#         >>  456 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             466 LOAD_ATTR               16 (_saferepr)
#             486 LOAD_FAST                4 (@py_assert2)
#             488 CALL                     1
#             496 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             506 LOAD_ATTR               16 (_saferepr)
#             526 LOAD_FAST                5 (@py_assert5)
#             528 CALL                     1
#             536 LOAD_CONST              12 (('py0', 'py1', 'py3', 'py6'))
#             538 BUILD_CONST_KEY_MAP      4
#             540 BINARY_OP                6 (%)
#             544 STORE_FAST               7 (@py_format7)
#             546 LOAD_CONST              13 ('assert %(py8)s')
#             548 LOAD_CONST              14 ('py8')
#             550 LOAD_FAST                7 (@py_format7)
#             552 BUILD_MAP                1
#             554 BINARY_OP                6 (%)
#             558 STORE_FAST               8 (@py_format9)
#             560 LOAD_GLOBAL             19 (NULL + AssertionError)
#             570 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             580 LOAD_ATTR               20 (_format_explanation)
#             600 LOAD_FAST                8 (@py_format9)
#             602 CALL                     1
#             610 CALL                     1
#             618 RAISE_VARARGS            1
#         >>  620 LOAD_CONST               0 (None)
#             622 COPY                     1
#             624 STORE_FAST               4 (@py_assert2)
#             626 COPY                     1
#             628 STORE_FAST               6 (@py_assert4)
#             630 STORE_FAST               5 (@py_assert5)
#             632 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestN2Assessment at 0x73cd945fe250, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 60>:
#  60           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestN2Assessment')
#               8 STORE_NAME               2 (__qualname__)
# 
#  61          10 LOAD_CONST               1 (<code object test_assess_voltage_violation_clean at 0x3af9c2b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 61>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_assess_voltage_violation_clean)
# 
#  70          16 LOAD_CONST               2 (<code object test_assess_voltage_violation_over at 0x3afa6250, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 70>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_assess_voltage_violation_over)
# 
#  76          22 LOAD_CONST               3 (<code object test_assess_thermal_loading_over at 0x3afa8100, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 76>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_assess_thermal_loading_over)
#              28 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_assess_voltage_violation_clean at 0x3af9c2b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 61>:
#  61           0 RESUME                   0
# 
#  62           2 LOAD_GLOBAL              1 (NULL + N2SecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  63          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _assess_voltage_violation)
# 
#  64          44 BUILD_LIST               0
#              46 LOAD_CONST               1 ((0.98, 1.02, 0.97))
#              48 LIST_EXTEND              1
#              50 LOAD_CONST               2 (0.95)
#              52 LOAD_CONST               3 (1.05)
# 
#  63          54 CALL                     3
#              62 UNPACK_SEQUENCE          3
#              66 STORE_FAST               2 (violation)
#              68 STORE_FAST               3 (max_v)
#              70 STORE_FAST               4 (min_v)
# 
#  66          72 LOAD_CONST               0 (None)
#              74 STORE_FAST               5 (@py_assert2)
#              76 LOAD_FAST                2 (violation)
#              78 LOAD_FAST                5 (@py_assert2)
#              80 IS_OP                    0
#              82 STORE_FAST               6 (@py_assert1)
#              84 LOAD_FAST                6 (@py_assert1)
#              86 POP_JUMP_IF_TRUE       153 (to 394)
#              88 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              98 LOAD_ATTR                6 (_call_reprcompare)
#             118 LOAD_CONST               4 (('is',))
#             120 LOAD_FAST                6 (@py_assert1)
#             122 BUILD_TUPLE              1
#             124 LOAD_CONST               5 (('%(py0)s is %(py3)s',))
#             126 LOAD_FAST                2 (violation)
#             128 LOAD_FAST                5 (@py_assert2)
#             130 BUILD_TUPLE              2
#             132 CALL                     4
#             140 LOAD_CONST               6 ('violation')
#             142 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             152 LOAD_ATTR               10 (locals)
#             172 CALL                     0
#             180 CONTAINS_OP              0
#             182 POP_JUMP_IF_TRUE        21 (to 226)
#             184 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             194 LOAD_ATTR               12 (_should_repr_global_name)
#             214 LOAD_FAST                2 (violation)
#             216 CALL                     1
#             224 POP_JUMP_IF_FALSE       21 (to 268)
#         >>  226 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             236 LOAD_ATTR               14 (_saferepr)
#             256 LOAD_FAST                2 (violation)
#             258 CALL                     1
#             266 JUMP_FORWARD             1 (to 270)
#         >>  268 LOAD_CONST               6 ('violation')
#         >>  270 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             280 LOAD_ATTR               14 (_saferepr)
#             300 LOAD_FAST                5 (@py_assert2)
#             302 CALL                     1
#             310 LOAD_CONST               7 (('py0', 'py3'))
#             312 BUILD_CONST_KEY_MAP      2
#             314 BINARY_OP                6 (%)
#             318 STORE_FAST               7 (@py_format4)
#             320 LOAD_CONST               8 ('assert %(py5)s')
#             322 LOAD_CONST               9 ('py5')
#             324 LOAD_FAST                7 (@py_format4)
#             326 BUILD_MAP                1
#             328 BINARY_OP                6 (%)
#             332 STORE_FAST               8 (@py_format6)
#             334 LOAD_GLOBAL             17 (NULL + AssertionError)
#             344 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             354 LOAD_ATTR               18 (_format_explanation)
#             374 LOAD_FAST                8 (@py_format6)
#             376 CALL                     1
#             384 CALL                     1
#             392 RAISE_VARARGS            1
#         >>  394 LOAD_CONST               0 (None)
#             396 COPY                     1
#             398 STORE_FAST               6 (@py_assert1)
#             400 STORE_FAST               5 (@py_assert2)
# 
#  67         402 LOAD_CONST              10 (1.02)
#             404 STORE_FAST               5 (@py_assert2)
#             406 LOAD_FAST                3 (max_v)
#             408 LOAD_FAST                5 (@py_assert2)
#             410 COMPARE_OP              40 (==)
#             414 STORE_FAST               6 (@py_assert1)
#             416 LOAD_FAST                6 (@py_assert1)
#             418 POP_JUMP_IF_TRUE       153 (to 726)
#             420 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             430 LOAD_ATTR                6 (_call_reprcompare)
#             450 LOAD_CONST              11 (('==',))
#             452 LOAD_FAST                6 (@py_assert1)
#             454 BUILD_TUPLE              1
#             456 LOAD_CONST              12 (('%(py0)s == %(py3)s',))
#             458 LOAD_FAST                3 (max_v)
#             460 LOAD_FAST                5 (@py_assert2)
#             462 BUILD_TUPLE              2
#             464 CALL                     4
#             472 LOAD_CONST              13 ('max_v')
#             474 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             484 LOAD_ATTR               10 (locals)
#             504 CALL                     0
#             512 CONTAINS_OP              0
#             514 POP_JUMP_IF_TRUE        21 (to 558)
#             516 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             526 LOAD_ATTR               12 (_should_repr_global_name)
#             546 LOAD_FAST                3 (max_v)
#             548 CALL                     1
#             556 POP_JUMP_IF_FALSE       21 (to 600)
#         >>  558 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             568 LOAD_ATTR               14 (_saferepr)
#             588 LOAD_FAST                3 (max_v)
#             590 CALL                     1
#             598 JUMP_FORWARD             1 (to 602)
#         >>  600 LOAD_CONST              13 ('max_v')
#         >>  602 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             612 LOAD_ATTR               14 (_saferepr)
#             632 LOAD_FAST                5 (@py_assert2)
#             634 CALL                     1
#             642 LOAD_CONST               7 (('py0', 'py3'))
#             644 BUILD_CONST_KEY_MAP      2
#             646 BINARY_OP                6 (%)
#             650 STORE_FAST               7 (@py_format4)
#             652 LOAD_CONST               8 ('assert %(py5)s')
#             654 LOAD_CONST               9 ('py5')
#             656 LOAD_FAST                7 (@py_format4)
#             658 BUILD_MAP                1
#             660 BINARY_OP                6 (%)
#             664 STORE_FAST               8 (@py_format6)
#             666 LOAD_GLOBAL             17 (NULL + AssertionError)
#             676 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             686 LOAD_ATTR               18 (_format_explanation)
#             706 LOAD_FAST                8 (@py_format6)
#             708 CALL                     1
#             716 CALL                     1
#             724 RAISE_VARARGS            1
#         >>  726 LOAD_CONST               0 (None)
#             728 COPY                     1
#             730 STORE_FAST               6 (@py_assert1)
#             732 STORE_FAST               5 (@py_assert2)
# 
#  68         734 LOAD_CONST              14 (0.97)
#             736 STORE_FAST               5 (@py_assert2)
#             738 LOAD_FAST                4 (min_v)
#             740 LOAD_FAST                5 (@py_assert2)
#             742 COMPARE_OP              40 (==)
#             746 STORE_FAST               6 (@py_assert1)
#             748 LOAD_FAST                6 (@py_assert1)
#             750 POP_JUMP_IF_TRUE       153 (to 1058)
#             752 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             762 LOAD_ATTR                6 (_call_reprcompare)
#             782 LOAD_CONST              11 (('==',))
#             784 LOAD_FAST                6 (@py_assert1)
#             786 BUILD_TUPLE              1
#             788 LOAD_CONST              12 (('%(py0)s == %(py3)s',))
#             790 LOAD_FAST                4 (min_v)
#             792 LOAD_FAST                5 (@py_assert2)
#             794 BUILD_TUPLE              2
#             796 CALL                     4
#             804 LOAD_CONST              15 ('min_v')
#             806 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             816 LOAD_ATTR               10 (locals)
#             836 CALL                     0
#             844 CONTAINS_OP              0
#             846 POP_JUMP_IF_TRUE        21 (to 890)
#             848 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             858 LOAD_ATTR               12 (_should_repr_global_name)
#             878 LOAD_FAST                4 (min_v)
#             880 CALL                     1
#             888 POP_JUMP_IF_FALSE       21 (to 932)
#         >>  890 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             900 LOAD_ATTR               14 (_saferepr)
#             920 LOAD_FAST                4 (min_v)
#             922 CALL                     1
#             930 JUMP_FORWARD             1 (to 934)
#         >>  932 LOAD_CONST              15 ('min_v')
#         >>  934 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             944 LOAD_ATTR               14 (_saferepr)
#             964 LOAD_FAST                5 (@py_assert2)
#             966 CALL                     1
#             974 LOAD_CONST               7 (('py0', 'py3'))
#             976 BUILD_CONST_KEY_MAP      2
#             978 BINARY_OP                6 (%)
#             982 STORE_FAST               7 (@py_format4)
#             984 LOAD_CONST               8 ('assert %(py5)s')
#             986 LOAD_CONST               9 ('py5')
#             988 LOAD_FAST                7 (@py_format4)
#             990 BUILD_MAP                1
#             992 BINARY_OP                6 (%)
#             996 STORE_FAST               8 (@py_format6)
#             998 LOAD_GLOBAL             17 (NULL + AssertionError)
#            1008 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1018 LOAD_ATTR               18 (_format_explanation)
#            1038 LOAD_FAST                8 (@py_format6)
#            1040 CALL                     1
#            1048 CALL                     1
#            1056 RAISE_VARARGS            1
#         >> 1058 LOAD_CONST               0 (None)
#            1060 COPY                     1
#            1062 STORE_FAST               6 (@py_assert1)
#            1064 STORE_FAST               5 (@py_assert2)
#            1066 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_assess_voltage_violation_over at 0x3afa6250, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 70>:
#  70           0 RESUME                   0
# 
#  71           2 LOAD_GLOBAL              1 (NULL + N2SecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  72          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _assess_voltage_violation)
#              44 LOAD_CONST               1 (1.06)
#              46 BUILD_LIST               1
#              48 LOAD_CONST               2 (0.95)
#              50 LOAD_CONST               3 (1.05)
#              52 CALL                     3
#              60 UNPACK_SEQUENCE          3
#              64 STORE_FAST               2 (violation)
#              66 STORE_FAST               3 (max_v)
#              68 STORE_FAST               4 (min_v)
# 
#  73          70 LOAD_CONST               0 (None)
#              72 STORE_FAST               5 (@py_assert2)
#              74 LOAD_FAST                2 (violation)
#              76 LOAD_FAST                5 (@py_assert2)
#              78 IS_OP                    1
#              80 STORE_FAST               6 (@py_assert1)
#              82 LOAD_FAST                6 (@py_assert1)
#              84 POP_JUMP_IF_TRUE       153 (to 392)
#              86 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              96 LOAD_ATTR                6 (_call_reprcompare)
#             116 LOAD_CONST               4 (('is not',))
#             118 LOAD_FAST                6 (@py_assert1)
#             120 BUILD_TUPLE              1
#             122 LOAD_CONST               5 (('%(py0)s is not %(py3)s',))
#             124 LOAD_FAST                2 (violation)
#             126 LOAD_FAST                5 (@py_assert2)
#             128 BUILD_TUPLE              2
#             130 CALL                     4
#             138 LOAD_CONST               6 ('violation')
#             140 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             150 LOAD_ATTR               10 (locals)
#             170 CALL                     0
#             178 CONTAINS_OP              0
#             180 POP_JUMP_IF_TRUE        21 (to 224)
#             182 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             192 LOAD_ATTR               12 (_should_repr_global_name)
#             212 LOAD_FAST                2 (violation)
#             214 CALL                     1
#             222 POP_JUMP_IF_FALSE       21 (to 266)
#         >>  224 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             234 LOAD_ATTR               14 (_saferepr)
#             254 LOAD_FAST                2 (violation)
#             256 CALL                     1
#             264 JUMP_FORWARD             1 (to 268)
#         >>  266 LOAD_CONST               6 ('violation')
#         >>  268 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             278 LOAD_ATTR               14 (_saferepr)
#             298 LOAD_FAST                5 (@py_assert2)
#             300 CALL                     1
#             308 LOAD_CONST               7 (('py0', 'py3'))
#             310 BUILD_CONST_KEY_MAP      2
#             312 BINARY_OP                6 (%)
#             316 STORE_FAST               7 (@py_format4)
#             318 LOAD_CONST               8 ('assert %(py5)s')
#             320 LOAD_CONST               9 ('py5')
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
# 
#  74         400 LOAD_CONST              10 ('over')
#             402 STORE_FAST               9 (@py_assert0)
#             404 LOAD_FAST                2 (violation)
#             406 LOAD_ATTR               20 (lower)
#             426 STORE_FAST              10 (@py_assert4)
#             428 PUSH_NULL
#             430 LOAD_FAST               10 (@py_assert4)
#             432 CALL                     0
#             440 STORE_FAST              11 (@py_assert6)
#             442 LOAD_FAST                9 (@py_assert0)
#             444 LOAD_FAST               11 (@py_assert6)
#             446 CONTAINS_OP              0
#             448 STORE_FAST               5 (@py_assert2)
#             450 LOAD_FAST                5 (@py_assert2)
#             452 POP_JUMP_IF_TRUE       193 (to 840)
#             454 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             464 LOAD_ATTR                6 (_call_reprcompare)
#             484 LOAD_CONST              11 (('in',))
#             486 LOAD_FAST                5 (@py_assert2)
#             488 BUILD_TUPLE              1
#             490 LOAD_CONST              12 (('%(py1)s in %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.lower\n}()\n}',))
#             492 LOAD_FAST                9 (@py_assert0)
#             494 LOAD_FAST               11 (@py_assert6)
#             496 BUILD_TUPLE              2
#             498 CALL                     4
#             506 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             516 LOAD_ATTR               14 (_saferepr)
#             536 LOAD_FAST                9 (@py_assert0)
#             538 CALL                     1
#             546 LOAD_CONST               6 ('violation')
#             548 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             558 LOAD_ATTR               10 (locals)
#             578 CALL                     0
#             586 CONTAINS_OP              0
#             588 POP_JUMP_IF_TRUE        21 (to 632)
#             590 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             600 LOAD_ATTR               12 (_should_repr_global_name)
#             620 LOAD_FAST                2 (violation)
#             622 CALL                     1
#             630 POP_JUMP_IF_FALSE       21 (to 674)
#         >>  632 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             642 LOAD_ATTR               14 (_saferepr)
#             662 LOAD_FAST                2 (violation)
#             664 CALL                     1
#             672 JUMP_FORWARD             1 (to 676)
#         >>  674 LOAD_CONST               6 ('violation')
#         >>  676 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             686 LOAD_ATTR               14 (_saferepr)
#             706 LOAD_FAST               10 (@py_assert4)
#             708 CALL                     1
#             716 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             726 LOAD_ATTR               14 (_saferepr)
#             746 LOAD_FAST               11 (@py_assert6)
#             748 CALL                     1
#             756 LOAD_CONST              13 (('py1', 'py3', 'py5', 'py7'))
#             758 BUILD_CONST_KEY_MAP      4
#             760 BINARY_OP                6 (%)
#             764 STORE_FAST              12 (@py_format8)
#             766 LOAD_CONST              14 ('assert %(py9)s')
#             768 LOAD_CONST              15 ('py9')
#             770 LOAD_FAST               12 (@py_format8)
#             772 BUILD_MAP                1
#             774 BINARY_OP                6 (%)
#             778 STORE_FAST              13 (@py_format10)
#             780 LOAD_GLOBAL             17 (NULL + AssertionError)
#             790 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             800 LOAD_ATTR               18 (_format_explanation)
#             820 LOAD_FAST               13 (@py_format10)
#             822 CALL                     1
#             830 CALL                     1
#             838 RAISE_VARARGS            1
#         >>  840 LOAD_CONST               0 (None)
#             842 COPY                     1
#             844 STORE_FAST               9 (@py_assert0)
#             846 COPY                     1
#             848 STORE_FAST               5 (@py_assert2)
#             850 COPY                     1
#             852 STORE_FAST              10 (@py_assert4)
#             854 STORE_FAST              11 (@py_assert6)
#             856 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_assess_thermal_loading_over at 0x3afa8100, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 76>:
#  76           0 RESUME                   0
# 
#  77           2 LOAD_GLOBAL              1 (NULL + N2SecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  78          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _assess_thermal_loading)
#              44 LOAD_CONST               1 (1.2)
#              46 LOAD_CONST               2 (0.8)
#              48 BUILD_LIST               2
#              50 LOAD_CONST               3 (1.0)
#              52 CALL                     2
#              60 UNPACK_SEQUENCE          2
#              64 STORE_FAST               2 (violation)
#              66 STORE_FAST               3 (max_loading)
# 
#  79          68 LOAD_CONST               0 (None)
#              70 STORE_FAST               4 (@py_assert2)
#              72 LOAD_FAST                2 (violation)
#              74 LOAD_FAST                4 (@py_assert2)
#              76 IS_OP                    1
#              78 STORE_FAST               5 (@py_assert1)
#              80 LOAD_FAST                5 (@py_assert1)
#              82 POP_JUMP_IF_TRUE       153 (to 390)
#              84 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              94 LOAD_ATTR                6 (_call_reprcompare)
#             114 LOAD_CONST               4 (('is not',))
#             116 LOAD_FAST                5 (@py_assert1)
#             118 BUILD_TUPLE              1
#             120 LOAD_CONST               5 (('%(py0)s is not %(py3)s',))
#             122 LOAD_FAST                2 (violation)
#             124 LOAD_FAST                4 (@py_assert2)
#             126 BUILD_TUPLE              2
#             128 CALL                     4
#             136 LOAD_CONST               6 ('violation')
#             138 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             148 LOAD_ATTR               10 (locals)
#             168 CALL                     0
#             176 CONTAINS_OP              0
#             178 POP_JUMP_IF_TRUE        21 (to 222)
#             180 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             190 LOAD_ATTR               12 (_should_repr_global_name)
#             210 LOAD_FAST                2 (violation)
#             212 CALL                     1
#             220 POP_JUMP_IF_FALSE       21 (to 264)
#         >>  222 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             232 LOAD_ATTR               14 (_saferepr)
#             252 LOAD_FAST                2 (violation)
#             254 CALL                     1
#             262 JUMP_FORWARD             1 (to 266)
#         >>  264 LOAD_CONST               6 ('violation')
#         >>  266 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             276 LOAD_ATTR               14 (_saferepr)
#             296 LOAD_FAST                4 (@py_assert2)
#             298 CALL                     1
#             306 LOAD_CONST               7 (('py0', 'py3'))
#             308 BUILD_CONST_KEY_MAP      2
#             310 BINARY_OP                6 (%)
#             314 STORE_FAST               6 (@py_format4)
#             316 LOAD_CONST               8 ('assert %(py5)s')
#             318 LOAD_CONST               9 ('py5')
#             320 LOAD_FAST                6 (@py_format4)
#             322 BUILD_MAP                1
#             324 BINARY_OP                6 (%)
#             328 STORE_FAST               7 (@py_format6)
#             330 LOAD_GLOBAL             17 (NULL + AssertionError)
#             340 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             350 LOAD_ATTR               18 (_format_explanation)
#             370 LOAD_FAST                7 (@py_format6)
#             372 CALL                     1
#             380 CALL                     1
#             388 RAISE_VARARGS            1
#         >>  390 LOAD_CONST               0 (None)
#             392 COPY                     1
#             394 STORE_FAST               5 (@py_assert1)
#             396 STORE_FAST               4 (@py_assert2)
# 
#  80         398 LOAD_CONST              10 ('over')
#             400 STORE_FAST               8 (@py_assert0)
#             402 LOAD_FAST                2 (violation)
#             404 LOAD_ATTR               20 (lower)
#             424 STORE_FAST               9 (@py_assert4)
#             426 PUSH_NULL
#             428 LOAD_FAST                9 (@py_assert4)
#             430 CALL                     0
#             438 STORE_FAST              10 (@py_assert6)
#             440 LOAD_FAST                8 (@py_assert0)
#             442 LOAD_FAST               10 (@py_assert6)
#             444 CONTAINS_OP              0
#             446 STORE_FAST               4 (@py_assert2)
#             448 LOAD_FAST                4 (@py_assert2)
#             450 POP_JUMP_IF_TRUE       193 (to 838)
#             452 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             462 LOAD_ATTR                6 (_call_reprcompare)
#             482 LOAD_CONST              11 (('in',))
#             484 LOAD_FAST                4 (@py_assert2)
#             486 BUILD_TUPLE              1
#             488 LOAD_CONST              12 (('%(py1)s in %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.lower\n}()\n}',))
#             490 LOAD_FAST                8 (@py_assert0)
#             492 LOAD_FAST               10 (@py_assert6)
#             494 BUILD_TUPLE              2
#             496 CALL                     4
#             504 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             514 LOAD_ATTR               14 (_saferepr)
#             534 LOAD_FAST                8 (@py_assert0)
#             536 CALL                     1
#             544 LOAD_CONST               6 ('violation')
#             546 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             556 LOAD_ATTR               10 (locals)
#             576 CALL                     0
#             584 CONTAINS_OP              0
#             586 POP_JUMP_IF_TRUE        21 (to 630)
#             588 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             598 LOAD_ATTR               12 (_should_repr_global_name)
#             618 LOAD_FAST                2 (violation)
#             620 CALL                     1
#             628 POP_JUMP_IF_FALSE       21 (to 672)
#         >>  630 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             640 LOAD_ATTR               14 (_saferepr)
#             660 LOAD_FAST                2 (violation)
#             662 CALL                     1
#             670 JUMP_FORWARD             1 (to 674)
#         >>  672 LOAD_CONST               6 ('violation')
#         >>  674 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             684 LOAD_ATTR               14 (_saferepr)
#             704 LOAD_FAST                9 (@py_assert4)
#             706 CALL                     1
#             714 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             724 LOAD_ATTR               14 (_saferepr)
#             744 LOAD_FAST               10 (@py_assert6)
#             746 CALL                     1
#             754 LOAD_CONST              13 (('py1', 'py3', 'py5', 'py7'))
#             756 BUILD_CONST_KEY_MAP      4
#             758 BINARY_OP                6 (%)
#             762 STORE_FAST              11 (@py_format8)
#             764 LOAD_CONST              14 ('assert %(py9)s')
#             766 LOAD_CONST              15 ('py9')
#             768 LOAD_FAST               11 (@py_format8)
#             770 BUILD_MAP                1
#             772 BINARY_OP                6 (%)
#             776 STORE_FAST              12 (@py_format10)
#             778 LOAD_GLOBAL             17 (NULL + AssertionError)
#             788 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             798 LOAD_ATTR               18 (_format_explanation)
#             818 LOAD_FAST               12 (@py_format10)
#             820 CALL                     1
#             828 CALL                     1
#             836 RAISE_VARARGS            1
#         >>  838 LOAD_CONST               0 (None)
#             840 COPY                     1
#             842 STORE_FAST               8 (@py_assert0)
#             844 COPY                     1
#             846 STORE_FAST               4 (@py_assert2)
#             848 COPY                     1
#             850 STORE_FAST               9 (@py_assert4)
#             852 STORE_FAST              10 (@py_assert6)
# 
#  81         854 LOAD_CONST               1 (1.2)
#             856 STORE_FAST               4 (@py_assert2)
#             858 LOAD_FAST                3 (max_loading)
#             860 LOAD_FAST                4 (@py_assert2)
#             862 COMPARE_OP              40 (==)
#             866 STORE_FAST               5 (@py_assert1)
#             868 LOAD_FAST                5 (@py_assert1)
#             870 POP_JUMP_IF_TRUE       153 (to 1178)
#             872 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             882 LOAD_ATTR                6 (_call_reprcompare)
#             902 LOAD_CONST              16 (('==',))
#             904 LOAD_FAST                5 (@py_assert1)
#             906 BUILD_TUPLE              1
#             908 LOAD_CONST              17 (('%(py0)s == %(py3)s',))
#             910 LOAD_FAST                3 (max_loading)
#             912 LOAD_FAST                4 (@py_assert2)
#             914 BUILD_TUPLE              2
#             916 CALL                     4
#             924 LOAD_CONST              18 ('max_loading')
#             926 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             936 LOAD_ATTR               10 (locals)
#             956 CALL                     0
#             964 CONTAINS_OP              0
#             966 POP_JUMP_IF_TRUE        21 (to 1010)
#             968 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             978 LOAD_ATTR               12 (_should_repr_global_name)
#             998 LOAD_FAST                3 (max_loading)
#            1000 CALL                     1
#            1008 POP_JUMP_IF_FALSE       21 (to 1052)
#         >> 1010 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1020 LOAD_ATTR               14 (_saferepr)
#            1040 LOAD_FAST                3 (max_loading)
#            1042 CALL                     1
#            1050 JUMP_FORWARD             1 (to 1054)
#         >> 1052 LOAD_CONST              18 ('max_loading')
#         >> 1054 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1064 LOAD_ATTR               14 (_saferepr)
#            1084 LOAD_FAST                4 (@py_assert2)
#            1086 CALL                     1
#            1094 LOAD_CONST               7 (('py0', 'py3'))
#            1096 BUILD_CONST_KEY_MAP      2
#            1098 BINARY_OP                6 (%)
#            1102 STORE_FAST               6 (@py_format4)
#            1104 LOAD_CONST               8 ('assert %(py5)s')
#            1106 LOAD_CONST               9 ('py5')
#            1108 LOAD_FAST                6 (@py_format4)
#            1110 BUILD_MAP                1
#            1112 BINARY_OP                6 (%)
#            1116 STORE_FAST               7 (@py_format6)
#            1118 LOAD_GLOBAL             17 (NULL + AssertionError)
#            1128 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1138 LOAD_ATTR               18 (_format_explanation)
#            1158 LOAD_FAST                7 (@py_format6)
#            1160 CALL                     1
#            1168 CALL                     1
#            1176 RAISE_VARARGS            1
#         >> 1178 LOAD_CONST               0 (None)
#            1180 COPY                     1
#            1182 STORE_FAST               5 (@py_assert1)
#            1184 STORE_FAST               4 (@py_assert2)
#            1186 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestN2ContingencyResult at 0x73cd945febf0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 84>:
#  84           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestN2ContingencyResult')
#               8 STORE_NAME               2 (__qualname__)
# 
#  85          10 LOAD_CONST               1 (<code object test_n2_contingency_result_dataclass at 0x3afaa690, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 85>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_n2_contingency_result_dataclass)
#              16 RETURN_CONST             2 (None)
# 
# Disassembly of <code object test_n2_contingency_result_dataclass at 0x3afaa690, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 85>:
#  85           0 RESUME                   0
# 
#  86           2 LOAD_GLOBAL              1 (NULL + N2ContingencyResult)
# 
#  87          12 LOAD_CONST               1 ('L1')
# 
#  88          14 LOAD_CONST               2 ('Line1')
# 
#  89          16 LOAD_CONST               3 ('L2')
# 
#  90          18 LOAD_CONST               4 ('Line2')
# 
#  91          20 LOAD_CONST               5 ('passed')
# 
#  92          22 LOAD_CONST               6 (True)
# 
#  86          24 KW_NAMES                 7 (('branch1_id', 'branch1_name', 'branch2_id', 'branch2_name', 'status', 'converged'))
#              26 CALL                     6
#              34 STORE_FAST               1 (r)
# 
#  94          36 LOAD_FAST                1 (r)
#              38 LOAD_ATTR                2 (status)
#              58 STORE_FAST               2 (@py_assert1)
#              60 LOAD_CONST               5 ('passed')
#              62 STORE_FAST               3 (@py_assert4)
#              64 LOAD_FAST                2 (@py_assert1)
#              66 LOAD_FAST                3 (@py_assert4)
#              68 COMPARE_OP              40 (==)
#              72 STORE_FAST               4 (@py_assert3)
#              74 LOAD_FAST                4 (@py_assert3)
#              76 POP_JUMP_IF_TRUE       173 (to 424)
#              78 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              88 LOAD_ATTR                6 (_call_reprcompare)
#             108 LOAD_CONST               8 (('==',))
#             110 LOAD_FAST                4 (@py_assert3)
#             112 BUILD_TUPLE              1
#             114 LOAD_CONST               9 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s',))
#             116 LOAD_FAST                2 (@py_assert1)
#             118 LOAD_FAST                3 (@py_assert4)
#             120 BUILD_TUPLE              2
#             122 CALL                     4
#             130 LOAD_CONST              10 ('r')
#             132 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             142 LOAD_ATTR               10 (locals)
#             162 CALL                     0
#             170 CONTAINS_OP              0
#             172 POP_JUMP_IF_TRUE        21 (to 216)
#             174 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             184 LOAD_ATTR               12 (_should_repr_global_name)
#             204 LOAD_FAST                1 (r)
#             206 CALL                     1
#             214 POP_JUMP_IF_FALSE       21 (to 258)
#         >>  216 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             226 LOAD_ATTR               14 (_saferepr)
#             246 LOAD_FAST                1 (r)
#             248 CALL                     1
#             256 JUMP_FORWARD             1 (to 260)
#         >>  258 LOAD_CONST              10 ('r')
#         >>  260 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             270 LOAD_ATTR               14 (_saferepr)
#             290 LOAD_FAST                2 (@py_assert1)
#             292 CALL                     1
#             300 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             310 LOAD_ATTR               14 (_saferepr)
#             330 LOAD_FAST                3 (@py_assert4)
#             332 CALL                     1
#             340 LOAD_CONST              11 (('py0', 'py2', 'py5'))
#             342 BUILD_CONST_KEY_MAP      3
#             344 BINARY_OP                6 (%)
#             348 STORE_FAST               5 (@py_format6)
#             350 LOAD_CONST              12 ('assert %(py7)s')
#             352 LOAD_CONST              13 ('py7')
#             354 LOAD_FAST                5 (@py_format6)
#             356 BUILD_MAP                1
#             358 BINARY_OP                6 (%)
#             362 STORE_FAST               6 (@py_format8)
#             364 LOAD_GLOBAL             17 (NULL + AssertionError)
#             374 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             384 LOAD_ATTR               18 (_format_explanation)
#             404 LOAD_FAST                6 (@py_format8)
#             406 CALL                     1
#             414 CALL                     1
#             422 RAISE_VARARGS            1
#         >>  424 LOAD_CONST               0 (None)
#             426 COPY                     1
#             428 STORE_FAST               2 (@py_assert1)
#             430 COPY                     1
#             432 STORE_FAST               4 (@py_assert3)
#             434 STORE_FAST               3 (@py_assert4)
# 
#  95         436 LOAD_FAST                1 (r)
#             438 LOAD_ATTR               20 (converged)
#             458 STORE_FAST               2 (@py_assert1)
#             460 LOAD_CONST               6 (True)
#             462 STORE_FAST               3 (@py_assert4)
#             464 LOAD_FAST                2 (@py_assert1)
#             466 LOAD_FAST                3 (@py_assert4)
#             468 IS_OP                    0
#             470 STORE_FAST               4 (@py_assert3)
#             472 LOAD_FAST                4 (@py_assert3)
#             474 POP_JUMP_IF_TRUE       173 (to 822)
#             476 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             486 LOAD_ATTR                6 (_call_reprcompare)
#             506 LOAD_CONST              14 (('is',))
#             508 LOAD_FAST                4 (@py_assert3)
#             510 BUILD_TUPLE              1
#             512 LOAD_CONST              15 (('%(py2)s\n{%(py2)s = %(py0)s.converged\n} is %(py5)s',))
#             514 LOAD_FAST                2 (@py_assert1)
#             516 LOAD_FAST                3 (@py_assert4)
#             518 BUILD_TUPLE              2
#             520 CALL                     4
#             528 LOAD_CONST              10 ('r')
#             530 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             540 LOAD_ATTR               10 (locals)
#             560 CALL                     0
#             568 CONTAINS_OP              0
#             570 POP_JUMP_IF_TRUE        21 (to 614)
#             572 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             582 LOAD_ATTR               12 (_should_repr_global_name)
#             602 LOAD_FAST                1 (r)
#             604 CALL                     1
#             612 POP_JUMP_IF_FALSE       21 (to 656)
#         >>  614 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             624 LOAD_ATTR               14 (_saferepr)
#             644 LOAD_FAST                1 (r)
#             646 CALL                     1
#             654 JUMP_FORWARD             1 (to 658)
#         >>  656 LOAD_CONST              10 ('r')
#         >>  658 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             668 LOAD_ATTR               14 (_saferepr)
#             688 LOAD_FAST                2 (@py_assert1)
#             690 CALL                     1
#             698 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             708 LOAD_ATTR               14 (_saferepr)
#             728 LOAD_FAST                3 (@py_assert4)
#             730 CALL                     1
#             738 LOAD_CONST              11 (('py0', 'py2', 'py5'))
#             740 BUILD_CONST_KEY_MAP      3
#             742 BINARY_OP                6 (%)
#             746 STORE_FAST               5 (@py_format6)
#             748 LOAD_CONST              12 ('assert %(py7)s')
#             750 LOAD_CONST              13 ('py7')
#             752 LOAD_FAST                5 (@py_format6)
#             754 BUILD_MAP                1
#             756 BINARY_OP                6 (%)
#             760 STORE_FAST               6 (@py_format8)
#             762 LOAD_GLOBAL             17 (NULL + AssertionError)
#             772 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             782 LOAD_ATTR               18 (_format_explanation)
#             802 LOAD_FAST                6 (@py_format8)
#             804 CALL                     1
#             812 CALL                     1
#             820 RAISE_VARARGS            1
#         >>  822 LOAD_CONST               0 (None)
#             824 COPY                     1
#             826 STORE_FAST               2 (@py_assert1)
#             828 COPY                     1
#             830 STORE_FAST               4 (@py_assert3)
#             832 STORE_FAST               3 (@py_assert4)
# 
#  96         834 LOAD_FAST                1 (r)
#             836 LOAD_ATTR               22 (violation)
#             856 STORE_FAST               2 (@py_assert1)
#             858 LOAD_CONST               0 (None)
#             860 STORE_FAST               3 (@py_assert4)
#             862 LOAD_FAST                2 (@py_assert1)
#             864 LOAD_FAST                3 (@py_assert4)
#             866 IS_OP                    0
#             868 STORE_FAST               4 (@py_assert3)
#             870 LOAD_FAST                4 (@py_assert3)
#             872 POP_JUMP_IF_TRUE       173 (to 1220)
#             874 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             884 LOAD_ATTR                6 (_call_reprcompare)
#             904 LOAD_CONST              14 (('is',))
#             906 LOAD_FAST                4 (@py_assert3)
#             908 BUILD_TUPLE              1
#             910 LOAD_CONST              16 (('%(py2)s\n{%(py2)s = %(py0)s.violation\n} is %(py5)s',))
#             912 LOAD_FAST                2 (@py_assert1)
#             914 LOAD_FAST                3 (@py_assert4)
#             916 BUILD_TUPLE              2
#             918 CALL                     4
#             926 LOAD_CONST              10 ('r')
#             928 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             938 LOAD_ATTR               10 (locals)
#             958 CALL                     0
#             966 CONTAINS_OP              0
#             968 POP_JUMP_IF_TRUE        21 (to 1012)
#             970 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             980 LOAD_ATTR               12 (_should_repr_global_name)
#            1000 LOAD_FAST                1 (r)
#            1002 CALL                     1
#            1010 POP_JUMP_IF_FALSE       21 (to 1054)
#         >> 1012 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1022 LOAD_ATTR               14 (_saferepr)
#            1042 LOAD_FAST                1 (r)
#            1044 CALL                     1
#            1052 JUMP_FORWARD             1 (to 1056)
#         >> 1054 LOAD_CONST              10 ('r')
#         >> 1056 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1066 LOAD_ATTR               14 (_saferepr)
#            1086 LOAD_FAST                2 (@py_assert1)
#            1088 CALL                     1
#            1096 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1106 LOAD_ATTR               14 (_saferepr)
#            1126 LOAD_FAST                3 (@py_assert4)
#            1128 CALL                     1
#            1136 LOAD_CONST              11 (('py0', 'py2', 'py5'))
#            1138 BUILD_CONST_KEY_MAP      3
#            1140 BINARY_OP                6 (%)
#            1144 STORE_FAST               5 (@py_format6)
#            1146 LOAD_CONST              12 ('assert %(py7)s')
#            1148 LOAD_CONST              13 ('py7')
#            1150 LOAD_FAST                5 (@py_format6)
#            1152 BUILD_MAP                1
#            1154 BINARY_OP                6 (%)
#            1158 STORE_FAST               6 (@py_format8)
#            1160 LOAD_GLOBAL             17 (NULL + AssertionError)
#            1170 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1180 LOAD_ATTR               18 (_format_explanation)
#            1200 LOAD_FAST                6 (@py_format8)
#            1202 CALL                     1
#            1210 CALL                     1
#            1218 RAISE_VARARGS            1
#         >> 1220 LOAD_CONST               0 (None)
#            1222 COPY                     1
#            1224 STORE_FAST               2 (@py_assert1)
#            1226 COPY                     1
#            1228 STORE_FAST               4 (@py_assert3)
#            1230 STORE_FAST               3 (@py_assert4)
#            1232 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestN2Run at 0x73cd945fecd0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 99>:
#  99           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestN2Run')
#               8 STORE_NAME               2 (__qualname__)
# 
# 100          10 LOAD_CONST               1 (<code object test_run_invalid_config_returns_failure at 0x3af8f430, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 100>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_run_invalid_config_returns_failure)
#              16 RETURN_CONST             2 (None)
# 
# Disassembly of <code object test_run_invalid_config_returns_failure at 0x3af8f430, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_n2_security.py", line 100>:
# 100           0 RESUME                   0
# 
# 101           2 LOAD_GLOBAL              1 (NULL + N2SecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
# 102          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + run)
#              44 BUILD_MAP                0
#              46 CALL                     1
#              54 STORE_FAST               2 (result)
# 
# 103          56 LOAD_FAST                2 (result)
#              58 LOAD_ATTR                4 (status)
#              78 STORE_FAST               3 (@py_assert1)
#              80 LOAD_FAST                3 (@py_assert1)
#              82 LOAD_ATTR                6 (value)
#             102 STORE_FAST               4 (@py_assert3)
#             104 LOAD_CONST               1 ('FAILED')
#             106 LOAD_CONST               2 ('failed')
#             108 BUILD_LIST               2
#             110 STORE_FAST               5 (@py_assert6)
#             112 LOAD_FAST                4 (@py_assert3)
#             114 LOAD_FAST                5 (@py_assert6)
#             116 CONTAINS_OP              0
#             118 STORE_FAST               6 (@py_assert5)
#             120 LOAD_FAST                6 (@py_assert5)
#             122 POP_JUMP_IF_TRUE       193 (to 510)
#             124 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             134 LOAD_ATTR               10 (_call_reprcompare)
#             154 LOAD_CONST               3 (('in',))
#             156 LOAD_FAST                6 (@py_assert5)
#             158 BUILD_TUPLE              1
#             160 LOAD_CONST               4 (('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.status\n}.value\n} in %(py7)s',))
#             162 LOAD_FAST                4 (@py_assert3)
#             164 LOAD_FAST                5 (@py_assert6)
#             166 BUILD_TUPLE              2
#             168 CALL                     4
#             176 LOAD_CONST               5 ('result')
#             178 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             188 LOAD_ATTR               14 (locals)
#             208 CALL                     0
#             216 CONTAINS_OP              0
#             218 POP_JUMP_IF_TRUE        21 (to 262)
#             220 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             230 LOAD_ATTR               16 (_should_repr_global_name)
#             250 LOAD_FAST                2 (result)
#             252 CALL                     1
#             260 POP_JUMP_IF_FALSE       21 (to 304)
#         >>  262 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             272 LOAD_ATTR               18 (_saferepr)
#             292 LOAD_FAST                2 (result)
#             294 CALL                     1
#             302 JUMP_FORWARD             1 (to 306)
#         >>  304 LOAD_CONST               5 ('result')
#         >>  306 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             316 LOAD_ATTR               18 (_saferepr)
#             336 LOAD_FAST                3 (@py_assert1)
#             338 CALL                     1
#             346 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             356 LOAD_ATTR               18 (_saferepr)
#             376 LOAD_FAST                4 (@py_assert3)
#             378 CALL                     1
#             386 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             396 LOAD_ATTR               18 (_saferepr)
#             416 LOAD_FAST                5 (@py_assert6)
#             418 CALL                     1
#             426 LOAD_CONST               6 (('py0', 'py2', 'py4', 'py7'))
#             428 BUILD_CONST_KEY_MAP      4
#             430 BINARY_OP                6 (%)
#             434 STORE_FAST               7 (@py_format8)
#             436 LOAD_CONST               7 ('assert %(py9)s')
#             438 LOAD_CONST               8 ('py9')
#             440 LOAD_FAST                7 (@py_format8)
#             442 BUILD_MAP                1
#             444 BINARY_OP                6 (%)
#             448 STORE_FAST               8 (@py_format10)
#             450 LOAD_GLOBAL             21 (NULL + AssertionError)
#             460 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             470 LOAD_ATTR               22 (_format_explanation)
#             490 LOAD_FAST                8 (@py_format10)
#             492 CALL                     1
#             500 CALL                     1
#             508 RAISE_VARARGS            1
#         >>  510 LOAD_CONST               0 (None)
#             512 COPY                     1
#             514 STORE_FAST               3 (@py_assert1)
#             516 COPY                     1
#             518 STORE_FAST               4 (@py_assert3)
#             520 COPY                     1
#             522 STORE_FAST               6 (@py_assert5)
#             524 STORE_FAST               5 (@py_assert6)
#             526 RETURN_CONST             0 (None)
# 