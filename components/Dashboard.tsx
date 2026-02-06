
import React, { useState, useMemo } from 'react';
import { Sparkles, Wallet, ChevronRight, Target, Radar, Box, Cpu, Zap, Gem, ReceiptText, PieChart, Info, Building2, TrendingUp, Share2, Globe, Brain, ChevronDown, ChevronUp, Users, Activity, GraduationCap, Network, FlaskConical, ArrowRight } from 'lucide-react';
import { ViewType } from '../types';
import ShareSheet from './ShareSheet';

// 市场态势背景组件 - 优化为自适应
const MarketSentimentBackground: React.FC<{ sentiment: 'positive' | 'negative' | 'neutral' }> = ({ sentiment }) => {
  const config = {
    positive: {
      color: 'rgba(16, 185, 129, 0.1)', // 翠绿色
      secondary: 'rgba(59, 130, 246, 0.08)', // 蓝色
      animation: 'animate-pulse-slow'
    },
    negative: {
      color: 'rgba(239, 68, 68, 0.1)', // 红色
      secondary: 'rgba(139, 92, 246, 0.08)', // 紫色
      animation: 'animate-pulse-fast'
    },
    neutral: {
      color: 'rgba(148, 163, 184, 0.08)', // 灰色
      secondary: 'rgba(0, 0, 0, 0)',
      animation: 'animate-breathe'
    }
  }[sentiment];

  return (
    <div className="fixed inset-0 pointer-events-none z-[-1] overflow-hidden opacity-60 dark:opacity-100">
      <div 
        className={`absolute -top-[20%] -left-[10%] w-[70%] h-[70%] rounded-full blur-[120px] transition-colors duration-2000 ease-in-out ${config.animation}`}
        style={{ backgroundColor: config.color }}
      />
      <div 
        className={`absolute -bottom-[10%] -right-[5%] w-[60%] h-[60%] rounded-full blur-[100px] transition-colors duration-2000 ease-in-out delay-1000 ${config.animation}`}
        style={{ backgroundColor: config.secondary }}
      />
      <div className="absolute inset-0 opacity-20 dark:opacity-40">
        <div className={`absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_0%,white_100%)] dark:bg-[radial-gradient(circle_at_center,transparent_0%,black_100%)]`} />
      </div>
    </div>
  );
};

const TopologySphereIcon: React.FC<{ color: string; onClick: (e: React.MouseEvent) => void; label?: string }> = ({ color, onClick, label = "智僚深度推演" }) => {
  const themeColorMap: Record<string, string> = {
    blue: '#3b82f6',
    emerald: '#10b981',
    purple: '#8b5cf6',
    orange: '#f59e0b',
    red: '#ef4444',
    cyan: '#06b6d4',
    indigo: '#6366f1'
  };
  const glowColor = themeColorMap[color] || themeColorMap.blue;

  return (
    <button 
      onClick={onClick}
      className="flex items-center gap-2 px-3 py-2 rounded-xl bg-slate-100 dark:bg-white/5 border border-slate-200 dark:border-white/10 hover:bg-slate-200 dark:hover:bg-white/10 hover:border-blue-500/50 transition-all active:scale-95 group/sphere shadow-sm"
    >
      <div className="relative w-4 h-4 flex items-center justify-center">
        <div className="absolute inset-0 bg-blue-500/10 dark:bg-blue-500/20 blur-md rounded-full group-hover/sphere:bg-blue-500/30 transition-all"></div>
        <Brain 
          size={10} 
          className="relative z-10 group-hover/sphere:scale-110 transition-transform" 
          style={{ color: glowColor }}
        />
      </div>
      <span className="text-[8px] font-bold text-slate-500 dark:text-slate-300 uppercase tracking-widest">{label}</span>
    </button>
  );
};

const ClusterItem: React.FC<{
  name: string;
  revenue: string;
  progress: number;
  icon: any;
  color: string;
  trend: string;
  isExpanded: boolean;
  onToggle: () => void;
  onNavigate: (v: ViewType, ctx?: string) => void;
  breakdown: any[];
  isSpecial?: boolean;
}> = ({ name, revenue, progress, icon: Icon, color, trend, isExpanded, onToggle, onNavigate, breakdown, isSpecial }) => (
  <div 
    className={`w-full glass-card rounded-[1.8rem] flex flex-col relative overflow-hidden transition-all duration-300 ${isExpanded ? 'ring-1 ring-blue-500/30 z-20 shadow-2xl absolute inset-x-2 top-0' : 'h-[140px] shadow-sm'}`}
  >
    <div className="p-3.5 flex flex-col justify-between h-full" onClick={onToggle}>
      <div className="flex justify-between items-start z-10">
        <div className={`p-2 rounded-xl bg-${color}-500/10 dark:bg-${color}-500/20 text-${color}-600 dark:text-${color}-400 shadow-sm border border-${color}-500/10 ${isSpecial ? 'animate-pulse' : ''}`}>
          <Icon size={16} />
        </div>
        <div className="flex flex-col items-end gap-1">
          {isSpecial && <span className="text-[7px] px-1 py-0.5 rounded bg-indigo-500/10 text-indigo-500 font-bold tracking-widest uppercase">增量</span>}
          <span className="text-[10px] font-mono text-emerald-600 dark:text-emerald-400 font-bold">{trend}</span>
        </div>
      </div>
      <div className="z-10 mt-1">
        <div className="flex items-center justify-between mb-1">
          <span className="text-[10px] text-slate-500 dark:text-slate-400 font-bold tracking-tight truncate">{name}</span>
        </div>
        <div className="text-xl font-mono-prec font-bold text-slate-900 dark:text-white tracking-tighter mb-1.5">{revenue}</div>
        <div className="h-1 w-full bg-slate-200 dark:bg-white/10 rounded-full overflow-hidden">
          <div className={`h-full bg-${color}-500 shadow-[0_0_8px_rgba(59,130,246,0.3)] transition-all duration-1000`} style={{ width: `${progress}%` }}></div>
        </div>
        <div className="flex justify-between mt-1 items-center">
          <span className="text-[8px] text-slate-400 dark:text-slate-500 font-bold uppercase tracking-wider">达成 {progress}%</span>
          {isExpanded ? <ChevronUp size={10} className="text-slate-400" /> : <ChevronDown size={10} className="text-slate-300" />}
        </div>
      </div>
    </div>
    
    {isExpanded && (
      <div className="px-4 pb-4 animate-in fade-in slide-in-from-top-2 duration-300 bg-white/10 dark:bg-black/40">
        <div className="h-px bg-slate-200 dark:bg-white/5 mb-3"></div>
        <div className="space-y-2">
          {breakdown.slice(0, 3).map((item, idx) => (
            <div key={idx} className="flex justify-between items-center px-1">
              <span className="text-[9px] text-slate-500 dark:text-slate-400 font-medium">{item.label}</span>
              <span className="text-[9px] font-mono text-slate-700 dark:text-slate-200 font-bold">{item.value}</span>
            </div>
          ))}
          <div className="pt-2 flex justify-center">
            <TopologySphereIcon 
              color={color} 
              onClick={(e) => {
                e.stopPropagation();
                onNavigate(ViewType.CHAT, `请深度剖析【${name}】的营收数据。核心业务线：${breakdown.map(b => b.label).join('、')}。当前总营收 ${revenue}，达成率 ${progress}%。请给出具体的增长点优化建议。`);
              }} 
            />
          </div>
        </div>
      </div>
    )}
  </div>
);

const CostCard: React.FC<{
  name: string;
  cost: string;
  breakdown: { label: string; value: string }[];
  color: string;
  isExpanded: boolean;
  onToggle: () => void;
  onNavigate: (v: ViewType, ctx?: string) => void;
}> = ({ name, cost, breakdown, color, isExpanded, onToggle, onNavigate }) => (
  <div 
    className={`w-full glass-card rounded-[1.8rem] flex flex-col relative overflow-hidden transition-all duration-300 ${isExpanded ? 'ring-1 ring-red-500/30 z-20 shadow-2xl absolute inset-x-2 top-0' : 'h-[140px] shadow-sm'}`}
  >
    <div className="p-3.5 flex flex-col justify-between h-full" onClick={onToggle}>
      <div className="z-10 h-full flex flex-col justify-between">
        <div className="flex justify-between items-start">
          <div className="flex items-center gap-1.5">
            <ReceiptText size={12} className={`text-red-500 dark:text-red-400`} />
            <span className="text-[10px] text-slate-500 dark:text-slate-400 font-bold tracking-tight truncate">{name}成本</span>
          </div>
          {isExpanded ? <ChevronUp size={10} className="text-slate-400" /> : <ChevronDown size={10} className="text-slate-300" />}
        </div>
        <div className="text-xl font-mono-prec font-bold text-red-600 dark:text-red-500 tracking-tighter mb-1.5">{cost}</div>
        <div className="space-y-1">
          <div className="flex justify-between items-center text-[9px] text-slate-400 uppercase tracking-tighter mb-0.5">
            <span>核心成本构成</span>
          </div>
          <div className="h-px bg-red-500/10 mb-1"></div>
          {breakdown.slice(0, 2).map((item, idx) => (
            <div key={idx} className="flex justify-between items-center border-b border-slate-100 dark:border-white/[0.03] pb-1">
              <span className="text-[9px] text-slate-500 dark:text-slate-400 truncate pr-2 font-medium">经营投入-{idx+1}</span>
              <span className="text-[9px] font-mono font-bold text-slate-700 dark:text-slate-300">{item.value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
    {isExpanded && (
      <div className="px-4 pb-4 animate-in fade-in slide-in-from-top-2 duration-300 bg-red-500/5 dark:bg-red-500/10">
        <div className="h-px bg-red-500/10 mb-3"></div>
        <div className="pt-2 flex justify-center">
          <TopologySphereIcon 
            color="red" 
            label="降本增效推演"
            onClick={(e) => {
              e.stopPropagation();
              onNavigate(ViewType.CHAT, `请深度剖析【${name}】的成本构成。当前总成本 ${cost}。请分析其中的主要支出点并给出降本增效建议。`);
            }} 
          />
        </div>
      </div>
    )}
  </div>
);

const OrgMetricCard: React.FC<{
  label: string;
  value: string;
  trend: string;
  icon: any;
  color: string;
  logic: string;
  isExpanded: boolean;
  onToggle: () => void;
  onNavigate: (v: ViewType, ctx?: string) => void;
}> = ({ label, value, trend, icon: Icon, color, logic, isExpanded, onToggle, onNavigate }) => (
  <div 
    className={`shrink-0 w-[280px] snap-center glass-card rounded-[2.5rem] bg-gradient-to-br from-${color}-500/5 dark:from-${color}-900/10 to-transparent flex flex-col relative overflow-hidden transition-all duration-500 ${isExpanded ? 'ring-1 ring-cyan-500/40 shadow-2xl' : 'h-[160px]'}`}
  >
    <div className="p-5 flex flex-col h-[160px] shrink-0" onClick={onToggle}>
      <div className="flex justify-between items-start mb-2">
        <div className={`p-3 rounded-2xl bg-${color}-500/10 dark:bg-${color}-500/20 text-${color}-600 dark:text-${color}-400 shadow-sm`}>
          <Icon size={18} />
        </div>
        <div className="flex flex-col items-end">
          <span className="text-[10px] font-mono text-emerald-600 dark:text-emerald-400 font-bold bg-emerald-500/5 px-1.5 py-0.5 rounded border border-emerald-500/10 dark:border-emerald-500/20">{trend}</span>
          <div className="mt-2 text-slate-400 dark:text-slate-600">
            {isExpanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
          </div>
        </div>
      </div>
      <div className="mt-auto">
        <div className="text-[10px] text-slate-500 font-bold uppercase tracking-[0.2em] mb-1">{label}</div>
        <div className="text-3xl font-mono-prec font-bold text-slate-900 dark:text-white tracking-tighter">{value}</div>
      </div>
    </div>

    {isExpanded && (
        <div className="px-6 pb-6 animate-in fade-in slide-in-from-top-2 duration-300">
            <div className="h-px bg-slate-200 dark:bg-white/10 mb-4"></div>
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-[9px] font-bold text-cyan-600 dark:text-cyan-400 uppercase tracking-widest">
                <Cpu size={10} /> 实时行为流监测逻辑
              </div>
              <p className="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed font-light italic bg-slate-50 dark:bg-white/5 p-3 rounded-2xl border border-slate-100 dark:border-white/5 shadow-inner">
                  {logic}
              </p>
              <div className="flex justify-center pt-2">
                  <TopologySphereIcon 
                    color={color} 
                    label="生成治理深度简报"
                    onClick={(e) => {
                      e.stopPropagation();
                      onNavigate(ViewType.CHAT, `请基于【${label}】的取数逻辑，分析当前 ${value} 数据背后的组织瓶颈。逻辑参考：${logic}`);
                    }} 
                  />
              </div>
            </div>
        </div>
    )}
  </div>
);

const InsightItem: React.FC<{ 
  item: any;
  isExpanded: boolean;
  onToggle: () => void;
  onNavigate: (v: ViewType, ctx?: string) => void;
}> = ({ item, isExpanded, onToggle, onNavigate }) => (
  <div 
    className={`flex flex-col rounded-[1.8rem] border transition-all duration-300 ${
      item.isUrgent ? 'bg-red-500/5 dark:bg-red-500/10 border-red-500/20 dark:border-red-500/30' : 'bg-slate-50/50 dark:bg-white/5 border-slate-200/50 dark:border-white/5 shadow-sm'
    } ${isExpanded ? 'ring-1 ring-blue-500/50 shadow-lg dark:shadow-2xl' : ''}`}
  >
    <div className="flex items-start gap-4 p-5 cursor-pointer" onClick={onToggle}>
      <div className={`p-3 rounded-2xl bg-${item.color}-500/10 dark:bg-${item.color}-500/20 text-${item.color}-600 dark:text-${item.color}-400 shrink-0 shadow-sm`}>
        <item.icon size={20} />
      </div>
      <div className="flex-1 min-w-0 pt-0.5">
        <div className={`text-[14px] font-medium text-slate-800 dark:text-slate-200 leading-relaxed mb-2 ${isExpanded ? '' : 'line-clamp-2'}`}>
          {item.text}
        </div>
        <div className="flex items-center gap-2">
          <span className="text-[10px] text-slate-500 font-bold tracking-widest uppercase">{item.subtext}</span>
          {item.isUrgent && <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-ping"></span>}
        </div>
      </div>
      <div className="flex flex-col items-center">
        {isExpanded ? <ChevronUp size={16} className="text-slate-400" /> : <ChevronDown size={16} className="text-slate-200 dark:text-slate-700" />}
      </div>
    </div>

    <div className={`overflow-hidden transition-all duration-500 ease-in-out ${isExpanded ? 'max-h-96 border-t border-slate-200 dark:border-white/5' : 'max-h-0'}`}>
      <div className="p-5 bg-slate-100/50 dark:bg-black/40 space-y-4 shadow-inner">
        <div className="flex items-center gap-2 text-[10px] font-bold text-blue-600 dark:text-blue-400 uppercase tracking-widest">
          <Globe size={12} /> 深度仿真推演背景 (DEEP SIMULATION)
        </div>
        <div className="pt-3 flex justify-center border-t border-slate-200 dark:border-white/5 mt-2">
          <TopologySphereIcon 
            color={item.color === 'orange' ? 'blue' : item.color} 
            label="启动全局推演"
            onClick={(e) => {
              e.stopPropagation();
              const context = `请针对以下洞察进行全局战略建模推演：\n\n【${item.subtext}】\n${item.text}`;
              onNavigate(ViewType.CHAT, context);
            }}
          />
        </div>
      </div>
    </div>
  </div>
);

const Dashboard: React.FC<{ onNavigate: (v: ViewType, ctx?: string) => void }> = ({ onNavigate }) => {
  const [shareConfig, setShareConfig] = useState<{ isOpen: boolean; data: any }>({ isOpen: false, data: {} });
  const [expandedInsightId, setExpandedInsightId] = useState<number | null>(null);
  const [expandedClusterId, setExpandedClusterId] = useState<string | null>(null);
  const [expandedOrgId, setExpandedOrgId] = useState<string | null>(null);
  const [activePageIndex, setActivePageIndex] = useState(0);
  
  const [liquidity, setLiquidity] = useState({ value: 8.2, trend: "-3.5%", status: "持续关注" });

  const marketSentiment = useMemo(() => {
    const trendVal = parseFloat(liquidity.trend.replace('%', ''));
    if (trendVal > 0.5) return 'positive';
    if (trendVal < -0.5) return 'negative';
    return 'neutral';
  }, [liquidity.trend]);

  // Page 1: 帝王, 欧神诺 - 营收明细重构（基于2025年真实预测数据）
  const pillarClusters = [
    { 
      id: 'c1', 
      name: "帝王卫浴", 
      revenue: "9.8 亿", 
      cost: "7.2 亿", 
      progress: 65, 
      icon: Box, 
      color: "blue", 
      trend: "-8.5%", 
      breakdown: [
        {label: "智能马桶", value: "3.2 亿"}, 
        {label: "浴室柜", value: "2.8 亿"}, 
        {label: "五金卫浴", value: "3.8 亿"}
      ] 
    },
    { 
      id: 'c2', 
      name: "欧神诺瓷砖", 
      revenue: "13.5 亿", 
      cost: "10.1 亿", 
      progress: 58, 
      icon: Gem, 
      color: "emerald", 
      trend: "-12.3%", 
      breakdown: [
        {label: "工程渠道", value: "6.2 亿"}, 
        {label: "零售渠道", value: "5.8 亿"}, 
        {label: "出口业务", value: "1.5 亿"}
      ] 
    },
  ];

  // Page 2: 智能制造, 新零售 - 营收明细重构
  const strategicClusters = [
    { 
      id: 'c3', 
      name: "智能制造升级", 
      revenue: "待转化", 
      cost: "1.8 亿", 
      progress: 35, 
      icon: Cpu, 
      color: "indigo", 
      trend: "筹建中", 
      isSpecial: true, 
      breakdown: [
        {label: "数字化产线改造", value: "0.8 亿"}, 
        {label: "智能仓储系统", value: "0.6 亿"}, 
        {label: "AI质检投入", value: "0.4 亿"}
      ] 
    },
    { 
      id: 'c4', 
      name: "新零售渠道", 
      revenue: "待突破", 
      cost: "1.2 亿", 
      progress: 28, 
      icon: FlaskConical, 
      color: "orange", 
      trend: "布局中", 
      isSpecial: true, 
      breakdown: [
        {label: "直播电商", value: "0.5 亿"}, 
        {label: "社区团购", value: "0.4 亿"}, 
        {label: "设计师渠道", value: "0.3 亿"}
      ] 
    },
  ];

  const orgMetrics = [
    { id: 'o1', label: "渠道数字化率", value: "42.8%", trend: "+8.5%", icon: Cpu, color: "indigo", logic: "实时监控全渠道数字化工具使用覆盖率。" },
    { id: 'o2', label: "经销商活跃度", value: "68", trend: "-5.2%", icon: Activity, color: "cyan", logic: "基于订单频次与回款周期综合评分。" },
    { id: 'o3', label: "产品研发投入", value: "3.2%", trend: "+0.5%", icon: GraduationCap, color: "blue", logic: "研发费用占营收比例，衡量创新投入强度。" },
  ];

  const insightItems = [
    { id: 1, icon: Target, color: "orange", isUrgent: true, text: "东鹏在2026年1月底的峰会上强调了“厂商协同”和“定制化胜出”。", subtext: "市场竞争态势深度分析" },
    { id: 2, icon: Building2, color: "blue", text: "保利等房企对精装供应商的要求已转向“AI+全案交付”。", subtext: "战略预研及技术对标建议" }
  ];

  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const scrollLeft = e.currentTarget.scrollLeft;
    const width = e.currentTarget.clientWidth;
    const newIndex = Math.round(scrollLeft / width);
    if (newIndex !== activePageIndex) setActivePageIndex(newIndex);
  };

  return (
    <div className="p-4 space-y-7 animate-in fade-in duration-700 bg-transparent relative">
      <MarketSentimentBackground sentiment={marketSentiment} />
      <ShareSheet isOpen={shareConfig.isOpen} onClose={() => setShareConfig({ ...shareConfig, isOpen: false })} data={shareConfig.data} />

      {/* 1. 流动性监控 */}
      <div className="relative glass-card rounded-[2.8rem] bg-gradient-to-br from-blue-100/50 to-white/80 dark:from-blue-900/20 dark:to-black p-8 overflow-hidden group shadow-xl dark:shadow-2xl">
        <div className="absolute top-0 right-0 p-10 opacity-5 dark:opacity-10 rotate-12 transition-transform group-hover:rotate-45 duration-1000">
            <Wallet size={100} className="text-blue-500" />
        </div>
        <div className="flex items-center gap-2.5 mb-5 relative z-10">
            <div className={`w-2.5 h-2.5 rounded-full animate-pulse glow-blue ${marketSentiment === 'positive' ? 'bg-emerald-500' : 'bg-red-500'}`}></div>
            <span className="text-xs font-bold tracking-[0.2em] text-slate-500 dark:text-slate-400 uppercase">流动性实时监测</span>
        </div>
        <div className="flex items-end justify-between relative z-10">
            <div className="flex items-baseline gap-2.5">
                <span className="text-5xl font-mono-prec font-bold text-slate-900 dark:text-white tracking-tighter">¥ {liquidity.value}</span>
                <span className="text-2xl font-bold text-blue-600 dark:text-blue-500">亿</span>
            </div>
            <div className="flex flex-col gap-2">
                <button onClick={() => setShareConfig({ isOpen: true, data: { title: `集团实时流动头寸日报 (¥${liquidity.value} 亿)`, type: "流动性快照" } })} className="p-2.5 bg-slate-100 dark:bg-white/5 hover:bg-blue-600/10 dark:hover:bg-blue-600/20 rounded-2xl border border-slate-200 dark:border-white/5 transition-all shadow-sm">
                    <Share2 size={16} className="text-slate-500 dark:text-slate-400 group-hover:text-blue-500" />
                </button>
                <button onClick={() => window.location.href = 'http://10.87.11.121:5092'} className="p-2.5 bg-slate-100 dark:bg-white/5 hover:bg-blue-600/10 dark:hover:bg-blue-600/20 rounded-2xl border border-slate-200 dark:border-white/5 transition-all shadow-sm active:scale-95">
                    <ArrowRight size={16} className="text-slate-500 dark:text-slate-400 group-hover:text-blue-500" />
                </button>
            </div>
        </div>
      </div>

      {/* 2. 业务集群经营快照 - 矩阵翻页布局 */}
      <div className="space-y-4">
        <div className="flex items-center justify-between px-2">
            <div className="flex items-center gap-2.5">
                <PieChart size={16} className="text-blue-600 dark:text-blue-500" />
                <h3 className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-[0.2em]">业务集群经营快照</h3>
            </div>
            <div className="flex gap-1.5 items-center">
                <div className={`h-1.5 rounded-full transition-all duration-300 ${activePageIndex === 0 ? 'w-4 bg-blue-500' : 'w-1.5 bg-slate-300 dark:bg-slate-700'}`}></div>
                <div className={`h-1.5 rounded-full transition-all duration-300 ${activePageIndex === 1 ? 'w-4 bg-indigo-500' : 'w-1.5 bg-slate-300 dark:bg-slate-700'}`}></div>
            </div>
        </div>
        <div className="relative">
          <div 
            className="flex overflow-x-auto no-scrollbar snap-x snap-mandatory" 
            onScroll={handleScroll}
          >
              {/* Page 1: 传统产业矩阵 (2x2) */}
              <div className="min-w-full snap-center px-1">
                <div className="grid grid-cols-2 gap-3 mb-4">
                  {pillarClusters.map(cluster => (
                    <React.Fragment key={cluster.id}>
                      <ClusterItem 
                        {...cluster}
                        isExpanded={expandedClusterId === cluster.id}
                        onToggle={() => setExpandedClusterId(expandedClusterId === cluster.id ? null : cluster.id)}
                        onNavigate={onNavigate}
                      />
                      <CostCard 
                        name={cluster.name.split('营收')[0]} 
                        cost={cluster.cost} 
                        breakdown={cluster.breakdown} 
                        color={cluster.color}
                        isExpanded={expandedClusterId === `${cluster.id}-cost`}
                        onToggle={() => setExpandedClusterId(expandedClusterId === `${cluster.id}-cost` ? null : `${cluster.id}-cost`)}
                        onNavigate={onNavigate}
                      />
                    </React.Fragment>
                  ))}
                </div>
              </div>

              {/* Page 2: 战略新兴矩阵 (2x2) */}
              <div className="min-w-full snap-center px-1">
                <div className="grid grid-cols-2 gap-3 mb-4">
                  {strategicClusters.map(cluster => (
                    <React.Fragment key={cluster.id}>
                      <ClusterItem 
                        {...cluster}
                        isExpanded={expandedClusterId === cluster.id}
                        onToggle={() => setExpandedClusterId(expandedClusterId === cluster.id ? null : cluster.id)}
                        onNavigate={onNavigate}
                      />
                      <CostCard 
                        name={cluster.name.split('事业营收')[0]} 
                        cost={cluster.cost} 
                        breakdown={cluster.breakdown} 
                        color={cluster.color}
                        isExpanded={expandedClusterId === `${cluster.id}-cost`}
                        onToggle={() => setExpandedClusterId(expandedClusterId === `${cluster.id}-cost` ? null : `${cluster.id}-cost`)}
                        onNavigate={onNavigate}
                      />
                    </React.Fragment>
                  ))}
                </div>
              </div>
          </div>
          
          {/* 滑动提示阴影 */}
          {activePageIndex === 0 && (
            <div className="absolute top-1/2 right-0 -translate-y-1/2 w-8 h-32 bg-gradient-to-l from-slate-200/20 dark:from-white/5 to-transparent pointer-events-none rounded-l-full"></div>
          )}
        </div>
      </div>

      {/* 3. 组织效能监控中心 */}
      <div className="space-y-5">
        <div className="flex items-center justify-between px-2">
            <div className="flex items-center gap-2.5">
                <Users size={16} className="text-cyan-600 dark:text-cyan-500" />
                <h3 className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-[0.2em]">组织治理与效能枢纽</h3>
            </div>
        </div>
        
        <div className="relative">
          <div className="flex gap-4 overflow-x-auto no-scrollbar snap-x snap-mandatory px-2 pb-6">
              {orgMetrics.map(metric => (
                  <OrgMetricCard 
                      key={metric.id}
                      {...metric}
                      isExpanded={expandedOrgId === metric.id}
                      onToggle={() => setExpandedOrgId(expandedOrgId === metric.id ? null : metric.id)}
                      onNavigate={onNavigate}
                  />
              ))}
          </div>
          <div className="flex justify-center gap-1.5 mt-[-10px]">
            {orgMetrics.map(m => (
              <div key={m.id} className={`h-1 rounded-full transition-all duration-300 ${expandedOrgId === m.id ? 'w-4 bg-cyan-500' : 'w-1.5 bg-slate-200 dark:bg-white/10'}`}></div>
            ))}
          </div>
        </div>
      </div>

      {/* 4. 战略雷达 */}
      <div className="space-y-5 pb-16">
        <div className="flex items-center justify-between px-2">
          <div className="flex items-center gap-2.5">
            <Sparkles size={16} className="text-blue-600 dark:text-blue-500" />
            <h3 className="text-xs font-bold tracking-[0.1em] text-slate-900 dark:text-white uppercase italic">战略态势推演</h3>
          </div>
          <Radar size={14} className="text-emerald-500 animate-spin-slow" />
        </div>
        <div className="glass-card p-2.5 rounded-[2.5rem] bg-white/40 dark:bg-black/20 space-y-3.5">
          {insightItems.map(item => (
            <InsightItem 
              key={item.id}
              item={item}
              isExpanded={expandedInsightId === item.id}
              onToggle={() => setExpandedInsightId(expandedInsightId === item.id ? null : item.id)}
              onNavigate={onNavigate}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
