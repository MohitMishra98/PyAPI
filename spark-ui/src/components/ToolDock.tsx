import React, { useState } from 'react';
import { Mail, Calendar, FileText, MessageSquare, GitBranch, CheckCircle2, BookOpen, Database } from 'lucide-react';

export const ToolDock: React.FC = () => {
  const [activeAppIndex, setActiveAppIndex] = useState<number>(0);

  const tools = [
    {
      name: 'Gmail',
      category: 'Email',
      icon: Mail,
      color: 'text-red-400',
      bgColor: 'bg-red-500/10 border-red-500/20',
      action: 'Audits unread threads, categorizes urgent executive emails, and drafts replies ready for your sign-off.'
    },
    {
      name: 'Google Calendar',
      category: 'Scheduling',
      icon: Calendar,
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/10 border-blue-500/20',
      action: 'Detects schedule collisions in advance and prepares conflict-free meeting reschedules.'
    },
    {
      name: 'Google Docs',
      category: 'Documents',
      icon: FileText,
      color: 'text-sky-400',
      bgColor: 'bg-sky-500/10 border-sky-500/20',
      action: 'Synthesizes research, morning intelligence memos, and weekly briefs directly into shared team docs.'
    },
    {
      name: 'Slack',
      category: 'Communication',
      icon: MessageSquare,
      color: 'text-emerald-400',
      bgColor: 'bg-emerald-500/10 border-emerald-500/20',
      action: 'Broadcasts executive updates and delivers one-tap approval buttons directly to your team channels.'
    },
    {
      name: 'GitHub',
      category: 'Code & DevOps',
      icon: GitBranch,
      color: 'text-purple-400',
      bgColor: 'bg-purple-500/10 border-purple-500/20',
      action: 'Replicates integration test failures in isolated cloud sandboxes, writes patches, and opens pull requests.'
    },
    {
      name: 'Linear',
      category: 'Project Tracking',
      icon: CheckCircle2,
      color: 'text-indigo-400',
      bgColor: 'bg-indigo-500/10 border-indigo-500/20',
      action: 'Auto-triages incoming customer bug reports, prioritizes sprints, and updates milestone progress.'
    },
    {
      name: 'Notion',
      category: 'Knowledge Base',
      icon: BookOpen,
      color: 'text-amber-400',
      bgColor: 'bg-amber-500/10 border-amber-500/20',
      action: 'Keeps team wikis, project documentation, and standard operating procedures continuously up to date.'
    },
    {
      name: 'PostgreSQL',
      category: 'Databases',
      icon: Database,
      color: 'text-cyan-400',
      bgColor: 'bg-cyan-500/10 border-cyan-500/20',
      action: 'Executes read-only analytical queries across application telemetry to spot user churn or errors.'
    }
  ];

  const activeTool = tools[activeAppIndex];
  const ActiveIcon = activeTool.icon;

  return (
    <section className="py-24 border-t border-[#1b2230] bg-[#070a10]">
      <div className="max-w-5xl mx-auto px-6">
        <div className="max-w-2xl mb-12 text-center mx-auto">
          <div className="text-xs font-mono text-blue-400 mb-2">
            Tool Integrations
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-white font-display mb-3">
            Connects to the tools you already rely on.
          </h2>
          <p className="text-sm text-zinc-400 leading-relaxed">
            Hover or tap any application to see what Spark automates with it.
          </p>
        </div>

        {/* The Dock */}
        <div className="flex flex-wrap items-center justify-center gap-3 mb-8 bg-[#0b0f17] p-3 rounded-2xl border border-[#1b2332] max-w-3xl mx-auto">
          {tools.map((tool, idx) => {
            const Icon = tool.icon;
            const isSelected = activeAppIndex === idx;

            return (
              <button
                key={idx}
                onClick={() => setActiveAppIndex(idx)}
                onMouseEnter={() => setActiveAppIndex(idx)}
                className={`p-3 rounded-xl flex items-center gap-2.5 transition-all duration-200 ${
                  isSelected
                    ? 'bg-[#182132] border border-blue-500/40 text-white shadow-lg shadow-blue-500/10 scale-105'
                    : 'bg-[#0e131d] border border-[#1b2434] text-zinc-400 hover:text-zinc-200 hover:border-zinc-700'
                }`}
              >
                <Icon className={`w-4 h-4 ${isSelected ? tool.color : 'text-zinc-400'}`} />
                <span className="text-xs font-medium hidden sm:inline">
                  {tool.name}
                </span>
              </button>
            );
          })}
        </div>

        {/* Dynamic Highlight Card */}
        <div className="max-w-xl mx-auto rounded-xl border border-[#212b3c] bg-[#0c1017] p-6 text-center shadow-xl transition-all duration-300">
          <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center mx-auto mb-4 text-blue-400">
            <ActiveIcon className="w-6 h-6" />
          </div>
          <div className="text-sm font-bold text-white font-display mb-1">
            Spark with {activeTool.name}
          </div>
          <div className="text-[11px] font-mono text-zinc-500 mb-3">
            {activeTool.category}
          </div>
          <p className="text-xs sm:text-sm text-zinc-300 leading-relaxed max-w-md mx-auto">
            {activeTool.action}
          </p>
        </div>
      </div>
    </section>
  );
};
