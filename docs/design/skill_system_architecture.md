# CloudPSS 技能系统架构设计

## 1. 设计目标

### 核心目标
- **配置驱动**: 用户只需编辑YAML，无需编程
- **预置技能**: 常用功能是预编写、预测试的脚本
- **一键执行**: 简化操作，隐藏技术细节
- **确定性**: 相同配置产生相同结果
- **可累积**: 技能库随使用不断丰富

### 非目标
- 不替代SDK底层API
- 不做实时交互式仿真控制
- 不处理非标准/定制化需求

## 2. 三层架构

### Layer 1: 预置技能库 (Skill Library)

**职责**: 封装具体的业务功能

**设计原则**:
- 每个技能是一个独立的Python模块
- 继承统一基类 `SkillBase`
- 配置Schema驱动，代码中硬编码逻辑
- 幂等性：相同输入总是产生相同输出

**接口规范**:
```python
class SkillBase(ABC):
    """技能基类"""

    @property
    @abstractmethod
    def name(self) -> str:
        """技能唯一标识名"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """技能描述"""
        pass

    @property
    @abstractmethod
    def config_schema(self) -> dict:
        """配置JSON Schema"""
        pass

    @abstractmethod
    def run(self, config: dict) -> SkillResult:
        """执行技能"""
        pass

    def validate(self, config: dict) -> ValidationResult:
        """验证配置（可覆盖）"""
        pass
```

**目录结构**:
```
skills/
├── __init__.py           # 技能注册和导出
├── __main__.py          # CLI入口
├── core/
│   ├── __init__.py
│   ├── base.py          # SkillBase基类
│   ├── result.py        # SkillResult结果类
│   ├── config.py        # 配置加载和验证
│   └── registry.py      # 技能注册表
├── builtin/             # 内置技能
│   ├── __init__.py
│   ├── emt_simulation.py
│   ├── power_flow.py
│   ├── waveform_export.py
│   └── ieee3_prep.py
└── templates/           # 默认配置模板
    ├── emt_simulation.yaml
    ├── power_flow.yaml
    └── default.yaml
```

### Layer 2: 配置层 (Configuration Layer)

**职责**: 管理用户配置，提供配置生成和验证

**设计原则**:
- YAML格式，人类可读
- Schema验证，错误前置
- 模板继承，减少重复
- 环境变量支持，敏感信息分离

**配置结构**:
```yaml
# 配置版本
version: "1.0"

# 技能选择
skill: emt_simulation

# 认证信息（可从环境变量读取）
auth:
  token: ${CLOUDPSS_TOKEN}  # 或从文件读取
  token_file: .cloudpss_token

# 模型信息
model:
  rid: model/holdme/IEEE3
  source: cloud  # cloud | local

# 技能特定参数
simulation:
  duration: 10.0
  step_size: 0.0001
  output_channels:
    - group: 0
      channels: ["*"]  # *表示全部

# 输出配置
output:
  format: csv  # csv | json | yaml | png
  path: ./results/
  prefix: ieee3_emt
  timestamp: true  # 自动添加时间戳

# 执行选项
execution:
  timeout: 300
  retry: 3
  parallel: false
```

**配置加载优先级** (从高到低):
1. 命令行参数 `--config`
2. 环境变量 `CLOUDPSS_SKILL_CONFIG`
3. 当前目录 `skill.yaml`
4. 用户目录 `~/.cloudpss/skill.yaml`
5. 默认模板

### Layer 3: 编排层 (Orchestration Layer)

**职责**: CLI入口、技能调度、执行监控

**CLI设计**:
```bash
# 列出可用技能
python -m skills list

# 查看技能详情
python -m skills describe emt_simulation

# 交互式创建配置
python -m skills init emt_simulation --output my_sim.yaml

# 运行技能
python -m skills run --config my_sim.yaml

# 批量运行
python -m skills batch --config-dir ./configs/

# 验证配置
python -m skills validate --config my_sim.yaml

# 显示版本
python -m skills version
```

**执行流程**:
```
CLI解析 → 加载配置 → 验证配置 → 发现技能 → 执行技能 → 处理结果 → 输出报告
```

**错误处理策略**:
- 配置错误：前置验证，不执行
- 运行时错误：详细日志，优雅退出
- 超时：可配置重试，默认失败
- 部分失败：批量任务继续执行其他

## 3. 关键技术决策

### 3.1 技能注册机制

**方案选择**: 装饰器自动注册

```python
# skills/core/registry.py
SKILL_REGISTRY = {}

def register(skill_class):
    """装饰器：自动注册技能"""
    skill = skill_class()
    SKILL_REGISTRY[skill.name] = skill
    return skill_class

# skills/builtin/emt_simulation.py
from skills.core import register, SkillBase

@register
class EmtSimulationSkill(SkillBase):
    name = "emt_simulation"
    ...
```

**优势**:
- 零配置，自动发现
- 代码即文档
- 支持插件扩展

### 3.2 配置验证

**方案选择**: JSON Schema + pydantic

```python
from pydantic import BaseModel, Field
from typing import Literal

class SimulationConfig(BaseModel):
    duration: float = Field(gt=0, default=10.0)
    step_size: float = Field(gt=0, default=0.0001)
    output_channels: list[dict] = []
```

**优势**:
- 类型安全
- 自动生成错误信息
- IDE支持

### 3.3 结果处理

**结果结构**:
```python
class SkillResult:
    success: bool
    data: dict  # 结果数据
    artifacts: list[Artifact]  # 输出文件
    logs: list[LogEntry]  # 执行日志
    metrics: dict  # 性能指标

class Artifact:
    type: str  # csv | json | png | log
    path: str
    size: int
    description: str
```

### 3.4 日志和输出

**日志级别**:
- ERROR: 致命错误，任务失败
- WARNING: 非致命警告，任务继续
- INFO: 关键进度信息（默认级别）
- DEBUG: 详细调试信息

**输出格式**:
```
[时间] [级别] [技能名] 消息
```

**进度报告**:
```bash
# 简洁模式（默认）
$ python -m skills run --config sim.yaml
[14:32:01] [INFO] [emt_simulation] 加载配置: sim.yaml
[14:32:02] [INFO] [emt_simulation] 获取模型: model/holdme/IEEE3
[14:32:05] [INFO] [emt_simulation] 运行仿真...
[14:32:45] [INFO] [emt_simulation] 仿真完成，耗时 40s
[14:32:46] [INFO] [emt_simulation] 导出波形: results/ieee3_emt_20240324.csv
[14:32:46] [INFO] [emt_simulation] 任务成功完成 ✓

# 详细模式
$ python -m skills run --config sim.yaml --verbose
```

## 4. 内置技能规划

### 4.1 emt_simulation

**功能**: 运行EMT暂态仿真并导出波形

**配置参数**:
- model.rid: 模型RID
- simulation.duration: 仿真时长
- simulation.step_size: 步长（可选，默认自动）
- output.format: 输出格式
- output.channels: 输出通道选择

**输出**:
- CSV/JSON格式的波形数据
- 仿真参数报告
- 执行日志

**模板**: `templates/emt_simulation.yaml`

### 4.2 power_flow

**功能**: 运行潮流计算

**配置参数**:
- model.rid: 模型RID
- algorithm: 算法选择（牛顿拉夫逊/快速分解）
- tolerance: 收敛精度
- max_iter: 最大迭代次数

**输出**:
- 节点电压/相角
- 支路功率
- 收敛报告

### 4.3 waveform_export

**功能**: 从已有仿真任务导出波形

**配置参数**:
- job_id: 任务ID（或从文件读取）
- channels: 通道选择
- format: 输出格式
- time_range: 时间范围切片

**输出**:
- 格式化波形数据
- 可选图表（PNG）

### 4.4 ieee3_prep

**功能**: IEEE3模型EMT准备（简化版）

**配置参数**:
- fault.start_time: 故障起始时间
- fault.end_time: 故障结束时间
- output.sampling_freq: 采样频率

**输出**:
- 准备好的本地YAML文件

### 4.5 n1_analysis (未来)

**功能**: N-1安全校核

**配置参数**:
- branches: 支路选择
- criteria: 校核准则
- report.format: 报告格式

**输出**:
- 校核报告
- 越限列表
- 安全评估

## 5. 扩展机制

### 5.1 自定义技能

用户可以在项目目录创建自定义技能：

```python
# my_project/skills/custom_skill.py
from skills.core import SkillBase, register

@register
class CustomSkill(SkillBase):
    name = "my_custom"
    description = "我的自定义技能"

    def run(self, config):
        # 实现逻辑
        pass
```

### 5.2 技能组合

支持将多个技能组合成工作流：

```yaml
# workflow.yaml
workflow:
  name: power_flow_then_emt
  steps:
    - skill: power_flow
      config: ./pf_config.yaml
      output_as: pf_result

    - skill: emt_simulation
      config: ./emt_config.yaml
      depends_on: [pf_result]
```

## 6. 测试策略

### 6.1 单元测试

每个技能独立的单元测试：

```python
# tests/skills/test_emt_simulation.py
class TestEmtSimulationSkill:
    def test_config_validation(self):
        ...

    def test_mock_execution(self):
        ...

    def test_result_parsing(self):
        ...
```

### 6.2 集成测试

端到端测试（使用测试模型）：

```python
# tests/integration/test_full_workflow.py
class TestFullWorkflow:
    def test_ieee3_emt_simulation(self):
        """测试完整的IEEE3 EMT仿真流程"""
        ...
```

### 6.3 Mock策略

- CloudPSS API: Mock SDK调用
- 文件系统: Mock读写
- 时间: Mock时间函数

## 7. 性能考虑

### 7.1 启动时间

- 技能懒加载，按需导入
- 配置缓存，避免重复解析
- 注册表预生成，加速发现

### 7.2 内存使用

- 大数据流式处理
- 结果按需加载
- 支持增量导出

### 7.3 并发

- 支持多配置并行执行
- 线程安全的结果收集
- 资源限制保护

## 8. 版本兼容性

### 8.1 配置版本

配置包含版本字段，支持向后兼容：

```yaml
version: "1.0"  # 技能系统版本
skill: emt_simulation
skill_version: ">=1.0,<2.0"  # 技能版本要求
```

### 8.2 SDK兼容性

- 支持 CloudPSS SDK 4.5.x
- API变更时自动适配
- 弃用警告机制

## 9. 安全考虑

### 9.1 Token管理

- 不存储token到配置
- 支持环境变量和文件
- 权限最小化原则

### 9.2 文件访问

- 路径验证，防止目录遍历
- 写入权限检查
- 敏感文件过滤

### 9.3 代码执行

- 技能代码审查机制
- 沙箱执行（未来）
- 禁止eval/exec

## 10. 未来演进

### 短期（1个月）

- 完成4个内置技能
- 完善CLI工具
- 基础文档和示例

### 中期（3个月）

- Web UI配置编辑器
- 技能市场（共享自定义技能）
- 工作流编排

### 长期（6个月+）

- 分布式仿真支持
- 与Jupyter Notebook集成
- 自动化回归测试平台

---

## 附录A: 配置Schema示例

```yaml
# JSON Schema for emt_simulation
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["skill", "model"],
  "properties": {
    "skill": {
      "type": "string",
      "const": "emt_simulation"
    },
    "model": {
      "type": "object",
      "required": ["rid"],
      "properties": {
        "rid": {"type": "string"},
        "source": {"enum": ["cloud", "local"], "default": "cloud"}
      }
    },
    "simulation": {
      "type": "object",
      "properties": {
        "duration": {"type": "number", "minimum": 0},
        "step_size": {"type": "number", "minimum": 0},
        "output_channels": {"type": "array"}
      }
    },
    "output": {
      "type": "object",
      "properties": {
        "format": {"enum": ["csv", "json", "yaml"]},
        "path": {"type": "string"},
        "prefix": {"type": "string"}
      }
    }
  }
}
```

## 附录B: CLI命令参考

| 命令 | 描述 | 示例 |
|-----|------|------|
| `list` | 列出可用技能 | `python -m skills list` |
| `describe` | 查看技能详情 | `python -m skills describe emt` |
| `init` | 创建配置模板 | `python -m skills init emt -o sim.yaml` |
| `run` | 执行技能 | `python -m skills run -c sim.yaml` |
| `batch` | 批量执行 | `python -m skills batch -d ./configs/` |
| `validate` | 验证配置 | `python -m skills validate -c sim.yaml` |
| `version` | 显示版本 | `python -m skills version` |

---

**设计完成日期**: 2024-03-24
**版本**: v1.0
**作者**: Claude
