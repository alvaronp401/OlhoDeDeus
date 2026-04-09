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
      if (data.discovery && data.discovery.type !== 'None') refreshVault();
    } catch (error) {
      addLog({ role: 'system', content: 'Erro na conexão neural.', timestamp: new Date().toLocaleTimeString(), error: true });
    } finally {
      setIsProcessing(false);
    }
  };

  // NOVO: Envio de imagens para a Visão do NEXUS
  const sendImage = async (image: File, prompt: string, target: string) => {
    if (isProcessing) return;
    setIsProcessing(true);
    
    addLog({ 
      role: 'user', 
      content: `[EVIDÊNCIA_VISUAL]: ${image.name} - ${prompt}`, 
      timestamp: new Date().toLocaleTimeString() 
    });

    const formData = new FormData();
    formData.append('image', image);
    formData.append('prompt', prompt);
    formData.append('target', target);

    try {
      const res = await fetch(`${API_URL}/ask/vision`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) throw new Error("Falha na análise de visão");

      const data = await res.json();
      addLog({ 
        role: 'vision', 
        ...data, 
        timestamp: new Date().toLocaleTimeString() 
      });
      refreshVault();
    } catch (error) {
      addLog({ 
        role: 'system', 
        content: `>>> VISION_ERROR: ${error instanceof Error ? error.message : 'Falha ao processar imagem'}`, 
        timestamp: new Date().toLocaleTimeString(), 
        error: true 
      });
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
        body: JSON.stringify({ command: comando, target, use_proxy: useProxy }),
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
      refreshVault();
    } catch (error) {
      addLog({ role: 'system', content: 'Falha na execução física.', timestamp: new Date().toLocaleTimeString(), error: true });
    } finally {
      setIsProcessing(false);
    }
  };

  return { logs, isProcessing, vulnerabilities, loot, sendCommand, sendImage, executeCommand, refreshVault };
};
