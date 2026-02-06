#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
LOG_DIR="$SCRIPT_DIR/logs"

echo "Stopping services..."

# Function to kill process and its children
kill_process_and_children() {
    local pid=$1
    if [ -z "$pid" ]; then return; fi

    if kill -0 $pid 2>/dev/null; then
        # Try to kill children first (useful for npm -> vite)
        # pkill -P matches Parent PID
        pkill -P $pid 2>/dev/null
        
        echo "   Killing PID $pid"
        kill $pid 2>/dev/null
    else
        echo "   PID $pid not running."
    fi
}

stop_service() {
    local pid_file=$1
    local name=$2
    
    if [ -f "$pid_file" ]; then
        PID=$(cat "$pid_file")
        echo "Stopping $name (PID: $PID)..."
        kill_process_and_children $PID
        rm "$pid_file"
    else
        echo "No PID file found for $name."
    fi
}

stop_service "$LOG_DIR/main_server.pid" "Main Backend"
stop_service "$LOG_DIR/wechat_server.pid" "WeChat Backend"
stop_service "$LOG_DIR/frontend.pid" "Frontend"

# Fallback: Kill by port (requires lsof or fuser) to ensure no zombies
echo "Ensuring ports are free (cleanup)..."

# 1. Try fuser (common on Linux)
if command -v fuser &> /dev/null; then
    fuser -k 8000/tcp 2>/dev/null && echo "  Force killed process on port 8000"
    fuser -k 8080/tcp 2>/dev/null && echo "  Force killed process on port 8080"
    fuser -k 5173/tcp 2>/dev/null && echo "  Force killed process on port 5173"
    fuser -k 3000/tcp 2>/dev/null && echo "  Force killed process on port 3000"
# 2. Try lsof
elif command -v lsof &> /dev/null; then
    for port in 8000 8080 5173 3000; do
        pid=$(lsof -t -i:$port)
        if [ ! -z "$pid" ]; then
            kill -9 $pid 2>/dev/null
            echo "  Force killed process on port $port (PID: $pid)"
        fi
    done
# 3. Last resort: pkill by name
else
    echo "  (fuser/lsof not found, checking process names...)"
    pkill -f "server.main"
    pkill -f "backend.server_receive"
    # Be careful with 'vite', only kill if it looks like ours? 
    # Or just kill all vite instances if this is a dedicated server.
    pkill -f "vite"
fi

echo "Done. All services stopped."

