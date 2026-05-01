"""
真实 CLI 用户旅程集成测试。

这些测试通过子进程执行 ``python -m cloudpss_skills_v3.master_organizer.cli.main``，
覆盖跨进程配置持久化和用户从任意目录调用 CLI 的行为。
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
CLI_MODULE = "cloudpss_skills_v3.master_organizer.cli.main"


class CliRunner:
    def __init__(self, home: Path):
        self.home = home
        self.env = {
            **os.environ,
            "HOME": str(home),
            "PYTHONPATH": str(REPO_ROOT),
        }
        self.env.pop("CLOUDPSS_HOME", None)

    def run(self, *args: str, cwd: Path | None = None, check: bool = True):
        result = subprocess.run(
            [sys.executable, "-m", CLI_MODULE, *args],
            cwd=str(cwd or self.home),
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
        )
        if check and result.returncode != 0:
            raise AssertionError(
                f"Command failed: {' '.join(args)}\n"
                f"exit={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}"
            )
        return result


def load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def first_id(registry_path: Path, section: str) -> str:
    data = load_yaml(registry_path)
    return next(iter(data[section]))


def test_real_cli_user_journey_from_arbitrary_directory(tmp_path):
    home = tmp_path / "home"
    workspace = tmp_path / "workspace"
    outside = tmp_path / "outside"
    export_dir = tmp_path / "exports"
    home.mkdir()
    outside.mkdir()
    export_dir.mkdir()
    cli = CliRunner(home)

    init_result = cli.run("init", "--path", str(workspace), cwd=outside)
    assert "工作区初始化完成" in init_result.stdout

    root_probe = subprocess.run(
        [
            sys.executable,
            "-c",
            "from cloudpss_skills_v3.master_organizer.core import get_path_manager; print(get_path_manager().root)",
        ],
        cwd=str(outside),
        env=cli.env,
        text=True,
        capture_output=True,
        check=True,
    )
    assert root_probe.stdout.strip() == str(workspace)

    cli.run("server", "add", "--name", "uat-server", "--url", "https://uat.test", "--default", cwd=outside)
    cli.run(
        "case",
        "create",
        "--name",
        "UATCase",
        "--rid",
        "model/uat/case",
        "--description",
        "user journey",
        "--tag",
        "uat,important",
        cwd=outside,
    )
    case_id = first_id(workspace / "registry" / "cases.yaml", "cases")

    cli.run("task", "create", "--name", "BaseRun", "--case-id", case_id, "--type", "powerflow", cwd=outside)
    task_id = first_id(workspace / "registry" / "tasks.yaml", "tasks")

    cli.run("variant", "create", "--case-id", case_id, "--name", "load-plus", "--parameters", "load.P=*1.1", cwd=outside)
    variant_id = first_id(workspace / "registry" / "variants.yaml", "variants")
    cli.run("variant", "apply", variant_id, "--name", "VariantRun", cwd=outside)

    ref_guard = cli.run("variant", "delete", variant_id, cwd=outside, check=False)
    assert ref_guard.returncode == 1
    assert "已被" in ref_guard.stdout

    for command in [
        ("case", "show", case_id),
        ("case", "clone", case_id, "--name", "UATClone"),
        ("case", "archive", case_id),
        ("case", "restore", case_id),
        ("case", "list", "--tree", "--tag", "uat"),
        ("query", "search", "UAT", "--type", "all"),
        ("query", "recent", "--limit", "5"),
    ]:
        result = cli.run(*command, cwd=outside)
        assert result.stdout.strip()

    cases = load_yaml(workspace / "registry" / "cases.yaml")["cases"]
    assert cases[case_id]["task_count"] == 2
    assert cases[case_id]["last_task_id"].startswith("task_")

    # 模拟远端任务结果登记后，验证 result 子命令和导出落盘。
    result_id = "result_20260501_120000_11111111"
    subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "from cloudpss_skills_v3.master_organizer.core import ResultRegistry, Result;"
                f"r=ResultRegistry(r'{workspace / 'registry'}');"
                f"r.create('{result_id}', Result(id='{result_id}', name='UAT result', "
                f"task_id='{task_id}', case_id='{case_id}', size_bytes=256, "
                "files=['powerflow.json'], metadata={'converged': True}))"
            ),
        ],
        cwd=str(outside),
        env=cli.env,
        text=True,
        capture_output=True,
        check=True,
    )

    export_path = export_dir / "result.json"
    cli.run("result", "analyze", result_id, cwd=outside)
    cli.run("result", "export", result_id, "--format", "json", "--output", str(export_path), cwd=outside)
    exported = json.loads(export_path.read_text(encoding="utf-8"))
    assert exported["result_id"] == result_id
    assert exported["metadata"]["converged"] is True

    cli.run("workspace", "save", "--name", "uat", cwd=outside)
    list_result = cli.run("workspace", "list", cwd=outside)
    assert "uat:" in list_result.stdout
    cli.run("workspace", "load", "--name", "uat", cwd=outside)

    cache_file = workspace / "cache" / "old.tmp"
    cache_file.write_text("cache", encoding="utf-8")
    cli.run("workspace", "clean", cwd=outside)
    assert not cache_file.exists()


def test_real_cli_error_paths_return_nonzero(tmp_path):
    home = tmp_path / "home"
    workspace = tmp_path / "workspace"
    home.mkdir()
    cli = CliRunner(home)
    cli.run("init", "--path", str(workspace))

    missing_subcommand = cli.run("task", check=False)
    assert missing_subcommand.returncode == 2

    missing_case = cli.run(
        "task",
        "create",
        "--name",
        "bad-task",
        "--case-id",
        "case_20260501_120000_12345678",
        "--type",
        "powerflow",
        check=False,
    )
    assert missing_case.returncode == 1
    assert "算例不存在" in missing_case.stdout

    missing_workspace = cli.run("workspace", "load", "--name", "missing", check=False)
    assert missing_workspace.returncode == 1
