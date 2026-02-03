from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..database import get_db
from ..models import Todo
from ..security import verify_token
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
def get_todos(http_request: Request, db: Session = Depends(get_db)):
    # Extract user_id from token if available
    user_id = "00000000-0000-0000-0000-000000000000"
    auth_header = http_request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = verify_token(token)
            if payload and "user_id" in payload:
                user_id = payload["user_id"]
        except Exception:
            pass
            
    # Query todos for this user (or default user if no token)
    # Also include tasks assigned to "Sender" if they belong to this user session context (simplified for now)
    todos = db.query(Todo).filter(
        Todo.is_deleted == False,
        Todo.user_id == user_id
    ).order_by(desc(Todo.created_at)).all()
    
    return [db_to_schema(t) for t in todos]

@router.post("/api/todos", response_model=TodoItemSchema)
def add_todo(todo: TodoItemSchema, http_request: Request, db: Session = Depends(get_db)):
    # Extract user_id from token
    user_id = "00000000-0000-0000-0000-000000000000"
    auth_header = http_request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = verify_token(token)
            if payload and "user_id" in payload:
                user_id = payload["user_id"]
        except Exception:
            pass
            
    # Check if this user_id exists in the database to prevent IntegrityError
    from ..models import User
    existing_user = db.query(User).filter(User.id == user_id).first()
    
    if not existing_user:
        # If the user doesn't exist (e.g. default placeholder or invalid token), try to find ANY user
        # DEPRECATED: This caused isolation issues where tasks were assigned to random users (e.g. admin)
        # We now strictly require a valid user_id or a valid default user.
        # fallback_user = db.query(User).first()
        # if fallback_user:
        #     user_id = fallback_user.id
        # else:
        #     # If NO users exist at all, we can't insert due to foreign key constraint
        #     # We must create a default user or fail
        #     raise HTTPException(status_code=500, detail="No users found in database to attach todo item")
        raise HTTPException(status_code=401, detail="Authentication required or invalid user")

    new_todo = Todo(
        id=str(uuid.uuid4()),
        user_id=user_id,
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
    assignee: Optional[str] = None,
    user_id: Optional[str] = None
):
    from ..models import User
    
    final_user_id = None
    
    # 1. Try to use provided user_id if it exists in DB
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            final_user_id = user.id
            
    # 2. If provided user_id was invalid or not provided, try default placeholder
    if not final_user_id:
        default_id = "00000000-0000-0000-0000-000000000000"
        # Only use default if it actually exists in DB
        user = db.query(User).filter(User.id == default_id).first()
        if user:
            final_user_id = user.id
            
    # 3. Fallback: use ANY valid user (e.g. for deployed envs without default user)
    # DEPRECATED: This caused isolation issues where tasks were assigned to random users (e.g. admin)
    # We now strictly require a valid user_id or a valid default user.
    # if not final_user_id:
    #     user = db.query(User).filter(User.is_deleted == False).first()
    #     if user:
    #         final_user_id = user.id
    #         print(f"⚠️ create_todo_internal: Using fallback user {user.username} ({user.id})")
            
    # 4. If absolutely no users found, raise error
    if not final_user_id:
        raise Exception("No valid user found in database to assign todo item. Please ensure users exist in shjl_users table.")

    
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
        user_id=final_user_id,
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



