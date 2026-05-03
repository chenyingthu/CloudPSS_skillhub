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

## Portal

收纳大师 Portal 是一个本地可视化工作台，零新增前端依赖，直接复用 v3 的
registry、task runner、result storage 和 release ops。

启动：

```bash
python -m cloudpss_skills_v3.master_organizer.portal.server --host 127.0.0.1 --port 8765
```

局域网访问时绑定 `0.0.0.0`。Portal 会自动生成访问 token，并在启动日志中打印带
`?token=...` 的 URL；也可以显式传入固定 token：

```bash
python -m cloudpss_skills_v3.master_organizer.portal.server --host 0.0.0.0 --port 8766 --token <portal-token>
```

打开：

```text
http://127.0.0.1:8765
```

第一版 Portal 覆盖：

- Dashboard：workspace、实体数量、存储和最近任务/结果。
- Case 工作台：Case 树、模型 RID、Server、Variant、Task、Result 关系。
- Task Runner：创建 powerflow/EMT 任务，一键运行 `task submit --wait` 生产路径。
- Result Viewer：查看 metadata、manifest、JSON artifacts、潮流表预览和 EMT 通道预览。
- Reports：生成包含 Case、Task、配置、结果摘要和文件清单的报告，并归档结果目录。
- Servers：查看 server URL、owner、默认状态和 token 来源；API 输出会隐藏加密 token。
- Audit：查看 `logs/audit.log`。

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
