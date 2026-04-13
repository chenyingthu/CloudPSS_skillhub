# CloudPSS Toolkit

CloudPSS API 增强工具包 - 为电力系统仿真研究提供高级 Python 封装

## 简介

`cloudpss-toolkit` 是对 [CloudPSS](https://www.cloudpss.net/) Python SDK 的高级封装，提供配置驱动的技能系统、丰富的示例代码和完整的文档支持。

## 特性

- **配置驱动的技能系统** - 30个即用型技能，通过YAML配置即可执行
- **简洁的 API 设计** - 隐藏底层复杂性，提供直观的接口
- **丰富的示例代码** - 从基础到高级应用的完整示例
- **批量处理支持** - 支持大规模批量仿真和分析
- **完整的测试覆盖** - 单元测试和集成测试（真实API验证）
- **结果可视化** - 内置可视化工具和数据导出功能

## 技能清单 (30个)

### 仿真执行类
| 技能 | 描述 |
|------|------|
| `power_flow` | 牛顿-拉夫逊潮流计算 |
| `emt_simulation` | EMT暂态仿真 |
| `emt_fault_study` | EMT故障研究 |
| `short_circuit` | 短路电流计算 |

### N-1安全分析类
| 技能 | 描述 |
|------|------|
| `n1_security` | N-1安全校核 |
| `emt_n1_screening` | EMT N-1安全筛查 |
| `contingency_analysis` | 预想事故分析 |
| `maintenance_security` | 检修方式安全校核 |

### 批量与扫描类
| 技能 | 描述 |
|------|------|
| `batch_powerflow` | 批量潮流计算 |
| `param_scan` | 参数扫描分析 |
| `fault_clearing_scan` | 故障清除时间扫描 |
| `fault_severity_scan` | 故障严重度扫描 |
| `batch_task_manager` | 批处理任务管理 |

### 稳定性分析类
| 技能 | 描述 |
|------|------|
| `voltage_stability` | 电压稳定分析 |
| `transient_stability` | 暂态稳定分析 |
| `small_signal_stability` | 小信号稳定分析 |
| `frequency_response` | 频率响应分析 |
| `vsi_weak_bus` | VSI弱母线分析 |
| `dudv_curve` | DUDV曲线生成 |

### 结果处理类
| 技能 | 描述 |
|------|------|
| `result_compare` | 结果对比分析 |
| `visualize` | 结果可视化 |
| `waveform_export` | 波形数据导出 |
| `hdf5_export` | HDF5数据导出 |
| `disturbance_severity` | 扰动严重度分析 |

### 电能质量类
| 技能 | 描述 |
|------|------|
| `harmonic_analysis` | 谐波分析 |
| `power_quality_analysis` | 电能质量分析 |
| `reactive_compensation_design` | 无功补偿设计 |

### 模型与拓扑类
| 技能 | 描述 |
|------|------|
| `topology_check` | 拓扑检查 |
| `parameter_sensitivity` | 参数灵敏度分析 |

## 安装

```bash
# 从源码安装
git clone https://git.tsinghua.edu.cn/chen_ying/cloudpss-toolkit.git
cd cloudpss-toolkit
pip install -e .

# 开发模式安装
pip install -e ".[dev]"
```

## 快速开始

### 配置Token

```bash
echo "your_token_here" > .cloudpss_token
```

### 列出所有技能

```bash
python -m cloudpss_skills list
```

### 运行技能

```bash
# 初始化配置
python -m cloudpss_skills init power_flow --output pf.yaml

# 运行
python -m cloudpss_skills run --config pf.yaml
```

### Python API 使用

```python
from cloudpss_skills import PowerFlowSkill

# 创建潮流计算任务
skill = PowerFlowSkill()
result = skill.run(
    model="model/holdme/IEEE39",
    tolerance=1e-6
)

print(f"收敛状态: {result.converged}")
print(f"迭代次数: {result.iterations}")
```

## 配置示例

### 无功补偿设计

```yaml
skill: reactive_compensation_design
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
vsi_input:
  vsi_result_file: ./results/vsi_weak_bus_result.json
compensation:
  device_type: capacitor  # sync_compensator/svg/svc/capacitor
  initial_capacity: 100
output:
  format: json
  path: ./results/
```

### VSI弱母线分析

```yaml
skill: vsi_weak_bus
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
analysis:
  threshold: 0.01
output:
  format: json
  path: ./results/
```

### 批处理任务管理

```yaml
skill: batch_task_manager
auth:
  token_file: .cloudpss_token
tasks:
  - name: pf_study
    type: skill
    skill: power_flow
    config:
      model:
        rid: model/holdme/IEEE39
execution:
  parallel: true
  max_workers: 4
```

## 示例代码

- `examples/basic/` - 基础用法示例（模型操作、组件修改）
- `examples/simulation/` - 完整仿真流程（潮流、EMT）
- `examples/analysis/` - 数据分析示例（N-1、参数扫描）

## 文档

- [项目成果总结](PROJECT_SUMMARY.md) - 完整的开发成果记录
- [文档索引](docs/README.md) - 所有文档入口
- [技能文档](docs/skills/) - 各技能详细说明
- [API参考](docs/api-reference/) - SDK API文档
- [工作流指南](docs/guides/) - 研究工作流指南

## 测试

```bash
# 运行单元测试（本地，无需网络）
pytest tests/ -q

# 运行集成测试（需要CloudPSS token）
pytest --run-integration -m "integration and not slow_emt"

# 生成覆盖率报告
pytest --cov=cloudpss_skills --cov-report=html
```

## 项目结构

```
cloudpss-toolkit/
├── cloudpss_skills/           # 技能包核心
│   ├── builtin/               # 30个内置技能
│   ├── core/                  # 核心框架
│   └── __main__.py            # CLI入口
├── config/                    # YAML配置示例（30+）
├── examples/                  # 示例程序（25+）
├── tests/                     # 测试套件
└── docs/                      # 文档
```

## 相关资源

- [CloudPSS平台](https://cloudpss.net/)
- [项目文档](docs/README.md)
- [开发日志](docs/development/vsi_development_summary.md)

## 许可证

MIT License

---

**维护者**: Chen Ying
