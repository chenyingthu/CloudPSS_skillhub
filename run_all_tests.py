#!/usr/bin/env python3
"""
CloudPSS Skill System - 一键测试执行脚本

使用方法:
    python run_all_tests.py           # 运行所有测试
    python run_all_tests.py --quick   # 快速测试（仅验证）
    python run_all_tests.py --full    # 完整测试（需token）
"""

import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime


def run_command(cmd, description, timeout=60):
    """运行命令并显示结果"""
    print(f"\n{'='*70}")
    print(f"▶ {description}")
    print(f"{'='*70}")
    print(f"命令: {cmd}\n")

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        if result.stdout:
            print(result.stdout)

        if result.returncode == 0:
            print(f"\n✅ {description} - 成功")
            return True
        else:
            print(f"\n❌ {description} - 失败")
            if result.stderr:
                print(f"错误: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print(f"\n⏱️ {description} - 超时")
        return False
    except Exception as e:
        print(f"\n💥 {description} - 异常: {e}")
        return False


def test_skill_registration():
    """测试技能注册"""
    return run_command(
        "python -m cloudpss_skills list",
        "测试1: 验证所有10个技能已注册"
    )


def test_skill_descriptions():
    """测试技能描述"""
    skills = [
        "n1_security",
        "param_scan",
        "result_compare",
        "visualize",
        "topology_check",
        "batch_powerflow",
    ]

    all_passed = True
    for skill in skills:
        if not run_command(
            f"python -m cloudpss_skills describe {skill}",
            f"测试2.{skills.index(skill)+1}: 查看{skill}技能详情",
            timeout=10
        ):
            all_passed = False

    return all_passed


def test_config_generation():
    """测试配置生成"""
    Path("/tmp/skill_configs").mkdir(parents=True, exist_ok=True)

    skills = [
        "n1_security",
        "param_scan",
        "topology_check",
        "batch_powerflow",
    ]

    all_passed = True
    for skill in skills:
        if not run_command(
            f"python -m cloudpss_skills init {skill} --output /tmp/skill_configs/{skill}.yaml",
            f"测试3.{skills.index(skill)+1}: 生成{skill}配置",
            timeout=10
        ):
            all_passed = False

    return all_passed


def test_config_validation():
    """测试配置验证"""
    skills = [
        "n1_security",
        "param_scan",
        "topology_check",
        "batch_powerflow",
    ]

    all_passed = True
    for skill in skills:
        # 先生成配置
        subprocess.run(
            f"python -m cloudpss_skills init {skill} --output /tmp/skill_configs/{skill}.yaml",
            shell=True,
            capture_output=True
        )
        # 然后验证
        if not run_command(
            f"python -m cloudpss_skills validate --config /tmp/skill_configs/{skill}.yaml",
            f"测试4.{skills.index(skill)+1}: 验证{skill}配置",
            timeout=10
        ):
            all_passed = False

    return all_passed


def test_unit_tests():
    """测试单元测试"""
    return run_command(
        "python -m pytest tests/skills/ -v --tb=short",
        "测试5: 运行单元测试套件",
        timeout=120
    )


def test_python_api():
    """测试Python API"""
    test_code = '''
import sys
sys.path.insert(0, '/home/chenying/researches/cloudpss-api-enhanced')

from cloudpss_skills.builtin import (
    N1SecuritySkill, ParamScanSkill, ResultCompareSkill,
    VisualizeSkill, TopologyCheckSkill, BatchPowerFlowSkill,
)
from cloudpss_skills.core import auto_discover, list_skills

# 测试1: 所有技能可以实例化
skills = [
    N1SecuritySkill(), ParamScanSkill(), ResultCompareSkill(),
    VisualizeSkill(), TopologyCheckSkill(), BatchPowerFlowSkill(),
]
print(f"✓ 成功实例化 {len(skills)} 个技能")

# 测试2: 技能已注册
auto_discover()
registered = list_skills()
print(f"✓ 已注册技能: {len(registered)} 个")

# 测试3: 获取默认配置
for skill in skills:
    config = skill.get_default_config()
    assert "skill" in config
    assert config["skill"] == skill.name
print(f"✓ 所有技能默认配置正确")

print("\\n✅ Python API 测试全部通过!")
'''

    # 写入临时文件并执行
    test_file = "/tmp/test_python_api.py"
    with open(test_file, 'w') as f:
        f.write(test_code)

    return run_command(
        f"python {test_file}",
        "测试6: Python API 测试",
        timeout=30
    )


def test_prompt_simulation():
    """测试提示词模拟"""
    return run_command(
        "python tests/prompt_driven_test_framework.py",
        "测试7: 提示词驱动自动化测试",
        timeout=180
    )


def main():
    parser = argparse.ArgumentParser(description='CloudPSS Skill System 测试脚本')
    parser.add_argument('--quick', action='store_true', help='快速测试（仅本地验证）')
    parser.add_argument('--full', action='store_true', help='完整测试（需token）')
    args = parser.parse_args()

    print("="*70)
    print("CloudPSS Skill System - 自动化测试套件")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    results = {}

    # 基础测试（所有模式都运行）
    results['skill_registration'] = test_skill_registration()
    results['skill_descriptions'] = test_skill_descriptions()
    results['config_generation'] = test_config_generation()
    results['config_validation'] = test_config_validation()
    results['unit_tests'] = test_unit_tests()
    results['python_api'] = test_python_api()

    # 完整测试
    if not args.quick:
        results['prompt_simulation'] = test_prompt_simulation()

    # 生成汇总
    print("\n" + "="*70)
    print("测试汇总")
    print("="*70)

    passed = sum(1 for v in results.values() if v)
    failed = sum(1 for v in results.values() if not v)
    total = len(results)

    for name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {status}: {name}")

    print(f"\n总计: {total} | 通过: {passed} | 失败: {failed}")
    print(f"通过率: {passed/total*100:.1f}%")
    print("="*70)

    # 返回状态码
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
