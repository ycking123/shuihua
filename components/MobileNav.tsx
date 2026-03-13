import React, { useEffect, useState } from 'react';
import { LayoutDashboard, MessageSquare, CalendarDays, CheckSquare, User } from 'lucide-react';
import { ViewType } from '../types';

interface MobileNavProps {
  activeView: ViewType;
  setActiveView: (view: ViewType) => void;
  hidden?: boolean;
}

const getBaseUrl = () => (import.meta.env.DEV ? '/api' : `http://${window.location.hostname}:8000/api`);
const getHeaders = (): Record<string, string> => {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  const token = localStorage.getItem('token');
  if (token) headers.Authorization = `Bearer ${token}`;
  return headers;
};

const MobileNav: React.FC<MobileNavProps> = ({ activeView, setActiveView, hidden = false }) => {
  const [pendingCount, setPendingCount] = useState(0);

  useEffect(() => {
    let ignore = false;
    const fetchPending = async () => {
      try {
        const response = await fetch(`${getBaseUrl()}/todos`, { headers: getHeaders() });
        const data = await response.json();
        if (!ignore && Array.isArray(data)) {
          setPendingCount(data.filter((item: any) => item?.status !== 'completed').length);
        }
      } catch (error) {
        console.error(error);
        if (!ignore) setPendingCount(0);
      }
    };

    fetchPending();
    const timer = window.setInterval(fetchPending, 15000);
    return () => {
      ignore = true;
      window.clearInterval(timer);
    };
  }, []);

  const mobileTabs = [
    { id: ViewType.MEETING, icon: CalendarDays, label: '会议' },
    { id: ViewType.DASHBOARD, icon: LayoutDashboard, label: '驾驶舱' },
    { id: ViewType.CHAT, icon: MessageSquare, label: 'AI智囊' },
    { id: ViewType.TODO, icon: CheckSquare, label: '待办事项', badge: pendingCount > 0 },
    { id: ViewType.SETTINGS, icon: User, label: '个人' }
  ];

  return (
    <div className={`fixed bottom-8 left-6 right-6 z-[100] animate-in slide-in-from-bottom-10 duration-700 transition-all ${hidden ? 'translate-y-24 opacity-0 pointer-events-none' : 'translate-y-0 opacity-100'}`}>
      <div className="glass-card rounded-[2.2rem] px-3 py-3 border-slate-200/60 dark:border-white/10 shadow-[0_20px_50px_-12px_rgba(0,0,0,0.1)] dark:shadow-[0_20px_50px_-12px_rgba(0,0,0,0.5)] flex items-center justify-between bg-white/90 dark:bg-black/80 transition-all">
        {mobileTabs.map((tab) => {
          const isActive = activeView === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveView(tab.id as ViewType)}
              className={`flex flex-col items-center gap-1.5 px-2 py-2 rounded-2xl transition-all duration-500 relative flex-1 ${isActive ? 'text-blue-600 dark:text-blue-400' : 'text-slate-400 dark:text-slate-600'}`}
            >
              <div className="relative">
                <tab.icon size={19} className={`transition-transform duration-300 ${isActive ? 'scale-110 drop-shadow-[0_0_8px_rgba(37,99,235,0.3)]' : 'scale-100'}`} />
                {tab.badge && (
                  <span className="absolute -top-1 -right-1 min-w-[14px] h-[14px] px-1 rounded-full bg-red-500 border-2 border-white dark:border-black shadow-sm text-[8px] leading-[10px] font-bold text-white flex items-center justify-center">
                    {pendingCount > 9 ? '9+' : pendingCount}
                  </span>
                )}
              </div>
              <span className={`text-[7.5px] font-bold tracking-tighter uppercase transition-opacity whitespace-nowrap ${isActive ? 'opacity-100' : 'opacity-50'}`}>
                {tab.label}
              </span>
              {isActive && <div className="absolute -bottom-0.5 w-1 h-1 bg-blue-600 dark:bg-blue-500 rounded-full shadow-lg"></div>}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default MobileNav;
