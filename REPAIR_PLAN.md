# CloudPSS SkillHub 修复计划

> **版本**: 1.0  
> **创建日期**: 2026-04-23  
> **预计工期**: 8-10 周  
> **优先级**: P0 (虚假测试) > P1 (代码缺陷) > P2 (质量提升)

---

## 📋 执行摘要

### 问题概览
| 类别 | 数量 | 风险等级 |
|------|------|---------|
| 虚假/空测试 | 340+ | 🔴 Critical |
| 未实现技能 | 11 | 🔴 Critical |
| 逻辑错误 | 15+ | 🔴 Critical |
| 安全问题 | 5+ | 🔴 Critical |
| 类型错误 | 10+ | 🟠 High |
| 不稳定测试 | 15+ | 🟠 High |

### 修复目标
1. **Phase 1 (2周)**: 清理虚假测试，建立可信基线
2. **Phase 2 (3周)**: 修复核心逻辑缺陷和安全问题
3. **Phase 3 (2周)**: 实现或删除未完成的技能
4. **Phase 4 (2周)**: 提升测试质量和覆盖率
5. **Phase 5 (1周)**: 全面回归验证和文档更新

---

## 🎯 Phase 1: 清理虚假测试 (Week 1-2)

### 目标
删除或修复 340+ 个问题测试，确保所有测试都是真实有效的。

### 任务清单

#### Week 1: 删除空/占位符测试

**任务 1.1: 删除完全空的测试类 (90+)**
```bash
# 目标文件列表
delete_list=(
  "cloudpss_skills_v2/tests/powerapi_tests/test_base.py"
  "cloudpss_skills_v2/tests/powerapi_tests/test_edge_cases.py"
  "cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_adapter.py"
  "cloudpss_skills_v2/tests/powerapi_tests/test_pandapower_sc_adapter.py"
  "cloudpss_skills_v2/tests/powerskill_tests/test_new_apis.py"
  "cloudpss_skills_v2/tests/skills/test_power_flow.py"
  "cloudpss_skills_v2/tests/test_auto_channel_setup.py"
  "cloudpss_skills_v2/tests/test_cloudpss_converter.py"
  "cloudpss_skills_v2/tests/test_comtrade_export.py"
  "cloudpss_skills_v2/tests/test_contingency_analysis.py"
  "cloudpss_skills_v2/tests/test_data_lib.py"
  "cloudpss_skills_v2/tests/test_hdf5_export.py"
  "cloudpss_skills_v2/tests/test_maintenance_security.py"
  "cloudpss_skills_v2/tests/test_n2_security.py"
  "cloudpss_skills_v2/tests/test_orthogonal_sensitivity.py"
  "cloudpss_skills_v2/tests/test_output_standard.py"
  "cloudpss_skills_v2/tests/test_skill_config_integrity.py"
  "cloudpss_skills_v2/tests/test_skills_integration.py"
  "cloudpss_skills_v2/tests/test_vsi_weak_bus.py"
)
```

**验收标准**:
- [ ] 所有列出的文件已删除
- [ ] pytest 收集不再显示这些测试
- [ ] 没有破坏其他测试的导入

**任务 1.2: 删除/修复永久跳过测试 (48个)**
```bash
# 24个文件需要处理
skip_files=(
  "test_algo_lib.py"
  "test_auto_loop_breaker.py"
  "test_batch_powerflow.py"
  "test_batch_task_manager.py"
  "test_compare_visualization.py"
  "test_component_catalog.py"
  "test_config_batch_runner.py"
  "test_fault_severity_scan.py"
  "test_harmonic_analysis.py"
  "test_integration_datalib.py"
  "test_loss_analysis.py"
  "test_model_builder.py"
  "test_model_hub.py"
  "test_model_lib.py"
  "test_model_parameter_extractor.py"
  "test_n1_security.py"
  "test_param_scan.py"
  "test_parameter_sensitivity.py"
  "test_power_quality_analysis.py"
  "test_protection_coordination.py"
  "test_reactive_compensation_design.py"
  "test_transient_stability_margin.py"
  "test_voltage_stability.py"
  "test_workflow_lib.py"
)
```

**决策流程**:
```
对于每个文件:
  1. 检查被测技能是否存在且有实际功能
     ├── 是 → 修复测试，提供正确的构造函数
     └── 否 → 删除整个测试文件
  2. 验证修复后的测试可以运行
```

**验收标准**:
- [ ] 48个永久跳过测试已处理
- [ ] pytest --collect-only 显示这些测试（如果技能存在）
- [ ] 或这些文件已删除（如果技能未实现）

#### Week 2: 修复无意义测试

**任务 1.3: 标记并审查冒烟测试 (200+)**

**策略**: 暂时保留，但标记为需要改进
```python
# 在每个无意义的测试上添加标记
@pytest.mark.smoke
@pytest.mark.needs_improvement(reason="仅验证属性存在，需添加行为验证")
def test_has_name_attribute(self):
    assert hasattr(self.skill, 'name')
```

**验收标准**:
- [ ] 200+ 个冒烟测试已标记
- [ ] 创建改进任务清单
- [ ] CI 可以过滤这些测试运行

**任务 1.4: 修复返回代替断言 (5个)**

| 文件 | 行号 | 修复方式 |
|------|------|---------|
| tests/test_all_skills_real.py:40-58 | 修改为 assert 语句 |
| tests/param_scan_emt_test.py:66,191 | 修改为 assert 语句 |
| tests/test_emt_fault_core_unit.py:14,22 | 修复为正常异常测试 |
| tests/test_emt_measurement_core_unit.py:259 | 修复为正常异常测试 |

**验收标准**:
- [ ] 所有返回bool的测试改为assert
- [ ] 测试可以正确失败
- [ ] pytest -x 在这些测试失败时停止

### Week 1-2 里程碑检查点

```bash
# 检查点 1.1: 虚假测试清理
pytest tests/ cloudpss_skills_v2/tests/ --collect-only -q | wc -l
# 预期: 从 1000+ 减少到 300-400

# 检查点 1.2: 真实测试运行
pytest tests/ -x --tb=short
# 预期: 通过率 > 80%

# 检查点 1.3: 无虚假测试
pytest tests/ --collect-only | grep -i "placeholder\|empty\|skip" | wc -l
# 预期: 0
```

---

## 🔧 Phase 2: 修复核心缺陷 (Week 3-5)

### 目标
修复 15+ 逻辑错误、5+ 安全问题、5+ 竞争条件。

### Week 3: 修复逻辑错误

**任务 2.1: 修复聚合逻辑错误**

| 文件 | 行号 | 问题 | 修复方案 |
|------|------|------|---------|
| poweranalysis/n1_security.py | 254-261 | case_violations 被覆盖 | 改为 extend() 追加 |
| poweranalysis/emt_n1_screening.py | 149-159 | 从未实际执行故障 | 添加 actual_trip 逻辑 |
| poweranalysis/loss_analysis.py | 314-323 | 0.0 被误判为缺失 | 使用 is None 检查 |
| poweranalysis/small_signal_stability.py | 145-149 | 硬编码矩阵 | 从模型动态派生 |

**验收标准**:
- [ ] 所有修复有单元测试覆盖
- [ ] 集成测试通过
- [ ] 代码审查通过

**任务 2.2: 修复字段映射错误**

| 文件 | 行号 | 问题 |
|------|------|------|
| poweranalysis/emt_fault_study.py | 59-69 | scenario result 字段组装错误 |

**修复代码**:
```python
# 修复前 (错误)
result = {
    "voltage_deviation": scenario_name,  # 错误!
    "severity": voltage_deviation,       # 错误!
}

# 修复后 (正确)
result = {
    "scenario_name": scenario_name,
    "voltage_deviation": voltage_deviation,
    "severity": calculate_severity(voltage_deviation),
}
```

### Week 4: 修复安全问题

**任务 2.3: 修复路径遍历漏洞**

| 文件 | 行号 | 风险 | 修复 |
|------|------|------|------|
| tools/visualize.py | 100-103 | 任意文件读取 | 添加路径白名单验证 |

**修复方案**:
```python
# 修复前
with open(source["data_file"]) as f:  # 危险!

# 修复后
import os
from pathlib import Path

allowed_dirs = ["/data", "/results"]
data_file = Path(source["data_file"]).resolve()
if not any(str(data_file).startswith(d) for d in allowed_dirs):
    raise ValueError(f"Invalid path: {data_file}")
with open(data_file) as f:
```

**任务 2.4: 修复 XSS 漏洞**

| 文件 | 行号 | 风险 |
|------|------|------|
| tools/report_generator.py | 132-149 | 原始内容嵌入 HTML |

**修复方案**:
```python
# 使用 html.escape 转义
import html

# 修复前
html_content = f"<div>{raw_content}</div>"

# 修复后
html_content = f"<div>{html.escape(raw_content)}</div>"
```

**任务 2.5: 修复 Token 路径安全问题**

| 文件 | 行号 | 风险 |
|------|------|------|
| powerapi/adapters/cloudpss/powerflow.py | 142-152 | 相对路径加载 |
| powerapi/adapters/cloudpss/short_circuit.py | 278-283 | 相对路径加载 |
| powerapi/adapters/cloudpss/emt.py | 277-287 | 相对路径加载 |

**修复方案**:
```python
# 使用绝对路径或配置路径
token_path = Path(config.get("token_path", "/etc/cloudpss/token")).resolve()
```

### Week 5: 修复竞争条件

**任务 2.6: 修复全局环境变量修改**

| 文件 | 行号 | 问题 |
|------|------|------|
| powerapi/adapters/cloudpss/powerflow.py | 136-140 | 修改全局 os.environ |
| powerapi/adapters/cloudpss/short_circuit.py | 273-277 | 修改全局 os.environ |
| powerapi/adapters/cloudpss/emt.py | 271-275 | 修改全局 os.environ |

**修复方案**:
```python
# 使用 threading.local() 或上下文管理器
import threading

_local = threading.local()

@contextmanager
def temp_env_var(key, value):
    old = os.environ.get(key)
    os.environ[key] = value
    try:
        yield
    finally:
        if old is None:
            del os.environ[key]
        else:
            os.environ[key] = old
```

**任务 2.7: 修复缓存竞争**

| 文件 | 行号 | 问题 |
|------|------|------|
| powerapi/adapters/pandapower/powerflow.py | 260-272 | 缓存网络对象被修改 |

**修复方案**:
```python
# 深拷贝缓存对象
import copy
net = copy.deepcopy(cached_net)
```

### Phase 2 里程碑检查点

```bash
# 安全检查
bandit -r cloudpss_skills_v2/poweranalysis cloudpss_skills_v2/powerapi cloudpss_skills_v2/tools
# 预期: 无 High/Critical 问题

# 逻辑测试
pytest tests/test_n1_security.py tests/test_emt_n1_screening.py -v
# 预期: 通过率 100%

# 集成测试
pytest tests/ --run-integration -m "integration and not slow_emt" -x
# 预期: 通过率 > 90%
```

---

## 🏗️ Phase 3: 实现/删除未完成的技能 (Week 6-7)

### 目标
处理 11 个只有 TODO 注释的未实现技能。

### 决策矩阵

| 技能 | 优先级 | 决策 | 工期 |
|------|--------|------|------|
| comtrade_export | High | 实现核心功能 | 2天 |
| hdf5_export | High | 实现核心功能 | 2天 |
| compare_visualization | Medium | 实现核心功能 | 3天 |
| auto_channel_setup | Medium | 实现核心功能 | 3天 |
| model_builder | Low | 删除（重复） | 1天 |
| batch_task_manager | Medium | 实现核心功能 | 3天 |
| config_batch_runner | Low | 删除 | 1天 |
| study_pipeline | High | 实现核心功能 | 4天 |
| model_hub | Low | 删除 | 1天 |
| report_generator | Medium | 完善现有功能 | 2天 |
| visualize | Medium | 完善现有功能 | 2天 |

### Week 6: 实现高优先级技能

**任务 3.1: 实现 comtrade_export**

```python
# cloudpss_skills_v2/tools/comtrade_export.py
class ComtradeExportTool:
    """导出 COMTRADE 格式波形数据"""
    
    def run(self, config: dict) -> SkillResult:
        # 1. 验证输入
        # 2. 读取波形数据
        # 3. 生成 .cfg 文件
        # 4. 生成 .dat 文件
        # 5. 返回结果
        pass
```

**验收标准**:
- [ ] 可以导出标准 COMTRADE 格式
- [ ] 有单元测试覆盖
- [ ] 集成测试通过

**任务 3.2: 实现 hdf5_export**

**验收标准**:
- [ ] 可以导出 HDF5 格式
- [ ] 支持读取和列出数据集
- [ ] 有完整测试

**任务 3.3: 实现 study_pipeline**

**验收标准**:
- [ ] 支持多步骤流水线
- [ ] 支持条件执行
- [ ] 支持变量解析
- [ ] 有完整测试

### Week 7: 删除/简化低优先级技能

**任务 3.4: 删除重复/低价值技能**

```bash
# 删除列表
rm cloudpss_skills_v2/tools/model_builder.py
rm cloudpss_skills_v2/tools/config_batch_runner.py
rm cloudpss_skills_v2/tools/model_hub.py

# 从注册表移除
# 更新 __init__.py
```

**任务 3.5: 完善现有技能**

- report_generator: 修复 XSS，添加格式选择
- visualize: 添加更多图表类型

### Phase 3 里程碑检查点

```python
# 验证技能数量
python -m cloudpss_skills list | wc -l
# 预期: 减少 3 个（删除的），新增 0 个

# 验证关键技能
python -c "from cloudpss_skills import get_skill; get_skill('comtrade_export').run({...})"
# 预期: 成功运行

# 测试覆盖率
pytest --cov=cloudpss_skills/tools --cov-report=term-missing
# 预期: 新技能覆盖率 > 70%
```

---

## 📈 Phase 4: 提升测试质量 (Week 8-9)

### 目标
提升剩余测试的质量，添加缺失的覆盖。

### Week 8: 修复测试质量问题

**任务 4.1: 修复不稳定测试**

| 文件 | 问题 | 修复 |
|------|------|------|
| test_powerflow_result.py:70-80 | time.sleep(5) | 使用指数退避轮询 |
| test_emt_result.py:98-108 | time.sleep(5) | 使用指数退避轮询 |
| test_all_skills_real.py | 硬编码超时 | 使用配置超时 |

**修复代码**:
```python
# 修复前
for i in range(30):
    time.sleep(2)
    if job.status() == 1:
        break

# 修复后
import backoff

@backoff.on_predicate(backoff.expo, max_time=300)
def wait_for_completion(job):
    return job.status() == 1
```

**任务 4.2: 修复执行顺序依赖**

```python
# 使用 pytest fixture 替代全局状态
@pytest.fixture(scope="session")
def job_id_from_power_flow():
    """在单独的 fixture 中运行 power flow"""
    result = run_power_flow()
    return result.job_id

def test_waveform_export_real(job_id_from_power_flow):
    """现在可以独立运行"""
    pass
```

**任务 4.3: 添加磁盘清理**

```python
# 使用 pytest tmp_path fixture
import tempfile
import shutil

def test_with_temp_files(tmp_path):
    output_file = tmp_path / "output.yaml"
    # 测试代码...
    # 自动清理
```

### Week 9: 添加缺失覆盖

**任务 4.4: 为关键模块添加测试**

| 模块 | 目标覆盖率 | 关键场景 |
|------|-----------|---------|
| poweranalysis/n1_security.py | 85% | 边界情况、多故障 |
| poweranalysis/emt_n1_screening.py | 80% | 实际故障注入 |
| tools/report_generator.py | 75% | 错误处理、大报告 |
| tools/visualize.py | 75% | 不同图表类型 |

**任务 4.5: 添加集成测试**

```python
# test_integration_real_scenarios.py
class TestRealScenarios:
    """真实场景集成测试"""
    
    def test_ieee39_n1_screening(self, auth_token):
        """IEEE39 N-1 筛查完整流程"""
        pass
    
    def test_ieee3_emt_fault_study(self, auth_token):
        """IEEE3 EMT 故障研究"""
        pass
```

### Phase 4 里程碑检查点

```bash
# 测试稳定性
pytest tests/ --count=5  # 运行5次
# 预期: 每次通过率 > 95%

# 覆盖率报告
pytest --cov=cloudpss_skills --cov-report=html --cov-fail-under=70
# 预期: 总体覆盖率 > 70%

# 独立运行测试
pytest tests/test_waveform_export_real.py  # 不依赖其他测试
# 预期: 通过
```

---

## ✅ Phase 5: 回归验证和文档 (Week 10)

### 目标
全面验证所有修复，更新文档。

### 任务清单

**任务 5.1: 完整回归测试**

```bash
# 单元测试
pytest tests/ -x -q --tb=short
# 预期: 100% 通过

# 集成测试
pytest tests/ --run-integration -m "integration and not slow_emt" -q
# 预期: > 95% 通过

# 慢速 EMT 测试
pytest tests/ --run-integration -m "integration and slow_emt" -q
# 预期: > 90% 通过
```

**任务 5.2: 性能基准测试**

```bash
# 记录关键操作性能
pytest tests/ --benchmark-only --benchmark-json=benchmark.json
```

**任务 5.3: 更新文档**

- [ ] 更新测试策略文档
- [ ] 记录删除的技能和原因
- [ ] 更新 API 文档
- [ ] 添加已知限制

**任务 5.4: 代码审查**

```bash
# 使用工具检查
flake8 cloudpss_skills/
mypy cloudpss_skills/
bandit -r cloudpss_skills/
black --check cloudpss_skills/
```

### Phase 5 里程碑检查点

```bash
# 最终验证
python -m cloudpss_skills list  # 验证技能列表
pytest --cov=cloudpss_skills --cov-fail-under=75  # 验证覆盖率
bandit -r cloudpss_skills/ -ll  # 验证无安全问题
```

---

## 📊 项目时间表

```
Week 1-2:   [Phase 1] ████████████████████ 清理虚假测试
Week 3-5:   [Phase 2] ██████████████████████████████ 修复核心缺陷
Week 6-7:   [Phase 3] ████████████████████ 实现/删除技能
Week 8-9:   [Phase 4] ████████████████████ 提升测试质量
Week 10:    [Phase 5] ██████████ 回归验证和文档
```

---

## 🎯 成功指标

### 修复前基线
- 总测试数: ~1000
- 虚假测试: 340+ (34%)
- 通过率: ~60%
- 代码覆盖率: ~45%

### 修复后目标
- 总测试数: ~400 (精简有效)
- 虚假测试: 0 (0%)
- 通过率: > 95%
- 代码覆盖率: > 75%
- 安全问题: 0 High/Critical
- 不稳定测试: < 5

---

## ⚠️ 风险与缓解

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|---------|
| 删除测试导致功能退化 | 中 | 高 | 每个删除前检查功能是否存在 |
| 修复逻辑错误引入新 bug | 中 | 高 | 每个修复必须有单元测试 |
| 实现技能超出工期 | 中 | 中 | 可延期到 Phase 6 |
| 集成测试依赖外部服务 | 高 | 中 | 使用 mocking 隔离外部依赖 |

---

## 📝 任务追踪模板

```markdown
### 任务: [任务ID] - [简短描述]
**负责人**: @username
**状态**: 🔄 进行中 / ✅ 完成 / ⏸️ 阻塞
**工期**: X 天
**截止日期**: YYYY-MM-DD

**验收标准**:
- [ ] 标准 1
- [ ] 标准 2
- [ ] 标准 3

**相关文件**:
- `path/to/file1.py`
- `path/to/file2.py`

**备注**:
任何额外信息
```

---

## 🚀 下一步行动

1. **立即**: 审批此计划
2. **本周**: 分配 Phase 1 任务
3. **Day 1**: 开始删除空测试类
4. **Day 3**: 第一轮代码审查
5. **Week 1 结束**: Phase 1 里程碑检查

---

**计划编制**: Sisyphus AI  
**审核状态**: 待审查  
**最后更新**: 2026-04-23
