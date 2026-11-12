import { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { CoreBenefits } from './components/CoreBenefits';
import { DayTimeline } from './components/DayTimeline';
import { ToolDock } from './components/ToolDock';
import { UseCases } from './components/UseCases';
import { Pricing } from './components/Pricing';
import { Faq } from './components/Faq';
import { Footer } from './components/Footer';
import { AccessModal } from './components/AccessModal';

export default function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#07090e] text-[#e5e9f0] selection:bg-blue-600/30 selection:text-white">
      <Navbar onOpenAccess={() => setIsModalOpen(true)} />
      <main>
        <Hero onOpenAccess={() => setIsModalOpen(true)} />
        <CoreBenefits />
        <DayTimeline />
        <ToolDock />
        <UseCases />
        <Pricing onOpenAccess={() => setIsModalOpen(true)} />
        <Faq />
      </main>
      <Footer />
      <AccessModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </div>
  );
}
