import React, { useState } from 'react';
import { Clock, Moon, Users, Plane, Check, ShieldCheck, Mail, Bug, AlertCircle } from 'lucide-react';

export const DayTimeline: React.FC = () => {
  const [activeSlot, setActiveSlot] = useState<number>(0);

  const slots = [
    {
      time: '06:00 AM',
      context: 'Laptop closed / You are asleep',
      icon: Moon,
      title: 'Morning briefing & calendar conflict triage',
      summary: 'While you were sleeping, Spark woke up on schedule to organize your day.',
      steps: [
        'Read 42 unread emails and isolated 2 critical investor questions.',
        'Spotted a double-booking at 2:00 PM and drafted a reschedule to 4:30 PM in Google Calendar.',
        'Synthesized an executive summary doc with key morning metrics.'
      ],
      approvalAction: 'Spark sent a 1-tap Slack message asking to confirm the 4:30 PM calendar shift.'
    },
    {
      time: '02:00 PM',
      context: 'In an executive meeting',
      icon: Users,
      title: 'Automated bug investigation & patch drafting',
      summary: 'A customer reported a broken checkout button during your meeting.',
      steps: [
        'Spark isolated the error in a secure cloud sandbox within 45 seconds.',
        'Pinpointed an unhandled edge case in the coupon validation function.',
        'Wrote a 6-line code patch and verified all 34 test cases passed cleanly.'
      ],
      approvalAction: 'Spark queued a GitHub pull request and notified your lead engineer for 1-click review.'
    },
    {
      time: '11:30 PM',
      context: 'Traveling / Offline without Wi-Fi',
      icon: Plane,
      title: 'Customer churn alert & retention outreach',
      summary: 'While you were in transit, an enterprise customer hit a technical roadblock.',
      steps: [
        'Detected that Acme Corp ($48k ARR) had a sudden 60% drop in daily API syncs.',
        'Checked server logs and identified a misconfigured webhook on their endpoint.',
        'Prepared a helpful, solution-oriented outreach email with the fix attached.'
      ],
      approvalAction: 'Spark saved the message in your Gmail drafts, ready for you to send when you land.'
    }
  ];

  const current = slots[activeSlot];
  const CurrentIcon = current.icon;

  return (
    <section className="py-24 border-t border-[#1b2230] bg-[#07090e]">
      <div className="max-w-5xl mx-auto px-6">
        <div className="max-w-2xl mb-12">
          <div className="text-xs font-mono text-blue-400 mb-2">
            24/7 Background Timeline
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-white font-display mb-3">
            A normal day with Spark.
          </h2>
          <p className="text-sm text-zinc-400 leading-relaxed">
            See how Spark keeps working quietly across the clock while your attention stays on what matters.
          </p>
        </div>

        {/* Time Selector Pills */}
        <div className="flex flex-wrap items-center gap-2 mb-8 bg-[#0b0f17] p-1.5 rounded-xl border border-[#1b2332] w-fit">
          {slots.map((slot, idx) => (
            <button
              key={idx}
              onClick={() => setActiveSlot(idx)}
              className={`px-4 py-2 rounded-lg text-xs font-medium transition-all duration-200 flex items-center gap-2 ${
                activeSlot === idx
                  ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                  : 'text-zinc-400 hover:text-zinc-200 hover:bg-[#121824]'
              }`}
            >
              <Clock className="w-3.5 h-3.5" />
              <span>{slot.time}</span>
            </button>
          ))}
        </div>

        {/* Interactive Timeline Card */}
        <div className="rounded-xl border border-[#212b3c] bg-[#0c1017] p-8 shadow-xl transition-all duration-300">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-5 border-b border-[#1b2332] mb-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
                <CurrentIcon className="w-5 h-5" />
              </div>
              <div>
                <div className="text-xs font-mono text-blue-400 font-semibold">
                  {current.time}
                </div>
                <div className="text-xs text-zinc-400">
                  {current.context}
                </div>
              </div>
            </div>

            <span className="text-[11px] font-mono text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20 w-fit">
              Cloud execution active
            </span>
          </div>

          <h3 className="text-lg font-bold text-white font-display mb-2">
            {current.title}
          </h3>
          <p className="text-xs sm:text-sm text-zinc-400 mb-6 leading-relaxed">
            {current.summary}
          </p>

          {/* Autonomous Steps Taken */}
          <div className="space-y-3 mb-6">
            {current.steps.map((step, sIdx) => (
              <div key={sIdx} className="flex items-start gap-3 text-xs sm:text-sm text-zinc-300">
                <div className="w-4 h-4 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0 mt-0.5">
                  <Check className="w-2.5 h-2.5 stroke-[2.5]" />
                </div>
                <span>{step}</span>
              </div>
            ))}
          </div>

          {/* Approval Safeguard Box */}
          <div className="p-4 rounded-lg bg-amber-500/10 border border-amber-500/25 flex items-start gap-3">
            <ShieldCheck className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <div className="text-xs text-amber-200 leading-relaxed">
              <span className="font-semibold text-amber-300">Human checkpoint: </span>
              {current.approvalAction}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
