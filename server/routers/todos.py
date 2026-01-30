from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

router = APIRouter()

class TodoItem(BaseModel):
    id: str
    type: str = "chat_record"  # default type for chat-created todos
    priority: str = "high"
    title: str
    sender: str = "AI智僚"
    time: str
    completed: bool = False
    status: str = "pending"
    aiSummary: Optional[str] = None
    aiAction: Optional[str] = None
    content: Optional[str] = None
    isUserTask: bool = False

# Global in-memory store
todos_store: List[TodoItem] = []

@router.get("/api/todos", response_model=List[TodoItem])
async def get_todos():
    return todos_store

@router.post("/api/todos", response_model=TodoItem)
async def add_todo(todo: TodoItem):
    todos_store.insert(0, todo)
    return todo

def create_todo_internal(title: str, summary: str, priority: str = "high"):
    new_todo = TodoItem(
        id=str(uuid.uuid4()),
        type="chat_record",
        priority=priority,
        title=title,
        sender="AI智僚",
        time=datetime.now().strftime("%H:%M"),
        status="pending",
        aiSummary=summary,
        content=summary
    )
    todos_store.insert(0, new_todo)
    return new_todo
