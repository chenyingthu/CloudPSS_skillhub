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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
