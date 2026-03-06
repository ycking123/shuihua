"""
对话处理器
集成多轮对话参数收集功能
处理用户输入 -> 意图识别 -> 参数提取 -> 完整性检查 -> 执行功能
"""

import json
import asyncio
from typing import Dict, List, Optional, Any
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..services.session_state_manager import session_manager, SessionState, REQUIRED_PARAMS, PARAM_NAMES_CN
from ..services.intent_service import intent_service


class DialogueProcessor:
    """对话处理器"""
    
    def __init__(self):
        self.session_manager = session_manager
        self.intent_service = intent_service
    
    async def process_message(self, user_input: str, user_id: str, 
                              context_messages: List[Dict] = None,
                              db: Session = None) -> Dict[str, Any]:
        """
        处理用户消息
        返回处理结果，包括：
        - type: "clarification" / "confirmation" / "execution" / "chat"
        - content: 响应内容
        - data: 附加数据
        """
        # 1. 检查是否有活跃的会话状态
        active_session = self.session_manager.get_user_active_session(user_id)
        
        # 2. 如果有活跃会话，尝试补全参数
        if active_session and active_session.status in ["collecting", "ready"]:
            return await self._handle_ongoing_session(
                user_input, active_session, context_messages, db
            )
        
        # 3. 没有活跃会话，进行意图识别
        intent_result = self.intent_service.detect_intent(user_input, context_messages)
        intent = intent_result.get("intent", "chat")
        confidence = intent_result.get("confidence", 0)
        
        # 4. 如果是普通聊天，直接返回
        if intent == "chat" or confidence < 0.5:
            return {"type": "chat", "content": None, "data": None}
        
        # 5. 创建新会话并提取参数
        session = self.session_manager.create_session(user_id, intent)
        
        # 6. 使用LLM提取参数
        extracted_params = self.intent_service.extract_params_with_llm(
            user_input, intent, context_messages=context_messages
        )
        
        # 7. 合并参数
        self.session_manager.merge_params(session.session_id, extracted_params)
        
        # 8. 检查完整性
        completeness = self.session_manager.check_completeness(session.session_id)
        
        if completeness["complete"]:
            # 参数齐全，返回确认提示
            confirmation = self.intent_service.generate_confirmation_prompt(
                intent, session.collected_params
            )
            return {
                "type": "confirmation",
                "content": confirmation,
                "data": {
                    "session_id": session.session_id,
                    "intent": intent,
                    "params": session.collected_params
                }
            }
        else:
            # 参数不齐，返回追问
            question = self.intent_service.generate_clarification_question(
                session.missing_params,
                session.collected_params,
                intent
            )
            return {
                "type": "clarification",
                "content": question,
                "data": {
                    "session_id": session.session_id,
                    "intent": intent,
                    "missing_params": session.missing_params,
                    "collected_params": session.collected_params
                }
            }
    
    async def _handle_ongoing_session(self, user_input: str, session: SessionState,
                                       context_messages: List[Dict] = None,
                                       db: Session = None) -> Dict[str, Any]:
        """处理进行中的会话"""
        
        # 检查用户是否确认执行
        confirmation_keywords = ["是", "确认", "确定", "好", "可以", "yes", "ok", "执行"]
        if session.status == "ready" and any(kw in user_input for kw in confirmation_keywords):
            # 执行功能
            return await self._execute_function(session, db)
        
        # 检查用户是否取消
        cancel_keywords = ["取消", "不", "算了", "no", "cancel", "放弃"]
        if any(kw in user_input for kw in cancel_keywords):
            self.session_manager.clear_session(session.session_id)
            return {
                "type": "chat",
                "content": "已取消操作。",
                "data": None
            }
        
        # 提取新参数
        extracted_params = self.intent_service.extract_params_with_llm(
            user_input, session.intent,
            existing_params=session.collected_params,
            context_messages=context_messages
        )
        
        # 合并参数
        self.session_manager.merge_params(session.session_id, extracted_params)
        
        # 检查完整性
        completeness = self.session_manager.check_completeness(session.session_id)
        
        if completeness["complete"]:
            # 参数齐全，返回确认提示
            confirmation = self.intent_service.generate_confirmation_prompt(
                session.intent, session.collected_params
            )
            return {
                "type": "confirmation",
                "content": confirmation,
                "data": {
                    "session_id": session.session_id,
                    "intent": session.intent,
                    "params": session.collected_params
                }
            }
        else:
            # 参数不齐，继续追问
            question = self.intent_service.generate_clarification_question(
                session.missing_params,
                session.collected_params,
                session.intent
            )
            return {
                "type": "clarification",
                "content": question,
                "data": {
                    "session_id": session.session_id,
                    "intent": session.intent,
                    "missing_params": session.missing_params,
                    "collected_params": session.collected_params
                }
            }
    
    async def _execute_function(self, session: SessionState, db: Session = None) -> Dict[str, Any]:
        """执行功能"""
        intent = session.intent
        params = session.collected_params
        
        try:
            if intent == "meeting":
                result = await self._create_meeting(params, db)
            elif intent == "group":
                result = await self._create_group(params, db)
            elif intent == "todo":
                result = await self._create_todo(params, db, session.user_id)
            else:
                result = {"success": False, "message": "未知意图"}
            
            # 清空会话
            self.session_manager.clear_session(session.session_id)
            
            if result.get("success"):
                return {
                    "type": "execution",
                    "content": result.get("message", "操作成功完成！"),
                    "data": result
                }
            else:
                return {
                    "type": "chat",
                    "content": f"操作失败：{result.get('message', '未知错误')}",
                    "data": result
                }
                
        except Exception as e:
            self.session_manager.clear_session(session.session_id)
            return {
                "type": "chat",
                "content": f"执行出错：{str(e)}",
                "data": {"error": str(e)}
            }
    
    async def _create_meeting(self, params: Dict, db: Session = None) -> Dict:
        """创建会议"""
        # 这里调用实际的会议创建逻辑
        # 暂时返回模拟结果
        title = params.get("title", "未命名会议")
        start_time = params.get("start_time", "待定")
        participants = params.get("participants", [])
        
        if isinstance(participants, list):
            participants_str = "、".join(participants)
        else:
            participants_str = str(participants)
        
        # TODO: 调用实际的会议创建API
        # from ..routers.meetings import create_meeting_internal
        # result = create_meeting_internal(db, {...})
        
        return {
            "success": True,
            "message": f"✅ 会议创建成功！\n📅 主题：{title}\n⏰ 时间：{start_time}\n👥 参会人：{participants_str}",
            "data": {
                "meeting_id": "mock_meeting_id",
                "title": title,
                "start_time": start_time,
                "participants": participants
            }
        }
    
    async def _create_group(self, params: Dict, db: Session = None) -> Dict:
        """创建群聊"""
        group_name = params.get("group_name", "未命名群聊")
        members = params.get("members", [])
        
        if isinstance(members, list):
            members_str = "、".join(members)
        else:
            members_str = str(members)
        
        # TODO: 调用实际的群聊创建API
        
        return {
            "success": True,
            "message": f"✅ 群聊创建成功！\n💬 群聊名称：{group_name}\n👥 成员：{members_str}",
            "data": {
                "group_id": "mock_group_id",
                "group_name": group_name,
                "members": members
            }
        }
    
    async def _create_todo(self, params: Dict, db: Session = None, user_id: str = None) -> Dict:
        """创建待办"""
        title = params.get("title", "未命名待办")
        owner = params.get("owner", "我")
        
        # 调用实际的待办创建逻辑
        if db and user_id:
            try:
                from ..routers.todos import create_todo_internal
                
                # 优先级映射
                priority_map = {
                    "紧急": "urgent", "urgent": "urgent",
                    "高": "high", "high": "high", "重要": "high",
                    "中": "normal", "medium": "normal", "普通": "normal",
                    "低": "low", "low": "low"
                }
                raw_priority = params.get("priority", "high")
                priority = priority_map.get(raw_priority, "high")
                
                new_todo = create_todo_internal(
                    db=db,
                    title=title,
                    summary=params.get("description", ""),
                    priority=priority,
                    category="task",
                    due_date=params.get("due_date"),
                    assignee=owner,
                    user_id=user_id
                )
                
                return {
                    "success": True,
                    "message": f"✅ 待办创建成功！\n📝 待办：{title}\n👤 负责人：{owner}",
                    "data": {
                        "todo_id": new_todo.id if hasattr(new_todo, 'id') else "created",
                        "title": title,
                        "owner": owner
                    }
                }
            except Exception as e:
                return {
                    "success": False,
                    "message": f"创建待办失败：{str(e)}"
                }
        
        return {
            "success": True,
            "message": f"✅ 待办创建成功！\n📝 待办：{title}\n👤 负责人：{owner}",
            "data": {
                "todo_id": "mock_todo_id",
                "title": title,
                "owner": owner
            }
        }
    
    def create_streaming_response(self, content: str, session_id: str = None,
                                   save_message_func = None) -> StreamingResponse:
        """创建流式响应"""
        async def generate():
            # 模拟流式输出
            for char in content:
                yield f"data: {json.dumps({'content': char})}\n\n"
                await asyncio.sleep(0.005)
            
            # 添加元数据
            metadata = {"type": "parameter_collection"}
            if session_id:
                metadata["session_id"] = session_id
            
            yield f"data: {json.dumps({'metadata': metadata})}\n\n"
            yield "data: [DONE]\n\n"
            
            # 保存消息
            if save_message_func:
                save_message_func(content)
        
        return StreamingResponse(generate(), media_type="text/event-stream")


# 全局对话处理器实例
dialogue_processor = DialogueProcessor()
