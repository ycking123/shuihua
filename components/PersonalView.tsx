
import React, { useState } from 'react';
import { 
  User, Sparkles, Target, 
  Save, Brain, History,
  Database, Bookmark, ShieldCheck, 
  Trash2, ShieldAlert,
  Settings2, MessageCircle, X, Check,
  Wind, Waves, Flame, Cloud, Eye, Clock, RotateCcw, BarChart, GraduationCap,
  Cpu, UserCog,
  MessageSquare
} from 'lucide-react';

const TONE_MODES = [
  { 
    id: 'calm', 
    name: '专业冷静模式', 
    desc: '基于数据与逻辑深度推演，提供客观中立的专业建议', 
    icon: Waves, 
    color: 'blue' 
  },
  { 
    id: 'agile', 
    name: '敏捷执行模式', 
    desc: '聚焦行动指令与即时反馈，最大化缩短决策响应链路', 
    icon: Wind, 
    color: 'emerald' 
  },
  { 
    id: 'creative', 
    name: '深度推演模式', 
    desc: '跳出常规思维框架，从全局视野探索突变机遇', 
    icon: Flame, 
    color: 'orange' 
  },
  { 
    id: 'balanced', 
    name: '柔波共理模式', 
    desc: '兼顾组织情绪与人文维度，提供更具温度的协同支持', 
    icon: Cloud, 
    color: 'purple' 
  }
];

const PersonalView: React.FC = () => {
  const [memo, setMemo] = useState("最近关注:AI是否能辅助经销商更快速地生成设计效果图、自动化获客或进行客户关系管理。");
  const [showToneSelector, setShowToneSelector] = useState(false);
  const [currentTone, setCurrentTone] = useState(TONE_MODES[0]);

  const [memories, setMemories] = useState([
    {
      id: 1,
      category: '重点关注',
      content: '本年每个季度欧神诺瓷砖板块经营性现金流净流入状态，以及综合融资成本情况和相关波动。',
      timestamp: '2026-02-06 14:30',
      icon: Eye,
      color: 'blue'
    },
    {
      id: 2,
      category: '短期记忆',
      content: '董事长在最近与人力开会时强调了营销板块需要更多具备AI能力的优秀导购。（近期会议重点）',
      timestamp: '2026-02-06 10:22',
      icon: Clock,
      color: 'orange'
    },
    {
      id: 3,
      category: '情景回顾',
      content: '董事长在历史汇报中更倾向于先看利润质量，而不是销售规模（决策偏好记录）',
      timestamp: '2026-02-03 16:45',
      icon: RotateCcw,
      color: 'purple'
    },
    {
      id: 4,
      category: '事实偏好',
      content: '董事长偏好"结论先行"+"穿透数据"。AI 应先给出一个结论，再提供可点击查看的底层原始数据。',
      timestamp: '2026-01-28 11:20',
      icon: BarChart,
      color: 'emerald'
    },
    {
      id: 5,
      category: '经验积累',
      content: '模型沉淀：在市场下行周期中，“智慧精装”板块的毛利率通常较传统板块高出 6.4%，具备更强防御属性。',
      timestamp: '2026-01-15 10:05',
      icon: GraduationCap,
      color: 'blue'
    }
  ]);

  const deleteMemory = (id: number) => {
    setMemories(memories.filter(m => m.id !== id));
  };

  const handleSelectTone = (tone: typeof TONE_MODES[0]) => {
    setCurrentTone(tone);
    setShowToneSelector(false);
  };

  return (
    <div className="p-6 space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500 pb-40 overflow-y-auto h-screen">
      {/* 个人信息卡片 */}
      <div className="glass-card p-8 rounded-[3rem] border-slate-200/60 dark:border-white/10 relative overflow-hidden shadow-xl">
        <div className="absolute -top-10 -right-10 w-48 h-48 bg-blue-500/10 blur-[60px] rounded-full"></div>
        <div className="flex items-center gap-6 relative z-10">
          <div className="w-20 h-20 rounded-[2rem] bg-gradient-to-tr from-blue-600 to-indigo-700 p-0.5 shadow-2xl shadow-blue-500/20">
            <div className="w-full h-full rounded-[1.9rem] bg-white dark:bg-black flex items-center justify-center">
                <User size={40} className="text-blue-600 dark:text-white" />
            </div>
          </div>
          <div className="flex flex-col">
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">吴志雄</h2>
            <div className="flex items-center gap-2 mt-1">
                <span className="text-[10px] text-blue-600 dark:text-blue-400 font-bold uppercase tracking-[0.2em]">董事长</span>
                <span className="w-1 h-1 rounded-full bg-slate-300 dark:bg-slate-700"></span>
                <span className="text-[10px] text-slate-400 dark:text-slate-500 font-mono">X-ESSENCE-001</span>
            </div>
          </div>
        </div>
        
        <div className="mt-8 grid grid-cols-2 gap-4">
            <div className="p-4 bg-slate-50/80 dark:bg-white/[0.03] border border-slate-100 dark:border-white/5 rounded-[1.8rem] flex flex-col gap-2 relative overflow-hidden shadow-inner">
                <div className="flex items-center gap-2">
                  <ShieldAlert size={12} className="text-red-500" />
                  <span className="text-[9px] text-slate-500 font-bold uppercase tracking-widest">访问权限</span>
                </div>
                <span className="text-xs font-bold text-slate-800 dark:text-white">全量超级权限</span>
                <div className="absolute bottom-0 left-0 h-1 w-1/2 bg-red-500/20"></div>
            </div>
            <div 
              onClick={() => setShowToneSelector(true)}
              className="p-4 bg-slate-50/80 dark:bg-white/[0.03] border border-slate-100 dark:border-white/5 rounded-[1.8rem] flex flex-col gap-2 group cursor-pointer active:scale-95 transition-all shadow-inner"
            >
                <div className="flex items-center gap-2">
                  <MessageCircle size={12} className="text-blue-600 dark:text-blue-400" />
                  <span className="text-[9px] text-slate-500 font-bold uppercase tracking-widest">交互人格</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className={`text-xs font-bold text-${currentTone.color}-600 dark:text-${currentTone.color}-400`}>{currentTone.name.split('模式')[0]}</span>
                  <Settings2 size={12} className="text-slate-400 animate-spin-slow" />
                </div>
                <div className={`absolute bottom-0 left-0 h-1 w-1/2 bg-${currentTone.color}-500/20`}></div>
            </div>
        </div>
      </div>

      {/* 核心关注 */}
      <div className="space-y-4">
        <div className="flex items-center justify-between px-3">
            <div className="flex items-center gap-2">
                <Target size={16} className="text-blue-600 dark:text-blue-400" />
                <h3 className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-widest">核心关注设定</h3>
            </div>
            <button className="p-2 bg-blue-600/5 hover:bg-blue-600/10 rounded-full transition-colors text-blue-600 dark:text-blue-400">
                <Save size={14} />
            </button>
        </div>
        <div className="glass-card p-6 rounded-[2.5rem] border-slate-200/60 dark:border-white/5 bg-white/60 dark:bg-white/[0.02] shadow-sm">
            <textarea 
                value={memo}
                onChange={(e) => setMemo(e.target.value)}
                className="w-full bg-transparent border-none focus:outline-none text-slate-700 dark:text-slate-300 text-[14px] leading-relaxed h-32 resize-none placeholder:text-slate-300 dark:placeholder:text-slate-800 font-light"
                placeholder="在此定义您的核心关注点..."
            />
            <div className="mt-4 flex items-center gap-2 text-[10px] text-slate-400 dark:text-slate-600 italic font-medium">
                <UserCog size={12} /> 指导 AI 采用特定的推演逻辑与敏感度阈值
            </div>
        </div>
      </div>

      {/* 记忆库 */}
      <div className="space-y-4">
        <div className="flex items-center justify-between px-3">
          <div className="flex items-center gap-2">
              <Brain size={16} className="text-purple-600 dark:text-purple-400" />
              <h3 className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-widest">AI 智僚核心记忆库</h3>
          </div>
          <div className="flex items-center gap-2 px-2 py-0.5 rounded-full bg-slate-100 dark:bg-white/5 border border-slate-200 dark:border-white/10">
            <span className="text-[9px] font-mono text-slate-500">LOAD: 15%</span>
          </div>
        </div>
        
        <div className="space-y-4">
          {memories.map((memory) => (
            <div key={memory.id} className="glass-card p-6 rounded-[2.5rem] border-slate-200/60 dark:border-white/5 bg-white/80 dark:bg-white/[0.01] hover:bg-slate-50 dark:hover:bg-white/[0.03] transition-all group relative overflow-hidden shadow-sm">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-2.5">
                  <div className={`p-2 rounded-xl bg-${memory.color}-500/10 text-${memory.color}-600 dark:text-${memory.color}-400 shadow-sm border border-${memory.color}-500/10`}>
                    <memory.icon size={14} />
                  </div>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-lg border uppercase tracking-wider ${
                    memory.color === 'blue' ? 'bg-blue-500/5 border-blue-500/20 text-blue-600 dark:text-blue-400' :
                    memory.color === 'orange' ? 'bg-orange-500/5 border-orange-500/20 text-orange-600 dark:text-orange-400' :
                    memory.color === 'purple' ? 'bg-purple-500/5 border-purple-500/20 text-purple-600 dark:text-purple-400' :
                    'bg-emerald-500/5 border-emerald-500/20 text-emerald-600 dark:text-emerald-400'
                  }`}>
                    {memory.category}
                  </span>
                </div>
                <button 
                  onClick={() => deleteMemory(memory.id)}
                  className="p-2 text-slate-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all active:scale-90"
                >
                  <Trash2 size={16} />
                </button>
              </div>
              <p className="text-[14px] text-slate-700 dark:text-slate-200 leading-relaxed font-medium mb-4">
                {memory.content}
              </p>
              <div className="flex items-center justify-between pt-4 border-t border-slate-100 dark:border-white/5">
                <div className="flex items-center gap-1.5 text-[10px] font-mono text-slate-400 dark:text-slate-600">
                  <History size={10} />
                  {memory.timestamp}
                </div>
                <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-50 dark:bg-black/20">
                   <Bookmark size={10} className="text-blue-500 fill-blue-500/20" />
                   <span className="text-[9px] font-bold text-slate-500 dark:text-slate-700 uppercase tracking-widest">固化存储</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 调色板对话框适配 */}
      {showToneSelector && (
        <div className="fixed inset-0 z-[150] flex items-end justify-center px-4 pb-12 animate-in fade-in duration-300">
          <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" onClick={() => setShowToneSelector(false)}></div>
          <div className="w-full max-w-md glass-card rounded-[3rem] border-slate-200/60 dark:border-white/10 p-8 z-10 animate-in slide-in-from-bottom-8 duration-500 bg-white/90 dark:bg-black/80 shadow-2xl">
            <div className="flex items-center justify-between mb-8">
              <div className="flex items-center gap-3">
                <h3 className="text-base font-bold text-slate-900 dark:text-white uppercase tracking-tight">智僚交互模态</h3>
              </div>
              <button onClick={() => setShowToneSelector(false)} className="p-2 text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors">
                <X size={20} />
              </button>
            </div>
            
            <div className="space-y-4">
              {TONE_MODES.map((tone) => (
                <div 
                  key={tone.id}
                  onClick={() => handleSelectTone(tone)}
                  className={`p-5 rounded-[2rem] border transition-all cursor-pointer flex items-center gap-5 group ${
                    currentTone.id === tone.id 
                    ? `bg-${tone.color}-600/10 border-${tone.color}-500/40 shadow-sm` 
                    : 'bg-slate-50/50 dark:bg-white/[0.02] border-slate-100 dark:border-white/5 hover:bg-slate-100/80 dark:hover:bg-white/[0.05]'
                  }`}
                >
                  <div className={`w-12 h-12 rounded-2xl flex items-center justify-center shrink-0 ${
                    currentTone.id === tone.id ? `bg-${tone.color}-600 text-white` : 'bg-slate-200 dark:bg-white/5 text-slate-500 dark:text-slate-600'
                  }`}>
                    <tone.icon size={24} />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <span className={`text-sm font-bold ${currentTone.id === tone.id ? `text-${tone.color}-600 dark:text-${tone.color}-400` : 'text-slate-700 dark:text-slate-300'}`}>
                        {tone.name}
                      </span>
                      {currentTone.id === tone.id && <Check size={18} className={`text-${tone.color}-600 dark:text-${tone.color}-400`} />}
                    </div>
                    <p className="text-[11px] text-slate-500 dark:text-slate-500 mt-1 line-clamp-1 group-hover:line-clamp-none leading-relaxed transition-all">
                      {tone.desc}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PersonalView;
