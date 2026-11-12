import React from 'react';
import { Moon, ShieldCheck, Layers } from 'lucide-react';

export const CoreBenefits: React.FC = () => {
  const benefits = [
    {
      icon: Moon,
      title: 'Works 24/7 in the background',
      description: 'Standard AI assistants stop working the second you close the tab. Spark runs continuously on dedicated cloud servers, finishing multi-hour tasks while your laptop is closed, your phone is locked, or you are completely offline.'
    },
    {
      icon: ShieldCheck,
      title: 'Always asks before big actions',
      description: 'Zero rogue mistakes. Spark reads files and drafts updates completely on its own, but automatically stops and waits for your one-click approval before sending external emails, updating databases, or pushing code.'
    },
    {
      icon: Layers,
      title: 'Connects to your everyday tools',
      description: 'No brittle custom setups. Spark connects securely to Google Workspace (Gmail, Calendar, Docs, Sheets), GitHub, Slack, Linear, Notion, and your databases using open protocol standards.'
    }
  ];

  return (
    <section id="how-it-works" className="py-24 border-t border-[#1b2230] bg-[#070a10]">
      <div className="max-w-6xl mx-auto px-6">
        <div className="max-w-2xl mb-16">
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-white font-display mb-3">
            Built for peace of mind and real work.
          </h2>
          <p className="text-sm text-zinc-400 leading-relaxed">
            Everything you need to automate multi-step tasks without worrying about hallucinations or surprises.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {benefits.map((b, idx) => {
            const Icon = b.icon;
            return (
              <div
                key={idx}
                className="bg-[#0c1017] border border-[#1b2436] rounded-xl p-7 hover:border-blue-500/30 transition-colors"
              >
                <div className="w-10 h-10 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 mb-5">
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="text-base font-semibold text-white mb-2 font-display">
                  {b.title}
                </h3>
                <p className="text-xs sm:text-sm text-zinc-400 leading-relaxed">
                  {b.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
