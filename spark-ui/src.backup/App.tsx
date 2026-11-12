import { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { HowItWorks } from './components/HowItWorks';
import { Capabilities } from './components/Capabilities';
import { Security } from './components/Security';
import { Pricing } from './components/Pricing';
import { Faq } from './components/Faq';
import { Footer } from './components/Footer';
import { AccessModal } from './components/AccessModal';

export default function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#000000] text-[#ececed]">
      <Navbar onOpenAccess={() => setIsModalOpen(true)} />
      <main>
        <Hero onOpenAccess={() => setIsModalOpen(true)} />
        <HowItWorks />
        <Capabilities />
        <Security />
        <Pricing onOpenAccess={() => setIsModalOpen(true)} />
        <Faq />
      </main>
      <Footer />
      <AccessModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </div>
  );
}
