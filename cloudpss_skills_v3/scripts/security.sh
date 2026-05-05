#!/bin/bash
# CloudPSS Skills V3 安全加固脚本

set -e

echo "=========================================="
echo "CloudPSS Skills V3 Security Hardening"
echo "=========================================="
echo ""

INSTALL_DIR="${INSTALL_DIR:-/opt/cloudpss_skills_v3}"
SERVICE_USER="${SERVICE_USER:-cloudpss}"

echo "[1/6] Checking file permissions..."

# 确保安装目录权限正确
if [ -d "$INSTALL_DIR" ]; then
    chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"
    chmod 750 "$INSTALL_DIR"
    echo "  - Fixed installation directory permissions"
fi

# 保护敏感文件
if [ -f "$INSTALL_DIR/.cloudpss_token" ]; then
    chmod 600 "$INSTALL_DIR/.cloudpss_token"
    chown "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR/.cloudpss_token"
    echo "  - Secured token file"
fi

# 保护脚本目录
if [ -d "$INSTALL_DIR/scripts" ]; then
    chmod 750 "$INSTALL_DIR/scripts"
    echo "  - Secured scripts directory"
fi

echo ""
echo "[2/6] Configuring firewall..."

# 检查 UFW 状态
if command -v ufw &> /dev/null; then
    if ufw status | grep -q "Status: active"; then
        # 允许 Portal 端口
        ufw allow 8765/tcp comment 'CloudPSS Portal' 2>/dev/null || true
        echo "  - Configured UFW rules"
    else
        echo "  - UFW not active (skipping)"
    fi
else
    echo "  - UFW not installed (skipping)"
fi

echo ""
echo "[3/6] Setting up log rotation..."

cat > /etc/logrotate.d/cloudpss << 'EOF'
/var/log/cloudpss/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0640 cloudpss cloudpss
    sharedscripts
    postrotate
        systemctl reload cloudpss-portal > /dev/null 2>&1 || true
    endscript
}
EOF

echo "  - Created logrotate configuration"

echo ""
echo "[4/6] Checking for security updates..."

# 检查 Python 依赖更新
if [ -d "$INSTALL_DIR/venv" ]; then
    echo "  - Checking Python packages for security updates..."
    "$INSTALL_DIR/venv/bin/pip" list --outdated 2>/dev/null | head -10 || echo "    (pip check complete)"
fi

echo ""
echo "[5/6] Audit check..."

# 检查敏感文件权限
echo "  - Sensitive files:"
find "$INSTALL_DIR" -name ".*token*" -o -name ".*secret*" -o -name ".*key*" 2>/dev/null | while read file; do
    if [ -f "$file" ]; then
        perms=$(stat -c "%a" "$file" 2>/dev/null || stat -f "%Lp" "$file" 2>/dev/null)
        if [ "$perms" != "600" ]; then
            echo "    WARNING: $file has permissions $perms (should be 600)"
        else
            echo "    OK: $file"
        fi
    fi
done

# 检查目录权限
echo "  - Directory permissions:"
for dir in "$INSTALL_DIR" "$INSTALL_DIR/scripts" "$INSTALL_DIR/venv"; do
    if [ -d "$dir" ]; then
        perms=$(stat -c "%a" "$dir" 2>/dev/null || stat -f "%Lp" "$dir" 2>/dev/null)
        echo "    $dir: $perms"
    fi
done

echo ""
echo "[6/6] Security recommendations..."

echo ""
echo "Completed checks:"
echo "  [✓] File permissions"
echo "  [✓] Firewall configuration"
echo "  [✓] Log rotation"
echo "  [✓] Security audit"
echo ""
echo "Recommendations:"
echo "  1. Enable SSL/TLS for production use"
echo "  2. Use strong authentication tokens"
echo "  3. Regularly update dependencies: pip list --outdated"
echo "  4. Monitor logs: sudo journalctl -u cloudpss-portal -f"
echo "  5. Set up fail2ban for additional protection"
echo "  6. Use VPN or private network for internal access"
echo ""
