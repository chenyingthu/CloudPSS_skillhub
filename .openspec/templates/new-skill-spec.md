# Spec: [Skill Name]

## 需求描述

### 功能目标
[描述这个技能要实现什么功能]

### 输入参数
| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| param1 | str  | 是   | 参数说明 |
| param2 | int  | 否   | 参数说明 |

### 输出结果
| 字段名 | 类型 | 描述 |
|--------|------|------|
| result1 | float | 结果说明 |
| result2 | dict  | 结果说明 |

## 技术方案

### 核心算法
[描述使用的算法或方法]

### 依赖组件
- `cloudpss_skills/core/job_runner.py` - 作业执行
- `cloudpss_skills/core/exporter.py` - 结果导出

### API 端点
- `POST /api/v1/simulation/[skill-name]`

## 实现步骤

1. [ ] 创建技能文件 `cloudpss_skills/builtin/[skill_name].py`
2. [ ] 实现 `SkillBase` 子类
3. [ ] 编写单元测试 `tests/test_[skill_name]_unit.py`
4. [ ] 编写集成测试 `tests/test_[skill_name]_integration.py`
5. [ ] 编写文档 `docs/skills/[skill_name].md`
6. [ ] 创建配置示例 `configs/examples/[skill_name].yaml`

## 验收标准

- [ ] 技能可以正确注册到注册表
- [ ] 配置验证通过
- [ ] 单元测试覆盖率 ≥ 80%
- [ ] 集成测试通过（需要 CloudPSS token）
- [ ] 文档完整
