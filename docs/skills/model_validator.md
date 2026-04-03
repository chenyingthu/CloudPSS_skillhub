# 模型验证技能 (model_validator)

## 功能概述

系统性验证测试算例的有效性，分阶段进行拓扑、潮流、暂态和参数对比验证。确保 `model_builder` 创建的模型真实可用。

## 核心特性

- ✅ **分阶段验证**: 拓扑 → 潮流 → 暂态 → 参数对比
- ✅ **批量验证**: 一次验证多个模型
- ✅ **详细报告**: 每个阶段的通过/失败状态和详细信息
- ✅ **新能源硬门槛**: 会直接拦截“元件存在但未接入母线”或“潮流里没有真实注入”的坏案例
- ✅ **常量配置**: 使用可配置的验证阈值（超时、电压范围等）

## 验证流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  拓扑验证   │ → │  潮流验证   │ → │  暂态验证   │ → │  参数对比   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      │                  │                  │                  │
      ▼                  ▼                  ▼                  ▼
  孤岛检测          收敛性检查        EMT拓扑就绪       与基模对比
  新能源接线        结果表完整性      仿真可行性        元件数量
  关键参数齐全      真实出力校验      输出通道          修改正确性
```

**执行顺序说明:**
- 验证是严格序贯的：`topology -> powerflow -> emt -> parameter`
- 前一阶段未通过，后一阶段直接跳过
- 因此：
  - 过 `topology + powerflow`，可视为“潮流可用算例”
  - 过 `topology + powerflow + emt`，可视为“具备最小 EMT 可仿真性”

## 配置说明

```yaml
skill: model_validator

auth:
  token_file: .cloudpss_token

models:
  - rid: model/holdme/test_ieee39_pv
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
- 新能源元件数量统计
- 新能源元件是否接到有效母线信号
- 新能源关键参数是否齐全

**通过标准:**
- 能成功获取模型拓扑
- 新能源元件没有悬空或错误母线连接
- 新能源关键参数满足最小运行要求

**示例输出:**
```
[阶段1] 拓扑验证...
  元件总数: 511
  母线数量: 39
  新能源元件数量: 1
  ✅ 拓扑验证通过
```

### 2. Powerflow 验证

运行潮流计算，检查收敛性和结果合理性。

**检查项目:**
- 潮流计算收敛性
- 母线/支路结果表是否非空
- 电压范围（默认 0.5~1.5 pu）
- 新能源接入点是否在潮流结果中出现真实出力

**通过标准:**
- 潮流计算成功收敛
- 结果表不为空
- 所有母线电压在合理范围内
- 对新能源模型，接入点必须在潮流结果中体现出非零有功出力

**示例输出:**
```
[阶段2] 潮流验证...
  提交潮流计算任务...
  电压范围: 0.9089 ~ 1.0630 pu
  新能源出力检查: 1 个接入点
  ✅ 潮流验证通过
```

### 3. EMT 验证

检查 EMT 暂态仿真可行性。

**检查项目:**
- EMT拓扑就绪状态
- 短时仿真测试（默认1秒）
- `plot` 输出是否存在
- 至少一条波形是否非空、点数足够、且不是全零空轨迹

**通过标准:**
- EMT拓扑可获取
- 仿真成功完成
- 至少存在一条有效波形

**示例输出:**
```
[阶段3] 暂态验证...
  检查EMT拓扑...
  EMT元件数: 511
  提交EMT仿真（1.0s）...
  输出通道: 3 个
  有效波形: plot-0 / vac:0 (20001 点)
  ✅ 暂态验证通过
```

**边界说明:**
- EMT 通过说明模型具备最小可仿真性
- EMT 通过不等于模型“完全正确”
- 对研究型或发布级算例，仍应继续结合潮流断面、关键波形断言和工程解释做更深验证

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
  - rid: model/holdme/test_ieee39_pv
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
RID: model/holdme/test_ieee39_pv
结果: ✅ 通过
  ✅ topology
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
    "model_rid": "model/holdme/test_ieee39_pv",
    "model_name": "光伏50MW",
    "overall_passed": true,
    "phases": {
      "topology": {
        "phase": "topology",
        "passed": true,
        "details": {
          "total_components": 511,
          "bus_count": 39,
          "renewable_count": 1
        }
      },
      "powerflow": {
        "phase": "powerflow",
        "passed": true,
        "details": {
          "converged": true,
          "voltage_min": 0.9525,
          "voltage_max": 1.03,
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
    "warnings": []
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
2. **硬门槛优先**: 对新能源模型，错误母线连接、缺关键参数、潮流结果无真实注入都会直接判定失败
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
