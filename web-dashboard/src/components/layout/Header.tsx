'use client';

import { motion } from 'framer-motion';
import { Cpu, Target } from 'lucide-react';

interface HeaderProps {
  target: string;
  onTargetChange: (newTarget: string) => void;
}

export const Header = ({ target, onTargetChange }: HeaderProps) => {
  return (
    <header className="flex items-center justify-between border border-emerald-900/30 bg-emerald-950/5 p-4 backdrop-blur-md glow-border-emerald">
      <div className="flex items-center gap-6">
        <motion.div 
          animate={{ rotate: 360 }} 
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
        >
          <Cpu className="text-emerald-500" size={32} />
        </motion.div>
        <div>
          <h1 className="text-xl font-black tracking-[0.2em] text-white">
            OLHO_DE_DEUS <span className="text-xs text-emerald-800">v.2.0.6</span>
          </h1>
          <div className="flex gap-4 text-[10px]">
            <span className="flex items-center gap-1">
              <div className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse"/> 
              NEURAL_LINK_ESTABLISHED
            </span>
            <span className="text-emerald-900">|</span>
            <span className="text-emerald-700 uppercase">Uplink: tor_proxy_node_4</span>
          </div>
        </div>
      </div>
      <div className="flex items-center gap-2 bg-black px-4 py-2 border border-emerald-900/50 group focus-within:border-emerald-500 transition-colors">
        <Target size={14} className="text-emerald-700 group-focus-within:text-emerald-500" />
        <input 
          value={target} 
          onChange={(e) => onTargetChange(e.target.value)}
          className="bg-transparent text-xs outline-none text-emerald-200 w-48 font-mono"
          placeholder="TARGET_DOMAIN"
        />
      </div>
    </header>
  );
};
