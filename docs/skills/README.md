# CloudPSS 技能系统

配置驱动的电力系统仿真工具。无需编程，只需编辑YAML配置文件即可运行仿真。

## 快速开始

### 1. 安装

```bash
# 确保已安装CloudPSS SDK
pip install cloudpss

# 克隆本仓库
git clone https://github.com/cloudpss/skills.git
cd skills
```

### 2. 配置Token

```bash
# 将CloudPSS API Token写入文件
echo "your_token_here" > .cloudpss_token
```

### 3. 列出可用技能

```bash
python -m cloudpss_skills list
```

### 4. 初始化配置

```bash
# 创建EMT仿真配置
python -m cloudpss_skills init emt_simulation --output my_sim.yaml
```

### 5. 运行技能

```bash
python -m cloudpss_skills run --config my_sim.yaml
```

## 核心概念

### 什么是技能？

技能是预置的、可复用的仿真脚本：

- **emt_simulation** - 运行EMT暂态仿真
- **power_flow** - 运行潮流计算
- **ieee3_prep** - 准备IEEE3模型
- **waveform_export** - 导出波形数据
- **n1_security** - N-1安全校核
- **param_scan** - 参数扫描
- **result_compare** - 结果对比
- **visualize** - 可视化
- **topology_check** - 拓扑检查
- **batch_powerflow** - 批量潮流计算

### 配置驱动

所有参数都在YAML配置中：

```yaml
skill: emt_simulation

model:
  rid: model/holdme/IEEE3

output:
  format: csv
  path: ./results/
```

## 命令参考

| 命令 | 说明 |
|-----|------|
| `list` | 列出可用技能 |
| `describe <skill>` | 查看技能详情 |
| `init <skill>` | 创建配置模板 |
| `run --config <file>` | 运行技能 |
| `validate --config <file>` | 验证配置 |
| `batch --config-dir <dir>` | 批量运行 |

## 配置示例

### EMT仿真

```yaml
skill: emt_simulation

auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE3

simulation:
  duration: 10.0
  timeout: 300

output:
  format: csv
  path: ./results/
  channels: ["Bus1_Va", "Bus1_Vb"]
```

### 潮流计算

```yaml
skill: power_flow

auth:
  token_file: .cloudpss_token

model:
  rid: model/holdme/IEEE39

output:
  format: json
  path: ./results/
```

## 目录结构

```
.
├── skills/              # 技能系统
│   ├── core/           # 核心模块
│   ├── builtin/        # 内置技能
│   └── templates/      # 配置模板
├── tests/              # 测试套件
├── configs/            # 用户配置
│   └── templates/      # 配置模板
└── docs/               # 文档
    └── design/         # 设计文档
```

## 特点

- **零编程** - 只需编辑YAML配置
- **预置技能** - 常用功能开箱即用
- **一键执行** - 简化操作，隐藏技术细节
- **确定性** - 相同配置产生相同结果
- **可累积** - 技能库不断丰富

## 开发

### 创建自定义技能

```python
from skills.core import SkillBase, register

@register
class MySkill(SkillBase):
    @property
    def name(self):
        return "my_skill"

    @property
    def description(self):
        return "我的自定义技能"

    def run(self, config):
        # 实现逻辑
        return SkillResult(...)
```

## 更多信息

- [架构设计](docs/design/skill_system_architecture.md)
- [用户手册](docs/skills/user_manual.md)
- [配置参考](docs/skills/config_reference.md)

## 许可证

MIT License
