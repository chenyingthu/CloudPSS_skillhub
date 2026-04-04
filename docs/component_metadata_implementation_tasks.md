# CloudPSS 元件库元数据系统 - 实施任务表

> 目标：建立自动化的元件库元数据管理系统
> 标准：高质量工程实践、自动化测试、真实API集成测试、零Fake Tests

---

## 📋 任务总览

```
Phase 1: 核心基础设施 ──────────────┐
  ├─ 1.1 项目结构搭建              │
  ├─ 1.2 Markdown表格解析器        │
  ├─ 1.3 元数据结构定义            │
  ├─ 1.4 元数据注册表              │
  └─ 1.5 单元测试 (>90%覆盖率)     │
                                   │
Phase 2: Skill 集成 ───────────────┤
  ├─ 2.1 model_builder 集成        │
  ├─ 2.2 model_validator 集成      │
  ├─ 2.3 参数自动补全              │
  └─ 2.4 集成测试                  │
                                   │
Phase 3: 自动化和文档 ─────────────┤
  ├─ 3.1 批量元数据提取工具        │
  ├─ 3.2 生成初始元数据            │
  ├─ 3.3 CI/CD 配置                │
  └─ 3.4 E2E 测试                  │
                                   │
Phase 4: 验证和优化 ───────────────┘
  ├─ 4.1 真实模型验证
  ├─ 4.2 性能优化
  └─ 4.3 最终验收
```

---

## 🔴 Phase 1: 核心基础设施

### Task 1.1: 项目结构搭建
**优先级**: P0 | **预计工时**: 2h | **状态**: 🆕

**描述**:
创建元数据系统的项目结构和基础文件

**验收标准**:
- [ ] 创建 `cloudpss_skills/metadata/` 目录
- [ ] 创建 `__init__.py` 并导出公共 API
- [ ] 创建基础文件: `parser.py`, `registry.py`, `models.py`
- [ ] 创建测试目录: `tests/unit/metadata/`, `tests/integration/metadata/`
- [ ] 更新 `setup.py` 添加依赖

**测试要求**:
- [ ] 导入测试通过
- [ ] 目录结构检查

**实现提示**:
```bash
mkdir -p cloudpss_skills/metadata
mkdir -p tests/unit/metadata
mkdir -p tests/integration/metadata
```

---

### Task 1.2: Markdown 表格解析器
**优先级**: P0 | **预计工时**: 4h | **状态**: 🆕

**描述**:
实现从 Markdown 文档提取参数和引脚定义的解析器

**验收标准**:
- [ ] 实现 `ComponentDocumentParser` 类
- [ ] 支持解析 `_parameters.md` 参数表格
- [ ] 支持解析 `_pins.md` 引脚表格
- [ ] 正确识别参数类型和单位
- [ ] 正确处理参数分组

**测试要求**:
- [ ] 单元测试 > 90% 覆盖率
- [ ] 测试 WGSource 参数解析
- [ ] 测试 TransmissionLine 参数解析
- [ ] 测试边界情况（空表格、缺失字段）

**依赖**: Task 1.1

**实现提示**:
```python
class ComponentDocumentParser:
    def parse_parameters(self, content: str) -> List[ParameterGroup]
    def parse_pins(self, content: str) -> Dict[str, List[PinDefinition]]
```

---

### Task 1.3: 元数据结构定义
**优先级**: P0 | **预计工时**: 3h | **状态**: 🆕

**描述**:
定义元数据的数据模型和验证逻辑

**验收标准**:
- [ ] 实现 `Parameter` dataclass
- [ ] 实现 `PinDefinition` dataclass
- [ ] 实现 `ParameterGroup` dataclass
- [ ] 实现 `ComponentMetadata` dataclass
- [ ] 实现参数验证方法

**测试要求**:
- [ ] 单元测试 > 90% 覆盖率
- [ ] 测试参数类型验证
- [ ] 测试参数范围验证
- [ ] 测试 JSON 序列化/反序列化

**依赖**: Task 1.1

**实现提示**:
```python
@dataclass
class ComponentMetadata:
    component_id: str
    parameter_groups: List[ParameterGroup]
    pins: Dict[str, List[PinDefinition]]
    
    def validate_parameters(self, params: Dict) -> ValidationResult
    def auto_complete(self, user_params: Dict) -> Dict
```

---

### Task 1.4: 元数据注册表
**优先级**: P0 | **预计工时**: 4h | **状态**: 🆕

**描述**:
实现元数据的加载、缓存和查询系统

**验收标准**:
- [ ] 实现 `ComponentMetadataRegistry` 类
- [ ] 支持从 JSON 文件加载
- [ ] 实现缓存机制
- [ ] 实现按类别查询
- [ ] 实现全局单例实例

**测试要求**:
- [ ] 单元测试 > 90% 覆盖率
- [ ] 测试加载多个元件
- [ ] 测试缓存机制
- [ ] 测试查询性能

**依赖**: Task 1.3

**实现提示**:
```python
class ComponentMetadataRegistry:
    def load_all(self) -> None
    def get_component(self, component_id: str) -> Optional[ComponentMetadata]
    def list_components(self, category: str = None) -> List[str]
    
_registry: Optional[ComponentMetadataRegistry] = None
def get_registry() -> ComponentMetadataRegistry
```

---

### Task 1.5: Phase 1 单元测试整合
**优先级**: P0 | **预计工时**: 3h | **状态**: 🆕

**描述**:
完成 Phase 1 所有单元测试并确保覆盖率

**验收标准**:
- [ ] Parser 单元测试通过率 100%
- [ ] Registry 单元测试通过率 100%
- [ ] Models 单元测试通过率 100%
- [ ] 整体代码覆盖率 > 90%

**测试命令**:
```bash
pytest tests/unit/metadata -v --cov=cloudpss_skills.metadata --cov-report=html
```

**依赖**: Task 1.1, 1.2, 1.3, 1.4

---

## 🟡 Phase 2: Skill 集成

### Task 2.1: model_builder 集成
**优先级**: P0 | **预计工时**: 4h | **状态**: 🆕

**描述**:
更新 model_builder 使用元数据进行参数验证和自动补全

**验收标准**:
- [ ] 在 `_add_component` 中集成元数据查询
- [ ] 实现参数自动补全
- [ ] 实现参数验证
- [ ] 实现引脚验证
- [ ] 向后兼容（无元数据时仍工作）

**测试要求**:
- [ ] 集成测试通过率 100%
- [ ] 使用真实 API 测试添加 WGSource
- [ ] 验证自动补全功能

**依赖**: Task 1.5

**实现提示**:
```python
def _add_component(self, config: Dict):
    metadata = self.metadata_registry.get_component(comp_type)
    if metadata:
        complete_params = metadata.auto_complete(user_params)
        validation = metadata.validate_parameters(complete_params)
        if not validation.valid:
            raise ValueError(...)
```

---

### Task 2.2: model_validator 集成
**优先级**: P0 | **预计工时**: 4h | **状态**: 🆕

**描述**:
更新 model_validator 使用元数据进行深度验证

**验收标准**:
- [ ] 在拓扑验证中集成参数验证
- [ ] 实现引脚连接验证
- [ ] 生成详细的验证报告
- [ ] 向后兼容

**测试要求**:
- [ ] 集成测试通过率 100%
- [ ] 使用真实 API 测试验证模型
- [ ] 验证错误检测功能

**依赖**: Task 2.1

---

### Task 2.3: Phase 2 集成测试
**优先级**: P0 | **预计工时**: 3h | **状态**: 🆕

**描述**:
完成 Phase 2 集成测试

**验收标准**:
- [ ] model_builder 集成测试通过率 100%
- [ ] model_validator 集成测试通过率 100%
- [ ] 使用真实 CloudPSS API

**测试文件**:
- `tests/integration/test_model_builder_metadata.py`
- `tests/integration/test_model_validator_metadata.py`

**依赖**: Task 2.1, 2.2

---

## 🟢 Phase 3: 自动化和文档

### Task 3.1: 批量元数据提取 CLI 工具
**优先级**: P1 | **预计工时**: 4h | **状态**: 🆕

**描述**:
实现批量从文档提取元数据的 CLI 工具

**验收标准**:
- [ ] 实现 `extract_metadata.py` 脚本
- [ ] 支持递归扫描文档目录
- [ ] 生成 JSON 元数据文件
- [ ] 生成索引文件
- [ ] 支持增量更新

**使用示例**:
```bash
python -m cloudpss_skills.tools.extract_metadata \
  --docs-path ../cloudpss_docs \
  --output ./component_metadata
```

**测试要求**:
- [ ] 单元测试 > 90% 覆盖率
- [ ] 测试提取所有可再生能源元件

**依赖**: Task 1.5

---

### Task 3.2: 生成初始元数据
**优先级**: P1 | **预计工时**: 2h | **状态**: 🆕

**描述**:
运行提取工具生成初始元数据文件

**验收标准**:
- [ ] 提取 WGSource 元数据
- [ ] 提取 TransmissionLine 元数据
- [ ] 提取至少 10 个常用元件
- [ ] 文件格式验证通过

**交付物**:
- `cloudpss_skills/component_metadata/*.json`
- `cloudpss_skills/component_metadata/_index.json`

**依赖**: Task 3.1

---

### Task 3.3: CI/CD 配置
**优先级**: P1 | **预计工时**: 3h | **状态**: 🆕

**描述**:
配置 GitHub Actions 自动化测试

**验收标准**:
- [ ] 创建 `.github/workflows/metadata-tests.yml`
- [ ] 配置单元测试 Job
- [ ] 配置集成测试 Job
- [ ] 配置 E2E 测试 Job
- [ ] 配置覆盖率报告

**工作流触发条件**:
- Push 到 main 分支
- PR 修改 metadata 相关文件

**依赖**: Task 2.3

---

### Task 3.4: E2E 测试
**优先级**: P1 | **预计工时**: 4h | **状态**: 🆕

**描述**:
实现端到端测试

**验收标准**:
- [ ] 测试完整工作流：提取 → 注册表 → Skill
- [ ] 使用真实 CloudPSS API
- [ ] 测试 IEEE39 模型添加风机
- [ ] 测试验证流程

**测试文件**:
- `tests/e2e/test_metadata_workflow.py`

**依赖**: Task 3.2, 3.3

---

## 🔵 Phase 4: 验证和优化

### Task 4.1: 真实模型验证
**优先级**: P1 | **预计工时**: 3h | **状态**: 🆕

**描述**:
使用真实模型验证系统功能

**验收标准**:
- [ ] 使用 IEEE39 模型
- [ ] 添加 WGSource 并验证参数自动补全
- [ ] 运行潮流验证
- [ ] 运行暂态验证
- [ ] 生成验证报告

**测试模型**:
- `model/holdme/IEEE39`
- 新模型: `model/holdme/test_metadata_integration`

**依赖**: Task 3.4

---

### Task 4.2: 性能优化
**优先级**: P2 | **预计工时**: 2h | **状态**: 🆕

**描述**:
优化加载和查询性能

**验收标准**:
- [ ] 注册表加载时间 < 1s (100个元件)
- [ ] 参数查询时间 < 10ms
- [ ] 实现懒加载
- [ ] 内存占用合理

**优化点**:
- 缓存策略
- 懒加载
- JSON 压缩

**依赖**: Task 4.1

---

### Task 4.3: 文档更新
**优先级**: P2 | **预计工时**: 3h | **状态**: 🆕

**描述**:
更新项目文档

**验收标准**:
- [ ] 更新 README.md
- [ ] 创建使用指南 docs/metadata_usage.md
- [ ] 创建 API 文档 docs/api.md
- [ ] 添加代码示例

**依赖**: Task 4.2

---

### Task 4.4: 最终验收测试
**优先级**: P0 | **预计工时**: 2h | **状态**: 🆕

**描述**:
完整验收测试

**验收标准**:
- [ ] 所有单元测试通过率 100%
- [ ] 所有集成测试通过率 100%
- [ ] 所有 E2E 测试通过率 100%
- [ ] 代码覆盖率 > 90%
- [ ] 文档完整
- [ ] 性能达标

**验收命令**:
```bash
# 运行所有测试
pytest tests/unit/metadata tests/integration/metadata tests/e2e -v --run-integration

# 检查覆盖率
pytest --cov=cloudpss_skills.metadata --cov-report=term-missing

# 验证元数据文件
python -c "from cloudpss_skills.metadata import get_registry; r = get_registry(); r.load_all(); print(f'Loaded {len(r.list_components())} components')"
```

**依赖**: Task 4.3

---

## 📊 进度跟踪

| Phase | 任务数 | 已完成 | 状态 |
|-------|--------|--------|------|
| Phase 1 | 5 | 0 | 🆕 |
| Phase 2 | 3 | 0 | 🆕 |
| Phase 3 | 4 | 0 | 🆕 |
| Phase 4 | 4 | 0 | 🆕 |
| **总计** | **16** | **0** | **0%** |

---

## 🎯 关键里程碑

1. **M1: 基础完成** (Week 1 End)
   - Phase 1 所有任务完成
   - 单元测试通过率 100%

2. **M2: 集成完成** (Week 2 End)
   - Phase 2 所有任务完成
   - model_builder 和 model_validator 功能正常

3. **M3: 自动化完成** (Week 3 End)
   - Phase 3 所有任务完成
   - CI/CD 运行正常
   - 初始元数据生成

4. **M4: 验收完成** (Week 4 End)
   - Phase 4 所有任务完成
   - 真实模型验证通过
   - 项目文档完整

