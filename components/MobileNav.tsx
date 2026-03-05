
import React from 'react';
import { LayoutDashboard, MessageSquare, CheckSquare, User } from 'lucide-react';
import { ViewType } from '../types';
import { TODOS_DATA } from '../constants';

interface MobileNavProps {
  activeView: ViewType;
  setActiveView: (view: ViewType) => void;
}

const MobileNav: React.FC<MobileNavProps> = ({ activeView, setActiveView }) => {
  const pendingCount = TODOS_DATA.filter(t => t.status === 'pending').length;

  const mobileTabs = [
    { id: ViewType.DASHBOARD, icon: LayoutDashboard, label: '驾驶舱' },
    { id: ViewType.CHAT, icon: MessageSquare, label: 'AI智僚' },
    { id: ViewType.TODO, icon: CheckSquare, label: '待办事项', badge: pendingCount > 0 },
    { id: ViewType.SETTINGS, icon: User, label: '个人' },
  ];

  return (
    <div className="fixed bottom-8 left-6 right-6 z-[100] animate-in slide-in-from-bottom-10 duration-700">
      <div className="glass-card rounded-[2.2rem] px-3 py-3 border-slate-200/60 dark:border-white/10 shadow-[0_20px_50px_-12px_rgba(0,0,0,0.1)] dark:shadow-[0_20px_50px_-12px_rgba(0,0,0,0.5)] flex items-center justify-between backdrop-blur-3xl bg-white/70 dark:bg-black/60 transition-all">
        {mobileTabs.map((tab) => {
          const isActive = activeView === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveView(tab.id as ViewType)}
              className={`flex flex-col items-center gap-1.5 px-2 py-2 rounded-2xl transition-all duration-500 relative flex-1 ${
                isActive ? 'text-blue-600 dark:text-blue-400' : 'text-slate-400 dark:text-slate-600'
              }`}
            >
              <div className="relative">
                <tab.icon size={19} className={`transition-transform duration-300 ${isActive ? 'scale-110 drop-shadow-[0_0_8px_rgba(37,99,235,0.3)]' : 'scale-100'}`} />
                {tab.badge && (
                  <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-white dark:border-black animate-pulse shadow-sm"></span>
                )}
              </div>
              <span className={`text-[7.5px] font-bold tracking-tighter uppercase transition-opacity whitespace-nowrap ${isActive ? 'opacity-100' : 'opacity-50'}`}>
                {tab.label}
              </span>
              {isActive && (
                <div className="absolute -bottom-0.5 w-1 h-1 bg-blue-600 dark:bg-blue-500 rounded-full shadow-lg"></div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default MobileNav;
