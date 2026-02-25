# ============================================================================
# 文件: main.py
# 模块: server
# 职责: FastAPI 应用主入口，路由注册，CORS 配置，生命周期管理
#
# 依赖声明:
#   - 外部: fastapi, uvicorn, pathlib, dotenv, os, contextlib
#   - 本模块: server.routers (asr, chat, todos, auth, dashboard, meetings)
#   - 本模块: server.database (engine, Base, init_db)
#
# 主要接口:
#   - app: FastAPI 应用实例
#   - GET /api/health: 健康检查接口
#
# 注册的路由:
#   - /api/asr: 语音识别
#   - /api/chat: 聊天对话
#   - /api/todos: 待办事项管理
#   - /api/auth: 用户认证
#   - /api/dashboard: 仪表盘数据
#   - /api/meetings: 会议管理
#
# ============================================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager

# Load environment variables from .env in root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Import routers
# Using relative imports as we are running as a module (python -m server.main)
from .routers import asr, chat, todos, auth, dashboard, meetings
from .database import engine, Base, init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables if not exist
    try:
        print("Initializing database...")
        init_db() # Ensure DB exists
        print("Initializing database tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully (if they didn't exist).")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        # We don't raise here to allow server to start, but DB ops will likely fail

    print("Database connection initialized")
    yield
    # Shutdown
    engine.dispose()
    print("Database connection closed")

app = FastAPI(lifespan=lifespan)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://47.121.138.58:3000",
        "http://47.121.138.58:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(asr.router)
app.include_router(chat.router)
app.include_router(todos.router)
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(meetings.router)

@app.get("/api/health")
def read_root():
    return {
        "status": "ok", 
        "message": "Python Backend is running (Refactored with MySQL)!", 
        "framework": "FastAPI"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



