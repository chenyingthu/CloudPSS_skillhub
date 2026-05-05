#!/bin/bash
# CloudPSS Skills V3 安装脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置
INSTALL_DIR="${INSTALL_DIR:-/opt/cloudpss_skills_v3}"
SERVICE_USER="${SERVICE_USER:-cloudpss}"
PYTHON_VERSION="${PYTHON_VERSION:-3.11}"

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
       print_error "This script must be run as root"
       exit 1
    fi
}

detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    else
        print_error "Cannot detect OS"
        exit 1
    fi
}

install_dependencies() {
    print_status "Installing dependencies..."

    case $OS in
        "Ubuntu"|"Debian GNU/Linux")
            apt-get update
            apt-get install -y python3.11 python3.11-venv python3-pip git curl
            ;;
        "CentOS Linux"|"Red Hat Enterprise Linux"|"Fedora")
            yum install -y python3 python3-pip git curl
            ;;
        *)
            print_warning "Unknown OS: $OS. Please install dependencies manually."
            ;;
    esac
}

create_user() {
    print_status "Creating service user: $SERVICE_USER"

    if ! id "$SERVICE_USER" &>/dev/null; then
        useradd -r -s /bin/false -d "$INSTALL_DIR" "$SERVICE_USER"
        print_status "User created: $SERVICE_USER"
    else
        print_warning "User already exists: $SERVICE_USER"
    fi
}

install_app() {
    print_status "Installing application to $INSTALL_DIR..."

    # 创建目录
    mkdir -p "$INSTALL_DIR"

    # 获取脚本所在目录
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

    # 复制代码
    print_status "Copying application files..."
    cp -r "$PROJECT_ROOT"/* "$INSTALL_DIR/"
    cp -r "$PROJECT_ROOT"/.* "$INSTALL_DIR/" 2>/dev/null || true

    # 设置权限
    chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"

    # 创建虚拟环境
    print_status "Creating Python virtual environment..."
    cd "$INSTALL_DIR"
    sudo -u "$SERVICE_USER" python3 -m venv venv

    # 安装依赖
    print_status "Installing Python dependencies..."
    sudo -u "$SERVICE_USER" "$INSTALL_DIR/venv/bin/pip" install --upgrade pip
    sudo -u "$SERVICE_USER" "$INSTALL_DIR/venv/bin/pip" install -e "$INSTALL_DIR/."
}

create_services() {
    print_status "Creating systemd services..."

    # MCP Server 服务
    cat > /etc/systemd/system/cloudpss-mcp.service << EOF
[Unit]
Description=CloudPSS Skills V3 MCP Server
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$INSTALL_DIR
Environment=PYTHONPATH=$INSTALL_DIR
Environment=CLOUDPSS_TOKEN_FILE=$INSTALL_DIR/.cloudpss_token
ExecStart=$INSTALL_DIR/venv/bin/python -m cloudpss_skills_v3.mcp_server
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

    # Portal 服务
    cat > /etc/systemd/system/cloudpss-portal.service << EOF
[Unit]
Description=CloudPSS Skills V3 Portal
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$INSTALL_DIR
Environment=PYTHONPATH=$INSTALL_DIR
Environment=CLOUDPSS_PORTAL_TOKEN=$(openssl rand -hex 32)
ExecStart=$INSTALL_DIR/venv/bin/python -m cloudpss_skills_v3.master_organizer.portal.server --host 0.0.0.0 --port 8765
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

    # 重新加载 systemd
    systemctl daemon-reload

    print_status "Services created. Use 'systemctl enable cloudpss-portal' to enable auto-start."
}

configure_app() {
    print_status "Configuring application..."

    # 创建工作区目录
    WORKSPACE_DIR="/var/lib/cloudpss/workspace"
    mkdir -p "$WORKSPACE_DIR"
    chown -R "$SERVICE_USER:$SERVICE_USER" "$WORKSPACE_DIR"

    # 创建日志目录
    LOG_DIR="/var/log/cloudpss"
    mkdir -p "$LOG_DIR"
    chown -R "$SERVICE_USER:$SERVICE_USER" "$LOG_DIR"

    # 提示输入 token
    echo ""
    print_warning "Please configure your CloudPSS token:"
    echo "1. Edit $INSTALL_DIR/.cloudpss_token"
    echo "2. Or set environment variable: export CLOUDPSS_TOKEN='your-token'"
    echo ""
}

print_summary() {
    echo ""
    echo "=========================================="
    echo -e "${GREEN}Installation Complete!${NC}"
    echo "=========================================="
    echo ""
    echo "Installation directory: $INSTALL_DIR"
    echo "Service user: $SERVICE_USER"
    echo ""
    echo "Next steps:"
    echo "1. Configure your CloudPSS token"
    echo "2. Start services:"
    echo "   sudo systemctl start cloudpss-portal"
    echo "3. Check status:"
    echo "   sudo systemctl status cloudpss-portal"
    echo "4. View logs:"
    echo "   sudo journalctl -u cloudpss-portal -f"
    echo ""
    echo "Access the portal at: http://localhost:8765"
    echo ""
}

# 主流程
main() {
    echo "=========================================="
    echo "CloudPSS Skills V3 Installer"
    echo "=========================================="
    echo ""

    check_root
    detect_os
    install_dependencies
    create_user
    install_app
    create_services
    configure_app
    print_summary
}

# 运行主流程
main "$@"
