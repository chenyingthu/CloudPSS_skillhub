# CloudPSS SkillHub V3 - Paper to Skills Pipeline

## 愿景

将电力系统领域的学术论文自动转换为可执行的仿真技能（skills）。

## 目录结构

```
cloudpss_skills_v3/
├── skills/                          # 生成的skill库
│   ├── paper2skill-v0.0.1/        # 自动提取的技能
│   │   └── <skill-name>/
│   │       ├── SKILL.md
│   │       └── scripts/
│   └── human/                     # 手动编写的技能
├── papers/                         # 论文库
│   ├── to-read/                   # 待处理论文
│   ├── reading/                  # 正在处理的
│   └── processed/                # 已处理
├── paper2skill/                   # 提取引擎
│   ├── prompts/                  # Prompt模板
│   └── workflows/                # 工作流定义
└── config.yaml
```

## 论文来源

- IEEE PES Transactions
- Elsevier International Journal of Electrical Power and Energy Systems
- arXiv (power systems相关)

## 工作流

1. **论文分类** → 判断属于哪个类别（潮流/EMT/故障分析/稳定性等）
2. **提取** → 使用类别专属prompt提取核心方法
3. **生成** → 输出SKILL.md格式
4. **验证** → 用CloudPSS SDK测试验证

## 使用方式

```bash
# 放入论文
cp paper.pdf cloudpss_skills_v3/papers/to-read/

# 运行提取pipeline
python -m paper2skill extract <paper-id>

# 查看生成的skill
cat skills/paper2skill-v0.0.1/<skill-name>/SKILL.md
```

---

*Version: 0.0.1*
*Date: 2026-04-27*