
import React from 'react';
import { LayoutDashboard, MessageSquare, CheckSquare, Bell, User } from 'lucide-react';
import { TodoItem, ViewType } from './types';

// 扩展 TodoItem 类型 definition 以支持会议
export interface ExtendedTodoItem extends TodoItem {
  location?: string;
  attendees?: string[];
  duration?: string;
}

export const MENU_ITEMS = [
  { id: ViewType.DASHBOARD, icon: LayoutDashboard, label: '驾驶舱' },
  { id: ViewType.CHAT, icon: MessageSquare, label: 'AI智僚' },
  { id: ViewType.TODO, icon: CheckSquare, label: '待办事项' },
  { id: ViewType.SETTINGS, icon: User, label: '个人' },
];

export const TODOS_DATA: (ExtendedTodoItem | any)[] = [
  {
    id: 102,
    type: 'approval',
    priority: 'urgent',
    title: '年度预算审批：集团 AI 数字化实验室二期投入',
    sender: '财务中心',
    time: '09:15',
    status: 'pending',
    aiSummary: '资金链压力测试：通过。预计年化收益率提升 12.5%，建议结合 Q3 现金流余量分批核准。',
    aiAction: '生成相关所需材料',
    content: '关于 AI 实验室二期算力集群采购及人才激励专项预算，总计 1.2 亿元，申请从年度战略储备金中拨付。由于近期美联储加息预期及汇率波动，财务中心建议采用分阶段付款方式以降低汇兑损益风险。'
  },
  {
    id: 201,
    type: 'meeting',
    priority: 'high',
    title: 'Q3 战略执行复盘会',
    sender: '总裁办',
    time: '14:00',
    duration: '90min',
    location: '18楼指挥舱 / 远程接入',
    status: 'pending',
    aiSummary: '核心议题：华东区订单流失 analysis。水华精灵已为您准备好竞品对比简报。',
    aiAction: '生成相关所需材料',
    content: '本次会议重点讨论华东区域市场占有率波动及应对方案。'
  },
  {
    id: 101,
    type: 'email',
    priority: 'high',
    title: '关于 2024 集团组织架构敏捷化调整的预案通知',
    sender: '人力资源中心 - 严总',
    time: '10:30',
    status: 'pending',
    aiSummary: '战略契合度：92%。涉及帝王事业集群与 AI 事业部深度融合，旨在提升交付效率。',
    aiAction: '生成相关所需材料',
    content: '朱董您好，针对 Q3 战略复盘中暴露的协同效率问题，人力资源中心拟定了《集团组织架构敏捷化调整方案（初稿）》。主要涉及将帝王事业集群的研发职能与 AI 事业集群进行矩阵化整合，以加速智慧家居产品的迭代速度。请审阅该方案的初步架构图及核心人事变动建议。'
  },
  {
    id: 202,
    type: 'meeting',
    priority: 'normal',
    title: '核心经销商 AI 数字化赋能专题研讨',
    sender: '营销管理中心',
    time: '16:30',
    duration: '45min',
    location: '线上会议',
    status: 'pending',
    aiSummary: '测算显示：数字化铺货工具可降低经销商库存周转周期 12 天。建议审阅首批 50 家试点名单。',
    aiAction: '生成相关所需材料',
    content: '探讨如何利用水华精灵的库存预测能力，为全国核心经销商提供精准的补货建议与营销策略支持，旨在通过 AI 算法解决终端动销慢、库存积压的长期痛点，提升渠道整体抗风险能力。'
  },
  {
    id: 103,
    type: 'task',
    priority: 'normal',
    title: '准备周五经营分析会材料',
    sender: '系统任务',
    time: '18:00',
    status: 'pending',
    aiSummary: '已自动抓取本周 SAP 销售数据及 CRM 客诉记录。',
    aiAction: '生成相关所需材料',
    content: '请更新各区域销售达成率及 Top 5 问题分析。'
  }
];

export const DIBMM_DATA = [
  { subject: '协同决策', current: 85, target: 100 },
  { subject: '系统自主性', current: 70, target: 100 },
  { subject: '交互界面', current: 90, target: 100 },
  { subject: '流程融合', current: 65, target: 100 },
  { subject: '绩效提升', current: 80, target: 100 },
  { subject: '技术环境', current: 75, target: 100 },
];

export const CASH_FLOW_DATA = [
  { time: '9:00', profit: 4200, cash: 3800 },
  { time: '10:00', profit: 4800, cash: 4300 },
  { time: '11:00', profit: 4500, cash: 4100 },
  { time: '12:00', profit: 5100, cash: 4800 },
  { time: '13:00', profit: 4900, cash: 4700 },
  { time: '14:00', profit: 5300, cash: 5100 },
  { time: '15:00', profit: 5600, cash: 5400 },
];
