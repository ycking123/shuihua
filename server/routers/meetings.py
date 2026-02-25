from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Meeting, User, Todo
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import re

router = APIRouter(
    prefix="/api/meetings",
    tags=["meetings"],
    responses={404: {"description": "Not found"}},
)

class MeetingResponse(BaseModel):
    id: str
    title: str
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    summary: Optional[str] = None
    transcript: Optional[str] = None
    organizer_id: Optional[str] = None
    todos_count: int = 0  # 新增：关联待办数量
    
    class Config:
        from_attributes = True

class TodoResponse(BaseModel):
    """会议关联的待办事项响应"""
    id: str
    title: str
    content: Optional[str] = None
    priority: str = "normal"
    status: str = "pending"
    assignee: Optional[str] = None
    due_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class SmartTitleRequest(BaseModel):
    """智能标题更新请求"""
    pass  # 不需要参数，服务端自动判断

def generate_smart_title(title: str, summary: str) -> str:
    """
    智能标题生成逻辑
    - 若为系统默认标题（如"xxx的快速会议"），提取 summary 第一句作为新标题
    - 否则保留原标题
    """
    default_patterns = ["的快速会议", "的会议", "快速会议"]
    
    # 检测默认标题特征
    for pattern in default_patterns:
        if pattern in title and len(title) < 30:
            # 提取 summary 第一句作为标题
            if summary:
                # 提取第一句（以句号、问号、感叹号结尾）
                sentences = re.split(r'[。！？\n]', summary)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if sentence and len(sentence) >= 5:  # 至少5个字符
                        return sentence[:50]  # 限制50字符
            return title
    
    return title  # 用户自定义标题保留

def db_meeting_to_response(meeting: Meeting, db: Session) -> MeetingResponse:
    """转换数据库模型为响应模型，包含待办数量"""
    todos_count = db.query(Todo).filter(
        Todo.source_message_id == meeting.id,
        Todo.is_deleted == False
    ).count()
    
    return MeetingResponse(
        id=meeting.id,
        title=meeting.title,
        start_time=meeting.start_time,
        end_time=meeting.end_time,
        location=meeting.location,
        summary=meeting.summary,
        transcript=meeting.transcript,
        organizer_id=meeting.organizer_id,
        todos_count=todos_count
    )

@router.get("/", response_model=List[MeetingResponse])
def get_meetings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    meetings = db.query(Meeting).order_by(Meeting.start_time.desc()).offset(skip).limit(limit).all()
    return [db_meeting_to_response(m, db) for m in meetings]

@router.get("/{meeting_id}", response_model=MeetingResponse)
def get_meeting(meeting_id: str, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return db_meeting_to_response(meeting, db)

@router.get("/{meeting_id}/todos", response_model=List[TodoResponse])
def get_meeting_todos(meeting_id: str, db: Session = Depends(get_db)):
    """
    获取会议关联的待办事项
    通过 source_message_id 关联
    """
    # 先检查会议是否存在
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    # 查询关联的待办
    todos = db.query(Todo).filter(
        Todo.source_message_id == meeting_id,
        Todo.is_deleted == False
    ).order_by(Todo.created_at.desc()).all()
    
    return [TodoResponse(
        id=t.id,
        title=t.title,
        content=t.content,
        priority=t.priority,
        status=t.status,
        assignee=t.sender,
        due_at=t.due_at,
        created_at=t.created_at
    ) for t in todos]

@router.post("/{meeting_id}/smart-title", response_model=MeetingResponse)
def update_smart_title(meeting_id: str, db: Session = Depends(get_db)):
    """
    智能标题更新
    - 判断标题是否为默认格式
    - 若是，提取 summary 第一句作为新标题
    """
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    # 生成智能标题
    new_title = generate_smart_title(meeting.title, meeting.summary or "")
    
    if new_title != meeting.title:
        meeting.title = new_title
        meeting.updated_at = datetime.now()
        db.commit()
        db.refresh(meeting)
    
    return db_meeting_to_response(meeting, db)