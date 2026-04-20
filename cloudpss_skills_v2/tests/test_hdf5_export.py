# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/__pycache__/test_hdf5_export.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


def TestHDF5Validation():
    """TestHDF5Validation"""
pass  # TODO: restore


def TestHDF5Export():
    """TestHDF5Export"""
pass  # TODO: restore


def TestHDF5Read():
    """TestHDF5Read"""
pass  # TODO: restore


def TestHDF5Run():
    """TestHDF5Run"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('Tests for HDF5ExportSkill v2.')
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
#              36 IMPORT_NAME              7 (json)
#              38 STORE_NAME               7 (json)
# 
#   4          40 LOAD_CONST               1 (0)
#              42 LOAD_CONST               2 (None)
#              44 IMPORT_NAME              8 (tempfile)
#              46 STORE_NAME               8 (tempfile)
# 
#   5          48 LOAD_CONST               1 (0)
#              50 LOAD_CONST               3 (('Path',))
#              52 IMPORT_NAME              9 (pathlib)
#              54 IMPORT_FROM             10 (Path)
#              56 STORE_NAME              10 (Path)
#              58 POP_TOP
# 
#   7          60 LOAD_CONST               1 (0)
#              62 LOAD_CONST               2 (None)
#              64 IMPORT_NAME             11 (h5py)
#              66 STORE_NAME              11 (h5py)
# 
#   8          68 LOAD_CONST               1 (0)
#              70 LOAD_CONST               2 (None)
#              72 IMPORT_NAME             12 (numpy)
#              74 STORE_NAME              13 (np)
# 
#   9          76 LOAD_CONST               1 (0)
#              78 LOAD_CONST               2 (None)
#              80 IMPORT_NAME             14 (pytest)
#              82 STORE_NAME              14 (pytest)
# 
#  10          84 LOAD_CONST               1 (0)
#              86 LOAD_CONST               4 (('HDF5ExportSkill',))
#              88 IMPORT_NAME             15 (cloudpss_skills_v2.skills.hdf5_export)
#              90 IMPORT_FROM             16 (HDF5ExportSkill)
#              92 STORE_NAME              16 (HDF5ExportSkill)
#              94 POP_TOP
# 
#  13          96 PUSH_NULL
#              98 LOAD_BUILD_CLASS
#             100 LOAD_CONST               5 (<code object TestHDF5Validation at 0x73cd945fe090, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 13>)
#             102 MAKE_FUNCTION            0
#             104 LOAD_CONST               6 ('TestHDF5Validation')
#             106 CALL                     2
#             114 STORE_NAME              17 (TestHDF5Validation)
# 
#  31         116 PUSH_NULL
#             118 LOAD_BUILD_CLASS
#             120 LOAD_CONST               7 (<code object TestHDF5Export at 0x73cd945fc110, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 31>)
#             122 MAKE_FUNCTION            0
#             124 LOAD_CONST               8 ('TestHDF5Export')
#             126 CALL                     2
#             134 STORE_NAME              18 (TestHDF5Export)
# 
#  55         136 PUSH_NULL
#             138 LOAD_BUILD_CLASS
#             140 LOAD_CONST               9 (<code object TestHDF5Read at 0x73cd945fdfb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 55>)
#             142 MAKE_FUNCTION            0
#             144 LOAD_CONST              10 ('TestHDF5Read')
#             146 CALL                     2
#             154 STORE_NAME              19 (TestHDF5Read)
# 
#  78         156 PUSH_NULL
#             158 LOAD_BUILD_CLASS
#             160 LOAD_CONST              11 (<code object TestHDF5Run at 0x73cd945ff210, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 78>)
#             162 MAKE_FUNCTION            0
#             164 LOAD_CONST              12 ('TestHDF5Run')
#             166 CALL                     2
#             174 STORE_NAME              20 (TestHDF5Run)
#             176 RETURN_CONST             2 (None)
# 
# Disassembly of <code object TestHDF5Validation at 0x73cd945fe090, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 13>:
#  13           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestHDF5Validation')
#               8 STORE_NAME               2 (__qualname__)
# 
#  14          10 LOAD_CONST               1 (<code object test_validate_missing_source at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 14>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_validate_missing_source)
# 
#  19          16 LOAD_CONST               2 (<code object test_validate_file_type_missing_path at 0x3af90d20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 19>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_validate_file_type_missing_path)
# 
#  24          22 LOAD_CONST               3 (<code object test_validate_valid_config at 0x3ae632d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 24>)
#              24 MAKE_FUNCTION            0
#              26 STORE_NAME               5 (test_validate_valid_config)
#              28 RETURN_CONST             4 (None)
# 
# Disassembly of <code object test_validate_missing_source at 0x3afa3fb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 14>:
#  14           0 RESUME                   0
# 
#  15           2 LOAD_GLOBAL              1 (NULL + HDF5ExportSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  16          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + validate)
#              44 BUILD_MAP                0
#              46 CALL                     1
#              54 UNPACK_SEQUENCE          2
#              58 STORE_FAST               2 (valid)
#              60 STORE_FAST               3 (errors)
# 
#  17          62 LOAD_CONST               1 (False)
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
# Disassembly of <code object test_validate_file_type_missing_path at 0x3af90d20, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 19>:
#  19           0 RESUME                   0
# 
#  20           2 LOAD_GLOBAL              1 (NULL + HDF5ExportSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  21          22 LOAD_FAST                1 (skill)
#              24 LOAD_ATTR                3 (NULL|self + validate)
#              44 LOAD_CONST               1 ('source')
#              46 LOAD_CONST               2 ('type')
#              48 LOAD_CONST               3 ('file')
#              50 BUILD_MAP                1
#              52 BUILD_MAP                1
#              54 CALL                     1
#              62 UNPACK_SEQUENCE          2
#              66 STORE_FAST               2 (valid)
#              68 STORE_FAST               3 (errors)
# 
#  22          70 LOAD_CONST               4 (False)
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
# Disassembly of <code object test_validate_valid_config at 0x3ae632d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 24>:
#  24           0 RESUME                   0
# 
#  25           2 LOAD_GLOBAL              1 (NULL + HDF5ExportSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  26          22 LOAD_CONST               1 ('source')
#              24 LOAD_CONST               2 ('type')
#              26 LOAD_CONST               3 ('emt_result')
#              28 BUILD_MAP                1
#              30 BUILD_MAP                1
#              32 STORE_FAST               2 (config)
# 
#  27          34 LOAD_FAST                1 (skill)
#              36 LOAD_ATTR                3 (NULL|self + validate)
#              56 LOAD_FAST                2 (config)
#              58 CALL                     1
#              66 UNPACK_SEQUENCE          2
#              70 STORE_FAST               3 (valid)
#              72 STORE_FAST               4 (errors)
# 
#  28          74 LOAD_CONST               4 (True)
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
# Disassembly of <code object TestHDF5Export at 0x73cd945fc110, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 31>:
#  31           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestHDF5Export')
#               8 STORE_NAME               2 (__qualname__)
# 
#  32          10 LOAD_CONST               1 (<code object test_export_to_hdf5 at 0x3afa7720, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 32>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_export_to_hdf5)
# 
#  44          16 LOAD_CONST               2 (<code object test_create_index at 0x3af9c2b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 44>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_create_index)
#              22 RETURN_CONST             3 (None)
# 
# Disassembly of <code object test_export_to_hdf5 at 0x3afa7720, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 32>:
#  32           0 RESUME                   0
# 
#  33           2 LOAD_GLOBAL              1 (NULL + HDF5ExportSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  34          22 LOAD_GLOBAL              3 (NULL + tempfile)
#              32 LOAD_ATTR                4 (TemporaryDirectory)
#              52 CALL                     0
#              60 BEFORE_WITH
#              62 STORE_FAST               2 (tmpdir)
# 
#  35          64 LOAD_GLOBAL              7 (NULL + Path)
#              74 LOAD_FAST                2 (tmpdir)
#              76 CALL                     1
#              84 LOAD_CONST               1 ('test.h5')
#              86 BINARY_OP               11 (/)
#              90 STORE_FAST               3 (hdf5_path)
# 
#  36          92 LOAD_CONST               2 ('test')
#              94 LOAD_GLOBAL              9 (NULL + np)
#             104 LOAD_ATTR               10 (array)
#             124 BUILD_LIST               0
#             126 LOAD_CONST               3 ((1.0, 2.0, 3.0))
#             128 LIST_EXTEND              1
#             130 CALL                     1
#             138 LOAD_CONST               4 (('type', 'values'))
#             140 BUILD_CONST_KEY_MAP      2
#             142 STORE_FAST               4 (data)
# 
#  37         144 LOAD_FAST                1 (skill)
#             146 LOAD_ATTR               13 (NULL|self + _export_to_hdf5)
#             166 LOAD_FAST                4 (data)
#             168 LOAD_FAST                3 (hdf5_path)
#             170 LOAD_CONST               5 ('title')
#             172 LOAD_CONST               6 ('Test')
#             174 BUILD_MAP                1
#             176 CALL                     3
#             184 POP_TOP
# 
#  38         186 LOAD_FAST                3 (hdf5_path)
#             188 LOAD_ATTR               14 (exists)
#             208 STORE_FAST               5 (@py_assert1)
#             210 PUSH_NULL
#             212 LOAD_FAST                5 (@py_assert1)
#             214 CALL                     0
#             222 STORE_FAST               6 (@py_assert3)
#             224 LOAD_FAST                6 (@py_assert3)
#             226 POP_JUMP_IF_TRUE       141 (to 510)
#             228 LOAD_CONST               7 ('assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.exists\n}()\n}')
#             230 LOAD_CONST               8 ('hdf5_path')
#             232 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             242 LOAD_ATTR               18 (locals)
#             262 CALL                     0
#             270 CONTAINS_OP              0
#             272 POP_JUMP_IF_TRUE        21 (to 316)
#             274 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             284 LOAD_ATTR               22 (_should_repr_global_name)
#             304 LOAD_FAST                3 (hdf5_path)
#             306 CALL                     1
#             314 POP_JUMP_IF_FALSE       21 (to 358)
#         >>  316 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             326 LOAD_ATTR               24 (_saferepr)
#             346 LOAD_FAST                3 (hdf5_path)
#             348 CALL                     1
#             356 JUMP_FORWARD             1 (to 360)
#         >>  358 LOAD_CONST               8 ('hdf5_path')
#         >>  360 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             370 LOAD_ATTR               24 (_saferepr)
#             390 LOAD_FAST                5 (@py_assert1)
#             392 CALL                     1
#             400 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             410 LOAD_ATTR               24 (_saferepr)
#             430 LOAD_FAST                6 (@py_assert3)
#             432 CALL                     1
#             440 LOAD_CONST               9 (('py0', 'py2', 'py4'))
#             442 BUILD_CONST_KEY_MAP      3
#             444 BINARY_OP                6 (%)
#             448 STORE_FAST               7 (@py_format5)
#             450 LOAD_GLOBAL             27 (NULL + AssertionError)
#             460 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             470 LOAD_ATTR               28 (_format_explanation)
#             490 LOAD_FAST                7 (@py_format5)
#             492 CALL                     1
#             500 CALL                     1
#             508 RAISE_VARARGS            1
#         >>  510 LOAD_CONST               0 (None)
#             512 COPY                     1
#             514 STORE_FAST               5 (@py_assert1)
#             516 STORE_FAST               6 (@py_assert3)
# 
#  39         518 LOAD_GLOBAL             31 (NULL + h5py)
#             528 LOAD_ATTR               32 (File)
#             548 LOAD_FAST                3 (hdf5_path)
#             550 LOAD_CONST              10 ('r')
#             552 CALL                     2
#             560 BEFORE_WITH
#             562 STORE_FAST               8 (f)
# 
#  40         564 LOAD_FAST                8 (f)
#             566 LOAD_ATTR               34 (attrs)
#             586 LOAD_CONST               5 ('title')
#             588 BINARY_SUBSCR
#             592 STORE_FAST               9 (@py_assert0)
#             594 LOAD_CONST               6 ('Test')
#             596 STORE_FAST               6 (@py_assert3)
#             598 LOAD_FAST                9 (@py_assert0)
#             600 LOAD_FAST                6 (@py_assert3)
#             602 COMPARE_OP              40 (==)
#             606 STORE_FAST              10 (@py_assert2)
#             608 LOAD_FAST               10 (@py_assert2)
#             610 POP_JUMP_IF_TRUE       108 (to 828)
#             612 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             622 LOAD_ATTR               36 (_call_reprcompare)
#             642 LOAD_CONST              11 (('==',))
#             644 LOAD_FAST               10 (@py_assert2)
#             646 BUILD_TUPLE              1
#             648 LOAD_CONST              12 (('%(py1)s == %(py4)s',))
#             650 LOAD_FAST                9 (@py_assert0)
#             652 LOAD_FAST                6 (@py_assert3)
#             654 BUILD_TUPLE              2
#             656 CALL                     4
#             664 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             674 LOAD_ATTR               24 (_saferepr)
#             694 LOAD_FAST                9 (@py_assert0)
#             696 CALL                     1
#             704 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             714 LOAD_ATTR               24 (_saferepr)
#             734 LOAD_FAST                6 (@py_assert3)
#             736 CALL                     1
#             744 LOAD_CONST              13 (('py1', 'py4'))
#             746 BUILD_CONST_KEY_MAP      2
#             748 BINARY_OP                6 (%)
#             752 STORE_FAST               7 (@py_format5)
#             754 LOAD_CONST              14 ('assert %(py6)s')
#             756 LOAD_CONST              15 ('py6')
#             758 LOAD_FAST                7 (@py_format5)
#             760 BUILD_MAP                1
#             762 BINARY_OP                6 (%)
#             766 STORE_FAST              11 (@py_format7)
#             768 LOAD_GLOBAL             27 (NULL + AssertionError)
#             778 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             788 LOAD_ATTR               28 (_format_explanation)
#             808 LOAD_FAST               11 (@py_format7)
#             810 CALL                     1
#             818 CALL                     1
#             826 RAISE_VARARGS            1
#         >>  828 LOAD_CONST               0 (None)
#             830 COPY                     1
#             832 STORE_FAST               9 (@py_assert0)
#             834 COPY                     1
#             836 STORE_FAST              10 (@py_assert2)
#             838 STORE_FAST               6 (@py_assert3)
# 
#  41         840 LOAD_CONST              16 ('values')
#             842 STORE_FAST               9 (@py_assert0)
#             844 LOAD_FAST                9 (@py_assert0)
#             846 LOAD_FAST                8 (f)
#             848 CONTAINS_OP              0
#             850 STORE_FAST              10 (@py_assert2)
#             852 LOAD_FAST               10 (@py_assert2)
#             854 POP_JUMP_IF_TRUE       153 (to 1162)
#             856 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             866 LOAD_ATTR               36 (_call_reprcompare)
#             886 LOAD_CONST              17 (('in',))
#             888 LOAD_FAST               10 (@py_assert2)
#             890 BUILD_TUPLE              1
#             892 LOAD_CONST              18 (('%(py1)s in %(py3)s',))
#             894 LOAD_FAST                9 (@py_assert0)
#             896 LOAD_FAST                8 (f)
#             898 BUILD_TUPLE              2
#             900 CALL                     4
#             908 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             918 LOAD_ATTR               24 (_saferepr)
#             938 LOAD_FAST                9 (@py_assert0)
#             940 CALL                     1
#             948 LOAD_CONST              19 ('f')
#             950 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             960 LOAD_ATTR               18 (locals)
#             980 CALL                     0
#             988 CONTAINS_OP              0
#             990 POP_JUMP_IF_TRUE        21 (to 1034)
#             992 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1002 LOAD_ATTR               22 (_should_repr_global_name)
#            1022 LOAD_FAST                8 (f)
#            1024 CALL                     1
#            1032 POP_JUMP_IF_FALSE       21 (to 1076)
#         >> 1034 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1044 LOAD_ATTR               24 (_saferepr)
#            1064 LOAD_FAST                8 (f)
#            1066 CALL                     1
#            1074 JUMP_FORWARD             1 (to 1078)
#         >> 1076 LOAD_CONST              19 ('f')
#         >> 1078 LOAD_CONST              20 (('py1', 'py3'))
#            1080 BUILD_CONST_KEY_MAP      2
#            1082 BINARY_OP                6 (%)
#            1086 STORE_FAST              12 (@py_format4)
#            1088 LOAD_CONST              21 ('assert %(py5)s')
#            1090 LOAD_CONST              22 ('py5')
#            1092 LOAD_FAST               12 (@py_format4)
#            1094 BUILD_MAP                1
#            1096 BINARY_OP                6 (%)
#            1100 STORE_FAST              13 (@py_format6)
#            1102 LOAD_GLOBAL             27 (NULL + AssertionError)
#            1112 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#            1122 LOAD_ATTR               28 (_format_explanation)
#            1142 LOAD_FAST               13 (@py_format6)
#            1144 CALL                     1
#            1152 CALL                     1
#            1160 RAISE_VARARGS            1
#         >> 1162 LOAD_CONST               0 (None)
#            1164 COPY                     1
#            1166 STORE_FAST               9 (@py_assert0)
#            1168 STORE_FAST              10 (@py_assert2)
# 
#  42        1170 LOAD_GLOBAL              8 (np)
#            1180 LOAD_ATTR               38 (testing)
#            1200 LOAD_ATTR               41 (NULL|self + assert_array_equal)
#            1220 LOAD_FAST                8 (f)
#            1222 LOAD_CONST              16 ('values')
#            1224 BINARY_SUBSCR
#            1228 LOAD_CONST               0 (None)
#            1230 LOAD_CONST               0 (None)
#            1232 BINARY_SLICE
#            1234 BUILD_LIST               0
#            1236 LOAD_CONST               3 ((1.0, 2.0, 3.0))
#            1238 LIST_EXTEND              1
#            1240 CALL                     2
#            1248 POP_TOP
# 
#  39        1250 LOAD_CONST               0 (None)
#            1252 LOAD_CONST               0 (None)
#            1254 LOAD_CONST               0 (None)
#            1256 CALL                     2
#            1264 POP_TOP
# 
#  34     >> 1266 LOAD_CONST               0 (None)
#            1268 LOAD_CONST               0 (None)
#            1270 LOAD_CONST               0 (None)
#            1272 CALL                     2
#            1280 POP_TOP
#            1282 RETURN_CONST             0 (None)
# 
#  39     >> 1284 PUSH_EXC_INFO
#            1286 WITH_EXCEPT_START
#            1288 POP_JUMP_IF_TRUE         1 (to 1292)
#            1290 RERAISE                  2
#         >> 1292 POP_TOP
#            1294 POP_EXCEPT
#            1296 POP_TOP
#            1298 POP_TOP
#            1300 JUMP_BACKWARD           18 (to 1266)
#         >> 1302 COPY                     3
#            1304 POP_EXCEPT
#            1306 RERAISE                  1
# 
#  34     >> 1308 PUSH_EXC_INFO
#            1310 WITH_EXCEPT_START
#            1312 POP_JUMP_IF_TRUE         1 (to 1316)
#            1314 RERAISE                  2
#         >> 1316 POP_TOP
#            1318 POP_EXCEPT
#            1320 POP_TOP
#            1322 POP_TOP
#            1324 RETURN_CONST             0 (None)
#         >> 1326 COPY                     3
#            1328 POP_EXCEPT
#            1330 RERAISE                  1
# ExceptionTable:
#   62 to 560 -> 1308 [1] lasti
#   562 to 1248 -> 1284 [2] lasti
#   1250 to 1264 -> 1308 [1] lasti
#   1284 to 1292 -> 1302 [4] lasti
#   1294 to 1306 -> 1308 [1] lasti
#   1308 to 1316 -> 1326 [3] lasti
# 
# Disassembly of <code object test_create_index at 0x3af9c2b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 44>:
#  44           0 RESUME                   0
# 
#  45           2 LOAD_GLOBAL              1 (NULL + HDF5ExportSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  46          22 LOAD_GLOBAL              3 (NULL + tempfile)
#              32 LOAD_ATTR                4 (TemporaryDirectory)
#              52 CALL                     0
#              60 BEFORE_WITH
#              62 STORE_FAST               2 (tmpdir)
# 
#  47          64 LOAD_GLOBAL              7 (NULL + Path)
#              74 LOAD_FAST                2 (tmpdir)
#              76 CALL                     1
#              84 LOAD_CONST               1 ('test.h5')
#              86 BINARY_OP               11 (/)
#              90 STORE_FAST               3 (hdf5_path)
# 
#  48          92 LOAD_GLOBAL              9 (NULL + h5py)
#             102 LOAD_ATTR               10 (File)
#             122 LOAD_FAST                3 (hdf5_path)
#             124 LOAD_CONST               2 ('w')
#             126 CALL                     2
#             134 BEFORE_WITH
#             136 STORE_FAST               4 (f)
# 
#  49         138 LOAD_FAST                4 (f)
#             140 LOAD_ATTR               13 (NULL|self + create_dataset)
#             160 LOAD_CONST               3 ('data')
#             162 LOAD_GLOBAL             15 (NULL + np)
#             172 LOAD_ATTR               16 (zeros)
#             192 LOAD_CONST               4 (10)
#             194 CALL                     1
#             202 KW_NAMES                 5 (('data',))
#             204 CALL                     2
#             212 POP_TOP
# 
#  48         214 LOAD_CONST               0 (None)
#             216 LOAD_CONST               0 (None)
#             218 LOAD_CONST               0 (None)
#             220 CALL                     2
#             228 POP_TOP
# 
#  50     >>  230 LOAD_FAST                1 (skill)
#             232 LOAD_ATTR               19 (NULL|self + _create_index)
#             252 LOAD_FAST                3 (hdf5_path)
#             254 CALL                     1
#             262 STORE_FAST               5 (index)
# 
#  51         264 LOAD_FAST                5 (index)
#             266 LOAD_CONST               6 ('datasets')
#             268 BINARY_SUBSCR
#             272 STORE_FAST               6 (@py_assert1)
#             274 LOAD_GLOBAL             21 (NULL + len)
#             284 LOAD_FAST                6 (@py_assert1)
#             286 CALL                     1
#             294 STORE_FAST               7 (@py_assert3)
#             296 LOAD_CONST               7 (1)
#             298 STORE_FAST               8 (@py_assert6)
#             300 LOAD_FAST                7 (@py_assert3)
#             302 LOAD_FAST                8 (@py_assert6)
#             304 COMPARE_OP              40 (==)
#             308 STORE_FAST               9 (@py_assert5)
#             310 LOAD_FAST                9 (@py_assert5)
#             312 POP_JUMP_IF_TRUE       201 (to 716)
#             314 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             324 LOAD_ATTR               24 (_call_reprcompare)
#             344 LOAD_CONST               8 (('==',))
#             346 LOAD_FAST                9 (@py_assert5)
#             348 BUILD_TUPLE              1
#             350 LOAD_CONST               9 (('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s',))
#             352 LOAD_FAST                7 (@py_assert3)
#             354 LOAD_FAST                8 (@py_assert6)
#             356 BUILD_TUPLE              2
#             358 CALL                     4
#             366 LOAD_CONST              10 ('len')
#             368 LOAD_GLOBAL             27 (NULL + @py_builtins)
#             378 LOAD_ATTR               28 (locals)
#             398 CALL                     0
#             406 CONTAINS_OP              0
#             408 POP_JUMP_IF_TRUE        25 (to 460)
#             410 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             420 LOAD_ATTR               30 (_should_repr_global_name)
#             440 LOAD_GLOBAL             20 (len)
#             450 CALL                     1
#             458 POP_JUMP_IF_FALSE       25 (to 510)
#         >>  460 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             470 LOAD_ATTR               32 (_saferepr)
#             490 LOAD_GLOBAL             20 (len)
#             500 CALL                     1
#             508 JUMP_FORWARD             1 (to 512)
#         >>  510 LOAD_CONST              10 ('len')
#         >>  512 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             522 LOAD_ATTR               32 (_saferepr)
#             542 LOAD_FAST                6 (@py_assert1)
#             544 CALL                     1
#             552 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             562 LOAD_ATTR               32 (_saferepr)
#             582 LOAD_FAST                7 (@py_assert3)
#             584 CALL                     1
#             592 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             602 LOAD_ATTR               32 (_saferepr)
#             622 LOAD_FAST                8 (@py_assert6)
#             624 CALL                     1
#             632 LOAD_CONST              11 (('py0', 'py2', 'py4', 'py7'))
#             634 BUILD_CONST_KEY_MAP      4
#             636 BINARY_OP                6 (%)
#             640 STORE_FAST              10 (@py_format8)
#             642 LOAD_CONST              12 ('assert %(py9)s')
#             644 LOAD_CONST              13 ('py9')
#             646 LOAD_FAST               10 (@py_format8)
#             648 BUILD_MAP                1
#             650 BINARY_OP                6 (%)
#             654 STORE_FAST              11 (@py_format10)
#             656 LOAD_GLOBAL             35 (NULL + AssertionError)
#             666 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             676 LOAD_ATTR               36 (_format_explanation)
#             696 LOAD_FAST               11 (@py_format10)
#             698 CALL                     1
#             706 CALL                     1
#             714 RAISE_VARARGS            1
#         >>  716 LOAD_CONST               0 (None)
#             718 COPY                     1
#             720 STORE_FAST               6 (@py_assert1)
#             722 COPY                     1
#             724 STORE_FAST               7 (@py_assert3)
#             726 COPY                     1
#             728 STORE_FAST               9 (@py_assert5)
#             730 STORE_FAST               8 (@py_assert6)
# 
#  52         732 LOAD_FAST                5 (index)
#             734 LOAD_CONST               6 ('datasets')
#             736 BINARY_SUBSCR
#             740 LOAD_CONST              14 (0)
#             742 BINARY_SUBSCR
#             746 LOAD_CONST              15 ('path')
#             748 BINARY_SUBSCR
#             752 STORE_FAST              12 (@py_assert0)
#             754 LOAD_CONST               3 ('data')
#             756 STORE_FAST               7 (@py_assert3)
#             758 LOAD_FAST               12 (@py_assert0)
#             760 LOAD_FAST                7 (@py_assert3)
#             762 COMPARE_OP              40 (==)
#             766 STORE_FAST              13 (@py_assert2)
#             768 LOAD_FAST               13 (@py_assert2)
#             770 POP_JUMP_IF_TRUE       108 (to 988)
#             772 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             782 LOAD_ATTR               24 (_call_reprcompare)
#             802 LOAD_CONST               8 (('==',))
#             804 LOAD_FAST               13 (@py_assert2)
#             806 BUILD_TUPLE              1
#             808 LOAD_CONST              16 (('%(py1)s == %(py4)s',))
#             810 LOAD_FAST               12 (@py_assert0)
#             812 LOAD_FAST                7 (@py_assert3)
#             814 BUILD_TUPLE              2
#             816 CALL                     4
#             824 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             834 LOAD_ATTR               32 (_saferepr)
#             854 LOAD_FAST               12 (@py_assert0)
#             856 CALL                     1
#             864 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             874 LOAD_ATTR               32 (_saferepr)
#             894 LOAD_FAST                7 (@py_assert3)
#             896 CALL                     1
#             904 LOAD_CONST              17 (('py1', 'py4'))
#             906 BUILD_CONST_KEY_MAP      2
#             908 BINARY_OP                6 (%)
#             912 STORE_FAST              14 (@py_format5)
#             914 LOAD_CONST              18 ('assert %(py6)s')
#             916 LOAD_CONST              19 ('py6')
#             918 LOAD_FAST               14 (@py_format5)
#             920 BUILD_MAP                1
#             922 BINARY_OP                6 (%)
#             926 STORE_FAST              15 (@py_format7)
#             928 LOAD_GLOBAL             35 (NULL + AssertionError)
#             938 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             948 LOAD_ATTR               36 (_format_explanation)
#             968 LOAD_FAST               15 (@py_format7)
#             970 CALL                     1
#             978 CALL                     1
#             986 RAISE_VARARGS            1
#         >>  988 LOAD_CONST               0 (None)
#             990 COPY                     1
#             992 STORE_FAST              12 (@py_assert0)
#             994 COPY                     1
#             996 STORE_FAST              13 (@py_assert2)
#             998 STORE_FAST               7 (@py_assert3)
# 
#  46        1000 LOAD_CONST               0 (None)
#            1002 LOAD_CONST               0 (None)
#            1004 LOAD_CONST               0 (None)
#            1006 CALL                     2
#            1014 POP_TOP
#            1016 RETURN_CONST             0 (None)
# 
#  48     >> 1018 PUSH_EXC_INFO
#            1020 WITH_EXCEPT_START
#            1022 POP_JUMP_IF_TRUE         1 (to 1026)
#            1024 RERAISE                  2
#         >> 1026 POP_TOP
#            1028 POP_EXCEPT
#            1030 POP_TOP
#            1032 POP_TOP
#            1034 EXTENDED_ARG             1
#            1036 JUMP_BACKWARD          404 (to 230)
#         >> 1038 COPY                     3
#            1040 POP_EXCEPT
#            1042 RERAISE                  1
# 
#  46     >> 1044 PUSH_EXC_INFO
#            1046 WITH_EXCEPT_START
#            1048 POP_JUMP_IF_TRUE         1 (to 1052)
#            1050 RERAISE                  2
#         >> 1052 POP_TOP
#            1054 POP_EXCEPT
#            1056 POP_TOP
#            1058 POP_TOP
#            1060 RETURN_CONST             0 (None)
#         >> 1062 COPY                     3
#            1064 POP_EXCEPT
#            1066 RERAISE                  1
# ExceptionTable:
#   62 to 134 -> 1044 [1] lasti
#   136 to 212 -> 1018 [2] lasti
#   214 to 998 -> 1044 [1] lasti
#   1018 to 1026 -> 1038 [4] lasti
#   1028 to 1042 -> 1044 [1] lasti
#   1044 to 1052 -> 1062 [3] lasti
# 
# Disassembly of <code object TestHDF5Read at 0x73cd945fdfb0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 55>:
#  55           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestHDF5Read')
#               8 STORE_NAME               2 (__qualname__)
# 
#  56          10 LOAD_CONST               1 (<code object test_read_hdf5 at 0x3af981b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 56>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_read_hdf5)
# 
#  66          16 LOAD_CONST               2 (<code object test_list_datasets at 0x3afa6690, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 66>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_list_datasets)
#              22 RETURN_CONST             3 (None)
# 
# Disassembly of <code object test_read_hdf5 at 0x3af981b0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 56>:
#  56           0 RESUME                   0
# 
#  57           2 LOAD_GLOBAL              1 (NULL + tempfile)
#              12 LOAD_ATTR                2 (TemporaryDirectory)
#              32 CALL                     0
#              40 BEFORE_WITH
#              42 STORE_FAST               1 (tmpdir)
# 
#  58          44 LOAD_GLOBAL              5 (NULL + Path)
#              54 LOAD_FAST                1 (tmpdir)
#              56 CALL                     1
#              64 LOAD_CONST               1 ('test.h5')
#              66 BINARY_OP               11 (/)
#              70 STORE_FAST               2 (hdf5_path)
# 
#  59          72 LOAD_GLOBAL              7 (NULL + h5py)
#              82 LOAD_ATTR                8 (File)
#             102 LOAD_FAST                2 (hdf5_path)
#             104 LOAD_CONST               2 ('w')
#             106 CALL                     2
#             114 BEFORE_WITH
#             116 STORE_FAST               3 (f)
# 
#  60         118 LOAD_FAST                3 (f)
#             120 LOAD_ATTR               11 (NULL|self + create_dataset)
#             140 LOAD_CONST               3 ('arr')
#             142 LOAD_GLOBAL             13 (NULL + np)
#             152 LOAD_ATTR               14 (array)
#             172 BUILD_LIST               0
#             174 LOAD_CONST               4 ((1, 2, 3))
#             176 LIST_EXTEND              1
#             178 CALL                     1
#             186 KW_NAMES                 5 (('data',))
#             188 CALL                     2
#             196 POP_TOP
# 
#  61         198 LOAD_CONST               6 ('value')
#             200 LOAD_FAST                3 (f)
#             202 LOAD_ATTR               16 (attrs)
#             222 LOAD_CONST               7 ('key')
#             224 STORE_SUBSCR
# 
#  59         228 LOAD_CONST               0 (None)
#             230 LOAD_CONST               0 (None)
#             232 LOAD_CONST               0 (None)
#             234 CALL                     2
#             242 POP_TOP
# 
#  62     >>  244 LOAD_GLOBAL             19 (NULL + HDF5ExportSkill)
#             254 LOAD_ATTR               20 (read_hdf5)
#             274 LOAD_GLOBAL             23 (NULL + str)
#             284 LOAD_FAST                2 (hdf5_path)
#             286 CALL                     1
#             294 CALL                     1
#             302 STORE_FAST               4 (result)
# 
#  63         304 LOAD_CONST               3 ('arr')
#             306 STORE_FAST               5 (@py_assert0)
#             308 LOAD_FAST                5 (@py_assert0)
#             310 LOAD_FAST                4 (result)
#             312 CONTAINS_OP              0
#             314 STORE_FAST               6 (@py_assert2)
#             316 LOAD_FAST                6 (@py_assert2)
#             318 POP_JUMP_IF_TRUE       153 (to 626)
#             320 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             330 LOAD_ATTR               26 (_call_reprcompare)
#             350 LOAD_CONST               8 (('in',))
#             352 LOAD_FAST                6 (@py_assert2)
#             354 BUILD_TUPLE              1
#             356 LOAD_CONST               9 (('%(py1)s in %(py3)s',))
#             358 LOAD_FAST                5 (@py_assert0)
#             360 LOAD_FAST                4 (result)
#             362 BUILD_TUPLE              2
#             364 CALL                     4
#             372 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             382 LOAD_ATTR               28 (_saferepr)
#             402 LOAD_FAST                5 (@py_assert0)
#             404 CALL                     1
#             412 LOAD_CONST              10 ('result')
#             414 LOAD_GLOBAL             31 (NULL + @py_builtins)
#             424 LOAD_ATTR               32 (locals)
#             444 CALL                     0
#             452 CONTAINS_OP              0
#             454 POP_JUMP_IF_TRUE        21 (to 498)
#             456 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             466 LOAD_ATTR               34 (_should_repr_global_name)
#             486 LOAD_FAST                4 (result)
#             488 CALL                     1
#             496 POP_JUMP_IF_FALSE       21 (to 540)
#         >>  498 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             508 LOAD_ATTR               28 (_saferepr)
#             528 LOAD_FAST                4 (result)
#             530 CALL                     1
#             538 JUMP_FORWARD             1 (to 542)
#         >>  540 LOAD_CONST              10 ('result')
#         >>  542 LOAD_CONST              11 (('py1', 'py3'))
#             544 BUILD_CONST_KEY_MAP      2
#             546 BINARY_OP                6 (%)
#             550 STORE_FAST               7 (@py_format4)
#             552 LOAD_CONST              12 ('assert %(py5)s')
#             554 LOAD_CONST              13 ('py5')
#             556 LOAD_FAST                7 (@py_format4)
#             558 BUILD_MAP                1
#             560 BINARY_OP                6 (%)
#             564 STORE_FAST               8 (@py_format6)
#             566 LOAD_GLOBAL             37 (NULL + AssertionError)
#             576 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             586 LOAD_ATTR               38 (_format_explanation)
#             606 LOAD_FAST                8 (@py_format6)
#             608 CALL                     1
#             616 CALL                     1
#             624 RAISE_VARARGS            1
#         >>  626 LOAD_CONST               0 (None)
#             628 COPY                     1
#             630 STORE_FAST               5 (@py_assert0)
#             632 STORE_FAST               6 (@py_assert2)
# 
#  64         634 LOAD_GLOBAL             12 (np)
#             644 LOAD_ATTR               40 (testing)
#             664 LOAD_ATTR               43 (NULL|self + assert_array_equal)
#             684 LOAD_FAST                4 (result)
#             686 LOAD_CONST               3 ('arr')
#             688 BINARY_SUBSCR
#             692 BUILD_LIST               0
#             694 LOAD_CONST               4 ((1, 2, 3))
#             696 LIST_EXTEND              1
#             698 CALL                     2
#             706 POP_TOP
# 
#  57         708 LOAD_CONST               0 (None)
#             710 LOAD_CONST               0 (None)
#             712 LOAD_CONST               0 (None)
#             714 CALL                     2
#             722 POP_TOP
#             724 RETURN_CONST             0 (None)
# 
#  59     >>  726 PUSH_EXC_INFO
#             728 WITH_EXCEPT_START
#             730 POP_JUMP_IF_TRUE         1 (to 734)
#             732 RERAISE                  2
#         >>  734 POP_TOP
#             736 POP_EXCEPT
#             738 POP_TOP
#             740 POP_TOP
#             742 JUMP_BACKWARD          250 (to 244)
#         >>  744 COPY                     3
#             746 POP_EXCEPT
#             748 RERAISE                  1
# 
#  57     >>  750 PUSH_EXC_INFO
#             752 WITH_EXCEPT_START
#             754 POP_JUMP_IF_TRUE         1 (to 758)
#             756 RERAISE                  2
#         >>  758 POP_TOP
#             760 POP_EXCEPT
#             762 POP_TOP
#             764 POP_TOP
#             766 RETURN_CONST             0 (None)
#         >>  768 COPY                     3
#             770 POP_EXCEPT
#             772 RERAISE                  1
# ExceptionTable:
#   42 to 114 -> 750 [1] lasti
#   116 to 226 -> 726 [2] lasti
#   228 to 706 -> 750 [1] lasti
#   726 to 734 -> 744 [4] lasti
#   736 to 748 -> 750 [1] lasti
#   750 to 758 -> 768 [3] lasti
# 
# Disassembly of <code object test_list_datasets at 0x3afa6690, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 66>:
#  66           0 RESUME                   0
# 
#  67           2 LOAD_GLOBAL              1 (NULL + tempfile)
#              12 LOAD_ATTR                2 (TemporaryDirectory)
#              32 CALL                     0
#              40 BEFORE_WITH
#              42 STORE_FAST               1 (tmpdir)
# 
#  68          44 LOAD_GLOBAL              5 (NULL + Path)
#              54 LOAD_FAST                1 (tmpdir)
#              56 CALL                     1
#              64 LOAD_CONST               1 ('test.h5')
#              66 BINARY_OP               11 (/)
#              70 STORE_FAST               2 (hdf5_path)
# 
#  69          72 LOAD_GLOBAL              7 (NULL + h5py)
#              82 LOAD_ATTR                8 (File)
#             102 LOAD_FAST                2 (hdf5_path)
#             104 LOAD_CONST               2 ('w')
#             106 CALL                     2
#             114 BEFORE_WITH
#             116 STORE_FAST               3 (f)
# 
#  70         118 LOAD_FAST                3 (f)
#             120 LOAD_ATTR               11 (NULL|self + create_dataset)
#             140 LOAD_CONST               3 ('a')
#             142 LOAD_CONST               4 (1)
#             144 BUILD_LIST               1
#             146 KW_NAMES                 5 (('data',))
#             148 CALL                     2
#             156 POP_TOP
# 
#  71         158 LOAD_FAST                3 (f)
#             160 LOAD_ATTR               13 (NULL|self + create_group)
#             180 LOAD_CONST               6 ('sub')
#             182 CALL                     1
#             190 STORE_FAST               4 (g)
# 
#  72         192 LOAD_FAST                4 (g)
#             194 LOAD_ATTR               11 (NULL|self + create_dataset)
#             214 LOAD_CONST               7 ('b')
#             216 LOAD_CONST               8 (2)
#             218 BUILD_LIST               1
#             220 KW_NAMES                 5 (('data',))
#             222 CALL                     2
#             230 POP_TOP
# 
#  69         232 LOAD_CONST               0 (None)
#             234 LOAD_CONST               0 (None)
#             236 LOAD_CONST               0 (None)
#             238 CALL                     2
#             246 POP_TOP
# 
#  73     >>  248 LOAD_GLOBAL             15 (NULL + HDF5ExportSkill)
#             258 LOAD_ATTR               16 (list_datasets)
#             278 LOAD_GLOBAL             19 (NULL + str)
#             288 LOAD_FAST                2 (hdf5_path)
#             290 CALL                     1
#             298 CALL                     1
#             306 STORE_FAST               5 (datasets)
# 
#  74         308 LOAD_CONST               3 ('a')
#             310 STORE_FAST               6 (@py_assert0)
#             312 LOAD_FAST                6 (@py_assert0)
#             314 LOAD_FAST                5 (datasets)
#             316 CONTAINS_OP              0
#             318 STORE_FAST               7 (@py_assert2)
#             320 LOAD_FAST                7 (@py_assert2)
#             322 POP_JUMP_IF_TRUE       153 (to 630)
#             324 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             334 LOAD_ATTR               22 (_call_reprcompare)
#             354 LOAD_CONST               9 (('in',))
#             356 LOAD_FAST                7 (@py_assert2)
#             358 BUILD_TUPLE              1
#             360 LOAD_CONST              10 (('%(py1)s in %(py3)s',))
#             362 LOAD_FAST                6 (@py_assert0)
#             364 LOAD_FAST                5 (datasets)
#             366 BUILD_TUPLE              2
#             368 CALL                     4
#             376 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             386 LOAD_ATTR               24 (_saferepr)
#             406 LOAD_FAST                6 (@py_assert0)
#             408 CALL                     1
#             416 LOAD_CONST              11 ('datasets')
#             418 LOAD_GLOBAL             27 (NULL + @py_builtins)
#             428 LOAD_ATTR               28 (locals)
#             448 CALL                     0
#             456 CONTAINS_OP              0
#             458 POP_JUMP_IF_TRUE        21 (to 502)
#             460 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             470 LOAD_ATTR               30 (_should_repr_global_name)
#             490 LOAD_FAST                5 (datasets)
#             492 CALL                     1
#             500 POP_JUMP_IF_FALSE       21 (to 544)
#         >>  502 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             512 LOAD_ATTR               24 (_saferepr)
#             532 LOAD_FAST                5 (datasets)
#             534 CALL                     1
#             542 JUMP_FORWARD             1 (to 546)
#         >>  544 LOAD_CONST              11 ('datasets')
#         >>  546 LOAD_CONST              12 (('py1', 'py3'))
#             548 BUILD_CONST_KEY_MAP      2
#             550 BINARY_OP                6 (%)
#             554 STORE_FAST               8 (@py_format4)
#             556 LOAD_CONST              13 ('assert %(py5)s')
#             558 LOAD_CONST              14 ('py5')
#             560 LOAD_FAST                8 (@py_format4)
#             562 BUILD_MAP                1
#             564 BINARY_OP                6 (%)
#             568 STORE_FAST               9 (@py_format6)
#             570 LOAD_GLOBAL             33 (NULL + AssertionError)
#             580 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             590 LOAD_ATTR               34 (_format_explanation)
#             610 LOAD_FAST                9 (@py_format6)
#             612 CALL                     1
#             620 CALL                     1
#             628 RAISE_VARARGS            1
#         >>  630 LOAD_CONST               0 (None)
#             632 COPY                     1
#             634 STORE_FAST               6 (@py_assert0)
#             636 STORE_FAST               7 (@py_assert2)
# 
#  75         638 LOAD_CONST              15 ('sub/b')
#             640 STORE_FAST               6 (@py_assert0)
#             642 LOAD_FAST                6 (@py_assert0)
#             644 LOAD_FAST                5 (datasets)
#             646 CONTAINS_OP              0
#             648 STORE_FAST               7 (@py_assert2)
#             650 LOAD_FAST                7 (@py_assert2)
#             652 POP_JUMP_IF_TRUE       153 (to 960)
#             654 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             664 LOAD_ATTR               22 (_call_reprcompare)
#             684 LOAD_CONST               9 (('in',))
#             686 LOAD_FAST                7 (@py_assert2)
#             688 BUILD_TUPLE              1
#             690 LOAD_CONST              10 (('%(py1)s in %(py3)s',))
#             692 LOAD_FAST                6 (@py_assert0)
#             694 LOAD_FAST                5 (datasets)
#             696 BUILD_TUPLE              2
#             698 CALL                     4
#             706 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             716 LOAD_ATTR               24 (_saferepr)
#             736 LOAD_FAST                6 (@py_assert0)
#             738 CALL                     1
#             746 LOAD_CONST              11 ('datasets')
#             748 LOAD_GLOBAL             27 (NULL + @py_builtins)
#             758 LOAD_ATTR               28 (locals)
#             778 CALL                     0
#             786 CONTAINS_OP              0
#             788 POP_JUMP_IF_TRUE        21 (to 832)
#             790 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             800 LOAD_ATTR               30 (_should_repr_global_name)
#             820 LOAD_FAST                5 (datasets)
#             822 CALL                     1
#             830 POP_JUMP_IF_FALSE       21 (to 874)
#         >>  832 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             842 LOAD_ATTR               24 (_saferepr)
#             862 LOAD_FAST                5 (datasets)
#             864 CALL                     1
#             872 JUMP_FORWARD             1 (to 876)
#         >>  874 LOAD_CONST              11 ('datasets')
#         >>  876 LOAD_CONST              12 (('py1', 'py3'))
#             878 BUILD_CONST_KEY_MAP      2
#             880 BINARY_OP                6 (%)
#             884 STORE_FAST               8 (@py_format4)
#             886 LOAD_CONST              13 ('assert %(py5)s')
#             888 LOAD_CONST              14 ('py5')
#             890 LOAD_FAST                8 (@py_format4)
#             892 BUILD_MAP                1
#             894 BINARY_OP                6 (%)
#             898 STORE_FAST               9 (@py_format6)
#             900 LOAD_GLOBAL             33 (NULL + AssertionError)
#             910 LOAD_GLOBAL             21 (NULL + @pytest_ar)
#             920 LOAD_ATTR               34 (_format_explanation)
#             940 LOAD_FAST                9 (@py_format6)
#             942 CALL                     1
#             950 CALL                     1
#             958 RAISE_VARARGS            1
#         >>  960 LOAD_CONST               0 (None)
#             962 COPY                     1
#             964 STORE_FAST               6 (@py_assert0)
#             966 STORE_FAST               7 (@py_assert2)
# 
#  67         968 LOAD_CONST               0 (None)
#             970 LOAD_CONST               0 (None)
#             972 LOAD_CONST               0 (None)
#             974 CALL                     2
#             982 POP_TOP
#             984 RETURN_CONST             0 (None)
# 
#  69     >>  986 PUSH_EXC_INFO
#             988 WITH_EXCEPT_START
#             990 POP_JUMP_IF_TRUE         1 (to 994)
#             992 RERAISE                  2
#         >>  994 POP_TOP
#             996 POP_EXCEPT
#             998 POP_TOP
#            1000 POP_TOP
#            1002 EXTENDED_ARG             1
#            1004 JUMP_BACKWARD          379 (to 248)
#         >> 1006 COPY                     3
#            1008 POP_EXCEPT
#            1010 RERAISE                  1
# 
#  67     >> 1012 PUSH_EXC_INFO
#            1014 WITH_EXCEPT_START
#            1016 POP_JUMP_IF_TRUE         1 (to 1020)
#            1018 RERAISE                  2
#         >> 1020 POP_TOP
#            1022 POP_EXCEPT
#            1024 POP_TOP
#            1026 POP_TOP
#            1028 RETURN_CONST             0 (None)
#         >> 1030 COPY                     3
#            1032 POP_EXCEPT
#            1034 RERAISE                  1
# ExceptionTable:
#   42 to 114 -> 1012 [1] lasti
#   116 to 230 -> 986 [2] lasti
#   232 to 966 -> 1012 [1] lasti
#   986 to 994 -> 1006 [4] lasti
#   996 to 1010 -> 1012 [1] lasti
#   1012 to 1020 -> 1030 [3] lasti
# 
# Disassembly of <code object TestHDF5Run at 0x73cd945ff210, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 78>:
#  78           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestHDF5Run')
#               8 STORE_NAME               2 (__qualname__)
# 
#  79          10 LOAD_CONST               1 (<code object test_run_invalid_config_returns_failure at 0x3af9ee00, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 79>)
#              12 MAKE_FUNCTION            0
#              14 STORE_NAME               3 (test_run_invalid_config_returns_failure)
# 
#  84          16 LOAD_CONST               2 (<code object test_run_file_export at 0x3afa9110, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 84>)
#              18 MAKE_FUNCTION            0
#              20 STORE_NAME               4 (test_run_file_export)
#              22 RETURN_CONST             3 (None)
# 
# Disassembly of <code object test_run_invalid_config_returns_failure at 0x3af9ee00, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 79>:
#  79           0 RESUME                   0
# 
#  80           2 LOAD_GLOBAL              1 (NULL + HDF5ExportSkill)
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
# Disassembly of <code object test_run_file_export at 0x3afa9110, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_hdf5_export.py", line 84>:
#  84           0 RESUME                   0
# 
#  85           2 LOAD_GLOBAL              1 (NULL + HDF5ExportSkill)
#              12 CALL                     0
#              20 STORE_FAST               1 (skill)
# 
#  86          22 LOAD_GLOBAL              3 (NULL + tempfile)
#              32 LOAD_ATTR                4 (TemporaryDirectory)
#              52 CALL                     0
#              60 BEFORE_WITH
#              62 STORE_FAST               2 (tmpdir)
# 
#  87          64 LOAD_GLOBAL              7 (NULL + Path)
#              74 LOAD_FAST                2 (tmpdir)
#              76 CALL                     1
#              84 LOAD_CONST               1 ('input.json')
#              86 BINARY_OP               11 (/)
#              90 STORE_FAST               3 (json_path)
# 
#  88          92 LOAD_FAST                3 (json_path)
#              94 LOAD_ATTR                9 (NULL|self + write_text)
#             114 LOAD_GLOBAL             11 (NULL + json)
#             124 LOAD_ATTR               12 (dumps)
#             144 LOAD_CONST               2 ('test')
#             146 LOAD_CONST               3 ('demo')
#             148 LOAD_CONST               4 (('type', 'name'))
#             150 BUILD_CONST_KEY_MAP      2
#             152 CALL                     1
#             160 CALL                     1
#             168 POP_TOP
# 
#  90         170 LOAD_CONST               5 ('file')
#             172 LOAD_GLOBAL             15 (NULL + str)
#             182 LOAD_FAST                3 (json_path)
#             184 CALL                     1
#             192 LOAD_CONST               6 (('type', 'file_path'))
#             194 BUILD_CONST_KEY_MAP      2
# 
#  91         196 LOAD_FAST                2 (tmpdir)
#             198 LOAD_CONST               7 ('output')
#             200 LOAD_CONST               8 (('path', 'filename'))
#             202 BUILD_CONST_KEY_MAP      2
# 
#  89         204 LOAD_CONST               9 (('source', 'output'))
#             206 BUILD_CONST_KEY_MAP      2
#             208 STORE_FAST               4 (config)
# 
#  93         210 LOAD_FAST                1 (skill)
#             212 LOAD_ATTR               17 (NULL|self + run)
#             232 LOAD_FAST                4 (config)
#             234 CALL                     1
#             242 STORE_FAST               5 (result)
# 
#  94         244 LOAD_FAST                5 (result)
#             246 LOAD_ATTR               18 (status)
#             266 STORE_FAST               6 (@py_assert1)
#             268 LOAD_FAST                6 (@py_assert1)
#             270 LOAD_ATTR               20 (value)
#             290 STORE_FAST               7 (@py_assert3)
#             292 LOAD_CONST              10 ('SUCCESS')
#             294 LOAD_CONST              11 ('success')
#             296 BUILD_LIST               2
#             298 STORE_FAST               8 (@py_assert6)
#             300 LOAD_FAST                7 (@py_assert3)
#             302 LOAD_FAST                8 (@py_assert6)
#             304 CONTAINS_OP              0
#             306 STORE_FAST               9 (@py_assert5)
#             308 LOAD_FAST                9 (@py_assert5)
#             310 POP_JUMP_IF_TRUE       193 (to 698)
#             312 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             322 LOAD_ATTR               24 (_call_reprcompare)
#             342 LOAD_CONST              12 (('in',))
#             344 LOAD_FAST                9 (@py_assert5)
#             346 BUILD_TUPLE              1
#             348 LOAD_CONST              13 (('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.status\n}.value\n} in %(py7)s',))
#             350 LOAD_FAST                7 (@py_assert3)
#             352 LOAD_FAST                8 (@py_assert6)
#             354 BUILD_TUPLE              2
#             356 CALL                     4
#             364 LOAD_CONST              14 ('result')
#             366 LOAD_GLOBAL             27 (NULL + @py_builtins)
#             376 LOAD_ATTR               28 (locals)
#             396 CALL                     0
#             404 CONTAINS_OP              0
#             406 POP_JUMP_IF_TRUE        21 (to 450)
#             408 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             418 LOAD_ATTR               30 (_should_repr_global_name)
#             438 LOAD_FAST                5 (result)
#             440 CALL                     1
#             448 POP_JUMP_IF_FALSE       21 (to 492)
#         >>  450 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             460 LOAD_ATTR               32 (_saferepr)
#             480 LOAD_FAST                5 (result)
#             482 CALL                     1
#             490 JUMP_FORWARD             1 (to 494)
#         >>  492 LOAD_CONST              14 ('result')
#         >>  494 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             504 LOAD_ATTR               32 (_saferepr)
#             524 LOAD_FAST                6 (@py_assert1)
#             526 CALL                     1
#             534 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             544 LOAD_ATTR               32 (_saferepr)
#             564 LOAD_FAST                7 (@py_assert3)
#             566 CALL                     1
#             574 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             584 LOAD_ATTR               32 (_saferepr)
#             604 LOAD_FAST                8 (@py_assert6)
#             606 CALL                     1
#             614 LOAD_CONST              15 (('py0', 'py2', 'py4', 'py7'))
#             616 BUILD_CONST_KEY_MAP      4
#             618 BINARY_OP                6 (%)
#             622 STORE_FAST              10 (@py_format8)
#             624 LOAD_CONST              16 ('assert %(py9)s')
#             626 LOAD_CONST              17 ('py9')
#             628 LOAD_FAST               10 (@py_format8)
#             630 BUILD_MAP                1
#             632 BINARY_OP                6 (%)
#             636 STORE_FAST              11 (@py_format10)
#             638 LOAD_GLOBAL             35 (NULL + AssertionError)
#             648 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             658 LOAD_ATTR               36 (_format_explanation)
#             678 LOAD_FAST               11 (@py_format10)
#             680 CALL                     1
#             688 CALL                     1
#             696 RAISE_VARARGS            1
#         >>  698 LOAD_CONST               0 (None)
#             700 COPY                     1
#             702 STORE_FAST               6 (@py_assert1)
#             704 COPY                     1
#             706 STORE_FAST               7 (@py_assert3)
#             708 COPY                     1
#             710 STORE_FAST               9 (@py_assert5)
#             712 STORE_FAST               8 (@py_assert6)
# 
#  95         714 LOAD_FAST                5 (result)
#             716 LOAD_ATTR               38 (artifacts)
#             736 STORE_FAST              12 (@py_assert2)
#             738 LOAD_GLOBAL             41 (NULL + len)
#             748 LOAD_FAST               12 (@py_assert2)
#             750 CALL                     1
#             758 STORE_FAST              13 (@py_assert4)
#             760 LOAD_CONST              18 (1)
#             762 STORE_FAST              14 (@py_assert7)
#             764 LOAD_FAST               13 (@py_assert4)
#             766 LOAD_FAST               14 (@py_assert7)
#             768 COMPARE_OP              92 (>=)
#             772 STORE_FAST               8 (@py_assert6)
#             774 LOAD_FAST                8 (@py_assert6)
#             776 EXTENDED_ARG             1
#             778 POP_JUMP_IF_TRUE       266 (to 1312)
#             780 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             790 LOAD_ATTR               24 (_call_reprcompare)
#             810 LOAD_CONST              19 (('>=',))
#             812 LOAD_FAST                8 (@py_assert6)
#             814 BUILD_TUPLE              1
#             816 LOAD_CONST              20 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.artifacts\n})\n} >= %(py8)s',))
#             818 LOAD_FAST               13 (@py_assert4)
#             820 LOAD_FAST               14 (@py_assert7)
#             822 BUILD_TUPLE              2
#             824 CALL                     4
#             832 LOAD_CONST              21 ('len')
#             834 LOAD_GLOBAL             27 (NULL + @py_builtins)
#             844 LOAD_ATTR               28 (locals)
#             864 CALL                     0
#             872 CONTAINS_OP              0
#             874 POP_JUMP_IF_TRUE        25 (to 926)
#             876 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             886 LOAD_ATTR               30 (_should_repr_global_name)
#             906 LOAD_GLOBAL             40 (len)
#             916 CALL                     1
#             924 POP_JUMP_IF_FALSE       25 (to 976)
#         >>  926 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#             936 LOAD_ATTR               32 (_saferepr)
#             956 LOAD_GLOBAL             40 (len)
#             966 CALL                     1
#             974 JUMP_FORWARD             1 (to 978)
#         >>  976 LOAD_CONST              21 ('len')
#         >>  978 LOAD_CONST              14 ('result')
#             980 LOAD_GLOBAL             27 (NULL + @py_builtins)
#             990 LOAD_ATTR               28 (locals)
#            1010 CALL                     0
#            1018 CONTAINS_OP              0
#            1020 POP_JUMP_IF_TRUE        21 (to 1064)
#            1022 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#            1032 LOAD_ATTR               30 (_should_repr_global_name)
#            1052 LOAD_FAST                5 (result)
#            1054 CALL                     1
#            1062 POP_JUMP_IF_FALSE       21 (to 1106)
#         >> 1064 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#            1074 LOAD_ATTR               32 (_saferepr)
#            1094 LOAD_FAST                5 (result)
#            1096 CALL                     1
#            1104 JUMP_FORWARD             1 (to 1108)
#         >> 1106 LOAD_CONST              14 ('result')
#         >> 1108 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#            1118 LOAD_ATTR               32 (_saferepr)
#            1138 LOAD_FAST               12 (@py_assert2)
#            1140 CALL                     1
#            1148 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#            1158 LOAD_ATTR               32 (_saferepr)
#            1178 LOAD_FAST               13 (@py_assert4)
#            1180 CALL                     1
#            1188 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#            1198 LOAD_ATTR               32 (_saferepr)
#            1218 LOAD_FAST               14 (@py_assert7)
#            1220 CALL                     1
#            1228 LOAD_CONST              22 (('py0', 'py1', 'py3', 'py5', 'py8'))
#            1230 BUILD_CONST_KEY_MAP      5
#            1232 BINARY_OP                6 (%)
#            1236 STORE_FAST              15 (@py_format9)
#            1238 LOAD_CONST              23 ('assert %(py10)s')
#            1240 LOAD_CONST              24 ('py10')
#            1242 LOAD_FAST               15 (@py_format9)
#            1244 BUILD_MAP                1
#            1246 BINARY_OP                6 (%)
#            1250 STORE_FAST              16 (@py_format11)
#            1252 LOAD_GLOBAL             35 (NULL + AssertionError)
#            1262 LOAD_GLOBAL             23 (NULL + @pytest_ar)
#            1272 LOAD_ATTR               36 (_format_explanation)
#            1292 LOAD_FAST               16 (@py_format11)
#            1294 CALL                     1
#            1302 CALL                     1
#            1310 RAISE_VARARGS            1
#         >> 1312 LOAD_CONST               0 (None)
#            1314 COPY                     1
#            1316 STORE_FAST              12 (@py_assert2)
#            1318 COPY                     1
#            1320 STORE_FAST              13 (@py_assert4)
#            1322 COPY                     1
#            1324 STORE_FAST               8 (@py_assert6)
#            1326 STORE_FAST              14 (@py_assert7)
# 
#  86        1328 LOAD_CONST               0 (None)
#            1330 LOAD_CONST               0 (None)
#            1332 LOAD_CONST               0 (None)
#            1334 CALL                     2
#            1342 POP_TOP
#            1344 RETURN_CONST             0 (None)
#         >> 1346 PUSH_EXC_INFO
#            1348 WITH_EXCEPT_START
#            1350 POP_JUMP_IF_TRUE         1 (to 1354)
#            1352 RERAISE                  2
#         >> 1354 POP_TOP
#            1356 POP_EXCEPT
#            1358 POP_TOP
#            1360 POP_TOP
#            1362 RETURN_CONST             0 (None)
#         >> 1364 COPY                     3
#            1366 POP_EXCEPT
#            1368 RERAISE                  1
# ExceptionTable:
#   62 to 1326 -> 1346 [1] lasti
#   1346 to 1354 -> 1364 [3] lasti
# 