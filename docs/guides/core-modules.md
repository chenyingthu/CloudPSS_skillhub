# CloudPSS Skills 核心模块文档

本文档介绍 `cloudpss_skills.core` 模块中提供的可复用核心功能。

## 模块概览

```
cloudpss_skills/core/
├── __init__.py              # 统一导出
├── base.py                  # 基础类和接口定义
├── config.py                # 配置加载和验证
├── registry.py              # 技能注册表
├── auth_utils.py            # 认证工具
├── utils.py                 # 通用工具函数
├── job_runner.py            # 任务运行器 ⭐
├── exporter.py              # 结果导出器 ⭐
├── model_utils.py           # 模型操作工具 ⭐
├── network_equivalent.py     # 网络等值计算
├── emt_fault_core.py        # EMT故障仿真核心
├── emt_measurement_core.py  # EMT量测核心
└── sync_support_core.py     # 同步机支持核心
```

## 已使用核心模块的技能

以下技能已迁移到核心模块：

| 技能 | 使用模块 |
|------|----------|
| `power_flow` | `run_powerflow_and_wait`, `OutputConfig`, `save_json` |
| `n1_security` | `reload_model`, `run_powerflow_and_wait`, `remove_component_safe` |
| `voltage_stability` | `clone_model`, `run_powerflow_and_wait`, `save_json/csv/md` |
| `batch_powerflow` | `reload_model`, `run_powerflow_and_wait` |
| `emt_simulation` | `run_emt_and_wait`, `OutputConfig` |
| `param_scan` | `clone_model`, `run_powerflow_and_wait`, `run_emt_and_wait` |
| `short_circuit` | `clone_model`, `run_emt_and_wait` |
| `n2_security` | `clone_model`, `reload_model`, `run_powerflow_and_wait` |
| `maintenance_security` | `clone_model`, `reload_model`, `run_powerflow_and_wait` |
| `contingency_analysis` | `clone_model`, `reload_model`, `run_powerflow_and_wait` |

## Job Runner 模块 (`job_runner.py`)

### 核心功能

#### `run_powerflow_and_wait()`
运行潮流计算并等待完成。

```python
from cloudpss_skills.core import run_powerflow_and_wait, OutputConfig

job_result = run_powerflow_and_wait(model, config, log_func=log)

if job_result.success:
    print(f"潮流收敛，Job ID: {job_result.job.id}")
    print(f"耗时: {job_result.waited_seconds:.1f}s")
else:
    print(f"潮流失败: {job_result.error}")
```

#### `run_emt_and_wait()`
运行EMT仿真并等待完成。

```python
from cloudpss_skills.core import run_emt_and_wait

job_result = run_emt_and_wait(model, config, timeout=300, log_func=log)

if job_result.success:
    result = job_result.result
    plots = list(result.getPlots())
```

#### `PollConfig` 配置类
```python
from cloudpss_skills.core import PollConfig

config = PollConfig(
    max_wait=120,      # 最大等待时间（秒）
    poll_seconds=2,    # 轮询间隔（秒）
)
```

### 数据类

#### `JobResult`
```python
@dataclass
class JobResult:
    job: Any              # CloudPSS Job 对象
    status: JobStatus    # 任务状态
    result: Any          # 任务结果
    error: Optional[str] # 错误信息
    duration: float      # 总耗时
    waited_seconds: float # 等待时间
    converged: bool       # 是否收敛
```

#### `BatchJobResult`
```python
@dataclass
class BatchJobResult:
    total: int           # 总任务数
    succeeded: int      # 成功数
    failed: int         # 失败数
    results: List[JobResult]
    start_time: datetime
    end_time: Optional[datetime]

    @property
    def success_rate(self) -> float:
        return self.succeeded / self.total if self.total > 0 else 0
```

---

## Exporter 模块 (`exporter.py`)

### 核心功能

#### `save_json()`
将数据保存为JSON文件。

```python
from cloudpss_skills.core import save_json, OutputConfig

output = OutputConfig(
    path="./results/",
    prefix="my_result",
    timestamp=True,
)

export_result = save_json(
    data={"key": "value"},
    output_config=output,
    description="我的结果",
)

if export_result.success:
    print(f"已保存: {export_result.filepath}")
    print(f"大小: {export_result.size} bytes")
```

#### `save_csv()`
将数据保存为CSV文件。

```python
from cloudpss_skills.core import save_csv

data = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
]

export_result = save_csv(
    data=data,
    output_config=output,
    headers=["name", "age"],
    description="人员信息",
)
```

#### `generate_report()`
生成Markdown报告。

```python
from cloudpss_skills.core import generate_report

content = """# 分析报告

## 汇总
- 总数: 100
- 成功率: 95%

## 详细结果
| 项目 | 状态 |
|------|------|
| Test1 | ✓ |
"""

export_result = generate_report(content, output, suffix="report")
```

### 配置类

#### `OutputConfig`
```python
from cloudpss_skills.core import OutputConfig

output = OutputConfig(
    path="./results/",        # 输出目录
    prefix="output",          # 文件名前缀
    format="json",            # 格式: json/csv/markdown
    timestamp=True,           # 是否添加时间戳
    ensure_ascii=False,       # 是否转义非ASCII字符
    indent=2,                 # JSON缩进
)

# 生成文件名
filename = output.get_filename()  # "output_20240101_120000.json"
```

---

## Model Utils 模块 (`model_utils.py`)

### 核心功能

#### `clone_model()`
创建模型的深拷贝，用于仿真修改。

```python
from cloudpss_skills.core import clone_model

# 创建工作副本
working_model = clone_model(base_model)

# 修改工作副本
working_model.updateComponent(component_id, args={"pf_P": {"source": "200", "ɵexp": ""}})

# 运行仿真（不影响原始模型）
job = working_model.runPowerFlow()
```

#### `reload_model()`
从源重新加载模型。

```python
from cloudpss_skills.core import reload_model

# 从云端加载
model = reload_model("model/holdme/IEEE39", source="cloud", config)

# 从本地加载
model = reload_model("/path/to/model.yaml", source="local")
```

#### `get_components_by_definition()`
按定义类型获取组件。

```python
from cloudpss_skills.core import get_components_by_definition

# 获取所有母线
buses = get_components_by_definition(model, "model/CloudPSS/_newBus_3p")

# 获取所有线路
lines = get_components_by_definition(model, "model/CloudPSS/TransmissionLine")

# 获取所有发电机
gens = get_components_by_definition(model, "model/CloudPSS/_newGenerator")

for key, bus in buses.items():
    print(f"{bus['label']}: {bus['name']}")
```

#### `remove_component_safe()`
安全移除组件。

```python
from cloudpss_skills.core import remove_component_safe

if remove_component_safe(model, component_id):
    print("组件已移除")
else:
    print("移除失败")
```

#### `matches_label()`
模糊匹配标签。

```python
from cloudpss_skills.core import matches_label

matches_label("BUS_1", "bus_1")      # True
matches_label("Bus30", "bus_30")     # True
matches_label("newBus_3p-1", "1")   # True (数字匹配)
```

### 快速参考

| 函数 | 用途 |
|------|------|
| `clone_model()` | 深拷贝模型 |
| `reload_model()` | 重新加载模型 |
| `get_or_clone_model()` | 获取或克隆模型 |
| `get_buses()` | 获取所有母线 |
| `get_lines()` | 获取所有线路 |
| `get_generators()` | 获取所有发电机 |
| `find_component_by_label()` | 按标签查找组件 |
| `remove_component_safe()` | 安全移除组件 |
| `update_component_args()` | 更新组件参数 |
| `matches_label()` | 模糊标签匹配 |

---

## 在技能中使用核心模块

### 标准技能结构

```python
from cloudpss_skills.core import (
    SkillBase,
    SkillResult,
    SkillStatus,
    Artifact,
    LogEntry,
    register,
    setup_auth,
    reload_model,
    clone_model,
    run_powerflow_and_wait,
    run_emt_and_wait,
    OutputConfig,
    save_json,
    save_csv,
    generate_report,
)

@register
class MySkill(SkillBase):
    @property
    def name(self) -> str:
        return "my_skill"

    def run(self, config: dict) -> SkillResult:
        start_time = datetime.now()
        logs = []
        artifacts = []

        def log(level: str, message: str):
            logs.append(LogEntry(timestamp=datetime.now(), level=level, message=message))

        try:
            # 1. 认证
            setup_auth(config)
            log("INFO", "认证成功")

            # 2. 获取模型
            model_config = config["model"]
            model = reload_model(
                model_config["rid"],
                model_config.get("source", "cloud"),
                config,
            )

            # 3. 创建工作副本
            working_model = clone_model(model)

            # 4. 运行仿真
            job_result = run_powerflow_and_wait(working_model, config, log_func=log)

            # 5. 导出结果
            output = OutputConfig(
                path=config.get("output", {}).get("path", "./results/"),
                prefix="my_skill",
            )
            export_result = save_json({"data": "result"}, output)

            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data={"result": "data"},
                artifacts=[export_result.artifact] if export_result.artifact else [],
                logs=logs,
            )

        except Exception as e:
            log("ERROR", str(e))
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                logs=logs,
                error=str(e),
            )
```

---

## 最佳实践

### 1. 使用核心模块而非重复代码

**推荐**:
```python
from cloudpss_skills.core import clone_model, run_powerflow_and_wait

working_model = clone_model(base_model)
job_result = run_powerflow_and_wait(working_model, config)
```

**不推荐**:
```python
from copy import deepcopy
import time

working_model = Model(deepcopy(base_model.toJSON()))
job = working_model.runPowerFlow()

max_wait = 120
waited = 0
while waited < max_wait:
    status = job.status()
    if status == 1:
        break
    time.sleep(2)
    waited += 2
```

### 2. 使用 `remove_component_safe()` 而非直接调用

**推荐**:
```python
from cloudpss_skills.core import remove_component_safe

if remove_component_safe(model, component_id):
    log("INFO", "组件已移除")
```

### 3. 使用 `OutputConfig` 管理输出路径

**推荐**:
```python
from cloudpss_skills.core import OutputConfig, save_json

output = OutputConfig(
    path=config.get("output", {}).get("path", "./results/"),
    prefix="my_result",
)
export_result = save_json(data, output)
```

---

## 技能相互逻辑

### 技能依赖关系

技能之间存在以下依赖关系：

```
power_flow (基础)
    ├── n1_security (依赖基线潮流)
    ├── voltage_stability (依赖基线潮流)
    ├── n2_security (依赖基线潮流)
    ├── contingency_analysis (依赖基线潮流)
    ├── maintenance_security (依赖基线潮流)
    └── batch_powerflow (多次调用 power_flow)

emt_simulation (独立)
    ├── short_circuit (依赖 EMT)
    └── param_scan (可依赖 EMT 或 power_flow)
```

### 技能组合使用

#### 1. 完整安全评估流程
```
power_flow (基线) → n1_security → n2_security → contingency_analysis
```

```python
# 示例：完整安全评估
configs = [
    {"skill": "power_flow", "model": {"rid": "model/holdme/IEEE39"}},
    {"skill": "n1_security", "model": {"rid": "model/holdme/IEEE39"}},
    {"skill": "contingency_analysis", "model": {"rid": "model/holdme/IEEE39"}, "contingency": {"level": "N-1"}},
]
```

#### 2. 电压稳定性研究
```
power_flow (基线) → voltage_stability (PV曲线)
```

#### 3. EMT故障分析
```
emt_simulation (基线) → short_circuit (短路计算)
                    → param_scan (参数扫描)
```

### 技能间数据传递

#### 通过配置传递
```python
# 技能A：将结果路径传递给技能B
skill_a_result = run_skill_a(config_a)
config_b = {
    "skill": "n1_security",
    "model": {"rid": "model/holdme/IEEE39"},
    "output": {
        "path": skill_a_result.artifacts[0].path,  # 复用输出路径
    }
}
```

#### 通过 SkillResult.data 传递
```python
# 技能A的结果作为技能B的参考
skill_a = get_skill("power_flow")
result_a = skill_a.run(config_a)

# 提取关键数据传递给技能B
config_b = {
    "skill": "voltage_stability",
    "model": {"rid": "model/holdme/IEEE39"},
    "monitoring": {
        "buses": result_a.data.get("critical_buses", []),  # 使用技能A识别的薄弱母线
    }
}
```

---

## 调用最佳实践

### 1. 模型加载策略

#### 何时使用 `reload_model()` vs `clone_model()`

| 场景 | 方法 | 原因 |
|------|------|------|
| 批量仿真（每个场景独立修改） | `clone_model(base_model)` | 避免重复网络请求 |
| 需要最新模型状态 | `reload_model()` | 获取云端最新版本 |
| 检修模拟（需要先停运再复核） | 初始`reload_model()` + 后续`clone_model()` | 首场景用reload，后续用clone |

```python
# ✅ 推荐：批量仿真场景
base_model = reload_model(model_rid, source, config)  # 只加载一次
for scenario in scenarios:
    working = clone_model(base_model)  # 每个场景克隆
    modify_and_simulate(working, scenario)

# ✅ 推荐：检修场景
model = reload_model(model_rid, source, config)  # 获取原始状态
# 检修态分析...
working = clone_model(model)  # 用于后续N-1复核
```

### 2. 错误处理模式

#### 分层错误处理
```python
def run(self, config: Dict) -> SkillResult:
    try:
        setup_auth(config)  # 认证错误：立即失败
        model = reload_model(...)  # 模型加载错误：立即失败
        
        results = []
        for scenario in scenarios:
            try:
                result = self._run_single_scenario(model, scenario)
                results.append(result)
            except RuntimeError as e:
                # 单场景失败：记录但继续
                results.append({"scenario": scenario, "error": str(e)})
        
        if not results:
            return SkillResult(status=SkillStatus.FAILED, error="所有场景失败")
        
        return self._aggregate_results(results)
    
    except (ConnectionError, FileNotFoundError) as e:
        # 致命错误：完全失败
        return SkillResult(status=SkillStatus.FAILED, error=str(e))
```

#### 使用 `JobResult` 进行仿真错误检查
```python
job_result = run_powerflow_and_wait(model, config)

if not job_result.success:
    # 区分不同失败原因
    if "timeout" in (job_result.error or "").lower():
        raise RuntimeError("潮流计算超时")
    else:
        raise RuntimeError(f"潮流计算失败: {job_result.error}")
```

### 3. 性能优化

#### 避免重复加载
```python
# ❌ 错误：每个场景都重新加载
for branch in branches:
    model = reload_model(model_rid, source, config)  # 慢！
    remove_component(model, branch)
    run_powerflow(model)

# ✅ 正确：加载一次，克隆多次
model = reload_model(model_rid, source, config)
for branch in branches:
    working = clone_model(model)  # 快！
    remove_component(working, branch)
    run_powerflow(working)
```

#### 使用批量操作
```python
# ❌ 低效：逐个更新
for comp in components:
    model.updateComponent(comp.id, args={...})

# ✅ 高效：收集后批量更新（如果SDK支持）
updates = {comp.id: {...} for comp in components}
model.updateComponents(updates)
```

### 4. 日志记录规范

#### 结构化日志
```python
def log(level: str, message: str):
    logs.append(LogEntry(timestamp=datetime.now(), level=level, message=message))
    # 添加上下文前缀
    getattr(logger, level.lower())(f"[{self.name}] {message}")

# 使用示例
log("INFO", f"加载模型: {model.name}")
log("DEBUG", f"支路数: {len(branches)}")
log("WARNING", f"潮流不收敛: {branch['name']}")
log("ERROR", f"仿真异常: {e}")
```

### 5. 输出管理

#### 使用统一的 OutputConfig
```python
# ✅ 推荐：统一的输出管理
output = OutputConfig(
    path=config.get("output", {}).get("path", "./results/"),
    prefix=f"{self.name}_{scenario_id}",
    timestamp=True,
)

# JSON结果
json_result = save_json(data, output, suffix="data")
artifacts.append(json_result.artifact)

# CSV表格
csv_result = save_csv(table_data, output, suffix="table", headers=headers)
artifacts.append(csv_result.artifact)

# Markdown报告
md_result = generate_report(report_content, output, suffix="report")
artifacts.append(md_result.artifact)
```

### 6. 技能链式调用

#### 创建可复用的研究流程
```python
class SecurityAssessmentPipeline:
    def __init__(self, model_rid: str, config: dict):
        self.model_rid = model_rid
        self.config = config
        self.results = {}
    
    def run(self) -> Dict[str, SkillResult]:
        # 1. 基线潮流
        pf = get_skill("power_flow")
        self.results["baseline"] = pf.run({
            "skill": "power_flow",
            "model": {"rid": self.model_rid},
            **self.config
        })
        
        # 2. N-1安全筛查
        n1 = get_skill("n1_security")
        self.results["n1"] = n1.run({
            "skill": "n1_security",
            "model": {"rid": self.model_rid},
            "output": {"path": self.results["baseline"].artifacts[0].path},
            **self.config
        })
        
        # 3. 电压稳定性
        vs = get_skill("voltage_stability")
        self.results["voltage"] = vs.run({
            "skill": "voltage_stability",
            "model": {"rid": self.model_rid},
            "monitoring": {"buses": self._get_critical_buses()},
            **self.config
        })
        
        return self.results
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.1.0 | 2026-04 | 新增 job_runner, exporter, model_utils 模块 |
| 1.0.0 | 2026-04 | 初始版本 |
