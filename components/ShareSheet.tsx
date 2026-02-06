
import React, { useState } from 'react';
import { 
  X, Share2, FileText, 
  Copy, Database, Zap, 
  ExternalLink, CheckCircle2, Loader2,
  Lock
} from 'lucide-react';

interface ShareOption {
  id: string;
  name: string;
  desc: string;
  icon: any;
  color: string;
}

const SHARE_OPTIONS: ShareOption[] = [
  { 
    id: 'external_app', 
    name: '同步至协作应用', 
    desc: '调用系统原生分发链路，即时推送至企业微信、钉钉等平台', 
    icon: Share2, 
    color: 'blue' 
  },
  { 
    id: 'pdf', 
    name: '生成加密报告文档', 
    desc: '导出具备动态水印的专家级深度分析简报', 
    icon: FileText, 
    color: 'purple' 
  },
  { 
    id: 'link', 
    name: '复制阅后即焚链接', 
    desc: '生成具备 5 分钟限时访问权限的安全凭证', 
    icon: Copy, 
    color: 'orange' 
  },
];

interface ShareSheetProps {
  isOpen: boolean;
  onClose: () => void;
  data: { title: string; type: string; content?: string };
}

const ShareSheet: React.FC<ShareSheetProps> = ({ isOpen, onClose, data }) => {
  const [status, setStatus] = useState<'idle' | 'processing' | 'success'>('idle');

  const handleShare = (optionId: string) => {
    setStatus('processing');
    setTimeout(() => {
      setStatus('success');
      setTimeout(() => {
        setStatus('idle');
        onClose();
      }, 1500);
    }, 2000);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[200] flex items-end justify-center px-4 pb-8 animate-in fade-in duration-300">
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" onClick={onClose}></div>
      <div className="w-full max-w-md glass-card rounded-[2.5rem] border-white/10 p-6 z-10 animate-in slide-in-from-bottom-8 duration-500 relative overflow-hidden">
        <div className="absolute -top-24 -left-24 w-48 h-48 bg-blue-600/10 blur-[60px] rounded-full"></div>
        
        {status === 'idle' ? (
          <>
            <div className="flex items-center justify-between mb-8">
              <div className="flex items-center gap-3">
                <div className="p-2.5 bg-blue-500/10 rounded-xl border border-blue-500/20">
                  <Share2 size={18} className="text-blue-400" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white uppercase tracking-tight">战略信息分发</h3>
                  <p className="text-[9px] text-slate-500 uppercase tracking-widest font-mono">EXTERNAL_ASSET_ALLOCATION</p>
                </div>
              </div>
              {/* Fix: Changed onClose to onClick which is a valid attribute for HTML button elements */}
              <button onClick={onClose} className="p-2 text-slate-500 hover:text-white transition-colors">
                <X size={18} />
              </button>
            </div>

            <div className="mb-6 p-4 bg-white/[0.02] border border-white/5 rounded-2xl">
                <div className="flex items-center gap-2 mb-1">
                    <Lock size={10} className="text-slate-600" />
                    <span className="text-[8px] text-slate-600 font-bold uppercase tracking-widest">LOAD_SUMMARY_PREVIEW</span>
                </div>
                <div className="text-[13px] text-blue-400 font-bold truncate uppercase">{data.title}</div>
                <div className="text-[10px] text-slate-500 mt-1 uppercase font-mono tracking-tighter">PAYLOAD: {data.type}-ENC-PRO</div>
            </div>

            <div className="space-y-3">
              {SHARE_OPTIONS.map((option) => (
                <div 
                  key={option.id}
                  onClick={() => handleShare(option.id)}
                  className="p-4 rounded-[1.8rem] border border-white/5 bg-white/[0.01] hover:bg-white/[0.04] transition-all cursor-pointer flex items-center gap-4 group active:scale-[0.98]"
                >
                  <div className={`w-10 h-10 rounded-2xl flex items-center justify-center shrink-0 bg-${option.color}-500/10 text-${option.color}-400 group-hover:scale-110 transition-transform`}>
                    <option.icon size={20} />
                  </div>
                  <div className="flex-1">
                    <span className="text-sm font-bold text-slate-200 group-hover:text-white transition-colors uppercase">
                      {option.name}
                    </span>
                    <p className="text-[11px] text-slate-500 mt-0.5 font-light">
                      {option.desc}
                    </p>
                  </div>
                  <ExternalLink size={14} className="text-slate-800 group-hover:text-slate-400 transition-colors" />
                </div>
              ))}
            </div>
          </>
        ) : (
          <div className="h-[400px] flex flex-col items-center justify-center text-center">
            {status === 'processing' ? (
              <div className="space-y-6 flex flex-col items-center">
                <div className="relative">
                    <div className="absolute inset-0 bg-blue-500/20 blur-xl rounded-full"></div>
                    <Loader2 size={48} className="text-blue-500 animate-spin relative" />
                </div>
                <div className="space-y-2">
                    <h3 className="text-lg font-bold text-white uppercase tracking-widest">ESTABLISHING_LINK</h3>
                    <p className="text-xs text-slate-500 font-mono italic">正在与目标接收端进行安全握手...</p>
                </div>
                <div className="flex items-center gap-2 text-[9px] text-blue-400/50 font-mono animate-pulse uppercase">
                    <Zap size={10} /> BITSTREAM_SYNCING
                </div>
              </div>
            ) : (
              <div className="space-y-6 flex flex-col items-center animate-in zoom-in-95 duration-500">
                <div className="w-16 h-16 bg-emerald-500/20 rounded-full flex items-center justify-center text-emerald-400 shadow-[0_0_30px_rgba(16,185,129,0.3)] border border-emerald-500/30">
                    <CheckCircle2 size={32} />
                </div>
                <div className="space-y-2">
                    <h3 className="text-lg font-bold text-white uppercase tracking-widest">TASK_COMPLETE</h3>
                    <p className="text-xs text-slate-500 uppercase tracking-tighter">Information payload successfully delivered.</p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ShareSheet;
