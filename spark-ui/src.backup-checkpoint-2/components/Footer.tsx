import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-[#1b2230] py-12 bg-[#05070a] text-xs text-zinc-500">
      <div className="max-w-6xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-6">
        {/* Brand */}
        <div className="flex items-center gap-2.5">
          <div className="w-5 h-5 rounded bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center">
            <svg
              className="w-3 h-3 text-white"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
            </svg>
          </div>
          <span className="font-bold text-white text-sm font-display">Spark</span>
        </div>

        {/* Links */}
        <div className="flex items-center gap-6 text-xs text-zinc-400">
          <a href="#how-it-works" className="hover:text-white transition-colors">
            How it works
          </a>
          <a href="#use-cases" className="hover:text-white transition-colors">
            Use cases
          </a>
          <a href="#pricing" className="hover:text-white transition-colors">
            Pricing
          </a>
          <a href="#faq" className="hover:text-white transition-colors">
            FAQ
          </a>
        </div>

        {/* Status */}
        <div className="flex items-center gap-2 text-[11px] font-mono text-zinc-400 bg-[#0c1017] px-3 py-1.5 rounded border border-[#1b2332]">
          <span className="w-2 h-2 rounded-full bg-emerald-400" />
          <span>All systems operational</span>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 mt-8 pt-6 border-t border-[#121824] text-[11px] text-zinc-600 font-mono text-center sm:text-left">
        © {new Date().getFullYear()} Spark Technologies Inc. All rights reserved.
      </div>
    </footer>
  );
};
