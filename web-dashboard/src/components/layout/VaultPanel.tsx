'use client';

import { Shield, Lock, AlertCircle } from 'lucide-react';

interface VaultPanelProps {
  vulnerabilities: any[];
  loot: any[];
}

export const VaultPanel = ({ vulnerabilities, loot }: VaultPanelProps) => {
  return (
    <aside className="w-80 space-y-4 flex flex-col h-full overflow-hidden">
      {/* VULNERABILITIES SECTION */}
      <section className="flex-1 border border-emerald-900/20 bg-emerald-950/5 p-4 flex flex-col overflow-hidden glow-border-emerald">
        <h2 className="text-[10px] uppercase text-rose-500 mb-4 flex items-center justify-between font-bold tracking-[0.2em]">
          <span className="flex items-center gap-2"><Shield size={12} className="animate-pulse" /> Detected_Vulns</span>
          <span className="bg-rose-500/20 px-2 rounded-full">{vulnerabilities.length}</span>
        </h2>
        
        <div className="flex-1 overflow-y-auto space-y-3 pr-1 custom-scrollbar">
          {vulnerabilities.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full gap-4 text-center opacity-40">
              <Shield size={32} className="text-emerald-900" />
              <p className="text-[10px] text-emerald-900 italic uppercase tracking-tighter">Aguardando vetor de entrada...</p>
            </div>
          ) : (
            vulnerabilities.map((v, i) => (
              <div key={i} className="border-l-2 border-rose-500 bg-rose-500/5 p-2 space-y-1 group hover:bg-rose-500/10 transition-colors">
                <div className="flex justify-between items-start">
                  <span className="text-[10px] font-black text-rose-400 uppercase leading-tight">{v.title}</span>
                  <span className={`text-[8px] px-1 font-bold ${
                    v.severity === 'CRITICAL' ? 'bg-rose-600 text-white' : 
                    v.severity === 'HIGH' ? 'bg-rose-500/30 text-rose-400' : 'bg-emerald-500/20 text-emerald-400'
                  }`}>{v.severity}</span>
                </div>
                <p className="text-[9px] text-rose-100/60 leading-tight italic truncate">{v.description}</p>
              </div>
            ))
          )}
        </div>
      </section>
      
      {/* LOOT SECTION */}
      <section className="flex-1 border border-emerald-900/20 bg-emerald-950/5 p-4 flex flex-col overflow-hidden glow-border-emerald text-amber-500">
        <h2 className="text-[10px] uppercase mb-4 flex items-center justify-between font-bold tracking-[0.2em]">
          <span className="flex items-center gap-2"><Lock size={12} /> Loot_Stash</span>
          <span className="bg-amber-500/20 px-2 rounded-full">{loot.length}</span>
        </h2>
        
        <div className="flex-1 overflow-y-auto space-y-3 pr-1 custom-scrollbar">
          {loot.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full gap-4 text-center opacity-40">
              <Lock size={32} className="text-emerald-900" />
              <p className="text-[10px] text-emerald-900 italic uppercase font-mono">COFRE_VAZIO.SYS</p>
            </div>
          ) : (
            loot.map((l, i) => (
              <div key={i} className="border border-amber-500/30 bg-amber-500/5 p-2 space-y-1 relative group overflow-hidden">
                <div className="absolute top-0 right-0 p-1 opacity-20"><AlertCircle size={8} /></div>
                <span className="text-[8px] text-amber-700 uppercase font-black tracking-widest block">{l.type}</span>
                <code className="text-[10px] text-amber-200 block break-all leading-tight font-mono">{l.data}</code>
                <span className="text-[8px] text-amber-900 block truncate italic mt-1">{l.origin}</span>
              </div>
            ))
          )}
        </div>
      </section>
    </aside>
  );
};
