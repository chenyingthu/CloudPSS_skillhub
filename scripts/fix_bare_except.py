#!/usr/bin/env python3
"""
修复bare except语句

将except: 替换为 except Exception as e:
"""

import re
from pathlib import Path


def fix_file(filepath: Path) -> dict:
    """修复单个文件中的bare except"""
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')

    fixes = 0
    new_lines = []

    for line in lines:
        # 匹配bare except（后面跟冒号）
        if re.match(r'^(\s*)except\s*:\s*$', line):
            indent = len(line) - len(line.lstrip())
            spaces = ' ' * indent
            # 替换为具体的异常捕获
            new_lines.append(f"{spaces}except Exception as e:")
            fixes += 1
        else:
            new_lines.append(line)

    # 写回文件
    if fixes > 0:
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

    print(f"\n总计: 修复 {total_fixes} 处 bare except")


if __name__ == '__main__':
    main()
