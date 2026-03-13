import asyncio
import json
from typing import Any, Dict, List

from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..routers.todos import create_todo_internal
from ..services.intent_service import intent_service
from ..services.meeting_service import MeetingServiceError, meeting_service
from ..services.session_state_manager import SessionState, session_manager


MEETING_INTENTS = {
    "meeting_create",
    "meeting_update",
    "meeting_cancel",
    "room_query",
    "room_book",
    "meeting_query",
    "minutes_import",
    "minutes_record",
}

AUTO_EXECUTE_INTENTS = {"room_query", "meeting_query"}


class DialogueProcessor:
    """多轮对话处理器。"""

    def __init__(self) -> None:
        self.session_manager = session_manager
        self.intent_service = intent_service

    async def process_message(
        self,
        user_input: str,
        user_id: str,
        context_messages: List[Dict] = None,
        db: Session = None,
    ) -> Dict[str, Any]:
        active_session = self.session_manager.get_user_active_session(user_id)
        if active_session and active_session.status in ["collecting", "ready"]:
            return await self._handle_ongoing_session(user_input, active_session, context_messages, db)

        intent_result = self.intent_service.detect_intent(user_input, context_messages)
        intent = intent_result.get("intent", "chat")
        confidence = intent_result.get("confidence", 0)
        if intent == "chat" or confidence < 0.6:
            return {"type": "chat", "content": None, "data": None}

        session = self.session_manager.create_session(user_id, intent)
        extracted_params = self.intent_service.extract_params_with_llm(
            user_input=user_input,
            intent=intent,
            context_messages=context_messages,
        )
        self.session_manager.merge_params(session.session_id, extracted_params)
        completeness = self.session_manager.check_completeness(session.session_id)

        if completeness["complete"]:
            if intent in AUTO_EXECUTE_INTENTS:
                return await self._execute_function(session, db)
            confirmation = self.intent_service.generate_confirmation_prompt(intent, session.collected_params)
            return {
                "type": "confirmation",
                "content": confirmation,
                "data": {
                    "session_id": session.session_id,
                    "intent": intent,
                    "params": session.collected_params,
                },
            }

        question = self.intent_service.generate_clarification_question(
            session.missing_params,
            session.collected_params,
            intent,
        )
        return {
            "type": "clarification",
            "content": question,
            "data": {
                "session_id": session.session_id,
                "intent": intent,
                "missing_params": session.missing_params,
                "collected_params": session.collected_params,
            },
        }

    async def _handle_ongoing_session(
        self,
        user_input: str,
        session: SessionState,
        context_messages: List[Dict] = None,
        db: Session = None,
    ) -> Dict[str, Any]:
        confirmation_keywords = ["是", "确认", "确定", "可以", "yes", "ok", "执行"]
        if session.status == "ready" and any(keyword in user_input for keyword in confirmation_keywords):
            return await self._execute_function(session, db)

        cancel_keywords = ["取消", "不用了", "算了", "no", "cancel", "放弃"]
        if any(keyword in user_input for keyword in cancel_keywords):
            self.session_manager.clear_session(session.session_id)
            return {"type": "chat", "content": "已取消本次操作。", "data": None}

        extracted_params = self.intent_service.extract_params_with_llm(
            user_input=user_input,
            intent=session.intent,
            existing_params=session.collected_params,
            context_messages=context_messages,
        )
        self.session_manager.merge_params(session.session_id, extracted_params)
        completeness = self.session_manager.check_completeness(session.session_id)

        if completeness["complete"]:
            if session.intent in AUTO_EXECUTE_INTENTS:
                return await self._execute_function(session, db)
            confirmation = self.intent_service.generate_confirmation_prompt(
                session.intent,
                session.collected_params,
            )
            return {
                "type": "confirmation",
                "content": confirmation,
                "data": {
                    "session_id": session.session_id,
                    "intent": session.intent,
                    "params": session.collected_params,
                },
            }

        question = self.intent_service.generate_clarification_question(
            session.missing_params,
            session.collected_params,
            session.intent,
        )
        return {
            "type": "clarification",
            "content": question,
            "data": {
                "session_id": session.session_id,
                "intent": session.intent,
                "missing_params": session.missing_params,
                "collected_params": session.collected_params,
            },
        }

    async def _execute_function(self, session: SessionState, db: Session = None) -> Dict[str, Any]:
        try:
            if session.intent in MEETING_INTENTS:
                result = meeting_service.execute_intent(
                    db=db,
                    intent=session.intent,
                    params=session.collected_params,
                    current_user_id=session.user_id,
                )
            elif session.intent == "todo":
                result = await self._create_todo(session.collected_params, db, session.user_id)
            elif session.intent == "group":
                result = self._create_group(session.collected_params)
            else:
                result = {"success": False, "message": "暂不支持的意图"}

            self.session_manager.clear_session(session.session_id)
            if result.get("success"):
                return {"type": "execution", "content": result.get("message", "操作完成。"), "data": result}
            return {"type": "chat", "content": result.get("message", "操作失败。"), "data": result}
        except MeetingServiceError as exc:
            self.session_manager.clear_session(session.session_id)
            detail = exc.message
            if exc.extra:
                detail = f"{detail}\n{json.dumps(exc.extra, ensure_ascii=False)}"
            return {"type": "chat", "content": detail, "data": {"error": exc.message, "code": exc.code}}
        except Exception as exc:  # pragma: no cover
            self.session_manager.clear_session(session.session_id)
            return {"type": "chat", "content": f"执行出错：{str(exc)}", "data": {"error": str(exc)}}

    async def _create_todo(self, params: Dict[str, Any], db: Session = None, user_id: str = None) -> Dict[str, Any]:
        if not db or not user_id:
            return {"success": False, "message": "当前无法创建待办。"}

        title = params.get("title", "未命名待办")
        owner = params.get("owner", "我")
        priority_map = {
            "紧急": "urgent",
            "urgent": "urgent",
            "高": "high",
            "high": "high",
            "重要": "high",
            "中": "normal",
            "normal": "normal",
            "低": "low",
            "low": "low",
        }
        priority = priority_map.get(str(params.get("priority", "high")).lower(), "high")
        new_todo = create_todo_internal(
            db=db,
            title=title,
            summary=params.get("description", ""),
            priority=priority,
            category="task",
            due_date=params.get("due_date"),
            assignee=owner,
            user_id=user_id,
        )
        return {
            "success": True,
            "message": f"已创建待办《{title}》，负责人：{owner}。",
            "data": new_todo.model_dump() if hasattr(new_todo, "model_dump") else {},
        }

    def _create_group(self, params: Dict[str, Any]) -> Dict[str, Any]:
        group_name = params.get("group_name", "未命名群聊")
        members = params.get("members", [])
        members_text = ", ".join(members) if isinstance(members, list) else str(members)
        return {
            "success": True,
            "message": f"群聊《{group_name}》已进入待接入状态，成员：{members_text}。",
            "data": {"group_name": group_name, "members": members},
        }

    def create_streaming_response(
        self,
        content: str,
        session_id: str = None,
        save_message_func=None,
    ) -> StreamingResponse:
        async def generate():
            for char in content:
                yield f"data: {json.dumps({'content': char})}\n\n"
                await asyncio.sleep(0.005)

            metadata = {"type": "parameter_collection"}
            if session_id:
                metadata["session_id"] = session_id
            yield f"data: {json.dumps({'metadata': metadata})}\n\n"
            yield "data: [DONE]\n\n"

            if save_message_func:
                save_message_func(content)

        return StreamingResponse(generate(), media_type="text/event-stream")


dialogue_processor = DialogueProcessor()
