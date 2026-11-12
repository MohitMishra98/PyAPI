import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';

export const Faq: React.FC = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  const faqs = [
    {
      q: 'What does "works while your laptop is closed" mean?',
      a: 'Unlike chatbots that stop the second you close your browser tab or turn off your computer, Spark runs on dedicated cloud servers. You can assign a task, shut your laptop, and go to sleep. Spark keeps executing until the goal is finished and alerts you when ready.'
    },
    {
      q: 'How do approvals work?',
      a: 'Spark safely handles all research, reading, and drafting on its own. Before taking any high-impact action—like sending an external email, updating a live database, or pushing code—Spark stops and sends you a 1-tap message on Slack or your phone. Nothing is dispatched without your sign-off.'
    },
    {
      q: 'Which tools can Spark connect to?',
      a: 'Spark connects directly to Google Workspace (Gmail, Calendar, Drive, Docs), GitHub, Slack, Linear, Notion, PostgreSQL, and custom internal tools using the open Model Context Protocol standard.'
    },
    {
      q: 'Is my company data safe and private?',
      a: 'Yes. Every task runs in an isolated, secure cloud sandbox that is wiped clean immediately after the task completes. Your emails, code, and customer records are never stored or used to train AI models.'
    }
  ];

  return (
    <section id="faq" className="py-24 border-t border-[#1b2230] bg-[#07090e]">
      <div className="max-w-3xl mx-auto px-6">
        <div className="mb-12">
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-white font-display mb-3">
            Frequently asked questions.
          </h2>
          <p className="text-sm text-zinc-400 leading-relaxed">
            Quick answers about how Spark works, stays safe, and keeps your data private.
          </p>
        </div>

        <div className="divide-y divide-[#182130]">
          {faqs.map((faq, idx) => {
            const isOpen = openIndex === idx;
            return (
              <div key={idx} className="py-5">
                <button
                  type="button"
                  onClick={() => setOpenIndex(isOpen ? null : idx)}
                  className="w-full text-left flex items-center justify-between gap-4 text-sm font-semibold text-white hover:text-blue-300 transition-colors font-display"
                >
                  <span>{faq.q}</span>
                  <ChevronDown
                    className={`w-4 h-4 text-zinc-500 transition-transform duration-200 shrink-0 ${
                      isOpen ? 'rotate-180 text-blue-400' : ''
                    }`}
                  />
                </button>
                {isOpen && (
                  <p className="mt-3 text-xs sm:text-sm text-zinc-400 leading-relaxed pr-6 font-normal">
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
