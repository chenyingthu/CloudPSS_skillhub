# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/__pycache__/test_result_compare.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


def TestResultCompareValidate():
    """TestResultCompareValidate"""
pass  # TODO: restore


def TestResultCompareRun():
    """TestResultCompareRun"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('Tests for result_compare skill (v2 pattern).')
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
#              54 LOAD_CONST               4 (('ResultCompareSkill',))
#              56 IMPORT_NAME             10 (cloudpss_skills_v2.skills.result_compare)
#              58 IMPORT_FROM             11 (ResultCompareSkill)
#              60 STORE_NAME              11 (ResultCompareSkill)
#              62 POP_TOP
# 
#   8          64 PUSH_NULL
#              66 LOAD_BUILD_CLASS
#              68 LOAD_CONST               5 (<code object TestResultCompareValidate at 0x73cd93b066a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 8>)
#              70 MAKE_FUNCTION            0
#              72 LOAD_CONST               6 ('TestResultCompareValidate')
#              74 CALL                     2
#              82 STORE_NAME              12 (TestResultCompareValidate)
# 
#  43          84 PUSH_NULL
#              86 LOAD_BUILD_CLASS
#              88 LOAD_CONST               7 (<code object TestResultCompareRun at 0x73cd93b065b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 43>)
#              90 MAKE_FUNCTION            0
#              92 LOAD_CONST               8 ('TestResultCompareRun')
#              94 CALL                     2
#             102 STORE_NAME              13 (TestResultCompareRun)
#             104 RETURN_CONST             2 (None)
# 
# Disassembly of <code object TestResultCompareValidate at 0x73cd93b066a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 8>:
#   8           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestResultCompareValidate')
#               8 STORE_NAME               2 (__qualname__)
# 
#   9          10 LOAD_CONST               1 (<code object test_valid_config at 0x3aeff050, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 9>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_valid_config)
# 
#  21          16 LOAD_CONST               2 (<code object test_missing_sources at 0x3af9bd40, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 21>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_missing_sources)
# 
#  27          22 LOAD_CONST               3 (<code object test_single_source at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 27>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_single_source)
# 
#  32          28 LOAD_CONST               4 (<code object test_invalid_time_range at 0x3afa5260, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 32>)
#              30 MAKE_FUNCTION            0
#              32 STORE_NAME               6 (test_invalid_time_range)
#              34 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_valid_config at 0x3aeff050, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 9>:
#   9           0 RESUME                   0
# 
#  10           2 LOAD_GLOBAL              1 (NULL + ResultCompareSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  12          22 LOAD_CONST               1 ('job1')
#              24 LOAD_CONST               2 ('job2')
#              26 BUILD_LIST               2
# 
#  14          28 LOAD_CONST               3 ('metrics')
#              30 LOAD_CONST               4 (10)
#              32 LOAD_CONST               5 (1)
#              34 LOAD_CONST               6 (5)
#              36 LOAD_CONST               7 (2)
#              38 LOAD_CONST               8 (('max', 'min', 'mean', 'rms'))
#              40 BUILD_CONST_KEY_MAP      4
#              42 BUILD_MAP                1
# 
#  15          44 LOAD_CONST               3 ('metrics')
#              46 LOAD_CONST               9 (8)
#              48 LOAD_CONST              10 (0)
#              50 LOAD_CONST              11 (4)
#              52 LOAD_CONST              12 (1.5)
#              54 LOAD_CONST               8 (('max', 'min', 'mean', 'rms'))
#              56 BUILD_CONST_KEY_MAP      4
#              58 BUILD_MAP                1
# 
#  13          60 LOAD_CONST              13 (('job1', 'job2'))
#              62 BUILD_CONST_KEY_MAP      2
# 
#  11          64 LOAD_CONST              14 (('job_ids', 'results_by_job'))
#              66 BUILD_CONST_KEY_MAP      2
#              68 STORE_FAST               2 (config)
# 
#  18          70 LOAD_FAST                1 (skill)
#              72 LOAD_ATTR                3 (NULL|self + validate)
#              92 LOAD_FAST                2 (config)
#              94 CALL                     1
#             102 UNPACK_SEQUENCE          2
#             106 STORE_FAST               3 (valid)
#             108 STORE_FAST               4 (errors)
# 
#  19         110 LOAD_CONST              15 (True)
#             112 STORE_FAST               5 (@py_assert2)
#             114 LOAD_FAST                3 (valid)
#             116 LOAD_FAST                5 (@py_assert2)
#             118 IS_OP                    0
#             120 STORE_FAST               6 (@py_assert1)
#             122 LOAD_FAST                6 (@py_assert1)
#             124 POP_JUMP_IF_TRUE       153 (to 432)
#             126 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             136 LOAD_ATTR                6 (_call_reprcompare)
#             156 LOAD_CONST              16 (('is',))
#             158 LOAD_FAST                6 (@py_assert1)
#             160 BUILD_TUPLE              1
#             162 LOAD_CONST              17 (('%(py0)s is %(py3)s',))
#             164 LOAD_FAST                3 (valid)
#             166 LOAD_FAST                5 (@py_assert2)
#             168 BUILD_TUPLE              2
#             170 CALL                     4
#             178 LOAD_CONST              18 ('valid')
#             180 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             190 LOAD_ATTR               10 (locals)
#             210 CALL                     0
#             218 CONTAINS_OP              0
#             220 POP_JUMP_IF_TRUE        21 (to 264)
#             222 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             232 LOAD_ATTR               12 (_should_repr_global_name)
#             252 LOAD_FAST                3 (valid)
#             254 CALL                     1
#             262 POP_JUMP_IF_FALSE       21 (to 306)
#         >>  264 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             274 LOAD_ATTR               14 (_saferepr)
#             294 LOAD_FAST                3 (valid)
#             296 CALL                     1
#             304 JUMP_FORWARD             1 (to 308)
#         >>  306 LOAD_CONST              18 ('valid')
#         >>  308 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             318 LOAD_ATTR               14 (_saferepr)
#             338 LOAD_FAST                5 (@py_assert2)
#             340 CALL                     1
#             348 LOAD_CONST              19 (('py0', 'py3'))
#             350 BUILD_CONST_KEY_MAP      2
#             352 BINARY_OP                6 (%)
#             356 STORE_FAST               7 (@py_format4)
#             358 LOAD_CONST              20 ('assert %(py5)s')
#             360 LOAD_CONST              21 ('py5')
#             362 LOAD_FAST                7 (@py_format4)
#             364 BUILD_MAP                1
#             366 BINARY_OP                6 (%)
#             370 STORE_FAST               8 (@py_format6)
#             372 LOAD_GLOBAL             17 (NULL + AssertionError)
#             382 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             392 LOAD_ATTR               18 (_format_explanation)
#             412 LOAD_FAST                8 (@py_format6)
#             414 CALL                     1
#             422 CALL                     1
#             430 RAISE_VARARGS            1
#         >>  432 LOAD_CONST               0 (None)
#             434 COPY                     1
#             436 STORE_FAST               6 (@py_assert1)
#             438 STORE_FAST               5 (@py_assert2)
#             440 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_missing_sources at 0x3af9bd40, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 21>:
#  21           0 RESUME                   0
# 
#  22           2 LOAD_GLOBAL              1 (NULL + ResultCompareSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  23          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + validate)
#              44 BUILD_MAP                0
#              46 CALL                     1
#              54 UNPACK_SEQUENCE          2
#              58 STORE_FAST               2 (valid)
#              60 STORE_FAST               3 (errors)
# 
#  24          62 LOAD_CONST               1 (False)
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
#  25         392 LOAD_CONST               8 (<code object <genexpr> at 0x73cd93b06880, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 25>)
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
# Disassembly of <code object <genexpr> at 0x73cd93b06880, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 25>:
#  25           0 RETURN_GENERATOR
#               2 POP_TOP
#               4 RESUME                   0
#               6 LOAD_FAST                0 (.0)
#         >>    8 FOR_ITER                 8 (to 28)
#              12 STORE_FAST               1 (e)
#              14 LOAD_CONST               0 ('2 sources')
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
# Disassembly of <code object test_single_source at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 27>:
#  27           0 RESUME                   0
# 
#  28           2 LOAD_GLOBAL              1 (NULL + ResultCompareSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  29          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + validate)
#              44 LOAD_CONST               1 ('job_ids')
#              46 LOAD_CONST               2 ('only_one')
#              48 BUILD_LIST               1
#              50 BUILD_MAP                1
#              52 CALL                     1
#              60 UNPACK_SEQUENCE          2
#              64 STORE_FAST               2 (valid)
#              66 STORE_FAST               3 (errors)
# 
#  30          68 LOAD_CONST               3 (False)
#              70 STORE_FAST               4 (@py_assert2)
#              72 LOAD_FAST                2 (valid)
#              74 LOAD_FAST                4 (@py_assert2)
#              76 IS_OP                    0
#              78 STORE_FAST               5 (@py_assert1)
#              80 LOAD_FAST                5 (@py_assert1)
#              82 POP_JUMP_IF_TRUE       153 (to 390)
#              84 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              94 LOAD_ATTR                6 (_call_reprcompare)
#             114 LOAD_CONST               4 (('is',))
#             116 LOAD_FAST                5 (@py_assert1)
#             118 BUILD_TUPLE              1
#             120 LOAD_CONST               5 (('%(py0)s is %(py3)s',))
#             122 LOAD_FAST                2 (valid)
#             124 LOAD_FAST                4 (@py_assert2)
#             126 BUILD_TUPLE              2
#             128 CALL                     4
#             136 LOAD_CONST               6 ('valid')
#             138 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             148 LOAD_ATTR               10 (locals)
#             168 CALL                     0
#             176 CONTAINS_OP              0
#             178 POP_JUMP_IF_TRUE        21 (to 222)
#             180 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             190 LOAD_ATTR               12 (_should_repr_global_name)
#             210 LOAD_FAST                2 (valid)
#             212 CALL                     1
#             220 POP_JUMP_IF_FALSE       21 (to 264)
#         >>  222 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             232 LOAD_ATTR               14 (_saferepr)
#             252 LOAD_FAST                2 (valid)
#             254 CALL                     1
#             262 JUMP_FORWARD             1 (to 266)
#         >>  264 LOAD_CONST               6 ('valid')
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
#             398 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_invalid_time_range at 0x3afa5260, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 32>:
#  32           0 RESUME                   0
# 
#  33           2 LOAD_GLOBAL              1 (NULL + ResultCompareSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  35          22 LOAD_CONST               1 ('j1')
#              24 LOAD_CONST               2 ('j2')
#              26 BUILD_LIST               2
# 
#  36          28 LOAD_CONST               3 ('time_range')
#              30 LOAD_CONST               4 (5)
#              32 LOAD_CONST               5 (3)
#              34 LOAD_CONST               6 (('start', 'end'))
#              36 BUILD_CONST_KEY_MAP      2
#              38 BUILD_MAP                1
# 
#  34          40 LOAD_CONST               7 (('job_ids', 'compare'))
#              42 BUILD_CONST_KEY_MAP      2
#              44 STORE_FAST               2 (config)
# 
#  38          46 LOAD_FAST                1 (skill)
#              48 LOAD_ATTR                3 (NULL|self + validate)
#              68 LOAD_FAST                2 (config)
#              70 CALL                     1
#              78 UNPACK_SEQUENCE          2
#              82 STORE_FAST               3 (valid)
#              84 STORE_FAST               4 (errors)
# 
#  39          86 LOAD_CONST               8 (False)
#              88 STORE_FAST               5 (@py_assert2)
#              90 LOAD_FAST                3 (valid)
#              92 LOAD_FAST                5 (@py_assert2)
#              94 IS_OP                    0
#              96 STORE_FAST               6 (@py_assert1)
#              98 LOAD_FAST                6 (@py_assert1)
#             100 POP_JUMP_IF_TRUE       153 (to 408)
#             102 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             112 LOAD_ATTR                6 (_call_reprcompare)
#             132 LOAD_CONST               9 (('is',))
#             134 LOAD_FAST                6 (@py_assert1)
#             136 BUILD_TUPLE              1
#             138 LOAD_CONST              10 (('%(py0)s is %(py3)s',))
#             140 LOAD_FAST                3 (valid)
#             142 LOAD_FAST                5 (@py_assert2)
#             144 BUILD_TUPLE              2
#             146 CALL                     4
#             154 LOAD_CONST              11 ('valid')
#             156 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             166 LOAD_ATTR               10 (locals)
#             186 CALL                     0
#             194 CONTAINS_OP              0
#             196 POP_JUMP_IF_TRUE        21 (to 240)
#             198 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             208 LOAD_ATTR               12 (_should_repr_global_name)
#             228 LOAD_FAST                3 (valid)
#             230 CALL                     1
#             238 POP_JUMP_IF_FALSE       21 (to 282)
#         >>  240 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             250 LOAD_ATTR               14 (_saferepr)
#             270 LOAD_FAST                3 (valid)
#             272 CALL                     1
#             280 JUMP_FORWARD             1 (to 284)
#         >>  282 LOAD_CONST              11 ('valid')
#         >>  284 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             294 LOAD_ATTR               14 (_saferepr)
#             314 LOAD_FAST                5 (@py_assert2)
#             316 CALL                     1
#             324 LOAD_CONST              12 (('py0', 'py3'))
#             326 BUILD_CONST_KEY_MAP      2
#             328 BINARY_OP                6 (%)
#             332 STORE_FAST               7 (@py_format4)
#             334 LOAD_CONST              13 ('assert %(py5)s')
#             336 LOAD_CONST              14 ('py5')
#             338 LOAD_FAST                7 (@py_format4)
#             340 BUILD_MAP                1
#             342 BINARY_OP                6 (%)
#             346 STORE_FAST               8 (@py_format6)
#             348 LOAD_GLOBAL             17 (NULL + AssertionError)
#             358 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             368 LOAD_ATTR               18 (_format_explanation)
#             388 LOAD_FAST                8 (@py_format6)
#             390 CALL                     1
#             398 CALL                     1
#             406 RAISE_VARARGS            1
#         >>  408 LOAD_CONST               0 (None)
#             410 COPY                     1
#             412 STORE_FAST               6 (@py_assert1)
#             414 STORE_FAST               5 (@py_assert2)
# 
#  40         416 LOAD_CONST              15 (<code object <genexpr> at 0x73cd93b06790, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 40>)
#             418 MAKE_FUNCTION            0
#             420 LOAD_FAST                4 (errors)
#             422 GET_ITER
#             424 CALL                     0
#             432 STORE_FAST               6 (@py_assert1)
#             434 LOAD_GLOBAL             21 (NULL + any)
#             444 LOAD_FAST                6 (@py_assert1)
#             446 CALL                     1
#             454 STORE_FAST               9 (@py_assert3)
#             456 LOAD_FAST                9 (@py_assert3)
#             458 POP_JUMP_IF_TRUE       149 (to 758)
#             460 LOAD_CONST              16 ('assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}')
#             462 LOAD_CONST              17 ('any')
#             464 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             474 LOAD_ATTR               10 (locals)
#             494 CALL                     0
#             502 CONTAINS_OP              0
#             504 POP_JUMP_IF_TRUE        25 (to 556)
#             506 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             516 LOAD_ATTR               12 (_should_repr_global_name)
#             536 LOAD_GLOBAL             20 (any)
#             546 CALL                     1
#             554 POP_JUMP_IF_FALSE       25 (to 606)
#         >>  556 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             566 LOAD_ATTR               14 (_saferepr)
#             586 LOAD_GLOBAL             20 (any)
#             596 CALL                     1
#             604 JUMP_FORWARD             1 (to 608)
#         >>  606 LOAD_CONST              17 ('any')
#         >>  608 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             618 LOAD_ATTR               14 (_saferepr)
#             638 LOAD_FAST                6 (@py_assert1)
#             640 CALL                     1
#             648 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             658 LOAD_ATTR               14 (_saferepr)
#             678 LOAD_FAST                9 (@py_assert3)
#             680 CALL                     1
#             688 LOAD_CONST              18 (('py0', 'py2', 'py4'))
#             690 BUILD_CONST_KEY_MAP      3
#             692 BINARY_OP                6 (%)
#             696 STORE_FAST              10 (@py_format5)
#             698 LOAD_GLOBAL             17 (NULL + AssertionError)
#             708 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             718 LOAD_ATTR               18 (_format_explanation)
#             738 LOAD_FAST               10 (@py_format5)
#             740 CALL                     1
#             748 CALL                     1
#             756 RAISE_VARARGS            1
#         >>  758 LOAD_CONST               0 (None)
#             760 COPY                     1
#             762 STORE_FAST               6 (@py_assert1)
#             764 STORE_FAST               9 (@py_assert3)
#             766 RETURN_CONST             0 (None)
# 
# Disassembly of <code object <genexpr> at 0x73cd93b06790, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 40>:
#  40           0 RETURN_GENERATOR
#               2 POP_TOP
#               4 RESUME                   0
#               6 LOAD_FAST                0 (.0)
#         >>    8 FOR_ITER                 8 (to 28)
#              12 STORE_FAST               1 (e)
#              14 LOAD_CONST               0 ('time_range')
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
# Disassembly of <code object TestResultCompareRun at 0x73cd93b065b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 43>:
#  43           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestResultCompareRun')
#               8 STORE_NAME               2 (__qualname__)
# 
#  44          10 LOAD_CONST               1 (<code object test_insufficient_valid_results at 0x3af9e490, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 44>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_insufficient_valid_results)
# 
#  55          16 LOAD_CONST               2 (<code object test_success_with_two_sources at 0x3afaaab0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 55>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_success_with_two_sources)
# 
#  72          22 LOAD_CONST               3 (<code object test_global_rms_computation at 0x3af9d7e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 72>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_global_rms_computation)
# 
#  88          28 LOAD_CONST               4 (<code object test_validation_failure_run at 0x3afabfe0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 88>)
#              30 MAKE_FUNCTION            0
#              32 STORE_NAME               6 (test_validation_failure_run)
#              34 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_insufficient_valid_results at 0x3af9e490, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 44>:
#  44           0 RESUME                   0
# 
#  45           2 LOAD_GLOBAL              1 (NULL + ResultCompareSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  47          22 LOAD_CONST               1 ('job1')
#              24 LOAD_CONST               2 ('job2')
#              26 BUILD_LIST               2
# 
#  49          28 LOAD_CONST               1 ('job1')
#              30 LOAD_CONST               3 ('metrics')
#              32 LOAD_CONST               4 (5)
#              34 LOAD_CONST               5 (1)
#              36 LOAD_CONST               6 (3)
#              38 LOAD_CONST               5 (1)
#              40 LOAD_CONST               7 (('max', 'min', 'mean', 'rms'))
#              42 BUILD_CONST_KEY_MAP      4
#              44 BUILD_MAP                1
# 
#  48          46 BUILD_MAP                1
# 
#  46          48 LOAD_CONST               8 (('job_ids', 'results_by_job'))
#              50 BUILD_CONST_KEY_MAP      2
#              52 STORE_FAST               2 (config)
# 
#  52          54 LOAD_FAST                1 (skill)
#              56 LOAD_ATTR                3 (NULL|self + run)
#              76 LOAD_FAST                2 (config)
#              78 CALL                     1
#              86 STORE_FAST               3 (result)
# 
#  53          88 LOAD_FAST                3 (result)
#              90 LOAD_ATTR                4 (status)
#             110 STORE_FAST               4 (@py_assert1)
#             112 LOAD_GLOBAL              6 (SkillStatus)
#             122 LOAD_ATTR                8 (FAILED)
#             142 STORE_FAST               5 (@py_assert5)
#             144 LOAD_FAST                4 (@py_assert1)
#             146 LOAD_FAST                5 (@py_assert5)
#             148 COMPARE_OP              40 (==)
#             152 STORE_FAST               6 (@py_assert3)
#             154 LOAD_FAST                6 (@py_assert3)
#             156 POP_JUMP_IF_TRUE       246 (to 650)
#             158 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             168 LOAD_ATTR               12 (_call_reprcompare)
#             188 LOAD_CONST               9 (('==',))
#             190 LOAD_FAST                6 (@py_assert3)
#             192 BUILD_TUPLE              1
#             194 LOAD_CONST              10 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.FAILED\n}',))
#             196 LOAD_FAST                4 (@py_assert1)
#             198 LOAD_FAST                5 (@py_assert5)
#             200 BUILD_TUPLE              2
#             202 CALL                     4
#             210 LOAD_CONST              11 ('result')
#             212 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             222 LOAD_ATTR               16 (locals)
#             242 CALL                     0
#             250 CONTAINS_OP              0
#             252 POP_JUMP_IF_TRUE        21 (to 296)
#             254 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             264 LOAD_ATTR               18 (_should_repr_global_name)
#             284 LOAD_FAST                3 (result)
#             286 CALL                     1
#             294 POP_JUMP_IF_FALSE       21 (to 338)
#         >>  296 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             306 LOAD_ATTR               20 (_saferepr)
#             326 LOAD_FAST                3 (result)
#             328 CALL                     1
#             336 JUMP_FORWARD             1 (to 340)
#         >>  338 LOAD_CONST              11 ('result')
#         >>  340 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             350 LOAD_ATTR               20 (_saferepr)
#             370 LOAD_FAST                4 (@py_assert1)
#             372 CALL                     1
#             380 LOAD_CONST              12 ('SkillStatus')
#             382 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             392 LOAD_ATTR               16 (locals)
#             412 CALL                     0
#             420 CONTAINS_OP              0
#             422 POP_JUMP_IF_TRUE        25 (to 474)
#             424 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             434 LOAD_ATTR               18 (_should_repr_global_name)
#             454 LOAD_GLOBAL              6 (SkillStatus)
#             464 CALL                     1
#             472 POP_JUMP_IF_FALSE       25 (to 524)
#         >>  474 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             484 LOAD_ATTR               20 (_saferepr)
#             504 LOAD_GLOBAL              6 (SkillStatus)
#             514 CALL                     1
#             522 JUMP_FORWARD             1 (to 526)
#         >>  524 LOAD_CONST              12 ('SkillStatus')
#         >>  526 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             536 LOAD_ATTR               20 (_saferepr)
#             556 LOAD_FAST                5 (@py_assert5)
#             558 CALL                     1
#             566 LOAD_CONST              13 (('py0', 'py2', 'py4', 'py6'))
#             568 BUILD_CONST_KEY_MAP      4
#             570 BINARY_OP                6 (%)
#             574 STORE_FAST               7 (@py_format7)
#             576 LOAD_CONST              14 ('assert %(py8)s')
#             578 LOAD_CONST              15 ('py8')
#             580 LOAD_FAST                7 (@py_format7)
#             582 BUILD_MAP                1
#             584 BINARY_OP                6 (%)
#             588 STORE_FAST               8 (@py_format9)
#             590 LOAD_GLOBAL             23 (NULL + AssertionError)
#             600 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             610 LOAD_ATTR               24 (_format_explanation)
#             630 LOAD_FAST                8 (@py_format9)
#             632 CALL                     1
#             640 CALL                     1
#             648 RAISE_VARARGS            1
#         >>  650 LOAD_CONST               0 (None)
#             652 COPY                     1
#             654 STORE_FAST               4 (@py_assert1)
#             656 COPY                     1
#             658 STORE_FAST               6 (@py_assert3)
#             660 STORE_FAST               5 (@py_assert5)
#             662 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_success_with_two_sources at 0x3afaaab0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 55>:
#  55           0 RESUME                   0
# 
#  56           2 LOAD_GLOBAL              1 (NULL + ResultCompareSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  58          22 LOAD_CONST               1 ('job1')
#              24 LOAD_CONST               2 ('job2')
#              26 BUILD_LIST               2
# 
#  60          28 LOAD_CONST               3 ('metrics')
#              30 LOAD_CONST               4 (10)
#              32 LOAD_CONST               5 (1)
#              34 LOAD_CONST               6 (5)
#              36 LOAD_CONST               7 (2)
#              38 LOAD_CONST               8 (('max', 'min', 'mean', 'rms'))
#              40 BUILD_CONST_KEY_MAP      4
#              42 BUILD_MAP                1
# 
#  61          44 LOAD_CONST               3 ('metrics')
#              46 LOAD_CONST               9 (8)
#              48 LOAD_CONST              10 (0)
#              50 LOAD_CONST              11 (4)
#              52 LOAD_CONST              12 (1.5)
#              54 LOAD_CONST               8 (('max', 'min', 'mean', 'rms'))
#              56 BUILD_CONST_KEY_MAP      4
#              58 BUILD_MAP                1
# 
#  59          60 LOAD_CONST              13 (('job1', 'job2'))
#              62 BUILD_CONST_KEY_MAP      2
# 
#  57          64 LOAD_CONST              14 (('job_ids', 'results_by_job'))
#              66 BUILD_CONST_KEY_MAP      2
#              68 STORE_FAST               2 (config)
# 
#  64          70 LOAD_FAST                1 (skill)
#              72 LOAD_ATTR                3 (NULL|self + run)
#              92 LOAD_FAST                2 (config)
#              94 CALL                     1
#             102 STORE_FAST               3 (result)
# 
#  65         104 LOAD_FAST                3 (result)
#             106 LOAD_ATTR                4 (status)
#             126 STORE_FAST               4 (@py_assert1)
#             128 LOAD_GLOBAL              6 (SkillStatus)
#             138 LOAD_ATTR                8 (SUCCESS)
#             158 STORE_FAST               5 (@py_assert5)
#             160 LOAD_FAST                4 (@py_assert1)
#             162 LOAD_FAST                5 (@py_assert5)
#             164 COMPARE_OP              40 (==)
#             168 STORE_FAST               6 (@py_assert3)
#             170 LOAD_FAST                6 (@py_assert3)
#             172 POP_JUMP_IF_TRUE       246 (to 666)
#             174 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             184 LOAD_ATTR               12 (_call_reprcompare)
#             204 LOAD_CONST              15 (('==',))
#             206 LOAD_FAST                6 (@py_assert3)
#             208 BUILD_TUPLE              1
#             210 LOAD_CONST              16 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.SUCCESS\n}',))
#             212 LOAD_FAST                4 (@py_assert1)
#             214 LOAD_FAST                5 (@py_assert5)
#             216 BUILD_TUPLE              2
#             218 CALL                     4
#             226 LOAD_CONST              17 ('result')
#             228 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             238 LOAD_ATTR               16 (locals)
#             258 CALL                     0
#             266 CONTAINS_OP              0
#             268 POP_JUMP_IF_TRUE        21 (to 312)
#             270 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             280 LOAD_ATTR               18 (_should_repr_global_name)
#             300 LOAD_FAST                3 (result)
#             302 CALL                     1
#             310 POP_JUMP_IF_FALSE       21 (to 354)
#         >>  312 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             322 LOAD_ATTR               20 (_saferepr)
#             342 LOAD_FAST                3 (result)
#             344 CALL                     1
#             352 JUMP_FORWARD             1 (to 356)
#         >>  354 LOAD_CONST              17 ('result')
#         >>  356 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             366 LOAD_ATTR               20 (_saferepr)
#             386 LOAD_FAST                4 (@py_assert1)
#             388 CALL                     1
#             396 LOAD_CONST              18 ('SkillStatus')
#             398 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             408 LOAD_ATTR               16 (locals)
#             428 CALL                     0
#             436 CONTAINS_OP              0
#             438 POP_JUMP_IF_TRUE        25 (to 490)
#             440 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             450 LOAD_ATTR               18 (_should_repr_global_name)
#             470 LOAD_GLOBAL              6 (SkillStatus)
#             480 CALL                     1
#             488 POP_JUMP_IF_FALSE       25 (to 540)
#         >>  490 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             500 LOAD_ATTR               20 (_saferepr)
#             520 LOAD_GLOBAL              6 (SkillStatus)
#             530 CALL                     1
#             538 JUMP_FORWARD             1 (to 542)
#         >>  540 LOAD_CONST              18 ('SkillStatus')
#         >>  542 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             552 LOAD_ATTR               20 (_saferepr)
#             572 LOAD_FAST                5 (@py_assert5)
#             574 CALL                     1
#             582 LOAD_CONST              19 (('py0', 'py2', 'py4', 'py6'))
#             584 BUILD_CONST_KEY_MAP      4
#             586 BINARY_OP                6 (%)
#             590 STORE_FAST               7 (@py_format7)
#             592 LOAD_CONST              20 ('assert %(py8)s')
#             594 LOAD_CONST              21 ('py8')
#             596 LOAD_FAST                7 (@py_format7)
#             598 BUILD_MAP                1
#             600 BINARY_OP                6 (%)
#             604 STORE_FAST               8 (@py_format9)
#             606 LOAD_GLOBAL             23 (NULL + AssertionError)
#             616 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             626 LOAD_ATTR               24 (_format_explanation)
#             646 LOAD_FAST                8 (@py_format9)
#             648 CALL                     1
#             656 CALL                     1
#             664 RAISE_VARARGS            1
#         >>  666 LOAD_CONST               0 (None)
#             668 COPY                     1
#             670 STORE_FAST               4 (@py_assert1)
#             672 COPY                     1
#             674 STORE_FAST               6 (@py_assert3)
#             676 STORE_FAST               5 (@py_assert5)
# 
#  66         678 LOAD_FAST                3 (result)
#             680 LOAD_ATTR               26 (data)
#             700 STORE_FAST               4 (@py_assert1)
#             702 LOAD_CONST               0 (None)
#             704 STORE_FAST               9 (@py_assert4)
#             706 LOAD_FAST                4 (@py_assert1)
#             708 LOAD_FAST                9 (@py_assert4)
#             710 IS_OP                    1
#             712 STORE_FAST               6 (@py_assert3)
#             714 LOAD_FAST                6 (@py_assert3)
#             716 POP_JUMP_IF_TRUE       173 (to 1064)
#             718 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             728 LOAD_ATTR               12 (_call_reprcompare)
#             748 LOAD_CONST              22 (('is not',))
#             750 LOAD_FAST                6 (@py_assert3)
#             752 BUILD_TUPLE              1
#             754 LOAD_CONST              23 (('%(py2)s\n{%(py2)s = %(py0)s.data\n} is not %(py5)s',))
#             756 LOAD_FAST                4 (@py_assert1)
#             758 LOAD_FAST                9 (@py_assert4)
#             760 BUILD_TUPLE              2
#             762 CALL                     4
#             770 LOAD_CONST              17 ('result')
#             772 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             782 LOAD_ATTR               16 (locals)
#             802 CALL                     0
#             810 CONTAINS_OP              0
#             812 POP_JUMP_IF_TRUE        21 (to 856)
#             814 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             824 LOAD_ATTR               18 (_should_repr_global_name)
#             844 LOAD_FAST                3 (result)
#             846 CALL                     1
#             854 POP_JUMP_IF_FALSE       21 (to 898)
#         >>  856 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             866 LOAD_ATTR               20 (_saferepr)
#             886 LOAD_FAST                3 (result)
#             888 CALL                     1
#             896 JUMP_FORWARD             1 (to 900)
#         >>  898 LOAD_CONST              17 ('result')
#         >>  900 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             910 LOAD_ATTR               20 (_saferepr)
#             930 LOAD_FAST                4 (@py_assert1)
#             932 CALL                     1
#             940 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             950 LOAD_ATTR               20 (_saferepr)
#             970 LOAD_FAST                9 (@py_assert4)
#             972 CALL                     1
#             980 LOAD_CONST              24 (('py0', 'py2', 'py5'))
#             982 BUILD_CONST_KEY_MAP      3
#             984 BINARY_OP                6 (%)
#             988 STORE_FAST              10 (@py_format6)
#             990 LOAD_CONST              25 ('assert %(py7)s')
#             992 LOAD_CONST              26 ('py7')
#             994 LOAD_FAST               10 (@py_format6)
#             996 BUILD_MAP                1
#             998 BINARY_OP                6 (%)
#            1002 STORE_FAST              11 (@py_format8)
#            1004 LOAD_GLOBAL             23 (NULL + AssertionError)
#            1014 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1024 LOAD_ATTR               24 (_format_explanation)
#            1044 LOAD_FAST               11 (@py_format8)
#            1046 CALL                     1
#            1054 CALL                     1
#            1062 RAISE_VARARGS            1
#         >> 1064 LOAD_CONST               0 (None)
#            1066 COPY                     1
#            1068 STORE_FAST               4 (@py_assert1)
#            1070 COPY                     1
#            1072 STORE_FAST               6 (@py_assert3)
#            1074 STORE_FAST               9 (@py_assert4)
# 
#  67        1076 LOAD_CONST              27 ('global_metrics')
#            1078 STORE_FAST              12 (@py_assert0)
#            1080 LOAD_FAST                3 (result)
#            1082 LOAD_ATTR               26 (data)
#            1102 STORE_FAST               9 (@py_assert4)
#            1104 LOAD_FAST               12 (@py_assert0)
#            1106 LOAD_FAST                9 (@py_assert4)
#            1108 CONTAINS_OP              0
#            1110 STORE_FAST              13 (@py_assert2)
#            1112 LOAD_FAST               13 (@py_assert2)
#            1114 POP_JUMP_IF_TRUE       173 (to 1462)
#            1116 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1126 LOAD_ATTR               12 (_call_reprcompare)
#            1146 LOAD_CONST              28 (('in',))
#            1148 LOAD_FAST               13 (@py_assert2)
#            1150 BUILD_TUPLE              1
#            1152 LOAD_CONST              29 (('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.data\n}',))
#            1154 LOAD_FAST               12 (@py_assert0)
#            1156 LOAD_FAST                9 (@py_assert4)
#            1158 BUILD_TUPLE              2
#            1160 CALL                     4
#            1168 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1178 LOAD_ATTR               20 (_saferepr)
#            1198 LOAD_FAST               12 (@py_assert0)
#            1200 CALL                     1
#            1208 LOAD_CONST              17 ('result')
#            1210 LOAD_GLOBAL             15 (NULL + @py_builtins)
#            1220 LOAD_ATTR               16 (locals)
#            1240 CALL                     0
#            1248 CONTAINS_OP              0
#            1250 POP_JUMP_IF_TRUE        21 (to 1294)
#            1252 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1262 LOAD_ATTR               18 (_should_repr_global_name)
#            1282 LOAD_FAST                3 (result)
#            1284 CALL                     1
#            1292 POP_JUMP_IF_FALSE       21 (to 1336)
#         >> 1294 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1304 LOAD_ATTR               20 (_saferepr)
#            1324 LOAD_FAST                3 (result)
#            1326 CALL                     1
#            1334 JUMP_FORWARD             1 (to 1338)
#         >> 1336 LOAD_CONST              17 ('result')
#         >> 1338 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1348 LOAD_ATTR               20 (_saferepr)
#            1368 LOAD_FAST                9 (@py_assert4)
#            1370 CALL                     1
#            1378 LOAD_CONST              30 (('py1', 'py3', 'py5'))
#            1380 BUILD_CONST_KEY_MAP      3
#            1382 BINARY_OP                6 (%)
#            1386 STORE_FAST              10 (@py_format6)
#            1388 LOAD_CONST              25 ('assert %(py7)s')
#            1390 LOAD_CONST              26 ('py7')
#            1392 LOAD_FAST               10 (@py_format6)
#            1394 BUILD_MAP                1
#            1396 BINARY_OP                6 (%)
#            1400 STORE_FAST              11 (@py_format8)
#            1402 LOAD_GLOBAL             23 (NULL + AssertionError)
#            1412 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1422 LOAD_ATTR               24 (_format_explanation)
#            1442 LOAD_FAST               11 (@py_format8)
#            1444 CALL                     1
#            1452 CALL                     1
#            1460 RAISE_VARARGS            1
#         >> 1462 LOAD_CONST               0 (None)
#            1464 COPY                     1
#            1466 STORE_FAST              12 (@py_assert0)
#            1468 COPY                     1
#            1470 STORE_FAST              13 (@py_assert2)
#            1472 STORE_FAST               9 (@py_assert4)
# 
#  68        1474 LOAD_CONST              31 ('per_job_metrics')
#            1476 STORE_FAST              12 (@py_assert0)
#            1478 LOAD_FAST                3 (result)
#            1480 LOAD_ATTR               26 (data)
#            1500 STORE_FAST               9 (@py_assert4)
#            1502 LOAD_FAST               12 (@py_assert0)
#            1504 LOAD_FAST                9 (@py_assert4)
#            1506 CONTAINS_OP              0
#            1508 STORE_FAST              13 (@py_assert2)
#            1510 LOAD_FAST               13 (@py_assert2)
#            1512 POP_JUMP_IF_TRUE       173 (to 1860)
#            1514 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1524 LOAD_ATTR               12 (_call_reprcompare)
#            1544 LOAD_CONST              28 (('in',))
#            1546 LOAD_FAST               13 (@py_assert2)
#            1548 BUILD_TUPLE              1
#            1550 LOAD_CONST              29 (('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.data\n}',))
#            1552 LOAD_FAST               12 (@py_assert0)
#            1554 LOAD_FAST                9 (@py_assert4)
#            1556 BUILD_TUPLE              2
#            1558 CALL                     4
#            1566 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1576 LOAD_ATTR               20 (_saferepr)
#            1596 LOAD_FAST               12 (@py_assert0)
#            1598 CALL                     1
#            1606 LOAD_CONST              17 ('result')
#            1608 LOAD_GLOBAL             15 (NULL + @py_builtins)
#            1618 LOAD_ATTR               16 (locals)
#            1638 CALL                     0
#            1646 CONTAINS_OP              0
#            1648 POP_JUMP_IF_TRUE        21 (to 1692)
#            1650 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1660 LOAD_ATTR               18 (_should_repr_global_name)
#            1680 LOAD_FAST                3 (result)
#            1682 CALL                     1
#            1690 POP_JUMP_IF_FALSE       21 (to 1734)
#         >> 1692 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1702 LOAD_ATTR               20 (_saferepr)
#            1722 LOAD_FAST                3 (result)
#            1724 CALL                     1
#            1732 JUMP_FORWARD             1 (to 1736)
#         >> 1734 LOAD_CONST              17 ('result')
#         >> 1736 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1746 LOAD_ATTR               20 (_saferepr)
#            1766 LOAD_FAST                9 (@py_assert4)
#            1768 CALL                     1
#            1776 LOAD_CONST              30 (('py1', 'py3', 'py5'))
#            1778 BUILD_CONST_KEY_MAP      3
#            1780 BINARY_OP                6 (%)
#            1784 STORE_FAST              10 (@py_format6)
#            1786 LOAD_CONST              25 ('assert %(py7)s')
#            1788 LOAD_CONST              26 ('py7')
#            1790 LOAD_FAST               10 (@py_format6)
#            1792 BUILD_MAP                1
#            1794 BINARY_OP                6 (%)
#            1798 STORE_FAST              11 (@py_format8)
#            1800 LOAD_GLOBAL             23 (NULL + AssertionError)
#            1810 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1820 LOAD_ATTR               24 (_format_explanation)
#            1840 LOAD_FAST               11 (@py_format8)
#            1842 CALL                     1
#            1850 CALL                     1
#            1858 RAISE_VARARGS            1
#         >> 1860 LOAD_CONST               0 (None)
#            1862 COPY                     1
#            1864 STORE_FAST              12 (@py_assert0)
#            1866 COPY                     1
#            1868 STORE_FAST              13 (@py_assert2)
#            1870 STORE_FAST               9 (@py_assert4)
# 
#  69        1872 LOAD_FAST                3 (result)
#            1874 LOAD_ATTR               26 (data)
#            1894 LOAD_CONST              27 ('global_metrics')
#            1896 BINARY_SUBSCR
#            1900 LOAD_CONST              32 ('max')
#            1902 BINARY_SUBSCR
#            1906 STORE_FAST              12 (@py_assert0)
#            1908 LOAD_CONST              33 (10.0)
#            1910 STORE_FAST               6 (@py_assert3)
#            1912 LOAD_FAST               12 (@py_assert0)
#            1914 LOAD_FAST                6 (@py_assert3)
#            1916 COMPARE_OP              40 (==)
#            1920 STORE_FAST              13 (@py_assert2)
#            1922 LOAD_FAST               13 (@py_assert2)
#            1924 POP_JUMP_IF_TRUE       108 (to 2142)
#            1926 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1936 LOAD_ATTR               12 (_call_reprcompare)
#            1956 LOAD_CONST              15 (('==',))
#            1958 LOAD_FAST               13 (@py_assert2)
#            1960 BUILD_TUPLE              1
#            1962 LOAD_CONST              34 (('%(py1)s == %(py4)s',))
#            1964 LOAD_FAST               12 (@py_assert0)
#            1966 LOAD_FAST                6 (@py_assert3)
#            1968 BUILD_TUPLE              2
#            1970 CALL                     4
#            1978 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1988 LOAD_ATTR               20 (_saferepr)
#            2008 LOAD_FAST               12 (@py_assert0)
#            2010 CALL                     1
#            2018 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            2028 LOAD_ATTR               20 (_saferepr)
#            2048 LOAD_FAST                6 (@py_assert3)
#            2050 CALL                     1
#            2058 LOAD_CONST              35 (('py1', 'py4'))
#            2060 BUILD_CONST_KEY_MAP      2
#            2062 BINARY_OP                6 (%)
#            2066 STORE_FAST              14 (@py_format5)
#            2068 LOAD_CONST              36 ('assert %(py6)s')
#            2070 LOAD_CONST              37 ('py6')
#            2072 LOAD_FAST               14 (@py_format5)
#            2074 BUILD_MAP                1
#            2076 BINARY_OP                6 (%)
#            2080 STORE_FAST               7 (@py_format7)
#            2082 LOAD_GLOBAL             23 (NULL + AssertionError)
#            2092 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            2102 LOAD_ATTR               24 (_format_explanation)
#            2122 LOAD_FAST                7 (@py_format7)
#            2124 CALL                     1
#            2132 CALL                     1
#            2140 RAISE_VARARGS            1
#         >> 2142 LOAD_CONST               0 (None)
#            2144 COPY                     1
#            2146 STORE_FAST              12 (@py_assert0)
#            2148 COPY                     1
#            2150 STORE_FAST              13 (@py_assert2)
#            2152 STORE_FAST               6 (@py_assert3)
# 
#  70        2154 LOAD_FAST                3 (result)
#            2156 LOAD_ATTR               26 (data)
#            2176 LOAD_CONST              27 ('global_metrics')
#            2178 BINARY_SUBSCR
#            2182 LOAD_CONST              38 ('min')
#            2184 BINARY_SUBSCR
#            2188 STORE_FAST              12 (@py_assert0)
#            2190 LOAD_CONST              39 (0.0)
#            2192 STORE_FAST               6 (@py_assert3)
#            2194 LOAD_FAST               12 (@py_assert0)
#            2196 LOAD_FAST                6 (@py_assert3)
#            2198 COMPARE_OP              40 (==)
#            2202 STORE_FAST              13 (@py_assert2)
#            2204 LOAD_FAST               13 (@py_assert2)
#            2206 POP_JUMP_IF_TRUE       108 (to 2424)
#            2208 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            2218 LOAD_ATTR               12 (_call_reprcompare)
#            2238 LOAD_CONST              15 (('==',))
#            2240 LOAD_FAST               13 (@py_assert2)
#            2242 BUILD_TUPLE              1
#            2244 LOAD_CONST              34 (('%(py1)s == %(py4)s',))
#            2246 LOAD_FAST               12 (@py_assert0)
#            2248 LOAD_FAST                6 (@py_assert3)
#            2250 BUILD_TUPLE              2
#            2252 CALL                     4
#            2260 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            2270 LOAD_ATTR               20 (_saferepr)
#            2290 LOAD_FAST               12 (@py_assert0)
#            2292 CALL                     1
#            2300 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            2310 LOAD_ATTR               20 (_saferepr)
#            2330 LOAD_FAST                6 (@py_assert3)
#            2332 CALL                     1
#            2340 LOAD_CONST              35 (('py1', 'py4'))
#            2342 BUILD_CONST_KEY_MAP      2
#            2344 BINARY_OP                6 (%)
#            2348 STORE_FAST              14 (@py_format5)
#            2350 LOAD_CONST              36 ('assert %(py6)s')
#            2352 LOAD_CONST              37 ('py6')
#            2354 LOAD_FAST               14 (@py_format5)
#            2356 BUILD_MAP                1
#            2358 BINARY_OP                6 (%)
#            2362 STORE_FAST               7 (@py_format7)
#            2364 LOAD_GLOBAL             23 (NULL + AssertionError)
#            2374 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            2384 LOAD_ATTR               24 (_format_explanation)
#            2404 LOAD_FAST                7 (@py_format7)
#            2406 CALL                     1
#            2414 CALL                     1
#            2422 RAISE_VARARGS            1
#         >> 2424 LOAD_CONST               0 (None)
#            2426 COPY                     1
#            2428 STORE_FAST              12 (@py_assert0)
#            2430 COPY                     1
#            2432 STORE_FAST              13 (@py_assert2)
#            2434 STORE_FAST               6 (@py_assert3)
#            2436 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_global_rms_computation at 0x3af9d7e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 72>:
#  72           0 RESUME                   0
# 
#  73           2 LOAD_GLOBAL              1 (NULL + ResultCompareSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  75          22 LOAD_CONST               1 ('j1')
#              24 LOAD_CONST               2 ('j2')
#              26 BUILD_LIST               2
# 
#  77          28 LOAD_CONST               3 ('metrics')
#              30 LOAD_CONST               4 (10)
#              32 LOAD_CONST               5 (1)
#              34 LOAD_CONST               6 (5)
#              36 LOAD_CONST               7 (3)
#              38 LOAD_CONST               8 (('max', 'min', 'mean', 'rms'))
#              40 BUILD_CONST_KEY_MAP      4
#              42 BUILD_MAP                1
# 
#  78          44 LOAD_CONST               3 ('metrics')
#              46 LOAD_CONST               9 (8)
#              48 LOAD_CONST              10 (2)
#              50 LOAD_CONST              11 (4)
#              52 LOAD_CONST              11 (4)
#              54 LOAD_CONST               8 (('max', 'min', 'mean', 'rms'))
#              56 BUILD_CONST_KEY_MAP      4
#              58 BUILD_MAP                1
# 
#  76          60 LOAD_CONST              12 (('j1', 'j2'))
#              62 BUILD_CONST_KEY_MAP      2
# 
#  74          64 LOAD_CONST              13 (('job_ids', 'results_by_job'))
#              66 BUILD_CONST_KEY_MAP      2
#              68 STORE_FAST               2 (config)
# 
#  81          70 LOAD_FAST                1 (skill)
#              72 LOAD_ATTR                3 (NULL|self + run)
#              92 LOAD_FAST                2 (config)
#              94 CALL                     1
#             102 STORE_FAST               3 (result)
# 
#  82         104 LOAD_FAST                3 (result)
#             106 LOAD_ATTR                4 (status)
#             126 STORE_FAST               4 (@py_assert1)
#             128 LOAD_GLOBAL              6 (SkillStatus)
#             138 LOAD_ATTR                8 (SUCCESS)
#             158 STORE_FAST               5 (@py_assert5)
#             160 LOAD_FAST                4 (@py_assert1)
#             162 LOAD_FAST                5 (@py_assert5)
#             164 COMPARE_OP              40 (==)
#             168 STORE_FAST               6 (@py_assert3)
#             170 LOAD_FAST                6 (@py_assert3)
#             172 POP_JUMP_IF_TRUE       246 (to 666)
#             174 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             184 LOAD_ATTR               12 (_call_reprcompare)
#             204 LOAD_CONST              14 (('==',))
#             206 LOAD_FAST                6 (@py_assert3)
#             208 BUILD_TUPLE              1
#             210 LOAD_CONST              15 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.SUCCESS\n}',))
#             212 LOAD_FAST                4 (@py_assert1)
#             214 LOAD_FAST                5 (@py_assert5)
#             216 BUILD_TUPLE              2
#             218 CALL                     4
#             226 LOAD_CONST              16 ('result')
#             228 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             238 LOAD_ATTR               16 (locals)
#             258 CALL                     0
#             266 CONTAINS_OP              0
#             268 POP_JUMP_IF_TRUE        21 (to 312)
#             270 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             280 LOAD_ATTR               18 (_should_repr_global_name)
#             300 LOAD_FAST                3 (result)
#             302 CALL                     1
#             310 POP_JUMP_IF_FALSE       21 (to 354)
#         >>  312 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             322 LOAD_ATTR               20 (_saferepr)
#             342 LOAD_FAST                3 (result)
#             344 CALL                     1
#             352 JUMP_FORWARD             1 (to 356)
#         >>  354 LOAD_CONST              16 ('result')
#         >>  356 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             366 LOAD_ATTR               20 (_saferepr)
#             386 LOAD_FAST                4 (@py_assert1)
#             388 CALL                     1
#             396 LOAD_CONST              17 ('SkillStatus')
#             398 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             408 LOAD_ATTR               16 (locals)
#             428 CALL                     0
#             436 CONTAINS_OP              0
#             438 POP_JUMP_IF_TRUE        25 (to 490)
#             440 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             450 LOAD_ATTR               18 (_should_repr_global_name)
#             470 LOAD_GLOBAL              6 (SkillStatus)
#             480 CALL                     1
#             488 POP_JUMP_IF_FALSE       25 (to 540)
#         >>  490 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             500 LOAD_ATTR               20 (_saferepr)
#             520 LOAD_GLOBAL              6 (SkillStatus)
#             530 CALL                     1
#             538 JUMP_FORWARD             1 (to 542)
#         >>  540 LOAD_CONST              17 ('SkillStatus')
#         >>  542 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             552 LOAD_ATTR               20 (_saferepr)
#             572 LOAD_FAST                5 (@py_assert5)
#             574 CALL                     1
#             582 LOAD_CONST              18 (('py0', 'py2', 'py4', 'py6'))
#             584 BUILD_CONST_KEY_MAP      4
#             586 BINARY_OP                6 (%)
#             590 STORE_FAST               7 (@py_format7)
#             592 LOAD_CONST              19 ('assert %(py8)s')
#             594 LOAD_CONST              20 ('py8')
#             596 LOAD_FAST                7 (@py_format7)
#             598 BUILD_MAP                1
#             600 BINARY_OP                6 (%)
#             604 STORE_FAST               8 (@py_format9)
#             606 LOAD_GLOBAL             23 (NULL + AssertionError)
#             616 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             626 LOAD_ATTR               24 (_format_explanation)
#             646 LOAD_FAST                8 (@py_format9)
#             648 CALL                     1
#             656 CALL                     1
#             664 RAISE_VARARGS            1
#         >>  666 LOAD_CONST               0 (None)
#             668 COPY                     1
#             670 STORE_FAST               4 (@py_assert1)
#             672 COPY                     1
#             674 STORE_FAST               6 (@py_assert3)
#             676 STORE_FAST               5 (@py_assert5)
# 
#  83         678 LOAD_FAST                3 (result)
#             680 LOAD_ATTR               26 (data)
#             700 LOAD_CONST              21 ('global_metrics')
#             702 BINARY_SUBSCR
#             706 LOAD_CONST              22 ('rms')
#             708 BINARY_SUBSCR
#             712 STORE_FAST               9 (global_rms)
# 
#  84         714 LOAD_CONST               0 (None)
#             716 STORE_FAST              10 (@py_assert2)
#             718 LOAD_FAST                9 (global_rms)
#             720 LOAD_FAST               10 (@py_assert2)
#             722 IS_OP                    1
#             724 STORE_FAST               4 (@py_assert1)
#             726 LOAD_FAST                4 (@py_assert1)
#             728 POP_JUMP_IF_TRUE       153 (to 1036)
#             730 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             740 LOAD_ATTR               12 (_call_reprcompare)
#             760 LOAD_CONST              23 (('is not',))
#             762 LOAD_FAST                4 (@py_assert1)
#             764 BUILD_TUPLE              1
#             766 LOAD_CONST              24 (('%(py0)s is not %(py3)s',))
#             768 LOAD_FAST                9 (global_rms)
#             770 LOAD_FAST               10 (@py_assert2)
#             772 BUILD_TUPLE              2
#             774 CALL                     4
#             782 LOAD_CONST              25 ('global_rms')
#             784 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             794 LOAD_ATTR               16 (locals)
#             814 CALL                     0
#             822 CONTAINS_OP              0
#             824 POP_JUMP_IF_TRUE        21 (to 868)
#             826 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             836 LOAD_ATTR               18 (_should_repr_global_name)
#             856 LOAD_FAST                9 (global_rms)
#             858 CALL                     1
#             866 POP_JUMP_IF_FALSE       21 (to 910)
#         >>  868 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             878 LOAD_ATTR               20 (_saferepr)
#             898 LOAD_FAST                9 (global_rms)
#             900 CALL                     1
#             908 JUMP_FORWARD             1 (to 912)
#         >>  910 LOAD_CONST              25 ('global_rms')
#         >>  912 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             922 LOAD_ATTR               20 (_saferepr)
#             942 LOAD_FAST               10 (@py_assert2)
#             944 CALL                     1
#             952 LOAD_CONST              26 (('py0', 'py3'))
#             954 BUILD_CONST_KEY_MAP      2
#             956 BINARY_OP                6 (%)
#             960 STORE_FAST              11 (@py_format4)
#             962 LOAD_CONST              27 ('assert %(py5)s')
#             964 LOAD_CONST              28 ('py5')
#             966 LOAD_FAST               11 (@py_format4)
#             968 BUILD_MAP                1
#             970 BINARY_OP                6 (%)
#             974 STORE_FAST              12 (@py_format6)
#             976 LOAD_GLOBAL             23 (NULL + AssertionError)
#             986 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             996 LOAD_ATTR               24 (_format_explanation)
#            1016 LOAD_FAST               12 (@py_format6)
#            1018 CALL                     1
#            1026 CALL                     1
#            1034 RAISE_VARARGS            1
#         >> 1036 LOAD_CONST               0 (None)
#            1038 COPY                     1
#            1040 STORE_FAST               4 (@py_assert1)
#            1042 STORE_FAST              10 (@py_assert2)
# 
#  85        1044 LOAD_CONST              29 (3.5355339059327378)
#            1046 STORE_FAST              13 (expected)
# 
#  86        1048 LOAD_FAST                9 (global_rms)
#            1050 LOAD_FAST               13 (expected)
#            1052 BINARY_OP               10 (-)
#            1056 STORE_FAST               6 (@py_assert3)
#            1058 LOAD_GLOBAL             29 (NULL + abs)
#            1068 LOAD_FAST                6 (@py_assert3)
#            1070 CALL                     1
#            1078 STORE_FAST              14 (@py_assert4)
#            1080 LOAD_CONST              30 (0.01)
#            1082 STORE_FAST              15 (@py_assert7)
#            1084 LOAD_FAST               14 (@py_assert4)
#            1086 LOAD_FAST               15 (@py_assert7)
#            1088 COMPARE_OP               2 (<)
#            1092 STORE_FAST              16 (@py_assert6)
#            1094 LOAD_FAST               16 (@py_assert6)
#            1096 EXTENDED_ARG             1
#            1098 POP_JUMP_IF_TRUE       311 (to 1722)
#            1100 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1110 LOAD_ATTR               12 (_call_reprcompare)
#            1130 LOAD_CONST              31 (('<',))
#            1132 LOAD_FAST               16 (@py_assert6)
#            1134 BUILD_TUPLE              1
#            1136 LOAD_CONST              32 (('%(py5)s\n{%(py5)s = %(py0)s((%(py1)s - %(py2)s))\n} < %(py8)s',))
#            1138 LOAD_FAST               14 (@py_assert4)
#            1140 LOAD_FAST               15 (@py_assert7)
#            1142 BUILD_TUPLE              2
#            1144 CALL                     4
#            1152 LOAD_CONST              33 ('abs')
#            1154 LOAD_GLOBAL             15 (NULL + @py_builtins)
#            1164 LOAD_ATTR               16 (locals)
#            1184 CALL                     0
#            1192 CONTAINS_OP              0
#            1194 POP_JUMP_IF_TRUE        25 (to 1246)
#            1196 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1206 LOAD_ATTR               18 (_should_repr_global_name)
#            1226 LOAD_GLOBAL             28 (abs)
#            1236 CALL                     1
#            1244 POP_JUMP_IF_FALSE       25 (to 1296)
#         >> 1246 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1256 LOAD_ATTR               20 (_saferepr)
#            1276 LOAD_GLOBAL             28 (abs)
#            1286 CALL                     1
#            1294 JUMP_FORWARD             1 (to 1298)
#         >> 1296 LOAD_CONST              33 ('abs')
#         >> 1298 LOAD_CONST              25 ('global_rms')
#            1300 LOAD_GLOBAL             15 (NULL + @py_builtins)
#            1310 LOAD_ATTR               16 (locals)
#            1330 CALL                     0
#            1338 CONTAINS_OP              0
#            1340 POP_JUMP_IF_TRUE        21 (to 1384)
#            1342 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1352 LOAD_ATTR               18 (_should_repr_global_name)
#            1372 LOAD_FAST                9 (global_rms)
#            1374 CALL                     1
#            1382 POP_JUMP_IF_FALSE       21 (to 1426)
#         >> 1384 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1394 LOAD_ATTR               20 (_saferepr)
#            1414 LOAD_FAST                9 (global_rms)
#            1416 CALL                     1
#            1424 JUMP_FORWARD             1 (to 1428)
#         >> 1426 LOAD_CONST              25 ('global_rms')
#         >> 1428 LOAD_CONST              34 ('expected')
#            1430 LOAD_GLOBAL             15 (NULL + @py_builtins)
#            1440 LOAD_ATTR               16 (locals)
#            1460 CALL                     0
#            1468 CONTAINS_OP              0
#            1470 POP_JUMP_IF_TRUE        21 (to 1514)
#            1472 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1482 LOAD_ATTR               18 (_should_repr_global_name)
#            1502 LOAD_FAST               13 (expected)
#            1504 CALL                     1
#            1512 POP_JUMP_IF_FALSE       21 (to 1556)
#         >> 1514 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1524 LOAD_ATTR               20 (_saferepr)
#            1544 LOAD_FAST               13 (expected)
#            1546 CALL                     1
#            1554 JUMP_FORWARD             1 (to 1558)
#         >> 1556 LOAD_CONST              34 ('expected')
#         >> 1558 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1568 LOAD_ATTR               20 (_saferepr)
#            1588 LOAD_FAST               14 (@py_assert4)
#            1590 CALL                     1
#            1598 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1608 LOAD_ATTR               20 (_saferepr)
#            1628 LOAD_FAST               15 (@py_assert7)
#            1630 CALL                     1
#            1638 LOAD_CONST              35 (('py0', 'py1', 'py2', 'py5', 'py8'))
#            1640 BUILD_CONST_KEY_MAP      5
#            1642 BINARY_OP                6 (%)
#            1646 STORE_FAST               8 (@py_format9)
#            1648 LOAD_CONST              36 ('assert %(py10)s')
#            1650 LOAD_CONST              37 ('py10')
#            1652 LOAD_FAST                8 (@py_format9)
#            1654 BUILD_MAP                1
#            1656 BINARY_OP                6 (%)
#            1660 STORE_FAST              17 (@py_format11)
#            1662 LOAD_GLOBAL             23 (NULL + AssertionError)
#            1672 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1682 LOAD_ATTR               24 (_format_explanation)
#            1702 LOAD_FAST               17 (@py_format11)
#            1704 CALL                     1
#            1712 CALL                     1
#            1720 RAISE_VARARGS            1
#         >> 1722 LOAD_CONST               0 (None)
#            1724 COPY                     1
#            1726 STORE_FAST               6 (@py_assert3)
#            1728 COPY                     1
#            1730 STORE_FAST              14 (@py_assert4)
#            1732 COPY                     1
#            1734 STORE_FAST              16 (@py_assert6)
#            1736 STORE_FAST              15 (@py_assert7)
#            1738 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validation_failure_run at 0x3afabfe0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_result_compare.py", line 88>:
#  88           0 RESUME                   0
# 
#  89           2 LOAD_GLOBAL              1 (NULL + ResultCompareSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  90          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + run)
#              44 BUILD_MAP                0
#              46 CALL                     1
#              54 STORE_FAST               2 (result)
# 
#  91          56 LOAD_FAST                2 (result)
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