import React, { useState } from 'react';
import { Check, ArrowRight, Clock, ShieldCheck, ChevronDown, ChevronUp } from 'lucide-react';

interface HeroProps {
  onOpenAccess: () => void;
}

export const Hero: React.FC<HeroProps> = ({ onOpenAccess }) => {
  const [email, setEmail] = useState('');
  const [isApproved, setIsApproved] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPayloadDiff, setShowPayloadDiff] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      onOpenAccess();
    }
  };

  const handleApprove = () => {
    setIsSubmitting(true);
    setTimeout(() => {
      setIsApproved(true);
      setIsSubmitting(false);
    }, 400);
  };

  return (
    <section className="pt-32 pb-20 md:pt-40 md:pb-28">
      <div className="max-w-4xl mx-auto px-6 text-center">
        {/* Release tag */}
        <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-md bg-white/[0.04] border border-white/[0.08] text-[11px] text-zinc-400 mb-8 font-mono">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
          <span>Persistent background runtime · v2.4</span>
        </div>

        {/* Headline */}
        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-white mb-6 leading-[1.1]">
          An autonomous agent that works while your laptop is shut.
        </h1>

        {/* Subhead */}
        <p className="text-base sm:text-lg text-zinc-400 max-w-2xl mx-auto leading-relaxed mb-10 font-normal">
          Assign multi-step objectives across your workspace and developer tools. Spark executes them 24/7 in dedicated cloud sandboxes, asking for your approval only before high-impact operations.
        </p>

        {/* Single minimal input form */}
        <form onSubmit={handleSubmit} className="max-w-md mx-auto flex items-center gap-2 mb-16">
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your work email"
            className="flex-1 px-4 py-2.5 rounded-lg bg-white/[0.04] border border-white/[0.1] text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-white/30 transition-colors"
          />
          <button
            type="submit"
            className="px-4 py-2.5 rounded-lg bg-white hover:bg-zinc-200 text-black text-xs font-semibold transition-colors flex items-center gap-1.5 shrink-0"
          >
            <span>Get access</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </form>

        {/* Single Quiet, Exquisite Hero Demo Card */}
        <div className="max-w-2xl mx-auto text-left rounded-xl border border-white/[0.1] bg-[#0a0a0a] p-6 shadow-2xl">
          {/* Top meta */}
          <div className="flex items-center justify-between pb-4 border-b border-white/[0.06] mb-5">
            <div className="flex items-center gap-2 text-xs">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-zinc-300 font-medium">Active background task</span>
              <span className="text-zinc-600 font-mono">·</span>
              <span className="text-zinc-500 font-mono text-[11px]">Cloud VM us-east4</span>
            </div>
            <div className="text-[11px] text-zinc-500 font-mono flex items-center gap-1">
              <Clock className="w-3 h-3" />
              <span>Started 2h ago</span>
            </div>
          </div>

          {/* Goal prompt */}
          <div className="text-xs text-zinc-300 font-mono mb-6 bg-white/[0.03] p-3 rounded-lg border border-white/[0.04]">
            <span className="text-zinc-500">spark:run</span> "Audit unread communications, re-align today's calendar collisions, and prepare morning briefing memo."
          </div>

          {/* Steps */}
          <div className="space-y-3.5 mb-6 text-xs">
            <div className="flex items-start gap-2.5 text-zinc-300">
              <div className="w-4 h-4 rounded-full bg-white/[0.08] text-white flex items-center justify-center shrink-0 mt-0.5">
                <Check className="w-2.5 h-2.5" />
              </div>
              <div>
                <span className="font-medium text-white">Audited 38 unread emails across Gmail</span>
                <span className="text-zinc-500 block text-[11px] mt-0.5">Filtered 2 critical investor threads requiring partner follow-up</span>
              </div>
            </div>

            <div className="flex items-start gap-2.5 text-zinc-300">
              <div className="w-4 h-4 rounded-full bg-white/[0.08] text-white flex items-center justify-center shrink-0 mt-0.5">
                <Check className="w-2.5 h-2.5" />
              </div>
              <div>
                <span className="font-medium text-white">Detected calendar conflict in Google Calendar</span>
                <span className="text-zinc-500 block text-[11px] mt-0.5">Resolved 2:00 PM product review overlap by drafting shift to 4:30 PM</span>
              </div>
            </div>

            <div className="flex items-start gap-2.5 text-zinc-300">
              <div className="w-4 h-4 rounded-full bg-white/[0.08] text-white flex items-center justify-center shrink-0 mt-0.5">
                <Check className="w-2.5 h-2.5" />
              </div>
              <div>
                <span className="font-medium text-white">Synthesized executive brief in Google Docs</span>
                <span className="text-zinc-500 block text-[11px] mt-0.5">Attached metrics and action recommendations to shared drive</span>
              </div>
            </div>
          </div>

          {/* Approval Checkpoint */}
          <div className="pt-4 border-t border-white/[0.06]">
            {!isApproved ? (
              <div className="p-4 rounded-lg bg-white/[0.02] border border-white/[0.08]">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-xs font-semibold text-white flex items-center gap-1.5">
                    <ShieldCheck className="w-4 h-4 text-zinc-400" />
                    <span>Approval checkpoint</span>
                  </div>
                  <span className="text-[10px] font-mono text-zinc-500">Outbound action</span>
                </div>
                <p className="text-xs text-zinc-400 mb-4 leading-relaxed">
                  Spark is ready to dispatch the digest to Slack #leadership and send the calendar reschedule notices to 3 attendees.
                </p>
                <div className="flex items-center gap-2">
                  <button
                    onClick={handleApprove}
                    disabled={isSubmitting}
                    className="px-3.5 py-1.5 rounded-md bg-white hover:bg-zinc-200 text-black font-semibold text-xs transition-colors flex items-center gap-1.5"
                  >
                    {isSubmitting ? (
                      <span>Executing in sandbox...</span>
                    ) : (
                      <>
                        <Check className="w-3.5 h-3.5" />
                        <span>Authorize and execute</span>
                      </>
                    )}
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowPayloadDiff(!showPayloadDiff)}
                    className="px-3 py-1.5 rounded-md bg-white/[0.04] hover:bg-white/[0.08] text-zinc-300 text-xs transition-colors flex items-center gap-1"
                  >
                    <span>Inspect payload diff</span>
                    {showPayloadDiff ? <ChevronUp className="w-3 h-3 text-zinc-500" /> : <ChevronDown className="w-3 h-3 text-zinc-500" />}
                  </button>
                </div>

                {showPayloadDiff && (
                  <div className="mt-3 p-3 rounded bg-black/50 border border-white/[0.08] text-[11px] font-mono text-zinc-400 space-y-1">
                    <div><span className="text-zinc-600">channel:</span> <span className="text-zinc-200">#leadership (Slack)</span></div>
                    <div><span className="text-zinc-600">document:</span> <span className="text-zinc-200">Briefing-Nov-11.gdoc (Drive)</span></div>
                    <div><span className="text-zinc-600">reschedule:</span> <span className="text-zinc-200">Product Review 2:00 PM → 4:30 PM (3 attendees)</span></div>
                  </div>
                )}
              </div>
            ) : (
              <div className="p-3.5 rounded-lg bg-emerald-500/[0.06] border border-emerald-500/20 text-xs text-emerald-300 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Check className="w-4 h-4 text-emerald-400" />
                  <span>Approved. Slack digest dispatched and calendar updated.</span>
                </div>
                <button
                  onClick={() => setIsApproved(false)}
                  className="text-[11px] text-zinc-500 hover:text-zinc-300 font-mono underline"
                >
                  Reset demo
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
};
