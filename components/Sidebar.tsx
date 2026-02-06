
import React from 'react';
import { BrainCircuit, ChevronRight } from 'lucide-react';
import { ViewType } from '../types';
import { MENU_ITEMS, TODOS_DATA } from '../constants';

interface SidebarProps {
  activeView: ViewType;
  setActiveView: (view: ViewType) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeView, setActiveView }) => {
  // Fix: Calculate pending count for sidebar badges locally from TODOS_DATA
  const pendingCount = TODOS_DATA.filter(t => t.status === 'pending').length;

  return (
    <div className="w-64 bg-[#000000] h-screen flex flex-col text-white fixed left-0 top-0 z-50 border-r border-white/10 shadow-2xl">
      <div className="h-20 flex items-center gap-3 px-6 border-b border-white/5">
        <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-600/30">
          <BrainCircuit size={24} className="text-white" />
        </div>
        <div className="flex flex-col">
          <span className="font-bold text-xl tracking-wider text-white">掌上指挥</span>
          <span className="text-[10px] tracking-[0.2em] text-blue-400 -mt-1 font-bold">POCKET COMMAND</span>
        </div>
      </div>

      <nav className="flex-1 p-4 space-y-2 mt-4">
        {MENU_ITEMS.map((item) => {
          const badge = item.id === ViewType.TODO && pendingCount > 0 ? pendingCount : null;
          
          return (
            <button
              key={item.id}
              onClick={() => setActiveView(item.id as ViewType)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 group relative ${
                activeView === item.id
                  ? 'bg-blue-600 shadow-[0_0_20px_rgba(37,99,235,0.4)] text-white'
                  : 'text-slate-400 hover:bg-white/5 hover:text-white'
              }`}
            >
              <item.icon size={20} className={activeView === item.id ? 'animate-pulse' : ''} />
              <span className="font-bold text-base">{item.label}</span>
              {badge && (
                <span className="absolute right-4 bg-red-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full ring-2 ring-black">
                  {badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      <div className="p-4 border-t border-white/10 bg-white/5 backdrop-blur-md">
        <div className="flex items-center gap-3 px-2 py-2 rounded-lg hover:bg-white/5 transition-colors cursor-pointer group">
          <div className="w-11 h-11 rounded-full bg-gradient-to-tr from-purple-500 to-blue-500 border-2 border-white/20 relative shadow-lg">
            <span className="absolute bottom-0 right-0 w-3 h-3 bg-emerald-500 border-2 border-black rounded-full"></span>
          </div>
          <div>
            <div className="text-base font-bold text-white group-hover:text-blue-400 transition-colors">朱江</div>
            <div className="text-[11px] text-slate-400 font-bold tracking-tight">集团董事长</div>
          </div>
          <ChevronRight size={14} className="text-slate-600 ml-auto group-hover:text-white transition-all group-hover:translate-x-1" />
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
