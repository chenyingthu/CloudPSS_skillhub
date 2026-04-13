# 拓扑检查技能 (Topology Check)

## 设计背景

### 研究对象

电力系统模型的拓扑结构是进行潮流计算、暂态仿真、安全分析等所有电力系统分析的基础。拓扑检查技能用于验证电力系统模型的拓扑完整性和连通性，识别可能影响计算和分析准确性的拓扑问题，如电气孤岛、悬空元件、参数缺失等。

### 实际需求

在电力系统模型构建、数据导入、仿真分析等场景中，拓扑检查具有以下重要作用：

1. **数据质量保障**: 在建模阶段识别数据错误和不完整
2. **仿真前验证**: 确保模型可以进行潮流计算和EMT仿真
3. **故障诊断**: 定位导致计算失败或结果异常的拓扑问题
4. **模型标准化**: 确保模型符合分析工具的要求
5. **EMT就绪检查**: 验证模型是否配置完整的EMT仿真所需元件
6. **数据导入验证**: 检查从外部系统导入的模型数据完整性

### 期望的输入和输出

**输入**:
- 电力系统模型（标准系统或实际系统）
- 检查类型配置（孤岛/悬空/参数/EMT就绪）
- 拓扑分析参数（连通性阈值等）

**输出**:
- 拓扑检查结果汇总
- 孤岛数量和详细信息
- 悬空元件清单
- 参数缺失问题列表
- EMT就绪状态评估
- 修复建议和详细报告

### 计算结果的用途和价值

拓扑检查结果可直接用于：
- 在仿真前识别和修复模型问题，避免计算失败
- 评估模型的可用性和可靠性
- 指导模型数据的清洗和完善
- 为新模型验收提供质量检验依据
- 定位复杂问题的根本原因
- 建立模型质量评估标准

## 功能特性

- **孤岛检测**: 识别电气上不相连的子系统（连通分量分析）
- **悬空检查**: 发现未连接任何支路的孤立元件
- **参数检查**: 检查元件关键参数是否缺失或无效
- **EMT就绪检查**: 验证模型是否具备EMT仿真所需的完整配置
- **详细报告**: 生成包含问题位置、类型、严重程度的详细报告
- **修复建议**: 针对发现的问题提供修复指导
- **批量检查**: 支持多种检查类型的批量执行

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化配置
python -m cloudpss_skills init topology_check --output tc.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config tc.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("topology_check")

# 配置
config = {
    "skill": "topology_check",
    "auth": {
        "token_file": ".cloudpss_token"
    },
    "model": {
        "rid": "model/holdme/IEEE39",
        "source": "cloud"
    },
    "checks": {
        "islands": True,       # 检查孤岛
        "dangling": True,      # 检查悬空元件
        "parameter": True,     # 检查参数
        "emt_ready": False     # 检查EMT就绪
    },
    "output": {
        "format": "json",
        "path": "./results/",
        "prefix": "topology_check",
        "timestamp": True
    }
}

# 验证配置
validation = skill.validate(config)
if not validation.valid:
    print("配置错误:", validation.errors)

# 运行
result = skill.run(config)
print(f"状态: {result.status}")
print(f"数据: {result.data}")
```

### 3.3 YAML配置示例

```yaml
skill: topology_check
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

checks:
  islands: true       # 检查孤岛
  dangling: true      # 检查悬空元件
  parameter: true     # 检查参数完整性
  emt_ready: false    # 检查EMT就绪状态

island_detection:
  min_island_size: 2  # 最小孤岛规模（节点数）
  ignore_ground: true # 忽略接地孤岛

dangling_detection:
  include_shunts: false  # 是否检查并联支路

parameter_check:
  required_only: true    # 仅检查必需参数
  check_ranges: true     # 检查参数数值范围

output:
  format: json
  path: ./results/
  prefix: topology_check
  timestamp: true
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: topology_check                   # 必需: 技能名称
auth:                                   # 认证配置
  token: string                         # 直接提供token（不推荐）
  token_file: string                    # token文件路径（默认: .cloudpss_token）

model:                                  # 模型配置（必需）
  rid: string                           # 模型RID或本地路径（必需）
  source: enum                          # cloud | local（默认: cloud）

checks:                                 # 检查类型配置
  islands: boolean                      # 孤岛检测（默认: true）
  dangling: boolean                     # 悬空检查（默认: true）
  parameter: boolean                    # 参数检查（默认: true）
  emt_ready: boolean                    # EMT就绪检查（默认: false）

island_detection:                       # 孤岛检测配置
  min_island_size: integer              # 最小孤岛规模（默认: 2）
  ignore_ground: boolean                # 忽略接地孤岛（默认: true）
  include_transformers: boolean         # 考虑变压器连接（默认: true）

dangling_detection:                     # 悬空检测配置
  include_shunts: boolean               # 检查并联支路（默认: false）
  include_generators: boolean           # 检查发电机（默认: true）
  include_loads: boolean                # 检查负荷（默认: true）

parameter_check:                        # 参数检查配置
  required_only: boolean                # 仅检查必需参数（默认: true）
  check_ranges: boolean                 # 检查参数范围（默认: true）
  tolerance: number                     # 参数容差（默认: 1e-6）

emt_check:                              # EMT检查配置
  check_fault_components: boolean       # 检查故障元件（默认: true）
  check_meters: boolean                 # 检查量测信号（默认: true）
  check_output_channels: boolean        # 检查输出通道（默认: true）

output:                                 # 输出配置
  format: enum                          # json | yaml（默认: json）
  path: string                          # 输出目录（默认: ./results/）
  prefix: string                        # 文件名前缀（默认: topology_check）
  timestamp: boolean                    # 是否添加时间戳（默认: true）
```

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"topology_check" |
| `auth.token` | string | 否 | - | 直接提供API token |
| `auth.token_file` | string | 否 | .cloudpss_token | token文件路径 |
| `model.rid` | string | 是 | - | 模型RID或本地YAML路径 |
| `model.source` | enum | 否 | cloud | 模型来源：cloud(云端) / local(本地) |
| `checks.islands` | boolean | 否 | true | 是否执行孤岛检测 |
| `checks.dangling` | boolean | 否 | true | 是否执行悬空检查 |
| `checks.parameter` | boolean | 否 | true | 是否执行参数检查 |
| `checks.emt_ready` | boolean | 否 | false | 是否执行EMT就绪检查 |
| `island_detection.min_island_size` | integer | 否 | 2 | 报告的最小孤岛节点数 |
| `island_detection.ignore_ground` | boolean | 否 | true | 是否忽略接地形成的孤岛 |
| `island_detection.include_transformers` | boolean | 否 | true | 是否考虑变压器连接关系 |
| `dangling_detection.include_shunts` | boolean | 否 | false | 是否检查未连接的并联支路 |
| `dangling_detection.include_generators` | boolean | 否 | true | 是否检查未连接的发电机 |
| `dangling_detection.include_loads` | boolean | 否 | true | 是否检查未连接的负荷 |
| `parameter_check.required_only` | boolean | 否 | true | 仅检查必需参数 |
| `parameter_check.check_ranges` | boolean | 否 | true | 检查参数是否在合理范围内 |
| `parameter_check.tolerance` | number | 否 | 1e-6 | 数值参数容差 |
| `emt_check.check_fault_components` | boolean | 否 | true | 检查是否有故障元件 |
| `emt_check.check_meters` | boolean | 否 | true | 检查是否有量测信号 |
| `emt_check.check_output_channels` | boolean | 否 | true | 检查是否有输出通道 |
| `output.format` | enum | 否 | json | 输出格式：json / yaml |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.prefix` | string | 否 | topology_check | 文件名前缀 |
| `output.timestamp` | boolean | 否 | true | 文件名是否包含时间戳 |

## Agent使用指南

### 5.1 基本调用模式

```python
# 获取技能实例
skill = get_skill("topology_check")

# 最小化配置（使用默认值）
config = {
    "model": {"rid": "model/holdme/IEEE39"},
    "checks": {
        "islands": True,
        "dangling": True,
        "parameter": True
    }
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status == "SUCCESS":
        print(f"检查完成: {result.data}")
    else:
        print(f"检查失败: {result.error}")
```

### 5.2 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data

    # 访问检查摘要
    summary = data.get("summary", {})
    print(f"孤岛数量: {summary.get('islands_count', 0)}")
    print(f"悬空元件: {summary.get('dangling_count', 0)}")
    print(f"参数问题: {summary.get('parameter_issues', 0)}")
    print(f"EMT就绪: {summary.get('emt_ready', False)}")

    # 访问详细问题列表
    issues = data.get("issues", [])
    print(f"发现问题总数: {len(issues)}")
    for issue in issues:
        print(f"  [{issue['severity']}] {issue['type']}: {issue['description']}")

    # 访问孤岛详情
    islands = data.get("details", {}).get("islands", [])
    for island in islands:
        print(f"孤岛 {island['id']}: {island['nodes']} 个节点, {island['components']} 个元件")

    # 访问输出文件
    for artifact in result.artifacts:
        print(f"输出文件: {artifact.path} ({artifact.type})")

# 查看日志
for log in result.logs:
    print(f"[{log.level}] {log.message}")
```

### 5.3 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    error_msg = result.error

    # 常见错误处理
    if "Token文件不存在" in error_msg:
        print("错误: 请创建.cloudpss_token文件")
    elif "模型不存在" in error_msg:
        print("错误: 请检查模型RID是否正确")
    elif "无法加载拓扑" in error_msg:
        print("错误: 模型拓扑数据损坏或不完整")
    elif "模型为空" in error_msg:
        print("错误: 模型中没有元件或母线")
    else:
        print(f"未知错误: {error_msg}")
```

## 输出结果

### 6.1 JSON输出格式

```json
{
  "model": "IEEE39",
  "model_rid": "model/holdme/IEEE39",
  "timestamp": "2024-03-24T14:32:01",
  "summary": {
    "islands_count": 1,
    "dangling_count": 0,
    "parameter_issues": 2,
    "emt_ready": true,
    "overall_status": "warning"
  },
  "issues": [
    {
      "id": 1,
      "type": "island",
      "severity": "error",
      "description": "发现2个电气孤岛",
      "location": "Island_2"
    },
    {
      "id": 2,
      "type": "parameter",
      "severity": "warning",
      "description": "元件参数超出合理范围",
      "location": "Line_1.R"
    }
  ],
  "details": {
    "islands": [
      {
        "id": 1,
        "size": 39,
        "nodes": ["Bus_1", "Bus_2", "..."],
        "components": ["Gen_1", "Load_1", "..."],
        "is_main": true
      }
    ],
    "dangling": [],
    "parameters": [
      {
        "component": "Line_1",
        "parameter": "R",
        "value": -0.01,
        "expected_range": [0, 10],
        "issue": "负值"
      }
    ],
    "emt_status": {
      "ready": true,
      "fault_components": true,
      "meters": true,
      "output_channels": true
    }
  }
}
```

### 6.2 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "topology_check" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典，包含检查结果摘要和详情 |
| `artifacts` | list | 输出文件列表（Artifact对象），包含JSON报告 |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标 |

## 设计原理

### 工作流程

```
1. 模型加载
   ├── 加载系统模型
   ├── 获取元件列表
   ├── 获取连接关系
   └── 获取参数数据

2. 孤岛检测
   ├── 构建无向图（母线为节点，支路为边）
   ├── 执行连通分量分析（DFS/BFS）
   ├── 识别连通分量
   ├── 标记主系统（最大连通分量）
   └── 统计孤岛信息

3. 悬空检查
   ├── 遍历所有元件
   ├── 检查元件连接状态
   │   ├── 发电机：检查是否连接母线
   │   ├── 负荷：检查是否连接母线
   │   ├── 线路：检查两端是否连接
   │   └── 变压器：检查绕组连接
   └── 记录未连接元件

4. 参数检查
   ├── 遍历所有元件参数
   ├── 检查必需参数是否存在
   ├── 检查参数值有效性
   │   ├── 数值类型检查
   │   ├── 范围检查（如R>0, X>0）
   │   └── 单位检查
   └── 记录参数问题

5. EMT就绪检查
   ├── 检查故障元件配置
   │   └── 是否存在故障组件
   ├── 检查量测信号
   │   └── 是否配置电压/电流量测
   ├── 检查输出通道
   │   └── 是否配置输出变量
   └── 评估EMT就绪状态

6. 结果汇总
   ├── 统计问题数量
   ├── 评估严重程度
   ├── 生成修复建议
   └── 输出JSON报告
```

### 检查规则

**孤岛检测规则**:
- 通过线路、变压器连接的母线属于同一连通分量
- 连通分量大小 = 包含的母线数量
- 最大连通分量为主系统
- 其他连通分量为孤岛

**悬空检测规则**:
- 发电机/负荷：至少连接到一个母线
- 线路：两端都必须连接到母线
- 变压器：所有绕组都必须连接

**参数检查规则**:
- 电阻R：必须 >= 0
- 电抗X：必须 >= 0
- 容量：必须 > 0
- 电压等级：必须在合理范围内

## 与其他技能的关联

```
topology_check
    ↓ (检查通过)
power_flow
    ↓ (潮流结果)
emt_simulation / n1_security
    ↓ (仿真/分析结果)
其他分析技能
```

### 依赖关系

- **必需依赖**: CloudPSS SDK (`cloudpss`)
- **输入依赖**: 无（直接使用模型）
- **输出被依赖**:
  - `power_flow`: 建议在潮流计算前执行拓扑检查
  - `emt_simulation`: EMT仿真前建议检查EMT就绪状态
  - `n1_security`: N-1分析前建议检查拓扑完整性

## 性能特点

- **执行时间**: IEEE39系统约1-3秒
- **内存占用**: 与系统规模成正比
- **算法复杂度**: O(N + E)，N为节点数，E为边数
- **适用规模**: 已测试至1000节点系统
- **实时性**: 可集成到建模工具实时检查

## 常见问题

### 问题1: 发现多个孤岛

**原因**:
- 线路或变压器未正确连接
- 模型数据不完整
- 系统本身设计为多区域

**解决**:
- 检查模型连接关系
- 确认是否为预期的多区域系统
- 使用`min_island_size`过滤小孤岛

```yaml
island_detection:
  min_island_size: 5  # 只报告5个节点以上的孤岛
```

### 问题2: 存在悬空元件

**原因**:
- 元件连接参数错误
- 母线标签不匹配
- 数据导入错误

**解决**:
- 检查元件的`bus`或`connections`参数
- 确认母线标签拼写正确
- 检查数据导入映射关系

### 问题3: EMT检查失败

**原因**:
- 缺少故障元件
- 未配置量测信号
- 未配置输出通道

**解决**:
- 使用 `auto_channel_setup` 技能配置EMT模型
- 配置电压/电流量测信号
- 添加输出通道配置

### 问题4: 参数检查误报

**原因**:
- 参数容差设置过严
- 特殊元件参数范围不同
- 单位换算问题

**解决**:
```yaml
parameter_check:
  tolerance: 1e-3    # 放宽容差
  check_ranges: false  # 关闭范围检查（仅检查存在性）
```

## 完整示例

### 场景描述

某电力公司在接收新的IEEE39系统模型数据后，需要在投入分析使用前进行全面的拓扑检查，确保模型数据完整、连接正确，并验证是否可以直接用于EMT仿真。

### 配置文件

```yaml
skill: topology_check
auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39
  source: cloud

checks:
  islands: true
  dangling: true
  parameter: true
  emt_ready: true

island_detection:
  min_island_size: 2
  ignore_ground: true

dangling_detection:
  include_shunts: false
  include_generators: true
  include_loads: true

parameter_check:
  required_only: true
  check_ranges: true

emt_check:
  check_fault_components: true
  check_meters: true
  check_output_channels: true

output:
  format: json
  path: ./results/
  prefix: topology_ieee39
  timestamp: true
```

### 执行命令

```bash
python -m cloudpss_skills run --config topology_check.yaml
```

### 预期输出

```
[INFO] 加载认证信息...
[INFO] 认证成功
[INFO] 获取模型: IEEE39
[INFO] 加载模型拓扑...
[INFO] 执行拓扑检查...
[INFO] [孤岛检测] 发现1个连通分量
[INFO] [悬空检查] 未发现悬空元件
[INFO] [参数检查] 发现2个参数问题
[INFO] [EMT就绪] 模型已配置完整
[INFO] 检查完成，整体状态: warning
[INFO] 结果已保存: ./results/topology_ieee39_20240324_143245_result.json
```

### 结果文件

**JSON结果文件** (`topology_ieee39_20240324_143245_result.json`):

```json
{
  "model": "IEEE39",
  "model_rid": "model/holdme/IEEE39",
  "timestamp": "2024-03-24T14:32:45",
  "summary": {
    "islands_count": 1,
    "dangling_count": 0,
    "parameter_issues": 2,
    "emt_ready": true,
    "overall_status": "warning"
  },
  "issues": [
    {
      "id": 1,
      "type": "parameter",
      "severity": "warning",
      "description": "线路电阻接近零",
      "location": "Line_1.R",
      "suggestion": "检查线路参数是否正确"
    },
    {
      "id": 2,
      "type": "parameter",
      "severity": "info",
      "description": "负荷功率因数偏低",
      "location": "Load_1.pf",
      "suggestion": "确认负荷特性参数"
    }
  ],
  "details": {
    "islands": [
      {
        "id": 1,
        "size": 39,
        "is_main": true,
        "nodes": ["Bus_1", "Bus_2", "..."],
        "components": 46
      }
    ],
    "dangling": [],
    "parameters": [
      {
        "component": "Line_1",
        "parameter": "R",
        "value": 0.0001,
        "issue": "接近零",
        "expected_min": 0.001
      }
    ],
    "emt_status": {
      "ready": true,
      "fault_components": true,
      "meters": true,
      "output_channels": true
    }
  }
}
```

### 后续应用

1. **模型修复**: 根据检查结果修复模型问题
2. **潮流计算**: 在确认拓扑正确后执行`power_flow`
3. **EMT仿真**: 在EMT就绪检查通过后执行`emt_simulation`
4. **批量检查**: 集成到模型入库流程中自动化检查

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28
