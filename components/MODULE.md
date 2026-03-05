# `/components` 模块文档

## 模块职责
React UI 组件层，负责用户交互和数据展示。

## 成员清单

### 视图组件
| 文件 | 组件名 | 职责 |
|-----|--------|------|
| `Dashboard.tsx` | `Dashboard` | 主仪表盘，数据可视化总览 |
| `ChatView.tsx` | `ChatView` | 聊天对话界面 |
| `TodoView.tsx` | `TodoView` | 待办事项管理界面 |
| `PersonalView.tsx` | `PersonalView` | 个人中心页面 |
| `LoginView.tsx` | `LoginView` | 登录页面 |

### 交互组件
| 文件 | 组件名 | 职责 |
|-----|--------|------|
| `MobileNav.tsx` | `MobileNav` | 移动端导航栏 |
| `ShareSheet.tsx` | `ShareSheet` | 分享面板 |
| `OntologySphere.tsx` | `OntologySphere` | 本体球可视化 |
| `ArchitectureCanvas.tsx` | `ArchitectureCanvas` | 架构图绘制 |

## 接口说明

### 对外暴露的 Props 接口
各组件主要接收的 Props 类型定义（详见对应文件）

### 依赖的外部类型
```typescript
import { ViewType } from '../types';
import { TODOS_DATA } from '../constants';
```

---

**最后更新**: 2026-02-25
