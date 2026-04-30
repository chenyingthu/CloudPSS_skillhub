# CloudPSS Skills V2 - 修复计划

**计划日期**: 2026-04-30  
**目标**: 解决设计与实现不一致问题  
**原则**: 先理解清楚，再动手修改；小步快跑，验证后再继续

---

## 修复原则

1. **理解先行**: 每处修改前确认根因和影响范围
2. **小步快跑**: 每次只修改一个独立问题
3. **验证驱动**: 修改后必须运行测试验证
4. **向后兼容**: 尽量保持 API 兼容性
5. **文档同步**: 修改代码必须同步更新文档

---

## 修复阶段规划

### 阶段 1: 基础设施统一 (P0 - 高优先级)

#### 1.1 统一 SkillResult 定义

**问题**: 两个 SkillResult 定义不一致
- `cloudpss_skills_v2/core/skill_result.py`: V2 版本
- `cloudpss_skills_v2/powerapi/base.py`: SimulationResult (类似但不一致)

**根因分析**:
```python
# core/skill_result.py - V2 SkillResult
@dataclass
class SkillResult:
    skill_name: str = ""
    status: SkillStatus = SkillStatus.PENDING
    data: dict[str, Any] = field(default_factory=dict)
    artifacts: list[Artifact] = field(default_factory=list)
    logs: list[LogEntry] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None

# powerapi/base.py - SimulationResult
@dataclass
class SimulationResult:
    job_id: str = ""
    status: Optional[SimulationStatus] = None
    data: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
```

**影响范围分析**:
- `SimulationResult` 用于 PowerAPI 层内部
- `SkillResult` 用于 PowerSkill 层和上层技能
- 两者用途不同，但都包含仿真结果数据

**修复方案** (待确认):
```python
# 方案 A: 保持两个类，统一字段命名
# - SimulationResult 用于底层适配器
# - SkillResult 用于上层技能
# - 在转换时统一字段名 (如 started_at ↔ start_time)

# 方案 B: 合并为一个类
# - 使用 SkillResult 作为统一接口
# - SimulationResult 作为别名或废弃

# 方案 C: 添加转换方法
# - 保持两个类独立
# - 添加 to_skill_result() 和 to_simulation_result() 方法
```

**我的建议**: 方案 A - 保持两个类但统一字段命名
- 原因: 两者职责不同 (底层 vs 上层)
- 修改量: 中等，需修改字段名
- 风险: 低，主要是命名统一

**需要您确认**:
1. 采用哪个方案？
2. 是否允许修改字段名 (如 `started_at` → `start_time`)？
3. 是否需要保留向后兼容的别名？

---

#### 1.2 统一 AnalysisBase 基类

**问题**: 两个 AnalysisBase 定义
- `cloudpss_skills_v2/base.py`: AnalysisBase (通用基类)
- `cloudpss_skills_v2/poweranalysis/base.py`: AnalysisBase (使用 PowerSkill API)

**根因分析**:
```python
# base.py - 通用基类
class AnalysisBase(SkillBase):
    """分析类技能基类 - 通用"""
    @property
    def category(self) -> str:
        return "poweranalysis"
    
    def _get_api(self, config): ...
    def _get_handle(self, config, api=None): ...

# poweranalysis/base.py - 使用 PowerSkill API
class AnalysisBase(ABC):
    """分析类技能基类 - 使用 PowerSkill API"""
    name: str = ""
    description: str = ""
    
    def _get_api(self, config): ...  # 使用 Engine.create_powerflow_for_skill
    def _get_handle(self, config, api=None): ...
```

**影响范围分析**:
- 所有 poweranalysis/ 下的 27 个技能都继承自 poweranalysis/base.py 的 AnalysisBase
- 修改基类会影响所有分析技能

**修复方案** (待确认):
```python
# 方案 A: 合并为一个基类
# - 保留 poweranalysis/base.py 的版本 (功能更完整)
# - 修改 base.py 中的 AnalysisBase 继承自它或标记为废弃

# 方案 B: 明确分层
# - base.py 中的 AnalysisBase: 最基础接口
# - poweranalysis/base.py 中的 AnalysisBase: 使用 PowerSkill 的实现
# - 重命名第二个以避免混淆 (如 PowerAnalysisBase)

# 方案 C: 删除一个
# - 删除 base.py 中的 AnalysisBase
# - 所有技能统一使用 poweranalysis/base.py 的版本
```

**我的建议**: 方案 B - 重命名明确区分
- 原因: 两者确实存在职责差异
- 修改量: 较大，需修改 27 个技能的导入
- 风险: 中等，主要是导入路径变更

**需要您确认**:
1. 采用哪个方案？
2. 如果重命名，新名称建议？(如 PowerAnalysisBase)
3. 是否需要提供向后兼容的导入别名？

---

### 阶段 2: Schema 与实现同步 (P1 - 高优先级)

#### 2.1 自动化 Schema/Default 一致性检查

**问题**: config_schema 中的 default 与 get_default_config() 返回的值不一致

**根因分析** (以 n1_security.py 为例):
```python
# config_schema
"voltage_threshold": {"type": "number", "default": 0.05}

# get_default_config
"analysis": {
    "voltage_threshold": 0.05,  # 可能不一致
}
```

**影响范围**:
- 27 个 PowerAnalysis 技能
- 19 个 Tools
- 需要逐一检查

**修复方案**:
```python
# 步骤 1: 创建自动化检查脚本
# scripts/validate_schema_defaults.py

def validate_skill(skill_class):
    """验证 schema 和 default_config 一致性"""
    schema = skill_class.config_schema
    defaults = skill_class.get_default_config()
    
    # 递归检查每个字段的 default 值
    # 返回不一致的字段列表

# 步骤 2: 修复不一致的技能
# 逐一修复，每个技能独立提交

# 步骤 3: 在 CI 中添加检查
# 防止未来出现不一致
```

**我的建议**:
1. 先创建检查脚本，列出所有不一致
2. 与您确认后再批量修复
3. 在 CI 中添加自动化检查

**需要您确认**:
1. 是否需要我创建检查脚本？
2. 修复顺序？(按技能类别还是按严重程度)

---

#### 2.2 完善 validate 方法

**问题**: 多数技能的 validate 方法不完整，缺少数组长度、数值范围检查

**根因分析**:
```python
# 当前实现 (n1_security.py)
def validate(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = []
    if not config.get("model", {}).get("rid"):
        errors.append("必须提供 model.rid")
    # 缺少:
    # - branches 数组长度检查
    # - voltage_threshold 范围检查
    # - thermal_threshold 范围检查
    return len(errors) == 0, errors
```

**修复方案**:
```python
# 增强版 validate
def validate(self, config: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = []
    
    # 必需字段
    if not config.get("model", {}).get("rid"):
        errors.append("必须提供 model.rid")
    
    # 数组长度检查
    branches = config.get("analysis", {}).get("branches", [])
    if branches and len(branches) < 1:
        errors.append("analysis.branches 如果提供，至少需要 1 个元素")
    
    # 数值范围检查
    voltage_threshold = config.get("analysis", {}).get("voltage_threshold", 0.05)
    if not (0 < voltage_threshold < 1):
        errors.append("analysis.voltage_threshold 必须在 0-1 之间")
    
    return len(errors) == 0, errors
```

**我的建议**:
1. 先创建 validate 基类模板
2. 逐一技能增强 validate 方法
3. 每个技能修改后运行测试验证

**需要您确认**:
1. 是否所有技能都需要完整的 validate？
2. 范围检查的阈值如何确定？(如 voltage_threshold 范围)

---

### 阶段 3: 代码质量改进 (P2 - 中优先级)

#### 3.1 提取 ToolBase 和 AnalysisBase 公共代码

**问题**: ToolBase 和 AnalysisBase 有大量重复代码

**根因分析**:
```python
# base.py - ToolBase
class ToolBase(SkillBase):
    def _log(self, level, message, context=None): ...
    def _add_artifact(self, name, path, type_, ...): ...
    def _success_result(self, data, metrics=None): ...
    def _failure_result(self, error, stage=None): ...

# base.py - AnalysisBase
class AnalysisBase(SkillBase):
    def _log(self, level, message, context=None): ...  # 重复
    def _add_artifact(self, name, path, type_, ...): ...  # 重复
    def _success_result(self, data, metrics=None): ...  # 重复
    def _failure_result(self, error, stage=None): ...  # 重复
```

**修复方案**:
```python
# 创建中间基类
class SkillMixin:
    """技能公共方法混入类"""
    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts: list[Artifact] = []
    
    def _log(self, level, message, context=None): ...
    def _add_artifact(self, name, path, type_, ...): ...
    def _success_result(self, data, metrics=None): ...
    def _failure_result(self, error, stage=None): ...

class ToolBase(SkillBase, SkillMixin): ...
class AnalysisBase(SkillBase, SkillMixin): ...
```

**影响范围**:
- 所有 Tools 和 PowerAnalysis 技能
- 需要测试所有技能确保行为不变

**需要您确认**:
1. 是否值得重构？(好处: 减少重复代码; 风险: 引入 bug)
2. 是否采用 Mixin 模式？

---

#### 3.2 HDF5ExportTool 继承 ToolBase

**问题**: HDF5ExportTool 未继承 ToolBase

**修复方案**:
```python
# 当前
class HDF5ExportTool:
    name: str = "hdf5_export"

# 修复后
class HDF5ExportTool(ToolBase):
    @property
    def name(self) -> str:
        return "hdf5_export"
```

**影响**: 需要验证所有使用 HDF5ExportTool 的代码

---

### 阶段 4: 文档同步 (P1 - 高优先级)

#### 4.1 更新 SYSTEM_DESIGN.md

**需要更新的章节**:
1. 2.1 Supported Configurations - 更新 PandaPower 状态
2. 5. Known Issues - 更新已修复问题状态
3. 新增: 9. Migration Guide (V1 → V2)

#### 4.2 更新 output-standard.md

**需要更新的章节**:
1. 2.1 SkillResult 标准结构 - 统一字段定义
2. 新增附录: V1 vs V2 字段映射

#### 4.3 更新 SKILL_DEVELOPMENT_STANDARD.md

**需要更新的章节**:
1. 2.1.1 顶层结构 - 明确使用哪个 AnalysisBase
2. 2.4 验证逻辑规范 - 添加更多验证示例
3. 新增: 8. 多引擎技能开发指南

---

## 修复执行计划

### 执行顺序

```
阶段 1.1: 统一 SkillResult (待您确认方案)
  ↓ [测试通过]
阶段 1.2: 统一 AnalysisBase (待您确认方案)
  ↓ [测试通过]
阶段 2.1: 创建 Schema 检查脚本
  ↓ [列出所有不一致]
阶段 2.2: 修复 Schema/Default 不一致 (分批)
  ↓ [测试通过]
阶段 2.3: 增强 validate 方法 (分批)
  ↓ [测试通过]
阶段 3: 代码质量改进 (可选)
  ↓ [测试通过]
阶段 4: 文档同步
```

### 每个修改的验证步骤

1. **修改前**:
   - 记录当前行为
   - 运行相关测试 (应通过)

2. **修改后**:
   - 运行相关测试 (应通过)
   - 运行示例代码
   - 检查无 regression

3. **提交前**:
   - 代码审查
   - 更新文档
   - 编写变更说明

---

## 风险评估与缓解

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| 修改引入新 bug | 中 | 高 | 每步修改后运行完整测试套件 |
| API 不兼容变化 | 中 | 高 | 保留向后兼容的别名/包装器 |
| 技能行为变化 | 低 | 高 | 对比修改前后的输出 |
| 文档不同步 | 中 | 中 | 文档修改与代码修改一起提交 |

---

## 需要您确认的问题

### 关键决策点

1. **SkillResult 统一方案**:
   - [ ] 方案 A: 保持两个类，统一字段命名
   - [ ] 方案 B: 合并为一个类
   - [ ] 方案 C: 添加转换方法

2. **AnalysisBase 统一方案**:
   - [ ] 方案 A: 合并为一个基类
   - [ ] 方案 B: 重命名区分 (推荐)
   - [ ] 方案 C: 删除一个

3. **修改范围**:
   - [ ] 只修复 P0 问题 (SkillResult, AnalysisBase, Schema)
   - [ ] 修复 P0 + P1 问题 (+ validate)
   - [ ] 修复所有问题 (+ 代码质量)

4. **向后兼容**:
   - [ ] 必须保持 100% 向后兼容
   - [ ] 允许破坏性变更 (V2 还未正式发布)
   - [ ] 保留旧 API 作为 deprecated 别名

5. **优先级**:
   - [ ] 立即开始修复
   - [ ] 先完成其他任务
   - [ ] 分阶段进行 (每周一个阶段)

### 具体问题

1. 是否允许修改字段名 (如 `started_at` → `start_time`)?
2. 如果重命名 AnalysisBase，建议的新名称？(如 PowerAnalysisBase)
3. 是否接受 Mixin 重构方案？
4. 修复过程中是否需要每日同步进度？

---

## 下一步行动

待您确认后，我将：

1. 根据您的选择确定修复方案
2. 创建第一个修复的详细实施计划
3. 执行修复并验证
4. 提交前再次与您确认

**请您审阅此计划，告诉我：**
1. 各问题的修复方案选择
2. 是否需要调整优先级
3. 其他注意事项

**在我获得您的明确确认前，我不会进行任何代码修改。**
