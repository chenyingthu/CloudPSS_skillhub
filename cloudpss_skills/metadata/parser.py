"""
组件文档解析器

从 CloudPSS 文档中提取组件参数和引脚定义
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass

from .models import Parameter, PinDefinition, ParameterGroup, ComponentMetadata

logger = logging.getLogger(__name__)


@dataclass
class ParseResult:
    """解析结果"""
    success: bool
    metadata: Optional[ComponentMetadata] = None
    errors: List[str] = None
    warnings: List[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []


class ParameterTableParser:
    """
    参数表格解析器

    解析 Markdown 表格格式的参数定义
    """

    # 参数类型映射
    TYPE_MAPPING = {
        # 中文类型映射
        '实数': 'real',
        '整数': 'integer',
        '文本': 'text',
        '布尔': 'boolean',
        '选择': 'choice',
        '多选': 'multi_choice',
        # 英文类型映射
        'real': 'real',
        'integer': 'integer',
        'int': 'integer',
        'float': 'real',
        'double': 'real',
        'number': 'real',
        'text': 'text',
        'string': 'text',
        'bool': 'boolean',
        'boolean': 'boolean',
        'choice': 'choice',
        'select': 'choice',
        'enum': 'choice',
    }

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def parse_markdown_table(self, table_content: str) -> List[Dict[str, Any]]:
        """
        解析 Markdown 表格

        Args:
            table_content: Markdown 表格文本

        Returns:
            参数定义字典列表
        """
        self.errors = []
        self.warnings = []

        lines = table_content.strip().split('\n')
        if len(lines) < 2:
            self.errors.append("表格至少需要表头和一行数据")
            return []

        # 解析表头
        header_line = lines[0]
        if not header_line.startswith('|'):
            self.errors.append("表格必须以 | 开头")
            return []

        headers = [h.strip().lower() for h in header_line.split('|')[1:-1]]

        # 检查分隔符行（第二行应该是 |---|---| 这种格式）
        if len(lines) > 1 and re.match(r'^[\|\-\s:]+$', lines[1]):
            data_start = 2
        else:
            data_start = 1
            self.warnings.append("表格缺少标准分隔符行")

        # 解析数据行
        params = []
        for i, line in enumerate(lines[data_start:], start=data_start):
            if not line.strip() or not line.startswith('|'):
                continue

            cells = [c.strip() for c in line.split('|')[1:-1]]
            if len(cells) != len(headers):
                self.warnings.append(f"第 {i+1} 行列数与表头不匹配")
                continue

            param = self._parse_row(dict(zip(headers, cells)))
            if param:
                params.append(param)

        return params

    def _parse_row(self, row: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """
        解析单行数据

        Args:
            row: 表头到单元格值的映射

        Returns:
            参数定义字典，解析失败返回 None
        """
        result = {}

        # 参数键名
        if '参数名' in row:
            result['key'] = row['参数名']
        elif 'name' in row:
            result['key'] = row['name']
        elif 'key' in row:
            result['key'] = row['key']
        else:
            return None

        # 显示名称（中文）
        if '显示名' in row:
            result['display_name'] = row['显示名']
        elif 'display_name' in row:
            result['display_name'] = row['display_name']
        else:
            result['display_name'] = result['key']

        # 参数类型
        param_type = 'text'  # 默认类型
        if '类型' in row:
            type_str = row['类型'].lower()
            param_type = self.TYPE_MAPPING.get(type_str, 'text')
        elif 'type' in row:
            type_str = row['type'].lower()
            param_type = self.TYPE_MAPPING.get(type_str, 'text')
        result['type'] = param_type

        # 单位
        if '单位' in row and row['单位']:
            result['unit'] = row['单位']
        elif 'unit' in row and row['unit']:
            result['unit'] = row['unit']

        # 描述
        if '描述' in row:
            result['description'] = row['描述']
        elif 'description' in row:
            result['description'] = row['description']
        else:
            result['description'] = ''

        # 是否必需
        result['required'] = False
        if '必需' in row:
            result['required'] = row['必需'].lower() in ['是', 'yes', 'true', 'y']
        elif 'required' in row:
            result['required'] = row['required'].lower() in ['是', 'yes', 'true', 'y']

        # 默认值
        if '默认值' in row and row['默认值']:
            result['default'] = self._parse_default_value(row['默认值'], param_type)
        elif 'default' in row and row['default']:
            result['default'] = self._parse_default_value(row['default'], param_type)

        # 选择项（仅用于 choice 类型）
        if param_type == 'choice':
            if '选项' in row and row['选项']:
                result['choices'] = self._parse_choices(row['选项'])
            elif 'choices' in row and row['choices']:
                result['choices'] = self._parse_choices(row['choices'])
            else:
                result['choices'] = []

        # 约束条件
        constraints = {}
        if '范围' in row and row['范围']:
            range_constraints = self._parse_range(row['范围'])
            constraints.update(range_constraints)
        if '最小值' in row and row['最小值']:
            constraints['min'] = float(row['最小值'])
        if '最大值' in row and row['最大值']:
            constraints['max'] = float(row['最大值'])
        if constraints:
            result['constraints'] = constraints

        return result

    def _parse_default_value(self, value: str, param_type: str) -> Any:
        """解析默认值"""
        if not value or value == '-':
            return None

        if param_type == 'boolean':
            return value.lower() in ['true', '是', 'yes', '1']
        elif param_type == 'integer':
            try:
                return int(value)
            except ValueError:
                return None
        elif param_type == 'real':
            try:
                return float(value)
            except ValueError:
                return None
        elif param_type == 'choice':
            return value
        else:
            return value

    def _parse_choices(self, choices_str: str) -> List[str]:
        """解析选择项"""
        if not choices_str:
            return []
        # 支持逗号、竖线或分号分隔
        choices = re.split(r'[,;|]', choices_str)
        return [c.strip() for c in choices if c.strip()]

    def _parse_range(self, range_str: str) -> Dict[str, float]:
        """解析范围字符串"""
        constraints = {}
        # 匹配 [min, max] 或 (min, max) 或 min~max 格式
        patterns = [
            r'\[\s*([\d.]+)\s*,\s*([\d.]+)\s*\]',
            r'\(\s*([\d.]+)\s*,\s*([\d.]+)\s*\)',
            r'([\d.]+)\s*~\s*([\d.]+)',
            r'([\d.]+)\s*-\s*([\d.]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, range_str)
            if match:
                try:
                    constraints['min'] = float(match.group(1))
                    constraints['max'] = float(match.group(2))
                    return constraints
                except ValueError:
                    continue

        return constraints


class ComponentDocumentParser:
    """
    组件文档解析器

    从完整的 Markdown 文档中提取组件元数据
    """

    def __init__(self):
        self.table_parser = ParameterTableParser()
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def parse(self, content: str, component_id: Optional[str] = None) -> ParseResult:
        """
        解析组件文档

        Args:
            content: Markdown 文档内容
            component_id: 可选的组件ID（如果文档中没有明确指定）

        Returns:
            解析结果
        """
        self.errors = []
        self.warnings = []

        # 提取元信息
        metadata = self._extract_metadata(content)
        if component_id:
            metadata['component_id'] = component_id

        # 提取参数组
        parameter_groups = self._extract_parameter_groups(content)

        # 提取引脚定义
        pins = self._extract_pins(content)

        # 如果没有找到组件ID，尝试从标题推断
        if 'component_id' not in metadata:
            title = self._extract_title(content)
            if title:
                metadata['component_id'] = self._title_to_component_id(title)
            else:
                self.errors.append("无法确定组件ID")
                return ParseResult(success=False, errors=self.errors, warnings=self.warnings)

        # 如果没有找到名称，使用组件ID的最后部分
        if 'name' not in metadata:
            metadata['name'] = metadata['component_id'].split('/')[-1]

        # 创建组件元数据对象
        try:
            component = ComponentMetadata(
                component_id=metadata['component_id'],
                name=metadata.get('name', ''),
                description=metadata.get('description', ''),
                category=metadata.get('category', ''),
                parameter_groups=parameter_groups,
                pins=pins
            )

            return ParseResult(
                success=True,
                metadata=component,
                errors=self.errors,
                warnings=self.warnings
            )

        except Exception as e:
            self.errors.append(f"创建元数据对象失败: {e}")
            return ParseResult(success=False, errors=self.errors, warnings=self.warnings)

    def parse_file(self, filepath: Union[str, Path]) -> ParseResult:
        """
        从文件解析组件文档

        Args:
            filepath: Markdown 文件路径

        Returns:
            解析结果
        """
        filepath = Path(filepath)

        if not filepath.exists():
            return ParseResult(
                success=False,
                errors=[f"文件不存在: {filepath}"]
            )

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # 从文件名推断组件ID
            component_id = filepath.stem

            return self.parse(content, component_id)

        except Exception as e:
            return ParseResult(
                success=False,
                errors=[f"读取文件失败: {e}"]
            )

    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """提取文档元信息"""
        metadata = {}

        # 尝试提取 YAML frontmatter
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if frontmatter_match:
            # 简单解析 YAML frontmatter
            yaml_content = frontmatter_match.group(1)
            for line in yaml_content.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()

        # 从标题提取名称
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            metadata['name'] = title_match.group(1).strip()

        # 提取描述（第一个段落）
        desc_match = re.search(r'(?:^#\s+.+\n+)([^#\n].+?)(?=\n{2,}|#{1,6}\s)', content, re.DOTALL)
        if desc_match:
            metadata['description'] = desc_match.group(1).strip()

        return metadata

    def _extract_title(self, content: str) -> Optional[str]:
        """提取文档标题"""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        return match.group(1).strip() if match else None

    def _title_to_component_id(self, title: str) -> str:
        """将标题转换为组件ID"""
        # 移除特殊字符，转换为小写
        component_id = re.sub(r'[^\w\s-]', '', title)
        component_id = re.sub(r'\s+', '_', component_id.strip())
        return component_id.lower()

    def _extract_parameter_groups(self, content: str) -> List[ParameterGroup]:
        """提取参数组"""
        groups = []

        # 查找参数组章节 - 支持多种格式
        # 模式1: ## 参数 / ## 参数说明 / ## Parameters (后面跟着 ### 或直接表格)
        param_section_patterns = [
            # 匹配 ## 参数... 直到下一个 ## 或文档结束
            r'#{1,2}\s*(?:参数|参数说明|Parameters|Parameter List).*?\n(.*?)(?=\n#{1,2}\s|\Z)',
            # 匹配带空格的变体
            r'#{1,2}\s*参数.*?\n([\s\S]*?)(?=\n#{1,2}\s|\Z)',
        ]

        param_content = None
        for pattern in param_section_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                param_content = match.group(1)
                break

        if not param_content:
            # 尝试直接查找包含参数表格的部分
            # 查找任何包含参数表格的 ### 或 #### 标题
            group_pattern = r'#{2,4}\s*(.+?)\n.*?\|[^\n]*参数名[^\n]*\|.*?(?=\n#{2,4}\s|\Z)'
            if re.search(group_pattern, content, re.DOTALL | re.IGNORECASE):
                # 文档中有参数组，但没有明确的"参数"章节标题
                param_content = content
            else:
                self.warnings.append("未找到参数说明章节")
                return groups

        # 查找子章节（参数组）- ### 或 #### 标题
        group_pattern = r'#{2,4}\s*(.+?)\n([\s\S]*?)(?=\n#{2,4}\s|\Z)'
        group_matches = list(re.finditer(group_pattern, param_content, re.MULTILINE))

        # 过滤出包含表格的组
        valid_groups = []
        for match in group_matches:
            group_content = match.group(2)
            # 检查是否包含参数表格
            if '|' in group_content and '参数' in group_content:
                valid_groups.append(match)

        if not valid_groups:
            # 没有找到子章节，将整个参数部分作为一个组
            params = self._extract_params_from_content(param_content)
            if params:
                groups.append(ParameterGroup(
                    group_id='default',
                    name='默认参数组',
                    description='',
                    parameters=params
                ))
        else:
            for match in valid_groups:
                group_name = match.group(1).strip()
                group_content = match.group(2)

                # 从组名提取ID
                group_id = re.sub(r'\s+', '_', group_name.lower())
                group_id = re.sub(r'[^\w_]', '', group_id)

                params = self._extract_params_from_content(group_content)
                if params:
                    groups.append(ParameterGroup(
                        group_id=group_id,
                        name=group_name,
                        description='',
                        parameters=params
                    ))

        return groups

    def _extract_params_from_content(self, content: str) -> List[Parameter]:
        """从内容中提取参数"""
        params = []

        # 查找表格
        table_pattern = r'(\|[^\n]+\|\n\|[-:\s|]+\|\n(?:\|[^\n]+\|\n?)+)'
        tables = re.finditer(table_pattern, content)

        for table_match in tables:
            table_content = table_match.group(1)
            parsed_params = self.table_parser.parse_markdown_table(table_content)

            for param_dict in parsed_params:
                try:
                    param = Parameter(
                        key=param_dict['key'],
                        display_name=param_dict.get('display_name', param_dict['key']),
                        type=param_dict.get('type', 'text'),
                        unit=param_dict.get('unit'),
                        description=param_dict.get('description', ''),
                        required=param_dict.get('required', False),
                        default=param_dict.get('default'),
                        choices=param_dict.get('choices', []),
                        constraints=param_dict.get('constraints', {})
                    )
                    params.append(param)
                except Exception as e:
                    self.warnings.append(f"创建参数失败 {param_dict.get('key', '?')}: {e}")

        # 合并表格解析的错误和警告
        self.errors.extend(self.table_parser.errors)
        self.warnings.extend(self.table_parser.warnings)

        return params

    def _extract_pins(self, content: str) -> Dict[str, List[PinDefinition]]:
        """提取引脚定义"""
        pins = {'electrical': [], 'input': [], 'output': []}

        # 查找引脚章节
        pin_section_match = re.search(
            r'#{1,2}\s*(?:引脚|引脚说明|Pins|Pin Definition).*?\n(.*?)(?=#{1,2}\s|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )

        if not pin_section_match:
            self.warnings.append("未找到引脚说明章节")
            return pins

        pin_content = pin_section_match.group(1)

        # 解析引脚表格
        table_pattern = r'(\|[^\n]+\|\n\|[-:\s|]+\|\n(?:\|[^\n]+\|\n?)+)'
        tables = re.finditer(table_pattern, pin_content)

        for table_match in tables:
            table_content = table_match.group(1)
            pin_list = self._parse_pin_table(table_content)

            # 根据名称或类型分类
            for pin in pin_list:
                pin_type = pin.get('type', 'electrical')
                if pin_type in pins:
                    pins[pin_type].append(pin['definition'])

        return pins

    def _parse_pin_table(self, table_content: str) -> List[Dict]:
        """解析引脚表格"""
        pins = []

        lines = table_content.strip().split('\n')
        if len(lines) < 2:
            return pins

        # 解析表头
        headers = [h.strip().lower() for h in lines[0].split('|')[1:-1]]

        # 跳过分隔符行
        data_start = 2 if len(lines) > 1 and re.match(r'^[\|\-\s:]+$', lines[1]) else 1

        for line in lines[data_start:]:
            if not line.strip() or not line.startswith('|'):
                continue

            cells = [c.strip() for c in line.split('|')[1:-1]]
            if len(cells) != len(headers):
                continue

            row = dict(zip(headers, cells))

            # 提取引脚信息
            pin_key = row.get('引脚', row.get('pin', row.get('key', '')))
            if not pin_key:
                continue

            pin_name = row.get('名称', row.get('name', pin_key))
            pin_type = row.get('类型', row.get('type', 'electrical')).lower()

            # 确定引脚类型
            if '电气' in pin_type or 'electrical' in pin_type:
                category = 'electrical'
            elif '输入' in pin_type or 'input' in pin_type:
                category = 'input'
            elif '输出' in pin_type or 'output' in pin_type:
                category = 'output'
            else:
                category = 'electrical'  # 默认为电气引脚

            # 提取维度
            dimension = row.get('维度', row.get('dimension', '1×1'))

            # 提取描述
            description = row.get('描述', row.get('description', ''))

            pin_def = PinDefinition(
                key=pin_key,
                name=pin_name,
                type=category,
                dimension=dimension,
                description=description
            )

            pins.append({
                'type': category,
                'definition': pin_def
            })

        return pins


class BatchMetadataExtractor:
    """
    批量元数据提取器

    从多个文档中提取组件元数据
    """

    def __init__(self):
        self.parser = ComponentDocumentParser()
        self.results: Dict[str, ParseResult] = {}

    def extract_from_directory(
        self,
        directory: Union[str, Path],
        pattern: str = '*.md'
    ) -> Dict[str, ParseResult]:
        """
        从目录批量提取

        Args:
            directory: 文档目录
            pattern: 文件匹配模式

        Returns:
            文件名到解析结果的映射
        """
        directory = Path(directory)
        self.results = {}

        if not directory.exists():
            logger.error(f"目录不存在: {directory}")
            return self.results

        for filepath in directory.glob(pattern):
            logger.info(f"正在解析: {filepath}")
            result = self.parser.parse_file(filepath)
            self.results[filepath.name] = result

            if result.success:
                logger.info(f"成功解析: {filepath.name}")
            else:
                logger.warning(f"解析失败: {filepath.name} - {result.errors}")

        return self.results

    def get_successful_results(self) -> Dict[str, ComponentMetadata]:
        """获取所有成功的解析结果"""
        return {
            name: result.metadata
            for name, result in self.results.items()
            if result.success and result.metadata
        }

    def get_failed_results(self) -> Dict[str, List[str]]:
        """获取所有失败的解析结果"""
        return {
            name: result.errors
            for name, result in self.results.items()
            if not result.success
        }

    def get_summary(self) -> Dict[str, Any]:
        """获取提取摘要"""
        total = len(self.results)
        successful = sum(1 for r in self.results.values() if r.success)
        failed = total - successful

        return {
            'total': total,
            'successful': successful,
            'failed': failed,
            'success_rate': successful / total if total > 0 else 0,
            'failed_files': list(self.get_failed_results().keys())
        }
