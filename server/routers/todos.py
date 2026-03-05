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
    time: Optional[str] = None
    completed: bool = False
    status: str = "pending"
    aiSummary: Optional[str] = None
    aiAction: Optional[str] = None
    content: Optional[str] = None
    isUserTask: bool = False
    textType: int = 0
    source_message_id: Optional[str] = None
    source_origin: Optional[str] = None
    meeting_start_time: Optional[str] = None
    meeting_created_at: Optional[str] = None
    
    class Config:
        from_attributes = True
        populate_by_name = True

# Helper to convert DB model to Pydantic model with custom time format
def db_to_schema(db_item: Todo, meeting_start_time: Optional[datetime] = None, meeting_created_at: Optional[datetime] = None) -> TodoItemSchema:
    return TodoItemSchema(
        id=db_item.id,
        type=db_item.type,
        priority=db_item.priority,
        title=db_item.title,
        sender=db_item.sender or "未知",
        time=db_item.created_at.strftime("%Y/%m/%d %H:%M:%S") if db_item.created_at else "",
        completed=db_item.status == "completed",
        status=db_item.status,
        aiSummary=db_item.ai_summary,
        aiAction=db_item.ai_action,
        content=db_item.content,
        isUserTask=db_item.is_user_task,
        textType=db_item.textType if hasattr(db_item, 'textType') else db_item.text_type,
        source_message_id=db_item.source_message_id,
        source_origin=db_item.source_origin,
        meeting_start_time=meeting_start_time.strftime("%Y/%m/%d %H:%M") if meeting_start_time else None,
        meeting_created_at=meeting_created_at.strftime("%Y/%m/%d %H:%M") if meeting_created_at else None
    )

@router.get("/api/todos", response_model=List[TodoItemSchema])
def get_todos(http_request: Request, db: Session = Depends(get_db), sort_by: str = "created_at"):
    """
    获取待办列表
    sort_by: "created_at" (发送时间) | "meeting_start_time" (会议时间)
    """
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
    
    from ..models import Meeting
            
    query = db.query(Todo, Meeting.start_time, Meeting.created_at).outerjoin(
        Meeting, Todo.source_message_id == Meeting.id
    ).filter(
        Todo.is_deleted == False,
        Todo.user_id == user_id
    )
    
    if sort_by == "meeting_start_time":
        query = query.order_by(
            Meeting.start_time.is_(None),
            desc(Meeting.start_time),
            desc(Todo.created_at)
        )
    else:
        query = query.order_by(
            Meeting.created_at.is_(None),
            desc(Meeting.created_at),
            desc(Todo.created_at)
        )
    
    results = query.all()
    
    todo_list = []
    for todo, meeting_start_time, meeting_created_at in results:
        todo_list.append(db_to_schema(todo, meeting_start_time, meeting_created_at))
    
    return todo_list

@router.post("/api/todos", response_model=TodoItemSchema)
def add_todo(todo: TodoItemSchema, http_request: Request, db: Session = Depends(get_db)):
    # Extract user_id from token
    user_id = None
    auth_header = http_request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = verify_token(token)
            if payload and "user_id" in payload:
                user_id = payload["user_id"]
        except Exception:
            pass
    
    # 如果没有有效的 user_id，使用默认用户或第一个用户
    from ..models import User
    if not user_id:
        # 尝试使用默认用户
        default_user = db.query(User).filter(User.id == "00000000-0000-0000-0000-000000000000").first()
        if default_user:
            user_id = default_user.id
        else:
            # 使用第一个可用用户
            first_user = db.query(User).first()
            if first_user:
                user_id = first_user.id
    
    if not user_id:
        raise HTTPException(status_code=500, detail="No users found in database")

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
        source_message_id=todo.source_message_id,  # 关联会议ID
        source_origin=todo.source_origin,  # 来源类型
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
        # Check if it's a valid UUID first to avoid DB errors
        try:
            uuid.UUID(user_id)
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                final_user_id = user.id
        except ValueError:
             print(f"⚠️ create_todo_internal: Invalid UUID provided: {user_id}")
            
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
        print(f"❌ create_todo_internal: Failed to find valid user. Provided: {user_id}")
        raise Exception("无法创建任务：未找到有效的用户关联。请尝试重新登录。")

    
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
    
    # Handle list type for assignee (convert to string)
    assignee_str = ""
    if assignee:
        if isinstance(assignee, list):
            assignee_str = ", ".join(assignee)
        else:
            assignee_str = str(assignee)
        formatted_content += f"\n责任人: {assignee_str}"
        
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
        sender=assignee_str if assignee_str else "AI智僚",
        ai_summary=formatted_ai_summary,
        due_at=due_at_dt,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return db_to_schema(new_todo)


class TodoUpdateSchema(BaseModel):
    """待办更新请求"""
    title: Optional[str] = None
    content: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None

@router.put("/api/todos/{todo_id}", response_model=TodoItemSchema)
def update_todo(todo_id: str, todo_update: TodoUpdateSchema, http_request: Request, db: Session = Depends(get_db)):
    """
    更新待办事项
    """
    from ..models import Meeting
    
    # 查询待办（不验证 user_id，因为会议待办可能是系统创建的）
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.is_deleted == False
    ).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # 更新字段
    if todo_update.title is not None:
        todo.title = todo_update.title
    if todo_update.content is not None:
        todo.content = todo_update.content
    if todo_update.priority is not None:
        todo.priority = todo_update.priority
    if todo_update.status is not None:
        todo.status = todo_update.status
        if todo_update.status == "completed":
            todo.completed_at = datetime.now()
    
    todo.updated_at = datetime.now()
    db.commit()
    db.refresh(todo)
    
    meeting = db.query(Meeting).filter(Meeting.id == todo.source_message_id).first() if todo.source_message_id else None
    
    return db_to_schema(todo, meeting.start_time if meeting else None, meeting.created_at if meeting else None)

@router.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: str, http_request: Request, db: Session = Depends(get_db)):
    """
    删除待办事项（软删除）
    """
    # 查询待办（不验证 user_id，因为会议待办可能是系统创建的）
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.is_deleted == False
    ).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # 软删除
    todo.is_deleted = True
    todo.updated_at = datetime.now()
    db.commit()
    
    return {"message": "Todo deleted successfully", "id": todo_id}
