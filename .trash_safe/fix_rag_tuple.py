with open("llamaindex/rag_manager.py", "r") as f:
    content = f.read()

tgt = 'return "\\n\\n".join(all_context)'
repl = 'return all_context # returning raw tuples up for the chat.py to parse'
if tgt in content:
    content = content.replace(tgt, repl)
else:
    print("WARNING tgt not found")

with open("llamaindex/rag_manager.py", "w") as f:
    f.write(content)

