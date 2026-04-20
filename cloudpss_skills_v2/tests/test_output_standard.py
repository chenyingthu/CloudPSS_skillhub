# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/__pycache__/test_output_standard.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


def TestSkillResult():
    """TestSkillResult"""
pass  # TODO: restore


def TestSkillOutputValidator():
    """TestSkillOutputValidator"""
pass  # TODO: restore


def TestFieldNormalization():
    """TestFieldNormalization"""
pass  # TODO: restore


def TestEnhancedFailurePath():
    """TestEnhancedFailurePath"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('Tests for output standard compliance.')
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
#              42 LOAD_CONST               3 (('datetime',))
#              44 IMPORT_NAME              8 (datetime)
#              46 IMPORT_FROM              8 (datetime)
#              48 STORE_NAME               8 (datetime)
#              50 POP_TOP
# 
#   5          52 LOAD_CONST               1 (0)
#              54 LOAD_CONST               4 (('SkillResult', 'SkillStatus', 'SkillOutputValidator'))
#              56 IMPORT_NAME              9 (cloudpss_skills_v2.core)
#              58 IMPORT_FROM             10 (SkillResult)
#              60 STORE_NAME              10 (SkillResult)
#              62 IMPORT_FROM             11 (SkillStatus)
#              64 STORE_NAME              11 (SkillStatus)
#              66 IMPORT_FROM             12 (SkillOutputValidator)
#              68 STORE_NAME              12 (SkillOutputValidator)
#              70 POP_TOP
# 
#   8          72 PUSH_NULL
#              74 LOAD_BUILD_CLASS
#              76 LOAD_CONST               5 (<code object TestSkillResult at 0x73cd93b31a30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 8>)
#              78 MAKE_FUNCTION            0
#              80 LOAD_CONST               6 ('TestSkillResult')
#              82 CALL                     2
#              90 STORE_NAME              13 (TestSkillResult)
# 
#  77          92 PUSH_NULL
#              94 LOAD_BUILD_CLASS
#              96 LOAD_CONST               7 (<code object TestSkillOutputValidator at 0x73cd93b31930, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 77>)
#              98 MAKE_FUNCTION            0
#             100 LOAD_CONST               8 ('TestSkillOutputValidator')
#             102 CALL                     2
#             110 STORE_NAME              14 (TestSkillOutputValidator)
# 
# 154         112 PUSH_NULL
#             114 LOAD_BUILD_CLASS
#             116 LOAD_CONST               9 (<code object TestFieldNormalization at 0x73cd945ff210, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 154>)
#             118 MAKE_FUNCTION            0
#             120 LOAD_CONST              10 ('TestFieldNormalization')
#             122 CALL                     2
#             130 STORE_NAME              15 (TestFieldNormalization)
# 
# 180         132 PUSH_NULL
#             134 LOAD_BUILD_CLASS
#             136 LOAD_CONST              11 (<code object TestEnhancedFailurePath at 0x73cd945feb10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 180>)
#             138 MAKE_FUNCTION            0
#             140 LOAD_CONST              12 ('TestEnhancedFailurePath')
#             142 CALL                     2
#             150 STORE_NAME              16 (TestEnhancedFailurePath)
#             152 RETURN_CONST             2 (None)
# 
# Disassembly of <code object TestSkillResult at 0x73cd93b31a30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 8>:
#   8           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestSkillResult')
#               8 STORE_NAME               2 (__qualname__)
# 
#   9          10 LOAD_CONST               1 (<code object test_create_success_result at 0x3afa8100, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 9>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_create_success_result)
# 
#  19          16 LOAD_CONST               2 (<code object test_create_failure_result at 0x3afab1c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 19>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_create_failure_result)
# 
#  31          22 LOAD_CONST               3 (<code object test_create_running_result at 0x3afa6250, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 31>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_create_running_result)
# 
#  37          28 LOAD_CONST               4 (<code object test_add_log at 0x3aed0fc0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 37>)
#              30 MAKE_FUNCTION            0
#              32 STORE_NAME               6 (test_add_log)
# 
#  44          34 LOAD_CONST               5 (<code object test_add_artifact at 0x3aed1ba0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 44>)
#              36 MAKE_FUNCTION            0
#              38 STORE_NAME               7 (test_add_artifact)
# 
#  51          40 LOAD_CONST               6 (<code object test_to_dict at 0x3afabac0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 51>)
#              42 MAKE_FUNCTION            0
#              44 STORE_NAME               8 (test_to_dict)
# 
#  59          46 LOAD_CONST               7 (<code object test_duration_calculation at 0x3aefe140, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 59>)
#              48 MAKE_FUNCTION            0
#              50 STORE_NAME               9 (test_duration_calculation)
# 
#  69          52 LOAD_CONST               8 (<code object test_has_error at 0x3aed21e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 69>)
#              54 MAKE_FUNCTION            0
#              56 STORE_NAME              10 (test_has_error)
#              58 RETURN_CONST             9 (None)
# 
# Disassembly of <code object test_create_success_result at 0x3afa8100, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 9>:
#   9           0 RESUME                   0
# 
#  10           2 LOAD_GLOBAL              1 (NULL + SkillResult)
#              12 LOAD_ATTR                2 (success)
# 
#  11          32 LOAD_CONST               1 ('test_skill')
# 
#  12          34 LOAD_CONST               2 ('value')
#              36 LOAD_CONST               3 (42)
#              38 BUILD_MAP                1
# 
#  10          40 KW_NAMES                 4 (('skill_name', 'data'))
#              42 CALL                     2
#              50 STORE_FAST               1 (result)
# 
#  14          52 LOAD_FAST                1 (result)
#              54 LOAD_ATTR                4 (skill_name)
#              74 STORE_FAST               2 (@py_assert1)
#              76 LOAD_CONST               1 ('test_skill')
#              78 STORE_FAST               3 (@py_assert4)
#              80 LOAD_FAST                2 (@py_assert1)
#              82 LOAD_FAST                3 (@py_assert4)
#              84 COMPARE_OP              40 (==)
#              88 STORE_FAST               4 (@py_assert3)
#              90 LOAD_FAST                4 (@py_assert3)
#              92 POP_JUMP_IF_TRUE       173 (to 440)
#              94 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             104 LOAD_ATTR                8 (_call_reprcompare)
#             124 LOAD_CONST               5 (('==',))
#             126 LOAD_FAST                4 (@py_assert3)
#             128 BUILD_TUPLE              1
#             130 LOAD_CONST               6 (('%(py2)s\n{%(py2)s = %(py0)s.skill_name\n} == %(py5)s',))
#             132 LOAD_FAST                2 (@py_assert1)
#             134 LOAD_FAST                3 (@py_assert4)
#             136 BUILD_TUPLE              2
#             138 CALL                     4
#             146 LOAD_CONST               7 ('result')
#             148 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             158 LOAD_ATTR               12 (locals)
#             178 CALL                     0
#             186 CONTAINS_OP              0
#             188 POP_JUMP_IF_TRUE        21 (to 232)
#             190 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             200 LOAD_ATTR               14 (_should_repr_global_name)
#             220 LOAD_FAST                1 (result)
#             222 CALL                     1
#             230 POP_JUMP_IF_FALSE       21 (to 274)
#         >>  232 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             242 LOAD_ATTR               16 (_saferepr)
#             262 LOAD_FAST                1 (result)
#             264 CALL                     1
#             272 JUMP_FORWARD             1 (to 276)
#         >>  274 LOAD_CONST               7 ('result')
#         >>  276 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             286 LOAD_ATTR               16 (_saferepr)
#             306 LOAD_FAST                2 (@py_assert1)
#             308 CALL                     1
#             316 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             326 LOAD_ATTR               16 (_saferepr)
#             346 LOAD_FAST                3 (@py_assert4)
#             348 CALL                     1
#             356 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#             358 BUILD_CONST_KEY_MAP      3
#             360 BINARY_OP                6 (%)
#             364 STORE_FAST               5 (@py_format6)
#             366 LOAD_CONST               9 ('assert %(py7)s')
#             368 LOAD_CONST              10 ('py7')
#             370 LOAD_FAST                5 (@py_format6)
#             372 BUILD_MAP                1
#             374 BINARY_OP                6 (%)
#             378 STORE_FAST               6 (@py_format8)
#             380 LOAD_GLOBAL             19 (NULL + AssertionError)
#             390 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             400 LOAD_ATTR               20 (_format_explanation)
#             420 LOAD_FAST                6 (@py_format8)
#             422 CALL                     1
#             430 CALL                     1
#             438 RAISE_VARARGS            1
#         >>  440 LOAD_CONST               0 (None)
#             442 COPY                     1
#             444 STORE_FAST               2 (@py_assert1)
#             446 COPY                     1
#             448 STORE_FAST               4 (@py_assert3)
#             450 STORE_FAST               3 (@py_assert4)
# 
#  15         452 LOAD_FAST                1 (result)
#             454 LOAD_ATTR               22 (status)
#             474 STORE_FAST               2 (@py_assert1)
#             476 LOAD_GLOBAL             24 (SkillStatus)
#             486 LOAD_ATTR               26 (SUCCESS)
#             506 STORE_FAST               7 (@py_assert5)
#             508 LOAD_FAST                2 (@py_assert1)
#             510 LOAD_FAST                7 (@py_assert5)
#             512 COMPARE_OP              40 (==)
#             516 STORE_FAST               4 (@py_assert3)
#             518 LOAD_FAST                4 (@py_assert3)
#             520 POP_JUMP_IF_TRUE       246 (to 1014)
#             522 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             532 LOAD_ATTR                8 (_call_reprcompare)
#             552 LOAD_CONST               5 (('==',))
#             554 LOAD_FAST                4 (@py_assert3)
#             556 BUILD_TUPLE              1
#             558 LOAD_CONST              11 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.SUCCESS\n}',))
#             560 LOAD_FAST                2 (@py_assert1)
#             562 LOAD_FAST                7 (@py_assert5)
#             564 BUILD_TUPLE              2
#             566 CALL                     4
#             574 LOAD_CONST               7 ('result')
#             576 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             586 LOAD_ATTR               12 (locals)
#             606 CALL                     0
#             614 CONTAINS_OP              0
#             616 POP_JUMP_IF_TRUE        21 (to 660)
#             618 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             628 LOAD_ATTR               14 (_should_repr_global_name)
#             648 LOAD_FAST                1 (result)
#             650 CALL                     1
#             658 POP_JUMP_IF_FALSE       21 (to 702)
#         >>  660 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             670 LOAD_ATTR               16 (_saferepr)
#             690 LOAD_FAST                1 (result)
#             692 CALL                     1
#             700 JUMP_FORWARD             1 (to 704)
#         >>  702 LOAD_CONST               7 ('result')
#         >>  704 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             714 LOAD_ATTR               16 (_saferepr)
#             734 LOAD_FAST                2 (@py_assert1)
#             736 CALL                     1
#             744 LOAD_CONST              12 ('SkillStatus')
#             746 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             756 LOAD_ATTR               12 (locals)
#             776 CALL                     0
#             784 CONTAINS_OP              0
#             786 POP_JUMP_IF_TRUE        25 (to 838)
#             788 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             798 LOAD_ATTR               14 (_should_repr_global_name)
#             818 LOAD_GLOBAL             24 (SkillStatus)
#             828 CALL                     1
#             836 POP_JUMP_IF_FALSE       25 (to 888)
#         >>  838 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             848 LOAD_ATTR               16 (_saferepr)
#             868 LOAD_GLOBAL             24 (SkillStatus)
#             878 CALL                     1
#             886 JUMP_FORWARD             1 (to 890)
#         >>  888 LOAD_CONST              12 ('SkillStatus')
#         >>  890 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             900 LOAD_ATTR               16 (_saferepr)
#             920 LOAD_FAST                7 (@py_assert5)
#             922 CALL                     1
#             930 LOAD_CONST              13 (('py0', 'py2', 'py4', 'py6'))
#             932 BUILD_CONST_KEY_MAP      4
#             934 BINARY_OP                6 (%)
#             938 STORE_FAST               8 (@py_format7)
#             940 LOAD_CONST              14 ('assert %(py8)s')
#             942 LOAD_CONST              15 ('py8')
#             944 LOAD_FAST                8 (@py_format7)
#             946 BUILD_MAP                1
#             948 BINARY_OP                6 (%)
#             952 STORE_FAST               9 (@py_format9)
#             954 LOAD_GLOBAL             19 (NULL + AssertionError)
#             964 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             974 LOAD_ATTR               20 (_format_explanation)
#             994 LOAD_FAST                9 (@py_format9)
#             996 CALL                     1
#            1004 CALL                     1
#            1012 RAISE_VARARGS            1
#         >> 1014 LOAD_CONST               0 (None)
#            1016 COPY                     1
#            1018 STORE_FAST               2 (@py_assert1)
#            1020 COPY                     1
#            1022 STORE_FAST               4 (@py_assert3)
#            1024 STORE_FAST               7 (@py_assert5)
# 
#  16        1026 LOAD_FAST                1 (result)
#            1028 LOAD_ATTR               28 (is_success)
#            1048 STORE_FAST               2 (@py_assert1)
#            1050 LOAD_CONST              16 (True)
#            1052 STORE_FAST               3 (@py_assert4)
#            1054 LOAD_FAST                2 (@py_assert1)
#            1056 LOAD_FAST                3 (@py_assert4)
#            1058 IS_OP                    0
#            1060 STORE_FAST               4 (@py_assert3)
#            1062 LOAD_FAST                4 (@py_assert3)
#            1064 POP_JUMP_IF_TRUE       173 (to 1412)
#            1066 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1076 LOAD_ATTR                8 (_call_reprcompare)
#            1096 LOAD_CONST              17 (('is',))
#            1098 LOAD_FAST                4 (@py_assert3)
#            1100 BUILD_TUPLE              1
#            1102 LOAD_CONST              18 (('%(py2)s\n{%(py2)s = %(py0)s.is_success\n} is %(py5)s',))
#            1104 LOAD_FAST                2 (@py_assert1)
#            1106 LOAD_FAST                3 (@py_assert4)
#            1108 BUILD_TUPLE              2
#            1110 CALL                     4
#            1118 LOAD_CONST               7 ('result')
#            1120 LOAD_GLOBAL             11 (NULL + @py_builtins)
#            1130 LOAD_ATTR               12 (locals)
#            1150 CALL                     0
#            1158 CONTAINS_OP              0
#            1160 POP_JUMP_IF_TRUE        21 (to 1204)
#            1162 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1172 LOAD_ATTR               14 (_should_repr_global_name)
#            1192 LOAD_FAST                1 (result)
#            1194 CALL                     1
#            1202 POP_JUMP_IF_FALSE       21 (to 1246)
#         >> 1204 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1214 LOAD_ATTR               16 (_saferepr)
#            1234 LOAD_FAST                1 (result)
#            1236 CALL                     1
#            1244 JUMP_FORWARD             1 (to 1248)
#         >> 1246 LOAD_CONST               7 ('result')
#         >> 1248 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1258 LOAD_ATTR               16 (_saferepr)
#            1278 LOAD_FAST                2 (@py_assert1)
#            1280 CALL                     1
#            1288 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1298 LOAD_ATTR               16 (_saferepr)
#            1318 LOAD_FAST                3 (@py_assert4)
#            1320 CALL                     1
#            1328 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#            1330 BUILD_CONST_KEY_MAP      3
#            1332 BINARY_OP                6 (%)
#            1336 STORE_FAST               5 (@py_format6)
#            1338 LOAD_CONST               9 ('assert %(py7)s')
#            1340 LOAD_CONST              10 ('py7')
#            1342 LOAD_FAST                5 (@py_format6)
#            1344 BUILD_MAP                1
#            1346 BINARY_OP                6 (%)
#            1350 STORE_FAST               6 (@py_format8)
#            1352 LOAD_GLOBAL             19 (NULL + AssertionError)
#            1362 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1372 LOAD_ATTR               20 (_format_explanation)
#            1392 LOAD_FAST                6 (@py_format8)
#            1394 CALL                     1
#            1402 CALL                     1
#            1410 RAISE_VARARGS            1
#         >> 1412 LOAD_CONST               0 (None)
#            1414 COPY                     1
#            1416 STORE_FAST               2 (@py_assert1)
#            1418 COPY                     1
#            1420 STORE_FAST               4 (@py_assert3)
#            1422 STORE_FAST               3 (@py_assert4)
# 
#  17        1424 LOAD_FAST                1 (result)
#            1426 LOAD_ATTR               30 (data)
#            1446 STORE_FAST               2 (@py_assert1)
#            1448 LOAD_CONST               2 ('value')
#            1450 LOAD_CONST               3 (42)
#            1452 BUILD_MAP                1
#            1454 STORE_FAST               3 (@py_assert4)
#            1456 LOAD_FAST                2 (@py_assert1)
#            1458 LOAD_FAST                3 (@py_assert4)
#            1460 COMPARE_OP              40 (==)
#            1464 STORE_FAST               4 (@py_assert3)
#            1466 LOAD_FAST                4 (@py_assert3)
#            1468 POP_JUMP_IF_TRUE       173 (to 1816)
#            1470 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1480 LOAD_ATTR                8 (_call_reprcompare)
#            1500 LOAD_CONST               5 (('==',))
#            1502 LOAD_FAST                4 (@py_assert3)
#            1504 BUILD_TUPLE              1
#            1506 LOAD_CONST              19 (('%(py2)s\n{%(py2)s = %(py0)s.data\n} == %(py5)s',))
#            1508 LOAD_FAST                2 (@py_assert1)
#            1510 LOAD_FAST                3 (@py_assert4)
#            1512 BUILD_TUPLE              2
#            1514 CALL                     4
#            1522 LOAD_CONST               7 ('result')
#            1524 LOAD_GLOBAL             11 (NULL + @py_builtins)
#            1534 LOAD_ATTR               12 (locals)
#            1554 CALL                     0
#            1562 CONTAINS_OP              0
#            1564 POP_JUMP_IF_TRUE        21 (to 1608)
#            1566 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1576 LOAD_ATTR               14 (_should_repr_global_name)
#            1596 LOAD_FAST                1 (result)
#            1598 CALL                     1
#            1606 POP_JUMP_IF_FALSE       21 (to 1650)
#         >> 1608 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1618 LOAD_ATTR               16 (_saferepr)
#            1638 LOAD_FAST                1 (result)
#            1640 CALL                     1
#            1648 JUMP_FORWARD             1 (to 1652)
#         >> 1650 LOAD_CONST               7 ('result')
#         >> 1652 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1662 LOAD_ATTR               16 (_saferepr)
#            1682 LOAD_FAST                2 (@py_assert1)
#            1684 CALL                     1
#            1692 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1702 LOAD_ATTR               16 (_saferepr)
#            1722 LOAD_FAST                3 (@py_assert4)
#            1724 CALL                     1
#            1732 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#            1734 BUILD_CONST_KEY_MAP      3
#            1736 BINARY_OP                6 (%)
#            1740 STORE_FAST               5 (@py_format6)
#            1742 LOAD_CONST               9 ('assert %(py7)s')
#            1744 LOAD_CONST              10 ('py7')
#            1746 LOAD_FAST                5 (@py_format6)
#            1748 BUILD_MAP                1
#            1750 BINARY_OP                6 (%)
#            1754 STORE_FAST               6 (@py_format8)
#            1756 LOAD_GLOBAL             19 (NULL + AssertionError)
#            1766 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1776 LOAD_ATTR               20 (_format_explanation)
#            1796 LOAD_FAST                6 (@py_format8)
#            1798 CALL                     1
#            1806 CALL                     1
#            1814 RAISE_VARARGS            1
#         >> 1816 LOAD_CONST               0 (None)
#            1818 COPY                     1
#            1820 STORE_FAST               2 (@py_assert1)
#            1822 COPY                     1
#            1824 STORE_FAST               4 (@py_assert3)
#            1826 STORE_FAST               3 (@py_assert4)
#            1828 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_create_failure_result at 0x3afab1c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 19>:
#  19           0 RESUME                   0
# 
#  20           2 LOAD_GLOBAL              1 (NULL + SkillResult)
#              12 LOAD_ATTR                2 (failure)
# 
#  21          32 LOAD_CONST               1 ('test_skill')
# 
#  22          34 LOAD_CONST               2 ('Something went wrong')
# 
#  23          36 LOAD_CONST               3 ('validation')
# 
#  20          38 KW_NAMES                 4 (('skill_name', 'error', 'stage'))
#              40 CALL                     3
#              48 STORE_FAST               1 (result)
# 
#  25          50 LOAD_FAST                1 (result)
#              52 LOAD_ATTR                4 (skill_name)
#              72 STORE_FAST               2 (@py_assert1)
#              74 LOAD_CONST               1 ('test_skill')
#              76 STORE_FAST               3 (@py_assert4)
#              78 LOAD_FAST                2 (@py_assert1)
#              80 LOAD_FAST                3 (@py_assert4)
#              82 COMPARE_OP              40 (==)
#              86 STORE_FAST               4 (@py_assert3)
#              88 LOAD_FAST                4 (@py_assert3)
#              90 POP_JUMP_IF_TRUE       173 (to 438)
#              92 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             102 LOAD_ATTR                8 (_call_reprcompare)
#             122 LOAD_CONST               5 (('==',))
#             124 LOAD_FAST                4 (@py_assert3)
#             126 BUILD_TUPLE              1
#             128 LOAD_CONST               6 (('%(py2)s\n{%(py2)s = %(py0)s.skill_name\n} == %(py5)s',))
#             130 LOAD_FAST                2 (@py_assert1)
#             132 LOAD_FAST                3 (@py_assert4)
#             134 BUILD_TUPLE              2
#             136 CALL                     4
#             144 LOAD_CONST               7 ('result')
#             146 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             156 LOAD_ATTR               12 (locals)
#             176 CALL                     0
#             184 CONTAINS_OP              0
#             186 POP_JUMP_IF_TRUE        21 (to 230)
#             188 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             198 LOAD_ATTR               14 (_should_repr_global_name)
#             218 LOAD_FAST                1 (result)
#             220 CALL                     1
#             228 POP_JUMP_IF_FALSE       21 (to 272)
#         >>  230 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             240 LOAD_ATTR               16 (_saferepr)
#             260 LOAD_FAST                1 (result)
#             262 CALL                     1
#             270 JUMP_FORWARD             1 (to 274)
#         >>  272 LOAD_CONST               7 ('result')
#         >>  274 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             284 LOAD_ATTR               16 (_saferepr)
#             304 LOAD_FAST                2 (@py_assert1)
#             306 CALL                     1
#             314 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             324 LOAD_ATTR               16 (_saferepr)
#             344 LOAD_FAST                3 (@py_assert4)
#             346 CALL                     1
#             354 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#             356 BUILD_CONST_KEY_MAP      3
#             358 BINARY_OP                6 (%)
#             362 STORE_FAST               5 (@py_format6)
#             364 LOAD_CONST               9 ('assert %(py7)s')
#             366 LOAD_CONST              10 ('py7')
#             368 LOAD_FAST                5 (@py_format6)
#             370 BUILD_MAP                1
#             372 BINARY_OP                6 (%)
#             376 STORE_FAST               6 (@py_format8)
#             378 LOAD_GLOBAL             19 (NULL + AssertionError)
#             388 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             398 LOAD_ATTR               20 (_format_explanation)
#             418 LOAD_FAST                6 (@py_format8)
#             420 CALL                     1
#             428 CALL                     1
#             436 RAISE_VARARGS            1
#         >>  438 LOAD_CONST               0 (None)
#             440 COPY                     1
#             442 STORE_FAST               2 (@py_assert1)
#             444 COPY                     1
#             446 STORE_FAST               4 (@py_assert3)
#             448 STORE_FAST               3 (@py_assert4)
# 
#  26         450 LOAD_FAST                1 (result)
#             452 LOAD_ATTR               22 (status)
#             472 STORE_FAST               2 (@py_assert1)
#             474 LOAD_GLOBAL             24 (SkillStatus)
#             484 LOAD_ATTR               26 (FAILED)
#             504 STORE_FAST               7 (@py_assert5)
#             506 LOAD_FAST                2 (@py_assert1)
#             508 LOAD_FAST                7 (@py_assert5)
#             510 COMPARE_OP              40 (==)
#             514 STORE_FAST               4 (@py_assert3)
#             516 LOAD_FAST                4 (@py_assert3)
#             518 POP_JUMP_IF_TRUE       246 (to 1012)
#             520 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             530 LOAD_ATTR                8 (_call_reprcompare)
#             550 LOAD_CONST               5 (('==',))
#             552 LOAD_FAST                4 (@py_assert3)
#             554 BUILD_TUPLE              1
#             556 LOAD_CONST              11 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.FAILED\n}',))
#             558 LOAD_FAST                2 (@py_assert1)
#             560 LOAD_FAST                7 (@py_assert5)
#             562 BUILD_TUPLE              2
#             564 CALL                     4
#             572 LOAD_CONST               7 ('result')
#             574 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             584 LOAD_ATTR               12 (locals)
#             604 CALL                     0
#             612 CONTAINS_OP              0
#             614 POP_JUMP_IF_TRUE        21 (to 658)
#             616 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             626 LOAD_ATTR               14 (_should_repr_global_name)
#             646 LOAD_FAST                1 (result)
#             648 CALL                     1
#             656 POP_JUMP_IF_FALSE       21 (to 700)
#         >>  658 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             668 LOAD_ATTR               16 (_saferepr)
#             688 LOAD_FAST                1 (result)
#             690 CALL                     1
#             698 JUMP_FORWARD             1 (to 702)
#         >>  700 LOAD_CONST               7 ('result')
#         >>  702 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             712 LOAD_ATTR               16 (_saferepr)
#             732 LOAD_FAST                2 (@py_assert1)
#             734 CALL                     1
#             742 LOAD_CONST              12 ('SkillStatus')
#             744 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             754 LOAD_ATTR               12 (locals)
#             774 CALL                     0
#             782 CONTAINS_OP              0
#             784 POP_JUMP_IF_TRUE        25 (to 836)
#             786 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             796 LOAD_ATTR               14 (_should_repr_global_name)
#             816 LOAD_GLOBAL             24 (SkillStatus)
#             826 CALL                     1
#             834 POP_JUMP_IF_FALSE       25 (to 886)
#         >>  836 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             846 LOAD_ATTR               16 (_saferepr)
#             866 LOAD_GLOBAL             24 (SkillStatus)
#             876 CALL                     1
#             884 JUMP_FORWARD             1 (to 888)
#         >>  886 LOAD_CONST              12 ('SkillStatus')
#         >>  888 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             898 LOAD_ATTR               16 (_saferepr)
#             918 LOAD_FAST                7 (@py_assert5)
#             920 CALL                     1
#             928 LOAD_CONST              13 (('py0', 'py2', 'py4', 'py6'))
#             930 BUILD_CONST_KEY_MAP      4
#             932 BINARY_OP                6 (%)
#             936 STORE_FAST               8 (@py_format7)
#             938 LOAD_CONST              14 ('assert %(py8)s')
#             940 LOAD_CONST              15 ('py8')
#             942 LOAD_FAST                8 (@py_format7)
#             944 BUILD_MAP                1
#             946 BINARY_OP                6 (%)
#             950 STORE_FAST               9 (@py_format9)
#             952 LOAD_GLOBAL             19 (NULL + AssertionError)
#             962 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             972 LOAD_ATTR               20 (_format_explanation)
#             992 LOAD_FAST                9 (@py_format9)
#             994 CALL                     1
#            1002 CALL                     1
#            1010 RAISE_VARARGS            1
#         >> 1012 LOAD_CONST               0 (None)
#            1014 COPY                     1
#            1016 STORE_FAST               2 (@py_assert1)
#            1018 COPY                     1
#            1020 STORE_FAST               4 (@py_assert3)
#            1022 STORE_FAST               7 (@py_assert5)
# 
#  27        1024 LOAD_FAST                1 (result)
#            1026 LOAD_ATTR               28 (is_success)
#            1046 STORE_FAST               2 (@py_assert1)
#            1048 LOAD_CONST              16 (False)
#            1050 STORE_FAST               3 (@py_assert4)
#            1052 LOAD_FAST                2 (@py_assert1)
#            1054 LOAD_FAST                3 (@py_assert4)
#            1056 IS_OP                    0
#            1058 STORE_FAST               4 (@py_assert3)
#            1060 LOAD_FAST                4 (@py_assert3)
#            1062 POP_JUMP_IF_TRUE       173 (to 1410)
#            1064 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1074 LOAD_ATTR                8 (_call_reprcompare)
#            1094 LOAD_CONST              17 (('is',))
#            1096 LOAD_FAST                4 (@py_assert3)
#            1098 BUILD_TUPLE              1
#            1100 LOAD_CONST              18 (('%(py2)s\n{%(py2)s = %(py0)s.is_success\n} is %(py5)s',))
#            1102 LOAD_FAST                2 (@py_assert1)
#            1104 LOAD_FAST                3 (@py_assert4)
#            1106 BUILD_TUPLE              2
#            1108 CALL                     4
#            1116 LOAD_CONST               7 ('result')
#            1118 LOAD_GLOBAL             11 (NULL + @py_builtins)
#            1128 LOAD_ATTR               12 (locals)
#            1148 CALL                     0
#            1156 CONTAINS_OP              0
#            1158 POP_JUMP_IF_TRUE        21 (to 1202)
#            1160 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1170 LOAD_ATTR               14 (_should_repr_global_name)
#            1190 LOAD_FAST                1 (result)
#            1192 CALL                     1
#            1200 POP_JUMP_IF_FALSE       21 (to 1244)
#         >> 1202 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1212 LOAD_ATTR               16 (_saferepr)
#            1232 LOAD_FAST                1 (result)
#            1234 CALL                     1
#            1242 JUMP_FORWARD             1 (to 1246)
#         >> 1244 LOAD_CONST               7 ('result')
#         >> 1246 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1256 LOAD_ATTR               16 (_saferepr)
#            1276 LOAD_FAST                2 (@py_assert1)
#            1278 CALL                     1
#            1286 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1296 LOAD_ATTR               16 (_saferepr)
#            1316 LOAD_FAST                3 (@py_assert4)
#            1318 CALL                     1
#            1326 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#            1328 BUILD_CONST_KEY_MAP      3
#            1330 BINARY_OP                6 (%)
#            1334 STORE_FAST               5 (@py_format6)
#            1336 LOAD_CONST               9 ('assert %(py7)s')
#            1338 LOAD_CONST              10 ('py7')
#            1340 LOAD_FAST                5 (@py_format6)
#            1342 BUILD_MAP                1
#            1344 BINARY_OP                6 (%)
#            1348 STORE_FAST               6 (@py_format8)
#            1350 LOAD_GLOBAL             19 (NULL + AssertionError)
#            1360 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1370 LOAD_ATTR               20 (_format_explanation)
#            1390 LOAD_FAST                6 (@py_format8)
#            1392 CALL                     1
#            1400 CALL                     1
#            1408 RAISE_VARARGS            1
#         >> 1410 LOAD_CONST               0 (None)
#            1412 COPY                     1
#            1414 STORE_FAST               2 (@py_assert1)
#            1416 COPY                     1
#            1418 STORE_FAST               4 (@py_assert3)
#            1420 STORE_FAST               3 (@py_assert4)
# 
#  28        1422 LOAD_FAST                1 (result)
#            1424 LOAD_ATTR               30 (error)
#            1444 STORE_FAST               2 (@py_assert1)
#            1446 LOAD_CONST               2 ('Something went wrong')
#            1448 STORE_FAST               3 (@py_assert4)
#            1450 LOAD_FAST                2 (@py_assert1)
#            1452 LOAD_FAST                3 (@py_assert4)
#            1454 COMPARE_OP              40 (==)
#            1458 STORE_FAST               4 (@py_assert3)
#            1460 LOAD_FAST                4 (@py_assert3)
#            1462 POP_JUMP_IF_TRUE       173 (to 1810)
#            1464 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1474 LOAD_ATTR                8 (_call_reprcompare)
#            1494 LOAD_CONST               5 (('==',))
#            1496 LOAD_FAST                4 (@py_assert3)
#            1498 BUILD_TUPLE              1
#            1500 LOAD_CONST              19 (('%(py2)s\n{%(py2)s = %(py0)s.error\n} == %(py5)s',))
#            1502 LOAD_FAST                2 (@py_assert1)
#            1504 LOAD_FAST                3 (@py_assert4)
#            1506 BUILD_TUPLE              2
#            1508 CALL                     4
#            1516 LOAD_CONST               7 ('result')
#            1518 LOAD_GLOBAL             11 (NULL + @py_builtins)
#            1528 LOAD_ATTR               12 (locals)
#            1548 CALL                     0
#            1556 CONTAINS_OP              0
#            1558 POP_JUMP_IF_TRUE        21 (to 1602)
#            1560 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1570 LOAD_ATTR               14 (_should_repr_global_name)
#            1590 LOAD_FAST                1 (result)
#            1592 CALL                     1
#            1600 POP_JUMP_IF_FALSE       21 (to 1644)
#         >> 1602 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1612 LOAD_ATTR               16 (_saferepr)
#            1632 LOAD_FAST                1 (result)
#            1634 CALL                     1
#            1642 JUMP_FORWARD             1 (to 1646)
#         >> 1644 LOAD_CONST               7 ('result')
#         >> 1646 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1656 LOAD_ATTR               16 (_saferepr)
#            1676 LOAD_FAST                2 (@py_assert1)
#            1678 CALL                     1
#            1686 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1696 LOAD_ATTR               16 (_saferepr)
#            1716 LOAD_FAST                3 (@py_assert4)
#            1718 CALL                     1
#            1726 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#            1728 BUILD_CONST_KEY_MAP      3
#            1730 BINARY_OP                6 (%)
#            1734 STORE_FAST               5 (@py_format6)
#            1736 LOAD_CONST               9 ('assert %(py7)s')
#            1738 LOAD_CONST              10 ('py7')
#            1740 LOAD_FAST                5 (@py_format6)
#            1742 BUILD_MAP                1
#            1744 BINARY_OP                6 (%)
#            1748 STORE_FAST               6 (@py_format8)
#            1750 LOAD_GLOBAL             19 (NULL + AssertionError)
#            1760 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1770 LOAD_ATTR               20 (_format_explanation)
#            1790 LOAD_FAST                6 (@py_format8)
#            1792 CALL                     1
#            1800 CALL                     1
#            1808 RAISE_VARARGS            1
#         >> 1810 LOAD_CONST               0 (None)
#            1812 COPY                     1
#            1814 STORE_FAST               2 (@py_assert1)
#            1816 COPY                     1
#            1818 STORE_FAST               4 (@py_assert3)
#            1820 STORE_FAST               3 (@py_assert4)
# 
#  29        1822 LOAD_FAST                1 (result)
#            1824 LOAD_ATTR               32 (data)
#            1844 LOAD_CONST              20 ('stage')
#            1846 BINARY_SUBSCR
#            1850 STORE_FAST              10 (@py_assert0)
#            1852 LOAD_CONST               3 ('validation')
#            1854 STORE_FAST               4 (@py_assert3)
#            1856 LOAD_FAST               10 (@py_assert0)
#            1858 LOAD_FAST                4 (@py_assert3)
#            1860 COMPARE_OP              40 (==)
#            1864 STORE_FAST              11 (@py_assert2)
#            1866 LOAD_FAST               11 (@py_assert2)
#            1868 POP_JUMP_IF_TRUE       108 (to 2086)
#            1870 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1880 LOAD_ATTR                8 (_call_reprcompare)
#            1900 LOAD_CONST               5 (('==',))
#            1902 LOAD_FAST               11 (@py_assert2)
#            1904 BUILD_TUPLE              1
#            1906 LOAD_CONST              21 (('%(py1)s == %(py4)s',))
#            1908 LOAD_FAST               10 (@py_assert0)
#            1910 LOAD_FAST                4 (@py_assert3)
#            1912 BUILD_TUPLE              2
#            1914 CALL                     4
#            1922 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1932 LOAD_ATTR               16 (_saferepr)
#            1952 LOAD_FAST               10 (@py_assert0)
#            1954 CALL                     1
#            1962 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1972 LOAD_ATTR               16 (_saferepr)
#            1992 LOAD_FAST                4 (@py_assert3)
#            1994 CALL                     1
#            2002 LOAD_CONST              22 (('py1', 'py4'))
#            2004 BUILD_CONST_KEY_MAP      2
#            2006 BINARY_OP                6 (%)
#            2010 STORE_FAST              12 (@py_format5)
#            2012 LOAD_CONST              23 ('assert %(py6)s')
#            2014 LOAD_CONST              24 ('py6')
#            2016 LOAD_FAST               12 (@py_format5)
#            2018 BUILD_MAP                1
#            2020 BINARY_OP                6 (%)
#            2024 STORE_FAST               8 (@py_format7)
#            2026 LOAD_GLOBAL             19 (NULL + AssertionError)
#            2036 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            2046 LOAD_ATTR               20 (_format_explanation)
#            2066 LOAD_FAST                8 (@py_format7)
#            2068 CALL                     1
#            2076 CALL                     1
#            2084 RAISE_VARARGS            1
#         >> 2086 LOAD_CONST               0 (None)
#            2088 COPY                     1
#            2090 STORE_FAST              10 (@py_assert0)
#            2092 COPY                     1
#            2094 STORE_FAST              11 (@py_assert2)
#            2096 STORE_FAST               4 (@py_assert3)
#            2098 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_create_running_result at 0x3afa6250, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 31>:
#  31           0 RESUME                   0
# 
#  32           2 LOAD_GLOBAL              1 (NULL + SkillResult)
#              12 LOAD_ATTR                2 (running)
#              32 LOAD_CONST               1 ('test_skill')
#              34 LOAD_CONST               2 ('progress')
#              36 LOAD_CONST               3 (50)
#              38 BUILD_MAP                1
#              40 KW_NAMES                 4 (('skill_name', 'data'))
#              42 CALL                     2
#              50 STORE_FAST               1 (result)
# 
#  33          52 LOAD_FAST                1 (result)
#              54 LOAD_ATTR                4 (skill_name)
#              74 STORE_FAST               2 (@py_assert1)
#              76 LOAD_CONST               1 ('test_skill')
#              78 STORE_FAST               3 (@py_assert4)
#              80 LOAD_FAST                2 (@py_assert1)
#              82 LOAD_FAST                3 (@py_assert4)
#              84 COMPARE_OP              40 (==)
#              88 STORE_FAST               4 (@py_assert3)
#              90 LOAD_FAST                4 (@py_assert3)
#              92 POP_JUMP_IF_TRUE       173 (to 440)
#              94 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             104 LOAD_ATTR                8 (_call_reprcompare)
#             124 LOAD_CONST               5 (('==',))
#             126 LOAD_FAST                4 (@py_assert3)
#             128 BUILD_TUPLE              1
#             130 LOAD_CONST               6 (('%(py2)s\n{%(py2)s = %(py0)s.skill_name\n} == %(py5)s',))
#             132 LOAD_FAST                2 (@py_assert1)
#             134 LOAD_FAST                3 (@py_assert4)
#             136 BUILD_TUPLE              2
#             138 CALL                     4
#             146 LOAD_CONST               7 ('result')
#             148 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             158 LOAD_ATTR               12 (locals)
#             178 CALL                     0
#             186 CONTAINS_OP              0
#             188 POP_JUMP_IF_TRUE        21 (to 232)
#             190 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             200 LOAD_ATTR               14 (_should_repr_global_name)
#             220 LOAD_FAST                1 (result)
#             222 CALL                     1
#             230 POP_JUMP_IF_FALSE       21 (to 274)
#         >>  232 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             242 LOAD_ATTR               16 (_saferepr)
#             262 LOAD_FAST                1 (result)
#             264 CALL                     1
#             272 JUMP_FORWARD             1 (to 276)
#         >>  274 LOAD_CONST               7 ('result')
#         >>  276 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             286 LOAD_ATTR               16 (_saferepr)
#             306 LOAD_FAST                2 (@py_assert1)
#             308 CALL                     1
#             316 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             326 LOAD_ATTR               16 (_saferepr)
#             346 LOAD_FAST                3 (@py_assert4)
#             348 CALL                     1
#             356 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#             358 BUILD_CONST_KEY_MAP      3
#             360 BINARY_OP                6 (%)
#             364 STORE_FAST               5 (@py_format6)
#             366 LOAD_CONST               9 ('assert %(py7)s')
#             368 LOAD_CONST              10 ('py7')
#             370 LOAD_FAST                5 (@py_format6)
#             372 BUILD_MAP                1
#             374 BINARY_OP                6 (%)
#             378 STORE_FAST               6 (@py_format8)
#             380 LOAD_GLOBAL             19 (NULL + AssertionError)
#             390 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             400 LOAD_ATTR               20 (_format_explanation)
#             420 LOAD_FAST                6 (@py_format8)
#             422 CALL                     1
#             430 CALL                     1
#             438 RAISE_VARARGS            1
#         >>  440 LOAD_CONST               0 (None)
#             442 COPY                     1
#             444 STORE_FAST               2 (@py_assert1)
#             446 COPY                     1
#             448 STORE_FAST               4 (@py_assert3)
#             450 STORE_FAST               3 (@py_assert4)
# 
#  34         452 LOAD_FAST                1 (result)
#             454 LOAD_ATTR               22 (status)
#             474 STORE_FAST               2 (@py_assert1)
#             476 LOAD_GLOBAL             24 (SkillStatus)
#             486 LOAD_ATTR               26 (RUNNING)
#             506 STORE_FAST               7 (@py_assert5)
#             508 LOAD_FAST                2 (@py_assert1)
#             510 LOAD_FAST                7 (@py_assert5)
#             512 COMPARE_OP              40 (==)
#             516 STORE_FAST               4 (@py_assert3)
#             518 LOAD_FAST                4 (@py_assert3)
#             520 POP_JUMP_IF_TRUE       246 (to 1014)
#             522 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             532 LOAD_ATTR                8 (_call_reprcompare)
#             552 LOAD_CONST               5 (('==',))
#             554 LOAD_FAST                4 (@py_assert3)
#             556 BUILD_TUPLE              1
#             558 LOAD_CONST              11 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.RUNNING\n}',))
#             560 LOAD_FAST                2 (@py_assert1)
#             562 LOAD_FAST                7 (@py_assert5)
#             564 BUILD_TUPLE              2
#             566 CALL                     4
#             574 LOAD_CONST               7 ('result')
#             576 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             586 LOAD_ATTR               12 (locals)
#             606 CALL                     0
#             614 CONTAINS_OP              0
#             616 POP_JUMP_IF_TRUE        21 (to 660)
#             618 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             628 LOAD_ATTR               14 (_should_repr_global_name)
#             648 LOAD_FAST                1 (result)
#             650 CALL                     1
#             658 POP_JUMP_IF_FALSE       21 (to 702)
#         >>  660 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             670 LOAD_ATTR               16 (_saferepr)
#             690 LOAD_FAST                1 (result)
#             692 CALL                     1
#             700 JUMP_FORWARD             1 (to 704)
#         >>  702 LOAD_CONST               7 ('result')
#         >>  704 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             714 LOAD_ATTR               16 (_saferepr)
#             734 LOAD_FAST                2 (@py_assert1)
#             736 CALL                     1
#             744 LOAD_CONST              12 ('SkillStatus')
#             746 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             756 LOAD_ATTR               12 (locals)
#             776 CALL                     0
#             784 CONTAINS_OP              0
#             786 POP_JUMP_IF_TRUE        25 (to 838)
#             788 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             798 LOAD_ATTR               14 (_should_repr_global_name)
#             818 LOAD_GLOBAL             24 (SkillStatus)
#             828 CALL                     1
#             836 POP_JUMP_IF_FALSE       25 (to 888)
#         >>  838 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             848 LOAD_ATTR               16 (_saferepr)
#             868 LOAD_GLOBAL             24 (SkillStatus)
#             878 CALL                     1
#             886 JUMP_FORWARD             1 (to 890)
#         >>  888 LOAD_CONST              12 ('SkillStatus')
#         >>  890 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             900 LOAD_ATTR               16 (_saferepr)
#             920 LOAD_FAST                7 (@py_assert5)
#             922 CALL                     1
#             930 LOAD_CONST              13 (('py0', 'py2', 'py4', 'py6'))
#             932 BUILD_CONST_KEY_MAP      4
#             934 BINARY_OP                6 (%)
#             938 STORE_FAST               8 (@py_format7)
#             940 LOAD_CONST              14 ('assert %(py8)s')
#             942 LOAD_CONST              15 ('py8')
#             944 LOAD_FAST                8 (@py_format7)
#             946 BUILD_MAP                1
#             948 BINARY_OP                6 (%)
#             952 STORE_FAST               9 (@py_format9)
#             954 LOAD_GLOBAL             19 (NULL + AssertionError)
#             964 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             974 LOAD_ATTR               20 (_format_explanation)
#             994 LOAD_FAST                9 (@py_format9)
#             996 CALL                     1
#            1004 CALL                     1
#            1012 RAISE_VARARGS            1
#         >> 1014 LOAD_CONST               0 (None)
#            1016 COPY                     1
#            1018 STORE_FAST               2 (@py_assert1)
#            1020 COPY                     1
#            1022 STORE_FAST               4 (@py_assert3)
#            1024 STORE_FAST               7 (@py_assert5)
# 
#  35        1026 LOAD_FAST                1 (result)
#            1028 LOAD_ATTR               28 (data)
#            1048 LOAD_CONST               2 ('progress')
#            1050 BINARY_SUBSCR
#            1054 STORE_FAST              10 (@py_assert0)
#            1056 LOAD_CONST               3 (50)
#            1058 STORE_FAST               4 (@py_assert3)
#            1060 LOAD_FAST               10 (@py_assert0)
#            1062 LOAD_FAST                4 (@py_assert3)
#            1064 COMPARE_OP              40 (==)
#            1068 STORE_FAST              11 (@py_assert2)
#            1070 LOAD_FAST               11 (@py_assert2)
#            1072 POP_JUMP_IF_TRUE       108 (to 1290)
#            1074 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1084 LOAD_ATTR                8 (_call_reprcompare)
#            1104 LOAD_CONST               5 (('==',))
#            1106 LOAD_FAST               11 (@py_assert2)
#            1108 BUILD_TUPLE              1
#            1110 LOAD_CONST              16 (('%(py1)s == %(py4)s',))
#            1112 LOAD_FAST               10 (@py_assert0)
#            1114 LOAD_FAST                4 (@py_assert3)
#            1116 BUILD_TUPLE              2
#            1118 CALL                     4
#            1126 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1136 LOAD_ATTR               16 (_saferepr)
#            1156 LOAD_FAST               10 (@py_assert0)
#            1158 CALL                     1
#            1166 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1176 LOAD_ATTR               16 (_saferepr)
#            1196 LOAD_FAST                4 (@py_assert3)
#            1198 CALL                     1
#            1206 LOAD_CONST              17 (('py1', 'py4'))
#            1208 BUILD_CONST_KEY_MAP      2
#            1210 BINARY_OP                6 (%)
#            1214 STORE_FAST              12 (@py_format5)
#            1216 LOAD_CONST              18 ('assert %(py6)s')
#            1218 LOAD_CONST              19 ('py6')
#            1220 LOAD_FAST               12 (@py_format5)
#            1222 BUILD_MAP                1
#            1224 BINARY_OP                6 (%)
#            1228 STORE_FAST               8 (@py_format7)
#            1230 LOAD_GLOBAL             19 (NULL + AssertionError)
#            1240 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1250 LOAD_ATTR               20 (_format_explanation)
#            1270 LOAD_FAST                8 (@py_format7)
#            1272 CALL                     1
#            1280 CALL                     1
#            1288 RAISE_VARARGS            1
#         >> 1290 LOAD_CONST               0 (None)
#            1292 COPY                     1
#            1294 STORE_FAST              10 (@py_assert0)
#            1296 COPY                     1
#            1298 STORE_FAST              11 (@py_assert2)
#            1300 STORE_FAST               4 (@py_assert3)
#            1302 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_add_log at 0x3aed0fc0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 37>:
#  37           0 RESUME                   0
# 
#  38           2 LOAD_GLOBAL              1 (NULL + SkillResult)
#              12 LOAD_ATTR                2 (success)
#              32 LOAD_CONST               1 ('test')
#              34 BUILD_MAP                0
#              36 KW_NAMES                 2 (('skill_name', 'data'))
#              38 CALL                     2
#              46 STORE_FAST               1 (result)
# 
#  39          48 LOAD_FAST                1 (result)
#              50 LOAD_ATTR                5 (NULL|self + add_log)
#              70 LOAD_CONST               3 ('INFO')
#              72 LOAD_CONST               4 ('Test message')
#              74 CALL                     2
#              82 POP_TOP
# 
#  40          84 LOAD_FAST                1 (result)
#              86 LOAD_ATTR                6 (logs)
#             106 STORE_FAST               2 (@py_assert2)
#             108 LOAD_GLOBAL              9 (NULL + len)
#             118 LOAD_FAST                2 (@py_assert2)
#             120 CALL                     1
#             128 STORE_FAST               3 (@py_assert4)
#             130 LOAD_CONST               5 (1)
#             132 STORE_FAST               4 (@py_assert7)
#             134 LOAD_FAST                3 (@py_assert4)
#             136 LOAD_FAST                4 (@py_assert7)
#             138 COMPARE_OP              40 (==)
#             142 STORE_FAST               5 (@py_assert6)
#             144 LOAD_FAST                5 (@py_assert6)
#             146 EXTENDED_ARG             1
#             148 POP_JUMP_IF_TRUE       266 (to 682)
#             150 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             160 LOAD_ATTR               12 (_call_reprcompare)
#             180 LOAD_CONST               6 (('==',))
#             182 LOAD_FAST                5 (@py_assert6)
#             184 BUILD_TUPLE              1
#             186 LOAD_CONST               7 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.logs\n})\n} == %(py8)s',))
#             188 LOAD_FAST                3 (@py_assert4)
#             190 LOAD_FAST                4 (@py_assert7)
#             192 BUILD_TUPLE              2
#             194 CALL                     4
#             202 LOAD_CONST               8 ('len')
#             204 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             214 LOAD_ATTR               16 (locals)
#             234 CALL                     0
#             242 CONTAINS_OP              0
#             244 POP_JUMP_IF_TRUE        25 (to 296)
#             246 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             256 LOAD_ATTR               18 (_should_repr_global_name)
#             276 LOAD_GLOBAL              8 (len)
#             286 CALL                     1
#             294 POP_JUMP_IF_FALSE       25 (to 346)
#         >>  296 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             306 LOAD_ATTR               20 (_saferepr)
#             326 LOAD_GLOBAL              8 (len)
#             336 CALL                     1
#             344 JUMP_FORWARD             1 (to 348)
#         >>  346 LOAD_CONST               8 ('len')
#         >>  348 LOAD_CONST               9 ('result')
#             350 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             360 LOAD_ATTR               16 (locals)
#             380 CALL                     0
#             388 CONTAINS_OP              0
#             390 POP_JUMP_IF_TRUE        21 (to 434)
#             392 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             402 LOAD_ATTR               18 (_should_repr_global_name)
#             422 LOAD_FAST                1 (result)
#             424 CALL                     1
#             432 POP_JUMP_IF_FALSE       21 (to 476)
#         >>  434 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             444 LOAD_ATTR               20 (_saferepr)
#             464 LOAD_FAST                1 (result)
#             466 CALL                     1
#             474 JUMP_FORWARD             1 (to 478)
#         >>  476 LOAD_CONST               9 ('result')
#         >>  478 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             488 LOAD_ATTR               20 (_saferepr)
#             508 LOAD_FAST                2 (@py_assert2)
#             510 CALL                     1
#             518 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             528 LOAD_ATTR               20 (_saferepr)
#             548 LOAD_FAST                3 (@py_assert4)
#             550 CALL                     1
#             558 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             568 LOAD_ATTR               20 (_saferepr)
#             588 LOAD_FAST                4 (@py_assert7)
#             590 CALL                     1
#             598 LOAD_CONST              10 (('py0', 'py1', 'py3', 'py5', 'py8'))
#             600 BUILD_CONST_KEY_MAP      5
#             602 BINARY_OP                6 (%)
#             606 STORE_FAST               6 (@py_format9)
#             608 LOAD_CONST              11 ('assert %(py10)s')
#             610 LOAD_CONST              12 ('py10')
#             612 LOAD_FAST                6 (@py_format9)
#             614 BUILD_MAP                1
#             616 BINARY_OP                6 (%)
#             620 STORE_FAST               7 (@py_format11)
#             622 LOAD_GLOBAL             23 (NULL + AssertionError)
#             632 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             642 LOAD_ATTR               24 (_format_explanation)
#             662 LOAD_FAST                7 (@py_format11)
#             664 CALL                     1
#             672 CALL                     1
#             680 RAISE_VARARGS            1
#         >>  682 LOAD_CONST               0 (None)
#             684 COPY                     1
#             686 STORE_FAST               2 (@py_assert2)
#             688 COPY                     1
#             690 STORE_FAST               3 (@py_assert4)
#             692 COPY                     1
#             694 STORE_FAST               5 (@py_assert6)
#             696 STORE_FAST               4 (@py_assert7)
# 
#  41         698 LOAD_FAST                1 (result)
#             700 LOAD_ATTR                6 (logs)
#             720 LOAD_CONST              13 (0)
#             722 BINARY_SUBSCR
#             726 STORE_FAST               8 (@py_assert0)
#             728 LOAD_FAST                8 (@py_assert0)
#             730 LOAD_ATTR               26 (level)
#             750 STORE_FAST               2 (@py_assert2)
#             752 LOAD_CONST               3 ('INFO')
#             754 STORE_FAST               9 (@py_assert5)
#             756 LOAD_FAST                2 (@py_assert2)
#             758 LOAD_FAST                9 (@py_assert5)
#             760 COMPARE_OP              40 (==)
#             764 STORE_FAST               3 (@py_assert4)
#             766 LOAD_FAST                3 (@py_assert4)
#             768 POP_JUMP_IF_TRUE       128 (to 1026)
#             770 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             780 LOAD_ATTR               12 (_call_reprcompare)
#             800 LOAD_CONST               6 (('==',))
#             802 LOAD_FAST                3 (@py_assert4)
#             804 BUILD_TUPLE              1
#             806 LOAD_CONST              14 (('%(py3)s\n{%(py3)s = %(py1)s.level\n} == %(py6)s',))
#             808 LOAD_FAST                2 (@py_assert2)
#             810 LOAD_FAST                9 (@py_assert5)
#             812 BUILD_TUPLE              2
#             814 CALL                     4
#             822 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             832 LOAD_ATTR               20 (_saferepr)
#             852 LOAD_FAST                8 (@py_assert0)
#             854 CALL                     1
#             862 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             872 LOAD_ATTR               20 (_saferepr)
#             892 LOAD_FAST                2 (@py_assert2)
#             894 CALL                     1
#             902 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             912 LOAD_ATTR               20 (_saferepr)
#             932 LOAD_FAST                9 (@py_assert5)
#             934 CALL                     1
#             942 LOAD_CONST              15 (('py1', 'py3', 'py6'))
#             944 BUILD_CONST_KEY_MAP      3
#             946 BINARY_OP                6 (%)
#             950 STORE_FAST              10 (@py_format7)
#             952 LOAD_CONST              16 ('assert %(py8)s')
#             954 LOAD_CONST              17 ('py8')
#             956 LOAD_FAST               10 (@py_format7)
#             958 BUILD_MAP                1
#             960 BINARY_OP                6 (%)
#             964 STORE_FAST               6 (@py_format9)
#             966 LOAD_GLOBAL             23 (NULL + AssertionError)
#             976 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             986 LOAD_ATTR               24 (_format_explanation)
#            1006 LOAD_FAST                6 (@py_format9)
#            1008 CALL                     1
#            1016 CALL                     1
#            1024 RAISE_VARARGS            1
#         >> 1026 LOAD_CONST               0 (None)
#            1028 COPY                     1
#            1030 STORE_FAST               8 (@py_assert0)
#            1032 COPY                     1
#            1034 STORE_FAST               2 (@py_assert2)
#            1036 COPY                     1
#            1038 STORE_FAST               3 (@py_assert4)
#            1040 STORE_FAST               9 (@py_assert5)
# 
#  42        1042 LOAD_FAST                1 (result)
#            1044 LOAD_ATTR                6 (logs)
#            1064 LOAD_CONST              13 (0)
#            1066 BINARY_SUBSCR
#            1070 STORE_FAST               8 (@py_assert0)
#            1072 LOAD_FAST                8 (@py_assert0)
#            1074 LOAD_ATTR               28 (message)
#            1094 STORE_FAST               2 (@py_assert2)
#            1096 LOAD_CONST               4 ('Test message')
#            1098 STORE_FAST               9 (@py_assert5)
#            1100 LOAD_FAST                2 (@py_assert2)
#            1102 LOAD_FAST                9 (@py_assert5)
#            1104 COMPARE_OP              40 (==)
#            1108 STORE_FAST               3 (@py_assert4)
#            1110 LOAD_FAST                3 (@py_assert4)
#            1112 POP_JUMP_IF_TRUE       128 (to 1370)
#            1114 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1124 LOAD_ATTR               12 (_call_reprcompare)
#            1144 LOAD_CONST               6 (('==',))
#            1146 LOAD_FAST                3 (@py_assert4)
#            1148 BUILD_TUPLE              1
#            1150 LOAD_CONST              18 (('%(py3)s\n{%(py3)s = %(py1)s.message\n} == %(py6)s',))
#            1152 LOAD_FAST                2 (@py_assert2)
#            1154 LOAD_FAST                9 (@py_assert5)
#            1156 BUILD_TUPLE              2
#            1158 CALL                     4
#            1166 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1176 LOAD_ATTR               20 (_saferepr)
#            1196 LOAD_FAST                8 (@py_assert0)
#            1198 CALL                     1
#            1206 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1216 LOAD_ATTR               20 (_saferepr)
#            1236 LOAD_FAST                2 (@py_assert2)
#            1238 CALL                     1
#            1246 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1256 LOAD_ATTR               20 (_saferepr)
#            1276 LOAD_FAST                9 (@py_assert5)
#            1278 CALL                     1
#            1286 LOAD_CONST              15 (('py1', 'py3', 'py6'))
#            1288 BUILD_CONST_KEY_MAP      3
#            1290 BINARY_OP                6 (%)
#            1294 STORE_FAST              10 (@py_format7)
#            1296 LOAD_CONST              16 ('assert %(py8)s')
#            1298 LOAD_CONST              17 ('py8')
#            1300 LOAD_FAST               10 (@py_format7)
#            1302 BUILD_MAP                1
#            1304 BINARY_OP                6 (%)
#            1308 STORE_FAST               6 (@py_format9)
#            1310 LOAD_GLOBAL             23 (NULL + AssertionError)
#            1320 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1330 LOAD_ATTR               24 (_format_explanation)
#            1350 LOAD_FAST                6 (@py_format9)
#            1352 CALL                     1
#            1360 CALL                     1
#            1368 RAISE_VARARGS            1
#         >> 1370 LOAD_CONST               0 (None)
#            1372 COPY                     1
#            1374 STORE_FAST               8 (@py_assert0)
#            1376 COPY                     1
#            1378 STORE_FAST               2 (@py_assert2)
#            1380 COPY                     1
#            1382 STORE_FAST               3 (@py_assert4)
#            1384 STORE_FAST               9 (@py_assert5)
#            1386 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_add_artifact at 0x3aed1ba0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 44>:
#  44           0 RESUME                   0
# 
#  45           2 LOAD_GLOBAL              1 (NULL + SkillResult)
#              12 LOAD_ATTR                2 (success)
#              32 LOAD_CONST               1 ('test')
#              34 BUILD_MAP                0
#              36 KW_NAMES                 2 (('skill_name', 'data'))
#              38 CALL                     2
#              46 STORE_FAST               1 (result)
# 
#  46          48 LOAD_FAST                1 (result)
#              50 LOAD_ATTR                5 (NULL|self + add_artifact)
#              70 LOAD_CONST               3 ('output.json')
#              72 LOAD_CONST               4 ('/tmp/output.json')
#              74 LOAD_CONST               5 ('json')
#              76 KW_NAMES                 6 (('name', 'path', 'type_'))
#              78 CALL                     3
#              86 POP_TOP
# 
#  47          88 LOAD_FAST                1 (result)
#              90 LOAD_ATTR                6 (artifacts)
#             110 STORE_FAST               2 (@py_assert2)
#             112 LOAD_GLOBAL              9 (NULL + len)
#             122 LOAD_FAST                2 (@py_assert2)
#             124 CALL                     1
#             132 STORE_FAST               3 (@py_assert4)
#             134 LOAD_CONST               7 (1)
#             136 STORE_FAST               4 (@py_assert7)
#             138 LOAD_FAST                3 (@py_assert4)
#             140 LOAD_FAST                4 (@py_assert7)
#             142 COMPARE_OP              40 (==)
#             146 STORE_FAST               5 (@py_assert6)
#             148 LOAD_FAST                5 (@py_assert6)
#             150 EXTENDED_ARG             1
#             152 POP_JUMP_IF_TRUE       266 (to 686)
#             154 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             164 LOAD_ATTR               12 (_call_reprcompare)
#             184 LOAD_CONST               8 (('==',))
#             186 LOAD_FAST                5 (@py_assert6)
#             188 BUILD_TUPLE              1
#             190 LOAD_CONST               9 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.artifacts\n})\n} == %(py8)s',))
#             192 LOAD_FAST                3 (@py_assert4)
#             194 LOAD_FAST                4 (@py_assert7)
#             196 BUILD_TUPLE              2
#             198 CALL                     4
#             206 LOAD_CONST              10 ('len')
#             208 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             218 LOAD_ATTR               16 (locals)
#             238 CALL                     0
#             246 CONTAINS_OP              0
#             248 POP_JUMP_IF_TRUE        25 (to 300)
#             250 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             260 LOAD_ATTR               18 (_should_repr_global_name)
#             280 LOAD_GLOBAL              8 (len)
#             290 CALL                     1
#             298 POP_JUMP_IF_FALSE       25 (to 350)
#         >>  300 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             310 LOAD_ATTR               20 (_saferepr)
#             330 LOAD_GLOBAL              8 (len)
#             340 CALL                     1
#             348 JUMP_FORWARD             1 (to 352)
#         >>  350 LOAD_CONST              10 ('len')
#         >>  352 LOAD_CONST              11 ('result')
#             354 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             364 LOAD_ATTR               16 (locals)
#             384 CALL                     0
#             392 CONTAINS_OP              0
#             394 POP_JUMP_IF_TRUE        21 (to 438)
#             396 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             406 LOAD_ATTR               18 (_should_repr_global_name)
#             426 LOAD_FAST                1 (result)
#             428 CALL                     1
#             436 POP_JUMP_IF_FALSE       21 (to 480)
#         >>  438 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             448 LOAD_ATTR               20 (_saferepr)
#             468 LOAD_FAST                1 (result)
#             470 CALL                     1
#             478 JUMP_FORWARD             1 (to 482)
#         >>  480 LOAD_CONST              11 ('result')
#         >>  482 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             492 LOAD_ATTR               20 (_saferepr)
#             512 LOAD_FAST                2 (@py_assert2)
#             514 CALL                     1
#             522 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             532 LOAD_ATTR               20 (_saferepr)
#             552 LOAD_FAST                3 (@py_assert4)
#             554 CALL                     1
#             562 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             572 LOAD_ATTR               20 (_saferepr)
#             592 LOAD_FAST                4 (@py_assert7)
#             594 CALL                     1
#             602 LOAD_CONST              12 (('py0', 'py1', 'py3', 'py5', 'py8'))
#             604 BUILD_CONST_KEY_MAP      5
#             606 BINARY_OP                6 (%)
#             610 STORE_FAST               6 (@py_format9)
#             612 LOAD_CONST              13 ('assert %(py10)s')
#             614 LOAD_CONST              14 ('py10')
#             616 LOAD_FAST                6 (@py_format9)
#             618 BUILD_MAP                1
#             620 BINARY_OP                6 (%)
#             624 STORE_FAST               7 (@py_format11)
#             626 LOAD_GLOBAL             23 (NULL + AssertionError)
#             636 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             646 LOAD_ATTR               24 (_format_explanation)
#             666 LOAD_FAST                7 (@py_format11)
#             668 CALL                     1
#             676 CALL                     1
#             684 RAISE_VARARGS            1
#         >>  686 LOAD_CONST               0 (None)
#             688 COPY                     1
#             690 STORE_FAST               2 (@py_assert2)
#             692 COPY                     1
#             694 STORE_FAST               3 (@py_assert4)
#             696 COPY                     1
#             698 STORE_FAST               5 (@py_assert6)
#             700 STORE_FAST               4 (@py_assert7)
# 
#  48         702 LOAD_FAST                1 (result)
#             704 LOAD_ATTR                6 (artifacts)
#             724 LOAD_CONST              15 (0)
#             726 BINARY_SUBSCR
#             730 STORE_FAST               8 (@py_assert0)
#             732 LOAD_FAST                8 (@py_assert0)
#             734 LOAD_ATTR               26 (name)
#             754 STORE_FAST               2 (@py_assert2)
#             756 LOAD_CONST               3 ('output.json')
#             758 STORE_FAST               9 (@py_assert5)
#             760 LOAD_FAST                2 (@py_assert2)
#             762 LOAD_FAST                9 (@py_assert5)
#             764 COMPARE_OP              40 (==)
#             768 STORE_FAST               3 (@py_assert4)
#             770 LOAD_FAST                3 (@py_assert4)
#             772 POP_JUMP_IF_TRUE       128 (to 1030)
#             774 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             784 LOAD_ATTR               12 (_call_reprcompare)
#             804 LOAD_CONST               8 (('==',))
#             806 LOAD_FAST                3 (@py_assert4)
#             808 BUILD_TUPLE              1
#             810 LOAD_CONST              16 (('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s',))
#             812 LOAD_FAST                2 (@py_assert2)
#             814 LOAD_FAST                9 (@py_assert5)
#             816 BUILD_TUPLE              2
#             818 CALL                     4
#             826 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             836 LOAD_ATTR               20 (_saferepr)
#             856 LOAD_FAST                8 (@py_assert0)
#             858 CALL                     1
#             866 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             876 LOAD_ATTR               20 (_saferepr)
#             896 LOAD_FAST                2 (@py_assert2)
#             898 CALL                     1
#             906 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             916 LOAD_ATTR               20 (_saferepr)
#             936 LOAD_FAST                9 (@py_assert5)
#             938 CALL                     1
#             946 LOAD_CONST              17 (('py1', 'py3', 'py6'))
#             948 BUILD_CONST_KEY_MAP      3
#             950 BINARY_OP                6 (%)
#             954 STORE_FAST              10 (@py_format7)
#             956 LOAD_CONST              18 ('assert %(py8)s')
#             958 LOAD_CONST              19 ('py8')
#             960 LOAD_FAST               10 (@py_format7)
#             962 BUILD_MAP                1
#             964 BINARY_OP                6 (%)
#             968 STORE_FAST               6 (@py_format9)
#             970 LOAD_GLOBAL             23 (NULL + AssertionError)
#             980 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             990 LOAD_ATTR               24 (_format_explanation)
#            1010 LOAD_FAST                6 (@py_format9)
#            1012 CALL                     1
#            1020 CALL                     1
#            1028 RAISE_VARARGS            1
#         >> 1030 LOAD_CONST               0 (None)
#            1032 COPY                     1
#            1034 STORE_FAST               8 (@py_assert0)
#            1036 COPY                     1
#            1038 STORE_FAST               2 (@py_assert2)
#            1040 COPY                     1
#            1042 STORE_FAST               3 (@py_assert4)
#            1044 STORE_FAST               9 (@py_assert5)
# 
#  49        1046 LOAD_FAST                1 (result)
#            1048 LOAD_ATTR                6 (artifacts)
#            1068 LOAD_CONST              15 (0)
#            1070 BINARY_SUBSCR
#            1074 STORE_FAST               8 (@py_assert0)
#            1076 LOAD_FAST                8 (@py_assert0)
#            1078 LOAD_ATTR               28 (type)
#            1098 STORE_FAST               2 (@py_assert2)
#            1100 LOAD_CONST               5 ('json')
#            1102 STORE_FAST               9 (@py_assert5)
#            1104 LOAD_FAST                2 (@py_assert2)
#            1106 LOAD_FAST                9 (@py_assert5)
#            1108 COMPARE_OP              40 (==)
#            1112 STORE_FAST               3 (@py_assert4)
#            1114 LOAD_FAST                3 (@py_assert4)
#            1116 POP_JUMP_IF_TRUE       128 (to 1374)
#            1118 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1128 LOAD_ATTR               12 (_call_reprcompare)
#            1148 LOAD_CONST               8 (('==',))
#            1150 LOAD_FAST                3 (@py_assert4)
#            1152 BUILD_TUPLE              1
#            1154 LOAD_CONST              20 (('%(py3)s\n{%(py3)s = %(py1)s.type\n} == %(py6)s',))
#            1156 LOAD_FAST                2 (@py_assert2)
#            1158 LOAD_FAST                9 (@py_assert5)
#            1160 BUILD_TUPLE              2
#            1162 CALL                     4
#            1170 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1180 LOAD_ATTR               20 (_saferepr)
#            1200 LOAD_FAST                8 (@py_assert0)
#            1202 CALL                     1
#            1210 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1220 LOAD_ATTR               20 (_saferepr)
#            1240 LOAD_FAST                2 (@py_assert2)
#            1242 CALL                     1
#            1250 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1260 LOAD_ATTR               20 (_saferepr)
#            1280 LOAD_FAST                9 (@py_assert5)
#            1282 CALL                     1
#            1290 LOAD_CONST              17 (('py1', 'py3', 'py6'))
#            1292 BUILD_CONST_KEY_MAP      3
#            1294 BINARY_OP                6 (%)
#            1298 STORE_FAST              10 (@py_format7)
#            1300 LOAD_CONST              18 ('assert %(py8)s')
#            1302 LOAD_CONST              19 ('py8')
#            1304 LOAD_FAST               10 (@py_format7)
#            1306 BUILD_MAP                1
#            1308 BINARY_OP                6 (%)
#            1312 STORE_FAST               6 (@py_format9)
#            1314 LOAD_GLOBAL             23 (NULL + AssertionError)
#            1324 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1334 LOAD_ATTR               24 (_format_explanation)
#            1354 LOAD_FAST                6 (@py_format9)
#            1356 CALL                     1
#            1364 CALL                     1
#            1372 RAISE_VARARGS            1
#         >> 1374 LOAD_CONST               0 (None)
#            1376 COPY                     1
#            1378 STORE_FAST               8 (@py_assert0)
#            1380 COPY                     1
#            1382 STORE_FAST               2 (@py_assert2)
#            1384 COPY                     1
#            1386 STORE_FAST               3 (@py_assert4)
#            1388 STORE_FAST               9 (@py_assert5)
#            1390 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_to_dict at 0x3afabac0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 51>:
#  51           0 RESUME                   0
# 
#  52           2 LOAD_GLOBAL              1 (NULL + SkillResult)
#              12 LOAD_ATTR                2 (success)
#              32 LOAD_CONST               1 ('test')
#              34 LOAD_CONST               2 ('key')
#              36 LOAD_CONST               3 ('value')
#              38 BUILD_MAP                1
#              40 KW_NAMES                 4 (('skill_name', 'data'))
#              42 CALL                     2
#              50 STORE_FAST               1 (result)
# 
#  53          52 LOAD_FAST                1 (result)
#              54 LOAD_ATTR                5 (NULL|self + to_dict)
#              74 CALL                     0
#              82 STORE_FAST               2 (d)
# 
#  54          84 LOAD_FAST                2 (d)
#              86 LOAD_CONST               5 ('skill_name')
#              88 BINARY_SUBSCR
#              92 STORE_FAST               3 (@py_assert0)
#              94 LOAD_CONST               1 ('test')
#              96 STORE_FAST               4 (@py_assert3)
#              98 LOAD_FAST                3 (@py_assert0)
#             100 LOAD_FAST                4 (@py_assert3)
#             102 COMPARE_OP              40 (==)
#             106 STORE_FAST               5 (@py_assert2)
#             108 LOAD_FAST                5 (@py_assert2)
#             110 POP_JUMP_IF_TRUE       108 (to 328)
#             112 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             122 LOAD_ATTR                8 (_call_reprcompare)
#             142 LOAD_CONST               6 (('==',))
#             144 LOAD_FAST                5 (@py_assert2)
#             146 BUILD_TUPLE              1
#             148 LOAD_CONST               7 (('%(py1)s == %(py4)s',))
#             150 LOAD_FAST                3 (@py_assert0)
#             152 LOAD_FAST                4 (@py_assert3)
#             154 BUILD_TUPLE              2
#             156 CALL                     4
#             164 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             174 LOAD_ATTR               10 (_saferepr)
#             194 LOAD_FAST                3 (@py_assert0)
#             196 CALL                     1
#             204 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             214 LOAD_ATTR               10 (_saferepr)
#             234 LOAD_FAST                4 (@py_assert3)
#             236 CALL                     1
#             244 LOAD_CONST               8 (('py1', 'py4'))
#             246 BUILD_CONST_KEY_MAP      2
#             248 BINARY_OP                6 (%)
#             252 STORE_FAST               6 (@py_format5)
#             254 LOAD_CONST               9 ('assert %(py6)s')
#             256 LOAD_CONST              10 ('py6')
#             258 LOAD_FAST                6 (@py_format5)
#             260 BUILD_MAP                1
#             262 BINARY_OP                6 (%)
#             266 STORE_FAST               7 (@py_format7)
#             268 LOAD_GLOBAL             13 (NULL + AssertionError)
#             278 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             288 LOAD_ATTR               14 (_format_explanation)
#             308 LOAD_FAST                7 (@py_format7)
#             310 CALL                     1
#             318 CALL                     1
#             326 RAISE_VARARGS            1
#         >>  328 LOAD_CONST               0 (None)
#             330 COPY                     1
#             332 STORE_FAST               3 (@py_assert0)
#             334 COPY                     1
#             336 STORE_FAST               5 (@py_assert2)
#             338 STORE_FAST               4 (@py_assert3)
# 
#  55         340 LOAD_FAST                2 (d)
#             342 LOAD_CONST              11 ('status')
#             344 BINARY_SUBSCR
#             348 STORE_FAST               3 (@py_assert0)
#             350 LOAD_CONST              12 ('success')
#             352 STORE_FAST               4 (@py_assert3)
#             354 LOAD_FAST                3 (@py_assert0)
#             356 LOAD_FAST                4 (@py_assert3)
#             358 COMPARE_OP              40 (==)
#             362 STORE_FAST               5 (@py_assert2)
#             364 LOAD_FAST                5 (@py_assert2)
#             366 POP_JUMP_IF_TRUE       108 (to 584)
#             368 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             378 LOAD_ATTR                8 (_call_reprcompare)
#             398 LOAD_CONST               6 (('==',))
#             400 LOAD_FAST                5 (@py_assert2)
#             402 BUILD_TUPLE              1
#             404 LOAD_CONST               7 (('%(py1)s == %(py4)s',))
#             406 LOAD_FAST                3 (@py_assert0)
#             408 LOAD_FAST                4 (@py_assert3)
#             410 BUILD_TUPLE              2
#             412 CALL                     4
#             420 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             430 LOAD_ATTR               10 (_saferepr)
#             450 LOAD_FAST                3 (@py_assert0)
#             452 CALL                     1
#             460 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             470 LOAD_ATTR               10 (_saferepr)
#             490 LOAD_FAST                4 (@py_assert3)
#             492 CALL                     1
#             500 LOAD_CONST               8 (('py1', 'py4'))
#             502 BUILD_CONST_KEY_MAP      2
#             504 BINARY_OP                6 (%)
#             508 STORE_FAST               6 (@py_format5)
#             510 LOAD_CONST               9 ('assert %(py6)s')
#             512 LOAD_CONST              10 ('py6')
#             514 LOAD_FAST                6 (@py_format5)
#             516 BUILD_MAP                1
#             518 BINARY_OP                6 (%)
#             522 STORE_FAST               7 (@py_format7)
#             524 LOAD_GLOBAL             13 (NULL + AssertionError)
#             534 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             544 LOAD_ATTR               14 (_format_explanation)
#             564 LOAD_FAST                7 (@py_format7)
#             566 CALL                     1
#             574 CALL                     1
#             582 RAISE_VARARGS            1
#         >>  584 LOAD_CONST               0 (None)
#             586 COPY                     1
#             588 STORE_FAST               3 (@py_assert0)
#             590 COPY                     1
#             592 STORE_FAST               5 (@py_assert2)
#             594 STORE_FAST               4 (@py_assert3)
# 
#  56         596 LOAD_FAST                2 (d)
#             598 LOAD_CONST              12 ('success')
#             600 BINARY_SUBSCR
#             604 STORE_FAST               3 (@py_assert0)
#             606 LOAD_CONST              13 (True)
#             608 STORE_FAST               4 (@py_assert3)
#             610 LOAD_FAST                3 (@py_assert0)
#             612 LOAD_FAST                4 (@py_assert3)
#             614 IS_OP                    0
#             616 STORE_FAST               5 (@py_assert2)
#             618 LOAD_FAST                5 (@py_assert2)
#             620 POP_JUMP_IF_TRUE       108 (to 838)
#             622 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             632 LOAD_ATTR                8 (_call_reprcompare)
#             652 LOAD_CONST              14 (('is',))
#             654 LOAD_FAST                5 (@py_assert2)
#             656 BUILD_TUPLE              1
#             658 LOAD_CONST              15 (('%(py1)s is %(py4)s',))
#             660 LOAD_FAST                3 (@py_assert0)
#             662 LOAD_FAST                4 (@py_assert3)
#             664 BUILD_TUPLE              2
#             666 CALL                     4
#             674 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             684 LOAD_ATTR               10 (_saferepr)
#             704 LOAD_FAST                3 (@py_assert0)
#             706 CALL                     1
#             714 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             724 LOAD_ATTR               10 (_saferepr)
#             744 LOAD_FAST                4 (@py_assert3)
#             746 CALL                     1
#             754 LOAD_CONST               8 (('py1', 'py4'))
#             756 BUILD_CONST_KEY_MAP      2
#             758 BINARY_OP                6 (%)
#             762 STORE_FAST               6 (@py_format5)
#             764 LOAD_CONST               9 ('assert %(py6)s')
#             766 LOAD_CONST              10 ('py6')
#             768 LOAD_FAST                6 (@py_format5)
#             770 BUILD_MAP                1
#             772 BINARY_OP                6 (%)
#             776 STORE_FAST               7 (@py_format7)
#             778 LOAD_GLOBAL             13 (NULL + AssertionError)
#             788 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             798 LOAD_ATTR               14 (_format_explanation)
#             818 LOAD_FAST                7 (@py_format7)
#             820 CALL                     1
#             828 CALL                     1
#             836 RAISE_VARARGS            1
#         >>  838 LOAD_CONST               0 (None)
#             840 COPY                     1
#             842 STORE_FAST               3 (@py_assert0)
#             844 COPY                     1
#             846 STORE_FAST               5 (@py_assert2)
#             848 STORE_FAST               4 (@py_assert3)
# 
#  57         850 LOAD_FAST                2 (d)
#             852 LOAD_CONST              16 ('data')
#             854 BINARY_SUBSCR
#             858 STORE_FAST               3 (@py_assert0)
#             860 LOAD_CONST               2 ('key')
#             862 LOAD_CONST               3 ('value')
#             864 BUILD_MAP                1
#             866 STORE_FAST               4 (@py_assert3)
#             868 LOAD_FAST                3 (@py_assert0)
#             870 LOAD_FAST                4 (@py_assert3)
#             872 COMPARE_OP              40 (==)
#             876 STORE_FAST               5 (@py_assert2)
#             878 LOAD_FAST                5 (@py_assert2)
#             880 POP_JUMP_IF_TRUE       108 (to 1098)
#             882 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             892 LOAD_ATTR                8 (_call_reprcompare)
#             912 LOAD_CONST               6 (('==',))
#             914 LOAD_FAST                5 (@py_assert2)
#             916 BUILD_TUPLE              1
#             918 LOAD_CONST               7 (('%(py1)s == %(py4)s',))
#             920 LOAD_FAST                3 (@py_assert0)
#             922 LOAD_FAST                4 (@py_assert3)
#             924 BUILD_TUPLE              2
#             926 CALL                     4
#             934 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             944 LOAD_ATTR               10 (_saferepr)
#             964 LOAD_FAST                3 (@py_assert0)
#             966 CALL                     1
#             974 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             984 LOAD_ATTR               10 (_saferepr)
#            1004 LOAD_FAST                4 (@py_assert3)
#            1006 CALL                     1
#            1014 LOAD_CONST               8 (('py1', 'py4'))
#            1016 BUILD_CONST_KEY_MAP      2
#            1018 BINARY_OP                6 (%)
#            1022 STORE_FAST               6 (@py_format5)
#            1024 LOAD_CONST               9 ('assert %(py6)s')
#            1026 LOAD_CONST              10 ('py6')
#            1028 LOAD_FAST                6 (@py_format5)
#            1030 BUILD_MAP                1
#            1032 BINARY_OP                6 (%)
#            1036 STORE_FAST               7 (@py_format7)
#            1038 LOAD_GLOBAL             13 (NULL + AssertionError)
#            1048 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1058 LOAD_ATTR               14 (_format_explanation)
#            1078 LOAD_FAST                7 (@py_format7)
#            1080 CALL                     1
#            1088 CALL                     1
#            1096 RAISE_VARARGS            1
#         >> 1098 LOAD_CONST               0 (None)
#            1100 COPY                     1
#            1102 STORE_FAST               3 (@py_assert0)
#            1104 COPY                     1
#            1106 STORE_FAST               5 (@py_assert2)
#            1108 STORE_FAST               4 (@py_assert3)
#            1110 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_duration_calculation at 0x3aefe140, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 59>:
#  59           0 RESUME                   0
# 
#  60           2 LOAD_GLOBAL              1 (NULL + datetime)
#              12 LOAD_ATTR                2 (now)
#              32 CALL                     0
#              40 STORE_FAST               1 (now)
# 
#  61          42 LOAD_GLOBAL              5 (NULL + SkillResult)
# 
#  62          52 LOAD_CONST               1 ('test')
# 
#  63          54 LOAD_GLOBAL              6 (SkillStatus)
#              64 LOAD_ATTR                8 (SUCCESS)
# 
#  64          84 LOAD_FAST                1 (now)
# 
#  65          86 LOAD_FAST                1 (now)
# 
#  61          88 KW_NAMES                 2 (('skill_name', 'status', 'start_time', 'end_time'))
#              90 CALL                     4
#              98 STORE_FAST               2 (result)
# 
#  67         100 LOAD_FAST                2 (result)
#             102 LOAD_ATTR               10 (duration_seconds)
#             122 STORE_FAST               3 (@py_assert1)
#             124 LOAD_CONST               3 (0.0)
#             126 STORE_FAST               4 (@py_assert4)
#             128 LOAD_FAST                3 (@py_assert1)
#             130 LOAD_FAST                4 (@py_assert4)
#             132 COMPARE_OP              40 (==)
#             136 STORE_FAST               5 (@py_assert3)
#             138 LOAD_FAST                5 (@py_assert3)
#             140 POP_JUMP_IF_TRUE       173 (to 488)
#             142 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             152 LOAD_ATTR               14 (_call_reprcompare)
#             172 LOAD_CONST               4 (('==',))
#             174 LOAD_FAST                5 (@py_assert3)
#             176 BUILD_TUPLE              1
#             178 LOAD_CONST               5 (('%(py2)s\n{%(py2)s = %(py0)s.duration_seconds\n} == %(py5)s',))
#             180 LOAD_FAST                3 (@py_assert1)
#             182 LOAD_FAST                4 (@py_assert4)
#             184 BUILD_TUPLE              2
#             186 CALL                     4
#             194 LOAD_CONST               6 ('result')
#             196 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             206 LOAD_ATTR               18 (locals)
#             226 CALL                     0
#             234 CONTAINS_OP              0
#             236 POP_JUMP_IF_TRUE        21 (to 280)
#             238 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             248 LOAD_ATTR               20 (_should_repr_global_name)
#             268 LOAD_FAST                2 (result)
#             270 CALL                     1
#             278 POP_JUMP_IF_FALSE       21 (to 322)
#         >>  280 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             290 LOAD_ATTR               22 (_saferepr)
#             310 LOAD_FAST                2 (result)
#             312 CALL                     1
#             320 JUMP_FORWARD             1 (to 324)
#         >>  322 LOAD_CONST               6 ('result')
#         >>  324 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             334 LOAD_ATTR               22 (_saferepr)
#             354 LOAD_FAST                3 (@py_assert1)
#             356 CALL                     1
#             364 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             374 LOAD_ATTR               22 (_saferepr)
#             394 LOAD_FAST                4 (@py_assert4)
#             396 CALL                     1
#             404 LOAD_CONST               7 (('py0', 'py2', 'py5'))
#             406 BUILD_CONST_KEY_MAP      3
#             408 BINARY_OP                6 (%)
#             412 STORE_FAST               6 (@py_format6)
#             414 LOAD_CONST               8 ('assert %(py7)s')
#             416 LOAD_CONST               9 ('py7')
#             418 LOAD_FAST                6 (@py_format6)
#             420 BUILD_MAP                1
#             422 BINARY_OP                6 (%)
#             426 STORE_FAST               7 (@py_format8)
#             428 LOAD_GLOBAL             25 (NULL + AssertionError)
#             438 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             448 LOAD_ATTR               26 (_format_explanation)
#             468 LOAD_FAST                7 (@py_format8)
#             470 CALL                     1
#             478 CALL                     1
#             486 RAISE_VARARGS            1
#         >>  488 LOAD_CONST               0 (None)
#             490 COPY                     1
#             492 STORE_FAST               3 (@py_assert1)
#             494 COPY                     1
#             496 STORE_FAST               5 (@py_assert3)
#             498 STORE_FAST               4 (@py_assert4)
#             500 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_has_error at 0x3aed21e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 69>:
#  69           0 RESUME                   0
# 
#  70           2 LOAD_GLOBAL              1 (NULL + SkillResult)
#              12 LOAD_ATTR                2 (failure)
#              32 LOAD_CONST               1 ('test')
#              34 LOAD_CONST               2 ('error message')
#              36 KW_NAMES                 3 (('skill_name', 'error'))
#              38 CALL                     2
#              46 STORE_FAST               1 (result)
# 
#  71          48 LOAD_FAST                1 (result)
#              50 LOAD_ATTR                4 (has_error)
#              70 STORE_FAST               2 (@py_assert1)
#              72 LOAD_CONST               4 (True)
#              74 STORE_FAST               3 (@py_assert4)
#              76 LOAD_FAST                2 (@py_assert1)
#              78 LOAD_FAST                3 (@py_assert4)
#              80 IS_OP                    0
#              82 STORE_FAST               4 (@py_assert3)
#              84 LOAD_FAST                4 (@py_assert3)
#              86 POP_JUMP_IF_TRUE       173 (to 434)
#              88 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#              98 LOAD_ATTR                8 (_call_reprcompare)
#             118 LOAD_CONST               5 (('is',))
#             120 LOAD_FAST                4 (@py_assert3)
#             122 BUILD_TUPLE              1
#             124 LOAD_CONST               6 (('%(py2)s\n{%(py2)s = %(py0)s.has_error\n} is %(py5)s',))
#             126 LOAD_FAST                2 (@py_assert1)
#             128 LOAD_FAST                3 (@py_assert4)
#             130 BUILD_TUPLE              2
#             132 CALL                     4
#             140 LOAD_CONST               7 ('result')
#             142 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             152 LOAD_ATTR               12 (locals)
#             172 CALL                     0
#             180 CONTAINS_OP              0
#             182 POP_JUMP_IF_TRUE        21 (to 226)
#             184 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             194 LOAD_ATTR               14 (_should_repr_global_name)
#             214 LOAD_FAST                1 (result)
#             216 CALL                     1
#             224 POP_JUMP_IF_FALSE       21 (to 268)
#         >>  226 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             236 LOAD_ATTR               16 (_saferepr)
#             256 LOAD_FAST                1 (result)
#             258 CALL                     1
#             266 JUMP_FORWARD             1 (to 270)
#         >>  268 LOAD_CONST               7 ('result')
#         >>  270 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             280 LOAD_ATTR               16 (_saferepr)
#             300 LOAD_FAST                2 (@py_assert1)
#             302 CALL                     1
#             310 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             320 LOAD_ATTR               16 (_saferepr)
#             340 LOAD_FAST                3 (@py_assert4)
#             342 CALL                     1
#             350 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#             352 BUILD_CONST_KEY_MAP      3
#             354 BINARY_OP                6 (%)
#             358 STORE_FAST               5 (@py_format6)
#             360 LOAD_CONST               9 ('assert %(py7)s')
#             362 LOAD_CONST              10 ('py7')
#             364 LOAD_FAST                5 (@py_format6)
#             366 BUILD_MAP                1
#             368 BINARY_OP                6 (%)
#             372 STORE_FAST               6 (@py_format8)
#             374 LOAD_GLOBAL             19 (NULL + AssertionError)
#             384 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             394 LOAD_ATTR               20 (_format_explanation)
#             414 LOAD_FAST                6 (@py_format8)
#             416 CALL                     1
#             424 CALL                     1
#             432 RAISE_VARARGS            1
#         >>  434 LOAD_CONST               0 (None)
#             436 COPY                     1
#             438 STORE_FAST               2 (@py_assert1)
#             440 COPY                     1
#             442 STORE_FAST               4 (@py_assert3)
#             444 STORE_FAST               3 (@py_assert4)
# 
#  73         446 LOAD_GLOBAL              1 (NULL + SkillResult)
#             456 LOAD_ATTR               22 (success)
#             476 LOAD_CONST               1 ('test')
#             478 BUILD_MAP                0
#             480 KW_NAMES                11 (('skill_name', 'data'))
#             482 CALL                     2
#             490 STORE_FAST               7 (success_result)
# 
#  74         492 LOAD_FAST                7 (success_result)
#             494 LOAD_ATTR                4 (has_error)
#             514 STORE_FAST               2 (@py_assert1)
#             516 LOAD_CONST              12 (False)
#             518 STORE_FAST               3 (@py_assert4)
#             520 LOAD_FAST                2 (@py_assert1)
#             522 LOAD_FAST                3 (@py_assert4)
#             524 IS_OP                    0
#             526 STORE_FAST               4 (@py_assert3)
#             528 LOAD_FAST                4 (@py_assert3)
#             530 POP_JUMP_IF_TRUE       173 (to 878)
#             532 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             542 LOAD_ATTR                8 (_call_reprcompare)
#             562 LOAD_CONST               5 (('is',))
#             564 LOAD_FAST                4 (@py_assert3)
#             566 BUILD_TUPLE              1
#             568 LOAD_CONST               6 (('%(py2)s\n{%(py2)s = %(py0)s.has_error\n} is %(py5)s',))
#             570 LOAD_FAST                2 (@py_assert1)
#             572 LOAD_FAST                3 (@py_assert4)
#             574 BUILD_TUPLE              2
#             576 CALL                     4
#             584 LOAD_CONST              13 ('success_result')
#             586 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             596 LOAD_ATTR               12 (locals)
#             616 CALL                     0
#             624 CONTAINS_OP              0
#             626 POP_JUMP_IF_TRUE        21 (to 670)
#             628 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             638 LOAD_ATTR               14 (_should_repr_global_name)
#             658 LOAD_FAST                7 (success_result)
#             660 CALL                     1
#             668 POP_JUMP_IF_FALSE       21 (to 712)
#         >>  670 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             680 LOAD_ATTR               16 (_saferepr)
#             700 LOAD_FAST                7 (success_result)
#             702 CALL                     1
#             710 JUMP_FORWARD             1 (to 714)
#         >>  712 LOAD_CONST              13 ('success_result')
#         >>  714 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             724 LOAD_ATTR               16 (_saferepr)
#             744 LOAD_FAST                2 (@py_assert1)
#             746 CALL                     1
#             754 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             764 LOAD_ATTR               16 (_saferepr)
#             784 LOAD_FAST                3 (@py_assert4)
#             786 CALL                     1
#             794 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#             796 BUILD_CONST_KEY_MAP      3
#             798 BINARY_OP                6 (%)
#             802 STORE_FAST               5 (@py_format6)
#             804 LOAD_CONST               9 ('assert %(py7)s')
#             806 LOAD_CONST              10 ('py7')
#             808 LOAD_FAST                5 (@py_format6)
#             810 BUILD_MAP                1
#             812 BINARY_OP                6 (%)
#             816 STORE_FAST               6 (@py_format8)
#             818 LOAD_GLOBAL             19 (NULL + AssertionError)
#             828 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             838 LOAD_ATTR               20 (_format_explanation)
#             858 LOAD_FAST                6 (@py_format8)
#             860 CALL                     1
#             868 CALL                     1
#             876 RAISE_VARARGS            1
#         >>  878 LOAD_CONST               0 (None)
#             880 COPY                     1
#             882 STORE_FAST               2 (@py_assert1)
#             884 COPY                     1
#             886 STORE_FAST               4 (@py_assert3)
#             888 STORE_FAST               3 (@py_assert4)
#             890 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestSkillOutputValidator at 0x73cd93b31930, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 77>:
#  77           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestSkillOutputValidator')
#               8 STORE_NAME               2 (__qualname__)
# 
#  78          10 LOAD_CONST               1 (<code object test_validate_success_result at 0x3aef8860, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 78>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_validate_success_result)
# 
#  87          16 LOAD_CONST               2 (<code object test_validate_missing_base_field at 0x3aed30d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 87>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_validate_missing_base_field)
# 
# 104          22 LOAD_CONST               3 (<code object test_validate_simulation_type_requirements at 0x3aef47a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 104>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_validate_simulation_type_requirements)
# 
# 113          28 LOAD_CONST               4 (<code object test_validate_failure_path_with_error at 0x3aefd020, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 113>)
#              30 MAKE_FUNCTION            0
#              32 STORE_NAME               6 (test_validate_failure_path_with_error)
# 
# 119          34 LOAD_CONST               5 (<code object test_validate_failure_path_missing_error at 0x3aefbf80, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 119>)
#              36 MAKE_FUNCTION            0
#              38 STORE_NAME               7 (test_validate_failure_path_missing_error)
# 
# 130          40 LOAD_CONST               6 (<code object test_validate_failure_path_inconsistent_status at 0x3af3ed40, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 130>)
#              42 MAKE_FUNCTION            0
#              44 STORE_NAME               8 (test_validate_failure_path_inconsistent_status)
# 
# 141          46 LOAD_CONST               7 (<code object test_validate_field_naming_snake_case at 0x3afa7230, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 141>)
#              48 MAKE_FUNCTION            0
#              50 STORE_NAME               9 (test_validate_field_naming_snake_case)
# 
# 147          52 LOAD_CONST               8 (<code object test_validate_field_naming_camel_case_warning at 0x3afa13e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 147>)
#              54 MAKE_FUNCTION            0
#              56 STORE_NAME              10 (test_validate_field_naming_camel_case_warning)
#              58 RETURN_CONST             9 (None)
# 
# Disassembly of <code object test_validate_success_result at 0x3aef8860, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 78>:
#  78           0 RESUME                   0
# 
#  79           2 LOAD_GLOBAL              1 (NULL + SkillOutputValidator)
#              12 CALL                     0
#              20 STORE_FAST               1 (validator)
# 
#  80          22 LOAD_GLOBAL              3 (NULL + SkillResult)
#              32 LOAD_ATTR                4 (success)
# 
#  81          52 LOAD_CONST               1 ('power_flow')
# 
#  82          54 LOAD_CONST               2 (True)
#              56 BUILD_MAP                0
#              58 BUILD_MAP                0
#              60 LOAD_CONST               3 (('converged', 'model_info', 'summary'))
#              62 BUILD_CONST_KEY_MAP      3
# 
#  80          64 KW_NAMES                 4 (('skill_name', 'data'))
#              66 CALL                     2
#              74 STORE_FAST               2 (result)
# 
#  84          76 LOAD_FAST                1 (validator)
#              78 LOAD_ATTR                7 (NULL|self + validate)
#              98 LOAD_FAST                2 (result)
#             100 CALL                     1
#             108 STORE_FAST               3 (validation)
# 
#  85         110 LOAD_FAST                3 (validation)
#             112 LOAD_ATTR                8 (valid)
#             132 STORE_FAST               4 (@py_assert1)
#             134 LOAD_CONST               2 (True)
#             136 STORE_FAST               5 (@py_assert4)
#             138 LOAD_FAST                4 (@py_assert1)
#             140 LOAD_FAST                5 (@py_assert4)
#             142 IS_OP                    0
#             144 STORE_FAST               6 (@py_assert3)
#             146 LOAD_FAST                6 (@py_assert3)
#             148 POP_JUMP_IF_TRUE       173 (to 496)
#             150 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             160 LOAD_ATTR               12 (_call_reprcompare)
#             180 LOAD_CONST               5 (('is',))
#             182 LOAD_FAST                6 (@py_assert3)
#             184 BUILD_TUPLE              1
#             186 LOAD_CONST               6 (('%(py2)s\n{%(py2)s = %(py0)s.valid\n} is %(py5)s',))
#             188 LOAD_FAST                4 (@py_assert1)
#             190 LOAD_FAST                5 (@py_assert4)
#             192 BUILD_TUPLE              2
#             194 CALL                     4
#             202 LOAD_CONST               7 ('validation')
#             204 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             214 LOAD_ATTR               16 (locals)
#             234 CALL                     0
#             242 CONTAINS_OP              0
#             244 POP_JUMP_IF_TRUE        21 (to 288)
#             246 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             256 LOAD_ATTR               18 (_should_repr_global_name)
#             276 LOAD_FAST                3 (validation)
#             278 CALL                     1
#             286 POP_JUMP_IF_FALSE       21 (to 330)
#         >>  288 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             298 LOAD_ATTR               20 (_saferepr)
#             318 LOAD_FAST                3 (validation)
#             320 CALL                     1
#             328 JUMP_FORWARD             1 (to 332)
#         >>  330 LOAD_CONST               7 ('validation')
#         >>  332 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             342 LOAD_ATTR               20 (_saferepr)
#             362 LOAD_FAST                4 (@py_assert1)
#             364 CALL                     1
#             372 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             382 LOAD_ATTR               20 (_saferepr)
#             402 LOAD_FAST                5 (@py_assert4)
#             404 CALL                     1
#             412 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#             414 BUILD_CONST_KEY_MAP      3
#             416 BINARY_OP                6 (%)
#             420 STORE_FAST               7 (@py_format6)
#             422 LOAD_CONST               9 ('assert %(py7)s')
#             424 LOAD_CONST              10 ('py7')
#             426 LOAD_FAST                7 (@py_format6)
#             428 BUILD_MAP                1
#             430 BINARY_OP                6 (%)
#             434 STORE_FAST               8 (@py_format8)
#             436 LOAD_GLOBAL             23 (NULL + AssertionError)
#             446 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             456 LOAD_ATTR               24 (_format_explanation)
#             476 LOAD_FAST                8 (@py_format8)
#             478 CALL                     1
#             486 CALL                     1
#             494 RAISE_VARARGS            1
#         >>  496 LOAD_CONST               0 (None)
#             498 COPY                     1
#             500 STORE_FAST               4 (@py_assert1)
#             502 COPY                     1
#             504 STORE_FAST               6 (@py_assert3)
#             506 STORE_FAST               5 (@py_assert4)
#             508 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_missing_base_field at 0x3aed30d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 87>:
#  87           0 RESUME                   0
# 
#  88           2 LOAD_GLOBAL              1 (NULL + SkillOutputValidator)
#              12 CALL                     0
#              20 STORE_FAST               1 (validator)
# 
#  89          22 LOAD_GLOBAL              3 (NULL + SkillResult)
# 
#  90          32 LOAD_CONST               1 ('')
# 
#  91          34 LOAD_GLOBAL              4 (SkillStatus)
#              44 LOAD_ATTR                6 (SUCCESS)
# 
#  92          64 BUILD_MAP                0
# 
#  89          66 KW_NAMES                 2 (('skill_name', 'status', 'data'))
#              68 CALL                     3
#              76 STORE_FAST               2 (result)
# 
#  94          78 LOAD_FAST                2 (result)
#              80 LOAD_ATTR                9 (NULL|self + to_dict)
#             100 CALL                     0
#             108 STORE_FAST               3 (d)
# 
#  95         110 BUILD_LIST               0
#             112 STORE_FAST               4 (@py_assert1)
#             114 LOAD_CONST               3 ('skill_name')
#             116 STORE_FAST               5 (@py_assert2)
#             118 LOAD_FAST                5 (@py_assert2)
#             120 LOAD_FAST                3 (d)
#             122 CONTAINS_OP              1
#             124 STORE_FAST               6 (@py_assert4)
#             126 LOAD_FAST                6 (@py_assert4)
#             128 STORE_FAST               7 (@py_assert0)
#             130 LOAD_FAST                6 (@py_assert4)
#             132 POP_JUMP_IF_TRUE        14 (to 162)
#             134 LOAD_FAST                3 (d)
#             136 LOAD_CONST               3 ('skill_name')
#             138 BINARY_SUBSCR
#             142 STORE_FAST               8 (@py_assert9)
#             144 LOAD_CONST               1 ('')
#             146 STORE_FAST               9 (@py_assert12)
#             148 LOAD_FAST                8 (@py_assert9)
#             150 LOAD_FAST                9 (@py_assert12)
#             152 COMPARE_OP              40 (==)
#             156 STORE_FAST              10 (@py_assert11)
#             158 LOAD_FAST               10 (@py_assert11)
#             160 STORE_FAST               7 (@py_assert0)
#         >>  162 LOAD_FAST                7 (@py_assert0)
#             164 EXTENDED_ARG             1
#             166 POP_JUMP_IF_TRUE       299 (to 766)
#             168 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             178 LOAD_ATTR               12 (_call_reprcompare)
#             198 LOAD_CONST               4 (('not in',))
#             200 LOAD_FAST                6 (@py_assert4)
#             202 BUILD_TUPLE              1
#             204 LOAD_CONST               5 (('%(py3)s not in %(py5)s',))
#             206 LOAD_FAST                5 (@py_assert2)
#             208 LOAD_FAST                3 (d)
#             210 BUILD_TUPLE              2
#             212 CALL                     4
#             220 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             230 LOAD_ATTR               14 (_saferepr)
#             250 LOAD_FAST                5 (@py_assert2)
#             252 CALL                     1
#             260 LOAD_CONST               6 ('d')
#             262 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             272 LOAD_ATTR               18 (locals)
#             292 CALL                     0
#             300 CONTAINS_OP              0
#             302 POP_JUMP_IF_TRUE        21 (to 346)
#             304 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             314 LOAD_ATTR               20 (_should_repr_global_name)
#             334 LOAD_FAST                3 (d)
#             336 CALL                     1
#             344 POP_JUMP_IF_FALSE       21 (to 388)
#         >>  346 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             356 LOAD_ATTR               14 (_saferepr)
#             376 LOAD_FAST                3 (d)
#             378 CALL                     1
#             386 JUMP_FORWARD             1 (to 390)
#         >>  388 LOAD_CONST               6 ('d')
#         >>  390 LOAD_CONST               7 (('py3', 'py5'))
#             392 BUILD_CONST_KEY_MAP      2
#             394 BINARY_OP                6 (%)
#             398 STORE_FAST              11 (@py_format6)
#             400 LOAD_CONST               8 ('%(py7)s')
#             402 LOAD_CONST               9 ('py7')
#             404 LOAD_FAST               11 (@py_format6)
#             406 BUILD_MAP                1
#             408 BINARY_OP                6 (%)
#             412 STORE_FAST              12 (@py_format8)
#             414 LOAD_FAST                4 (@py_assert1)
#             416 LOAD_ATTR               23 (NULL|self + append)
#             436 LOAD_FAST               12 (@py_format8)
#             438 CALL                     1
#             446 POP_TOP
#             448 LOAD_FAST                6 (@py_assert4)
#             450 POP_JUMP_IF_TRUE        95 (to 642)
#             452 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             462 LOAD_ATTR               12 (_call_reprcompare)
#             482 LOAD_CONST              10 (('==',))
#             484 LOAD_FAST_CHECK         10 (@py_assert11)
#             486 BUILD_TUPLE              1
#             488 LOAD_CONST              11 (('%(py10)s == %(py13)s',))
#             490 LOAD_FAST_CHECK          8 (@py_assert9)
#             492 LOAD_FAST_CHECK          9 (@py_assert12)
#             494 BUILD_TUPLE              2
#             496 CALL                     4
#             504 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             514 LOAD_ATTR               14 (_saferepr)
#             534 LOAD_FAST                8 (@py_assert9)
#             536 CALL                     1
#             544 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             554 LOAD_ATTR               14 (_saferepr)
#             574 LOAD_FAST                9 (@py_assert12)
#             576 CALL                     1
#             584 LOAD_CONST              12 (('py10', 'py13'))
#             586 BUILD_CONST_KEY_MAP      2
#             588 BINARY_OP                6 (%)
#             592 STORE_FAST              13 (@py_format14)
#             594 LOAD_CONST              13 ('%(py15)s')
#             596 LOAD_CONST              14 ('py15')
#             598 LOAD_FAST               13 (@py_format14)
#             600 BUILD_MAP                1
#             602 BINARY_OP                6 (%)
#             606 STORE_FAST              14 (@py_format16)
#             608 LOAD_FAST                4 (@py_assert1)
#             610 LOAD_ATTR               23 (NULL|self + append)
#             630 LOAD_FAST               14 (@py_format16)
#             632 CALL                     1
#             640 POP_TOP
#         >>  642 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             652 LOAD_ATTR               24 (_format_boolop)
#             672 LOAD_FAST                4 (@py_assert1)
#             674 LOAD_CONST              15 (1)
#             676 CALL                     2
#             684 BUILD_MAP                0
#             686 BINARY_OP                6 (%)
#             690 STORE_FAST              15 (@py_format17)
#             692 LOAD_CONST              16 ('assert %(py18)s')
#             694 LOAD_CONST              17 ('py18')
#             696 LOAD_FAST               15 (@py_format17)
#             698 BUILD_MAP                1
#             700 BINARY_OP                6 (%)
#             704 STORE_FAST              16 (@py_format19)
#             706 LOAD_GLOBAL             27 (NULL + AssertionError)
#             716 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             726 LOAD_ATTR               28 (_format_explanation)
#             746 LOAD_FAST               16 (@py_format19)
#             748 CALL                     1
#             756 CALL                     1
#             764 RAISE_VARARGS            1
#         >>  766 LOAD_CONST               0 (None)
#             768 COPY                     1
#             770 STORE_FAST               7 (@py_assert0)
#             772 COPY                     1
#             774 STORE_FAST               4 (@py_assert1)
#             776 COPY                     1
#             778 STORE_FAST               5 (@py_assert2)
#             780 COPY                     1
#             782 STORE_FAST               6 (@py_assert4)
#             784 COPY                     1
#             786 STORE_FAST               8 (@py_assert9)
#             788 COPY                     1
#             790 STORE_FAST              10 (@py_assert11)
#             792 STORE_FAST               9 (@py_assert12)
# 
#  96         794 LOAD_GLOBAL              3 (NULL + SkillResult)
# 
#  97         804 LOAD_CONST              18 ('test')
# 
#  98         806 LOAD_GLOBAL              4 (SkillStatus)
#             816 LOAD_ATTR                6 (SUCCESS)
# 
#  99         836 BUILD_MAP                0
# 
#  96         838 KW_NAMES                 2 (('skill_name', 'status', 'data'))
#             840 CALL                     3
#             848 STORE_FAST              17 (result2)
# 
# 101         850 LOAD_FAST                1 (validator)
#             852 LOAD_ATTR               31 (NULL|self + validate)
#             872 LOAD_FAST               17 (result2)
#             874 CALL                     1
#             882 STORE_FAST              18 (validation)
# 
# 102         884 LOAD_FAST               18 (validation)
#             886 LOAD_ATTR               32 (valid)
#             906 STORE_FAST               4 (@py_assert1)
#             908 LOAD_CONST              19 (True)
#             910 STORE_FAST               6 (@py_assert4)
#             912 LOAD_FAST                4 (@py_assert1)
#             914 LOAD_FAST                6 (@py_assert4)
#             916 IS_OP                    0
#             918 STORE_FAST              19 (@py_assert3)
#             920 LOAD_FAST               19 (@py_assert3)
#             922 POP_JUMP_IF_TRUE       173 (to 1270)
#             924 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             934 LOAD_ATTR               12 (_call_reprcompare)
#             954 LOAD_CONST              20 (('is',))
#             956 LOAD_FAST               19 (@py_assert3)
#             958 BUILD_TUPLE              1
#             960 LOAD_CONST              21 (('%(py2)s\n{%(py2)s = %(py0)s.valid\n} is %(py5)s',))
#             962 LOAD_FAST                4 (@py_assert1)
#             964 LOAD_FAST                6 (@py_assert4)
#             966 BUILD_TUPLE              2
#             968 CALL                     4
#             976 LOAD_CONST              22 ('validation')
#             978 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             988 LOAD_ATTR               18 (locals)
#            1008 CALL                     0
#            1016 CONTAINS_OP              0
#            1018 POP_JUMP_IF_TRUE        21 (to 1062)
#            1020 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1030 LOAD_ATTR               20 (_should_repr_global_name)
#            1050 LOAD_FAST               18 (validation)
#            1052 CALL                     1
#            1060 POP_JUMP_IF_FALSE       21 (to 1104)
#         >> 1062 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1072 LOAD_ATTR               14 (_saferepr)
#            1092 LOAD_FAST               18 (validation)
#            1094 CALL                     1
#            1102 JUMP_FORWARD             1 (to 1106)
#         >> 1104 LOAD_CONST              22 ('validation')
#         >> 1106 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1116 LOAD_ATTR               14 (_saferepr)
#            1136 LOAD_FAST                4 (@py_assert1)
#            1138 CALL                     1
#            1146 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1156 LOAD_ATTR               14 (_saferepr)
#            1176 LOAD_FAST                6 (@py_assert4)
#            1178 CALL                     1
#            1186 LOAD_CONST              23 (('py0', 'py2', 'py5'))
#            1188 BUILD_CONST_KEY_MAP      3
#            1190 BINARY_OP                6 (%)
#            1194 STORE_FAST              11 (@py_format6)
#            1196 LOAD_CONST              24 ('assert %(py7)s')
#            1198 LOAD_CONST               9 ('py7')
#            1200 LOAD_FAST               11 (@py_format6)
#            1202 BUILD_MAP                1
#            1204 BINARY_OP                6 (%)
#            1208 STORE_FAST              12 (@py_format8)
#            1210 LOAD_GLOBAL             27 (NULL + AssertionError)
#            1220 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1230 LOAD_ATTR               28 (_format_explanation)
#            1250 LOAD_FAST               12 (@py_format8)
#            1252 CALL                     1
#            1260 CALL                     1
#            1268 RAISE_VARARGS            1
#         >> 1270 LOAD_CONST               0 (None)
#            1272 COPY                     1
#            1274 STORE_FAST               4 (@py_assert1)
#            1276 COPY                     1
#            1278 STORE_FAST              19 (@py_assert3)
#            1280 STORE_FAST               6 (@py_assert4)
#            1282 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_simulation_type_requirements at 0x3aef47a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 104>:
# 104           0 RESUME                   0
# 
# 105           2 LOAD_GLOBAL              1 (NULL + SkillOutputValidator)
#              12 CALL                     0
#              20 STORE_FAST               1 (validator)
# 
# 106          22 LOAD_GLOBAL              3 (NULL + SkillResult)
#              32 LOAD_ATTR                4 (success)
# 
# 107          52 LOAD_CONST               1 ('power_flow')
# 
# 108          54 LOAD_CONST               2 (True)
#              56 BUILD_MAP                0
#              58 BUILD_MAP                0
#              60 LOAD_CONST               3 (('converged', 'model_info', 'summary'))
#              62 BUILD_CONST_KEY_MAP      3
# 
# 106          64 KW_NAMES                 4 (('skill_name', 'data'))
#              66 CALL                     2
#              74 STORE_FAST               2 (result)
# 
# 110          76 LOAD_FAST                1 (validator)
#              78 LOAD_ATTR                7 (NULL|self + validate)
#              98 LOAD_FAST                2 (result)
#             100 CALL                     1
#             108 STORE_FAST               3 (validation)
# 
# 111         110 LOAD_FAST                3 (validation)
#             112 LOAD_ATTR                8 (valid)
#             132 STORE_FAST               4 (@py_assert1)
#             134 LOAD_CONST               2 (True)
#             136 STORE_FAST               5 (@py_assert4)
#             138 LOAD_FAST                4 (@py_assert1)
#             140 LOAD_FAST                5 (@py_assert4)
#             142 IS_OP                    0
#             144 STORE_FAST               6 (@py_assert3)
#             146 LOAD_FAST                6 (@py_assert3)
#             148 POP_JUMP_IF_TRUE       173 (to 496)
#             150 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             160 LOAD_ATTR               12 (_call_reprcompare)
#             180 LOAD_CONST               5 (('is',))
#             182 LOAD_FAST                6 (@py_assert3)
#             184 BUILD_TUPLE              1
#             186 LOAD_CONST               6 (('%(py2)s\n{%(py2)s = %(py0)s.valid\n} is %(py5)s',))
#             188 LOAD_FAST                4 (@py_assert1)
#             190 LOAD_FAST                5 (@py_assert4)
#             192 BUILD_TUPLE              2
#             194 CALL                     4
#             202 LOAD_CONST               7 ('validation')
#             204 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             214 LOAD_ATTR               16 (locals)
#             234 CALL                     0
#             242 CONTAINS_OP              0
#             244 POP_JUMP_IF_TRUE        21 (to 288)
#             246 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             256 LOAD_ATTR               18 (_should_repr_global_name)
#             276 LOAD_FAST                3 (validation)
#             278 CALL                     1
#             286 POP_JUMP_IF_FALSE       21 (to 330)
#         >>  288 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             298 LOAD_ATTR               20 (_saferepr)
#             318 LOAD_FAST                3 (validation)
#             320 CALL                     1
#             328 JUMP_FORWARD             1 (to 332)
#         >>  330 LOAD_CONST               7 ('validation')
#         >>  332 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             342 LOAD_ATTR               20 (_saferepr)
#             362 LOAD_FAST                4 (@py_assert1)
#             364 CALL                     1
#             372 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             382 LOAD_ATTR               20 (_saferepr)
#             402 LOAD_FAST                5 (@py_assert4)
#             404 CALL                     1
#             412 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#             414 BUILD_CONST_KEY_MAP      3
#             416 BINARY_OP                6 (%)
#             420 STORE_FAST               7 (@py_format6)
#             422 LOAD_CONST               9 ('assert %(py7)s')
#             424 LOAD_CONST              10 ('py7')
#             426 LOAD_FAST                7 (@py_format6)
#             428 BUILD_MAP                1
#             430 BINARY_OP                6 (%)
#             434 STORE_FAST               8 (@py_format8)
#             436 LOAD_GLOBAL             23 (NULL + AssertionError)
#             446 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             456 LOAD_ATTR               24 (_format_explanation)
#             476 LOAD_FAST                8 (@py_format8)
#             478 CALL                     1
#             486 CALL                     1
#             494 RAISE_VARARGS            1
#         >>  496 LOAD_CONST               0 (None)
#             498 COPY                     1
#             500 STORE_FAST               4 (@py_assert1)
#             502 COPY                     1
#             504 STORE_FAST               6 (@py_assert3)
#             506 STORE_FAST               5 (@py_assert4)
#             508 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_failure_path_with_error at 0x3aefd020, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 113>:
# 113           0 RESUME                   0
# 
# 114           2 LOAD_GLOBAL              1 (NULL + SkillOutputValidator)
#              12 CALL                     0
#              20 STORE_FAST               1 (validator)
# 
# 115          22 LOAD_GLOBAL              3 (NULL + SkillResult)
#              32 LOAD_ATTR                4 (failure)
#              52 LOAD_CONST               1 ('test')
#              54 LOAD_CONST               2 ('error message')
#              56 KW_NAMES                 3 (('skill_name', 'error'))
#              58 CALL                     2
#              66 STORE_FAST               2 (result)
# 
# 116          68 LOAD_FAST                1 (validator)
#              70 LOAD_ATTR                7 (NULL|self + validate_failure_path)
#              90 LOAD_FAST                2 (result)
#              92 CALL                     1
#             100 STORE_FAST               3 (validation)
# 
# 117         102 LOAD_FAST                3 (validation)
#             104 LOAD_ATTR                8 (valid)
#             124 STORE_FAST               4 (@py_assert1)
#             126 LOAD_CONST               4 (True)
#             128 STORE_FAST               5 (@py_assert4)
#             130 LOAD_FAST                4 (@py_assert1)
#             132 LOAD_FAST                5 (@py_assert4)
#             134 IS_OP                    0
#             136 STORE_FAST               6 (@py_assert3)
#             138 LOAD_FAST                6 (@py_assert3)
#             140 POP_JUMP_IF_TRUE       173 (to 488)
#             142 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             152 LOAD_ATTR               12 (_call_reprcompare)
#             172 LOAD_CONST               5 (('is',))
#             174 LOAD_FAST                6 (@py_assert3)
#             176 BUILD_TUPLE              1
#             178 LOAD_CONST               6 (('%(py2)s\n{%(py2)s = %(py0)s.valid\n} is %(py5)s',))
#             180 LOAD_FAST                4 (@py_assert1)
#             182 LOAD_FAST                5 (@py_assert4)
#             184 BUILD_TUPLE              2
#             186 CALL                     4
#             194 LOAD_CONST               7 ('validation')
#             196 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             206 LOAD_ATTR               16 (locals)
#             226 CALL                     0
#             234 CONTAINS_OP              0
#             236 POP_JUMP_IF_TRUE        21 (to 280)
#             238 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             248 LOAD_ATTR               18 (_should_repr_global_name)
#             268 LOAD_FAST                3 (validation)
#             270 CALL                     1
#             278 POP_JUMP_IF_FALSE       21 (to 322)
#         >>  280 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             290 LOAD_ATTR               20 (_saferepr)
#             310 LOAD_FAST                3 (validation)
#             312 CALL                     1
#             320 JUMP_FORWARD             1 (to 324)
#         >>  322 LOAD_CONST               7 ('validation')
#         >>  324 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             334 LOAD_ATTR               20 (_saferepr)
#             354 LOAD_FAST                4 (@py_assert1)
#             356 CALL                     1
#             364 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             374 LOAD_ATTR               20 (_saferepr)
#             394 LOAD_FAST                5 (@py_assert4)
#             396 CALL                     1
#             404 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#             406 BUILD_CONST_KEY_MAP      3
#             408 BINARY_OP                6 (%)
#             412 STORE_FAST               7 (@py_format6)
#             414 LOAD_CONST               9 ('assert %(py7)s')
#             416 LOAD_CONST              10 ('py7')
#             418 LOAD_FAST                7 (@py_format6)
#             420 BUILD_MAP                1
#             422 BINARY_OP                6 (%)
#             426 STORE_FAST               8 (@py_format8)
#             428 LOAD_GLOBAL             23 (NULL + AssertionError)
#             438 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             448 LOAD_ATTR               24 (_format_explanation)
#             468 LOAD_FAST                8 (@py_format8)
#             470 CALL                     1
#             478 CALL                     1
#             486 RAISE_VARARGS            1
#         >>  488 LOAD_CONST               0 (None)
#             490 COPY                     1
#             492 STORE_FAST               4 (@py_assert1)
#             494 COPY                     1
#             496 STORE_FAST               6 (@py_assert3)
#             498 STORE_FAST               5 (@py_assert4)
#             500 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_failure_path_missing_error at 0x3aefbf80, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 119>:
# 119           0 RESUME                   0
# 
# 120           2 LOAD_GLOBAL              1 (NULL + SkillOutputValidator)
#              12 CALL                     0
#              20 STORE_FAST               1 (validator)
# 
# 121          22 LOAD_GLOBAL              3 (NULL + SkillResult)
# 
# 122          32 LOAD_CONST               1 ('test')
# 
# 123          34 LOAD_GLOBAL              4 (SkillStatus)
#              44 LOAD_ATTR                6 (FAILED)
# 
# 124          64 BUILD_MAP                0
# 
# 125          66 LOAD_CONST               0 (None)
# 
# 121          68 KW_NAMES                 2 (('skill_name', 'status', 'data', 'error'))
#              70 CALL                     4
#              78 STORE_FAST               2 (result)
# 
# 127          80 LOAD_FAST                1 (validator)
#              82 LOAD_ATTR                9 (NULL|self + validate_failure_path)
#             102 LOAD_FAST                2 (result)
#             104 CALL                     1
#             112 STORE_FAST               3 (validation)
# 
# 128         114 LOAD_FAST                3 (validation)
#             116 LOAD_ATTR               10 (valid)
#             136 STORE_FAST               4 (@py_assert1)
#             138 LOAD_CONST               3 (False)
#             140 STORE_FAST               5 (@py_assert4)
#             142 LOAD_FAST                4 (@py_assert1)
#             144 LOAD_FAST                5 (@py_assert4)
#             146 IS_OP                    0
#             148 STORE_FAST               6 (@py_assert3)
#             150 LOAD_FAST                6 (@py_assert3)
#             152 POP_JUMP_IF_TRUE       173 (to 500)
#             154 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             164 LOAD_ATTR               14 (_call_reprcompare)
#             184 LOAD_CONST               4 (('is',))
#             186 LOAD_FAST                6 (@py_assert3)
#             188 BUILD_TUPLE              1
#             190 LOAD_CONST               5 (('%(py2)s\n{%(py2)s = %(py0)s.valid\n} is %(py5)s',))
#             192 LOAD_FAST                4 (@py_assert1)
#             194 LOAD_FAST                5 (@py_assert4)
#             196 BUILD_TUPLE              2
#             198 CALL                     4
#             206 LOAD_CONST               6 ('validation')
#             208 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             218 LOAD_ATTR               18 (locals)
#             238 CALL                     0
#             246 CONTAINS_OP              0
#             248 POP_JUMP_IF_TRUE        21 (to 292)
#             250 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             260 LOAD_ATTR               20 (_should_repr_global_name)
#             280 LOAD_FAST                3 (validation)
#             282 CALL                     1
#             290 POP_JUMP_IF_FALSE       21 (to 334)
#         >>  292 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             302 LOAD_ATTR               22 (_saferepr)
#             322 LOAD_FAST                3 (validation)
#             324 CALL                     1
#             332 JUMP_FORWARD             1 (to 336)
#         >>  334 LOAD_CONST               6 ('validation')
#         >>  336 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             346 LOAD_ATTR               22 (_saferepr)
#             366 LOAD_FAST                4 (@py_assert1)
#             368 CALL                     1
#             376 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             386 LOAD_ATTR               22 (_saferepr)
#             406 LOAD_FAST                5 (@py_assert4)
#             408 CALL                     1
#             416 LOAD_CONST               7 (('py0', 'py2', 'py5'))
#             418 BUILD_CONST_KEY_MAP      3
#             420 BINARY_OP                6 (%)
#             424 STORE_FAST               7 (@py_format6)
#             426 LOAD_CONST               8 ('assert %(py7)s')
#             428 LOAD_CONST               9 ('py7')
#             430 LOAD_FAST                7 (@py_format6)
#             432 BUILD_MAP                1
#             434 BINARY_OP                6 (%)
#             438 STORE_FAST               8 (@py_format8)
#             440 LOAD_GLOBAL             25 (NULL + AssertionError)
#             450 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             460 LOAD_ATTR               26 (_format_explanation)
#             480 LOAD_FAST                8 (@py_format8)
#             482 CALL                     1
#             490 CALL                     1
#             498 RAISE_VARARGS            1
#         >>  500 LOAD_CONST               0 (None)
#             502 COPY                     1
#             504 STORE_FAST               4 (@py_assert1)
#             506 COPY                     1
#             508 STORE_FAST               6 (@py_assert3)
#             510 STORE_FAST               5 (@py_assert4)
#             512 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_failure_path_inconsistent_status at 0x3af3ed40, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 130>:
# 130           0 RESUME                   0
# 
# 131           2 LOAD_GLOBAL              1 (NULL + SkillOutputValidator)
#              12 CALL                     0
#              20 STORE_FAST               1 (validator)
# 
# 132          22 LOAD_GLOBAL              3 (NULL + SkillResult)
# 
# 133          32 LOAD_CONST               1 ('test')
# 
# 134          34 LOAD_GLOBAL              4 (SkillStatus)
#              44 LOAD_ATTR                6 (SUCCESS)
# 
# 135          64 BUILD_MAP                0
# 
# 136          66 LOAD_CONST               2 ('some error')
# 
# 132          68 KW_NAMES                 3 (('skill_name', 'status', 'data', 'error'))
#              70 CALL                     4
#              78 STORE_FAST               2 (result)
# 
# 138          80 LOAD_FAST                1 (validator)
#              82 LOAD_ATTR                9 (NULL|self + validate_failure_path)
#             102 LOAD_FAST                2 (result)
#             104 CALL                     1
#             112 STORE_FAST               3 (validation)
# 
# 139         114 LOAD_FAST                3 (validation)
#             116 LOAD_ATTR               10 (warnings)
#             136 STORE_FAST               4 (@py_assert2)
#             138 LOAD_GLOBAL             13 (NULL + len)
#             148 LOAD_FAST                4 (@py_assert2)
#             150 CALL                     1
#             158 STORE_FAST               5 (@py_assert4)
#             160 LOAD_CONST               4 (1)
#             162 STORE_FAST               6 (@py_assert7)
#             164 LOAD_FAST                5 (@py_assert4)
#             166 LOAD_FAST                6 (@py_assert7)
#             168 COMPARE_OP              92 (>=)
#             172 STORE_FAST               7 (@py_assert6)
#             174 LOAD_FAST                7 (@py_assert6)
#             176 EXTENDED_ARG             1
#             178 POP_JUMP_IF_TRUE       266 (to 712)
#             180 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             190 LOAD_ATTR               16 (_call_reprcompare)
#             210 LOAD_CONST               5 (('>=',))
#             212 LOAD_FAST                7 (@py_assert6)
#             214 BUILD_TUPLE              1
#             216 LOAD_CONST               6 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.warnings\n})\n} >= %(py8)s',))
#             218 LOAD_FAST                5 (@py_assert4)
#             220 LOAD_FAST                6 (@py_assert7)
#             222 BUILD_TUPLE              2
#             224 CALL                     4
#             232 LOAD_CONST               7 ('len')
#             234 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             244 LOAD_ATTR               20 (locals)
#             264 CALL                     0
#             272 CONTAINS_OP              0
#             274 POP_JUMP_IF_TRUE        25 (to 326)
#             276 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             286 LOAD_ATTR               22 (_should_repr_global_name)
#             306 LOAD_GLOBAL             12 (len)
#             316 CALL                     1
#             324 POP_JUMP_IF_FALSE       25 (to 376)
#         >>  326 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             336 LOAD_ATTR               24 (_saferepr)
#             356 LOAD_GLOBAL             12 (len)
#             366 CALL                     1
#             374 JUMP_FORWARD             1 (to 378)
#         >>  376 LOAD_CONST               7 ('len')
#         >>  378 LOAD_CONST               8 ('validation')
#             380 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             390 LOAD_ATTR               20 (locals)
#             410 CALL                     0
#             418 CONTAINS_OP              0
#             420 POP_JUMP_IF_TRUE        21 (to 464)
#             422 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             432 LOAD_ATTR               22 (_should_repr_global_name)
#             452 LOAD_FAST                3 (validation)
#             454 CALL                     1
#             462 POP_JUMP_IF_FALSE       21 (to 506)
#         >>  464 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             474 LOAD_ATTR               24 (_saferepr)
#             494 LOAD_FAST                3 (validation)
#             496 CALL                     1
#             504 JUMP_FORWARD             1 (to 508)
#         >>  506 LOAD_CONST               8 ('validation')
#         >>  508 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             518 LOAD_ATTR               24 (_saferepr)
#             538 LOAD_FAST                4 (@py_assert2)
#             540 CALL                     1
#             548 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             558 LOAD_ATTR               24 (_saferepr)
#             578 LOAD_FAST                5 (@py_assert4)
#             580 CALL                     1
#             588 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             598 LOAD_ATTR               24 (_saferepr)
#             618 LOAD_FAST                6 (@py_assert7)
#             620 CALL                     1
#             628 LOAD_CONST               9 (('py0', 'py1', 'py3', 'py5', 'py8'))
#             630 BUILD_CONST_KEY_MAP      5
#             632 BINARY_OP                6 (%)
#             636 STORE_FAST               8 (@py_format9)
#             638 LOAD_CONST              10 ('assert %(py10)s')
#             640 LOAD_CONST              11 ('py10')
#             642 LOAD_FAST                8 (@py_format9)
#             644 BUILD_MAP                1
#             646 BINARY_OP                6 (%)
#             650 STORE_FAST               9 (@py_format11)
#             652 LOAD_GLOBAL             27 (NULL + AssertionError)
#             662 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             672 LOAD_ATTR               28 (_format_explanation)
#             692 LOAD_FAST                9 (@py_format11)
#             694 CALL                     1
#             702 CALL                     1
#             710 RAISE_VARARGS            1
#         >>  712 LOAD_CONST               0 (None)
#             714 COPY                     1
#             716 STORE_FAST               4 (@py_assert2)
#             718 COPY                     1
#             720 STORE_FAST               5 (@py_assert4)
#             722 COPY                     1
#             724 STORE_FAST               7 (@py_assert6)
#             726 STORE_FAST               6 (@py_assert7)
#             728 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_field_naming_snake_case at 0x3afa7230, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 141>:
# 141           0 RESUME                   0
# 
# 142           2 LOAD_GLOBAL              1 (NULL + SkillOutputValidator)
#              12 CALL                     0
#              20 STORE_FAST               1 (validator)
# 
# 143          22 LOAD_CONST               1 ('snake_case_field')
#              24 LOAD_CONST               2 (42)
#              26 BUILD_MAP                1
#              28 STORE_FAST               2 (data)
# 
# 144          30 LOAD_FAST                1 (validator)
#              32 LOAD_ATTR                3 (NULL|self + validate_field_naming)
#              52 LOAD_FAST                2 (data)
#              54 CALL                     1
#              62 STORE_FAST               3 (validation)
# 
# 145          64 LOAD_FAST                3 (validation)
#              66 LOAD_ATTR                4 (valid)
#              86 STORE_FAST               4 (@py_assert1)
#              88 LOAD_CONST               3 (True)
#              90 STORE_FAST               5 (@py_assert4)
#              92 LOAD_FAST                4 (@py_assert1)
#              94 LOAD_FAST                5 (@py_assert4)
#              96 IS_OP                    0
#              98 STORE_FAST               6 (@py_assert3)
#             100 LOAD_FAST                6 (@py_assert3)
#             102 POP_JUMP_IF_TRUE       173 (to 450)
#             104 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             114 LOAD_ATTR                8 (_call_reprcompare)
#             134 LOAD_CONST               4 (('is',))
#             136 LOAD_FAST                6 (@py_assert3)
#             138 BUILD_TUPLE              1
#             140 LOAD_CONST               5 (('%(py2)s\n{%(py2)s = %(py0)s.valid\n} is %(py5)s',))
#             142 LOAD_FAST                4 (@py_assert1)
#             144 LOAD_FAST                5 (@py_assert4)
#             146 BUILD_TUPLE              2
#             148 CALL                     4
#             156 LOAD_CONST               6 ('validation')
#             158 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             168 LOAD_ATTR               12 (locals)
#             188 CALL                     0
#             196 CONTAINS_OP              0
#             198 POP_JUMP_IF_TRUE        21 (to 242)
#             200 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             210 LOAD_ATTR               14 (_should_repr_global_name)
#             230 LOAD_FAST                3 (validation)
#             232 CALL                     1
#             240 POP_JUMP_IF_FALSE       21 (to 284)
#         >>  242 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             252 LOAD_ATTR               16 (_saferepr)
#             272 LOAD_FAST                3 (validation)
#             274 CALL                     1
#             282 JUMP_FORWARD             1 (to 286)
#         >>  284 LOAD_CONST               6 ('validation')
#         >>  286 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             296 LOAD_ATTR               16 (_saferepr)
#             316 LOAD_FAST                4 (@py_assert1)
#             318 CALL                     1
#             326 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             336 LOAD_ATTR               16 (_saferepr)
#             356 LOAD_FAST                5 (@py_assert4)
#             358 CALL                     1
#             366 LOAD_CONST               7 (('py0', 'py2', 'py5'))
#             368 BUILD_CONST_KEY_MAP      3
#             370 BINARY_OP                6 (%)
#             374 STORE_FAST               7 (@py_format6)
#             376 LOAD_CONST               8 ('assert %(py7)s')
#             378 LOAD_CONST               9 ('py7')
#             380 LOAD_FAST                7 (@py_format6)
#             382 BUILD_MAP                1
#             384 BINARY_OP                6 (%)
#             388 STORE_FAST               8 (@py_format8)
#             390 LOAD_GLOBAL             19 (NULL + AssertionError)
#             400 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             410 LOAD_ATTR               20 (_format_explanation)
#             430 LOAD_FAST                8 (@py_format8)
#             432 CALL                     1
#             440 CALL                     1
#             448 RAISE_VARARGS            1
#         >>  450 LOAD_CONST               0 (None)
#             452 COPY                     1
#             454 STORE_FAST               4 (@py_assert1)
#             456 COPY                     1
#             458 STORE_FAST               6 (@py_assert3)
#             460 STORE_FAST               5 (@py_assert4)
#             462 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_field_naming_camel_case_warning at 0x3afa13e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 147>:
# 147           0 RESUME                   0
# 
# 148           2 LOAD_GLOBAL              1 (NULL + SkillOutputValidator)
#              12 CALL                     0
#              20 STORE_FAST               1 (validator)
# 
# 149          22 LOAD_CONST               1 ('camelCaseField')
#              24 LOAD_CONST               2 (42)
#              26 BUILD_MAP                1
#              28 STORE_FAST               2 (data)
# 
# 150          30 LOAD_FAST                1 (validator)
#              32 LOAD_ATTR                3 (NULL|self + validate_field_naming)
#              52 LOAD_FAST                2 (data)
#              54 CALL                     1
#              62 STORE_FAST               3 (validation)
# 
# 151          64 LOAD_FAST                3 (validation)
#              66 LOAD_ATTR                4 (warnings)
#              86 STORE_FAST               4 (@py_assert2)
#              88 LOAD_GLOBAL              7 (NULL + len)
#              98 LOAD_FAST                4 (@py_assert2)
#             100 CALL                     1
#             108 STORE_FAST               5 (@py_assert4)
#             110 LOAD_CONST               3 (1)
#             112 STORE_FAST               6 (@py_assert7)
#             114 LOAD_FAST                5 (@py_assert4)
#             116 LOAD_FAST                6 (@py_assert7)
#             118 COMPARE_OP              92 (>=)
#             122 STORE_FAST               7 (@py_assert6)
#             124 LOAD_FAST                7 (@py_assert6)
#             126 EXTENDED_ARG             1
#             128 POP_JUMP_IF_TRUE       266 (to 662)
#             130 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             140 LOAD_ATTR               10 (_call_reprcompare)
#             160 LOAD_CONST               4 (('>=',))
#             162 LOAD_FAST                7 (@py_assert6)
#             164 BUILD_TUPLE              1
#             166 LOAD_CONST               5 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.warnings\n})\n} >= %(py8)s',))
#             168 LOAD_FAST                5 (@py_assert4)
#             170 LOAD_FAST                6 (@py_assert7)
#             172 BUILD_TUPLE              2
#             174 CALL                     4
#             182 LOAD_CONST               6 ('len')
#             184 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             194 LOAD_ATTR               14 (locals)
#             214 CALL                     0
#             222 CONTAINS_OP              0
#             224 POP_JUMP_IF_TRUE        25 (to 276)
#             226 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             236 LOAD_ATTR               16 (_should_repr_global_name)
#             256 LOAD_GLOBAL              6 (len)
#             266 CALL                     1
#             274 POP_JUMP_IF_FALSE       25 (to 326)
#         >>  276 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             286 LOAD_ATTR               18 (_saferepr)
#             306 LOAD_GLOBAL              6 (len)
#             316 CALL                     1
#             324 JUMP_FORWARD             1 (to 328)
#         >>  326 LOAD_CONST               6 ('len')
#         >>  328 LOAD_CONST               7 ('validation')
#             330 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             340 LOAD_ATTR               14 (locals)
#             360 CALL                     0
#             368 CONTAINS_OP              0
#             370 POP_JUMP_IF_TRUE        21 (to 414)
#             372 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             382 LOAD_ATTR               16 (_should_repr_global_name)
#             402 LOAD_FAST                3 (validation)
#             404 CALL                     1
#             412 POP_JUMP_IF_FALSE       21 (to 456)
#         >>  414 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             424 LOAD_ATTR               18 (_saferepr)
#             444 LOAD_FAST                3 (validation)
#             446 CALL                     1
#             454 JUMP_FORWARD             1 (to 458)
#         >>  456 LOAD_CONST               7 ('validation')
#         >>  458 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             468 LOAD_ATTR               18 (_saferepr)
#             488 LOAD_FAST                4 (@py_assert2)
#             490 CALL                     1
#             498 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             508 LOAD_ATTR               18 (_saferepr)
#             528 LOAD_FAST                5 (@py_assert4)
#             530 CALL                     1
#             538 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             548 LOAD_ATTR               18 (_saferepr)
#             568 LOAD_FAST                6 (@py_assert7)
#             570 CALL                     1
#             578 LOAD_CONST               8 (('py0', 'py1', 'py3', 'py5', 'py8'))
#             580 BUILD_CONST_KEY_MAP      5
#             582 BINARY_OP                6 (%)
#             586 STORE_FAST               8 (@py_format9)
#             588 LOAD_CONST               9 ('assert %(py10)s')
#             590 LOAD_CONST              10 ('py10')
#             592 LOAD_FAST                8 (@py_format9)
#             594 BUILD_MAP                1
#             596 BINARY_OP                6 (%)
#             600 STORE_FAST               9 (@py_format11)
#             602 LOAD_GLOBAL             21 (NULL + AssertionError)
#             612 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             622 LOAD_ATTR               22 (_format_explanation)
#             642 LOAD_FAST                9 (@py_format11)
#             644 CALL                     1
#             652 CALL                     1
#             660 RAISE_VARARGS            1
#         >>  662 LOAD_CONST               0 (None)
#             664 COPY                     1
#             666 STORE_FAST               4 (@py_assert2)
#             668 COPY                     1
#             670 STORE_FAST               5 (@py_assert4)
#             672 COPY                     1
#             674 STORE_FAST               7 (@py_assert6)
#             676 STORE_FAST               6 (@py_assert7)
#             678 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestFieldNormalization at 0x73cd945ff210, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 154>:
# 154           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestFieldNormalization')
#               8 STORE_NAME               2 (__qualname__)
# 
# 155          10 LOAD_CONST               1 (<code object test_normalize_camel_case at 0x3af9e7f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 155>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_normalize_camel_case)
# 
# 161          16 LOAD_CONST               2 (<code object test_normalize_known_mappings at 0x3aed2b60, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 161>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_normalize_known_mappings)
# 
# 167          22 LOAD_CONST               3 (<code object test_normalize_data_nested at 0x3aed3df0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 167>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_normalize_data_nested)
#              28 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_normalize_camel_case at 0x3af9e7f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 155>:
# 155           0 RESUME                   0
# 
# 156           2 LOAD_CONST               1 (0)
#               4 LOAD_CONST               2 (('normalize_field_name',))
#               6 IMPORT_NAME              0 (cloudpss_skills_v2.core.skill_result)
#               8 IMPORT_FROM              1 (normalize_field_name)
#              10 STORE_FAST               1 (normalize_field_name)
#              12 POP_TOP
# 
# 158          14 LOAD_CONST               3 ('camelCase')
#              16 STORE_FAST               2 (@py_assert1)
#              18 PUSH_NULL
#              20 LOAD_FAST                1 (normalize_field_name)
#              22 LOAD_FAST                2 (@py_assert1)
#              24 CALL                     1
#              32 STORE_FAST               3 (@py_assert3)
#              34 LOAD_CONST               4 ('camel_case')
#              36 STORE_FAST               4 (@py_assert6)
#              38 LOAD_FAST                3 (@py_assert3)
#              40 LOAD_FAST                4 (@py_assert6)
#              42 COMPARE_OP              40 (==)
#              46 STORE_FAST               5 (@py_assert5)
#              48 LOAD_FAST                5 (@py_assert5)
#              50 POP_JUMP_IF_TRUE       193 (to 438)
#              52 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              62 LOAD_ATTR                6 (_call_reprcompare)
#              82 LOAD_CONST               5 (('==',))
#              84 LOAD_FAST                5 (@py_assert5)
#              86 BUILD_TUPLE              1
#              88 LOAD_CONST               6 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',))
#              90 LOAD_FAST                3 (@py_assert3)
#              92 LOAD_FAST                4 (@py_assert6)
#              94 BUILD_TUPLE              2
#              96 CALL                     4
#             104 LOAD_CONST               7 ('normalize_field_name')
#             106 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             116 LOAD_ATTR               10 (locals)
#             136 CALL                     0
#             144 CONTAINS_OP              0
#             146 POP_JUMP_IF_TRUE        21 (to 190)
#             148 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             158 LOAD_ATTR               12 (_should_repr_global_name)
#             178 LOAD_FAST                1 (normalize_field_name)
#             180 CALL                     1
#             188 POP_JUMP_IF_FALSE       21 (to 232)
#         >>  190 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             200 LOAD_ATTR               14 (_saferepr)
#             220 LOAD_FAST                1 (normalize_field_name)
#             222 CALL                     1
#             230 JUMP_FORWARD             1 (to 234)
#         >>  232 LOAD_CONST               7 ('normalize_field_name')
#         >>  234 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             244 LOAD_ATTR               14 (_saferepr)
#             264 LOAD_FAST                2 (@py_assert1)
#             266 CALL                     1
#             274 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             284 LOAD_ATTR               14 (_saferepr)
#             304 LOAD_FAST                3 (@py_assert3)
#             306 CALL                     1
#             314 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             324 LOAD_ATTR               14 (_saferepr)
#             344 LOAD_FAST                4 (@py_assert6)
#             346 CALL                     1
#             354 LOAD_CONST               8 (('py0', 'py2', 'py4', 'py7'))
#             356 BUILD_CONST_KEY_MAP      4
#             358 BINARY_OP                6 (%)
#             362 STORE_FAST               6 (@py_format8)
#             364 LOAD_CONST               9 ('assert %(py9)s')
#             366 LOAD_CONST              10 ('py9')
#             368 LOAD_FAST                6 (@py_format8)
#             370 BUILD_MAP                1
#             372 BINARY_OP                6 (%)
#             376 STORE_FAST               7 (@py_format10)
#             378 LOAD_GLOBAL             17 (NULL + AssertionError)
#             388 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             398 LOAD_ATTR               18 (_format_explanation)
#             418 LOAD_FAST                7 (@py_format10)
#             420 CALL                     1
#             428 CALL                     1
#             436 RAISE_VARARGS            1
#         >>  438 LOAD_CONST               0 (None)
#             440 COPY                     1
#             442 STORE_FAST               2 (@py_assert1)
#             444 COPY                     1
#             446 STORE_FAST               3 (@py_assert3)
#             448 COPY                     1
#             450 STORE_FAST               5 (@py_assert5)
#             452 STORE_FAST               4 (@py_assert6)
# 
# 159         454 LOAD_CONST              11 ('myFieldName')
#             456 STORE_FAST               2 (@py_assert1)
#             458 PUSH_NULL
#             460 LOAD_FAST                1 (normalize_field_name)
#             462 LOAD_FAST                2 (@py_assert1)
#             464 CALL                     1
#             472 STORE_FAST               3 (@py_assert3)
#             474 LOAD_CONST              12 ('my_field_name')
#             476 STORE_FAST               4 (@py_assert6)
#             478 LOAD_FAST                3 (@py_assert3)
#             480 LOAD_FAST                4 (@py_assert6)
#             482 COMPARE_OP              40 (==)
#             486 STORE_FAST               5 (@py_assert5)
#             488 LOAD_FAST                5 (@py_assert5)
#             490 POP_JUMP_IF_TRUE       193 (to 878)
#             492 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             502 LOAD_ATTR                6 (_call_reprcompare)
#             522 LOAD_CONST               5 (('==',))
#             524 LOAD_FAST                5 (@py_assert5)
#             526 BUILD_TUPLE              1
#             528 LOAD_CONST               6 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',))
#             530 LOAD_FAST                3 (@py_assert3)
#             532 LOAD_FAST                4 (@py_assert6)
#             534 BUILD_TUPLE              2
#             536 CALL                     4
#             544 LOAD_CONST               7 ('normalize_field_name')
#             546 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             556 LOAD_ATTR               10 (locals)
#             576 CALL                     0
#             584 CONTAINS_OP              0
#             586 POP_JUMP_IF_TRUE        21 (to 630)
#             588 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             598 LOAD_ATTR               12 (_should_repr_global_name)
#             618 LOAD_FAST                1 (normalize_field_name)
#             620 CALL                     1
#             628 POP_JUMP_IF_FALSE       21 (to 672)
#         >>  630 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             640 LOAD_ATTR               14 (_saferepr)
#             660 LOAD_FAST                1 (normalize_field_name)
#             662 CALL                     1
#             670 JUMP_FORWARD             1 (to 674)
#         >>  672 LOAD_CONST               7 ('normalize_field_name')
#         >>  674 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             684 LOAD_ATTR               14 (_saferepr)
#             704 LOAD_FAST                2 (@py_assert1)
#             706 CALL                     1
#             714 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             724 LOAD_ATTR               14 (_saferepr)
#             744 LOAD_FAST                3 (@py_assert3)
#             746 CALL                     1
#             754 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             764 LOAD_ATTR               14 (_saferepr)
#             784 LOAD_FAST                4 (@py_assert6)
#             786 CALL                     1
#             794 LOAD_CONST               8 (('py0', 'py2', 'py4', 'py7'))
#             796 BUILD_CONST_KEY_MAP      4
#             798 BINARY_OP                6 (%)
#             802 STORE_FAST               6 (@py_format8)
#             804 LOAD_CONST               9 ('assert %(py9)s')
#             806 LOAD_CONST              10 ('py9')
#             808 LOAD_FAST                6 (@py_format8)
#             810 BUILD_MAP                1
#             812 BINARY_OP                6 (%)
#             816 STORE_FAST               7 (@py_format10)
#             818 LOAD_GLOBAL             17 (NULL + AssertionError)
#             828 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             838 LOAD_ATTR               18 (_format_explanation)
#             858 LOAD_FAST                7 (@py_format10)
#             860 CALL                     1
#             868 CALL                     1
#             876 RAISE_VARARGS            1
#         >>  878 LOAD_CONST               0 (None)
#             880 COPY                     1
#             882 STORE_FAST               2 (@py_assert1)
#             884 COPY                     1
#             886 STORE_FAST               3 (@py_assert3)
#             888 COPY                     1
#             890 STORE_FAST               5 (@py_assert5)
#             892 STORE_FAST               4 (@py_assert6)
#             894 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_normalize_known_mappings at 0x3aed2b60, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 161>:
# 161           0 RESUME                   0
# 
# 162           2 LOAD_CONST               1 (0)
#               4 LOAD_CONST               2 (('normalize_field_name',))
#               6 IMPORT_NAME              0 (cloudpss_skills_v2.core.skill_result)
#               8 IMPORT_FROM              1 (normalize_field_name)
#              10 STORE_FAST               1 (normalize_field_name)
#              12 POP_TOP
# 
# 164          14 LOAD_CONST               3 ('busCount')
#              16 STORE_FAST               2 (@py_assert1)
#              18 PUSH_NULL
#              20 LOAD_FAST                1 (normalize_field_name)
#              22 LOAD_FAST                2 (@py_assert1)
#              24 CALL                     1
#              32 STORE_FAST               3 (@py_assert3)
#              34 LOAD_CONST               4 ('bus_count')
#              36 STORE_FAST               4 (@py_assert6)
#              38 LOAD_FAST                3 (@py_assert3)
#              40 LOAD_FAST                4 (@py_assert6)
#              42 COMPARE_OP              40 (==)
#              46 STORE_FAST               5 (@py_assert5)
#              48 LOAD_FAST                5 (@py_assert5)
#              50 POP_JUMP_IF_TRUE       193 (to 438)
#              52 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              62 LOAD_ATTR                6 (_call_reprcompare)
#              82 LOAD_CONST               5 (('==',))
#              84 LOAD_FAST                5 (@py_assert5)
#              86 BUILD_TUPLE              1
#              88 LOAD_CONST               6 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',))
#              90 LOAD_FAST                3 (@py_assert3)
#              92 LOAD_FAST                4 (@py_assert6)
#              94 BUILD_TUPLE              2
#              96 CALL                     4
#             104 LOAD_CONST               7 ('normalize_field_name')
#             106 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             116 LOAD_ATTR               10 (locals)
#             136 CALL                     0
#             144 CONTAINS_OP              0
#             146 POP_JUMP_IF_TRUE        21 (to 190)
#             148 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             158 LOAD_ATTR               12 (_should_repr_global_name)
#             178 LOAD_FAST                1 (normalize_field_name)
#             180 CALL                     1
#             188 POP_JUMP_IF_FALSE       21 (to 232)
#         >>  190 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             200 LOAD_ATTR               14 (_saferepr)
#             220 LOAD_FAST                1 (normalize_field_name)
#             222 CALL                     1
#             230 JUMP_FORWARD             1 (to 234)
#         >>  232 LOAD_CONST               7 ('normalize_field_name')
#         >>  234 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             244 LOAD_ATTR               14 (_saferepr)
#             264 LOAD_FAST                2 (@py_assert1)
#             266 CALL                     1
#             274 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             284 LOAD_ATTR               14 (_saferepr)
#             304 LOAD_FAST                3 (@py_assert3)
#             306 CALL                     1
#             314 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             324 LOAD_ATTR               14 (_saferepr)
#             344 LOAD_FAST                4 (@py_assert6)
#             346 CALL                     1
#             354 LOAD_CONST               8 (('py0', 'py2', 'py4', 'py7'))
#             356 BUILD_CONST_KEY_MAP      4
#             358 BINARY_OP                6 (%)
#             362 STORE_FAST               6 (@py_format8)
#             364 LOAD_CONST               9 ('assert %(py9)s')
#             366 LOAD_CONST              10 ('py9')
#             368 LOAD_FAST                6 (@py_format8)
#             370 BUILD_MAP                1
#             372 BINARY_OP                6 (%)
#             376 STORE_FAST               7 (@py_format10)
#             378 LOAD_GLOBAL             17 (NULL + AssertionError)
#             388 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             398 LOAD_ATTR               18 (_format_explanation)
#             418 LOAD_FAST                7 (@py_format10)
#             420 CALL                     1
#             428 CALL                     1
#             436 RAISE_VARARGS            1
#         >>  438 LOAD_CONST               0 (None)
#             440 COPY                     1
#             442 STORE_FAST               2 (@py_assert1)
#             444 COPY                     1
#             446 STORE_FAST               3 (@py_assert3)
#             448 COPY                     1
#             450 STORE_FAST               5 (@py_assert5)
#             452 STORE_FAST               4 (@py_assert6)
# 
# 165         454 LOAD_CONST              11 ('totalLoss')
#             456 STORE_FAST               2 (@py_assert1)
#             458 PUSH_NULL
#             460 LOAD_FAST                1 (normalize_field_name)
#             462 LOAD_FAST                2 (@py_assert1)
#             464 CALL                     1
#             472 STORE_FAST               3 (@py_assert3)
#             474 LOAD_CONST              12 ('total_loss')
#             476 STORE_FAST               4 (@py_assert6)
#             478 LOAD_FAST                3 (@py_assert3)
#             480 LOAD_FAST                4 (@py_assert6)
#             482 COMPARE_OP              40 (==)
#             486 STORE_FAST               5 (@py_assert5)
#             488 LOAD_FAST                5 (@py_assert5)
#             490 POP_JUMP_IF_TRUE       193 (to 878)
#             492 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             502 LOAD_ATTR                6 (_call_reprcompare)
#             522 LOAD_CONST               5 (('==',))
#             524 LOAD_FAST                5 (@py_assert5)
#             526 BUILD_TUPLE              1
#             528 LOAD_CONST               6 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',))
#             530 LOAD_FAST                3 (@py_assert3)
#             532 LOAD_FAST                4 (@py_assert6)
#             534 BUILD_TUPLE              2
#             536 CALL                     4
#             544 LOAD_CONST               7 ('normalize_field_name')
#             546 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             556 LOAD_ATTR               10 (locals)
#             576 CALL                     0
#             584 CONTAINS_OP              0
#             586 POP_JUMP_IF_TRUE        21 (to 630)
#             588 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             598 LOAD_ATTR               12 (_should_repr_global_name)
#             618 LOAD_FAST                1 (normalize_field_name)
#             620 CALL                     1
#             628 POP_JUMP_IF_FALSE       21 (to 672)
#         >>  630 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             640 LOAD_ATTR               14 (_saferepr)
#             660 LOAD_FAST                1 (normalize_field_name)
#             662 CALL                     1
#             670 JUMP_FORWARD             1 (to 674)
#         >>  672 LOAD_CONST               7 ('normalize_field_name')
#         >>  674 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             684 LOAD_ATTR               14 (_saferepr)
#             704 LOAD_FAST                2 (@py_assert1)
#             706 CALL                     1
#             714 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             724 LOAD_ATTR               14 (_saferepr)
#             744 LOAD_FAST                3 (@py_assert3)
#             746 CALL                     1
#             754 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             764 LOAD_ATTR               14 (_saferepr)
#             784 LOAD_FAST                4 (@py_assert6)
#             786 CALL                     1
#             794 LOAD_CONST               8 (('py0', 'py2', 'py4', 'py7'))
#             796 BUILD_CONST_KEY_MAP      4
#             798 BINARY_OP                6 (%)
#             802 STORE_FAST               6 (@py_format8)
#             804 LOAD_CONST               9 ('assert %(py9)s')
#             806 LOAD_CONST              10 ('py9')
#             808 LOAD_FAST                6 (@py_format8)
#             810 BUILD_MAP                1
#             812 BINARY_OP                6 (%)
#             816 STORE_FAST               7 (@py_format10)
#             818 LOAD_GLOBAL             17 (NULL + AssertionError)
#             828 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             838 LOAD_ATTR               18 (_format_explanation)
#             858 LOAD_FAST                7 (@py_format10)
#             860 CALL                     1
#             868 CALL                     1
#             876 RAISE_VARARGS            1
#         >>  878 LOAD_CONST               0 (None)
#             880 COPY                     1
#             882 STORE_FAST               2 (@py_assert1)
#             884 COPY                     1
#             886 STORE_FAST               3 (@py_assert3)
#             888 COPY                     1
#             890 STORE_FAST               5 (@py_assert5)
#             892 STORE_FAST               4 (@py_assert6)
#             894 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_normalize_data_nested at 0x3aed3df0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 167>:
# 167           0 RESUME                   0
# 
# 168           2 LOAD_CONST               1 (0)
#               4 LOAD_CONST               2 (('normalize_data',))
#               6 IMPORT_NAME              0 (cloudpss_skills_v2.core.skill_result)
#               8 IMPORT_FROM              1 (normalize_data)
#              10 STORE_FAST               1 (normalize_data)
#              12 POP_TOP
# 
# 171          14 LOAD_CONST               3 (10)
# 
# 172          16 LOAD_CONST               4 ('totalLoss')
#              18 LOAD_CONST               5 (5.0)
#              20 BUILD_MAP                1
# 
# 170          22 LOAD_CONST               6 (('busCount', 'nested'))
#              24 BUILD_CONST_KEY_MAP      2
#              26 STORE_FAST               2 (data)
# 
# 174          28 PUSH_NULL
#              30 LOAD_FAST                1 (normalize_data)
#              32 LOAD_FAST                2 (data)
#              34 CALL                     1
#              42 STORE_FAST               3 (normalized)
# 
# 175          44 LOAD_CONST               7 ('bus_count')
#              46 STORE_FAST               4 (@py_assert0)
#              48 LOAD_FAST                4 (@py_assert0)
#              50 LOAD_FAST                3 (normalized)
#              52 CONTAINS_OP              0
#              54 STORE_FAST               5 (@py_assert2)
#              56 LOAD_FAST                5 (@py_assert2)
#              58 POP_JUMP_IF_TRUE       153 (to 366)
#              60 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              70 LOAD_ATTR                6 (_call_reprcompare)
#              90 LOAD_CONST               8 (('in',))
#              92 LOAD_FAST                5 (@py_assert2)
#              94 BUILD_TUPLE              1
#              96 LOAD_CONST               9 (('%(py1)s in %(py3)s',))
#              98 LOAD_FAST                4 (@py_assert0)
#             100 LOAD_FAST                3 (normalized)
#             102 BUILD_TUPLE              2
#             104 CALL                     4
#             112 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             122 LOAD_ATTR                8 (_saferepr)
#             142 LOAD_FAST                4 (@py_assert0)
#             144 CALL                     1
#             152 LOAD_CONST              10 ('normalized')
#             154 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             164 LOAD_ATTR               12 (locals)
#             184 CALL                     0
#             192 CONTAINS_OP              0
#             194 POP_JUMP_IF_TRUE        21 (to 238)
#             196 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             206 LOAD_ATTR               14 (_should_repr_global_name)
#             226 LOAD_FAST                3 (normalized)
#             228 CALL                     1
#             236 POP_JUMP_IF_FALSE       21 (to 280)
#         >>  238 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             248 LOAD_ATTR                8 (_saferepr)
#             268 LOAD_FAST                3 (normalized)
#             270 CALL                     1
#             278 JUMP_FORWARD             1 (to 282)
#         >>  280 LOAD_CONST              10 ('normalized')
#         >>  282 LOAD_CONST              11 (('py1', 'py3'))
#             284 BUILD_CONST_KEY_MAP      2
#             286 BINARY_OP                6 (%)
#             290 STORE_FAST               6 (@py_format4)
#             292 LOAD_CONST              12 ('assert %(py5)s')
#             294 LOAD_CONST              13 ('py5')
#             296 LOAD_FAST                6 (@py_format4)
#             298 BUILD_MAP                1
#             300 BINARY_OP                6 (%)
#             304 STORE_FAST               7 (@py_format6)
#             306 LOAD_GLOBAL             17 (NULL + AssertionError)
#             316 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             326 LOAD_ATTR               18 (_format_explanation)
#             346 LOAD_FAST                7 (@py_format6)
#             348 CALL                     1
#             356 CALL                     1
#             364 RAISE_VARARGS            1
#         >>  366 LOAD_CONST               0 (None)
#             368 COPY                     1
#             370 STORE_FAST               4 (@py_assert0)
#             372 STORE_FAST               5 (@py_assert2)
# 
# 176         374 LOAD_CONST              14 ('nested')
#             376 STORE_FAST               4 (@py_assert0)
#             378 LOAD_FAST                4 (@py_assert0)
#             380 LOAD_FAST                3 (normalized)
#             382 CONTAINS_OP              0
#             384 STORE_FAST               5 (@py_assert2)
#             386 LOAD_FAST                5 (@py_assert2)
#             388 POP_JUMP_IF_TRUE       153 (to 696)
#             390 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             400 LOAD_ATTR                6 (_call_reprcompare)
#             420 LOAD_CONST               8 (('in',))
#             422 LOAD_FAST                5 (@py_assert2)
#             424 BUILD_TUPLE              1
#             426 LOAD_CONST               9 (('%(py1)s in %(py3)s',))
#             428 LOAD_FAST                4 (@py_assert0)
#             430 LOAD_FAST                3 (normalized)
#             432 BUILD_TUPLE              2
#             434 CALL                     4
#             442 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             452 LOAD_ATTR                8 (_saferepr)
#             472 LOAD_FAST                4 (@py_assert0)
#             474 CALL                     1
#             482 LOAD_CONST              10 ('normalized')
#             484 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             494 LOAD_ATTR               12 (locals)
#             514 CALL                     0
#             522 CONTAINS_OP              0
#             524 POP_JUMP_IF_TRUE        21 (to 568)
#             526 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             536 LOAD_ATTR               14 (_should_repr_global_name)
#             556 LOAD_FAST                3 (normalized)
#             558 CALL                     1
#             566 POP_JUMP_IF_FALSE       21 (to 610)
#         >>  568 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             578 LOAD_ATTR                8 (_saferepr)
#             598 LOAD_FAST                3 (normalized)
#             600 CALL                     1
#             608 JUMP_FORWARD             1 (to 612)
#         >>  610 LOAD_CONST              10 ('normalized')
#         >>  612 LOAD_CONST              11 (('py1', 'py3'))
#             614 BUILD_CONST_KEY_MAP      2
#             616 BINARY_OP                6 (%)
#             620 STORE_FAST               6 (@py_format4)
#             622 LOAD_CONST              12 ('assert %(py5)s')
#             624 LOAD_CONST              13 ('py5')
#             626 LOAD_FAST                6 (@py_format4)
#             628 BUILD_MAP                1
#             630 BINARY_OP                6 (%)
#             634 STORE_FAST               7 (@py_format6)
#             636 LOAD_GLOBAL             17 (NULL + AssertionError)
#             646 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             656 LOAD_ATTR               18 (_format_explanation)
#             676 LOAD_FAST                7 (@py_format6)
#             678 CALL                     1
#             686 CALL                     1
#             694 RAISE_VARARGS            1
#         >>  696 LOAD_CONST               0 (None)
#             698 COPY                     1
#             700 STORE_FAST               4 (@py_assert0)
#             702 STORE_FAST               5 (@py_assert2)
# 
# 177         704 LOAD_CONST              15 ('total_loss')
#             706 STORE_FAST               4 (@py_assert0)
#             708 LOAD_FAST                3 (normalized)
#             710 LOAD_CONST              14 ('nested')
#             712 BINARY_SUBSCR
#             716 STORE_FAST               8 (@py_assert3)
#             718 LOAD_FAST                4 (@py_assert0)
#             720 LOAD_FAST                8 (@py_assert3)
#             722 CONTAINS_OP              0
#             724 STORE_FAST               5 (@py_assert2)
#             726 LOAD_FAST                5 (@py_assert2)
#             728 POP_JUMP_IF_TRUE       108 (to 946)
#             730 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             740 LOAD_ATTR                6 (_call_reprcompare)
#             760 LOAD_CONST               8 (('in',))
#             762 LOAD_FAST                5 (@py_assert2)
#             764 BUILD_TUPLE              1
#             766 LOAD_CONST              16 (('%(py1)s in %(py4)s',))
#             768 LOAD_FAST                4 (@py_assert0)
#             770 LOAD_FAST                8 (@py_assert3)
#             772 BUILD_TUPLE              2
#             774 CALL                     4
#             782 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             792 LOAD_ATTR                8 (_saferepr)
#             812 LOAD_FAST                4 (@py_assert0)
#             814 CALL                     1
#             822 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             832 LOAD_ATTR                8 (_saferepr)
#             852 LOAD_FAST                8 (@py_assert3)
#             854 CALL                     1
#             862 LOAD_CONST              17 (('py1', 'py4'))
#             864 BUILD_CONST_KEY_MAP      2
#             866 BINARY_OP                6 (%)
#             870 STORE_FAST               9 (@py_format5)
#             872 LOAD_CONST              18 ('assert %(py6)s')
#             874 LOAD_CONST              19 ('py6')
#             876 LOAD_FAST                9 (@py_format5)
#             878 BUILD_MAP                1
#             880 BINARY_OP                6 (%)
#             884 STORE_FAST              10 (@py_format7)
#             886 LOAD_GLOBAL             17 (NULL + AssertionError)
#             896 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             906 LOAD_ATTR               18 (_format_explanation)
#             926 LOAD_FAST               10 (@py_format7)
#             928 CALL                     1
#             936 CALL                     1
#             944 RAISE_VARARGS            1
#         >>  946 LOAD_CONST               0 (None)
#             948 COPY                     1
#             950 STORE_FAST               4 (@py_assert0)
#             952 COPY                     1
#             954 STORE_FAST               5 (@py_assert2)
#             956 STORE_FAST               8 (@py_assert3)
#             958 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestEnhancedFailurePath at 0x73cd945feb10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 180>:
# 180           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestEnhancedFailurePath')
#               8 STORE_NAME               2 (__qualname__)
# 
# 181          10 LOAD_CONST               1 (<code object test_validation_failure_contains_partial_data at 0x3aed46f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 181>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_validation_failure_contains_partial_data)
# 
# 192          16 LOAD_CONST               2 (<code object test_simulation_failure_contains_job_id at 0x3afa0aa0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 192>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_simulation_failure_contains_job_id)
#              22 RETURN_CONST             3 (None)
# 
# Disassembly of <code object test_validation_failure_contains_partial_data at 0x3aed46f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 181>:
# 181           0 RESUME                   0
# 
# 182           2 LOAD_GLOBAL              1 (NULL + SkillOutputValidator)
#              12 CALL                     0
#              20 STORE_FAST               1 (validator)
# 
# 183          22 LOAD_GLOBAL              3 (NULL + SkillResult)
#              32 LOAD_ATTR                4 (failure)
# 
# 184          52 LOAD_CONST               1 ('power_flow')
# 
# 185          54 LOAD_CONST               2 ('Invalid model RID')
# 
# 186          56 LOAD_CONST               3 ('validation')
#              58 LOAD_CONST               4 ('model.rid')
#              60 LOAD_CONST               5 (('stage', 'field'))
#              62 BUILD_CONST_KEY_MAP      2
# 
# 183          64 KW_NAMES                 6 (('skill_name', 'error', 'data'))
#              66 CALL                     3
#              74 STORE_FAST               2 (result)
# 
# 188          76 LOAD_FAST                1 (validator)
#              78 LOAD_ATTR                7 (NULL|self + validate_failure_path)
#              98 LOAD_FAST                2 (result)
#             100 CALL                     1
#             108 STORE_FAST               3 (validation)
# 
# 189         110 LOAD_FAST                3 (validation)
#             112 LOAD_ATTR                8 (valid)
#             132 STORE_FAST               4 (@py_assert1)
#             134 LOAD_CONST               7 (True)
#             136 STORE_FAST               5 (@py_assert4)
#             138 LOAD_FAST                4 (@py_assert1)
#             140 LOAD_FAST                5 (@py_assert4)
#             142 IS_OP                    0
#             144 STORE_FAST               6 (@py_assert3)
#             146 LOAD_FAST                6 (@py_assert3)
#             148 POP_JUMP_IF_TRUE       173 (to 496)
#             150 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             160 LOAD_ATTR               12 (_call_reprcompare)
#             180 LOAD_CONST               8 (('is',))
#             182 LOAD_FAST                6 (@py_assert3)
#             184 BUILD_TUPLE              1
#             186 LOAD_CONST               9 (('%(py2)s\n{%(py2)s = %(py0)s.valid\n} is %(py5)s',))
#             188 LOAD_FAST                4 (@py_assert1)
#             190 LOAD_FAST                5 (@py_assert4)
#             192 BUILD_TUPLE              2
#             194 CALL                     4
#             202 LOAD_CONST               3 ('validation')
#             204 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             214 LOAD_ATTR               16 (locals)
#             234 CALL                     0
#             242 CONTAINS_OP              0
#             244 POP_JUMP_IF_TRUE        21 (to 288)
#             246 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             256 LOAD_ATTR               18 (_should_repr_global_name)
#             276 LOAD_FAST                3 (validation)
#             278 CALL                     1
#             286 POP_JUMP_IF_FALSE       21 (to 330)
#         >>  288 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             298 LOAD_ATTR               20 (_saferepr)
#             318 LOAD_FAST                3 (validation)
#             320 CALL                     1
#             328 JUMP_FORWARD             1 (to 332)
#         >>  330 LOAD_CONST               3 ('validation')
#         >>  332 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             342 LOAD_ATTR               20 (_saferepr)
#             362 LOAD_FAST                4 (@py_assert1)
#             364 CALL                     1
#             372 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             382 LOAD_ATTR               20 (_saferepr)
#             402 LOAD_FAST                5 (@py_assert4)
#             404 CALL                     1
#             412 LOAD_CONST              10 (('py0', 'py2', 'py5'))
#             414 BUILD_CONST_KEY_MAP      3
#             416 BINARY_OP                6 (%)
#             420 STORE_FAST               7 (@py_format6)
#             422 LOAD_CONST              11 ('assert %(py7)s')
#             424 LOAD_CONST              12 ('py7')
#             426 LOAD_FAST                7 (@py_format6)
#             428 BUILD_MAP                1
#             430 BINARY_OP                6 (%)
#             434 STORE_FAST               8 (@py_format8)
#             436 LOAD_GLOBAL             23 (NULL + AssertionError)
#             446 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             456 LOAD_ATTR               24 (_format_explanation)
#             476 LOAD_FAST                8 (@py_format8)
#             478 CALL                     1
#             486 CALL                     1
#             494 RAISE_VARARGS            1
#         >>  496 LOAD_CONST               0 (None)
#             498 COPY                     1
#             500 STORE_FAST               4 (@py_assert1)
#             502 COPY                     1
#             504 STORE_FAST               6 (@py_assert3)
#             506 STORE_FAST               5 (@py_assert4)
# 
# 190         508 LOAD_FAST                2 (result)
#             510 LOAD_ATTR               26 (data)
#             530 STORE_FAST               4 (@py_assert1)
#             532 LOAD_FAST                4 (@py_assert1)
#             534 LOAD_ATTR               28 (get)
#             554 STORE_FAST               6 (@py_assert3)
#             556 LOAD_CONST              13 ('stage')
#             558 STORE_FAST               9 (@py_assert5)
#             560 PUSH_NULL
#             562 LOAD_FAST                6 (@py_assert3)
#             564 LOAD_FAST                9 (@py_assert5)
#             566 CALL                     1
#             574 STORE_FAST              10 (@py_assert7)
#             576 LOAD_CONST               3 ('validation')
#             578 STORE_FAST              11 (@py_assert10)
#             580 LOAD_FAST               10 (@py_assert7)
#             582 LOAD_FAST               11 (@py_assert10)
#             584 COMPARE_OP              40 (==)
#             588 STORE_FAST              12 (@py_assert9)
#             590 LOAD_FAST               12 (@py_assert9)
#             592 POP_JUMP_IF_TRUE       233 (to 1060)
#             594 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             604 LOAD_ATTR               12 (_call_reprcompare)
#             624 LOAD_CONST              14 (('==',))
#             626 LOAD_FAST               12 (@py_assert9)
#             628 BUILD_TUPLE              1
#             630 LOAD_CONST              15 (('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.data\n}.get\n}(%(py6)s)\n} == %(py11)s',))
#             632 LOAD_FAST               10 (@py_assert7)
#             634 LOAD_FAST               11 (@py_assert10)
#             636 BUILD_TUPLE              2
#             638 CALL                     4
#             646 LOAD_CONST              16 ('result')
#             648 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             658 LOAD_ATTR               16 (locals)
#             678 CALL                     0
#             686 CONTAINS_OP              0
#             688 POP_JUMP_IF_TRUE        21 (to 732)
#             690 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             700 LOAD_ATTR               18 (_should_repr_global_name)
#             720 LOAD_FAST                2 (result)
#             722 CALL                     1
#             730 POP_JUMP_IF_FALSE       21 (to 774)
#         >>  732 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             742 LOAD_ATTR               20 (_saferepr)
#             762 LOAD_FAST                2 (result)
#             764 CALL                     1
#             772 JUMP_FORWARD             1 (to 776)
#         >>  774 LOAD_CONST              16 ('result')
#         >>  776 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             786 LOAD_ATTR               20 (_saferepr)
#             806 LOAD_FAST                4 (@py_assert1)
#             808 CALL                     1
#             816 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             826 LOAD_ATTR               20 (_saferepr)
#             846 LOAD_FAST                6 (@py_assert3)
#             848 CALL                     1
#             856 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             866 LOAD_ATTR               20 (_saferepr)
#             886 LOAD_FAST                9 (@py_assert5)
#             888 CALL                     1
#             896 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             906 LOAD_ATTR               20 (_saferepr)
#             926 LOAD_FAST               10 (@py_assert7)
#             928 CALL                     1
#             936 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             946 LOAD_ATTR               20 (_saferepr)
#             966 LOAD_FAST               11 (@py_assert10)
#             968 CALL                     1
#             976 LOAD_CONST              17 (('py0', 'py2', 'py4', 'py6', 'py8', 'py11'))
#             978 BUILD_CONST_KEY_MAP      6
#             980 BINARY_OP                6 (%)
#             984 STORE_FAST              13 (@py_format12)
#             986 LOAD_CONST              18 ('assert %(py13)s')
#             988 LOAD_CONST              19 ('py13')
#             990 LOAD_FAST               13 (@py_format12)
#             992 BUILD_MAP                1
#             994 BINARY_OP                6 (%)
#             998 STORE_FAST              14 (@py_format14)
#            1000 LOAD_GLOBAL             23 (NULL + AssertionError)
#            1010 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1020 LOAD_ATTR               24 (_format_explanation)
#            1040 LOAD_FAST               14 (@py_format14)
#            1042 CALL                     1
#            1050 CALL                     1
#            1058 RAISE_VARARGS            1
#         >> 1060 LOAD_CONST               0 (None)
#            1062 COPY                     1
#            1064 STORE_FAST               4 (@py_assert1)
#            1066 COPY                     1
#            1068 STORE_FAST               6 (@py_assert3)
#            1070 COPY                     1
#            1072 STORE_FAST               9 (@py_assert5)
#            1074 COPY                     1
#            1076 STORE_FAST              10 (@py_assert7)
#            1078 COPY                     1
#            1080 STORE_FAST              12 (@py_assert9)
#            1082 STORE_FAST              11 (@py_assert10)
#            1084 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_simulation_failure_contains_job_id at 0x3afa0aa0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_output_standard.py", line 192>:
# 192           0 RESUME                   0
# 
# 193           2 LOAD_GLOBAL              1 (NULL + SkillResult)
#              12 LOAD_ATTR                2 (failure)
# 
# 194          32 LOAD_CONST               1 ('power_flow')
# 
# 195          34 LOAD_CONST               2 ('Simulation failed')
# 
# 196          36 LOAD_CONST               3 ('simulation')
#              38 LOAD_CONST               4 ('job_123')
#              40 LOAD_CONST               5 (('stage', 'job_id'))
#              42 BUILD_CONST_KEY_MAP      2
# 
# 193          44 KW_NAMES                 6 (('skill_name', 'error', 'data'))
#              46 CALL                     3
#              54 STORE_FAST               1 (result)
# 
# 198          56 LOAD_FAST                1 (result)
#              58 LOAD_ATTR                4 (data)
#              78 STORE_FAST               2 (@py_assert1)
#              80 LOAD_FAST                2 (@py_assert1)
#              82 LOAD_ATTR                6 (get)
#             102 STORE_FAST               3 (@py_assert3)
#             104 LOAD_CONST               7 ('job_id')
#             106 STORE_FAST               4 (@py_assert5)
#             108 PUSH_NULL
#             110 LOAD_FAST                3 (@py_assert3)
#             112 LOAD_FAST                4 (@py_assert5)
#             114 CALL                     1
#             122 STORE_FAST               5 (@py_assert7)
#             124 LOAD_CONST               4 ('job_123')
#             126 STORE_FAST               6 (@py_assert10)
#             128 LOAD_FAST                5 (@py_assert7)
#             130 LOAD_FAST                6 (@py_assert10)
#             132 COMPARE_OP              40 (==)
#             136 STORE_FAST               7 (@py_assert9)
#             138 LOAD_FAST                7 (@py_assert9)
#             140 POP_JUMP_IF_TRUE       233 (to 608)
#             142 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             152 LOAD_ATTR               10 (_call_reprcompare)
#             172 LOAD_CONST               8 (('==',))
#             174 LOAD_FAST                7 (@py_assert9)
#             176 BUILD_TUPLE              1
#             178 LOAD_CONST               9 (('%(py8)s\n{%(py8)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.data\n}.get\n}(%(py6)s)\n} == %(py11)s',))
#             180 LOAD_FAST                5 (@py_assert7)
#             182 LOAD_FAST                6 (@py_assert10)
#             184 BUILD_TUPLE              2
#             186 CALL                     4
#             194 LOAD_CONST              10 ('result')
#             196 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             206 LOAD_ATTR               14 (locals)
#             226 CALL                     0
#             234 CONTAINS_OP              0
#             236 POP_JUMP_IF_TRUE        21 (to 280)
#             238 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             248 LOAD_ATTR               16 (_should_repr_global_name)
#             268 LOAD_FAST                1 (result)
#             270 CALL                     1
#             278 POP_JUMP_IF_FALSE       21 (to 322)
#         >>  280 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             290 LOAD_ATTR               18 (_saferepr)
#             310 LOAD_FAST                1 (result)
#             312 CALL                     1
#             320 JUMP_FORWARD             1 (to 324)
#         >>  322 LOAD_CONST              10 ('result')
#         >>  324 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             334 LOAD_ATTR               18 (_saferepr)
#             354 LOAD_FAST                2 (@py_assert1)
#             356 CALL                     1
#             364 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             374 LOAD_ATTR               18 (_saferepr)
#             394 LOAD_FAST                3 (@py_assert3)
#             396 CALL                     1
#             404 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             414 LOAD_ATTR               18 (_saferepr)
#             434 LOAD_FAST                4 (@py_assert5)
#             436 CALL                     1
#             444 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             454 LOAD_ATTR               18 (_saferepr)
#             474 LOAD_FAST                5 (@py_assert7)
#             476 CALL                     1
#             484 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             494 LOAD_ATTR               18 (_saferepr)
#             514 LOAD_FAST                6 (@py_assert10)
#             516 CALL                     1
#             524 LOAD_CONST              11 (('py0', 'py2', 'py4', 'py6', 'py8', 'py11'))
#             526 BUILD_CONST_KEY_MAP      6
#             528 BINARY_OP                6 (%)
#             532 STORE_FAST               8 (@py_format12)
#             534 LOAD_CONST              12 ('assert %(py13)s')
#             536 LOAD_CONST              13 ('py13')
#             538 LOAD_FAST                8 (@py_format12)
#             540 BUILD_MAP                1
#             542 BINARY_OP                6 (%)
#             546 STORE_FAST               9 (@py_format14)
#             548 LOAD_GLOBAL             21 (NULL + AssertionError)
#             558 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             568 LOAD_ATTR               22 (_format_explanation)
#             588 LOAD_FAST                9 (@py_format14)
#             590 CALL                     1
#             598 CALL                     1
#             606 RAISE_VARARGS            1
#         >>  608 LOAD_CONST               0 (None)
#             610 COPY                     1
#             612 STORE_FAST               2 (@py_assert1)
#             614 COPY                     1
#             616 STORE_FAST               3 (@py_assert3)
#             618 COPY                     1
#             620 STORE_FAST               4 (@py_assert5)
#             622 COPY                     1
#             624 STORE_FAST               5 (@py_assert7)
#             626 COPY                     1
#             628 STORE_FAST               7 (@py_assert9)
#             630 STORE_FAST               6 (@py_assert10)
#             632 RETURN_CONST             0 (None)
# 