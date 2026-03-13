import re

with open('server/services/dialogue_processor.py', 'r') as f:
    text = f.read()

# 1. remove branch from process_message
#     if session.intent == "create_meeting":
#         return await self._handle_create_meeting_turn(session, user_input)
text = re.sub(
    r'        if session\.intent == "create_meeting":.*?elif session\.intent == "create_todo":',
    r'        if session.intent == "create_todo":',
    text,
    flags=re.DOTALL
)

# 2. remove intent handling switch
#     if intent_name == "create_meeting":
#         ...
text = re.sub(
    r'        if intent_name == "create_meeting":.*?elif intent_name == "create_todo":',
    r'        if intent_name == "create_todo":',
    text,
    flags=re.DOTALL
)

with open('server/services/dialogue_processor.py', 'w') as f:
    f.write(text)
