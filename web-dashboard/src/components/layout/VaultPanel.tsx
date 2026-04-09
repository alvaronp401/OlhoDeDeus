'use client';

import { Shield, Lock } from 'lucide-react';

export const VaultPanel = () => {
  return (
    <aside className="w-80 space-y-4 flex flex-col">
      <section className="flex-1 border border-emerald-900/20 bg-emerald-950/5 p-4 overflow-y-auto glow-border-emerald">
        <h2 className="text-[10px] uppercase text-rose-500 mb-4 flex items-center gap-2 font-bold tracking-[0.2em]">
          <Shield size={12} className="animate-pulse" /> Detected_Vulns
        </h2>
        <div className="flex flex-col items-center justify-center h-full gap-4 text-center opacity-40 grayscale group hover:grayscale-0 hover:opacity-100 transition-all">
          <Shield size={32} className="text-emerald-900 group-hover:text-rose-600" />
          <p className="text-[10px] text-emerald-900 italic uppercase tracking-tighter">
            Aguardando vetor de entrada...
          </p>
        </div>
      </section>
      
      <section className="flex-1 border border-emerald-900/20 bg-emerald-950/5 p-4 overflow-y-auto glow-border-emerald">
        <h2 className="text-[10px] uppercase text-amber-500 mb-4 flex items-center gap-2 font-bold tracking-[0.2em]">
          <Lock size={12} /> Loot_Stash
        </h2>
        <div className="flex flex-col items-center justify-center h-full gap-4 text-center opacity-40 grayscale group hover:grayscale-0 hover:opacity-100 transition-all">
          <Lock size={32} className="text-emerald-900 group-hover:text-amber-500" />
          <p className="text-[10px] text-emerald-900 italic uppercase tracking-tighter font-mono">
            COFRE_VAZIO.SYS
          </p>
        </div>
      </section>
    </aside>
  );
};
