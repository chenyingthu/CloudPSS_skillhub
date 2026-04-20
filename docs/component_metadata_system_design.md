# CloudPSS 元件库元数据系统 - 详细设计文档

## 版本信息
- 版本: 1.0.0
- 日期: 2026-04-02
- 状态: 详细设计阶段

## 目录
1. [系统概述](#系统概述)
2. [元数据 JSON Schema](#元数据-json-schema)
3. [Document Parser 设计](#document-parser-设计)
4. [Metadata Registry 设计](#metadata-registry-设计)
5. [参数验证引擎设计](#参数验证引擎设计)
6. [数据流图](#数据流图)
7. [测试策略](#测试策略)
8. [实施计划](#实施计划)

---

## 系统概述

### 目标
建立一个自动化的元件库元数据管理系统，实现：
- 从 CloudPSS 文档自动提取元件参数定义
- 集中化管理和查询元件元数据
- 动态验证模型参数的完整性和正确性
- 支持未来新元件的自动扩展

### 架构原则
1. **单一数据源** - 文档作为唯一权威来源
2. **自动生成** - 元数据从文档自动生成，不手动维护
3. **向后兼容** - 现有技能和配置继续工作
4. **可测试性** - 每个组件都有完整测试覆盖
5. **零 Fake Tests** - 集成测试使用真实 API

---

## 元数据 JSON Schema

### 完整 Schema 定义

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "cloudpss-component-metadata",
  "title": "CloudPSS Component Metadata",
  "type": "object",
  "required": ["component_id", "name", "version", "parameters", "pins"],
  "properties": {
    "component_id": {
      "type": "string",
      "description": "元件唯一标识，如 model/CloudPSS/WGSource"
    },
    "name": {
      "type": "string",
      "description": "元件显示名称"
    },
    "description": {
      "type": "string",
      "description": "元件描述"
    },
    "version": {
      "type": "string",
      "description": "元数据版本"
    },
    "category": {
      "type": "string",
      "description": "元件类别",
      "enum": [
        "basic-electrical",
        "basic-control",
        "renewable-energy",
        "dc-modules",
        "protection",
        "measurement"
      ]
    },
    "source": {
      "type": "object",
      "description": "文档来源信息",
      "properties": {
        "doc_path": {"type": "string"},
        "last_updated": {"type": "string", "format": "date-time"},
        "hash": {"type": "string"}
      }
    },
    "parameters": {
      "type": "object",
      "required": ["groups"],
      "properties": {
        "groups": {
          "type": "array",
          "items": {"$ref": "#/definitions/ParameterGroup"}
        }
      }
    },
    "pins": {
      "type": "object",
      "properties": {
        "electrical": {
          "type": "array",
          "items": {"$ref": "#/definitions/PinDefinition"}
        },
        "input": {
          "type": "array",
          "items": {"$ref": "#/definitions/PinDefinition"}
        },
        "output": {
          "type": "array",
          "items": {"$ref": "#/definitions/PinDefinition"}
        }
      }
    },
    "validation_rules": {
      "type": "object",
      "additionalProperties": {"$ref": "#/definitions/ValidationRule"}
    },
    "simulation_support": {
      "type": "object",
      "properties": {
        "powerflow": {"type": "boolean"},
        "emt": {"type": "boolean"},
        "sfemt": {"type": "boolean"}
      }
    }
  },
  "definitions": {
    "ParameterGroup": {
      "type": "object",
      "required": ["group_id", "name"],
      "properties": {
        "group_id": {"type": "string"},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "conditional": {"$ref": "#/definitions/ConditionalRule"},
        "parameters": {
          "type": "array",
          "items": {"$ref": "#/definitions/Parameter"}
        }
      }
    },
    "Parameter": {
      "type": "object",
      "required": ["key", "display_name", "type"],
      "properties": {
        "key": {"type": "string"},
        "display_name": {"type": "string"},
        "type": {
          "type": "string",
          "enum": ["real", "integer", "text", "boolean", "choice", "virtual"]
        },
        "unit": {"type": ["string", "null"]},
        "description": {"type": "string"},
        "required": {"type": "boolean", "default": false},
        "default": {},
        "choices": {
          "type": "array",
          "items": {"type": "string"}
        },
        "constraints": {
          "type": "object",
          "properties": {
            "min": {"type": "number"},
            "max": {"type": "number"},
            "regex": {"type": "string"}
          }
        }
      }
    },
    "PinDefinition": {
      "type": "object",
      "required": ["key", "name", "type"],
      "properties": {
        "key": {"type": "string"},
        "name": {"type": "string"},
        "type": {
          "type": "string",
          "enum": ["electrical", "input", "output"]
        },
        "dimension": {"type": "string"},
        "description": {"type": "string"},
        "required": {"type": "boolean", "default": false},
        "valid_connections": {
          "type": "array",
          "items": {"type": "string"}
        }
      }
    },
    "ConditionalRule": {
      "type": "object",
      "required": ["field", "operator", "value"],
      "properties": {
        "field": {"type": "string"},
        "operator": {
          "type": "string",
          "enum": ["equals", "not_equals", "in", "not_in", "gt", "lt"]
        },
        "value": {},
        "then_group": {"type": "string"},
        "else_group": {"type": "string"}
      }
    },
    "ValidationRule": {
      "type": "object",
      "properties": {
        "type": {
          "type": "string",
          "enum": ["required", "range", "regex", "custom"]
        },
        "message": {"type": "string"},
        "min": {"type": "number"},
        "max": {"type": "number"},
        "pattern": {"type": "string"},
        "custom_function": {"type": "string"}
      }
    }
  }
}
```

### WGSource 元数据示例

```json
{
  "component_id": "model/CloudPSS/WGSource",
  "name": "风场等值模型I：PMSG网侧变流器模型",
  "description": "直驱风机风电场等值模型，支持功率控制、低电压穿越",
  "version": "1.0.0",
  "category": "renewable-energy",
  "source": {
    "doc_path": "docs/documents/software/20-emtlab/110-component-library/20-renewable-energy-modules/10-wgsource",
    "last_updated": "2026-04-02T00:00:00Z",
    "hash": "abc123"
  },
  "parameters": {
    "groups": [
      {
        "group_id": "basic",
        "name": "基础参数",
        "parameters": [
          {
            "key": "Name",
            "display_name": "Name",
            "type": "text",
            "unit": null,
            "description": "Name",
            "required": false,
            "default": ""
          },
          {
            "key": "Vpcc",
            "display_name": "并网点电压",
            "type": "real",
            "unit": "kV",
            "description": "并网点线电压有效值",
            "required": true,
            "constraints": {"min": 0.1, "max": 1000}
          },
          {
            "key": "Init_Phase",
            "display_name": "电压初始相位",
            "type": "real",
            "unit": "Deg",
            "description": "电压初始相位",
            "required": false,
            "default": 0
          },
          {
            "key": "Startup_Time",
            "display_name": "启动时间",
            "type": "real",
            "unit": "s",
            "description": "启动时间",
            "required": false,
            "default": 0.1
          },
          {
            "key": "WT_Num",
            "display_name": "风机台数",
            "type": "real",
            "unit": null,
            "description": "风机台数",
            "required": true,
            "default": 1,
            "constraints": {"min": 1, "max": 10000}
          },
          {
            "key": "Ctrlmode",
            "display_name": "功率控制方式",
            "type": "choice",
            "unit": null,
            "description": "功率控制方式（单机最大1.5MW）",
            "required": false,
            "choices": ["MPPT", "Constant Power"],
            "default": "MPPT"
          },
          {
            "key": "mode",
            "display_name": "控制模式",
            "type": "choice",
            "unit": null,
            "description": "控制模式",
            "required": false,
            "choices": ["Grid Following", "Grid Forming"],
            "default": "Grid Following"
          },
          {
            "key": "Xtrans",
            "display_name": "连接电抗",
            "type": "real",
            "unit": "Ω",
            "description": "连接电抗",
            "required": true,
            "default": 0.1
          },
          {
            "key": "Kp_udc",
            "display_name": "Udc比例控制系数",
            "type": "real",
            "unit": null,
            "description": "直流电压比例控制系数",
            "required": false,
            "default": 1.0
          },
          {
            "key": "Ki_udc",
            "display_name": "Udc积分控制系数",
            "type": "real",
            "unit": "s",
            "description": "直流电压积分控制系数",
            "required": false,
            "default": 0.1
          },
          {
            "key": "LVRT_Startup",
            "display_name": "低穿判断起始时间",
            "type": "real",
            "unit": "s",
            "description": "低穿判断起始时间。禁用低穿时可填99999",
            "required": false,
            "default": 99999
          }
        ]
      },
      {
        "group_id": "power_flow",
        "name": "Power Flow Data",
        "parameters": [
          {
            "key": "BusType",
            "display_name": "Bus Type",
            "type": "choice",
            "unit": null,
            "description": "节点类型",
            "required": true,
            "choices": ["PQ", "PV", "Slack"],
            "default": "PQ"
          },
          {
            "key": "pf_P",
            "display_name": "Injected Active Power",
            "type": "real",
            "unit": "MW",
            "description": "节点注入有功功率",
            "required": true,
            "default": 0
          },
          {
            "key": "pf_Q",
            "display_name": "Injected Reactive Power",
            "type": "real",
            "unit": "MVar",
            "description": "节点注入无功功率",
            "required": false,
            "default": 0
          },
          {
            "key": "pf_V",
            "display_name": "Bus Voltage Magnitude",
            "type": "real",
            "unit": "p.u.",
            "description": "母线电压幅值",
            "required": false,
            "default": 1.0
          },
          {
            "key": "pf_Theta",
            "display_name": "Bus Voltage Angle",
            "type": "real",
            "unit": "Deg",
            "description": "母线电压相位",
            "required": false,
            "default": 0
          },
          {
            "key": "pf_Vmin",
            "display_name": "Lower Voltage Limit",
            "type": "real",
            "unit": "p.u.",
            "description": "母线电压下限",
            "required": false,
            "default": 0.95
          },
          {
            "key": "pf_Vmax",
            "display_name": "Upper Voltage Limit",
            "type": "real",
            "unit": "p.u.",
            "description": "母线电压上限",
            "required": false,
            "default": 1.05
          },
          {
            "key": "pf_Qmin",
            "display_name": "Lower Reactive Power Limit",
            "type": "real",
            "unit": "MVar",
            "description": "无功功率下限",
            "required": false,
            "default": -100
          },
          {
            "key": "pf_Qmax",
            "display_name": "Upper Reactive Power Limit",
            "type": "real",
            "unit": "MVar",
            "description": "无功功率上限",
            "required": false,
            "default": 100
          }
        ]
      },
      {
        "group_id": "wind_farm_power",
        "name": "风场功率参数",
        "parameters": [
          {
            "key": "Pref_WF",
            "display_name": "风场有功功率参考值",
            "type": "real",
            "unit": "MW",
            "description": "风场有功功率参考值",
            "required": false,
            "default": 0
          },
          {
            "key": "Qref_WF",
            "display_name": "风场无功功率参考值",
            "type": "real",
            "unit": "MVar",
            "description": "风场无功功率参考值",
            "required": false,
            "default": 0
          }
        ]
      },
      {
        "group_id": "unit_test",
        "name": "单元测试",
        "parameters": [
          {
            "key": "UnitTest",
            "display_name": "启用单元测试元件？",
            "type": "boolean",
            "unit": null,
            "description": "是否启用单元测试元件？",
            "required": false,
            "default": false
          },
          {
            "key": "FaultSet",
            "display_name": "是否为故障电压源？",
            "type": "choice",
            "unit": null,
            "description": "是否为故障电压源？",
            "required": false,
            "choices": ["No", "Yes"],
            "default": "No"
          },
          {
            "key": "FaultStartTime",
            "display_name": "故障开始时间",
            "type": "real",
            "unit": "s",
            "description": "故障开始时间",
            "required": false,
            "default": 1.0
          },
          {
            "key": "FaultEndTime",
            "display_name": "故障结束时间",
            "type": "real",
            "unit": "s",
            "description": "故障结束时间",
            "required": false,
            "default": 1.5
          },
          {
            "key": "FaultDropRatio",
            "display_name": "故障电压降",
            "type": "real",
            "unit": "p.u.",
            "description": "故障电压降",
            "required": false,
            "default": 0.5
          }
        ]
      },
      {
        "group_id": "recovery",
        "name": "功率恢复参数",
        "parameters": [
          {
            "key": "Krate",
            "display_name": "恢复速率",
            "type": "real",
            "unit": null,
            "description": "恢复速率",
            "required": false,
            "default": 0.1
          }
        ]
      }
    ]
  },
  "pins": {
    "electrical": [
      {
        "key": "0",
        "name": "AC",
        "type": "electrical",
        "dimension": "3×1",
        "description": "交流电气连接",
        "required": true,
        "valid_connections": ["bus", "line", "transformer"]
      }
    ],
    "input": [
      {
        "key": "1",
        "name": "P[MW]",
        "type": "input",
        "dimension": "1×1",
        "description": "单机有功功率控制（MW）",
        "required": false
      },
      {
        "key": "2",
        "name": "Q[MVar]",
        "type": "input",
        "dimension": "1×1",
        "description": "单机无功功率控制（MVar）",
        "required": false
      }
    ],
    "output": [
      {
        "key": "3",
        "name": "Po",
        "type": "output",
        "dimension": "1×1",
        "description": "P Output",
        "required": false
      },
      {
        "key": "4",
        "name": "Qo",
        "type": "output",
        "dimension": "1×1",
        "description": "Q Output",
        "required": false
      },
      {
        "key": "5",
        "name": "LVRT_Flag",
        "type": "output",
        "dimension": "1×1",
        "description": "LVRT_Flag",
        "required": false
      }
    ]
  },
  "validation_rules": {
    "Vpcc": {
      "type": "range",
      "min": 0.1,
      "max": 1000,
      "message": "并网点电压必须在0.1-1000kV之间"
    },
    "WT_Num": {
      "type": "range",
      "min": 1,
      "max": 10000,
      "message": "风机台数必须在1-10000之间"
    },
    "pf_V": {
      "type": "range",
      "min": 0.5,
      "max": 1.5,
      "message": "电压标幺值应在0.5-1.5之间"
    }
  },
  "simulation_support": {
    "powerflow": true,
    "emt": true,
    "sfemt": false
  }
}
```


---

## Document Parser 设计

### 设计目标
- 从 Markdown 表格提取结构化的参数和引脚定义
- 支持 CloudPSS 文档的标准格式
- 处理条件参数和参数分组
- 生成标准化的 JSON 元数据

### 解析策略

```python
# cloudpss_skills/metadata/parser.py

import re
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass

@dataclass
class ParsedTable:
    """解析后的表格数据"""
    headers: List[str]
    rows: List[List[str]]
    table_type: str  # 'parameters' or 'pins'

@dataclass
class ParameterGroup:
    """参数组"""
    group_id: str
    name: str
    description: Optional[str]
    conditional: Optional[Dict]
    parameters: List[Dict]

class ComponentDocumentParser:
    """
    CloudPSS 元件文档解析器
    
    输入: _parameters.md, _pins.md
    输出: ComponentMetadata 对象
    
    支持的功能:
    1. 解析 Markdown 表格
    2. 提取参数组结构
    3. 识别参数类型和单位
    4. 处理条件参数
    5. 生成标准化元数据
    """
    
    # Markdown 表格正则
    TABLE_PATTERN = re.compile(
        r'\|(.+?)\|\n\|[-:\s|]+\|\n((?:\|.+?\|\n?)+)',
        re.MULTILINE
    )
    
    # 参数类型映射
    TYPE_MAPPING = {
        '实数': 'real',
        '整数': 'integer',
        '文本': 'text',
        '布尔': 'boolean',
        '选择': 'choice',
        '虚拟引脚': 'virtual',
    }
    
    # 引脚类型映射
    PIN_TYPE_MAPPING = {
        '电气': 'electrical',
        '输入': 'input',
        '输出': 'output',
    }
    
    def __init__(self, docs_base_path: str):
        self.docs_base_path = Path(docs_base_path)
    
    def parse_component(self, component_relative_path: str) -> Dict[str, Any]:
        """
        解析单个元件的文档
        
        Args:
            component_relative_path: 相对于 docs_base_path 的路径
                例如: "documents/software/20-emtlab/110-component-library/.../10-wgsource"
        
        Returns:
            ComponentMetadata 字典
        """
        component_path = self.docs_base_path / component_relative_path
        
        # 读取 index.md 获取基本信息
        index_file = component_path / "index.md"
        if not index_file.exists():
            raise FileNotFoundError(f"找不到 index.md: {index_file}")
        
        index_content = index_file.read_text(encoding='utf-8')
        metadata = self._extract_frontmatter(index_content)
        
        # 读取 _parameters.md
        params_file = component_path / "_parameters.md"
        if params_file.exists():
            params_content = params_file.read_text(encoding='utf-8')
            metadata['parameters'] = self._parse_parameters(params_content)
        
        # 读取 _pins.md
        pins_file = component_path / "_pins.md"
        if pins_file.exists():
            pins_content = pins_file.read_text(encoding='utf-8')
            metadata['pins'] = self._parse_pins(pins_content)
        
        # 添加来源信息
        metadata['source'] = {
            'doc_path': str(component_relative_path),
            'last_updated': self._get_file_mtime(params_file),
            'hash': self._calculate_file_hash(params_file)
        }
        
        return metadata
    
    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """提取 YAML frontmatter"""
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            import yaml
            frontmatter = yaml.safe_load(match.group(1))
            return {
                'name': frontmatter.get('title', ''),
                'description': frontmatter.get('description', ''),
            }
        return {'name': '', 'description': ''}
    
    def _parse_parameters(self, content: str) -> Dict[str, Any]:
        """
        解析参数文档
        
        策略:
        1. 识别参数组标题 (#### 参数组名称)
        2. 解析每个表格
        3. 转换参数类型和单位
        4. 提取默认值和约束
        """
        groups = []
        
        # 分割参数组
        # 模式: #### 标题 + 可选描述 + 表格
        group_pattern = r'####\s+(.+?)\n\n(.+?)\n\n(\|.+?\|)'
        
        # 找到所有表格
        tables = list(self.TABLE_PATTERN.finditer(content))
        
        current_group = None
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            # 检测参数组标题
            if line.startswith('#### '):
                group_name = line[5:].strip()
                current_group = {
                    'group_id': self._slugify(group_name),
                    'name': group_name,
                    'description': '',
                    'parameters': []
                }
                groups.append(current_group)
            
            # 检测表格开始
            elif line.startswith('|') and current_group:
                # 解析表格
                table_data = self._parse_markdown_table(content, i)
                if table_data:
                    params = self._convert_table_to_params(table_data)
                    current_group['parameters'].extend(params)
        
        return {'groups': groups}
    
    def _parse_markdown_table(self, content: str, start_line: int) -> Optional[ParsedTable]:
        """解析 Markdown 表格"""
        lines = content.split('\n')
        
        # 找到表格范围
        table_lines = []
        for i in range(start_line, len(lines)):
            line = lines[i]
            if line.startswith('|'):
                table_lines.append(line)
            elif table_lines:
                break
        
        if len(table_lines) < 3:
            return None
        
        # 解析表头
        header_line = table_lines[0]
        headers = [h.strip() for h in header_line.split('|')[1:-1]]
        
        # 跳过分隔行
        # 解析数据行
        rows = []
        for line in table_lines[2:]:
            if line.startswith('|'):
                cells = [c.strip() for c in line.split('|')[1:-1]]
                rows.append(cells)
        
        return ParsedTable(
            headers=headers,
            rows=rows,
            table_type='parameters'
        )
    
    def _convert_table_to_params(self, table: ParsedTable) -> List[Dict]:
        """将表格数据转换为参数定义"""
        params = []
        
        # 列索引映射
        col_mapping = {}
        for i, header in enumerate(table.headers):
            header_lower = header.lower()
            if '参数名' in header_lower or 'name' in header_lower:
                col_mapping['display_name'] = i
            elif '键名' in header_lower or 'key' in header_lower:
                col_mapping['key'] = i
            elif '类型' in header_lower or 'type' in header_lower:
                col_mapping['type'] = i
            elif '单位' in header_lower or 'unit' in header_lower:
                col_mapping['unit'] = i
            elif '描述' in header_lower or 'description' in header_lower:
                col_mapping['description'] = i
        
        for row in table.rows:
            param = self._parse_param_row(row, col_mapping)
            if param:
                params.append(param)
        
        return params
    
    def _parse_param_row(self, row: List[str], col_mapping: Dict) -> Optional[Dict]:
        """解析单行参数"""
        if 'key' not in col_mapping:
            return None
        
        key_idx = col_mapping['key']
        if key_idx >= len(row):
            return None
        
        key = row[key_idx].strip().strip('`')
        if not key:
            return None
        
        param = {
            'key': key,
            'display_name': row[col_mapping.get('display_name', key_idx)].strip() if 'display_name' in col_mapping else key,
            'type': 'text',
            'unit': None,
            'description': '',
            'required': False,
        }
        
        # 解析类型和单位
        if 'type' in col_mapping:
            type_cell = row[col_mapping['type']]
            type_info = self._parse_type_and_unit(type_cell)
            param['type'] = type_info['type']
            param['unit'] = type_info['unit']
        
        # 解析描述
        if 'description' in col_mapping:
            param['description'] = row[col_mapping['description']].strip()
        
        # 推断必需性
        if '必需' in param.get('description', '') or 'required' in param.get('description', '').lower():
            param['required'] = True
        
        # 推断默认值
        if '默认' in param.get('description', ''):
            default_match = re.search(r'默认[值为]?[:：]?\s*([\d.]+)', param['description'])
            if default_match:
                param['default'] = float(default_match.group(1))
        
        return param
    
    def _parse_type_and_unit(self, type_cell: str) -> Dict[str, str]:
        """解析类型和单位"""
        type_cell = type_cell.strip()
        
        result = {'type': 'text', 'unit': None}
        
        # 检查类型映射
        for cn_type, en_type in self.TYPE_MAPPING.items():
            if cn_type in type_cell:
                result['type'] = en_type
                break
        
        # 提取单位
        unit_match = re.search(r'\[([^\]]+)\]', type_cell)
        if unit_match:
            result['unit'] = unit_match.group(1)
        
        return result
    
    def _parse_pins(self, content: str) -> Dict[str, List[Dict]]:
        """解析引脚文档"""
        pins = {'electrical': [], 'input': [], 'output': []}
        
        table = self._parse_markdown_table(content, 0)
        if not table:
            return pins
        
        # 列映射
        col_mapping = {}
        for i, header in enumerate(table.headers):
            header_lower = header.lower()
            if '引脚名' in header_lower:
                col_mapping['name'] = i
            elif '键名' in header_lower:
                col_mapping['key'] = i
            elif '类型' in header_lower:
                col_mapping['type'] = i
            elif '维度' in header_lower:
                col_mapping['dimension'] = i
            elif '描述' in header_lower:
                col_mapping['description'] = i
        
        for row in table.rows:
            pin = self._parse_pin_row(row, col_mapping)
            if pin:
                pin_type = pin.get('pin_category', 'electrical')
                if pin_type in pins:
                    pins[pin_type].append(pin)
        
        return pins
    
    def _parse_pin_row(self, row: List[str], col_mapping: Dict) -> Optional[Dict]:
        """解析单行引脚"""
        if 'key' not in col_mapping:
            return None
        
        key_idx = col_mapping['key']
        if key_idx >= len(row):
            return None
        
        key = row[key_idx].strip().strip('`"')
        if not key:
            return None
        
        pin = {
            'key': key,
            'name': row[col_mapping.get('name', key_idx)].strip() if 'name' in col_mapping else key,
            'type': 'electrical',
            'dimension': row[col_mapping.get('dimension', 0)].strip() if 'dimension' in col_mapping else '1×1',
            'description': row[col_mapping.get('description', 0)].strip() if 'description' in col_mapping else '',
            'required': False,
        }
        
        # 解析类型
        if 'type' in col_mapping:
            type_cell = row[col_mapping['type']]
            for cn_type, en_type in self.PIN_TYPE_MAPPING.items():
                if cn_type in type_cell:
                    pin['pin_category'] = en_type
                    pin['type'] = en_type
                    break
        
        # 电气引脚默认必需
        if pin['type'] == 'electrical' and key == '0':
            pin['required'] = True
        
        return pin
    
    def _slugify(self, text: str) -> str:
        """转换为 URL slug"""
        return re.sub(r'[^\w]', '_', text.lower())
    
    def _get_file_mtime(self, file_path: Path) -> str:
        """获取文件修改时间"""
        from datetime import datetime
        if file_path.exists():
            mtime = file_path.stat().st_mtime
            return datetime.fromtimestamp(mtime).isoformat()
        return ''
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """计算文件哈希"""
        import hashlib
        if file_path.exists():
            content = file_path.read_bytes()
            return hashlib.md5(content).hexdigest()[:8]
        return ''


class BatchMetadataExtractor:
    """
    批量元数据提取器
    
    扫描整个文档目录，提取所有元件的元数据
    """
    
    def __init__(self, docs_base_path: str, output_path: str):
        self.docs_base_path = Path(docs_base_path)
        self.output_path = Path(output_path)
        self.parser = ComponentDocumentParser(docs_base_path)
    
    def extract_all(self, component_library_path: str = None) -> Dict[str, Any]:
        """
        提取所有元件的元数据
        
        Args:
            component_library_path: 元件库相对路径，默认为查找所有元件
        
        Returns:
            包含所有元件元数据的字典
        """
        if component_library_path:
            search_path = self.docs_base_path / component_library_path
        else:
            search_path = self.docs_base_path
        
        # 查找所有包含 _parameters.md 的目录
        components = {}
        
        for param_file in search_path.rglob('_parameters.md'):
            component_dir = param_file.parent
            relative_path = component_dir.relative_to(self.docs_base_path)
            
            try:
                metadata = self.parser.parse_component(str(relative_path))
                
                # 生成 component_id
                component_id = self._generate_component_id(relative_path)
                metadata['component_id'] = component_id
                metadata['version'] = '1.0.0'
                
                components[component_id] = metadata
                
            except Exception as e:
                print(f"解析失败 {relative_path}: {e}")
        
        return components
    
    def save_metadata(self, components: Dict[str, Any]):
        """保存元数据到文件"""
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # 保存每个元件的单独文件
        for component_id, metadata in components.items():
            # 清理 component_id 作为文件名
            safe_name = re.sub(r'[^\w]', '_', component_id)
            file_path = self.output_path / f"{safe_name}.json"
            
            import json
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # 保存索引文件
        index = {
            'components': list(components.keys()),
            'total': len(components),
            'generated_at': datetime.now().isoformat()
        }
        
        index_path = self.output_path / '_index.json'
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
    
    def _generate_component_id(self, relative_path: Path) -> str:
        """从路径生成 component_id"""
        # 从路径推断 RID
        # 例如: .../10-wgsource -> model/CloudPSS/WGSource
        
        dir_name = relative_path.name
        
        # 移除数字前缀
        name = re.sub(r'^\d+-', '', dir_name)
        
        # 转换为 PascalCase
        name = ''.join(word.capitalize() for word in name.split('-'))
        name = name.replace('_', '')
        
        return f"model/CloudPSS/{name}"
```


---

## Metadata Registry 设计

### 设计目标
- 高效管理和查询元件元数据
- 支持按类别、类型、功能筛选
- 提供参数验证和自动补全
- 缓存机制提高性能

### 核心类设计

```python
# cloudpss_skills/metadata/registry.py

from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
import json
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)


@dataclass
class Parameter:
    """参数定义"""
    key: str
    display_name: str
    type: str  # 'real', 'integer', 'text', 'boolean', 'choice'
    unit: Optional[str] = None
    description: str = ""
    required: bool = False
    default: Any = None
    choices: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    
    def validate_value(self, value: Any) -> tuple[bool, Optional[str]]:
        """验证参数值"""
        # 类型验证
        if self.type == 'real':
            if not isinstance(value, (int, float)):
                return False, f"参数 {self.key} 必须是实数"
        elif self.type == 'integer':
            if not isinstance(value, int):
                return False, f"参数 {self.key} 必须是整数"
        elif self.type == 'boolean':
            if not isinstance(value, bool):
                return False, f"参数 {self.key} 必须是布尔值"
        elif self.type == 'text':
            if not isinstance(value, str):
                return False, f"参数 {self.key} 必须是文本"
        elif self.type == 'choice':
            if value not in self.choices:
                return False, f"参数 {self.key} 必须是 {self.choices} 之一"
        
        # 范围验证
        if 'min' in self.constraints and value < self.constraints['min']:
            return False, f"参数 {self.key} 必须 >= {self.constraints['min']}"
        if 'max' in self.constraints and value > self.constraints['max']:
            return False, f"参数 {self.key} 必须 <= {self.constraints['max']}"
        
        return True, None


@dataclass
class PinDefinition:
    """引脚定义"""
    key: str
    name: str
    type: str  # 'electrical', 'input', 'output'
    dimension: str = "1×1"
    description: str = ""
    required: bool = False
    valid_connections: List[str] = field(default_factory=list)


@dataclass
class ParameterGroup:
    """参数组"""
    group_id: str
    name: str
    description: str = ""
    conditional: Optional[Dict] = None
    parameters: List[Parameter] = field(default_factory=list)
    
    def get_required_params(self) -> List[Parameter]:
        """获取必需参数"""
        return [p for p in self.parameters if p.required]
    
    def get_param(self, key: str) -> Optional[Parameter]:
        """获取指定参数"""
        for p in self.parameters:
            if p.key == key:
                return p
        return None


@dataclass
class ComponentMetadata:
    """元件元数据"""
    component_id: str
    name: str
    description: str = ""
    version: str = "1.0.0"
    category: str = ""
    source: Dict = field(default_factory=dict)
    parameter_groups: List[ParameterGroup] = field(default_factory=list)
    pins: Dict[str, List[PinDefinition]] = field(default_factory=dict)
    validation_rules: Dict[str, Any] = field(default_factory=dict)
    simulation_support: Dict[str, bool] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ComponentMetadata':
        """从字典创建对象"""
        # 转换参数组
        groups = []
        for group_data in data.get('parameters', {}).get('groups', []):
            params = []
            for param_data in group_data.get('parameters', []):
                params.append(Parameter(
                    key=param_data['key'],
                    display_name=param_data.get('display_name', param_data['key']),
                    type=param_data.get('type', 'text'),
                    unit=param_data.get('unit'),
                    description=param_data.get('description', ''),
                    required=param_data.get('required', False),
                    default=param_data.get('default'),
                    choices=param_data.get('choices', []),
                    constraints=param_data.get('constraints', {})
                ))
            
            groups.append(ParameterGroup(
                group_id=group_data['group_id'],
                name=group_data['name'],
                description=group_data.get('description', ''),
                conditional=group_data.get('conditional'),
                parameters=params
            ))
        
        # 转换引脚
        pins_data = data.get('pins', {})
        pins = {}
        for pin_type in ['electrical', 'input', 'output']:
            pins[pin_type] = []
            for pin_data in pins_data.get(pin_type, []):
                pins[pin_type].append(PinDefinition(
                    key=pin_data['key'],
                    name=pin_data.get('name', pin_data['key']),
                    type=pin_data.get('type', pin_type),
                    dimension=pin_data.get('dimension', '1×1'),
                    description=pin_data.get('description', ''),
                    required=pin_data.get('required', False),
                    valid_connections=pin_data.get('valid_connections', [])
                ))
        
        return cls(
            component_id=data['component_id'],
            name=data['name'],
            description=data.get('description', ''),
            version=data.get('version', '1.0.0'),
            category=data.get('category', ''),
            source=data.get('source', {}),
            parameter_groups=groups,
            pins=pins,
            validation_rules=data.get('validation_rules', {}),
            simulation_support=data.get('simulation_support', {})
        )
    
    def get_all_parameters(self) -> List[Parameter]:
        """获取所有参数"""
        params = []
        for group in self.parameter_groups:
            params.extend(group.parameters)
        return params
    
    def get_parameter(self, key: str) -> Optional[Parameter]:
        """获取指定参数"""
        for group in self.parameter_groups:
            param = group.get_param(key)
            if param:
                return param
        return None
    
    def get_required_parameters(self) -> List[Parameter]:
        """获取所有必需参数"""
        return [p for p in self.get_all_parameters() if p.required]
    
    def get_required_pins(self) -> List[PinDefinition]:
        """获取所有必需引脚"""
        required = []
        for pin_type in ['electrical', 'input', 'output']:
            for pin in self.pins.get(pin_type, []):
                if pin.required:
                    required.append(pin)
        return required
    
    def validate_parameters(self, params: Dict[str, Any]) -> 'ValidationResult':
        """验证参数字典"""
        from cloudpss_skills.core.base import ValidationResult
        
        errors = []
        warnings = []
        
        # 检查必需参数
        all_params = {p.key: p for p in self.get_all_parameters()}
        
        for key, param in all_params.items():
            if param.required and key not in params:
                errors.append(f"缺少必需参数: {param.display_name} ({key})")
        
        # 验证每个参数值
        for key, value in params.items():
            if key not in all_params:
                warnings.append(f"未知参数: {key}")
                continue
            
            param = all_params[key]
            valid, message = param.validate_value(value)
            if not valid:
                errors.append(message)
        
        return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)
    
    def auto_complete(self, user_params: Dict[str, Any]) -> Dict[str, Any]:
        """自动补全参数"""
        complete = {}
        
        for group in self.parameter_groups:
            for param in group.parameters:
                if param.key in user_params:
                    complete[param.key] = user_params[param.key]
                elif param.default is not None:
                    complete[param.key] = param.default
                elif param.required:
                    # 必需参数但没有提供也没有默认值
                    logger.warning(f"必需参数 {param.key} 没有值")
        
        return complete


class ComponentMetadataRegistry:
    """
    元件元数据注册表
    
    功能:
    1. 加载和缓存元数据
    2. 按类别查询
    3. 参数验证
    4. 自动补全
    """
    
    def __init__(self, metadata_path: Optional[str] = None):
        self.metadata_path = Path(metadata_path) if metadata_path else Path(__file__).parent / 'component_metadata'
        self._cache: Dict[str, ComponentMetadata] = {}
        self._index: Dict[str, List[str]] = {}  # 按类别索引
        self._loaded = False
    
    def load_all(self) -> None:
        """加载所有元数据"""
        if self._loaded:
            return
        
        if not self.metadata_path.exists():
            logger.warning(f"元数据目录不存在: {self.metadata_path}")
            return
        
        # 加载索引
        index_file = self.metadata_path / '_index.json'
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
                logger.info(f"从索引加载 {len(index_data.get('components', []))} 个元件")
        
        # 加载每个元件
        for json_file in self.metadata_path.glob('*.json'):
            if json_file.name.startswith('_'):
                continue
            
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                metadata = ComponentMetadata.from_dict(data)
                self._cache[metadata.component_id] = metadata
                
                # 更新索引
                if metadata.category:
                    if metadata.category not in self._index:
                        self._index[metadata.category] = []
                    self._index[metadata.category].append(metadata.component_id)
                
            except Exception as e:
                logger.error(f"加载元数据失败 {json_file}: {e}")
        
        self._loaded = True
        logger.info(f"已加载 {len(self._cache)} 个元件元数据")
    
    @lru_cache(maxsize=128)
    def get_component(self, component_id: str) -> Optional[ComponentMetadata]:
        """获取元件元数据"""
        self.load_all()
        return self._cache.get(component_id)
    
    def list_components(self, category: Optional[str] = None) -> List[str]:
        """列出元件ID"""
        self.load_all()
        
        if category:
            return self._index.get(category, [])
        return list(self._cache.keys())
    
    def search_by_name(self, name_pattern: str) -> List[ComponentMetadata]:
        """按名称搜索"""
        self.load_all()
        
        results = []
        pattern = name_pattern.lower()
        for metadata in self._cache.values():
            if pattern in metadata.name.lower():
                results.append(metadata)
        return results
    
    def get_categories(self) -> List[str]:
        """获取所有类别"""
        self.load_all()
        return list(self._index.keys())
    
    def reload(self) -> None:
        """重新加载元数据"""
        self._cache.clear()
        self._index.clear()
        self._loaded = False
        self.load_all()


# 全局注册表实例
_registry: Optional[ComponentMetadataRegistry] = None


def get_registry(metadata_path: Optional[str] = None) -> ComponentMetadataRegistry:
    """获取全局注册表实例"""
    global _registry
    if _registry is None:
        _registry = ComponentMetadataRegistry(metadata_path)
    return _registry
```

---

## Skill 集成方案

### model_builder 集成

```python
# cloudpss_skills/builtin/model_builder.py (修改部分)

from cloudpss_skills.metadata.registry import get_registry, ComponentMetadata

class ModelBuilderSkill(SkillBase):
    def __init__(self):
        super().__init__()
        self.model = None
        self.metadata_registry = get_registry()
    
    def _add_component(self, config: Dict):
        """添加组件（增强版）"""
        comp_type = config["component_type"]
        label = config["label"]
        user_params = config.get("parameters", {})
        position = config.get("position", {})
        pin_connection = config.get("pin_connection", {})
        
        # 1. 获取元件元数据
        metadata = self.metadata_registry.get_component(comp_type)
        if not metadata:
            logger.warning(f"未找到元件元数据: {comp_type}，使用用户提供的参数")
            complete_params = user_params
        else:
            logger.info(f"使用元数据配置元件: {metadata.name}")
            
            # 2. 自动补全参数
            complete_params = metadata.auto_complete(user_params)
            
            # 3. 验证参数
            validation = metadata.validate_parameters(complete_params)
            if not validation.valid:
                raise ValueError(f"参数验证失败:\n" + "\n".join(f"  - {e}" for e in validation.errors))
            
            if validation.warnings:
                for warning in validation.warnings:
                    logger.warning(f"参数警告: {warning}")
        
        # 4. 处理引脚连接
        pins = {}
        if metadata and pin_connection:
            # 验证引脚有效性
            target_bus = pin_connection.get("target_bus")
            pin_name = pin_connection.get("pin_name", "0")
            
            # 检查引脚是否存在
            all_pins = []
            for pin_type in ['electrical', 'input', 'output']:
                all_pins.extend(metadata.pins.get(pin_type, []))
            
            pin_exists = any(p.key == pin_name for p in all_pins)
            if not pin_exists:
                available = [p.key for p in all_pins]
                raise ValueError(f"引脚 {pin_name} 不存在，可用引脚: {available}")
            
            pins[pin_name] = target_bus
            logger.info(f"  配置引脚 {pin_name} -> 母线 {target_bus}")
        elif pin_connection:
            # 无元数据时直接配置
            pins[pin_connection.get("pin_name", "0")] = pin_connection.get("target_bus")
        
        # 5. 添加组件
        try:
            self.model.addComponent(
                definition=comp_type,
                label=label,
                args=complete_params,
                pins=pins
            )
            self.modifications_applied.append(f"add:{label}")
            if pins:
                self.modifications_applied.append(f"connect:{label}->{target_bus}")
            
            # 记录实际使用的参数
            logger.info(f"  参数: {json.dumps(complete_params, ensure_ascii=False, indent=2)}")
            
        except Exception as e:
            logger.error(f"添加组件失败: {e}")
            raise
```

### model_validator 集成

```python
# cloudpss_skills/builtin/model_validator.py (修改部分)

from cloudpss_skills.metadata.registry import get_registry

class ModelValidatorSkill(SkillBase):
    def __init__(self):
        super().__init__()
        self.metadata_registry = get_registry()
    
    def _validate_component_params(self, comp_id: str, comp: Any) -> Dict:
        """验证元件参数（增强版）"""
        metadata = self.metadata_registry.get_component(
            getattr(comp, 'definition', '')
        )
        
        if not metadata:
            # 未知元件，仅做基本检查
            return {
                "passed": True,
                "warnings": [f"未知元件类型，无法深度验证: {getattr(comp, 'definition', 'N/A')}"],
                "details": {}
            }
        
        args = getattr(comp, 'args', {})
        
        # 使用元数据验证
        validation = metadata.validate_parameters(args)
        
        # 检查是否使用了默认值
        auto_completed = metadata.auto_complete({})
        missing_required = []
        for key in auto_completed:
            if key not in args:
                param = metadata.get_parameter(key)
                if param and param.required:
                    missing_required.append(key)
        
        result = {
            "passed": validation.valid,
            "errors": validation.errors,
            "warnings": validation.warnings,
            "details": {
                "component_name": metadata.name,
                "total_params": len(metadata.get_all_parameters()),
                "provided_params": len(args),
                "auto_completed_params": len(auto_completed) - len(args),
                "missing_required": missing_required
            }
        }
        
        return result
    
    def _validate_component_pins(self, comp_id: str, comp: Any) -> Dict:
        """验证元件引脚（增强版）"""
        metadata = self.metadata_registry.get_component(
            getattr(comp, 'definition', '')
        )
        
        pins = getattr(comp, 'pins', {})
        
        if not metadata:
            # 基本引脚检查
            if not pins:
                return {
                    "passed": True,
                    "warnings": ["元件无引脚信息"],
                    "details": {}
                }
            return {"passed": True, "details": {}}
        
        # 检查必需引脚
        missing_required = []
        for pin in metadata.get_required_pins():
            if pin.key not in pins or not pins.get(pin.key):
                missing_required.append(f"{pin.name} ({pin.key})")
        
        if missing_required:
            return {
                "passed": False,
                "errors": [f"缺少必需引脚: {', '.join(missing_required)}"],
                "details": {"missing_pins": missing_required}
            }
        
        return {
            "passed": True,
            "details": {
                "connected_pins": len([v for v in pins.values() if v]),
                "total_pins": sum(len(pins_list) for pins_list in metadata.pins.values())
            }
        }
```

---

## 数据流图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          元数据生成流程                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐            │
│  │ _parameters │      │   Parser    │      │    JSON     │            │
│  │    .md      │ ───▶ │   Engine    │ ───▶ │  Metadata   │            │
│  └─────────────┘      └─────────────┘      └─────────────┘            │
│         │                   │                   │                       │
│         │                   │                   │                       │
│         ▼                   ▼                   ▼                       │
│  ┌─────────────────────────────────────────────────────┐               │
│  │                  Validation                         │               │
│  │  - 检查参数完整性                                  │               │
│  │  - 验证类型映射                                    │               │
│  │  - 生成默认值                                      │               │
│  └─────────────────────────────────────────────────────┘               │
│                            │                                           │
│                            ▼                                           │
│  ┌─────────────────────────────────────────────────────┐               │
│  │              ComponentMetadata                       │               │
│  │                 Registry                             │               │
│  └─────────────────────────────────────────────────────┘               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                          运行时查询流程                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  User Config                                                            │
│       │                                                                 │
│       ▼                                                                 │
│  ┌─────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────┐   │
│  │ model_  │───▶│   Registry   │───▶│  Metadata   │───▶│ Auto-    │   │
│  │ builder │    │   Lookup     │    │   Object    │    │ Complete │   │
│  └─────────┘    └─────────────┘    └─────────────┘    └──────────┘   │
│       │                                                    │          │
│       │                                                    ▼          │
│       │                                            ┌─────────────┐   │
│       │                                            │   Validate  │   │
│       │                                            └─────────────┘   │
│       │                                                    │          │
│       ▼                                                    ▼          │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │                    CloudPSS Model.addComponent               │     │
│  │                   (with complete params & pins)              │     │
│  └─────────────────────────────────────────────────────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```


---

## 测试策略

### 测试原则

1. **零 Fake Tests** - 所有集成测试使用真实 CloudPSS API
2. **自动化测试** - CI/CD 自动运行所有测试
3. **高覆盖率** - 核心代码覆盖率 > 90%
4. **文档驱动测试** - 测试用例基于设计文档

### 测试金字塔

```
                    ▲
                   /│\     E2E Tests (真实API)
                  / │ \    - model_builder 端到端
                 /  │  \   - model_validator 端到端
                /   │   \  - 完整工作流测试
               ───────────
              /     │     \  Integration Tests
             /      │      \ - Registry 集成
            /       │       \- Parser 集成
           /        │        \
          ─────────────────────
         /           │          \ Unit Tests
        /            │           \- Parser 单元测试
       /             │            - Registry 单元测试
      /              │             - Validation 单元测试
     ───────────────────────────────
```

### 测试分类

#### 1. 单元测试 (tests/unit/metadata/)

**test_parser.py**
```python
"""
Document Parser 单元测试
- 测试表格解析
- 测试参数提取
- 测试引脚提取
- 测试类型映射
"""

import pytest
from cloudpss_skills.metadata.parser import ComponentDocumentParser

class TestParameterParsing:
    """参数解析测试"""
    
    def test_parse_real_parameter(self):
        """测试解析实数参数"""
        content = """
| 参数名 | 键名 | 类型 [单位] | 描述 |
|:------ |:---- |:-----------:|:---- |
| 并网点电压 | `Vpcc` | 实数 [kV] | 并网点电压 |
"""
        parser = ComponentDocumentParser("/tmp")
        table = parser._parse_markdown_table(content, 0)
        
        assert table is not None
        assert len(table.rows) == 1
        assert table.rows[0][1] == "`Vpcc`"
    
    def test_parse_choice_parameter(self):
        """测试解析选择参数"""
        content = """
| 参数名 | 键名 | 类型 | 描述 |
|:------ |:---- |:----:|:---- |
| 控制模式 | `Ctrlmode` | 选择 | 选择模式 |
"""
        parser = ComponentDocumentParser("/tmp")
        table = parser._parse_markdown_table(content, 0)
        
        assert table is not None
        param = parser._convert_table_to_params(table)[0]
        assert param['type'] == 'choice'
    
    def test_parse_with_unit(self):
        """测试解析带单位的参数"""
        type_cell = "实数 [kV]"
        parser = ComponentDocumentParser("/tmp")
        result = parser._parse_type_and_unit(type_cell)
        
        assert result['type'] == 'real'
        assert result['unit'] == 'kV'


class TestPinParsing:
    """引脚解析测试"""
    
    def test_parse_electrical_pin(self):
        """测试解析电气引脚"""
        content = """
| 引脚名 | 键名 | 类型 | 维度 | 描述 |
|:------ |:---- |:----:|:----:|:---- |
| AC | `0` | 电气 | 3×1 | 交流连接 |
"""
        parser = ComponentDocumentParser("/tmp")
        pins = parser._parse_pins(content)
        
        assert len(pins['electrical']) == 1
        assert pins['electrical'][0]['key'] == '0'
    
    def test_parse_input_pin(self):
        """测试解析输入引脚"""
        content = """
| 引脚名 | 键名 | 类型 | 维度 | 描述 |
|:------ |:---- |:----:|:----:|:---- |
| Pref | `Pref` | 输入 | 1×1 | 有功参考 |
"""
        parser = ComponentDocumentParser("/tmp")
        pins = parser._parse_pins(content)
        
        assert len(pins['input']) == 1
        assert pins['input'][0]['type'] == 'input'
```

**test_registry.py**
```python
"""
Metadata Registry 单元测试
- 测试加载和缓存
- 测试查询和筛选
- 测试参数验证
"""

import pytest
import json
import tempfile
from pathlib import Path
from cloudpss_skills.metadata.registry import (
    ComponentMetadataRegistry,
    ComponentMetadata,
    Parameter,
    ParameterGroup
)

class TestRegistryLoading:
    """注册表加载测试"""
    
    def test_load_single_component(self, tmp_path):
        """测试加载单个元件"""
        # 创建测试元数据文件
        metadata = {
            "component_id": "model/CloudPSS/TestComponent",
            "name": "测试元件",
            "version": "1.0.0",
            "parameters": {
                "groups": [
                    {
                        "group_id": "basic",
                        "name": "基础参数",
                        "parameters": [
                            {
                                "key": "Param1",
                                "display_name": "参数1",
                                "type": "real",
                                "unit": "kV",
                                "required": True
                            }
                        ]
                    }
                ]
            },
            "pins": {"electrical": [], "input": [], "output": []}
        }
        
        # 写入文件
        meta_file = tmp_path / "model_CloudPSS_TestComponent.json"
        with open(meta_file, 'w') as f:
            json.dump(metadata, f)
        
        # 创建索引
        index = {"components": ["model/CloudPSS/TestComponent"], "total": 1}
        with open(tmp_path / "_index.json", 'w') as f:
            json.dump(index, f)
        
        # 加载
        registry = ComponentMetadataRegistry(str(tmp_path))
        registry.load_all()
        
        # 验证
        comp = registry.get_component("model/CloudPSS/TestComponent")
        assert comp is not None
        assert comp.name == "测试元件"
    
    def test_cache_mechanism(self, tmp_path):
        """测试缓存机制"""
        registry = ComponentMetadataRegistry(str(tmp_path))
        
        # 第一次加载
        registry.load_all()
        
        # 第二次应该使用缓存
        registry.load_all()  # 不应报错


class TestParameterValidation:
    """参数验证测试"""
    
    def test_validate_real_parameter(self):
        """测试验证实数参数"""
        param = Parameter(
            key="Vpcc",
            display_name="并网点电压",
            type="real",
            unit="kV",
            required=True,
            constraints={"min": 0.1, "max": 1000}
        )
        
        # 有效值
        valid, msg = param.validate_value(0.69)
        assert valid
        assert msg is None
        
        # 低于最小值
        valid, msg = param.validate_value(0.01)
        assert not valid
        assert "min" in msg
        
        # 错误类型
        valid, msg = param.validate_value("invalid")
        assert not valid
        assert "实数" in msg
    
    def test_validate_choice_parameter(self):
        """测试验证选择参数"""
        param = Parameter(
            key="BusType",
            display_name="节点类型",
            type="choice",
            choices=["PQ", "PV", "Slack"],
            required=True
        )
        
        # 有效值
        valid, _ = param.validate_value("PQ")
        assert valid
        
        # 无效值
        valid, msg = param.validate_value("Invalid")
        assert not valid
        assert "PQ" in msg  # 应该包含有效选项
```

#### 2. 集成测试 (tests/integration/metadata/)

**test_parser_integration.py**
```python
"""
Document Parser 集成测试
- 使用真实文档进行测试
- 验证与文档的一致性
"""

import pytest
from pathlib import Path
from cloudpss_skills.metadata.parser import ComponentDocumentParser, BatchMetadataExtractor

DOCS_PATH = Path("../cloudpss_docs/docs")

@pytest.mark.skipif(not DOCS_PATH.exists(), reason="文档目录不存在")
class TestWGSourceParsing:
    """WGSource 文档解析测试"""
    
    def test_parse_wgsource(self):
        """解析 WGSource 文档"""
        parser = ComponentDocumentParser(str(DOCS_PATH))
        
        metadata = parser.parse_component(
            "documents/software/20-emtlab/110-component-library/"
            "20-renewable-energy-modules/10-wgsource"
        )
        
        # 验证基本信息
        assert metadata['name']
        assert metadata['description']
        
        # 验证参数组
        params = metadata['parameters']
        assert len(params['groups']) >= 5  # 至少5个参数组
        
        # 验证关键参数
        param_keys = []
        for group in params['groups']:
            for param in group['parameters']:
                param_keys.append(param['key'])
        
        assert 'Vpcc' in param_keys
        assert 'WT_Num' in param_keys
        assert 'Pref_WF' in param_keys
    
    def test_parse_transmission_line(self):
        """解析 TransmissionLine 文档"""
        parser = ComponentDocumentParser(str(DOCS_PATH))
        
        metadata = parser.parse_component(
            "documents/software/20-emtlab/110-component-library/"
            "10-basic/10-electrical/40-three-phase-ac-components/60-TransmissionLine"
        )
        
        # 验证参数组
        params = metadata['parameters']
        group_ids = [g['group_id'] for g in params['groups']]
        assert 'configuration' in group_ids
        assert 'r_x_b_pu' in group_ids or 'r_x_l_ohm' in group_ids


class TestBatchExtraction:
    """批量提取测试"""
    
    def test_extract_renewable_energy_components(self, tmp_path):
        """提取可再生能源元件"""
        extractor = BatchMetadataExtractor(
            str(DOCS_PATH),
            str(tmp_path)
        )
        
        components = extractor.extract_all(
            "documents/software/20-emtlab/110-component-library/"
            "20-renewable-energy-modules"
        )
        
        # 验证提取到元件
        assert len(components) > 0
        
        # 保存并验证
        extractor.save_metadata(components)
        
        # 检查文件生成
        assert (tmp_path / "_index.json").exists()
```

**test_registry_integration.py**
```python
"""
Metadata Registry 集成测试
- 使用生成的元数据文件
- 验证查询和验证功能
"""

import pytest
import json
import tempfile
from pathlib import Path
from cloudpss_skills.metadata.registry import ComponentMetadataRegistry

class TestRegistryWithRealMetadata:
    """使用真实元数据的注册表测试"""
    
    @pytest.fixture(scope="class")
    def registry_with_wgsource(self, tmp_path_factory):
        """创建包含 WGSource 的注册表"""
        tmp_path = tmp_path_factory.mktemp("metadata")
        
        # 创建 WGSource 元数据
        wgsource = {
            "component_id": "model/CloudPSS/WGSource",
            "name": "风场等值模型I：PMSG网侧变流器模型",
            "version": "1.0.0",
            "category": "renewable-energy",
            "parameters": {
                "groups": [
                    {
                        "group_id": "basic",
                        "name": "基础参数",
                        "parameters": [
                            {
                                "key": "Vpcc",
                                "display_name": "并网点电压",
                                "type": "real",
                                "unit": "kV",
                                "description": "并网点线电压有效值",
                                "required": True,
                                "constraints": {"min": 0.1, "max": 1000}
                            },
                            {
                                "key": "WT_Num",
                                "display_name": "风机台数",
                                "type": "real",
                                "unit": None,
                                "description": "风机台数",
                                "required": True,
                                "default": 1,
                                "constraints": {"min": 1, "max": 10000}
                            }
                        ]
                    }
                ]
            },
            "pins": {
                "electrical": [
                    {
                        "key": "0",
                        "name": "AC",
                        "type": "electrical",
                        "dimension": "3×1",
                        "required": True
                    }
                ],
                "input": [],
                "output": []
            }
        }
        
        # 保存
        with open(tmp_path / "model_CloudPSS_WGSource.json", 'w') as f:
            json.dump(wgsource, f)
        
        with open(tmp_path / "_index.json", 'w') as f:
            json.dump({"components": ["model/CloudPSS/WGSource"], "total": 1}, f)
        
        return ComponentMetadataRegistry(str(tmp_path))
    
    def test_query_wgsource(self, registry_with_wgsource):
        """查询 WGSource"""
        registry = registry_with_wgsource
        
        metadata = registry.get_component("model/CloudPSS/WGSource")
        assert metadata is not None
        assert metadata.name == "风场等值模型I：PMSG网侧变流器模型"
    
    def test_validate_wgsource_params(self, registry_with_wgsource):
        """验证 WGSource 参数"""
        registry = registry_with_wgsource
        
        metadata = registry.get_component("model/CloudPSS/WGSource")
        
        # 完整参数
        result = metadata.validate_parameters({
            "Vpcc": 0.69,
            "WT_Num": 100
        })
        assert result.valid
        
        # 缺少必需参数
        result = metadata.validate_parameters({"Vpcc": 0.69})
        assert not result.valid
        assert any("WT_Num" in e for e in result.errors)
    
    def test_auto_complete_wgsource(self, registry_with_wgsource):
        """测试自动补全"""
        registry = registry_with_wgsource
        
        metadata = registry.get_component("model/CloudPSS/WGSource")
        
        # 用户提供部分参数
        params = metadata.auto_complete({"Vpcc": 0.69})
        
        # WT_Num 应该被自动填充
        assert "Vpcc" in params
        assert "WT_Num" in params
        assert params["WT_Num"] == 1  # 默认值
```

#### 3. 端到端测试 (tests/e2e/)

**test_model_builder_e2e.py**
```python
"""
model_builder 端到端测试
- 使用真实 CloudPSS API
- 验证完整工作流
"""

import pytest
from cloudpss_skills.builtin.model_builder import ModelBuilderSkill
from cloudpss import setToken

# 读取 token
import os
token_path = os.path.join(os.path.dirname(__file__), '../../../.cloudpss_token')
if os.path.exists(token_path):
    with open(token_path) as f:
        TOKEN = f.read().strip()
else:
    TOKEN = None

@pytest.mark.skipif(not TOKEN, reason="未找到 CloudPSS Token")
class TestModelBuilderWithMetadata:
    """使用元数据的 model_builder 测试"""
    
    @pytest.fixture(autouse=True)
    def setup_token(self):
        setToken(TOKEN)
    
    def test_add_wgsource_with_auto_complete(self):
        """测试添加 WGSource 自动补全参数"""
        skill = ModelBuilderSkill()
        
        config = {
            'base_model': {'rid': 'model/holdme/IEEE39'},
            'modifications': [
                {
                    'action': 'add_component',
                    'component_type': 'model/CloudPSS/WGSource',
                    'label': 'TestWind',
                    'parameters': {
                        'Vpcc': 0.69,  # 只提供必需参数
                        'WT_Num': 50
                    },
                    'pin_connection': {'target_bus': 'bus39'}
                }
            ],
            'output': {
                'save': True,
                'branch': 'test_metadata_autocomplete',
                'name': 'TestMetadata'
            }
        }
        
        result = skill.run(config)
        assert result.status.name == 'SUCCESS'
        
        # 验证生成的模型
        from cloudpss import Model
        models = result.data.get('generated_models', [])
        assert len(models) == 1
        
        new_rid = models[0]['rid']
        model = Model.fetch(new_rid)
        components = model.getAllComponents()
        
        # 找到 WGSource
        wind_gen = None
        for comp_id, comp in components.items():
            if 'WGSource' in getattr(comp, 'definition', ''):
                wind_gen = comp
                break
        
        assert wind_gen is not None
        
        # 验证参数被自动补全
        args = getattr(wind_gen, 'args', {})
        assert 'Vpcc' in args
        assert 'WT_Num' in args
        # 默认值被填充
        assert 'Startup_Time' in args or 'Init_Phase' in args
    
    def test_add_wgsource_validation_error(self):
        """测试参数验证失败"""
        skill = ModelBuilderSkill()
        
        config = {
            'base_model': {'rid': 'model/holdme/IEEE39'},
            'modifications': [
                {
                    'action': 'add_component',
                    'component_type': 'model/CloudPSS/WGSource',
                    'label': 'TestWind',
                    'parameters': {
                        # 缺少必需参数 Vpcc
                        'WT_Num': 50
                    }
                }
            ],
            'output': {'save': False}
        }
        
        result = skill.run(config)
        assert result.status.name == 'FAILED'
        assert '参数' in result.error or 'Vpcc' in result.error


class TestModelValidatorWithMetadata:
    """使用元数据的 model_validator 测试"""
    
    def test_validate_wgsource_params(self):
        """验证 WGSource 参数完整性"""
        from cloudpss_skills.builtin.model_validator import ModelValidatorSkill
        
        skill = ModelValidatorSkill()
        
        # 使用之前创建的测试模型
        config = {
            'models': [
                {'rid': 'model/holdme/test_ieee39_wind'}
            ],
            'validation': {'phases': ['topology']}
        }
        
        result = skill.run(config)
        
        # 应该通过验证
        assert result.status.name == 'SUCCESS'
        
        reports = result.data.get('reports', [])
        if reports:
            # 检查是否有 WGSource 的参数验证
            phases = reports[0].get('phases', {})
            topology = phases.get('topology', {})
            # 应该没有参数相关的错误
            assert 'errors' not in topology or len(topology['errors']) == 0
```

### CI/CD 集成

**.github/workflows/metadata-tests.yml**
```yaml
name: Component Metadata Tests

on:
  push:
    paths:
      - 'cloudpss_skills/metadata/**'
      - 'cloudpss_skills/builtin/model_builder.py'
      - 'cloudpss_skills/builtin/model_validator.py'
      - 'tests/**'
  pull_request:
    paths:
      - 'cloudpss_skills/metadata/**'

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      
      - name: Run unit tests
        run: |
          pytest tests/unit/metadata -v --cov=cloudpss_skills.metadata --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      
      - name: Run integration tests
        run: |
          pytest tests/integration/metadata -v --run-integration
        env:
          CLOUDPSS_TOKEN: ${{ secrets.CLOUDPSS_TOKEN }}

  e2e-tests:
    runs-on: ubuntu-latest
    needs: integration-tests
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      
      - name: Run E2E tests
        run: |
          pytest tests/e2e -v --run-integration -m "e2e"
        env:
          CLOUDPSS_TOKEN: ${{ secrets.CLOUDPSS_TOKEN }}
```

---

## 实施计划

### Phase 1: 核心基础设施 (Week 1)

**目标**: 建立元数据提取和注册表基础

| 任务 | 描述 | 负责人 | 交付物 |
|------|------|--------|--------|
| 1.1 | 实现 Markdown 表格解析器 | @agent | parser.py |
| 1.2 | 实现元数据结构定义 | @agent | models.py |
| 1.3 | 实现元数据注册表 | @agent | registry.py |
| 1.4 | 单元测试 (>90% 覆盖率) | @agent | test_*.py |

**验收标准**:
- [ ] 可以解析 WGSource 和 TransmissionLine 文档
- [ ] 单元测试通过率 100%
- [ ] 代码覆盖率 > 90%

### Phase 2: Skill 集成 (Week 2)

**目标**: 集成到 model_builder 和 model_validator

| 任务 | 描述 | 负责人 | 交付物 |
|------|------|--------|--------|
| 2.1 | 更新 model_builder 使用注册表 | @agent | model_builder.py |
| 2.2 | 更新 model_validator 使用注册表 | @agent | model_validator.py |
| 2.3 | 实现参数自动补全 | @agent | registry.py |
| 2.4 | 集成测试 | @agent | test_*_integration.py |

**验收标准**:
- [ ] model_builder 可以自动补全 WGSource 参数
- [ ] model_validator 可以检测参数缺失
- [ ] 集成测试通过率 100%

### Phase 3: 文档和自动化 (Week 3)

**目标**: 自动化元数据生成和 CI/CD

| 任务 | 描述 | 负责人 | 交付物 |
|------|------|--------|--------|
| 3.1 | 实现批量元数据提取工具 | @agent | extract_metadata.py |
| 3.2 | 生成初始元数据文件 | @agent | component_metadata/*.json |
| 3.3 | 配置 CI/CD 自动化测试 | @agent | .github/workflows/*.yml |
| 3.4 | 端到端测试 | @agent | tests/e2e/*.py |

**验收标准**:
- [ ] 可以批量提取所有元件元数据
- [ ] CI/CD 自动运行测试
- [ ] E2E 测试通过率 100%

### Phase 4: 验证和优化 (Week 4)

**目标**: 完整验证和性能优化

| 任务 | 描述 | 负责人 | 交付物 |
|------|------|--------|--------|
| 4.1 | 使用真实模型验证 | @agent | validation_report.md |
| 4.2 | 性能优化 (缓存、懒加载) | @agent | registry.py |
| 4.3 | 文档更新 | @agent | README.md, API.md |
| 4.4 | 最终验收测试 | @agent | acceptance_tests.py |

**验收标准**:
- [ ] 使用 IEEE39 模型验证通过
- [ ] 加载时间 < 1s
- [ ] 所有测试通过率 100%

---

## 文档清单

1. **设计文档**
   - [x] component_metadata_system_design.md
   - [ ] API 设计文档 (api.md)
   - [ ] 架构决策记录 (adr/*.md)

2. **用户文档**
   - [ ] 使用指南 (docs/metadata_usage.md)
   - [ ] model_builder 配置示例
   - [ ] model_validator 配置示例

3. **开发文档**
   - [ ] 贡献指南 (CONTRIBUTING.md)
   - [ ] 测试指南 (TESTING.md)
   - [ ] 代码规范 (STYLE.md)

4. **API 文档**
   - [ ] Python API 文档 (docstrings)
   - [ ] JSON Schema 文档
   - [ ] 配置参考 (config_reference.md)
