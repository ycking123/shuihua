
import React, { useState, useEffect, useRef } from 'react';
import { Send, Sparkles, Cpu, Database, BarChart3, Target, Zap, Brain, Network, FileText, ChevronDown, ChevronUp, Share2 } from 'lucide-react';
import OntologySphere from './OntologySphere';
import ShareSheet from './ShareSheet';
import { GoogleGenAI } from "@google/genai";

type MessageCategory = 'standard' | 'urgent' | 'strategic';

interface MindMapNode {
  label: string;
  subNodes?: string[];
}

interface VisualData {
  type: 'analysis' | 'chart' | 'plan';
  title: string;
  conclusionCards: { label: string; value: string; trend: string; isGood: boolean }[];
  mindMap: MindMapNode[];
  detailedReport?: string;
}

interface Message {
  id: number;
  type: 'agent' | 'user';
  content: string;
  category?: MessageCategory;
  visual?: VisualData;
  isStreaming?: boolean;
  showReport?: boolean;
}

interface ThinkingStep {
  id: string;
  text: string;
  icon: any;
  status: 'pending' | 'active' | 'done';
}

const StrategicMindMap: React.FC<{ data: MindMapNode[] }> = ({ data }) => (
  <div className="space-y-3 mt-4">
    <div className="flex items-center gap-2 mb-2">
      <Network size={12} className="text-blue-500 dark:text-blue-400" />
      <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">战略决策逻辑链</span>
    </div>
    <div className="grid grid-cols-1 gap-2">
      {data.map((node, idx) => (
        <div key={idx} className="flex gap-3 relative group">
          <div className="flex flex-col items-center">
            <div className="w-2.5 h-2.5 rounded-full border-2 border-blue-500 bg-white dark:bg-black z-10"></div>
            {idx !== data.length - 1 && <div className="w-0.5 flex-1 bg-slate-200 dark:bg-white/10 my-1"></div>}
          </div>
          <div className="flex-1 pb-4">
            <div className="text-[13px] font-bold text-slate-800 dark:text-slate-100 mb-1">{node.label}</div>
            <div className="flex flex-wrap gap-1.5">
              {node.subNodes?.map((sub, sIdx) => (
                <span key={sIdx} className="px-2 py-0.5 rounded-md bg-white/40 dark:bg-white/5 border border-slate-200 dark:border-white/5 text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                  {sub}
                </span>
              ))}
            </div>
          </div>
        </div>
      ))}
    </div>
  </div>
);

const ChatView: React.FC<{ initialContext?: string | null; onClearContext?: () => void }> = ({ initialContext, onClearContext }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [sphereStatus, setSphereStatus] = useState<'idle' | 'thinking' | 'working'>('idle');
  const [shareConfig, setShareConfig] = useState<{ isOpen: boolean; data: any }>({ isOpen: false, data: {} });
  const [thinkingSteps, setThinkingSteps] = useState<ThinkingStep[]>([
    { id: '1', text: '获取商业情报', icon: Target, status: 'pending' },
    { id: '2', text: '逻辑交叉验证', icon: Database, status: 'pending' },
    { id: '3', text: '多维仿真推演', icon: BarChart3, status: 'pending' },
    { id: '4', text: '生成战略建议', icon: Zap, status: 'pending' },
  ]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const hasInteracted = messages.length > 0 || isThinking;

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isThinking]);

  useEffect(() => {
    if (initialContext) {
      handleSend(initialContext);
      onClearContext?.();
    }
  }, [initialContext]);

  const handleSend = async (text?: string) => {
    const content = text || inputValue;
    if (!content.trim()) return;
    
    setMessages(prev => [...prev, { id: Date.now(), type: 'user', content }]);
    setInputValue('');
    setIsThinking(true);
    setSphereStatus('thinking');

    const runSteps = async () => {
      for (let i = 0; i < thinkingSteps.length; i++) {
        setThinkingSteps(prev => prev.map((s, idx) => ({ 
          ...s, status: idx === i ? 'active' : (idx < i ? 'done' : 'pending') 
        })));
        await new Promise(r => setTimeout(r, 600));
      }
    };

    const callBackendAi = async () => {
      try {
        const response = await fetch('http://localhost:8002/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: content })
        });
        
        if (!response.ok) throw new Error('Backend connection failed');

        const data = await response.json();
        setMessages(prev => [...prev, {
          id: Date.now(),
          type: 'agent',
          content: data.summary,
          category: data.category,
          visual: {
            type: 'analysis',
            title: data.visualTitle,
            conclusionCards: data.conclusionCards,
            mindMap: data.mindMap,
            detailedReport: data.detailedReport
          }
        }]);
      } catch (e) {
        console.error(e);
        // Fallback error message
        setMessages(prev => [...prev, {
            id: Date.now(),
            type: 'agent',
            content: "系统连接异常，请确保后端服务已在 8002 端口启动。",
            category: 'standard'
        }]);
      }
    };

    const callAi = async () => {
      try {
        const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
        const systemInstruction = `
          你是一个战略智僚助手。你的职责是提供深度洞察、数据挖掘和可视化结论。
          输出结构必须包含JSON，格式如下：
          {
            "category": "urgent|strategic|standard",
            "summary": "一句简短的分析摘要",
            "visualTitle": "分析报告维度",
            "conclusionCards": [{"label": "关键指标", "value": "数据值", "trend": "+X%", "isGood": true}],
            "mindMap": [{"label": "逻辑节点", "subNodes": ["支撑项1", "支撑项2"]}],
            "detailedReport": "详细的推演逻辑和背景情报分析"
          }
        `;
        
        const response = await ai.models.generateContent({
          model: 'gemini-3-pro-preview',
          contents: content,
          config: { systemInstruction, responseMimeType: "application/json" }
        });

        const data = JSON.parse(response.text);
        setMessages(prev => [...prev, {
          id: Date.now(),
          type: 'agent',
          content: data.summary,
          category: data.category,
          visual: {
            type: 'analysis',
            title: data.visualTitle,
            conclusionCards: data.conclusionCards,
            mindMap: data.mindMap,
            detailedReport: data.detailedReport
          }
        }]);
      } catch (e) {
        console.error(e);
      }
    };

    await Promise.all([callBackendAi(), runSteps()]);
    setIsThinking(false);
    setSphereStatus('idle');
  };

  const toggleReport = (id: number) => {
    setMessages(prev => prev.map(m => m.id === id ? { ...m, showReport: !m.showReport } : m));
  };

  const handleOpenShare = (msg: Message) => {
    setShareConfig({
        isOpen: true,
        data: {
            title: `智能战略报告: ${msg.visual?.title || '综合推演'}`,
            type: 'REPORT',
            content: msg.visual?.detailedReport
        }
    });
  };

  return (
    <div className="flex flex-col h-full bg-slate-50 dark:bg-black overflow-hidden relative transition-colors duration-500">
      <ShareSheet 
        isOpen={shareConfig.isOpen} 
        onClose={() => setShareConfig({ ...shareConfig, isOpen: false })} 
        data={shareConfig.data} 
      />

      {/* 顶部交互区 */}
      <div className={`shrink-0 transition-all duration-700 ease-[cubic-bezier(0.23,1,0.32,1)] relative z-30 border-b border-slate-200 dark:border-white/5 ${
        hasInteracted ? 'h-[80px] bg-white/70 dark:bg-black/70 backdrop-blur-3xl' : 'h-[260px]'
      }`}>
        <div className={`absolute transition-all duration-1000 ease-[cubic-bezier(0.23,1,0.32,1)] ${
            hasInteracted ? '-left-12 top-1/2 -translate-y-1/2 scale-[0.45]' : 'left-1/2 -translate-x-1/2 top-4 scale-100'
        }`}>
           <OntologySphere status={sphereStatus} />
        </div>

        <div className={`absolute transition-all duration-700 ${
            hasInteracted ? 'left-24 right-4 top-1/2 -translate-y-1/2' : 'left-0 right-0 bottom-8 flex flex-col items-center'
        }`}>
            {!hasInteracted ? (
                <div className="text-center animate-in fade-in duration-1000 px-6">
                    <div className="flex items-center justify-center gap-2 mb-2 text-slate-400 dark:text-slate-500 font-mono text-[9px] uppercase tracking-[0.4em]">
                       <div className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse glow-blue"></div>
                       STRATEGIC_HUD_ACTIVE
                    </div>
                    <h1 className="text-2xl font-bold text-slate-900 dark:text-white leading-tight">
                        董事长，<br />水华精灵已就绪，请下达指令。
                    </h1>
                </div>
            ) : (
                <div className="flex flex-col gap-1 animate-in fade-in slide-in-from-left-4 duration-700">
                    <div className="flex items-center gap-1.5 mb-1 opacity-60">
                         <div className={`w-1 h-1 rounded-full ${isThinking ? 'bg-blue-600 animate-pulse' : 'bg-emerald-500'}`}></div>
                         <span className="text-[8px] font-bold text-slate-500 uppercase tracking-[0.2em]">
                            {isThinking ? '正在进行深度推演...' : '已完成战略分析'}
                         </span>
                    </div>
                    <div className="grid grid-cols-2 gap-1.5">
                        {thinkingSteps.map(step => (
                            <div key={step.id} className={`flex items-center gap-2 px-2.5 py-1 rounded-lg border transition-all duration-500 ${
                                step.status === 'active' ? 'bg-blue-500/10 border-blue-500/40 dark:border-blue-500/40 shadow-md dark:shadow-blue-500/10' : 
                                step.status === 'done' ? 'border-transparent opacity-60' : 'border-transparent opacity-10'
                            }`}>
                                <step.icon size={10} className={step.status === 'active' ? 'text-blue-600 dark:text-blue-400 animate-pulse' : 'text-slate-500'} />
                                <span className="text-[9px] font-bold text-slate-600 dark:text-slate-300 uppercase tracking-tighter truncate">{step.text}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
      </div>

      {/* 对话列表 - 增加 pb 以避开更靠上的输入框 */}
      <div className="flex-1 overflow-y-auto px-4 pt-6 pb-52 no-scrollbar">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex flex-col mb-8 ${msg.type === 'user' ? 'items-end' : 'items-start'} animate-in slide-in-from-bottom-2 duration-500`}>
            {msg.type === 'user' && (
              <div className="max-w-[90%] px-4 py-3 bg-blue-600 text-white rounded-[1.4rem] rounded-tr-none text-[14px] shadow-lg shadow-blue-500/20 font-medium">
                {msg.content}
              </div>
            )}

            {msg.type === 'agent' && (
              <div className="w-full space-y-4">
                <div className="flex items-start gap-2.5">
                  <div className="w-7 h-7 rounded-full bg-blue-600 flex items-center justify-center shrink-0 shadow-lg glow-blue mt-0.5">
                    <Brain size={14} className="text-white" />
                  </div>
                  <div className="flex-1 p-4 glass-card rounded-[1.4rem] rounded-tl-none text-[14px] leading-relaxed text-slate-800 dark:text-slate-200 relative group font-light shadow-sm">
                    {msg.content}
                  </div>
                </div>

                {msg.visual && (
                  <div className="w-full glass-card rounded-[2rem] border-slate-200 dark:border-white/10 bg-white/40 dark:bg-black/40 shadow-xl dark:shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-500 relative">
                    <div className="px-5 py-3 border-b border-slate-100 dark:border-white/5 bg-slate-50 dark:bg-white/5 flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <BarChart3 size={12} className="text-blue-600 dark:text-blue-400" />
                        <span className="text-[9px] font-bold text-slate-500 uppercase tracking-widest">{msg.visual.title}</span>
                      </div>
                      <div className="flex items-center gap-2.5">
                        <button 
                            onClick={() => handleOpenShare(msg)}
                            className="p-1.5 text-slate-400 dark:text-slate-500 hover:text-blue-600 active:scale-90 transition-all"
                        >
                            <Share2 size={13} />
                        </button>
                        <Zap size={12} className="text-emerald-500 animate-pulse" />
                      </div>
                    </div>

                    <div className="p-5">
                      <div className="grid grid-cols-2 gap-2.5 mb-5">
                        {msg.visual.conclusionCards.map((card, i) => (
                          <div key={i} className="p-3.5 rounded-xl bg-slate-100/50 dark:bg-white/5 border border-slate-200 dark:border-white/5 shadow-sm">
                            <div className="text-[8px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-1">{card.label}</div>
                            <div className="flex items-baseline gap-1.5">
                              <span className="text-lg font-mono-prec font-bold text-slate-900 dark:text-white tracking-tighter">{card.value}</span>
                              <span className={`text-[8px] font-bold ${card.isGood ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'}`}>
                                {card.trend}
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>

                      <StrategicMindMap data={msg.visual.mindMap} />

                      <div className="mt-5 flex flex-col gap-2">
                        {msg.visual.detailedReport && (
                          <button 
                            onClick={() => toggleReport(msg.id)}
                            className="w-full py-3.5 glass-card border-slate-200 dark:border-white/10 rounded-xl text-[10px] font-bold text-slate-600 dark:text-slate-300 uppercase tracking-widest flex items-center justify-center gap-2 active:scale-95 transition-all hover:bg-slate-100 dark:hover:bg-white/10"
                          >
                            {msg.showReport ? <><ChevronUp size={12} /> 收起分析</> : <><FileText size={12} /> 展开深度逻辑建议</>}
                          </button>
                        )}
                      </div>

                      {msg.showReport && msg.visual.detailedReport && (
                        <div className="mt-4 p-4 bg-slate-50 dark:bg-white/5 rounded-xl border border-slate-200 dark:border-white/5 text-[13px] leading-relaxed text-slate-700 dark:text-slate-300 whitespace-pre-wrap animate-in slide-in-from-top-2 duration-300 font-light shadow-inner">
                          {msg.visual.detailedReport}
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* 底部输入框 - 避开底部导航栏，位置从 bottom-[94px] 上移至 bottom-[116px] */}
      <div className="fixed bottom-[116px] left-0 right-0 px-5 z-40 pb-safe transition-all duration-500">
        <div className="max-w-2xl mx-auto relative group">
            <div className="absolute inset-0 bg-blue-600/5 dark:bg-blue-900/10 blur-[30px] rounded-[2rem] -z-10 group-focus-within:bg-blue-600/10 dark:group-focus-within:bg-blue-800/20 transition-all"></div>
            <div className="relative glass-card bg-white/95 dark:bg-black/70 backdrop-blur-3xl rounded-[2rem] border-slate-200 dark:border-white/10 p-1 flex items-center shadow-2xl">
                <div className="px-4 text-slate-400 dark:text-slate-600">
                    <Brain size={18} className={isThinking ? 'animate-pulse text-blue-600 dark:text-blue-400' : ''} />
                </div>
                <input 
                    type="text" 
                    value={inputValue}
                    disabled={isThinking}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                    placeholder={isThinking ? "思维推演中..." : "输入您的战略指令..."}
                    className="flex-1 bg-transparent border-none focus:outline-none py-4 text-[14px] text-slate-800 dark:text-white placeholder:text-slate-300 dark:placeholder:text-slate-700 font-light"
                />
                <button 
                    onClick={() => handleSend()}
                    disabled={isThinking || !inputValue.trim()}
                    className={`w-10 h-10 rounded-full flex items-center justify-center text-white active:scale-90 transition-all ${
                      isThinking || !inputValue.trim() ? 'bg-slate-100 dark:bg-white/5 text-slate-300 dark:text-slate-800' : 'bg-blue-600 shadow-lg glow-blue'
                    }`}
                >
                    <Send size={16} />
                </button>
            </div>
        </div>
      </div>
    </div>
  );
};

export default ChatView;
