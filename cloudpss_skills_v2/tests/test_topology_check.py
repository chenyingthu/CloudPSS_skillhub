# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/__pycache__/test_topology_check.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


def TestTopologyValidation():
    """TestTopologyValidation"""
pass  # TODO: restore


def TestTopologyIslands():
    """TestTopologyIslands"""
pass  # TODO: restore


def TestTopologyDangling():
    """TestTopologyDangling"""
pass  # TODO: restore


def TestTopologyParameters():
    """TestTopologyParameters"""
pass  # TODO: restore


def TestTopologyAdjacency():
    """TestTopologyAdjacency"""
pass  # TODO: restore


def TestTopologyRun():
    """TestTopologyRun"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('Tests for TopologyCheckSkill v2.')
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
#              42 LOAD_CONST               3 (('TopologyCheckSkill',))
#              44 IMPORT_NAME              8 (cloudpss_skills_v2.skills.topology_check)
#              46 IMPORT_FROM              9 (TopologyCheckSkill)
#              48 STORE_NAME               9 (TopologyCheckSkill)
#              50 POP_TOP
# 
#   7          52 PUSH_NULL
#              54 LOAD_BUILD_CLASS
#              56 LOAD_CONST               4 (<code object TestTopologyValidation at 0x73cd945ff050, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 7>)
#              58 MAKE_FUNCTION            0
#              60 LOAD_CONST               5 ('TestTopologyValidation')
#              62 CALL                     2
#              70 STORE_NAME              10 (TestTopologyValidation)
# 
#  20          72 PUSH_NULL
#              74 LOAD_BUILD_CLASS
#              76 LOAD_CONST               6 (<code object TestTopologyIslands at 0x73cd945fe4f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 20>)
#              78 MAKE_FUNCTION            0
#              80 LOAD_CONST               7 ('TestTopologyIslands')
#              82 CALL                     2
#              90 STORE_NAME              11 (TestTopologyIslands)
# 
#  41          92 PUSH_NULL
#              94 LOAD_BUILD_CLASS
#              96 LOAD_CONST               8 (<code object TestTopologyDangling at 0x73cd945fedb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 41>)
#              98 MAKE_FUNCTION            0
#             100 LOAD_CONST               9 ('TestTopologyDangling')
#             102 CALL                     2
#             110 STORE_NAME              12 (TestTopologyDangling)
# 
#  61         112 PUSH_NULL
#             114 LOAD_BUILD_CLASS
#             116 LOAD_CONST              10 (<code object TestTopologyParameters at 0x73cd945ff590, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 61>)
#             118 MAKE_FUNCTION            0
#             120 LOAD_CONST              11 ('TestTopologyParameters')
#             122 CALL                     2
#             130 STORE_NAME              13 (TestTopologyParameters)
# 
#  79         132 PUSH_NULL
#             134 LOAD_BUILD_CLASS
#             136 LOAD_CONST              12 (<code object TestTopologyAdjacency at 0x73cd945fecd0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 79>)
#             138 MAKE_FUNCTION            0
#             140 LOAD_CONST              13 ('TestTopologyAdjacency')
#             142 CALL                     2
#             150 STORE_NAME              14 (TestTopologyAdjacency)
# 
#  88         152 PUSH_NULL
#             154 LOAD_BUILD_CLASS
#             156 LOAD_CONST              14 (<code object TestTopologyRun at 0x73cd945fe870, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 88>)
#             158 MAKE_FUNCTION            0
#             160 LOAD_CONST              15 ('TestTopologyRun')
#             162 CALL                     2
#             170 STORE_NAME              15 (TestTopologyRun)
#             172 RETURN_CONST             2 (None)
# 
# Disassembly of <code object TestTopologyValidation at 0x73cd945ff050, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 7>:
#   7           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestTopologyValidation')
#               8 STORE_NAME               2 (__qualname__)
# 
#   8          10 LOAD_CONST               1 (<code object test_validate_missing_model at 0x3afa7230, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 8>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_validate_missing_model)
# 
#  13          16 LOAD_CONST               2 (<code object test_validate_valid_config at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 13>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_validate_valid_config)
#              22 RETURN_CONST             3 (None)
# 
# Disassembly of <code object test_validate_missing_model at 0x3afa7230, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 8>:
#   8           0 RESUME                   0
# 
#   9           2 LOAD_GLOBAL              1 (NULL + TopologyCheckSkill)
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
# Disassembly of <code object test_validate_valid_config at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 13>:
#  13           0 RESUME                   0
# 
#  14           2 LOAD_GLOBAL              1 (NULL + TopologyCheckSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  15          22 LOAD_CONST               1 ('model')
#              24 LOAD_CONST               2 ('rid')
#              26 LOAD_CONST               3 ('model/test/IEEE39')
#              28 BUILD_MAP                1
#              30 BUILD_MAP                1
#              32 STORE_FAST               2 (config)
# 
#  16          34 LOAD_FAST                1 (skill)
#              36 LOAD_ATTR                3 (NULL|self + validate)
#              56 LOAD_FAST                2 (config)
#              58 CALL                     1
#              66 UNPACK_SEQUENCE          2
#              70 STORE_FAST               3 (valid)
#              72 STORE_FAST               4 (errors)
# 
#  17          74 LOAD_CONST               4 (True)
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
# Disassembly of <code object TestTopologyIslands at 0x73cd945fe4f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 20>:
#  20           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestTopologyIslands')
#               8 STORE_NAME               2 (__qualname__)
# 
#  21          10 LOAD_CONST               1 (<code object test_check_islands_single at 0x3afabfe0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 21>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_check_islands_single)
# 
#  28          16 LOAD_CONST               2 (<code object test_check_islands_two at 0x3ae73540, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 28>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_check_islands_two)
# 
#  35          22 LOAD_CONST               3 (<code object test_check_islands_empty at 0x3aed0c90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 35>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_check_islands_empty)
#              28 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_check_islands_single at 0x3afabfe0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 21>:
#  21           0 RESUME                   0
# 
#  22           2 LOAD_GLOBAL              1 (NULL + TopologyCheckSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  23          22 LOAD_CONST               1 ('B')
#              24 BUILD_LIST               1
#              26 LOAD_CONST               2 ('A')
#              28 LOAD_CONST               3 ('C')
#              30 BUILD_LIST               2
#              32 LOAD_CONST               1 ('B')
#              34 BUILD_LIST               1
#              36 LOAD_CONST               4 (('A', 'B', 'C'))
#              38 BUILD_CONST_KEY_MAP      3
#              40 STORE_FAST               2 (adj)
# 
#  24          42 BUILD_LIST               0
#              44 LOAD_CONST               4 (('A', 'B', 'C'))
#              46 LIST_EXTEND              1
#              48 STORE_FAST               3 (nodes)
# 
#  25          50 LOAD_FAST                1 (skill)
#              52 LOAD_ATTR                3 (NULL|self + _check_islands)
#              72 LOAD_FAST                2 (adj)
#              74 LOAD_FAST                3 (nodes)
#              76 CALL                     2
#              84 STORE_FAST               4 (islands)
# 
#  26          86 LOAD_GLOBAL              5 (NULL + len)
#              96 LOAD_FAST                4 (islands)
#              98 CALL                     1
#             106 STORE_FAST               5 (@py_assert2)
#             108 LOAD_CONST               5 (1)
#             110 STORE_FAST               6 (@py_assert5)
#             112 LOAD_FAST                5 (@py_assert2)
#             114 LOAD_FAST                6 (@py_assert5)
#             116 COMPARE_OP              40 (==)
#             120 STORE_FAST               7 (@py_assert4)
#             122 LOAD_FAST                7 (@py_assert4)
#             124 POP_JUMP_IF_TRUE       246 (to 618)
#             126 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             136 LOAD_ATTR                8 (_call_reprcompare)
#             156 LOAD_CONST               6 (('==',))
#             158 LOAD_FAST                7 (@py_assert4)
#             160 BUILD_TUPLE              1
#             162 LOAD_CONST               7 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             164 LOAD_FAST                5 (@py_assert2)
#             166 LOAD_FAST                6 (@py_assert5)
#             168 BUILD_TUPLE              2
#             170 CALL                     4
#             178 LOAD_CONST               8 ('len')
#             180 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             190 LOAD_ATTR               12 (locals)
#             210 CALL                     0
#             218 CONTAINS_OP              0
#             220 POP_JUMP_IF_TRUE        25 (to 272)
#             222 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             232 LOAD_ATTR               14 (_should_repr_global_name)
#             252 LOAD_GLOBAL              4 (len)
#             262 CALL                     1
#             270 POP_JUMP_IF_FALSE       25 (to 322)
#         >>  272 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             282 LOAD_ATTR               16 (_saferepr)
#             302 LOAD_GLOBAL              4 (len)
#             312 CALL                     1
#             320 JUMP_FORWARD             1 (to 324)
#         >>  322 LOAD_CONST               8 ('len')
#         >>  324 LOAD_CONST               9 ('islands')
#             326 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             336 LOAD_ATTR               12 (locals)
#             356 CALL                     0
#             364 CONTAINS_OP              0
#             366 POP_JUMP_IF_TRUE        21 (to 410)
#             368 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             378 LOAD_ATTR               14 (_should_repr_global_name)
#             398 LOAD_FAST                4 (islands)
#             400 CALL                     1
#             408 POP_JUMP_IF_FALSE       21 (to 452)
#         >>  410 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             420 LOAD_ATTR               16 (_saferepr)
#             440 LOAD_FAST                4 (islands)
#             442 CALL                     1
#             450 JUMP_FORWARD             1 (to 454)
#         >>  452 LOAD_CONST               9 ('islands')
#         >>  454 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             464 LOAD_ATTR               16 (_saferepr)
#             484 LOAD_FAST                5 (@py_assert2)
#             486 CALL                     1
#             494 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             504 LOAD_ATTR               16 (_saferepr)
#             524 LOAD_FAST                6 (@py_assert5)
#             526 CALL                     1
#             534 LOAD_CONST              10 (('py0', 'py1', 'py3', 'py6'))
#             536 BUILD_CONST_KEY_MAP      4
#             538 BINARY_OP                6 (%)
#             542 STORE_FAST               8 (@py_format7)
#             544 LOAD_CONST              11 ('assert %(py8)s')
#             546 LOAD_CONST              12 ('py8')
#             548 LOAD_FAST                8 (@py_format7)
#             550 BUILD_MAP                1
#             552 BINARY_OP                6 (%)
#             556 STORE_FAST               9 (@py_format9)
#             558 LOAD_GLOBAL             19 (NULL + AssertionError)
#             568 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             578 LOAD_ATTR               20 (_format_explanation)
#             598 LOAD_FAST                9 (@py_format9)
#             600 CALL                     1
#             608 CALL                     1
#             616 RAISE_VARARGS            1
#         >>  618 LOAD_CONST               0 (None)
#             620 COPY                     1
#             622 STORE_FAST               5 (@py_assert2)
#             624 COPY                     1
#             626 STORE_FAST               7 (@py_assert4)
#             628 STORE_FAST               6 (@py_assert5)
#             630 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_check_islands_two at 0x3ae73540, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 28>:
#  28           0 RESUME                   0
# 
#  29           2 LOAD_GLOBAL              1 (NULL + TopologyCheckSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  30          22 LOAD_CONST               1 ('B')
#              24 BUILD_LIST               1
#              26 LOAD_CONST               2 ('A')
#              28 BUILD_LIST               1
#              30 BUILD_LIST               0
#              32 LOAD_CONST               3 (('A', 'B', 'C'))
#              34 BUILD_CONST_KEY_MAP      3
#              36 STORE_FAST               2 (adj)
# 
#  31          38 BUILD_LIST               0
#              40 LOAD_CONST               3 (('A', 'B', 'C'))
#              42 LIST_EXTEND              1
#              44 STORE_FAST               3 (nodes)
# 
#  32          46 LOAD_FAST                1 (skill)
#              48 LOAD_ATTR                3 (NULL|self + _check_islands)
#              68 LOAD_FAST                2 (adj)
#              70 LOAD_FAST                3 (nodes)
#              72 CALL                     2
#              80 STORE_FAST               4 (islands)
# 
#  33          82 LOAD_GLOBAL              5 (NULL + len)
#              92 LOAD_FAST                4 (islands)
#              94 CALL                     1
#             102 STORE_FAST               5 (@py_assert2)
#             104 LOAD_CONST               4 (2)
#             106 STORE_FAST               6 (@py_assert5)
#             108 LOAD_FAST                5 (@py_assert2)
#             110 LOAD_FAST                6 (@py_assert5)
#             112 COMPARE_OP              40 (==)
#             116 STORE_FAST               7 (@py_assert4)
#             118 LOAD_FAST                7 (@py_assert4)
#             120 POP_JUMP_IF_TRUE       246 (to 614)
#             122 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             132 LOAD_ATTR                8 (_call_reprcompare)
#             152 LOAD_CONST               5 (('==',))
#             154 LOAD_FAST                7 (@py_assert4)
#             156 BUILD_TUPLE              1
#             158 LOAD_CONST               6 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             160 LOAD_FAST                5 (@py_assert2)
#             162 LOAD_FAST                6 (@py_assert5)
#             164 BUILD_TUPLE              2
#             166 CALL                     4
#             174 LOAD_CONST               7 ('len')
#             176 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             186 LOAD_ATTR               12 (locals)
#             206 CALL                     0
#             214 CONTAINS_OP              0
#             216 POP_JUMP_IF_TRUE        25 (to 268)
#             218 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             228 LOAD_ATTR               14 (_should_repr_global_name)
#             248 LOAD_GLOBAL              4 (len)
#             258 CALL                     1
#             266 POP_JUMP_IF_FALSE       25 (to 318)
#         >>  268 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             278 LOAD_ATTR               16 (_saferepr)
#             298 LOAD_GLOBAL              4 (len)
#             308 CALL                     1
#             316 JUMP_FORWARD             1 (to 320)
#         >>  318 LOAD_CONST               7 ('len')
#         >>  320 LOAD_CONST               8 ('islands')
#             322 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             332 LOAD_ATTR               12 (locals)
#             352 CALL                     0
#             360 CONTAINS_OP              0
#             362 POP_JUMP_IF_TRUE        21 (to 406)
#             364 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             374 LOAD_ATTR               14 (_should_repr_global_name)
#             394 LOAD_FAST                4 (islands)
#             396 CALL                     1
#             404 POP_JUMP_IF_FALSE       21 (to 448)
#         >>  406 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             416 LOAD_ATTR               16 (_saferepr)
#             436 LOAD_FAST                4 (islands)
#             438 CALL                     1
#             446 JUMP_FORWARD             1 (to 450)
#         >>  448 LOAD_CONST               8 ('islands')
#         >>  450 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             460 LOAD_ATTR               16 (_saferepr)
#             480 LOAD_FAST                5 (@py_assert2)
#             482 CALL                     1
#             490 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             500 LOAD_ATTR               16 (_saferepr)
#             520 LOAD_FAST                6 (@py_assert5)
#             522 CALL                     1
#             530 LOAD_CONST               9 (('py0', 'py1', 'py3', 'py6'))
#             532 BUILD_CONST_KEY_MAP      4
#             534 BINARY_OP                6 (%)
#             538 STORE_FAST               8 (@py_format7)
#             540 LOAD_CONST              10 ('assert %(py8)s')
#             542 LOAD_CONST              11 ('py8')
#             544 LOAD_FAST                8 (@py_format7)
#             546 BUILD_MAP                1
#             548 BINARY_OP                6 (%)
#             552 STORE_FAST               9 (@py_format9)
#             554 LOAD_GLOBAL             19 (NULL + AssertionError)
#             564 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             574 LOAD_ATTR               20 (_format_explanation)
#             594 LOAD_FAST                9 (@py_format9)
#             596 CALL                     1
#             604 CALL                     1
#             612 RAISE_VARARGS            1
#         >>  614 LOAD_CONST               0 (None)
#             616 COPY                     1
#             618 STORE_FAST               5 (@py_assert2)
#             620 COPY                     1
#             622 STORE_FAST               7 (@py_assert4)
#             624 STORE_FAST               6 (@py_assert5)
#             626 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_check_islands_empty at 0x3aed0c90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 35>:
#  35           0 RESUME                   0
# 
#  36           2 LOAD_GLOBAL              1 (NULL + TopologyCheckSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  37          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _check_islands)
#              44 BUILD_MAP                0
#              46 BUILD_LIST               0
#              48 CALL                     2
#              56 STORE_FAST               2 (islands)
# 
#  38          58 LOAD_GLOBAL              5 (NULL + len)
#              68 LOAD_FAST                2 (islands)
#              70 CALL                     1
#              78 STORE_FAST               3 (@py_assert2)
#              80 LOAD_CONST               1 (0)
#              82 STORE_FAST               4 (@py_assert5)
#              84 LOAD_FAST                3 (@py_assert2)
#              86 LOAD_FAST                4 (@py_assert5)
#              88 COMPARE_OP              40 (==)
#              92 STORE_FAST               5 (@py_assert4)
#              94 LOAD_FAST                5 (@py_assert4)
#              96 POP_JUMP_IF_TRUE       246 (to 590)
#              98 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             108 LOAD_ATTR                8 (_call_reprcompare)
#             128 LOAD_CONST               2 (('==',))
#             130 LOAD_FAST                5 (@py_assert4)
#             132 BUILD_TUPLE              1
#             134 LOAD_CONST               3 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             136 LOAD_FAST                3 (@py_assert2)
#             138 LOAD_FAST                4 (@py_assert5)
#             140 BUILD_TUPLE              2
#             142 CALL                     4
#             150 LOAD_CONST               4 ('len')
#             152 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             162 LOAD_ATTR               12 (locals)
#             182 CALL                     0
#             190 CONTAINS_OP              0
#             192 POP_JUMP_IF_TRUE        25 (to 244)
#             194 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             204 LOAD_ATTR               14 (_should_repr_global_name)
#             224 LOAD_GLOBAL              4 (len)
#             234 CALL                     1
#             242 POP_JUMP_IF_FALSE       25 (to 294)
#         >>  244 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             254 LOAD_ATTR               16 (_saferepr)
#             274 LOAD_GLOBAL              4 (len)
#             284 CALL                     1
#             292 JUMP_FORWARD             1 (to 296)
#         >>  294 LOAD_CONST               4 ('len')
#         >>  296 LOAD_CONST               5 ('islands')
#             298 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             308 LOAD_ATTR               12 (locals)
#             328 CALL                     0
#             336 CONTAINS_OP              0
#             338 POP_JUMP_IF_TRUE        21 (to 382)
#             340 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             350 LOAD_ATTR               14 (_should_repr_global_name)
#             370 LOAD_FAST                2 (islands)
#             372 CALL                     1
#             380 POP_JUMP_IF_FALSE       21 (to 424)
#         >>  382 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             392 LOAD_ATTR               16 (_saferepr)
#             412 LOAD_FAST                2 (islands)
#             414 CALL                     1
#             422 JUMP_FORWARD             1 (to 426)
#         >>  424 LOAD_CONST               5 ('islands')
#         >>  426 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             436 LOAD_ATTR               16 (_saferepr)
#             456 LOAD_FAST                3 (@py_assert2)
#             458 CALL                     1
#             466 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             476 LOAD_ATTR               16 (_saferepr)
#             496 LOAD_FAST                4 (@py_assert5)
#             498 CALL                     1
#             506 LOAD_CONST               6 (('py0', 'py1', 'py3', 'py6'))
#             508 BUILD_CONST_KEY_MAP      4
#             510 BINARY_OP                6 (%)
#             514 STORE_FAST               6 (@py_format7)
#             516 LOAD_CONST               7 ('assert %(py8)s')
#             518 LOAD_CONST               8 ('py8')
#             520 LOAD_FAST                6 (@py_format7)
#             522 BUILD_MAP                1
#             524 BINARY_OP                6 (%)
#             528 STORE_FAST               7 (@py_format9)
#             530 LOAD_GLOBAL             19 (NULL + AssertionError)
#             540 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             550 LOAD_ATTR               20 (_format_explanation)
#             570 LOAD_FAST                7 (@py_format9)
#             572 CALL                     1
#             580 CALL                     1
#             588 RAISE_VARARGS            1
#         >>  590 LOAD_CONST               0 (None)
#             592 COPY                     1
#             594 STORE_FAST               3 (@py_assert2)
#             596 COPY                     1
#             598 STORE_FAST               5 (@py_assert4)
#             600 STORE_FAST               4 (@py_assert5)
#             602 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestTopologyDangling at 0x73cd945fedb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 41>:
#  41           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestTopologyDangling')
#               8 STORE_NAME               2 (__qualname__)
# 
#  42          10 LOAD_CONST               1 (<code object test_check_dangling at 0x3afac750, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 42>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_check_dangling)
# 
#  52          16 LOAD_CONST               2 (<code object test_check_dangling_none at 0x3af9a2d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 52>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_check_dangling_none)
#              22 RETURN_CONST             3 (None)
# 
# Disassembly of <code object test_check_dangling at 0x3afac750, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 42>:
#  42           0 RESUME                   0
# 
#  43           2 LOAD_GLOBAL              1 (NULL + TopologyCheckSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  45          22 LOAD_CONST               1 ('L1')
#              24 LOAD_CONST               2 ('Line1')
#              26 LOAD_CONST               3 ('Bus1')
#              28 LOAD_CONST               4 ('Bus2')
#              30 LOAD_CONST               5 (('0', '1'))
#              32 BUILD_CONST_KEY_MAP      2
#              34 LOAD_CONST               6 (('id', 'name', 'pins'))
#              36 BUILD_CONST_KEY_MAP      3
# 
#  46          38 LOAD_CONST               7 ('L2')
#              40 LOAD_CONST               8 ('Line2')
#              42 LOAD_CONST               9 ('Bus3')
#              44 LOAD_CONST              10 ('')
#              46 LOAD_CONST               5 (('0', '1'))
#              48 BUILD_CONST_KEY_MAP      2
#              50 LOAD_CONST               6 (('id', 'name', 'pins'))
#              52 BUILD_CONST_KEY_MAP      3
# 
#  44          54 BUILD_LIST               2
#              56 STORE_FAST               2 (components)
# 
#  48          58 LOAD_FAST                1 (skill)
#              60 LOAD_ATTR                3 (NULL|self + _check_dangling)
#              80 LOAD_FAST                2 (components)
#              82 CALL                     1
#              90 STORE_FAST               3 (dangling)
# 
#  49          92 LOAD_GLOBAL              5 (NULL + len)
#             102 LOAD_FAST                3 (dangling)
#             104 CALL                     1
#             112 STORE_FAST               4 (@py_assert2)
#             114 LOAD_CONST              11 (1)
#             116 STORE_FAST               5 (@py_assert5)
#             118 LOAD_FAST                4 (@py_assert2)
#             120 LOAD_FAST                5 (@py_assert5)
#             122 COMPARE_OP              40 (==)
#             126 STORE_FAST               6 (@py_assert4)
#             128 LOAD_FAST                6 (@py_assert4)
#             130 POP_JUMP_IF_TRUE       246 (to 624)
#             132 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             142 LOAD_ATTR                8 (_call_reprcompare)
#             162 LOAD_CONST              12 (('==',))
#             164 LOAD_FAST                6 (@py_assert4)
#             166 BUILD_TUPLE              1
#             168 LOAD_CONST              13 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             170 LOAD_FAST                4 (@py_assert2)
#             172 LOAD_FAST                5 (@py_assert5)
#             174 BUILD_TUPLE              2
#             176 CALL                     4
#             184 LOAD_CONST              14 ('len')
#             186 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             196 LOAD_ATTR               12 (locals)
#             216 CALL                     0
#             224 CONTAINS_OP              0
#             226 POP_JUMP_IF_TRUE        25 (to 278)
#             228 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             238 LOAD_ATTR               14 (_should_repr_global_name)
#             258 LOAD_GLOBAL              4 (len)
#             268 CALL                     1
#             276 POP_JUMP_IF_FALSE       25 (to 328)
#         >>  278 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             288 LOAD_ATTR               16 (_saferepr)
#             308 LOAD_GLOBAL              4 (len)
#             318 CALL                     1
#             326 JUMP_FORWARD             1 (to 330)
#         >>  328 LOAD_CONST              14 ('len')
#         >>  330 LOAD_CONST              15 ('dangling')
#             332 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             342 LOAD_ATTR               12 (locals)
#             362 CALL                     0
#             370 CONTAINS_OP              0
#             372 POP_JUMP_IF_TRUE        21 (to 416)
#             374 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             384 LOAD_ATTR               14 (_should_repr_global_name)
#             404 LOAD_FAST                3 (dangling)
#             406 CALL                     1
#             414 POP_JUMP_IF_FALSE       21 (to 458)
#         >>  416 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             426 LOAD_ATTR               16 (_saferepr)
#             446 LOAD_FAST                3 (dangling)
#             448 CALL                     1
#             456 JUMP_FORWARD             1 (to 460)
#         >>  458 LOAD_CONST              15 ('dangling')
#         >>  460 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             470 LOAD_ATTR               16 (_saferepr)
#             490 LOAD_FAST                4 (@py_assert2)
#             492 CALL                     1
#             500 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             510 LOAD_ATTR               16 (_saferepr)
#             530 LOAD_FAST                5 (@py_assert5)
#             532 CALL                     1
#             540 LOAD_CONST              16 (('py0', 'py1', 'py3', 'py6'))
#             542 BUILD_CONST_KEY_MAP      4
#             544 BINARY_OP                6 (%)
#             548 STORE_FAST               7 (@py_format7)
#             550 LOAD_CONST              17 ('assert %(py8)s')
#             552 LOAD_CONST              18 ('py8')
#             554 LOAD_FAST                7 (@py_format7)
#             556 BUILD_MAP                1
#             558 BINARY_OP                6 (%)
#             562 STORE_FAST               8 (@py_format9)
#             564 LOAD_GLOBAL             19 (NULL + AssertionError)
#             574 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             584 LOAD_ATTR               20 (_format_explanation)
#             604 LOAD_FAST                8 (@py_format9)
#             606 CALL                     1
#             614 CALL                     1
#             622 RAISE_VARARGS            1
#         >>  624 LOAD_CONST               0 (None)
#             626 COPY                     1
#             628 STORE_FAST               4 (@py_assert2)
#             630 COPY                     1
#             632 STORE_FAST               6 (@py_assert4)
#             634 STORE_FAST               5 (@py_assert5)
# 
#  50         636 LOAD_FAST                3 (dangling)
#             638 LOAD_CONST              19 (0)
#             640 BINARY_SUBSCR
#             644 LOAD_CONST              20 ('id')
#             646 BINARY_SUBSCR
#             650 STORE_FAST               9 (@py_assert0)
#             652 LOAD_CONST               7 ('L2')
#             654 STORE_FAST              10 (@py_assert3)
#             656 LOAD_FAST                9 (@py_assert0)
#             658 LOAD_FAST               10 (@py_assert3)
#             660 COMPARE_OP              40 (==)
#             664 STORE_FAST               4 (@py_assert2)
#             666 LOAD_FAST                4 (@py_assert2)
#             668 POP_JUMP_IF_TRUE       108 (to 886)
#             670 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             680 LOAD_ATTR                8 (_call_reprcompare)
#             700 LOAD_CONST              12 (('==',))
#             702 LOAD_FAST                4 (@py_assert2)
#             704 BUILD_TUPLE              1
#             706 LOAD_CONST              21 (('%(py1)s == %(py4)s',))
#             708 LOAD_FAST                9 (@py_assert0)
#             710 LOAD_FAST               10 (@py_assert3)
#             712 BUILD_TUPLE              2
#             714 CALL                     4
#             722 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             732 LOAD_ATTR               16 (_saferepr)
#             752 LOAD_FAST                9 (@py_assert0)
#             754 CALL                     1
#             762 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             772 LOAD_ATTR               16 (_saferepr)
#             792 LOAD_FAST               10 (@py_assert3)
#             794 CALL                     1
#             802 LOAD_CONST              22 (('py1', 'py4'))
#             804 BUILD_CONST_KEY_MAP      2
#             806 BINARY_OP                6 (%)
#             810 STORE_FAST              11 (@py_format5)
#             812 LOAD_CONST              23 ('assert %(py6)s')
#             814 LOAD_CONST              24 ('py6')
#             816 LOAD_FAST               11 (@py_format5)
#             818 BUILD_MAP                1
#             820 BINARY_OP                6 (%)
#             824 STORE_FAST               7 (@py_format7)
#             826 LOAD_GLOBAL             19 (NULL + AssertionError)
#             836 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             846 LOAD_ATTR               20 (_format_explanation)
#             866 LOAD_FAST                7 (@py_format7)
#             868 CALL                     1
#             876 CALL                     1
#             884 RAISE_VARARGS            1
#         >>  886 LOAD_CONST               0 (None)
#             888 COPY                     1
#             890 STORE_FAST               9 (@py_assert0)
#             892 COPY                     1
#             894 STORE_FAST               4 (@py_assert2)
#             896 STORE_FAST              10 (@py_assert3)
#             898 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_check_dangling_none at 0x3af9a2d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 52>:
#  52           0 RESUME                   0
# 
#  53           2 LOAD_GLOBAL              1 (NULL + TopologyCheckSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  55          22 LOAD_CONST               1 ('L1')
#              24 LOAD_CONST               2 ('Line1')
#              26 LOAD_CONST               3 ('Bus1')
#              28 LOAD_CONST               4 ('Bus2')
#              30 LOAD_CONST               5 (('0', '1'))
#              32 BUILD_CONST_KEY_MAP      2
#              34 LOAD_CONST               6 (('id', 'name', 'pins'))
#              36 BUILD_CONST_KEY_MAP      3
# 
#  54          38 BUILD_LIST               1
#              40 STORE_FAST               2 (components)
# 
#  57          42 LOAD_FAST                1 (skill)
#              44 LOAD_ATTR                3 (NULL|self + _check_dangling)
#              64 LOAD_FAST                2 (components)
#              66 CALL                     1
#              74 STORE_FAST               3 (dangling)
# 
#  58          76 LOAD_GLOBAL              5 (NULL + len)
#              86 LOAD_FAST                3 (dangling)
#              88 CALL                     1
#              96 STORE_FAST               4 (@py_assert2)
#              98 LOAD_CONST               7 (0)
#             100 STORE_FAST               5 (@py_assert5)
#             102 LOAD_FAST                4 (@py_assert2)
#             104 LOAD_FAST                5 (@py_assert5)
#             106 COMPARE_OP              40 (==)
#             110 STORE_FAST               6 (@py_assert4)
#             112 LOAD_FAST                6 (@py_assert4)
#             114 POP_JUMP_IF_TRUE       246 (to 608)
#             116 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             126 LOAD_ATTR                8 (_call_reprcompare)
#             146 LOAD_CONST               8 (('==',))
#             148 LOAD_FAST                6 (@py_assert4)
#             150 BUILD_TUPLE              1
#             152 LOAD_CONST               9 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             154 LOAD_FAST                4 (@py_assert2)
#             156 LOAD_FAST                5 (@py_assert5)
#             158 BUILD_TUPLE              2
#             160 CALL                     4
#             168 LOAD_CONST              10 ('len')
#             170 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             180 LOAD_ATTR               12 (locals)
#             200 CALL                     0
#             208 CONTAINS_OP              0
#             210 POP_JUMP_IF_TRUE        25 (to 262)
#             212 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             222 LOAD_ATTR               14 (_should_repr_global_name)
#             242 LOAD_GLOBAL              4 (len)
#             252 CALL                     1
#             260 POP_JUMP_IF_FALSE       25 (to 312)
#         >>  262 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             272 LOAD_ATTR               16 (_saferepr)
#             292 LOAD_GLOBAL              4 (len)
#             302 CALL                     1
#             310 JUMP_FORWARD             1 (to 314)
#         >>  312 LOAD_CONST              10 ('len')
#         >>  314 LOAD_CONST              11 ('dangling')
#             316 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             326 LOAD_ATTR               12 (locals)
#             346 CALL                     0
#             354 CONTAINS_OP              0
#             356 POP_JUMP_IF_TRUE        21 (to 400)
#             358 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             368 LOAD_ATTR               14 (_should_repr_global_name)
#             388 LOAD_FAST                3 (dangling)
#             390 CALL                     1
#             398 POP_JUMP_IF_FALSE       21 (to 442)
#         >>  400 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             410 LOAD_ATTR               16 (_saferepr)
#             430 LOAD_FAST                3 (dangling)
#             432 CALL                     1
#             440 JUMP_FORWARD             1 (to 444)
#         >>  442 LOAD_CONST              11 ('dangling')
#         >>  444 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             454 LOAD_ATTR               16 (_saferepr)
#             474 LOAD_FAST                4 (@py_assert2)
#             476 CALL                     1
#             484 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             494 LOAD_ATTR               16 (_saferepr)
#             514 LOAD_FAST                5 (@py_assert5)
#             516 CALL                     1
#             524 LOAD_CONST              12 (('py0', 'py1', 'py3', 'py6'))
#             526 BUILD_CONST_KEY_MAP      4
#             528 BINARY_OP                6 (%)
#             532 STORE_FAST               7 (@py_format7)
#             534 LOAD_CONST              13 ('assert %(py8)s')
#             536 LOAD_CONST              14 ('py8')
#             538 LOAD_FAST                7 (@py_format7)
#             540 BUILD_MAP                1
#             542 BINARY_OP                6 (%)
#             546 STORE_FAST               8 (@py_format9)
#             548 LOAD_GLOBAL             19 (NULL + AssertionError)
#             558 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             568 LOAD_ATTR               20 (_format_explanation)
#             588 LOAD_FAST                8 (@py_format9)
#             590 CALL                     1
#             598 CALL                     1
#             606 RAISE_VARARGS            1
#         >>  608 LOAD_CONST               0 (None)
#             610 COPY                     1
#             612 STORE_FAST               4 (@py_assert2)
#             614 COPY                     1
#             616 STORE_FAST               6 (@py_assert4)
#             618 STORE_FAST               5 (@py_assert5)
#             620 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestTopologyParameters at 0x73cd945ff590, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 61>:
#  61           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestTopologyParameters')
#               8 STORE_NAME               2 (__qualname__)
# 
#  62          10 LOAD_CONST               1 (<code object test_check_parameters_incomplete at 0x3af9b9b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 62>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_check_parameters_incomplete)
# 
#  70          16 LOAD_CONST               2 (<code object test_check_parameters_complete at 0x3af8ede0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 70>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_check_parameters_complete)
#              22 RETURN_CONST             3 (None)
# 
# Disassembly of <code object test_check_parameters_incomplete at 0x3af9b9b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 62>:
#  62           0 RESUME                   0
# 
#  63           2 LOAD_GLOBAL              1 (NULL + TopologyCheckSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  65          22 LOAD_CONST               1 ('G1')
#              24 LOAD_CONST               2 ('Gen1')
#              26 LOAD_CONST               3 (100)
#              28 LOAD_CONST               4 ('')
#              30 LOAD_CONST               5 (('P', 'Q'))
#              32 BUILD_CONST_KEY_MAP      2
#              34 LOAD_CONST               6 (('id', 'name', 'args'))
#              36 BUILD_CONST_KEY_MAP      3
# 
#  64          38 BUILD_LIST               1
#              40 STORE_FAST               2 (components)
# 
#  67          42 LOAD_FAST                1 (skill)
#              44 LOAD_ATTR                3 (NULL|self + _check_parameters)
#              64 LOAD_FAST                2 (components)
#              66 CALL                     1
#              74 STORE_FAST               3 (incomplete)
# 
#  68          76 LOAD_GLOBAL              5 (NULL + len)
#              86 LOAD_FAST                3 (incomplete)
#              88 CALL                     1
#              96 STORE_FAST               4 (@py_assert2)
#              98 LOAD_CONST               7 (1)
#             100 STORE_FAST               5 (@py_assert5)
#             102 LOAD_FAST                4 (@py_assert2)
#             104 LOAD_FAST                5 (@py_assert5)
#             106 COMPARE_OP              40 (==)
#             110 STORE_FAST               6 (@py_assert4)
#             112 LOAD_FAST                6 (@py_assert4)
#             114 POP_JUMP_IF_TRUE       246 (to 608)
#             116 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             126 LOAD_ATTR                8 (_call_reprcompare)
#             146 LOAD_CONST               8 (('==',))
#             148 LOAD_FAST                6 (@py_assert4)
#             150 BUILD_TUPLE              1
#             152 LOAD_CONST               9 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             154 LOAD_FAST                4 (@py_assert2)
#             156 LOAD_FAST                5 (@py_assert5)
#             158 BUILD_TUPLE              2
#             160 CALL                     4
#             168 LOAD_CONST              10 ('len')
#             170 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             180 LOAD_ATTR               12 (locals)
#             200 CALL                     0
#             208 CONTAINS_OP              0
#             210 POP_JUMP_IF_TRUE        25 (to 262)
#             212 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             222 LOAD_ATTR               14 (_should_repr_global_name)
#             242 LOAD_GLOBAL              4 (len)
#             252 CALL                     1
#             260 POP_JUMP_IF_FALSE       25 (to 312)
#         >>  262 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             272 LOAD_ATTR               16 (_saferepr)
#             292 LOAD_GLOBAL              4 (len)
#             302 CALL                     1
#             310 JUMP_FORWARD             1 (to 314)
#         >>  312 LOAD_CONST              10 ('len')
#         >>  314 LOAD_CONST              11 ('incomplete')
#             316 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             326 LOAD_ATTR               12 (locals)
#             346 CALL                     0
#             354 CONTAINS_OP              0
#             356 POP_JUMP_IF_TRUE        21 (to 400)
#             358 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             368 LOAD_ATTR               14 (_should_repr_global_name)
#             388 LOAD_FAST                3 (incomplete)
#             390 CALL                     1
#             398 POP_JUMP_IF_FALSE       21 (to 442)
#         >>  400 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             410 LOAD_ATTR               16 (_saferepr)
#             430 LOAD_FAST                3 (incomplete)
#             432 CALL                     1
#             440 JUMP_FORWARD             1 (to 444)
#         >>  442 LOAD_CONST              11 ('incomplete')
#         >>  444 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             454 LOAD_ATTR               16 (_saferepr)
#             474 LOAD_FAST                4 (@py_assert2)
#             476 CALL                     1
#             484 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             494 LOAD_ATTR               16 (_saferepr)
#             514 LOAD_FAST                5 (@py_assert5)
#             516 CALL                     1
#             524 LOAD_CONST              12 (('py0', 'py1', 'py3', 'py6'))
#             526 BUILD_CONST_KEY_MAP      4
#             528 BINARY_OP                6 (%)
#             532 STORE_FAST               7 (@py_format7)
#             534 LOAD_CONST              13 ('assert %(py8)s')
#             536 LOAD_CONST              14 ('py8')
#             538 LOAD_FAST                7 (@py_format7)
#             540 BUILD_MAP                1
#             542 BINARY_OP                6 (%)
#             546 STORE_FAST               8 (@py_format9)
#             548 LOAD_GLOBAL             19 (NULL + AssertionError)
#             558 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             568 LOAD_ATTR               20 (_format_explanation)
#             588 LOAD_FAST                8 (@py_format9)
#             590 CALL                     1
#             598 CALL                     1
#             606 RAISE_VARARGS            1
#         >>  608 LOAD_CONST               0 (None)
#             610 COPY                     1
#             612 STORE_FAST               4 (@py_assert2)
#             614 COPY                     1
#             616 STORE_FAST               6 (@py_assert4)
#             618 STORE_FAST               5 (@py_assert5)
#             620 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_check_parameters_complete at 0x3af8ede0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 70>:
#  70           0 RESUME                   0
# 
#  71           2 LOAD_GLOBAL              1 (NULL + TopologyCheckSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  73          22 LOAD_CONST               1 ('G1')
#              24 LOAD_CONST               2 ('Gen1')
#              26 LOAD_CONST               3 (100)
#              28 LOAD_CONST               4 (50)
#              30 LOAD_CONST               5 (('P', 'Q'))
#              32 BUILD_CONST_KEY_MAP      2
#              34 LOAD_CONST               6 (('id', 'name', 'args'))
#              36 BUILD_CONST_KEY_MAP      3
# 
#  72          38 BUILD_LIST               1
#              40 STORE_FAST               2 (components)
# 
#  75          42 LOAD_FAST                1 (skill)
#              44 LOAD_ATTR                3 (NULL|self + _check_parameters)
#              64 LOAD_FAST                2 (components)
#              66 CALL                     1
#              74 STORE_FAST               3 (incomplete)
# 
#  76          76 LOAD_GLOBAL              5 (NULL + len)
#              86 LOAD_FAST                3 (incomplete)
#              88 CALL                     1
#              96 STORE_FAST               4 (@py_assert2)
#              98 LOAD_CONST               7 (0)
#             100 STORE_FAST               5 (@py_assert5)
#             102 LOAD_FAST                4 (@py_assert2)
#             104 LOAD_FAST                5 (@py_assert5)
#             106 COMPARE_OP              40 (==)
#             110 STORE_FAST               6 (@py_assert4)
#             112 LOAD_FAST                6 (@py_assert4)
#             114 POP_JUMP_IF_TRUE       246 (to 608)
#             116 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             126 LOAD_ATTR                8 (_call_reprcompare)
#             146 LOAD_CONST               8 (('==',))
#             148 LOAD_FAST                6 (@py_assert4)
#             150 BUILD_TUPLE              1
#             152 LOAD_CONST               9 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             154 LOAD_FAST                4 (@py_assert2)
#             156 LOAD_FAST                5 (@py_assert5)
#             158 BUILD_TUPLE              2
#             160 CALL                     4
#             168 LOAD_CONST              10 ('len')
#             170 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             180 LOAD_ATTR               12 (locals)
#             200 CALL                     0
#             208 CONTAINS_OP              0
#             210 POP_JUMP_IF_TRUE        25 (to 262)
#             212 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             222 LOAD_ATTR               14 (_should_repr_global_name)
#             242 LOAD_GLOBAL              4 (len)
#             252 CALL                     1
#             260 POP_JUMP_IF_FALSE       25 (to 312)
#         >>  262 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             272 LOAD_ATTR               16 (_saferepr)
#             292 LOAD_GLOBAL              4 (len)
#             302 CALL                     1
#             310 JUMP_FORWARD             1 (to 314)
#         >>  312 LOAD_CONST              10 ('len')
#         >>  314 LOAD_CONST              11 ('incomplete')
#             316 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             326 LOAD_ATTR               12 (locals)
#             346 CALL                     0
#             354 CONTAINS_OP              0
#             356 POP_JUMP_IF_TRUE        21 (to 400)
#             358 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             368 LOAD_ATTR               14 (_should_repr_global_name)
#             388 LOAD_FAST                3 (incomplete)
#             390 CALL                     1
#             398 POP_JUMP_IF_FALSE       21 (to 442)
#         >>  400 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             410 LOAD_ATTR               16 (_saferepr)
#             430 LOAD_FAST                3 (incomplete)
#             432 CALL                     1
#             440 JUMP_FORWARD             1 (to 444)
#         >>  442 LOAD_CONST              11 ('incomplete')
#         >>  444 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             454 LOAD_ATTR               16 (_saferepr)
#             474 LOAD_FAST                4 (@py_assert2)
#             476 CALL                     1
#             484 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             494 LOAD_ATTR               16 (_saferepr)
#             514 LOAD_FAST                5 (@py_assert5)
#             516 CALL                     1
#             524 LOAD_CONST              12 (('py0', 'py1', 'py3', 'py6'))
#             526 BUILD_CONST_KEY_MAP      4
#             528 BINARY_OP                6 (%)
#             532 STORE_FAST               7 (@py_format7)
#             534 LOAD_CONST              13 ('assert %(py8)s')
#             536 LOAD_CONST              14 ('py8')
#             538 LOAD_FAST                7 (@py_format7)
#             540 BUILD_MAP                1
#             542 BINARY_OP                6 (%)
#             546 STORE_FAST               8 (@py_format9)
#             548 LOAD_GLOBAL             19 (NULL + AssertionError)
#             558 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             568 LOAD_ATTR               20 (_format_explanation)
#             588 LOAD_FAST                8 (@py_format9)
#             590 CALL                     1
#             598 CALL                     1
#             606 RAISE_VARARGS            1
#         >>  608 LOAD_CONST               0 (None)
#             610 COPY                     1
#             612 STORE_FAST               4 (@py_assert2)
#             614 COPY                     1
#             616 STORE_FAST               6 (@py_assert4)
#             618 STORE_FAST               5 (@py_assert5)
#             620 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestTopologyAdjacency at 0x73cd945fecd0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 79>:
#  79           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestTopologyAdjacency')
#               8 STORE_NAME               2 (__qualname__)
# 
#  80          10 LOAD_CONST               1 (<code object test_build_adjacency at 0x3af9ce50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 80>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_build_adjacency)
#              16 RETURN_CONST             2 (None)
# 
# Disassembly of <code object test_build_adjacency at 0x3af9ce50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 80>:
#  80           0 RESUME                   0
# 
#  81           2 LOAD_GLOBAL              1 (NULL + TopologyCheckSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  82          22 BUILD_LIST               0
#              24 LOAD_CONST               1 ((('A', 'B'), ('B', 'C'), ('C', 'A')))
#              26 LIST_EXTEND              1
#              28 STORE_FAST               2 (connections)
# 
#  83          30 LOAD_FAST                1 (skill)
#              32 LOAD_ATTR                3 (NULL|self + _build_adjacency)
#              52 LOAD_FAST                2 (connections)
#              54 CALL                     1
#              62 STORE_FAST               3 (adj)
# 
#  84          64 LOAD_CONST               2 ('A')
#              66 STORE_FAST               4 (@py_assert0)
#              68 LOAD_FAST                3 (adj)
#              70 LOAD_CONST               3 ('B')
#              72 BINARY_SUBSCR
#              76 STORE_FAST               5 (@py_assert3)
#              78 LOAD_FAST                4 (@py_assert0)
#              80 LOAD_FAST                5 (@py_assert3)
#              82 CONTAINS_OP              0
#              84 STORE_FAST               6 (@py_assert2)
#              86 LOAD_FAST                6 (@py_assert2)
#              88 POP_JUMP_IF_TRUE       108 (to 306)
#              90 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             100 LOAD_ATTR                6 (_call_reprcompare)
#             120 LOAD_CONST               4 (('in',))
#             122 LOAD_FAST                6 (@py_assert2)
#             124 BUILD_TUPLE              1
#             126 LOAD_CONST               5 (('%(py1)s in %(py4)s',))
#             128 LOAD_FAST                4 (@py_assert0)
#             130 LOAD_FAST                5 (@py_assert3)
#             132 BUILD_TUPLE              2
#             134 CALL                     4
#             142 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             152 LOAD_ATTR                8 (_saferepr)
#             172 LOAD_FAST                4 (@py_assert0)
#             174 CALL                     1
#             182 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             192 LOAD_ATTR                8 (_saferepr)
#             212 LOAD_FAST                5 (@py_assert3)
#             214 CALL                     1
#             222 LOAD_CONST               6 (('py1', 'py4'))
#             224 BUILD_CONST_KEY_MAP      2
#             226 BINARY_OP                6 (%)
#             230 STORE_FAST               7 (@py_format5)
#             232 LOAD_CONST               7 ('assert %(py6)s')
#             234 LOAD_CONST               8 ('py6')
#             236 LOAD_FAST                7 (@py_format5)
#             238 BUILD_MAP                1
#             240 BINARY_OP                6 (%)
#             244 STORE_FAST               8 (@py_format7)
#             246 LOAD_GLOBAL             11 (NULL + AssertionError)
#             256 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             266 LOAD_ATTR               12 (_format_explanation)
#             286 LOAD_FAST                8 (@py_format7)
#             288 CALL                     1
#             296 CALL                     1
#             304 RAISE_VARARGS            1
#         >>  306 LOAD_CONST               0 (None)
#             308 COPY                     1
#             310 STORE_FAST               4 (@py_assert0)
#             312 COPY                     1
#             314 STORE_FAST               6 (@py_assert2)
#             316 STORE_FAST               5 (@py_assert3)
# 
#  85         318 LOAD_CONST               3 ('B')
#             320 STORE_FAST               4 (@py_assert0)
#             322 LOAD_FAST                3 (adj)
#             324 LOAD_CONST               2 ('A')
#             326 BINARY_SUBSCR
#             330 STORE_FAST               5 (@py_assert3)
#             332 LOAD_FAST                4 (@py_assert0)
#             334 LOAD_FAST                5 (@py_assert3)
#             336 CONTAINS_OP              0
#             338 STORE_FAST               6 (@py_assert2)
#             340 LOAD_FAST                6 (@py_assert2)
#             342 POP_JUMP_IF_TRUE       108 (to 560)
#             344 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             354 LOAD_ATTR                6 (_call_reprcompare)
#             374 LOAD_CONST               4 (('in',))
#             376 LOAD_FAST                6 (@py_assert2)
#             378 BUILD_TUPLE              1
#             380 LOAD_CONST               5 (('%(py1)s in %(py4)s',))
#             382 LOAD_FAST                4 (@py_assert0)
#             384 LOAD_FAST                5 (@py_assert3)
#             386 BUILD_TUPLE              2
#             388 CALL                     4
#             396 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             406 LOAD_ATTR                8 (_saferepr)
#             426 LOAD_FAST                4 (@py_assert0)
#             428 CALL                     1
#             436 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             446 LOAD_ATTR                8 (_saferepr)
#             466 LOAD_FAST                5 (@py_assert3)
#             468 CALL                     1
#             476 LOAD_CONST               6 (('py1', 'py4'))
#             478 BUILD_CONST_KEY_MAP      2
#             480 BINARY_OP                6 (%)
#             484 STORE_FAST               7 (@py_format5)
#             486 LOAD_CONST               7 ('assert %(py6)s')
#             488 LOAD_CONST               8 ('py6')
#             490 LOAD_FAST                7 (@py_format5)
#             492 BUILD_MAP                1
#             494 BINARY_OP                6 (%)
#             498 STORE_FAST               8 (@py_format7)
#             500 LOAD_GLOBAL             11 (NULL + AssertionError)
#             510 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             520 LOAD_ATTR               12 (_format_explanation)
#             540 LOAD_FAST                8 (@py_format7)
#             542 CALL                     1
#             550 CALL                     1
#             558 RAISE_VARARGS            1
#         >>  560 LOAD_CONST               0 (None)
#             562 COPY                     1
#             564 STORE_FAST               4 (@py_assert0)
#             566 COPY                     1
#             568 STORE_FAST               6 (@py_assert2)
#             570 STORE_FAST               5 (@py_assert3)
#             572 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestTopologyRun at 0x73cd945fe870, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 88>:
#  88           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestTopologyRun')
#               8 STORE_NAME               2 (__qualname__)
# 
#  89          10 LOAD_CONST               1 (<code object test_run_invalid_config_returns_failure at 0x3af9ee00, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 89>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_run_invalid_config_returns_failure)
#              16 RETURN_CONST             2 (None)
# 
# Disassembly of <code object test_run_invalid_config_returns_failure at 0x3af9ee00, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_topology_check.py", line 89>:
#  89           0 RESUME                   0
# 
#  90           2 LOAD_GLOBAL              1 (NULL + TopologyCheckSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  91          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + run)
#              44 BUILD_MAP                0
#              46 CALL                     1
#              54 STORE_FAST               2 (result)
# 
#  92          56 LOAD_FAST                2 (result)
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