
export enum ViewType {
  DASHBOARD = 'dashboard',
  CHAT = 'chat',
  MEETING = 'meeting',
  TODO = 'todo',
  ALERTS = 'alerts',
  SETTINGS = 'settings',
  LOGIN = 'login'
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

export type MeetingTabType = 'overview' | 'booking' | 'rooms' | 'minutes';

export interface MeetingTodo {
  id: string;
  title: string;
  content?: string;
  priority: string;
  status: string;
  assignee?: string;
  due_at?: string;
  created_at?: string;
}

export interface MeetingItem {
  id: string;
  title: string;
  description?: string | null;
  start_time: string;
  created_at: string;
  end_time: string;
  status?: string;
  channel?: string;
  source_type?: string;
  location?: string | null;
  meeting_url?: string | null;
  room_name?: string | null;
  room_site_name?: string | null;
  room_id?: string | null;
  participants?: string[];
  sync_status?: string | null;
  wecom_schedule_id?: string | null;
  audio_file_key?: string | null;
  summary?: string | null;
  transcript?: string | null;
  organizer_id?: string | null;
  todos_count?: number;
}

