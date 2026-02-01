#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
LOG_DIR="$SCRIPT_DIR/logs"

echo "Stopping services..."

stop_process() {
    local pid_file=$1
    local name=$2
    
    if [ -f "$pid_file" ]; then
        PID=$(cat "$pid_file")
        if kill -0 $PID 2>/dev/null; then
            echo "Stopping $name (PID: $PID)..."
            kill $PID
        else
            echo "$name (PID: $PID) is not running."
        fi
        rm "$pid_file"
    else
        echo "No PID file found for $name."
    fi
}

stop_process "$LOG_DIR/main_server.pid" "Main Backend"
stop_process "$LOG_DIR/wechat_server.pid" "WeChat Backend"
stop_process "$LOG_DIR/frontend.pid" "Frontend"

echo "Done."

