import { useState, useCallback, useEffect } from 'react';
import { NexusLog, PentestRequest, ExecuteRequest } from '../types';

const API_URL = 'http://localhost:8000';

export const useNexus = (currentTarget?: string) => {
  const [logs, setLogs] = useState<NexusLog[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [vulnerabilities, setVulnerabilities] = useState<any[]>([]);
  const [loot, setLoot] = useState<any[]>([]);

  const addLog = useCallback((log: NexusLog) => {
    setLogs((prev) => [...prev, log]);
  }, []);

  // Busca dados reais do banco (Vulns e Loot)
  const refreshVault = useCallback(async () => {
    if (!currentTarget) return;
    try {
      const [vRes, lRes] = await Promise.all([
        fetch(`${API_URL}/vulnerabilities?target=${currentTarget}`),
        fetch(`${API_URL}/loot?target=${currentTarget}`)
      ]);
      if (vRes.ok) setVulnerabilities(await vRes.json());
      if (lRes.ok) setLoot(await lRes.json());
    } catch (err) {
      console.error("Erro ao atualizar cofre:", err);
    }
  }, [currentTarget]);

  // Atualiza automaticamente quando o alvo muda ou algo novo é encontrado
  useEffect(() => {
    refreshVault();
  }, [currentTarget, refreshVault]);

  const sendCommand = async (command: string, target: string) => {
    if (!command || isProcessing) return;
    setIsProcessing(true);
    addLog({ role: 'user', content: command, timestamp: new Date().toLocaleTimeString() });

    try {
      const res = await fetch(`${API_URL}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command, target } as PentestRequest),
      });
      const data = await res.json();
      addLog({ role: 'nexus', ...data, timestamp: new Date().toLocaleTimeString() });
      
      // Se a IA encontrou algo no pensamento, atualiza o painel lateral
      if (data.discovery && data.discovery.type !== 'None') {
        refreshVault();
      }
    } catch (error) {
      addLog({ role: 'system', content: 'Erro na conexão neural.', timestamp: new Date().toLocaleTimeString(), error: true });
    } finally {
      setIsProcessing(false);
    }
  };

  const executeCommand = async (comando: string, target: string, useProxy: boolean = true) => {
    if (!comando || isProcessing) return;
    setIsProcessing(true);
    addLog({ role: 'system', content: `[EXEC] ${comando}`, timestamp: new Date().toLocaleTimeString() });

    try {
      const res = await fetch(`${API_URL}/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: comando, target, use_proxy: useProxy } as ExecuteRequest),
      });
      const data = await res.json();
      addLog({
        role: 'execution',
        content: data.stdout || data.stderr || 'No output.',
        stdout: data.stdout,
        stderr: data.stderr,
        exit_code: data.exit_code,
        timestamp: new Date().toLocaleTimeString(),
        error: data.exit_code !== 0,
      });
      refreshVault(); // Atualiza após execução
    } catch (error) {
      addLog({ role: 'system', content: 'Falha na execução física.', timestamp: new Date().toLocaleTimeString(), error: true });
    } finally {
      setIsProcessing(false);
    }
  };

  return { logs, isProcessing, vulnerabilities, loot, sendCommand, executeCommand, refreshVault };
};
