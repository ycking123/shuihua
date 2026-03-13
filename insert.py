lines = open('/home/git/shuihua/llamaindex/rag_manager.py').readlines()
with open('/home/git/shuihua/llamaindex/rag_manager.py', 'w') as f:
    for i, line in enumerate(lines):
        if i == 152:
            f.write('''    def _get_index(self, category_id: str, storage_dir: str):
        if not hasattr(self, '_index_cache'):
            self._index_cache = {}
        if category_id not in self._index_cache:
            storage_context = StorageContext.from_defaults(persist_dir=storage_dir)
            self._index_cache[category_id] = load_index_from_storage(storage_context)
            print(f"📦 [{category_id}] Index cached in memory.")
        return self._index_cache[category_id]

    def _init_models(self):
        """
        配置全局模型设置
        
        LlamaIndex 使用 Settings 全局单例来管理模型配置：
        - Settings.embed_model：所有索引构建和检索时使用的 embedding 模型
        - Settings.llm：所有需要 LLM 的操作（查询改写、LLM Rerank、上下文压缩、答案生成）都隐式使用它
        - Settings.text_splitter：默认文本分割器（作为后备，主要使用 sentence_window_parser）
        
        这意味着整个模块中无需显式传递模型实例，
        所有 LlamaIndex 组件会自动从 Settings 获取模型。
        """
        try:
''')
        f.write(line)
