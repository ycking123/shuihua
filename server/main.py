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
from .routers import asr, chat, todos, auth
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

@app.get("/api/health")
def read_root():
    return {
        "status": "ok", 
        "message": "Python Backend is running (Refactored with MySQL)!", 
        "framework": "FastAPI"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


