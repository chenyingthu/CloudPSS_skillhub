# CloudPSS 元件元数据系统

## 概述

CloudPSS 元件元数据系统是一个完整的组件参数管理和验证框架，用于解决电力系统仿真中元件参数不完整、引脚连接错误等建模问题。

## 核心功能

- **参数自动补全**：根据元件元数据自动填充缺失参数
- **参数验证**：验证参数类型、取值范围和必需参数
- **引脚验证**：验证电气连接完整性和引脚类型匹配
- **元数据注册表**：集中管理所有元件的元数据信息
- **文档解析**：从 CloudPSS 文档自动提取元件参数信息

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    元数据系统架构                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   数据模型   │  │   注册表     │  │   解析器     │      │
│  │  (models)    │  │  (registry)  │  │  (parser)    │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │              │
│         └─────────────────┼─────────────────┘              │
│                           │                                │
│                    ┌──────┴───────┐                       │
│                    │  集成层      │                       │
│                    │(integration) │                       │
│                    └──────┬───────┘                       │
│                           │                                │
│         ┌─────────────────┼─────────────────┐              │
│         │                 │                 │              │
│  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐     │
│  │ model_builder│  │model_validator│  │    CLI       │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 快速开始

### 1. 初始化元数据集成

```python
from cloudpss_skills.metadata import get_metadata_integration

# 初始化元数据集成
mi = get_metadata_integration()
mi.initialize('examples/metadata')

# 列出可用组件
components = mi.list_available_components()
print(f"可用组件: {components}")
```

### 2. 参数自动补全

```python
# 用户提供部分参数
user_params = {
    'Vpcc': 0.69,    # 并网点电压
    'Pnom': 100.0,   # 额定功率
}

# 自动补全缺失参数
completed = mi.auto_complete_parameters('model/CloudPSS/WGSource', user_params)

print(f"补全后参数数量: {len(completed)}")
# 输出: 补全后参数数量: 15
```

### 3. 参数验证

```python
# 验证参数完整性
result = mi.validate_parameters('model/CloudPSS/WGSource', completed)

if result.valid:
    print("✅ 参数验证通过")
else:
    print(f"❌ 参数验证失败: {result.errors}")
```

### 4. 引脚验证

```python
# 验证引脚连接
connections = {'0': 'Bus10'}  # 引脚0连接到Bus10
result = mi.validate_pin_connection('model/CloudPSS/WGSource', connections)

if result.valid:
    print("✅ 引脚连接验证通过")
else:
    print(f"❌ 引脚连接验证失败: {result.errors}")
```

## 元数据文件格式

### 完整示例 (WGSource)

```json
{
  "component_id": "model/CloudPSS/WGSource",
  "name": "风场等值模型I：PMSG网侧变流器模型",
  "description": "基于永磁同步发电机(PMSG)和网侧变流器的风电场等值模型",
  "version": "1.0.0",
  "category": "renewable",
  "source": {
    "documentation_url": "https://kb.cloudpss.net/...",
    "version": "2024.12"
  },
  "parameters": {
    "groups": [
      {
        "group_id": "basic",
        "name": "基础电气参数",
        "description": "风机基本电气额定参数",
        "parameters": [
          {
            "key": "Vbase",
            "display_name": "基准电压",
            "type": "real",
            "unit": "kV",
            "description": "风机额定电压（线电压）",
            "required": true,
            "default": 0.69,
            "constraints": {"min": 0.1, "max": 1000.0}
          }
          // ... 更多参数
        ]
      }
    ]
  },
  "pins": {
    "electrical": [
      {
        "key": "0",
        "name": "电网连接",
        "type": "electrical",
        "dimension": "3×1",
        "description": "风机并网点，三相电气端口",
        "required": true
      }
    ],
    "control": []
  },
  "validation_rules": {
    "require_at_least_one_pin": true
  },
  "simulation_support": {
    "powerflow": true,
    "emt": true,
    "phasor": false
  }
}
```

### 参数类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `real` | 实数 | `{"type": "real", "default": 50.0}` |
| `integer` | 整数 | `{"type": "integer", "default": 10}` |
| `boolean` | 布尔值 | `{"type": "boolean", "default": true}` |
| `string` | 字符串 | `{"type": "string", "default": "normal"}` |
| `choice` | 枚举选项 | `{"type": "choice", "choices": ["Y", "Yn", "D"]}` |

## CLI 工具

### 列出可用组件

```bash
python -m cloudpss_skills.metadata list
```

### 查看组件详情

```bash
python -m cloudpss_skills.metadata show model/CloudPSS/WGSource
```

### 验证元数据文件

```bash
python -m cloudpss_skills.metadata validate examples/metadata/wgsource.json
```

### 批量提取元数据

```bash
python -m cloudpss_skills.metadata batch \
    --input-dir docs/components/ \
    --output-dir examples/metadata/
```

## 与 model_builder 集成

`model_builder` 技能已集成元数据系统，自动进行参数补全和验证：

```yaml
skill: model_builder
base_model:
  rid: model/holdme/IEEE39
modifications:
  - action: add_component
    component_type: model/CloudPSS/WGSource
    label: WindFarm_Bus10
    parameters:
      Vpcc: 0.69    # 只需提供关键参数
      Pnom: 50.0    # 其他参数自动补全
    pin_connection:
      target_bus: Bus10
output:
  save: true
  branch: my_wind_farm_model
```

## 与 model_validator 集成

`model_validator` 技能使用元数据进行深度验证：

```yaml
skill: model_validator
models:
  - rid: model/holdme/my_wind_farm_model
    name: IEEE39 with Wind Farm
validation:
  phases: [topology, powerflow]
  check_metadata: true  # 启用元数据验证
output:
  format: console
```

## 性能指标

- **元数据加载时间**: < 0.1s (7个组件)
- **参数补全时间**: < 1ms (单个组件)
- **参数验证时间**: < 1ms (单个组件)
- **引脚验证时间**: < 0.1ms (单个组件)

## 测试覆盖

- **单元测试**: 55个测试用例，覆盖所有核心模块
- **集成测试**: 12个测试用例，验证组件交互
- **E2E测试**: 6个测试用例，验证完整工作流
- **真实API测试**: 使用 CloudPSS 平台验证

运行测试：

```bash
# 单元测试
pytest tests/unit/metadata/ -v

# 集成测试
pytest tests/integration/metadata/ -v --run-integration

# E2E测试
pytest tests/e2e/test_metadata_workflow.py -v --run-integration

# 真实模型验证
python examples/metadata/real_model_validation.py --auto
```

## 可用组件

当前支持的组件类型：

| 组件ID | 名称 | 类别 | 参数数量 | 引脚数量 |
|--------|------|------|----------|----------|
| model/CloudPSS/WGSource | 风场等值模型I | renewable | 15 | 6 |
| model/CloudPSS/PVStation | 光伏电站 | renewable | 12 | 2 |
| model/CloudPSS/_newTransformer_3p | 三相变压器 | transformer | 10 | 2 |
| model/CloudPSS/_newBus_3p | 三相母线 | bus | 4 | 1 |
| model/CloudPSS/_newLoad_3p | 三相负荷 | load | 9 | 1 |
| model/CloudPSS/_newGenerator | 同步发电机 | generator | 28 | 6 |
| model/CloudPSS/_newTLine_3p | 三相传输线 | transmission | 8 | 2 |

## 扩展指南

### 添加新组件

1. 创建元数据 JSON 文件：`examples/metadata/my_component.json`
2. 定义参数组和引脚
3. 添加到索引：`examples/metadata/_index.json`
4. 运行验证：`python -m cloudpss_skills.metadata validate my_component.json`

### 从文档提取

```python
from cloudpss_skills.metadata.parser import ComponentDocumentParser

parser = ComponentDocumentParser()
metadata = parser.parse_file('docs/my_component.md')
parser.save_metadata(metadata, 'examples/metadata/my_component.json')
```

## CI/CD 集成

GitHub Actions 工作流自动运行：

```yaml
name: Metadata System CI/CD
on:
  push:
    paths:
      - 'cloudpss_skills/metadata/**'
      - 'examples/metadata/**'

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest tests/unit/metadata/ -v --cov

  metadata-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python -m cloudpss_skills.metadata.cli validate examples/metadata/
```

## 项目结构

```
cloudpss_skills/metadata/
├── __init__.py          # 模块入口，导出公共API
├── models.py            # 数据模型 (Parameter, ComponentMetadata)
├── registry.py          # 元数据注册表
├── parser.py            # 文档解析器
├── integration.py       # 技能集成层
└── cli.py               # 命令行工具

examples/metadata/
├── _index.json          # 组件索引
├── wgsource.json        # WGSource 元数据
├── pv_station.json      # 光伏电站元数据
├── transformer_3p.json  # 三相变压器元数据
├── bus_3p.json          # 三相母线元数据
├── load_3p.json         # 三相负荷元数据
├── generator.json       # 同步发电机元数据
└── transmission_line.json # 传输线元数据

tests/
├── unit/metadata/       # 单元测试
├── integration/metadata/ # 集成测试
└── e2e/test_metadata_workflow.py # E2E测试
```

## 许可证

MIT License - 详见项目根目录 LICENSE 文件
