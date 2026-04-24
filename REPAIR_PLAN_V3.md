# CloudPSS SkillHub 修复与实现计划 V3

> **版本**: 3.0 (纳入审查反馈)  
> **更新日期**: 2026-04-23  
> **核心理念**: 坚持实现既定设计目标，安全可控地修复  
> **预计工期**: 14-16 周 (含 2 周缓冲)  
> **审查评分**: 6.5/10 → 目标 8.5/10

---

## 📋 执行摘要

### 审查反馈整合
针对第三方审查报告中的 14 项问题，本版本已做以下关键修订：

1. ✅ **新增代码目录基线** - 消除路径歧义
2. ✅ **建立测试处置决策矩阵** - 避免误删有价值的测试
3. ✅ **重写安全修复方案** - 修复方案本身的安全问题
4. ✅ **重估 Phase 3 工期** - 2天→4天，4天→8天等
5. ✅ **补充文档同步检查清单** - README/CLI/示例/配置一致性
6. ✅ **增加测试分层模型** - unit/integration/live/smoke 分层策略
7. ✅ **增加阶段退出条件** - 未达基线不得进入下一阶段
8. ✅ **增加 2 周缓冲时间** - 应对返工和延期风险

### 调整后的时间表

```
Week 1-2:   [Phase 1] ████████████████████ 清理虚假测试 (保守策略)
Week 3-4:   [Phase 2] ████████████████████ 修复核心缺陷 (安全方案)
Week 5-12:  [Phase 3] ████████████████████████████████████████ 实现未完成技能 (工期翻倍)
Week 13-14: [Phase 4] ████████████████████ 提升测试质量
Week 15-16: [Phase 5] ████████████████████ 回归验证与文档 (含缓冲)
```

---

## 🏗️ 基础：代码目录与测试分层基线

### 1.1 代码目录基线

在开始任何修复前，必须明确以下目录结构：

```
/home/chenying/researches/cloudpss-toolkit/
├── cloudpss_skills/              # ⚠️ 历史遗留，逐步迁移中
│   ├── builtin/                  # 旧版技能实现
│   ├── core/                     # 核心框架
│   └── ...
│
├── cloudpss_skills_v2/           # ✅ 当前主代码目录 (v2 版本)
│   ├── poweranalysis/            # 30+ 分析技能
│   │   ├── n1_security.py
│   │   ├── emt_n1_screening.py
│   │   └── ...
│   ├── powerapi/                 # API 适配层
│   │   ├── adapters/
│   │   │   ├── cloudpss/
│   │   │   └── pandapower/
│   │   └── registry.py
│   ├── powerskill/               # 技能预设
│   ├── tools/                    # 工具层
│   │   ├── comtrade_export.py    # TODO: 待实现
│   │   ├── hdf5_export.py        # TODO: 待实现
│   │   ├── study_pipeline.py     # TODO: 待实现
│   │   └── ...
│   ├── libs/                     # 共享库
│   │   ├── data_lib/
│   │   ├── model_lib/
│   │   └── workflow_lib/
│   ├── core/                     # 核心框架
│   └── tests/                    # v2 版本测试
│       ├── powerapi_tests/       # ⚠️ 大量空测试类
│       ├── powerskill_tests/
│       └── test_*.py             # ⚠️ 200+ 冒烟测试
│
├── tests/                        # 根目录测试 (主测试套件)
│   ├── test_*.py                 # 92 个测试文件
│   ├── test_all_skills_real.py   # ⚠️ 返回代替断言
│   └── conftest.py
│
├── docs/                         # 文档
│   ├── IMPLEMENTATION_PLAN.md    # ✅ 设计文档
│   ├── guides/
│   └── skills/
│
├── examples/                     # 示例代码
├── configs/                      # 配置示例
└── README.md                     # 公开接口承诺
```

**关键决策**:
- 主代码目录: `cloudpss_skills_v2/` (所有新开发在此)
- 历史代码: `cloudpss_skills/` (逐步迁移，本次不删除)
- 主测试目录: `tests/` (Phase 1 重点清理对象)
- v2 测试目录: `cloudpss_skills_v2/tests/` (Phase 1 清理对象)

---

### 1.2 测试分层模型

所有测试必须按以下分层归类：

| 层级 | 定义 | 运行时机 | 成功率目标 | 标记 |
|------|------|---------|-----------|------|
| **Unit** | 本地可重复，无网络，快速 (<1s) | PR 必跑 | 100% | `@pytest.mark.unit` |
| **Integration** | 允许 mock 或本地依赖 | PR 必跑 | 100% | `@pytest.mark.integration` |
| **Live** | 真实 CloudPSS 服务，需 token | Nightly | >90% | `@pytest.mark.live` |
| **Smoke** | 仅验证存活性，无业务逻辑验证 | CI 快速检查 | 不强制 | `@pytest.mark.smoke` |

**CI 运行策略**:

```yaml
# .github/workflows/ci.yml
jobs:
  unit-and-integration:
    runs-on: ubuntu-latest
    steps:
      - run: pytest tests/ -m "unit or integration" -v --cov
    # PR 必跑，100% 通过

  live-smoke:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - run: pytest tests/ -m "live and not slow" -v
    # main 分支 nightly，>90% 通过

  full-regression:
    runs-on: ubuntu-latest
    if: github.event_name == 'release'
    steps:
      - run: pytest tests/ -m "live" -v
    # 发布前手动触发，>85% 通过
```

---

### 1.3 测试处置决策矩阵

Phase 1 必须按以下矩阵处理每个测试：

| 类别 | 判定标准 | 处理方式 | 审批要求 | 留痕要求 |
|------|---------|---------|---------|---------|
| **完全空类** | 只有 `class TestX:` + `pass` | **删除** | 单人审批 | PR 中标注 "empty placeholder" |
| **永久跳过** | `pytest.skip()` 无条件执行 | **修复** | 技能存在则修复，不存在则删除 | 记录 issue 链接 |
| **仅属性检查** | 只检查 `hasattr(obj, 'name')` | **标记保留** | 标记为 `@pytest.mark.smoke` + `@pytest.mark.needs_improvement` | 创建改进任务 |
| **返回代替断言** | 函数返回 bool 而非 assert | **修复** | 修改为 assert | 关联修复 PR |
| **顺序依赖** | 依赖其他测试的输出 | **重构** | 改为 fixture 提供依赖 | 记录重构方法 |
| **不稳定** | 含 `time.sleep()` 或随机性 | **重构** | 使用指数退避或 mock | 记录不稳定原因 |

**禁止行为**:
- ❌ 不得仅因"测试质量差"就删除功能测试
- ❌ 不得删除后不留痕（必须关联 issue/PR）
- ❌ 不得把永久跳过测试算作"有效覆盖"

---

## 🎯 Phase 1: 清理虚假测试 (Week 1-2)

### 修订后的目标
从"激进删除 340+ 测试"改为"**保守治理，保护有价值的回归资产**"

**数量目标修订**:

| 类型 | 修订前目标 | 修订后目标 | 原因 |
|------|-----------|-----------|------|
| 完全空类 | 删除 90+ | 删除 90+ | 这些确实无价值 |
| 永久跳过 | 修复或删除 48 | 修复 48 | 技能存在，应修复而非删除 |
| 冒烟测试 | 标记保留 200+ | 标记保留 200+ | Phase 4 逐步改进 |
| 总计 | 1000+ → 300-400 | 1000+ → 600-700 | 保留更多有价值的测试 |

---

### Week 1: 删除完全空类 (90+ 测试类)

**任务 1.1: 删除占位符测试类**

这些测试类只有定义，无任何实际代码：

**删除清单**:

```bash
# cloudpss_skills_v2/tests/powerapi_tests/ (16 个空类)
cloudpss_skills_v2/tests/powerapi_tests/test_base.py
  - TestValidationResult (34-35)
  - TestSimulationResult (39-40)
  - TestEngineAdapter (44-45)
  - TestTimeoutHandling (59-60)
  - TestErrorHandling (64-65)
  - TestValidationEdgeCases (69-70)
  - TestSimulationResultEdgeCases (74-75)

cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py
  - 6 个空类 (7-33)

cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py
  - 6 个空类 (7-33)

# cloudpss_skills_v2/tests/ (74 个空类)
cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py (3 个)
cloudpss_skills_v2/tests/skills/test_power_flow.py (4 个)
cloudpss_skills_v2/tests/test_auto_channel_setup.py (4 个)
cloudpss_skills_v2/tests/test_cloudpss_converter.py (2 个)
cloudpss_skills_v2/tests/test_comtrade_export.py (3 个)
cloudpss_skills_v2/tests/test_contingency_analysis.py (5 个)
cloudpss_skills_v2/tests/test_data_lib.py (8 个)
cloudpss_skills_v2/tests/test_hdf5_export.py (4 个)
cloudpss_skills_v2/tests/test_maintenance_security.py (5 个)
cloudpss_skills_v2/tests/test_n2_security.py (5 个)
cloudpss_skills_v2/tests/test_orthogonal_sensitivity.py (7 个)
cloudpss_skills_v2/tests/test_output_standard.py (4 个)
cloudpss_skills_v2/tests/test_skill_config_integrity.py (3 个)
cloudpss_skills_v2/tests/test_skills_integration.py (6 个)
cloudpss_skills_v2/tests/test_vsi_weak_bus.py (6 个)
```

**执行步骤**:

```bash
# 1. 创建删除分支
git checkout -b cleanup/phase-1-remove-empty-tests

# 2. 删除文件 (不是清空，是 git rm)
git rm cloudpss_skills_v2/tests/powerapi_tests/test_base.py
git rm cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py
git rm cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py
git rm cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py
# ... 其他文件

# 3. 检查导入影响
grep -r "from.*test_base import" cloudpss_skills_v2/
grep -r "from.*test_edge_cases import" cloudpss_skills_v2/

# 4. 提交并标注
git commit -m "cleanup(phase-1): Remove 90+ empty placeholder test classes

- Remove completely empty test classes (only 'pass' statements)
- These provided false confidence in coverage reports
- No functional code was removed
- See issue #123 for full list"
```

**验收标准 (修订后)**:
- [ ] 90 个空测试类已删除
- [ ] pytest 收集不再显示这些测试
- [ ] 没有破坏其他测试的导入
- [ ] 删除记录已留痕（PR 描述 + issue 链接）

---

### Week 1 (续): 修复永久跳过测试 (48 个测试)

**修订策略**: 从"删除或修复"改为"**全部修复**"

**任务 1.2: 修复永久跳过测试**

这些测试使用 `pytest.skip("Class requires constructor arguments")` 永久跳过。

**分析**:
- 24 个文件，每个文件 2 个测试
- 被测技能都存在且有实际功能
- **决策**: 修复而非删除

**修复方法**:

```python
# 修复前 (test_algo_lib.py)
class TestNewtonRaphsonSolver:
    def test_instantiation(self):
        pytest.skip("Class requires constructor arguments")  # ❌ 永久跳过

# 修复后
class TestNewtonRaphsonSolver:
    def test_instantiation(self):
        # ✅ 提供必要的构造函数参数
        solver = NewtonRaphsonSolver(
            max_iterations=100,
            tolerance=1e-6
        )
        assert solver is not None
        assert solver.max_iterations == 100
```

**修复清单**:

| 文件 | 测试数量 | 所需构造函数参数 |
|------|---------|----------------|
| test_algo_lib.py | 2 | max_iterations, tolerance |
| test_auto_loop_breaker.py | 2 | model, config |
| test_batch_powerflow.py | 2 | models, algorithm |
| test_batch_task_manager.py | 2 | tasks, max_workers |
| test_compare_visualization.py | 2 | sources, config |
| test_component_catalog.py | 2 | server, token |
| test_config_batch_runner.py | 2 | configs, base_config |
| test_fault_severity_scan.py | 2 | model, fault_config |
| test_harmonic_analysis.py | 2 | model, harmonic_config |
| test_integration_datalib.py | 2 | data_type, values |
| test_loss_analysis.py | 2 | model, result |
| test_model_builder.py | 2 | base_model, operations |
| test_model_hub.py | 2 | servers, cache_config |
| test_model_lib.py | 2 | topology, parameters |
| test_model_parameter_extractor.py | 2 | model, component_types |
| test_n1_security.py | 2 | model, branch_list |
| test_param_scan.py | 2 | model, param_config |
| test_parameter_sensitivity.py | 2 | model, sensitivity_config |
| test_power_quality_analysis.py | 2 | model, quality_config |
| test_protection_coordination.py | 2 | model, protection_config |
| test_reactive_compensation_design.py | 2 | model, compensation_config |
| test_transient_stability_margin.py | 2 | model, stability_config |
| test_voltage_stability.py | 2 | model, stability_config |
| test_workflow_lib.py | 2 | steps, context |

**验收标准**:
- [ ] 48 个永久跳过测试已修复
- [ ] 所有测试可以正常运行（不跳过）
- [ ] 测试覆盖率提升 > 5%
- [ ] 修复记录已留痕

---

### Week 2: 标记和改进冒烟测试 (200+ 测试)

**任务 1.3: 标记无意义冒烟测试**

这些测试只验证导入、实例化、属性存在，不验证业务逻辑。

**处理方式**: 不删除，而是**标记并创建改进任务**

```python
# 标记前
class TestDisturbanceSeverityAnalysis:
    def test_import(self):
        import disturbance_severity
        assert True

# 标记后
@pytest.mark.smoke
@pytest.mark.needs_improvement(
    reason="仅验证导入，需添加业务逻辑验证",
    issue="https://github.com/org/repo/issues/456"
)
class TestDisturbanceSeverityAnalysis:
    def test_import(self):
        import disturbance_severity
        assert True
```

**标记范围**:
- cloudpss_skills_v2/tests/test_disturbance_severity.py (8 个)
- cloudpss_skills_v2/tests/test_dudv_curve.py (12 个)
- cloudpss_skills_v2/tests/test_emt_n1_screening.py (9 个)
- cloudpss_skills_v2/tests/test_fault_clearing_scan.py (7 个)
- cloudpss_skills_v2/tests/test_frequency_response.py (6 个)
- cloudpss_skills_v2/tests/test_renewable_integration.py (6 个)
- cloudpss_skills_v2/tests/test_small_signal_stability.py (6 个)
- cloudpss_skills_v2/tests/test_transient_stability.py (6 个)
- ... 共 200+ 个

**同时创建改进任务**:

```markdown
## 改进任务: 提升冒烟测试质量

### Priority 1 (Week 13-14)
- [ ] test_disturbance_severity.py - 添加业务逻辑验证
- [ ] test_dudv_curve.py - 添加曲线计算验证
- [ ] test_emt_n1_screening.py - 添加筛选逻辑验证

### Priority 2 (后续迭代)
- [ ] test_frequency_response.py - 添加频率响应验证
- [ ] test_renewable_integration.py - 添加新能源验证
...
```

**验收标准**:
- [ ] 200+ 个冒烟测试已标记
- [ ] 改进任务清单已创建
- [ ] CI 可以过滤这些测试 (`-m "not needs_improvement"`)

---

### Week 2 (续): 修复返回代替断言 (5 个测试)

**任务 1.4: 修复返回代替断言**

| 文件 | 行号 | 问题 | 修复方式 |
|------|------|------|---------|
| tests/test_all_skills_real.py | 40-58 | 返回 (bool, message) | 修改为 assert 语句 |
| tests/param_scan_emt_test.py | 66 | 返回 False | 修改为 assert False |
| tests/param_scan_emt_test.py | 191 | 返回 success_count > 0 | 修改为 assert success_count > 0 |
| tests/test_emt_fault_core_unit.py | 14 | assert False | 修复为正常异常测试 |
| tests/test_emt_fault_core_unit.py | 22 | assert False | 修复为正常异常测试 |
| tests/test_emt_measurement_core_unit.py | 259 | assert False | 修复为正常异常测试 |

**修复示例**:

```python
# 修复前
def test_skill_config(self):
    result = validate_config(config)
    return (result.valid, result.message)  # ❌ 返回而不是断言

# 修复后
def test_skill_config(self):
    result = validate_config(config)
    assert result.valid, f"Config invalid: {result.message}"  # ✅ 断言
```

---

### Phase 1 里程碑检查点 (修订后)

```bash
# 检查点 1.1: 空测试类已删除
pytest cloudpss_skills_v2/tests/powerapi_tests/ --collect-only 2>&1 | grep -i "test" | wc -l
# 预期: 0 (powerapi_tests 目录为空或删除)

# 检查点 1.2: 永久跳过测试已修复
pytest cloudpss_skills_v2/tests/test_algo_lib.py -v 2>&1 | grep -i "skip"
# 预期: 无 skip 输出

# 检查点 1.3: 冒烟测试已标记
grep -r "@pytest.mark.needs_improvement" cloudpss_skills_v2/tests/ | wc -l
# 预期: 200+

# 检查点 1.4: 总测试数
pytest tests/ cloudpss_skills_v2/tests/ --collect-only -q 2>&1 | tail -1
# 预期: 600-700 个测试 (修订前目标是 300-400，修订后是 600-700)

# 检查点 1.5: 阶段退出条件
# - 空测试类删除率: 100%
# - 永久跳过测试修复率: 100%
# - 冒烟测试标记率: 100%
# - 导入破坏: 0
```

**阶段退出条件 (新增)**:

```markdown
Phase 1 退出检查清单:
- [ ] 90 个空测试类已删除 (100%)
- [ ] 48 个永久跳过测试已修复 (100%)
- [ ] 200+ 个冒烟测试已标记 (100%)
- [ ] 5 个返回代替断言已修复 (100%)
- [ ] 无导入破坏 (pytest --collect-only 通过)
- [ ] 代码审查通过

⚠️ **未达基线不得进入 Phase 2**
```

---

## 🔧 Phase 2: 修复核心缺陷 (Week 3-4)

### 修订后的安全修复方案

针对审查报告中指出的安全修复方案本身的问题，以下是修订后的方案：

---

#### 任务 2.1: 修复路径遍历漏洞 (修订方案)

**问题文件**: `tools/visualize.py` (100-103 行)

**修订前方案的问题**:
```python
# ❌ 不安全：startswith 可被绕过
if path.startswith("/data"):  # /data_evil 也能通过
```

**修订后方案**:

```python
import os
from pathlib import Path

def validate_data_path(user_input: str) -> Path:
    """
    验证并规范化用户输入的数据文件路径
    
    安全要求：
    1. 必须是绝对路径
    2. 必须在允许的目录内
    3. 必须是文件（不是目录）
    4. 必须是 .csv, .json, .h5 格式
    5. 文件必须存在
    """
    # 允许的根目录
    ALLOWED_ROOTS = [
        Path("/data").resolve(),
        Path("/results").resolve(),
        Path.home() / "cloudpss_data",  # 用户目录
    ]
    
    # 允许的文件扩展名
    ALLOWED_EXTENSIONS = {'.csv', '.json', '.h5', '.hdf5'}
    
    try:
        # 1. 解析路径
        path = Path(user_input).resolve()
        
        # 2. 检查路径是否在允许范围内
        is_allowed = any(
            path.is_relative_to(root) 
            for root in ALLOWED_ROOTS
        )
        if not is_allowed:
            raise ValueError(
                f"Path {path} is outside allowed directories: {ALLOWED_ROOTS}"
            )
        
        # 3. 检查文件扩展名
        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            raise ValueError(
                f"File extension {path.suffix} not allowed. "
                f"Use: {ALLOWED_EXTENSIONS}"
            )
        
        # 4. 检查路径是否存在路径遍历攻击
        # resolve() 已经处理了 ../ 等，但双重检查
        if ".." in user_input:
            raise ValueError("Path traversal detected")
        
        # 5. 检查是否是文件
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")
        
        return path
        
    except (ValueError, OSError) as e:
        raise ValueError(f"Invalid path: {e}")

# 使用
config_path = validate_data_path(config["source"]["data_file"])
with open(config_path, 'r') as f:
    data = f.read()
```

**安全测试**:

```python
def test_path_validation():
    # 合法路径
    assert validate_data_path("/data/results.csv").exists()
    
    # 非法路径 - 路径遍历
    with pytest.raises(ValueError):
        validate_data_path("/data/../../../etc/passwd")
    
    # 非法路径 - 不在允许范围
    with pytest.raises(ValueError):
        validate_data_path("/etc/passwd")
    
    # 非法路径 - 扩展名不允许
    with pytest.raises(ValueError):
        validate_data_path("/data/script.py")
```

---

#### 任务 2.2: 修复 Token 路径安全 (修订方案)

**问题文件**: 
- `powerapi/adapters/cloudpss/powerflow.py` (142-152)
- `powerapi/adapters/cloudpss/short_circuit.py` (278-283)
- `powerapi/adapters/cloudpss/emt.py` (277-287)

**修订前方案的问题**:
```python
# ❌ 问题：硬编码系统路径，部署耦合
token = Path("/etc/cloudpss/token").read_text()
```

**修订后方案**:

```python
import os
from pathlib import Path
from typing import Optional

class TokenManager:
    """
    Token 管理器 - 安全的 token 获取策略
    
    优先级：
    1. 显式配置 (最安全)
    2. 环境变量
    3. 用户本地配置文件
    4. 当前工作目录 .cloudpss_token (仅开发)
    """
    
    @staticmethod
    def get_token(config: Optional[dict] = None) -> str:
        """获取 token，按优先级尝试"""
        
        # 1. 显式配置 (最高优先级)
        if config and config.get("token"):
            return config["token"]
        
        # 2. 环境变量
        if os.environ.get("CLOUDPSS_TOKEN"):
            return os.environ["CLOUDPSS_TOKEN"]
        
        # 3. 用户本地配置文件
        user_config = Path.home() / ".cloudpss" / "config"
        if user_config.exists():
            import json
            with open(user_config) as f:
                cfg = json.load(f)
                if cfg.get("token"):
                    return cfg["token"]
        
        # 4. 开发环境：当前工作目录
        dev_token = Path(".cloudpss_token")
        if dev_token.exists():
            # 警告：不要在生产环境使用
            import warnings
            warnings.warn("Using dev token from current directory")
            return dev_token.read_text().strip()
        
        raise ValueError(
            "No CloudPSS token found. Provide via: "
            "config['token'], CLOUDPSS_TOKEN env var, "
            "or ~/.cloudpss/config"
        )
    
    @staticmethod
    def validate_token(token: str) -> bool:
        """验证 token 格式"""
        if not token or len(token) < 10:
            return False
        # 可以添加更多格式验证
        return True

# 使用
token = TokenManager.get_token(config.get("auth"))
if not TokenManager.validate_token(token):
    raise ValueError("Invalid token format")
```

---

#### 任务 2.3: 修复全局环境变量竞争 (修订方案)

**问题文件**:
- `powerapi/adapters/cloudpss/powerflow.py` (136-140)
- `powerapi/adapters/cloudpss/short_circuit.py` (273-277)
- `powerapi/adapters/cloudpss/emt.py` (271-275)

**修订前方案的问题**:
```python
# ❌ 问题：threading.local() 不能解决 os.environ 的进程级共享
import threading
_local = threading.local()
# os.environ 仍是进程级共享，threading.local 无效
```

**修订后方案**:

**策略**: 改造下游 API，**显式传 token**，不依赖全局环境变量

```python
# 方案 1: 封装 CloudPSS SDK 调用，显式传 token
class CloudPSSAdapter:
    """
    CloudPSS 适配器 - 隔离全局状态
    """
    
    def __init__(self, token: str, api_url: Optional[str] = None):
        self.token = token
        self.api_url = api_url or "https://www.cloudpss.net/"
        # 不再修改 os.environ，而是保存为实例属性
    
    def connect(self) -> bool:
        """连接，使用实例属性而非全局环境变量"""
        # 如果 SDK 支持显式传 token
        from cloudpss import Client
        self.client = Client(token=self.token, base_url=self.api_url)
        return True
        
        # 如果 SDK 强制使用环境变量，则使用进程隔离
        # 见方案 2
    
    def run_powerflow(self, model_rid: str) -> dict:
        """执行潮流计算"""
        model = self.client.fetch(model_rid)
        job = model.run_powerflow()
        return job.result()

# 使用
adapter = CloudPSSAdapter(token="xxx")
result = adapter.run_powerflow("model/holdme/IEEE39")
```

**方案 2: 如果 SDK 强制使用环境变量，使用进程隔离**:

```python
import multiprocessing
from typing import Dict, Any

def _run_in_isolated_process(token: str, api_url: str, task_config: dict) -> dict:
    """
    在隔离进程中运行，避免污染主进程环境变量
    """
    import os
    os.environ["CLOUDPSS_API_URL"] = api_url
    os.environ["CLOUDPSS_TOKEN"] = token
    
    from cloudpss import Model, setToken
    setToken(token)
    
    model = Model.fetch(task_config["model_rid"])
    job = model.run_powerflow()
    result = job.result()
    
    return {
        "buses": result.get_buses(),
        "branches": result.get_branches(),
    }

class IsolatedCloudPSSAdapter:
    """
    使用进程隔离的适配器
    适用于必须修改全局环境变量的场景
    """
    
    def run_powerflow(self, token: str, model_rid: str) -> dict:
        """在隔离进程中执行"""
        with multiprocessing.Pool(1) as pool:
            result = pool.apply(
                _run_in_isolated_process,
                args=(token, self.api_url, {"model_rid": model_rid})
            )
        return result
```

**方案选择**:
- 优先方案 1: 改造 SDK 调用，显式传参数
- 备选方案 2: 如果 SDK 不支持，使用进程隔离
- **禁止**: 继续使用 `os.environ` + `threading.local()` 的错误组合

---

### Phase 2 其他关键修复

#### 任务 2.4: 修复聚合逻辑错误

| 文件 | 行号 | 问题 | 修复 |
|------|------|------|------|
| poweranalysis/n1_security.py | 254-261 | case_violations 被覆盖 | 改为 extend() 追加 |
| poweranalysis/emt_n1_screening.py | 149-159 | 从未实际执行故障 | 添加 actual_trip 逻辑 |
| poweranalysis/loss_analysis.py | 314-323 | 0.0 被误判为缺失 | 使用 is None 检查 |

#### 任务 2.5: 同类缺陷模式扫描 (新增)

**审查反馈要求**: 不仅修复已知缺陷，还要系统扫描同类问题

```bash
# 搜索模式 1: 数值误判 (0.0 被当作 False)
grep -rn "if not \w\+:" cloudpss_skills_v2/poweranalysis/ --include="*.py" | grep -v "__pycache__"

# 搜索模式 2: 结果字段错配
grep -rn "result\[.*\] = .*" cloudpss_skills_v2/poweranalysis/ --include="*.py" | head -20

# 搜索模式 3: 循环内覆盖集合
grep -rn "for.*in.*:" -A 5 cloudpss_skills_v2/poweranalysis/ --include="*.py" | grep -B 5 "= \[\]"
```

**执行**: 将这些搜索结果纳入修复范围

**2026-04-23 扫描结果（cleanup/phase-1-remove-empty-tests 分支）**:

| 模式 | 扫描范围 | 结果摘要 | 需要立即修复 |
|------|----------|----------|--------------|
| 数值误判 (`if not x:`) | `poweranalysis/`, `powerapi/` | 命中较多，但大多数是配置/列表判空；确认 1 个已知真缺陷 (`loss_analysis.py:314-323`) 与 3 个需跟踪的并发/认证判空点 | **是（部分）** |
| 结果字段错配 (`result[...] = ...`) | `poweranalysis/`, `powerapi/` | `poweranalysis/contingency_analysis.py` 命中 9 处，当前未发现字段名错配；`powerapi/adapters/cloudpss/powerflow.py` 中 6 处为字段标准化映射，属正常逻辑 | 否 |
| 循环内覆盖集合 | `poweranalysis/`, `powerapi/` | 确认 1 个已知真缺陷：`poweranalysis/n1_security.py:254-261` 中 `case_violations` 被重新赋值，覆盖前序电压违规收集 | **是** |
| 路径遍历 | `poweranalysis/`, `powerapi/` | 未发现 `open(user_input)` / `Path(user_input)` 直接消费用户输入的模式；但 `token_file` 路径读取缺少约束，建议作为低优先级安全加固 | 否 |
| 硬编码凭据 | `poweranalysis/`, `powerapi/` | 未发现硬编码 `password/token/api_key` 常量；命中的 `token = auth.get(...)` 为运行时配置读取 | 否 |
| `eval` / `exec` | `poweranalysis/`, `powerapi/` | 未发现 | 否 |
| 并发/环境竞争 | `poweranalysis/`, `powerapi/` | 确认 3 处高风险：`powerapi/adapters/cloudpss/{powerflow,short_circuit,emt}.py` 在 `_setup_auth()` 中写入 `os.environ["CLOUDPSS_API_URL"]`，与 Phase 2 安全目标冲突 | **是** |
| 类型混淆 (`isinstance(x, bool)`) | `poweranalysis/`, `powerapi/` | 未发现 | 否 |

**已确认的真缺陷 / Critical issues**:

1. **聚合覆盖缺陷（P0）**  
   - 文件: `cloudpss_skills_v2/poweranalysis/n1_security.py:254-261`  
   - 问题: `case_violations` 已先 `extend(v_violations)`，随后又被 `case_violations = self._check_voltage_violations(...)` 覆盖，导致前序聚合结果丢失。  
   - 风险: N-1 安全校核结果漏报违规，属于核心分析错误。  
   - Fix ticket: `P2-SCAN-001` - 改为仅追加热稳定违规，不得重新赋值；补充回归测试覆盖“同时存在电压与热稳定违规”场景。

2. **故障筛查未实际施加扰动（P0）**  
   - 文件: `cloudpss_skills_v2/poweranalysis/emt_n1_screening.py:149-159`  
   - 问题: 循环中对每个 contingency 直接重复执行 `api.run_power_flow(model_handle=handle)`，未对模型做 branch trip / actual fault 注入，导致结果并非 N-1 后故障结果。  
   - 风险: EMT N-1 screening 产出“伪分析结果”，业务含义错误。  
   - Fix ticket: `P2-SCAN-002` - 为每个 contingency 生成独立扰动模型并执行真实故障/切除逻辑；增加基线与故障后差异断言。

3. **0.0 数值误判（P0）**  
   - 文件: `cloudpss_skills_v2/poweranalysis/loss_analysis.py:314-323`  
   - 问题: `branch.get("power_loss_mw") or branch.get("Ploss") or ...` 会把合法的 `0.0` 当作假值，误回退到其他字段。  
   - 风险: 线路/变压器损耗计算错误，尤其在零损耗/边界场景下会污染结果。  
   - Fix ticket: `P2-SCAN-003` - 使用 `is None` 链式判空辅助函数替代 `or` 回退；补充 0.0 边界测试。

4. **全局环境变量竞争（P0 / Security）**  
   - 文件:  
     - `cloudpss_skills_v2/powerapi/adapters/cloudpss/powerflow.py:136-140`  
     - `cloudpss_skills_v2/powerapi/adapters/cloudpss/short_circuit.py:273-277`  
     - `cloudpss_skills_v2/powerapi/adapters/cloudpss/emt.py:271-275`  
   - 问题: `_setup_auth()` 通过 `os.environ["CLOUDPSS_API_URL"] = base_url` 切换服务地址，这是进程级全局状态；并发调用不同 server/base_url 时会互相污染。  
   - 风险: 请求串线、跨租户访问错误、并发测试失败；与 Phase 2 “禁止继续使用 `os.environ` + `threading.local()` 错误组合” 的约束直接冲突。  
   - Fix ticket: `P2-SCAN-004` - 优先改为 SDK 显式传递 `baseUrl`；若 SDK 无法完全覆盖，采用进程隔离，不允许在共享进程内覆写全局环境变量。

**已检查但暂未判定为缺陷的命中**:

- `poweranalysis/contingency_analysis.py:305-307, 481, 523-566` 的 `result[...] = ...` 为状态/摘要字段写回，未见字段名错配。  
- `powerapi/adapters/cloudpss/powerflow.py:69-97` 的 `result[...] = ...` 为总线/支路字段标准化映射，逻辑正常。  
- 多数 `if not config / if not valid / if not contingencies / if not target_buses` 属于配置、列表、校验结果判空，不属于 `0.0` 误判。  
- `token_file = auth.get("token_file", ".cloudpss_token")` 相关读取未直接暴露为用户输入拼接型路径遍历，但后续仍建议限制为受信目录或显式校验文件类型。

**建议修复顺序**:

1. 先修 `P2-SCAN-004`（并发/安全基线）  
2. 再修 `P2-SCAN-001` / `P2-SCAN-002`（分析逻辑正确性）  
3. 最后修 `P2-SCAN-003`（数值边界正确性）  
4. 修复后补跑：`pytest tests/test_n1_security.py tests/test_emt_n1_screening.py tests/test_concurrent_adapter.py -v`

---

### Phase 2 里程碑检查点

```bash
# 安全检查
bandit -r cloudpss_skills_v2/poweranalysis cloudpss_skills_v2/powerapi cloudpss_skills_v2/tools -ll
# 预期: 无 High/Critical 问题

# 逻辑测试
pytest tests/test_n1_security.py tests/test_emt_n1_screening.py -v
# 预期: 100% 通过

# 并发测试 (新增)
pytest tests/test_concurrent_adapter.py -v
# 预期: 并发调用不互相干扰
```

**阶段退出条件**:
- [ ] 5+ 安全问题已修复 (100%)
- [ ] 15+ 逻辑错误已修复 (100%)
- [ ] 同类缺陷扫描完成
- [ ] bandit 无 High/Critical 问题
- [ ] 安全修复有单元测试覆盖

---

## 🏗️ Phase 3: 实现未完成技能 (Week 5-12) [工期翻倍]

### 关键修订: 工期重估

| 技能 | 修订前工期 | 修订后工期 | 说明 |
|------|-----------|-----------|------|
| HDF5 Export | 2 天 | **4 天** | 含格式校验、回读测试 |
| COMTRADE Export | 2 天 | **4 天** | 含标准兼容验证 |
| Batch Task Manager | 5 天 | **7 天** | 含依赖图、并发控制 |
| Study Pipeline | 4 天 | **8 天** | 含条件/循环/变量解析 |
| Auto Channel Setup | 4 天 | **5 天** | 含多类型通道 |
| Model Hub | 5 天 | **6 天** | 含多服务器同步 |
| Model Builder | 4 天 | **5 天** | 含类型转换 |
| Compare Visualization | 4 天 | **5 天** | 含雷达图、时序对比 |
| Component Catalog | 3 天 | **4 天** | 含跨服务器搜索 |
| **总计** | **33 天** | **48 天** | **Week 5-12 (8周)** |

---

### Week 5-6: P0 核心数据导出

**任务 3.1: HDF5 Export (修订后，4天)**

**MVP 范围 (明确限定)**:
- ✅ 支持导出基本数据类型 (array, table)
- ✅ 支持元数据 (attrs)
- ✅ 支持读取回 h5py
- ❌ 不支持压缩 (Phase 4 添加)
- ❌ 不支持分块存储 (Phase 4 添加)

**验收标准 (具体可验证)**:
- [ ] 可以导出 IEEE39 潮流结果到 HDF5
- [ ] 导出文件可被 h5py 读取
- [ ] 元数据包含 skill 名称、时间戳、版本
- [ ] 单元测试覆盖率 > 80%
- [ ] 通过 HDF5 验证工具检查格式正确性

---

**任务 3.2: COMTRADE Export (修订后，4天)**

**MVP 范围**:
- ✅ 支持 ASCII 格式 (.cfg + .dat)
- ✅ 支持电压、电流通道
- ✅ 支持时间戳
- ❌ 不支持 BINARY 格式 (Phase 4)
- ❌ 不支持 .cff 合并格式 (Phase 4)

**验收标准**:
- [ ] 生成的 .cfg 和 .dat 文件可通过 COMTRADE 标准解析器读取
- [ ] 可通过第三方工具 (如 SEL Compass) 打开
- [ ] 时间戳精度达到微秒级
- [ ] 单元测试覆盖率 > 80%

---

### Week 7-8: P1 工作流与批处理

**任务 3.3: Study Pipeline (修订后，8天)**

**MVP 范围 (关键限定)**:
- ✅ 支持顺序执行
- ✅ 支持变量引用 (${var})
- ✅ 支持 if 条件
- ❌ 不支持 for_each 循环 (Phase 4)
- ❌ 不支持嵌套 pipeline (Phase 4)

**验收标准**:
- [ ] 可以顺序执行 3 个步骤
- [ ] 步骤 2 可以引用步骤 1 的结果
- [ ] 支持 if: condition 控制步骤执行
- [ ] 失败时停止并报告错误步骤
- [ ] 单元测试覆盖率 > 80%

**分解任务**:
- Day 1-2: 语法定义和解析
- Day 3-4: 执行器实现
- Day 5-6: 变量解析
- Day 7-8: 错误处理和测试

---

### Week 9-12: P2 模型与通道管理

**任务 3.4-3.11**: 其他 8 个技能

每个技能按以下模板执行:

```markdown
### Skill: [名称]
**工期**: X 天
**MVP 范围**: 
- ✅ 支持...
- ❌ 不支持...(Phase 4)

**每日检查点**:
- Day 1: 核心框架
- Day 2: 主要功能
- Day 3: 错误处理
- Day 4: 单元测试

**验收标准**:
- [ ] 具体可验证标准 1
- [ ] 具体可验证标准 2
- [ ] 单元测试覆盖率 > 80%
```

---

### Phase 3 里程碑检查点

```python
# 验证技能实现
python -m cloudpss_skills list | wc -l
# 预期: 48 (所有技能都实现)

# 验证测试覆盖
pytest cloudpss_skills_v2/tests/test_*.py --cov=cloudpss_skills_v2/tools -v
# 预期: 新技能覆盖率 > 75%

# 验证功能
python -c "from cloudpss_skills import get_skill; get_skill('hdf5_export').run({...})"
# 预期: 成功运行
```

---

## 📚 Phase 4: 公开接口一致性 (新增，贯穿全程)

**审查反馈要求**: 不能只在 Phase 5 更新文档，要在 Phase 3 同步执行

### 一致性检查清单

每个技能实现时必须同步检查:

```markdown
### Skill: [名称]
- [ ] **README**: 技能列表已更新
- [ ] **docs/skills/**: 详细文档已添加
- [ ] **examples/**: 使用示例已添加
- [ ] **configs/**: 配置示例已添加
- [ ] **CLI**: cloudpss-skills list 显示正确
- [ ] **Registry**: 注册表已更新
- [ ] **测试**: 单元测试和集成测试已添加
```

---

## ✅ Phase 5: 回归验证 (Week 13-16)

### 包含 2 周缓冲时间

```
Week 13-14: 测试质量提升
Week 15-16: 回归验证 + 缓冲
```

**缓冲用途**:
- 应对 Phase 3 技能实现的延期
- 修复集成测试中发现的问题
- 完善文档和示例

---

## 📊 修订后的成功指标

| 指标 | 修复前 | 修订前目标 | 修订后目标 |
|------|--------|-----------|-----------|
| 总测试数 | ~1000 | ~400 | ~650 |
| 虚假测试 | 340+ | 0 | 0 |
| 永久跳过 | 48 | 0 | 0 |
| 可用技能 | 37/48 | 37/48 (删除11) | **48/48 (全部实现)** |
| 代码覆盖率 | ~45% | >75% | >75% |
| 安全问题 | 5+ High | 0 High | 0 High |
| 工期 | - | 8-10 周 | **14-16 周** |

---

## 🚦 关键决策总结

| 决策 | 修订前 | 修订后 | 原因 |
|------|--------|--------|------|
| 未实现技能 | 部分删除 | **全部实现** | 符合 README 承诺和设计目标 |
| 永久跳过测试 | 删除或修复 | **全部修复** | 保护回归资产 |
| 总测试数 | 300-400 | **600-700** | 保留有价值的冒烟测试 |
| 工期 | 8-10 周 | **14-16 周** | 更现实的估时 |
| 安全方案 | 基础修复 | **严谨方案** | 避免引入新问题 |

---

**计划状态**: 已纳入审查反馈，等待最终审批  
**关键改进**: 保守测试治理 + 实现全部技能 + 严谨安全方案 + 现实工期  
**建议**: 按此版本执行
