# CloudPSS SkillHub V4 - Paper to Skills Pipeline

## 愿景

将电力系统领域的学术论文转换为可执行、可验证、边界清晰的仿真技能。

这个目录承接原 `cloudpss_skills_v3` 中的论文学习和复现工作，使 v3 可以专注
Master Organizer 管理平台。

## 目录结构

```text
cloudpss_skills_v4/
├── skills/                          # 生成的 skill 库
│   ├── paper2skill-v0.0.1/          # 自动提取的技能
│   │   └── <skill-name>/
│   │       ├── SKILL.md
│   │       └── scripts/
│   └── human/                       # 手动编写的技能
├── papers/                          # 论文库
│   ├── to-read/                     # 待处理论文
│   ├── reading/                     # 正在处理的论文
│   └── processed/                   # 已处理论文
└── paper2skill/                     # 提取引擎
    ├── prompts/                     # Prompt 模板
    └── workflows/                   # 工作流定义
```

## 工作流

1. 论文分类：判断属于潮流、短路、EMT、稳定性等类别。
2. 方法提取：使用类别专属 prompt 提取核心方法、公式、数据和限制。
3. 技能生成：输出 `SKILL.md` 和可运行脚本。
4. 验证：用本地脚本和 CloudPSS SDK 路径分别验证，不能把假设性复现当作严格复现。

## 当前技能

`skills/paper2skill-v0.0.1/vsc-short-circuit-nr/` 包含 VSC 短路计算论文复现技能。

验证命令：

```bash
pytest tests/test_cloudpss_skills_v4_vsc_solver.py -q
python cloudpss_skills_v4/skills/paper2skill-v0.0.1/vsc-short-circuit-nr/scripts/run_validation.py
```

`run_validation.py` 目前应返回非零退出码，因为 Test System 1 严格论文复现仍然保持红灯。
这是刻意的防虚假成功门槛。
