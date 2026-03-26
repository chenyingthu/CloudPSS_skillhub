# CloudPSS 技能系统 - 使用与测试指南

## 快速验证

### 1. 检查系统状态

```bash
# 进入项目目录
cd /home/chenying/researches/cloudpss-api-enhanced

# 验证技能系统安装
python -m cloudpss_skills version
```

**预期输出**:
```
CloudPSS Skill System
版本: 1.0.0
```

### 2. 查看可用技能

```bash
python -m cloudpss_skills list
```

**预期输出**:
```
可用技能 (4个):
------------------------------------------------------------

  emt_simulation
    描述: 运行EMT暂态仿真并导出波形数据
    版本: 1.0.0

  power_flow
    描述: 运行潮流计算并输出结果
    版本: 1.0.0

  ieee3_prep
    描述: 准备IEEE3模型用于EMT仿真（调整故障时间和输出通道）
    版本: 1.0.0

  waveform_export
    描述: 从仿真结果导出波形数据
    版本: 1.0.0
```

### 3. 查看技能详情

```bash
python -m cloudpss_skills describe emt_simulation
```

**预期输出**:
```
技能详情: emt_simulation
============================================================
描述: 运行EMT暂态仿真并导出波形数据
版本: 1.0.0
作者: CloudPSS

默认配置:
------------------------------------------------------------
{
  "skill": "emt_simulation",
  "auth": {"token_file": ".cloudpss_token"},
  "model": {"rid": "model/holdme/IEEE3", "source": "cloud"},
  ...
}
```

---

## 测试套件

### 运行单元测试

```bash
# 运行所有测试
python -m pytest tests/skills/ tests/integration/ -v

# 仅运行单元测试（不需要网络）
python -m pytest tests/skills/test_core.py tests/skills/test_builtin.py -v

# 运行特定测试
python -m pytest tests/skills/test_core.py::TestSkillBase -v
```

**预期输出**:
```
============================= test session starts =============================
collected 28 items

tests/skills/test_core.py::TestValidationResult::test_valid_result PASSED
tests/skills/test_core.py::TestValidationResult::test_add_error PASSED
...
============================== 28 passed in 0.07s ============================
```

### 测试覆盖率

```bash
# 安装coverage工具
pip install pytest-cov

# 生成覆盖率报告
python -m pytest tests/skills/ --cov=skills --cov-report=html

# 查看报告
open htmlcov/index.html  # macOS
# 或
firefox htmlcov/index.html  # Linux
```

---

## 使用场景

### 场景1: 首次使用（完整流程）

```bash
# 步骤1: 确认token已配置
ls -la .cloudpss_token

# 步骤2: 创建EMT仿真配置
python -m cloudpss_skills init emt_simulation --output my_first_sim.yaml

# 步骤3: 查看生成的配置
cat my_first_sim.yaml

# 步骤4: 验证配置格式
python -m cloudpss_skills validate --config my_first_sim.yaml

# 步骤5: 运行仿真（需要有效的token和网络）
python -m cloudpss_skills run --config my_first_sim.yaml
```

**预期行为**:
1. 创建配置文件
2. 验证通过
3. 运行仿真，显示进度
4. 导出CSV文件到 `./results/`

### 场景2: 批量仿真

```bash
# 创建多个配置
mkdir -p batch_jobs

# 配置1: IEEE3模型
cat > batch_jobs/ieee3.yaml << 'EOF'
skill: emt_simulation
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE3
output:
  format: csv
  path: ./results/batch/
  prefix: ieee3
EOF

# 配置2: IEEE39模型
cat > batch_jobs/ieee39.yaml << 'EOF'
skill: emt_simulation
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
output:
  format: csv
  path: ./results/batch/
  prefix: ieee39
EOF

# 批量运行
python -m cloudpss_skills batch --config-dir ./batch_jobs/
```

**预期输出**:
```
[INFO] 发现 2 个配置
处理: ieee3.yaml
------------------------------------------------------------
[INFO] 加载配置...
...
处理: ieee39.yaml
------------------------------------------------------------
...
============================================================
批量执行汇总:
------------------------------------------------------------
成功: 2
失败: 0
```

### 场景3: 使用本地模型

```bash
# 步骤1: 准备本地模型
python -m cloudpss_skills init ieee3_prep --output prep.yaml
# 编辑prep.yaml调整故障参数

# 步骤2: 运行准备
python -m cloudpss_skills run --config prep.yaml
# 生成 ieee3_prepared.yaml

# 步骤3: 使用本地模型运行EMT
cat > local_sim.yaml << 'EOF'
skill: emt_simulation
auth:
  token_file: .cloudpss_token
model:
  rid: ./ieee3_prepared.yaml
  source: local
output:
  format: csv
  path: ./results/
EOF

python -m cloudpss_skills run --config local_sim.yaml
```

### 场景4: 导出已有任务的波形

```bash
# 假设已有任务ID: abc123xyz
cat > export_waveform.yaml << 'EOF'
skill: waveform_export
source:
  job_id: "abc123xyz"
  auth:
    token_file: .cloudpss_token
export:
  plots: [0]
  channels: []
  time_range:
    start: 2.0
    end: 3.0
output:
  format: csv
  path: ./results/
  filename: fault_period.csv
EOF

python -m cloudpss_skills run --config export_waveform.yaml
```

### 场景5: CI/CD集成

```yaml
# .github/workflows/simulation.yml
name: Power System Simulation

on: [push]

jobs:
  simulate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9

      - name: Install dependencies
        run: |
          pip install cloudpss
          pip install -e .

      - name: Run simulation
        env:
          CLOUDPSS_TOKEN: ${{ secrets.CLOUDPSS_TOKEN }}
        run: |
          python -m cloudpss_skills run --config configs/ci_simulation.yaml

      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: simulation-results
          path: results/
```

---

## 配置文件模板

### 模板1: 最小配置

```yaml
skill: emt_simulation
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE3
```

### 模板2: 完整配置

```yaml
skill: emt_simulation
version: "1.0"

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
  channels: []
```

### 模板3: 环境变量配置

```yaml
skill: emt_simulation
auth:
  token: "${CLOUDPSS_TOKEN}"
model:
  rid: "${MODEL_RID:-model/holdme/IEEE3}"
output:
  path: "${OUTPUT_PATH:-./results/}"
```

---

## 故障排查

### 问题1: "No module named 'skills'"

**原因**: 未在项目根目录运行

**解决**:
```bash
cd /home/chenying/researches/cloudpss-api-enhanced
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python -m cloudpss_skills list
```

### 问题2: "Token文件不存在"

**解决**:
```bash
# 检查文件是否存在
ls -la .cloudpss_token

# 创建token文件
echo "your_token_here" > .cloudpss_token

# 或使用环境变量
export CLOUDPSS_TOKEN="your_token_here"
```

### 问题3: "配置验证失败"

**解决**:
```bash
# 验证配置获取详细信息
python -m cloudpss_skills validate --config my_sim.yaml --verbose

# 检查YAML语法
python -c "import yaml; yaml.safe_load(open('my_sim.yaml'))"

# 使用示例配置对比
diff my_sim.yaml configs/examples/basic_emt.yaml
```

### 问题4: "技能未找到"

**解决**:
```bash
# 确认技能已注册
python -m cloudpss_skills list

# 检查技能名称拼写
python -m cloudpss_skills describe emt_simulation
```

### 问题5: 导入错误

**解决**:
```bash
# 检查Python路径
python -c "import sys; print('\n'.join(sys.path))"

# 确保在项目根目录
pwd  # 应该是 .../cloudpss-api-enhanced

# 安装依赖
pip install pyyaml jsonschema click
```

---

## 性能测试

### 测量执行时间

```bash
# 使用time命令
time python -m cloudpss_skills run --config my_sim.yaml

# 使用Python的cProfile
python -m cProfile -o profile.stats -m skills run --config my_sim.yaml

# 分析结果
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative').print_stats(20)"
```

### 内存使用

```bash
# 使用memory_profiler
pip install memory_profiler

python -m memory_profiler -m skills run --config my_sim.yaml
```

---

## 高级用法

### 自定义日志级别

```bash
# 调试模式
python -m cloudpss_skills run --config my_sim.yaml --verbose

# 仅错误信息
export SKILLS_LOG_LEVEL=ERROR
python -m cloudpss_skills run --config my_sim.yaml
```

### 结果后处理

```bash
# 运行并保存结果到JSON
python -m cloudpss_skills run --config my_sim.yaml --json > result.json

# 提取特定字段
python -c "import json,sys; d=json.load(open('result.json')); print(d['duration'])"
```

### 程序化调用

```python
# 在Python代码中使用技能
from skills.core import get_skill, auto_discover
from skills.core.config import ConfigLoader

# 自动发现技能
auto_discover()

# 获取技能
skill = get_skill("emt_simulation")

# 加载配置
config = ConfigLoader.load("my_sim.yaml")

# 验证
validation = skill.validate(config)
if not validation.valid:
    print("配置错误:", validation.errors)
    exit(1)

# 执行
result = skill.run(config)

if result.success:
    print(f"成功！耗时: {result.duration}s")
    for artifact in result.artifacts:
        print(f"输出: {artifact.path}")
else:
    print(f"失败: {result.error}")
```

---

## 开发测试

### 添加新技能后测试

```python
# tests/skills/test_my_skill.py
import unittest
from skills.builtin import MySkill

class TestMySkill(unittest.TestCase):
    def setUp(self):
        self.skill = MySkill()

    def test_name(self):
        self.assertEqual(self.skill.name, "my_skill")

    def test_default_config(self):
        defaults = self.skill.get_default_config()
        self.assertIn("skill", defaults)

if __name__ == "__main__":
    unittest.main()
```

运行测试:
```bash
python -m pytest tests/skills/test_my_skill.py -v
```

---

## 总结

### 常用命令速查

```bash
# 基础命令
python -m cloudpss_skills list                                    # 列出技能
python -m cloudpss_skills describe emt_simulation                 # 查看详情
python -m cloudpss_skills init emt_simulation -o sim.yaml         # 创建配置
python -m cloudpss_skills validate -c sim.yaml                    # 验证配置
python -m cloudpss_skills run -c sim.yaml                         # 运行技能
python -m cloudpss_skills batch -d ./configs/                     # 批量运行

# 测试命令
python -m pytest tests/skills/ -v                        # 运行测试
python -m pytest tests/skills/ --cov=skills              # 覆盖率

# 故障排查
python -m cloudpss_skills validate -c sim.yaml --verbose          # 详细验证
python -c "import yaml; yaml.safe_load(open('sim.yaml'))" # 检查YAML
```

### 下一步

1. **试用**: 运行 `python -m cloudpss_skills init emt_simulation` 创建第一个配置
2. **学习**: 阅读 `docs/skills/user_manual.md` 了解完整功能
3. **定制**: 基于 `configs/examples/` 创建自己的配置
4. **扩展**: 参考架构文档开发自定义技能

---

**文档版本**: 1.0.0
**更新日期**: 2024-03-24
