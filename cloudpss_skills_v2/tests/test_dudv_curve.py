# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/__pycache__/test_dudv_curve.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


def TestDUDVValidation():
    """TestDUDVValidation"""
pass  # TODO: restore


def TestDUDVComputation():
    """TestDUDVComputation"""
pass  # TODO: restore


def TestDUDVRun():
    """TestDUDVRun"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('Tests for DUDVCurveSkill v2.')
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
#              36 IMPORT_NAME              7 (numpy)
#              38 STORE_NAME               8 (np)
# 
#   4          40 LOAD_CONST               1 (0)
#              42 LOAD_CONST               2 (None)
#              44 IMPORT_NAME              9 (pytest)
#              46 STORE_NAME               9 (pytest)
# 
#   5          48 LOAD_CONST               1 (0)
#              50 LOAD_CONST               3 (('DUDVCurveSkill',))
#              52 IMPORT_NAME             10 (cloudpss_skills_v2.skills.dudv_curve)
#              54 IMPORT_FROM             11 (DUDVCurveSkill)
#              56 STORE_NAME              11 (DUDVCurveSkill)
#              58 POP_TOP
# 
#   8          60 PUSH_NULL
#              62 LOAD_BUILD_CLASS
#              64 LOAD_CONST               4 (<code object TestDUDVValidation at 0x73cd945fdfb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 8>)
#              66 MAKE_FUNCTION            0
#              68 LOAD_CONST               5 ('TestDUDVValidation')
#              70 CALL                     2
#              78 STORE_NAME              12 (TestDUDVValidation)
# 
#  21          80 PUSH_NULL
#              82 LOAD_BUILD_CLASS
#              84 LOAD_CONST               6 (<code object TestDUDVComputation at 0x73cd93b06970, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 21>)
#              86 MAKE_FUNCTION            0
#              88 LOAD_CONST               7 ('TestDUDVComputation')
#              90 CALL                     2
#              98 STORE_NAME              13 (TestDUDVComputation)
# 
#  81         100 PUSH_NULL
#             102 LOAD_BUILD_CLASS
#             104 LOAD_CONST               8 (<code object TestDUDVRun at 0x73cd945fedb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 81>)
#             106 MAKE_FUNCTION            0
#             108 LOAD_CONST               9 ('TestDUDVRun')
#             110 CALL                     2
#             118 STORE_NAME              14 (TestDUDVRun)
#             120 RETURN_CONST             2 (None)
# 
# Disassembly of <code object TestDUDVValidation at 0x73cd945fdfb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 8>:
#   8           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestDUDVValidation')
#               8 STORE_NAME               2 (__qualname__)
# 
#   9          10 LOAD_CONST               1 (<code object test_validate_missing_buses at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 9>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_validate_missing_buses)
# 
#  14          16 LOAD_CONST               2 (<code object test_validate_valid_config at 0x3af90d20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 14>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_validate_valid_config)
#              22 RETURN_CONST             3 (None)
# 
# Disassembly of <code object test_validate_missing_buses at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 9>:
#   9           0 RESUME                   0
# 
#  10           2 LOAD_GLOBAL              1 (NULL + DUDVCurveSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  11          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + validate)
#              44 BUILD_MAP                0
#              46 CALL                     1
#              54 UNPACK_SEQUENCE          2
#              58 STORE_FAST               2 (valid)
#              60 STORE_FAST               3 (errors)
# 
#  12          62 LOAD_CONST               1 (False)
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
# Disassembly of <code object test_validate_valid_config at 0x3af90d20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 14>:
#  14           0 RESUME                   0
# 
#  15           2 LOAD_GLOBAL              1 (NULL + DUDVCurveSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  16          22 LOAD_CONST               1 ('buses')
#              24 LOAD_CONST               2 ('Bus7')
#              26 LOAD_CONST               3 ('Bus16')
#              28 BUILD_LIST               2
#              30 BUILD_MAP                1
#              32 STORE_FAST               2 (config)
# 
#  17          34 LOAD_FAST                1 (skill)
#              36 LOAD_ATTR                3 (NULL|self + validate)
#              56 LOAD_FAST                2 (config)
#              58 CALL                     1
#              66 UNPACK_SEQUENCE          2
#              70 STORE_FAST               3 (valid)
#              72 STORE_FAST               4 (errors)
# 
#  18          74 LOAD_CONST               4 (True)
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
# Disassembly of <code object TestDUDVComputation at 0x73cd93b06970, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 21>:
#  21           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestDUDVComputation')
#               8 STORE_NAME               2 (__qualname__)
# 
#  22          10 LOAD_CONST               1 (<code object test_compute_dudv_points_shape at 0x3afa5260, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 22>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_compute_dudv_points_shape)
# 
#  30          16 LOAD_CONST               2 (<code object test_compute_dudv_points_zero_at_steady at 0x3afa23c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 30>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_compute_dudv_points_zero_at_steady)
# 
#  40          22 LOAD_CONST               3 (<code object test_compute_dudv_points_none_margins at 0x3afa4860, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 40>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_compute_dudv_points_none_margins)
# 
#  47          28 LOAD_CONST               4 (<code object test_extract_dudv_from_result at 0x3af981b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 47>)
#              30 MAKE_FUNCTION            0
#              32 STORE_NAME               6 (test_extract_dudv_from_result)
# 
#  65          34 LOAD_CONST               5 (<code object test_identify_stability_boundary at 0x3afa7720, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 65>)
#              36 MAKE_FUNCTION            0
#              38 STORE_NAME               7 (test_identify_stability_boundary)
# 
#  73          40 LOAD_CONST               6 (<code object test_identify_stability_boundary_none at 0x3af1bad0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 73>)
#              42 MAKE_FUNCTION            0
#              44 STORE_NAME               8 (test_identify_stability_boundary_none)
#              46 RETURN_CONST             7 (None)
# 
# Disassembly of <code object test_compute_dudv_points_shape at 0x3afa5260, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 22>:
#  22           0 RESUME                   0
# 
#  23           2 LOAD_GLOBAL              1 (NULL + DUDVCurveSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  24          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _compute_dudv_points)
# 
#  25          44 LOAD_CONST               1 (1.0)
#              46 LOAD_CONST               2 (0.1)
#              48 LOAD_CONST               3 (-0.1)
#              50 LOAD_CONST               4 (20)
# 
#  24          52 KW_NAMES                 5 (('v_steady', 'dv_up', 'dv_down', 'num_points'))
#              54 CALL                     4
#              62 STORE_FAST               2 (result)
# 
#  27          64 LOAD_FAST                2 (result)
#              66 LOAD_CONST               6 ('voltage')
#              68 BINARY_SUBSCR
#              72 STORE_FAST               3 (@py_assert1)
#              74 LOAD_GLOBAL              5 (NULL + len)
#              84 LOAD_FAST                3 (@py_assert1)
#              86 CALL                     1
#              94 STORE_FAST               4 (@py_assert3)
#              96 LOAD_CONST               4 (20)
#              98 STORE_FAST               5 (@py_assert6)
#             100 LOAD_FAST                4 (@py_assert3)
#             102 LOAD_FAST                5 (@py_assert6)
#             104 COMPARE_OP              40 (==)
#             108 STORE_FAST               6 (@py_assert5)
#             110 LOAD_FAST                6 (@py_assert5)
#             112 POP_JUMP_IF_TRUE       201 (to 516)
#             114 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             124 LOAD_ATTR                8 (_call_reprcompare)
#             144 LOAD_CONST               7 (('==',))
#             146 LOAD_FAST                6 (@py_assert5)
#             148 BUILD_TUPLE              1
#             150 LOAD_CONST               8 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',))
#             152 LOAD_FAST                4 (@py_assert3)
#             154 LOAD_FAST                5 (@py_assert6)
#             156 BUILD_TUPLE              2
#             158 CALL                     4
#             166 LOAD_CONST               9 ('len')
#             168 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             178 LOAD_ATTR               12 (locals)
#             198 CALL                     0
#             206 CONTAINS_OP              0
#             208 POP_JUMP_IF_TRUE        25 (to 260)
#             210 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             220 LOAD_ATTR               14 (_should_repr_global_name)
#             240 LOAD_GLOBAL              4 (len)
#             250 CALL                     1
#             258 POP_JUMP_IF_FALSE       25 (to 310)
#         >>  260 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             270 LOAD_ATTR               16 (_saferepr)
#             290 LOAD_GLOBAL              4 (len)
#             300 CALL                     1
#             308 JUMP_FORWARD             1 (to 312)
#         >>  310 LOAD_CONST               9 ('len')
#         >>  312 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             322 LOAD_ATTR               16 (_saferepr)
#             342 LOAD_FAST                3 (@py_assert1)
#             344 CALL                     1
#             352 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             362 LOAD_ATTR               16 (_saferepr)
#             382 LOAD_FAST                4 (@py_assert3)
#             384 CALL                     1
#             392 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             402 LOAD_ATTR               16 (_saferepr)
#             422 LOAD_FAST                5 (@py_assert6)
#             424 CALL                     1
#             432 LOAD_CONST              10 (('py0', 'py2', 'py4', 'py7'))
#             434 BUILD_CONST_KEY_MAP      4
#             436 BINARY_OP                6 (%)
#             440 STORE_FAST               7 (@py_format8)
#             442 LOAD_CONST              11 ('assert %(py9)s')
#             444 LOAD_CONST              12 ('py9')
#             446 LOAD_FAST                7 (@py_format8)
#             448 BUILD_MAP                1
#             450 BINARY_OP                6 (%)
#             454 STORE_FAST               8 (@py_format10)
#             456 LOAD_GLOBAL             19 (NULL + AssertionError)
#             466 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             476 LOAD_ATTR               20 (_format_explanation)
#             496 LOAD_FAST                8 (@py_format10)
#             498 CALL                     1
#             506 CALL                     1
#             514 RAISE_VARARGS            1
#         >>  516 LOAD_CONST               0 (None)
#             518 COPY                     1
#             520 STORE_FAST               3 (@py_assert1)
#             522 COPY                     1
#             524 STORE_FAST               4 (@py_assert3)
#             526 COPY                     1
#             528 STORE_FAST               6 (@py_assert5)
#             530 STORE_FAST               5 (@py_assert6)
# 
#  28         532 LOAD_FAST                2 (result)
#             534 LOAD_CONST              13 ('dv')
#             536 BINARY_SUBSCR
#             540 STORE_FAST               3 (@py_assert1)
#             542 LOAD_GLOBAL              5 (NULL + len)
#             552 LOAD_FAST                3 (@py_assert1)
#             554 CALL                     1
#             562 STORE_FAST               4 (@py_assert3)
#             564 LOAD_CONST               4 (20)
#             566 STORE_FAST               5 (@py_assert6)
#             568 LOAD_FAST                4 (@py_assert3)
#             570 LOAD_FAST                5 (@py_assert6)
#             572 COMPARE_OP              40 (==)
#             576 STORE_FAST               6 (@py_assert5)
#             578 LOAD_FAST                6 (@py_assert5)
#             580 POP_JUMP_IF_TRUE       201 (to 984)
#             582 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             592 LOAD_ATTR                8 (_call_reprcompare)
#             612 LOAD_CONST               7 (('==',))
#             614 LOAD_FAST                6 (@py_assert5)
#             616 BUILD_TUPLE              1
#             618 LOAD_CONST               8 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',))
#             620 LOAD_FAST                4 (@py_assert3)
#             622 LOAD_FAST                5 (@py_assert6)
#             624 BUILD_TUPLE              2
#             626 CALL                     4
#             634 LOAD_CONST               9 ('len')
#             636 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             646 LOAD_ATTR               12 (locals)
#             666 CALL                     0
#             674 CONTAINS_OP              0
#             676 POP_JUMP_IF_TRUE        25 (to 728)
#             678 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             688 LOAD_ATTR               14 (_should_repr_global_name)
#             708 LOAD_GLOBAL              4 (len)
#             718 CALL                     1
#             726 POP_JUMP_IF_FALSE       25 (to 778)
#         >>  728 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             738 LOAD_ATTR               16 (_saferepr)
#             758 LOAD_GLOBAL              4 (len)
#             768 CALL                     1
#             776 JUMP_FORWARD             1 (to 780)
#         >>  778 LOAD_CONST               9 ('len')
#         >>  780 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             790 LOAD_ATTR               16 (_saferepr)
#             810 LOAD_FAST                3 (@py_assert1)
#             812 CALL                     1
#             820 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             830 LOAD_ATTR               16 (_saferepr)
#             850 LOAD_FAST                4 (@py_assert3)
#             852 CALL                     1
#             860 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             870 LOAD_ATTR               16 (_saferepr)
#             890 LOAD_FAST                5 (@py_assert6)
#             892 CALL                     1
#             900 LOAD_CONST              10 (('py0', 'py2', 'py4', 'py7'))
#             902 BUILD_CONST_KEY_MAP      4
#             904 BINARY_OP                6 (%)
#             908 STORE_FAST               7 (@py_format8)
#             910 LOAD_CONST              11 ('assert %(py9)s')
#             912 LOAD_CONST              12 ('py9')
#             914 LOAD_FAST                7 (@py_format8)
#             916 BUILD_MAP                1
#             918 BINARY_OP                6 (%)
#             922 STORE_FAST               8 (@py_format10)
#             924 LOAD_GLOBAL             19 (NULL + AssertionError)
#             934 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             944 LOAD_ATTR               20 (_format_explanation)
#             964 LOAD_FAST                8 (@py_format10)
#             966 CALL                     1
#             974 CALL                     1
#             982 RAISE_VARARGS            1
#         >>  984 LOAD_CONST               0 (None)
#             986 COPY                     1
#             988 STORE_FAST               3 (@py_assert1)
#             990 COPY                     1
#             992 STORE_FAST               4 (@py_assert3)
#             994 COPY                     1
#             996 STORE_FAST               6 (@py_assert5)
#             998 STORE_FAST               5 (@py_assert6)
#            1000 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_compute_dudv_points_zero_at_steady at 0x3afa23c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 30>:
#  30           0 RESUME                   0
# 
#  31           2 LOAD_GLOBAL              1 (NULL + DUDVCurveSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  32          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _compute_dudv_points)
# 
#  33          44 LOAD_CONST               1 (1.0)
#              46 LOAD_CONST               2 (0.1)
#              48 LOAD_CONST               3 (-0.1)
#              50 LOAD_CONST               4 (21)
# 
#  32          52 KW_NAMES                 5 (('v_steady', 'dv_up', 'dv_down', 'num_points'))
#              54 CALL                     4
#              62 STORE_FAST               2 (result)
# 
#  35          64 LOAD_FAST                2 (result)
#              66 LOAD_CONST               6 ('voltage')
#              68 BINARY_SUBSCR
#              72 STORE_FAST               3 (voltages)
# 
#  36          74 LOAD_FAST                2 (result)
#              76 LOAD_CONST               7 ('dv')
#              78 BINARY_SUBSCR
#              82 STORE_FAST               4 (dv)
# 
#  37          84 LOAD_GLOBAL              5 (NULL + np)
#              94 LOAD_ATTR                6 (argmin)
#             114 LOAD_GLOBAL              5 (NULL + np)
#             124 LOAD_ATTR                8 (abs)
#             144 LOAD_FAST                3 (voltages)
#             146 LOAD_CONST               1 (1.0)
#             148 BINARY_OP               10 (-)
#             152 CALL                     1
#             160 CALL                     1
#             168 STORE_FAST               5 (idx)
# 
#  38         170 LOAD_FAST                4 (dv)
#             172 LOAD_FAST                5 (idx)
#             174 BINARY_SUBSCR
#             178 STORE_FAST               6 (@py_assert1)
#             180 LOAD_GLOBAL              9 (NULL + abs)
#             190 LOAD_FAST                6 (@py_assert1)
#             192 CALL                     1
#             200 STORE_FAST               7 (@py_assert3)
#             202 LOAD_CONST               8 (0.01)
#             204 STORE_FAST               8 (@py_assert6)
#             206 LOAD_FAST                7 (@py_assert3)
#             208 LOAD_FAST                8 (@py_assert6)
#             210 COMPARE_OP               2 (<)
#             214 STORE_FAST               9 (@py_assert5)
#             216 LOAD_FAST                9 (@py_assert5)
#             218 POP_JUMP_IF_TRUE       201 (to 622)
#             220 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             230 LOAD_ATTR               12 (_call_reprcompare)
#             250 LOAD_CONST               9 (('<',))
#             252 LOAD_FAST                9 (@py_assert5)
#             254 BUILD_TUPLE              1
#             256 LOAD_CONST              10 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} < %(py7)s',))
#             258 LOAD_FAST                7 (@py_assert3)
#             260 LOAD_FAST                8 (@py_assert6)
#             262 BUILD_TUPLE              2
#             264 CALL                     4
#             272 LOAD_CONST              11 ('abs')
#             274 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             284 LOAD_ATTR               16 (locals)
#             304 CALL                     0
#             312 CONTAINS_OP              0
#             314 POP_JUMP_IF_TRUE        25 (to 366)
#             316 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             326 LOAD_ATTR               18 (_should_repr_global_name)
#             346 LOAD_GLOBAL              8 (abs)
#             356 CALL                     1
#             364 POP_JUMP_IF_FALSE       25 (to 416)
#         >>  366 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             376 LOAD_ATTR               20 (_saferepr)
#             396 LOAD_GLOBAL              8 (abs)
#             406 CALL                     1
#             414 JUMP_FORWARD             1 (to 418)
#         >>  416 LOAD_CONST              11 ('abs')
#         >>  418 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             428 LOAD_ATTR               20 (_saferepr)
#             448 LOAD_FAST                6 (@py_assert1)
#             450 CALL                     1
#             458 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             468 LOAD_ATTR               20 (_saferepr)
#             488 LOAD_FAST                7 (@py_assert3)
#             490 CALL                     1
#             498 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             508 LOAD_ATTR               20 (_saferepr)
#             528 LOAD_FAST                8 (@py_assert6)
#             530 CALL                     1
#             538 LOAD_CONST              12 (('py0', 'py2', 'py4', 'py7'))
#             540 BUILD_CONST_KEY_MAP      4
#             542 BINARY_OP                6 (%)
#             546 STORE_FAST              10 (@py_format8)
#             548 LOAD_CONST              13 ('assert %(py9)s')
#             550 LOAD_CONST              14 ('py9')
#             552 LOAD_FAST               10 (@py_format8)
#             554 BUILD_MAP                1
#             556 BINARY_OP                6 (%)
#             560 STORE_FAST              11 (@py_format10)
#             562 LOAD_GLOBAL             23 (NULL + AssertionError)
#             572 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             582 LOAD_ATTR               24 (_format_explanation)
#             602 LOAD_FAST               11 (@py_format10)
#             604 CALL                     1
#             612 CALL                     1
#             620 RAISE_VARARGS            1
#         >>  622 LOAD_CONST               0 (None)
#             624 COPY                     1
#             626 STORE_FAST               6 (@py_assert1)
#             628 COPY                     1
#             630 STORE_FAST               7 (@py_assert3)
#             632 COPY                     1
#             634 STORE_FAST               9 (@py_assert5)
#             636 STORE_FAST               8 (@py_assert6)
#             638 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_compute_dudv_points_none_margins at 0x3afa4860, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 40>:
#  40           0 RESUME                   0
# 
#  41           2 LOAD_GLOBAL              1 (NULL + DUDVCurveSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  42          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _compute_dudv_points)
# 
#  43          44 LOAD_CONST               1 (1.0)
#              46 LOAD_CONST               0 (None)
#              48 LOAD_CONST               0 (None)
#              50 LOAD_CONST               2 (10)
# 
#  42          52 KW_NAMES                 3 (('v_steady', 'dv_up', 'dv_down', 'num_points'))
#              54 CALL                     4
#              62 STORE_FAST               2 (result)
# 
#  45          64 LOAD_FAST                2 (result)
#              66 LOAD_CONST               4 ('dv')
#              68 BINARY_SUBSCR
#              72 STORE_FAST               3 (@py_assert1)
#              74 LOAD_GLOBAL              5 (NULL + len)
#              84 LOAD_FAST                3 (@py_assert1)
#              86 CALL                     1
#              94 STORE_FAST               4 (@py_assert3)
#              96 LOAD_CONST               2 (10)
#              98 STORE_FAST               5 (@py_assert6)
#             100 LOAD_FAST                4 (@py_assert3)
#             102 LOAD_FAST                5 (@py_assert6)
#             104 COMPARE_OP              40 (==)
#             108 STORE_FAST               6 (@py_assert5)
#             110 LOAD_FAST                6 (@py_assert5)
#             112 POP_JUMP_IF_TRUE       201 (to 516)
#             114 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             124 LOAD_ATTR                8 (_call_reprcompare)
#             144 LOAD_CONST               5 (('==',))
#             146 LOAD_FAST                6 (@py_assert5)
#             148 BUILD_TUPLE              1
#             150 LOAD_CONST               6 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',))
#             152 LOAD_FAST                4 (@py_assert3)
#             154 LOAD_FAST                5 (@py_assert6)
#             156 BUILD_TUPLE              2
#             158 CALL                     4
#             166 LOAD_CONST               7 ('len')
#             168 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             178 LOAD_ATTR               12 (locals)
#             198 CALL                     0
#             206 CONTAINS_OP              0
#             208 POP_JUMP_IF_TRUE        25 (to 260)
#             210 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             220 LOAD_ATTR               14 (_should_repr_global_name)
#             240 LOAD_GLOBAL              4 (len)
#             250 CALL                     1
#             258 POP_JUMP_IF_FALSE       25 (to 310)
#         >>  260 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             270 LOAD_ATTR               16 (_saferepr)
#             290 LOAD_GLOBAL              4 (len)
#             300 CALL                     1
#             308 JUMP_FORWARD             1 (to 312)
#         >>  310 LOAD_CONST               7 ('len')
#         >>  312 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             322 LOAD_ATTR               16 (_saferepr)
#             342 LOAD_FAST                3 (@py_assert1)
#             344 CALL                     1
#             352 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             362 LOAD_ATTR               16 (_saferepr)
#             382 LOAD_FAST                4 (@py_assert3)
#             384 CALL                     1
#             392 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             402 LOAD_ATTR               16 (_saferepr)
#             422 LOAD_FAST                5 (@py_assert6)
#             424 CALL                     1
#             432 LOAD_CONST               8 (('py0', 'py2', 'py4', 'py7'))
#             434 BUILD_CONST_KEY_MAP      4
#             436 BINARY_OP                6 (%)
#             440 STORE_FAST               7 (@py_format8)
#             442 LOAD_CONST               9 ('assert %(py9)s')
#             444 LOAD_CONST              10 ('py9')
#             446 LOAD_FAST                7 (@py_format8)
#             448 BUILD_MAP                1
#             450 BINARY_OP                6 (%)
#             454 STORE_FAST               8 (@py_format10)
#             456 LOAD_GLOBAL             19 (NULL + AssertionError)
#             466 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             476 LOAD_ATTR               20 (_format_explanation)
#             496 LOAD_FAST                8 (@py_format10)
#             498 CALL                     1
#             506 CALL                     1
#             514 RAISE_VARARGS            1
#         >>  516 LOAD_CONST               0 (None)
#             518 COPY                     1
#             520 STORE_FAST               3 (@py_assert1)
#             522 COPY                     1
#             524 STORE_FAST               4 (@py_assert3)
#             526 COPY                     1
#             528 STORE_FAST               6 (@py_assert5)
#             530 STORE_FAST               5 (@py_assert6)
#             532 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_extract_dudv_from_result at 0x3af981b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 47>:
#  47           0 RESUME                   0
# 
#  48           2 LOAD_GLOBAL              1 (NULL + DUDVCurveSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  50          22 LOAD_CONST               1 ('channel_results')
# 
#  52          24 LOAD_CONST               2 ('Bus7')
# 
#  53          26 LOAD_CONST               3 (1.0)
#              28 LOAD_CONST               4 (0.05)
#              30 LOAD_CONST               5 (-0.08)
#              32 LOAD_CONST               6 (('v_steady', 'dv_up', 'dv_down'))
#              34 BUILD_CONST_KEY_MAP      3
# 
#  51          36 LOAD_CONST               7 (('name', 'dv'))
#              38 BUILD_CONST_KEY_MAP      2
# 
#  56          40 LOAD_CONST               8 ('Bus16')
# 
#  57          42 LOAD_CONST               9 (0.98)
#              44 LOAD_CONST              10 (0.02)
#              46 LOAD_CONST              11 (-0.12)
#              48 LOAD_CONST               6 (('v_steady', 'dv_up', 'dv_down'))
#              50 BUILD_CONST_KEY_MAP      3
# 
#  55          52 LOAD_CONST               7 (('name', 'dv'))
#              54 BUILD_CONST_KEY_MAP      2
# 
#  50          56 BUILD_LIST               2
# 
#  49          58 BUILD_MAP                1
#              60 STORE_FAST               2 (result_data)
# 
#  61          62 LOAD_FAST                1 (skill)
#              64 LOAD_ATTR                3 (NULL|self + _extract_dudv_from_result)
#              84 LOAD_FAST                2 (result_data)
#              86 LOAD_CONST               2 ('Bus7')
#              88 BUILD_LIST               1
#              90 CALL                     2
#              98 STORE_FAST               3 (extracted)
# 
#  62         100 LOAD_CONST               2 ('Bus7')
#             102 STORE_FAST               4 (@py_assert0)
#             104 LOAD_FAST                4 (@py_assert0)
#             106 LOAD_FAST                3 (extracted)
#             108 CONTAINS_OP              0
#             110 STORE_FAST               5 (@py_assert2)
#             112 LOAD_FAST                5 (@py_assert2)
#             114 POP_JUMP_IF_TRUE       153 (to 422)
#             116 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             126 LOAD_ATTR                6 (_call_reprcompare)
#             146 LOAD_CONST              12 (('in',))
#             148 LOAD_FAST                5 (@py_assert2)
#             150 BUILD_TUPLE              1
#             152 LOAD_CONST              13 (('%(py1)s in %(py3)s',))
#             154 LOAD_FAST                4 (@py_assert0)
#             156 LOAD_FAST                3 (extracted)
#             158 BUILD_TUPLE              2
#             160 CALL                     4
#             168 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             178 LOAD_ATTR                8 (_saferepr)
#             198 LOAD_FAST                4 (@py_assert0)
#             200 CALL                     1
#             208 LOAD_CONST              14 ('extracted')
#             210 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             220 LOAD_ATTR               12 (locals)
#             240 CALL                     0
#             248 CONTAINS_OP              0
#             250 POP_JUMP_IF_TRUE        21 (to 294)
#             252 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             262 LOAD_ATTR               14 (_should_repr_global_name)
#             282 LOAD_FAST                3 (extracted)
#             284 CALL                     1
#             292 POP_JUMP_IF_FALSE       21 (to 336)
#         >>  294 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             304 LOAD_ATTR                8 (_saferepr)
#             324 LOAD_FAST                3 (extracted)
#             326 CALL                     1
#             334 JUMP_FORWARD             1 (to 338)
#         >>  336 LOAD_CONST              14 ('extracted')
#         >>  338 LOAD_CONST              15 (('py1', 'py3'))
#             340 BUILD_CONST_KEY_MAP      2
#             342 BINARY_OP                6 (%)
#             346 STORE_FAST               6 (@py_format4)
#             348 LOAD_CONST              16 ('assert %(py5)s')
#             350 LOAD_CONST              17 ('py5')
#             352 LOAD_FAST                6 (@py_format4)
#             354 BUILD_MAP                1
#             356 BINARY_OP                6 (%)
#             360 STORE_FAST               7 (@py_format6)
#             362 LOAD_GLOBAL             17 (NULL + AssertionError)
#             372 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             382 LOAD_ATTR               18 (_format_explanation)
#             402 LOAD_FAST                7 (@py_format6)
#             404 CALL                     1
#             412 CALL                     1
#             420 RAISE_VARARGS            1
#         >>  422 LOAD_CONST               0 (None)
#             424 COPY                     1
#             426 STORE_FAST               4 (@py_assert0)
#             428 STORE_FAST               5 (@py_assert2)
# 
#  63         430 LOAD_CONST               8 ('Bus16')
#             432 STORE_FAST               4 (@py_assert0)
#             434 LOAD_FAST                4 (@py_assert0)
#             436 LOAD_FAST                3 (extracted)
#             438 CONTAINS_OP              1
#             440 STORE_FAST               5 (@py_assert2)
#             442 LOAD_FAST                5 (@py_assert2)
#             444 POP_JUMP_IF_TRUE       153 (to 752)
#             446 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             456 LOAD_ATTR                6 (_call_reprcompare)
#             476 LOAD_CONST              18 (('not in',))
#             478 LOAD_FAST                5 (@py_assert2)
#             480 BUILD_TUPLE              1
#             482 LOAD_CONST              19 (('%(py1)s not in %(py3)s',))
#             484 LOAD_FAST                4 (@py_assert0)
#             486 LOAD_FAST                3 (extracted)
#             488 BUILD_TUPLE              2
#             490 CALL                     4
#             498 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             508 LOAD_ATTR                8 (_saferepr)
#             528 LOAD_FAST                4 (@py_assert0)
#             530 CALL                     1
#             538 LOAD_CONST              14 ('extracted')
#             540 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             550 LOAD_ATTR               12 (locals)
#             570 CALL                     0
#             578 CONTAINS_OP              0
#             580 POP_JUMP_IF_TRUE        21 (to 624)
#             582 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             592 LOAD_ATTR               14 (_should_repr_global_name)
#             612 LOAD_FAST                3 (extracted)
#             614 CALL                     1
#             622 POP_JUMP_IF_FALSE       21 (to 666)
#         >>  624 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             634 LOAD_ATTR                8 (_saferepr)
#             654 LOAD_FAST                3 (extracted)
#             656 CALL                     1
#             664 JUMP_FORWARD             1 (to 668)
#         >>  666 LOAD_CONST              14 ('extracted')
#         >>  668 LOAD_CONST              15 (('py1', 'py3'))
#             670 BUILD_CONST_KEY_MAP      2
#             672 BINARY_OP                6 (%)
#             676 STORE_FAST               6 (@py_format4)
#             678 LOAD_CONST              16 ('assert %(py5)s')
#             680 LOAD_CONST              17 ('py5')
#             682 LOAD_FAST                6 (@py_format4)
#             684 BUILD_MAP                1
#             686 BINARY_OP                6 (%)
#             690 STORE_FAST               7 (@py_format6)
#             692 LOAD_GLOBAL             17 (NULL + AssertionError)
#             702 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             712 LOAD_ATTR               18 (_format_explanation)
#             732 LOAD_FAST                7 (@py_format6)
#             734 CALL                     1
#             742 CALL                     1
#             750 RAISE_VARARGS            1
#         >>  752 LOAD_CONST               0 (None)
#             754 COPY                     1
#             756 STORE_FAST               4 (@py_assert0)
#             758 STORE_FAST               5 (@py_assert2)
#             760 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_identify_stability_boundary at 0x3afa7720, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 65>:
#  65           0 RESUME                   0
# 
#  66           2 LOAD_GLOBAL              1 (NULL + DUDVCurveSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  67          22 LOAD_GLOBAL              3 (NULL + np)
#              32 LOAD_ATTR                4 (array)
#              52 BUILD_LIST               0
#              54 LOAD_CONST               1 ((0.8, 0.9, 1.0, 1.1, 1.2))
#              56 LIST_EXTEND              1
#              58 CALL                     1
#              66 STORE_FAST               2 (voltage)
# 
#  68          68 LOAD_GLOBAL              3 (NULL + np)
#              78 LOAD_ATTR                4 (array)
#              98 BUILD_LIST               0
#             100 LOAD_CONST               2 ((0.1, 0.05, 0.0, -0.03, -0.08))
#             102 LIST_EXTEND              1
#             104 CALL                     1
#             112 STORE_FAST               3 (dv)
# 
#  69         114 LOAD_FAST                1 (skill)
#             116 LOAD_ATTR                7 (NULL|self + _identify_stability_boundary)
#             136 LOAD_FAST                2 (voltage)
#             138 LOAD_FAST                3 (dv)
#             140 CALL                     2
#             148 STORE_FAST               4 (boundary)
# 
#  70         150 LOAD_CONST               0 (None)
#             152 STORE_FAST               5 (@py_assert2)
#             154 LOAD_FAST                4 (boundary)
#             156 LOAD_FAST                5 (@py_assert2)
#             158 IS_OP                    1
#             160 STORE_FAST               6 (@py_assert1)
#             162 LOAD_FAST                6 (@py_assert1)
#             164 POP_JUMP_IF_TRUE       153 (to 472)
#             166 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             176 LOAD_ATTR               10 (_call_reprcompare)
#             196 LOAD_CONST               3 (('is not',))
#             198 LOAD_FAST                6 (@py_assert1)
#             200 BUILD_TUPLE              1
#             202 LOAD_CONST               4 (('%(py0)s is not %(py3)s',))
#             204 LOAD_FAST                4 (boundary)
#             206 LOAD_FAST                5 (@py_assert2)
#             208 BUILD_TUPLE              2
#             210 CALL                     4
#             218 LOAD_CONST               5 ('boundary')
#             220 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             230 LOAD_ATTR               14 (locals)
#             250 CALL                     0
#             258 CONTAINS_OP              0
#             260 POP_JUMP_IF_TRUE        21 (to 304)
#             262 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             272 LOAD_ATTR               16 (_should_repr_global_name)
#             292 LOAD_FAST                4 (boundary)
#             294 CALL                     1
#             302 POP_JUMP_IF_FALSE       21 (to 346)
#         >>  304 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             314 LOAD_ATTR               18 (_saferepr)
#             334 LOAD_FAST                4 (boundary)
#             336 CALL                     1
#             344 JUMP_FORWARD             1 (to 348)
#         >>  346 LOAD_CONST               5 ('boundary')
#         >>  348 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             358 LOAD_ATTR               18 (_saferepr)
#             378 LOAD_FAST                5 (@py_assert2)
#             380 CALL                     1
#             388 LOAD_CONST               6 (('py0', 'py3'))
#             390 BUILD_CONST_KEY_MAP      2
#             392 BINARY_OP                6 (%)
#             396 STORE_FAST               7 (@py_format4)
#             398 LOAD_CONST               7 ('assert %(py5)s')
#             400 LOAD_CONST               8 ('py5')
#             402 LOAD_FAST                7 (@py_format4)
#             404 BUILD_MAP                1
#             406 BINARY_OP                6 (%)
#             410 STORE_FAST               8 (@py_format6)
#             412 LOAD_GLOBAL             21 (NULL + AssertionError)
#             422 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             432 LOAD_ATTR               22 (_format_explanation)
#             452 LOAD_FAST                8 (@py_format6)
#             454 CALL                     1
#             462 CALL                     1
#             470 RAISE_VARARGS            1
#         >>  472 LOAD_CONST               0 (None)
#             474 COPY                     1
#             476 STORE_FAST               6 (@py_assert1)
#             478 STORE_FAST               5 (@py_assert2)
# 
#  71         480 LOAD_CONST               9 (1.0)
#             482 STORE_FAST               9 (@py_assert0)
#             484 LOAD_FAST                9 (@py_assert0)
#             486 LOAD_FAST                4 (boundary)
#             488 COMPARE_OP              26 (<=)
#             492 STORE_FAST               5 (@py_assert2)
#             494 LOAD_CONST              10 (1.1)
#             496 STORE_FAST              10 (@py_assert5)
#             498 LOAD_FAST                4 (boundary)
#             500 LOAD_FAST               10 (@py_assert5)
#             502 COMPARE_OP              26 (<=)
#             506 STORE_FAST              11 (@py_assert3)
#             508 LOAD_FAST                5 (@py_assert2)
#             510 POP_JUMP_IF_FALSE        2 (to 516)
#             512 LOAD_FAST               11 (@py_assert3)
#             514 POP_JUMP_IF_TRUE       175 (to 866)
#         >>  516 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             526 LOAD_ATTR               10 (_call_reprcompare)
#             546 LOAD_CONST              11 (('<=', '<='))
#             548 LOAD_FAST                5 (@py_assert2)
#             550 LOAD_FAST               11 (@py_assert3)
#             552 BUILD_TUPLE              2
#             554 LOAD_CONST              12 (('%(py1)s <= %(py4)s', '%(py4)s <= %(py6)s'))
#             556 LOAD_FAST                9 (@py_assert0)
#             558 LOAD_FAST                4 (boundary)
#             560 LOAD_FAST               10 (@py_assert5)
#             562 BUILD_TUPLE              3
#             564 CALL                     4
#             572 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             582 LOAD_ATTR               18 (_saferepr)
#             602 LOAD_FAST                9 (@py_assert0)
#             604 CALL                     1
#             612 LOAD_CONST               5 ('boundary')
#             614 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             624 LOAD_ATTR               14 (locals)
#             644 CALL                     0
#             652 CONTAINS_OP              0
#             654 POP_JUMP_IF_TRUE        21 (to 698)
#             656 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             666 LOAD_ATTR               16 (_should_repr_global_name)
#             686 LOAD_FAST                4 (boundary)
#             688 CALL                     1
#             696 POP_JUMP_IF_FALSE       21 (to 740)
#         >>  698 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             708 LOAD_ATTR               18 (_saferepr)
#             728 LOAD_FAST                4 (boundary)
#             730 CALL                     1
#             738 JUMP_FORWARD             1 (to 742)
#         >>  740 LOAD_CONST               5 ('boundary')
#         >>  742 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             752 LOAD_ATTR               18 (_saferepr)
#             772 LOAD_FAST               10 (@py_assert5)
#             774 CALL                     1
#             782 LOAD_CONST              13 (('py1', 'py4', 'py6'))
#             784 BUILD_CONST_KEY_MAP      3
#             786 BINARY_OP                6 (%)
#             790 STORE_FAST              12 (@py_format7)
#             792 LOAD_CONST              14 ('assert %(py8)s')
#             794 LOAD_CONST              15 ('py8')
#             796 LOAD_FAST               12 (@py_format7)
#             798 BUILD_MAP                1
#             800 BINARY_OP                6 (%)
#             804 STORE_FAST              13 (@py_format9)
#             806 LOAD_GLOBAL             21 (NULL + AssertionError)
#             816 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             826 LOAD_ATTR               22 (_format_explanation)
#             846 LOAD_FAST               13 (@py_format9)
#             848 CALL                     1
#             856 CALL                     1
#             864 RAISE_VARARGS            1
#         >>  866 LOAD_CONST               0 (None)
#             868 COPY                     1
#             870 STORE_FAST               9 (@py_assert0)
#             872 COPY                     1
#             874 STORE_FAST               5 (@py_assert2)
#             876 COPY                     1
#             878 STORE_FAST              11 (@py_assert3)
#             880 STORE_FAST              10 (@py_assert5)
#             882 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_identify_stability_boundary_none at 0x3af1bad0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 73>:
#  73           0 RESUME                   0
# 
#  74           2 LOAD_GLOBAL              1 (NULL + DUDVCurveSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  75          22 LOAD_GLOBAL              3 (NULL + np)
#              32 LOAD_ATTR                4 (array)
#              52 BUILD_LIST               0
#              54 LOAD_CONST               1 ((0.8, 0.9, 1.0, 1.1, 1.2))
#              56 LIST_EXTEND              1
#              58 CALL                     1
#              66 STORE_FAST               2 (voltage)
# 
#  76          68 LOAD_GLOBAL              3 (NULL + np)
#              78 LOAD_ATTR                4 (array)
#              98 BUILD_LIST               0
#             100 LOAD_CONST               2 ((0.1, 0.05, 0.02, 0.01, 0.0))
#             102 LIST_EXTEND              1
#             104 CALL                     1
#             112 STORE_FAST               3 (dv)
# 
#  77         114 LOAD_FAST                1 (skill)
#             116 LOAD_ATTR                7 (NULL|self + _identify_stability_boundary)
#             136 LOAD_FAST                2 (voltage)
#             138 LOAD_FAST                3 (dv)
#             140 CALL                     2
#             148 STORE_FAST               4 (boundary)
# 
#  78         150 LOAD_CONST               0 (None)
#             152 STORE_FAST               5 (@py_assert2)
#             154 LOAD_FAST                4 (boundary)
#             156 LOAD_FAST                5 (@py_assert2)
#             158 IS_OP                    0
#             160 STORE_FAST               6 (@py_assert1)
#             162 LOAD_FAST                6 (@py_assert1)
#             164 POP_JUMP_IF_TRUE       153 (to 472)
#             166 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             176 LOAD_ATTR               10 (_call_reprcompare)
#             196 LOAD_CONST               3 (('is',))
#             198 LOAD_FAST                6 (@py_assert1)
#             200 BUILD_TUPLE              1
#             202 LOAD_CONST               4 (('%(py0)s is %(py3)s',))
#             204 LOAD_FAST                4 (boundary)
#             206 LOAD_FAST                5 (@py_assert2)
#             208 BUILD_TUPLE              2
#             210 CALL                     4
#             218 LOAD_CONST               5 ('boundary')
#             220 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             230 LOAD_ATTR               14 (locals)
#             250 CALL                     0
#             258 CONTAINS_OP              0
#             260 POP_JUMP_IF_TRUE        21 (to 304)
#             262 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             272 LOAD_ATTR               16 (_should_repr_global_name)
#             292 LOAD_FAST                4 (boundary)
#             294 CALL                     1
#             302 POP_JUMP_IF_FALSE       21 (to 346)
#         >>  304 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             314 LOAD_ATTR               18 (_saferepr)
#             334 LOAD_FAST                4 (boundary)
#             336 CALL                     1
#             344 JUMP_FORWARD             1 (to 348)
#         >>  346 LOAD_CONST               5 ('boundary')
#         >>  348 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             358 LOAD_ATTR               18 (_saferepr)
#             378 LOAD_FAST                5 (@py_assert2)
#             380 CALL                     1
#             388 LOAD_CONST               6 (('py0', 'py3'))
#             390 BUILD_CONST_KEY_MAP      2
#             392 BINARY_OP                6 (%)
#             396 STORE_FAST               7 (@py_format4)
#             398 LOAD_CONST               7 ('assert %(py5)s')
#             400 LOAD_CONST               8 ('py5')
#             402 LOAD_FAST                7 (@py_format4)
#             404 BUILD_MAP                1
#             406 BINARY_OP                6 (%)
#             410 STORE_FAST               8 (@py_format6)
#             412 LOAD_GLOBAL             21 (NULL + AssertionError)
#             422 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             432 LOAD_ATTR               22 (_format_explanation)
#             452 LOAD_FAST                8 (@py_format6)
#             454 CALL                     1
#             462 CALL                     1
#             470 RAISE_VARARGS            1
#         >>  472 LOAD_CONST               0 (None)
#             474 COPY                     1
#             476 STORE_FAST               6 (@py_assert1)
#             478 STORE_FAST               5 (@py_assert2)
#             480 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestDUDVRun at 0x73cd945fedb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 81>:
#  81           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestDUDVRun')
#               8 STORE_NAME               2 (__qualname__)
# 
#  82          10 LOAD_CONST               1 (<code object test_run_invalid_config_returns_failure at 0x3afa13e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 82>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_run_invalid_config_returns_failure)
#              16 RETURN_CONST             2 (None)
# 
# Disassembly of <code object test_run_invalid_config_returns_failure at 0x3afa13e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_dudv_curve.py", line 82>:
#  82           0 RESUME                   0
# 
#  83           2 LOAD_GLOBAL              1 (NULL + DUDVCurveSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  84          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + run)
#              44 BUILD_MAP                0
#              46 CALL                     1
#              54 STORE_FAST               2 (result)
# 
#  85          56 LOAD_FAST                2 (result)
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