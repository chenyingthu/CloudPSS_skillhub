# EMT 母线电压量测链指南

本指南专门说明如何在当前仓库的主线范围内，为一个 `_newBus_3p` 母线脚本化新增：

1. `_NewVoltageMeter`
2. `_newChannel`
3. meter -> bus `diagram-edge`
4. EMT 输出分组引用

它不是“任意模型通用建模手册”，而是当前已完成 live 验证的一条受约束研究配方。

## 适用前提

当前这条配方只建议在下面这些条件同时满足时使用：

- 目标分析仍然是普通云 EMT 离线仿真
- 目标母线是 `model/CloudPSS/_newBus_3p`
- 你愿意先在本地工作副本上改模，而不是直接改原始云端算例
- 你接受当前 SDK 没有公开 `addEdge()`，因此需要直接注入 `diagram-edge`

当前已完成真实云端验证的样本只有：

- `model/holdme/IEEE3` `Bus7`
- `model/holdme/IEEE3` `Bus2`
- `model/holdme/IEEE39` `bus37`

因此当前最稳妥的说法是：

- 这条配方已经表现出跨母线、跨模型的可迁移性
- 但还不能宣称对所有 EMT 模型和所有母线类型都通用

## 已验证结论

当前仓库已经用真实 CloudPSS API 验证了下面三件事：

1. 仅新增 `_NewVoltageMeter` 和 `_newChannel` 不够  
   缺少 meter -> bus `diagram-edge` 时，真实云端可能返回 `KLU Error: singular`

2. 把 `diagram-edge` 补齐后，新通道会真实进入 EMT 输出  
   新增 `vac_added:*`、`bus2_added:*`、`bus37_added:*` 都已经在真实 EMT 结果中返回

3. 这条链路有一个可复验的正确性判据  
   对新增母线电压通道，可用稳态 RMS 校核：

```text
V_rms ≈ V_pu * VBase / sqrt(3)
```

这个判据已经在：

- `IEEE3 Bus2`
- `IEEE39 bus37`

两条真实云端用例上成立。

## 推荐入口

如果只是想准备本地研究分支，推荐直接运行：

```bash
python examples/basic/emt_voltage_meter_chain_example.py
```

对应脚本：

- `examples/basic/emt_voltage_meter_chain_example.py`

这个脚本做的事情是：

- 加载云端 RID 或本地 YAML
- 先导出本地工作副本
- 找到目标 `_newBus_3p`
- 新增 `_NewVoltageMeter`
- 新增 `_newChannel`
- 注入一条 `diagram-edge`
- 追加 EMT 输出分组
- 保存准备后的本地副本

## 操作步骤

### 1. 选择研究起点

可以从云端模型或已有本地 YAML 起步：

```bash
python examples/basic/emt_voltage_meter_chain_example.py
```

脚本会提示输入：

- 模型 RID 或本地 YAML
- 工作副本路径
- 目标母线 `Name`
- 量测信号名
- 输出通道名
- 采样频率
- 准备后副本保存路径

### 2. 脚本如何选择 edge 路径

脚本内部有两条路径：

#### 路径 A：优先克隆现成模板 edge

如果模型里已经存在可工作的 `_NewVoltageMeter` 和对应 `diagram-edge`，脚本会：

- 复用现有电压表的尺寸
- 克隆现有 edge 的 `attrs`
- 克隆现有 edge 的 `target` 结构
- 只替换新表计的 `source.cell`
- 把 `target.cell` 改为目标母线

这是当前最稳妥的路径。

#### 路径 B：generic edge scaffold

如果模型里根本没有现成电压表模板，脚本会回退到 generic scaffold：

- 仍然新增 `_NewVoltageMeter`
- 仍然新增 `_newChannel`
- 手工构造一个适用于 `_newBus_3p` 的 `diagram-edge`
- 再由真实 EMT 运行结果做校核

这条路径已经在 `IEEE39 bus37` 上通过，但证据还不够多，所以仍然只建议用于当前已知主线。

## 正确性判据

### 判据 1：输出通道是否真的出现

运行 EMT 后，应能在新增分组看到：

- `xxx:0`
- `xxx:1`
- `xxx:2`

例如：

- `vac_added:0/1/2`
- `bus2_added:0/1/2`
- `bus37_added:0/1/2`

如果分组里根本没有这些通道，先不要急着看数值，先回到连接关系检查。

### 判据 2：稳态 RMS 是否合理

对新增母线电压通道，在稳态窗口中计算 RMS，应近似满足：

```text
V_rms ≈ V_pu * VBase / sqrt(3)
```

其中：

- `V_pu` 和 `VBase` 可通过 `fetchTopology("emtp")` 展开后的 `_newBus_3p.args` 获取
- 稳态窗口应避开故障、扰动或 ramping 段

例如：

- `IEEE3 Bus2`
- `IEEE39 bus37`

这两个样本已经用真实云端结果对齐了这个判据。

## 常见失败与排查

### 1. `KLU Error: singular`

优先检查：

- 是否只新增了 `_NewVoltageMeter` / `_newChannel`，但没有注入 `diagram-edge`
- `diagram-edge.source.cell` 是否真的指向新表计
- `diagram-edge.target.cell` 是否真的指向目标母线
- `target.port` 是否仍然是母线的 `0`

这类问题的根因通常不是输出分组，而是量测元件没有真正接入电网拓扑。

### 2. 通道名没有出现在结果里

优先检查：

- `_newChannel.pins["0"]` 是否等于量测信号名
- `emt_job["args"]["output_channels"]` 是否追加了新 channel id
- `channel_name` 和 `signal_name` 是否混用了 `#`

当前建议是：

- `signal_name` 以 `#` 开头
- `channel_name` 不带 `#`

### 3. 波形能出，但数值明显不对

优先检查：

- 是否选错了目标母线
- 是否取了 ramping 段或故障段做 RMS 校核
- `VBase` 是否已通过 `fetchTopology("emtp")` 展开，而不是直接读取未展开表达式

## 当前能力边界

当前可以谨慎认为“已完成”的只有：

- `_newBus_3p` 母线电压量测链的脚本化新增
- 基于模板 edge 的路径
- 无模板时的 generic scaffold 路径
- EMT 结果通道返回与 RMS 校核

当前仍不应宣称“已完成”的有：

- 任意母线类型通用
- 任意 EMT 模型通用
- 不依赖底层 `diagram-edge` 的高层 SDK 建模能力
- 大规模批量母线自动挂表在所有模型上稳定成立

## 对应代码与测试

示例脚本：

- `examples/basic/emt_voltage_meter_chain_example.py`

本地入口测试：

- `tests/test_examples.py`

真实云端验证：

- `tests/test_emt_result.py`

相关真实样本：

- `IEEE3 Bus7`
- `IEEE3 Bus2`
- `IEEE39 bus37`
