# COMTRADE导出技能 (COMTRADE Export)

## 设计背景

### 研究对象

COMTRADE（Common Format for Transient Data Exchange）是IEEE Std C37.111标准定义的电力系统暂态数据交换格式，广泛应用于继电保护测试、故障录波分析、RTDS仿真等领域。该格式由.cfg配置文件（通道元数据）和.dat数据文件（时序采样值）组成，是电力系统领域的通用标准格式。

### 实际需求

在电力系统仿真研究中，经常需要将仿真结果导出为标准格式以便：

1. **继电保护测试**: 导入RelaySimTest、OMICRON等专业测试设备进行保护装置测试
2. **故障分析**: 使用SEL、Beckwith等故障录波分析软件进行波形分析
3. **跨平台仿真**: 将CloudPSS仿真结果导入RTDS、PSCAD等其他仿真平台
4. **报告归档**: 生成符合行业标准的波形记录文件
5. **第三方验证**: 提供标准格式数据供外部工具验证仿真结果

### 期望的输入和输出

**输入**:

- CloudPSS EMT仿真任务的Job ID
- 要导出的波形分组索引（默认为0）
- 通道筛选配置（可选）
- 单位和相别映射（可选，支持自动识别）
- COMTRADE标准参数（厂站名、频率、版本等）
- 输出格式配置（BINARY/ASCII）

**输出**:

- .cfg配置文件：包含通道定义、采样率、时间信息等元数据
- .dat数据文件：包含时序采样数据（二进制或ASCII格式）
- 导出报告：包含通道数、采样点数、采样率等统计信息

### 计算结果的用途和价值

COMTRADE导出结果可直接用于：

- **保护装置测试**: 作为数字继电保护测试仪的输入信号
- **故障录波分析**: 导入专业软件进行谐波分析、序分量分析
- **波形对比**: 与实测录波数据或第三方仿真结果对比
- **标准归档**: 符合IEEE C37.111标准的数据存储格式
- **协同仿真**: 与其他电力系统仿真软件进行数据交换

## 功能特性

- **标准兼容**: 符合IEEE Std C37.111-1991/1999/2013标准
- **双格式支持**: 支持BINARY（二进制）和ASCII两种数据格式
- **智能识别**: 自动识别通道类型（电压/电流/功率）和单位
- **灵活配置**: 支持自定义单位、相别、变比等参数
- **通道筛选**: 可选择性导出特定通道
- **高兼容性**: 生成的文件可被主流继电保护测试软件读取

## 快速开始

### CLI方式（推荐）

```bash
# 基础导出（自动识别参数）
python -m cloudpss_skills run --config config_comtrade.yaml
```

### 配置示例

```yaml
skill: comtrade_export
auth:
  token_file: .cloudpss_token
source:
  job_id: "job-abc123-xxxx"
  plot_index: 0
comtrade:
  station_name: "IEEE39"
  rec_dev_id: "EMT"
  rev_year: 1999
  frequency: 50.0
channels:
  selected: []  # 空数组表示全部通道
  uu_map:
    Bus30_V: "kV"
    Gen1_P: "MW"
output:
  format: BINARY
  path: ./results/
  filename: ieee39_fault
```

## 配置参数详解

### source（数据源）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `job_id` | string | ✅ | - | EMT仿真任务ID |
| `plot_index` | integer | ❌ | 0 | 波形分组索引 |

### comtrade（COMTRADE参数）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `station_name` | string | ❌ | "CloudPSS" | 厂站名称 |
| `rec_dev_id` | string | ❌ | "EMT" | 记录装置标识 |
| `rev_year` | integer | ❌ | 1999 | 版本年号(1991/1999/2013) |
| `frequency` | number | ❌ | 50.0 | 系统频率(Hz) |
| `time_mult` | number | ❌ | 1.0 | 时间戳倍率因子 |

### channels（通道配置）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `selected` | list | ❌ | [] | 要导出的通道列表，空数组表示全部 |
| `uu_map` | dict | ❌ | {} | 通道名称到单位的映射 |
| `ph_map` | dict | ❌ | {} | 通道名称到相别的映射 |
| `ratio_map` | dict | ❌ | {} | 通道名称到变比的映射 |

**自动识别规则**:
- 单位识别：包含`_v`或`voltage`→kV，包含`_i`或`current`→kA，包含`_p`或`power`→MW
- 相别识别：包含`_a`或`_0`→A相，包含`_b`或`_1`→B相，包含`_c`或`_2`→C相

### output（输出配置）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `path` | string | ❌ | "./results/" | 输出目录 |
| `filename` | string | ❌ | "" | 文件名前缀（默认使用job_id） |
| `file_type` | string | ❌ | "BINARY" | 格式：BINARY/ASCII |

## 配置示例

### 示例1：基础导出

```yaml
skill: comtrade_export
auth:
  token_file: .cloudpss_token
source:
  job_id: "job-abc123-xxxx"
comtrade:
  station_name: "TestSystem"
  frequency: 50.0
output:
  file_type: BINARY
  filename: fault_record
```

### 示例2：指定通道和单位

```yaml
skill: comtrade_export
source:
  job_id: "job-def456-yyyy"
channels:
  selected:
    - Bus30_V
    - Bus38_V
    - Line_1_I
  uu_map:
    Bus30_V: "kV"
    Bus38_V: "kV"
    Line_1_I: "kA"
  ph_map:
    Bus30_V: "A"
    Bus38_V: "A"
    Line_1_I: "A"
output:
  file_type: ASCII
  filename: selected_channels
```

### 示例3：带变比的导出

```yaml
skill: comtrade_export
source:
  job_id: "job-ghi789-zzzz"
channels:
  ratio_map:
    Bus30_V: [220.0, 1.0]  # 一次值220kV，二次值1kV
    Bus38_V: [500.0, 1.0]  # 一次值500kV，二次值1kV
comtrade:
  station_name: "500kVSystem"
  rev_year: 2013
output:
  file_type: BINARY
  filename: hv_system
```

## 输出结果说明

### CFG文件结构

```
CloudPSS,EMT,1999                    <- 厂站名,装置标识,版本年号
3,3A,0D                               <- 通道总数,模拟通道数,状态通道数
1,Bus30_V,A,Bus30_V,kV,0.001,0.0,0.0,-32767,32767,220.0,1.0,p
2,Bus38_V,A,Bus38_V,kV,0.001,0.0,0.0,-32767,32767,500.0,1.0,p
3,Line_1_I,A,Line_1_I,kA,0.001,0.0,0.0,-32767,32767,1.0,1.0,p
50.000000                             <- 系统频率
1                                     <- 采样率个数
1000.000000,10000                     <- 采样率(Hz),采样点数
01/01/2024,12:00:00.000               <- 开始时间
01/01/2024,12:00:10.000               <- 结束时间
BINARY                                <- 文件格式
1.000000                              <- 时间倍率
```

### DAT文件格式

**BINARY格式**:
- 每个采样点：采样序号(4字节) + 时间戳(4字节) + 通道数据(2字节×通道数)
- 小端序(Little Endian)
- 时间戳单位：微秒

**ASCII格式**:
- 每行：采样序号,时间戳,通道1值,通道2值,...
- CSV格式，逗号分隔

### SkillResult结构

```json
{
  "skill_name": "comtrade_export",
  "status": "SUCCESS",
  "data": {
    "job_id": "job-abc123-xxxx",
    "channels_exported": 3,
    "samples": 10000,
    "sampling_rate_hz": 1000.0,
    "file_type": "BINARY",
    "cfg_file": "./results/fault_record.cfg",
    "dat_file": "./results/fault_record.dat"
  },
  "artifacts": [
    {"type": "cfg", "path": "./results/fault_record.cfg", ...},
    {"type": "dat", "path": "./results/fault_record.dat", ...}
  ]
}
```

## 设计原理

### 数据转换流程

```
1. 获取EMT结果 → 从CloudPSS拉取Job结果
2. 提取波形数据 → 获取时序和幅值
3. 计算转换因子 → A=(max-min)/8192, B=(max+min)/2
4. 生成CFG文件 → 元数据和通道配置
5. 生成DAT文件 → 采样点数据（二进制或ASCII）
```

### 转换因子计算

- **A因子**: (最大值 - 最小值) / 8192
- **B因子**: (最大值 + 最小值) / 2
- **原始值 → 整数值**: (value - B) / A
- **整数值 → 原始值**: value × A + B

### 时间戳处理

- **时间单位**: 秒（原始数据）→ 微秒（COMTRADE）
- **转换公式**: timestamp = time_seconds × 1000000 / time_mult
- **时间倍率**: 默认为1，可调整以适应不同时间尺度

## 使用场景

### 场景1：继电保护测试

将故障仿真结果导出为COMTRADE格式，导入OMICRON CMC或RelaySimTest进行保护装置测试。

```yaml
source:
  job_id: "fault_sim_job_id"
comtrade:
  station_name: "RelayTest"
  frequency: 50.0
output:
  file_type: BINARY  # 测试仪通常要求二进制格式
```

### 场景2：故障录波分析

导出波形到SEL-5601或Beckwith软件进行详细的故障分析。

```yaml
channels:
  selected:
    - Bus7_V
    - Bus8_V
    - Line_I
  uu_map:
    Bus7_V: "kV"
    Bus8_V: "kV"
    Line_I: "kA"
```

### 场景3：跨平台仿真

将CloudPSS结果导出后导入RTDS进行硬件在环仿真。

```yaml
output:
  file_type: ASCII  # 便于查看和调试
  filename: cloudpss_to_rtds
```

## 注意事项

1. **数据精度**: BINARY格式使用16位整数，精度约0.015%，一般够用
2. **时间同步**: 确保仿真时间从0开始，避免负时间戳
3. **通道命名**: COMTRADE通道ID有64字符限制，超长名称会被截断
4. **编码格式**: CFG文件使用GB2312编码，确保中文厂站名正确显示
5. **采样率**: 自动从数据推断，不均匀采样可能产生误差

## 故障排除

### 问题1："没有波形数据"

**原因**: Job不是EMT仿真或结果为空
**解决**: 确认Job ID是已完成的EMT仿真任务

### 问题2：测试仪无法读取文件

**原因**: 格式不兼容或编码问题
**解决**: 尝试ASCII格式，检查rev_year是否与测试仪兼容

### 问题3：数值显示异常

**原因**: 单位或变比设置错误
**解决**: 检查uu_map和ratio_map配置

### 问题4：中文厂站名乱码

**原因**: 编码问题
**解决**: 使用英文厂站名或确保软件支持GB2312编码

## 相关技能

- **waveform_export**: 导出为CSV/JSON格式
- **hdf5_export**: 导出为HDF5格式（适合大数据量）
- **emt_simulation**: 运行EMT仿真获取数据源
- **compare_visualization**: 可视化对比（可与COMTRADE转换后的数据对比）

## 完整示例

### 场景描述

对IEEE39系统进行三相短路故障仿真，将结果导出为COMTRADE格式用于继电保护测试。

### 配置文件

```yaml
skill: comtrade_export
auth:
  token_file: .cloudpss_token
source:
  job_id: "job-20240315-001-3ph-fault"
  plot_index: 0
comtrade:
  station_name: "IEEE39_Test"
  rec_dev_id: "CloudPSS_EMT"
  rev_year: 1999
  frequency: 50.0
  time_mult: 1.0
channels:
  selected:
    - Bus30_V
    - Bus38_V
    - Bus26_V
    - Line_1_I
    - Line_2_I
  uu_map:
    Bus30_V: "kV"
    Bus38_V: "kV"
    Bus26_V: "kV"
    Line_1_I: "kA"
    Line_2_I: "kA"
  ph_map:
    Bus30_V: "A"
    Bus38_V: "A"
    Bus26_V: "A"
    Line_1_I: "A"
    Line_2_I: "A"
  ratio_map:
    Bus30_V: [220.0, 1.0]
    Bus38_V: [500.0, 1.0]
    Bus26_V: [220.0, 1.0]
    Line_1_I: [1.0, 1.0]
    Line_2_I: [1.0, 1.0]
output:
  file_type: BINARY
  path: ./results/comtrade/
  filename: ieee39_3ph_fault
```

### 执行命令

```bash
python -m cloudpss_skills run --config config_comtrade.yaml
```

### 预期输出

```
[INFO] 加载认证信息...
[INFO] 认证成功
[INFO] 获取任务结果: job-20240315-001-3ph-fault
[INFO] 找到 5 个通道
[INFO] 将导出 5 个通道
[INFO] 收集波形数据...
[INFO] 数据点数: 10000, 采样率: 1000.00 Hz
[INFO] 生成CFG配置文件...
[INFO] CFG文件已保存: ieee39_3ph_fault.cfg
[INFO] 生成DAT数据文件 (BINARY)...
[INFO] DAT文件已保存: ieee39_3ph_fault.dat
[INFO] COMTRADE导出完成
```

### 结果文件

- `ieee39_3ph_fault.cfg` - 配置文件，包含5个通道的定义
- `ieee39_3ph_fault.dat` - 二进制数据文件，包含10000个采样点

### 后续应用

1. **导入测试仪**: 使用OMICRON RelaySimTest导入.cfg和.dat文件
2. **配置测试**: 设置保护装置的定值和测试序列
3. **执行测试**: 回放故障波形，验证保护动作
4. **对比分析**: 将测试结果与仿真预期对比

**支持的软件**:
- OMICRON RelaySimTest / Test Universe
- Doble F6150 / Protection Suite
- SEL-5601 / ACSELERATOR
- Beckwith Electric M-3425
- GE UR / EnerVista
- 南瑞继保PCS-9794
- 四方CSC-103

---

*COMTRADE是IEEE标准协会注册商标*
