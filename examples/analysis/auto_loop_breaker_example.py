"""
模型自动解环技能示例

演示如何使用 auto_loop_breaker 技能检测并消除模型中的控制环路。
"""

import yaml
from pathlib import Path

from cloudpss import Model, setToken
from cloudpss_skills import SkillExecutor


def check_loops_only():
    """仅检测环路，不解环（试运行模式）"""

    config = {
        "skill": "auto_loop_breaker",
        "auth": {
            "token_file": ".cloudpss_token"
        },
        "model": {
            "rid": "model/holdme/IEEE39",
            "source": "cloud"
        },
        "algorithm": {
            "max_iterations": 500,
            "strategy": "degree"
        },
        "output": {
            "save_model": False,
            "dry_run": True  # 试运行模式
        }
    }

    config_path = Path("config_loop_breaker_check.yaml")
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print(f"环路检测配置已保存: {config_path}")
    print("\n执行命令:")
    print(f"  python -m cloudpss_skills run --config {config_path}")
    print("\n预期结果:")
    print("  - 分析模型拓扑结构")
    print("  - 检测是否存在控制环路")
    print("  - 生成环路分析报告（不修改模型）")


def basic_loop_breaking():
    """基础解环配置"""

    config = {
        "skill": "auto_loop_breaker",
        "auth": {
            "token_file": ".cloudpss_token"
        },
        "model": {
            "rid": "model/holdme/ControlSystemModel",
            "source": "cloud"
        },
        "algorithm": {
            "max_iterations": 500,
            "strategy": "degree"  # 度数优先策略
        },
        "loop_node": {
            "init_value": "0",
            "name_prefix": "LoopBreaker"
        },
        "output": {
            "save_model": True,
            "dry_run": False,
            "new_name_suffix": "_unloop"
        }
    }

    config_path = Path("config_loop_breaker_basic.yaml")
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print(f"\n基础解环配置已保存: {config_path}")
    print("\n执行命令:")
    print(f"  python -m cloudpss_skills run --config {config_path}")
    print("\n预期结果:")
    print("  - 使用度数优先策略选择解环点")
    print("  - 在环路中自动插入解环元件")
    print("  - 保存解环后的模型（名称后缀_unloop）")


def advanced_loop_breaking():
    """高级解环配置（使用混合策略）"""

    config = {
        "skill": "auto_loop_breaker",
        "auth": {
            "token_file": ".cloudpss_token"
        },
        "model": {
            "rid": "model/holdme/ComplexControlModel",
            "source": "cloud"
        },
        "algorithm": {
            "max_iterations": 1000,
            "strategy": "hybrid",  # 混合策略
            "random_seed": 42
        },
        "loop_node": {
            "init_value": "0.0",
            "name_prefix": "AutoBreak"
        },
        "output": {
            "save_model": True,
            "dry_run": False,
            "new_name_suffix": "_nobloop"
        }
    }

    config_path = Path("config_loop_breaker_advanced.yaml")
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print(f"\n高级解环配置已保存: {config_path}")
    print("\n执行命令:")
    print(f"  python -m cloudpss_skills run --config {config_path}")
    print("\n预期结果:")
    print("  - 使用混合策略（度数+随机）选择解环点")
    print("  - 最大迭代次数1000次")
    print("  - 支持复杂模型的解环")
    print("  - 保存解环后的模型（名称后缀_nobloop）")


def custom_init_value():
    """自定义解环点初始值"""

    config = {
        "skill": "auto_loop_breaker",
        "auth": {
            "token_file": ".cloudpss_token"
        },
        "model": {
            "rid": "model/holdme/SpecialModel",
            "source": "cloud"
        },
        "algorithm": {
            "max_iterations": 500,
            "strategy": "degree"
        },
        "loop_node": {
            "init_value": "1.0",  # 自定义初始值
            "name_prefix": "CustomBreak"
        },
        "output": {
            "save_model": True,
            "dry_run": False,
            "new_name_suffix": "_unloop"
        }
    }

    config_path = Path("config_loop_breaker_custom.yaml")
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print(f"\n自定义初始值配置已保存: {config_path}")
    print("\n执行命令:")
    print(f"  python -m cloudpss_skills run --config {config_path}")
    print("\n预期结果:")
    print("  - 解环点初始值设为1.0")
    print("  - 解环点名称为 CustomBreak_1, CustomBreak_2, ...")
    print("  - 适合需要特定初始条件的模型")


if __name__ == "__main__":
    print("=" * 60)
    print("模型自动解环技能示例")
    print("=" * 60)

    check_loops_only()
    basic_loop_breaking()
    advanced_loop_breaking()
    custom_init_value()

    print("\n" + "=" * 60)
    print("所有配置文件已生成！")
    print("=" * 60)
    print("\n使用步骤:")
    print("1. 确保已配置CloudPSS Token (.cloudpss_token)")
    print("2. 建议先用 dry_run: true 检查环路")
    print("3. 确认无误后再执行实际解环")
    print("4. 查看解环报告: results/auto_loop_breaker_report.json")
    print("\n注意事项:")
    print("- 试运行模式不会修改模型，只生成报告")
    print("- 解环后会保存为新模型（原模型不变）")
    print("- 解环点初始值会影响仿真初始状态")
    print("- 对于电气代数环，需要手动处理")
