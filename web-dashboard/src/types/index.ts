export interface NexusLog {
  role: 'user' | 'nexus' | 'system';
  content?: string;
  fase?: string;
  estrategia?: string;
  comando?: string;
  ferramenta?: string;
  alerta?: string;
  timestamp: string;
  error?: boolean;
}

export interface NexusResponse {
  fase: string;
  estrategia: string;
  comando: string;
  ferramenta: string;
  alerta: string;
}

export interface PentestRequest {
  command: string;
  target: string;
}
