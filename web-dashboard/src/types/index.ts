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
  analise?: string;
  vetor?: string;
  sugestao?: string;
  ferramenta_detectada?: string;
}

export interface ProxyStatus {
  proxy_ip: string;
  direct_ip: string;
  status: 'PROTECTED' | 'UNSAFE' | 'ERROR';
  provider: string;
}

export interface TargetIntel {
  os_family: string;
  os_version: string;
  tech_stack: string;
}

export interface PayloadResult {
  target: string;
  os: string;
  tech: string;
  payload: string;
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
