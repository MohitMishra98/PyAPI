import React, { useState, useEffect } from 'react';
import { Check, ShieldCheck, RefreshCw, Play, Sparkles } from 'lucide-react';

interface HeroProps {
  onOpenAccess: () => void;
}

export const Hero: React.FC<HeroProps> = ({ onOpenAccess }) => {
  const [email, setEmail] = useState('');
  
  // Step state: 0 = starting, 1 = step 1 done, 2 = step 2 done (ready for approval), 3 = approved
  const [activeStep, setActiveStep] = useState<number>(2);
  const [isSimulating, setIsSimulating] = useState<boolean>(false);
  const [isApproving, setIsApproving] = useState<boolean>(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      onOpenAccess();
    }
  };

  // Run the animated step-by-step demo
  const runLiveSimulation = () => {
    setIsSimulating(true);
    setActiveStep(0);

    setTimeout(() => {
      setActiveStep(1); // Step 1 complete
      setTimeout(() => {
        setActiveStep(2); // Step 2 complete, approval gate active
        setIsSimulating(false);
      }, 900);
    }, 800);
  };

  const handleApprove = () => {
    setIsApproving(true);
    setTimeout(() => {
      setActiveStep(3);
      setIsApproving(false);
    }, 450);
  };

  const handleReset = () => {
    setActiveStep(2);
    setIsApproving(false);
    setIsSimulating(false);
  };

  return (
    <section className="pt-32 pb-20 md:pt-40 md:pb-28 relative overflow-hidden">
      {/* Background glow */}
      <div
        className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[720px] h-[360px] bg-blue-600/10 blur-[130px] pointer-events-none rounded-full"
        aria-hidden="true"
      />

      <div className="max-w-4xl mx-auto px-6 text-center relative z-10">
        {/* Release badge */}
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#111722] border border-[#1f2a3c] text-xs text-blue-400 font-mono mb-6">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Always-on cloud runtime</span>
        </div>

        {/* Main Headline */}
        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-white mb-6 leading-[1.15] font-display">
          The AI agent that works while your laptop is closed.
        </h1>

        {/* 1 Clear Sentence Subhead */}
        <p className="text-base sm:text-lg text-zinc-400 max-w-2xl mx-auto leading-relaxed mb-10 font-normal">
          Assign goals across your daily work tools. Spark runs 24/7 in the cloud and asks for your approval before sending messages, running code, or making changes.
        </p>

        {/* Email Capture */}
        <form onSubmit={handleSubmit} className="max-w-md mx-auto flex items-center gap-2 mb-16">
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your work email"
            className="flex-1 px-4 py-2.5 rounded-md bg-[#0e131c] border border-[#212c3f] text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500 transition-colors shadow-inner"
          />
          <button
            type="submit"
            className="px-5 py-2.5 rounded-md bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold transition-colors shrink-0 shadow-md shadow-blue-600/30"
          >
            Try Spark free
          </button>
        </form>

        {/* Single Dead-Simple Interactive Card with Step Motion */}
        <div className="max-w-2xl mx-auto text-left rounded-xl border border-[#212b3c] bg-[#0c1017] p-6 shadow-2xl transition-all duration-300 hover:border-[#2f3d55]">
          {/* Card Header */}
          <div className="flex items-center justify-between pb-4 border-b border-[#1b2332] mb-5">
            <div>
              <div className="text-xs font-semibold text-white flex items-center gap-2">
                <span>Morning briefing & calendar review</span>
              </div>
              <div className="text-[11px] text-zinc-400 mt-0.5">
                Started automatically at 6:00 AM while your laptop was asleep
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={runLiveSimulation}
                disabled={isSimulating}
                className="hidden sm:inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#141b27] hover:bg-[#1b2434] text-[11px] text-zinc-300 border border-[#202c3e] transition-colors"
                title="Watch Spark execute in real-time"
              >
                <Play className="w-3 h-3 text-blue-400 fill-blue-400" />
                <span>Replay demo</span>
              </button>
              <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-[11px] text-emerald-400 font-mono">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                <span>Running in cloud</span>
              </div>
            </div>
          </div>

          {/* Finished Steps with Animated Transitions */}
          <div className="space-y-3.5 mb-6 text-xs">
            {/* Step 1 */}
            <div
              className={`flex items-start gap-3 transition-all duration-300 ${
                activeStep >= 1 ? 'opacity-100 translate-y-0' : 'opacity-40 translate-y-1'
              }`}
            >
              <div
                className={`w-5 h-5 rounded-full flex items-center justify-center shrink-0 mt-0.5 transition-colors ${
                  activeStep >= 1
                    ? 'bg-emerald-500/20 border border-emerald-500/40 text-emerald-400'
                    : 'bg-zinc-800 border border-zinc-700 text-zinc-500'
                }`}
              >
                {activeStep >= 1 ? (
                  <Check className="w-3 h-3 stroke-[2.5]" />
                ) : (
                  <RefreshCw className="w-2.5 h-2.5 animate-spin text-blue-400" />
                )}
              </div>
              <div>
                <span className="font-medium text-white">Audited 38 unread emails across Gmail</span>
                <span className="text-zinc-400 block text-[11px] mt-0.5">
                  Filtered 2 urgent investor threads requiring your personal follow-up
                </span>
              </div>
            </div>

            {/* Step 2 */}
            <div
              className={`flex items-start gap-3 transition-all duration-300 ${
                activeStep >= 2 ? 'opacity-100 translate-y-0' : 'opacity-40 translate-y-1'
              }`}
            >
              <div
                className={`w-5 h-5 rounded-full flex items-center justify-center shrink-0 mt-0.5 transition-colors ${
                  activeStep >= 2
                    ? 'bg-emerald-500/20 border border-emerald-500/40 text-emerald-400'
                    : 'bg-zinc-800 border border-zinc-700 text-zinc-500'
                }`}
              >
                {activeStep >= 2 ? (
                  <Check className="w-3 h-3 stroke-[2.5]" />
                ) : activeStep === 1 ? (
                  <RefreshCw className="w-2.5 h-2.5 animate-spin text-blue-400" />
                ) : (
                  <span className="w-1.5 h-1.5 rounded-full bg-zinc-600" />
                )}
              </div>
              <div>
                <span className="font-medium text-white">Checked Google Calendar for schedule conflicts</span>
                <span className="text-zinc-400 block text-[11px] mt-0.5">
                  Resolved 2:00 PM overlap by drafting a 4:30 PM time slot shift
                </span>
              </div>
            </div>
          </div>

          {/* Approval Checkpoint with Smooth Transitions */}
          <div className="pt-4 border-t border-[#1b2332]">
            {activeStep < 3 ? (
              <div
                className={`p-4 rounded-lg bg-amber-500/10 border transition-all duration-300 ${
                  activeStep === 2
                    ? 'border-amber-500/35 shadow-sm shadow-amber-500/5'
                    : 'border-amber-500/20 opacity-50'
                }`}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-amber-400" />
                    <span className="text-xs font-semibold text-amber-300">
                      Approval requested
                    </span>
                  </div>
                  <span className="text-[10px] font-mono text-zinc-400">
                    Awaiting authorization
                  </span>
                </div>
                <p className="text-xs text-zinc-300 mb-4 leading-relaxed">
                  Spark wants to send reschedule notices to 3 attendees and post the morning brief to Slack #leadership.
                </p>
                <div className="flex items-center gap-2">
                  <button
                    onClick={handleApprove}
                    disabled={isApproving || activeStep < 2}
                    className="px-4 py-2 rounded-md bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-semibold text-xs transition-colors flex items-center gap-1.5 shadow-sm shadow-emerald-600/30"
                  >
                    {isApproving ? (
                      <>
                        <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                        <span>Sending updates...</span>
                      </>
                    ) : (
                      <>
                        <Check className="w-3.5 h-3.5" />
                        <span>Approve action</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            ) : (
              <div className="p-4 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-between animate-fade-in">
                <div className="flex items-center gap-2 text-xs text-emerald-300">
                  <div className="w-5 h-5 rounded-full bg-emerald-500/20 flex items-center justify-center">
                    <Check className="w-3.5 h-3.5 text-emerald-400 stroke-[2.5]" />
                  </div>
                  <span>Approved. Slack update posted and 3 calendar invites rescheduled.</span>
                </div>
                <button
                  onClick={handleReset}
                  className="text-xs text-zinc-400 hover:text-white font-mono underline ml-3 shrink-0"
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
