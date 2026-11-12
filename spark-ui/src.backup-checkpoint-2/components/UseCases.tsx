import React from 'react';
import { Mail, Bug, Users, Check } from 'lucide-react';

export const UseCases: React.FC = () => {
  const cases = [
    {
      icon: Mail,
      tag: 'Executive productivity',
      title: 'Morning brief & calendar cleanup',
      sentences: [
        'Every day at 6:00 AM, Spark reviews unread emails, cleans up meeting collisions, and compiles a concise morning memo.',
        'You wake up with your entire schedule aligned and high-priority action items ready for review.'
      ],
      tools: 'Gmail, Google Calendar, Slack'
    },
    {
      icon: Bug,
      tag: 'Engineering & DevOps',
      title: 'Automated bug investigation',
      sentences: [
        'When an automated test breaks, Spark isolates the failing code in a secure sandbox and writes a clean fix.',
        'It verifies all tests pass and asks your lead developer to approve the GitHub pull request with one tap.'
      ],
      tools: 'GitHub, Docker, Slack'
    },
    {
      icon: Users,
      tag: 'Customer success',
      title: 'Customer churn warnings',
      sentences: [
        'Spark tracks customer activity and flags when an enterprise account drops in daily usage.',
        'It detects the technical root cause and stages a personalized check-in email in your drafts ready for you to review.'
      ],
      tools: 'PostgreSQL, Stripe, Gmail'
    }
  ];

  return (
    <section id="use-cases" className="py-24 border-t border-[#1b2230] bg-[#07090e]">
      <div className="max-w-6xl mx-auto px-6">
        <div className="max-w-2xl mb-16">
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-white font-display mb-3">
            Real workflows Spark handles every day.
          </h2>
          <p className="text-sm text-zinc-400 leading-relaxed">
            See how high-velocity leaders and teams automate repetitive, multi-step operations.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {cases.map((c, idx) => {
            const Icon = c.icon;
            return (
              <div
                key={idx}
                className="bg-[#0c1017] border border-[#1b2436] rounded-xl p-7 flex flex-col justify-between hover:border-blue-500/30 transition-colors"
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <div className="w-9 h-9 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
                      <Icon className="w-4 h-4" />
                    </div>
                    <span className="text-[11px] font-mono text-zinc-400 bg-[#131a26] px-2 py-0.5 rounded border border-[#1e2738]">
                      {c.tag}
                    </span>
                  </div>

                  <h3 className="text-base font-semibold text-white mb-3 font-display">
                    {c.title}
                  </h3>

                  <div className="space-y-2 mb-6">
                    {c.sentences.map((sentence, sIdx) => (
                      <p key={sIdx} className="text-xs sm:text-sm text-zinc-400 leading-relaxed">
                        {sentence}
                      </p>
                    ))}
                  </div>
                </div>

                <div className="pt-4 border-t border-[#182130] text-[11px] font-mono text-zinc-400">
                  <span className="text-zinc-500">Connects:</span> {c.tools}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
