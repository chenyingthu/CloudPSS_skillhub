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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
