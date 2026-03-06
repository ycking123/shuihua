"""
会话状态管理器
负责管理多轮对话中的参数收集状态
支持功能：创建会议、创建群聊、创建待办
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json
import uuid


@dataclass
class SessionState:
    """会话状态数据结构"""
    intent: str = ""                          # 当前意图：meeting/group/todo
    collected_params: Dict[str, Any] = field(default_factory=dict)   # 已收集参数
    missing_params: List[str] = field(default_factory=list)          # 缺失参数列表
    status: str = "idle"                      # idle/collecting/ready/completed
    session_id: str = ""                      # 会话ID
    user_id: str = ""                         # 用户ID
    created_at: datetime = field(default_factory=datetime.now)       # 创建时间
    updated_at: datetime = field(default_factory=datetime.now)       # 更新时间
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "intent": self.intent,
            "collected_params": self.collected_params,
            "missing_params": self.missing_params,
            "status": self.status,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SessionState":
        """从字典创建"""
        state = cls()
        state.intent = data.get("intent", "")
        state.collected_params = data.get("collected_params", {})
        state.missing_params = data.get("missing_params", [])
        state.status = data.get("status", "idle")
        state.session_id = data.get("session_id", "")
        state.user_id = data.get("user_id", "")
        if data.get("created_at"):
            state.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("updated_at"):
            state.updated_at = datetime.fromisoformat(data["updated_at"])
        return state


# 各功能的必填参数定义
REQUIRED_PARAMS = {
    "meeting": ["title", "start_time", "participants"],
    "group": ["group_name", "members"],
    "todo": ["title", "owner"]
}

# 参数中文名称映射
PARAM_NAMES_CN = {
    "title": "会议主题",
    "start_time": "会议时间",
    "end_time": "结束时间",
    "participants": "参会人员",
    "location": "会议地点",
    "group_name": "群聊名称",
    "members": "群成员",
    "owner": "负责人",
    "priority": "优先级",
    "description": "描述"
}


class SessionStateManager:
    """会话状态管理器"""
    
    def __init__(self):
        # 内存中存储会话状态 {session_id: SessionState}
        self._sessions: Dict[str, SessionState] = {}
    
    def create_session(self, user_id: str, intent: str) -> SessionState:
        """创建新的会话状态"""
        session_id = str(uuid.uuid4())
        required = REQUIRED_PARAMS.get(intent, [])
        
        state = SessionState(
            session_id=session_id,
            user_id=user_id,
            intent=intent,
            status="collecting",
            missing_params=required.copy(),
            collected_params={},
        )
        
        self._sessions[session_id] = state
        return state
    
    def get_session(self, session_id: str) -> Optional[SessionState]:
        """获取会话状态"""
        return self._sessions.get(session_id)
    
    def update_session(self, session_id: str, **kwargs) -> Optional[SessionState]:
        """更新会话状态"""
        state = self._sessions.get(session_id)
        if not state:
            return None
        
        for key, value in kwargs.items():
            if hasattr(state, key):
                setattr(state, key, value)
        
        state.updated_at = datetime.now()
        return state
    
    def delete_session(self, session_id: str) -> bool:
        """删除会话状态"""
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False
    
    def get_or_create_session(self, user_id: str, intent: str = "") -> SessionState:
        """获取或创建会话状态"""
        # 查找用户现有的活跃会话
        for session_id, state in self._sessions.items():
            if state.user_id == user_id and state.status in ["collecting", "ready"]:
                # 如果提供了新的意图且与当前不同，重置会话
                if intent and state.intent != intent:
                    return self.create_session(user_id, intent)
                return state
        
        # 创建新会话
        if intent:
            return self.create_session(user_id, intent)
        
        # 没有意图，返回空会话
        return SessionState(user_id=user_id, status="idle")
    
    def extract_params(self, user_input: str, intent: str) -> Dict[str, Any]:
        """
        从用户输入中提取参数
        使用简单的关键词匹配，实际项目中可以使用LLM进行提取
        """
        extracted = {}
        
        if intent == "meeting":
            # 提取会议主题
            if "会" in user_input or "讨论" in user_input:
                # 简单提取：找"开"字后面的内容
                if "开" in user_input:
                    parts = user_input.split("开")
                    if len(parts) > 1:
                        title_part = parts[1].split("，")[0].split(",")[0].split(" ")[0]
                        if title_part and len(title_part) < 50:
                            extracted["title"] = title_part
            
            # 提取时间（简化版）
            time_keywords = ["明天", "后天", "今天", "下午", "上午", "晚上", "点"]
            for kw in time_keywords:
                if kw in user_input:
                    # 提取时间描述
                    extracted["start_time"] = user_input
                    break
            
            # 提取参会人员
            if "张三" in user_input or "李四" in user_input or "王五" in user_input:
                participants = []
                if "张三" in user_input:
                    participants.append("张三")
                if "李四" in user_input:
                    participants.append("李四")
                if "王五" in user_input:
                    participants.append("王五")
                if participants:
                    extracted["participants"] = participants
        
        elif intent == "group":
            # 提取群聊名称
            if "群" in user_input:
                extracted["group_name"] = user_input.replace("创建", "").replace("群聊", "").replace("群", "").strip()
            
            # 提取成员
            members = []
            if "张三" in user_input:
                members.append("张三")
            if "李四" in user_input:
                members.append("李四")
            if "王五" in user_input:
                members.append("王五")
            if members:
                extracted["members"] = members
        
        elif intent == "todo":
            # 提取待办标题
            if "做" in user_input or "完成" in user_input:
                extracted["title"] = user_input
            
            # 提取负责人
            if "我" in user_input:
                extracted["owner"] = "我"
            elif "张三" in user_input:
                extracted["owner"] = "张三"
            elif "李四" in user_input:
                extracted["owner"] = "李四"
        
        return extracted
    
    def merge_params(self, session_id: str, new_params: Dict[str, Any]) -> SessionState:
        """合并新参数到会话状态"""
        state = self._sessions.get(session_id)
        if not state:
            raise ValueError(f"Session {session_id} not found")
        
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
        
        state.updated_at = datetime.now()
        return state
    
    def check_completeness(self, session_id: str) -> Dict[str, Any]:
        """检查参数完整性"""
        state = self._sessions.get(session_id)
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
                "session_id": session_id,
                "intent": state.intent,
                "params": state.collected_params
            }
        else:
            state.status = "collecting"
            return {
                "complete": False,
                "session_id": session_id,
                "intent": state.intent,
                "missing_params": missing,
                "collected_params": state.collected_params
            }
    
    def generate_missing_prompt(self, session_id: str) -> str:
        """生成缺失参数提示"""
        state = self._sessions.get(session_id)
        if not state:
            return "会话已过期，请重新开始。"
        
        if not state.missing_params:
            return "参数已收集完整，可以执行操作。"
        
        # 生成提示
        missing_names = [PARAM_NAMES_CN.get(p, p) for p in state.missing_params]
        
        prompt = "还缺少以下信息：\n"
        for name in missing_names:
            prompt += f"- {name}\n"
        
        prompt += "\n请补充上述信息。"
        
        return prompt
    
    def generate_summary(self, session_id: str) -> str:
        """生成当前参数摘要"""
        state = self._sessions.get(session_id)
        if not state:
            return "会话不存在。"
        
        if state.intent == "meeting":
            summary = "当前信息：\n"
            summary += f"会议主题：{state.collected_params.get('title', '未填写')}\n"
            summary += f"时间：{state.collected_params.get('start_time', '未填写')}\n"
            participants = state.collected_params.get('participants', [])
            summary += f"参会人：{'、'.join(participants) if participants else '未填写'}\n"
            if state.collected_params.get('location'):
                summary += f"地点：{state.collected_params['location']}\n"
        
        elif state.intent == "group":
            summary = "当前信息：\n"
            summary += f"群聊名称：{state.collected_params.get('group_name', '未填写')}\n"
            members = state.collected_params.get('members', [])
            summary += f"成员：{'、'.join(members) if members else '未填写'}\n"
        
        elif state.intent == "todo":
            summary = "当前信息：\n"
            summary += f"待办标题：{state.collected_params.get('title', '未填写')}\n"
            summary += f"负责人：{state.collected_params.get('owner', '未填写')}\n"
            if state.collected_params.get('priority'):
                summary += f"优先级：{state.collected_params['priority']}\n"
        
        else:
            summary = "未知意图。"
        
        return summary
    
    def clear_session(self, session_id: str) -> bool:
        """清空会话状态（执行完成后调用）"""
        return self.delete_session(session_id)
    
    def get_user_active_session(self, user_id: str) -> Optional[SessionState]:
        """获取用户的活跃会话"""
        for session_id, state in self._sessions.items():
            if state.user_id == user_id and state.status in ["collecting", "ready"]:
                return state
        return None


# 全局会话状态管理器实例
session_manager = SessionStateManager()
