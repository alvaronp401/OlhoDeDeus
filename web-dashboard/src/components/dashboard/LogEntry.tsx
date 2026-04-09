'use client';

import { motion } from 'framer-motion';
import { Zap } from 'lucide-react';
import { NexusLog } from '../../types';

interface LogEntryProps {
  log: NexusLog;
}

export const LogEntry = ({ log }: LogEntryProps) => {
  const isUser = log.role === 'user';
  const isSystem = log.role === 'system';

  return (
    <motion.div 
      initial={{ opacity: 0, x: isUser ? 20 : -20 }} 
      animate={{ opacity: 1, x: 0 }}
      className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}
    >
      {isUser ? (
        <div className="bg-emerald-900/10 border border-emerald-900/30 p-3 text-xs text-emerald-200 max-w-[60%] glow-border-emerald">
          <span className="text-emerald-700 mr-2 font-black">USER@KALI:~$</span> {log.content}
        </div>
      ) : isSystem ? (
        <div className={`text-[10px] font-bold p-2 ${log.error ? 'text-rose-500 bg-rose-500/5' : 'text-emerald-700 bg-emerald-500/5'}`}>
          {log.content}
        </div>
      ) : (
        <div className="w-full max-w-[90%] space-y-2 group">
          <div className="flex items-center gap-2">
            <span className="text-[9px] bg-emerald-500 text-black px-1 font-black uppercase tracking-tighter">
              {log.fase || 'NEXUS_CORE'}
            </span>
            <span className="text-[9px] text-emerald-900 tracking-tighter font-mono italic">
              [{log.timestamp}]
            </span>
          </div>
          <div className="border-l-2 border-emerald-500 bg-emerald-950/5 p-4 shadow-[0_0_15px_rgba(16,185,129,0.05)] group-hover:bg-emerald-950/10 transition-colors">
            <p className="text-sm text-emerald-100 leading-relaxed mb-4 font-mono antialiased">
              {log.estrategia}
            </p>
            {log.comando && log.comando !== "N/A" && (
              <div className="bg-black/90 p-3 border border-emerald-900/30 group/cmd relative overflow-hidden">
                <div className="flex justify-between items-center mb-1 relative z-10">
                  <span className="text-[8px] text-emerald-800 uppercase font-bold tracking-widest">Sugestão_de_Payload</span>
                  <Zap size={10} className="text-emerald-500 animate-pulse" />
                </div>
                <code className="text-xs text-emerald-400 block break-all font-mono relative z-10">
                  {log.comando}
                </code>
                <div className="absolute inset-0 bg-emerald-500/5 opacity-0 group-hover/cmd:opacity-100 transition-opacity" />
              </div>
            )}
          </div>
        </div>
      )}
    </motion.div>
  );
};
