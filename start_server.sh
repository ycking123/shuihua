#!/bin/bash

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# 创建日志目录
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

echo "=================================================="
echo "   Water Essence Sprite - Linux Startup Script"
echo "=================================================="

# 检查环境
if ! command -v python &> /dev/null; then
    echo "Error: 'python' command not found."
    echo "Please activate your Conda/Python environment first:"
    echo "  e.g., conda activate water_essence_backend"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "Error: 'npm' command not found."
    exit 1
fi

# 1. 启动主后端 (Port 8000)
echo "[1/3] Starting Main Backend (server/main.py)..."
nohup python server/main.py > "$LOG_DIR/main_server.log" 2>&1 &
MAIN_PID=$!
echo "      PID: $MAIN_PID | Log: $LOG_DIR/main_server.log"

# 2. 启动企业微信后端 (Port 8080)
echo "[2/3] Starting WeChat Backend (backend.server_receive)..."
nohup python -m backend.server_receive > "$LOG_DIR/wechat_server.log" 2>&1 &
WECHAT_PID=$!
echo "      PID: $WECHAT_PID | Log: $LOG_DIR/wechat_server.log"

# 3. 启动前端
echo "[3/3] Starting Frontend (npm run dev)..."
nohup npm run dev > "$LOG_DIR/frontend.log" 2>&1 &
FRONT_PID=$!
echo "      PID: $FRONT_PID | Log: $LOG_DIR/frontend.log"

# 保存 PID 以便停止
echo "$MAIN_PID" > "$LOG_DIR/main_server.pid"
echo "$WECHAT_PID" > "$LOG_DIR/wechat_server.pid"
echo "$FRONT_PID" > "$LOG_DIR/frontend.pid"

echo "=================================================="
echo "All services started successfully in background!"
echo "You can close this terminal session now."
echo "To stop services, run: ./stop_server.sh"
echo "=================================================="

