# `/server` 模块文档

## 模块职责
FastAPI 路由层，负责 API 接口定义、数据库连接、请求分发。

## 成员清单

### 核心文件
| 文件 | 职责 |
|-----|------|
| `main.py` | FastAPI 应用入口，路由注册，CORS 配置 |
| `database.py` | 数据库连接引擎，Session 管理 |
| `models.py` | SQLAlchemy 数据模型定义 |
| `security.py` | 安全认证相关工具 |

### 路由模块 (`routers/`)
| 文件 | 前缀 | 职责 |
|-----|------|------|
| `todos.py` | `/api/todos` | 待办事项 CRUD |
| `meetings.py` | `/api/meetings` | 会议数据管理 |
| `chat.py` | `/api/chat` | 聊天对话接口 |
| `auth.py` | `/api/auth` | 用户认证 |
| `dashboard.py` | `/api/dashboard` | 仪表盘数据 |
| `asr.py` | `/api/asr` | 语音识别 |

### 服务模块 (`services/`)
待补充成员清单

## 接口说明

### 主应用 (`main.py`)
```python
app = FastAPI(lifespan=lifespan)

# 注册的路由:
# - /api/health
# - /api/todos
# - /api/meetings
# - /api/chat
# - /api/auth
# - /api/dashboard
# - /api/asr
```

### 数据库 (`database.py`)
```python
engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession)
```

### 依赖关系
```python
from .routers import asr, chat, todos, auth, dashboard, meetings
from .database import engine, Base, init_db
```

---

**最后更新**: 2026-02-25
