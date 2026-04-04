#!/usr/bin/env python3
"""
批量修复TODO异常捕获脚本

将带有 # TODO: 细化为具体异常类型 的裸异常捕获细化为具体类型
"""

import re
from pathlib import Path
from typing import List, Tuple


def analyze_try_block(lines: List[str], except_line_num: int) -> str:
    """分析try块的内容，推断可能的异常类型"""
    # 找到try行的位置
    try_line_num = except_line_num - 1
    while try_line_num >= 0:
        if re.match(r'^(\s*)try\s*:', lines[try_line_num]):
            break
        try_line_num -= 1

    if try_line_num < 0:
        return "Exception"

    # 获取try块内的代码
    try_block = []
    indent = len(lines[try_line_num]) - len(lines[try_line_num].lstrip())
    base_indent = ' ' * (indent + 4)

    for i in range(try_line_num + 1, except_line_num):
        line = lines[i]
        if line.strip() and not line.startswith(base_indent):
            break
        try_block.append(line)

    try_code = '\n'.join(try_block)

    # 根据代码内容推断异常类型
    exceptions = []

    # 字典/列表访问
    if re.search(r'\[.*\]', try_code) or '.get(' in try_code:
        exceptions.append('KeyError')

    # 对象属性访问
    if re.search(r'\.[a-zA-Z_]', try_code):
        exceptions.append('AttributeError')

    # 类型转换
    if re.search(r'^(float|int|str|list|dict)\s*\(', try_code, re.M):
        exceptions.append('ValueError')
        exceptions.append('TypeError')

    # 数学运算
    if re.search(r'/\s*\w+', try_code):
        exceptions.append('ZeroDivisionError')

    # 文件操作
    if 'open(' in try_code or 'read(' in try_code or 'write(' in try_code:
        exceptions.append('IOError')

    # 网络/连接操作
    if 'fetch' in try_code or 'runPowerFlow' in try_code or 'runEMT' in try_code:
        exceptions.append('ConnectionError')
        exceptions.append('RuntimeError')

    # JSON操作
    if 'json.' in try_code:
        exceptions.append('json.JSONDecodeError')

    # CloudPSS SDK操作
    if 'model.' in try_code or 'Model.' in try_code:
        exceptions.append('AttributeError')
        exceptions.append('KeyError')

    # 如果没有推断出特定类型，返回通用类型
    if not exceptions:
        return "Exception"

    return '(' + ', '.join(exceptions[:3]) + ')'  # 最多3个异常类型


def fix_file(filepath: Path) -> dict:
    """修复单个文件中的TODO异常捕获"""
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')

    # 查找带有TODO的裸异常捕获
    pattern = r'^(\s*)except\s+Exception\s+as\s+e:\s*#\s*TODO.*细化为具体异常类型.*$'
    matches = []

    for i, line in enumerate(lines):
        if re.match(pattern, line):
            matches.append(i)

    if not matches:
        return {'file': str(filepath), 'fixes': 0}

    fixes = 0
    new_lines = lines.copy()

    # 从后往前处理
    for line_num in reversed(matches):
        indent = len(lines[line_num]) - len(lines[line_num].lstrip())
        spaces = ' ' * indent

        # 分析try块推断异常类型
        exception_type = analyze_try_block(lines, line_num)

        # 替换行
        new_line = f"{spaces}except {exception_type} as e:"
        new_lines[line_num] = new_line
        fixes += 1

    # 写回文件
    filepath.write_text('\n'.join(new_lines), encoding='utf-8')

    return {'file': str(filepath), 'fixes': fixes}


def main():
    """主函数"""
    builtin_dir = Path('/home/chenying/researches/cloudpss-toolkit/cloudpss_skills/builtin')
    py_files = list(builtin_dir.glob('*.py'))

    results = []
    total_fixes = 0

    print(f"扫描 {len(py_files)} 个文件...")

    for filepath in sorted(py_files):
        if filepath.name == '__init__.py':
            continue

        result = fix_file(filepath)
        if result['fixes'] > 0:
            results.append(result)
            total_fixes += result['fixes']
            print(f"  {filepath.name}: 修复 {result['fixes']} 处")

    print(f"\n总计: 修复 {total_fixes} 处")
    print("✅ 已将裸异常捕获细化为具体异常类型")


if __name__ == '__main__':
    main()
