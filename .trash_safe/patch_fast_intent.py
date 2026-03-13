import re

with open('server/services/intent_service.py', 'r') as f:
    text = f.read()

# 1. Modify `detect_intent` to NOT use LLM if heuristic says chat, or just completely disable LLM for intent detection
tgt1 = '''    def detect_intent(self, user_input: str, context_messages: List[Dict] = None) -> Dict[str, Any]:
        heuristic = self._heuristic_detect_intent(user_input)
        if heuristic["intent"] != "chat":
            return heuristic'''

repl1 = '''    def detect_intent(self, user_input: str, context_messages: List[Dict] = None) -> Dict[str, Any]:
        return self._heuristic_detect_intent(user_input)
    
    def detect_intent_legacy(self, user_input: str, context_messages: List[Dict] = None) -> Dict[str, Any]:
        heuristic = self._heuristic_detect_intent(user_input)
        if heuristic["intent"] != "chat":
            return heuristic'''

if tgt1 in text:
    text = text.replace(tgt1, repl1)
else:
    print("tgt1 not found")

# 2. Delete all meeting-related intents from heuristic
tgt2 = '''        rules = [
            ("minutes_import", [r"https?://", r"导入.*会议链接", r"纪要链接"]),
            ("minutes_record", [r"录音", r"转写", r"纪要"]),
            ("meeting_cancel", [r"取消.*会议", r"取消.*会", r"删掉.*会议"]),
            ("meeting_update", [r"修改.*会议", r"调整.*会议", r"改到.*会议", r"延期.*会议"]),
            ("room_book", [r"预约.*会议室", r"预定.*会议室", r"订.*会议室", r"定个.*会议室"]),
            ("room_query", [r"会议室", r"空闲.*会议室", r"有哪些会议室", r"会议室占用"]),
            ("meeting_query", [r"我的会议", r"有哪些会议", r"查.*会议", r"会议列表"]),
            ("meeting_create", [r"创建.*会议", r"安排.*会议", r"开个会", r"约个会", r"组织.*会议"]),
            ("group", [r"建群", r"群聊", r"拉个群"]),
            ("todo", [r"待办", r"任务", r"提醒我", r"帮我记一下"]),
        ]'''

repl2 = '''        rules = [
            ("group", [r"建群", r"群聊", r"拉个群"]),
            ("todo", [r"待办", r"任务", r"提醒我", r"帮我记一下"]),
        ]'''

if tgt2 in text:
    text = text.replace(tgt2, repl2)
else:
    print("tgt2 not found")


with open('server/services/intent_service.py', 'w') as f:
    f.write(text)

