from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.sql import func

from .database import Base

import uuid


def generate_uuid() -> str:
    """生成字符串主键。"""
    return str(uuid.uuid4())


class SysUser(Base):
    """系统用户表，映射真实的 sys_user。"""

    __tablename__ = "sys_user"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    dept_id = Column(BigInteger)
    user_name = Column(String(30), nullable=False)
    nick_name = Column(String(30), nullable=False)
    user_type = Column(String(2))
    email = Column(String(50))
    phonenumber = Column(String(11))
    sex = Column(String(1))
    avatar = Column(String(100))
    password = Column(String(100))
    status = Column(String(1), default="0")
    del_flag = Column(String(1), default="0")
    login_ip = Column(String(128))
    login_date = Column(DateTime)
    create_by = Column(String(64))
    create_time = Column(DateTime)
    update_by = Column(String(64))
    update_time = Column(DateTime)
    remark = Column(String(500))
    post_name = Column(String(100))
    position = Column(String(100))
    office_phone = Column(String(30))
    alias = Column(String(50))
    user_code = Column(String(50))
    order_num = Column(Integer)
    short_number = Column(String(20))
    wechat = Column(String(50))
    rtx_account = Column(String(50))
    dept_path = Column(String(500))
    wecom_userid = Column(String(64), unique=True)


class SysDept(Base):
    """系统部门表。"""

    __tablename__ = "sys_dept"

    dept_id = Column(BigInteger, primary_key=True)
    parent_id = Column(BigInteger, default=0)
    ancestors = Column(String(500))
    dept_name = Column(String(30))
    status = Column(String(1), default="0")
    del_flag = Column(String(1), default="0")


class Todo(Base):
    __tablename__ = "shjl_todos"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    type = Column(String(20), default="task")
    priority = Column(String(20), default="normal")
    status = Column(String(20), default="pending")
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

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), nullable=False)
    title = Column(String(100))
    summary = Column(Text)
    is_pinned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)


class ChatMessage(Base):
    __tablename__ = "shjl_chat_messages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    session_id = Column(String(36), ForeignKey("shjl_chat_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")
    meta_data = Column(JSON)
    created_at = Column(DateTime, default=func.now())


class AnalysisReport(Base):
    __tablename__ = "shjl_analysis_reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    source_type = Column(String(20))
    source_id = Column(String(36), nullable=False)
    title = Column(String(255))
    detailed_report = Column(Text)
    conclusion_cards = Column(JSON)
    mind_map_data = Column(JSON)
    raw_response = Column(JSON)
    created_at = Column(DateTime, default=func.now())


class MeetingRoom(Base):
    """会议室主数据。"""

    __tablename__ = "shjl_meeting_rooms"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    room_name = Column(String(120), nullable=False)
    site_name = Column(String(100), nullable=False)
    location_text = Column(String(200), nullable=False)
    building_name = Column(String(100))
    floor_label = Column(String(50))
    capacity = Column(Integer, nullable=False, default=0)
    seat_layout = Column(String(50))
    manager_name = Column(String(50))
    manager_user_id = Column(BigInteger)
    sort_order = Column(Integer)
    is_enabled = Column(Boolean, nullable=False, default=True)
    source_file = Column(String(100))
    source_sheet = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Meeting(Base):
    """会议主表，统一承载预约、链接导入、录音转写与纪要。"""

    __tablename__ = "shjl_meetings"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    organizer_user_id = Column(BigInteger)
    organizer_id = Column(String(36))
    status = Column(String(20), nullable=False, default="scheduled")
    channel = Column(String(20), nullable=False, default="web")
    source_type = Column(String(30), nullable=False, default="manual")
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    room_id = Column(String(36))
    location = Column(String(255))
    participants_json = Column(JSON)
    meeting_url = Column(String(500))
    wecom_schedule_id = Column(String(100))
    audio_file_key = Column(String(255))
    summary = Column(Text)
    transcript = Column(LONGTEXT)
    sync_status = Column(String(20), nullable=False, default="none")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class StrategyDaily(Base):
    __tablename__ = "shjl_strategy_daily"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    report_date = Column(String(10), nullable=False)
    query_key = Column(String(255), nullable=False)
    title = Column(String(255))
    content = Column(Text)
    url = Column(String(500))
    subtext = Column(String(100))
    color = Column(String(20))
    icon_type = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
