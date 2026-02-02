-- ==================================================================================
-- 数据库设计方案 - 基于企业级成熟体系 (MySQL 8.0+ 推荐)
-- 项目：Agent (水化 / Water Essence Sprite)
-- 设计原则：
-- 1. 三范式(3NF)为主，适度反范式(JSON)以支持灵活业务
-- 2. 软删除 (is_deleted) 支持数据恢复与审计
-- 3. 审计字段 (created_at, updated_at, created_by) 全覆盖
-- 4. 索引优化 (针对常用查询字段)
-- 注意：本脚本适用于 MySQL 8.0+，因使用了 JSON 类型和 Generated Columns 特性
-- ==================================================================================

-- ----------------------------------------------------------------------------------
-- 1. 用户与权限模块 (RBAC)
-- ----------------------------------------------------------------------------------

CREATE TABLE shjl_roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE, -- e.g., 'admin', 'user', 'manager'
    description VARCHAR(255),
    permissions JSON, -- 存储具体权限点的JSON，如 {"can_delete_todo": true}
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE shjl_users (
    id CHAR(36) PRIMARY KEY, -- 建议应用层生成 UUID，或使用 (UUID()) 作为默认值(MySQL 8.0.13+)
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL, -- 存储加密后的密码
    wecom_userid VARCHAR(100) UNIQUE, -- 企业微信 UserID，用于关联企业微信账号
    full_name VARCHAR(50),
    avatar_url TEXT,
    role_id INT,
    is_active BOOLEAN DEFAULT TRUE,
    last_login_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (role_id) REFERENCES shjl_roles(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_users_wecom_userid ON shjl_users(wecom_userid);
CREATE INDEX idx_users_email ON shjl_users(email);

-- ----------------------------------------------------------------------------------
-- 2. 待办事项核心模块 (Todos)
-- 对应 server/routers/todos.py 和 frontend/types.ts 中的 TodoItem
-- ----------------------------------------------------------------------------------

CREATE TABLE shjl_todos (
    id CHAR(36) PRIMARY KEY, -- 建议应用层生成 UUID
    user_id CHAR(36) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content LONGTEXT, -- 对应 content 字段，存储详细内容，使用 LONGTEXT 防溢出
    type ENUM('task', 'email', 'approval', 'meeting', 'chat_record') DEFAULT 'task',
    priority ENUM('urgent', 'high', 'normal', 'low') DEFAULT 'normal',
    status ENUM('pending', 'in_progress', 'completed', 'archived') DEFAULT 'pending',
    
    -- 来源信息
    sender VARCHAR(100), -- 发送者/来源，如 "AI智僚", "会议纪要"
    source_origin VARCHAR(50), -- 来源系统，如 "wechat", "web", "system"
    source_message_id VARCHAR(100), -- 关联的原始消息ID (如微信MessageID)
    
    -- AI 增强字段
    ai_summary TEXT, -- AI生成的摘要
    ai_action TEXT, -- AI建议的行动点
    is_user_task BOOLEAN DEFAULT FALSE, -- 是否为用户任务
    text_type INT DEFAULT 0, -- 0: Image/Default, 1: Text Message
    
    -- 时间管理
    due_at DATETIME, -- 截止时间
    completed_at DATETIME, -- 完成时间
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES shjl_users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_todos_user_status ON shjl_todos(user_id, status);
CREATE INDEX idx_todos_created_at ON shjl_todos(created_at DESC);

-- ----------------------------------------------------------------------------------
-- 3. 智能对话与分析报告模块 (Chat & Analysis)
-- ----------------------------------------------------------------------------------

CREATE TABLE shjl_chat_sessions (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    title VARCHAR(100), -- 会话标题，可由AI自动生成
    summary TEXT, -- 会话总结
    is_pinned BOOLEAN DEFAULT FALSE, -- 是否置顶
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES shjl_users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE shjl_chat_messages (
    id CHAR(36) PRIMARY KEY,
    session_id CHAR(36) NOT NULL,
    role VARCHAR(20) NOT NULL, -- 'user', 'assistant', 'system', 'function'
    content LONGTEXT NOT NULL,
    message_type VARCHAR(20) DEFAULT 'text', -- 'text', 'image', 'file'
    
    -- 元数据，存储 Token 消耗、引用来源、意图识别结果等
    meta_data JSON, 
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES shjl_chat_sessions(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_messages_session_created ON shjl_chat_messages(session_id, created_at);

-- 新增：AI 分析报告表 (对应 VisualData/ConclusionCard/MindMap)
-- 用于存储复杂的结构化分析结果，支持前端 Dashboard 展示
CREATE TABLE shjl_analysis_reports (
    id CHAR(36) PRIMARY KEY,
    source_type VARCHAR(20), -- 'chat_message', 'todo', 'meeting'
    source_id CHAR(36) NOT NULL, -- 关联的来源ID
    
    title VARCHAR(255), -- 报告标题
    detailed_report LONGTEXT, -- 详细文本报告
    
    -- 核心指标卡片 (存储 ConclusionCard 数组)
    -- 结构: [{"label": "营收", "value": "100万", "trend": "+10%", "isGood": true}]
    conclusion_cards JSON,
    
    -- 思维导图/知识图谱数据 (存储 MindMapNode 数组)
    -- 结构: [{"label": "核心", "subNodes": ["子节点1", "子节点2"]}]
    mind_map_data JSON,
    
    raw_response JSON, -- 原始 AI 响应备份
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_analysis_source (source_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------------
-- 4. 会议与日程模块 (Meetings)
-- 对应 backend/server_receive.py 中的会议逻辑
-- ----------------------------------------------------------------------------------

CREATE TABLE shjl_meetings (
    id CHAR(36) PRIMARY KEY,
    organizer_id CHAR(36),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    location VARCHAR(255),
    
    wecom_schedule_id VARCHAR(100), -- 关联企业微信日程ID
    
    -- AI 会议纪要相关
    summary TEXT, -- 会议纪要摘要
    transcript LONGTEXT, -- 会议转录全文
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (organizer_id) REFERENCES shjl_users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE shjl_meeting_attendees (
    meeting_id CHAR(36),
    user_id CHAR(36), -- 内部用户
    external_email VARCHAR(100), -- 外部用户邮箱
    external_name VARCHAR(100), -- 外部用户姓名
    status VARCHAR(20) DEFAULT 'pending', -- 'accepted', 'declined', 'tentative'
    PRIMARY KEY (meeting_id, user_id),
    FOREIGN KEY (meeting_id) REFERENCES shjl_meetings(id),
    FOREIGN KEY (user_id) REFERENCES shjl_users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------------
-- 5. 知识图谱与本体库 (Ontology & Graph)
-- 对应 components/OntologySphere.tsx
-- ----------------------------------------------------------------------------------

CREATE TABLE shjl_ontology_nodes (
    id CHAR(36) PRIMARY KEY,
    label VARCHAR(100) NOT NULL,
    type VARCHAR(50), -- 节点类型，如 'Project', 'Person', 'Concept'
    properties JSON, -- 存储节点的其他属性，如颜色、大小、描述
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE shjl_ontology_edges (
    id CHAR(36) PRIMARY KEY,
    source_node_id CHAR(36),
    target_node_id CHAR(36),
    relation_type VARCHAR(50), -- 关系类型，如 'OWNS', 'RELATED_TO'
    weight FLOAT DEFAULT 1.0, -- 权重
    properties JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_node_id) REFERENCES shjl_ontology_nodes(id),
    FOREIGN KEY (target_node_id) REFERENCES shjl_ontology_nodes(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_edges_source ON shjl_ontology_edges(source_node_id);
CREATE INDEX idx_edges_target ON shjl_ontology_edges(target_node_id);

-- ----------------------------------------------------------------------------------
-- 6. 知识库与RAG (Knowledge Base)
-- 对应 RAG 功能
-- ----------------------------------------------------------------------------------

CREATE TABLE shjl_knowledge_documents (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content LONGTEXT NOT NULL,
    source_url VARCHAR(500),
    file_type VARCHAR(20), -- 'pdf', 'docx', 'md'
    
    -- 向量存储引用 (如果是使用 vector 插件，可以直接在这里存 vector)
    -- embedding BLOB, 
    
    created_by CHAR(36),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES shjl_users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------------
-- 7. 系统审计日志 (Audit Logs)
-- 企业级必备，用于追踪系统操作
-- ----------------------------------------------------------------------------------

CREATE TABLE shjl_audit_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id CHAR(36),
    action VARCHAR(100) NOT NULL, -- e.g., 'CREATE_TODO', 'DELETE_USER'
    resource_type VARCHAR(50), -- e.g., 'todo', 'user'
    resource_id VARCHAR(100),
    ip_address VARCHAR(45),
    user_agent TEXT,
    details JSON, -- 变更前后的数据快照
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES shjl_users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_audit_user_action ON shjl_audit_logs(user_id, action);

