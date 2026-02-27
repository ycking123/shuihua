# Agent Skill Creator v2.1

**Meta-skill for autonomous agent and skill creation**

## 概述

这是一个强大的元技能，教会 Claude Code 如何自主创建完整的 Agent 和 Skills。

## 功能特性

- ✅ **自主创建 Agent** - 自动研究 API、定义分析、实现代码
- ✅ **多 Agent 支持** - 创建 Agent 套件（多个协作的 Agent）
- ✅ **模板系统** - 使用预配置模板快速创建
- ✅ **转录处理** - 从视频/音频转录中提取工作流并创建 Agent
- ✅ **交互式配置** - 向导式创建流程

## 使用方法

### 创建单个 Agent

```
"Create an agent for processing daily invoice PDFs"
```

### 创建 Agent 套件

```
"Create a financial analysis suite with 4 agents:
fundamental analysis, technical analysis,
portfolio management, and risk assessment"
```

### 使用模板

```
"Create an agent using the financial-analysis template"
```

### 处理转录

```
"I have a YouTube transcript about e-commerce analytics,
can you create agents based on the workflows described?"
```

## 工作流程

当激活时，此技能会引导 Claude 通过 **5 个自主阶段**：

```
PHASE 1: DISCOVERY    - 研究可用 API
PHASE 2: DESIGN       - 定义有用的分析
PHASE 3: ARCHITECTURE - 构建文件夹和文件
PHASE 4: DETECTION    - 确定关键词
PHASE 5: IMPLEMENTATION - 实现功能代码
```

## 命名约定

所有创建的技能都使用 "-cskill" 后缀：

- `pdf-text-extractor-cskill/`
- `financial-analysis-suite-cskill/`
- `stock-analyzer-cskill/`

## 输出

完整的、可安装的 Claude Skill，包括：
- marketplace.json（强制）
- SKILL.md（5000+ 字）
- 功能性 Python 脚本
- 参考文档
- README

## 参考

- [SKILL.md](../skills/agent-skill-creator.skill) - 完整技能文档
- [references/](./references/) - 详细指南和最佳实践
- [templates/](./templates/) - 可用模板
