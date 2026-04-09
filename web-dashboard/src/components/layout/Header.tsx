'use client';

import { motion } from 'framer-motion';
import { Cpu, Target } from 'lucide-react';

import { ProxyStatus as ProxyStatusType } from '../../types';
import { ProxyStatus } from '../dashboard/ProxyStatus';

interface HeaderProps {
    target: string;
    onTargetChange: (newTarget: string) => void;
    proxyStatus: ProxyStatusType | null;
    currentPhase?: string;
}

export const Header = ({ target, onTargetChange, proxyStatus, currentPhase = 'RECON' }: HeaderProps) => {
    const phases = ['RECON', 'ENUM', 'VULN_DEV', 'EXPLOIT', 'POST'];

    return (
        <header className="flex items-center justify-between border border-emerald-900/30 bg-emerald-950/5 p-4 backdrop-blur-md glow-border-emerald gap-8">
            <div className="flex items-center gap-6">
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                >
                    <Cpu className="text-emerald-500" size={32} />
                </motion.div>
                <div>
                    <h1 className="text-xl font-black tracking-[0.2em] text-white">
                        OLHO_DE_DEUS <span className="text-xs text-emerald-800 italic">v.2.0.7</span>
                    </h1>
                    <div className="flex gap-4 text-[10px] mt-1">
                        <span className="flex items-center gap-1 text-emerald-500 font-bold">
                            <div className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.8)]" />
                            NEURAL_LINK_ESTABLISHED
                        </span>
                    </div>
                </div>
            </div>

            {/* MONITOR DE ANONIMATO EM TEMPO REAL */}
            <ProxyStatus status={proxyStatus} />

            {/* BARRA DE FASES PTES */}
            <div className="flex-1 flex justify-center gap-2">
                {phases.map((p) => (
                    <div
                        key={p}
                        className={`flex flex-col items-center gap-1 group transition-all duration-500 ${currentPhase === p ? 'opacity-100 scale-105' : 'opacity-20 translate-y-1 hover:opacity-40'}`}
                    >
                        <span className={`text-[8px] font-black tracking-widest ${currentPhase === p ? 'text-emerald-400' : 'text-white'}`}>
                            {p}
                        </span>
                        <div className={`h-1 w-12 rounded-full transition-all duration-1000 ${currentPhase === p ? 'bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.8)]' : 'bg-emerald-900/40'}`} />
                    </div>
                ))}
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
