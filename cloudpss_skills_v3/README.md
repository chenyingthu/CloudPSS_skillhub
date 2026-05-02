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

当前目录包含“收纳大师”的发布级 v3 工作台：

```text
cloudpss_skills_v3/
├── README.md
├── __init__.py
└── master_organizer/
    ├── __init__.py
    ├── __main__.py
    ├── cli/
    │   └── main.py
    ├── core/
    │   ├── config_manager.py
    │   ├── crypto.py
    │   ├── id_generator.py
    │   ├── models.py
    │   ├── path_manager.py
    │   ├── registries.py
    │   ├── registry_base.py
    │   ├── release_ops.py
    │   ├── result_storage.py
    │   ├── server_auth.py
    │   └── task_runner.py
    └── tests/
        └── ...
```

## 发布级能力

- Server/token/owner 绑定管理，内网服务固定为 `http://166.111.60.76:50001/`，owner 为 `chenying`。
- Case/Variant/Task/Result/Workspace/Query 的 CLI 管理面。
- `task submit --wait` 生产执行路径：读取已注册 server token，调用 CloudPSS SDK，等待 job 完成，保存结果。
- 潮流结果落盘：`manifest.json`、母线/支路 JSON、母线/支路 CSV、原始表。
- EMT 结果落盘：`plots.json`、`channels.json`、通道 JSON、通道 CSV。
- 发布级工作区治理：状态机校验、`registry/index.yaml`、实体 YAML、`logs/audit.log`、配额检查。
- Result 发布操作：`result export`、`result archive`、`result report`、`result analyze`、`result compare`。

## 常用命令

```bash
python -m cloudpss_skills_v3.master_organizer.cli.main init --path ~/.cloudpss
python -m cloudpss_skills_v3.master_organizer.cli.main server internal
python -m cloudpss_skills_v3.master_organizer.cli.main case create --name IEEE39 --rid model/chenying/IEEE39 --tag ieee39,powerflow
python -m cloudpss_skills_v3.master_organizer.cli.main task create --case-id <case_id> --name base-pf --type powerflow
python -m cloudpss_skills_v3.master_organizer.cli.main task submit <task_id> --wait
python -m cloudpss_skills_v3.master_organizer.cli.main result analyze <result_id>
python -m cloudpss_skills_v3.master_organizer.cli.main result export <result_id> --format csv --table buses --output buses.csv
python -m cloudpss_skills_v3.master_organizer.cli.main result report <result_id> --output report.md
python -m cloudpss_skills_v3.master_organizer.cli.main result archive <result_id> --output result.tar.gz
```

EMT 任务可以记录本地模型源和导出通道：

```bash
python -m cloudpss_skills_v3.master_organizer.cli.main task create \
  --case-id <case_id> \
  --name ieee3-emt \
  --type emt \
  --model-source examples/basic/ieee3-emt-prepared.yaml \
  --channel plot-2/vac:0
python -m cloudpss_skills_v3.master_organizer.cli.main task submit <task_id> --wait --timeout 300
```

## 验证

```bash
pytest cloudpss_skills_v3/master_organizer/tests -q
python -m cloudpss_skills_v3.master_organizer
CLOUDPSS_V3_RUN_LIVE=1 pytest cloudpss_skills_v3/master_organizer/tests/test_live_powerflow_registration.py -q
```

## 边界

论文学习、论文复现、paper2skill 生成技能等研究工作已经迁移到
`cloudpss_skills_v4/`。不要把新的 paper2skill 资产放回 v3。
