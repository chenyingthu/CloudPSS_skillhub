"""
CloudPSS Skill System - CLI Module

命令行接口实现。
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List, Optional

from .base import SkillResult, SkillStatus
from .config import ConfigGenerator, ConfigLoader, ConfigValidator, InteractiveConfigBuilder
from .registry import auto_discover, get_skill, has_skill, list_skills

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def print_error(message: str):
    """打印错误信息"""
    print(f"[ERROR] {message}", file=sys.stderr)


def print_success(message: str):
    """打印成功信息"""
    print(f"[OK] {message}")


def print_info(message: str):
    """打印信息"""
    print(f"[INFO] {message}")


def print_warning(message: str):
    """打印警告"""
    print(f"[WARN] {message}")


def cmd_list(args: argparse.Namespace) -> int:
    """列出可用技能"""
    skills = list_skills()

    if not skills:
        print_info("暂无可用技能")
        return 0

    print(f"\n可用技能 ({len(skills)}个):")
    print("-" * 60)

    for skill in sorted(skills, key=lambda s: s.name):
        print(f"\n  {skill.name}")
        print(f"    描述: {skill.description}")
        print(f"    版本: {skill.version}")

    print()
    return 0


def cmd_describe(args: argparse.Namespace) -> int:
    """查看技能详情"""
    skill_name = args.skill

    if not has_skill(skill_name):
        print_error(f"技能 '{skill_name}' 不存在")
        print_info(f"可用技能: {', '.join(s.name for s in list_skills())}")
        return 1

    skill = get_skill(skill_name)
    desc = skill.describe()

    print(f"\n技能详情: {skill.name}")
    print("=" * 60)
    print(f"描述: {desc['description']}")
    print(f"版本: {desc['version']}")
    print(f"作者: {desc['author']}")

    print(f"\n默认配置:")
    print("-" * 60)
    print(json.dumps(desc['defaults'], indent=2, ensure_ascii=False))

    if args.verbose:
        print(f"\n配置Schema:")
        print("-" * 60)
        print(json.dumps(desc['schema'], indent=2, ensure_ascii=False))

    print()
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    """初始化配置文件"""
    skill_name = args.skill

    if not has_skill(skill_name):
        print_error(f"技能 '{skill_name}' 不存在")
        return 1

    skill = get_skill(skill_name)
    output_path = args.output or f"{skill_name}.yaml"

    # 交互式模式
    if args.interactive:
        config = InteractiveConfigBuilder.build(skill_name, skill.get_default_config())

        # 保存配置
        import yaml
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        print_success(f"配置文件已创建: {output_path}")
        return 0

    # 模板模式
    try:
        path = ConfigGenerator.generate(skill_name, output_path)
        print_success(f"配置文件已创建: {path}")
        print_info(f"编辑此文件后运行: python -m skills run --config {path}")
        return 0
    except Exception as e:
        print_error(f"创建配置文件失败: {e}")
        return 1


def cmd_run(args: argparse.Namespace) -> int:
    """运行技能"""
    config_path = args.config

    # 加载配置
    try:
        config = ConfigLoader.load(config_path)
    except FileNotFoundError as e:
        print_error(f"配置加载失败: {e}")
        return 1
    except Exception as e:
        print_error(f"配置解析失败: {e}")
        return 1

    # 获取技能
    skill_name = config.get("skill")
    if not skill_name:
        print_error("配置缺少 'skill' 字段")
        return 1

    if not has_skill(skill_name):
        print_error(f"技能 '{skill_name}' 不存在")
        print_info(f"可用技能: {', '.join(s.name for s in list_skills())}")
        return 1

    skill = get_skill(skill_name)

    # 验证配置
    print_info(f"正在验证配置...")
    validation = skill.validate(config)
    if not validation.valid:
        print_error("配置验证失败:")
        for error in validation.errors:
            print(f"  - {error}")
        return 1

    if validation.warnings:
        print_warning("配置警告:")
        for warning in validation.warnings:
            print(f"  - {warning}")

    # 执行技能
    print_info(f"开始执行技能: {skill_name}")
    print("-" * 60)

    try:
        result = skill.run(config)
        return _handle_result(result, args)
    except KeyboardInterrupt:
        print_error("\n用户中断执行")
        return 130
    except Exception as e:
        print_error(f"执行失败: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def _handle_result(result: SkillResult, args: argparse.Namespace) -> int:
    """处理执行结果"""
    print()
    print("=" * 60)

    if result.success:
        print_success(f"技能执行成功: {result.skill_name}")
    else:
        print_error(f"技能执行失败: {result.skill_name}")

    print(f"耗时: {result.duration:.2f}s")

    if result.error:
        print_error(f"错误: {result.error}")

    # 输出产物
    if result.artifacts:
        print(f"\n输出文件:")
        for artifact in result.artifacts:
            print(f"  - {artifact.path} ({artifact.type})")
            if artifact.description:
                print(f"    {artifact.description}")

    # 指标
    if result.metrics:
        print(f"\n执行指标:")
        for key, value in result.metrics.items():
            print(f"  {key}: {value}")

    # 详细日志
    if args.verbose and result.logs:
        print(f"\n执行日志:")
        for log in result.logs:
            print(f"  [{log.level}] {log.message}")

    print()
    return 0 if result.success else 1


def cmd_validate(args: argparse.Namespace) -> int:
    """验证配置文件"""
    config_path = args.config

    try:
        config = ConfigLoader.load(config_path)
    except Exception as e:
        print_error(f"配置加载失败: {e}")
        return 1

    skill_name = config.get("skill")
    if not skill_name:
        print_error("配置缺少 'skill' 字段")
        return 1

    if not has_skill(skill_name):
        print_error(f"技能 '{skill_name}' 不存在")
        return 1

    skill = get_skill(skill_name)

    print_info(f"正在验证配置 (技能: {skill_name})...")

    validation = skill.validate(config)

    if validation.valid:
        print_success("配置验证通过 ✓")
    else:
        print_error("配置验证失败:")
        for error in validation.errors:
            print(f"  ✗ {error}")

    if validation.warnings:
        print_warning("配置警告:")
        for warning in validation.warnings:
            print(f"  ⚠ {warning}")

    return 0 if validation.valid else 1


def cmd_batch(args: argparse.Namespace) -> int:
    """批量执行"""
    config_dir = Path(args.config_dir)

    if not config_dir.exists():
        print_error(f"配置目录不存在: {config_dir}")
        return 1

    config_files = list(config_dir.glob("*.yaml")) + list(config_dir.glob("*.yml"))

    if not config_files:
        print_error(f"目录中找不到YAML配置文件: {config_dir}")
        return 1

    print_info(f"发现 {len(config_files)} 个配置")
    print()

    results = []
    for config_file in sorted(config_files):
        print(f"处理: {config_file.name}")
        print("-" * 60)

        # 创建临时args对象
        sub_args = argparse.Namespace(
            config=str(config_file),
            verbose=args.verbose
        )

        ret = cmd_run(sub_args)
        results.append((config_file.name, ret))
        print()

    # 汇总
    print("=" * 60)
    print("批量执行汇总:")
    print("-" * 60)

    success = sum(1 for _, ret in results if ret == 0)
    failed = len(results) - success

    print(f"成功: {success}")
    print(f"失败: {failed}")

    if failed > 0:
        print("\n失败项:")
        for name, ret in results:
            if ret != 0:
                print(f"  - {name} (返回码: {ret})")

    return 0 if failed == 0 else 1


def cmd_version(args: argparse.Namespace) -> int:
    """显示版本"""
    print("CloudPSS Skill System")
    print("版本: 1.0.0")
    print()
    return 0


def create_parser() -> argparse.ArgumentParser:
    """创建命令行解析器"""
    parser = argparse.ArgumentParser(
        prog="python -m skills",
        description="CloudPSS 技能系统 - 配置驱动的电力系统仿真工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 列出可用技能
  python -m skills list

  # 初始化配置
  python -m skills init emt_simulation --output my_sim.yaml

  # 运行技能
  python -m skills run --config my_sim.yaml

  # 验证配置
  python -m skills validate --config my_sim.yaml

更多信息: https://github.com/cloudpss/skills
        """
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细信息"
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # list 命令
    list_parser = subparsers.add_parser(
        "list",
        help="列出可用技能",
        aliases=["ls"]
    )
    list_parser.set_defaults(func=cmd_list)

    # describe 命令
    desc_parser = subparsers.add_parser(
        "describe",
        help="查看技能详情",
        aliases=["info", "show"]
    )
    desc_parser.add_argument("skill", help="技能名称")
    desc_parser.set_defaults(func=cmd_describe)

    # init 命令
    init_parser = subparsers.add_parser(
        "init",
        help="初始化配置文件"
    )
    init_parser.add_argument("skill", help="技能名称")
    init_parser.add_argument(
        "--output", "-o",
        help="输出文件路径"
    )
    init_parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="交互式配置"
    )
    init_parser.set_defaults(func=cmd_init)

    # run 命令
    run_parser = subparsers.add_parser(
        "run",
        help="运行技能",
        aliases=["execute", "start"]
    )
    run_parser.add_argument(
        "--config", "-c",
        required=True,
        help="配置文件路径"
    )
    run_parser.set_defaults(func=cmd_run)

    # validate 命令
    validate_parser = subparsers.add_parser(
        "validate",
        help="验证配置文件",
        aliases=["check", "verify"]
    )
    validate_parser.add_argument(
        "--config", "-c",
        required=True,
        help="配置文件路径"
    )
    validate_parser.set_defaults(func=cmd_validate)

    # batch 命令
    batch_parser = subparsers.add_parser(
        "batch",
        help="批量执行多个配置"
    )
    batch_parser.add_argument(
        "--config-dir", "-d",
        required=True,
        help="配置目录路径"
    )
    batch_parser.set_defaults(func=cmd_batch)

    # version 命令
    version_parser = subparsers.add_parser(
        "version",
        help="显示版本信息",
        aliases=["--version", "-V"]
    )
    version_parser.set_defaults(func=cmd_version)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """主入口"""
    # 自动发现技能
    auto_discover()

    # 解析命令行
    parser = create_parser()
    args = parser.parse_args(argv)

    # 没有子命令时显示帮助
    if not args.command:
        parser.print_help()
        return 0

    # 执行命令
    if hasattr(args, "func"):
        return args.func(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
