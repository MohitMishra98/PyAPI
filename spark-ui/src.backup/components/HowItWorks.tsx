import React from 'react';
import { Server, Shield, Network } from 'lucide-react';

export const HowItWorks: React.FC = () => {
  return (
    <section id="how-it-works" className="py-24 border-t border-white/[0.06]">
      <div className="max-w-6xl mx-auto px-6">
        <div className="max-w-xl mb-16">
          <div className="text-xs font-mono text-zinc-500 mb-2">Core Architecture</div>
          <h2 className="text-2xl sm:text-3xl font-semibold tracking-tight text-white">
            Designed for high agency, engineered for total control.
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          {/* Pillar 1 */}
          <div className="space-y-4">
            <div className="w-8 h-8 rounded-lg bg-white/[0.05] border border-white/[0.08] flex items-center justify-center text-zinc-300">
              <Server className="w-4 h-4" />
            </div>
            <h3 className="text-sm font-semibold text-white">
              Persistent cloud runtime
            </h3>
            <p className="text-xs text-zinc-400 leading-relaxed">
              Standard chatbots halt execution the moment you navigate away. Spark runs on dedicated, isolated cloud virtual machines that continue executing multi-step workflows even when your laptop is completely shut.
            </p>
          </div>

          {/* Pillar 2 */}
          <div className="space-y-4">
            <div className="w-8 h-8 rounded-lg bg-white/[0.05] border border-white/[0.08] flex items-center justify-center text-zinc-300">
              <Shield className="w-4 h-4" />
            </div>
            <h3 className="text-sm font-semibold text-white">
              Deterministic human approvals
            </h3>
            <p className="text-xs text-zinc-400 leading-relaxed">
              Autonomous execution requires explicit boundaries. Spark reads files, runs queries, and compiles drafts without interruption, but pauses at checkpoints for your one-click authorization before any high-impact action.
            </p>
          </div>

          {/* Pillar 3 */}
          <div className="space-y-4">
            <div className="w-8 h-8 rounded-lg bg-white/[0.05] border border-white/[0.08] flex items-center justify-center text-zinc-300">
              <Network className="w-4 h-4" />
            </div>
            <h3 className="text-sm font-semibold text-white">
              Model Context Protocol (MCP)
            </h3>
            <p className="text-xs text-zinc-400 leading-relaxed">
              Built on the open standard for tool integration. Connect natively to Google Workspace, GitHub, Slack, Linear, PostgreSQL, and custom internal servers with verifiable JSON-RPC schemas.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};
