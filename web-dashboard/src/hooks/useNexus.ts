import { useState, useCallback } from 'react';
import { NexusLog, PentestRequest } from '../types';

export const useNexus = () => {
  const [logs, setLogs] = useState<NexusLog[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);

  const addLog = useCallback((log: NexusLog) => {
    setLogs((prev) => [...prev, log]);
  }, []);

  const clearLogs = useCallback(() => {
    setLogs([]);
  }, []);

  const sendCommand = async (command: string, target: string) => {
    if (!command || isProcessing) return;

    setIsProcessing(true);
    const timestamp = new Date().toLocaleTimeString();
    
    // Add user log immediately
    addLog({
      role: 'user',
      content: command,
      timestamp,
    });

    try {
      const res = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command, target } as PentestRequest),
      });

      if (!res.ok) throw new Error('Falha na comunicação com o Nexus Core');

      const data = await res.json();
      
      // Add nexus response log
      addLog({
        role: 'nexus',
        ...data,
        timestamp: new Date().toLocaleTimeString(),
      });
    } catch (error) {
      addLog({
        role: 'system',
        content: `>>> CRITICAL_ERROR: ${error instanceof Error ? error.message : 'Unknown system failure'}`,
        timestamp: new Date().toLocaleTimeString(),
        error: true,
      });
    } finally {
      setIsProcessing(false);
    }
  };

  return {
    logs,
    isProcessing,
    sendCommand,
    clearLogs,
  };
};
