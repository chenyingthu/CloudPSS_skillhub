# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/__pycache__/test_skills_integration.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


def TestPowerFlowSkillIntegration():
    """TestPowerFlowSkillIntegration"""
pass  # TODO: restore


def TestEMTSkillIntegration():
    """TestEMTSkillIntegration"""
pass  # TODO: restore


def TestShortCircuitSkillIntegration():
    """TestShortCircuitSkillIntegration"""
pass  # TODO: restore


def TestSkillOutputCompliance():
    """TestSkillOutputCompliance"""
pass  # TODO: restore


def TestValidatorWithAllSkills():
    """TestValidatorWithAllSkills"""
pass  # TODO: restore


def TestSkillResultToDict():
    """TestSkillResultToDict"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('Integration tests for all skills with output standard compliance.')
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
#              42 LOAD_CONST               3 (('MagicMock', 'patch'))
#              44 IMPORT_NAME              8 (unittest.mock)
#              46 IMPORT_FROM              9 (MagicMock)
#              48 STORE_NAME               9 (MagicMock)
#              50 IMPORT_FROM             10 (patch)
#              52 STORE_NAME              10 (patch)
#              54 POP_TOP
# 
#   5          56 LOAD_CONST               1 (0)
#              58 LOAD_CONST               4 (('PowerFlowSkill', 'EMTSimulationSkill', 'ShortCircuitSkill'))
#              60 IMPORT_NAME             11 (cloudpss_skills_v2.skills)
#              62 IMPORT_FROM             12 (PowerFlowSkill)
#              64 STORE_NAME              12 (PowerFlowSkill)
#              66 IMPORT_FROM             13 (EMTSimulationSkill)
#              68 STORE_NAME              13 (EMTSimulationSkill)
#              70 IMPORT_FROM             14 (ShortCircuitSkill)
#              72 STORE_NAME              14 (ShortCircuitSkill)
#              74 POP_TOP
# 
#  10          76 LOAD_CONST               1 (0)
#              78 LOAD_CONST               5 (('SkillResult', 'SkillStatus', 'SkillOutputValidator'))
#              80 IMPORT_NAME             15 (cloudpss_skills_v2.core)
#              82 IMPORT_FROM             16 (SkillResult)
#              84 STORE_NAME              16 (SkillResult)
#              86 IMPORT_FROM             17 (SkillStatus)
#              88 STORE_NAME              17 (SkillStatus)
#              90 IMPORT_FROM             18 (SkillOutputValidator)
#              92 STORE_NAME              18 (SkillOutputValidator)
#              94 POP_TOP
# 
#  11          96 LOAD_CONST               1 (0)
#              98 LOAD_CONST               6 (('SimulationResult', 'SimulationStatus'))
#             100 IMPORT_NAME             19 (cloudpss_skills_v2.powerapi)
#             102 IMPORT_FROM             20 (SimulationResult)
#             104 STORE_NAME              20 (SimulationResult)
#             106 IMPORT_FROM             21 (SimulationStatus)
#             108 STORE_NAME              21 (SimulationStatus)
#             110 POP_TOP
# 
#  14         112 PUSH_NULL
#             114 LOAD_BUILD_CLASS
#             116 LOAD_CONST               7 (<code object TestPowerFlowSkillIntegration at 0x73cd93b06880, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 14>)
#             118 MAKE_FUNCTION            0
#             120 LOAD_CONST               8 ('TestPowerFlowSkillIntegration')
#             122 CALL                     2
#             130 STORE_NAME              22 (TestPowerFlowSkillIntegration)
# 
#  40         132 PUSH_NULL
#             134 LOAD_BUILD_CLASS
#             136 LOAD_CONST               9 (<code object TestEMTSkillIntegration at 0x73cd93b066a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 40>)
#             138 MAKE_FUNCTION            0
#             140 LOAD_CONST              10 ('TestEMTSkillIntegration')
#             142 CALL                     2
#             150 STORE_NAME              23 (TestEMTSkillIntegration)
# 
#  68         152 PUSH_NULL
#             154 LOAD_BUILD_CLASS
#             156 LOAD_CONST              11 (<code object TestShortCircuitSkillIntegration at 0x73cd93b06790, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 68>)
#             158 MAKE_FUNCTION            0
#             160 LOAD_CONST              12 ('TestShortCircuitSkillIntegration')
#             162 CALL                     2
#             170 STORE_NAME              24 (TestShortCircuitSkillIntegration)
# 
#  96         172 PUSH_NULL
#             174 LOAD_BUILD_CLASS
#             176 LOAD_CONST              13 (<code object TestSkillOutputCompliance at 0x73cd9495ba60, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 96>)
#             178 MAKE_FUNCTION            0
#             180 LOAD_CONST              14 ('TestSkillOutputCompliance')
#             182 CALL                     2
#             190 STORE_NAME              25 (TestSkillOutputCompliance)
# 
# 125         192 PUSH_NULL
#             194 LOAD_BUILD_CLASS
#             196 LOAD_CONST              15 (<code object TestValidatorWithAllSkills at 0x73cd93b065b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 125>)
#             198 MAKE_FUNCTION            0
#             200 LOAD_CONST              16 ('TestValidatorWithAllSkills')
#             202 CALL                     2
#             210 STORE_NAME              26 (TestValidatorWithAllSkills)
# 
# 156         212 PUSH_NULL
#             214 LOAD_BUILD_CLASS
#             216 LOAD_CONST              17 (<code object TestSkillResultToDict at 0x73cd93b06970, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 156>)
#             218 MAKE_FUNCTION            0
#             220 LOAD_CONST              18 ('TestSkillResultToDict')
#             222 CALL                     2
#             230 STORE_NAME              27 (TestSkillResultToDict)
#             232 RETURN_CONST             2 (None)
# 
# Disassembly of <code object TestPowerFlowSkillIntegration at 0x73cd93b06880, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 14>:
#  14           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestPowerFlowSkillIntegration')
#               8 STORE_NAME               2 (__qualname__)
# 
#  15          10 LOAD_CONST               1 ('Integration tests for PowerFlowSkill.')
#              12 STORE_NAME               3 (__doc__)
# 
#  17          14 LOAD_CONST               2 (<code object test_run_returns_skill_result at 0x3aefe140, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 17>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_run_returns_skill_result)
# 
#  21          20 LOAD_CONST               3 (<code object test_validate_missing_model at 0x3afac750, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 21>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_validate_missing_model)
# 
#  27          26 LOAD_CONST               4 (<code object test_validate_valid_config at 0x3af3fb70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 27>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_validate_valid_config)
# 
#  33          32 LOAD_CONST               5 (<code object test_validate_invalid_tolerance at 0x3afad0d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 33>)
#              34 MAKE_FUNCTION            0
#              36 STORE_NAME               7 (test_validate_invalid_tolerance)
#              38 RETURN_CONST             6 (None)
# 
# Disassembly of <code object test_run_returns_skill_result at 0x3aefe140, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 17>:
#  17           0 RESUME                   0
# 
#  18           2 LOAD_GLOBAL              1 (NULL + PowerFlowSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  19          22 LOAD_CONST               1 ('run')
#              24 STORE_FAST               2 (@py_assert2)
#              26 LOAD_GLOBAL              3 (NULL + hasattr)
#              36 LOAD_FAST                1 (skill)
#              38 LOAD_FAST                2 (@py_assert2)
#              40 CALL                     2
#              48 STORE_FAST               3 (@py_assert4)
#              50 LOAD_FAST                3 (@py_assert4)
#              52 POP_JUMP_IF_TRUE       214 (to 482)
#              54 LOAD_CONST               2 ('assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}')
#              56 LOAD_CONST               3 ('hasattr')
#              58 LOAD_GLOBAL              5 (NULL + @py_builtins)
#              68 LOAD_ATTR                6 (locals)
#              88 CALL                     0
#              96 CONTAINS_OP              0
#              98 POP_JUMP_IF_TRUE        25 (to 150)
#             100 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             110 LOAD_ATTR               10 (_should_repr_global_name)
#             130 LOAD_GLOBAL              2 (hasattr)
#             140 CALL                     1
#             148 POP_JUMP_IF_FALSE       25 (to 200)
#         >>  150 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             160 LOAD_ATTR               12 (_saferepr)
#             180 LOAD_GLOBAL              2 (hasattr)
#             190 CALL                     1
#             198 JUMP_FORWARD             1 (to 202)
#         >>  200 LOAD_CONST               3 ('hasattr')
#         >>  202 LOAD_CONST               4 ('skill')
#             204 LOAD_GLOBAL              5 (NULL + @py_builtins)
#             214 LOAD_ATTR                6 (locals)
#             234 CALL                     0
#             242 CONTAINS_OP              0
#             244 POP_JUMP_IF_TRUE        21 (to 288)
#             246 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             256 LOAD_ATTR               10 (_should_repr_global_name)
#             276 LOAD_FAST                1 (skill)
#             278 CALL                     1
#             286 POP_JUMP_IF_FALSE       21 (to 330)
#         >>  288 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             298 LOAD_ATTR               12 (_saferepr)
#             318 LOAD_FAST                1 (skill)
#             320 CALL                     1
#             328 JUMP_FORWARD             1 (to 332)
#         >>  330 LOAD_CONST               4 ('skill')
#         >>  332 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             342 LOAD_ATTR               12 (_saferepr)
#             362 LOAD_FAST                2 (@py_assert2)
#             364 CALL                     1
#             372 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             382 LOAD_ATTR               12 (_saferepr)
#             402 LOAD_FAST                3 (@py_assert4)
#             404 CALL                     1
#             412 LOAD_CONST               5 (('py0', 'py1', 'py3', 'py5'))
#             414 BUILD_CONST_KEY_MAP      4
#             416 BINARY_OP                6 (%)
#             420 STORE_FAST               4 (@py_format6)
#             422 LOAD_GLOBAL             15 (NULL + AssertionError)
#             432 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             442 LOAD_ATTR               16 (_format_explanation)
#             462 LOAD_FAST                4 (@py_format6)
#             464 CALL                     1
#             472 CALL                     1
#             480 RAISE_VARARGS            1
#         >>  482 LOAD_CONST               0 (None)
#             484 COPY                     1
#             486 STORE_FAST               2 (@py_assert2)
#             488 STORE_FAST               3 (@py_assert4)
#             490 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_missing_model at 0x3afac750, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 21>:
#  21           0 RESUME                   0
# 
#  22           2 LOAD_GLOBAL              1 (NULL + PowerFlowSkill)
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
#  25         392 LOAD_GLOBAL             21 (NULL + len)
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
#             936 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_valid_config at 0x3af3fb70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 27>:
#  27           0 RESUME                   0
# 
#  28           2 LOAD_GLOBAL              1 (NULL + PowerFlowSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  29          22 LOAD_CONST               1 ('rid')
#              24 LOAD_CONST               2 ('test/123')
#              26 BUILD_MAP                1
#              28 LOAD_CONST               3 ('tolerance')
#              30 LOAD_CONST               4 (1e-06)
#              32 BUILD_MAP                1
#              34 LOAD_CONST               5 (('model', 'algorithm'))
#              36 BUILD_CONST_KEY_MAP      2
#              38 STORE_FAST               2 (config)
# 
#  30          40 LOAD_FAST                1 (skill)
#              42 LOAD_ATTR                3 (NULL|self + validate)
#              62 LOAD_FAST                2 (config)
#              64 CALL                     1
#              72 UNPACK_SEQUENCE          2
#              76 STORE_FAST               3 (valid)
#              78 STORE_FAST               4 (errors)
# 
#  31          80 LOAD_CONST               6 (True)
#              82 STORE_FAST               5 (@py_assert2)
#              84 LOAD_FAST                3 (valid)
#              86 LOAD_FAST                5 (@py_assert2)
#              88 IS_OP                    0
#              90 STORE_FAST               6 (@py_assert1)
#              92 LOAD_FAST                6 (@py_assert1)
#              94 POP_JUMP_IF_TRUE       153 (to 402)
#              96 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             106 LOAD_ATTR                6 (_call_reprcompare)
#             126 LOAD_CONST               7 (('is',))
#             128 LOAD_FAST                6 (@py_assert1)
#             130 BUILD_TUPLE              1
#             132 LOAD_CONST               8 (('%(py0)s is %(py3)s',))
#             134 LOAD_FAST                3 (valid)
#             136 LOAD_FAST                5 (@py_assert2)
#             138 BUILD_TUPLE              2
#             140 CALL                     4
#             148 LOAD_CONST               9 ('valid')
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
#         >>  276 LOAD_CONST               9 ('valid')
#         >>  278 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             288 LOAD_ATTR               14 (_saferepr)
#             308 LOAD_FAST                5 (@py_assert2)
#             310 CALL                     1
#             318 LOAD_CONST              10 (('py0', 'py3'))
#             320 BUILD_CONST_KEY_MAP      2
#             322 BINARY_OP                6 (%)
#             326 STORE_FAST               7 (@py_format4)
#             328 LOAD_CONST              11 ('assert %(py5)s')
#             330 LOAD_CONST              12 ('py5')
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
# Disassembly of <code object test_validate_invalid_tolerance at 0x3afad0d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 33>:
#  33           0 RESUME                   0
# 
#  34           2 LOAD_GLOBAL              1 (NULL + PowerFlowSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  35          22 LOAD_CONST               1 ('rid')
#              24 LOAD_CONST               2 ('test/123')
#              26 BUILD_MAP                1
#              28 LOAD_CONST               3 ('tolerance')
#              30 LOAD_CONST               4 (-1)
#              32 BUILD_MAP                1
#              34 LOAD_CONST               5 (('model', 'algorithm'))
#              36 BUILD_CONST_KEY_MAP      2
#              38 STORE_FAST               2 (config)
# 
#  36          40 LOAD_FAST                1 (skill)
#              42 LOAD_ATTR                3 (NULL|self + validate)
#              62 LOAD_FAST                2 (config)
#              64 CALL                     1
#              72 UNPACK_SEQUENCE          2
#              76 STORE_FAST               3 (valid)
#              78 STORE_FAST               4 (errors)
# 
#  37          80 LOAD_CONST               6 (False)
#              82 STORE_FAST               5 (@py_assert2)
#              84 LOAD_FAST                3 (valid)
#              86 LOAD_FAST                5 (@py_assert2)
#              88 IS_OP                    0
#              90 STORE_FAST               6 (@py_assert1)
#              92 LOAD_FAST                6 (@py_assert1)
#              94 POP_JUMP_IF_TRUE       153 (to 402)
#              96 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             106 LOAD_ATTR                6 (_call_reprcompare)
#             126 LOAD_CONST               7 (('is',))
#             128 LOAD_FAST                6 (@py_assert1)
#             130 BUILD_TUPLE              1
#             132 LOAD_CONST               8 (('%(py0)s is %(py3)s',))
#             134 LOAD_FAST                3 (valid)
#             136 LOAD_FAST                5 (@py_assert2)
#             138 BUILD_TUPLE              2
#             140 CALL                     4
#             148 LOAD_CONST               9 ('valid')
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
#         >>  276 LOAD_CONST               9 ('valid')
#         >>  278 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             288 LOAD_ATTR               14 (_saferepr)
#             308 LOAD_FAST                5 (@py_assert2)
#             310 CALL                     1
#             318 LOAD_CONST              10 (('py0', 'py3'))
#             320 BUILD_CONST_KEY_MAP      2
#             322 BINARY_OP                6 (%)
#             326 STORE_FAST               7 (@py_format4)
#             328 LOAD_CONST              11 ('assert %(py5)s')
#             330 LOAD_CONST              12 ('py5')
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
# Disassembly of <code object TestEMTSkillIntegration at 0x73cd93b066a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 40>:
#  40           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestEMTSkillIntegration')
#               8 STORE_NAME               2 (__qualname__)
# 
#  41          10 LOAD_CONST               1 ('Integration tests for EMTSimulationSkill.')
#              12 STORE_NAME               3 (__doc__)
# 
#  43          14 LOAD_CONST               2 (<code object test_run_returns_skill_result at 0x3aefd020, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 43>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_run_returns_skill_result)
# 
#  47          20 LOAD_CONST               3 (<code object test_validate_missing_model at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 47>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_validate_missing_model)
# 
#  52          26 LOAD_CONST               4 (<code object test_validate_valid_config at 0x3af0c6d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 52>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_validate_valid_config)
# 
#  61          32 LOAD_CONST               5 (<code object test_validate_invalid_time_step at 0x3af94a10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 61>)
#              34 MAKE_FUNCTION            0
#              36 STORE_NAME               7 (test_validate_invalid_time_step)
#              38 RETURN_CONST             6 (None)
# 
# Disassembly of <code object test_run_returns_skill_result at 0x3aefd020, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 43>:
#  43           0 RESUME                   0
# 
#  44           2 LOAD_GLOBAL              1 (NULL + EMTSimulationSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  45          22 LOAD_CONST               1 ('run')
#              24 STORE_FAST               2 (@py_assert2)
#              26 LOAD_GLOBAL              3 (NULL + hasattr)
#              36 LOAD_FAST                1 (skill)
#              38 LOAD_FAST                2 (@py_assert2)
#              40 CALL                     2
#              48 STORE_FAST               3 (@py_assert4)
#              50 LOAD_FAST                3 (@py_assert4)
#              52 POP_JUMP_IF_TRUE       214 (to 482)
#              54 LOAD_CONST               2 ('assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}')
#              56 LOAD_CONST               3 ('hasattr')
#              58 LOAD_GLOBAL              5 (NULL + @py_builtins)
#              68 LOAD_ATTR                6 (locals)
#              88 CALL                     0
#              96 CONTAINS_OP              0
#              98 POP_JUMP_IF_TRUE        25 (to 150)
#             100 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             110 LOAD_ATTR               10 (_should_repr_global_name)
#             130 LOAD_GLOBAL              2 (hasattr)
#             140 CALL                     1
#             148 POP_JUMP_IF_FALSE       25 (to 200)
#         >>  150 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             160 LOAD_ATTR               12 (_saferepr)
#             180 LOAD_GLOBAL              2 (hasattr)
#             190 CALL                     1
#             198 JUMP_FORWARD             1 (to 202)
#         >>  200 LOAD_CONST               3 ('hasattr')
#         >>  202 LOAD_CONST               4 ('skill')
#             204 LOAD_GLOBAL              5 (NULL + @py_builtins)
#             214 LOAD_ATTR                6 (locals)
#             234 CALL                     0
#             242 CONTAINS_OP              0
#             244 POP_JUMP_IF_TRUE        21 (to 288)
#             246 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             256 LOAD_ATTR               10 (_should_repr_global_name)
#             276 LOAD_FAST                1 (skill)
#             278 CALL                     1
#             286 POP_JUMP_IF_FALSE       21 (to 330)
#         >>  288 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             298 LOAD_ATTR               12 (_saferepr)
#             318 LOAD_FAST                1 (skill)
#             320 CALL                     1
#             328 JUMP_FORWARD             1 (to 332)
#         >>  330 LOAD_CONST               4 ('skill')
#         >>  332 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             342 LOAD_ATTR               12 (_saferepr)
#             362 LOAD_FAST                2 (@py_assert2)
#             364 CALL                     1
#             372 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             382 LOAD_ATTR               12 (_saferepr)
#             402 LOAD_FAST                3 (@py_assert4)
#             404 CALL                     1
#             412 LOAD_CONST               5 (('py0', 'py1', 'py3', 'py5'))
#             414 BUILD_CONST_KEY_MAP      4
#             416 BINARY_OP                6 (%)
#             420 STORE_FAST               4 (@py_format6)
#             422 LOAD_GLOBAL             15 (NULL + AssertionError)
#             432 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             442 LOAD_ATTR               16 (_format_explanation)
#             462 LOAD_FAST                4 (@py_format6)
#             464 CALL                     1
#             472 CALL                     1
#             480 RAISE_VARARGS            1
#         >>  482 LOAD_CONST               0 (None)
#             484 COPY                     1
#             486 STORE_FAST               2 (@py_assert2)
#             488 STORE_FAST               3 (@py_assert4)
#             490 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_missing_model at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 47>:
#  47           0 RESUME                   0
# 
#  48           2 LOAD_GLOBAL              1 (NULL + EMTSimulationSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  49          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + validate)
#              44 BUILD_MAP                0
#              46 CALL                     1
#              54 UNPACK_SEQUENCE          2
#              58 STORE_FAST               2 (valid)
#              60 STORE_FAST               3 (errors)
# 
#  50          62 LOAD_CONST               1 (False)
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
# Disassembly of <code object test_validate_valid_config at 0x3af0c6d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 52>:
#  52           0 RESUME                   0
# 
#  53           2 LOAD_GLOBAL              1 (NULL + EMTSimulationSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  55          22 LOAD_CONST               1 ('rid')
#              24 LOAD_CONST               2 ('test/123')
#              26 BUILD_MAP                1
# 
#  56          28 LOAD_CONST               3 (0.0001)
#              30 LOAD_CONST               4 (1.0)
#              32 LOAD_CONST               5 (('time_step', 'end_time'))
#              34 BUILD_CONST_KEY_MAP      2
# 
#  54          36 LOAD_CONST               6 (('model', 'simulation'))
#              38 BUILD_CONST_KEY_MAP      2
#              40 STORE_FAST               2 (config)
# 
#  58          42 LOAD_FAST                1 (skill)
#              44 LOAD_ATTR                3 (NULL|self + validate)
#              64 LOAD_FAST                2 (config)
#              66 CALL                     1
#              74 UNPACK_SEQUENCE          2
#              78 STORE_FAST               3 (valid)
#              80 STORE_FAST               4 (errors)
# 
#  59          82 LOAD_CONST               7 (True)
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
# Disassembly of <code object test_validate_invalid_time_step at 0x3af94a10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 61>:
#  61           0 RESUME                   0
# 
#  62           2 LOAD_GLOBAL              1 (NULL + EMTSimulationSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  63          22 LOAD_CONST               1 ('rid')
#              24 LOAD_CONST               2 ('test/123')
#              26 BUILD_MAP                1
#              28 LOAD_CONST               3 ('time_step')
#              30 LOAD_CONST               4 (-0.001)
#              32 BUILD_MAP                1
#              34 LOAD_CONST               5 (('model', 'simulation'))
#              36 BUILD_CONST_KEY_MAP      2
#              38 STORE_FAST               2 (config)
# 
#  64          40 LOAD_FAST                1 (skill)
#              42 LOAD_ATTR                3 (NULL|self + validate)
#              62 LOAD_FAST                2 (config)
#              64 CALL                     1
#              72 UNPACK_SEQUENCE          2
#              76 STORE_FAST               3 (valid)
#              78 STORE_FAST               4 (errors)
# 
#  65          80 LOAD_CONST               6 (False)
#              82 STORE_FAST               5 (@py_assert2)
#              84 LOAD_FAST                3 (valid)
#              86 LOAD_FAST                5 (@py_assert2)
#              88 IS_OP                    0
#              90 STORE_FAST               6 (@py_assert1)
#              92 LOAD_FAST                6 (@py_assert1)
#              94 POP_JUMP_IF_TRUE       153 (to 402)
#              96 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             106 LOAD_ATTR                6 (_call_reprcompare)
#             126 LOAD_CONST               7 (('is',))
#             128 LOAD_FAST                6 (@py_assert1)
#             130 BUILD_TUPLE              1
#             132 LOAD_CONST               8 (('%(py0)s is %(py3)s',))
#             134 LOAD_FAST                3 (valid)
#             136 LOAD_FAST                5 (@py_assert2)
#             138 BUILD_TUPLE              2
#             140 CALL                     4
#             148 LOAD_CONST               9 ('valid')
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
#         >>  276 LOAD_CONST               9 ('valid')
#         >>  278 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             288 LOAD_ATTR               14 (_saferepr)
#             308 LOAD_FAST                5 (@py_assert2)
#             310 CALL                     1
#             318 LOAD_CONST              10 (('py0', 'py3'))
#             320 BUILD_CONST_KEY_MAP      2
#             322 BINARY_OP                6 (%)
#             326 STORE_FAST               7 (@py_format4)
#             328 LOAD_CONST              11 ('assert %(py5)s')
#             330 LOAD_CONST              12 ('py5')
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
# Disassembly of <code object TestShortCircuitSkillIntegration at 0x73cd93b06790, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 68>:
#  68           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestShortCircuitSkillIntegration')
#               8 STORE_NAME               2 (__qualname__)
# 
#  69          10 LOAD_CONST               1 ('Integration tests for ShortCircuitSkill.')
#              12 STORE_NAME               3 (__doc__)
# 
#  71          14 LOAD_CONST               2 (<code object test_run_returns_skill_result at 0x3af1c4d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 71>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_run_returns_skill_result)
# 
#  75          20 LOAD_CONST               3 (<code object test_validate_missing_model at 0x3af90d20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 75>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_validate_missing_model)
# 
#  80          26 LOAD_CONST               4 (<code object test_validate_valid_config at 0x3aefb4d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 80>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_validate_valid_config)
# 
#  89          32 LOAD_CONST               5 (<code object test_validate_invalid_impedance at 0x3afa7ad0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 89>)
#              34 MAKE_FUNCTION            0
#              36 STORE_NAME               7 (test_validate_invalid_impedance)
#              38 RETURN_CONST             6 (None)
# 
# Disassembly of <code object test_run_returns_skill_result at 0x3af1c4d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 71>:
#  71           0 RESUME                   0
# 
#  72           2 LOAD_GLOBAL              1 (NULL + ShortCircuitSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  73          22 LOAD_CONST               1 ('run')
#              24 STORE_FAST               2 (@py_assert2)
#              26 LOAD_GLOBAL              3 (NULL + hasattr)
#              36 LOAD_FAST                1 (skill)
#              38 LOAD_FAST                2 (@py_assert2)
#              40 CALL                     2
#              48 STORE_FAST               3 (@py_assert4)
#              50 LOAD_FAST                3 (@py_assert4)
#              52 POP_JUMP_IF_TRUE       214 (to 482)
#              54 LOAD_CONST               2 ('assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}')
#              56 LOAD_CONST               3 ('hasattr')
#              58 LOAD_GLOBAL              5 (NULL + @py_builtins)
#              68 LOAD_ATTR                6 (locals)
#              88 CALL                     0
#              96 CONTAINS_OP              0
#              98 POP_JUMP_IF_TRUE        25 (to 150)
#             100 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             110 LOAD_ATTR               10 (_should_repr_global_name)
#             130 LOAD_GLOBAL              2 (hasattr)
#             140 CALL                     1
#             148 POP_JUMP_IF_FALSE       25 (to 200)
#         >>  150 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             160 LOAD_ATTR               12 (_saferepr)
#             180 LOAD_GLOBAL              2 (hasattr)
#             190 CALL                     1
#             198 JUMP_FORWARD             1 (to 202)
#         >>  200 LOAD_CONST               3 ('hasattr')
#         >>  202 LOAD_CONST               4 ('skill')
#             204 LOAD_GLOBAL              5 (NULL + @py_builtins)
#             214 LOAD_ATTR                6 (locals)
#             234 CALL                     0
#             242 CONTAINS_OP              0
#             244 POP_JUMP_IF_TRUE        21 (to 288)
#             246 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             256 LOAD_ATTR               10 (_should_repr_global_name)
#             276 LOAD_FAST                1 (skill)
#             278 CALL                     1
#             286 POP_JUMP_IF_FALSE       21 (to 330)
#         >>  288 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             298 LOAD_ATTR               12 (_saferepr)
#             318 LOAD_FAST                1 (skill)
#             320 CALL                     1
#             328 JUMP_FORWARD             1 (to 332)
#         >>  330 LOAD_CONST               4 ('skill')
#         >>  332 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             342 LOAD_ATTR               12 (_saferepr)
#             362 LOAD_FAST                2 (@py_assert2)
#             364 CALL                     1
#             372 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             382 LOAD_ATTR               12 (_saferepr)
#             402 LOAD_FAST                3 (@py_assert4)
#             404 CALL                     1
#             412 LOAD_CONST               5 (('py0', 'py1', 'py3', 'py5'))
#             414 BUILD_CONST_KEY_MAP      4
#             416 BINARY_OP                6 (%)
#             420 STORE_FAST               4 (@py_format6)
#             422 LOAD_GLOBAL             15 (NULL + AssertionError)
#             432 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             442 LOAD_ATTR               16 (_format_explanation)
#             462 LOAD_FAST                4 (@py_format6)
#             464 CALL                     1
#             472 CALL                     1
#             480 RAISE_VARARGS            1
#         >>  482 LOAD_CONST               0 (None)
#             484 COPY                     1
#             486 STORE_FAST               2 (@py_assert2)
#             488 STORE_FAST               3 (@py_assert4)
#             490 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_missing_model at 0x3af90d20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 75>:
#  75           0 RESUME                   0
# 
#  76           2 LOAD_GLOBAL              1 (NULL + ShortCircuitSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  77          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + validate)
#              44 BUILD_MAP                0
#              46 CALL                     1
#              54 UNPACK_SEQUENCE          2
#              58 STORE_FAST               2 (valid)
#              60 STORE_FAST               3 (errors)
# 
#  78          62 LOAD_CONST               1 (False)
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
# Disassembly of <code object test_validate_valid_config at 0x3aefb4d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 80>:
#  80           0 RESUME                   0
# 
#  81           2 LOAD_GLOBAL              1 (NULL + ShortCircuitSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  83          22 LOAD_CONST               1 ('rid')
#              24 LOAD_CONST               2 ('test/123')
#              26 BUILD_MAP                1
# 
#  84          28 LOAD_CONST               3 ('3phase')
#              30 LOAD_CONST               4 (0.01)
#              32 LOAD_CONST               5 (('type', 'impedance'))
#              34 BUILD_CONST_KEY_MAP      2
# 
#  82          36 LOAD_CONST               6 (('model', 'fault'))
#              38 BUILD_CONST_KEY_MAP      2
#              40 STORE_FAST               2 (config)
# 
#  86          42 LOAD_FAST                1 (skill)
#              44 LOAD_ATTR                3 (NULL|self + validate)
#              64 LOAD_FAST                2 (config)
#              66 CALL                     1
#              74 UNPACK_SEQUENCE          2
#              78 STORE_FAST               3 (valid)
#              80 STORE_FAST               4 (errors)
# 
#  87          82 LOAD_CONST               7 (True)
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
# Disassembly of <code object test_validate_invalid_impedance at 0x3afa7ad0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 89>:
#  89           0 RESUME                   0
# 
#  90           2 LOAD_GLOBAL              1 (NULL + ShortCircuitSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  91          22 LOAD_CONST               1 ('rid')
#              24 LOAD_CONST               2 ('test/123')
#              26 BUILD_MAP                1
#              28 LOAD_CONST               3 ('impedance')
#              30 LOAD_CONST               4 (-1)
#              32 BUILD_MAP                1
#              34 LOAD_CONST               5 (('model', 'fault'))
#              36 BUILD_CONST_KEY_MAP      2
#              38 STORE_FAST               2 (config)
# 
#  92          40 LOAD_FAST                1 (skill)
#              42 LOAD_ATTR                3 (NULL|self + validate)
#              62 LOAD_FAST                2 (config)
#              64 CALL                     1
#              72 UNPACK_SEQUENCE          2
#              76 STORE_FAST               3 (valid)
#              78 STORE_FAST               4 (errors)
# 
#  93          80 LOAD_CONST               6 (False)
#              82 STORE_FAST               5 (@py_assert2)
#              84 LOAD_FAST                3 (valid)
#              86 LOAD_FAST                5 (@py_assert2)
#              88 IS_OP                    0
#              90 STORE_FAST               6 (@py_assert1)
#              92 LOAD_FAST                6 (@py_assert1)
#              94 POP_JUMP_IF_TRUE       153 (to 402)
#              96 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             106 LOAD_ATTR                6 (_call_reprcompare)
#             126 LOAD_CONST               7 (('is',))
#             128 LOAD_FAST                6 (@py_assert1)
#             130 BUILD_TUPLE              1
#             132 LOAD_CONST               8 (('%(py0)s is %(py3)s',))
#             134 LOAD_FAST                3 (valid)
#             136 LOAD_FAST                5 (@py_assert2)
#             138 BUILD_TUPLE              2
#             140 CALL                     4
#             148 LOAD_CONST               9 ('valid')
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
#         >>  276 LOAD_CONST               9 ('valid')
#         >>  278 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             288 LOAD_ATTR               14 (_saferepr)
#             308 LOAD_FAST                5 (@py_assert2)
#             310 CALL                     1
#             318 LOAD_CONST              10 (('py0', 'py3'))
#             320 BUILD_CONST_KEY_MAP      2
#             322 BINARY_OP                6 (%)
#             326 STORE_FAST               7 (@py_format4)
#             328 LOAD_CONST              11 ('assert %(py5)s')
#             330 LOAD_CONST              12 ('py5')
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
# Disassembly of <code object TestSkillOutputCompliance at 0x73cd9495ba60, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 96>:
#  96           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestSkillOutputCompliance')
#               8 STORE_NAME               2 (__qualname__)
# 
#  97          10 LOAD_CONST               1 ('Verify all skills follow output standard.')
#              12 STORE_NAME               3 (__doc__)
# 
#  99          14 PUSH_NULL
#              16 LOAD_NAME                4 (patch)
#              18 LOAD_CONST               2 ('cloudpss_skills_v2.skills.power_flow.APIFactory')
#              20 CALL                     1
# 
# 100          28 LOAD_CONST               3 (<code object test_power_flow_failure_includes_error at 0x3afa6250, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 99>)
#              30 MAKE_FUNCTION            0
# 
#  99          32 CALL                     0
# 
# 100          40 STORE_NAME               5 (test_power_flow_failure_includes_error)
# 
# 108          42 PUSH_NULL
#              44 LOAD_NAME                4 (patch)
#              46 LOAD_CONST               4 ('cloudpss_skills_v2.skills.emt_simulation.APIFactory')
#              48 CALL                     1
# 
# 109          56 LOAD_CONST               5 (<code object test_emt_failure_includes_error at 0x3af9d7e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 108>)
#              58 MAKE_FUNCTION            0
# 
# 108          60 CALL                     0
# 
# 109          68 STORE_NAME               6 (test_emt_failure_includes_error)
# 
# 116          70 PUSH_NULL
#              72 LOAD_NAME                4 (patch)
#              74 LOAD_CONST               6 ('cloudpss_skills_v2.skills.short_circuit.APIFactory')
#              76 CALL                     1
# 
# 117          84 LOAD_CONST               7 (<code object test_short_circuit_failure_includes_error at 0x3afa8540, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 116>)
#              86 MAKE_FUNCTION            0
# 
# 116          88 CALL                     0
# 
# 117          96 STORE_NAME               7 (test_short_circuit_failure_includes_error)
#              98 RETURN_CONST             8 (None)
# 
# Disassembly of <code object test_power_flow_failure_includes_error at 0x3afa6250, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 99>:
#  99           0 RESUME                   0
# 
# 101           2 LOAD_GLOBAL              1 (NULL + PowerFlowSkill)
#              12 CALL                     0
#              20 STORE_FAST               2 (skill)
# 
# 102          22 LOAD_CONST               1 ('model')
#              24 BUILD_MAP                0
#              26 BUILD_MAP                1
#              28 STORE_FAST               3 (config)
# 
# 103          30 LOAD_FAST                2 (skill)
#              32 LOAD_ATTR                3 (NULL|self + run)
#              52 LOAD_FAST                3 (config)
#              54 CALL                     1
#              62 STORE_FAST               4 (result)
# 
# 104          64 LOAD_FAST                4 (result)
#              66 LOAD_ATTR                4 (status)
#              86 STORE_FAST               5 (@py_assert1)
#              88 LOAD_GLOBAL              6 (SkillStatus)
#              98 LOAD_ATTR                8 (FAILED)
#             118 STORE_FAST               6 (@py_assert5)
#             120 LOAD_FAST                5 (@py_assert1)
#             122 LOAD_FAST                6 (@py_assert5)
#             124 COMPARE_OP              40 (==)
#             128 STORE_FAST               7 (@py_assert3)
#             130 LOAD_FAST                7 (@py_assert3)
#             132 POP_JUMP_IF_TRUE       246 (to 626)
#             134 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             144 LOAD_ATTR               12 (_call_reprcompare)
#             164 LOAD_CONST               2 (('==',))
#             166 LOAD_FAST                7 (@py_assert3)
#             168 BUILD_TUPLE              1
#             170 LOAD_CONST               3 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.FAILED\n}',))
#             172 LOAD_FAST                5 (@py_assert1)
#             174 LOAD_FAST                6 (@py_assert5)
#             176 BUILD_TUPLE              2
#             178 CALL                     4
#             186 LOAD_CONST               4 ('result')
#             188 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             198 LOAD_ATTR               16 (locals)
#             218 CALL                     0
#             226 CONTAINS_OP              0
#             228 POP_JUMP_IF_TRUE        21 (to 272)
#             230 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             240 LOAD_ATTR               18 (_should_repr_global_name)
#             260 LOAD_FAST                4 (result)
#             262 CALL                     1
#             270 POP_JUMP_IF_FALSE       21 (to 314)
#         >>  272 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             282 LOAD_ATTR               20 (_saferepr)
#             302 LOAD_FAST                4 (result)
#             304 CALL                     1
#             312 JUMP_FORWARD             1 (to 316)
#         >>  314 LOAD_CONST               4 ('result')
#         >>  316 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             326 LOAD_ATTR               20 (_saferepr)
#             346 LOAD_FAST                5 (@py_assert1)
#             348 CALL                     1
#             356 LOAD_CONST               5 ('SkillStatus')
#             358 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             368 LOAD_ATTR               16 (locals)
#             388 CALL                     0
#             396 CONTAINS_OP              0
#             398 POP_JUMP_IF_TRUE        25 (to 450)
#             400 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             410 LOAD_ATTR               18 (_should_repr_global_name)
#             430 LOAD_GLOBAL              6 (SkillStatus)
#             440 CALL                     1
#             448 POP_JUMP_IF_FALSE       25 (to 500)
#         >>  450 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             460 LOAD_ATTR               20 (_saferepr)
#             480 LOAD_GLOBAL              6 (SkillStatus)
#             490 CALL                     1
#             498 JUMP_FORWARD             1 (to 502)
#         >>  500 LOAD_CONST               5 ('SkillStatus')
#         >>  502 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             512 LOAD_ATTR               20 (_saferepr)
#             532 LOAD_FAST                6 (@py_assert5)
#             534 CALL                     1
#             542 LOAD_CONST               6 (('py0', 'py2', 'py4', 'py6'))
#             544 BUILD_CONST_KEY_MAP      4
#             546 BINARY_OP                6 (%)
#             550 STORE_FAST               8 (@py_format7)
#             552 LOAD_CONST               7 ('assert %(py8)s')
#             554 LOAD_CONST               8 ('py8')
#             556 LOAD_FAST                8 (@py_format7)
#             558 BUILD_MAP                1
#             560 BINARY_OP                6 (%)
#             564 STORE_FAST               9 (@py_format9)
#             566 LOAD_GLOBAL             23 (NULL + AssertionError)
#             576 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             586 LOAD_ATTR               24 (_format_explanation)
#             606 LOAD_FAST                9 (@py_format9)
#             608 CALL                     1
#             616 CALL                     1
#             624 RAISE_VARARGS            1
#         >>  626 LOAD_CONST               0 (None)
#             628 COPY                     1
#             630 STORE_FAST               5 (@py_assert1)
#             632 COPY                     1
#             634 STORE_FAST               7 (@py_assert3)
#             636 STORE_FAST               6 (@py_assert5)
# 
# 105         638 LOAD_FAST                4 (result)
#             640 LOAD_ATTR               26 (error)
#             660 STORE_FAST               5 (@py_assert1)
#             662 LOAD_CONST               0 (None)
#             664 STORE_FAST              10 (@py_assert4)
#             666 LOAD_FAST                5 (@py_assert1)
#             668 LOAD_FAST               10 (@py_assert4)
#             670 IS_OP                    1
#             672 STORE_FAST               7 (@py_assert3)
#             674 LOAD_FAST                7 (@py_assert3)
#             676 POP_JUMP_IF_TRUE       173 (to 1024)
#             678 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             688 LOAD_ATTR               12 (_call_reprcompare)
#             708 LOAD_CONST               9 (('is not',))
#             710 LOAD_FAST                7 (@py_assert3)
#             712 BUILD_TUPLE              1
#             714 LOAD_CONST              10 (('%(py2)s\n{%(py2)s = %(py0)s.error\n} is not %(py5)s',))
#             716 LOAD_FAST                5 (@py_assert1)
#             718 LOAD_FAST               10 (@py_assert4)
#             720 BUILD_TUPLE              2
#             722 CALL                     4
#             730 LOAD_CONST               4 ('result')
#             732 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             742 LOAD_ATTR               16 (locals)
#             762 CALL                     0
#             770 CONTAINS_OP              0
#             772 POP_JUMP_IF_TRUE        21 (to 816)
#             774 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             784 LOAD_ATTR               18 (_should_repr_global_name)
#             804 LOAD_FAST                4 (result)
#             806 CALL                     1
#             814 POP_JUMP_IF_FALSE       21 (to 858)
#         >>  816 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             826 LOAD_ATTR               20 (_saferepr)
#             846 LOAD_FAST                4 (result)
#             848 CALL                     1
#             856 JUMP_FORWARD             1 (to 860)
#         >>  858 LOAD_CONST               4 ('result')
#         >>  860 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             870 LOAD_ATTR               20 (_saferepr)
#             890 LOAD_FAST                5 (@py_assert1)
#             892 CALL                     1
#             900 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             910 LOAD_ATTR               20 (_saferepr)
#             930 LOAD_FAST               10 (@py_assert4)
#             932 CALL                     1
#             940 LOAD_CONST              11 (('py0', 'py2', 'py5'))
#             942 BUILD_CONST_KEY_MAP      3
#             944 BINARY_OP                6 (%)
#             948 STORE_FAST              11 (@py_format6)
#             950 LOAD_CONST              12 ('assert %(py7)s')
#             952 LOAD_CONST              13 ('py7')
#             954 LOAD_FAST               11 (@py_format6)
#             956 BUILD_MAP                1
#             958 BINARY_OP                6 (%)
#             962 STORE_FAST              12 (@py_format8)
#             964 LOAD_GLOBAL             23 (NULL + AssertionError)
#             974 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             984 LOAD_ATTR               24 (_format_explanation)
#            1004 LOAD_FAST               12 (@py_format8)
#            1006 CALL                     1
#            1014 CALL                     1
#            1022 RAISE_VARARGS            1
#         >> 1024 LOAD_CONST               0 (None)
#            1026 COPY                     1
#            1028 STORE_FAST               5 (@py_assert1)
#            1030 COPY                     1
#            1032 STORE_FAST               7 (@py_assert3)
#            1034 STORE_FAST              10 (@py_assert4)
# 
# 106        1036 LOAD_FAST                4 (result)
#            1038 LOAD_ATTR               28 (has_error)
#            1058 STORE_FAST               5 (@py_assert1)
#            1060 LOAD_CONST              14 (True)
#            1062 STORE_FAST              10 (@py_assert4)
#            1064 LOAD_FAST                5 (@py_assert1)
#            1066 LOAD_FAST               10 (@py_assert4)
#            1068 IS_OP                    0
#            1070 STORE_FAST               7 (@py_assert3)
#            1072 LOAD_FAST                7 (@py_assert3)
#            1074 POP_JUMP_IF_TRUE       173 (to 1422)
#            1076 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1086 LOAD_ATTR               12 (_call_reprcompare)
#            1106 LOAD_CONST              15 (('is',))
#            1108 LOAD_FAST                7 (@py_assert3)
#            1110 BUILD_TUPLE              1
#            1112 LOAD_CONST              16 (('%(py2)s\n{%(py2)s = %(py0)s.has_error\n} is %(py5)s',))
#            1114 LOAD_FAST                5 (@py_assert1)
#            1116 LOAD_FAST               10 (@py_assert4)
#            1118 BUILD_TUPLE              2
#            1120 CALL                     4
#            1128 LOAD_CONST               4 ('result')
#            1130 LOAD_GLOBAL             15 (NULL + @py_builtins)
#            1140 LOAD_ATTR               16 (locals)
#            1160 CALL                     0
#            1168 CONTAINS_OP              0
#            1170 POP_JUMP_IF_TRUE        21 (to 1214)
#            1172 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1182 LOAD_ATTR               18 (_should_repr_global_name)
#            1202 LOAD_FAST                4 (result)
#            1204 CALL                     1
#            1212 POP_JUMP_IF_FALSE       21 (to 1256)
#         >> 1214 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1224 LOAD_ATTR               20 (_saferepr)
#            1244 LOAD_FAST                4 (result)
#            1246 CALL                     1
#            1254 JUMP_FORWARD             1 (to 1258)
#         >> 1256 LOAD_CONST               4 ('result')
#         >> 1258 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1268 LOAD_ATTR               20 (_saferepr)
#            1288 LOAD_FAST                5 (@py_assert1)
#            1290 CALL                     1
#            1298 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1308 LOAD_ATTR               20 (_saferepr)
#            1328 LOAD_FAST               10 (@py_assert4)
#            1330 CALL                     1
#            1338 LOAD_CONST              11 (('py0', 'py2', 'py5'))
#            1340 BUILD_CONST_KEY_MAP      3
#            1342 BINARY_OP                6 (%)
#            1346 STORE_FAST              11 (@py_format6)
#            1348 LOAD_CONST              12 ('assert %(py7)s')
#            1350 LOAD_CONST              13 ('py7')
#            1352 LOAD_FAST               11 (@py_format6)
#            1354 BUILD_MAP                1
#            1356 BINARY_OP                6 (%)
#            1360 STORE_FAST              12 (@py_format8)
#            1362 LOAD_GLOBAL             23 (NULL + AssertionError)
#            1372 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#            1382 LOAD_ATTR               24 (_format_explanation)
#            1402 LOAD_FAST               12 (@py_format8)
#            1404 CALL                     1
#            1412 CALL                     1
#            1420 RAISE_VARARGS            1
#         >> 1422 LOAD_CONST               0 (None)
#            1424 COPY                     1
#            1426 STORE_FAST               5 (@py_assert1)
#            1428 COPY                     1
#            1430 STORE_FAST               7 (@py_assert3)
#            1432 STORE_FAST              10 (@py_assert4)
#            1434 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_emt_failure_includes_error at 0x3af9d7e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 108>:
# 108           0 RESUME                   0
# 
# 110           2 LOAD_GLOBAL              1 (NULL + EMTSimulationSkill)
#              12 CALL                     0
#              20 STORE_FAST               2 (skill)
# 
# 111          22 LOAD_CONST               1 ('model')
#              24 BUILD_MAP                0
#              26 BUILD_MAP                1
#              28 STORE_FAST               3 (config)
# 
# 112          30 LOAD_FAST                2 (skill)
#              32 LOAD_ATTR                3 (NULL|self + run)
#              52 LOAD_FAST                3 (config)
#              54 CALL                     1
#              62 STORE_FAST               4 (result)
# 
# 113          64 LOAD_FAST                4 (result)
#              66 LOAD_ATTR                4 (status)
#              86 STORE_FAST               5 (@py_assert1)
#              88 LOAD_GLOBAL              6 (SkillStatus)
#              98 LOAD_ATTR                8 (FAILED)
#             118 STORE_FAST               6 (@py_assert5)
#             120 LOAD_FAST                5 (@py_assert1)
#             122 LOAD_FAST                6 (@py_assert5)
#             124 COMPARE_OP              40 (==)
#             128 STORE_FAST               7 (@py_assert3)
#             130 LOAD_FAST                7 (@py_assert3)
#             132 POP_JUMP_IF_TRUE       246 (to 626)
#             134 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             144 LOAD_ATTR               12 (_call_reprcompare)
#             164 LOAD_CONST               2 (('==',))
#             166 LOAD_FAST                7 (@py_assert3)
#             168 BUILD_TUPLE              1
#             170 LOAD_CONST               3 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.FAILED\n}',))
#             172 LOAD_FAST                5 (@py_assert1)
#             174 LOAD_FAST                6 (@py_assert5)
#             176 BUILD_TUPLE              2
#             178 CALL                     4
#             186 LOAD_CONST               4 ('result')
#             188 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             198 LOAD_ATTR               16 (locals)
#             218 CALL                     0
#             226 CONTAINS_OP              0
#             228 POP_JUMP_IF_TRUE        21 (to 272)
#             230 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             240 LOAD_ATTR               18 (_should_repr_global_name)
#             260 LOAD_FAST                4 (result)
#             262 CALL                     1
#             270 POP_JUMP_IF_FALSE       21 (to 314)
#         >>  272 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             282 LOAD_ATTR               20 (_saferepr)
#             302 LOAD_FAST                4 (result)
#             304 CALL                     1
#             312 JUMP_FORWARD             1 (to 316)
#         >>  314 LOAD_CONST               4 ('result')
#         >>  316 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             326 LOAD_ATTR               20 (_saferepr)
#             346 LOAD_FAST                5 (@py_assert1)
#             348 CALL                     1
#             356 LOAD_CONST               5 ('SkillStatus')
#             358 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             368 LOAD_ATTR               16 (locals)
#             388 CALL                     0
#             396 CONTAINS_OP              0
#             398 POP_JUMP_IF_TRUE        25 (to 450)
#             400 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             410 LOAD_ATTR               18 (_should_repr_global_name)
#             430 LOAD_GLOBAL              6 (SkillStatus)
#             440 CALL                     1
#             448 POP_JUMP_IF_FALSE       25 (to 500)
#         >>  450 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             460 LOAD_ATTR               20 (_saferepr)
#             480 LOAD_GLOBAL              6 (SkillStatus)
#             490 CALL                     1
#             498 JUMP_FORWARD             1 (to 502)
#         >>  500 LOAD_CONST               5 ('SkillStatus')
#         >>  502 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             512 LOAD_ATTR               20 (_saferepr)
#             532 LOAD_FAST                6 (@py_assert5)
#             534 CALL                     1
#             542 LOAD_CONST               6 (('py0', 'py2', 'py4', 'py6'))
#             544 BUILD_CONST_KEY_MAP      4
#             546 BINARY_OP                6 (%)
#             550 STORE_FAST               8 (@py_format7)
#             552 LOAD_CONST               7 ('assert %(py8)s')
#             554 LOAD_CONST               8 ('py8')
#             556 LOAD_FAST                8 (@py_format7)
#             558 BUILD_MAP                1
#             560 BINARY_OP                6 (%)
#             564 STORE_FAST               9 (@py_format9)
#             566 LOAD_GLOBAL             23 (NULL + AssertionError)
#             576 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             586 LOAD_ATTR               24 (_format_explanation)
#             606 LOAD_FAST                9 (@py_format9)
#             608 CALL                     1
#             616 CALL                     1
#             624 RAISE_VARARGS            1
#         >>  626 LOAD_CONST               0 (None)
#             628 COPY                     1
#             630 STORE_FAST               5 (@py_assert1)
#             632 COPY                     1
#             634 STORE_FAST               7 (@py_assert3)
#             636 STORE_FAST               6 (@py_assert5)
# 
# 114         638 LOAD_FAST                4 (result)
#             640 LOAD_ATTR               26 (error)
#             660 STORE_FAST               5 (@py_assert1)
#             662 LOAD_CONST               0 (None)
#             664 STORE_FAST              10 (@py_assert4)
#             666 LOAD_FAST                5 (@py_assert1)
#             668 LOAD_FAST               10 (@py_assert4)
#             670 IS_OP                    1
#             672 STORE_FAST               7 (@py_assert3)
#             674 LOAD_FAST                7 (@py_assert3)
#             676 POP_JUMP_IF_TRUE       173 (to 1024)
#             678 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             688 LOAD_ATTR               12 (_call_reprcompare)
#             708 LOAD_CONST               9 (('is not',))
#             710 LOAD_FAST                7 (@py_assert3)
#             712 BUILD_TUPLE              1
#             714 LOAD_CONST              10 (('%(py2)s\n{%(py2)s = %(py0)s.error\n} is not %(py5)s',))
#             716 LOAD_FAST                5 (@py_assert1)
#             718 LOAD_FAST               10 (@py_assert4)
#             720 BUILD_TUPLE              2
#             722 CALL                     4
#             730 LOAD_CONST               4 ('result')
#             732 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             742 LOAD_ATTR               16 (locals)
#             762 CALL                     0
#             770 CONTAINS_OP              0
#             772 POP_JUMP_IF_TRUE        21 (to 816)
#             774 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             784 LOAD_ATTR               18 (_should_repr_global_name)
#             804 LOAD_FAST                4 (result)
#             806 CALL                     1
#             814 POP_JUMP_IF_FALSE       21 (to 858)
#         >>  816 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             826 LOAD_ATTR               20 (_saferepr)
#             846 LOAD_FAST                4 (result)
#             848 CALL                     1
#             856 JUMP_FORWARD             1 (to 860)
#         >>  858 LOAD_CONST               4 ('result')
#         >>  860 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             870 LOAD_ATTR               20 (_saferepr)
#             890 LOAD_FAST                5 (@py_assert1)
#             892 CALL                     1
#             900 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             910 LOAD_ATTR               20 (_saferepr)
#             930 LOAD_FAST               10 (@py_assert4)
#             932 CALL                     1
#             940 LOAD_CONST              11 (('py0', 'py2', 'py5'))
#             942 BUILD_CONST_KEY_MAP      3
#             944 BINARY_OP                6 (%)
#             948 STORE_FAST              11 (@py_format6)
#             950 LOAD_CONST              12 ('assert %(py7)s')
#             952 LOAD_CONST              13 ('py7')
#             954 LOAD_FAST               11 (@py_format6)
#             956 BUILD_MAP                1
#             958 BINARY_OP                6 (%)
#             962 STORE_FAST              12 (@py_format8)
#             964 LOAD_GLOBAL             23 (NULL + AssertionError)
#             974 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             984 LOAD_ATTR               24 (_format_explanation)
#            1004 LOAD_FAST               12 (@py_format8)
#            1006 CALL                     1
#            1014 CALL                     1
#            1022 RAISE_VARARGS            1
#         >> 1024 LOAD_CONST               0 (None)
#            1026 COPY                     1
#            1028 STORE_FAST               5 (@py_assert1)
#            1030 COPY                     1
#            1032 STORE_FAST               7 (@py_assert3)
#            1034 STORE_FAST              10 (@py_assert4)
#            1036 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_short_circuit_failure_includes_error at 0x3afa8540, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 116>:
# 116           0 RESUME                   0
# 
# 118           2 LOAD_GLOBAL              1 (NULL + ShortCircuitSkill)
#              12 CALL                     0
#              20 STORE_FAST               2 (skill)
# 
# 119          22 LOAD_CONST               1 ('model')
#              24 BUILD_MAP                0
#              26 BUILD_MAP                1
#              28 STORE_FAST               3 (config)
# 
# 120          30 LOAD_FAST                2 (skill)
#              32 LOAD_ATTR                3 (NULL|self + run)
#              52 LOAD_FAST                3 (config)
#              54 CALL                     1
#              62 STORE_FAST               4 (result)
# 
# 121          64 LOAD_FAST                4 (result)
#              66 LOAD_ATTR                4 (status)
#              86 STORE_FAST               5 (@py_assert1)
#              88 LOAD_GLOBAL              6 (SkillStatus)
#              98 LOAD_ATTR                8 (FAILED)
#             118 STORE_FAST               6 (@py_assert5)
#             120 LOAD_FAST                5 (@py_assert1)
#             122 LOAD_FAST                6 (@py_assert5)
#             124 COMPARE_OP              40 (==)
#             128 STORE_FAST               7 (@py_assert3)
#             130 LOAD_FAST                7 (@py_assert3)
#             132 POP_JUMP_IF_TRUE       246 (to 626)
#             134 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             144 LOAD_ATTR               12 (_call_reprcompare)
#             164 LOAD_CONST               2 (('==',))
#             166 LOAD_FAST                7 (@py_assert3)
#             168 BUILD_TUPLE              1
#             170 LOAD_CONST               3 (('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py6)s\n{%(py6)s = %(py4)s.FAILED\n}',))
#             172 LOAD_FAST                5 (@py_assert1)
#             174 LOAD_FAST                6 (@py_assert5)
#             176 BUILD_TUPLE              2
#             178 CALL                     4
#             186 LOAD_CONST               4 ('result')
#             188 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             198 LOAD_ATTR               16 (locals)
#             218 CALL                     0
#             226 CONTAINS_OP              0
#             228 POP_JUMP_IF_TRUE        21 (to 272)
#             230 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             240 LOAD_ATTR               18 (_should_repr_global_name)
#             260 LOAD_FAST                4 (result)
#             262 CALL                     1
#             270 POP_JUMP_IF_FALSE       21 (to 314)
#         >>  272 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             282 LOAD_ATTR               20 (_saferepr)
#             302 LOAD_FAST                4 (result)
#             304 CALL                     1
#             312 JUMP_FORWARD             1 (to 316)
#         >>  314 LOAD_CONST               4 ('result')
#         >>  316 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             326 LOAD_ATTR               20 (_saferepr)
#             346 LOAD_FAST                5 (@py_assert1)
#             348 CALL                     1
#             356 LOAD_CONST               5 ('SkillStatus')
#             358 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             368 LOAD_ATTR               16 (locals)
#             388 CALL                     0
#             396 CONTAINS_OP              0
#             398 POP_JUMP_IF_TRUE        25 (to 450)
#             400 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             410 LOAD_ATTR               18 (_should_repr_global_name)
#             430 LOAD_GLOBAL              6 (SkillStatus)
#             440 CALL                     1
#             448 POP_JUMP_IF_FALSE       25 (to 500)
#         >>  450 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             460 LOAD_ATTR               20 (_saferepr)
#             480 LOAD_GLOBAL              6 (SkillStatus)
#             490 CALL                     1
#             498 JUMP_FORWARD             1 (to 502)
#         >>  500 LOAD_CONST               5 ('SkillStatus')
#         >>  502 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             512 LOAD_ATTR               20 (_saferepr)
#             532 LOAD_FAST                6 (@py_assert5)
#             534 CALL                     1
#             542 LOAD_CONST               6 (('py0', 'py2', 'py4', 'py6'))
#             544 BUILD_CONST_KEY_MAP      4
#             546 BINARY_OP                6 (%)
#             550 STORE_FAST               8 (@py_format7)
#             552 LOAD_CONST               7 ('assert %(py8)s')
#             554 LOAD_CONST               8 ('py8')
#             556 LOAD_FAST                8 (@py_format7)
#             558 BUILD_MAP                1
#             560 BINARY_OP                6 (%)
#             564 STORE_FAST               9 (@py_format9)
#             566 LOAD_GLOBAL             23 (NULL + AssertionError)
#             576 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             586 LOAD_ATTR               24 (_format_explanation)
#             606 LOAD_FAST                9 (@py_format9)
#             608 CALL                     1
#             616 CALL                     1
#             624 RAISE_VARARGS            1
#         >>  626 LOAD_CONST               0 (None)
#             628 COPY                     1
#             630 STORE_FAST               5 (@py_assert1)
#             632 COPY                     1
#             634 STORE_FAST               7 (@py_assert3)
#             636 STORE_FAST               6 (@py_assert5)
# 
# 122         638 LOAD_FAST                4 (result)
#             640 LOAD_ATTR               26 (error)
#             660 STORE_FAST               5 (@py_assert1)
#             662 LOAD_CONST               0 (None)
#             664 STORE_FAST              10 (@py_assert4)
#             666 LOAD_FAST                5 (@py_assert1)
#             668 LOAD_FAST               10 (@py_assert4)
#             670 IS_OP                    1
#             672 STORE_FAST               7 (@py_assert3)
#             674 LOAD_FAST                7 (@py_assert3)
#             676 POP_JUMP_IF_TRUE       173 (to 1024)
#             678 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             688 LOAD_ATTR               12 (_call_reprcompare)
#             708 LOAD_CONST               9 (('is not',))
#             710 LOAD_FAST                7 (@py_assert3)
#             712 BUILD_TUPLE              1
#             714 LOAD_CONST              10 (('%(py2)s\n{%(py2)s = %(py0)s.error\n} is not %(py5)s',))
#             716 LOAD_FAST                5 (@py_assert1)
#             718 LOAD_FAST               10 (@py_assert4)
#             720 BUILD_TUPLE              2
#             722 CALL                     4
#             730 LOAD_CONST               4 ('result')
#             732 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             742 LOAD_ATTR               16 (locals)
#             762 CALL                     0
#             770 CONTAINS_OP              0
#             772 POP_JUMP_IF_TRUE        21 (to 816)
#             774 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             784 LOAD_ATTR               18 (_should_repr_global_name)
#             804 LOAD_FAST                4 (result)
#             806 CALL                     1
#             814 POP_JUMP_IF_FALSE       21 (to 858)
#         >>  816 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             826 LOAD_ATTR               20 (_saferepr)
#             846 LOAD_FAST                4 (result)
#             848 CALL                     1
#             856 JUMP_FORWARD             1 (to 860)
#         >>  858 LOAD_CONST               4 ('result')
#         >>  860 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             870 LOAD_ATTR               20 (_saferepr)
#             890 LOAD_FAST                5 (@py_assert1)
#             892 CALL                     1
#             900 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             910 LOAD_ATTR               20 (_saferepr)
#             930 LOAD_FAST               10 (@py_assert4)
#             932 CALL                     1
#             940 LOAD_CONST              11 (('py0', 'py2', 'py5'))
#             942 BUILD_CONST_KEY_MAP      3
#             944 BINARY_OP                6 (%)
#             948 STORE_FAST              11 (@py_format6)
#             950 LOAD_CONST              12 ('assert %(py7)s')
#             952 LOAD_CONST              13 ('py7')
#             954 LOAD_FAST               11 (@py_format6)
#             956 BUILD_MAP                1
#             958 BINARY_OP                6 (%)
#             962 STORE_FAST              12 (@py_format8)
#             964 LOAD_GLOBAL             23 (NULL + AssertionError)
#             974 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             984 LOAD_ATTR               24 (_format_explanation)
#            1004 LOAD_FAST               12 (@py_format8)
#            1006 CALL                     1
#            1014 CALL                     1
#            1022 RAISE_VARARGS            1
#         >> 1024 LOAD_CONST               0 (None)
#            1026 COPY                     1
#            1028 STORE_FAST               5 (@py_assert1)
#            1030 COPY                     1
#            1032 STORE_FAST               7 (@py_assert3)
#            1034 STORE_FAST              10 (@py_assert4)
#            1036 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestValidatorWithAllSkills at 0x73cd93b065b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 125>:
# 125           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestValidatorWithAllSkills')
#               8 STORE_NAME               2 (__qualname__)
# 
# 126          10 LOAD_CONST               1 ('Test validator with all skill types.')
#              12 STORE_NAME               3 (__doc__)
# 
# 128          14 LOAD_CONST               2 (<code object test_power_flow_result_validation at 0x3aef47a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 128>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_power_flow_result_validation)
# 
# 137          20 LOAD_CONST               3 (<code object test_emt_result_validation at 0x3aef8860, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 137>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_emt_result_validation)
# 
# 146          26 LOAD_CONST               4 (<code object test_short_circuit_result_validation at 0x3aefbf80, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 146>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_short_circuit_result_validation)
#              32 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_power_flow_result_validation at 0x3aef47a0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 128>:
# 128           0 RESUME                   0
# 
# 129           2 LOAD_GLOBAL              1 (NULL + SkillOutputValidator)
#              12 CALL                     0
#              20 STORE_FAST               1 (validator)
# 
# 130          22 LOAD_GLOBAL              3 (NULL + SkillResult)
#              32 LOAD_ATTR                4 (success)
# 
# 131          52 LOAD_CONST               1 ('power_flow')
# 
# 132          54 LOAD_CONST               2 (True)
#              56 BUILD_MAP                0
#              58 BUILD_MAP                0
#              60 LOAD_CONST               3 (('converged', 'model_info', 'summary'))
#              62 BUILD_CONST_KEY_MAP      3
# 
# 130          64 KW_NAMES                 4 (('skill_name', 'data'))
#              66 CALL                     2
#              74 STORE_FAST               2 (result)
# 
# 134          76 LOAD_FAST                1 (validator)
#              78 LOAD_ATTR                7 (NULL|self + validate)
#              98 LOAD_FAST                2 (result)
#             100 CALL                     1
#             108 STORE_FAST               3 (validation)
# 
# 135         110 LOAD_FAST                3 (validation)
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
# Disassembly of <code object test_emt_result_validation at 0x3aef8860, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 137>:
# 137           0 RESUME                   0
# 
# 138           2 LOAD_GLOBAL              1 (NULL + SkillOutputValidator)
#              12 CALL                     0
#              20 STORE_FAST               1 (validator)
# 
# 139          22 LOAD_GLOBAL              3 (NULL + SkillResult)
#              32 LOAD_ATTR                4 (success)
# 
# 140          52 LOAD_CONST               1 ('emt_simulation')
# 
# 141          54 LOAD_CONST               2 (True)
#              56 BUILD_MAP                0
#              58 BUILD_MAP                0
#              60 LOAD_CONST               3 (('converged', 'model_info', 'summary'))
#              62 BUILD_CONST_KEY_MAP      3
# 
# 139          64 KW_NAMES                 4 (('skill_name', 'data'))
#              66 CALL                     2
#              74 STORE_FAST               2 (result)
# 
# 143          76 LOAD_FAST                1 (validator)
#              78 LOAD_ATTR                7 (NULL|self + validate)
#              98 LOAD_FAST                2 (result)
#             100 CALL                     1
#             108 STORE_FAST               3 (validation)
# 
# 144         110 LOAD_FAST                3 (validation)
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
# Disassembly of <code object test_short_circuit_result_validation at 0x3aefbf80, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 146>:
# 146           0 RESUME                   0
# 
# 147           2 LOAD_GLOBAL              1 (NULL + SkillOutputValidator)
#              12 CALL                     0
#              20 STORE_FAST               1 (validator)
# 
# 148          22 LOAD_GLOBAL              3 (NULL + SkillResult)
#              32 LOAD_ATTR                4 (success)
# 
# 149          52 LOAD_CONST               1 ('short_circuit')
# 
# 150          54 LOAD_CONST               2 (True)
#              56 BUILD_MAP                0
#              58 BUILD_MAP                0
#              60 LOAD_CONST               3 (('converged', 'model_info', 'summary'))
#              62 BUILD_CONST_KEY_MAP      3
# 
# 148          64 KW_NAMES                 4 (('skill_name', 'data'))
#              66 CALL                     2
#              74 STORE_FAST               2 (result)
# 
# 152          76 LOAD_FAST                1 (validator)
#              78 LOAD_ATTR                7 (NULL|self + validate)
#              98 LOAD_FAST                2 (result)
#             100 CALL                     1
#             108 STORE_FAST               3 (validation)
# 
# 153         110 LOAD_FAST                3 (validation)
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
# Disassembly of <code object TestSkillResultToDict at 0x73cd93b06970, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 156>:
# 156           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestSkillResultToDict')
#               8 STORE_NAME               2 (__qualname__)
# 
# 157          10 LOAD_CONST               1 ('Test SkillResult serialization.')
#              12 STORE_NAME               3 (__doc__)
# 
# 159          14 LOAD_CONST               2 (<code object test_power_flow_result_serialization at 0x3afa9cf0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 159>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_power_flow_result_serialization)
# 
# 171          20 LOAD_CONST               3 (<code object test_emt_result_serialization at 0x3aed0c90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 171>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_emt_result_serialization)
# 
# 180          26 LOAD_CONST               4 (<code object test_failure_result_serialization at 0x3afaa320, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 180>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_failure_result_serialization)
#              32 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_power_flow_result_serialization at 0x3afa9cf0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 159>:
# 159           0 RESUME                   0
# 
# 160           2 LOAD_GLOBAL              1 (NULL + SkillResult)
#              12 LOAD_ATTR                2 (success)
# 
# 161          32 LOAD_CONST               1 ('power_flow')
# 
# 162          34 LOAD_CONST               2 (True)
#              36 LOAD_CONST               3 (10)
#              38 LOAD_CONST               4 (('converged', 'bus_count'))
#              40 BUILD_CONST_KEY_MAP      2
# 
# 160          42 KW_NAMES                 5 (('skill_name', 'data'))
#              44 CALL                     2
#              52 STORE_FAST               1 (result)
# 
# 164          54 LOAD_FAST                1 (result)
#              56 LOAD_ATTR                5 (NULL|self + to_dict)
#              76 CALL                     0
#              84 STORE_FAST               2 (d)
# 
# 165          86 LOAD_FAST                2 (d)
#              88 LOAD_CONST               6 ('skill_name')
#              90 BINARY_SUBSCR
#              94 STORE_FAST               3 (@py_assert0)
#              96 LOAD_CONST               1 ('power_flow')
#              98 STORE_FAST               4 (@py_assert3)
#             100 LOAD_FAST                3 (@py_assert0)
#             102 LOAD_FAST                4 (@py_assert3)
#             104 COMPARE_OP              40 (==)
#             108 STORE_FAST               5 (@py_assert2)
#             110 LOAD_FAST                5 (@py_assert2)
#             112 POP_JUMP_IF_TRUE       108 (to 330)
#             114 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             124 LOAD_ATTR                8 (_call_reprcompare)
#             144 LOAD_CONST               7 (('==',))
#             146 LOAD_FAST                5 (@py_assert2)
#             148 BUILD_TUPLE              1
#             150 LOAD_CONST               8 (('%(py1)s == %(py4)s',))
#             152 LOAD_FAST                3 (@py_assert0)
#             154 LOAD_FAST                4 (@py_assert3)
#             156 BUILD_TUPLE              2
#             158 CALL                     4
#             166 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             176 LOAD_ATTR               10 (_saferepr)
#             196 LOAD_FAST                3 (@py_assert0)
#             198 CALL                     1
#             206 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             216 LOAD_ATTR               10 (_saferepr)
#             236 LOAD_FAST                4 (@py_assert3)
#             238 CALL                     1
#             246 LOAD_CONST               9 (('py1', 'py4'))
#             248 BUILD_CONST_KEY_MAP      2
#             250 BINARY_OP                6 (%)
#             254 STORE_FAST               6 (@py_format5)
#             256 LOAD_CONST              10 ('assert %(py6)s')
#             258 LOAD_CONST              11 ('py6')
#             260 LOAD_FAST                6 (@py_format5)
#             262 BUILD_MAP                1
#             264 BINARY_OP                6 (%)
#             268 STORE_FAST               7 (@py_format7)
#             270 LOAD_GLOBAL             13 (NULL + AssertionError)
#             280 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             290 LOAD_ATTR               14 (_format_explanation)
#             310 LOAD_FAST                7 (@py_format7)
#             312 CALL                     1
#             320 CALL                     1
#             328 RAISE_VARARGS            1
#         >>  330 LOAD_CONST               0 (None)
#             332 COPY                     1
#             334 STORE_FAST               3 (@py_assert0)
#             336 COPY                     1
#             338 STORE_FAST               5 (@py_assert2)
#             340 STORE_FAST               4 (@py_assert3)
# 
# 166         342 LOAD_FAST                2 (d)
#             344 LOAD_CONST              12 ('status')
#             346 BINARY_SUBSCR
#             350 STORE_FAST               3 (@py_assert0)
#             352 LOAD_CONST              13 ('success')
#             354 STORE_FAST               4 (@py_assert3)
#             356 LOAD_FAST                3 (@py_assert0)
#             358 LOAD_FAST                4 (@py_assert3)
#             360 COMPARE_OP              40 (==)
#             364 STORE_FAST               5 (@py_assert2)
#             366 LOAD_FAST                5 (@py_assert2)
#             368 POP_JUMP_IF_TRUE       108 (to 586)
#             370 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             380 LOAD_ATTR                8 (_call_reprcompare)
#             400 LOAD_CONST               7 (('==',))
#             402 LOAD_FAST                5 (@py_assert2)
#             404 BUILD_TUPLE              1
#             406 LOAD_CONST               8 (('%(py1)s == %(py4)s',))
#             408 LOAD_FAST                3 (@py_assert0)
#             410 LOAD_FAST                4 (@py_assert3)
#             412 BUILD_TUPLE              2
#             414 CALL                     4
#             422 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             432 LOAD_ATTR               10 (_saferepr)
#             452 LOAD_FAST                3 (@py_assert0)
#             454 CALL                     1
#             462 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             472 LOAD_ATTR               10 (_saferepr)
#             492 LOAD_FAST                4 (@py_assert3)
#             494 CALL                     1
#             502 LOAD_CONST               9 (('py1', 'py4'))
#             504 BUILD_CONST_KEY_MAP      2
#             506 BINARY_OP                6 (%)
#             510 STORE_FAST               6 (@py_format5)
#             512 LOAD_CONST              10 ('assert %(py6)s')
#             514 LOAD_CONST              11 ('py6')
#             516 LOAD_FAST                6 (@py_format5)
#             518 BUILD_MAP                1
#             520 BINARY_OP                6 (%)
#             524 STORE_FAST               7 (@py_format7)
#             526 LOAD_GLOBAL             13 (NULL + AssertionError)
#             536 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             546 LOAD_ATTR               14 (_format_explanation)
#             566 LOAD_FAST                7 (@py_format7)
#             568 CALL                     1
#             576 CALL                     1
#             584 RAISE_VARARGS            1
#         >>  586 LOAD_CONST               0 (None)
#             588 COPY                     1
#             590 STORE_FAST               3 (@py_assert0)
#             592 COPY                     1
#             594 STORE_FAST               5 (@py_assert2)
#             596 STORE_FAST               4 (@py_assert3)
# 
# 167         598 LOAD_FAST                2 (d)
#             600 LOAD_CONST              13 ('success')
#             602 BINARY_SUBSCR
#             606 STORE_FAST               3 (@py_assert0)
#             608 LOAD_CONST               2 (True)
#             610 STORE_FAST               4 (@py_assert3)
#             612 LOAD_FAST                3 (@py_assert0)
#             614 LOAD_FAST                4 (@py_assert3)
#             616 IS_OP                    0
#             618 STORE_FAST               5 (@py_assert2)
#             620 LOAD_FAST                5 (@py_assert2)
#             622 POP_JUMP_IF_TRUE       108 (to 840)
#             624 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             634 LOAD_ATTR                8 (_call_reprcompare)
#             654 LOAD_CONST              14 (('is',))
#             656 LOAD_FAST                5 (@py_assert2)
#             658 BUILD_TUPLE              1
#             660 LOAD_CONST              15 (('%(py1)s is %(py4)s',))
#             662 LOAD_FAST                3 (@py_assert0)
#             664 LOAD_FAST                4 (@py_assert3)
#             666 BUILD_TUPLE              2
#             668 CALL                     4
#             676 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             686 LOAD_ATTR               10 (_saferepr)
#             706 LOAD_FAST                3 (@py_assert0)
#             708 CALL                     1
#             716 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             726 LOAD_ATTR               10 (_saferepr)
#             746 LOAD_FAST                4 (@py_assert3)
#             748 CALL                     1
#             756 LOAD_CONST               9 (('py1', 'py4'))
#             758 BUILD_CONST_KEY_MAP      2
#             760 BINARY_OP                6 (%)
#             764 STORE_FAST               6 (@py_format5)
#             766 LOAD_CONST              10 ('assert %(py6)s')
#             768 LOAD_CONST              11 ('py6')
#             770 LOAD_FAST                6 (@py_format5)
#             772 BUILD_MAP                1
#             774 BINARY_OP                6 (%)
#             778 STORE_FAST               7 (@py_format7)
#             780 LOAD_GLOBAL             13 (NULL + AssertionError)
#             790 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             800 LOAD_ATTR               14 (_format_explanation)
#             820 LOAD_FAST                7 (@py_format7)
#             822 CALL                     1
#             830 CALL                     1
#             838 RAISE_VARARGS            1
#         >>  840 LOAD_CONST               0 (None)
#             842 COPY                     1
#             844 STORE_FAST               3 (@py_assert0)
#             846 COPY                     1
#             848 STORE_FAST               5 (@py_assert2)
#             850 STORE_FAST               4 (@py_assert3)
# 
# 168         852 LOAD_FAST                2 (d)
#             854 LOAD_CONST              16 ('data')
#             856 BINARY_SUBSCR
#             860 LOAD_CONST              17 ('converged')
#             862 BINARY_SUBSCR
#             866 STORE_FAST               3 (@py_assert0)
#             868 LOAD_CONST               2 (True)
#             870 STORE_FAST               4 (@py_assert3)
#             872 LOAD_FAST                3 (@py_assert0)
#             874 LOAD_FAST                4 (@py_assert3)
#             876 IS_OP                    0
#             878 STORE_FAST               5 (@py_assert2)
#             880 LOAD_FAST                5 (@py_assert2)
#             882 POP_JUMP_IF_TRUE       108 (to 1100)
#             884 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             894 LOAD_ATTR                8 (_call_reprcompare)
#             914 LOAD_CONST              14 (('is',))
#             916 LOAD_FAST                5 (@py_assert2)
#             918 BUILD_TUPLE              1
#             920 LOAD_CONST              15 (('%(py1)s is %(py4)s',))
#             922 LOAD_FAST                3 (@py_assert0)
#             924 LOAD_FAST                4 (@py_assert3)
#             926 BUILD_TUPLE              2
#             928 CALL                     4
#             936 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             946 LOAD_ATTR               10 (_saferepr)
#             966 LOAD_FAST                3 (@py_assert0)
#             968 CALL                     1
#             976 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             986 LOAD_ATTR               10 (_saferepr)
#            1006 LOAD_FAST                4 (@py_assert3)
#            1008 CALL                     1
#            1016 LOAD_CONST               9 (('py1', 'py4'))
#            1018 BUILD_CONST_KEY_MAP      2
#            1020 BINARY_OP                6 (%)
#            1024 STORE_FAST               6 (@py_format5)
#            1026 LOAD_CONST              10 ('assert %(py6)s')
#            1028 LOAD_CONST              11 ('py6')
#            1030 LOAD_FAST                6 (@py_format5)
#            1032 BUILD_MAP                1
#            1034 BINARY_OP                6 (%)
#            1038 STORE_FAST               7 (@py_format7)
#            1040 LOAD_GLOBAL             13 (NULL + AssertionError)
#            1050 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1060 LOAD_ATTR               14 (_format_explanation)
#            1080 LOAD_FAST                7 (@py_format7)
#            1082 CALL                     1
#            1090 CALL                     1
#            1098 RAISE_VARARGS            1
#         >> 1100 LOAD_CONST               0 (None)
#            1102 COPY                     1
#            1104 STORE_FAST               3 (@py_assert0)
#            1106 COPY                     1
#            1108 STORE_FAST               5 (@py_assert2)
#            1110 STORE_FAST               4 (@py_assert3)
# 
# 169        1112 LOAD_FAST                2 (d)
#            1114 LOAD_CONST              16 ('data')
#            1116 BINARY_SUBSCR
#            1120 LOAD_CONST              18 ('bus_count')
#            1122 BINARY_SUBSCR
#            1126 STORE_FAST               3 (@py_assert0)
#            1128 LOAD_CONST               3 (10)
#            1130 STORE_FAST               4 (@py_assert3)
#            1132 LOAD_FAST                3 (@py_assert0)
#            1134 LOAD_FAST                4 (@py_assert3)
#            1136 COMPARE_OP              40 (==)
#            1140 STORE_FAST               5 (@py_assert2)
#            1142 LOAD_FAST                5 (@py_assert2)
#            1144 POP_JUMP_IF_TRUE       108 (to 1362)
#            1146 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1156 LOAD_ATTR                8 (_call_reprcompare)
#            1176 LOAD_CONST               7 (('==',))
#            1178 LOAD_FAST                5 (@py_assert2)
#            1180 BUILD_TUPLE              1
#            1182 LOAD_CONST               8 (('%(py1)s == %(py4)s',))
#            1184 LOAD_FAST                3 (@py_assert0)
#            1186 LOAD_FAST                4 (@py_assert3)
#            1188 BUILD_TUPLE              2
#            1190 CALL                     4
#            1198 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1208 LOAD_ATTR               10 (_saferepr)
#            1228 LOAD_FAST                3 (@py_assert0)
#            1230 CALL                     1
#            1238 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1248 LOAD_ATTR               10 (_saferepr)
#            1268 LOAD_FAST                4 (@py_assert3)
#            1270 CALL                     1
#            1278 LOAD_CONST               9 (('py1', 'py4'))
#            1280 BUILD_CONST_KEY_MAP      2
#            1282 BINARY_OP                6 (%)
#            1286 STORE_FAST               6 (@py_format5)
#            1288 LOAD_CONST              10 ('assert %(py6)s')
#            1290 LOAD_CONST              11 ('py6')
#            1292 LOAD_FAST                6 (@py_format5)
#            1294 BUILD_MAP                1
#            1296 BINARY_OP                6 (%)
#            1300 STORE_FAST               7 (@py_format7)
#            1302 LOAD_GLOBAL             13 (NULL + AssertionError)
#            1312 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1322 LOAD_ATTR               14 (_format_explanation)
#            1342 LOAD_FAST                7 (@py_format7)
#            1344 CALL                     1
#            1352 CALL                     1
#            1360 RAISE_VARARGS            1
#         >> 1362 LOAD_CONST               0 (None)
#            1364 COPY                     1
#            1366 STORE_FAST               3 (@py_assert0)
#            1368 COPY                     1
#            1370 STORE_FAST               5 (@py_assert2)
#            1372 STORE_FAST               4 (@py_assert3)
#            1374 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_emt_result_serialization at 0x3aed0c90, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 171>:
# 171           0 RESUME                   0
# 
# 172           2 LOAD_GLOBAL              1 (NULL + SkillResult)
#              12 LOAD_ATTR                2 (success)
# 
# 173          32 LOAD_CONST               1 ('emt_simulation')
# 
# 174          34 LOAD_CONST               2 ('waveform_count')
#              36 LOAD_CONST               3 (5)
#              38 BUILD_MAP                1
# 
# 172          40 KW_NAMES                 4 (('skill_name', 'data'))
#              42 CALL                     2
#              50 STORE_FAST               1 (result)
# 
# 176          52 LOAD_FAST                1 (result)
#              54 LOAD_ATTR                5 (NULL|self + to_dict)
#              74 CALL                     0
#              82 STORE_FAST               2 (d)
# 
# 177          84 LOAD_FAST                2 (d)
#              86 LOAD_CONST               5 ('skill_name')
#              88 BINARY_SUBSCR
#              92 STORE_FAST               3 (@py_assert0)
#              94 LOAD_CONST               1 ('emt_simulation')
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
# 178         340 LOAD_FAST                2 (d)
#             342 LOAD_CONST              11 ('data')
#             344 BINARY_SUBSCR
#             348 LOAD_CONST               2 ('waveform_count')
#             350 BINARY_SUBSCR
#             354 STORE_FAST               3 (@py_assert0)
#             356 LOAD_CONST               3 (5)
#             358 STORE_FAST               4 (@py_assert3)
#             360 LOAD_FAST                3 (@py_assert0)
#             362 LOAD_FAST                4 (@py_assert3)
#             364 COMPARE_OP              40 (==)
#             368 STORE_FAST               5 (@py_assert2)
#             370 LOAD_FAST                5 (@py_assert2)
#             372 POP_JUMP_IF_TRUE       108 (to 590)
#             374 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             384 LOAD_ATTR                8 (_call_reprcompare)
#             404 LOAD_CONST               6 (('==',))
#             406 LOAD_FAST                5 (@py_assert2)
#             408 BUILD_TUPLE              1
#             410 LOAD_CONST               7 (('%(py1)s == %(py4)s',))
#             412 LOAD_FAST                3 (@py_assert0)
#             414 LOAD_FAST                4 (@py_assert3)
#             416 BUILD_TUPLE              2
#             418 CALL                     4
#             426 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             436 LOAD_ATTR               10 (_saferepr)
#             456 LOAD_FAST                3 (@py_assert0)
#             458 CALL                     1
#             466 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             476 LOAD_ATTR               10 (_saferepr)
#             496 LOAD_FAST                4 (@py_assert3)
#             498 CALL                     1
#             506 LOAD_CONST               8 (('py1', 'py4'))
#             508 BUILD_CONST_KEY_MAP      2
#             510 BINARY_OP                6 (%)
#             514 STORE_FAST               6 (@py_format5)
#             516 LOAD_CONST               9 ('assert %(py6)s')
#             518 LOAD_CONST              10 ('py6')
#             520 LOAD_FAST                6 (@py_format5)
#             522 BUILD_MAP                1
#             524 BINARY_OP                6 (%)
#             528 STORE_FAST               7 (@py_format7)
#             530 LOAD_GLOBAL             13 (NULL + AssertionError)
#             540 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             550 LOAD_ATTR               14 (_format_explanation)
#             570 LOAD_FAST                7 (@py_format7)
#             572 CALL                     1
#             580 CALL                     1
#             588 RAISE_VARARGS            1
#         >>  590 LOAD_CONST               0 (None)
#             592 COPY                     1
#             594 STORE_FAST               3 (@py_assert0)
#             596 COPY                     1
#             598 STORE_FAST               5 (@py_assert2)
#             600 STORE_FAST               4 (@py_assert3)
#             602 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_failure_result_serialization at 0x3afaa320, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_skills_integration.py", line 180>:
# 180           0 RESUME                   0
# 
# 181           2 LOAD_GLOBAL              1 (NULL + SkillResult)
#              12 LOAD_ATTR                2 (failure)
# 
# 182          32 LOAD_CONST               1 ('power_flow')
# 
# 183          34 LOAD_CONST               2 ('Test error')
# 
# 184          36 LOAD_CONST               3 ('stage')
#              38 LOAD_CONST               4 ('validation')
#              40 BUILD_MAP                1
# 
# 181          42 KW_NAMES                 5 (('skill_name', 'error', 'data'))
#              44 CALL                     3
#              52 STORE_FAST               1 (result)
# 
# 186          54 LOAD_FAST                1 (result)
#              56 LOAD_ATTR                5 (NULL|self + to_dict)
#              76 CALL                     0
#              84 STORE_FAST               2 (d)
# 
# 187          86 LOAD_FAST                2 (d)
#              88 LOAD_CONST               6 ('status')
#              90 BINARY_SUBSCR
#              94 STORE_FAST               3 (@py_assert0)
#              96 LOAD_CONST               7 ('failed')
#              98 STORE_FAST               4 (@py_assert3)
#             100 LOAD_FAST                3 (@py_assert0)
#             102 LOAD_FAST                4 (@py_assert3)
#             104 COMPARE_OP              40 (==)
#             108 STORE_FAST               5 (@py_assert2)
#             110 LOAD_FAST                5 (@py_assert2)
#             112 POP_JUMP_IF_TRUE       108 (to 330)
#             114 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             124 LOAD_ATTR                8 (_call_reprcompare)
#             144 LOAD_CONST               8 (('==',))
#             146 LOAD_FAST                5 (@py_assert2)
#             148 BUILD_TUPLE              1
#             150 LOAD_CONST               9 (('%(py1)s == %(py4)s',))
#             152 LOAD_FAST                3 (@py_assert0)
#             154 LOAD_FAST                4 (@py_assert3)
#             156 BUILD_TUPLE              2
#             158 CALL                     4
#             166 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             176 LOAD_ATTR               10 (_saferepr)
#             196 LOAD_FAST                3 (@py_assert0)
#             198 CALL                     1
#             206 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             216 LOAD_ATTR               10 (_saferepr)
#             236 LOAD_FAST                4 (@py_assert3)
#             238 CALL                     1
#             246 LOAD_CONST              10 (('py1', 'py4'))
#             248 BUILD_CONST_KEY_MAP      2
#             250 BINARY_OP                6 (%)
#             254 STORE_FAST               6 (@py_format5)
#             256 LOAD_CONST              11 ('assert %(py6)s')
#             258 LOAD_CONST              12 ('py6')
#             260 LOAD_FAST                6 (@py_format5)
#             262 BUILD_MAP                1
#             264 BINARY_OP                6 (%)
#             268 STORE_FAST               7 (@py_format7)
#             270 LOAD_GLOBAL             13 (NULL + AssertionError)
#             280 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             290 LOAD_ATTR               14 (_format_explanation)
#             310 LOAD_FAST                7 (@py_format7)
#             312 CALL                     1
#             320 CALL                     1
#             328 RAISE_VARARGS            1
#         >>  330 LOAD_CONST               0 (None)
#             332 COPY                     1
#             334 STORE_FAST               3 (@py_assert0)
#             336 COPY                     1
#             338 STORE_FAST               5 (@py_assert2)
#             340 STORE_FAST               4 (@py_assert3)
# 
# 188         342 LOAD_FAST                2 (d)
#             344 LOAD_CONST              13 ('success')
#             346 BINARY_SUBSCR
#             350 STORE_FAST               3 (@py_assert0)
#             352 LOAD_CONST              14 (False)
#             354 STORE_FAST               4 (@py_assert3)
#             356 LOAD_FAST                3 (@py_assert0)
#             358 LOAD_FAST                4 (@py_assert3)
#             360 IS_OP                    0
#             362 STORE_FAST               5 (@py_assert2)
#             364 LOAD_FAST                5 (@py_assert2)
#             366 POP_JUMP_IF_TRUE       108 (to 584)
#             368 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             378 LOAD_ATTR                8 (_call_reprcompare)
#             398 LOAD_CONST              15 (('is',))
#             400 LOAD_FAST                5 (@py_assert2)
#             402 BUILD_TUPLE              1
#             404 LOAD_CONST              16 (('%(py1)s is %(py4)s',))
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
#             500 LOAD_CONST              10 (('py1', 'py4'))
#             502 BUILD_CONST_KEY_MAP      2
#             504 BINARY_OP                6 (%)
#             508 STORE_FAST               6 (@py_format5)
#             510 LOAD_CONST              11 ('assert %(py6)s')
#             512 LOAD_CONST              12 ('py6')
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
# 189         596 LOAD_FAST                2 (d)
#             598 LOAD_CONST              17 ('error')
#             600 BINARY_SUBSCR
#             604 STORE_FAST               3 (@py_assert0)
#             606 LOAD_CONST               2 ('Test error')
#             608 STORE_FAST               4 (@py_assert3)
#             610 LOAD_FAST                3 (@py_assert0)
#             612 LOAD_FAST                4 (@py_assert3)
#             614 COMPARE_OP              40 (==)
#             618 STORE_FAST               5 (@py_assert2)
#             620 LOAD_FAST                5 (@py_assert2)
#             622 POP_JUMP_IF_TRUE       108 (to 840)
#             624 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             634 LOAD_ATTR                8 (_call_reprcompare)
#             654 LOAD_CONST               8 (('==',))
#             656 LOAD_FAST                5 (@py_assert2)
#             658 BUILD_TUPLE              1
#             660 LOAD_CONST               9 (('%(py1)s == %(py4)s',))
#             662 LOAD_FAST                3 (@py_assert0)
#             664 LOAD_FAST                4 (@py_assert3)
#             666 BUILD_TUPLE              2
#             668 CALL                     4
#             676 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             686 LOAD_ATTR               10 (_saferepr)
#             706 LOAD_FAST                3 (@py_assert0)
#             708 CALL                     1
#             716 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             726 LOAD_ATTR               10 (_saferepr)
#             746 LOAD_FAST                4 (@py_assert3)
#             748 CALL                     1
#             756 LOAD_CONST              10 (('py1', 'py4'))
#             758 BUILD_CONST_KEY_MAP      2
#             760 BINARY_OP                6 (%)
#             764 STORE_FAST               6 (@py_format5)
#             766 LOAD_CONST              11 ('assert %(py6)s')
#             768 LOAD_CONST              12 ('py6')
#             770 LOAD_FAST                6 (@py_format5)
#             772 BUILD_MAP                1
#             774 BINARY_OP                6 (%)
#             778 STORE_FAST               7 (@py_format7)
#             780 LOAD_GLOBAL             13 (NULL + AssertionError)
#             790 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             800 LOAD_ATTR               14 (_format_explanation)
#             820 LOAD_FAST                7 (@py_format7)
#             822 CALL                     1
#             830 CALL                     1
#             838 RAISE_VARARGS            1
#         >>  840 LOAD_CONST               0 (None)
#             842 COPY                     1
#             844 STORE_FAST               3 (@py_assert0)
#             846 COPY                     1
#             848 STORE_FAST               5 (@py_assert2)
#             850 STORE_FAST               4 (@py_assert3)
# 
# 190         852 LOAD_FAST                2 (d)
#             854 LOAD_CONST              18 ('data')
#             856 BINARY_SUBSCR
#             860 LOAD_CONST               3 ('stage')
#             862 BINARY_SUBSCR
#             866 STORE_FAST               3 (@py_assert0)
#             868 LOAD_CONST               4 ('validation')
#             870 STORE_FAST               4 (@py_assert3)
#             872 LOAD_FAST                3 (@py_assert0)
#             874 LOAD_FAST                4 (@py_assert3)
#             876 COMPARE_OP              40 (==)
#             880 STORE_FAST               5 (@py_assert2)
#             882 LOAD_FAST                5 (@py_assert2)
#             884 POP_JUMP_IF_TRUE       108 (to 1102)
#             886 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             896 LOAD_ATTR                8 (_call_reprcompare)
#             916 LOAD_CONST               8 (('==',))
#             918 LOAD_FAST                5 (@py_assert2)
#             920 BUILD_TUPLE              1
#             922 LOAD_CONST               9 (('%(py1)s == %(py4)s',))
#             924 LOAD_FAST                3 (@py_assert0)
#             926 LOAD_FAST                4 (@py_assert3)
#             928 BUILD_TUPLE              2
#             930 CALL                     4
#             938 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             948 LOAD_ATTR               10 (_saferepr)
#             968 LOAD_FAST                3 (@py_assert0)
#             970 CALL                     1
#             978 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             988 LOAD_ATTR               10 (_saferepr)
#            1008 LOAD_FAST                4 (@py_assert3)
#            1010 CALL                     1
#            1018 LOAD_CONST              10 (('py1', 'py4'))
#            1020 BUILD_CONST_KEY_MAP      2
#            1022 BINARY_OP                6 (%)
#            1026 STORE_FAST               6 (@py_format5)
#            1028 LOAD_CONST              11 ('assert %(py6)s')
#            1030 LOAD_CONST              12 ('py6')
#            1032 LOAD_FAST                6 (@py_format5)
#            1034 BUILD_MAP                1
#            1036 BINARY_OP                6 (%)
#            1040 STORE_FAST               7 (@py_format7)
#            1042 LOAD_GLOBAL             13 (NULL + AssertionError)
#            1052 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1062 LOAD_ATTR               14 (_format_explanation)
#            1082 LOAD_FAST                7 (@py_format7)
#            1084 CALL                     1
#            1092 CALL                     1
#            1100 RAISE_VARARGS            1
#         >> 1102 LOAD_CONST               0 (None)
#            1104 COPY                     1
#            1106 STORE_FAST               3 (@py_assert0)
#            1108 COPY                     1
#            1110 STORE_FAST               5 (@py_assert2)
#            1112 STORE_FAST               4 (@py_assert3)
#            1114 RETURN_CONST             0 (None)
# 