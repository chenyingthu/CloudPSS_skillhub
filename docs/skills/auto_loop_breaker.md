# 模型自动解环技能 (Auto Loop Breaker)

## 设计背景

### 研究对象

在电力系统仿真建模中，控制环路（Control Loop）是常见的结构。当模型中存在闭环控制时，可能会产生代数环（Algebraic Loop）或信号环（Signal Loop），这会导致：

1. **EMT仿真失败**: 代数环可能导致仿真器无法收敛
2. **数值不稳定**: 信号环可能引起数值振荡
3. **计算效率降低**: 迭代求解增加计算开销

CloudPSS提供了 `_newLoopNode` 和 `_newLoopNodeMultiDim` 解环元件，可以手动插入到环路中打破闭环。但对于复杂模型，手动识别和解环非常繁琐。

### 实际需求

1. **自动检测环路**: 识别模型中所有的控制环路
2. **智能选择解环点**: 基于图论算法选择最优的解环位置
3. **批量插入解环点**: 自动在选定位置插入解环元件
4. **预览功能**: 在修改模型前预览解环方案
5. **支持多维信号**: 处理多通道信号（ChannelMerge/ChannelDeMerge）

### 期望的输入和输出

**输入**:

- 模型RID（本地或云端）
- 解环算法参数（最大迭代次数、选择策略等）
- 解环点配置（初始值、名称前缀等）
- 输出选项（是否保存、试运行模式等）

**输出**:

- 解环分析报告（JSON格式）
- 发现的环路数量和位置
- 插入的解环点列表
- 修改后的模型（可选）

### 计算结果的用途和价值

自动解环结果可用于：

- **快速模型修复**: 自动解决代数环问题，使仿真能够正常进行
- **模型质量提升**: 消除潜在的不稳定因素
- **批量处理**: 对多个模型进行标准化解环处理
- **版本管理**: 保留原始模型，生成解环后的新分支

## 功能特性

- **图论算法**: 使用networkx构建信号流图，检测强连通分量
- **启发式FVS**: 采用启发式反馈顶点集算法，最小化解环点数量
- **多种策略**: 支持度数优先、随机、混合三种节点选择策略
- **智能识别**: 自动识别普通信号和ChannelMerge/DeMerge多维信号
- **试运行模式**: 预览解环方案而不实际修改模型
- **报告生成**: 详细的解环分析报告，包含环路位置和解环点信息

## 快速开始

### CLI方式（推荐）

```bash
# 基础解环
python -m cloudpss_skills run --config config_loop_breaker.yaml
```

### 配置示例

```yaml
skill: auto_loop_breaker
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
  source: cloud
algorithm:
  max_iterations: 500
  strategy: degree  # degree/random/hybrid
loop_node:
  init_value: "0"
  name_prefix: "LoopBreaker"
output:
  save_model: true
  dry_run: false
  new_name_suffix: "_unloop"
```

## 配置参数详解

### model（模型配置）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `rid` | string | ✅ | - | 模型RID或本地路径 |
| `source` | string | ❌ | "cloud" | 模型来源：cloud/local |

### algorithm（算法配置）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `max_iterations` | integer | ❌ | 500 | 最大迭代次数 |
| `strategy` | string | ❌ | "degree" | 节点选择策略：degree/random/hybrid |
| `random_seed` | integer | ❌ | null | 随机种子（用于random/hybrid策略） |

**策略说明**:
- `degree`: 选择度数最高的节点（出入度之和），优先打破连接最多的环路
- `random`: 随机选择节点，适用于探索不同解环方案
- `hybrid`: 混合策略，每5次迭代进行一次随机选择

### loop_node（解环点配置）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `init_value` | string | ❌ | "0" | 解环点初始值 |
| `name_prefix` | string | ❌ | "LoopBreaker" | 解环点名称前缀 |

### output（输出配置）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `save_model` | boolean | ❌ | false | 是否保存修改后的模型 |
| `dry_run` | boolean | ❌ | false | 仅预览不修改 |
| `new_name_suffix` | string | ❌ | "_unloop" | 新模型名称后缀 |

## 配置示例

### 示例1：基础解环

```yaml
skill: auto_loop_breaker
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
output:
  save_model: true
```

### 示例2：试运行模式

```yaml
skill: auto_loop_breaker
model:
  rid: model/holdme/IEEE39
output:
  dry_run: true
```

### 示例3：高级配置

```yaml
skill: auto_loop_breaker
model:
  rid: model/holdme/ComplexModel
algorithm:
  max_iterations: 1000
  strategy: hybrid
  random_seed: 42
loop_node:
  init_value: "0.0"
  name_prefix: "AutoBreak"
output:
  save_model: true
  new_name_suffix: "_nobloop"
```

## 输出结果说明

### SkillResult结构

```json
{
  "skill_name": "auto_loop_breaker",
  "status": "SUCCESS",
  "data": {
    "model_rid": "model/holdme/IEEE39",
    "model_name": "IEEE39",
    "loops_found": 5,
    "loops_broken": 5,
    "nodes_analyzed": 156,
    "edges_analyzed": 203,
    "strategy": "degree",
    "dry_run": false,
    "saved": true
  },
  "artifacts": [
    {
      "type": "json",
      "path": "./results/auto_loop_breaker_report.json",
      "description": "解环分析报告"
    }
  ]
}
```

### 解环报告结构

```json
{
  "summary": {
    "loops_found": 5,
    "loops_broken": 5,
    "dry_run": false
  },
  "loops": [
    {
      "node_id": 123,
      "component": "component-abc",
      "pin": "output"
    }
  ],
  "break_points": [
    {
      "component": "component-abc",
      "pin": "output",
      "loop_node_id": "loop-1",
      "loop_node_name": "LoopBreaker_1"
    }
  ]
}
```

## 设计原理

### 环路检测流程

```
1. 拓扑分析 → 从模型提取信号连接关系
2. 构建图 → 将信号连接转换为有向图
3. SCC检测 → 使用Tarjan算法寻找强连通分量
4. FVS计算 → 启发式算法选择最小反馈顶点集
5. 插入解环点 → 在选定节点插入LoopNode元件
```

### 反馈顶点集算法

反馈顶点集（Feedback Vertex Set, FVS）是图论中的经典问题，目标是找到最小的节点集合，使得删除这些节点后图变为无环。

**启发式算法步骤**:
1. 找到所有强连通分量（SCC）
2. 选择最大的非平凡SCC（大小>1）
3. 根据策略选择节点（度数最高或随机）
4. 从图中移除该节点，加入FVS
5. 重复直到图为有向无环图（DAG）

### 多维信号处理

对于使用ChannelMerge/ChannelDeMerge的多维信号，使用 `_newLoopNodeMultiDim` 元件，并根据信号的维度参数自动设置。

## 使用场景

### 场景1：新模型验证

对新导入的模型进行环路检测和解环，确保仿真稳定性。

```yaml
skill: auto_loop_breaker
model:
  rid: model/holdme/NewModel
output:
  dry_run: true  # 先检查是否有环路
```

### 场景2：批量解环

对多个模型进行标准化解环处理。

```yaml
skill: batch_task_manager
tasks:
  - skill: auto_loop_breaker
    model:
      rid: model/holdme/Model1
  - skill: auto_loop_breaker
    model:
      rid: model/holdme/Model2
output:
  save_model: true
  new_name_suffix: "_unloop"
```

### 场景3：复杂模型优化

对复杂模型使用混合策略进行优化解环。

```yaml
skill: auto_loop_breaker
model:
  rid: model/holdme/ComplexModel
algorithm:
  strategy: hybrid
  max_iterations: 1000
  random_seed: 42
output:
  save_model: true
```

## 注意事项

1. **试运行模式**: 建议在首次解环时启用 `dry_run: true`，预览解环方案
2. **模型备份**: 解环会修改模型，建议在解环前手动备份
3. **初始值设置**: 解环点的初始值会影响仿真初始状态，请根据实际情况设置
4. **多维信号**: 确保ChannelMerge/ChannelDeMerge的维度参数正确
5. **迭代次数**: 对于超大规模模型，可能需要增加 `max_iterations`

## 故障排除

### 问题1："未检测到环路"

**原因**: 模型中确实没有控制环路，或环路已被其他方式解决
**解决**: 检查模型拓扑，确认是否存在闭环控制

### 问题2："解环后仿真仍失败"

**原因**: 可能存在电气代数环（Electrical Algebraic Loop），而非信号环
**解决**: 检查电气连接，使用电感/电容元件打破电气环路

### 问题3："解环点插入位置不理想"

**原因**: 启发式算法选择的解环点可能不是最优
**解决**: 尝试不同的策略（random/hybrid），或手动调整解环点位置

### 问题4："保存模型失败"

**原因**: 权限不足或模型被锁定
**解决**: 确认Token有写权限，或尝试保存为新分支

## 相关技能

- **topology_check**: 拓扑检查，可用于分析模型结构
- **auto_channel_setup**: 自动量测配置，配合解环后的模型使用
- **emt_simulation**: EMT仿真，验证解环效果
- **batch_task_manager**: 批量任务管理，用于多模型解环

## 完整示例

### 场景描述

对一个包含复杂控制系统的模型进行自动解环，确保EMT仿真能够正常进行。

### 配置文件

```yaml
skill: auto_loop_breaker
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/ControlSystemModel
  source: cloud
algorithm:
  max_iterations: 500
  strategy: degree
loop_node:
  init_value: "0"
  name_prefix: "AutoBreak"
output:
  save_model: true
  dry_run: false
  new_name_suffix: "_unloop"
```

### 执行命令

```bash
python -m cloudpss_skills run --config config_loop_breaker.yaml
```

### 预期输出

```
[INFO] 加载认证信息...
[INFO] 认证成功
[INFO] 加载模型: model/holdme/ControlSystemModel
[INFO] 模型名称: ControlSystemModel
[INFO] 分析模型拓扑...
[INFO]   -> 发现 156 个信号节点，203 条连接
[INFO] 检测控制环路...
[INFO]   -> 发现控制环路，开始计算解环方案...
[INFO]   -> 需要打破 5 个环路节点
[INFO] 执行解环操作...
[INFO]   -> 成功插入 5 个解环点
[INFO] 保存修改后的模型...
[INFO]   -> 模型已保存: ControlSystemModel_unloop
[INFO] 生成解环报告...
[INFO] 解环完成！共打破 5 个环路
```

### 结果应用

1. **查看报告**: 打开 `results/auto_loop_breaker_report.json` 查看详细解环信息
2. **验证解环**: 运行EMT仿真，验证解环后的模型能够正常仿真
3. **调整优化**: 根据需要调整解环点位置或初始值

---

*该技能基于图论算法和CloudPSS SDK开发，遵循技能系统架构规范*
