#!/bin/bash
# CloudPSS Skills V3 恢复脚本

set -e

# 配置
WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.cloudpss/workspace}"
TOKEN_FILE="${TOKEN_FILE:-$HOME/.cloudpss/.cloudpss_token}"

# 检查参数
if [ $# -eq 0 ]; then
    echo "Usage: $0 <backup-file.tar.gz>"
    echo ""
    echo "Available backups:"
    ls -1t ~/.cloudpss/backups/backup_*.tar.gz 2>/dev/null | head -10 || echo "No backups found"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "Restoring from: $BACKUP_FILE"
read -p "This will overwrite existing data. Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Restore cancelled."
    exit 0
fi

# 创建临时目录
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# 解压备份
echo "Extracting backup..."
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"

# 查找备份目录
BACKUP_DIR=$(find "$TEMP_DIR" -type d -name "backup_*" | head -1)

if [ -z "$BACKUP_DIR" ]; then
    echo "Error: Invalid backup file structure"
    exit 1
fi

# 停止服务（如果运行中）
if systemctl is-active --quiet cloudpss-portal 2>/dev/null; then
    echo "Stopping cloudpss-portal service..."
    sudo systemctl stop cloudpss-portal
    SERVICE_STOPPED=true
fi

# 恢复工作区
if [ -d "$BACKUP_DIR/workspace" ]; then
    echo "Restoring workspace..."
    mkdir -p "$WORKSPACE_DIR"
    rm -rf "$WORKSPACE_DIR"/*
    cp -r "$BACKUP_DIR/workspace"/* "$WORKSPACE_DIR/"
fi

# 恢复 token
if [ -f "$BACKUP_DIR/$(basename "$TOKEN_FILE")" ]; then
    echo "Restoring token..."
    mkdir -p "$(dirname "$TOKEN_FILE")"
    cp "$BACKUP_DIR/$(basename "$TOKEN_FILE")" "$TOKEN_FILE"
    chmod 600 "$TOKEN_FILE"
fi

echo "Restore completed!"

# 重启服务
if [ "$SERVICE_STOPPED" = true ]; then
    echo "Starting cloudpss-portal service..."
    sudo systemctl start cloudpss-portal
fi

echo "Done."
