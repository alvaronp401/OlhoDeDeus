'use client';

import { useRef, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { LogEntry } from './LogEntry';
import { NexusLog } from '../../types';

interface TerminalContainerProps {
  logs: NexusLog[];
}

export const TerminalContainer = ({ logs }: TerminalContainerProps) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <main className="flex-1 flex flex-col border border-emerald-900/20 bg-black/20 rounded-sm relative overflow-hidden glow-border-emerald">
      <div className="absolute top-0 right-0 p-2 text-[8px] text-emerald-900 opacity-30 select-none font-mono">
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
            logs.map((log, i) => (
              <LogEntry key={`${log.timestamp}-${i}`} log={log} />
            ))
          )}
        </AnimatePresence>
      </div>
    </main>
  );
};
