# CloudPSS 技能开发指南

本文档面向开发者，介绍如何为 CloudPSS SkillHub 创建和扩展技能，并确保配置模式的一致性。

## 目录

1. [技能基础结构](#技能基础结构)
2. [Schema 与 Default Config 一致性](#schema-与-default-config-一致性)
3. [最佳实践](#最佳实践)
4. [常见问题](#常见问题)
5. [代码示例](#代码示例)
6. [测试要求](#测试要求)

---

## 技能基础结构

### 1.1 技能类结构

每个技能应该是一个类，包含以下必需的方法和属性：

```python
from __future__ import annotations
from typing import Any
from cloudpss_skills_v2.core import SkillResult, SkillStatus

class MySkill:
    """技能描述 - 简要说明技能功能。"""

    name = "my_skill"  # 技能唯一标识
    description = "技能描述"  # 技能功能描述

    def __init__(self):
        self.logs = []
        self.artifacts = []

    @property
    def config_schema(self) -> dict[str, Any]:
        """返回 JSON Schema 定义，用于验证配置和 UI 生成。"""
        return {
            "type": "object",
            "required": ["skill"],
            "properties": {
                "skill": {
                    "type": "string",
                    "const": "my_skill",
                    "default": "my_skill"
                },
                # 其他配置项...
            },
        }

    def get_default_config(self) -> dict[str, Any]:
        """返回默认配置，必须与 schema 中的 default 值一致。"""
        return {
            "skill": self.name,
            # 其他默认值...
        }

    def validate(self, config: dict[str, Any] | None) -> tuple[bool, list[str]]:
        """验证配置是否有效。

        返回:
            (is_valid, error_list): 验证结果和错误列表
        """
        errors = []
        if not isinstance(config, dict):
            return False, ["config must be a dictionary"]
        # 其他验证逻辑...
        return len(errors) == 0, errors

    def run(self, config: dict[str, Any] | None) -> SkillResult:
        """执行技能主逻辑。"""
        # 实现技能功能...
        pass
```

---

## Schema 与 Default Config 一致性

### 2.1 为什么需要一致性

- **UI 生成**: Schema 用于生成配置界面
- **配置验证**: 用户提供配置时需要验证
- **默认值填充**: 缺失配置时使用默认值
- **用户体验**: 确保 UI 显示的默认值与实际使用的一致

### 2.2 一致性规则

**规则 1: Schema 中的 default 必须匹配 Config 中的值**

```python
# ❌ 错误示例
@property
def config_schema(self) -> dict[str, Any]:
    return {
        "properties": {
            "timeout": {"type": "number", "default": 30.0}
        }
    }

def get_default_config(self) -> dict[str, Any]:
    return {
        "timeout": 60.0  # ❌ 不匹配！schema 说是 30.0
    }

# ✅ 正确示例
@property
def config_schema(self) -> dict[str, Any]:
    return {
        "properties": {
            "timeout": {"type": "number", "default": 30.0}
        }
    }

def get_default_config(self) -> dict[str, Any]:
    return {
        "timeout": 30.0  # ✅ 匹配！
    }
```

**规则 2: 嵌套对象的 default 必须一致**

```python
# ✅ 正确示例
@property
def config_schema(self) -> dict[str, Any]:
    return {
        "properties": {
            "model": {
                "type": "object",
                "properties": {
                    "rid": {"type": "string", "default": "case14"},
                    "source": {"type": "string", "default": "local"}
                }
            }
        }
    }

def get_default_config(self) -> dict[str, Any]:
    return {
        "model": {
            "rid": "case14",      # ✅ 匹配 schema default
            "source": "local"     # ✅ 匹配 schema default
        }
    }
```

**规则 3: 数组的 default 处理**

```python
# ✅ 正确示例 - 数组项有 default
@property
def config_schema(self) -> dict[str, Any]:
    return {
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}  # 数组项字段不设 default
                    }
                },
                "default": [{"name": "default"}]  # 数组整体有 default
            }
        }
    }

def get_default_config(self) -> dict[str, Any]:
    return {
        "items": [{"name": "default"}]  # ✅ 匹配
    }
```

**规则 4: 空对象的处理**

```python
# ✅ 正确示例 - 空对象
@property
def config_schema(self) -> dict[str, Any]:
    return {
        "properties": {
            "metadata": {
                "type": "object",
                "default": {}  # ✅ 明确指定空对象 default
            }
        }
    }

def get_default_config(self) -> dict[str, Any]:
    return {
        "metadata": {}  # ✅ 匹配 schema
    }
```

### 2.3 验证一致性

使用提供的脚本验证一致性：

```bash
# 验证所有技能
python scripts/validate_schema_defaults.py

# 运行单元测试
python -m pytest tests/test_schema_consistency_unit.py -v
```

---

## 最佳实践

### 3.1 Schema 设计原则

**1. 使用明确的类型**

```python
# ✅ 好的示例
{
    "count": {"type": "integer", "minimum": 0, "default": 10},
    "ratio": {"type": "number", "minimum": 0.0, "maximum": 1.0, "default": 0.5},
    "name": {"type": "string", "minLength": 1, "default": "default_name"}
}

# ❌ 避免的示例
{
    "value": {},  # 缺少类型定义
}
```

**2. 为所有可选字段设置 default**

```python
# ✅ 好的示例
{
    "timeout": {"type": "number", "default": 30.0},
    "retries": {"type": "integer", "default": 3}
}

# ❌ 避免的示例 - 可选字段缺少 default
{
    "timeout": {"type": "number"}  # 用户不提供时会出错
}
```

**3. 使用 enum 限制选项**

```python
# ✅ 好的示例
{
    "format": {
        "type": "string",
        "enum": ["json", "csv", "hdf5"],
        "default": "json"
    }
}
```

### 3.2 配置验证原则

**1. 尽早失败**

```python
def validate(self, config: dict[str, Any] | None) -> tuple[bool, list[str]]:
    errors = []

    # 检查 config 类型
    if not isinstance(config, dict):
        return False, ["config must be a dictionary"]

    # 检查必需字段
    if not config.get("model", {}).get("rid"):
        errors.append("model.rid is required")

    return len(errors) == 0, errors
```

**2. 提供清晰的错误信息**

```python
# ✅ 好的示例
errors.append("model.rid is required")
errors.append(f"timeout must be positive, got {timeout}")

# ❌ 避免的示例
errors.append("Invalid")  # 太模糊
```

**3. 处理 None 配置**

```python
def validate(self, config: dict[str, Any] | None) -> tuple[bool, list[str]]:
    if config is None:
        return False, ["config is required"]
    # ...
```

### 3.3 代码组织原则

**1. 技能文件命名**

```
cloudpss_skills_v2/
├── tools/
│   ├── visualize.py              # 工具类技能
│   ├── compare_visualization.py
│   └── waveform_export.py
├── poweranalysis/
│   ├── power_flow.py             # 分析类技能
│   ├── n1_security.py
│   └── renewable_integration.py
```

**2. 导入规范**

```python
# ✅ 好的示例 - 使用绝对导入
from cloudpss_skills_v2.core import SkillResult, SkillStatus
from cloudpss_skills_v2.core.skill_result import LogEntry

# ❌ 避免的示例 - 相对导入
from ..core import SkillResult
```

---

## 常见问题

### Q1: Schema 和 Config 不一致会导致什么问题？

**A:** 会导致：
- UI 显示的默认值与实际使用的不一致
- 用户困惑
- 配置验证失败
- CI/CD 检查失败

### Q2: 如何修复已有的不一致？

**A:** 运行验证脚本查看不一致项，然后修改 schema 或 default config：

```bash
python scripts/validate_schema_defaults.py
```

### Q3: 数组项的 default 如何处理？

**A:** 对于数组项，如果每个项有复杂结构，建议在数组级别设置 default，而不是在项的字段级别。

### Q4: 可以为字段设置多个类型吗？

**A:** 可以，使用数组形式：

```python
{
    "value": {"type": ["string", "number", "null"], "default": None}
}
```

### Q5: CI/CD 检查失败怎么办？

**A:** 在提交 PR 前本地运行验证脚本：

```bash
python scripts/validate_schema_defaults.py
python -m pytest tests/test_schema_consistency_unit.py -v
```

---

## 代码示例

### 完整技能示例

```python
#!/usr/bin/env python3
"""示例技能 - 展示完整的技能结构。"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from cloudpss_skills_v2.core import SkillResult, SkillStatus, LogEntry


class ExampleSkill:
    """示例技能 - 展示最佳实践。"""

    name = "example_skill"
    description = "示例技能，展示完整的结构"

    def __init__(self):
        self.logs: list[LogEntry] = []
        self.artifacts = []

    @property
    def config_schema(self) -> dict[str, Any]:
        """JSON Schema 定义。"""
        return {
            "type": "object",
            "required": ["skill"],
            "properties": {
                "skill": {
                    "type": "string",
                    "const": "example_skill",
                    "default": "example_skill"
                },
                "engine": {
                    "type": "string",
                    "enum": ["cloudpss", "pandapower"],
                    "default": "cloudpss"
                },
                "model": {
                    "type": "object",
                    "properties": {
                        "rid": {"type": "string", "default": "case14"},
                        "source": {
                            "type": "string",
                            "enum": ["cloud", "local"],
                            "default": "local"
                        }
                    }
                },
                "parameters": {
                    "type": "object",
                    "properties": {
                        "timeout": {
                            "type": "number",
                            "minimum": 1.0,
                            "default": 30.0
                        },
                        "iterations": {
                            "type": "integer",
                            "minimum": 1,
                            "default": 100
                        }
                    }
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "format": {
                            "type": "string",
                            "enum": ["json", "csv"],
                            "default": "json"
                        },
                        "path": {"type": "string", "default": "./results/"}
                    }
                }
            }
        }

    def get_default_config(self) -> dict[str, Any]:
        """默认配置 - 与 schema 完全一致。"""
        return {
            "skill": self.name,
            "engine": "cloudpss",
            "model": {
                "rid": "case14",
                "source": "local"
            },
            "parameters": {
                "timeout": 30.0,
                "iterations": 100
            },
            "output": {
                "format": "json",
                "path": "./results/"
            }
        }

    def validate(self, config: dict[str, Any] | None) -> tuple[bool, list[str]]:
        """验证配置。"""
        errors = []

        if not isinstance(config, dict):
            return False, ["config must be a dictionary"]

        # 验证必需字段
        if not config.get("model", {}).get("rid"):
            errors.append("model.rid is required")

        # 验证参数范围
        params = config.get("parameters", {})
        timeout = params.get("timeout")
        if timeout is not None and (not isinstance(timeout, (int, float)) or timeout < 1.0):
            errors.append(f"parameters.timeout must be >= 1.0, got {timeout}")

        return len(errors) == 0, errors

    def run(self, config: dict[str, Any] | None) -> SkillResult:
        """执行技能。"""
        start_time = datetime.now()
        self.logs = []

        # 验证配置
        is_valid, errors = self.validate(config)
        if not is_valid:
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                error="; ".join(errors),
                logs=self.logs,
                start_time=start_time,
                end_time=datetime.now()
            )

        # 执行技能逻辑...
        self.logs.append(LogEntry(
            timestamp=datetime.now(),
            level="info",
            message="Example skill executed successfully"
        ))

        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.SUCCESS,
            data={"message": "Success"},
            logs=self.logs,
            start_time=start_time,
            end_time=datetime.now()
        )
```

---

## 测试要求

### 必需测试

每个新技能必须包含以下测试：

**1. 结构测试**

```python
def test_skill_has_required_methods():
    skill = MySkill()
    assert hasattr(skill, 'config_schema')
    assert hasattr(skill, 'get_default_config')
    assert hasattr(skill, 'validate')
    assert hasattr(skill, 'run')
```

**2. Schema/Default 一致性测试**

```python
def test_schema_default_matches_config():
    skill = MySkill()
    schema = skill.config_schema
    default = skill.get_default_config()

    # 验证必需字段
    assert "skill" in default
    assert default["skill"] == skill.name
```

**3. 验证方法测试**

```python
def test_validate_with_valid_config():
    skill = MySkill()
    default = skill.get_default_config()
    is_valid, errors = skill.validate(default)
    assert is_valid
    assert len(errors) == 0

def test_validate_with_invalid_config():
    skill = MySkill()
    is_valid, errors = skill.validate({"invalid": "config"})
    assert not is_valid
    assert len(errors) > 0
```

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试文件
python -m pytest tests/test_my_skill_unit.py -v

# 运行 schema 一致性测试
python -m pytest tests/test_schema_consistency_unit.py -v
```

---

## 总结

开发 CloudPSS 技能时，务必遵循以下原则：

1. ✅ **Schema 与 Default Config 必须一致**
2. ✅ **所有可选字段设置 default**
3. ✅ **验证方法返回 (bool, list[str]) 元组**
4. ✅ **提供清晰的错误信息**
5. ✅ **在提交前运行验证脚本**

遵循这些原则可以确保技能质量，避免 CI/CD 检查失败。
