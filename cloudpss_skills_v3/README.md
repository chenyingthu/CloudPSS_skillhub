# CloudPSS SkillHub V3 - Master Organizer

## 定位

`cloudpss_skills_v3` 只承载 CloudPSS SkillHub 的“收纳大师”管理平台实现。

它的目标是把 CloudPSS 的本地工作对象统一整理为五类实体：

- Server
- Case
- Variant
- Task
- Result

详细设计见 `docs/CLOUDPSS_MASTER_ORGANIZER_PLAN.md`。

## 当前范围

当前目录只包含 Phase 1 基础设施：

```text
cloudpss_skills_v3/
├── README.md
├── __init__.py
└── master_organizer/
    ├── __init__.py
    ├── __main__.py
    ├── core/
    │   ├── config_manager.py
    │   ├── crypto.py
    │   ├── id_generator.py
    │   ├── models.py
    │   ├── path_manager.py
    │   └── registry_base.py
    └── tests/
        ├── test_core.py
        └── verify_phase1.py
```

## 验证

```bash
pytest cloudpss_skills_v3/master_organizer/tests -q
python cloudpss_skills_v3/master_organizer/tests/verify_phase1.py
python -m cloudpss_skills_v3.master_organizer
```

## 边界

论文学习、论文复现、paper2skill 生成技能等研究工作已经迁移到
`cloudpss_skills_v4/`。不要把新的 paper2skill 资产放回 v3。
