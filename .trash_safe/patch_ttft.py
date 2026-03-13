import re

with open('server/routers/chat.py', 'r') as f:
    text = f.read()

tgt = '''                if isinstance(item, Exception):
                    raise item
                
                full_response += item'''

repl = '''                if isinstance(item, Exception):
                    raise item
                
                if full_response == "":
                    t5_first_token = time.time()
                    print(f"⏱️ [5. First Token Delay (TTFT)] Cost: {t5_first_token - t4_llm_start:.3f}s")
                    print(f"⏱️ [TOTAL. User Ask -> First Token] Cost: {t5_first_token - t0_start:.3f}s")
                    
                full_response += item'''

if tgt in text:
    text = text.replace(tgt, repl)
else:
    print("Target not found")

with open('server/routers/chat.py', 'w') as f:
    f.write(text)
