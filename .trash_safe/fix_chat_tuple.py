with open("server/routers/chat.py", "r") as f:
    text = f.read()

tgt = """                rag_context = await asyncio.to_thread(rag_manager.retrieve_all_documents, last_user_message, 3, allowed_categories)
                if isinstance(rag_context, tuple):
                    citations = rag_context[1]
                    rag_context = rag_context[0]"""

repl = """                rag_context_raw = await asyncio.to_thread(rag_manager.retrieve_all_documents, last_user_message, 3, allowed_categories)
                if isinstance(rag_context_raw, list):
                    all_citations = []
                    for ctx_tuple in rag_context_raw:
                        if isinstance(ctx_tuple, tuple):
                            all_citations.extend(ctx_tuple[1])
                    rag_context = "\\n\\n".join([c[0] for c in rag_context_raw if isinstance(c, tuple)])
                    
                    unique_citations = {}
                    for c in all_citations:
                        if c['file'] not in unique_citations or c['score'] > unique_citations[c['file']]['score']:
                            unique_citations[c['file']] = c
                    citations = sorted(unique_citations.values(), key=lambda x: x['score'], reverse=True)
                elif isinstance(rag_context_raw, str):
                    rag_context = rag_context_raw"""

if tgt in text:
    text = text.replace(tgt, repl)
else:
    print("WARNING chat.py tgt not found")
    
with open("server/routers/chat.py", "w") as f:
    f.write(text)

