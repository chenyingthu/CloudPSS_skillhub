#!/usr/bin/env python3
"""
CloudPSS Skill System - 技能配置验证脚本

验证所有技能的默认配置是否可通过验证。
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 必须先导入builtin模块触发技能注册
from cloudpss_skills import builtin  # noqa: F401
from cloudpss_skills.core import list_skills, get_skill


def validate_all_skills():
    """验证所有技能的默认配置"""
    print("=" * 70)
    print("CloudPSS Skill System - 配置验证")
    print("=" * 70)

    skill_list = list_skills()
    total = len(skill_list)

    passed = 0
    failed = 0
    results = []

    for skill in skill_list:
        skill_name = skill.name

        # 获取默认配置
        config = skill.get_default_config()

        # 验证
        result = skill.validate(config)

        if result.valid:
            passed += 1
            status = "✓"
        else:
            failed += 1
            status = "✗"

        results.append({
            "name": skill_name,
            "valid": result.valid,
            "errors": result.errors,
            "warnings": result.warnings,
        })

        # 打印结果
        print(f"\n[{status}] {skill_name}")
        if not result.valid:
            for error in result.errors:
                print(f"    ✗ {error}")
        if result.warnings:
            for warning in result.warnings:
                print(f"    ⚠ {warning}")

    # 汇总
    print("\n" + "=" * 70)
    print(f"总计: {total} | 通过: {passed} ✓ | 失败: {failed} ✗")
    print(f"通过率: {passed/total*100:.1f}%")
    print("=" * 70)

    # 分类说明
    if failed > 0:
        print("\n说明:")
        print("  • 失败的技能需要用户提供特定参数才能运行")
        print("  • 这是预期行为，因为这些技能需要用户输入")
        print("  • 使用 'python -m cloudpss_skills describe <skill>' 查看配置要求")
        print("  • 运行 'python -m cloudpss_skills init <skill>' 生成配置文件模板")

    return failed == 0


if __name__ == "__main__":
    success = validate_all_skills()
    sys.exit(0 if success else 1)
