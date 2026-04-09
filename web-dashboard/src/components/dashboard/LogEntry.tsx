'use client';

import { motion } from 'framer-motion';
import { Zap, Play, Terminal, AlertTriangle, Eye, ShieldAlert, Cpu } from 'lucide-react';
import { NexusLog } from '../../types';

interface LogEntryProps {
  log: NexusLog;
  onExecuteCommand?: (comando: string) => void;
}

export const LogEntry = ({ log, onExecuteCommand }: LogEntryProps) => {
  const isUser = log.role === 'user';
  const isSystem = log.role === 'system';
  const isExecution = log.role === 'execution';
  const isVision = log.role === 'vision';

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
        <div className={`text-[10px] font-bold p-2 ${log.error ? 'text-rose-500 bg-rose-500/5' : 'text-amber-500 bg-amber-500/5'}`}>
          {log.content}
        </div>
      ) : isExecution ? (
        <div className="w-full max-w-[95%] space-y-1">
          <div className="flex items-center gap-2">
            <Terminal size={10} className="text-cyan-400" />
            <span className="text-[9px] bg-cyan-500 text-black px-1 font-black uppercase tracking-tighter">EXEC_OUTPUT</span>
            <span className={`text-[9px] font-mono ${log.exit_code === 0 ? 'text-emerald-500' : 'text-rose-500'}`}>exit:{log.exit_code}</span>
          </div>
          <pre className="bg-black/90 border border-cyan-900/30 p-3 text-[11px] text-cyan-300 font-mono overflow-x-auto max-h-60 overflow-y-auto whitespace-pre-wrap break-all custom-scrollbar">
            {log.stdout || log.content}
          </pre>
          {log.stderr && (
            <pre className="bg-black/90 border border-rose-900/30 p-2 text-[10px] text-rose-400 font-mono">
              <AlertTriangle size={10} className="inline mr-1" />
              {log.stderr}
            </pre>
          )}
        </div>
      ) : isVision ? (
        /* NEXUS VISION RENDERER */
        <div className="w-full max-w-[90%] space-y-3 p-4 bg-emerald-500/5 border border-emerald-500/20 relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-2 opacity-20 pointer-events-none group-hover:opacity-40 transition-opacity">
            <Eye size={48} className="text-emerald-500" />
          </div>
          
          <div className="flex items-center gap-2 relative z-10">
            <Eye size={14} className="text-emerald-400 animate-pulse" />
            <span className="text-[10px] bg-emerald-500 text-black px-1 font-black uppercase tracking-widest">NEXUS_VISION</span>
            <span className="text-[9px] text-emerald-700 italic font-mono">[{log.timestamp}]</span>
          </div>

          <div className="space-y-4 relative z-10">
            <div className="space-y-1">
              <span className="text-[8px] text-emerald-800 uppercase font-bold tracking-widest">Análise_de_Evidência</span>
              <p className="text-sm text-emerald-100 leading-relaxed font-mono">{log.analise}</p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-black/40 p-2 border border-emerald-900/30">
                <span className="text-[8px] text-rose-500 uppercase font-black tracking-widest block mb-1">Vetor_Detectado</span>
                <div className="flex items-center gap-2">
                  <ShieldAlert size={12} className="text-rose-500" />
                  <span className="text-xs text-rose-200 font-bold">{log.vetor}</span>
                </div>
              </div>
              <div className="bg-black/40 p-2 border border-emerald-900/30">
                <span className="text-[8px] text-cyan-500 uppercase font-black tracking-widest block mb-1">Ferramenta_Origem</span>
                <div className="flex items-center gap-2">
                  <Cpu size={12} className="text-cyan-500" />
                  <span className="text-xs text-cyan-200 font-bold">{log.ferramenta_detectada}</span>
                </div>
              </div>
            </div>

            {log.sugestao && (
              <div className="bg-black/90 p-3 border border-emerald-500/30 group/cmd relative overflow-hidden">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-[8px] text-emerald-500 uppercase font-bold tracking-widest">Payload_Sugerido</span>
                  <Zap size={10} className="text-emerald-500 animate-pulse" />
                </div>
                <code className="text-xs text-brand-emerald block break-all font-mono">{log.sugestao}</code>
                {onExecuteCommand && log.sugestao.includes(' ') && (
                   <button
                   onClick={() => onExecuteCommand(log.sugestao!)}
                   className="mt-3 flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/30 px-3 py-1.2 text-[9px] text-emerald-400 uppercase font-bold hover:bg-emerald-500/20 transition-all cursor-pointer"
                 >
                   <Play size={10} /> Executar_Exploração
                 </button>
                )}
              </div>
            )}
          </div>
        </div>
      ) : (
        /* NEXUS STANDARD RESPONSE */
        <div className="w-full max-w-[90%] space-y-2 group">
          <div className="flex items-center gap-2">
            <span className="text-[10px] bg-emerald-500 text-black px-1 font-black uppercase tracking-tighter">
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
                {onExecuteCommand && (
                  <button
                    onClick={() => onExecuteCommand(log.comando!)}
                    className="mt-3 flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/30 px-3 py-1.5 text-[10px] text-emerald-400 uppercase tracking-widest font-bold hover:bg-emerald-500/20 hover:border-emerald-500/60 transition-all cursor-pointer relative z-10 group/btn"
                  >
                    <Play size={10} className="group-hover/btn:animate-pulse" />
                    Executar_no_Kali
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </motion.div>
  );
};
