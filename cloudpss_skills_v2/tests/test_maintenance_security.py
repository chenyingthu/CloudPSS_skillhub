# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/__pycache__/test_maintenance_security.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


def TestMaintenanceValidation():
    """TestMaintenanceValidation"""
pass  # TODO: restore


def TestMaintenanceSeverity():
    """TestMaintenanceSeverity"""
pass  # TODO: restore


def TestMaintenancePower():
    """TestMaintenancePower"""
pass  # TODO: restore


def TestMaintenanceN1Plan():
    """TestMaintenanceN1Plan"""
pass  # TODO: restore


def TestMaintenanceRun():
    """TestMaintenanceRun"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('Tests for MaintenanceSecuritySkill v2.')
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
#              42 LOAD_CONST               3 (('MaintenanceSecuritySkill',))
#              44 IMPORT_NAME              8 (cloudpss_skills_v2.skills.maintenance_security)
#              46 IMPORT_FROM              9 (MaintenanceSecuritySkill)
#              48 STORE_NAME               9 (MaintenanceSecuritySkill)
#              50 POP_TOP
# 
#   7          52 PUSH_NULL
#              54 LOAD_BUILD_CLASS
#              56 LOAD_CONST               4 (<code object TestMaintenanceValidation at 0x73cd945fedb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 7>)
#              58 MAKE_FUNCTION            0
#              60 LOAD_CONST               5 ('TestMaintenanceValidation')
#              62 CALL                     2
#              70 STORE_NAME              10 (TestMaintenanceValidation)
# 
#  25          72 PUSH_NULL
#              74 LOAD_BUILD_CLASS
#              76 LOAD_CONST               6 (<code object TestMaintenanceSeverity at 0x73cd93b06970, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 25>)
#              78 MAKE_FUNCTION            0
#              80 LOAD_CONST               7 ('TestMaintenanceSeverity')
#              82 CALL                     2
#              90 STORE_NAME              11 (TestMaintenanceSeverity)
# 
#  47          92 PUSH_NULL
#              94 LOAD_BUILD_CLASS
#              96 LOAD_CONST               8 (<code object TestMaintenancePower at 0x73cd93b065b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 47>)
#              98 MAKE_FUNCTION            0
#             100 LOAD_CONST               9 ('TestMaintenancePower')
#             102 CALL                     2
#             110 STORE_NAME              12 (TestMaintenancePower)
# 
#  70         112 PUSH_NULL
#             114 LOAD_BUILD_CLASS
#             116 LOAD_CONST              10 (<code object TestMaintenanceN1Plan at 0x73cd945fe870, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 70>)
#             118 MAKE_FUNCTION            0
#             120 LOAD_CONST              11 ('TestMaintenanceN1Plan')
#             122 CALL                     2
#             130 STORE_NAME              13 (TestMaintenanceN1Plan)
# 
#  79         132 PUSH_NULL
#             134 LOAD_BUILD_CLASS
#             136 LOAD_CONST              12 (<code object TestMaintenanceRun at 0x73cd945fe090, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 79>)
#             138 MAKE_FUNCTION            0
#             140 LOAD_CONST              13 ('TestMaintenanceRun')
#             142 CALL                     2
#             150 STORE_NAME              14 (TestMaintenanceRun)
#             152 RETURN_CONST             2 (None)
# 
# Disassembly of <code object TestMaintenanceValidation at 0x73cd945fedb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 7>:
#   7           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestMaintenanceValidation')
#               8 STORE_NAME               2 (__qualname__)
# 
#   8          10 LOAD_CONST               1 (<code object test_validate_missing_model at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 8>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_validate_missing_model)
# 
#  13          16 LOAD_CONST               2 (<code object test_validate_missing_branch_id at 0x3af90d20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 13>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_validate_missing_branch_id)
# 
#  18          22 LOAD_CONST               3 (<code object test_validate_valid_config at 0x3af0c6d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 18>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_validate_valid_config)
#              28 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_validate_missing_model at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 8>:
#   8           0 RESUME                   0
# 
#   9           2 LOAD_GLOBAL              1 (NULL + MaintenanceSecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  10          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + validate)
#              44 LOAD_CONST               1 ('maintenance')
#              46 LOAD_CONST               2 ('branch_id')
#              48 LOAD_CONST               3 ('L1')
#              50 BUILD_MAP                1
#              52 BUILD_MAP                1
#              54 CALL                     1
#              62 UNPACK_SEQUENCE          2
#              66 STORE_FAST               2 (valid)
#              68 STORE_FAST               3 (errors)
# 
#  11          70 LOAD_CONST               4 (False)
#              72 STORE_FAST               4 (@py_assert2)
#              74 LOAD_FAST                2 (valid)
#              76 LOAD_FAST                4 (@py_assert2)
#              78 IS_OP                    0
#              80 STORE_FAST               5 (@py_assert1)
#              82 LOAD_FAST                5 (@py_assert1)
#              84 POP_JUMP_IF_TRUE       153 (to 392)
#              86 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              96 LOAD_ATTR                6 (_call_reprcompare)
#             116 LOAD_CONST               5 (('is',))
#             118 LOAD_FAST                5 (@py_assert1)
#             120 BUILD_TUPLE              1
#             122 LOAD_CONST               6 (('%(py0)s is %(py3)s',))
#             124 LOAD_FAST                2 (valid)
#             126 LOAD_FAST                4 (@py_assert2)
#             128 BUILD_TUPLE              2
#             130 CALL                     4
#             138 LOAD_CONST               7 ('valid')
#             140 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             150 LOAD_ATTR               10 (locals)
#             170 CALL                     0
#             178 CONTAINS_OP              0
#             180 POP_JUMP_IF_TRUE        21 (to 224)
#             182 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             192 LOAD_ATTR               12 (_should_repr_global_name)
#             212 LOAD_FAST                2 (valid)
#             214 CALL                     1
#             222 POP_JUMP_IF_FALSE       21 (to 266)
#         >>  224 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             234 LOAD_ATTR               14 (_saferepr)
#             254 LOAD_FAST                2 (valid)
#             256 CALL                     1
#             264 JUMP_FORWARD             1 (to 268)
#         >>  266 LOAD_CONST               7 ('valid')
#         >>  268 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             278 LOAD_ATTR               14 (_saferepr)
#             298 LOAD_FAST                4 (@py_assert2)
#             300 CALL                     1
#             308 LOAD_CONST               8 (('py0', 'py3'))
#             310 BUILD_CONST_KEY_MAP      2
#             312 BINARY_OP                6 (%)
#             316 STORE_FAST               6 (@py_format4)
#             318 LOAD_CONST               9 ('assert %(py5)s')
#             320 LOAD_CONST              10 ('py5')
#             322 LOAD_FAST                6 (@py_format4)
#             324 BUILD_MAP                1
#             326 BINARY_OP                6 (%)
#             330 STORE_FAST               7 (@py_format6)
#             332 LOAD_GLOBAL             17 (NULL + AssertionError)
#             342 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             352 LOAD_ATTR               18 (_format_explanation)
#             372 LOAD_FAST                7 (@py_format6)
#             374 CALL                     1
#             382 CALL                     1
#             390 RAISE_VARARGS            1
#         >>  392 LOAD_CONST               0 (None)
#             394 COPY                     1
#             396 STORE_FAST               5 (@py_assert1)
#             398 STORE_FAST               4 (@py_assert2)
#             400 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_missing_branch_id at 0x3af90d20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 13>:
#  13           0 RESUME                   0
# 
#  14           2 LOAD_GLOBAL              1 (NULL + MaintenanceSecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  15          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + validate)
#              44 LOAD_CONST               1 ('model')
#              46 LOAD_CONST               2 ('rid')
#              48 LOAD_CONST               3 ('test')
#              50 BUILD_MAP                1
#              52 BUILD_MAP                1
#              54 CALL                     1
#              62 UNPACK_SEQUENCE          2
#              66 STORE_FAST               2 (valid)
#              68 STORE_FAST               3 (errors)
# 
#  16          70 LOAD_CONST               4 (False)
#              72 STORE_FAST               4 (@py_assert2)
#              74 LOAD_FAST                2 (valid)
#              76 LOAD_FAST                4 (@py_assert2)
#              78 IS_OP                    0
#              80 STORE_FAST               5 (@py_assert1)
#              82 LOAD_FAST                5 (@py_assert1)
#              84 POP_JUMP_IF_TRUE       153 (to 392)
#              86 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              96 LOAD_ATTR                6 (_call_reprcompare)
#             116 LOAD_CONST               5 (('is',))
#             118 LOAD_FAST                5 (@py_assert1)
#             120 BUILD_TUPLE              1
#             122 LOAD_CONST               6 (('%(py0)s is %(py3)s',))
#             124 LOAD_FAST                2 (valid)
#             126 LOAD_FAST                4 (@py_assert2)
#             128 BUILD_TUPLE              2
#             130 CALL                     4
#             138 LOAD_CONST               7 ('valid')
#             140 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             150 LOAD_ATTR               10 (locals)
#             170 CALL                     0
#             178 CONTAINS_OP              0
#             180 POP_JUMP_IF_TRUE        21 (to 224)
#             182 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             192 LOAD_ATTR               12 (_should_repr_global_name)
#             212 LOAD_FAST                2 (valid)
#             214 CALL                     1
#             222 POP_JUMP_IF_FALSE       21 (to 266)
#         >>  224 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             234 LOAD_ATTR               14 (_saferepr)
#             254 LOAD_FAST                2 (valid)
#             256 CALL                     1
#             264 JUMP_FORWARD             1 (to 268)
#         >>  266 LOAD_CONST               7 ('valid')
#         >>  268 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             278 LOAD_ATTR               14 (_saferepr)
#             298 LOAD_FAST                4 (@py_assert2)
#             300 CALL                     1
#             308 LOAD_CONST               8 (('py0', 'py3'))
#             310 BUILD_CONST_KEY_MAP      2
#             312 BINARY_OP                6 (%)
#             316 STORE_FAST               6 (@py_format4)
#             318 LOAD_CONST               9 ('assert %(py5)s')
#             320 LOAD_CONST              10 ('py5')
#             322 LOAD_FAST                6 (@py_format4)
#             324 BUILD_MAP                1
#             326 BINARY_OP                6 (%)
#             330 STORE_FAST               7 (@py_format6)
#             332 LOAD_GLOBAL             17 (NULL + AssertionError)
#             342 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             352 LOAD_ATTR               18 (_format_explanation)
#             372 LOAD_FAST                7 (@py_format6)
#             374 CALL                     1
#             382 CALL                     1
#             390 RAISE_VARARGS            1
#         >>  392 LOAD_CONST               0 (None)
#             394 COPY                     1
#             396 STORE_FAST               5 (@py_assert1)
#             398 STORE_FAST               4 (@py_assert2)
#             400 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_valid_config at 0x3af0c6d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 18>:
#  18           0 RESUME                   0
# 
#  19           2 LOAD_GLOBAL              1 (NULL + MaintenanceSecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  20          22 LOAD_CONST               1 ('rid')
#              24 LOAD_CONST               2 ('test')
#              26 BUILD_MAP                1
#              28 LOAD_CONST               3 ('branch_id')
#              30 LOAD_CONST               4 ('L1')
#              32 BUILD_MAP                1
#              34 LOAD_CONST               5 (('model', 'maintenance'))
#              36 BUILD_CONST_KEY_MAP      2
#              38 STORE_FAST               2 (config)
# 
#  21          40 LOAD_FAST                1 (skill)
#              42 LOAD_ATTR                3 (NULL|self + validate)
#              62 LOAD_FAST                2 (config)
#              64 CALL                     1
#              72 UNPACK_SEQUENCE          2
#              76 STORE_FAST               3 (valid)
#              78 STORE_FAST               4 (errors)
# 
#  22          80 LOAD_CONST               6 (True)
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
# Disassembly of <code object TestMaintenanceSeverity at 0x73cd93b06970, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 25>:
#  25           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestMaintenanceSeverity')
#               8 STORE_NAME               2 (__qualname__)
# 
#  26          10 LOAD_CONST               1 (<code object test_classify_severity_critical at 0x3afa4f50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 26>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_classify_severity_critical)
# 
#  30          16 LOAD_CONST               2 (<code object test_classify_severity_warning at 0x3af9ce50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 30>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_classify_severity_warning)
# 
#  34          22 LOAD_CONST               3 (<code object test_classify_severity_normal at 0x3aee3ab0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 34>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_classify_severity_normal)
# 
#  38          28 LOAD_CONST               4 (<code object test_classify_severity_overload_critical at 0x3af909c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 38>)
#              30 MAKE_FUNCTION            0
#              32 STORE_NAME               6 (test_classify_severity_overload_critical)
# 
#  42          34 LOAD_CONST               5 (<code object test_classify_severity_overload_warning at 0x3aefddd0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 42>)
#              36 MAKE_FUNCTION            0
#              38 STORE_NAME               7 (test_classify_severity_overload_warning)
#              40 RETURN_CONST             6 (None)
# 
# Disassembly of <code object test_classify_severity_critical at 0x3afa4f50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 26>:
#  26           0 RESUME                   0
# 
#  27           2 LOAD_GLOBAL              1 (NULL + MaintenanceSecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  28          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                2 (_classify_severity)
#              44 STORE_FAST               2 (@py_assert1)
#              46 LOAD_CONST               1 (0.8)
#              48 STORE_FAST               3 (@py_assert3)
#              50 LOAD_CONST               2 (0.5)
#              52 STORE_FAST               4 (@py_assert5)
#              54 PUSH_NULL
#              56 LOAD_FAST                2 (@py_assert1)
#              58 LOAD_FAST                3 (@py_assert3)
#              60 LOAD_FAST                4 (@py_assert5)
#              62 KW_NAMES                 3 (('min_vm', 'max_loading'))
#              64 CALL                     2
#              72 STORE_FAST               5 (@py_assert7)
#              74 LOAD_CONST               4 ('critical')
#              76 STORE_FAST               6 (@py_assert10)
#              78 LOAD_FAST                5 (@py_assert7)
#              80 LOAD_FAST                6 (@py_assert10)
#              82 COMPARE_OP              40 (==)
#              86 STORE_FAST               7 (@py_assert9)
#              88 LOAD_FAST                7 (@py_assert9)
#              90 POP_JUMP_IF_TRUE       233 (to 558)
#              92 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             102 LOAD_ATTR                6 (_call_reprcompare)
#             122 LOAD_CONST               5 (('==',))
#             124 LOAD_FAST                7 (@py_assert9)
#             126 BUILD_TUPLE              1
#             128 LOAD_CONST               6 (('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s._classify_severity\n}(min_vm=%(py4)s, max_loading=%(py6)s)\n} == %(py11)s',))
#             130 LOAD_FAST                5 (@py_assert7)
#             132 LOAD_FAST                6 (@py_assert10)
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
#             304 LOAD_FAST                2 (@py_assert1)
#             306 CALL                     1
#             314 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             324 LOAD_ATTR               14 (_saferepr)
#             344 LOAD_FAST                3 (@py_assert3)
#             346 CALL                     1
#             354 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             364 LOAD_ATTR               14 (_saferepr)
#             384 LOAD_FAST                4 (@py_assert5)
#             386 CALL                     1
#             394 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             404 LOAD_ATTR               14 (_saferepr)
#             424 LOAD_FAST                5 (@py_assert7)
#             426 CALL                     1
#             434 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             444 LOAD_ATTR               14 (_saferepr)
#             464 LOAD_FAST                6 (@py_assert10)
#             466 CALL                     1
#             474 LOAD_CONST               8 (('py0', 'py2', 'py4', 'py6', 'py8', 'py11'))
#             476 BUILD_CONST_KEY_MAP      6
#             478 BINARY_OP                6 (%)
#             482 STORE_FAST               8 (@py_format12)
#             484 LOAD_CONST               9 ('assert %(py13)s')
#             486 LOAD_CONST              10 ('py13')
#             488 LOAD_FAST                8 (@py_format12)
#             490 BUILD_MAP                1
#             492 BINARY_OP                6 (%)
#             496 STORE_FAST               9 (@py_format14)
#             498 LOAD_GLOBAL             17 (NULL + AssertionError)
#             508 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             518 LOAD_ATTR               18 (_format_explanation)
#             538 LOAD_FAST                9 (@py_format14)
#             540 CALL                     1
#             548 CALL                     1
#             556 RAISE_VARARGS            1
#         >>  558 LOAD_CONST               0 (None)
#             560 COPY                     1
#             562 STORE_FAST               2 (@py_assert1)
#             564 COPY                     1
#             566 STORE_FAST               3 (@py_assert3)
#             568 COPY                     1
#             570 STORE_FAST               4 (@py_assert5)
#             572 COPY                     1
#             574 STORE_FAST               5 (@py_assert7)
#             576 COPY                     1
#             578 STORE_FAST               7 (@py_assert9)
#             580 STORE_FAST               6 (@py_assert10)
#             582 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_classify_severity_warning at 0x3af9ce50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 30>:
#  30           0 RESUME                   0
# 
#  31           2 LOAD_GLOBAL              1 (NULL + MaintenanceSecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  32          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                2 (_classify_severity)
#              44 STORE_FAST               2 (@py_assert1)
#              46 LOAD_CONST               1 (0.87)
#              48 STORE_FAST               3 (@py_assert3)
#              50 LOAD_CONST               2 (0.5)
#              52 STORE_FAST               4 (@py_assert5)
#              54 PUSH_NULL
#              56 LOAD_FAST                2 (@py_assert1)
#              58 LOAD_FAST                3 (@py_assert3)
#              60 LOAD_FAST                4 (@py_assert5)
#              62 KW_NAMES                 3 (('min_vm', 'max_loading'))
#              64 CALL                     2
#              72 STORE_FAST               5 (@py_assert7)
#              74 LOAD_CONST               4 ('warning')
#              76 STORE_FAST               6 (@py_assert10)
#              78 LOAD_FAST                5 (@py_assert7)
#              80 LOAD_FAST                6 (@py_assert10)
#              82 COMPARE_OP              40 (==)
#              86 STORE_FAST               7 (@py_assert9)
#              88 LOAD_FAST                7 (@py_assert9)
#              90 POP_JUMP_IF_TRUE       233 (to 558)
#              92 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             102 LOAD_ATTR                6 (_call_reprcompare)
#             122 LOAD_CONST               5 (('==',))
#             124 LOAD_FAST                7 (@py_assert9)
#             126 BUILD_TUPLE              1
#             128 LOAD_CONST               6 (('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s._classify_severity\n}(min_vm=%(py4)s, max_loading=%(py6)s)\n} == %(py11)s',))
#             130 LOAD_FAST                5 (@py_assert7)
#             132 LOAD_FAST                6 (@py_assert10)
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
#             304 LOAD_FAST                2 (@py_assert1)
#             306 CALL                     1
#             314 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             324 LOAD_ATTR               14 (_saferepr)
#             344 LOAD_FAST                3 (@py_assert3)
#             346 CALL                     1
#             354 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             364 LOAD_ATTR               14 (_saferepr)
#             384 LOAD_FAST                4 (@py_assert5)
#             386 CALL                     1
#             394 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             404 LOAD_ATTR               14 (_saferepr)
#             424 LOAD_FAST                5 (@py_assert7)
#             426 CALL                     1
#             434 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             444 LOAD_ATTR               14 (_saferepr)
#             464 LOAD_FAST                6 (@py_assert10)
#             466 CALL                     1
#             474 LOAD_CONST               8 (('py0', 'py2', 'py4', 'py6', 'py8', 'py11'))
#             476 BUILD_CONST_KEY_MAP      6
#             478 BINARY_OP                6 (%)
#             482 STORE_FAST               8 (@py_format12)
#             484 LOAD_CONST               9 ('assert %(py13)s')
#             486 LOAD_CONST              10 ('py13')
#             488 LOAD_FAST                8 (@py_format12)
#             490 BUILD_MAP                1
#             492 BINARY_OP                6 (%)
#             496 STORE_FAST               9 (@py_format14)
#             498 LOAD_GLOBAL             17 (NULL + AssertionError)
#             508 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             518 LOAD_ATTR               18 (_format_explanation)
#             538 LOAD_FAST                9 (@py_format14)
#             540 CALL                     1
#             548 CALL                     1
#             556 RAISE_VARARGS            1
#         >>  558 LOAD_CONST               0 (None)
#             560 COPY                     1
#             562 STORE_FAST               2 (@py_assert1)
#             564 COPY                     1
#             566 STORE_FAST               3 (@py_assert3)
#             568 COPY                     1
#             570 STORE_FAST               4 (@py_assert5)
#             572 COPY                     1
#             574 STORE_FAST               5 (@py_assert7)
#             576 COPY                     1
#             578 STORE_FAST               7 (@py_assert9)
#             580 STORE_FAST               6 (@py_assert10)
#             582 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_classify_severity_normal at 0x3aee3ab0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 34>:
#  34           0 RESUME                   0
# 
#  35           2 LOAD_GLOBAL              1 (NULL + MaintenanceSecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  36          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                2 (_classify_severity)
#              44 STORE_FAST               2 (@py_assert1)
#              46 LOAD_CONST               1 (0.95)
#              48 STORE_FAST               3 (@py_assert3)
#              50 LOAD_CONST               2 (0.8)
#              52 STORE_FAST               4 (@py_assert5)
#              54 PUSH_NULL
#              56 LOAD_FAST                2 (@py_assert1)
#              58 LOAD_FAST                3 (@py_assert3)
#              60 LOAD_FAST                4 (@py_assert5)
#              62 KW_NAMES                 3 (('min_vm', 'max_loading'))
#              64 CALL                     2
#              72 STORE_FAST               5 (@py_assert7)
#              74 LOAD_CONST               4 ('normal')
#              76 STORE_FAST               6 (@py_assert10)
#              78 LOAD_FAST                5 (@py_assert7)
#              80 LOAD_FAST                6 (@py_assert10)
#              82 COMPARE_OP              40 (==)
#              86 STORE_FAST               7 (@py_assert9)
#              88 LOAD_FAST                7 (@py_assert9)
#              90 POP_JUMP_IF_TRUE       233 (to 558)
#              92 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             102 LOAD_ATTR                6 (_call_reprcompare)
#             122 LOAD_CONST               5 (('==',))
#             124 LOAD_FAST                7 (@py_assert9)
#             126 BUILD_TUPLE              1
#             128 LOAD_CONST               6 (('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s._classify_severity\n}(min_vm=%(py4)s, max_loading=%(py6)s)\n} == %(py11)s',))
#             130 LOAD_FAST                5 (@py_assert7)
#             132 LOAD_FAST                6 (@py_assert10)
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
#             304 LOAD_FAST                2 (@py_assert1)
#             306 CALL                     1
#             314 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             324 LOAD_ATTR               14 (_saferepr)
#             344 LOAD_FAST                3 (@py_assert3)
#             346 CALL                     1
#             354 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             364 LOAD_ATTR               14 (_saferepr)
#             384 LOAD_FAST                4 (@py_assert5)
#             386 CALL                     1
#             394 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             404 LOAD_ATTR               14 (_saferepr)
#             424 LOAD_FAST                5 (@py_assert7)
#             426 CALL                     1
#             434 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             444 LOAD_ATTR               14 (_saferepr)
#             464 LOAD_FAST                6 (@py_assert10)
#             466 CALL                     1
#             474 LOAD_CONST               8 (('py0', 'py2', 'py4', 'py6', 'py8', 'py11'))
#             476 BUILD_CONST_KEY_MAP      6
#             478 BINARY_OP                6 (%)
#             482 STORE_FAST               8 (@py_format12)
#             484 LOAD_CONST               9 ('assert %(py13)s')
#             486 LOAD_CONST              10 ('py13')
#             488 LOAD_FAST                8 (@py_format12)
#             490 BUILD_MAP                1
#             492 BINARY_OP                6 (%)
#             496 STORE_FAST               9 (@py_format14)
#             498 LOAD_GLOBAL             17 (NULL + AssertionError)
#             508 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             518 LOAD_ATTR               18 (_format_explanation)
#             538 LOAD_FAST                9 (@py_format14)
#             540 CALL                     1
#             548 CALL                     1
#             556 RAISE_VARARGS            1
#         >>  558 LOAD_CONST               0 (None)
#             560 COPY                     1
#             562 STORE_FAST               2 (@py_assert1)
#             564 COPY                     1
#             566 STORE_FAST               3 (@py_assert3)
#             568 COPY                     1
#             570 STORE_FAST               4 (@py_assert5)
#             572 COPY                     1
#             574 STORE_FAST               5 (@py_assert7)
#             576 COPY                     1
#             578 STORE_FAST               7 (@py_assert9)
#             580 STORE_FAST               6 (@py_assert10)
#             582 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_classify_severity_overload_critical at 0x3af909c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 38>:
#  38           0 RESUME                   0
# 
#  39           2 LOAD_GLOBAL              1 (NULL + MaintenanceSecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  40          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                2 (_classify_severity)
#              44 STORE_FAST               2 (@py_assert1)
#              46 LOAD_CONST               1 (1.0)
#              48 STORE_FAST               3 (@py_assert3)
#              50 LOAD_CONST               2 (1.3)
#              52 STORE_FAST               4 (@py_assert5)
#              54 PUSH_NULL
#              56 LOAD_FAST                2 (@py_assert1)
#              58 LOAD_FAST                3 (@py_assert3)
#              60 LOAD_FAST                4 (@py_assert5)
#              62 KW_NAMES                 3 (('min_vm', 'max_loading'))
#              64 CALL                     2
#              72 STORE_FAST               5 (@py_assert7)
#              74 LOAD_CONST               4 ('critical')
#              76 STORE_FAST               6 (@py_assert10)
#              78 LOAD_FAST                5 (@py_assert7)
#              80 LOAD_FAST                6 (@py_assert10)
#              82 COMPARE_OP              40 (==)
#              86 STORE_FAST               7 (@py_assert9)
#              88 LOAD_FAST                7 (@py_assert9)
#              90 POP_JUMP_IF_TRUE       233 (to 558)
#              92 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             102 LOAD_ATTR                6 (_call_reprcompare)
#             122 LOAD_CONST               5 (('==',))
#             124 LOAD_FAST                7 (@py_assert9)
#             126 BUILD_TUPLE              1
#             128 LOAD_CONST               6 (('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s._classify_severity\n}(min_vm=%(py4)s, max_loading=%(py6)s)\n} == %(py11)s',))
#             130 LOAD_FAST                5 (@py_assert7)
#             132 LOAD_FAST                6 (@py_assert10)
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
#             304 LOAD_FAST                2 (@py_assert1)
#             306 CALL                     1
#             314 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             324 LOAD_ATTR               14 (_saferepr)
#             344 LOAD_FAST                3 (@py_assert3)
#             346 CALL                     1
#             354 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             364 LOAD_ATTR               14 (_saferepr)
#             384 LOAD_FAST                4 (@py_assert5)
#             386 CALL                     1
#             394 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             404 LOAD_ATTR               14 (_saferepr)
#             424 LOAD_FAST                5 (@py_assert7)
#             426 CALL                     1
#             434 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             444 LOAD_ATTR               14 (_saferepr)
#             464 LOAD_FAST                6 (@py_assert10)
#             466 CALL                     1
#             474 LOAD_CONST               8 (('py0', 'py2', 'py4', 'py6', 'py8', 'py11'))
#             476 BUILD_CONST_KEY_MAP      6
#             478 BINARY_OP                6 (%)
#             482 STORE_FAST               8 (@py_format12)
#             484 LOAD_CONST               9 ('assert %(py13)s')
#             486 LOAD_CONST              10 ('py13')
#             488 LOAD_FAST                8 (@py_format12)
#             490 BUILD_MAP                1
#             492 BINARY_OP                6 (%)
#             496 STORE_FAST               9 (@py_format14)
#             498 LOAD_GLOBAL             17 (NULL + AssertionError)
#             508 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             518 LOAD_ATTR               18 (_format_explanation)
#             538 LOAD_FAST                9 (@py_format14)
#             540 CALL                     1
#             548 CALL                     1
#             556 RAISE_VARARGS            1
#         >>  558 LOAD_CONST               0 (None)
#             560 COPY                     1
#             562 STORE_FAST               2 (@py_assert1)
#             564 COPY                     1
#             566 STORE_FAST               3 (@py_assert3)
#             568 COPY                     1
#             570 STORE_FAST               4 (@py_assert5)
#             572 COPY                     1
#             574 STORE_FAST               5 (@py_assert7)
#             576 COPY                     1
#             578 STORE_FAST               7 (@py_assert9)
#             580 STORE_FAST               6 (@py_assert10)
#             582 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_classify_severity_overload_warning at 0x3aefddd0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 42>:
#  42           0 RESUME                   0
# 
#  43           2 LOAD_GLOBAL              1 (NULL + MaintenanceSecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  44          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                2 (_classify_severity)
#              44 STORE_FAST               2 (@py_assert1)
#              46 LOAD_CONST               1 (1.0)
#              48 STORE_FAST               3 (@py_assert3)
#              50 LOAD_CONST               2 (1.05)
#              52 STORE_FAST               4 (@py_assert5)
#              54 PUSH_NULL
#              56 LOAD_FAST                2 (@py_assert1)
#              58 LOAD_FAST                3 (@py_assert3)
#              60 LOAD_FAST                4 (@py_assert5)
#              62 KW_NAMES                 3 (('min_vm', 'max_loading'))
#              64 CALL                     2
#              72 STORE_FAST               5 (@py_assert7)
#              74 LOAD_CONST               4 ('warning')
#              76 STORE_FAST               6 (@py_assert10)
#              78 LOAD_FAST                5 (@py_assert7)
#              80 LOAD_FAST                6 (@py_assert10)
#              82 COMPARE_OP              40 (==)
#              86 STORE_FAST               7 (@py_assert9)
#              88 LOAD_FAST                7 (@py_assert9)
#              90 POP_JUMP_IF_TRUE       233 (to 558)
#              92 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             102 LOAD_ATTR                6 (_call_reprcompare)
#             122 LOAD_CONST               5 (('==',))
#             124 LOAD_FAST                7 (@py_assert9)
#             126 BUILD_TUPLE              1
#             128 LOAD_CONST               6 (('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s._classify_severity\n}(min_vm=%(py4)s, max_loading=%(py6)s)\n} == %(py11)s',))
#             130 LOAD_FAST                5 (@py_assert7)
#             132 LOAD_FAST                6 (@py_assert10)
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
#             304 LOAD_FAST                2 (@py_assert1)
#             306 CALL                     1
#             314 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             324 LOAD_ATTR               14 (_saferepr)
#             344 LOAD_FAST                3 (@py_assert3)
#             346 CALL                     1
#             354 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             364 LOAD_ATTR               14 (_saferepr)
#             384 LOAD_FAST                4 (@py_assert5)
#             386 CALL                     1
#             394 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             404 LOAD_ATTR               14 (_saferepr)
#             424 LOAD_FAST                5 (@py_assert7)
#             426 CALL                     1
#             434 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             444 LOAD_ATTR               14 (_saferepr)
#             464 LOAD_FAST                6 (@py_assert10)
#             466 CALL                     1
#             474 LOAD_CONST               8 (('py0', 'py2', 'py4', 'py6', 'py8', 'py11'))
#             476 BUILD_CONST_KEY_MAP      6
#             478 BINARY_OP                6 (%)
#             482 STORE_FAST               8 (@py_format12)
#             484 LOAD_CONST               9 ('assert %(py13)s')
#             486 LOAD_CONST              10 ('py13')
#             488 LOAD_FAST                8 (@py_format12)
#             490 BUILD_MAP                1
#             492 BINARY_OP                6 (%)
#             496 STORE_FAST               9 (@py_format14)
#             498 LOAD_GLOBAL             17 (NULL + AssertionError)
#             508 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             518 LOAD_ATTR               18 (_format_explanation)
#             538 LOAD_FAST                9 (@py_format14)
#             540 CALL                     1
#             548 CALL                     1
#             556 RAISE_VARARGS            1
#         >>  558 LOAD_CONST               0 (None)
#             560 COPY                     1
#             562 STORE_FAST               2 (@py_assert1)
#             564 COPY                     1
#             566 STORE_FAST               3 (@py_assert3)
#             568 COPY                     1
#             570 STORE_FAST               4 (@py_assert5)
#             572 COPY                     1
#             574 STORE_FAST               5 (@py_assert7)
#             576 COPY                     1
#             578 STORE_FAST               7 (@py_assert9)
#             580 STORE_FAST               6 (@py_assert10)
#             582 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestMaintenancePower at 0x73cd93b065b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 47>:
#  47           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestMaintenancePower')
#               8 STORE_NAME               2 (__qualname__)
# 
#  48          10 LOAD_CONST               1 (<code object test_compute_apparent_power at 0x3afa13e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 48>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_compute_apparent_power)
# 
#  53          16 LOAD_CONST               2 (<code object test_compute_branch_loading at 0x3aec4850, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 53>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_compute_branch_loading)
# 
#  58          22 LOAD_CONST               3 (<code object test_compute_branch_loading_zero_rating at 0x3ae632d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 58>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_compute_branch_loading_zero_rating)
# 
#  63          28 LOAD_CONST               4 (<code object test_compute_rating_from_irated at 0x3af9f150, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 63>)
#              30 MAKE_FUNCTION            0
#              32 STORE_NAME               6 (test_compute_rating_from_irated)
#              34 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_compute_apparent_power at 0x3afa13e0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 48>:
#  48           0 RESUME                   0
# 
#  49           2 LOAD_GLOBAL              1 (NULL + MaintenanceSecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  50          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _compute_apparent_power)
#              44 LOAD_CONST               1 (3.0)
#              46 LOAD_CONST               2 (4.0)
#              48 KW_NAMES                 3 (('p', 'q'))
#              50 CALL                     2
#              58 STORE_FAST               2 (s)
# 
#  51          60 LOAD_CONST               4 (5.0)
#              62 STORE_FAST               3 (@py_assert2)
#              64 LOAD_FAST                2 (s)
#              66 LOAD_FAST                3 (@py_assert2)
#              68 BINARY_OP               10 (-)
#              72 STORE_FAST               4 (@py_assert4)
#              74 LOAD_GLOBAL              5 (NULL + abs)
#              84 LOAD_FAST                4 (@py_assert4)
#              86 CALL                     1
#              94 STORE_FAST               5 (@py_assert5)
#              96 LOAD_CONST               5 (1e-10)
#              98 STORE_FAST               6 (@py_assert8)
#             100 LOAD_FAST                5 (@py_assert5)
#             102 LOAD_FAST                6 (@py_assert8)
#             104 COMPARE_OP               2 (<)
#             108 STORE_FAST               7 (@py_assert7)
#             110 LOAD_FAST                7 (@py_assert7)
#             112 EXTENDED_ARG             1
#             114 POP_JUMP_IF_TRUE       266 (to 648)
#             116 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             126 LOAD_ATTR                8 (_call_reprcompare)
#             146 LOAD_CONST               6 (('<',))
#             148 LOAD_FAST                7 (@py_assert7)
#             150 BUILD_TUPLE              1
#             152 LOAD_CONST               7 (('%(py6)s\n{%(py6)s = %(py0)s((%(py1)s - %(py3)s))\n} < %(py9)s',))
#             154 LOAD_FAST                5 (@py_assert5)
#             156 LOAD_FAST                6 (@py_assert8)
#             158 BUILD_TUPLE              2
#             160 CALL                     4
#             168 LOAD_CONST               8 ('abs')
#             170 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             180 LOAD_ATTR               12 (locals)
#             200 CALL                     0
#             208 CONTAINS_OP              0
#             210 POP_JUMP_IF_TRUE        25 (to 262)
#             212 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             222 LOAD_ATTR               14 (_should_repr_global_name)
#             242 LOAD_GLOBAL              4 (abs)
#             252 CALL                     1
#             260 POP_JUMP_IF_FALSE       25 (to 312)
#         >>  262 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             272 LOAD_ATTR               16 (_saferepr)
#             292 LOAD_GLOBAL              4 (abs)
#             302 CALL                     1
#             310 JUMP_FORWARD             1 (to 314)
#         >>  312 LOAD_CONST               8 ('abs')
#         >>  314 LOAD_CONST               9 ('s')
#             316 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             326 LOAD_ATTR               12 (locals)
#             346 CALL                     0
#             354 CONTAINS_OP              0
#             356 POP_JUMP_IF_TRUE        21 (to 400)
#             358 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             368 LOAD_ATTR               14 (_should_repr_global_name)
#             388 LOAD_FAST                2 (s)
#             390 CALL                     1
#             398 POP_JUMP_IF_FALSE       21 (to 442)
#         >>  400 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             410 LOAD_ATTR               16 (_saferepr)
#             430 LOAD_FAST                2 (s)
#             432 CALL                     1
#             440 JUMP_FORWARD             1 (to 444)
#         >>  442 LOAD_CONST               9 ('s')
#         >>  444 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             454 LOAD_ATTR               16 (_saferepr)
#             474 LOAD_FAST                3 (@py_assert2)
#             476 CALL                     1
#             484 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             494 LOAD_ATTR               16 (_saferepr)
#             514 LOAD_FAST                5 (@py_assert5)
#             516 CALL                     1
#             524 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             534 LOAD_ATTR               16 (_saferepr)
#             554 LOAD_FAST                6 (@py_assert8)
#             556 CALL                     1
#             564 LOAD_CONST              10 (('py0', 'py1', 'py3', 'py6', 'py9'))
#             566 BUILD_CONST_KEY_MAP      5
#             568 BINARY_OP                6 (%)
#             572 STORE_FAST               8 (@py_format10)
#             574 LOAD_CONST              11 ('assert %(py11)s')
#             576 LOAD_CONST              12 ('py11')
#             578 LOAD_FAST                8 (@py_format10)
#             580 BUILD_MAP                1
#             582 BINARY_OP                6 (%)
#             586 STORE_FAST               9 (@py_format12)
#             588 LOAD_GLOBAL             19 (NULL + AssertionError)
#             598 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             608 LOAD_ATTR               20 (_format_explanation)
#             628 LOAD_FAST                9 (@py_format12)
#             630 CALL                     1
#             638 CALL                     1
#             646 RAISE_VARARGS            1
#         >>  648 LOAD_CONST               0 (None)
#             650 COPY                     1
#             652 STORE_FAST               3 (@py_assert2)
#             654 COPY                     1
#             656 STORE_FAST               4 (@py_assert4)
#             658 COPY                     1
#             660 STORE_FAST               5 (@py_assert5)
#             662 COPY                     1
#             664 STORE_FAST               7 (@py_assert7)
#             666 STORE_FAST               6 (@py_assert8)
#             668 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_compute_branch_loading at 0x3aec4850, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 53>:
#  53           0 RESUME                   0
# 
#  54           2 LOAD_GLOBAL              1 (NULL + MaintenanceSecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  55          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _compute_branch_loading)
#              44 LOAD_CONST               1 (50.0)
#              46 LOAD_CONST               2 (100.0)
#              48 KW_NAMES                 3 (('apparent_mva', 'rating_mva'))
#              50 CALL                     2
#              58 STORE_FAST               2 (loading)
# 
#  56          60 LOAD_CONST               4 (0.5)
#              62 STORE_FAST               3 (@py_assert2)
#              64 LOAD_FAST                2 (loading)
#              66 LOAD_FAST                3 (@py_assert2)
#              68 BINARY_OP               10 (-)
#              72 STORE_FAST               4 (@py_assert4)
#              74 LOAD_GLOBAL              5 (NULL + abs)
#              84 LOAD_FAST                4 (@py_assert4)
#              86 CALL                     1
#              94 STORE_FAST               5 (@py_assert5)
#              96 LOAD_CONST               5 (1e-10)
#              98 STORE_FAST               6 (@py_assert8)
#             100 LOAD_FAST                5 (@py_assert5)
#             102 LOAD_FAST                6 (@py_assert8)
#             104 COMPARE_OP               2 (<)
#             108 STORE_FAST               7 (@py_assert7)
#             110 LOAD_FAST                7 (@py_assert7)
#             112 EXTENDED_ARG             1
#             114 POP_JUMP_IF_TRUE       266 (to 648)
#             116 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             126 LOAD_ATTR                8 (_call_reprcompare)
#             146 LOAD_CONST               6 (('<',))
#             148 LOAD_FAST                7 (@py_assert7)
#             150 BUILD_TUPLE              1
#             152 LOAD_CONST               7 (('%(py6)s\n{%(py6)s = %(py0)s((%(py1)s - %(py3)s))\n} < %(py9)s',))
#             154 LOAD_FAST                5 (@py_assert5)
#             156 LOAD_FAST                6 (@py_assert8)
#             158 BUILD_TUPLE              2
#             160 CALL                     4
#             168 LOAD_CONST               8 ('abs')
#             170 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             180 LOAD_ATTR               12 (locals)
#             200 CALL                     0
#             208 CONTAINS_OP              0
#             210 POP_JUMP_IF_TRUE        25 (to 262)
#             212 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             222 LOAD_ATTR               14 (_should_repr_global_name)
#             242 LOAD_GLOBAL              4 (abs)
#             252 CALL                     1
#             260 POP_JUMP_IF_FALSE       25 (to 312)
#         >>  262 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             272 LOAD_ATTR               16 (_saferepr)
#             292 LOAD_GLOBAL              4 (abs)
#             302 CALL                     1
#             310 JUMP_FORWARD             1 (to 314)
#         >>  312 LOAD_CONST               8 ('abs')
#         >>  314 LOAD_CONST               9 ('loading')
#             316 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             326 LOAD_ATTR               12 (locals)
#             346 CALL                     0
#             354 CONTAINS_OP              0
#             356 POP_JUMP_IF_TRUE        21 (to 400)
#             358 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             368 LOAD_ATTR               14 (_should_repr_global_name)
#             388 LOAD_FAST                2 (loading)
#             390 CALL                     1
#             398 POP_JUMP_IF_FALSE       21 (to 442)
#         >>  400 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             410 LOAD_ATTR               16 (_saferepr)
#             430 LOAD_FAST                2 (loading)
#             432 CALL                     1
#             440 JUMP_FORWARD             1 (to 444)
#         >>  442 LOAD_CONST               9 ('loading')
#         >>  444 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             454 LOAD_ATTR               16 (_saferepr)
#             474 LOAD_FAST                3 (@py_assert2)
#             476 CALL                     1
#             484 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             494 LOAD_ATTR               16 (_saferepr)
#             514 LOAD_FAST                5 (@py_assert5)
#             516 CALL                     1
#             524 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             534 LOAD_ATTR               16 (_saferepr)
#             554 LOAD_FAST                6 (@py_assert8)
#             556 CALL                     1
#             564 LOAD_CONST              10 (('py0', 'py1', 'py3', 'py6', 'py9'))
#             566 BUILD_CONST_KEY_MAP      5
#             568 BINARY_OP                6 (%)
#             572 STORE_FAST               8 (@py_format10)
#             574 LOAD_CONST              11 ('assert %(py11)s')
#             576 LOAD_CONST              12 ('py11')
#             578 LOAD_FAST                8 (@py_format10)
#             580 BUILD_MAP                1
#             582 BINARY_OP                6 (%)
#             586 STORE_FAST               9 (@py_format12)
#             588 LOAD_GLOBAL             19 (NULL + AssertionError)
#             598 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             608 LOAD_ATTR               20 (_format_explanation)
#             628 LOAD_FAST                9 (@py_format12)
#             630 CALL                     1
#             638 CALL                     1
#             646 RAISE_VARARGS            1
#         >>  648 LOAD_CONST               0 (None)
#             650 COPY                     1
#             652 STORE_FAST               3 (@py_assert2)
#             654 COPY                     1
#             656 STORE_FAST               4 (@py_assert4)
#             658 COPY                     1
#             660 STORE_FAST               5 (@py_assert5)
#             662 COPY                     1
#             664 STORE_FAST               7 (@py_assert7)
#             666 STORE_FAST               6 (@py_assert8)
#             668 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_compute_branch_loading_zero_rating at 0x3ae632d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 58>:
#  58           0 RESUME                   0
# 
#  59           2 LOAD_GLOBAL              1 (NULL + MaintenanceSecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  60          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _compute_branch_loading)
#              44 LOAD_CONST               1 (50.0)
#              46 LOAD_CONST               2 (0.0)
#              48 KW_NAMES                 3 (('apparent_mva', 'rating_mva'))
#              50 CALL                     2
#              58 STORE_FAST               2 (loading)
# 
#  61          60 LOAD_CONST               2 (0.0)
#              62 STORE_FAST               3 (@py_assert2)
#              64 LOAD_FAST                2 (loading)
#              66 LOAD_FAST                3 (@py_assert2)
#              68 COMPARE_OP              40 (==)
#              72 STORE_FAST               4 (@py_assert1)
#              74 LOAD_FAST                4 (@py_assert1)
#              76 POP_JUMP_IF_TRUE       153 (to 384)
#              78 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              88 LOAD_ATTR                6 (_call_reprcompare)
#             108 LOAD_CONST               4 (('==',))
#             110 LOAD_FAST                4 (@py_assert1)
#             112 BUILD_TUPLE              1
#             114 LOAD_CONST               5 (('%(py0)s == %(py3)s',))
#             116 LOAD_FAST                2 (loading)
#             118 LOAD_FAST                3 (@py_assert2)
#             120 BUILD_TUPLE              2
#             122 CALL                     4
#             130 LOAD_CONST               6 ('loading')
#             132 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             142 LOAD_ATTR               10 (locals)
#             162 CALL                     0
#             170 CONTAINS_OP              0
#             172 POP_JUMP_IF_TRUE        21 (to 216)
#             174 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             184 LOAD_ATTR               12 (_should_repr_global_name)
#             204 LOAD_FAST                2 (loading)
#             206 CALL                     1
#             214 POP_JUMP_IF_FALSE       21 (to 258)
#         >>  216 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             226 LOAD_ATTR               14 (_saferepr)
#             246 LOAD_FAST                2 (loading)
#             248 CALL                     1
#             256 JUMP_FORWARD             1 (to 260)
#         >>  258 LOAD_CONST               6 ('loading')
#         >>  260 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             270 LOAD_ATTR               14 (_saferepr)
#             290 LOAD_FAST                3 (@py_assert2)
#             292 CALL                     1
#             300 LOAD_CONST               7 (('py0', 'py3'))
#             302 BUILD_CONST_KEY_MAP      2
#             304 BINARY_OP                6 (%)
#             308 STORE_FAST               5 (@py_format4)
#             310 LOAD_CONST               8 ('assert %(py5)s')
#             312 LOAD_CONST               9 ('py5')
#             314 LOAD_FAST                5 (@py_format4)
#             316 BUILD_MAP                1
#             318 BINARY_OP                6 (%)
#             322 STORE_FAST               6 (@py_format6)
#             324 LOAD_GLOBAL             17 (NULL + AssertionError)
#             334 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             344 LOAD_ATTR               18 (_format_explanation)
#             364 LOAD_FAST                6 (@py_format6)
#             366 CALL                     1
#             374 CALL                     1
#             382 RAISE_VARARGS            1
#         >>  384 LOAD_CONST               0 (None)
#             386 COPY                     1
#             388 STORE_FAST               4 (@py_assert1)
#             390 STORE_FAST               3 (@py_assert2)
#             392 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_compute_rating_from_irated at 0x3af9f150, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 63>:
#  63           0 RESUME                   0
# 
#  64           2 LOAD_GLOBAL              1 (NULL + MaintenanceSecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  65          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _compute_rating_from_irated)
#              44 LOAD_CONST               1 (1000.0)
#              46 LOAD_CONST               2 (220.0)
#              48 KW_NAMES                 3 (('i_rated', 'v_base'))
#              50 CALL                     2
#              58 STORE_FAST               2 (rating)
# 
#  66          60 LOAD_CONST               4 (381051.177665153)
#              62 STORE_FAST               3 (expected)
# 
#  67          64 LOAD_FAST                2 (rating)
#              66 LOAD_FAST                3 (expected)
#              68 BINARY_OP               10 (-)
#              72 STORE_FAST               4 (@py_assert3)
#              74 LOAD_GLOBAL              5 (NULL + abs)
#              84 LOAD_FAST                4 (@py_assert3)
#              86 CALL                     1
#              94 STORE_FAST               5 (@py_assert4)
#              96 LOAD_CONST               5 (1e-06)
#              98 STORE_FAST               6 (@py_assert7)
#             100 LOAD_FAST                5 (@py_assert4)
#             102 LOAD_FAST                6 (@py_assert7)
#             104 COMPARE_OP               2 (<)
#             108 STORE_FAST               7 (@py_assert6)
#             110 LOAD_FAST                7 (@py_assert6)
#             112 EXTENDED_ARG             1
#             114 POP_JUMP_IF_TRUE       311 (to 738)
#             116 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             126 LOAD_ATTR                8 (_call_reprcompare)
#             146 LOAD_CONST               6 (('<',))
#             148 LOAD_FAST                7 (@py_assert6)
#             150 BUILD_TUPLE              1
#             152 LOAD_CONST               7 (('%(py5)s\n{%(py5)s = %(py0)s((%(py1)s - %(py2)s))\n} < %(py8)s',))
#             154 LOAD_FAST                5 (@py_assert4)
#             156 LOAD_FAST                6 (@py_assert7)
#             158 BUILD_TUPLE              2
#             160 CALL                     4
#             168 LOAD_CONST               8 ('abs')
#             170 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             180 LOAD_ATTR               12 (locals)
#             200 CALL                     0
#             208 CONTAINS_OP              0
#             210 POP_JUMP_IF_TRUE        25 (to 262)
#             212 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             222 LOAD_ATTR               14 (_should_repr_global_name)
#             242 LOAD_GLOBAL              4 (abs)
#             252 CALL                     1
#             260 POP_JUMP_IF_FALSE       25 (to 312)
#         >>  262 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             272 LOAD_ATTR               16 (_saferepr)
#             292 LOAD_GLOBAL              4 (abs)
#             302 CALL                     1
#             310 JUMP_FORWARD             1 (to 314)
#         >>  312 LOAD_CONST               8 ('abs')
#         >>  314 LOAD_CONST               9 ('rating')
#             316 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             326 LOAD_ATTR               12 (locals)
#             346 CALL                     0
#             354 CONTAINS_OP              0
#             356 POP_JUMP_IF_TRUE        21 (to 400)
#             358 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             368 LOAD_ATTR               14 (_should_repr_global_name)
#             388 LOAD_FAST                2 (rating)
#             390 CALL                     1
#             398 POP_JUMP_IF_FALSE       21 (to 442)
#         >>  400 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             410 LOAD_ATTR               16 (_saferepr)
#             430 LOAD_FAST                2 (rating)
#             432 CALL                     1
#             440 JUMP_FORWARD             1 (to 444)
#         >>  442 LOAD_CONST               9 ('rating')
#         >>  444 LOAD_CONST              10 ('expected')
#             446 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             456 LOAD_ATTR               12 (locals)
#             476 CALL                     0
#             484 CONTAINS_OP              0
#             486 POP_JUMP_IF_TRUE        21 (to 530)
#             488 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             498 LOAD_ATTR               14 (_should_repr_global_name)
#             518 LOAD_FAST                3 (expected)
#             520 CALL                     1
#             528 POP_JUMP_IF_FALSE       21 (to 572)
#         >>  530 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             540 LOAD_ATTR               16 (_saferepr)
#             560 LOAD_FAST                3 (expected)
#             562 CALL                     1
#             570 JUMP_FORWARD             1 (to 574)
#         >>  572 LOAD_CONST              10 ('expected')
#         >>  574 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             584 LOAD_ATTR               16 (_saferepr)
#             604 LOAD_FAST                5 (@py_assert4)
#             606 CALL                     1
#             614 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             624 LOAD_ATTR               16 (_saferepr)
#             644 LOAD_FAST                6 (@py_assert7)
#             646 CALL                     1
#             654 LOAD_CONST              11 (('py0', 'py1', 'py2', 'py5', 'py8'))
#             656 BUILD_CONST_KEY_MAP      5
#             658 BINARY_OP                6 (%)
#             662 STORE_FAST               8 (@py_format9)
#             664 LOAD_CONST              12 ('assert %(py10)s')
#             666 LOAD_CONST              13 ('py10')
#             668 LOAD_FAST                8 (@py_format9)
#             670 BUILD_MAP                1
#             672 BINARY_OP                6 (%)
#             676 STORE_FAST               9 (@py_format11)
#             678 LOAD_GLOBAL             19 (NULL + AssertionError)
#             688 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             698 LOAD_ATTR               20 (_format_explanation)
#             718 LOAD_FAST                9 (@py_format11)
#             720 CALL                     1
#             728 CALL                     1
#             736 RAISE_VARARGS            1
#         >>  738 LOAD_CONST               0 (None)
#             740 COPY                     1
#             742 STORE_FAST               4 (@py_assert3)
#             744 COPY                     1
#             746 STORE_FAST               5 (@py_assert4)
#             748 COPY                     1
#             750 STORE_FAST               7 (@py_assert6)
#             752 STORE_FAST               6 (@py_assert7)
#             754 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestMaintenanceN1Plan at 0x73cd945fe870, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 70>:
#  70           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestMaintenanceN1Plan')
#               8 STORE_NAME               2 (__qualname__)
# 
#  71          10 LOAD_CONST               1 (<code object test_generate_residual_n1_plan at 0x3afac750, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 71>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_generate_residual_n1_plan)
#              16 RETURN_CONST             2 (None)
# 
# Disassembly of <code object test_generate_residual_n1_plan at 0x3afac750, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 71>:
#  71           0 RESUME                   0
# 
#  72           2 LOAD_GLOBAL              1 (NULL + MaintenanceSecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  73          22 BUILD_LIST               0
#              24 LOAD_CONST               1 (('L1', 'L2', 'L3', 'L4'))
#              26 LIST_EXTEND              1
#              28 STORE_FAST               2 (branches)
# 
#  74          30 LOAD_FAST                1 (skill)
#              32 LOAD_ATTR                3 (NULL|self + _generate_residual_n1_plan)
#              52 LOAD_FAST                2 (branches)
#              54 LOAD_CONST               2 ('L2')
#              56 CALL                     2
#              64 STORE_FAST               3 (plan)
# 
#  75          66 LOAD_CONST               2 ('L2')
#              68 STORE_FAST               4 (@py_assert0)
#              70 LOAD_FAST                4 (@py_assert0)
#              72 LOAD_FAST                3 (plan)
#              74 CONTAINS_OP              1
#              76 STORE_FAST               5 (@py_assert2)
#              78 LOAD_FAST                5 (@py_assert2)
#              80 POP_JUMP_IF_TRUE       153 (to 388)
#              82 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              92 LOAD_ATTR                6 (_call_reprcompare)
#             112 LOAD_CONST               3 (('not in',))
#             114 LOAD_FAST                5 (@py_assert2)
#             116 BUILD_TUPLE              1
#             118 LOAD_CONST               4 (('%(py1)s not in %(py3)s',))
#             120 LOAD_FAST                4 (@py_assert0)
#             122 LOAD_FAST                3 (plan)
#             124 BUILD_TUPLE              2
#             126 CALL                     4
#             134 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             144 LOAD_ATTR                8 (_saferepr)
#             164 LOAD_FAST                4 (@py_assert0)
#             166 CALL                     1
#             174 LOAD_CONST               5 ('plan')
#             176 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             186 LOAD_ATTR               12 (locals)
#             206 CALL                     0
#             214 CONTAINS_OP              0
#             216 POP_JUMP_IF_TRUE        21 (to 260)
#             218 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             228 LOAD_ATTR               14 (_should_repr_global_name)
#             248 LOAD_FAST                3 (plan)
#             250 CALL                     1
#             258 POP_JUMP_IF_FALSE       21 (to 302)
#         >>  260 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             270 LOAD_ATTR                8 (_saferepr)
#             290 LOAD_FAST                3 (plan)
#             292 CALL                     1
#             300 JUMP_FORWARD             1 (to 304)
#         >>  302 LOAD_CONST               5 ('plan')
#         >>  304 LOAD_CONST               6 (('py1', 'py3'))
#             306 BUILD_CONST_KEY_MAP      2
#             308 BINARY_OP                6 (%)
#             312 STORE_FAST               6 (@py_format4)
#             314 LOAD_CONST               7 ('assert %(py5)s')
#             316 LOAD_CONST               8 ('py5')
#             318 LOAD_FAST                6 (@py_format4)
#             320 BUILD_MAP                1
#             322 BINARY_OP                6 (%)
#             326 STORE_FAST               7 (@py_format6)
#             328 LOAD_GLOBAL             17 (NULL + AssertionError)
#             338 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             348 LOAD_ATTR               18 (_format_explanation)
#             368 LOAD_FAST                7 (@py_format6)
#             370 CALL                     1
#             378 CALL                     1
#             386 RAISE_VARARGS            1
#         >>  388 LOAD_CONST               0 (None)
#             390 COPY                     1
#             392 STORE_FAST               4 (@py_assert0)
#             394 STORE_FAST               5 (@py_assert2)
# 
#  76         396 LOAD_GLOBAL             21 (NULL + len)
#             406 LOAD_FAST                3 (plan)
#             408 CALL                     1
#             416 STORE_FAST               5 (@py_assert2)
#             418 LOAD_CONST               9 (3)
#             420 STORE_FAST               8 (@py_assert5)
#             422 LOAD_FAST                5 (@py_assert2)
#             424 LOAD_FAST                8 (@py_assert5)
#             426 COMPARE_OP              40 (==)
#             430 STORE_FAST               9 (@py_assert4)
#             432 LOAD_FAST                9 (@py_assert4)
#             434 POP_JUMP_IF_TRUE       246 (to 928)
#             436 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             446 LOAD_ATTR                6 (_call_reprcompare)
#             466 LOAD_CONST              10 (('==',))
#             468 LOAD_FAST                9 (@py_assert4)
#             470 BUILD_TUPLE              1
#             472 LOAD_CONST              11 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             474 LOAD_FAST                5 (@py_assert2)
#             476 LOAD_FAST                8 (@py_assert5)
#             478 BUILD_TUPLE              2
#             480 CALL                     4
#             488 LOAD_CONST              12 ('len')
#             490 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             500 LOAD_ATTR               12 (locals)
#             520 CALL                     0
#             528 CONTAINS_OP              0
#             530 POP_JUMP_IF_TRUE        25 (to 582)
#             532 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             542 LOAD_ATTR               14 (_should_repr_global_name)
#             562 LOAD_GLOBAL             20 (len)
#             572 CALL                     1
#             580 POP_JUMP_IF_FALSE       25 (to 632)
#         >>  582 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             592 LOAD_ATTR                8 (_saferepr)
#             612 LOAD_GLOBAL             20 (len)
#             622 CALL                     1
#             630 JUMP_FORWARD             1 (to 634)
#         >>  632 LOAD_CONST              12 ('len')
#         >>  634 LOAD_CONST               5 ('plan')
#             636 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             646 LOAD_ATTR               12 (locals)
#             666 CALL                     0
#             674 CONTAINS_OP              0
#             676 POP_JUMP_IF_TRUE        21 (to 720)
#             678 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             688 LOAD_ATTR               14 (_should_repr_global_name)
#             708 LOAD_FAST                3 (plan)
#             710 CALL                     1
#             718 POP_JUMP_IF_FALSE       21 (to 762)
#         >>  720 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             730 LOAD_ATTR                8 (_saferepr)
#             750 LOAD_FAST                3 (plan)
#             752 CALL                     1
#             760 JUMP_FORWARD             1 (to 764)
#         >>  762 LOAD_CONST               5 ('plan')
#         >>  764 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             774 LOAD_ATTR                8 (_saferepr)
#             794 LOAD_FAST                5 (@py_assert2)
#             796 CALL                     1
#             804 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             814 LOAD_ATTR                8 (_saferepr)
#             834 LOAD_FAST                8 (@py_assert5)
#             836 CALL                     1
#             844 LOAD_CONST              13 (('py0', 'py1', 'py3', 'py6'))
#             846 BUILD_CONST_KEY_MAP      4
#             848 BINARY_OP                6 (%)
#             852 STORE_FAST              10 (@py_format7)
#             854 LOAD_CONST              14 ('assert %(py8)s')
#             856 LOAD_CONST              15 ('py8')
#             858 LOAD_FAST               10 (@py_format7)
#             860 BUILD_MAP                1
#             862 BINARY_OP                6 (%)
#             866 STORE_FAST              11 (@py_format9)
#             868 LOAD_GLOBAL             17 (NULL + AssertionError)
#             878 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             888 LOAD_ATTR               18 (_format_explanation)
#             908 LOAD_FAST               11 (@py_format9)
#             910 CALL                     1
#             918 CALL                     1
#             926 RAISE_VARARGS            1
#         >>  928 LOAD_CONST               0 (None)
#             930 COPY                     1
#             932 STORE_FAST               5 (@py_assert2)
#             934 COPY                     1
#             936 STORE_FAST               9 (@py_assert4)
#             938 STORE_FAST               8 (@py_assert5)
#             940 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestMaintenanceRun at 0x73cd945fe090, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 79>:
#  79           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestMaintenanceRun')
#               8 STORE_NAME               2 (__qualname__)
# 
#  80          10 LOAD_CONST               1 (<code object test_run_invalid_config_returns_failure at 0x3af9ee00, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 80>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_run_invalid_config_returns_failure)
#              16 RETURN_CONST             2 (None)
# 
# Disassembly of <code object test_run_invalid_config_returns_failure at 0x3af9ee00, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_maintenance_security.py", line 80>:
#  80           0 RESUME                   0
# 
#  81           2 LOAD_GLOBAL              1 (NULL + MaintenanceSecuritySkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  82          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + run)
#              44 BUILD_MAP                0
#              46 CALL                     1
#              54 STORE_FAST               2 (result)
# 
#  83          56 LOAD_FAST                2 (result)
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