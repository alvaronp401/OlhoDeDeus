'use client';

import { useRef, useEffect } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { LogEntry } from './LogEntry';
import { NexusLog } from '../../types';
import { Loader2, Activity } from 'lucide-react';

interface TerminalContainerProps {
  logs: NexusLog[];
  liveLogs?: string;
  isProcessing?: boolean;
  onExecuteCommand?: (comando: string) => void;
}

export const TerminalContainer = ({ logs, liveLogs, isProcessing, onExecuteCommand }: TerminalContainerProps) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs, liveLogs]);

  return (
    <main className="flex-1 flex flex-col border border-emerald-900/20 bg-black/20 rounded-sm relative overflow-hidden glow-border-emerald">
      <div className="absolute top-0 right-0 p-2 text-[8px] text-emerald-900 opacity-30 select-none font-mono flex items-center gap-2">
        {isProcessing && (
          <span className="flex items-center gap-1 text-emerald-500 animate-pulse">
            <Activity size={8} /> LIVE_STREAM_ACTIVE
          </span>
        )}
        SECURE_ENCRYPTION_AES_256_ACTIVE
      </div>
      
      <div 
        ref={scrollRef} 
        className="flex-1 overflow-y-auto p-6 space-y-8 scrollbar-hide scroll-smooth"
      >
        <AnimatePresence mode="popLayout">
          {logs.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full opacity-20 pointer-events-none">
              <p className="text-xs uppercase tracking-[0.5em] animate-pulse">Aguardando Conexão Neural...</p>
            </div>
          ) : (
            <>
              {logs.map((log, i) => (
                <LogEntry 
                  key={`${log.timestamp}-${i}`} 
                  log={log} 
                  onExecuteCommand={onExecuteCommand}
                />
              ))}
              
              {/* LIVE LOG STREAMING AREA */}
              {isProcessing && (
                <motion.div 
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="mt-4 pt-4 border-t border-emerald-900/10"
                >
                  <div className="flex items-center gap-2 mb-2">
                    <Loader2 size={10} className="animate-spin text-emerald-500" />
                    <span className="text-[8px] font-black uppercase text-emerald-800 tracking-widest">Buffer_Process_Output</span>
                  </div>
                  <pre className="text-[10px] font-mono text-emerald-400 bg-emerald-950/5 p-4 border-l-2 border-emerald-500/30 whitespace-pre-wrap leading-relaxed">
                    {liveLogs || 'Aguardando output do terminal...'}
                    <span className="inline-block w-1.5 h-3 bg-emerald-500 ml-1 animate-pulse" />
                  </pre>
                </motion.div>
              )}
            </>
          )}
        </AnimatePresence>
      </div>
    </main>
  );
};
