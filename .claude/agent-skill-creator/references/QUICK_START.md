# Agent Skill Creator - 快速开始指南

## 基本使用

### 1. 创建简单的 Agent

只需描述您想要自动化的工作流：

```
"Every day I download stock market data, analyze trends,
and create reports. This takes 2 hours. Create an agent for this."
```

Claude 将：
- 🤖 研究合适的 API（如 Alpha Vantage, Yahoo Finance）
- 🤖 实现趋势分析逻辑
- 🤖 生成专业报告
- 🤖 自动存储结果
- 🤖 创建完整的可安装 Skill

### 2. 创建 Agent 套件

当您需要多个相关 Agent 时：

```
"Create a complete financial analysis system with 4 agents:
1. Fundamental analysis for company valuation
2. Technical analysis for trading signals
3. Portfolio management and optimization
4. Risk assessment and compliance"
```

### 3. 使用模板加速创建

```
"Create an agent using the financial-analysis template"
```

可用模板：
- 📊 **financial-analysis** - 金融分析
- 🌡️ **climate-analysis** - 气候分析
- 🛒 **e-commerce-analytics** - 电商分析

## 激活关键词

Claude 会自动检测以下关键词并激活此技能：

- "create an agent for"
- "create a skill for"
- "automate workflow"
- "every day I have to"
- "daily I need to"
- "I need to repeat"
- "turn process into agent"

## 输出内容

创建完成后，您将得到：

```
your-agent-name-cskill/
├── .claude-plugin/
│   └── marketplace.json      # 安装配置
├── SKILL.md                   # 完整技能文档（5000+ 字）
├── scripts/
│   └── main.py                # 功能性代码
├── requirements.txt            # Python 依赖
└── README.md                  # 使用说明
```

## 安装创建的 Skill

创建完成后，安装步骤：

```bash
# 复制到项目的 .claude/skills/ 目录
cp -r your-agent-name-cskill/SKILL.md .claude/skills/

# 或者添加到 marketplace.json
```

## 常见用例

### 财务分析
```
"Create an agent that fetches stock data from Yahoo Finance,
calculates RSI and MACD indicators, and sends alerts."
```

### 数据处理
```
"Every week I download CSV files from FTP, clean them,
and upload to database. Automate this."
```

### 报告生成
```
"Create a skill that generates weekly reports from
Google Analytics data and emails them to stakeholders."
```

### 文档处理
```
"I have 100 PDF invoices monthly. Create an agent that
extracts data, validates it, and updates our accounting system."
```

## 高级功能

### 从转录创建

提供视频或音频转录，Claude 会：
1. 识别多个工作流
2. 提取步骤和 API
3. 创建集成 Agent 套件

```
"Here's a 2-hour tutorial transcript on building a business
intelligence system. Create agents for all workflows described."
```

### 交互式创建

对于复杂项目，使用向导模式：

```
"Help me create an agent with preview options"
```

Claude 将：
1. 询问澄清问题
2. 提供实时预览
3. 迭代优化

## 时间节省统计

| 任务类型 | 手动时间 | Agent 时间 | 节省 |
|---------|---------|-----------|------|
| 财务分析 | 2小时/天 | 5分钟/天 | 96% |
| 库存管理 | 1.5小时/天 | 3分钟/天 | 97% |
| 研究数据收集 | 8小时/周 | 20分钟/周 | 95% |
| 报告生成 | 3小时/周 | 10分钟/周 | 94% |

## 下一步

- 查看完整文档：[SKILL.md](../skills/agent-skill-creator.skill)
- 探索可用模板：[templates/](../templates/)
- 了解最佳实践：[ACTIVATION_BEST_PRACTICES.md](ACTIVATION_BEST_PRACTICES.md)
