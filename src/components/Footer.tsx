interface FooterProps {
  onScrollToSection: (sectionId: string) => void;
}

export default function Footer({ onScrollToSection }: FooterProps) {
  return (
    <footer className="bg-background border-t border-on-surface/10 py-16 md:py-24 w-full" id="app-footer">
      <div className="flex flex-col md:flex-row justify-between items-start gap-12 px-6 md:px-20 max-w-7xl mx-auto">
        <div className="mb-8 md:mb-0 text-left">
          <div className="font-display italic text-3xl font-bold text-on-surface mb-4">DECOMPAS</div>
          <p className="font-sans text-sm text-on-surface/80 opacity-80 max-w-xs leading-relaxed font-light">
            Agencia de diseño y tecnología enfocada en escalar operaciones mediante digitalización.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-12 sm:gap-24 text-left">
          {/* Navigation */}
          <div className="flex flex-col gap-4">
            <h4 className="font-display text-xs uppercase tracking-widest text-secondary font-bold">Navegación</h4>
            <button 
              onClick={() => onScrollToSection("servicios")}
              className="text-left font-sans text-sm text-on-surface/80 opacity-80 hover:text-secondary hover:opacity-100 transition-colors duration-300 font-light cursor-pointer"
            >
              Servicios
            </button>
            <button 
              onClick={() => onScrollToSection("proceso")}
              className="text-left font-sans text-sm text-on-surface/80 opacity-80 hover:text-secondary hover:opacity-100 transition-colors duration-300 font-light cursor-pointer"
            >
              Proceso
            </button>
          </div>

          {/* Contact */}
          <div className="flex flex-col gap-4">
            <h4 className="font-display text-xs uppercase tracking-widest text-secondary font-bold">Contacto</h4>
            <button 
              onClick={() => onScrollToSection("cta-section")}
              className="text-left font-sans text-sm text-on-surface/80 opacity-80 hover:text-secondary hover:opacity-100 transition-colors duration-300 font-light cursor-pointer"
            >
              WhatsApp
            </button>
            <span 
              className="text-left font-sans text-sm text-on-surface/80 opacity-80"
            >
              Protección de Datos
            </span>
          </div>
        </div>
      </div>

      <div className="mt-16 px-6 md:px-20 max-w-7xl mx-auto border-t border-on-surface/10 pt-8 text-left">
        <p className="font-sans text-xs text-on-surface/60 opacity-60">
          © 2026 DECOMPAS. Digital Agency. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
