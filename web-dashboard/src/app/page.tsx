'use client';

import { useState } from 'react';
import { ScanlineOverlay } from '@/components/effects/ScanlineOverlay';
import { Header } from '@/components/layout/Header';
import { AssetTree } from '@/components/layout/AssetTree';
import { TerminalContainer } from '@/components/dashboard/TerminalContainer';
import { CommandInput } from '@/components/dashboard/CommandInput';
import { VaultPanel } from '@/components/layout/VaultPanel';
import { useNexus } from '@/hooks/useNexus';

export default function CyberpunkDashboard() {
  const [target, setTarget] = useState('dev-pulse-front.light.com.br');
  const { logs, isProcessing, sendCommand } = useNexus();

  const handleExecute = (command: string) => {
    sendCommand(command, target);
  };

  return (
    <div className="min-h-screen bg-[#050505] text-brand-emerald font-mono selection:bg-brand-emerald selection:text-black overflow-hidden relative">
      {/* Visual FX */}
      <ScanlineOverlay />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(16,185,129,0.05)_0%,transparent_100%)] pointer-events-none" />

      {/* Main UI Layer */}
      <div className="relative z-10 flex h-screen flex-col p-4 gap-4 crt-flicker">
        
        <Header 
          target={target} 
          onTargetChange={setTarget} 
        />

        <div className="flex flex-1 gap-4 overflow-hidden">
          
          <AssetTree target={target} />

          <section className="flex-1 flex flex-col gap-0 overflow-hidden">
            <TerminalContainer logs={logs} />
            <CommandInput 
              onExecute={handleExecute} 
              isProcessing={isProcessing} 
            />
          </section>

          <VaultPanel />

        </div>

        {/* Footer info bar */}
        <footer className="flex justify-between items-center px-4 py-1 border border-emerald-900/10 bg-black/50 text-[8px] text-emerald-900 tracking-[0.3em] font-bold uppercase">
          <span>Cpu_Load: 12.4%</span>
          <span className="animate-pulse">Active_Neural_Link: Standard_Protocol_V2</span>
          <span>System_Region: South_America_East</span>
        </footer>
      </div>
    </div>
  );
}
