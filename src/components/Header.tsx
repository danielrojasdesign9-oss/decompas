import { useState } from "react";

interface HeaderProps {
  onScrollToSection: (sectionId: string) => void;
}

export default function Header({ onScrollToSection }: HeaderProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-background/95 backdrop-blur-md w-full top-0 z-50 border-b border-on-surface/10 shadow-[0_4px_30px_rgba(0,0,0,0.1)] sticky" id="app-header">
      <div className="flex justify-between items-center w-full h-20 px-6 md:px-20 max-w-7xl mx-auto">
        {/* Logo */}
        <div 
          onClick={() => onScrollToSection("hero")}
          className="font-display italic font-bold text-2xl text-secondary cursor-pointer hover:opacity-90 transition-opacity tracking-tight"
        >
          DECOMPAS
        </div>

        {/* Desktop Nav */}
        <div className="hidden md:flex items-center gap-8">
          <button 
            onClick={() => onScrollToSection("servicios")}
            className="font-display text-[11px] uppercase tracking-widest text-on-surface hover:text-secondary transition-colors duration-300 font-semibold cursor-pointer"
          >
            Servicios
          </button>
          
          <button 
            onClick={() => onScrollToSection("proceso")}
            className="font-display text-[11px] uppercase tracking-widest text-on-surface hover:text-secondary transition-colors duration-300 font-semibold cursor-pointer"
          >
            Proceso
          </button>

          <a 
            href="mailto:decompasdesign@gmail.com?subject=Inquiry"
            className="font-display text-[11px] uppercase tracking-widest text-on-surface hover:text-secondary transition-colors duration-300 font-semibold"
          >
            Correo
          </a>
          
          <button 
            onClick={() => onScrollToSection("cta-section")}
            className="bg-secondary text-on-secondary font-display text-[11px] uppercase tracking-widest px-6 py-3 rounded-full hover:scale-105 transition-all duration-200 font-bold cursor-pointer"
          >
            WhatsApp
          </button>
        </div>

        {/* Mobile menu button */}
        <div className="md:hidden flex items-center gap-2">
          <button
            onClick={() => onScrollToSection("cta-section")}
            className="px-3 py-1.5 rounded-full border border-secondary/35 text-secondary font-display text-[10px] uppercase font-bold"
          >
            WhatsApp
          </button>
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="p-1.5 text-secondary focus:outline-none cursor-pointer"
            id="mobile-menu-btn"
          >
            <span className="material-symbols-outlined block" style={{ fontSize: "28px" }}>
              {isOpen ? "close" : "menu"}
            </span>
          </button>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {isOpen && (
        <div className="md:hidden w-full bg-background border-b border-on-surface/10 px-6 py-4 flex flex-col gap-4 animate-fadeIn" id="mobile-menu">
          <button 
            onClick={() => {
              onScrollToSection("servicios");
              setIsOpen(false);
            }}
            className="text-left py-2 font-display text-xs uppercase tracking-widest text-on-surface hover:text-secondary transition-colors"
          >
            Servicios
          </button>
          <button 
            onClick={() => {
              onScrollToSection("proceso");
              setIsOpen(false);
            }}
            className="text-left py-2 font-display text-xs uppercase tracking-widest text-on-surface hover:text-secondary transition-colors"
          >
            Proceso
          </button>
          <a 
            href="mailto:decompasdesign@gmail.com?subject=Inquiry"
            onClick={() => setIsOpen(false)}
            className="text-left py-2 font-display text-xs uppercase tracking-widest text-on-surface hover:text-secondary transition-colors"
          >
            Enviar Correo
          </a>
          
          <button 
            onClick={() => {
              onScrollToSection("cta-section");
              setIsOpen(false);
            }}
            className="w-full text-center py-3.5 bg-secondary text-on-secondary font-display text-xs uppercase tracking-widest rounded-full font-bold"
          >
            Contactar por WhatsApp
          </button>
        </div>
      )}
    </nav>
  );
}
