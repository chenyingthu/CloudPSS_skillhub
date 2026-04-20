# CloudPSS 技能 v2 - Claude Code 使用指南

## 概述

`cloudpss-sim-v2` 是专为 Claude Code 设计的技能包，将内置的 `cloudpss_skills` 封装为自然语言交互界面。

**两种使用方式的对比**：

| 方式 | 命令 | 适用场景 |
|------|------|----------|
| 内置技能 | `python -m cloudpss_skills run --config xxx.yaml` | 任何Python环境 |
| Claude Code技能 | 自然语言对话（如"帮我跑个潮流"） | 仅在Claude Code中 |

---

## 安装步骤

### 方式1：直接使用内置技能（推荐）

不需要安装Claude Code技能，直接使用项目内置的YAML配置驱动系统：

```bash
# 1. 克隆项目
git clone https://git.tsinghua.edu.cn/chen_ying/cloudpss-api-new.git
cd cloudpss-api-new

# 2. 安装依赖
pip install cloudpss matplotlib pandas

# 3. 配置Token
echo "your_token" > .cloudpss_token

# 4. 运行技能
python -m cloudpss_skills run --config cloudpss_skills/templates/power_flow.yaml
```

### 方式2：安装Claude Code技能

如果你想在Claude Code中用自然语言调用：

```bash
# 在Claude Code中执行
/skill install cloudpss-sim-v2.skill
```

安装后即可用自然语言：
- "帮我跑个IEEE39的潮流计算"
- "对IEEE3做EMT仿真"
- "做N-1安全校核"

---

## cloudpss-sim-v2.skill 结构

```
cloudpss-sim-v2/
├── SKILL.md                    # 技能定义（触发条件、工作流程）
├── evals/
│   └── evals.json              # 测试用例（8个典型场景）
├── references/
│   ├── usage-guide.md          # 使用指南
│   └── config-reference.md     # 配置参考
└── scripts/
    └── generate_config.py      # 配置生成辅助脚本
```

---

## 技能触发关键词

当安装 `cloudpss-sim-v2` 后，Claude Code 会在以下场景自动触发：

**电力系统仿真相关**：
- CloudPSS / cloudpss / 电力系统仿真
- 潮流计算 / power flow / 稳态分析
- EMT仿真 / 暂态仿真 / electromagnetic transient
- N-1安全校核 / N-1筛查
- 参数扫描 / 批量仿真

**模型相关**：
- IEEE39 / IEEE3 / IEEE标准系统
- 波形提取 / 结果可视化
- 仿真报告 / 结果分析

---

## 技能工作流程

当Claude Code触发技能后：

```
1. 检测环境
   ├── 检查是否在 cloudpss-api-new 项目目录
   ├── 检查 cloudpss_skills/ 目录是否存在
   └── 检查 .cloudpss_token 文件

2. 意图识别
   ├── 识别仿真类型（潮流/EMT/N-1/批量/参数扫描）
   ├── 确定模型（IEEE39/IEEE3/自定义）
   └── 询问关键参数（如时长、支路等）

3. 配置生成
   ├── 生成YAML配置文件
   └── 保存到 configs/<skill_name>_<timestamp>.yaml

4. 执行仿真
   ├── 运行: python -m cloudpss_skills run --config <file>
   ├── 监控输出和状态
   └── 等待仿真完成

5. 结果展示
   ├── 读取结果文件
   ├── 提取关键指标
   └── 向用户展示摘要
```

---

## 示例交互

### 示例1：潮流计算

**用户**：帮我跑个IEEE39的潮流计算

**Claude**：
1. 检测到环境正常
2. 识别为 `power_flow` 技能
3. 使用默认模型 `model/holdme/IEEE39`
4. 生成配置 `configs/power_flow_20260325_143022.yaml`
5. 执行：`python -m cloudpss_skills run --config configs/power_flow_20260325_143022.yaml`
6. 返回结果：
   ```
   仿真完成！
   模型: IEEE39
   任务ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   状态: 成功（6秒）
   结果文件: ./results/power_flow_20260325_143022.json
   ```

### 示例2：EMT仿真

**用户**：对IEEE3做EMT仿真，仿真5秒钟

**Claude**：
1. 识别为 `emt_simulation` 技能
2. 设置 `duration: 5.0`
3. 生成配置并执行
4. 等待仿真完成（约30-60秒）
5. 返回波形数据摘要

### 示例3：N-1安全校核

**用户**：做N-1安全校核

**Claude**：
1. 识别为 `n1_security` 技能
2. 询问：检查全部支路还是指定支路？
3. 用户回答：全部
4. 生成配置并执行
5. 返回结果：
   ```
   N-1校核完成
   总支路: 46条
   通过: 44条
   失败: 2条
   通过率: 95.7%
   结果文件: ./results/n1_security_20260325_143522.json
   ```

---

## 技能 vs 内置技能对比

| 特性 | 内置技能 | Claude Code技能 |
|------|----------|-----------------|
| **使用方式** | YAML配置 + 命令行 | 自然语言对话 |
| **学习成本** | 需要了解YAML结构 | 零学习成本 |
| **灵活性** | 高（可精细调整参数） | 中（自动配置） |
| **适用场景** | 批量运行、自动化脚本 | 快速单次仿真 |
| **依赖** | Python环境 | Claude Code + Python |

**建议**：
- 日常使用 → Claude Code技能（方便快捷）
- 批量运行/自动化 → 内置技能（更灵活）

---

## 分发方式

### 方式1：直接使用内置技能（推荐）

将项目作为普通Python包分发：

```bash
# 用户克隆后直接使用
git clone https://git.tsinghua.edu.cn/chen_ying/cloudpss-api-new.git
cd cloudpss-api-new
pip install -e .  # 如果添加了setup.py
python -m cloudpss_skills list
```

### 方式2：分发Claude Code技能

分享 `.skill` 文件：

```bash
# 技能文件位置
cloudpss-sim-v2.skill  # 11KB

# 用户安装
/skill install cloudpss-sim-v2.skill
```

---

## 故障排除

### 问题1：技能未触发

**现象**：用户说"帮我跑个潮流"，但Claude没有调用技能

**解决**：
1. 确认技能已安装：`/skill list`
2. 使用更明确的关键词："CloudPSS潮流计算"
3. 手动指定技能：`@cloudpss-sim-v2 帮我跑个潮流`

### 问题2：环境检测失败

**现象**：技能提示"未找到cloudpss_skills目录"

**解决**：
1. 确认在项目根目录：`pwd` 应显示 `cloudpss-api-new`
2. 确认目录存在：`ls cloudpss_skills/`
3. 如果不存在，提示用户克隆项目

### 问题3：Token问题

**现象**：认证失败或"Token无效"

**解决**：
1. 检查 `.cloudpss_token` 是否存在
2. 检查Token是否过期（在CloudPSS网站重新生成）
3. 确认Token格式正确（无多余空格/换行）

---

## 高级配置

### 自定义模型参数

如果需要调整默认参数，可以：

1. **方式A**：让Claude生成配置后手动编辑YAML
2. **方式B**：在内置技能中直接编辑模板

### 批量运行

Claude Code技能适合单次交互，批量运行建议使用内置技能：

```bash
# 批量运行多个配置
for config in configs/*.yaml; do
    python -m cloudpss_skills run --config "$config"
done
```

---

## 版本历史

- **v1.0.0** (旧版): 直接调用CloudPSS SDK的脚本
- **v2.0.0** (当前): 基于内置技能系统的YAML配置驱动

**主要改进**：
- 从脚本驱动改为配置驱动
- 新增自动等待机制
- 内置10个验证过的技能
- 支持YAML/JSON/CSV多种输出格式

---

## 总结

**对于普通用户**：
- 推荐直接使用内置技能（`python -m cloudpss_skills`）
- 学习YAML配置后更灵活

**对于Claude Code用户**：
- 安装 `cloudpss-sim-v2.skill` 后可用自然语言
- 适合快速单次仿真需求

**两种方式的底层是同一套系统**，只是交互方式不同。
