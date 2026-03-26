# CloudPSS 技能系统 - 用户手册

## 目录

1. [概述](#概述)
2. [安装](#安装)
3. [快速开始](#快速开始)
4. [配置详解](#配置详解)
5. [技能列表](#技能列表)
6. [CLI命令](#cli命令)
7. [故障排查](#故障排查)
8. [最佳实践](#最佳实践)

---

## 概述

CloudPSS技能系统是一个**配置驱动的电力系统仿真工具**。它将复杂的仿真流程封装为预置的技能，用户只需通过YAML配置文件即可运行仿真，无需编写任何代码。

### 核心特性

- **零编程门槛** - 编辑YAML即可运行仿真
- **预置技能** - EMT、潮流等常用功能开箱即用
- **一键执行** - 简化操作，隐藏技术细节
- **确定性结果** - 相同配置产生相同输出
- **可扩展** - 支持自定义技能

### 工作流程

```
用户配置 (YAML) → 技能执行 → 结果输出
```

---

## 安装

### 前置条件

- Python 3.8+
- CloudPSS SDK 4.5.28+

### 安装步骤

1. **安装CloudPSS SDK**（如未安装）

```bash
pip install cloudpss
```

2. **验证安装**

```bash
python -c "import cloudpss; print(cloudpss.__version__)"
```

3. **配置Token**

```bash
# 在项目根目录创建token文件
echo "your_api_token" > .cloudpss_token
```

---

## 快速开始

### 5分钟上手指南

#### 第1步：查看可用技能

```bash
$ python -m cloudpss_skills list

可用技能 (10个):
------------------------------------------------------------

  emt_simulation
    描述: 运行EMT暂态仿真并导出波形数据
    版本: 1.0.0

  power_flow
    描述: 运行潮流计算并输出结果
    版本: 1.0.0

  ieee3_prep
    描述: 准备IEEE3模型用于EMT仿真
    版本: 1.0.0

  waveform_export
    描述: 从仿真结果导出波形数据
    版本: 1.0.0

  n1_security
    描述: N-1安全校核 - 逐一停运支路评估系统安全性
    版本: 1.0.0

  param_scan
    描述: 参数扫描 - 批量改变参数运行多次仿真
    版本: 1.0.0

  result_compare
    描述: 对比多次仿真结果，生成差异分析报告
    版本: 1.0.0

  visualize
    描述: 生成波形图和结果可视化图表
    版本: 1.0.0

  topology_check
    描述: 检查模型拓扑完整性和连通性
    版本: 1.0.0

  batch_powerflow
    描述: 批量对多个模型运行潮流计算
    版本: 1.0.0
```

#### 第2步：创建配置

```bash
$ python -m cloudpss_skills init emt_simulation --output my_simulation.yaml
[OK] 配置文件已创建: my_simulation.yaml
[INFO] 编辑此文件后运行: python -m cloudpss_skills run --config my_simulation.yaml
```

#### 第3步：编辑配置

```yaml
# my_simulation.yaml
skill: emt_simulation

auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3
  source: cloud

simulation:
  duration: 10.0
  timeout: 300

output:
  format: csv
  path: ./results/
  prefix: ieee3_emt
  timestamp: true
```

#### 第4步：运行仿真

```bash
$ python -m cloudpss_skills run --config my_simulation.yaml

[14:32:01] [INFO] Token 已设置
[14:32:02] [INFO] 获取模型: model/holdme/IEEE3
[14:32:03] [INFO] 检查EMT拓扑
[14:32:05] [INFO] 启动EMT仿真...
[14:32:05] [INFO] 任务已创建，ID: xxx
[14:32:15] [INFO] 运行中... (10s)
...
[14:32:45] [INFO] 仿真已完成
[14:32:46] [INFO] 导出: ./results/ieee3_emt_20240324_143245_plot_0.csv

[OK] 技能执行成功: emt_simulation
耗时: 45.23s
```

---

## 配置详解

### 配置文件结构

```yaml
skill: <skill_name>          # 技能名称（必填）
version: "1.0"               # 配置版本（可选）

auth:                        # 认证设置
  token: "..."              # 直接指定token
  token_file: ".token"      # 从文件读取

model:                       # 模型设置
  rid: "model/holdme/..."   # 模型RID（必填）
  source: "cloud"           # 来源: cloud | local

simulation:                  # 仿真参数（可选）
  duration: 10.0
  step_size: 0.0001
  timeout: 300

output:                      # 输出设置
  format: "csv"             # 格式: csv | json | yaml
  path: "./results/"        # 输出目录
  prefix: "output"          # 文件名前缀
  timestamp: true           # 是否添加时间戳
```

### 认证方式

支持三种认证方式（优先级从高到低）：

1. **环境变量**（推荐用于CI/CD）

```yaml
auth:
  token: "${CLOUDPSS_TOKEN}"
```

2. **Token文件**（推荐用于交互使用）

```yaml
auth:
  token_file: ".cloudpss_token"
```

3. **直接指定**（不推荐，可能泄露）

```yaml
auth:
  token: "your_token_here"
```

### 模型来源

- **cloud**: 从CloudPSS云端获取
- **local**: 从本地YAML文件加载

```yaml
model:
  rid: "model/holdme/IEEE3"      # cloud模式
  # rid: "./local_model.yaml"     # local模式
  source: "cloud"
```

---

## 技能列表

### emt_simulation

运行EMT暂态仿真并导出波形数据。

**配置Schema**:

```yaml
skill: emt_simulation
auth:
  token_file: ".cloudpss_token"
model:
  rid: "model/holdme/IEEE3"
  source: "cloud"
simulation:
  duration: 10.0          # 仿真时长（秒）
  step_size: 0.0001       # 步长（秒）
  timeout: 300            # 超时（秒）
output:
  format: "csv"           # csv | json | yaml
  path: "./results/"
  prefix: "emt_output"
  timestamp: true
  channels: []            # 通道列表，空表示全部
```

**输出**:

- CSV/JSON格式的波形数据
- 包含时间序列和通道数值

---

### power_flow

运行潮流计算。

**配置Schema**:

```yaml
skill: power_flow
auth:
  token_file: ".cloudpss_token"
model:
  rid: "model/holdme/IEEE39"
algorithm:
  type: "newton_raphson"  # newton_raphson | fast_decoupled
  tolerance: 1.0e-6
  max_iterations: 100
output:
  format: "json"
  path: "./results/"
```

**输出**:

- JSON格式的潮流计算结果
- 节点电压、支路功率等

---

### ieee3_prep

准备IEEE3模型用于EMT仿真。

**配置Schema**:

```yaml
skill: ieee3_prep
auth:
  token_file: ".cloudpss_token"
model:
  rid: "model/holdme/IEEE3"
fault:
  start_time: 2.5         # 故障开始时间（秒）
  end_time: 2.7           # 故障结束时间（秒）
output:
  sampling_freq: 2000     # 采样频率（Hz）
  path: "./"
  filename: "ieee3_prepared.yaml"
```

**输出**:

- 准备好的模型YAML文件

---

### waveform_export

从已有仿真任务导出波形数据。

**配置Schema**:

```yaml
skill: waveform_export
source:
  job_id: "your_job_id"   # 仿真任务ID（必填）
  auth:
    token_file: ".cloudpss_token"
export:
  plots: []               # 分组索引列表
  channels: []            # 通道名称列表
  time_range:
    start: 0.0
    end: 10.0
output:
  format: "csv"
  path: "./results/"
```

**输出**:

- CSV/JSON格式的波形数据
- 支持时间范围切片

---

### n1_security

N-1安全校核 - 逐一停运支路评估系统安全性。

**配置Schema**:

```yaml
skill: n1_security
auth:
  token_file: ".cloudpss_token"
model:
  rid: "model/holdme/IEEE39"
analysis:
  branches: []              # 要检查的支路，空表示全部
  check_voltage: true
  check_thermal: true
  voltage_threshold: 0.05   # 电压越限阈值
  thermal_threshold: 1.0    # 热稳定阈值
output:
  format: "json"
  path: "./results/"
```

**输出**:

- JSON格式的N-1校核报告
- 包含通过/失败的支路列表

---

### param_scan

参数扫描 - 批量改变参数运行多次仿真。

**配置Schema**:

```yaml
skill: param_scan
auth:
  token_file: ".cloudpss_token"
model:
  rid: "model/holdme/IEEE3"
scan:
  component: "Bus1_Load"    # 元件ID或名称
  parameter: "P"            # 参数名
  values: [10, 20, 30, 40]  # 参数值列表
  simulation_type: "power_flow"  # power_flow | emt
output:
  format: "json"
  path: "./results/"
```

**输出**:

- JSON格式的扫描结果
- 每个参数值对应的仿真结果

---

### result_compare

对比多次仿真结果，生成差异分析报告。

**配置Schema**:

```yaml
skill: result_compare
source:
  - job_id: "abc123"
    label: "Case A"
  - job_id: "def456"
    label: "Case B"
compare:
  channels: ["Bus1_Va"]
  metrics: [max, min, mean]
output:
  format: "markdown"
  path: "./results/"
```

**输出**:

- Markdown或JSON格式的对比报告
- 通道指标对比表

---

### visualize

生成波形图和结果可视化图表。

**配置Schema**:

```yaml
skill: visualize
source:
  job_id: "your_job_id"     # 或 data_file: "./data.csv"
plot:
  type: "time_series"       # time_series | bar | scatter
  channels: ["Bus1_Va"]
  title: "波形图"
output:
  format: "png"             # png | pdf | svg
  path: "./results/"
  dpi: 150
```

**输出**:

- PNG/PDF/SVG格式的图表文件

---

### topology_check

检查模型拓扑完整性和连通性。

**配置Schema**:

```yaml
skill: topology_check
auth:
  token_file: ".cloudpss_token"
model:
  rid: "model/holdme/IEEE39"
checks:
  islands: true
  dangling: true
  parameter: true
  emt_ready: false
output:
  format: "json"
  path: "./results/"
```

**输出**:

- JSON格式的拓扑检查报告
- 包含问题和警告列表

---

### batch_powerflow

批量对多个模型运行潮流计算。

**配置Schema**:

```yaml
skill: batch_powerflow
auth:
  token_file: ".cloudpss_token"
models:
  - rid: "model/holdme/IEEE39"
    name: "IEEE39"
  - rid: "model/holdme/IEEE3"
    name: "IEEE3"
algorithm:
  type: "newton_raphson"
output:
  format: "json"
  path: "./results/"
  aggregate: true
```

**输出**:

- JSON格式的批量计算结果
- Markdown汇总报告

---

## CLI命令

### list

列出所有可用技能。

```bash
python -m cloudpss_skills list
```

### describe

查看技能详细信息。

```bash
python -m cloudpss_skills describe emt_simulation
python -m cloudpss_skills describe emt_simulation --verbose  # 显示Schema
```

### init

创建配置模板。

```bash
# 从模板创建
python -m cloudpss_skills init emt_simulation --output sim.yaml

# 交互式创建
python -m cloudpss_skills init emt_simulation --interactive --output sim.yaml
```

### run

运行技能。

```bash
python -m cloudpss_skills run --config sim.yaml
python -m cloudpss_skills run --config sim.yaml --verbose  # 详细输出
```

### validate

验证配置文件。

```bash
python -m cloudpss_skills validate --config sim.yaml
```

### batch

批量运行多个配置。

```bash
python -m cloudpss_skills batch --config-dir ./configs/
```

### version

显示版本信息。

```bash
python -m cloudpss_skills version
```

---

## 故障排查

### 常见问题

#### 1. "Token文件不存在"

**原因**: `.cloudpss_token`文件不存在或路径错误

**解决**:

```bash
# 创建token文件
echo "your_token" > .cloudpss_token

# 或在配置中指定其他路径
auth:
  token_file: "/path/to/token"
```

#### 2. "模型不存在"

**原因**: 指定的模型RID不存在或无权访问

**解决**:

- 确认模型RID正确
- 确认Token有访问权限
- 使用 `model/holdme/IEEE3` 测试

#### 3. "EMT拓扑检查失败"

**原因**: 模型未配置EMT参数

**解决**:

- 先运行 `ieee3_prep` 技能准备模型
- 检查模型是否有EMT计算方案

#### 4. "配置验证失败"

**原因**: 配置文件格式错误

**解决**:

```bash
# 验证配置
python -m cloudpss_skills validate --config sim.yaml

# 查看错误详情
python -m cloudpss_skills validate --config sim.yaml --verbose
```

---

## 最佳实践

### 1. 配置管理

- 将配置文件放入 `configs/` 目录
- 使用描述性文件名：`ieee3_fault_sim.yaml`
- 版本控制配置（不含敏感信息）

### 2. Token安全

- 从不提交token到版本控制
- 使用环境变量或外部文件
- 设置适当的文件权限：`chmod 600 .cloudpss_token`

### 3. 批量仿真

```bash
# 创建多个配置
configs/
├── sim_10ms.yaml
├── sim_20ms.yaml
└── sim_30ms.yaml

# 批量运行
python -m cloudpss_skills batch --config-dir ./configs/
```

### 4. 结果管理

- 使用 `timestamp: true` 自动添加时间戳
- 设置有意义的 `prefix`
- 将结果目录加入 `.gitignore`

### 5. 调试技巧

```bash
# 验证配置但不运行
python -m cloudpss_skills validate --config sim.yaml

# 查看技能详情
python -m cloudpss_skills describe emt_simulation --verbose

# 详细日志
python -m cloudpss_skills run --config sim.yaml --verbose
```

---

## 附录

### 环境变量

| 变量 | 说明 |
|-----|------|
| `CLOUDPSS_TOKEN` | API Token |
| `CLOUDPSS_SKILL_CONFIG` | 默认配置文件路径 |

### 配置搜索路径

1. `--config` 指定的路径
2. `$CLOUDPSS_SKILL_CONFIG`
3. `./skill.yaml`
4. `./.cloudpss/skill.yaml`
5. `~/.cloudpss/skill.yaml`

---

**文档版本**: 1.0.0
**最后更新**: 2024-03-24
