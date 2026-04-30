# CLAUDE.md
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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
