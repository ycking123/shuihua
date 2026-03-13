import json
import re
from typing import Any, Dict, List, Optional

from ..services.llm_factory import LLMFactory
from ..services.session_state_manager import PARAM_NAMES_CN


INTENTS = {
    "meeting_create": "创建会议",
    "meeting_update": "修改会议",
    "meeting_cancel": "取消会议",
    "room_query": "查询会议室",
    "room_book": "预约会议室",
    "meeting_query": "查询会议",
    "minutes_import": "导入会议链接",
    "minutes_record": "录音转写纪要",
    "group": "创建群聊",
    "todo": "创建待办",
    "chat": "普通聊天",
}


class IntentService:
    """意图识别与参数抽取服务。"""

    def __init__(self) -> None:
        self.provider = LLMFactory.get_provider("MiniMaxAI/MiniMax-M2.5")
        self.model_name = "MiniMaxAI/MiniMax-M2.5"

    def detect_intent(self, user_input: str, context_messages: List[Dict] = None) -> Dict[str, Any]:
        return self._heuristic_detect_intent(user_input)
    
    def detect_intent_legacy(self, user_input: str, context_messages: List[Dict] = None) -> Dict[str, Any]:
        heuristic = self._heuristic_detect_intent(user_input)
        if heuristic["intent"] != "chat":
            return heuristic

        system_prompt = """
你是会议助手的意图识别器，只能输出 JSON。

可选意图：
- meeting_create
- meeting_update
- meeting_cancel
- room_query
- room_book
- meeting_query
- minutes_import
- minutes_record
- group
- todo
- chat

规则：
1. 只有当用户明确表达会议、会议室、纪要、录音、群聊、待办诉求时，才能返回对应意图。
2. 会议相关若置信度低于 0.6，一律返回 chat。
3. 只输出形如 {"intent":"...", "confidence":0.0} 的 JSON。
"""
        messages = [{"role": "system", "content": system_prompt}]
        if context_messages:
            for item in context_messages[-3:]:
                messages.append({"role": item.get("role", "user"), "content": item.get("content", "")})
        messages.append({"role": "user", "content": user_input})

        try:
            response = self.provider.chat_stream(model=self.model_name, messages=messages)
            content = "".join(chunk for chunk in response)
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if not match:
                return {"intent": "chat", "confidence": 1.0}
            data = json.loads(match.group())
            intent = data.get("intent", "chat")
            confidence = float(data.get("confidence", 0))
            if confidence < 0.6:
                return {"intent": "chat", "confidence": confidence}
            if intent not in INTENTS:
                return {"intent": "chat", "confidence": 1.0}
            return {"intent": intent, "confidence": confidence}
        except Exception:
            return {"intent": "chat", "confidence": 1.0}

    def extract_params_with_llm(
        self,
        user_input: str,
        intent: str,
        existing_params: Dict = None,
        context_messages: List[Dict] = None,
    ) -> Dict[str, Any]:
        params = self._heuristic_extract(user_input, intent)
        if params:
            return params

        if intent not in INTENTS or intent == "chat":
            return {}

        system_prompt = f"""
你是会议助手的参数抽取器，只能输出 JSON。
当前意图：{intent}

会议相关参数 schema：
- title
- start_time
- end_time
- duration
- participants
- room_id
- room_name
- site_name
- location
- description
- meeting_url
- transcript
- status

要求：
1. 只提取用户明确说出的信息，不允许猜测。
2. 时间保持用户原始表达，不要自行换算。
3. 只输出 JSON；缺失字段不要输出。
"""
        messages = [{"role": "system", "content": system_prompt}]
        if existing_params:
            messages.append(
                {
                    "role": "system",
                    "content": f"已收集参数：{json.dumps(existing_params, ensure_ascii=False)}",
                }
            )
        if context_messages:
            context_text = "\n".join(
                [f"{item.get('role', 'user')}: {item.get('content', '')}" for item in context_messages[-5:]]
            )
            messages.append({"role": "system", "content": f"对话上下文：\n{context_text}"})
        messages.append({"role": "user", "content": user_input})

        try:
            response = self.provider.chat_stream(model=self.model_name, messages=messages)
            content = "".join(chunk for chunk in response)
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if not match:
                return {}
            data = json.loads(match.group())
            return {k: v for k, v in data.items() if v not in [None, "", []]}
        except Exception:
            return {}

    def generate_clarification_question(
        self,
        missing_params: List[str],
        collected_params: Dict,
        intent: str,
    ) -> str:
        collected_lines = []
        for key in ["title", "start_time", "room_name", "location", "meeting_url"]:
            value = collected_params.get(key)
            if value:
                label = PARAM_NAMES_CN.get(key, key)
                if isinstance(value, list):
                    collected_lines.append(f"{label}：{', '.join(value)}")
                else:
                    collected_lines.append(f"{label}：{value}")

        missing_names = [PARAM_NAMES_CN.get(item, item) for item in missing_params]
        if collected_lines:
            return "已记录信息：\n" + "\n".join(collected_lines) + f"\n\n还缺少：{'、'.join(missing_names)}。请继续补充。"
        return f"请补充以下信息：{'、'.join(missing_names)}。"

    def generate_confirmation_prompt(self, intent: str, params: Dict) -> str:
        if intent in {"meeting_create", "room_book"}:
            lines = [
                "请确认以下会议信息：",
                f"主题：{params.get('title')}",
                f"开始时间：{params.get('start_time')}",
            ]
            if params.get("end_time"):
                lines.append(f"结束时间：{params.get('end_time')}")
            elif params.get("duration"):
                lines.append(f"时长：{params.get('duration')}")
            if params.get("room_name"):
                lines.append(f"会议室：{params.get('room_name')}")
            elif params.get("location"):
                lines.append(f"地点：{params.get('location')}")
            if params.get("participants"):
                participants = params.get("participants")
                if isinstance(participants, list):
                    lines.append(f"参会人：{', '.join(participants)}")
                else:
                    lines.append(f"参会人：{participants}")
            lines.append("确认执行请回复“确认”。")
            return "\n".join(lines)

        if intent == "meeting_update":
            return f"将更新会议《{params.get('title', '未命名会议')}》，确认执行请回复“确认”。"
        if intent == "meeting_cancel":
            return f"将取消会议《{params.get('title', '未命名会议')}》，确认执行请回复“确认”。"
        if intent == "minutes_import":
            return f"将导入会议链接：{params.get('meeting_url')}，确认执行请回复“确认”。"
        if intent == "minutes_record":
            return "将保存录音纪要并生成摘要，确认执行请回复“确认”。"
        if intent == "group":
            return f"将创建群聊《{params.get('group_name', '未命名群聊')}》，确认执行请回复“确认”。"
        if intent == "todo":
            return f"将创建待办《{params.get('title', '未命名待办')}》，确认执行请回复“确认”。"
        return "参数已收集完成，确认执行请回复“确认”。"

    def _heuristic_detect_intent(self, user_input: str) -> Dict[str, Any]:
        text = user_input.strip()

        rules = [
            ("group", [r"建群", r"群聊", r"拉个群"]),
            ("todo", [r"待办", r"任务", r"提醒我", r"帮我记一下"]),
        ]

        for intent, patterns in rules:
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
                return {"intent": intent, "confidence": 0.9}
        return {"intent": "chat", "confidence": 1.0}

    def _heuristic_extract(self, user_input: str, intent: str) -> Dict[str, Any]:
        if intent == "chat":
            return {}

        params: Dict[str, Any] = {}
        url_match = re.search(r"https?://\S+", user_input)
        if url_match:
            params["meeting_url"] = url_match.group()

        time_match = re.search(
            r"((今天|明天|后天)?(上午|下午|晚上|中午)?\s*\d{1,2}(?::\d{1,2}|点半|点)?|"
            r"\d{4}[-/年]\d{1,2}[-/月]\d{1,2}(日)?\s*\d{0,2}:?\d{0,2})",
            user_input,
        )
        if time_match:
            params["start_time"] = time_match.group(1).strip()

        end_match = re.search(r"到\s*((上午|下午|晚上|中午)?\s*\d{1,2}(?::\d{1,2}|点半|点)?)", user_input)
        if end_match:
            params["end_time"] = end_match.group(1).strip()

        duration_match = re.search(r"(\d+\s*(分钟|分|min|小时|hour))", user_input, re.IGNORECASE)
        if duration_match:
            params["duration"] = duration_match.group(1).strip()

        room_match = re.search(r"([^\s，。；,;]{1,30}会议室)", user_input)
        if room_match:
            params["room_name"] = room_match.group(1).strip()
            if intent not in {"room_book", "room_query"}:
                params.setdefault("location", room_match.group(1).strip())

        online_match = re.search(r"(线上会议|线上|腾讯会议|视频会议)", user_input)
        if online_match and "location" not in params:
            params["location"] = online_match.group(1)

        title_patterns = [
            r"主题[是为:：]\s*([^\n，。；,;]+)",
            r"关于([^\n，。；,;]+)的会议",
            r"(?:安排|创建|组织|开|约|取消|修改)([^\n，。；,;]{2,30})会议",
        ]
        for pattern in title_patterns:
            match = re.search(pattern, user_input)
            if match:
                params["title"] = match.group(1).strip()
                break

        participants_match = re.search(r"(参会人|参与人|叫上|和|与)(.+)", user_input)
        if participants_match:
            tail = participants_match.group(2)
            names = [item.strip() for item in re.split(r"[、,，和及\-\s]+", tail) if item.strip()]
            filtered = [item for item in names if len(item) <= 8 and "会议" not in item and "会议室" not in item]
            if filtered:
                params["participants"] = filtered[:8]

        if intent == "minutes_record" and len(user_input.strip()) > 20 and "meeting_url" not in params:
            params.setdefault("transcript", user_input.strip())

        if intent in {"meeting_query", "meeting_cancel", "meeting_update"} and "title" not in params:
            plain_title = re.sub(r"(帮我|请|把|给我|一下|会议|修改|取消|查询|查看|安排|创建)", "", user_input).strip()
            if 2 <= len(plain_title) <= 30:
                params["title"] = plain_title

        if intent == "group":
            if "群" in user_input:
                params["group_name"] = re.sub(r"(建群|创建|群聊|拉个群|把|帮我)", "", user_input).strip()[:20]
            if params.get("participants"):
                params["members"] = params.pop("participants")

        if intent == "todo":
            params["title"] = params.get("title") or user_input.strip()[:40]
            if "我" in user_input:
                params["owner"] = "我"

        return {k: v for k, v in params.items() if v not in [None, "", []]}


intent_service = IntentService()
