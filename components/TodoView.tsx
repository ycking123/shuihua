// ============================================================================
// 文件: TodoView.tsx
// 模块: components
// 职责: 待办事项管理界面，支持会议关联待办和个人待办的展示和编辑
//
// 依赖声明:
//   - 外部: react, react-dom, lucide-react
//   - 本项目: constants (TODOS_DATA), types (ViewType)
//
// 主要组件:
//   - TodoView: 主组件，渲染待办事项列表和详情
//
// ============================================================================

import React, { useState, useMemo, useEffect } from 'react';
import { createPortal } from 'react-dom';
import {
  CheckSquare, Sparkles, ChevronLeft, Search,
  Layers, Inbox, Coffee, ShieldCheck, Trash2,
  Target, ArrowRight, PenLine, User, AlertCircle, Clock, Info,
  MessageSquare, FileText, Calendar, Link as LinkIcon, X, Plus, Check, Edit2
} from 'lucide-react';
import { TODOS_DATA } from '../constants';
import { ViewType } from '../types';

type TodoCategory = 'all' | 'email' | 'meeting' | 'approval' | 'chat_record' | 'meeting_minutes';
type PriorityType = 'urgent' | 'high' | 'normal';

type SortByType = 'created_at' | 'meeting_start_time';

interface TaskItem {
  id: string | number;
  type: string;
  priority: PriorityType;
  title: string;
  sender: string;
  time: string;
  completed?: boolean;
  status?: string;
  aiSummary?: string;
  aiAction?: string;
  content?: string;
  isUserTask?: boolean;
  source_message_id?: string;
  meeting_start_time?: string;
  meeting_created_at?: string;
}

// 会议关联的待办事项
interface MeetingTodo {
  id: string;
  title: string;
  content?: string;
  priority: string;
  status: string;
  assignee?: string;
  due_at?: string;
  created_at?: string;
}

interface MeetingItem {
  id: string;
  title: string;
  start_time: string;
  created_at: string;
  location: string;
  summary: string;
  transcript: string;
  organizer_id?: string;
  todos_count?: number;
}

interface TodoViewProps {
  onNavigate?: (view: ViewType, context?: string) => void;
}

const PriorityTag: React.FC<{ priority: string }> = ({ priority }) => {
  const styles: Record<string, { bg: string, text: string, border: string, label: string }> = {
    urgent: { bg: 'bg-red-500/10', text: 'text-red-600 dark:text-red-500', border: 'border-red-500/20', label: '紧急' },
    high: { bg: 'bg-blue-500/10', text: 'text-blue-600 dark:text-blue-500', border: 'border-blue-400/20', label: '重要' },
    normal: { bg: 'bg-slate-500/10', text: 'text-slate-600 dark:text-slate-400', border: 'border-slate-200 dark:border-white/5', label: '普通' },
  };
  const config = styles[priority] || styles.normal;
  return (
    <div className={`flex items-center gap-1 px-2 py-0.5 rounded border ${config.bg} ${config.border}`}>
      <span className={`text-[9px] font-bold uppercase tracking-widest ${config.text}`}>{config.label}</span>
    </div>
  );
};

const TodoView: React.FC<TodoViewProps> = ({ onNavigate }) => {
  const [selectedItem, setSelectedItem] = useState<any | null>(null);
  const [selectedMeeting, setSelectedMeeting] = useState<MeetingItem | null>(null);
  const [meetingTodos, setMeetingTodos] = useState<MeetingTodo[]>([]); // 会议关联的待办
  const [activeCategory, setActiveCategory] = useState<TodoCategory>('all');
  const [sortBy, setSortBy] = useState<SortByType>('created_at'); // 排序方式
  const [userTasks, setUserTasks] = useState<TaskItem[]>([]);
  const [backendTasks, setBackendTasks] = useState<TaskItem[]>([]);
  const [meetingMinutes, setMeetingMinutes] = useState<MeetingItem[]>([]);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskPriority, setNewTaskPriority] = useState<PriorityType>('high');
  const [isInputFocused, setIsInputFocused] = useState(false);
  
  // 待办编辑状态
  const [editingTodo, setEditingTodo] = useState<MeetingTodo | null>(null);
  const [editForm, setEditForm] = useState({ title: '', content: '', priority: 'normal' });
  const [isAddingTodo, setIsAddingTodo] = useState(false);
  const [newTodoForm, setNewTodoForm] = useState({ title: '', content: '', priority: 'normal' });
  
  // 获取 API 基础 URL
  const getBaseUrl = () => {
    if (import.meta.env.DEV) return '/api';
    return `http://${window.location.hostname}:8000/api`;
  };
  
  // 获取请求头
  const getHeaders = () => {
    const headers: HeadersInit = { 'Content-Type': 'application/json' };
    const token = localStorage.getItem('token');
    if (token) headers['Authorization'] = `Bearer ${token}`;
    return headers;
  };
  
  // 获取会议关联的待办事项
  const fetchMeetingTodos = async (meetingId: string) => {
    try {
      const res = await fetch(`${getBaseUrl()}/meetings/${meetingId}/todos`, { headers: getHeaders() });
      if (res.ok) {
        const data = await res.json();
        setMeetingTodos(data);
      }
    } catch (e) {
      console.error('Failed to fetch meeting todos:', e);
    }
  };
  
  // 打开会议详情时加载待办
  useEffect(() => {
    if (selectedMeeting) {
      fetchMeetingTodos(selectedMeeting.id);
      setIsAddingTodo(false);
      setEditingTodo(null);
    }
  }, [selectedMeeting]);
  
  // 更新待办
  const handleUpdateTodo = async () => {
    if (!editingTodo) return;
    try {
      const res = await fetch(`${getBaseUrl()}/todos/${editingTodo.id}`, {
        method: 'PUT',
        headers: getHeaders(),
        body: JSON.stringify(editForm)
      });
      if (res.ok) {
        fetchMeetingTodos(selectedMeeting!.id);
        setEditingTodo(null);
      } else {
        const errorData = await res.json().catch(() => ({}));
        console.error('Update failed:', errorData);
        alert(`保存失败: ${errorData.detail || '请检查网络或登录状态'}`);
      }
    } catch (e) {
      console.error('Failed to update todo:', e);
      alert('保存失败，请检查网络连接');
    }
  };
  
  // 删除待办
  const handleDeleteTodo = async (todoId: string) => {
    if (!confirm('确定要删除这个待办吗？')) return;
    try {
      const res = await fetch(`${getBaseUrl()}/todos/${todoId}`, {
        method: 'DELETE',
        headers: getHeaders()
      });
      if (res.ok) {
        fetchMeetingTodos(selectedMeeting!.id);
      }
    } catch (e) {
      console.error('Failed to delete todo:', e);
    }
  };
  
  // 新增待办
  const handleAddTodo = async () => {
    if (!newTodoForm.title.trim() || !selectedMeeting) return;
    try {
      const res = await fetch(`${getBaseUrl()}/todos`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({
          ...newTodoForm,
          type: 'meeting',
          status: 'pending',
          sender: '会议助手',
          source_message_id: selectedMeeting.id,
          source_origin: 'meeting_minutes'
        })
      });
      if (res.ok) {
        fetchMeetingTodos(selectedMeeting.id);
        setNewTodoForm({ title: '', content: '', priority: 'normal' });
        setIsAddingTodo(false);
      } else {
        const errorData = await res.json().catch(() => ({}));
        console.error('Add failed:', errorData);
        alert(`保存失败: ${errorData.detail || '请检查网络或登录状态'}`);
      }
    } catch (e) {
      console.error('Failed to add todo:', e);
      alert('保存失败，请检查网络连接');
    }
  };

  // Fetch tasks and meetings from backend on mount
  React.useEffect(() => {
    const fetchData = async () => {
      try {
        // Use hostname to adapt to both local and server environments
        const hostname = window.location.hostname;
        let baseUrl = `http://${hostname}:8000/api`;
        
        // If local development (npm run dev), use proxy
        if (import.meta.env.DEV) {
             baseUrl = '/api';
        }

        // Add Authorization header if token exists
        const token = localStorage.getItem('token');
        const headers: HeadersInit = {
            'Content-Type': 'application/json'
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        // Fetch Todos with sort parameter
        const resTodos = await fetch(`${baseUrl}/todos?sort_by=${sortBy}`, { headers });
        if (resTodos.ok) {
          const data = await resTodos.json();
          setBackendTasks(data);
        }

        // Fetch Meetings with sort parameter
        const resMeetings = await fetch(`${baseUrl}/meetings?sort_by=${sortBy}`, { headers });
        if (resMeetings.ok) {
          const data = await resMeetings.json();
          setMeetingMinutes(data);
        }

      } catch (e: any) {
        console.error("Failed to fetch data:", e);
      }
    };
    fetchData();
    // Poll every 5 seconds for updates
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, [sortBy]); // Add sortBy as dependency

  const categories = [
    { id: 'all', label: '全部待办', icon: Layers },
    { id: 'email', label: '邮件', icon: Inbox },
    { id: 'meeting', label: '会议', icon: Coffee },
    { id: 'approval', label: '审批', icon: ShieldCheck },
    { id: 'chat_record', label: '其他', icon: MessageSquare },
    { id: 'meeting_minutes', label: '会议纪要', icon: FileText },
  ];

  const getCount = (id: string) => {
    if (id === 'meeting_minutes') return meetingMinutes.length;
    const all = [...TODOS_DATA, ...userTasks, ...backendTasks];
    return all.filter(task => {
      // Determine if task is pending
      const isPending = task.status === 'pending' || (task.completed === false);
      // Check if task matches the category
      // userTasks have type 'task' which is not in standard categories, so they only show in 'all'
      const matchesType = id === 'all' || task.type === id;
      return isPending && matchesType;
    }).length;
  };

  const handleAddUserTask = () => {
    if (!newTaskTitle.trim()) return;
    const task: TaskItem = {
      id: `user-${Date.now()}`,
      type: 'task',
      priority: newTaskPriority,
      title: newTaskTitle,
      sender: '朱江 (本人)',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      completed: false,
      isUserTask: true
    };
    setUserTasks([task, ...userTasks]);
    setNewTaskTitle('');
    setNewTaskPriority('high');
    setIsInputFocused(false);
  };

  const toggleUserTask = (id: string | number) => {
    setUserTasks(userTasks.map(t => t.id === id ? { ...t, completed: !t.completed } : t));
  };

  const deleteUserTask = (id: string | number) => {
    setUserTasks(userTasks.filter(t => t.id !== id));
  };

  const allTasks = useMemo(() => {
    const systemTasks = TODOS_DATA.map(t => ({ ...t, isUserTask: false }));
    // Merge user tasks, system tasks, and backend tasks
    return [...userTasks, ...backendTasks, ...systemTasks].sort((a, b) => {
      const priorityWeight = { urgent: 3, high: 2, normal: 1 };
      return priorityWeight[b.priority] - priorityWeight[a.priority];
    });
  }, [userTasks, backendTasks]);

  const filteredTasks = allTasks.filter(task => {
    if (activeCategory === 'all') return true;
    return task.type === activeCategory;
  });

  const handleTaskClick = (item: TaskItem) => {
    if (activeCategory === 'all' && !item.isUserTask) {
      setActiveCategory(item.type as TodoCategory);
    } else if (!item.isUserTask) {
      setSelectedItem(item);
    }
  };

  const handleActionClick = () => {
    if (onNavigate && selectedItem) {
      const pText = selectedItem.priority === 'urgent' ? '紧急立即执行' : (selectedItem.priority === 'high' ? '重要战略关注' : '常规跟进');
      const prompt = `请帮我生成关于“${selectedItem.title}”的相关所需材料和详细建议报告。这份任务是由 ${selectedItem.sender} 发起的，目前的状态是 ${pText}。请给出具体的执行路线图。`;
      onNavigate(ViewType.CHAT, prompt);
      setSelectedItem(null);
    }
  };

  return (
    <div className="relative h-full animate-in fade-in duration-500 flex flex-col bg-slate-50 dark:bg-black transition-colors duration-500">
      {/* 顶部标题与分类导航 */}
      <div className="shrink-0 p-6 flex flex-col border-b border-slate-200 dark:border-white/5 bg-white/40 dark:bg-black/40 backdrop-blur-xl z-20">
        <div className="flex items-center justify-between mb-6">
          <div className="flex flex-col">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-slate-900 dark:text-white">
              <div className="w-1.5 h-6 bg-blue-600 rounded-full glow-blue"></div>
              待办事项
            </h2>
            <span className="text-[9px] font-mono-prec text-slate-400 dark:text-slate-500 uppercase tracking-[0.3em] mt-1">COMMAND DASHBOARD SYSTEM</span>
          </div>
          <button className="p-2.5 glass-card rounded-xl border-slate-200 dark:border-white/10 text-slate-500 dark:text-slate-400 active:scale-90 transition-all shadow-sm">
            <Search size={18} />
          </button>
        </div>

        <div className="flex gap-2 overflow-x-auto no-scrollbar pb-1">
          {categories.map((cat) => {
            const isActive = activeCategory === cat.id;
            const count = getCount(cat.id);
            return (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id as TodoCategory)}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-2xl transition-all duration-300 border relative ${
                  isActive 
                  ? 'bg-blue-600 border-blue-400/50 text-white shadow-lg glow-blue' 
                  : 'bg-white/40 dark:bg-white/5 border-slate-200 dark:border-white/5 text-slate-500 hover:bg-white/60 dark:hover:bg-white/10'
                }`}
              >
                <cat.icon size={14} className={isActive ? 'animate-pulse' : ''} />
                <span className="text-xs font-bold whitespace-nowrap">{cat.label}</span>
                {count > 0 && (
                  <span className={`flex items-center justify-center min-w-[16px] h-4 px-1 rounded-full text-[8px] font-bold ring-1 ring-black/10 dark:ring-black/50 ${
                    isActive ? 'bg-white text-blue-600 shadow-sm' : 'bg-blue-500 text-white'
                  }`}>
                    {count}
                  </span>
                )}
              </button>
            );
          })}
        </div>
                
        {/* 排序切换 */}
        <div className="flex items-center gap-2 mt-3">
          <span className="text-[9px] text-slate-400 dark:text-slate-500 uppercase tracking-wider">排序:</span>
          <div className="flex gap-1">
            <button
              onClick={() => setSortBy('created_at')}
              className={`px-3 py-1 rounded-full text-[10px] font-medium transition-colors ${
                sortBy === 'created_at' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-slate-100 dark:bg-white/5 text-slate-500 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-white/10'
              }`}
            >
              <Clock size={10} className="inline mr-1" />
              发送时间
            </button>
            <button
              onClick={() => setSortBy('meeting_start_time')}
              className={`px-3 py-1 rounded-full text-[10px] font-medium transition-colors ${
                sortBy === 'meeting_start_time' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-slate-100 dark:bg-white/5 text-slate-500 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-white/10'
              }`}
            >
              <Calendar size={10} className="inline mr-1" />
              会议时间
            </button>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4 no-scrollbar pb-40">
        {/* 集成式任务输入面板 */}
        {activeCategory === 'all' && (
          <div className={`glass-card rounded-[2.2rem] border-slate-200 dark:border-white/10 bg-white dark:bg-white/[0.03] transition-all duration-300 flex flex-col overflow-hidden mb-6 ${isInputFocused ? 'ring-1 ring-blue-500/40 shadow-2xl scale-[1.01]' : 'shadow-sm'}`}>
            <div className="p-1.5 flex items-center">
              <div className="w-10 h-10 rounded-full flex items-center justify-center text-slate-400 dark:text-slate-600 shrink-0">
                <PenLine size={18} />
              </div>
              <input 
                type="text" 
                value={newTaskTitle}
                onFocus={() => setIsInputFocused(true)}
                onChange={(e) => setNewTaskTitle(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAddUserTask()}
                placeholder="在此输入新的待办指令..."
                className="flex-1 bg-transparent border-none focus:outline-none px-2 py-4 text-[14px] text-slate-800 dark:text-white placeholder:text-slate-300 dark:placeholder:text-slate-800 font-light"
              />
              <button 
                onClick={handleAddUserTask}
                className={`w-10 h-10 rounded-full flex items-center justify-center text-white active:scale-90 transition-all shadow-lg ${
                  newTaskTitle.trim() ? 'bg-blue-600 glow-blue' : 'bg-slate-100 dark:bg-white/5 text-slate-300 dark:text-slate-800 pointer-events-none'
                }`}
              >
                <ArrowRight size={16} />
              </button>
            </div>
            
            <div className={`flex items-center gap-1.5 px-3 pb-3 transition-all duration-300 overflow-hidden ${isInputFocused || newTaskTitle.length > 0 ? 'max-h-12 opacity-100 mt-1' : 'max-h-0 opacity-0'}`}>
                {[
                    { id: 'urgent', label: '紧急', color: 'red', icon: AlertCircle },
                    { id: 'high', label: '重要', color: 'blue', icon: Clock },
                    { id: 'normal', label: '普通', color: 'slate', icon: Info },
                ].map((p) => (
                    <button
                        key={p.id}
                        onClick={() => setNewTaskPriority(p.id as PriorityType)}
                        className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-[10px] font-bold transition-all ${
                            newTaskPriority === p.id 
                            ? `bg-${p.color}-500/10 dark:bg-${p.color}-500/20 border-${p.color}-500/30 dark:border-${p.color}-500/40 text-${p.color}-600 dark:text-${p.color}-400 ring-1 ring-${p.color}-500/10 shadow-md`
                            : 'bg-white/20 dark:bg-white/2 border-slate-200 dark:border-white/5 text-slate-400 dark:text-slate-600 hover:text-slate-600'
                        }`}
                    >
                        <p.icon size={10} />
                        {p.label}
                    </button>
                ))}
            </div>
          </div>
        )}

        {/* 任务列表 & 会议纪要列表 */}
        {activeCategory === 'meeting_minutes' ? (
          <div className="space-y-3">
            {meetingMinutes.map((item) => (
              <div 
                key={item.id} 
                onClick={() => setSelectedMeeting(item)}
                className="glass-card p-4 rounded-[1.5rem] bg-white/60 dark:bg-white/5 border-slate-100 dark:border-white/5 transition-all relative group overflow-hidden shadow-sm hover:shadow-md active:scale-[0.98]"
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-blue-500/10 flex items-center justify-center shrink-0">
                    <FileText size={18} className="text-blue-600 dark:text-blue-400" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1.5">
                      <span className="text-[9px] font-mono-prec text-slate-400 dark:text-slate-600 uppercase tracking-tighter truncate">
                        {sortBy === 'meeting_start_time'
                          ? <><Calendar size={10} className="inline mr-1" />{item.start_time ? new Date(item.start_time).toLocaleString() : ''}</>
                          : <><Clock size={10} className="inline mr-1" />{item.created_at ? new Date(item.created_at).toLocaleString() : ''}</>
                        }
                      </span>
                    </div>
                    <h3 className="text-[13px] font-bold truncate text-slate-800 dark:text-slate-200 group-hover:text-blue-600 dark:group-hover:text-blue-400">
                      {item.title}
                    </h3>
                  </div>
                  <ChevronLeft className="rotate-180 text-slate-300 dark:text-slate-700 group-hover:text-blue-600 dark:group-hover:text-blue-500 transition-colors" size={12} />
                </div>
              </div>
            ))}
            {meetingMinutes.length === 0 && (
              <div className="h-64 flex flex-col items-center justify-center opacity-10">
                <FileText size={48} className="text-slate-900 dark:text-slate-600 mb-4" />
                <span className="text-[10px] font-mono uppercase tracking-[0.2em]">NO_MEETINGS</span>
              </div>
            )}
          </div>
        ) : (
        <div className="space-y-3">
          {filteredTasks.map((item) => (
            <div 
              key={item.id} 
              onClick={() => handleTaskClick(item)}
              className={`glass-card p-4 rounded-[1.5rem] bg-white/60 dark:bg-white/5 border-slate-100 dark:border-white/5 transition-all relative group overflow-hidden shadow-sm hover:shadow-md ${
                item.completed || item.status === 'completed' ? 'opacity-40 grayscale' : 'active:scale-[0.98]'
              }`}
            >
              <div className="flex items-center gap-3">
                {item.isUserTask && (
                  <button 
                    onClick={(e) => { e.stopPropagation(); toggleUserTask(item.id); }}
                    className={`w-5 h-5 rounded-full border flex items-center justify-center shrink-0 transition-all ${
                      item.completed ? 'bg-emerald-500 border-emerald-400' : 'border-slate-300 dark:border-white/20 hover:border-blue-500/50'
                    }`}
                  >
                    {item.completed && <CheckSquare size={12} className="text-white" />}
                  </button>
                )}
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1.5">
                    <PriorityTag priority={item.priority} />
                    <span className="text-[9px] font-mono-prec text-slate-400 dark:text-slate-600 uppercase tracking-tighter truncate">
                      {sortBy === 'meeting_start_time' && item.meeting_start_time 
                        ? <><Calendar size={10} className="inline mr-1" />{item.meeting_start_time}</>
                        : <><Clock size={10} className="inline mr-1" />{item.meeting_created_at || item.time}</>
                      } • {item.sender}
                    </span>
                  </div>
                  <h3 className={`text-[13px] font-bold truncate transition-colors ${
                    item.completed || item.status === 'completed' ? 'text-slate-400 line-through' : 'text-slate-800 dark:text-slate-200 group-hover:text-blue-600 dark:group-hover:text-blue-400'
                  }`}>
                    {item.title}
                  </h3>
                </div>

                <div className="flex items-center gap-2">
                  {item.isUserTask ? (
                    <button 
                      onClick={(e) => { e.stopPropagation(); deleteUserTask(item.id); }}
                      className="p-2 text-slate-300 hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100"
                    >
                      <Trash2 size={14} />
                    </button>
                  ) : (
                    <ChevronLeft className="rotate-180 text-slate-300 dark:text-slate-700 group-hover:text-blue-600 dark:group-hover:text-blue-500 transition-colors" size={12} />
                  )}
                </div>
              </div>
            </div>
          ))}

          {filteredTasks.length === 0 && (
            <div className="h-64 flex flex-col items-center justify-center opacity-10">
              <CheckSquare size={48} className="text-slate-900 dark:text-slate-600 mb-4" />
              <span className="text-[10px] font-mono uppercase tracking-[0.2em]">POOL_EMPTY</span>
            </div>
          )}
        </div>
        )}
      </div>

      {/* 任务详情抽屉 */}
      {selectedItem && createPortal(
        <div className="fixed inset-0 z-[200] bg-white dark:bg-black animate-in slide-in-from-right duration-300 flex flex-col transition-colors duration-500">
          <div className="shrink-0 bg-white/95 dark:bg-black/95 backdrop-blur-xl border-b border-slate-200 dark:border-white/5 p-4 flex items-center justify-between z-50 shadow-sm safe-area-top">
            <button 
              onClick={() => setSelectedItem(null)} 
              className="px-4 py-2 bg-slate-100 dark:bg-white/10 rounded-full text-slate-900 dark:text-white flex items-center gap-2 active:scale-90 transition-all hover:bg-slate-200 dark:hover:bg-white/20"
            >
                <ChevronLeft size={18} />
                <span className="text-xs font-bold uppercase tracking-widest">返回列表</span>
            </button>
            <div className="text-[9px] font-bold text-slate-400 dark:text-slate-600 tracking-[0.3em] uppercase">执行情报视图</div>
          </div>

          <div className="flex-1 overflow-y-auto p-6 space-y-8 pb-32 safe-area-bottom">
             <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <PriorityTag priority={selectedItem.priority} />
                  <span className="text-xs font-mono-prec text-blue-600 dark:text-blue-500">{selectedItem.time}</span>
                </div>
                <h1 className="text-2xl font-bold leading-tight text-slate-900 dark:text-white">{selectedItem.title}</h1>
                
                <div className="flex items-center gap-3 p-4 glass-card rounded-2xl inline-flex border-slate-200 dark:border-white/10 bg-slate-50 dark:bg-white/5">
                    <div className="w-10 h-10 rounded-full bg-blue-600/10 flex items-center justify-center border border-blue-500/20">
                        <User size={18} className="text-blue-600 dark:text-blue-400" />
                    </div>
                    <div className="flex flex-col">
                        <span className="text-sm font-bold text-slate-800 dark:text-white leading-none mb-1">{selectedItem.sender}</span>
                        <span className="text-[10px] text-slate-400 dark:text-slate-500 uppercase font-mono tracking-tighter">任务发起人</span>
                    </div>
                </div>
             </div>

             <div className="p-6 rounded-[2.5rem] bg-gradient-to-br from-blue-50 to-white dark:from-blue-900/20 dark:to-transparent border border-blue-100 dark:border-white/10 shadow-xl dark:shadow-2xl relative overflow-hidden">
                <div className="absolute -right-4 -top-4 opacity-5 dark:opacity-10">
                  <Sparkles size={100} className="text-blue-500" />
                </div>
                <div className="flex items-center gap-2 text-blue-600 dark:text-blue-400 text-[10px] font-bold uppercase tracking-widest mb-4">
                    <Sparkles size={14} /> 智僚增强分析
                </div>
                <p className="text-sm text-slate-700 dark:text-slate-200 italic leading-relaxed mb-6 relative z-10">"{selectedItem.aiSummary}"</p>
                <button 
                  onClick={handleActionClick}
                  className="w-full bg-blue-600 text-white py-4 rounded-2xl text-xs font-bold uppercase tracking-widest shadow-lg glow-blue active:scale-[0.97] transition-all border border-blue-400/30"
                >
                    准备相关材料
                </button>
             </div>

             <div className="space-y-4">
                <div className="text-[10px] font-bold text-slate-400 dark:text-slate-600 uppercase tracking-widest flex items-center gap-2">
                    <div className="h-px flex-1 bg-slate-200 dark:bg-white/5"></div>
                    指令原文内容
                    <div className="h-px flex-1 bg-slate-200 dark:bg-white/5"></div>
                </div>
                <div className="text-slate-600 dark:text-slate-300 text-[15px] leading-relaxed font-light whitespace-pre-wrap px-2">
                    {selectedItem.content}
                </div>
             </div>
          </div>
        </div>,
        document.body
      )}

      {/* 会议详情抽屉 - 三大模块展示 */}
      {selectedMeeting && createPortal(
        <div className="fixed inset-0 z-[200] bg-white dark:bg-black animate-in slide-in-from-right duration-300 flex flex-col transition-colors duration-500">
          <div className="shrink-0 bg-white/95 dark:bg-black/95 backdrop-blur-xl border-b border-slate-200 dark:border-white/5 p-4 flex items-center justify-between z-50 shadow-sm safe-area-top">
            <button 
              onClick={() => setSelectedMeeting(null)} 
              className="px-4 py-2 bg-slate-100 dark:bg-white/10 rounded-full text-slate-900 dark:text-white flex items-center gap-2 active:scale-90 transition-all hover:bg-slate-200 dark:hover:bg-white/20"
            >
                <ChevronLeft size={18} />
                <span className="text-xs font-bold uppercase tracking-widest">返回列表</span>
            </button>
            <div className="text-[9px] font-bold text-slate-400 dark:text-slate-600 tracking-[0.3em] uppercase">会议纪要详情</div>
          </div>

          <div className="flex-1 overflow-y-auto p-6 space-y-6 pb-32 safe-area-bottom">
             {/* 会议主题和时间 */}
             <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono text-blue-600 dark:text-blue-500">
                    {new Date(selectedMeeting.start_time).toLocaleString()}
                  </span>
                </div>
                <h1 className="text-xl font-bold leading-tight text-slate-900 dark:text-white">{selectedMeeting.title}</h1>
             </div>
             
             {/* 模块一：会议链接 */}
             <div className="space-y-3">
                <div className="text-[10px] font-bold text-slate-400 dark:text-slate-600 uppercase tracking-widest flex items-center gap-2">
                    <div className="h-px flex-1 bg-slate-200 dark:bg-white/5"></div>
                    <LinkIcon size={12} />
                    会议链接
                    <div className="h-px flex-1 bg-slate-200 dark:bg-white/5"></div>
                </div>
                <div className="bg-slate-50 dark:bg-white/5 p-4 rounded-xl">
                  {selectedMeeting.location && selectedMeeting.location.startsWith('http') ? (
                      <a href={selectedMeeting.location} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-blue-600 hover:underline">
                          <LinkIcon size={14} />
                          <span className="text-sm break-all">{selectedMeeting.location}</span>
                      </a>
                  ) : (
                      <div className="flex items-center gap-2 text-slate-500">
                          <Target size={14} />
                          <span className="text-sm">{selectedMeeting.location || '无会议链接'}</span>
                      </div>
                  )}
                </div>
             </div>

             {/* 模块二：会议纪要正文 */}
             <div className="space-y-3">
                <div className="text-[10px] font-bold text-slate-400 dark:text-slate-600 uppercase tracking-widest flex items-center gap-2">
                    <div className="h-px flex-1 bg-slate-200 dark:bg-white/5"></div>
                    <FileText size={12} />
                    会议纪要正文
                    <div className="h-px flex-1 bg-slate-200 dark:bg-white/5"></div>
                </div>
                <div className="text-slate-600 dark:text-slate-300 text-[15px] leading-relaxed font-light whitespace-pre-wrap bg-slate-50 dark:bg-white/5 p-4 rounded-xl">
                    {selectedMeeting.summary || "暂无摘要"}
                </div>
             </div>
             
             {/* 模块三：会议待办事项 */}
             <div className="space-y-3">
                <div className="text-[10px] font-bold text-slate-400 dark:text-slate-600 uppercase tracking-widest flex items-center gap-2">
                    <div className="h-px flex-1 bg-slate-200 dark:bg-white/5"></div>
                    <CheckSquare size={12} />
                    会议待办事项 ({meetingTodos.length})
                    <div className="h-px flex-1 bg-slate-200 dark:bg-white/5"></div>
                </div>
                
                <div className="space-y-2">
                  {/* 新增待办按钮 */}
                  {!isAddingTodo && (
                    <button
                      onClick={() => setIsAddingTodo(true)}
                      className="w-full py-3 border-2 border-dashed border-slate-200 dark:border-white/10 rounded-xl text-slate-500 dark:text-slate-400 text-sm font-medium hover:border-blue-400 hover:text-blue-600 dark:hover:border-blue-500 dark:hover:text-blue-400 transition-colors flex items-center justify-center gap-2"
                    >
                      <Plus size={16} />
                      新增待办
                    </button>
                  )}
                  
                  {/* 新增待办表单 */}
                  {isAddingTodo && (
                    <div className="bg-blue-50 dark:bg-blue-500/10 p-4 rounded-xl space-y-3">
                      <input
                        type="text"
                        placeholder="待办标题"
                        value={newTodoForm.title}
                        onChange={(e) => setNewTodoForm({...newTodoForm, title: e.target.value})}
                        className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-black/50 text-slate-900 dark:text-white text-sm"
                      />
                      <textarea
                        placeholder="待办详情（可选）"
                        value={newTodoForm.content}
                        onChange={(e) => setNewTodoForm({...newTodoForm, content: e.target.value})}
                        className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-black/50 text-slate-900 dark:text-white text-sm resize-none"
                        rows={2}
                      />
                      <div className="flex items-center gap-2">
                        <select
                          value={newTodoForm.priority}
                          onChange={(e) => setNewTodoForm({...newTodoForm, priority: e.target.value})}
                          className="px-3 py-2 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-black/50 text-slate-900 dark:text-white text-sm"
                        >
                          <option value="urgent">紧急</option>
                          <option value="high">重要</option>
                          <option value="normal">普通</option>
                        </select>
                        <button
                          onClick={handleAddTodo}
                          className="flex-1 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
                        >
                          保存
                        </button>
                        <button
                          onClick={() => { setIsAddingTodo(false); setNewTodoForm({ title: '', content: '', priority: 'normal' }); }}
                          className="px-4 py-2 bg-slate-200 dark:bg-white/10 text-slate-600 dark:text-slate-400 rounded-lg text-sm"
                        >
                          取消
                        </button>
                      </div>
                    </div>
                  )}
                  
                  {/* 待办列表 */}
                  {meetingTodos.map((todo) => (
                    <div key={todo.id} className="bg-slate-50 dark:bg-white/5 p-4 rounded-xl">
                      {editingTodo?.id === todo.id ? (
                        /* 编辑模式 */
                        <div className="space-y-3">
                          <input
                            type="text"
                            value={editForm.title}
                            onChange={(e) => setEditForm({...editForm, title: e.target.value})}
                            className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-black/50 text-slate-900 dark:text-white text-sm"
                          />
                          <textarea
                            value={editForm.content || ''}
                            onChange={(e) => setEditForm({...editForm, content: e.target.value})}
                            className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-black/50 text-slate-900 dark:text-white text-sm resize-none"
                            rows={2}
                          />
                          <div className="flex items-center gap-2">
                            <select
                              value={editForm.priority}
                              onChange={(e) => setEditForm({...editForm, priority: e.target.value})}
                              className="px-3 py-2 rounded-lg border border-slate-200 dark:border-white/10 bg-white dark:bg-black/50 text-slate-900 dark:text-white text-sm"
                            >
                              <option value="urgent">紧急</option>
                              <option value="high">重要</option>
                              <option value="normal">普通</option>
                            </select>
                            <button onClick={handleUpdateTodo} className="flex-1 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium">保存</button>
                            <button onClick={() => setEditingTodo(null)} className="px-4 py-2 bg-slate-200 dark:bg-white/10 text-slate-600 dark:text-slate-400 rounded-lg text-sm">取消</button>
                          </div>
                        </div>
                      ) : (
                        /* 展示模式 */
                        <div className="flex items-start gap-3">
                          <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center shrink-0 mt-0.5 ${
                            todo.status === 'completed' ? 'bg-green-500 border-green-500' : 'border-slate-300 dark:border-white/20'
                          }`}>
                            {todo.status === 'completed' && <Check size={12} className="text-white" />}
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-1">
                              <span className="text-sm font-medium text-slate-900 dark:text-white">{todo.title}</span>
                              <PriorityTag priority={todo.priority} />
                            </div>
                            {todo.content && (
                              <p className="text-xs text-slate-500 dark:text-slate-400 line-clamp-2">{todo.content}</p>
                            )}
                          </div>
                          <div className="flex items-center gap-1 shrink-0">
                            <button
                              onClick={() => { setEditingTodo(todo); setEditForm({ title: todo.title, content: todo.content || '', priority: todo.priority }); }}
                              className="p-1.5 rounded-lg hover:bg-slate-200 dark:hover:bg-white/10 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
                            >
                              <Edit2 size={14} />
                            </button>
                            <button
                              onClick={() => handleDeleteTodo(todo.id)}
                              className="p-1.5 rounded-lg hover:bg-red-100 dark:hover:bg-red-500/20 text-slate-400 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                            >
                              <Trash2 size={14} />
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                  
                  {meetingTodos.length === 0 && !isAddingTodo && (
                    <div className="text-center py-8 text-slate-400 dark:text-slate-500">
                      <CheckSquare size={32} className="mx-auto mb-2 opacity-30" />
                      <p className="text-sm">暂无待办事项</p>
                    </div>
                  )}
                </div>
             </div>
          </div>
        </div>,
        document.body
      )}
    </div>
  );
};

export default TodoView;



