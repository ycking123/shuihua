import re

with open("/home/git/shuihua/llamaindex/rag_manager.py", "r") as f:
    content = f.read()

def inject_cache_method(match):
    return match.group(0) + """

    def _get_index(self, category_id: str, storage_dir: str):
        if not hasattr(self, '_index_cache'):
            self._index_cache = {}
            
        if category_id not in self._index_cache:
            storage_context = StorageContext.from_defaults(persist_dir=storage_dir)
            self._index_cache[category_id] = load_index_from_storage(storage_context)
            print(f"📦 [{category_id}] Index cached in memory.")
        return self._index_cache[category_id]
"""

content = re.sub(r'def _init_models\(self\):.*?(?=\n\s+try:)', inject_cache_method, content, flags=re.DOTALL)

content = content.replace("storage_context = StorageContext.from_defaults(persist_dir=storage_dir)\n                    index = load_index_from_storage(storage_context)",
                          "index = self._get_index(category_id, storage_dir)")

content = content.replace("storage_context = StorageContext.from_defaults(persist_dir=storage_dir)\n            index = load_index_from_storage(storage_context)",
                          "index = self._get_index(category_id, storage_dir)")

with open("/home/git/shuihua/llamaindex/rag_manager.py", "w") as f:
    f.write(content)
