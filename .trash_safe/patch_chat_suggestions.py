import re

with open('server/routers/chat.py', 'r') as f:
    text = f.read()

# Replace the end of generate()
old_end = '''                yield f"data: {json.dumps({'content': item})}\\n\\n"
            
            save_message(session_id, "assistant", full_response)
            yield "data: [DONE]\\n\\n"'''

new_end = '''                yield f"data: {json.dumps({'content': item})}\\n\\n"
            
            save_message(session_id, "assistant", full_response)
            
            # --- Generate Suggestions ---
            try:
                sug_prompt = f"基于用户的原问题和你的回答，提供3个推荐的追问（每行1个，不要序号，简短）。\\n问题:{last_user_message}\\n回答:{full_response[:300]}"
                sug_model = "glm-4-flash" if "glm" in request.model.lower() else request.model
                # Run generator inside thread
                def _get_sug():
                    s_gen = provider.chat_stream(
                        model=sug_model,
                        messages=[{"role": "user", "content": sug_prompt}],
                        system_instruction="你负责猜用户会问什么，只直接输出3个问题文本，不要序号与标点前缀，一行一个"
                    )
                    return "".join(s_gen)
                
                sug_text = await asyncio.to_thread(_get_sug)
                suggestions = [s.strip('- *0123456789.') for s in sug_text.split('\\n') if s.strip()][:3]
                if suggestions:
                    yield f"data: {json.dumps({'suggestions': suggestions})}\\n\\n"
            except Exception as e:
                print("Failed catching suggestions:", e)
                
            yield "data: [DONE]\\n\\n"'''

text = text.replace(old_end, new_end)

with open('server/routers/chat.py', 'w') as f:
    f.write(text)

