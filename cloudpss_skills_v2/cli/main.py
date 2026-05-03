"""CloudPSS Skills V2 CLI - Main Entry Point.

提供命令行解析和命令分发功能。
"""

import argparse
import logging
import sys
from typing import List, Optional

# Import commands
from cloudpss_skills_v2.cli.commands import list_cmd

# Setup logging
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


def create_parser() -> argparse.ArgumentParser:
    """创建命令行解析器

    Returns:
        argparse.ArgumentParser: 配置好的解析器
    """
    parser = argparse.ArgumentParser(
        prog="python -m cloudpss_skills_v2",
        description="CloudPSS Skills V2 - 电力系统仿真技能框架",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 列出可用技能
  python -m cloudpss_skills_v2 list

  # 运行技能
  python -m cloudpss_skills_v2 run --config config.yaml

  # 对比多个配置结果
  python -m cloudpss_skills_v2 compare --configs a.yaml b.yaml

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
    list_parser.add_argument(
        "--category", "-c",
        help="按类别过滤 (tool/poweranalysis/simulation)"
    )
    list_parser.set_defaults(func=list_cmd.cmd_list)

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
    run_parser.add_argument(
        "--output", "-o",
        help="输出目录路径"
    )
    run_parser.set_defaults(func=_cmd_run_placeholder)

    # compare 命令
    compare_parser = subparsers.add_parser(
        "compare",
        help="跨引擎对比分析结果",
        description="Run the same analysis on multiple engines and compare results.",
        aliases=["diff"]
    )
    compare_parser.add_argument(
        "--configs", "-c",
        nargs="+",
        required=True,
        help="配置文件路径列表"
    )
    compare_parser.add_argument(
        "--output", "-o",
        help="对比报告输出路径"
    )
    compare_parser.set_defaults(func=_cmd_compare_placeholder)

    # version 命令
    version_parser = subparsers.add_parser(
        "version",
        help="显示版本信息",
        aliases=["--version", "-V"]
    )
    version_parser.set_defaults(func=_cmd_version)

    return parser


def _cmd_run_placeholder(args: argparse.Namespace) -> int:
    """运行技能（占位符实现）"""
    print_info("运行技能功能将在 Task 2 中实现")
    print_info(f"配置文件: {args.config}")
    if args.output:
        print_info(f"输出目录: {args.output}")
    return 0


def _cmd_version(args: argparse.Namespace) -> int:
    """显示版本信息"""
    from cloudpss_skills_v2 import __version__
    print(f"CloudPSS Skills V2")
    print(f"版本: {__version__}")
    print()
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    """CLI主入口

    Args:
        argv: 命令行参数列表，默认为sys.argv

    Returns:
        int: 退出码
    """
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
