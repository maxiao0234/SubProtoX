#!/bin/bash

# SubProtoX Uninstallation Script
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${RED}=========================================${NC}"
echo -e "${RED}  SubProtoX Uninstallation${NC}"
echo -e "${RED}=========================================${NC}"

# Confirmation prompt
echo -e "${YELLOW}�  This will remove SubProtoX from your system.${NC}"
echo -e "${YELLOW}�  The following will be deleted:${NC}"
echo -e "  - Systemd service"
echo -e "  - Virtual environment (venv/)"
echo -e "  - Database file (gringotts.db)"
echo -e "  - Log files"
echo -e ""
echo -e "${BLUE}The following will be kept:${NC}"
echo -e "  - Source code files"
echo -e "  - Configuration file (config.py)"
echo -e "  - Custom rules"
echo -e ""
read -p "Do you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${GREEN}Uninstallation cancelled.${NC}"
    exit 0
fi

# ============================================
# Step 1/4: Stop and remove systemd service
# ============================================
echo -e "${YELLOW}[1/4] Stopping and removing systemd service...${NC}"

if systemctl is-active --quiet subprotox 2>/dev/null; then
    echo -e "${BLUE}  Stopping SubProtoX service...${NC}"
    sudo systemctl stop subprotox
    echo -e "${GREEN} Service stopped${NC}"
fi

if systemctl is-enabled --quiet subprotox 2>/dev/null; then
    echo -e "${BLUE}  Disabling SubProtoX service...${NC}"
    sudo systemctl disable subprotox
    echo -e "${GREEN} Service disabled${NC}"
fi

if [ -f "/etc/systemd/system/subprotox.service" ]; then
    echo -e "${BLUE}  Removing service file...${NC}"
    sudo rm -f /etc/systemd/system/subprotox.service
    sudo systemctl daemon-reload
    echo -e "${GREEN} Service file removed${NC}"
else
    echo -e "${GREEN} No service file found${NC}"
fi

# ============================================
# Step 2/4: Remove virtual environment
# ============================================
echo -e "${YELLOW}[2/4] Removing virtual environment...${NC}"

if [ -d "$PROJECT_DIR/venv" ]; then
    echo -e "${BLUE}  Removing venv directory...${NC}"
    rm -rf "$PROJECT_DIR/venv"
    echo -e "${GREEN} Virtual environment removed${NC}"
else
    echo -e "${GREEN} No virtual environment found${NC}"
fi

# ============================================
# Step 3/4: Remove database and cache files
# ============================================
echo -e "${YELLOW}[3/4] Removing database and cache files...${NC}"

# Remove database
if [ -f "$PROJECT_DIR/gringotts.db" ]; then
    echo -e "${BLUE}  Removing database (gringotts.db)...${NC}"
    rm -f "$PROJECT_DIR/gringotts.db"
    echo -e "${GREEN} Database removed${NC}"
else
    echo -e "${GREEN} No database found${NC}"
fi

# Remove Python cache
if [ -d "$PROJECT_DIR/__pycache__" ]; then
    echo -e "${BLUE}  Removing Python cache...${NC}"
    find "$PROJECT_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$PROJECT_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true
    echo -e "${GREEN} Python cache removed${NC}"
fi

# ============================================
# Step 4/4: Clean up optional files
# ============================================
echo -e "${YELLOW}[4/4] Cleanup summary...${NC}"

KEPT_FILES=()
if [ -f "$PROJECT_DIR/config.py" ]; then
    KEPT_FILES+=("config.py")
fi

if [ -d "$PROJECT_DIR/rules" ] && [ "$(ls -A $PROJECT_DIR/rules/*.py 2>/dev/null | wc -l)" -gt 0 ]; then
    KEPT_FILES+=("rules/")
fi

if [ ${#KEPT_FILES[@]} -gt 0 ]; then
    echo -e "${BLUE}The following files/directories have been kept:${NC}"
    for file in "${KEPT_FILES[@]}"; do
        echo -e "  - ${GREEN}$file${NC}"
    done
    echo -e ""
    echo -e "${YELLOW}To completely remove SubProtoX, run:${NC}"
    echo -e "  ${RED}cd .. && rm -rf $(basename $PROJECT_DIR)${NC}"
else
    echo -e "${GREEN} All generated files removed${NC}"
    echo -e "${YELLOW}To completely remove SubProtoX, run:${NC}"
    echo -e "  ${RED}cd .. && rm -rf $(basename $PROJECT_DIR)${NC}"
fi

echo -e "\n${GREEN}=========================================${NC}"
echo -e "${GREEN}  Uninstallation Complete!${NC}"
echo -e "${GREEN}=========================================${NC}"

echo -e "\n${BLUE}What was removed:${NC}"
echo -e "   Systemd service (subprotox)"
echo -e "   Virtual environment (venv/)"
echo -e "   Database file (gringotts.db)"
echo -e "   Python cache files"

echo -e "\n${YELLOW}What was kept:${NC}"
echo -e "  =� Source code files"
echo -e "  =� Configuration file (if exists)"
echo -e "  =� Custom rules (if exists)"

echo -e "\n${YELLOW}Optional: Remove everything${NC}"
echo -e "  To delete the entire project directory:"
echo -e "  ${RED}cd .. && rm -rf $(basename $PROJECT_DIR)${NC}"

echo -e "\n${GREEN}Thank you for using SubProtoX!${NC}"
echo -e "${GREEN}=========================================${NC}\n"
