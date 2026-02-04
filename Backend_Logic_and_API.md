# 水花 (Shuihua) 后端逻辑与接口文档

## 1. 项目概览
本项目是一个基于 **FastAPI** 的智能企业微信助理后端，采用 **双服务架构**（主业务服务 + 微信消息处理服务），集成了 **MySQL 持久化存储**、**智谱 AI (GLM-4V)** 多模态大模型和 **RAG (检索增强生成)** 技术。它能够处理企业微信消息，自动提取待办事项并同步到主数据库，同时为前端提供标准的 RESTful API。

## 2. 系统架构

### 2.1 双服务架构
项目包含两个核心服务进程：
1.  **Main API Server (Port 8000)**: 
    *   **职责**: 核心业务后端，负责用户认证、待办管理 (MySQL)、AI 对话 (Chat)、ASR 语音转写。
    *   **入口**: `server/main.py`
    *   **数据库**: MySQL (`shuihua` database)
2.  **WeChat Worker Server (Port 8080)**: 
    *   **职责**: 专门处理企业微信回调，运行 Playwright 爬虫，进行图片/文本分析。
    *   **入口**: `backend/server_receive.py`
    *   **数据流**: 接收消息 -> AI 分析 -> 提取数据 -> **同步到 Main API**。

### 2.2 技术栈
- **Web 框架**: FastAPI (Python)
- **数据库**: MySQL 8.0 + SQLAlchemy ORM
- **AI 模型**: ZhipuAI (GLM-4, GLM-4V)
- **企业微信 SDK**: wechatpy
- **浏览器自动化**: Playwright (用于会议纪要爬取)
- **认证**: JWT (JSON Web Token)

### 2.3 核心模块与文件结构
| 模块 | 文件路径 | 职责描述 |
| :--- | :--- | :--- |
| **入口** | `server/main.py` | 主服务入口，挂载所有路由，管理数据库生命周期。 |
| **认证** | `server/routers/auth.py` | 用户注册、登录、JWT 签发与验证。 |
| **待办** | `server/routers/todos.py` | 待办事项 CRUD，连接 MySQL `shjl_todos` 表。 |
| **对话** | `server/routers/chat.py` | AI 智能对话，支持 RAG 知识库检索。 |
| **微信** | `backend/server_receive.py` | 微信消息接收器，包含图片分析和会议日程创建逻辑。 |
| **AI处理** | `backend/ai_handler.py` | 封装 GLM-4V 调用，处理图像理解、文本意图识别。 |
| **模型** | `server/models.py` | SQLAlchemy 数据库模型定义 (User, Todo, ChatSession 等)。 |

---

## 3. 核心业务流程

### 3.1 用户认证流程
1.  **注册**: 用户提交用户名/密码 -> 密码哈希存储 -> 返回 UserID。
2.  **登录**: 用户提交凭证 -> 验证哈希 -> 签发 JWT Access Token。
3.  **鉴权**: API 请求头携带 `Authorization: Bearer <token>` -> 中间件解析 Token 获取 `user_id`。

### 3.2 微信消息转待办流程
当用户在企业微信发送消息（文本/图片）时：
1.  **接收**: `WeChat Worker` 收到 XML 回调。
2.  **分析**:
    *   **图片**: 下载图片 -> 转 Base64 -> 调用 GLM-4V -> 提取待办字段 (标题, DDL, 优先级)。
    *   **文本**: 调用 GLM-4 意图识别 -> 提取待办或会议信息。
3.  **同步**: `WeChat Worker` 将提取的数据封装为 JSON，通过 HTTP POST 调用 `Main API` 的 `/api/todos` 接口。
4.  **存储**: `Main API` 接收请求 -> 写入 MySQL 数据库。

### 3.3 智能对话 (Chat) 流程
1.  **请求**: 用户发送消息 -> `Main API` (`/api/chat`).
2.  **RAG (可选)**: 检索相关历史记录或文档上下文。
3.  **生成**: 调用 GLM-4 模型生成回复。
4.  **记录**: 保存对话历史到 MySQL `shjl_chat_messages` 表。

---

## 4. API 接口文档 (Main API - Port 8000)

### 4.1 认证模块 (Auth)

#### 注册用户
- **URL**: `/api/auth/register`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "username": "string",
    "password": "string",
    "email": "string",
    "full_name": "string"
  }
  ```
- **Response**: JWT Token & User Info

#### 用户登录
- **URL**: `/api/auth/login`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "eyJhbG...",
    "token_type": "bearer",
    "user_id": "uuid...",
    "username": "admin"
  }
  ```

### 4.2 待办事项模块 (Todos)

#### 获取待办列表
- **URL**: `/api/todos`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Query Params**:
  - `skip`: int (default 0)
  - `limit`: int (default 100)
- **Response**: List of Todos

#### 创建待办
- **URL**: `/api/todos`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>` (可选，若无 Token 则归属默认用户)
- **Body**:
  ```json
  {
    "title": "完成API文档",
    "content": "详细描述...",
    "type": "task",
    "priority": "high",
    "status": "pending",
    "due_at": "2023-12-31T23:59:59"
  }
  ```

#### 更新待办状态
- **URL**: `/api/todos/{todo_id}`
- **Method**: `PUT`
- **Body**: (Partial update supported)
  ```json
  {
    "status": "completed"
  }
  ```

#### 删除待办
- **URL**: `/api/todos/{todo_id}`
- **Method**: `DELETE`

### 4.3 对话模块 (Chat)

#### 发起对话
- **URL**: `/api/chat/chat`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "message": "帮我总结一下今天的待办",
    "session_id": "optional-uuid"
  }
  ```

### 4.4 语音识别 (ASR)

#### 上传音频转文字
- **URL**: `/api/asr/upload`
- **Method**: `POST`
- **Form Data**: `file: (binary)`

---

## 5. 微信服务接口 (WeChat Worker - Port 8080)

### 企业微信回调
- **URL**: `/wecom/callback`
- **Method**: `GET` (Verify) / `POST` (Receive)
- **Description**: 接收企业微信加密消息，处理后分发后台任务。

### 健康检查
- **URL**: `/health`
- **Method**: `GET`
- **Response**: `{"status": "ok"}`
