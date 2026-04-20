# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/__pycache__/test_auto_channel_setup.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


def TestAutoChannelValidation():
    """TestAutoChannelValidation"""
pass  # TODO: restore


def TestAutoChannelBuilders():
    """TestAutoChannelBuilders"""
pass  # TODO: restore


def TestAutoChannelGrouping():
    """TestAutoChannelGrouping"""
pass  # TODO: restore


def TestAutoChannelRun():
    """TestAutoChannelRun"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('Tests for AutoChannelSetupSkill v2.')
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
#              42 LOAD_CONST               3 (('AutoChannelSetupSkill',))
#              44 IMPORT_NAME              8 (cloudpss_skills_v2.skills.auto_channel_setup)
#              46 IMPORT_FROM              9 (AutoChannelSetupSkill)
#              48 STORE_NAME               9 (AutoChannelSetupSkill)
#              50 POP_TOP
# 
#   7          52 PUSH_NULL
#              54 LOAD_BUILD_CLASS
#              56 LOAD_CONST               4 (<code object TestAutoChannelValidation at 0x73cd945fe4f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 7>)
#              58 MAKE_FUNCTION            0
#              60 LOAD_CONST               5 ('TestAutoChannelValidation')
#              62 CALL                     2
#              70 STORE_NAME              10 (TestAutoChannelValidation)
# 
#  28          72 PUSH_NULL
#              74 LOAD_BUILD_CLASS
#              76 LOAD_CONST               6 (<code object TestAutoChannelBuilders at 0x73cd93b064c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 28>)
#              78 MAKE_FUNCTION            0
#              80 LOAD_CONST               7 ('TestAutoChannelBuilders')
#              82 CALL                     2
#              90 STORE_NAME              11 (TestAutoChannelBuilders)
# 
#  55          92 PUSH_NULL
#              94 LOAD_BUILD_CLASS
#              96 LOAD_CONST               8 (<code object TestAutoChannelGrouping at 0x73cd945fc110, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 55>)
#              98 MAKE_FUNCTION            0
#             100 LOAD_CONST               9 ('TestAutoChannelGrouping')
#             102 CALL                     2
#             110 STORE_NAME              12 (TestAutoChannelGrouping)
# 
#  78         112 PUSH_NULL
#             114 LOAD_BUILD_CLASS
#             116 LOAD_CONST              10 (<code object TestAutoChannelRun at 0x73cd945fe090, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 78>)
#             118 MAKE_FUNCTION            0
#             120 LOAD_CONST              11 ('TestAutoChannelRun')
#             122 CALL                     2
#             130 STORE_NAME              13 (TestAutoChannelRun)
#             132 RETURN_CONST             2 (None)
# 
# Disassembly of <code object TestAutoChannelValidation at 0x73cd945fe4f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 7>:
#   7           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestAutoChannelValidation')
#               8 STORE_NAME               2 (__qualname__)
# 
#   8          10 LOAD_CONST               1 (<code object test_validate_missing_model at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 8>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_validate_missing_model)
# 
#  13          16 LOAD_CONST               2 (<code object test_validate_no_measurements at 0x3af90d20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 13>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_validate_no_measurements)
# 
#  18          22 LOAD_CONST               3 (<code object test_validate_valid_config at 0x3af3fb70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 18>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_validate_valid_config)
#              28 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_validate_missing_model at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 8>:
#   8           0 RESUME                   0
# 
#   9           2 LOAD_GLOBAL              1 (NULL + AutoChannelSetupSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  10          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + validate)
#              44 LOAD_CONST               1 ('measurements')
#              46 LOAD_CONST               2 ('voltage')
#              48 LOAD_CONST               3 ('enabled')
#              50 LOAD_CONST               4 (True)
#              52 BUILD_MAP                1
#              54 BUILD_MAP                1
#              56 BUILD_MAP                1
#              58 CALL                     1
#              66 UNPACK_SEQUENCE          2
#              70 STORE_FAST               2 (valid)
#              72 STORE_FAST               3 (errors)
# 
#  11          74 LOAD_CONST               5 (False)
#              76 STORE_FAST               4 (@py_assert2)
#              78 LOAD_FAST                2 (valid)
#              80 LOAD_FAST                4 (@py_assert2)
#              82 IS_OP                    0
#              84 STORE_FAST               5 (@py_assert1)
#              86 LOAD_FAST                5 (@py_assert1)
#              88 POP_JUMP_IF_TRUE       153 (to 396)
#              90 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             100 LOAD_ATTR                6 (_call_reprcompare)
#             120 LOAD_CONST               6 (('is',))
#             122 LOAD_FAST                5 (@py_assert1)
#             124 BUILD_TUPLE              1
#             126 LOAD_CONST               7 (('%(py0)s is %(py3)s',))
#             128 LOAD_FAST                2 (valid)
#             130 LOAD_FAST                4 (@py_assert2)
#             132 BUILD_TUPLE              2
#             134 CALL                     4
#             142 LOAD_CONST               8 ('valid')
#             144 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             154 LOAD_ATTR               10 (locals)
#             174 CALL                     0
#             182 CONTAINS_OP              0
#             184 POP_JUMP_IF_TRUE        21 (to 228)
#             186 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             196 LOAD_ATTR               12 (_should_repr_global_name)
#             216 LOAD_FAST                2 (valid)
#             218 CALL                     1
#             226 POP_JUMP_IF_FALSE       21 (to 270)
#         >>  228 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             238 LOAD_ATTR               14 (_saferepr)
#             258 LOAD_FAST                2 (valid)
#             260 CALL                     1
#             268 JUMP_FORWARD             1 (to 272)
#         >>  270 LOAD_CONST               8 ('valid')
#         >>  272 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             282 LOAD_ATTR               14 (_saferepr)
#             302 LOAD_FAST                4 (@py_assert2)
#             304 CALL                     1
#             312 LOAD_CONST               9 (('py0', 'py3'))
#             314 BUILD_CONST_KEY_MAP      2
#             316 BINARY_OP                6 (%)
#             320 STORE_FAST               6 (@py_format4)
#             322 LOAD_CONST              10 ('assert %(py5)s')
#             324 LOAD_CONST              11 ('py5')
#             326 LOAD_FAST                6 (@py_format4)
#             328 BUILD_MAP                1
#             330 BINARY_OP                6 (%)
#             334 STORE_FAST               7 (@py_format6)
#             336 LOAD_GLOBAL             17 (NULL + AssertionError)
#             346 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             356 LOAD_ATTR               18 (_format_explanation)
#             376 LOAD_FAST                7 (@py_format6)
#             378 CALL                     1
#             386 CALL                     1
#             394 RAISE_VARARGS            1
#         >>  396 LOAD_CONST               0 (None)
#             398 COPY                     1
#             400 STORE_FAST               5 (@py_assert1)
#             402 STORE_FAST               4 (@py_assert2)
#             404 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_no_measurements at 0x3af90d20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 13>:
#  13           0 RESUME                   0
# 
#  14           2 LOAD_GLOBAL              1 (NULL + AutoChannelSetupSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  15          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + validate)
#              44 LOAD_CONST               1 ('rid')
#              46 LOAD_CONST               2 ('test')
#              48 BUILD_MAP                1
#              50 BUILD_MAP                0
#              52 LOAD_CONST               3 (('model', 'measurements'))
#              54 BUILD_CONST_KEY_MAP      2
#              56 CALL                     1
#              64 UNPACK_SEQUENCE          2
#              68 STORE_FAST               2 (valid)
#              70 STORE_FAST               3 (errors)
# 
#  16          72 LOAD_CONST               4 (False)
#              74 STORE_FAST               4 (@py_assert2)
#              76 LOAD_FAST                2 (valid)
#              78 LOAD_FAST                4 (@py_assert2)
#              80 IS_OP                    0
#              82 STORE_FAST               5 (@py_assert1)
#              84 LOAD_FAST                5 (@py_assert1)
#              86 POP_JUMP_IF_TRUE       153 (to 394)
#              88 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              98 LOAD_ATTR                6 (_call_reprcompare)
#             118 LOAD_CONST               5 (('is',))
#             120 LOAD_FAST                5 (@py_assert1)
#             122 BUILD_TUPLE              1
#             124 LOAD_CONST               6 (('%(py0)s is %(py3)s',))
#             126 LOAD_FAST                2 (valid)
#             128 LOAD_FAST                4 (@py_assert2)
#             130 BUILD_TUPLE              2
#             132 CALL                     4
#             140 LOAD_CONST               7 ('valid')
#             142 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             152 LOAD_ATTR               10 (locals)
#             172 CALL                     0
#             180 CONTAINS_OP              0
#             182 POP_JUMP_IF_TRUE        21 (to 226)
#             184 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             194 LOAD_ATTR               12 (_should_repr_global_name)
#             214 LOAD_FAST                2 (valid)
#             216 CALL                     1
#             224 POP_JUMP_IF_FALSE       21 (to 268)
#         >>  226 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             236 LOAD_ATTR               14 (_saferepr)
#             256 LOAD_FAST                2 (valid)
#             258 CALL                     1
#             266 JUMP_FORWARD             1 (to 270)
#         >>  268 LOAD_CONST               7 ('valid')
#         >>  270 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             280 LOAD_ATTR               14 (_saferepr)
#             300 LOAD_FAST                4 (@py_assert2)
#             302 CALL                     1
#             310 LOAD_CONST               8 (('py0', 'py3'))
#             312 BUILD_CONST_KEY_MAP      2
#             314 BINARY_OP                6 (%)
#             318 STORE_FAST               6 (@py_format4)
#             320 LOAD_CONST               9 ('assert %(py5)s')
#             322 LOAD_CONST              10 ('py5')
#             324 LOAD_FAST                6 (@py_format4)
#             326 BUILD_MAP                1
#             328 BINARY_OP                6 (%)
#             332 STORE_FAST               7 (@py_format6)
#             334 LOAD_GLOBAL             17 (NULL + AssertionError)
#             344 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             354 LOAD_ATTR               18 (_format_explanation)
#             374 LOAD_FAST                7 (@py_format6)
#             376 CALL                     1
#             384 CALL                     1
#             392 RAISE_VARARGS            1
#         >>  394 LOAD_CONST               0 (None)
#             396 COPY                     1
#             398 STORE_FAST               5 (@py_assert1)
#             400 STORE_FAST               4 (@py_assert2)
#             402 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_validate_valid_config at 0x3af3fb70, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 18>:
#  18           0 RESUME                   0
# 
#  19           2 LOAD_GLOBAL              1 (NULL + AutoChannelSetupSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  21          22 LOAD_CONST               1 ('rid')
#              24 LOAD_CONST               2 ('test')
#              26 BUILD_MAP                1
# 
#  22          28 LOAD_CONST               3 ('voltage')
#              30 LOAD_CONST               4 ('enabled')
#              32 LOAD_CONST               5 (True)
#              34 BUILD_MAP                1
#              36 BUILD_MAP                1
# 
#  20          38 LOAD_CONST               6 (('model', 'measurements'))
#              40 BUILD_CONST_KEY_MAP      2
#              42 STORE_FAST               2 (config)
# 
#  24          44 LOAD_FAST                1 (skill)
#              46 LOAD_ATTR                3 (NULL|self + validate)
#              66 LOAD_FAST                2 (config)
#              68 CALL                     1
#              76 UNPACK_SEQUENCE          2
#              80 STORE_FAST               3 (valid)
#              82 STORE_FAST               4 (errors)
# 
#  25          84 LOAD_CONST               5 (True)
#              86 STORE_FAST               5 (@py_assert2)
#              88 LOAD_FAST                3 (valid)
#              90 LOAD_FAST                5 (@py_assert2)
#              92 IS_OP                    0
#              94 STORE_FAST               6 (@py_assert1)
#              96 LOAD_FAST                6 (@py_assert1)
#              98 POP_JUMP_IF_TRUE       153 (to 406)
#             100 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             110 LOAD_ATTR                6 (_call_reprcompare)
#             130 LOAD_CONST               7 (('is',))
#             132 LOAD_FAST                6 (@py_assert1)
#             134 BUILD_TUPLE              1
#             136 LOAD_CONST               8 (('%(py0)s is %(py3)s',))
#             138 LOAD_FAST                3 (valid)
#             140 LOAD_FAST                5 (@py_assert2)
#             142 BUILD_TUPLE              2
#             144 CALL                     4
#             152 LOAD_CONST               9 ('valid')
#             154 LOAD_GLOBAL              9 (NULL + @py_builtins)
#             164 LOAD_ATTR               10 (locals)
#             184 CALL                     0
#             192 CONTAINS_OP              0
#             194 POP_JUMP_IF_TRUE        21 (to 238)
#             196 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             206 LOAD_ATTR               12 (_should_repr_global_name)
#             226 LOAD_FAST                3 (valid)
#             228 CALL                     1
#             236 POP_JUMP_IF_FALSE       21 (to 280)
#         >>  238 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             248 LOAD_ATTR               14 (_saferepr)
#             268 LOAD_FAST                3 (valid)
#             270 CALL                     1
#             278 JUMP_FORWARD             1 (to 282)
#         >>  280 LOAD_CONST               9 ('valid')
#         >>  282 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             292 LOAD_ATTR               14 (_saferepr)
#             312 LOAD_FAST                5 (@py_assert2)
#             314 CALL                     1
#             322 LOAD_CONST              10 (('py0', 'py3'))
#             324 BUILD_CONST_KEY_MAP      2
#             326 BINARY_OP                6 (%)
#             330 STORE_FAST               7 (@py_format4)
#             332 LOAD_CONST              11 ('assert %(py5)s')
#             334 LOAD_CONST              12 ('py5')
#             336 LOAD_FAST                7 (@py_format4)
#             338 BUILD_MAP                1
#             340 BINARY_OP                6 (%)
#             344 STORE_FAST               8 (@py_format6)
#             346 LOAD_GLOBAL             17 (NULL + AssertionError)
#             356 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             366 LOAD_ATTR               18 (_format_explanation)
#             386 LOAD_FAST                8 (@py_format6)
#             388 CALL                     1
#             396 CALL                     1
#             404 RAISE_VARARGS            1
#         >>  406 LOAD_CONST               0 (None)
#             408 COPY                     1
#             410 STORE_FAST               6 (@py_assert1)
#             412 STORE_FAST               5 (@py_assert2)
#             414 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestAutoChannelBuilders at 0x73cd93b064c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 28>:
#  28           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestAutoChannelBuilders')
#               8 STORE_NAME               2 (__qualname__)
# 
#  29          10 LOAD_CONST               1 (<code object test_build_voltage_channel at 0x3afa4b40, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 29>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_build_voltage_channel)
# 
#  36          16 LOAD_CONST               2 (<code object test_build_current_channel at 0x3afa4f50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 36>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_build_current_channel)
# 
#  42          22 LOAD_CONST               3 (<code object test_build_power_channel at 0x3af9ce50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 42>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_build_power_channel)
# 
#  48          28 LOAD_CONST               4 (<code object test_build_frequency_channel at 0x3af909c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 48>)
#              30 MAKE_FUNCTION            0
#              32 STORE_NAME               6 (test_build_frequency_channel)
#              34 RETURN_CONST             5 (None)
# 
# Disassembly of <code object test_build_voltage_channel at 0x3afa4b40, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 29>:
#  29           0 RESUME                   0
# 
#  30           2 LOAD_GLOBAL              1 (NULL + AutoChannelSetupSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  31          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _build_voltage_channel)
#              44 LOAD_CONST               1 ('Bus7')
#              46 LOAD_CONST               2 (220.0)
#              48 LOAD_CONST               3 (200)
#              50 KW_NAMES                 4 (('v_base', 'freq'))
#              52 CALL                     3
#              60 STORE_FAST               2 (ch)
# 
#  32          62 LOAD_FAST                2 (ch)
#              64 LOAD_CONST               5 ('type')
#              66 BINARY_SUBSCR
#              70 STORE_FAST               3 (@py_assert0)
#              72 LOAD_CONST               6 ('voltage')
#              74 STORE_FAST               4 (@py_assert3)
#              76 LOAD_FAST                3 (@py_assert0)
#              78 LOAD_FAST                4 (@py_assert3)
#              80 COMPARE_OP              40 (==)
#              84 STORE_FAST               5 (@py_assert2)
#              86 LOAD_FAST                5 (@py_assert2)
#              88 POP_JUMP_IF_TRUE       108 (to 306)
#              90 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             100 LOAD_ATTR                6 (_call_reprcompare)
#             120 LOAD_CONST               7 (('==',))
#             122 LOAD_FAST                5 (@py_assert2)
#             124 BUILD_TUPLE              1
#             126 LOAD_CONST               8 (('%(py1)s == %(py4)s',))
#             128 LOAD_FAST                3 (@py_assert0)
#             130 LOAD_FAST                4 (@py_assert3)
#             132 BUILD_TUPLE              2
#             134 CALL                     4
#             142 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             152 LOAD_ATTR                8 (_saferepr)
#             172 LOAD_FAST                3 (@py_assert0)
#             174 CALL                     1
#             182 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             192 LOAD_ATTR                8 (_saferepr)
#             212 LOAD_FAST                4 (@py_assert3)
#             214 CALL                     1
#             222 LOAD_CONST               9 (('py1', 'py4'))
#             224 BUILD_CONST_KEY_MAP      2
#             226 BINARY_OP                6 (%)
#             230 STORE_FAST               6 (@py_format5)
#             232 LOAD_CONST              10 ('assert %(py6)s')
#             234 LOAD_CONST              11 ('py6')
#             236 LOAD_FAST                6 (@py_format5)
#             238 BUILD_MAP                1
#             240 BINARY_OP                6 (%)
#             244 STORE_FAST               7 (@py_format7)
#             246 LOAD_GLOBAL             11 (NULL + AssertionError)
#             256 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             266 LOAD_ATTR               12 (_format_explanation)
#             286 LOAD_FAST                7 (@py_format7)
#             288 CALL                     1
#             296 CALL                     1
#             304 RAISE_VARARGS            1
#         >>  306 LOAD_CONST               0 (None)
#             308 COPY                     1
#             310 STORE_FAST               3 (@py_assert0)
#             312 COPY                     1
#             314 STORE_FAST               5 (@py_assert2)
#             316 STORE_FAST               4 (@py_assert3)
# 
#  33         318 LOAD_FAST                2 (ch)
#             320 LOAD_CONST              12 ('component')
#             322 BINARY_SUBSCR
#             326 STORE_FAST               3 (@py_assert0)
#             328 LOAD_CONST               1 ('Bus7')
#             330 STORE_FAST               4 (@py_assert3)
#             332 LOAD_FAST                3 (@py_assert0)
#             334 LOAD_FAST                4 (@py_assert3)
#             336 COMPARE_OP              40 (==)
#             340 STORE_FAST               5 (@py_assert2)
#             342 LOAD_FAST                5 (@py_assert2)
#             344 POP_JUMP_IF_TRUE       108 (to 562)
#             346 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             356 LOAD_ATTR                6 (_call_reprcompare)
#             376 LOAD_CONST               7 (('==',))
#             378 LOAD_FAST                5 (@py_assert2)
#             380 BUILD_TUPLE              1
#             382 LOAD_CONST               8 (('%(py1)s == %(py4)s',))
#             384 LOAD_FAST                3 (@py_assert0)
#             386 LOAD_FAST                4 (@py_assert3)
#             388 BUILD_TUPLE              2
#             390 CALL                     4
#             398 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             408 LOAD_ATTR                8 (_saferepr)
#             428 LOAD_FAST                3 (@py_assert0)
#             430 CALL                     1
#             438 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             448 LOAD_ATTR                8 (_saferepr)
#             468 LOAD_FAST                4 (@py_assert3)
#             470 CALL                     1
#             478 LOAD_CONST               9 (('py1', 'py4'))
#             480 BUILD_CONST_KEY_MAP      2
#             482 BINARY_OP                6 (%)
#             486 STORE_FAST               6 (@py_format5)
#             488 LOAD_CONST              10 ('assert %(py6)s')
#             490 LOAD_CONST              11 ('py6')
#             492 LOAD_FAST                6 (@py_format5)
#             494 BUILD_MAP                1
#             496 BINARY_OP                6 (%)
#             500 STORE_FAST               7 (@py_format7)
#             502 LOAD_GLOBAL             11 (NULL + AssertionError)
#             512 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             522 LOAD_ATTR               12 (_format_explanation)
#             542 LOAD_FAST                7 (@py_format7)
#             544 CALL                     1
#             552 CALL                     1
#             560 RAISE_VARARGS            1
#         >>  562 LOAD_CONST               0 (None)
#             564 COPY                     1
#             566 STORE_FAST               3 (@py_assert0)
#             568 COPY                     1
#             570 STORE_FAST               5 (@py_assert2)
#             572 STORE_FAST               4 (@py_assert3)
# 
#  34         574 LOAD_FAST                2 (ch)
#             576 LOAD_CONST              13 ('v_base')
#             578 BINARY_SUBSCR
#             582 STORE_FAST               3 (@py_assert0)
#             584 LOAD_CONST               2 (220.0)
#             586 STORE_FAST               4 (@py_assert3)
#             588 LOAD_FAST                3 (@py_assert0)
#             590 LOAD_FAST                4 (@py_assert3)
#             592 COMPARE_OP              40 (==)
#             596 STORE_FAST               5 (@py_assert2)
#             598 LOAD_FAST                5 (@py_assert2)
#             600 POP_JUMP_IF_TRUE       108 (to 818)
#             602 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             612 LOAD_ATTR                6 (_call_reprcompare)
#             632 LOAD_CONST               7 (('==',))
#             634 LOAD_FAST                5 (@py_assert2)
#             636 BUILD_TUPLE              1
#             638 LOAD_CONST               8 (('%(py1)s == %(py4)s',))
#             640 LOAD_FAST                3 (@py_assert0)
#             642 LOAD_FAST                4 (@py_assert3)
#             644 BUILD_TUPLE              2
#             646 CALL                     4
#             654 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             664 LOAD_ATTR                8 (_saferepr)
#             684 LOAD_FAST                3 (@py_assert0)
#             686 CALL                     1
#             694 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             704 LOAD_ATTR                8 (_saferepr)
#             724 LOAD_FAST                4 (@py_assert3)
#             726 CALL                     1
#             734 LOAD_CONST               9 (('py1', 'py4'))
#             736 BUILD_CONST_KEY_MAP      2
#             738 BINARY_OP                6 (%)
#             742 STORE_FAST               6 (@py_format5)
#             744 LOAD_CONST              10 ('assert %(py6)s')
#             746 LOAD_CONST              11 ('py6')
#             748 LOAD_FAST                6 (@py_format5)
#             750 BUILD_MAP                1
#             752 BINARY_OP                6 (%)
#             756 STORE_FAST               7 (@py_format7)
#             758 LOAD_GLOBAL             11 (NULL + AssertionError)
#             768 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             778 LOAD_ATTR               12 (_format_explanation)
#             798 LOAD_FAST                7 (@py_format7)
#             800 CALL                     1
#             808 CALL                     1
#             816 RAISE_VARARGS            1
#         >>  818 LOAD_CONST               0 (None)
#             820 COPY                     1
#             822 STORE_FAST               3 (@py_assert0)
#             824 COPY                     1
#             826 STORE_FAST               5 (@py_assert2)
#             828 STORE_FAST               4 (@py_assert3)
#             830 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_build_current_channel at 0x3afa4f50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 36>:
#  36           0 RESUME                   0
# 
#  37           2 LOAD_GLOBAL              1 (NULL + AutoChannelSetupSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  38          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _build_current_channel)
#              44 LOAD_CONST               1 ('Line1')
#              46 LOAD_CONST               2 ('Is')
#              48 LOAD_CONST               3 (200)
#              50 KW_NAMES                 4 (('freq',))
#              52 CALL                     3
#              60 STORE_FAST               2 (ch)
# 
#  39          62 LOAD_FAST                2 (ch)
#              64 LOAD_CONST               5 ('type')
#              66 BINARY_SUBSCR
#              70 STORE_FAST               3 (@py_assert0)
#              72 LOAD_CONST               6 ('current')
#              74 STORE_FAST               4 (@py_assert3)
#              76 LOAD_FAST                3 (@py_assert0)
#              78 LOAD_FAST                4 (@py_assert3)
#              80 COMPARE_OP              40 (==)
#              84 STORE_FAST               5 (@py_assert2)
#              86 LOAD_FAST                5 (@py_assert2)
#              88 POP_JUMP_IF_TRUE       108 (to 306)
#              90 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             100 LOAD_ATTR                6 (_call_reprcompare)
#             120 LOAD_CONST               7 (('==',))
#             122 LOAD_FAST                5 (@py_assert2)
#             124 BUILD_TUPLE              1
#             126 LOAD_CONST               8 (('%(py1)s == %(py4)s',))
#             128 LOAD_FAST                3 (@py_assert0)
#             130 LOAD_FAST                4 (@py_assert3)
#             132 BUILD_TUPLE              2
#             134 CALL                     4
#             142 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             152 LOAD_ATTR                8 (_saferepr)
#             172 LOAD_FAST                3 (@py_assert0)
#             174 CALL                     1
#             182 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             192 LOAD_ATTR                8 (_saferepr)
#             212 LOAD_FAST                4 (@py_assert3)
#             214 CALL                     1
#             222 LOAD_CONST               9 (('py1', 'py4'))
#             224 BUILD_CONST_KEY_MAP      2
#             226 BINARY_OP                6 (%)
#             230 STORE_FAST               6 (@py_format5)
#             232 LOAD_CONST              10 ('assert %(py6)s')
#             234 LOAD_CONST              11 ('py6')
#             236 LOAD_FAST                6 (@py_format5)
#             238 BUILD_MAP                1
#             240 BINARY_OP                6 (%)
#             244 STORE_FAST               7 (@py_format7)
#             246 LOAD_GLOBAL             11 (NULL + AssertionError)
#             256 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             266 LOAD_ATTR               12 (_format_explanation)
#             286 LOAD_FAST                7 (@py_format7)
#             288 CALL                     1
#             296 CALL                     1
#             304 RAISE_VARARGS            1
#         >>  306 LOAD_CONST               0 (None)
#             308 COPY                     1
#             310 STORE_FAST               3 (@py_assert0)
#             312 COPY                     1
#             314 STORE_FAST               5 (@py_assert2)
#             316 STORE_FAST               4 (@py_assert3)
# 
#  40         318 LOAD_FAST                2 (ch)
#             320 LOAD_CONST              12 ('dim')
#             322 BINARY_SUBSCR
#             326 STORE_FAST               3 (@py_assert0)
#             328 LOAD_CONST              13 (3)
#             330 STORE_FAST               4 (@py_assert3)
#             332 LOAD_FAST                3 (@py_assert0)
#             334 LOAD_FAST                4 (@py_assert3)
#             336 COMPARE_OP              40 (==)
#             340 STORE_FAST               5 (@py_assert2)
#             342 LOAD_FAST                5 (@py_assert2)
#             344 POP_JUMP_IF_TRUE       108 (to 562)
#             346 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             356 LOAD_ATTR                6 (_call_reprcompare)
#             376 LOAD_CONST               7 (('==',))
#             378 LOAD_FAST                5 (@py_assert2)
#             380 BUILD_TUPLE              1
#             382 LOAD_CONST               8 (('%(py1)s == %(py4)s',))
#             384 LOAD_FAST                3 (@py_assert0)
#             386 LOAD_FAST                4 (@py_assert3)
#             388 BUILD_TUPLE              2
#             390 CALL                     4
#             398 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             408 LOAD_ATTR                8 (_saferepr)
#             428 LOAD_FAST                3 (@py_assert0)
#             430 CALL                     1
#             438 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             448 LOAD_ATTR                8 (_saferepr)
#             468 LOAD_FAST                4 (@py_assert3)
#             470 CALL                     1
#             478 LOAD_CONST               9 (('py1', 'py4'))
#             480 BUILD_CONST_KEY_MAP      2
#             482 BINARY_OP                6 (%)
#             486 STORE_FAST               6 (@py_format5)
#             488 LOAD_CONST              10 ('assert %(py6)s')
#             490 LOAD_CONST              11 ('py6')
#             492 LOAD_FAST                6 (@py_format5)
#             494 BUILD_MAP                1
#             496 BINARY_OP                6 (%)
#             500 STORE_FAST               7 (@py_format7)
#             502 LOAD_GLOBAL             11 (NULL + AssertionError)
#             512 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             522 LOAD_ATTR               12 (_format_explanation)
#             542 LOAD_FAST                7 (@py_format7)
#             544 CALL                     1
#             552 CALL                     1
#             560 RAISE_VARARGS            1
#         >>  562 LOAD_CONST               0 (None)
#             564 COPY                     1
#             566 STORE_FAST               3 (@py_assert0)
#             568 COPY                     1
#             570 STORE_FAST               5 (@py_assert2)
#             572 STORE_FAST               4 (@py_assert3)
#             574 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_build_power_channel at 0x3af9ce50, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 42>:
#  42           0 RESUME                   0
# 
#  43           2 LOAD_GLOBAL              1 (NULL + AutoChannelSetupSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  44          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _build_power_channel)
#              44 LOAD_CONST               1 ('Gen1')
#              46 LOAD_CONST               2 ('P')
#              48 LOAD_CONST               3 (200)
#              50 KW_NAMES                 4 (('freq',))
#              52 CALL                     3
#              60 STORE_FAST               2 (ch)
# 
#  45          62 LOAD_FAST                2 (ch)
#              64 LOAD_CONST               5 ('type')
#              66 BINARY_SUBSCR
#              70 STORE_FAST               3 (@py_assert0)
#              72 LOAD_CONST               6 ('power')
#              74 STORE_FAST               4 (@py_assert3)
#              76 LOAD_FAST                3 (@py_assert0)
#              78 LOAD_FAST                4 (@py_assert3)
#              80 COMPARE_OP              40 (==)
#              84 STORE_FAST               5 (@py_assert2)
#              86 LOAD_FAST                5 (@py_assert2)
#              88 POP_JUMP_IF_TRUE       108 (to 306)
#              90 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             100 LOAD_ATTR                6 (_call_reprcompare)
#             120 LOAD_CONST               7 (('==',))
#             122 LOAD_FAST                5 (@py_assert2)
#             124 BUILD_TUPLE              1
#             126 LOAD_CONST               8 (('%(py1)s == %(py4)s',))
#             128 LOAD_FAST                3 (@py_assert0)
#             130 LOAD_FAST                4 (@py_assert3)
#             132 BUILD_TUPLE              2
#             134 CALL                     4
#             142 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             152 LOAD_ATTR                8 (_saferepr)
#             172 LOAD_FAST                3 (@py_assert0)
#             174 CALL                     1
#             182 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             192 LOAD_ATTR                8 (_saferepr)
#             212 LOAD_FAST                4 (@py_assert3)
#             214 CALL                     1
#             222 LOAD_CONST               9 (('py1', 'py4'))
#             224 BUILD_CONST_KEY_MAP      2
#             226 BINARY_OP                6 (%)
#             230 STORE_FAST               6 (@py_format5)
#             232 LOAD_CONST              10 ('assert %(py6)s')
#             234 LOAD_CONST              11 ('py6')
#             236 LOAD_FAST                6 (@py_format5)
#             238 BUILD_MAP                1
#             240 BINARY_OP                6 (%)
#             244 STORE_FAST               7 (@py_format7)
#             246 LOAD_GLOBAL             11 (NULL + AssertionError)
#             256 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             266 LOAD_ATTR               12 (_format_explanation)
#             286 LOAD_FAST                7 (@py_format7)
#             288 CALL                     1
#             296 CALL                     1
#             304 RAISE_VARARGS            1
#         >>  306 LOAD_CONST               0 (None)
#             308 COPY                     1
#             310 STORE_FAST               3 (@py_assert0)
#             312 COPY                     1
#             314 STORE_FAST               5 (@py_assert2)
#             316 STORE_FAST               4 (@py_assert3)
# 
#  46         318 LOAD_FAST                2 (ch)
#             320 LOAD_CONST              12 ('power_type')
#             322 BINARY_SUBSCR
#             326 STORE_FAST               3 (@py_assert0)
#             328 LOAD_CONST               2 ('P')
#             330 STORE_FAST               4 (@py_assert3)
#             332 LOAD_FAST                3 (@py_assert0)
#             334 LOAD_FAST                4 (@py_assert3)
#             336 COMPARE_OP              40 (==)
#             340 STORE_FAST               5 (@py_assert2)
#             342 LOAD_FAST                5 (@py_assert2)
#             344 POP_JUMP_IF_TRUE       108 (to 562)
#             346 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             356 LOAD_ATTR                6 (_call_reprcompare)
#             376 LOAD_CONST               7 (('==',))
#             378 LOAD_FAST                5 (@py_assert2)
#             380 BUILD_TUPLE              1
#             382 LOAD_CONST               8 (('%(py1)s == %(py4)s',))
#             384 LOAD_FAST                3 (@py_assert0)
#             386 LOAD_FAST                4 (@py_assert3)
#             388 BUILD_TUPLE              2
#             390 CALL                     4
#             398 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             408 LOAD_ATTR                8 (_saferepr)
#             428 LOAD_FAST                3 (@py_assert0)
#             430 CALL                     1
#             438 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             448 LOAD_ATTR                8 (_saferepr)
#             468 LOAD_FAST                4 (@py_assert3)
#             470 CALL                     1
#             478 LOAD_CONST               9 (('py1', 'py4'))
#             480 BUILD_CONST_KEY_MAP      2
#             482 BINARY_OP                6 (%)
#             486 STORE_FAST               6 (@py_format5)
#             488 LOAD_CONST              10 ('assert %(py6)s')
#             490 LOAD_CONST              11 ('py6')
#             492 LOAD_FAST                6 (@py_format5)
#             494 BUILD_MAP                1
#             496 BINARY_OP                6 (%)
#             500 STORE_FAST               7 (@py_format7)
#             502 LOAD_GLOBAL             11 (NULL + AssertionError)
#             512 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             522 LOAD_ATTR               12 (_format_explanation)
#             542 LOAD_FAST                7 (@py_format7)
#             544 CALL                     1
#             552 CALL                     1
#             560 RAISE_VARARGS            1
#         >>  562 LOAD_CONST               0 (None)
#             564 COPY                     1
#             566 STORE_FAST               3 (@py_assert0)
#             568 COPY                     1
#             570 STORE_FAST               5 (@py_assert2)
#             572 STORE_FAST               4 (@py_assert3)
#             574 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_build_frequency_channel at 0x3af909c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 48>:
#  48           0 RESUME                   0
# 
#  49           2 LOAD_GLOBAL              1 (NULL + AutoChannelSetupSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  50          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _build_frequency_channel)
#              44 LOAD_CONST               1 ('Bus7')
#              46 LOAD_CONST               2 (50)
#              48 KW_NAMES                 3 (('freq',))
#              50 CALL                     2
#              58 STORE_FAST               2 (ch)
# 
#  51          60 LOAD_FAST                2 (ch)
#              62 LOAD_CONST               4 ('type')
#              64 BINARY_SUBSCR
#              68 STORE_FAST               3 (@py_assert0)
#              70 LOAD_CONST               5 ('frequency')
#              72 STORE_FAST               4 (@py_assert3)
#              74 LOAD_FAST                3 (@py_assert0)
#              76 LOAD_FAST                4 (@py_assert3)
#              78 COMPARE_OP              40 (==)
#              82 STORE_FAST               5 (@py_assert2)
#              84 LOAD_FAST                5 (@py_assert2)
#              86 POP_JUMP_IF_TRUE       108 (to 304)
#              88 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#              98 LOAD_ATTR                6 (_call_reprcompare)
#             118 LOAD_CONST               6 (('==',))
#             120 LOAD_FAST                5 (@py_assert2)
#             122 BUILD_TUPLE              1
#             124 LOAD_CONST               7 (('%(py1)s == %(py4)s',))
#             126 LOAD_FAST                3 (@py_assert0)
#             128 LOAD_FAST                4 (@py_assert3)
#             130 BUILD_TUPLE              2
#             132 CALL                     4
#             140 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             150 LOAD_ATTR                8 (_saferepr)
#             170 LOAD_FAST                3 (@py_assert0)
#             172 CALL                     1
#             180 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             190 LOAD_ATTR                8 (_saferepr)
#             210 LOAD_FAST                4 (@py_assert3)
#             212 CALL                     1
#             220 LOAD_CONST               8 (('py1', 'py4'))
#             222 BUILD_CONST_KEY_MAP      2
#             224 BINARY_OP                6 (%)
#             228 STORE_FAST               6 (@py_format5)
#             230 LOAD_CONST               9 ('assert %(py6)s')
#             232 LOAD_CONST              10 ('py6')
#             234 LOAD_FAST                6 (@py_format5)
#             236 BUILD_MAP                1
#             238 BINARY_OP                6 (%)
#             242 STORE_FAST               7 (@py_format7)
#             244 LOAD_GLOBAL             11 (NULL + AssertionError)
#             254 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             264 LOAD_ATTR               12 (_format_explanation)
#             284 LOAD_FAST                7 (@py_format7)
#             286 CALL                     1
#             294 CALL                     1
#             302 RAISE_VARARGS            1
#         >>  304 LOAD_CONST               0 (None)
#             306 COPY                     1
#             308 STORE_FAST               3 (@py_assert0)
#             310 COPY                     1
#             312 STORE_FAST               5 (@py_assert2)
#             314 STORE_FAST               4 (@py_assert3)
# 
#  52         316 LOAD_FAST                2 (ch)
#             318 LOAD_CONST              11 ('freq')
#             320 BINARY_SUBSCR
#             324 STORE_FAST               3 (@py_assert0)
#             326 LOAD_CONST               2 (50)
#             328 STORE_FAST               4 (@py_assert3)
#             330 LOAD_FAST                3 (@py_assert0)
#             332 LOAD_FAST                4 (@py_assert3)
#             334 COMPARE_OP              40 (==)
#             338 STORE_FAST               5 (@py_assert2)
#             340 LOAD_FAST                5 (@py_assert2)
#             342 POP_JUMP_IF_TRUE       108 (to 560)
#             344 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             354 LOAD_ATTR                6 (_call_reprcompare)
#             374 LOAD_CONST               6 (('==',))
#             376 LOAD_FAST                5 (@py_assert2)
#             378 BUILD_TUPLE              1
#             380 LOAD_CONST               7 (('%(py1)s == %(py4)s',))
#             382 LOAD_FAST                3 (@py_assert0)
#             384 LOAD_FAST                4 (@py_assert3)
#             386 BUILD_TUPLE              2
#             388 CALL                     4
#             396 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             406 LOAD_ATTR                8 (_saferepr)
#             426 LOAD_FAST                3 (@py_assert0)
#             428 CALL                     1
#             436 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             446 LOAD_ATTR                8 (_saferepr)
#             466 LOAD_FAST                4 (@py_assert3)
#             468 CALL                     1
#             476 LOAD_CONST               8 (('py1', 'py4'))
#             478 BUILD_CONST_KEY_MAP      2
#             480 BINARY_OP                6 (%)
#             484 STORE_FAST               6 (@py_format5)
#             486 LOAD_CONST               9 ('assert %(py6)s')
#             488 LOAD_CONST              10 ('py6')
#             490 LOAD_FAST                6 (@py_format5)
#             492 BUILD_MAP                1
#             494 BINARY_OP                6 (%)
#             498 STORE_FAST               7 (@py_format7)
#             500 LOAD_GLOBAL             11 (NULL + AssertionError)
#             510 LOAD_GLOBAL              5 (NULL + @pytest_ar)
#             520 LOAD_ATTR               12 (_format_explanation)
#             540 LOAD_FAST                7 (@py_format7)
#             542 CALL                     1
#             550 CALL                     1
#             558 RAISE_VARARGS            1
#         >>  560 LOAD_CONST               0 (None)
#             562 COPY                     1
#             564 STORE_FAST               3 (@py_assert0)
#             566 COPY                     1
#             568 STORE_FAST               5 (@py_assert2)
#             570 STORE_FAST               4 (@py_assert3)
#             572 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestAutoChannelGrouping at 0x73cd945fc110, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 55>:
#  55           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestAutoChannelGrouping')
#               8 STORE_NAME               2 (__qualname__)
# 
#  56          10 LOAD_CONST               1 (<code object test_group_channels_by_type at 0x3aef1020, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 56>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_group_channels_by_type)
# 
#  67          16 LOAD_CONST               2 (<code object test_generate_output_config at 0x3af9a920, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 67>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_generate_output_config)
#              22 RETURN_CONST             3 (None)
# 
# Disassembly of <code object test_group_channels_by_type at 0x3aef1020, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 56>:
#  56           0 RESUME                   0
# 
#  57           2 LOAD_GLOBAL              1 (NULL + AutoChannelSetupSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  59          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _build_voltage_channel)
#              44 LOAD_CONST               1 ('Bus1')
#              46 LOAD_CONST               2 (220)
#              48 CALL                     2
# 
#  60          56 LOAD_FAST                1 (skill)
#              58 LOAD_ATTR                3 (NULL|self + _build_voltage_channel)
#              78 LOAD_CONST               3 ('Bus2')
#              80 LOAD_CONST               2 (220)
#              82 CALL                     2
# 
#  61          90 LOAD_FAST                1 (skill)
#              92 LOAD_ATTR                5 (NULL|self + _build_current_channel)
#             112 LOAD_CONST               4 ('Line1')
#             114 LOAD_CONST               5 ('Is')
#             116 CALL                     2
# 
#  58         124 BUILD_LIST               3
#             126 STORE_FAST               2 (channels)
# 
#  63         128 LOAD_FAST                1 (skill)
#             130 LOAD_ATTR                7 (NULL|self + _group_channels_by_type)
#             150 LOAD_FAST                2 (channels)
#             152 CALL                     1
#             160 STORE_FAST               3 (counts)
# 
#  64         162 LOAD_FAST                3 (counts)
#             164 LOAD_CONST               6 ('voltage')
#             166 BINARY_SUBSCR
#             170 STORE_FAST               4 (@py_assert0)
#             172 LOAD_CONST               7 (2)
#             174 STORE_FAST               5 (@py_assert3)
#             176 LOAD_FAST                4 (@py_assert0)
#             178 LOAD_FAST                5 (@py_assert3)
#             180 COMPARE_OP              40 (==)
#             184 STORE_FAST               6 (@py_assert2)
#             186 LOAD_FAST                6 (@py_assert2)
#             188 POP_JUMP_IF_TRUE       108 (to 406)
#             190 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             200 LOAD_ATTR               10 (_call_reprcompare)
#             220 LOAD_CONST               8 (('==',))
#             222 LOAD_FAST                6 (@py_assert2)
#             224 BUILD_TUPLE              1
#             226 LOAD_CONST               9 (('%(py1)s == %(py4)s',))
#             228 LOAD_FAST                4 (@py_assert0)
#             230 LOAD_FAST                5 (@py_assert3)
#             232 BUILD_TUPLE              2
#             234 CALL                     4
#             242 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             252 LOAD_ATTR               12 (_saferepr)
#             272 LOAD_FAST                4 (@py_assert0)
#             274 CALL                     1
#             282 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             292 LOAD_ATTR               12 (_saferepr)
#             312 LOAD_FAST                5 (@py_assert3)
#             314 CALL                     1
#             322 LOAD_CONST              10 (('py1', 'py4'))
#             324 BUILD_CONST_KEY_MAP      2
#             326 BINARY_OP                6 (%)
#             330 STORE_FAST               7 (@py_format5)
#             332 LOAD_CONST              11 ('assert %(py6)s')
#             334 LOAD_CONST              12 ('py6')
#             336 LOAD_FAST                7 (@py_format5)
#             338 BUILD_MAP                1
#             340 BINARY_OP                6 (%)
#             344 STORE_FAST               8 (@py_format7)
#             346 LOAD_GLOBAL             15 (NULL + AssertionError)
#             356 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             366 LOAD_ATTR               16 (_format_explanation)
#             386 LOAD_FAST                8 (@py_format7)
#             388 CALL                     1
#             396 CALL                     1
#             404 RAISE_VARARGS            1
#         >>  406 LOAD_CONST               0 (None)
#             408 COPY                     1
#             410 STORE_FAST               4 (@py_assert0)
#             412 COPY                     1
#             414 STORE_FAST               6 (@py_assert2)
#             416 STORE_FAST               5 (@py_assert3)
# 
#  65         418 LOAD_FAST                3 (counts)
#             420 LOAD_CONST              13 ('current')
#             422 BINARY_SUBSCR
#             426 STORE_FAST               4 (@py_assert0)
#             428 LOAD_CONST              14 (1)
#             430 STORE_FAST               5 (@py_assert3)
#             432 LOAD_FAST                4 (@py_assert0)
#             434 LOAD_FAST                5 (@py_assert3)
#             436 COMPARE_OP              40 (==)
#             440 STORE_FAST               6 (@py_assert2)
#             442 LOAD_FAST                6 (@py_assert2)
#             444 POP_JUMP_IF_TRUE       108 (to 662)
#             446 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             456 LOAD_ATTR               10 (_call_reprcompare)
#             476 LOAD_CONST               8 (('==',))
#             478 LOAD_FAST                6 (@py_assert2)
#             480 BUILD_TUPLE              1
#             482 LOAD_CONST               9 (('%(py1)s == %(py4)s',))
#             484 LOAD_FAST                4 (@py_assert0)
#             486 LOAD_FAST                5 (@py_assert3)
#             488 BUILD_TUPLE              2
#             490 CALL                     4
#             498 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             508 LOAD_ATTR               12 (_saferepr)
#             528 LOAD_FAST                4 (@py_assert0)
#             530 CALL                     1
#             538 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             548 LOAD_ATTR               12 (_saferepr)
#             568 LOAD_FAST                5 (@py_assert3)
#             570 CALL                     1
#             578 LOAD_CONST              10 (('py1', 'py4'))
#             580 BUILD_CONST_KEY_MAP      2
#             582 BINARY_OP                6 (%)
#             586 STORE_FAST               7 (@py_format5)
#             588 LOAD_CONST              11 ('assert %(py6)s')
#             590 LOAD_CONST              12 ('py6')
#             592 LOAD_FAST                7 (@py_format5)
#             594 BUILD_MAP                1
#             596 BINARY_OP                6 (%)
#             600 STORE_FAST               8 (@py_format7)
#             602 LOAD_GLOBAL             15 (NULL + AssertionError)
#             612 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             622 LOAD_ATTR               16 (_format_explanation)
#             642 LOAD_FAST                8 (@py_format7)
#             644 CALL                     1
#             652 CALL                     1
#             660 RAISE_VARARGS            1
#         >>  662 LOAD_CONST               0 (None)
#             664 COPY                     1
#             666 STORE_FAST               4 (@py_assert0)
#             668 COPY                     1
#             670 STORE_FAST               6 (@py_assert2)
#             672 STORE_FAST               5 (@py_assert3)
#             674 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_generate_output_config at 0x3af9a920, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 67>:
#  67           0 RESUME                   0
# 
#  68           2 LOAD_GLOBAL              1 (NULL + AutoChannelSetupSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  70          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + _build_voltage_channel)
#              44 LOAD_CONST               1 ('Bus1')
#              46 LOAD_CONST               2 (220)
#              48 CALL                     2
# 
#  71          56 LOAD_FAST                1 (skill)
#              58 LOAD_ATTR                3 (NULL|self + _build_voltage_channel)
#              78 LOAD_CONST               3 ('Bus2')
#              80 LOAD_CONST               2 (220)
#              82 CALL                     2
# 
#  69          90 BUILD_LIST               2
#              92 STORE_FAST               2 (channels)
# 
#  73          94 LOAD_FAST                1 (skill)
#              96 LOAD_ATTR                5 (NULL|self + _generate_output_config)
#             116 LOAD_FAST                2 (channels)
#             118 CALL                     1
#             126 STORE_FAST               3 (output)
# 
#  74         128 LOAD_GLOBAL              7 (NULL + len)
#             138 LOAD_FAST                3 (output)
#             140 CALL                     1
#             148 STORE_FAST               4 (@py_assert2)
#             150 LOAD_CONST               4 (1)
#             152 STORE_FAST               5 (@py_assert5)
#             154 LOAD_FAST                4 (@py_assert2)
#             156 LOAD_FAST                5 (@py_assert5)
#             158 COMPARE_OP              92 (>=)
#             162 STORE_FAST               6 (@py_assert4)
#             164 LOAD_FAST                6 (@py_assert4)
#             166 POP_JUMP_IF_TRUE       246 (to 660)
#             168 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             178 LOAD_ATTR               10 (_call_reprcompare)
#             198 LOAD_CONST               5 (('>=',))
#             200 LOAD_FAST                6 (@py_assert4)
#             202 BUILD_TUPLE              1
#             204 LOAD_CONST               6 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} >= %(py6)s',))
#             206 LOAD_FAST                4 (@py_assert2)
#             208 LOAD_FAST                5 (@py_assert5)
#             210 BUILD_TUPLE              2
#             212 CALL                     4
#             220 LOAD_CONST               7 ('len')
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
#         >>  364 LOAD_CONST               7 ('len')
#         >>  366 LOAD_CONST               8 ('output')
#             368 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             378 LOAD_ATTR               14 (locals)
#             398 CALL                     0
#             406 CONTAINS_OP              0
#             408 POP_JUMP_IF_TRUE        21 (to 452)
#             410 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             420 LOAD_ATTR               16 (_should_repr_global_name)
#             440 LOAD_FAST                3 (output)
#             442 CALL                     1
#             450 POP_JUMP_IF_FALSE       21 (to 494)
#         >>  452 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             462 LOAD_ATTR               18 (_saferepr)
#             482 LOAD_FAST                3 (output)
#             484 CALL                     1
#             492 JUMP_FORWARD             1 (to 496)
#         >>  494 LOAD_CONST               8 ('output')
#         >>  496 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             506 LOAD_ATTR               18 (_saferepr)
#             526 LOAD_FAST                4 (@py_assert2)
#             528 CALL                     1
#             536 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             546 LOAD_ATTR               18 (_saferepr)
#             566 LOAD_FAST                5 (@py_assert5)
#             568 CALL                     1
#             576 LOAD_CONST               9 (('py0', 'py1', 'py3', 'py6'))
#             578 BUILD_CONST_KEY_MAP      4
#             580 BINARY_OP                6 (%)
#             584 STORE_FAST               7 (@py_format7)
#             586 LOAD_CONST              10 ('assert %(py8)s')
#             588 LOAD_CONST              11 ('py8')
#             590 LOAD_FAST                7 (@py_format7)
#             592 BUILD_MAP                1
#             594 BINARY_OP                6 (%)
#             598 STORE_FAST               8 (@py_format9)
#             600 LOAD_GLOBAL             21 (NULL + AssertionError)
#             610 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             620 LOAD_ATTR               22 (_format_explanation)
#             640 LOAD_FAST                8 (@py_format9)
#             642 CALL                     1
#             650 CALL                     1
#             658 RAISE_VARARGS            1
#         >>  660 LOAD_CONST               0 (None)
#             662 COPY                     1
#             664 STORE_FAST               4 (@py_assert2)
#             666 COPY                     1
#             668 STORE_FAST               6 (@py_assert4)
#             670 STORE_FAST               5 (@py_assert5)
# 
#  75         672 LOAD_FAST                3 (output)
#             674 LOAD_CONST              12 (0)
#             676 BINARY_SUBSCR
#             680 LOAD_CONST              13 ('freq')
#             682 BINARY_SUBSCR
#             686 STORE_FAST               9 (@py_assert0)
#             688 LOAD_CONST              14 (200)
#             690 STORE_FAST              10 (@py_assert3)
#             692 LOAD_FAST                9 (@py_assert0)
#             694 LOAD_FAST               10 (@py_assert3)
#             696 COMPARE_OP              40 (==)
#             700 STORE_FAST               4 (@py_assert2)
#             702 LOAD_FAST                4 (@py_assert2)
#             704 POP_JUMP_IF_TRUE       108 (to 922)
#             706 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             716 LOAD_ATTR               10 (_call_reprcompare)
#             736 LOAD_CONST              15 (('==',))
#             738 LOAD_FAST                4 (@py_assert2)
#             740 BUILD_TUPLE              1
#             742 LOAD_CONST              16 (('%(py1)s == %(py4)s',))
#             744 LOAD_FAST                9 (@py_assert0)
#             746 LOAD_FAST               10 (@py_assert3)
#             748 BUILD_TUPLE              2
#             750 CALL                     4
#             758 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             768 LOAD_ATTR               18 (_saferepr)
#             788 LOAD_FAST                9 (@py_assert0)
#             790 CALL                     1
#             798 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             808 LOAD_ATTR               18 (_saferepr)
#             828 LOAD_FAST               10 (@py_assert3)
#             830 CALL                     1
#             838 LOAD_CONST              17 (('py1', 'py4'))
#             840 BUILD_CONST_KEY_MAP      2
#             842 BINARY_OP                6 (%)
#             846 STORE_FAST              11 (@py_format5)
#             848 LOAD_CONST              18 ('assert %(py6)s')
#             850 LOAD_CONST              19 ('py6')
#             852 LOAD_FAST               11 (@py_format5)
#             854 BUILD_MAP                1
#             856 BINARY_OP                6 (%)
#             860 STORE_FAST               7 (@py_format7)
#             862 LOAD_GLOBAL             21 (NULL + AssertionError)
#             872 LOAD_GLOBAL              9 (NULL + @pytest_ar)
#             882 LOAD_ATTR               22 (_format_explanation)
#             902 LOAD_FAST                7 (@py_format7)
#             904 CALL                     1
#             912 CALL                     1
#             920 RAISE_VARARGS            1
#         >>  922 LOAD_CONST               0 (None)
#             924 COPY                     1
#             926 STORE_FAST               9 (@py_assert0)
#             928 COPY                     1
#             930 STORE_FAST               4 (@py_assert2)
#             932 STORE_FAST              10 (@py_assert3)
#             934 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestAutoChannelRun at 0x73cd945fe090, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 78>:
#  78           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestAutoChannelRun')
#               8 STORE_NAME               2 (__qualname__)
# 
#  79          10 LOAD_CONST               1 (<code object test_run_invalid_config_returns_failure at 0x3afa4860, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 79>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_run_invalid_config_returns_failure)
#              16 RETURN_CONST             2 (None)
# 
# Disassembly of <code object test_run_invalid_config_returns_failure at 0x3afa4860, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_auto_channel_setup.py", line 79>:
#  79           0 RESUME                   0
# 
#  80           2 LOAD_GLOBAL              1 (NULL + AutoChannelSetupSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  81          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + run)
#              44 BUILD_MAP                0
#              46 CALL                     1
#              54 STORE_FAST               2 (result)
# 
#  82          56 LOAD_FAST                2 (result)
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