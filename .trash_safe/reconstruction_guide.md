以下是完整的操作指南。修改后即可退回到传统的全文 Chunk（以固定字数为单位，不再额外处理句级语境窗口）方式做特征检索：

### 第一步：修改代码逻辑
1. 打开 `llamaindex/rag_manager.py`。
2. 找到 `def build_index()` 方法内的这行代码（大约 283 行附近）：
   ```python
   nodes = self.sentence_window_parser.get_nodes_from_documents(documents)
   ```
3. 将上方那一句代码替换成如下形式，让它改走 `Settings` 里定义好的后备文本分割器（默认是 512 Token 一个大分块）：
   ```python
   from llama_index.core import Settings
   nodes = Settings.text_splitter.get_nodes_from_documents(documents)
   ```

*(注：系统中的 `_expand_sentence_window` 函数底层调用的 PostProcessor 含有后向兼容设计，如果它找不到节点上的窗口元数据，会自动原样返回您的 Chunk，因此不用非得去修改取回代码)*

### 第二步：清理脏数据并重建库
因为我们改变了切割文本的基础单位维度，之前已经保存在本地 `storage_multi` 里的向量维度全部作废了。必须强行清空后重新建立：
1. 停掉现有的服务（跑 `./stop_server.sh`）
2. 把旧的历史检索数据库整个删掉：
   ```bash
   rm -rf llamaindex/storage_multi/*
   ```
3. 进去重新扫描 `data/` 目录的内容执行建库：
   ```bash
   cd llamaindex
   python build_indices.py
   ```
4. 建完之后再启动 `./start_server.sh` 即可。此时 RAG 拿回的就完全是干干脆脆的 512 个字符片段了。
