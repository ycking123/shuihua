import re

with open('server/routers/chat.py', 'r') as f:
    text = f.read()

tgt = """- 基于知识库内容回答，确保准确。
- 转换成通俗易懂的“人话”进行讲解，而不是生硬地复述。"""

repl = """- 基于知识库内容回答，确保准确。
- 转换成通俗易懂的“人话”进行讲解。
- 必须全面、详尽地涵盖原文中的细节和条件，不得擅自遗漏关键条款。"""

if tgt in text:
    text = text.replace(tgt, repl)

with open('server/routers/chat.py', 'w') as f:
    f.write(text)

