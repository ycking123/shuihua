
import React from 'react';

interface OntologySphereProps {
  status?: 'idle' | 'thinking' | 'working';
  isActive?: boolean;
}

// 球体点位和连线预计算（模块级常量，整个应用生命周期只计算一次）
const SPHERE_DATA = (() => {
  const points: { x: number; y: number; z: number; size: number; opacity: number }[] = [];
  const connections: { x1: number; y1: number; x2: number; y2: number; opacity: number }[] = [];
  const numPoints = 60;
  const radius = 100;
  const cx = 150, cy = 130;

  for (let i = 0; i < numPoints; i++) {
    const phi = Math.acos(-1 + (2 * i) / numPoints);
    const theta = Math.sqrt(numPoints * Math.PI) * phi;
    const x = radius * Math.cos(theta) * Math.sin(phi);
    const y = radius * Math.sin(theta) * Math.sin(phi);
    const z = radius * Math.cos(phi);
    const scale = (z + radius * 2) / (radius * 3);
    points.push({
      x: x * scale + cx,
      y: y * scale + cy,
      z,
      size: 1.5 * scale,
      opacity: 0.3 + scale * 0.4,
    });
  }

  // 预计算连线（距离 < 60px 的点对）
  for (let i = 0; i < points.length; i++) {
    for (let j = i + 1; j < points.length; j++) {
      const dist = Math.hypot(points[i].x - points[j].x, points[i].y - points[j].y);
      if (dist < 60) {
        connections.push({
          x1: points[i].x, y1: points[i].y,
          x2: points[j].x, y2: points[j].y,
          opacity: (1 - dist / 60) * 0.3 * ((points[i].z + radius * 2) / (radius * 3)),
        });
      }
    }
  }

  // 按z轴排序（远→近），确保绘制层次正确
  points.sort((a, b) => a.z - b.z);
  return { points, connections };
})();

// CSS keyframes — 仅使用 transform + opacity（compositor-only，近零GPU开销）
const pulseKeyframes = `
@keyframes spherePulse {
  0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.85; }
  50% { transform: scale(1.06) rotate(3deg); opacity: 1; }
}`;

const OntologySphere: React.FC<OntologySphereProps> = ({ status = 'idle', isActive = true }) => {
  // 非活跃时不渲染内容，保留占位高度防止布局跳动
  if (!isActive) return <div className="w-full flex justify-center py-4" style={{ height: 260 }} />;

  const isAnimating = status === 'thinking' || status === 'working';

  return (
    <div className="w-full flex justify-center py-4 relative group">
      <style>{pulseKeyframes}</style>
      <div style={isAnimating ? {
        animation: `spherePulse ${status === 'thinking' ? '2s' : '3s'} ease-in-out infinite`,
        willChange: 'transform, opacity',
      } : undefined}>
        <svg width="300" height="260" viewBox="0 0 300 260">
          {/* 连线 */}
          {SPHERE_DATA.connections.map((c, i) => (
            <line key={i} x1={c.x1} y1={c.y1} x2={c.x2} y2={c.y2}
              stroke={`rgba(59,130,246,${c.opacity.toFixed(3)})`} strokeWidth="0.5" />
          ))}
          {/* 节点 */}
          {SPHERE_DATA.points.map((p, i) => (
            <circle key={i} cx={p.x} cy={p.y} r={p.size}
              fill={`rgba(59,130,246,${p.opacity.toFixed(3)})`} />
          ))}
        </svg>
      </div>
    </div>
  );
};

export default OntologySphere;

