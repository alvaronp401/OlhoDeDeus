export interface NexusLog {
  role: 'user' | 'nexus' | 'system' | 'execution' | 'vision';
  content?: string;
  fase?: string;
  estrategia?: string;
  comando?: string;
  ferramenta?: string;
  alerta?: string;
  timestamp: string;
  error?: boolean;
  stdout?: string;
  stderr?: string;
  exit_code?: number;
  // Vision fields
  analise?: string;
  vetor?: string;
  sugestao?: string;
  ferramenta_detectada?: string;
}

export interface VisionResponse {
  analise: string;
  vetor: string;
  sugestao: string;
  ferramenta_detectada: string;
}

export interface NexusResponse {
  fase: string;
  estrategia: string;
  comando: string;
  ferramenta: string;
  alerta: string;
  discovery?: any;
}

export interface PentestRequest {
  command: string;
  target: string;
}

export interface ExecuteRequest {
  command: string;
  target: string;
  use_proxy: boolean;
}
