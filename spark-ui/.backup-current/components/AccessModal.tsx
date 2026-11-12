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
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div 
        className="relative w-full max-w-sm rounded-xl bg-[#0c0c0c] border border-white/[0.1] shadow-2xl p-6"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={handleReset}
          className="absolute top-4 right-4 text-zinc-400 hover:text-white"
        >
          <X className="w-4 h-4" />
        </button>

        {!submitted ? (
          <div>
            <h3 className="text-sm font-semibold text-white mb-1.5 font-sans">
              Request access to Spark
            </h3>
            <p className="text-xs text-zinc-400 mb-5 leading-relaxed">
              We are onboarding teams in batches. Enter your work email to receive an invitation to provision your cloud sandbox.
            </p>

            <form onSubmit={handleSubmit} className="space-y-3">
              <div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@company.com"
                  className="w-full px-3.5 py-2.5 rounded-lg bg-white/[0.04] border border-white/[0.1] text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-white/30"
                />
              </div>

              <button
                type="submit"
                className="w-full py-2.5 rounded-lg bg-white hover:bg-zinc-200 text-black font-semibold text-xs transition-colors"
              >
                Join access list
              </button>
            </form>
          </div>
        ) : (
          <div className="text-center py-4 space-y-3">
            <div className="w-8 h-8 rounded-full bg-white/[0.08] text-white flex items-center justify-center mx-auto">
              <Check className="w-4 h-4" />
            </div>
            <h4 className="text-sm font-semibold text-white">
              Request received
            </h4>
            <p className="text-xs text-zinc-400 leading-relaxed">
              We've noted <span className="text-zinc-200 font-mono">{email}</span> and will reach out with early sandbox access.
            </p>
            <button
              onClick={handleReset}
              className="mt-2 text-xs text-zinc-400 hover:text-white underline"
            >
              Close
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
