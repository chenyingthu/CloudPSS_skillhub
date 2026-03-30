# 模型参数提取技能 (Model Parameter Extractor)

## 设计背景

### 研究对象
模型参数提取技能用于从CloudPSS电力系统模型中提取元件参数，支持按类型批量提取、拓扑分析和参数导出。这是模型文档化、参数校核和数据驱动分析的基础工具。

### 实际需求
在电力系统建模和分析中，经常需要：
1. **模型文档化**：生成模型参数清单和报告
2. **参数校核**：验证模型参数的正确性和一致性
3. **模型版本对比**：对比不同版本模型的参数差异
4. **数据驱动分析**：提取参数用于外部分析和优化
5. **拓扑分析**：了解模型结构和连接关系

### 期望的输入和输出

**输入**：
- 模型配置（RID和来源）
- 元件类型选择（母线、线路、发电机、负荷等）
- 提取选项（是否包含拓扑、是否过滤空值）
- 输出配置（格式、路径、分组方式）

**输出**：
- JSON格式的完整参数报告
- CSV格式的参数表格（按类型分组或统一导出）
- 拓扑连接信息
- 元件类型统计

### 计算结果的用途和价值
模型参数提取结果可用于：
- 模型参数文档生成
- 参数统计和校核
- 模型版本管理
- 数据驱动的系统分析
- 模型拓扑可视化

## 功能特性

- **按类型提取**：支持母线、线路、发电机、负荷、并联补偿等元件类型
- **拓扑分析**：可选提取模型拓扑连接关系
- **参数过滤**：可过滤空值参数，只导出有效参数
- **多格式导出**：支持JSON和CSV格式
- **分组导出**：可按元件类型分组导出CSV
- **完整报告**：生成包含统计信息的完整参数报告

## 快速开始

### CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init model_parameter_extractor --output extract_params.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config extract_params.yaml
```

### Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("model_parameter_extractor")

# 配置
config = {
    "skill": "model_parameter_extractor",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "extraction": {
        "component_types": [          # 要提取的元件类型
            "bus_3p",
            "line_3p",
            "generator",
            "load",
            "transformer_3p"
        ],
        "include_topology": True,     # 提取拓扑连接
        "include_all_args": False,    # 包含所有参数
        "filter_empty": True          # 过滤空值
    },
    "output": {
        "format": "both",             # json | csv | both
        "path": "./results/",
        "prefix": "model_params",
        "group_by_type": True         # 按类型分组导出CSV
    }
}

# 运行
result = skill.run(config)
print(f"状态: {result.status}")
print(f"提取元件数: {result.data.get('total_components')}")
```

### YAML配置示例

```yaml
skill: model_parameter_extractor
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

extraction:
  component_types:
    - bus_3p
    - line_3p
    - generator
    - load
    - transformer_3p
    - shunt
  include_topology: true
  include_all_args: false
  filter_empty: true

output:
  format: both
  path: ./results/
  prefix: ieee39_params
  group_by_type: true
```

## 配置Schema

### 完整配置结构

```yaml
skill: model_parameter_extractor      # 必需: 技能名称
auth:                              # 认证配置
  token: string                    # 直接提供token（不推荐）
  token_file: string               # token文件路径（默认: .cloudpss_token）

model:                             # 模型配置
  rid: string                      # 模型RID（必需）
  source: enum                     # cloud | local（默认: cloud）

extraction:                        # 提取配置
  component_types: array           # 要提取的元件类型列表
  include_topology: boolean        # 是否提取拓扑（默认: true）
  include_all_args: boolean        # 是否包含所有参数（默认: false）
  filter_empty: boolean            # 是否过滤空值（默认: true）

output:                            # 输出配置
  format: enum                     # json | csv | both（默认: both）
  path: string                     # 输出目录（默认: ./results/）
  prefix: string                   # 文件名前缀（默认: model_params）
  group_by_type: boolean           # CSV按类型分组（默认: true）
```

### 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"model_parameter_extractor" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `extraction.component_types` | array | 否 | 全部类型 | 要提取的元件类型列表 |
| `extraction.include_topology` | boolean | 否 | true | 是否提取拓扑连接关系 |
| `extraction.include_all_args` | boolean | 否 | false | 是否包含空值参数 |
| `extraction.filter_empty` | boolean | 否 | true | 是否过滤空值参数 |
| `output.format` | enum | 否 | both | 输出格式：json/csv/both |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | model_params | 文件名前缀 |
| `output.group_by_type` | boolean | 否 | true | CSV是否按类型分组 |

### 支持的元件类型

| 类型标识 | 描述 | CloudPSS定义RID |
|----------|------|-----------------|
| `bus_3p` | 三相母线 | model/CloudPSS/_newBus_3p |
| `line_3p` | 三相线路 | model/CloudPSS/TransmissionLine |
| `transformer_3p` | 三相变压器 | model/CloudPSS/_newTransformer_3p |
| `generator` | 发电机 | model/CloudPSS/_newGenerator |
| `load` | 负荷 | model/CloudPSS/_newLoad_3p |
| `shunt` | 并联补偿 | model/CloudPSS/_newShuntLC_3p |
| `ac_source` | 交流电源 | model/CloudPSS/_newACVoltageSource_3p |
| `fault` | 故障 | model/CloudPSS/_newFault_3p |

## Agent使用指南

### 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("model_parameter_extractor")

# 配置
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "extraction": {
        "component_types": ["bus_3p", "line_3p", "generator"],
        "include_topology": True
    }
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status.value == "SUCCESS":
        print(f"参数提取完成: {result.data['total_components']} 个元件")
    else:
        print(f"参数提取失败: {result.error}")
```

### 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data

    # 访问汇总统计
    print(f"模型名称: {data['model_name']}")
    print(f"总元件数: {data['total_components']}")
    print(f"连接数: {data['connections_count']}")

    # 各类型元件数量
    for comp_type, count in data.get('type_counts', {}).items():
        print(f"  {comp_type}: {count} 个")

    # 访问输出文件
    for artifact in result.artifacts:
        print(f"输出文件: {artifact.path} ({artifact.type})")
        print(f"  描述: {artifact.description}")

# 查看日志
for log in result.logs:
    print(f"[{log.level}] {log.message}")
```

### 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    error_msg = result.error

    # 常见错误处理
    if "Token文件不存在" in error_msg:
        print("错误: 请创建.cloudpss_token文件")
    elif "模型不存在" in error_msg:
        print("错误: 请检查模型RID是否正确")
    elif "无效的元件类型" in error_msg:
        print("错误: 请检查component_types设置")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### JSON报告格式

```json
{
  "summary": {
    "model_rid": "model/holdme/IEEE39",
    "model_name": "IEEE39",
    "total_components": 100,
    "component_types": ["bus_3p", "line_3p", "generator", "load"],
    "type_summaries": {
      "bus_3p": {
        "count": 39,
        "common_parameters": ["Vn", "f", "VoltageLevel"]
      },
      "line_3p": {
        "count": 46,
        "common_parameters": ["Length", "R1", "X1", "B1"]
      }
    },
    "connections_count": 184
  },
  "components": [
    {
      "key": "Bus_1",
      "type": "bus_3p",
      "label": "Bus 1",
      "args": {
        "Vn": 345.0,
        "f": 50.0,
        "VoltageLevel": 345.0
      },
      "pins": {
        "pin_1": "pin_12345"
      }
    }
  ],
  "connections": [
    {
      "source_component": "Bus_1",
      "source_pin": "pin_1",
      "pin_id": "pin_12345"
    }
  ]
}
```

### CSV导出格式（分组模式）

**bus_3p.csv**:
```csv
component_key,label,Vn,f,VoltageLevel
Bus_1,Bus 1,345.0,50.0,345.0
Bus_2,Bus 2,345.0,50.0,345.0
...
```

**line_3p.csv**:
```csv
component_key,label,Length,R1,X1,B1
Line_1,Line 1,100.0,0.01,0.1,0.001
Line_2,Line 2,150.0,0.015,0.15,0.0015
...
```

### CSV导出格式（统一模式）

**model_params_all.csv**:
```csv
component_type,component_key,label,parameter,value
bus_3p,Bus_1,Bus 1,Vn,345.0
bus_3p,Bus_1,Bus 1,f,50.0
line_3p,Line_1,Line 1,Length,100.0
...
```

### SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "model_parameter_extractor" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典，包含元件统计 |
| `artifacts` | list | 输出文件列表（JSON、CSV） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |

## 设计原理

### 工作流程

```
1. 配置加载与验证
   └── 验证model.rid非空
   └── 验证component_types有效

2. 模型加载
   └── 从云端或本地加载模型

3. 拓扑提取（可选）
   └── 调用fetchTopology获取连接关系

4. 按类型提取元件
   └── 遍历指定的component_types
   └── 调用getComponentsByRid获取元件
   └── 提取每个元件的参数和引脚
   └── 过滤空值（如启用filter_empty）

5. 连接关系提取（可选）
   └── 从拓扑数据解析连接关系

6. 报告生成
   └── 统计各类型元件数量
   └── 生成完整参数报告

7. 结果导出
   └── 导出JSON报告
   └── 按类型或统一导出CSV
```

## 与其他技能的关联

```
model_parameter_extractor (模型参数提取)
    ↓ (获取模型参数)
参数分析和校核
    ↓ (生成修改建议)
param_scan (参数扫描) / orthogonal_sensitivity (正交敏感性)
    ↓ (批量仿真验证)
result_compare (结果对比)
```

**依赖关系**：
- **输入依赖**：无（可独立使用）
- **输出被依赖**：
  - `param_scan`: 基于提取的参数设计扫描方案
  - `orthogonal_sensitivity`: 基于提取的参数进行敏感性分析
  - `config_batch_runner`: 结合参数进行批量配置运行

**典型工作流**：
1. 使用 `model_parameter_extractor` 提取模型参数
2. 基于参数特征设计分析方案
3. 使用 `param_scan` 或 `orthogonal_sensitivity` 进行参数分析

## 性能特点

- **执行方式**：本地处理，无需仿真计算
- **网络开销**：仅需加载模型和拓扑
- **内存占用**：与模型规模成正比
- **处理速度**：典型模型（IEEE39）< 5秒
- **适用规模**：适合各种规模的电力系统模型

## 常见问题

### 问题1: 参数提取不完整

**原因**：
- 元件类型未包含在component_types中
- filter_empty过滤了有效空值

**解决**：
```yaml
extraction:
  component_types:          # 包含所有需要的类型
    - bus_3p
    - line_3p
    - generator
    - load
    - transformer_3p
    - shunt
  filter_empty: false       # 保留空值参数
```

### 问题2: 拓扑提取失败

**原因**：
- 模型拓扑复杂
- 网络连接问题

**解决**：
```yaml
extraction:
  include_topology: false   # 禁用拓扑提取，只提取参数
```

### 问题3: CSV文件过多

**原因**：
- group_by_type为true时每个类型一个文件
- 模型包含大量元件类型

**解决**：
```yaml
output:
  group_by_type: false      # 统一导出到一个CSV文件
```

## 完整示例

### 场景描述
某电力系统分析部门需要提取IEEE39模型的所有参数，用于生成模型文档和后续的参数敏感性分析。

### 配置文件

```yaml
skill: model_parameter_extractor
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

extraction:
  component_types:
    - bus_3p
    - line_3p
    - generator
    - load
    - transformer_3p
    - shunt
  include_topology: true
  include_all_args: false
  filter_empty: true

output:
  format: both
  path: ./results/
  prefix: ieee39_documentation
  group_by_type: true
```

### 执行命令

```bash
# 创建输出目录
mkdir -p ./results

# 执行参数提取
python -m cloudpss_skills run --config extract_params.yaml
```

### 预期输出

```
[INFO] 模型参数提取开始
[INFO] 加载模型: model/holdme/IEEE39
[INFO] 模型名称: IEEE39
[INFO] 提取模型拓扑...
  -> 拓扑组件数: 146
[INFO] 提取元件参数...
  -> 提取 bus_3p (model/CloudPSS/_newBus_3p)...
     找到 39 个bus_3p
  -> 提取 line_3p (model/CloudPSS/TransmissionLine)...
     找到 46 个line_3p
  -> 提取 generator (model/CloudPSS/_newGenerator)...
     找到 10 个generator
  -> 提取 load (model/CloudPSS/_newLoad_3p)...
     找到 21 个load
  -> 提取 transformer_3p (model/CloudPSS/_newTransformer_3p)...
     找到 12 个transformer_3p
  -> 提取 shunt (model/CloudPSS/_newShuntLC_3p)...
     找到 2 个shunt
[INFO] 提取连接关系...
[INFO] 生成参数报告...
  -> JSON报告: ./results/ieee39_documentation.json
  -> bus_3p CSV: ./results/ieee39_documentation_bus_3p.csv
  -> line_3p CSV: ./results/ieee39_documentation_line_3p.csv
  -> generator CSV: ./results/ieee39_documentation_generator.csv
  -> load CSV: ./results/ieee39_documentation_load.csv
  -> transformer_3p CSV: ./results/ieee39_documentation_transformer_3p.csv
  -> shunt CSV: ./results/ieee39_documentation_shunt.csv
[INFO] 参数提取完成: 总计 130 个元件
  -> bus_3p: 39 个
  -> line_3p: 46 个
  -> generator: 10 个
  -> load: 21 个
  -> transformer_3p: 12 个
  -> shunt: 2 个
```

### 结果文件

**JSON报告** (`ieee39_documentation.json`):
```json
{
  "summary": {
    "model_rid": "model/holdme/IEEE39",
    "model_name": "IEEE39",
    "total_components": 130,
    "component_types": ["bus_3p", "line_3p", "generator", "load", "transformer_3p", "shunt"],
    "type_summaries": {
      "bus_3p": {
        "count": 39,
        "common_parameters": ["Vn", "f", "VoltageLevel"]
      },
      "generator": {
        "count": 10,
        "common_parameters": ["pf_P", "pf_V", "Sn", "Vn"]
      }
    },
    "connections_count": 276
  },
  "components": [...],
  "connections": [...]
}
```

### 后续应用

基于参数提取结果，可以：
1. 生成模型参数文档和报告
2. 使用 `orthogonal_sensitivity` 进行关键参数识别
3. 使用 `param_scan` 进行参数扫描分析
4. 进行模型版本对比和变更追踪

**关键结论**：IEEE39模型共包含130个元件，其中线路46条、母线39个、发电机10台。已生成完整参数文档，可用于后续分析和校核工作。

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
