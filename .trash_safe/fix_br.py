import re

with open('server/routers/chat.py', 'r') as f:
    text = f.read()

# Replace <br> tag instructions in system prompt
tgt = """- 如果原文跨多段或结构明确，善随内容分段，合理使用 <br> 换行和**加粗**"""
repl = """- 不要使用任何HTML标签（特别是<br>，禁止使用），分段直接使用 '\\n\\n' 连续回车。重点信息要采用全角的 **加粗**"""
if tgt in text:
    text = text.replace(tgt, repl)

with open('server/routers/chat.py', 'w') as f:
    f.write(text)

with open('components/ChatView.tsx', 'r') as f:
    text_cv = f.read()

tgt_cv = """ol: ({node, ...props}) => <ol className="list-decimal list-inside mb-2" {...props} />,"""
repl_cv = """ol: ({node, ...props}) => <ol className="list-decimal list-inside mb-2" {...props} />,
            br: () => <br />,"""
if tgt_cv in text_cv:
    text_cv = text_cv.replace(tgt_cv, repl_cv)

with open('components/ChatView.tsx', 'w') as f:
    f.write(text_cv)
