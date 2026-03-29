# 对比可视化技能 (Compare Visualization)

## 设计背景

### 研究对象

在电力系统分析中，经常需要对比多个场景、不同参数配置或不同时间点的仿真结果。传统的文本对比报告虽然提供了详细数据，但缺乏直观的可视化展示。对比可视化技能通过生成多种类型的对比图表（时序对比图、指标柱状图、热力图、雷达图等），帮助工程师更直观地理解不同场景间的差异和规律。

### 实际需求

工程师在以下场景需要进行结果对比可视化：

1. **故障场景对比**: 对比基态、故障态、延迟切除等不同工况的波形差异
2. **参数扫描分析**: 可视化不同参数值下的系统响应变化趋势
3. **N-1安全分析**: 对比各支路停运后的关键指标差异
4. **多方案评估**: 直观展示不同规划方案的优劣
5. **时序演进分析**: 展示系统在不同时段的运行特征变化

### 期望的输入和输出

**输入**:

- 多个仿真任务的Job ID列表（至少2个）
- 对比通道列表（可选，默认全部）
- 对比指标（max/min/mean/rms/peak）
- 图表类型配置（时序图/柱状图/热力图/雷达图）
- 时间范围切片（可选）
- 输出格式和样式配置

**输出**:

- 多场景时序对比图（PNG/PDF/SVG）
- 指标对比柱状图（按指标或按场景分组）
- 通道-场景热力图（展示数值分布）
- 多维度雷达图（综合评估）
- 图表元数据（通道数、场景数、生成文件列表）

### 计算结果的用途和价值

对比可视化结果可直接用于：

- **汇报展示**: 生成可直接插入PPT/报告的专业图表
- **差异识别**: 快速识别关键通道和关键场景的差异
- **趋势分析**: 直观展示参数变化对系统的影响趋势
- **决策支持**: 为方案选择提供直观的可视化依据
- **文档归档**: 作为研究过程的可视化记录

## 功能特性

- **多场景对比**: 支持2个及以上场景的对比分析
- **多样化图表**:
  - 时序对比图：多线叠加展示波形差异
  - 指标柱状图：分组对比关键指标
  - 热力图：矩阵形式展示数值分布
  - 雷达图：多维度综合评估
- **灵活配置**: 支持自定义通道、指标、时间范围
- **专业输出**: 高分辨率图表，支持PNG/PDF/SVG格式
- **智能分组**: 支持按通道或按场景分组展示

## 快速开始

### CLI方式（推荐）

```bash
# 基础对比（时序图+柱状图）
python -m cloudpss_skills run --config config_compare_viz.yaml
```

### 配置示例

```yaml
skill: compare_visualization
auth:
  token_file: .cloudpss_token
sources:
  - job_id: "job-abc123-xxx"
    label: "基态"
    color: "#1f77b4"
  - job_id: "job-def456-yyy"
    label: "故障态"
    color: "#ff7f0e"
  - job_id: "job-ghi789-zzz"
    label: "延迟切除"
    color: "#2ca02c"
compare:
  channels: ["Bus1_V", "Bus2_V", "Gen1_P"]
  metrics: ["max", "min", "mean"]
  time_range:
    start: 0.0
    end: 5.0
charts:
  time_series:
    enabled: true
    per_channel: false
    title: "故障场景电压对比"
  bar_chart:
    enabled: true
    group_by: "metric"
    title: "电压指标对比"
  heatmap:
    enabled: true
    metric: "max"
    title: "场景-通道热力图"
  radar:
    enabled: true
    title: "综合评估雷达图"
output:
  format: png
  path: ./results/
  filename_prefix: fault_compare
  dpi: 150
  width: 14
  height: 8
```

## 配置参数详解

### sources（数据源）

要对比的仿真任务列表，每个任务包含：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `job_id` | string | ✅ | CloudPSS仿真任务ID |
| `label` | string | ❌ | 场景标签（默认: 场景N） |
| `color` | string | ❌ | 线条颜色（HEX格式，如"#1f77b4"） |

### compare（对比配置）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `channels` | list | ❌ | [] | 要对比的通道列表，空数组表示全部 |
| `metrics` | list | ❌ | ["max","min","mean"] | 计算指标：max/min/mean/rms/peak |
| `time_range` | object | ❌ | {} | 时间范围筛选 |
| `time_range.start` | number | ❌ | - | 开始时间（秒） |
| `time_range.end` | number | ❌ | - | 结束时间（秒） |

### charts（图表配置）

#### 时序对比图 (time_series)

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `enabled` | boolean | ❌ | true | 是否启用 |
| `per_channel` | boolean | ❌ | false | true=每个通道单独一张图 |
| `title` | string | ❌ | "多场景时序对比" | 图表标题 |

#### 指标柱状图 (bar_chart)

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `enabled` | boolean | ❌ | true | 是否启用 |
| `group_by` | string | ❌ | "metric" | "metric"按指标分组/"source"按场景分组 |
| `title` | string | ❌ | "指标对比" | 图表标题 |

#### 热力图 (heatmap)

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `enabled` | boolean | ❌ | false | 是否启用 |
| `metric` | string | ❌ | "max" | 热力图显示的指标 |
| `title` | string | ❌ | "通道-场景热力图" | 图表标题 |

#### 雷达图 (radar)

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `enabled` | boolean | ❌ | false | 是否启用 |
| `title` | string | ❌ | "多维度雷达图" | 图表标题 |

### output（输出配置）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `format` | string | ❌ | "png" | 输出格式：png/pdf/svg |
| `path` | string | ❌ | "./results/" | 输出目录 |
| `filename_prefix` | string | ❌ | "compare" | 文件名前缀 |
| `dpi` | integer | ❌ | 150 | 图像分辨率 |
| `width` | number | ❌ | 14 | 图像宽度（英寸） |
| `height` | number | ❌ | 8 | 图像高度（英寸） |

## 配置示例

### 示例1：故障场景对比

```yaml
skill: compare_visualization
auth:
  token_file: .cloudpss_token
sources:
  - job_id: "job-abc123"
    label: "基态"
    color: "#2E86AB"
  - job_id: "job-def456"
    label: "三相故障"
    color: "#A23B72"
  - job_id: "job-ghi789"
    label: "单相故障"
    color: "#F18F01"
compare:
  channels: ["Bus7_V", "Bus8_V", "Bus2_V"]
  metrics: ["max", "min", "mean"]
  time_range:
    start: 0.0
    end: 3.0
charts:
  time_series:
    enabled: true
    per_channel: false
  bar_chart:
    enabled: true
    group_by: "metric"
  heatmap:
    enabled: true
    metric: "min"
output:
  format: png
  path: ./results/
  filename_prefix: fault_comparison
  dpi: 150
```

### 示例2：参数扫描结果可视化

```yaml
skill: compare_visualization
sources:
  - job_id: "job-scan-001"
    label: "负荷80%"
  - job_id: "job-scan-002"
    label: "负荷90%"
  - job_id: "job-scan-003"
    label: "负荷100%"
  - job_id: "job-scan-004"
    label: "负荷110%"
  - job_id: "job-scan-005"
    label: "负荷120%"
compare:
  channels: ["Bus30_V", "Bus38_V"]
  metrics: ["mean", "rms"]
charts:
  time_series:
    enabled: true
  bar_chart:
    enabled: true
    group_by: "source"
  radar:
    enabled: true
output:
  format: pdf
  filename_prefix: load_scan
  width: 16
  height: 10
```

### 示例3：N-1结果对比

```yaml
skill: compare_visualization
sources:
  - job_id: "job-n1-base"
    label: "基态"
    color: "#1a1a2e"
  - job_id: "job-n1-line26"
    label: "Line26-28断开"
    color: "#e94560"
  - job_id: "job-n1-line28"
    label: "Line28-29断开"
    color: "#533483"
compare:
  channels: ["Bus26_V", "Bus28_V", "Bus29_V", "Bus38_V"]
  metrics: ["max", "min"]
charts:
  time_series:
    enabled: false
  bar_chart:
    enabled: true
    group_by: "metric"
  heatmap:
    enabled: true
    metric: "min"
output:
  format: svg
  filename_prefix: n1_comparison
  dpi: 200
```

## 输出结果说明

### 输出文件

技能会生成以下类型的图表文件：

| 文件名模式 | 说明 |
|-----------|------|
| `{prefix}_timeseries.{fmt}` | 时序对比图（多通道subplot） |
| `{prefix}_timeseries_{channel}.{fmt}` | 单通道时序图（per_channel=true时） |
| `{prefix}_bar_{metric}.{fmt}` | 指标柱状图（group_by=metric时） |
| `{prefix}_bar_{source}.{fmt}` | 场景柱状图（group_by=source时） |
| `{prefix}_heatmap.{fmt}` | 通道-场景热力图 |
| `{prefix}_radar.{fmt}` | 多维度雷达图 |

### SkillResult结构

```json
{
  "skill_name": "compare_visualization",
  "status": "SUCCESS",
  "data": {
    "sources": 3,
    "channels": 5,
    "charts_generated": 4,
    "output_path": "./results/"
  },
  "artifacts": [
    {
      "type": "png",
      "path": "./results/fault_comparison_timeseries.png",
      "size": 245678,
      "description": "对比图表: fault_comparison_timeseries.png"
    }
  ]
}
```

## 设计原理

### 工作流程

```
1. 加载认证 → 设置CloudPSS Token
2. 获取任务 → 逐一拉取各Job的结果
3. 数据提取 → 提取指定通道的时序数据和指标
4. 时间筛选 → 应用时间范围过滤
5. 图表生成 → 根据配置生成多种图表
6. 文件导出 → 保存为高分辨率图像
```

### 指标计算

- **max**: 最大值 `np.max(arr)`
- **min**: 最小值 `np.min(arr)`
- **mean**: 平均值 `np.mean(arr)`
- **rms**: 有效值 `sqrt(np.mean(arr^2))`
- **peak**: 峰值 `np.max(np.abs(arr))`

### 图表设计

- **时序图**: 多线叠加，不同颜色区分场景，网格辅助读数
- **柱状图**: 分组柱状，误差线展示范围，自动旋转标签
- **热力图**: 红黄色谱，数值标注，颜色条指示量级
- **雷达图**: 归一化处理，填充区域，多边形对比

## 使用场景

### 场景1：故障严重程度对比

对比基态、三相短路、单相短路三种工况的电压跌落深度。

```yaml
sources:
  - {job_id: "base", label: "基态"}
  - {job_id: "3ph", label: "三相故障"}
  - {job_id: "1ph", label: "单相故障"}
compare:
  channels: ["Bus_V"]
  metrics: ["min"]
charts:
  time_series: {enabled: true}
  bar_chart: {enabled: true}
```

### 场景2：参数灵敏度分析

可视化不同负荷水平下的系统响应。

```yaml
sources:
  - {job_id: "load80", label: "80%"}
  - {job_id: "load100", label: "100%"}
  - {job_id: "load120", label: "120%"}
charts:
  heatmap: {enabled: true, metric: "mean"}
  radar: {enabled: true}
```

### 场景3：N-1薄弱环节识别

对比各支路停运后的关键母线电压。

```yaml
sources:
  - {job_id: "base", label: "基态"}
  - {job_id: "n1-1", label: "Line1断开"}
  - {job_id: "n1-2", label: "Line2断开"}
  # ...
compare:
  channels: ["Bus30_V", "Bus38_V"]
charts:
  bar_chart: {enabled: true, group_by: "source"}
  heatmap: {enabled: true, metric: "min"}
```

## 注意事项

1. **数据源要求**: 所有Job必须是EMT仿真结果（有时序数据）
2. **通道匹配**: 不同任务的通道名称需一致才能对比
3. **颜色配置**: 建议为每个场景指定颜色，避免自动分配
4. **图表数量**: 大量通道会生成大量图表，注意per_channel设置
5. **内存限制**: 大量数据点可能导致内存占用高，建议设置time_range

## 故障排除

### 问题1："成功获取的任务数不足2个"

**原因**: 部分Job ID无效或结果为空
**解决**: 检查Job ID是否正确，确认任务已完成

### 问题2：图表中的线条颜色相同

**原因**: 未指定color或matplotlib默认循环
**解决**: 在sources中为每个场景指定color参数

### 问题3：热力图显示异常

**原因**: 通道或场景数量过多/过少
**解决**: 确保至少有2个通道和2个场景

### 问题4：生成的图片模糊

**原因**: DPI设置过低
**解决**: 提高output.dpi至200或300

## 相关技能

- **result_compare**: 生成文本格式的对比报告
- **visualize**: 单场景波形可视化
- **emt_simulation**: 运行EMT仿真获取对比数据源
- **param_scan**: 参数扫描生成多场景数据

## 完整示例

### 场景描述

对IEEE3系统进行故障对比分析：比较基态运行、三相短路故障、延迟切除故障三种工况下的电压响应特性。

### 配置文件

```yaml
skill: compare_visualization
auth:
  token_file: .cloudpss_token
sources:
  - job_id: "job-20240315-001"
    label: "基态运行"
    color: "#2E86AB"
  - job_id: "job-20240315-002"
    label: "三相短路"
    color: "#A23B72"
  - job_id: "job-20240315-003"
    label: "延迟切除"
    color: "#F18F01"
compare:
  channels: ["Bus7_V", "Bus8_V", "Bus2_V"]
  metrics: ["max", "min", "mean"]
  time_range:
    start: 0.0
    end: 3.0
charts:
  time_series:
    enabled: true
    per_channel: false
    title: "故障场景电压对比"
  bar_chart:
    enabled: true
    group_by: "metric"
    title: "电压指标对比"
  heatmap:
    enabled: true
    metric: "min"
    title: "电压跌落热力图"
  radar:
    enabled: true
    title: "综合响应评估"
output:
  format: png
  path: ./results/
  filename_prefix: ieee3_fault_compare
  dpi: 150
  width: 14
  height: 8
```

### 执行命令

```bash
python -m cloudpss_skills run --config config_compare_viz.yaml
```

### 预期输出

```
[INFO] 加载认证信息...
[INFO] 认证成功
[INFO] 对比 3 个仿真结果
[INFO] 获取任务: 基态运行 (job-20240315-001)
[INFO]   -> 获取 3 个通道
[INFO] 获取任务: 三相短路 (job-20240315-002)
[INFO]   -> 获取 3 个通道
[INFO] 获取任务: 延迟切除 (job-20240315-003)
[INFO]   -> 获取 3 个通道
[INFO] 生成时序对比图...
[INFO]   -> 时序对比图已保存: ieee3_fault_compare_timeseries.png
[INFO] 生成指标对比柱状图...
[INFO]   -> max指标柱状图已保存: ieee3_fault_compare_bar_max.png
[INFO]   -> min指标柱状图已保存: ieee3_fault_compare_bar_min.png
[INFO]   -> mean指标柱状图已保存: ieee3_fault_compare_bar_mean.png
[INFO] 生成热力图...
[INFO]   -> 热力图已保存: ieee3_fault_compare_heatmap.png
[INFO] 生成雷达图...
[INFO]   -> 雷达图已保存: ieee3_fault_compare_radar.png
[INFO] 对比可视化完成，生成 6 张图表
```

### 结果文件

生成以下图表文件：

- `ieee3_fault_compare_timeseries.png` - 三母线电压时序对比
- `ieee3_fault_compare_bar_max.png` - 最大值指标对比
- `ieee3_fault_compare_bar_min.png` - 最小值指标对比（展示电压跌落）
- `ieee3_fault_compare_bar_mean.png` - 平均值指标对比
- `ieee3_fault_compare_heatmap.png` - 场景-通道电压跌落热力图
- `ieee3_fault_compare_radar.png` - 三场景综合评估雷达图

### 后续应用

1. **汇报材料**: 将图表插入技术汇报PPT
2. **分析报告**: 结合result_compare的文本报告撰写完整分析
3. **文档归档**: 作为故障研究过程的可视化记录保存
4. **对比决策**: 基于图表直观对比，选择最优控制策略
