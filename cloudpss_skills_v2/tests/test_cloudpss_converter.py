# Recovered from: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/__pycache__/test_cloudpss_converter.cpython-312-pytest-9.0.2.pyc
# Original source: /home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py
# WARNING: This file was reconstructed from .pyc bytecode.
# The structure is accurate but implementation details may need manual review.


def _make_synthetic_topology():
    """Create a synthetic CloudPSS topology dict for unit testing."""
pass  # TODO: restore


class _MockTopology:
    """_MockTopology"""
    def __init__(self, components):
        pass


def TestCloudPSSModelConverterUnit():
    """TestCloudPSSModelConverterUnit"""
pass  # TODO: restore


def TestCloudPSSModelConverterIntegration():
    """TestCloudPSSModelConverterIntegration"""
pass  # TODO: restore



# === FULL DISASSEMBLY (for manual reconstruction) ===
#   0           0 RESUME                   0
# 
#   1           2 LOAD_CONST               0 ('\nTests for CloudPSSModelConverter - CloudPSS topology to PowerSystemModel conversion.\n\nUnit tests use synthetic topology data (no API calls required).\nIntegration tests require CloudPSS API access (--run-integration).\n')
#               4 STORE_NAME               0 (__doc__)
# 
#   8           6 LOAD_CONST               1 (0)
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
#              36 IMPORT_NAME              7 (os)
#              38 STORE_NAME               7 (os)
# 
#   9          40 LOAD_CONST               1 (0)
#              42 LOAD_CONST               2 (None)
#              44 IMPORT_NAME              8 (pytest)
#              46 STORE_NAME               8 (pytest)
# 
#  11          48 LOAD_CONST               1 (0)
#              50 LOAD_CONST               3 (('CloudPSSModelConverter', 'ConversionMode', 'ConversionQuality', 'PowerSystemModel'))
#              52 IMPORT_NAME              9 (cloudpss_skills_v2.libs.model_lib)
#              54 IMPORT_FROM             10 (CloudPSSModelConverter)
#              56 STORE_NAME              10 (CloudPSSModelConverter)
#              58 IMPORT_FROM             11 (ConversionMode)
#              60 STORE_NAME              11 (ConversionMode)
#              62 IMPORT_FROM             12 (ConversionQuality)
#              64 STORE_NAME              12 (ConversionQuality)
#              66 IMPORT_FROM             13 (PowerSystemModel)
#              68 STORE_NAME              13 (PowerSystemModel)
#              70 POP_TOP
# 
#  17          72 LOAD_CONST               1 (0)
#              74 LOAD_CONST               4 (('BranchType', 'BusType', 'GeneratorType'))
#              76 IMPORT_NAME             14 (cloudpss_skills_v2.libs.data_lib)
#              78 IMPORT_FROM             15 (BranchType)
#              80 STORE_NAME              15 (BranchType)
#              82 IMPORT_FROM             16 (BusType)
#              84 STORE_NAME              16 (BusType)
#              86 IMPORT_FROM             17 (GeneratorType)
#              88 STORE_NAME              17 (GeneratorType)
#              90 POP_TOP
# 
#  24          92 LOAD_CONST               5 (<code object _make_synthetic_topology at 0x73cd949426f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 24>)
#              94 MAKE_FUNCTION            0
#              96 STORE_NAME              18 (_make_synthetic_topology)
# 
# 133          98 PUSH_NULL
#             100 LOAD_BUILD_CLASS
#             102 LOAD_CONST               6 (<code object _MockTopology at 0x73cd945fea30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 133>)
#             104 MAKE_FUNCTION            0
#             106 LOAD_CONST               7 ('_MockTopology')
#             108 CALL                     2
#             116 STORE_NAME              19 (_MockTopology)
# 
# 140         118 PUSH_NULL
#             120 LOAD_BUILD_CLASS
#             122 LOAD_CONST               8 (<code object TestCloudPSSModelConverterUnit at 0x73cd93b39a10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 140>)
#             124 MAKE_FUNCTION            0
#             126 LOAD_CONST               9 ('TestCloudPSSModelConverterUnit')
#             128 CALL                     2
#             136 STORE_NAME              20 (TestCloudPSSModelConverterUnit)
# 
# 326         138 LOAD_NAME                8 (pytest)
#             140 LOAD_ATTR               42 (mark)
#             160 LOAD_ATTR               44 (integration)
# 
# 327         180 PUSH_NULL
#             182 LOAD_BUILD_CLASS
#             184 LOAD_CONST              10 (<code object TestCloudPSSModelConverterIntegration at 0x73cd93b398f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 326>)
#             186 MAKE_FUNCTION            0
#             188 LOAD_CONST              11 ('TestCloudPSSModelConverterIntegration')
#             190 CALL                     2
# 
# 326         198 CALL                     0
# 
# 327         206 STORE_NAME              23 (TestCloudPSSModelConverterIntegration)
#             208 RETURN_CONST             2 (None)
# 
# Disassembly of <code object _make_synthetic_topology at 0x73cd949426f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 24>:
#  24           0 RESUME                   0
# 
#  28           2 LOAD_CONST               1 ('model/CloudPSS/_newBus_3p')
# 
#  29           4 LOAD_CONST               2 ('newBus_3p-0')
# 
#  31           6 LOAD_CONST               3 ('bus1')
# 
#  32           8 LOAD_CONST               4 ('345')
# 
#  33          10 LOAD_CONST               4 ('345')
# 
#  34          12 LOAD_CONST               5 ('0')
# 
#  35          14 LOAD_CONST               6 ('60')
# 
#  30          16 LOAD_CONST               7 (('Name', 'V', 'VBase', 'Theta', 'Freq'))
#              18 BUILD_CONST_KEY_MAP      5
# 
#  37          20 LOAD_CONST               5 ('0')
#              22 LOAD_CONST               8 (1)
#              24 BUILD_MAP                1
# 
#  38          26 LOAD_CONST               8 (1)
# 
#  27          28 LOAD_CONST               9 (('rid', 'label', 'args', 'pins', 'status'))
#              30 BUILD_CONST_KEY_MAP      5
# 
#  41          32 LOAD_CONST               1 ('model/CloudPSS/_newBus_3p')
# 
#  42          34 LOAD_CONST              10 ('newBus_3p-1')
# 
#  44          36 LOAD_CONST              11 ('bus2')
# 
#  45          38 LOAD_CONST               4 ('345')
# 
#  46          40 LOAD_CONST               4 ('345')
# 
#  47          42 LOAD_CONST              12 ('-5')
# 
#  48          44 LOAD_CONST               6 ('60')
# 
#  43          46 LOAD_CONST               7 (('Name', 'V', 'VBase', 'Theta', 'Freq'))
#              48 BUILD_CONST_KEY_MAP      5
# 
#  50          50 LOAD_CONST               5 ('0')
#              52 LOAD_CONST              13 (2)
#              54 BUILD_MAP                1
# 
#  51          56 LOAD_CONST               8 (1)
# 
#  40          58 LOAD_CONST               9 (('rid', 'label', 'args', 'pins', 'status'))
#              60 BUILD_CONST_KEY_MAP      5
# 
#  54          62 LOAD_CONST               1 ('model/CloudPSS/_newBus_3p')
# 
#  55          64 LOAD_CONST              14 ('newBus_3p-2')
# 
#  57          66 LOAD_CONST              15 ('bus3')
# 
#  58          68 LOAD_CONST              16 ('230')
# 
#  59          70 LOAD_CONST              16 ('230')
# 
#  60          72 LOAD_CONST              17 ('-10')
# 
#  61          74 LOAD_CONST               6 ('60')
# 
#  56          76 LOAD_CONST               7 (('Name', 'V', 'VBase', 'Theta', 'Freq'))
#              78 BUILD_CONST_KEY_MAP      5
# 
#  63          80 LOAD_CONST               5 ('0')
#              82 LOAD_CONST              18 (3)
#              84 BUILD_MAP                1
# 
#  64          86 LOAD_CONST               8 (1)
# 
#  53          88 LOAD_CONST               9 (('rid', 'label', 'args', 'pins', 'status'))
#              90 BUILD_CONST_KEY_MAP      5
# 
#  67          92 LOAD_CONST              19 ('model/CloudPSS/TransmissionLine')
# 
#  68          94 LOAD_CONST              20 ('TLine_3p-0')
# 
#  70          96 LOAD_CONST              21 ('line-1-2')
# 
#  71          98 LOAD_CONST              22 ('0.002')
# 
#  72         100 LOAD_CONST              23 ('0.04')
# 
#  73         102 LOAD_CONST              24 ('0.01')
# 
#  74         104 LOAD_CONST              25 ('500')
# 
#  69         106 LOAD_CONST              26 (('Name', 'R', 'X', 'B', 'Rating'))
#             108 BUILD_CONST_KEY_MAP      5
# 
#  76         110 LOAD_CONST               8 (1)
#             112 LOAD_CONST              13 (2)
#             114 LOAD_CONST              27 (('0', '1'))
#             116 BUILD_CONST_KEY_MAP      2
# 
#  77         118 LOAD_CONST               8 (1)
# 
#  66         120 LOAD_CONST               9 (('rid', 'label', 'args', 'pins', 'status'))
#             122 BUILD_CONST_KEY_MAP      5
# 
#  80         124 LOAD_CONST              19 ('model/CloudPSS/TransmissionLine')
# 
#  81         126 LOAD_CONST              28 ('TLine_3p-1')
# 
#  82         128 LOAD_CONST              29 ('line-2-3')
#             130 LOAD_CONST              30 ('0.005')
#             132 LOAD_CONST              31 ('0.06')
#             134 LOAD_CONST              32 ('0.02')
#             136 LOAD_CONST              33 (('Name', 'R', 'X', 'B'))
#             138 BUILD_CONST_KEY_MAP      4
# 
#  83         140 LOAD_CONST              13 (2)
#             142 LOAD_CONST              18 (3)
#             144 LOAD_CONST              27 (('0', '1'))
#             146 BUILD_CONST_KEY_MAP      2
# 
#  84         148 LOAD_CONST               8 (1)
# 
#  79         150 LOAD_CONST               9 (('rid', 'label', 'args', 'pins', 'status'))
#             152 BUILD_CONST_KEY_MAP      5
# 
#  87         154 LOAD_CONST              34 ('model/CloudPSS/_newTransformer_3p2w')
# 
#  88         156 LOAD_CONST              35 ('newTransformer_3p2w-0')
# 
#  90         158 LOAD_CONST              36 ('trafo-1-3')
# 
#  91         160 LOAD_CONST              37 ('300')
# 
#  92         162 LOAD_CONST               4 ('345')
# 
#  93         164 LOAD_CONST              16 ('230')
# 
#  94         166 LOAD_CONST               6 ('60')
# 
#  95         168 LOAD_CONST              22 ('0.002')
# 
#  96         170 LOAD_CONST              38 ('0.08')
# 
#  97         172 LOAD_CONST              39 ('30')
# 
#  89         174 LOAD_CONST              40 (('Name', 'Tmva', 'V1', 'V2', 'f', 'Rn1', 'Xn1', 'Lead'))
#             176 BUILD_CONST_KEY_MAP      8
# 
#  99         178 LOAD_CONST               8 (1)
#             180 LOAD_CONST              18 (3)
#             182 LOAD_CONST              41 (4)
#             184 LOAD_CONST              42 (5)
#             186 LOAD_CONST              43 (('0', '1', '4', '5'))
#             188 BUILD_CONST_KEY_MAP      4
# 
# 100         190 LOAD_CONST               8 (1)
# 
#  86         192 LOAD_CONST               9 (('rid', 'label', 'args', 'pins', 'status'))
#             194 BUILD_CONST_KEY_MAP      5
# 
# 103         196 LOAD_CONST              44 ('model/CloudPSS/SyncGeneratorRouter')
# 
# 104         198 LOAD_CONST              45 ('SyncGen-0')
# 
# 106         200 LOAD_CONST              46 ('Gen1')
# 
# 107         202 LOAD_CONST              47 ('100')
# 
# 108         204 LOAD_CONST              48 ('200')
# 
# 109         206 LOAD_CONST               4 ('345')
# 
# 110         208 LOAD_CONST               6 ('60')
# 
# 111         210 LOAD_CONST              49 ('0.003')
# 
# 105         212 LOAD_CONST              50 (('Name', 'P', 'Smva', 'V', 'freq', 'Rs'))
#             214 BUILD_CONST_KEY_MAP      6
# 
# 113         216 LOAD_CONST               5 ('0')
#             218 LOAD_CONST               8 (1)
#             220 BUILD_MAP                1
# 
# 114         222 LOAD_CONST               8 (1)
# 
# 102         224 LOAD_CONST               9 (('rid', 'label', 'args', 'pins', 'status'))
#             226 BUILD_CONST_KEY_MAP      5
# 
# 117         228 LOAD_CONST              51 ('model/CloudPSS/_newExpLoad_3p')
# 
# 118         230 LOAD_CONST              52 ('newExpLoad-0')
# 
# 119         232 LOAD_CONST              53 ('load-2')
#             234 LOAD_CONST              54 ('50')
#             236 LOAD_CONST              55 ('25')
#             238 LOAD_CONST              56 ('1')
#             240 LOAD_CONST              56 ('1')
#             242 LOAD_CONST              57 (('Name', 'p', 'q', 'NP', 'NQ'))
#             244 BUILD_CONST_KEY_MAP      5
# 
# 120         246 LOAD_CONST               5 ('0')
#             248 LOAD_CONST              13 (2)
#             250 BUILD_MAP                1
# 
# 121         252 LOAD_CONST               8 (1)
# 
# 116         254 LOAD_CONST               9 (('rid', 'label', 'args', 'pins', 'status'))
#             256 BUILD_CONST_KEY_MAP      5
# 
# 124         258 LOAD_CONST              51 ('model/CloudPSS/_newExpLoad_3p')
# 
# 125         260 LOAD_CONST              58 ('newExpLoad-1')
# 
# 126         262 LOAD_CONST              59 ('load-3')
#             264 LOAD_CONST              60 ('80')
#             266 LOAD_CONST              61 ('40')
#             268 LOAD_CONST              56 ('1')
#             270 LOAD_CONST              62 ('2')
#             272 LOAD_CONST              57 (('Name', 'p', 'q', 'NP', 'NQ'))
#             274 BUILD_CONST_KEY_MAP      5
# 
# 127         276 LOAD_CONST               5 ('0')
#             278 LOAD_CONST              18 (3)
#             280 BUILD_MAP                1
# 
# 128         282 LOAD_CONST               8 (1)
# 
# 123         284 LOAD_CONST               9 (('rid', 'label', 'args', 'pins', 'status'))
#             286 BUILD_CONST_KEY_MAP      5
# 
#  26         288 LOAD_CONST              63 (('bus_0', 'bus_1', 'bus_2', 'line_0', 'line_1', 'trafo_0', 'gen_0', 'load_0', 'load_1'))
#             290 BUILD_CONST_KEY_MAP      9
#             292 RETURN_VALUE
# 
# Disassembly of <code object _MockTopology at 0x73cd945fea30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 133>:
# 133           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('_MockTopology')
#               8 STORE_NAME               2 (__qualname__)
# 
# 134          10 LOAD_CONST               1 ('Mock CloudPSS ModelTopology with synthetic components.')
#              12 STORE_NAME               3 (__doc__)
# 
# 136          14 LOAD_CONST               2 (<code object __init__ at 0x73cd945ff210, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 136>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (__init__)
#              20 RETURN_CONST             3 (None)
# 
# Disassembly of <code object __init__ at 0x73cd945ff210, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 136>:
# 136           0 RESUME                   0
# 
# 137           2 LOAD_FAST                1 (components)
#               4 LOAD_FAST                0 (self)
#               6 STORE_ATTR               0 (components)
#              16 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestCloudPSSModelConverterUnit at 0x73cd93b39a10, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 140>:
# 140           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestCloudPSSModelConverterUnit')
#               8 STORE_NAME               2 (__qualname__)
# 
# 141          10 LOAD_CONST               1 ('Unit tests using synthetic topology data (no API required).')
#              12 STORE_NAME               3 (__doc__)
# 
# 143          14 LOAD_CONST               2 (<code object test_convert_to_model_basic at 0x3af9e7f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 143>)
#              16 MAKE_FUNCTION            0
#              18 STORE_NAME               4 (test_convert_to_model_basic)
# 
# 156          20 LOAD_CONST               3 (<code object test_bus_data_extraction at 0x3afa8120, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 156>)
#              22 MAKE_FUNCTION            0
#              24 STORE_NAME               5 (test_bus_data_extraction)
# 
# 172          26 LOAD_CONST               4 (<code object test_branch_line_extraction at 0x3afa9580, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 172>)
#              28 MAKE_FUNCTION            0
#              30 STORE_NAME               6 (test_branch_line_extraction)
# 
# 187          32 LOAD_CONST               5 (<code object test_branch_transformer_extraction at 0x3afaa950, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 187>)
#              34 MAKE_FUNCTION            0
#              36 STORE_NAME               7 (test_branch_transformer_extraction)
# 
# 201          38 LOAD_CONST               6 (<code object test_generator_extraction at 0x3afabb00, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 201>)
#              40 MAKE_FUNCTION            0
#              42 STORE_NAME               8 (test_generator_extraction)
# 
# 213          44 LOAD_CONST               7 (<code object test_load_extraction at 0x3aeca6c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 213>)
#              46 MAKE_FUNCTION            0
#              48 STORE_NAME               9 (test_load_extraction)
# 
# 229          50 LOAD_CONST               8 (<code object test_topology_validation at 0x3af96680, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 229>)
#              52 MAKE_FUNCTION            0
#              54 STORE_NAME              10 (test_topology_validation)
# 
# 239          56 LOAD_CONST               9 (<code object test_invalid_source_error at 0x3af9bd40, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 239>)
#              58 MAKE_FUNCTION            0
#              60 STORE_NAME              11 (test_invalid_source_error)
# 
# 246          62 LOAD_CONST              10 (<code object test_convert_from_model_roundtrip at 0x3aecbce0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 246>)
#              64 MAKE_FUNCTION            0
#              66 STORE_NAME              12 (test_convert_from_model_roundtrip)
# 
# 264          68 LOAD_CONST              11 (<code object test_convert_from_model_bus_generation at 0x3aecdc30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 264>)
#              70 MAKE_FUNCTION            0
#              72 STORE_NAME              13 (test_convert_from_model_bus_generation)
# 
# 313          74 LOAD_CONST              12 (<code object test_conversion_report_quality at 0x3af9f220, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 313>)
#              76 MAKE_FUNCTION            0
#              78 STORE_NAME              14 (test_conversion_report_quality)
#              80 RETURN_CONST            13 (None)
# 
# Disassembly of <code object test_convert_to_model_basic at 0x3af9e7f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 143>:
# 143           0 RESUME                   0
# 
# 144           2 LOAD_GLOBAL              1 (NULL + CloudPSSModelConverter)
#              12 CALL                     0
#              20 STORE_FAST               1 (converter)
# 
# 145          22 LOAD_GLOBAL              3 (NULL + _make_synthetic_topology)
#              32 CALL                     0
#              40 STORE_FAST               2 (topo_dict)
# 
# 146          42 LOAD_GLOBAL              5 (NULL + _MockTopology)
#              52 LOAD_FAST                2 (topo_dict)
#              54 CALL                     1
#              62 STORE_FAST               3 (topo)
# 
# 148          64 LOAD_FAST                1 (converter)
#              66 LOAD_ATTR                7 (NULL|self + convert_to_model)
#              86 LOAD_FAST                3 (topo)
#              88 CALL                     1
#              96 UNPACK_SEQUENCE          2
#             100 STORE_FAST               4 (model)
#             102 STORE_FAST               5 (report)
# 
# 150         104 LOAD_FAST                5 (report)
#             106 LOAD_ATTR                8 (is_success)
#             126 STORE_FAST               6 (@py_assert1)
#             128 LOAD_FAST                6 (@py_assert1)
#             130 POP_JUMP_IF_TRUE       121 (to 374)
#             132 LOAD_CONST               1 ('assert %(py2)s\n{%(py2)s = %(py0)s.is_success\n}')
#             134 LOAD_CONST               2 ('report')
#             136 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             146 LOAD_ATTR               12 (locals)
#             166 CALL                     0
#             174 CONTAINS_OP              0
#             176 POP_JUMP_IF_TRUE        21 (to 220)
#             178 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             188 LOAD_ATTR               16 (_should_repr_global_name)
#             208 LOAD_FAST                5 (report)
#             210 CALL                     1
#             218 POP_JUMP_IF_FALSE       21 (to 262)
#         >>  220 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             230 LOAD_ATTR               18 (_saferepr)
#             250 LOAD_FAST                5 (report)
#             252 CALL                     1
#             260 JUMP_FORWARD             1 (to 264)
#         >>  262 LOAD_CONST               2 ('report')
#         >>  264 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             274 LOAD_ATTR               18 (_saferepr)
#             294 LOAD_FAST                6 (@py_assert1)
#             296 CALL                     1
#             304 LOAD_CONST               3 (('py0', 'py2'))
#             306 BUILD_CONST_KEY_MAP      2
#             308 BINARY_OP                6 (%)
#             312 STORE_FAST               7 (@py_format3)
#             314 LOAD_GLOBAL             21 (NULL + AssertionError)
#             324 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             334 LOAD_ATTR               22 (_format_explanation)
#             354 LOAD_FAST                7 (@py_format3)
#             356 CALL                     1
#             364 CALL                     1
#             372 RAISE_VARARGS            1
#         >>  374 LOAD_CONST               0 (None)
#             376 STORE_FAST               6 (@py_assert1)
# 
# 151         378 LOAD_FAST                4 (model)
#             380 LOAD_ATTR               24 (bus_count)
#             400 STORE_FAST               6 (@py_assert1)
#             402 LOAD_CONST               4 (3)
#             404 STORE_FAST               8 (@py_assert4)
#             406 LOAD_FAST                6 (@py_assert1)
#             408 LOAD_FAST                8 (@py_assert4)
#             410 COMPARE_OP              40 (==)
#             414 STORE_FAST               9 (@py_assert3)
#             416 LOAD_FAST                9 (@py_assert3)
#             418 POP_JUMP_IF_TRUE       173 (to 766)
#             420 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             430 LOAD_ATTR               26 (_call_reprcompare)
#             450 LOAD_CONST               5 (('==',))
#             452 LOAD_FAST                9 (@py_assert3)
#             454 BUILD_TUPLE              1
#             456 LOAD_CONST               6 (('%(py2)s\n{%(py2)s = %(py0)s.bus_count\n} == %(py5)s',))
#             458 LOAD_FAST                6 (@py_assert1)
#             460 LOAD_FAST                8 (@py_assert4)
#             462 BUILD_TUPLE              2
#             464 CALL                     4
#             472 LOAD_CONST               7 ('model')
#             474 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             484 LOAD_ATTR               12 (locals)
#             504 CALL                     0
#             512 CONTAINS_OP              0
#             514 POP_JUMP_IF_TRUE        21 (to 558)
#             516 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             526 LOAD_ATTR               16 (_should_repr_global_name)
#             546 LOAD_FAST                4 (model)
#             548 CALL                     1
#             556 POP_JUMP_IF_FALSE       21 (to 600)
#         >>  558 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             568 LOAD_ATTR               18 (_saferepr)
#             588 LOAD_FAST                4 (model)
#             590 CALL                     1
#             598 JUMP_FORWARD             1 (to 602)
#         >>  600 LOAD_CONST               7 ('model')
#         >>  602 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             612 LOAD_ATTR               18 (_saferepr)
#             632 LOAD_FAST                6 (@py_assert1)
#             634 CALL                     1
#             642 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             652 LOAD_ATTR               18 (_saferepr)
#             672 LOAD_FAST                8 (@py_assert4)
#             674 CALL                     1
#             682 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#             684 BUILD_CONST_KEY_MAP      3
#             686 BINARY_OP                6 (%)
#             690 STORE_FAST              10 (@py_format6)
#             692 LOAD_CONST               9 ('assert %(py7)s')
#             694 LOAD_CONST              10 ('py7')
#             696 LOAD_FAST               10 (@py_format6)
#             698 BUILD_MAP                1
#             700 BINARY_OP                6 (%)
#             704 STORE_FAST              11 (@py_format8)
#             706 LOAD_GLOBAL             21 (NULL + AssertionError)
#             716 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             726 LOAD_ATTR               22 (_format_explanation)
#             746 LOAD_FAST               11 (@py_format8)
#             748 CALL                     1
#             756 CALL                     1
#             764 RAISE_VARARGS            1
#         >>  766 LOAD_CONST               0 (None)
#             768 COPY                     1
#             770 STORE_FAST               6 (@py_assert1)
#             772 COPY                     1
#             774 STORE_FAST               9 (@py_assert3)
#             776 STORE_FAST               8 (@py_assert4)
# 
# 152         778 LOAD_FAST                4 (model)
#             780 LOAD_ATTR               28 (branch_count)
#             800 STORE_FAST               6 (@py_assert1)
#             802 LOAD_CONST               4 (3)
#             804 STORE_FAST               8 (@py_assert4)
#             806 LOAD_FAST                6 (@py_assert1)
#             808 LOAD_FAST                8 (@py_assert4)
#             810 COMPARE_OP              40 (==)
#             814 STORE_FAST               9 (@py_assert3)
#             816 LOAD_FAST                9 (@py_assert3)
#             818 POP_JUMP_IF_TRUE       173 (to 1166)
#             820 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             830 LOAD_ATTR               26 (_call_reprcompare)
#             850 LOAD_CONST               5 (('==',))
#             852 LOAD_FAST                9 (@py_assert3)
#             854 BUILD_TUPLE              1
#             856 LOAD_CONST              11 (('%(py2)s\n{%(py2)s = %(py0)s.branch_count\n} == %(py5)s',))
#             858 LOAD_FAST                6 (@py_assert1)
#             860 LOAD_FAST                8 (@py_assert4)
#             862 BUILD_TUPLE              2
#             864 CALL                     4
#             872 LOAD_CONST               7 ('model')
#             874 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             884 LOAD_ATTR               12 (locals)
#             904 CALL                     0
#             912 CONTAINS_OP              0
#             914 POP_JUMP_IF_TRUE        21 (to 958)
#             916 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             926 LOAD_ATTR               16 (_should_repr_global_name)
#             946 LOAD_FAST                4 (model)
#             948 CALL                     1
#             956 POP_JUMP_IF_FALSE       21 (to 1000)
#         >>  958 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             968 LOAD_ATTR               18 (_saferepr)
#             988 LOAD_FAST                4 (model)
#             990 CALL                     1
#             998 JUMP_FORWARD             1 (to 1002)
#         >> 1000 LOAD_CONST               7 ('model')
#         >> 1002 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1012 LOAD_ATTR               18 (_saferepr)
#            1032 LOAD_FAST                6 (@py_assert1)
#            1034 CALL                     1
#            1042 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1052 LOAD_ATTR               18 (_saferepr)
#            1072 LOAD_FAST                8 (@py_assert4)
#            1074 CALL                     1
#            1082 LOAD_CONST               8 (('py0', 'py2', 'py5'))
#            1084 BUILD_CONST_KEY_MAP      3
#            1086 BINARY_OP                6 (%)
#            1090 STORE_FAST              10 (@py_format6)
#            1092 LOAD_CONST               9 ('assert %(py7)s')
#            1094 LOAD_CONST              10 ('py7')
#            1096 LOAD_FAST               10 (@py_format6)
#            1098 BUILD_MAP                1
#            1100 BINARY_OP                6 (%)
#            1104 STORE_FAST              11 (@py_format8)
#            1106 LOAD_GLOBAL             21 (NULL + AssertionError)
#            1116 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1126 LOAD_ATTR               22 (_format_explanation)
#            1146 LOAD_FAST               11 (@py_format8)
#            1148 CALL                     1
#            1156 CALL                     1
#            1164 RAISE_VARARGS            1
#         >> 1166 LOAD_CONST               0 (None)
#            1168 COPY                     1
#            1170 STORE_FAST               6 (@py_assert1)
#            1172 COPY                     1
#            1174 STORE_FAST               9 (@py_assert3)
#            1176 STORE_FAST               8 (@py_assert4)
# 
# 153        1178 LOAD_FAST                4 (model)
#            1180 LOAD_ATTR               30 (generators)
#            1200 STORE_FAST              12 (@py_assert2)
#            1202 LOAD_GLOBAL             33 (NULL + len)
#            1212 LOAD_FAST               12 (@py_assert2)
#            1214 CALL                     1
#            1222 STORE_FAST               8 (@py_assert4)
#            1224 LOAD_CONST              12 (1)
#            1226 STORE_FAST              13 (@py_assert7)
#            1228 LOAD_FAST                8 (@py_assert4)
#            1230 LOAD_FAST               13 (@py_assert7)
#            1232 COMPARE_OP              40 (==)
#            1236 STORE_FAST              14 (@py_assert6)
#            1238 LOAD_FAST               14 (@py_assert6)
#            1240 EXTENDED_ARG             1
#            1242 POP_JUMP_IF_TRUE       266 (to 1776)
#            1244 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1254 LOAD_ATTR               26 (_call_reprcompare)
#            1274 LOAD_CONST               5 (('==',))
#            1276 LOAD_FAST               14 (@py_assert6)
#            1278 BUILD_TUPLE              1
#            1280 LOAD_CONST              13 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.generators\n})\n} == %(py8)s',))
#            1282 LOAD_FAST                8 (@py_assert4)
#            1284 LOAD_FAST               13 (@py_assert7)
#            1286 BUILD_TUPLE              2
#            1288 CALL                     4
#            1296 LOAD_CONST              14 ('len')
#            1298 LOAD_GLOBAL             11 (NULL + @py_builtins)
#            1308 LOAD_ATTR               12 (locals)
#            1328 CALL                     0
#            1336 CONTAINS_OP              0
#            1338 POP_JUMP_IF_TRUE        25 (to 1390)
#            1340 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1350 LOAD_ATTR               16 (_should_repr_global_name)
#            1370 LOAD_GLOBAL             32 (len)
#            1380 CALL                     1
#            1388 POP_JUMP_IF_FALSE       25 (to 1440)
#         >> 1390 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1400 LOAD_ATTR               18 (_saferepr)
#            1420 LOAD_GLOBAL             32 (len)
#            1430 CALL                     1
#            1438 JUMP_FORWARD             1 (to 1442)
#         >> 1440 LOAD_CONST              14 ('len')
#         >> 1442 LOAD_CONST               7 ('model')
#            1444 LOAD_GLOBAL             11 (NULL + @py_builtins)
#            1454 LOAD_ATTR               12 (locals)
#            1474 CALL                     0
#            1482 CONTAINS_OP              0
#            1484 POP_JUMP_IF_TRUE        21 (to 1528)
#            1486 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1496 LOAD_ATTR               16 (_should_repr_global_name)
#            1516 LOAD_FAST                4 (model)
#            1518 CALL                     1
#            1526 POP_JUMP_IF_FALSE       21 (to 1570)
#         >> 1528 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1538 LOAD_ATTR               18 (_saferepr)
#            1558 LOAD_FAST                4 (model)
#            1560 CALL                     1
#            1568 JUMP_FORWARD             1 (to 1572)
#         >> 1570 LOAD_CONST               7 ('model')
#         >> 1572 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1582 LOAD_ATTR               18 (_saferepr)
#            1602 LOAD_FAST               12 (@py_assert2)
#            1604 CALL                     1
#            1612 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1622 LOAD_ATTR               18 (_saferepr)
#            1642 LOAD_FAST                8 (@py_assert4)
#            1644 CALL                     1
#            1652 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1662 LOAD_ATTR               18 (_saferepr)
#            1682 LOAD_FAST               13 (@py_assert7)
#            1684 CALL                     1
#            1692 LOAD_CONST              15 (('py0', 'py1', 'py3', 'py5', 'py8'))
#            1694 BUILD_CONST_KEY_MAP      5
#            1696 BINARY_OP                6 (%)
#            1700 STORE_FAST              15 (@py_format9)
#            1702 LOAD_CONST              16 ('assert %(py10)s')
#            1704 LOAD_CONST              17 ('py10')
#            1706 LOAD_FAST               15 (@py_format9)
#            1708 BUILD_MAP                1
#            1710 BINARY_OP                6 (%)
#            1714 STORE_FAST              16 (@py_format11)
#            1716 LOAD_GLOBAL             21 (NULL + AssertionError)
#            1726 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1736 LOAD_ATTR               22 (_format_explanation)
#            1756 LOAD_FAST               16 (@py_format11)
#            1758 CALL                     1
#            1766 CALL                     1
#            1774 RAISE_VARARGS            1
#         >> 1776 LOAD_CONST               0 (None)
#            1778 COPY                     1
#            1780 STORE_FAST              12 (@py_assert2)
#            1782 COPY                     1
#            1784 STORE_FAST               8 (@py_assert4)
#            1786 COPY                     1
#            1788 STORE_FAST              14 (@py_assert6)
#            1790 STORE_FAST              13 (@py_assert7)
# 
# 154        1792 LOAD_FAST                4 (model)
#            1794 LOAD_ATTR               34 (loads)
#            1814 STORE_FAST              12 (@py_assert2)
#            1816 LOAD_GLOBAL             33 (NULL + len)
#            1826 LOAD_FAST               12 (@py_assert2)
#            1828 CALL                     1
#            1836 STORE_FAST               8 (@py_assert4)
#            1838 LOAD_CONST              18 (2)
#            1840 STORE_FAST              13 (@py_assert7)
#            1842 LOAD_FAST                8 (@py_assert4)
#            1844 LOAD_FAST               13 (@py_assert7)
#            1846 COMPARE_OP              40 (==)
#            1850 STORE_FAST              14 (@py_assert6)
#            1852 LOAD_FAST               14 (@py_assert6)
#            1854 EXTENDED_ARG             1
#            1856 POP_JUMP_IF_TRUE       266 (to 2390)
#            1858 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1868 LOAD_ATTR               26 (_call_reprcompare)
#            1888 LOAD_CONST               5 (('==',))
#            1890 LOAD_FAST               14 (@py_assert6)
#            1892 BUILD_TUPLE              1
#            1894 LOAD_CONST              19 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.loads\n})\n} == %(py8)s',))
#            1896 LOAD_FAST                8 (@py_assert4)
#            1898 LOAD_FAST               13 (@py_assert7)
#            1900 BUILD_TUPLE              2
#            1902 CALL                     4
#            1910 LOAD_CONST              14 ('len')
#            1912 LOAD_GLOBAL             11 (NULL + @py_builtins)
#            1922 LOAD_ATTR               12 (locals)
#            1942 CALL                     0
#            1950 CONTAINS_OP              0
#            1952 POP_JUMP_IF_TRUE        25 (to 2004)
#            1954 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            1964 LOAD_ATTR               16 (_should_repr_global_name)
#            1984 LOAD_GLOBAL             32 (len)
#            1994 CALL                     1
#            2002 POP_JUMP_IF_FALSE       25 (to 2054)
#         >> 2004 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            2014 LOAD_ATTR               18 (_saferepr)
#            2034 LOAD_GLOBAL             32 (len)
#            2044 CALL                     1
#            2052 JUMP_FORWARD             1 (to 2056)
#         >> 2054 LOAD_CONST              14 ('len')
#         >> 2056 LOAD_CONST               7 ('model')
#            2058 LOAD_GLOBAL             11 (NULL + @py_builtins)
#            2068 LOAD_ATTR               12 (locals)
#            2088 CALL                     0
#            2096 CONTAINS_OP              0
#            2098 POP_JUMP_IF_TRUE        21 (to 2142)
#            2100 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            2110 LOAD_ATTR               16 (_should_repr_global_name)
#            2130 LOAD_FAST                4 (model)
#            2132 CALL                     1
#            2140 POP_JUMP_IF_FALSE       21 (to 2184)
#         >> 2142 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            2152 LOAD_ATTR               18 (_saferepr)
#            2172 LOAD_FAST                4 (model)
#            2174 CALL                     1
#            2182 JUMP_FORWARD             1 (to 2186)
#         >> 2184 LOAD_CONST               7 ('model')
#         >> 2186 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            2196 LOAD_ATTR               18 (_saferepr)
#            2216 LOAD_FAST               12 (@py_assert2)
#            2218 CALL                     1
#            2226 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            2236 LOAD_ATTR               18 (_saferepr)
#            2256 LOAD_FAST                8 (@py_assert4)
#            2258 CALL                     1
#            2266 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            2276 LOAD_ATTR               18 (_saferepr)
#            2296 LOAD_FAST               13 (@py_assert7)
#            2298 CALL                     1
#            2306 LOAD_CONST              15 (('py0', 'py1', 'py3', 'py5', 'py8'))
#            2308 BUILD_CONST_KEY_MAP      5
#            2310 BINARY_OP                6 (%)
#            2314 STORE_FAST              15 (@py_format9)
#            2316 LOAD_CONST              16 ('assert %(py10)s')
#            2318 LOAD_CONST              17 ('py10')
#            2320 LOAD_FAST               15 (@py_format9)
#            2322 BUILD_MAP                1
#            2324 BINARY_OP                6 (%)
#            2328 STORE_FAST              16 (@py_format11)
#            2330 LOAD_GLOBAL             21 (NULL + AssertionError)
#            2340 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#            2350 LOAD_ATTR               22 (_format_explanation)
#            2370 LOAD_FAST               16 (@py_format11)
#            2372 CALL                     1
#            2380 CALL                     1
#            2388 RAISE_VARARGS            1
#         >> 2390 LOAD_CONST               0 (None)
#            2392 COPY                     1
#            2394 STORE_FAST              12 (@py_assert2)
#            2396 COPY                     1
#            2398 STORE_FAST               8 (@py_assert4)
#            2400 COPY                     1
#            2402 STORE_FAST              14 (@py_assert6)
#            2404 STORE_FAST              13 (@py_assert7)
#            2406 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_bus_data_extraction at 0x3afa8120, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 156>:
# 156           0 RESUME                   0
# 
# 157           2 LOAD_GLOBAL              1 (NULL + CloudPSSModelConverter)
#              12 CALL                     0
#              20 STORE_FAST               1 (converter)
# 
# 158          22 LOAD_GLOBAL              3 (NULL + _MockTopology)
#              32 LOAD_GLOBAL              5 (NULL + _make_synthetic_topology)
#              42 CALL                     0
#              50 CALL                     1
#              58 STORE_FAST               2 (topo)
# 
# 160          60 LOAD_FAST                1 (converter)
#              62 LOAD_ATTR                7 (NULL|self + convert_to_model)
#              82 LOAD_FAST                2 (topo)
#              84 CALL                     1
#              92 UNPACK_SEQUENCE          2
#              96 STORE_FAST               3 (model)
#              98 STORE_FAST               4 (_)
# 
# 162         100 LOAD_FAST                3 (model)
#             102 LOAD_ATTR                8 (buses)
#             122 GET_ITER
#             124 LOAD_FAST_AND_CLEAR      5 (b)
#             126 SWAP                     2
#             128 BUILD_SET                0
#             130 SWAP                     2
#         >>  132 FOR_ITER                14 (to 164)
#             136 STORE_FAST               5 (b)
#             138 LOAD_FAST                5 (b)
#             140 LOAD_ATTR               10 (name)
#             160 SET_ADD                  2
#             162 JUMP_BACKWARD           16 (to 132)
#         >>  164 END_FOR
#             166 STORE_FAST               6 (bus_names)
#             168 STORE_FAST               5 (b)
# 
# 163         170 LOAD_CONST               1 ('bus1')
#             172 STORE_FAST               7 (@py_assert0)
#             174 LOAD_FAST                7 (@py_assert0)
#             176 LOAD_FAST                6 (bus_names)
#             178 CONTAINS_OP              0
#             180 STORE_FAST               8 (@py_assert2)
#             182 LOAD_FAST                8 (@py_assert2)
#             184 POP_JUMP_IF_TRUE       153 (to 492)
#             186 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             196 LOAD_ATTR               14 (_call_reprcompare)
#             216 LOAD_CONST               2 (('in',))
#             218 LOAD_FAST                8 (@py_assert2)
#             220 BUILD_TUPLE              1
#             222 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             224 LOAD_FAST                7 (@py_assert0)
#             226 LOAD_FAST                6 (bus_names)
#             228 BUILD_TUPLE              2
#             230 CALL                     4
#             238 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             248 LOAD_ATTR               16 (_saferepr)
#             268 LOAD_FAST                7 (@py_assert0)
#             270 CALL                     1
#             278 LOAD_CONST               4 ('bus_names')
#             280 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             290 LOAD_ATTR               20 (locals)
#             310 CALL                     0
#             318 CONTAINS_OP              0
#             320 POP_JUMP_IF_TRUE        21 (to 364)
#             322 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             332 LOAD_ATTR               22 (_should_repr_global_name)
#             352 LOAD_FAST                6 (bus_names)
#             354 CALL                     1
#             362 POP_JUMP_IF_FALSE       21 (to 406)
#         >>  364 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             374 LOAD_ATTR               16 (_saferepr)
#             394 LOAD_FAST                6 (bus_names)
#             396 CALL                     1
#             404 JUMP_FORWARD             1 (to 408)
#         >>  406 LOAD_CONST               4 ('bus_names')
#         >>  408 LOAD_CONST               5 (('py1', 'py3'))
#             410 BUILD_CONST_KEY_MAP      2
#             412 BINARY_OP                6 (%)
#             416 STORE_FAST               9 (@py_format4)
#             418 LOAD_CONST               6 ('assert %(py5)s')
#             420 LOAD_CONST               7 ('py5')
#             422 LOAD_FAST                9 (@py_format4)
#             424 BUILD_MAP                1
#             426 BINARY_OP                6 (%)
#             430 STORE_FAST              10 (@py_format6)
#             432 LOAD_GLOBAL             25 (NULL + AssertionError)
#             442 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             452 LOAD_ATTR               26 (_format_explanation)
#             472 LOAD_FAST               10 (@py_format6)
#             474 CALL                     1
#             482 CALL                     1
#             490 RAISE_VARARGS            1
#         >>  492 LOAD_CONST               0 (None)
#             494 COPY                     1
#             496 STORE_FAST               7 (@py_assert0)
#             498 STORE_FAST               8 (@py_assert2)
# 
# 164         500 LOAD_CONST               8 ('bus2')
#             502 STORE_FAST               7 (@py_assert0)
#             504 LOAD_FAST                7 (@py_assert0)
#             506 LOAD_FAST                6 (bus_names)
#             508 CONTAINS_OP              0
#             510 STORE_FAST               8 (@py_assert2)
#             512 LOAD_FAST                8 (@py_assert2)
#             514 POP_JUMP_IF_TRUE       153 (to 822)
#             516 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             526 LOAD_ATTR               14 (_call_reprcompare)
#             546 LOAD_CONST               2 (('in',))
#             548 LOAD_FAST                8 (@py_assert2)
#             550 BUILD_TUPLE              1
#             552 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             554 LOAD_FAST                7 (@py_assert0)
#             556 LOAD_FAST                6 (bus_names)
#             558 BUILD_TUPLE              2
#             560 CALL                     4
#             568 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             578 LOAD_ATTR               16 (_saferepr)
#             598 LOAD_FAST                7 (@py_assert0)
#             600 CALL                     1
#             608 LOAD_CONST               4 ('bus_names')
#             610 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             620 LOAD_ATTR               20 (locals)
#             640 CALL                     0
#             648 CONTAINS_OP              0
#             650 POP_JUMP_IF_TRUE        21 (to 694)
#             652 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             662 LOAD_ATTR               22 (_should_repr_global_name)
#             682 LOAD_FAST                6 (bus_names)
#             684 CALL                     1
#             692 POP_JUMP_IF_FALSE       21 (to 736)
#         >>  694 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             704 LOAD_ATTR               16 (_saferepr)
#             724 LOAD_FAST                6 (bus_names)
#             726 CALL                     1
#             734 JUMP_FORWARD             1 (to 738)
#         >>  736 LOAD_CONST               4 ('bus_names')
#         >>  738 LOAD_CONST               5 (('py1', 'py3'))
#             740 BUILD_CONST_KEY_MAP      2
#             742 BINARY_OP                6 (%)
#             746 STORE_FAST               9 (@py_format4)
#             748 LOAD_CONST               6 ('assert %(py5)s')
#             750 LOAD_CONST               7 ('py5')
#             752 LOAD_FAST                9 (@py_format4)
#             754 BUILD_MAP                1
#             756 BINARY_OP                6 (%)
#             760 STORE_FAST              10 (@py_format6)
#             762 LOAD_GLOBAL             25 (NULL + AssertionError)
#             772 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             782 LOAD_ATTR               26 (_format_explanation)
#             802 LOAD_FAST               10 (@py_format6)
#             804 CALL                     1
#             812 CALL                     1
#             820 RAISE_VARARGS            1
#         >>  822 LOAD_CONST               0 (None)
#             824 COPY                     1
#             826 STORE_FAST               7 (@py_assert0)
#             828 STORE_FAST               8 (@py_assert2)
# 
# 165         830 LOAD_CONST               9 ('bus3')
#             832 STORE_FAST               7 (@py_assert0)
#             834 LOAD_FAST                7 (@py_assert0)
#             836 LOAD_FAST                6 (bus_names)
#             838 CONTAINS_OP              0
#             840 STORE_FAST               8 (@py_assert2)
#             842 LOAD_FAST                8 (@py_assert2)
#             844 POP_JUMP_IF_TRUE       153 (to 1152)
#             846 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             856 LOAD_ATTR               14 (_call_reprcompare)
#             876 LOAD_CONST               2 (('in',))
#             878 LOAD_FAST                8 (@py_assert2)
#             880 BUILD_TUPLE              1
#             882 LOAD_CONST               3 (('%(py1)s in %(py3)s',))
#             884 LOAD_FAST                7 (@py_assert0)
#             886 LOAD_FAST                6 (bus_names)
#             888 BUILD_TUPLE              2
#             890 CALL                     4
#             898 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             908 LOAD_ATTR               16 (_saferepr)
#             928 LOAD_FAST                7 (@py_assert0)
#             930 CALL                     1
#             938 LOAD_CONST               4 ('bus_names')
#             940 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             950 LOAD_ATTR               20 (locals)
#             970 CALL                     0
#             978 CONTAINS_OP              0
#             980 POP_JUMP_IF_TRUE        21 (to 1024)
#             982 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             992 LOAD_ATTR               22 (_should_repr_global_name)
#            1012 LOAD_FAST                6 (bus_names)
#            1014 CALL                     1
#            1022 POP_JUMP_IF_FALSE       21 (to 1066)
#         >> 1024 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1034 LOAD_ATTR               16 (_saferepr)
#            1054 LOAD_FAST                6 (bus_names)
#            1056 CALL                     1
#            1064 JUMP_FORWARD             1 (to 1068)
#         >> 1066 LOAD_CONST               4 ('bus_names')
#         >> 1068 LOAD_CONST               5 (('py1', 'py3'))
#            1070 BUILD_CONST_KEY_MAP      2
#            1072 BINARY_OP                6 (%)
#            1076 STORE_FAST               9 (@py_format4)
#            1078 LOAD_CONST               6 ('assert %(py5)s')
#            1080 LOAD_CONST               7 ('py5')
#            1082 LOAD_FAST                9 (@py_format4)
#            1084 BUILD_MAP                1
#            1086 BINARY_OP                6 (%)
#            1090 STORE_FAST              10 (@py_format6)
#            1092 LOAD_GLOBAL             25 (NULL + AssertionError)
#            1102 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1112 LOAD_ATTR               26 (_format_explanation)
#            1132 LOAD_FAST               10 (@py_format6)
#            1134 CALL                     1
#            1142 CALL                     1
#            1150 RAISE_VARARGS            1
#         >> 1152 LOAD_CONST               0 (None)
#            1154 COPY                     1
#            1156 STORE_FAST               7 (@py_assert0)
#            1158 STORE_FAST               8 (@py_assert2)
# 
# 167        1160 LOAD_FAST                3 (model)
#            1162 LOAD_ATTR               29 (NULL|self + get_bus_by_name)
#            1182 LOAD_CONST               1 ('bus1')
#            1184 CALL                     1
#            1192 STORE_FAST              11 (bus1)
# 
# 168        1194 LOAD_CONST               0 (None)
#            1196 STORE_FAST               8 (@py_assert2)
#            1198 LOAD_FAST               11 (bus1)
#            1200 LOAD_FAST                8 (@py_assert2)
#            1202 IS_OP                    1
#            1204 STORE_FAST              12 (@py_assert1)
#            1206 LOAD_FAST               12 (@py_assert1)
#            1208 POP_JUMP_IF_TRUE       153 (to 1516)
#            1210 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1220 LOAD_ATTR               14 (_call_reprcompare)
#            1240 LOAD_CONST              10 (('is not',))
#            1242 LOAD_FAST               12 (@py_assert1)
#            1244 BUILD_TUPLE              1
#            1246 LOAD_CONST              11 (('%(py0)s is not %(py3)s',))
#            1248 LOAD_FAST               11 (bus1)
#            1250 LOAD_FAST                8 (@py_assert2)
#            1252 BUILD_TUPLE              2
#            1254 CALL                     4
#            1262 LOAD_CONST               1 ('bus1')
#            1264 LOAD_GLOBAL             19 (NULL + @py_builtins)
#            1274 LOAD_ATTR               20 (locals)
#            1294 CALL                     0
#            1302 CONTAINS_OP              0
#            1304 POP_JUMP_IF_TRUE        21 (to 1348)
#            1306 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1316 LOAD_ATTR               22 (_should_repr_global_name)
#            1336 LOAD_FAST               11 (bus1)
#            1338 CALL                     1
#            1346 POP_JUMP_IF_FALSE       21 (to 1390)
#         >> 1348 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1358 LOAD_ATTR               16 (_saferepr)
#            1378 LOAD_FAST               11 (bus1)
#            1380 CALL                     1
#            1388 JUMP_FORWARD             1 (to 1392)
#         >> 1390 LOAD_CONST               1 ('bus1')
#         >> 1392 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1402 LOAD_ATTR               16 (_saferepr)
#            1422 LOAD_FAST                8 (@py_assert2)
#            1424 CALL                     1
#            1432 LOAD_CONST              12 (('py0', 'py3'))
#            1434 BUILD_CONST_KEY_MAP      2
#            1436 BINARY_OP                6 (%)
#            1440 STORE_FAST               9 (@py_format4)
#            1442 LOAD_CONST               6 ('assert %(py5)s')
#            1444 LOAD_CONST               7 ('py5')
#            1446 LOAD_FAST                9 (@py_format4)
#            1448 BUILD_MAP                1
#            1450 BINARY_OP                6 (%)
#            1454 STORE_FAST              10 (@py_format6)
#            1456 LOAD_GLOBAL             25 (NULL + AssertionError)
#            1466 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1476 LOAD_ATTR               26 (_format_explanation)
#            1496 LOAD_FAST               10 (@py_format6)
#            1498 CALL                     1
#            1506 CALL                     1
#            1514 RAISE_VARARGS            1
#         >> 1516 LOAD_CONST               0 (None)
#            1518 COPY                     1
#            1520 STORE_FAST              12 (@py_assert1)
#            1522 STORE_FAST               8 (@py_assert2)
# 
# 169        1524 LOAD_FAST               11 (bus1)
#            1526 LOAD_ATTR               30 (voltage_kv)
#            1546 STORE_FAST              12 (@py_assert1)
#            1548 LOAD_CONST              13 (345.0)
#            1550 STORE_FAST              13 (@py_assert4)
#            1552 LOAD_FAST               12 (@py_assert1)
#            1554 LOAD_FAST               13 (@py_assert4)
#            1556 COMPARE_OP              40 (==)
#            1560 STORE_FAST              14 (@py_assert3)
#            1562 LOAD_FAST               14 (@py_assert3)
#            1564 POP_JUMP_IF_TRUE       173 (to 1912)
#            1566 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1576 LOAD_ATTR               14 (_call_reprcompare)
#            1596 LOAD_CONST              14 (('==',))
#            1598 LOAD_FAST               14 (@py_assert3)
#            1600 BUILD_TUPLE              1
#            1602 LOAD_CONST              15 (('%(py2)s\n{%(py2)s = %(py0)s.voltage_kv\n} == %(py5)s',))
#            1604 LOAD_FAST               12 (@py_assert1)
#            1606 LOAD_FAST               13 (@py_assert4)
#            1608 BUILD_TUPLE              2
#            1610 CALL                     4
#            1618 LOAD_CONST               1 ('bus1')
#            1620 LOAD_GLOBAL             19 (NULL + @py_builtins)
#            1630 LOAD_ATTR               20 (locals)
#            1650 CALL                     0
#            1658 CONTAINS_OP              0
#            1660 POP_JUMP_IF_TRUE        21 (to 1704)
#            1662 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1672 LOAD_ATTR               22 (_should_repr_global_name)
#            1692 LOAD_FAST               11 (bus1)
#            1694 CALL                     1
#            1702 POP_JUMP_IF_FALSE       21 (to 1746)
#         >> 1704 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1714 LOAD_ATTR               16 (_saferepr)
#            1734 LOAD_FAST               11 (bus1)
#            1736 CALL                     1
#            1744 JUMP_FORWARD             1 (to 1748)
#         >> 1746 LOAD_CONST               1 ('bus1')
#         >> 1748 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1758 LOAD_ATTR               16 (_saferepr)
#            1778 LOAD_FAST               12 (@py_assert1)
#            1780 CALL                     1
#            1788 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1798 LOAD_ATTR               16 (_saferepr)
#            1818 LOAD_FAST               13 (@py_assert4)
#            1820 CALL                     1
#            1828 LOAD_CONST              16 (('py0', 'py2', 'py5'))
#            1830 BUILD_CONST_KEY_MAP      3
#            1832 BINARY_OP                6 (%)
#            1836 STORE_FAST              10 (@py_format6)
#            1838 LOAD_CONST              17 ('assert %(py7)s')
#            1840 LOAD_CONST              18 ('py7')
#            1842 LOAD_FAST               10 (@py_format6)
#            1844 BUILD_MAP                1
#            1846 BINARY_OP                6 (%)
#            1850 STORE_FAST              15 (@py_format8)
#            1852 LOAD_GLOBAL             25 (NULL + AssertionError)
#            1862 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1872 LOAD_ATTR               26 (_format_explanation)
#            1892 LOAD_FAST               15 (@py_format8)
#            1894 CALL                     1
#            1902 CALL                     1
#            1910 RAISE_VARARGS            1
#         >> 1912 LOAD_CONST               0 (None)
#            1914 COPY                     1
#            1916 STORE_FAST              12 (@py_assert1)
#            1918 COPY                     1
#            1920 STORE_FAST              14 (@py_assert3)
#            1922 STORE_FAST              13 (@py_assert4)
# 
# 170        1924 LOAD_FAST               11 (bus1)
#            1926 LOAD_ATTR               32 (bus_type)
#            1946 STORE_FAST              12 (@py_assert1)
#            1948 LOAD_GLOBAL             34 (BusType)
#            1958 LOAD_ATTR               36 (PQ)
#            1978 STORE_FAST              16 (@py_assert5)
#            1980 LOAD_FAST               12 (@py_assert1)
#            1982 LOAD_FAST               16 (@py_assert5)
#            1984 COMPARE_OP              40 (==)
#            1988 STORE_FAST              14 (@py_assert3)
#            1990 LOAD_FAST               14 (@py_assert3)
#            1992 POP_JUMP_IF_TRUE       246 (to 2486)
#            1994 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            2004 LOAD_ATTR               14 (_call_reprcompare)
#            2024 LOAD_CONST              14 (('==',))
#            2026 LOAD_FAST               14 (@py_assert3)
#            2028 BUILD_TUPLE              1
#            2030 LOAD_CONST              19 (('%(py2)s\n{%(py2)s = %(py0)s.bus_type\n} == %(py6)s\n{%(py6)s = %(py4)s.PQ\n}',))
#            2032 LOAD_FAST               12 (@py_assert1)
#            2034 LOAD_FAST               16 (@py_assert5)
#            2036 BUILD_TUPLE              2
#            2038 CALL                     4
#            2046 LOAD_CONST               1 ('bus1')
#            2048 LOAD_GLOBAL             19 (NULL + @py_builtins)
#            2058 LOAD_ATTR               20 (locals)
#            2078 CALL                     0
#            2086 CONTAINS_OP              0
#            2088 POP_JUMP_IF_TRUE        21 (to 2132)
#            2090 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            2100 LOAD_ATTR               22 (_should_repr_global_name)
#            2120 LOAD_FAST               11 (bus1)
#            2122 CALL                     1
#            2130 POP_JUMP_IF_FALSE       21 (to 2174)
#         >> 2132 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            2142 LOAD_ATTR               16 (_saferepr)
#            2162 LOAD_FAST               11 (bus1)
#            2164 CALL                     1
#            2172 JUMP_FORWARD             1 (to 2176)
#         >> 2174 LOAD_CONST               1 ('bus1')
#         >> 2176 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            2186 LOAD_ATTR               16 (_saferepr)
#            2206 LOAD_FAST               12 (@py_assert1)
#            2208 CALL                     1
#            2216 LOAD_CONST              20 ('BusType')
#            2218 LOAD_GLOBAL             19 (NULL + @py_builtins)
#            2228 LOAD_ATTR               20 (locals)
#            2248 CALL                     0
#            2256 CONTAINS_OP              0
#            2258 POP_JUMP_IF_TRUE        25 (to 2310)
#            2260 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            2270 LOAD_ATTR               22 (_should_repr_global_name)
#            2290 LOAD_GLOBAL             34 (BusType)
#            2300 CALL                     1
#            2308 POP_JUMP_IF_FALSE       25 (to 2360)
#         >> 2310 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            2320 LOAD_ATTR               16 (_saferepr)
#            2340 LOAD_GLOBAL             34 (BusType)
#            2350 CALL                     1
#            2358 JUMP_FORWARD             1 (to 2362)
#         >> 2360 LOAD_CONST              20 ('BusType')
#         >> 2362 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            2372 LOAD_ATTR               16 (_saferepr)
#            2392 LOAD_FAST               16 (@py_assert5)
#            2394 CALL                     1
#            2402 LOAD_CONST              21 (('py0', 'py2', 'py4', 'py6'))
#            2404 BUILD_CONST_KEY_MAP      4
#            2406 BINARY_OP                6 (%)
#            2410 STORE_FAST              17 (@py_format7)
#            2412 LOAD_CONST              22 ('assert %(py8)s')
#            2414 LOAD_CONST              23 ('py8')
#            2416 LOAD_FAST               17 (@py_format7)
#            2418 BUILD_MAP                1
#            2420 BINARY_OP                6 (%)
#            2424 STORE_FAST              18 (@py_format9)
#            2426 LOAD_GLOBAL             25 (NULL + AssertionError)
#            2436 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            2446 LOAD_ATTR               26 (_format_explanation)
#            2466 LOAD_FAST               18 (@py_format9)
#            2468 CALL                     1
#            2476 CALL                     1
#            2484 RAISE_VARARGS            1
#         >> 2486 LOAD_CONST               0 (None)
#            2488 COPY                     1
#            2490 STORE_FAST              12 (@py_assert1)
#            2492 COPY                     1
#            2494 STORE_FAST              14 (@py_assert3)
#            2496 STORE_FAST              16 (@py_assert5)
#            2498 RETURN_CONST             0 (None)
#         >> 2500 SWAP                     2
#            2502 POP_TOP
# 
# 162        2504 SWAP                     2
#            2506 STORE_FAST               5 (b)
#            2508 RERAISE                  0
# ExceptionTable:
#   128 to 164 -> 2500 [2]
# 
# Disassembly of <code object test_branch_line_extraction at 0x3afa9580, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 172>:
# 172           0 RESUME                   0
# 
# 173           2 LOAD_GLOBAL              1 (NULL + CloudPSSModelConverter)
#              12 CALL                     0
#              20 STORE_FAST               1 (converter)
# 
# 174          22 LOAD_GLOBAL              3 (NULL + _MockTopology)
#              32 LOAD_GLOBAL              5 (NULL + _make_synthetic_topology)
#              42 CALL                     0
#              50 CALL                     1
#              58 STORE_FAST               2 (topo)
# 
# 176          60 LOAD_FAST                1 (converter)
#              62 LOAD_ATTR                7 (NULL|self + convert_to_model)
#              82 LOAD_FAST                2 (topo)
#              84 CALL                     1
#              92 UNPACK_SEQUENCE          2
#              96 STORE_FAST               3 (model)
#              98 STORE_FAST               4 (_)
# 
# 178         100 LOAD_FAST                3 (model)
#             102 LOAD_ATTR                8 (branches)
#             122 GET_ITER
#             124 LOAD_FAST_AND_CLEAR      5 (b)
#             126 SWAP                     2
#             128 BUILD_LIST               0
#             130 SWAP                     2
#         >>  132 FOR_ITER                34 (to 204)
#             136 STORE_FAST               5 (b)
#             138 LOAD_FAST                5 (b)
#             140 LOAD_ATTR               10 (branch_type)
#             160 LOAD_GLOBAL             12 (BranchType)
#             170 LOAD_ATTR               14 (LINE)
#             190 COMPARE_OP              40 (==)
#             194 POP_JUMP_IF_TRUE         1 (to 198)
#             196 JUMP_BACKWARD           33 (to 132)
#         >>  198 LOAD_FAST                5 (b)
#             200 LIST_APPEND              2
#             202 JUMP_BACKWARD           36 (to 132)
#         >>  204 END_FOR
#             206 STORE_FAST               6 (lines)
#             208 STORE_FAST               5 (b)
# 
# 179         210 LOAD_GLOBAL             17 (NULL + len)
#             220 LOAD_FAST                6 (lines)
#             222 CALL                     1
#             230 STORE_FAST               7 (@py_assert2)
#             232 LOAD_CONST               1 (2)
#             234 STORE_FAST               8 (@py_assert5)
#             236 LOAD_FAST                7 (@py_assert2)
#             238 LOAD_FAST                8 (@py_assert5)
#             240 COMPARE_OP              40 (==)
#             244 STORE_FAST               9 (@py_assert4)
#             246 LOAD_FAST                9 (@py_assert4)
#             248 POP_JUMP_IF_TRUE       246 (to 742)
#             250 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             260 LOAD_ATTR               20 (_call_reprcompare)
#             280 LOAD_CONST               2 (('==',))
#             282 LOAD_FAST                9 (@py_assert4)
#             284 BUILD_TUPLE              1
#             286 LOAD_CONST               3 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             288 LOAD_FAST                7 (@py_assert2)
#             290 LOAD_FAST                8 (@py_assert5)
#             292 BUILD_TUPLE              2
#             294 CALL                     4
#             302 LOAD_CONST               4 ('len')
#             304 LOAD_GLOBAL             23 (NULL + @py_builtins)
#             314 LOAD_ATTR               24 (locals)
#             334 CALL                     0
#             342 CONTAINS_OP              0
#             344 POP_JUMP_IF_TRUE        25 (to 396)
#             346 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             356 LOAD_ATTR               26 (_should_repr_global_name)
#             376 LOAD_GLOBAL             16 (len)
#             386 CALL                     1
#             394 POP_JUMP_IF_FALSE       25 (to 446)
#         >>  396 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             406 LOAD_ATTR               28 (_saferepr)
#             426 LOAD_GLOBAL             16 (len)
#             436 CALL                     1
#             444 JUMP_FORWARD             1 (to 448)
#         >>  446 LOAD_CONST               4 ('len')
#         >>  448 LOAD_CONST               5 ('lines')
#             450 LOAD_GLOBAL             23 (NULL + @py_builtins)
#             460 LOAD_ATTR               24 (locals)
#             480 CALL                     0
#             488 CONTAINS_OP              0
#             490 POP_JUMP_IF_TRUE        21 (to 534)
#             492 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             502 LOAD_ATTR               26 (_should_repr_global_name)
#             522 LOAD_FAST                6 (lines)
#             524 CALL                     1
#             532 POP_JUMP_IF_FALSE       21 (to 576)
#         >>  534 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             544 LOAD_ATTR               28 (_saferepr)
#             564 LOAD_FAST                6 (lines)
#             566 CALL                     1
#             574 JUMP_FORWARD             1 (to 578)
#         >>  576 LOAD_CONST               5 ('lines')
#         >>  578 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             588 LOAD_ATTR               28 (_saferepr)
#             608 LOAD_FAST                7 (@py_assert2)
#             610 CALL                     1
#             618 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             628 LOAD_ATTR               28 (_saferepr)
#             648 LOAD_FAST                8 (@py_assert5)
#             650 CALL                     1
#             658 LOAD_CONST               6 (('py0', 'py1', 'py3', 'py6'))
#             660 BUILD_CONST_KEY_MAP      4
#             662 BINARY_OP                6 (%)
#             666 STORE_FAST              10 (@py_format7)
#             668 LOAD_CONST               7 ('assert %(py8)s')
#             670 LOAD_CONST               8 ('py8')
#             672 LOAD_FAST               10 (@py_format7)
#             674 BUILD_MAP                1
#             676 BINARY_OP                6 (%)
#             680 STORE_FAST              11 (@py_format9)
#             682 LOAD_GLOBAL             31 (NULL + AssertionError)
#             692 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             702 LOAD_ATTR               32 (_format_explanation)
#             722 LOAD_FAST               11 (@py_format9)
#             724 CALL                     1
#             732 CALL                     1
#             740 RAISE_VARARGS            1
#         >>  742 LOAD_CONST               0 (None)
#             744 COPY                     1
#             746 STORE_FAST               7 (@py_assert2)
#             748 COPY                     1
#             750 STORE_FAST               9 (@py_assert4)
#             752 STORE_FAST               8 (@py_assert5)
# 
# 181         754 LOAD_FAST                6 (lines)
#             756 GET_ITER
#             758 LOAD_FAST_AND_CLEAR     12 (l)
#             760 SWAP                     2
#             762 BUILD_LIST               0
#             764 SWAP                     2
#         >>  766 FOR_ITER                20 (to 810)
#             770 STORE_FAST              12 (l)
#             772 LOAD_FAST               12 (l)
#             774 LOAD_ATTR               34 (name)
#             794 LOAD_CONST               9 ('line-1-2')
#             796 COMPARE_OP              40 (==)
#             800 POP_JUMP_IF_TRUE         1 (to 804)
#             802 JUMP_BACKWARD           19 (to 766)
#         >>  804 LOAD_FAST               12 (l)
#             806 LIST_APPEND              2
#             808 JUMP_BACKWARD           22 (to 766)
#         >>  810 END_FOR
#             812 SWAP                     2
#             814 STORE_FAST              12 (l)
#             816 LOAD_CONST              10 (0)
#             818 BINARY_SUBSCR
#             822 STORE_FAST              13 (line_12)
# 
# 182         824 LOAD_FAST               13 (line_12)
#             826 LOAD_ATTR               36 (from_bus)
#             846 STORE_FAST              14 (@py_assert1)
#             848 LOAD_CONST              11 ('bus1')
#             850 STORE_FAST               9 (@py_assert4)
#             852 LOAD_FAST               14 (@py_assert1)
#             854 LOAD_FAST                9 (@py_assert4)
#             856 COMPARE_OP              40 (==)
#             860 STORE_FAST              15 (@py_assert3)
#             862 LOAD_FAST               15 (@py_assert3)
#             864 POP_JUMP_IF_TRUE       173 (to 1212)
#             866 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             876 LOAD_ATTR               20 (_call_reprcompare)
#             896 LOAD_CONST               2 (('==',))
#             898 LOAD_FAST               15 (@py_assert3)
#             900 BUILD_TUPLE              1
#             902 LOAD_CONST              12 (('%(py2)s\n{%(py2)s = %(py0)s.from_bus\n} == %(py5)s',))
#             904 LOAD_FAST               14 (@py_assert1)
#             906 LOAD_FAST                9 (@py_assert4)
#             908 BUILD_TUPLE              2
#             910 CALL                     4
#             918 LOAD_CONST              13 ('line_12')
#             920 LOAD_GLOBAL             23 (NULL + @py_builtins)
#             930 LOAD_ATTR               24 (locals)
#             950 CALL                     0
#             958 CONTAINS_OP              0
#             960 POP_JUMP_IF_TRUE        21 (to 1004)
#             962 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             972 LOAD_ATTR               26 (_should_repr_global_name)
#             992 LOAD_FAST               13 (line_12)
#             994 CALL                     1
#            1002 POP_JUMP_IF_FALSE       21 (to 1046)
#         >> 1004 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1014 LOAD_ATTR               28 (_saferepr)
#            1034 LOAD_FAST               13 (line_12)
#            1036 CALL                     1
#            1044 JUMP_FORWARD             1 (to 1048)
#         >> 1046 LOAD_CONST              13 ('line_12')
#         >> 1048 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1058 LOAD_ATTR               28 (_saferepr)
#            1078 LOAD_FAST               14 (@py_assert1)
#            1080 CALL                     1
#            1088 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1098 LOAD_ATTR               28 (_saferepr)
#            1118 LOAD_FAST                9 (@py_assert4)
#            1120 CALL                     1
#            1128 LOAD_CONST              14 (('py0', 'py2', 'py5'))
#            1130 BUILD_CONST_KEY_MAP      3
#            1132 BINARY_OP                6 (%)
#            1136 STORE_FAST              16 (@py_format6)
#            1138 LOAD_CONST              15 ('assert %(py7)s')
#            1140 LOAD_CONST              16 ('py7')
#            1142 LOAD_FAST               16 (@py_format6)
#            1144 BUILD_MAP                1
#            1146 BINARY_OP                6 (%)
#            1150 STORE_FAST              17 (@py_format8)
#            1152 LOAD_GLOBAL             31 (NULL + AssertionError)
#            1162 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1172 LOAD_ATTR               32 (_format_explanation)
#            1192 LOAD_FAST               17 (@py_format8)
#            1194 CALL                     1
#            1202 CALL                     1
#            1210 RAISE_VARARGS            1
#         >> 1212 LOAD_CONST               0 (None)
#            1214 COPY                     1
#            1216 STORE_FAST              14 (@py_assert1)
#            1218 COPY                     1
#            1220 STORE_FAST              15 (@py_assert3)
#            1222 STORE_FAST               9 (@py_assert4)
# 
# 183        1224 LOAD_FAST               13 (line_12)
#            1226 LOAD_ATTR               38 (to_bus)
#            1246 STORE_FAST              14 (@py_assert1)
#            1248 LOAD_CONST              17 ('bus2')
#            1250 STORE_FAST               9 (@py_assert4)
#            1252 LOAD_FAST               14 (@py_assert1)
#            1254 LOAD_FAST                9 (@py_assert4)
#            1256 COMPARE_OP              40 (==)
#            1260 STORE_FAST              15 (@py_assert3)
#            1262 LOAD_FAST               15 (@py_assert3)
#            1264 POP_JUMP_IF_TRUE       173 (to 1612)
#            1266 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1276 LOAD_ATTR               20 (_call_reprcompare)
#            1296 LOAD_CONST               2 (('==',))
#            1298 LOAD_FAST               15 (@py_assert3)
#            1300 BUILD_TUPLE              1
#            1302 LOAD_CONST              18 (('%(py2)s\n{%(py2)s = %(py0)s.to_bus\n} == %(py5)s',))
#            1304 LOAD_FAST               14 (@py_assert1)
#            1306 LOAD_FAST                9 (@py_assert4)
#            1308 BUILD_TUPLE              2
#            1310 CALL                     4
#            1318 LOAD_CONST              13 ('line_12')
#            1320 LOAD_GLOBAL             23 (NULL + @py_builtins)
#            1330 LOAD_ATTR               24 (locals)
#            1350 CALL                     0
#            1358 CONTAINS_OP              0
#            1360 POP_JUMP_IF_TRUE        21 (to 1404)
#            1362 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1372 LOAD_ATTR               26 (_should_repr_global_name)
#            1392 LOAD_FAST               13 (line_12)
#            1394 CALL                     1
#            1402 POP_JUMP_IF_FALSE       21 (to 1446)
#         >> 1404 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1414 LOAD_ATTR               28 (_saferepr)
#            1434 LOAD_FAST               13 (line_12)
#            1436 CALL                     1
#            1444 JUMP_FORWARD             1 (to 1448)
#         >> 1446 LOAD_CONST              13 ('line_12')
#         >> 1448 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1458 LOAD_ATTR               28 (_saferepr)
#            1478 LOAD_FAST               14 (@py_assert1)
#            1480 CALL                     1
#            1488 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1498 LOAD_ATTR               28 (_saferepr)
#            1518 LOAD_FAST                9 (@py_assert4)
#            1520 CALL                     1
#            1528 LOAD_CONST              14 (('py0', 'py2', 'py5'))
#            1530 BUILD_CONST_KEY_MAP      3
#            1532 BINARY_OP                6 (%)
#            1536 STORE_FAST              16 (@py_format6)
#            1538 LOAD_CONST              15 ('assert %(py7)s')
#            1540 LOAD_CONST              16 ('py7')
#            1542 LOAD_FAST               16 (@py_format6)
#            1544 BUILD_MAP                1
#            1546 BINARY_OP                6 (%)
#            1550 STORE_FAST              17 (@py_format8)
#            1552 LOAD_GLOBAL             31 (NULL + AssertionError)
#            1562 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1572 LOAD_ATTR               32 (_format_explanation)
#            1592 LOAD_FAST               17 (@py_format8)
#            1594 CALL                     1
#            1602 CALL                     1
#            1610 RAISE_VARARGS            1
#         >> 1612 LOAD_CONST               0 (None)
#            1614 COPY                     1
#            1616 STORE_FAST              14 (@py_assert1)
#            1618 COPY                     1
#            1620 STORE_FAST              15 (@py_assert3)
#            1622 STORE_FAST               9 (@py_assert4)
# 
# 184        1624 LOAD_FAST               13 (line_12)
#            1626 LOAD_ATTR               40 (resistance_pu)
#            1646 STORE_FAST              14 (@py_assert1)
#            1648 LOAD_CONST              19 (0.002)
#            1650 STORE_FAST               9 (@py_assert4)
#            1652 LOAD_FAST               14 (@py_assert1)
#            1654 LOAD_FAST                9 (@py_assert4)
#            1656 COMPARE_OP              40 (==)
#            1660 STORE_FAST              15 (@py_assert3)
#            1662 LOAD_FAST               15 (@py_assert3)
#            1664 POP_JUMP_IF_TRUE       173 (to 2012)
#            1666 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1676 LOAD_ATTR               20 (_call_reprcompare)
#            1696 LOAD_CONST               2 (('==',))
#            1698 LOAD_FAST               15 (@py_assert3)
#            1700 BUILD_TUPLE              1
#            1702 LOAD_CONST              20 (('%(py2)s\n{%(py2)s = %(py0)s.resistance_pu\n} == %(py5)s',))
#            1704 LOAD_FAST               14 (@py_assert1)
#            1706 LOAD_FAST                9 (@py_assert4)
#            1708 BUILD_TUPLE              2
#            1710 CALL                     4
#            1718 LOAD_CONST              13 ('line_12')
#            1720 LOAD_GLOBAL             23 (NULL + @py_builtins)
#            1730 LOAD_ATTR               24 (locals)
#            1750 CALL                     0
#            1758 CONTAINS_OP              0
#            1760 POP_JUMP_IF_TRUE        21 (to 1804)
#            1762 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1772 LOAD_ATTR               26 (_should_repr_global_name)
#            1792 LOAD_FAST               13 (line_12)
#            1794 CALL                     1
#            1802 POP_JUMP_IF_FALSE       21 (to 1846)
#         >> 1804 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1814 LOAD_ATTR               28 (_saferepr)
#            1834 LOAD_FAST               13 (line_12)
#            1836 CALL                     1
#            1844 JUMP_FORWARD             1 (to 1848)
#         >> 1846 LOAD_CONST              13 ('line_12')
#         >> 1848 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1858 LOAD_ATTR               28 (_saferepr)
#            1878 LOAD_FAST               14 (@py_assert1)
#            1880 CALL                     1
#            1888 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1898 LOAD_ATTR               28 (_saferepr)
#            1918 LOAD_FAST                9 (@py_assert4)
#            1920 CALL                     1
#            1928 LOAD_CONST              14 (('py0', 'py2', 'py5'))
#            1930 BUILD_CONST_KEY_MAP      3
#            1932 BINARY_OP                6 (%)
#            1936 STORE_FAST              16 (@py_format6)
#            1938 LOAD_CONST              15 ('assert %(py7)s')
#            1940 LOAD_CONST              16 ('py7')
#            1942 LOAD_FAST               16 (@py_format6)
#            1944 BUILD_MAP                1
#            1946 BINARY_OP                6 (%)
#            1950 STORE_FAST              17 (@py_format8)
#            1952 LOAD_GLOBAL             31 (NULL + AssertionError)
#            1962 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1972 LOAD_ATTR               32 (_format_explanation)
#            1992 LOAD_FAST               17 (@py_format8)
#            1994 CALL                     1
#            2002 CALL                     1
#            2010 RAISE_VARARGS            1
#         >> 2012 LOAD_CONST               0 (None)
#            2014 COPY                     1
#            2016 STORE_FAST              14 (@py_assert1)
#            2018 COPY                     1
#            2020 STORE_FAST              15 (@py_assert3)
#            2022 STORE_FAST               9 (@py_assert4)
# 
# 185        2024 LOAD_FAST               13 (line_12)
#            2026 LOAD_ATTR               42 (reactance_pu)
#            2046 STORE_FAST              14 (@py_assert1)
#            2048 LOAD_CONST              21 (0.04)
#            2050 STORE_FAST               9 (@py_assert4)
#            2052 LOAD_FAST               14 (@py_assert1)
#            2054 LOAD_FAST                9 (@py_assert4)
#            2056 COMPARE_OP              40 (==)
#            2060 STORE_FAST              15 (@py_assert3)
#            2062 LOAD_FAST               15 (@py_assert3)
#            2064 POP_JUMP_IF_TRUE       173 (to 2412)
#            2066 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            2076 LOAD_ATTR               20 (_call_reprcompare)
#            2096 LOAD_CONST               2 (('==',))
#            2098 LOAD_FAST               15 (@py_assert3)
#            2100 BUILD_TUPLE              1
#            2102 LOAD_CONST              22 (('%(py2)s\n{%(py2)s = %(py0)s.reactance_pu\n} == %(py5)s',))
#            2104 LOAD_FAST               14 (@py_assert1)
#            2106 LOAD_FAST                9 (@py_assert4)
#            2108 BUILD_TUPLE              2
#            2110 CALL                     4
#            2118 LOAD_CONST              13 ('line_12')
#            2120 LOAD_GLOBAL             23 (NULL + @py_builtins)
#            2130 LOAD_ATTR               24 (locals)
#            2150 CALL                     0
#            2158 CONTAINS_OP              0
#            2160 POP_JUMP_IF_TRUE        21 (to 2204)
#            2162 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            2172 LOAD_ATTR               26 (_should_repr_global_name)
#            2192 LOAD_FAST               13 (line_12)
#            2194 CALL                     1
#            2202 POP_JUMP_IF_FALSE       21 (to 2246)
#         >> 2204 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            2214 LOAD_ATTR               28 (_saferepr)
#            2234 LOAD_FAST               13 (line_12)
#            2236 CALL                     1
#            2244 JUMP_FORWARD             1 (to 2248)
#         >> 2246 LOAD_CONST              13 ('line_12')
#         >> 2248 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            2258 LOAD_ATTR               28 (_saferepr)
#            2278 LOAD_FAST               14 (@py_assert1)
#            2280 CALL                     1
#            2288 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            2298 LOAD_ATTR               28 (_saferepr)
#            2318 LOAD_FAST                9 (@py_assert4)
#            2320 CALL                     1
#            2328 LOAD_CONST              14 (('py0', 'py2', 'py5'))
#            2330 BUILD_CONST_KEY_MAP      3
#            2332 BINARY_OP                6 (%)
#            2336 STORE_FAST              16 (@py_format6)
#            2338 LOAD_CONST              15 ('assert %(py7)s')
#            2340 LOAD_CONST              16 ('py7')
#            2342 LOAD_FAST               16 (@py_format6)
#            2344 BUILD_MAP                1
#            2346 BINARY_OP                6 (%)
#            2350 STORE_FAST              17 (@py_format8)
#            2352 LOAD_GLOBAL             31 (NULL + AssertionError)
#            2362 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            2372 LOAD_ATTR               32 (_format_explanation)
#            2392 LOAD_FAST               17 (@py_format8)
#            2394 CALL                     1
#            2402 CALL                     1
#            2410 RAISE_VARARGS            1
#         >> 2412 LOAD_CONST               0 (None)
#            2414 COPY                     1
#            2416 STORE_FAST              14 (@py_assert1)
#            2418 COPY                     1
#            2420 STORE_FAST              15 (@py_assert3)
#            2422 STORE_FAST               9 (@py_assert4)
#            2424 RETURN_CONST             0 (None)
#         >> 2426 SWAP                     2
#            2428 POP_TOP
# 
# 178        2430 SWAP                     2
#            2432 STORE_FAST               5 (b)
#            2434 RERAISE                  0
#         >> 2436 SWAP                     2
#            2438 POP_TOP
# 
# 181        2440 SWAP                     2
#            2442 STORE_FAST              12 (l)
#            2444 RERAISE                  0
# ExceptionTable:
#   128 to 194 -> 2426 [2]
#   198 to 204 -> 2426 [2]
#   762 to 800 -> 2436 [2]
#   804 to 810 -> 2436 [2]
# 
# Disassembly of <code object test_branch_transformer_extraction at 0x3afaa950, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 187>:
# 187           0 RESUME                   0
# 
# 188           2 LOAD_GLOBAL              1 (NULL + CloudPSSModelConverter)
#              12 CALL                     0
#              20 STORE_FAST               1 (converter)
# 
# 189          22 LOAD_GLOBAL              3 (NULL + _MockTopology)
#              32 LOAD_GLOBAL              5 (NULL + _make_synthetic_topology)
#              42 CALL                     0
#              50 CALL                     1
#              58 STORE_FAST               2 (topo)
# 
# 191          60 LOAD_FAST                1 (converter)
#              62 LOAD_ATTR                7 (NULL|self + convert_to_model)
#              82 LOAD_FAST                2 (topo)
#              84 CALL                     1
#              92 UNPACK_SEQUENCE          2
#              96 STORE_FAST               3 (model)
#              98 STORE_FAST               4 (_)
# 
# 193         100 LOAD_FAST                3 (model)
#             102 LOAD_ATTR                8 (branches)
#             122 GET_ITER
#             124 LOAD_FAST_AND_CLEAR      5 (b)
#             126 SWAP                     2
#             128 BUILD_LIST               0
#             130 SWAP                     2
#         >>  132 FOR_ITER                34 (to 204)
#             136 STORE_FAST               5 (b)
#             138 LOAD_FAST                5 (b)
#             140 LOAD_ATTR               10 (branch_type)
#             160 LOAD_GLOBAL             12 (BranchType)
#             170 LOAD_ATTR               14 (TRANSFORMER)
#             190 COMPARE_OP              40 (==)
#             194 POP_JUMP_IF_TRUE         1 (to 198)
#             196 JUMP_BACKWARD           33 (to 132)
#         >>  198 LOAD_FAST                5 (b)
#             200 LIST_APPEND              2
#             202 JUMP_BACKWARD           36 (to 132)
#         >>  204 END_FOR
#             206 STORE_FAST               6 (trafos)
#             208 STORE_FAST               5 (b)
# 
# 194         210 LOAD_GLOBAL             17 (NULL + len)
#             220 LOAD_FAST                6 (trafos)
#             222 CALL                     1
#             230 STORE_FAST               7 (@py_assert2)
#             232 LOAD_CONST               1 (1)
#             234 STORE_FAST               8 (@py_assert5)
#             236 LOAD_FAST                7 (@py_assert2)
#             238 LOAD_FAST                8 (@py_assert5)
#             240 COMPARE_OP              40 (==)
#             244 STORE_FAST               9 (@py_assert4)
#             246 LOAD_FAST                9 (@py_assert4)
#             248 POP_JUMP_IF_TRUE       246 (to 742)
#             250 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             260 LOAD_ATTR               20 (_call_reprcompare)
#             280 LOAD_CONST               2 (('==',))
#             282 LOAD_FAST                9 (@py_assert4)
#             284 BUILD_TUPLE              1
#             286 LOAD_CONST               3 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             288 LOAD_FAST                7 (@py_assert2)
#             290 LOAD_FAST                8 (@py_assert5)
#             292 BUILD_TUPLE              2
#             294 CALL                     4
#             302 LOAD_CONST               4 ('len')
#             304 LOAD_GLOBAL             23 (NULL + @py_builtins)
#             314 LOAD_ATTR               24 (locals)
#             334 CALL                     0
#             342 CONTAINS_OP              0
#             344 POP_JUMP_IF_TRUE        25 (to 396)
#             346 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             356 LOAD_ATTR               26 (_should_repr_global_name)
#             376 LOAD_GLOBAL             16 (len)
#             386 CALL                     1
#             394 POP_JUMP_IF_FALSE       25 (to 446)
#         >>  396 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             406 LOAD_ATTR               28 (_saferepr)
#             426 LOAD_GLOBAL             16 (len)
#             436 CALL                     1
#             444 JUMP_FORWARD             1 (to 448)
#         >>  446 LOAD_CONST               4 ('len')
#         >>  448 LOAD_CONST               5 ('trafos')
#             450 LOAD_GLOBAL             23 (NULL + @py_builtins)
#             460 LOAD_ATTR               24 (locals)
#             480 CALL                     0
#             488 CONTAINS_OP              0
#             490 POP_JUMP_IF_TRUE        21 (to 534)
#             492 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             502 LOAD_ATTR               26 (_should_repr_global_name)
#             522 LOAD_FAST                6 (trafos)
#             524 CALL                     1
#             532 POP_JUMP_IF_FALSE       21 (to 576)
#         >>  534 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             544 LOAD_ATTR               28 (_saferepr)
#             564 LOAD_FAST                6 (trafos)
#             566 CALL                     1
#             574 JUMP_FORWARD             1 (to 578)
#         >>  576 LOAD_CONST               5 ('trafos')
#         >>  578 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             588 LOAD_ATTR               28 (_saferepr)
#             608 LOAD_FAST                7 (@py_assert2)
#             610 CALL                     1
#             618 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             628 LOAD_ATTR               28 (_saferepr)
#             648 LOAD_FAST                8 (@py_assert5)
#             650 CALL                     1
#             658 LOAD_CONST               6 (('py0', 'py1', 'py3', 'py6'))
#             660 BUILD_CONST_KEY_MAP      4
#             662 BINARY_OP                6 (%)
#             666 STORE_FAST              10 (@py_format7)
#             668 LOAD_CONST               7 ('assert %(py8)s')
#             670 LOAD_CONST               8 ('py8')
#             672 LOAD_FAST               10 (@py_format7)
#             674 BUILD_MAP                1
#             676 BINARY_OP                6 (%)
#             680 STORE_FAST              11 (@py_format9)
#             682 LOAD_GLOBAL             31 (NULL + AssertionError)
#             692 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             702 LOAD_ATTR               32 (_format_explanation)
#             722 LOAD_FAST               11 (@py_format9)
#             724 CALL                     1
#             732 CALL                     1
#             740 RAISE_VARARGS            1
#         >>  742 LOAD_CONST               0 (None)
#             744 COPY                     1
#             746 STORE_FAST               7 (@py_assert2)
#             748 COPY                     1
#             750 STORE_FAST               9 (@py_assert4)
#             752 STORE_FAST               8 (@py_assert5)
# 
# 196         754 LOAD_FAST                6 (trafos)
#             756 LOAD_CONST               9 (0)
#             758 BINARY_SUBSCR
#             762 STORE_FAST              12 (trafo)
# 
# 197         764 LOAD_FAST               12 (trafo)
#             766 LOAD_ATTR               34 (from_bus)
#             786 STORE_FAST              13 (@py_assert1)
#             788 LOAD_CONST              10 ('bus1')
#             790 STORE_FAST               9 (@py_assert4)
#             792 LOAD_FAST               13 (@py_assert1)
#             794 LOAD_FAST                9 (@py_assert4)
#             796 COMPARE_OP              40 (==)
#             800 STORE_FAST              14 (@py_assert3)
#             802 LOAD_FAST               14 (@py_assert3)
#             804 POP_JUMP_IF_TRUE       173 (to 1152)
#             806 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             816 LOAD_ATTR               20 (_call_reprcompare)
#             836 LOAD_CONST               2 (('==',))
#             838 LOAD_FAST               14 (@py_assert3)
#             840 BUILD_TUPLE              1
#             842 LOAD_CONST              11 (('%(py2)s\n{%(py2)s = %(py0)s.from_bus\n} == %(py5)s',))
#             844 LOAD_FAST               13 (@py_assert1)
#             846 LOAD_FAST                9 (@py_assert4)
#             848 BUILD_TUPLE              2
#             850 CALL                     4
#             858 LOAD_CONST              12 ('trafo')
#             860 LOAD_GLOBAL             23 (NULL + @py_builtins)
#             870 LOAD_ATTR               24 (locals)
#             890 CALL                     0
#             898 CONTAINS_OP              0
#             900 POP_JUMP_IF_TRUE        21 (to 944)
#             902 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             912 LOAD_ATTR               26 (_should_repr_global_name)
#             932 LOAD_FAST               12 (trafo)
#             934 CALL                     1
#             942 POP_JUMP_IF_FALSE       21 (to 986)
#         >>  944 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             954 LOAD_ATTR               28 (_saferepr)
#             974 LOAD_FAST               12 (trafo)
#             976 CALL                     1
#             984 JUMP_FORWARD             1 (to 988)
#         >>  986 LOAD_CONST              12 ('trafo')
#         >>  988 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             998 LOAD_ATTR               28 (_saferepr)
#            1018 LOAD_FAST               13 (@py_assert1)
#            1020 CALL                     1
#            1028 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1038 LOAD_ATTR               28 (_saferepr)
#            1058 LOAD_FAST                9 (@py_assert4)
#            1060 CALL                     1
#            1068 LOAD_CONST              13 (('py0', 'py2', 'py5'))
#            1070 BUILD_CONST_KEY_MAP      3
#            1072 BINARY_OP                6 (%)
#            1076 STORE_FAST              15 (@py_format6)
#            1078 LOAD_CONST              14 ('assert %(py7)s')
#            1080 LOAD_CONST              15 ('py7')
#            1082 LOAD_FAST               15 (@py_format6)
#            1084 BUILD_MAP                1
#            1086 BINARY_OP                6 (%)
#            1090 STORE_FAST              16 (@py_format8)
#            1092 LOAD_GLOBAL             31 (NULL + AssertionError)
#            1102 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1112 LOAD_ATTR               32 (_format_explanation)
#            1132 LOAD_FAST               16 (@py_format8)
#            1134 CALL                     1
#            1142 CALL                     1
#            1150 RAISE_VARARGS            1
#         >> 1152 LOAD_CONST               0 (None)
#            1154 COPY                     1
#            1156 STORE_FAST              13 (@py_assert1)
#            1158 COPY                     1
#            1160 STORE_FAST              14 (@py_assert3)
#            1162 STORE_FAST               9 (@py_assert4)
# 
# 198        1164 LOAD_FAST               12 (trafo)
#            1166 LOAD_ATTR               36 (to_bus)
#            1186 STORE_FAST              13 (@py_assert1)
#            1188 LOAD_CONST              16 ('bus3')
#            1190 STORE_FAST               9 (@py_assert4)
#            1192 LOAD_FAST               13 (@py_assert1)
#            1194 LOAD_FAST                9 (@py_assert4)
#            1196 COMPARE_OP              40 (==)
#            1200 STORE_FAST              14 (@py_assert3)
#            1202 LOAD_FAST               14 (@py_assert3)
#            1204 POP_JUMP_IF_TRUE       173 (to 1552)
#            1206 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1216 LOAD_ATTR               20 (_call_reprcompare)
#            1236 LOAD_CONST               2 (('==',))
#            1238 LOAD_FAST               14 (@py_assert3)
#            1240 BUILD_TUPLE              1
#            1242 LOAD_CONST              17 (('%(py2)s\n{%(py2)s = %(py0)s.to_bus\n} == %(py5)s',))
#            1244 LOAD_FAST               13 (@py_assert1)
#            1246 LOAD_FAST                9 (@py_assert4)
#            1248 BUILD_TUPLE              2
#            1250 CALL                     4
#            1258 LOAD_CONST              12 ('trafo')
#            1260 LOAD_GLOBAL             23 (NULL + @py_builtins)
#            1270 LOAD_ATTR               24 (locals)
#            1290 CALL                     0
#            1298 CONTAINS_OP              0
#            1300 POP_JUMP_IF_TRUE        21 (to 1344)
#            1302 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1312 LOAD_ATTR               26 (_should_repr_global_name)
#            1332 LOAD_FAST               12 (trafo)
#            1334 CALL                     1
#            1342 POP_JUMP_IF_FALSE       21 (to 1386)
#         >> 1344 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1354 LOAD_ATTR               28 (_saferepr)
#            1374 LOAD_FAST               12 (trafo)
#            1376 CALL                     1
#            1384 JUMP_FORWARD             1 (to 1388)
#         >> 1386 LOAD_CONST              12 ('trafo')
#         >> 1388 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1398 LOAD_ATTR               28 (_saferepr)
#            1418 LOAD_FAST               13 (@py_assert1)
#            1420 CALL                     1
#            1428 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1438 LOAD_ATTR               28 (_saferepr)
#            1458 LOAD_FAST                9 (@py_assert4)
#            1460 CALL                     1
#            1468 LOAD_CONST              13 (('py0', 'py2', 'py5'))
#            1470 BUILD_CONST_KEY_MAP      3
#            1472 BINARY_OP                6 (%)
#            1476 STORE_FAST              15 (@py_format6)
#            1478 LOAD_CONST              14 ('assert %(py7)s')
#            1480 LOAD_CONST              15 ('py7')
#            1482 LOAD_FAST               15 (@py_format6)
#            1484 BUILD_MAP                1
#            1486 BINARY_OP                6 (%)
#            1490 STORE_FAST              16 (@py_format8)
#            1492 LOAD_GLOBAL             31 (NULL + AssertionError)
#            1502 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1512 LOAD_ATTR               32 (_format_explanation)
#            1532 LOAD_FAST               16 (@py_format8)
#            1534 CALL                     1
#            1542 CALL                     1
#            1550 RAISE_VARARGS            1
#         >> 1552 LOAD_CONST               0 (None)
#            1554 COPY                     1
#            1556 STORE_FAST              13 (@py_assert1)
#            1558 COPY                     1
#            1560 STORE_FAST              14 (@py_assert3)
#            1562 STORE_FAST               9 (@py_assert4)
# 
# 199        1564 LOAD_FAST               12 (trafo)
#            1566 LOAD_ATTR               38 (tap_ratio)
#            1586 STORE_FAST              13 (@py_assert1)
#            1588 LOAD_GLOBAL             40 (pytest)
#            1598 LOAD_ATTR               42 (approx)
#            1618 STORE_FAST               8 (@py_assert5)
#            1620 LOAD_CONST              18 (345.0)
#            1622 STORE_FAST              17 (@py_assert7)
#            1624 LOAD_CONST              19 (230.0)
#            1626 STORE_FAST              18 (@py_assert9)
#            1628 LOAD_FAST               17 (@py_assert7)
#            1630 LOAD_FAST               18 (@py_assert9)
#            1632 BINARY_OP               11 (/)
#            1636 STORE_FAST              19 (@py_assert11)
#            1638 LOAD_CONST              20 (1e-06)
#            1640 STORE_FAST              20 (@py_assert12)
#            1642 PUSH_NULL
#            1644 LOAD_FAST                8 (@py_assert5)
#            1646 LOAD_FAST               19 (@py_assert11)
#            1648 LOAD_FAST               20 (@py_assert12)
#            1650 KW_NAMES                21 (('rel',))
#            1652 CALL                     2
#            1660 STORE_FAST              21 (@py_assert14)
#            1662 LOAD_FAST               13 (@py_assert1)
#            1664 LOAD_FAST               21 (@py_assert14)
#            1666 COMPARE_OP              40 (==)
#            1670 STORE_FAST              14 (@py_assert3)
#            1672 LOAD_FAST               14 (@py_assert3)
#            1674 EXTENDED_ARG             1
#            1676 POP_JUMP_IF_TRUE       326 (to 2330)
#            1678 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1688 LOAD_ATTR               20 (_call_reprcompare)
#            1708 LOAD_CONST               2 (('==',))
#            1710 LOAD_FAST               14 (@py_assert3)
#            1712 BUILD_TUPLE              1
#            1714 LOAD_CONST              22 (('%(py2)s\n{%(py2)s = %(py0)s.tap_ratio\n} == %(py15)s\n{%(py15)s = %(py6)s\n{%(py6)s = %(py4)s.approx\n}((%(py8)s / %(py10)s), rel=%(py13)s)\n}',))
#            1716 LOAD_FAST               13 (@py_assert1)
#            1718 LOAD_FAST               21 (@py_assert14)
#            1720 BUILD_TUPLE              2
#            1722 CALL                     4
#            1730 LOAD_CONST              12 ('trafo')
#            1732 LOAD_GLOBAL             23 (NULL + @py_builtins)
#            1742 LOAD_ATTR               24 (locals)
#            1762 CALL                     0
#            1770 CONTAINS_OP              0
#            1772 POP_JUMP_IF_TRUE        21 (to 1816)
#            1774 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1784 LOAD_ATTR               26 (_should_repr_global_name)
#            1804 LOAD_FAST               12 (trafo)
#            1806 CALL                     1
#            1814 POP_JUMP_IF_FALSE       21 (to 1858)
#         >> 1816 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1826 LOAD_ATTR               28 (_saferepr)
#            1846 LOAD_FAST               12 (trafo)
#            1848 CALL                     1
#            1856 JUMP_FORWARD             1 (to 1860)
#         >> 1858 LOAD_CONST              12 ('trafo')
#         >> 1860 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1870 LOAD_ATTR               28 (_saferepr)
#            1890 LOAD_FAST               13 (@py_assert1)
#            1892 CALL                     1
#            1900 LOAD_CONST              23 ('pytest')
#            1902 LOAD_GLOBAL             23 (NULL + @py_builtins)
#            1912 LOAD_ATTR               24 (locals)
#            1932 CALL                     0
#            1940 CONTAINS_OP              0
#            1942 POP_JUMP_IF_TRUE        25 (to 1994)
#            1944 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1954 LOAD_ATTR               26 (_should_repr_global_name)
#            1974 LOAD_GLOBAL             40 (pytest)
#            1984 CALL                     1
#            1992 POP_JUMP_IF_FALSE       25 (to 2044)
#         >> 1994 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            2004 LOAD_ATTR               28 (_saferepr)
#            2024 LOAD_GLOBAL             40 (pytest)
#            2034 CALL                     1
#            2042 JUMP_FORWARD             1 (to 2046)
#         >> 2044 LOAD_CONST              23 ('pytest')
#         >> 2046 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            2056 LOAD_ATTR               28 (_saferepr)
#            2076 LOAD_FAST                8 (@py_assert5)
#            2078 CALL                     1
#            2086 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            2096 LOAD_ATTR               28 (_saferepr)
#            2116 LOAD_FAST               17 (@py_assert7)
#            2118 CALL                     1
#            2126 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            2136 LOAD_ATTR               28 (_saferepr)
#            2156 LOAD_FAST               18 (@py_assert9)
#            2158 CALL                     1
#            2166 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            2176 LOAD_ATTR               28 (_saferepr)
#            2196 LOAD_FAST               20 (@py_assert12)
#            2198 CALL                     1
#            2206 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            2216 LOAD_ATTR               28 (_saferepr)
#            2236 LOAD_FAST               21 (@py_assert14)
#            2238 CALL                     1
#            2246 LOAD_CONST              24 (('py0', 'py2', 'py4', 'py6', 'py8', 'py10', 'py13', 'py15'))
#            2248 BUILD_CONST_KEY_MAP      8
#            2250 BINARY_OP                6 (%)
#            2254 STORE_FAST              22 (@py_format16)
#            2256 LOAD_CONST              25 ('assert %(py17)s')
#            2258 LOAD_CONST              26 ('py17')
#            2260 LOAD_FAST               22 (@py_format16)
#            2262 BUILD_MAP                1
#            2264 BINARY_OP                6 (%)
#            2268 STORE_FAST              23 (@py_format18)
#            2270 LOAD_GLOBAL             31 (NULL + AssertionError)
#            2280 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            2290 LOAD_ATTR               32 (_format_explanation)
#            2310 LOAD_FAST               23 (@py_format18)
#            2312 CALL                     1
#            2320 CALL                     1
#            2328 RAISE_VARARGS            1
#         >> 2330 LOAD_CONST               0 (None)
#            2332 COPY                     1
#            2334 STORE_FAST              13 (@py_assert1)
#            2336 COPY                     1
#            2338 STORE_FAST              14 (@py_assert3)
#            2340 COPY                     1
#            2342 STORE_FAST               8 (@py_assert5)
#            2344 COPY                     1
#            2346 STORE_FAST              17 (@py_assert7)
#            2348 COPY                     1
#            2350 STORE_FAST              18 (@py_assert9)
#            2352 COPY                     1
#            2354 STORE_FAST              19 (@py_assert11)
#            2356 COPY                     1
#            2358 STORE_FAST              20 (@py_assert12)
#            2360 STORE_FAST              21 (@py_assert14)
#            2362 RETURN_CONST             0 (None)
#         >> 2364 SWAP                     2
#            2366 POP_TOP
# 
# 193        2368 SWAP                     2
#            2370 STORE_FAST               5 (b)
#            2372 RERAISE                  0
# ExceptionTable:
#   128 to 194 -> 2364 [2]
#   198 to 204 -> 2364 [2]
# 
# Disassembly of <code object test_generator_extraction at 0x3afabb00, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 201>:
# 201           0 RESUME                   0
# 
# 202           2 LOAD_GLOBAL              1 (NULL + CloudPSSModelConverter)
#              12 CALL                     0
#              20 STORE_FAST               1 (converter)
# 
# 203          22 LOAD_GLOBAL              3 (NULL + _MockTopology)
#              32 LOAD_GLOBAL              5 (NULL + _make_synthetic_topology)
#              42 CALL                     0
#              50 CALL                     1
#              58 STORE_FAST               2 (topo)
# 
# 205          60 LOAD_FAST                1 (converter)
#              62 LOAD_ATTR                7 (NULL|self + convert_to_model)
#              82 LOAD_FAST                2 (topo)
#              84 CALL                     1
#              92 UNPACK_SEQUENCE          2
#              96 STORE_FAST               3 (model)
#              98 STORE_FAST               4 (_)
# 
# 207         100 LOAD_FAST                3 (model)
#             102 LOAD_ATTR                8 (generators)
#             122 LOAD_CONST               1 (0)
#             124 BINARY_SUBSCR
#             128 STORE_FAST               5 (gen)
# 
# 208         130 LOAD_FAST                5 (gen)
#             132 LOAD_ATTR               10 (name)
#             152 STORE_FAST               6 (@py_assert1)
#             154 LOAD_CONST               2 ('Gen1')
#             156 STORE_FAST               7 (@py_assert4)
#             158 LOAD_FAST                6 (@py_assert1)
#             160 LOAD_FAST                7 (@py_assert4)
#             162 COMPARE_OP              40 (==)
#             166 STORE_FAST               8 (@py_assert3)
#             168 LOAD_FAST                8 (@py_assert3)
#             170 POP_JUMP_IF_TRUE       173 (to 518)
#             172 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             182 LOAD_ATTR               14 (_call_reprcompare)
#             202 LOAD_CONST               3 (('==',))
#             204 LOAD_FAST                8 (@py_assert3)
#             206 BUILD_TUPLE              1
#             208 LOAD_CONST               4 (('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s',))
#             210 LOAD_FAST                6 (@py_assert1)
#             212 LOAD_FAST                7 (@py_assert4)
#             214 BUILD_TUPLE              2
#             216 CALL                     4
#             224 LOAD_CONST               5 ('gen')
#             226 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             236 LOAD_ATTR               18 (locals)
#             256 CALL                     0
#             264 CONTAINS_OP              0
#             266 POP_JUMP_IF_TRUE        21 (to 310)
#             268 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             278 LOAD_ATTR               20 (_should_repr_global_name)
#             298 LOAD_FAST                5 (gen)
#             300 CALL                     1
#             308 POP_JUMP_IF_FALSE       21 (to 352)
#         >>  310 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             320 LOAD_ATTR               22 (_saferepr)
#             340 LOAD_FAST                5 (gen)
#             342 CALL                     1
#             350 JUMP_FORWARD             1 (to 354)
#         >>  352 LOAD_CONST               5 ('gen')
#         >>  354 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             364 LOAD_ATTR               22 (_saferepr)
#             384 LOAD_FAST                6 (@py_assert1)
#             386 CALL                     1
#             394 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             404 LOAD_ATTR               22 (_saferepr)
#             424 LOAD_FAST                7 (@py_assert4)
#             426 CALL                     1
#             434 LOAD_CONST               6 (('py0', 'py2', 'py5'))
#             436 BUILD_CONST_KEY_MAP      3
#             438 BINARY_OP                6 (%)
#             442 STORE_FAST               9 (@py_format6)
#             444 LOAD_CONST               7 ('assert %(py7)s')
#             446 LOAD_CONST               8 ('py7')
#             448 LOAD_FAST                9 (@py_format6)
#             450 BUILD_MAP                1
#             452 BINARY_OP                6 (%)
#             456 STORE_FAST              10 (@py_format8)
#             458 LOAD_GLOBAL             25 (NULL + AssertionError)
#             468 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             478 LOAD_ATTR               26 (_format_explanation)
#             498 LOAD_FAST               10 (@py_format8)
#             500 CALL                     1
#             508 CALL                     1
#             516 RAISE_VARARGS            1
#         >>  518 LOAD_CONST               0 (None)
#             520 COPY                     1
#             522 STORE_FAST               6 (@py_assert1)
#             524 COPY                     1
#             526 STORE_FAST               8 (@py_assert3)
#             528 STORE_FAST               7 (@py_assert4)
# 
# 209         530 LOAD_FAST                5 (gen)
#             532 LOAD_ATTR               28 (bus)
#             552 STORE_FAST               6 (@py_assert1)
#             554 LOAD_CONST               9 ('bus1')
#             556 STORE_FAST               7 (@py_assert4)
#             558 LOAD_FAST                6 (@py_assert1)
#             560 LOAD_FAST                7 (@py_assert4)
#             562 COMPARE_OP              40 (==)
#             566 STORE_FAST               8 (@py_assert3)
#             568 LOAD_FAST                8 (@py_assert3)
#             570 POP_JUMP_IF_TRUE       173 (to 918)
#             572 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             582 LOAD_ATTR               14 (_call_reprcompare)
#             602 LOAD_CONST               3 (('==',))
#             604 LOAD_FAST                8 (@py_assert3)
#             606 BUILD_TUPLE              1
#             608 LOAD_CONST              10 (('%(py2)s\n{%(py2)s = %(py0)s.bus\n} == %(py5)s',))
#             610 LOAD_FAST                6 (@py_assert1)
#             612 LOAD_FAST                7 (@py_assert4)
#             614 BUILD_TUPLE              2
#             616 CALL                     4
#             624 LOAD_CONST               5 ('gen')
#             626 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             636 LOAD_ATTR               18 (locals)
#             656 CALL                     0
#             664 CONTAINS_OP              0
#             666 POP_JUMP_IF_TRUE        21 (to 710)
#             668 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             678 LOAD_ATTR               20 (_should_repr_global_name)
#             698 LOAD_FAST                5 (gen)
#             700 CALL                     1
#             708 POP_JUMP_IF_FALSE       21 (to 752)
#         >>  710 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             720 LOAD_ATTR               22 (_saferepr)
#             740 LOAD_FAST                5 (gen)
#             742 CALL                     1
#             750 JUMP_FORWARD             1 (to 754)
#         >>  752 LOAD_CONST               5 ('gen')
#         >>  754 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             764 LOAD_ATTR               22 (_saferepr)
#             784 LOAD_FAST                6 (@py_assert1)
#             786 CALL                     1
#             794 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             804 LOAD_ATTR               22 (_saferepr)
#             824 LOAD_FAST                7 (@py_assert4)
#             826 CALL                     1
#             834 LOAD_CONST               6 (('py0', 'py2', 'py5'))
#             836 BUILD_CONST_KEY_MAP      3
#             838 BINARY_OP                6 (%)
#             842 STORE_FAST               9 (@py_format6)
#             844 LOAD_CONST               7 ('assert %(py7)s')
#             846 LOAD_CONST               8 ('py7')
#             848 LOAD_FAST                9 (@py_format6)
#             850 BUILD_MAP                1
#             852 BINARY_OP                6 (%)
#             856 STORE_FAST              10 (@py_format8)
#             858 LOAD_GLOBAL             25 (NULL + AssertionError)
#             868 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             878 LOAD_ATTR               26 (_format_explanation)
#             898 LOAD_FAST               10 (@py_format8)
#             900 CALL                     1
#             908 CALL                     1
#             916 RAISE_VARARGS            1
#         >>  918 LOAD_CONST               0 (None)
#             920 COPY                     1
#             922 STORE_FAST               6 (@py_assert1)
#             924 COPY                     1
#             926 STORE_FAST               8 (@py_assert3)
#             928 STORE_FAST               7 (@py_assert4)
# 
# 210         930 LOAD_FAST                5 (gen)
#             932 LOAD_ATTR               30 (p_mw)
#             952 STORE_FAST               6 (@py_assert1)
#             954 LOAD_CONST              11 (100.0)
#             956 STORE_FAST               7 (@py_assert4)
#             958 LOAD_FAST                6 (@py_assert1)
#             960 LOAD_FAST                7 (@py_assert4)
#             962 COMPARE_OP              40 (==)
#             966 STORE_FAST               8 (@py_assert3)
#             968 LOAD_FAST                8 (@py_assert3)
#             970 POP_JUMP_IF_TRUE       173 (to 1318)
#             972 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             982 LOAD_ATTR               14 (_call_reprcompare)
#            1002 LOAD_CONST               3 (('==',))
#            1004 LOAD_FAST                8 (@py_assert3)
#            1006 BUILD_TUPLE              1
#            1008 LOAD_CONST              12 (('%(py2)s\n{%(py2)s = %(py0)s.p_mw\n} == %(py5)s',))
#            1010 LOAD_FAST                6 (@py_assert1)
#            1012 LOAD_FAST                7 (@py_assert4)
#            1014 BUILD_TUPLE              2
#            1016 CALL                     4
#            1024 LOAD_CONST               5 ('gen')
#            1026 LOAD_GLOBAL             17 (NULL + @py_builtins)
#            1036 LOAD_ATTR               18 (locals)
#            1056 CALL                     0
#            1064 CONTAINS_OP              0
#            1066 POP_JUMP_IF_TRUE        21 (to 1110)
#            1068 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1078 LOAD_ATTR               20 (_should_repr_global_name)
#            1098 LOAD_FAST                5 (gen)
#            1100 CALL                     1
#            1108 POP_JUMP_IF_FALSE       21 (to 1152)
#         >> 1110 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1120 LOAD_ATTR               22 (_saferepr)
#            1140 LOAD_FAST                5 (gen)
#            1142 CALL                     1
#            1150 JUMP_FORWARD             1 (to 1154)
#         >> 1152 LOAD_CONST               5 ('gen')
#         >> 1154 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1164 LOAD_ATTR               22 (_saferepr)
#            1184 LOAD_FAST                6 (@py_assert1)
#            1186 CALL                     1
#            1194 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1204 LOAD_ATTR               22 (_saferepr)
#            1224 LOAD_FAST                7 (@py_assert4)
#            1226 CALL                     1
#            1234 LOAD_CONST               6 (('py0', 'py2', 'py5'))
#            1236 BUILD_CONST_KEY_MAP      3
#            1238 BINARY_OP                6 (%)
#            1242 STORE_FAST               9 (@py_format6)
#            1244 LOAD_CONST               7 ('assert %(py7)s')
#            1246 LOAD_CONST               8 ('py7')
#            1248 LOAD_FAST                9 (@py_format6)
#            1250 BUILD_MAP                1
#            1252 BINARY_OP                6 (%)
#            1256 STORE_FAST              10 (@py_format8)
#            1258 LOAD_GLOBAL             25 (NULL + AssertionError)
#            1268 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1278 LOAD_ATTR               26 (_format_explanation)
#            1298 LOAD_FAST               10 (@py_format8)
#            1300 CALL                     1
#            1308 CALL                     1
#            1316 RAISE_VARARGS            1
#         >> 1318 LOAD_CONST               0 (None)
#            1320 COPY                     1
#            1322 STORE_FAST               6 (@py_assert1)
#            1324 COPY                     1
#            1326 STORE_FAST               8 (@py_assert3)
#            1328 STORE_FAST               7 (@py_assert4)
# 
# 211        1330 LOAD_FAST                5 (gen)
#            1332 LOAD_ATTR               32 (generator_type)
#            1352 STORE_FAST               6 (@py_assert1)
#            1354 LOAD_GLOBAL             34 (GeneratorType)
#            1364 LOAD_ATTR               36 (SYNCHRONOUS)
#            1384 STORE_FAST              11 (@py_assert5)
#            1386 LOAD_FAST                6 (@py_assert1)
#            1388 LOAD_FAST               11 (@py_assert5)
#            1390 COMPARE_OP              40 (==)
#            1394 STORE_FAST               8 (@py_assert3)
#            1396 LOAD_FAST                8 (@py_assert3)
#            1398 POP_JUMP_IF_TRUE       246 (to 1892)
#            1400 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1410 LOAD_ATTR               14 (_call_reprcompare)
#            1430 LOAD_CONST               3 (('==',))
#            1432 LOAD_FAST                8 (@py_assert3)
#            1434 BUILD_TUPLE              1
#            1436 LOAD_CONST              13 (('%(py2)s\n{%(py2)s = %(py0)s.generator_type\n} == %(py6)s\n{%(py6)s = %(py4)s.SYNCHRONOUS\n}',))
#            1438 LOAD_FAST                6 (@py_assert1)
#            1440 LOAD_FAST               11 (@py_assert5)
#            1442 BUILD_TUPLE              2
#            1444 CALL                     4
#            1452 LOAD_CONST               5 ('gen')
#            1454 LOAD_GLOBAL             17 (NULL + @py_builtins)
#            1464 LOAD_ATTR               18 (locals)
#            1484 CALL                     0
#            1492 CONTAINS_OP              0
#            1494 POP_JUMP_IF_TRUE        21 (to 1538)
#            1496 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1506 LOAD_ATTR               20 (_should_repr_global_name)
#            1526 LOAD_FAST                5 (gen)
#            1528 CALL                     1
#            1536 POP_JUMP_IF_FALSE       21 (to 1580)
#         >> 1538 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1548 LOAD_ATTR               22 (_saferepr)
#            1568 LOAD_FAST                5 (gen)
#            1570 CALL                     1
#            1578 JUMP_FORWARD             1 (to 1582)
#         >> 1580 LOAD_CONST               5 ('gen')
#         >> 1582 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1592 LOAD_ATTR               22 (_saferepr)
#            1612 LOAD_FAST                6 (@py_assert1)
#            1614 CALL                     1
#            1622 LOAD_CONST              14 ('GeneratorType')
#            1624 LOAD_GLOBAL             17 (NULL + @py_builtins)
#            1634 LOAD_ATTR               18 (locals)
#            1654 CALL                     0
#            1662 CONTAINS_OP              0
#            1664 POP_JUMP_IF_TRUE        25 (to 1716)
#            1666 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1676 LOAD_ATTR               20 (_should_repr_global_name)
#            1696 LOAD_GLOBAL             34 (GeneratorType)
#            1706 CALL                     1
#            1714 POP_JUMP_IF_FALSE       25 (to 1766)
#         >> 1716 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1726 LOAD_ATTR               22 (_saferepr)
#            1746 LOAD_GLOBAL             34 (GeneratorType)
#            1756 CALL                     1
#            1764 JUMP_FORWARD             1 (to 1768)
#         >> 1766 LOAD_CONST              14 ('GeneratorType')
#         >> 1768 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1778 LOAD_ATTR               22 (_saferepr)
#            1798 LOAD_FAST               11 (@py_assert5)
#            1800 CALL                     1
#            1808 LOAD_CONST              15 (('py0', 'py2', 'py4', 'py6'))
#            1810 BUILD_CONST_KEY_MAP      4
#            1812 BINARY_OP                6 (%)
#            1816 STORE_FAST              12 (@py_format7)
#            1818 LOAD_CONST              16 ('assert %(py8)s')
#            1820 LOAD_CONST              17 ('py8')
#            1822 LOAD_FAST               12 (@py_format7)
#            1824 BUILD_MAP                1
#            1826 BINARY_OP                6 (%)
#            1830 STORE_FAST              13 (@py_format9)
#            1832 LOAD_GLOBAL             25 (NULL + AssertionError)
#            1842 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1852 LOAD_ATTR               26 (_format_explanation)
#            1872 LOAD_FAST               13 (@py_format9)
#            1874 CALL                     1
#            1882 CALL                     1
#            1890 RAISE_VARARGS            1
#         >> 1892 LOAD_CONST               0 (None)
#            1894 COPY                     1
#            1896 STORE_FAST               6 (@py_assert1)
#            1898 COPY                     1
#            1900 STORE_FAST               8 (@py_assert3)
#            1902 STORE_FAST              11 (@py_assert5)
#            1904 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_load_extraction at 0x3aeca6c0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 213>:
# 213           0 RESUME                   0
# 
# 214           2 LOAD_GLOBAL              1 (NULL + CloudPSSModelConverter)
#              12 CALL                     0
#              20 STORE_FAST               1 (converter)
# 
# 215          22 LOAD_GLOBAL              3 (NULL + _MockTopology)
#              32 LOAD_GLOBAL              5 (NULL + _make_synthetic_topology)
#              42 CALL                     0
#              50 CALL                     1
#              58 STORE_FAST               2 (topo)
# 
# 217          60 LOAD_FAST                1 (converter)
#              62 LOAD_ATTR                7 (NULL|self + convert_to_model)
#              82 LOAD_FAST                2 (topo)
#              84 CALL                     1
#              92 UNPACK_SEQUENCE          2
#              96 STORE_FAST               3 (model)
#              98 STORE_FAST               4 (_)
# 
# 219         100 LOAD_FAST                3 (model)
#             102 LOAD_ATTR                9 (NULL|self + get_loads_at_bus)
#             122 LOAD_CONST               1 ('bus2')
#             124 CALL                     1
#             132 STORE_FAST               5 (load_2)
# 
# 220         134 LOAD_GLOBAL             11 (NULL + len)
#             144 LOAD_FAST                5 (load_2)
#             146 CALL                     1
#             154 STORE_FAST               6 (@py_assert2)
#             156 LOAD_CONST               2 (1)
#             158 STORE_FAST               7 (@py_assert5)
#             160 LOAD_FAST                6 (@py_assert2)
#             162 LOAD_FAST                7 (@py_assert5)
#             164 COMPARE_OP              40 (==)
#             168 STORE_FAST               8 (@py_assert4)
#             170 LOAD_FAST                8 (@py_assert4)
#             172 POP_JUMP_IF_TRUE       246 (to 666)
#             174 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             184 LOAD_ATTR               14 (_call_reprcompare)
#             204 LOAD_CONST               3 (('==',))
#             206 LOAD_FAST                8 (@py_assert4)
#             208 BUILD_TUPLE              1
#             210 LOAD_CONST               4 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             212 LOAD_FAST                6 (@py_assert2)
#             214 LOAD_FAST                7 (@py_assert5)
#             216 BUILD_TUPLE              2
#             218 CALL                     4
#             226 LOAD_CONST               5 ('len')
#             228 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             238 LOAD_ATTR               18 (locals)
#             258 CALL                     0
#             266 CONTAINS_OP              0
#             268 POP_JUMP_IF_TRUE        25 (to 320)
#             270 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             280 LOAD_ATTR               20 (_should_repr_global_name)
#             300 LOAD_GLOBAL             10 (len)
#             310 CALL                     1
#             318 POP_JUMP_IF_FALSE       25 (to 370)
#         >>  320 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             330 LOAD_ATTR               22 (_saferepr)
#             350 LOAD_GLOBAL             10 (len)
#             360 CALL                     1
#             368 JUMP_FORWARD             1 (to 372)
#         >>  370 LOAD_CONST               5 ('len')
#         >>  372 LOAD_CONST               6 ('load_2')
#             374 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             384 LOAD_ATTR               18 (locals)
#             404 CALL                     0
#             412 CONTAINS_OP              0
#             414 POP_JUMP_IF_TRUE        21 (to 458)
#             416 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             426 LOAD_ATTR               20 (_should_repr_global_name)
#             446 LOAD_FAST                5 (load_2)
#             448 CALL                     1
#             456 POP_JUMP_IF_FALSE       21 (to 500)
#         >>  458 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             468 LOAD_ATTR               22 (_saferepr)
#             488 LOAD_FAST                5 (load_2)
#             490 CALL                     1
#             498 JUMP_FORWARD             1 (to 502)
#         >>  500 LOAD_CONST               6 ('load_2')
#         >>  502 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             512 LOAD_ATTR               22 (_saferepr)
#             532 LOAD_FAST                6 (@py_assert2)
#             534 CALL                     1
#             542 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             552 LOAD_ATTR               22 (_saferepr)
#             572 LOAD_FAST                7 (@py_assert5)
#             574 CALL                     1
#             582 LOAD_CONST               7 (('py0', 'py1', 'py3', 'py6'))
#             584 BUILD_CONST_KEY_MAP      4
#             586 BINARY_OP                6 (%)
#             590 STORE_FAST               9 (@py_format7)
#             592 LOAD_CONST               8 ('assert %(py8)s')
#             594 LOAD_CONST               9 ('py8')
#             596 LOAD_FAST                9 (@py_format7)
#             598 BUILD_MAP                1
#             600 BINARY_OP                6 (%)
#             604 STORE_FAST              10 (@py_format9)
#             606 LOAD_GLOBAL             25 (NULL + AssertionError)
#             616 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             626 LOAD_ATTR               26 (_format_explanation)
#             646 LOAD_FAST               10 (@py_format9)
#             648 CALL                     1
#             656 CALL                     1
#             664 RAISE_VARARGS            1
#         >>  666 LOAD_CONST               0 (None)
#             668 COPY                     1
#             670 STORE_FAST               6 (@py_assert2)
#             672 COPY                     1
#             674 STORE_FAST               8 (@py_assert4)
#             676 STORE_FAST               7 (@py_assert5)
# 
# 221         678 LOAD_FAST                5 (load_2)
#             680 LOAD_CONST              10 (0)
#             682 BINARY_SUBSCR
#             686 STORE_FAST              11 (@py_assert0)
#             688 LOAD_FAST               11 (@py_assert0)
#             690 LOAD_ATTR               28 (p_mw)
#             710 STORE_FAST               6 (@py_assert2)
#             712 LOAD_CONST              11 (50.0)
#             714 STORE_FAST               7 (@py_assert5)
#             716 LOAD_FAST                6 (@py_assert2)
#             718 LOAD_FAST                7 (@py_assert5)
#             720 COMPARE_OP              40 (==)
#             724 STORE_FAST               8 (@py_assert4)
#             726 LOAD_FAST                8 (@py_assert4)
#             728 POP_JUMP_IF_TRUE       128 (to 986)
#             730 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             740 LOAD_ATTR               14 (_call_reprcompare)
#             760 LOAD_CONST               3 (('==',))
#             762 LOAD_FAST                8 (@py_assert4)
#             764 BUILD_TUPLE              1
#             766 LOAD_CONST              12 (('%(py3)s\n{%(py3)s = %(py1)s.p_mw\n} == %(py6)s',))
#             768 LOAD_FAST                6 (@py_assert2)
#             770 LOAD_FAST                7 (@py_assert5)
#             772 BUILD_TUPLE              2
#             774 CALL                     4
#             782 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             792 LOAD_ATTR               22 (_saferepr)
#             812 LOAD_FAST               11 (@py_assert0)
#             814 CALL                     1
#             822 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             832 LOAD_ATTR               22 (_saferepr)
#             852 LOAD_FAST                6 (@py_assert2)
#             854 CALL                     1
#             862 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             872 LOAD_ATTR               22 (_saferepr)
#             892 LOAD_FAST                7 (@py_assert5)
#             894 CALL                     1
#             902 LOAD_CONST              13 (('py1', 'py3', 'py6'))
#             904 BUILD_CONST_KEY_MAP      3
#             906 BINARY_OP                6 (%)
#             910 STORE_FAST               9 (@py_format7)
#             912 LOAD_CONST               8 ('assert %(py8)s')
#             914 LOAD_CONST               9 ('py8')
#             916 LOAD_FAST                9 (@py_format7)
#             918 BUILD_MAP                1
#             920 BINARY_OP                6 (%)
#             924 STORE_FAST              10 (@py_format9)
#             926 LOAD_GLOBAL             25 (NULL + AssertionError)
#             936 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             946 LOAD_ATTR               26 (_format_explanation)
#             966 LOAD_FAST               10 (@py_format9)
#             968 CALL                     1
#             976 CALL                     1
#             984 RAISE_VARARGS            1
#         >>  986 LOAD_CONST               0 (None)
#             988 COPY                     1
#             990 STORE_FAST              11 (@py_assert0)
#             992 COPY                     1
#             994 STORE_FAST               6 (@py_assert2)
#             996 COPY                     1
#             998 STORE_FAST               8 (@py_assert4)
#            1000 STORE_FAST               7 (@py_assert5)
# 
# 222        1002 LOAD_FAST                5 (load_2)
#            1004 LOAD_CONST              10 (0)
#            1006 BINARY_SUBSCR
#            1010 STORE_FAST              11 (@py_assert0)
#            1012 LOAD_FAST               11 (@py_assert0)
#            1014 LOAD_ATTR               30 (q_mvar)
#            1034 STORE_FAST               6 (@py_assert2)
#            1036 LOAD_CONST              14 (25.0)
#            1038 STORE_FAST               7 (@py_assert5)
#            1040 LOAD_FAST                6 (@py_assert2)
#            1042 LOAD_FAST                7 (@py_assert5)
#            1044 COMPARE_OP              40 (==)
#            1048 STORE_FAST               8 (@py_assert4)
#            1050 LOAD_FAST                8 (@py_assert4)
#            1052 POP_JUMP_IF_TRUE       128 (to 1310)
#            1054 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1064 LOAD_ATTR               14 (_call_reprcompare)
#            1084 LOAD_CONST               3 (('==',))
#            1086 LOAD_FAST                8 (@py_assert4)
#            1088 BUILD_TUPLE              1
#            1090 LOAD_CONST              15 (('%(py3)s\n{%(py3)s = %(py1)s.q_mvar\n} == %(py6)s',))
#            1092 LOAD_FAST                6 (@py_assert2)
#            1094 LOAD_FAST                7 (@py_assert5)
#            1096 BUILD_TUPLE              2
#            1098 CALL                     4
#            1106 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1116 LOAD_ATTR               22 (_saferepr)
#            1136 LOAD_FAST               11 (@py_assert0)
#            1138 CALL                     1
#            1146 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1156 LOAD_ATTR               22 (_saferepr)
#            1176 LOAD_FAST                6 (@py_assert2)
#            1178 CALL                     1
#            1186 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1196 LOAD_ATTR               22 (_saferepr)
#            1216 LOAD_FAST                7 (@py_assert5)
#            1218 CALL                     1
#            1226 LOAD_CONST              13 (('py1', 'py3', 'py6'))
#            1228 BUILD_CONST_KEY_MAP      3
#            1230 BINARY_OP                6 (%)
#            1234 STORE_FAST               9 (@py_format7)
#            1236 LOAD_CONST               8 ('assert %(py8)s')
#            1238 LOAD_CONST               9 ('py8')
#            1240 LOAD_FAST                9 (@py_format7)
#            1242 BUILD_MAP                1
#            1244 BINARY_OP                6 (%)
#            1248 STORE_FAST              10 (@py_format9)
#            1250 LOAD_GLOBAL             25 (NULL + AssertionError)
#            1260 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1270 LOAD_ATTR               26 (_format_explanation)
#            1290 LOAD_FAST               10 (@py_format9)
#            1292 CALL                     1
#            1300 CALL                     1
#            1308 RAISE_VARARGS            1
#         >> 1310 LOAD_CONST               0 (None)
#            1312 COPY                     1
#            1314 STORE_FAST              11 (@py_assert0)
#            1316 COPY                     1
#            1318 STORE_FAST               6 (@py_assert2)
#            1320 COPY                     1
#            1322 STORE_FAST               8 (@py_assert4)
#            1324 STORE_FAST               7 (@py_assert5)
# 
# 224        1326 LOAD_FAST                3 (model)
#            1328 LOAD_ATTR                9 (NULL|self + get_loads_at_bus)
#            1348 LOAD_CONST              16 ('bus3')
#            1350 CALL                     1
#            1358 STORE_FAST              12 (load_3)
# 
# 225        1360 LOAD_GLOBAL             11 (NULL + len)
#            1370 LOAD_FAST               12 (load_3)
#            1372 CALL                     1
#            1380 STORE_FAST               6 (@py_assert2)
#            1382 LOAD_CONST               2 (1)
#            1384 STORE_FAST               7 (@py_assert5)
#            1386 LOAD_FAST                6 (@py_assert2)
#            1388 LOAD_FAST                7 (@py_assert5)
#            1390 COMPARE_OP              40 (==)
#            1394 STORE_FAST               8 (@py_assert4)
#            1396 LOAD_FAST                8 (@py_assert4)
#            1398 POP_JUMP_IF_TRUE       246 (to 1892)
#            1400 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1410 LOAD_ATTR               14 (_call_reprcompare)
#            1430 LOAD_CONST               3 (('==',))
#            1432 LOAD_FAST                8 (@py_assert4)
#            1434 BUILD_TUPLE              1
#            1436 LOAD_CONST               4 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#            1438 LOAD_FAST                6 (@py_assert2)
#            1440 LOAD_FAST                7 (@py_assert5)
#            1442 BUILD_TUPLE              2
#            1444 CALL                     4
#            1452 LOAD_CONST               5 ('len')
#            1454 LOAD_GLOBAL             17 (NULL + @py_builtins)
#            1464 LOAD_ATTR               18 (locals)
#            1484 CALL                     0
#            1492 CONTAINS_OP              0
#            1494 POP_JUMP_IF_TRUE        25 (to 1546)
#            1496 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1506 LOAD_ATTR               20 (_should_repr_global_name)
#            1526 LOAD_GLOBAL             10 (len)
#            1536 CALL                     1
#            1544 POP_JUMP_IF_FALSE       25 (to 1596)
#         >> 1546 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1556 LOAD_ATTR               22 (_saferepr)
#            1576 LOAD_GLOBAL             10 (len)
#            1586 CALL                     1
#            1594 JUMP_FORWARD             1 (to 1598)
#         >> 1596 LOAD_CONST               5 ('len')
#         >> 1598 LOAD_CONST              17 ('load_3')
#            1600 LOAD_GLOBAL             17 (NULL + @py_builtins)
#            1610 LOAD_ATTR               18 (locals)
#            1630 CALL                     0
#            1638 CONTAINS_OP              0
#            1640 POP_JUMP_IF_TRUE        21 (to 1684)
#            1642 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1652 LOAD_ATTR               20 (_should_repr_global_name)
#            1672 LOAD_FAST               12 (load_3)
#            1674 CALL                     1
#            1682 POP_JUMP_IF_FALSE       21 (to 1726)
#         >> 1684 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1694 LOAD_ATTR               22 (_saferepr)
#            1714 LOAD_FAST               12 (load_3)
#            1716 CALL                     1
#            1724 JUMP_FORWARD             1 (to 1728)
#         >> 1726 LOAD_CONST              17 ('load_3')
#         >> 1728 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1738 LOAD_ATTR               22 (_saferepr)
#            1758 LOAD_FAST                6 (@py_assert2)
#            1760 CALL                     1
#            1768 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1778 LOAD_ATTR               22 (_saferepr)
#            1798 LOAD_FAST                7 (@py_assert5)
#            1800 CALL                     1
#            1808 LOAD_CONST               7 (('py0', 'py1', 'py3', 'py6'))
#            1810 BUILD_CONST_KEY_MAP      4
#            1812 BINARY_OP                6 (%)
#            1816 STORE_FAST               9 (@py_format7)
#            1818 LOAD_CONST               8 ('assert %(py8)s')
#            1820 LOAD_CONST               9 ('py8')
#            1822 LOAD_FAST                9 (@py_format7)
#            1824 BUILD_MAP                1
#            1826 BINARY_OP                6 (%)
#            1830 STORE_FAST              10 (@py_format9)
#            1832 LOAD_GLOBAL             25 (NULL + AssertionError)
#            1842 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1852 LOAD_ATTR               26 (_format_explanation)
#            1872 LOAD_FAST               10 (@py_format9)
#            1874 CALL                     1
#            1882 CALL                     1
#            1890 RAISE_VARARGS            1
#         >> 1892 LOAD_CONST               0 (None)
#            1894 COPY                     1
#            1896 STORE_FAST               6 (@py_assert2)
#            1898 COPY                     1
#            1900 STORE_FAST               8 (@py_assert4)
#            1902 STORE_FAST               7 (@py_assert5)
# 
# 226        1904 LOAD_FAST               12 (load_3)
#            1906 LOAD_CONST              10 (0)
#            1908 BINARY_SUBSCR
#            1912 STORE_FAST              11 (@py_assert0)
#            1914 LOAD_FAST               11 (@py_assert0)
#            1916 LOAD_ATTR               28 (p_mw)
#            1936 STORE_FAST               6 (@py_assert2)
#            1938 LOAD_CONST              18 (80.0)
#            1940 STORE_FAST               7 (@py_assert5)
#            1942 LOAD_FAST                6 (@py_assert2)
#            1944 LOAD_FAST                7 (@py_assert5)
#            1946 COMPARE_OP              40 (==)
#            1950 STORE_FAST               8 (@py_assert4)
#            1952 LOAD_FAST                8 (@py_assert4)
#            1954 POP_JUMP_IF_TRUE       128 (to 2212)
#            1956 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            1966 LOAD_ATTR               14 (_call_reprcompare)
#            1986 LOAD_CONST               3 (('==',))
#            1988 LOAD_FAST                8 (@py_assert4)
#            1990 BUILD_TUPLE              1
#            1992 LOAD_CONST              12 (('%(py3)s\n{%(py3)s = %(py1)s.p_mw\n} == %(py6)s',))
#            1994 LOAD_FAST                6 (@py_assert2)
#            1996 LOAD_FAST                7 (@py_assert5)
#            1998 BUILD_TUPLE              2
#            2000 CALL                     4
#            2008 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            2018 LOAD_ATTR               22 (_saferepr)
#            2038 LOAD_FAST               11 (@py_assert0)
#            2040 CALL                     1
#            2048 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            2058 LOAD_ATTR               22 (_saferepr)
#            2078 LOAD_FAST                6 (@py_assert2)
#            2080 CALL                     1
#            2088 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            2098 LOAD_ATTR               22 (_saferepr)
#            2118 LOAD_FAST                7 (@py_assert5)
#            2120 CALL                     1
#            2128 LOAD_CONST              13 (('py1', 'py3', 'py6'))
#            2130 BUILD_CONST_KEY_MAP      3
#            2132 BINARY_OP                6 (%)
#            2136 STORE_FAST               9 (@py_format7)
#            2138 LOAD_CONST               8 ('assert %(py8)s')
#            2140 LOAD_CONST               9 ('py8')
#            2142 LOAD_FAST                9 (@py_format7)
#            2144 BUILD_MAP                1
#            2146 BINARY_OP                6 (%)
#            2150 STORE_FAST              10 (@py_format9)
#            2152 LOAD_GLOBAL             25 (NULL + AssertionError)
#            2162 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            2172 LOAD_ATTR               26 (_format_explanation)
#            2192 LOAD_FAST               10 (@py_format9)
#            2194 CALL                     1
#            2202 CALL                     1
#            2210 RAISE_VARARGS            1
#         >> 2212 LOAD_CONST               0 (None)
#            2214 COPY                     1
#            2216 STORE_FAST              11 (@py_assert0)
#            2218 COPY                     1
#            2220 STORE_FAST               6 (@py_assert2)
#            2222 COPY                     1
#            2224 STORE_FAST               8 (@py_assert4)
#            2226 STORE_FAST               7 (@py_assert5)
# 
# 227        2228 LOAD_FAST               12 (load_3)
#            2230 LOAD_CONST              10 (0)
#            2232 BINARY_SUBSCR
#            2236 STORE_FAST              11 (@py_assert0)
#            2238 LOAD_FAST               11 (@py_assert0)
#            2240 LOAD_ATTR               30 (q_mvar)
#            2260 STORE_FAST               6 (@py_assert2)
#            2262 LOAD_CONST              19 (40.0)
#            2264 STORE_FAST               7 (@py_assert5)
#            2266 LOAD_FAST                6 (@py_assert2)
#            2268 LOAD_FAST                7 (@py_assert5)
#            2270 COMPARE_OP              40 (==)
#            2274 STORE_FAST               8 (@py_assert4)
#            2276 LOAD_FAST                8 (@py_assert4)
#            2278 POP_JUMP_IF_TRUE       128 (to 2536)
#            2280 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            2290 LOAD_ATTR               14 (_call_reprcompare)
#            2310 LOAD_CONST               3 (('==',))
#            2312 LOAD_FAST                8 (@py_assert4)
#            2314 BUILD_TUPLE              1
#            2316 LOAD_CONST              15 (('%(py3)s\n{%(py3)s = %(py1)s.q_mvar\n} == %(py6)s',))
#            2318 LOAD_FAST                6 (@py_assert2)
#            2320 LOAD_FAST                7 (@py_assert5)
#            2322 BUILD_TUPLE              2
#            2324 CALL                     4
#            2332 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            2342 LOAD_ATTR               22 (_saferepr)
#            2362 LOAD_FAST               11 (@py_assert0)
#            2364 CALL                     1
#            2372 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            2382 LOAD_ATTR               22 (_saferepr)
#            2402 LOAD_FAST                6 (@py_assert2)
#            2404 CALL                     1
#            2412 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            2422 LOAD_ATTR               22 (_saferepr)
#            2442 LOAD_FAST                7 (@py_assert5)
#            2444 CALL                     1
#            2452 LOAD_CONST              13 (('py1', 'py3', 'py6'))
#            2454 BUILD_CONST_KEY_MAP      3
#            2456 BINARY_OP                6 (%)
#            2460 STORE_FAST               9 (@py_format7)
#            2462 LOAD_CONST               8 ('assert %(py8)s')
#            2464 LOAD_CONST               9 ('py8')
#            2466 LOAD_FAST                9 (@py_format7)
#            2468 BUILD_MAP                1
#            2470 BINARY_OP                6 (%)
#            2474 STORE_FAST              10 (@py_format9)
#            2476 LOAD_GLOBAL             25 (NULL + AssertionError)
#            2486 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#            2496 LOAD_ATTR               26 (_format_explanation)
#            2516 LOAD_FAST               10 (@py_format9)
#            2518 CALL                     1
#            2526 CALL                     1
#            2534 RAISE_VARARGS            1
#         >> 2536 LOAD_CONST               0 (None)
#            2538 COPY                     1
#            2540 STORE_FAST              11 (@py_assert0)
#            2542 COPY                     1
#            2544 STORE_FAST               6 (@py_assert2)
#            2546 COPY                     1
#            2548 STORE_FAST               8 (@py_assert4)
#            2550 STORE_FAST               7 (@py_assert5)
#            2552 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_topology_validation at 0x3af96680, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 229>:
# 229           0 RESUME                   0
# 
# 230           2 LOAD_GLOBAL              1 (NULL + CloudPSSModelConverter)
#              12 CALL                     0
#              20 STORE_FAST               1 (converter)
# 
# 231          22 LOAD_GLOBAL              3 (NULL + _MockTopology)
#              32 LOAD_GLOBAL              5 (NULL + _make_synthetic_topology)
#              42 CALL                     0
#              50 CALL                     1
#              58 STORE_FAST               2 (topo)
# 
# 233          60 LOAD_FAST                1 (converter)
#              62 LOAD_ATTR                7 (NULL|self + convert_to_model)
#              82 LOAD_FAST                2 (topo)
#              84 CALL                     1
#              92 UNPACK_SEQUENCE          2
#              96 STORE_FAST               3 (model)
#              98 STORE_FAST               4 (report)
# 
# 235         100 LOAD_FAST                3 (model)
#             102 LOAD_ATTR                9 (NULL|self + validate_topology)
#             122 CALL                     0
#             130 STORE_FAST               5 (topology_errors)
# 
# 236         132 LOAD_FAST                5 (topology_errors)
#             134 GET_ITER
#             136 LOAD_FAST_AND_CLEAR      6 (e)
#             138 SWAP                     2
#             140 BUILD_LIST               0
#             142 SWAP                     2
#         >>  144 FOR_ITER                 9 (to 166)
#             148 STORE_FAST               6 (e)
#             150 LOAD_CONST               1 ('not found')
#             152 LOAD_FAST                6 (e)
#             154 CONTAINS_OP              0
#             156 POP_JUMP_IF_TRUE         1 (to 160)
#             158 JUMP_BACKWARD            8 (to 144)
#         >>  160 LOAD_FAST                6 (e)
#             162 LIST_APPEND              2
#             164 JUMP_BACKWARD           11 (to 144)
#         >>  166 END_FOR
#             168 STORE_FAST               7 (slack_errors)
#             170 STORE_FAST               6 (e)
# 
# 237         172 LOAD_GLOBAL             11 (NULL + len)
#             182 LOAD_FAST                7 (slack_errors)
#             184 CALL                     1
#             192 STORE_FAST               8 (@py_assert2)
#             194 LOAD_CONST               2 (0)
#             196 STORE_FAST               9 (@py_assert5)
#             198 LOAD_FAST                8 (@py_assert2)
#             200 LOAD_FAST                9 (@py_assert5)
#             202 COMPARE_OP              40 (==)
#             206 STORE_FAST              10 (@py_assert4)
#             208 LOAD_FAST               10 (@py_assert4)
#             210 EXTENDED_ARG             1
#             212 POP_JUMP_IF_TRUE       271 (to 756)
#             214 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             224 LOAD_ATTR               14 (_call_reprcompare)
#             244 LOAD_CONST               3 (('==',))
#             246 LOAD_FAST               10 (@py_assert4)
#             248 BUILD_TUPLE              1
#             250 LOAD_CONST               4 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             252 LOAD_FAST                8 (@py_assert2)
#             254 LOAD_FAST                9 (@py_assert5)
#             256 BUILD_TUPLE              2
#             258 CALL                     4
#             266 LOAD_CONST               5 ('len')
#             268 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             278 LOAD_ATTR               18 (locals)
#             298 CALL                     0
#             306 CONTAINS_OP              0
#             308 POP_JUMP_IF_TRUE        25 (to 360)
#             310 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             320 LOAD_ATTR               20 (_should_repr_global_name)
#             340 LOAD_GLOBAL             10 (len)
#             350 CALL                     1
#             358 POP_JUMP_IF_FALSE       25 (to 410)
#         >>  360 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             370 LOAD_ATTR               22 (_saferepr)
#             390 LOAD_GLOBAL             10 (len)
#             400 CALL                     1
#             408 JUMP_FORWARD             1 (to 412)
#         >>  410 LOAD_CONST               5 ('len')
#         >>  412 LOAD_CONST               6 ('slack_errors')
#             414 LOAD_GLOBAL             17 (NULL + @py_builtins)
#             424 LOAD_ATTR               18 (locals)
#             444 CALL                     0
#             452 CONTAINS_OP              0
#             454 POP_JUMP_IF_TRUE        21 (to 498)
#             456 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             466 LOAD_ATTR               20 (_should_repr_global_name)
#             486 LOAD_FAST                7 (slack_errors)
#             488 CALL                     1
#             496 POP_JUMP_IF_FALSE       21 (to 540)
#         >>  498 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             508 LOAD_ATTR               22 (_saferepr)
#             528 LOAD_FAST                7 (slack_errors)
#             530 CALL                     1
#             538 JUMP_FORWARD             1 (to 542)
#         >>  540 LOAD_CONST               6 ('slack_errors')
#         >>  542 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             552 LOAD_ATTR               22 (_saferepr)
#             572 LOAD_FAST                8 (@py_assert2)
#             574 CALL                     1
#             582 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             592 LOAD_ATTR               22 (_saferepr)
#             612 LOAD_FAST                9 (@py_assert5)
#             614 CALL                     1
#             622 LOAD_CONST               7 (('py0', 'py1', 'py3', 'py6'))
#             624 BUILD_CONST_KEY_MAP      4
#             626 BINARY_OP                6 (%)
#             630 STORE_FAST              11 (@py_format7)
#             632 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             642 LOAD_ATTR               24 (_format_assertmsg)
#             662 LOAD_CONST               8 ('Connectivity errors: ')
#             664 LOAD_FAST                7 (slack_errors)
#             666 FORMAT_VALUE             0
#             668 BUILD_STRING             2
#             670 CALL                     1
#             678 LOAD_CONST               9 ('\n>assert %(py8)s')
#             680 BINARY_OP                0 (+)
#             684 LOAD_CONST              10 ('py8')
#             686 LOAD_FAST               11 (@py_format7)
#             688 BUILD_MAP                1
#             690 BINARY_OP                6 (%)
#             694 STORE_FAST              12 (@py_format9)
#             696 LOAD_GLOBAL             27 (NULL + AssertionError)
#             706 LOAD_GLOBAL             13 (NULL + @pytest_ar)
#             716 LOAD_ATTR               28 (_format_explanation)
#             736 LOAD_FAST               12 (@py_format9)
#             738 CALL                     1
#             746 CALL                     1
#             754 RAISE_VARARGS            1
#         >>  756 LOAD_CONST               0 (None)
#             758 COPY                     1
#             760 STORE_FAST               8 (@py_assert2)
#             762 COPY                     1
#             764 STORE_FAST              10 (@py_assert4)
#             766 STORE_FAST               9 (@py_assert5)
#             768 RETURN_CONST             0 (None)
#         >>  770 SWAP                     2
#             772 POP_TOP
# 
# 236         774 SWAP                     2
#             776 STORE_FAST               6 (e)
#             778 RERAISE                  0
# ExceptionTable:
#   140 to 156 -> 770 [2]
#   160 to 166 -> 770 [2]
# 
# Disassembly of <code object test_invalid_source_error at 0x3af9bd40, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 239>:
# 239           0 RESUME                   0
# 
# 240           2 LOAD_GLOBAL              1 (NULL + CloudPSSModelConverter)
#              12 CALL                     0
#              20 STORE_FAST               1 (converter)
# 
# 241          22 LOAD_FAST                1 (converter)
#              24 LOAD_ATTR                3 (NULL|self + convert_to_model)
#              44 LOAD_CONST               1 ('not_a_model')
#              46 CALL                     1
#              54 UNPACK_SEQUENCE          2
#              58 STORE_FAST               2 (model_obj)
#              60 STORE_FAST               3 (report)
# 
# 243          62 LOAD_FAST                3 (report)
#              64 LOAD_ATTR                4 (is_success)
#              84 STORE_FAST               4 (@py_assert1)
#              86 LOAD_FAST                4 (@py_assert1)
#              88 UNARY_NOT
#              90 STORE_FAST               5 (@py_assert3)
#              92 LOAD_FAST                5 (@py_assert3)
#              94 POP_JUMP_IF_TRUE       121 (to 338)
#              96 LOAD_CONST               2 ('assert not %(py2)s\n{%(py2)s = %(py0)s.is_success\n}')
#              98 LOAD_CONST               3 ('report')
#             100 LOAD_GLOBAL              7 (NULL + @py_builtins)
#             110 LOAD_ATTR                8 (locals)
#             130 CALL                     0
#             138 CONTAINS_OP              0
#             140 POP_JUMP_IF_TRUE        21 (to 184)
#             142 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             152 LOAD_ATTR               12 (_should_repr_global_name)
#             172 LOAD_FAST                3 (report)
#             174 CALL                     1
#             182 POP_JUMP_IF_FALSE       21 (to 226)
#         >>  184 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             194 LOAD_ATTR               14 (_saferepr)
#             214 LOAD_FAST                3 (report)
#             216 CALL                     1
#             224 JUMP_FORWARD             1 (to 228)
#         >>  226 LOAD_CONST               3 ('report')
#         >>  228 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             238 LOAD_ATTR               14 (_saferepr)
#             258 LOAD_FAST                4 (@py_assert1)
#             260 CALL                     1
#             268 LOAD_CONST               4 (('py0', 'py2'))
#             270 BUILD_CONST_KEY_MAP      2
#             272 BINARY_OP                6 (%)
#             276 STORE_FAST               6 (@py_format4)
#             278 LOAD_GLOBAL             17 (NULL + AssertionError)
#             288 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             298 LOAD_ATTR               18 (_format_explanation)
#             318 LOAD_FAST                6 (@py_format4)
#             320 CALL                     1
#             328 CALL                     1
#             336 RAISE_VARARGS            1
#         >>  338 LOAD_CONST               0 (None)
#             340 COPY                     1
#             342 STORE_FAST               4 (@py_assert1)
#             344 STORE_FAST               5 (@py_assert3)
# 
# 244         346 LOAD_FAST                3 (report)
#             348 LOAD_ATTR               20 (errors)
#             368 STORE_FAST               7 (@py_assert2)
#             370 LOAD_GLOBAL             23 (NULL + len)
#             380 LOAD_FAST                7 (@py_assert2)
#             382 CALL                     1
#             390 STORE_FAST               8 (@py_assert4)
#             392 LOAD_CONST               5 (0)
#             394 STORE_FAST               9 (@py_assert7)
#             396 LOAD_FAST                8 (@py_assert4)
#             398 LOAD_FAST                9 (@py_assert7)
#             400 COMPARE_OP              68 (>)
#             404 STORE_FAST              10 (@py_assert6)
#             406 LOAD_FAST               10 (@py_assert6)
#             408 EXTENDED_ARG             1
#             410 POP_JUMP_IF_TRUE       266 (to 944)
#             412 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             422 LOAD_ATTR               24 (_call_reprcompare)
#             442 LOAD_CONST               6 (('>',))
#             444 LOAD_FAST               10 (@py_assert6)
#             446 BUILD_TUPLE              1
#             448 LOAD_CONST               7 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.errors\n})\n} > %(py8)s',))
#             450 LOAD_FAST                8 (@py_assert4)
#             452 LOAD_FAST                9 (@py_assert7)
#             454 BUILD_TUPLE              2
#             456 CALL                     4
#             464 LOAD_CONST               8 ('len')
#             466 LOAD_GLOBAL              7 (NULL + @py_builtins)
#             476 LOAD_ATTR                8 (locals)
#             496 CALL                     0
#             504 CONTAINS_OP              0
#             506 POP_JUMP_IF_TRUE        25 (to 558)
#             508 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             518 LOAD_ATTR               12 (_should_repr_global_name)
#             538 LOAD_GLOBAL             22 (len)
#             548 CALL                     1
#             556 POP_JUMP_IF_FALSE       25 (to 608)
#         >>  558 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             568 LOAD_ATTR               14 (_saferepr)
#             588 LOAD_GLOBAL             22 (len)
#             598 CALL                     1
#             606 JUMP_FORWARD             1 (to 610)
#         >>  608 LOAD_CONST               8 ('len')
#         >>  610 LOAD_CONST               3 ('report')
#             612 LOAD_GLOBAL              7 (NULL + @py_builtins)
#             622 LOAD_ATTR                8 (locals)
#             642 CALL                     0
#             650 CONTAINS_OP              0
#             652 POP_JUMP_IF_TRUE        21 (to 696)
#             654 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             664 LOAD_ATTR               12 (_should_repr_global_name)
#             684 LOAD_FAST                3 (report)
#             686 CALL                     1
#             694 POP_JUMP_IF_FALSE       21 (to 738)
#         >>  696 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             706 LOAD_ATTR               14 (_saferepr)
#             726 LOAD_FAST                3 (report)
#             728 CALL                     1
#             736 JUMP_FORWARD             1 (to 740)
#         >>  738 LOAD_CONST               3 ('report')
#         >>  740 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             750 LOAD_ATTR               14 (_saferepr)
#             770 LOAD_FAST                7 (@py_assert2)
#             772 CALL                     1
#             780 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             790 LOAD_ATTR               14 (_saferepr)
#             810 LOAD_FAST                8 (@py_assert4)
#             812 CALL                     1
#             820 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             830 LOAD_ATTR               14 (_saferepr)
#             850 LOAD_FAST                9 (@py_assert7)
#             852 CALL                     1
#             860 LOAD_CONST               9 (('py0', 'py1', 'py3', 'py5', 'py8'))
#             862 BUILD_CONST_KEY_MAP      5
#             864 BINARY_OP                6 (%)
#             868 STORE_FAST              11 (@py_format9)
#             870 LOAD_CONST              10 ('assert %(py10)s')
#             872 LOAD_CONST              11 ('py10')
#             874 LOAD_FAST               11 (@py_format9)
#             876 BUILD_MAP                1
#             878 BINARY_OP                6 (%)
#             882 STORE_FAST              12 (@py_format11)
#             884 LOAD_GLOBAL             17 (NULL + AssertionError)
#             894 LOAD_GLOBAL             11 (NULL + @pytest_ar)
#             904 LOAD_ATTR               18 (_format_explanation)
#             924 LOAD_FAST               12 (@py_format11)
#             926 CALL                     1
#             934 CALL                     1
#             942 RAISE_VARARGS            1
#         >>  944 LOAD_CONST               0 (None)
#             946 COPY                     1
#             948 STORE_FAST               7 (@py_assert2)
#             950 COPY                     1
#             952 STORE_FAST               8 (@py_assert4)
#             954 COPY                     1
#             956 STORE_FAST              10 (@py_assert6)
#             958 STORE_FAST               9 (@py_assert7)
#             960 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_convert_from_model_roundtrip at 0x3aecbce0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 246>:
# 246           0 RESUME                   0
# 
# 247           2 LOAD_GLOBAL              1 (NULL + CloudPSSModelConverter)
#              12 CALL                     0
#              20 STORE_FAST               1 (converter)
# 
# 248          22 LOAD_GLOBAL              3 (NULL + _make_synthetic_topology)
#              32 CALL                     0
#              40 STORE_FAST               2 (topo_dict)
# 
# 249          42 LOAD_GLOBAL              5 (NULL + _MockTopology)
#              52 LOAD_FAST                2 (topo_dict)
#              54 CALL                     1
#              62 STORE_FAST               3 (topo)
# 
# 251          64 LOAD_FAST                1 (converter)
#              66 LOAD_ATTR                7 (NULL|self + convert_to_model)
#              86 LOAD_FAST                3 (topo)
#              88 CALL                     1
#              96 UNPACK_SEQUENCE          2
#             100 STORE_FAST               4 (model)
#             102 STORE_FAST               5 (_)
# 
# 253         104 LOAD_FAST                1 (converter)
#             106 LOAD_ATTR                9 (NULL|self + convert_from_model)
#             126 LOAD_FAST                4 (model)
#             128 CALL                     1
#             136 UNPACK_SEQUENCE          2
#             140 STORE_FAST               6 (result)
#             142 STORE_FAST               7 (report)
# 
# 255         144 LOAD_FAST                7 (report)
#             146 LOAD_ATTR               10 (is_success)
#             166 STORE_FAST               8 (@py_assert1)
#             168 LOAD_FAST                8 (@py_assert1)
#             170 POP_JUMP_IF_TRUE       121 (to 414)
#             172 LOAD_CONST               1 ('assert %(py2)s\n{%(py2)s = %(py0)s.is_success\n}')
#             174 LOAD_CONST               2 ('report')
#             176 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             186 LOAD_ATTR               14 (locals)
#             206 CALL                     0
#             214 CONTAINS_OP              0
#             216 POP_JUMP_IF_TRUE        21 (to 260)
#             218 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             228 LOAD_ATTR               18 (_should_repr_global_name)
#             248 LOAD_FAST                7 (report)
#             250 CALL                     1
#             258 POP_JUMP_IF_FALSE       21 (to 302)
#         >>  260 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             270 LOAD_ATTR               20 (_saferepr)
#             290 LOAD_FAST                7 (report)
#             292 CALL                     1
#             300 JUMP_FORWARD             1 (to 304)
#         >>  302 LOAD_CONST               2 ('report')
#         >>  304 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             314 LOAD_ATTR               20 (_saferepr)
#             334 LOAD_FAST                8 (@py_assert1)
#             336 CALL                     1
#             344 LOAD_CONST               3 (('py0', 'py2'))
#             346 BUILD_CONST_KEY_MAP      2
#             348 BINARY_OP                6 (%)
#             352 STORE_FAST               9 (@py_format3)
#             354 LOAD_GLOBAL             23 (NULL + AssertionError)
#             364 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             374 LOAD_ATTR               24 (_format_explanation)
#             394 LOAD_FAST                9 (@py_format3)
#             396 CALL                     1
#             404 CALL                     1
#             412 RAISE_VARARGS            1
#         >>  414 LOAD_CONST               0 (None)
#             416 STORE_FAST               8 (@py_assert1)
# 
# 256         418 LOAD_CONST               4 ('components')
#             420 STORE_FAST              10 (@py_assert0)
#             422 LOAD_FAST               10 (@py_assert0)
#             424 LOAD_FAST                6 (result)
#             426 CONTAINS_OP              0
#             428 STORE_FAST              11 (@py_assert2)
#             430 LOAD_FAST               11 (@py_assert2)
#             432 POP_JUMP_IF_TRUE       153 (to 740)
#             434 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             444 LOAD_ATTR               26 (_call_reprcompare)
#             464 LOAD_CONST               5 (('in',))
#             466 LOAD_FAST               11 (@py_assert2)
#             468 BUILD_TUPLE              1
#             470 LOAD_CONST               6 (('%(py1)s in %(py3)s',))
#             472 LOAD_FAST               10 (@py_assert0)
#             474 LOAD_FAST                6 (result)
#             476 BUILD_TUPLE              2
#             478 CALL                     4
#             486 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             496 LOAD_ATTR               20 (_saferepr)
#             516 LOAD_FAST               10 (@py_assert0)
#             518 CALL                     1
#             526 LOAD_CONST               7 ('result')
#             528 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             538 LOAD_ATTR               14 (locals)
#             558 CALL                     0
#             566 CONTAINS_OP              0
#             568 POP_JUMP_IF_TRUE        21 (to 612)
#             570 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             580 LOAD_ATTR               18 (_should_repr_global_name)
#             600 LOAD_FAST                6 (result)
#             602 CALL                     1
#             610 POP_JUMP_IF_FALSE       21 (to 654)
#         >>  612 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             622 LOAD_ATTR               20 (_saferepr)
#             642 LOAD_FAST                6 (result)
#             644 CALL                     1
#             652 JUMP_FORWARD             1 (to 656)
#         >>  654 LOAD_CONST               7 ('result')
#         >>  656 LOAD_CONST               8 (('py1', 'py3'))
#             658 BUILD_CONST_KEY_MAP      2
#             660 BINARY_OP                6 (%)
#             664 STORE_FAST              12 (@py_format4)
#             666 LOAD_CONST               9 ('assert %(py5)s')
#             668 LOAD_CONST              10 ('py5')
#             670 LOAD_FAST               12 (@py_format4)
#             672 BUILD_MAP                1
#             674 BINARY_OP                6 (%)
#             678 STORE_FAST              13 (@py_format6)
#             680 LOAD_GLOBAL             23 (NULL + AssertionError)
#             690 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             700 LOAD_ATTR               24 (_format_explanation)
#             720 LOAD_FAST               13 (@py_format6)
#             722 CALL                     1
#             730 CALL                     1
#             738 RAISE_VARARGS            1
#         >>  740 LOAD_CONST               0 (None)
#             742 COPY                     1
#             744 STORE_FAST              10 (@py_assert0)
#             746 STORE_FAST              11 (@py_assert2)
# 
# 257         748 LOAD_CONST              11 ('metadata')
#             750 STORE_FAST              10 (@py_assert0)
#             752 LOAD_FAST               10 (@py_assert0)
#             754 LOAD_FAST                6 (result)
#             756 CONTAINS_OP              0
#             758 STORE_FAST              11 (@py_assert2)
#             760 LOAD_FAST               11 (@py_assert2)
#             762 POP_JUMP_IF_TRUE       153 (to 1070)
#             764 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             774 LOAD_ATTR               26 (_call_reprcompare)
#             794 LOAD_CONST               5 (('in',))
#             796 LOAD_FAST               11 (@py_assert2)
#             798 BUILD_TUPLE              1
#             800 LOAD_CONST               6 (('%(py1)s in %(py3)s',))
#             802 LOAD_FAST               10 (@py_assert0)
#             804 LOAD_FAST                6 (result)
#             806 BUILD_TUPLE              2
#             808 CALL                     4
#             816 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             826 LOAD_ATTR               20 (_saferepr)
#             846 LOAD_FAST               10 (@py_assert0)
#             848 CALL                     1
#             856 LOAD_CONST               7 ('result')
#             858 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             868 LOAD_ATTR               14 (locals)
#             888 CALL                     0
#             896 CONTAINS_OP              0
#             898 POP_JUMP_IF_TRUE        21 (to 942)
#             900 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             910 LOAD_ATTR               18 (_should_repr_global_name)
#             930 LOAD_FAST                6 (result)
#             932 CALL                     1
#             940 POP_JUMP_IF_FALSE       21 (to 984)
#         >>  942 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             952 LOAD_ATTR               20 (_saferepr)
#             972 LOAD_FAST                6 (result)
#             974 CALL                     1
#             982 JUMP_FORWARD             1 (to 986)
#         >>  984 LOAD_CONST               7 ('result')
#         >>  986 LOAD_CONST               8 (('py1', 'py3'))
#             988 BUILD_CONST_KEY_MAP      2
#             990 BINARY_OP                6 (%)
#             994 STORE_FAST              12 (@py_format4)
#             996 LOAD_CONST               9 ('assert %(py5)s')
#             998 LOAD_CONST              10 ('py5')
#            1000 LOAD_FAST               12 (@py_format4)
#            1002 BUILD_MAP                1
#            1004 BINARY_OP                6 (%)
#            1008 STORE_FAST              13 (@py_format6)
#            1010 LOAD_GLOBAL             23 (NULL + AssertionError)
#            1020 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#            1030 LOAD_ATTR               24 (_format_explanation)
#            1050 LOAD_FAST               13 (@py_format6)
#            1052 CALL                     1
#            1060 CALL                     1
#            1068 RAISE_VARARGS            1
#         >> 1070 LOAD_CONST               0 (None)
#            1072 COPY                     1
#            1074 STORE_FAST              10 (@py_assert0)
#            1076 STORE_FAST              11 (@py_assert2)
# 
# 259        1078 LOAD_FAST                6 (result)
#            1080 LOAD_CONST               4 ('components')
#            1082 BINARY_SUBSCR
#            1086 STORE_FAST              14 (components)
# 
# 260        1088 LOAD_GLOBAL             29 (NULL + len)
#            1098 LOAD_FAST               14 (components)
#            1100 CALL                     1
#            1108 STORE_FAST              11 (@py_assert2)
#            1110 LOAD_FAST                4 (model)
#            1112 LOAD_ATTR               30 (bus_count)
#            1132 STORE_FAST              15 (@py_assert6)
#            1134 LOAD_FAST                4 (model)
#            1136 LOAD_ATTR               32 (branch_count)
#            1156 STORE_FAST              16 (@py_assert9)
#            1158 LOAD_FAST               15 (@py_assert6)
#            1160 LOAD_FAST               16 (@py_assert9)
#            1162 BINARY_OP                0 (+)
#            1166 STORE_FAST              17 (@py_assert11)
# 
# 261        1168 LOAD_FAST                4 (model)
#            1170 LOAD_ATTR               34 (generators)
# 
# 260        1190 STORE_FAST              18 (@py_assert14)
#            1192 LOAD_GLOBAL             29 (NULL + len)
# 
# 261        1202 LOAD_FAST               18 (@py_assert14)
# 
# 260        1204 CALL                     1
#            1212 STORE_FAST              19 (@py_assert16)
#            1214 LOAD_FAST               17 (@py_assert11)
#            1216 LOAD_FAST               19 (@py_assert16)
#            1218 BINARY_OP                0 (+)
#            1222 STORE_FAST              20 (@py_assert18)
# 
# 262        1224 LOAD_FAST                4 (model)
#            1226 LOAD_ATTR               36 (loads)
# 
# 260        1246 STORE_FAST              21 (@py_assert21)
# 
# 262        1248 LOAD_GLOBAL             29 (NULL + len)
#            1258 LOAD_FAST               21 (@py_assert21)
#            1260 CALL                     1
# 
# 260        1268 STORE_FAST              22 (@py_assert23)
#            1270 LOAD_FAST               20 (@py_assert18)
# 
# 262        1272 LOAD_FAST               22 (@py_assert23)
# 
# 260        1274 BINARY_OP                0 (+)
#            1278 STORE_FAST              23 (@py_assert25)
#            1280 LOAD_FAST               11 (@py_assert2)
#            1282 LOAD_FAST               23 (@py_assert25)
#            1284 COMPARE_OP              92 (>=)
#            1288 STORE_FAST              24 (@py_assert4)
#            1290 LOAD_FAST               24 (@py_assert4)
#            1292 EXTENDED_ARG             2
#            1294 POP_JUMP_IF_TRUE       752 (to 2800)
#            1296 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        1306 LOAD_ATTR               26 (_call_reprcompare)
# 
# 260        1326 LOAD_CONST              12 (('>=',))
#            1328 LOAD_FAST               24 (@py_assert4)
#            1330 BUILD_TUPLE              1
#            1332 LOAD_CONST              13 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} >= (((%(py7)s\n{%(py7)s = %(py5)s.bus_count\n} + %(py10)s\n{%(py10)s = %(py8)s.branch_count\n}) + %(py17)s\n{%(py17)s = %(py12)s(%(py15)s\n{%(py15)s = %(py13)s.generators\n})\n}) + %(py24)s\n{%(py24)s = %(py19)s(%(py22)s\n{%(py22)s = %(py20)s.loads\n})\n})',))
#            1334 LOAD_FAST               11 (@py_assert2)
#            1336 LOAD_FAST               23 (@py_assert25)
#            1338 BUILD_TUPLE              2
#            1340 CALL                     4
#            1348 LOAD_CONST              14 ('len')
#            1350 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
# 262        1360 LOAD_ATTR               14 (locals)
# 
# 260        1380 CALL                     0
#            1388 CONTAINS_OP              0
#            1390 POP_JUMP_IF_TRUE        25 (to 1442)
#            1392 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        1402 LOAD_ATTR               18 (_should_repr_global_name)
# 
# 260        1422 LOAD_GLOBAL             28 (len)
#            1432 CALL                     1
#            1440 POP_JUMP_IF_FALSE       25 (to 1492)
#         >> 1442 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        1452 LOAD_ATTR               20 (_saferepr)
# 
# 260        1472 LOAD_GLOBAL             28 (len)
#            1482 CALL                     1
#            1490 JUMP_FORWARD             1 (to 1494)
#         >> 1492 LOAD_CONST              14 ('len')
#         >> 1494 LOAD_CONST               4 ('components')
#            1496 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
# 262        1506 LOAD_ATTR               14 (locals)
# 
# 260        1526 CALL                     0
#            1534 CONTAINS_OP              0
#            1536 POP_JUMP_IF_TRUE        21 (to 1580)
#            1538 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        1548 LOAD_ATTR               18 (_should_repr_global_name)
# 
# 260        1568 LOAD_FAST               14 (components)
#            1570 CALL                     1
#            1578 POP_JUMP_IF_FALSE       21 (to 1622)
#         >> 1580 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        1590 LOAD_ATTR               20 (_saferepr)
# 
# 260        1610 LOAD_FAST               14 (components)
#            1612 CALL                     1
#            1620 JUMP_FORWARD             1 (to 1624)
#         >> 1622 LOAD_CONST               4 ('components')
#         >> 1624 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        1634 LOAD_ATTR               20 (_saferepr)
# 
# 260        1654 LOAD_FAST               11 (@py_assert2)
#            1656 CALL                     1
#            1664 LOAD_CONST              15 ('model')
#            1666 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
# 262        1676 LOAD_ATTR               14 (locals)
# 
# 260        1696 CALL                     0
#            1704 CONTAINS_OP              0
#            1706 POP_JUMP_IF_TRUE        21 (to 1750)
#            1708 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        1718 LOAD_ATTR               18 (_should_repr_global_name)
# 
# 260        1738 LOAD_FAST                4 (model)
#            1740 CALL                     1
#            1748 POP_JUMP_IF_FALSE       21 (to 1792)
#         >> 1750 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        1760 LOAD_ATTR               20 (_saferepr)
# 
# 260        1780 LOAD_FAST                4 (model)
#            1782 CALL                     1
#            1790 JUMP_FORWARD             1 (to 1794)
#         >> 1792 LOAD_CONST              15 ('model')
#         >> 1794 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        1804 LOAD_ATTR               20 (_saferepr)
# 
# 260        1824 LOAD_FAST               15 (@py_assert6)
#            1826 CALL                     1
#            1834 LOAD_CONST              15 ('model')
#            1836 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
# 262        1846 LOAD_ATTR               14 (locals)
# 
# 260        1866 CALL                     0
#            1874 CONTAINS_OP              0
#            1876 POP_JUMP_IF_TRUE        21 (to 1920)
#            1878 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        1888 LOAD_ATTR               18 (_should_repr_global_name)
# 
# 260        1908 LOAD_FAST                4 (model)
#            1910 CALL                     1
#            1918 POP_JUMP_IF_FALSE       21 (to 1962)
#         >> 1920 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        1930 LOAD_ATTR               20 (_saferepr)
# 
# 260        1950 LOAD_FAST                4 (model)
#            1952 CALL                     1
#            1960 JUMP_FORWARD             1 (to 1964)
#         >> 1962 LOAD_CONST              15 ('model')
#         >> 1964 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        1974 LOAD_ATTR               20 (_saferepr)
# 
# 260        1994 LOAD_FAST               16 (@py_assert9)
#            1996 CALL                     1
#            2004 LOAD_CONST              14 ('len')
#            2006 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
# 262        2016 LOAD_ATTR               14 (locals)
# 
# 260        2036 CALL                     0
#            2044 CONTAINS_OP              0
#            2046 POP_JUMP_IF_TRUE        25 (to 2098)
#            2048 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        2058 LOAD_ATTR               18 (_should_repr_global_name)
# 
# 260        2078 LOAD_GLOBAL             28 (len)
#            2088 CALL                     1
#            2096 POP_JUMP_IF_FALSE       25 (to 2148)
#         >> 2098 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        2108 LOAD_ATTR               20 (_saferepr)
# 
# 260        2128 LOAD_GLOBAL             28 (len)
#            2138 CALL                     1
#            2146 JUMP_FORWARD             1 (to 2150)
#         >> 2148 LOAD_CONST              14 ('len')
#         >> 2150 LOAD_CONST              15 ('model')
#            2152 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
# 262        2162 LOAD_ATTR               14 (locals)
# 
# 260        2182 CALL                     0
#            2190 CONTAINS_OP              0
#            2192 POP_JUMP_IF_TRUE        21 (to 2236)
#            2194 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        2204 LOAD_ATTR               18 (_should_repr_global_name)
# 
# 261        2224 LOAD_FAST                4 (model)
# 
# 260        2226 CALL                     1
#            2234 POP_JUMP_IF_FALSE       21 (to 2278)
#         >> 2236 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        2246 LOAD_ATTR               20 (_saferepr)
# 
# 261        2266 LOAD_FAST                4 (model)
# 
# 260        2268 CALL                     1
#            2276 JUMP_FORWARD             1 (to 2280)
#         >> 2278 LOAD_CONST              15 ('model')
#         >> 2280 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        2290 LOAD_ATTR               20 (_saferepr)
# 
# 261        2310 LOAD_FAST               18 (@py_assert14)
# 
# 260        2312 CALL                     1
#            2320 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        2330 LOAD_ATTR               20 (_saferepr)
# 
# 260        2350 LOAD_FAST               19 (@py_assert16)
#            2352 CALL                     1
#            2360 LOAD_CONST              14 ('len')
#            2362 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
# 262        2372 LOAD_ATTR               14 (locals)
# 
# 260        2392 CALL                     0
#            2400 CONTAINS_OP              0
#            2402 POP_JUMP_IF_TRUE        25 (to 2454)
#            2404 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        2414 LOAD_ATTR               18 (_should_repr_global_name)
#            2434 LOAD_GLOBAL             28 (len)
# 
# 260        2444 CALL                     1
#            2452 POP_JUMP_IF_FALSE       25 (to 2504)
#         >> 2454 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        2464 LOAD_ATTR               20 (_saferepr)
#            2484 LOAD_GLOBAL             28 (len)
# 
# 260        2494 CALL                     1
#            2502 JUMP_FORWARD             1 (to 2506)
#         >> 2504 LOAD_CONST              14 ('len')
#         >> 2506 LOAD_CONST              15 ('model')
#            2508 LOAD_GLOBAL             13 (NULL + @py_builtins)
# 
# 262        2518 LOAD_ATTR               14 (locals)
# 
# 260        2538 CALL                     0
#            2546 CONTAINS_OP              0
#            2548 POP_JUMP_IF_TRUE        21 (to 2592)
#            2550 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        2560 LOAD_ATTR               18 (_should_repr_global_name)
#            2580 LOAD_FAST                4 (model)
# 
# 260        2582 CALL                     1
#            2590 POP_JUMP_IF_FALSE       21 (to 2634)
#         >> 2592 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        2602 LOAD_ATTR               20 (_saferepr)
#            2622 LOAD_FAST                4 (model)
# 
# 260        2624 CALL                     1
#            2632 JUMP_FORWARD             1 (to 2636)
#         >> 2634 LOAD_CONST              15 ('model')
#         >> 2636 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        2646 LOAD_ATTR               20 (_saferepr)
#            2666 LOAD_FAST               21 (@py_assert21)
# 
# 260        2668 CALL                     1
#            2676 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        2686 LOAD_ATTR               20 (_saferepr)
#            2706 LOAD_FAST               22 (@py_assert23)
# 
# 260        2708 CALL                     1
#            2716 LOAD_CONST              16 (('py0', 'py1', 'py3', 'py5', 'py7', 'py8', 'py10', 'py12', 'py13', 'py15', 'py17', 'py19', 'py20', 'py22', 'py24'))
#            2718 BUILD_CONST_KEY_MAP     15
#            2720 BINARY_OP                6 (%)
#            2724 STORE_FAST              25 (@py_format26)
#            2726 LOAD_CONST              17 ('assert %(py27)s')
#            2728 LOAD_CONST              18 ('py27')
#            2730 LOAD_FAST               25 (@py_format26)
#            2732 BUILD_MAP                1
#            2734 BINARY_OP                6 (%)
#            2738 STORE_FAST              26 (@py_format28)
#            2740 LOAD_GLOBAL             23 (NULL + AssertionError)
#            2750 LOAD_GLOBAL             17 (NULL + @pytest_ar)
# 
# 262        2760 LOAD_ATTR               24 (_format_explanation)
# 
# 260        2780 LOAD_FAST               26 (@py_format28)
#            2782 CALL                     1
#            2790 CALL                     1
#            2798 RAISE_VARARGS            1
#         >> 2800 LOAD_CONST               0 (None)
#            2802 COPY                     1
#            2804 STORE_FAST              11 (@py_assert2)
#            2806 COPY                     1
#            2808 STORE_FAST              24 (@py_assert4)
#            2810 COPY                     1
#            2812 STORE_FAST              15 (@py_assert6)
#            2814 COPY                     1
#            2816 STORE_FAST              16 (@py_assert9)
#            2818 COPY                     1
#            2820 STORE_FAST              17 (@py_assert11)
#            2822 COPY                     1
#            2824 STORE_FAST              18 (@py_assert14)
#            2826 COPY                     1
#            2828 STORE_FAST              19 (@py_assert16)
#            2830 COPY                     1
#            2832 STORE_FAST              20 (@py_assert18)
#            2834 COPY                     1
#            2836 STORE_FAST              21 (@py_assert21)
#            2838 COPY                     1
#            2840 STORE_FAST              22 (@py_assert23)
#            2842 STORE_FAST              23 (@py_assert25)
#            2844 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_convert_from_model_bus_generation at 0x3aecdc30, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 264>:
# 264           0 RESUME                   0
# 
# 265           2 LOAD_GLOBAL              1 (NULL + CloudPSSModelConverter)
#              12 CALL                     0
#              20 STORE_FAST               1 (converter)
# 
# 266          22 LOAD_CONST               1 (0)
#              24 LOAD_CONST               2 (('BusData', 'BranchData', 'LoadData'))
#              26 IMPORT_NAME              1 (cloudpss_skills_v2.libs.data_lib)
#              28 IMPORT_FROM              2 (BusData)
#              30 STORE_FAST               2 (BusData)
#              32 IMPORT_FROM              3 (BranchData)
#              34 STORE_FAST               3 (BranchData)
#              36 IMPORT_FROM              4 (LoadData)
#              38 STORE_FAST               4 (LoadData)
#              40 POP_TOP
# 
# 268          42 LOAD_GLOBAL             11 (NULL + PowerSystemModel)
# 
# 269          52 LOAD_CONST               3 ('Simple3Bus')
# 
# 270          54 LOAD_CONST               4 (100.0)
# 
# 271          56 LOAD_CONST               5 (60.0)
# 
# 273          58 PUSH_NULL
#              60 LOAD_FAST                2 (BusData)
#              62 LOAD_CONST               6 ('B1')
#              64 LOAD_CONST               7 (345.0)
#              66 LOAD_GLOBAL             12 (BusType)
#              76 LOAD_ATTR               14 (SLACK)
#              96 KW_NAMES                 8 (('name', 'voltage_kv', 'bus_type'))
#              98 CALL                     3
# 
# 274         106 PUSH_NULL
#             108 LOAD_FAST                2 (BusData)
#             110 LOAD_CONST               9 ('B2')
#             112 LOAD_CONST               7 (345.0)
#             114 KW_NAMES                10 (('name', 'voltage_kv'))
#             116 CALL                     2
# 
# 272         124 BUILD_LIST               2
# 
# 277         126 PUSH_NULL
#             128 LOAD_FAST                3 (BranchData)
# 
# 278         130 LOAD_CONST              11 ('L1')
# 
# 279         132 LOAD_CONST               6 ('B1')
# 
# 280         134 LOAD_CONST               9 ('B2')
# 
# 281         136 LOAD_CONST              12 (0.01)
# 
# 282         138 LOAD_CONST              13 (0.05)
# 
# 277         140 KW_NAMES                14 (('name', 'from_bus', 'to_bus', 'resistance_pu', 'reactance_pu'))
#             142 CALL                     5
# 
# 276         150 BUILD_LIST               1
# 
# 286         152 PUSH_NULL
#             154 LOAD_FAST                4 (LoadData)
#             156 LOAD_CONST              15 ('LD1')
#             158 LOAD_CONST               9 ('B2')
#             160 LOAD_CONST              16 (50.0)
#             162 LOAD_CONST              17 (25.0)
#             164 KW_NAMES                18 (('name', 'bus', 'p_mw', 'q_mvar'))
#             166 CALL                     4
# 
# 285         174 BUILD_LIST               1
# 
# 288         176 LOAD_CONST              19 ('test')
# 
# 268         178 KW_NAMES                20 (('name', 'base_mva', 'frequency_hz', 'buses', 'branches', 'loads', 'source_engine'))
#             180 CALL                     7
#             188 STORE_FAST               5 (simple_model)
# 
# 291         190 LOAD_FAST                1 (converter)
#             192 LOAD_ATTR               17 (NULL|self + convert_from_model)
#             212 LOAD_FAST                5 (simple_model)
#             214 CALL                     1
#             222 UNPACK_SEQUENCE          2
#             226 STORE_FAST               6 (result)
#             228 STORE_FAST               7 (report)
# 
# 293         230 LOAD_FAST                7 (report)
#             232 LOAD_ATTR               18 (is_success)
#             252 STORE_FAST               8 (@py_assert1)
#             254 LOAD_FAST                8 (@py_assert1)
#             256 POP_JUMP_IF_TRUE       121 (to 500)
#             258 LOAD_CONST              21 ('assert %(py2)s\n{%(py2)s = %(py0)s.is_success\n}')
#             260 LOAD_CONST              22 ('report')
#             262 LOAD_GLOBAL             21 (NULL + @py_builtins)
#             272 LOAD_ATTR               22 (locals)
#             292 CALL                     0
#             300 CONTAINS_OP              0
#             302 POP_JUMP_IF_TRUE        21 (to 346)
#             304 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             314 LOAD_ATTR               26 (_should_repr_global_name)
#             334 LOAD_FAST                7 (report)
#             336 CALL                     1
#             344 POP_JUMP_IF_FALSE       21 (to 388)
#         >>  346 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             356 LOAD_ATTR               28 (_saferepr)
#             376 LOAD_FAST                7 (report)
#             378 CALL                     1
#             386 JUMP_FORWARD             1 (to 390)
#         >>  388 LOAD_CONST              22 ('report')
#         >>  390 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             400 LOAD_ATTR               28 (_saferepr)
#             420 LOAD_FAST                8 (@py_assert1)
#             422 CALL                     1
#             430 LOAD_CONST              23 (('py0', 'py2'))
#             432 BUILD_CONST_KEY_MAP      2
#             434 BINARY_OP                6 (%)
#             438 STORE_FAST               9 (@py_format3)
#             440 LOAD_GLOBAL             31 (NULL + AssertionError)
#             450 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             460 LOAD_ATTR               32 (_format_explanation)
#             480 LOAD_FAST                9 (@py_format3)
#             482 CALL                     1
#             490 CALL                     1
#             498 RAISE_VARARGS            1
#         >>  500 LOAD_CONST               0 (None)
#             502 STORE_FAST               8 (@py_assert1)
# 
# 294         504 LOAD_FAST                6 (result)
#             506 LOAD_CONST              24 ('components')
#             508 BINARY_SUBSCR
#             512 STORE_FAST              10 (components)
# 
# 296         514 LOAD_FAST               10 (components)
#             516 LOAD_ATTR               35 (NULL|self + items)
#             536 CALL                     0
#             544 GET_ITER
# 
# 295         546 LOAD_FAST_AND_CLEAR     11 (k)
#             548 LOAD_FAST_AND_CLEAR     12 (v)
#             550 SWAP                     3
#             552 BUILD_LIST               0
#             554 SWAP                     2
# 
# 296     >>  556 FOR_ITER                16 (to 592)
#             560 UNPACK_SEQUENCE          2
#             564 STORE_FAST              11 (k)
#             566 STORE_FAST              12 (v)
#             568 LOAD_FAST               12 (v)
#             570 LOAD_CONST              25 ('rid')
#             572 BINARY_SUBSCR
#             576 LOAD_CONST              26 ('model/CloudPSS/_newBus_3p')
#             578 COMPARE_OP              40 (==)
#             582 POP_JUMP_IF_TRUE         1 (to 586)
#             584 JUMP_BACKWARD           15 (to 556)
#         >>  586 LOAD_FAST               11 (k)
#             588 LIST_APPEND              2
#             590 JUMP_BACKWARD           18 (to 556)
#         >>  592 END_FOR
# 
# 295         594 STORE_FAST              13 (bus_keys)
#             596 STORE_FAST              11 (k)
#             598 STORE_FAST              12 (v)
# 
# 300         600 LOAD_FAST               10 (components)
#             602 LOAD_ATTR               35 (NULL|self + items)
#             622 CALL                     0
#             630 GET_ITER
# 
# 298         632 LOAD_FAST_AND_CLEAR     11 (k)
#             634 LOAD_FAST_AND_CLEAR     12 (v)
#             636 SWAP                     3
#             638 BUILD_LIST               0
#             640 SWAP                     2
# 
# 300     >>  642 FOR_ITER                15 (to 676)
#             646 UNPACK_SEQUENCE          2
#             650 STORE_FAST              11 (k)
#             652 STORE_FAST              12 (v)
# 
# 301         654 LOAD_FAST               12 (v)
#             656 LOAD_CONST              25 ('rid')
#             658 BINARY_SUBSCR
#             662 LOAD_CONST              27 ('model/CloudPSS/TransmissionLine')
#             664 COMPARE_OP              40 (==)
#             668 POP_JUMP_IF_FALSE        2 (to 674)
# 
# 299         670 LOAD_FAST               11 (k)
#             672 LIST_APPEND              2
#         >>  674 JUMP_BACKWARD           17 (to 642)
# 
# 300     >>  676 END_FOR
# 
# 298         678 STORE_FAST              14 (line_keys)
#             680 STORE_FAST              11 (k)
#             682 STORE_FAST              12 (v)
# 
# 305         684 LOAD_FAST               10 (components)
#             686 LOAD_ATTR               35 (NULL|self + items)
#             706 CALL                     0
#             714 GET_ITER
# 
# 303         716 LOAD_FAST_AND_CLEAR     11 (k)
#             718 LOAD_FAST_AND_CLEAR     12 (v)
#             720 SWAP                     3
#             722 BUILD_LIST               0
#             724 SWAP                     2
# 
# 305     >>  726 FOR_ITER                15 (to 760)
#             730 UNPACK_SEQUENCE          2
#             734 STORE_FAST              11 (k)
#             736 STORE_FAST              12 (v)
# 
# 306         738 LOAD_FAST               12 (v)
#             740 LOAD_CONST              25 ('rid')
#             742 BINARY_SUBSCR
#             746 LOAD_CONST              28 ('model/CloudPSS/_newExpLoad_3p')
#             748 COMPARE_OP              40 (==)
#             752 POP_JUMP_IF_FALSE        2 (to 758)
# 
# 304         754 LOAD_FAST               11 (k)
#             756 LIST_APPEND              2
#         >>  758 JUMP_BACKWARD           17 (to 726)
# 
# 305     >>  760 END_FOR
# 
# 303         762 STORE_FAST              15 (load_keys)
#             764 STORE_FAST              11 (k)
#             766 STORE_FAST              12 (v)
# 
# 309         768 LOAD_GLOBAL             37 (NULL + len)
#             778 LOAD_FAST               13 (bus_keys)
#             780 CALL                     1
#             788 STORE_FAST              16 (@py_assert2)
#             790 LOAD_CONST              29 (2)
#             792 STORE_FAST              17 (@py_assert5)
#             794 LOAD_FAST               16 (@py_assert2)
#             796 LOAD_FAST               17 (@py_assert5)
#             798 COMPARE_OP              40 (==)
#             802 STORE_FAST              18 (@py_assert4)
#             804 LOAD_FAST               18 (@py_assert4)
#             806 POP_JUMP_IF_TRUE       246 (to 1300)
#             808 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             818 LOAD_ATTR               38 (_call_reprcompare)
#             838 LOAD_CONST              30 (('==',))
#             840 LOAD_FAST               18 (@py_assert4)
#             842 BUILD_TUPLE              1
#             844 LOAD_CONST              31 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             846 LOAD_FAST               16 (@py_assert2)
#             848 LOAD_FAST               17 (@py_assert5)
#             850 BUILD_TUPLE              2
#             852 CALL                     4
#             860 LOAD_CONST              32 ('len')
#             862 LOAD_GLOBAL             21 (NULL + @py_builtins)
#             872 LOAD_ATTR               22 (locals)
#             892 CALL                     0
#             900 CONTAINS_OP              0
#             902 POP_JUMP_IF_TRUE        25 (to 954)
#             904 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             914 LOAD_ATTR               26 (_should_repr_global_name)
#             934 LOAD_GLOBAL             36 (len)
#             944 CALL                     1
#             952 POP_JUMP_IF_FALSE       25 (to 1004)
#         >>  954 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#             964 LOAD_ATTR               28 (_saferepr)
#             984 LOAD_GLOBAL             36 (len)
#             994 CALL                     1
#            1002 JUMP_FORWARD             1 (to 1006)
#         >> 1004 LOAD_CONST              32 ('len')
#         >> 1006 LOAD_CONST              33 ('bus_keys')
#            1008 LOAD_GLOBAL             21 (NULL + @py_builtins)
#            1018 LOAD_ATTR               22 (locals)
#            1038 CALL                     0
#            1046 CONTAINS_OP              0
#            1048 POP_JUMP_IF_TRUE        21 (to 1092)
#            1050 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1060 LOAD_ATTR               26 (_should_repr_global_name)
#            1080 LOAD_FAST               13 (bus_keys)
#            1082 CALL                     1
#            1090 POP_JUMP_IF_FALSE       21 (to 1134)
#         >> 1092 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1102 LOAD_ATTR               28 (_saferepr)
#            1122 LOAD_FAST               13 (bus_keys)
#            1124 CALL                     1
#            1132 JUMP_FORWARD             1 (to 1136)
#         >> 1134 LOAD_CONST              33 ('bus_keys')
#         >> 1136 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1146 LOAD_ATTR               28 (_saferepr)
#            1166 LOAD_FAST               16 (@py_assert2)
#            1168 CALL                     1
#            1176 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1186 LOAD_ATTR               28 (_saferepr)
#            1206 LOAD_FAST               17 (@py_assert5)
#            1208 CALL                     1
#            1216 LOAD_CONST              34 (('py0', 'py1', 'py3', 'py6'))
#            1218 BUILD_CONST_KEY_MAP      4
#            1220 BINARY_OP                6 (%)
#            1224 STORE_FAST              19 (@py_format7)
#            1226 LOAD_CONST              35 ('assert %(py8)s')
#            1228 LOAD_CONST              36 ('py8')
#            1230 LOAD_FAST               19 (@py_format7)
#            1232 BUILD_MAP                1
#            1234 BINARY_OP                6 (%)
#            1238 STORE_FAST              20 (@py_format9)
#            1240 LOAD_GLOBAL             31 (NULL + AssertionError)
#            1250 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1260 LOAD_ATTR               32 (_format_explanation)
#            1280 LOAD_FAST               20 (@py_format9)
#            1282 CALL                     1
#            1290 CALL                     1
#            1298 RAISE_VARARGS            1
#         >> 1300 LOAD_CONST               0 (None)
#            1302 COPY                     1
#            1304 STORE_FAST              16 (@py_assert2)
#            1306 COPY                     1
#            1308 STORE_FAST              18 (@py_assert4)
#            1310 STORE_FAST              17 (@py_assert5)
# 
# 310        1312 LOAD_GLOBAL             37 (NULL + len)
#            1322 LOAD_FAST               14 (line_keys)
#            1324 CALL                     1
#            1332 STORE_FAST              16 (@py_assert2)
#            1334 LOAD_CONST              37 (1)
#            1336 STORE_FAST              17 (@py_assert5)
#            1338 LOAD_FAST               16 (@py_assert2)
#            1340 LOAD_FAST               17 (@py_assert5)
#            1342 COMPARE_OP              40 (==)
#            1346 STORE_FAST              18 (@py_assert4)
#            1348 LOAD_FAST               18 (@py_assert4)
#            1350 POP_JUMP_IF_TRUE       246 (to 1844)
#            1352 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1362 LOAD_ATTR               38 (_call_reprcompare)
#            1382 LOAD_CONST              30 (('==',))
#            1384 LOAD_FAST               18 (@py_assert4)
#            1386 BUILD_TUPLE              1
#            1388 LOAD_CONST              31 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#            1390 LOAD_FAST               16 (@py_assert2)
#            1392 LOAD_FAST               17 (@py_assert5)
#            1394 BUILD_TUPLE              2
#            1396 CALL                     4
#            1404 LOAD_CONST              32 ('len')
#            1406 LOAD_GLOBAL             21 (NULL + @py_builtins)
#            1416 LOAD_ATTR               22 (locals)
#            1436 CALL                     0
#            1444 CONTAINS_OP              0
#            1446 POP_JUMP_IF_TRUE        25 (to 1498)
#            1448 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1458 LOAD_ATTR               26 (_should_repr_global_name)
#            1478 LOAD_GLOBAL             36 (len)
#            1488 CALL                     1
#            1496 POP_JUMP_IF_FALSE       25 (to 1548)
#         >> 1498 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1508 LOAD_ATTR               28 (_saferepr)
#            1528 LOAD_GLOBAL             36 (len)
#            1538 CALL                     1
#            1546 JUMP_FORWARD             1 (to 1550)
#         >> 1548 LOAD_CONST              32 ('len')
#         >> 1550 LOAD_CONST              38 ('line_keys')
#            1552 LOAD_GLOBAL             21 (NULL + @py_builtins)
#            1562 LOAD_ATTR               22 (locals)
#            1582 CALL                     0
#            1590 CONTAINS_OP              0
#            1592 POP_JUMP_IF_TRUE        21 (to 1636)
#            1594 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1604 LOAD_ATTR               26 (_should_repr_global_name)
#            1624 LOAD_FAST               14 (line_keys)
#            1626 CALL                     1
#            1634 POP_JUMP_IF_FALSE       21 (to 1678)
#         >> 1636 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1646 LOAD_ATTR               28 (_saferepr)
#            1666 LOAD_FAST               14 (line_keys)
#            1668 CALL                     1
#            1676 JUMP_FORWARD             1 (to 1680)
#         >> 1678 LOAD_CONST              38 ('line_keys')
#         >> 1680 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1690 LOAD_ATTR               28 (_saferepr)
#            1710 LOAD_FAST               16 (@py_assert2)
#            1712 CALL                     1
#            1720 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1730 LOAD_ATTR               28 (_saferepr)
#            1750 LOAD_FAST               17 (@py_assert5)
#            1752 CALL                     1
#            1760 LOAD_CONST              34 (('py0', 'py1', 'py3', 'py6'))
#            1762 BUILD_CONST_KEY_MAP      4
#            1764 BINARY_OP                6 (%)
#            1768 STORE_FAST              19 (@py_format7)
#            1770 LOAD_CONST              35 ('assert %(py8)s')
#            1772 LOAD_CONST              36 ('py8')
#            1774 LOAD_FAST               19 (@py_format7)
#            1776 BUILD_MAP                1
#            1778 BINARY_OP                6 (%)
#            1782 STORE_FAST              20 (@py_format9)
#            1784 LOAD_GLOBAL             31 (NULL + AssertionError)
#            1794 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1804 LOAD_ATTR               32 (_format_explanation)
#            1824 LOAD_FAST               20 (@py_format9)
#            1826 CALL                     1
#            1834 CALL                     1
#            1842 RAISE_VARARGS            1
#         >> 1844 LOAD_CONST               0 (None)
#            1846 COPY                     1
#            1848 STORE_FAST              16 (@py_assert2)
#            1850 COPY                     1
#            1852 STORE_FAST              18 (@py_assert4)
#            1854 STORE_FAST              17 (@py_assert5)
# 
# 311        1856 LOAD_GLOBAL             37 (NULL + len)
#            1866 LOAD_FAST               15 (load_keys)
#            1868 CALL                     1
#            1876 STORE_FAST              16 (@py_assert2)
#            1878 LOAD_CONST              37 (1)
#            1880 STORE_FAST              17 (@py_assert5)
#            1882 LOAD_FAST               16 (@py_assert2)
#            1884 LOAD_FAST               17 (@py_assert5)
#            1886 COMPARE_OP              40 (==)
#            1890 STORE_FAST              18 (@py_assert4)
#            1892 LOAD_FAST               18 (@py_assert4)
#            1894 POP_JUMP_IF_TRUE       246 (to 2388)
#            1896 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            1906 LOAD_ATTR               38 (_call_reprcompare)
#            1926 LOAD_CONST              30 (('==',))
#            1928 LOAD_FAST               18 (@py_assert4)
#            1930 BUILD_TUPLE              1
#            1932 LOAD_CONST              31 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#            1934 LOAD_FAST               16 (@py_assert2)
#            1936 LOAD_FAST               17 (@py_assert5)
#            1938 BUILD_TUPLE              2
#            1940 CALL                     4
#            1948 LOAD_CONST              32 ('len')
#            1950 LOAD_GLOBAL             21 (NULL + @py_builtins)
#            1960 LOAD_ATTR               22 (locals)
#            1980 CALL                     0
#            1988 CONTAINS_OP              0
#            1990 POP_JUMP_IF_TRUE        25 (to 2042)
#            1992 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            2002 LOAD_ATTR               26 (_should_repr_global_name)
#            2022 LOAD_GLOBAL             36 (len)
#            2032 CALL                     1
#            2040 POP_JUMP_IF_FALSE       25 (to 2092)
#         >> 2042 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            2052 LOAD_ATTR               28 (_saferepr)
#            2072 LOAD_GLOBAL             36 (len)
#            2082 CALL                     1
#            2090 JUMP_FORWARD             1 (to 2094)
#         >> 2092 LOAD_CONST              32 ('len')
#         >> 2094 LOAD_CONST              39 ('load_keys')
#            2096 LOAD_GLOBAL             21 (NULL + @py_builtins)
#            2106 LOAD_ATTR               22 (locals)
#            2126 CALL                     0
#            2134 CONTAINS_OP              0
#            2136 POP_JUMP_IF_TRUE        21 (to 2180)
#            2138 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            2148 LOAD_ATTR               26 (_should_repr_global_name)
#            2168 LOAD_FAST               15 (load_keys)
#            2170 CALL                     1
#            2178 POP_JUMP_IF_FALSE       21 (to 2222)
#         >> 2180 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            2190 LOAD_ATTR               28 (_saferepr)
#            2210 LOAD_FAST               15 (load_keys)
#            2212 CALL                     1
#            2220 JUMP_FORWARD             1 (to 2224)
#         >> 2222 LOAD_CONST              39 ('load_keys')
#         >> 2224 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            2234 LOAD_ATTR               28 (_saferepr)
#            2254 LOAD_FAST               16 (@py_assert2)
#            2256 CALL                     1
#            2264 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            2274 LOAD_ATTR               28 (_saferepr)
#            2294 LOAD_FAST               17 (@py_assert5)
#            2296 CALL                     1
#            2304 LOAD_CONST              34 (('py0', 'py1', 'py3', 'py6'))
#            2306 BUILD_CONST_KEY_MAP      4
#            2308 BINARY_OP                6 (%)
#            2312 STORE_FAST              19 (@py_format7)
#            2314 LOAD_CONST              35 ('assert %(py8)s')
#            2316 LOAD_CONST              36 ('py8')
#            2318 LOAD_FAST               19 (@py_format7)
#            2320 BUILD_MAP                1
#            2322 BINARY_OP                6 (%)
#            2326 STORE_FAST              20 (@py_format9)
#            2328 LOAD_GLOBAL             31 (NULL + AssertionError)
#            2338 LOAD_GLOBAL             25 (NULL + @pytest_ar)
#            2348 LOAD_ATTR               32 (_format_explanation)
#            2368 LOAD_FAST               20 (@py_format9)
#            2370 CALL                     1
#            2378 CALL                     1
#            2386 RAISE_VARARGS            1
#         >> 2388 LOAD_CONST               0 (None)
#            2390 COPY                     1
#            2392 STORE_FAST              16 (@py_assert2)
#            2394 COPY                     1
#            2396 STORE_FAST              18 (@py_assert4)
#            2398 STORE_FAST              17 (@py_assert5)
#            2400 RETURN_CONST             0 (None)
#         >> 2402 SWAP                     2
#            2404 POP_TOP
# 
# 295        2406 SWAP                     3
#            2408 STORE_FAST              12 (v)
#            2410 STORE_FAST              11 (k)
#            2412 RERAISE                  0
#         >> 2414 SWAP                     2
#            2416 POP_TOP
# 
# 298        2418 SWAP                     3
#            2420 STORE_FAST              12 (v)
#            2422 STORE_FAST              11 (k)
#            2424 RERAISE                  0
#         >> 2426 SWAP                     2
#            2428 POP_TOP
# 
# 303        2430 SWAP                     3
#            2432 STORE_FAST              12 (v)
#            2434 STORE_FAST              11 (k)
#            2436 RERAISE                  0
# ExceptionTable:
#   552 to 582 -> 2402 [3]
#   586 to 592 -> 2402 [3]
#   638 to 676 -> 2414 [3]
#   722 to 760 -> 2426 [3]
# 
# Disassembly of <code object test_conversion_report_quality at 0x3af9f220, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 313>:
# 313           0 RESUME                   0
# 
# 314           2 LOAD_GLOBAL              1 (NULL + CloudPSSModelConverter)
#              12 CALL                     0
#              20 STORE_FAST               1 (converter)
# 
# 316          22 LOAD_FAST                1 (converter)
#              24 LOAD_ATTR                3 (NULL|self + convert_to_model)
# 
# 317          44 LOAD_GLOBAL              5 (NULL + _MockTopology)
#              54 LOAD_GLOBAL              7 (NULL + _make_synthetic_topology)
#              64 CALL                     0
#              72 CALL                     1
# 
# 318          80 LOAD_GLOBAL              8 (ConversionMode)
#              90 LOAD_ATTR               10 (APPROXIMATE)
# 
# 316         110 KW_NAMES                 1 (('mode',))
#             112 CALL                     2
#             120 UNPACK_SEQUENCE          2
#             124 STORE_FAST               2 (model)
#             126 STORE_FAST               3 (report)
# 
# 321         128 LOAD_FAST                3 (report)
#             130 LOAD_ATTR               12 (quality)
#             150 STORE_FAST               4 (@py_assert1)
#             152 LOAD_GLOBAL             14 (ConversionQuality)
#             162 LOAD_ATTR               16 (HIGH)
#             182 STORE_FAST               5 (@py_assert5)
#             184 LOAD_FAST                4 (@py_assert1)
#             186 LOAD_FAST                5 (@py_assert5)
#             188 COMPARE_OP              40 (==)
#             192 STORE_FAST               6 (@py_assert3)
#             194 LOAD_FAST                6 (@py_assert3)
#             196 POP_JUMP_IF_TRUE       246 (to 690)
#             198 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             208 LOAD_ATTR               20 (_call_reprcompare)
#             228 LOAD_CONST               2 (('==',))
#             230 LOAD_FAST                6 (@py_assert3)
#             232 BUILD_TUPLE              1
#             234 LOAD_CONST               3 (('%(py2)s\n{%(py2)s = %(py0)s.quality\n} == %(py6)s\n{%(py6)s = %(py4)s.HIGH\n}',))
#             236 LOAD_FAST                4 (@py_assert1)
#             238 LOAD_FAST                5 (@py_assert5)
#             240 BUILD_TUPLE              2
#             242 CALL                     4
#             250 LOAD_CONST               4 ('report')
#             252 LOAD_GLOBAL             23 (NULL + @py_builtins)
#             262 LOAD_ATTR               24 (locals)
#             282 CALL                     0
#             290 CONTAINS_OP              0
#             292 POP_JUMP_IF_TRUE        21 (to 336)
#             294 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             304 LOAD_ATTR               26 (_should_repr_global_name)
#             324 LOAD_FAST                3 (report)
#             326 CALL                     1
#             334 POP_JUMP_IF_FALSE       21 (to 378)
#         >>  336 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             346 LOAD_ATTR               28 (_saferepr)
#             366 LOAD_FAST                3 (report)
#             368 CALL                     1
#             376 JUMP_FORWARD             1 (to 380)
#         >>  378 LOAD_CONST               4 ('report')
#         >>  380 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             390 LOAD_ATTR               28 (_saferepr)
#             410 LOAD_FAST                4 (@py_assert1)
#             412 CALL                     1
#             420 LOAD_CONST               5 ('ConversionQuality')
#             422 LOAD_GLOBAL             23 (NULL + @py_builtins)
#             432 LOAD_ATTR               24 (locals)
#             452 CALL                     0
#             460 CONTAINS_OP              0
#             462 POP_JUMP_IF_TRUE        25 (to 514)
#             464 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             474 LOAD_ATTR               26 (_should_repr_global_name)
#             494 LOAD_GLOBAL             14 (ConversionQuality)
#             504 CALL                     1
#             512 POP_JUMP_IF_FALSE       25 (to 564)
#         >>  514 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             524 LOAD_ATTR               28 (_saferepr)
#             544 LOAD_GLOBAL             14 (ConversionQuality)
#             554 CALL                     1
#             562 JUMP_FORWARD             1 (to 566)
#         >>  564 LOAD_CONST               5 ('ConversionQuality')
#         >>  566 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             576 LOAD_ATTR               28 (_saferepr)
#             596 LOAD_FAST                5 (@py_assert5)
#             598 CALL                     1
#             606 LOAD_CONST               6 (('py0', 'py2', 'py4', 'py6'))
#             608 BUILD_CONST_KEY_MAP      4
#             610 BINARY_OP                6 (%)
#             614 STORE_FAST               7 (@py_format7)
#             616 LOAD_CONST               7 ('assert %(py8)s')
#             618 LOAD_CONST               8 ('py8')
#             620 LOAD_FAST                7 (@py_format7)
#             622 BUILD_MAP                1
#             624 BINARY_OP                6 (%)
#             628 STORE_FAST               8 (@py_format9)
#             630 LOAD_GLOBAL             31 (NULL + AssertionError)
#             640 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             650 LOAD_ATTR               32 (_format_explanation)
#             670 LOAD_FAST                8 (@py_format9)
#             672 CALL                     1
#             680 CALL                     1
#             688 RAISE_VARARGS            1
#         >>  690 LOAD_CONST               0 (None)
#             692 COPY                     1
#             694 STORE_FAST               4 (@py_assert1)
#             696 COPY                     1
#             698 STORE_FAST               6 (@py_assert3)
#             700 STORE_FAST               5 (@py_assert5)
# 
# 322         702 LOAD_FAST                3 (report)
#             704 LOAD_ATTR               34 (source_engine)
#             724 STORE_FAST               4 (@py_assert1)
#             726 LOAD_CONST               9 ('cloudpss')
#             728 STORE_FAST               9 (@py_assert4)
#             730 LOAD_FAST                4 (@py_assert1)
#             732 LOAD_FAST                9 (@py_assert4)
#             734 COMPARE_OP              40 (==)
#             738 STORE_FAST               6 (@py_assert3)
#             740 LOAD_FAST                6 (@py_assert3)
#             742 POP_JUMP_IF_TRUE       173 (to 1090)
#             744 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             754 LOAD_ATTR               20 (_call_reprcompare)
#             774 LOAD_CONST               2 (('==',))
#             776 LOAD_FAST                6 (@py_assert3)
#             778 BUILD_TUPLE              1
#             780 LOAD_CONST              10 (('%(py2)s\n{%(py2)s = %(py0)s.source_engine\n} == %(py5)s',))
#             782 LOAD_FAST                4 (@py_assert1)
#             784 LOAD_FAST                9 (@py_assert4)
#             786 BUILD_TUPLE              2
#             788 CALL                     4
#             796 LOAD_CONST               4 ('report')
#             798 LOAD_GLOBAL             23 (NULL + @py_builtins)
#             808 LOAD_ATTR               24 (locals)
#             828 CALL                     0
#             836 CONTAINS_OP              0
#             838 POP_JUMP_IF_TRUE        21 (to 882)
#             840 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             850 LOAD_ATTR               26 (_should_repr_global_name)
#             870 LOAD_FAST                3 (report)
#             872 CALL                     1
#             880 POP_JUMP_IF_FALSE       21 (to 924)
#         >>  882 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             892 LOAD_ATTR               28 (_saferepr)
#             912 LOAD_FAST                3 (report)
#             914 CALL                     1
#             922 JUMP_FORWARD             1 (to 926)
#         >>  924 LOAD_CONST               4 ('report')
#         >>  926 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             936 LOAD_ATTR               28 (_saferepr)
#             956 LOAD_FAST                4 (@py_assert1)
#             958 CALL                     1
#             966 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             976 LOAD_ATTR               28 (_saferepr)
#             996 LOAD_FAST                9 (@py_assert4)
#             998 CALL                     1
#            1006 LOAD_CONST              11 (('py0', 'py2', 'py5'))
#            1008 BUILD_CONST_KEY_MAP      3
#            1010 BINARY_OP                6 (%)
#            1014 STORE_FAST              10 (@py_format6)
#            1016 LOAD_CONST              12 ('assert %(py7)s')
#            1018 LOAD_CONST              13 ('py7')
#            1020 LOAD_FAST               10 (@py_format6)
#            1022 BUILD_MAP                1
#            1024 BINARY_OP                6 (%)
#            1028 STORE_FAST              11 (@py_format8)
#            1030 LOAD_GLOBAL             31 (NULL + AssertionError)
#            1040 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1050 LOAD_ATTR               32 (_format_explanation)
#            1070 LOAD_FAST               11 (@py_format8)
#            1072 CALL                     1
#            1080 CALL                     1
#            1088 RAISE_VARARGS            1
#         >> 1090 LOAD_CONST               0 (None)
#            1092 COPY                     1
#            1094 STORE_FAST               4 (@py_assert1)
#            1096 COPY                     1
#            1098 STORE_FAST               6 (@py_assert3)
#            1100 STORE_FAST               9 (@py_assert4)
# 
# 323        1102 LOAD_FAST                3 (report)
#            1104 LOAD_ATTR               36 (target_engine)
#            1124 STORE_FAST               4 (@py_assert1)
#            1126 LOAD_CONST              14 ('model')
#            1128 STORE_FAST               9 (@py_assert4)
#            1130 LOAD_FAST                4 (@py_assert1)
#            1132 LOAD_FAST                9 (@py_assert4)
#            1134 COMPARE_OP              40 (==)
#            1138 STORE_FAST               6 (@py_assert3)
#            1140 LOAD_FAST                6 (@py_assert3)
#            1142 POP_JUMP_IF_TRUE       173 (to 1490)
#            1144 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1154 LOAD_ATTR               20 (_call_reprcompare)
#            1174 LOAD_CONST               2 (('==',))
#            1176 LOAD_FAST                6 (@py_assert3)
#            1178 BUILD_TUPLE              1
#            1180 LOAD_CONST              15 (('%(py2)s\n{%(py2)s = %(py0)s.target_engine\n} == %(py5)s',))
#            1182 LOAD_FAST                4 (@py_assert1)
#            1184 LOAD_FAST                9 (@py_assert4)
#            1186 BUILD_TUPLE              2
#            1188 CALL                     4
#            1196 LOAD_CONST               4 ('report')
#            1198 LOAD_GLOBAL             23 (NULL + @py_builtins)
#            1208 LOAD_ATTR               24 (locals)
#            1228 CALL                     0
#            1236 CONTAINS_OP              0
#            1238 POP_JUMP_IF_TRUE        21 (to 1282)
#            1240 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1250 LOAD_ATTR               26 (_should_repr_global_name)
#            1270 LOAD_FAST                3 (report)
#            1272 CALL                     1
#            1280 POP_JUMP_IF_FALSE       21 (to 1324)
#         >> 1282 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1292 LOAD_ATTR               28 (_saferepr)
#            1312 LOAD_FAST                3 (report)
#            1314 CALL                     1
#            1322 JUMP_FORWARD             1 (to 1326)
#         >> 1324 LOAD_CONST               4 ('report')
#         >> 1326 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1336 LOAD_ATTR               28 (_saferepr)
#            1356 LOAD_FAST                4 (@py_assert1)
#            1358 CALL                     1
#            1366 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1376 LOAD_ATTR               28 (_saferepr)
#            1396 LOAD_FAST                9 (@py_assert4)
#            1398 CALL                     1
#            1406 LOAD_CONST              11 (('py0', 'py2', 'py5'))
#            1408 BUILD_CONST_KEY_MAP      3
#            1410 BINARY_OP                6 (%)
#            1414 STORE_FAST              10 (@py_format6)
#            1416 LOAD_CONST              12 ('assert %(py7)s')
#            1418 LOAD_CONST              13 ('py7')
#            1420 LOAD_FAST               10 (@py_format6)
#            1422 BUILD_MAP                1
#            1424 BINARY_OP                6 (%)
#            1428 STORE_FAST              11 (@py_format8)
#            1430 LOAD_GLOBAL             31 (NULL + AssertionError)
#            1440 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1450 LOAD_ATTR               32 (_format_explanation)
#            1470 LOAD_FAST               11 (@py_format8)
#            1472 CALL                     1
#            1480 CALL                     1
#            1488 RAISE_VARARGS            1
#         >> 1490 LOAD_CONST               0 (None)
#            1492 COPY                     1
#            1494 STORE_FAST               4 (@py_assert1)
#            1496 COPY                     1
#            1498 STORE_FAST               6 (@py_assert3)
#            1500 STORE_FAST               9 (@py_assert4)
#            1502 RETURN_CONST             0 (None)
# 
# Disassembly of <code object TestCloudPSSModelConverterIntegration at 0x73cd93b398f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 326>:
# 326           0 RESUME                   0
#               2 LOAD_NAME                0 (__name__)
#               4 STORE_NAME               1 (__module__)
#               6 LOAD_CONST               0 ('TestCloudPSSModelConverterIntegration')
#               8 STORE_NAME               2 (__qualname__)
# 
# 328          10 LOAD_CONST               1 ('Integration tests requiring CloudPSS API access.')
#              12 STORE_NAME               3 (__doc__)
# 
# 330          14 PUSH_NULL
#              16 LOAD_NAME                4 (pytest)
#              18 LOAD_ATTR               10 (fixture)
#              38 LOAD_CONST               2 (True)
#              40 KW_NAMES                 3 (('autouse',))
#              42 CALL                     1
# 
# 331          50 LOAD_CONST               4 (<code object setup_cloudpss at 0x3af23100, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 330>)
#              52 MAKE_FUNCTION            0
# 
# 330          54 CALL                     0
# 
# 331          62 STORE_NAME               6 (setup_cloudpss)
# 
# 346          64 LOAD_CONST               5 (<code object test_fetch_ieee39_topology at 0x3aed0a40, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 346>)
#              66 MAKE_FUNCTION            0
#              68 STORE_NAME               7 (test_fetch_ieee39_topology)
# 
# 365          70 LOAD_CONST               6 (<code object test_ieee39_bus_names_resolved at 0x3aed1740, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 365>)
#              72 MAKE_FUNCTION            0
#              74 STORE_NAME               8 (test_ieee39_bus_names_resolved)
# 
# 379          76 LOAD_CONST               7 (<code object test_ieee39_branch_connectivity at 0x3aecd6d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 379>)
#              78 MAKE_FUNCTION            0
#              80 STORE_NAME               9 (test_ieee39_branch_connectivity)
# 
# 394          82 LOAD_CONST               8 (<code object test_ieee39_topology_consistency at 0x3aed1ee0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 394>)
#              84 MAKE_FUNCTION            0
#              86 STORE_NAME              10 (test_ieee39_topology_consistency)
# 
# 407          88 LOAD_CONST               9 (<code object test_ieee39_roundtrip_conversion at 0x3aed27f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 407>)
#              90 MAKE_FUNCTION            0
#              92 STORE_NAME              11 (test_ieee39_roundtrip_conversion)
#              94 RETURN_CONST            10 (None)
# 
# Disassembly of <code object setup_cloudpss at 0x3af23100, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 330>:
# 330           0 RESUME                   0
# 
# 333           2 LOAD_CONST               1 ('/home/chenying/researches/cloudpss-toolkit/.cloudpss_token_internal')
# 
# 332           4 STORE_FAST               1 (token_file)
# 
# 335           6 LOAD_GLOBAL              0 (os)
#              16 LOAD_ATTR                2 (path)
#              36 LOAD_ATTR                5 (NULL|self + exists)
#              56 LOAD_FAST                1 (token_file)
#              58 CALL                     1
#              66 POP_JUMP_IF_TRUE        21 (to 110)
# 
# 336          68 LOAD_GLOBAL              7 (NULL + pytest)
#              78 LOAD_ATTR                8 (skip)
#              98 LOAD_CONST               2 ('CloudPSS token file not found')
#             100 CALL                     1
#             108 POP_TOP
# 
# 337     >>  110 LOAD_GLOBAL             11 (NULL + open)
#             120 LOAD_FAST                1 (token_file)
#             122 LOAD_CONST               3 ('r')
#             124 CALL                     2
#             132 BEFORE_WITH
#             134 STORE_FAST               2 (f)
# 
# 338         136 LOAD_FAST                2 (f)
#             138 LOAD_ATTR               13 (NULL|self + read)
#             158 CALL                     0
#             166 LOAD_ATTR               15 (NULL|self + strip)
#             186 CALL                     0
#             194 STORE_FAST               3 (token)
# 
# 337         196 LOAD_CONST               0 (None)
#             198 LOAD_CONST               0 (None)
#             200 LOAD_CONST               0 (None)
#             202 CALL                     2
#             210 POP_TOP
# 
# 339     >>  212 LOAD_FAST_CHECK          3 (token)
#             214 POP_JUMP_IF_FALSE        5 (to 226)
#             216 LOAD_FAST                3 (token)
#             218 LOAD_CONST               4 ('your-token-here')
#             220 COMPARE_OP              40 (==)
#             224 POP_JUMP_IF_FALSE       21 (to 268)
# 
# 340     >>  226 LOAD_GLOBAL              7 (NULL + pytest)
#             236 LOAD_ATTR                8 (skip)
#             256 LOAD_CONST               5 ('CloudPSS token not configured')
#             258 CALL                     1
#             266 POP_TOP
# 
# 341     >>  268 LOAD_CONST               6 ('http://166.111.60.76:50001/')
#             270 LOAD_GLOBAL              0 (os)
#             280 LOAD_ATTR               16 (environ)
#             300 LOAD_CONST               7 ('CLOUDPSS_API_URL')
#             302 STORE_SUBSCR
# 
# 342         306 LOAD_CONST               8 (0)
#             308 LOAD_CONST               0 (None)
#             310 IMPORT_NAME              9 (cloudpss)
#             312 STORE_FAST               4 (cloudpss)
# 
# 344         314 LOAD_FAST                4 (cloudpss)
#             316 LOAD_ATTR               21 (NULL|self + setToken)
#             336 LOAD_FAST                3 (token)
#             338 CALL                     1
#             346 POP_TOP
#             348 RETURN_CONST             0 (None)
# 
# 337     >>  350 PUSH_EXC_INFO
#             352 WITH_EXCEPT_START
#             354 POP_JUMP_IF_TRUE         1 (to 358)
#             356 RERAISE                  2
#         >>  358 POP_TOP
#             360 POP_EXCEPT
#             362 POP_TOP
#             364 POP_TOP
#             366 JUMP_BACKWARD           78 (to 212)
#         >>  368 COPY                     3
#             370 POP_EXCEPT
#             372 RERAISE                  1
# ExceptionTable:
#   134 to 194 -> 350 [1] lasti
#   350 to 358 -> 368 [3] lasti
# 
# Disassembly of <code object test_fetch_ieee39_topology at 0x3aed0a40, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 346>:
# 346           0 RESUME                   0
# 
# 347           2 LOAD_CONST               1 (0)
#               4 LOAD_CONST               2 (('Model',))
#               6 IMPORT_NAME              0 (cloudpss.model)
#               8 IMPORT_FROM              1 (Model)
#              10 STORE_FAST               1 (Model)
#              12 POP_TOP
# 
# 349          14 LOAD_FAST                1 (Model)
#              16 LOAD_ATTR                5 (NULL|self + fetch)
#              36 LOAD_CONST               3 ('model/chenying/IEEE39')
#              38 CALL                     1
#              46 STORE_FAST               2 (model)
# 
# 350          48 LOAD_CONST               0 (None)
#              50 STORE_FAST               3 (@py_assert2)
#              52 LOAD_FAST                2 (model)
#              54 LOAD_FAST                3 (@py_assert2)
#              56 IS_OP                    1
#              58 STORE_FAST               4 (@py_assert1)
#              60 LOAD_FAST                4 (@py_assert1)
#              62 POP_JUMP_IF_TRUE       153 (to 370)
#              64 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#              74 LOAD_ATTR                8 (_call_reprcompare)
#              94 LOAD_CONST               4 (('is not',))
#              96 LOAD_FAST                4 (@py_assert1)
#              98 BUILD_TUPLE              1
#             100 LOAD_CONST               5 (('%(py0)s is not %(py3)s',))
#             102 LOAD_FAST                2 (model)
#             104 LOAD_FAST                3 (@py_assert2)
#             106 BUILD_TUPLE              2
#             108 CALL                     4
#             116 LOAD_CONST               6 ('model')
#             118 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             128 LOAD_ATTR               12 (locals)
#             148 CALL                     0
#             156 CONTAINS_OP              0
#             158 POP_JUMP_IF_TRUE        21 (to 202)
#             160 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             170 LOAD_ATTR               14 (_should_repr_global_name)
#             190 LOAD_FAST                2 (model)
#             192 CALL                     1
#             200 POP_JUMP_IF_FALSE       21 (to 244)
#         >>  202 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             212 LOAD_ATTR               16 (_saferepr)
#             232 LOAD_FAST                2 (model)
#             234 CALL                     1
#             242 JUMP_FORWARD             1 (to 246)
#         >>  244 LOAD_CONST               6 ('model')
#         >>  246 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             256 LOAD_ATTR               16 (_saferepr)
#             276 LOAD_FAST                3 (@py_assert2)
#             278 CALL                     1
#             286 LOAD_CONST               7 (('py0', 'py3'))
#             288 BUILD_CONST_KEY_MAP      2
#             290 BINARY_OP                6 (%)
#             294 STORE_FAST               5 (@py_format4)
#             296 LOAD_CONST               8 ('assert %(py5)s')
#             298 LOAD_CONST               9 ('py5')
#             300 LOAD_FAST                5 (@py_format4)
#             302 BUILD_MAP                1
#             304 BINARY_OP                6 (%)
#             308 STORE_FAST               6 (@py_format6)
#             310 LOAD_GLOBAL             19 (NULL + AssertionError)
#             320 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             330 LOAD_ATTR               20 (_format_explanation)
#             350 LOAD_FAST                6 (@py_format6)
#             352 CALL                     1
#             360 CALL                     1
#             368 RAISE_VARARGS            1
#         >>  370 LOAD_CONST               0 (None)
#             372 COPY                     1
#             374 STORE_FAST               4 (@py_assert1)
#             376 STORE_FAST               3 (@py_assert2)
# 
# 352         378 LOAD_GLOBAL             23 (NULL + CloudPSSModelConverter)
#             388 CALL                     0
#             396 STORE_FAST               7 (converter)
# 
# 353         398 LOAD_FAST                7 (converter)
#             400 LOAD_ATTR               25 (NULL|self + convert_to_model)
#             420 LOAD_FAST                2 (model)
#             422 CALL                     1
#             430 UNPACK_SEQUENCE          2
#             434 STORE_FAST               8 (psm)
#             436 STORE_FAST               9 (report)
# 
# 355         438 LOAD_FAST                9 (report)
#             440 LOAD_ATTR               26 (is_success)
#             460 STORE_FAST               4 (@py_assert1)
#             462 LOAD_FAST                4 (@py_assert1)
#             464 POP_JUMP_IF_TRUE       156 (to 778)
#             466 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             476 LOAD_ATTR               28 (_format_assertmsg)
#             496 LOAD_CONST              10 ('Conversion failed: ')
#             498 LOAD_FAST                9 (report)
#             500 LOAD_ATTR               30 (errors)
#             520 FORMAT_VALUE             0
#             522 BUILD_STRING             2
#             524 CALL                     1
#             532 LOAD_CONST              11 ('\n>assert %(py2)s\n{%(py2)s = %(py0)s.is_success\n}')
#             534 BINARY_OP                0 (+)
#             538 LOAD_CONST              12 ('report')
#             540 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             550 LOAD_ATTR               12 (locals)
#             570 CALL                     0
#             578 CONTAINS_OP              0
#             580 POP_JUMP_IF_TRUE        21 (to 624)
#             582 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             592 LOAD_ATTR               14 (_should_repr_global_name)
#             612 LOAD_FAST                9 (report)
#             614 CALL                     1
#             622 POP_JUMP_IF_FALSE       21 (to 666)
#         >>  624 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             634 LOAD_ATTR               16 (_saferepr)
#             654 LOAD_FAST                9 (report)
#             656 CALL                     1
#             664 JUMP_FORWARD             1 (to 668)
#         >>  666 LOAD_CONST              12 ('report')
#         >>  668 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             678 LOAD_ATTR               16 (_saferepr)
#             698 LOAD_FAST                4 (@py_assert1)
#             700 CALL                     1
#             708 LOAD_CONST              13 (('py0', 'py2'))
#             710 BUILD_CONST_KEY_MAP      2
#             712 BINARY_OP                6 (%)
#             716 STORE_FAST              10 (@py_format3)
#             718 LOAD_GLOBAL             19 (NULL + AssertionError)
#             728 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             738 LOAD_ATTR               20 (_format_explanation)
#             758 LOAD_FAST               10 (@py_format3)
#             760 CALL                     1
#             768 CALL                     1
#             776 RAISE_VARARGS            1
#         >>  778 LOAD_CONST               0 (None)
#             780 STORE_FAST               4 (@py_assert1)
# 
# 356         782 LOAD_FAST                8 (psm)
#             784 LOAD_ATTR               32 (bus_count)
#             804 STORE_FAST               4 (@py_assert1)
#             806 LOAD_CONST              14 (39)
#             808 STORE_FAST              11 (@py_assert4)
#             810 LOAD_FAST                4 (@py_assert1)
#             812 LOAD_FAST               11 (@py_assert4)
#             814 COMPARE_OP              40 (==)
#             818 STORE_FAST              12 (@py_assert3)
#             820 LOAD_FAST               12 (@py_assert3)
#             822 POP_JUMP_IF_TRUE       208 (to 1240)
#             824 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             834 LOAD_ATTR                8 (_call_reprcompare)
#             854 LOAD_CONST              15 (('==',))
#             856 LOAD_FAST               12 (@py_assert3)
#             858 BUILD_TUPLE              1
#             860 LOAD_CONST              16 (('%(py2)s\n{%(py2)s = %(py0)s.bus_count\n} == %(py5)s',))
#             862 LOAD_FAST                4 (@py_assert1)
#             864 LOAD_FAST               11 (@py_assert4)
#             866 BUILD_TUPLE              2
#             868 CALL                     4
#             876 LOAD_CONST              17 ('psm')
#             878 LOAD_GLOBAL             11 (NULL + @py_builtins)
#             888 LOAD_ATTR               12 (locals)
#             908 CALL                     0
#             916 CONTAINS_OP              0
#             918 POP_JUMP_IF_TRUE        21 (to 962)
#             920 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             930 LOAD_ATTR               14 (_should_repr_global_name)
#             950 LOAD_FAST                8 (psm)
#             952 CALL                     1
#             960 POP_JUMP_IF_FALSE       21 (to 1004)
#         >>  962 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#             972 LOAD_ATTR               16 (_saferepr)
#             992 LOAD_FAST                8 (psm)
#             994 CALL                     1
#            1002 JUMP_FORWARD             1 (to 1006)
#         >> 1004 LOAD_CONST              17 ('psm')
#         >> 1006 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1016 LOAD_ATTR               16 (_saferepr)
#            1036 LOAD_FAST                4 (@py_assert1)
#            1038 CALL                     1
#            1046 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1056 LOAD_ATTR               16 (_saferepr)
#            1076 LOAD_FAST               11 (@py_assert4)
#            1078 CALL                     1
#            1086 LOAD_CONST              18 (('py0', 'py2', 'py5'))
#            1088 BUILD_CONST_KEY_MAP      3
#            1090 BINARY_OP                6 (%)
#            1094 STORE_FAST               6 (@py_format6)
#            1096 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1106 LOAD_ATTR               28 (_format_assertmsg)
#            1126 LOAD_CONST              19 ('Expected 39 buses, got ')
#            1128 LOAD_FAST                8 (psm)
#            1130 LOAD_ATTR               32 (bus_count)
#            1150 FORMAT_VALUE             0
#            1152 BUILD_STRING             2
#            1154 CALL                     1
#            1162 LOAD_CONST              20 ('\n>assert %(py7)s')
#            1164 BINARY_OP                0 (+)
#            1168 LOAD_CONST              21 ('py7')
#            1170 LOAD_FAST                6 (@py_format6)
#            1172 BUILD_MAP                1
#            1174 BINARY_OP                6 (%)
#            1178 STORE_FAST              13 (@py_format8)
#            1180 LOAD_GLOBAL             19 (NULL + AssertionError)
#            1190 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            1200 LOAD_ATTR               20 (_format_explanation)
#            1220 LOAD_FAST               13 (@py_format8)
#            1222 CALL                     1
#            1230 CALL                     1
#            1238 RAISE_VARARGS            1
#         >> 1240 LOAD_CONST               0 (None)
#            1242 COPY                     1
#            1244 STORE_FAST               4 (@py_assert1)
#            1246 COPY                     1
#            1248 STORE_FAST              12 (@py_assert3)
#            1250 STORE_FAST              11 (@py_assert4)
# 
# 357        1252 LOAD_FAST                8 (psm)
#            1254 LOAD_ATTR               34 (branch_count)
#            1274 STORE_FAST               4 (@py_assert1)
#            1276 LOAD_CONST              22 (34)
#            1278 STORE_FAST              11 (@py_assert4)
#            1280 LOAD_FAST                4 (@py_assert1)
#            1282 LOAD_FAST               11 (@py_assert4)
#            1284 COMPARE_OP              92 (>=)
#            1288 STORE_FAST              12 (@py_assert3)
#            1290 LOAD_FAST               12 (@py_assert3)
#            1292 POP_JUMP_IF_TRUE       208 (to 1710)
#            1294 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 359        1304 LOAD_ATTR                8 (_call_reprcompare)
# 
# 357        1324 LOAD_CONST              23 (('>=',))
#            1326 LOAD_FAST               12 (@py_assert3)
#            1328 BUILD_TUPLE              1
#            1330 LOAD_CONST              24 (('%(py2)s\n{%(py2)s = %(py0)s.branch_count\n} >= %(py5)s',))
#            1332 LOAD_FAST                4 (@py_assert1)
#            1334 LOAD_FAST               11 (@py_assert4)
#            1336 BUILD_TUPLE              2
#            1338 CALL                     4
#            1346 LOAD_CONST              17 ('psm')
#            1348 LOAD_GLOBAL             11 (NULL + @py_builtins)
# 
# 359        1358 LOAD_ATTR               12 (locals)
# 
# 357        1378 CALL                     0
#            1386 CONTAINS_OP              0
#            1388 POP_JUMP_IF_TRUE        21 (to 1432)
#            1390 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 359        1400 LOAD_ATTR               14 (_should_repr_global_name)
# 
# 357        1420 LOAD_FAST                8 (psm)
#            1422 CALL                     1
#            1430 POP_JUMP_IF_FALSE       21 (to 1474)
#         >> 1432 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 359        1442 LOAD_ATTR               16 (_saferepr)
# 
# 357        1462 LOAD_FAST                8 (psm)
#            1464 CALL                     1
#            1472 JUMP_FORWARD             1 (to 1476)
#         >> 1474 LOAD_CONST              17 ('psm')
#         >> 1476 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 359        1486 LOAD_ATTR               16 (_saferepr)
# 
# 357        1506 LOAD_FAST                4 (@py_assert1)
#            1508 CALL                     1
#            1516 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 359        1526 LOAD_ATTR               16 (_saferepr)
# 
# 357        1546 LOAD_FAST               11 (@py_assert4)
#            1548 CALL                     1
#            1556 LOAD_CONST              18 (('py0', 'py2', 'py5'))
#            1558 BUILD_CONST_KEY_MAP      3
#            1560 BINARY_OP                6 (%)
#            1564 STORE_FAST               6 (@py_format6)
#            1566 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 359        1576 LOAD_ATTR               28 (_format_assertmsg)
# 
# 358        1596 LOAD_CONST              25 ('Expected >= 34 branches, got ')
#            1598 LOAD_FAST                8 (psm)
#            1600 LOAD_ATTR               34 (branch_count)
#            1620 FORMAT_VALUE             0
#            1622 BUILD_STRING             2
# 
# 357        1624 CALL                     1
#            1632 LOAD_CONST              20 ('\n>assert %(py7)s')
#            1634 BINARY_OP                0 (+)
#            1638 LOAD_CONST              21 ('py7')
#            1640 LOAD_FAST                6 (@py_format6)
#            1642 BUILD_MAP                1
#            1644 BINARY_OP                6 (%)
#            1648 STORE_FAST              13 (@py_format8)
#            1650 LOAD_GLOBAL             19 (NULL + AssertionError)
#            1660 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 359        1670 LOAD_ATTR               20 (_format_explanation)
# 
# 357        1690 LOAD_FAST               13 (@py_format8)
#            1692 CALL                     1
#            1700 CALL                     1
#            1708 RAISE_VARARGS            1
#         >> 1710 LOAD_CONST               0 (None)
#            1712 COPY                     1
#            1714 STORE_FAST               4 (@py_assert1)
#            1716 COPY                     1
#            1718 STORE_FAST              12 (@py_assert3)
#            1720 STORE_FAST              11 (@py_assert4)
# 
# 360        1722 LOAD_FAST                8 (psm)
#            1724 LOAD_ATTR               36 (generators)
#            1744 STORE_FAST               3 (@py_assert2)
#            1746 LOAD_GLOBAL             39 (NULL + len)
#            1756 LOAD_FAST                3 (@py_assert2)
#            1758 CALL                     1
#            1766 STORE_FAST              11 (@py_assert4)
#            1768 LOAD_CONST              26 (10)
#            1770 STORE_FAST              14 (@py_assert7)
#            1772 LOAD_FAST               11 (@py_assert4)
#            1774 LOAD_FAST               14 (@py_assert7)
#            1776 COMPARE_OP              40 (==)
#            1780 STORE_FAST              15 (@py_assert6)
#            1782 LOAD_FAST               15 (@py_assert6)
#            1784 EXTENDED_ARG             1
#            1786 POP_JUMP_IF_TRUE       310 (to 2408)
#            1788 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 362        1798 LOAD_ATTR                8 (_call_reprcompare)
# 
# 360        1818 LOAD_CONST              15 (('==',))
#            1820 LOAD_FAST               15 (@py_assert6)
#            1822 BUILD_TUPLE              1
#            1824 LOAD_CONST              27 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.generators\n})\n} == %(py8)s',))
#            1826 LOAD_FAST               11 (@py_assert4)
#            1828 LOAD_FAST               14 (@py_assert7)
#            1830 BUILD_TUPLE              2
#            1832 CALL                     4
#            1840 LOAD_CONST              28 ('len')
#            1842 LOAD_GLOBAL             11 (NULL + @py_builtins)
# 
# 362        1852 LOAD_ATTR               12 (locals)
# 
# 360        1872 CALL                     0
#            1880 CONTAINS_OP              0
#            1882 POP_JUMP_IF_TRUE        25 (to 1934)
#            1884 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 362        1894 LOAD_ATTR               14 (_should_repr_global_name)
# 
# 360        1914 LOAD_GLOBAL             38 (len)
#            1924 CALL                     1
#            1932 POP_JUMP_IF_FALSE       25 (to 1984)
#         >> 1934 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 362        1944 LOAD_ATTR               16 (_saferepr)
# 
# 360        1964 LOAD_GLOBAL             38 (len)
#            1974 CALL                     1
#            1982 JUMP_FORWARD             1 (to 1986)
#         >> 1984 LOAD_CONST              28 ('len')
#         >> 1986 LOAD_CONST              17 ('psm')
#            1988 LOAD_GLOBAL             11 (NULL + @py_builtins)
# 
# 362        1998 LOAD_ATTR               12 (locals)
# 
# 360        2018 CALL                     0
#            2026 CONTAINS_OP              0
#            2028 POP_JUMP_IF_TRUE        21 (to 2072)
#            2030 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 362        2040 LOAD_ATTR               14 (_should_repr_global_name)
# 
# 360        2060 LOAD_FAST                8 (psm)
#            2062 CALL                     1
#            2070 POP_JUMP_IF_FALSE       21 (to 2114)
#         >> 2072 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 362        2082 LOAD_ATTR               16 (_saferepr)
# 
# 360        2102 LOAD_FAST                8 (psm)
#            2104 CALL                     1
#            2112 JUMP_FORWARD             1 (to 2116)
#         >> 2114 LOAD_CONST              17 ('psm')
#         >> 2116 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 362        2126 LOAD_ATTR               16 (_saferepr)
# 
# 360        2146 LOAD_FAST                3 (@py_assert2)
#            2148 CALL                     1
#            2156 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 362        2166 LOAD_ATTR               16 (_saferepr)
# 
# 360        2186 LOAD_FAST               11 (@py_assert4)
#            2188 CALL                     1
#            2196 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 362        2206 LOAD_ATTR               16 (_saferepr)
# 
# 360        2226 LOAD_FAST               14 (@py_assert7)
#            2228 CALL                     1
#            2236 LOAD_CONST              29 (('py0', 'py1', 'py3', 'py5', 'py8'))
#            2238 BUILD_CONST_KEY_MAP      5
#            2240 BINARY_OP                6 (%)
#            2244 STORE_FAST              16 (@py_format9)
#            2246 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 362        2256 LOAD_ATTR               28 (_format_assertmsg)
# 
# 361        2276 LOAD_CONST              30 ('Expected 10 generators, got ')
#            2278 LOAD_GLOBAL             39 (NULL + len)
#            2288 LOAD_FAST                8 (psm)
#            2290 LOAD_ATTR               36 (generators)
#            2310 CALL                     1
#            2318 FORMAT_VALUE             0
#            2320 BUILD_STRING             2
# 
# 360        2322 CALL                     1
#            2330 LOAD_CONST              31 ('\n>assert %(py10)s')
#            2332 BINARY_OP                0 (+)
#            2336 LOAD_CONST              32 ('py10')
#            2338 LOAD_FAST               16 (@py_format9)
#            2340 BUILD_MAP                1
#            2342 BINARY_OP                6 (%)
#            2346 STORE_FAST              17 (@py_format11)
#            2348 LOAD_GLOBAL             19 (NULL + AssertionError)
#            2358 LOAD_GLOBAL              7 (NULL + @pytest_ar)
# 
# 362        2368 LOAD_ATTR               20 (_format_explanation)
# 
# 360        2388 LOAD_FAST               17 (@py_format11)
#            2390 CALL                     1
#            2398 CALL                     1
#            2406 RAISE_VARARGS            1
#         >> 2408 LOAD_CONST               0 (None)
#            2410 COPY                     1
#            2412 STORE_FAST               3 (@py_assert2)
#            2414 COPY                     1
#            2416 STORE_FAST              11 (@py_assert4)
#            2418 COPY                     1
#            2420 STORE_FAST              15 (@py_assert6)
#            2422 STORE_FAST              14 (@py_assert7)
# 
# 363        2424 LOAD_FAST                8 (psm)
#            2426 LOAD_ATTR               40 (loads)
#            2446 STORE_FAST               3 (@py_assert2)
#            2448 LOAD_GLOBAL             39 (NULL + len)
#            2458 LOAD_FAST                3 (@py_assert2)
#            2460 CALL                     1
#            2468 STORE_FAST              11 (@py_assert4)
#            2470 LOAD_CONST              33 (19)
#            2472 STORE_FAST              14 (@py_assert7)
#            2474 LOAD_FAST               11 (@py_assert4)
#            2476 LOAD_FAST               14 (@py_assert7)
#            2478 COMPARE_OP              92 (>=)
#            2482 STORE_FAST              15 (@py_assert6)
#            2484 LOAD_FAST               15 (@py_assert6)
#            2486 EXTENDED_ARG             1
#            2488 POP_JUMP_IF_TRUE       310 (to 3110)
#            2490 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            2500 LOAD_ATTR                8 (_call_reprcompare)
#            2520 LOAD_CONST              23 (('>=',))
#            2522 LOAD_FAST               15 (@py_assert6)
#            2524 BUILD_TUPLE              1
#            2526 LOAD_CONST              34 (('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.loads\n})\n} >= %(py8)s',))
#            2528 LOAD_FAST               11 (@py_assert4)
#            2530 LOAD_FAST               14 (@py_assert7)
#            2532 BUILD_TUPLE              2
#            2534 CALL                     4
#            2542 LOAD_CONST              28 ('len')
#            2544 LOAD_GLOBAL             11 (NULL + @py_builtins)
#            2554 LOAD_ATTR               12 (locals)
#            2574 CALL                     0
#            2582 CONTAINS_OP              0
#            2584 POP_JUMP_IF_TRUE        25 (to 2636)
#            2586 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            2596 LOAD_ATTR               14 (_should_repr_global_name)
#            2616 LOAD_GLOBAL             38 (len)
#            2626 CALL                     1
#            2634 POP_JUMP_IF_FALSE       25 (to 2686)
#         >> 2636 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            2646 LOAD_ATTR               16 (_saferepr)
#            2666 LOAD_GLOBAL             38 (len)
#            2676 CALL                     1
#            2684 JUMP_FORWARD             1 (to 2688)
#         >> 2686 LOAD_CONST              28 ('len')
#         >> 2688 LOAD_CONST              17 ('psm')
#            2690 LOAD_GLOBAL             11 (NULL + @py_builtins)
#            2700 LOAD_ATTR               12 (locals)
#            2720 CALL                     0
#            2728 CONTAINS_OP              0
#            2730 POP_JUMP_IF_TRUE        21 (to 2774)
#            2732 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            2742 LOAD_ATTR               14 (_should_repr_global_name)
#            2762 LOAD_FAST                8 (psm)
#            2764 CALL                     1
#            2772 POP_JUMP_IF_FALSE       21 (to 2816)
#         >> 2774 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            2784 LOAD_ATTR               16 (_saferepr)
#            2804 LOAD_FAST                8 (psm)
#            2806 CALL                     1
#            2814 JUMP_FORWARD             1 (to 2818)
#         >> 2816 LOAD_CONST              17 ('psm')
#         >> 2818 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            2828 LOAD_ATTR               16 (_saferepr)
#            2848 LOAD_FAST                3 (@py_assert2)
#            2850 CALL                     1
#            2858 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            2868 LOAD_ATTR               16 (_saferepr)
#            2888 LOAD_FAST               11 (@py_assert4)
#            2890 CALL                     1
#            2898 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            2908 LOAD_ATTR               16 (_saferepr)
#            2928 LOAD_FAST               14 (@py_assert7)
#            2930 CALL                     1
#            2938 LOAD_CONST              29 (('py0', 'py1', 'py3', 'py5', 'py8'))
#            2940 BUILD_CONST_KEY_MAP      5
#            2942 BINARY_OP                6 (%)
#            2946 STORE_FAST              16 (@py_format9)
#            2948 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            2958 LOAD_ATTR               28 (_format_assertmsg)
#            2978 LOAD_CONST              35 ('Expected >= 19 loads, got ')
#            2980 LOAD_GLOBAL             39 (NULL + len)
#            2990 LOAD_FAST                8 (psm)
#            2992 LOAD_ATTR               40 (loads)
#            3012 CALL                     1
#            3020 FORMAT_VALUE             0
#            3022 BUILD_STRING             2
#            3024 CALL                     1
#            3032 LOAD_CONST              31 ('\n>assert %(py10)s')
#            3034 BINARY_OP                0 (+)
#            3038 LOAD_CONST              32 ('py10')
#            3040 LOAD_FAST               16 (@py_format9)
#            3042 BUILD_MAP                1
#            3044 BINARY_OP                6 (%)
#            3048 STORE_FAST              17 (@py_format11)
#            3050 LOAD_GLOBAL             19 (NULL + AssertionError)
#            3060 LOAD_GLOBAL              7 (NULL + @pytest_ar)
#            3070 LOAD_ATTR               20 (_format_explanation)
#            3090 LOAD_FAST               17 (@py_format11)
#            3092 CALL                     1
#            3100 CALL                     1
#            3108 RAISE_VARARGS            1
#         >> 3110 LOAD_CONST               0 (None)
#            3112 COPY                     1
#            3114 STORE_FAST               3 (@py_assert2)
#            3116 COPY                     1
#            3118 STORE_FAST              11 (@py_assert4)
#            3120 COPY                     1
#            3122 STORE_FAST              15 (@py_assert6)
#            3124 STORE_FAST              14 (@py_assert7)
#            3126 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_ieee39_bus_names_resolved at 0x3aed1740, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 365>:
# 365           0 RESUME                   0
# 
# 366           2 LOAD_CONST               1 (0)
#               4 LOAD_CONST               2 (('Model',))
#               6 IMPORT_NAME              0 (cloudpss.model)
#               8 IMPORT_FROM              1 (Model)
#              10 STORE_FAST               1 (Model)
#              12 POP_TOP
# 
# 368          14 LOAD_FAST                1 (Model)
#              16 LOAD_ATTR                5 (NULL|self + fetch)
#              36 LOAD_CONST               3 ('model/chenying/IEEE39')
#              38 CALL                     1
#              46 STORE_FAST               2 (model)
# 
# 369          48 LOAD_GLOBAL              7 (NULL + CloudPSSModelConverter)
#              58 CALL                     0
#              66 STORE_FAST               3 (converter)
# 
# 370          68 LOAD_FAST                3 (converter)
#              70 LOAD_ATTR                9 (NULL|self + convert_to_model)
#              90 LOAD_FAST                2 (model)
#              92 CALL                     1
#             100 UNPACK_SEQUENCE          2
#             104 STORE_FAST               4 (psm)
#             106 STORE_FAST               5 (report)
# 
# 372         108 LOAD_FAST                5 (report)
#             110 LOAD_ATTR               10 (is_success)
#             130 STORE_FAST               6 (@py_assert1)
#             132 LOAD_FAST                6 (@py_assert1)
#             134 POP_JUMP_IF_TRUE       121 (to 378)
#             136 LOAD_CONST               4 ('assert %(py2)s\n{%(py2)s = %(py0)s.is_success\n}')
#             138 LOAD_CONST               5 ('report')
#             140 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             150 LOAD_ATTR               14 (locals)
#             170 CALL                     0
#             178 CONTAINS_OP              0
#             180 POP_JUMP_IF_TRUE        21 (to 224)
#             182 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             192 LOAD_ATTR               18 (_should_repr_global_name)
#             212 LOAD_FAST                5 (report)
#             214 CALL                     1
#             222 POP_JUMP_IF_FALSE       21 (to 266)
#         >>  224 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             234 LOAD_ATTR               20 (_saferepr)
#             254 LOAD_FAST                5 (report)
#             256 CALL                     1
#             264 JUMP_FORWARD             1 (to 268)
#         >>  266 LOAD_CONST               5 ('report')
#         >>  268 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             278 LOAD_ATTR               20 (_saferepr)
#             298 LOAD_FAST                6 (@py_assert1)
#             300 CALL                     1
#             308 LOAD_CONST               6 (('py0', 'py2'))
#             310 BUILD_CONST_KEY_MAP      2
#             312 BINARY_OP                6 (%)
#             316 STORE_FAST               7 (@py_format3)
#             318 LOAD_GLOBAL             23 (NULL + AssertionError)
#             328 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             338 LOAD_ATTR               24 (_format_explanation)
#             358 LOAD_FAST                7 (@py_format3)
#             360 CALL                     1
#             368 CALL                     1
#             376 RAISE_VARARGS            1
#         >>  378 LOAD_CONST               0 (None)
#             380 STORE_FAST               6 (@py_assert1)
# 
# 373         382 LOAD_FAST                4 (psm)
#             384 LOAD_ATTR               26 (buses)
#             404 GET_ITER
#             406 LOAD_FAST_AND_CLEAR      8 (b)
#             408 SWAP                     2
#             410 BUILD_SET                0
#             412 SWAP                     2
#         >>  414 FOR_ITER                14 (to 446)
#             418 STORE_FAST               8 (b)
#             420 LOAD_FAST                8 (b)
#             422 LOAD_ATTR               28 (name)
#             442 SET_ADD                  2
#             444 JUMP_BACKWARD           16 (to 414)
#         >>  446 END_FOR
#             448 STORE_FAST               9 (bus_names)
#             450 STORE_FAST               8 (b)
# 
# 374         452 LOAD_GLOBAL             31 (NULL + len)
#             462 LOAD_FAST                9 (bus_names)
#             464 CALL                     1
#             472 STORE_FAST              10 (@py_assert2)
#             474 LOAD_CONST               7 (39)
#             476 STORE_FAST              11 (@py_assert5)
#             478 LOAD_FAST               10 (@py_assert2)
#             480 LOAD_FAST               11 (@py_assert5)
#             482 COMPARE_OP              40 (==)
#             486 STORE_FAST              12 (@py_assert4)
#             488 LOAD_FAST               12 (@py_assert4)
#             490 POP_JUMP_IF_TRUE       246 (to 984)
#             492 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             502 LOAD_ATTR               32 (_call_reprcompare)
#             522 LOAD_CONST               8 (('==',))
#             524 LOAD_FAST               12 (@py_assert4)
#             526 BUILD_TUPLE              1
#             528 LOAD_CONST               9 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             530 LOAD_FAST               10 (@py_assert2)
#             532 LOAD_FAST               11 (@py_assert5)
#             534 BUILD_TUPLE              2
#             536 CALL                     4
#             544 LOAD_CONST              10 ('len')
#             546 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             556 LOAD_ATTR               14 (locals)
#             576 CALL                     0
#             584 CONTAINS_OP              0
#             586 POP_JUMP_IF_TRUE        25 (to 638)
#             588 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             598 LOAD_ATTR               18 (_should_repr_global_name)
#             618 LOAD_GLOBAL             30 (len)
#             628 CALL                     1
#             636 POP_JUMP_IF_FALSE       25 (to 688)
#         >>  638 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             648 LOAD_ATTR               20 (_saferepr)
#             668 LOAD_GLOBAL             30 (len)
#             678 CALL                     1
#             686 JUMP_FORWARD             1 (to 690)
#         >>  688 LOAD_CONST              10 ('len')
#         >>  690 LOAD_CONST              11 ('bus_names')
#             692 LOAD_GLOBAL             13 (NULL + @py_builtins)
#             702 LOAD_ATTR               14 (locals)
#             722 CALL                     0
#             730 CONTAINS_OP              0
#             732 POP_JUMP_IF_TRUE        21 (to 776)
#             734 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             744 LOAD_ATTR               18 (_should_repr_global_name)
#             764 LOAD_FAST                9 (bus_names)
#             766 CALL                     1
#             774 POP_JUMP_IF_FALSE       21 (to 818)
#         >>  776 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             786 LOAD_ATTR               20 (_saferepr)
#             806 LOAD_FAST                9 (bus_names)
#             808 CALL                     1
#             816 JUMP_FORWARD             1 (to 820)
#         >>  818 LOAD_CONST              11 ('bus_names')
#         >>  820 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             830 LOAD_ATTR               20 (_saferepr)
#             850 LOAD_FAST               10 (@py_assert2)
#             852 CALL                     1
#             860 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             870 LOAD_ATTR               20 (_saferepr)
#             890 LOAD_FAST               11 (@py_assert5)
#             892 CALL                     1
#             900 LOAD_CONST              12 (('py0', 'py1', 'py3', 'py6'))
#             902 BUILD_CONST_KEY_MAP      4
#             904 BINARY_OP                6 (%)
#             908 STORE_FAST              13 (@py_format7)
#             910 LOAD_CONST              13 ('assert %(py8)s')
#             912 LOAD_CONST              14 ('py8')
#             914 LOAD_FAST               13 (@py_format7)
#             916 BUILD_MAP                1
#             918 BINARY_OP                6 (%)
#             922 STORE_FAST              14 (@py_format9)
#             924 LOAD_GLOBAL             23 (NULL + AssertionError)
#             934 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#             944 LOAD_ATTR               24 (_format_explanation)
#             964 LOAD_FAST               14 (@py_format9)
#             966 CALL                     1
#             974 CALL                     1
#             982 RAISE_VARARGS            1
#         >>  984 LOAD_CONST               0 (None)
#             986 COPY                     1
#             988 STORE_FAST              10 (@py_assert2)
#             990 COPY                     1
#             992 STORE_FAST              12 (@py_assert4)
#             994 STORE_FAST              11 (@py_assert5)
# 
# 376         996 LOAD_FAST                4 (psm)
#             998 LOAD_ATTR               26 (buses)
#            1018 GET_ITER
#            1020 LOAD_FAST_AND_CLEAR      8 (b)
#            1022 SWAP                     2
#            1024 BUILD_LIST               0
#            1026 SWAP                     2
#         >> 1028 FOR_ITER                42 (to 1116)
#            1032 STORE_FAST               8 (b)
#            1034 LOAD_FAST                8 (b)
#            1036 LOAD_ATTR               28 (name)
#            1056 LOAD_ATTR               35 (NULL|self + startswith)
#            1076 LOAD_CONST              15 ('Unknown')
#            1078 CALL                     1
#            1086 POP_JUMP_IF_TRUE         1 (to 1090)
#            1088 JUMP_BACKWARD           31 (to 1028)
#         >> 1090 LOAD_FAST                8 (b)
#            1092 LOAD_ATTR               28 (name)
#            1112 LIST_APPEND              2
#            1114 JUMP_BACKWARD           44 (to 1028)
#         >> 1116 END_FOR
#            1118 STORE_FAST              15 (unknown_buses)
#            1120 STORE_FAST               8 (b)
# 
# 377        1122 LOAD_GLOBAL             31 (NULL + len)
#            1132 LOAD_FAST               15 (unknown_buses)
#            1134 CALL                     1
#            1142 STORE_FAST              10 (@py_assert2)
#            1144 LOAD_CONST               1 (0)
#            1146 STORE_FAST              11 (@py_assert5)
#            1148 LOAD_FAST               10 (@py_assert2)
#            1150 LOAD_FAST               11 (@py_assert5)
#            1152 COMPARE_OP              40 (==)
#            1156 STORE_FAST              12 (@py_assert4)
#            1158 LOAD_FAST               12 (@py_assert4)
#            1160 EXTENDED_ARG             1
#            1162 POP_JUMP_IF_TRUE       271 (to 1706)
#            1164 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#            1174 LOAD_ATTR               32 (_call_reprcompare)
#            1194 LOAD_CONST               8 (('==',))
#            1196 LOAD_FAST               12 (@py_assert4)
#            1198 BUILD_TUPLE              1
#            1200 LOAD_CONST               9 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#            1202 LOAD_FAST               10 (@py_assert2)
#            1204 LOAD_FAST               11 (@py_assert5)
#            1206 BUILD_TUPLE              2
#            1208 CALL                     4
#            1216 LOAD_CONST              10 ('len')
#            1218 LOAD_GLOBAL             13 (NULL + @py_builtins)
#            1228 LOAD_ATTR               14 (locals)
#            1248 CALL                     0
#            1256 CONTAINS_OP              0
#            1258 POP_JUMP_IF_TRUE        25 (to 1310)
#            1260 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#            1270 LOAD_ATTR               18 (_should_repr_global_name)
#            1290 LOAD_GLOBAL             30 (len)
#            1300 CALL                     1
#            1308 POP_JUMP_IF_FALSE       25 (to 1360)
#         >> 1310 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#            1320 LOAD_ATTR               20 (_saferepr)
#            1340 LOAD_GLOBAL             30 (len)
#            1350 CALL                     1
#            1358 JUMP_FORWARD             1 (to 1362)
#         >> 1360 LOAD_CONST              10 ('len')
#         >> 1362 LOAD_CONST              16 ('unknown_buses')
#            1364 LOAD_GLOBAL             13 (NULL + @py_builtins)
#            1374 LOAD_ATTR               14 (locals)
#            1394 CALL                     0
#            1402 CONTAINS_OP              0
#            1404 POP_JUMP_IF_TRUE        21 (to 1448)
#            1406 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#            1416 LOAD_ATTR               18 (_should_repr_global_name)
#            1436 LOAD_FAST               15 (unknown_buses)
#            1438 CALL                     1
#            1446 POP_JUMP_IF_FALSE       21 (to 1490)
#         >> 1448 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#            1458 LOAD_ATTR               20 (_saferepr)
#            1478 LOAD_FAST               15 (unknown_buses)
#            1480 CALL                     1
#            1488 JUMP_FORWARD             1 (to 1492)
#         >> 1490 LOAD_CONST              16 ('unknown_buses')
#         >> 1492 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#            1502 LOAD_ATTR               20 (_saferepr)
#            1522 LOAD_FAST               10 (@py_assert2)
#            1524 CALL                     1
#            1532 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#            1542 LOAD_ATTR               20 (_saferepr)
#            1562 LOAD_FAST               11 (@py_assert5)
#            1564 CALL                     1
#            1572 LOAD_CONST              12 (('py0', 'py1', 'py3', 'py6'))
#            1574 BUILD_CONST_KEY_MAP      4
#            1576 BINARY_OP                6 (%)
#            1580 STORE_FAST              13 (@py_format7)
#            1582 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#            1592 LOAD_ATTR               36 (_format_assertmsg)
#            1612 LOAD_CONST              17 ('Unresolved buses: ')
#            1614 LOAD_FAST               15 (unknown_buses)
#            1616 FORMAT_VALUE             0
#            1618 BUILD_STRING             2
#            1620 CALL                     1
#            1628 LOAD_CONST              18 ('\n>assert %(py8)s')
#            1630 BINARY_OP                0 (+)
#            1634 LOAD_CONST              14 ('py8')
#            1636 LOAD_FAST               13 (@py_format7)
#            1638 BUILD_MAP                1
#            1640 BINARY_OP                6 (%)
#            1644 STORE_FAST              14 (@py_format9)
#            1646 LOAD_GLOBAL             23 (NULL + AssertionError)
#            1656 LOAD_GLOBAL             17 (NULL + @pytest_ar)
#            1666 LOAD_ATTR               24 (_format_explanation)
#            1686 LOAD_FAST               14 (@py_format9)
#            1688 CALL                     1
#            1696 CALL                     1
#            1704 RAISE_VARARGS            1
#         >> 1706 LOAD_CONST               0 (None)
#            1708 COPY                     1
#            1710 STORE_FAST              10 (@py_assert2)
#            1712 COPY                     1
#            1714 STORE_FAST              12 (@py_assert4)
#            1716 STORE_FAST              11 (@py_assert5)
#            1718 RETURN_CONST             0 (None)
#         >> 1720 SWAP                     2
#            1722 POP_TOP
# 
# 373        1724 SWAP                     2
#            1726 STORE_FAST               8 (b)
#            1728 RERAISE                  0
#         >> 1730 SWAP                     2
#            1732 POP_TOP
# 
# 376        1734 SWAP                     2
#            1736 STORE_FAST               8 (b)
#            1738 RERAISE                  0
# ExceptionTable:
#   410 to 446 -> 1720 [2]
#   1024 to 1086 -> 1730 [2]
#   1090 to 1116 -> 1730 [2]
# 
# Disassembly of <code object test_ieee39_branch_connectivity at 0x3aecd6d0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 379>:
# 379           0 RESUME                   0
# 
# 380           2 LOAD_CONST               1 (0)
#               4 LOAD_CONST               2 (('Model',))
#               6 IMPORT_NAME              0 (cloudpss.model)
#               8 IMPORT_FROM              1 (Model)
#              10 STORE_FAST               1 (Model)
#              12 POP_TOP
# 
# 382          14 LOAD_FAST                1 (Model)
#              16 LOAD_ATTR                5 (NULL|self + fetch)
#              36 LOAD_CONST               3 ('model/chenying/IEEE39')
#              38 CALL                     1
#              46 STORE_FAST               2 (model)
# 
# 383          48 LOAD_GLOBAL              7 (NULL + CloudPSSModelConverter)
#              58 CALL                     0
#              66 STORE_FAST               3 (converter)
# 
# 384          68 LOAD_FAST                3 (converter)
#              70 LOAD_ATTR                9 (NULL|self + convert_to_model)
#              90 LOAD_FAST                2 (model)
#              92 CALL                     1
#             100 UNPACK_SEQUENCE          2
#             104 STORE_FAST               4 (psm)
#             106 STORE_FAST               5 (report)
# 
# 386         108 LOAD_FAST                4 (psm)
#             110 LOAD_ATTR               10 (buses)
#             130 GET_ITER
#             132 LOAD_FAST_AND_CLEAR      6 (b)
#             134 SWAP                     2
#             136 BUILD_SET                0
#             138 SWAP                     2
#         >>  140 FOR_ITER                14 (to 172)
#             144 STORE_FAST               6 (b)
#             146 LOAD_FAST                6 (b)
#             148 LOAD_ATTR               12 (name)
#             168 SET_ADD                  2
#             170 JUMP_BACKWARD           16 (to 140)
#         >>  172 END_FOR
#             174 STORE_FAST               7 (bus_names)
#             176 STORE_FAST               6 (b)
# 
# 387         178 LOAD_FAST                4 (psm)
#             180 LOAD_ATTR               15 (NULL|self + validate_topology)
#             200 CALL                     0
#             208 STORE_FAST               8 (topology_errors)
# 
# 390         210 LOAD_FAST                8 (topology_errors)
#             212 GET_ITER
# 
# 389         214 LOAD_FAST_AND_CLEAR      9 (e)
#             216 SWAP                     2
#             218 BUILD_LIST               0
#             220 SWAP                     2
# 
# 390     >>  222 FOR_ITER                14 (to 254)
#             226 STORE_FAST               9 (e)
#             228 LOAD_CONST               4 ('Branch')
#             230 LOAD_FAST                9 (e)
#             232 CONTAINS_OP              0
#             234 POP_JUMP_IF_TRUE         1 (to 238)
#             236 JUMP_BACKWARD            8 (to 222)
#         >>  238 LOAD_CONST               5 ('not found')
#             240 LOAD_FAST                9 (e)
#             242 CONTAINS_OP              0
#             244 POP_JUMP_IF_TRUE         1 (to 248)
#             246 JUMP_BACKWARD           13 (to 222)
#         >>  248 LOAD_FAST                9 (e)
#             250 LIST_APPEND              2
#             252 JUMP_BACKWARD           16 (to 222)
#         >>  254 END_FOR
# 
# 389         256 STORE_FAST              10 (branch_errors)
#             258 STORE_FAST               9 (e)
# 
# 392         260 LOAD_GLOBAL             17 (NULL + len)
#             270 LOAD_FAST               10 (branch_errors)
#             272 CALL                     1
#             280 STORE_FAST              11 (@py_assert2)
#             282 LOAD_CONST               1 (0)
#             284 STORE_FAST              12 (@py_assert5)
#             286 LOAD_FAST               11 (@py_assert2)
#             288 LOAD_FAST               12 (@py_assert5)
#             290 COMPARE_OP              40 (==)
#             294 STORE_FAST              13 (@py_assert4)
#             296 LOAD_FAST               13 (@py_assert4)
#             298 EXTENDED_ARG             1
#             300 POP_JUMP_IF_TRUE       271 (to 844)
#             302 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             312 LOAD_ATTR               20 (_call_reprcompare)
#             332 LOAD_CONST               6 (('==',))
#             334 LOAD_FAST               13 (@py_assert4)
#             336 BUILD_TUPLE              1
#             338 LOAD_CONST               7 (('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s',))
#             340 LOAD_FAST               11 (@py_assert2)
#             342 LOAD_FAST               12 (@py_assert5)
#             344 BUILD_TUPLE              2
#             346 CALL                     4
#             354 LOAD_CONST               8 ('len')
#             356 LOAD_GLOBAL             23 (NULL + @py_builtins)
#             366 LOAD_ATTR               24 (locals)
#             386 CALL                     0
#             394 CONTAINS_OP              0
#             396 POP_JUMP_IF_TRUE        25 (to 448)
#             398 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             408 LOAD_ATTR               26 (_should_repr_global_name)
#             428 LOAD_GLOBAL             16 (len)
#             438 CALL                     1
#             446 POP_JUMP_IF_FALSE       25 (to 498)
#         >>  448 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             458 LOAD_ATTR               28 (_saferepr)
#             478 LOAD_GLOBAL             16 (len)
#             488 CALL                     1
#             496 JUMP_FORWARD             1 (to 500)
#         >>  498 LOAD_CONST               8 ('len')
#         >>  500 LOAD_CONST               9 ('branch_errors')
#             502 LOAD_GLOBAL             23 (NULL + @py_builtins)
#             512 LOAD_ATTR               24 (locals)
#             532 CALL                     0
#             540 CONTAINS_OP              0
#             542 POP_JUMP_IF_TRUE        21 (to 586)
#             544 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             554 LOAD_ATTR               26 (_should_repr_global_name)
#             574 LOAD_FAST               10 (branch_errors)
#             576 CALL                     1
#             584 POP_JUMP_IF_FALSE       21 (to 628)
#         >>  586 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             596 LOAD_ATTR               28 (_saferepr)
#             616 LOAD_FAST               10 (branch_errors)
#             618 CALL                     1
#             626 JUMP_FORWARD             1 (to 630)
#         >>  628 LOAD_CONST               9 ('branch_errors')
#         >>  630 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             640 LOAD_ATTR               28 (_saferepr)
#             660 LOAD_FAST               11 (@py_assert2)
#             662 CALL                     1
#             670 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             680 LOAD_ATTR               28 (_saferepr)
#             700 LOAD_FAST               12 (@py_assert5)
#             702 CALL                     1
#             710 LOAD_CONST              10 (('py0', 'py1', 'py3', 'py6'))
#             712 BUILD_CONST_KEY_MAP      4
#             714 BINARY_OP                6 (%)
#             718 STORE_FAST              14 (@py_format7)
#             720 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             730 LOAD_ATTR               30 (_format_assertmsg)
#             750 LOAD_CONST              11 ('Branch connectivity errors: ')
#             752 LOAD_FAST               10 (branch_errors)
#             754 FORMAT_VALUE             0
#             756 BUILD_STRING             2
#             758 CALL                     1
#             766 LOAD_CONST              12 ('\n>assert %(py8)s')
#             768 BINARY_OP                0 (+)
#             772 LOAD_CONST              13 ('py8')
#             774 LOAD_FAST               14 (@py_format7)
#             776 BUILD_MAP                1
#             778 BINARY_OP                6 (%)
#             782 STORE_FAST              15 (@py_format9)
#             784 LOAD_GLOBAL             33 (NULL + AssertionError)
#             794 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             804 LOAD_ATTR               34 (_format_explanation)
#             824 LOAD_FAST               15 (@py_format9)
#             826 CALL                     1
#             834 CALL                     1
#             842 RAISE_VARARGS            1
#         >>  844 LOAD_CONST               0 (None)
#             846 COPY                     1
#             848 STORE_FAST              11 (@py_assert2)
#             850 COPY                     1
#             852 STORE_FAST              13 (@py_assert4)
#             854 STORE_FAST              12 (@py_assert5)
#             856 RETURN_CONST             0 (None)
#         >>  858 SWAP                     2
#             860 POP_TOP
# 
# 386         862 SWAP                     2
#             864 STORE_FAST               6 (b)
#             866 RERAISE                  0
#         >>  868 SWAP                     2
#             870 POP_TOP
# 
# 389         872 SWAP                     2
#             874 STORE_FAST               9 (e)
#             876 RERAISE                  0
# ExceptionTable:
#   136 to 172 -> 858 [2]
#   218 to 234 -> 868 [2]
#   238 to 244 -> 868 [2]
#   248 to 254 -> 868 [2]
# 
# Disassembly of <code object test_ieee39_topology_consistency at 0x3aed1ee0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 394>:
# 394           0 RESUME                   0
# 
# 395           2 LOAD_CONST               1 (0)
#               4 LOAD_CONST               2 (('Model',))
#               6 IMPORT_NAME              0 (cloudpss.model)
#               8 IMPORT_FROM              1 (Model)
#              10 STORE_FAST               1 (Model)
#              12 POP_TOP
# 
# 397          14 LOAD_FAST                1 (Model)
#              16 LOAD_ATTR                5 (NULL|self + fetch)
#              36 LOAD_CONST               3 ('model/chenying/IEEE39')
#              38 CALL                     1
#              46 STORE_FAST               2 (model)
# 
# 398          48 LOAD_GLOBAL              7 (NULL + CloudPSSModelConverter)
#              58 CALL                     0
#              66 STORE_FAST               3 (converter)
# 
# 399          68 LOAD_FAST                3 (converter)
#              70 LOAD_ATTR                9 (NULL|self + convert_to_model)
#              90 LOAD_FAST                2 (model)
#              92 CALL                     1
#             100 UNPACK_SEQUENCE          2
#             104 STORE_FAST               4 (psm)
#             106 STORE_FAST               5 (report)
# 
# 401         108 LOAD_FAST                4 (psm)
#             110 LOAD_ATTR               10 (total_generation_mw)
#             130 STORE_FAST               6 (total_generation)
# 
# 402         132 LOAD_FAST                4 (psm)
#             134 LOAD_ATTR               12 (total_load_mw)
#             154 STORE_FAST               7 (total_load)
# 
# 404         156 LOAD_CONST               1 (0)
#             158 STORE_FAST               8 (@py_assert2)
#             160 LOAD_FAST                6 (total_generation)
#             162 LOAD_FAST                8 (@py_assert2)
#             164 COMPARE_OP              68 (>)
#             168 STORE_FAST               9 (@py_assert1)
#             170 LOAD_FAST                9 (@py_assert1)
#             172 POP_JUMP_IF_TRUE       175 (to 524)
#             174 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             184 LOAD_ATTR               16 (_call_reprcompare)
#             204 LOAD_CONST               4 (('>',))
#             206 LOAD_FAST                9 (@py_assert1)
#             208 BUILD_TUPLE              1
#             210 LOAD_CONST               5 (('%(py0)s > %(py3)s',))
#             212 LOAD_FAST                6 (total_generation)
#             214 LOAD_FAST                8 (@py_assert2)
#             216 BUILD_TUPLE              2
#             218 CALL                     4
#             226 LOAD_CONST               6 ('total_generation')
#             228 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             238 LOAD_ATTR               20 (locals)
#             258 CALL                     0
#             266 CONTAINS_OP              0
#             268 POP_JUMP_IF_TRUE        21 (to 312)
#             270 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             280 LOAD_ATTR               22 (_should_repr_global_name)
#             300 LOAD_FAST                6 (total_generation)
#             302 CALL                     1
#             310 POP_JUMP_IF_FALSE       21 (to 354)
#         >>  312 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             322 LOAD_ATTR               24 (_saferepr)
#             342 LOAD_FAST                6 (total_generation)
#             344 CALL                     1
#             352 JUMP_FORWARD             1 (to 356)
#         >>  354 LOAD_CONST               6 ('total_generation')
#         >>  356 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             366 LOAD_ATTR               24 (_saferepr)
#             386 LOAD_FAST                8 (@py_assert2)
#             388 CALL                     1
#             396 LOAD_CONST               7 (('py0', 'py3'))
#             398 BUILD_CONST_KEY_MAP      2
#             400 BINARY_OP                6 (%)
#             404 STORE_FAST              10 (@py_format4)
#             406 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             416 LOAD_ATTR               26 (_format_assertmsg)
#             436 LOAD_CONST               8 ('Generator P values should be positive')
#             438 CALL                     1
#             446 LOAD_CONST               9 ('\n>assert %(py5)s')
#             448 BINARY_OP                0 (+)
#             452 LOAD_CONST              10 ('py5')
#             454 LOAD_FAST               10 (@py_format4)
#             456 BUILD_MAP                1
#             458 BINARY_OP                6 (%)
#             462 STORE_FAST              11 (@py_format6)
#             464 LOAD_GLOBAL             29 (NULL + AssertionError)
#             474 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             484 LOAD_ATTR               30 (_format_explanation)
#             504 LOAD_FAST               11 (@py_format6)
#             506 CALL                     1
#             514 CALL                     1
#             522 RAISE_VARARGS            1
#         >>  524 LOAD_CONST               0 (None)
#             526 COPY                     1
#             528 STORE_FAST               9 (@py_assert1)
#             530 STORE_FAST               8 (@py_assert2)
# 
# 405         532 LOAD_CONST               1 (0)
#             534 STORE_FAST               8 (@py_assert2)
#             536 LOAD_FAST                7 (total_load)
#             538 LOAD_FAST                8 (@py_assert2)
#             540 COMPARE_OP              68 (>)
#             544 STORE_FAST               9 (@py_assert1)
#             546 LOAD_FAST                9 (@py_assert1)
#             548 POP_JUMP_IF_TRUE       175 (to 900)
#             550 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             560 LOAD_ATTR               16 (_call_reprcompare)
#             580 LOAD_CONST               4 (('>',))
#             582 LOAD_FAST                9 (@py_assert1)
#             584 BUILD_TUPLE              1
#             586 LOAD_CONST               5 (('%(py0)s > %(py3)s',))
#             588 LOAD_FAST                7 (total_load)
#             590 LOAD_FAST                8 (@py_assert2)
#             592 BUILD_TUPLE              2
#             594 CALL                     4
#             602 LOAD_CONST              11 ('total_load')
#             604 LOAD_GLOBAL             19 (NULL + @py_builtins)
#             614 LOAD_ATTR               20 (locals)
#             634 CALL                     0
#             642 CONTAINS_OP              0
#             644 POP_JUMP_IF_TRUE        21 (to 688)
#             646 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             656 LOAD_ATTR               22 (_should_repr_global_name)
#             676 LOAD_FAST                7 (total_load)
#             678 CALL                     1
#             686 POP_JUMP_IF_FALSE       21 (to 730)
#         >>  688 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             698 LOAD_ATTR               24 (_saferepr)
#             718 LOAD_FAST                7 (total_load)
#             720 CALL                     1
#             728 JUMP_FORWARD             1 (to 732)
#         >>  730 LOAD_CONST              11 ('total_load')
#         >>  732 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             742 LOAD_ATTR               24 (_saferepr)
#             762 LOAD_FAST                8 (@py_assert2)
#             764 CALL                     1
#             772 LOAD_CONST               7 (('py0', 'py3'))
#             774 BUILD_CONST_KEY_MAP      2
#             776 BINARY_OP                6 (%)
#             780 STORE_FAST              10 (@py_format4)
#             782 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             792 LOAD_ATTR               26 (_format_assertmsg)
#             812 LOAD_CONST              12 ('Load P values should be positive')
#             814 CALL                     1
#             822 LOAD_CONST               9 ('\n>assert %(py5)s')
#             824 BINARY_OP                0 (+)
#             828 LOAD_CONST              10 ('py5')
#             830 LOAD_FAST               10 (@py_format4)
#             832 BUILD_MAP                1
#             834 BINARY_OP                6 (%)
#             838 STORE_FAST              11 (@py_format6)
#             840 LOAD_GLOBAL             29 (NULL + AssertionError)
#             850 LOAD_GLOBAL             15 (NULL + @pytest_ar)
#             860 LOAD_ATTR               30 (_format_explanation)
#             880 LOAD_FAST               11 (@py_format6)
#             882 CALL                     1
#             890 CALL                     1
#             898 RAISE_VARARGS            1
#         >>  900 LOAD_CONST               0 (None)
#             902 COPY                     1
#             904 STORE_FAST               9 (@py_assert1)
#             906 STORE_FAST               8 (@py_assert2)
#             908 RETURN_CONST             0 (None)
# 
# Disassembly of <code object test_ieee39_roundtrip_conversion at 0x3aed27f0, file "/home/chenying/researches/cloudpss-toolkit/cloudpss_skills_v2/tests/test_cloudpss_converter.py", line 407>:
# 407           0 RESUME                   0
# 
# 408           2 LOAD_CONST               1 (0)
#               4 LOAD_CONST               2 (('Model',))
#               6 IMPORT_NAME              0 (cloudpss.model)
#               8 IMPORT_FROM              1 (Model)
#              10 STORE_FAST               1 (Model)
#              12 POP_TOP
# 
# 410          14 LOAD_FAST                1 (Model)
#              16 LOAD_ATTR                5 (NULL|self + fetch)
#              36 LOAD_CONST               3 ('model/chenying/IEEE39')
#              38 CALL                     1
#              46 STORE_FAST               2 (model)
# 
# 411          48 LOAD_GLOBAL              7 (NULL + CloudPSSModelConverter)
#              58 CALL                     0
#              66 STORE_FAST               3 (converter)
# 
# 412          68 LOAD_FAST                3 (converter)
#              70 LOAD_ATTR                9 (NULL|self + convert_to_model)
#              90 LOAD_FAST                2 (model)
#              92 CALL                     1
#             100 UNPACK_SEQUENCE          2
#             104 STORE_FAST               4 (psm)
#             106 STORE_FAST               5 (report)
# 
# 414         108 LOAD_FAST                3 (converter)
#             110 LOAD_ATTR               11 (NULL|self + convert_from_model)
#             130 LOAD_FAST                4 (psm)
#             132 CALL                     1
#             140 UNPACK_SEQUENCE          2
#             144 STORE_FAST               6 (result)
#             146 STORE_FAST               7 (report2)
# 
# 416         148 LOAD_FAST                7 (report2)
#             150 LOAD_ATTR               12 (is_success)
#             170 STORE_FAST               8 (@py_assert1)
#             172 LOAD_FAST                8 (@py_assert1)
#             174 POP_JUMP_IF_TRUE       121 (to 418)
#             176 LOAD_CONST               4 ('assert %(py2)s\n{%(py2)s = %(py0)s.is_success\n}')
#             178 LOAD_CONST               5 ('report2')
#             180 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             190 LOAD_ATTR               16 (locals)
#             210 CALL                     0
#             218 CONTAINS_OP              0
#             220 POP_JUMP_IF_TRUE        21 (to 264)
#             222 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             232 LOAD_ATTR               20 (_should_repr_global_name)
#             252 LOAD_FAST                7 (report2)
#             254 CALL                     1
#             262 POP_JUMP_IF_FALSE       21 (to 306)
#         >>  264 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             274 LOAD_ATTR               22 (_saferepr)
#             294 LOAD_FAST                7 (report2)
#             296 CALL                     1
#             304 JUMP_FORWARD             1 (to 308)
#         >>  306 LOAD_CONST               5 ('report2')
#         >>  308 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             318 LOAD_ATTR               22 (_saferepr)
#             338 LOAD_FAST                8 (@py_assert1)
#             340 CALL                     1
#             348 LOAD_CONST               6 (('py0', 'py2'))
#             350 BUILD_CONST_KEY_MAP      2
#             352 BINARY_OP                6 (%)
#             356 STORE_FAST               9 (@py_format3)
#             358 LOAD_GLOBAL             25 (NULL + AssertionError)
#             368 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             378 LOAD_ATTR               26 (_format_explanation)
#             398 LOAD_FAST                9 (@py_format3)
#             400 CALL                     1
#             408 CALL                     1
#             416 RAISE_VARARGS            1
#         >>  418 LOAD_CONST               0 (None)
#             420 STORE_FAST               8 (@py_assert1)
# 
# 417         422 LOAD_FAST                7 (report2)
#             424 LOAD_ATTR               28 (items_converted)
#             444 STORE_FAST               8 (@py_assert1)
#             446 LOAD_CONST               1 (0)
#             448 STORE_FAST              10 (@py_assert4)
#             450 LOAD_FAST                8 (@py_assert1)
#             452 LOAD_FAST               10 (@py_assert4)
#             454 COMPARE_OP              68 (>)
#             458 STORE_FAST              11 (@py_assert3)
#             460 LOAD_FAST               11 (@py_assert3)
#             462 POP_JUMP_IF_TRUE       173 (to 810)
#             464 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             474 LOAD_ATTR               30 (_call_reprcompare)
#             494 LOAD_CONST               7 (('>',))
#             496 LOAD_FAST               11 (@py_assert3)
#             498 BUILD_TUPLE              1
#             500 LOAD_CONST               8 (('%(py2)s\n{%(py2)s = %(py0)s.items_converted\n} > %(py5)s',))
#             502 LOAD_FAST                8 (@py_assert1)
#             504 LOAD_FAST               10 (@py_assert4)
#             506 BUILD_TUPLE              2
#             508 CALL                     4
#             516 LOAD_CONST               5 ('report2')
#             518 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             528 LOAD_ATTR               16 (locals)
#             548 CALL                     0
#             556 CONTAINS_OP              0
#             558 POP_JUMP_IF_TRUE        21 (to 602)
#             560 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             570 LOAD_ATTR               20 (_should_repr_global_name)
#             590 LOAD_FAST                7 (report2)
#             592 CALL                     1
#             600 POP_JUMP_IF_FALSE       21 (to 644)
#         >>  602 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             612 LOAD_ATTR               22 (_saferepr)
#             632 LOAD_FAST                7 (report2)
#             634 CALL                     1
#             642 JUMP_FORWARD             1 (to 646)
#         >>  644 LOAD_CONST               5 ('report2')
#         >>  646 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             656 LOAD_ATTR               22 (_saferepr)
#             676 LOAD_FAST                8 (@py_assert1)
#             678 CALL                     1
#             686 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             696 LOAD_ATTR               22 (_saferepr)
#             716 LOAD_FAST               10 (@py_assert4)
#             718 CALL                     1
#             726 LOAD_CONST               9 (('py0', 'py2', 'py5'))
#             728 BUILD_CONST_KEY_MAP      3
#             730 BINARY_OP                6 (%)
#             734 STORE_FAST              12 (@py_format6)
#             736 LOAD_CONST              10 ('assert %(py7)s')
#             738 LOAD_CONST              11 ('py7')
#             740 LOAD_FAST               12 (@py_format6)
#             742 BUILD_MAP                1
#             744 BINARY_OP                6 (%)
#             748 STORE_FAST              13 (@py_format8)
#             750 LOAD_GLOBAL             25 (NULL + AssertionError)
#             760 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             770 LOAD_ATTR               26 (_format_explanation)
#             790 LOAD_FAST               13 (@py_format8)
#             792 CALL                     1
#             800 CALL                     1
#             808 RAISE_VARARGS            1
#         >>  810 LOAD_CONST               0 (None)
#             812 COPY                     1
#             814 STORE_FAST               8 (@py_assert1)
#             816 COPY                     1
#             818 STORE_FAST              11 (@py_assert3)
#             820 STORE_FAST              10 (@py_assert4)
# 
# 418         822 LOAD_CONST              12 ('components')
#             824 STORE_FAST              14 (@py_assert0)
#             826 LOAD_FAST               14 (@py_assert0)
#             828 LOAD_FAST                6 (result)
#             830 CONTAINS_OP              0
#             832 STORE_FAST              15 (@py_assert2)
#             834 LOAD_FAST               15 (@py_assert2)
#             836 POP_JUMP_IF_TRUE       153 (to 1144)
#             838 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             848 LOAD_ATTR               30 (_call_reprcompare)
#             868 LOAD_CONST              13 (('in',))
#             870 LOAD_FAST               15 (@py_assert2)
#             872 BUILD_TUPLE              1
#             874 LOAD_CONST              14 (('%(py1)s in %(py3)s',))
#             876 LOAD_FAST               14 (@py_assert0)
#             878 LOAD_FAST                6 (result)
#             880 BUILD_TUPLE              2
#             882 CALL                     4
#             890 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             900 LOAD_ATTR               22 (_saferepr)
#             920 LOAD_FAST               14 (@py_assert0)
#             922 CALL                     1
#             930 LOAD_CONST              15 ('result')
#             932 LOAD_GLOBAL             15 (NULL + @py_builtins)
#             942 LOAD_ATTR               16 (locals)
#             962 CALL                     0
#             970 CONTAINS_OP              0
#             972 POP_JUMP_IF_TRUE        21 (to 1016)
#             974 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#             984 LOAD_ATTR               20 (_should_repr_global_name)
#            1004 LOAD_FAST                6 (result)
#            1006 CALL                     1
#            1014 POP_JUMP_IF_FALSE       21 (to 1058)
#         >> 1016 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1026 LOAD_ATTR               22 (_saferepr)
#            1046 LOAD_FAST                6 (result)
#            1048 CALL                     1
#            1056 JUMP_FORWARD             1 (to 1060)
#         >> 1058 LOAD_CONST              15 ('result')
#         >> 1060 LOAD_CONST              16 (('py1', 'py3'))
#            1062 BUILD_CONST_KEY_MAP      2
#            1064 BINARY_OP                6 (%)
#            1068 STORE_FAST              16 (@py_format4)
#            1070 LOAD_CONST              17 ('assert %(py5)s')
#            1072 LOAD_CONST              18 ('py5')
#            1074 LOAD_FAST               16 (@py_format4)
#            1076 BUILD_MAP                1
#            1078 BINARY_OP                6 (%)
#            1082 STORE_FAST              12 (@py_format6)
#            1084 LOAD_GLOBAL             25 (NULL + AssertionError)
#            1094 LOAD_GLOBAL             19 (NULL + @pytest_ar)
#            1104 LOAD_ATTR               26 (_format_explanation)
#            1124 LOAD_FAST               12 (@py_format6)
#            1126 CALL                     1
#            1134 CALL                     1
#            1142 RAISE_VARARGS            1
#         >> 1144 LOAD_CONST               0 (None)
#            1146 COPY                     1
#            1148 STORE_FAST              14 (@py_assert0)
#            1150 STORE_FAST              15 (@py_assert2)
#            1152 RETURN_CONST             0 (None)
# 