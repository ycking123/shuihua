import React, { useState, useEffect, useRef } from 'react';
import { Send, Brain, Database } from 'lucide-react';
import OntologySphere from './OntologySphere';

interface Message {
  id: string | number;
  type: 'agent' | 'user';
  content: string;
}

const ChatView: React.FC<{ initialContext?: string | null; onClearContext?: () => void }> = ({ initialContext, onClearContext }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');    
  const [isThinking, setIsThinking] = useState(false); 
  const [isRagEnabled, setIsRagEnabled] = useState(false);
  const [sphereStatus, setSphereStatus] = useState<'idle' | 'thinking' | 'working'>('idle');
  const messagesEndRef = useRef<HTMLDivElement>(null); 

  const hasInteracted = messages.length > 0 || isThinking;

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isThinking]);

  // Load history on mount
  useEffect(() => {
    const fetchHistory = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) return;

            const getBackendUrl = () => {
                if (import.meta.env.DEV) return '/api/chat/history';
                return `http://${window.location.hostname}:8000/api/chat/history`;
            };

            const res = await fetch(getBackendUrl(), {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (res.ok) {
                 const data = await res.json();
                 const historyMsgs: Message[] = data.map((m: any) => ({
                     id: m.id, 
                     type: m.role === 'user' ? 'user' : 'agent',
                     content: m.content
                 }));
                 
                 setMessages(prev => {
                     const existingIds = new Set(prev.map(p => p.id));
                     const newMsgs = historyMsgs.filter(h => !existingIds.has(h.id));
                     return [...newMsgs, ...prev];
                 });
             }
        } catch (e) {
            console.error("Fetch history failed", e);
        }
    };
    fetchHistory();
  }, []);

  useEffect(() => {
    if (initialContext) {
      handleSend(initialContext);
      onClearContext?.();
    }
  }, [initialContext]);

  const handleSend = async (text?: string) => {        
    const content = text || inputValue;
    if (!content.trim() || isThinking) return;

    // Add user message
    const userMsg: Message = { id: Date.now(), type: 'user', content };
    setMessages(prev => [...prev, userMsg]);
    setInputValue('');
    setIsThinking(true);
    setSphereStatus('working'); // Start animation immediately

    // Add placeholder for agent message
    const agentMsgId = Date.now() + 1;
    setMessages(prev => [...prev, { id: agentMsgId, type: 'agent', content: '' }]);

    try {
      // Determine backend URL based on environment
      const getBackendUrl = () => {
          // Use Vite proxy in development mode
          if (import.meta.env.DEV) {
               return '/api/chat';
          }
          // Otherwise use the same hostname as the frontend
          return `http://${window.location.hostname}:8000/api/chat`;
      };

      const backendUrl = getBackendUrl();
      const token = localStorage.getItem('token');
      const headers: HeadersInit = {
        'Content-Type': 'application/json'
      };
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(backendUrl, {
          method: 'POST',
          headers: headers,
          body: JSON.stringify({ 
            messages: [...messages.map(m => ({ role: m.type === 'user' ? 'user' : 'assistant', content: m.content })), { role: 'user', content }],
            use_rag: isRagEnabled
          }) 
      });

      if (!response.ok) throw new Error('Backend connection failed');
      if (!response.body) throw new Error('No response body');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulatedContent = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.replace('data: ', '').trim();
            if (dataStr === '[DONE]') break;
            
            try {
              const data = JSON.parse(dataStr);
              if (data.content) {
                accumulatedContent += data.content;
                setMessages(prev => prev.map(m => 
                  m.id === agentMsgId ? { ...m, content: accumulatedContent } : m
                ));
              }
            } catch (e) {
              console.error('Error parsing SSE chunk', e);
            }
          }
        }
      }
    } catch (e: any) {
      console.error(e);
      const errorMessage = e.message || 'Unknown error';
      setMessages(prev => prev.map(m => 
        m.id === agentMsgId ? { ...m, content: `系统连接异常: ${errorMessage}。请确保后端服务已在 8000 端口启动。` } : m
      ));
    } finally {
      setIsThinking(false);
      setSphereStatus('idle');
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-50 dark:bg-black overflow-hidden relative transition-colors duration-500">

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
                        董事长，<br />水华精灵已就绪， 请下达指令。
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
                </div>
            )}
        </div>
      </div>

      {/* 对话列表 */}  
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
                  <div className="w-7 h-7 rounded-full bg-blue-600 flex items-center justify-center shrink-0 shadow-lg glow-blue mt-0">
                    <Brain size={14} className="text-white" />
                  </div>
                  <div className="flex-1 p-4 glass-card rounded-[1.4rem] rounded-tl-none text-[14px] leading-relaxed text-slate-800 dark:text-slate-200 relative group font-light shadow-sm whitespace-pre-wrap">
                    {msg.content || <span className="animate-pulse">Thinking...</span>}
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* 底部输入框 */}
      <div className="fixed bottom-[116px] left-0 right-0 px-5 z-40 pb-safe transition-all duration-500">     
        <div className="max-w-2xl mx-auto relative group">
            <div className="absolute inset-0 bg-blue-600/5 dark:bg-blue-900/10 blur-[30px] rounded-[2rem] -z-10 group-focus-within:bg-blue-600/10 dark:group-focus-within:bg-blue-800/20 transition-all"></div>
            <div className="relative glass-card bg-white/95 dark:bg-black/70 backdrop-blur-3xl rounded-[2rem] border-slate-200 dark:border-white/10 p-1 flex items-center shadow-2xl">
                <div className="px-3 text-slate-400 dark:text-slate-600">
                    <Brain size={18} className={isThinking ? 'animate-pulse text-blue-600 dark:text-blue-400' : ''} />
                </div>
                
                <button
                    onClick={() => setIsRagEnabled(!isRagEnabled)}
                    className={`mr-2 px-3 py-1.5 rounded-full flex items-center gap-1.5 transition-all text-[10px] font-bold uppercase tracking-wider ${
                      isRagEnabled 
                      ? 'bg-blue-600/10 text-blue-600 border border-blue-600/20' 
                      : 'bg-slate-100 dark:bg-white/5 text-slate-400 dark:text-slate-600 hover:bg-slate-200 dark:hover:bg-white/10'
                    }`}
                >
                    <Database size={12} />
                    {isRagEnabled ? 'RAG ON' : 'RAG OFF'}
                </button>

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



