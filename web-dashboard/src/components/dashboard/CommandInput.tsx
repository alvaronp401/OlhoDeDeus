'use client';

import { useState, KeyboardEvent } from 'react';
import { ChevronRight, Zap, Loader2 } from 'lucide-react';

interface CommandInputProps {
  onExecute: (command: string) => void;
  isProcessing: boolean;
}

export const CommandInput = ({ onExecute, isProcessing }: CommandInputProps) => {
  const [value, setValue] = useState('');

  const handleSend = () => {
    if (value.trim()) {
      onExecute(value);
      setValue('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <div className="p-4 bg-emerald-950/10 border-t border-emerald-900/20 flex gap-4 items-center glow-border-emerald">
      <div className="flex items-center gap-2">
        {isProcessing ? (
          <Loader2 className="text-emerald-500 animate-spin" size={18} />
        ) : (
          <ChevronRight className="text-emerald-500 animate-pulse" size={18} />
        )}
      </div>
      
      <input 
        autoFocus
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={isProcessing}
        className="flex-1 bg-transparent outline-none text-sm text-emerald-400 placeholder:text-emerald-900 disabled:opacity-50 font-mono tracking-wide"
        placeholder={isProcessing ? "PROCESSANDO_REQUISICAO..." : "ESTABELECER_OBJETIVO_DE_INTRUSAO..."}
      />
      
      <button 
        onClick={handleSend}
        disabled={isProcessing || !value.trim()}
        className="group relative px-6 py-2 overflow-hidden bg-emerald-600 hover:bg-emerald-400 disabled:bg-emerald-900 disabled:cursor-not-allowed transition-all"
      >
        <span className="relative z-10 text-black text-[10px] font-black uppercase tracking-widest flex items-center gap-2">
          {isProcessing ? 'CALCULANDO...' : 'EXECUTAR'}
          {!isProcessing && <Zap size={10} className="group-hover:animate-bounce" />}
        </span>
        <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform" />
      </button>
    </div>
  );
};
