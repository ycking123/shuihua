from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..database import get_db
from ..models import Todo
# 为了避免循环导入，不要直接导入 create_todo_internal，而是将其重构为依赖注入的服务函数

router = APIRouter()

# Pydantic Model (Schema)
class TodoItemSchema(BaseModel):
    id: Optional[str] = None
    type: str = "chat_record"
    priority: str = "high"
    title: str
    sender: str = "AI智僚"
    time: Optional[str] = None # 用于前端显示的格式化时间，后端使用 created_at
    completed: bool = False
    status: str = "pending"
    aiSummary: Optional[str] = None
    aiAction: Optional[str] = None
    content: Optional[str] = None
    isUserTask: bool = False
    textType: int = 0
    
    # 兼容前端字段名到数据库字段名的映射
    class Config:
        from_attributes = True
        populate_by_name = True

# Helper to convert DB model to Pydantic model with custom time format
def db_to_schema(db_item: Todo) -> TodoItemSchema:
    return TodoItemSchema(
        id=db_item.id,
        type=db_item.type,
        priority=db_item.priority,
        title=db_item.title,
        sender=db_item.sender,
        time=db_item.created_at.strftime("%H:%M") if db_item.created_at else "",
        completed=db_item.status == "completed",
        status=db_item.status,
        aiSummary=db_item.ai_summary,
        aiAction=db_item.ai_action,
        content=db_item.content,
        isUserTask=db_item.is_user_task,
        textType=db_item.textType if hasattr(db_item, 'textType') else db_item.text_type # Handle snake_case vs camelCase mismatch if any
    )

@router.get("/api/todos", response_model=List[TodoItemSchema])
def get_todos(db: Session = Depends(get_db)):
    # 查询所有非删除的 Todos，按创建时间倒序
    todos = db.query(Todo).filter(Todo.is_deleted == False).order_by(desc(Todo.created_at)).all()
    return [db_to_schema(t) for t in todos]

@router.post("/api/todos", response_model=TodoItemSchema)
def add_todo(todo: TodoItemSchema, db: Session = Depends(get_db)):
    # 简单的用户 ID 占位符，实际应从 Auth 获取
    default_user_id = "00000000-0000-0000-0000-000000000000" 
    
    new_todo = Todo(
        id=str(uuid.uuid4()),
        user_id=default_user_id,
        title=todo.title,
        content=todo.content,
        type=todo.type,
        priority=todo.priority,
        status=todo.status,
        sender=todo.sender,
        ai_summary=todo.aiSummary,
        ai_action=todo.aiAction,
        is_user_task=todo.isUserTask,
        text_type=todo.textType,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return db_to_schema(new_todo)

# 重构内部函数，使其支持数据库操作
# 注意：现在是同步操作
def create_todo_internal(
    db: Session, 
    title: str, 
    summary: str, 
    priority: str = "high", 
    category: str = "chat_record",
    due_date: Optional[str] = None,
    assignee: Optional[str] = None
):
    default_user_id = "00000000-0000-0000-0000-000000000000"
    
    # Parse due_date if provided
    due_at_dt = None
    if due_date:
        try:
            # Try parsing typical formats
            # AI usually returns YYYY-MM-DD HH:MM
            due_at_dt = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
        except ValueError:
            try:
                 due_at_dt = datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                pass

    # Format content to include details
    formatted_content = summary
    if assignee:
        formatted_content += f"\n责任人: {assignee}"
    if due_date:
        formatted_content += f"\n截止时间: {due_date}"

    # Format ai_summary
    formatted_ai_summary = summary
    if due_date:
         formatted_ai_summary = f"【截止: {due_date}】 {summary}"

    new_todo = Todo(
        id=str(uuid.uuid4()),
        user_id=default_user_id,
        title=title,
        content=formatted_content,
        type=category,
        priority=priority,
        status="pending",
        sender=assignee if assignee else "AI智僚",
        ai_summary=formatted_ai_summary,
        due_at=due_at_dt,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return db_to_schema(new_todo)

