'use client';

import { Shield, ShieldAlert, Wifi, Globe } from 'lucide-react';
import { ProxyStatus as ProxyStatusType } from '../../types';

interface ProxyStatusProps {
  status: ProxyStatusType | null;
}

export const ProxyStatus = ({ status }: ProxyStatusProps) => {
  if (!status) return (
    <div className="flex items-center gap-2 opacity-30 animate-pulse">
      <Wifi size={12} />
      <span className="text-[10px] font-bold uppercase tracking-widest">Iniciando_Uplink...</span>
    </div>
  );

  const isProtected = status.status === 'PROTECTED';
  const isError = status.status === 'ERROR';

  return (
    <div className={`flex items-center gap-4 px-3 py-1 border ${
      isProtected ? 'border-emerald-500/30 bg-emerald-500/5 text-emerald-400' : 
      isError ? 'border-amber-500/30 bg-amber-500/5 text-amber-500' :
      'border-rose-500 bg-rose-500/10 text-rose-500 shadow-[0_0_15px_rgba(244,63,94,0.2)]'
    } transition-all duration-500`}>
      
      <div className="flex items-center gap-2">
        {isProtected ? <Shield size={12} /> : <ShieldAlert size={12} className="animate-bounce" />}
        <span className="text-[10px] font-black uppercase tracking-tighter">
          {isProtected ? 'ANON_UPLINK_SECURE' : 'UNSAFE_CONNECTION'}
        </span>
      </div>

      <div className="h-4 w-px bg-current opacity-20" />

      <div className="flex items-center gap-2">
        <Globe size={11} className={isProtected ? 'animate-spin-slow' : ''} />
        <span className="text-[10px] font-mono font-bold tracking-widest">
          {status.proxy_ip}
        </span>
        <span className="text-[8px] opacity-40 uppercase">({status.provider})</span>
      </div>

      {!isProtected && !isError && (
        <div className="absolute inset-0 bg-rose-500/20 animate-pulse pointer-events-none" />
      )}
    </div>
  );
};
