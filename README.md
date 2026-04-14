# CloudPSS SkillHub

> **CloudPSS 电力系统仿真技能中心** - 配置驱动的技能系统，提供 48 个专业仿真技能

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 简介

**CloudPSS SkillHub** 是对 [CloudPSS](https://www.cloudpss.net/) 电力系统仿真平台的高级封装，提供配置驱动的技能系统、丰富的示例代码和完整的文档支持。

## 特性

- **48 个专业仿真技能** - 覆盖潮流计算、暂态仿真、安全分析、稳定性评估等
- **配置驱动** - YAML 配置文件即可执行复杂仿真任务
- **简洁的 API** - 隐藏底层复杂性，提供直观的编程接口
- **丰富的示例** - 从基础到高级应用的完整示例代码
- **批量处理** - 支持大规模批量仿真和分析
- **结果可视化** - 内置可视化工具和数据导出功能（COMTRADE、HDF5 等）

## 技能清单（48 个）

### 模型管理类（4 个）
| 技能 | 描述 |
|------|------|
| `component_catalog` | 组件目录发现、RID 查询 |
| `model_builder` | 模型构建、组件添加/修改/删除 |
| `model_validator` | 模型验证（拓扑/潮流/暂态） |
| `model_hub` | 算例中心 - 多服务器统一管理 |

### 仿真执行类（4 个）
| 技能 | 描述 |
|------|------|
| `power_flow` | 牛顿 - 拉夫逊潮流计算 |
| `emt_simulation` | EMT 暂态仿真 |
| `emt_fault_study` | EMT 故障研究 |
| `short_circuit` | 短路电流计算 |

### 安全分析类（5 个）
| 技能 | 描述 |
|------|------|
| `n1_security` | N-1 安全校核 |
| `n2_security` | N-2 安全校核 |
| `emt_n1_screening` | EMT N-1 安全筛查 |
| `contingency_analysis` | 预想事故分析 |
| `maintenance_security` | 检修方式安全校核 |

### 保护配合类（1 个）
| 技能 | 描述 |
|------|------|
| `protection_coordination` | 继电保护定值计算与配合 |

### 批量扫描类（7 个）
| 技能 | 描述 |
|------|------|
| `batch_powerflow` | 批量潮流计算 |
| `param_scan` | 参数扫描分析 |
| `fault_clearing_scan` | 故障清除时间扫描 |
| `fault_severity_scan` | 故障严重度扫描 |
| `batch_task_manager` | 批处理任务管理 |
| `config_batch_runner` | 多配置批量运行 |
| `study_pipeline` | 研究流水线编排 |

### 稳定性分析类（8 个）
| 技能 | 描述 |
|------|------|
| `voltage_stability` | 电压稳定分析（PV 曲线） |
| `transient_stability` | 暂态稳定分析 |
| `transient_stability_margin` | 暂态稳定裕度评估（CCT） |
| `small_signal_stability` | 小信号稳定分析 |
| `frequency_response` | 频率响应分析 |
| `vsi_weak_bus` | VSI 弱母线分析 |
| `dudv_curve` | DUDV 曲线生成 |
| `orthogonal_sensitivity` | 正交敏感性分析 |

### 结果处理类（9 个）
| 技能 | 描述 |
|------|------|
| `result_compare` | 结果对比分析 |
| `visualize` | 结果可视化 |
| `waveform_export` | 波形数据导出 |
| `hdf5_export` | HDF5 标准格式导出 |
| `comtrade_export` | COMTRADE 标准格式导出 |
| `compare_visualization` | 多场景对比可视化 |
| `disturbance_severity` | 扰动严重度分析 |
| `loss_analysis` | 网损分析 |
| `report_generator` | 智能报告生成 |

### 新能源接入类（2 个）
| 技能 | 描述 |
|------|------|
| `renewable_integration` | 新能源接入评估（SCR/谐波/LVRT） |
| `thevenin_equivalent` | PCC 戴维南等值计算 |

### 电能质量类（3 个）
| 技能 | 描述 |
|------|------|
| `harmonic_analysis` | 谐波分析（FFT/THD） |
| `power_quality_analysis` | 电能质量综合分析 |
| `reactive_compensation_design` | 无功补偿设计 |

### 模型拓扑类（5 个）
| 技能 | 描述 |
|------|------|
| `topology_check` | 拓扑完整性检查 |
| `parameter_sensitivity` | 参数灵敏度分析 |
| `auto_channel_setup` | 自动量测配置 |
| `auto_loop_breaker` | 自动解环 |
| `model_parameter_extractor` | 模型参数提取 |

## 安装

### 前置要求

- Python 3.8+
- CloudPSS 账户和 API token（从 https://www.cloudpss.net/ 获取）

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/chenyingthu/CloudPSS_skillhub.git
cd CloudPSS_skillhub

# 安装依赖
pip install -e ".[dev]"
```

### 配置 Token

⚠️ **重要**：请勿将 token 文件提交到 git 仓库！

```bash
# 方法 1：创建 token 文件（已添加到.gitignore）
echo "your_cloudpss_token_here" > .cloudpss_token

# 方法 2：设置环境变量
export CLOUDPSS_TOKEN="your_cloudpss_token_here"
```

## 使用方法

### 方法 1：命令行工具

```bash
# 列出所有可用技能
python -m cloudpss_skills list

# 初始化技能配置
python -m cloudpss_skills init power_flow --output pf_config.yaml

# 编辑配置文件后运行
python -m cloudpss_skills run --config pf_config.yaml
```

### 方法 2：Python API

```python
from cloudpss_skills.core.registry import get_skill

# 获取技能
power_flow = get_skill("power_flow")

# 运行技能
result = power_flow.run({
    "skill": "power_flow",
    "model": {"rid": "model/holdme/IEEE39"},
    "algorithm": {"type": "newton_raphson"},
})

print(f"状态：{result.status}")
print(f"结果：{result.data}")
```

### 方法 3：示例脚本

```bash
# 运行潮流计算示例
python examples/simulation/run_powerflow.py

# 运行 EMT 仿真示例
python examples/simulation/run_emt_simulation.py

# 运行 N-1 安全校核示例
python examples/analysis/powerflow_n1_screening_example.py
```

## 配置示例

### 潮流计算配置

```yaml
skill: power_flow
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
  source: cloud
algorithm:
  type: newton_raphson
  tolerance: 1e-6
  max_iterations: 100
output:
  format: json
  path: ./results/
  prefix: power_flow
```

### EMT 仿真配置

```yaml
skill: emt_simulation
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE3
  source: cloud
simulation:
  duration: 5.0
  step_size: 0.0001
  fault:
    type: three_phase
    location: bus1
    start_time: 0.5
    clear_time: 0.6
output:
  format: comtrade
  path: ./results/
```

## 典型工作流

### 工作流 1: 模型创建与验证

```
component_catalog → model_builder → model_validator
```

### 工作流 2: N-1 安全校核

```
n1_security → contingency_analysis → result_compare
```

### 工作流 3: 故障分析

```
emt_fault_study → disturbance_severity → visualize
```

### 工作流 4: 批量仿真

```
batch_task_manager → hdf5_export → result_compare
```

## 项目结构

```
CloudPSS_skillhub/
├── cloudpss_skills/       # 核心技能包
│   ├── core/             # 核心模块（认证、执行器、导出器）
│   └── builtin/          # 内置技能（48 个）
├── examples/             # 示例代码（25+）
├── docs/                 # 文档
│   ├── skills/          # 技能详细说明
│   ├── guides/          # 工作流指南
│   └── api-reference/   # API 参考文档
├── configs/              # 配置示例（30+）
└── tests/                # 测试用例
```

## 测试

```bash
# 运行单元测试（默认，无需网络）
pytest

# 运行集成测试（需要有效的 CloudPSS token）
pytest --run-integration -m "integration and not slow_emt"

# 运行特定测试文件
pytest tests/test_powerflow_result.py

# 生成覆盖率报告
pytest --cov=cloudpss_skills --cov-report=html
```

## 文档

- [技能系统文档](docs/skills/README.md) - 完整的技能说明和索引
- [用户手册](docs/skills/user_manual.md) - 用户操作指南
- [配置参考](docs/skills/config_reference.md) - 配置参数详解
- [API 文档](docs/api-reference/) - SDK API 参考文档
- [工作流指南](docs/guides/) - 典型研究工作流

## 安全提示

⚠️ **保护你的 API Token**

- `.cloudpss_token` 文件已添加到 `.gitignore`，不会被提交
- 但请确保：
  - 不在代码中硬编码 token
  - 使用环境变量或本地配置文件管理 token
  - 定期更新 token
  - 不与他人分享 token

## 许可证

MIT License

## 联系与支持

- **GitHub Issues**: 报告问题或提出功能请求
- **CloudPSS 官方**: https://www.cloudpss.net/

## 致谢

- [CloudPSS](https://www.cloudpss.net/) - 电力系统仿真平台
- 所有贡献者和用户

---

**维护者**: Chen Ying (@chenyingthu)
