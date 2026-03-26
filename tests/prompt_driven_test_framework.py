"""
CloudPSS Skill System - 提示词驱动自动化测试框架

模拟真实用户使用自然语言提示词与Claude Code交互的场景
"""

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class TestStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class PromptStyle(Enum):
    DETAILED = "detailed"      # 用户给出详细明确的指令
    CONCISE = "concise"        # 用户给出简洁指令
    VAGUE = "vague"            # 用户给出模糊指令
    CONVERSATIONAL = "conversational"  # 对话式指令


@dataclass
class TestCase:
    """测试用例"""
    id: str
    category: str
    name: str
    prompt_style: PromptStyle
    prompt: str
    expected_skill: Optional[str] = None
    expected_actions: List[str] = field(default_factory=list)
    setup_commands: List[str] = field(default_factory=list)
    cleanup_commands: List[str] = field(default_factory=list)
    requires_token: bool = False
    notes: str = ""


@dataclass
class TestResult:
    """测试结果"""
    test_case: TestCase
    status: TestStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    output: str = ""
    error: str = ""
    issues: List[Dict[str, Any]] = field(default_factory=list)
    observations: List[str] = field(default_factory=list)
    execution_time: float = 0.0


@dataclass
class TestReport:
    """测试报告"""
    start_time: datetime
    end_time: Optional[datetime] = None
    results: List[TestResult] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)


class PromptDrivenTestFramework:
    """提示词驱动测试框架"""

    def __init__(self, output_dir: str = "./test_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.report = TestReport(start_time=datetime.now())
        self.test_cases = []

    def add_test_case(self, test_case: TestCase):
        """添加测试用例"""
        self.test_cases.append(test_case)

    def run_shell_command(self, command: str, timeout: int = 60) -> Tuple[int, str, str]:
        """运行shell命令，返回(返回码, stdout, stderr)"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)

    def execute_test(self, test_case: TestCase) -> TestResult:
        """执行单个测试用例"""
        result = TestResult(
            test_case=test_case,
            status=TestStatus.RUNNING,
            start_time=datetime.now()
        )

        print(f"\n{'='*70}")
        print(f"执行测试: [{test_case.id}] {test_case.name}")
        print(f"提示词风格: {test_case.prompt_style.value}")
        print(f"{'='*70}")

        try:
            # 1. 执行前置命令
            if test_case.setup_commands:
                print("执行前置设置...")
                for cmd in test_case.setup_commands:
                    rc, out, err = self.run_shell_command(cmd)
                    if rc != 0:
                        result.issues.append({
                            "type": "setup_error",
                            "command": cmd,
                            "error": err
                        })

            # 2. 模拟用户提示词交互
            print(f"\n[用户提示词]\n{test_case.prompt}\n")

            # 3. 执行实际的技能调用（这里模拟Agent的响应）
            skill_output = self.simulate_agent_response(test_case)
            result.output = skill_output

            # 4. 验证结果
            success, validation_issues = self.validate_result(test_case, skill_output)
            result.status = TestStatus.PASSED if success else TestStatus.FAILED
            result.issues.extend(validation_issues)

            # 5. 执行清理命令
            if test_case.cleanup_commands:
                print("\n执行清理...")
                for cmd in test_case.cleanup_commands:
                    self.run_shell_command(cmd)

        except Exception as e:
            result.status = TestStatus.FAILED
            result.error = str(e)
            result.issues.append({
                "type": "execution_error",
                "error": str(e)
            })

        result.end_time = datetime.now()
        result.execution_time = (result.end_time - result.start_time).total_seconds()

        # 打印结果
        status_icon = "✓" if result.status == TestStatus.PASSED else "✗"
        print(f"\n[{status_icon}] 测试结果: {result.status.value}")
        if result.issues:
            print(f"发现问题: {len(result.issues)} 个")

        return result

    def simulate_agent_response(self, test_case: TestCase) -> str:
        """模拟Agent对用户提示词的响应"""
        # 这里实际应该调用Claude Code的API或模拟Agent行为
        # 目前先用简单的关键词匹配来模拟

        output_lines = []
        output_lines.append(f"[Agent响应模拟]")
        output_lines.append(f"识别到用户意图: {test_case.category}")

        if test_case.expected_skill:
            output_lines.append(f"匹配技能: {test_case.expected_skill}")

            # 尝试执行实际的技能命令
            if "list" in test_case.expected_actions:
                rc, out, err = self.run_shell_command("python -m cloudpss_skills list")
                output_lines.append(f"\n[技能列表输出]\n{out}")

            elif "describe" in test_case.expected_actions:
                skill = test_case.expected_skill
                rc, out, err = self.run_shell_command(f"python -m cloudpss_skills describe {skill}")
                output_lines.append(f"\n[技能详情输出]\n{out[:500]}...")

            elif "init" in test_case.expected_actions:
                skill = test_case.expected_skill
                output_file = f"/tmp/test_{skill}.yaml"
                rc, out, err = self.run_shell_command(
                    f"python -m cloudpss_skills init {skill} --output {output_file}"
                )
                output_lines.append(f"\n[配置生成输出]\n{out}")

            elif "validate" in test_case.expected_actions:
                skill = test_case.expected_skill
                config_file = f"/tmp/test_{skill}.yaml"
                rc, out, err = self.run_shell_command(
                    f"python -m cloudpss_skills validate --config {config_file}"
                )
                output_lines.append(f"\n[配置验证输出]\n{out}")

        return "\n".join(output_lines)

    def validate_result(self, test_case: TestCase, output: str) -> Tuple[bool, List[Dict]]:
        """验证测试结果"""
        issues = []
        success = True  # 初始为True，发现问题设为False

        # 1. 检查是否包含预期技能名称
        if test_case.expected_skill:
            if test_case.expected_skill not in output:
                issues.append({
                    "type": "missing_skill_reference",
                    "expected": test_case.expected_skill,
                    "message": f"输出中未找到技能引用: {test_case.expected_skill}"
                })
                success = False  # 关键修复：设为失败

        # 2. 检查错误信息 - 更严格的检查
        error_indicators = ["[ERROR]", "[验证状态] FAILED", "配置验证失败", "Error:", "Traceback"]
        if any(indicator in output for indicator in error_indicators):
            issues.append({
                "type": "error_in_output",
                "message": "输出中包含错误信息"
            })
            success = False  # 关键修复：设为失败

        # 3. 检查是否有预期动作 - 关键修复
        for action in test_case.expected_actions:
            action_executed = False

            # 根据动作类型检查执行证据
            if action == "list" and ("可用技能" in output or "[技能列表输出]" in output):
                action_executed = True
            elif action == "describe" and ("技能详情" in output or "[技能详情输出]" in output):
                action_executed = True
            elif action == "init" and ("[OK] 配置文件已创建" in output or "配置文件已创建" in output):
                action_executed = True
            elif action == "validate" and "[配置验证输出]" in output:
                action_executed = True
            elif action == "run" and "[执行输出]" in output:
                action_executed = True
            elif action in output.lower():
                action_executed = True

            if not action_executed:
                issues.append({
                    "type": "missing_action",
                    "expected": action,
                    "message": f"未执行预期动作: {action}"
                })
                success = False  # 关键修复：missing_action导致测试失败

        return success, issues

    def run_all_tests(self):
        """运行所有测试"""
        print("="*70)
        print("开始提示词驱动自动化测试")
        print(f"测试用例数: {len(self.test_cases)}")
        print(f"开始时间: {self.report.start_time}")
        print("="*70)

        for test_case in self.test_cases:
            result = self.execute_test(test_case)
            self.report.results.append(result)

        self.report.end_time = datetime.now()
        self.generate_report()

    def generate_report(self):
        """生成测试报告"""
        total = len(self.report.results)
        passed = sum(1 for r in self.report.results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in self.report.results if r.status == TestStatus.FAILED)
        skipped = sum(1 for r in self.report.results if r.status == TestStatus.SKIPPED)

        self.report.summary = {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_rate": passed / total if total > 0 else 0,
            "total_execution_time": sum(r.execution_time for r in self.report.results),
            "start_time": self.report.start_time.isoformat(),
            "end_time": self.report.end_time.isoformat() if self.report.end_time else None,
        }

        # 生成详细报告
        report_file = self.output_dir / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                "summary": self.report.summary,
                "results": [
                    {
                        "test_id": r.test_case.id,
                        "name": r.test_case.name,
                        "category": r.test_case.category,
                        "prompt_style": r.test_case.prompt_style.value,
                        "status": r.status.value,
                        "execution_time": r.execution_time,
                        "output": r.output,
                        "error": r.error,
                        "issues": r.issues,
                        "observations": r.observations,
                    }
                    for r in self.report.results
                ]
            }, f, indent=2, ensure_ascii=False)

        # 生成Markdown报告
        md_file = self.output_dir / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        self.generate_markdown_report(md_file)

        print(f"\n{'='*70}")
        print("测试报告生成完成:")
        print(f"  JSON: {report_file}")
        print(f"  Markdown: {md_file}")
        print(f"\n汇总:")
        print(f"  总计: {total}")
        print(f"  通过: {passed} ✓")
        print(f"  失败: {failed} ✗")
        print(f"  跳过: {skipped} -")
        print(f"  通过率: {self.report.summary['pass_rate']*100:.1f}%")
        print(f"  总耗时: {self.report.summary['total_execution_time']:.2f}s")
        print(f"{'='*70}")

    def generate_markdown_report(self, filepath: Path):
        """生成Markdown格式的测试报告"""
        lines = [
            "# CloudPSS Skill System - 提示词驱动测试报告",
            "",
            f"**测试时间**: {self.report.start_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**总耗时**: {self.report.summary['total_execution_time']:.2f}s",
            "",
            "## 汇总",
            "",
            f"| 指标 | 数值 |",
            f"|------|------|",
            f"| 总测试数 | {self.report.summary['total']} |",
            f"| 通过 | {self.report.summary['passed']} ✓ |",
            f"| 失败 | {self.report.summary['failed']} ✗ |",
            f"| 跳过 | {self.report.summary['skipped']} - |",
            f"| 通过率 | {self.report.summary['pass_rate']*100:.1f}% |",
            "",
            "## 详细结果",
            "",
        ]

        # 按分类分组
        categories = {}
        for result in self.report.results:
            cat = result.test_case.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(result)

        for category, results in sorted(categories.items()):
            lines.append(f"### {category}")
            lines.append("")

            for result in results:
                status_icon = "✓" if result.status == TestStatus.PASSED else "✗" if result.status == TestStatus.FAILED else "-"
                lines.append(f"#### [{status_icon}] {result.test_case.id}: {result.test_case.name}")
                lines.append("")
                lines.append(f"- **提示词风格**: {result.test_case.prompt_style.value}")
                lines.append(f"- **状态**: {result.status.value}")
                lines.append(f"- **耗时**: {result.execution_time:.2f}s")
                lines.append("")

                lines.append("**用户提示词**:")
                lines.append("```")
                lines.append(result.test_case.prompt)
                lines.append("```")
                lines.append("")

                if result.issues:
                    lines.append("**发现的问题**:")
                    for issue in result.issues:
                        lines.append(f"- ⚠️ {issue['type']}: {issue.get('message', '')}")
                    lines.append("")

                lines.append("---")
                lines.append("")

        # 问题汇总
        lines.append("## 问题汇总")
        lines.append("")

        all_issues = []
        for result in self.report.results:
            for issue in result.issues:
                all_issues.append({
                    "test_id": result.test_case.id,
                    "test_name": result.test_case.name,
                    **issue
                })

        if all_issues:
            lines.append("| 测试ID | 问题类型 | 描述 |")
            lines.append("|--------|----------|------|")
            for issue in all_issues:
                lines.append(f"| {issue['test_id']} | {issue['type']} | {issue.get('message', '')} |")
        else:
            lines.append("未发现任何问题。")

        lines.append("")
        lines.append("## 改进建议")
        lines.append("")

        # 根据问题生成改进建议
        issue_types = set(i['type'] for i in all_issues)
        if 'missing_skill_reference' in issue_types:
            lines.append("1. **技能识别**: 需要改进Agent识别用户意图并匹配技能的能力")
        if 'error_in_output' in issue_types:
            lines.append("2. **错误处理**: 需要增强错误处理和用户友好的错误提示")
        if 'missing_action' in issue_types:
            lines.append("3. **动作执行**: 确保Agent执行用户期望的所有动作")

        filepath.write_text("\n".join(lines), encoding='utf-8')


def create_test_suite() -> List[TestCase]:
    """创建完整的测试套件"""
    tests = []

    # ============ 类别1: 技能发现与查询 ============
    tests.append(TestCase(
        id="T001",
        category="技能发现与查询",
        name="列出所有技能（简洁提示）",
        prompt_style=PromptStyle.CONCISE,
        prompt="列出所有可用的技能",
        expected_skill=None,
        expected_actions=["list"],
        notes="测试简洁提示词是否能触发技能列表"
    ))

    tests.append(TestCase(
        id="T002",
        category="技能发现与查询",
        name="列出所有技能（详细提示）",
        prompt_style=PromptStyle.DETAILED,
        prompt="请列出CloudPSS技能系统中所有可用的技能，并显示它们的描述和版本信息",
        expected_skill=None,
        expected_actions=["list", "describe"],
        notes="测试详细提示词是否能获取更完整信息"
    ))

    tests.append(TestCase(
        id="T003",
        category="技能发现与查询",
        name="查看特定技能详情（对话式）",
        prompt_style=PromptStyle.CONVERSATIONAL,
        prompt="我想了解一下n1_security这个技能是做什么的，能给我详细说说吗？",
        expected_skill="n1_security",
        expected_actions=["describe"],
        notes="测试对话式提示词是否能正确识别技能并获取详情"
    ))

    tests.append(TestCase(
        id="T004",
        category="技能发现与查询",
        name="模糊查询技能（模糊提示）",
        prompt_style=PromptStyle.VAGUE,
        prompt="有没有能检查电网安全的技能？",
        expected_skill="n1_security",
        expected_actions=["list", "describe"],
        notes="测试模糊提示词是否能匹配到相关技能"
    ))

    # ============ 类别2: 配置生成 ============
    tests.append(TestCase(
        id="T005",
        category="配置生成",
        name="生成N-1安全校核配置（简洁）",
        prompt_style=PromptStyle.CONCISE,
        prompt="生成n1_security配置",
        expected_skill="n1_security",
        expected_actions=["init"],
        setup_commands=["mkdir -p /tmp/test_configs"],
        notes="测试简洁提示词生成配置"
    ))

    tests.append(TestCase(
        id="T006",
        category="配置生成",
        name="生成参数扫描配置（详细）",
        prompt_style=PromptStyle.DETAILED,
        prompt="请帮我创建一个param_scan技能的配置文件，保存到/tmp/test_configs/目录下，用于对IEEE3模型的负载进行有功功率参数扫描",
        expected_skill="param_scan",
        expected_actions=["init"],
        setup_commands=["mkdir -p /tmp/test_configs"],
        notes="测试详细提示词生成配置"
    ))

    tests.append(TestCase(
        id="T007",
        category="配置生成",
        name="批量生成多个配置（对话式）",
        prompt_style=PromptStyle.CONVERSATIONAL,
        prompt="我需要做拓扑检查和批量潮流计算，能帮我生成这两个技能的配置文件吗？",
        expected_skill="topology_check",
        expected_actions=["init"],
        notes="测试多技能配置生成请求"
    ))

    # ============ 类别3: 配置验证 ============
    tests.append(TestCase(
        id="T008",
        category="配置验证",
        name="验证拓扑检查配置（简洁）",
        prompt_style=PromptStyle.CONCISE,
        prompt="验证topology_check配置",
        expected_skill="topology_check",
        expected_actions=["validate"],
        setup_commands=["python -m cloudpss_skills init topology_check --output /tmp/test_topo.yaml"],
        notes="测试配置验证"
    ))

    tests.append(TestCase(
        id="T009",
        category="配置验证",
        name="验证并修复配置（详细）",
        prompt_style=PromptStyle.DETAILED,
        prompt="请检查我生成的batch_powerflow配置是否正确，如果有问题请指出并建议如何修复",
        expected_skill="batch_powerflow",
        expected_actions=["validate"],
        setup_commands=["python -m cloudpss_skills init batch_powerflow --output /tmp/test_batch.yaml"],
        notes="测试配置验证和问题诊断"
    ))

    # ============ 类别4: 技能执行 ============
    tests.append(TestCase(
        id="T010",
        category="技能执行",
        name="执行拓扑检查（详细提示）",
        prompt_style=PromptStyle.DETAILED,
        prompt="运行topology_check技能检查model/holdme/IEEE3模型的拓扑，启用所有检查项，结果保存到./results/目录",
        expected_skill="topology_check",
        expected_actions=["run"],
        requires_token=True,
        notes="测试实际执行技能（需要token）"
    ))

    tests.append(TestCase(
        id="T011",
        category="技能执行",
        name="批量潮流计算（对话式）",
        prompt_style=PromptStyle.CONVERSATIONAL,
        prompt="我想对IEEE3和IEEE39两个模型批量跑一下潮流计算，你能帮我设置一下吗？",
        expected_skill="batch_powerflow",
        expected_actions=["init", "run"],
        requires_token=True,
        notes="测试批量操作请求"
    ))

    # ============ 类别5: 结果分析 ============
    tests.append(TestCase(
        id="T012",
        category="结果分析",
        name="对比仿真结果（模糊提示）",
        prompt_style=PromptStyle.VAGUE,
        prompt="我有两次仿真的结果，想对比一下",
        expected_skill="result_compare",
        expected_actions=["describe", "init"],
        notes="测试结果对比意图识别"
    ))

    tests.append(TestCase(
        id="T013",
        category="结果分析",
        name="生成可视化图表（详细）",
        prompt_style=PromptStyle.DETAILED,
        prompt="使用visualize技能从最近的EMT仿真任务生成波形图，绘制Bus1_Va和Bus1_Vb通道，时间范围2-5秒，输出为PNG格式",
        expected_skill="visualize",
        expected_actions=["init", "run"],
        notes="测试可视化请求"
    ))

    # ============ 类别6: 复杂工作流 ============
    tests.append(TestCase(
        id="T014",
        category="复杂工作流",
        name="完整分析流程（详细）",
        prompt_style=PromptStyle.DETAILED,
        prompt="""请帮我完成一个完整的电力系统分析工作流：
1. 首先检查IEEE39模型的拓扑
2. 然后运行潮流计算
3. 接着做N-1安全校核
4. 最后生成汇总报告
请按顺序执行这些步骤。""",
        expected_skill="topology_check",
        expected_actions=["init", "run"],
        requires_token=True,
        notes="测试多步骤工作流请求"
    ))

    tests.append(TestCase(
        id="T015",
        category="复杂工作流",
        name="参数研究（对话式）",
        prompt_style=PromptStyle.CONVERSATIONAL,
        prompt="我想研究一下负载变化对系统的影响，应该怎么做？",
        expected_skill="param_scan",
        expected_actions=["describe", "init"],
        notes="测试研究场景的建议请求"
    ))

    # ============ 类别7: 边界情况 ============
    tests.append(TestCase(
        id="T016",
        category="边界情况",
        name="无效技能名称",
        prompt_style=PromptStyle.CONCISE,
        prompt="运行 invalid_skill",
        expected_skill=None,
        expected_actions=["error"],
        notes="测试无效技能名称的处理"
    ))

    tests.append(TestCase(
        id="T017",
        category="边界情况",
        name="拼写错误的技能名（模糊）",
        prompt_style=PromptStyle.VAGUE,
        prompt="我想用 n1secure 技能做安全校核",
        expected_skill="n1_security",
        expected_actions=["list", "suggest"],
        notes="测试拼写错误的容错"
    ))

    tests.append(TestCase(
        id="T018",
        category="边界情况",
        name="不完整的请求",
        prompt_style=PromptStyle.VAGUE,
        prompt="帮我跑个仿真",
        expected_skill=None,
        expected_actions=["clarify"],
        notes="测试不完整请求的澄清"
    ))

    # ============ 类别8: 进阶功能 ============
    tests.append(TestCase(
        id="T019",
        category="进阶功能",
        name="自定义参数配置（详细）",
        prompt_style=PromptStyle.DETAILED,
        prompt="创建一个n1_security配置，指定检查支路Line_1和Line_2，电压阈值设为0.1，输出格式用JSON",
        expected_skill="n1_security",
        expected_actions=["init", "customize"],
        notes="测试自定义参数"
    ))

    tests.append(TestCase(
        id="T020",
        category="进阶功能",
        name="Python API调用（详细）",
        prompt_style=PromptStyle.DETAILED,
        prompt="在Python中导入N1SecuritySkill和ParamScanSkill，获取它们的默认配置并验证",
        expected_skill="n1_security",
        expected_actions=["import", "validate"],
        notes="测试Python API使用"
    ))

    return tests


def main():
    """主入口"""
    print("CloudPSS Skill System - 提示词驱动自动化测试")
    print("=" * 70)

    # 创建测试框架
    framework = PromptDrivenTestFramework(output_dir="./test_results")

    # 创建测试套件
    test_cases = create_test_suite()

    # 添加测试用例
    for test_case in test_cases:
        framework.add_test_case(test_case)

    # 运行所有测试
    framework.run_all_tests()


if __name__ == "__main__":
    main()
