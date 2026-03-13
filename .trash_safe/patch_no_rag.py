import re

with open('server/routers/chat.py', 'r') as f:
    text = f.read()

target = '''                for char in no_result_msg:
                    yield f"data: {json.dumps({'content': char})}\\n\\n"
                    await asyncio.sleep(0.005)
                yield "data: [DONE]\\n\\n"'''

ui = '''                for char in no_result_msg:
                    yield f"data: {json.dumps({'content': char})}\\n\\n"
                    await asyncio.sleep(0.005)
                
                try:
                    sug_prompt = f"用户提问：{last_user_message}\\n系统未在企业知识库找到答案。请生成3个推荐的引导性追问（例如：询问其他方面、调整问题表述等），一行一个。"
                    sug_model = "glm-4-flash" if "glm" in request.model.lower() else request.model
                    def _get_sug():
                        s_gen = provider.chat_stream(model=sug_model, messages=[{"role": "user", "content": sug_prompt}], system_instruction="只直接输出3个问题文本，一行一个")
                        return "".join(s_gen)
                    sug_text = await asyncio.to_thread(_get_sug)
                    suggestions = [s.strip('- *0123456789.') for s in sug_text.split('\\n') if s.strip()][:3]
                    if suggestions:
                        yield f"data: {json.dumps({'suggestions': suggestions})}\\n\\n"
                except Exception:
                    pass
                    
                yield "data: [DONE]\\n\\n"'''

if target in text:
    text = text.replace(target, ui)
else:
    print('Target not found')

with open('server/routers/chat.py', 'w') as f:
    f.write(text)

