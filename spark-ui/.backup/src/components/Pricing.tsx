import React from 'react';
import { Check, ArrowRight } from 'lucide-react';

interface PricingProps {
  onOpenAccess: () => void;
}

export const Pricing: React.FC<PricingProps> = ({ onOpenAccess }) => {
  return (
    <section id="pricing" className="py-24 border-t border-white/[0.06]">
      <div className="max-w-6xl mx-auto px-6">
        <div className="max-w-xl mb-16">
          <div className="text-xs font-mono text-zinc-500 mb-2">Pricing</div>
          <h2 className="text-2xl sm:text-3xl font-semibold tracking-tight text-white mb-2">
            Predictable cloud runtime pricing.
          </h2>
          <p className="text-xs text-zinc-400">
            All plans include dedicated cloud sandbox execution and human-in-the-loop approvals.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl">
          {/* Plan 1: Pro */}
          <div className="p-8 rounded-xl border border-white/[0.1] bg-[#0a0a0a] flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-base font-semibold text-white">Professional</h3>
                <span className="text-[11px] font-mono text-zinc-400">Monthly or annual</span>
              </div>
              <div className="flex items-baseline gap-1 mb-6">
                <span className="text-3xl font-bold text-white font-sans">$39</span>
                <span className="text-xs text-zinc-500">/ seat / month</span>
              </div>
              <p className="text-xs text-zinc-400 mb-8 leading-relaxed">
                For builders and high-velocity teams automating daily execution across their work tools.
              </p>

              <div className="space-y-3 mb-8 text-xs text-zinc-300">
                <div className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-zinc-400" />
                  <span>Dedicated cloud VM background execution</span>
                </div>
                <div className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-zinc-400" />
                  <span>Google Workspace & GitHub MCP connectors</span>
                </div>
                <div className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-zinc-400" />
                  <span>Slack & mobile 1-click approvals</span>
                </div>
                <div className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-zinc-400" />
                  <span>Persistent procedural skills</span>
                </div>
              </div>
            </div>

            <button
              onClick={onOpenAccess}
              className="w-full py-2.5 rounded-lg bg-white hover:bg-zinc-200 text-black text-xs font-semibold transition-colors flex items-center justify-center gap-1.5"
            >
              <span>Get started</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Plan 2: Enterprise */}
          <div className="p-8 rounded-xl border border-white/[0.08] bg-[#050505] flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-base font-semibold text-white">Enterprise Fleet</h3>
                <span className="text-[11px] font-mono text-zinc-400">Custom deployment</span>
              </div>
              <div className="flex items-baseline gap-1 mb-6">
                <span className="text-3xl font-bold text-white font-sans">Custom</span>
              </div>
              <p className="text-xs text-zinc-400 mb-8 leading-relaxed">
                For organizations requiring dedicated VPC sandboxes, custom LLM routing, and strict SLAs.
              </p>

              <div className="space-y-3 mb-8 text-xs text-zinc-300">
                <div className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-zinc-400" />
                  <span>Dedicated VPC isolation & custom LLM keys</span>
                </div>
                <div className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-zinc-400" />
                  <span>Unlimited background compute hours</span>
                </div>
                <div className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-zinc-400" />
                  <span>SAML SSO (Okta/Google) & SCIM provisioning</span>
                </div>
                <div className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-zinc-400" />
                  <span>Custom security reviews & BAA contracts</span>
                </div>
              </div>
            </div>

            <button
              onClick={onOpenAccess}
              className="w-full py-2.5 rounded-lg bg-white/[0.06] hover:bg-white/[0.1] text-white text-xs font-semibold border border-white/[0.08] transition-colors"
            >
              Contact enterprise team
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};
