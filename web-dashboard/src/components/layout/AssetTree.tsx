'use client';

import { Database, Folder, FileText, ChevronRight } from 'lucide-react';

interface AssetTreeProps {
  target: string;
}

export const AssetTree = ({ target }: AssetTreeProps) => {
  return (
    <aside className="w-72 border border-emerald-900/20 bg-emerald-950/5 p-4 rounded-sm flex flex-col glow-border-emerald">
      <h2 className="text-[10px] uppercase tracking-widest text-emerald-800 mb-4 flex items-center gap-2 font-bold">
        <Database size={12} /> Asset_Tree
      </h2>
      <div className="flex-1 space-y-2 text-xs overflow-y-auto scrollbar-hide">
        <div className="p-2 border border-emerald-900/10 bg-black/40 group hover:border-emerald-500/30 transition-colors cursor-pointer">
          <div className="flex items-center gap-2">
            <ChevronRight size={10} className="text-emerald-900" />
            <p className="text-emerald-400 font-bold truncate">📁 {target}</p>
          </div>
          <div className="pl-6 mt-2 space-y-2 text-[10px] text-emerald-700">
            <div className="flex items-center gap-2 hover:text-emerald-500 transition-colors">
              <FileText size={10} />
              <span>nmap_full.log</span>
            </div>
            <div className="flex items-center gap-2 hover:text-emerald-500 transition-colors">
              <FileText size={10} />
              <span>subdomains.json</span>
            </div>
            <div className="flex items-center gap-2 text-emerald-500 font-bold">
              <Folder size={10} />
              <span>loot_vault/</span>
            </div>
            <div className="flex items-center gap-2 hover:text-emerald-500 transition-colors">
              <FileText size={10} />
              <span>katana_scans.txt</span>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
};
