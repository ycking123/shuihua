from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, JSON, Enum, ForeignKey
from sqlalchemy.sql import func
from .database import Base
import uuid

# 定义 Enum 类型 (为了与 SQL 中的 ENUM 匹配，但在 SQLAlchemy 中也可以使用 String)
# 这里为了兼容性，使用 String 存储 Enum 值，应用层校验
# 或者使用 SQLAlchemy 的 Enum 类型

class User(Base):
    __tablename__ = "shjl_users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    password_hash = Column(String(255), nullable=False)
    wecom_userid = Column(String(100), unique=True)
    full_name = Column(String(50))
    avatar_url = Column(Text)
    role_id = Column(Integer) # 简化，暂不定义 Role 表关系
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

class Todo(Base):
    __tablename__ = "shjl_todos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("shjl_users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text) # LONGTEXT in MySQL
    type = Column(String(20), default="task") # 'task', 'email', 'approval', 'meeting', 'chat_record'
    priority = Column(String(20), default="normal") # 'urgent', 'high', 'normal', 'low'
    status = Column(String(20), default="pending") # 'pending', 'in_progress', 'completed', 'archived'
    
    sender = Column(String(100))
    source_origin = Column(String(50))
    source_message_id = Column(String(100))
    
    ai_summary = Column(Text)
    ai_action = Column(Text)
    is_user_task = Column(Boolean, default=False)
    text_type = Column(Integer, default=0)
    
    due_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

class ChatSession(Base):
    __tablename__ = "shjl_chat_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("shjl_users.id"), nullable=False)
    title = Column(String(100))
    summary = Column(Text)
    is_pinned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

class ChatMessage(Base):
    __tablename__ = "shjl_chat_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("shjl_chat_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")
    meta_data = Column(JSON)
    created_at = Column(DateTime, default=func.now())

class AnalysisReport(Base):
    __tablename__ = "shjl_analysis_reports"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_type = Column(String(20)) # 'chat_message', 'todo', 'meeting'
    source_id = Column(String(36), nullable=False)
    title = Column(String(255))
    detailed_report = Column(Text)
    conclusion_cards = Column(JSON)
    mind_map_data = Column(JSON)
    raw_response = Column(JSON)
    created_at = Column(DateTime, default=func.now())

class Meeting(Base):
    __tablename__ = "shjl_meetings"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organizer_id = Column(String(36), ForeignKey("shjl_users.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String(255))
    wecom_schedule_id = Column(String(100))
    summary = Column(Text)
    transcript = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

