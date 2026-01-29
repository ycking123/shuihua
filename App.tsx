
import React, { useState } from 'react';
import MobileNav from './components/MobileNav';
import Dashboard from './components/Dashboard';
import ChatView from './components/ChatView';
import TodoView from './components/TodoView';
import PersonalView from './components/PersonalView';
import ArchitectureCanvas from './components/ArchitectureCanvas';
import { ViewType } from './types';
import { User } from 'lucide-react';

const App: React.FC = () => {
  const [activeView, setActiveView] = useState<ViewType>(ViewType.DASHBOARD);
  const [chatContext, setChatContext] = useState<string | null>(null);
  const [showDevMode, setShowDevMode] = useState(false);

  const handleNavigate = (view: ViewType, context?: string) => {
    if (context) {
      setChatContext(context);
    }
    setActiveView(view);
  };

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
        </div>
      </header>

      {/* 主内容区域 */}
      <main className="flex-1 overflow-y-auto pb-32 no-scrollbar scroll-smooth">
        {activeView === ViewType.DASHBOARD && <Dashboard onNavigate={handleNavigate} />}
        {activeView === ViewType.CHAT && (
          <ChatView 
            initialContext={chatContext} 
            onClearContext={() => setChatContext(null)} 
          />
        )}
        {activeView === ViewType.TODO && <TodoView onNavigate={handleNavigate} />}
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
