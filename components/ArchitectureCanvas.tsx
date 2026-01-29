
import React, { useState, useEffect, useRef } from 'react';
import { Code, X, Cpu, Zap, Maximize2 } from 'lucide-react';
import { Node, Edge } from '../types';

interface Particle {
  from: { x: number; y: number };
  to: { x: number; y: number };
  progress: number;
  speed: number;
  color: string;
}

const ArchitectureCanvas: React.FC<{ onClose: () => void }> = ({ onClose }) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);

  const nodes = useRef<Node[]>([
    { id: 'root', label: '<核心入口 />', type: 'core', x: 0.5, y: 0.1, color: '#ffffff' },
    { id: 'state', label: '全局状态管理', type: 'data', x: 0.5, y: 0.25, color: '#f59e0b' },
    { id: 'sidebar', label: '<侧边栏组件 />', type: 'ui', x: 0.2, y: 0.4, color: '#3b82f6' },
    { id: 'dashboard', label: '<驾驶舱视图 />', type: 'view', x: 0.4, y: 0.55, color: '#10b981' },
    { id: 'chat', label: '<智僚对话视图 />', type: 'view', x: 0.6, y: 0.55, color: '#8b5cf6' },
    { id: 'todo', label: '<行动中心视图 />', type: 'view', x: 0.8, y: 0.55, color: '#ec4899' },
    { id: 'charts', label: '可视化引擎', type: 'component', x: 0.35, y: 0.75, color: '#10b981' },
    { id: 'kpi', label: '<KPI 卡片 />', type: 'component', x: 0.45, y: 0.75, color: '#10b981' },
    { id: 'agent_logic', label: '智僚调度逻辑', type: 'logic', x: 0.6, y: 0.75, color: '#8b5cf6' },
    { id: 'sidebar_agent', label: '侧边智僚栏', type: 'component', x: 0.7, y: 0.75, color: '#8b5cf6' },
    { id: 'backend_supply', label: '供应链智能体', type: 'backend', x: 0.5, y: 0.9, color: '#64748b' },
    { id: 'backend_finance', label: '财务风控智能体', type: 'backend', x: 0.7, y: 0.9, color: '#64748b' },
  ]);

  const edges = useRef<Edge[]>([
    { from: 'root', to: 'state' },
    { from: 'root', to: 'sidebar' },
    { from: 'state', to: 'dashboard' },
    { from: 'state', to: 'chat' },
    { from: 'state', to: 'todo' },
    { from: 'dashboard', to: 'charts' },
    { from: 'dashboard', to: 'kpi' },
    { from: 'chat', to: 'agent_logic' },
    { from: 'chat', to: 'sidebar_agent' },
    { from: 'agent_logic', to: 'backend_supply' },
    { from: 'agent_logic', to: 'backend_finance' },
  ]);

  const particles = useRef<Particle[]>([]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let width: number, height: number;

    const resize = () => {
      if (containerRef.current) {
        width = containerRef.current.clientWidth;
        height = containerRef.current.clientHeight;
        canvas.width = width;
        canvas.height = height;
      }
    };

    const resizeObserver = new ResizeObserver(() => resize());
    if (containerRef.current) resizeObserver.observe(containerRef.current);
    resize();

    const drawNode = (node: Node) => {
      const x = node.x * width;
      const y = node.y * height;

      ctx.shadowBlur = 15;
      ctx.shadowColor = node.color;
      ctx.fillStyle = '#0f172a';
      ctx.beginPath();
      ctx.arc(x, y, 6, 0, Math.PI * 2);
      ctx.fill();
      ctx.lineWidth = 2;
      ctx.strokeStyle = node.color;
      ctx.stroke();
      ctx.shadowBlur = 0;
      ctx.fillStyle = node.color;
      ctx.font = 'bold 10px "Inter", sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(node.label, x, y - 20);
    };

    const drawEdge = (edge: Edge) => {
      const fromNode = nodes.current.find(n => n.id === edge.from)!;
      const toNode = nodes.current.find(n => n.id === edge.to)!;
      const x1 = fromNode.x * width;
      const y1 = fromNode.y * height;
      const x2 = toNode.x * width;
      const y2 = toNode.y * height;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      const cp1y = y1 + (y2 - y1) / 2;
      const cp2y = y1 + (y2 - y1) / 2;
      ctx.bezierCurveTo(x1, cp1y, x2, cp2y, x2, y2);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
      ctx.lineWidth = 1;
      ctx.stroke();
      if (Math.random() < 0.02) {
        particles.current.push({
          from: { x: x1, y: y1 },
          to: { x: x2, y: y2 },
          progress: 0,
          speed: 0.005 + Math.random() * 0.01,
          color: toNode.color
        });
      }
    };

    const drawParticles = () => {
      for (let i = particles.current.length - 1; i >= 0; i--) {
        const p = particles.current[i];
        p.progress += p.speed;
        if (p.progress >= 1) {
          particles.current.splice(i, 1);
          continue;
        }
        const t = p.progress;
        const x1 = p.from.x, y1 = p.from.y;
        const x2 = p.to.x, y2 = p.to.y;
        const cp1y = y1 + (y2 - y1) / 2;
        const cp2y = y1 + (y2 - y1) / 2;
        const cx = Math.pow(1-t, 3)*x1 + 3*Math.pow(1-t, 2)*t*x1 + 3*(1-t)*Math.pow(t, 2)*x2 + Math.pow(t, 3)*x2;
        const cy = Math.pow(1-t, 3)*y1 + 3*Math.pow(1-t, 2)*t*cp1y + 3*(1-t)*Math.pow(t, 2)*cp2y + Math.pow(t, 3)*y2;
        ctx.shadowBlur = 8;
        ctx.shadowColor = p.color;
        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(cx, cy, 2, 0, Math.PI * 2);
        ctx.fill();
      }
    };

    const render = () => {
      ctx.clearRect(0, 0, width, height);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
      ctx.lineWidth = 0.5;
      const gridSize = 40;
      ctx.beginPath();
      for (let x = 0; x < width; x += gridSize) { ctx.moveTo(x, 0); ctx.lineTo(x, height); }
      for (let y = 0; y < height; y += gridSize) { ctx.moveTo(0, y); ctx.lineTo(width, y); }
      ctx.stroke();
      edges.current.forEach(drawEdge);
      drawParticles();
      nodes.current.forEach(drawNode);
      animationFrameId = requestAnimationFrame(render);
    };
    render();
    return () => {
      cancelAnimationFrame(animationFrameId);
      resizeObserver.disconnect();
    };
  }, []);

  return (
    <div className="fixed inset-0 z-[100] bg-black/90 backdrop-blur-xl flex items-center justify-center p-4 md:p-8 animate-in fade-in zoom-in duration-300">
      <div ref={containerRef} className="w-full h-full border border-white/10 rounded-3xl bg-[#000000] relative overflow-hidden shadow-[0_0_50px_rgba(0,0,0,1)] ring-1 ring-white/10">
        
        <div className="absolute top-0 left-0 right-0 p-6 border-b border-white/5 flex justify-between items-center z-10 bg-black/40 backdrop-blur-xl">
          <div className="flex items-center gap-4">
            <div className="p-2.5 bg-blue-600/10 rounded-xl text-blue-400 border border-blue-500/20 shadow-[0_0_15px_rgba(59,130,246,0.3)]">
              <Code size={20} />
            </div>
            <div>
              <h2 className="text-white font-bold text-lg tracking-tighter flex items-center gap-2">
                系统架构实时监控
                <span className="text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded animate-pulse">实时分析中</span>
              </h2>
              <p className="text-slate-500 text-[10px] tracking-widest uppercase">React 组件层级与实时数据流向</p>
            </div>
          </div>
          <button onClick={onClose} className="p-3 text-slate-400 hover:text-white hover:bg-red-500/20 border border-white/5 rounded-2xl transition-all">
            <X size={20} />
          </button>
        </div>

        <div className="absolute bottom-8 left-8 z-10 space-y-4 pointer-events-none select-none">
          <div className="glass-card px-4 py-2 flex items-center gap-3 text-xs font-mono text-emerald-400">
            <Cpu size={14} className="animate-spin-slow" />
            <span>内存负载: 12%</span>
          </div>
          <div className="glass-card px-4 py-2 flex items-center gap-3 text-xs font-mono text-blue-400">
            <Zap size={14} className="animate-pulse" />
            <span>活跃信号: 28</span>
          </div>
        </div>

        <div className="absolute bottom-8 right-8 z-10 space-y-2 pointer-events-none select-none flex flex-col items-end">
            <div className="flex items-center gap-2 text-[10px] font-mono text-slate-500">
                <span className="w-2 h-2 rounded-full bg-white"></span> 核心应用
            </div>
            <div className="flex items-center gap-2 text-[10px] font-mono text-slate-500">
                <span className="w-2 h-2 rounded-full bg-blue-500"></span> UI 组件
            </div>
            <div className="flex items-center gap-2 text-[10px] font-mono text-slate-500">
                <span className="w-2 h-2 rounded-full bg-emerald-500"></span> 分析层
            </div>
            <div className="flex items-center gap-2 text-[10px] font-mono text-slate-500">
                <span className="w-2 h-2 rounded-full bg-purple-500"></span> AI 智能体
            </div>
        </div>

        <canvas ref={canvasRef} className="block w-full h-full cursor-crosshair" />
      </div>
    </div>
  );
};

export default ArchitectureCanvas;
