# CloudPSS Skill Framework - Implementation Plan

**版本**: 1.0.0  
**创建日期**: 2026-04-16  
**状态**: 规划中

---

## 一、总体策略

### 1.1 实施原则

```
1. 渐进式演进：逐步迁移，不破坏现有功能
2. 向后兼容：现有 skills 继续工作
3. 增量价值：每阶段交付可用功能
4. 测试驱动：每层独立测试
```

### 1.2 三层开发顺序

```
第一阶段：AWT 适配层
         ↓
第二阶段：Swing 抽象层
         ↓
第三阶段：支撑工具层 + Skill 重构
         ↓
第四阶段：多工具集成
```

---

## 二、分阶段实施计划

### Phase 1: AWT 适配层 (Week 1-2)

**目标**：建立 AWT Adapter 基础框架，实现第一个 Adapter

#### 1.1.1 目录结构

```
cloudpss_skills/
├── awt/                           # 新增
│   ├── __init__.py
│   ├── base.py                    # Adapter 基类
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── cloudpss/              # CloudPSS 适配器
│   │   │   ├── __init__.py
│   │   │   ├── powerflow.py
│   │   │   ├── shortcircuit.py
│   │   │   └── transient.py
│   │   └── pandapower/            # pandapower 适配器
│   │       ├── __init__.py
│   │       └── powerflow.py
│   └── registry.py               # Adapter 注册表
```

#### 1.1.2 AWT Base 定义

```python
# awt/base.py
class AdapterBase(ABC):
    """AWT 适配器基类"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """适配器名称"""
        pass
    
    @property
    @abstractmethod
    def supported_analyses(self) -> List[str]:
        """支持的仿真分析类型"""
        pass
    
    @abstractmethod
    def connect(self, config: Dict) -> bool:
        """连接到仿真引擎"""
        pass
    
    @abstractmethod
    def disconnect(self):
        """断开连接"""
        pass
```

#### 1.1.3 CloudPSS PowerFlow Adapter 实现

```python
# awt/adapters/cloudpss/powerflow.py
class CloudPSSPowerFlowAdapter(AdapterBase):
    """CloudPSS 潮流计算适配器"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.model = None
    
    @property
    def name(self) -> str:
        return "cloudpss"
    
    @property
    def supported_analyses(self) -> List[str]:
        return ["powerflow", "shortcircuit", "transient"]
    
    def connect(self, config: Dict) -> bool:
        """连接 CloudPSS"""
        from cloudpss import Model, setToken
        
        auth = config.get("auth", {})
        token = auth.get("token") or self._load_token(auth.get("token_file"))
        setToken(token)
        return True
    
    def run_powerflow(self, model_rid: str, params: Dict) -> Dict:
        """执行潮流计算"""
        model = Model.fetch(model_rid)
        job = model.runPowerFlow()
        result = job.result()
        
        return {
            "status": "success",
            "buses": parse_cloudpss_table(result.getBuses()),
            "branches": parse_cloudpss_table(result.getBranches()),
            "converged": True,
        }
```

#### 1.1.4 交付物

| 交付物 | 描述 | 验收标准 |
|--------|------|----------|
| `awt/base.py` | Adapter 基类定义 | 抽象方法完整 |
| `awt/adapters/cloudpss/powerflow.py` | CloudPSS PF Adapter | 潮流计算功能正常 |
| `awt/registry.py` | Adapter 注册表 | 可按名称查找 Adapter |
| 测试用例 | AWT Layer 单元测试 | 100% 覆盖率 |

#### 1.1.5 测试策略

```python
# tests/test_awt_adapter_base.py
class TestCloudPSSPowerFlowAdapter:
    """CloudPSS PF Adapter 测试"""
    
    def test_adapter_name(self):
        adapter = CloudPSSPowerFlowAdapter()
        assert adapter.name == "cloudpss"
    
    def test_supported_analyses(self):
        adapter = CloudPSSPowerFlowAdapter()
        assert "powerflow" in adapter.supported_analyses
    
    @pytest.mark.integration
    def test_run_powerflow(self, cloudpss_model):
        adapter = CloudPSSPowerFlowAdapter()
        adapter.connect({"auth": {"token_file": ".cloudpss_token"}})
        
        result = adapter.run_powerflow("model/holdme/IEEE39", {})
        
        assert result["status"] == "success"
        assert len(result["buses"]) > 0
```

---

### Phase 2: Swing 抽象层 (Week 3-4)

**目标**：定义引擎无关的抽象 API

#### 2.1.1 目录结构

```
cloudpss_skills/
├── swing/                         # 新增
│   ├── __init__.py
│   ├── base.py                    # API 基类
│   ├── apis/
│   │   ├── __init__.py
│   │   ├── powerflow.py           # 潮流计算 API
│   │   ├── shortcircuit.py        # 短路计算 API
│   │   ├── transient.py            # 暂态仿真 API
│   │   └── factory.py             # API 工厂
│   └── exceptions.py               # 异常定义
```

#### 2.1.2 Swing API 基类

```python
# swing/base.py
class SwingAPI(ABC):
    """Swing 抽象 API 基类"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """API 名称"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """API 版本"""
        pass


# swing/apis/powerflow.py
class PowerFlowAPI(SwingAPI):
    """潮流计算抽象 API"""
    
    @abstractmethod
    def run(
        self,
        model: Union[str, Dict],  # RID 或配置
        config: PowerFlowConfig = None
    ) -> PowerFlowResult:
        """
        执行潮流计算
        
        Args:
            model: 模型 RID 或配置
            config: 潮流计算配置
        
        Returns:
            PowerFlowResult: 潮流计算结果
        """
        pass
    
    @abstractmethod
    def extract_buses(self, result: PowerFlowResult) -> List[BusData]:
        """提取母线数据"""
        pass
    
    @abstractmethod
    def extract_branches(self, result: PowerFlowResult) -> List[BranchData]:
        """提取支路数据"""
        pass
```

#### 2.1.3 CloudPSS 实现

```python
# swing/apis/powerflow.py
class CloudPSSPowerFlow(PowerFlowAPI):
    """CloudPSS 潮流计算实现"""
    
    def __init__(self, adapter: CloudPSSPowerFlowAdapter = None):
        self._adapter = adapter or CloudPSSPowerFlowAdapter()
    
    @property
    def name(self) -> str:
        return "cloudpss_powerflow"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    def run(self, model: Union[str, Dict], config: PowerFlowConfig = None) -> PowerFlowResult:
        model_rid = model if isinstance(model, str) else model.get("rid")
        
        result = self._adapter.run_powerflow(model_rid, config or {})
        
        return PowerFlowResult(
            buses=result["buses"],
            branches=result["branches"],
            converged=result.get("converged", True),
        )
    
    def extract_buses(self, result: PowerFlowResult) -> List[BusData]:
        return result.buses
    
    def extract_branches(self, result: PowerFlowResult) -> List[BranchData]:
        return result.branches
```

#### 2.1.4 pandapower 实现

```python
# swing/apis/powerflow.py
class PandapowerPowerFlow(PowerFlowAPI):
    """pandapower 潮流计算实现"""
    
    def __init__(self, adapter: PandapowerPowerFlowAdapter = None):
        self._adapter = adapter or PandapowerPowerFlowAdapter()
        self._net = None
    
    @property
    def name(self) -> str:
        return "pandapower_powerflow"
    
    def run(self, model: Union[str, Dict], config: PowerFlowConfig = None) -> PowerFlowResult:
        # model 可以是 pandapower net 或转换配置
        if isinstance(model, str):
            # 从文件加载
            self._net = pp.from_json(model)
        else:
            self._net = model
        
        result = self._adapter.run_powerflow(self._net, config or {})
        
        return PowerFlowResult(
            buses=result["buses"],
            branches=result["branches"],
        )
```

#### 2.1.5 API 工厂

```python
# swing/apis/factory.py
class PowerFlowAPIFactory:
    """潮流计算 API 工厂"""
    
    _registry: Dict[str, Type[PowerFlowAPI]] = {}
    
    @classmethod
    def register(cls, name: str, impl_class: Type[PowerFlowAPI]):
        """注册实现"""
        cls._registry[name] = impl_class
    
    @classmethod
    def create(cls, engine: str, **kwargs) -> PowerFlowAPI:
        """创建 API 实例"""
        if engine not in cls._registry:
            raise ValueError(f"Unknown engine: {engine}")
        
        return cls._registry[engine](**kwargs)
    
    @classmethod
    def list_engines(cls) -> List[str]:
        """列出可用引擎"""
        return list(cls._registry.keys())


# 注册默认实现
PowerFlowAPIFactory.register("cloudpss", CloudPSSPowerFlow)
PowerFlowAPIFactory.register("pandapower", PandapowerPowerFlow)
```

#### 2.1.6 交付物

| 交付物 | 描述 | 验收标准 |
|--------|------|----------|
| `swing/base.py` | Swing API 基类 | 抽象方法完整 |
| `swing/apis/powerflow.py` | PowerFlowAPI + CloudPSS/PP 实现 | 接口一致 |
| `swing/apis/factory.py` | API 工厂 | 可按名称创建 |
| 集成测试 | CloudPSS + pandapower 互操作性 | 两种引擎结果可比 |

---

### Phase 3: 支撑工具层 (Week 5-6)

**目标**：实现 ModelLib、DataLib、WorkflowLib

#### 3.1.1 目录结构

```
cloudpss_skills/
├── lib/                            # 新增
│   ├── __init__.py
│   ├── model/                      # ModelLib
│   │   ├── __init__.py
│   │   ├── base.py                # 模型基类
│   │   ├── converter.py           # 模型转换器
│   │   └── adapters/
│   │       ├── cloudpss.py
│   │       └── pandapower.py
│   ├── data/                       # DataLib
│   │   ├── __init__.py
│   │   ├── bus.py
│   │   ├── branch.py
│   │   ├── generator.py
│   │   └── types.py
│   ├── workflow/                   # WorkflowLib
│   │   ├── __init__.py
│   │   ├── pipeline.py
│   │   ├── step.py
│   │   └── merger.py
│   └── algo/                       # AlgoLib
│       ├── __init__.py
│       └── algorithms.py
```

#### 3.1.2 ModelLib - 模型转换

```python
# lib/model/converter.py
class ModelConverter:
    """模型转换器"""
    
    @staticmethod
    def cloudpss_to_pandapower(cloudpss_model: Any) -> pp.Net:
        """
        CloudPSS → pandapower
        严格转换，保留拓扑和参数
        """
        net = pp.create_empty_network()
        
        # 提取拓扑
        topology = cloudpss_model.fetchTopology()
        
        # 创建母线
        for bus in topology.buses:
            pp.create_bus(net, vn_kv=bus.voltage, name=bus.name)
        
        # 创建支路
        for branch in topology.branches:
            # ...
        
        return net
    
    @staticmethod
    def pandapower_to_cloudpss(net: pp.Net) -> Dict:
        """
        pandapower → CloudPSS 配置
        用于在 CloudPSS 中创建等效模型
        """
        return {
            "buses": [...],
            "branches": [...],
        }
```

#### 3.1.3 DataLib - 数据抽象

```python
# lib/data/types.py
@dataclass
class BusData:
    """母线数据"""
    name: str
    voltage_kv: float
    angle_deg: float = None
    load_mw: float = None
    load_mvar: float = None
    generation_mw: float = None
    # ...

@dataclass
class BranchData:
    """支路数据"""
    from_bus: str
    to_bus: str
    resistance: float
    reactance: float
    line_mva: float = None
    loading_percent: float = None
    # ...
```

#### 3.1.4 WorkflowLib - 流程编排

```python
# lib/workflow/pipeline.py
class WorkflowPipeline:
    """工作流流水线"""
    
    def __init__(self, steps: List[WorkflowStep] = None):
        self.steps = steps or []
        self.results = {}
    
    def add_step(self, name: str, api: str, engine: str, config: Dict):
        """添加步骤"""
        self.steps.append(WorkflowStep(
            name=name,
            api=api,
            engine=engine,
            config=config,
        ))
    
    def run(self) -> WorkflowResult:
        """执行流水线"""
        for step in self.steps:
            api = SwingAPIFactory.create(step.api, engine=step.engine)
            result = api.run(step.config)
            self.results[step.name] = result
        
        return WorkflowResult(results=self.results)
    
    def add_conditional_branch(
        self, 
        condition: Callable, 
        if_true: "WorkflowPipeline",
        if_false: "WorkflowPipeline" = None
    ):
        """添加条件分支"""
        # ...
```

#### 3.1.5 交付物

| 交付物 | 描述 | 验收标准 |
|--------|------|----------|
| `lib/model/converter.py` | 模型转换器 | CloudPSS ↔ pandapower 双向转换 |
| `lib/data/types.py` | 数据类型定义 | Bus, Branch, Generator 等 |
| `lib/workflow/pipeline.py` | 工作流编排 | 支持顺序、条件分支 |
| 模型转换测试 | 拓扑完整性验证 | 转换前后数据一致 |

---

### Phase 4: Skill 层重构 (Week 7-8)

**目标**：将现有 skills 重构为调用 Swing API

#### 4.1.1 重构模式

```
旧架构：
power_flow.py → 直接调用 CloudPSS SDK

新架构：
power_flow.py → Swing PowerFlowAPI → AWT CloudPSS Adapter → CloudPSS SDK
                      ↓
                  或 → AWT Pandapower Adapter → pandapower API
```

#### 4.1.2 重构示例

```python
# 旧版 power_flow.py
class PowerFlowSkill(SkillBase):
    def run(self, config):
        from cloudpss import Model
        model = Model.fetch(config["model"]["rid"])
        job = model.runPowerFlow()
        result = job.result()
        return result

# 新版 power_flow.py
class PowerFlowSkill(SkillBase):
    def run(self, config):
        engine = config.get("engine", "cloudpss")
        api = PowerFlowAPIFactory.create("powerflow", engine=engine)
        
        result = api.run(config["model"], config.get("algorithm"))
        
        return SkillResult(
            data={
                "buses": api.extract_buses(result),
                "branches": api.extract_branches(result),
            }
        )
```

#### 4.1.3 配置示例

```yaml
# CloudPSS 引擎
skill: power_flow
engine: cloudpss
model:
  rid: model/holdme/IEEE39
algorithm:
  type: newton_raphson
  tolerance: 1e-6

# pandapower 引擎
skill: power_flow
engine: pandapower
model:
  source: file
  path: ./models/ieee39.json
algorithm:
  type: dc
```

#### 4.1.4 交付物

| 交付物 | 描述 | 验收标准 |
|--------|------|----------|
| 重构 `power_flow.py` | 调用 Swing API | 引擎可配置 |
| 重构 `emt_simulation.py` | 调用 Swing API | CloudPSS Only |
| 重构 `n1_security.py` | 混合引擎支持 | pandapower 初筛 + CloudPSS 验证 |
| 向后兼容测试 | 现有配置仍可用 | 回归测试通过 |

---

### Phase 5: 多工具集成 (Week 9-12)

**目标**：支持更多仿真引擎

#### 5.1.1 优先级

| 优先级 | 引擎 | 工作量 | 备注 |
|--------|------|--------|------|
| P0 | pandapower | 中 | 纯 Python，易集成 |
| P1 | PSSE | 高 | 需要 Windows + PSSE 许可证 |
| P1 | BPA | 高 | 需要专业格式支持 |
| P2 | Simulink | 高 | 需要 MATLAB |

#### 5.1.2 pandapower 完整支持

```python
# awt/adapters/pandapower/shortcircuit.py
class PandapowerShortCircuitAdapter:
    """pandapower 短路计算适配器"""
    
    def run_shortcircuit(self, net: pp.Net, fault_bus: int, fault_type: str) -> Dict:
        """执行短路计算"""
        pp.runppc2_options(f_hz=50, add_shortcircuit_z=0)
        
        sc = pp.shortcircuit_analysis(net)
        sc.calculate()
        
        return {
            "bus": fault_bus,
            "ikss_ka": net.res_shortcircuit.at[fault_bus, "ikss_ka"],
            "ip_ka": net.res_shortcircuit.at[fault_bus, "ip_ka"],
        }
```

#### 5.1.3 交付物

| 交付物 | 描述 | 验收标准 |
|--------|------|----------|
| pandapower ShortCircuit Adapter | 短路计算 | IEC 60909 标准 |
| pandapower OPF Adapter | 最优潮流 | 优化功能正常 |
| PSSE Adapter (基础) | PSSE 导入 | PSS/e 格式支持 |
| 多引擎对比工具 | 结果对比 | 统一格式输出 |

---

### Phase 6: 研究技能封装 (Week 13+)

**目标**：将论文算法转化为技能

#### 6.1.1 工作流程

```
docs/research-papers/
    └── [论文 PDF]
           ↓
    Agent 研读论文
           ↓
    提取算法要点 + 设计接口
           ↓
    实现 Swing API (AlgoLib)
           ↓
    实现 Skill
           ↓
    CloudPSS 验证
           ↓
    合并到 skills/
```

#### 6.1.2 第一个研究技能示例

```
目标：lvrt_short_circuit (考虑 LVRT 的短路电流分析)

步骤：
1. 研读论文提取算法
2. 设计 Swing API: LVRTShortCircuitAPI
3. 实现 AWT Adapter: CloudPSS LVRT Adapter
4. 实现 AlgoLib: LVRT 迭代算法
5. 实现 Skill: LvrtShortCircuitSkill
6. 在 CloudPSS IEEE39 模型上验证
```

---

## 三、测试策略

### 3.1 分层测试

```
┌─────────────────────────────────────────────────────────┐
│                    测试金字塔                                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                          ▲                               │
│                         ╱ ╲                              │
│                        ╱   ╲                             │
│                       ╱ Top │                            │
│                      ╱──────│  Skill Integration Tests    │
│                     ╱       │  (端到端测试)              │
│                    ╱  Middle│                           │
│                   ╱─────────│  Swing API Tests          │
│                  ╱          │  (接口一致性)             │
│                 ╱   Bottom   │                          │
│                ╱─────────────│  AWT Adapter Tests       │
│               ╱              │  (单元测试)               │
│              ╱                │                          │
│             ╱────────────────│────────────────────────│
│                                                         │
│            Level 1: AWT Adapter (mock 引擎)            │
│            Level 2: Swing API (mock Adapter)            │
│            Level 3: Skill (mock API)                  │
│            Level 4: Integration (真实引擎)              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 3.2 测试用例设计

```python
# Level 1: AWT Adapter 测试
class TestCloudPSSPowerFlowAdapter:
    @pytest.fixture
    def mock_cloudpss(self):
        """Mock CloudPSS SDK"""
        with patch("cloudpss.Model") as mock_model:
            mock_result = MagicMock()
            mock_result.getBuses.return_value = [{"Bus": "B1", "Vm": 1.0}]
            mock_model.fetch().runPowerFlow().result.return_value = mock_result
            yield mock_model
    
    def test_run_powerflow(self, mock_cloudpss):
        adapter = CloudPSSPowerFlowAdapter()
        adapter.connect({"auth": {"token": "test"}})
        
        result = adapter.run_powerflow("model/test", {})
        
        assert result["status"] == "success"

# Level 2: Swing API 测试
class TestPowerFlowAPI:
    def test_cloudpss_pandapower_consistency(self):
        """验证不同引擎 API 一致性"""
        cloudpss_api = PowerFlowAPIFactory.create("cloudpss")
        pp_api = PowerFlowAPIFactory.create("pandapower")
        
        # 使用同一标准模型
        model = create_standard_model()
        
        cloudpss_result = cloudpss_api.run(model)
        pp_result = pp_api.run(model)
        
        # 母线电压应在容差范围内
        for cb, pb in zip(cloudpss_result.buses, pp_result.buses):
            assert abs(cb.vm_pu - pb.vm_pu) < 0.01

# Level 3: Skill 测试
class TestPowerFlowSkill:
    def test_skill_with_cloudpss_engine(self, skill_config):
        skill = PowerFlowSkill()
        result = skill.run(skill_config)
        
        assert result.status == SkillStatus.SUCCESS
        assert "buses" in result.data

# Level 4: Integration 测试
@pytest.mark.integration
class TestPowerFlowIntegration:
    def test_real_cloudpss_execution(self):
        """真实 CloudPSS 执行"""
        with cloudpss_configured():
            skill = PowerFlowSkill()
            result = skill.run({
                "skill": "power_flow",
                "engine": "cloudpss",
                "model": {"rid": "model/holdme/IEEE39"}
            })
            
            assert result.data["converged"] == True
```

---

## 四、部署策略

### 4.1 部署环境

```
┌─────────────────────────────────────────────────────────┐
│                    开发环境 (Development)                  │
│  - 本地 Python 环境                                     │
│  - CloudPSS 开发 Token                                 │
│  - 本地 pandapower                                     │
│  - 所有代码可写                                         │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│                    测试环境 (Staging)                      │
│  - Docker 容器化                                       │
│  - CloudPSS 测试 Token                                 │
│  - 自动化 CI/CD                                        │
│  - 每次 PR 自动部署测试                                 │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│                    生产环境 (Production)                   │
│  - 云端部署                                             │
│  - CloudPSS 生产 Token                                 │
│  - 版本化发布 (v1.0, v1.1, ...)                        │
│  - 向后兼容保证                                         │
└─────────────────────────────────────────────────────────┘
```

### 4.2 CI/CD 流水线

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      
      - name: Run AWT tests
        run: pytest tests/awt/ -v --cov=cloudpss_skills.awt
      
      - name: Run Swing tests
        run: pytest tests/swing/ -v --cov=cloudpss_skills.swing
      
      - name: Run Skill tests
        run: pytest tests/skills/ -v --cov=cloudpss_skills.skills
      
      - name: Integration tests (main only)
        if: github.ref == 'refs/heads/main'
        run: pytest tests/integration/ -v
        env:
          CLOUDPSS_TOKEN: ${{ secrets.CLOUDPSS_TOKEN }}

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    
    steps:
      - name: Build package
        run: python -m build
      
      - name: Publish to PyPI
        run: |
          pip install twine
          twine upload dist/*
        env:
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
```

### 4.3 版本管理

```
版本号: MAJOR.MINOR.PATCH

MAJOR: 架构重大变化（如 AWT/Swing 分层）
MINOR: 新增功能（如新增 pandapower 支持）
PATCH: Bug 修复

向后兼容性:
- MAJOR 版本：不保证兼容
- MINOR 版本：保证向后兼容
- PATCH 版本：保证向后兼容
```

---

## 五、里程碑

### 5.1 里程碑 1: AWT/Swing 框架就绪 (Week 2 末)

```
✅ 完成:
- awt/base.py
- awt/adapters/cloudpss/powerflow.py
- swing/base.py
- swing/apis/powerflow.py
- Swing API 测试套件

验证标准:
- CloudPSS PF 计算功能正常
- pandapower PF 计算功能正常
- 两种引擎 API 接口一致
```

### 5.2 里程碑 2: 支撑工具层完成 (Week 6 末)

```
✅ 完成:
- lib/model/converter.py
- lib/data/types.py
- lib/workflow/pipeline.py
- 模型转换测试通过

验证标准:
- CloudPSS ↔ pandapower 双向转换
- 转换后拓扑完整性 > 95%
- Workflow Pipeline 可执行
```

### 5.3 里程碑 3: Skill 重构完成 (Week 8 末)

```
✅ 完成:
- power_flow.py 重构
- emt_simulation.py 重构
- n1_security.py 重构
- 向后兼容测试通过

验证标准:
- 现有配置无需修改即可运行
- 新配置可指定引擎
- 回归测试 100% 通过
```

### 5.4 里程碑 4: 多引擎支持 (Week 12 末)

```
✅ 完成:
- pandapower 完整支持 (PF + SC + OPF)
- PSSE 基础支持
- 多引擎对比工具

验证标准:
- pandapower 所有分析功能可用
- 多引擎结果可比
- 文档完整
```

---

## 六、资源估算

### 6.1 开发时间

| Phase | 工作量 | 人员 |
|-------|--------|------|
| Phase 1: AWT Layer | 2 周 | 1 人 |
| Phase 2: Swing Layer | 2 周 | 1 人 |
| Phase 3: 支撑工具层 | 2 周 | 1 人 |
| Phase 4: Skill 重构 | 2 周 | 1 人 |
| Phase 5: 多工具集成 | 4 周 | 1-2 人 |
| Phase 6: 研究技能 | 持续 | 1 人 |

**总计**: 约 12-16 周（3-4 个月）

### 6.2 依赖项

| 依赖 | 版本 | 用途 |
|------|------|------|
| Python | >= 3.9 | 运行环境 |
| cloudpss SDK | 最新 | CloudPSS 集成 |
| pandapower | >= 3.0 | 稳态分析 |
| numpy | >= 1.20 | 数值计算 |
| pytest | >= 7.0 | 测试框架 |
| docker | 最新 | 容器化部署 |

---

## 七、风险与缓解

### 7.1 技术风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 模型转换丢失信息 | 高 | 明确转换边界，提供近似转换选项 |
| 多引擎结果不一致 | 中 | 提供对比工具，告知用户差异 |
| CloudPSS API 变更 | 中 | 封装隔离，版本锁定 |

### 7.2 项目风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 范围蔓延 | 高 | 严格按 Phase 执行，不追加需求 |
| 测试覆盖不足 | 中 | 每层独立测试，CI 强制覆盖 |
| 文档不足 | 低 | 自动化生成 + Code Review |

---

## 八、下一步行动

### 本周

1. [ ] 创建 `cloudpss_skills/awt/` 目录结构
2. [ ] 实现 `awt/base.py` Adapter 基类
3. [ ] 实现 `awt/adapters/cloudpss/powerflow.py`
4. [ ] 编写 AWT 层单元测试

### 下周

5. [ ] 实现 `cloudpss_skills/swing/` 目录结构
6. [ ] 实现 `swing/base.py` API 基类
7. [ ] 实现 `swing/apis/powerflow.py`
8. [ ] 实现 `swing/apis/factory.py`

### 验证标准

- [ ] CloudPSS PF 计算功能正常
- [ ] pandapower PF 计算功能正常
- [ ] API 接口一致
- [ ] 测试覆盖率 > 80%

---

**文档状态**: 规划中  
**下一步**: 开始 Phase 1 实现  
**预计完成**: Week 12 (多引擎支持)
