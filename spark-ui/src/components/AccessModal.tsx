import React, { useState } from 'react';
import { X, Check } from 'lucide-react';

interface AccessModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AccessModal: React.FC<AccessModalProps> = ({ isOpen, onClose }) => {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      setSubmitted(true);
    }
  };

  const handleReset = () => {
    setSubmitted(false);
    setEmail('');
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md">
      <div
        className="relative w-full max-w-sm rounded-xl bg-[#0c1017] border border-[#212c3f] shadow-2xl p-6 text-left"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={handleReset}
          className="absolute top-4 right-4 text-zinc-400 hover:text-white p-1"
          aria-label="Close"
        >
          <X className="w-4 h-4" />
        </button>

        {!submitted ? (
          <div>
            <h3 className="text-base font-bold text-white font-display mb-1.5">
              Start your 14-day free trial
            </h3>
            <p className="text-xs text-zinc-400 mb-5 leading-relaxed">
              No credit card required. Connect your tools and let Spark handle multi-step tasks in the background.
            </p>

            <form onSubmit={handleSubmit} className="space-y-3">
              <div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your work email"
                  className="w-full px-3.5 py-2.5 rounded-md bg-[#080c13] border border-[#1e2738] text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-blue-500 font-mono transition-colors"
                />
              </div>

              <button
                type="submit"
                className="w-full py-2.5 rounded-md bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs transition-colors shadow-md shadow-blue-600/30"
              >
                Create free trial account
              </button>
            </form>
          </div>
        ) : (
          <div className="text-center py-4 space-y-3">
            <div className="w-9 h-9 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center justify-center mx-auto">
              <Check className="w-4 h-4 stroke-[2.5]" />
            </div>
            <div>
              <h4 className="text-sm font-semibold text-white font-display mb-1">
                Trial invitation sent
              </h4>
              <p className="text-xs text-zinc-400 leading-relaxed">
                We've sent an activation link to <span className="text-blue-300 font-mono">{email}</span>. Click it to set up your workspace.
              </p>
            </div>
            <button
              onClick={handleReset}
              className="mt-2 text-xs text-zinc-400 hover:text-white underline font-mono"
            >
              Close
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
