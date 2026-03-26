# EMTResult API 参考

**文件位置**: `cloudpss/job/result/EMTResult.py`

**继承关系**: `EMTResult` 继承自 `Result`，专用于电磁暂态（EMT）仿真结果处理。

**研究工作流定位**:
- `EMTResult` 在普通离线研究里主要承担“提取波形、读取原始消息、准备后处理数据”的角色
- `getPlots()` / `getPlot()` / `getPlotChannelNames()` / `getPlotChannelData()` 是最核心的离线分析入口
- `getMessagesByKey()` 适合保留原始 plot 分段消息或辅助排错
- 实时控制相关方法当前应视为扩展能力，而不是普通云仿真的主线能力

---

## 构造函数

### `__init__(job, receiver, sender=None)`

初始化 EMTResult 实例。

**参数**:
- `job`: Job, 必需。关联的 Job 实例。
- `receiver`: MessageStreamReceiver, 必需。消息接收器。
- `sender`: 可选。消息发送器（用于实时控制）。

**说明**: 通常不直接构造，通过 `job.result` 获取。

---

## 波形数据获取方法

### `result.getPlots()`

获取所有波形分组数据。

这是 EMT 离线分析里最常用的入口，适合先确认当前算例是否真的产出了可分析的波形。

**返回**:
- 可迭代对象：SDK 4.5.28 实际返回 `dict_values`，通常应先转成 `list(...)`
- 每个元素是一个波形分组字典，包含：
  - `key`: 波形分组键，例如 `plot-0`
  - `name`: 波形名称（可选，live 返回里不一定存在）
  - `data`: 波形数据
    - `traces`: 曲线列表，每条曲线包含 `name`, `x`, `y` 数组

**示例**:
```python
# 获取所有波形
plots = list(result.getPlots())
print(f"波形分组数量：{len(plots)}")

# 遍历所有波形
for i, plot in enumerate(plots):
    label = plot.get('key') or plot.get('name') or f'Plot {i}'
    print(f"\n波形 [{i}]: {label}")

    # 获取曲线数量
    traces = plot.get('data', {}).get('traces', [])
    print(f"  曲线数量：{len(traces)}")

    # 显示曲线名称
    for trace in traces:
        print(f"    - {trace['name']}: {len(trace['x'])} 个点")
```

**相关方法**:
- `result.getPlot(index)` - 获取单个波形
- `result.getPlotChannelNames(index)` - 获取通道名称

---

### `result.getPlot(index: int)`

获取指定索引的波形分组。

适合在多组示波器输出中定位某一个目标分组，再继续读取通道。

**参数**:
- `index`: int, 必需。波形位置索引（从 0 开始）。

**返回**:
- dict: 波形分组数据，包含：
  - `key`: 波形分组键
  - `name`: 波形名称（可选）
  - `data`: 波形数据
    - `traces`: 曲线列表

**示例**:
```python
# 获取第一个波形
plot = result.getPlot(0)

if plot:
    print(f"波形分组键：{plot.get('key')}")
    print(f"波形显示名：{plot.get('name', 'N/A')}")

    # 获取曲线
    traces = plot['data']['traces']
    for trace in traces:
        print(f"  曲线：{trace['name']}")
        print(f"    X 范围：[{trace['x'][0]:.6f}, {trace['x'][-1]:.6f}]")
        print(f"    Y 范围：[{min(trace['y']):.4f}, {max(trace['y']):.4f}]")
```

**异常**:
- 索引超出范围时返回 None。

**当前 live 边界**:
- `plot.get('key')` 比 `plot.get('name')` 更稳定
- 对普通云 EMT 仿真，脚本中更稳妥的分组标识方式是优先使用 `key`，再把 `name` 当作可选展示字段

---

### `result.getPlotChannelNames(index: int)`

获取指定波形分组的所有通道名称。

适合先确认某个分组里有哪些电压、电流、转速或功角通道，再决定后续分析对象。

**参数**:
- `index`: int, 必需。波形位置索引。

**返回**:
- list[str] | None: 通道名称列表；索引不存在时返回 `None`。

**示例**:
```python
# 获取第一个波形的所有通道
names = result.getPlotChannelNames(0)

if names:
    print("通道列表:")
    for i, name in enumerate(names):
        print(f"  [{i}] {name}")
```

**相关方法**:
- `result.getPlotChannelData(index, channelName)` - 获取通道数据

---

### `result.getPlotChannelData(index: int, channelName: str)`

获取指定通道的波形数据。

这是后处理最直接的入口，通常会被用于导出 CSV、绘图或计算稳定性指标。

**参数**:
- `index`: int, 必需。波形位置索引。
- `channelName`: str, 必需。通道名称。

**返回**:
- dict: 通道数据（trace 对象），包含：
  - `name`: 通道名称
  - `x`: 自变量数组（通常是时间）
  - `y`: 因变量数组（仿真值）

**当前 SDK 边界行为**:
- 如果 `index` 无效，返回 `None`
- 如果 `channelName` 不存在，SDK 4.5.28 不会抛错，而是会回落到该 plot 中最后一条 trace
- 因此更稳妥的做法是先调用 `getPlotChannelNames(index)`，再从返回值中选择合法通道名

**示例**:
```python
# 获取通道数据
data = result.getPlotChannelData(0, 'Ia (pu)')

if data:
    # 访问数据
    time_array = data['x']
    value_array = data['y']

    print(f"数据点数：{len(time_array)}")
    print(f"时间范围：[{time_array[0]:.6f}, {time_array[-1]:.6f}] 秒")
    print(f"值范围：[{min(value_array):.4f}, {max(value_array):.4f}]")

    # 导出前 10 个点
    print("\n前 10 个数据点:")
    for i in range(min(10, len(time_array))):
        print(f"  t={time_array[i]:.6f}s, y={value_array[i]:.4f}")
```

**数据处理示例**:
```python
# 导出到 CSV
import csv

data = result.getPlotChannelData(0, 'Ia (pu)')
with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['time', 'Ia'])
    for i in range(len(data['x'])):
        writer.writerow([data['x'][i], data['y'][i]])

# 使用 matplotlib 绘图
import matplotlib.pyplot as plt

data = result.getPlotChannelData(0, 'Ia (pu)')
plt.plot(data['x'], data['y'])
plt.xlabel('Time (s)')
plt.ylabel('Ia (pu)')
plt.title('Current Waveform')
plt.grid(True)
plt.savefig('waveform.png')
```

---

### `result.getMessagesByKey(key: str)`

按消息 `key` 过滤当前结果缓存中的消息。

**参数**:
- `key`: str, 必需。要筛选的消息键。

**返回**:
- `list[dict]`: 所有匹配该 `key` 的消息，保持原始顺序。

**示例**:
```python
# 获取某个原始 plot 分组的消息片段
raw_plot0 = result.getMessagesByKey('plot-0')
print(len(raw_plot0))

# 也可以查日志消息
hidden_logs = result.getMessagesByKey('emtLab-log-hidden')
```

**说明**:
- 该方法来自 `Result` 基类，`EMTResult` 直接继承可用。
- 返回的是接收器缓存中的原始消息，不会做二次解析。
- 当前普通云 EMT 仿真中，已验证常见 key 包括 `plot-0` 到 `plot-n` 这类波形分组 key；日志类 key 是否存在取决于具体算例和运行过程。

---

## 仿真控制方法（实时仿真）

以下方法用于实时仿真控制，需要 `sender` 不为 None。

**当前阶段说明**:
- 这些接口已经做了本地边界验证
- 但当前仓库不把它们作为普通云仿真的主线能力
- 如果缺少实时交互环境或专门设备，不建议把它们作为近期研究流程的依赖

建议把这一组接口视为“延后能力”：
- 当前主线先完成波形提取、原始消息排查和后处理
- 只有在确实具备实时交互条件时，再进入 `next()` / `goto()` / `control()` 等接口

### `result.next()`

向前推进一个时步。

**异常**:
- `Exception`: 当 sender 为 None 时抛出。

**示例**:
```python
# 单步仿真
result.next()

# 多步仿真
for i in range(10):
    result.next()
    # 获取当前数据
    plots = result.getPlots()
```

---

### `result.goto(step)`

推进到指定时步。

**参数**:
- `step`: int, 必需。目标时步。

**异常**:
- `Exception`: 当 sender 为 None 时抛出。

**示例**:
```python
# 跳到第 100 步
result.goto(100)

# 跳到特定时间（需要转换为时步）
target_time = 0.01  # 10ms
step = int(target_time / simulation_step_size)
result.goto(step)
```

---

### `result.send(message=None)`

发送虚拟输入消息。

**参数**:
- `message`: dict | VirtualInput, 可选。消息内容。

**示例**:
```python
# 发送虚拟输入
result.send({
    'type': 'virtual_input',
    'data': {
        'key1': 'value1',
        'key2': 'value2'
    }
})

# 使用 VirtualInput
from cloudpss.model.model import VirtualInput
vi = VirtualInput(param1='value1', param2='value2')
result.send(vi)
```

---

### `result.writeShm(path, buffer, offset)`

写入共享内存接口。

**参数**:
- `path`: str, 必需。内存路径。
- `buffer`: 必需。数据缓冲区。
- `offset`: int, 必需。偏移量。

**注意**: 此接口未最终确定，后续版本可能修改。

---

### `result.control(controlParam, eventTime='-1', eventTimeType='1')`

控制仿真参数。

**参数**:
- `controlParam`: dict | list, 必需。控制参数。
- `eventTime`: str, 可选。事件时间，默认 '-1'。
- `eventTimeType`: str, 可选。事件时间类型，默认 '1'。

**示例**:
```python
# 单个控制
param = {
    'key': 'R1',
    'value': 100,
    'uuid': 'unique-id-123',
    'log': '电阻值变化到 100 欧姆'
}
result.control(param)

# 多个控制
params = [
    {'key': 'R1', 'value': 100},
    {'key': 'C1', 'value': 0.001}
]
result.control(params)
```

---

### `result.monitor(monitorParam, eventTime='-1', eventTimeType='1')`

设置仿真监控条件。

**参数**:
- `monitorParam`: dict | list, 必需。监控参数。
- `eventTime`: str, 可选。事件时间。
- `eventTimeType`: str, 可选。事件时间类型。

**示例**:
```python
# 设置监控
param = {
    'key': 'V1',
    'function': 'over',
    'value': 1.1,
    'period': 0.01,
    'freq': 50,
    'condition': 'gt',
    'cycle': 1,
    'nCount': 3
}
result.monitor(param)
```

---

### `result.stopSimulation()`

停止仿真。

**示例**:
```python
# 满足条件时停止
if some_condition:
    result.stopSimulation()
    print("仿真已停止")
```

---

### `result.saveSnapshot(number)`

保存仿真断面。

**参数**:
- `number`: int, 必需。断面编号。

**示例**:
```python
# 保存当前断面
result.saveSnapshot(1)

# 保存多个断面
for i in range(10):
    result.saveSnapshot(i)
    result.next()  # 前进一步
```

---

### `result.loadSnapshot(number)`

加载仿真断面。

**参数**:
- `number`: int, 必需。断面编号。

**示例**:
```python
# 加载之前保存的断面
result.loadSnapshot(1)

# 从断面继续仿真
result.next()
```

---

## 内部缓存说明

SDK 当前实现里，`EMTResult` 内部会维护一个按 plot key 聚合后的缓存字典，但仓库当前不把这个内部字段当作主线公开入口。

对普通云 EMT 研究脚本，更稳妥的读取方式仍然是：

- `list(result.getPlots())`
- `result.getPlot(index)`
- `result.getPlotChannelNames(index)`
- `result.getPlotChannelData(index, channelName)`
- `result.getMessagesByKey(key)`

---

## 完整示例

### 示例 1: 基本数据处理

```python
import os
import time

from cloudpss import Model

# 运行仿真
model = Model.fetch(os.environ.get("TEST_MODEL_RID", "model/holdme/IEEE39"))
job = model.runEMT()

# 等待完成
while job.status() == 0:
    time.sleep(3)

# 获取结果
result = job.result

# 获取所有波形
plots = list(result.getPlots())
print(f"共 {len(plots)} 个波形分组")

# 处理第一个波形
plot = result.getPlot(0)
names = result.getPlotChannelNames(0)

label = plot.get('key') or plot.get('name') or 'plot-0'
print(f"\n波形 '{label}' 包含:")
for name in names:
    data = result.getPlotChannelData(0, name)
    print(f"  {name}: {len(data['x'])} 点")
```

### 示例 2: 数据导出

```python
import csv
import json

# 获取所有波形数据
plots = list(result.getPlots())

# 导出为 CSV
for i, plot in enumerate(plots):
    names = result.getPlotChannelNames(i)

    for name in names:
        data = result.getPlotChannelData(i, name)

        filename = f"plot_{i}_{name.replace('/', '_')}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['time', name])
            for j in range(len(data['x'])):
                writer.writerow([data['x'][j], data['y'][j]])
        print(f"已导出：{filename}")

# 导出为 JSON
all_data = {}
for i, plot in enumerate(plots):
    all_data[f'plot_{i}'] = {
        'key': plot.get('key'),
        'key': plot.get('key'),
        'name': plot.get('name'),
        'channels': {}
    }
    names = result.getPlotChannelNames(i)
    for name in names:
        data = result.getPlotChannelData(i, name)
        all_data[f'plot_{i}']['channels'][name] = {
            'x': data['x'],
            'y': data['y']
        }

with open('all_data.json', 'w') as f:
    json.dump(all_data, f, indent=2)
```

### 示例 3: 延后能力示意

```python
# 需要支持实时控制的仿真环境
# 普通云仿真和离线研究流程通常不以这一段为主线
job = model.runEMT()
result = job.result

# 单步仿真
for i in range(100):
    result.next()

    # 获取当前数据
    data = result.getPlotChannelData(0, 'Ia')
    current_value = data['y'][-1]

    # 根据当前值调整参数
    if current_value > 1.5:
        result.control({'key': 'R1', 'value': 200})
        print(f"步骤 {i}: 电流过大，增加电阻")

# 保存断面
result.saveSnapshot(100)

# 停止仿真
result.stopSimulation()
```

### 示例 4: 可视化

```python
import matplotlib.pyplot as plt

# 获取数据
result = job.result

# 创建图表
fig, axes = plt.subplots(2, 1, figsize=(10, 8))

# 绘制第一个波形的所有通道
names = result.getPlotChannelNames(0)
for name in names:
    data = result.getPlotChannelData(0, name)
    axes[0].plot(data['x'], data['y'], label=name)

axes[0].set_xlabel('Time (s)')
axes[0].set_ylabel('Values')
axes[0].set_title('Plot 0')
axes[0].legend()
axes[0].grid(True)

# 绘制特定通道
data = result.getPlotChannelData(0, 'Ia (pu)')
axes[1].plot(data['x'], data['y'], 'r-', linewidth=2)
axes[1].set_xlabel('Time (s)')
axes[1].set_ylabel('Ia (pu)')
axes[1].set_title('Current Ia')
axes[1].grid(True)

plt.tight_layout()
plt.savefig('waveforms.png', dpi=150)
plt.show()
```

---

## 版本信息

**SDK 版本**: 4.5.28+

**相关文档**:
- [Model API 参考](./model-api.md)
- [Job API 参考](./job-api.md)
- [PowerFlowResult API 参考](./powerflow-result-api.md)
- `IESResult` 当前未单列 API 参考；IES 相关入口仅在 [Job API 参考](./job-api.md) 中做非主线说明
