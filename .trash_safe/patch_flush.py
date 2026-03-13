import re

with open('server/routers/chat.py', 'r') as f:
    text = f.read()

text = text.replace('print(f"⏱️ [1. Auth & Session Init] Cost: {t1_dialog_start - t0_start:.3f}s")', 'print(f"⏱️ [1. Auth & Session Init] Cost: {t1_dialog_start - t0_start:.3f}s", flush=True)')
text = text.replace('print(f"⏱️ [2. Dialogue & Pre-flight] Cost: {t2_rag_start - t1_dialog_start:.3f}s")', 'print(f"⏱️ [2. Dialogue & Pre-flight] Cost: {t2_rag_start - t1_dialog_start:.3f}s", flush=True)')
text = text.replace('print(f"⏱️ [3. RAG Retrieval] Cost: {t3_rag_end - t2_rag_start:.3f}s")', 'print(f"⏱️ [3. RAG Retrieval] Cost: {t3_rag_end - t2_rag_start:.3f}s", flush=True)')
text = text.replace('print(f"⏱️ [4. Prompt Prep & Context] Cost: {t4_llm_start - locals().get(\'t3_rag_end\', t4_llm_start):.3f}s")', 'print(f"⏱️ [4. Prompt Prep & Context] Cost: {t4_llm_start - locals().get(\'t3_rag_end\', t4_llm_start):.3f}s", flush=True)')
text = text.replace('print(f"⏱️ [5. First Token Delay (TTFT)] Cost: {t5_first_token - t4_llm_start:.3f}s")', 'print(f"⏱️ [5. First Token Delay (TTFT)] Cost: {t5_first_token - t4_llm_start:.3f}s", flush=True)')
text = text.replace('print(f"⏱️ [TOTAL. User Ask -> First Token] Cost: {t5_first_token - t0_start:.3f}s")', 'print(f"⏱️ [TOTAL. User Ask -> First Token] Cost: {t5_first_token - t0_start:.3f}s", flush=True)')

with open('server/routers/chat.py', 'w') as f:
    f.write(text)

