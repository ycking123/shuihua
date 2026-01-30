from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env.local in root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env.local")

# Import routers
# Try relative import first (if running as package), then absolute (if running as script)
try:
    from .routers import asr, chat, todos
except ImportError:
    from routers import asr, chat, todos

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(asr.router)
app.include_router(chat.router)
app.include_router(todos.router)

@app.get("/api/health")
def read_root():
    return {
        "status": "ok", 
        "message": "Python Backend is running (Refactored)!", 
        "framework": "FastAPI"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
