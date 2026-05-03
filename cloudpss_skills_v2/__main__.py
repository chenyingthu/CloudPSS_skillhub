"""CloudPSS Skills V2 - Module Entry Point.

允许通过 `python -m cloudpss_skills_v2` 运行 CLI。

用法:
    python -m cloudpss_skills_v2 [命令] [选项]

示例:
    # 列出可用技能
    python -m cloudpss_skills_v2 list

    # 运行技能
    python -m cloudpss_skills_v2 run --config config.yaml

    # 对比多个配置
    python -m cloudpss_skills_v2 compare --configs a.yaml b.yaml
"""

import sys

from cloudpss_skills_v2.cli import main

if __name__ == "__main__":
    sys.exit(main())
