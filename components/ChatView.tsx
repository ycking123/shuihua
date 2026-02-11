import React, { useState, useEffect, useRef } from 'react';
import { Send, Brain, Database, ChevronDown, ChevronRight, Globe, Mic, MicOff } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import OntologySphere from './OntologySphere';

interface Message {
  id: string | number;
  type: 'agent' | 'user';
  content: string;
}

interface Model {
  id: string;
  name: string;
  provider: string;
}

const ThinkingProcess = ({ content }: { content: string }) => {
  const [isExpanded, setIsExpanded] = useState(true);

  return (
    <div className="mb-4 rounded-lg bg-slate-100 dark:bg-white/5 border border-slate-200 dark:border-white/10 overflow-hidden">
      <div 
        className="flex items-center gap-2 px-3 py-2 cursor-pointer hover:bg-slate-200/50 dark:hover:bg-white/10 transition-colors"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <Brain size={14} className="text-slate-500 animate-pulse" />
        <span className="text-xs font-medium text-slate-500">深度思考过程</span>
        {isExpanded ? <ChevronDown size={12} className="text-slate-400"/> : <ChevronRight size={12} className="text-slate-400"/>}
      </div>
      
      {isExpanded && (
        <div className="px-3 py-2 text-xs text-slate-500 dark:text-slate-400 border-t border-slate-200 dark:border-white/10 font-mono whitespace-pre-wrap leading-relaxed">
            {content}
        </div>
      )}
    </div>
  );
};

const ChatView: React.FC<{ initialContext?: string | null; onClearContext?: () => void }> = ({ initialContext, onClearContext }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');    
  const [isThinking, setIsThinking] = useState(false); 
  const [isRagEnabled, setIsRagEnabled] = useState(false);
  const [isWebSearchEnabled, setIsWebSearchEnabled] = useState(false);
  const [models, setModels] = useState<Model[]>([]);
  const [selectedModel, setSelectedModel] = useState<string>('glm-4-flash');
  const [sphereStatus, setSphereStatus] = useState<'idle' | 'thinking' | 'working'>('idle');
  const messagesEndRef = useRef<HTMLDivElement>(null); 
  
  // ASR State
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<any>(null);
  const wsRef = useRef<WebSocket | null>(null);

  const startRecording = async () => {
    // Check if browser supports mediaDevices
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert(
            "无法访问麦克风：浏览器安全策略限制。\n\n" +
            "1. 请确保您正在使用 HTTPS 协议访问 (https://...)\n" +
            "2. 如果是自签名证书，请允许浏览器的安全警告。\n" +
            "3. 如果必须使用 HTTP，请在浏览器地址栏输入 chrome://flags/#unsafely-treat-insecure-origin-as-secure \n" +
            "   将您的访问地址填入并设为 Enabled，然后重启浏览器。"
        );
        return;
    }

    try {
      // 1. Get user media first
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // 2. Create AudioContext IMMEDIATELY after user interaction/permission
      // This is critical for Autoplay Policy
      const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
      const audioContext = new AudioContextClass({ sampleRate: 16000 });

      // 3. Connect WebSocket
      const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      // Use the same host/port as the frontend (Vite proxy will handle it)
      let wsUrl = `${wsProtocol}//${window.location.host}/api/asr`;
      
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        console.log("ASR WebSocket Connected");
        setIsRecording(true);
        // Pass the already created audioContext
        processAudio(stream, ws, audioContext);
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.text) {
               setInputValue(prev => prev + data.text);
          }
          if (data.error) {
              console.error(data.error);
              alert(`识别错误: ${data.error}`);
              stopRecording();
          }
        } catch (e) {
          console.error("Error parsing ASR message:", e);
        }
      };
      
      ws.onerror = (e) => {
          console.error("WebSocket error", e);
          alert("连接语音服务失败，请检查网络或稍后重试。");
          stopRecording();
      }

      ws.onclose = () => {
          console.log("WebSocket closed");
          setIsRecording(false);
      }

    } catch (err: any) {
      console.error('Error accessing microphone:', err);
      // Detailed error handling
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
          alert("无法访问麦克风：权限被拒绝。请在浏览器地址栏点击锁形图标，允许使用麦克风。");
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
          alert("无法访问麦克风：未找到麦克风设备。");
      } else if (err.name === 'NotReadableError' || err.name === 'TrackStartError') {
          alert("无法访问麦克风：麦克风可能被其他应用占用。");
      } else if (err.name === 'OverconstrainedError') {
          alert("无法访问麦克风：请求的麦克风参数不满足要求。");
      } else if (err.name === 'SecurityError' || err.name === 'SecureContextRequiredError') {
         alert("无法访问麦克风：安全策略限制。请确保使用 localhost 或 HTTPS 访问。如果使用 IP 访问，浏览器可能因安全原因禁用麦克风。");
      } else {
         alert(`无法访问麦克风 (${err.name}): ${err.message}`);
      }
    }
  };

  const processAudio = (stream: MediaStream, ws: WebSocket, audioContext: AudioContext) => {
      // AudioContext is passed in, not created here
      const source = audioContext.createMediaStreamSource(stream);
      // Reduce buffer size to 1024 (approx 64ms) for smoother streaming
      const processor = audioContext.createScriptProcessor(1024, 1, 1);

      source.connect(processor);
      processor.connect(audioContext.destination);

      processor.onaudioprocess = (e) => {
          if (ws.readyState !== WebSocket.OPEN) return;
          
          const inputData = e.inputBuffer.getChannelData(0);
          
          const buffer = new ArrayBuffer(inputData.length * 2);
          const outputView = new DataView(buffer);
          for (let i = 0; i < inputData.length; i++) {
              let s = Math.max(-1, Math.min(1, inputData[i]));
              s = s < 0 ? s * 0x8000 : s * 0x7FFF;
              outputView.setInt16(i * 2, s, true);
          }
          ws.send(buffer);
      };

      mediaRecorderRef.current = { stream, audioContext, processor, source };
  };

  const stopRecording = () => {
      if (wsRef.current) {
          if (wsRef.current.readyState === WebSocket.OPEN) {
             wsRef.current.send("STOP");
             // Close after a short delay to allow final results
             setTimeout(() => {
                 wsRef.current?.close();
             }, 500);
          } else {
             wsRef.current.close();
          }
      }
      
      if (mediaRecorderRef.current) {
          const { stream, audioContext, processor, source } = mediaRecorderRef.current;
          stream.getTracks().forEach((track: any) => track.stop());
          processor.disconnect();
          source.disconnect();
          audioContext.close();
      }
      setIsRecording(false);
  };

  const toggleRecording = () => {
      if (isRecording) {
          stopRecording();
      } else {
          startRecording();
      }
  };

  const hasInteracted = messages.length > 0 || isThinking;

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isThinking]);

  // Load models on mount
  useEffect(() => {
      const fetchModels = async () => {
          try {
              const getBackendUrl = () => {
                  if (import.meta.env.DEV) return '/api/chat/models';
                  return `http://${window.location.hostname}:8000/api/chat/models`;
              };
              const res = await fetch(getBackendUrl());
              if (res.ok) {
                  const data = await res.json();
                  setModels(data);
                  if (data.length > 0) {
                      // Keep default if exists, else take first
                      const hasDefault = data.find((m: Model) => m.id === 'glm-4-flash');
                      if (!hasDefault) {
                          setSelectedModel(data[0].id);
                      }
                  }
              }
          } catch (e) {
              console.error("Fetch models failed", e);
          }
      };
      fetchModels();
  }, []);

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
            use_rag: isRagEnabled,
            use_search: isWebSearchEnabled,
            model: selectedModel
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
                        总裁，您好！<br />水华精灵已就绪， 请下达指令。
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
                  <div className="flex-1 p-4 glass-card rounded-[1.4rem] rounded-tl-none text-[14px] leading-relaxed text-slate-800 dark:text-slate-200 relative group font-light shadow-sm">
                    {(() => {
                        const content = msg.content || '';
                        const thinkStart = content.indexOf('<think>');
                        let thinkContent = null;
                        let mainContent = content;

                        if (thinkStart !== -1) {
                            const thinkEnd = content.indexOf('</think>');
                            if (thinkEnd !== -1) {
                                thinkContent = content.substring(thinkStart + 7, thinkEnd);
                                mainContent = content.substring(thinkEnd + 8);
                            } else {
                                thinkContent = content.substring(thinkStart + 7);
                                mainContent = ''; 
                            }
                        }

                        return (
                           <>
                                {thinkContent && <ThinkingProcess content={thinkContent} />}
                                {mainContent ? (
                                    <ReactMarkdown 
                                        remarkPlugins={[remarkGfm]}
                                        components={{
                                            p: ({node, ...props}) => <p className="mb-2 last:mb-0" {...props} />,
                                            ul: ({node, ...props}) => <ul className="list-disc list-inside mb-2" {...props} />,
                                            ol: ({node, ...props}) => <ol className="list-decimal list-inside mb-2" {...props} />,
                                            li: ({node, ...props}) => <li className="mb-1" {...props} />,
                                            a: ({node, ...props}) => <a className="text-blue-500 hover:underline" {...props} />,
                                            blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-slate-300 pl-4 italic my-2" {...props} />,
                                            code: ({node, inline, className, children, ...props}: any) => {
                                                const match = /language-(\w+)/.exec(className || '');
                                                return !inline ? (
                                                    <div className="bg-slate-900 text-slate-100 rounded-md p-3 my-2 overflow-x-auto text-xs font-mono">
                                                        <code className={className} {...props}>
                                                            {children}
                                                        </code>
                                                    </div>
                                                ) : (
                                                    <code className="bg-slate-200 dark:bg-slate-700 px-1.5 py-0.5 rounded text-xs font-mono" {...props}>
                                                        {children}
                                                    </code>
                                                )
                                            }
                                        }}
                                    >
                                        {mainContent}
                                    </ReactMarkdown>
                                ) : (
                                    !thinkContent && <span className="animate-pulse">Thinking...</span>
                                )}
                           </>
                        );
                    })()}
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
            <div className="relative glass-card bg-white/95 dark:bg-black/70 backdrop-blur-3xl rounded-[2rem] border-slate-200 dark:border-white/10 p-4 shadow-2xl flex flex-col gap-3">
                
                {/* Input Area */}
                <div className="flex items-start w-full">
                     <textarea
                        value={inputValue}
                        disabled={isThinking}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleSend();
                            }
                        }}
                        placeholder={isThinking ? "思维推演中..." : "输入您的战略指令..."}
                        className="w-full bg-transparent border-none focus:outline-none text-[14px] text-slate-800 dark:text-white placeholder:text-slate-300 dark:placeholder:text-slate-700 font-light resize-none h-[48px] max-h-[120px]"
                    />
                </div>

                {/* Toolbar */}
                <div className="flex items-center justify-between pt-2 border-t border-slate-100 dark:border-white/5">
                    <div className="flex items-center gap-2">
                        {/* Brain Icon (Status) */}
                        <div className="text-slate-400 dark:text-slate-600 mr-1">
                            <Brain size={16} className={isThinking ? 'animate-pulse text-blue-600 dark:text-blue-400' : ''} />
                        </div>

                        {/* Mic Button */}
                        <button
                            onClick={toggleRecording}
                            className={`w-7 h-7 rounded-full flex items-center justify-center transition-all mr-1 ${
                            isRecording 
                            ? 'bg-red-500 text-white animate-pulse shadow-lg glow-red' 
                            : 'text-slate-400 dark:text-slate-600 hover:text-blue-500 dark:hover:text-blue-400 hover:bg-slate-100 dark:hover:bg-white/5'
                            }`}
                            title={isRecording ? "停止录音" : "开始录音"}
                        >
                            {isRecording ? <MicOff size={14} /> : <Mic size={14} />}
                        </button>

                        {/* RAG Toggle */}
                        <button
                            onClick={() => setIsRagEnabled(!isRagEnabled)}
                            className={`px-3 py-1.5 rounded-full flex items-center gap-1.5 transition-all text-[10px] font-bold uppercase tracking-wider ${
                            isRagEnabled 
                            ? 'bg-blue-600/10 text-blue-600 border border-blue-600/20' 
                            : 'bg-slate-100 dark:bg-white/5 text-slate-400 dark:text-slate-600 hover:bg-slate-200 dark:hover:bg-white/10'
                            }`}
                        >
                            <Database size={12} />
                            {isRagEnabled ? 'RAG ON' : 'RAG OFF'}
                        </button>

                        {/* Web Search Toggle */}
                        <button
                            onClick={() => setIsWebSearchEnabled(!isWebSearchEnabled)}
                            className={`px-3 py-1.5 rounded-full flex items-center gap-1.5 transition-all text-[10px] font-bold uppercase tracking-wider ${
                            isWebSearchEnabled 
                            ? 'bg-blue-600/10 text-blue-600 border border-blue-600/20' 
                            : 'bg-slate-100 dark:bg-white/5 text-slate-400 dark:text-slate-600 hover:bg-slate-200 dark:hover:bg-white/10'
                            }`}
                        >
                            <Globe size={12} />
                            {isWebSearchEnabled ? 'WEB ON' : 'WEB OFF'}
                        </button>

                        {/* Model Selector */}
                        <select
                            value={selectedModel}
                            onChange={(e) => setSelectedModel(e.target.value)}
                            className="px-2 py-1.5 rounded-full bg-slate-100 dark:bg-white/5 text-slate-500 dark:text-slate-400 text-[10px] font-bold uppercase tracking-wider border-none outline-none hover:bg-slate-200 dark:hover:bg-white/10 transition-all cursor-pointer appearance-none"
                            style={{ WebkitAppearance: 'none', MozAppearance: 'none' }}
                        >
                            {models.map(m => (
                                <option key={m.id} value={m.id}>
                                    {m.name}
                                </option>
                            ))}
                            {models.length === 0 && <option value="glm-4-flash">GLM-4-Flash</option>}
                        </select>
                    </div>

                    {/* Send Button */}
                    <button
                        onClick={() => handleSend()}       
                        disabled={isThinking || !inputValue.trim()}
                        className={`w-9 h-9 rounded-full flex items-center justify-center text-white active:scale-90 transition-all ${
                        isThinking || !inputValue.trim() ? 'bg-slate-100 dark:bg-white/5 text-slate-300 dark:text-slate-800' : 'bg-blue-600 shadow-lg glow-blue'       
                        }`}
                    >
                        <Send size={14} />
                    </button>
                </div>
            </div>
        </div>
      </div>
    </div>
  );
};

export default ChatView;






