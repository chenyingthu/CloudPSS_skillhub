# CloudPSS Skills 输出标准规范

**版本**: 1.0  
**状态**: 草稿  
**最后更新**: 2026-04-15

---

## 1. 概述

本文档定义了 CloudPSS Skills 的标准输出格式，确保所有技能的执行结果能够：
- **完备**: 包含所有计算产生的有效数据
- **一致**: 统一的字段命名和数据结构
- **准确**: 无 mock 数据、无假成功状态
- **可处理**: 便于后续数据处理和可视化

---

## 2. 核心数据结构

### 2.1 SkillResult 标准结构

```python
@dataclass
class SkillResult:
    skill_name: str          # 技能名称
    status: SkillStatus      # 执行状态
    start_time: datetime      # 开始时间
    end_time: datetime        # 结束时间
    
    # 核心输出数据
    data: Dict[str, Any]      # 主数据（见 3.1）
    
    # 附加输出
    artifacts: List[Artifact] # 文件输出
    logs: List[LogEntry]     # 日志
    metrics: Dict[str, Any]   # 性能指标
    
    # 错误信息
    error: Optional[str]      # 错误描述（失败时必填）
```

### 2.2 状态码规范

| 状态 | 何时使用 | data 内容 |
|------|----------|-----------|
| `SUCCESS` | 正常完成 | 完整的计算结果 |
| `FAILED` | 执行失败 | `{}` 或部分结果 + `error` |
| `CANCELLED` | 用户取消 | `{}` |
| `RUNNING` | 执行中 | 当前进度数据 |
| `PENDING` | 等待中 | `{}` |

**⚠️ 重要**: `SUCCESS` 状态必须对应真实计算结果，不得返回 mock/假数据。

---

## 3. data 字段标准

### 3.1 必需字段（所有技能）

```python
# 基础元数据（所有 SkillResult.data 必须包含）
data = {
    "skill_name": str,           # 技能标识
    "execution_id": str,         # 执行唯一ID（UUID）
    "timestamp": str,            # ISO8601 时间戳
    
    # 状态指示
    "success": bool,             # 是否成功（与 status 一致）
    "message": str,              # 简要描述
}
```

### 3.2 按技能类型的数据字段

#### 3.2.1 仿真类技能 (Simulation)

```python
data = {
    # 基础字段
    **base_fields,
    
    # 仿真特有
    "simulation_type": str,       # "power_flow" | "emt" | "dynamic"
    "model_info": {
        "rid": str,              # 模型 RID
        "name": str,             # 模型名称
        "bus_count": int,        # 母线数
        "branch_count": int,     # 支路数
        "generator_count": int,  # 发电机数
    },
    
    # 收敛信息
    "converged": bool,           # 是否收敛
    "iterations": int,           # 迭代次数
    "tolerance": float,          # 最终误差
    
    # 结果摘要
    "summary": {
        "total_generation": {"p_mw": float, "q_mvar": float},
        "total_load": {"p_mw": float, "q_mvar": float},
        "total_loss": {"p_mw": float, "q_mvar": float},
    },
    
    # 详细结果（按类型）
    "results": Dict[str, Any],    # 技能特定结果
}
```

#### 3.2.2 安全分析类技能 (Security Analysis)

```python
data = {
    **base_fields,
    
    # 分析配置
    "analysis_type": str,        # "n1" | "n2" | "contingency" | "maintenance"
    
    # 评估结果
    "total_cases": int,          # 总测试案例数
    "passed_cases": int,         # 通过案例数
    "failed_cases": int,         # 失败案例数
    "pass_rate": float,          # 通过率 (0.0-1.0)
    
    # 违规详情
    "violations": [
        {
            "case_id": str,      # 案例ID
            "case_name": str,    # 案例名称
            "violation_type": str,  # "voltage" | "overload" | "stability"
            "severity": str,     # "critical" | "major" | "minor"
            "details": Dict,     # 详细数据
        }
    ],
    
    # 安全指标
    "security_metrics": {
        "min_voltage_pu": float,
        "max_voltage_pu": float,
        "max_branch_loading_pct": float,
    },
}
```

#### 3.2.3 稳定性分析类技能 (Stability Analysis)

```python
data = {
    **base_fields,
    
    "analysis_type": str,        # "voltage" | "small_signal" | "transient" | "frequency"
    
    # 稳定性评估
    "stable": bool,              # 是否稳定
    "stability_margin": float,   # 稳定裕度
    "critical_value": float,      # 临界值
    
    # 模式信息
    "modes": [
        {
            "mode_id": int,
            "eigenvalue": complex,
            "damping_ratio": float,
            "frequency_hz": float,
        }
    ],
    
    # 结果详情
    "results": Dict[str, Any],
}
```

#### 3.2.4 参数分析类技能 (Parameter Analysis)

```python
data = {
    **base_fields,
    
    "analysis_type": str,        # "sensitivity" | "param_scan" | "optimization"
    
    # 分析范围
    "parameter_range": {
        "name": str,
        "min": float,
        "max": float,
        "step": float,
    },
    
    # 扫描结果
    "scan_results": [
        {
            "parameter_value": float,
            "objective_value": float,
            "metrics": Dict,
        }
    ],
    
    # 最优值
    "optimal": {
        "parameter_value": float,
        "objective_value": float,
        "metrics": Dict,
    },
}
```

#### 3.2.5 结果处理类技能 (Result Processing)

```python
data = {
    **base_fields,
    
    "processing_type": str,      # "export" | "compare" | "visualize"
    
    # 处理结果
    "processed_items": int,      # 处理项数
    "output_files": List[str],   # 输出文件列表
    
    # 导出特有
    "export_format": str,        # "csv" | "json" | "hdf5" | "comtrade"
    
    # 对比特有
    "comparison": {
        "difference_count": int,
        "max_difference": float,
        "metrics": Dict,
    },
}
```

#### 3.2.6 模型管理类技能 (Model Management)

```python
data = {
    **base_fields,
    
    "operation": str,            # 操作类型
    
    # 模型信息
    "model": {
        "rid": str,
        "name": str,
        "type": str,
        "version": str,
    },
    
    # 操作结果
    "changes": List[Dict],      # 变更列表
    "validation": {
        "valid": bool,
        "warnings": List[str],
    },
}
```

---

## 4. 字段命名规范

### 4.1 命名约定

| 类型 | 格式 | 示例 |
|------|------|------|
| Python 内部 | `snake_case` | `bus_count`, `total_loss` |
| JSON 输出 | `snake_case` | `bus_count`, `total_loss` |
| 外部 API | `camelCase` | `busCount`, `totalLoss` |

### 4.2 统一字段名映射

| 概念 | 标准名称 | 废弃名称 |
|------|----------|----------|
| 母线数 | `bus_count` | `busCount`, `BusNum` |
| 支路数 | `branch_count` | `branchCount`, `BranchNum` |
| 发电机数 | `generator_count` | `genCount`, `GenNum` |
| 总损耗 | `total_loss` | `totalLoss`, `LossTotal` |
| 有功功率 | `p_mw` | `p_mw`, `PMW`, `active_power` |
| 无功功率 | `q_mvar` | `q_mvar`, `Q_MVAR`, `reactive_power` |
| 电压标幺值 | `voltage_pu` | `voltage_pu`, `Vpu` |
| 负载率 | `loading_pct` | `loading_pct`, `loadPercent` |
| 通过率 | `pass_rate` | `pass_rate`, `PassRate` |
| 收敛 | `converged` | `converged`, `isConverged` |

---

## 5. 数据完整性要求

### 5.1 必须输出的数据

| 场景 | 必需字段 |
|------|----------|
| 仿真完成 | `converged`, `iterations`, `summary` |
| 安全分析 | `total_cases`, `passed_cases`, `failed_cases`, `violations` |
| 稳定性分析 | `stable`, `stability_margin` |
| 参数扫描 | `scan_results`, `optimal` |
| 导出操作 | `output_files`, `processed_items` |

### 5.2 禁止的行为

```python
# ❌ 禁止：返回硬编码假数据
def _calculate_loss_sensitivity(self):
    return {
        "sensitivities": [
            {"bus": f"Bus_{i}", "sensitivity": 0.01 * i} for i in range(1, 11)  # 假数据！
        ],
    }

# ❌ 禁止：异常后返回 SUCCESS
try:
    result = compute()
    return SkillResult(SUCCESS, data=result)
except Exception as e:
    return SkillResult(SUCCESS, data={})  # 错误！

# ❌ 禁止：空数据返回 SUCCESS
if not results:
    return SkillResult(SUCCESS, data={})  # 应该返回 FAILED 或 WARNING
```

### 5.3 正确做法

```python
# ✅ 正确：计算失败时返回 FAILED
try:
    result = compute()
    return SkillResult(SUCCESS, data={"result": result})
except ComputationError as e:
    return SkillResult(FAILED, data={}, error=str(e))

# ✅ 正确：无结果时返回 WARNING 或空结果
if not results:
    return SkillResult(
        SUCCESS, 
        data={
            "success": True,
            "message": "No violations found",
            "violations": [],  # 空列表是合法的
        }
    )

# ✅ 正确：实现未完成时抛出异常
def _calculate_loss_sensitivity(self, power_flow_result) -> Dict:
    raise NotImplementedError(
        "Loss sensitivity calculation requires perturbation analysis. "
        "This feature is not yet implemented."
    )
```

---

## 6. 验证与测试

### 6.1 输出验证规则

```python
class SkillOutputValidator:
    """输出验证器"""
    
    RULES = {
        # 基础验证
        "required_fields": ["skill_name", "success", "timestamp"],
        
        # 仿真类验证
        "simulation": ["converged", "model_info", "summary"],
        
        # 安全分析验证
        "security": ["total_cases", "pass_rate"],
        
        # 稳定性验证
        "stability": ["stable", "stability_margin"],
    }
    
    def validate(self, skill_name: str, data: Dict) -> ValidationResult:
        """验证输出数据"""
        result = ValidationResult(valid=True)
        
        # 检查必需字段
        for field in self.RULES["required_fields"]:
            if field not in data:
                result.add_error(f"Missing required field: {field}")
        
        # 按技能类型检查
        skill_category = self._get_category(skill_name)
        for field in self.RULES.get(skill_category, []):
            if field not in data:
                result.add_error(f"Missing {skill_category} field: {field}")
        
        return result
```

### 6.2 测试用例

```python
def test_loss_analysis_output():
    """测试网损分析输出"""
    skill = LossAnalysisSkill()
    result = skill.run({"model": {"rid": "test"}})
    
    assert result.status == SkillStatus.SUCCESS
    assert "summary" in result.data
    assert "losses" in result.data
    assert len(result.data.get("losses", [])) > 0  # 必须有真实数据
    
    # 禁止假数据
    if "sensitivities" in result.data:
        # 如果返回灵敏度，必须是真实计算结果
        for s in result.data["sensitivities"]:
            assert s["bus"] in real_buses, "Hardcoded fake bus names"
            assert s["sensitivity"] != 0.01, "Hardcoded fake sensitivity"
```

---

## 7. 迁移指南

### 7.1 现有 skills 改造清单

| Skill | 必需修改 | 优先级 |
|-------|----------|--------|
| `loss_analysis.py` | 移除 mock 数据，实现真实灵敏度计算 | P0 |
| `voltage_stability.py` | 补充 `stability_margin` 字段 | P1 |
| `n1_security.py` | 统一 `violations` 格式 | P1 |
| `power_flow.py` | 补充 `model_info` 完整信息 | P2 |
| 其他 | 按类别补充标准字段 | P2 |

### 7.2 改造示例

**Before (loss_analysis.py)**:
```python
def _calculate_loss_sensitivity(self, power_flow_result) -> Dict:
    return {
        "sensitivities": [
            {"bus": f"Bus_{i}", "sensitivity": 0.01 * i} for i in range(1, 11)
        ],
    }
```

**After**:
```python
def _calculate_loss_sensitivity(self, power_flow_result) -> Dict:
    """计算网损灵敏度
    
    Raises:
        NotImplementedError: 当前版本不支持灵敏度计算
    """
    raise NotImplementedError(
        "Loss sensitivity calculation requires perturbation analysis. "
        "This feature is not yet implemented."
    )
    
    # 未来实现示例:
    # sensitivities = []
    # buses = power_flow_result.getBuses()
    # for bus in buses:
    #     if bus.type != "slack":
    #         sensitivity = self._compute_sensitivity(power_flow_result, bus)
    #         sensitivities.append({
    #             "bus": bus.name,
    #             "bus_id": bus.id,
    #             "sensitivity": sensitivity,
    #         })
    # return {"sensitivities": sensitivities}
```

---

## 8. 附录

### 8.1 数据类型标准

| 类型 | 格式 | 示例 |
|------|------|------|
| 功率 | `{"p_mw": float, "q_mvar": float}` | `{"p_mw": 100.5, "q_mvar": 30.2}` |
| 电压 | `{"bus": str, "voltage_pu": float, "angle_deg": float}` | - |
| 电流/负载 | `{"branch": str, "loading_pct": float, "current_ka": float}` | - |
| 时间序列 | `{"time_s": List[float], "values": List[float]}` | - |

### 8.2 错误代码

| 代码 | 含义 | 处理建议 |
|------|------|----------|
| `E001` | 模型不存在 | 检查 RID |
| `E002` | 仿真不收敛 | 检查网络参数 |
| `E003` | 认证失败 | 刷新 token |
| `E004` | 特性未实现 | 记录为 TODO |
| `E005` | 数据不可用 | 返回空结果而非假数据 |

---

**文档版本历史**:
- v1.0 (2026-04-15): 初始版本
