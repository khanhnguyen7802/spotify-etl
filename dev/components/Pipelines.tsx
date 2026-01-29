import React, { useEffect, useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { fetchPipelineStatus, fetchLogs } from '../services/api';
import { PipelineStats, LogEntry } from '../types';
import { Database, Filter, Star, CheckCircle, Terminal } from 'lucide-react';

const PipeConnector = ({ active }: { active: boolean }) => (
  <div className="hidden lg:flex flex-1 h-[2px] bg-white/10 relative mx-4 items-center">
    {active && (
      <motion.div
        layoutId="particle"
        className="absolute h-2 w-8 bg-spotify rounded-full blur-[2px]"
        initial={{ x: 0 }}
        animate={{ x: '100%' }}
        transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
        style={{ width: '30%' }}
      />
    )}
  </div>
);

const PipelineCard: React.FC<{
  title: string;
  layer: string;
  icon: React.ReactNode;
  stats: any;
  color: string;
  active: boolean;
}> = ({ title, layer, icon, stats, color, active }) => (
  <div className={`relative flex flex-col p-6 rounded-2xl border bg-offblack/60 backdrop-blur-md transition-all duration-500
    ${active ? `border-${color} shadow-[0_0_30px_-10px_rgba(255,255,255,0.1)]` : 'border-white/5 opacity-60'}
  `}>
    <div className={`absolute top-0 left-0 w-full h-1 bg-${color}/50 rounded-t-2xl`} />
    <div className="flex justify-between items-start mb-4">
        <div className={`p-3 rounded-xl bg-white/5 text-${color}`}>
            {icon}
        </div>
        {active && <span className="flex h-2 w-2 rounded-full bg-green-500 animate-pulse"></span>}
    </div>
    <h3 className="text-lg font-bold text-white">{title}</h3>
    <p className="text-xs uppercase tracking-widest text-graphite mb-4">{layer} Layer</p>
    
    <div className="mt-auto space-y-2">
        <div className="flex justify-between text-sm">
            <span className="text-graphite">Processed</span>
            <span className="text-mist font-mono">{stats.rows || stats.kpis || 0}</span>
        </div>
        <div className="flex justify-between text-sm">
            <span className="text-graphite">Last Update</span>
            <span className="text-mist font-mono text-xs">{stats.timestamp !== 'PENDING' ? 'Just now' : 'Pending'}</span>
        </div>
    </div>
  </div>
);

const Pipelines: React.FC = () => {
  const [status, setStatus] = useState<PipelineStats | null>(null);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchPipelineStatus().then(setStatus);
    const interval = setInterval(() => {
        fetchLogs().then(newLogs => {
            setLogs(prev => [...prev.slice(-50), ...newLogs]);
            if (scrollRef.current) {
                scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
            }
        });
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  if (!status) return <div>Loading Systems...</div>;

  return (
    <div className="h-full flex flex-col gap-8">
      {/* Top: Visualization */}
      <div className="flex flex-col lg:flex-row items-stretch justify-between gap-4 lg:gap-0 p-8 rounded-3xl bg-obsidian/50 border border-white/5 relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-5 pointer-events-none"></div>
        
        <PipelineCard 
            title="Ingestion" 
            layer="Bronze"
            icon={<Database />} 
            stats={status.bronze} 
            color="bronze" 
            active={true}
        />
        
        <PipeConnector active={true} />
        
        <PipelineCard 
            title="Cleaning" 
            layer="Silver"
            icon={<Filter />} 
            stats={status.silver} 
            color="silver" 
            active={status.currentStage === 'silver' || status.currentStage === 'gold'}
        />

        <PipeConnector active={status.currentStage === 'gold'} />

        <PipelineCard 
            title="Business Logic" 
            layer="Gold"
            icon={<Star />} 
            stats={status.gold} 
            color="gold" 
            active={status.currentStage === 'gold'}
        />
      </div>

      {/* Bottom: Logs */}
      <div className="flex-1 bg-[#0a0a0a] rounded-xl border border-white/10 overflow-hidden flex flex-col font-mono text-sm shadow-2xl">
        <div className="flex items-center px-4 py-2 border-b border-white/5 bg-white/5 gap-2">
            <Terminal size={14} className="text-graphite" />
            <span className="text-graphite text-xs">Pipeline Execution Logs</span>
            <div className="ml-auto flex gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/50"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/50"></div>
                <div className="w-3 h-3 rounded-full bg-green-500/20 border border-green-500/50"></div>
            </div>
        </div>
        <div className="flex-1 p-4 overflow-y-auto space-y-1" ref={scrollRef}>
            {logs.map((log, i) => (
                <div key={i} className="flex gap-4 hover:bg-white/5 p-1 rounded transition-colors">
                    <span className="text-graphite w-24 shrink-0 opacity-50">{log.timestamp.split('T')[1].split('.')[0]}</span>
                    <span className={`shrink-0 font-bold w-20 
                        ${log.level === 'INFO' ? 'text-blue-400' : 
                          log.level === 'SUCCESS' ? 'text-green-400' : 
                          log.level === 'WARNING' ? 'text-yellow-400' : 'text-red-500'}`}>
                        [{log.level}]
                    </span>
                    <span className="text-gray-300 break-all">{log.message}</span>
                </div>
            ))}
            <div className="animate-pulse text-spotify">_</div>
        </div>
      </div>
    </div>
  );
};

export default Pipelines;