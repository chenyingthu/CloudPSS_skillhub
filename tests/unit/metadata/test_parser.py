"""
文档解析器单元测试
"""

import pytest
from cloudpss_skills.metadata.parser import (
    ParameterTableParser,
    ComponentDocumentParser,
    BatchMetadataExtractor
)
from cloudpss_skills.metadata.models import ComponentMetadata


class TestParameterTableParser:
    """参数表格解析器测试"""

    def setup_method(self):
        self.parser = ParameterTableParser()

    def test_parse_basic_table(self):
        """测试解析基本表格"""
        table = """
| 参数名 | 显示名 | 类型 | 单位 | 描述 | 默认值 |
|--------|--------|------|------|------|--------|
| Vpcc | 并网点电压 | real | kV | 并网点的电压 | 0.69 |
| Pnom | 额定功率 | real | MW | 额定有功功率 | 1.5 |
| isEnabled | 启用 | boolean | - | 是否启用 | true |
"""

        params = self.parser.parse_markdown_table(table)
        assert len(params) == 3

        # 检查第一个参数
        assert params[0]['key'] == 'Vpcc'
        assert params[0]['display_name'] == '并网点电压'
        assert params[0]['type'] == 'real'
        assert params[0]['unit'] == 'kV'
        assert params[0]['default'] == 0.69

    def test_parse_with_required(self):
        """测试解析带必需标记的表格"""
        table = """
| 参数名 | 显示名 | 类型 | 必需 | 默认值 |
|--------|--------|------|------|--------|
| required_param | 必需参数 | real | 是 | - |
| optional_param | 可选参数 | real | 否 | 10.0 |
"""

        params = self.parser.parse_markdown_table(table)
        assert len(params) == 2
        assert params[0]['required'] is True
        assert params[1]['required'] is False

    def test_parse_with_choices(self):
        """测试解析带选择项的表格"""
        table = """
| 参数名 | 显示名 | 类型 | 选项 |
|--------|--------|------|------|
| control_mode | 控制模式 | choice | 自动,手动,禁用 |
"""

        params = self.parser.parse_markdown_table(table)
        assert len(params) == 1
        assert params[0]['type'] == 'choice'
        assert params[0]['choices'] == ['自动', '手动', '禁用']

    def test_parse_with_constraints(self):
        """测试解析带约束的表格"""
        table = """
| 参数名 | 显示名 | 类型 | 范围 |
|--------|--------|------|------|
| ratio | 比例 | real | [0, 100] |
| count | 数量 | integer | 0~100 |
"""

        params = self.parser.parse_markdown_table(table)
        assert len(params) == 2
        assert params[0]['constraints']['min'] == 0.0
        assert params[0]['constraints']['max'] == 100.0

    def test_parse_english_headers(self):
        """测试解析英文表头"""
        table = """
| name | display_name | type | unit | default |
|------|--------------|------|------|---------|
| voltage | Voltage | real | kV | 220.0 |
| enabled | Enabled | boolean | - | true |
"""

        params = self.parser.parse_markdown_table(table)
        assert len(params) == 2
        assert params[0]['key'] == 'voltage'
        assert params[0]['display_name'] == 'Voltage'

    def test_parse_type_mapping(self):
        """测试类型映射"""
        table = """
| 参数名 | 显示名 | 类型 |
|--------|--------|------|
| p1 | 参数1 | 实数 |
| p2 | 参数2 | 整数 |
| p3 | 参数3 | 文本 |
| p4 | 参数4 | 布尔 |
"""

        params = self.parser.parse_markdown_table(table)
        assert params[0]['type'] == 'real'
        assert params[1]['type'] == 'integer'
        assert params[2]['type'] == 'text'
        assert params[3]['type'] == 'boolean'

    def test_parse_invalid_table(self):
        """测试解析无效表格"""
        # 不是表格格式
        params = self.parser.parse_markdown_table("不是表格")
        assert len(params) == 0
        assert len(self.parser.errors) > 0

    def test_parse_empty_table(self):
        """测试解析空表格"""
        table = """
| 参数名 | 显示名 | 类型 |
|--------|--------|------|
"""

        params = self.parser.parse_markdown_table(table)
        assert len(params) == 0


class TestComponentDocumentParser:
    """组件文档解析器测试"""

    def setup_method(self):
        self.parser = ComponentDocumentParser()

    def test_parse_simple_document(self):
        """测试解析简单文档"""
        doc = """
# 测试组件

这是一个用于测试的组件。

## 参数

### 基础参数

| 参数名 | 显示名 | 类型 | 默认值 |
|--------|--------|------|--------|
| Vpcc | 并网点电压 | real | 0.69 |
| Pnom | 额定功率 | real | 1.5 |

## 引脚

| 引脚 | 名称 | 类型 | 描述 |
|------|------|------|------|
| 0 | N | 电气 | 中性点 |
| 1 | A | 电气 | A相 |
"""

        result = self.parser.parse(doc, 'model/test/component')
        assert result.success is True
        assert result.metadata is not None
        assert result.metadata.component_id == 'model/test/component'
        assert result.metadata.name == '测试组件'
        assert len(result.metadata.parameter_groups) == 1
        assert len(result.metadata.pins['electrical']) == 2

    def test_parse_without_component_id(self):
        """测试解析没有指定组件ID的文档"""
        doc = """
# WGSource 风场模型

这是一个风场模型组件。
"""

        result = self.parser.parse(doc)
        assert result.success is True
        assert result.metadata.component_id == 'wgsource_风场模型'

    def test_parse_without_param_section(self):
        """测试解析没有参数章节的文档"""
        doc = """
# 测试组件

这是一个测试组件。
"""

        result = self.parser.parse(doc, 'model/test/component')
        assert result.success is True
        assert len(result.warnings) > 0
        assert any('未找到参数' in w for w in result.warnings)

    def test_parse_multiple_parameter_groups(self):
        """测试解析多个参数组"""
        doc = """
# 多组参数组件

## 参数

### 基础参数

| 参数名 | 显示名 | 类型 |
|--------|--------|------|
| base_param | 基础参数 | real |

### 高级参数

| 参数名 | 显示名 | 类型 |
|--------|--------|------|
| advanced_param | 高级参数 | integer |

### 控制参数

| 参数名 | 显示名 | 类型 |
|--------|--------|------|
| ctrl_param | 控制参数 | boolean |
"""

        result = self.parser.parse(doc, 'model/test/multi')
        assert result.success is True
        assert len(result.metadata.parameter_groups) == 3

    def test_parse_complex_wgsource_like_document(self):
        """测试解析类似 WGSource 的复杂文档"""
        doc = """
# 风场等值模型 I：PMSG 网侧变流器模型

风场等值模型，用于模拟风电场的功率输出特性。

## 参数说明

### 基础参数

| 参数名 | 显示名 | 类型 | 单位 | 描述 | 默认值 |
|--------|--------|------|------|------|--------|
| Vpcc | 并网点电压 | real | kV | 风场并网点电压 | 0.69 |
| Pnom | 额定功率 | real | MW | 风场额定装机容量 | 100.0 |
| Fnom | 额定频率 | real | Hz | 系统额定频率 | 50.0 |

### Power Flow Data

| 参数名 | 显示名 | 类型 | 单位 | 描述 | 默认值 |
|--------|--------|------|------|------|--------|
| Vbase | 基准电压 | real | kV | 单台风机基准电压 | 0.69 |
| WindSpeed | 风速 | real | m/s | 轮毂高度处风速 | 12.0 |
| AirDensity | 空气密度 | real | kg/m³ | 空气密度 | 1.225 |

### 风场功率参数

| 参数名 | 显示名 | 类型 | 单位 | 描述 | 默认值 |
|--------|--------|------|------|------|--------|
| MPPTEnable | MPPT控制使能 | boolean | - | 是否启用最大功率跟踪 | true |

## 引脚说明

| 引脚 | 名称 | 类型 | 维度 | 描述 |
|------|------|------|------|------|
| 0 | 电气连接 | 电气 | 3×1 | 风场三相电气连接端口 |
"""

        result = self.parser.parse(doc, 'model/CloudPSS/WGSource')
        assert result.success is True
        assert result.metadata.component_id == 'model/CloudPSS/WGSource'
        assert '风场等值模型' in result.metadata.name
        assert len(result.metadata.parameter_groups) == 3
        assert len(result.metadata.pins['electrical']) == 1

        # 检查参数组
        group_names = [g.name for g in result.metadata.parameter_groups]
        assert '基础参数' in group_names
        assert 'Power Flow Data' in group_names
        assert '风场功率参数' in group_names

    def test_parse_with_yaml_frontmatter(self):
        """测试解析带 YAML frontmatter 的文档"""
        doc = """---
component_id: model/test/frontmatter
version: 1.0.0
category: test
---

# 带 Frontmatter 的组件

这是一个带有 YAML frontmatter 的组件文档。

## 参数

| 参数名 | 显示名 | 类型 |
|--------|--------|------|
| param1 | 参数1 | real |
"""

        result = self.parser.parse(doc)
        assert result.success is True
        assert result.metadata.component_id == 'model/test/frontmatter'

    def test_parse_file_not_found(self):
        """测试解析不存在的文件"""
        result = self.parser.parse_file('/nonexistent/path/file.md')
        assert result.success is False
        assert any('文件不存在' in e for e in result.errors)


class TestBatchMetadataExtractor:
    """批量元数据提取器测试"""

    def setup_method(self):
        self.extractor = BatchMetadataExtractor()

    def test_extract_empty_directory(self):
        """测试提取空目录"""
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            results = self.extractor.extract_from_directory(temp_dir)
            assert len(results) == 0

    def test_extract_single_file(self):
        """测试提取单个文件"""
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建一个文档
            doc_content = """
# 测试组件

## 参数

| 参数名 | 显示名 | 类型 |
|--------|--------|------|
| param1 | 参数1 | real |

## 引脚

| 引脚 | 名称 | 类型 |
|------|------|------|
| 0 | 引脚0 | 电气 |
"""
            filepath = os.path.join(temp_dir, 'test_component.md')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(doc_content)

            results = self.extractor.extract_from_directory(temp_dir)
            assert len(results) == 1
            assert 'test_component.md' in results
            assert results['test_component.md'].success is True

    def test_get_successful_results(self):
        """测试获取成功的结果"""
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建一个有效文档
            with open(os.path.join(temp_dir, 'valid.md'), 'w', encoding='utf-8') as f:
                f.write("""
# 有效组件

## 参数

| 参数名 | 显示名 | 类型 |
|--------|--------|------|
| param1 | 参数1 | real |
""")

            self.extractor.extract_from_directory(temp_dir)
            successful = self.extractor.get_successful_results()
            assert len(successful) == 1

    def test_get_summary(self):
        """测试获取摘要"""
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建一些文档
            for i in range(3):
                with open(os.path.join(temp_dir, f'comp{i}.md'), 'w', encoding='utf-8') as f:
                    f.write(f"""
# 组件{i}

## 参数

| 参数名 | 显示名 | 类型 |
|--------|--------|------|
| param{i} | 参数{i} | real |
""")

            self.extractor.extract_from_directory(temp_dir)
            summary = self.extractor.get_summary()
            assert summary['total'] == 3
            assert summary['successful'] == 3
            assert summary['failed'] == 0
            assert summary['success_rate'] == 1.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
