
export enum ViewType {
  DASHBOARD = 'dashboard',
  CHAT = 'chat',
  TODO = 'todo',
  ALERTS = 'alerts',
  SETTINGS = 'settings'
}

export interface KpiData {
  title: string;
  value: string;
  trend: string;
  trendUp: boolean;
  isNegativeGood?: boolean;
  iconColor: string;
  color: 'blue' | 'emerald' | 'orange' | 'purple';
  subtext: string;
}

export interface TodoItem {
  id: number;
  type: 'email' | 'approval' | 'task';
  priority: 'urgent' | 'high' | 'normal';
  title: string;
  sender: string;
  time: string;
  status: 'pending' | 'completed';
  aiSummary: string;
  aiAction: string;
  content: string;
}

export interface Node {
  id: string;
  label: string;
  type: string;
  x: number;
  y: number;
  color: string;
}

export interface Edge {
  from: string;
  to: string;
}
