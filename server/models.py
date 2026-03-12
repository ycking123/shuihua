# ============================================================================
# 文件: models.py
# 模块: server
# 职责: SQLAlchemy ORM 模型定义，映射数据库表结构
#
# 依赖声明:
#   - 外部: sqlalchemy, uuid
#   - 本模块: server.database (Base)
#
# 主要模型:
#   - User: 用户表 (shjl_users)
#   - Todo: 待办事项表 (shjl_todos)
#   - Meeting: 会议表 (shjl_meetings)
#   - ChatMessage: 聊天消息表 (shjl_chat_messages)
#
# ============================================================================

from sqlalchemy import Column, String, Integer, BigInteger, Boolean, Text, DateTime, JSON, Enum, ForeignKey
from sqlalchemy.sql import func
from .database import Base
import uuid


class SysUser(Base):
    """系统用户表（映射 sys_user），用于登录认证"""
    __tablename__ = "sys_user"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    dept_id = Column(BigInteger)
    user_name = Column(String(30), nullable=False)
    nick_name = Column(String(30), nullable=False)
    password = Column(String(100))
    status = Column(String(1), default='0')      # '0' 正常 '1' 停用
    del_flag = Column(String(1), default='0')     # '0' 正常 '2' 已删除
    avatar = Column(String(100))
    phonenumber = Column(String(11))
    dept_path = Column(String(500))

class SysDept(Base):
    """系统部门表（映射 sys_dept），用于部门层级和知识库权限判定"""
    __tablename__ = "sys_dept"

    dept_id = Column(BigInteger, primary_key=True)
    parent_id = Column(BigInteger, default=0)
    ancestors = Column(String(500))    # 祖先部门ID链，逗号分隔，如 "0,100,101,107"
    dept_name = Column(String(30))
    status = Column(String(1), default='0')
    del_flag = Column(String(1), default='0')

class Todo(Base):
    __tablename__ = "shjl_todos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
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
    user_id = Column(String(36), nullable=False)
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
    organizer_id = Column(String(36))
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

class StrategyDaily(Base):
    __tablename__ = "shjl_strategy_daily"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    report_date = Column(String(10), nullable=False) # Format: YYYY-MM-DD
    query_key = Column(String(255), nullable=False)
    title = Column(String(255))
    content = Column(Text)
    url = Column(String(500))
    subtext = Column(String(100))
    color = Column(String(20))
    icon_type = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())




