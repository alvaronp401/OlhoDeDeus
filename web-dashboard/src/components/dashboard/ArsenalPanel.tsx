'use client';

import { useState } from 'react';
import { TargetIntel, PayloadResult } from '../../types';
import { Skull, Zap, Copy, Terminal, Monitor, Server } from 'lucide-react';

interface ArsenalPanelProps {
  intel: TargetIntel | null;
  onGenerate: (config: any) => Promise<PayloadResult | null>;
}

export const ArsenalPanel = ({ intel, onGenerate }: ArsenalPanelProps) => {
  const [lhost, setLhost] = useState('10.10.x.x');
  const [lport, setLport] = useState('4444');
  const [shellType, setShellType] = useState('bash');
  const [result, setResult] = useState<PayloadResult | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async (type: 'reverse' | 'web') => {
    setIsGenerating(true);
    const res = await onGenerate({ type, lhost, lport, shell_type: shellType });
    setResult(res);
    setIsGenerating(false);
  };

  const copyToClipboard = () => {
    if (result) {
      navigator.clipboard.writeText(result.payload);
    }
  };

  return (
    <div className="w-80 border-l border-emerald-900/30 bg-black/40 flex flex-col overflow-hidden">
      <div className="p-4 border-b border-emerald-900/50 bg-emerald-950/10 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Skull size={16} className="text-rose-500 animate-pulse" />
          <h2 className="text-xs font-black tracking-widest text-white uppercase">Arsenal_Factory</h2>
        </div>
        <div className="text-[8px] text-emerald-800 font-mono">Status: READY</div>
      </div>

      <div className="p-4 space-y-4 overflow-y-auto flex-1 scrollbar-hide">
        {/* TARGET INTEL */}
        <div className="p-3 bg-black/60 border border-emerald-900/20 space-y-2">
          <div className="flex items-center gap-2 text-[10px] text-emerald-500 font-bold uppercase tracking-tighter">
            <Monitor size={10} /> 
            <span>Intel_Detected</span>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <div className="bg-emerald-950/20 p-2 border border-emerald-900/10">
              <span className="block text-[8px] text-emerald-800 uppercase">OS Family</span>
              <span className="text-[10px] text-white font-mono">{intel?.os_family || 'Scanning...'}</span>
            </div>
            <div className="bg-emerald-950/20 p-2 border border-emerald-900/10">
              <span className="block text-[8px] text-emerald-800 uppercase">Tech Stack</span>
              <span className="text-[10px] text-white font-mono">{intel?.tech_stack || 'N/A'}</span>
            </div>
          </div>
        </div>

        {/* PAYLOAD CONFIG */}
        <div className="space-y-3">
          <div className="flex items-center gap-2 text-[10px] text-emerald-500 font-bold uppercase tracking-tighter">
            <Zap size={10} /> 
            <span>Payload_Config</span>
          </div>
          
          <div className="group relative">
            <span className="absolute left-3 top-[-6px] bg-black px-1 text-[8px] text-emerald-700">LHOST</span>
            <input 
              value={lhost}
              onChange={(e) => setLhost(e.target.value)}
              className="w-full bg-black border border-emerald-900/30 p-2 text-[11px] text-emerald-200 outline-none focus:border-emerald-500 transition-colors font-mono"
            />
          </div>

          <div className="group relative">
            <span className="absolute left-3 top-[-6px] bg-black px-1 text-[8px] text-emerald-700">LPORT</span>
            <input 
              value={lport}
              onChange={(e) => setLport(e.target.value)}
              className="w-full bg-black border border-emerald-900/30 p-2 text-[11px] text-emerald-200 outline-none focus:border-emerald-500 transition-colors font-mono"
            />
          </div>

          <div className="flex gap-2">
            <button 
              onClick={() => handleGenerate('reverse')}
              disabled={isGenerating}
              className="flex-1 bg-emerald-900/20 hover:bg-emerald-900/40 border border-emerald-800/50 py-2 flex flex-col items-center gap-1 transition-all group"
            >
              <Terminal size={14} className="text-emerald-500 group-hover:scale-110 transition-transform" />
              <span className="text-[8px] font-black uppercase tracking-widest text-emerald-400">Gen_RevShell</span>
            </button>
            <button 
              onClick={() => handleGenerate('web')}
              disabled={isGenerating}
              className="flex-1 bg-rose-950/10 hover:bg-rose-950/20 border border-rose-900/30 py-2 flex flex-col items-center gap-1 transition-all group"
            >
              <Server size={14} className="text-rose-500 group-hover:scale-110 transition-transform" />
              <span className="text-[8px] font-black uppercase tracking-widest text-rose-400">Gen_WebShell</span>
            </button>
          </div>
        </div>

        {/* OUTPUT AREA */}
        {result && (
          <div className="mt-4 space-y-2 animate-in fade-in slide-in-from-bottom-2">
            <div className="flex items-center justify-between text-[8px] text-emerald-800 uppercase font-black">
              <span>Weapon_Generated</span>
              <button onClick={copyToClipboard} className="flex items-center gap-1 hover:text-emerald-400 transition-colors">
                <Copy size={8} /> Copy
              </button>
            </div>
            <div className="p-3 bg-black border border-emerald-500/30 text-[10px] font-mono text-emerald-100 break-all leading-relaxed relative group overflow-hidden">
               <div className="absolute top-0 right-0 w-8 h-full bg-gradient-to-l from-emerald-500/10 to-transparent pointer-events-none" />
               {result.payload}
            </div>
          </div>
        )}
      </div>

      <div className="p-2 border-t border-emerald-900/30 bg-black/60">
        <div className="text-[6px] text-emerald-900 uppercase font-black tracking-[0.4em] text-center">
          NEURAL_WEAPONIZATION_PROTOCOL_V.1
        </div>
      </div>
    </div>
  );
};
