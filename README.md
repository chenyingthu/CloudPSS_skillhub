# CloudPSS Toolkit

CloudPSS API 增强工具包 - 为电力系统仿真研究提供高级 Python 封装

## 简介

`cloudpss-toolkit` 是对 [CloudPSS](https://www.cloudpss.net/) Python SDK 的高级封装，提供更易用的 API、丰富的示例代码和完整的文档支持。

## 特性

- **简洁的 API 设计** - 隐藏底层复杂性，提供直观的接口
- **丰富的示例代码** - 从基础到高级应用的完整示例
- **内置技能模板** - 常用仿真任务的预配置模板
- **批量处理支持** - 支持大规模批量仿真和分析
- **完整的测试覆盖** - 单元测试和集成测试

## 安装

```bash
# 从 PyPI 安装（发布后）
pip install cloudpss-toolkit

# 从源码安装
git clone https://git.tsinghua.edu.cn/chen_ying/cloudpss-toolkit.git
cd cloudpss-toolkit
pip install -e .

# 开发模式安装
pip install -e ".[dev]"
```

## 快速开始

```python
from cloudpss_skills import PowerFlowSkill

# 创建潮流计算任务
skill = PowerFlowSkill()
result = skill.run(
    model="model/holdme/IEEE39",
    tolerance=1e-6
)

print(f"收敛状态: {result.converged}")
print(f"迭代次数: {result.iterations}")
```

## 示例代码

- `examples/basic/` - 基础用法示例
- `examples/advanced/` - 高级功能示例
- `examples/simulation/` - 完整仿真流程
- `examples/analysis/` - 数据分析示例

## 文档

- [使用指南](docs/usage-guide.md)
- [API 参考](docs/api-reference.md)
- [配置说明](docs/configuration.md)

## 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_power_flow.py

# 生成覆盖率报告
pytest --cov=cloudpss_skills --cov-report=html
```

## 相关项目

- [cloudpss-sim-skill](https://git.tsinghua.edu.cn/chen_ying/cloudpss-sim-skill) - Claude Code Skill 版本

## 许可证

MIT License
