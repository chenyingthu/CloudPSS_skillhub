# HDF5数据导出技能

## 设计背景

### 研究对象

电力系统仿真产生多种类型的数据，包括EMT波形数据、潮流计算结果、VSI分析结果、扰动严重度指标等。这些数据需要长期存储、高效检索和跨平台交换。

### 实际需求

工程师和数据科学家需要：

1. **标准化存储**：统一的格式存储不同类型的仿真结果
2. **高效压缩**：减少存储空间占用
3. **元数据管理**：完整记录数据的上下文信息
4. **跨平台兼容**：支持Python、MATLAB、Julia等多种工具
5. **快速检索**：快速读取特定数据集而无需加载全部数据

### 期望的输入和输出

**输入**:
- 数据源（EMT结果、潮流结果、VSI结果、JSON文件等）
- 元数据（标题、描述、标签、自定义属性）
- 压缩配置（算法、级别）
- 存储选项（分块大小、包含内容）

**输出**:
- HDF5格式数据文件（.h5）
- JSON格式索引文件（.json）
- 文件元数据和结构信息

### 计算结果的用途和价值

HDF5格式数据可用于：
- 大规模仿真结果归档
- 长期数据存储和版本管理
- 跨团队协作和数据共享
- 机器学习训练数据准备
- 高性能科学计算数据交换

## 功能特性

- **多数据源支持**：支持EMT、PowerFlow、VSI、扰动严重度等结果导出
- **元数据索引**：完整的数据描述和自定义属性
- **压缩存储**：支持gzip、lzf压缩算法，减少存储空间
- **跨平台兼容**：与NumPy/Pandas/ MATLAB/Julia无缝集成
- **JSON索引**：自动生成数据索引文件，便于快速检索

## 快速开始

### 3.1 CLI方式（推荐）

```bash
# 初始化HDF5导出配置
python -m cloudpss_skills init hdf5_export --output hdf5_export.yaml

# 编辑配置后运行
python -m cloudpss_skills run --config hdf5_export.yaml
```

### 3.2 Python API方式

```python
from cloudpss_skills import get_skill

# 获取技能
skill = get_skill("hdf5_export")

# 配置
config = {
    "skill": "hdf5_export",
    "source": {
        "type": "file",
        "file_path": "./results/emt_result.json"
    },
    "output": {
        "path": "./results/",
        "filename": "simulation_data.h5",
        "compression": "gzip",
        "compression_level": 4
    },
    "metadata": {
        "title": "IEEE39系统N-1分析",
        "description": "夏季峰值负荷场景下的N-1故障分析",
        "tags": ["IEEE39", "N-1", "summer_peak"],
        "custom_attrs": {
            "project": "TSQH_2026",
            "engineer": "chenying"
        }
    },
    "options": {
        "include_waveforms": True,
        "include_metrics": True,
        "chunk_size": 1000
    }
}

# 运行
result = skill.run(config)
print(f"HDF5导出完成: {result.data}")
```

### 3.3 YAML配置示例

```yaml
skill: hdf5_export
source:
  type: file                    # emt_result | powerflow_result | vsi_result | disturbance_result | file
  file_path: ./results/emt_result.json

output:
  path: ./results/
  filename: simulation_data.h5
  compression: gzip             # gzip | lzf | none
  compression_level: 4          # 1-9（仅gzip）

metadata:
  title: "仿真结果"
  description: "N-1故障分析"
  tags: ["N-1", "voltage_stability"]
  custom_attrs:
    project: "TSQH_2026"
    scenario: "summer_peak"

options:
  include_waveforms: true
  include_metrics: true
  chunk_size: 1000
```

## 配置Schema

### 4.1 完整配置结构

```yaml
skill: hdf5_export                     # 必需: 技能名称
source:                                 # 必需: 数据源配置
  type: enum                           # 源类型（见下方说明）
  rid: string                          # CloudPSS结果RID（cloud类型）
  file_path: string                    # 结果文件路径（file类型）

output:                                 # 输出配置
  path: string                         # 输出目录（默认: ./results/）
  filename: string                     # 输出文件名（可选）
  compression: enum                    # gzip | lzf | none（默认: gzip）
  compression_level: integer           # 压缩级别1-9（默认: 4）

metadata:                               # 元数据配置
  title: string                        # 数据集标题
  description: string                  # 数据集描述
  tags:                                # 标签列表
    - string
  custom_attrs:                        # 自定义属性
    key: value

options:                                # 选项配置
  include_waveforms: boolean           # 包含波形数据（默认: true）
  include_metrics: boolean             # 包含指标数据（默认: true）
  include_metadata: boolean            # 包含元数据（默认: true）
  chunk_size: integer                  # 数据块大小（默认: 1000）
```

**source.type 枚举值**:
- `emt_result`: EMT仿真结果
- `powerflow_result`: 潮流计算结果
- `vsi_result`: VSI弱母线分析结果
- `disturbance_result`: 扰动严重度分析结果
- `file`: 本地JSON文件

### 4.2 参数说明

| 参数路径 | 类型 | 必需 | 默认值 | 说明 |
|----------|------|------|--------|------|
| `skill` | string | 是 | - | 技能标识，必须为"hdf5_export" |
| `source.type` | enum | 是 | - | 源类型（见上方枚举） |
| `source.rid` | string | 条件 | - | CloudPSS结果RID（cloud类型必需） |
| `source.file_path` | string | 条件 | - | 文件路径（file类型必需） |
| `output.path` | string | 否 | ./results/ | 输出目录路径 |
| `output.filename` | string | 否 | 自动生成 | 输出文件名（.h5后缀） |
| `output.compression` | enum | 否 | gzip | 压缩算法: gzip/lzf/none |
| `output.compression_level` | integer | 否 | 4 | 压缩级别1-9（仅gzip） |
| `metadata.title` | string | 否 | - | 数据集标题 |
| `metadata.description` | string | 否 | - | 数据集描述 |
| `metadata.tags` | array | 否 | [] | 标签列表 |
| `metadata.custom_attrs` | object | 否 | {} | 自定义属性键值对 |
| `options.include_waveforms` | boolean | 否 | true | 是否包含波形数据 |
| `options.include_metrics` | boolean | 否 | true | 是否包含指标数据 |
| `options.chunk_size` | integer | 否 | 1000 | 数据块大小 |

## Agent使用指南

### 5.1 基本调用模式

```python
from cloudpss_skills import get_skill

# 获取技能实例
skill = get_skill("hdf5_export")

# 从JSON文件导出
config = {
    "source": {
        "type": "file",
        "file_path": "./results/result.json"
    }
}

# 验证并运行
validation = skill.validate(config)
if validation.valid:
    result = skill.run(config)
    if result.status == "SUCCESS":
        print(f"导出完成: {result.data}")
    else:
        print(f"导出失败: {result.error}")
```

### 5.2 处理结果

```python
result = skill.run(config)

# 检查结果状态
if result.status.value == "SUCCESS":
    data = result.data
    # 访问结果数据
    hdf5_file = data.get("hdf5_file")
    index_file = data.get("index_file")
    file_size_mb = data.get("file_size_mb")

    print(f"HDF5文件: {hdf5_file}")
    print(f"索引文件: {index_file}")
    print(f"文件大小: {file_size_mb:.2f} MB")

# 访问输出文件
for artifact in result.artifacts:
    print(f"输出文件: {artifact.path} ({artifact.type}, {artifact.size} bytes)")
```

### 5.3 错误处理

```python
result = skill.run(config)

if result.status.value == "FAILED":
    error_msg = result.error

    # 常见错误处理
    if "必须指定source配置" in error_msg:
        print("错误: 请配置source参数")
    elif "file类型必须指定file_path" in error_msg:
        print("错误: file类型需要提供file_path")
    elif "不支持的源类型" in error_msg:
        print("错误: source.type值无效")
    else:
        print(f"未知错误: {error_msg}")

# 使用技能提供的辅助方法读取HDF5
if result.status.value == "SUCCESS":
    # 读取全部数据
    data = skill.read_hdf5("./results/data.h5")

    # 读取特定数据集
    waveform = skill.read_hdf5("./results/data.h5", "waveforms/Bus_16_V")

    # 列出所有数据集
    datasets = skill.list_datasets("./results/data.h5")
    print(f"可用数据集: {datasets}")
```

## 输出结果

### 6.1 HDF5文件结构

```
/
├── _attrs (根属性)
│   ├── created: "2024-03-29T10:30:00"
│   ├── version: "1.0"
│   ├── source_type: "emt"
│   ├── title: "IEEE39系统N-1分析"
│   ├── description: "夏季峰值负荷场景"
│   └── tags: "N-1,voltage_stability"
├── waveforms (波形数据组)
│   ├── time (数据集: [10000])
│   ├── Bus_16_V (数据集: [10000])
│   └── Bus_15_V (数据集: [10000])
└── metadata (元数据组)
    └── (属性)
```

### 6.2 JSON索引文件

```json
{
  "hdf5_file": "simulation_data.h5",
  "created": "2024-03-29T10:30:00",
  "version": "1.0",
  "source_type": "emt",
  "groups": ["waveforms", "metadata"],
  "datasets": [
    {
      "path": "waveforms/time",
      "shape": [10000],
      "dtype": "float64",
      "size": 10000
    },
    {
      "path": "waveforms/Bus_16_V",
      "shape": [10000],
      "dtype": "float64",
      "size": 10000
    }
  ],
  "metadata": {
    "title": "IEEE39系统N-1分析",
    "description": "夏季峰值负荷场景",
    "tags": ["N-1", "voltage_stability"]
  }
}
```

### 6.3 SkillResult结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `skill_name` | string | 技能名称 "hdf5_export" |
| `status` | SkillStatus | SUCCESS / FAILED / PENDING / RUNNING / CANCELLED |
| `start_time` | datetime | 开始时间 |
| `end_time` | datetime | 结束时间 |
| `data` | dict | 结果数据字典（hdf5_file, index_file, file_size） |
| `artifacts` | list | 输出文件列表（HDF5和JSON） |
| `logs` | list | 执行日志列表（LogEntry对象） |
| `error` | string | 错误信息（仅当FAILED时） |
| `metrics` | dict | 性能指标（duration, file_size_mb） |

## 设计原理

### 工作流程

```
1. 数据源加载
   ├── 根据source.type选择加载器
   │   ├── emt_result: 从CloudPSS加载EMT结果
   │   ├── powerflow_result: 加载潮流结果
   │   ├── vsi_result: 加载VSI结果
   │   ├── disturbance_result: 加载扰动严重度结果
   │   └── file: 从JSON文件加载
   └── 解析为标准格式

2. 数据转换
   └── 转换为NumPy数组
   └── 组织为分层结构

3. 元数据添加
   ├── 标准属性（created, version, source_type）
   ├── 用户元数据（title, description, tags）
   └── 自定义属性

4. 压缩存储
   ├── 根据compression选择算法
   │   ├── gzip: 通用压缩
   │   ├── lzf: 快速压缩
   │   └── none: 无压缩
   └── 按chunk_size分块存储

5. 索引生成
   └── 遍历HDF5结构
   └── 生成JSON索引文件

6. 输出文件
   └── *.h5 - 主数据文件
   └── *.json - 索引文件
```

## 与其他技能的关联

```
EMT仿真/潮流计算/VSI分析/扰动严重度分析
    ↓ (结果数据)
hdf5_export
    ↓ (标准化存储)
HDF5文件 + JSON索引
    ↓ (后续分析)
    ├── Python (h5py/pandas)
    ├── MATLAB (h5read)
    └── Julia (HDF5.jl)
```

**输入依赖**: 支持多种技能产生的结果数据或JSON文件
**输出被依赖**: HDF5文件可被各种科学计算工具读取

## 性能特点

- **执行时间**: 取决于数据量和压缩级别，通常10-30秒
- **压缩比**: gzip(4)约50-70%，gzip(9)约60-80%
- **读写速度**: 约50-100MB/s（取决于压缩级别）
- **适用规模**: 已测试至导出1GB原始数据
- **内存占用**: 与数据量和分块大小成正比

### 压缩选项对比

| 算法 | 压缩比 | 速度 | 适用场景 |
|------|--------|------|----------|
| gzip(4) | 中 | 中 | 通用场景，推荐 |
| gzip(9) | 高 | 慢 | 存储空间优先 |
| lzf | 低 | 快 | 速度优先 |
| none | 无 | 最快 | 不需要压缩 |

## 常见问题

### 问题1: 压缩失败

**原因**: 未安装支持的压缩库

**解决**:
```bash
pip install python-lzf  # 如果需要lzf压缩
```

### 问题2: 文件读取失败

**原因**: HDF5文件损坏或格式不兼容

**解决**:
```python
import h5py

# 检查文件完整性
try:
    with h5py.File("data.h5", "r") as f:
        print("文件有效")
        print(f"根组属性: {dict(f.attrs)}")
except Exception as e:
    print(f"文件损坏: {e}")
```

### 问题3: 内存不足

**原因**: 大数据集一次性加载

**解决**:
```python
# 使用分块读取
skill = get_skill("hdf5_export")

# 只读取特定数据集
waveform = skill.read_hdf5("./results/data.h5", "waveforms/Bus_16_V")

# 或使用h5py直接分块读取
import h5py
with h5py.File("data.h5", "r") as f:
    dataset = f["waveforms/Bus_16_V"]
    for chunk in dataset.iter_chunks():
        data_chunk = dataset[chunk]
        # 处理数据块
```

### 问题4: 中文字符问题

**原因**: HDF5属性中存储中文字符

**解决**: HDF5本身支持UTF-8，确保使用最新版本的h5py库：
```bash
pip install --upgrade h5py
```

### 问题5: 与其他工具兼容性

**原因**: 不同工具的HDF5库版本差异

**解决**: 使用标准的HDF5结构，避免特殊属性：
```python
# 导出时设置兼容性选项
config["options"]["compatibility"] = "standard"
```

## 完整示例

### 场景描述

某研究团队需要归档IEEE39系统不同季节的N-1分析结果，用于后续机器学习模型训练。

### 配置文件

```yaml
skill: hdf5_export
source:
  type: file
  file_path: ./results/ieee39_n1_summer_result.json

output:
  path: ./archive/
  filename: ieee39_n1_summer.h5
  compression: gzip
  compression_level: 6

metadata:
  title: "IEEE39系统N-1分析-夏季场景"
  description: "夏季峰值负荷下的N-1故障扫描结果，包含39条母线电压数据"
  tags:
    - "IEEE39"
    - "N-1"
    - "summer_peak"
    - "voltage_stability"
  custom_attrs:
    project: "ML_PowerSystem_2024"
    scenario: "summer_peak"
    engineer: "researcher_chen"
    date_created: "2024-03-24"

options:
  include_waveforms: true
  include_metrics: true
  chunk_size: 5000
```

### 执行命令

```bash
python -m cloudpss_skills run --config hdf5_config.yaml
```

### 预期输出

```
[INFO] HDF5导出开始，源类型: file
[INFO] HDF5导出完成，文件: ./archive/ieee39_n1_summer.h5
```

### 结果文件

**HDF5文件**: `./archive/ieee39_n1_summer.h5`
**索引文件**: `./archive/ieee39_n1_summer.json`

### 后续应用

1. **Python分析**:
```python
import h5py
import pandas as pd

# 读取HDF5
with h5py.File('./archive/ieee39_n1_summer.h5', 'r') as f:
    # 读取元数据
    title = f.attrs['title']
    tags = f.attrs['tags']

    # 读取波形数据
    time = f['waveforms/time'][:]
    bus_16_v = f['waveforms/Bus_16_V'][:]

    # 转换为DataFrame
    df = pd.DataFrame({
        'time': time,
        'Bus_16_V': bus_16_v
    })
```

2. **MATLAB分析**:
```matlab
% 读取HDF5
time = h5read('ieee39_n1_summer.h5', '/waveforms/time');
bus16v = h5read('ieee39_n1_summer.h5', '/waveforms/Bus_16_V');

% 绘图
plot(time, bus16v);
```

3. **批量导出**:
```python
from cloudpss_skills import get_skill

skill = get_skill("hdf5_export")

scenarios = ["spring", "summer", "autumn", "winter"]
for scenario in scenarios:
    config = {
        "source": {
            "type": "file",
            "file_path": f"./results/ieee39_n1_{scenario}_result.json"
        },
        "output": {
            "path": "./archive/",
            "filename": f"ieee39_n1_{scenario}.h5"
        },
        "metadata": {
            "title": f"IEEE39系统N-1分析-{scenario}场景"
        }
    }
    skill.run(config)
```

## 版本信息

- **技能版本**: 1.0.0
- **最后更新**: 2024-03-24
- **SDK要求**: cloudpss >= 4.5.28, h5py >= 3.0.0, numpy >= 1.20.0
