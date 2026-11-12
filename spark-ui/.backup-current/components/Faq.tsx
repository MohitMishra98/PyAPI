import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';

export const Faq: React.FC = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  const faqs = [
    {
      q: 'How is Spark different from standard chat assistants?',
      a: 'Chatbots only run while you have the tab open and require you to prompt every step. Spark runs in an isolated cloud virtual machine that operates 24/7 in the background—decomposing multi-step goals and executing across tools even when your laptop is completely shut.'
    },
    {
      q: 'How do human-in-the-loop approvals work?',
      a: 'Spark can read files, inspect code, and prepare drafts autonomously. Before performing high-impact external actions—like sending an email, pushing a commit, or rescheduling meetings—Spark halts and sends you an instant 1-click notification with a visual diff.'
    },
    {
      q: 'Which tools and APIs does Spark connect to?',
      a: 'Spark natively implements the Model Context Protocol (MCP). It connects to Google Workspace (Gmail, Calendar, Drive, Docs, Sheets), GitHub, Slack, Linear, PostgreSQL, and any custom internal MCP server with verifiable JSON-RPC schemas.'
    },
    {
      q: 'Is my company’s data or code used to train models?',
      a: 'No. We enforce strict contractual zero-retention policies. Your files, communications, and code are never stored for foundation model training. All compute sandboxes are ephemeral and wiped upon task completion.'
    }
  ];

  return (
    <section className="py-24 border-t border-white/[0.06]">
      <div className="max-w-3xl mx-auto px-6">
        <div className="mb-12">
          <div className="text-xs font-mono text-zinc-500 mb-2">FAQ</div>
          <h2 className="text-2xl font-semibold tracking-tight text-white">
            Common questions.
          </h2>
        </div>

        <div className="divide-y divide-white/[0.06]">
          {faqs.map((faq, idx) => {
            const isOpen = openIndex === idx;
            return (
              <div key={idx} className="py-5">
                <button
                  onClick={() => setOpenIndex(isOpen ? null : idx)}
                  className="w-full text-left flex items-center justify-between gap-4 text-xs font-medium text-white hover:text-zinc-300 transition-colors"
                >
                  <span>{faq.q}</span>
                  <ChevronDown
                    className={`w-4 h-4 text-zinc-500 transition-transform duration-200 shrink-0 ${
                      isOpen ? 'rotate-180 text-white' : ''
                    }`}
                  />
                </button>
                {isOpen && (
                  <p className="mt-3 text-xs text-zinc-400 leading-relaxed pr-8">
                    {faq.a}
                  </p>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
