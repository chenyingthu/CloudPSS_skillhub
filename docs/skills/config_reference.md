# 配置参考

## 全局配置项

### 顶层字段

| 字段 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| `skill` | string | 是 | 技能名称 |
| `version` | string | 否 | 配置版本，默认"1.0" |
| `auth` | object | 是 | 认证设置 |
| `model` | object | 是 | 模型设置 |

### 认证设置 (auth)

| 字段 | 类型 | 默认 | 说明 |
|-----|------|-----|------|
| `token` | string | - | API Token（直接指定） |
| `token_file` | string | .cloudpss_token | Token文件路径 |

**注意**: `token` 和 `token_file` 二选一，同时存在时 `token` 优先。

### 模型设置 (model)

| 字段 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| `rid` | string | 是 | 模型RID或本地路径 |
| `source` | enum | cloud | 模型来源: cloud/local |

### 输出设置 (output)

| 字段 | 类型 | 默认 | 说明 |
|-----|------|-----|------|
| `format` | enum | csv | 输出格式: csv/json/yaml |
| `path` | string | ./results/ | 输出目录 |
| `prefix` | string | output | 文件名前缀 |
| `timestamp` | boolean | true | 添加时间戳 |

---

## 技能特定配置

### emt_simulation

#### simulation 字段

| 字段 | 类型 | 默认 | 说明 |
|-----|------|-----|------|
| `duration` | number | - | 仿真时长（秒） |
| `step_size` | number | - | 仿真步长（秒） |
| `timeout` | integer | 300 | 超时时间（秒） |

#### output.channels 字段

- `[]` - 导出所有通道
- `["channel1", "channel2"]` - 指定通道
- `["Bus*_V*"]` - 支持通配符（未来支持）

**完整示例**:

```yaml
skill: emt_simulation
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE3
  source: cloud
simulation:
  duration: 10.0
  step_size: 0.0001
  timeout: 300
output:
  format: csv
  path: ./results/
  prefix: emt_output
  timestamp: true
  channels: []  # 导出全部
```

---

### power_flow

#### algorithm 字段

| 字段 | 类型 | 默认 | 说明 |
|-----|------|-----|------|
| `type` | enum | newton_raphson | newton_raphson/fast_decoupled |
| `tolerance` | number | 1e-6 | 收敛精度 |
| `max_iterations` | integer | 100 | 最大迭代次数 |

#### 仿真等待

技能会自动等待仿真完成，最大等待时间为 **120秒**。如果超时，将报告失败。

**完整示例**:

```yaml
skill: power_flow
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
algorithm:
  type: newton_raphson
  tolerance: 1.0e-6
  max_iterations: 100
output:
  format: json
  path: ./results/
  prefix: pf_result
  timestamp: true
```

---

### ieee3_prep

#### fault 字段

| 字段 | 类型 | 默认 | 说明 |
|-----|------|-----|------|
| `start_time` | number | 2.5 | 故障起始时间（秒） |
| `end_time` | number | 2.7 | 故障结束时间（秒） |

#### output 字段

| 字段 | 类型 | 默认 | 说明 |
|-----|------|-----|------|
| `sampling_freq` | integer | 2000 | 采样频率（Hz） |
| `filename` | string | ieee3_prepared.yaml | 输出文件名 |

**完整示例**:

```yaml
skill: ieee3_prep
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE3
fault:
  start_time: 2.5
  end_time: 2.7
output:
  sampling_freq: 2000
  path: ./
  filename: ieee3_prepared.yaml
```

---

### waveform_export

#### source 字段

| 字段 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| `job_id` | string | 是 | 仿真任务ID |
| `auth` | object | 否 | 认证设置（如未设置使用全局） |

#### export 字段

| 字段 | 类型 | 默认 | 说明 |
|-----|------|-----|------|
| `plots` | array | [] | 分组索引列表，空表示全部 |
| `channels` | array | [] | 通道名称列表，空表示全部 |
| `time_range` | object | - | 时间范围切片 |

#### time_range 字段

| 字段 | 类型 | 说明 |
|-----|------|------|
| `start` | number | 开始时间（秒） |
| `end` | number | 结束时间（秒） |

**完整示例**:

```yaml
skill: waveform_export
source:
  job_id: "abc123"
  auth:
    token_file: .cloudpss_token
export:
  plots: [0, 1]           # 导出第0、1分组
  channels: ["Bus1_Va"]   # 只导出指定通道
  time_range:
    start: 2.0
    end: 5.0
output:
  format: csv
  path: ./results/
  filename: waveforms.csv
```

---

## 数据类型定义

### 数值类型

- **number**: 浮点数（支持科学计数法）
- **integer**: 整数
- **boolean**: true/false
- **string**: 字符串

### 枚举类型

**source**:
- `cloud` - CloudPSS云端
- `local` - 本地文件

**format**:
- `csv` - CSV格式
- `json` - JSON格式
- `yaml` - YAML格式
- `png` - 图片格式（图表）

**algorithm_type**:
- `newton_raphson` - 牛顿拉夫逊法
- `fast_decoupled` - 快速分解法

---

## 环境变量支持

配置中支持使用环境变量：

```yaml
auth:
  token: "${CLOUDPSS_TOKEN}"

model:
  rid: "${MODEL_RID:-model/holdme/IEEE3}"  # 支持默认值
```

语法：
- `${VAR}` - 使用环境变量
- `${VAR:-default}` - 变量不存在时使用默认值

---

## 配置验证规则

### 必填字段检查

- 所有 `required: true` 的字段必须存在
- 空字符串视为无效

### 类型检查

- 数值字段不能为NaN或Infinity
- 路径字段不能包含非法字符
- 枚举字段值必须在允许列表中

### 范围检查

- `duration > 0`
- `timeout >= 0`
- `sampling_freq > 0`
- `0 < tolerance < 1`

### 依赖检查

- `auth` 必须有 `token` 或 `token_file`
- `model.rid` 不能为空

---

## 配置示例集

### 示例1: 基础EMT仿真

```yaml
skill: emt_simulation
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE3
output:
  format: csv
  path: ./results/
```

### 示例2: 指定输出通道

```yaml
skill: emt_simulation
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE3
output:
  format: csv
  path: ./results/
  channels:
    - "Bus1_Va"
    - "Bus1_Vb"
    - "Bus1_Vc"
```

### 示例3: 本地模型

```yaml
skill: emt_simulation
auth:
  token_file: .cloudpss_token
model:
  rid: ./models/my_model.yaml
  source: local
output:
  format: json
  path: ./results/
```

### 示例4: 批量配置

```yaml
# config_1.yaml
skill: power_flow
model:
  rid: model/holdme/IEEE39
output:
  format: json

# config_2.yaml
skill: power_flow
model:
  rid: model/holdme/IEEE3
output:
  format: json
```

批量运行：

```bash
python -m cloudpss_skills batch --config-dir ./configs/
```

---

**文档版本**: 1.0.1
**最后更新**: 2026-03-25

## 附录: 技能执行行为

### 仿真等待机制

以下技能在执行仿真时会自动等待完成：

| 技能 | 仿真类型 | 最大等待时间 | 轮询间隔 |
|------|----------|-------------|----------|
| `power_flow` | 潮流计算 | 120秒 | 2秒 |
| `batch_powerflow` | 批量潮流 | 120秒/模型 | 2秒 |
| `n1_security` | N-1校核 | 120秒/支路 | 2秒 |
| `param_scan` | 参数扫描 | 120秒/参数 | 2秒 |
| `emt_simulation` | EMT仿真 | 300秒 | 3秒 |

**状态码说明**:
- `status=0` - 运行中
- `status=1` - 已完成（成功）
- `status=2` - 失败
