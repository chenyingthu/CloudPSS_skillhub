# CloudPSS SkillHub 修复与实现计划 V2

> **版本**: 2.0  
> **更新日期**: 2026-04-23  
> **核心理念**: 坚持实现既定设计目标，而非删除功能  
> **预计工期**: 12-14 周

---

## 📋 执行摘要

### 调整后的策略
原计划的"删除未实现技能"调整为"**实现所有设计功能**"

### 问题与目标
| 类别 | 数量 | 处理方式 |
|------|------|---------|
| 虚假/空测试 | 340+ | 🔴 清理 (Week 1-2) |
| 逻辑错误 | 15+ | 🔴 修复 (Week 3-4) |
| 未实现技能 | 11 | 🟢 **实现** (Week 5-10) |
| 安全问题 | 5+ | 🔴 修复 (Week 3-4) |
| 测试质量 | 200+ 需改进 | 🟡 提升 (Week 11-12) |

### 新时间表
```
Week 1-2:   [Phase 1] ████████████████████ 清理虚假测试
Week 3-4:   [Phase 2] ████████████████████ 修复核心缺陷
Week 5-10:  [Phase 3] ██████████████████████████████ 实现未完成技能
Week 11-12: [Phase 4] ████████████████████ 提升测试质量
Week 13-14: [Phase 5] ████████████████████ 回归验证与文档
```

---

## 🎯 重点：11 个待实现技能详细规划

基于 `IMPLEMENTATION_PLAN.md` 和代码中的 TODO，以下是实现优先级：

### 优先级 P0 (核心数据导出)

#### 1. HDF5 Export (`tools/hdf5_export.py`)
**设计目标**: 导出仿真结果为 HDF5 标准格式

**TODO 列表**:
- [ ] Add validation logic (line 17)
- [ ] Implement _export_to_hdf5 (line 21)
- [ ] Implement _create_index (line 25)
- [ ] Implement read_hdf5 (line 29)
- [ ] Implement list_datasets (line 33)
- [ ] Implement skill logic (line 42)

**实现方案**:
```python
import h5py
import numpy as np
from typing import Dict, List, Any

class HDF5ExportTool:
    """HDF5 数据导出工具"""
    
    def run(self, config: Dict) -> SkillResult:
        # 1. 验证输入配置
        self._validate_config(config)
        
        # 2. 读取仿真结果
        results = self._load_results(config["source"])
        
        # 3. 创建 HDF5 文件
        output_path = config["output"]["path"]
        with h5py.File(output_path, 'w') as f:
            # 创建元数据组
            meta = f.create_group('metadata')
            meta.attrs['skill'] = config['skill']
            meta.attrs['timestamp'] = datetime.now().isoformat()
            
            # 创建数据集
            for name, data in results.items():
                f.create_dataset(name, data=np.array(data))
        
        return SkillResult(status=SkillStatus.SUCCESS, data={"path": output_path})
```

**验收标准**:
- [ ] 可以导出标准 HDF5 格式
- [ ] 支持读取和列出数据集
- [ ] 包含完整的元数据
- [ ] 单元测试覆盖率 > 80%
- [ ] 集成测试通过

**工期**: 3 天

---

#### 2. COMTRADE Export (`tools/comtrade_export.py`)
**设计目标**: 导出 COMTRADE 格式波形数据 (电力系统标准)

**TODO 列表**:
- [ ] Add validation logic (line 18)
- [ ] Implement _generate_cfg_header (line 22)
- [ ] Implement _generate_dat_record (line 26)
- [ ] Implement _format_timestamp (line 30)
- [ ] Implement skill logic (line 39)

**实现方案**:
```python
class ComtradeExportTool:
    """COMTRADE 格式导出工具 (IEEE C37.111-2013)"""
    
    def run(self, config: Dict) -> SkillResult:
        # 1. 读取波形数据
        waveforms = self._load_waveforms(config["source"])
        
        # 2. 生成 .cfg 配置文件
        cfg_content = self._generate_cfg(
            station_name=config.get("station", "STATION"),
            channels=waveforms.keys(),
            sample_rate=config.get("sample_rate", 1000)
        )
        
        # 3. 生成 .dat 数据文件
        dat_content = self._generate_dat(waveforms)
        
        # 4. 保存文件
        base_path = config["output"]["path"]
        self._save_files(base_path, cfg_content, dat_content)
        
        return SkillResult(status=SkillStatus.SUCCESS)
    
    def _generate_cfg(self, station_name: str, channels: List[str], 
                      sample_rate: float) -> str:
        """生成 COMTRADE .cfg 文件内容"""
        lines = [
            station_name,  # 变电站名称
            "1,1A",        # 版本号
            str(len(channels)),  # 通道数
            # ... 更多格式
        ]
        return "\n".join(lines)
```

**验收标准**:
- [ ] 生成标准 COMTRADE (.cfg + .dat) 文件
- [ ] 可被标准 COMTRADE 查看器读取
- [ ] 支持 ASCII 和 BINARY 格式
- [ ] 单元测试覆盖率 > 80%

**工期**: 3 天

---

### 优先级 P1 (工作流与批处理)

#### 3. Batch Task Manager (`tools/batch_task_manager.py`)
**设计目标**: 并行执行多个仿真任务

**TODO**: Implement batch_task_manager logic (line 54)

**实现方案**:
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any

class BatchTaskManager:
    """批处理任务管理器"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def run_batch(self, tasks: List[Dict]) -> List[SkillResult]:
        """并行执行多个任务"""
        # 1. 任务依赖分析
        task_graph = self._build_dependency_graph(tasks)
        
        # 2. 按依赖层级执行
        results = {}
        for level in task_graph.topological_sort():
            # 并行执行当前层级的任务
            futures = [
                self._run_single_task(task) 
                for task in level
            ]
            level_results = await asyncio.gather(*futures)
            results.update(dict(zip(level, level_results)))
        
        return results
    
    async def _run_single_task(self, task_config: Dict) -> SkillResult:
        """执行单个任务"""
        skill = get_skill(task_config["skill"])
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, skill.run, task_config
        )
    
    def _build_dependency_graph(self, tasks: List[Dict]) -> TaskGraph:
        """构建任务依赖图"""
        graph = TaskGraph()
        for task in tasks:
            graph.add_node(task["id"], task)
            for dep in task.get("depends_on", []):
                graph.add_edge(dep, task["id"])
        return graph
```

**验收标准**:
- [ ] 支持并行执行多个任务
- [ ] 正确处理任务依赖
- [ ] 失败任务不影响其他任务
- [ ] 提供进度报告
- [ ] 单元测试覆盖率 > 80%

**工期**: 5 天

---

#### 4. Study Pipeline (`tools/study_pipeline.py`)
**设计目标**: 研究流水线编排（设计文档 Week 5-6 重点）

**TODO 列表**:
- [ ] Add validation logic (line 15)
- [ ] Implement _expand_pipeline (line 19)
- [ ] Implement _get_ready_steps (line 23)
- [ ] Implement _evaluate_condition (line 27)
- [ ] Implement _resolve_var_path (line 31)
- [ ] Implement _resolve_config (line 35)
- [ ] Implement _resolve_string (line 39)
- [ ] Implement skill logic (line 48)

**实现方案** (基于设计文档):
```python
from typing import List, Dict, Callable, Optional
import jinja2

class StudyPipelineTool:
    """研究流水线编排工具"""
    
    def __init__(self):
        self.context = {}  # 变量上下文
        self.results = {}  # 步骤结果
    
    def run(self, config: Dict) -> SkillResult:
        """执行流水线"""
        # 1. 展开流水线定义
        pipeline = self._expand_pipeline(config["pipeline"])
        
        # 2. 按依赖顺序执行步骤
        while True:
            ready_steps = self._get_ready_steps(pipeline)
            if not ready_steps:
                break
            
            for step in ready_steps:
                # 评估条件
                if not self._evaluate_condition(step.get("condition")):
                    continue
                
                # 解析配置（变量替换）
                resolved_config = self._resolve_config(step["config"])
                
                # 执行步骤
                result = self._execute_step(step, resolved_config)
                self.results[step["name"]] = result
                self.context[f"steps.{step['name']}"] = result.data
        
        return SkillResult(status=SkillStatus.SUCCESS, data=self.results)
    
    def _expand_pipeline(self, pipeline_def: Dict) -> Pipeline:
        """展开流水线定义，处理循环和模板"""
        steps = []
        for step_def in pipeline_def["steps"]:
            if "for_each" in step_def:
                # 展开循环
                items = self._resolve_var_path(step_def["for_each"]["in"])
                for item in items:
                    steps.append(self._instantiate_step(step_def, item))
            else:
                steps.append(Step.from_dict(step_def))
        return Pipeline(steps)
    
    def _resolve_config(self, config: Dict) -> Dict:
        """解析配置，替换变量引用"""
        template = jinja2.Template(str(config))
        resolved = template.render(ctx=self.context, steps=self.results)
        return eval(resolved)  # 安全考虑：使用 ast.literal_eval
    
    def _evaluate_condition(self, condition: Optional[str]) -> bool:
        """评估条件表达式"""
        if not condition:
            return True
        template = jinja2.Template(f"{{{{ {condition} }}}}")
        result = template.render(ctx=self.context)
        return result.lower() == "true"
```

**验收标准**:
- [ ] 支持顺序执行
- [ ] 支持条件分支
- [ ] 支持循环 (for_each)
- [ ] 支持变量传递和模板
- [ ] 支持步骤依赖
- [ ] 单元测试覆盖率 > 80%
- [ ] 与设计文档一致

**工期**: 6 天

---

#### 5. Config Batch Runner (`tools/config_batch_runner.py`)
**设计目标**: 多配置批量运行

**TODO**: Implement config_batch_runner logic (line 33)

**实现方案**:
```python
class ConfigBatchRunner:
    """多配置批量运行器"""
    
    def run(self, config: Dict) -> SkillResult:
        """批量运行多个配置"""
        base_config = config["base_config"]
        variations = config["variations"]
        
        results = []
        for variation in variations:
            # 合并基础配置和变体
            merged = self._merge_configs(base_config, variation)
            
            # 执行
            skill = get_skill(merged["skill"])
            result = skill.run(merged)
            results.append({
                "variation": variation.get("name", "unnamed"),
                "result": result
            })
        
        # 汇总结果
        summary = self._summarize_results(results)
        
        return SkillResult(status=SkillStatus.SUCCESS, data={
            "results": results,
            "summary": summary
        })
    
    def _merge_configs(self, base: Dict, variation: Dict) -> Dict:
        """深度合并配置"""
        import copy
        merged = copy.deepcopy(base)
        self._deep_update(merged, variation)
        return merged
```

**验收标准**:
- [ ] 支持配置变体
- [ ] 深度合并配置
- [ ] 结果汇总和对比
- [ ] 单元测试覆盖率 > 80%

**工期**: 3 天

---

### 优先级 P2 (模型与通道管理)

#### 6. Auto Channel Setup (`tools/auto_channel_setup.py`)
**设计目标**: 自动配置 EMT 输出通道

**TODO 列表**:
- [ ] Add validation logic (line 15)
- [ ] Implement _build_voltage_channel (line 19)
- [ ] Implement _build_current_channel (line 23)
- [ ] Implement _build_power_channel (line 27)
- [ ] Implement _build_frequency_channel (line 31)
- [ ] Implement _generate_output_config (line 35)
- [ ] Implement _group_channels_by_type (line 39)
- [ ] Implement skill logic (line 48)

**实现方案**:
```python
class AutoChannelSetupTool:
    """自动量测通道配置工具"""
    
    def run(self, config: Dict) -> SkillResult:
        """自动配置输出通道"""
        model = self._load_model(config["model"])
        
        channels = []
        
        # 1. 为所有母线添加电压通道
        if config.get("auto_voltage", True):
            for bus in model.get_buses():
                ch = self._build_voltage_channel(bus)
                channels.append(ch)
        
        # 2. 为所有线路添加电流通道
        if config.get("auto_current", True):
            for line in model.get_lines():
                ch = self._build_current_channel(line)
                channels.append(ch)
        
        # 3. 为所有发电机添加功率通道
        if config.get("auto_power", True):
            for gen in model.get_generators():
                ch = self._build_power_channel(gen)
                channels.append(ch)
        
        # 4. 生成输出配置
        output_config = self._generate_output_config(channels)
        
        # 5. 应用配置到模型
        self._apply_to_model(model, output_config)
        
        return SkillResult(status=SkillStatus.SUCCESS, data={
            "channels_configured": len(channels),
            "config": output_config
        })
    
    def _build_voltage_channel(self, bus: Bus) -> Channel:
        """构建电压量测通道"""
        return Channel(
            name=f"V_{bus.name}",
            component=bus.id,
            signal="voltage",
            type="analog",
            unit="kV"
        )
```

**验收标准**:
- [ ] 自动识别模型组件
- [ ] 支持电压/电流/功率/频率通道
- [ ] 生成有效的 EMT 输出配置
- [ ] 单元测试覆盖率 > 80%

**工期**: 4 天

---

#### 7. Model Hub (`tools/model_hub.py`)
**设计目标**: 算例中心 - 多服务器统一管理（设计文档重点）

**TODO**: Implement model_hub logic (line 73)

**实现方案**:
```python
from typing import Dict, List, Optional

class ModelHub:
    """模型中心 - 多服务器统一管理"""
    
    def __init__(self):
        self.servers: Dict[str, ServerConfig] = {}
        self.cache: Dict[str, ModelCache] = {}
    
    def register_server(self, name: str, config: Dict):
        """注册服务器"""
        self.servers[name] = ServerConfig(**config)
    
    def search_models(self, query: str, servers: List[str] = None) -> List[ModelInfo]:
        """跨服务器搜索模型"""
        results = []
        servers_to_search = servers or list(self.servers.keys())
        
        for server_name in servers_to_search:
            server = self.servers[server_name]
            models = self._search_server(server, query)
            for model in models:
                results.append(ModelInfo(
                    rid=model["rid"],
                    name=model["name"],
                    server=server_name,
                    owner=model["owner"],
                    modified=model["modified"]
                ))
        
        return results
    
    def fetch_model(self, rid: str, server: str = None) -> Model:
        """获取模型（支持跨服务器）"""
        if server:
            return self._fetch_from_server(rid, self.servers[server])
        
        # 自动发现服务器
        for server_name, config in self.servers.items():
            try:
                return self._fetch_from_server(rid, config)
            except ModelNotFoundError:
                continue
        
        raise ModelNotFoundError(f"Model {rid} not found in any server")
    
    def sync_model(self, rid: str, from_server: str, to_servers: List[str]):
        """同步模型到多个服务器"""
        model = self.fetch_model(rid, from_server)
        
        for target in to_servers:
            self._upload_to_server(model, self.servers[target])
```

**验收标准**:
- [ ] 支持多服务器注册
- [ ] 跨服务器搜索模型
- [ ] 模型同步功能
- [ ] 缓存机制
- [ ] 单元测试覆盖率 > 80%
- [ ] 与设计文档一致

**工期**: 5 天

---

#### 8. Model Builder (`tools/model_builder.py`)
**设计目标**: 模型构建工具

**TODO 列表**:
- [ ] Implement _coerce_scalar_value (line 16)
- [ ] Implement _normalize_lookup_value (line 20)
- [ ] Implement _first_present (line 24)
- [ ] Add validation logic (line 29)
- [ ] Implement skill logic (line 38)

**实现方案**:
```python
class ModelBuilderTool:
    """模型构建工具"""
    
    def run(self, config: Dict) -> SkillResult:
        """构建或修改模型"""
        if "base_model" in config:
            # 基于现有模型修改
            model = self._load_model(config["base_model"])
        else:
            # 创建新模型
            model = self._create_empty_model()
        
        # 添加组件
        for component in config.get("add_components", []):
            self._add_component(model, component)
        
        # 修改组件
        for modification in config.get("modify_components", []):
            self._modify_component(model, modification)
        
        # 删除组件
        for comp_id in config.get("remove_components", []):
            self._remove_component(model, comp_id)
        
        # 保存模型
        if config.get("save", True):
            rid = self._save_model(model, config.get("output"))
            return SkillResult(status=SkillStatus.SUCCESS, data={"rid": rid})
        
        return SkillResult(status=SkillStatus.SUCCESS, data={"model": model})
    
    def _coerce_scalar_value(self, value: Any, target_type: type) -> Any:
        """强制类型转换"""
        if target_type == float:
            return float(value)
        elif target_type == int:
            return int(value)
        elif target_type == bool:
            return bool(value) if isinstance(value, (int, bool)) else value.lower() == "true"
        return value
```

**验收标准**:
- [ ] 支持添加/修改/删除组件
- [ ] 类型强制转换
- [ ] 参数验证
- [ ] 单元测试覆盖率 > 80%

**工期**: 4 天

---

### 优先级 P3 (可视化与组件)

#### 9. Compare Visualization (`tools/compare_visualization.py`)
**设计目标**: 多场景对比可视化

**TODO 列表**:
- [ ] Add validation logic (line 19)
- [ ] Implement _compute_metrics (line 23)
- [ ] Implement _filter_time_range (line 27)
- [ ] Implement _normalize_for_radar (line 31)
- [ ] Implement _extract_channel_data (line 35)
- [ ] Implement skill logic (line 44)

**工期**: 4 天

---

#### 10. Component Catalog (`tools/component_catalog.py`)
**设计目标**: 组件目录发现与 RID 查询

**TODO**: Implement component_catalog logic (line 34)

**工期**: 3 天

---

## 📅 详细实施时间表

### Week 5-6: P0 核心数据导出

| 天 | 任务 | 技能 | 验收 |
|---|------|------|------|
| 1-2 | HDF5 Export 基础框架 | HDF5ExportTool | 可创建 HDF5 文件 |
| 3 | HDF5 Export 完善 | HDF5ExportTool | 支持读取/列出数据集 |
| 4-5 | HDF5 Export 测试 | HDF5ExportTool | 测试覆盖率 > 80% |
| 6-7 | COMTRADE Export 实现 | ComtradeExportTool | 生成标准格式 |
| 8 | COMTRADE 验证 | ComtradeExportTool | 可被查看器读取 |
| 9-10 | COMTRADE 测试 | ComtradeExportTool | 测试完成 |

**里程碑**: 
- [ ] 2 个数据导出技能可用
- [ ] 测试覆盖率 > 80%
- [ ] 集成测试通过

### Week 7-8: P1 工作流与批处理

| 天 | 任务 | 技能 | 验收 |
|---|------|------|------|
| 1-2 | Batch Task Manager 基础 | BatchTaskManager | 并行执行 |
| 3 | Batch Task 依赖管理 | BatchTaskManager | 支持依赖图 |
| 4-5 | Batch Task 测试 | BatchTaskManager | 测试完成 |
| 6-8 | Study Pipeline 实现 | StudyPipelineTool | 支持条件/循环 |
| 9 | Study Pipeline 变量 | StudyPipelineTool | 模板解析 |
| 10 | Study Pipeline 测试 | StudyPipelineTool | 测试完成 |

**里程碑**:
- [ ] 工作流编排可用
- [ ] 批处理功能可用

### Week 9-10: P2 模型与通道管理

| 天 | 任务 | 技能 | 验收 |
|---|------|------|------|
| 1-2 | Auto Channel Setup | AutoChannelSetupTool | 自动配置通道 |
| 3-4 | Auto Channel 测试 | AutoChannelSetupTool | 测试完成 |
| 5-6 | Model Hub 基础 | ModelHub | 多服务器管理 |
| 7 | Model Hub 搜索 | ModelHub | 跨服务器搜索 |
| 8-9 | Model Builder | ModelBuilderTool | 模型构建 |
| 10 | 测试与文档 | - | 测试覆盖 > 80% |

**里程碑**:
- [ ] 4 个技能可用
- [ ] 模型管理功能完善

### Week 11-12: P3 可视化与完善

| 天 | 任务 | 技能 | 验收 |
|---|------|------|------|
| 1-3 | Compare Visualization | CompareVisualizationTool | 对比可视化 |
| 4-5 | Component Catalog | ComponentCatalogTool | 组件目录 |
| 6-10 | 全面测试与修复 | 所有技能 | 测试 > 80% |
| 11-12 | 集成测试 | 所有技能 | 集成测试通过 |

**里程碑**:
- [ ] 11 个技能全部实现
- [ ] 测试覆盖率 > 75%
- [ ] 集成测试通过

---

## ✅ 关键检查点

### 技能实现检查清单

每个技能实现后必须完成：

```markdown
### Skill: [名称]
- [ ] 核心功能实现
- [ ] 输入验证
- [ ] 错误处理
- [ ] 单元测试 (> 80%)
- [ ] 集成测试
- [ ] API 文档
- [ ] 示例代码
- [ ] 代码审查通过
```

### 每周检查点

**Week 5 结束**:
```bash
# 验证 HDF5 和 COMTRADE
python -m cloudpss_skills run --config examples/hdf5_export.yaml
python -m cloudpss_skills run --config examples/comtrade_export.yaml
pytest tests/test_hdf5_export.py tests/test_comtrade_export.py -v --cov
# 预期: 覆盖率 > 80%
```

**Week 8 结束**:
```bash
# 验证工作流
pytest tests/test_batch_task_manager.py tests/test_study_pipeline.py -v
# 预期: 所有测试通过
```

**Week 12 结束**:
```bash
# 验证所有新技能
pytest cloudpss_skills_v2/tests/test_*.py -v --cov=cloudpss_skills_v2/tools
# 预期: 覆盖率 > 75%, 0 失败
```

---

## 📊 预期成果

### 修复前
- 虚假测试: 340+
- 未实现技能: 11
- 可用技能: 37/48 (77%)

### 修复后 (Week 12)
- 虚假测试: 0
- 未实现技能: 0
- 可用技能: 48/48 (100%)
- 测试覆盖率: > 75%
- 文档完整度: 100%

---

**计划状态**: 待审批  
**下一步**: 开始 Week 1 的虚假测试清理
