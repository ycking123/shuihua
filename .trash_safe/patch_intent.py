import re

with open('server/services/intent_service.py', 'r') as f:
    text = f.read()

# 1. remove create_meeting from prompt
req = """    1. 'manage_department_task': 提取出包含（需求、事项等）、（人名或者职务：例如前端，林某等）等信息，要求是建立一个群聊
    2. 'create_meeting': 企微预约会议或预定会议室（包含“由于某种需求预定会议”、“预约明天的会议”、“由于A需要订一个B会议室“等表述）
    3. 'create_todo': 创建个人待办事项（比如“提醒我X”、“待办：X”）
    4. 'normal_chat': 其他所有情况（日常寒暄、询问知识库等）"""
repl = """    1. 'manage_department_task': 提取出包含（需求、事项等）、（人名或者职务：例如前端，林某等）等信息，要求是建立一个群聊
    2. 'create_todo': 创建个人待办事项（比如“提醒我X”、“待办：X”）
    3. 'normal_chat': 其他所有情况（日常寒暄、询问知识库等）"""
text = text.replace(req, repl)

# 2. handle fallback removing create_meeting
text = text.replace("if intent not in ['manage_department_task', 'create_meeting', 'create_todo', 'normal_chat']:", "if intent not in ['manage_department_task', 'create_todo', 'normal_chat']:")
text = text.replace("if intent == 'create_meeting':", "if intent == 'deleted_meeting':") # Just map it to something that won't happen

# rewrite intent_service
with open('server/services/intent_service.py', 'w') as f:
    f.write(text)

