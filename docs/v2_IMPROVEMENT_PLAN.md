# CloudPSS Skills V2 - 全面改进计划

**计划版本**: 1.0  
**创建日期**: 2026-04-30  
**计划周期**: 4周（分4个阶段）  
**状态**: 待审批  

---

## 一、计划总览

### 1.1 改进目标

| 目标 | 描述 | 验收标准 |
|------|------|----------|
| 配置一致性 | 修复 46 个技能的 Schema/Default 不一致 | `validate_schema_defaults.py` 全绿 |
| 架构健壮性 | 统一错误处理、完善类型注解 | 新增 0 个 mypy 错误 |
| 测试覆盖 | 补充核心技能测试 | 覆盖率从 45% 提升至 75% |
| 文档完善 | API 文档、使用示例、故障排查 | 每个技能有完整示例 |
| 工程规范 | CI 增强、预提交钩子、依赖管理 | CI 全绿、100% 提交检查 |

### 1.2 风险评估

| 风险项 | 级别 | 影响 | 缓解策略 |
|--------|------|------|----------|
| 批量修改引入回归 | 高 | 技能功能异常 | 分批次修改、每批后运行集成测试 |
| 配置格式变更破坏兼容性 | 中 | 现有配置失效 | 保持向后兼容、渐进式迁移 |
| 时间超期 | 低 | 无法按计划完成 | 优先级排序、可裁剪低优先级任务 |

### 1.3 备份与回滚策略

```bash
# 1. 阶段开始前备份
git checkout -b improvement/{phase-name}-backup-{date}
git push origin improvement/{phase-name}-backup-{date}

# 2. 每批次修改后提交
git add .
git commit -m "feat({skill-name}): fix schema/default consistency"

# 3. 回滚命令（如需要）
git reset --hard HEAD~{n}  # 回滚最近n次提交
git revert {commit-hash}   # 撤销特定提交
```

---

## 二、阶段详细计划

### 阶段 1: Schema/Default 一致性修复（Week 1）

**目标**: 修复所有 46 个技能的配置不一致问题

#### 1.1 前置准备

| 步骤 | 内容 | 预计时间 | 验证方式 |
|------|------|----------|----------|
| 1.1.1 | 创建改进分支 `improvement/schema-consistency` | 5min | `git branch` |
| 1.1.2 | 运行完整检查，生成详细报告 | 10min | `validate_schema_defaults.py > reports/schema_issues.json` |
| 1.1.3 | 按严重度分类技能列表 | 15min | 分类文档 |

#### 1.2 修复批次划分

```
批次 1（核心技能 - 8个）: power_flow, n1_security, short_circuit, emt_simulation,
                         transient_stability, voltage_stability, contingency_analysis, batch_powerflow
                         时间: Day 1-2

批次 2（高级分析 - 15个）: param_scan, loss_analysis, harmonic_analysis, small_signal_stability,
                          frequency_response, disturbance_severity, protection_coordination,
                          thevenin_equivalent, dudv_curve, orthogonal_sensitivity,
                          transient_stability_margin, fault_clearing_scan, fault_severity_scan,
                          maintenance_security, n2_security
                          时间: Day 3-4

批次 3（其他技能 - 23个）: 剩余技能
                          时间: Day 5-7
```

#### 1.3 单技能修复规范

**修复原则**:
1. **保持向后兼容**: 不改变现有行为的默认值
2. **Schema 为准**: 如果 Schema 有 `default`，Config 必须匹配
3. **显式优于隐式**: 所有字段都应在 Schema 中声明

**修复检查清单**:
```markdown
- [ ] 识别该技能的所有不一致字段
- [ ] 确定每个字段的正确默认值
- [ ] 修改 `config_schema` 添加缺失的 `default`
- [ ] 或修改 `get_default_config` 匹配 Schema
- [ ] 更新 `__init__.py` 中的类型注解（如需要）
- [ ] 运行单技能测试: `python -c "from cloudpss_skills_v2 import get_skill; s = get_skill('{skill_name}'); print(s().config_schema); print(s().get_default_config())"`
- [ ] 提交并标记完成
```

**示例修复**:
```python
# 修复前
def config_schema(self) -> dict[str, Any]:
    return {
        "properties": {
            "model": {
                "properties": {
                    "rid": {"type": "string"},  # 缺少 default
                },
            },
        },
    }

def get_default_config(self) -> dict[str, Any]:
    return {
        "model": {"rid": ""},  # 有值但 Schema 未声明
    }

# 修复后
def config_schema(self) -> dict[str, Any]:
    return {
        "properties": {
            "model": {
                "properties": {
                    "rid": {"type": "string", "default": ""},  # 添加 default
                },
            },
        },
    }

def get_default_config(self) -> dict[str, Any]:
    return {
        "model": {"rid": ""},  # 保持不变
    }
```

#### 1.4 验证检查点

| 检查点 | 验证命令 | 通过标准 |
|--------|----------|----------|
| 批次 1 完成 | `python scripts/validate_schema_defaults.py` | 核心技能全绿 |
| 批次 2 完成 | `python scripts/validate_schema_defaults.py` | 高级分析技能全绿 |
| 批次 3 完成 | `python scripts/validate_schema_defaults.py` | 所有技能全绿 |
| 集成测试 | `pytest tests/test_*_integration.py --run-integration -m "not slow_emt"` | 100% 通过 |

---

### 阶段 2: 架构改进（Week 2）

#### 2.1 统一错误处理

**目标**: 所有技能使用统一的错误转换格式

**实现步骤**:
1. 创建 `cloudpss_skills_v2/core/error_utils.py`
2. 定义异常类和转换函数
3. 修改 `PowerAnalysisBase.run()` 基类方法
4. 批量更新所有技能的错误处理

**验证方式**:
```python
# 测试：故意传入无效配置，检查返回的 SkillResult
from cloudpss_skills_v2 import get_skill

skill = get_skill('power_flow')()
result = skill.run({})  # 空配置
assert result.status == 'failed'
assert 'error' in result.to_dict()
assert result.logs  # 有错误日志
```

#### 2.2 类型注解完善

**目标**: 消除 mypy 错误，提高代码可维护性

**文件清单**:
- `cloudpss_skills_v2/core/skill_result.py`
- `cloudpss_skills_v2/powerapi/base.py`
- `cloudpss_skills_v2/poweranalysis/base.py`
- `cloudpss_skills_v2/powerskill/power_flow.py`
- `cloudpss_skills_v2/powerskill/emt.py`

**验证命令**:
```bash
pyright cloudpss_skills_v2/core/
pyright cloudpss_skills_v2/powerapi/
pyright cloudpss_skills_v2/poweranalysis/
```

---

### 阶段 3: 测试覆盖提升（Week 3）

#### 3.1 测试策略

| 测试类型 | 当前覆盖 | 目标覆盖 | 新增测试数 |
|----------|----------|----------|------------|
| Schema 测试 | 0% | 100% | 48 个 |
| 配置验证测试 | 20% | 80% | ~30 个 |
| 集成测试 | 30% | 60% | ~15 个 |
| Mock 测试 | 10% | 50% | ~20 个 |

#### 3.2 Schema 测试模板

每个技能需添加 `tests/test_{skill}_schema.py`:

```python
"""Test {skill_name} schema and default config consistency."""
import pytest
from cloudpss_skills_v2 import get_skill


class Test{SkillName}Schema:
    """Test suite for {skill_name} configuration schema."""

    @pytest.fixture
    def skill(self):
        return get_skill('{skill_name}')()

    def test_schema_has_required_fields(self, skill):
        """Schema should define all required fields."""
        schema = skill.config_schema
        assert 'type' in schema
        assert schema['type'] == 'object'

    def test_default_config_matches_schema(self, skill):
        """Default config values should match schema defaults."""
        schema = skill.config_schema
        config = skill.get_default_config()

        # Check all config keys are in schema
        for key in config:
            assert key in schema.get('properties', {}), f"'{key}' missing in schema"

    def test_validate_rejects_invalid_config(self, skill):
        """Validation should reject invalid configurations."""
        is_valid, errors = skill.validate({})
        assert not is_valid
        assert errors  # Should have error messages
```

#### 3.3 验证检查点

```bash
# 检查测试覆盖
pytest --cov=cloudpss_skills_v2 --cov-report=html --cov-report=term-missing

# 目标：核心模块达到 75%
# cloudpss_skills_v2/core/     : 75%+
# cloudpss_skills_v2/powerapi/ : 70%+
# cloudpss_skills_v2/powerskill/ : 60%+
```

---

### 阶段 4: 文档与工程化（Week 4）

#### 4.1 API 文档生成

**目标**: 使用 Sphinx 自动生成 API 文档

**步骤**:
1. 安装 Sphinx 和相关主题
2. 创建 `docs/api/` 目录结构
3. 配置 `conf.py` 支持 Google/NumPy 风格 docstring
4. 生成并部署 HTML 文档

**验证**:
```bash
cd docs/api
make html
# 检查 _build/html/ 目录生成成功
```

#### 4.2 CI 增强

**新增 CI Job**:

```yaml
# .github/workflows/ci.yml 新增
schema_validation:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    - run: pip install -e ".[dev]"
    - run: python scripts/validate_schema_defaults.py
      env:
        VALIDATE_STRICT: true  # 新增环境变量，严格模式

type_check:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - run: pip install -e ".[dev]"
    - run: pyright cloudpss_skills_v2/ --outputjson
```

#### 4.3 预提交钩子

创建 `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: local
    hooks:
      - id: schema-validation
        name: Validate skill schemas
        entry: python scripts/validate_schema_defaults.py
        language: python
        pass_filenames: false
        always_run: true
```

#### 4.4 依赖管理迁移

将项目配置迁移到 `pyproject.toml`（PEP 621 标准）:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "cloudpss-skills-v2"
version = "2.0.0"
description = "CloudPSS SkillHub V2 - Power System Simulation Framework"
readme = "README.md"
license = {file = "LICENSE"}
requires-python = ">=3.10"
dependencies = [
    "pydantic>=2.0",
    "httpx>=0.24",
    # ...
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "pyright>=1.1",
    "ruff>=0.3",
    # ...
]

[tool.pyright]
include = ["cloudpss_skills_v2"]
exclude = ["**/__pycache__", "**/tests"]
strict = ["cloudpss_skills_v2/core"]
```

---

## 三、执行时间表

### 甘特图概览

```
Week 1: [====Schema修复====]
       Day 1-2: 核心技能 (8个)
       Day 3-4: 高级分析 (15个)
       Day 5-7: 其他技能 (23个)

Week 2: [====架构改进====]
       Day 1-2: 错误处理统一
       Day 3-4: 类型注解完善
       Day 5-7: 集成测试验证

Week 3: [====测试覆盖====]
       Day 1-3: Schema 测试 (48个)
       Day 4-5: 集成测试补充
       Day 6-7: Mock 测试完善

Week 4: [====工程化====]
       Day 1-2: API 文档
       Day 3-4: CI/预提交
       Day 5-6: 依赖迁移
       Day 7:  最终验证
```

---

## 四、验收标准

### 4.1 功能验收

| 检查项 | 验收标准 | 验证方式 |
|--------|----------|----------|
| Schema 一致性 | 48/48 技能通过 | `validate_schema_defaults.py` 返回 0 |
| 向后兼容 | 现有配置都能运行 | 运行所有集成测试 |
| 错误处理 | 所有技能统一格式 | 检查 5 个技能的异常输出 |
| 类型检查 | 0 mypy 错误 | `pyright cloudpss_skills_v2/` |

### 4.2 质量验收

| 检查项 | 目标值 | 验证方式 |
|--------|--------|----------|
| 测试覆盖率 | ≥75% | `pytest --cov` |
| 代码风格 | 0 ruff 错误 | `ruff check cloudpss_skills_v2/` |
| 文档完整度 | 100% 技能有示例 | 检查 `docs/skills/*.md` |
| CI 通过率 | 100% | GitHub Actions 全绿 |

---

## 五、附录

### A. 自动化脚本

```bash
#!/bin/bash
# scripts/improvement/run_batch.sh - 批量执行修复

BATCH=$1  # batch1, batch2, batch3
SKILLS_FILE="scripts/improvement/${BATCH}_skills.txt"

echo "Starting $BATCH..."

while read -r skill; do
    echo "Processing: $skill"
    python scripts/improvement/fix_skill_schema.py "$skill"
    if [ $? -eq 0 ]; then
        git add -A
        git commit -m "fix($skill): align schema with default config"
    else
        echo "FAILED: $skill"
        exit 1
    fi
done < "$SKILLS_FILE"

echo "$BATCH complete!"
python scripts/validate_schema_defaults.py
```

### B. 技能分类清单

**批次 1 - 核心技能 (8个)**:
```
power_flow
n1_security
short_circuit
emt_simulation
transient_stability
voltage_stability
contingency_analysis
batch_powerflow
```

**批次 2 - 高级分析 (15个)**:
```
param_scan
loss_analysis
harmonic_analysis
small_signal_stability
frequency_response
disturbance_severity
protection_coordination
thevenin_equivalent
dudv_curve
orthogonal_sensitivity
transient_stability_margin
fault_clearing_scan
fault_severity_scan
maintenance_security
n2_security
```

**批次 3 - 其他技能 (23个)**:
```
auto_channel_setup
auto_loop_breaker
batch_task_manager
compare_visualization
component_catalog
comtrade_export
config_batch_runner
dynamic_stability
emt_fault_study
emt_n1_screening
fourier_analysis
frequency_scan
model_comparison
model_merge
model_validation
monte_carlo
power_quality_analysis
powerflow_comparison
reactive_compensation_design
renewable_integration
snapshot_manager
vsi_weak_bus
workbench_helper
```

### C. 回滚检查清单

```markdown
## 回滚前检查
- [ ] 已确定问题引入的提交哈希
- [ ] 已评估回滚影响（是否有后续依赖提交）
- [ ] 已通知团队成员

## 回滚步骤
1. `git log --oneline -10` 确认目标提交
2. `git revert <commit-hash>` 或 `git reset --hard <commit-hash>`
3. `git push --force-with-lease` （如需要强制推送）
4. 运行完整测试套件验证

## 回滚后验证
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] Schema 检查通过
```

---

**计划编制**: Claude Code  
**审批状态**: 待用户审批  
**开始条件**: 用户确认计划后创建对应分支
