# CloudPSS Toolkit 技能开发标准

**版本**: 1.0.0  
**发布日期**: 2026-04-16  
**状态**: 正式标准  

---

## 1. 概述

### 1.1 目的

本标准定义了 CloudPSS Toolkit 技能（Skill）的输入输出设计规范，确保所有技能在**规范性**、**标准化**、**完备性**和**准确性**四个维度上保持一致。

### 1.2 适用范围

- 所有内置技能（`cloudpss_skills/builtin/`）
- 第三方开发的插件技能
- 技能模板和示例代码

### 1.3 核心原则

| 原则 | 定义 | 优先级 |
|------|------|--------|
| **规范性** | Schema 定义与代码实现保持一致 | P0 |
| **标准化** | 同类参数使用统一命名和默认值模式 | P1 |
| **完备性** | 所有必需输入在验证阶段被检查，输出包含完整数据 | P0 |
| **准确性** | Schema 与运行时逻辑完全对齐，类型正确 | P0 |

---

## 2. 输入设计标准

### 2.1 Schema 声明规范

#### 2.1.1 顶层结构

所有技能必须定义 `config_schema` 属性，且顶层结构必须包含：

```python
@property
def config_schema(self) -> Dict[str, Any]:
    return {
        "type": "object",
        "required": ["skill", "model"],  # 技能标识和模型为必需
        "properties": {
            "skill": {"type": "string", "const": "<skill_name>"},
            "model": {
                "type": "object",
                "required": ["rid"],
                "properties": {
                    "rid": {"type": "string", "description": "模型RID"},
                    "source": {"enum": ["cloud", "local"], "default": "cloud"},
                },
            },
            # ... 其他字段
        },
    }
```

#### 2.1.2 Required 字段声明规则

| 字段类型 | 放入 required | 说明 |
|----------|--------------|------|
| 无默认值且业务必需 | ✅ 必须 | 缺少则无法运行 |
| 有默认值 | ❌ 不放入 | 可选，使用默认值 |
| 运行时动态计算 | ❌ 不放入 | 由代码逻辑推导 |
| 嵌套对象主键 | ✅ 必须 | 如 `model.rid` |

**反例**：
```python
# 错误：parameters 有默认值但放入 required
"required": ["skill", "model", "parameters", "target"]
"properties": {
    "parameters": {"type": "array", "default": []}  # 有默认值
}
```

**正例**：
```python
# 正确：parameters 不在 required 中
"required": ["skill", "model", "target"]
```

#### 2.1.3 例外：后处理技能

以下技能是**后处理/结果导出类技能**，它们不需要 `model` 字段，因为操作对象是已有的仿真结果（通过 `job_id` 或文件路径）：

```python
# 后处理技能
"required": ["skill", "source"]  # 或 ["skill"]（查询类技能）
```

**后处理技能包括**：
| 类别 | 技能 |
|------|------|
| 结果导出类 | `waveform_export`, `hdf5_export`, `comtrade_export` |
| 可视化类 | `visualize`, `compare_visualization` |
| 报告类 | `report_generator` |
| 查询类 | `component_catalog` |
| 批量处理类 | `batch_powerflow`, `batch_task_manager` |
| 结果分析类 | `result_compare`, `disturbance_severity` |

**注意**：这些技能仍必须包含 `"skill"` 在 required 中。

#### 2.1.4 例外：多模型/多母线操作类技能

以下技能使用**替代主输入字段**（数组类型），而不是单一的 `model` 字段：

| 技能 | 主输入字段 | 说明 |
|------|-----------|------|
| `dudv_curve` | `buses` (array) | DUDV 曲线可视化，需要指定多个待分析的母线 |
| `model_validator` | `models` (array) | 模型验证技能，可批量验证多个测试算例 |

```python
# dudv_curve: 多母线分析
"required": ["skill", "buses"]
"properties": {
    "buses": {
        "type": "array",
        "items": {"type": "string"},
        "description": "要分析的母线列表"
    }
}

# model_validator: 多模型验证
"required": ["skill", "models"]
"properties": {
    "models": {
        "type": "array",
        "items": {"type": "object", "required": ["rid"]}
    }
}
```

**设计理由**：
- 这些技能的操作对象是**多个目标**（多母线或多模型），而非单一模型
- 使用数组字段作为主输入更符合业务场景
- 与后处理技能类似，属于合理的例外情况

#### 2.1.5 例外：流程编排类技能

以下技能使用**流程定义**作为主输入字段，而不是单一的 `model` 字段：

| 技能 | 主输入字段 | 说明 |
|------|-----------|------|
| `study_pipeline` | `pipeline` (array) | 多技能流程编排，定义执行步骤列表 |

```python
# study_pipeline: 流程编排
"required": ["skill", "pipeline"]
"properties": {
    "pipeline": {
        "type": "array",
        "items": {
            "type": "object",
            "required": ["skill"],
            "properties": {
                "name": {"type": "string"},
                "skill": {"type": "string"},
                "config": {"type": "object"}
            }
        }
    }
}
```

**设计理由**：
- 流程编排技能的核心是**执行步骤序列**，而非单一模型
- 每个步骤可以有自己的模型配置
- 属于合理的例外情况

### 2.2 数据类型规范

#### 2.2.1 数值类型

```yaml
# 正确：使用 number 类型
"fs": {"type": "number", "default": 2.5}
"tolerance": {"type": "number", "default": 1e-6}

# 错误：禁止不必要的字符串转换
"fs": {"type": "string"}  # ❌ EMT 参数必须为 number
```

**关键规则**：
- EMT 仿真参数（`fs`、`fe`、`chg`）必须保持 `number` 类型
- 禁止使用 `str()` 转换数值参数
- 数值字段禁止不必要的类型转换

#### 2.2.2 数组类型

```yaml
"fe_values":
  type: array
  items: {"type": "number"}
  minItems: 1              # 必须有最小长度约束
  maxItems: 100            # 根据业务需求设置上限
  default: [2.7, 2.8, 2.9]
  description: "故障切除时间扫描值（至少1个值）"

"time_range":
  type: array
  items: {"type": "number"}
  minItems: 2
  maxItems: 2              # 固定2元素数组
  description: "时间窗口[开始, 结束]"
```

**数组字段规则**：
| 场景 | 必须约束 |
|------|----------|
| 扫描参数 | `minItems: 1` |
| 时间窗口 | `minItems: 2, maxItems: 2` |
| 坐标/范围 | `minItems: 2, maxItems: 2` |
| 通道列表 | `minItems: 1`（如有最低要求） |

#### 2.2.3 枚举类型

```yaml
"format":
  type: string
  enum: ["json", "csv"]    # 只包含代码已实现的选项
  default: json

# 错误：schema 定义但代码未实现
enum: ["json", "yaml", "csv"]  # ❌ yaml 未实现
```

**规则**：枚举值必须与代码实现完全一致。

### 2.3 默认值规范

#### 2.3.1 get_default_config 方法

所有技能必须实现 `get_default_config()` 方法，返回与 `config_schema` 一致的默认值：

```python
def get_default_config(self) -> Dict[str, Any]:
    return {
        "skill": self.name,
        "auth": {"token_file": ".cloudpss_token"},
        "model": {"rid": "", "source": "cloud"},
        "analysis": {
            "enabled": True,
            "threshold": 0.05,
            "window": [0.1, 1.0],  # 与 schema default 一致
        },
        "output": {
            "format": "json",
            "path": "./results/",
        },
    }
```

#### 2.3.2 三层默认值同步

```
Schema default  ←→  get_default_config()  ←→  config.get(key, default)
       ↓                    ↓                       ↓
  JSON Schema          Python Dict            代码实现
     必须一致            必须一致                必须一致
```

**检查清单**：
- [ ] Schema 中每个有 `default` 的字段
- [ ] `get_default_config()` 中有对应的值
- [ ] `run()` 中使用 `config.get(key, schema_default)`

### 2.4 验证逻辑规范

#### 2.4.1 validate 方法

```python
def validate(self, config: Dict[str, Any]) -> ValidationResult:
    """验证配置 - 必须覆盖所有 required 字段"""
    result = ValidationResult(valid=True)
    
    # 必须字段检查
    if "model" not in config:
        result.add_error("必须指定 model 配置")
    elif "rid" not in config.get("model", {}):
        result.add_error("必须指定 model.rid")
    
    # 数组非空检查
    scan_values = config.get("scan", {}).get("values", [])
    if len(scan_values) < 1:
        result.add_error("scan.values 至少需要1个元素")
    
    # 逻辑顺序检查
    time_range = config.get("compare", {}).get("time_range", {})
    if time_range:
        start = time_range.get("start")
        end = time_range.get("end")
        if start is not None and end is not None and start >= end:
            result.add_error("time_range.start 必须小于 time_range.end")
    
    return result
```

#### 2.4.2 验证覆盖清单

| 验证类型 | 检查项 |
|----------|--------|
| 必需字段 | `model.rid` 存在 |
| 数组长度 | `minItems` 约束 |
| 范围顺序 | `start < end` |
| 类型正确 | 数值不为字符串 |
| 枚举有效 | 值在允许列表中 |

---

## 3. 输出设计标准

### 3.1 SkillResult 结构规范

```python
def run(self, config: Dict[str, Any]) -> SkillResult:
    start_time = datetime.now()
    logs = []
    artifacts = []
    
    try:
        # ... 业务逻辑 ...
        
        result_data = {
            # 元信息
            "model_rid": model_rid,
            "model_name": getattr(model, "name", model_rid),
            
            # 核心结果数据（完整输出，不仅是 counts）
            "buses": bus_rows,           # 潮流结果母线数据
            "branches": branch_rows,     # 潮流结果支路数据
            "summary": self._generate_summary(),
            
            # 详细分析结果
            "metrics": {...},
            "waveforms": [...],          # 波形数据（可选）
        }
        
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.SUCCESS,
            start_time=start_time,
            end_time=datetime.now(),
            data=result_data,
            artifacts=artifacts,
            logs=logs,
        )
        
    except Exception as e:
        logger.error(f"技能执行失败: {e}", exc_info=True)
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.FAILED,
            start_time=start_time,
            end_time=datetime.now(),
            error=str(e),
            logs=logs,
        )
```

### 3.2 输出完备性规则

#### 3.2.1 核心数据输出

| 技能类型 | 必须输出的数据 |
|----------|----------------|
| 潮流计算 | `buses`（母线数据）、`branches`（支路数据） |
| EMT 仿真 | `waveforms`（原始波形数据，可配置输出） |
| 故障分析 | `fault_results`（故障事件详情） |
| 稳定性分析 | `stability_metrics`（稳定性指标） |
| 扫描分析 | `scan_results`（每个扫描点的结果） |

#### 3.2.2 配置化输出控制

```python
output_config = config.get("output", {})

# 原始数据输出（大数据量）
if output_config.get("include_raw_data", False):
    result_data["raw_data"] = waveform_data

# 汇总数据输出（默认）
result_data["summary"] = {
    "count": len(raw_data),
    "metrics": calculate_metrics(raw_data),
}
```

### 3.3 失败路径规范

```python
except (KeyError, AttributeError, ConnectionError, RuntimeError) as e:
    logger.error(f"技能执行失败: {e}", exc_info=True)
    return SkillResult(
        skill_name=self.name,
        status=SkillStatus.FAILED,
        start_time=start_time,
        end_time=datetime.now(),
        error=str(e),
        logs=logs,
        data={
            "success": False,
            "error": str(e),
            "stage": "model_loading",  # 标记失败阶段
        },
    )
```

**失败数据必须包含**：
| 字段 | 说明 |
|------|------|
| `success` | `false` |
| `error` | 错误消息 |
| `stage` | 失败阶段（`validation`、`model_loading`、`simulation`、`post_processing`） |

---

## 4. 代码模板

### 4.1 技能基础模板

```python
from cloudpss_skills.core import (
    SkillBase, SkillResult, SkillStatus, ValidationResult, register,
)

class MySkill(SkillBase):
    """技能描述"""
    
    @property
    def name(self) -> str:
        return "my_skill"
    
    @property
    def description(self) -> str:
        return "技能功能描述"
    
    @property
    def config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["skill", "model"],
            "properties": {
                "skill": {"type": "string", "const": "my_skill"},
                "model": {
                    "type": "object",
                    "required": ["rid"],
                    "properties": {
                        "rid": {"type": "string"},
                        "source": {"enum": ["cloud", "local"], "default": "cloud"},
                    },
                },
                "analysis": {
                    "type": "object",
                    "properties": {
                        "enabled": {"type": "boolean", "default": True},
                        "threshold": {"type": "number", "default": 0.05},
                        "values": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 1,
                            "default": [1.0, 2.0, 3.0],
                        },
                    },
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {"enum": ["json", "csv"], "default": "json"},
                        "path": {"type": "string", "default": "./results/"},
                        "include_raw_data": {"type": "boolean", "default": False},
                    },
                },
            },
        }
    
    def get_default_config(self) -> Dict[str, Any]:
        return {
            "skill": self.name,
            "auth": {"token_file": ".cloudpss_token"},
            "model": {"rid": "", "source": "cloud"},
            "analysis": {
                "enabled": True,
                "threshold": 0.05,
                "values": [1.0, 2.0, 3.0],
            },
            "output": {
                "format": "json",
                "path": "./results/",
                "include_raw_data": False,
            },
        }
    
    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        result = ValidationResult(valid=True)
        
        # 必须字段检查
        if not config.get("model", {}).get("rid"):
            result.add_error("必须指定 model.rid")
        
        # 数组检查
        values = config.get("analysis", {}).get("values", [])
        if len(values) < 1:
            result.add_error("analysis.values 至少需要1个元素")
        
        return result
    
    def run(self, config: Dict[str, Any]) -> SkillResult:
        from datetime import datetime
        from cloudpss_skills.core.auth_utils import setup_auth
        
        start_time = datetime.now()
        logs = []
        
        try:
            setup_auth(config)
            
            # 1. 加载模型
            model = self._load_model(config)
            
            # 2. 执行分析
            results = self._analyze(config, model)
            
            # 3. 整理输出
            result_data = {
                "model_rid": config["model"]["rid"],
                "summary": results["summary"],
                "details": results["details"],
            }
            
            # 4. 可选原始数据
            if config.get("output", {}).get("include_raw_data"):
                result_data["raw_data"] = results["raw"]
            
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.SUCCESS,
                start_time=start_time,
                end_time=datetime.now(),
                data=result_data,
                logs=logs,
            )
            
        except Exception as e:
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                error=str(e),
                data={"success": False, "error": str(e), "stage": "analysis"},
                logs=logs,
            )
```

---

## 5. 审查清单

### 5.1 开发自检

开发完成后，使用以下清单进行自检：

#### Schema 检查
- [ ] 顶层包含 `required: ["skill", "model"]`
- [ ] 所有数值字段类型为 `number`（非 string）
- [ ] 所有数组字段有 `minItems` 约束
- [ ] 枚举值与代码实现一致
- [ ] `get_default_config()` 已实现且与 schema 一致

#### 验证检查
- [ ] `validate()` 检查所有 required 字段
- [ ] `validate()` 检查数组最小长度
- [ ] `validate()` 检查逻辑顺序（如 start < end）

#### 输出检查
- [ ] 核心数据完整输出（不仅是 counts）
- [ ] 失败路径包含 `success: False`、`error`、`stage`
- [ ] 可选原始数据有配置开关

### 5.2 PR 审查要点

审查者应关注：

1. **Schema-Runtime 一致性**
   - schema 定义的字段在代码中是否使用？
   - 代码使用的字段是否在 schema 中定义？

2. **类型正确性**
   - 数值参数是否为 `number` 类型？
   - 是否有不必要的 `str()` 转换？

3. **默认值同步**
   - schema default == get_default_config() == 代码中的默认值

4. **输出完备性**
   - 核心计算结果是否完整输出？
   - 失败路径是否规范？

---

## 6. 常见问题

### Q1: 为什么 required 中不能放有默认值的字段？

因为 JSON Schema 的 `required` 表示"必须有"，而 `default` 表示"可以有默认值"。两者语义冲突。

```python
# 语义错误
"required": ["threshold"]
"properties": {
    "threshold": {"type": "number", "default": 0.05}  # 有默认值但必需？
}
```

### Q2: 数组字段如何选择 minItems？

| 场景 | minItems | 说明 |
|------|----------|------|
| 扫描参数 | 1 | 至少1个值 |
| 时间窗口 | 2 | [start, end] |
| 坐标 | 2 | [x, y] |
| 范围 | 2 | [min, max] |
| 三相通道 | 3 | [a, b, c] |

### Q3: 输出数据量太大怎么办？

使用配置化输出：

```python
if output_config.get("include_raw_data", False):
    result_data["raw_data"] = large_waveform_data
else:
    result_data["summary"] = calculate_summary(large_waveform_data)
```

### Q4: EMT 参数为什么不能转字符串？

CloudPSS API 内部期望数值类型：

```python
# 错误 ❌
{"fs": "2.5"}  # 字符串，EMT 计算错误

# 正确 ✅
{"fs": 2.5}    # 数值，正确传递
```

---

## 7. 更新历史

| 版本 | 日期 | 修改内容 |
|------|------|----------|
| 1.0.0 | 2026-04-16 | 初始版本，基于 48 个技能审查结果制定 |

---

**附录 A: Schema 类型速查表**

| 类型 | JSON Schema | Python | 说明 |
|------|-------------|--------|------|
| 字符串 | `{"type": "string"}` | `str` | 文本 |
| 整数 | `{"type": "integer"}` | `int` | 整数值 |
| 数值 | `{"type": "number"}` | `float` | 浮点数 |
| 布尔 | `{"type": "boolean"}` | `bool` | true/false |
| 数组 | `{"type": "array", "items": {...}}` | `list` | 列表 |
| 对象 | `{"type": "object", "properties": {...}}` | `dict` | 字典 |

**附录 B: 约束关键字速查**

| 关键字 | 适用类型 | 说明 |
|--------|----------|------|
| `required` | object | 必需字段列表 |
| `minItems` | array | 最小元素数 |
| `maxItems` | array | 最大元素数 |
| `minimum` | number | 最小值 |
| `maximum` | number | 最大值 |
| `enum` | any | 允许值列表 |
| `const` | any | 固定值 |
| `default` | any | 默认值 |
