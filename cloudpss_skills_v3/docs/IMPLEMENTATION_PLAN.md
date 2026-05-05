# CloudPSS Skills V3 - Agent-First 实施计划

**文档版本**: 1.0  
**创建日期**: 2026-05-04  
**基于**: AGENT_FIRST_DESIGN.md, DESIGN.md  

---

## 实施概览

| 阶段 | 周期 | 目标 | 关键产出 |
|------|------|------|---------|
| **Phase 1** | 2周 | MCP Server 基础 | MCP Server 可运行，支持基础 Tool 调用 |
| **Phase 2** | 2周 | 异步与观测 | 异步任务系统，Portal 观测界面 |
| **Phase 3** | 2周 | 智能交互 | 参数推断，异常处理，结果分析 |
| **Phase 4** | 4周 | 高级功能 | 批量编排，报告生成，多 Agent 集成 |

**总计**: 10周

---

## Phase 1: MCP Server 基础 (2周)

### 目标
搭建 MCP Server 框架，实现基础 Tool 定义和调用。

### 任务清单

#### Task 1.1: MCP Server 框架搭建
**文件**: `cloudpss_skills_v3/mcp_server/__init__.py`, `server.py`  
**耗时**: 30分钟  
**依赖**: 无

**实现**:
```python
from mcp.server import Server
from mcp.types import Tool, TextContent
import asyncio

app = Server("cloudpss-skills")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """返回所有可用的 Skills"""
    pass

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """执行指定的 Skill"""
    pass

if __name__ == "__main__":
    asyncio.run(app.run())
```

**验收标准**:
- [ ] `python -m cloudpss_skills_v3.mcp_server` 可启动
- [ ] 不报错，能响应 MCP 协议请求

---

#### Task 1.2: 定义 Core Tools
**文件**: `cloudpss_skills_v3/mcp_server/tools.py`  
**耗时**: 45分钟  
**依赖**: Task 1.1

**实现**:
```python
TOOLS = [
    Tool(
        name="powerflow_run",
        description="运行潮流计算，返回母线电压和支路功率",
        inputSchema={
            "type": "object",
            "properties": {
                "case_name": {"type": "string", "description": "案例名称"},
                "model_rid": {"type": "string", "description": "CloudPSS 模型 RID"},
                "wait": {"type": "boolean", "description": "是否等待完成", "default": True}
            },
            "required": ["case_name", "model_rid"]
        }
    ),
    Tool(
        name="emt_run",
        description="运行暂态仿真（EMT）",
        inputSchema={...}
    ),
    Tool(
        name="result_query",
        description="查询仿真结果",
        inputSchema={...}
    ),
    # ... 其他工具
]
```

**验收标准**:
- [ ] 定义至少 6 个 Core Tools
- [ ] 每个 Tool 有完整的 inputSchema
- [ ] 描述使用电力专业语言

---

#### Task 1.3: 实现 powerflow_run Tool
**文件**: `cloudpss_skills_v3/mcp_server/handlers/powerflow.py`  
**耗时**: 60分钟  
**依赖**: Task 1.2

**实现**:
```python
async def handle_powerflow_run(arguments: dict) -> list[TextContent]:
    """执行潮流计算"""
    case_name = arguments["case_name"]
    model_rid = arguments["model_rid"]
    wait = arguments.get("wait", True)
    
    # 1. 创建案例
    case = await case_registry.create(name=case_name, model_rid=model_rid)
    
    # 2. 创建任务
    task = await task_runner.create(type="powerflow", case_id=case.id)
    
    # 3. 执行或返回任务ID
    if wait:
        result = await task_runner.wait_for_completion(task.id)
        return [TextContent(text=format_powerflow_result(result))]
    else:
        return [TextContent(text=f"任务已提交，ID: {task.id}")]

def format_powerflow_result(result) -> str:
    """格式化结果为自然语言"""
    return f"""✅ 潮流计算完成！

**结果摘要**：
- 母线数量：{result.bus_count}
- 支路数量：{result.branch_count}
- 电压范围：{result.voltage_min} ~ {result.voltage_max} pu
- 收敛迭代：{result.iterations} 次

**状态**: 计算成功，系统运行正常"""
```

**验收标准**:
- [ ] 支持同步执行（wait=True）
- [ ] 返回自然语言格式的结果
- [ ] 错误时返回友好的错误信息

---

#### Task 1.4: 实现 emt_run Tool
**文件**: `cloudpss_skills_v3/mcp_server/handlers/emt.py`  
**耗时**: 45分钟  
**依赖**: Task 1.3

**实现**: 类似 powerflow_run，支持 EMT 仿真参数

**验收标准**:
- [ ] 支持 duration、fault_config 等参数
- [ ] 正确格式化 EMT 结果

---

#### Task 1.5: 实现 result_query Tool
**文件**: `cloudpss_skills_v3/mcp_server/handlers/result.py`  
**耗时**: 30分钟  
**依赖**: Task 1.3

**实现**:
```python
async def handle_result_query(arguments: dict) -> list[TextContent]:
    task_id = arguments["task_id"]
    task = await task_registry.get(task_id)
    
    if task.status == "completed":
        return [TextContent(text=format_result_summary(task.result))]
    else:
        return [TextContent(text=f"任务状态: {task.status}, 进度: {task.progress}%")]
```

**验收标准**:
- [ ] 支持查询任务状态
- [ ] 支持查询已完成任务的结果

---

#### Task 1.6: MCP 配置文件
**文件**: `.mcp.json` (项目根目录)  
**耗时**: 15分钟  
**依赖**: Task 1.1

**实现**:
```json
{
  "mcpServers": {
    "cloudpss": {
      "command": "python",
      "args": ["-m", "cloudpss_skills_v3.mcp_server"],
      "env": {
        "CLOUDPSS_TOKEN_FILE": "~/.cloudpss/token",
        "CLOUDPSS_WORKSPACE": "~/.cloudpss/workspace"
      }
    }
  }
}
```

**验收标准**:
- [ ] Claude Desktop 能识别并加载
- [ ] 环境变量配置正确

---

#### Task 1.7: Phase 1 集成测试
**文件**: `cloudpss_skills_v3/mcp_server/tests/test_mcp_server.py`  
**耗时**: 45分钟  
**依赖**: Task 1.1-1.6

**测试用例**:
```python
async def test_list_tools():
    tools = await list_tools()
    assert len(tools) >= 6
    assert any(t.name == "powerflow_run" for t in tools)

async def test_powerflow_run_sync():
    result = await call_tool("powerflow_run", {
        "case_name": "test-ieee39",
        "model_rid": "model/chenying/IEEE39",
        "wait": True
    })
    assert "计算完成" in result[0].text
```

**验收标准**:
- [ ] 所有测试用例通过
- [ ] 覆盖 list_tools 和主要 tool 调用

---

### Phase 1 里程碑
- [ ] MCP Server 可独立运行
- [ ] 支持 6+ 个 Core Tools
- [ ] 与 Claude Desktop 集成测试通过

---

## Phase 2: 异步与观测 (2周)

### 目标
实现异步任务系统，重构 Portal 为观测界面。

### 任务清单

#### Task 2.1: 异步任务管理器
**文件**: `cloudpss_skills_v3/core/async_task_manager.py`  
**耗时**: 60分钟  
**依赖**: Phase 1 完成

**实现**:
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Callable
import asyncio

@dataclass
class AsyncTask:
    id: str
    type: str
    status: str  # pending, running, completed, failed
    progress: int  # 0-100
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[dict] = None
    error: Optional[str] = None
    
class AsyncTaskManager:
    def __init__(self):
        self.tasks: dict[str, AsyncTask] = {}
        self.callbacks: dict[str, list[Callable]] = {}
    
    async def create_task(self, task_type: str, params: dict) -> AsyncTask:
        """创建异步任务"""
        pass
    
    async def start_task(self, task_id: str):
        """启动任务执行"""
        pass
    
    async def update_progress(self, task_id: str, progress: int):
        """更新进度"""
        pass
    
    async def complete_task(self, task_id: str, result: dict):
        """标记任务完成"""
        pass
    
    async def fail_task(self, task_id: str, error: str):
        """标记任务失败"""
        pass
    
    def subscribe(self, task_id: str, callback: Callable):
        """订阅任务状态更新"""
        pass
```

**验收标准**:
- [ ] 支持任务创建、启动、完成、失败状态流转
- [ ] 支持进度更新
- [ ] 支持回调订阅

---

#### Task 2.2: 任务状态持久化
**文件**: `cloudpss_skills_v3/core/task_storage.py`  
**耗时**: 45分钟  
**依赖**: Task 2.1

**实现**:
```python
class TaskStorage:
    """任务状态持久化到磁盘"""
    
    def save_task(self, task: AsyncTask):
        """保存任务状态"""
        pass
    
    def load_task(self, task_id: str) -> Optional[AsyncTask]:
        """加载任务状态"""
        pass
    
    def list_tasks(self, status: Optional[str] = None) -> list[AsyncTask]:
        """列出任务"""
        pass
```

**验收标准**:
- [ ] 任务状态可持久化
- [ ] 服务重启后可恢复

---

#### Task 2.3: Portal 仪表盘页面
**文件**: `cloudpss_skills_v3/portal/templates/dashboard.html`  
**耗时**: 90分钟  
**依赖**: Task 2.1

**设计**:
```html
<!-- 基于 DESIGN.md 的 Agent Kanban 风格 -->
<body class="bg-[#09090B] text-[#FAFAFA] font-geist">
  <div class="max-w-[1200px] mx-auto p-6">
    <!-- Header -->
    <header class="flex justify-between items-center mb-8">
      <h1 class="text-2xl font-bold tracking-tight">CloudPSS Agent Hub</h1>
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-[#22D3EE] animate-pulse"></span>
        <span class="text-sm text-[#22D3EE] font-mono">Agent 运行中</span>
      </div>
    </header>
    
    <!-- Current Activity -->
    <section class="bg-[#18181B] rounded-lg p-4 mb-6">
      <h2 class="text-xs font-mono uppercase text-[#71717A] mb-3">当前活动</h2>
      <div id="current-task" class="space-y-2">
        <!-- 动态加载 -->
      </div>
    </section>
    
    <!-- Recent Tasks -->
    <section class="bg-[#18181B] rounded-lg p-4">
      <h2 class="text-xs font-mono uppercase text-[#71717A] mb-3">最近任务</h2>
      <div id="recent-tasks" class="space-y-2">
        <!-- 动态加载 -->
      </div>
    </section>
  </div>
</body>
```

**验收标准**:
- [ ] 页面加载正确，无样式错误
- [ ] 符合 DESIGN.md 的配色和字体规范
- [ ] 响应式布局正常

---

#### Task 2.4: Portal API - 任务状态
**文件**: `cloudpss_skills_v3/portal/handlers/api.py`  
**耗时**: 45分钟  
**依赖**: Task 2.1, 2.3

**实现**:
```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/api/tasks/current")
async def get_current_task():
    """获取当前正在运行的任务"""
    pass

@app.get("/api/tasks/recent")
async def get_recent_tasks(limit: int = 10):
    """获取最近完成的任务"""
    pass

@app.get("/api/tasks/{task_id}")
async def get_task_detail(task_id: str):
    """获取任务详情"""
    pass

@app.post("/api/tasks/{task_id}/pause")
async def pause_task(task_id: str):
    """暂停任务"""
    pass

@app.post("/api/tasks/{task_id}/cancel")
async def cancel_task(task_id: str):
    """取消任务"""
    pass
```

**验收标准**:
- [ ] API 返回正确的 JSON 格式
- [ ] 支持 CORS
- [ ] 错误处理完善

---

#### Task 2.5: 实时状态推送 (SSE)
**文件**: `cloudpss_skills_v3/portal/handlers/sse.py`  
**耗时**: 60分钟  
**依赖**: Task 2.4

**实现**:
```python
from fastapi import Request
from fastapi.responses import StreamingResponse
import asyncio
import json

@app.get("/api/stream")
async def event_stream(request: Request):
    """SSE 实时推送任务状态更新"""
    async def generate():
        while True:
            if await request.is_disconnected():
                break
            
            # 获取最新任务状态
            tasks = await get_tasks_update()
            yield f"data: {json.dumps(tasks)}\n\n"
            
            await asyncio.sleep(2)  # 每 2 秒推送一次
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

**验收标准**:
- [ ] SSE 连接稳定
- [ ] 状态更新实时推送到前端
- [ ] 支持多客户端同时连接

---

#### Task 2.6: 前端状态渲染
**文件**: `cloudpss_skills_v3/portal/static/js/dashboard.js`  
**耗时**: 60分钟  
**依赖**: Task 2.5

**实现**:
```javascript
// 连接 SSE
const evtSource = new EventSource('/api/stream');

evtSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateDashboard(data);
};

function updateDashboard(data) {
  // 更新当前任务
  const currentTaskEl = document.getElementById('current-task');
  if (data.current) {
    currentTaskEl.innerHTML = renderCurrentTask(data.current);
  }
  
  // 更新最近任务
  const recentTasksEl = document.getElementById('recent-tasks');
  recentTasksEl.innerHTML = data.recent.map(renderTaskCard).join('');
}

function renderCurrentTask(task) {
  return `
    <div class="flex items-center justify-between p-3 bg-[#27272A] rounded border-l-4 border-[#22D3EE]">
      <div>
        <div class="text-sm font-medium">${task.name}</div>
        <div class="text-xs text-[#A1A1AA] font-mono">${task.id}</div>
      </div>
      <div class="flex items-center gap-4">
        <div class="w-32 h-2 bg-[#27272A] rounded-full overflow-hidden">
          <div class="h-full bg-[#22D3EE] transition-all" style="width: ${task.progress}%"></div>
        </div>
        <span class="text-sm font-mono text-[#22D3EE]">${task.progress}%</span>
      </div>
    </div>
  `;
}
```

**验收标准**:
- [ ] 实时更新任务进度条
- [ ] Agent 活动时有发光效果 (glow effect)
- [ ] 进度变化平滑动画

---

#### Task 2.7: Phase 2 集成测试
**文件**: `cloudpss_skills_v3/portal/tests/test_dashboard.py`  
**耗时**: 60分钟  
**依赖**: Task 2.1-2.6

**测试用例**:
```python
async def test_async_task_lifecycle():
    """测试异步任务完整生命周期"""
    task = await task_manager.create_task("powerflow", {...})
    assert task.status == "pending"
    
    await task_manager.start_task(task.id)
    assert task.status == "running"
    
    await task_manager.complete_task(task.id, {...})
    assert task.status == "completed"

async def test_sse_stream():
    """测试 SSE 实时推送"""
    # 模拟任务更新，验证 SSE 推送
    pass
```

**验收标准**:
- [ ] 异步任务生命周期测试通过
- [ ] SSE 推送测试通过
- [ ] Portal 页面 E2E 测试通过

---

### Phase 2 里程碑
- [ ] 异步任务系统稳定运行
- [ ] Portal 观测界面可实时显示任务状态
- [ ] 支持任务暂停、取消等干预操作

---

## Phase 3: 智能交互 (2周)

### 目标
实现参数推断、异常处理、结果智能分析。

### 任务清单

#### Task 3.1: 参数自动推断
**文件**: `cloudpss_skills_v3/core/param_inference.py`  
**耗时**: 90分钟  
**依赖**: Phase 2 完成

**实现**:
```python
class ParamInference:
    """根据上下文推断参数"""
    
    async def infer_model_rid(self, case_name: str) -> Optional[str]:
        """根据案例名称推断模型 RID"""
        # 1. 检查本地缓存
        # 2. 搜索云端模型
        # 3. 返回最佳匹配
        pass
    
    async def suggest_parameters(self, task_type: str, goal: str) -> dict:
        """根据目标建议参数"""
        # 例如："快速验证" -> 简化参数
        #       "精确计算" -> 严格参数
        pass
```

**验收标准**:
- [ ] 能根据案例名推断模型 RID
- [ ] 能根据用户意图建议参数

---

#### Task 3.2: 异常分类与处理
**文件**: `cloudpss_skills_v3/core/exception_handler.py`  
**耗时**: 75分钟  
**依赖**: Task 3.1

**实现**:
```python
class ExceptionClassifier:
    """分类异常并给出处理建议"""
    
    ERROR_PATTERNS = {
        "model_not_found": {
            "pattern": r"模型.*不存在|rid.*not found",
            "suggestion": "检查模型 RID 或列出可用模型",
            "action": "list_available_models"
        },
        "convergence_failed": {
            "pattern": r"不收敛|diverge",
            "suggestion": "调整初始值或检查模型参数",
            "action": "suggest_fixes"
        },
        "timeout": {
            "pattern": r"超时|timeout",
            "suggestion": "增加超时时间或简化计算",
            "action": "adjust_timeout"
        }
    }
    
    def classify(self, error_message: str) -> dict:
        """分类错误并返回处理建议"""
        pass
```

**验收标准**:
- [ ] 能识别常见错误类型
- [ ] 给出友好的错误信息和处理建议

---

#### Task 3.3: 结果智能分析
**文件**: `cloudpss_skills_v3/core/result_analyzer.py`  
**耗时**: 90分钟  
**依赖**: Task 3.2

**实现**:
```python
class ResultAnalyzer:
    """智能分析仿真结果"""
    
    def analyze_powerflow(self, result: dict) -> str:
        """分析潮流计算结果"""
        issues = []
        suggestions = []
        
        # 检查电压
        if result['voltage_min'] < 0.95:
            issues.append(f"母线 {result['min_voltage_bus']} 电压偏低 ({result['voltage_min']:.3f} pu)")
            suggestions.append("建议增加该母线无功补偿")
        
        # 检查负载率
        if result['max_loading'] > 90:
            issues.append(f"支路 {result['max_loading_branch']} 负载率高 ({result['max_loading']:.1f}%)")
            suggestions.append("建议关注该支路 N-1 安全性")
        
        return self._format_analysis(issues, suggestions)
    
    def _format_analysis(self, issues: list, suggestions: list) -> str:
        """格式化为自然语言"""
        pass
```

**验收标准**:
- [ ] 能识别电压、负载率等关键问题
- [ ] 给出专业的分析建议
- [ ] 输出自然语言格式

---

#### Task 3.4: 中断协作流程
**文件**: `cloudpss_skills_v3/core/human_in_the_loop.py`  
**耗时**: 75分钟  
**依赖**: Task 3.2

**实现**:
```python
class HumanInTheLoop:
    """需要人决策时的中断处理"""
    
    async def request_decision(self, task_id: str, question: str, options: list) -> str:
        """请求用户决策"""
        # 1. 标记任务为 waiting_for_human
        # 2. 通过 Portal 通知用户
        # 3. 等待用户响应
        # 4. 返回用户选择
        pass
    
    async def notify_completion(self, task_id: str, result: dict):
        """任务完成时通知用户"""
        pass
```

**验收标准**:
- [ ] 能在 Portal 显示决策请求
- [ ] 支持用户通过对话或界面响应
- [ ] 超时处理机制

---

#### Task 3.5: 实现 analyze Tool
**文件**: `cloudpss_skills_v3/mcp_server/handlers/analyze.py`  
**耗时**: 45分钟  
**依赖**: Task 3.3

**实现**:
```python
async def handle_analyze(arguments: dict) -> list[TextContent]:
    task_id = arguments["task_id"]
    focus = arguments.get("focus", "general")
    
    result = await result_storage.get(task_id)
    analyzer = ResultAnalyzer()
    
    if focus == "voltage":
        analysis = analyzer.analyze_voltage(result)
    elif focus == "stability":
        analysis = analyzer.analyze_stability(result)
    else:
        analysis = analyzer.analyze_general(result)
    
    return [TextContent(text=analysis)]
```

**验收标准**:
- [ ] 支持不同维度的分析 (voltage/stability/losses)
- [ ] 返回自然语言分析结果

---

#### Task 3.6: Phase 3 集成测试
**文件**: `cloudpss_skills_v3/tests/test_smart_interaction.py`  
**耗时**: 60分钟  
**依赖**: Task 3.1-3.5

**验收标准**:
- [ ] 参数推断测试通过
- [ ] 异常分类测试通过
- [ ] 结果分析测试通过

---

### Phase 3 里程碑
- [ ] 支持参数自动推断
- [ ] 异常情况给出友好提示和处理建议
- [ ] 结果自动分析，输出专业解读

---

## Phase 4: 高级功能 (4周)

### 目标
实现批量编排、报告生成、多 Agent 集成。

### 任务清单

#### Task 4.1: 批量任务编排
**文件**: `cloudpss_skills_v3/core/batch_orchestrator.py`  
**耗时**: 120分钟  
**依赖**: Phase 3 完成

**实现**:
```python
class BatchOrchestrator:
    """批量任务编排器"""
    
    async def create_batch(self, name: str, tasks: list) -> str:
        """创建批量任务"""
        pass
    
    async def execute_parallel(self, batch_id: str, max_concurrent: int = 3):
        """并行执行批量任务"""
        pass
    
    async def execute_sequential(self, batch_id: str):
        """串行执行批量任务"""
        pass
    
    def get_progress(self, batch_id: str) -> dict:
        """获取批量任务进度"""
        pass
```

**验收标准**:
- [ ] 支持并行和串行执行模式
- [ ] 支持任务依赖关系
- [ ] 实时显示批量任务进度

---

#### Task 4.2: 参数扫描自动化
**文件**: `cloudpss_skills_v3/mcp_server/handlers/sweep.py`  
**耗时**: 90分钟  
**依赖**: Task 4.1

**实现**:
```python
async def handle_parameter_sweep(arguments: dict) -> list[TextContent]:
    """参数扫描"""
    base_case = arguments["base_case"]
    parameter = arguments["parameter"]
    range_values = arguments["range"]
    
    # 1. 创建批量任务
    tasks = []
    for value in range_values:
        task = await create_variant_task(base_case, parameter, value)
        tasks.append(task)
    
    batch_id = await batch_orchestrator.create_batch(
        name=f"Sweep {parameter}",
        tasks=tasks
    )
    
    # 2. 并行执行
    await batch_orchestrator.execute_parallel(batch_id)
    
    # 3. 汇总结果
    results = await batch_orchestrator.get_results(batch_id)
    summary = format_sweep_summary(results)
    
    return [TextContent(text=summary)]
```

**验收标准**:
- [ ] 支持单参数多值扫描
- [ ] 自动汇总对比结果
- [ ] 生成扫描报告

---

#### Task 4.3: 报告生成器
**文件**: `cloudpss_skills_v3/core/report_generator.py`  
**耗时**: 120分钟  
**依赖**: Task 4.2

**实现**:
```python
class ReportGenerator:
    """生成专业报告"""
    
    async def generate_markdown(self, task_ids: list, template: str) -> str:
        """生成 Markdown 报告"""
        pass
    
    async def generate_excel(self, task_ids: list) -> bytes:
        """生成 Excel 数据手册"""
        pass
    
    async def generate_presentation(self, task_ids: list) -> str:
        """生成演示文稿"""
        pass
```

**验收标准**:
- [ ] 支持 Markdown、Excel、PDF 格式
- [ ] 包含数据表格和图表
- [ ] 专业排版，适合论文/报告使用

---

#### Task 4.4: 实现 compare Tool
**文件**: `cloudpss_skills_v3/mcp_server/handlers/compare.py`  
**耗时**: 90分钟  
**依赖**: Task 4.3

**实现**:
```python
async def handle_compare(arguments: dict) -> list[TextContent]:
    """对比多个算例结果"""
    case_ids = arguments["case_ids"]
    metrics = arguments.get("metrics", ["voltage", "loading", "losses"])
    
    results = await result_storage.get_multiple(case_ids)
    comparison = compare_results(results, metrics)
    
    return [TextContent(text=format_comparison(comparison))]
```

**验收标准**:
- [ ] 支持多维度对比
- [ ] 生成对比表格和图表
- [ ] 输出差异分析

---

#### Task 4.5: 多 Agent 协作支持
**文件**: `cloudpss_skills_v3/core/agent_coordinator.py`  
**耗时**: 150分钟  
**依赖**: Task 4.4

**实现**:
```python
class AgentCoordinator:
    """协调多个 Agent 协作"""
    
    def register_agent(self, agent_id: str, capabilities: list):
        """注册 Agent 能力"""
        pass
    
    async def delegate_task(self, task: dict, agent_id: Optional[str] = None):
        """分配任务给 Agent"""
        pass
    
    async def coordinate_agents(self, workflow: list):
        """编排多 Agent 工作流"""
        pass
```

**验收标准**:
- [ ] 支持多个 Agent 同时工作
- [ ] Agent 能力发现和匹配
- [ ] 工作流编排

---

#### Task 4.6: 与 Claude Desktop 集成测试
**文件**: `cloudpss_skills_v3/tests/integration/test_claude_desktop.py`  
**耗时**: 90分钟  
**依赖**: Task 4.5

**测试用例**:
```python
async def test_end_to_end_powerflow():
    """端到端潮流计算测试"""
    # 模拟用户通过 Claude Desktop 调用
    pass

async def test_batch_sweep():
    """批量扫描测试"""
    pass

async def test_error_recovery():
    """错误恢复测试"""
    pass
```

**验收标准**:
- [ ] 与 Claude Desktop 集成测试通过
- [ ] 10 个故事场景都能正常运行

---

### Phase 4 里程碑
- [ ] 支持批量任务编排和参数扫描
- [ ] 自动生成专业报告
- [ ] 与主流 Agent 客户端集成测试通过

---

## 依赖关系图

```
Phase 1: MCP Server 基础
├── 1.1 MCP Server 框架
├── 1.2 Core Tools 定义
├── 1.3 powerflow_run
├── 1.4 emt_run
├── 1.5 result_query
├── 1.6 MCP 配置
└── 1.7 Phase 1 测试
    ↓
Phase 2: 异步与观测
├── 2.1 异步任务管理器
├── 2.2 任务持久化
├── 2.3 Portal 仪表盘
├── 2.4 Portal API
├── 2.5 SSE 推送
├── 2.6 前端渲染
└── 2.7 Phase 2 测试
    ↓
Phase 3: 智能交互
├── 3.1 参数推断
├── 3.2 异常处理
├── 3.3 结果分析
├── 3.4 中断协作
├── 3.5 analyze Tool
└── 3.6 Phase 3 测试
    ↓
Phase 4: 高级功能
├── 4.1 批量编排
├── 4.2 参数扫描
├── 4.3 报告生成
├── 4.4 compare Tool
├── 4.5 多 Agent 协调
└── 4.6 集成测试
```

---

## 风险管理

| 风险 | 可能性 | 影响 | 应对措施 |
|------|--------|------|---------|
| MCP 协议兼容性问题 | 中 | 高 | 早期与 Claude Desktop 集成测试 |
| 异步任务状态同步复杂 | 中 | 中 | 充分单元测试，使用成熟模式 |
| 性能瓶颈（大量任务） | 低 | 高 | 设计时考虑批量优化 |
| Portal 实时推送不稳定 | 中 | 中 | 实现重连机制，降级方案 |

---

## 成功标准

### 功能完成
- [ ] 支持 8+ 个 Core Tools
- [ ] 支持异步任务执行
- [ ] Portal 实时观测功能
- [ ] 参数自动推断
- [ ] 结果智能分析
- [ ] 批量任务编排
- [ ] 报告自动生成

### 用户体验
- [ ] 10 个故事场景全部可用
- [ ] Agent 调用成功率 > 95%
- [ ] Portal 页面加载 < 2s
- [ ] 任务状态更新延迟 < 3s

### 集成测试
- [ ] Claude Desktop 集成通过
- [ ] VS Code Copilot 集成通过
- [ ] 与其他 MCP Client 兼容

---

**实施计划已就绪。建议从 Phase 1 Task 1.1 开始执行。**
