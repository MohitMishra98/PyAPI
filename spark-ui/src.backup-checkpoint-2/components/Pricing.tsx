import React, { useState } from 'react';
import { Check } from 'lucide-react';

interface PricingProps {
  onOpenAccess: () => void;
}

export const Pricing: React.FC<PricingProps> = ({ onOpenAccess }) => {
  const [isAnnual, setIsAnnual] = useState(true);

  return (
    <section id="pricing" className="py-24 border-t border-[#1b2230] bg-[#070a10]">
      <div className="max-w-5xl mx-auto px-6">
        <div className="max-w-2xl mb-10 text-center mx-auto">
          <div className="text-xs font-mono text-blue-400 mb-2">
            Transparent Pricing
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-white font-display mb-3">
            Simple, predictable plans.
          </h2>
          <p className="text-sm text-zinc-400 leading-relaxed">
            All plans include dedicated background cloud servers and one-tap human approval safeguards.
          </p>

          {/* Interactive Monthly / Annual Toggle */}
          <div className="mt-8 inline-flex items-center gap-1.5 p-1 rounded-xl bg-[#0b0f17] border border-[#1b2332]">
            <button
              onClick={() => setIsAnnual(false)}
              className={`px-4 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
                !isAnnual
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              Monthly billing
            </button>
            <button
              onClick={() => setIsAnnual(true)}
              className={`px-4 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 flex items-center gap-1.5 ${
                isAnnual
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              <span>Annual billing</span>
              <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-1.5 py-0.2 rounded border border-emerald-500/30">
                Save 20%
              </span>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {/* Pro Plan */}
          <div className="rounded-xl p-8 bg-[#0f1522] border-2 border-blue-500/50 shadow-xl shadow-blue-500/10 flex flex-col justify-between transition-all duration-300 hover:border-blue-400">
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-white font-display">
                  Pro Plan
                </h3>
                <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30">
                  14-day free trial
                </span>
              </div>

              <div className="flex items-baseline gap-1.5 mb-4">
                <span className="text-4xl font-bold text-white font-display">
                  ${isAnnual ? '24' : '29'}
                </span>
                <span className="text-xs text-zinc-400 font-mono">
                  / user / month
                </span>
              </div>

              <p className="text-xs text-zinc-400 leading-relaxed mb-6">
                For professionals and teams automating daily multi-step workflows.
              </p>

              <div className="space-y-3 mb-8 text-xs text-zinc-300">
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-blue-400 shrink-0" />
                  <span>24/7 background execution in the cloud</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-blue-400 shrink-0" />
                  <span>Works with Gmail, Calendar, Slack, GitHub, Linear, Notion</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-blue-400 shrink-0" />
                  <span>One-tap approvals via Slack and mobile</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-blue-400 shrink-0" />
                  <span>Up to 50 background execution hours monthly</span>
                </div>
              </div>
            </div>

            <button
              onClick={onOpenAccess}
              className="w-full py-2.5 rounded-md bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold transition-colors shadow-md shadow-blue-600/30 text-center"
            >
              Start 14-day free trial
            </button>
          </div>

          {/* Enterprise Plan */}
          <div className="rounded-xl p-8 bg-[#0c1017] border border-[#1b2332] flex flex-col justify-between transition-all duration-300 hover:border-zinc-700">
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-white font-display">
                  Enterprise
                </h3>
                <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-[#151c29] text-zinc-400">
                  Custom deployment
                </span>
              </div>

              <div className="flex items-baseline gap-1.5 mb-4">
                <span className="text-3xl font-bold text-white font-display">
                  Custom
                </span>
              </div>

              <p className="text-xs text-zinc-400 leading-relaxed mb-6">
                For organizations requiring dedicated cloud networks, custom models, and strict SLAs.
              </p>

              <div className="space-y-3 mb-8 text-xs text-zinc-300">
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-zinc-400 shrink-0" />
                  <span>Dedicated private cloud infrastructure</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-zinc-400 shrink-0" />
                  <span>Unlimited background compute hours</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-zinc-400 shrink-0" />
                  <span>Single Sign-On (Okta, Google Workspace) & SCIM</span>
                </div>
                <div className="flex items-center gap-2.5">
                  <Check className="w-4 h-4 text-zinc-400 shrink-0" />
                  <span>SOC 2 Type II compliance reports and BAA contracts</span>
                </div>
              </div>
            </div>

            <button
              onClick={onOpenAccess}
              className="w-full py-2.5 rounded-md bg-[#182130] hover:bg-[#222e44] text-zinc-200 border border-[#232e42] text-xs font-semibold transition-colors text-center"
            >
              Talk to our team
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};
