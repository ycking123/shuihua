"""
企微多轮对话会话状态管理器
负责管理企微用户的多轮对话参数收集状态
"""

import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class WecomSessionState:
    """企微会话状态"""

    user_id: str = ""
    intent: str = ""
    collected_params: Dict[str, Any] = field(default_factory=dict)
    missing_params: List[str] = field(default_factory=list)
    status: str = "idle"
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    chat_id: Optional[str] = None
    message_history: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "user_id": self.user_id,
            "intent": self.intent,
            "collected_params": self.collected_params,
            "missing_params": self.missing_params,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "chat_id": self.chat_id,
            "message_history": self.message_history,
        }

    def is_expired(self, timeout: int = 300) -> bool:
        """检查会话是否过期"""
        return time.time() - self.updated_at > timeout

    def add_message(self, role: str, content: str, extracted_params: Dict[str, Any] = None):
        """添加消息到历史记录"""
        self.message_history.append(
            {
                "role": role,
                "content": content,
                "timestamp": time.time(),
                "extracted_params": extracted_params or {},
            }
        )
        if len(self.message_history) > 10:
            self.message_history = self.message_history[-10:]

    def update_last_message_params(self, extracted_params: Dict[str, Any]):
        """更新最后一条消息的抽取结果"""
        if not self.message_history:
            return
        self.message_history[-1]["extracted_params"] = extracted_params or {}

    def get_recent_messages(self, count: int = 3) -> List[Dict[str, Any]]:
        """获取最近N条消息"""
        return self.message_history[-count:] if self.message_history else []

    def get_recent_user_messages(self, count: int = 3) -> List[Dict[str, Any]]:
        """获取最近N条用户消息"""
        user_messages = [msg for msg in self.message_history if msg.get("role") == "user"]
        return user_messages[-count:] if user_messages else []


REQUIRED_PARAMS = {
    "meeting": ["topic", "start_time"],
    "group_chat": ["chat_name", "user_ids"],
    "todo": ["title"],
}


PARAM_NAMES_CN = {
    "topic": "会议主题",
    "start_time": "会议时间",
    "duration": "会议时长",
    "attendees": "参会人员",
    "chat_name": "群聊名称",
    "user_ids": "群成员",
    "title": "待办标题",
    "description": "待办描述",
    "due_date": "截止时间",
    "assignee": "负责人",
    "priority": "优先级",
}


class WecomSessionManager:
    """企微会话状态管理器"""

    def __init__(self, timeout: int = 300):
        self._sessions: Dict[str, WecomSessionState] = {}
        self._timeout = timeout

    def _normalize_intent(self, intent: str) -> str:
        """统一意图名称，兼容旧值"""
        intent_alias = {
            "meeting": "meeting",
            "group": "group_chat",
            "group_chat": "group_chat",
            "todo": "todo",
        }
        return intent_alias.get(intent, intent or "")

    def create_session(self, user_id: str, intent: str, chat_id: str = None) -> WecomSessionState:
        """创建新的会话状态"""
        normalized_intent = self._normalize_intent(intent)
        required = REQUIRED_PARAMS.get(normalized_intent, [])
        state = WecomSessionState(
            user_id=user_id,
            intent=normalized_intent,
            status="collecting",
            missing_params=required.copy(),
            collected_params={},
            chat_id=chat_id,
            created_at=time.time(),
            updated_at=time.time(),
        )
        self._sessions[user_id] = state
        return state

    def get_session(self, user_id: str) -> Optional[WecomSessionState]:
        """获取用户会话状态"""
        state = self._sessions.get(user_id)
        if state and state.is_expired(self._timeout):
            del self._sessions[user_id]
            return None
        return state

    def update_session(self, user_id: str, **kwargs) -> Optional[WecomSessionState]:
        """更新会话状态"""
        state = self._sessions.get(user_id)
        if not state:
            return None

        for key, value in kwargs.items():
            if hasattr(state, key):
                setattr(state, key, value)

        if "intent" in kwargs:
            state.intent = self._normalize_intent(state.intent)

        state.updated_at = time.time()
        return state

    def delete_session(self, user_id: str) -> bool:
        """删除会话状态"""
        if user_id in self._sessions:
            del self._sessions[user_id]
            return True
        return False

    def merge_params(self, user_id: str, new_params: Dict[str, Any]) -> Optional[WecomSessionState]:
        """合并新参数到会话状态"""
        state = self._sessions.get(user_id)
        if not state:
            return None

        state.intent = self._normalize_intent(state.intent)
        state.collected_params.update(new_params or {})
        required = REQUIRED_PARAMS.get(state.intent, [])
        state.missing_params = [
            param
            for param in required
            if param not in state.collected_params or not state.collected_params[param]
        ]
        state.status = "ready" if not state.missing_params else "collecting"
        state.updated_at = time.time()
        return state

    def check_completeness(self, user_id: str) -> Dict[str, Any]:
        """检查参数完整性"""
        state = self._sessions.get(user_id)
        if not state:
            return {"complete": False, "error": "Session not found"}

        state.intent = self._normalize_intent(state.intent)
        required = REQUIRED_PARAMS.get(state.intent, [])
        missing = [
            param
            for param in required
            if param not in state.collected_params or not state.collected_params[param]
        ]
        state.missing_params = missing

        if not missing:
            state.status = "ready"
            return {
                "complete": True,
                "user_id": user_id,
                "intent": state.intent,
                "params": state.collected_params,
            }

        state.status = "collecting"
        return {
            "complete": False,
            "user_id": user_id,
            "intent": state.intent,
            "missing_params": missing,
            "collected_params": state.collected_params,
        }

    def generate_recent_user_summary(self, user_id: str, count: int = 3) -> str:
        """生成最近N条用户输入摘要"""
        state = self._sessions.get(user_id)
        if not state:
            return ""

        recent_msgs = state.get_recent_user_messages(count)
        lines = []
        for index, msg in enumerate(recent_msgs, 1):
            content = (msg.get("content") or "").strip()
            if not content:
                continue
            if len(content) > 80:
                content = content[:80] + "..."
            lines.append(f"{index}. {content}")
        return "\n".join(lines)

    def generate_param_collection_context(self, user_id: str, count: int = 3) -> str:
        """生成给参数抽取使用的多轮上下文"""
        state = self._sessions.get(user_id)
        if not state:
            return ""

        sections = []
        recent_summary = self.generate_recent_user_summary(user_id, count=count)
        if recent_summary:
            sections.append("最近3条用户输入：")
            sections.append(recent_summary)

        if state.collected_params:
            sections.append("已识别参数：")
            sections.append(json.dumps(state.collected_params, ensure_ascii=False))

        if state.missing_params:
            missing_names = [PARAM_NAMES_CN.get(param, param) for param in state.missing_params]
            sections.append("当前缺失参数：")
            sections.append("、".join(missing_names))

        return "\n".join(sections)

    def generate_collected_params_summary(self, user_id: str) -> str:
        """生成人类可读的已识别信息摘要"""
        state = self._sessions.get(user_id)
        if not state:
            return ""

        lines = []
        if state.intent == "meeting":
            if state.collected_params.get("topic"):
                lines.append(f"会议主题：{state.collected_params['topic']}")
            if state.collected_params.get("start_time"):
                lines.append(f"会议时间：{state.collected_params['start_time']}")
            attendees = state.collected_params.get("attendees")
            if attendees:
                attendee_text = "、".join(attendees) if isinstance(attendees, list) else str(attendees)
                lines.append(f"参会人员：{attendee_text}")
        elif state.intent == "group_chat":
            if state.collected_params.get("chat_name"):
                lines.append(f"群聊名称：{state.collected_params['chat_name']}")
            user_ids = state.collected_params.get("user_ids")
            if user_ids:
                user_text = "、".join(user_ids) if isinstance(user_ids, list) else str(user_ids)
                lines.append(f"群成员：{user_text}")
        elif state.intent == "todo":
            if state.collected_params.get("title"):
                lines.append(f"待办标题：{state.collected_params['title']}")
            if state.collected_params.get("due_date"):
                lines.append(f"截止时间：{state.collected_params['due_date']}")
            if state.collected_params.get("assignee"):
                lines.append(f"负责人：{state.collected_params['assignee']}")

        return "\n".join(lines)

    def generate_missing_examples(self, user_id: str) -> str:
        """根据意图生成补参示例"""
        state = self._sessions.get(user_id)
        if not state:
            return "请重新描述您的需求。"

        if state.intent == "meeting":
            return "请直接补充缺失字段，例如：主题是项目复盘，明天下午3点开，参会人有张三和李四。"
        if state.intent == "group_chat":
            return "请直接补充缺失字段，例如：群名叫华南项目群，成员有张三、李四、王五。"
        if state.intent == "todo":
            return "请直接补充缺失字段，例如：提醒王磊今天18点前提交周报，优先级高。"
        return "请直接补充缺失字段。"

    def generate_missing_prompt(self, user_id: str) -> str:
        """生成缺失参数提示"""
        state = self._sessions.get(user_id)
        if not state:
            return "会话已过期，请重新开始。"

        if not state.missing_params:
            return "参数已收集完整，可以执行操作。"

        missing_names = [PARAM_NAMES_CN.get(param, param) for param in state.missing_params]
        prompt_parts = []

        history_summary = self.generate_recent_user_summary(user_id, count=3)
        if history_summary:
            prompt_parts.append("最近3条用户输入：")
            prompt_parts.append(history_summary)
            prompt_parts.append("")

        collected_summary = self.generate_collected_params_summary(user_id)
        if collected_summary:
            prompt_parts.append("已识别信息：")
            prompt_parts.append(collected_summary)
            prompt_parts.append("")

        prompt_parts.append(f"当前还缺少：{', '.join(missing_names)}")
        prompt_parts.append(self.generate_missing_examples(user_id))
        return "\n".join(prompt_parts)

    def generate_confirmation_prompt(self, user_id: str) -> str:
        """生成确认提示"""
        state = self._sessions.get(user_id)
        if not state:
            return "会话不存在。"

        params = state.collected_params
        if state.intent == "meeting":
            prompt = "请确认以下会议信息：\n"
            prompt += f"主题：{params.get('topic', '未填写')}\n"
            prompt += f"时间：{params.get('start_time', '未填写')}\n"
            if params.get("duration"):
                prompt += f"时长：{int(params.get('duration', 3600) / 60)}分钟\n"
            attendees = params.get("attendees", [])
            if attendees:
                attendee_text = "、".join(attendees) if isinstance(attendees, list) else str(attendees)
                prompt += f"参会人员：{attendee_text}\n"
            prompt += '\n回复"确认"创建会议，回复"取消"放弃。'
            return prompt

        if state.intent == "group_chat":
            prompt = "请确认以下群聊信息：\n"
            prompt += f"群聊名称：{params.get('chat_name', '未填写')}\n"
            user_ids = params.get("user_ids", [])
            if user_ids:
                user_text = "、".join(user_ids) if isinstance(user_ids, list) else str(user_ids)
                prompt += f"群成员：{user_text}\n"
            prompt += '\n回复"确认"创建群聊，回复"取消"放弃。'
            return prompt

        if state.intent == "todo":
            prompt = "请确认以下待办信息：\n"
            prompt += f"待办标题：{params.get('title', '未填写')}\n"
            if params.get("due_date"):
                prompt += f"截止时间：{params['due_date']}\n"
            if params.get("assignee"):
                prompt += f"负责人：{params['assignee']}\n"
            if params.get("priority"):
                prompt += f"优先级：{params['priority']}\n"
            prompt += '\n回复"确认"创建待办，回复"取消"放弃。'
            return prompt

        return "参数已收集完整，是否执行？"

    def clear_session(self, user_id: str) -> bool:
        """清空会话状态"""
        return self.delete_session(user_id)

    def cleanup_expired(self):
        """清理过期会话"""
        expired_users = []
        for user_id, state in self._sessions.items():
            if state.is_expired(self._timeout):
                expired_users.append(user_id)

        for user_id in expired_users:
            del self._sessions[user_id]

        return len(expired_users)


wecom_session_manager = WecomSessionManager(timeout=300)
