import React, { useState } from 'react';
import { Zap, Menu, X } from 'lucide-react';

interface NavbarProps {
  onOpenAccess: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onOpenAccess }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#000000]/80 backdrop-blur-md border-b border-white/[0.06]">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Brand */}
        <a href="#" className="flex items-center gap-2">
          <div className="w-5 h-5 rounded-md bg-white flex items-center justify-center">
            <Zap className="w-3 h-3 text-black fill-black" />
          </div>
          <span className="text-sm font-semibold tracking-tight text-white font-sans">
            Spark
          </span>
        </a>

        {/* Center Nav */}
        <nav className="hidden md:flex items-center gap-8 text-xs text-zinc-400">
          <a href="#how-it-works" className="hover:text-white transition-colors">
            How it works
          </a>
          <a href="#capabilities" className="hover:text-white transition-colors">
            Capabilities
          </a>
          <a href="#security" className="hover:text-white transition-colors">
            Security
          </a>
          <a href="#pricing" className="hover:text-white transition-colors">
            Pricing
          </a>
        </nav>

        {/* Right CTA */}
        <div className="hidden md:flex items-center gap-4">
          <button
            onClick={onOpenAccess}
            className="text-xs text-zinc-400 hover:text-white transition-colors"
          >
            Sign in
          </button>
          <button
            onClick={onOpenAccess}
            className="text-xs font-medium text-black bg-white hover:bg-zinc-200 px-3.5 py-1.5 rounded-md transition-colors"
          >
            Get access
          </button>
        </div>

        {/* Mobile toggle */}
        <div className="flex md:hidden">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="text-zinc-400 hover:text-white p-1"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-[#0a0a0a] border-b border-white/[0.08] px-6 py-4 space-y-3">
          <a
            href="#how-it-works"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-xs text-zinc-400 hover:text-white py-1.5"
          >
            How it works
          </a>
          <a
            href="#capabilities"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-xs text-zinc-400 hover:text-white py-1.5"
          >
            Capabilities
          </a>
          <a
            href="#security"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-xs text-zinc-400 hover:text-white py-1.5"
          >
            Security
          </a>
          <a
            href="#pricing"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-xs text-zinc-400 hover:text-white py-1.5"
          >
            Pricing
          </a>
          <div className="pt-2 border-t border-white/[0.06] flex items-center justify-between">
            <button
              onClick={() => {
                setMobileMenuOpen(false);
                onOpenAccess();
              }}
              className="text-xs text-zinc-300"
            >
              Sign in
            </button>
            <button
              onClick={() => {
                setMobileMenuOpen(false);
                onOpenAccess();
              }}
              className="text-xs font-medium text-black bg-white px-3 py-1.5 rounded-md"
            >
              Get access
            </button>
          </div>
        </div>
      )}
    </header>
  );
};
