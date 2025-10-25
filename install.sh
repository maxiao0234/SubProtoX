#!/bin/bash

# SubProtoXInstallation Script
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Default configuration
DEFAULT_PORT=7777
DEFAULT_USER="$(whoami)"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  SubProtoX Installation Setup${NC}"
echo -e "${GREEN}=========================================${NC}"

# ============================================
# Step 1/4: Create configuration file
# ============================================
echo -e "${YELLOW}[1/4] Creating configuration file...${NC}"
if [ ! -f "$PROJECT_DIR/config.py" ]; then
    if [ -f "$PROJECT_DIR/config.example.py" ]; then
        echo -e "${BLUE}  Copying configuration template...${NC}"
        cp "$PROJECT_DIR/config.example.py" "$PROJECT_DIR/config.py"
        # Ensure config.py is owned by the current user
        chown "$DEFAULT_USER:$DEFAULT_USER" "$PROJECT_DIR/config.py"
        echo -e "${GREEN}✅ Created config.py${NC}"
        echo -e "${YELLOW}⚠️ Please modify config.py according to your environment${NC}"
    else
        echo -e "${RED}❌ Configuration template not found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Configuration file already exists${NC}"
    # Ensure existing config.py is owned by the current user
    chown "$DEFAULT_USER:$DEFAULT_USER" "$PROJECT_DIR/config.py" 2>/dev/null || true
fi

# ============================================
# Step 2/4: Install system dependencies
# ============================================
echo -e "${YELLOW}[2/4] Installing system dependencies...${NC}"
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv

# ============================================
# Step 3/4: Create virtual environment and install dependencies
# ============================================
echo -e "${YELLOW}[3/4] Creating virtual environment and installing dependencies...${NC}"
cd "$PROJECT_DIR"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

source venv/bin/activate
pip install -r requirements.txt

# ============================================
# Step 4/4: Create and start systemd service
# ============================================
echo -e "${YELLOW}[4/4] Creating and starting systemd service...${NC}"

sudo tee /etc/systemd/system/subprotox.service > /dev/null << EOF
[Unit]
Description=SubProtoX Protocol Conversion Service
After=network.target

[Service]
Type=simple
User=$DEFAULT_USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/app.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable subprotox
sudo systemctl start subprotox

# Wait for service to start
sleep 3

# Check service status
if sudo systemctl is-active --quiet subprotox; then
    echo -e "${GREEN}✅ Service started successfully${NC}"
else
    echo -e "${RED}❌ Service failed to start${NC}"
    sudo systemctl status subprotox
    exit 1
fi

# Get configured port and address
PORT=$(python3 -c "
import sys
sys.path.append('$PROJECT_DIR')
try:
    from config import get_config
    config = get_config()
    print(config['server']['port'])
except:
    print('$DEFAULT_PORT')
" 2>/dev/null || echo "$DEFAULT_PORT")

# Get IP address
IP=$(curl -s4 https://api.ipify.org 2>/dev/null || echo "YOUR_SERVER_IP")

echo -e "\n${GREEN}=========================================${NC}"
echo -e "${GREEN}  Installation Complete!${NC}"
echo -e "${GREEN}=========================================${NC}"

echo -e "\n${BLUE}Access URL:${NC}"
echo -e "  ${GREEN}http://${IP}:${PORT}/${NC}"

echo -e "\n${YELLOW}Default Login Credentials:${NC}"
echo -e "  Username: ${GREEN}admin${NC}"
echo -e "  Password: ${GREEN}admin${NC}"
echo -e "  ${RED}⚠️ IMPORTANT: Change the default password immediately after first login!${NC}"

echo -e "\n${YELLOW}Next Steps:${NC}"
echo -e "  1. ${BLUE}Login to the web interface${NC}"
echo -e "  2. ${BLUE}Go to Settings tab and change your password${NC}"
echo -e "  3. ${BLUE}(Optional) Configure SSL/HTTPS in the Settings tab${NC}"
echo -e "  4. ${BLUE}(Optional) Adjust other settings as needed${NC}"

echo -e "\n${YELLOW}Configuration:${NC}"
echo -e "  Config file: ${BLUE}$PROJECT_DIR/config.py${NC}"
echo -e "  ${GREEN}✅ All settings can be modified via the Web interface (Settings tab)${NC}"

echo -e "\n${YELLOW}Service Management:${NC}"
echo -e "  Start service: ${GREEN}sudo systemctl start subprotox${NC}"
echo -e "  Stop service: ${GREEN}sudo systemctl stop subprotox${NC}"
echo -e "  Restart service: ${GREEN}sudo systemctl restart subprotox${NC}"
echo -e "  Check status: ${GREEN}sudo systemctl status subprotox${NC}"
echo -e "  View logs: ${GREEN}sudo journalctl -u subprotox -f${NC}"

echo -e "\n${YELLOW}Features:${NC}"
echo -e "  ✅ Support Vless/Vmess/Trojan/Shadowsocks link conversion"
echo -e "  ✅ Support subscription conversion (Base64 encoded and plain text)"
echo -e "  ✅ Custom routing rules"
echo -e "  ✅ Web management interface"
echo -e "  ✅ RESTful API"
echo -e "  ✅ Configuration file management"
echo -e "  ✅ Multi-language support"

echo -e "\n${YELLOW}API Examples:${NC}"
echo -e "  Convert links: POST /convert/api/convert/links"
echo -e "  Convert subscription: GET /convert/api/convert/sub?url=<subscription_url>"
echo -e "  Get configuration: GET /convert/clash/<token>"

echo -e "${GREEN}=========================================${NC}"