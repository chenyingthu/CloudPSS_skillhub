"""
Observation Portal 测试

测试 Portal 的 API 和页面功能。
"""

import pytest
import tempfile
import shutil
from pathlib import Path

from cloudpss_skills_v3.portal.app import create_app
from cloudpss_skills_v3.core.task_store import TaskStatus, reset_task_store


class TestPortal:
    """Portal 测试套件"""

    @pytest.fixture
    def app(self):
        """创建测试应用"""
        reset_task_store()
        temp_dir = tempfile.mkdtemp()

        # 创建测试配置
        test_config = {
            'TESTING': True,
            'SECRET_KEY': 'test-secret-key'
        }

        app = create_app()
        app.config.update(test_config)

        yield app

        # 清理
        reset_task_store()
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def client(self, app):
        """创建测试客户端"""
        return app.test_client()

    def test_index_page(self, client):
        """测试首页"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'\xe4\xbb\xaa\xe8\xa1\xa8\xe6\x9d\xbf' in response.data  # "仪表板" in bytes

    def test_tasks_page(self, client):
        """测试任务列表页"""
        response = client.get('/tasks')
        assert response.status_code == 200
        assert b'\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x88\x97\xe8\xa1\xa8' in response.data  # "任务列表"

    def test_task_detail_page(self, client):
        """测试任务详情页"""
        response = client.get('/tasks/task-001')
        assert response.status_code == 200
        assert b'task-001' in response.data

    def test_api_health(self, client):
        """测试健康检查 API"""
        response = client.get('/api/health')
        assert response.status_code == 200

        json_data = response.get_json()
        assert json_data['status'] == 'healthy'
        assert 'timestamp' in json_data
        assert json_data['version'] == '0.1.0'

    def test_api_dashboard_stats(self, client):
        """测试仪表板统计 API"""
        response = client.get('/api/dashboard/stats')
        assert response.status_code == 200

        json_data = response.get_json()
        assert 'stats' in json_data
        assert 'recent_tasks' in json_data

        stats = json_data['stats']
        assert 'total_tasks' in stats
        assert 'completed' in stats
        assert 'running' in stats
        assert 'failed' in stats
        assert 'pending' in stats

    def test_api_tasks_empty(self, client):
        """测试空任务列表 API"""
        response = client.get('/api/tasks')
        assert response.status_code == 200

        json_data = response.get_json()
        assert json_data['tasks'] == []
        assert json_data['total'] == 0

    def test_api_task_detail_not_found(self, client):
        """测试获取不存在的任务"""
        response = client.get('/api/tasks/nonexistent')
        assert response.status_code == 404

    def test_api_tasks_with_filter(self, client):
        """测试带过滤条件的任务列表"""
        # 先创建一些任务
        from cloudpss_skills_v3.core.task_store import get_task_store
        store = get_task_store()

        store.create_task('task-001', 'Test 1', 'model/1')
        store.update_task_status('task-001', TaskStatus.COMPLETED)

        store.create_task('task-002', 'Test 2', 'model/2')
        store.update_task_status('task-002', TaskStatus.RUNNING)

        # 测试过滤
        response = client.get('/api/tasks?status=completed')
        assert response.status_code == 200

        json_data = response.get_json()
        assert len(json_data['tasks']) == 1
        assert json_data['tasks'][0]['task_id'] == 'task-001'

    def test_api_task_detail_with_data(self, client):
        """测试获取任务详情"""
        # 创建任务
        from cloudpss_skills_v3.core.task_store import get_task_store
        store = get_task_store()

        store.create_task('task-003', 'Test Detail', 'model/3', 'powerflow')
        store.update_task_status(
            'task-003',
            status=TaskStatus.COMPLETED,
            progress=100,
            message='计算完成',
            result_data={'voltage': 1.0}
        )

        # 获取详情
        response = client.get('/api/tasks/task-003')
        assert response.status_code == 200

        json_data = response.get_json()
        assert json_data['task_id'] == 'task-003'
        assert json_data['case_name'] == 'Test Detail'
        assert json_data['task_type'] == 'powerflow'
        assert json_data['status'] == 'completed'
        assert json_data['progress'] == 100
        assert json_data['result_data'] == {'voltage': 1.0}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
