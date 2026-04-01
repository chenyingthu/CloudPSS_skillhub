# 模型验证技能 (model_validator)

## 功能概述

系统性验证测试算例的有效性，分阶段进行拓扑、潮流、暂态和参数对比验证。确保 `model_builder` 创建的模型真实可用。

## 核心特性

- ✅ **分阶段验证**: 拓扑 → 潮流 → 暂态 → 参数对比
- ✅ **批量验证**: 一次验证多个模型
- ✅ **详细报告**: 每个阶段的通过/失败状态和详细信息
- ✅ **常量配置**: 使用可配置的验证阈值（超时、电压范围等）

## 验证流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  拓扑验证   │ → │  潮流验证   │ → │  暂态验证   │ → │  参数对比   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      │                  │                  │                  │
      ▼                  ▼                  ▼                  ▼
  孤岛检测          收敛性检查        EMT拓扑就绪       与基模对比
  悬空引脚          电压范围          仿真可行性        元件数量
  参数完整性        支路潮流          输出通道          修改正确性
```

## 配置说明

```yaml
skill: model_validator

auth:
  token_file: .cloudpss_token

models:
  - rid: model/holdme/test_IEEE39_with_PV_50MW
    base_rid: model/holdme/IEEE39
    name: "IEEE39+50MW光伏"

  - rid: model/holdme/test_IEEE39_with_DifferentialProtection
    base_rid: model/holdme/IEEE39
    name: "IEEE39+差动保护"

validation:
  phases:
    - topology      # 拓扑验证
    - powerflow     # 潮流验证
    - emt           # 暂态验证（可选）
    - parameter     # 参数对比验证
  timeout: 300
  powerflow_tolerance: 1e-6
  emt_duration: 1.0

output:
  format: console  # console 或 json
  path: ./validation_report.json
```

## 验证阶段

### 1. Topology 验证

检查模型拓扑的完整性和连通性。

**检查项目:**
- 元件总数统计
- 母线数量统计
- 电源数量统计
- 悬空引脚检测
- 参数完整性检查

**通过标准:**
- 能成功获取模型拓扑
- 无严重连通性问题

**示例输出:**
```
[阶段1] 拓扑验证...
  元件总数: 511
  母线数量: 39
  电源数量: 14
  ⚠️ 悬空引脚: 187 个
  ⚠️ 参数不完整: 193 个
  ✅ 拓扑验证通过
```

### 2. Powerflow 验证

运行潮流计算，检查收敛性和结果合理性。

**检查项目:**
- 潮流计算收敛性
- 电压范围（默认 0.5~1.5 pu）
- 支路潮流计算

**通过标准:**
- 潮流计算成功收敛
- 所有母线电压在合理范围内

**示例输出:**
```
[阶段2] 潮流验证...
  提交潮流计算任务...
  电压范围: 0.9823 ~ 1.0435 pu
  支路数量: 46
  ✅ 潮流验证通过
```

### 3. EMT 验证

检查EMT暂态仿真可行性。

**检查项目:**
- EMT拓扑就绪状态
- 短时仿真测试（默认1秒）
- 输出通道存在性

**通过标准:**
- EMT拓扑可获取
- 仿真成功完成

**示例输出:**
```
[阶段3] 暂态验证...
  检查EMT拓扑...
  EMT元件数: 511
  提交EMT仿真（1.0s）...
  输出通道: 3 个
  ✅ 暂态验证通过
```

### 4. Parameter 验证

与原始模型对比，验证修改正确性。

**检查项目:**
- 基模与修改模型元件数量对比
- 新增元件统计
- 元件删除确认

**通过标准:**
- 元件数量变化符合预期

**示例输出:**
```
[阶段4] 参数对比验证...
  原始元件: 510
  当前元件: 511
  新增元件: 1
  ✅ 参数对比验证通过
```

## 使用示例

### 示例1: 验证单个模型

```yaml
skill: model_validator

models:
  - rid: model/holdme/test_IEEE39_with_PV_50MW
    base_rid: model/holdme/IEEE39
    name: "光伏模型验证"

validation:
  phases:
    - topology
    - powerflow
    - parameter
```

### 示例2: 批量验证多个模型

```yaml
skill: model_validator

models:
  - rid: model/holdme/test_IEEE39_with_PV_50MW
    base_rid: model/holdme/IEEE39
    name: "光伏50MW"
  - rid: model/holdme/test_IEEE39_with_PV_100MW
    base_rid: model/holdme/IEEE39
    name: "光伏100MW"
  - rid: model/holdme/test_IEEE39_with_PV_150MW
    base_rid: model/holdme/IEEE39
    name: "光伏150MW"

validation:
  phases: [topology, powerflow, parameter]
  timeout: 300

output:
  format: json
  path: ./pv_validation_report.json
```

### 示例3: 完整验证（含EMT）

```yaml
skill: model_validator

models:
  - rid: model/holdme/test_IEEE39_with_DifferentialProtection
    base_rid: model/holdme/IEEE39
    name: "保护模型"

validation:
  phases:
    - topology
    - powerflow
    - emt           # 包含EMT验证
    - parameter
  emt_duration: 2.0  # EMT仿真2秒

output:
  format: console
```

## 输出结果

### Console 格式

```
================================================================================
模型验证报告
================================================================================

模型: 光伏50MW
RID: model/holdme/test_IEEE39_with_PV_50MW
结果: ✅ 通过
  ✅ topology
      警告: 发现 187 个元件有悬空引脚
      警告: 发现 193 个元件参数不完整
  ✅ powerflow
  ✅ parameter

================================================================================
总计: 1/1 通过
================================================================================
```

### JSON 格式

```json
[
  {
    "model_rid": "model/holdme/test_IEEE39_with_PV_50MW",
    "model_name": "光伏50MW",
    "overall_passed": true,
    "phases": {
      "topology": {
        "phase": "topology",
        "passed": true,
        "details": {
          "total_components": 511,
          "bus_count": 39,
          "generator_count": 14
        }
      },
      "powerflow": {
        "phase": "powerflow",
        "passed": true,
        "details": {
          "converged": true,
          "voltage_min": 0.9823,
          "voltage_max": 1.0435,
          "branch_count": 46
        }
      },
      "parameter": {
        "phase": "parameter",
        "passed": true,
        "details": {
          "base_component_count": 510,
          "modified_component_count": 511,
          "added_components": 1
        }
      }
    },
    "issues": [],
    "warnings": ["发现 187 个元件有悬空引脚", "发现 193 个元件参数不完整"]
  }
]
```

## 验证结果字段

| 字段 | 类型 | 说明 |
|-----|-----|-----|
| `model_rid` | string | 模型RID |
| `model_name` | string | 模型名称 |
| `overall_passed` | boolean | 整体是否通过 |
| `phases` | object | 各阶段验证结果 |
| `phases.{phase}.passed` | boolean | 该阶段是否通过 |
| `phases.{phase}.errors` | array | 错误信息列表 |
| `phases.{phase}.warnings` | array | 警告信息列表 |
| `phases.{phase}.details` | object | 详细数据 |
| `issues` | array | 所有错误汇总 |
| `warnings` | array | 所有警告汇总 |

## 常量配置

从 `cloudpss_skills.core.auth_utils` 导入的默认常量：

| 常量 | 默认值 | 说明 |
|-----|-------|-----|
| `DEFAULT_TIMEOUT` | 300 | 仿真超时时间（秒） |
| `DEFAULT_POWERFLOW_TOLERANCE` | 1e-6 | 潮流收敛精度 |
| `DEFAULT_VOLTAGE_MIN` | 0.5 | 电压下限（pu） |
| `DEFAULT_VOLTAGE_MAX` | 1.5 | 电压上限（pu） |

## 技术实现

### 公共认证模块

```python
from cloudpss_skills.core.auth_utils import setup_auth, DEFAULT_TIMEOUT

# 统一认证
setup_auth(config)
```

### 验证报告类

```python
@dataclass
class ValidationReport:
    model_rid: str
    model_name: str = ""
    phases: Dict[str, Any] = field(default_factory=dict)
    overall_passed: bool = False
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
```

## 注意事项

1. **验证时间**: 每个模型的完整验证可能需要几分钟（取决于仿真计算时间）
2. **警告处理**: 悬空引脚和参数不完整警告通常来自原始模型，不影响使用
3. **基模对比**: `parameter` 阶段需要 `base_rid` 才能进行对比
4. **EMT验证**: EMT仿真较耗时，如不需要可跳过该阶段

## 故障排查

| 问题 | 可能原因 | 解决方案 |
|-----|---------|---------|
| 拓扑验证失败 | 模型RID错误 | 检查模型RID是否存在 |
| 潮流验证失败 | 模型不收敛 | 检查模型参数设置 |
| EMT验证失败 | EMT拓扑错误 | 使用 `auto_channel_setup` 配置通道 |
| 验证超时 | 仿真时间太长 | 增加 `timeout` 配置或跳过EMT验证 |

## 配套技能

- **[model_builder](model_builder.md)**: 创建测试算例
- **[component_catalog](component_catalog.md)**: 查找可用组件
- **[auto_channel_setup](auto_channel_setup.md)**: 自动配置EMT输出通道
