import React from 'react';
import { ShieldCheck } from 'lucide-react';

export const Security: React.FC = () => {
  return (
    <section id="security" className="py-24 border-t border-white/[0.06]">
      <div className="max-w-6xl mx-auto px-6">
        <div className="max-w-xl mb-12">
          <div className="text-xs font-mono text-zinc-500 mb-2">Security & Privacy</div>
          <h2 className="text-2xl sm:text-3xl font-semibold tracking-tight text-white">
            Zero-trust by architecture.
          </h2>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 py-8 border-y border-white/[0.06]">
          <div>
            <div className="text-sm font-semibold text-white mb-1">SOC 2 Type II</div>
            <div className="text-xs text-zinc-400">Independently audited compliance & controls</div>
          </div>
          <div>
            <div className="text-sm font-semibold text-white mb-1">Ephemeral VMs</div>
            <div className="text-xs text-zinc-400">Containers destroyed upon task resolution</div>
          </div>
          <div>
            <div className="text-sm font-semibold text-white mb-1">Zero Training</div>
            <div className="text-xs text-zinc-400">Customer data is never used to train models</div>
          </div>
          <div>
            <div className="text-sm font-semibold text-white mb-1">AES-256 Encryption</div>
            <div className="text-xs text-zinc-400">Envelope encryption in transit and at rest</div>
          </div>
        </div>
      </div>
    </section>
  );
};
