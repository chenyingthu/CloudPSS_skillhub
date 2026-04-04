#!/usr/bin/env python3
"""
批量修复裸异常捕获脚本

自动修复 except Exception as e: 为捕获特定异常类型
"""

import re
from pathlib import Path
from typing import List, Tuple


def find_bare_exceptions(content: str) -> List[Tuple[int, str]]:
    """查找所有裸异常捕获的行"""
    lines = content.split('\n')
    matches = []
    for i, line in enumerate(lines, 1):
        if re.match(r'^(\s*)except\s+Exception\s+as\s+e\s*:', line):
            matches.append((i, line))
    return matches


def analyze_context(lines: List[str], line_num: int) -> dict:
    """分析异常捕获的上下文，判断类型"""
    # 获取前几行来判断try块的内容
    start_line = max(0, line_num - 10)
    context = '\n'.join(lines[start_line:line_num])

    result = {
        'is_top_level': line_num < 5 or 'def run(' in context or 'def execute(' in context,
        'has_sdk_call': 'Model.' in context or 'model.' in context or 'CloudPSS' in context,
        'has_re_raise': 'raise' in lines[line_num:line_num+3] if line_num < len(lines) else False,
        'suggested_exception': 'Exception'  # 默认
    }

    # 根据上下文推断异常类型
    if 'fetchTopology' in context or 'fetch' in context:
        result['suggested_exception'] = '(KeyError, AttributeError)'
    elif 'updateComponent' in context or 'addComponent' in context:
        result['suggested_exception'] = '(AttributeError, TypeError)'
    elif 'runPowerFlow' in context or 'runEMT' in context:
        result['suggested_exception'] = '(RuntimeError, ConnectionError)'
    elif 'open(' in context or 'read()' in context or 'write()' in context:
        result['suggested_exception'] = 'IOError'
    elif 'import' in context:
        result['suggested_exception'] = 'ImportError'
    elif result['has_re_raise']:
        result['suggested_exception'] = 'Exception'  # 会重新抛出，保留原样
        result['keep_bare'] = True

    return result


def fix_file(filepath: Path) -> dict:
    """修复单个文件中的裸异常捕获"""
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')

    matches = find_bare_exceptions(content)
    if not matches:
        return {'file': str(filepath), 'fixes': 0, 'skipped': 0}

    fixes = 0
    skipped = 0
    new_lines = lines.copy()

    # 从后往前处理，避免行号变化
    for line_num, original_line in reversed(matches):
        context = analyze_context(lines, line_num - 1)
        indent = len(original_line) - len(original_line.lstrip())
        spaces = ' ' * indent

        if context.get('keep_bare'):
            skipped += 1
            continue

        # 构建替换的异常类型
        exception_type = context['suggested_exception']

        if exception_type == 'Exception':
            # 无法确定具体类型，保留但添加注释
            new_line = f"{spaces}except Exception as e:  # TODO: 细化为具体异常类型"
        else:
            new_line = f"{spaces}except {exception_type} as e:"

        new_lines[line_num - 1] = new_line
        fixes += 1

    # 写回文件
    filepath.write_text('\n'.join(new_lines), encoding='utf-8')

    return {
        'file': str(filepath),
        'fixes': fixes,
        'skipped': skipped,
        'total': len(matches)
    }


def main():
    """主函数"""
    builtin_dir = Path('/home/chenying/researches/cloudpss-toolkit/cloudpss_skills/builtin')
    py_files = list(builtin_dir.glob('*.py'))

    results = []
    total_fixes = 0
    total_skipped = 0

    print(f"扫描 {len(py_files)} 个文件...")

    for filepath in sorted(py_files):
        if filepath.name == '__init__.py':
            continue

        result = fix_file(filepath)
        if result['total'] > 0:
            results.append(result)
            total_fixes += result['fixes']
            total_skipped += result['skipped']
            print(f"  {filepath.name}: 修复 {result['fixes']}/{result['total']}, 跳过 {result['skipped']}")

    print(f"\n总计: 修复 {total_fixes} 处, 跳过 {total_skipped} 处")
    print("注意: 部分修复使用了推断的异常类型，建议人工复查")


if __name__ == '__main__':
    main()
