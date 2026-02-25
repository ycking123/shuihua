# 水花项目 - 全局地图

> **导航提示**: AI 从任意文件进入，三次 Read 即可获得完整上下文：
> 1. 读取当前文件头（依赖声明 + 职责说明）
> 2. 读取所在模块的 `MODULE.md`（成员清单 + 接口说明）
> 3. 读取根目录的 `MAP.md`（本文档）

## 项目定位
**水花** - 企业会议智能助手平台
- 核心功能：会议爬取、AI 分析、待办管理、数据可视化
- 技术栈：React + TypeScript + FastAPI + Python + MySQL

## 模块结构

### 📱 `/components` - 前端组件层
**职责**: React UI 组件，负责用户交互和数据展示
**成员清单**: 见 `components/MODULE.md`
**依赖**: 无（被 `App.tsx` 依赖）

### 🐍 `/backend` - 后端服务层
**职责**: 会议爬虫、AI 处理、业务逻辑
**成员清单**: 见 `backend/MODULE.md`
**依赖**: 无（被 `server/` 依赖）

### 🌐 `/server` - API 路由层
**职责**: FastAPI 接口定义、数据库连接、请求路由
**成员清单**: 见 `server/MODULE.md`
**依赖**: `backend/` 模块

### 🕷️ `/crawlers` - 爬虫模块
**职责**: 第三方平台会议数据爬取（腾讯会议等）
**成员清单**: 见 `crawlers/MODULE.md`
**依赖**: 待定

### 🔧 `/utils` - 工具函数库
**职责**: 通用工具函数、辅助方法
**成员清单**: 见 `utils/MODULE.md`
**依赖**: 无

## 数据流向
```
会议分享链接
    ↓
[crawlers] 爬取原始数据
    ↓
[backend] AI 分析提取
    ↓
[server] 数据库存储
    ↓
[components] 前端展示
```

## 强制同构规则
**每次代码变更后必须检查**：
1. ✅ 文件头部的依赖声明是否最新
2. ✅ 文件头部的职责说明是否准确
3. ✅ 模块 `MODULE.md` 的成员清单是否完整
4. ✅ 模块 `MODULE.md` 的接口说明是否同步

**检查命令**：
```bash
# TODO: 添加自动化检查脚本
python scripts/check_docs_sync.py
```

## 快速定位

| 功能模块 | 文件路径 | 核心接口/组件 |
|---------|---------|-------------|
| 会议爬取 | `backend/url_crawler.py` | `crawl_meeting_url()` |
| AI 分析 | `backend/ai_handler.py` | `extract_todos_from_text()` |
| 待办 API | `server/routers/todos.py` | `GET/POST /api/todos` |
| 待办 UI | `components/TodoView.tsx` | `TodoView` |
| 数据库 | `server/database.py` | `engine, Base` |
| 主入口 | `server/main.py` | `app = FastAPI()` |

---

**最后更新**: 2026-02-25
**维护者**: Claude Code
