from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

import uuid


@dataclass
class SessionState:
    """多轮对话状态。"""

    intent: str = ""
    collected_params: Dict[str, Any] = field(default_factory=dict)
    missing_params: List[str] = field(default_factory=list)
    status: str = "idle"
    session_id: str = ""
    user_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


REQUIRED_PARAMS = {
    "meeting_create": ["title", "start_time", "location"],
    "meeting_update": ["title"],
    "meeting_cancel": ["title"],
    "room_query": [],
    "room_book": ["title", "start_time", "room_name"],
    "meeting_query": [],
    "minutes_import": ["meeting_url"],
    "minutes_record": ["transcript"],
    "group": ["group_name", "members"],
    "todo": ["title", "owner"],
}


PARAM_NAMES_CN = {
    "title": "会议主题",
    "start_time": "开始时间",
    "end_time": "结束时间",
    "duration": "会议时长",
    "participants": "参会人员",
    "room_id": "会议室ID",
    "room_name": "会议室名称",
    "site_name": "园区归属",
    "location": "会议地点",
    "description": "会议描述",
    "meeting_url": "会议链接",
    "meeting_id": "会议ID",
    "transcript": "转写文本",
    "status": "会议状态",
    "group_name": "群聊名称",
    "members": "群成员",
    "owner": "负责人",
    "priority": "优先级",
}


class SessionStateManager:
    """对话状态管理器。"""

    def __init__(self) -> None:
        self._sessions: Dict[str, SessionState] = {}

    def create_session(self, user_id: str, intent: str) -> SessionState:
        session_id = str(uuid.uuid4())
        state = SessionState(
            session_id=session_id,
            user_id=user_id,
            intent=intent,
            status="collecting",
            missing_params=REQUIRED_PARAMS.get(intent, []).copy(),
        )
        self._sessions[session_id] = state
        return state

    def delete_session(self, session_id: str) -> bool:
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def merge_params(self, session_id: str, new_params: Dict[str, Any]) -> SessionState:
        state = self._sessions.get(session_id)
        if not state:
            raise ValueError(f"Session {session_id} not found")

        state.collected_params.update({k: v for k, v in new_params.items() if v not in [None, "", []]})
        state.missing_params = self._calculate_missing_params(state.intent, state.collected_params)
        state.status = "ready" if not state.missing_params else "collecting"
        state.updated_at = datetime.now()
        return state

    def check_completeness(self, session_id: str) -> Dict[str, Any]:
        state = self._sessions.get(session_id)
        if not state:
            return {"complete": False, "error": "Session not found"}

        state.missing_params = self._calculate_missing_params(state.intent, state.collected_params)
        state.status = "ready" if not state.missing_params else "collecting"
        if not state.missing_params:
            return {
                "complete": True,
                "session_id": session_id,
                "intent": state.intent,
                "params": state.collected_params,
            }
        return {
            "complete": False,
            "session_id": session_id,
            "intent": state.intent,
            "missing_params": state.missing_params,
            "collected_params": state.collected_params,
        }

    def get_user_active_session(self, user_id: str) -> Optional[SessionState]:
        for state in self._sessions.values():
            if state.user_id == user_id and state.status in ["collecting", "ready"]:
                return state
        return None

    def clear_session(self, session_id: str) -> bool:
        return self.delete_session(session_id)

    def _calculate_missing_params(self, intent: str, params: Dict[str, Any]) -> List[str]:
        required = REQUIRED_PARAMS.get(intent, [])
        missing = []
        for field in required:
            value = params.get(field)
            if value in [None, "", []]:
                missing.append(field)
        return missing


session_manager = SessionStateManager()
