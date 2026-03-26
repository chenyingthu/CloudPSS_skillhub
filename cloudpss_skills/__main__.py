"""
CloudPSS Skill System

配置驱动的电力系统仿真工具。

用法:
    python -m cloudpss_skills [命令] [选项]

示例:
    # 列出可用技能
    python -m cloudpss_skills list

    # 初始化配置
    python -m cloudpss_skills init emt_simulation --output my_sim.yaml

    # 运行技能
    python -m cloudpss_skills run --config my_sim.yaml

    # 验证配置
    python -m cloudpss_skills validate --config my_sim.yaml
"""

from cloudpss_skills.core import main

if __name__ == "__main__":
    import sys
    sys.exit(main())
