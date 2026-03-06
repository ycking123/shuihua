"""
企微多轮对话会话状态管理器
负责管理企微用户的多轮对话参数收集状态
"""

import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class WecomSessionState:
    """企微会话状态"""
    user_id: str = ""                          # 企微用户ID
    intent: str = ""                           # 当前意图：meeting/group/todo
    collected_params: Dict[str, Any] = field(default_factory=dict)   # 已收集参数
    missing_params: List[str] = field(default_factory=list)          # 缺失参数
    status: str = "idle"                       # idle/collecting/ready
    created_at: float = field(default_factory=time.time)             # 创建时间戳
    updated_at: float = field(default_factory=time.time)             # 更新时间戳
    chat_id: Optional[str] = None              # 群聊ID（如果在群聊中）
    message_history: List[Dict[str, Any]] = field(default_factory=list)  # 历史消息记录
    
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
        """检查会话是否过期（默认5分钟）"""
        return time.time() - self.updated_at > timeout
    
    def add_message(self, role: str, content: str, extracted_params: Dict[str, Any] = None):
        """添加消息到历史记录"""
        self.message_history.append({
            "role": role,
            "content": content,
            "timestamp": time.time(),
            "extracted_params": extracted_params or {}
        })
        # 只保留最近5条消息
        if len(self.message_history) > 5:
            self.message_history = self.message_history[-5:]
    
    def get_recent_messages(self, count: int = 3) -> List[Dict[str, Any]]:
        """获取最近N条消息"""
        return self.message_history[-count:] if self.message_history else []


# 各功能的必填参数
REQUIRED_PARAMS = {
    "meeting": ["topic", "start_time"],
    "group": ["chat_name", "user_ids"],
    "todo": ["title"]
}

# 参数中文名称映射
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
    "priority": "优先级"
}


class WecomSessionManager:
    """企微会话状态管理器"""
    
    def __init__(self, timeout: int = 300):
        # 内存中存储会话状态 {user_id: WecomSessionState}
        self._sessions: Dict[str, WecomSessionState] = {}
        self._timeout = timeout  # 会话超时时间（秒）
    
    def create_session(self, user_id: str, intent: str, chat_id: str = None) -> WecomSessionState:
        """创建新的会话状态"""
        required = REQUIRED_PARAMS.get(intent, [])
        
        state = WecomSessionState(
            user_id=user_id,
            intent=intent,
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
            # 会话已过期，删除
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
        
        # 合并参数
        state.collected_params.update(new_params)
        
        # 更新缺失参数列表
        required = REQUIRED_PARAMS.get(state.intent, [])
        state.missing_params = [
            param for param in required 
            if param not in state.collected_params or not state.collected_params[param]
        ]
        
        # 更新状态
        if not state.missing_params:
            state.status = "ready"
        else:
            state.status = "collecting"
        
        state.updated_at = time.time()
        return state
    
    def check_completeness(self, user_id: str) -> Dict[str, Any]:
        """检查参数完整性"""
        state = self._sessions.get(user_id)
        if not state:
            return {"complete": False, "error": "Session not found"}
        
        required = REQUIRED_PARAMS.get(state.intent, [])
        missing = []
        
        for param in required:
            if param not in state.collected_params or not state.collected_params[param]:
                missing.append(param)
        
        state.missing_params = missing
        
        if not missing:
            state.status = "ready"
            return {
                "complete": True,
                "user_id": user_id,
                "intent": state.intent,
                "params": state.collected_params
            }
        else:
            state.status = "collecting"
            return {
                "complete": False,
                "user_id": user_id,
                "intent": state.intent,
                "missing_params": missing,
                "collected_params": state.collected_params
            }
    
    def generate_missing_prompt(self, user_id: str) -> str:
        """生成缺失参数提示，结合历史消息理解上下文"""
        state = self._sessions.get(user_id)
        if not state:
            return "会话已过期，请重新开始。"
        
        if not state.missing_params:
            return "参数已收集完整，可以执行操作。"
        
        # 生成提示
        missing_names = [PARAM_NAMES_CN.get(p, p) for p in state.missing_params]
        
        # 先显示已收集的信息
        lines = []
        
        if state.intent == "meeting":
            if state.collected_params.get("topic"):
                lines.append(f"📅 会议主题：{state.collected_params['topic']}")
            if state.collected_params.get("start_time"):
                lines.append(f"⏰ 时间：{state.collected_params['start_time']}")
            if state.collected_params.get("attendees"):
                attendees = state.collected_params["attendees"]
                if isinstance(attendees, list):
                    lines.append(f"👥 参会人：{'、'.join(attendees)}")
        
        elif state.intent == "group":
            if state.collected_params.get("chat_name"):
                lines.append(f"💬 群聊名称：{state.collected_params['chat_name']}")
            if state.collected_params.get("user_ids"):
                user_ids = state.collected_params["user_ids"]
                if isinstance(user_ids, list):
                    lines.append(f"👥 成员：{'、'.join(user_ids)}")
        
        elif state.intent == "todo":
            if state.collected_params.get("title"):
                lines.append(f"📝 待办：{state.collected_params['title']}")
            if state.collected_params.get("due_date"):
                lines.append(f"📅 截止时间：{state.collected_params['due_date']}")
            if state.collected_params.get("assignee"):
                lines.append(f"👤 负责人：{state.collected_params['assignee']}")
        
        # 构建提示
        prompt_parts = []
        
        # 添加历史消息上下文（最近3条）
        recent_msgs = state.get_recent_messages(3)
        if recent_msgs:
            prompt_parts.append("💬 对话上下文：")
            for i, msg in enumerate(recent_msgs, 1):
                role = "您" if msg.get("role") == "user" else "系统"
                content = msg.get("content", "")
                # 截断过长的内容
                if len(content) > 30:
                    content = content[:30] + "..."
                prompt_parts.append(f"  {i}. {role}：{content}")
            prompt_parts.append("")
        
        # 添加已收集的信息
        if lines:
            prompt_parts.append("已记录信息：")
            prompt_parts.extend(lines)
            prompt_parts.append("")
        
        # 添加缺失参数提示
        prompt_parts.append(f"❓ 还缺少：{', '.join(missing_names)}")
        prompt_parts.append("请补充上述信息，或提供更多细节。")
        
        return "\n".join(prompt_parts)
    
    def generate_confirmation_prompt(self, user_id: str) -> str:
        """生成确认提示"""
        state = self._sessions.get(user_id)
        if not state:
            return "会话不存在。"
        
        params = state.collected_params
        
        if state.intent == "meeting":
            prompt = "请确认以下会议信息：\n"
            prompt += f"📅 主题：{params.get('topic', '未填写')}\n"
            prompt += f"⏰ 时间：{params.get('start_time', '未填写')}\n"
            if params.get('duration'):
                prompt += f"⏱️ 时长：{int(params.get('duration', 3600)/60)}分钟\n"
            attendees = params.get('attendees', [])
            if attendees:
                if isinstance(attendees, list):
                    prompt += f"👥 参会人：{'、'.join(attendees)}\n"
                else:
                    prompt += f"👥 参会人：{attendees}\n"
            prompt += '\n回复"确认"创建会议，回复"取消"放弃。'
        
        elif state.intent == "group":
            prompt = "请确认以下群聊信息：\n"
            prompt += f"💬 群聊名称：{params.get('chat_name', '未填写')}\n"
            user_ids = params.get('user_ids', [])
            if user_ids:
                if isinstance(user_ids, list):
                    prompt += f"👥 成员：{'、'.join(user_ids)}\n"
                else:
                    prompt += f"👥 成员：{user_ids}\n"
            prompt += '\n回复"确认"创建群聊，回复"取消"放弃。'
        
        elif state.intent == "todo":
            prompt = "请确认以下待办信息：\n"
            prompt += f"📝 待办：{params.get('title', '未填写')}\n"
            if params.get('due_date'):
                prompt += f"📅 截止时间：{params['due_date']}\n"
            if params.get('assignee'):
                prompt += f"👤 负责人：{params['assignee']}\n"
            if params.get('priority'):
                prompt += f"⚡ 优先级：{params['priority']}\n"
            prompt += '\n回复"确认"创建待办，回复"取消"放弃。'
        
        else:
            prompt = "参数已收集完整，是否执行？"
        
        return prompt
    
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


# 全局企微会话状态管理器实例
wecom_session_manager = WecomSessionManager(timeout=300)  # 5分钟超时
