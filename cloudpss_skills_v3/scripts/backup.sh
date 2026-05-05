#!/bin/bash
# CloudPSS Skills V3 备份脚本

set -e

# 配置
WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.cloudpss/workspace}"
TOKEN_FILE="${TOKEN_FILE:-$HOME/.cloudpss/.cloudpss_token}"
BACKUP_DIR="${BACKUP_DIR:-$HOME/.cloudpss/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"

# 创建备份目录
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="$BACKUP_DIR/backup_$TIMESTAMP"
mkdir -p "$BACKUP_PATH"

echo "Starting backup to $BACKUP_PATH..."

# 备份工作区
if [ -d "$WORKSPACE_DIR" ]; then
    echo "Backing up workspace..."
    cp -r "$WORKSPACE_DIR" "$BACKUP_PATH/"
fi

# 备份 token
if [ -f "$TOKEN_FILE" ]; then
    echo "Backing up token..."
    cp "$TOKEN_FILE" "$BACKUP_PATH/"
    chmod 600 "$BACKUP_PATH/$(basename "$TOKEN_FILE")"
fi

# 压缩备份
echo "Compressing backup..."
cd "$BACKUP_DIR"
tar -czf "backup_$TIMESTAMP.tar.gz" "backup_$TIMESTAMP"
rm -rf "backup_$TIMESTAMP"

# 清理旧备份
echo "Cleaning old backups (older than $RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup completed: $BACKUP_DIR/backup_$TIMESTAMP.tar.gz"

# 列出最近的备份
echo "Recent backups:"
ls -lh "$BACKUP_DIR"/backup_*.tar.gz 2>/dev/null | tail -5 || echo "No backups found"
