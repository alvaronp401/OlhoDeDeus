'use client';

import { useState, useMemo } from 'react';
import { ScanlineOverlay } from '@/components/effects/ScanlineOverlay';
import { Header } from '@/components/layout/Header';
import { AssetTree } from '@/components/layout/AssetTree';
import { TerminalContainer } from '@/components/dashboard/TerminalContainer';
import { CommandInput } from '@/components/dashboard/CommandInput';
import { VaultPanel } from '@/components/layout/VaultPanel';
import { ArsenalPanel } from '@/components/dashboard/ArsenalPanel';
import { useNexus } from '@/hooks/useNexus';

export default function CyberpunkDashboard() {
  const [target, setTarget] = useState('movemind.ia.br');
  
  const { 
    logs, 
    isProcessing, 
    vulnerabilities, 
    loot, 
    proxyStatus,
    targetIntel,
    sendCommand, 
    sendImage,
    executeCommand,
    generatePayload
  } = useNexus(target);

  // Extrai a fase atual baseada no último log do Nexus
  const currentPhase = useMemo(() => {
    const lastNexusLog = [...logs].reverse().find(l => l.role === 'nexus');
    return lastNexusLog?.fase || 'RECON';
  }, [logs]);

  const handleAsk = (command: string) => {
    sendCommand(command, target);
  };

  const handleExecute = (command: string) => {
    executeCommand(command, target);
  };

  const handleSendImage = (file: File, prompt: string) => {
    sendImage(file, prompt, target);
  };

  return (
    <div className="min-h-screen bg-[#050505] text-brand-emerald font-mono selection:bg-brand-emerald selection:text-black overflow-hidden relative">
      <ScanlineOverlay />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(16,185,129,0.05)_0%,transparent_100%)] pointer-events-none" />

      <div className="relative z-10 flex h-screen flex-col p-4 gap-4 crt-flicker">
        
        <Header 
          target={target} 
          onTargetChange={setTarget} 
          proxyStatus={proxyStatus}
          currentPhase={currentPhase}
        />

        <div className="flex flex-1 gap-4 overflow-hidden">
          
          <AssetTree target={target} />

          <section className="flex-1 flex flex-col gap-0 overflow-hidden">
            <TerminalContainer 
              logs={logs} 
              onExecuteCommand={handleExecute} 
            />
            <CommandInput 
              onExecute={handleAsk} 
              onSendImage={handleSendImage}
              isProcessing={isProcessing} 
            />
          </section>

          <div className="flex flex-col gap-4">
            <VaultPanel vulnerabilities={vulnerabilities} loot={loot} />
            <ArsenalPanel intel={targetIntel} onGenerate={generatePayload} />
          </div>

        </div>

        <footer className="flex justify-between items-center px-4 py-1 border border-emerald-900/10 bg-black/50 text-[8px] text-emerald-900 tracking-[0.3em] font-bold uppercase">
          <span>Cpu_Load: 12.4%</span>
          <span className="animate-pulse flex gap-2">
            NEURAL_LINK: ACTIVE 
            <span className="text-emerald-500">|</span> 
            ADAPTIVE_PROXY: {proxyStatus?.status === 'PROTECTED' ? 'ENABLED' : 'DANGER'}
            <span className="text-emerald-500">|</span> 
            OS: {targetIntel?.os_family || 'SCANNING'}
          </span>
          <span>System_Region: South_America_East</span>
        </footer>
      </div>
    </div>
  );
}
