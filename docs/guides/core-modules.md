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

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.1.0 | 2024-01 | 新增 job_runner, exporter, model_utils 模块 |
