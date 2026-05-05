# CloudPSS Skills V3 部署指南

## 系统要求

### 最低配置
- **CPU:** 2 核心
- **内存:** 4 GB RAM
- **存储:** 20 GB 可用空间
- **操作系统:** Linux (Ubuntu 20.04+ / CentOS 8+)
- **Python:** 3.10+
- **Node.js:** 18+ (可选，用于前端开发)

### 推荐配置
- **CPU:** 4 核心+
- **内存:** 8 GB RAM+
- **存储:** 50 GB SSD
- **网络:** 稳定的外网连接（访问 CloudPSS API）

---

## 快速开始

### 1. 安装依赖

```bash
# 系统依赖 (Ubuntu/Debian)
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3-pip git

# 系统依赖 (CentOS/RHEL)
sudo yum install -y python3 python3-pip git
```

### 2. 克隆仓库

```bash
git clone <repository-url>
cd cloudpss_skills_v3
```

### 3. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. 安装 Python 包

```bash
pip install -e ".[dev]"
```

### 5. 配置环境变量

```bash
# 创建配置文件
mkdir -p ~/.cloudpss
echo "your-cloudpss-token" > ~/.cloudpss/.cloudpss_token

# 或者设置环境变量
export CLOUDPSS_TOKEN="your-cloudpss-token"
```

### 6. 启动服务

```bash
# 启动 MCP Server
python -m cloudpss_skills_v3.mcp_server

# 或者启动 Portal
python -m cloudpss_skills_v3.master_organizer.portal.server
```

---

## 部署模式

### 模式 1: 开发环境

适用于本地开发和测试。

```bash
# 1. 安装依赖
pip install -e ".[dev]"

# 2. 运行测试
pytest

# 3. 启动开发服务器
python -m cloudpss_skills_v3.master_organizer.portal.server --host 127.0.0.1 --port 8765
```

### 模式 2: 生产环境 (systemd)

#### 2.1 创建 systemd 服务

**MCP Server 服务:**
```bash
sudo tee /etc/systemd/system/cloudpss-mcp.service > /dev/null << 'EOF'
[Unit]
Description=CloudPSS Skills V3 MCP Server
After=network.target

[Service]
Type=simple
User=cloudpss
Group=cloudpss
WorkingDirectory=/opt/cloudpss_skills_v3
Environment=PYTHONPATH=/opt/cloudpss_skills_v3
Environment=CLOUDPSS_TOKEN_FILE=/opt/cloudpss_skills_v3/.cloudpss_token
ExecStart=/opt/cloudpss_skills_v3/venv/bin/python -m cloudpss_skills_v3.mcp_server
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

**Portal 服务:**
```bash
sudo tee /etc/systemd/system/cloudpss-portal.service > /dev/null << 'EOF'
[Unit]
Description=CloudPSS Skills V3 Portal
After=network.target

[Service]
Type=simple
User=cloudpss
Group=cloudpss
WorkingDirectory=/opt/cloudpss_skills_v3
Environment=PYTHONPATH=/opt/cloudpss_skills_v3
Environment=CLOUDPSS_PORTAL_TOKEN=your-secure-token
ExecStart=/opt/cloudpss_skills_v3/venv/bin/python -m cloudpss_skills_v3.master_organizer.portal.server --host 0.0.0.0 --port 8765
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

#### 2.2 创建用户和目录

```bash
# 创建用户
sudo useradd -r -s /bin/false cloudpss

# 创建目录
sudo mkdir -p /opt/cloudpss_skills_v3
sudo chown cloudpss:cloudpss /opt/cloudpss_skills_v3

# 复制代码
sudo cp -r . /opt/cloudpss_skills_v3/
sudo chown -R cloudpss:cloudpss /opt/cloudpss_skills_v3
```

#### 2.3 安装依赖

```bash
sudo -u cloudpss bash -c '
cd /opt/cloudpss_skills_v3
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
'
```

#### 2.4 配置 token

```bash
sudo -u cloudpss tee /opt/cloudpss_skills_v3/.cloudpss_token > /dev/null << 'EOF'
your-cloudpss-token-here
EOF
sudo chmod 600 /opt/cloudpss_skills_v3/.cloudpss_token
```

#### 2.5 启动服务

```bash
sudo systemctl daemon-reload
sudo systemctl enable cloudpss-mcp cloudpss-portal
sudo systemctl start cloudpss-mcp cloudpss-portal
```

#### 2.6 检查状态

```bash
sudo systemctl status cloudpss-mcp
sudo systemctl status cloudpss-portal
sudo journalctl -u cloudpss-portal -f
```

### 模式 3: Docker 部署

#### 3.1 创建 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . /app/

# 安装 Python 依赖
RUN pip install --no-cache-dir -e ".[dev]"

# 创建非 root 用户
RUN useradd -m -u 1000 cloudpss && \
    chown -R cloudpss:cloudpss /app
USER cloudpss

# 暴露端口
EXPOSE 8765

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8765/api/health')" || exit 1

# 默认启动 Portal
CMD ["python", "-m", "cloudpss_skills_v3.master_organizer.portal.server", "--host", "0.0.0.0", "--port", "8765"]
```

#### 3.2 创建 docker-compose.yml

```yaml
version: '3.8'

services:
  cloudpss-portal:
    build: .
    container_name: cloudpss-portal
    ports:
      - "8765:8765"
    environment:
      - CLOUDPSS_PORTAL_TOKEN=${CLOUDPSS_PORTAL_TOKEN:-secure-token}
      - CLOUDPSS_TOKEN=${CLOUDPSS_TOKEN}
    volumes:
      - ./data:/app/data
      - ./workspace:/app/workspace
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8765/api/health')"]
      interval: 30s
      timeout: 10s
      retries: 3

  # 可选：Nginx 反向代理
  nginx:
    image: nginx:alpine
    container_name: cloudpss-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - cloudpss-portal
    restart: unless-stopped
```

#### 3.3 构建和运行

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 模式 4: Kubernetes 部署

#### 4.1 创建 ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cloudpss-config
data:
  PORTAL_HOST: "0.0.0.0"
  PORTAL_PORT: "8765"
```

#### 4.2 创建 Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: cloudpss-secrets
type: Opaque
stringData:
  CLOUDPSS_TOKEN: "your-cloudpss-token"
  CLOUDPSS_PORTAL_TOKEN: "your-portal-token"
```

#### 4.3 创建 Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloudpss-portal
  labels:
    app: cloudpss-portal
spec:
  replicas: 2
  selector:
    matchLabels:
      app: cloudpss-portal
  template:
    metadata:
      labels:
        app: cloudpss-portal
    spec:
      containers:
      - name: portal
        image: your-registry/cloudpss-skills:v3.0.0
        ports:
        - containerPort: 8765
        envFrom:
        - configMapRef:
            name: cloudpss-config
        - secretRef:
            name: cloudpss-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 8765
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health
            port: 8765
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### 4.4 创建 Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: cloudpss-portal
spec:
  selector:
    app: cloudpss-portal
  ports:
  - port: 80
    targetPort: 8765
  type: ClusterIP
```

#### 4.5 部署

```bash
kubectl apply -f k8s/
kubectl get pods -l app=cloudpss-portal
```

---

## Nginx 反向代理配置

```nginx
server {
    listen 80;
    server_name cloudpss.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8765;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
    }
}
```

---

## SSL/TLS 配置

### 使用 Let's Encrypt

```bash
# 安装 certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d cloudpss.yourdomain.com

# 自动续期
sudo certbot renew --dry-run
```

---

## 备份与恢复

### 备份数据

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup/cloudpss/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 备份工作区
cp -r /opt/cloudpss_skills_v3/workspace "$BACKUP_DIR/"

# 备份配置
cp /opt/cloudpss_skills_v3/.cloudpss_token "$BACKUP_DIR/"

# 压缩
tar -czf "$BACKUP_DIR.tar.gz" -C "$BACKUP_DIR" .
rm -rf "$BACKUP_DIR"

echo "Backup completed: $BACKUP_DIR.tar.gz"
```

### 恢复数据

```bash
#!/bin/bash
# restore.sh

BACKUP_FILE="$1"
if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup-file.tar.gz>"
    exit 1
fi

# 停止服务
sudo systemctl stop cloudpss-portal

# 解压备份
tar -xzf "$BACKUP_FILE" -C /tmp/

# 恢复数据
sudo cp -r /tmp/workspace/* /opt/cloudpss_skills_v3/workspace/
sudo cp /tmp/.cloudpss_token /opt/cloudpss_skills_v3/

# 启动服务
sudo systemctl start cloudpss-portal

echo "Restore completed"
```

---

## 监控与日志

### 日志位置

```
# systemd 日志
sudo journalctl -u cloudpss-portal -f

# 应用日志
/opt/cloudpss_skills_v3/logs/

# 访问日志
/var/log/nginx/access.log
```

### 监控指标

```bash
# 查看服务状态
sudo systemctl status cloudpss-portal

# 查看资源使用
ps aux | grep cloudpss
df -h /opt/cloudpss_skills_v3

# 查看端口监听
ss -tlnp | grep 8765
```

---

## 故障排除

### 服务无法启动

```bash
# 检查日志
sudo journalctl -u cloudpss-portal -n 50

# 检查配置
sudo -u cloudpss python -m cloudpss_skills_v3.master_organizer.portal.server --help

# 测试启动
sudo -u cloudpss python -m cloudpss_skills_v3.master_organizer.portal.server
```

### API 无响应

```bash
# 测试健康检查
curl http://localhost:8765/api/health

# 检查端口
curl -v http://localhost:8765/api/snapshot
```

### 权限问题

```bash
# 修复权限
sudo chown -R cloudpss:cloudpss /opt/cloudpss_skills_v3
sudo chmod 600 /opt/cloudpss_skills_v3/.cloudpss_token
```

---

## 升级指南

### 升级步骤

```bash
# 1. 备份数据
./backup.sh

# 2. 停止服务
sudo systemctl stop cloudpss-portal

# 3. 更新代码
cd /opt/cloudpss_skills_v3
git pull origin main

# 4. 更新依赖
source venv/bin/activate
pip install -e ".[dev]"

# 5. 启动服务
sudo systemctl start cloudpss-portal

# 6. 验证
sudo systemctl status cloudpss-portal
curl http://localhost:8765/api/health
```

---

## 安全建议

1. **使用防火墙** - 仅开放必要的端口
2. **启用 SSL/TLS** - 使用 HTTPS
3. **定期更新** - 保持系统和依赖更新
4. **使用强密码** - Portal token 使用随机字符串
5. **限制访问** - 使用 VPN 或内网访问
6. **日志审计** - 定期检查访问日志

---

## 性能优化

### 系统优化

```bash
# 增加文件描述符限制
echo "cloudpss soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "cloudpss hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# 优化 TCP 参数
sudo sysctl -w net.core.somaxconn=65535
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=65535
```

### 应用优化

```bash
# 设置环境变量
export PYTHONOPTIMIZE=1
export PYTHONDONTWRITEBYTECODE=1
```
