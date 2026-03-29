# HDF5数据导出技能

标准化仿真结果存储格式，支持元数据索引和多种压缩算法。

## 功能特性

- **多种数据源支持**: EMT、PowerFlow、VSI、扰动严重度等结果导出
- **元数据索引**: 完整的数据描述和自定义属性
- **压缩存储**: 支持gzip、lzf压缩算法
- **跨平台兼容**: 与NumPy/Pandas无缝集成
- **JSON索引**: 自动生成数据索引文件

## 适用场景

- 大批量仿真结果归档
- 多场景数据对比分析
- 长期数据存储
- 跨平台数据交换

## 快速开始

### 1. 基本使用

```python
from cloudpss_skills import get_skill

skill = get_skill("hdf5_export")

config = {
    "source": {
        "type": "file",
        "file_path": "./results/result.json"
    },
    "output": {
        "path": "./results/",
        "filename": "result.h5",
        "compression": "gzip",
        "compression_level": 4
    },
    "metadata": {
        "title": "仿真结果",
        "description": "N-1故障分析",
        "tags": ["N-1", "voltage_stability"]
    }
}

result = skill.run(config)
```

### 2. 使用配置文件

```bash
python -m cloudpss_skills run --config config/hdf5_export.yaml
```

### 3. 运行示例

```bash
python examples/analysis/hdf5_export_example.py
```

## 工作流程

```
1. 数据源加载
   └── 从文件或CloudPSS加载结果

2. 数据转换
   └── 转换为HDF5格式
   └── NumPy数组存储

3. 元数据添加
   └── 标题、描述、标签
   └── 自定义属性

4. 压缩存储
   └── gzip/lzf压缩
   └── 分块存储优化

5. 索引生成
   └── 创建JSON索引文件
   └── 记录数据集结构

6. 输出文件
   └── *.h5 - 主数据文件
   └── *.json - 索引文件
```

## 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `source.type` | enum | - | 源类型: emt_result, powerflow_result, vsi_result, disturbance_result, file |
| `source.file_path` | string | - | 源文件路径（file类型） |
| `source.rid` | string | - | CloudPSS结果RID |
| `output.path` | string | ./results/ | 输出目录 |
| `output.filename` | string | - | 输出文件名（可选） |
| `output.compression` | enum | gzip | 压缩算法: gzip, lzf, none |
| `output.compression_level` | int | 4 | 压缩级别（1-9，仅gzip） |
| `metadata.title` | string | - | 数据集标题 |
| `metadata.description` | string | - | 数据集描述 |
| `metadata.tags` | array | - | 标签列表 |
| `metadata.custom_attrs` | object | - | 自定义属性 |
| `options.chunk_size` | int | 1000 | 数据块大小 |

## 数据源类型

### file类型

从JSON文件加载结果数据。

```python
config = {
    "source": {
        "type": "file",
        "file_path": "./results/disturbance_severity_result.json"
    }
}
```

### emt_result类型

从CloudPSS EMT仿真结果导出。

```python
config = {
    "source": {
        "type": "emt_result",
        "rid": "job/emt/abc123"
    }
}
```

### powerflow_result类型

从潮流计算结果导出。

```python
config = {
    "source": {
        "type": "powerflow_result",
        "rid": "job/pf/abc123"
    }
}
```

## 压缩选项

| 算法 | 压缩比 | 速度 | 适用场景 |
|------|--------|------|----------|
| gzip(4) | 中 | 中 | 通用场景，推荐 |
| gzip(9) | 高 | 慢 | 存储空间优先 |
| lzf | 低 | 快 | 速度优先 |
| none | 无 | 最快 | 不需要压缩 |

## 辅助方法

### read_hdf5

读取HDF5文件内容。

```python
# 读取所有数据
data = skill.read_hdf5("./results/result.h5")

# 读取特定数据集
waveform = skill.read_hdf5("./results/result.h5", "waveforms/Bus_16_V")
```

### list_datasets

列出HDF5文件中的所有数据集。

```python
datasets = skill.list_datasets("./results/result.h5")
# ['waveforms/time', 'waveforms/Bus_16_V', 'waveforms/Bus_15_V', ...]
```

## 输出文件

### HDF5文件 (*.h5)

```
/
├── _attrs (根属性)
│   ├── created: "2026-03-29T10:30:00"
│   ├── version: "1.0"
│   ├── source_type: "emt"
│   ├── title: "仿真结果"
│   └── tags: "N-1,voltage_stability"
├── waveforms (波形数据组)
│   ├── time (数据集)
│   ├── Bus_16_V (数据集)
│   └── Bus_15_V (数据集)
└── metadata (元数据组)
    └── (属性)
```

### 索引文件 (*.json)

```json
{
  "hdf5_file": "result.h5",
  "created": "2026-03-29T10:30:00",
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
    "title": "仿真结果",
    "description": "N-1故障分析",
    "tags": ["N-1", "voltage_stability"]
  }
}
```

## 与已有技能的关联

```
EMT仿真/潮流计算/其他技能
    ↓ (结果数据)
hdf5_export
    ↓ (标准化存储)
HDF5文件 + JSON索引
    ↓ (后续分析)
Python/MATLAB/其他工具
```

## 使用建议

### 1. 选择合适的压缩算法

```python
# 通用场景（推荐）
"compression": "gzip",
"compression_level": 4

# 存储空间受限
"compression": "gzip",
"compression_level": 9

# 速度优先
"compression": "lzf"
```

### 2. 添加完整元数据

```python
"metadata": {
    "title": "IEEE39系统N-1分析",
    "description": "夏季峰值负荷场景",
    "tags": ["IEEE39", "N-1", "summer_peak"],
    "custom_attrs": {
        "project": "TSQH_2026",
        "scenario": "summer_peak",
        "engineer": "chenying"
    }
}
```

### 3. 批量导出

```python
# 导出多个结果文件
result_files = ["result1.json", "result2.json", "result3.json"]

for rf in result_files:
    config["source"]["file_path"] = rf
    config["output"]["filename"] = rf.replace(".json", ".h5")
    skill.run(config)
```

## 故障排查

### 问题1: 压缩失败

**原因**: 未安装支持的压缩库
**解决**: 安装lzf: `pip install python-lzf`

### 问题2: 文件读取失败

**原因**: HDF5文件损坏
**解决**: 检查文件完整性，尝试h5py.File检查

### 问题3: 内存不足

**原因**: 大数据集一次性加载
**解决**: 使用分块读取：`skill.read_hdf5(path, dataset)`

## 与其他工具的集成

### Python

```python
import h5py

with h5py.File("result.h5", "r") as f:
    data = f["waveforms/Bus_16_V"][:]
```

### MATLAB

```matlab
data = h5read('result.h5', '/waveforms/Bus_16_V');
```

### Julia

```julia
using HDF5

data = h5read("result.h5", "waveforms/Bus_16_V")
```

## 版本历史

- **v1.0**: 基础HDF5导出功能
  - 支持多种数据源
  - gzip/lzf压缩
  - 元数据和索引
