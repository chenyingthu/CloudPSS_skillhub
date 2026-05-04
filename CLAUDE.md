# CLAUDE.md
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **重要提示**: 本项目使用 OpenSpec + Superpowers + gstack 三件套工作流。详见 [WORKFLOW.md](WORKFLOW.md)

## 快速开始（三件套工作流）

### 新功能开发
```bash
# Phase 1: 想清楚
/opsx:propose <feature-name>

# Phase 2: 拆清楚
/sc:brainstorm
/sc:workflow
/sc:implement

# Phase 3: 做清楚
/plan-eng-review
/review
/sc:test
/ship

# Phase 4: 复盘归档
/retro
```

### 简单修改（直接模式）
对于简单修改，可以直接使用 Claude Code 而无需走完整流程。

## Project Overview

CloudPSS SkillHub is a configuration-driven power system simulation framework with 48 specialized skills for electrical power system analysis, including power flow, transient simulation, security analysis, and stability assessment. It wraps the CloudPSS platform API.

## Common Commands

### Installation
```bash
pip install -e ".[dev]"
```

### Testing
```bash
# Run unit tests only (default, no network required)
pytest

# Run with coverage
pytest --cov=cloudpss_skills --cov-report=html

# Run integration tests (requires valid CloudPSS token)
pytest --run-integration -m "integration and not slow_emt"

# Run specific test file
pytest tests/test_powerflow_result.py

# Run specific integration test
pytest tests/test_power_flow_integration.py --run-integration
```

### CLI Usage
```bash
# List all available skills
python -m cloudpss_skills list

# Initialize skill configuration
python -m cloudpss_skills init power_flow --output pf_config.yaml

# Run a skill with config file
python -m cloudpss_skills run --config pf_config.yaml

# Alternative entry point
cloudpss-run list
```

### Linting
```bash
ruff check cloudpss_skills/ --select=E,F,W,C90 --ignore=E501
pyright cloudpss_skills/core/
```

## High-Level Architecture

### Skill System Pattern
- All skills inherit from `SkillBase` in `cloudpss_skills/core/base.py`
- Skills are registered via `@register` decorator from `cloudpss_skills/core/registry.py`
- Skills auto-discover from `cloudpss_skills/builtin/` on import
- Each skill implements: `name`, `description`, `run()`, `validate()`, `get_default_config()`, `config_schema`

### Core Modules
- `cloudpss_skills/core/base.py`: Abstract base class `SkillBase`, `SkillResult`, `SkillStatus`
- `cloudpss_skills/core/registry.py`: Skill registration and discovery (`register`, `get_skill`, `list_skills`)
- `cloudpss_skills/core/auth_utils.py`: Token management and CloudPSS API authentication
- `cloudpss_skills/core/job_runner.py`: Unified job execution and polling for CloudPSS jobs
- `cloudpss_skills/core/exporter.py`: Export utilities (JSON, CSV, HDF5, COMTRADE)
- `cloudpss_skills/core/model_utils.py`: Model loading from cloud or local

### Authentication
- Token loaded from file (`.cloudpss_token`) or environment variable (`CLOUDPSS_TOKEN`)
- Internal server uses `.cloudpss_token_internal`
- Configure via `auth.token_file` in skill config
- Token file is gitignored

### Test Organization
- Unit tests: `tests/test_*_unit.py` - no network, mock dependencies
- Integration tests: `tests/test_*_integration.py` - require CloudPSS token
- Test markers: `integration`, `slow_emt`
- Shared fixtures in `tests/fixtures/`
- Integration tests use `--run-integration` flag

### Configuration Pattern
Skills accept YAML/JSON configs with standard structure:
```yaml
skill: <skill_name>
auth:
  token_file: .cloudpss_token
model:
  rid: model/holdme/IEEE39
  source: cloud  # or "local"
output:
  format: json
  path: ./results/
```

### Multiple Versions
- `cloudpss_skills/`: Main v1 skill package with 48 builtin skills
- `cloudpss_skills_v2/`: Next generation with powerapi, powerskill modules
- `cloudpss_skills_v3/`: Research paper to skill extraction pipeline

## CI/CD Notes

GitHub Actions run on Python 3.10, 3.11, 3.12:
1. `lint` job: ruff + pyright
2. `unit-tests` job: pytest with coverage (excludes integration)
3. `integration-tests` job: Requires `CLOUDPSS_TOKEN` secret, runs only on workflow_dispatch
4. `skill-smoke-tests` job: Verifies all skills load and have schemas

## Important File Patterns

- Skills: `cloudpss_skills/builtin/<skill_name>.py`
- Skill docs: `docs/skills/<skill_name>.md`
- Config examples: `configs/examples/*.yaml`
- Test naming: `test_<skill>_<type>.py` where type is unit|integration

---

## Development Workflow (OpenSpec + Superpowers + gstack)

### Workflow Configuration

项目使用以下配置文件：
- `.gstack/config.yaml` - gstack 工作流配置
- `.openspec/proposal.md` - OpenSpec 提案模板

### Available Commands

**OpenSpec:**
- `/opsx:propose <feature>` - 创建功能提案
- `/opsx:archive` - 归档规格

**Superpowers (/sc):**
- `/sc:brainstorm` - 需求探索
- `/sc:workflow` - 生成执行计划
- `/sc:implement` - 功能实现
- `/sc:analyze` - 代码分析
- `/sc:design` - 架构设计
- `/sc:test` - 执行测试
- `/sc:review` - 代码审查

**gstack:**
- `/plan-ceo-review` - CEO 视角审查
- `/plan-eng-review` - 工程审查
- `/plan-design-review` - 设计审查
- `/review` - 代码审查
- `/qa` - QA 测试
- `/ship` - 部署上线
- `/retro` - 工程复盘

### Workflow Decision Tree

```
新功能开发?
├─ 是 → 走完整三件套流程
│      1. /opsx:propose
│      2. /sc:brainstorm
│      3. /sc:workflow
│      4. /sc:implement
│      5. /plan-eng-review
│      6. /review
│      7. /ship
│      8. /retro
│
└─ 否 (简单修改)
       └─ 复杂度 > 3 个文件?
          ├─ 是 → /sc:implement + /review
          └─ 否 → 直接使用 Claude Code
```

### Quality Gates

根据 `.gstack/config.yaml`：
- 测试覆盖率 ≥ 80%
- 代码风格检查通过 (ruff)
- 类型检查通过 (pyright)
- 安全扫描通过

# currentDate
Today's date is 2026/05/03.
