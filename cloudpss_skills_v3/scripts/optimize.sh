#!/bin/bash
# CloudPSS Skills V3 性能优化脚本

set -e

echo "=========================================="
echo "CloudPSS Skills V3 Performance Optimization"
echo "=========================================="
echo ""

# 系统优化
echo "[1/5] Optimizing system parameters..."

# 增加文件描述符限制
if ! grep -q "cloudpss soft nofile" /etc/security/limits.conf 2>/dev/null; then
    echo "cloudpss soft nofile 65536" | sudo tee -a /etc/security/limits.conf
    echo "cloudpss hard nofile 65536" | sudo tee -a /etc/security/limits.conf
    echo "  - Increased file descriptor limits"
fi

# 优化 TCP 参数
sudo sysctl -w net.core.somaxconn=65535 2>/dev/null || true
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=65535 2>/dev/null || true
sudo sysctl -w net.ipv4.ip_local_port_range="1024 65535" 2>/dev/null || true
echo "  - Optimized TCP parameters"

# Python 优化
echo ""
echo "[2/5] Configuring Python optimizations..."

# 创建优化配置
cat > /opt/cloudpss_skills_v3/.env << 'EOF'
# Python optimizations
PYTHONOPTIMIZE=1
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1

# Performance settings
WEB_CONCURRENCY=4
MAX_WORKERS=4

# Cache settings
CACHE_TTL=300
EOF

echo "  - Created environment configuration"

# 清理缓存
echo ""
echo "[3/5] Cleaning up..."
find /opt/cloudpss_skills_v3 -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find /opt/cloudpss_skills_v3 -type f -name "*.pyc" -delete 2>/dev/null || true
echo "  - Cleaned Python cache files"

# 服务优化
echo ""
echo "[4/5] Optimizing service configuration..."

# 更新服务文件以使用优化参数
if [ -f /etc/systemd/system/cloudpss-portal.service ]; then
    sudo systemctl daemon-reload
    echo "  - Reloaded systemd configuration"
fi

# 性能测试
echo ""
echo "[5/5] Running performance check..."

# 检查服务状态
if systemctl is-active --quiet cloudpss-portal 2>/dev/null; then
    echo "  - Service is running"
    # 测试响应时间
    RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" http://localhost:8765/api/health 2>/dev/null || echo "N/A")
    echo "  - API response time: ${RESPONSE_TIME}s"
else
    echo "  - Service not running (skipping response test)"
fi

echo ""
echo "=========================================="
echo "Optimization complete!"
echo "=========================================="
echo ""
echo "Recommendations:"
echo "1. Restart services to apply changes:"
echo "   sudo systemctl restart cloudpss-portal"
echo "2. Monitor resource usage:"
echo "   sudo journalctl -u cloudpss-portal -f"
echo ""
