
import React, { useEffect, useRef } from 'react';

interface OntologySphereProps {
  status?: 'idle' | 'thinking' | 'working';
}

const OntologySphere: React.FC<OntologySphereProps> = ({ status = 'idle' }) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    const points: { x: number; y: number; z: number; flash: number }[] = [];
    const numPoints = 80;
    const radius = 100;

    for (let i = 0; i < numPoints; i++) {
      const phi = Math.acos(-1 + (2 * i) / numPoints);
      const theta = Math.sqrt(numPoints * Math.PI) * phi;
      points.push({
        x: radius * Math.cos(theta) * Math.sin(phi),
        y: radius * Math.sin(theta) * Math.sin(phi),
        z: radius * Math.cos(phi),
        flash: 0,
      });
    }

    let angleX = 0;
    let angleY = 0;

    const render = (time: number) => {
      const width = canvas.width;
      const height = canvas.height;
      ctx.clearRect(0, 0, width, height);

      const speedMultiplier = status === 'thinking' ? 4 : status === 'working' ? 2 : 1;
      const flashChance = status === 'thinking' ? 0.08 : status === 'working' ? 0.03 : 0.005;
      const connectionDistThreshold = status === 'thinking' ? 80 : 60;

      angleX += 0.003 * speedMultiplier;
      angleY += 0.005 * speedMultiplier;

      const breathe = 1 + Math.sin(time * 0.001 * speedMultiplier) * 0.05;

      const projectedPoints = points.map((p) => {
        let y1 = p.y * Math.cos(angleX) - p.z * Math.sin(angleX);
        let z1 = p.y * Math.sin(angleX) + p.z * Math.cos(angleX);
        let x2 = p.x * Math.cos(angleY) + z1 * Math.sin(angleY);
        let z2 = -p.x * Math.sin(angleY) + z1 * Math.cos(angleY);
        const scale = (z2 + radius * 2) / (radius * 3) * breathe;
        
        if (Math.random() < flashChance) p.flash = 1.0;
        p.flash *= 0.94;

        return {
          x: x2 * scale + width / 2,
          y: y1 * scale + height / 2,
          z: z2,
          scale,
          flash: p.flash,
        };
      });

      ctx.lineWidth = status === 'thinking' ? 1 : 0.5;
      for (let i = 0; i < projectedPoints.length; i++) {
        for (let j = i + 1; j < projectedPoints.length; j++) {
          const p1 = projectedPoints[i];
          const p2 = projectedPoints[j];
          const dist = Math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2);
          if (dist < connectionDistThreshold) {
            const opacity = (1 - dist / connectionDistThreshold) * 0.3 * (p1.scale);
            const color = status === 'thinking' ? '37, 99, 235' : '59, 130, 246';
            ctx.strokeStyle = `rgba(${color}, ${opacity})`;
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
          }
        }
      }

      projectedPoints.sort((a, b) => a.z - b.z).forEach((p) => {
        const size = (status === 'thinking' ? 2 : 1.5) * p.scale;
        const baseOpacity = 0.3 + (p.scale * 0.4);
        
        if (p.flash > 0.1) {
          ctx.shadowBlur = 10 * p.flash;
          ctx.shadowColor = '#3b82f6';
          ctx.fillStyle = `rgba(59, 130, 246, ${p.flash})`;
          ctx.beginPath();
          ctx.arc(p.x, p.y, size * (1.5 + p.flash), 0, Math.PI * 2);
          ctx.fill();
          ctx.shadowBlur = 0;
        }
        
        ctx.fillStyle = status === 'thinking' 
          ? `rgba(37, 99, 235, ${baseOpacity})` 
          : `rgba(59, 130, 246, ${baseOpacity})`;
        ctx.beginPath();
        ctx.arc(p.x, p.y, size, 0, Math.PI * 2);
        ctx.fill();
      });

      animationFrameId = requestAnimationFrame(render);
    };

    animationFrameId = requestAnimationFrame(render);
    return () => cancelAnimationFrame(animationFrameId);
  }, [status]);

  return (
    <div className="w-full flex justify-center py-4 relative group">
      <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 blur-[60px] rounded-full pointer-events-none transition-all duration-700 ${
        status === 'thinking' ? 'bg-blue-600/10 scale-125' : 'bg-blue-500/5'
      }`}></div>
      <canvas 
        ref={canvasRef} 
        width={300} 
        height={260} 
        className={`relative z-10 transition-transform duration-700 ${status === 'thinking' ? 'scale-110' : 'scale-100'}`}
      />
    </div>
  );
};

export default OntologySphere;
