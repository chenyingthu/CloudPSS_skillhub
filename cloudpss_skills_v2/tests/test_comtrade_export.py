# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/__pycache__/test_comtrade_export.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


def TestComtradeExportValidation():
    """TestComtradeExportValidation"""
pass  # TODO: restore


def TestComtradeExportHelpers():
    """TestComtradeExportHelpers"""
pass  # TODO: restore


def TestComtradeExportRun():
    """TestComtradeExportRun"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('Tests for ComtradeExportSkill v2.')
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
#              42 LOAD_CONST               3 (('ComtradeExportSkill',))
#              44 IMPORT_NAME              8 (cloudpss_skills_v2.skills.comtrade_export)
#              46 IMPORT_FROM              9 (ComtradeExportSkill)
#              48 STORE_NAME               9 (ComtradeExportSkill)
#              50 POP_TOP
# 
#   7          52 PUSH_NULL
#              54 LOAD_BUILD_CLASS
#              56 LOAD_CONST               4 (<code object TestComtradeExportValidation at 0x73cd93b06880, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 7>)
#              58 MAKE_FUNCTION            0
#              60 LOAD_CONST               5 ('TestComtradeExportValidation')
#              62 CALL                     2
#              70 STORE_NAME              10 (TestComtradeExportValidation)
# 
#  31          72 PUSH_NULL
#              74 LOAD_BUILD_CLASS
#              76 LOAD_CONST               6 (<code object TestComtradeExportHelpers at 0x73cd93b06970, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 31>)
#              78 MAKE_FUNCTION            0
#              80 LOAD_CONST               7 ('TestComtradeExportHelpers')
#              82 CALL                     2
#              90 STORE_NAME              11 (TestComtradeExportHelpers)
# 
#  59          92 PUSH_NULL
#              94 LOAD_BUILD_CLASS
#              96 LOAD_CONST               8 (<code object TestComtradeExportRun at 0x73cd945fea30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 59>)
#              98 MAKE_FUNCTION            0
#             100 LOAD_CONST               9 ('TestComtradeExportRun')
#             102 CALL                     2
#             110 STORE_NAME              12 (TestComtradeExportRun)
#             112 RETURN_CONST             2 (None)
# 
# Disassembly of <code object TestComtradeExportValidation at 0x73cd93b06880, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 7>:
#   7           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestComtradeExportValidation')
#               8 STORE_NAME               2 (__qualname__)
# 
#   8          10 LOAD_CONST               1 ('Test validation logic.')
#              12 STORE_NAME               3 (__doc__)
# 
#  10          14 LOAD_CONST               2 (<code object test_validate_missing_source at 0x3af9f150, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 10>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_validate_missing_source)
# 
#  17          20 LOAD_CONST               3 (<code object test_validate_source_missing_job_id at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 17>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_validate_source_missing_job_id)
# 
#  23          26 LOAD_CONST               4 (<code object test_validate_valid_config at 0x3afa7720, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 23>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_validate_valid_config)
#              32 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_validate_missing_source at 0x3af9f150, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 10>:
#  10           0 RESUME                   0
# 
#  11           2 LOAD_GLOBAL              1 (NULL + ComtradeExportSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  12          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + validate)
#              44 BUILD_MAP                0
#              46 CALL                     1
#              54 UNPACK_SEQUENCE          2
#              58 STORE_FAST               2 (valid)
#              60 STORE_FAST               3 (errors)
# 
#  13          62 LOAD_CONST               1 (False)
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
#  14         392 LOAD_GLOBAL             21 (NULL + len)
#             402 LOAD_FAST                3 (errors)
#             404 CALL                     1
#             412 STORE_FAST               4 (@py_assert2)
#             414 LOAD_CONST               8 (0)
#             416 STORE_FAST               8 (@py_assert5)
#             418 LOAD_FAST                4 (@py_assert2)
#             420 LOAD_FAST                8 (@py_assert5)
#             422 COMPARE_OP              68 (>)
#             426 STORE_FAST               9 (@py_assert4)
#             428 LOAD_FAST                9 (@py_assert4)
#             430 POP_JUMP_IF_TRUE       246 (to 924)
#             432 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             442 LOAD_ATTR                6 (_call_reprcompare)
#             462 LOAD_CONST               9 (('>',))
#             464 LOAD_FAST                9 (@py_assert4)
#             466 BUILD_TUPLE              1
#             468 LOAD_CONST              10 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} > %(py6)s',))
#             470 LOAD_FAST                4 (@py_assert2)
#             472 LOAD_FAST                8 (@py_assert5)
#             474 BUILD_TUPLE              2
#             476 CALL                     4
#             484 LOAD_CONST              11 ('len')
#             486 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             496 LOAD_ATTR               10 (locals)
#             516 CALL                     0
#             524 CONTAINS_OP              0
#             526 POP_JUMP_IF_TRUE        25 (to 578)
#             528 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             538 LOAD_ATTR               12 (_should_repr_global_name)
#             558 LOAD_GLOBAL             20 (len)
#             568 CALL                     1
#             576 POP_JUMP_IF_FALSE       25 (to 628)
#         >>  578 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             588 LOAD_ATTR               14 (_saferepr)
#             608 LOAD_GLOBAL             20 (len)
#             618 CALL                     1
#             626 JUMP_FORWARD             1 (to 630)
#         >>  628 LOAD_CONST              11 ('len')
#         >>  630 LOAD_CONST              12 ('errors')
#             632 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             642 LOAD_ATTR               10 (locals)
#             662 CALL                     0
#             670 CONTAINS_OP              0
#             672 POP_JUMP_IF_TRUE        21 (to 716)
#             674 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             684 LOAD_ATTR               12 (_should_repr_global_name)
#             704 LOAD_FAST                3 (errors)
#             706 CALL                     1
#             714 POP_JUMP_IF_FALSE       21 (to 758)
#         >>  716 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             726 LOAD_ATTR               14 (_saferepr)
#             746 LOAD_FAST                3 (errors)
#             748 CALL                     1
#             756 JUMP_FORWARD             1 (to 760)
#         >>  758 LOAD_CONST              12 ('errors')
#         >>  760 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             770 LOAD_ATTR               14 (_saferepr)
#             790 LOAD_FAST                4 (@py_assert2)
#             792 CALL                     1
#             800 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             810 LOAD_ATTR               14 (_saferepr)
#             830 LOAD_FAST                8 (@py_assert5)
#             832 CALL                     1
#             840 LOAD_CONST              13 (('py0', 'py1', 'py3', 'py6'))
#             842 BUILD_CONST_KEY_MAP      4
#             844 BINARY_OP                6 (%)
#             848 STORE_FAST              10 (@py_format7)
#             850 LOAD_CONST              14 ('assert %(py8)s')
#             852 LOAD_CONST              15 ('py8')
#             854 LOAD_FAST               10 (@py_format7)
#             856 BUILD_MAP                1
#             858 BINARY_OP                6 (%)
#             862 STORE_FAST              11 (@py_format9)
#             864 LOAD_GLOBAL             17 (NULL + AssertionError)
#             874 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             884 LOAD_ATTR               18 (_format_explanation)
#             904 LOAD_FAST               11 (@py_format9)
#             906 CALL                     1
#             914 CALL                     1
#             922 RAISE_VARARGS            1
#         >>  924 LOAD_CONST               0 (None)
#             926 COPY                     1
#             928 STORE_FAST               4 (@py_assert2)
#             930 COPY                     1
#             932 STORE_FAST               9 (@py_assert4)
#             934 STORE_FAST               8 (@py_assert5)
# 
#  15         936 LOAD_CONST              16 (<code object <genexpr> at 0x73cd93b064c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 15>)
#             938 MAKE_FUNCTION            0
#             940 LOAD_FAST                3 (errors)
#             942 GET_ITER
#             944 CALL                     0
#             952 STORE_FAST               5 (@py_assert1)
#             954 LOAD_GLOBAL             23 (NULL + any)
#             964 LOAD_FAST                5 (@py_assert1)
#             966 CALL                     1
#             974 STORE_FAST              12 (@py_assert3)
#             976 LOAD_FAST               12 (@py_assert3)
#             978 POP_JUMP_IF_TRUE       149 (to 1278)
#             980 LOAD_CONST              17 ('assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}')
#             982 LOAD_CONST              18 ('any')
#             984 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             994 LOAD_ATTR               10 (locals)
#            1014 CALL                     0
#            1022 CONTAINS_OP              0
#            1024 POP_JUMP_IF_TRUE        25 (to 1076)
#            1026 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1036 LOAD_ATTR               12 (_should_repr_global_name)
#            1056 LOAD_GLOBAL             22 (any)
#            1066 CALL                     1
#            1074 POP_JUMP_IF_FALSE       25 (to 1126)
#         >> 1076 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1086 LOAD_ATTR               14 (_saferepr)
#            1106 LOAD_GLOBAL             22 (any)
#            1116 CALL                     1
#            1124 JUMP_FORWARD             1 (to 1128)
#         >> 1126 LOAD_CONST              18 ('any')
#         >> 1128 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1138 LOAD_ATTR               14 (_saferepr)
#            1158 LOAD_FAST                5 (@py_assert1)
#            1160 CALL                     1
#            1168 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1178 LOAD_ATTR               14 (_saferepr)
#            1198 LOAD_FAST               12 (@py_assert3)
#            1200 CALL                     1
#            1208 LOAD_CONST              19 (('py0', 'py2', 'py4'))
#            1210 BUILD_CONST_KEY_MAP      3
#            1212 BINARY_OP                6 (%)
#            1216 STORE_FAST              13 (@py_format5)
#            1218 LOAD_GLOBAL             17 (NULL + AssertionError)
#            1228 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1238 LOAD_ATTR               18 (_format_explanation)
#            1258 LOAD_FAST               13 (@py_format5)
#            1260 CALL                     1
#            1268 CALL                     1
#            1276 RAISE_VARARGS            1
#         >> 1278 LOAD_CONST               0 (None)
#            1280 COPY                     1
#            1282 STORE_FAST               5 (@py_assert1)
#            1284 STORE_FAST              12 (@py_assert3)
#            1286 RETURN_CONST             0 (None)
# 
# Disassembly of <code object <genexpr> at 0x73cd93b064c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 15>:
#  15           0 RETURN_GENERATOR
#               2 POP_TOP
#               4 RESUME                   0
#               6 LOAD_FAST                0 (.0)
#         >>    8 FOR_ITER                 8 (to 28)
#              12 STORE_FAST               1 (e)
#              14 LOAD_CONST               0 ('source.job_id')
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
# Disassembly of <code object test_validate_source_missing_job_id at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 17>:
#  17           0 RESUME                   0
# 
#  18           2 LOAD_GLOBAL              1 (NULL + ComtradeExportSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  19          22 LOAD_CONST               1 ('source')
#              24 LOAD_CONST               2 ('other')
#              26 LOAD_CONST               3 ('value')
#              28 BUILD_MAP                1
#              30 BUILD_MAP                1
#              32 STORE_FAST               2 (config)
# 
#  20          34 LOAD_FAST                1 (skill)
#              36 LOAD_ATTR                3 (NULL|self + validate)
#              56 LOAD_FAST                2 (config)
#              58 CALL                     1
#              66 UNPACK_SEQUENCE          2
#              70 STORE_FAST               3 (valid)
#              72 STORE_FAST               4 (errors)
# 
#  21          74 LOAD_CONST               4 (False)
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
# Disassembly of <code object test_validate_valid_config at 0x3afa7720, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 23>:
#  23           0 RESUME                   0
# 
#  24           2 LOAD_GLOBAL              1 (NULL + ComtradeExportSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  25          22 LOAD_CONST               1 ('source')
#              24 LOAD_CONST               2 ('job_id')
#              26 LOAD_CONST               3 ('test_job_123')
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
#  27          74 LOAD_CONST               4 (True)
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
#  28         404 LOAD_GLOBAL             21 (NULL + len)
#             414 LOAD_FAST                4 (errors)
#             416 CALL                     1
#             424 STORE_FAST               5 (@py_assert2)
#             426 LOAD_CONST              11 (0)
#             428 STORE_FAST               9 (@py_assert5)
#             430 LOAD_FAST                5 (@py_assert2)
#             432 LOAD_FAST                9 (@py_assert5)
#             434 COMPARE_OP              40 (==)
#             438 STORE_FAST              10 (@py_assert4)
#             440 LOAD_FAST               10 (@py_assert4)
#             442 POP_JUMP_IF_TRUE       246 (to 936)
#             444 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             454 LOAD_ATTR                6 (_call_reprcompare)
#             474 LOAD_CONST              12 (('==',))
#             476 LOAD_FAST               10 (@py_assert4)
#             478 BUILD_TUPLE              1
#             480 LOAD_CONST              13 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             482 LOAD_FAST                5 (@py_assert2)
#             484 LOAD_FAST                9 (@py_assert5)
#             486 BUILD_TUPLE              2
#             488 CALL                     4
#             496 LOAD_CONST              14 ('len')
#             498 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             508 LOAD_ATTR               10 (locals)
#             528 CALL                     0
#             536 CONTAINS_OP              0
#             538 POP_JUMP_IF_TRUE        25 (to 590)
#             540 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             550 LOAD_ATTR               12 (_should_repr_global_name)
#             570 LOAD_GLOBAL             20 (len)
#             580 CALL                     1
#             588 POP_JUMP_IF_FALSE       25 (to 640)
#         >>  590 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             600 LOAD_ATTR               14 (_saferepr)
#             620 LOAD_GLOBAL             20 (len)
#             630 CALL                     1
#             638 JUMP_FORWARD             1 (to 642)
#         >>  640 LOAD_CONST              14 ('len')
#         >>  642 LOAD_CONST              15 ('errors')
#             644 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             654 LOAD_ATTR               10 (locals)
#             674 CALL                     0
#             682 CONTAINS_OP              0
#             684 POP_JUMP_IF_TRUE        21 (to 728)
#             686 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             696 LOAD_ATTR               12 (_should_repr_global_name)
#             716 LOAD_FAST                4 (errors)
#             718 CALL                     1
#             726 POP_JUMP_IF_FALSE       21 (to 770)
#         >>  728 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             738 LOAD_ATTR               14 (_saferepr)
#             758 LOAD_FAST                4 (errors)
#             760 CALL                     1
#             768 JUMP_FORWARD             1 (to 772)
#         >>  770 LOAD_CONST              15 ('errors')
#         >>  772 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             782 LOAD_ATTR               14 (_saferepr)
#             802 LOAD_FAST                5 (@py_assert2)
#             804 CALL                     1
#             812 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             822 LOAD_ATTR               14 (_saferepr)
#             842 LOAD_FAST                9 (@py_assert5)
#             844 CALL                     1
#             852 LOAD_CONST              16 (('py0', 'py1', 'py3', 'py6'))
#             854 BUILD_CONST_KEY_MAP      4
#             856 BINARY_OP                6 (%)
#             860 STORE_FAST              11 (@py_format7)
#             862 LOAD_CONST              17 ('assert %(py8)s')
#             864 LOAD_CONST              18 ('py8')
#             866 LOAD_FAST               11 (@py_format7)
#             868 BUILD_MAP                1
#             870 BINARY_OP                6 (%)
#             874 STORE_FAST              12 (@py_format9)
#             876 LOAD_GLOBAL             17 (NULL + AssertionError)
#             886 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             896 LOAD_ATTR               18 (_format_explanation)
#             916 LOAD_FAST               12 (@py_format9)
#             918 CALL                     1
#             926 CALL                     1
#             934 RAISE_VARARGS            1
#         >>  936 LOAD_CONST               0 (None)
#             938 COPY                     1
#             940 STORE_FAST               5 (@py_assert2)
#             942 COPY                     1
#             944 STORE_FAST              10 (@py_assert4)
#             946 STORE_FAST               9 (@py_assert5)
#             948 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestComtradeExportHelpers at 0x73cd93b06970, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 31>:
#  31           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestComtradeExportHelpers')
#               8 STORE_NAME               2 (__qualname__)
# 
#  32          10 LOAD_CONST               1 ('Test helper methods.')
#              12 STORE_NAME               3 (__doc__)
# 
#  34          14 LOAD_CONST               2 (<code object test_generate_cfg_header at 0x3af9e7f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 34>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_generate_cfg_header)
# 
#  47          20 LOAD_CONST               3 (<code object test_format_timestamp at 0x3afa5570, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 47>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_format_timestamp)
# 
#  52          26 LOAD_CONST               4 (<code object test_generate_dat_record at 0x3afa6720, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 52>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_generate_dat_record)
#              32 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_generate_cfg_header at 0x3af9e7f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 34>:
#  34           0 RESUME                   0
# 
#  35           2 LOAD_GLOBAL              1 (NULL + ComtradeExportSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  36          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _generate_cfg_header)
# 
#  37          44 LOAD_CONST               1 ('TEST')
# 
#  38          46 LOAD_CONST               2 ('EMT1')
# 
#  39          48 LOAD_CONST               3 (3)
# 
#  40          50 LOAD_CONST               4 (4800)
# 
#  41          52 LOAD_CONST               5 (60.0)
# 
#  36          54 KW_NAMES                 6 (('station_name', 'rec_dev_id', 'num_channels', 'sample_rate', 'frequency'))
#              56 CALL                     5
#              64 STORE_FAST               2 (header)
# 
#  43          66 LOAD_CONST               1 ('TEST')
#              68 STORE_FAST               3 (@py_assert0)
#              70 LOAD_FAST                3 (@py_assert0)
#              72 LOAD_FAST                2 (header)
#              74 CONTAINS_OP              0
#              76 STORE_FAST               4 (@py_assert2)
#              78 LOAD_FAST                4 (@py_assert2)
#              80 POP_JUMP_IF_TRUE       153 (to 388)
#              82 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              92 LOAD_ATTR                6 (_call_reprcompare)
#             112 LOAD_CONST               7 (('in',))
#             114 LOAD_FAST                4 (@py_assert2)
#             116 BUILD_TUPLE              1
#             118 LOAD_CONST               8 (('%(py1)s in %(py3)s',))
#             120 LOAD_FAST                3 (@py_assert0)
#             122 LOAD_FAST                2 (header)
#             124 BUILD_TUPLE              2
#             126 CALL                     4
#             134 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             144 LOAD_ATTR                8 (_saferepr)
#             164 LOAD_FAST                3 (@py_assert0)
#             166 CALL                     1
#             174 LOAD_CONST               9 ('header')
#             176 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             186 LOAD_ATTR               12 (locals)
#             206 CALL                     0
#             214 CONTAINS_OP              0
#             216 POP_JUMP_IF_TRUE        21 (to 260)
#             218 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             228 LOAD_ATTR               14 (_should_repr_global_name)
#             248 LOAD_FAST                2 (header)
#             250 CALL                     1
#             258 POP_JUMP_IF_FALSE       21 (to 302)
#         >>  260 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             270 LOAD_ATTR                8 (_saferepr)
#             290 LOAD_FAST                2 (header)
#             292 CALL                     1
#             300 JUMP_FORWARD             1 (to 304)
#         >>  302 LOAD_CONST               9 ('header')
#         >>  304 LOAD_CONST              10 (('py1', 'py3'))
#             306 BUILD_CONST_KEY_MAP      2
#             308 BINARY_OP                6 (%)
#             312 STORE_FAST               5 (@py_format4)
#             314 LOAD_CONST              11 ('assert %(py5)s')
#             316 LOAD_CONST              12 ('py5')
#             318 LOAD_FAST                5 (@py_format4)
#             320 BUILD_MAP                1
#             322 BINARY_OP                6 (%)
#             326 STORE_FAST               6 (@py_format6)
#             328 LOAD_GLOBAL             17 (NULL + AssertionError)
#             338 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             348 LOAD_ATTR               18 (_format_explanation)
#             368 LOAD_FAST                6 (@py_format6)
#             370 CALL                     1
#             378 CALL                     1
#             386 RAISE_VARARGS            1
#         >>  388 LOAD_CONST               0 (None)
#             390 COPY                     1
#             392 STORE_FAST               3 (@py_assert0)
#             394 STORE_FAST               4 (@py_assert2)
# 
#  44         396 LOAD_CONST               2 ('EMT1')
#             398 STORE_FAST               3 (@py_assert0)
#             400 LOAD_FAST                3 (@py_assert0)
#             402 LOAD_FAST                2 (header)
#             404 CONTAINS_OP              0
#             406 STORE_FAST               4 (@py_assert2)
#             408 LOAD_FAST                4 (@py_assert2)
#             410 POP_JUMP_IF_TRUE       153 (to 718)
#             412 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             422 LOAD_ATTR                6 (_call_reprcompare)
#             442 LOAD_CONST               7 (('in',))
#             444 LOAD_FAST                4 (@py_assert2)
#             446 BUILD_TUPLE              1
#             448 LOAD_CONST               8 (('%(py1)s in %(py3)s',))
#             450 LOAD_FAST                3 (@py_assert0)
#             452 LOAD_FAST                2 (header)
#             454 BUILD_TUPLE              2
#             456 CALL                     4
#             464 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             474 LOAD_ATTR                8 (_saferepr)
#             494 LOAD_FAST                3 (@py_assert0)
#             496 CALL                     1
#             504 LOAD_CONST               9 ('header')
#             506 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             516 LOAD_ATTR               12 (locals)
#             536 CALL                     0
#             544 CONTAINS_OP              0
#             546 POP_JUMP_IF_TRUE        21 (to 590)
#             548 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             558 LOAD_ATTR               14 (_should_repr_global_name)
#             578 LOAD_FAST                2 (header)
#             580 CALL                     1
#             588 POP_JUMP_IF_FALSE       21 (to 632)
#         >>  590 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             600 LOAD_ATTR                8 (_saferepr)
#             620 LOAD_FAST                2 (header)
#             622 CALL                     1
#             630 JUMP_FORWARD             1 (to 634)
#         >>  632 LOAD_CONST               9 ('header')
#         >>  634 LOAD_CONST              10 (('py1', 'py3'))
#             636 BUILD_CONST_KEY_MAP      2
#             638 BINARY_OP                6 (%)
#             642 STORE_FAST               5 (@py_format4)
#             644 LOAD_CONST              11 ('assert %(py5)s')
#             646 LOAD_CONST              12 ('py5')
#             648 LOAD_FAST                5 (@py_format4)
#             650 BUILD_MAP                1
#             652 BINARY_OP                6 (%)
#             656 STORE_FAST               6 (@py_format6)
#             658 LOAD_GLOBAL             17 (NULL + AssertionError)
#             668 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             678 LOAD_ATTR               18 (_format_explanation)
#             698 LOAD_FAST                6 (@py_format6)
#             700 CALL                     1
#             708 CALL                     1
#             716 RAISE_VARARGS            1
#         >>  718 LOAD_CONST               0 (None)
#             720 COPY                     1
#             722 STORE_FAST               3 (@py_assert0)
#             724 STORE_FAST               4 (@py_assert2)
# 
#  45         726 LOAD_CONST              13 ('1999')
#             728 STORE_FAST               3 (@py_assert0)
#             730 LOAD_FAST                3 (@py_assert0)
#             732 LOAD_FAST                2 (header)
#             734 CONTAINS_OP              0
#             736 STORE_FAST               4 (@py_assert2)
#             738 LOAD_FAST                4 (@py_assert2)
#             740 POP_JUMP_IF_TRUE       153 (to 1048)
#             742 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             752 LOAD_ATTR                6 (_call_reprcompare)
#             772 LOAD_CONST               7 (('in',))
#             774 LOAD_FAST                4 (@py_assert2)
#             776 BUILD_TUPLE              1
#             778 LOAD_CONST               8 (('%(py1)s in %(py3)s',))
#             780 LOAD_FAST                3 (@py_assert0)
#             782 LOAD_FAST                2 (header)
#             784 BUILD_TUPLE              2
#             786 CALL                     4
#             794 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             804 LOAD_ATTR                8 (_saferepr)
#             824 LOAD_FAST                3 (@py_assert0)
#             826 CALL                     1
#             834 LOAD_CONST               9 ('header')
#             836 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             846 LOAD_ATTR               12 (locals)
#             866 CALL                     0
#             874 CONTAINS_OP              0
#             876 POP_JUMP_IF_TRUE        21 (to 920)
#             878 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             888 LOAD_ATTR               14 (_should_repr_global_name)
#             908 LOAD_FAST                2 (header)
#             910 CALL                     1
#             918 POP_JUMP_IF_FALSE       21 (to 962)
#         >>  920 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             930 LOAD_ATTR                8 (_saferepr)
#             950 LOAD_FAST                2 (header)
#             952 CALL                     1
#             960 JUMP_FORWARD             1 (to 964)
#         >>  962 LOAD_CONST               9 ('header')
#         >>  964 LOAD_CONST              10 (('py1', 'py3'))
#             966 BUILD_CONST_KEY_MAP      2
#             968 BINARY_OP                6 (%)
#             972 STORE_FAST               5 (@py_format4)
#             974 LOAD_CONST              11 ('assert %(py5)s')
#             976 LOAD_CONST              12 ('py5')
#             978 LOAD_FAST                5 (@py_format4)
#             980 BUILD_MAP                1
#             982 BINARY_OP                6 (%)
#             986 STORE_FAST               6 (@py_format6)
#             988 LOAD_GLOBAL             17 (NULL + AssertionError)
#             998 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#            1008 LOAD_ATTR               18 (_format_explanation)
#            1028 LOAD_FAST                6 (@py_format6)
#            1030 CALL                     1
#            1038 CALL                     1
#            1046 RAISE_VARARGS            1
#         >> 1048 LOAD_CONST               0 (None)
#            1050 COPY                     1
#            1052 STORE_FAST               3 (@py_assert0)
#            1054 STORE_FAST               4 (@py_assert2)
#            1056 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_format_timestamp at 0x3afa5570, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 47>:
#  47           0 RESUME                   0
# 
#  48           2 LOAD_GLOBAL              1 (NULL + ComtradeExportSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  49          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _format_timestamp)
#              44 LOAD_CONST               1 (1.5)
#              46 CALL                     1
#              54 STORE_FAST               2 (result)
# 
#  50          56 LOAD_CONST               2 ('1.5')
#              58 STORE_FAST               3 (@py_assert0)
#              60 LOAD_FAST                3 (@py_assert0)
#              62 LOAD_FAST                2 (result)
#              64 CONTAINS_OP              0
#              66 STORE_FAST               4 (@py_assert2)
#              68 LOAD_FAST                4 (@py_assert2)
#              70 POP_JUMP_IF_TRUE       153 (to 378)
#              72 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              82 LOAD_ATTR                6 (_call_reprcompare)
#             102 LOAD_CONST               3 (('in',))
#             104 LOAD_FAST                4 (@py_assert2)
#             106 BUILD_TUPLE              1
#             108 LOAD_CONST               4 (('%(py1)s in %(py3)s',))
#             110 LOAD_FAST                3 (@py_assert0)
#             112 LOAD_FAST                2 (result)
#             114 BUILD_TUPLE              2
#             116 CALL                     4
#             124 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             134 LOAD_ATTR                8 (_saferepr)
#             154 LOAD_FAST                3 (@py_assert0)
#             156 CALL                     1
#             164 LOAD_CONST               5 ('result')
#             166 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             176 LOAD_ATTR               12 (locals)
#             196 CALL                     0
#             204 CONTAINS_OP              0
#             206 POP_JUMP_IF_TRUE        21 (to 250)
#             208 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             218 LOAD_ATTR               14 (_should_repr_global_name)
#             238 LOAD_FAST                2 (result)
#             240 CALL                     1
#             248 POP_JUMP_IF_FALSE       21 (to 292)
#         >>  250 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             260 LOAD_ATTR                8 (_saferepr)
#             280 LOAD_FAST                2 (result)
#             282 CALL                     1
#             290 JUMP_FORWARD             1 (to 294)
#         >>  292 LOAD_CONST               5 ('result')
#         >>  294 LOAD_CONST               6 (('py1', 'py3'))
#             296 BUILD_CONST_KEY_MAP      2
#             298 BINARY_OP                6 (%)
#             302 STORE_FAST               5 (@py_format4)
#             304 LOAD_CONST               7 ('assert %(py5)s')
#             306 LOAD_CONST               8 ('py5')
#             308 LOAD_FAST                5 (@py_format4)
#             310 BUILD_MAP                1
#             312 BINARY_OP                6 (%)
#             316 STORE_FAST               6 (@py_format6)
#             318 LOAD_GLOBAL             17 (NULL + AssertionError)
#             328 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             338 LOAD_ATTR               18 (_format_explanation)
#             358 LOAD_FAST                6 (@py_format6)
#             360 CALL                     1
#             368 CALL                     1
#             376 RAISE_VARARGS            1
#         >>  378 LOAD_CONST               0 (None)
#             380 COPY                     1
#             382 STORE_FAST               3 (@py_assert0)
#             384 STORE_FAST               4 (@py_assert2)
#             386 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_generate_dat_record at 0x3afa6720, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 52>:
#  52           0 RESUME                   0
# 
#  53           2 LOAD_GLOBAL              1 (NULL + ComtradeExportSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  54          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _generate_dat_record)
#              44 BUILD_LIST               0
#              46 LOAD_CONST               1 ((100.0, 200.0, 300.0))
#              48 LIST_EXTEND              1
#              50 CALL                     1
#              58 STORE_FAST               2 (record)
# 
#  55          60 LOAD_GLOBAL              5 (NULL + isinstance)
#              70 LOAD_FAST                2 (record)
#              72 LOAD_GLOBAL              6 (bytes)
#              82 CALL                     2
#              90 STORE_FAST               3 (@py_assert3)
#              92 LOAD_FAST                3 (@py_assert3)
#              94 EXTENDED_ARG             1
#              96 POP_JUMP_IF_TRUE       267 (to 632)
#              98 LOAD_CONST               2 ('assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}')
#             100 LOAD_CONST               3 ('isinstance')
#             102 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             112 LOAD_ATTR               10 (locals)
#             132 CALL                     0
#             140 CONTAINS_OP              0
#             142 POP_JUMP_IF_TRUE        25 (to 194)
#             144 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             154 LOAD_ATTR               14 (_should_repr_global_name)
#             174 LOAD_GLOBAL              4 (isinstance)
#             184 CALL                     1
#             192 POP_JUMP_IF_FALSE       25 (to 244)
#         >>  194 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             204 LOAD_ATTR               16 (_saferepr)
#             224 LOAD_GLOBAL              4 (isinstance)
#             234 CALL                     1
#             242 JUMP_FORWARD             1 (to 246)
#         >>  244 LOAD_CONST               3 ('isinstance')
#         >>  246 LOAD_CONST               4 ('record')
#             248 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             258 LOAD_ATTR               10 (locals)
#             278 CALL                     0
#             286 CONTAINS_OP              0
#             288 POP_JUMP_IF_TRUE        21 (to 332)
#             290 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             300 LOAD_ATTR               14 (_should_repr_global_name)
#             320 LOAD_FAST                2 (record)
#             322 CALL                     1
#             330 POP_JUMP_IF_FALSE       21 (to 374)
#         >>  332 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             342 LOAD_ATTR               16 (_saferepr)
#             362 LOAD_FAST                2 (record)
#             364 CALL                     1
#             372 JUMP_FORWARD             1 (to 376)
#         >>  374 LOAD_CONST               4 ('record')
#         >>  376 LOAD_CONST               5 ('bytes')
#             378 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             388 LOAD_ATTR               10 (locals)
#             408 CALL                     0
#             416 CONTAINS_OP              0
#             418 POP_JUMP_IF_TRUE        25 (to 470)
#             420 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             430 LOAD_ATTR               14 (_should_repr_global_name)
#             450 LOAD_GLOBAL              6 (bytes)
#             460 CALL                     1
#             468 POP_JUMP_IF_FALSE       25 (to 520)
#         >>  470 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             480 LOAD_ATTR               16 (_saferepr)
#             500 LOAD_GLOBAL              6 (bytes)
#             510 CALL                     1
#             518 JUMP_FORWARD             1 (to 522)
#         >>  520 LOAD_CONST               5 ('bytes')
#         >>  522 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             532 LOAD_ATTR               16 (_saferepr)
#             552 LOAD_FAST                3 (@py_assert3)
#             554 CALL                     1
#             562 LOAD_CONST               6 (('py0', 'py1', 'py2', 'py4'))
#             564 BUILD_CONST_KEY_MAP      4
#             566 BINARY_OP                6 (%)
#             570 STORE_FAST               4 (@py_format5)
#             572 LOAD_GLOBAL             19 (NULL + AssertionError)
#             582 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             592 LOAD_ATTR               20 (_format_explanation)
#             612 LOAD_FAST                4 (@py_format5)
#             614 CALL                     1
#             622 CALL                     1
#             630 RAISE_VARARGS            1
#         >>  632 LOAD_CONST               0 (None)
#             634 STORE_FAST               3 (@py_assert3)
# 
#  56         636 LOAD_GLOBAL             23 (NULL + len)
#             646 LOAD_FAST                2 (record)
#             648 CALL                     1
#             656 STORE_FAST               5 (@py_assert2)
#             658 LOAD_CONST               7 (0)
#             660 STORE_FAST               6 (@py_assert5)
#             662 LOAD_FAST                5 (@py_assert2)
#             664 LOAD_FAST                6 (@py_assert5)
#             666 COMPARE_OP              68 (>)
#             670 STORE_FAST               7 (@py_assert4)
#             672 LOAD_FAST                7 (@py_assert4)
#             674 POP_JUMP_IF_TRUE       246 (to 1168)
#             676 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             686 LOAD_ATTR               24 (_call_reprcompare)
#             706 LOAD_CONST               8 (('>',))
#             708 LOAD_FAST                7 (@py_assert4)
#             710 BUILD_TUPLE              1
#             712 LOAD_CONST               9 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} > %(py6)s',))
#             714 LOAD_FAST                5 (@py_assert2)
#             716 LOAD_FAST                6 (@py_assert5)
#             718 BUILD_TUPLE              2
#             720 CALL                     4
#             728 LOAD_CONST              10 ('len')
#             730 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             740 LOAD_ATTR               10 (locals)
#             760 CALL                     0
#             768 CONTAINS_OP              0
#             770 POP_JUMP_IF_TRUE        25 (to 822)
#             772 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             782 LOAD_ATTR               14 (_should_repr_global_name)
#             802 LOAD_GLOBAL             22 (len)
#             812 CALL                     1
#             820 POP_JUMP_IF_FALSE       25 (to 872)
#         >>  822 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             832 LOAD_ATTR               16 (_saferepr)
#             852 LOAD_GLOBAL             22 (len)
#             862 CALL                     1
#             870 JUMP_FORWARD             1 (to 874)
#         >>  872 LOAD_CONST              10 ('len')
#         >>  874 LOAD_CONST               4 ('record')
#             876 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             886 LOAD_ATTR               10 (locals)
#             906 CALL                     0
#             914 CONTAINS_OP              0
#             916 POP_JUMP_IF_TRUE        21 (to 960)
#             918 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             928 LOAD_ATTR               14 (_should_repr_global_name)
#             948 LOAD_FAST                2 (record)
#             950 CALL                     1
#             958 POP_JUMP_IF_FALSE       21 (to 1002)
#         >>  960 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             970 LOAD_ATTR               16 (_saferepr)
#             990 LOAD_FAST                2 (record)
#             992 CALL                     1
#            1000 JUMP_FORWARD             1 (to 1004)
#         >> 1002 LOAD_CONST               4 ('record')
#         >> 1004 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1014 LOAD_ATTR               16 (_saferepr)
#            1034 LOAD_FAST                5 (@py_assert2)
#            1036 CALL                     1
#            1044 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1054 LOAD_ATTR               16 (_saferepr)
#            1074 LOAD_FAST                6 (@py_assert5)
#            1076 CALL                     1
#            1084 LOAD_CONST              11 (('py0', 'py1', 'py3', 'py6'))
#            1086 BUILD_CONST_KEY_MAP      4
#            1088 BINARY_OP                6 (%)
#            1092 STORE_FAST               8 (@py_format7)
#            1094 LOAD_CONST              12 ('assert %(py8)s')
#            1096 LOAD_CONST              13 ('py8')
#            1098 LOAD_FAST                8 (@py_format7)
#            1100 BUILD_MAP                1
#            1102 BINARY_OP                6 (%)
#            1106 STORE_FAST               9 (@py_format9)
#            1108 LOAD_GLOBAL             19 (NULL + AssertionError)
#            1118 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1128 LOAD_ATTR               20 (_format_explanation)
#            1148 LOAD_FAST                9 (@py_format9)
#            1150 CALL                     1
#            1158 CALL                     1
#            1166 RAISE_VARARGS            1
#         >> 1168 LOAD_CONST               0 (None)
#            1170 COPY                     1
#            1172 STORE_FAST               5 (@py_assert2)
#            1174 COPY                     1
#            1176 STORE_FAST               7 (@py_assert4)
#            1178 STORE_FAST               6 (@py_assert5)
#            1180 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestComtradeExportRun at 0x73cd945fea30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 59>:
#  59           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestComtradeExportRun')
#               8 STORE_NAME               2 (__qualname__)
# 
#  60          10 LOAD_CONST               1 ('Test run method.')
#              12 STORE_NAME               3 (__doc__)
# 
#  62          14 LOAD_CONST               2 (<code object test_run_invalid_config_returns_failure at 0x3afa4860, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 62>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_run_invalid_config_returns_failure)
# 
#  67          20 LOAD_CONST               3 (<code object test_run_valid_config_returns_success at 0x3afa99a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 67>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_run_valid_config_returns_success)
#              26 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_run_invalid_config_returns_failure at 0x3afa4860, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 62>:
#  62           0 RESUME                   0
# 
#  63           2 LOAD_GLOBAL              1 (NULL + ComtradeExportSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  64          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + run)
#              44 BUILD_MAP                0
#              46 CALL                     1
#              54 STORE_FAST               2 (result)
# 
#  65          56 LOAD_FAST                2 (result)
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
# Disassembly of <code object test_run_valid_config_returns_success at 0x3afa99a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_comtrade_export.py", line 67>:
#  67           0 RESUME                   0
# 
#  68           2 LOAD_GLOBAL              1 (NULL + ComtradeExportSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  70          22 LOAD_CONST               1 ('job_id')
#              24 LOAD_CONST               2 ('test_job')
#              26 BUILD_MAP                1
# 
#  71          28 LOAD_CONST               3 ('path')
#              30 LOAD_CONST               4 ('/tmp/test_comtrade')
#              32 BUILD_MAP                1
# 
#  69          34 LOAD_CONST               5 (('source', 'output'))
#              36 BUILD_CONST_KEY_MAP      2
#              38 STORE_FAST               2 (config)
# 
#  73          40 LOAD_FAST                1 (skill)
#              42 LOAD_ATTR                3 (NULL|self + run)
#              62 LOAD_FAST                2 (config)
#              64 CALL                     1
#              72 STORE_FAST               3 (result)
# 
#  74          74 LOAD_FAST                3 (result)
#              76 LOAD_ATTR                4 (status)
#              96 STORE_FAST               4 (@py_assert1)
#              98 LOAD_FAST                4 (@py_assert1)
#             100 LOAD_ATTR                6 (value)
#             120 STORE_FAST               5 (@py_assert3)
#             122 LOAD_CONST               6 ('SUCCESS')
#             124 LOAD_CONST               7 ('success')
#             126 BUILD_LIST               2
#             128 STORE_FAST               6 (@py_assert6)
#             130 LOAD_FAST                5 (@py_assert3)
#             132 LOAD_FAST                6 (@py_assert6)
#             134 CONTAINS_OP              0
#             136 STORE_FAST               7 (@py_assert5)
#             138 LOAD_FAST                7 (@py_assert5)
#             140 POP_JUMP_IF_TRUE       193 (to 528)
#             142 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             152 LOAD_ATTR               10 (_call_reprcompare)
#             172 LOAD_CONST               8 (('in',))
#             174 LOAD_FAST                7 (@py_assert5)
#             176 BUILD_TUPLE              1
#             178 LOAD_CONST               9 (('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.status\n}.value\n} in %(py7)s',))
#             180 LOAD_FAST                5 (@py_assert3)
#             182 LOAD_FAST                6 (@py_assert6)
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
#             268 LOAD_FAST                3 (result)
#             270 CALL                     1
#             278 POP_JUMP_IF_FALSE       21 (to 322)
#         >>  280 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             290 LOAD_ATTR               18 (_saferepr)
#             310 LOAD_FAST                3 (result)
#             312 CALL                     1
#             320 JUMP_FORWARD             1 (to 324)
#         >>  322 LOAD_CONST              10 ('result')
#         >>  324 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             334 LOAD_ATTR               18 (_saferepr)
#             354 LOAD_FAST                4 (@py_assert1)
#             356 CALL                     1
#             364 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             374 LOAD_ATTR               18 (_saferepr)
#             394 LOAD_FAST                5 (@py_assert3)
#             396 CALL                     1
#             404 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             414 LOAD_ATTR               18 (_saferepr)
#             434 LOAD_FAST                6 (@py_assert6)
#             436 CALL                     1
#             444 LOAD_CONST              11 (('py0', 'py2', 'py4', 'py7'))
#             446 BUILD_CONST_KEY_MAP      4
#             448 BINARY_OP                6 (%)
#             452 STORE_FAST               8 (@py_format8)
#             454 LOAD_CONST              12 ('assert %(py9)s')
#             456 LOAD_CONST              13 ('py9')
#             458 LOAD_FAST                8 (@py_format8)
#             460 BUILD_MAP                1
#             462 BINARY_OP                6 (%)
#             466 STORE_FAST               9 (@py_format10)
#             468 LOAD_GLOBAL             21 (NULL + AssertionError)
#             478 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             488 LOAD_ATTR               22 (_format_explanation)
#             508 LOAD_FAST                9 (@py_format10)
#             510 CALL                     1
#             518 CALL                     1
#             526 RAISE_VARARGS            1
#         >>  528 LOAD_CONST               0 (None)
#             530 COPY                     1
#             532 STORE_FAST               4 (@py_assert1)
#             534 COPY                     1
#             536 STORE_FAST               5 (@py_assert3)
#             538 COPY                     1
#             540 STORE_FAST               7 (@py_assert5)
#             542 STORE_FAST               6 (@py_assert6)
# 
#  75         544 LOAD_FAST                3 (result)
#             546 LOAD_ATTR               24 (artifacts)
#             566 STORE_FAST              10 (@py_assert2)
#             568 LOAD_GLOBAL             27 (NULL + len)
#             578 LOAD_FAST               10 (@py_assert2)
#             580 CALL                     1
#             588 STORE_FAST              11 (@py_assert4)
#             590 LOAD_CONST              14 (0)
#             592 STORE_FAST              12 (@py_assert7)
#             594 LOAD_FAST               11 (@py_assert4)
#             596 LOAD_FAST               12 (@py_assert7)
#             598 COMPARE_OP              68 (>)
#             602 STORE_FAST               6 (@py_assert6)
#             604 LOAD_FAST                6 (@py_assert6)
#             606 EXTENDED_ARG             1
#             608 POP_JUMP_IF_TRUE       266 (to 1142)
#             610 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             620 LOAD_ATTR               10 (_call_reprcompare)
#             640 LOAD_CONST              15 (('>',))
#             642 LOAD_FAST                6 (@py_assert6)
#             644 BUILD_TUPLE              1
#             646 LOAD_CONST              16 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.artifacts\n})\n} > %(py8)s',))
#             648 LOAD_FAST               11 (@py_assert4)
#             650 LOAD_FAST               12 (@py_assert7)
#             652 BUILD_TUPLE              2
#             654 CALL                     4
#             662 LOAD_CONST              17 ('len')
#             664 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             674 LOAD_ATTR               14 (locals)
#             694 CALL                     0
#             702 CONTAINS_OP              0
#             704 POP_JUMP_IF_TRUE        25 (to 756)
#             706 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             716 LOAD_ATTR               16 (_should_repr_global_name)
#             736 LOAD_GLOBAL             26 (len)
#             746 CALL                     1
#             754 POP_JUMP_IF_FALSE       25 (to 806)
#         >>  756 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             766 LOAD_ATTR               18 (_saferepr)
#             786 LOAD_GLOBAL             26 (len)
#             796 CALL                     1
#             804 JUMP_FORWARD             1 (to 808)
#         >>  806 LOAD_CONST              17 ('len')
#         >>  808 LOAD_CONST              10 ('result')
#             810 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             820 LOAD_ATTR               14 (locals)
#             840 CALL                     0
#             848 CONTAINS_OP              0
#             850 POP_JUMP_IF_TRUE        21 (to 894)
#             852 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             862 LOAD_ATTR               16 (_should_repr_global_name)
#             882 LOAD_FAST                3 (result)
#             884 CALL                     1
#             892 POP_JUMP_IF_FALSE       21 (to 936)
#         >>  894 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             904 LOAD_ATTR               18 (_saferepr)
#             924 LOAD_FAST                3 (result)
#             926 CALL                     1
#             934 JUMP_FORWARD             1 (to 938)
#         >>  936 LOAD_CONST              10 ('result')
#         >>  938 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             948 LOAD_ATTR               18 (_saferepr)
#             968 LOAD_FAST               10 (@py_assert2)
#             970 CALL                     1
#             978 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             988 LOAD_ATTR               18 (_saferepr)
#            1008 LOAD_FAST               11 (@py_assert4)
#            1010 CALL                     1
#            1018 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1028 LOAD_ATTR               18 (_saferepr)
#            1048 LOAD_FAST               12 (@py_assert7)
#            1050 CALL                     1
#            1058 LOAD_CONST              18 (('py0', 'py1', 'py3', 'py5', 'py8'))
#            1060 BUILD_CONST_KEY_MAP      5
#            1062 BINARY_OP                6 (%)
#            1066 STORE_FAST              13 (@py_format9)
#            1068 LOAD_CONST              19 ('assert %(py10)s')
#            1070 LOAD_CONST              20 ('py10')
#            1072 LOAD_FAST               13 (@py_format9)
#            1074 BUILD_MAP                1
#            1076 BINARY_OP                6 (%)
#            1080 STORE_FAST              14 (@py_format11)
#            1082 LOAD_GLOBAL             21 (NULL + AssertionError)
#            1092 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#            1102 LOAD_ATTR               22 (_format_explanation)
#            1122 LOAD_FAST               14 (@py_format11)
#            1124 CALL                     1
#            1132 CALL                     1
#            1140 RAISE_VARARGS            1
#         >> 1142 LOAD_CONST               0 (None)
#            1144 COPY                     1
#            1146 STORE_FAST              10 (@py_assert2)
#            1148 COPY                     1
#            1150 STORE_FAST              11 (@py_assert4)
#            1152 COPY                     1
#            1154 STORE_FAST               6 (@py_assert6)
#            1156 STORE_FAST              12 (@py_assert7)
# 
#  76        1158 LOAD_FAST                3 (result)
#            1160 LOAD_ATTR               24 (artifacts)
#            1180 GET_ITER
#            1182 LOAD_FAST_AND_CLEAR     15 (a)
#            1184 SWAP                     2
#            1186 BUILD_LIST               0
#            1188 SWAP                     2
#         >> 1190 FOR_ITER                14 (to 1222)
#            1194 STORE_FAST              15 (a)
#            1196 LOAD_FAST               15 (a)
#            1198 LOAD_ATTR               28 (name)
#            1218 LIST_APPEND              2
#            1220 JUMP_BACKWARD           16 (to 1190)
#         >> 1222 END_FOR
#            1224 STORE_FAST              16 (artifact_names)
#            1226 STORE_FAST              15 (a)
# 
#  77        1228 BUILD_LIST               0
#            1230 STORE_FAST               4 (@py_assert1)
# 
#  78        1232 LOAD_CONST              21 ('artifact')
# 
#  77        1234 STORE_FAST              10 (@py_assert2)
# 
#  78        1236 LOAD_CONST              22 (' ')
# 
#  77        1238 STORE_FAST               7 (@py_assert5)
# 
#  78        1240 LOAD_FAST                7 (@py_assert5)
#            1242 LOAD_ATTR               30 (join)
# 
#  77        1262 STORE_FAST              12 (@py_assert7)
# 
#  78        1264 PUSH_NULL
#            1266 LOAD_FAST               12 (@py_assert7)
#            1268 LOAD_FAST               16 (artifact_names)
#            1270 CALL                     1
# 
#  77        1278 STORE_FAST              17 (@py_assert10)
# 
#  78        1280 LOAD_FAST               17 (@py_assert10)
#            1282 LOAD_ATTR               32 (lower)
# 
#  77        1302 STORE_FAST              18 (@py_assert12)
# 
#  78        1304 PUSH_NULL
#            1306 LOAD_FAST               18 (@py_assert12)
#            1308 CALL                     0
# 
#  77        1316 STORE_FAST              19 (@py_assert14)
# 
#  78        1318 LOAD_FAST               10 (@py_assert2)
#            1320 LOAD_FAST               19 (@py_assert14)
#            1322 CONTAINS_OP              0
# 
#  77        1324 STORE_FAST              11 (@py_assert4)
#            1326 LOAD_FAST               11 (@py_assert4)
#            1328 STORE_FAST              20 (@py_assert0)
#            1330 LOAD_FAST               11 (@py_assert4)
#            1332 POP_JUMP_IF_TRUE        32 (to 1398)
# 
#  78        1334 LOAD_FAST                3 (result)
#            1336 LOAD_ATTR               24 (artifacts)
# 
#  77        1356 STORE_FAST              21 (@py_assert21)
# 
#  78        1358 LOAD_GLOBAL             27 (NULL + len)
#            1368 LOAD_FAST               21 (@py_assert21)
#            1370 CALL                     1
# 
#  77        1378 STORE_FAST              22 (@py_assert23)
# 
#  78        1380 LOAD_CONST              23 (3)
# 
#  77        1382 STORE_FAST              23 (@py_assert26)
# 
#  78        1384 LOAD_FAST               22 (@py_assert23)
#            1386 LOAD_FAST               23 (@py_assert26)
#            1388 COMPARE_OP              92 (>=)
# 
#  77        1392 STORE_FAST              24 (@py_assert25)
#            1394 LOAD_FAST               24 (@py_assert25)
#            1396 STORE_FAST              20 (@py_assert0)
#         >> 1398 LOAD_FAST               20 (@py_assert0)
#            1400 EXTENDED_ARG             2
#            1402 POP_JUMP_IF_TRUE       557 (to 2518)
#            1404 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        1414 LOAD_ATTR               10 (_call_reprcompare)
# 
#  77        1434 LOAD_CONST               8 (('in',))
#            1436 LOAD_FAST               11 (@py_assert4)
#            1438 BUILD_TUPLE              1
#            1440 LOAD_CONST              24 (('%(py3)s in %(py15)s\n{%(py15)s = %(py13)s\n{%(py13)s = %(py11)s\n{%(py11)s = %(py8)s\n{%(py8)s = %(py6)s.join\n}(%(py9)s)\n}.lower\n}()\n}',))
# 
#  78        1442 LOAD_FAST               10 (@py_assert2)
#            1444 LOAD_FAST               19 (@py_assert14)
# 
#  77        1446 BUILD_TUPLE              2
#            1448 CALL                     4
#            1456 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        1466 LOAD_ATTR               18 (_saferepr)
# 
#  78        1486 LOAD_FAST               10 (@py_assert2)
# 
#  77        1488 CALL                     1
#            1496 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        1506 LOAD_ATTR               18 (_saferepr)
# 
#  78        1526 LOAD_FAST                7 (@py_assert5)
# 
#  77        1528 CALL                     1
#            1536 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        1546 LOAD_ATTR               18 (_saferepr)
# 
#  78        1566 LOAD_FAST               12 (@py_assert7)
# 
#  77        1568 CALL                     1
#            1576 LOAD_CONST              25 ('artifact_names')
#            1578 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
#  79        1588 LOAD_ATTR               14 (locals)
# 
#  77        1608 CALL                     0
#            1616 CONTAINS_OP              0
#            1618 POP_JUMP_IF_TRUE        21 (to 1662)
#            1620 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        1630 LOAD_ATTR               16 (_should_repr_global_name)
# 
#  78        1650 LOAD_FAST               16 (artifact_names)
# 
#  77        1652 CALL                     1
#            1660 POP_JUMP_IF_FALSE       21 (to 1704)
#         >> 1662 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        1672 LOAD_ATTR               18 (_saferepr)
# 
#  78        1692 LOAD_FAST               16 (artifact_names)
# 
#  77        1694 CALL                     1
#            1702 JUMP_FORWARD             1 (to 1706)
#         >> 1704 LOAD_CONST              25 ('artifact_names')
#         >> 1706 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        1716 LOAD_ATTR               18 (_saferepr)
# 
#  78        1736 LOAD_FAST               17 (@py_assert10)
# 
#  77        1738 CALL                     1
#            1746 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        1756 LOAD_ATTR               18 (_saferepr)
# 
#  78        1776 LOAD_FAST               18 (@py_assert12)
# 
#  77        1778 CALL                     1
#            1786 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        1796 LOAD_ATTR               18 (_saferepr)
# 
#  78        1816 LOAD_FAST               19 (@py_assert14)
# 
#  77        1818 CALL                     1
#            1826 LOAD_CONST              26 (('py3', 'py6', 'py8', 'py9', 'py11', 'py13', 'py15'))
#            1828 BUILD_CONST_KEY_MAP      7
#            1830 BINARY_OP                6 (%)
#            1834 STORE_FAST              25 (@py_format16)
#            1836 LOAD_CONST              27 ('%(py17)s')
#            1838 LOAD_CONST              28 ('py17')
#            1840 LOAD_FAST               25 (@py_format16)
#            1842 BUILD_MAP                1
#            1844 BINARY_OP                6 (%)
#            1848 STORE_FAST              26 (@py_format18)
#            1850 LOAD_FAST                4 (@py_assert1)
# 
#  79        1852 LOAD_ATTR               35 (NULL|self + append)
# 
#  77        1872 LOAD_FAST               26 (@py_format18)
# 
#  79        1874 CALL                     1
#            1882 POP_TOP
# 
#  77        1884 LOAD_FAST               11 (@py_assert4)
#            1886 POP_JUMP_IF_TRUE       253 (to 2394)
#            1888 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        1898 LOAD_ATTR               10 (_call_reprcompare)
# 
#  77        1918 LOAD_CONST              29 (('>=',))
#            1920 LOAD_FAST_CHECK         24 (@py_assert25)
#            1922 BUILD_TUPLE              1
#            1924 LOAD_CONST              30 (('%(py24)s\n{%(py24)s = %(py19)s(%(py22)s\n{%(py22)s = %(py20)s.artifacts\n})\n} >= %(py27)s',))
# 
#  78        1926 LOAD_FAST_CHECK         22 (@py_assert23)
#            1928 LOAD_FAST_CHECK         23 (@py_assert26)
# 
#  77        1930 BUILD_TUPLE              2
#            1932 CALL                     4
#            1940 LOAD_CONST              17 ('len')
#            1942 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
#  79        1952 LOAD_ATTR               14 (locals)
# 
#  77        1972 CALL                     0
#            1980 CONTAINS_OP              0
#            1982 POP_JUMP_IF_TRUE        25 (to 2034)
#            1984 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        1994 LOAD_ATTR               16 (_should_repr_global_name)
# 
#  78        2014 LOAD_GLOBAL             26 (len)
# 
#  77        2024 CALL                     1
#            2032 POP_JUMP_IF_FALSE       25 (to 2084)
#         >> 2034 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        2044 LOAD_ATTR               18 (_saferepr)
# 
#  78        2064 LOAD_GLOBAL             26 (len)
# 
#  77        2074 CALL                     1
#            2082 JUMP_FORWARD             1 (to 2086)
#         >> 2084 LOAD_CONST              17 ('len')
#         >> 2086 LOAD_CONST              10 ('result')
#            2088 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
#  79        2098 LOAD_ATTR               14 (locals)
# 
#  77        2118 CALL                     0
#            2126 CONTAINS_OP              0
#            2128 POP_JUMP_IF_TRUE        21 (to 2172)
#            2130 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        2140 LOAD_ATTR               16 (_should_repr_global_name)
# 
#  78        2160 LOAD_FAST                3 (result)
# 
#  77        2162 CALL                     1
#            2170 POP_JUMP_IF_FALSE       21 (to 2214)
#         >> 2172 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        2182 LOAD_ATTR               18 (_saferepr)
# 
#  78        2202 LOAD_FAST                3 (result)
# 
#  77        2204 CALL                     1
#            2212 JUMP_FORWARD             1 (to 2216)
#         >> 2214 LOAD_CONST              10 ('result')
#         >> 2216 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        2226 LOAD_ATTR               18 (_saferepr)
# 
#  78        2246 LOAD_FAST_CHECK         21 (@py_assert21)
# 
#  77        2248 CALL                     1
#            2256 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        2266 LOAD_ATTR               18 (_saferepr)
# 
#  78        2286 LOAD_FAST               22 (@py_assert23)
# 
#  77        2288 CALL                     1
#            2296 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        2306 LOAD_ATTR               18 (_saferepr)
# 
#  78        2326 LOAD_FAST               23 (@py_assert26)
# 
#  77        2328 CALL                     1
#            2336 LOAD_CONST              31 (('py19', 'py20', 'py22', 'py24', 'py27'))
#            2338 BUILD_CONST_KEY_MAP      5
#            2340 BINARY_OP                6 (%)
#            2344 STORE_FAST              27 (@py_format28)
#            2346 LOAD_CONST              32 ('%(py29)s')
#            2348 LOAD_CONST              33 ('py29')
#            2350 LOAD_FAST               27 (@py_format28)
#            2352 BUILD_MAP                1
#            2354 BINARY_OP                6 (%)
#            2358 STORE_FAST              28 (@py_format30)
#            2360 LOAD_FAST                4 (@py_assert1)
# 
#  79        2362 LOAD_ATTR               35 (NULL|self + append)
# 
#  77        2382 LOAD_FAST               28 (@py_format30)
# 
#  79        2384 CALL                     1
#            2392 POP_TOP
# 
#  77     >> 2394 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        2404 LOAD_ATTR               36 (_format_boolop)
# 
#  77        2424 LOAD_FAST                4 (@py_assert1)
#            2426 LOAD_CONST              34 (1)
#            2428 CALL                     2
#            2436 BUILD_MAP                0
#            2438 BINARY_OP                6 (%)
#            2442 STORE_FAST              29 (@py_format31)
#            2444 LOAD_CONST              35 ('assert %(py32)s')
#            2446 LOAD_CONST              36 ('py32')
#            2448 LOAD_FAST               29 (@py_format31)
#            2450 BUILD_MAP                1
#            2452 BINARY_OP                6 (%)
#            2456 STORE_FAST              30 (@py_format33)
#            2458 LOAD_GLOBAL             21 (NULL + AssertionError)
#            2468 LOAD_GLOBAL              9 (NULL + @pytest_ar)
# 
#  79        2478 LOAD_ATTR               22 (_format_explanation)
# 
#  77        2498 LOAD_FAST               30 (@py_format33)
#            2500 CALL                     1
#            2508 CALL                     1
#            2516 RAISE_VARARGS            1
#         >> 2518 LOAD_CONST               0 (None)
#            2520 COPY                     1
#            2522 STORE_FAST              20 (@py_assert0)
#            2524 COPY                     1
#            2526 STORE_FAST               4 (@py_assert1)
#            2528 COPY                     1
#            2530 STORE_FAST              10 (@py_assert2)
#            2532 COPY                     1
#            2534 STORE_FAST              11 (@py_assert4)
#            2536 COPY                     1
#            2538 STORE_FAST               7 (@py_assert5)
#            2540 COPY                     1
#            2542 STORE_FAST              12 (@py_assert7)
#            2544 COPY                     1
#            2546 STORE_FAST              17 (@py_assert10)
#            2548 COPY                     1
#            2550 STORE_FAST              18 (@py_assert12)
#            2552 COPY                     1
#            2554 STORE_FAST              19 (@py_assert14)
#            2556 COPY                     1
#            2558 STORE_FAST              21 (@py_assert21)
#            2560 COPY                     1
#            2562 STORE_FAST              22 (@py_assert23)
#            2564 COPY                     1
#            2566 STORE_FAST              24 (@py_assert25)
#            2568 STORE_FAST              23 (@py_assert26)
#            2570 RETURN_CONST             0 (None)
#         >> 2572 SWAP                     2
#            2574 POP_TOP
# 
#  76        2576 SWAP                     2
#            2578 STORE_FAST              15 (a)
#            2580 RERAISE                  0
# ExceptionTable:
#   1186 to 1222 -> 2572 [2]
# 