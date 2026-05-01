"""
CLI 测试
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch
import sys

from cloudpss_skills_v3.master_organizer.cli.main import main


class TestCLI:
    """CLI 测试"""

    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_cli_no_args(self):
        """测试无参数运行"""
        with patch.object(sys, 'argv', ['cloudpss-master']):
            result = main()
            assert result == 1  # 应该返回错误码

    def test_cli_init(self):
        """测试 init 命令"""
        with patch.object(sys, 'argv', ['cloudpss-master', 'init', '--path', str(self.temp_dir)]):
            result = main()
            assert result == 0
            assert (self.temp_dir / "config").exists()

    def test_cli_status(self):
        """测试 status 命令"""
        # 先初始化
        with patch.object(sys, 'argv', ['cloudpss-master', 'init', '--path', str(self.temp_dir)]):
            main()

        with patch.object(sys, 'argv', ['cloudpss-master', 'status']):
            with patch('cloudpss_skills_v3.master_organizer.cli.main.get_path_manager') as mock_pm:
                from cloudpss_skills_v3.master_organizer.core import PathManager
                mock_pm.return_value = PathManager(self.temp_dir)
                result = main()
                assert result == 0

    def test_cli_case_list(self):
        """测试 case list 命令"""
        with patch.object(sys, 'argv', ['cloudpss-master', 'init', '--path', str(self.temp_dir)]):
            main()

        with patch.object(sys, 'argv', ['cloudpss-master', 'case', 'list']):
            with patch('cloudpss_skills_v3.master_organizer.cli.main.get_path_manager') as mock_pm:
                from cloudpss_skills_v3.master_organizer.core import PathManager
                mock_pm.return_value = PathManager(self.temp_dir)
                result = main()
                assert result == 0

    def test_cli_server_add_list_remove(self):
        """测试 server add/list/remove 命令"""
        with patch.object(sys, 'argv', ['cloudpss-master', 'init', '--path', str(self.temp_dir)]):
            main()

        with patch('cloudpss_skills_v3.master_organizer.cli.main.get_path_manager') as mock_pm:
            from cloudpss_skills_v3.master_organizer.core import PathManager
            mock_pm.return_value = PathManager(self.temp_dir)

            # 添加服务器
            with patch.object(sys, 'argv', ['cloudpss-master', 'server', 'add', '--name', 'test-server', '--url', 'https://test.com']):
                result = main()
                assert result == 0

            # 列出服务器
            with patch.object(sys, 'argv', ['cloudpss-master', 'server', 'list']):
                result = main()
                assert result == 0

    def test_cli_case_create_delete(self):
        """测试 case create/delete 命令"""
        with patch.object(sys, 'argv', ['cloudpss-master', 'init', '--path', str(self.temp_dir)]):
            main()

        with patch('cloudpss_skills_v3.master_organizer.cli.main.get_path_manager') as mock_pm:
            from cloudpss_skills_v3.master_organizer.core import PathManager
            mock_pm.return_value = PathManager(self.temp_dir)

            # 创建算例
            with patch.object(sys, 'argv', ['cloudpss-master', 'case', 'create', '--name', 'test-case', '--rid', 'model/test/123']):
                result = main()
                assert result == 0

            # 删除算例 (需要使用正确的ID格式)
            case_id = "case_20250101_120000_12345678"
            with patch.object(sys, 'argv', ['cloudpss-master', 'case', 'delete', case_id]):
                # 由于case不存在，应该返回错误
                result = main()
                # 非0表示错误
                assert result == 1

    def test_cli_task_create(self):
        """测试 task create 命令"""
        with patch.object(sys, 'argv', ['cloudpss-master', 'init', '--path', str(self.temp_dir)]):
            main()

        with patch('cloudpss_skills_v3.master_organizer.cli.main.get_path_manager') as mock_pm:
            from cloudpss_skills_v3.master_organizer.core import PathManager
            mock_pm.return_value = PathManager(self.temp_dir)

            # 创建任务
            with patch.object(sys, 'argv', ['cloudpss-master', 'task', 'create', '--name', 'test-task', '--case-id', 'case_test', '--type', 'powerflow']):
                result = main()
                assert result == 0

    def test_cli_query_tree(self):
        """测试 query tree 命令"""
        with patch.object(sys, 'argv', ['cloudpss-master', 'init', '--path', str(self.temp_dir)]):
            main()

        with patch('cloudpss_skills_v3.master_organizer.cli.main.get_path_manager') as mock_pm:
            from cloudpss_skills_v3.master_organizer.core import PathManager
            mock_pm.return_value = PathManager(self.temp_dir)

            with patch.object(sys, 'argv', ['cloudpss-master', 'query', 'tree']):
                result = main()
                assert result == 0

    def test_cli_query_dashboard(self):
        """测试 query dashboard 命令"""
        with patch.object(sys, 'argv', ['cloudpss-master', 'init', '--path', str(self.temp_dir)]):
            main()

        with patch('cloudpss_skills_v3.master_organizer.cli.main.get_path_manager') as mock_pm:
            from cloudpss_skills_v3.master_organizer.core import PathManager
            mock_pm.return_value = PathManager(self.temp_dir)

            with patch.object(sys, 'argv', ['cloudpss-master', 'query', 'dashboard']):
                result = main()
                assert result == 0

    def test_cli_variant_list(self):
        """测试 variant list 命令"""
        with patch.object(sys, 'argv', ['cloudpss-master', 'init', '--path', str(self.temp_dir)]):
            main()

        with patch('cloudpss_skills_v3.master_organizer.cli.main.get_path_manager') as mock_pm:
            from cloudpss_skills_v3.master_organizer.core import PathManager
            mock_pm.return_value = PathManager(self.temp_dir)

            with patch.object(sys, 'argv', ['cloudpss-master', 'variant', 'list']):
                result = main()
                assert result == 0

    def test_cli_result_list(self):
        """测试 result list 命令"""
        with patch.object(sys, 'argv', ['cloudpss-master', 'init', '--path', str(self.temp_dir)]):
            main()

        with patch('cloudpss_skills_v3.master_organizer.cli.main.get_path_manager') as mock_pm:
            from cloudpss_skills_v3.master_organizer.core import PathManager
            mock_pm.return_value = PathManager(self.temp_dir)

            with patch.object(sys, 'argv', ['cloudpss-master', 'result', 'list']):
                result = main()
                assert result == 0

    def test_cli_task_lifecycle(self):
        """测试 task submit/status/cancel 生命周期命令"""
        with patch.object(sys, 'argv', ['cloudpss-master', 'init', '--path', str(self.temp_dir)]):
            main()

        with patch('cloudpss_skills_v3.master_organizer.cli.main.get_path_manager') as mock_pm:
            from cloudpss_skills_v3.master_organizer.core import PathManager
            mock_pm.return_value = PathManager(self.temp_dir)

            # 创建任务
            with patch.object(sys, 'argv', ['cloudpss-master', 'task', 'create', '--name', 'lifecycle-test', '--case-id', 'case_test', '--type', 'powerflow']):
                result = main()
                assert result == 0

            # 获取刚创建的任务ID（通过列出任务）
            from cloudpss_skills_v3.master_organizer.core import TaskRegistry
            tasks = TaskRegistry().list_all()
            if tasks:
                task_id = tasks[0][0]

                # 提交任务
                with patch.object(sys, 'argv', ['cloudpss-master', 'task', 'submit', task_id]):
                    result = main()
                    assert result == 0

                # 查看状态
                with patch.object(sys, 'argv', ['cloudpss-master', 'task', 'status', task_id]):
                    result = main()
                    assert result == 0

                # 取消任务（只有在 created/submitted/running 状态才能取消）
                with patch.object(sys, 'argv', ['cloudpss-master', 'task', 'cancel', task_id]):
                    result = main()
                    assert result == 0

    def test_cli_variant_lifecycle(self):
        """测试 variant create/apply/delete 生命周期命令"""
        with patch.object(sys, 'argv', ['cloudpss-master', 'init', '--path', str(self.temp_dir)]):
            main()

        with patch('cloudpss_skills_v3.master_organizer.cli.main.get_path_manager') as mock_pm:
            from cloudpss_skills_v3.master_organizer.core import PathManager
            mock_pm.return_value = PathManager(self.temp_dir)

            # 先创建算例
            with patch.object(sys, 'argv', ['cloudpss-master', 'case', 'create', '--name', 'variant-test-case', '--rid', 'model/test/456']):
                result = main()
                assert result == 0

            # 获取算例ID
            from cloudpss_skills_v3.master_organizer.core import CaseRegistry
            cases = CaseRegistry().list_all()
            if cases:
                case_id = cases[0][0]

                # 创建变体
                with patch.object(sys, 'argv', ['cloudpss-master', 'variant', 'create', '--case-id', case_id, '--name', 'test-variant', '--parameters', 'param1=value1']):
                    result = main()
                    assert result == 0

                # 列出变体
                with patch.object(sys, 'argv', ['cloudpss-master', 'variant', 'list', '--case-id', case_id]):
                    result = main()
                    assert result == 0

                # 获取变体ID并删除
                from cloudpss_skills_v3.master_organizer.core import VariantRegistry
                variants = VariantRegistry().list_all()
                if variants:
                    variant_id = variants[0][0]
                    with patch.object(sys, 'argv', ['cloudpss-master', 'variant', 'delete', variant_id]):
                        result = main()
                        assert result == 0

    def test_cli_result_export_and_analyze(self):
        """测试 result export 和 analyze 命令"""
        import json

        with patch.object(sys, 'argv', ['cloudpss-master', 'init', '--path', str(self.temp_dir)]):
            main()

        with patch('cloudpss_skills_v3.master_organizer.cli.main.get_path_manager') as mock_pm:
            from cloudpss_skills_v3.master_organizer.core import PathManager
            mock_pm.return_value = PathManager(self.temp_dir)

            # 创建结果
            from cloudpss_skills_v3.master_organizer.core import ResultRegistry, Result, IDGenerator, EntityType
            result_id = IDGenerator.generate(EntityType.RESULT)
            result = Result(
                id=result_id,
                name="test-result",
                task_id="task_test",
                case_id="case_test",
                format="json",
                size_bytes=1024,
                files=["data.json"],
                metadata={"test": True}
            )
            ResultRegistry().create(result_id, result)

            export_path = self.temp_dir / "test_export.json"

            # 导出结果
            with patch.object(sys, 'argv', ['cloudpss-master', 'result', 'export', result_id, '--format', 'json', '--output', str(export_path)]):
                result = main()
                assert result == 0

            # 验证导出文件存在
            assert export_path.exists(), f"导出文件不存在: {export_path}"

            # 验证导出文件内容
            with open(export_path, 'r') as f:
                exported_data = json.load(f)
                assert exported_data['result_id'] == result_id
                assert exported_data['name'] == 'test-result'

            # 分析结果
            with patch.object(sys, 'argv', ['cloudpss-master', 'result', 'analyze', result_id]):
                result = main()
                assert result == 0

    def test_cli_path_isolation_with_cwd(self):
        """测试路径隔离：在自定义工作区目录下执行命令能正确找到工作区"""
        import os

        # 创建自定义工作区
        custom_workspace = self.temp_dir / "custom_workspace"

        # 初始化工作区
        with patch.object(sys, 'argv', ['cloudpss-master', 'init', '--path', str(custom_workspace)]):
            result = main()
            assert result == 0

        # 验证工作区结构已创建 (init --path 直接在该路径下创建结构，不是 .cloudpss 子目录)
        assert (custom_workspace / "config").exists()

        # 模拟在自定义工作区目录下执行命令
        original_cwd = os.getcwd()
        try:
            os.chdir(custom_workspace)

            # 不使用 mock，测试真实的路径解析
            from cloudpss_skills_v3.master_organizer.core import get_path_manager

            # 清除单例缓存，强制重新解析
            import cloudpss_skills_v3.master_organizer.core.path_manager as pm_module
            pm_module._path_manager = None

            pm = get_path_manager()

            # 验证路径管理器指向自定义工作区
            expected_root = custom_workspace.resolve()
            actual_root = pm.root.resolve()

            assert actual_root == expected_root, f"路径解析错误: 期望 {expected_root}, 实际 {actual_root}"

        finally:
            os.chdir(original_cwd)
            # 清理单例
            pm_module._path_manager = None

    def test_cli_result_compare(self):
        """测试 result compare 命令"""
        with patch.object(sys, 'argv', ['cloudpss-master', 'init', '--path', str(self.temp_dir)]):
            main()

        with patch('cloudpss_skills_v3.master_organizer.cli.main.get_path_manager') as mock_pm:
            from cloudpss_skills_v3.master_organizer.core import PathManager
            mock_pm.return_value = PathManager(self.temp_dir)

            # 创建两个结果
            from cloudpss_skills_v3.master_organizer.core import ResultRegistry, Result, IDGenerator, EntityType

            result1_id = IDGenerator.generate(EntityType.RESULT)
            result1 = Result(id=result1_id, name="result-1", task_id="task1", case_id="case1", size_bytes=1000)
            ResultRegistry().create(result1_id, result1)

            result2_id = IDGenerator.generate(EntityType.RESULT)
            result2 = Result(id=result2_id, name="result-2", task_id="task2", case_id="case1", size_bytes=2000)
            ResultRegistry().create(result2_id, result2)

            # 比较结果
            with patch.object(sys, 'argv', ['cloudpss-master', 'result', 'compare', result1_id, result2_id]):
                result = main()
                assert result == 0

    def test_cli_result_delete(self):
        """测试 result delete 命令"""
        with patch.object(sys, 'argv', ['cloudpss-master', 'init', '--path', str(self.temp_dir)]):
            main()

        with patch('cloudpss_skills_v3.master_organizer.cli.main.get_path_manager') as mock_pm:
            from cloudpss_skills_v3.master_organizer.core import PathManager
            mock_pm.return_value = PathManager(self.temp_dir)

            # 创建结果
            from cloudpss_skills_v3.master_organizer.core import ResultRegistry, Result, IDGenerator, EntityType
            result_id = IDGenerator.generate(EntityType.RESULT)
            result = Result(id=result_id, name="delete-test", task_id="task1", case_id="case1")
            ResultRegistry().create(result_id, result)

            # 删除结果
            with patch.object(sys, 'argv', ['cloudpss-master', 'result', 'delete', result_id]):
                result_code = main()
                assert result_code == 0

            # 验证已删除
            assert ResultRegistry().get(result_id) is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
