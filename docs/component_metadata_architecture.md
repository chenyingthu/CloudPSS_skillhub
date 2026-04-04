# CloudPSS 元件库元数据架构设计

## 1. 问题分析

### 当前问题
- model_builder 参数硬编码，无法动态获取元件完整参数
- model_validator 无法验证参数完整性和正确性
- 新元件添加时需要重复开发
- 参数名、键名、类型、单位信息分散在文档中

### 核心需求
1. **动态参数发现** - 自动从文档提取元件参数定义
2. **参数验证** - 验证参数完整性、类型、范围
3. **引脚验证** - 验证引脚连接正确性
4. **可扩展性** - 新元件自动支持

## 2. 架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    CloudPSS Component Metadata System            │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Document   │  │   Metadata   │  │    Skill     │          │
│  │   Parser     │→ │   Registry   │→ │   Integration│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                 │                 │                   │
│         ▼                 ▼                 ▼                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Markdown    │  │  JSON DB     │  │ model_builder│          │
│  │  _parameters │  │  _pins.json  │  │ model_validat│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 元数据结构

```json
{
  "component_id": "model/CloudPSS/WGSource",
  "name": "风场等值模型I：PMSG网侧变流器模型",
  "description": "直驱风机风电场等值模型",
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
            "required": true,
            "default": null
          },
          {
            "key": "WT_Num",
            "display_name": "风机台数",
            "type": "real",
            "unit": null,
            "description": "风机台数",
            "required": true,
            "default": 1
          }
        ]
      },
      {
        "group_id": "power_flow",
        "name": "潮流数据",
        "conditional": {
          "field": "BusType",
          "values": ["PQ", "PV"]
        },
        "parameters": [
          {
            "key": "pf_P",
            "display_name": "注入有功功率",
            "type": "real",
            "unit": "MW",
            "description": "节点注入有功功率",
            "required": true,
            "default": 0
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
        "dimension": "3x1",
        "description": "交流电气连接",
        "required": true
      }
    ],
    "input": [
      {
        "key": "Pref",
        "name": "有功功率参考值",
        "type": "input",
        "dimension": "1x1",
        "description": "有功功率参考值输入",
        "required": false
      }
    ]
  },
  
  "validation_rules": {
    "Vpcc": {
      "min": 0.1,
      "max": 1000,
      "message": "并网点电压必须在0.1-1000kV之间"
    },
    "WT_Num": {
      "min": 1,
      "max": 10000,
      "message": "风机台数必须在1-10000之间"
    }
  }
}
```

## 3. 组件设计

### 3.1 Document Parser

**功能**: 从 Markdown 文档提取参数定义

```python
class ComponentDocumentParser:
    """
    解析 CloudPSS 元件文档
    输入: _parameters.md, _pins.md
    输出: ComponentMetadata 对象
    """
    
    def parse_parameters(self, content: str) -> List[ParameterGroup]:
        """解析参数表格"""
        # 提取表格结构
        # 转换为参数对象
        pass
    
    def parse_pins(self, content: str) -> List[PinDefinition]:
        """解析引脚表格"""
        pass
    
    def extract_metadata(self, component_path: str) -> ComponentMetadata:
        """提取完整元数据"""
        pass
```

### 3.2 Metadata Registry

**功能**: 管理和查询元件元数据

```python
class ComponentMetadataRegistry:
    """
    元件元数据注册表
    支持按类型、类别查询
    """
    
    def register(self, metadata: ComponentMetadata):
        """注册元件元数据"""
        pass
    
    def get_component(self, rid: str) -> ComponentMetadata:
        """获取元件元数据"""
        pass
    
    def list_components(self, category: str = None) -> List[ComponentMetadata]:
        """列出元件"""
        pass
    
    def get_required_parameters(self, rid: str) -> List[Parameter]:
        """获取必需参数"""
        pass
    
    def validate_parameters(self, rid: str, params: dict) -> ValidationResult:
        """验证参数"""
        pass
```

### 3.3 Skill Integration

#### model_builder 集成

```python
class ModelBuilderSkill:
    def __init__(self):
        self.metadata_registry = ComponentMetadataRegistry()
    
    def _add_component(self, config: dict):
        # 获取元件元数据
        metadata = self.metadata_registry.get_component(config['component_type'])
        
        # 自动补全默认参数
        complete_params = self._auto_complete_params(
            metadata, 
            config.get('parameters', {})
        )
        
        # 验证参数完整性
        validation = metadata.validate_parameters(complete_params)
        if not validation.valid:
            raise ValueError(f"参数不完整: {validation.errors}")
        
        # 添加组件
        self.model.addComponent(
            definition=config['component_type'],
            label=config['label'],
            args=complete_params,
            pins=config.get('pins', {})
        )
    
    def _auto_complete_params(self, metadata: ComponentMetadata, 
                               user_params: dict) -> dict:
        """自动补全参数"""
        complete = {}
        for group in metadata.parameters.groups:
            for param in group.parameters:
                if param.key in user_params:
                    complete[param.key] = user_params[param.key]
                elif param.default is not None:
                    complete[param.key] = param.default
                elif param.required:
                    raise ValueError(f"缺少必需参数: {param.display_name} ({param.key})")
        return complete
```

#### model_validator 集成

```python
class ModelValidatorSkill:
    def __init__(self):
        self.metadata_registry = ComponentMetadataRegistry()
    
    def _validate_component_params(self, component: Component) -> ValidationResult:
        """验证元件参数"""
        metadata = self.metadata_registry.get_component(
            component.definition
        )
        
        if not metadata:
            return ValidationResult.warning(f"未知元件类型: {component.definition}")
        
        args = getattr(component, 'args', {})
        return metadata.validate_parameters(args)
    
    def _validate_component_pins(self, component: Component) -> ValidationResult:
        """验证元件引脚"""
        metadata = self.metadata_registry.get_component(
            component.definition
        )
        
        pins = getattr(component, 'pins', {})
        
        # 检查必需引脚
        missing = []
        for pin in metadata.pins.electrical:
            if pin.required and pin.key not in pins:
                missing.append(pin.name)
        
        if missing:
            return ValidationResult.error(
                f"缺少必需引脚: {', '.join(missing)}"
            )
        
        return ValidationResult.valid()
```

## 4. 实施步骤

### Phase 1: 元数据提取器
1. 实现 Markdown 表格解析器
2. 提取参数和引脚定义
3. 生成 JSON 元数据文件

### Phase 2: 元数据注册表
1. 设计元数据存储格式
2. 实现注册表 API
3. 实现查询和验证接口

### Phase 3: Skill 集成
1. 更新 model_builder 使用元数据
2. 更新 model_validator 使用元数据
3. 添加自动补全和验证

### Phase 4: 自动化流程
1. 文档变更自动重新生成元数据
2. CI/CD 集成
3. 版本管理

## 5. 技术细节

### 5.1 参数类型映射

| CloudPSS 类型 | JSON 类型 | Python 类型 | 验证规则 |
|--------------|-----------|-------------|----------|
| 实数         | number    | float       | min/max  |
| 整数         | integer   | int         | min/max  |
| 文本         | string    | str         | regex    |
| 布尔         | boolean   | bool        | -        |
| 选择         | enum      | str         | values   |

### 5.2 条件参数

```json
{
  "conditional": {
    "field": "ParamFormat",
    "operator": "equals",
    "value": "PerUnit",
    "then": "use_group_r_x_b_pu",
    "else": "use_group_r_x_l_ohm"
  }
}
```

### 5.3 引脚类型

```json
{
  "pin_types": {
    "electrical": {
      "description": "电气连接",
      "must_connect_to": ["bus", "line"]
    },
    "input": {
      "description": "控制输入",
      "must_connect_to": ["signal", "control"]
    },
    "output": {
      "description": "信号输出",
      "can_connect_to": ["scope", "meter"]
    }
  }
}
```

## 6. 使用示例

### 6.1 生成元数据

```bash
python -m cloudpss_skills.tools.extract_metadata \
  --docs-path ../cloudpss_docs \
  --output ./component_metadata
```

### 6.2 查询元件参数

```python
from cloudpss_skills.metadata import ComponentMetadataRegistry

registry = ComponentMetadataRegistry()
metadata = registry.get_component("model/CloudPSS/WGSource")

# 获取必需参数
required = metadata.get_required_parameters()
print(f"WGSource 必需参数: {[p.key for p in required]}")

# 验证参数
result = metadata.validate_parameters({
    "Vpcc": 0.69,
    "WT_Num": 100,
    "Pref_WF": 0.8
})
```

### 6.3 model_builder 配置

```yaml
skill: model_builder
base_model:
  rid: model/holdme/IEEE39

modifications:
  - action: add_component
    component_type: model/CloudPSS/WGSource
    label: Wind_Bus39
    # 自动补全会填充默认值
    parameters:
      Vpcc: 0.69          # 显式指定
      WT_Num: 100         # 显式指定
      Pref_WF: 0.8        # 显式指定
    pin_connection:
      0: bus39
```

## 7. 优势

1. **自动化** - 从文档自动生成，无需手动维护
2. **一致性** - 确保文档、代码、验证逻辑一致
3. **可扩展** - 新元件自动支持
4. **健壮性** - 自动验证参数完整性和正确性
5. **可维护性** - 集中管理元件定义

