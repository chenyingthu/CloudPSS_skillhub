"""
元数据管理 CLI 工具

提供命令行接口用于组件元数据的提取、管理和查询。

用法:
    python -m cloudpss_skills.metadata.cli extract <doc_path> [--output <output_path>]
    python -m cloudpss_skills.metadata.cli validate <metadata_file>
    python -m cloudpss_skills.metadata.cli list [--category <category>]
    python -m cloudpss_skills.metadata.cli show <component_id>
    python -m cloudpss_skills.metadata.cli batch <directory> [--pattern <pattern>] [--output <output_path>]
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Optional

from .parser import ComponentDocumentParser, BatchMetadataExtractor
from .registry import get_registry, reset_registry
from .models import ComponentMetadata

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def cmd_extract(args):
    """从文档提取元数据"""
    parser = ComponentDocumentParser()

    if not Path(args.doc_path).exists():
        logger.error(f"文档不存在: {args.doc_path}")
        return 1

    result = parser.parse_file(args.doc_path)

    if not result.success:
        logger.error("解析失败:")
        for error in result.errors:
            logger.error(f"  - {error}")
        return 1

    metadata = result.metadata

    # 输出结果
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata.to_dict(), f, ensure_ascii=False, indent=2)
        logger.info(f"元数据已保存到: {output_path}")
    else:
        print(json.dumps(metadata.to_dict(), ensure_ascii=False, indent=2))

    # 输出警告
    if result.warnings:
        logger.warning("警告:")
        for warning in result.warnings:
            logger.warning(f"  - {warning}")

    # 输出摘要
    print(f"\n{metadata.get_summary()}")
    return 0


def cmd_validate(args):
    """验证元数据文件"""
    if not Path(args.metadata_file).exists():
        logger.error(f"文件不存在: {args.metadata_file}")
        return 1

    try:
        with open(args.metadata_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 处理包含components字段的情况
        if 'components' in data:
            components = data['components']
        elif isinstance(data, list):
            components = data
        else:
            components = [data]

        valid_count = 0
        for i, comp_data in enumerate(components):
            try:
                metadata = ComponentMetadata.from_dict(comp_data)

                # 基本验证
                errors = []
                if not metadata.component_id:
                    errors.append("缺少 component_id")
                if not metadata.name:
                    errors.append("缺少 name")
                if not metadata.parameter_groups:
                    errors.append("没有参数组")

                if errors:
                    logger.error(f"组件 {i+1} ({metadata.component_id}): 验证失败")
                    for error in errors:
                        logger.error(f"  - {error}")
                else:
                    valid_count += 1
                    logger.info(f"组件 {i+1} ({metadata.component_id}): 验证通过")

            except Exception as e:
                logger.error(f"组件 {i+1}: 解析失败 - {e}")

        logger.info(f"\n验证完成: {valid_count}/{len(components)} 个组件通过")
        return 0 if valid_count == len(components) else 1

    except json.JSONDecodeError as e:
        logger.error(f"JSON解析失败: {e}")
        return 1
    except Exception as e:
        logger.error(f"验证失败: {e}")
        return 1


def cmd_list(args):
    """列出已注册的组件"""
    registry = get_registry()

    # 尝试加载元数据目录
    if args.metadata_dir:
        registry.load_from_directory(args.metadata_dir)

    if args.category:
        components = registry.list_components(category=args.category)
        logger.info(f"类别 '{args.category}' 的组件:")
    else:
        components = registry.list_components()
        logger.info("所有组件:")

    if not components:
        logger.info("  (无)")
        return 0

    for comp_id in components:
        metadata = registry.get_component(comp_id)
        if metadata:
            print(f"  - {comp_id}: {metadata.name}")
        else:
            print(f"  - {comp_id}")

    logger.info(f"\n共 {len(components)} 个组件")
    return 0


def cmd_show(args):
    """显示组件详细信息"""
    registry = get_registry()

    # 尝试加载元数据目录
    if args.metadata_dir:
        registry.load_from_directory(args.metadata_dir)

    metadata = registry.get_component(args.component_id)
    if not metadata:
        logger.error(f"组件未找到: {args.component_id}")
        return 1

    print(f"\n{'='*60}")
    print(f"组件: {metadata.name}")
    print(f"{'='*60}")
    print(f"\nID: {metadata.component_id}")
    print(f"版本: {metadata.version}")
    if metadata.category:
        print(f"类别: {metadata.category}")
    if metadata.description:
        print(f"描述: {metadata.description}")

    # 参数信息
    all_params = metadata.get_all_parameters()
    if all_params:
        print(f"\n参数 ({len(all_params)}个):")
        for group in metadata.parameter_groups:
            print(f"\n  [{group.name}]")
            for param in group.parameters:
                required = "*" if param.required else ""
                default = f" (默认: {param.default})" if param.default is not None else ""
                print(f"    - {param.key}{required}: {param.display_name} [{param.type}]{default}")

        required_params = metadata.get_required_parameters()
        if required_params:
            print(f"\n  必需参数: {len(required_params)}个")

    # 引脚信息
    all_pins = metadata.get_all_pins()
    if all_pins:
        print(f"\n引脚 ({len(all_pins)}个):")
        for pin_type, pins in metadata.pins.items():
            if pins:
                print(f"\n  [{pin_type}]")
                for pin in pins:
                    required = "*" if pin.required else ""
                    print(f"    - {pin.key}{required}: {pin.name} [{pin.dimension}]")

    print(f"\n{'='*60}\n")
    return 0


def cmd_batch(args):
    """批量提取元数据"""
    extractor = BatchMetadataExtractor()

    directory = Path(args.directory)
    if not directory.exists():
        logger.error(f"目录不存在: {directory}")
        return 1

    results = extractor.extract_from_directory(directory, args.pattern)
    summary = extractor.get_summary()

    logger.info(f"\n提取结果:")
    logger.info(f"  总计: {summary['total']}")
    logger.info(f"  成功: {summary['successful']}")
    logger.info(f"  失败: {summary['failed']}")
    logger.info(f"  成功率: {summary['success_rate']*100:.1f}%")

    if summary['failed_files']:
        logger.error(f"\n失败的文件:")
        for filename in summary['failed_files']:
            errors = extractor.results[filename].errors
            logger.error(f"  - {filename}: {errors}")

    # 保存成功的结果
    successful = extractor.get_successful_results()
    if successful and args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            'components': [m.to_dict() for m in successful.values()]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"\n元数据已保存到: {output_path}")

    return 0 if summary['success_rate'] == 1.0 else 1


def main(argv: Optional[list] = None) -> int:
    """主入口"""
    parser = argparse.ArgumentParser(
        description='CloudPSS 组件元数据管理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s extract docs/wgsource.md --output wgsource.json
  %(prog)s validate wgsource.json
  %(prog)s list --metadata-dir ./metadata
  %(prog)s show model/CloudPSS/WGSource --metadata-dir ./metadata
  %(prog)s batch ./docs --pattern "*.md" --output components.json
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # extract 命令
    extract_parser = subparsers.add_parser('extract', help='从文档提取元数据')
    extract_parser.add_argument('doc_path', help='文档路径')
    extract_parser.add_argument('-o', '--output', help='输出文件路径')
    extract_parser.set_defaults(func=cmd_extract)

    # validate 命令
    validate_parser = subparsers.add_parser('validate', help='验证元数据文件')
    validate_parser.add_argument('metadata_file', help='元数据文件路径')
    validate_parser.set_defaults(func=cmd_validate)

    # list 命令
    list_parser = subparsers.add_parser('list', help='列出已注册的组件')
    list_parser.add_argument('-c', '--category', help='按类别过滤')
    list_parser.add_argument('-d', '--metadata-dir', help='元数据目录')
    list_parser.set_defaults(func=cmd_list)

    # show 命令
    show_parser = subparsers.add_parser('show', help='显示组件详细信息')
    show_parser.add_argument('component_id', help='组件ID')
    show_parser.add_argument('-d', '--metadata-dir', help='元数据目录')
    show_parser.set_defaults(func=cmd_show)

    # batch 命令
    batch_parser = subparsers.add_parser('batch', help='批量提取元数据')
    batch_parser.add_argument('directory', help='文档目录')
    batch_parser.add_argument('-p', '--pattern', default='*.md', help='文件匹配模式')
    batch_parser.add_argument('-o', '--output', help='输出文件路径')
    batch_parser.set_defaults(func=cmd_batch)

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
