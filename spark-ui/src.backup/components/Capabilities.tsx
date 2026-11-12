import React from 'react';
import { GitBranch, Clock, BrainCircuit, Lock } from 'lucide-react';

export const Capabilities: React.FC = () => {
  const capabilities = [
    {
      icon: GitBranch,
      title: 'Milestone decomposition graph',
      description: 'Breaks high-level objectives into sequential micro-milestones. Resolves prerequisites, retries on transient errors, and adapts execution paths dynamically.'
    },
    {
      icon: Clock,
      title: 'Scheduled autonomous crons',
      description: 'Configure agents to trigger on schedule—running daily morning scans, triaging customer churn, or preparing release notes before you wake up.'
    },
    {
      icon: BrainCircuit,
      title: 'Adaptive procedural skills',
      description: 'Define your team’s tone, code review checklist, or compliance rubric once. Spark preserves them as persistent operational routines across all workflows.'
    },
    {
      icon: Lock,
      title: 'Zero-retention ephemeral isolation',
      description: 'Workflows execute in isolated Linux containers that are destroyed upon completion. No customer data or code is ever retained or used to train models.'
    }
  ];

  return (
    <section id="capabilities" className="py-24 border-t border-white/[0.06]">
      <div className="max-w-6xl mx-auto px-6">
        <div className="max-w-xl mb-16">
          <div className="text-xs font-mono text-zinc-500 mb-2">Capabilities</div>
          <h2 className="text-2xl sm:text-3xl font-semibold tracking-tight text-white">
            Built for enterprise-grade execution.
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-16 gap-y-12">
          {capabilities.map((cap, idx) => {
            const Icon = cap.icon;
            return (
              <div key={idx} className="space-y-3">
                <div className="flex items-center gap-2.5">
                  <Icon className="w-4 h-4 text-zinc-400" />
                  <h3 className="text-sm font-semibold text-white">
                    {cap.title}
                  </h3>
                </div>
                <p className="text-xs text-zinc-400 leading-relaxed pl-6">
                  {cap.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
