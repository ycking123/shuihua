
import React, { useState, useEffect } from 'react';
import MobileNav from './components/MobileNav';
import Dashboard from './components/Dashboard';
import ChatView from './components/ChatView';
import TodoView from './components/TodoView';
import PersonalView from './components/PersonalView';
import ArchitectureCanvas from './components/ArchitectureCanvas';
import LoginView from './components/LoginView';
import { ViewType } from './types';
import { User } from 'lucide-react';

const App: React.FC = () => {
  const [activeView, setActiveView] = useState<ViewType>(ViewType.LOGIN);
  const [chatContext, setChatContext] = useState<string | null>(null);
  const [showDevMode, setShowDevMode] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check for token on mount
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
      setActiveView(ViewType.DASHBOARD);
    } else {
      setIsAuthenticated(false);
      setActiveView(ViewType.LOGIN);
    }
  }, []);

  const handleNavigate = (view: ViewType, context?: string) => {
    if (context) {
      setChatContext(context);
    }
    setActiveView(view);
  };

  const handleLoginSuccess = (token: string, username: string) => {
    localStorage.setItem('token', token);
    localStorage.setItem('username', username);
    setIsAuthenticated(true);
    setActiveView(ViewType.DASHBOARD);
  };
  
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setIsAuthenticated(false);
    setActiveView(ViewType.LOGIN);
  };

  // If showing Login View (special case without layout)
  if (activeView === ViewType.LOGIN) {
      return <LoginView onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="flex flex-col h-screen bg-slate-50 dark:bg-black font-sans antialiased text-slate-900 dark:text-white overflow-hidden relative transition-colors duration-500">
      {/* 顶部状态栏 */}
      <header className="shrink-0 h-14 flex items-center justify-between px-6 z-[60] bg-white/70 dark:bg-black/40 backdrop-blur-md border-b border-slate-200 dark:border-white/5 transition-colors">
        <div className="flex flex-col">
          <span className="font-bold text-base tracking-widest text-slate-900 dark:text-white leading-tight">水华精灵</span>
          <span className="text-[10px] tracking-[0.2em] text-slate-400 dark:text-slate-500 font-bold uppercase">STRATEGIC INSIGHT HUB V4</span>
        </div>
        <div className="flex items-center gap-4">
          <div 
            onClick={() => handleNavigate(ViewType.SETTINGS)}
            className="w-9 h-9 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-700 border border-white/20 flex items-center justify-center cursor-pointer shadow-lg active:scale-90 transition-transform"
          >
            <User size={16} className="text-white" />
          </div>
          <button onClick={handleLogout} className="text-xs text-slate-500 hover:text-slate-800 dark:hover:text-slate-300">
             退出
          </button>
        </div>
      </header>

      {/* 主内容区域 */}
      <main className="flex-1 overflow-hidden relative">
        <div className={`absolute inset-0 transition-opacity duration-300 overflow-y-auto pb-32 no-scrollbar ${activeView === ViewType.DASHBOARD ? 'opacity-100 z-10' : 'opacity-0 -z-10 pointer-events-none'}`}>
          <Dashboard onNavigate={handleNavigate} />
        </div>
        
        <div className={`absolute inset-0 transition-opacity duration-300 ${activeView === ViewType.CHAT ? 'opacity-100 z-10' : 'opacity-0 -z-10 pointer-events-none'}`}>
          <ChatView 
            initialContext={chatContext} 
            onClearContext={() => setChatContext(null)} 
          />
        </div>

        <div className={`absolute inset-0 transition-opacity duration-300 ${activeView === ViewType.TODO ? 'opacity-100 z-10' : 'opacity-0 -z-10 pointer-events-none'}`}>
          <TodoView onNavigate={handleNavigate} />
        </div>

        {activeView === ViewType.SETTINGS && <PersonalView />}
      </main>

      {/* 系统架构监控 */}
      {showDevMode && <ArchitectureCanvas onClose={() => setShowDevMode(false)} />}

      {/* 底部导航 */}
      <MobileNav activeView={activeView} setActiveView={handleNavigate} />
    </div>
  );
};

export default App;

