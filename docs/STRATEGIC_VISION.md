# CloudPSS Skill Library - Strategic Vision & Architecture Design

**创建日期**: 2026-04-16  
**状态**: 战略规划中  
**版本**: 2.0.0 (AWT/Swing 分层架构)

---

## 一、设计灵感：Java AWT/Swing 模式

### 1.1 Java 传统架构回顾

```
┌─────────────────────────────────────────────────────────────┐
│                        Java 平台                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌───────────────┐                                        │
│   │    Swing      │  ← 轻量级组件，纯Java实现                 │
│   │  (JButton等)  │    无原生对等物(peer)                    │
│   └───────┬───────┘                                        │
│           │                                                │
│   ┌───────▼───────┐                                        │
│   │     AWT       │  ← 重量级组件，有原生对等物(peer)        │
│   │  (Button等)   │    直接调用操作系统原生组件              │
│   └───────┬───────┘                                        │
│           │                                                │
│   ┌───────▼───────┐                                        │
│   │  Native/OS    │  ← Windows/X11/Mac 操作系统             │
│   └───────────────┘                                        │
│                                                             │
│   同时存在：模型层(JavaBeans)、视图层(Swing)、控制逻辑        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 对应我们的架构映射

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CloudPSS Skill Framework                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌───────────────────────────────────────────────────────────────┐ │
│   │                      Skill Layer (技能层)                       │ │
│   │                                                               │ │
│   │   user_skill_1 | user_skill_2 | research_skill_1 | ...      │ │
│   └───────────────────────────────────────────────────────────────┘ │
│                                ↑                                    │
│   ┌───────────────────────────────────────────────────────────────┐ │
│   │                    Swing Layer (抽象API层)                      │ │
│   │                                                               │ │
│   │   PowerFlowAPI | ShortCircuitAPI | TransientAPI | OPFAPI     │ │
│   │   ↑ 这层是引擎无关的，所有工具通用                               │ │
│   └───────────────────────────────────────────────────────────────┘ │
│                                ↑                                    │
│   ┌───────────────────────────────────────────────────────────────┐ │
│   │               AWT Layer (Peered 适配层)                         │ │
│   │                                                               │ │
│   │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │ │
│   │   │ CloudPSS    │  │  pandapower │  │    PSSE     │  ...   │ │
│   │   │   Adapter   │  │   Adapter    │  │   Adapter   │         │ │
│   │   │   (Peered)  │  │   (Peered)   │  │   (Peered)  │         │ │
│   │   └─────────────┘  └─────────────┘  └─────────────┘         │ │
│   │                                                               │ │
│   │   ↓ 重量级，每个工具一套实现                                    │ │
│   └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              支撑工具层 (Beside AWT/Swing)                     │   │
│  │                                                               │   │
│  │   ModelLib | DataLib | AlgoLib | WorkflowLib | Utils        │   │
│  │   ~~~      ~~~    ~~~      ~~~         ~~~                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 二、层次职责定义

### 2.1 AWT Layer - Peered 适配层（重量级）

**职责**：直接对接各仿真引擎和工具，处理引擎特定的 API 和数据格式

**特点**：
- 每个工具一套 Adapter
- 重量级实现
- 引擎特定代码

**类比**：
```
Java AWT: Button → 调用 Windows Button / Mac Button / X11 Button
         ↓
我们: CloudPSS Adapter → 调用 CloudPSS SDK
      pandapower Adapter → 调用 pandapower API
      PSSE Adapter → 调用 PSSE API
```

**实现示例**：

```python
# AWT Layer - 每个引擎一个 Adapter
class CloudPSSPowerFlowAdapter:
    """CloudPSS 潮流计算适配器"""
    
    def run_powerflow(self, model: CloudPSSModel, config: PFConfig) -> CloudPSSResult:
        job = model.runPowerFlow()
        return job.result
    
    def extract_buses(self, result: CloudPSSResult) -> List[Bus]:
        return parse_cloudpss_table(result.getBuses())


class PandapowerPowerFlowAdapter:
    """pandapower 潮流计算适配器"""
    
    def run_powerflow(self, net: pp_net, config: PFConfig) -> PPResult:
        pp.runpowerflow(net)
        return net
    
    def extract_buses(self, net: pp_net) -> List[Bus]:
        return net.bus[['name', 'vn_kv']].to_dict('records')


class PSSERowerFlowAdapter:
    """PSSE 潮流计算适配器"""
    # ...
```

### 2.2 Swing Layer - 抽象API层（轻量级）

**职责**：定义引擎无关的抽象接口，统一不同工具的调用方式

**特点**：
- 引擎无关
- 轻量级
- 统一接口

**类比**：
```
Java Swing: JButton 不关心底层是 Windows 还是 X11
           统一接口：setText(), addActionListener(), etc.

我们: PowerFlowAPI 不关心底层是 CloudPSS 还是 pandapower
      统一接口：run(), extractBuses(), extractBranches(), etc.
```

**接口示例**：

```python
# Swing Layer - 抽象API
class PowerFlowAPI(ABC):
    """潮流计算抽象接口"""
    
    @abstractmethod
    def run(self, model: Any, config: PFConfig) -> PowerFlowResult:
        """执行潮流计算"""
        pass
    
    @abstractmethod
    def extract_buses(self, result: PowerFlowResult) -> List[BusData]:
        """提取母线数据"""
        pass
    
    @abstractmethod
    def extract_branches(self, result: PowerFlowResult) -> List[BranchData]:
        """提取支路数据"""
        pass


class ShortCircuitAPI(ABC):
    """短路计算抽象接口"""
    
    @abstractmethod
    def run(self, model: Any, fault: FaultConfig) -> ShortCircuitResult:
        pass


class TransientStabilityAPI(ABC):
    """暂态稳定抽象接口"""
    
    @abstractmethod
    def run(self, model: Any, config: TransientConfig) -> TransientResult:
        pass
```

### 2.3 Skill Layer - 技能层（用户级）

**职责**：面向终端用户的技能封装，提供友好的配置和输出

**特点**：
- 用户友好
- 配置驱动
- 标准化输出

**类比**：
```
Java Swing: 应用开发者用 JButton 构建 UI
           不需要知道 AWT Button 的细节

我们: 技能开发者用 PowerFlowAPI 实现 skill
      不需要知道 CloudPSS Adapter 的细节
```

### 2.4 支撑工具层

**职责**：在 AWT/Swing 旁边提供支撑性工具

| 工具库 | 职责 | 示例 |
|--------|------|------|
| **ModelLib** | 模型抽象和转换 | `CloudPSSModel`, `PPNet`, `PSSECase` |
| **DataLib** | 数据抽象和标准化 | `BusData`, `BranchData`, `GeneratorData` |
| **AlgoLib** | 算法实现 | `IEC60909`, `NewtonRaphson`, `FastDecoupled` |
| **WorkflowLib** | 流程编排 | `Pipeline`, `ConditionalBranch`, `Loop` |
| **Utils** | 通用工具 | `UnitConversion`, `GridVisualization` |

---

## 三、层次交互关系

### 3.1 正常调用路径

```
用户/Agent
    ↓
Skill Layer (用户技能)
    ↓
Swing Layer (PowerFlowAPI.run())
    ↓
AWT Layer (Adapter 实现)
    ↓
仿真引擎 (CloudPSS/pandapower/PSSE)
```

### 3.2 模型转换路径

```
CloudPSS Model ←→ ModelLib ←→ pandapower Net
                    ↓
              DataLib (统一格式)
                    ↓
              AlgoLib (通用算法)
```

### 3.3 多工具混合路径

```
Pipeline:
┌─────────────────────────────────────────────────────────────┐
│ WorkflowLib (流程编排)                                        │
│                                                             │
│  Step1: pandapower (快速初筛)                                 │
│      ↓                                                      │
│  Step2: ModelLib.convert() (格式转换)                         │
│      ↓                                                      │
│  Step3: CloudPSS (精确验证)                                   │
│      ↓                                                      │
│  Step4: DataLib.merge() (结果整合)                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 四、关键设计决策

### 决策1：AWT Adapter 的粒度

```
选项A：每个工具一套完整 Adapter (PowerFlow + ShortCircuit + Transient...)
选项B：每个分析类型一个 Adapter 家族 (CloudPSS族 / pandapower族 / PSSE族)

推荐：选项B - 按分析类型组织
├── adapters/
│   ├── powerflow/
│   │   ├── cloudpss_pf.py
│   │   ├── pandapower_pf.py
│   │   └── psse_pf.py
│   ├── shortcircuit/
│   │   ├── cloudpss_sc.py
│   │   ├── pandapower_sc.py
│   │   └── psse_sc.py
│   └── transient/
│       ├── cloudpss_transient.py
│       └── simulink_transient.py
```

### 决策2：Swing API 的实现方式

```
选项A：每个 API 一个基类，继承决定实现
       class PowerFlowAPI:  # 抽象基类
           pass
       class CloudPSSPowerFlow(PowerFlowAPI):  # CloudPSS 实现
           pass

选项B：每个 API 一个工厂，根据配置返回实现
       class PowerFlowAPIFactory:
           @staticmethod
           def create(engine: str) -> PowerFlowAPI:
               if engine == "cloudpss":
                   return CloudPSSPowerFlow()
               elif engine == "pandapower":
                   return PandapowerPowerFlow()

推荐：选项A - 更符合 OOP 设计，易于扩展
```

### 决策3：ModelLib 的转换策略

```
转换策略：

严格转换 (Lossless)
  CloudPSS Model ←→ PP Net
  - 拓扑完整保留
  - 参数一一对应
  - 控制逻辑丢失

近似转换 (Lossy)
  CloudPSS Model → PP Net
  - 提取主要拓扑
  - 参数近似
  - 控制逻辑转为静态模型

语义转换 (Semantic)
  PP Net → CloudPSS Model
  - 识别等值模型
  - 构建简化动态模型
```

---

## 五、实施路线图

### Phase 1: 核心框架 (AWT + Swing 基础)

```
目标：建立 AWT/Swing 分层架构

交付物：
├── cloudpss_skills/
│   ├── awt/                    # 新增：AWT 适配层
│   │   ├── adapters/
│   │   │   ├── cloudpss/       # CloudPSS 适配器
│   │   │   └── pandapower/    # pandapower 适配器
│   │   └── base.py            # Adapter 基类
│   ├── swing/                 # 新增：Swing 抽象层
│   │   ├── apis/              # 抽象 API
│   │   │   ├── powerflow.py
│   │   │   └── shortcircuit.py
│   │   └── base.py            # API 基类
│   ├── lib/                   # 新增：支撑工具层
│   │   ├── model/             # ModelLib
│   │   ├── data/              # DataLib
│   │   ├── algo/              # AlgoLib
│   │   └── workflow/         # WorkflowLib
│   └── skills/                # 现有技能层
│       └── ...
```

### Phase 2: 扩展工具支持

```
目标：支持更多仿真引擎

交付物：
├── awt/adapters/
│   ├── psse/                  # PSSE 适配器
│   ├── bpa/                   # BPA 适配器
│   └── simulink/              # Simulink 适配器
```

### Phase 3: 研究技能封装

```
目标：将论文算法转化为技能

交付物：
├── skills/research/
│   ├── lvrt_short_circuit/    # LVRT 短路电流分析
│   ├── advanced_voltage_stab/ # 高级电压稳定
│   └── protection_advanced/   # 高级保护整定
```

---

## 六、架构优势

### 6.1 可扩展性

```
新增工具支持：
只需新增一个 AWT Adapter，
Swing API 和 Skills 自动获得支持

示例：添加 PSSE 支持
├── awt/adapters/
│   └── psse/
│       ├── powerflow.py
│       ├── shortcircuit.py
│       └── ...

现有 skills 无需修改！
```

### 6.2 可替换性

```
切换底层引擎：
只需更换 AWT Adapter 实现，
用户无感知

示例：从 CloudPSS 切换到 pandapower
# 用户配置
config:
  engine: pandapower  # 只需改这一行

现有 skills 代码不变！
```

### 6.3 可测试性

```
分层测试策略：
├── AWT Layer: mock 仿真引擎
├── Swing Layer: mock AWT Adapter
└── Skill Layer: mock Swing API

每层独立测试！
```

---

## 七、与现有架构的对比

### 7.1 旧架构（平铺式）

```
skills/
├── power_flow.py      # 直接调用 CloudPSS SDK
├── power_flow_pp.py   # 直接调用 pandapower
├── power_flow_psse.py  # 直接调用 PSSE
└── ...
问题：
- 代码重复
- 接口不一致
- 难以混合使用
```

### 7.2 新架构（AWT/Swing 分层）

```
awt/adapters/          ← 引擎特定实现
├── cloudpss/pf.py
├── pandapower/pf.py
└── psse/pf.py

swing/apis/            ← 统一抽象接口
└── powerflow.py        ← 引擎无关

skills/                ← 用户技能
└── power_flow.py      ← 调用 Swing API
```

---

## 八、下一步行动

### 立即开始

1. [ ] 设计 `cloudpss_skills/awt/` 目录结构
2. [ ] 实现第一个 AWT Adapter：`CloudPSSPowerFlowAdapter`
3. [ ] 实现第一个 Swing API：`PowerFlowAPI`
4. [ ] 重构现有 `power_flow.py` 使用新的分层架构

### 待确认

1. Adapter 基类接口设计
2. API 基类抽象程度
3. ModelLib 的转换精度要求

---

**文档状态**: 战略规划中  
**负责人**: Claude Code (Agent)  
**最后更新**: 2026-04-16  
**版本**: 2.0.0 (AWT/Swing 分层架构)
