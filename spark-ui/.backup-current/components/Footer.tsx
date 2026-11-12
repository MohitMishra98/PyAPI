import React from 'react';
import { Zap } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-white/[0.06] py-12 text-xs text-zinc-500">
      <div className="max-w-6xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-3">
          <div className="w-4 h-4 rounded bg-white flex items-center justify-center">
            <Zap className="w-2.5 h-2.5 text-black fill-black" />
          </div>
          <span className="font-semibold text-zinc-300">Spark</span>
          <span>·</span>
          <span className="font-mono text-[11px] text-zinc-500">Persistent agent runtime</span>
        </div>

        <div className="flex items-center gap-6 text-xs text-zinc-400">
          <a href="#how-it-works" className="hover:text-white transition-colors">How it works</a>
          <a href="#capabilities" className="hover:text-white transition-colors">Capabilities</a>
          <a href="#security" className="hover:text-white transition-colors">Security</a>
          <a href="#pricing" className="hover:text-white transition-colors">Pricing</a>
        </div>

        <div className="flex items-center gap-2 text-[11px] font-mono text-zinc-500">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
          <span>All systems operational</span>
        </div>
      </div>
    </footer>
  );
};
