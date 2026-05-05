"""
Observation Portal 主应用

基于 Flask 的只读监控界面。
"""

import os
import logging
from datetime import datetime, timedelta
from pathlib import Path

from flask import Flask, render_template, jsonify, request

from cloudpss_skills_v3.core.task_store import get_task_store, TaskStatus

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建 Flask 应用
def create_app():
    """创建并配置 Flask 应用"""
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')

    # 配置
    app.config['SECRET_KEY'] = os.getenv('PORTAL_SECRET_KEY', 'dev-secret-key')
    app.config['JSON_AS_ASCII'] = False

    # 注册路由
    _register_routes(app)

    logger.info("Observation Portal 初始化完成")
    return app


def _register_routes(app):
    """注册所有路由"""

    @app.route('/')
    def index():
        """首页 - 仪表板"""
        return render_template('dashboard.html')

    @app.route('/tasks')
    def tasks():
        """任务列表页"""
        return render_template('tasks.html')

    @app.route('/tasks/<task_id>')
    def task_detail(task_id):
        """任务详情页"""
        return render_template('task_detail.html', task_id=task_id)

    @app.route('/cases')
    def cases():
        """案例列表页"""
        return render_template('cases.html')

    @app.route('/api/dashboard/stats')
    def api_dashboard_stats():
        """API: 获取仪表板统计"""
        task_store = get_task_store()
        all_tasks = task_store.list_tasks(limit=1000)

        # 统计信息
        stats = {
            'total_tasks': len(all_tasks),
            'completed': len([t for t in all_tasks if t.status == TaskStatus.COMPLETED]),
            'running': len([t for t in all_tasks if t.status == TaskStatus.RUNNING]),
            'failed': len([t for t in all_tasks if t.status == TaskStatus.FAILED]),
            'pending': len([t for t in all_tasks if t.status == TaskStatus.PENDING]),
        }

        # 最近24小时的任务
        recent_tasks = [
            t for t in all_tasks
            if datetime.now() - t.created_at < timedelta(hours=24)
        ][:10]

        return jsonify({
            'stats': stats,
            'recent_tasks': [t.to_dict() for t in recent_tasks]
        })

    @app.route('/api/tasks')
    def api_tasks():
        """API: 获取任务列表"""
        task_store = get_task_store()

        # 获取过滤参数
        status_filter = request.args.get('status')
        limit = int(request.args.get('limit', 100))

        # 转换状态字符串为枚举
        status = None
        if status_filter:
            try:
                status = TaskStatus(status_filter)
            except ValueError:
                pass

        tasks = task_store.list_tasks(status=status, limit=limit)

        return jsonify({
            'tasks': [t.to_dict() for t in tasks],
            'total': len(tasks)
        })

    @app.route('/api/tasks/<task_id>')
    def api_task_detail(task_id):
        """API: 获取单个任务详情"""
        task_store = get_task_store()
        task = task_store.get_task(task_id)

        if not task:
            return jsonify({'error': 'Task not found'}), 404

        return jsonify(task.to_dict())

    @app.route('/api/health')
    def api_health():
        """API: 健康检查"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '0.1.0'
        })


# 全局应用实例
_app = None


def get_app():
    """获取全局应用实例"""
    global _app
    if _app is None:
        _app = create_app()
    return _app


if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORTAL_PORT', 5001))
    debug = os.getenv('PORTAL_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
