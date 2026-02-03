
import React, { useState, useMemo } from 'react';
import { createPortal } from 'react-dom';
import { 
  CheckSquare, Sparkles, ChevronLeft, Search, 
  Layers, Inbox, Coffee, ShieldCheck, Trash2,
  Target, ArrowRight, PenLine, User, AlertCircle, Clock, Info,
  MessageSquare
} from 'lucide-react';
import { TODOS_DATA } from '../constants';
import { ViewType } from '../types';

type TodoCategory = 'all' | 'email' | 'meeting' | 'approval' | 'chat_record';
type PriorityType = 'urgent' | 'high' | 'normal';

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
  const [activeCategory, setActiveCategory] = useState<TodoCategory>('all');
  const [userTasks, setUserTasks] = useState<TaskItem[]>([]);
  const [backendTasks, setBackendTasks] = useState<TaskItem[]>([]); // New state for backend tasks
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskPriority, setNewTaskPriority] = useState<PriorityType>('high');
  const [isInputFocused, setIsInputFocused] = useState(false);

  // Fetch tasks from backend on mount
  React.useEffect(() => {
    const fetchTodos = async () => {
      try {
        // Use hostname to adapt to both local and server environments
        const hostname = window.location.hostname;
        let backendUrl = `http://${window.location.hostname}:8000/api/todos`;
        
        // If local development (npm run dev), use proxy
        if (import.meta.env.DEV) {
             backendUrl = '/api/todos';
        }

        // Add Authorization header if token exists
        const token = localStorage.getItem('token');
        const headers: HeadersInit = {
            'Content-Type': 'application/json'
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const res = await fetch(backendUrl, { headers });
        if (res.ok) {
          const data = await res.json();
          setBackendTasks(data);
        } else {
            console.error(`Fetch failed with status: ${res.status}`);
            // Do not throw, just log. 
        }
      } catch (e: any) {
        console.error("Failed to fetch todos:", e);
        // Maybe show a toast or small error indicator in UI, but for now just console
      }
    };
    fetchTodos();
    // Poll every 5 seconds for updates
    const interval = setInterval(fetchTodos, 5000);
    return () => clearInterval(interval);
  }, []);

  const categories = [
    { id: 'all', label: '全部待办', icon: Layers },
    { id: 'email', label: '邮件', icon: Inbox },
    { id: 'meeting', label: '会议', icon: Coffee },
    { id: 'approval', label: '审批', icon: ShieldCheck },
    { id: 'chat_record', label: '其他', icon: MessageSquare },
  ];

  const getCount = (id: string) => {
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

        {/* 任务列表 */}
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
                      {item.time} • {item.sender}
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
    </div>
  );
};

export default TodoView;



